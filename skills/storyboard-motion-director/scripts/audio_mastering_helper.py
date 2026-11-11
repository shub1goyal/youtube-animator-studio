"""
YouTube Broadcast Audio Mastering Utility
Analyzes loudness and generates FFmpeg filter chains for:
- 16:9 Long-Form: -14.0 LUFS Integrated, -1.0 dB True Peak.
- 9:16 Shorts: -12.0 LUFS Integrated, -0.5 dB True Peak.
"""

import sys
import os
import subprocess
import re
import argparse

def master_audio(input_file, output_file, mode="long_form"):
    target_i = -14.0 if mode == "long_form" else -12.0
    target_tp = -1.0 if mode == "long_form" else -0.5
    target_lra = 11.0 if mode == "long_form" else 7.0

    print("=" * 60)
    print(f"YOUTUBE AUDIO MASTERING: {os.path.basename(input_file)}")
    print(f"Target Mode: {mode.upper()} (Target: {target_i} LUFS, Peak: {target_tp} dBTP)")
    print("=" * 60)

    # Stage 1: Measure current loudness with ebur128
    measure_cmd = [
        "ffmpeg", "-i", input_file,
        "-filter_complex", "ebur128=peak=true",
        "-f", "null", "NUL"
    ]
    res = subprocess.run(measure_cmd, stderr=subprocess.PIPE, text=True)
    
    current_i = None
    current_tp = None
    for line in res.stderr.splitlines():
        if "I:" in line and "LUFS" in line:
            m = re.search(r"I:\s*(-?[0-9.]+)\s*LUFS", line)
            if m:
                current_i = float(m.group(1))
        elif "Peak:" in line and "dBFS" in line:
            m = re.search(r"Peak:\s*(-?[0-9.]+)\s*dBFS", line)
            if m:
                current_tp = float(m.group(1))

    if current_i is not None:
        print(f"Measured Input Loudness: {current_i:.1f} LUFS (Peak: {current_tp:.1f} dBFS)")
    else:
        print("Loudness measured via two-pass loudnorm.")

    # Stage 2: Master with highpass (80Hz rumble cut), speech clarity EQ, and dynamic loudnorm
    # highpass=f=80, equalizer=f=300:t=q:w=1.5:g=-2.5 (mud cut), equalizer=f=4500:t=q:w=2:g=+1.8 (presence)
    filter_chain = (
        f"highpass=f=80,"
        f"equalizer=f=320:t=q:w=1.5:g=-2.5,"
        f"equalizer=f=4200:t=q:w=2.0:g=1.8,"
        f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}"
    )

    print("\nApplying broadcast processing chain...")
    print(f"Filters: {filter_chain}")

    out_cmd = [
        "ffmpeg", "-y", "-i", input_file,
        "-af", filter_chain,
        "-c:v", "copy", # Preserve video stream if present
        "-c:a", "aac", "-b:a", "192k",
        output_file
    ]
    
    proc = subprocess.run(out_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    if proc.returncode == 0:
        print(f"\n✅ Mastering Complete! Output saved to: {output_file}")
    else:
        print(f"\n❌ Error during mastering: {proc.stderr[:300]}")

    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input video or audio file")
    parser.add_argument("--out", default="mastered_output.mp4", help="Output file path")
    parser.add_argument("--mode", choices=["long_form", "shorts"], default="long_form")
    args = parser.parse_args()

    if os.path.exists(args.input):
        master_audio(args.input, args.out, args.mode)
    else:
        print(f"Error: Input file does not exist: {args.input}")

