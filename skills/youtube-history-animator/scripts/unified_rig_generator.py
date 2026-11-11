"""
engine_2d/unified_rig_generator.py
Generates broadcast-quality, anatomically unified OverSimplified / History Matters 2D character rigs.
Renders pixel-perfect 1:1 transparent PNGs (320x440) via Chrome headless so facial coordinates
(eyes, eyebrows, monocle, spectacles, nose clip, mouth, beard) match with mathematical precision.

UPGRADE 1: Graphic-Novel Vector Spec
- Outer silhouette strokes: stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"
- Inner cloth folds, belts, collars: stroke-width="3.5"
- Cel-shaded two-tone ambient occlusion (<path> under chin Y=200..218, under hat/ghutra brim, torso back edge)
- Clean, open facial canvas (X in [105, 215], Y in [100, 220]) for high-contrast FACE_CONFIG
"""

import os
import subprocess
from PIL import Image

SPRITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
os.makedirs(SPRITES_DIR, exist_ok=True)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CHARACTER_RIGS = {
    # ================= 1. SHEIKH ZAYED BIN SULTAN AL NAHYAN =================
    "sheikh_zayed": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
      <defs>
        <radialGradient id="zSkin" cx="45%" cy="40%" r="55%">
          <stop offset="0%" stop-color="#fae3cb"/>
          <stop offset="85%" stop-color="#e8ba8c"/>
          <stop offset="100%" stop-color="#d49c6e"/>
        </radialGradient>
        <linearGradient id="zBisht" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#2a221b"/>
          <stop offset="50%" stop-color="#3c3127"/>
          <stop offset="100%" stop-color="#1f1812"/>
        </linearGradient>
        <linearGradient id="goldZari" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#fbbf24"/>
          <stop offset="50%" stop-color="#f59e0b"/>
          <stop offset="100%" stop-color="#d97706"/>
        </linearGradient>
      </defs>

      <!-- Ghutra Back Drape Layer (Cel-Shaded White Fabric) -->
      <path d="M 60 140 C 45 60, 275 60, 260 140 C 285 220, 290 320, 275 380 C 255 350, 235 250, 220 200 C 190 190, 130 190, 100 200 C 85 250, 65 350, 45 380 C 30 320, 35 220, 60 140 Z"
            fill="#f1f5f9" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Ghutra Back Shadow Edge -->
      <path d="M 45 380 C 30 320, 35 220, 60 140 C 55 180, 52 280, 68 340 Z" fill="#cbd5e1"/>
      <path d="M 275 380 C 290 320, 285 220, 260 140 C 265 180, 268 280, 252 340 Z" fill="#cbd5e1"/>

      <!-- White Kandura Torso Base -->
      <path d="M 95 190 C 95 180, 225 180, 225 190 L 255 420 C 205 432, 115 432, 65 420 Z"
            fill="#ffffff" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
      <!-- Kandura Side Shadow -->
      <path d="M 65 420 L 95 190 L 115 190 L 90 422 Z" fill="#e2e8f0"/>

      <!-- Royal Bisht Robe with Cel-Shaded Fold Shadows -->
      <path d="M 80 185 C 80 170, 240 170, 240 185 L 265 425 C 215 435, 105 435, 55 425 Z"
            fill="url(#zBisht)" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Bisht Outer Dark Crease AO Path -->
      <path d="M 55 425 L 80 185 L 105 185 L 75 427 Z" fill="#150f0b"/>
      <path d="M 265 425 L 240 185 L 220 185 L 248 427 Z" fill="#150f0b"/>

      <!-- Gold Zari Embroidery -->
      <path d="M 125 185 L 160 300 L 195 185" fill="none" stroke="url(#goldZari)" stroke-width="9" stroke-linecap="round"/>
      <path d="M 160 300 L 160 430" fill="none" stroke="url(#goldZari)" stroke-width="6.5" stroke-linecap="round"/>
      <line x1="125" y1="185" x2="160" y2="300" stroke="#090a0f" stroke-width="1.5" stroke-dasharray="3,3"/>
      <line x1="195" y1="185" x2="160" y2="300" stroke="#090a0f" stroke-width="1.5" stroke-dasharray="3,3"/>

      <!-- Arms & Gesturing Hands -->
      <path d="M 80 200 Q 30 260 65 330" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 80 200 Q 30 260 65 330" fill="none" stroke="url(#zBisht)" stroke-width="16" stroke-linecap="round"/>
      <path d="M 240 200 Q 290 260 255 330" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 240 200 Q 290 260 255 330" fill="none" stroke="url(#zBisht)" stroke-width="16" stroke-linecap="round"/>
      <circle cx="68" cy="335" r="14" fill="#fae3cb" stroke="#090a0f" stroke-width="4.5"/>
      <circle cx="252" cy="335" r="14" fill="#fae3cb" stroke="#090a0f" stroke-width="4.5"/>

      <!-- Head Base (Pill Shape) sitting directly on collar -->
      <path d="M 85 140 C 85 80, 235 80, 235 140 C 235 220, 85 220, 85 140 Z"
            fill="#fae3cb" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>

      <!-- Crisp Cel-Shaded Chin & Neck Collar Ambient Occlusion (Y in [198, 220]) -->
      <path d="M 105 198 Q 160 218 215 198 C 205 220, 115 220, 105 198 Z" fill="#d49c6e"/>
      <path d="M 120 202 Q 160 216 200 202 C 185 218, 135 218, 120 202 Z" fill="#b87333" opacity="0.4"/>

      <!-- Ghutra Framing Drapes (Face Left and Right Open) -->
      <path d="M 90 95 C 70 120, 55 180, 68 310 C 80 290, 88 230, 96 170 C 92 135, 88 115, 90 95 Z"
            fill="#ffffff" stroke="#090a0f" stroke-width="5" stroke-linejoin="round"/>
      <path d="M 230 95 C 250 120, 265 180, 252 310 C 240 290, 232 230, 224 170 C 228 135, 232 115, 230 95 Z"
            fill="#ffffff" stroke="#090a0f" stroke-width="5" stroke-linejoin="round"/>
      <path d="M 85 105 Q 160 70 235 105 Q 160 90 85 105 Z" fill="#ffffff" stroke="#090a0f" stroke-width="5"/>
      <!-- Shadow under Ghutra Brim onto Forehead -->
      <path d="M 92 108 Q 160 120 228 108 Q 160 100 92 108 Z" fill="#e2ba94" opacity="0.75"/>

      <!-- Black Agal Dual Rings with Gold Thread -->
      <ellipse cx="160" cy="92" rx="72" ry="16" fill="none" stroke="#090a0f" stroke-width="14"/>
      <ellipse cx="160" cy="92" rx="72" ry="16" fill="none" stroke="#27272a" stroke-width="8"/>
      <ellipse cx="160" cy="104" rx="68" ry="15" fill="none" stroke="#090a0f" stroke-width="13"/>
      <ellipse cx="160" cy="104" rx="68" ry="15" fill="none" stroke="#27272a" stroke-width="7"/>
      <path d="M 225 104 Q 238 145 235 185" fill="none" stroke="url(#goldZari)" stroke-width="3.5" stroke-linecap="round"/>

      <!-- Cheeks Subtle Warmth -->
      <ellipse cx="118" cy="160" rx="10" ry="5" fill="#f87171" opacity="0.32"/>
      <ellipse cx="202" cy="160" rx="10" ry="5" fill="#f87171" opacity="0.32"/>

      <!-- Distinguished Royal Beard & Mustache (Graphic-Novel Ink) -->
      <path d="M 120 180 Q 160 220 200 180 Q 185 214 160 220 Q 135 214 120 180 Z"
            fill="#1c1917" stroke="#090a0f" stroke-width="4.5" stroke-linejoin="round"/>
      <path d="M 134 172 Q 160 184 186 172" fill="none" stroke="#1c1917" stroke-width="7.5" stroke-linecap="round"/>

      <!-- Eyebrows (Strict FACE_CONFIG: 160, 126, Y in [124, 128]) -->
      <path d="M 122 126 Q 138 118 152 126" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
      <path d="M 168 126 Q 182 118 198 126" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
    </svg>
    """,

    # ================= 2. BRITISH ROYAL NAVY OFFICER (1820) =================
    "british_officer": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
      <defs>
        <linearGradient id="bGold" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#fde047"/>
          <stop offset="50%" stop-color="#eab308"/>
          <stop offset="100%" stop-color="#ca8a04"/>
        </linearGradient>
      </defs>

      <!-- Royal Navy Deep Blue Coat Base -->
      <path d="M 90 190 C 90 180, 230 180, 230 190 L 255 400 C 205 410, 115 410, 65 400 Z"
            fill="#1e3a8a" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Cel-shaded Coat Shadow Path -->
      <path d="M 65 400 L 90 190 L 115 190 L 85 402 Z" fill="#0f172a"/>
      <path d="M 255 400 L 230 190 L 215 190 L 240 402 Z" fill="#0f172a"/>

      <!-- Crimson Lapels & White Cravat -->
      <path d="M 135 185 L 160 240 L 185 185 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="3.5"/>
      <path d="M 135 185 L 120 270 L 160 270 Z" fill="#b91c1c" stroke="#090a0f" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M 185 185 L 200 270 L 160 270 Z" fill="#b91c1c" stroke="#090a0f" stroke-width="3.5" stroke-linejoin="round"/>

      <!-- Double-Breasted Brass Buttons -->
      <g fill="url(#bGold)" stroke="#090a0f" stroke-width="2.5">
        <circle cx="138" cy="285" r="5.5"/> <circle cx="182" cy="285" r="5.5"/>
        <circle cx="138" cy="315" r="5.5"/> <circle cx="182" cy="315" r="5.5"/>
        <circle cx="138" cy="345" r="5.5"/> <circle cx="182" cy="345" r="5.5"/>
        <circle cx="138" cy="375" r="5.5"/> <circle cx="182" cy="375" r="5.5"/>
      </g>

      <!-- White Breeches & Black Naval Boots -->
      <path d="M 95 400 L 155 400 L 150 430 L 90 430 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="4"/>
      <path d="M 165 400 L 225 400 L 230 430 L 170 430 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="4"/>
      <rect x="85" y="420" width="70" height="18" rx="4" fill="#0f172a" stroke="#090a0f" stroke-width="3.5"/>
      <rect x="165" y="420" width="70" height="18" rx="4" fill="#0f172a" stroke="#090a0f" stroke-width="3.5"/>

      <!-- Golden Epaulettes on Shoulders -->
      <ellipse cx="85" cy="192" rx="22" ry="12" fill="url(#bGold)" stroke="#090a0f" stroke-width="4"/>
      <ellipse cx="235" cy="192" rx="22" ry="12" fill="url(#bGold)" stroke="#090a0f" stroke-width="4"/>

      <!-- Left Arm Behind Back, Right Arm Holding Brass Spyglass -->
      <path d="M 85 200 Q 55 250 80 310" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 85 200 Q 55 250 80 310" fill="none" stroke="#1e3a8a" stroke-width="16" stroke-linecap="round"/>
      <path d="M 235 200 Q 275 250 240 310" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 235 200 Q 275 250 240 310" fill="none" stroke="#1e3a8a" stroke-width="16" stroke-linecap="round"/>
      <circle cx="238" cy="315" r="12" fill="#fcd5b5" stroke="#090a0f" stroke-width="3.5"/>
      <!-- Spyglass in Hand -->
      <rect x="230" y="280" width="45" height="14" rx="3" transform="rotate(-35 230 280)" fill="url(#bGold)" stroke="#090a0f" stroke-width="3.5"/>

      <!-- Head Base (Pill Shape) sitting snugly on collar -->
      <path d="M 95 145 C 95 90, 225 90, 225 145 C 225 210, 95 210, 95 145 Z"
            fill="#fff1e6" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>

      <!-- Cel-Shaded Chin/Neck Shadow Path (Y in [198, 218]) -->
      <path d="M 112 198 Q 160 216 208 198 C 200 214, 120 214, 112 198 Z" fill="#e6b38a"/>

      <!-- Aristocratic Sideburns -->
      <path d="M 100 135 L 105 175 L 115 165 Z" fill="#78350f" stroke="#090a0f" stroke-width="2.5"/>
      <path d="M 220 135 L 215 175 L 205 165 Z" fill="#78350f" stroke="#090a0f" stroke-width="2.5"/>

      <!-- Grand Naval Bicorne Cocked Hat with Cockade & Gold Lace -->
      <path d="M 35 155 C 35 60, 285 60, 285 155 C 255 120, 65 120, 35 155 Z"
            fill="#09090b" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
      <path d="M 45 152 C 60 128, 260 128, 275 152" fill="none" stroke="url(#bGold)" stroke-width="5"/>
      <!-- Shadow under Bicorne Hat Brim -->
      <path d="M 65 125 Q 160 142 255 125 Q 160 120 65 125 Z" fill="#cbd5e1" opacity="0.65"/>

      <!-- British Cockade (Red, White, Blue Rosette) -->
      <circle cx="160" cy="120" r="14" fill="#b91c1c" stroke="#090a0f" stroke-width="3"/>
      <circle cx="160" cy="120" r="9" fill="#ffffff"/>
      <circle cx="160" cy="120" r="4.5" fill="#1e3a8a"/>

      <!-- Aristocratic Monocle on Left Eye with Hanging Chain (Exact Center at 182, 146) -->
      <circle cx="182" cy="146" r="14" fill="rgba(255,255,255,0.3)" stroke="url(#bGold)" stroke-width="3.5"/>
      <circle cx="182" cy="146" r="14" fill="none" stroke="#090a0f" stroke-width="1.5"/>
      <path d="M 196 146 Q 210 185 195 220" fill="none" stroke="url(#bGold)" stroke-width="2.5"/>

      <!-- Stiff Upper Lip Mustache -->
      <path d="M 136 172 Q 160 182 184 172" fill="none" stroke="#78350f" stroke-width="6.5" stroke-linecap="round"/>

      <!-- Strict British Eyebrows (FACE_CONFIG: Y in [124, 128]) -->
      <path d="M 124 128 Q 138 122 152 130" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
      <path d="M 168 130 Q 182 122 196 128" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
    </svg>
    """,

    # ================= 3. BEDOUIN PEARL DIVER (1930s) =================
    "pearl_diver": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
      <defs>
        <radialGradient id="dSkin" cx="45%" cy="40%" r="55%">
          <stop offset="0%" stop-color="#f5caa0"/>
          <stop offset="85%" stop-color="#d99360"/>
          <stop offset="100%" stop-color="#b87333"/>
        </radialGradient>
      </defs>

      <!-- Weathered Tan Torso -->
      <path d="M 100 190 C 90 180, 230 180, 220 190 L 210 350 C 190 360, 130 360, 110 350 Z"
            fill="#d99360" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Torso Cel Shadow Back Edge -->
      <path d="M 100 190 L 110 350 L 130 350 L 115 190 Z" fill="#b87333"/>

      <!-- Diver Cotton Vest Folds -->
      <path d="M 90 190 L 125 350 L 80 350 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="4.5" stroke-linejoin="round"/>
      <path d="M 230 190 L 195 350 L 240 350 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="4.5" stroke-linejoin="round"/>
      <!-- Vest Shadow Lines -->
      <line x1="95" y1="220" x2="115" y2="330" stroke="#cbd5e1" stroke-width="3.5"/>
      <line x1="225" y1="220" x2="205" y2="330" stroke="#cbd5e1" stroke-width="3.5"/>

      <!-- Traditional Pearl Diving Waistcloth (Izar) -->
      <path d="M 72 345 L 248 345 L 260 425 C 210 438, 110 438, 60 425 Z"
            fill="#1e293b" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="68" y="340" width="184" height="12" rx="4" fill="#f1f5f9" stroke="#090a0f" stroke-width="3.5"/>

      <!-- Diver Arms with Shell Knife & Rope Bracelet -->
      <path d="M 90 200 Q 40 260 70 330" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 90 200 Q 40 260 70 330" fill="none" stroke="#d99360" stroke-width="16" stroke-linecap="round"/>
      <path d="M 230 200 Q 280 260 250 330" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 230 200 Q 280 260 250 330" fill="none" stroke="#d99360" stroke-width="16" stroke-linecap="round"/>
      <circle cx="70" cy="335" r="13" fill="#d49360" stroke="#090a0f" stroke-width="4.5"/>
      <circle cx="250" cy="335" r="13" fill="#d49360" stroke="#090a0f" stroke-width="4.5"/>

      <!-- Diyyin: Woven String Neck Bag with Glistening Natural Pearl -->
      <path d="M 125 190 Q 160 260 195 190" fill="none" stroke="#78350f" stroke-width="4.5"/>
      <path d="M 135 240 C 135 295, 185 295, 185 240 Z" fill="#b45309" stroke="#090a0f" stroke-width="4" stroke-dasharray="4,4"/>
      <circle cx="160" cy="265" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="3"/>
      <circle cx="156" cy="261" r="4" fill="#fef08a"/>

      <!-- Head Base (Pill Shape) sitting directly on collar -->
      <path d="M 88 140 C 88 80, 232 80, 232 140 C 232 215, 88 215, 88 140 Z"
            fill="#f5caa0" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>

      <!-- Cel-Shaded Chin/Neck Shadow Path (Y in [198, 218]) -->
      <path d="M 105 198 Q 160 218 215 198 C 200 216, 120 216, 105 198 Z" fill="#b87333" opacity="0.6"/>

      <!-- Knotted Indigo Sea Bandana / Headscarf -->
      <path d="M 80 125 C 75 75, 245 75, 240 125 C 248 105, 240 75, 220 62 C 190 48, 130 48, 100 62 C 80 75, 72 105, 80 125 Z"
            fill="#1e1b4b" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
      <circle cx="82" cy="115" r="9" fill="#312e81" stroke="#090a0f" stroke-width="3.5"/>
      <!-- Shadow under Bandana -->
      <path d="M 86 115 Q 160 130 234 115 Q 160 102 86 115 Z" fill="#b87333" opacity="0.45"/>

      <!-- Fitam: Traditional Bone Nose Clip (Exact Coordinates: 160, 166, Y in [160, 172]) -->
      <path d="M 157 160 C 153 155, 167 155, 163 160 L 162 172 L 158 172 Z"
            fill="#fef08a" stroke="#090a0f" stroke-width="3"/>

      <!-- Sailor Eyebrows & Stubbled Chin (FACE_CONFIG: 160, 126) -->
      <path d="M 122 126 Q 138 118 152 126" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
      <path d="M 168 126 Q 182 118 198 126" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
      <path d="M 130 198 Q 160 212 190 198" fill="none" stroke="#44403c" stroke-width="3.5" stroke-dasharray="3,3"/>
    </svg>
    """,

    # ================= 4. JAPANESE INVENTOR KOKICHI MIKIMOTO =================
    "inventor_mikimoto": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
      <defs>
        <radialGradient id="pearlGlow" cx="35%" cy="35%" r="65%">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="60%" stop-color="#e0f2fe"/>
          <stop offset="100%" stop-color="#38bdf8"/>
        </radialGradient>
      </defs>

      <!-- 1920s Charcoal Vest & Slacks -->
      <path d="M 95 190 C 95 180, 225 180, 225 190 L 250 410 C 205 420, 115 420, 70 410 Z"
            fill="#334155" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Vest Shadow Path -->
      <path d="M 70 410 L 95 190 L 115 190 L 85 412 Z" fill="#1e293b"/>

      <!-- White Collared Shirt & Burgundy Bowtie -->
      <polygon points="140,185 160,230 180,185" fill="#f8fafc" stroke="#090a0f" stroke-width="3.5"/>
      <polygon points="148,190 160,200 172,190 172,204 160,195 148,204" fill="#991b1b" stroke="#090a0f" stroke-width="2.5"/>

      <!-- Vest Buttons -->
      <circle cx="160" cy="250" r="4.5" fill="#0f172a" stroke="#090a0f" stroke-width="2"/>
      <circle cx="160" cy="280" r="4.5" fill="#0f172a" stroke="#090a0f" stroke-width="2"/>
      <circle cx="160" cy="310" r="4.5" fill="#0f172a" stroke="#090a0f" stroke-width="2"/>

      <!-- Left Arm Extended Holding Giant Shimmering Cultured Pearl -->
      <path d="M 95 200 Q 50 250 75 320" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 95 200 Q 50 250 75 320" fill="none" stroke="#334155" stroke-width="16" stroke-linecap="round"/>
      <path d="M 225 200 Q 285 240 260 290" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 225 200 Q 285 240 260 290" fill="none" stroke="#334155" stroke-width="16" stroke-linecap="round"/>
      <circle cx="75" cy="325" r="12" fill="#fae3c6" stroke="#090a0f" stroke-width="3.5"/>
      <circle cx="260" cy="285" r="12" fill="#fae3c6" stroke="#090a0f" stroke-width="3.5"/>

      <!-- Giant Cultured Pearl with Sparkle Rays -->
      <g transform="translate(265, 235)">
        <circle cx="0" cy="0" r="28" fill="url(#pearlGlow)" stroke="#090a0f" stroke-width="4.5"/>
        <circle cx="-8" cy="-8" r="7" fill="#ffffff"/>
        <path d="M 0 -36 L 0 -44 M 0 36 L 0 44 M -36 0 L -44 0 M 36 0 L 44 0" stroke="#fde047" stroke-width="4" stroke-linecap="round"/>
        <path d="M -24 -24 L -30 -30 M 24 24 L 30 30 M 24 -24 L 30 -30 M -24 24 L -30 30" stroke="#fde047" stroke-width="3.5" stroke-linecap="round"/>
      </g>

      <!-- Head Base (Pill Shape) sitting directly on collar -->
      <path d="M 90 145 C 90 85, 230 85, 230 145 C 230 215, 90 215, 90 145 Z"
            fill="#fff5eb" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>

      <!-- Cel-Shaded Chin Shadow (Y in [198, 218]) -->
      <path d="M 110 198 Q 160 218 210 198 C 200 216, 120 216, 110 198 Z" fill="#e8be99"/>

      <!-- 1920s Side-Parted Black Hair -->
      <path d="M 85 130 C 80 75, 240 75, 235 130 C 235 100, 220 85, 180 85 C 140 85, 95 100, 85 130 Z"
            fill="#1e293b" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
      <path d="M 120 90 Q 150 100 180 90" fill="none" stroke="#0f172a" stroke-width="4"/>
      <!-- Shadow under Hair onto Forehead -->
      <path d="M 90 115 Q 160 128 230 115 Q 160 105 90 115 Z" fill="#fae3c6" opacity="0.6"/>

      <!-- Round Wireframe Spectacles (Exact Alignment: Centers at 138, 146 and 182, 146) -->
      <circle cx="138" cy="146" r="16" fill="rgba(255,255,255,0.35)" stroke="#090a0f" stroke-width="3.5"/>
      <circle cx="182" cy="146" r="16" fill="rgba(255,255,255,0.35)" stroke="#090a0f" stroke-width="3.5"/>
      <line x1="154" y1="146" x2="166" y2="146" stroke="#090a0f" stroke-width="3.5"/>
      <line x1="122" y1="144" x2="100" y2="138" stroke="#090a0f" stroke-width="3.5"/>
      <line x1="198" y1="144" x2="220" y2="138" stroke="#090a0f" stroke-width="3.5"/>

      <!-- Polite Japanese Mustache & Eyebrows (FACE_CONFIG: Y in [124, 128]) -->
      <path d="M 144 172 Q 160 166 176 172" fill="none" stroke="#090a0f" stroke-width="5" stroke-linecap="round"/>
      <path d="M 124 126 Q 138 120 150 126" fill="none" stroke="#090a0f" stroke-width="5" stroke-linecap="round"/>
      <path d="M 170 126 Q 182 120 196 126" fill="none" stroke="#090a0f" stroke-width="5" stroke-linecap="round"/>
    </svg>
    """,

    # ================= 5. SHEIKH RASHID OF DUBAI =================
    "sheikh_rashid": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
      <defs>
        <linearGradient id="rBisht" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#3d2817"/>
          <stop offset="50%" stop-color="#543820"/>
          <stop offset="100%" stop-color="#301f11"/>
        </linearGradient>
      </defs>

      <!-- Ghutra Back Layer -->
      <path d="M 60 140 C 45 60, 275 60, 260 140 C 285 220, 290 320, 275 380 C 255 350, 235 250, 220 200 C 190 190, 130 190, 100 200 C 85 250, 65 350, 45 380 C 30 320, 35 220, 60 140 Z"
            fill="#f1f5f9" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M 45 380 C 30 320, 35 220, 60 140 C 55 180, 52 280, 68 340 Z" fill="#cbd5e1"/>
      <path d="M 275 380 C 290 320, 285 220, 260 140 C 265 180, 268 280, 252 340 Z" fill="#cbd5e1"/>

      <!-- White Kandura & Dark Brown Bisht -->
      <path d="M 95 190 C 95 180, 225 180, 225 190 L 255 420 C 205 432, 115 432, 65 420 Z"
            fill="#ffffff" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
      <path d="M 80 185 C 80 170, 240 170, 240 185 L 265 425 C 215 435, 105 435, 55 425 Z"
            fill="url(#rBisht)" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Bisht Outer Dark Crease AO Path -->
      <path d="M 55 425 L 80 185 L 105 185 L 75 427 Z" fill="#1f140a"/>
      <path d="M 265 425 L 240 185 L 220 185 L 248 427 Z" fill="#1f140a"/>

      <!-- Bisht Gold Trim -->
      <path d="M 125 185 L 160 300 L 195 185" fill="none" stroke="#eab308" stroke-width="9" stroke-linecap="round"/>
      <path d="M 160 300 L 160 430" fill="none" stroke="#eab308" stroke-width="6.5" stroke-linecap="round"/>

      <!-- Right Hand Holding Blue Architectural Blueprint of Port Rashid -->
      <path d="M 80 200 Q 30 260 65 330" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 80 200 Q 30 260 65 330" fill="none" stroke="url(#rBisht)" stroke-width="16" stroke-linecap="round"/>
      <path d="M 240 200 Q 290 260 255 330" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
      <path d="M 240 200 Q 290 260 255 330" fill="none" stroke="url(#rBisht)" stroke-width="16" stroke-linecap="round"/>
      <circle cx="68" cy="335" r="14" fill="#fae3cb" stroke="#090a0f" stroke-width="4.5"/>
      <circle cx="252" cy="335" r="14" fill="#fae3cb" stroke="#090a0f" stroke-width="4.5"/>
      <rect x="235" y="300" width="40" height="15" rx="3" transform="rotate(-25 235 300)" fill="#0284c7" stroke="#090a0f" stroke-width="3"/>

      <!-- Head Base (Pill Shape) sitting directly on collar -->
      <path d="M 85 140 C 85 80, 235 80, 235 140 C 235 220, 85 220, 85 140 Z"
            fill="#fae3cb" stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>

      <!-- Cel-Shaded Chin Ambient Occlusion Path (Y in [198, 218]) -->
      <path d="M 105 198 Q 160 218 215 198 C 205 220, 115 220, 105 198 Z" fill="#d49c6e"/>

      <!-- White Ghutra Framing Drapes -->
      <path d="M 90 95 C 70 120, 55 180, 68 310 C 80 290, 88 230, 96 170 C 92 135, 88 115, 90 95 Z"
            fill="#ffffff" stroke="#090a0f" stroke-width="5" stroke-linejoin="round"/>
      <path d="M 230 95 C 250 120, 265 180, 252 310 C 240 290, 232 230, 224 170 C 228 135, 232 115, 230 95 Z"
            fill="#ffffff" stroke="#090a0f" stroke-width="5" stroke-linejoin="round"/>
      <path d="M 85 105 Q 160 70 235 105 Q 160 90 85 105 Z" fill="#ffffff" stroke="#090a0f" stroke-width="5"/>
      <!-- Shadow under Ghutra Brim -->
      <path d="M 92 108 Q 160 120 228 108 Q 160 100 92 108 Z" fill="#e2ba94" opacity="0.75"/>

      <!-- Black Agal Dual Rings -->
      <ellipse cx="160" cy="92" rx="72" ry="16" fill="none" stroke="#090a0f" stroke-width="14"/>
      <ellipse cx="160" cy="92" rx="72" ry="16" fill="none" stroke="#27272a" stroke-width="8"/>
      <ellipse cx="160" cy="104" rx="68" ry="15" fill="none" stroke="#090a0f" stroke-width="13"/>
      <ellipse cx="160" cy="104" rx="68" ry="15" fill="none" stroke="#27272a" stroke-width="7"/>

      <!-- Cheeks Subtle Warmth -->
      <ellipse cx="118" cy="160" rx="10" ry="5" fill="#f87171" opacity="0.32"/>
      <ellipse cx="202" cy="160" rx="10" ry="5" fill="#f87171" opacity="0.32"/>

      <!-- Charismatic Sharp Arabian Beard & Eyebrows (FACE_CONFIG: 160, 126) -->
      <path d="M 125 180 Q 160 215 195 180 Q 180 208 160 215 Q 140 208 125 180 Z"
            fill="#1c1917" stroke="#090a0f" stroke-width="4.5" stroke-linejoin="round"/>
      <path d="M 135 170 Q 160 182 185 170" fill="none" stroke="#1c1917" stroke-width="7.5" stroke-linecap="round"/>
      <path d="M 122 126 Q 138 118 152 126" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
      <path d="M 168 126 Q 182 118 198 126" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
    </svg>
    """,

    # ================= 6. ROBOT MINISTER OF AI (MODERN/FUTURE) =================
    "robot_minister": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
      <defs>
        <linearGradient id="botChassis" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#cbd5e1"/>
          <stop offset="50%" stop-color="#f8fafc"/>
          <stop offset="100%" stop-color="#94a3b8"/>
        </linearGradient>
      </defs>

      <!-- Sleek Cyber Pod Chassis Base -->
      <path d="M 95 190 C 85 180, 235 180, 225 190 L 255 410 C 210 425, 110 425, 65 410 Z"
            fill="url(#botChassis)" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
      <!-- Chassis Shadow Path -->
      <path d="M 65 410 L 95 190 L 115 190 L 85 412 Z" fill="#64748b"/>

      <!-- Glowing Cyan Circuit Traces -->
      <path d="M 160 210 L 160 410" stroke="#0ea5e9" stroke-width="4.5"/>
      <path d="M 110 280 L 210 280" stroke="#0ea5e9" stroke-width="3.5"/>
      <circle cx="160" cy="280" r="6" fill="#38bdf8"/>
      <circle cx="110" cy="280" r="4" fill="#38bdf8"/>
      <circle cx="210" cy="280" r="4" fill="#38bdf8"/>

      <!-- Official UAE AI Ministry Gold Badge -->
      <rect x="135" y="225" width="50" height="22" rx="4" fill="#fbbf24" stroke="#090a0f" stroke-width="3"/>
      <text x="142" y="240" font-family="Arial, sans-serif" font-weight="900" font-size="10" fill="#0f172a">AI • UAE</text>

      <!-- Mechanical Arms -->
      <path d="M 85 200 Q 50 260 75 320" fill="none" stroke="#090a0f" stroke-width="20" stroke-linecap="round"/>
      <path d="M 85 200 Q 50 260 75 320" fill="none" stroke="#64748b" stroke-width="14" stroke-linecap="round"/>
      <path d="M 235 200 Q 270 260 245 320" fill="none" stroke="#090a0f" stroke-width="20" stroke-linecap="round"/>
      <path d="M 235 200 Q 270 260 245 320" fill="none" stroke="#64748b" stroke-width="14" stroke-linecap="round"/>
      <circle cx="75" cy="325" r="10" fill="#0284c7" stroke="#090a0f" stroke-width="3.5"/>
      <circle cx="245" cy="325" r="10" fill="#0284c7" stroke="#090a0f" stroke-width="3.5"/>

      <!-- Robot Head Chassis -->
      <rect x="90" y="95" width="140" height="95" rx="35" fill="url(#botChassis)" stroke="#090a0f" stroke-width="6.5"/>
      <!-- Shadow under chin plate -->
      <path d="M 105 185 L 215 185 L 205 195 L 115 195 Z" fill="#64748b"/>

      <!-- Cyber Antenna on Top with Pulsing Cyan Orb -->
      <line x1="160" y1="95" x2="160" y2="60" stroke="#090a0f" stroke-width="5"/>
      <circle cx="160" cy="55" r="8" fill="#00f2fe" stroke="#090a0f" stroke-width="3.5"/>

      <!-- Electronic Dark Glass Visor Screen -->
      <rect x="106" y="112" width="108" height="60" rx="20" fill="#090d16" stroke="#090a0f" stroke-width="4"/>

      <!-- Glowing Cyan Digital LED Eyes (Built Into Visor) -->
      <ellipse cx="138" cy="142" rx="14" ry="10" fill="#00f2fe"/>
      <ellipse cx="182" cy="142" rx="14" ry="10" fill="#00f2fe"/>
      <circle cx="140" cy="142" r="5" fill="#0284c7"/>
      <circle cx="184" cy="142" r="5" fill="#0284c7"/>
      <circle cx="137" cy="139" r="2.5" fill="#ffffff"/>
      <circle cx="181" cy="139" r="2.5" fill="#ffffff"/>
    </svg>
    """,

    # ================= 7. DR. OTTO HAHN (ACTIVE: POINTING UP TO BOARD) =================
    "dr_otto_hahn": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
      <defs>
        <radialGradient id="hahnGlow" cx="80%" cy="30%" r="50%">
          <stop offset="0%" stop-color="#fef08a" stop-opacity="0.8"/>
          <stop offset="100%" stop-color="#eab308" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <!-- Floor Shadow -->
      <ellipse cx="160" cy="425" rx="85" ry="18" fill="#020305" opacity="0.75"/>
      <!-- Legs in Dark Trousers -->
      <line x1="135" y1="360" x2="135" y2="420" stroke="#090a0f" stroke-width="14" stroke-linecap="round"/>
      <line x1="185" y1="360" x2="185" y2="420" stroke="#090a0f" stroke-width="14" stroke-linecap="round"/>
      <ellipse cx="130" cy="422" rx="20" ry="10" fill="#090b10" stroke="#090a0f" stroke-width="4"/>
      <ellipse cx="190" cy="422" rx="20" ry="10" fill="#090b10" stroke="#090a0f" stroke-width="4"/>
      <!-- White Laboratory Coat -->
      <path d="M 100 195 C 90 260 90 320 110 370 L 210 370 C 230 320 230 260 220 195 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="8" stroke-linejoin="round"/>
      <path d="M 130 195 L 160 270 L 190 195 Z" fill="#1e293b" stroke="#090a0f" stroke-width="4"/>
      <line x1="160" y1="270" x2="160" y2="370" stroke="#090a0f" stroke-width="4"/>
      <!-- Right Amber Motivated Rim Light from Lab Lamp -->
      <path d="M 215 210 L 225 365" stroke="#fbbf24" stroke-width="6" stroke-linecap="round" opacity="0.85"/>
      <!-- Left Arm: Resting at Hip -->
      <path d="M 110 240 Q 75 280 100 320" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>
      <circle cx="102" cy="324" r="13" fill="#fae3cb" stroke="#090a0f" stroke-width="4.5"/>
      <!-- Right Arm: Pointing Up to Board (pose="pointing_up_board") -->
      <path d="M 205 260 C 245 230 265 180 285 135" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>
      <circle cx="286" cy="132" r="13" fill="#fae3cb" stroke="#090a0f" stroke-width="4.5"/>
      <!-- Chalk Stick in Hand -->
      <rect x="282" y="98" width="8" height="34" rx="2" fill="#fef08a" stroke="#090a0f" stroke-width="2.5" transform="rotate(22 286 115)"/>
      <!-- Head Base & Warm Motivated Rim Arc -->
      <circle cx="160" cy="144" r="64" fill="#fae3cb" stroke="#090a0f" stroke-width="8"/>
      <path d="M 195 88 A 64 64 0 0 1 198 208 A 54 64 0 0 0 195 88 Z" fill="#fbbf24" opacity="0.6"/>
      <!-- 1930s Receding Dark Hair -->
      <path d="M 100 135 C 95 80 225 80 220 135 C 220 100 205 90 160 90 C 115 90 100 100 100 135 Z" fill="#292524" stroke="#090a0f" stroke-width="6"/>
      <!-- Wire Spectacles on Eyes -->
      <circle cx="138" cy="144" r="16" fill="rgba(255,255,255,0.4)" stroke="#090a0f" stroke-width="4"/>
      <circle cx="182" cy="144" r="16" fill="rgba(255,255,255,0.4)" stroke="#090a0f" stroke-width="4"/>
      <line x1="154" y1="144" x2="166" y2="144" stroke="#090a0f" stroke-width="4"/>
      <circle cx="138" cy="144" r="5" fill="#090a0f"/>
      <circle cx="182" cy="144" r="5" fill="#090a0f"/>
      <!-- Serious German Mustache & Eyebrows -->
      <path d="M 136 172 Q 160 180 184 172" fill="none" stroke="#292524" stroke-width="6.5" stroke-linecap="round"/>
      <line x1="144" y1="188" x2="176" y2="188" stroke="#090a0f" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M 124 124 Q 138 116 150 124" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
      <path d="M 170 124 Q 182 116 196 124" fill="none" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round"/>
    </svg>
    """,

    # ================= 8. FRITZ STRASSMANN (REACTIVE: HEAD CLUTCH PANIC) =================
    "fritz_strassmann": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 440" width="320" height="440">
      <defs>
        <radialGradient id="strassMoon" cx="20%" cy="30%" r="50%">
          <stop offset="0%" stop-color="#93c5fd" stop-opacity="0.8"/>
          <stop offset="100%" stop-color="#3b82f6" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <!-- Floor Shadow -->
      <ellipse cx="160" cy="425" rx="85" ry="18" fill="#020305" opacity="0.75"/>
      <!-- Legs in Grey Trousers -->
      <line x1="135" y1="360" x2="135" y2="420" stroke="#090a0f" stroke-width="14" stroke-linecap="round"/>
      <line x1="185" y1="360" x2="185" y2="420" stroke="#090a0f" stroke-width="14" stroke-linecap="round"/>
      <ellipse cx="130" cy="422" rx="20" ry="10" fill="#090b10" stroke="#090a0f" stroke-width="4"/>
      <ellipse cx="190" cy="422" rx="20" ry="10" fill="#090b10" stroke="#090a0f" stroke-width="4"/>
      <!-- White Laboratory Coat -->
      <path d="M 100 195 C 90 260 90 320 110 370 L 210 370 C 230 320 230 260 220 195 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="8" stroke-linejoin="round"/>
      <path d="M 130 195 L 160 265 L 190 195 Z" fill="#78350f" stroke="#090a0f" stroke-width="4"/>
      <line x1="160" y1="265" x2="160" y2="370" stroke="#090a0f" stroke-width="4"/>
      <!-- Cold Moonlit Rim Light from Window on Right -->
      <path d="M 215 210 L 225 365" stroke="#60a5fa" stroke-width="6" stroke-linecap="round" opacity="0.85"/>
      <!-- Both Arms Gripping Head in Disbelief (pose="head_clutch_panic") -->
      <path d="M 115 260 C 75 220 80 150 110 125" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>
      <circle cx="110" cy="122" r="13" fill="#fae3cb" stroke="#090a0f" stroke-width="4.5"/>
      <path d="M 205 260 C 245 220 240 150 210 125" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>
      <circle cx="210" cy="122" r="13" fill="#fae3cb" stroke="#090a0f" stroke-width="4.5"/>
      <!-- Head Base & Cold Window Rim Arc -->
      <circle cx="160" cy="144" r="64" fill="#fae3cb" stroke="#090a0f" stroke-width="8"/>
      <path d="M 195 88 A 64 64 0 0 1 198 208 A 54 64 0 0 0 195 88 Z" fill="#60a5fa" opacity="0.6"/>
      <!-- Brown Parted Hair -->
      <path d="M 98 128 C 95 82 225 82 222 128 C 215 95 185 88 160 88 C 135 88 105 95 98 128 Z" fill="#44403c" stroke="#090a0f" stroke-width="6"/>
      <!-- Wide Shocked Eyes & Sweat Drop -->
      <ellipse cx="138" cy="144" rx="14" ry="17" fill="#ffffff" stroke="#090a0f" stroke-width="5"/>
      <circle cx="136" cy="144" r="5.5" fill="#090a0f"/>
      <ellipse cx="182" cy="144" rx="14" ry="17" fill="#ffffff" stroke="#090a0f" stroke-width="5"/>
      <circle cx="180" cy="144" r="5.5" fill="#090a0f"/>
      <!-- Disbelief Furrowed Eyebrows -->
      <path d="M 122 122 Q 138 108 152 124" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round" fill="none"/>
      <path d="M 168 124 Q 182 108 198 122" stroke="#090a0f" stroke-width="5.5" stroke-linecap="round" fill="none"/>
      <!-- Wide Gaping Mouth -->
      <ellipse cx="160" cy="186" rx="12" ry="15" fill="#090a0f"/>
      <!-- Blue Sweat Bead -->
      <path d="M 205 130 C 212 142 212 152 205 156 C 198 152 198 142 205 130 Z" fill="#38bdf8" stroke="#090a0f" stroke-width="3"/>
    </svg>
    """
}


def render_svg_1to1_png(svg_content, out_png, width=320, height=440):
    """Renders SVG to transparent high-res PNG at exact 1:1 dimensions without bounding box shift."""
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: {width}px; height: {height}px;
    background: transparent !important;
    overflow: hidden;
  }}
  svg {{ width: {width}px; height: {height}px; display: block; }}
</style>
</head>
<body>{svg_content}</body>
</html>"""

    temp_html = os.path.abspath("temp_rig_1to1.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html)

    abs_out = os.path.abspath(out_png)
    html_url = "file:///" + temp_html.replace("\\", "/")
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        f"--screenshot={abs_out}",
        f"--window-size={width},{height}",
        html_url
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_html):
        os.remove(temp_html)

    return abs_out


def build_all_unified_rigs(target_dir=None):
    dst_dir = target_dir if target_dir else SPRITES_DIR
    os.makedirs(dst_dir, exist_ok=True)
    print(f"🎨 Generating Exact 1:1 Graphic-Novel Vector Character Rigs in {dst_dir}...")
    generated = {}
    for name, svg in CHARACTER_RIGS.items():
        out_png = os.path.join(dst_dir, f"{name}.png")
        p = render_svg_1to1_png(svg, out_png, width=320, height=440)
        im = Image.open(p)
        generated[name] = im
        print(f"  ✨ Graphic-Novel Rig Rendered: {name}.png ({im.width}x{im.height})")
    print(f"✅ All {len(generated)} Unified Rigs Successfully Created!")
    return generated


if __name__ == "__main__":
    build_all_unified_rigs()
