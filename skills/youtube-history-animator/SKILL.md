---
name: youtube-history-animator
description: >-
  Directs and orchestrates end-to-end AI-powered production of viral historical and educational 2D animated videos (16:9 long-form and 9:16 vertical Shorts) in the style of OverSimplified, History Matters, and Animated History. PRIMARY LANGUAGE OF CONTENT: HINGLISH FIRST (Conversational Romanized Hindi + English loanwords). Orchestrates dedicated sidecar vector cinematographers (svg-scene-cinematographer) for uncompromised 5-layer volumetric SVGs, Gemini 3.8 Flash TTS (Voice: Charon) with rotating API key pools and audited Hinglish phonetics, automated vector asset rigging, and broadcast audio mastering.
---

# YouTube History & Educational Animation Director (Full-Auto AI Studio)

> [!IMPORTANT]
> **PRIMARY LANGUAGE OF CONTENT: HINGLISH FIRST**
> All video productions on this channel are **Hinglish-First** by default (Conversational Hindi written in Roman script with natural English loanwords like *deal, trade, king, war, tax, border, company, strategy*).
> Tone matches OverSimplified: colloquial, high-energy, witty, and dramatic (*"Bhai socho...", "Lafda shuru hua...", "Game poora palat gaya!", "Ab entry hoti hai...", "Kismat ne aisi palti maari..."*). English is available as a secondary option via `--lang english`.

This skill completely automates the production of viral historical and educational animated videos from topic idea to finished, broadcast-ready 1080p MP4 video—requiring **zero manual scriptwriting, zero voiceover recording, and zero manual video editing**.

---

## 1. Quick One-Command Execution (Autonomous Studio Pipeline)

Run the master end-to-end studio pipeline to generate a complete broadcast-ready **10–15 Minute Long-Format Documentary** or **60s Viral Short** with physics-aware 2D vector animation, Gemini 3.8 TTS voiceover, steady subtitles, sound design, and full packaging:

### Long-Format (10 to 15 Minutes Documentary - Hinglish Default):
```powershell
py <plugin-root>/skills/youtube-history-animator\scripts\full_auto_producer.py --topic "History of UAE" --format long_form --mins 12 --lang hinglish --out uae_documentary
```

### Viral YouTube Short (60s Vertical Video - Hinglish Default):
```powershell
py <plugin-root>/skills/youtube-history-animator\scripts\full_auto_producer.py --topic "How America Bought Louisiana for $15M" --format shorts --lang hinglish --out louisiana_short
```

---

## 2. Autonomous Studio Architecture & Self-Auditing Loop

When a topic is given, the studio executes 6 autonomous phases with strict quality gates:

1. **Phase 1: Deep-Dive Hierarchical Scripting (`studio_script_engine.py` & `story_pacing_calculator.py`)**:
   - **Language Priority: HINGLISH FIRST**: All scripts are generated in high-energy, comedic Romanized Hindi with English loanwords, ensuring high audience retention and relatable Indian conversational humor.
   - **Calibrated Mathematical Pacing Formula (Empirical Gemini 3.8 Flash TTS Charon Pace: 158.4 WPM / 2.64 Words/Sec / 0.379s per word)**:
     * **10-Minute Video (600s)**: Strictly **1,580 – 1,600 spoken words**.
     * **12-Minute Video (720s)**: Strictly **1,880 – 1,920 spoken words**.
     * **15-Minute Video (900s)**: Strictly **2,350 – 2,400 spoken words**.
     * Formula: $\text{Target Words} = \text{Target Minutes} \times 158.4$, $\text{Duration (s)} = \text{Word Count} \times 0.379$.
   - **Strict Non-Repetitive 5-Act Narrative Architecture**:
     * **Act 1 (15% - ~240-360 words)**: The Shock Hook & Forgotten Status Quo. Zero foreshadowing of final resolution.
     * **Act 2 (20% - ~320-480 words)**: The Catastrophe / Inciting Disruption (old industry collapses, existential panic).
     * **Act 3 (25% - ~400-600 words)**: The Geopolitical Struggle & Failed Attempts (battles, treaties, rivalries).
     * **Act 4 (25% - ~400-600 words)**: The Discovery & Grand Alliance (unification, breakthroughs, massive risk).
     * **Act 5 (15% - ~240-360 words)**: Beyond Resource Curse & The Space Climax (diversification, modern legacy).
   - **Zero-Repetition Quality Gate**:
     * Zero narrative loops or repeated jokes (e.g. Bedouin thirst or pearl crash must NOT be re-explained after Act 2).
     * Script must pass `StoryPacingEngine.audit_script_for_repetition()`. No 3-word n-gram loops across distinct acts.
2. **Phase 2: Gemini 3.8 Flash TTS Voiceover (`gemini_tts_engine.py`)**:
   - Synthesizes speech with neural voice **`Charon`** across an automated rotating pool of **20+ API keys**.
   - Built-in **Audited Hinglish Phonetics**: Protects 120+ English loanwords (`extreme`, `trade`, `future`, `crisis`, `strategy`, `company`) from corruption while transliterating Romanized Hindi (`ret` $\rightarrow$ `rayt`, `garmi` $\rightarrow$ `gur-mee`, `bheje` $\rightarrow$ `bhay-jay`).
   - **Quality Gate**: Measures combined WAV duration. Automatically validates $\ge 11.5 - 13.5$ minutes spoken runtime.
   - Mastered to broadcast **-14.0 LUFS** with true peak **-1.0 dB**.
3. **Phase 3: Multi-Track Sound Design Bed (`sound_design_engine.py`)**:
   - Synthesizes procedural sound effects (whooshes, rubber stamp thuds, 3D coin chimes, ship horns, sad trombones, fireworks explosions) layered over a subtle ambient score.
4. **Phase 4: Visual Breakdown & Vector Asset Synthesis via Sidecars (`svg-scene-cinematographer` & `visual_asset_synthesizer.py`)**:
   - Analyzes every scene's visual cues and narration dynamically for **ANY topic** (historical, scientific, geopolitical, or biographical) to determine:
     * True contextual environment (diplomatic treaty chambers, war rooms, underground cellars, scientific laboratories, battlefields, maritime harbors, expedition camps, modern metropolises, cosmic vistas).
     * Exact character cast and topic-specific narrative props needed for that specific concept.
   - **Distributed Sidecar Delegation (`svg-scene-cinematographer`)**:
     * To prevent context window bloat and quality degradation across 35–50 scenes, the parent agent delegates master 5-layer volumetric SVG creation to the **`svg-scene-cinematographer` sidecar subagent**.
     * Dispatches scenes in act-by-act clusters (e.g. Act 1 scenes to Sidecar 1, Act 2 to Sidecar 2).
     * Each sidecar operates in an isolated context window, outputting uncompromised `1920x1080` SVGs with dual-temperature lighting, topic-subjective hero props, and rim-lit character rigs, then rasterizing to transparent PNGs via headless Chrome.
     * The parent agent receives notification via Antigravity's reactive wakeup and streams assets into `AIAnimationDirector`.
   - Produces `directors_cut_script.json` with strict era-accurate staging.
