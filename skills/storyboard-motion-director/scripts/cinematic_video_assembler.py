"""
cinematic_video_assembler.py
Broadcast-grade Video Assembler for YouTube Animation Studio.
Solves:
1. 'zoom s not smooth' -> Subpixel floating-point OpenCV Lanczos camera engine with quintic easing (zero pixel snapping or stepping).
2. 'we need more cuts' -> 12 dynamic cinematic shots (3 distinct angles/punches per scene: Wide -> Detail -> Reaction).
3. 'moving captions' -> Word-by-word kinetic animated ASS captions (active word scales up 112% in glowing electric yellow).
"""

import os
import sys
import json
import wave
import subprocess
import cv2
import numpy as np

SCRIPT_DIR = r"c:\Users\shubh\OneDrive\Desktop\animator\youtube_history_30s"
SCENES_DIR = os.path.join(SCRIPT_DIR, "scenes")
AUDIO_DIR = os.path.join(SCRIPT_DIR, "audio")
OUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

FFMPEG = r"C:\Users\shubh\AppData\Local\agy\bin\ffmpeg.exe"


def format_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def get_wav_duration(wav_path):
    with wave.open(wav_path, "rb") as wf:
        return wf.getnframes() / float(wf.getframerate())


def generate_moving_captions_ass(words, era_badge, duration, out_ass_path, is_vertical=False):
    """
    Generates broadcast-grade kinetic moving captions with active word highlighting & scale bounce.
    """
    # Chunk words into 2-3 word units or on pauses >= 0.28s
    chunks = []
    current_chunk = []
    
    for w in words:
        if not current_chunk:
            current_chunk.append(w)
            continue
        prev_w = current_chunk[-1]
        gap = w["start"] - prev_w["end"]
        if len(current_chunk) >= 3 or gap >= 0.28:
            chunks.append(current_chunk)
            current_chunk = [w]
        else:
            current_chunk.append(w)
    if current_chunk:
        chunks.append(current_chunk)

    play_w = 1080 if is_vertical else 1920
    play_h = 1920 if is_vertical else 1080
    font_size = 56 if is_vertical else 48
    margin_v = 450 if is_vertical else 85

    ass_lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {play_w}",
        f"PlayResY: {play_h}",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: MovingCaption,Arial Black,{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,5.0,2.5,2,40,40,{margin_v},1",
        f"Style: EraBadge,Segoe UI,28,&H00E2E8F0,&H000000FF,&H00090A0F,&HA0090A0F,-1,0,0,0,100,100,0,0,1,2.5,2.0,7,60,60,60,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    # Era badge in upper corner
    if era_badge:
        clean_badge = era_badge.replace("•", "-").strip()
        t_badge_end = format_ass_time(min(3.2, duration))
        ass_lines.append(f"Dialogue: 0,0:00:00.20,{t_badge_end},EraBadge,,0,0,0,,{{\\fade(250,350)}}{clean_badge}")

    # Moving caption events
    for chunk in chunks:
        chunk_end = chunk[-1]["end"] + 0.12
        for active_idx, target_w in enumerate(chunk):
            w_start = target_w["start"]
            if active_idx < len(chunk) - 1:
                w_end = min(chunk[active_idx + 1]["start"], target_w["end"] + 0.08)
            else:
                w_end = chunk_end

            parts = []
            for j, w in enumerate(chunk):
                w_clean = w["text"].upper()
                if j == active_idx:
                    # Electric Yellow glow with 114% scale pop
                    parts.append(f"{{\\c&H0000E6FF&\\fscx114\\fscy114}}{w_clean}{{\\r\\c&H00FFFFFF&}}")
                else:
                    parts.append(w_clean)

            line_text = " ".join(parts)
            ass_lines.append(f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},MovingCaption,,0,0,0,,{line_text}")

    with open(out_ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines) + "\n")
    return out_ass_path


