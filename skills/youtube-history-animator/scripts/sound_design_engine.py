"""
engine_2d/sound_design_engine.py
Procedural Sound Design Engine for Cartoon & Documentary Animations.
Synthesizes custom sound effects (whooshes, rubber stamp thuds, coin chimes, tire screeches,
sad trombones, fireworks booms, oil gushers) and mixes them with the ambient score and voiceover.
"""

import os
import math
import numpy as np
from scipy.io import wavfile

SR = 44100
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SFX_DIR = os.path.join(SCRIPT_DIR, "sfx")
BASE_DIR = os.path.join(os.getcwd(), "production")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

os.makedirs(SFX_DIR, exist_ok=True)


def gen_whoosh(dur=0.35):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * (t / dur)) ** 2.2
    sweep = np.sin(2 * np.pi * (250 + 2200 * (t / dur)) * t)
    return (noise * 0.35 + sweep * 0.65) * env * 0.7


def gen_stamp_thud(dur=0.3):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    punch = np.sin(2 * np.pi * 85 * t) * np.exp(-16 * t)
    sub = np.sin(2 * np.pi * 45 * t) * np.exp(-8 * t)
    click = np.random.uniform(-1, 1, len(t)) * np.exp(-120 * t)
    return (punch * 0.6 + sub * 0.5 + click * 0.3) * 0.9


def gen_coin_chime(dur=0.5):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    # Bright harmonics
    chime = (
        0.5 * np.sin(2 * np.pi * 2637 * t) +
        0.3 * np.sin(2 * np.pi * 3136 * t) +
        0.2 * np.sin(2 * np.pi * 3951 * t)
    ) * np.exp(-7 * t)
    return chime * 0.65


def gen_cha_ching(dur=0.6):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    lever = np.sin(2 * np.pi * 880 * t) * np.exp(-60 * t)
    # Ring bell
    bell1 = np.sin(2 * np.pi * 3520 * t) * np.exp(-8 * t)
    bell2 = np.sin(2 * np.pi * 4186 * t) * np.exp(-7 * t)
    return (lever * 0.4 + bell1 * 0.5 + bell2 * 0.4) * 0.8


def gen_tire_screech(dur=0.8):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    # Friction whine
    mod = np.sin(2 * np.pi * 18 * t)
    screech = np.sin(2 * np.pi * (1200 + 400 * mod) * t)
    env = np.sin(np.pi * (t / dur)) ** 1.8
    return (screech * 0.6 + noise * 0.4) * env * 0.55


def gen_sad_trombone(dur=1.4):
    """Classic cartoon wa-wa-waaa descending slide."""
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    audio = np.zeros(len(t))
    # 4 notes: D3 (146.8) -> Db3 (138.6) -> C3 (130.8) -> B2 (123.5) with vibrato
    notes = [(0.0, 0.3, 146.8), (0.3, 0.6, 138.6), (0.6, 0.9, 130.8), (0.9, 1.4, 123.5)]
    for start, end, freq in notes:
        s_idx, e_idx = int(start * SR), int(end * SR)
        seg_t = t[s_idx:e_idx] - start
        seg_dur = end - start
        env = np.sin(np.pi * (seg_t / seg_dur)) ** 1.2
        vib = 1.0 + 0.03 * np.sin(2 * np.pi * 5.0 * seg_t)
        # Brass buzz (harmonics)
        wave = (
            np.sin(2 * np.pi * freq * vib * seg_t) +
            0.5 * np.sin(4 * np.pi * freq * vib * seg_t) +
            0.25 * np.sin(6 * np.pi * freq * vib * seg_t)
        )
        audio[s_idx:e_idx] += wave * env * 0.45
    return audio


def gen_fireworks_boom(dur=1.2):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    sub_thud = np.sin(2 * np.pi * 55 * t) * np.exp(-5 * t)
    crackle = np.random.uniform(-1, 1, len(t)) * np.exp(-3 * t) * (np.sin(2 * np.pi * 40 * t) > 0.6)
    return (sub_thud * 0.7 + crackle * 0.4) * 0.85


def gen_oil_gush(dur=1.5):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    surge = (np.sin(np.pi * (t / dur)) ** 1.5) * (0.8 + 0.2 * np.sin(2 * np.pi * 8 * t))
    return noise * surge * 0.45


def synthesize_all_sfx():
    """Generates individual SFX WAV files."""
    sfx_map = {
        "whoosh.wav": gen_whoosh(),
        "stamp_thud.wav": gen_stamp_thud(),
        "coin_chime.wav": gen_coin_chime(),
        "cha_ching.wav": gen_cha_ching(),
        "tire_screech.wav": gen_tire_screech(),
        "sad_trombone.wav": gen_sad_trombone(),
        "fireworks_boom.wav": gen_fireworks_boom(),
        "oil_gush.wav": gen_oil_gush()
    }
    for fname, data in sfx_map.items():
        p = os.path.join(SFX_DIR, fname)
        wavfile.write(p, SR, (data * 32767).astype(np.int16))
    print(f"Generated {len(sfx_map)} sound effect assets in {SFX_DIR}")


