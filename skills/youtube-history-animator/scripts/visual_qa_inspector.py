"""
skills/youtube-history-animator/scripts/visual_qa_inspector.py

Automated Visual QA & Quality Inspector for 2.5D Animated Studio Outputs.
Extracts evenly spaced frame samples across the timeline, synthesizes a labeled
4x3 contact sheet PNG, and computes forensic metrics (luminance, motion delta,
black-frame / freeze-frame detection) into qa_report.json.
"""

import os
import sys
import json
import shutil
import argparse
import tempfile
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Import centralized configuration
try:
    from config import FFMPEG_PATH
except ImportError:
    FFMPEG_PATH = os.environ.get("FFMPEG_PATH") or shutil.which("ffmpeg") or "ffmpeg"


def get_video_duration(video_path):
    """Retrieves video duration in seconds using ffmpeg output."""
    cmd = [FFMPEG_PATH, "-i", str(video_path)]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors="replace")
    for line in proc.stderr.splitlines():
        if "Duration:" in line:
            # Format: Duration: 00:00:15.00, start: ...
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            if len(parts) == 3:
                hours = float(parts[0])
                mins = float(parts[1])
                secs = float(parts[2])
                return hours * 3600 + mins * 60 + secs
    return 15.0  # Fallback duration if unparsed


def extract_sample_frames(video_path, num_frames=12, temp_dir=None):
    """Extracts evenly spaced frame samples from the video."""
    duration = get_video_duration(video_path)
    if duration <= 0:
        duration = 1.0

    frames = []
    timestamps = []

    # Calculate interval timestamps (avoid exact 0.0s boundary)
    step = duration / num_frames
    for i in range(num_frames):
        t = (i + 0.5) * step
        if t >= duration:
            t = max(0.0, duration - 0.1)
        timestamps.append(t)

        out_img = os.path.join(temp_dir, f"frame_{i:02d}_{t:.2f}s.png")
        cmd = [
            FFMPEG_PATH,
            "-y",
            "-i", str(video_path),
            "-ss", f"{t:.3f}",
            "-frames:v", "1",
            "-q:v", "2",
            str(out_img)
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(out_img):
            frames.append(out_img)
        else:
            # Generate black placeholder if ffmpeg fails on a frame
            img = Image.new("RGB", (1920, 1080), (10, 10, 15))
            img.save(out_img)
            frames.append(out_img)

    return frames, timestamps, duration


def compute_frame_metrics(frame_paths):
    """Forensically analyzes frame brightness, contrast, and inter-frame delta."""
    luminances = []
    motion_deltas = []
    prev_gray = None
    width, height = 1920, 1080

    for idx, f_path in enumerate(frame_paths):
        with Image.open(f_path) as im:
            if idx == 0:
                width, height = im.size
            im_rgb = im.convert("RGB")
            im_gray = im.convert("L")

            # Average luminance across all pixels
            raw_bytes = im_gray.tobytes()
            stat_lum = sum(raw_bytes) / len(raw_bytes)
            luminances.append(round(stat_lum, 2))

            # Inter-frame motion delta (MAE)
            if prev_gray is not None:
                # Downsample to 160x90 for fast pixel diff
                p1 = prev_gray.resize((160, 90), Image.Resampling.BILINEAR)
                p2 = im_gray.resize((160, 90), Image.Resampling.BILINEAR)
                d1 = p1.tobytes()
                d2 = p2.tobytes()
                diff = sum(abs(a - b) for a, b in zip(d1, d2)) / len(d1)
                motion_deltas.append(round(diff, 2))
            prev_gray = im_gray

    avg_lum = sum(luminances) / len(luminances) if luminances else 0.0
    avg_delta = sum(motion_deltas) / len(motion_deltas) if motion_deltas else 0.0

    # Checks
    is_blackout = avg_lum < 10.0
    is_frozen = (avg_delta < 1.0) and (len(motion_deltas) > 0)
    has_underlit_frames = any(lum < 5.0 for lum in luminances)

    status = "PASS"
    issues = []
    if is_blackout:
        status = "FAIL"
        issues.append("Critical: Video appears entirely black/blank.")
    if is_frozen:
        status = "WARN"
        issues.append("Warning: Very low motion delta across timeline; check for frozen layers.")
    if has_underlit_frames:
        issues.append("Notice: Some frames have near-zero luminance.")

    report = {
        "status": status,
        "resolution": f"{width}x{height}",
        "frame_count": len(frame_paths),
        "avg_luminance": round(avg_lum, 2),
        "min_luminance": min(luminances) if luminances else 0.0,
        "max_luminance": max(luminances) if luminances else 0.0,
        "avg_motion_delta": round(avg_delta, 2),
        "frame_luminances": luminances,
        "inter_frame_deltas": motion_deltas,
        "issues": issues
    }
    return report


def build_contact_sheet(frame_paths, timestamps, out_path, cols=4, rows=3, title="VISUAL QA CONTACT SHEET"):
    """Composites frames into a high-resolution 4x3 labeled contact sheet."""
    thumb_w, thumb_h = 440, 248
    margin = 16
    header_h = 70
    footer_h = 40

    total_w = cols * thumb_w + (cols + 1) * margin
    total_h = header_h + rows * thumb_h + (rows + 1) * margin + footer_h

    sheet = Image.new("RGB", (total_w, total_h), (15, 17, 23))
    draw = ImageDraw.Draw(sheet)

    # Header Bar
    draw.rectangle([(0, 0), (total_w, header_h)], fill=(24, 28, 38))
    draw.text((margin, 18), title, fill=(245, 158, 11))
    draw.text((margin, 40), f"Generated by VisualQAInspector | Samples: {len(frame_paths)} frames", fill=(148, 163, 184))

    for idx, (f_path, t_val) in enumerate(zip(frame_paths, timestamps)):
        r = idx // cols
        c = idx % cols
        x = margin + c * (thumb_w + margin)
        y = header_h + margin + r * (thumb_h + margin)

        with Image.open(f_path) as im:
            thumb = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y))

        # Border
        draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], outline=(51, 65, 85), width=2)

        # Timestamp badge
        badge_text = f"#{idx+1:02d} | {t_val:.2f}s"
        badge_w = 90
        badge_h = 22
        bx = x + 8
        by = y + thumb_h - badge_h - 8
        draw.rectangle([(bx, by), (bx + badge_w, by + badge_h)], fill=(15, 23, 42, 220), outline=(245, 158, 11), width=1)
        draw.text((bx + 8, by + 4), badge_text, fill=(255, 255, 255))

    # Footer note
    draw.text((margin, total_h - 28), "youtube-animator-studio • Hybrid 2.5D Animation Stack QA Audit", fill=(100, 116, 139))

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    sheet.save(out_path, quality=92)
    return out_path


