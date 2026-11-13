#!/usr/bin/env python3
"""
build_audio_timeline.py
Universal Audio-First Beat Synchronizer & Procedural Sound Designer.
1. Synthesizes seamless documentary voiceover via edge-tts + captures exact WordBoundary events.
2. Maps every script beat in episode_script.json to exact frame boundaries (2.0s-3.2s per beat).
3. Mixes voiceover + subtle warm tension drone + frame-exact procedural SFX into public/audio/master.wav.
4. Exports deterministic src/data/timeline.json for Remotion pure-code rendering.
"""
import asyncio
import json
import math
import re
import subprocess
from pathlib import Path

import edge_tts
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "episode_script.json"
AUDIO_DIR = ROOT / "public" / "audio"
DATA_DIR = ROOT / "src" / "data"
FFMPEG = r"C:\Users\shubh\AppData\Local\agy\bin\ffmpeg.exe"


def norm_word(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


async def synthesize_with_word_timestamps(full_text: str, voice: str, rate: str, mp3_path: Path):
    communicate = edge_tts.Communicate(full_text, voice=voice, rate=rate, boundary="WordBoundary")
    words = []
    with open(mp3_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = chunk["offset"] / 10_000_000.0
                dur_sec = chunk["duration"] / 10_000_000.0
                words.append(
                    {
                        "text": chunk["text"],
                        "norm": norm_word(chunk["text"]),
                        "start": round(start_sec, 4),
                        "end": round(start_sec + dur_sec, 4),
                    }
                )
    return words


def make_sfx(kind: str, sr: int = 44100) -> np.ndarray:
    """Crisp, subtle editorial motion-design Foley synthesized purely in NumPy/SciPy."""
    rng = np.random.default_rng(42)
    if kind in ("whoosh_soft", "whoosh_low", "whoosh_tight", "sweep_down"):
        dur = 0.28 if kind != "whoosh_low" else 0.38
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        noise = rng.standard_normal(len(t))
        cutoff = 900 if kind == "whoosh_low" else (1600 if kind == "whoosh_soft" else 2200)
        b, a = butter(3, cutoff / (sr / 2), btype="low")
        filtered = lfilter(b, a, noise)
        env = np.sin(np.pi * (t / dur)) ** 1.8
        tone_f0 = 190 if kind == "sweep_down" else 130
        tone_f1 = 75 if kind == "sweep_down" else 180
        sweep = np.sin(2 * np.pi * np.cumsum(np.linspace(tone_f0, tone_f1, len(t))) / sr) * 0.35
        return (filtered * 0.45 + sweep) * env * 0.22

    if kind == "thud_double":
        dur = 0.45
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        hit1 = np.sin(2 * np.pi * (110 * np.exp(-t * 14)) * t) * np.exp(-t * 12)
        t2 = np.clip(t - 0.18, 0, None)
        mask2 = (t >= 0.18).astype(float)
        hit2 = np.sin(2 * np.pi * (95 * np.exp(-t2 * 14)) * t2) * np.exp(-t2 * 12) * mask2
        return (hit1 + hit2 * 0.9) * 0.28

    if kind == "paper_snap":
        dur = 0.14
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        noise = rng.standard_normal(len(t))
        b, a = butter(2, [800 / (sr / 2), 4500 / (sr / 2)], btype="band")
        snap = lfilter(b, a, noise) * np.exp(-t * 28)
        return snap * 0.22

    if kind == "ink_slash":
        dur = 0.26
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        noise = rng.standard_normal(len(t))
        b, a = butter(2, [1200 / (sr / 2), 6000 / (sr / 2)], btype="band")
        slash = lfilter(b, a, noise) * np.sin(np.pi * (t / dur)) ** 0.7 * np.exp(-t * 6)
        sub = np.sin(2 * np.pi * 85 * t) * np.exp(-t * 16) * 0.5
        return (slash + sub) * 0.28

    if kind == "impact_boom":
        dur = 0.65
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        freq = 55 + 95 * np.exp(-t * 18)
        phase = 2 * np.pi * np.cumsum(freq) / sr
        sub = np.sin(phase) * np.exp(-t * 5.5)
        crunch = lfilter(*butter(2, 900 / (sr / 2), btype="low"), rng.standard_normal(len(t))) * np.exp(-t * 18) * 0.4
        return (sub + crunch) * 0.34

    if kind == "lock_slam":
        dur = 0.42
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        clank = (
            np.sin(2 * np.pi * 420 * t) * 0.35
            + np.sin(2 * np.pi * 685 * t) * 0.25
            + np.sin(2 * np.pi * 92 * t) * 0.8
        ) * np.exp(-t * 13)
        return clank * 0.26

    if kind == "dark_braam":
        dur = 1.1
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        sig = (
            np.sin(2 * np.pi * 55.0 * t) * 0.6
            + np.sin(2 * np.pi * 110.0 * t + 0.3 * np.sin(2 * np.pi * 3 * t)) * 0.35
            + np.sin(2 * np.pi * 164.8 * t) * 0.2
        )
        env = np.minimum(t / 0.08, 1.0) * np.exp(-t * 2.4)
        return sig * env * 0.26

    # final_chime
    dur = 1.2
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    sig = (
        np.sin(2 * np.pi * 220.0 * t) * 0.5
        + np.sin(2 * np.pi * 329.63 * t) * 0.35
        + np.sin(2 * np.pi * 440.0 * t) * 0.2
    ) * np.exp(-t * 2.6)
    return sig * 0.20


def build_ambient_bed(total_samples: int, sr: int = 44100) -> np.ndarray:
    """Subtle documentary tension drone + soft rhythmic pulse (-26 dB under narration)."""
    t = np.arange(total_samples) / sr
    # Warm A1 (55Hz) + E2 (82.4Hz) subtle cinematic pad
    lfo = 0.65 + 0.35 * np.sin(2 * np.pi * 0.22 * t)
    pad = (
        np.sin(2 * np.pi * 55.0 * t) * 0.55
        + np.sin(2 * np.pi * 82.41 * t) * 0.30
        + np.sin(2 * np.pi * 110.0 * t) * 0.15
    ) * lfo
    # Soft 96 BPM muted heartbeat pulse every 0.625s
    beat_period = 0.625
    phase_in_beat = np.mod(t, beat_period)
    pulse = np.sin(2 * np.pi * 62.0 * phase_in_beat) * np.exp(-phase_in_beat * 18.0) * 0.45
    bed = (pad * 0.032) + (pulse * 0.028)
    # Fade in 0.4s, fade out 1.2s
    fade_in = np.minimum(t / 0.4, 1.0)
    fade_out = np.minimum((t[-1] - t) / 1.2, 1.0)
    return bed * fade_in * fade_out


def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    spec = json.loads(SCRIPT_PATH.read_text(encoding="utf-8"))
    fps = spec["fps"]
    beats_spec = spec["beats"]
    full_text = " ".join(b["text"] for b in beats_spec)

    raw_mp3 = AUDIO_DIR / "vo_raw.mp3"
    raw_wav = AUDIO_DIR / "vo_raw.wav"
    master_wav = AUDIO_DIR / "master.wav"

    print(f"Synthesizing VO ({len(beats_spec)} beats)...")
    words = asyncio.run(
        synthesize_with_word_timestamps(
            full_text=full_text,
            voice=spec["voice"],
            rate=spec.get("rate", "+8%"),
            mp3_path=raw_mp3,
        )
    )
    print(f"Captured {len(words)} exact WordBoundary events.")

    # Convert MP3 to 44.1kHz mono WAV via FFmpeg
    subprocess.run(
        [FFMPEG, "-y", "-i", str(raw_mp3), "-ac", "1", "-ar", "44100", str(raw_wav)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    sr, vo_pcm = wavfile.read(str(raw_wav))
    vo = vo_pcm.astype(np.float32) / 32768.0

    # Add 0.85s tail hold so the final punchline lands cleanly
    tail_sec = 0.85
    total_samples = len(vo) + int(sr * tail_sec)
    total_duration_sec = round(total_samples / sr, 4)
    total_frames = int(math.ceil(total_duration_sec * fps))

    # Align each beat's tokens to word stream sequentially
    word_cursor = 0
    aligned_beats = []
    for idx, b in enumerate(beats_spec):
        raw_tokens = [norm_word(tok) for tok in b["text"].split() if norm_word(tok)]
        start_w_idx = word_cursor
        # Advance word_cursor across matching tokens
        matched = 0
        while word_cursor < len(words) and matched < len(raw_tokens):
            # Handle hyphenated tokens like "eighty-six" (edge-tts may emit 1 or 2 boundaries)
            w_norm = words[word_cursor]["norm"]
            target_norm = raw_tokens[matched]
            if w_norm == target_norm or w_norm in target_norm or target_norm in w_norm:
                matched += 1
                word_cursor += 1
            else:
                # Check if next word boundary splits a compound token
                if matched > 0 and w_norm in raw_tokens[matched - 1]:
                    word_cursor += 1
                else:
                    matched += 1
                    word_cursor += 1

        end_w_idx = max(start_w_idx, word_cursor - 1)
        start_sec = 0.0 if idx == 0 else words[start_w_idx]["start"]
        aligned_beats.append(
            {
                "index": idx,
                "id": b["id"],
                "archetype": b["archetype"],
                "chapter": b["chapter"],
                "sfx": b["sfx"],
                "text": b["text"],
                "startSec": round(start_sec, 4),
                "wordStartIdx": start_w_idx,
                "wordEndIdx": end_w_idx,
            }
        )

    # Make beats tile 100% seamlessly from 0 to total_duration_sec (zero black gaps!)
    for idx, ab in enumerate(aligned_beats):
        if idx + 1 < len(aligned_beats):
            # Start visual transition 40ms before spoken word for snappy perceptual sync
            next_start = max(ab["startSec"] + 0.5, aligned_beats[idx + 1]["startSec"] - 0.04)
            aligned_beats[idx + 1]["startSec"] = round(next_start, 4)
            ab["endSec"] = round(next_start, 4)
        else:
            ab["endSec"] = total_duration_sec

        ab["durationSec"] = round(ab["endSec"] - ab["startSec"], 4)
        ab["startFrame"] = int(round(ab["startSec"] * fps))
        ab["endFrame"] = total_frames if idx == len(aligned_beats) - 1 else int(round(ab["endSec"] * fps))
        ab["durationFrames"] = max(1, ab["endFrame"] - ab["startFrame"])

    # Mix master audio: VO + ambient drone + beat-synced SFX
    mix = np.zeros(total_samples, dtype=np.float32)
    # Normalize VO peak to 0.86
    vo_peak = np.max(np.abs(vo)) or 1.0
    mix[: len(vo)] += (vo / vo_peak) * 0.86
    mix += build_ambient_bed(total_samples, sr)

    for ab in aligned_beats:
        sfx_wave = make_sfx(ab["sfx"], sr=sr)
        pos = max(0, int(ab["startSec"] * sr))
        end_pos = min(total_samples, pos + len(sfx_wave))
        if end_pos > pos:
            mix[pos:end_pos] += sfx_wave[: end_pos - pos]
        # Extra sub-beat cavalry slam SFX inside b08_pincer
        if ab["id"] == "b08_pincer":
            sub_pos = min(total_samples - 1, pos + int(1.45 * sr))
            slam = make_sfx("impact_boom", sr=sr) * 0.65
            sub_end = min(total_samples, sub_pos + len(slam))
            mix[sub_pos:sub_end] += slam[: sub_end - sub_pos]

    # Soft-clip limiter & export stereo 16-bit WAV
    mix = np.tanh(mix * 1.08) * 0.92
    stereo = np.column_stack([mix, mix])
    wavfile.write(str(master_wav), sr, (stereo * 32767).astype(np.int16))

    timeline = {
        "id": spec["id"],
        "title": spec["title"],
        "fps": fps,
        "width": 1920,
        "height": 1080,
        "totalDurationSec": total_duration_sec,
        "totalFrames": total_frames,
        "audioSrc": "audio/master.wav",
        "beats": aligned_beats,
        "words": words,
    }
    out_json = DATA_DIR / "timeline.json"
    out_json.write_text(json.dumps(timeline, indent=2), encoding="utf-8")

    print(f"\n=== TIMELINE SUMMARY ({total_duration_sec:.2f}s / {total_frames} frames @ {fps}fps) ===")
    for ab in aligned_beats:
        print(
            f"  [{ab['index']:02d}] {ab['startSec']:5.2f}s -> {ab['endSec']:5.2f}s "
            f"({ab['durationSec']:4.2f}s | {ab['durationFrames']:2d}f) | {ab['archetype']:18s} | {ab['text']}"
        )


if __name__ == "__main__":
    main()
