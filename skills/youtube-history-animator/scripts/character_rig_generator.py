"""
character_rig_generator.py
Generates cinematic OverSimplified / History Matters vector SVG character rigs.
Supports directional environmental rim lighting, expressive facial micro-features (dread, panic, shock, smug),
anti-clone asymmetric gesture presets, and weighted contact shadows on a strict 320x440 canvas.
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
    output_path="character.svg"
):
    """
    Renders a monolithic OverSimplified 320x440 character rig with asymmetric arms and physical rim lighting.
    Modular Poses:
      - pointing_up_board: Right arm raised diagonally holding chalk/pointer to board.
      - head_clutch_panic: Both arms curved upward gripping sides of head in shock.
      - chin_stroke_thinking: Left arm crossed, right hand to chin with asymmetric furrowed brow.
      - shh_finger_lips: Hand raised to mouth with upright index finger over tense 'O' mouth.
      - holding_prop_chest: Forearm angled across torso holding handheld prop.
      - ear_cupping_listen: Body leaned 12deg, back hand cupping ear, front hand reaching dial.
      - standing: Natural asymmetric standing pose.
    """
    # 1. Expressions & Eyes (Strict FACE_CONFIG: Eyebrows Y in [124, 128], Eyes center (160, 144), Mouth Y=186)
    eyes_svg = ""
    eyebrows_svg = ""
    mouth_svg = ""
    sweat_svg = ""

    if expression == "shocked" or expression == "panicked":
        eyes_svg = """
            <ellipse cx="138" cy="144" rx="13" ry="16" fill="#ffffff" stroke="#050608" stroke-width="5"/>
            <circle cx="138" cy="144" r="5" fill="#050608"/>
            <ellipse cx="182" cy="144" rx="13" ry="16" fill="#ffffff" stroke="#050608" stroke-width="5"/>
            <circle cx="182" cy="144" r="5" fill="#050608"/>
        """
        eyebrows_svg = """
            <path d="M 122 124 Q 138 112 152 126" stroke="#050608" stroke-width="5.5" stroke-linecap="round" fill="none"/>
            <path d="M 168 126 Q 182 112 198 124" stroke="#050608" stroke-width="5.5" stroke-linecap="round" fill="none"/>
            <path d="M 130 162 Q 138 166 146 162 M 174 162 Q 182 166 190 162" stroke="#050608" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.6"/>
        """
        mouth_svg = '<ellipse cx="160" cy="186" rx="11" ry="9" fill="#050608"/>'
        sweat_svg = '<path d="M 205 130 C 212 142 212 152 205 156 C 198 152 198 142 205 130 Z" fill="#38bdf8" stroke="#050608" stroke-width="3"/>'
    elif expression == "intense_dread":
        eyes_svg = """
            <ellipse cx="138" cy="144" rx="12" ry="14" fill="#ffffff" stroke="#050608" stroke-width="5.5"/>
            <circle cx="136" cy="142" r="4.5" fill="#050608"/>
            <ellipse cx="182" cy="144" rx="12" ry="14" fill="#ffffff" stroke="#050608" stroke-width="5.5"/>
            <circle cx="180" cy="142" r="4.5" fill="#050608"/>
        """
        eyebrows_svg = """
            <path d="M 122 130 L 152 138" stroke="#050608" stroke-width="7" stroke-linecap="round"/>
            <path d="M 168 138 L 198 130" stroke="#050608" stroke-width="7" stroke-linecap="round"/>
        """
        mouth_svg = """
            <path d="M 144 186 Q 160 176 176 186 Q 160 196 144 186 Z" fill="#1f2937" stroke="#050608" stroke-width="4"/>
        """
        sweat_svg = '<path d="M 115 132 C 122 144 122 154 115 158 C 108 154 108 144 115 132 Z" fill="#fde047" stroke="#050608" stroke-width="3.5"/>'
    elif expression == "thinking":
        eyes_svg = """
            <ellipse cx="138" cy="144" rx="11" ry="12" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <circle cx="141" cy="140" r="4.5" fill="#050608"/>
            <ellipse cx="182" cy="144" rx="11" ry="12" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <circle cx="185" cy="140" r="4.5" fill="#050608"/>
        """
        # Asymmetric brow: one raised, one lowered
        eyebrows_svg = """
            <path d="M 124 122 Q 138 114 152 122" stroke="#050608" stroke-width="5.5" stroke-linecap="round" fill="none"/>
            <path d="M 168 132 Q 182 134 196 128" stroke="#050608" stroke-width="5.5" stroke-linecap="round" fill="none"/>
        """
        mouth_svg = '<path d="M 148 186 Q 160 182 172 188" stroke="#050608" stroke-width="4.5" stroke-linecap="round" fill="none"/>'
    else:  # neutral / determined
        eyes_svg = """
            <circle cx="138" cy="144" r="6" fill="#050608"/>
            <circle cx="182" cy="144" r="6" fill="#050608"/>
        """
        eyebrows_svg = """
            <line x1="124" y1="126" x2="152" y2="126" stroke="#050608" stroke-width="5.5" stroke-linecap="round"/>
            <line x1="168" y1="126" x2="196" y2="126" stroke="#050608" stroke-width="5.5" stroke-linecap="round"/>
        """
        mouth_svg = '<line x1="148" y1="186" x2="172" y2="186" stroke="#050608" stroke-width="5" stroke-linecap="round"/>'

    # 2. Environmental Directional Rim Lighting
    head_rim_svg = ""
    torso_rim_svg = ""
    if rim_color:
        if rim_side == "right":
            head_rim_svg = f'<path d="M 195 88 A 72 72 0 0 1 198 210 A 58 68 0 0 0 195 88 Z" fill="{rim_color}" opacity="0.6"/>'
            torso_rim_svg = f'<path d="M 210 220 L 222 360" stroke="{rim_color}" stroke-width="6" stroke-linecap="round" opacity="0.8"/>'
        else:
            head_rim_svg = f'<path d="M 125 88 A 72 72 0 0 0 122 210 A 58 68 0 0 1 125 88 Z" fill="{rim_color}" opacity="0.6"/>'
            torso_rim_svg = f'<path d="M 110 220 L 98 360" stroke="{rim_color}" stroke-width="6" stroke-linecap="round" opacity="0.8"/>'

    # 3. Base Torso & Legs
    legs_svg = """
        <line x1="135" y1="360" x2="135" y2="420" stroke="#050608" stroke-width="14" stroke-linecap="round"/>
        <line x1="185" y1="360" x2="185" y2="420" stroke="#050608" stroke-width="14" stroke-linecap="round"/>
        <ellipse cx="130" cy="422" rx="20" ry="10" fill="#090b10" stroke="#050608" stroke-width="5"/>
        <ellipse cx="190" cy="422" rx="20" ry="10" fill="#090b10" stroke="#050608" stroke-width="5"/>
    """

    torso_svg = f"""
        <!-- Torso Base -->
        <path d="M 105 200 C 95 260 95 320 115 365 L 205 365 C 225 320 225 260 215 200 Z" fill="{coat_color}" stroke="#050608" stroke-width="8" stroke-linejoin="round"/>
        <path d="M 130 200 L 190 200 L 195 365 L 125 365 Z" fill="{vest_color}" stroke="#050608" stroke-width="5" stroke-linejoin="round"/>
        <!-- Chin AO shadow -->
        <path d="M 115 198 Q 160 218 205 198 C 195 216, 125 216, 115 198 Z" fill="#050608" opacity="0.25"/>
        {torso_rim_svg}
    """

    # 4. Modular Arm & Gesture Presets (The 6 Modular Poses)
    limbs_svg = ""
    extra_props_svg = ""

    if pose == "pointing_up_board":
        # Right noodle arm raised diagonally holding chalk/pointer stick
        limbs_svg = f"""
            <!-- Left Arm: Resting at hip -->
            <path d="M 115 240 Q 80 280 105 320" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="106" cy="324" r="13" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <!-- Right Arm: Pointing Up to Board -->
            <path d="M 205 260 C 245 230 265 180 285 135" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="286" cy="132" r="13" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <!-- Chalk / Pointer Stick -->
            <rect x="282" y="98" width="8" height="34" rx="2" fill="#fef08a" stroke="#050608" stroke-width="2.5" transform="rotate(22 286 115)"/>
        """

    elif pose == "head_clutch_panic":
        # Both arms curved upward with hands gripping sides of head in disbelief
        limbs_svg = f"""
            <!-- Left Arm Clutching Head -->
            <path d="M 115 260 C 75 220 80 150 110 125" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="110" cy="122" r="13" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <!-- Right Arm Clutching Head -->
            <path d="M 205 260 C 245 220 240 150 210 125" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="210" cy="122" r="13" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
        """

    elif pose == "chin_stroke_thinking":
        # Left arm crossed under chest, right hand raised to chin (175, 202)
        limbs_svg = f"""
            <!-- Left Arm Crossed Under Chest -->
            <path d="M 115 260 C 135 290 190 290 205 270" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="206" cy="270" r="12" fill="#ffffff" stroke="#050608" stroke-width="4"/>
            <!-- Right Arm Stroking Chin -->
            <path d="M 205 260 C 220 230 195 210 175 202" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="175" cy="202" r="13" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
        """

    elif pose == "shh_finger_lips":
        # Hand raised to (160, 188) with upright index finger over mouth
        limbs_svg = f"""
            <!-- Left Arm: Bracing at side -->
            <path d="M 115 240 C 85 265 75 290 60 280" stroke="#050608" stroke-width="18" stroke-linecap="round" fill="none"/>
            <circle cx="58" cy="278" r="12" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <!-- Right Arm: Hand to Lips with Shh Finger -->
            <path d="M 205 250 C 230 240 200 205 165 188" stroke="#050608" stroke-width="18" stroke-linecap="round" fill="none"/>
            <g transform="translate(160, 185)">
                <circle cx="0" cy="0" r="12" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
                <rect x="-4" y="-24" width="8" height="22" rx="4" fill="#ffffff" stroke="#050608" stroke-width="4"/>
            </g>
        """

    elif pose == "holding_prop_chest":
        # Forearm angled across torso holding topic prop
        limbs_svg = f"""
            <!-- Left Arm: Holding Base -->
            <path d="M 115 240 C 130 270 150 280 170 275" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="170" cy="275" r="12" fill="#ffffff" stroke="#050608" stroke-width="4"/>
            <!-- Right Arm: Clasping Prop -->
            <path d="M 205 240 C 190 270 170 275 160 270" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="160" cy="270" r="12" fill="#ffffff" stroke="#050608" stroke-width="4"/>
        """
        if handheld_prop == "test_tube":
            extra_props_svg = """
                <!-- Translucent Bubbling Test Tube -->
                <g transform="translate(165, 235)">
                    <rect x="-7" y="-25" width="14" height="42" rx="7" fill="rgba(56, 189, 248, 0.75)" stroke="#050608" stroke-width="3"/>
                    <ellipse cx="0" cy="-25" rx="7" ry="2" fill="#ffffff" opacity="0.6"/>
                    <circle cx="-2" cy="0" r="2" fill="#ffffff" opacity="0.8"/>
                    <circle cx="2" cy="8" r="1.5" fill="#ffffff" opacity="0.8"/>
                    <path d="M -4 -20 L -4 10" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" opacity="0.7"/>
                </g>
            """
        elif handheld_prop == "clipboard":
            extra_props_svg = """
                <!-- Scientific Clipboard -->
                <rect x="145" y="225" width="38" height="52" rx="3" fill="#d97706" stroke="#050608" stroke-width="3"/>
                <rect x="149" y="232" width="30" height="40" fill="#ffffff"/>
                <rect x="156" y="222" width="16" height="6" rx="2" fill="#71717a" stroke="#050608" stroke-width="2"/>
                <line x1="153" y1="242" x2="175" y2="242" stroke="#050608" stroke-width="2"/>
                <line x1="153" y1="250" x2="175" y2="250" stroke="#050608" stroke-width="2"/>
                <line x1="153" y1="258" x2="168" y2="258" stroke="#050608" stroke-width="2"/>
            """
        elif handheld_prop == "karak_chai":
            extra_props_svg = """
                <!-- Steaming Glass of Karak Chai -->
                <polygon points="154,235 174,235 171,265 157,265" fill="#b45309" stroke="#050608" stroke-width="2.5"/>
                <ellipse cx="164" cy="235" rx="10" ry="3" fill="#d97706"/>
                <path d="M 160 228 Q 164 220 162 215" stroke="#ffffff" stroke-width="2" stroke-linecap="round" fill="none" opacity="0.7"/>
            """

    elif pose == "ear_cupping_listen":
        # Body leaned 12deg toward sound, back hand cupping ear (102, 145), front hand reaching dial
        limbs_svg = f"""
            <!-- Back Arm: Cupping Ear at (102, 145) -->
            <path d="M 115 220 C 75 205 85 130 102 145" stroke="#050608" stroke-width="18" stroke-linecap="round" fill="none"/>
            <circle cx="102" cy="145" r="13" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <!-- Front Arm: Reaching out -->
            <path d="M 205 240 C 245 270 280 250 295 220" stroke="#050608" stroke-width="18" stroke-linecap="round" fill="none"/>
            <circle cx="295" cy="220" r="13" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
        """

    else:  # standard active standing with natural asymmetry
        limbs_svg = f"""
            <path d="M 110 220 Q 80 270 95 320" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="96" cy="324" r="13" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
            <path d="M 210 220 Q 235 270 220 320" fill="none" stroke="#050608" stroke-width="18" stroke-linecap="round"/>
            <circle cx="218" cy="324" r="13" fill="#ffffff" stroke="#050608" stroke-width="4.5"/>
        """

    # 5. Head
    head_svg = f"""
        <g id="head">
            <circle cx="160" cy="144" r="64" fill="{skin_tone}" stroke="#050608" stroke-width="8"/>
            {head_rim_svg}
            {eyebrows_svg}
            {eyes_svg}
            {mouth_svg}
            {sweat_svg}
        </g>
    """

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
  <defs>
    <filter id="soft-shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
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
</svg>"""

    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"✅ Generated Master Character Rig: {output_path} (Pose: {pose}, Expression: {expression})")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate Cinematic Chibi Character Rig")
    parser.add_argument("--name", default="scientist")
    parser.add_argument("--expression", default="shocked", choices=["shocked", "panicked", "intense_dread", "thinking", "neutral"])
    parser.add_argument("--pose", default="pointing_up_board", choices=[
        "pointing_up_board", "head_clutch_panic", "chin_stroke_thinking",
        "shh_finger_lips", "holding_prop_chest", "ear_cupping_listen", "standing"
    ])
    parser.add_argument("--rim-color", default="#fbbf24")
    parser.add_argument("--rim-side", default="right", choices=["left", "right"])
    parser.add_argument("--prop", default=None, choices=["test_tube", "clipboard", "karak_chai", "none"])
    parser.add_argument("--out", default="char_cinematic.svg")
    args = parser.parse_args()

    prop_val = None if args.prop == "none" else args.prop
    generate_chibi_character(
        name=args.name,
        expression=args.expression,
        pose=args.pose,
        rim_color=args.rim_color,
        rim_side=args.rim_side,
        handheld_prop=prop_val,
        output_path=args.out
    )


if __name__ == "__main__":
    main()
