# -*- coding: utf-8 -*-
"""
منصة إعداد وطباعة الأسئلة الامتحانية العراقية الرسمية
Iraqi School Examination Maker & Publisher
"""

import base64
import os
import sys
import streamlit as st

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from core.ai_service import (
    extract_handwritten_questions,
    extract_text_from_pdf_book,
    fix_and_polish_exam_text,
    generate_ministerial_exam_ai,
    select_questions_from_book,
)
from core.pdf_engine import build_exam_html, generate_exam_pdf
from core.subject_presets import (
    SUBJECT_PRESETS,
    get_subject_preset,
    list_available_subjects,
)

GEMINI_MODEL = "gemini-3.6-flash"

PAGE_SIZE_MAP = {
    "A4 كاملة": "full",
    "تلقائي (نصف صفحة عند قلة الأسئلة)": "auto",
    "A4 نصف صفحة": "half",
    "A5": "a5",
}

TARGET_PAGES_MAP = {
    "بدون تحديد": None,
    "صفحة واحدة": 1,
    "صفحتان": 2,
}

PRESET_FIELD_MAP = {
    "school_name": "default_school",
    "grade": "default_grade",
    "time_limit": "default_time",
    "academic_year": "default_academic_year",
    "exam_type": "default_exam_type",
    "session": "default_session",
    "teacher_name": "default_teacher",
    "general_note": "default_general_note",
    "constants_text": "default_constants",
}

st.set_page_config(
    page_title="صانع الأسئلة الامتحانية العراقية | Iraqi Exam Maker",
    page_icon="🇮🇶",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Cairo', sans-serif;
        }

        .stButton > button {
            font-family: 'Cairo', sans-serif;
            font-weight: 700;
            border-radius: 8px;
        }

        .main-title {
            text-align: center;
            color: #1e3a8a;
            font-size: 26px;
            font-weight: 900;
            margin-bottom: 2px;
        }

        .sub-title {
            text-align: center;
            color: #4b5563;
            font-size: 14px;
            margin-bottom: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_session_state() -> None:
    """تهيئة متغيرات الجلسة وتطبيق التحديثات المعلقة قبل رسم عناصر الواجهة."""
    if "current_subject" not in st.session_state:
        st.session_state["current_subject"] = "math"

    if st.session_state.get("pending_exam_text") is not None:
        st.session_state["exam_text"] = st.session_state["pending_exam_text"]
        st.session_state["pending_exam_text"] = None

    if "exam_text" not in st.session_state:
        st.session_state["exam_text"] = SUBJECT_PRESETS["math"]["sample_text"]

    if "user_images" not in st.session_state:
        st.session_state["user_images"] = {}

    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = os.getenv("GEMINI_API_KEY", "")

    preset_default = get_subject_preset(st.session_state["current_subject"])
    for state_key, preset_key in PRESET_FIELD_MAP.items():
        if state_key not in st.session_state:
            st.session_state[state_key] = preset_default[preset_key]

    if "motivational_quote" not in st.session_state:
        st.session_state["motivational_quote"] = preset_default["motivational_quotes"][0]

    if st.session_state.get("toast_msg"):
        st.toast(st.session_state.pop("toast_msg"))


def set_exam_text(new_text: str, toast_msg: str | None = None) -> None:
    """تحديث نص المحرر بأمان وإعادة تحميل الواجهة."""
    st.session_state["pending_exam_text"] = new_text
    if toast_msg:
        st.session_state["toast_msg"] = toast_msg
    st.rerun()


def append_to_exam_text(addition: str, toast_msg: str | None = None) -> None:
    """إضافة نص جديد إلى نهاية الأسئلة الحالية."""
    current = st.session_state.get("exam_text", "").strip()
    updated = f"{current}\n\n{addition.strip()}" if current else addition.strip()
    set_exam_text(updated, toast_msg=toast_msg)


def on_subject_change() -> None:
    """تحديث بيانات الترويسة والنموذج الافتراضي عند تغيير المادة."""
    new_sub = st.session_state["sel_subject"]
    st.session_state["current_subject"] = new_sub
    preset = get_subject_preset(new_sub)

    for state_key, preset_key in PRESET_FIELD_MAP.items():
        st.session_state[state_key] = preset[preset_key]

    st.session_state["motivational_quote"] = preset["motivational_quotes"][0]
    st.session_state["pending_exam_text"] = preset["sample_text"]


init_session_state()

# ==================== الشريط الجانبي ====================
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/f/f6/Coat_of_arms_of_Iraq.svg",
        width=65,
    )
    st.markdown("### 🇮🇶 وزارة التربية العراقية")
    st.markdown("**منصة إعداد وطباعة الأسئلة الرسمية**")
    st.divider()

    st.subheader("📚 المادة الدراسية")
    subj_options = list_available_subjects()
    subj_keys = [item["key"] for item in subj_options]
    subj_names = {item["key"]: item["name"] for item in subj_options}
    cur_idx = (
        subj_keys.index(st.session_state["current_subject"])
        if st.session_state["current_subject"] in subj_keys
        else 0
    )

    st.selectbox(
        "اختر المادة لتخصيص الهيدر والقوالب:",
        options=subj_keys,
        index=cur_idx,
        format_func=lambda k: subj_names[k],
        key="sel_subject",
        on_change=on_subject_change,
    )

    preset = get_subject_preset(st.session_state["current_subject"])
    dir_label = "RTL (من اليمين لليسار)" if preset["is_rtl"] else "LTR (English Left-to-Right)"
    st.caption(f"الاتجاه التلقائي: `{dir_label}`")
    st.divider()

    st.subheader("⚙️ خيارات التنسيق والطباعة")
    layout_choice = st.radio(
        "نمط تخطيط الورقة:",
        ["عمود واحد (النمط المدرسي التقليدي)", "عمودان (النمط الوزاري الرسمي)"],
        index=0,
    )
    layout_mode = "two_columns" if "عمودان" in layout_choice else "single"

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        page_size_choice = st.selectbox(
            "حجم الصفحة:",
            list(PAGE_SIZE_MAP.keys()),
            index=0,
        )
    with col_p2:
        target_pages_choice = st.selectbox(
            "عدد الصفحات المستهدف:",
            list(TARGET_PAGES_MAP.keys()),
            index=0,
        )

    st.divider()

    st.subheader("🔑 الذكاء الاصطناعي")
    api_key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state["gemini_api_key"],
        type="password",
        placeholder="AIzaSy...",
    )
    st.session_state["gemini_api_key"] = api_key_input.strip()

    if st.session_state["gemini_api_key"]:
        st.success(f"✅ متصل بنموذج `{GEMINI_MODEL}`")
    else:
        st.caption(f"أدخل مفتاح Gemini API لتفعيل خدمات `{GEMINI_MODEL}`.")


