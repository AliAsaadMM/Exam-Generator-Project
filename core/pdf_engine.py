# -*- coding: utf-8 -*-
"""
محرك بناء ورقة الأسئلة الامتحانية (HTML) وتصديرها إلى ملف PDF عالي الدقة
"""

import html
import re
from core.diagram_generator import execute_custom_python_diagram
from core.subject_presets import get_subject_preset


def _render_markdown_tables(lines: list[str]) -> str:
    """تحويل جداول Markdown إلى جداول HTML منسقة للطباعة."""
    output = []
    table_buffer = []

    def flush_table():
        if not table_buffer:
            return
        rows = [
            [cell.strip() for cell in row.strip().strip("|").split("|")]
            for row in table_buffer
        ]
        # تجاهل سطر الفاصل |:---|:---|
        clean_rows = [
            r for r in rows if not all(re.match(r"^:?-{2,}:?$", c) for c in r if c)
        ]
        if not clean_rows:
            table_buffer.clear()
            return

        html_tbl = ["<table class='exam-table'><thead><tr>"]
        for th in clean_rows[0]:
            html_tbl.append(f"<th>{th}</th>")
        html_tbl.append("</tr></thead><tbody>")
        for tr in clean_rows[1:]:
            html_tbl.append("<tr>")
            for td in tr:
                html_tbl.append(f"<td>{td}</td>")
            html_tbl.append("</tr>")
        html_tbl.append("</tbody></table>")
        output.append("".join(html_tbl))
        table_buffer.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            table_buffer.append(stripped)
        else:
            flush_table()
            output.append(line)

    flush_table()
    return "\n".join(output)


def _format_exam_body(text_content: str, user_images: dict | None = None) -> str:
    """تنسيق نص الأسئلة وتحويل الأوسمة والجداول والأبيات الشعرية."""
    user_images = user_images or {}
    safe_text = html.escape(text_content)

    # 1. معالجة الجداول
    processed = _render_markdown_tables(safe_text.splitlines())

    # 2. استبدال أوسمة الرسومات الهندسية [diagram: name]
    def repl_diagram(match):
        return execute_custom_python_diagram(match.group(1))

    processed = re.sub(r"\[diagram:\s*([a-zA-Z0-9_]+)\]", repl_diagram, processed)

    # 3. استبدال أوسمة الصور المرفوعة [صورة: 1]
    def repl_image(match):
        img_id = match.group(1).strip()
        data_url = user_images.get(img_id)
        if data_url:
            return (
                f"<div style='text-align:center;margin:8px 0;'>"
                f"<img src='{data_url}' style='max-width:260px;max-height:190px;border:1px solid #cbd5e1;border-radius:4px;'/>"
                f"</div>"
            )
        return f"<div style='color:#b91c1c;font-size:12px;'>[صورة رقم {img_id} غير مرفوعة]</div>"

    processed = re.sub(r"\[صورة:\s*(\d+)\]", repl_image, processed)

    # 4. تنسيق الأبيات الشعرية (صدر البيت ... عجز البيت)
    final_lines = []
    for line in processed.splitlines():
        s = line.strip()
        if "..." in s and not s.startswith("<") and not s.startswith("$$"):
            parts = s.split("...", 1)
            final_lines.append(
                f"<div class='poetry-line'>"
                f"<span>{parts[0].strip()}</span>"
                f"<span>{parts[1].strip()}</span>"
                f"</div>"
            )
        elif re.match(r"^(س\d+|Q\d+)\s*:", s):
            # تمييز رأس السؤال
            s_bold = re.sub(r"(\[.*?\])", r"<span class='mark-badge'>\1</span>", s)
            final_lines.append(f"<div class='question-header'>{s_bold}</div>")
        elif s == "":
            final_lines.append("<div class='spacer'></div>")
        else:
            s_styled = re.sub(r"(\[.*?\])", r"<span class='mark-badge'>\1</span>", line)
            final_lines.append(f"<div class='question-line'>{s_styled}</div>")

    return "\n".join(final_lines)


