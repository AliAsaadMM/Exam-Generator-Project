# -*- coding: utf-8 -*-
"""
خدمات الذكاء الاصطناعي المعتمدة على نموذج gemini-3.6-flash
"""

from google import genai
from google.genai import types
from core.subject_presets import get_subject_preset

DEFAULT_MODEL = "gemini-3.6-flash"


def _get_client(api_key: str) -> genai.Client:
    if not api_key or not api_key.strip():
        raise ValueError("يرجى إدخال مفتاح Gemini API Key أولاً.")
    return genai.Client(api_key=api_key.strip())


def extract_handwritten_questions(
    images: list[tuple[bytes, str]],
    api_key: str,
    subject_key: str = "math",
    model_name: str = DEFAULT_MODEL,
) -> str:
    """استخراج الأسئلة المكتوبة بخط اليد أو المصورة وتنسيقها وفق النمط الوزاري العراقي."""
    client = _get_client(api_key)
    preset = get_subject_preset(subject_key)

    prompt = f"""
أنت خبير تربوي عراقي في صياغة وطباعة الأسئلة الوزارية لمادة ({preset['name']}).
استخرج جميع الأسئلة والفروع والدرجات الموجودة في الصور المرفقة بدقة تامة.
القواعد الصارمة:
1. اكتب المعادلات الرياضية والكيميائية والفيزيائية بصيغة LaTeX صحيحة محصورة بـ $...$ أو $$...$$.
2. نسّق الأسئلة على شكل (س1: [20 درجة]) والفروع (A. ... B. ...).
3. أعد نص الأسئلة المنسق فقط بدون أي مقدمات أو شروحات إضافية.
"""

    contents: list = [prompt]
    for img_bytes, mime_type in images:
        contents.append(types.Part.from_bytes(data=img_bytes, mime_type=mime_type))

    response = client.models.generate_content(
        model=model_name or DEFAULT_MODEL,
        contents=contents,
    )
    return (response.text or "").strip()


def extract_text_from_pdf_book(pdf_bytes: bytes) -> str:
    """استخراج النصوص من صفحات الكتاب المدرسي بصيغة PDF."""
    import fitz  # PyMuPDF

    extracted_pages = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if text:
                extracted_pages.append(f"--- صفحة {page_num} ---\n{text}")
    return "\n\n".join(extracted_pages)


def select_questions_from_book(
    images: list[tuple[bytes, str]],
    pdf_texts: list[str],
    num_questions: int,
    criteria: str,
    api_key: str,
    subject_key: str = "math",
    model_name: str = DEFAULT_MODEL,
) -> str:
    """انتقاء وصياغة أسئلة وزارية من محتوى الكتاب المدرسي أو الملزمة."""
    client = _get_client(api_key)
    preset = get_subject_preset(subject_key)

    book_context = "\n\n".join(pdf_texts)[:35000]
    extra_rules = f"شروط إضافية من المدرس: {criteria}" if criteria.strip() else ""

    prompt = f"""
أنت واضع أسئلة وزارية عراقي لمادة ({preset['name']}).
بالاعتماد على محتوى الكتاب/الملزمة المرفق، اختر وصُغ ({num_questions}) أسئلة امتحانية بمستوى الأسئلة الوزارية العراقية.
{extra_rules}

القواعد:
- وزّع الدرجات والفروع (A, B) بشكل منطقي.
- اكتب جميع المعادلات والرموز العلمية بصيغة LaTeX ($...$ أو $$...$$).
- أعد نص الأسئلة الجاهز للطباعة فقط بدون أي مقدمات.

محتوى الكتاب النصي:
{book_context}
"""

    contents: list = [prompt]
    for img_bytes, mime_type in images:
        contents.append(types.Part.from_bytes(data=img_bytes, mime_type=mime_type))

    response = client.models.generate_content(
        model=model_name or DEFAULT_MODEL,
        contents=contents,
    )
    return (response.text or "").strip()


def generate_ministerial_exam_ai(
    subject_key: str,
    grade: str,
    exam_type: str,
    topics: str,
    api_key: str,
    num_questions: int = 6,
    model_name: str = DEFAULT_MODEL,
) -> str:
    """توليد نموذج أسئلة امتحانية وزارية متكاملة حسب المادة والصف والفصول."""
    client = _get_client(api_key)
    preset = get_subject_preset(subject_key)

    prompt = f"""
صمم نموذج أسئلة امتحانية رسمية وفق المنهج العراقي الحديث بالمواصفات التالية:
- المادة: {preset['name']}
- الصف الدراسي: {grade}
- نوع الامتحان: {exam_type}
- المواضيع والفصول المشمولة: {topics or 'المنهج المقرر كاملاً'}
- عدد الأسئلة الكلي: {num_questions} أسئلة

تعليمات التنسيق:
- ابدأ كل سؤال بـ (س1: [20 درجة]) أو (Q1: [20 Marks]) حسب لغة المادة.
- نوّع بين الفروع (A, B) والمسائل والتعاريف والمقارنات والتعاليل حسب طبيعة المادة.
- استخدم صيغ LaTeX للمعادلات الرياضية والكيميائية ($...$ و $$...$$).
- أعد ورقة الأسئلة مباشرة دون أي كلام تمهيدي.
"""

    response = client.models.generate_content(
        model=model_name or DEFAULT_MODEL,
        contents=prompt,
    )
    return (response.text or "").strip()


def fix_and_polish_exam_text(
    raw_text: str,
    api_key: str,
    subject_key: str = "math",
    model_name: str = DEFAULT_MODEL,
) -> str:
    """تدقيق وإصلاح التنسيق وصيغ LaTeX والأقواس وترقيم الفروع والدرجات."""
    client = _get_client(api_key)
    preset = get_subject_preset(subject_key)

    prompt = f"""
راجع ودقق نص الأسئلة الامتحانية التالي لمادة ({preset['name']}) وفق المعايير الوزارية العراقية:
1. صحح أي أخطاء إملائية أو نحوية أو علمية.
2. اضبط جميع المعادلات والرموز بصيغة LaTeX سليمة محصورة بـ $...$ أو $$...$$.
3. وحّد تنسيق ترقيم الأسئلة (س1: [20 درجة]) والفروع (A. و B.) والدرجات.
4. حافظ على أوسمة الرسومات والصور مثل [diagram: ...] و [صورة: ...] كما هي تماماً دون حذفها.
5. أعد النص المصحح النهائي فقط بدون أي تعليقات.

النص المراد تدقيقه:
{raw_text}
"""

    response = client.models.generate_content(
        model=model_name or DEFAULT_MODEL,
        contents=prompt,
    )
    return (response.text or "").strip()