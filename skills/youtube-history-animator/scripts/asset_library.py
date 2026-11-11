"""
engine_2d/asset_library.py
High-Fidelity Vector Sprite & Asset Synthesis Library for OverSimplified 2D Animations.
Generates broadcast-quality SVG vector definitions and rasterizes them into ultra-sharp
transparent RGBA PNGs using Chrome headless or pure Pillow vector rasterization.
"""

import os
import sys
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SPRITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
os.makedirs(SPRITES_DIR, exist_ok=True)

HIGH_FIDELITY_SVGS = {
    # ================= SHEIKH ZAYED V2 =================
    "sheikh_zayed_head": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 400" width="380" height="400">
      <defs>
        <radialGradient id="skinG" cx="45%" cy="40%" r="55%">
          <stop offset="0%" stop-color="#f8d8b8"/>
          <stop offset="80%" stop-color="#e8b88d"/>
          <stop offset="100%" stop-color="#d49c6e"/>
        </radialGradient>
        <filter id="dropShadow" x="-10%" y="-10%" width="130%" height="130%">
          <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#000" flood-opacity="0.3"/>
        </filter>
      </defs>
      <!-- Flowing White Ghutra (Headdress) with realistic layered folds -->
      <path d="M 40 160 C 30 70, 310 70, 300 160 C 330 250, 325 350, 310 390 C 285 365, 260 270, 245 220 C 220 200, 120 200, 95 220 C 80 270, 55 365, 30 390 C 15 350, 10 250, 40 160 Z" 
            fill="#ffffff" stroke="#18181b" stroke-width="7" stroke-linejoin="round" filter="url(#dropShadow)" />
      <!-- Ghutra inner fabric shade line -->
      <path d="M 70 190 Q 95 270 80 340" fill="none" stroke="#e2e8f0" stroke-width="5" stroke-linecap="round"/>
      <path d="M 270 190 Q 245 270 260 340" fill="none" stroke="#e2e8f0" stroke-width="5" stroke-linecap="round"/>
      
      <!-- Agal (Dual Corded Black Rings with braided gold thread) -->
      <ellipse cx="170" cy="115" rx="84" ry="20" fill="none" stroke="#09090b" stroke-width="15" />
      <ellipse cx="170" cy="115" rx="84" ry="20" fill="none" stroke="#27272a" stroke-width="9" />
      <ellipse cx="170" cy="130" rx="80" ry="18" fill="none" stroke="#09090b" stroke-width="13" />
      <ellipse cx="170" cy="130" rx="80" ry="18" fill="none" stroke="#27272a" stroke-width="7" />
      <!-- Golden agal tassels -->
      <path d="M 245 130 Q 260 170 255 220" fill="none" stroke="#eab308" stroke-width="4" stroke-linecap="round"/>

      <!-- OverSimplified Face Base -->
      <path d="M 95 160 C 95 110, 245 110, 245 160 C 245 235, 95 235, 95 160 Z" fill="url(#skinG)" stroke="#18181b" stroke-width="7" />

      <!-- Cheeks Blush -->
      <ellipse cx="120" cy="195" rx="14" ry="8" fill="#e07a5f" opacity="0.35"/>
      <ellipse cx="220" cy="195" rx="14" ry="8" fill="#e07a5f" opacity="0.35"/>

      <!-- Distinguished Royal Arabian Beard & Mustache -->
      <path d="M 115 210 Q 170 265 225 210 Q 210 255 170 265 Q 130 255 115 210 Z" fill="#262626" stroke="#18181b" stroke-width="5" stroke-linejoin="round" />
      <path d="M 130 195 Q 170 215 210 195" fill="none" stroke="#262626" stroke-width="9" stroke-linecap="round" />

      <!-- Wise Eyebrows -->
      <path d="M 115 142 Q 138 132 155 142" fill="none" stroke="#1c1917" stroke-width="7" stroke-linecap="round" />
      <path d="M 185 142 Q 202 132 225 142" fill="none" stroke="#1c1917" stroke-width="7" stroke-linecap="round" />
    </svg>
    """,

    "sheikh_zayed_body": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 520" width="440" height="520">
      <defs>
        <radialGradient id="bishtG" cx="40%" cy="30%" r="70%">
          <stop offset="0%" stop-color="#3b2d1f"/>
          <stop offset="100%" stop-color="#1f160e"/>
        </radialGradient>
      </defs>
      <!-- Pure White Crisp Kandura/Thobe -->
      <path d="M 120 110 C 120 100, 260 100, 260 110 L 290 470 C 240 480, 140 480, 90 470 Z" fill="#ffffff" stroke="#18181b" stroke-width="7" />
      
      <!-- Ceremonial Dark Charcoal/Gold-Brocade Royal Bisht -->
      <path d="M 95 110 C 95 90, 285 90, 285 110 L 320 480 C 260 495, 120 495, 60 480 Z" 
            fill="url(#bishtG)" stroke="#18181b" stroke-width="8" stroke-linejoin="round" />
      
      <!-- Elaborate Royal Zari Embroidery (Gold Leaf Trim) -->
      <path d="M 150 110 L 190 280 L 230 110" fill="none" stroke="#eab308" stroke-width="12" stroke-linecap="round" />
      <path d="M 190 280 L 190 485" fill="none" stroke="#eab308" stroke-width="10" />
      <!-- Gold braided frogging clasps -->
      <circle cx="190" cy="220" r="8" fill="#ca8a04" stroke="#18181b" stroke-width="3"/>
      <circle cx="190" cy="255" r="8" fill="#ca8a04" stroke="#18181b" stroke-width="3"/>

      <!-- Traditional Silver Khanjar Dagger at Belt -->
      <path d="M 170 300 C 180 325, 215 340, 230 330 C 220 315, 195 295, 170 300 Z" fill="#cbd5e1" stroke="#18181b" stroke-width="5"/>
      <rect x="160" y="292" width="22" height="12" rx="4" fill="#eab308" stroke="#18181b" stroke-width="3"/>

      <!-- Sleeves & Expressive Gesturing Hands -->
      <path d="M 95 130 Q 30 200 70 300 Q 110 300 120 250" fill="url(#bishtG)" stroke="#18181b" stroke-width="7" />
      <path d="M 285 130 Q 350 200 310 300 Q 270 300 260 250" fill="url(#bishtG)" stroke="#18181b" stroke-width="7" />
      <circle cx="78" cy="305" r="18" fill="#f8d8b8" stroke="#18181b" stroke-width="5" />
      <circle cx="302" cy="305" r="18" fill="#f8d8b8" stroke="#18181b" stroke-width="5" />
    </svg>
    """,

    # ================= BRITISH NAVY OFFICER V2 =================
    "british_officer_head": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 400" width="380" height="400">
      <!-- Victorian Naval Bicorne Hat with Gold Bullion & Cockade -->
      <path d="M 40 140 C 20 60, 320 60, 300 140 C 350 145, 360 110, 310 80 C 240 20, 100 20, 30 80 C -20 110, -10 145, 40 140 Z" 
            fill="#0f172a" stroke="#18181b" stroke-width="7" stroke-linejoin="round" />
      <path d="M 30 135 C 90 70, 250 70, 310 135 Z" fill="#0f172a" stroke="#18181b" stroke-width="6"/>
      <!-- Gold bullion braid border along hat -->
      <path d="M 35 130 Q 170 65 305 130" fill="none" stroke="#eab308" stroke-width="10" stroke-linecap="round"/>
      <!-- British Royal Navy Cockade (Red, White, Gold button) -->
      <circle cx="170" cy="85" r="22" fill="#dc2626" stroke="#18181b" stroke-width="4"/>
      <circle cx="170" cy="85" r="14" fill="#ffffff"/>
      <circle cx="170" cy="85" r="7" fill="#eab308" stroke="#18181b" stroke-width="2"/>

      <!-- OverSimplified Face -->
      <path d="M 100 135 C 100 100, 240 100, 240 135 C 240 215, 100 215, 100 135 Z" fill="#fde047" stroke="#18181b" stroke-width="7" />
      
      <!-- Victorian Sideburns / Muttonchops -->
      <path d="M 100 135 L 100 185 Q 115 190 120 170 Z" fill="#78350f" stroke="#18181b" stroke-width="4"/>
      <path d="M 240 135 L 240 185 Q 225 190 220 170 Z" fill="#78350f" stroke="#18181b" stroke-width="4"/>

      <!-- Aristocratic Monocle on Left Eye -->
      <circle cx="135" cy="155" r="22" fill="none" stroke="#eab308" stroke-width="5"/>
      <path d="M 155 165 Q 180 200 190 240" fill="none" stroke="#eab308" stroke-width="3"/>

      <!-- Stiff Upper Lip Mustache -->
      <path d="M 140 190 Q 170 180 200 190 Q 220 185 225 178 Q 200 205 170 200 Q 140 205 115 178 Q 120 185 140 190 Z" 
            fill="#78350f" stroke="#18181b" stroke-width="4"/>
    </svg>
    """,

    "british_officer_body": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 500" width="440" height="500">
      <!-- Deep Victorian Navy Blue Coat with Red Collar -->
      <path d="M 110 100 C 110 90, 250 90, 250 100 L 270 450 C 220 460, 140 460, 90 450 Z" 
            fill="#1e3a8a" stroke="#18181b" stroke-width="8" stroke-linejoin="round" />
      <!-- Red Lapels & White Cravat -->
      <path d="M 145 95 L 180 180 L 215 95 Z" fill="#ffffff" stroke="#18181b" stroke-width="4"/>
      <path d="M 145 95 L 125 210 L 180 210 Z" fill="#b91c1c" stroke="#18181b" stroke-width="5"/>
      <path d="M 215 95 L 235 210 L 180 210 Z" fill="#b91c1c" stroke="#18181b" stroke-width="5"/>

      <!-- Double-Breasted Brass Buttons -->
      <g fill="#eab308" stroke="#18181b" stroke-width="3">
        <circle cx="150" cy="235" r="7"/> <circle cx="210" cy="235" r="7"/>
        <circle cx="150" cy="275" r="7"/> <circle cx="210" cy="275" r="7"/>
        <circle cx="150" cy="315" r="7"/> <circle cx="210" cy="315" r="7"/>
        <circle cx="150" cy="355" r="7"/> <circle cx="210" cy="355" r="7"/>
      </g>

      <!-- Golden Epaulettes on Shoulders -->
      <ellipse cx="105" cy="110" rx="30" ry="16" fill="#eab308" stroke="#18181b" stroke-width="6"/>
      <ellipse cx="255" cy="110" rx="30" ry="16" fill="#eab308" stroke="#18181b" stroke-width="6"/>

      <!-- Holding Imperial Spyglass in Hand -->
      <path d="M 250 120 Q 320 180 280 270" fill="#1e3a8a" stroke="#18181b" stroke-width="7"/>
      <circle cx="280" cy="275" r="16" fill="#fde047" stroke="#18181b" stroke-width="4"/>
      <rect x="270" y="240" width="60" height="18" rx="4" transform="rotate(-30 270 240)" fill="#d97706" stroke="#18181b" stroke-width="4"/>
    </svg>
    """,

    # ================= BEDOUIN PEARL DIVER V2 =================
    "pearl_diver_head": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 380" width="360" height="380">
      <!-- Sunbaked Weathered Sailor Skin -->
      <path d="M 90 140 C 90 85, 230 85, 230 140 C 230 220, 90 220, 90 140 Z" fill="#c28854" stroke="#18181b" stroke-width="7" />
      <!-- Knotted Indigo Sea Bandana / Headscarf -->
      <path d="M 80 140 C 70 80, 250 80, 240 140 C 255 140, 255 110, 240 95 C 220 70, 100 70, 80 95 C 65 110, 65 140, 80 140 Z" 
            fill="#1e1b4b" stroke="#18181b" stroke-width="7" />
      <circle cx="75" cy="140" r="12" fill="#312e81" stroke="#18181b" stroke-width="4"/>

      <!-- Fitam (Turtle-shell Bone Nose Clip for deep-sea breath holding) -->
      <path d="M 152 165 C 145 155, 175 155, 168 165 L 163 182 L 157 182 Z" fill="#fef08a" stroke="#18181b" stroke-width="4"/>

      <!-- Sailor Eyebrows & Stubbled Beard -->
      <path d="M 110 135 Q 130 128 145 135" fill="none" stroke="#1c1917" stroke-width="7" stroke-linecap="round"/>
      <path d="M 175 135 Q 190 128 210 135" fill="none" stroke="#1c1917" stroke-width="7" stroke-linecap="round"/>
      <path d="M 120 195 Q 160 215 200 195" fill="none" stroke="#44403c" stroke-width="4" stroke-dasharray="3,3"/>
    </svg>
    """,

    "pearl_diver_body": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 500" width="420" height="500">
      <!-- Athletic Diver Torso with Rope Harness -->
      <path d="M 110 100 C 110 90, 230 90, 230 100 L 250 360 C 210 370, 130 370, 90 360 Z" fill="#c28854" stroke="#18181b" stroke-width="7" />
      <!-- Traditional Pearl Diving Waistcloth (Izar) -->
      <path d="M 85 350 L 255 350 L 270 480 C 220 495, 120 495, 70 480 Z" fill="#0f172a" stroke="#18181b" stroke-width="7" />
      <rect x="80" y="345" width="180" height="15" rx="4" fill="#cbd5e1" stroke="#18181b" stroke-width="4"/>

      <!-- Diyyin (Woven String Neck Bag for Collected Oysters) -->
      <path d="M 130 105 Q 170 220 210 105" fill="none" stroke="#78350f" stroke-width="5"/>
      <path d="M 140 180 C 140 260, 200 260, 200 180 Z" fill="#a16207" stroke="#18181b" stroke-width="5" stroke-dasharray="4,4"/>
      <!-- Glistening Pearl Inside Bag -->
      <circle cx="170" cy="210" r="14" fill="#ffffff" stroke="#18181b" stroke-width="3"/>
      <circle cx="166" cy="206" r="4" fill="#fef08a"/>
    </svg>
    """,

    # ================= PROPS & HISTORICAL ELEMENTS =================
    "eyes_angry": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 80" width="160" height="80">
      <ellipse cx="45" cy="45" rx="20" ry="24" fill="#ffffff" stroke="#18181b" stroke-width="5"/>
      <circle cx="50" cy="45" r="9" fill="#dc2626"/>
      <ellipse cx="115" cy="45" rx="20" ry="24" fill="#ffffff" stroke="#18181b" stroke-width="5"/>
      <circle cx="110" cy="45" r="9" fill="#dc2626"/>
      <!-- Angry sharp V-eyebrows -->
      <polygon points="15,20 70,45 68,36 20,12" fill="#18181b"/>
      <polygon points="145,20 90,45 92,36 140,12" fill="#18181b"/>
    </svg>
    """,

    "treaty_scroll": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 320" width="240" height="320">
      <defs>
        <radialGradient id="parchmentG" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#fef9c3"/>
          <stop offset="100%" stop-color="#fde047"/>
        </radialGradient>
      </defs>
      <!-- Rolled Parchment Scroll -->
      <path d="M 30 30 C 50 10, 190 10, 210 30 L 200 290 C 180 310, 40 310, 20 290 Z" 
            fill="#fef08a" stroke="#854d0e" stroke-width="6" stroke-linejoin="round"/>
      <!-- Text lines -->
      <g stroke="#713f12" stroke-width="4" stroke-linecap="round">
        <line x1="50" y1="70" x2="180" y2="70"/>
        <line x1="50" y1="105" x2="170" y2="105"/>
        <line x1="50" y1="140" x2="185" y2="140"/>
        <line x1="50" y1="175" x2="160" y2="175"/>
        <line x1="50" y1="210" x2="175" y2="210"/>
      </g>
      <!-- Royal Red Wax Seal -->
      <circle cx="115" cy="260" r="28" fill="#dc2626" stroke="#991b1b" stroke-width="5"/>
      <circle cx="115" cy="260" r="18" fill="none" stroke="#fef2f2" stroke-width="2"/>
      <!-- Red ribbon hanging -->
      <polygon points="108,280 100,310 115,302 130,310 122,280" fill="#dc2626"/>
    </svg>
    """,

    "oil_derrick_monumental": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 700" width="500" height="700">
      <defs>
        <linearGradient id="steelG" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#334155"/>
          <stop offset="50%" stop-color="#64748b"/>
          <stop offset="100%" stop-color="#1e293b"/>
        </linearGradient>
      </defs>
      <!-- Base Steel Platform -->
      <rect x="50" y="650" width="400" height="40" rx="8" fill="#1e293b" stroke="#0f172a" stroke-width="8"/>
      <!-- Main Tapered Derrick Tower Truss -->
      <polygon points="190,80 310,80 410,650 90,650" fill="none" stroke="url(#steelG)" stroke-width="14" stroke-linejoin="round"/>
      <!-- Horizontal Crossbeams -->
      <line x1="175" y1="180" x2="325" y2="180" stroke="#475569" stroke-width="10"/>
      <line x1="150" y1="310" x2="350" y2="310" stroke="#475569" stroke-width="10"/>
      <line x1="125" y1="450" x2="375" y2="450" stroke="#475569" stroke-width="10"/>
      <line x1="105" y1="570" x2="395" y2="570" stroke="#475569" stroke-width="10"/>
      <!-- Diagonal X-Braces -->
      <line x1="190" y1="80" x2="325" y2="180" stroke="#475569" stroke-width="7"/>
      <line x1="310" y1="80" x2="175" y2="180" stroke="#475569" stroke-width="7"/>
      <line x1="175" y1="180" x2="350" y2="310" stroke="#475569" stroke-width="8"/>
      <line x1="325" y1="180" x2="150" y2="310" stroke="#475569" stroke-width="8"/>
      <line x1="150" y1="310" x2="375" y2="450" stroke="#475569" stroke-width="8"/>
      <line x1="350" y1="310" x2="125" y2="450" stroke="#475569" stroke-width="8"/>
      <line x1="125" y1="450" x2="395" y2="570" stroke="#475569" stroke-width="9"/>
      <line x1="375" y1="450" x2="105" y2="570" stroke="#475569" stroke-width="9"/>
      <!-- Crown Block Pulley at Top -->
      <rect x="210" y="45" width="80" height="35" rx="6" fill="#eab308" stroke="#18181b" stroke-width="6"/>
      <!-- Crown Flare Burner -->
      <polygon points="250,5 230,45 270,45" fill="#f97316" stroke="#ea580c" stroke-width="4"/>
    </svg>
    """,

    "burj_khalifa_tower": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 900" width="350" height="900">
      <defs>
        <linearGradient id="glassG" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#bae6fd"/>
          <stop offset="40%" stop-color="#f0f9ff"/>
          <stop offset="60%" stop-color="#38bdf8"/>
          <stop offset="100%" stop-color="#0284c7"/>
        </linearGradient>
      </defs>
      <!-- Base Tier 1 -->
      <polygon points="120,680 230,680 260,890 90,890" fill="url(#glassG)" stroke="#0369a1" stroke-width="5"/>
      <!-- Tier 2 -->
      <polygon points="130,500 220,500 230,680 120,680" fill="url(#glassG)" stroke="#0369a1" stroke-width="5"/>
      <!-- Tier 3 -->
      <polygon points="140,340 210,340 220,500 130,500" fill="url(#glassG)" stroke="#0369a1" stroke-width="4"/>
      <!-- Tier 4 -->
      <polygon points="150,210 200,210 210,340 140,340" fill="url(#glassG)" stroke="#0369a1" stroke-width="4"/>
      <!-- Spire -->
      <polygon points="172,40 178,40 185,210 165,210" fill="#e2e8f0" stroke="#0284c7" stroke-width="3"/>
      <!-- Pinnacle Beacon -->
      <circle cx="175" cy="35" r="8" fill="#ef4444" stroke="#ffffff" stroke-width="3"/>
      <!-- Horizontal floor division stripes -->
      <g stroke="#ffffff" stroke-width="2" opacity="0.6">
        <line x1="125" y1="750" x2="225" y2="750"/>
        <line x1="135" y1="580" x2="215" y2="580"/>
        <line x1="145" y1="420" x2="205" y2="420"/>
        <line x1="155" y1="280" x2="195" y2="280"/>
      </g>
    </svg>
    """,

    "mars_hope_orbiter": """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 360" width="500" height="360">
      <defs>
        <linearGradient id="goldFoil" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#fef08a"/>
          <stop offset="40%" stop-color="#eab308"/>
          <stop offset="100%" stop-color="#854d0e"/>
        </linearGradient>
      </defs>
      <!-- Left Solar Array Wing -->
      <rect x="30" y="130" width="130" height="70" rx="4" fill="#1e3a8a" stroke="#60a5fa" stroke-width="5"/>
      <line x1="75" y1="130" x2="75" y2="200" stroke="#93c5fd" stroke-width="3"/>
      <line x1="120" y1="130" x2="120" y2="200" stroke="#93c5fd" stroke-width="3"/>
      <line x1="30" y1="165" x2="160" y2="165" stroke="#93c5fd" stroke-width="3"/>

      <!-- Right Solar Array Wing -->
      <rect x="340" y="130" width="130" height="70" rx="4" fill="#1e3a8a" stroke="#60a5fa" stroke-width="5"/>
      <line x1="385" y1="130" x2="385" y2="200" stroke="#93c5fd" stroke-width="3"/>
      <line x1="430" y1="130" x2="430" y2="200" stroke="#93c5fd" stroke-width="3"/>
      <line x1="340" y1="165" x2="470" y2="165" stroke="#93c5fd" stroke-width="3"/>

      <!-- Hexagonal Satellite Body with Golden Thermal Insulation Foil -->
      <polygon points="210,100 290,100 330,165 290,230 210,230 170,165" 
               fill="url(#goldFoil)" stroke="#713f12" stroke-width="6"/>
      
      <!-- High-Gain Dish Antenna -->
      <ellipse cx="250" cy="70" rx="45" ry="18" fill="#e2e8f0" stroke="#475569" stroke-width="5"/>
      <line x1="250" y1="70" x2="250" y2="100" stroke="#475569" stroke-width="6"/>
      <circle cx="250" cy="55" r="5" fill="#ef4444"/>

      <!-- UAE National Flag & Emirates Mars Mission Badge -->
      <rect x="235" y="150" width="30" height="18" fill="#22c55e" stroke="#18181b" stroke-width="1.5"/>
      <rect x="235" y="156" width="30" height="6" fill="#ffffff"/>
      <rect x="235" y="162" width="30" height="6" fill="#000000"/>
      <rect x="235" y="150" width="8" height="18" fill="#ef4444"/>
    </svg>
    """
}