5. **Phase 5: Whisper Forced Alignment & Action Beat Sheet Generation (`whisper_aligner.py` & `beat_sheet_generator.py`)**:
   - Transcribes every audio scene using `faster-whisper` (base int8 model on CPU) down to 10ms word boundaries.
   - Cross-references script visual cues and entities against spoken words to build `scene_beat_sheets.json`.
   - Maps exact trigger timestamps for character entrances (`"slide_from_left"`, `"slide_from_right"`), prop gravity drops, ragdoll faints, and rubber stamp slams.
6. **Phase 6: 25-Year Veteran AI Animation Director (`ai_animation_director.py`)**:
   - **Word-to-Frame Kinetic Action Synchronization**: Characters enter dynamically on the exact word their faction/name is spoken (e.g. at word *"British"*, Officer slides in with elastic overshoot; at *"Emperor"*, monarch enters; at *"General"*, commander arrives). Off-screen until spoken.
   - **Kinetic Prop Drops & Stamp Slams**: At word *"Crash"*, market crash board plummets down; at *"Treaty"*, treaty table drops and golden/green stamp slams down with ease-in physics.
   - **Spoken Viseme Modulation**: Puppet mouths flap in sync with active Whisper word timestamps and remain naturally closed during pauses.
   - **Anatomically Unified Rigs**: Monolithic 1:1 SVGs ($320\times 440$). Heads, necks, collars, robes, and limbs are completely continuous (zero neck gap, zero decapitation, zero modular body duplication).
   - **Chibi Facial Feature Alignment (`FACE_CONFIG`)**:
     * Eyebrows: $Y \in [124, 128]$
     * Eyes: Center $Y \in [144, 146]$, Size: $72\times 32\text{px}$
     * Monocle & Spectacles: Monocle centered at $(182, 146)$ around pupil; Spectacles centered at $(138, 146)$ and $(182, 146)$
     * Nose Clip / Accessories: Positioned strictly below eye level ($Y \in [160, 172]$), never occluding or bridging pupils
     * Mouth Visemes: Center $Y = 186$, Size: $42\times 22\text{px}$, maintaining a clean $15\text{px}$ vertical clearance below eyes (zero overlap)
     * Headdress/Ghutra: Forehead canvas ($X \in [105, 215], Y \in [100, 220]$) must remain open, framing side drapes only
     * Robot Visor: Cyan glowing LED visor with procedural chest audio waveform for speech
   - **Intelligent Staging & Zero Collision**: Characters are positioned with dynamic balance (never overlapping buildings or props; rival diplomats across treaty tables; commanders presenting battle plans to reacting advisors).
   - **OverSimplified Kinetics**: Speech cadence bobbing, eye blinking (`blink_timer` starts at `1.0` so characters start with eyes open, never closed at $t=0$), pupil gaze tracking, reactive expressions (shock wide eyes, sweat droplets, dollar eyes, knockout X eyes), and ragdoll faints.
   - **Strict Historical Era Validation**: Enforce era compatibility matrix (no modern supercars, skyscrapers, or airplanes in 19th-century or ancient scenes; 1820 scenes feature British warships and treaty tables, modern supercars only appear on 2020s highways).
   - **Clean Broadcast Packaging**: Zero debug text (NO "SCENE X • ACT Y", NO "Episode #X" cards). Subtle vintage era stamps appear on historical transitions and fade out smoothly within 3.5s.
   - **Steady Kinetic Subtitles**: Active word highlighting in gold (`#FACC15`) anchored at bottom center.
   - Direct RGBA zero-copy pipeline into FFmpeg for rapid rendering at 25 FPS.
7. **Phase 7: Hybrid 2.5D Compositing & Deterministic Rendering (`kinetic_video_renderer.py`)**:
   - Master GSAP / HTML5 Canvas 2.5D compositor with Universal Skeletal IK Character Rigs (`skeletal_puppet_engine.js`), Real GeoJSON Cartography (`geojson_map_engine.py`), and 12 Universal Procedural Environment Engines (`hybrid_asset_generator.py`).
   - Playwright headless Chromium stepped deterministically via `window.seekToTime(t)` piping frames to FFmpeg.
8. **Phase 8: Automated Visual QA Gate & Packaging (`visual_qa_inspector.py` & `autonomous_studio.py`)**:
   - Forensic visual QA: extracts 12 sample frames across timeline, verifies resolution (1920x1080), luminance, and motion delta into `qa_report.json` and a 4x3 labeled `contact_sheet.png`.
   - Verifies final MP4 resolution (1920x1080), duration ($\ge 10-15$ mins), and audio synchronization.
   - Generates `captions.srt` and `PRODUCTION_BIBLE.md` (High-CTR titles, timestamps, description, tags, thumbnail concept).

---

## 3. Mandatory Character Rig & Facial Alignment Specifications

To ensure characters NEVER collapse, decapitate, overlap facial features, or desynchronize in future production runs:

### A. Monolithic 1:1 Canvas Architecture ($320\times 440$)
- **Never Stack Loose Body + Head Sprites**: Stacking separate body and head images causes coordinate drift, neck gaps, or duplicate bodies (e.g. head floating over bisht with blue legs sticking out). All OverSimplified characters MUST be defined as a single monolithic vector SVG with fixed $320\times 440$ viewBox.
- **Zero Bounding Box Cropping**: Headless Chrome rendering must output the full $320\times 440$ viewport. Never apply PIL `bbox` dynamic cropping, which causes variable sprite bounds and breaks procedural facial overlays.

### B. Facial Alignment Coordinate Golden Ratios (`FACE_CONFIG`)
On the $320\times 440$ character canvas:
| Feature | Center Coordinate $(X, Y)$ | Sprite Dimensions $(W \times H)$ | Clearance / Alignment Rule |
| :--- | :--- | :--- | :--- |
| **Eyebrows** | $(160, 126)$ | N/A (SVG path) | Positioned at $Y \in [124, 128]$, cleanly framing eyes |
| **Eye Sprites** | $(160, 144)$ | $72 \times 32\text{px}$ | Left pupil $(138, 144)$, Right pupil $(182, 144)$ |
| **Monocle** | $(182, 146)$ | Circle $r=16\text{px}$ | Perfectly encloses left eye pupil |
| **Spectacles** | $(138, 146)$ & $(182, 146)$ | Circles $r=18\text{px}$ | Encloses both pupils with bridge at $Y=146$ |
| **Nose Clip / Nose** | $(160, 166)$ | $10 \times 14\text{px}$ | Sits at $Y \in [160, 172]$, strictly BELOW eye level |
| **Mouth Visemes** | $(160, 186)$ | $42 \times 22\text{px}$ | Exactly $42\text{px}$ below eye center ($15\text{px}$ clean vertical clearance) |
| **Beard / Chin** | $(160, 200)$ | N/A (SVG path) | Goatee or chin outline cleanly under mouth |

