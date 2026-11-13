# 🎬 YouTube Animator Studio & Motion Engine

Production suite and global skill bundles for **Google Antigravity AI** and **Remotion**, specialized in high-retention faceless animated explainers, documentary stickman cartoons (*OverSimplified* style), kinetic typography, Vox-style tactical maps, and Hinglish audio synthesis via `gemini-3.8-flash-tts`.

---

## 📦 Installed Skill Bundles (34 Skills Across 4 Plugins)

This repository houses the global production skills and ready-to-run Remotion video generator:

### 1. `motion-skills-pack` (19 Skills)
- **`map-animation`**: Vox-style 2D/3D map camera animations, GeoJSON vector boundaries, route tracing, and pins.
- **`kinetic-typography`**: Per-character/word reveals, dynamic text effects, and subtitle styling.
- **`animation-principles`**: Easing curves, spring physics, anticipation, and graph editor presets.
- **`beat-sync-editing`**: Sound-to-cut synchronization, rhythm editing, match cuts, and speed ramping.
- **`chart-animation`**: Bar chart races, CSV data visualizations, and animated counter tickers.
- **`color-motion`**: Perceptual interpolation (OKLCH/Lab), gradient shaders, and video color grading.
- **`isometric-animation`**: 2.5D isometric scenes, exploded diagram builds, and Three.js camera drifts.
- **`whiteboard-animation`**: SVG hand-drawn scribbles, stroke draw-on reveals, and marker wipes.
- **`diagram-animation`**, **`explainer-video`**, **`logo-animation`**, **`motion-art-direction`**, **`motion-background`**, **`presentation-video`**, **`remotion-video`**, **`shot-composition`**, **`wrapped-video`**, **`after-effects`**, **`animated-infographic`**.

### 2. `remotion-toolkit` (13 Skills)
- **`remotion-best-practices`**, **`remotion-captions`**, **`remotion-create`**, **`remotion-docs`**, **`remotion-interactivity`**, **`remotion-license`**, **`remotion-maps`**, **`remotion-markup`**, **`remotion-multimedia`**, **`remotion-render`**, **`remotion-saas`**, **`remotion-studio`**, **`remotion-upgrade`**.

### 3. `video-shotcraft` (1 Skill)
- **`video-shotcraft`**: Ink Press 2.5D cinematic system, real page captures, shot cards, SFX candidate search and beat alignment.

### 4. `video-talkcraft` (1 Skill)
- **`video-talkcraft`**: Spoken explainer video engine with 108 motion recipe cards, word-level timestamp alignment, continuous camera tracking, and Apple-standard motion restraint.

---

## 🚀 Studio Runner (`studio-runner/`)

Contains the end-to-end Pure Code Stickman Explainer video pipeline:
- **TTS Engine**: `gemini-3.8-flash-tts` (`hi-in-podcaster-2` voice profile) for Indian Hinglish cadence.
- **Vector Rig**: Custom React SVG stickman actor with line-boil filter (`<feTurbulence>`), dynamic costumes, facial expressions, and asymmetric poses.
- **100% Deterministic Code**: Built with Remotion, RoughJS, and Iconify. Zero generative AI images.

### Quick Start

```bash
# 1. Install dependencies
cd studio-runner
npm install

# 2. Add Gemini API keys to api_keys.json (gitignored)
cp ../api_keys.example.json ../api_keys.json

# 3. Synthesize Hinglish Voiceover
python scripts/gemini_tts_producer.py

# 4. Preview in Remotion Studio
npx remotion preview

# 5. Render Video
npx remotion render src/index.ts CannaeProof out/stickman_hinglish_30s.mp4
```

---

## 🏛️ Directory Layout

```
├── plugins/                     # Plugin manifests and bundled skills
│   ├── motion-skills-pack/      # 19 motion skills
│   ├── remotion-toolkit/        # 13 remotion skills
│   ├── video-shotcraft/         # Ink Press 2.5D camera skill
│   └── video-talkcraft/         # 108 motion recipe cards
├── skills/                      # All 34 skills unbundled for direct CLI discovery
├── studio-runner/               # Remotion React project & Stickman animation engine
├── api_keys.example.json        # Template for Gemini TTS keys
└── .gitignore                   # Ignores build artifacts and credentials
```

---

## 📄 License

MIT
