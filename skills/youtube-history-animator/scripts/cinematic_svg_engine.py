"""
cinematic_svg_engine.py
The Master Hybrid 2.5D Volumetric + GeoJSON + Skeletal Actor Vector Scene Engine for YouTube Animation Studio.
Generates broadcast-grade 1920x1080 master stages and scene_X_movie.html deterministic Playwright players
with GSAP-style multi-plane camera easing, skeletal IK puppets, tactile map cutaways, and interactive HTML.
"""

import os
import sys
import json
import math
import argparse
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

# Local config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CHROME_PATH
from geojson_map_engine import GeoJsonMapEngine
from hybrid_asset_generator import HybridAssetGenerator


class CinematicSvgEngine:
    """Master generator for broadcast-grade 1920x1080 historical and explainer vector scenes."""

    @staticmethod
    def get_standard_defs():
        """Returns the canonical <defs> stack with embedded self-contained CSS animations, blurs, blooms, and gradients."""
        return """
        <defs>
          <style type="text/css">
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&amp;family=Playfair+Display:ital,wght@0,700;1,400&amp;family=Bangers&amp;family=Noto+Sans+Devanagari:wght@700;900&amp;display=swap');

            @keyframes svgBreathing {
              0%, 100% { transform: scaleY(1) translateY(0px); }
              50% { transform: scaleY(1.018) translateY(-2.5px); }
            }
            @keyframes svgEyeBlink {
              0%, 44%, 48%, 94%, 98%, 100% { transform: scaleY(1); }
              46%, 96% { transform: scaleY(0.08); }
            }
            @keyframes svgSweatDrop {
              0%, 100% { transform: translateY(0px); opacity: 0.95; }
              50% { transform: translateY(8px); opacity: 0.35; }
            }
            @keyframes svgDustFloat {
              0%, 100% { transform: translate(0px, 0px); opacity: 0.35; }
              50% { transform: translate(14px, -22px); opacity: 0.85; }
            }
            @keyframes svgAlertPop {
              0%, 100% { transform: scale(1) rotate(-4deg); }
              50% { transform: scale(1.12) rotate(4deg); }
            }
            @keyframes svgCandleFlicker {
              0%, 100% { transform: scale(1) skewX(0deg); opacity: 0.95; }
              50% { transform: scale(0.97, 1.05) skewX(2deg); opacity: 1; }
            }
            @keyframes svgOrbitalSpin {
              from { transform: rotate(0deg); }
              to { transform: rotate(360deg); }
            }
            @keyframes svgBubbleRise {
              0% { transform: translateY(0px) scale(0.8); opacity: 0.4; }
              50% { transform: translateY(-20px) scale(1.1); opacity: 0.9; }
              100% { transform: translateY(-42px) scale(0.6); opacity: 0.0; }
            }
            @keyframes svgRadioPulse {
              0%, 100% { opacity: 0.4; transform: scale(1); }
              50% { opacity: 0.95; transform: scale(1.08); }
            }

            .svg-anim-breathe { animation: svgBreathing 3.6s ease-in-out infinite; transform-origin: 50% 100%; }
            .svg-anim-blink { animation: svgEyeBlink 4.2s infinite; transform-origin: 50% 50%; }
            .svg-anim-sweat { animation: svgSweatDrop 1.8s infinite; }
            .svg-anim-dust { animation: svgDustFloat 6.0s ease-in-out infinite; }
            .svg-anim-alert { animation: svgAlertPop 1.6s cubic-bezier(0.34, 1.56, 0.64, 1) infinite; transform-origin: 50% 50%; }
            .svg-anim-candle { animation: svgCandleFlicker 1.4s infinite alternate; transform-origin: 50% 100%; }
            .svg-anim-orbital { animation: svgOrbitalSpin 8s linear infinite; transform-origin: 0 0; }
            .svg-anim-bubble { animation: svgBubbleRise 2.4s ease-in-out infinite; }
            .svg-anim-pulse { animation: svgRadioPulse 2.0s ease-in-out infinite; transform-origin: 50% 50%; }
          </style>

          <filter id="bg-gaussian-node" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3.5"/>
          </filter>
          <filter id="soft-shadow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur in="SourceAlpha" stdDeviation="10"/>
            <feOffset dx="0" dy="16"/>
            <feComponentTransfer><feFuncA type="linear" slope="0.45"/></feComponentTransfer>
            <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
          <filter id="glow-gold" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="16" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
          <filter id="glow-teal" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="14" result="blur"/>
            <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>

          <pattern id="ancient-stone-pattern" width="160" height="90" patternUnits="userSpaceOnUse">
            <rect width="160" height="90" fill="#181410"/>
            <rect x="2" y="2" width="76" height="41" fill="#221b14" rx="2" stroke="#0e0a07" stroke-width="2"/>
            <rect x="82" y="2" width="76" height="41" fill="#261e16" rx="2" stroke="#0e0a07" stroke-width="2"/>
            <rect x="42" y="47" width="76" height="41" fill="#1f1812" rx="2" stroke="#0e0a07" stroke-width="2"/>
          </pattern>
          <pattern id="brick-wall-pattern" width="120" height="60" patternUnits="userSpaceOnUse">
            <rect width="120" height="60" fill="#1c1917"/>
            <rect x="2" y="2" width="56" height="26" fill="#292524" rx="1" stroke="#0c0a09" stroke-width="1.5"/>
            <rect x="62" y="2" width="56" height="26" fill="#262220" rx="1" stroke="#0c0a09" stroke-width="1.5"/>
          </pattern>
          <pattern id="wood-panel-pattern" width="100" height="200" patternUnits="userSpaceOnUse">
            <rect width="100" height="200" fill="#271810"/>
            <rect x="3" y="0" width="94" height="200" fill="#382216" stroke="#160d08" stroke-width="2"/>
          </pattern>

          <linearGradient id="warm-volumetric-beam" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#fef08a" stop-opacity="0.42"/>
            <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
          </linearGradient>
          <linearGradient id="cool-window-spill" x1="100%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.32"/>
            <stop offset="100%" stop-color="#0c4a6e" stop-opacity="0"/>
          </linearGradient>
          <radialGradient id="vignette-overlay" cx="50%" cy="50%" r="68%">
            <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
            <stop offset="100%" stop-color="#000000" stop-opacity="0.82"/>
          </radialGradient>
        </defs>
        """

    @classmethod
    def draw_animated_prop(cls, prop_type, x, y, scale=1.0):
        """Draws rich animated hero props with micro-physics classes."""
        if prop_type == "erlenmeyer_flask":
            svg = f'<g id="prop-erlenmeyer" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <polygon points="-12,-60 12,-60 45,30 -45,30" fill="#38bdf8" opacity="0.35" stroke="#090a0f" stroke-width="4"/>\n'
            svg += '  <ellipse cx="0" cy="30" rx="45" ry="10" fill="#0284c7" stroke="#090a0f" stroke-width="4"/>\n'
            svg += '  <polygon points="-8,-40 8,-40 40,25 -40,25" fill="#22c55e" opacity="0.85"/>\n'
            svg += '  <circle class="svg-anim-bubble" cx="-10" cy="15" r="4" fill="#ffffff" opacity="0.8"/>\n'
            svg += '  <circle class="svg-anim-bubble" style="animation-delay: 0.8s;" cx="12" cy="10" r="5" fill="#ffffff" opacity="0.8"/>\n'
            svg += '</g>\n'
            return svg

        elif prop_type == "bohr_atom":
            svg = f'<g id="prop-bohr-atom" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <circle class="svg-anim-pulse" cx="0" cy="0" r="16" fill="#ef4444" filter="url(#glow-gold)"/>\n'
            svg += '  <g class="svg-anim-orbital">\n'
            svg += '    <ellipse cx="0" cy="0" rx="70" ry="24" fill="none" stroke="#38bdf8" stroke-width="3" opacity="0.8"/>\n'
            svg += '    <circle cx="70" cy="0" r="6" fill="#38bdf8"/>\n'
            svg += '  </g>\n</g>\n'
            return svg

        elif prop_type == "vacuum_tube_radio":
            svg = f'<g id="prop-radio" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <rect x="-60" y="-45" width="120" height="90" rx="8" fill="#451a03" stroke="#090a0f" stroke-width="5"/>\n'
            svg += '  <circle cx="-25" cy="0" r="24" fill="#0f172a" stroke="#d97706" stroke-width="3"/>\n'
            svg += '  <g class="svg-anim-pulse" transform="translate(25, -5)">\n'
            svg += '    <rect x="-10" y="-20" width="20" height="35" rx="10" fill="#fef08a" opacity="0.85" filter="url(#glow-gold)"/>\n'
            svg += '  </g>\n</g>\n'
            return svg

        elif prop_type == "stock_ticker_board":
            svg = f'<g id="prop-ticker" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <rect x="-80" y="-55" width="160" height="110" rx="6" fill="#090a0f" stroke="#050608" stroke-width="5"/>\n'
            svg += '  <rect x="-74" y="-49" width="148" height="98" fill="#022c22"/>\n'
            svg += '  <text x="-65" y="-20" font-family="monospace" font-size="12" fill="#ef4444" font-weight="bold">INDEX: -18.4% [CRASH]</text>\n'
            svg += '  <text x="-65" y="10" font-family="monospace" font-size="12" fill="#ef4444" font-weight="bold">PANIC SELLING</text>\n'
            svg += '</g>\n'
            return svg

        elif prop_type == "treaty_wax_seal_easel":
            svg = f'<g id="prop-treaty-easel" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <line x1="-30" y1="-80" x2="-50" y2="80" stroke="#78350f" stroke-width="7" stroke-linecap="round"/>\n'
            svg += '  <line x1="30" y1="-80" x2="50" y2="80" stroke="#78350f" stroke-width="7" stroke-linecap="round"/>\n'
            svg += '  <rect x="-45" y="-50" width="90" height="110" rx="4" fill="#fef3c7" stroke="#090a0f" stroke-width="4.5"/>\n'
            svg += '  <circle cx="0" cy="32" r="16" fill="#dc2626" stroke="#991b1b" stroke-width="3"/>\n'
            svg += '</g>\n'
            return svg

        elif prop_type == "flaming_torch":
            svg = f'<g id="prop-torch" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <rect x="-10" y="0" width="20" height="90" rx="4" fill="#78350f" stroke="#090a0f" stroke-width="4"/>\n'
            svg += '  <g class="svg-anim-candle">\n'
            svg += '    <path d="M 0 -70 C 25 -40 20 -10 0 0 C -20 -10 -25 -40 0 -70 Z" fill="#f59e0b" filter="url(#glow-gold)"/>\n'
            svg += '  </g>\n</g>\n'
            return svg

        return ""

    @classmethod
    def get_preset_scene(cls, preset_name):
        """Returns the complete scene configuration dict for master presets."""
        presets = {
            "ww2_cellar_resistance": {
                "title": "Underground Resistance Cellar",
                "era_badge": "OCCUPIED EUROPE • 1943",
                "bg_color": "#120f0d",
                "pattern": "brick-wall-pattern",
                "props": [{"type": "vacuum_tube_radio", "x": 420, "y": 620, "scale": 1.1}],
                "characters": [
                    {"cx": 820, "cy": 690, "name": "Operative", "pose": "ear_listening", "body_color": "#1e293b", "rim_color": "#38bdf8", "rim_side": "left"},
                    {"cx": 1240, "cy": 690, "name": "Analyst", "pose": "chin_stroke_thinking", "body_color": "#334155", "rim_color": "#fbbf24", "rim_side": "right"}
                ],
                "alert": {"x": 420, "y": 480, "text": "BROADCAST ALERT!", "bg_color": "#dc2626"}
            },
            "victorian_treaty_chamber": {
                "title": "Imperial Treaty Chamber",
                "era_badge": "1858 TREATY COUNCIL",
                "bg_color": "#170f0b",
                "pattern": "wood-panel-pattern",
                "props": [{"type": "treaty_wax_seal_easel", "x": 960, "y": 620, "scale": 1.3}],
                "characters": [
                    {"cx": 620, "cy": 680, "name": "Diplomat A", "pose": "arms_crossed_skeptical", "body_color": "#0f172a", "rim_color": "#fbbf24", "rim_side": "right"},
                    {"cx": 1320, "cy": 680, "name": "Diplomat B", "pose": "chin_stroke_thinking", "body_color": "#7c2d12", "rim_color": "#38bdf8", "rim_side": "left"}
                ],
                "alert": {"x": 960, "y": 420, "text": "TREATY SIGNED!", "bg_color": "#b45309"}
            },
            "great_depression_stock_crash": {
                "title": "Stock Exchange Crash",
                "era_badge": "FINANCIAL MARKET CRASH",
                "bg_color": "#0c0e12",
                "pattern": "brick-wall-pattern",
                "props": [{"type": "stock_ticker_board", "x": 960, "y": 440, "scale": 1.4}],
                "characters": [
                    {"cx": 650, "cy": 690, "name": "Banker", "pose": "head_clutch_panic", "body_color": "#1e293b", "rim_color": "#ef4444", "rim_side": "left"},
                    {"cx": 1280, "cy": 690, "name": "Trader", "pose": "shock_lean_back", "body_color": "#334155", "rim_color": "#ef4444", "rim_side": "right"}
                ],
                "alert": {"x": 960, "y": 280, "text": "PANIC: -90% WIPEOUT!", "bg_color": "#dc2626"}
            },
            "cold_war_bunker": {
                "title": "Secret Command Bunker",
                "era_badge": "COMMAND BUNKER • DEFCON 2",
                "bg_color": "#0d1117",
                "pattern": "brick-wall-pattern",
                "props": [
                    {"type": "bohr_atom", "x": 960, "y": 420, "scale": 1.4},
                    {"type": "erlenmeyer_flask", "x": 340, "y": 650, "scale": 1.2}
                ],
                "characters": [
                    {"cx": 620, "cy": 690, "name": "Commander", "pose": "ear_listening", "body_color": "#1e293b", "rim_color": "#ef4444", "rim_side": "left"},
                    {"cx": 1300, "cy": 690, "name": "Physicist", "pose": "head_clutch_panic", "body_color": "#334155", "rim_color": "#facc15", "rim_side": "right"}
                ],
                "alert": {"x": 960, "y": 260, "text": "ALERT RED!", "bg_color": "#dc2626"}
            }
        }
        return presets.get(preset_name, presets["ww2_cellar_resistance"])

    @classmethod
    def generate_scene(cls, scene_dict):
        """Builds a pristine 5-layer volumetric SVG string."""
        title = scene_dict.get("title", "Historical Scene")
        era_badge = scene_dict.get("era_badge", "HISTORICAL ARCHIVE")
        bg_color = scene_dict.get("bg_color", "#181410")
        pattern = scene_dict.get("pattern", "ancient-stone-pattern")
        props = scene_dict.get("props", [])
        characters = scene_dict.get("characters", [])
        alert = scene_dict.get("alert")

        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">\n'
        svg += cls.get_standard_defs()

        # LAYER 1: Deep Volumetric Background
        svg += '  <g id="layer-bg" filter="url(#bg-gaussian-node)">\n'
        svg += f'    <rect width="1920" height="1080" fill="{bg_color}"/>\n'
        svg += f'    <rect width="1920" height="1080" fill="url(#{pattern})" opacity="0.65"/>\n'
        svg += '    <path d="M 0 0 L 320 0 L 320 1080 L 0 1080 Z" fill="#0b0806" opacity="0.85"/>\n'
        svg += '    <path d="M 1600 0 L 1920 0 L 1920 1080 L 1600 1080 Z" fill="#0b0806" opacity="0.85"/>\n'
        svg += '    <path d="M 320 0 Q 960 220 1600 0 Z" fill="#0e0a08"/>\n'
        svg += '    <rect x="0" y="860" width="1920" height="220" fill="#080604"/>\n'
        svg += '    <line x1="0" y1="860" x2="1920" y2="860" stroke="#1f1812" stroke-width="4"/>\n'
        svg += '  </g>\n\n'

        # LAYER 2: Midground Props
        svg += '  <g id="layer-mg">\n'
        for p in props:
            svg += "    " + cls.draw_animated_prop(p.get("type"), p.get("x", 960), p.get("y", 540), p.get("scale", 1.0))
        svg += '  </g>\n\n'

        # LAYER 3: Character Rigs
        svg += '  <g id="layer-characters">\n'
        for char in characters:
            cx = char.get("cx", 960)
            cy = char.get("cy", 700)
            c_name = char.get("name", "Character")
            c_exp = char.get("expression", "neutral")

            svg += f'    <g id="char-{xml_escape(str(c_name)).lower().replace(" ", "-")}" transform="translate({cx - 160}, {cy - 220})">\n'
            svg += '      <ellipse cx="160" cy="425" rx="85" ry="18" fill="#020305" opacity="0.75" filter="url(#soft-shadow)"/>\n'
            svg += '      <g class="svg-anim-breathe">\n'
            svg += f'        <rect x="114" y="214" width="92" height="116" rx="14" fill="{char.get("body_color", "#1e293b")}" stroke="#050608" stroke-width="5"/>\n'
            svg += '        <rect x="126" y="325" width="26" height="75" fill="#0f172a" stroke="#050608" stroke-width="4.5"/>\n'
            svg += '        <rect x="168" y="325" width="26" height="75" fill="#0f172a" stroke="#050608" stroke-width="4.5"/>\n'
            svg += '        <ellipse cx="160" cy="144" rx="60" ry="68" fill="#ffffff" stroke="#050608" stroke-width="5.5"/>\n'
            svg += '        <g class="svg-anim-blink">\n'
            svg += '          <circle cx="140" cy="144" r="5" fill="#050608"/>\n'
            svg += '          <circle cx="180" cy="144" r="5" fill="#050608"/>\n'
            svg += '        </g>\n'
            if c_exp in ["shocked", "panicked"]:
                svg += '        <ellipse cx="160" cy="186" rx="12" ry="16" fill="#050608"/>\n'
            else:
                svg += '        <line x1="150" y1="186" x2="170" y2="186" stroke="#050608" stroke-width="4.5" stroke-linecap="round"/>\n'
            svg += f'        <rect x="85" y="420" width="150" height="24" rx="4" fill="#0f172a" opacity="0.9"/>\n'
            svg += f'        <text x="160" y="437" font-family="Arial, sans-serif" font-weight="bold" font-size="12" fill="#ffffff" text-anchor="middle">{xml_escape(str(c_name))}</text>\n'
            svg += '      </g>\n'
            svg += '    </g>\n'
        svg += '  </g>\n\n'

        # LAYER 4: Atmospheric Lighting & Alert
        svg += '  <g id="layer-lighting">\n'
        svg += '    <polygon points="0,0 720,0 1100,1080 0,1080" fill="url(#warm-volumetric-beam)"/>\n'
        svg += '    <polygon points="1920,0 1200,0 820,1080 1920,1080" fill="url(#cool-window-spill)"/>\n'
        svg += '    <g class="svg-anim-dust">\n'
        svg += '      <circle cx="520" cy="380" r="3.5" fill="#fef08a" opacity="0.75" filter="url(#glow-gold)"/>\n'
        svg += '      <circle cx="1120" cy="410" r="3.0" fill="#38bdf8" opacity="0.7" filter="url(#glow-teal)"/>\n'
        svg += '    </g>\n'
        if alert:
            ax = alert.get("x", 960)
            ay = alert.get("y", 350)
            atext = alert.get("text", "ALERT!")
            abg = alert.get("bg_color", "#dc2626")
            svg += f'    <g id="alert-popup" class="svg-anim-alert" transform="translate({ax}, {ay})">\n'
            svg += f'      <rect x="-140" y="-30" width="280" height="60" rx="10" fill="{abg}" stroke="#ffffff" stroke-width="4.5" filter="url(#soft-shadow)"/>\n'
            svg += f'      <text x="0" y="10" font-family="Bangers, Impact, sans-serif" font-size="28" fill="#ffffff" text-anchor="middle" letter-spacing="1.5">{xml_escape(str(atext))}</text>\n'
            svg += '    </g>\n'
        svg += '  </g>\n\n'

        # LAYER 5: Global Post-FX
        svg += '  <g id="layer-global-postfx">\n'
        svg += '    <rect width="1920" height="1080" fill="url(#vignette-overlay)"/>\n'
        svg += '    <rect x="0" y="0" width="1920" height="1080" fill="none" stroke="#050608" stroke-width="14"/>\n'
        svg += '    <g id="era-badge" transform="translate(60, 55)">\n'
        svg += '      <rect x="0" y="0" width="380" height="42" rx="6" fill="#050608" opacity="0.88" stroke="#facc15" stroke-width="2.5"/>\n'
        svg += f'      <text x="190" y="27" font-family="Arial, sans-serif" font-weight="900" font-size="14" fill="#facc15" text-anchor="middle" letter-spacing="1.5">{xml_escape(str(era_badge))}</text>\n'
        svg += '    </g>\n'
        svg += '  </g>\n'
        svg += '</svg>\n'
        return svg

    @classmethod
    def generate_interactive_movie_html(cls, scene_dict, shots_list, out_html_path):
        """
        Generates master scene_X_movie.html containing hybrid 2.5D GSAP master timeline,
        HTML5 canvas skeletal puppets, and dynamic camera choreography.
        """
        svg_content = cls.generate_scene(scene_dict)
        shots_json_str = json.dumps(shots_list or [])

        # Generate companion tactical map cutaway SVG from GeoJsonMapEngine
        map_svg_content = GeoJsonMapEngine.render_map_cutaway_svg(
            region="europe",
            highlight_color="#38bdf8",
            title=f"STRATEGIC MAP • {scene_dict.get('era_badge', 'TACTICAL THEATER')}"
        )

        # Load skeletal puppet engine script for inlining
        engine_js_path = Path(__file__).resolve().parent / "skeletal_puppet_engine.js"
        engine_js_content = ""
        if engine_js_path.is_file():
            with open(engine_js_path, "r", encoding="utf-8") as f:
                engine_js_content = f.read()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{scene_dict.get('title', 'Movie Stage')}</title>
  <style>
    body, html {{
      margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden;
      background: #000000; display: flex; align-items: center; justify-content: center;
      font-family: 'Inter', sans-serif;
    }}
    #viewport {{
      width: 1920px; height: 1080px; position: relative; overflow: hidden;
      background: #050811;
    }}
    #camera-rig {{
      width: 1920px; height: 1080px; position: absolute; left: 0; top: 0;
      transform-origin: 50% 50%;
    }}
    #layer-bg-plane {{
      position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;
      transition: filter 0.3s ease;
    }}
    #actors-canvas {{
      position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;
      pointer-events: none;
    }}
    #overlay-ui {{
      position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;
      pointer-events: none;
    }}
    #subtitles-box {{
      position: absolute; bottom: 80px; width: 100%; text-align: center;
      color: #ffffff; font-size: 38px; font-weight: 800; text-shadow: 0 4px 12px rgba(0,0,0,0.9);
    }}
    .sub-highlight {{
      color: #facc15; display: inline-block; transform: scale(1.12);
    }}
  </style>