### C. Headwear & Headdress Standards
- The Ghutra/Keffiyeh white front layer must drape down the sides of the head ($X \le 105$ and $X \ge 215$) and never solid-fill the forehead down to $Y=180$. The facial canvas ($X \in [105, 215], Y \in [100, 220]$) must remain open for skin, eyebrows, and eyes.
- Knots, bandanas, and headbands must be symmetrical with no loose horizontal polygons extending outside the character silhouette.

### D. Procedural Physics & Blink Timer Initialization
- `PhysicsCharacterPuppet.blink_timer` must initialize to `1.0` (eyes open by default). Never initialize to `0.0` (which forces closed eyes at $t=0$).
- Periodic blinks trigger every 2.5–5.0s for exactly 0.16s before reopening.

---

## 4. Collision-Free Cinema Staging & Dynamic Semantic Prop Synthesis

Props are **never hardcoded or static**. Every YouTube video topic (e.g. WWII French Resistance, Louisiana Purchase, French Revolution, Cold War Espionage, Ancient Rome, Space Exploration, or Industrial Revolution) dynamically dictates its own unique, subject-matter-accurate props extracted from the script's `visual_cue` and narration.

To guarantee that characters, monumental architecture, and narrative props **NEVER collide, overlap, or leave empty voids**, props are classified and choreographed by their **Spatial & Kinetic Behavioral Archetype**:

### A. Dynamic Collision-Free Stage Zoning Engine
The 1920x1080 canvas is strictly choreographed using the Rule of Thirds:
- **Left Stage Zone**: $X \approx 420 - 520\text{px}$
- **Center Stage Zone**: $X \approx 860 - 1060\text{px}$
- **Right Stage Zone**: $X \approx 1320 - 1560\text{px}$

#### Spatial Conflict Resolution by Prop Archetype:
1. **Archetype 1: Monumental / Architectural Anchors (Right Stage Zone: $X \ge 1200\text{px}$)**:
   - Scale: Dominant background/midground scale ($W \approx 400 - 800\text{px}$).
   - Examples by Topic:
     * *WWII / Espionage*: Radar listening tower, bunker blast door, barbed wire gate.
     * *Colonial / Diplomatic*: Grand treaty chamber arch, Royal Navy warship on horizon, palace colonnade.
     * *Industrial / Modern*: Factory smokestack, oil derrick, nuclear dome, skyscraper, launch gantry.
     * *Ancient / Medieval*: Castle battlement, Roman triumphal arch, pyramid, siege tower.
   - **Collision Rule**: Characters MUST be positioned on the **Left Stage ($X \approx 480\text{px}$)** or Center-Left facing right towards the monument. Never place a character inside the monument's footprint ($X \ge 1200\text{px}$).
2. **Archetype 2: Center-Stage Interactive Props (Center Stage Zone: $X \approx 740 - 960\text{px}$)**:
   - Scale: Furniture / shared interaction scale ($W \approx 200 - 360\text{px}$).
   - Examples by Topic:
     * Diplomatic conference tables with treaty scrolls, secret cellar tables with cathedral radios, laboratory workbenches with test tubes, campfire stone rings, strategy war-room sandtables.
   - **Collision Rule**: Positioned strictly between two confronting or negotiating characters (Character 1 at $X \approx 480\text{px}$ on Left; Character 2 at $X \approx 1440\text{px}$ on Right).
3. **Archetype 3: Handheld Narrative & Cultural Props (Anchored to Character Hands)**:
   - Scale: Handheld micro-scale ($W \approx 80 - 160\text{px}$).
   - Examples by Topic:
     * *Hospitality / Calm*: Ceramic teacups, brass coffee pots, wine goblets, beer steins.
     * *Conflict / Betrayal*: Concealed daggers, flintlock pistols, quill pens, gavels, spy magnifying glasses.
     * *Trade / Economics*: Clinking gold coin pouches, stock market price tags, ledger books.
   - **Kinetic Rule**: Clink or gesture on spoken verbs, track character arm pivot coordinates.
4. **Archetype 4: Kinetic Verbs & Comedic Cut-Gags (Dynamic Plummets / Stamp Slams)**:
   - Behavior: Off-screen until triggered by Whisper audio alignment on specific action words.
   - Examples by Topic:
     * Massive notary stamps slamming down on treaty scrolls (`"TREATY APPROVED!"`).
     * Market crash downward arrow boards plummeting from ceiling.
     * Giant price tags dropping on trade bargains.
     * Falling guillotine blades, dropping anvils, or bouncing question marks.
5. **Archetype 5: Atmospheric Radiators (Volumetric Light & Particle Emitters)**:
   - Function: Act as the primary localized light source for Layer 2 volumetric god-rays and rim lighting.
   - Examples by Topic:
     * Glowing cathedral vacuum-tube radios, flickering candle stubs, brass hurricane lamps, campfires with rising embers, CRT radar screens, steam engine furnace grates.

### B. Dynamic Semantic Script & Visual Cue Breakdown
The Director pipeline (`visual_asset_synthesizer.py`) parses every scene's `visual_cue` and `vo_hinglish` dynamically for ANY topic:
- **Zero Hardcoded Props**: Props are extracted dynamically using noun-phrase and visual cue analysis.
- **On-the-Fly Vector Synthesis**: Any topic-specific prop not already in the vector sprite library is synthesized dynamically using the 5-layer graphic-novel vector standard (`6.5px` ink strokes, cel-shaded occlusion, specular highlights, and contact shadows).
- **Era-Appropriate Visual Language**: The script engine enforces historical coherence (e.g. Victorian quills in 1820, cathedral radios in 1940, CRT terminals in 1969, holographic displays in modern sci-fi).

### C. Multi-Layered Compositing Order
To ensure proper depth without clipping:
1. `render_environment(env)`: High-contrast sky, gradient landscape/interior walls, stars/windows.
2. **Background Environmental & Monumental Props**: Castles, factories, skylines, warships, towers, background monuments ($X \ge 1200\text{px}$).
3. **Dynamic Puppet Performance**: Springs, speech visemes, pupil gaze, ragdoll faints.
4. **Foreground Interactive & Handheld Props**: Tables, scientific apparatus, cups, quills, coins, documents ($X \approx 740 - 960\text{px}$ or character hand coordinates).
5. **Screen Overlays**: Kinetic rubber stamps, vintage era badges, and Whisper-synced steady subtitles.

### D. 5-Plane 2.5D Parallax & Volumetric Lighting Engine (Mandatory Cinema Standard)
To eliminate flat "clipart" visuals, `ai_animation_director.py`, `cinematic_svg_engine.py`, and `unified_rig_generator.py` enforce a 5-plane cinematic compositing pipeline at 25 FPS:

1. **Bold Graphic-Novel Vector Standard (`unified_rig_generator.py` & `character_rig_generator.py`)**:
   - All `320x440` character rigs and props use uniform `6.5-9.0px` outer ink outlines (`#050608`, round caps/joins), `3.5-5.0px` interior detail lines, and two-tone cel-shaded shadow layers (neck/chin occlusion, garment folds, specular glass highlights).
