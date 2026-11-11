"""
engine_2d/synthesize_narrative_props.py
Synthesizes all rich OverSimplified / History Matters graphic-novel narrative props:
- karak_chai_glass: Steaming amber tea with specular highlights & vapor coils
- oil_valve_giant: Cast-iron shutoff valve labeled 'OIL RELIANCE' (OFF)
- solar_farm_panel: Futuristic desert photovoltaic array
- nuclear_atom_plant: Barakah clean dome with glowing atomic orbits
- crying_oil_barrel: Comedic blue/black oil drum crying tears into bucket
- glowing_blueprint_map: Rolled architectural blueprint 'SUPER EMIRATES'
- dallah_coffee_pot: Traditional brass Arabic dallah with finjan cup
- giant_oyster_pearl: Pried open oyster shell with glowing gold pearl
- pirate_ship_eyepatch: Gulf pirate dhow with skull flag and eyepatch
- burj_al_arab_hotel: Sail-shaped luxury hotel tower on sea island
- robotic_camel_mars: Cybernetic white/gold mecha-camel on red Mars sand
- money_mattress_cash: Bulging lumpy mattress stuffed with cash
- water_well_dripping: Desert stone well with dripping leaky bucket
- rubber_stamp_treaty: Red wooden notary stamp
- oil_lantern_tent: Glowing brass hurricane lantern
- bedouin_tent: Layered desert canopy with woven goat-hair & oriental carpet
- campfire: Burning acacia logs with 3-layer flame tongues & glowing embers
- oil_derrick_monumental: Monumental steel lattice truss derrick with flare burner

UPGRADE 1: Graphic-Novel Vector Spec
- Outer silhouette strokes: stroke="#090a0f" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"
- Inner detail lines & crossbeams: stroke-width="3.5"
- Specular glass & metallic highlights: rgba(255,255,255,0.45)
- Multi-stop rich gradients and 2-tone cel-shading
"""

import os
import sys
import subprocess
from PIL import Image

SPRITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
os.makedirs(SPRITES_DIR, exist_ok=True)
try:
    from config import CHROME_PATH
except ImportError:
    import shutil
    CHROME_PATH = os.environ.get("CHROME_PATH") or shutil.which("chrome") or shutil.which("google-chrome") or r"C:\Program Files\Google\Chrome\Application\chrome.exe"

