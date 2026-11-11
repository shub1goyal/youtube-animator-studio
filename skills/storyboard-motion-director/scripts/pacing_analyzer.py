"""
Video Pacing & Retention Analyzer
Analyzes video pacing, cut frequencies, and visual deltas using FFmpeg.
Identifies retention drop-off risk zones (scenes longer than 12 seconds with no motion).
"""

import sys
import os
import subprocess
import re
import argparse

def analyze_video_pacing(video_path, scene_threshold=0.25):
    print("=" * 60)
    print(f"PACING & RETENTION ANALYSIS: {os.path.basename(video_path)}")
    print("=" * 60)

    # 1. Get duration and stream info
    probe_cmd = ["ffmpeg", "-i", video_path]
    res = subprocess.run(probe_cmd, stderr=subprocess.PIPE, text=True)
    
    dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if not dur_match:
        print("❌ Error: Could not determine video duration.")
        return

    hours, mins, secs = map(float, dur_match.groups())
    total_duration = hours * 3600 + mins * 60 + secs
    print(f"Total Duration: {total_duration:.2f} seconds ({int(total_duration // 60)}m {int(total_duration % 60)}s)")

    # 2. Detect Scene Cuts
    print(f"Detecting scene transitions (threshold = {scene_threshold})...")
    cut_cmd = [
        "ffmpeg", "-i", video_path,
        "-filter_complex", f"select='gt(scene,{scene_threshold})',metadata=print:file=-",
        "-f", "null", "NUL"
    ]
    cut_res = subprocess.run(cut_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    timestamps = [0.0]
    for line in cut_res.stdout.splitlines():
        if "pts_time:" in line:
            m = re.search(r"pts_time:([0-9.]+)", line)
            if m:
                t = float(m.group(1))
                if t - timestamps[-1] > 0.5: # debounce cuts within 0.5s
                    timestamps.append(t)
    timestamps.append(total_duration)

    num_cuts = len(timestamps) - 2
    print(f"Total Major Visual Cuts: {num_cuts}")

    # 3. Calculate Shot Durations
    shot_durations = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
    if shot_durations:
        avg_shot = sum(shot_durations) / len(shot_durations)
        max_shot = max(shot_durations)
        min_shot = min(shot_durations)
        print(f"Average Shot Duration: {avg_shot:.2f}s")
        print(f"Shortest Shot: {min_shot:.2f}s | Longest Shot: {max_shot:.2f}s")
        
        # Pacing assessment
        print("\n[Pacing Evaluation]")
        if avg_shot <= 4.0:
            print("🚀 HYPER-KINETIC PACING (Ideal for YouTube Shorts / TikTok).")
            print("   Visual stimulation is constant. High potential for >100% Shorts retention.")
        elif 4.0 < avg_shot <= 8.5:
            print("✨ GOLDILOCKS DOCUMENTARY PACING (Ideal for 16:9 Long-Form).")
            print("   Matches the rhythm of top educational creators (OverSimplified, History Matters).")
        else:
            print("⚠️ SLOW PACING DETECTED: Average shot duration exceeds 8.5s.")
            print("   Risk of audience drop-off. Inject cutaways, kinetic zooms, or visual gags.")

        # Identify static danger zones
        danger_zones = []
        for i, dur in enumerate(shot_durations):
            if dur > 12.0:
                danger_zones.append((timestamps[i], timestamps[i+1], dur))
        
        if danger_zones:
            print(f"\n⚠️ WARNING: {len(danger_zones)} static danger zones found (>12s without major scene change):")
            for start, end, dur in danger_zones[:5]:
                print(f"   From {start:.1f}s to {end:.1f}s ({dur:.1f}s span)")
            print("   Recommendation: Add camera punch-ins, dialogue popups, or character head turns.")
        else:
            print("\n✅ RETENTION PASS: Zero stagnant scenes (>12s). Excellent visual continuity.")

    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--threshold", type=float, default=0.25, help="Scene change sensitivity")
    args = parser.parse_args()
    
    if os.path.exists(args.video):
        analyze_video_pacing(args.video, args.threshold)
    else:
        print(f"Error: File not found: {args.video}")

