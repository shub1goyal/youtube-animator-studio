"""
engine_2d/full_documentary_renderer.py
The Complete Physics-Aware Long-Form Documentary 2D Animation Director.
Renders all N scenes of a 10-15 minute historical documentary with:
- Physics-based character puppet kinetics (damped harmonic springs, squash & stretch, ragdoll knockouts)
- Dynamic environmental particle systems (3D spinning gold coins, oil geysers, celebratory fireworks)
- Animated cartography & vehicle kinetics (moving camels, drifting supercars, rocking dhows, Burj Khalifa growth, Mars orbit)
- Calm, steady phrase-chunked subtitles (4-5 words anchored for 2.5s with dynamic gold word highlight)
- Broadcast audio integration: mixes -14.0 LUFS dialogue with multi-layer sound design bed
- Streams 1080p raw frames directly into FFmpeg stdin pipe for maximum efficiency
"""

import os
import sys
import json
import time
import math
import wave
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Add engine_2d directory to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from physics_rig import PhysicsCharacterPuppet, SpringDamper, RagdollEntity
from particle_system import CoinShowerSystem, OilGeyserSystem, FireworksSystem
from map_animator import MapEntityAnimator
from motion_graphics import MotionGraphicsEngine
from asset_library import HighFidelityAssetManager

FFMPEG_PATH = r"C:\Users\shubh\AppData\Local\agy\bin\ffmpeg.exe"


def get_wav_duration(wav_path):
    """Calculates exact duration in seconds from WAV header."""
    try:
        with wave.open(wav_path, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)
    except Exception:
        return 12.0