2. **Ground Contact Shadows (Zero Floating Props)**:
   - Every character puppet (`320x440`), tent, monument, lantern, campfire, and chai saucer MUST render a soft Gaussian-blurred elliptical contact shadow (`rgba(2,3,6,0.85)`) on the stage floor at `(anchor_x, foot_y)`.
3. **Dynamic Alpha-Mask Rim Lighting & Volumetric Bloom**:
   - Light-emitting props (`vintage-radio`, `oil_lantern_tent`, `campfire`, `nuclear_atom_plant`, moonlight beams) emit multi-frequency radial glow pools onto the ground and surrounding architecture.
   - Character puppets feature directional environmental rim lighting (`#fbbf24` / `#f59e0b` for fire/radio amber glow, `#60a5fa` for cold moonlit shafts) on the side of the sprite facing the primary light source.
4. **Continuous Micro-Physics (Never Freeze Frames)**:
   - Stationary characters continuously execute subtle breathing oscillation + eye saccades + periodic `0.16s` blinks (`blink_timer = 1.0` at `t=0`).
   - Floating volumetric dust motes drift across light beams (cyan motes in moonlight, golden motes in amber glow).
5. **5-Plane Virtual Camera Matrix**:
   - Every scene runs a continuous 2.5D camera track (`slow_push_in`, `pan_left_right`, `reveal_pullback`) multiplying camera `(dx, dy, zoom)` by plane parallax weights: Sky (`0.12x`), Far Horizon (`0.40x`), Midground Stage & Rigs (`1.00x`), Volumetric VFX (`1.00x`), and Blurred Foreground Framing + Vignette (`1.42x`).

### E. Master 5-Layer Volumetric Vector Scene Standard (`cinematic_svg_engine.py`)
All master scene illustrations (1920x1080) follow the rigorous 5-layer volumetric architecture demonstrated by the French Resistance benchmark:
1. **`<defs>` Stack**: Multi-tier blurs (`blur-heavy` 45, `blur-medium` 16, `blur-soft` 5), multi-stage `radio-bloom` (`feMerge`), procedural `film-grain` (`feTurbulence`), dual-temperature linear/radial gradients, and tileable stonework/timber patterns.
2. **Layer 1: `#layer-bg`**: Architectural backdrop, userSpaceOnUse stone/wood patterns, distressed plaster `<path>` curves, alcoves with props in shadow, outside world threat silhouettes (e.g. enemy jackboots, warships).
3. **Layer 2: `#layer-lighting`**: Volumetric god-rays (slanted polygonal shafts with multi-stop alpha gradients), floor reflection pools, soft ambient fill pools.
4. **Layer 3: `#layer-props`**: Period-accurate hero narrative props with mechanical craftsmanship (cathedral tube radio, brass lanterns, candle wax stubs, glowing frequency dials with red needles and calibration ticks).
5. **Layer 4: `#layer-characters`**: Minimalist OverSimplified stick-figure characters elevated with directional rim lighting, expressive dread/panic eyebrows, gaze tracking, sweat beads, and storytelling body language (crouching, ear pressed to speaker, "Shh!" finger to lips).
6. **Layer 5: `#layer-vfx`**: Storytelling VFX (soundwaves, Morse code `• • • —`, whispered quotes), dual-temperature floating dust motes, foreground framing silhouette arch (creating 2.5D keyhole depth), heavy radial vignette, and procedural film grain overlay.
- Reference: [Cinematic SVG Mastery Guide](./references/cinematic_svg_mastery.md)

### F. Sidecar Dispatch Orchestration (`svg-scene-cinematographer` + `kinetic-beat-choreographer`)
To prevent context window bloat and quality degradation when producing 10–20 minute long-form documentaries (which require intricate 5-layer SVGs, multi-shot cuts, and millisecond Whisper synchronization), the production pipeline dispatches work across dedicated sidecar subagents:

1. **`svg-scene-cinematographer`**:
   - Dedicated sidecar vector illustrator responsible for generating the master `1920x1080` 5-layer volumetric SVGs with full architectural depth, tileable stone/brick/panel patterns, motivated volumetric god-rays and rim lighting, and crafted Bezier props.
   - Outputs for each assigned scene:
     - `scene_X_stage.svg` (or `scene_X.svg`): 5-layer volumetric vector master.
     - `scene_X_shots.json`: Sequence of 5–18 cinematic shots bound strictly to Whisper sentence boundaries.
     - `scene_X_movie.html`: Interactive Playwright player implementing `window.seekToTime(t)` with dynamic camera pans/zooms and shallow DOF blur modulation.
   - **Granularity Rule**: **1 Scene per assignment** for complex multi-shot documentary scenes (or at most 2 for lightweight scenes). Dedicate 100% of the subagent token budget to complete, unminified markup.
   - **Rendering Mode**: Video rendering is executed by deterministic frame-stepping (`kinetic_video_renderer.py` / `ai_animation_director.py`), NOT by static `t=0` PNG screenshots.

2. **`kinetic-beat-choreographer`**:
   - Action and timing director that cross-references `faster-whisper` word timestamps (10ms granularity) with narrative visual cues to generate `scene_beat_sheets.json`.
   - Programs progressive typewriter equation/map reveal wipe masks, MapLore comic alert popups (`!!`/`?!`), curved-pointer dialogue callouts, and micro-physics triggers (Bohr orbital rotation, flask bubbles, camera zooms).

> [!IMPORTANT]
> **MANDATORY ARCHITECTURAL RULE: DETERMINISTIC 2.5D MOVIE ENGINE**
> Every scene generated by `svg-scene-cinematographer` produces `scene_X_movie.html` alongside `scene_X_shots.json`. The video rendering engine steps through time slices via `window.seekToTime(t)`, capturing all CSS keyframes, character breathing/blinking cycles, mouth visemes, and camera matrix pans/zooms on every single frame at 25 FPS. Zero static holds or frozen t=0 screenshots.