# ==================== الواجهة الرئيسية ====================
st.markdown(
    "<div class='main-title'>📄 صانع ومنسق الأسئلة الامتحانية العراقية</div>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<div class='sub-title'>نظام احترافي وفق الضوابط الوزارية • المادة الحالية: <b>{preset['name']}</b></div>",
    unsafe_allow_html=True,
)

tab_editor, tab_ai, tab_settings = st.tabs(
    [
        "✏️ محرر الأسئلة والمعاينة الحية",
        "🤖 المساعد الذكي وتوليد الأسئلة",
        "🏷️ بيانات الهيدر والفوتر والثوابت",
    ]
)

current_meta = {
    "subject_key": st.session_state["current_subject"],
    "subject": preset["name"] if preset["is_rtl"] else "English",
    "school_name": st.session_state["school_name"],
    "grade": st.session_state["grade"],
    "academic_year": st.session_state["academic_year"],
    "exam_type": st.session_state["exam_type"],
    "session": st.session_state["session"],
    "time_limit": st.session_state["time_limit"],
    "teacher_name": st.session_state["teacher_name"],
    "general_note": st.session_state["general_note"],
    "constants_title": preset.get("constants_title", "استفد من الثوابت:"),
    "constants_text": st.session_state["constants_text"],
    "motivational_quote": st.session_state["motivational_quote"],
}