def run_visual_qa(video_path, out_sheet=None, report_path=None, num_frames=12):
    """End-to-end QA execution."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    video_p = Path(video_path).resolve()
    if not out_sheet:
        out_sheet = str(video_p.parent / f"{video_p.stem}_contact_sheet.png")
    if not report_path:
        report_path = str(video_p.parent / f"{video_p.stem}_qa_report.json")

    with tempfile.TemporaryDirectory() as tmp_dir:
        print(f"🔍 Sampling {num_frames} frames from: {video_p.name}...")
        frames, timestamps, duration = extract_sample_frames(video_p, num_frames=num_frames, temp_dir=tmp_dir)

        print(f"📊 Computing forensic metrics across {len(frames)} frames...")
        report = compute_frame_metrics(frames)
        report["duration_seconds"] = round(duration, 2)
        report["source_video"] = str(video_p)

        print(f"🖼️ Rendering contact sheet (4x3) to: {out_sheet}...")
        build_contact_sheet(frames, timestamps, out_sheet, title=f"VISUAL QA: {video_p.name} ({duration:.1f}s)")

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        verdict_icon = "✅" if report["status"] == "PASS" else ("⚠️" if report["status"] == "WARN" else "❌")
        print(f"\n{verdict_icon} QA VERDICT: {report['status']}")
        print(f"   • Resolution: {report['resolution']}")
        print(f"   • Avg Luminance: {report['avg_luminance']} (Min: {report['min_luminance']}, Max: {report['max_luminance']})")
        print(f"   • Avg Motion Delta: {report['avg_motion_delta']} px")
        if report["issues"]:
            for issue in report["issues"]:
                print(f"   • {issue}")
        print(f"📄 Report: {report_path}")
        print(f"🖼️ Sheet:  {out_sheet}\n")

        return report


def main():
    parser = argparse.ArgumentParser(description="Automated Visual QA Inspector for 2.5D Animated Studio Videos")
    parser.add_argument("--video", required=True, help="Path to input .mp4 video file")
    parser.add_argument("--out", default=None, help="Output path for contact sheet PNG")
    parser.add_argument("--report", default=None, help="Output path for qa_report.json")
    parser.add_argument("--frames", type=int, default=12, help="Number of sample frames (default: 12)")
    args = parser.parse_args()

    run_visual_qa(args.video, out_sheet=args.out, report_path=args.report, num_frames=args.frames)


if __name__ == "__main__":
    main()
