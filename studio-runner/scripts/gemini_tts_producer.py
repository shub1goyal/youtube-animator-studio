#!/usr/bin/env python3
"""
gemini_tts_producer.py — Production-Grade Gemini 3.8 Flash TTS Engine.
- Voice: hi-in-podcaster-2 (Finalized charismatic Hindi/Hinglish storyteller)
- Model: gemini-3.8-flash-tts
- Handles API key round-robin across cleaned api_keys.json
- Automatically runs local faster-whisper word-level alignment
- Synthesizes procedural Foley SFX & ambient tension drone
- Exports master.wav + src/data/timeline.json for Remotion
"""
import base64
import itertools
import json
import math
import os
import re
import subprocess
import threading
import urllib.request
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

ROOT = Path(__file__).resolve().parent.parent
KEYS_FILE = ROOT / "api_keys.json"
SCRIPT_PATH = ROOT / "episode_script.json"
AUDIO_DIR = ROOT / "public" / "audio"
DATA_DIR = ROOT / "src" / "data"
FFMPEG = r"C:\Users\shubh\AppData\Local\agy\bin\ffmpeg.exe"

VOICE_ID = "hi-in-podcaster-2"
MODEL_ID = "gemini-3.8-flash-tts"
DEFAULT_STYLE = (
    "energetic, witty Indian podcast storyteller, sharp Hinglish conversational pacing, "
    "confident natural cadence, crisp studio mic presence"
)


class KeyPool:
    def __init__(self):
        self._lock = threading.Lock()
        raw = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
        self.keys = raw if isinstance(raw, list) else raw.get("gemini_api_keys", [])
        self._cycle = itertools.cycle(self.keys) if self.keys else None

    def get_key(self) -> str:
        with self._lock:
            return next(self._cycle) if self._cycle else os.environ.get("GEMINI_API_KEY", "")


KEY_POOL = KeyPool()


def synthesize_gemini_tts(text: str, voice: str = VOICE_ID, style: str = DEFAULT_STYLE) -> bytes:
    """Invokes gemini-3.8-flash-tts via Google GenAI Interactions API with automatic retry on 429 across key pool."""
    url = "https://generativelanguage.googleapis.com/v1beta/interactions"
    payload = {
        "model": MODEL_ID,
        "input": [
            {
                "type": "user_input",
                "content": [
                    {
                        "type": "text",
                        "text": text,
                        "annotations": [{"type": "speech_metadata", "style": style}],
                    }
                ],
            }
        ],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": voice}]},
    }

    last_err = None
    for attempt in range(len(KEY_POOL.keys)):
        key = KEY_POOL.get_key()
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-goog-api-key": key},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=35) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                b64_audio = data["steps"][0]["content"][0]["data"]
                return base64.b64decode(b64_audio)
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429:
                print(f"Key rate-limited (HTTP 429). Rotating to next key (attempt {attempt+1}/{len(KEY_POOL.keys)})...")
                continue
            raise
        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(f"All keys rate-limited or failed. Last error: {last_err}")