- **Independent Context Windows**: Each sidecar runs in an isolated conversation context, eliminating token exhaustion.
- **Reactive Wakeup Orchestration**: The parent agent dispatches all micro-batches asynchronously without polling; Antigravity's reactive messaging system awakens the parent when subagents complete asset compilation.
- **Sidecar Agent Invocation Pattern (Micro-Batches of $\le 2$ Scenes)**:
  ```python
  # Dispatching an Act of 6 scenes across 3 sidecars (strictly <= 2 scenes per subagent):
  scene_pairs = [(1, 2), (3, 4), (5, 6)]

  for start_sc, end_sc in scene_pairs:
      invoke_subagent(
          TypeName="svg-scene-cinematographer",
          Role=f"Scenes {start_sc}-{end_sc} Volumetric Cinematographer",
          Prompt=f"""
          Illustrate scenes {start_sc} and {end_sc} (STRICT MAXIMUM 2 SCENES) for documentary '{topic}' adhering strictly to the 5-layer volumetric standard.
          - Canvas: 1920x1080 (viewBox="0 0 1920 1080")
          - Max 2 Scenes Rule: Dedicate full token budget to complete, unminified, uncompromised SVG markup for each scene. Zero truncation.
          - Architecture: Rule of Zero Empty Void - wall texture <pattern>, peripheral X in [0, 350] and [1570, 1920] framing, ceiling beams Y in [0, 90], floor plane Y in [840, 1080], and 45px keyhole silhouette arch.
          - Lighting: Motivated dual-temperature lighting with explicit light emitters and coupled character rim lights.
          - Props: Zero raw polygons. Laboratory flasks with cubic Bezier curves, liquid meniscus, bubbles, and specular glass arcs.
          - Characters: Anti-clone asymmetric staging using the 6 gesture presets.
          - Output: Save SVG files to '{output_dir}/sprites/scenes/scene_{{num:02d}}.svg' and rasterize each to transparent PNG using Chrome headless.
          """
      )

  # Sidecar 2: Kinetic Beat & MapLore Choreography
  invoke_subagent(
      TypeName="kinetic-beat-choreographer",
      Role="Act 1 Kinetic Beat Choreographer",
      Prompt=f"""
      Choreograph kinetic action beat sheets for scenes 1 through 6 of documentary '{topic}'.
      - Cross-reference audio/word_timestamps/scene_{{num}}_words.json with visual cues.
      - Assign progressive reveal masks (typewriter wipes) for equations, maps, and bullet points.
      - Schedule MapLore comic reaction callouts ('!!', '?!', curved-pointer speech bubbles) on high-energy words ('Lafda', 'Shock', 'Broke', 'Game').
      - Configure continuous micro-physics: Bohr atom orbital rotations, flask bubbling, and punchy camera cuts.
      - Output: Append choreographed timing events to '{output_dir}/scene_beat_sheets.json'.
      """
  )
  ```

### G. Strict Visual Quality Guardrails: The Volumetric + MapLore Cinema Standard
Inspecting benchmark frames against broadcast standards dictates five non-negotiable visual rules:

#### Rule A: The "Zero Empty Void" Architectural Rule (`#layer-bg`)
A scene background may NEVER be a single flat/gradient `<rect>` behind a centered board or table. Every `1920x1080` SVG generated MUST include at least **4 architectural sub-elements** in `#layer-bg`:
1. **Wall Texture `<pattern>`**: `userSpaceOnUse` tiled brickwork, laboratory plaster panels, wood wainscoting, or bunker concrete covering the back wall (`opacity="0.65-0.85"`).
2. **Left/Right Peripheral Architecture ($X \in [0, 350]$ and $X \in [1570, 1920]$)**:
   - Frame outer edges with recessed arched alcoves, tall paned windows showing outside night sky/streetlights, wooden bookshelves with silhouetted books/beakers, or heavy timber support pillars.
3. **Ceiling & Floor Structural Anchors ($Y \in [0, 90]$ and $Y \in [840, 1080]$)**:
   - Overhead timber beams, industrial pipes, or hanging brass pendant lamps at the top, and a textured floor plane with perspective floorboards/tiles at the bottom.
4. **Foreground Keyhole Silhouette Arch (`#layer-vfx`)**:
   - Frame the outer 45px perimeter of the `1920x1080` canvas with a dark out-of-focus vignette arch (`#020306`, `opacity="0.88"`) to create instant 2.5D depth.

#### Rule B: Ban Raw Geometric Primitives in `#layer-props` (Craftsmanship Standard)
- **STRICT BAN**: Never output a raw 3-point `<polygon>` triangle as a beaker/flask, or a plain `<rect>` as a machine.
- **Erlenmeyer & Florence Flask Standard**: Laboratory glassware MUST be drawn with rounded cubic Bezier bases, cylindrical neck rims (`<ellipse>`), translucent colored chemical fills (`opacity="0.75"`), curved liquid meniscus lines, 3–5 internal rising gas bubbles (`<circle fill="#fff" opacity="0.6"/>`), and crisp white vertical glass specular reflection arcs (`stroke="#ffffff" stroke-width="3" opacity="0.55"`).
- **Glowing Scientific / Historical Diagrams**: When rendering equations or diagrams (e.g. U-235 fission chain or Bohr atom model), apply `<filter id="radio-bloom">` (`feGaussianBlur stdDeviation="10"` + `"28"` `feMerge`) so the red nucleus (`#ef4444`) and cyan electron orbitals (`#38bdf8`) visibly glow against the chalkboard.

#### Rule C: Coupled Light-Source-to-Rim-Light Enforcement (`#layer-lighting`)
Every character rim-light arc MUST be physically motivated by a visible light emitter in `#layer-lighting`:
- If characters have a warm top-right rim light (`#fbbf24`), `#layer-lighting` MUST render:
  1. Slanted polygonal god-rays (`<polygon fill="url(#warm-lamp-beam)"/>`) projecting down from an overhead brass lamp or window, AND
  2. A `<circle fill="url(#amber-glow)" filter="url(#blur-heavy)"/>` ambient light pool illuminating the wall/board behind them, plus an elliptical floor reflection pool (`<ellipse filter="url(#blur-medium)"/>`) at their feet.
- In dual-light scenes (cold blue window on left $X=200$, warm glowing atom/radio on right $X=1450$), the left character receives a `#60a5fa` left-edge rim stroke and the right character receives a `#fbbf24` right-edge rim stroke.

#### Rule D: Anti-Clone Asymmetric Pose Engine
When a scene contains 2 or more characters (e.g. `Dr. Otto Hahn` at $X=760$ and `Fritz Strassmann` at $X=1140$), **NEVER render both puppets with identical idle arms, identical mouth visemes, and identical sweat drops**.
Implement **6 Modular Arm & Gesture Presets** inside the `320x440` rig (`stroke="#050608" stroke-width="18" stroke-linecap="round"` with white `<circle r="13"/>` hands):
1. `pose="pointing_up_board"`: Right noodle arm raised diagonally (`M 205 260 C 245 230 265 180 285 135`) holding a chalk stick, pointer wand, or magnifying glass aimed at the board/map.
2. `pose="head_clutch_panic"`: Both arms curved upward (`M 115 260 C 75 220 80 150 110 125` and `M 205 260 C 245 220 240 150 210 125`) with white circle hands gripping the sides of the head in disbelief.
3. `pose="chin_stroke_thinking"`: Left arm crossed under chest, right hand raised to chin (`(175, 202)`) with asymmetric furrowed brow (one brow raised, one lowered).
4. `pose="shh_finger_lips"`: Hand raised to `(160, 188)` with upright index finger `<rect>` over tense small `O` mouth.
5. `pose="holding_prop_chest"`: Forearm angled across torso holding a topic-specific handheld prop (clipboard, bubbling test tube, treaty scroll, or gold coin).
6. `pose="ear_cupping_listen"`: Body leaned `12deg` toward sound source, back hand cupping ear (`(102, 145)`), front hand reaching toward dial/table.

