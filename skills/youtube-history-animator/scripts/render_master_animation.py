"""
engine_2d/render_master_animation.py
The Master 2D Animation Timeline Director.
Renders all 11 scenes with procedural character puppet kinetics, vehicle entity motions,
particle physics (coins, oil, fireworks), animated cartography, and word-highlighted subtitles.
Streams 1080p raw frames directly into FFmpeg stdin at 200+ FPS for ultra-fast master encoding.
"""

import os
import sys
import json
import time
import math
import wave
import subprocess
import numpy as np
from PIL import Image, ImageDraw

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from puppet_animator import CharacterPuppet
from particle_system import CoinShowerSystem, OilGeyserSystem, FireworksSystem
from map_animator import MapEntityAnimator
from motion_graphics import MotionGraphicsEngine

BASE_DIR = r"c:\Users\shubh\OneDrive\Desktop\animator\uae_history_documentary"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
FFMPEG_PATH = r"C:\Users\shubh\AppData\Local\agy\bin\ffmpeg.exe"
OUTPUT_VIDEO = os.path.join(BASE_DIR, "history_of_uae_animated.mp4")


def build_background(width=1920, height=1080, bg_type="desert"):
    """Creates a base background image with gradients and vignette."""
    bg = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(bg)

    if bg_type == "desert":
        # Deep desert twilight gradient
        for y in range(height):
            prog = y / float(height)
            r = int(27 + (74 - 27) * prog)
            g = int(40 + (59 - 40) * prog)
            b = int(56 + (50 - 56) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        # Dunes silhouette at bottom
        dune_pts = [(0, 1080), (0, 840), (450, 790), (1050, 830), (1600, 780), (1920, 810), (1920, 1080)]
        draw.polygon(dune_pts, fill=(35, 25, 20, 255))
    elif bg_type == "ocean":
        # Persian Gulf turquoise azure gradient
        for y in range(height):
            prog = y / float(height)
            r = int(10 + (14 - 10) * prog)
            g = int(61 + (116 - 61) * prog)
            b = int(98 + (144 - 98) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        # Stylized water wave lines
        for wy in range(550, 1080, 45):
            draw.line([(0, wy), (width, wy)], fill=(30, 144, 255, 60), width=4)
    elif bg_type == "storm":
        # Dark gloomy crisis gradient
        for y in range(height):
            prog = y / float(height)
            r = int(35 + (20 - 35) * prog)
            g = int(12 + (8 - 12) * prog)
            b = int(18 + (10 - 18) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    elif bg_type == "oil":
        # Deep industrial night desert
        for y in range(height):
            prog = y / float(height)
            r = int(15 + (45 - 15) * prog)
            g = int(15 + (35 - 15) * prog)
            b = int(22 + (20 - 22) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        draw.rectangle([(0, 820), (width, 1080)], fill=(20, 18, 15, 255))
    elif bg_type == "royal":
        # Regal royal blue / gold gradient
        for y in range(height):
            prog = y / float(height)
            r = int(6 + (27 - 6) * prog)
            g = int(40 + (20 - 40) * prog)
            b = int(100 + (60 - 100) * prog)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    elif bg_type == "space":
        # Deep cosmic space with twinkling stars
        draw.rectangle([(0, 0), (width, height)], fill=(8, 10, 22, 255))
        import random
        rnd = random.Random(42)
        for _ in range(120):
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


def render_all_animated_scenes():
    """Main rendering loop: streams all 11 scenes to FFmpeg."""
    print("=== Initializing 2D Animation Engine ===")
    
    # 1. Load Puppets & Directors
    zayed_puppet = CharacterPuppet("sheikh_zayed")
    diver_puppet = CharacterPuppet("pearl_diver")
    officer_puppet = CharacterPuppet("british_officer")
    
    entity_anim = MapEntityAnimator()
    mg = MotionGraphicsEngine()
    
    # 2. Load Script Data
    with open(os.path.join(BASE_DIR, "script.json"), "r", encoding="utf-8") as f:
        script_data = json.load(f)
    scenes_data = {s["scene_number"]: s for s in script_data["scenes"]}

    # Measure exact scene durations from WAV audio
    scene_durations = {}
    total_duration = 0.0
    for num in range(1, 12):
        wav_path = os.path.join(AUDIO_DIR, f"scene_{num}.wav")
        with wave.open(wav_path, "rb") as w:
            dur = w.getnframes() / float(w.getframerate())
            scene_durations[num] = dur
            total_duration += dur

    print(f"Total Video Length: {total_duration:.2f}s across 11 scenes.")

    # 3. Setup FFmpeg Output Pipe
    fps = 25
    # Choose complete sound design track if available, else voiceover
    soundtrack = os.path.join(AUDIO_DIR, "master_soundtrack_complete.wav")
    if not os.path.exists(soundtrack):
        soundtrack = os.path.join(AUDIO_DIR, "final_mastered_voiceover.wav")

    ffmpeg_cmd = [
        FFMPEG_PATH,
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "-s", "1920x1080",
        "-r", str(fps),
        "-i", "-",  # Video from stdin pipe
        "-i", soundtrack,  # Complete Audio track
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        OUTPUT_VIDEO,
        "-y"
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    # 4. Render Scene by Scene
    global_time = 0.0
    start_time = time.time()
    total_frames = int(total_duration * fps)
    rendered_frames = 0

    print("Beginning frame streaming to FFmpeg...")

    for num in range(1, 12):
        scene_info = scenes_data[num]
        scene_dur = scene_durations[num]
        num_frames = int(scene_dur * fps)
        vo_text = scene_info["vo_hinglish"]

        # Instantiate scene-specific particle systems
        coins = CoinShowerSystem(coin_count=35, spawn_center=(960, 250)) if num == 5 else None
        oil_geyser = OilGeyserSystem(nozzle_pos=(1250, 720), particle_count=50) if num == 5 else None
        fireworks = FireworksSystem(num_bursts=4) if num in [7, 11] else None

        # Determine scene background type
        bg_types = {
            1: "desert", 2: "ocean", 3: "storm", 4: "royal",
            5: "oil", 6: "royal", 7: "desert", 8: "ocean",
            9: "desert", 10: "space", 11: "royal"
        }
        base_bg = build_background(1920, 1080, bg_types.get(num, "desert"))

        for f in range(num_frames):
            t_rel = f / float(fps)
            t = global_time + t_rel
            dt = 1.0 / fps

            # Clone base background
            frame = base_bg.copy()

            # ================= SCENE-SPECIFIC KINETICS =================
            if num == 1:
                # Scene 1: Camel walking, Supercar drifting, Sheikh host talking
                entity_anim.draw_camel_walk(frame, t, start_x=-150, target_x=550, y=560)
                entity_anim.draw_supercar_drift(frame, t, t_rel, start_x=2100, end_x=650, y=700)
                
                # Host puppet
                host_img = zayed_puppet.get_frame(t, t_rel, is_speaking=True, expression="neutral")
                frame.alpha_composite(host_img, (1320, 480))
                
                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 1 • 1950s: THE DESERT ORIGINS", accent=(230, 126, 34))
                mg.draw_headline_card(frame, t_rel, "A Desert With Zero Roads", "Bedouin roots vs. 2024 gold-plated supercars.")

            elif num == 2:
                # Scene 2: Sailing dhows, Pearl Diver, Oyster Shell
                entity_anim.draw_dhow_boat(frame, t, pos=(1150, 420), scale=0.85)
                entity_anim.draw_dhow_boat(frame, t + 1.5, pos=(650, 460), scale=0.6)
                
                diver_img = diver_puppet.get_frame(t, t_rel, is_speaking=True, expression="neutral")
                frame.alpha_composite(diver_img, (1320, 480))
                
                # Pearl Oyster pop-up at bottom-left
                if t_rel > 1.2:
                    frame.alpha_composite(entity_anim.oyster_sprite, (350, 680))
                    mg.draw_number_counter(frame, t_rel - 1.2, 10, 1000, prefix="$", suffix=" / Pearl", pos=(450, 600), color=(241, 196, 15))

                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 2 • 19th CENTURY: PEARL DIVING", accent=(72, 219, 251))
                mg.draw_headline_card(frame, t_rel, "The Ocean's White Gold", "80,000 Bedouin divers plunged 20m deep on a single breath.")

            elif num == 3:
                # Scene 3: The Pearl Crash, Red Arrow, Diver Faints
                entity_anim.draw_animated_trade_route(frame, t, (1600, 200), (400, 600), color=(239, 68, 68, 255))
                
                # Diver faints backwards at t_rel = 2.5
                diver_action = "faint" if t_rel > 2.5 else "idle"
                diver_expr = "x" if t_rel > 2.5 else "shocked"
                diver_img = diver_puppet.get_frame(t, t_rel, is_speaking=(t_rel <= 2.5), expression=diver_expr, action=diver_action)
                
                faint_y = 480 + int(min(200, (t_rel - 2.5) * 400)) if t_rel > 2.5 else 480
                frame.alpha_composite(diver_img, (1100, faint_y))
                
                mg.draw_slam_stamp(frame, t_rel - 2.2, text="CRASH: -95%", color=(239, 68, 68), center=(960, 450))
                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 3 • 1930s: THE GREAT CRASH", accent=(255, 71, 87))
                mg.draw_headline_card(frame, t_rel, "The Death of the Pearl Trade", "Japan's cultured pearls decimated the Gulf overnight.")

            elif num == 4:
                # Scene 4: British Officer, Royal Navy treaties
                officer_img = officer_puppet.get_frame(t, t_rel, is_speaking=True, expression="neutral")
                frame.alpha_composite(officer_img, (200, 480))
                
                entity_anim.draw_dhow_boat(frame, t, pos=(1250, 480), scale=0.75)
                mg.draw_slam_stamp(frame, t_rel - 1.5, text="PROTECTED (1820)", color=(251, 197, 49), center=(1300, 450))
                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 4 • 1820–1968: THE TRUCIAL COAST", accent=(251, 197, 49))
                mg.draw_headline_card(frame, t_rel, "The British Naval Alliance", "Anti-piracy treaties created the Trucial States.")

            elif num == 5:
                # Scene 5: Oil Derrick pumping, Gushing Oil Geyser, Coin Shower
                entity_anim.draw_oil_derrick(frame, t, pos=(1350, 680), scale=0.95)
                
                # Update & draw oil geyser
                if oil_geyser and t_rel > 1.0:
                    oil_geyser.update(dt)
                    oil_geyser.draw(frame)

                # Update & draw coin shower after 3.5s
                if coins and t_rel > 3.5:
                    coins.update(dt)
                    coins.draw(frame, t)
                    mg.draw_number_counter(frame, t_rel - 3.5, 0, 10000000000, prefix="$", suffix="+", pos=(960, 380), color=(250, 204, 21))

                # Sheikh puppet with dollar eyes
                zayed_expr = "dollar" if t_rel > 4.0 else "neutral"
                zayed_img = zayed_puppet.get_frame(t, t_rel, is_speaking=True, expression=zayed_expr)
                frame.alpha_composite(zayed_img, (180, 480))

                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 5 • 1958 & 1966: BLACK GOLD", accent=(255, 211, 42))
                mg.draw_headline_card(frame, t_rel, "Liquid Gold from the Sand", "Abu Dhabi (1958) & Dubai (1966) struck monumental oil!")

            elif num == 6:
                # Scene 6: Sheikh Zayed Visionary Leader
                zayed_img = zayed_puppet.get_frame(t, t_rel, is_speaking=True, expression="happy")
                frame.alpha_composite(zayed_img, (350, 460))
                
                # Animated connecting energy cables to Dubai
                entity_anim.draw_animated_trade_route(frame, t, (600, 600), (1450, 500), color=(0, 210, 211, 240))
                mg.draw_slam_stamp(frame, t_rel - 1.8, text="FREE HOUSING & SCHOOLS", color=(0, 210, 211), center=(1300, 450))
                
                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 6 • 1966–1971: THE VISIONARY", accent=(0, 210, 211))
                mg.draw_headline_card(frame, t_rel, "Sheikh Zayed bin Sultan Al Nahyan", "'Wealth is of no value unless used for the benefit of people.'")

            elif num == 7:
                # Scene 7: The Union Flag & Fireworks
                if fireworks:
                    fireworks.update(dt)
                    fireworks.draw(frame)

                frame.alpha_composite(entity_anim.uae_flag_sprite, (810, 260))
                
                zayed_img = zayed_puppet.get_frame(t, t_rel, is_speaking=True, expression="happy")
                frame.alpha_composite(zayed_img, (800, 480))
                
                mg.draw_slam_stamp(frame, t_rel - 1.2, text="DECEMBER 2, 1971", color=(34, 197, 94), center=(960, 460))
                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 7 • DECEMBER 2, 1971: THE UNION", accent=(29, 209, 161))
                mg.draw_headline_card(frame, t_rel, "The Birth of United Arab Emirates", "Six Emirates signed the Union Accord at Union House.")

            elif num == 8:
                # Scene 8: Jebel Ali Port & Global Trade routes
                entity_anim.draw_dhow_boat(frame, t, pos=(1200, 650), scale=1.1)
                entity_anim.draw_animated_trade_route(frame, t, (1200, 650), (200, 300), color=(76, 209, 55, 230))
                entity_anim.draw_animated_trade_route(frame, t, (1200, 650), (1700, 320), color=(76, 209, 55, 230))
                
                mg.draw_slam_stamp(frame, t_rel - 1.5, text="80% NON-OIL ECONOMY", color=(76, 209, 55), center=(800, 480))
                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 8 • 1979: BEYOND THE OIL", accent=(76, 209, 55))
                mg.draw_headline_card(frame, t_rel, "Sheikh Rashid's Masterstroke", "Jebel Ali Port: The world's largest man-made harbor.")

            elif num == 9:
                # Scene 9: Burj Khalifa rising into sky, Supercar cruising
                entity_anim.draw_burj_khalifa_growth(frame, t_rel, pos=(1350, 180), scale=1.0)
                entity_anim.draw_supercar_drift(frame, t, t_rel, start_x=2200, end_x=450, y=760)
                
                mg.draw_slam_stamp(frame, t_rel - 1.6, text="828 METERS (TALLEST ON EARTH)", color=(243, 156, 18), center=(750, 450))
                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 9 • 2000s: THE MEGACITY MIRACLE", accent=(243, 156, 18))
                mg.draw_headline_card(frame, t_rel, "Burj Khalifa & Global Magnet", "Zero income tax, safety, and futuristic infrastructure.")

            elif num == 10:
                # Scene 10: Space & Hope Mars Probe orbiting
                entity_anim.draw_hope_mars_probe(frame, t, mars_pos=(1450, 280), probe_scale=0.75)
                
                mg.draw_slam_stamp(frame, t_rel - 1.5, text="EMIRATES MARS MISSION", color=(0, 168, 255), center=(700, 450))
                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 10 • THE FUTURE: MARS & AI", accent=(0, 168, 255))
                mg.draw_headline_card(frame, t_rel, "From Sand Dunes to the Stars", "Hope probe enters Mars orbit; UAE pioneers national AI strategy.")

            elif num == 11:
                # Scene 11: Finale, all characters together, Fireworks, Subscribe
                if fireworks:
                    fireworks.update(dt)
                    fireworks.draw(frame)

                zayed_img = zayed_puppet.get_frame(t, t_rel, is_speaking=True, expression="happy")
                diver_img = diver_puppet.get_frame(t + 0.3, t_rel, is_speaking=False, expression="smile")
                officer_img = officer_puppet.get_frame(t + 0.6, t_rel, is_speaking=False, expression="neutral")
                
                frame.alpha_composite(officer_img, (150, 480))
                frame.alpha_composite(zayed_img, (760, 460))
                frame.alpha_composite(diver_img, (1350, 480))

                # Pulsing Subscribe Button
                pulse = 1.0 + 0.08 * math.sin(t * 8.0)
                mg.draw_slam_stamp(frame, t_rel - 0.5, text="🔔 SUBSCRIBE FOR MORE HISTORY!", color=(241, 196, 15), center=(960, 360))
                
                mg.draw_chapter_badge(frame, t_rel, "CHAPTER 11 • FINALE: WHAT DO YOU THINK?", accent=(241, 196, 15))
                mg.draw_headline_card(frame, t_rel, "Will UAE Rule the 21st Century?", "Drop your comments below! Which historical topic next?")

            # ================= COMMON FOREGROUND: KINETIC SUBTITLE =================
            mg.draw_kinetic_subtitle(frame, t_rel, vo_text, scene_dur, center_x=960, bottom_y=1020)

            # ================= CONVERT TO BGR & PIPE TO FFMPEG =================
            frame_rgb = frame.convert("RGB")
            # Convert PIL RGB to BGR numpy array
            arr = np.array(frame_rgb)
            bgr_arr = arr[:, :, ::-1]  # RGB to BGR
            proc.stdin.write(bgr_arr.tobytes())

            rendered_frames += 1
            if rendered_frames % 100 == 0:
                elapsed = time.time() - start_time
                fps_rate = rendered_frames / max(0.1, elapsed)
                print(f"Rendered {rendered_frames}/{total_frames} frames ({rendered_frames/total_frames*100:.1f}%) at {fps_rate:.1f} FPS...")

        global_time += scene_dur

    # Close pipe and finalize video
    proc.stdin.close()
    _, stderr = proc.communicate()
    total_elapsed = time.time() - start_time
    print(f"=== Master Animation Completed in {total_elapsed:.2f}s ({rendered_frames / total_elapsed:.1f} FPS) ===")
    print(f"Final Master Animated Video: {OUTPUT_VIDEO}")


if __name__ == "__main__":
    render_all_animated_scenes()