class HighFidelityAssetManager:
    """Manages compilation, rasterization, and caching of high-resolution 2D animation assets."""
    def __init__(self, sprites_dir=SPRITES_DIR):
        self.sprites_dir = sprites_dir
        self.cached_images = {}
        self.compile_all()

    def compile_all(self):
        """Rasterizes SVGs into transparent PNGs using headless Chrome."""
        print("🎨 Rasterizing High-Fidelity Vector Sprite Assets...")
        for name, svg_code in HIGH_FIDELITY_SVGS.items():
            out_png = os.path.join(self.sprites_dir, f"{name}.png")
            temp_html = os.path.join(self.sprites_dir, f"temp_{name}.html")
            
            # Wrap SVG into transparent HTML page
            html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; }}
  svg {{ display: block; }}
</style>
</head>
<body>
{svg_code}
</body>
</html>"""
            with open(temp_html, "w", encoding="utf-8") as f:
                f.write(html_content)

            # Rasterize via Chrome headless
            cmd = [
                CHROME_PATH,
                "--headless",
                "--disable-gpu",
                "--default-background-color=00000000",
                f"--screenshot={out_png}",
                "--window-size=600,800",
                temp_html
            ]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # Crop bounding box of non-transparent pixels
                im = Image.open(out_png)
                bbox = im.getbbox()
                if bbox:
                    im = im.crop(bbox)
                    im.save(out_png)
                self.cached_images[name] = Image.open(out_png).convert("RGBA")
            except Exception as e:
                print(f"Warning: Failed to rasterize {name}: {e}")
            finally:
                if os.path.exists(temp_html):
                    os.remove(temp_html)

        print(f"✅ Loaded {len(self.cached_images)} high-fidelity vector assets into memory.")

    def get(self, name):
        """Retrieves cached PIL image for sprite."""
        if name in self.cached_images:
            return self.cached_images[name]
        png_path = os.path.join(self.sprites_dir, f"{name}.png")
        if os.path.exists(png_path):
            img = Image.open(png_path).convert("RGBA")
            self.cached_images[name] = img
            return img
        return None


if __name__ == "__main__":
    mgr = HighFidelityAssetManager()
    print("Asset Compilation Complete!")