# ==================== التبويب الأول: المحرر والمعاينة ====================
with tab_editor:
    st.markdown("##### 🛠️ أدوات الإدراج السريع:")
    quick_snippets = [
        ("➕ سؤال جديد", "س: [20 درجة]\nA. الفرع الأول... [10 درجات]\nB. الفرع الثاني... [10 درجات]"),
        ("📐 معادلة", "$$f(x) = \\int_{0}^{x} t^2 \\, dt$$"),
        ("📊 جدول مقارنة", "| وجه المقارنة | الطرف الأول | الطرف الثاني |\n|:---|:---|:---|\n| الخاصية 1 | بيان أ | بيان ب |\n| الخاصية 2 | بيان أ | بيان ب |"),
        ("📜 بيت شعري", "صدر البيت الشعري الأول ... عجز البيت الشعري المقابل"),
        ("﴿﴾ آية / حديث", "قال تعالى: ﴿إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾\nقال رسول الله ﷺ: «خَيْرُ النَّاسِ أَنْفَعُهُمْ لِلنَّاسِ»"),
        ("⚡ رسم هندسي/دائرة", "[diagram: triangle]\n[diagram: rlc_circuit]"),
    ]

    t_cols = st.columns(len(quick_snippets) + 1)
    for idx, (label, snippet) in enumerate(quick_snippets):
        with t_cols[idx]:
            if st.button(label, use_container_width=True):
                append_to_exam_text(snippet)

    with t_cols[-1]:
        if st.button("🔄 استعادة النموذج", use_container_width=True):
            set_exam_text(preset["sample_text"], toast_msg="تمت استعادة النموذج الافتراضي")

    col_edit, col_prev = st.columns([1, 1], gap="medium")

    with col_edit:
        st.markdown("##### 📝 نص الأسئلة:")
        st.text_area(
            "نص ورقة الامتحان",
            key="exam_text",
            height=580,
            label_visibility="collapsed",
        )

        c_act1, c_act2 = st.columns(2)
        with c_act1:
            if st.button("🗑️ مسح النص بالكامل"):
                set_exam_text("")
        with c_act2:
            txt = st.session_state["exam_text"]
            st.caption(f"عدد الأسطر: {len(txt.splitlines())} | عدد الأحرف: {len(txt)}")

    with col_prev:
        st.markdown("##### 👁️ المعاينة الحية للورقة:")
        try:
            live_html = build_exam_html(
                metadata=current_meta,
                text_content=st.session_state["exam_text"],
                font_scale=0.92,
                page_size_mode=PAGE_SIZE_MAP[page_size_choice],
                layout_mode=layout_mode,
                user_images=st.session_state["user_images"],
            )
            st.components.v1.html(live_html, height=580, scrolling=True)
        except Exception as exc:
            st.error(f"خطأ أثناء بناء المعاينة: {exc}")

    st.divider()
    st.subheader("🚀 إنتاج وطباعة ملف PDF النهائي")

    if st.button("🖨️ إنشاء ملف الـ PDF الآن", type="primary", use_container_width=True):
        with st.spinner("جاري معالجة وتجميع ملف الـ PDF عالي الدقة وفق المعايير الوزارية..."):
            try:
                chosen_target = TARGET_PAGES_MAP[target_pages_choice]
                pdf_bytes, final_pages, fit_ok, _ = generate_exam_pdf(
                    metadata=current_meta,
                    text_content=st.session_state["exam_text"],
                    output_pdf_path="iraqi_exam_output.pdf",
                    page_size_mode=PAGE_SIZE_MAP[page_size_choice],
                    layout_mode=layout_mode,
                    target_pages=chosen_target,
                    user_images=st.session_state["user_images"],
                )

                st.success(f"🎉 تم إنشاء ملف الـ PDF بنجاح! (عدد الصفحات: {final_pages})")

                if chosen_target and not fit_ok:
                    st.warning(
                        f"⚠️ تنبيه: تعذر ضغط الأسئلة في {chosen_target} صفحة فقط دون التأثير على وضوح الخط. عدد الصفحات الحالي: {final_pages}."
                    )

                safe_filename = f"اسئلة_{preset['name']}_{st.session_state['grade']}.pdf".replace(" ", "_")
                st.download_button(
                    label=f"📥 تحميل ملف PDF ({preset['name']} - {st.session_state['grade']}) للطباعة",
                    data=pdf_bytes,
                    file_name=safe_filename,
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as exc:
                st.error(f"حدث خطأ أثناء إنشاء ملف الـ PDF: {exc}")


# ==================== التبويب الثاني: المساعد الذكي ====================
with tab_ai:
    st.subheader("🤖 أدوات الذكاء الاصطناعي لإعداد الأسئلة")
    st.info(
        "💡 يقوم الذكاء الاصطناعي بالصياغة المباشرة وفق المعايير الوزارية العراقية ونظام الـ RTL/LTR والمعادلات الرياضية والكيميائية."
    )

    ai_key = st.session_state["gemini_api_key"]

    ai_tab1, ai_tab2, ai_tab3, ai_tab4, ai_tab5 = st.tabs(
        [
            "📷 استخراج من صور خط اليد",
            "📚 استخراج من كتاب / ملزمة",
            "🏛️ توليد نموذج وزاري متكامل",
            "✨ تدقيق وإصلاح التنسيق والمعادلات",
            "🎨 الرسومات والصور التوضيحية",
        ]
    )

    # 1. استخراج من صور خط اليد
    with ai_tab1:
        st.markdown("##### 📷 رفع صور مكتوبة بخط اليد أو ممسوحة ضوئياً")
        hand_files = st.file_uploader(
            "اختر صورة أو عدة صور لورقة الأسئلة (JPG / PNG)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="ai_handwritten_up",
        )
        if st.button("🔍 قراءة واستخراج الأسئلة من الصور", type="primary", use_container_width=True):
            if not hand_files:
                st.error("⚠️ يرجى رفع صورة واحدة على الأقل.")
            elif not ai_key:
                st.error("⚠️ يرجى إدخال مفتاح Gemini API Key في الشريط الجانبي أولاً.")
            else:
                with st.spinner("جاري قراءة خط اليد وتنسيق الأسئلة..."):
                    try:
                        images = [(f.getvalue(), f.type) for f in hand_files]
                        extracted = extract_handwritten_questions(
                            images=images,
                            api_key=ai_key,
                            subject_key=st.session_state["current_subject"],
                            model_name=GEMINI_MODEL,
                        )
                        st.session_state["last_extracted"] = extracted
                        append_to_exam_text(
                            extracted,
                            toast_msg="✅ تم استخراج الأسئلة وإضافتها إلى المحرر!",
                        )
                    except Exception as exc:
                        st.error(f"حدث خطأ أثناء الاستخراج: {exc}")

        if st.session_state.get("last_extracted"):
            with st.expander("👁️ عرض آخر نص مستخرج من الصور:", expanded=True):
                st.text_area(
                    "المحتوى المستخرج:",
                    value=st.session_state["last_extracted"],
                    height=180,
                    disabled=True,
                    key="prev_handwritten",
                )
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    if st.button("📝 استبدال المحرر بالكامل بهذا النص"):
                        set_exam_text(st.session_state["last_extracted"], toast_msg="تم استبدال محتوى المحرر")
                with c_btn2:
                    if st.button("➕ إضافة هذا النص مرة أخرى"):
                        append_to_exam_text(st.session_state["last_extracted"], toast_msg="تمت إضافة النص")

    # 2. استخراج من كتاب أو ملزمة
    with ai_tab2:
        st.markdown("##### 📚 اختيار أسئلة من كتاب مدرسي أو ملزمة (PDF / صور)")
        book_files = st.file_uploader(
            "ارفع صفحات الكتاب (PDF أو صور)",
            type=["pdf", "jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="ai_book_up",
        )
        col_b1, col_b2 = st.columns([1, 2])
        with col_b1:
            n_questions = st.number_input("عدد الأسئلة المطلوب اختيارها:", min_value=1, max_value=20, value=5)
        with col_b2:
            criteria_text = st.text_input(
                "شروط خاصة (مثال: التركيز على المسائل الحسابية، أسئلة وزارية مكررة):"
            )

        if st.button("🔍 تحليل الكتاب واختيار الأسئلة الوزارية", type="primary", use_container_width=True):
            if not book_files:
                st.error("⚠️ يرجى رفع ملفات الكتاب أولاً.")
            elif not ai_key:
                st.error("⚠️ يرجى إدخال مفتاح Gemini API Key في الشريط الجانبي أولاً.")
            else:
                with st.spinner("جاري تحليل محتوى الكتاب وانتقاء أفضل الأسئلة..."):
                    try:
                        imgs, pdf_texts = [], []
                        for f in book_files:
                            if f.type == "application/pdf" or f.name.lower().endswith(".pdf"):
                                parsed = extract_text_from_pdf_book(f.getvalue())
                                if parsed:
                                    pdf_texts.append(parsed)
                            else:
                                imgs.append((f.getvalue(), f.type))

                        extracted = select_questions_from_book(
                            images=imgs,
                            pdf_texts=pdf_texts,
                            num_questions=int(n_questions),
                            criteria=criteria_text,
                            api_key=ai_key,
                            subject_key=st.session_state["current_subject"],
                            model_name=GEMINI_MODEL,
                        )
                        st.session_state["last_book_extracted"] = extracted
                        append_to_exam_text(
                            extracted,
                            toast_msg="✅ تم اختيار الأسئلة وإضافتها إلى المحرر!",
                        )
                    except Exception as exc:
                        st.error(f"خطأ أثناء التحليل: {exc}")

        if st.session_state.get("last_book_extracted"):
            with st.expander("👁️ عرض الأسئلة المختارة من الكتاب:", expanded=True):
                st.text_area(
                    "المحتوى المختار:",
                    value=st.session_state["last_book_extracted"],
                    height=180,
                    disabled=True,
                    key="prev_book",
                )
                c_b1, c_b2 = st.columns(2)
                with c_b1:
                    if st.button("📝 استبدال المحرر بالكامل بهذه الأسئلة"):
                        set_exam_text(st.session_state["last_book_extracted"], toast_msg="تم استبدال محتوى المحرر")
                with c_b2:
                    if st.button("➕ إضافة هذه الأسئلة مرة أخرى"):
                        append_to_exam_text(st.session_state["last_book_extracted"], toast_msg="تمت إضافة الأسئلة")

    # 3. توليد نموذج وزاري متكامل
    with ai_tab3:
        st.markdown(f"##### 🏛️ توليد نموذج امتحاني وزاري كامل لمادة ({preset['name']})")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            gen_grade = st.text_input("الصف الدراسي:", value=st.session_state["grade"])
            gen_exam_type = st.selectbox(
                "نوع الامتحان:",
                ["الامتحان النهائي الوزاري", "امتحان نصف السنة", "امتحان شهري شامل"],
            )
        with col_g2:
            gen_topics = st.text_area(
                "الفصول والمواضيع المشمولة بالامتحان:",
                placeholder="مثال: الفصل الأول والثاني والثالث / قواعد الاشتقاق والأعداد المركبة",
            )
            gen_n_q = st.number_input("عدد الأسئلة:", min_value=1, max_value=10, value=6)

        if st.button("⚡ توليد نموذج الامتحان الوزاري الآن", type="primary", use_container_width=True):
            if not ai_key:
                st.error("⚠️ يرجى إدخال مفتاح Gemini API Key في الشريط الجانبي أولاً.")
            else:
                with st.spinner("جاري توليد نموذج الامتحان الوزاري المتكامل..."):
                    try:
                        generated_exam = generate_ministerial_exam_ai(
                            subject_key=st.session_state["current_subject"],
                            grade=gen_grade,
                            exam_type=gen_exam_type,
                            topics=gen_topics,
                            api_key=ai_key,
                            num_questions=int(gen_n_q),
                            model_name=GEMINI_MODEL,
                        )
                        set_exam_text(
                            generated_exam,
                            toast_msg="✅ تم توليد النموذج الوزاري ووضعه في المحرر!",
                        )
                    except Exception as exc:
                        st.error(f"حدث خطأ أثناء التوليد: {exc}")

    # 4. تدقيق وإصلاح التنسيق
    with ai_tab4:
        st.markdown("##### ✨ تدقيق وإصلاح التنسيق والمعادلات الرياضية والكيميائية")
        st.caption(
            "يفحص هذا الخيار المسودة الحالية ويصحح أخطاء LaTeX والأقواس وتنسيق الفروع والدرجات تلقائياً."
        )
        if st.button("🔧 تدقيق وإصلاح نص الأسئلة الحالي", type="primary", use_container_width=True):
            if not st.session_state["exam_text"].strip():
                st.error("⚠️ لا يوجد نص في المحرر للتدقيق!")
            elif not ai_key:
                st.error("⚠️ يرجى إدخال مفتاح Gemini API Key في الشريط الجانبي أولاً.")
            else:
                with st.spinner("جاري تدقيق النصوص وصيغ LaTeX وترتيب الفروع..."):
                    try:
                        polished = fix_and_polish_exam_text(
                            raw_text=st.session_state["exam_text"],
                            api_key=ai_key,
                            subject_key=st.session_state["current_subject"],
                            model_name=GEMINI_MODEL,
                        )
                        set_exam_text(polished, toast_msg="✅ تم تدقيق وتنسيق النص بنجاح!")
                    except Exception as exc:
                        st.error(f"حدث خطأ: {exc}")

    # 5. الرسومات والصور المخصصة
    with ai_tab5:
        st.markdown("##### 🎨 إدراج الرسومات الهندسية والعلمية الجاهزة")
        st.markdown(
            """
            يمكنك استخدام الأوسمة التالية مباشرة في نص السؤال:
            - `[diagram: triangle]` : رسم مثلث قائم الزاوية مع الزوايا والأبعاد
            - `[diagram: circle]` : رسم دائرة هندسية مع نصف القطر والمركز
            - `[diagram: parabola]` أو `[diagram: sine]` : رسم دالة رياضية على المستوي الإحداثي
            - `[diagram: rlc_circuit]` : رسم دائرة تيار متناوب متوالية الربط (R-L-C)
            - `[diagram: optics_lens]` : رسم مسار الأشعة والعدسة المحدبة
            """
        )

        st.divider()
        st.markdown("##### 🖼️ رفع صور مخصصة لإدراجها في الأسئلة:")
        uploaded_imgs = st.file_uploader(
            "ارفع صورة أو أكثر كرسم توضيحي",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="custom_user_imgs",
        )
        if uploaded_imgs:
            st.session_state["user_images"] = {}
            img_cols = st.columns(min(len(uploaded_imgs), 4))
            for idx, img_file in enumerate(uploaded_imgs, start=1):
                img_b64 = base64.b64encode(img_file.getvalue()).decode("utf-8")
                st.session_state["user_images"][str(idx)] = f"data:{img_file.type};base64,{img_b64}"
                with img_cols[(idx - 1) % 4]:
                    st.image(img_file, width=160, caption=f"صورة #{idx}")
                    st.code(f"[صورة: {idx}]", language="markdown")
            st.success("✅ انسخ وسم الصورة أعلاه وضعه في المكان المطلوب داخل نص السؤال.")


# ==================== التبويب الثالث: الترويسة والثوابت ====================
with tab_settings:
    st.subheader("🏷️ إعدادات الترويسة والفوتر المخصص للمادة")

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.text_input("اسم المدرسة / المؤسسة التعليمية:", key="school_name")
        st.text_input("الصف الدراسي والفرع:", key="grade")
        st.text_input("الوقت المحدد للامتحان:", key="time_limit")
        st.text_input("العام الدراسي:", key="academic_year")

    with col_h2:
        st.text_input("نوع الامتحان:", key="exam_type")
        st.text_input("الدور الامتحاني:", key="session")
        st.text_input("اسم مدرس / مدرسة المادة:", key="teacher_name")
        st.text_area("الملاحظة العامة في رأس الصفحة:", key="general_note")

    st.divider()
    st.subheader("🧪 مربع الثوابت العلمية والكتل الذرية (اختياري)")
    st.text_area(
        "نص الثوابت (يقبل صيغ LaTeX محصورة بـ $...$):",
        key="constants_text",
        height=80,
    )

    st.divider()
    st.subheader("💬 العبارة التحفيزية في التذييل (الفوتر)")
    st.text_input("العبارة التشجيعية للطلبة:", key="motivational_quote")