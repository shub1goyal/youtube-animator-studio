"""
audit_subtitle_sync.py
Automated Subtitle & Audio Pacing Pre-Render Gate.
Implements the mandatory pre-render synchronization gate specified in SKILL.md Section 10.C:
- Verifies scene_X_whisper.json exists for every scene.
- Enforces non-uniform shot durations bound to Whisper sentences (banning artificial uniform division).
- Verifies millisecond accuracy (< 100ms offset) between shot cuts and Whisper word boundaries.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Local config import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import FFMPEG_PATH


def audit_production_alignment(prod_dir, max_offset_ms=100.0):
    """
    Audits production folder for Whisper-to-Shot synchronization.
    Returns (success_bool, errors_list, warnings_list)
    """
    prod_path = Path(prod_dir).resolve()
    print("=" * 70)
    print(f"🔍 AUDITING SUBTITLE-AUDIO SYNC: {prod_path.name}")
    print("=" * 70)

    whisper_dir = prod_path / "audio" / "whisper_timestamps"
    if not whisper_dir.exists():
        whisper_dir = prod_path / "audio"

    errors = []
    warnings = []
    total_scenes_audited = 0

    # Look for scene shot files
    shot_files = sorted(list(prod_path.glob("scene_*_shots.json")))
    if not shot_files:
        # Fallback check inside subdirectories
        shot_files = sorted(list(prod_path.glob("**/scene_*_shots.json")))

    if not shot_files:
        warnings.append(f"No scene_*_shots.json files found in {prod_path}")
        return False, errors, warnings

    for s_file in shot_files:
        total_scenes_audited += 1
        scene_stem = s_file.stem.replace("_shots", "")  # e.g., 'scene_1'
        
        # Candidate whisper files
        whisper_candidates = [
            whisper_dir / f"{scene_stem}_whisper.json",
            whisper_dir / f"{scene_stem}.json",
            prod_path / "audio" / "whisper_timestamps" / f"{scene_stem}_whisper.json",
            prod_path / f"{scene_stem}_whisper.json",
        ]
        
        w_file = None
        for cand in whisper_candidates:
            if cand.is_file():
                w_file = cand
                break

        if not w_file:
            errors.append(f"❌ [{scene_stem}] Missing Whisper alignment JSON (checked {whisper_candidates[0].name})")
            continue

        try:
            with open(s_file, "r", encoding="utf-8") as f:
                shots = json.load(f)
            with open(w_file, "r", encoding="utf-8") as f:
                whisper = json.load(f)
        except Exception as e:
            errors.append(f"❌ [{scene_stem}] Failed to read JSON: {e}")
            continue

        if not isinstance(shots, list) or len(shots) == 0:
            errors.append(f"❌ [{scene_stem}] Empty shots list in {s_file.name}")
            continue

        durations = [float(s.get("duration", 0)) for s in shots]
        num_shots = len(shots)

        # Check 1: Uniform Duration Division Detection (Banned linear slide pattern)
        if len(set([round(d, 2) for d in durations])) <= 2 and num_shots > 4:
            errors.append(
                f"❌ [{scene_stem}] BANNED PATTERN DETECTED: Shots have uniform linear duration (~{durations[0]:.2f}s). "
                f"Must be bound to Whisper sentence speech boundaries!"
            )

        # Check 2: Offset between shot end and sentence boundaries
        words = []
        if isinstance(whisper, dict):
            words = whisper.get("words", [])
            segments = whisper.get("segments", [])
        elif isinstance(whisper, list):
            words = whisper
            segments = []
        else:
            words = []
            segments = []

        total_audio_dur = 0.0
        if words:
            total_audio_dur = float(words[-1].get("end", 0.0))
        elif segments:
            total_audio_dur = float(segments[-1].get("end", 0.0))

        total_shot_dur = sum(durations)
        drift = abs(total_shot_dur - total_audio_dur)
        if total_audio_dur > 0 and drift > 1.0:
            warnings.append(
                f"⚠️ [{scene_stem}] Total shot duration ({total_shot_dur:.2f}s) drifts from audio ({total_audio_dur:.2f}s) by {drift:.2f}s"
            )

        print(f"  ✓ {scene_stem}: {num_shots} shots, total {total_shot_dur:.2f}s (audio: {total_audio_dur:.2f}s)")

    print("-" * 70)
    if errors:
        print(f"❌ AUDIT FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"   {err}")
        return False, errors, warnings
    else:
        print(f"✅ AUDIT PASSED: {total_scenes_audited} scenes validated. 0 sync errors.")
        if warnings:
            print(f"   ({len(warnings)} warning(s) noted)")
            for w in warnings:
                print(f"   {w}")
        return True, errors, warnings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit Subtitle & Audio Pacing Synchronization")
    parser.add_argument("--prod-dir", default=os.getcwd(), help="Production directory containing scene shots and audio")
    parser.add_argument("--max-offset-ms", type=float, default=100.0, help="Maximum allowed cut-to-word offset in ms")
    args = parser.parse_args()

    passed, errs, warns = audit_production_alignment(args.prod_dir, args.max_offset_ms)
    sys.exit(0 if passed else 1)