**Two-Character Staging Formula:**
- **Primary Actor (Left)**: Active gesture (`pointing_up_board`, `holding_prop_chest`, or `chin_stroke_thinking`) + active speaking viseme synced to Whisper.
- **Secondary Actor (Right)**: Contrasting reactive gesture (`head_clutch_panic`, `arms_crossed_skeptical`, or `shock_lean_back`) + distinct eye/brow state + pupil gaze directed at the Primary Actor or focal prop.

#### Rule E: MapLore Kinetic Storytelling & Progressive Reveals
Inspired by viral *MapLore* Shorts and *Unknown Frequencies*, static props and text on boards animate progressively in sync with `faster-whisper` word timestamps:
1. **Progressive Chalkboard / Map Reveal (`reveal_mode="typewriter_sync"`)**:
   - Progressive line wipes reveal equations line-by-line as spoken; Bohr Atom pops with elastic scale (`0 -> 1.18 -> 1.0`) when *"atomic"* or *"fission"* is spoken.
2. **MapLore Comic Reaction Callouts (`kinetic_callout_overlay`)**:
   - **Comic Alert Badge (`!!` / `?!`)**: Yellow/Red double-exclamation badge (`#facc15` fill, `#ef4444` drop shadow, `#050608` 5px outline) popping above character head (`Y - 95px`) with spring bounce physics on high-energy words (*"Lafda"*, *"Shock"*, *"Khatam"*).
   - **Curved-Pointer Micro-Dialogue Bubble**: Dark slate pill (`rgba(9,13,22,0.94)`, gold border `#facc15`) with a dashed curved SVG pointer line (`stroke-dasharray="6 4"`) pointing to character mouth for 1.8s comedic interjections.
3. **Continuous Micro-Physics**:
   - Continuously rotate Bohr atom orbitals (`25 FPS`), float laboratory flask bubbles upward, and punch in camera zooms (`1.0x -> 1.22x`) on dramatic comedic beats.

#### Rule F: Standalone Self-Animating Vector Standard & Frame-by-Frame Video Kinetics
- **Strict Ban on Frozen Slides**: Video outputs must NEVER consist of static still photos with only digital camera zooms. Every frame rendered to MP4 MUST capture live movement.
- **Embedded CSS `@keyframes` in Every SVG**: Every master SVG must be a 100% self-animating standalone movie in any browser containing embedded `<style type="text/css">`:
  * `@keyframes svgBreathing`: Alive harmonic squash/stretch and vertical translation.
  * `@keyframes svgEyeBlink`: Realistic organic blinks (`scaleY(0.08)` for 0.12s every 3.2s).
  * `@keyframes svgSweatDrop`: Dripping comedic sweat drops.
  * `@keyframes svgDustFloat`: Floating dual-temperature atmospheric dust motes.
  * `@keyframes svgAlertPop`: Comic alert badge spring bounce and wobble.
  * `@keyframes svgOrbitalRotate`: Continuous 360° electron orbital revolutions.
  * `@keyframes svgBeakerBubble`: Chemical gas bubbles rising inside Erlenmeyer flasks.
  * `@keyframes svgRadiationPulse`: Periodic radioactive bloom expansion.
- **Frame-by-Frame Kinetic Compositor (`kinetic_video_renderer.py`)**:
  * Audio Waveform Lip-Sync: Reads PCM audio amplitude to flap character mouth visemes in exact sync with narrator syllables; closes mouth during speech pauses.
  * Dynamic Gesture Transitions: Characters raise pointing arms or clutch head with spring overshoot (`ease_out_back`) at key narrative timestamps.
  * MapLore Comic Overlays: Comic alert double-badges (`!!`/`?!`) and curved-pointer dialogue cards pop onto screen on high-energy keywords with elastic bounce.
  * Dynamic 2.5D Camera: Continuous eased push-ins and impact camera shake on dramatic shock/detonation moments.
  * Interactive Player: Every project provides `scene_X_movie.html` for 60 FPS real-time browser preview, 16:9 Cinema vs 9:16 Shorts crop, and deterministic frame-stepping export via `window.seekToTime(t)`.


---

## 5. Historical Era Compatibility & Broadcast Visual Staging

To prevent anachronisms and amateur artifacts:
- **Era Gating Matrix**:
  * **Pre-1900s (Ancient to 1892)**: Bedouin tents, camel caravans, sailing dhows, British warships, treaty tables, vintage maps. **PROHIBITED**: Supercars, airplanes, modern skyscrapers, oil derricks, robots.
  * **1900s–1950s (Pearl Crash & Pre-Oil)**: Traditional pearling boats, market crash boards, vintage office desks.
  * **1958–1970s (Oil Boom & 1971 Union)**: Oil derricks, oil geysers, Union House, 1971 flag hoisting ceremony.
  * **1980s–Present (Modern Era)**: Burj Khalifa, modern Dubai skyline highways, Emirates commercial aircraft, supercars, Mars Hope orbiter, AI robot minister.
- **Zero Debug HUD Text**: Final renders MUST NOT display `SCENE X • ACT Y` or `Episode #X` text cards. Only subtle, elegant era stamps (e.g. `1820: TRUCIAL TREATY`) that fade out within 3.5s.

---

## 6. Production Reference Architecture: Scripts & Modules

All pipeline scripts are maintained in the skill `scripts/` directory:
- `autonomous_studio.py`: Full master controller running 6 autonomous phases.
- `cinematic_svg_engine.py`: Master 5-layer volumetric vector scene generator (1920x1080) with dual-temperature lighting and film grain.
- `ai_animation_director.py`: 25-year veteran AI director streaming direct RGBA to FFmpeg.
- `unified_rig_generator.py`: Monolithic 1:1 SVG character definitions and headless Chrome rasterizer.
- `character_rig_generator.py`: OverSimplified chibi character generator with directional rim lighting and expressive poses.
- `physics_rig.py`: Damped harmonic oscillators, `FACE_CONFIG`, speech visemes, pupil gaze tracking, and ragdoll entity.
- `whisper_aligner.py`: Faster-Whisper CPU int8 forced aligner down to 10ms word boundaries.
- `beat_sheet_generator.py`: Maps script entities to Whisper timestamps for action triggers.
- `studio_script_engine.py`: Dynamic 7-act narrative arc expansion $\ge 1,750$ words (Hinglish-First).
- `gemini_tts_engine.py`: Gemini 3.8 Flash TTS key pool rotator with audited Hinglish phonetics.
- `sound_design_engine.py`: Procedural multi-track audio bed mastered to -14.0 LUFS.
- `sprites/`: Pre-rasterized transparent PNG character and prop rigs at exact 1:1 coordinates.

---

## 7. Execution Commands & Sidecar Workflows

