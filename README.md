# 🎬 YouTube Animation Studio & Monetization Suite

> **Broadcast-Grade 2.5D Vector Movie Engine & Viral Production Suite for Antigravity AI**  
> Produces high-retention 1080p 25 FPS animated historical and educational documentaries in the iconic style of **OverSimplified**, **History Matters**, and **Johnny Harris** with Conversational Hinglish narration, 5-layer volumetric staging, Whisper forced alignment, and YouTube Partner Program (YPP) monetization compliance.

[![Plugin Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](plugin.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)]()
[![Platform: Cross--Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

---

## 🏛️ Unified Architecture Overview

```
                                  [ Topic Request ]
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    1. Viral Hinglish Script Engine    │
                      │       (ai_script_generator.py)        │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    2. AdSense & YPP Compliance Guard  │
                      │        (compliance_checker.py)        │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │     3. Gemini 3.8 Flash TTS Engine    │
                      │    (Voice: Charon, Key Pool Rotate)   │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    4. Whisper Word Forced Alignment   │
                      │      (whisper_aligner.py 10ms sync)   │
                      └───────────────────┬───────────────────┘
                                          │
                    ┌─────────────────────┴─────────────────────┐
                    ▼                                           ▼
      ┌───────────────────────────┐               ┌───────────────────────────┐
      │   Sidecar Agent:          │               │   Sidecar Agent:          │
      │   kinetic-beat-choreographer│             │   svg-scene-cinematographer│
      │   (Action beat sheets,    │               │   (5-Layer volumetric     │
      │    asymmetric staging,    │               │    1920x1080 SVGs &       │
      │    MapLore alert badges)  │               │    scene_X_movie.html)    │
      └─────────────┬─────────────┘               └─────────────┬─────────────┘
                    │                                           │
                    └─────────────────────┬─────────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    5. Pre-Render Synchronization Gate │
                      │        (audit_subtitle_sync.py)       │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │   6. Deterministic 2.5D Movie Renderer│
                      │      (kinetic_video_renderer.py)      │
                      │   - Playwright window.seekToTime(t)   │
                      │   - Dynamic viewBox camera pan/zoom   │
                      │   - Direct JPEG pipe to FFmpeg        │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │  7. Audio Mastering & Packaging       │
                      │     - EBU R128 (-14 LUFS Long-Form)   │
                      │     - High-CTR OverSimplified Thumb   │
                      │     - YouTube Upload & Pinned Comment │
                      └───────────────────────────────────────┘
```

---

## 📁 Repository Directory Structure

```
youtube-animator-studio/
├── plugin.json                              # Antigravity plugin manifest
├── README.md                                # Comprehensive studio documentation
├── LICENSE                                  # MIT License
├── .gitignore                               # Strict security & credential exclusion rules
├── api_keys.example.json                    # Clean template for API keys
│
├── agents/                                  # Dedicated Antigravity Sidecar Agents
│   ├── kinetic-beat-choreographer.md        # Sidecar wrapper reference
│   ├── kinetic-beat-choreographer/
│   │   └── agent.md                         # Whisper beat-sheet timing & action choreography
│   ├── svg-scene-cinematographer.md         # Sidecar wrapper reference
│   ├── svg-scene-cinematographer/
│   │   └── agent.md                         # 5-Layer volumetric SVG scene illustration
│   ├── thumbnail-vector-artist.md           # Sidecar wrapper reference
│   └── thumbnail-vector-artist/
│       └── agent.md                         # High-CTR OverSimplified thumbnail engineering
│
└── skills/                                  # Domain Skills & Execution Engines
    ├── youtube-history-animator/            # Master Documentary Orchestration Suite
    │   ├── SKILL.md                         # Complete production specification & rules
    │   ├── references/                      # Deep Technical Knowledge Bibles
    │   │   ├── cinematic_svg_mastery.md     # 5-Layer volumetric SVG visual craftsmanship
    │   │   ├── hinglish_phonetics_guide.md  # Charon TTS phonetics & loanword dictionary
    │   │   ├── viral_scripting_framework.md # Two-tier CTA, pacing & humor architecture
    │   │   ├── animation_pipeline.md        # Technical compositing & render contract
    │   │   └── ai_voice_monetization_guide.md# YPP synthetic media defense guidelines
    │   └── scripts/                         # Executable Python Modules
    │       ├── config.py                    # Cross-platform binary & API key loader
    │       ├── ai_script_generator.py       # Hierarchical multi-act script generator
    │       ├── gemini_tts_engine.py         # Gemini 3.8 Flash TTS with key pool rotation
    │       ├── whisper_aligner.py           # Faster-Whisper forced word aligner
    │       ├── audit_subtitle_sync.py       # Pre-render subtitle synchronization gate
    │       ├── beat_sheet_generator.py      # Topic-agnostic kinetic beat sheet builder
    │       ├── character_rig_generator.py   # Monolithic 320x440 OverSimplified rigs
    │       ├── cinematic_svg_engine.py      # 5-Layer volumetric SVG & movie HTML builder
    │       ├── kinetic_video_renderer.py    # Deterministic Playwright-to-FFmpeg renderer
    │       ├── full_auto_producer.py        # End-to-end full auto episode pipeline
    │       ├── autonomous_studio.py         # Autonomous production orchestrator
    │       ├── sound_design_engine.py       # Procedural SFX & cartoon whoosh synthesizer
    │       ├── map_svg_generator.py         # MapLore animated vector cartography
    │       └── asset_library.py             # Vector sprite & prop management
    │
    ├── storyboard-motion-director/          # Motion Pacing & Audio Mastering
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── ctr_thumbnail_mastery.md     # Packaging & visual psychology formulas
    │   │   └── motion_easing_formulas.md    # Spring overshoot & cubic Bezier curves
    │   └── scripts/
    │       ├── audio_mastering_helper.py    # EBU R128 loudness normalizer (-14 / -12 LUFS)
    │       ├── pacing_analyzer.py           # Shot duration audit (2.5–4.5s sweet spot)
    │       └── cinematic_video_assembler.py # Multi-shot camera choreography & ASS subtitles
    │
    ├── youtube-policy-monetization-guard/   # Compliance & YPP Safety
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── advertiser_friendly_rules.md # Green dollar advertiser guidelines
    │   │   ├── reused_content_defense.md    # Original commentary & copyright protection
    │   │   └── public_domain_asset_sources.md
    │   └── scripts/
    │       └── compliance_checker.py        # Automated script demonetization audit
    │
    └── youtube-viral-publisher/             # YouTube Publishing Automation
        ├── SKILL.md
        └── scripts/
            ├── publish_to_youtube.py        # Automated publishing with A/B variant titles
            ├── youtube_auth.py              # OAuth2 authentication & token auto-refresh
            ├── youtube_uploader.py          # Resumable chunked 1080p video uploader
            ├── viral_metadata_engine.py     # SEO tags, chapters & description generator
            └── viral_thumbnail_generator.py # Automated high-CTR thumbnail compositor
```

---

## ⚡ Environment Setup & Cross-Platform Portability

### 1. System Dependencies
- **Python 3.10+**
- **FFmpeg**: Automatically detected in system `PATH`, local Antigravity runtime, Homebrew, Chocolatey, or via `FFMPEG_PATH`.
- **Google Chrome / Chromium**: Automatically detected cross-platform or via `CHROME_PATH`.

### 2. Python Package Installation
```bash
pip install playwright faster-whisper pillow opencv-python numpy scipy google-generativeai
playwright install chromium
```

### 3. API Key Configuration
Provide Gemini API keys using any of these methods (checked automatically in priority order):
1. **Environment Variable**:
   ```bash
   export GEMINI_API_KEY="AIzaSyYourKey1,AIzaSyYourKey2"
   ```
2. **Local Config File** (gitignored):
   Copy `api_keys.example.json` to `api_keys.json`:
   ```json
   {
     "gemini_api_keys": [
       "YOUR_GEMINI_API_KEY_1",
       "YOUR_GEMINI_API_KEY_2"
     ]
   }
   ```

---

## 🛠️ CLI Usage Examples

### 1. Full-Auto 60-Second YouTube Short
Generates Hinglish script, checks YPP compliance, synthesizes Charon TTS, aligns Whisper words, renders 9:16 vertical MP4, and masters audio to `-12.0 LUFS`:
```bash
py skills/youtube-history-animator/scripts/full_auto_producer.py \
  --topic "How America Bought Louisiana for $15M" \
  --format shorts \
  --lang hinglish \
  --out louisiana_short
```

### 2. Full-Auto 12-Minute Long-Form Documentary
```bash
py skills/youtube-history-animator/scripts/full_auto_producer.py \
  --topic "The Fall of the Mughal Empire" \
  --format long_form \
  --mins 12 \
  --lang hinglish \
  --out mughal_empire_doc
```

### 3. Standalone 5-Layer Volumetric SVG & Deterministic Movie HTML
Generate master vector scenes across the 6 historical presets (`ww2_cellar_resistance`, `victorian_treaty_chamber`, `great_depression_stock_crash`, `desert_oil_strike_1958`, `bedouin_campfire_night`, `cold_war_bunker`):
```bash
py skills/youtube-history-animator/scripts/cinematic_svg_engine.py \
  --scene "ww2_cellar_resistance" \
  --out "scene_cellar.svg" \
  --html "scene_cellar_movie.html" \
  --rasterize "scene_cellar.png"
```

### 4. OverSimplified Character Rig Generator
Generate monolithic `320x440` vector rigs with asymmetric arm poses, custom headdresses, props, and environmental rim lighting:
```bash
# Resistance Fighter listening to radio
py skills/youtube-history-animator/scripts/character_rig_generator.py \
  --name "resistance_fighter" \
  --expression "intense_dread" \
  --pose "ear_listening" \
  --hat "military_cap" \
  --rim-color "#f59e0b" \
  --rim-side "right" \
  --out "fighter.svg"

# Victorian Diplomat with treaty scroll
py skills/youtube-history-animator/scripts/character_rig_generator.py \
  --name "viceroy" \
  --expression "smug" \
  --pose "pointing_up_board" \
  --hat "powdered_wig" \
  --prop "treaty_scroll" \
  --out "viceroy.svg"
```

### 5. Deterministic Playwright-to-FFmpeg Frame Renderer
Executes deterministic frame-stepping via `window.seekToTime(t)` directly streaming JPEG buffers to FFmpeg:
```bash
py skills/youtube-history-animator/scripts/kinetic_video_renderer.py \
  --prod-dir "productions/my_episode" \
  --fps 25 \
  --workers 4
```

### 6. Pre-Render Subtitle Synchronization Audit
Verifies that shot durations are bound to Whisper sentence speech boundaries with `< 100ms` offset:
```bash
py skills/youtube-history-animator/scripts/audit_subtitle_sync.py \
  --prod-dir "productions/my_episode"
```

### 7. Audio Mastering & Pacing Analysis
Master scene audio to broadcast loudness standards and verify cut frequency:
```bash
# Broadcast Audio Loudness Normalization (-14 LUFS Long-Form)
py skills/storyboard-motion-director/scripts/audio_mastering_helper.py \
  --input raw_voice.wav \
  --output mastered_voice.wav \
  --target-lufs -14.0

# Pacing Sweet-Spot Audit (Flags cuts > 6.0s or < 1.8s)
py skills/storyboard-motion-director/scripts/pacing_analyzer.py \
  --video episode_master.mp4
```

---

## 🔐 Security & Governance

- **Zero Hardcoded Secrets**: All API keys are loaded strictly from environment variables or gitignored configuration files.
- **Excluded Files**: `.gitignore` strictly rejects all `*token*.json`, `*secret*.json`, `client_secret*.json`, and `api_keys.json` files.
- **YouTube Synthetic Media Policy Compliance**: OverSimplified 2D cartoon animation is explicitly exempt from synthetic media disclosures (`containsSyntheticMedia: false`).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