def build_mixed_soundtrack(total_duration, output_wav):
    """Mixes voiceover, ambient score, and timed SFX cues into one broadcast-ready stereo master."""
    n_samples = int(SR * total_duration)
    left_mix = np.zeros(n_samples, dtype=np.float32)
    right_mix = np.zeros(n_samples, dtype=np.float32)

    # 1. Overlay SFX cues at exact chronological scene beats
    # Timings based on script cue timestamps:
    sfx_events = [
        # Scene 1
        (0.0, gen_whoosh(), 0.5),
        (4.2, gen_tire_screech(), 0.6),
        (5.5, gen_cha_ching(), 0.7),
        # Scene 2
        (13.76, gen_whoosh(), 0.5),
        (16.5, gen_coin_chime(), 0.6),
        # Scene 3
        (24.76, gen_whoosh(), 0.5),
        (27.0, gen_stamp_thud(), 0.8),
        (27.3, gen_sad_trombone(), 0.7),
        # Scene 4
        (34.52, gen_whoosh(), 0.5),
        (36.2, gen_stamp_thud(), 0.8),
        # Scene 5 (Oil & Coins)
        (43.80, gen_whoosh(), 0.5),
        (45.5, gen_oil_gush(), 0.6),
        (47.5, gen_cha_ching(), 0.75),
        (48.0, gen_coin_chime(), 0.6),
        (48.5, gen_coin_chime(), 0.6),
        (49.0, gen_coin_chime(), 0.6),
        # Scene 6
        (56.88, gen_whoosh(), 0.5),
        (58.8, gen_stamp_thud(), 0.7),
        # Scene 7 (Union & Fireworks)
        (68.96, gen_whoosh(), 0.5),
        (70.2, gen_stamp_thud(), 0.8),
        (71.0, gen_fireworks_boom(), 0.8),
        (73.5, gen_fireworks_boom(), 0.8),
        # Scene 8
        (79.60, gen_whoosh(), 0.5),
        (81.2, gen_stamp_thud(), 0.75),
        # Scene 9
        (90.64, gen_whoosh(), 0.5),
        (92.5, gen_stamp_thud(), 0.75),
        # Scene 10
        (101.20, gen_whoosh(), 0.5),
        (102.8, gen_stamp_thud(), 0.7),
        # Scene 11 (Finale)
        (110.48, gen_whoosh(), 0.5),
        (112.0, gen_fireworks_boom(), 0.8),
        (114.5, gen_fireworks_boom(), 0.8),
        (116.0, gen_cha_ching(), 0.8)
    ]

    for start_t, sfx_data, vol in sfx_events:
        idx = int(start_t * SR)
        dur_samples = len(sfx_data)
        if idx < n_samples:
            end_idx = min(idx + dur_samples, n_samples)
            actual_len = end_idx - idx
            left_mix[idx:end_idx] += sfx_data[:actual_len] * vol
            right_mix[idx:end_idx] += sfx_data[:actual_len] * vol

    # 2. Add Warm Ambient Pad Soundtrack underneath (-20 dB)
    t = np.linspace(0, total_duration, n_samples, endpoint=False)
    pad = (
        0.5 * np.sin(2 * np.pi * 146.83 * t) +
        0.3 * np.sin(2 * np.pi * 220.00 * t) +
        0.2 * np.sin(2 * np.pi * 261.63 * t)
    ) * 0.08
    left_mix += pad
    right_mix += pad

    # Scale to prevent clipping
    max_val = max(np.max(np.abs(left_mix)), np.max(np.abs(right_mix)), 1e-4)
    if max_val > 0.85:
        left_mix = left_mix * (0.85 / max_val)
        right_mix = right_mix * (0.85 / max_val)

    stereo_sfx = np.column_stack([
        (left_mix * 32767).astype(np.int16),
        (right_mix * 32767).astype(np.int16)
    ])
    wavfile.write(output_wav, SR, stereo_sfx)
    print(f"Master Sound Design Bed Written: {output_wav}")


class SoundDesignEngine:
    def __init__(self, sfx_dir=None):
        self.sfx_dir = sfx_dir or SFX_DIR

    def generate_complete_soundtrack(self, total_duration, output_wav):
        build_mixed_soundtrack(total_duration, output_wav)


if __name__ == "__main__":
    synthesize_all_sfx()
    build_mixed_soundtrack(118.68, os.path.join(AUDIO_DIR, "sound_design_bed.wav"))