def align_with_faster_whisper(wav_path: Path):
    """Generates precise 10ms word-level timestamps using faster-whisper."""
    from faster_whisper import WhisperModel

    print("Running faster-whisper word alignment...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(wav_path), word_timestamps=True)
    words = []
    for seg in segments:
        for w in seg.words:
            clean = re.sub(r"[^\w\s]", "", w.word.strip().lower())
            if clean:
                words.append({
                    "text": w.word.strip(),
                    "norm": clean,
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                })
    return words


def make_sfx(kind: str, sr: int = 44100) -> np.ndarray:
    """Editorial motion-design SFX synthesized in NumPy/SciPy."""
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

    dur = 1.2
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    sig = (
        np.sin(2 * np.pi * 220.0 * t) * 0.5
        + np.sin(2 * np.pi * 329.63 * t) * 0.35
        + np.sin(2 * np.pi * 440.0 * t) * 0.2
    ) * np.exp(-t * 2.6)
    return sig * 0.20


def build_ambient_bed(total_samples: int, sr: int = 44100) -> np.ndarray:
    """Subtle documentary tension pad + heartbeat pulse (-25dB)."""
    t = np.arange(total_samples) / sr
    lfo = 0.65 + 0.35 * np.sin(2 * np.pi * 0.22 * t)
    pad = (
        np.sin(2 * np.pi * 55.0 * t) * 0.55
        + np.sin(2 * np.pi * 82.41 * t) * 0.30
        + np.sin(2 * np.pi * 110.0 * t) * 0.15
    ) * lfo
    pulse = np.sin(2 * np.pi * 62.0 * np.mod(t, 0.625)) * np.exp(-np.mod(t, 0.625) * 18.0) * 0.45
    bed = (pad * 0.032) + (pulse * 0.028)
    fade_in = np.minimum(t / 0.4, 1.0)
    fade_out = np.minimum((t[-1] - t) / 1.2, 1.0)
    return bed * fade_in * fade_out


def produce_episode():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    spec = json.loads(SCRIPT_PATH.read_text(encoding="utf-8"))
    fps = spec.get("fps", 30)
    beats_spec = spec["beats"]

    # Combine text with subtle micro-pauses between sentences
    full_text = " ".join(b["text"] for b in beats_spec)

    raw_wav = AUDIO_DIR / "gemini_vo_raw.wav"
    master_wav = AUDIO_DIR / "master.wav"

    print(f"Calling Gemini 3.8 Flash TTS [Voice: {VOICE_ID}]...")
    wav_bytes = synthesize_gemini_tts(full_text, voice=VOICE_ID)
    raw_wav.write_bytes(wav_bytes)
    print(f"Synthesized {len(wav_bytes)} bytes of studio WAV.")

    # Convert to 44.1kHz mono for Remotion mixing
    clean_wav = AUDIO_DIR / "gemini_vo_44k.wav"
    subprocess.run(
        [FFMPEG, "-y", "-i", str(raw_wav), "-ac", "1", "-ar", "44100", str(clean_wav)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    sr, vo_pcm = wavfile.read(str(clean_wav))
    vo = vo_pcm.astype(np.float32) / 32768.0

    # Extract word timestamps via faster-whisper
    words = align_with_faster_whisper(clean_wav)
    print(f"Whisper mapped {len(words)} words.")

    tail_sec = 0.85
    total_samples = len(vo) + int(sr * tail_sec)
    total_duration_sec = round(total_samples / sr, 3)
    total_frames = int(math.ceil(total_duration_sec * fps))

    # Match each beat to word timestamps
    word_cursor = 0
    aligned_beats = []
    for idx, b in enumerate(beats_spec):
        raw_tokens = [re.sub(r"[^\w\s]", "", t.lower()) for t in b["text"].split() if t.strip()]
        start_w = word_cursor
        matched = 0
        while word_cursor < len(words) and matched < len(raw_tokens):
            w_norm = words[word_cursor]["norm"]
            t_norm = raw_tokens[matched]
            if w_norm == t_norm or w_norm in t_norm or t_norm in w_norm:
                matched += 1
                word_cursor += 1
            else:
                matched += 1
                word_cursor += 1

        end_w = max(start_w, word_cursor - 1)
        start_sec = 0.0 if idx == 0 else words[start_w]["start"]
        aligned_beats.append({
            "index": idx,
            "id": b["id"],
            "archetype": b["archetype"],
            "chapter": b.get("chapter", "DOCUMENTARY"),
            "sfx": b.get("sfx", "whoosh_soft"),
            "text": b["text"],
            "startSec": round(start_sec, 3),
            "wordStartIdx": start_w,
            "wordEndIdx": end_w,
        })

    # Seamless tiling: visual leads audio by 40ms for snappy sync
    for idx, ab in enumerate(aligned_beats):
        if idx + 1 < len(aligned_beats):
            next_start = max(ab["startSec"] + 0.5, aligned_beats[idx + 1]["startSec"] - 0.04)
            aligned_beats[idx + 1]["startSec"] = round(next_start, 3)
            ab["endSec"] = round(next_start, 3)
        else:
            ab["endSec"] = total_duration_sec

        ab["durationSec"] = round(ab["endSec"] - ab["startSec"], 3)
        ab["startFrame"] = int(round(ab["startSec"] * fps))
        ab["endFrame"] = total_frames if idx == len(aligned_beats) - 1 else int(round(ab["endSec"] * fps))
        ab["durationFrames"] = max(1, ab["endFrame"] - ab["startFrame"])

    # Sound design mix: VO + Ambient tension bed + Foley hits
    mix = np.zeros(total_samples, dtype=np.float32)
    vo_peak = np.max(np.abs(vo)) or 1.0
    mix[: len(vo)] += (vo / vo_peak) * 0.88
    mix += build_ambient_bed(total_samples, sr)

    for ab in aligned_beats:
        sfx_wave = make_sfx(ab["sfx"], sr=sr)
        pos = max(0, int(ab["startSec"] * sr))
        end_pos = min(total_samples, pos + len(sfx_wave))
        if end_pos > pos:
            mix[pos:end_pos] += sfx_wave[: end_pos - pos]

    mix = np.tanh(mix * 1.06) * 0.92
    stereo = np.column_stack([mix, mix])
    wavfile.write(str(master_wav), sr, (stereo * 32767).astype(np.int16))

    timeline = {
        "id": spec.get("id", "documentary"),
        "title": spec.get("title", "Documentary"),
        "voice": VOICE_ID,
        "fps": fps,
        "width": 1920,
        "height": 1080,
        "totalDurationSec": total_duration_sec,
        "totalFrames": total_frames,
        "audioSrc": "audio/master.wav",
        "beats": aligned_beats,
        "words": words,
    }
    (DATA_DIR / "timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    print(f"\nTimeline generated: {total_duration_sec}s ({total_frames} frames).")
    for ab in aligned_beats:
        print(f"  [{ab['index']:02d}] {ab['startSec']:5.2f}s -> {ab['endSec']:5.2f}s ({ab['durationSec']:4.2f}s) | {ab['archetype']}")


if __name__ == "__main__":
    produce_episode()
