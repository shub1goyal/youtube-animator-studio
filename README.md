# YouTube Animation Studio & Monetization Suite

> **An Antigravity AI plugin** for producing viral 2D historical animated YouTube videos — in the style of OverSimplified, History Matters, and Animated History.

[![Plugin Version](https://img.shields.io/badge/version-1.1.0-blue)](plugin.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎬 What This Plugin Does

A complete **end-to-end animated documentary production pipeline** that runs inside [Antigravity AI](https://antigravity.dev), giving you:

| Capability | Skill / Agent |
|---|---|
| 🎥 Full-length Hinglish historical documentary authoring | `youtube-history-animator` |
| 🖼️ 5-layer volumetric SVG scene generation | `svg-scene-cinematographer` (sidecar) |
| 🎵 Shot-by-shot storyboard, audio mastering & pacing | `storyboard-motion-director` |
| 📋 YouTube YPP / AdSense compliance auditing | `youtube-policy-monetization-guard` |
| 🚀 Automated YouTube upload with viral metadata & thumbnail | `youtube-viral-publisher` |
| 🎬 CTR thumbnail generation (OverSimplified style) | `thumbnail-vector-artist` (sidecar) |
| 💃 Whisper-aligned caption beat sheets | `kinetic-beat-choreographer` (sidecar) |

---

## 🗂️ Plugin Structure

```
youtube-animator-studio/
├── plugin.json                          # Plugin manifest
├── agents/
│   ├── svg-scene-cinematographer/       # Renders 5-layer SVG scenes
│   ├── kinetic-beat-choreographer/      # Whisper-aligned caption timing
│   └── thumbnail-vector-artist/         # YouTube CTR thumbnail generator
├── skills/
│   ├── youtube-history-animator/        # Main documentary production skill
│   ├── storyboard-motion-director/      # Shot pacing & audio mastering
│   ├── youtube-policy-monetization-guard/ # YPP compliance checker
│   └── youtube-viral-publisher/         # Upload + metadata automation
```

---

## 🚀 Quick Start

### 1. Install in Antigravity
Copy this folder to your Antigravity plugins directory:
```
~/.gemini/config/plugins/youtube-animator-studio/
```

### 2. Trigger a production
In Antigravity chat, type:
```
@[plugin:youtube-animator-studio] The Fall of the Mughal Empire — 20 minute Hinglish documentary
```

### 3. What happens automatically
1. **Script** — Viral Hinglish script with two-tier CTA written
2. **Sidecars dispatched** — One `svg-scene-cinematographer` per scene runs in parallel
3. **SVGs rendered** — 5-layer volumetric scenes (background, midground, character, FX, caption)
4. **Audio synced** — Gemini TTS (Charon voice) with Whisper word alignment
5. **MP4 rendered** — Playwright → FFmpeg deterministic pipeline
6. **Uploaded** — YouTube Data API v3 with viral title, thumbnail, chapters, pinned comment

---

## 🎨 Skills Detail

### `youtube-history-animator`
Main orchestration skill. Writes the full script, dispatches sidecar SVG cinematographers, manages the render pipeline, and coordinates the upload.

- **Style**: OverSimplified + History Matters + Animated History
- **Language**: Hinglish first (Conversational Romanized Hindi + English loanwords)
- **Format**: 16:9 1080p 25 FPS, long-form (10–25 min) or Shorts (60s)
- **CTA**: Two-tier — mid-roll subscribe pill + end-roll debate card

### `svg-scene-cinematographer`
Dedicated sidecar agent for generating a single scene's master SVG.

- 5-layer architecture: `bg` → `mg` → `char` → `fx` → `caption`
- 1920×1080 master canvas with dual-temperature lighting
- Procedural architectural patterns, rim-lit character rigs
- Outputs: `scene_N.svg` + `scene_N_movie.html` + `scene_N_shots.json`

### `storyboard-motion-director`
Calculates shot-by-shot pacing, easing curves, and audio mastering.

- Broadcast-compliant audio: −14 LUFS long-form, −12 LUFS Shorts
- Millisecond-accurate Whisper word-aligned beat sheets
- Camera choreography: zoom, pan, shake, letterbox

### `youtube-policy-monetization-guard`
Audits scripts and assets against YouTube Partner Program standards.

- Checks for demonetization triggers (violence, profanity, controversy)
- Verifies `containsSyntheticMedia` disclosure rules
- Ensures public domain / copyright safety for all assets

### `youtube-viral-publisher`
Automates the full YouTube upload flow.

- OAuth2 via YouTube Data API v3 (auto token refresh)
- A/B title generation, timestamped chapters, 500-char SEO tags
- Resumable chunked upload for large MP4s
- Auto thumbnail + pinned comment injection post-upload

---

## ⚙️ Requirements

- [Antigravity AI](https://antigravity.dev) (for plugin system)
- Python 3.10+
- `playwright` (`pip install playwright && playwright install chromium`)
- `ffmpeg` (bundled with Antigravity, or install separately)
- YouTube Data API v3 OAuth2 credentials (`client_secret_*.json`)
- Gemini API key (for TTS via `google-generativeai`)

---

## 🔐 Security

**Never commit secrets.** The `.gitignore` excludes:
- `*token*.json` — YouTube OAuth tokens
- `client_secret*.json` — Google API credentials
- `*.env` — Environment files

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Credits

Built with [Antigravity AI](https://antigravity.dev) · Inspired by OverSimplified, History Matters, Animated History · TTS by Google Gemini (Charon voice)