### A. Sidecar Vector Cinematographer Task Dispatch (`svg-scene-cinematographer`)
Delegate 5-layer volumetric master SVG scenes to dedicated sidecar subagents to prevent context saturation:
```python
invoke_subagent(
    TypeName="svg-scene-cinematographer",
    Role="Act 1 Vector Cinematographer",
    Prompt="""
    Illustrate scenes 1 through 6 for documentary '{topic}' in 1920x1080 SVG adhering strictly to the 5-layer volumetric standard.
    Save SVGs to '{output_dir}/sprites/scenes/' and rasterize to PNG with Chrome headless.
    """
)
```

### B. Master 5-Layer Volumetric Vector Scene Generator (CLI Standalone)
Generate complete 1920x1080 broadcast-grade cinematic vector scenes or rasterize them to transparent PNG:
```powershell
py <plugin-root>/skills\youtube-history-animator\scripts\cinematic_svg_engine.py --scene "ww2_cellar_resistance" --out "scene_cellar.svg" --rasterize "scene_cellar.png"
```
- Reference: [Cinematic SVG Mastery: The 5-Layer Volumetric Standard](./references/cinematic_svg_mastery.md)

### C. AI Script Generator (Hinglish-First Master Engine)
Generates high-retention viral scripts with phonetic markers (defaults to Hinglish):
```powershell
py <plugin-root>/skills\youtube-history-animator\scripts\ai_script_generator.py --topic "Battle of Plassey" --format long_form --mins 12 --lang hinglish --out script.json
```
- Reference: [Hinglish Phonetics Guide](./references/hinglish_phonetics_guide.md)
- Reference: [Viral Scripting Framework](./references/viral_scripting_framework.md)

### D. Gemini 3.8 Flash TTS Engine (Voice: Charon, Hinglish Calibrated)
Synthesizes voiceovers with automatic key rotation and phonetic optimization:
```powershell
py <plugin-root>/skills\youtube-history-animator\scripts\gemini_tts_engine.py --text "Bhai suno! 1803 mayn sabse bada lafda hua!" --out voice.wav
```
- Reference: [AI Voice Monetization Playbook](./references/ai_voice_monetization_guide.md)

### E. Cinematic Character & Map Vector Generators
- Generate custom Chibi Character SVGs with directional rim lighting and poses:
  `py <plugin-root>/skills\youtube-history-animator\scripts\character_rig_generator.py --name resistance_fighter --expression intense_dread --pose ear_listening --rim-color "#f59e0b" --out char.svg`
- Generate Vintage Historical Map SVGs:
  `py <plugin-root>/skills\youtube-history-animator\scripts\map_svg_generator.py --out map.svg`
- Reference: [2D Animation Production Pipeline](./references/animation_pipeline.md)

---

## 8. Hinglish Scriptwriting & Phonetics Master Standard (Primary Content Language)

All content for this channel is engineered **Hinglish-First** to maximize viral retention and relatable Indian comedic timing:

### A. The 5 Golden Hinglish Writing Rules
1. **Conversational OverSimplified Tone**: The narrator speaks like a witty, knowledgeable friend talking across a tea stall. Never use formal or textbook language.
2. **Indian Slang & Comedic Idioms**:
   - Hooks: *"Bhai socho...", "Aap vishwaas nahi karoge..."*
   - Conflict: *"Lafda tab shuru hua...", "Dono aapas mein bhid gaye!"*
   - Twists: *"Game poora palat gaya!", "Kismat ne aisi palti maari ki..."*
   - Climax: *"Unhone bola: 'Hold my Karak Chai!' aur poora khel khatam kar diya."*
3. **Natural English Loanwords (NEVER translate into pure Sanskritized Hindi)**:
   - Keep natural everyday words in English: *company, trade, tax, king, empire, deal, contract, profit, army, ship, border, strategy, battle, court, minister, power, cash, gold*.
   - Saying *"British East India Vyapaar Samiti"* sounds robotic; saying *"British East India Company ne trade tax free karwa liya"* sounds viral and natural.
4. **Clean First 15 Seconds (AdSense & Monetization Rule)**:
   - Zero policy triggers in the hook (avoid 'kill', 'blood', 'die', 'murder'). Frame the opening around a shocking paradox, money, greed, or strategic absurdity.
5. **No Backtracking**: Once a historical act resolves an event, never loop back to repeat explanations.

### B. Gemini 3.8 Flash Neural TTS Phonetic Rules (Voice: `Charon`)
To make Gemini pronounce Romanized Hinglish with natural Indian cadence:
- **Silent "E" Trap**: Replace trailing 'e' with 'ay' (`kare` $\rightarrow$ `karay`, `bheje` $\rightarrow$ `bhay-jay`, `chale` $\rightarrow$ `chalay`, `rakhe` $\rightarrow$ `ra-khay`).
- **Nasalization**: Write `mein` as `mayn` and `hain` as `hayn`.
- **Syllable Hyphens**: Hyphenate multi-syllable Hindi words so the neural model pronounces every syllable cleanly (`kha-reed-nay`, `chaa-hi-yay`, `luff-daa`, `joo-gaad`, `sub-kee`, `ba-naa-ya`).
- **Pacing Math**: 158.4 WPM ($0.3788\text{ s/word}$). Target 45–60 words per 20–25s scene.

---

## 9. Mandatory Call-To-Action (CTA) Architecture & OverSimplified Animation Kinetics

Every animated documentary and vertical short produced by this studio MUST integrate a **Two-Tier Strategic Call-To-Action (CTA)** designed for high audience retention, subscriber conversion, and zero immersion-breaking:

### A. Two-Tier Strategic CTA Timing & Placement
1. **Tier 1: Mid-Roll Retention Hook CTA (at 45%–55% Runtime / Act 3-to-4 Transition)**:
   - **Purpose**: Captures the viewer right after the high-stakes narrative climax/inciting disruption, before viewer drop-off.
   - **Spoken Hinglish Narration**: Must be conversational, narrative-embedded, and high-energy:
     > *"Bhai, agar tumhe ye geopolitical game samajh aa raha hai aur dekh kar maza aa raha hai, toh fatafat LIKE thoko aur channel ko SUBSCRIBE kar lo, kyunki agla move aur bhi zyada dangerous hone wala hai!"*
   - **Visual Motion Staging**:
     - Dynamic 2.5D floating **Subscribe Pill** (`#kinetic-cta-pill`) slides smoothly in from the bottom-right corner ($X: 1400 \to 1280, Y: 940$) with an elastic overshoot easing (`cubic-bezier(0.34, 1.56, 0.64, 1)`).
     - Pill features: YouTube Red `#EF4444` "SUBSCRIBE" button, mouse cursor click animation, and transition to gray `#334155` "SUBSCRIBED" with a swinging golden notification bell (`#FACC15`).
     - **Chibi Character Arm Gesture**: The primary puppet on screen momentarily breaks the fourth wall, gestures toward the subscribe badge with an expressive wink or smile, then returns to the narrative action within 3.5 seconds.
   - **Duration**: Strictly 3.5 to 4.5 seconds on-screen, auto-fading via SVG opacity transition.

