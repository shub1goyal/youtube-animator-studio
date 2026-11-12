"""
storybook_ink_engine.py
Flagship "Past in Ink" Hand-Drawn Watercolor & Ink Storybook Animation Engine.
Produces 100% self-contained, 100% local broadcast-grade 1920x1080 animated episodes
in the exact style of the viral "Past in Ink" channel:
- Warm parchment cream paper (#f5efe0) with organic paper grain & watercolor wash shaders
- Hand-drawn ink pen outlines with SVG feTurbulence & feDisplacementMap ink-boil filters
- 3/4 Perspective white-circle-head characters with authentic hairstyles (chonmage, topknots)
- 6 distinct rapidly-cutting compositional layouts (Courtyard, Tatami Table, Macro POV Coins,
  Calligraphy Desk, 3-Panel Triptych Split, Edo Street Procession)
- Deterministic 60 FPS Playwright timeline with window.seekToTime(t)
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

# Local config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CHROME_PATH, FFMPEG_PATH


class StorybookInkEngine:
    """Master generator for 'Past in Ink' Hand-Drawn Watercolor & Ink Storybook Animations."""

    @staticmethod
    def get_storybook_defs():
        """Returns the canonical watercolor paper & dip-pen ink filter stack."""
        return """
        <defs>
          <style type="text/css">
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,800;1,400&family=Noto+Serif+JP:wght@600;900&family=Inter:wght@600;800&display=swap');

            /* Organic Ink Line Boil */
            @keyframes inkBoil {
              0%, 100% { transform: translate(0px, 0px) scale(1.0); }
              25% { transform: translate(-0.3px, 0.4px) scale(1.001); }
              50% { transform: translate(0.4px, -0.2px) scale(0.999); }
              75% { transform: translate(-0.2px, -0.3px) scale(1.0005); }
            }
            @keyframes softFloat {
              0%, 100% { transform: translateY(0px) rotate(0deg); }
              50% { transform: translateY(-4px) rotate(0.4deg); }
            }
            @keyframes leafDrift {
              0% { transform: translate(0px, 0px) rotate(0deg); opacity: 0; }
              20% { opacity: 0.85; }
              80% { opacity: 0.85; }
              100% { transform: translate(320px, 140px) rotate(160deg); opacity: 0; }
            }

            .ink-line {
              stroke: #181412;
              stroke-width: 4.5;
              stroke-linecap: round;
              stroke-linejoin: round;
              fill: none;
            }
            .ink-heavy {
              stroke: #181412;
              stroke-width: 6.5;
              stroke-linecap: round;
              stroke-linejoin: round;
            }
            .ink-fine {
              stroke: #181412;
              stroke-width: 2.8;
              stroke-linecap: round;
              stroke-linejoin: round;
            }
          </style>

          <!-- Organic Hand-Inked Pen Line Filter -->
          <filter id="hand-ink-filter" x="-20%" y="-20%" width="140%" height="140%">
            <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" result="noise"/>
            <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.2" xChannelSelector="R" yChannelSelector="G"/>
          </filter>

          <!-- Soft Watercolor Wash Bleed Filter -->
          <filter id="watercolor-bleed" x="-20%" y="-20%" width="140%" height="140%">
            <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" result="washNoise"/>
            <feDisplacementMap in="SourceGraphic" in2="washNoise" scale="3.8" xChannelSelector="R" yChannelSelector="G"/>
          </filter>

          <!-- Soft Textured Watercolor Paper Gradients -->
          <radialGradient id="paperVignette" cx="50%" cy="50%" r="70%">
            <stop offset="60%" stop-color="#f5efe0" stop-opacity="0"/>
            <stop offset="100%" stop-color="#dfd2bc" stop-opacity="0.85"/>
          </radialGradient>

          <!-- Sky Watercolor Wash -->
          <linearGradient id="skyWatercolor" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#c2d7e0" stop-opacity="0.95"/>
            <stop offset="50%" stop-color="#dce8ec" stop-opacity="0.75"/>
            <stop offset="100%" stop-color="#f5efe0" stop-opacity="0.1"/>
          </linearGradient>

          <!-- Tatami Mat Shading -->
          <linearGradient id="tatamiWash" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#d4cca0"/>
            <stop offset="50%" stop-color="#ded7b4"/>
            <stop offset="100%" stop-color="#cfc797"/>
          </linearGradient>

          <!-- Warm Cedar Wood Shading -->
          <linearGradient id="cedarWash" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#b07b4e"/>
            <stop offset="100%" stop-color="#8a5a32"/>
          </linearGradient>

          <!-- Japanese Clay Roof Tiles (Kawara) -->
          <linearGradient id="roofTileWash" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#3d434a"/>
            <stop offset="100%" stop-color="#242930"/>
          </linearGradient>

          <!-- Samurai Kimono Maroon Watercolor -->
          <linearGradient id="kimonoMaroon" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#944850"/>
            <stop offset="70%" stop-color="#7d373f"/>
            <stop offset="100%" stop-color="#662930"/>
          </linearGradient>

          <!-- Samurai Hakama Slate-Blue Watercolor -->
          <linearGradient id="hakamaSlate" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#4d5d73"/>
            <stop offset="100%" stop-color="#344254"/>
          </linearGradient>

          <!-- Tatami Mat Border Pattern -->
          <pattern id="tatamiBorder" width="24" height="24" patternUnits="userSpaceOnUse">
            <rect width="24" height="24" fill="#2d3329"/>
            <line x1="0" y1="12" x2="24" y2="12" stroke="#525c4b" stroke-width="2"/>
          </pattern>
        </defs>
        """

    @classmethod
    def draw_storybook_character(cls, x=960, y=860, scale=1.0, pose="standing", facing=1, gaze=0.0, mouth="closed", worried=False):
        """
        Draws the signature 'Past in Ink' character:
        - 3/4 Angle white round head (#ffffff) with expressive black ink eyebrows and dot eyes
        - Traditional Edo samurai chonmage (side hair, shaved crown, tied topknot curving forward)
        - Layered kimono (maroon kimono, white collar, striped obi sash, slate-blue hakama trousers)
        - Twin daisho katanas tucked at the waist
        - Expressive black stick/sleeved arms with white cartoon hands
        """
        s = scale
        svg = f'<g id="char-samurai" transform="translate({x}, {y}) scale({facing * s}, {s})" filter="url(#hand-ink-filter)">\n'

        # Soft watercolor ground shadow
        svg += f'  <ellipse cx="0" cy="8" rx="{85 * s}" ry="{16 * s}" fill="#1a1410" opacity="0.32"/>\n'

        if pose == "kneeling":
            # 1. Kneeling Hakama Pleats & Sandals
            svg += f'  <path d="M -90 -30 Q -110 0 -80 0 L 80 0 Q 110 0 90 -30 L 60 -140 L -60 -140 Z" fill="url(#hakamaSlate)" stroke="#181412" stroke-width="5"/>\n'
            # Pleat lines
            for px in [-40, -15, 15, 40]:
                svg += f'  <line x1="{px}" y1="-140" x2="{px * 1.35}" y2="0" stroke="#181412" stroke-width="3" stroke-linecap="round"/>\n'

            # 2. Torso with Maroon Kimono
            svg += '  <path d="M -54 -140 L -62 -250 L 62 -250 L 54 -140 Z" fill="url(#kimonoMaroon)" stroke="#181412" stroke-width="5.5"/>\n'
            # White Juban Inner Collar V-neck
            svg += '  <polygon points="-16,-250 16,-250 0,-215" fill="#ffffff" stroke="#181412" stroke-width="3"/>\n'
            # Obi Sash
            svg += '  <rect x="-56" y="-155" width="112" height="24" rx="3" fill="#2d2926" stroke="#181412" stroke-width="4"/>\n'

            # 3. Katana Hilts at Hip
            svg += '  <g transform="translate(-52, -145) rotate(-28)">\n'
            svg += '    <!-- Katana 1 (Longer) -->\n'
            svg += '    <line x1="-15" y1="0" x2="65" y2="0" stroke="#181412" stroke-width="6"/>\n'
            svg += '    <circle cx="20" cy="0" r="8" fill="#c29b38" stroke="#181412" stroke-width="2.5"/>\n'
            svg += '    <rect x="-15" y="-5" width="32" height="10" rx="2" fill="#ffffff" stroke="#181412" stroke-width="2.5"/>\n'
            svg += '    <!-- Katana 2 (Wakizashi) -->\n'
            svg += '    <line x1="-10" y1="12" x2="45" y2="12" stroke="#181412" stroke-width="5"/>\n'
            svg += '    <circle cx="16" cy="12" r="7" fill="#c29b38" stroke="#181412" stroke-width="2.5"/>\n'
            svg += '    <rect x="-10" y="8" width="24" height="8" rx="2" fill="#ffffff" stroke="#181412" stroke-width="2"/>\n'
            svg += '  </g>\n'

            # Head position for kneeling
            head_y = -310

        elif pose == "walking":
            # Walking Legs
            svg += '  <!-- Back Leg -->\n'
            svg += '  <path d="M -22 -120 L -38 0 L -12 0 L 0 -120 Z" fill="url(#hakamaSlate)" stroke="#181412" stroke-width="4.5"/>\n'
            svg += '  <!-- Front Leg -->\n'
            svg += '  <path d="M 12 -120 L 32 0 L 58 0 L 32 -120 Z" fill="url(#hakamaSlate)" stroke="#181412" stroke-width="4.5"/>\n'
            # Sandals (Zori) with White Tabi
            svg += '  <ellipse cx="-25" cy="2" rx="15" ry="5" fill="#f8f4eb" stroke="#181412" stroke-width="3"/>\n'
            svg += '  <ellipse cx="45" cy="2" rx="15" ry="5" fill="#f8f4eb" stroke="#181412" stroke-width="3"/>\n'

            # Torso
            svg += '  <path d="M -50 -120 L -58 -260 L 58 -260 L 50 -120 Z" fill="url(#kimonoMaroon)" stroke="#181412" stroke-width="5.5"/>\n'
            svg += '  <polygon points="-16,-260 16,-260 0,-220" fill="#ffffff" stroke="#181412" stroke-width="3"/>\n'
            svg += '  <rect x="-52" y="-135" width="104" height="24" rx="3" fill="#2d2926" stroke="#181412" stroke-width="4"/>\n'
            head_y = -320

        else:
            # Standing 3/4 Posture
            # 1. Pleated Hakama Trousers
            svg += '  <path d="M -60 -130 L -75 0 L 75 0 L 60 -130 Z" fill="url(#hakamaSlate)" stroke="#181412" stroke-width="5.5"/>\n'
            # Pleat creases
            for px in [-35, -12, 12, 35]:
                svg += f'  <line x1="{px}" y1="-130" x2="{px * 1.25}" y2="0" stroke="#181412" stroke-width="3.5" stroke-linecap="round"/>\n'
            # Straw Sandals (Zori) & White Tabi Socks
            svg += '  <ellipse cx="-40" cy="2" rx="18" ry="6" fill="#f8f4eb" stroke="#181412" stroke-width="3.5"/>\n'
            svg += '  <ellipse cx="40" cy="2" rx="18" ry="6" fill="#f8f4eb" stroke="#181412" stroke-width="3.5"/>\n'
            svg += '  <path d="M -48 1 L -40 -3 L -32 1" stroke="#181412" stroke-width="3" fill="none"/>\n'
            svg += '  <path d="M 32 1 L 40 -3 L 48 1" stroke="#181412" stroke-width="3" fill="none"/>\n'

            # 2. Maroon Kimono Torso
            svg += '  <path d="M -54 -130 L -62 -270 L 62 -270 L 54 -130 Z" fill="url(#kimonoMaroon)" stroke="#181412" stroke-width="5.5"/>\n'
            # White Juban Under-Collar V
            svg += '  <polygon points="-18,-270 18,-270 0,-225" fill="#ffffff" stroke="#181412" stroke-width="3.5"/>\n'
            # Kimono Lapel Fold Cross
            svg += '  <line x1="-54" y1="-265" x2="24" y2="-130" stroke="#181412" stroke-width="4.5" stroke-linecap="round"/>\n'
            # Obi Belt
            svg += '  <rect x="-56" y="-145" width="112" height="26" rx="3" fill="#2d2926" stroke="#181412" stroke-width="4"/>\n'
            svg += '  <line x1="-54" y1="-132" x2="54" y2="-132" stroke="#d4cca0" stroke-width="2"/>\n'

            # 3. Katana Pair (Daisho) at Left Hip
            svg += '  <g transform="translate(-48, -135) rotate(-25)">\n'
            svg += '    <!-- Katana Scabbard (Saya) -->\n'
            svg += '    <path d="M -20 0 Q 60 10 120 4" stroke="#181412" stroke-width="7" fill="none" stroke-linecap="round"/>\n'
            svg += '    <!-- Tsuba (Handguard) -->\n'
            svg += '    <ellipse cx="15" cy="2" rx="7" ry="12" fill="#c29b38" stroke="#181412" stroke-width="3"/>\n'
            # Tsuka (Hilt with Diamond Wrap)
            svg += '    <line x1="-22" y1="-2" x2="14" y2="2" stroke="#ffffff" stroke-width="6"/>\n'
            svg += '    <line x1="-22" y1="-2" x2="14" y2="2" stroke="#181412" stroke-width="6" stroke-dasharray="3,3"/>\n'
            svg += '  </g>\n'

            # 4. Arms with Sleeves
            # Left Hand resting on Katana Hilt
            svg += '  <path d="M -54 -250 Q -85 -200 -36 -142" stroke="#181412" stroke-width="12" fill="none" stroke-linecap="round"/>\n'
            svg += '  <path d="M -54 -250 Q -85 -200 -36 -142" stroke="url(#kimonoMaroon)" stroke-width="8" fill="none" stroke-linecap="round"/>\n'
            # White Cartoon Hand on Hilt
            svg += '  <circle cx="-32" cy="-142" r="11" fill="#ffffff" stroke="#181412" stroke-width="3.5"/>\n'

            # Right Arm Relaxed at Side
            svg += '  <path d="M 54 -250 Q 82 -200 68 -135" stroke="#181412" stroke-width="12" fill="none" stroke-linecap="round"/>\n'
            svg += '  <path d="M 54 -250 Q 82 -200 68 -135" stroke="url(#kimonoMaroon)" stroke-width="8" fill="none" stroke-linecap="round"/>\n'
            svg += '  <circle cx="68" cy="-132" r="11" fill="#ffffff" stroke="#181412" stroke-width="3.5"/>\n'

            head_y = -330

        # =====================================================================
        # 5. THE "PAST IN INK" CHARACTER HEAD (Pure White Round 3/4 Head)
        # =====================================================================
        svg += f'  <g id="samurai-head" transform="translate(0, {head_y})">\n'

        # Chonmage Back Hair (Under Head)
        svg += '    <!-- Samurai Chonmage (Back Hair & Topknot) -->\n'
        svg += '    <ellipse cx="-18" cy="-12" rx="58" ry="48" fill="#181412"/>\n'
        # Shaved Crown (Sakayaki) visible at top
        svg += '    <ellipse cx="4" cy="-38" rx="34" ry="14" fill="#ebe4d3" opacity="0.6"/>\n'
        # Tied Topknot Hair Curving Forward over Crown
        svg += '    <path d="M -34 -48 Q 12 -65 38 -45" stroke="#181412" stroke-width="10" fill="none" stroke-linecap="round"/>\n'
        # White Cord Tie (Motoyui)
        svg += '    <rect x="-30" y="-56" width="9" height="12" rx="2" fill="#ffffff" stroke="#181412" stroke-width="2"/>\n'

        # PURE WHITE ROUND HEAD (3/4 slightly oval)
        svg += '    <ellipse cx="2" cy="0" rx="54" ry="52" fill="#ffffff" stroke="#181412" stroke-width="5.5"/>\n'

        # Expressive Black Eyebrows
        g_shift = gaze * 10
        if worried:
            # Arched Worried / Perplexed Eyebrows
            svg += f'    <path d="M {-26 + g_shift} -18 Q {-12 + g_shift} -28 {0 + g_shift} -20" stroke="#181412" stroke-width="4.5" fill="none" stroke-linecap="round"/>\n'
            svg += f'    <path d="M {12 + g_shift} -20 Q {24 + g_shift} -28 {38 + g_shift} -18" stroke="#181412" stroke-width="4.5" fill="none" stroke-linecap="round"/>\n'
            # Subtle Under-Eye Worry Line
            svg += f'    <path d="M {-20 + g_shift} 8 Q {-12 + g_shift} 12 {-4 + g_shift} 8" stroke="#78716c" stroke-width="2" fill="none"/>\n'
        else:
            # Calm / Focused Eyebrows
            svg += f'    <path d="M {-24 + g_shift} -20 Q {-12 + g_shift} -24 {0 + g_shift} -21" stroke="#181412" stroke-width="4.5" fill="none" stroke-linecap="round"/>\n'
            svg += f'    <path d="M {12 + g_shift} -21 Q {24 + g_shift} -24 {36 + g_shift} -20" stroke="#181412" stroke-width="4.5" fill="none" stroke-linecap="round"/>\n'

        # Minimalist Black Oval Dot Eyes (Past in Ink signature style)
        svg += f'    <ellipse cx="{-12 + g_shift}" cy="-4" rx="4.5" ry="6" fill="#181412"/>\n'
        svg += f'    <ellipse cx="{22 + g_shift}" cy="-4" rx="4.5" ry="6" fill="#181412"/>\n'

        # Expressive Hand-Inked Mouth
        if mouth == "open" or mouth == "talk":
            svg += f'    <ellipse cx="{5 + g_shift}" cy="22" rx="9" ry="11" fill="#7a2e36" stroke="#181412" stroke-width="3.5"/>\n'
            svg += f'    <path d="M {-2 + g_shift} 27 Q {5 + g_shift} 23 {12 + g_shift} 27" fill="#dc2626"/>\n'
        elif mouth == "worried_wavy":
            svg += f'    <path d="M {-10 + g_shift} 22 Q {-2 + g_shift} 17 {6 + g_shift} 24 Q {14 + g_shift} 19 {20 + g_shift} 23" stroke="#181412" stroke-width="3.5" fill="none" stroke-linecap="round"/>\n'
        else:
            # Closed calm line
            svg += f'    <path d="M {-8 + g_shift} 22 Q {5 + g_shift} 25 {16 + g_shift} 21" stroke="#181412" stroke-width="3.5" fill="none" stroke-linecap="round"/>\n'

        svg += '  </g>\n'
        svg += '</g>\n'
        return svg

    # =====================================================================
    # 6 SIGNATURE SHOT COMPOSITIONS (RAPID CUTTING STORYBOOK MOVIE)
    # =====================================================================

    @classmethod
    def render_shot_1_courtyard(cls):
        """Shot 1: Exterior Courtyard Low-Angle Establishing."""
        svg = '<g id="shot-1-plane" style="position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;">\n'
        # Warm Parchment Base
        svg += '  <rect width="1920" height="1080" fill="#f5efe0"/>\n'
        # Sky Watercolor Wash
        svg += '  <rect width="1920" height="600" fill="url(#skyWatercolor)"/>\n'

        # Pine Tree Foliage in Background
        svg += '  <g filter="url(#watercolor-bleed)" opacity="0.88">\n'
        svg += '    <ellipse cx="280" cy="240" rx="220" ry="160" fill="#607d56"/>\n'
        svg += '    <ellipse cx="440" cy="180" rx="160" ry="120" fill="#739467"/>\n'
        svg += '  </g>\n'

        # Traditional Edo Timber Wall & Kawara Clay Tiled Roof
        svg += '  <!-- Edo Timber Wall with Plaster Base -->\n'
        svg += '  <rect x="0" y="440" width="1920" height="640" fill="#ded4be" stroke="#181412" stroke-width="6"/>\n'
        # Vertical Cedar Wall Slats
        for wx in range(60, 1920, 160):
            svg += f'  <line x1="{wx}" y1="440" x2="{wx}" y2="1080" stroke="#8a5a32" stroke-width="5" opacity="0.65"/>\n'

        # Heavy Clay Tile Roof (Kawara) with Ridge End Ornament (Onigawara)
        svg += '  <polygon points="0,380 1920,380 1920,440 0,440" fill="url(#roofTileWash)" stroke="#181412" stroke-width="6"/>\n'
        svg += '  <polygon points="0,350 1920,350 1920,380 0,380" fill="#2d333b" stroke="#181412" stroke-width="5"/>\n'
        for tx in range(30, 1920, 60):
            svg += f'  <circle cx="{tx}" cy="440" r="14" fill="#3d434a" stroke="#181412" stroke-width="3"/>\n'

        # Stone Paved Ground
        svg += '  <rect x="0" y="900" width="1920" height="180" fill="#cfc5af"/>\n'
        svg += '  <line x1="0" y1="900" x2="1920" y2="900" stroke="#181412" stroke-width="6"/>\n'

        # Hero Character: Standing Samurai 3/4 low-angle
        svg += cls.draw_storybook_character(x=960, y=910, scale=1.35, pose="standing", facing=1, gaze=0.2, mouth="talk", worried=False)

        # Drifting Maple Leaves
        svg += '  <g class="anim-leaves">\n'
        svg += '    <path d="M 280 120 Q 300 110 310 130 Q 300 145 285 138 Z" fill="#b94a38" stroke="#181412" stroke-width="1.8"/>\n'
        svg += '    <path d="M 1480 90 Q 1500 80 1515 98 Q 1502 112 1485 106 Z" fill="#c97334" stroke="#181412" stroke-width="1.8"/>\n'
        svg += '  </g>\n'
        svg += '</g>\n'
        return svg

    @classmethod
    def render_shot_2_tatami_table(cls):
        """Shot 2: Warm Tatami Interior Two-Person Table Exchange."""
        svg = '<g id="shot-2-plane" style="position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;">\n'
        # Warm Parchment Base
        svg += '  <rect width="1920" height="1080" fill="#f5efe0"/>\n'

        # Shoji Paper Sliding Screen Wall
        svg += '  <rect x="120" y="80" width="1680" height="660" fill="#faf6ed" stroke="#181412" stroke-width="6"/>\n'
        # Cedar Wood Shoji Grids
        for gx in range(120, 1800, 140):
            svg += f'  <line x1="{gx}" y1="80" x2="{gx}" y2="740" stroke="#a06c3f" stroke-width="4"/>\n'
        for gy in range(80, 740, 110):
            svg += f'  <line x1="120" y1="{gy}" x2="1800" y2="{gy}" stroke="#a06c3f" stroke-width="4"/>\n'

        # Tatami Mats Floor
        svg += '  <rect x="0" y="740" width="1920" height="340" fill="url(#tatamiWash)"/>\n'
        svg += '  <line x1="0" y1="740" x2="1920" y2="740" stroke="#181412" stroke-width="6"/>\n'
        svg += '  <rect x="0" y="736" width="1920" height="16" fill="url(#tatamiBorder)"/>\n'

        # Low Wooden Table (Zataku) in Center
        svg += '  <!-- Low Wooden Japanese Table (Zataku) -->\n'
        svg += '  <polygon points="620,780 1300,780 1240,710 680,710" fill="url(#cedarWash)" stroke="#181412" stroke-width="6"/>\n'
        svg += '  <rect x="620" y="780" width="680" height="30" rx="4" fill="#6d421e" stroke="#181412" stroke-width="5"/>\n'
        svg += '  <rect x="660" y="810" width="34" height="65" fill="#4d2f16" stroke="#181412" stroke-width="4"/>\n'
        svg += '  <rect x="1226" y="810" width="34" height="65" fill="#4d2f16" stroke="#181412" stroke-width="4"/>\n'

        # Wooden Tray with 3 Copper Coins on Table
        svg += '  <rect x="860" y="725" width="200" height="45" rx="5" fill="#dfd0b2" stroke="#181412" stroke-width="3.5"/>\n'
        for cx_val in [900, 960, 1020]:
            svg += f'  <circle cx="{cx_val}" cy="746" r="14" fill="#a86236" stroke="#181412" stroke-width="3"/>\n'
            svg += f'  <rect x="{cx_val - 4}" y="742" width="8" height="8" fill="#dfd0b2" stroke="#181412" stroke-width="2"/>\n'

        # Dark Cloth Coin Purse next to tray
        svg += '  <path d="M 770 755 C 760 730, 810 720, 830 740 C 840 760, 785 770, 770 755 Z" fill="#475569" stroke="#181412" stroke-width="3"/>\n'
        svg += '  <circle cx="800" cy="735" r="4" fill="#dc2626"/>\n'

        # Character 1 (Left): Samurai Looking Down at Coins (Worried)
        svg += cls.draw_storybook_character(x=540, y=900, scale=1.2, pose="standing", facing=1, gaze=0.3, mouth="worried_wavy", worried=True)

        # Character 2 (Right): Family Member pointing at coins
        svg += '  <!-- Family Member in Grey Kimono Pointing -->\n'
        svg += '  <g transform="translate(1380, 900) scale(-1.18, 1.18)">\n'
        # Grey Kimono
        svg += '    <path d="M -50 -120 L -60 -260 L 60 -260 L 50 -120 Z" fill="#64748b" stroke="#181412" stroke-width="5.5"/>\n'
        svg += '    <rect x="-52" y="-135" width="104" height="24" rx="3" fill="#334155" stroke="#181412" stroke-width="4"/>\n'
        svg += '    <path d="M -55 -120 L -65 0 L 65 0 L 55 -120 Z" fill="#475569" stroke="#181412" stroke-width="5"/>\n'
        # Arm Pointing at Table
        svg += '    <path d="M -50 -240 Q -110 -210 -150 -160" stroke="#181412" stroke-width="12" fill="none" stroke-linecap="round"/>\n'
        svg += '    <path d="M -50 -240 Q -110 -210 -150 -160" stroke="#64748b" stroke-width="8" fill="none" stroke-linecap="round"/>\n'
        svg += '    <circle cx="-150" cy="-160" r="11" fill="#ffffff" stroke="#181412" stroke-width="3.5"/>\n'
        # White Head with Hair Bun
        svg += '    <g transform="translate(0, -320)">\n'
        svg += '      <circle cx="-16" cy="-35" r="18" fill="#181412"/>\n'
        svg += '      <ellipse cx="0" cy="0" rx="52" ry="50" fill="#ffffff" stroke="#181412" stroke-width="5.5"/>\n'
        svg += '      <ellipse cx="-12" cy="-4" rx="4.5" ry="6" fill="#181412"/>\n'
        svg += '      <ellipse cx="22" cy="-4" rx="4.5" ry="6" fill="#181412"/>\n'
        svg += '      <path d="M -22 -18 Q -10 -24 0 -20" stroke="#181412" stroke-width="4.5" fill="none"/>\n'
        svg += '      <path d="M 12 -20 Q 24 -24 36 -18" stroke="#181412" stroke-width="4.5" fill="none"/>\n'
        svg += '      <path d="M -6 20 Q 5 24 16 20" stroke="#181412" stroke-width="3.5" fill="none"/>\n'
        svg += '    </g>\n'
        svg += '  </g>\n'
        svg += '</g>\n'
        return svg

    @classmethod
    def render_shot_3_macro_coins(cls):
        """Shot 3: Macro POV Close-Up of White Cartoon Hand Counting 3 Copper Coins."""
        svg = '<g id="shot-3-plane" style="position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;">\n'
        # Warm Tatami Grain Background
        svg += '  <rect width="1920" height="1080" fill="url(#tatamiWash)"/>\n'
        for ty in range(0, 1080, 48):
            svg += f'  <line x1="0" y1="{ty}" x2="1920" y2="{ty}" stroke="#a39a75" stroke-width="1.8" opacity="0.45"/>\n'

        # Large Grained Wooden Tray (Top-Down Perspective)
        svg += '  <!-- Grained Wooden Tray (Macro View) -->\n'
        svg += '  <rect x="240" y="140" width="1440" height="800" rx="28" fill="#cfa574" stroke="#181412" stroke-width="10"/>\n'
        svg += '  <rect x="270" y="170" width="1380" height="740" rx="20" fill="#dfbe90" stroke="#181412" stroke-width="5"/>\n'

        # Open Grey Cloth Coin Pouch on Left
        svg += '  <path d="M 360 420 C 320 280, 540 260, 580 380 C 620 520, 420 560, 360 420 Z" fill="#64748b" stroke="#181412" stroke-width="7"/>\n'
        svg += '  <ellipse cx="480" cy="370" rx="75" ry="45" fill="#334155" stroke="#181412" stroke-width="4.5"/>\n'
        svg += '  <line x1="420" y1="360" x2="520" y2="400" stroke="#dc2626" stroke-width="5"/>\n'

        # 3 Large Copper Edo Kan'ei Tsuho Coins (Detailed Calligraphy Markings & Square Holes)
        coin_coords = [(720, 540), (960, 540), (1200, 540)]
        for idx, (cx, cy) in enumerate(coin_coords, 1):
            svg += f'  <g id="coin-{idx}" transform="translate({cx}, {cy})">\n'
            # Drop shadow
            svg += '    <ellipse cx="10" cy="18" rx="100" ry="95" fill="#181412" opacity="0.25"/>\n'
            # Coin Outer Rim
            svg += '    <circle cx="0" cy="0" r="100" fill="#b0643b" stroke="#181412" stroke-width="8"/>\n'
            svg += '    <circle cx="0" cy="0" r="86" fill="#c8794d" stroke="#181412" stroke-width="3.5"/>\n'
            # Square Center Hole
            svg += '    <rect x="-24" y="-24" width="48" height="48" rx="4" fill="#dfbe90" stroke="#181412" stroke-width="7"/>\n'
            # Embossed Characters on 4 Sides
            svg += '    <text x="0" y="-48" font-family="Noto Serif JP, serif" font-size="26" font-weight="900" fill="#181412" text-anchor="middle">寛</text>\n'
            svg += '    <text x="0" y="68" font-family="Noto Serif JP, serif" font-size="26" font-weight="900" fill="#181412" text-anchor="middle">寳</text>\n'
            svg += '    <text x="-58" y="8" font-family="Noto Serif JP, serif" font-size="26" font-weight="900" fill="#181412" text-anchor="middle">永</text>\n'
            svg += '    <text x="58" y="8" font-family="Noto Serif JP, serif" font-size="26" font-weight="900" fill="#181412" text-anchor="middle">通</text>\n'
            svg += '  </g>\n'

        # White Cartoon Hand Reaching from Bottom Right with Pointing Finger
        svg += '  <!-- White Cartoon Hand Pointing / Counting Coins -->\n'
        svg += '  <g id="pointing-hand" style="transform-origin: 1400px 920px;">\n'
        # Black Stick Arm Wrist
        svg += '    <path d="M 1880 1140 L 1320 740" stroke="#181412" stroke-width="26" stroke-linecap="round"/>\n'
        svg += '    <!-- White Glove Hand -->\n'
        svg += '    <circle cx="1290" cy="720" r="55" fill="#ffffff" stroke="#181412" stroke-width="8"/>\n'
        # Pointing Index Finger
        svg += '    <path d="M 1260 700 L 1050 580" stroke="#181412" stroke-width="32" stroke-linecap="round"/>\n'
        svg += '    <path d="M 1260 700 L 1050 580" stroke="#ffffff" stroke-width="20" stroke-linecap="round"/>\n'
        svg += '  </g>\n'
        svg += '</g>\n'
        return svg

    @classmethod
    def render_shot_4_calligraphy_desk(cls):
        """Shot 4: Samurai Kneeling at Low Wooden Desk Writing Calligraphy with Brush."""
        svg = '<g id="shot-4-plane" style="position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;">\n'
        # Warm Parchment Base
        svg += '  <rect width="1920" height="1080" fill="#f5efe0"/>\n'

        # Open Shoji Doors Overlooking Peaceful Watercolor Garden
        svg += '  <rect x="220" y="60" width="1480" height="520" fill="url(#skyWatercolor)" stroke="#181412" stroke-width="6"/>\n'
        # Garden Stone Lantern & Bamboo in Background
        svg += '  <g filter="url(#watercolor-bleed)" opacity="0.85">\n'
        svg += '    <!-- Stone Lantern (Toro) -->\n'
        svg += '    <rect x="1340" y="340" width="60" height="180" fill="#88949e" stroke="#181412" stroke-width="3"/>\n'
        svg += '    <polygon points="1320,340 1420,340 1370,300" fill="#697682" stroke="#181412" stroke-width="3"/>\n'
        svg += '    <!-- Green Bamboo Leaves -->\n'
        svg += '    <ellipse cx="420" cy="360" rx="140" ry="240" fill="#7ba36e"/>\n'
        svg += '  </g>\n'

        # Tatami Floor
        svg += '  <rect x="0" y="580" width="1920" height="500" fill="url(#tatamiWash)"/>\n'
        svg += '  <line x1="0" y1="580" x2="1920" y2="580" stroke="#181412" stroke-width="6"/>\n'

        # Katana Sword Stand (Katana-kake) with 2 Swords in Background
        svg += '  <!-- Traditional Wooden Sword Rack (Katana-Kake) -->\n'
        svg += '  <g transform="translate(1420, 640)">\n'
        svg += '    <rect x="-60" y="0" width="120" height="18" fill="#181412"/>\n'
        svg += '    <rect x="-45" y="-120" width="14" height="120" fill="#181412"/>\n'
        svg += '    <rect x="31" y="-120" width="14" height="120" fill="#181412"/>\n'
        # Katana 1
        svg += '    <path d="M -90 -85 Q 0 -95 90 -88" stroke="#ffffff" stroke-width="7" fill="none"/>\n'
        svg += '    <path d="M -90 -85 Q 0 -95 90 -88" stroke="#181412" stroke-width="5" fill="none"/>\n'
        svg += '    <!-- Katana 2 -->\n'
        svg += '    <path d="M -75 -45 Q 0 -55 75 -48" stroke="#ffffff" stroke-width="6" fill="none"/>\n'
        svg += '    <path d="M -75 -45 Q 0 -55 75 -48" stroke="#181412" stroke-width="4.5" fill="none"/>\n'
        svg += '  </g>\n'

        # Samurai Kneeling at Desk (Seiza)
        svg += cls.draw_storybook_character(x=720, y=860, scale=1.3, pose="kneeling", facing=1, gaze=0.35, mouth="closed", worried=False)

        # Low Wooden Calligraphy Desk (Kyousoku / Bunkodai)
        svg += '  <!-- Low Wooden Writing Desk -->\n'
        svg += '  <polygon points="780,820 1440,820 1380,740 840,740" fill="url(#cedarWash)" stroke="#181412" stroke-width="6"/>\n'
        svg += '  <rect x="780" y="820" width="660" height="30" rx="3" fill="#6d421e" stroke="#181412" stroke-width="5"/>\n'
        svg += '  <rect x="820" y="850" width="30" height="70" fill="#4d2f16" stroke="#181412" stroke-width="4"/>\n'
        svg += '  <rect x="1370" y="850" width="30" height="70" fill="#4d2f16" stroke="#181412" stroke-width="4"/>\n'

        # Rice Paper Scroll with Calligraphy on Desk
        svg += '  <rect x="920" y="755" width="280" height="85" rx="3" fill="#faf6ed" stroke="#181412" stroke-width="3"/>\n'
        # Calligraphy Characters
        for lx in [960, 1020, 1080, 1140]:
            svg += f'  <line x1="{lx}" y1="765" x2="{lx}" y2="825" stroke="#181412" stroke-width="3.5" stroke-dasharray="8,6"/>\n'

        # Slate Inkstone (Suzuri) & Stacked Bound Books
        svg += '  <rect x="1230" y="760" width="55" height="75" rx="6" fill="#292524" stroke="#181412" stroke-width="4"/>\n'
        svg += '  <ellipse cx="1257" cy="790" rx="16" ry="24" fill="#0c0a09"/>\n'
        # Stacked Bound Rice-Paper Ledgers
        svg += '  <rect x="1310" y="750" width="95" height="70" rx="3" fill="#3b82f6" stroke="#181412" stroke-width="3.5"/>\n'
        svg += '  <rect x="1305" y="765" width="95" height="18" rx="2" fill="#faf6ed" stroke="#181412" stroke-width="2"/>\n'

        # Animated Bamboo Brush (Fude) held in Hand
        svg += '  <g transform="translate(1040, 750) rotate(-22)">\n'
        svg += '    <rect x="-4" y="-70" width="8" height="70" rx="3" fill="#b45309" stroke="#181412" stroke-width="2.5"/>\n'
        svg += '    <polygon points="-6,0 6,0 0,22" fill="#181412"/>\n'
        svg += '    <circle cx="0" cy="-28" r="14" fill="#ffffff" stroke="#181412" stroke-width="3"/>\n'
        svg += '  </g>\n'
        svg += '</g>\n'
        return svg

    @classmethod
    def render_shot_5_triptych(cls):
        """Shot 5: The Signature 'Past in Ink' 3-Panel Split Triptych on Cream Paper."""
        svg = '<g id="shot-5-plane" style="position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;">\n'
        # Cream Parchment Base
        svg += '  <rect width="1920" height="1080" fill="#f5efe0"/>\n'

        # Title Header Banner on Top
        svg += '  <text x="960" y="95" font-family="Noto Serif JP, Playfair Display, serif" font-size="34" font-weight="900" fill="#181412" text-anchor="middle" letter-spacing="3">THE THREE SPHERES OF SAMURAI DUTY</text>\n'
        svg += '  <line x1="560" y1="120" x2="1360" y2="120" stroke="#181412" stroke-width="3"/>\n'

        # 3 Vertical Panels: Left (Martial), Center (Administrative), Right (Literary)
        panels = [
            {"x": 120, "wash": "#bce0d5", "border": "#5c9183", "label": "MARTIAL PRACTICE (武)", "desc": "Kendo Shinai & Combat Forms"},
            {"x": 700, "wash": "#eedbb8", "border": "#a88147", "label": "ADMINISTRATION (政)", "desc": "Ledgers, Scrolls & Governance"},
            {"x": 1280, "wash": "#cad4e8", "border": "#627394", "label": "LITERARY ARTS (文)", "desc": "Confucian Classics & Poetry"}
        ]

        for p in panels:
            px = p["x"]
            # Panel Container
            svg += f'  <g id="panel-{p["label"][:4]}" transform="translate({px}, 160)">\n'
            svg += f'    <rect width="520" height="820" rx="16" fill="{p["wash"]}" stroke="#181412" stroke-width="7"/>\n'
            svg += f'    <rect x="14" y="14" width="492" height="792" rx="10" fill="none" stroke="{p["border"]}" stroke-width="3"/>\n'

            # Header Label
            svg += '    <rect x="30" y="35" width="460" height="48" rx="6" fill="#181412"/>\n'
            svg += f'    <text x="260" y="68" font-family="Noto Serif JP, serif" font-size="20" font-weight="900" fill="#f5efe0" text-anchor="middle" letter-spacing="1.5">{p["label"]}</text>\n'
            svg += f'    <text x="260" y="115" font-family="Inter, sans-serif" font-size="14" font-weight="600" fill="#44403c" text-anchor="middle">{p["desc"]}</text>\n'

            # Distinct Hand-Drawn Vignette inside each panel
            if "武" in p["label"]:
                # Bamboo Shinai Sword & Kendo Armor
                svg += '    <g transform="translate(260, 480)">\n'
                svg += '      <!-- Bamboo Shinai -->\n'
                svg += '      <line x1="-120" y1="120" x2="120" y2="-120" stroke="#d97706" stroke-width="14" stroke-linecap="round"/>\n'
                svg += '      <line x1="-120" y1="120" x2="120" y2="-120" stroke="#181412" stroke-width="4"/>\n'
                svg += '      <circle cx="-50" cy="50" r="22" fill="#ffffff" stroke="#181412" stroke-width="4"/>\n'
                svg += '      <!-- Kendo Men Helmet -->\n'
                svg += '      <ellipse cx="0" cy="-40" rx="70" ry="85" fill="#1e293b" stroke="#181412" stroke-width="6"/>\n'
                for my in range(-70, 0, 16):
                    svg += f'      <line x1="-45" y1="{my}" x2="45" y2="{my}" stroke="#f8fafc" stroke-width="3"/>\n'
                svg += '    </g>\n'

            elif "政" in p["label"]:
                # Center: Writing Brush & Ledger Books
                svg += '    <g transform="translate(260, 480)">\n'
                svg += '      <rect x="-140" y="-80" width="280" height="180" rx="8" fill="#faf6ed" stroke="#181412" stroke-width="6"/>\n'
                for ly in range(-50, 80, 28):
                    svg += f'      <line x1="-110" y1="{ly}" x2="110" y2="{ly}" stroke="#181412" stroke-width="4" stroke-dasharray="12,8"/>\n'
                # Big Red Official Seal (Inkan / Hanko)
                svg += '      <rect x="40" y="15" width="60" height="60" rx="4" fill="#dc2626" stroke="#991b1b" stroke-width="3"/>\n'
                svg += '      <text x="70" y="52" font-family="Noto Serif JP, serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">印</text>\n'
                svg += '    </g>\n'

            else:
                # Right: Open Bound Book (Wahon)
                svg += '    <g transform="translate(260, 480)">\n'
                svg += '      <path d="M -150 40 Q -75 25 0 35 Q 75 25 150 40 L 150 -70 Q 75 -85 0 -75 Q -75 -85 -150 -70 Z" fill="#faf6ed" stroke="#181412" stroke-width="6"/>\n'
                svg += '      <line x1="0" y1="-75" x2="0" y2="35" stroke="#181412" stroke-width="4"/>\n'
                for bx in [-100, -50, 50, 100]:
                    svg += f'      <line x1="{bx}" y1="-55" x2="{bx}" y2="15" stroke="#181412" stroke-width="3" stroke-dasharray="8,6"/>\n'
                svg += '    </g>\n'

            svg += '  </g>\n'

        svg += '</g>\n'
        return svg

    @classmethod
    def render_shot_6_edo_street(cls):
        """Shot 6: Wide Edo Street Procession with Traditional Shopfronts & Castle Roof."""
        svg = '<g id="shot-6-plane" style="position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;">\n'
        # Sky Watercolor Wash
        svg += '  <rect width="1920" height="1080" fill="#f5efe0"/>\n'
        svg += '  <rect width="1920" height="520" fill="url(#skyWatercolor)"/>\n'

        # Distant Edo Castle Tower Roof
        svg += '  <!-- Distant Edo Castle Pagoda Roof -->\n'
        svg += '  <g transform="translate(1380, 220)" opacity="0.65" filter="url(#watercolor-bleed)">\n'
        svg += '    <polygon points="0,0 220,0 110,-70" fill="#3d434a" stroke="#181412" stroke-width="3"/>\n'
        svg += '    <polygon points="30,-70 190,-70 110,-125" fill="#3d434a" stroke="#181412" stroke-width="3"/>\n'
        svg += '  </g>\n'

        # Street Buildings (Merchant Houses with Noren Shop Curtains)
        # Left Storefront
        svg += '  <!-- Left Wooden Merchant Storefront -->\n'
        svg += '  <polygon points="0,320 540,400 540,860 0,860" fill="#c49e74" stroke="#181412" stroke-width="6"/>\n'
        # Noren Curtains
        svg += '  <polygon points="0,480 540,530 540,610 0,560" fill="#1e3a8a" stroke="#181412" stroke-width="4.5"/>\n'
        svg += '  <text x="260" y="565" font-family="Noto Serif JP, serif" font-size="28" font-weight="900" fill="#ffffff" text-anchor="middle">呉服問屋</text>\n'

        # Right Storefront with Paper Lantern
        svg += '  <!-- Right Storefront with Paper Lantern -->\n'
        svg += '  <polygon points="1920,320 1380,400 1380,860 1920,860" fill="#b0855b" stroke="#181412" stroke-width="6"/>\n'
        # Paper Lantern (Chochin)
        svg += '  <ellipse cx="1420" cy="510" rx="32" ry="48" fill="#fef08a" stroke="#181412" stroke-width="4"/>\n'
        svg += '  <text x="1420" y="520" font-family="Noto Serif JP, serif" font-size="20" font-weight="900" fill="#dc2626" text-anchor="middle">酒</text>\n'

        # Wide Dirt Street
        svg += '  <polygon points="0,860 540,860 1380,860 1920,860 1920,1080 0,1080" fill="#d9cdb4" stroke="#181412" stroke-width="6"/>\n'

        # Distant Townspeople Walking
        svg += '  <!-- Distant Background Townspeople -->\n'
        svg += '  <g transform="translate(680, 840) scale(0.65)">\n'
        svg += '    <ellipse cx="0" cy="0" rx="36" ry="34" fill="#ffffff" stroke="#181412" stroke-width="4"/>\n'
        svg += '    <path d="M -30 30 L -35 140 L 35 140 L 30 30 Z" fill="#65a30d" stroke="#181412" stroke-width="4"/>\n'
        svg += '  </g>\n'
        svg += '  <g transform="translate(1220, 840) scale(0.65)">\n'
        svg += '    <ellipse cx="0" cy="0" rx="36" ry="34" fill="#ffffff" stroke="#181412" stroke-width="4"/>\n'
        svg += '    <path d="M -30 30 L -35 140 L 35 140 L 30 30 Z" fill="#0284c7" stroke="#181412" stroke-width="4"/>\n'
        svg += '  </g>\n'

        # Hero Character: Samurai Walking Down the Center of Edo
        svg += cls.draw_storybook_character(x=960, y=930, scale=1.35, pose="walking", facing=1, gaze=0.0, mouth="talk", worried=False)
        svg += '</g>\n'
        return svg

    @classmethod
    def generate_storybook_movie_html(cls, shots_list, out_html_path, captions_mode="pill"):
        """
        Builds the 60 FPS deterministic HTML5/SVG movie player for 'Past in Ink' style.
        """
        # Render all 6 signature shot layouts
        shot_planes = [
            cls.render_shot_1_courtyard(),
            cls.render_shot_2_tatami_table(),
            cls.render_shot_3_macro_coins(),
            cls.render_shot_4_calligraphy_desk(),
            cls.render_shot_5_triptych(),
            cls.render_shot_6_edo_street()
        ]

        shots_json_str = json.dumps(shots_list or [])

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Past in Ink: A Day in the Life of a Samurai</title>
  <style>
    body, html {{
      margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden;
      background: #181412; display: flex; align-items: center; justify-content: center;
      font-family: 'Inter', sans-serif;
    }}
    #viewport {{
      width: 1920px; height: 1080px; position: relative; overflow: hidden;
      background: #f5efe0;
    }}
    .shot-container {{
      width: 1920px; height: 1080px; position: absolute; left: 0; top: 0;
      display: none; transform-origin: 50% 50%;
    }}

    /* Subtitles in signature high-contrast dark ink pill */
    #subtitles-box {{
      position: absolute; bottom: 55px; width: 100%; text-align: center;
      pointer-events: none; z-index: 50;
    }}
    #subtitle-pill {{
      display: inline-block; background: rgba(24, 20, 18, 0.88);
      border: 2px solid rgba(245, 239, 224, 0.65); border-radius: 38px;
      padding: 10px 42px; max-width: 1540px;
      color: #f5efe0; font-family: 'Noto Serif JP', 'Playfair Display', serif;
      font-size: 38px; font-weight: 700; line-height: 1.35;
      text-shadow: 0 3px 10px rgba(0,0,0,0.9);
      white-space: normal; word-break: break-word;
    }}
  </style>
</head>
<body>
  <div id="viewport">
    <svg xmlns="http://www.w3.org/2000/svg" style="display:none;">
      {cls.get_storybook_defs()}
    </svg>

    <!-- Shot Planes -->
    <div id="shot-plane-0" class="shot-container"><svg viewBox="0 0 1920 1080" width="1920" height="1080">{shot_planes[0]}</svg></div>
    <div id="shot-plane-1" class="shot-container"><svg viewBox="0 0 1920 1080" width="1920" height="1080">{shot_planes[1]}</svg></div>
    <div id="shot-plane-2" class="shot-container"><svg viewBox="0 0 1920 1080" width="1920" height="1080">{shot_planes[2]}</svg></div>
    <div id="shot-plane-3" class="shot-container"><svg viewBox="0 0 1920 1080" width="1920" height="1080">{shot_planes[3]}</svg></div>
    <div id="shot-plane-4" class="shot-container"><svg viewBox="0 0 1920 1080" width="1920" height="1080">{shot_planes[4]}</svg></div>
    <div id="shot-plane-5" class="shot-container"><svg viewBox="0 0 1920 1080" width="1920" height="1080">{shot_planes[5]}</svg></div>

    <!-- Pinned Subtitles with generous word margins -->
    <div id="subtitles-box"><span id="subtitle-pill"><span id="subtitle-text"></span></span></div>
  </div>

  <script>
    const SHOTS = {shots_json_str};
    const subText = document.getElementById("subtitle-text");
    const planes = [
      document.getElementById("shot-plane-0"),
      document.getElementById("shot-plane-1"),
      document.getElementById("shot-plane-2"),
      document.getElementById("shot-plane-3"),
      document.getElementById("shot-plane-4"),
      document.getElementById("shot-plane-5")
    ];

    // Helper: Build rolling 6-word phrase chunks with gold active-word highlight
    function updateRollingSubtitles(shot, t) {{
      if (!shot || !shot.text) {{
        subText.innerHTML = "";
        return;
      }}
      const fullText = shot.text.trim();
      const words = fullText.split(/\\s+/);
      if (words.length === 0) return;

      const duration = Math.max(shot.end - shot.start, 0.1);
      const elapsed = Math.max(0, Math.min(t - shot.start, duration));
      const progress = elapsed / duration;

      const activeWordIdx = Math.min(Math.floor(progress * words.length), words.length - 1);

      const chunkSize = 6;
      const chunkIdx = Math.floor(activeWordIdx / chunkSize);
      const chunkStart = chunkIdx * chunkSize;
      const chunkEnd = Math.min(chunkStart + chunkSize, words.length);
      const chunkWords = words.slice(chunkStart, chunkEnd);

      const htmlWords = chunkWords.map((w, idx) => {{
        const globalIdx = chunkStart + idx;
        if (globalIdx === activeWordIdx) {{
          return '<span style="color:#facc15; display:inline-block; transform:scale(1.14); text-shadow:0 0 14px rgba(250,204,21,0.75); font-weight:900; margin:0 9px;">' + w + '</span>';
        }}
        return '<span style="display:inline-block; margin:0 5px;">' + w + '</span>';
      }});

      subText.innerHTML = htmlWords.join(" ");
    }}

    function doRenderFrame(timeSec) {{
      // Locate active shot
      let activeIdx = 0;
      let activeShot = null;
      for (let i = 0; i < SHOTS.length; i++) {{
        if (timeSec >= SHOTS[i].start && timeSec < SHOTS[i].end) {{
          activeIdx = i;
          activeShot = SHOTS[i];
          break;
        }}
      }}
      if (!activeShot && SHOTS.length > 0) {{
        activeIdx = SHOTS.length - 1;
        activeShot = SHOTS[activeIdx];
      }}

      // Toggle Active Shot Plane
      for (let i = 0; i < planes.length; i++) {{
        if (planes[i]) {{
          planes[i].style.display = (i === (activeIdx % planes.length)) ? "block" : "none";
        }}
      }}

      // Subtle Ken-Burns pan/zoom within current shot
      if (activeShot) {{
        const shotDuration = Math.max(activeShot.end - activeShot.start, 0.1);
        const shotProgress = Math.max(0, Math.min((timeSec - activeShot.start) / shotDuration, 1.0));
        const activePlane = planes[activeIdx % planes.length];
        if (activePlane) {{
          const zoom = 1.0 + shotProgress * 0.08;
          const panY = (activeIdx % 2 === 0) ? -shotProgress * 15 : shotProgress * 10;
          activePlane.style.transform = `scale(${{zoom.toFixed(3)}}) translateY(${{panY.toFixed(1)}}px)`;
        }}

        // Animate coin counting hand on Shot 3
        if ((activeIdx % planes.length) === 2) {{
          const hand = document.getElementById("pointing-hand");
          if (hand) {{
            // Points to coin 1 (0-33%), coin 2 (33-66%), coin 3 (66-100%)
            const handX = (shotProgress < 0.35) ? -240 : ((shotProgress < 0.70) ? 0 : 240);
            const tap = Math.sin(shotProgress * Math.PI * 6.0) * 14.0;
            hand.style.transform = `translate(${{handX}}px, ${{tap}}px)`;
          }}
        }}

        updateRollingSubtitles(activeShot, timeSec);
      }}
    }}

    window.seekToTime = function(t) {{
      doRenderFrame(t);
    }};

    window.renderMovieFrame = function(t) {{
      doRenderFrame(t);
    }};
  </script>
</body>
</html>
"""
        out_p = Path(out_html_path).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"🎬 Generated Storybook Movie HTML: {out_p.name}")
        return str(out_p)