def build_exam_html(
    metadata: dict,
    text_content: str,
    font_scale: float = 1.0,
    page_size_mode: str = "full",
    layout_mode: str = "single",
    user_images: dict | None = None,
) -> str:
    """بناء مستند HTML متكامل لورقة الامتحان مع دعم KaTeX للمعادلات."""
    preset = get_subject_preset(metadata.get("subject_key", "math"))
    is_rtl = preset["is_rtl"]
    direction = "rtl" if is_rtl else "ltr"
    base_font_px = round(14 * font_scale, 2)

    page_css_size = {
        "full": "A4 portrait",
        "auto": "A4 portrait",
        "half": "210mm 148mm",
        "a5": "A5 portrait",
    }.get(page_size_mode, "A4 portrait")

    columns_css = (
        "column-count: 2; column-gap: 18px; column-rule: 1px solid #94a3b8;"
        if layout_mode == "two_columns"
        else "column-count: 1;"
    )

    body_html = _format_exam_body(text_content, user_images=user_images)

    constants_block = ""
    if metadata.get("constants_text", "").strip():
        constants_block = f"""
        <div class="constants-box">
            <strong>{html.escape(metadata.get('constants_title', ''))}</strong>
            <span>{html.escape(metadata.get('constants_text', ''))}</span>
        </div>
        """

    lbl_republic = "جمهورية العراق<br>وزارة التربية" if is_rtl else "Republic of Iraq<br>Ministry of Education"
    lbl_subject = f"المادة: {html.escape(metadata.get('subject', ''))}" if is_rtl else f"Subject: {html.escape(metadata.get('subject', ''))}"
    lbl_grade = f"الصف: {html.escape(metadata.get('grade', ''))}" if is_rtl else f"Grade: {html.escape(metadata.get('grade', ''))}"
    lbl_time = f"الوقت: {html.escape(metadata.get('time_limit', ''))}" if is_rtl else f"Time: {html.escape(metadata.get('time_limit', ''))}"
    lbl_year = f"العام الدراسي: {html.escape(metadata.get('academic_year', ''))}" if is_rtl else f"Year: {html.escape(metadata.get('academic_year', ''))}"

    return f"""<!DOCTYPE html>
<html lang="{'ar' if is_rtl else 'en'}" dir="{direction}">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '$', right: '$', display: false}}
    ]}});"></script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    @page {{
        size: {page_css_size};
        margin: 10mm 12mm;
    }}
    body {{
        font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif;
        font-size: {base_font_px}px;
        line-height: 1.65;
        color: #0f172a;
        background: #ffffff;
        margin: 0;
        padding: 12px;
    }}
    .exam-sheet {{
        border: 2px solid #0f172a;
        border-radius: 6px;
        padding: 12px 15px;
    }}
    .header-grid {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #0f172a;
        padding-bottom: 8px;
        margin-bottom: 8px;
    }}
    .header-col {{
        width: 34%;
        font-weight: 700;
        font-size: 0.92em;
        line-height: 1.5;
    }}
    .header-center {{
        width: 30%;
        text-align: center;
    }}
    .header-center img {{
        width: 52px;
        height: auto;
    }}
    .exam-title-banner {{
        font-weight: 800;
        font-size: 1.02em;
        color: #1e3a8a;
        margin-top: 2px;
    }}
    .general-note {{
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        padding: 4px 10px;
        font-weight: 700;
        font-size: 0.9em;
        margin-bottom: 10px;
        text-align: center;
    }}
    .questions-container {{
        {columns_css}
    }}
    .question-header {{
        font-weight: 800;
        color: #1e3a8a;
        margin-top: 8px;
        margin-bottom: 3px;
        border-bottom: 1px dashed #cbd5e1;
        padding-bottom: 2px;
    }}
    .question-line {{
        margin-bottom: 3px;
    }}
    .mark-badge {{
        font-weight: 700;
        color: #0f172a;
        font-size: 0.9em;
    }}
    .poetry-line {{
        display: flex;
        justify-content: space-around;
        font-weight: 700;
        margin: 5px 0;
        padding: 2px 16px;
    }}
    .exam-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 8px 0;
        font-size: 0.9em;
    }}
    .exam-table th, .exam-table td {{
        border: 1px solid #334155;
        padding: 5px 8px;
        text-align: center;
    }}
    .exam-table th {{
        background-color: #e2e8f0;
        font-weight: 800;
    }}
    .spacer {{
        height: 6px;
    }}
    .constants-box {{
        margin-top: 10px;
        padding: 6px 10px;
        border: 1px solid #64748b;
        border-radius: 4px;
        background: #f8fafc;
        font-size: 0.88em;
        text-align: center;
    }}
    .exam-footer {{
        margin-top: 12px;
        padding-top: 6px;
        border-top: 1.5px solid #0f172a;
        display: flex;
        justify-content: space-between;
        font-weight: 700;
        font-size: 0.88em;
    }}
</style>
</head>
<body>
<div class="exam-sheet">
    <div class="header-grid">
        <div class="header-col">
            <div>{lbl_republic}</div>
            <div>{html.escape(metadata.get('school_name', ''))}</div>
            <div>{lbl_year}</div>
        </div>
        <div class="header-center">
            <img src="https://upload.wikimedia.org/wikipedia/commons/f/f6/Coat_of_arms_of_Iraq.svg" alt="Iraq">
            <div class="exam-title-banner">{html.escape(metadata.get('exam_type', ''))} ({html.escape(metadata.get('session', ''))})</div>
        </div>
        <div class="header-col" style="text-align: {'left' if is_rtl else 'right'};">
            <div>{lbl_subject}</div>
            <div>{lbl_grade}</div>
            <div>{lbl_time}</div>
        </div>
    </div>

    <div class="general-note">{html.escape(metadata.get('general_note', ''))}</div>

    <div class="questions-container">
        {body_html}
    </div>

    {constants_block}

    <div class="exam-footer">
        <span>{html.escape(metadata.get('teacher_name', ''))}</span>
        <span>{html.escape(metadata.get('motivational_quote', ''))}</span>
    </div>
</div>
</body>
</html>"""


def generate_exam_pdf(
    metadata: dict,
    text_content: str,
    output_pdf_path: str = "iraqi_exam_output.pdf",
    page_size_mode: str = "full",
    layout_mode: str = "single",
    target_pages: int | None = None,
    user_images: dict | None = None,
) -> tuple[bytes, int, bool, dict]:
    """تحويل ورقة الامتحان إلى ملف PDF مع محاولة ضبط عدد الصفحات المستهدف."""
    try:
        from weasyprint import HTML
    except ImportError as exc:
        raise RuntimeError(
            "مكتبة WeasyPrint غير مثبتة. نفّذ الأمر: pip install weasyprint"
        ) from exc

    scales_to_try = [1.0, 0.92, 0.85, 0.78] if target_pages else [1.0]
    pdf_bytes = b""
    final_pages = 1
    fit_ok = True

    for scale in scales_to_try:
        html_str = build_exam_html(
            metadata=metadata,
            text_content=text_content,
            font_scale=scale,
            page_size_mode=page_size_mode,
            layout_mode=layout_mode,
            user_images=user_images,
        )
        doc = HTML(string=html_str).render()
        final_pages = len(doc.pages)
        pdf_bytes = doc.write_pdf()

        if not target_pages or final_pages <= target_pages:
            fit_ok = True
            break
        fit_ok = False

    if output_pdf_path:
        with open(output_pdf_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes, final_pages, fit_ok, {}