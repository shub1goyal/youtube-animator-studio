"""
sidecar_scene_orchestrator.py
Orchestrates micro-batching for sidecar vector illustration agents (svg-scene-cinematographer).
Strictly enforces the rule: MAXIMUM 2 SCENES PER SIDECAR AGENT (max_scenes <= 2)
to ensure uncompromised 5-layer volumetric SVG generation without token exhaustion.
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any, Tuple


MAX_SCENES_PER_SIDECAR = 2


class SidecarSceneOrchestrator:
    """
    Partitions documentary scenes into micro-batches of at most 2 scenes per subagent,
    generating structured dispatch manifests and tailored prompts for 'svg-scene-cinematographer'.
    """

    def __init__(self, script_path: str, output_dir: str, max_scenes_per_agent: int = 2):
        self.script_path = script_path
        self.output_dir = output_dir
        
        # Enforce strict maximum of 2 scenes per agent
        if max_scenes_per_agent > MAX_SCENES_PER_SIDECAR:
            print(f"⚠️ [WARNING] Requested {max_scenes_per_agent} scenes per agent exceeds limit. Clamping strictly to {MAX_SCENES_PER_SIDECAR}.")
            self.max_scenes = MAX_SCENES_PER_SIDECAR
        else:
            self.max_scenes = max(1, max_scenes_per_agent)
            
        self.scenes = self._load_scenes()
        self.sprites_dir = os.path.join(self.output_dir, "sprites", "scenes")
        os.makedirs(self.sprites_dir, exist_ok=True)

    def _load_scenes(self) -> List[Dict[str, Any]]:
        """Loads scene definitions from directors_cut_script.json or master_script.json."""
        if not os.path.exists(self.script_path):
            raise FileNotFoundError(f"Script file not found: {self.script_path}")

        with open(self.script_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            if "scenes" in data and isinstance(data["scenes"], list):
                return data["scenes"]
            elif "directors_cut" in data and isinstance(data["directors_cut"], list):
                return data["directors_cut"]
            else:
                raise ValueError("Could not locate 'scenes' or 'directors_cut' array in script JSON.")
        else:
            raise ValueError("Script JSON root must be a dict or list.")

    def create_micro_batches(self) -> List[List[Dict[str, Any]]]:
        """
        Splits total scenes into micro-batches of strictly <= 2 scenes.
        Returns: list of scene lists, where len(batch) <= 2.
        """
        batches = []
        for i in range(0, len(self.scenes), self.max_scenes):
            batch = self.scenes[i:i + self.max_scenes]
            batches.append(batch)
        return batches

    def generate_sidecar_prompt(self, batch_index: int, batch_scenes: List[Dict[str, Any]], start_index: int = 0) -> Dict[str, Any]:
        """
        Constructs the invocation prompt and metadata for a single sidecar agent.
        """
        scene_ids = []
        for idx, s in enumerate(batch_scenes):
            sc_num = s.get("scene_number") or s.get("scene_id") or (start_index + idx + 1)
            scene_ids.append(int(sc_num))

        if len(scene_ids) == 1:
            scene_range_str = f"Scene {scene_ids[0]}"
            role_title = f"Scene {scene_ids[0]:02d} Volumetric Cinematographer"
        else:
            scene_range_str = f"Scenes {scene_ids[0]} and {scene_ids[-1]}"
            role_title = f"Scenes {scene_ids[0]:02d}-{scene_ids[-1]:02d} Volumetric Cinematographer"

        scene_briefs = []
        for s, sc_num in zip(batch_scenes, scene_ids):
            era = s.get("era_badge") or s.get("era") or "HISTORICAL DOCUMENTARY"
            setting = s.get("setting") or s.get("location") or s.get("environment") or "Historical Chamber"
            narration = s.get("vo_hinglish") or s.get("narration") or s.get("vo") or ""
            characters = s.get("characters") or []
            hero_props = s.get("hero_props") or s.get("props") or []
            visual_cue = s.get("visual_cue") or ""
            lighting = s.get("lighting") or "Dual-temperature (warm brass lantern + cold moonlight window)"

            brief = f"""
### Scene {sc_num:02d}: {s.get('title', f'Historical Scene {sc_num}')}
- **Era / Badge**: {era}
- **Architectural Setting**: {setting}
- **Visual Cue**: {visual_cue}
- **Narration Context**: "{narration}"
- **Characters & Staging**: {characters}
  * Left Actor: Active gesture (pointing, holding prop, or chin stroke)
  * Right Actor: Contrasting reactive gesture (head clutch panic, arms crossed, or shock)
- **Hero Narrative Props**: {hero_props} (Apply Bezier curvature, meniscus, bubbles, and glowing bloom; NO raw polygons)
- **Lighting Rig**: {lighting} (Couple light rays to visible lamp/window emitters and character rim strokes)
- **Target SVG**: {os.path.join(self.sprites_dir, f'scene_{sc_num:02d}.svg')}
- **Target PNG**: {os.path.join(self.sprites_dir, f'scene_{sc_num:02d}.png')}
"""
            scene_briefs.append(brief.strip())

        combined_briefs = "\n\n".join(scene_briefs)

        prompt = f"""You are the Master Vector Scene Cinematographer sidecar agent.
