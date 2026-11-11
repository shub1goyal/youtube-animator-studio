"""
engine_2d/ai_animation_director.py
The 25-Year Veteran AI Animation Director with Millisecond-Accurate Whisper Word-to-Frame Synchronization
and 2.5D Cinematic Volumetric Engine.

UPGRADES:
- UPGRADE 1: Graphic-novel vector character rigs and rich detailed prop assets.
- UPGRADE 2: 5-Plane Parallax Environment Engine on 2160x1215 overscan canvas with mandatory soft contact shadows.
- UPGRADE 3: Dynamic Alpha-Edge Character Rim Lighting (NumPy fast vector ops), Volumetric bloom & flicker cones,
             continuous prop micro-physics (karak tea steam, 3-layer campfire flames & embers, alive idle breathing).
- UPGRADE 4: 2.5D Virtual Camera Choreography (slow_cinematic_push_in, slow_pan_across_stage, dramatic_reveal_pullback).
- Broadcast packaging: 22% cinematic radial vignette, subtle film grain, vintage era badge, Whisper word-aligned subtitles.
"""

import os
import sys
import re
import json
import time
import math
import wave
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from config import FFMPEG_PATH
from physics_rig import PhysicsCharacterPuppet, SpringDamper, RagdollEntity, apply_alpha_edge_rim_light, render_contact_shadow
from particle_system import CoinShowerSystem, OilGeyserSystem, FireworksSystem
from map_animator import MapEntityAnimator
from motion_graphics import MotionGraphicsEngine
from asset_library import HighFidelityAssetManager

FONT_TITLE = r"C:\Windows\Fonts\segoeuib.ttf" if os.path.exists(r"C:\Windows\Fonts\segoeuib.ttf") else None
FONT_BODY = r"C:\Windows\Fonts\arialbd.ttf" if os.path.exists(r"C:\Windows\Fonts\arialbd.ttf") else None

# Overscan Dimensions for 2.5D Parallax Camera
OVERSCAN_W = 2160
OVERSCAN_H = 1215
OVERSCAN_X = 120  # (2160 - 1920) // 2
OVERSCAN_Y = 68   # (1215 - 1080) // 2


def get_wav_duration(wav_path):
    try:
        with wave.open(wav_path, "rb") as wf:
            return wf.getnframes() / float(wf.getframerate())
    except Exception:
        return 14.0


