"""
character_rig_generator.py
Generates broadcast-grade OverSimplified / History Matters vector SVG character rigs.
Supports directional environmental rim lighting, expressive facial micro-features,
modular hats/headdresses, anti-clone asymmetric gesture presets, props, and weighted contact shadows
on a strict 320x440 monolithic canvas conforming to SKILL.md Section 3.B.
"""

import os
import argparse


def generate_chibi_character(
    name="resistance_fighter",
    skin_tone="#ffffff",
    coat_color="#2b303c",
    vest_color="#cbd5e1",
    hair_color="#1f2937",
    hat_type=None,
    expression="panicked",
    pose="standing",
    rim_color="#fbbf24",
    rim_side="right",
    handheld_prop=None,
    show_nameplate=False,
    output_path="character.svg"
):
    """
    Renders a monolithic OverSimplified 320x440 character rig with asymmetric arms and physical rim lighting.
    """
    # 1. Expressions & Eyes (Strict FACE_CONFIG: Eyebrows Y in [124, 128], Eyes center (160, 144), Mouth Y=186)
    eyes_svg = ""
    eyebrows_svg = ""
    mouth_svg = ""
    sweat_svg = ""

    if expression in ["shocked", "panicked"]:
        eyes_svg = """
            <ellipse cx="138" cy="144" rx="13" ry="16" fill="#ffffff" stroke="#050608" stroke-width="5"/>
            <circle cx="138" cy="144" r="5" fill="#050608"/>
            <ellipse cx="182" cy="144" rx="13" ry="16" fill="#ffffff" stroke="#050608" stroke-width="5"/>
            <circle cx="182" cy="144" r="5" fill="#050608"/>
        """
        eyebrows_svg = """
            <path d="M 124 122 Q 138 112 152 126" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
            <path d="M 168 126 Q 182 112 196 122" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
        """
        mouth_svg = """
            <ellipse cx="160" cy="190" rx="14" ry="19" fill="#1e1b18" stroke="#050608" stroke-width="4.5"/>
            <path d="M 152 198 Q 160 193 168 198" fill="#e11d48"/>
        """
        sweat_svg = """
            <path d="M 198 120 C 196 114 204 114 202 120 C 202 124 198 124 198 120 Z" fill="#38bdf8"/>
        """
    elif expression == "intense_dread":
        eyes_svg = """
            <ellipse cx="138" cy="144" rx="15" ry="18" fill="#ffffff" stroke="#050608" stroke-width="5"/>
            <circle cx="138" cy="144" r="3.5" fill="#050608"/>
            <ellipse cx="182" cy="144" rx="15" ry="18" fill="#ffffff" stroke="#050608" stroke-width="5"/>
            <circle cx="182" cy="144" r="3.5" fill="#050608"/>
        """
        eyebrows_svg = """
            <path d="M 124 122 Q 138 110 152 124" stroke="#050608" stroke-width="5.5" stroke-linecap="round" fill="none"/>
            <path d="M 168 124 Q 182 110 196 122" stroke="#050608" stroke-width="5.5" stroke-linecap="round" fill="none"/>
            <line x1="156" y1="126" x2="156" y2="136" stroke="#050608" stroke-width="3"/>
            <line x1="164" y1="126" x2="164" y2="136" stroke="#050608" stroke-width="3"/>
        """
        mouth_svg = """
            <path d="M 144 190 Q 152 184 160 190 T 176 186" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
        """
        sweat_svg = """
            <path d="M 198 122 C 195 116 205 116 202 122 C 202 126 198 126 198 122 Z" fill="#38bdf8"/>
            <path d="M 122 124 C 119 118 129 118 126 124 C 126 128 122 128 122 124 Z" fill="#38bdf8"/>
        """
    elif expression == "thinking":
        eyes_svg = """
            <circle cx="138" cy="142" r="6" fill="#050608"/>
            <circle cx="182" cy="142" r="6" fill="#050608"/>
        """
        eyebrows_svg = """
            <path d="M 124 122 L 152 128" stroke="#050608" stroke-width="5" stroke-linecap="round"/>
            <path d="M 168 120 Q 182 112 196 122" stroke="#050608" stroke-width="5.5" stroke-linecap="round" fill="none"/>
        """
        mouth_svg = """
            <path d="M 152 186 Q 164 184 172 188" stroke="#050608" stroke-width="4.5" stroke-linecap="round" fill="none"/>
        """
    elif expression == "smug":
        eyes_svg = """
            <path d="M 126 142 Q 138 132 150 142" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
            <circle cx="138" cy="145" r="4" fill="#050608"/>
            <path d="M 170 142 Q 182 132 194 142" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
            <circle cx="182" cy="145" r="4" fill="#050608"/>
        """
        eyebrows_svg = """
            <path d="M 124 124 Q 138 118 152 124" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
            <path d="M 168 116 Q 182 108 196 118" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
        """
        mouth_svg = """
            <path d="M 148 184 Q 168 184 176 176" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
        """
    elif expression == "happy":
        eyes_svg = """
            <path d="M 126 146 Q 138 134 150 146" stroke="#050608" stroke-width="5.5" stroke-linecap="round" fill="none"/>
            <path d="M 170 146 Q 182 134 194 146" stroke="#050608" stroke-width="5.5" stroke-linecap="round" fill="none"/>
        """
        eyebrows_svg = """
            <path d="M 124 120 Q 138 112 152 120" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
            <path d="M 168 120 Q 182 112 196 120" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
        """
        mouth_svg = """
            <path d="M 144 180 Q 160 200 176 180 Z" fill="#e11d48" stroke="#050608" stroke-width="4.5"/>
        """
    elif expression == "angry":
        eyes_svg = """
            <ellipse cx="138" cy="146" rx="10" ry="12" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <circle cx="140" cy="146" r="4.5" fill="#050608"/>
            <ellipse cx="182" cy="146" rx="10" ry="12" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <circle cx="180" cy="146" r="4.5" fill="#050608"/>
        """
        eyebrows_svg = """
            <path d="M 124 120 L 154 134" stroke="#050608" stroke-width="6" stroke-linecap="round"/>
            <path d="M 196 120 L 166 134" stroke="#050608" stroke-width="6" stroke-linecap="round"/>
        """
        mouth_svg = """
            <path d="M 146 190 Q 160 178 174 190" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
        """
    elif expression == "crying":
        eyes_svg = """
            <path d="M 128 142 Q 138 136 148 142" stroke="#050608" stroke-width="5" fill="none"/>
            <path d="M 172 142 Q 182 136 192 142" stroke="#050608" stroke-width="5" fill="none"/>
            <path d="M 132 146 Q 130 170 128 190" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" fill="none"/>
            <path d="M 188 146 Q 190 170 192 190" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" fill="none"/>
        """
        eyebrows_svg = """
            <path d="M 124 124 Q 138 114 152 126" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
            <path d="M 168 126 Q 182 114 196 124" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
        """
        mouth_svg = """
            <ellipse cx="160" cy="192" rx="12" ry="16" fill="#1e1b18" stroke="#050608" stroke-width="4.5"/>
        """
    elif expression == "dollar_eyes":
        eyes_svg = """
            <ellipse cx="138" cy="144" rx="14" ry="16" fill="#22c55e" stroke="#050608" stroke-width="4"/>
            <text x="131" y="152" font-family="Arial, sans-serif" font-weight="900" font-size="22" fill="#ffffff">$</text>
            <ellipse cx="182" cy="144" rx="14" ry="16" fill="#22c55e" stroke="#050608" stroke-width="4"/>
            <text x="175" y="152" font-family="Arial, sans-serif" font-weight="900" font-size="22" fill="#ffffff">$</text>
        """
        eyebrows_svg = """
            <path d="M 124 116 Q 138 108 152 116" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
            <path d="M 168 116 Q 182 108 196 116" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
        """
        mouth_svg = """
            <path d="M 144 182 Q 160 206 176 182 Z" fill="#e11d48" stroke="#050608" stroke-width="4.5"/>
            <path d="M 152 188 L 152 208 Q 160 216 168 208 L 168 188 Z" fill="#fb7185"/>
        """
    elif expression == "knockout":
        eyes_svg = """
            <path d="M 130 136 L 146 152 M 146 136 L 130 152" stroke="#050608" stroke-width="5.5" stroke-linecap="round"/>
            <path d="M 174 136 L 190 152 M 190 136 L 174 152" stroke="#050608" stroke-width="5.5" stroke-linecap="round"/>
        """
        eyebrows_svg = """
            <path d="M 124 126 L 152 122" stroke="#050608" stroke-width="5" stroke-linecap="round"/>
            <path d="M 168 122 L 196 126" stroke="#050608" stroke-width="5" stroke-linecap="round"/>
        """
        mouth_svg = """
            <path d="M 146 188 Q 156 196 166 188 T 176 188" stroke="#050608" stroke-width="4.5" stroke-linecap="round" fill="none"/>
        """
    else:  # neutral
        eyes_svg = """
            <ellipse cx="138" cy="144" rx="10" ry="14" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <circle cx="138" cy="144" r="4.5" fill="#050608"/>
            <ellipse cx="182" cy="144" rx="10" ry="14" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <circle cx="182" cy="144" r="4.5" fill="#050608"/>
        """
        eyebrows_svg = """
            <path d="M 126 124 Q 138 120 150 124" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
            <path d="M 170 124 Q 182 120 194 124" stroke="#050608" stroke-width="5" stroke-linecap="round" fill="none"/>
        """
        mouth_svg = """
            <line x1="150" y1="186" x2="170" y2="186" stroke="#050608" stroke-width="4.5" stroke-linecap="round"/>
        """

    # 2. Hats & Headgear
    hat_svg = ""
    if hat_type == "keffiyeh":
        hat_svg = f"""
            <!-- Keffiyeh / Ghutra headdress -->
            <path d="M 88 140 C 85 80 120 60 160 60 C 200 60 235 80 232 140 C 230 180 238 230 242 260 L 210 260 C 210 210 215 160 210 130 C 200 80 120 80 110 130 C 105 160 110 210 110 260 L 78 260 C 82 230 90 180 88 140 Z" fill="#ffffff" stroke="#050608" stroke-width="5"/>
            <!-- Agal black cord band -->
            <ellipse cx="160" cy="85" rx="55" ry="12" fill="none" stroke="#050608" stroke-width="12"/>
            <ellipse cx="160" cy="94" rx="52" ry="10" fill="none" stroke="#050608" stroke-width="8"/>
        """
    elif hat_type == "powdered_wig":
        hat_svg = """
            <!-- 18th Century British Colonial Powdered Wig -->
            <ellipse cx="110" cy="120" rx="26" ry="32" fill="#f1f5f9" stroke="#050608" stroke-width="4.5"/>
            <ellipse cx="210" cy="120" rx="26" ry="32" fill="#f1f5f9" stroke="#050608" stroke-width="4.5"/>
            <path d="M 100 115 C 100 60 140 50 160 50 C 180 50 220 60 220 115 Z" fill="#f8fafc" stroke="#050608" stroke-width="5"/>
            <circle cx="160" cy="50" r="14" fill="#f8fafc" stroke="#050608" stroke-width="4"/>
        """
    elif hat_type == "bicorne":
        hat_svg = """
            <!-- Napoleonic Bicorne Hat -->
            <path d="M 70 100 C 110 40 160 45 160 50 C 160 45 210 40 250 100 C 210 95 160 92 70 100 Z" fill="#0f172a" stroke="#050608" stroke-width="5"/>
            <circle cx="160" cy="82" r="10" fill="#e11d48" stroke="#facc15" stroke-width="3"/>
        """
    elif hat_type in ["ashoka_crown", "royal_mukut"]:
        hat_svg = """
            <!-- Imperial Indian Gold Mukut / Crown -->
            <polygon points="110,95 125,50 145,80 160,35 175,80 195,50 210,95" fill="#facc15" stroke="#050608" stroke-width="5"/>
            <circle cx="160" cy="65" r="7" fill="#dc2626" stroke="#050608" stroke-width="2.5"/>
            <ellipse cx="160" cy="96" rx="52" ry="8" fill="#ca8a04" stroke="#050608" stroke-width="4"/>
        """
    elif hat_type in ["turban", "pagri"]:
        hat_svg = """
            <!-- Royal Rajput / Sikh Turban -->
            <ellipse cx="160" cy="80" rx="64" ry="36" fill="#ea580c" stroke="#050608" stroke-width="5"/>
            <path d="M 100 80 Q 160 50 220 80 Q 160 100 100 80 Z" fill="#f97316" stroke="#050608" stroke-width="4"/>
            <circle cx="160" cy="62" r="9" fill="#facc15" stroke="#050608" stroke-width="3"/>
        """
    elif hat_type == "gandhi_topi":
        hat_svg = """
            <!-- Khadi Gandhi Topi -->
            <path d="M 112 95 Q 160 70 208 95 L 202 105 Q 160 88 118 105 Z" fill="#f8fafc" stroke="#050608" stroke-width="4.5"/>
        """
    elif hat_type == "military_cap":
        hat_svg = """
            <!-- WW2 Military Peaked Cap -->
            <ellipse cx="160" cy="80" rx="58" ry="16" fill="#334155" stroke="#050608" stroke-width="5"/>
            <path d="M 118 80 C 120 55 160 50 160 50 C 160 50 200 55 202 80 Z" fill="#1e293b" stroke="#050608" stroke-width="4.5"/>
            <path d="M 115 88 Q 160 102 205 88" stroke="#0f172a" stroke-width="8" stroke-linecap="round" fill="none"/>
        """
    elif hat_type == "top_hat":
        hat_svg = """
            <!-- Victorian Gentleman Top Hat -->
            <ellipse cx="160" cy="95" rx="62" ry="12" fill="#0f172a" stroke="#050608" stroke-width="5"/>
            <rect x="120" y="25" width="80" height="70" rx="4" fill="#0f172a" stroke="#050608" stroke-width="5"/>
            <rect x="120" y="80" width="80" height="12" fill="#dc2626"/>
        """

    # 3. Handheld Props
    prop_svg = ""
    if handheld_prop == "test_tube":
        prop_svg = """
            <g id="prop-test-tube" transform="translate(230, 240) rotate(15)">
                <rect x="0" y="0" width="16" height="52" rx="8" fill="#38bdf8" opacity="0.85" stroke="#050608" stroke-width="4"/>
                <rect x="2" y="20" width="12" height="30" rx="6" fill="#22c55e"/>
                <line x1="-3" y1="2" x2="19" y2="2" stroke="#050608" stroke-width="5" stroke-linecap="round"/>
            </g>
        """
    elif handheld_prop == "clipboard":
        prop_svg = """
            <g id="prop-clipboard" transform="translate(195, 230) rotate(-10)">
                <rect x="0" y="0" width="46" height="62" rx="4" fill="#92400e" stroke="#050608" stroke-width="4.5"/>
                <rect x="4" y="6" width="38" height="50" rx="2" fill="#f8fafc"/>
                <line x1="8" y1="16" x2="36" y2="16" stroke="#050608" stroke-width="3"/>
                <line x1="8" y1="26" x2="36" y2="26" stroke="#050608" stroke-width="3"/>
                <line x1="8" y1="36" x2="26" y2="36" stroke="#050608" stroke-width="3"/>
                <rect x="14" y="-3" width="18" height="8" rx="2" fill="#64748b" stroke="#050608" stroke-width="3"/>
            </g>
        """
    elif handheld_prop == "karak_chai":
        prop_svg = """
            <g id="prop-karak-chai" transform="translate(225, 245)">
                <polygon points="0,0 24,0 20,40 4,40" fill="#d97706" stroke="#050608" stroke-width="4"/>
                <ellipse cx="12" cy="0" rx="12" ry="4" fill="#fbbf24" stroke="#050608" stroke-width="3"/>
            </g>
        """
    elif handheld_prop == "oil_barrel":
        prop_svg = """
            <g id="prop-oil-barrel" transform="translate(200, 240)">
                <rect x="0" y="0" width="48" height="65" rx="8" fill="#1e293b" stroke="#050608" stroke-width="4.5"/>
                <line x1="2" y1="20" x2="46" y2="20" stroke="#facc15" stroke-width="3"/>
                <line x1="2" y1="44" x2="46" y2="44" stroke="#facc15" stroke-width="3"/>
                <circle cx="24" cy="32" r="10" fill="#dc2626"/>
            </g>
        """
    elif handheld_prop == "pearl_oyster":
        prop_svg = """
            <g id="prop-pearl-oyster" transform="translate(210, 245)">
                <ellipse cx="20" cy="18" rx="22" ry="16" fill="#0284c7" stroke="#050608" stroke-width="4"/>
                <circle cx="20" cy="18" r="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
            </g>
        """
    elif handheld_prop == "dagger_behind_back":
        prop_svg = """
            <g id="prop-dagger" transform="translate(85, 270) rotate(-45)">
                <polygon points="0,0 6,-35 12,0" fill="#cbd5e1" stroke="#050608" stroke-width="3"/>
                <rect x="2" y="0" width="8" height="16" rx="2" fill="#78350f" stroke="#050608" stroke-width="3"/>
                <line x1="-4" y1="0" x2="16" y2="0" stroke="#facc15" stroke-width="4"/>
            </g>
        """
    elif handheld_prop == "treaty_scroll":
        prop_svg = """
            <g id="prop-treaty-scroll" transform="translate(200, 235) rotate(15)">
                <rect x="0" y="0" width="36" height="54" rx="4" fill="#fef3c7" stroke="#050608" stroke-width="4"/>
                <line x1="6" y1="12" x2="30" y2="12" stroke="#050608" stroke-width="2.5"/>
                <line x1="6" y1="22" x2="30" y2="22" stroke="#050608" stroke-width="2.5"/>
                <circle cx="18" cy="38" r="7" fill="#dc2626"/>
            </g>
        """
    elif handheld_prop == "magnifying_glass":
        prop_svg = """
            <g id="prop-mag-glass" transform="translate(210, 220) rotate(25)">
                <circle cx="18" cy="18" r="18" fill="#e0f2fe" opacity="0.8" stroke="#050608" stroke-width="5"/>
                <rect x="14" y="36" width="8" height="28" rx="3" fill="#78350f" stroke="#050608" stroke-width="4"/>
            </g>
        """
    elif handheld_prop == "quill_pen":
        prop_svg = """
            <g id="prop-quill" transform="translate(220, 230) rotate(-35)">
                <path d="M 0 40 Q 15 20 25 0 Q 15 15 0 40 Z" fill="#f8fafc" stroke="#050608" stroke-width="3"/>
                <line x1="0" y1="40" x2="4" y2="48" stroke="#050608" stroke-width="3"/>
            </g>
        """
    elif handheld_prop == "sword":
        prop_svg = """
            <g id="prop-sword" transform="translate(230, 180) rotate(-20)">
                <polygon points="4,-60 12,-60 14,10 2,10" fill="#e2e8f0" stroke="#050608" stroke-width="4"/>
                <rect x="0" y="10" width="16" height="5" rx="2" fill="#facc15" stroke="#050608" stroke-width="3"/>
                <rect x="5" y="15" width="6" height="18" rx="2" fill="#78350f" stroke="#050608" stroke-width="3"/>
            </g>
        """
    elif handheld_prop == "briefcase_cash":
        prop_svg = """
            <g id="prop-briefcase" transform="translate(215, 260)">
                <rect x="0" y="10" width="55" height="42" rx="4" fill="#451a03" stroke="#050608" stroke-width="4.5"/>
                <path d="M 18 10 L 18 2 L 36 2 L 36 10" stroke="#050608" stroke-width="4" fill="none"/>
                <circle cx="27" cy="30" r="5" fill="#facc15"/>
            </g>
        """

    # 4. Asymmetric Poses & Limbs
    limbs_svg = ""
    extra_props_svg = prop_svg

    if pose == "pointing_up_board":
        limbs_svg = f"""
            <!-- Left Arm: relaxed at side -->
            <path d="M 106 230 Q 92 270 96 310" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 230 Q 92 270 96 310" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="96" cy="312" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>

            <!-- Right Arm: raised diagonally pointing up -->
            <path d="M 214 230 Q 240 180 260 130" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 230 Q 240 180 260 130" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="260" cy="130" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>
            <!-- Pointing index finger -->
            <path d="M 260 130 L 275 110" stroke="#050608" stroke-width="9" stroke-linecap="round"/>
            <path d="M 260 130 L 275 110" stroke="{skin_tone}" stroke-width="5" stroke-linecap="round"/>
        """
    elif pose == "head_clutch_panic":
        limbs_svg = f"""
            <!-- Left Arm: gripping head in shock -->
            <path d="M 106 240 Q 65 180 110 135" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 240 Q 65 180 110 135" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="110" cy="135" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>

            <!-- Right Arm: gripping head in shock -->
            <path d="M 214 240 Q 255 180 210 135" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 240 Q 255 180 210 135" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="210" cy="135" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>
        """
    elif pose == "chin_stroke_thinking":
        limbs_svg = f"""
            <!-- Left Arm: crossed horizontally across chest -->
            <path d="M 106 240 Q 150 255 180 250" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 240 Q 150 255 180 250" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>

            <!-- Right Arm: elbow resting on left arm, hand stroking chin -->
            <path d="M 214 240 Q 190 230 170 196" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 240 Q 190 230 170 196" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="170" cy="196" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>
        """
    elif pose == "shh_finger_lips":
        limbs_svg = f"""
            <!-- Left Arm: relaxed at side -->
            <path d="M 106 230 Q 92 270 96 310" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 230 Q 92 270 96 310" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="96" cy="312" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>

            <!-- Right Arm: hand raised to mouth with upright index finger -->
            <path d="M 214 240 Q 200 200 168 186" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 240 Q 200 200 168 186" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="168" cy="186" r="11" fill="{skin_tone}" stroke="#050608" stroke-width="4"/>
            <line x1="168" y1="186" x2="168" y2="165" stroke="#050608" stroke-width="8" stroke-linecap="round"/>
            <line x1="168" y1="186" x2="168" y2="165" stroke="{skin_tone}" stroke-width="4.5" stroke-linecap="round"/>
        """
    elif pose == "ear_cupping_listen" or pose == "ear_listening":
        limbs_svg = f"""
            <!-- Left Arm: hand cupping ear -->
            <path d="M 106 240 Q 75 190 98 144" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 240 Q 75 190 98 144" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <!-- Hand cupped behind left ear -->
            <path d="M 96 130 C 88 135 88 155 96 160" stroke="#050608" stroke-width="6" fill="{skin_tone}"/>

            <!-- Right Arm: reaching forward tensely -->
            <path d="M 214 235 Q 235 250 250 270" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 235 Q 235 250 250 270" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="250" cy="270" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>
        """
    elif pose == "holding_prop_chest":
        limbs_svg = f"""
            <!-- Left Arm: supporting prop from below -->
            <path d="M 106 240 Q 140 260 170 265" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 240 Q 140 260 170 265" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="170" cy="265" r="11" fill="{skin_tone}" stroke="#050608" stroke-width="4"/>

            <!-- Right Arm: wrapped forward holding prop -->
            <path d="M 214 240 Q 230 255 210 270" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 240 Q 230 255 210 270" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="210" cy="270" r="11" fill="{skin_tone}" stroke="#050608" stroke-width="4"/>
        """
    elif pose == "namaste_greeting":
        limbs_svg = f"""
            <!-- Both hands joined in namaste at chest -->
            <path d="M 106 235 Q 135 240 156 225" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 235 Q 135 240 156 225" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <path d="M 214 235 Q 185 240 164 225" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 235 Q 185 240 164 225" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <ellipse cx="160" cy="222" rx="10" ry="18" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>
        """
    elif pose == "sword_raised":
        limbs_svg = f"""
            <!-- Left Arm: tense fist on hip -->
            <path d="M 106 230 Q 90 260 100 270" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 230 Q 90 260 100 270" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="100" cy="272" r="11" fill="{skin_tone}" stroke="#050608" stroke-width="4"/>

            <!-- Right Arm: raised holding sword vertically -->
            <path d="M 214 230 Q 235 180 230 160" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 230 Q 235 180 230 160" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="230" cy="160" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>
        """
    elif pose == "arms_crossed_skeptical":
        limbs_svg = f"""
            <!-- Both Arms crossed over chest -->
            <path d="M 106 235 Q 160 255 204 240" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 235 Q 160 255 204 240" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <path d="M 214 235 Q 160 265 116 245" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 235 Q 160 265 116 245" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
        """
    elif pose == "shock_lean_back":
        limbs_svg = f"""
            <!-- Both Arms thrown up and back -->
            <path d="M 106 230 Q 80 170 70 140" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 230 Q 80 170 70 140" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="70" cy="140" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>
            <path d="M 214 230 Q 240 170 250 140" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 230 Q 240 170 250 140" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="250" cy="140" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>
        """
    else:  # standing
        limbs_svg = f"""
            <!-- Asymmetric standing limbs -->
            <path d="M 106 230 Q 94 270 98 310" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 106 230 Q 94 270 98 310" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="98" cy="312" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>

            <path d="M 214 230 Q 224 265 218 305" stroke="#050608" stroke-width="24" stroke-linecap="round" fill="none"/>
            <path d="M 214 230 Q 224 265 218 305" stroke="{coat_color}" stroke-width="16" stroke-linecap="round" fill="none"/>
            <circle cx="218" cy="308" r="12" fill="{skin_tone}" stroke="#050608" stroke-width="4.5"/>
        """

    # 5. Rim Light Stroke Layer
    rim_stroke_svg = ""
    if rim_side == "right":
        rim_stroke_svg = f"""
            <!-- Warm Environmental Rim Light on right edge -->
            <path d="M 160 74 C 200 74 220 102 220 144 C 220 186 200 214 160 214" fill="none" stroke="{rim_color}" stroke-width="6" opacity="0.85" filter="url(#glow-rim)"/>
            <path d="M 204 220 C 218 245 220 280 206 330" fill="none" stroke="{rim_color}" stroke-width="6" opacity="0.8" filter="url(#glow-rim)"/>
        """
    elif rim_side == "left":
        rim_stroke_svg = f"""
            <!-- Cool Environmental Rim Light on left edge -->
            <path d="M 160 74 C 120 74 100 102 100 144 C 100 186 120 214 160 214" fill="none" stroke="{rim_color}" stroke-width="6" opacity="0.85" filter="url(#glow-rim)"/>
            <path d="M 116 220 C 102 245 100 280 114 330" fill="none" stroke="{rim_color}" stroke-width="6" opacity="0.8" filter="url(#glow-rim)"/>
        """

    # 6. Torso & Clothes
    torso_svg = f"""
        <!-- Coat / Body Torso -->
        <path d="M 114 214 C 114 214 102 245 106 330 L 214 330 C 218 245 206 214 206 214 Z" fill="{coat_color}" stroke="#050608" stroke-width="6"/>
        <!-- Vest / Inner Shirt -->
        <path d="M 134 214 L 142 330 L 178 330 L 186 214 Z" fill="{vest_color}" stroke="#050608" stroke-width="4.5"/>
        <line x1="160" y1="214" x2="160" y2="330" stroke="#050608" stroke-width="3"/>
        <circle cx="160" cy="245" r="3.5" fill="#facc15"/>
        <circle cx="160" cy="275" r="3.5" fill="#facc15"/>
        <circle cx="160" cy="305" r="3.5" fill="#facc15"/>
    """

    # 7. Legs & Shoes
    legs_svg = f"""
        <!-- Left Leg & Shoe -->
        <rect x="124" y="325" width="28" height="75" rx="6" fill="#1e293b" stroke="#050608" stroke-width="5"/>
        <ellipse cx="132" cy="405" rx="20" ry="10" fill="#0f172a" stroke="#050608" stroke-width="4.5"/>
        <!-- Right Leg & Shoe -->
        <rect x="168" y="325" width="28" height="75" rx="6" fill="#1e293b" stroke="#050608" stroke-width="5"/>
        <ellipse cx="188" cy="405" rx="20" ry="10" fill="#0f172a" stroke="#050608" stroke-width="4.5"/>
    """

    # 8. Head & Face Monolith
    head_svg = f"""
        <g id="char-head">
            <!-- OverSimplified Classic Egg Head (center 160, 144) -->
            <ellipse cx="160" cy="144" rx="62" ry="70" fill="{skin_tone}" stroke="#050608" stroke-width="6"/>
            <!-- Hair Base -->
            <path d="M 104 140 C 98 100 120 74 160 74 C 200 74 222 100 216 140 C 206 90 114 90 104 140 Z" fill="{hair_color}" stroke="#050608" stroke-width="5"/>
            {hat_svg}
            {rim_stroke_svg}
            {eyebrows_svg}
            {eyes_svg}
            {mouth_svg}
            {sweat_svg}
        </g>
    """

    # 9. Optional Nameplate
    nameplate_svg = ""
    if show_nameplate and name:
        clean_title = name.replace("_", " ").upper()
        nameplate_svg = f"""
            <g id="nameplate" transform="translate(160, 420)">
                <rect x="-70" y="-12" width="140" height="24" rx="4" fill="#0f172a" opacity="0.85" stroke="#facc15" stroke-width="2"/>
                <text x="0" y="5" font-family="Arial, sans-serif" font-weight="900" font-size="12" fill="#ffffff" text-anchor="middle">{clean_title}</text>
            </g>
        """

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
  <defs>
    <filter id="soft-shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
    <filter id="glow-rim" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>
  <!-- Floor Contact Shadow -->
  <ellipse cx="160" cy="425" rx="85" ry="18" fill="#020305" opacity="0.75" filter="url(#soft-shadow)"/>
  <!-- Legs -->
  {legs_svg}
  <!-- Torso -->
  {torso_svg}
  <!-- Arms & Gestures -->
  {limbs_svg}
  {extra_props_svg}
  <!-- Head & Micro-Expressions -->
  {head_svg}
  {nameplate_svg}
