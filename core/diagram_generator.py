# -*- coding: utf-8 -*-
"""
مولد الرسومات الهندسية والفيزيائية المدمجة بصيغة SVG عالية الدقة
"""

import base64

DIAGRAM_TEMPLATES = {
    "triangle": """
    <svg xmlns="http://www.w3.org/2000/svg" width="240" height="170" viewBox="0 0 240 170">
      <polygon points="40,140 200,140 40,30" fill="#eff6ff" stroke="#1e3a8a" stroke-width="2.5"/>
      <polyline points="40,124 56,124 56,140" fill="none" stroke="#1e3a8a" stroke-width="1.8"/>
      <text x="26" y="26" font-family="Cairo, sans-serif" font-size="14" font-weight="bold" fill="#0f172a">A</text>
      <text x="24" y="152" font-family="Cairo, sans-serif" font-size="14" font-weight="bold" fill="#0f172a">B</text>
      <text x="206" y="152" font-family="Cairo, sans-serif" font-size="14" font-weight="bold" fill="#0f172a">C</text>
      <text x="128" y="75" font-family="Cairo, sans-serif" font-size="13" fill="#dc2626">الوتر</text>
      <text x="115" y="158" font-family="Cairo, sans-serif" font-size="13" fill="#334155">x</text>
      <text x="18" y="90" font-family="Cairo, sans-serif" font-size="13" fill="#334155">y</text>
    </svg>
    """,
    "circle": """
    <svg xmlns="http://www.w3.org/2000/svg" width="210" height="180" viewBox="0 0 210 180">
      <circle cx="105" cy="90" r="68" fill="#f8fafc" stroke="#1e3a8a" stroke-width="2.5"/>
      <circle cx="105" cy="90" r="3.5" fill="#dc2626"/>
      <line x1="105" y1="90" x2="173" y2="90" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,3"/>
      <text x="95" y="82" font-family="Cairo, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">O</text>
      <text x="135" y="83" font-family="Cairo, sans-serif" font-size="13" font-weight="bold" fill="#dc2626">r</text>
    </svg>
    """,
    "parabola": """
    <svg xmlns="http://www.w3.org/2000/svg" width="230" height="180" viewBox="0 0 230 180">
      <line x1="20" y1="145" x2="210" y2="145" stroke="#475569" stroke-width="1.8"/>
      <line x1="115" y1="15" x2="115" y2="165" stroke="#475569" stroke-width="1.8"/>
      <path d="M 55,25 Q 115,265 175,25" fill="none" stroke="#1e3a8a" stroke-width="2.5"/>
      <text x="200" y="138" font-family="sans-serif" font-size="12" fill="#0f172a">X</text>
      <text x="122" y="25" font-family="sans-serif" font-size="12" fill="#0f172a">Y</text>
    </svg>
    """,
    "sine": """
    <svg xmlns="http://www.w3.org/2000/svg" width="250" height="160" viewBox="0 0 250 160">
      <line x1="15" y1="80" x2="235" y2="80" stroke="#475569" stroke-width="1.5"/>
      <line x1="35" y1="15" x2="35" y2="145" stroke="#475569" stroke-width="1.5"/>
      <path d="M 35,80 Q 80,5 125,80 T 215,80" fill="none" stroke="#1e3a8a" stroke-width="2.5"/>
      <text x="225" y="73" font-family="sans-serif" font-size="12" fill="#0f172a">x</text>
      <text x="42" y="24" font-family="sans-serif" font-size="12" fill="#0f172a">y</text>
    </svg>
    """,
    "rlc_circuit": """
    <svg xmlns="http://www.w3.org/2000/svg" width="320" height="150" viewBox="0 0 320 150">
      <rect x="30" y="30" width="260" height="90" fill="none" stroke="#1e3a8a" stroke-width="2"/>
      <!-- Resistor -->
      <rect x="70" y="20" width="44" height="20" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
      <text x="87" y="14" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0f172a">R</text>
      <!-- Inductor -->
      <rect x="140" y="20" width="46" height="20" fill="#ffffff" stroke="#ffffff"/>
      <path d="M 140,30 Q 147,12 155,30 Q 163,12 171,30 Q 179,12 186,30" fill="none" stroke="#0f172a" stroke-width="2"/>
      <text x="159" y="14" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0f172a">L</text>
      <!-- Capacitor -->
      <rect x="215" y="18" width="16" height="24" fill="#ffffff"/>
      <line x1="216" y1="18" x2="216" y2="42" stroke="#0f172a" stroke-width="2.5"/>
      <line x1="228" y1="18" x2="228" y2="42" stroke="#0f172a" stroke-width="2.5"/>
      <text x="218" y="13" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0f172a">C</text>
      <!-- AC Source -->
      <circle cx="160" cy="120" r="16" fill="#ffffff" stroke="#dc2626" stroke-width="2"/>
      <path d="M 151,120 Q 155,112 160,120 T 169,120" fill="none" stroke="#dc2626" stroke-width="1.8"/>
      <text x="182" y="138" font-family="sans-serif" font-size="11" font-weight="bold" fill="#dc2626">AC Source</text>
    </svg>
    """,
    "optics_lens": """
    <svg xmlns="http://www.w3.org/2000/svg" width="300" height="160" viewBox="0 0 300 160">
      <line x1="15" y1="80" x2="285" y2="80" stroke="#64748b" stroke-width="1.5" stroke-dasharray="5,4"/>
      <path d="M 150,20 Q 170,80 150,140 Q 130,80 150,20 Z" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>
      <line x1="40" y1="45" x2="150" y2="45" stroke="#dc2626" stroke-width="1.8"/>
      <line x1="150" y1="45" x2="255" y2="112" stroke="#dc2626" stroke-width="1.8"/>
      <circle cx="205" cy="80" r="3" fill="#0f172a"/>
      <text x="201" y="72" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0f172a">F</text>
    </svg>
    """,
}


def execute_custom_python_diagram(diagram_key: str) -> str:
    """إرجاع وسم صورة HTML يحتوي على الرسم الهندسي بصيغة Base64 SVG."""
    clean_key = diagram_key.strip().lower()
    svg_code = DIAGRAM_TEMPLATES.get(clean_key)
    if not svg_code:
        return f"<div style='color:#b91c1c;font-size:12px;'>[رسم غير معروف: {diagram_key}]</div>"

    b64 = base64.b64encode(svg_code.strip().encode("utf-8")).decode("utf-8")
    return (
        f"<div style='text-align:center; margin:8px 0;'>"
        f"<img src='data:image/svg+xml;base64,{b64}' style='max-width:100%; height:auto;'/>"
        f"</div>"
    )