"""
kinetic_video_renderer.py
Deterministic Frame-by-Frame Playwright/Chromium + FFmpeg Renderer.
Executes scene_X_movie.html or animated SVG stages via window.seekToTime(t) at 25/30/60 FPS.
Ensures CSS/JS animations, viewBox camera zooms/pans, shallow DOF blurs, character breathing/blinking/visemes,
and MapLore callouts are rendered deterministically on every single frame.
"""

import os
import sys
import re
import wave
import time
import argparse
import subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# Local cross-platform config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import FFMPEG_PATH, CHROME_PATH

try:
    from audit_subtitle_sync import audit_production_alignment
except ImportError:
    audit_production_alignment = None


def get_audio_duration(wav_path):
    """Calculates exact duration from 16-bit PCM WAV header."""
    if not os.path.exists(wav_path):
        return 0.0
    try:
        with wave.open(wav_path, "rb") as wf:
            return wf.getnframes() / float(wf.getframerate())
    except Exception:
        return 0.0


def render_scene_worker(scene_id, prod_dir, fps=25, force=False, quality=95):
    """
    Renders a single scene using Playwright headless browser stepped deterministically via window.seekToTime(t).
    Pipes JPEG frame buffers directly to FFmpeg stdin (zero temp files on disk).
    """
    from playwright.sync_api import sync_playwright

    prod_path = Path(prod_dir).resolve()
    html_candidates = [
        prod_path / f"scene_{scene_id}_movie.html",
        prod_path / f"scene_{scene_id}.html",
    ]
    html_file = None
    for cand in html_candidates:
        if cand.is_file():
            html_file = cand
            break

    if not html_file:
        print(f"⚠️ [Scene {scene_id:02d}] Missing movie HTML file ({html_candidates[0].name})")
        return False

    wav_candidates = [
        prod_path / "audio" / f"scene_{scene_id}.wav",
        prod_path / f"scene_{scene_id}.wav",
        prod_path / "audio" / f"scene_{scene_id:02d}.wav",
    ]
    wav_file = None
    for cand in wav_candidates:
        if cand.is_file():
            wav_file = cand
            break

    output_dir = prod_path / "output" / "deterministic_segments"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_mp4 = output_dir / f"scene_{scene_id}_cinema.mp4"

    if not force and out_mp4.is_file() and out_mp4.stat().st_size > 100000:
        print(f"⏩ [Scene {scene_id:02d}] Already rendered ({out_mp4.name}) — skipping (use --force to re-render)")
        return True

    # Audio duration
    dur = get_audio_duration(str(wav_file)) if wav_file else 0.0
    if dur <= 0.0:
        # Check shots file or HTML file for fallback duration
        shots_file = prod_path / f"scene_{scene_id}_shots.json"
        if shots_file.is_file():
            try:
                import json
                with open(shots_file, "r", encoding="utf-8") as f:
                    shots = json.load(f)
                    dur = sum(float(s.get("duration", 0)) for s in shots)
            except Exception:
                dur = 0.0

        if dur <= 0.0 and html_file and html_file.is_file():
            try:
                import re, json
                with open(html_file, "r", encoding="utf-8") as f:
                    c = f.read()
                    match = re.search(r'const\s+SHOTS\s*=\s*(\[.*?\]);', c, re.DOTALL)
                    if match:
                        shots = json.loads(match.group(1))
                        dur = max([float(s.get("end", 0)) for s in shots] + [sum(float(s.get("duration", 0)) for s in shots)] + [10.0])
            except Exception:
                dur = 10.0

        if dur <= 0.0:
            dur = 10.0

    total_frames = int(math.ceil(dur * fps))
    print(f"🎬 [Scene {scene_id:02d}] Rendering {total_frames} frames ({dur:.2f}s @ {fps}fps) -> {out_mp4.name}")

    ffmpeg_cmd = [
        FFMPEG_PATH,
        "-y",
        "-f", "image2pipe",
        "-vcodec", "mjpeg",
        "-r", str(fps),
        "-i", "pipe:0",
    ]

    if wav_file and os.path.exists(wav_file):
        ffmpeg_cmd.extend([
            "-i", str(wav_file),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(out_mp4)
        ])
    else:
        ffmpeg_cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-crf", "18",
            str(out_mp4)
        ])

    ff_proc = subprocess.Popen(
        ffmpeg_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    t0 = time.time()
    try:
        with sync_playwright() as p:
            launch_args = {
                "headless": True,
                "args": [
                    "--disable-web-security",
                    "--allow-file-access-from-files",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-gpu",
                ]
            }
            if CHROME_PATH and os.path.isfile(CHROME_PATH):
                launch_args["executable_path"] = CHROME_PATH

            browser = p.chromium.launch(**launch_args)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

            file_url = html_file.resolve().as_uri()
            page.goto(file_url, wait_until="load")
            page.evaluate("window.isExternalRenderMode = true;")

            for frame_idx in range(total_frames):
                current_time = frame_idx / float(fps)
                page.evaluate(f"if (window.seekToTime) {{ window.seekToTime({current_time:.4f}); }} else if (window.renderMovieFrame) {{ window.renderMovieFrame({current_time:.4f}); }}")
                frame_bytes = page.screenshot(type="jpeg", quality=quality)
                ff_proc.stdin.write(frame_bytes)

            browser.close()

        ff_proc.stdin.close()
        ff_proc.wait()
        elapsed = time.time() - t0
        fps_achieved = total_frames / max(elapsed, 0.001)
        print(f"✅ [Scene {scene_id:02d}] Finished in {elapsed:.1f}s ({fps_achieved:.1f} FPS) -> {out_mp4.name}")
        return True

    except Exception as e:
        if ff_proc and ff_proc.stdin:
            try:
                ff_proc.stdin.close()
            except Exception:
                pass
        print(f"❌ [Scene {scene_id:02d}] Render failed: {e}")
        return False


def render_all_scenes_parallel(prod_dir, scenes=None, fps=25, max_workers=2, force=False):
    """Renders all scenes in a production folder and concatenates them into master video."""
    prod_path = Path(prod_dir).resolve()
    
    if scenes is None:
        html_files = sorted(list(prod_path.glob("scene_*_movie.html")))
        scenes = []
        for hf in html_files:
            m = re.search(r"scene_(\d+)_movie\.html", hf.name)
            if m:
                scenes.append(int(m.group(1)))
        scenes = sorted(list(set(scenes)))

    if not scenes:
        print(f"No scenes found to render in {prod_path}")
        return False

    print(f"🚀 Starting Deterministic Batch Render for scenes: {scenes}")
    out_dir = prod_path / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    segments_dir = out_dir / "deterministic_segments"
    segments_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(render_scene_worker, sc, str(prod_path), fps, force): sc
            for sc in scenes
        }
        for f in as_completed(futures):
            sc = futures[f]
            try:
                if f.result():
                    success_count += 1
            except Exception as e:
                print(f"❌ Worker error on scene {sc}: {e}")

    print(f"\n📊 Render summary: {success_count}/{len(scenes)} scenes completed successfully.")

    # Master concatenation
    segment_files = [segments_dir / f"scene_{sc}_cinema.mp4" for sc in scenes]
    valid_segments = [s for s in segment_files if s.is_file() and s.stat().st_size > 100000]

    if len(valid_segments) == len(scenes):
        concat_txt = out_dir / "concat_list.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for s in valid_segments:
                escaped = str(s.resolve()).replace("\\", "/")
                f.write(f"file '{escaped}'\n")

        master_mp4 = out_dir / f"{prod_path.name}_deterministic_master.mp4"
        print(f"📦 Concatenating {len(valid_segments)} segments -> {master_mp4.name} ...")
        cmd = [
            FFMPEG_PATH,
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            str(master_mp4)
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if res.returncode == 0:
            sz_mb = master_mp4.stat().st_size / (1024 * 1024)
            print(f"🎉 MASTER EXPORT COMPLETE: {master_mp4} ({sz_mb:.1f} MB)")
            return True
        else:
            print(f"❌ Master concat failed: {res.stderr.decode('utf-8', errors='ignore')}")
            return False
    return False


if __name__ == "__main__":
    import math
    parser = argparse.ArgumentParser(description="Deterministic 2.5D Movie Renderer")
    parser.add_argument("--prod-dir", default=os.getcwd(), help="Production directory")
    parser.add_argument("--scene", type=int, default=None, help="Render single scene")
    parser.add_argument("--fps", type=int, default=25, help="Render framerate")
    parser.add_argument("--workers", type=int, default=2, help="Parallel worker threads")
    parser.add_argument("--force", action="store_true", help="Force re-render existing segments")
    args = parser.parse_args()

    if args.scene is not None:
        success = render_scene_worker(args.scene, args.prod_dir, args.fps, args.force)
        sys.exit(0 if success else 1)
    else:
        success = render_all_scenes_parallel(args.prod_dir, None, args.fps, args.workers, args.force)
        sys.exit(0 if success else 1)

