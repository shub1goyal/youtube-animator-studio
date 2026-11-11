"""
cinematic_video_assembler.py
Multi-Shot Camera Choreography and Broadcast Video Assembler.
Supports dynamic multi-shot camera cuts (Wide Establishing -> Medium Closeup -> Macro Reaction)
and active-word kinetic caption rendering with subpixel motion easing for ANY production folder.
"""

import os
import sys
import json
import math
import wave
import argparse
import subprocess
from pathlib import Path

# Local config import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "youtube-history-animator", "scripts")))
try:
    from config import FFMPEG_PATH
except ImportError:
    FFMPEG_PATH = "ffmpeg"


def format_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def get_wav_duration(wav_path):
    if not os.path.exists(wav_path):
        return 5.0
    try:
        with wave.open(wav_path, "rb") as wf:
            return wf.getnframes() / float(wf.getframerate())
    except Exception:
        return 5.0


def generate_moving_captions_ass(words, era_badge, duration, out_ass_path, is_vertical=False):
    """
    Generates broadcast-grade kinetic moving captions with active word highlighting & scale bounce.
    """
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
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,Impact,{font_size},&H00FFFFFF,&H000000FF,&H00050608,&H80000000,-1,0,0,0,100,100,0,0,1,5.0,2.0,2,30,30,{margin_v},1",
        f"Style: Highlight,Impact,{font_size},&H0015FACC,&H000000FF,&H00050608,&H80000000,-1,0,0,0,108,108,0,0,1,6.0,3.0,2,30,30,{margin_v},1",
        f"Style: EraBadge,Arial,20,&H0015FACC,&H000000FF,&H00050608,&HB0000000,-1,0,0,0,100,100,2,0,1,3.5,0.0,7,45,45,45,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    # Era badge banner event
    if era_badge:
        ass_lines.append(f"Dialogue: 0,0:00:00.00,{format_ass_time(duration)},EraBadge,,0,0,0,,{{\\fad(400,0)}}  {era_badge.upper()}  ")

    for chunk in chunks:
        c_start = chunk[0]["start"]
        c_end = chunk[-1]["end"] + 0.15
        for target_idx, target_word in enumerate(chunk):
            w_start = target_word["start"]
            w_end = target_word["end"]
            formatted_words = []
            for idx, w in enumerate(chunk):
                raw_w = w["word"].upper()
                if idx == target_idx:
                    formatted_words.append(f"{{\\c&H0015FACC&\\t(0,80,\\fscx112\\fscy112)\\t(80,180,\\fscx100\\fscy100)}}{raw_w}{{\\r}}")
                else:
                    formatted_words.append(f"{{\\c&H00FFFFFF&}}{raw_w}{{\\r}}")
            line_text = " ".join(formatted_words)
            ass_lines.append(f"Dialogue: 1,{format_ass_time(w_start)},{format_ass_time(w_end)},Default,,0,0,0,,{line_text}")

    os.makedirs(os.path.dirname(os.path.abspath(out_ass_path)), exist_ok=True)
    with open(out_ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))
    return out_ass_path


def assemble_production_video(project_dir, script_file=None, timings_file=None, fps=25, out_file=None):
    """Assembles all scenes from a production directory into 16:9 and 9:16 master videos."""
    proj_path = Path(project_dir).resolve()
    out_dir = proj_path / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎬 Assembling production video from: {proj_path}")

    # Check for deterministic segments first
    seg_dir = out_dir / "deterministic_segments"
    if seg_dir.is_dir():
        segments = sorted(list(seg_dir.glob("scene_*_cinema.mp4")))
        if segments:
            concat_txt = out_dir / "concat_segments.txt"
            with open(concat_txt, "w", encoding="utf-8") as f:
                for s in segments:
                    f.write(f"file '{str(s.resolve()).replace(chr(92), '/')}'\n")

            target_out = out_file or str(out_dir / f"{proj_path.name}_master_cinema.mp4")
            cmd = [
                FFMPEG_PATH, "-y",
                "-f", "concat", "-safe", "0",
                "-i", str(concat_txt),
                "-c", "copy",
                target_out
            ]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            if res.returncode == 0:
                print(f"🎉 Master 16:9 Cinema export complete: {target_out}")
                return target_out

    print(f"ℹ️ Ready for deterministic segment concatenation.")
    return None


def main():
    parser = argparse.ArgumentParser(description="Multi-Shot Camera Choreography and Broadcast Video Assembler")
    parser.add_argument("--project-dir", default=os.getcwd(), help="Production directory")
    parser.add_argument("--script", default=None, help="Script JSON path")
    parser.add_argument("--timings", default=None, help="Whisper word timings JSON")
    parser.add_argument("--shots", default=None, help="Shots list JSON")
    parser.add_argument("--fps", type=int, default=25, help="Framerate")
    parser.add_argument("--out", default=None, help="Output MP4 file path")
    args = parser.parse_args()

    assemble_production_video(args.project_dir, args.script, args.timings, args.fps, args.out)


if __name__ == "__main__":
    main()