# Shot choreography configurations for all 12 cuts
# Coordinates relative to 3840x2160 source canvas
SHOT_CHOREOGRAPHY = {
    1: [
        # Shot 1.1: Wide Establishing Shot (0.00s -> 4.50s)
        {
            "start_time": 0.00,
            "end_time": 4.50,
            "start_cx": 1920.0, "start_cy": 1080.0, "start_scale": 0.50,
            "end_cx": 1820.0,   "end_cy": 1050.0, "end_scale": 0.55
        },
        # Shot 1.2: Medium Close-Up Punch on Jawed Karim (4.50s -> 6.50s)
        {
            "start_time": 4.50,
            "end_time": 6.50,
            "start_cx": 2240.0, "start_cy": 780.0, "start_scale": 0.88,
            "end_cx": 2200.0,   "end_cy": 760.0, "end_scale": 0.94
        },
        # Shot 1.3: Macro Detail on 2005 Camcorder LCD & Elephant (6.50s -> 9.00s)
        {
            "start_time": 6.50,
            "end_time": 9.00,
            "start_cx": 1050.0, "start_cy": 1100.0, "start_scale": 0.82,
            "end_cx": 1250.0,   "end_cy": 980.0,  "end_scale": 0.72
        }
    ],
    2: [
        # Shot 2.1: Server Room Wide Panic Shot (0.00s -> 2.00s)
        {
            "start_time": 0.00,
            "end_time": 2.00,
            "start_cx": 1920.0, "start_cy": 1080.0, "start_scale": 0.50,
            "end_cx": 1920.0,   "end_cy": 980.0,  "end_scale": 0.56
        },
        # Shot 2.2: Extreme Close-Up Founder Panic Scream Face (2.00s -> 5.00s)
        {
            "start_time": 2.00,
            "end_time": 5.00,
            "start_cx": 1720.0, "start_cy": 780.0, "start_scale": 0.92,
            "end_cx": 1720.0,   "end_cy": 760.0, "end_scale": 1.02
        },
        # Shot 2.3: Macro Dial 100°C & Meltdown Server Rack (5.00s -> 8.11s)
        {
            "start_time": 5.00,
            "end_time": 8.11,
            "start_cx": 2520.0, "start_cy": 560.0, "start_scale": 0.85,
            "end_cx": 2400.0,   "end_cy": 600.0, "end_scale": 0.92
        }
    ],
    3: [
        # Shot 3.1: Late Night Diner Booth Two-Shot (0.00s -> 2.20s)
        {
            "start_time": 0.00,
            "end_time": 2.20,
            "start_cx": 1920.0, "start_cy": 1080.0, "start_scale": 0.50,
            "end_cx": 1920.0,   "end_cy": 1040.0, "end_scale": 0.54
        },
        # Shot 3.2: Macro Punch on $1.65B Contract & Gold Seal (2.20s -> 5.20s)
        {
            "start_time": 2.20,
            "end_time": 5.20,
            "start_cx": 1920.0, "start_cy": 1250.0, "start_scale": 0.90,
            "end_cx": 1920.0,   "end_cy": 1220.0, "end_scale": 0.98
        },
        # Shot 3.3: Ecstatic Founder Dollar-Sign Eyes ($$) Reaction (5.20s -> 7.51s)
        {
            "start_time": 5.20,
            "end_time": 7.51,
            "start_cx": 2440.0, "start_cy": 680.0, "start_scale": 0.90,
            "end_cx": 2420.0,   "end_cy": 660.0, "end_scale": 0.98
        }
    ],
    4: [
        # Shot 4.1: Grand Stadium Stage Wide (0.00s -> 3.00s)
        {
            "start_time": 0.00,
            "end_time": 3.00,
            "start_cx": 1920.0, "start_cy": 1080.0, "start_scale": 0.50,
            "end_cx": 1920.0,   "end_cy": 980.0,  "end_scale": 0.56
        },
        # Shot 4.2: Macro Close-Up Gold & Diamond Creator Awards (3.00s -> 5.50s)
        {
            "start_time": 3.00,
            "end_time": 5.50,
            "start_cx": 980.0,  "start_cy": 1360.0, "start_scale": 0.88,
            "end_cx": 1200.0,   "end_cy": 1320.0, "end_scale": 0.82
        },
        # Shot 4.3: Leaping Creator Finale with Confetti Blizzard (5.50s -> 7.87s)
        {
            "start_time": 5.50,
            "end_time": 7.87,
            "start_cx": 1920.0, "start_cy": 1280.0, "start_scale": 0.86,
            "end_cx": 1920.0,   "end_cy": 1220.0, "end_scale": 0.96
        }
    ]
}


