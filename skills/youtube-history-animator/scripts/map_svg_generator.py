"""
Historical Map SVG Generator for Documentary & Explainer Animations
Generates animated-ready vector maps with vintage parchment textures, glowing borders,
Mississippi River trade paths, and modular territory layers.
"""

import os
import argparse

def generate_map_svg(output_path="historical_map.svg", theme="louisiana_1803"):
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
    <defs>
        <!-- Vintage Parchment Paper Filter -->
        <filter id="parchment-texture" x="0%" y="0%" width="100%" height="100%">
            <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="5" result="noise"/>
            <feDiffuseLighting in="noise" lighting-color="#f5e6cb" surfaceScale="2" result="light">
                <feDistantLight azimuth="45" elevation="60" />
            </feDiffuseLighting>
            <feBlend mode="multiply" in="SourceGraphic" in2="light" />
        </filter>

        <!-- Drop Shadow for Territory Borders -->
        <filter id="territory-shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.45"/>
        </filter>

        <!-- Glowing River Neon Filter -->
        <filter id="river-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="6" result="blur1" />
            <feGaussianBlur stdDeviation="14" result="blur2" />
            <feMerge>
                <feMergeNode in="blur2" />
                <feMergeNode in="blur1" />
                <feMergeNode in="SourceGraphic" />
            </feMerge>
        </filter>

        <!-- Gradient for River -->
        <linearGradient id="river-grad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#38bdf8" />
            <stop offset="50%" stop-color="#ffffff" />
            <stop offset="100%" stop-color="#0284c7" />
        </linearGradient>

        <style>
            .territory {
                transition: all 0.5s ease-in-out;
            }
            .river-path {
                stroke-dasharray: 1200;
                stroke-dashoffset: 1200;
                animation: drawRiver 3s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            @keyframes drawRiver {
                to {
                    stroke-dashoffset: 0;
                }
            }
            .barrel {
                animation: floatDown 6s infinite ease-in-out;
            }
            @keyframes floatDown {
                0% { transform: translateY(0px) rotate(0deg); }
                50% { transform: translateY(80px) rotate(15deg); }
                100% { transform: translateY(160px) rotate(0deg); }
            }
        </style>
    </defs>

    <!-- Background Ocean / Water -->
    <rect width="1080" height="1920" fill="#4a6b6d" />

    <!-- Landmass Base (Parchment Tone) -->
    <g id="continental-base" filter="url(#parchment-texture)">
        <rect width="1080" height="1920" fill="#d9cbb2" opacity="0.9" />
    </g>

    <!-- Map Contours & Mountain Sketches -->
    <g id="hand-drawn-topography" stroke="#8c7853" stroke-width="2" fill="none" opacity="0.4">
        <!-- Appalachian Mountains -->
        <path d="M 780 750 L 795 720 L 810 750 L 825 715 L 840 750" />
        <path d="M 800 820 L 815 790 L 830 820 L 845 785 L 860 820" />
        <path d="M 820 900 L 835 870 L 850 900 L 865 865 L 880 900" />
        <!-- Rocky Mountains -->
        <path d="M 280 500 L 305 460 L 330 500 L 355 450 L 380 500" />
        <path d="M 310 620 L 335 580 L 360 620 L 385 570 L 410 620" />
        <path d="M 340 760 L 365 720 L 390 760 L 415 710 L 440 760" />
    </g>

    <!-- Political Territories -->
    <g id="territories" filter="url(#territory-shadow)">
        <!-- British Canada (Top) -->
        <path id="canada" class="territory" 
              d="M 0 0 L 1080 0 L 1080 520 C 950 510, 750 580, 600 500 C 450 420, 200 480, 0 460 Z" 
              fill="#992b2b" stroke="#1f2937" stroke-width="4" opacity="0.92" />

        <!-- USA / 13 States + Northwest Territory (Right) -->
        <path id="usa" class="territory" 
              d="M 580 500 C 720 560, 920 520, 1080 530 L 1080 1250 C 950 1260, 780 1280, 650 1290 C 620 1150, 600 950, 580 850 C 560 720, 570 600, 580 500 Z" 
              fill="#3b7a8c" stroke="#1f2937" stroke-width="4" opacity="0.94" />

        <!-- Louisiana Territory (Center - Massive French Territory) -->
        <path id="louisiana" class="territory" 
              d="M 240 470 C 380 460, 500 450, 580 500 C 570 600, 560 720, 580 850 C 600 950, 620 1150, 650 1290 L 520 1340 C 460 1320, 360 1350, 310 1330 C 260 1150, 220 900, 240 470 Z" 
              fill="#223d6b" stroke="#ffffff" stroke-width="5" opacity="0.96" />

        <!-- New Spain / Mexico (Left and South) -->
        <path id="spain" class="territory" 
              d="M 0 460 C 120 470, 200 460, 240 470 C 220 900, 260 1150, 310 1330 L 0 1450 Z" 
              fill="#c97728" stroke="#1f2937" stroke-width="4" opacity="0.92" />
        
        <!-- Spanish Florida -->
        <path id="florida" class="territory" 
              d="M 650 1290 C 780 1280, 950 1260, 1080 1250 L 1080 1420 C 980 1450, 850 1480, 780 1560 C 740 1500, 700 1380, 650 1290 Z" 
              fill="#c97728" stroke="#1f2937" stroke-width="4" opacity="0.92" />
    </g>

    <!-- Mississippi River (The Core Strategic Lifeline) -->
    <g id="mississippi-river" filter="url(#river-glow)">
        <path class="river-path" 
              d="M 580 510 C 560 620, 610 740, 570 850 C 540 930, 610 1020, 590 1120 C 570 1200, 640 1280, 650 1320" 
              fill="none" stroke="url(#river-grad)" stroke-width="8" stroke-linecap="round" />
    </g>

    <!-- Strategic Port of New Orleans Marker -->
    <g id="new-orleans-marker" transform="translate(650, 1320)">
        <circle cx="0" cy="0" r="16" fill="#ef4444" stroke="#ffffff" stroke-width="4" />
        <circle cx="0" cy="0" r="6" fill="#ffffff" />
        <!-- Pulse ring -->
        <circle cx="0" cy="0" r="28" fill="none" stroke="#ef4444" stroke-width="2" opacity="0.6" />
    </g>

    <!-- Floating Trade Barrels & Crates along River -->
    <g id="river-trade-cargo" transform="translate(560, 880)" class="barrel">
        <!-- Wooden Barrel -->
        <ellipse cx="20" cy="20" rx="14" ry="18" fill="#854d0e" stroke="#111" stroke-width="2" />
        <line x1="8" y1="12" x2="32" y2="12" stroke="#d4af37" stroke-width="2" />
        <line x1="6" y1="20" x2="34" y2="20" stroke="#d4af37" stroke-width="2" />
        <line x1="8" y1="28" x2="32" y2="28" stroke="#d4af37" stroke-width="2" />
    </g>

    <g id="river-trade-cargo-2" transform="translate(585, 1080)">
        <!-- Wooden Crate -->
        <polygon points="10,10 30,5 50,12 30,17" fill="#a16207" stroke="#111" stroke-width="2" />
        <polygon points="10,10 30,17 30,35 10,28" fill="#78350f" stroke="#111" stroke-width="2" />
        <polygon points="50,12 30,17 30,35 50,30" fill="#92400e" stroke="#111" stroke-width="2" />
    </g>

    <!-- Territory Labels (Vintage Serif Typography) -->
    <g id="labels" font-family="'Georgia', 'Times New Roman', serif" font-weight="bold" fill="#ffffff">
        <text x="540" y="320" text-anchor="middle" font-size="52" letter-spacing="4" filter="url(#territory-shadow)">BRITISH NORTH AMERICA</text>
        <text x="880" y="880" text-anchor="middle" font-size="64" letter-spacing="6" filter="url(#territory-shadow)">UNITED STATES</text>
        <text x="410" y="860" text-anchor="middle" font-size="60" letter-spacing="4" filter="url(#territory-shadow)">LOUISIANA</text>
        <text x="410" y="930" text-anchor="middle" font-size="44" letter-spacing="3" opacity="0.9" filter="url(#territory-shadow)">TERRITORY</text>
        <text x="130" y="980" text-anchor="middle" font-size="54" letter-spacing="5" filter="url(#territory-shadow)">NEW SPAIN</text>
        <text x="730" y="1328" font-size="32" font-family="Arial, sans-serif" font-weight="bold" fill="#ffffff" filter="url(#territory-shadow)">NEW ORLEANS</text>
    </g>
</svg>
'''
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())
    print(f"Generated historical map SVG: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="historical_map.svg")
    args = parser.parse_args()
    generate_map_svg(args.out)