You are assigned to illustrate {scene_range_str} (STRICT MAXIMUM 2 SCENES).

## MANDATORY VISUAL STANDARDS:
1. Rule of Zero Empty Void (#layer-bg):
   - Wall texture <pattern> (brickwork, bunker concrete, or wood wainscoting)
   - Left/Right peripheral architectural framing (X in [0, 350] and [1570, 1920])
   - Ceiling rafters/beams (Y in [0, 90]) and perspective floor plane (Y in [840, 1080])
   - 45px dark keyhole framing silhouette arch on outer perimeter

2. Coupled Motivated Lighting (#layer-lighting):
   - Every character rim light MUST be coupled to an explicit emitter (lamp god-rays, ambient light pool, floor pool).
   - In dual-temperature setups, use cold blue (#60a5fa) left rim and warm amber (#fbbf24) right rim.

3. Hero Props Craftsmanship (#layer-props):
   - ZERO RAW POLYGONS. Erlenmeyer & Florence glassware with cubic Bezier bases, curved liquid meniscus, rising bubbles, and white specular glass arcs.
   - Equations and atomic models must use <filter id="radio-bloom"> for radiant glow.

4. Anti-Clone Asymmetric Character Rigs (#layer-characters):
   - OverSimplified chibi aesthetic (white circle heads, noodle limbs, bean bodies).
   - Never clone twin poses. Left actor gets active gesture; Right actor gets contrasting shock/panic gesture.

5. MapLore Overlays (#layer-vfx):
   - Comic alert double-badges (!! / ?!) popping at Y-95px with #facc15 fill and #ef4444 shadow.
   - Curved-pointer micro-dialogue bubbles with dashed pointer lines.
   - Subtle floating dust motes and procedural film grain overlay.

## SCENES TO ILLUSTRATE (EXACTLY {len(batch_scenes)} SCENE{'S' if len(batch_scenes) > 1 else ''}):
{combined_briefs}

## EXECUTION STEPS:
1. Generate complete, unminified, pristine 1920x1080 SVGs (viewBox="0 0 1920 1080") for each assigned scene.
2. Save SVGs to the target paths above.
3. Rasterize each SVG to 1920x1080 transparent PNG using Chrome Headless:
   & "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --headless=new --disable-gpu --hide-scrollbars --window-size=1920,1080 --screenshot="<out.png>" "file:///<abs_svg>"
4. Reply with completed filepaths and visual breakdown.
"""
        return {
            "batch_index": batch_index,
            "scene_ids": scene_ids,
            "role": role_title,
            "subagent_type": "svg-scene-cinematographer",
            "prompt": prompt.strip(),
            "target_svgs": [os.path.join(self.sprites_dir, f"scene_{sc:02d}.svg") for sc in scene_ids],
            "target_pngs": [os.path.join(self.sprites_dir, f"scene_{sc:02d}.png") for sc in scene_ids]
        }

    def generate_manifest(self) -> Dict[str, Any]:
        """
        Compiles the full dispatch manifest across all micro-batches.
        Verifies that no batch has > 2 scenes.
        """
        batches = self.create_micro_batches()
        sidecar_tasks = []

        for idx, batch in enumerate(batches, 1):
            start_index = (idx - 1) * self.max_scenes
            task = self.generate_sidecar_prompt(idx, batch, start_index=start_index)
            sidecar_tasks.append(task)

        manifest = {
            "total_scenes": len(self.scenes),
            "max_scenes_per_sidecar": self.max_scenes,
            "total_sidecar_dispatches": len(sidecar_tasks),
            "granularity_compliance": all(len(t["scene_ids"]) <= MAX_SCENES_PER_SIDECAR for t in sidecar_tasks),
            "tasks": sidecar_tasks
        }

        # Save manifest to disk
        manifest_path = os.path.join(self.output_dir, "sidecar_dispatch_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print(f"✅ Generated Sidecar Dispatch Manifest: {manifest_path}")
        print(f"   Total Scenes: {manifest['total_scenes']} | Dispatches: {manifest['total_sidecar_dispatches']} (Max {self.max_scenes} scenes/agent)")
        return manifest


def main():
    parser = argparse.ArgumentParser(description="Sidecar Scene Orchestrator with <= 2 scenes/subagent enforcement.")
    parser.add_argument("--script", required=True, help="Path to directors_cut_script.json or master_script.json")
    parser.add_argument("--output-dir", required=True, help="Project output directory")
    parser.add_argument("--max-scenes", type=int, default=2, help="Max scenes per sidecar (capped strictly at 2)")
    args = parser.parse_args()

    orchestrator = SidecarSceneOrchestrator(args.script, args.output_dir, max_scenes_per_agent=args.max_scenes)
    manifest = orchestrator.generate_manifest()
    print(f"Granularity Compliance Verified: {manifest['granularity_compliance']}")


if __name__ == "__main__":
    main()
