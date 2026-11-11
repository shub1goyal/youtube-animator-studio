"""
UAE Historical Map Generator (16:9 Landscape - 1920x1080)
Generates vector historical maps of the 7 Emirates, Trucial States,
Persian Gulf pearl beds, and the 1971 Unification moment.
"""

import os
import argparse

def generate_uae_map(output_path="uae_history_map.svg"):
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
    <defs>
        <!-- Vintage Desert Sand & Parchment Filter -->
        <filter id="desert-texture" x="0%" y="0%" width="100%" height="100%">
            <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="4" result="noise"/>
            <feDiffuseLighting in="noise" lighting-color="#eed8ae" surfaceScale="2" result="light">
                <feDistantLight azimuth="55" elevation="65" />
            </feDiffuseLighting>
            <feBlend mode="multiply" in="SourceGraphic" in2="light" />
        </filter>

        <!-- Territory Drop Shadow -->
        <filter id="emirate-shadow" x="-5%" y="-5%" width="110%" height="110%">
            <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000000" flood-opacity="0.35"/>
        </filter>

        <!-- Gulf Water Glow -->
        <radialGradient id="water-grad" cx="50%" cy="30%" r="80%">
            <stop offset="0%" stop-color="#1e4e5f" />
            <stop offset="100%" stop-color="#0f2b35" />
        </radialGradient>

        <!-- Sand Dune Gradient -->
        <linearGradient id="dune-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#e2c290" />
            <stop offset="100%" stop-color="#c99f63" />
        </linearGradient>

        <style>
            .emirate {
                transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
            }
            .oil-pulse {
                animation: oilGush 2.5s infinite ease-out;
            }
            @keyframes oilGush {
                0% { r: 6px; opacity: 1; }
                100% { r: 35px; opacity: 0; }
            }
            .pearl-twinkle {
                animation: twinkle 3s infinite ease-in-out;
            }
            @keyframes twinkle {
                0%, 100% { opacity: 0.6; transform: scale(1); }
                50% { opacity: 1; transform: scale(1.3); }
            }
        </style>
    </defs>

    <!-- Deep Arabian Gulf Ocean Background -->
    <rect width="1920" height="1080" fill="url(#water-grad)" />

    <!-- Wave Contours in Persian Gulf -->
    <g stroke="#2a6275" stroke-width="2" fill="none" opacity="0.4">
        <path d="M 100 200 Q 300 180 500 220 T 900 210 T 1300 230" />
        <path d="M 200 350 Q 400 320 600 360 T 1000 340 T 1400 360" />
        <path d="M 800 120 Q 1000 100 1200 130 T 1600 110" />
    </g>

    <!-- Arabian Peninsula Landmass (Base Desert) -->
    <g id="landmass" filter="url(#desert-texture)">
        <!-- Saudi Arabia / Empty Quarter & Oman Base -->
        <path d="M 0 500 C 200 480, 450 550, 600 620 C 750 680, 950 600, 1100 520 C 1250 450, 1350 350, 1420 220 C 1450 180, 1490 140, 1540 180 C 1600 240, 1680 400, 1720 550 C 1750 680, 1820 850, 1920 950 L 1920 1080 L 0 1080 Z" 
              fill="url(#dune-grad)" stroke="#1f2937" stroke-width="4" />
    </g>

    <!-- The 7 Emirates & Trucial States Layers -->
    <g id="emirates" filter="url(#emirate-shadow)">
        <!-- 1. Abu Dhabi (Vast Western Emirate - 86% of land) -->
        <path id="abu-dhabi" class="emirate" 
              d="M 280 620 C 420 580, 620 660, 850 660 C 1020 660, 1140 600, 1180 540 C 1120 660, 1020 820, 850 880 C 650 920, 400 880, 280 780 Z" 
              fill="#15803d" stroke="#fef08a" stroke-width="4" opacity="0.92" />

        <!-- 2. Dubai (Commercial Heart on Gulf Coast) -->
        <path id="dubai" class="emirate" 
              d="M 1180 540 C 1220 500, 1280 460, 1320 440 C 1310 500, 1260 560, 1220 580 Z" 
              fill="#0284c7" stroke="#ffffff" stroke-width="3" opacity="0.95" />

        <!-- 3. Sharjah (Spans Gulf to Gulf of Oman) -->
        <path id="sharjah" class="emirate" 
              d="M 1320 440 C 1350 410, 1370 380, 1390 360 C 1410 400, 1390 480, 1340 500 Z" 
              fill="#dc2626" stroke="#ffffff" stroke-width="2.5" opacity="0.92" />

        <!-- 4. Ajman (Compact Coastal Enclave) -->
        <path id="ajman" class="emirate" 
              d="M 1340 420 C 1360 410, 1370 420, 1360 440 Z" 
              fill="#f59e0b" stroke="#ffffff" stroke-width="2" />

        <!-- 5. Umm Al Quwain -->
        <path id="umm-al-quwain" class="emirate" 
              d="M 1370 380 C 1390 360, 1400 370, 1390 390 Z" 
              fill="#8b5cf6" stroke="#ffffff" stroke-width="2" />

        <!-- 6. Ras Al Khaimah (Northern Musandam Gateway) -->
        <path id="ras-al-khaimah" class="emirate" 
              d="M 1390 360 C 1420 300, 1440 250, 1450 200 C 1470 230, 1460 320, 1420 350 Z" 
              fill="#10b981" stroke="#ffffff" stroke-width="3" opacity="0.94" />

        <!-- 7. Fujairah (Facing Gulf of Oman / Indian Ocean) -->
        <path id="fujairah" class="emirate" 
              d="M 1430 350 C 1470 380, 1500 450, 1490 520 C 1460 500, 1440 430, 1420 390 Z" 
              fill="#e11d48" stroke="#ffffff" stroke-width="3" opacity="0.94" />
    </g>

    <!-- Historic Pearl Diving Oyster Beds (Offshore Gulf) -->
    <g id="pearl-banks" transform="translate(700, 360)" class="pearl-twinkle">
        <circle cx="0" cy="0" r="8" fill="#ffffff" stroke="#38bdf8" stroke-width="2" />
        <circle cx="40" cy="-30" r="7" fill="#ffffff" stroke="#38bdf8" stroke-width="2" />
        <circle cx="90" cy="15" r="9" fill="#ffffff" stroke="#38bdf8" stroke-width="2" />
        <text x="0" y="35" font-family="'Cinzel', serif, Georgia" font-size="20" fill="#bae6fd" font-weight="bold">HISTORIC PEARL BANKS (1800s)</text>
    </g>

    <!-- 1958/1962 Oil Strike Marker (Abu Dhabi - Bab & Umm Shaif) -->
    <g id="oil-strike-marker" transform="translate(620, 720)">
        <circle cx="0" cy="0" r="12" fill="#000000" stroke="#facc15" stroke-width="3" />
        <circle class="oil-pulse" cx="0" cy="0" r="10" fill="none" stroke="#facc15" stroke-width="3" />
        <!-- Oil Derrick Icon -->
        <path d="M -15 25 L 0 -25 L 15 25 Z" fill="none" stroke="#18181b" stroke-width="3" />
        <line x1="-10" y1="5" x2="10" y2="5" stroke="#18181b" stroke-width="2" />
        <line x1="-6" y1="-8" x2="6" y2="-8" stroke="#18181b" stroke-width="2" />
        <text x="30" y="5" font-family="Arial, sans-serif" font-weight="900" font-size="24" fill="#000000">1958: BLACK GOLD FOUND!</text>
    </g>

    <!-- Strait of Hormuz Maritime Label -->
    <g transform="translate(1550, 130)">
        <text font-family="'Georgia', serif" font-weight="bold" font-size="28" fill="#93c5fd" letter-spacing="4">STRAIT OF HORMUZ</text>
        <path d="M -20 15 L 280 15" stroke="#93c5fd" stroke-width="2" stroke-dasharray="6,4" />
    </g>

    <!-- Geographic Labels -->
    <g font-family="'Georgia', 'Times New Roman', serif" font-weight="bold" fill="#ffffff">
        <text x="680" y="780" font-size="44" letter-spacing="5" filter="url(#emirate-shadow)">ABU DHABI</text>
        <text x="1170" y="470" font-size="34" letter-spacing="3" filter="url(#emirate-shadow)">DUBAI</text>
        <text x="1390" y="420" font-size="22" letter-spacing="2" filter="url(#emirate-shadow)">SHARJAH</text>
        <text x="1480" y="320" font-size="24" letter-spacing="2" filter="url(#emirate-shadow)">RAK</text>
        <text x="1510" y="470" font-size="24" letter-spacing="2" filter="url(#emirate-shadow)">FUJAIRAH</text>
        <text x="350" y="980" font-size="36" fill="#785c37" letter-spacing="6">RUB' AL KHALI (EMPTY QUARTER)</text>
    </g>

    <!-- 1971 Unification Badge (Top Left Corner) -->
    <g id="unification-badge" transform="translate(80, 80)" filter="url(#emirate-shadow)">
        <rect x="0" y="0" width="460" height="150" rx="14" fill="#18181b" opacity="0.92" stroke="#facc15" stroke-width="3" />
        <!-- UAE Flag Stripes -->
        <rect x="20" y="25" width="28" height="96" fill="#ef4444" />
        <rect x="48" y="25" width="70" height="32" fill="#22c55e" />
        <rect x="48" y="57" width="70" height="32" fill="#ffffff" />
        <rect x="48" y="89" width="70" height="32" fill="#000000" />
        <!-- Badge Text -->
        <text x="135" y="65" font-family="'Cinzel', Georgia, serif" font-weight="bold" font-size="26" fill="#facc15">DECEMBER 2, 1971</text>
        <text x="135" y="98" font-family="Arial, sans-serif" font-weight="bold" font-size="20" fill="#ffffff">THE 7 EMIRATES UNITE</text>
    </g>
</svg>
'''
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"Generated UAE Historical Map: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="uae_history_map.svg")
    args = parser.parse_args()
    generate_uae_map(args.out)