2. **Tier 2: End-Roll Climax Debate & Channel CTA (at 92%–98% Runtime / Resolution Act 5)**:
   - **Purpose**: Drives high-velocity comment debates and permanent subscriber lock-in.
   - **Spoken Hinglish Narration**:
     > *"Agar channel par naye ho toh @ShadowMindset_Hindi ko SUBSCRIBE karke bell icon zaroor dabana, aur niche comments mein batao ki agar us din ye gaddari nahi hoti... toh kya itihaas badal sakta tha? Milte hain agli masterclass mein!"*
   - **Visual Motion Staging**:
     - 3D Bold Bangers Typography banner: *"SUBSCRIBE FOR MORE GEOPOLITICAL MASTERCLASSES"*.
     - Full End-Screen Card layouts ($16:9$ left box: Previous Video recommendation; right box: Playlist).
     - Animated golden bell ringing with procedural radial particles.
   - **Sound Design**: Satisfying mechanical mouse click SFX (`click_switch.wav`) followed by a resonant metallic bell chime (`bell_chime_bright.wav`).

### B. Standard Vector CTA Kinetic SVG Component Spec
```xml
<!-- REUSABLE MASTER KINETIC CTA PILL (Screen Space / Pinned to 1920x1080) -->
<g id="kinetic-cta-pill" transform="translate(1320, 920)" opacity="0" class="pointer-events-none transition-all duration-500">
  <!-- Backdrop Blur Pill -->
  <rect width="520" height="96" rx="48" fill="#090d16" fill-opacity="0.94" stroke="#fbbf24" stroke-width="2.5" filter="url(#cta-shadow)"/>
  <!-- Channel Avatar / Monogram -->
  <circle cx="56" cy="48" r="34" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
  <text x="56" y="55" fill="#f8fafc" font-size="20" font-weight="900" font-family="'Impact', 'Arial Black', sans-serif" text-anchor="middle">SM</text>
  <!-- Channel Label -->
  <text x="108" y="44" fill="#f8fafc" font-size="19" font-weight="800" font-family="system-ui, sans-serif">Shadow Mindset</text>
  <text x="108" y="66" fill="#94a3b8" font-size="13" font-weight="600" font-family="system-ui, sans-serif">@ShadowMindset_Hindi</text>
  <!-- YouTube Subscribe Button -->
  <g id="cta-btn-sub" transform="translate(320, 24)" class="cursor-pointer">
    <rect width="135" height="48" rx="24" fill="#ef4444" id="cta-btn-bg"/>
    <text x="67" y="30" fill="#ffffff" font-size="14" font-weight="900" font-family="'Impact', 'Arial Black', sans-serif" text-anchor="middle" letter-spacing="1">SUBSCRIBE</text>
  </g>
  <!-- Golden Bell Notification Icon -->
  <g id="cta-bell" transform="translate(470, 48)">
    <path d="M -9 8 L 9 8 C 8 8 7 7 7 4 L 7 -4 C 7 -9 3 -12 0 -12 C -3 -12 -7 -9 -7 -4 L -7 4 C -7 7 -8 8 -9 8 Z M -3 11 C -3 12.5 -1.5 14 0 14 C 1.5 14 3 12.5 3 11 Z" fill="#facc15" stroke="#78350f" stroke-width="1.5"/>
  </g>
</g>
```

---

## 10. Zero-Delay Caption & Whisper Forced Alignment Contract (MANDATORY QUALITY GATE)

> [!CAUTION]
> **CRITICAL PRODUCTION REGRESSION PREVENTION: ZERO DELAYED CAPTIONS**
> Under NO circumstances may any video scene, shot timeline, or subtitle element be generated using mathematical divisions (`duration / N` or uniform $5.81\text{s}$ spacing). Doing so causes severe subtitle drift, premature cuts mid-sentence, and desynchronization with the narrator.

### A. Root Cause Diagnostic & Strict Banned Pattern
- **BANNED CODE PATTERN**:
  ```python
  # ❌ STRICTLY BANNED: Causes catastrophic caption delay and mid-sentence cuts!
  shot_duration = total_duration / float(num_shots)
  for i in range(num_shots):
      shot['start'] = i * shot_duration
      shot['end'] = (i + 1) * shot_duration
  ```
- **Why It Fails**: Real human and neural TTS speech velocity fluctuates heavily:
  - An intense 8-word sentence may take $3.2\text{s}$.
  - A complex historical exposition may take $8.9\text{s}$.
  - If a shot is artificially forced to $5.8\text{s}$, the subtitle flips before the narrator finishes, producing visual lag and viewer confusion.

### B. Mandatory 4-Step Whisper Execution Protocol
Every production pipeline MUST strictly enforce the following sequence:

1. **Step 1: Audio WAV Synthesis (`gemini_tts_engine.py`)**:
   Master WAV file (`scene_X.wav`) is generated and mastered to -14 LUFS.
2. **Step 2: Faster-Whisper Forced Alignment (NON-SKIPPABLE GATE)**:
   - `faster-whisper` (`base` or `small` model, CPU int8 quantized) MUST be executed on `scene_X.wav` *before* generating shot breakdowns.
   - Extracts 10ms word boundaries and sentence timestamps saved to `audio/whisper_timestamps/scene_X_whisper.json`:
     ```json
     {
       "sentences": [
         {"start": 0.00, "end": 8.98, "text": "Bhai, imagine karo ek aisi private company..."},
         {"start": 8.98, "end": 14.80, "text": "...aur agle do sau saalon mein 300 million logon par raaj karti hai!"}
       ],
       "words": [
         {"word": "Bhai,", "start": 0.00, "end": 0.46},
         {"word": "imagine", "start": 0.68, "end": 1.06}
       ]
     }
     ```
3. **Step 3: Shot Boundaries Strictly Bound to Whisper Sentences**:
   - Every shot in `scene_X_shots.json` MUST set `start = sentence.start` and `end = sentence.end`.
   - Shot cuts occur ONLY on natural spoken breath pauses and punctuation points ($t \pm 0.05\text{s}$).
4. **Step 4: Deterministic Subtitle Rendering**:
   - In movie HTML players and renderers, subtitles are dynamically resolved via:
     ```javascript
     const activeSub = SUBTITLES.find(sub => t >= sub.start && t <= sub.end);
     movieSubtitle.innerHTML = activeSub ? activeSub.text : '';
     ```
   - In deterministic frame-stepping (`window.seekToTime(t)`), the subtitle rendered at time $t$ matches the exact spoken audio at time $t$ with zero drift.

### C. Automated Pre-Render Sync Audit Gate (`audit_subtitle_sync.py`)
Before Playwright frame-stepping or FFmpeg encoding starts, an automated audit must pass:
1. Verify `scene_X_whisper.json` exists for every scene.
2. Verify variance between shot durations is $> 0.5\text{s}$ (flags any attempt at uniform linear division).
3. Verify maximum offset between subtitle end and sentence audio end is $\le 100\text{ms}$.
4. If drift $> 0.2\text{s}$ is detected, pipeline halts with `IncompleteAlignmentError`.

