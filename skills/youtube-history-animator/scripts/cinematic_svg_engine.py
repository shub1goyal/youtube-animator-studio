"""
cinematic_svg_engine.py
The Master Hybrid 2.5D Volumetric + GeoJSON + Skeletal Actor Vector Scene Engine for YouTube Animation Studio.
Generates broadcast-grade 1920x1080 master stages and scene_X_movie.html deterministic Playwright players
with GSAP-style multi-plane camera easing, skeletal IK puppets, tactile map cutaways, and interactive HTML.
"""

import os
import re
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
from geojson_map_engine import GeoJsonMapEngine, extract_countries_from_text
from hybrid_asset_generator import HybridAssetGenerator
from vector_prop_library import VectorPropLibrary


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
        """Draws rich animated hero props using vector_prop_library Iconify integration and parametric vector Bezier."""
        if prop_type == "war_briefing_table":
            # 3D Perspective Heavy Briefing Table (Waist height, 160px tall, Y: 740..900)
            svg = f'<g id="prop-briefing-table" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <!-- Ground Contact Shadow -->\n'
            svg += '  <ellipse cx="0" cy="145" rx="380" ry="24" fill="#020408" opacity="0.8"/>\n'
            svg += '  <!-- Table Legs with Metallic Base -->\n'
            svg += '  <rect x="-310" y="25" width="34" height="120" rx="3" fill="#0f172a" stroke="#050608" stroke-width="5"/>\n'
            svg += '  <rect x="276" y="25" width="34" height="120" rx="3" fill="#0f172a" stroke="#050608" stroke-width="5"/>\n'
            svg += '  <rect x="-17" y="25" width="34" height="120" rx="3" fill="#090d16" stroke="#050608" stroke-width="5"/>\n'
            # 3D Trapezoidal Top Surface
            svg += '  <!-- 3D Trapezoidal Tabletop -->\n'
            svg += '  <polygon points="-360,25 360,25 320,-35 -320,-35" fill="#334155" stroke="#050608" stroke-width="6"/>\n'
            svg += '  <!-- Front Beveled Apron -->\n'
            svg += '  <rect x="-360" y="25" width="720" height="30" rx="4" fill="#1e293b" stroke="#050608" stroke-width="6"/>\n'
            # Tabletop Inset Tactical Map Pad
            svg += '  <polygon points="-160,20 160,20 140,-25 -140,-25" fill="#fef08a" opacity="0.9" stroke="#050608" stroke-width="3"/>\n'
            # Status Lights Panel on Table Front
            svg += '  <circle cx="-310" cy="40" r="5" fill="#22c55e"/>\n'
            svg += '  <circle cx="-290" cy="40" r="5" fill="#ef4444"/>\n'
            svg += '  <circle cx="-270" cy="40" r="5" fill="#facc15"/>\n'
            svg += '</g>\n'
            return svg

        # Check vector_prop_library for rich SVG prop
        prop_svg = VectorPropLibrary.get_prop_svg(prop_type, width=int(120*scale), height=int(120*scale))
        if prop_svg and "<svg" in prop_svg:
            clean_markup = prop_svg
            # Strip outer <svg ...> and </svg> to embed neatly into a <g>
            clean_markup = re.sub(r'<\?xml[^>]*\?>', '', clean_markup)
            clean_markup = re.sub(r'<svg[^>]*>', '', clean_markup, count=1)
            clean_markup = re.sub(r'</svg>\s*$', '', clean_markup)
            svg = f'<g id="prop-{prop_type}" transform="translate({x}, {y}) scale({scale})">\n'
            svg += clean_markup
            svg += '\n</g>\n'
            return svg

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

        elif prop_type == "war_briefing_table":
            svg = f'<g id="prop-briefing-table" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <!-- Heavy Steel War Room Briefing Table -->\n'
            svg += '  <rect x="-320" y="-30" width="640" height="45" rx="6" fill="#1e293b" stroke="#050608" stroke-width="5"/>\n'
            svg += '  <rect x="-310" y="-24" width="620" height="12" fill="#334155"/>\n'
            svg += '  <!-- Tactical Grid Inset -->\n'
            svg += '  <rect x="-260" y="-12" width="520" height="20" rx="3" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" opacity="0.85"/>\n'
            svg += '  <!-- Table Legs -->\n'
            svg += '  <rect x="-290" y="15" width="28" height="150" fill="#0f172a" stroke="#050608" stroke-width="4"/>\n'
            svg += '  <rect x="262" y="15" width="28" height="150" fill="#0f172a" stroke="#050608" stroke-width="4"/>\n'
            svg += '  <rect x="-14" y="15" width="28" height="150" fill="#090d16" stroke="#050608" stroke-width="4"/>\n'
            svg += '  <!-- Status Indicators / Tactical Map Dossier on Table -->\n'
            svg += '  <rect x="-180" y="-22" width="60" height="8" rx="2" fill="#ef4444" opacity="0.9"/>\n'
            svg += '  <rect x="-100" y="-22" width="60" height="8" rx="2" fill="#facc15" opacity="0.9"/>\n'
            svg += '  <rect x="60" y="-24" width="110" height="16" rx="2" fill="#fef3c7" stroke="#050608" stroke-width="1.5"/>\n'
            svg += '  <line x1="70" y1="-16" x2="160" y2="-16" stroke="#b45309" stroke-width="2"/>\n'
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
                    {"type": "war_briefing_table", "x": 960, "y": 760, "scale": 1.0},
                    {"type": "hotline_phone", "x": 840, "y": 710, "scale": 0.85},
                    {"type": "map_folder", "x": 1080, "y": 715, "scale": 0.85}
                ],
                "characters": [
                    {"cx": 580, "cy": 890, "name": "Commander", "pose": "ear_listening", "body_color": "#1e3a8a", "rim_color": "#ef4444", "rim_side": "left"},
                    {"cx": 1340, "cy": 890, "name": "Analyst", "pose": "chin_stroke_thinking", "body_color": "#7f1d1d", "rim_color": "#facc15", "rim_side": "right"}
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

        # Check if an AI-synthesized background or procedural SVG environment exists
        ai_bg_data_uri = scene_dict.get("ai_background_uri")
        if not ai_bg_data_uri:
            # Attempt to fetch/load free Flux background or cached background
            ai_bg_data_uri = HybridAssetGenerator.fetch_free_ai_background(
                scene_dict.get("title", "command bunker war room interior"),
                env_type="war_room_bunker"
            )

        # LAYER 1: Deep Volumetric Background
        svg += '  <g id="layer-bg" filter="url(#bg-gaussian-node)">\n'
        if ai_bg_data_uri:
            svg += f'    <image href="{ai_bg_data_uri}" width="1920" height="1080" preserveAspectRatio="xMidYMid slice"/>\n'
            svg += '    <rect width="1920" height="1080" fill="#000000" opacity="0.15"/>\n'
        else:
            svg += f'    <rect width="1920" height="1080" fill="{bg_color}"/>\n'
            svg += f'    <rect width="1920" height="1080" fill="url(#{pattern})" opacity="0.65"/>\n'
            # Center-Wall Focal Element: Giant Illuminated DEFCON Tactical Monitor
            svg += '    <rect x="460" y="120" width="1000" height="460" rx="8" fill="#021f18" stroke="#0f172a" stroke-width="6"/>\n'
            svg += '    <rect x="475" y="135" width="970" height="430" rx="4" fill="#01140f" stroke="#047857" stroke-width="2"/>\n'
            svg += '    <text x="960" y="175" font-family="monospace" font-size="22" fill="#34d399" font-weight="900" text-anchor="middle" letter-spacing="2">DEFCON 2 • STRATEGIC THEATER COMMAND</text>\n'
            svg += '    <circle cx="960" cy="360" r="140" fill="none" stroke="#059669" stroke-width="1.5" stroke-dasharray="6,6"/>\n'
            svg += '    <circle cx="960" cy="360" r="70" fill="none" stroke="#059669" stroke-width="1.5"/>\n'
            svg += '    <line x1="780" y1="360" x2="1140" y2="360" stroke="#059669" stroke-width="1.5"/>\n'
            # Side panels
            svg += '    <path d="M 0 0 L 240 0 L 240 1080 L 0 1080 Z" fill="#0b0806" opacity="0.72"/>\n'
            svg += '    <path d="M 1680 0 L 1920 0 L 1920 1080 L 1680 1080 Z" fill="#0b0806" opacity="0.72"/>\n'
            svg += '    <rect x="0" y="880" width="1920" height="200" fill="#080604"/>\n'
            svg += '    <line x1="0" y1="880" x2="1920" y2="880" stroke="#1f1812" stroke-width="4"/>\n'
        svg += '  </g>\n\n'

        # LAYER 2: Midground Props
        svg += '  <g id="layer-mg">\n'
        for p in props:
            svg += "    " + cls.draw_animated_prop(p.get("type"), p.get("x", 960), p.get("y", 540), p.get("scale", 1.0))
        svg += '  </g>\n\n'

        # NOTE: Layer 3 (Character Rigs) is intentionally omitted — characters are rendered
        # exclusively as Canvas skeletal puppets in generate_interactive_movie_html() to
        # prevent ghost-clone duplicates (static SVG chars behind canvas actors).

        # LAYER 4: Atmospheric Lighting & Alert (Crisp, clean, no muddy circles)
        svg += '  <g id="layer-lighting">\n'
        svg += '    <g class="svg-anim-dust">\n'
        svg += '      <circle cx="520" cy="380" r="3.5" fill="#fef08a" opacity="0.65" filter="url(#glow-gold)"/>\n'
        svg += '      <circle cx="1120" cy="410" r="3.0" fill="#38bdf8" opacity="0.6" filter="url(#glow-teal)"/>\n'
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

        # Detect target countries from scene shots narration for smart GeoJSON map
        detected_countries = []
        for s in (shots_list or []):
            if s.get("text"):
                for c in extract_countries_from_text(s["text"]):
                    if c not in detected_countries:
                        detected_countries.append(c)

        # Generate companion tactical map cutaway SVG from GeoJsonMapEngine
        map_region = "cuba_missile" if any("cuba" in c.lower() for c in detected_countries) else "cold_war"
        map_svg_content = GeoJsonMapEngine.render_map_cutaway_svg(
            region=map_region,
            highlight_countries=detected_countries if detected_countries else None,
            highlight_color="#38bdf8",
            target_color="#ef4444",
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
      position: absolute; bottom: 55px; width: 100%; text-align: center;
      pointer-events: none; z-index: 50;
    }}
    #subtitle-pill {{
      display: inline-block; background: rgba(5,6,8,0.84);
      border: 2px solid rgba(250,204,21,0.45); border-radius: 38px;
      padding: 10px 42px; max-width: 1540px;
      color: #ffffff; font-family: 'Inter', 'Arial Black', sans-serif;
      font-size: 42px; font-weight: 800; line-height: 1.35;
      text-shadow: 0 3px 10px rgba(0,0,0,0.95);
      white-space: normal; word-break: break-word;
    }}
    .sub-highlight {{
      color: #facc15; display: inline-block; transform: scale(1.12);
    }}
    #comic-alert-badge {{
      position: absolute; left: 880px; top: 180px; z-index: 40;
      display: none; pointer-events: none;
      transform-origin: 50% 50%;
    }}
    .badge-pop {{
      animation: alertPopSpring 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }}
    @keyframes alertPopSpring {{
      0% {{ transform: scale(0) rotate(-12deg); opacity: 0; }}
      70% {{ transform: scale(1.22) rotate(4deg); opacity: 1; }}
      100% {{ transform: scale(1.0) rotate(-2deg); opacity: 1; }}
    }}
  </style>
