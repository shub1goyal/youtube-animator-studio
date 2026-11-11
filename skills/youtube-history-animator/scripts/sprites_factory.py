"""
engine_2d/sprites_factory.py
Generates modular SVG sprite components and rasterizes them into transparent RGBA PNGs
for the 2D Animation Engine using headless Chromium.
"""

import os
import subprocess

SPRITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(SPRITES_DIR, exist_ok=True)

SPRITE_DEFINITIONS = {
    # ================= SHEIKH ZAYED RIG =================
    "sheikh_zayed_body": {
        "w": 400, "h": 500,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
          <g transform="translate(40, 20)">
            <!-- Inner White Thobe -->
            <path d="M 100 120 C 100 110, 220 110, 220 120 L 250 420 C 210 430, 110 430, 70 420 Z" fill="#fdfbf7" stroke="#111" stroke-width="6" />
            <!-- Royal Bisht Robe (Dark Charcoal / Brown with Gold Brocade) -->
            <path d="M 80 120 C 80 100, 240 100, 240 120 L 270 430 C 230 440, 90 440, 50 430 Z" fill="#2d2218" stroke="#111" stroke-width="7" stroke-linejoin="round" />
            <!-- Gold Trim along Bisht Collar & Opening (Zari) -->
            <path d="M 125 120 L 160 260 L 195 120" fill="none" stroke="#d4af37" stroke-width="10" stroke-linecap="round" />
            <path d="M 160 260 L 160 435" fill="none" stroke="#d4af37" stroke-width="8" />
            <!-- Left Arm in Robe Sleeve -->
            <path d="M 80 140 Q 30 200 60 280 Q 90 280 100 240" fill="#2d2218" stroke="#111" stroke-width="6" />
            <!-- Right Arm Gesturing / Blueprint hand -->
            <path d="M 240 140 Q 290 190 270 270 Q 240 270 220 230" fill="#2d2218" stroke="#111" stroke-width="6" />
            <!-- Hands -->
            <circle cx="65" cy="285" r="16" fill="#f2caa0" stroke="#111" stroke-width="4" />
            <circle cx="265" cy="275" r="16" fill="#f2caa0" stroke="#111" stroke-width="4" />
          </g>
        </svg>
        """
    },
    "sheikh_zayed_head": {
        "w": 360, "h": 380,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 380" width="360" height="380">
          <g transform="translate(30, 20)">
            <!-- Flowing White Ghutra Headdress -->
            <path d="M 50 150 C 40 80, 260 80, 250 150 C 280 230, 280 320, 270 360 C 250 340, 230 260, 220 220 C 200 200, 100 200, 80 220 C 70 260, 50 340, 30 360 C 20 320, 20 230, 50 150 Z" 
                  fill="#ffffff" stroke="#111" stroke-width="6" stroke-linejoin="round" />
            <!-- Agal Cord (Double Black Ring) -->
            <ellipse cx="150" cy="115" rx="72" ry="18" fill="none" stroke="#18181b" stroke-width="12" />
            <ellipse cx="150" cy="126" rx="68" ry="16" fill="none" stroke="#27272a" stroke-width="10" />
            <!-- Head Shape -->
            <path d="M 85 160 C 85 120, 215 120, 215 160 C 215 220, 85 220, 85 160 Z" fill="#f2caa0" stroke="#111" stroke-width="6" />
            <!-- Distinguished Arab Beard & Mustache -->
            <path d="M 100 205 Q 150 245 200 205 Q 185 240 150 250 Q 115 240 100 205 Z" fill="#2d2926" stroke="#111" stroke-width="4" />
            <path d="M 120 190 Q 150 200 180 190" fill="none" stroke="#2d2926" stroke-width="8" stroke-linecap="round" />
            <!-- Wise Eyebrows -->
            <path d="M 105 145 Q 125 138 135 145" fill="none" stroke="#2d2926" stroke-width="6" stroke-linecap="round" />
            <path d="M 165 145 Q 175 138 195 145" fill="none" stroke="#2d2926" stroke-width="6" stroke-linecap="round" />
          </g>
        </svg>
        """
    },

    # ================= PEARL DIVER RIG =================
    "pearl_diver_body": {
        "w": 400, "h": 500,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
          <g transform="translate(40, 20)">
            <!-- Weathered Torso -->
            <path d="M 100 120 C 90 110, 230 110, 220 120 L 210 250 C 190 260, 130 260, 110 250 Z" fill="#d99b66" stroke="#111" stroke-width="6" />
            <!-- Traditional Wizar (Waist Wrap Cloth) -->
            <path d="M 95 240 C 95 235, 225 235, 225 240 L 235 400 C 200 415, 120 415, 85 400 Z" fill="#3c6382" stroke="#111" stroke-width="6" />
            <!-- Pearl Collection Rope Basket Strap -->
            <line x1="100" y1="125" x2="210" y2="250" stroke="#78350f" stroke-width="7" stroke-dasharray="8,4" />
            <!-- Wicker Diving Basket -->
            <ellipse cx="230" cy="270" rx="35" ry="45" fill="#a16207" stroke="#111" stroke-width="5" />
            <line x1="200" y1="270" x2="260" y2="270" stroke="#78350f" stroke-width="4" />
            <line x1="230" y1="230" x2="230" y2="310" stroke="#78350f" stroke-width="4" />
            <!-- Divers Arms -->
            <path d="M 90 135 Q 40 190 60 260" fill="none" stroke="#d99b66" stroke-width="26" stroke-linecap="round" />
            <path d="M 90 135 Q 40 190 60 260" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" />
            <path d="M 230 135 Q 280 180 250 250" fill="none" stroke="#d99b66" stroke-width="26" stroke-linecap="round" />
            <path d="M 230 135 Q 280 180 250 250" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" />
          </g>
        </svg>
        """
    },
    "pearl_diver_head": {
        "w": 360, "h": 360,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 360" width="360" height="360">
          <g transform="translate(30, 20)">
            <!-- Head Shape -->
            <circle cx="150" cy="160" r="65" fill="#d99b66" stroke="#111" stroke-width="6" />
            <!-- Diver Cap (Fabric Bandana) -->
            <path d="M 90 145 C 90 100, 210 100, 210 145 C 200 120, 100 120, 90 145 Z" fill="#1e272e" stroke="#111" stroke-width="6" />
            <!-- Traditional Nose Clip (Ftam made of turtle shell / wood) -->
            <path d="M 144 165 C 140 150, 160 150, 156 165 L 150 178 Z" fill="#854d0e" stroke="#111" stroke-width="4" />
            <!-- Determined Diver Eyebrows -->
            <path d="M 110 140 Q 125 130 135 140" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round" />
            <path d="M 165 140 Q 175 130 190 140" fill="none" stroke="#111" stroke-width="5" stroke-linecap="round" />
          </g>
        </svg>
        """
    },

    # ================= BRITISH OFFICER RIG =================
    "british_officer_body": {
        "w": 400, "h": 500,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
          <g transform="translate(40, 20)">
            <!-- Royal Navy Dark Blue Coat -->
            <path d="M 85 120 C 85 105, 235 105, 235 120 L 250 420 C 210 430, 110 430, 70 420 Z" fill="#192a56" stroke="#111" stroke-width="7" stroke-linejoin="round" />
            <!-- Crimson Red Officer Sash -->
            <path d="M 95 130 L 230 260 L 215 285 L 80 155 Z" fill="#c23616" stroke="#111" stroke-width="4" />
            <!-- Double Row of Gold Buttons -->
            <circle cx="130" cy="180" r="5" fill="#fbc531" stroke="#111" stroke-width="2" />
            <circle cx="130" cy="210" r="5" fill="#fbc531" stroke="#111" stroke-width="2" />
            <circle cx="130" cy="240" r="5" fill="#fbc531" stroke="#111" stroke-width="2" />
            <circle cx="190" cy="180" r="5" fill="#fbc531" stroke="#111" stroke-width="2" />
            <circle cx="190" cy="210" r="5" fill="#fbc531" stroke="#111" stroke-width="2" />
            <circle cx="190" cy="240" r="5" fill="#fbc531" stroke="#111" stroke-width="2" />
            <!-- Gold Shoulder Epaulettes with Tassels -->
            <ellipse cx="80" cy="125" rx="22" ry="12" fill="#fbc531" stroke="#111" stroke-width="3" />
            <ellipse cx="240" cy="125" rx="22" ry="12" fill="#fbc531" stroke="#111" stroke-width="3" />
            <!-- Left Arm on Hip -->
            <path d="M 75 140 Q 30 190 70 230" fill="none" stroke="#192a56" stroke-width="26" stroke-linecap="round" />
            <path d="M 75 140 Q 30 190 70 230" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" />
            <!-- Right Arm Holding Treaty / Sword -->
            <path d="M 245 140 Q 285 190 250 240" fill="none" stroke="#192a56" stroke-width="26" stroke-linecap="round" />
            <path d="M 245 140 Q 285 190 250 240" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" />
          </g>
        </svg>
        """
    },
    "british_officer_head": {
        "w": 360, "h": 360,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 360" width="360" height="360">
          <g transform="translate(30, 20)">
            <!-- Head Shape -->
            <circle cx="150" cy="165" r="62" fill="#fcdba8" stroke="#111" stroke-width="6" />
            <!-- Victorian Muttonchops Sideburns -->
            <path d="M 90 145 C 90 195, 110 205, 110 175 Z" fill="#9c7a5b" stroke="#111" stroke-width="3" />
            <path d="M 210 145 C 210 195, 190 205, 190 175 Z" fill="#9c7a5b" stroke="#111" stroke-width="3" />
            <!-- Bicorne Admiral Hat -->
            <path d="M 40 135 C 50 60, 140 30, 150 30 C 160 30, 250 60, 260 135 C 220 115, 80 115, 40 135 Z" fill="#1e272e" stroke="#111" stroke-width="6" stroke-linejoin="round" />
            <path d="M 45 130 C 90 115, 210 115, 255 130" fill="none" stroke="#fbc531" stroke-width="5" />
            <!-- Golden Monocle over Left Eye -->
            <circle cx="178" cy="165" r="16" fill="rgba(255,255,255,0.4)" stroke="#fbc531" stroke-width="4" />
            <path d="M 194 165 Q 210 220 190 250" fill="none" stroke="#fbc531" stroke-width="2" />
          </g>
        </svg>
        """
    },

    # ================= MOUTHS & EYES (VISEMES & EXPRESSIONS) =================
    "mouth_closed": {
        "w": 120, "h": 60,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 60" width="120" height="60">
          <path d="M 30 30 Q 60 32 90 30" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" />
        </svg>"""
    },
    "mouth_open": {
        "w": 120, "h": 60,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 60" width="120" height="60">
          <ellipse cx="60" cy="30" rx="26" ry="16" fill="#63171b" stroke="#111" stroke-width="5" />
          <path d="M 42 22 Q 60 26 78 22" fill="#ffffff" stroke="#111" stroke-width="3" />
        </svg>"""
    },
    "mouth_smile": {
        "w": 120, "h": 60,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 60" width="120" height="60">
          <path d="M 28 24 Q 60 46 92 24" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" />
        </svg>"""
    },
    "eyes_open": {
        "w": 140, "h": 60,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 60" width="140" height="60">
          <circle cx="40" cy="30" r="14" fill="#ffffff" stroke="#111" stroke-width="4" />
          <circle cx="43" cy="30" r="6" fill="#111" />
          <circle cx="45" cy="27" r="2.5" fill="#fff" />
          <circle cx="100" cy="30" r="14" fill="#ffffff" stroke="#111" stroke-width="4" />
          <circle cx="103" cy="30" r="6" fill="#111" />
          <circle cx="105" cy="27" r="2.5" fill="#fff" />
        </svg>"""
    },
    "eyes_blink": {
        "w": 140, "h": 60,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 60" width="140" height="60">
          <path d="M 26 30 Q 40 38 54 30" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" />
          <path d="M 86 30 Q 100 38 114 30" fill="none" stroke="#111" stroke-width="6" stroke-linecap="round" />
        </svg>"""
    },
    "eyes_dollar": {
        "w": 140, "h": 60,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 60" width="140" height="60">
          <circle cx="40" cy="30" r="16" fill="#f1c40f" stroke="#111" stroke-width="4" />
          <text x="31" y="40" font-family="Arial, sans-serif" font-weight="900" font-size="28" fill="#111">$</text>
          <circle cx="100" cy="30" r="16" fill="#f1c40f" stroke="#111" stroke-width="4" />
          <text x="91" y="40" font-family="Arial, sans-serif" font-weight="900" font-size="28" fill="#111">$</text>
        </svg>"""
    },
    "eyes_shocked": {
        "w": 140, "h": 60,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 60" width="140" height="60">
          <circle cx="40" cy="30" r="18" fill="#ffffff" stroke="#111" stroke-width="5" />
          <circle cx="40" cy="30" r="4" fill="#111" />
          <circle cx="100" cy="30" r="18" fill="#ffffff" stroke="#111" stroke-width="5" />
          <circle cx="100" cy="30" r="4" fill="#111" />
        </svg>"""
    },
    "eyes_x": {
        "w": 140, "h": 60,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 60" width="140" height="60">
          <path d="M 28 18 L 52 42 M 52 18 L 28 42" stroke="#e74c3c" stroke-width="7" stroke-linecap="round" />
          <path d="M 88 18 L 112 42 M 112 18 L 88 42" stroke="#e74c3c" stroke-width="7" stroke-linecap="round" />
        </svg>"""
    },

    # ================= VEHICLES, STRUCTURES & PROPS =================
    "camel": {
        "w": 400, "h": 340,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 340" width="400" height="340">
          <g transform="translate(20, 20)">
            <!-- Legs (Back and Front) -->
            <path d="M 120 180 L 110 300 L 95 300" fill="none" stroke="#b7791f" stroke-width="14" stroke-linecap="round" />
            <path d="M 140 180 L 150 300 L 165 300" fill="none" stroke="#92400e" stroke-width="14" stroke-linecap="round" />
            <path d="M 260 180 L 250 300 L 235 300" fill="none" stroke="#b7791f" stroke-width="14" stroke-linecap="round" />
            <path d="M 280 180 L 290 300 L 305 300" fill="none" stroke="#92400e" stroke-width="14" stroke-linecap="round" />
            <!-- Body & Hump -->
            <path d="M 100 180 C 90 140, 130 90, 180 80 C 230 70, 260 130, 280 180 C 290 220, 100 220, 100 180 Z" fill="#d97706" stroke="#111" stroke-width="6" />
            <!-- Red Decorative Saddle Blanket -->
            <rect x="160" y="110" width="80" height="60" rx="8" fill="#dc2626" stroke="#111" stroke-width="4" />
            <line x1="160" y1="140" x2="240" y2="140" stroke="#facc15" stroke-width="5" />
            <!-- Long Curved Neck & Head -->
            <path d="M 270 170 C 310 150, 330 90, 310 40 C 300 20, 360 20, 360 50 C 360 80, 320 170, 290 190 Z" fill="#d97706" stroke="#111" stroke-width="6" />
            <!-- Camel Eye with Long Lashes -->
            <circle cx="340" cy="35" r="5" fill="#111" />
            <!-- Tail -->
            <path d="M 100 180 Q 70 210 80 240" fill="none" stroke="#d97706" stroke-width="8" stroke-linecap="round" />
          </g>
        </svg>
        """
    },
    "supercar": {
        "w": 500, "h": 200,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 200" width="500" height="200">
          <g transform="translate(10, 20)">
            <!-- Gold Metallic Paint Chassis -->
            <path d="M 30 130 L 70 70 L 160 50 L 320 50 L 400 90 L 460 110 L 470 140 L 30 140 Z" fill="url(#goldGrad)" stroke="#111" stroke-width="6" stroke-linejoin="round" />
            <defs>
              <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#fef08a" />
                <stop offset="50%" stop-color="#eab308" />
                <stop offset="100%" stop-color="#ca8a04" />
              </linearGradient>
            </defs>
            <!-- Tinted Windshield & Cabin -->
            <path d="M 170 54 L 230 25 L 310 25 L 340 54 Z" fill="#0f172a" stroke="#111" stroke-width="4" />
            <!-- Rear Aerodynamic Spoiler -->
            <path d="M 40 65 L 80 65 L 70 75 L 30 75 Z" fill="#18181b" stroke="#111" stroke-width="4" />
            <!-- Glowing LED Headlights (Cyan Neon) -->
            <polygon points="440,105 465,112 445,120" fill="#38bdf8" />
            <!-- Wheels with Low-Profile Tires & Chrome Gold Rims -->
            <circle cx="120" cy="140" r="38" fill="#18181b" stroke="#111" stroke-width="5" />
            <circle cx="120" cy="140" r="22" fill="#ca8a04" stroke="#fef08a" stroke-width="4" />
            <circle cx="390" cy="140" r="38" fill="#18181b" stroke="#111" stroke-width="5" />
            <circle cx="390" cy="140" r="22" fill="#ca8a04" stroke="#fef08a" stroke-width="4" />
          </g>
        </svg>
        """
    },
    "dhow_ship": {
        "w": 400, "h": 320,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 320" width="400" height="320">
          <g transform="translate(20, 20)">
            <!-- Wooden Hull (Teak) -->
            <path d="M 30 210 Q 180 260 330 200 L 310 240 Q 180 270 50 240 Z" fill="#78350f" stroke="#111" stroke-width="6" stroke-linejoin="round" />
            <!-- Mast -->
            <line x1="170" y1="210" x2="150" y2="40" stroke="#451a03" stroke-width="8" stroke-linecap="round" />
            <!-- Lateen Triangular White Canvas Sail -->
            <path d="M 70 80 L 280 40 L 170 200 Z" fill="#fefce8" stroke="#111" stroke-width="6" stroke-linejoin="round" opacity="0.95" />
            <!-- Rigging Ropes -->
            <line x1="70" y1="80" x2="40" y2="210" stroke="#78350f" stroke-width="3" />
            <line x1="280" y1="40" x2="310" y2="200" stroke="#78350f" stroke-width="3" />
          </g>
        </svg>
        """
    },
    "oil_derrick": {
        "w": 320, "h": 460,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 460" width="320" height="460">
          <g transform="translate(20, 20)">
            <!-- Steel Lattice Tower Structure -->
            <polygon points="140,40 180,40 260,400 60,400" fill="none" stroke="#27272a" stroke-width="8" stroke-linejoin="round" />
            <!-- Cross Bracing Beams -->
            <line x1="120" y1="120" x2="200" y2="120" stroke="#3f3f46" stroke-width="5" />
            <line x1="100" y1="200" x2="220" y2="200" stroke="#3f3f46" stroke-width="6" />
            <line x1="80" y1="300" x2="240" y2="300" stroke="#3f3f46" stroke-width="7" />
            <line x1="120" y1="120" x2="220" y2="200" stroke="#52525b" stroke-width="4" />
            <line x1="200" y1="120" x2="100" y2="200" stroke="#52525b" stroke-width="4" />
            <line x1="100" y1="200" x2="240" y2="300" stroke="#52525b" stroke-width="4" />
            <line x1="220" y1="200" x2="80" y2="300" stroke="#52525b" stroke-width="4" />
            <!-- Top Crown Block Sheave -->
            <rect x="130" y="20" width="60" height="20" fill="#eab308" stroke="#111" stroke-width="4" />
          </g>
        </svg>
        """
    },
    "burj_khalifa": {
        "w": 300, "h": 700,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 700" width="300" height="700">
          <g transform="translate(30, 20)">
            <!-- Center Spire (Tip reaching into sky) -->
            <line x1="120" y1="20" x2="120" y2="120" stroke="#e2e8f0" stroke-width="4" />
            <circle cx="120" cy="18" r="4" fill="#38bdf8" />
            <!-- Stepped Tapering Sections (Y-shaped Architecture) -->
            <polygon points="110,120 130,120 135,220 105,220" fill="#cbd5e1" stroke="#1e293b" stroke-width="3" />
            <polygon points="100,220 140,220 148,340 92,340" fill="#94a3b8" stroke="#1e293b" stroke-width="4" />
            <polygon points="85,340 155,340 165,480 75,480" fill="#64748b" stroke="#1e293b" stroke-width="5" />
            <polygon points="65,480 175,480 195,660 45,660" fill="#475569" stroke="#1e293b" stroke-width="6" />
            <!-- Reflective Glass Highlights & Balconies -->
            <line x1="120" y1="120" x2="120" y2="660" stroke="#f8fafc" stroke-width="3" opacity="0.8" />
            <line x1="90" y1="340" x2="90" y2="660" stroke="#38bdf8" stroke-width="2" opacity="0.6" />
            <line x1="150" y1="340" x2="150" y2="660" stroke="#38bdf8" stroke-width="2" opacity="0.6" />
          </g>
        </svg>
        """
    },
    "hope_satellite": {
        "w": 400, "h": 260,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260" width="400" height="260">
          <g transform="translate(20, 20)">
            <!-- Left Solar Array Panel (Blue Photovoltaic Cells) -->
            <rect x="20" y="70" width="110" height="80" rx="4" fill="#1e3a8a" stroke="#60a5fa" stroke-width="3" />
            <line x1="55" y1="70" x2="55" y2="150" stroke="#93c5fd" stroke-width="2" />
            <line x1="95" y1="70" x2="95" y2="150" stroke="#93c5fd" stroke-width="2" />
            <line x1="20" y1="110" x2="130" y2="110" stroke="#93c5fd" stroke-width="2" />
            <!-- Right Solar Array Panel -->
            <rect x="230" y="70" width="110" height="80" rx="4" fill="#1e3a8a" stroke="#60a5fa" stroke-width="3" />
            <line x1="265" y1="70" x2="265" y2="150" stroke="#93c5fd" stroke-width="2" />
            <line x1="305" y1="70" x2="305" y2="150" stroke="#93c5fd" stroke-width="2" />
            <line x1="230" y1="110" x2="340" y2="110" stroke="#93c5fd" stroke-width="2" />
            <!-- Main Satellite Hexagonal Gold Foil Body -->
            <polygon points="150,60 210,60 230,110 210,160 150,160 130,110" fill="#facc15" stroke="#111" stroke-width="5" />
            <!-- High Gain Parabolic Dish Antenna -->
            <ellipse cx="180" cy="50" rx="35" ry="12" fill="#e2e8f0" stroke="#111" stroke-width="4" />
            <line x1="180" y1="50" x2="180" y2="20" stroke="#dc2626" stroke-width="3" />
          </g>
        </svg>
        """
    },
    "gold_coin": {
        "w": 120, "h": 120,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
          <circle cx="60" cy="60" r="54" fill="#eab308" stroke="#713f12" stroke-width="6" />
          <circle cx="60" cy="60" r="44" fill="#facc15" stroke="#ca8a04" stroke-width="4" />
          <text x="44" y="78" font-family="Arial, sans-serif" font-weight="900" font-size="52" fill="#713f12">$</text>
        </svg>"""
    },
    "pearl_oyster": {
        "w": 200, "h": 160,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 160" width="200" height="160">
          <path d="M 20 120 C 20 50, 180 50, 180 120 C 180 150, 20 150, 20 120 Z" fill="#64748b" stroke="#0f172a" stroke-width="6" />
          <ellipse cx="100" cy="115" rx="70" ry="25" fill="#f8fafc" stroke="#94a3b8" stroke-width="4" />
          <!-- Glowing Natural Pearl -->
          <circle cx="100" cy="100" r="28" fill="#ffffff" stroke="#cbd5e1" stroke-width="3" />
          <circle cx="92" cy="92" r="8" fill="#ffffff" />
          <!-- Sparkle Glint -->
          <polygon points="100,60 104,70 114,74 104,78 100,88 96,78 86,74 96,70" fill="#fef08a" />
        </svg>"""
    },
    "uae_flag": {
        "w": 300, "h": 180,
        "svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 180" width="300" height="180">
          <!-- 3 Horizontal Stripes: Green, White, Black -->
          <rect x="75" y="0" width="225" height="60" fill="#00732f" />
          <rect x="75" y="60" width="225" height="60" fill="#ffffff" />
          <rect x="75" y="120" width="225" height="60" fill="#000000" />
          <!-- Vertical Red Hoist -->
          <rect x="0" y="0" width="75" height="180" fill="#ff0000" />
          <!-- Border -->
          <rect x="0" y="0" width="300" height="180" fill="none" stroke="#111" stroke-width="6" />
        </svg>"""
    }
}


def build_all_sprites():
    """Generates transparent PNG sprites via Chrome headless."""
    print(f"Building {len(SPRITE_DEFINITIONS)} transparent sprites...")
    for name, defn in SPRITE_DEFINITIONS.items():
        w = defn["w"]
        h = defn["h"]
        svg_code = defn["svg"].strip()

        html = f"""<!DOCTYPE html>
<html>
<body style='margin:0; padding:0; background:transparent; overflow:hidden;'>
  {svg_code}
</body>
</html>"""
        html_path = os.path.join(SPRITES_DIR, f"{name}.html")
        png_path = os.path.join(SPRITES_DIR, f"{name}.png")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        cmd = [
            CHROME_PATH,
            "--headless=new",
            f"--window-size={w},{h}",
            "--default-background-color=00000000",
            f"--screenshot={png_path}",
            html_path
        ]
        subprocess.run(cmd, check=True)
        # Clean up temporary HTML
        try:
            os.remove(html_path)
        except OSError:
            pass

    print(f"All {len(SPRITE_DEFINITIONS)} sprites built in {SPRITES_DIR}!")


if __name__ == "__main__":
    build_all_sprites()