class AIAnimationDirector:
    def __init__(self, script_path, audio_dir, output_mp4):
        self.script_path = script_path
        self.audio_dir = audio_dir
        self.output_mp4 = output_mp4

        with open(script_path, "r", encoding="utf-8") as f:
            self.script_data = json.load(f)

        # Load Whisper Beat Sheets
        beat_sheet_path = os.path.join(os.path.dirname(self.script_path), "scene_beat_sheets.json")
        if os.path.exists(beat_sheet_path):
            with open(beat_sheet_path, "r", encoding="utf-8") as f:
                self.beat_sheets = json.load(f)
            print(f"📖 Loaded {len(self.beat_sheets)} scene beat sheets with Whisper word synchronization.")
        else:
            self.beat_sheets = {}

        self.asset_mgr = HighFidelityAssetManager()
        self.sprites = self.asset_mgr.cached_images

        # Load sprites: prioritize project-specific sprites folder, fallback to engine shared assets
        project_dir = os.path.dirname(os.path.abspath(self.script_path))
        project_sprites_dir = os.path.join(project_dir, "sprites")
        engine_sprites_dir = os.path.join(SCRIPT_DIR, "sprites")

        for sdir in [engine_sprites_dir, project_sprites_dir]:
            if os.path.exists(sdir):
                for f in os.listdir(sdir):
                    if f.endswith(".png"):
                        k = f[:-4]
                        try:
                            self.sprites[k] = Image.open(os.path.join(sdir, f)).convert("RGBA")
                        except Exception:
                            pass

        # Pre-scale specific narrative props for high-performance cinematic rendering
        if "karak_chai_glass" in self.sprites:
            orig = self.sprites["karak_chai_glass"]
            self.sprites["karak_chai_glass_scaled"] = orig.resize((160, int(orig.height * (160 / orig.width))), Image.Resampling.LANCZOS)
        if "dallah_coffee_pot" in self.sprites:
            orig = self.sprites["dallah_coffee_pot"]
            self.sprites["dallah_coffee_pot_scaled"] = orig.resize((220, int(orig.height * (220 / orig.width))), Image.Resampling.LANCZOS)
        if "crying_oil_barrel" in self.sprites:
            orig = self.sprites["crying_oil_barrel"]
            self.sprites["crying_oil_barrel_scaled"] = orig.resize((270, int(orig.height * (270 / orig.width))), Image.Resampling.LANCZOS)
        if "rubber_stamp_treaty" in self.sprites:
            orig = self.sprites["rubber_stamp_treaty"]
            self.sprites["rubber_stamp_treaty_scaled"] = orig.resize((230, int(orig.height * (230 / orig.width))), Image.Resampling.LANCZOS)
        if "oil_lantern_tent" in self.sprites:
            orig = self.sprites["oil_lantern_tent"]
            self.sprites["oil_lantern_tent_scaled"] = orig.resize((160, int(orig.height * (160 / orig.width))), Image.Resampling.LANCZOS)
        if "oil_valve_giant" in self.sprites:
            orig = self.sprites["oil_valve_giant"]
            self.sprites["oil_valve_giant_scaled"] = orig.resize((390, int(orig.height * (390 / orig.width))), Image.Resampling.LANCZOS)
        if "nuclear_atom_plant" in self.sprites:
            orig = self.sprites["nuclear_atom_plant"]
            self.sprites["nuclear_atom_plant_scaled"] = orig.resize((400, int(orig.height * (400 / orig.width))), Image.Resampling.LANCZOS)

        self.mg = MotionGraphicsEngine()
        self.entity_anim = MapEntityAnimator()

        try:
            self.font_era = ImageFont.truetype(FONT_TITLE, 28)
            self.font_sub = ImageFont.truetype(FONT_BODY, 34)
            self.font_sub_active = ImageFont.truetype(FONT_BODY, 36)
        except OSError:
            self.font_era = ImageFont.load_default()
            self.font_sub = ImageFont.load_default()
            self.font_sub_active = ImageFont.load_default()

        # Precompute 22% Radial Vignette Mask (1920x1080)
        self._init_cinematic_filters()

    def _init_cinematic_filters(self):
        """Precomputes 22% radial vignette and subtle dynamic film grain buffers."""
        # 1. 22% Radial Vignette Mask
        Y, X = np.ogrid[:1080, :1920]
        max_dist = math.sqrt(960.0**2 + 540.0**2)
        dist = np.sqrt((X - 960.0)**2 + (Y - 540.0)**2) / max_dist
        falloff = np.clip((dist - 0.45) / 0.55, 0.0, 1.0)
        darkness = 0.5 * (1.0 - np.cos(np.pi * falloff)) * 0.22
        vig_arr = np.zeros((1080, 1920, 4), dtype=np.uint8)
        vig_arr[:, :, 3] = (darkness * 255.0).astype(np.uint8)
        self.vignette_img = Image.fromarray(vig_arr, "RGBA")

        # 2. Subtle Film Grain (4 alternating noise buffers)
        self.grain_frames = []
        rng = np.random.default_rng(42)
        for _ in range(4):
            noise = rng.normal(0, 3.5, (1080, 1920)).clip(-12, 12)
            grain_arr = np.zeros((1080, 1920, 4), dtype=np.uint8)
            # Positive noise adds subtle white speckles, negative noise adds subtle dark speckles
            mask_white = noise > 2.0
            mask_dark = noise < -2.0
            grain_arr[mask_white, 0:3] = 255
            grain_arr[mask_white, 3] = (noise[mask_white] * 2.2).astype(np.uint8)
            grain_arr[mask_dark, 0:3] = 0
            grain_arr[mask_dark, 3] = (-noise[mask_dark] * 2.2).astype(np.uint8)
            self.grain_frames.append(Image.fromarray(grain_arr, "RGBA"))

    # ================= 1. KINETIC SYNCHRONIZATION HELPERS =================
    def get_character_sprite_key(self, char_id):
        """Resolves character ID to available 1:1 compiled vector rig."""
        if char_id in self.sprites:
            return char_id
        for sk in self.sprites.keys():
            if sk in char_id or char_id in sk:
                return sk
        # Contextual archetype fallbacks
        c_low = char_id.lower()
        if any(k in c_low for k in ["oppenheimer", "robert", "physicist"]):
            return "j_robert_oppenheimer"
        elif any(k in c_low for k in ["truman", "harry", "potus", "president"]):
            return "harry_truman"
        elif any(k in c_low for k in ["hirohito", "emperor", "showa", "tenno"]):
            return "emperor_hirohito"
        elif any(k in c_low for k in ["groves", "general_groves", "manhattan"]):
            return "general_leslie_groves"
        elif any(k in c_low for k in ["tibbets", "pilot", "enola", "colonel_tibbets"]):
            return "colonel_paul_tibbets"
        elif any(k in c_low for k in ["anami", "korechika", "minister", "war_minister"]):
            return "general_korechika_anami"
        elif any(k in c_low for k in ["einstein", "albert"]):
            return "albert_einstein"
        elif any(k in c_low for k in ["clive", "officer", "commander", "admiral", "governor", "clerk", "planter", "munro", "watson", "merchant", "smith", "hawkins"]):
            return "robert_clive"
        elif any(k in c_low for k in ["jahangir", "emperor", "farrukhsiyar", "shah_alam", "alivardi", "shuja", "mughal", "badshah"]):
            return "emperor_jahangir"
        elif any(k in c_low for k in ["sepoy", "soldier", "gunner", "recruit", "sainik"]):
            return "indian_sepoy"
        elif any(k in c_low for k in ["queen", "victoria", "elizabeth"]):
            return "queen_victoria"
        elif any(k in c_low for k in ["jafar", "omichund"]):
            return "mir_jafar"
        elif any(k in c_low for k in ["siraj", "qasim"]):
            return "siraj_ud_daulah"
        elif any(k in c_low for k in ["mangal", "pandey", "tatya", "nana"]):
            return "mangal_pandey"
        elif any(k in c_low for k in ["rani", "lakshmi"]):
            return "rani_lakshmibai"
        elif any(k in c_low for k in ["tipu", "sultan"]):
            return "tipu_sultan"
        elif any(k in c_low for k in ["dalhousie", "hastings", "wellesley", "canning", "derby", "north"]):
            return "lord_dalhousie"
        elif any(k in c_low for k in ["zafar", "bahadur"]):
            return "bahadur_shah_zafar"
        elif any(k in c_low for k in ["analyst", "modern"]):
            return "modern_analyst"
        return "sir_thomas_roe"

    def compute_kinetic_anchor(self, beat, t_rel):
        """Computes animated screen position with cartoon elastic snap."""
        tx, ty = beat["anchor_target"]
        style = beat.get("enter_style", "present")
        t_enter = beat.get("enter_time", 0.0)

        if style == "present" or t_rel >= t_enter + 0.35:
            return tx, ty, True

        if t_rel < t_enter:
            return tx, ty, False

        p = (t_rel - t_enter) / 0.35
        overshoot = 1.0 + 2.70158 * math.pow(p - 1.0, 3) + 1.70158 * math.pow(p - 1.0, 2)

        if style == "slide_from_left":
            start_x = -380
            return int(start_x + (tx - start_x) * overshoot), ty, True
        elif style == "slide_from_right":
            start_x = 2300
            return int(start_x + (tx - start_x) * overshoot), ty, True
        elif style == "pop_up":
            start_y = 1250
            return tx, int(start_y + (ty - start_y) * overshoot), True
        return tx, ty, True

    def get_puppet_reaction(self, beat, t_rel):
        reactions = beat.get("reactions", [])
        expr = "neutral"
        should_faint = False
        for r in reactions:
            if t_rel >= r["time"]:
                expr = r.get("expression", "neutral")
                if r.get("type") == "faint":
                    should_faint = True
        return expr, should_faint

    # ================= 2. PROP MICRO-PHYSICS & VOLUMETRIC BLOOM HELPERS =================
    def draw_karak_steam(self, canvas, cup_center_x, cup_top_y, t):
        """Continuous Particle & Prop Micro-Physics: 3 sine-wave Bezier vapor plumes."""
        draw = ImageDraw.Draw(canvas, "RGBA")
        for i in range(3):
            phase = i * 2.1
            y_rise = (t * 45.0 + i * 30.0) % 90.0
            alpha = int(220.0 * max(0.0, 1.0 - y_rise / 90.0))
            if alpha <= 0:
                continue
            base_x = cup_center_x + (i - 1) * 16
            pts = []
            for seg in range(6):
                sy = cup_top_y - y_rise - seg * 12
                sway = math.sin(t * 5.0 + (y_rise + seg * 12) * 0.1 + phase) * 6.0
                pts.append((base_x + sway, sy))
            for k in range(len(pts) - 1):
                draw.line([pts[k], pts[k+1]], fill=(255, 255, 255, alpha), width=3)

    def draw_campfire_vfx(self, canvas_floor, canvas_actors, cx, cy, t):
        """Campfire & Lantern Micro-Physics: 3 layered flame tongues & 12 rising embers."""
        fdraw = ImageDraw.Draw(canvas_floor, "RGBA")
        adraw = ImageDraw.Draw(canvas_actors, "RGBA")

        # Multi-frequency Perlin/sine flicker
        flicker = 0.88 + 0.12 * (math.sin(t * 14.0) * 0.6 + math.cos(t * 27.0) * 0.4)

        # 1. Warm radial floor pool on Plane 3 underneath campfire
        rx = int(280 * flicker)
        ry = int(90 * flicker)
        fdraw.ellipse([cx - rx, cy - ry + 15, cx + rx, cy + ry + 15], fill=(251, 191, 36, int(95 * flicker)))
        fdraw.ellipse([cx - int(rx * 0.5), cy - int(ry * 0.5) + 15, cx + int(rx * 0.5), cy + int(ry * 0.5) + 15], fill=(254, 240, 138, int(130 * flicker)))

        # 2. 3 Layered Dynamic Flame Tongues
        h1 = 75.0 * (1.0 + 0.15 * math.sin(t * 16.0))
        h2 = 52.0 * (1.0 + 0.20 * math.cos(t * 19.0))
        h3 = 30.0 * (1.0 + 0.10 * math.sin(t * 23.0))

        # Layer 1: Crimson flame tongue
        adraw.polygon([(cx - 38, cy + 10), (cx, cy - h1), (cx + 38, cy + 10)], fill=(220, 38, 38, 230))
        # Layer 2: Amber tongue
        adraw.polygon([(cx - 24, cy + 10), (cx, cy - h2), (cx + 24, cy + 10)], fill=(245, 158, 11, 240))
        # Layer 3: White-Yellow core
        adraw.polygon([(cx - 14, cy + 10), (cx, cy - h3), (cx + 14, cy + 10)], fill=(254, 240, 138, 255))
        adraw.ellipse([cx - 10, cy - 8, cx + 10, cy + 12], fill=(255, 255, 255, 255))

        # 3. 12 Rising Glowing Ember Particles
        for e_idx in range(12):
            speed = 55.0 + (e_idx % 4) * 25.0
            e_y = cy - ((t * speed + e_idx * 32.0) % 190.0)
            drift = math.sin(t * 3.5 + e_idx * 1.8) * 26.0
            e_x = cx + (e_idx - 6) * 5 + drift
            e_alpha = int(255.0 * max(0.0, 1.0 - (cy - e_y) / 190.0))
            adraw.ellipse([e_x - 3, e_y - 3, e_x + 3, e_y + 3], fill=(254, 240, 138, e_alpha))

    def draw_lantern_vfx(self, canvas_floor, canvas_actors, lx, ly, t):
        """Volumetric Light Cones & Ground Glow for Oil Lantern."""
        fdraw = ImageDraw.Draw(canvas_floor, "RGBA")
        adraw = ImageDraw.Draw(canvas_actors, "RGBA")

        flicker = 0.88 + 0.12 * (math.sin(t * 14.0) * 0.6 + math.cos(t * 27.0) * 0.4)

        # 1. Warm radial floor pool (Plane 3)
        rx = int(280 * flicker)
        ry = int(90 * flicker)
        fdraw.ellipse([lx - rx, ly - ry + 40, lx + rx, ly + ry + 40], fill=(251, 191, 36, int(85 * flicker)))

        # 2. Dual-radius volumetric additive glow buffer
        lr1 = int(150 * flicker)
        lr2 = int(75 * flicker)
        adraw.ellipse([lx - lr1, ly - lr1, lx + lr1, ly + lr1], fill=(251, 191, 36, int(50 * flicker)))
        adraw.ellipse([lx - lr2, ly - lr2, lx + lr2, ly + lr2], fill=(254, 240, 138, int(90 * flicker)))
        adraw.ellipse([lx - 12, ly - 12, lx + 12, ly + 12], fill=(255, 255, 255, 220))

    # ================= 3. 5-PLANE PARALLAX ENVIRONMENT ENGINE =================
    def render_5plane_environment(self, env_type, t, t_rel):
        """
        UPGRADE 2: Generates a 5-layer RGBA depth stack on 2160x1215 overscan canvas:
        - Plane 1: Sky & Celestial Atmosphere (Parallax 0.12)
        - Plane 2: Far & Mid-Horizon Terrain (Parallax 0.40 & 0.65)
        - Plane 3: Main Stage Floor & Contact Shadows (Parallax 1.00)
        - Plane 5: Out-of-Focus Foreground DoF Framing (Parallax 1.42)
        """
        W, H = OVERSCAN_W, OVERSCAN_H

        plane_sky = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        plane_horizon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        plane_floor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        plane_foreground = Image.new("RGBA", (W, H), (0, 0, 0, 0))

        sdraw = ImageDraw.Draw(plane_sky)
        hdraw = ImageDraw.Draw(plane_horizon)
        fdraw = ImageDraw.Draw(plane_floor)
        fg_draw = ImageDraw.Draw(plane_foreground)

        # ---------------- 0. ATOMIC MUSHROOM BLAST VISTA ----------------
        if env_type == "atomic_mushroom":
            # Plane 1: Apocalyptic Irradiated Orange-Red Sky
            for y in range(720):
                p = y / 720.0
                r = int(220 - 50 * p)
                g = int(60 + 60 * p)
                b = int(20 + 20 * p)
                sdraw.line([(0, y), (W, y)], fill=(r, g, b, 255))
            # Pulsing Atomic Glow at Epicenter
            sdraw.ellipse([960 - 320, 480 - 180, 960 + 320, 480 + 180], fill=(255, 235, 120, 60))
            # Plane 2: Distant Ruined Skyline & Billowing Smoke
            hdraw.polygon([(0, 620), (250, 580), (480, 630), (850, 560), (1350, 640), (1750, 570), (W, 610), (W, H), (0, H)], fill=(35, 20, 18, 255))
            # Plane 3: Scorched Stage Ground
            fdraw.polygon([(0, 780), (W, 780), (W, H), (0, H)], fill=(28, 16, 14, 255))
            for ry in range(800, H, 20):
                fdraw.line([(0, ry), (W, ry + 6)], fill=(45, 25, 20, 120), width=2)
            # Plane 5: Out of focus ruined steel girders
            fg_draw.polygon([(-30, 750), (120, 1215), (70, 1215), (-60, 750)], fill=(12, 8, 8, 255))
            fg_draw.polygon([(W + 30, 800), (W - 140, 1215), (W - 90, 1215), (W + 60, 800)], fill=(12, 8, 8, 255))
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        # ---------------- 0B. STRATOSPHERE FLIGHT (B-29 ENOLA GAY) ----------------
        elif env_type == "stratosphere_flight":
            # Plane 1: High Altitude Azure Sky
            for y in range(650):
                p = y / 650.0
                r = int(15 + 40 * p)
                g = int(35 + 85 * p)
                b = int(85 + 130 * p)
                sdraw.line([(0, y), (W, y)], fill=(r, g, b, 255))
            # Curved Earth Horizon Arc
            sdraw.arc([-200, 520, W + 200, 1600], 180, 360, fill=(180, 220, 255, 140), width=4)
            # Plane 2: Sea of Pacific Fluffy Clouds
            for cx_i in range(0, W + 200, 180):
                hdraw.ellipse([cx_i - 120, 600, cx_i + 140, 760], fill=(225, 235, 245, 255))
                hdraw.ellipse([cx_i - 90, 620, cx_i + 110, 780], fill=(200, 215, 230, 255))
            # Plane 3: Lower Flight Altitude Deck
            fdraw.rectangle([(0, 740), (W, H)], fill=(185, 205, 225, 255))
            # Plane 5: Out of focus B-29 Cockpit Canopy Struts
            fg_draw.rectangle([(-20, 0), (120, 1215)], fill=(15, 23, 42, 255))
            fg_draw.polygon([(-20, 0), (W // 2, 0), (W // 2, 80), (-20, 120)], fill=(15, 23, 42, 255))
            fg_draw.rectangle([(W - 120, 0), (W + 20, 1215)], fill=(15, 23, 42, 255))
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        # ---------------- 0C. JAPANESE IMPERIAL PALACE / SHOJI CHAMBER ----------------
        elif env_type in ["japanese_imperial_chamber", "tokyo_imperial_palace", "imperial_chamber"]:
            # Plane 1: Warm Wood & Paper Ambient Wall
            sdraw.rectangle([(0, 0), (W, H)], fill=(42, 33, 24, 255))
            # Plane 2: Traditional Shoji Lattice Paper Sliding Screens
            for sx_i in range(80, W, 240):
                hdraw.rectangle([(sx_i, 140), (sx_i + 220, 740)], fill=(245, 240, 225, 255), outline=(30, 20, 12, 255), width=6)
                # Shoji Wooden Grid Lines
                for gy in range(180, 740, 65):
                    hdraw.line([(sx_i, gy), (sx_i + 220, gy)], fill=(45, 30, 18, 255), width=3)
                for gx in range(sx_i + 45, sx_i + 220, 55):
                    hdraw.line([(gx, 140), (gx, 740)], fill=(45, 30, 18, 255), width=3)
            # Plane 3: Golden-Brown Woven Tatami Mat Floor
            fdraw.rectangle([(0, 740), (W, H)], fill=(180, 150, 95, 255))
            for ty in range(750, H, 45):
                fdraw.line([(0, ty), (W, ty)], fill=(130, 105, 60, 255), width=4)
            # Black Silk Border Tatami Seams
            for tx in range(160, W, 360):
                fdraw.line([(tx, 740), (tx + int((tx - 1080) * 0.3), H)], fill=(20, 20, 20, 255), width=8)
            # Plane 5: Out of focus dark wooden cedar pillar
            fg_draw.rectangle([(-30, 0), (140, 1215)], fill=(18, 12, 8, 255))
            fg_draw.rectangle([(W - 140, 0), (W + 30, 1215)], fill=(18, 12, 8, 255))
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        # ---------------- A. DESERT DUNES & TENT ----------------
        elif env_type in ["desert_dunes", "desert_tent"]:
            is_night = (env_type == "desert_tent")

            # Plane 1: Sky & Atmosphere (Parallax 0.12)
            if is_night:
                # Deep Indigo / Navy Night Sky
                for y in range(720):
                    p = y / 720.0
                    r = int(9 + 25 * p)
                    g = int(10 + 20 * p)
                    b = int(24 + 55 * p)
                    sdraw.line([(0, y), (W, y)], fill=(r, g, b, 255))
                # Twinkling Starfield
                for s_i in range(120):
                    sx = (s_i * 89 + int(s_i * 13.5)) % W
                    sy = (s_i * 37) % 520
                    twinkle = 0.5 + 0.5 * math.sin(t * 3.5 + s_i * 1.5)
                    sdraw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(240, 245, 255, int(220 * twinkle)))
                # Golden Crescent Moon with Soft Glow
                mx, my = 1720, 160
                sdraw.ellipse([mx - 75, my - 75, mx + 75, my + 75], fill=(254, 240, 138, 45))
                sdraw.ellipse([mx - 40, my - 40, mx + 40, my + 40], fill=(254, 240, 138, 255))
                sdraw.ellipse([mx - 22, my - 44, mx + 46, my + 38], fill=(15, 23, 42, 255))
            else:
                # Blazing Desert Sky Gradient
                for y in range(650):
                    p = y / 650.0
                    r = int(245 - 20 * p)
                    g = int(130 + 90 * p)
                    b = int(40 + 130 * p)
                    sdraw.line([(0, y), (W, y)], fill=(r, g, b, 255))
                # Volumetric Sun with Radial Rays
                sx, sy = 1700, 160
                sdraw.ellipse([sx - 110, sy - 110, sx + 110, sy + 110], fill=(255, 235, 120, 60))
                sdraw.ellipse([sx - 65, sy - 65, sx + 65, sy + 65], fill=(255, 215, 0, 255))
                for ray in range(6):
                    ang = ray * (math.pi / 3) + t * 0.05
                    rx = sx + math.cos(ang) * 450
                    ry = sy + math.sin(ang) * 250
                    sdraw.line([(sx, sy), (rx, ry)], fill=(255, 245, 180, 35), width=18)

            # Plane 2: 4 Overlapping Dune Layers (Parallax 0.40 & 0.65)
            c1 = (45, 35, 55, 255) if is_night else (195, 135, 75, 255)
            c2 = (40, 30, 48, 255) if is_night else (180, 120, 62, 255)
            c3 = (35, 25, 42, 255) if is_night else (165, 105, 50, 255)
            c4 = (30, 20, 36, 255) if is_night else (150, 92, 40, 255)

            hdraw.polygon([(0, 580), (600, 520), (1400, 610), (W, 540), (W, H), (0, H)], fill=c1)
            hdraw.polygon([(0, 660), (750, 590), (1600, 680), (W, 610), (W, H), (0, H)], fill=c2)
            hdraw.polygon([(0, 730), (900, 660), (1800, 740), (W, 680), (W, H), (0, H)], fill=c3)
            hdraw.polygon([(0, 800), (1100, 720), (1950, 800), (W, 740), (W, H), (0, H)], fill=c4)

            # Plane 3: Stage Ground Plane (Parallax 1.00)
            ground_c = (25, 18, 14, 255) if is_night else (140, 82, 34, 255)
            fdraw.polygon([(0, 790), (W, 790), (W, H), (0, H)], fill=ground_c)
            # Sandy Floor Texture Ripples
            for ry in range(800, H, 24):
                fdraw.line([(0, ry), (W, ry + 8)], fill=(ground_c[0]+15, ground_c[1]+10, ground_c[2]+5, 110), width=2)

            # Plane 5: Out-of-Focus Foreground DoF Framing (Parallax 1.42)
            fg_c = (9, 10, 15, 255)
            fg_draw.ellipse([-60, 1020, 320, 1380], fill=fg_c)
            fg_draw.ellipse([1900, 990, 2260, 1360], fill=fg_c)
            # Desert Shrub Silhouettes
            for px, py in [(120, 1050), (2000, 1020)]:
                fg_draw.polygon([(px - 40, py + 80), (px, py), (px + 40, py + 80)], fill=fg_c)
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        # ---------------- B. OCEAN UNDERWATER ----------------
        elif env_type == "ocean_underwater":
            # Plane 1: Abyss Sky / God Rays
            for y in range(H):
                p = y / float(H)
                sdraw.line([(0, y), (W, y)], fill=(int(5 + 10*p), int(35 + 40*p), int(75 + 30*p), 255))
            for s_idx in range(6):
                sx = 250 + s_idx * 340 + math.sin(t * 0.8 + s_idx) * 40
                sdraw.polygon([(sx, 0), (sx + 80, 0), (sx + 350, H), (sx + 190, H)], fill=(200, 245, 255, 18))

            # Plane 2: Distant Reefs
            hdraw.polygon([(0, 850), (550, 790), (1200, 860), (1750, 800), (W, 840), (W, H), (0, H)], fill=(20, 60, 85, 255))
            hdraw.polygon([(0, 900), (650, 840), (1400, 910), (W, 870), (W, H), (0, H)], fill=(30, 80, 105, 255))

            # Plane 3: Seabed
            fdraw.polygon([(0, 930), (W, 930), (W, H), (0, H)], fill=(160, 122, 75, 255))
            # Giant Pearl Oyster
            ox, oy = 1120, 920
            fdraw.ellipse([ox - 65, oy - 35, ox + 65, oy + 35], fill=(65, 75, 85, 255), outline=(9, 10, 15, 255), width=4)
            fdraw.ellipse([ox - 22, oy - 24, ox + 22, oy + 20], fill=(255, 255, 255, 255))
            fdraw.ellipse([ox - 36, oy - 38, ox + 36, oy + 34], outline=(255, 255, 200, 160), width=5)
            # Rising Bubbles
            for b_idx in range(18):
                bx = (b_idx * 135 + int(t * 40)) % W
                by = (H - int(t * 120 + b_idx * 80)) % H
                br = 3 + (b_idx % 4) * 2
                fdraw.ellipse([bx - br, by - br, bx + br, by + br], outline=(220, 245, 255, 190), width=2)

            # Plane 5: Out of Focus Kelp Framing
            fg_draw.polygon([(-40, 1215), (80, 800), (160, 1215)], fill=(10, 35, 45, 255))
            fg_draw.polygon([(2000, 1215), (2080, 820), (2200, 1215)], fill=(10, 35, 45, 255))
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        # ---------------- C. OCEAN SURFACE & SHORE ----------------
        elif env_type == "ocean_surface":
            # Plane 1: Maritime Sky & Sun
            for y in range(540):
                p = y / 540.0
                sdraw.line([(0, y), (W, y)], fill=(int(240 - 20*p), int(170 - 40*p), int(110 - 20*p), 255))
            sdraw.ellipse([1560, 130, 1740, 310], fill=(255, 220, 120, 255))

            # Plane 2: Distant Island Mountains & Waves
            hdraw.polygon([(0, 520), (750, 480), (1450, 530), (W, 490), (W, H), (0, H)], fill=(170, 135, 95, 255))
            for y in range(530, 780):
                p = (y - 530) / 250.0
                hdraw.line([(0, y), (W, y)], fill=(int(18 + 10*p), int(72 + 20*p), int(100 + 15*p), 255))

            # Plane 3: Beach / Pier Shore
            fdraw.polygon([(0, 780), (W, 780), (W, H), (0, H)], fill=(190, 155, 105, 255))

            # Plane 5: Mooring Post & Rigging Ropes
            fg_draw.rectangle([(-20, 880), (100, 1215)], fill=(15, 12, 10, 255))
            fg_draw.ellipse([1960, 1020, 2240, 1300], fill=(15, 12, 10, 255))
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        # ---------------- D. HISTORICAL INTERIORS (TREATY ROOM, PARLIAMENT, PALACE) ----------------
        elif env_type in ["treaty_room", "crash_office", "london_tavern", "union_house"] or "palace" in env_type or "court" in env_type:
            # Plane 1: Grand Arched Windows looking at outdoor sky
            sdraw.rectangle([(0, 0), (W, H)], fill=(45, 55, 72, 255))
            # Arched Window
            sdraw.rounded_rectangle([860, 180, 1300, 580], radius=90, fill=(135, 206, 235, 255), outline=(212, 175, 55, 255), width=7)
            sdraw.line([(1080, 180), (1080, 580)], fill=(212, 175, 55, 255), width=5)
            sdraw.line([(860, 380), (1300, 380)], fill=(212, 175, 55, 255), width=5)

            # Plane 2: Wainscoting & Columns
            for px in range(0, W, 180):
                hdraw.rectangle([(px + 10, 100), (px + 170, 740)], fill=(35, 42, 54, 255), outline=(60, 70, 85, 255), width=3)
            hdraw.line([(0, 140), (W, 140)], fill=(212, 175, 55, 255), width=5)

            # Plane 3: Polished Parquet / Marble Floor
            for y in range(740, H):
                p = (y - 740) / float(H - 740)
                fdraw.line([(0, y), (W, y)], fill=(int(60 + 20*p), int(35 + 12*p), int(20 + 8*p), 255))
            for px in range(0, W, 160):
                fdraw.line([(px, 740), (px + int((px - 1080) * 0.4), H)], fill=(40, 22, 12, 180), width=3)

            # Plane 5: Out of Focus Velvet Curtains
            fg_draw.polygon([(-30, 0), (160, 0), (70, 700), (-30, 600)], fill=(120, 15, 15, 255))
            fg_draw.polygon([(W + 30, 0), (W - 160, 0), (W - 70, 700), (W + 30, 600)], fill=(120, 15, 15, 255))
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        # ---------------- E. DUBAI MODERN & OIL BOOM ----------------
        elif env_type in ["dubai_modern", "oil_boom", "oil_field"]:
            # Plane 1: Twilight Sky
            for y in range(750):
                p = y / 750.0
                sdraw.line([(0, y), (W, y)], fill=(int(15 + 30*p), int(23 + 45*p), int(42 + 65*p), 255))

            # Plane 2: Skyline Layers
            hdraw.polygon([(0, 750), (0, 580), (120, 580), (120, 480), (220, 480), (220, 750),
                           (450, 750), (450, 400), (560, 400), (560, 750), (850, 750), (850, 520),
                           (960, 520), (960, 750), (1300, 750), (1300, 420), (1450, 420), (1450, 750),
                           (1750, 750), (1750, 500), (1880, 500), (1880, 750), (W, 750), (W, H), (0, H)],
                          fill=(15, 23, 42, 255))

            # Plane 3: Highway Floor
            fdraw.rectangle([(0, 850), (W, H)], fill=(30, 41, 59, 255))
            fdraw.line([(0, 960), (W, 960)], fill=(250, 204, 21, 200), width=4)

            # Plane 5: Highway Girder Silhouettes
            fg_draw.rectangle([(-20, 980), (140, 1215)], fill=(9, 10, 15, 255))
            fg_draw.rectangle([(W - 140, 980), (W + 20, 1215)], fill=(9, 10, 15, 255))
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        # ---------------- F. MARS SPACE ----------------
        elif env_type == "mars_space":
            # Plane 1: Cosmic Nebula Void
            sdraw.rectangle([(0, 0), (W, H)], fill=(4, 6, 14, 255))
            for s_i in range(160):
                sx = (s_i * 97) % W
                sy = (s_i * 43) % H
                twinkle = 0.5 + 0.5 * math.sin(t * 3.0 + s_i)
                sdraw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(240, 245, 255, int(230 * twinkle)))

            # Plane 2: Red Mars Globe
            mcx, mcy, mr = 1620, 360, 230
            hdraw.ellipse([mcx - mr, mcy - mr, mcx + mr, mcy + mr], fill=(185, 28, 28, 255), outline=(239, 68, 68, 140), width=6)
            hdraw.ellipse([mcx - 80, mcy - 50, mcx - 20, mcy + 10], fill=(127, 29, 29, 200))
            hdraw.ellipse([mcx + 40, mcy + 50, mcx + 110, mcy + 100], fill=(127, 29, 29, 200))

            # Plane 3: Red Sand Floor
            fdraw.polygon([(0, 850), (W, 850), (W, H), (0, H)], fill=(127, 29, 29, 255))

            # Plane 5: Out of Focus Mars Boulders
            fg_draw.ellipse([-50, 1020, 260, 1300], fill=(20, 5, 5, 255))
            fg_draw.ellipse([(W - 240, 1020), (W + 50, 1300)], fill=(20, 5, 5, 255))
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        # ---------------- G. HISTORICAL BATTLEFIELDS (PLASSEY, BUXAR, ETC) ----------------
        else:
            # Plane 1: Thunderstorm Sky
            for y in range(650):
                p = y / 650.0
                sdraw.line([(0, y), (W, y)], fill=(int(40 + 35*p), int(45 + 30*p), int(55 + 20*p), 255))

            # Plane 2: Distant Tree Silhouettes
            hdraw.polygon([(0, 640), (450, 590), (1200, 660), (1800, 600), (W, 630), (W, H), (0, H)], fill=(35, 45, 30, 255))

            # Plane 3: Muddy Plains Ground
            fdraw.polygon([(0, 780), (W, 780), (W, H), (0, H)], fill=(115, 80, 50, 255))

            # Plane 5: Out of Focus Rubble
            fg_draw.ellipse([-40, 1020, 260, 1320], fill=(9, 10, 15, 255))
            fg_draw.ellipse([(W - 240, 1020), (W + 40, 1320)], fill=(9, 10, 15, 255))
            plane_foreground = plane_foreground.filter(ImageFilter.GaussianBlur(8))

        return plane_sky, plane_horizon, plane_floor, plane_foreground

    # ================= 4. 2.5D VIRTUAL CAMERA COMPOSITING =================
    def composite_2_5d_frame(self, planes, cam_x, cam_y, cam_zoom, f_idx=0):
        """
        UPGRADE 4: Multi-Plane 2.5D Virtual Camera Choreography:
        Composites 5 planes using their parallax factors, extracts zoomed viewport,
        and applies 22% radial vignette & subtle film grain.
        """
        master = Image.new("RGBA", (OVERSCAN_W, OVERSCAN_H), (0, 0, 0, 255))

        for p_img, p_factor in planes:
            if p_img is None:
                continue
            shift_x = int(cam_x * (p_factor - 1.0))
            shift_y = int(cam_y * (p_factor - 1.0))
            master.alpha_composite(p_img, (shift_x, shift_y))

        # Viewport Extraction (1920x1080)
        w_view = int(1920 / cam_zoom)
        h_view = int(1080 / cam_zoom)
        cx = (OVERSCAN_W // 2) + int(cam_x)
        cy = (OVERSCAN_H // 2) + int(cam_y)

        x1 = max(0, min(OVERSCAN_W - w_view, cx - w_view // 2))
        y1 = max(0, min(OVERSCAN_H - h_view, cy - h_view // 2))
        x2 = x1 + w_view
        y2 = y1 + h_view

        viewport = master.crop((x1, y1, x2, y2))
        if viewport.size != (1920, 1080):
            viewport = viewport.resize((1920, 1080), Image.Resampling.BILINEAR)

        # Apply 22% Radial Vignette
        viewport.alpha_composite(self.vignette_img, (0, 0))

        # Apply Subtle Dynamic Film Grain
        if self.grain_frames:
            grain = self.grain_frames[f_idx % len(self.grain_frames)]
            viewport.alpha_composite(grain, (0, 0))

        return viewport

    # ================= 5. MASTER PRODUCTION DIRECTOR =================
    def direct_and_render(self, fps=25):
        sys.stdout.reconfigure(line_buffering=True)
        scenes = self.script_data.get("scenes", [])
        n_scenes = len(scenes)
        print(f"🎬 [2.5D Volumetric AI Director] Directing {n_scenes} Scenes at {fps} FPS...", flush=True)

        scene_durations = []
        total_duration = 0.0
        for i, sc in enumerate(scenes, 1):
            wav_file = os.path.join(self.audio_dir, f"scene_{i}.wav")
            if os.path.exists(wav_file):
                d = get_wav_duration(wav_file)
            else:
                d = float(sc.get("duration", 14.0))
            d = max(3.0, d)
            scene_durations.append(d)
            total_duration += d

        print(f"⏱️ Audio Runtime: {total_duration:.2f}s ({total_duration/60:.2f} minutes) across {n_scenes} scenes.")

        master_audio = os.path.join(self.audio_dir, "master_soundtrack_complete.wav")
        if not os.path.exists(master_audio):
            master_audio = os.path.join(self.audio_dir, "final_mastered_voiceover.wav")

        ffmpeg_cmd = [
            FFMPEG_PATH,
            "-f", "rawvideo",
            "-pix_fmt", "rgba",
            "-s", "1920x1080",
            "-r", str(fps),
            "-i", "-",
            "-i", master_audio,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "256k",
            "-shortest",
            self.output_mp4,
            "-y"
        ]

        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        puppets = {}
        global_time = 0.0
        start_time = time.time()
        total_frames = int(total_duration * fps)
        rendered_frames = 0

        for idx, (scene, scene_dur) in enumerate(zip(scenes, scene_durations), 1):
            for p in puppets.values():
                p.is_ragdoll = False
            num_frames = int(scene_dur * fps)
            env = scene.get("environment", "desert_dunes")
            chars = scene.get("characters", ["sheikh_zayed"])
            props = scene.get("props", [])
            particle_mode = scene.get("particles", None)
            era_badge = scene.get("era_badge", None)
            vo_text = scene.get("vo_hinglish", "") or scene.get("vo", "")

            # Retrieve Whisper Beat Sheet for this Scene
            sc_beat = self.beat_sheets.get(str(idx), {})
            raw_chars = sc_beat.get("characters", {})
            if isinstance(raw_chars, list):
                char_beats = {c.get("char_id", f"char_{i}"): c for i, c in enumerate(raw_chars)}
            else:
                char_beats = raw_chars

            prop_beats = {}
            for p in sc_beat.get("props", []):
                p_name = p.get("name") or p.get("prop_id")
                if p_name:
                    prop_beats[p_name] = p

            stamp_info = sc_beat.get("stamp", None)
            speech_intervals = sc_beat.get("speech_intervals", [])

            # UPGRADE 4: Determine Camera Choreography Preset
            cam_preset = sc_beat.get("camera", {}).get("preset", None)
            if not cam_preset:
                if any(p in ["oil_derrick_monumental", "burj_khalifa_tower", "crying_oil_barrel", "nuclear_atom_plant"] for p in props):
                    cam_preset = "dramatic_reveal_pullback"
                elif len(chars) >= 2 or env in ["union_house", "treaty_room", "map_uae"]:
                    cam_preset = "slow_pan_across_stage"
                else:
                    cam_preset = "slow_cinematic_push_in"

            # Load scene Whisper words for zero-drift subtitle sync
            whisper_words = None
            words_file = os.path.join(self.audio_dir, "word_timestamps", f"scene_{idx}_words.json")
            if os.path.exists(words_file):
                try:
                    with open(words_file, "r", encoding="utf-8") as wf:
                        whisper_words = json.load(wf)
                except Exception:
                    pass

            for p in puppets.values():
                p.trigger_reaction("reset")

            coins = CoinShowerSystem(coin_count=35, spawn_center=(960 + OVERSCAN_X, 200 + OVERSCAN_Y)) if particle_mode == "coins" else None
            oil_geyser = OilGeyserSystem(nozzle_pos=(1350 + OVERSCAN_X, 690 + OVERSCAN_Y), particle_count=55) if particle_mode == "oil_geyser" else None
            fireworks = FireworksSystem(num_bursts=4) if particle_mode == "fireworks" else None

            # Pre-render static 5-plane environment once per scene (massive 5x-8x FPS speedup)
            cached_sky, cached_horizon, cached_floor, cached_foreground = self.render_5plane_environment(env, global_time, 0.0)

            for f in range(num_frames):
                t_rel = f / float(fps)
                t = global_time + t_rel
                dt = 1.0 / fps

                # ---------------- 1. Virtual Camera State Math ----------------
                p_dur = max(0.01, t_rel / scene_dur)
                if cam_preset == "slow_cinematic_push_in":
                    ease = 0.5 * (1.0 - math.cos(math.pi * p_dur))
                    cam_zoom = 1.00 + 0.14 * ease
                    cam_x = -15.0 * ease
                    cam_y = -8.0 * ease
                elif cam_preset == "slow_pan_across_stage":
                    ease = 0.5 * (1.0 - math.cos(math.pi * p_dur))
                    cam_x = -55.0 + 110.0 * ease
                    cam_y = 0.0
                    cam_zoom = 1.02
                elif cam_preset == "dramatic_reveal_pullback":
                    p_drop = min(1.0, t_rel / 1.8)
                    ease = 1.0 - math.cos(math.pi * 0.5 * p_drop)
                    cam_zoom = 1.22 - 0.22 * ease
                    cam_x = 35.0 * (1.0 - ease)
                    cam_y = 15.0 * (1.0 - ease)
                else:
                    cam_x, cam_y, cam_zoom = 0.0, 0.0, 1.00

                # ---------------- 2. Render 5-Plane Environment Stack ----------------
                plane_sky = cached_sky
                plane_horizon = cached_horizon
                plane_floor = cached_floor.copy()
                plane_foreground = cached_foreground
                plane_actors = Image.new("RGBA", (OVERSCAN_W, OVERSCAN_H), (0, 0, 0, 0))

                # Active Light Source Detection for Rim Lighting
                light_pos = (960 + OVERSCAN_X, 830 + OVERSCAN_Y)
                light_color = (251, 191, 36)
                if "nuclear_atom_plant" in props:
                    light_pos = (1460 + OVERSCAN_X, 480 + OVERSCAN_Y)
                    light_color = (34, 211, 238)
                elif env in ["desert_dunes", "ocean_surface"]:
                    light_pos = (1700 + OVERSCAN_X, 160 + OVERSCAN_Y)
                    light_color = (254, 240, 138)
                elif env == "mars_space":
                    light_pos = (1620 + OVERSCAN_X, 360 + OVERSCAN_Y)
                    light_color = (96, 165, 250)

                # ---------------- 3. Background Narrative Props ----------------
                # Bedouin Tent with Contact Shadow
                if "bedouin_tent" in props:
                    tent_img = self.sprites.get("bedouin_tent", None)
                    if tent_img:
                        render_contact_shadow(plane_floor, 300 + OVERSCAN_X + tent_img.width // 2, 500 + OVERSCAN_Y + tent_img.height, rx=240, ry=38, sigma=14)
                        plane_actors.alpha_composite(tent_img, (300 + OVERSCAN_X, 500 + OVERSCAN_Y))

                # Monumental Oil Derrick with Contact Shadow
                if "oil_derrick_monumental" in props:
                    derrick_img = self.sprites.get("oil_derrick_monumental", None)
                    if derrick_img:
                        render_contact_shadow(plane_floor, 1260 + OVERSCAN_X + derrick_img.width // 2, 240 + OVERSCAN_Y + derrick_img.height, rx=200, ry=34, sigma=14)
                        plane_actors.alpha_composite(derrick_img, (1260 + OVERSCAN_X, 240 + OVERSCAN_Y))
                    if oil_geyser:
                        oil_geyser.update(dt)
                        oil_geyser.draw(plane_actors)

                # Pirate Ship with Eyepatch
                if "pirate_ship_eyepatch" in props:
                    pirate_img = self.sprites.get("pirate_ship_eyepatch", None)
                    if pirate_img:
                        p_info = prop_beats.get("pirate_ship_eyepatch", {})
                        p_enter = p_info.get("enter_time", 0.0)
                        prog = min(1.0, max(0.0, (t_rel - p_enter) / 3.0))
                        drift_x = int(1920 - prog * (1920 - 1240)) + OVERSCAN_X
                        wave_y = int(460 + math.sin(t * 2.0) * 8) + OVERSCAN_Y
                        plane_actors.alpha_composite(pirate_img, (drift_x, wave_y))

                # Campfire & Lantern Micro-Physics & Volumetric Bloom
                if "campfire" in props or (env == "desert_tent" and "oil_lantern_tent" not in props):
                    cf_x = 960 + OVERSCAN_X
                    cf_y = 830 + OVERSCAN_Y
                    render_contact_shadow(plane_floor, cf_x, cf_y + 20, rx=130, ry=30, sigma=14)
                    self.draw_campfire_vfx(plane_floor, plane_actors, cf_x, cf_y, t)

                if "oil_lantern_tent" in props:
                    lx = 960 + OVERSCAN_X
                    ly = 780 + OVERSCAN_Y
                    render_contact_shadow(plane_floor, lx, ly + 60, rx=70, ry=20, sigma=14)
                    self.draw_lantern_vfx(plane_floor, plane_actors, lx, ly, t)

                # ---------------- 4. Character Puppets with Rim-Lighting & Breathing ----------------
                if speech_intervals:
                    if isinstance(speech_intervals[0], dict):
                        is_active_speech = any(item.get("start", 0) <= t_rel <= item.get("end", 0) for item in speech_intervals)
                    else:
                        is_active_speech = any(s <= t_rel <= e for s, e in speech_intervals)
                else:
                    is_active_speech = (t_rel < scene_dur - 0.4)

                active_chars = list(char_beats.keys()) if char_beats else chars

                for c_idx, char_id in enumerate(active_chars):
                    c_beat = char_beats.get(char_id, {
                        "anchor_target": [480 if c_idx == 0 else 1440, 810],
                        "enter_time": 0.0,
                        "enter_style": "slide_from_left" if c_idx == 0 else "slide_from_right",
                        "reactions": []
                    })

                    cur_x, cur_y, is_visible = self.compute_kinetic_anchor(c_beat, t_rel)
                    if not is_visible:
                        continue

                    # Stage overscan coordinates
                    stage_x = cur_x + OVERSCAN_X
                    stage_y = cur_y + OVERSCAN_Y

                    if char_id not in puppets:
                        sprite_key = self.get_character_sprite_key(char_id)
                        puppets[char_id] = PhysicsCharacterPuppet(sprite_key, self.sprites, anchor_pos=(stage_x, stage_y), base_scale=0.92)

                    puppet = puppets[char_id]
                    cur_expr, should_faint = self.get_puppet_reaction(c_beat, t_rel)
                    if should_faint and not puppet.is_ragdoll:
                        puppet.trigger_reaction("faint")

                    puppet.anchor_x = stage_x
                    puppet.anchor_y = stage_y

                    # Mandatory Ground Contact Shadow (Plane 3)
                    render_contact_shadow(plane_floor, stage_x, stage_y, rx=int(85 * puppet.base_scale), ry=int(22 * puppet.base_scale), sigma=14, opacity=0.72)

                    # Dynamic Alpha-Edge Rim Lighting (NumPy Fast Operation)
                    rim_dict = {
                        "char_x": stage_x,
                        "light_x": light_pos[0],
                        "color": light_color,
                        "opacity": 0.75,
                        "shift_px": 5
                    }

                    char_is_speaking = is_active_speech and (char_id == active_chars[0] or len(active_chars) == 1)
                    puppet.update(dt, t, is_speaking=char_is_speaking)
                    puppet.render(plane_actors, t_rel, expression=cur_expr, is_speaking=char_is_speaking, rim_light=rim_dict)

                # ---------------- 5. Foreground Interactive Props ----------------
                all_prop_names = list(prop_beats.keys()) if prop_beats else (props if isinstance(props, list) else [])
                for p_name in all_prop_names:
                    p_info = prop_beats.get(p_name, {})
                    p_enter = p_info.get("drop_time", p_info.get("enter_time", 0.0))
                    if t_rel < p_enter:
                        continue

                    prop_img = self.sprites.get(p_name, None)
                    if prop_img is None:
                        for sk in self.sprites.keys():
                            if p_name in sk or sk in p_name:
                                prop_img = self.sprites[sk]
                                break

                    if prop_img is not None:
                        tx = p_info.get("target_x", 1400) + OVERSCAN_X
                        ty_target = p_info.get("target_y", 720) + OVERSCAN_Y
                        drop_dt = t_rel - p_enter
                        if drop_dt < 0.28:
                            prog = drop_dt / 0.28
                            ty = int(-250 + (ty_target - (-250)) * (prog * prog))
                        else:
                            ty = ty_target + int(math.sin(t * 3.0) * 5)

                        px = int(tx - prop_img.width // 2)
                        py = int(ty - prop_img.height // 2)

                        # Mandatory Prop Ground Contact Shadow (Plane 3)
                        render_contact_shadow(plane_floor, tx, ty + prop_img.height // 2 - 12, rx=int(prop_img.width * 0.40), ry=int(prop_img.width * 0.12), sigma=14)

                        plane_actors.alpha_composite(prop_img, (px, py))

                        # Karak Chai Steam Micro-Physics
                        if "karak_chai_glass" in p_name:
                            self.draw_karak_steam(plane_actors, tx, py + 20, t)

                # ---------------- 6. Parallax 2.5D Virtual Camera Compositing ----------------
                planes_stack = [
                    (plane_sky, 0.12),
                    (plane_horizon, 0.50),
                    (plane_floor, 1.00),
                    (plane_actors, 1.00),
                    (plane_foreground, 1.42)
                ]

                # Composite view and crop to 1920x1080 with 22% vignette & grain
                frame = self.composite_2_5d_frame(planes_stack, cam_x, cam_y, cam_zoom, f_idx=rendered_frames)
                fdraw = ImageDraw.Draw(frame, "RGBA")

                # ---------------- 7. Kinetic Rubber Stamp Slam ----------------
                if stamp_info:
                    st_time = stamp_info.get("time", stamp_info.get("trigger_time", 0.5))
                    st_center = stamp_info.get("center", (960, 540))
                    if t_rel >= st_time:
                        stamp_elapsed = t_rel - st_time
                        self.mg.draw_slam_stamp(
                            frame,
                            stamp_elapsed,
                            text=stamp_info.get("text", "HISTORIC TREATY"),
                            color=tuple(stamp_info.get("color", [251, 197, 49])),
                            center=tuple(st_center)
                        )

                # ---------------- 8. Subtle Vintage Era Badge (NO DEBUG HUD!) ----------------
                if era_badge and t_rel < 3.8:
                    alpha = 255
                    if t_rel < 0.4:
                        alpha = int(255 * (t_rel / 0.4))
                    elif t_rel > 3.2:
                        alpha = int(255 * max(0.0, (3.8 - t_rel) / 0.6))

                    bbox = self.font_era.getbbox(era_badge)
                    tw = bbox[2] - bbox[0]
                    th = bbox[3] - bbox[1]
                    bx, by = 60, 50
                    fdraw.rounded_rectangle([bx, by, bx + tw + 36, by + th + 18], radius=12, fill=(15, 23, 42, int(alpha * 0.88)), outline=(251, 191, 36, alpha), width=2)
                    fdraw.text((bx + 18, by + 8), era_badge, font=self.font_era, fill=(251, 191, 36, alpha))

                # ---------------- 8.5 MapLore Kinetic Callouts & Comic Alerts ----------------
                kinetic_callouts = list(sc_beat.get("kinetic_callouts", []))
                if not kinetic_callouts and whisper_words:
                    for w_item in whisper_words:
                        w_clean = re.sub(r'[^\w]', '', w_item["word"].lower())
                        if w_clean in ["lafda", "shock", "khatam", "barium", "khel", "twist", "wait", "duniya"]:
                            kinetic_callouts.append({
                                "type": "comic_alert",
                                "badge": "!!" if w_clean != "wait" else "?!",
                                "trigger_time": w_item["start"],
                                "duration": 1.8,
                                "pos": (1140, 640) if len(active_chars) > 1 else (960, 640)
                            })
                            break

                for c_out in kinetic_callouts:
                    c_type = c_out.get("type", "comic_alert")
                    c_trigger = c_out.get("trigger_time", 0.5)
                    c_dur = c_out.get("duration", 1.8)
                    if c_type in ["comic_alert", "comic_alert_double"]:
                        pos = c_out.get("pos", (1140, 640))
                        self.mg.draw_comic_alert(frame, t_rel, badge_text=c_out.get("badge", "!!"), head_pos=pos, trigger_time=c_trigger, duration=c_dur)
                    elif c_type == "curved_pointer_bubble":
                        pos = c_out.get("mouth_pos", (1140, 700))
                        self.mg.draw_curved_pointer_callout(frame, t_rel, text=c_out.get("text", "Wait!"), mouth_pos=pos, trigger_time=c_trigger, duration=c_dur)

                # ---------------- 9. Kinetic Subtitles with Whisper Alignment ----------------
                self.mg.draw_kinetic_subtitle(frame, t_rel, vo_text, scene_dur, center_x=960, bottom_y=1010, whisper_words=whisper_words)

                # ---------------- 10. Stream to FFmpeg Pipe ----------------
                try:
                    proc.stdin.write(frame.tobytes())
                except (BrokenPipeError, OSError):
                    print("⚡ FFmpeg pipe closed at audio endpoint - finalizing video cleanly.")
                    break

                rendered_frames += 1
                if rendered_frames % 250 == 0:
                    elapsed = time.time() - start_time
                    fps_rate = rendered_frames / max(0.1, elapsed)
                    pct = (rendered_frames / float(total_frames)) * 100
                    print(f"🎬 Directed {rendered_frames}/{total_frames} frames ({pct:.1f}%) at {fps_rate:.1f} FPS...")

            global_time += scene_dur

        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()
        total_time = time.time() - start_time
        print(f"🏆 MASTER DOCUMENTARY DIRECTED & RENDERED in {total_time:.2f}s ({rendered_frames/total_time:.1f} FPS)!", flush=True)
        print(f"🎬 Output Masterpiece: {self.output_mp4}", flush=True)
        return self.output_mp4


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI Animation Director & Compositor")
    parser.add_argument("--script", default="production/directors_cut_script.json", help="Path to script JSON")
    parser.add_argument("--audio", default="production/audio", help="Path to audio directory")
    parser.add_argument("--out", default="production/master_animation.mp4", help="Output MP4 path")
    args = parser.parse_args()

    director = AIAnimationDirector(args.script, args.audio, args.out)
    director.direct_and_render()