def render_scene_smooth(scene_idx, script_data, word_timings, fps=30):
    """
    Renders one scene segment with:
    - 3 rapid cinematic cuts (subpixel Lanczos easing)
    - Moving kinetic captions
    - Broadcast audio
    """
    sc_info = script_data["scenes"][scene_idx - 1]
    era_badge = sc_info.get("era_badge", "")
    words = word_timings[str(scene_idx)]
    
    img_4k_path = os.path.join(SCENES_DIR, f"scene_{scene_idx:02d}_4k.png")
    wav_path = os.path.join(AUDIO_DIR, f"scene_{scene_idx:02d}.wav")
    ass_path = os.path.join(OUT_DIR, f"moving_caps_scene_{scene_idx:02d}.ass")
    out_mp4 = os.path.join(OUT_DIR, f"cut_segment_{scene_idx:02d}.mp4")
    
    dur = get_wav_duration(wav_path)
    total_frames = int(dur * fps)
    
    # 1. Build moving captions ASS
    generate_moving_captions_ass(words, era_badge, dur, ass_path, is_vertical=False)
    
    # 2. Load 4K image
    img = cv2.imread(img_4k_path)
    if img is None:
        raise FileNotFoundError(f"Missing 4K image: {img_4k_path}")
        
    cuts = SHOT_CHOREOGRAPHY[scene_idx]
    # Adjust last cut end_time to match exact audio duration
    cuts[-1]["end_time"] = dur
    
    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\\\:")
    vf = f"subtitles={ass_escaped}"
    
    cmd = [
        FFMPEG, "-y",
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "-s", "1920x1080",
        "-r", str(fps),
        "-i", "-",
        "-i", wav_path,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{dur:.2f}",
        out_mp4
    ]
    
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    for f in range(total_frames):
        current_time = f / float(fps)
        
        # Determine active cut
        active_cut = cuts[-1]
        for c in cuts:
            if c["start_time"] <= current_time < c["end_time"]:
                active_cut = c
                break
                
        cut_duration = max(0.01, active_cut["end_time"] - active_cut["start_time"])
        local_t = min(1.0, max(0.0, (current_time - active_cut["start_time"]) / cut_duration))
        
        # Quintic butter-smooth easing: 6t^5 - 15t^4 + 10t^3
        ease = 6 * (local_t ** 5) - 15 * (local_t ** 4) + 10 * (local_t ** 3)
        
        scale = active_cut["start_scale"] + (active_cut["end_scale"] - active_cut["start_scale"]) * ease
        cx = active_cut["start_cx"] + (active_cut["end_cx"] - active_cut["start_cx"]) * ease
        cy = active_cut["start_cy"] + (active_cut["end_cy"] - active_cut["start_cy"]) * ease
        
        # Subpixel floating-point affine matrix
        M = np.float32([
            [scale, 0, 960.0 - cx * scale],
            [0, scale, 540.0 - cy * scale]
        ])
        
        frame = cv2.warpAffine(img, M, (1920, 1080), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
        p.stdin.write(frame.tobytes())
        
    p.stdin.close()
    p.wait()
    
    if p.returncode != 0:
        raise RuntimeError(f"FFmpeg failed on scene {scene_idx} with code {p.returncode}")
        
    print(f"  ✅ Scene {scene_idx} rendered with {len(cuts)} cuts: {out_mp4}")
    return out_mp4


def compile_master_video():
    """Compiles all scenes into the final broadcast-grade 1080p landscape & 9:16 vertical shorts!"""
    with open(os.path.join(SCRIPT_DIR, "script.json"), "r", encoding="utf-8") as f:
        script_data = json.load(f)
        
    with open(os.path.join(SCRIPT_DIR, "word_timings.json"), "r", encoding="utf-8") as f:
        word_timings = json.load(f)
        
    print("🚀 Rendering 12 Dynamic Cuts with Butter-Smooth Subpixel Zoom & Moving Captions...")
    segment_files = []
    
    for idx in range(1, 5):
        seg_mp4 = render_scene_smooth(idx, script_data, word_timings, fps=30)
        segment_files.append(seg_mp4)
        
    # Concatenate segments
    concat_txt = os.path.join(OUT_DIR, "concat_smooth.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for seg in segment_files:
            f.write(f"file '{seg.replace(chr(92), '/')}'\n")
            
    master_mp4 = os.path.join(OUT_DIR, "history_of_youtube_30s_v2.mp4")
    cmd_cat = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-c", "copy",
        master_mp4
    ]
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"\n🎉 16:9 MASTER VIDEO COMPLETE: {master_mp4}")
    
    # Generate 9:16 Vertical Shorts companion format
    shorts_mp4 = os.path.join(OUT_DIR, "history_of_youtube_30s_v2_shorts.mp4")
    print(f"\n📱 Generating 9:16 Vertical Shorts companion: {shorts_mp4}...")
    vf_vertical = (
        "split[a][b];"
        "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
        "[b]scale=1080:-1[fg];"
        "[bg][fg]overlay=0:(H-h)/2"
    )
    cmd_shorts = [
        FFMPEG, "-y",
        "-i", master_mp4,
        "-vf", vf_vertical,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        shorts_mp4
    ]
    subprocess.run(cmd_shorts, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"🎉 9:16 VERTICAL SHORTS COMPLETE: {shorts_mp4}")
    
    return master_mp4, shorts_mp4


if __name__ == "__main__":
    compile_master_video()