def main():
    parser = argparse.ArgumentParser(description="'Past in Ink' Hand-Drawn Watercolor Engine")
    parser.add_argument("--html", default="storybook_movie.html", help="Output HTML movie player")
    parser.add_argument("--captions", default="pill", choices=["pill", "minimal", "none"])
    args = parser.parse_args()

    default_shots = [
        {"start": 0.0, "end": 4.0, "duration": 4.0, "camera": "wide", "text": "You are a samurai in Edo. You have two swords, a family name to protect, and duties this morning."},
        {"start": 4.0, "end": 8.0, "duration": 4.0, "camera": "medium", "text": "Unfortunately, before you leave the house, there is a much more urgent problem: money."},
        {"start": 8.0, "end": 12.0, "duration": 4.0, "camera": "macro", "text": "You count what is available, and count it again. Social status has not improved the total."},
        {"start": 12.0, "end": 16.0, "duration": 4.0, "camera": "medium", "text": "In the peaceful Edo era, samurai spend their days keeping records, ledgers, and accounts."},
        {"start": 16.0, "end": 20.0, "duration": 4.0, "camera": "infographic", "text": "Martial skill, administrative governance, and classical scholarship define an educated warrior."},
        {"start": 20.0, "end": 24.0, "duration": 4.0, "camera": "wide", "text": "Walking down the busy streets of Edo, you carry the heavy weight of warrior obligations."}
    ]

    StorybookInkEngine.generate_storybook_movie_html(default_shots, args.html, captions_mode=args.captions)


if __name__ == "__main__":
    main()