</head>
<body>
  <div id="viewport">
    <div id="camera-rig">
      <div id="layer-bg-plane">
        {svg_content}
      </div>
      <div id="layer-map-plane" style="position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; display: none;">
        {map_svg_content}
      </div>
      <canvas id="actors-canvas" width="1920" height="1080"></canvas>
    </div>

    <!-- Pinned Screen-Space Post-FX & Subtitles -->
    <div id="overlay-ui">
      <div id="subtitles-box"><span id="subtitle-text"></span></div>
    </div>
  </div>

  <script>
    {engine_js_content}

    const SHOTS = {shots_json_str};
    const canvas = document.getElementById("actors-canvas");
    const ctx = canvas.getContext("2d");
    const cameraRig = document.getElementById("camera-rig");
    const bgPlane = document.getElementById("layer-bg-plane");
    const subText = document.getElementById("subtitle-text");
    const mapPlane = document.getElementById("layer-map-plane");

    // Initialize Universal Skeletal Actors
    const actorLead = new SkeletalPuppet({{
      name: "Lead Actor", x: 680, y: 840, scale: 1.15, facing: 1,
      coatColor: "#1e3a8a", vestColor: "#facc15", skinColor: "#f8fafc"
    }});

    const actorRival = new SkeletalPuppet({{
      name: "Rival Actor", x: 1240, y: 840, scale: 1.15, facing: -1,
      coatColor: "#7c2d12", vestColor: "#cbd5e1", skinColor: "#f8fafc"
    }});

    function doRenderFrame(timeSec) {{
      // 1. Locate active shot from shotlist
      let activeShot = null;
      for (const s of SHOTS) {{
        if (timeSec >= s.start && timeSec < s.end) {{
          activeShot = s;
          break;
        }}
      }}
      if (!activeShot && SHOTS.length > 0) {{
        activeShot = SHOTS[SHOTS.length - 1];
      }}

      // 2. Camera Choreography & Cutaways
      let isMapShot = false;
      if (activeShot) {{
        const cam = (activeShot.camera || "wide").toLowerCase();
        if (cam === "map" || cam === "map_cutaway") {{
          isMapShot = true;
          bgPlane.style.display = "none";
          if (mapPlane) mapPlane.style.display = "block";
          cameraRig.style.transform = "scale(1.0) translate(0px, 0px)";
          bgPlane.style.filter = "none";
        }} else {{
          bgPlane.style.display = "block";
          if (mapPlane) mapPlane.style.display = "none";

          if (cam === "closeup" || cam === "macro") {{
            cameraRig.style.transform = "scale(1.4) translate(-80px, -60px)";
            bgPlane.style.filter = "blur(7px)";
          }} else if (cam === "data_infographic" || cam === "infographic") {{
            cameraRig.style.transform = "scale(1.22) translate(0px, 35px)";
            bgPlane.style.filter = "blur(1.5px)";
          }} else if (cam === "medium") {{
            cameraRig.style.transform = "scale(1.18) translate(-40px, -20px)";
            bgPlane.style.filter = "blur(3.5px)";
          }} else {{
            cameraRig.style.transform = "scale(1.0) translate(0px, 0px)";
            bgPlane.style.filter = "blur(0px)";
          }}
        }}

        // Subtitles update
        if (activeShot.text) {{
          subText.innerHTML = activeShot.text;
        }}
      }}

      // 3. Clear Canvas & Update Skeletal Rigs
      ctx.clearRect(0, 0, 1920, 1080);

      if (!isMapShot) {{
        // Procedural behavior updates
        const isLeadSpeaking = Math.sin(timeSec * 3.5) > 0.1;
        actorLead.update(timeSec, isLeadSpeaking ? "talk" : "idle", {{ isSpeaking: isLeadSpeaking }});
        actorRival.update(timeSec, "idle", {{ isSpeaking: false }});

        // Render onto canvas
        actorLead.renderCanvas(ctx);
        actorRival.renderCanvas(ctx);
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
        out_path = Path(out_html_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"🎬 Generated Hybrid Movie HTML: {out_path.name}")
        return str(out_path)


def rasterize_svg_with_chrome(svg_path, output_png_path, width=1920, height=1080):
    abs_svg = os.path.abspath(svg_path).replace("\\", "/")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={os.path.abspath(output_png_path)}",
        f"file:///{abs_svg}"
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Pristine PNG rasterized: {output_png_path}")
        return True
    except Exception as e:
        print(f"⚠️ Error rasterizing SVG via Chrome: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate 1920x1080 Self-Animating Master SVGs")
    parser.add_argument("--scene", default=None)
    parser.add_argument("--config", default=None)
    parser.add_argument("--html", default=None)
    parser.add_argument("--out", default="master_scene.svg")
    parser.add_argument("--rasterize", default=None)
    args = parser.parse_args()

    scene_data = None
    if args.config and os.path.isfile(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            scene_data = json.load(f)
    elif args.scene:
        scene_data = CinematicSvgEngine.get_preset_scene(args.scene)
    else:
        scene_data = CinematicSvgEngine.get_preset_scene("ww2_cellar_resistance")

    svg_content = CinematicSvgEngine.generate_scene(scene_data)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"🎬 Self-Animating Master SVG generated: {args.out}")

    if args.html:
        CinematicSvgEngine.generate_interactive_movie_html(scene_data, [], args.html)

    if args.rasterize:
        rasterize_svg_with_chrome(args.out, args.rasterize)


if __name__ == "__main__":
    main()
