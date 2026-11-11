---
name: storyboard-motion-director
description: >-
  Technical director for shot-by-shot storyboarding, camera choreography, motion kinetics, pacing analysis, audio mastering, and CTR thumbnail engineering for animated YouTube channels. Use this skill to calculate pacing metrics, generate broadcast-compliant audio filters (-14 LUFS long-form, -12 LUFS shorts), design easing curves, and optimize packaging.
---

# Storyboard & Motion Director

This skill provides technical and motion-design direction for animated YouTube creators. It optimizes video pacing, motion easing, broadcast audio normalization, and click-through rate (CTR) packaging.

---

## 1. Quick Workflow Routing

- **Analyze Video Pacing & Retention Danger Zones**:
  `python scripts/pacing_analyzer.py <video_path> [--threshold 0.2]`
- **Master Audio to Broadcast Standards (-14 LUFS / -12 LUFS)**:
  `python scripts/audio_mastering_helper.py <input_video_or_audio> --mode [long_form|shorts] --out <output_path>`
- **Motion Easing Formulas & After Effects Expressions**:
  Review [Motion Easing Formulas](./references/motion_easing_formulas.md).
- **CTR Thumbnail & Title Engineering**:
  Review [Thumbnail & CTR Blueprint](./references/ctr_thumbnail_mastery.md).

---

## 2. Pacing Guidelines & Word-to-Duration Formula

- **Content Language Mandate**: All speech velocity calculations, script structures, and kinetic typography pacing are engineered **Hinglish-First** (conversational Romanized Hindi with punchy English loanwords, e.g. *"Bhai socho...", "Lafda shuru hua...", "Game poora palat gaya!"*).
- **Calibrated Speech Pace (Gemini 3.8 Flash Neural TTS - Charon)**:
  - **Overall Pacing Rate**: **158.4 WPM** (Words Per Minute)
  - **Speech Velocity**: **2.64 Words / Second**
  - **Time Cost per Word**: **0.379 Seconds / Word**
- **Word-Count-to-Runtime Planning Table**:
  - **10 Minutes (600s)**: Target **1,580 – 1,600 spoken words**
  - **12 Minutes (720s)**: Target **1,880 – 1,920 spoken words**
  - **15 Minutes (900s)**: Target **2,350 – 2,400 spoken words**
  - Formula: $\text{Duration (seconds)} = \text{Word Count} \times 0.3788 = \frac{\text{Word Count}}{2.64}$
- **Non-Repetitive Narrative Progression (5-Act Structure)**:
  - Act 1 (15%): Shocking Status Quo & Primitive Baseline (zero repetition of final outcome).
  - Act 2 (20%): Sudden Catastrophic Disruption (industry collapse, starvation/existential threat).
  - Act 3 (25%): Multi-Polar Geopolitical Chess & Failed Attempts (treaties, wars, rivalries).
  - Act 4 (25%): Breakthrough Discovery & Visionary Alliance (oil/wealth pivot, risky unification).
  - Act 5 (15%): High-Tech Future & Enduring Moral Lesson (space exploration, AI, beyond resources).
  - **Rule of No Backtracking**: Once a historical conflict or concept is resolved, it must NEVER be re-explained or looped back in later scenes.
- **YouTube Shorts (9:16)**:
  - Target cut / camera pan frequency: Every 2.5 to 3.5 seconds.
  - Zero static spans greater than 5 seconds.
  - Word count: 140 – 160 words (55s – 60s runtime).
  - Kinetic typography synced to spoken syllables.
- **Long-Form Documentaries (16:9)**:
  - Target cut frequency: Every 6.0 to 8.5 seconds.
  - Continuous subtle 2.5D camera drifting or parallax to eliminate static downtime.
  - Visual punchline or comedic prop insertion every 12 to 20 seconds.

---

## 3. Broadcast Audio Specifications

- **Integrated Loudness**:
  - Long-Form (16:9): `-14.0 LUFS` (±0.5 LUFS), True Peak `-1.0 dBTP`.
  - Shorts (9:16): `-12.0 LUFS` (±0.5 LUFS), True Peak `-0.5 dBTP`.
