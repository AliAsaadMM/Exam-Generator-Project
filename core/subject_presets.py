# -*- coding: utf-8 -*-
"""
القوالب الافتراضية والثوابت الوزارية للمواد الدراسية العراقية
"""

SUBJECT_PRESETS = {
    "math": {
        "name": "الرياضيات",
        "is_rtl": True,
        "default_school": "إعدادية بغداد المركزية للبنين",
        "default_grade": "السادس العلمي",
        "default_time": "ثلاث ساعات",
        "default_academic_year": "2026 - 2027",
        "default_exam_type": "الامتحان النهائي الوزاري",
        "default_session": "الدور الأول",
        "default_teacher": "أ. علي أسعد",
        "default_general_note": "ملاحظة: الإجابة عن خمسة أسئلة فقط، ولكل سؤال (20 درجة).",
        "constants_title": "ملاحظات رياضية:",
        "default_constants": "",
        "motivational_quotes": [
            "مع تمنياتنا لجميع طلبتنا الأعزاء بالنجاح والتفوق الدائم",
            "بالجد والاجتهاد تُبنى الأوطان وتُحقق الطموحات",
        ],
        "sample_text": """س1: [20 درجة]
A. جد قيمة $x, y \\in \\mathbb{R}$ التي تحقق المعادلة الآتية: [10 درجات]
$$\\frac{3 + i}{1 - i} x + \\frac{2 - i}{1 + i} y = 4 + 3i$$

B. جد معادلة القطع الناقص الذي مركزه نقطة الأصل وبؤرتاه على محور السينات ويمر بالنقطتين $(6, 2)$ و $(3, 4)$. [10 درجات]

س2: [20 درجة]
A. احسب التكامل الآتي: [10 درجات]
$$\\int_{0}^{\\frac{\\pi}{4}} \\sec^2(x) \\cdot e^{\\tan(x)} \\, dx$$

B. في المثلث القائم المجاور، إذا كان طول الوتر $10\\text{ cm}$، جد المساحة القصوى للمثلث. [10 درجات]
[diagram: triangle]""",
    },
    "physics": {
        "name": "الفيزياء",
        "is_rtl": True,
        "default_school": "ثانوية المتميزين",
        "default_grade": "السادس العلمي",
        "default_time": "ثلاث ساعات",
        "default_academic_year": "2026 - 2027",
        "default_exam_type": "الامتحان النهائي الوزاري",
        "default_session": "الدور الأول",
        "default_teacher": "قسم الفيزياء",
        "default_general_note": "ملاحظة: أجب عن خمسة أسئلة فقط، ولكل سؤال (20 درجة).",
        "constants_title": "استفد من الثوابت الفيزيائية الآتية:",
        "default_constants": "$c = 3 \\times 10^8\\text{ m/s}$  |  $h = 6.63 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$  |  $e = 1.6 \\times 10^{-19}\\text{ C}$  |  $\\pi = 3.14$",
        "motivational_quotes": [
            "تمنياتنا لكم بالموفقية والنجاح الباهر",
        ],
        "sample_text": """س1: [20 درجة]
A. دائرة تيار متناوب متوالية الربط تحتوي مقاومة صرف $R = 30\\,\\Omega$ ومحث صرف معامل حثه الذاتي $L = \\frac{0.4}{\\pi}\\text{ H}$ ومتسعة ذات سعة صرف، ربطت المجموعة بين قطبي مصدر للفولطية المتناوبة تردده $50\\text{ Hz}$ وفرق الجهد بين طرفيه $200\\text{ V}$، احسب الممانعة الكلية وتيار الدائرة. [12 درجة]
[diagram: rlc_circuit]

B. ما المقصود بـ (قوة لورنتز)؟ وأين تستثمر؟ [8 درجات]

س2: [20 درجة]
قارن بين المتسعة ذات الورق المشمع والمتسعة الإلكتروليتية من حيث التركيب والاستعمال:
| وجه المقارنة | المتسعة ذات الورق المشمع | المتسعة الإلكتروليتية |
|:---|:---|:---|
| المادة العازلة | الورق المشمع | أكسيد الألمنيوم أو التنتالوم |
| الحجم والسعة | صغيرة الحجم نسبياً | تتحمل فرق جهد عالٍ وتُعلم بقطبين |""",
    },
    "chemistry": {
        "name": "الكيمياء",
        "is_rtl": True,
        "default_school": "ثانوية المتفوقين",
        "default_grade": "السادس العلمي",
        "default_time": "ثلاث ساعات",
        "default_academic_year": "2026 - 2027",
        "default_exam_type": "الامتحان النهائي الوزاري",
        "default_session": "الدور الأول",
        "default_teacher": "قسم الكيمياء",
        "default_general_note": "ملاحظة: أجب عن خمسة أسئلة فقط، ولكل سؤال (20 درجة).",
        "constants_title": "الكتل الذرية والثوابت:",
        "default_constants": "$\\text{H}=1,\\; \\text{C}=12,\\; \\text{N}=14,\\; \\text{O}=16,\\; \\text{Na}=23,\\; \\text{Cl}=35.5$  |  $R = 0.082\\text{ L}\\cdot\\text{atm/mol}\\cdot\\text{K}$",
        "motivational_quotes": [
            "مع أطيب الأمنيات بالنجاح والتفوق",
        ],
        "sample_text": """س1: [20 درجة]
A. للتفاعل الغازي المتزن الآتي:
$$2\\text{SO}_2(g) + \\text{O}_2(g) \\rightleftharpoons 2\\text{SO}_3(g) \\quad \\Delta H = -198\\text{ kJ}$$
وضح تأثير كل من العوامل الآتية على حالة الاتزان وقيمة ثابت الاتزان $K_{eq}$: [10 درجات]
1. خفض درجة حرارة التفاعل.
2. زيادة الضغط المسلط على النظام.

B. احسب $\\text{pH}$ لمحلول بفر مكون من حامض الخليك بتركيز $0.1\\text{ M}$ وخلات الصوديوم بتركيز $0.2\\text{ M}$ علماً أن $pK_a = 4.74$ و $\\log 2 = 0.3$. [10 درجات]""",
    },
    "arabic": {
        "name": "اللغة العربية",
        "is_rtl": True,
        "default_school": "إعدادية الرصافة النموذجية",
        "default_grade": "السادس الإعدادي",
        "default_time": "ثلاث ساعات",
        "default_academic_year": "2026 - 2027",
        "default_exam_type": "الامتحان النهائي الوزاري",
        "default_session": "الدور الأول",
        "default_teacher": "قسم اللغة العربية",
        "default_general_note": "ملاحظة: الإجابة عن جميع الأسئلة وضمن التفرعات المحددة.",
        "constants_title": "",
        "default_constants": "",
        "motivational_quotes": [
            "أمنياتنا لكم بالتوفيق والسداد",
        ],
        "sample_text": """قواعد اللغة العربية: [40 درجة]
س1: قال تعالى: ﴿وَمَا تُقَدِّمُوا لِأَنْفُسِكُمْ مِنْ خَيْرٍ تَجِدُوهُ عِنْدَ اللَّهِ﴾
1. استخرج أداة الشرط وبين معناها وإعرابها معللاً. [6 درجات]
2. ما نوع (ما) الواردة في النص الكريم؟ [4 درجات]

الأدب والنصوص: [40 درجة]
س2: قال الشاعر:
أَنا في أُمَّةٍ تَدارَكَها اللَـهُ ... غَريبٌ كَصالِحٍ في ثَمودِ
1. من قائل البيت؟ وما عنوان قصيدته؟ [4 درجات]
2. اكتب ثلاثة أبيات تلي هذا البيت مضبوطة بالشكل. [6 درجات]""",
    },
    "islamic": {
        "name": "التربية الإسلامية",
        "is_rtl": True,
        "default_school": "ثانوية النور للبنين",
        "default_grade": "السادس الإعدادي",
        "default_time": "ساعتان",
        "default_academic_year": "2026 - 2027",
        "default_exam_type": "الامتحان النهائي الوزاري",
        "default_session": "الدور الأول",
        "default_teacher": "قسم التربية الإسلامية",
        "default_general_note": "ملاحظة: أجب عن خمسة أسئلة فقط، ولكل سؤال (20 درجة).",
        "constants_title": "",
        "default_constants": "",
        "motivational_quotes": [
            "وفقكم الله لما يحب ويرضى",
        ],
        "sample_text": """أحكام التلاوة: [10 درجات]
س1: عيّن المد المتصل والمد المنفصل في قوله تعالى:
﴿يَا أَيُّهَا الَّذِينَ آمَنُوا إِذَا قُمْتُمْ إِلَى الصَّلَاةِ فَاغْسِلُوا وُجُوهَكُمْ﴾ واذكر السبب.

الحفظ: [20 درجة]
س2: اكتب من قوله تعالى: ﴿لَقَدْ كَانَ لَكُمْ فِي رَسُولِ اللَّهِ أُسْوَةٌ حَسَنَةٌ...﴾ إلى قوله تعالى: ﴿...وَكَانَ اللَّهُ غَفُورًا رَحِيمًا﴾.""",
    },
    "english": {
        "name": "اللغة الإنجليزية (English)",
        "is_rtl": False,
        "default_school": "Al-Mustansiriya Distinguished Secondary School",
        "default_grade": "6th Preparatory",
        "default_time": "3 Hours",
        "default_academic_year": "2026 - 2027",
        "default_exam_type": "Ministerial Final Exam",
        "default_session": "First Attempt",
        "default_teacher": "English Department",
        "default_general_note": "Note: Answer all the questions.",
        "constants_title": "",
        "default_constants": "",
        "motivational_quotes": [
            "Best of luck to all our dear students!",
        ],
        "sample_text": """Q1: Reading Comprehension (25 Marks)
Read the following passage carefully and answer the questions below:
Tariq was floating peacefully on his airbed in Sharm El Sheikh when he felt something push him up...

Q2: Grammar and Functions (30 Marks)
A. Re-write the following sentences, follow the instructions between brackets: (20 Marks)
1. My brother (be) in Egypt for two years. (Correct the form of the verb)
2. Define a cameraman. (Use: operates the camera for films or TV programmes)""",
    },
    "biology": {
        "name": "الأحياء",
        "is_rtl": True,
        "default_school": "ثانوية الخوارزمي",
        "default_grade": "السادس العلمي",
        "default_time": "ثلاث ساعات",
        "default_academic_year": "2026 - 2027",
        "default_exam_type": "الامتحان النهائي الوزاري",
        "default_session": "الدور الأول",
        "default_teacher": "قسم علوم الحياة",
        "default_general_note": "ملاحظة: أجب عن خمسة أسئلة فقط، ولكل سؤال (20 درجة).",
        "constants_title": "",
        "default_constants": "",
        "motivational_quotes": [
            "مع تمنياتنا لكم بالنجاح الباهر",
        ],
        "sample_text": """س1: [20 درجة]
A. عرّف أربعة مما يأتي: [12 درجة]
(البلعمة، التناضح، النسيج المرستيمي، الإخصاب المزدوج، البلازميد).

B. ما موقع ووظيفة كل من: [8 درجات]
1. الجسيم المركزي.
2. الخلايا المرافقة.""",
    },
}


def get_subject_preset(subject_key: str) -> dict:
    """إرجاع قالب المادة المطلوبة مع الرجوع للرياضيات كخيار افتراضي."""
    return SUBJECT_PRESETS.get(subject_key, SUBJECT_PRESETS["math"])


def list_available_subjects() -> list[dict]:
    """إرجاع قائمة بجميع المواد المتوفرة لملء القائمة المنسدلة."""
    return [{"key": k, "name": v["name"]} for k, v in SUBJECT_PRESETS.items()]