</head>
<body>
  <div id="viewport">
    <div id="camera-rig">
      <div id="layer-bg-plane">
        {svg_content}
      </div>
      <div id="layer-map-plane" style="position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; display: none; transform-origin: 50% 50%;">
        {map_svg_content}
      </div>
      <canvas id="actors-canvas" width="1920" height="1080"></canvas>
    </div>

    <!-- Comic Alert Callout Badge for Climax / Closeup -->
    <div id="comic-alert-badge">
      <svg width="340" height="120" viewBox="0 0 340 120">
        <polygon points="10,60 30,20 80,30 130,10 170,28 220,8 260,32 310,18 330,60 310,102 260,88 210,112 170,92 120,110 70,90 20,104" fill="#dc2626" stroke="#ffffff" stroke-width="6"/>
        <text x="170" y="70" font-family="'Impact', 'Bangers', Arial Black, sans-serif" font-size="38" font-weight="900" fill="#facc15" text-anchor="middle" letter-spacing="2">DEFCON 2!!</text>
      </svg>
    </div>

    <!-- Pinned Screen-Space Post-FX & Subtitles -->
    <div id="overlay-ui">
      <div id="subtitles-box"><span id="subtitle-pill"><span id="subtitle-text"></span></span></div>
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
      name: "Lead Actor", x: 580, y: 890, scale: 1.15, facing: 1,
      coatColor: "#1e3a8a", vestColor: "#facc15", skinColor: "#fae3cb",
      hatType: "peaked_cap", tieColor: "#dc2626"
    }});

    const actorRival = new SkeletalPuppet({{
      name: "Rival Actor", x: 1340, y: 890, scale: 1.15, facing: -1,
      coatColor: "#7f1d1d", vestColor: "#cbd5e1", skinColor: "#fae3cb",
      hasGlasses: true
    }});

    const comicBadge = document.getElementById("comic-alert-badge");

    // Helper: Build rolling 6-word phrase chunks with gold active-word highlight (ZERO "..." truncation)
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

      // Determine active word index across full sentence
      const activeWordIdx = Math.min(Math.floor(progress * words.length), words.length - 1);

      // Determine active 6-word chunk
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

      // 2. Camera Choreography, Smooth Map Zoom-In & Closeups
      let isMapShot = false;
      if (activeShot) {{
        const cam = (activeShot.camera || "wide").toLowerCase();
        const shotDuration = Math.max(activeShot.end - activeShot.start, 0.1);
        const shotProgress = Math.max(0, Math.min((timeSec - activeShot.start) / shotDuration, 1.0));

        if (cam === "map" || cam === "map_cutaway") {{
          isMapShot = true;
          bgPlane.style.display = "none";
          if (mapPlane) {{
            mapPlane.style.display = "block";
            // Retrieve target centroid for centered camera pan & zoom
            let targetX = 720.0;
            let targetY = 560.0;
            const svgRoot = mapPlane.querySelector("svg");
            if (svgRoot && svgRoot.hasAttribute("data-target-x")) {{
              targetX = parseFloat(svgRoot.getAttribute("data-target-x")) || 720.0;
              targetY = parseFloat(svgRoot.getAttribute("data-target-y")) || 560.0;
            }}
            mapPlane.style.transformOrigin = `${{targetX}}px ${{targetY}}px`;
            // Smooth quintic push-in 1.0x -> 2.6x keeping target centered
            const easeP = 6 * Math.pow(shotProgress, 5) - 15 * Math.pow(shotProgress, 4) + 10 * Math.pow(shotProgress, 3);
            const currentZoom = 1.0 + easeP * 1.6;
            const panX = (960.0 - targetX) * easeP * 0.45;
            const panY = (540.0 - targetY) * easeP * 0.45;
            mapPlane.style.transform = `translate(${{panX.toFixed(1)}}px, ${{panY.toFixed(1)}}px) scale(${{currentZoom.toFixed(3)}})`;
          }}
          cameraRig.style.transform = "scale(1.0) translate(0px, 0px)";
          bgPlane.style.filter = "none";
          if (comicBadge) comicBadge.style.display = "none";
        }} else {{
          bgPlane.style.display = "block";
          if (mapPlane) mapPlane.style.display = "none";

          if (cam === "closeup" || cam === "macro") {{
            // True 2.2x Close-Up focused directly onto speaking commander's chest & head (580, 600)
            cameraRig.style.transform = "scale(2.15) translate(280px, 90px)";
            bgPlane.style.filter = "blur(8px)";
            // Trigger Comic Alert Callout Badge
            if (comicBadge) {{
              comicBadge.style.display = "block";
              comicBadge.className = "badge-pop";
            }}
          }} else if (cam === "data_infographic" || cam === "infographic") {{
            cameraRig.style.transform = "scale(1.22) translate(0px, 35px)";
            bgPlane.style.filter = "none";
            if (comicBadge) comicBadge.style.display = "none";
          }} else if (cam === "medium") {{
            cameraRig.style.transform = "scale(1.18) translate(-40px, -20px)";
            bgPlane.style.filter = "none";
            if (comicBadge) comicBadge.style.display = "none";
          }} else {{
            cameraRig.style.transform = "scale(1.0) translate(0px, 0px)";
            bgPlane.style.filter = "none";
            if (comicBadge) comicBadge.style.display = "none";
          }}
        }}

        // Subtitles with zero truncation and gold active-word highlight
        updateRollingSubtitles(activeShot, timeSec);
      }}

      // 3. Clear Canvas & Update Skeletal Rigs
      ctx.clearRect(0, 0, 1920, 1080);

      if (!isMapShot) {{
        // Procedural behavior & acting
        const isLeadSpeaking = Math.sin(timeSec * 3.5) > 0.1;
        // In wide opening, lead character walks in for first 1.2s, then gestures
        let leadPose = "idle";
        if (timeSec < 1.2) {{
          leadPose = "walk";
        }} else if (isLeadSpeaking) {{
          leadPose = "talk";
        }}
        actorLead.update(timeSec, leadPose, {{ isSpeaking: isLeadSpeaking }});
        // Secondary actor acts reactively (listens, looks at speaker, strokes chin)
        actorRival.update(timeSec, "idle", {{ isSpeaking: false, isListening: isLeadSpeaking }});

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
