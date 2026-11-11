"""
ai_script_generator.py
AI Viral Script Generator for Historical & Explainer Animations
Supports:
- YouTube Shorts (60s)
- Long-Form Documentaries (10 to 15 Minutes) via Hierarchical Multi-Act Generation
- Natural Hinglish with Colloquial Punchlines & Slapstick Visual Directions
- Audited Hinglish Phonetics with English Loanword Protection
- Automatic Key Pool Rotation across 20+ Gemini API keys
"""

import sys
import os
import json
import urllib.request
import urllib.error
import time
import argparse

# Import configuration and phonetic engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import get_gemini_api_keys
from gemini_tts_engine import HinglishPhoneticEngine


class AIScriptGenerator:
    def __init__(self, keys_file=None, model="gemini-2.5-flash"):
        self.model = model
        self.phonetic_engine = HinglishPhoneticEngine()
        
        raw_keys = []
        if keys_file and os.path.isfile(keys_file):
            try:
                with open(keys_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        raw_keys = data
                    elif isinstance(data, dict):
                        raw_keys = data.get("gemini_api_keys", []) or data.get("keys", [])
            except Exception:
                raw_keys = []
        if not raw_keys:
            raw_keys = get_gemini_api_keys()

        self.keys = [str(k).strip() for k in raw_keys if str(k).strip()]
        if not self.keys:
            # Fallback mock placeholder if operating offline or testing
            self.keys = ["DUMMY_KEY_SET_GEMINI_API_KEY"]
        self.current_key_idx = 0

    def get_next_key(self):
        key = self.keys[self.current_key_idx]
        self.current_key_idx = (self.current_key_idx + 1) % len(self.keys)
        return key

    def _call_gemini_json(self, prompt, max_tokens=4096, max_retries=15):
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.75,
                "maxOutputTokens": max_tokens
            }
        }
        attempts = 0
        while attempts < max_retries:
            api_key = self.get_next_key()
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(req, timeout=70) as resp:
                    data = json.loads(resp.read().decode())
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(raw_text)
            except urllib.error.HTTPError as e:
                time.sleep(0.3)
                attempts += 1
            except Exception as e:
                time.sleep(0.3)
                attempts += 1
        raise RuntimeError(f"Failed to call Gemini JSON after {max_retries} attempts.")

    def generate_long_form_10_15_mins(self, topic, target_mins=12, language="hinglish"):
        """Generates a complete 10-15 minute documentary using hierarchical multi-act episodic generation."""
        print(f"🎬 Architecting {target_mins}-minute long-form documentary on: '{topic}'...")

        # Stage 1: Generate Master 6-Act Narrative Architecture
        outline_prompt = f"""
You are the head writer for an OverSimplified-style viral historical documentary channel.
Create a detailed 6-Act master outline for a {target_mins}-minute video on:
TOPIC: "{topic}"
LANGUAGE: {language.upper()}

The documentary must cover the full epic historical arc with intense narrative pacing, comedic slapstick, and mindblowing factual twists.

Return JSON with this schema:
{{
  "title": "Main Viral Title with Emojis",
  "packaging": {{
    "title_options": ["Title 1", "Title 2", "Title 3"],
    "thumbnail_concept": "High contrast 3-color concept with chibi characters and glowing map",
    "thumbnail_text": "Max 3-4 words"
  }},
  "acts": [
    {{
      "act_number": 1,
      "act_title": "Title of Act 1",
      "time_range": "0:00 - 2:30",
      "summary": "Core conflict, historical paradox, and comedic focus of this act"
    }}
  ]
}}
Ensure exactly 6 distinct chronological acts are generated.
"""
        outline = self._call_gemini_json(outline_prompt, max_tokens=3000)
        print(f"✅ Generated 6-Act Master Outline: {outline.get('title', topic)}")

        all_scenes = []
        global_scene_num = 1

        # Stage 2: Generate detailed scenes act by act
        for act in outline.get("acts", []):
            act_num = act["act_number"]
            act_title = act["act_title"]
            print(f"📝 Scripting Act {act_num}/6: '{act_title}' ({act.get('time_range', '')})...")

            act_prompt = f"""
You are writing Act {act_num} of 6 for a viral {target_mins}-minute OverSimplified-style animation.
TOPIC: "{topic}"
ACT TITLE: "{act_title}"
ACT SUMMARY: "{act.get('summary', '')}"
LANGUAGE: {language.upper()}

Write 5 to 6 continuous chronological scenes for this act (each scene between 20 to 28 seconds).
REQUIREMENTS:
1. Pacing: Every scene must have:
   - Punchy conversational {language.upper()} dialogue (use colloquial phrases: 'Bhai socho', 'Lafda ho gaya', 'Game palat gaya', 'Deal sign hui').
   - Specific comedic character action (slapstick, sweat drops, money eyes, fainting, coffee spitting).
   - Clear map directions (borders glowing, dashed trade arrows, troop movements).
   - Exact sound effects (SFX: whoosh, stamp thud, cha-ching, sad trombone).
2. AdSense Green Dollar compliance: Keep historical conflict cartoonish (no gore, no sensitive policy violations).

Return JSON with schema:
{{
  "scenes": [
    {{
      "duration_seconds": 24,
      "visual_cue": "Detailed 2D layout: characters, expressions, actions, props",
      "map_directions": "What map is shown, borders, vectors",
      "sfx": "Exact sound effects cues",
      "vo_hinglish": "Spoken colloquial narration for subtitles"
    }}
  ]
}}
"""
            act_data = self._call_gemini_json(act_prompt, max_tokens=4096)
            for sc in act_data.get("scenes", []):
                sc["scene_number"] = global_scene_num
                # Apply audited phonetic transliteration
                sc["vo_phonetic_tts"] = self.phonetic_engine.phonetize(sc["vo_hinglish"])
                all_scenes.append(sc)
                global_scene_num += 1

        total_sec = sum(s.get("duration_seconds", 22) for s in all_scenes)
        print(f"🎉 Complete Long-Form Script Finished: {len(all_scenes)} scenes ({total_sec/60:.1f} minutes)!")

        return {
            "title": outline.get("title", topic),
            "topic": topic,
            "language": language,
            "target_duration_seconds": total_sec,
            "packaging": outline.get("packaging", {}),
            "acts": outline.get("acts", []),
            "scenes": all_scenes
        }

    def generate_script(self, topic, format_type="shorts", language="hinglish", target_mins=12):
        if format_type == "long_form":
            return self.generate_long_form_10_15_mins(topic, target_mins=target_mins, language=language)

        # Standard YouTube Short (60s)
        prompt = f"""
You are the world's best viral YouTube historical animation director (OverSimplified style).
Create a 60-second viral Short script about: "{topic}" in {language.upper()}.
Return JSON with 4-5 rapid scenes (10-14s each), packaging, and visual/sfx cues.
"""
        data = self._call_gemini_json(prompt, max_tokens=2048)
        for s in data.get("scenes", []):
            s["vo_phonetic_tts"] = self.phonetic_engine.phonetize(s.get("vo_hinglish", ""))
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="History of UAE: Desert to Superpower", help="Topic for the video")
    parser.add_argument("--format", choices=["shorts", "long_form"], default="long_form")
    parser.add_argument("--mins", type=int, default=12, help="Target duration in minutes for long form")
    parser.add_argument("--lang", default="hinglish", help="Language: hinglish or english")
    parser.add_argument("--out", default="epic_script.json", help="Output JSON path")
    args = parser.parse_args()

    generator = AIScriptGenerator()
    script = generator.generate_script(args.topic, format_type=args.format, language=args.lang, target_mins=args.mins)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(script, f, indent=2, ensure_ascii=False)
    print(f"Saved complete script to {args.out}")
