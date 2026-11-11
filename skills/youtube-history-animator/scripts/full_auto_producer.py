"""
Full End-to-End AI YouTube History & Explainer Animation Producer
Automates the entire pipeline from Topic to Production-Ready Episode:
1. Generates Viral High-Retention Hinglish/English Script (with Gemini API key rotation)
2. Runs YouTube AdSense & YPP Monetization Compliance Audit
3. Synthesizes Voiceover with Gemini 3.8 Flash TTS (Voice: Charon) & Phonetic Normalizer
4. Broadcast Masters Audio (-14 LUFS Long-Form / -12 LUFS Shorts)
5. Generates Episode Character SVGs & Animated Map Assets
6. Generates Video Subtitle (.srt) File
7. Generates Shot-by-Shot Timeline & Viral Thumbnail Packaging
"""

import sys
import os
import json
import argparse
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POLICY_SCRIPTS = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "youtube-policy-monetization-guard", "scripts"))
if POLICY_SCRIPTS not in sys.path:
    sys.path.append(POLICY_SCRIPTS)

from ai_script_generator import AIScriptGenerator
from gemini_tts_engine import GeminiTTSManager
import compliance_checker

def seconds_to_srt_time(secs):
    hrs = int(secs // 3600)
    mins = int((secs % 3600) // 60)
    s = int(secs % 60)
    ms = int((secs - int(secs)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{s:02d},{ms:03d}"

def run_full_pipeline(topic, format_type="shorts", language="hinglish", output_dir="episode_package", target_mins=12):
    sys.stdout.reconfigure(line_buffering=True)
    os.makedirs(output_dir, exist_ok=True)
    print("=" * 70, flush=True)
    print(f"🎬 LAUNCHING FULL-AUTO AI ANIMATION PRODUCER", flush=True)
    print(f"Topic: {topic}", flush=True)
    print(f"Format: {format_type.upper()} ({target_mins} mins) | Language: {language.upper()}", flush=True)
    print("=" * 70, flush=True)

    if format_type == "long_form":
        from autonomous_studio import AutonomousStudio
        studio = AutonomousStudio(topic, target_minutes=target_mins, output_dir=output_dir)
        return studio.execute_studio_pipeline()

    # 1. Script Generation
    print("\n[Step 1/6] Generating Viral Script with AI...")
    script_gen = AIScriptGenerator()
    script_data = script_gen.generate_script(topic, format_type=format_type, language=language, target_mins=target_mins)
    
    script_json_path = os.path.join(output_dir, "script.json")
    with open(script_json_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved script JSON: {script_json_path}")

    # 2. Compliance Audit
    print("\n[Step 2/6] Auditing Script Against YouTube Policies...")
    full_text = " ".join([s.get("vo_hinglish", "") for s in script_data.get("scenes", [])])
    compliance_checker.audit_script(full_text)

    # 3. Voiceover Generation with Gemini 3.8 Flash TTS (Charon)
    print("\n[Step 3/6] Generating Voiceover with Gemini 3.8 Flash TTS (Voice: Charon)...")
    tts_manager = GeminiTTSManager(model="gemini-3.8-flash-tts", voice="Charon")
    audio_dir = os.path.join(output_dir, "audio")
    mastered_audio = tts_manager.generate_scene_voiceovers(
        script_data["scenes"], audio_dir, mode=format_type
    )

    # 4. Generate Subtitles (.srt)
    print("\n[Step 4/6] Generating Timed Subtitle (.srt) File...")
    srt_path = os.path.join(output_dir, "captions.srt")
    current_time = 0.0
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        for idx, scene in enumerate(script_data["scenes"], 1):
            dur = scene.get("duration_seconds", 12)
            start_t = seconds_to_srt_time(current_time)
            end_t = seconds_to_srt_time(current_time + dur)
            caption_text = scene.get("vo_hinglish", "")
            
            srt_file.write(f"{idx}\n{start_t} --> {end_t}\n{caption_text}\n\n")
            current_time += dur
    print(f"✅ Generated timed subtitles: {srt_path}")

    # 5. Asset Generation (Character Rigs & Map)
    print("\n[Step 5/6] Generating Episode Vector Assets...")
    assets_dir = os.path.join(output_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Run character rig generator
    char_script = os.path.join(os.path.dirname(__file__), "character_rig_generator.py")
    map_script = os.path.join(os.path.dirname(__file__), "map_svg_generator.py")
    uae_map_script = os.path.join(os.path.dirname(__file__), "generate_uae_map.py")

    topic_lower = topic.lower()
    if any(k in topic_lower for k in ["uae", "emirates", "dubai", "abu dhabi", "arab"]):
        leader_svg = os.path.join(assets_dir, "sheikh_zayed_leader.svg")
        subprocess.run([sys.executable, char_script, "--name", "sheikh_zayed", "--hat", "keffiyeh", "--expression", "smug", "--prop", "oil_barrel", "--out", leader_svg], check=True)

        diver_svg = os.path.join(assets_dir, "pearl_diver.svg")
        subprocess.run([sys.executable, char_script, "--name", "pearl_diver", "--hat", "none", "--expression", "shocked", "--prop", "pearl_oyster", "--out", diver_svg], check=True)

        officer_svg = os.path.join(assets_dir, "british_officer.svg")
        subprocess.run([sys.executable, char_script, "--name", "british_officer", "--hat", "powdered_wig", "--expression", "neutral", "--prop", "dagger_behind_back", "--out", officer_svg], check=True)

        map_svg = os.path.join(assets_dir, "uae_history_map.svg")
        subprocess.run([sys.executable, uae_map_script, "--out", map_svg], check=True)
    else:
        protagonist_svg = os.path.join(assets_dir, "protagonist.svg")
        subprocess.run([sys.executable, char_script, "--name", "protagonist", "--hat", "powdered_wig", "--expression", "smug", "--out", protagonist_svg], check=True)

        rival_svg = os.path.join(assets_dir, "rival.svg")
        subprocess.run([sys.executable, char_script, "--name", "rival", "--hat", "bicorne", "--expression", "shocked", "--out", rival_svg], check=True)

        map_svg = os.path.join(assets_dir, "historical_map.svg")
        subprocess.run([sys.executable, map_script, "--out", map_svg], check=True)
    print(f"✅ Generated SVG assets in: {assets_dir}")

    # 6. Production Bible & Storyboard Markdown
    print("\n[Step 6/6] Generating Production Bible & Packaging...")
    bible_path = os.path.join(output_dir, "PRODUCTION_BIBLE.md")
    
    with open(bible_path, "w", encoding="utf-8") as bf:
        bf.write(f"# Episode Production Bible: {script_data.get('title')}\n\n")
        bf.write(f"**Topic**: {topic}\n")
        bf.write(f"**Format**: {format_type.upper()}\n")
        bf.write(f"**Language**: {language.upper()} (Hinglish)\n")
        bf.write(f"**Voice**: Gemini 3.8 Flash TTS (`Charon`)\n")
        bf.write(f"**Mastered Audio**: `{os.path.basename(mastered_audio)}`\n\n")
        
        bf.write("## Packaging (CTR Engineering)\n")
        pkg = script_data.get("packaging", {})
        bf.write(f"- **Suggested Titles**:\n")
        for t in pkg.get("title_options", []):
            bf.write(f"  1. {t}\n")
        bf.write(f"- **Thumbnail Hook Concept**: {pkg.get('thumbnail_concept')}\n")
        bf.write(f"- **Thumbnail Bold Text**: `{pkg.get('thumbnail_text')}`\n\n")

        bf.write("## Shot-by-Shot Storyboard & Timeline\n\n")
        for sc in script_data.get("scenes", []):
            bf.write(f"### Scene {sc.get('scene_number')} ({sc.get('duration_seconds')}s)\n")
            bf.write(f"- **Visual Cue**: {sc.get('visual_cue')}\n")
            if "map_directions" in sc:
                bf.write(f"- **Map Animation**: {sc.get('map_directions')}\n")
            bf.write(f"- **SFX**: {sc.get('sfx')}\n")
            bf.write(f"- **Voiceover (Hinglish Subtitles)**: *\"{sc.get('vo_hinglish')}\"*\n")
            bf.write(f"- **TTS Phonetic Line**: `{sc.get('vo_phonetic_tts')}`\n\n")

    print(f"✅ Production Bible generated: {bible_path}")
    print("\n" + "=" * 70)
    print(f"🎉 PRODUCTION PACKAGE FULLY ASSEMBLED IN: {output_dir}")
    print("=" * 70)
    return output_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True, help="Historical topic")
    parser.add_argument("--format", choices=["shorts", "long_form"], default="shorts")
    parser.add_argument("--mins", type=int, default=12, help="Target duration in minutes for long form")
    parser.add_argument("--lang", default="hinglish", help="Language")
    parser.add_argument("--out", default="episode_package", help="Output directory")
    args = parser.parse_args()

    run_full_pipeline(args.topic, format_type=args.format, language=args.lang, output_dir=args.out, target_mins=args.mins)