</svg>"""

    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"✅ Generated Master Character Rig: {output_path} (Name: {name}, Pose: {pose}, Expression: {expression}, Hat: {hat_type}, Prop: {handheld_prop})")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate Cinematic Chibi Character Rig")
    parser.add_argument("--name", default="resistance_fighter")
    parser.add_argument("--expression", default="shocked", help="Expression keyword (shocked, panicked, intense_dread, thinking, neutral, smug, happy, angry, crying, dollar_eyes, knockout, or custom)")
    parser.add_argument("--pose", default="pointing_up_board", help="Pose keyword (pointing_up_board, head_clutch_panic, chin_stroke_thinking, shh_finger_lips, holding_prop_chest, ear_cupping_listen, standing, namaste_greeting, sword_raised, arms_crossed_skeptical, shock_lean_back, or custom)")
    parser.add_argument("--hat", default=None, help="Hat / headdress type (keffiyeh, powdered_wig, bicorne, ashoka_crown, royal_mukut, turban, pagri, gandhi_topi, military_cap, top_hat, or custom)")
    parser.add_argument("--hair-color", default="#1f2937")
    parser.add_argument("--coat-color", default="#2b303c")
    parser.add_argument("--vest-color", default="#cbd5e1")
    parser.add_argument("--skin-tone", default="#ffffff")
    parser.add_argument("--rim-color", default="#fbbf24")
    parser.add_argument("--rim-side", default="right", choices=["left", "right"])
    parser.add_argument("--prop", default=None, help="Handheld prop (test_tube, clipboard, karak_chai, oil_barrel, pearl_oyster, dagger_behind_back, treaty_scroll, magnifying_glass, quill_pen, sword, briefcase_cash, or custom)")
    parser.add_argument("--nameplate", action="store_true", help="Display nameplate at bottom")
    parser.add_argument("--out", default="char_cinematic.svg")
    args = parser.parse_args()

    prop_val = None if (args.prop in ["none", "", None]) else args.prop
    hat_val = None if (args.hat in ["none", "", None]) else args.hat

    generate_chibi_character(
        name=args.name,
        skin_tone=args.skin_tone,
        coat_color=args.coat_color,
        vest_color=args.vest_color,
        hair_color=args.hair_color,
        hat_type=hat_val,
        expression=args.expression,
        pose=args.pose,
        rim_color=args.rim_color,
        rim_side=args.rim_side,
        handheld_prop=prop_val,
        show_nameplate=args.nameplate,
        output_path=args.out
    )


if __name__ == "__main__":
    main()
