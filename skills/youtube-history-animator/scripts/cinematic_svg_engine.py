"""
cinematic_svg_engine.py
The Master 5-Layer Volumetric + MapLore Self-Animating Vector Scene Engine for YouTube Animation Studio.
Generates broadcast-grade 1920x1080 master vector SVGs with embedded CSS @keyframes for continuous micro-physics
(breathing, eye blinking, sweat droplets, dust motes, alert popups, orbital rotations, bubbling glassware, spinning chakras, fluttering flags),
dual-temperature volumetric lighting, procedural architectural patterns, and articulated character rigs.
"""

import os
import sys
import argparse
import subprocess
import math
from xml.sax.saxutils import escape as xml_escape

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


class CinematicSvgEngine:
    """Master generator for broadcast-grade 1920x1080 historical and explainer vector scenes."""

    @staticmethod
    def get_standard_defs():
        """Returns the canonical <defs> stack with embedded self-contained CSS animations, blurs, blooms, and gradients."""
        return """
        <defs>
          <!-- ================================================================= -->
          <!-- 1. EMBEDDED SELF-CONTAINED CSS ANIMATIONS (Standalone SVG Movies)  -->
          <!-- ================================================================= -->
          <style type="text/css">
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&amp;family=Playfair+Display:ital,wght@0,700;1,400&amp;family=Bangers&amp;family=Noto+Sans+Devanagari:wght@700;900&amp;display=swap');

            /* Continuous Micro-Physics inside Standalone SVG */
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
            @keyframes svgPetalFloat {
              0% { transform: translate(0px, 0px) rotate(0deg); opacity: 0.85; }
              50% { transform: translate(35px, 60px) rotate(45deg); opacity: 0.95; }
              100% { transform: translate(70px, 130px) rotate(90deg); opacity: 0.2; }
            }
            @keyframes svgAlertPop {
              0%, 100% { transform: scale(1) rotate(-4deg); }
              50% { transform: scale(1.12) rotate(4deg); }
            }
            @keyframes svgCandleFlicker {
              0%, 100% { transform: scale(1) skewX(0deg); opacity: 0.95; }
              25% { transform: scale(1.08, 0.94) skewX(4deg); opacity: 0.85; }
              50% { transform: scale(0.95, 1.06) skewX(-5deg); opacity: 1; }
              75% { transform: scale(1.05, 0.97) skewX(3deg); opacity: 0.9; }
            }
            @keyframes svgOrbitalRotate {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
            @keyframes svgChakraSpin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }
            @keyframes svgFlagWave {
              0%, 100% { transform: skewY(0deg) scaleX(1); }
              50% { transform: skewY(2.5deg) scaleX(0.98); }
            }
            @keyframes svgBeakerBubble {
              0% { transform: translateY(0px); opacity: 0.2; }
              50% { opacity: 0.85; }
              100% { transform: translateY(-38px); opacity: 0.0; }
            }
            @keyframes svgRadiationPulse {
              0%, 100% { transform: scale(1); opacity: 0.75; }
              50% { transform: scale(1.08); opacity: 1; }
            }
            @keyframes svgPropellerSpin {
              0% { transform: rotate(0deg); }
              100% { transform: rotate(360deg); }
            }

            .svg-anim-breathe {
              transform-box: fill-box;
              transform-origin: bottom center;
              animation: svgBreathing 2.6s infinite ease-in-out;
            }
            .svg-anim-blink {
              transform-box: fill-box;
              transform-origin: center;
              animation: svgEyeBlink 4.5s infinite;
            }
            .svg-anim-sweat {
              animation: svgSweatDrop 1.8s infinite ease-in-out;
            }
            .svg-anim-dust {
              animation: svgDustFloat 4.2s infinite ease-in-out;
            }
            .svg-anim-petal {
              animation: svgPetalFloat 5.5s infinite ease-in-out;
            }
            .svg-anim-alert-badge {
              transform-box: fill-box;
              transform-origin: center bottom;
              animation: svgAlertPop 0.55s infinite ease-in-out;
            }
            .svg-anim-candle {
              transform-box: fill-box;
              transform-origin: bottom center;
              animation: svgCandleFlicker 1.4s infinite ease-in-out;
            }
            .svg-anim-orbit-1 {
              transform-box: fill-box;
              transform-origin: center;
              animation: svgOrbitalRotate 4.0s linear infinite;
            }
            .svg-anim-orbit-2 {
              transform-box: fill-box;
              transform-origin: center;
              animation: svgOrbitalRotate 5.5s linear infinite reverse;
            }
            .svg-anim-orbit-3 {
              transform-box: fill-box;
              transform-origin: center;
              animation: svgOrbitalRotate 7.0s linear infinite;
            }
            .svg-anim-chakra {
              transform-box: fill-box;
              transform-origin: center;
              animation: svgChakraSpin 8.0s linear infinite;
            }
            .svg-anim-flag {
              transform-box: fill-box;
              transform-origin: left center;
              animation: svgFlagWave 2.8s infinite ease-in-out;
            }
            .svg-anim-bubble {
              animation: svgBeakerBubble 2.2s infinite ease-in;
            }
            .svg-anim-radiation {
              transform-box: fill-box;
              transform-origin: center;
              animation: svgRadiationPulse 2.8s infinite ease-in-out;
            }
            .svg-anim-propeller {
              transform-box: fill-box;
              transform-origin: center;
              animation: svgPropellerSpin 0.15s linear infinite;
            }
          </style>

          <!-- 2. VOLUMETRIC GAUSSIAN BLURS -->
          <filter id="blur-soft" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="8"/>
          </filter>
          <filter id="blur-med" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="16"/>
          </filter>
          <filter id="blur-heavy" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="35"/>
          </filter>

          <!-- 3. VOLUMETRIC GLOWS & BLOOM -->
          <filter id="radio-bloom" x="-80%" y="-80%" width="260%" height="260%">
            <feGaussianBlur stdDeviation="10" result="b1"/>
            <feGaussianBlur stdDeviation="28" result="b2"/>
            <feMerge>
              <feMergeNode in="b2"/>
              <feMergeNode in="b1"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
          <filter id="glow-gold" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="14" result="b1"/>
            <feMerge>
              <feMergeNode in="b1"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
          <filter id="glow-saffron" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="18" result="b1"/>
            <feMerge>
              <feMergeNode in="b1"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>

          <!-- 4. LIGHTING & ATMOSPHERIC GRADIENTS -->
          <radialGradient id="sun-burst" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.95"/>
            <stop offset="35%" stop-color="#f59e0b" stop-opacity="0.6"/>
            <stop offset="70%" stop-color="#b45309" stop-opacity="0.2"/>
            <stop offset="100%" stop-color="#78350f" stop-opacity="0"/>
          </radialGradient>
          <linearGradient id="warm-godray" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#fef08a" stop-opacity="0.35"/>
            <stop offset="60%" stop-color="#f59e0b" stop-opacity="0.12"/>
            <stop offset="100%" stop-color="#b45309" stop-opacity="0.0"/>
          </linearGradient>
          <radialGradient id="cinematic-vignette" cx="50%" cy="50%" r="65%">
            <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
            <stop offset="85%" stop-color="#020409" stop-opacity="0.65"/>
            <stop offset="100%" stop-color="#000000" stop-opacity="0.95"/>
          </radialGradient>

          <!-- 5. PROCEDURAL TEXTURES -->
          <pattern id="brick-pattern" width="64" height="32" patternUnits="userSpaceOnUse">
            <rect width="64" height="32" fill="#171e2e"/>
            <path d="M 0 0 L 64 0 M 0 16 L 64 16 M 0 32 L 64 32" stroke="#0d131f" stroke-width="2"/>
            <path d="M 32 0 L 32 16 M 0 16 L 0 32 M 64 16 L 64 32" stroke="#0d131f" stroke-width="2"/>
          </pattern>
          <pattern id="ancient-stone-pattern" width="90" height="45" patternUnits="userSpaceOnUse">
            <rect width="90" height="45" fill="#2d2215"/>
            <path d="M 0 0 L 90 0 M 0 22.5 L 90 22.5 M 0 45 L 90 45" stroke="#1c140b" stroke-width="2.5"/>
            <path d="M 45 0 L 45 22.5 M 0 22.5 L 0 45 M 90 22.5 L 90 45" stroke="#1c140b" stroke-width="2.5"/>
          </pattern>
        </defs>
        """

    @classmethod
    def draw_animated_chibi(cls, cx, cy, name="Hero", hat=None, glasses=False, facial_hair=None,
                            expression="neutral", pose="standing", body_color="#1e293b",
                            tie_color="#dc2626", coat_type="suit", rim_color="#fbbf24",
                            rim_side="right", scale=1.0):
        """
        Renders a fully articulated OverSimplified character with:
          - Alive breathing on body & arms (.svg-anim-breathe)
          - Natural eye blinking (.svg-anim-blink)
          - Animated sweat beads (.svg-anim-sweat)
          - Coupled physical rim lighting
          - 7 Asymmetric gesture presets
        """
        svg = f'<g id="char-{name.lower().replace(" ", "_")}" transform="translate({cx}, {cy}) scale({scale})">\n'

        # Floor contact shadow (static)
        svg += '  <ellipse cx="0" cy="180" rx="90" ry="22" fill="#020306" opacity="0.75" filter="url(#blur-soft)"/>\n'

        # Legs (grounded)
        svg += '  <line x1="-25" y1="120" x2="-25" y2="180" stroke="#090a0f" stroke-width="14" stroke-linecap="round"/>\n'
        svg += '  <line x1="25" y1="120" x2="25" y2="180" stroke="#090a0f" stroke-width="14" stroke-linecap="round"/>\n'
        svg += '  <ellipse cx="-28" cy="182" rx="20" ry="10" fill="#090b10" stroke="#090a0f" stroke-width="4"/>\n'
        svg += '  <ellipse cx="28" cy="182" rx="20" ry="10" fill="#090b10" stroke="#090a0f" stroke-width="4"/>\n'

        # BREATHE GROUP: Torso, Arms, Head, Facial Features
        svg += '  <g class="svg-anim-breathe">\n'

        # Torso / Garment
        if coat_type == "labcoat":
            svg += f'    <path d="M -50 30 C -55 90 -55 150 -35 172 L 35 172 C 55 150 55 90 50 30 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="8" stroke-linejoin="round"/>\n'
            svg += f'    <path d="M -25 30 L 0 95 L 25 30 Z" fill="{body_color}" stroke="#090a0f" stroke-width="4"/>\n'
            svg += '    <line x1="0" y1="95" x2="0" y2="172" stroke="#090a0f" stroke-width="4"/>\n'
        elif coat_type == "royal_angavastram" or coat_type == "dhoti_kurta":
            svg += f'    <path d="M -55 30 C -60 90 -60 150 -40 172 L 40 172 C 60 150 60 90 55 30 Z" fill="{body_color}" stroke="#090a0f" stroke-width="8" stroke-linejoin="round"/>\n'
            # Golden sash / Angavastram draped diagonally
            svg += '    <path d="M -45 35 Q 0 85 45 145" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="round"/>\n'
            svg += '    <circle cx="0" cy="85" r="10" fill="#fbbf24" stroke="#090a0f" stroke-width="3"/>\n'
        elif coat_type == "nehru_jacket":
            svg += f'    <path d="M -50 30 C -55 90 -55 150 -35 172 L 35 172 C 55 150 55 90 50 30 Z" fill="{body_color}" stroke="#090a0f" stroke-width="8" stroke-linejoin="round"/>\n'
            # Mandarin collar & buttons
            svg += '    <rect x="-24" y="22" width="48" height="14" rx="4" fill="#090a0f"/>\n'
            svg += '    <line x1="0" y1="36" x2="0" y2="172" stroke="#090a0f" stroke-width="4"/>\n'
            svg += '    <circle cx="0" cy="65" r="3.5" fill="#fef08a"/>\n'
            svg += '    <circle cx="0" cy="95" r="3.5" fill="#fef08a"/>\n'
            svg += '    <circle cx="0" cy="125" r="3.5" fill="#fef08a"/>\n'
            # Pocket rose
            svg += '    <circle cx="28" cy="70" r="5" fill="#ef4444"/>\n'
        else:  # Standard Suit / Uniform
            svg += f'    <path d="M -50 30 C -55 90 -55 150 -35 172 L 35 172 C 55 150 55 90 50 30 Z" fill="{body_color}" stroke="#090a0f" stroke-width="8" stroke-linejoin="round"/>\n'
            svg += '    <polygon points="-25,30 0,90 25,30" fill="#ffffff" stroke="#090a0f" stroke-width="4"/>\n'
            svg += f'    <polygon points="-8,40 0,110 8,40" fill="{tie_color}" stroke="#090a0f" stroke-width="4"/>\n'

        # Motivated Rim Light on Torso
        if rim_color:
            if rim_side == "right":
                svg += f'    <path d="M 48 35 L 54 165" stroke="{rim_color}" stroke-width="6" stroke-linecap="round" opacity="0.85"/>\n'
            else:
                svg += f'    <path d="M -48 35 L -54 165" stroke="{rim_color}" stroke-width="6" stroke-linecap="round" opacity="0.85"/>\n'

        # Modular Arm Poses
        if pose == "pointing_up_board":
            svg += '    <path d="M -50 40 Q -85 80 -60 120" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="-58" cy="124" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="4.5"/>\n'
            svg += '    <path d="M 45 45 C 85 20 105 -25 125 -65" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="126" cy="-68" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="4.5"/>\n'
            svg += '    <rect x="122" y="-102" width="8" height="32" rx="2" fill="#fef08a" stroke="#090a0f" stroke-width="2" transform="rotate(22 126 -85)"/>\n'

        elif pose == "head_clutch_panic":
            svg += '    <path d="M -45 50 C -85 10 -80 -40 -50 -60" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="-50" cy="-62" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="4.5"/>\n'
            svg += '    <path d="M 45 50 C 85 10 80 -40 50 -60" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="50" cy="-62" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="4.5"/>\n'

        elif pose == "chin_stroke_thinking":
            svg += '    <path d="M -45 45 C -25 75 25 75 40 60" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="42" cy="60" r="12" fill="#ffffff" stroke="#090a0f" stroke-width="4"/>\n'
            svg += '    <path d="M 45 45 C 60 20 35 0 15 -10" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="15" cy="-10" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="4.5"/>\n'

        elif pose == "namaste_greeting":
            # Both hands folded in front of chest
            svg += '    <path d="M -50 45 C -30 70 -10 65 0 50" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <path d="M 50 45 C 30 70 10 65 0 50" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <polygon points="-8,35 0,15 8,35 0,55" fill="#ffffff" stroke="#090a0f" stroke-width="4"/>\n'

        elif pose == "sword_raised":
            # Right arm raised high holding sword
            svg += '    <path d="M -50 40 Q -80 80 -60 120" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="-58" cy="124" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="4.5"/>\n'
            svg += '    <path d="M 45 40 Q 80 0 75 -70" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="75" cy="-74" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="4.5"/>\n'
            # Ancient Steel Talwar Sword
            svg += '    <path d="M 75 -80 Q 90 -160 130 -220 Q 95 -165 75 -80 Z" fill="#e2e8f0" stroke="#090a0f" stroke-width="3" filter="url(#glow-gold)"/>\n'
            svg += '    <rect x="62" y="-85" width="26" height="6" rx="2" fill="#f59e0b" stroke="#090a0f" stroke-width="2"/>\n'

        else:  # Natural standing
            svg += '    <path d="M -50 40 Q -80 90 -65 130" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="-65" cy="134" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="4.5"/>\n'
            svg += '    <path d="M 50 40 Q 80 90 65 130" fill="none" stroke="#090a0f" stroke-width="18" stroke-linecap="round"/>\n'
            svg += '    <circle cx="65" cy="134" r="13" fill="#ffffff" stroke="#090a0f" stroke-width="4.5"/>\n'

        # Head Base
        svg += '    <circle cx="0" cy="-35" r="64" fill="#ffffff" stroke="#090a0f" stroke-width="8"/>\n'
        if rim_color:
            if rim_side == "right":
                svg += f'    <path d="M 0 -99 A 64 64 0 0 1 64 -35" fill="none" stroke="{rim_color}" stroke-width="7" stroke-linecap="round" opacity="0.85"/>\n'
            else:
                svg += f'    <path d="M 0 -99 A 64 64 0 0 0 -64 -35" fill="none" stroke="{rim_color}" stroke-width="7" stroke-linecap="round" opacity="0.85"/>\n'

        # Hats / Crowns / Turbans
        if hat == "ashoka_crown" or hat == "royal_mukut":
            # Golden Royal Crown
            svg += '    <polygon points="-48,-65 -36,-115 -14,-75 0,-130 14,-75 36,-115 48,-65" fill="#f59e0b" stroke="#090a0f" stroke-width="5" stroke-linejoin="round"/>\n'
            svg += '    <circle cx="0" cy="-132" r="7" fill="#ef4444" stroke="#090a0f" stroke-width="3"/>\n'
            svg += '    <circle cx="-36" cy="-117" r="5" fill="#38bdf8" stroke="#090a0f" stroke-width="2"/>\n'
            svg += '    <circle cx="36" cy="-117" r="5" fill="#38bdf8" stroke="#090a0f" stroke-width="2"/>\n'
            svg += '    <rect x="-48" y="-68" width="96" height="12" rx="4" fill="#d97706" stroke="#090a0f" stroke-width="4"/>\n'
        elif hat == "turban" or hat == "pagri":
            # Saffron / Royal Turban
            svg += '    <path d="M -60 -50 C -68 -105 -15 -125 0 -115 C 25 -125 68 -105 60 -50 Z" fill="#f97316" stroke="#090a0f" stroke-width="6"/>\n'
            svg += '    <path d="M -50 -70 Q 0 -95 50 -70" fill="none" stroke="#ea580c" stroke-width="5"/>\n'
            svg += '    <circle cx="0" cy="-85" r="9" fill="#fbbf24" stroke="#090a0f" stroke-width="3"/>\n'
        elif hat == "gandhi_topi":
            # White Khadi Cap
            svg += '    <path d="M -54 -55 C -45 -95 0 -105 45 -90 L 54 -55 Z" fill="#f8fafc" stroke="#090a0f" stroke-width="6"/>\n'
            svg += '    <line x1="-50" y1="-55" x2="50" y2="-55" stroke="#090a0f" stroke-width="5"/>\n'

        # Hair / Beard
        if facial_hair == "mustache":
            svg += '    <path d="M -22 -15 Q 0 -5 22 -15 Q 0 -22 -22 -15 Z" fill="#090a0f"/>\n'
        elif facial_hair == "royal_beard":
            svg += '    <path d="M -30 -25 C -20 15 0 25 20 15 L 30 -25" fill="#090a0f" stroke="#090a0f" stroke-width="3"/>\n'

        # BLINK GROUP: Eyes & Spectacles
        svg += '    <g class="svg-anim-blink">\n'
        if glasses:
            svg += '      <circle cx="-20" cy="-35" r="16" fill="none" stroke="#090a0f" stroke-width="4.5"/>\n'
            svg += '      <circle cx="20" cy="-35" r="16" fill="none" stroke="#090a0f" stroke-width="4.5"/>\n'
            svg += '      <line x1="-4" y1="-35" x2="4" y2="-35" stroke="#090a0f" stroke-width="4.5"/>\n'
            svg += '      <circle cx="-20" cy="-35" r="6" fill="#090a0f"/>\n'
            svg += '      <circle cx="20" cy="-35" r="6" fill="#090a0f"/>\n'
        elif expression == "shocked":
            svg += '      <ellipse cx="-20" cy="-35" rx="14" ry="18" fill="#ffffff" stroke="#090a0f" stroke-width="5"/>\n'
            svg += '      <circle cx="-20" cy="-35" r="6" fill="#090a0f"/>\n'
            svg += '      <ellipse cx="20" cy="-35" rx="14" ry="18" fill="#ffffff" stroke="#090a0f" stroke-width="5"/>\n'
            svg += '      <circle cx="20" cy="-35" r="6" fill="#090a0f"/>\n'
        else:
            svg += '      <circle cx="-20" cy="-35" r="7.5" fill="#090a0f"/>\n'
            svg += '      <circle cx="20" cy="-35" r="7.5" fill="#090a0f"/>\n'
            svg += '      <line x1="-28" y1="-50" x2="-12" y2="-50" stroke="#090a0f" stroke-width="4.5" stroke-linecap="round"/>\n'
            svg += '      <line x1="12" y1="-50" x2="28" y2="-50" stroke="#090a0f" stroke-width="4.5" stroke-linecap="round"/>\n'
        svg += '    </g>\n'

        # Mouth
        if expression == "shocked":
            svg += '    <ellipse cx="0" cy="-6" rx="12" ry="16" fill="#090a0f"/>\n'
            # Animated panic sweat
            svg += '    <path class="svg-anim-sweat" d="M 45 -55 C 52 -67 52 -77 45 -81 C 38 -77 38 -67 45 -55 Z" fill="#38bdf8" stroke="#090a0f" stroke-width="3"/>\n'
        elif expression == "smile":
            svg += '    <path d="M -16 -12 Q 0 4 16 -12" fill="none" stroke="#090a0f" stroke-width="5" stroke-linecap="round"/>\n'
        else:
            svg += '    <line x1="-12" y1="-10" x2="12" y2="-10" stroke="#090a0f" stroke-width="4.5" stroke-linecap="round"/>\n'

        svg += '  </g>\n'  # Close .svg-anim-breathe

        # Nameplate (static)
        svg += f'  <rect x="-75" y="195" width="150" height="28" rx="6" fill="#0f172a" opacity="0.9"/>\n'
        svg += f'  <text x="0" y="214" font-family="Arial, sans-serif" font-weight="bold" font-size="14" fill="#ffffff" text-anchor="middle">{xml_escape(str(name))}</text>\n'
        svg += '</g>\n'
        return svg

    @classmethod
    def draw_animated_prop(cls, prop_type, x, y, scale=1.0):
        """Draws animated hero props with embedded micro-physics classes."""
        if prop_type == "ashoka_chakra":
            svg = f'<g id="prop-ashoka-chakra" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <!-- Outer Golden Aura Bloom -->\n'
            svg += '  <circle cx="0" cy="0" r="130" fill="url(#sun-burst)" filter="url(#glow-gold)" opacity="0.6"/>\n'
            svg += '  <!-- Spinning Navy Chakra Core (24 Spokes) -->\n'
            svg += '  <g class="svg-anim-chakra">\n'
            svg += '    <circle cx="0" cy="0" r="100" fill="none" stroke="#1e3a8a" stroke-width="12"/>\n'
            svg += '    <circle cx="0" cy="0" r="22" fill="#1e3a8a"/>\n'
            for sp in range(24):
                deg = sp * 15
                rad = math.radians(deg)
                x2 = int(98 * math.cos(rad))
                y2 = int(98 * math.sin(rad))
                svg += f'    <line x1="0" y1="0" x2="{x2}" y2="{y2}" stroke="#1e3a8a" stroke-width="4.5"/>\n'
            svg += '  </g>\n'
            svg += '</g>\n'
            return svg

        elif prop_type == "tricolor_flag":
            svg = f'<g id="prop-indian-tricolor" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <!-- Staff / Flagpole -->\n'
            svg += '  <line x1="0" y1="-180" x2="0" y2="180" stroke="#94a3b8" stroke-width="8" stroke-linecap="round"/>\n'
            svg += '  <circle cx="0" cy="-185" r="10" fill="#f59e0b" stroke="#090a0f" stroke-width="3"/>\n'
            svg += '  <!-- Waving Flag Cloth -->\n'
            svg += '  <g class="svg-anim-flag" transform="translate(0, -170)">\n'
            # Saffron
            svg += '    <rect x="4" y="0" width="180" height="40" fill="#ff9933" stroke="#090a0f" stroke-width="2"/>\n'
            # White with mini chakra
            svg += '    <rect x="4" y="40" width="180" height="40" fill="#ffffff" stroke="#090a0f" stroke-width="2"/>\n'
            svg += '    <circle cx="94" cy="60" r="14" fill="none" stroke="#000080" stroke-width="2.5"/>\n'
            # Green
            svg += '    <rect x="4" y="80" width="180" height="40" fill="#138808" stroke="#090a0f" stroke-width="2"/>\n'
            svg += '  </g>\n'
            svg += '</g>\n'
            return svg

        elif prop_type == "flaming_torch":
            svg = f'<g id="prop-torch" transform="translate({x}, {y}) scale({scale})">\n'
            svg += '  <rect x="-10" y="0" width="20" height="90" rx="4" fill="#78350f" stroke="#090a0f" stroke-width="4"/>\n'
            svg += '  <polygon points="-20,0 20,0 12,24 -12,24" fill="#d97706" stroke="#090a0f" stroke-width="4"/>\n'
            # Animated Flickering Flame
            svg += '  <g class="svg-anim-candle">\n'
            svg += '    <path d="M 0 -70 C 25 -40 20 -10 0 0 C -20 -10 -25 -40 0 -70 Z" fill="#f59e0b" filter="url(#glow-saffron)"/>\n'
            svg += '    <path d="M 0 -45 C 14 -25 10 -6 0 0 C -10 -6 -14 -25 0 -45 Z" fill="#fef08a"/>\n'
            svg += '  </g>\n'
            svg += '</g>\n'
            return svg

        return ""

    @classmethod
    def draw_alert_badge(cls, x, y, text="!!", bg_color="#dc2626"):
        """Draws a comic alert badge with MapLore bounce physics and dual-script Devanagari/Roman font support."""
        svg = f'<g transform="translate({x}, {y})">\n'
        svg += f'  <g class="svg-anim-alert-badge">\n'
        burst_pts = []
        for i in range(12):
            ang = math.radians(i * 30)
            r = 45 if (i % 2 == 0) else 28
            burst_pts.append(f"{int(r * math.cos(ang))},{int(r * math.sin(ang))}")
        pts_str = " ".join(burst_pts)
        svg += f'    <polygon points="{pts_str}" fill="{bg_color}" stroke="#090a0f" stroke-width="5" filter="url(#glow-gold)"/>\n'
        svg += f'    <text x="0" y="10" font-family="Bangers, \'Nirmala UI\', \'Noto Sans Devanagari\', Impact, sans-serif" font-weight="bold" font-size="34" fill="#fef08a" text-anchor="middle" stroke="#090a0f" stroke-width="2">{xml_escape(str(text))}</text>\n'
        svg += '  </g>\n'
        svg += '</g>\n'
        return svg

    @classmethod
    def generate_scene(cls, scene_dict):
        """
        Builds a complete, broadcast-compliant 1920x1080 animated 5-layer SVG from a scene config dictionary.
        Enforces Rules A, B, C, D, E, F:
          Layer 1 (#layer-bg): Architectural pattern, left/right columns, ceiling/floor.
          Layer 2 (#layer-lighting): Motivated beams & warm/cyan emitters.
          Layer 3 (#layer-props): Hero animated props (Chakra, Torch, Atom, etc.).
          Layer 4 (#layer-characters): OverSimplified rigs with breathing, blinking, sweat.
          Layer 5 (#layer-vfx): 45px perimeter framing vignette & era badge.
        """
        title = xml_escape(str(scene_dict.get("title", "Historical Scene")))
        era = xml_escape(str(scene_dict.get("era_badge", "HISTORY • ERA")))
        bg_color = scene_dict.get("bg_color", "#111827")
        pattern = scene_dict.get("pattern", "ancient-stone-pattern")
        characters_data = scene_dict.get("characters", [])
        props_data = scene_dict.get("props", [])
        alert_data = scene_dict.get("alert", None)

        svg = f'''<svg id="master-svg" viewBox="0.0 0.0 1920.0 1080.0" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" class="w-full h-full block">
        {cls.get_standard_defs()}

        <!-- ========================================================================= -->
        <!-- LAYER 1: BACKGROUND & ARCHITECTURE (#layer-bg) - ZERO EMPTY VOID          -->
        <!-- ========================================================================= -->
        <g id="layer-bg">
          <!-- Back Wall Base -->
          <rect width="1920" height="1080" fill="{bg_color}"/>
          <!-- Procedural Architectural Texture -->
          <rect width="1920" height="850" fill="url(#{pattern})" opacity="0.65"/>

          <!-- Structural Ceiling Beams -->
          <rect x="0" y="0" width="1920" height="90" fill="#0f141e" stroke="#06090e" stroke-width="5"/>
          <line x1="480" y1="0" x2="480" y2="90" stroke="#06090e" stroke-width="8"/>
          <line x1="960" y1="0" x2="960" y2="90" stroke="#06090e" stroke-width="8"/>
          <line x1="1440" y1="0" x2="1440" y2="90" stroke="#06090e" stroke-width="8"/>

          <!-- Left Peripheral Framing Architecture -->
          <g id="left-alcove">
            <rect x="0" y="90" width="340" height="760" fill="#0d1117" stroke="#05070a" stroke-width="6"/>
            <path d="M 40 180 C 40 120 300 120 300 180 L 300 780 L 40 780 Z" fill="#161b22" stroke="#05070a" stroke-width="5"/>
          </g>

          <!-- Right Peripheral Framing Architecture -->
          <g id="right-alcove">
            <rect x="1580" y="90" width="340" height="760" fill="#0d1117" stroke="#05070a" stroke-width="6"/>
            <path d="M 1620 180 C 1620 120 1880 120 1880 180 L 1880 780 L 1620 780 Z" fill="#161b22" stroke="#05070a" stroke-width="5"/>
          </g>

          <!-- Ground Floor Plane with Perspective -->
          <path d="M 0 850 L 1920 850 L 1920 1080 L 0 1080 Z" fill="#0a0e17"/>
          <line x1="0" y1="850" x2="1920" y2="850" stroke="#f59e0b" stroke-width="4" opacity="0.6"/>
          <line x1="250" y1="850" x2="100" y2="1080" stroke="#1e293b" stroke-width="3"/>
          <line x1="650" y1="850" x2="550" y2="1080" stroke="#1e293b" stroke-width="3"/>
          <line x1="1270" y1="850" x2="1370" y2="1080" stroke="#1e293b" stroke-width="3"/>
          <line x1="1670" y1="850" x2="1820" y2="1080" stroke="#1e293b" stroke-width="3"/>
        </g>

        <!-- ========================================================================= -->
        <!-- LAYER 2: MOTIVATED LIGHTING & ATMOSPHERE (#layer-lighting)               -->
        <!-- ========================================================================= -->
        <g id="layer-lighting">
          <!-- Overhead Warm Light Emitter & Downward God-Ray -->
          <circle cx="960" cy="90" r="35" fill="#fbbf24" filter="url(#glow-gold)"/>
          <polygon points="900,90 1020,90 1520,860 400,860" fill="url(#warm-godray)" opacity="0.75"/>
          <!-- Floating Atmospheric Dust Motes -->
          <g class="svg-anim-dust" fill="#fef08a">
            <circle cx="780" cy="450" r="3" opacity="0.6"/>
            <circle cx="1140" cy="520" r="2.5" opacity="0.7"/>
            <circle cx="980" cy="360" r="3.5" opacity="0.5"/>
            <circle cx="850" cy="620" r="2" opacity="0.8"/>
          </g>
        </g>

        <!-- ========================================================================= -->
        <!-- LAYER 3: HERO PROPS WITH EMBEDDED KINETICS (#layer-props)                -->
        <!-- ========================================================================= -->
        <g id="layer-props">
        '''

        # Render Props
        for pr in props_data:
            svg += cls.draw_animated_prop(pr.get("type"), pr.get("x", 960), pr.get("y", 450), pr.get("scale", 1.0))

        svg += '''
        </g>

        <!-- ========================================================================= -->
        <!-- LAYER 4: ARTICULATED OVER-SIMPLIFIED CHARACTERS (#layer-characters)      -->
        <!-- ========================================================================= -->
        <g id="layer-characters">
        '''

        # Render Characters
        for ch in characters_data:
            svg += cls.draw_animated_chibi(
                cx=ch.get("cx", 960),
                cy=ch.get("cy", 680),
                name=ch.get("name", "Character"),
                hat=ch.get("hat", None),
                glasses=ch.get("glasses", False),
                facial_hair=ch.get("facial_hair", None),
                expression=ch.get("expression", "neutral"),
                pose=ch.get("pose", "standing"),
                body_color=ch.get("body_color", "#1e293b"),
                tie_color=ch.get("tie_color", "#dc2626"),
                coat_type=ch.get("coat_type", "suit"),
                rim_color=ch.get("rim_color", "#fbbf24"),
                rim_side=ch.get("rim_side", "right"),
                scale=ch.get("scale", 1.0)
            )

        # Alert Badge if present
        if alert_data:
            svg += cls.draw_alert_badge(
                alert_data.get("x", 1250),
                alert_data.get("y", 460),
                alert_data.get("text", "!!"),
                alert_data.get("bg_color", "#dc2626")
            )

        svg += f'''
        </g>

        <!-- ========================================================================= -->
        <!-- LAYER 5: FOREGROUND FRAMING ARCH & HUD VFX (#layer-vfx)                  -->
        <!-- ========================================================================= -->
        <g id="layer-vfx">
          <!-- Outer 45px Perimeter Keyhole Silhouette Framing -->
          <path d="M 0 0 L 1920 0 L 1920 1080 L 0 1080 Z M 45 45 L 45 1035 L 1875 1035 L 1875 45 Z"
                fill="#020306" opacity="0.88" fill-rule="evenodd" pointer-events="none"/>
          <!-- Cinematic Radial Vignette -->
          <rect width="1920" height="1080" fill="url(#cinematic-vignette)" pointer-events="none"/>

          <!-- Era Badge Card (Top Left) -->
          <g transform="translate(65, 65)">
            <rect x="0" y="0" width="360" height="42" rx="8" fill="#0f172a" opacity="0.9" stroke="#f59e0b" stroke-width="2"/>
            <text x="180" y="27" font-family="Inter, sans-serif" font-weight="bold" font-size="14" fill="#fbbf24" text-anchor="middle" letter-spacing="1.5">{era}</text>
          </g>
        </g>
      </svg>'''
        return svg