- **Dynamic EQ Filter Chain**:
  - 80Hz High-Pass (18dB/octave).
  - 320Hz notch (-2.5dB, Q=1.5) to clear room boom.
  - 4.2kHz shelf/bell (+1.8dB, Q=2.0) for vocal articulation.
  - Dynamic sidechain ducking on background music (-18dB under dialogue).

---

## 4. Chibi Character Staging & Facial Kinetic Standards

To prevent visual decapitation, facial feature overlap, and temporal desynchronization:
- **Monolithic 1:1 Puppet Canvas ($320\times 440$)**:
  - Never stack loose body + head images (prevents neck gaps and floating heads).
  - Fixed $320\times 440$ headless Chrome output without dynamic bounding-box cropping.
- **Anatomical Golden Ratios (`FACE_CONFIG`)**:
  - Eyebrows: $Y \in [124, 128]$
  - Eyes: Center $Y \in [144, 146]$, Size: $72 \times 32\text{px}$
  - Mouth Visemes: Center $Y = 186$, Size: $42 \times 22\text{px}$ (clean $15\text{px}$ vertical clearance below eyes, zero overlap)
  - Monocle & Spectacles: Monocle centered at $(182, 146)$; Spectacles at $(138, 146)$ and $(182, 146)$
  - Nose / Nose Clip: Sits strictly below eye pupil level ($Y \in [160, 172]$), never occluding or bridging pupils
  - Blink Timer: Initialized to `1.0` so characters start with eyes open by default.
- **Word-to-Frame Kinetic Synchronization**:
  - Characters remain off-screen and slide in with elastic overshoot on the exact word their name/faction is spoken.
  - Props drop with ease-in physics on action verbs.
  - Treaty stamps slam down on exact treaty keywords with camera shake.
- **Strict Historical Era Validation & Zero Debug HUD**:
  - Era gating: No modern vehicles or skyscrapers in pre-1900 scenes.
  - Zero debug text cards (`SCENE X • ACT Y` or `Episode #X`); only subtle vintage era badges fading out within 3.5s.

---

## 5. Cinematic 5-Layer Volumetric Vector Staging & Lighting Rules

To match broadcast-grade graphic-novel cinematography:
- **The "One-Look Story" Principle**:
  - Every master shot must convey complete historical and emotional stakes in a single glance (e.g. subterranean resistance couple crouched by an illegal tube radio while enemy jackboots loom outside the street-level grate).
- **Dual-Temperature Lighting Architecture**:
  - Oppressive Cold Key (`#60a5fa` / `#172554` moonlight & streetlamp shafts through iron bars) vs Intimate Warm Key (`#fef08a` / `#f59e0b` amber pool from radios, lanterns, campfires).
- **5-Layer Spatial Compositing Hierarchy**:
  1. `Layer 1: #layer-bg`: Base architectural walls, procedural userSpaceOnUse stonework patterns, distressed plaster, and external threat silhouettes.
  2. `Layer 2: #layer-lighting`: Slanted polygonal volumetric god-rays (`moonlight-beam`), floor reflection pools, and soft ambient fill circles.
  3. `Layer 3: #layer-props`: Topic-subjective hero narrative props crafted with extreme detail (e.g. arched cathedral tube radio for WWII espionage, rolled parchment and wax seals for diplomacy, astrolabe/telescope for maritime/space, steam valves for industrial era). All props follow the 5 behavioral archetypes (Monumental, Center Interactive, Handheld, Kinetic Slam/Drop, Atmospheric Radiator).
  4. `Layer 4: #layer-characters`: OverSimplified stick-figure characters elevated with directional environmental rim lighting, expressive dread/panic brows, sweat beads, and storytelling body language (crouching, ear pressed to speaker, "Shh!" finger to lips).
  5. `Layer 5: #layer-vfx`: Floating dual-tone dust motes, radio soundwaves, Morse code notes, 2.5D keyhole framing silhouette arch, radial vignette, and procedural film grain.
- **Sidecar Vector Cinematographer Delegation (`svg-scene-cinematographer`)**: When executing multi-shot documentary storyboards, 5-layer vector scene creation is delegated to dedicated `svg-scene-cinematographer` sidecar subagents in act-by-act clusters to maintain isolated context windows and guarantee uncompromised 5-layer volumetric fidelity across all cuts.
- Reference: [Cinematic SVG Mastery Guide](../youtube-history-animator/references/cinematic_svg_mastery.md)