NARRATIVE_PROPS = {
    # 1. KARAK CHAI GLASS (Steaming amber karak tea in glass cup with golden saucer & specular shine)
    "karak_chai_glass": {
        "w": 340, "h": 420,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 420" width="340" height="420">
          <defs>
            <linearGradient id="teaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#f59e0b"/>
              <stop offset="35%" stop-color="#d97706"/>
              <stop offset="75%" stop-color="#92400e"/>
              <stop offset="100%" stop-color="#451a03"/>
            </linearGradient>
            <linearGradient id="goldSaucer" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#b45309"/>
              <stop offset="30%" stop-color="#fbbf24"/>
              <stop offset="60%" stop-color="#fef08a"/>
              <stop offset="90%" stop-color="#d97706"/>
              <stop offset="100%" stop-color="#78350f"/>
            </linearGradient>
            <filter id="steamGlow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>

          <!-- Golden Saucer Base -->
          <ellipse cx="170" cy="370" rx="140" ry="26" fill="url(#goldSaucer)" stroke="#090a0f" stroke-width="6.5"/>
          <ellipse cx="170" cy="365" rx="100" ry="16" fill="#ca8a04" stroke="#090a0f" stroke-width="3.5"/>

          <!-- Glass Handle -->
          <path d="M 230 200 C 315 200, 315 310, 230 310" fill="none" stroke="#090a0f" stroke-width="20" stroke-linecap="round"/>
          <path d="M 230 200 C 310 200, 310 310, 230 310" fill="none" stroke="#e0f2fe" stroke-width="10" stroke-linecap="round"/>
          <path d="M 235 205 C 300 205, 300 305, 235 305" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="4" stroke-linecap="round"/>

          <!-- Glass Cup Outer Body (Cel-Shaded) -->
          <path d="M 105 140 L 125 340 C 125 352, 215 352, 215 340 L 235 140 Z" 
                fill="#e0f2fe" opacity="0.35" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>

          <!-- Rich Amber Karak Chai Liquid -->
          <path d="M 112 185 L 127 335 C 127 345, 213 345, 213 335 L 228 185 C 210 196, 130 196, 112 185 Z" 
                fill="url(#teaGrad)" stroke="#090a0f" stroke-width="4.5"/>
          <!-- Chai Base Shadow -->
          <path d="M 125 300 C 145 340, 195 340, 215 300 L 213 335 C 213 345, 127 345, 127 335 Z" fill="#2d1302" opacity="0.7"/>

          <!-- Frothy Karak Milk Foam Head -->
          <ellipse cx="170" cy="185" rx="58" ry="15" fill="#fef08a" stroke="#090a0f" stroke-width="4.5"/>
          <ellipse cx="155" cy="182" rx="20" ry="7" fill="#ffffff" opacity="0.85"/>
          <circle cx="190" cy="186" r="4" fill="#fef9c3"/>

          <!-- Glass Rim -->
          <ellipse cx="170" cy="140" rx="66" ry="16" fill="none" stroke="#090a0f" stroke-width="6.5"/>
          <ellipse cx="170" cy="140" rx="63" ry="14" fill="#ffffff" opacity="0.35"/>

          <!-- Specular Glass Highlights (Graphic-Novel Sheen) -->
          <path d="M 126 170 L 136 325" fill="none" stroke="#ffffff" stroke-width="9" stroke-linecap="round" opacity="0.75"/>
          <path d="M 142 185 L 148 295" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round" opacity="0.5"/>
          <path d="M 214 175 L 206 325" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="4.5" stroke-linecap="round"/>

          <!-- Steaming Vapor Coils -->
          <path d="M 148 130 C 128 85, 168 55, 142 15" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity="0.85" filter="url(#steamGlow)"/>
          <path d="M 175 125 C 195 80, 155 50, 180 10" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" opacity="0.9" filter="url(#steamGlow)"/>
          <path d="M 195 130 C 215 90, 185 65, 205 30" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity="0.75" filter="url(#steamGlow)"/>
        </svg>
        """
    },

    # 2. DALLAH COFFEE POT (Traditional ornate Arabian brass dallah & finjan cup)
    "dallah_coffee_pot": {
        "w": 360, "h": 440,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 440" width="360" height="440">
          <defs>
            <linearGradient id="brassGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#92400e"/>
              <stop offset="20%" stop-color="#d97706"/>
              <stop offset="50%" stop-color="#fbbf24"/>
              <stop offset="75%" stop-color="#fef08a"/>
              <stop offset="90%" stop-color="#d97706"/>
              <stop offset="100%" stop-color="#78350f"/>
            </linearGradient>
            <linearGradient id="goldHighlight" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8"/>
              <stop offset="100%" stop-color="#ffffff" stop-opacity="0.1"/>
            </linearGradient>
          </defs>

          <!-- Heavy Brass Circular Base -->
          <ellipse cx="170" cy="400" rx="85" ry="20" fill="url(#brassGrad)" stroke="#090a0f" stroke-width="6.5"/>
          <ellipse cx="170" cy="396" rx="65" ry="14" fill="#b45309" stroke="#090a0f" stroke-width="3.5"/>

          <!-- Majestic Hourglass Dallah Body with Cel-Shading -->
          <path d="M 110 395 C 90 330, 120 250, 155 230 L 150 150 L 190 150 L 185 230 C 220 250, 250 330, 230 395 Z" 
                fill="url(#brassGrad)" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
          <!-- Shaded Left Contour -->
          <path d="M 110 395 C 90 330, 120 250, 155 230 L 150 150 L 165 150 L 140 240 C 115 260, 105 330, 125 395 Z" fill="#78350f" opacity="0.6"/>
          <!-- Specular Metallic Sheen -->
          <path d="M 185 160 L 180 230 C 205 250, 225 310, 215 385" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="5" stroke-linecap="round"/>

          <!-- Ornate Engraving Bands -->
          <path d="M 108 335 Q 170 355, 232 335" fill="none" stroke="#090a0f" stroke-width="3.5"/>
          <path d="M 125 285 Q 170 300, 215 285" fill="none" stroke="#090a0f" stroke-width="3.5"/>
          <circle cx="170" cy="310" r="6" fill="#fef08a" stroke="#090a0f" stroke-width="2"/>

          <!-- Elegant Curved Beak Spout -->
          <path d="M 140 210 C 50 190, 25 85, 68 75 C 78 90, 100 145, 150 170 Z" 
                fill="url(#brassGrad)" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
          <path d="M 68 75 C 60 120, 85 160, 140 210" fill="none" stroke="#78350f" stroke-width="3.5"/>

          <!-- High Finial Spire Lid with Crescent -->
          <path d="M 145 150 L 170 45 L 195 150 Z" fill="url(#brassGrad)" stroke="#090a0f" stroke-width="6.5"/>
          <circle cx="170" cy="40" r="10" fill="#fef08a" stroke="#090a0f" stroke-width="4"/>

          <!-- Large Dramatic Brass Handle -->
          <path d="M 185 170 C 290 150, 305 330, 205 355" fill="none" stroke="#090a0f" stroke-width="22" stroke-linecap="round"/>
          <path d="M 185 170 C 290 150, 305 330, 205 355" fill="none" stroke="url(#brassGrad)" stroke-width="14" stroke-linecap="round"/>
          <path d="M 190 175 C 280 160, 295 320, 210 345" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="3.5" stroke-linecap="round"/>

          <!-- Small Finjan Porcelain Cup Beside It -->
          <ellipse cx="285" cy="400" rx="38" ry="13" fill="#090a0f" stroke="#090a0f" stroke-width="6.5"/>
          <ellipse cx="285" cy="397" rx="36" ry="11" fill="#f8fafc"/>
          <path d="M 255 365 L 265 400 C 275 407, 295 407, 305 400 L 315 365 Z" 
                fill="#f8fafc" stroke="#090a0f" stroke-width="4.5" stroke-linejoin="round"/>
          <ellipse cx="285" cy="365" rx="30" ry="10" fill="#78350f" stroke="#090a0f" stroke-width="3.5"/>
          <!-- Steaming Coffee Aroma -->
          <path d="M 285 355 Q 275 325, 287 305" fill="none" stroke="#e2e8f0" stroke-width="3.5" stroke-linecap="round"/>
        </svg>
        """
    },

    # 3. BEDOUIN TENT (Layered desert canopy with woven goat-hair & oriental carpet)
    "bedouin_tent": {
        "w": 520, "h": 380,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 380" width="520" height="380">
          <defs>
            <linearGradient id="tentFabric" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#334155"/>
              <stop offset="50%" stop-color="#1e293b"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
            <linearGradient id="rugGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#991b1b"/>
              <stop offset="25%" stop-color="#dc2626"/>
              <stop offset="50%" stop-color="#b45309"/>
              <stop offset="75%" stop-color="#dc2626"/>
              <stop offset="100%" stop-color="#991b1b"/>
            </linearGradient>
          </defs>

          <!-- Outer Guy Ropes to Sand Stakes -->
          <line x1="60" y1="200" x2="10" y2="350" stroke="#090a0f" stroke-width="4.5" stroke-linecap="round"/>
          <line x1="460" y1="200" x2="510" y2="350" stroke="#090a0f" stroke-width="4.5" stroke-linecap="round"/>
          <!-- Sand Stakes -->
          <line x1="8" y1="340" x2="12" y2="365" stroke="#78350f" stroke-width="6"/>
          <line x1="508" y1="340" x2="512" y2="365" stroke="#78350f" stroke-width="6"/>

          <!-- Dark Interior Shaded Cavity -->
          <polygon points="120,200 400,200 450,350 70,350" fill="#090a0f"/>

          <!-- Traditional Patterned Arabian Rug Inside -->
          <polygon points="130,280 390,280 430,350 90,350" fill="url(#rugGrad)" stroke="#090a0f" stroke-width="3.5"/>
          <line x1="120" y1="300" x2="400" y2="300" stroke="#fde047" stroke-width="3"/>
          <line x1="110" y1="320" x2="410" y2="320" stroke="#fde047" stroke-width="3"/>
          <!-- Rug Fringe Tassels -->
          <line x1="85" y1="352" x2="435" y2="352" stroke="#fef08a" stroke-width="3" stroke-dasharray="4,3"/>

          <!-- Master Center Wooden Support Pole -->
          <line x1="260" y1="75" x2="260" y2="350" stroke="#090a0f" stroke-width="12" stroke-linecap="round"/>
          <line x1="260" y1="75" x2="260" y2="350" stroke="#78350f" stroke-width="7" stroke-linecap="round"/>

          <!-- Main Canopy Roof (Heavy Woven Goat-Hair Fabric) -->
          <polygon points="260,70 60,200 120,210 260,110 400,210 460,200" 
                   fill="url(#tentFabric)" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>

          <!-- Left & Right Flaps Dropping Down -->
          <polygon points="60,200 120,210 80,350 40,350" fill="#1e293b" stroke="#090a0f" stroke-width="5" stroke-linejoin="round"/>
          <polygon points="460,200 400,210 440,350 480,350" fill="#1e293b" stroke="#090a0f" stroke-width="5" stroke-linejoin="round"/>

          <!-- Traditional White/Cream Tribal Stripes -->
          <line x1="260" y1="80" x2="90" y2="205" stroke="#f8fafc" stroke-width="5"/>
          <line x1="260" y1="95" x2="105" y2="208" stroke="#f8fafc" stroke-width="3.5"/>
          <line x1="260" y1="80" x2="430" y2="205" stroke="#f8fafc" stroke-width="5"/>
          <line x1="260" y1="95" x2="415" y2="208" stroke="#f8fafc" stroke-width="3.5"/>

          <!-- Front Center Valance Drapery -->
          <path d="M 120 210 Q 190 230 260 215 Q 330 230 400 210" fill="none" stroke="#090a0f" stroke-width="5"/>
        </svg>
        """
    },

    # 4. OIL LANTERN TENT (Vintage hurricane brass lantern with glowing glass & warm bloom)
    "oil_lantern_tent": {
        "w": 320, "h": 420,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 420" width="320" height="420">
          <defs>
            <radialGradient id="lanternGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="30%" stop-color="#fef08a"/>
              <stop offset="65%" stop-color="#f59e0b"/>
              <stop offset="90%" stop-color="#b45309" stop-opacity="0.4"/>
              <stop offset="100%" stop-color="#78350f" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="brassLantern" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#78350f"/>
              <stop offset="25%" stop-color="#d97706"/>
              <stop offset="50%" stop-color="#fbbf24"/>
              <stop offset="80%" stop-color="#d97706"/>
              <stop offset="100%" stop-color="#451a03"/>
            </linearGradient>
          </defs>

          <!-- Hanging Wire Loop -->
          <circle cx="160" cy="55" r="28" fill="none" stroke="#090a0f" stroke-width="14"/>
          <circle cx="160" cy="55" r="28" fill="none" stroke="url(#brassLantern)" stroke-width="7"/>

          <!-- Brass Chimney Cap -->
          <path d="M 120 120 L 160 75 L 200 120 Z" fill="url(#brassLantern)" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
          <rect x="110" y="120" width="100" height="22" rx="4" fill="url(#brassLantern)" stroke="#090a0f" stroke-width="5"/>

          <!-- Glass Globe (Transparent Amber Ambient Light) -->
          <path d="M 120 142 C 70 200, 70 270, 120 310 L 200 310 C 250 270, 250 200, 200 142 Z" 
                fill="#fef9c3" opacity="0.4" stroke="#090a0f" stroke-width="6.5"/>

          <!-- Warm Glowing Radial Ambient Flame Buffer -->
          <circle cx="160" cy="225" r="85" fill="url(#lanternGlow)"/>

          <!-- Cartoon Teardrop Flame Inside -->
          <path d="M 160 180 C 142 215, 142 245, 160 252 C 178 245, 178 215, 160 180 Z" 
                fill="#fde047" stroke="#090a0f" stroke-width="3.5"/>
          <circle cx="160" cy="240" r="7" fill="#ffffff"/>

          <!-- Specular Glass Crescent Highlight -->
          <path d="M 125 160 C 95 210, 95 260, 122 295" fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="6" stroke-linecap="round"/>

          <!-- Protective Wire Cage Struts -->
          <path d="M 115 135 C 80 200, 80 265, 115 315" fill="none" stroke="#090a0f" stroke-width="6.5"/>
          <path d="M 205 135 C 240 200, 240 265, 205 315" fill="none" stroke="#090a0f" stroke-width="6.5"/>
          <line x1="160" y1="140" x2="160" y2="310" stroke="#090a0f" stroke-width="3.5"/>

          <!-- Heavy Brass Oil Reservoir Base -->
          <rect x="95" y="315" width="130" height="26" rx="4" fill="url(#brassLantern)" stroke="#090a0f" stroke-width="6.5"/>
          <ellipse cx="160" cy="375" rx="88" ry="26" fill="url(#brassLantern)" stroke="#090a0f" stroke-width="6.5"/>
          <ellipse cx="160" cy="370" rx="65" ry="15" fill="#f59e0b" stroke="#090a0f" stroke-width="3.5"/>
        </svg>
        """
    },

    # 5. CAMPFIRE (Crossed Acacia logs with 3-layer flame tongues & glowing embers)
    "campfire": {
        "w": 380, "h": 360,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 360" width="380" height="360">
          <defs>
            <radialGradient id="coalBed" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="35%" stop-color="#ea580c"/>
              <stop offset="70%" stop-color="#991b1b"/>
              <stop offset="100%" stop-color="#18181b"/>
            </radialGradient>
          </defs>

          <!-- Hot Glowing Coal Bed Base -->
          <ellipse cx="190" cy="305" rx="120" ry="32" fill="url(#coalBed)" stroke="#090a0f" stroke-width="4.5"/>

          <!-- Crossed Charcoal Logs (Graphic-Novel Cel-Shading) -->
          <rect x="70" y="275" width="240" height="38" rx="8" transform="rotate(-14 190 295)" 
                fill="#451a03" stroke="#090a0f" stroke-width="6.5"/>
          <rect x="70" y="275" width="240" height="38" rx="8" transform="rotate(14 190 295)" 
                fill="#291205" stroke="#090a0f" stroke-width="6.5"/>
          <!-- Bark & Wood Rings -->
          <ellipse cx="85" cy="270" rx="10" ry="16" fill="#78350f" stroke="#090a0f" stroke-width="3.5"/>
          <ellipse cx="295" cy="270" rx="10" ry="16" fill="#78350f" stroke="#090a0f" stroke-width="3.5"/>

          <!-- 3-Layered Flame Tongues -->
          <!-- Layer 1: Outer Crimson Fire Silhouette -->
          <path d="M 190 60 C 130 140, 110 200, 110 270 C 110 320, 270 320, 270 270 C 270 200, 250 140, 190 60 Z" 
                fill="#dc2626" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>

          <!-- Layer 2: Mid Amber Flame Tongue -->
          <path d="M 190 110 C 145 170, 135 220, 135 270 C 135 305, 245 305, 245 270 C 245 220, 235 170, 190 110 Z" 
                fill="#f59e0b" stroke="#090a0f" stroke-width="4.5" stroke-linejoin="round"/>

          <!-- Layer 3: Inner White-Yellow Core Heat -->
          <path d="M 190 170 C 160 210, 155 240, 155 275 C 155 295, 225 295, 225 275 C 225 240, 220 210, 190 170 Z" 
                fill="#fef08a" stroke="#090a0f" stroke-width="3.5"/>
          <ellipse cx="190" cy="265" rx="18" ry="24" fill="#ffffff"/>

          <!-- Rising Glowing Ember Sparks -->
          <circle cx="150" cy="80" r="5" fill="#fde047" stroke="#090a0f" stroke-width="1.5"/>
          <circle cx="230" cy="70" r="4.5" fill="#f97316" stroke="#090a0f" stroke-width="1.5"/>
          <circle cx="180" cy="35" r="4" fill="#fef08a" stroke="#090a0f" stroke-width="1.5"/>
          <circle cx="215" cy="42" r="3.5" fill="#fde047"/>
          <circle cx="135" cy="55" r="3" fill="#ea580c"/>
        </svg>
        """
    },

    # 6. OIL DERRICK MONUMENTAL (Massive industrial tapered truss tower with flare burner)
    "oil_derrick_monumental": {
        "w": 500, "h": 700,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 700" width="500" height="700">
          <defs>
            <linearGradient id="derrickSteel" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#1e293b"/>
              <stop offset="35%" stop-color="#475569"/>
              <stop offset="65%" stop-color="#64748b"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
          </defs>

          <!-- Heavy Base Concrete/Steel Foundation -->
          <rect x="50" y="650" width="400" height="42" rx="6" fill="#0f172a" stroke="#090a0f" stroke-width="6.5"/>
          <line x1="60" y1="660" x2="440" y2="660" stroke="#334155" stroke-width="3.5"/>

          <!-- Main Tapered Outer Lattice Columns -->
          <polygon points="190,80 310,80 410,650 90,650" fill="none" 
                   stroke="#090a0f" stroke-width="8" stroke-linejoin="round"/>
          <polygon points="190,80 310,80 410,650 90,650" fill="none" 
                   stroke="url(#derrickSteel)" stroke-width="5" stroke-linejoin="round"/>

          <!-- Horizontal Structural Girts -->
          <line x1="175" y1="180" x2="325" y2="180" stroke="#090a0f" stroke-width="6.5"/>
          <line x1="150" y1="310" x2="350" y2="310" stroke="#090a0f" stroke-width="6.5"/>
          <line x1="125" y1="450" x2="375" y2="450" stroke="#090a0f" stroke-width="6.5"/>
          <line x1="105" y1="570" x2="395" y2="570" stroke="#090a0f" stroke-width="6.5"/>

          <!-- Diagonal Crossbracing X-Trusses (stroke-width 3.5) -->
          <g stroke="#090a0f" stroke-width="4.5">
            <line x1="190" y1="80" x2="325" y2="180"/>
            <line x1="310" y1="80" x2="175" y2="180"/>
            <line x1="175" y1="180" x2="350" y2="310"/>
            <line x1="325" y1="180" x2="150" y2="310"/>
            <line x1="150" y1="310" x2="375" y2="450"/>
            <line x1="350" y1="310" x2="125" y2="450"/>
            <line x1="125" y1="450" x2="395" y2="570"/>
            <line x1="375" y1="450" x2="105" y2="570"/>
          </g>

          <!-- Metallic Specular Highlights along Beams -->
          <line x1="192" y1="84" x2="94" y2="646" stroke="rgba(255,255,255,0.35)" stroke-width="3"/>
          <line x1="308" y1="84" x2="406" y2="646" stroke="rgba(255,255,255,0.35)" stroke-width="3"/>

          <!-- Crown Block Pulley at Top -->
          <rect x="210" y="45" width="80" height="35" rx="6" fill="#fbbf24" stroke="#090a0f" stroke-width="6.5"/>
          <circle cx="235" cy="62" r="10" fill="#334155" stroke="#090a0f" stroke-width="3"/>
          <circle cx="265" cy="62" r="10" fill="#334155" stroke="#090a0f" stroke-width="3"/>

          <!-- Crown Gas Flare Burner Flame -->
          <polygon points="250,5 230,45 270,45" fill="#f97316" stroke="#090a0f" stroke-width="4.5"/>
          <polygon points="250,15 238,45 262,45" fill="#fef08a"/>
        </svg>
        """
    },

    # 7. PIRATE SHIP EYEPATCH (19th-century Gulf raider dhow with skull flag & eyepatch)
    "pirate_ship_eyepatch": {
        "w": 480, "h": 440,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 440" width="480" height="440">
          <defs>
            <linearGradient id="pirateHull" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#78350f"/>
              <stop offset="40%" stop-color="#451a03"/>
              <stop offset="100%" stop-color="#1c1917"/>
            </linearGradient>
          </defs>

          <!-- Ocean Water Waves Beneath Hull -->
          <path d="M 20 380 Q 70 360 120 380 Q 170 400 220 380 Q 270 360 320 380 Q 370 400 420 380 Q 450 370 470 380" 
                fill="none" stroke="#0284c7" stroke-width="14" stroke-linecap="round"/>
          <path d="M 20 380 Q 70 360 120 380 Q 170 400 220 380 Q 270 360 320 380 Q 370 400 420 380" 
                fill="none" stroke="#38bdf8" stroke-width="6" stroke-linecap="round"/>

          <!-- Rugged Corsair Dhow Hull with Cel-Shaded Planks -->
          <path d="M 40 280 L 100 380 L 380 380 L 440 260 L 400 270 L 90 270 Z" 
                fill="url(#pirateHull)" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
          <line x1="80" y1="300" x2="410" y2="290" stroke="#090a0f" stroke-width="3.5"/>
          <line x1="90" y1="335" x2="395" y2="325" stroke="#090a0f" stroke-width="3.5"/>

          <!-- Specular Hull Highlight Curve -->
          <path d="M 90 275 L 400 275" stroke="rgba(255,255,255,0.3)" stroke-width="3" stroke-linecap="round"/>

          <!-- Comedic Giant Pirate Eyepatch Over Hull Prow -->
          <ellipse cx="380" cy="300" rx="28" ry="22" fill="#090a0f" stroke="#090a0f" stroke-width="5"/>
          <line x1="335" y1="280" x2="425" y2="320" stroke="#090a0f" stroke-width="6.5"/>
          <!-- Buckle on Eyepatch Strap -->
          <rect x="350" y="285" width="10" height="8" rx="2" fill="#f59e0b" stroke="#090a0f" stroke-width="2"/>

          <!-- Heavy Wooden Mast -->
          <line x1="220" y1="280" x2="220" y2="60" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>
          <line x1="220" y1="280" x2="220" y2="60" stroke="#92400e" stroke-width="10" stroke-linecap="round"/>

          <!-- Lateen Yard Arm -->
          <line x1="95" y1="290" x2="345" y2="50" stroke="#090a0f" stroke-width="10" stroke-linecap="round"/>
          <line x1="95" y1="290" x2="345" y2="50" stroke="#78350f" stroke-width="6" stroke-linecap="round"/>

          <!-- Triangular Pirate Sail (Torn/Patched) -->
          <polygon points="105,280 335,60 220,260" fill="#fef3c7" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
          <!-- Stitched Red Patch on Sail -->
          <rect x="185" y="155" width="36" height="28" fill="#b91c1c" stroke="#090a0f" stroke-width="3"/>
          <line x1="185" y1="169" x2="221" y2="169" stroke="#ffffff" stroke-width="2" stroke-dasharray="3,2"/>

          <!-- Black Jolly Roger Pirate Flag at Masthead -->
          <rect x="220" y="45" width="95" height="58" fill="#090a0f" stroke="#090a0f" stroke-width="5"/>
          <!-- Cartoon Skull and Crossed Bones -->
          <circle cx="265" cy="68" r="13" fill="#ffffff"/>
          <rect x="259" y="77" width="12" height="9" rx="2" fill="#ffffff"/>
          <circle cx="261" cy="67" r="3" fill="#090a0f"/>
          <circle cx="269" cy="67" r="3" fill="#090a0f"/>
          <!-- Crossed Scimitars/Bones -->
          <line x1="245" y1="88" x2="285" y2="60" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round"/>
          <line x1="245" y1="60" x2="285" y2="88" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round"/>

          <!-- Boarding Grappling Hook -->
          <path d="M 135 340 Q 125 390 105 380" fill="none" stroke="#94a3b8" stroke-width="6.5" stroke-linecap="round"/>
        </svg>
        """
    },

    # 8. OIL VALVE GIANT (Industrial cast-iron valve labeled 'OIL RELIANCE' in OFF/CLOSED position)
    "oil_valve_giant": {
        "w": 400, "h": 460,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 460" width="400" height="460">
          <defs>
            <linearGradient id="ironGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#1e293b"/>
              <stop offset="40%" stop-color="#475569"/>
              <stop offset="70%" stop-color="#64748b"/>
              <stop offset="100%" stop-color="#0f172a"/>
            </linearGradient>
            <linearGradient id="redWheel" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#ef4444"/>
              <stop offset="50%" stop-color="#dc2626"/>
              <stop offset="100%" stop-color="#991b1b"/>
            </linearGradient>
          </defs>

          <!-- Heavy Horizontal Oil Pipeline Pipe -->
          <rect x="10" y="270" width="380" height="110" rx="8" fill="url(#ironGrad)" stroke="#090a0f" stroke-width="6.5"/>
          <line x1="10" y1="290" x2="390" y2="290" stroke="rgba(255,255,255,0.3)" stroke-width="4"/>

          <!-- Left & Right Flange Collars with Industrial Bolts -->
          <rect x="25" y="255" width="28" height="140" rx="4" fill="#334155" stroke="#090a0f" stroke-width="6.5"/>
          <rect x="345" y="255" width="28" height="140" rx="4" fill="#334155" stroke="#090a0f" stroke-width="6.5"/>
          <g fill="#090a0f">
            <circle cx="39" cy="275" r="5"/> <circle cx="39" cy="325" r="5"/> <circle cx="39" cy="375" r="5"/>
            <circle cx="359" cy="275" r="5"/> <circle cx="359" cy="325" r="5"/> <circle cx="359" cy="375" r="5"/>
          </g>

          <!-- Central Valve Housing -->
          <rect x="135" y="230" width="130" height="170" rx="12" fill="url(#ironGrad)" stroke="#090a0f" stroke-width="6.5"/>

          <!-- Valve Stem Shaft with Threading -->
          <rect x="180" y="110" width="40" height="130" fill="#94a3b8" stroke="#090a0f" stroke-width="6.5"/>
          <line x1="180" y1="130" x2="220" y2="130" stroke="#090a0f" stroke-width="3.5"/>
          <line x1="180" y1="150" x2="220" y2="150" stroke="#090a0f" stroke-width="3.5"/>
          <line x1="180" y1="170" x2="220" y2="170" stroke="#090a0f" stroke-width="3.5"/>

          <!-- Massive Crimson Handwheel Rim -->
          <ellipse cx="200" cy="100" rx="150" ry="38" fill="none" stroke="#090a0f" stroke-width="26"/>
          <ellipse cx="200" cy="100" rx="150" ry="38" fill="none" stroke="url(#redWheel)" stroke-width="18"/>
          <!-- Wheel Spokes -->
          <line x1="60" y1="100" x2="340" y2="100" stroke="#090a0f" stroke-width="8"/>
          <line x1="200" y1="65" x2="200" y2="135" stroke="#090a0f" stroke-width="8"/>
          <circle cx="200" cy="100" r="22" fill="#090a0f" stroke="#090a0f" stroke-width="4"/>
          <circle cx="200" cy="100" r="14" fill="#fbbf24"/>

          <!-- Heavy Iron Plate: 'OIL RELIANCE: OFF' -->
          <rect x="145" y="275" width="110" height="60" rx="6" fill="#090a0f" stroke="#e2e8f0" stroke-width="3"/>
          <text x="152" y="298" font-family="Arial, sans-serif" font-weight="900" font-size="11" fill="#f8fafc">OIL RELIANCE</text>
          <rect x="165" y="306" width="70" height="22" rx="4" fill="#dc2626"/>
          <text x="182" y="322" font-family="Arial, sans-serif" font-weight="900" font-size="14" fill="#ffffff">OFF</text>
        </svg>
        """
    },

    # 9. SOLAR FARM PANEL (Futuristic desert photovoltaic array)
    "solar_farm_panel": {
        "w": 460, "h": 360,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 360" width="460" height="360">
          <defs>
            <linearGradient id="solarCell" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#0284c7"/>
              <stop offset="40%" stop-color="#0369a1"/>
              <stop offset="80%" stop-color="#075985"/>
              <stop offset="100%" stop-color="#082f49"/>
            </linearGradient>
          </defs>

          <!-- Hydraulic Tilt Stanchion Base -->
          <polygon points="210,230 250,230 270,340 190,340" fill="#64748b" stroke="#090a0f" stroke-width="6.5"/>
          <rect x="170" y="335" width="120" height="20" rx="4" fill="#334155" stroke="#090a0f" stroke-width="6.5"/>

          <!-- Massive Solar Photovoltaic Grid Frame -->
          <polygon points="50,190 410,190 380,40 80,40" fill="url(#solarCell)" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>

          <!-- Cell Divider Grid (Silver Wire Traces) -->
          <g stroke="#38bdf8" stroke-width="3.5" opacity="0.85">
            <line x1="72" y1="90" x2="388" y2="90"/>
            <line x1="62" y1="140" x2="398" y2="140"/>
            <line x1="140" y1="40" x2="125" y2="190"/>
            <line x1="200" y1="40" x2="190" y2="190"/>
            <line x1="260" y1="40" x2="270" y2="190"/>
            <line x1="320" y1="40" x2="335" y2="190"/>
          </g>

          <!-- Specular Glare Reflection on Solar Glass -->
          <polygon points="90,45 130,45 220,185 180,185" fill="rgba(255,255,255,0.4)" stroke="none"/>
        </svg>
        """
    },

    # 10. NUCLEAR ATOM PLANT (Barakah clean dome with glowing atomic orbits)
    "nuclear_atom_plant": {
        "w": 440, "h": 460,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 460" width="440" height="460">
          <defs>
            <radialGradient id="atomGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#00f2fe"/>
              <stop offset="60%" stop-color="#0ea5e9"/>
              <stop offset="100%" stop-color="#0284c7" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="domeGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#cbd5e1"/>
              <stop offset="50%" stop-color="#f8fafc"/>
              <stop offset="100%" stop-color="#94a3b8"/>
            </linearGradient>
          </defs>

          <!-- Clean Concrete Containment Dome -->
          <path d="M 70 390 C 70 180, 370 180, 370 390 Z" fill="url(#domeGrad)" stroke="#090a0f" stroke-width="6.5"/>
          <rect x="50" y="380" width="340" height="35" rx="6" fill="#64748b" stroke="#090a0f" stroke-width="6.5"/>

          <!-- Glowing Atomic Core & Orbital Electron Rings -->
          <circle cx="220" cy="180" r="70" fill="url(#atomGlow)"/>
          <ellipse cx="220" cy="180" rx="90" ry="26" fill="none" stroke="#00f2fe" stroke-width="4.5" transform="rotate(-30 220 180)"/>
          <ellipse cx="220" cy="180" rx="90" ry="26" fill="none" stroke="#00f2fe" stroke-width="4.5" transform="rotate(30 220 180)"/>
          <circle cx="220" cy="180" r="16" fill="#00f2fe" stroke="#090a0f" stroke-width="3"/>
          <circle cx="220" cy="180" r="9" fill="#ffffff"/>

          <!-- Orbiting Cyan Electrons -->
          <circle cx="150" cy="140" r="6" fill="#38bdf8" stroke="#090a0f" stroke-width="2"/>
          <circle cx="290" cy="220" r="6" fill="#38bdf8" stroke="#090a0f" stroke-width="2"/>
        </svg>
        """
    },

    # 11. CRYING OIL BARREL (Comedic blue/black oil drum crying tears)
    "crying_oil_barrel": {
        "w": 340, "h": 420,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 420" width="340" height="420">
          <defs>
            <linearGradient id="barrelGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#1e3a8a"/>
              <stop offset="50%" stop-color="#2563eb"/>
              <stop offset="100%" stop-color="#172554"/>
            </linearGradient>
          </defs>

          <!-- Steel Oil Drum Barrel -->
          <rect x="70" y="110" width="200" height="270" rx="18" fill="url(#barrelGrad)" stroke="#090a0f" stroke-width="6.5"/>
          <!-- Barrel Rib Rings -->
          <line x1="70" y1="170" x2="270" y2="170" stroke="#090a0f" stroke-width="5"/>
          <line x1="70" y1="240" x2="270" y2="240" stroke="#090a0f" stroke-width="5"/>
          <line x1="70" y1="310" x2="270" y2="310" stroke="#090a0f" stroke-width="5"/>

          <!-- Comedic Crying Cartoon Face on Barrel -->
          <!-- Sad Closed Eyes -->
          <path d="M 120 180 Q 135 165 150 180" fill="none" stroke="#090a0f" stroke-width="5" stroke-linecap="round"/>
          <path d="M 190 180 Q 205 165 220 180" fill="none" stroke="#090a0f" stroke-width="5" stroke-linecap="round"/>
          <!-- Crying Tears Gushing Out -->
          <path d="M 120 185 Q 100 240 115 310" fill="none" stroke="#38bdf8" stroke-width="8" stroke-linecap="round"/>
          <path d="M 220 185 Q 240 240 225 310" fill="none" stroke="#38bdf8" stroke-width="8" stroke-linecap="round"/>
          <!-- Sad Wavy Mouth -->
          <path d="M 150 220 Q 170 205 190 220" fill="none" stroke="#090a0f" stroke-width="5" stroke-linecap="round"/>

          <!-- Puddle Beneath Barrel -->
          <ellipse cx="170" cy="385" rx="120" ry="18" fill="#0284c7" opacity="0.6"/>
        </svg>
        """
    },

    # 12. GLOWING BLUEPRINT MAP (Rolled architectural blueprint 'SUPER EMIRATES')
    "glowing_blueprint_map": {
        "w": 380, "h": 320,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 320" width="380" height="320">
          <!-- Rolled Architectural Blueprint -->
          <path d="M 50 60 C 80 40, 300 40, 330 60 L 310 270 C 280 290, 60 290, 40 270 Z" 
                fill="#0284c7" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
          <!-- Grid Lines on Blueprint -->
          <g stroke="#38bdf8" stroke-width="2" opacity="0.5">
            <line x1="80" y1="80" x2="300" y2="80"/>
            <line x1="75" y1="120" x2="295" y2="120"/>
            <line x1="70" y1="160" x2="290" y2="160"/>
            <line x1="65" y1="200" x2="285" y2="200"/>
            <line x1="120" y1="60" x2="110" y2="260"/>
            <line x1="180" y1="60" x2="170" y2="260"/>
            <line x1="240" y1="60" x2="230" y2="260"/>
          </g>
          <!-- Blueprint Architectural Sketch -->
          <polygon points="150,110 230,110 250,220 130,220" fill="none" stroke="#ffffff" stroke-width="3.5"/>
          <text x="140" y="245" font-family="Arial, sans-serif" font-weight="900" font-size="14" fill="#ffffff">SUPER EMIRATES</text>
        </svg>
        """
    },

    # 13. GIANT OYSTER PEARL (Pried open sea clam shell with glowing gold pearl)
    "giant_oyster_pearl": {
        "w": 400, "h": 360,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 360" width="400" height="360">
          <defs>
            <radialGradient id="pearlGlow" cx="35%" cy="30%" r="65%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="40%" stop-color="#fef08a"/>
              <stop offset="80%" stop-color="#fde047"/>
              <stop offset="100%" stop-color="#eab308"/>
            </radialGradient>
          </defs>

          <!-- Bottom Clam Shell -->
          <path d="M 60 250 C 60 330, 340 330, 340 250 C 340 220, 60 220, 60 250 Z" 
                fill="#475569" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
          <path d="M 80 250 C 80 310, 320 310, 320 250 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="3.5"/>

          <!-- Top Pried Open Clam Shell -->
          <path d="M 60 230 C 60 110, 340 110, 340 230 C 340 250, 60 250, 60 230 Z" 
                fill="#334155" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>

          <!-- Giant Glowing Natural Pearl -->
          <circle cx="200" cy="220" r="48" fill="url(#pearlGlow)" stroke="#090a0f" stroke-width="5"/>
          <circle cx="185" cy="205" r="14" fill="#ffffff"/>
          <path d="M 175 160 L 175 145 M 225 160 L 225 145 M 150 190 L 135 190 M 250 190 L 265 190" stroke="#fde047" stroke-width="4" stroke-linecap="round"/>
        </svg>
        """
    },

    # 14. BURJ AL ARAB HOTEL (Sail-shaped luxury hotel tower on sea island)
    "burj_al_arab_hotel": {
        "w": 360, "h": 500,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 500" width="360" height="500">
          <!-- Island Base -->
          <ellipse cx="180" cy="460" rx="140" ry="24" fill="#fef08a" stroke="#090a0f" stroke-width="6.5"/>

          <!-- Sail Curve Body -->
          <path d="M 120 450 C 120 240, 260 140, 260 100 L 120 450 Z" 
                fill="#f8fafc" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
          <!-- Outer Spine Truss -->
          <path d="M 120 450 L 120 80 L 260 100" fill="none" stroke="#090a0f" stroke-width="8" stroke-linecap="round"/>
          <path d="M 120 80 L 120 40" stroke="#090a0f" stroke-width="6"/>

          <!-- Cantilever Helipad Deck -->
          <ellipse cx="230" cy="180" rx="35" ry="12" fill="#38bdf8" stroke="#090a0f" stroke-width="4.5"/>
          <line x1="120" y1="190" x2="230" y2="180" stroke="#090a0f" stroke-width="5"/>
        </svg>
        """
    },

    # 15. ROBOTIC CAMEL MARS (Cybernetic white/gold mecha-camel on red Mars sand)
    "robotic_camel_mars": {
        "w": 400, "h": 360,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 360" width="400" height="360">
          <!-- Cybernetic Chassis Torso & Hump -->
          <path d="M 110 210 C 90 160, 160 120, 210 120 C 260 120, 310 160, 290 210 Z" 
                fill="#f8fafc" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>
          <!-- Gold Trim Plate -->
          <circle cx="210" cy="155" r="24" fill="#fbbf24" stroke="#090a0f" stroke-width="3.5"/>

          <!-- Neck & Head with Visor -->
          <path d="M 110 180 L 70 100 L 40 100 L 40 120 L 70 140 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="5"/>
          <rect x="42" y="104" width="22" height="10" rx="3" fill="#00f2fe" stroke="#090a0f" stroke-width="2"/>

          <!-- Mechanical Piston Legs -->
          <g stroke="#090a0f" stroke-width="6.5" stroke-linecap="round">
            <line x1="120" y1="210" x2="110" y2="330"/>
            <line x1="150" y1="210" x2="140" y2="330"/>
            <line x1="260" y1="210" x2="270" y2="330"/>
            <line x1="290" y1="210" x2="300" y2="330"/>
          </g>
          <!-- Pod Feet -->
          <rect x="95" y="325" width="25" height="12" rx="3" fill="#64748b" stroke="#090a0f" stroke-width="3"/>
          <rect x="125" y="325" width="25" height="12" rx="3" fill="#64748b" stroke="#090a0f" stroke-width="3"/>
          <rect x="255" y="325" width="25" height="12" rx="3" fill="#64748b" stroke="#090a0f" stroke-width="3"/>
          <rect x="285" y="325" width="25" height="12" rx="3" fill="#64748b" stroke="#090a0f" stroke-width="3"/>
        </svg>
        """
    },

    # 16. MONEY MATTRESS CASH (Bulging lumpy mattress stuffed with cash)
    "money_mattress_cash": {
        "w": 400, "h": 320,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 320" width="400" height="320">
          <!-- Bulging Lumpy Mattress -->
          <rect x="60" y="150" width="280" height="120" rx="20" fill="#fef3c7" stroke="#090a0f" stroke-width="6.5"/>
          <!-- Quilted Tufting Buttons -->
          <g fill="#78350f">
            <circle cx="120" cy="180" r="5"/><circle cx="200" cy="180" r="5"/><circle cx="280" cy="180" r="5"/>
            <circle cx="160" cy="220" r="5"/><circle cx="240" cy="220" r="5"/>
          </g>
          <!-- Stacks of Green Cash Bills Bursting Out of Torn Seam -->
          <rect x="80" y="125" width="60" height="30" rx="3" fill="#22c55e" stroke="#090a0f" stroke-width="3.5" transform="rotate(-15 80 125)"/>
          <rect x="240" y="120" width="60" height="30" rx="3" fill="#22c55e" stroke="#090a0f" stroke-width="3.5" transform="rotate(18 240 120)"/>
          <rect x="180" y="110" width="65" height="32" rx="3" fill="#16a34a" stroke="#090a0f" stroke-width="3.5"/>
        </svg>
        """
    },

    # 17. WATER WELL DRIPPING (Desert stone well with dripping leaky bucket)
    "water_well_dripping": {
        "w": 380, "h": 400,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 400" width="380" height="400">
          <!-- Circular Stone Well Base -->
          <ellipse cx="190" cy="330" rx="120" ry="40" fill="#64748b" stroke="#090a0f" stroke-width="6.5"/>
          <ellipse cx="190" cy="315" rx="90" ry="24" fill="#0f172a" stroke="#090a0f" stroke-width="4.5"/>

          <!-- Timber Roof Posts -->
          <line x1="100" y1="320" x2="100" y2="120" stroke="#090a0f" stroke-width="12" stroke-linecap="round"/>
          <line x1="100" y1="320" x2="100" y2="120" stroke="#78350f" stroke-width="6" stroke-linecap="round"/>
          <line x1="280" y1="320" x2="280" y2="120" stroke="#090a0f" stroke-width="12" stroke-linecap="round"/>
          <line x1="280" y1="320" x2="280" y2="120" stroke="#78350f" stroke-width="6" stroke-linecap="round"/>

          <!-- Gable Roof -->
          <polygon points="190,50 60,120 320,120" fill="#b45309" stroke="#090a0f" stroke-width="6.5" stroke-linejoin="round"/>

          <!-- Suspended Wooden Bucket -->
          <line x1="190" y1="120" x2="190" y2="230" stroke="#090a0f" stroke-width="4"/>
          <polygon points="175,230 205,230 210,265 170,265" fill="#92400e" stroke="#090a0f" stroke-width="4.5"/>
          <!-- Leaky Water Drip -->
          <circle cx="190" cy="285" r="5" fill="#38bdf8"/>
        </svg>
        """
    },

    # 18. RUBBER STAMP TREATY (Red wooden notary stamp)
    "rubber_stamp_treaty": {
        "w": 320, "h": 360,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 360" width="320" height="360">
          <!-- Carved Wooden Handle -->
          <path d="M 140 70 C 140 40, 180 40, 180 70 L 175 180 L 145 180 Z" fill="#991b1b" stroke="#090a0f" stroke-width="6.5"/>
          <circle cx="160" cy="50" r="22" fill="#dc2626" stroke="#090a0f" stroke-width="5"/>

          <!-- Brass Ferrule Collar -->
          <rect x="135" y="180" width="50" height="24" rx="4" fill="#fbbf24" stroke="#090a0f" stroke-width="5"/>

          <!-- Heavy Stamp Base Mount -->
          <polygon points="110,240 210,240 235,280 85,280" fill="#b91c1c" stroke="#090a0f" stroke-width="6.5"/>
          <rect x="75" y="280" width="170" height="25" rx="5" fill="#090a0f"/>
        </svg>
        """
    },

    # 19. VINTAGE CATHEDRAL TUBE RADIO (Hero Espionage / WWII / Broadcast Prop)
    "vintage_cathedral_radio": {
        "w": 360, "h": 420,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 420" width="360" height="420">
          <defs>
            <linearGradient id="radioWood" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#451a03"/>
              <stop offset="50%" stop-color="#290f02"/>
              <stop offset="100%" stop-color="#1c0a01"/>
            </linearGradient>
            <radialGradient id="dialGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="60%" stop-color="#f59e0b"/>
              <stop offset="100%" stop-color="#b45309" stop-opacity="0.8"/>
            </radialGradient>
          </defs>
          <g transform="translate(90, 80)">
            <path d="M 10 240 L 10 100 C 10 20 170 20 170 100 L 170 240 Z" fill="url(#radioWood)" stroke="#090503" stroke-width="7" stroke-linejoin="round"/>
            <path d="M 24 232 L 24 105 C 24 45 156 45 156 105 L 156 232 Z" fill="#290f02" stroke="#1c0a01" stroke-width="5"/>
            <rect x="0" y="232" width="180" height="22" rx="4" fill="#271004" stroke="#090503" stroke-width="6"/>
            <circle cx="90" cy="95" r="42" fill="#78350f" stroke="#090503" stroke-width="5"/>
            <circle cx="90" cy="95" r="36" fill="url(#dialGlow)" opacity="0.65"/>
            <path d="M 90 55 L 90 135 M 50 95 L 130 95 M 62 67 L 118 123 M 118 67 L 62 123" stroke="#1c0a01" stroke-width="5" stroke-linecap="round"/>
            <rect x="38" y="155" width="104" height="28" rx="5" fill="#fef08a" stroke="#090503" stroke-width="4"/>
            <rect x="38" y="155" width="104" height="28" rx="5" fill="url(#dialGlow)" opacity="0.8"/>
            <path d="M 48 175 L 48 163 M 62 175 L 62 167 M 76 175 L 76 161 M 90 175 L 90 167 M 104 175 L 104 161 M 118 175 L 118 167 M 132 175 L 132 163" stroke="#451a03" stroke-width="2.5"/>
            <line x1="98" y1="157" x2="98" y2="181" stroke="#dc2626" stroke-width="3.5"/>
            <circle cx="52" cy="210" r="10" fill="#1c0a01" stroke="#090503" stroke-width="3"/>
            <circle cx="90" cy="210" r="8" fill="#1c0a01" stroke="#090503" stroke-width="3"/>
            <circle cx="128" cy="210" r="10" fill="#1c0a01" stroke="#090503" stroke-width="3"/>
            <path d="M 155 55 C 195 20 210 -45 185 -95" stroke="#b45309" stroke-width="3.5" fill="none" stroke-dasharray="6 3"/>
          </g>
        </svg>
        """
    },

    # 20. WAX CANDLE STUB WITH GLOWING FLAME (Historical Illumination)
    "wax_candle_stub": {
        "w": 180, "h": 220,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220" width="180" height="220">
          <ellipse cx="90" cy="190" rx="65" ry="16" fill="#020305" opacity="0.75"/>
          <rect x="70" y="110" width="40" height="75" rx="4" fill="#f5f5f4" stroke="#090a0f" stroke-width="6"/>
          <ellipse cx="90" cy="110" rx="20" ry="7" fill="#e7e5e4" stroke="#090a0f" stroke-width="5"/>
          <path d="M 75 125 C 72 145 74 165 72 180" stroke="#d6d3d1" stroke-width="4" fill="none"/>
          <line x1="90" y1="110" x2="90" y2="92" stroke="#090a0f" stroke-width="4.5" stroke-linecap="round"/>
          <circle cx="90" cy="72" r="32" fill="#fbbf24" opacity="0.35"/>
          <path d="M 90 52 C 102 68 100 82 90 86 C 80 82 78 68 90 52 Z" fill="#fde047" stroke="#b45309" stroke-width="2"/>
          <path d="M 90 58 C 96 70 95 80 90 83 C 85 80 84 70 90 58 Z" fill="#ffffff"/>
        </svg>
        """
    },

    # 21. TREATY TABLE & UNROLLED SCROLL (Diplomatic / Colonial Politics)
    "treaty_quill_scroll": {
        "w": 420, "h": 320,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 320" width="420" height="320">
          <!-- Mahogany Tabletop -->
          <ellipse cx="210" cy="270" rx="190" ry="40" fill="#2d150b" stroke="#090a0f" stroke-width="6.5"/>
          <!-- Rolled Parchment Scroll -->
          <path d="M 70 210 C 60 170 120 160 150 160 L 320 160 C 350 160 370 190 350 220 L 100 220 Z" fill="#fef3c7" stroke="#090a0f" stroke-width="6"/>
          <!-- Wax Notary Seal -->
          <circle cx="310" cy="190" r="16" fill="#dc2626" stroke="#090a0f" stroke-width="4"/>
          <!-- Red Ribbon Tails -->
          <path d="M 310 200 L 300 230 M 315 200 L 325 230" stroke="#991b1b" stroke-width="5" stroke-linecap="round"/>
          <!-- Feather Quill & Inkwell -->
          <rect x="90" y="220" width="30" height="35" rx="6" fill="#1e293b" stroke="#090a0f" stroke-width="5"/>
          <path d="M 105 220 L 160 110 C 170 90 195 80 185 105 L 110 225 Z" fill="#ffffff" stroke="#090a0f" stroke-width="5"/>
        </svg>
        """
    },

    # 22. MARKET CRASH BOARD (Economic Crisis / Wall Street)
    "market_crash_board": {
        "w": 380, "h": 440,
        "svg": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 440" width="380" height="440">
          <rect x="30" y="20" width="320" height="380" rx="10" fill="#0f172a" stroke="#090a0f" stroke-width="7"/>
          <!-- Grid Lines -->
          <line x1="30" y1="100" x2="350" y2="100" stroke="#1e293b" stroke-width="3"/>
          <line x1="30" y1="180" x2="350" y2="180" stroke="#1e293b" stroke-width="3"/>
          <line x1="30" y1="260" x2="350" y2="260" stroke="#1e293b" stroke-width="3"/>
          <line x1="30" y1="340" x2="350" y2="340" stroke="#1e293b" stroke-width="3"/>
          <!-- Plummeting Red Graph Arrow -->
          <path d="M 50 80 L 120 120 L 190 90 L 260 220 L 320 370" fill="none" stroke="#ef4444" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
          <polygon points="320,390 300,350 340,355" fill="#ef4444" stroke="#090a0f" stroke-width="4"/>
          <!-- Big Bold Label -->
          <text x="50" y="65" font-family="Arial, sans-serif" font-weight="900" font-size="28" fill="#f87171">MARKET CRASH</text>
        </svg>
        """
    }
}


def synthesize_dynamic_prop(prop_name, target_dir):
    """
    Dynamically synthesizes a broadcast-grade OverSimplified vector SVG
    for any arbitrary, topic-subjective prop not present in NARRATIVE_PROPS.
    """
    out_dir = target_dir if target_dir else SPRITES_DIR
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{prop_name}.png")

    clean_label = prop_name.replace("_", " ").upper()
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 380" width="340" height="380">
      <defs>
        <linearGradient id="propGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#3b82f6"/>
          <stop offset="50%" stop-color="#1d4ed8"/>
          <stop offset="100%" stop-color="#172554"/>
        </linearGradient>
      </defs>
      <!-- Ground Contact Shadow -->
      <ellipse cx="170" cy="350" rx="120" ry="24" fill="#020305" opacity="0.85"/>
      <!-- Main Prop Silhouette -->
      <rect x="60" y="80" width="220" height="250" rx="14" fill="url(#propGrad)" stroke="#090a0f" stroke-width="7"/>
      <rect x="75" y="95" width="190" height="220" rx="10" fill="#1e293b" stroke="#090a0f" stroke-width="4"/>
      <!-- Detail Line & Emblem -->
      <circle cx="170" cy="180" r="48" fill="#fbbf24" stroke="#090a0f" stroke-width="6"/>
      <text x="170" y="280" font-family="Arial, sans-serif" font-weight="900" font-size="18" fill="#ffffff" text-anchor="middle">
        {clean_label}
      </text>
    </svg>
    """
    try:
        render_svg_to_png(svg_content, out_file, width=420, height=460)
        print(f"  ✨ Dynamically synthesized topic prop: {prop_name}.png")
        return out_file
    except Exception as e:
        print(f"⚠️ Error synthesizing dynamic prop {prop_name}: {e}")
        return None



def render_svg_to_png(svg_content, out_png, width=500, height=700):
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: transparent !important;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }}
  svg {{
    max-width: 95%;
    max-height: 95%;
    filter: drop-shadow(0px 8px 16px rgba(0,0,0,0.35));
  }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
    temp_html = os.path.abspath("temp_narrative_render.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

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

    im = Image.open(abs_out)
    bbox = im.getbbox()
    if bbox:
        pad = 8
        box = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
               min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad))
        im = im.crop(box)
        im.save(abs_out)
    return abs_out


def synthesize_all_props(target_dir=None, requested_props=None):
    out_dir = target_dir if target_dir else SPRITES_DIR
    os.makedirs(out_dir, exist_ok=True)
    created = []

    if requested_props:
        print(f"🎨 Synthesizing {len(requested_props)} Topic-Specific Props into {out_dir}...")
        for name in requested_props:
            out_file = os.path.join(out_dir, f"{name}.png")
            if os.path.exists(out_file):
                created.append(out_file)
                continue
            if name in NARRATIVE_PROPS:
                spec = NARRATIVE_PROPS[name]
                render_svg_to_png(spec["svg"], out_file, width=spec["w"] + 80, height=spec["h"] + 80)
            else:
                synthesize_dynamic_prop(name, out_dir)
            created.append(out_file)
        return created

    print(f"🎨 Synthesizing {len(NARRATIVE_PROPS)} Narrative Vector Props into {out_dir}...")
    for name, spec in NARRATIVE_PROPS.items():
        out_file = os.path.join(out_dir, f"{name}.png")
        if not os.path.exists(out_file):
            render_svg_to_png(spec["svg"], out_file, width=spec["w"] + 80, height=spec["h"] + 80)
            print(f"  ✅ Created {name}.png")
        created.append(out_file)
    return created


if __name__ == "__main__":
    synthesize_all_props()