def rasterize_svg_with_chrome(svg_path, output_png_path, width=1920, height=1080):
    """Renders the master SVG file into a pristine 1080p PNG via headless Chrome."""
    if not os.path.exists(CHROME_PATH):
        print(f"⚠️ Chrome not found at {CHROME_PATH}. SVG saved to {svg_path}.")
        return False

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
    parser.add_argument("--out", default="master_scene.svg", help="Output SVG filepath")
    parser.add_argument("--rasterize", default=None, help="Optional output PNG filepath")
    args = parser.parse_args()

    # Default demo scene
    demo_scene = {
        "title": "Emperor Ashoka and the Maurya Empire",
        "era_badge": "INDIA • MAURYA EMPIRE (268 BCE)",
        "bg_color": "#181410",
        "pattern": "ancient-stone-pattern",
        "props": [
            {"type": "ashoka_chakra", "x": 960, "y": 420, "scale": 1.2},
            {"type": "flaming_torch", "x": 220, "y": 550, "scale": 1.1},
            {"type": "flaming_torch", "x": 1700, "y": 550, "scale": 1.1}
        ],
        "characters": [
            {
                "cx": 700, "cy": 680, "name": "Emperor Ashoka", "hat": "ashoka_crown",
                "facial_hair": "mustache", "coat_type": "royal_angavastram", "pose": "sword_raised",
                "body_color": "#7c2d12", "rim_color": "#fbbf24", "rim_side": "right"
            },
            {
                "cx": 1220, "cy": 680, "name": "Royal Advisor", "hat": "turban",
                "facial_hair": "royal_beard", "coat_type": "dhoti_kurta", "pose": "chin_stroke_thinking",
                "body_color": "#1e3a8a", "rim_color": "#38bdf8", "rim_side": "left"
            }
        ],
        "alert": {"x": 1380, "y": 490, "text": "विजय!", "bg_color": "#d97706"}
    }

    svg_content = CinematicSvgEngine.generate_scene(demo_scene)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"🎬 Self-Animating 5-Layer Volumetric Master SVG generated: {args.out}")

    if args.rasterize:
        rasterize_svg_with_chrome(args.out, args.rasterize)


if __name__ == "__main__":
    main()