def build_background(width=1920, height=1080, bg_type="desert"):
    """Creates a high-contrast cinematic background."""
    bg = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(bg)

    if bg_type == "desert":
        for y in range(height):
            prog = y / float(height)
            r = int(25 + (70 - 25) * prog)
            g = int(38 + (55 - 38) * prog)
            b = int(54 + (45 - 54) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        dune_pts = [(0, 1080), (0, 840), (450, 790), (1050, 830), (1600, 780), (1920, 810), (1920, 1080)]
        draw.polygon(dune_pts, fill=(35, 25, 20, 255))
    elif bg_type == "ocean":
        for y in range(height):
            prog = y / float(height)
            r = int(10 + (12 - 10) * prog)
            g = int(55 + (110 - 55) * prog)
            b = int(90 + (140 - 90) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        for wy in range(550, 1080, 45):
            draw.line([(0, wy), (width, wy)], fill=(30, 144, 255, 60), width=4)
    elif bg_type == "storm":
        for y in range(height):
            prog = y / float(height)
            r = int(32 + (18 - 32) * prog)
            g = int(10 + (6 - 10) * prog)
            b = int(15 + (8 - 15) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    elif bg_type == "oil":
        for y in range(height):
            prog = y / float(height)
            r = int(14 + (40 - 14) * prog)
            g = int(14 + (30 - 14) * prog)
            b = int(20 + (18 - 20) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        draw.rectangle([(0, 820), (width, 1080)], fill=(18, 16, 14, 255))
    elif bg_type == "royal":
        for y in range(height):
            prog = y / float(height)
            r = int(6 + (24 - 6) * prog)
            g = int(35 + (18 - 35) * prog)
            b = int(90 + (55 - 90) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    elif bg_type == "space":
        draw.rectangle([(0, 0), (width, height)], fill=(6, 8, 18, 255))
        import random
        rnd = random.Random(42)
        for _ in range(150):
            sx, sy = rnd.randint(0, width), rnd.randint(0, height)
            draw.ellipse([sx-1, sy-1, sx+1, sy+1], fill=(240, 245, 255, rnd.randint(120, 255)))
    else:
        for y in range(height):
            prog = y / float(height)
            r = int(20 + 20 * prog)
            g = int(25 + 20 * prog)
            b = int(35 + 20 * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    return bg


class FullDocumentaryRenderer:
    def __init__(self, script_path, audio_dir, output_mp4):
        self.script_path = script_path
        self.audio_dir = audio_dir
        self.output_mp4 = output_mp4

        with open(script_path, "r", encoding="utf-8") as f:
            self.script_data = json.load(f)

        self.asset_mgr = HighFidelityAssetManager()
        self.mg = MotionGraphicsEngine()
        self.entity_anim = MapEntityAnimator()

        # Load sprites dictionary
        self.sprites = self.asset_mgr.cached_images

    def render_complete_documentary(self, fps=25):
        """Renders every single scene in the documentary into the final master MP4."""
        sys.stdout.reconfigure(line_buffering=True)
        scenes = self.script_data.get("scenes", [])
        n_scenes = len(scenes)
        print(f"🎬 Initiating Full Documentary Master Render: {n_scenes} Scenes at {fps} FPS...", flush=True)

        # 1. Calculate exact durations
        scene_durations = []
        total_duration = 0.0
        for i, sc in enumerate(scenes, 1):
            wav_file = os.path.join(self.audio_dir, f"scene_{i}.wav")
            if os.path.exists(wav_file):
                d = get_wav_duration(wav_file)
            else:
                d = float(sc.get("duration_seconds", 14.0))
            # Pad by 0.25s for natural pause between scenes
            d = max(3.0, d + 0.25)
            scene_durations.append(d)
            total_duration += d

        print(f"⏱️ Total Master Video Runtime: {total_duration:.2f}s ({total_duration/60:.2f} minutes) across {n_scenes} scenes.")

        # Master audio file
        master_audio = os.path.join(self.audio_dir, "master_soundtrack_complete.wav")
        if not os.path.exists(master_audio):
            master_audio = os.path.join(self.audio_dir, "final_mastered_voiceover.wav")

        # 2. Setup FFmpeg Output Pipe with Direct RGBA Pipe for Ultra-Fast Frame Streaming
        ffmpeg_cmd = [
            FFMPEG_PATH,
            "-f", "rawvideo",
            "-pix_fmt", "rgba",
            "-s", "1920x1080",
            "-r", str(fps),
            "-i", "-",  # Video from stdin pipe (direct RGBA bytes)
            "-i", master_audio,  # Synchronized master audio
            "-c:v", "libx264",
            "-preset", "faster",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "256k",
            "-shortest",
            self.output_mp4,
            "-y"
        ]

        # Prevent pipe buffer deadlocks by discarding stdout and letting stderr write to devnull
        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 3. Instantiate Physics Character Puppets
        zayed_puppet = PhysicsCharacterPuppet("sheikh_zayed", self.sprites, anchor_pos=(1350, 780), base_scale=0.95)
        officer_puppet = PhysicsCharacterPuppet("british_officer", self.sprites, anchor_pos=(320, 780), base_scale=0.92)
        diver_puppet = PhysicsCharacterPuppet("pearl_diver", self.sprites, anchor_pos=(960, 780), base_scale=0.92)

        global_time = 0.0
        start_time = time.time()
        total_frames = int(total_duration * fps)
        rendered_frames = 0

        # Background types cycle
        bg_cycle = ["desert", "ocean", "storm", "royal", "oil", "royal", "desert", "ocean", "desert", "space", "royal"]

        # 4. Render Scene by Scene
        for idx, (scene, scene_dur) in enumerate(zip(scenes, scene_durations), 1):
            num_frames = int(scene_dur * fps)
            cue = scene.get("visual_cue", "").lower()
            vo_text = scene.get("vo_hinglish", "")
            sfx_cue = scene.get("sfx", "")

            # Reset puppet physics at scene start
            zayed_puppet.trigger_reaction("reset")
            officer_puppet.trigger_reaction("reset")
            diver_puppet.trigger_reaction("reset")

            # Determine background
            bg_type = "desert"
            if any(w in cue for w in ["ocean", "sea", "pearl", "dive", "dhow", "water"]):
                bg_type = "ocean"
            elif any(w in cue for w in ["storm", "crash", "collapse", "crisis", "faint", "poverty"]):
                bg_type = "storm"
            elif any(w in cue for w in ["oil", "gusher", "rig", "derrick", "drilling", "money"]):
                bg_type = "oil"
            elif any(w in cue for w in ["british", "treaty", "union", "sheikh", "federation", "royalty"]):
                bg_type = "royal"
            elif any(w in cue for w in ["space", "mars", "satellite", "hope", "future", "stars"]):
                bg_type = "space"
            else:
                bg_type = bg_cycle[idx % len(bg_cycle)]

            base_bg = build_background(1920, 1080, bg_type)

            # Scene-specific particle systems
            coins = CoinShowerSystem(coin_count=35, spawn_center=(960, 220)) if any(w in cue for w in ["coin", "money", "rich", "gold", "billion"]) else None
            oil_geyser = OilGeyserSystem(nozzle_pos=(1250, 720), particle_count=50) if any(w in cue for w in ["oil", "derrick", "gusher"]) else None
            fireworks = FireworksSystem(num_bursts=4) if any(w in cue for w in ["union", "celebrate", "firework", "victory"]) else None

            # Chapter badge info
            act_label = f"SCENE {idx} • {scene.get('time_range', f'ACT {(idx-1)//5 + 1}')}"

            for f in range(num_frames):
                t_rel = f / float(fps)
                t = global_time + t_rel
                dt = 1.0 / fps

                frame = base_bg.copy()

                # Update physics puppets
                is_host_speaking = (t_rel < scene_dur - 0.5)
                zayed_puppet.update(dt, t, is_speaking=is_host_speaking)
                officer_puppet.update(dt, t, is_speaking=False)
                diver_puppet.update(dt, t, is_speaking=False)

                # ================= CINEMATIC VISUAL ELEMENTS =================
                if any(w in cue for w in ["camel", "desert"]):
                    self.entity_anim.draw_camel_walk(frame, t, start_x=-150, target_x=550, y=560)
                if any(w in cue for w in ["supercar", "car", "modern"]):
                    self.entity_anim.draw_supercar_drift(frame, t, t_rel, start_x=2200, end_x=650, y=720)
                if any(w in cue for w in ["dhow", "boat", "sail"]):
                    self.entity_anim.draw_dhow_boat(frame, t, pos=(1150, 420), scale=0.85)
                    self.entity_anim.draw_dhow_boat(frame, t + 1.5, pos=(600, 460), scale=0.6)
                if any(w in cue for w in ["burj", "tower", "skyline"]):
                    self.entity_anim.draw_burj_khalifa_growth(frame, t_rel, pos=(1350, 180), scale=1.0)
                if any(w in cue for w in ["mars", "probe", "satellite"]):
                    self.entity_anim.draw_hope_mars_probe(frame, t, mars_pos=(1450, 280), probe_scale=0.75)

                # Oil derrick & geyser
                if oil_geyser:
                    self.entity_anim.draw_oil_derrick(frame, t, pos=(1350, 680), scale=0.95)
                    oil_geyser.update(dt)
                    oil_geyser.draw(frame)

                # Coin shower
                if coins:
                    coins.update(dt)
                    coins.draw(frame, t)

                # Fireworks
                if fireworks:
                    fireworks.update(dt)
                    fireworks.draw(frame)

                # Character staging based on cues
                if any(w in cue for w in ["british", "officer", "treaty"]):
                    officer_puppet.anchor_x = 320
                    officer_puppet.render(frame, t_rel, expression="neutral", is_speaking=False)
                    # Treaty stamp
                    if t_rel > 1.2:
                        self.mg.draw_slam_stamp(frame, t_rel - 1.2, text="BRITISH TREATY (1820)", color=(251, 197, 49), center=(960, 420))

                if any(w in cue for w in ["pearl", "diver", "crash"]):
                    # If crash, trigger faint ragdoll
                    if "crash" in cue and t_rel > 2.2 and not diver_puppet.is_ragdoll:
                        diver_puppet.trigger_reaction("faint")
                    diver_puppet.anchor_x = 750 if "british" in cue else 960
                    diver_puppet.render(frame, t_rel, expression="shocked" if "crash" in cue else "neutral")

                # Zayed Host is always present on right or center
                zayed_expr = "dollar" if coins else ("happy" if fireworks else "neutral")
                zayed_puppet.anchor_x = 1450
                zayed_puppet.render(frame, t_rel, expression=zayed_expr, is_speaking=is_host_speaking)

                # Chapter badge & Headline
                self.mg.draw_chapter_badge(frame, t_rel, act_label, accent=(245, 158, 11))
                headline_title = scene.get("headline", f"History of UAE — Episode #{idx}")
                headline_sub = scene.get("subhead", vo_text[:60] + "...")
                self.mg.draw_headline_card(frame, t_rel, headline_title, headline_sub)

                # ================= ROCK-SOLID STEADY SUBTITLES =================
                self.mg.draw_kinetic_subtitle(frame, t_rel, vo_text, scene_dur, center_x=960, bottom_y=1010)

                # Direct Zero-Copy RGBA Pipe to FFmpeg
                proc.stdin.write(frame.tobytes())

                rendered_frames += 1
                if rendered_frames % 250 == 0:
                    elapsed = time.time() - start_time
                    fps_rate = rendered_frames / max(0.1, elapsed)
                    percent = (rendered_frames / float(total_frames)) * 100
                    print(f"🎬 Rendered {rendered_frames}/{total_frames} frames ({percent:.1f}%) at {fps_rate:.1f} FPS...")

            global_time += scene_dur

        # Finalize video and allow FFmpeg to write moov atom
        proc.stdin.close()
        proc.wait()
        total_time = time.time() - start_time
        print(f"🏆 COMPLETE MASTER DOCUMENTARY RENDERED in {total_time:.2f}s ({rendered_frames/total_time:.1f} FPS)!", flush=True)
        print(f"Output File: {self.output_mp4}", flush=True)
        return self.output_mp4

