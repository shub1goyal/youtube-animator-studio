"""
engine_2d/beat_sheet_generator.py
Generates millisecond-accurate action beat sheets by cross-referencing:
1. Script visual cues, characters, and props (uae_12min_production/directors_cut_script.json)
2. Whisper word timestamps (uae_12min_production/audio/word_timestamps/scene_{i}_words.json)
3. Dynamic Collision-Free Stage Zoning (Left/Center/Right balance, zero character-prop overlap)

Outputs: uae_12min_production/scene_beat_sheets.json
"""

import os
import re
import json

SCRIPT_PATH = "uae_12min_production/directors_cut_script.json"
TIMESTAMPS_DIR = "uae_12min_production/audio/word_timestamps"
OUTPUT_PATH = "uae_12min_production/scene_beat_sheets.json"

# Character entrance triggers
CHAR_TRIGGERS = {
    "british_officer": [
        "british", "royal", "navy", "officer", "angrez", "general", "treaty",
        "pirate", "1820", "1853", "1892", "force", "ships", "protection"
    ],
    "inventor_mikimoto": [
        "mikimoto", "japan", "japanese", "cultured", "artificial", "lab",
        "scientist", "pearls", "moti", "entry"
    ],
    "sheikh_rashid": [
        "rashid", "dubai", "creek", "vision", "bhai", "ruler", "together",
        "unite", "union", "port", "jebel"
    ],
    "sheikh_zayed": [
        "zayed", "father", "leader", "abudhabi", "abu", "dhabi", "union",
        "unite", "nation", "federation", "soil", "ret"
    ],
    "pearl_diver": [
        "diver", "pearl", "bedouin", "samundar", "moti", "poverty", "dates",
        "camel", "hungry", "sea", "dive", "chappal", "garmi"
    ],
    "robot_minister": [
        "robot", "ai", "minister", "future", "tech", "technology", "smart",
        "digital", "2071", "innovation"
    ]
}

PROP_TRIGGERS = {
    "crash_board": ["crash", "zero", "mitti", "keemat", "poverty", "khatam", "loss", "market", "collapse", "game", "tarse"],
    "treaty_table": ["treaty", "sign", "peace", "agreement", "accord", "shanti", "1820", "1853", "1892", "dastakhat", "border", "truce"],
    "british_warship": ["warship", "jahaz", "navy", "fleet", "sea", "bombardment", "golabari", "1819", "power"],
    "uae_flag_hoist": ["flag", "jhanda", "unfurl", "union", "unite", "1971", "azadi", "ek", "together", "official"],
    "airplane_emirates": ["emirates", "airline", "fly", "plane", "airport", "duniya", "international", "sky", "aviation", "global"],
    "burj_khalifa_tower": ["burj", "khalifa", "tallest", "building", "tower", "record", "sky", "skyscrapers", "modern"],
    "palm_jumeirah": ["palm", "island", "jumeirah", "samundar", "ret", "sand", "man-made", "sea"],
    "supercar": ["car", "police", "lamborghini", "ferrari", "supercar", "fast", "speed", "highway"],
    "mars_hope_orbiter": ["hope", "probe", "mars", "space", "orbit", "mission", "satellite", "red", "planet", "science"],
    "karak_chai_glass": ["karak", "chai", "tea", "hold", "cup", "sip", "pi", "khatam"],
    "oil_valve_giant": ["valve", "reliance", "bye", "khatam", "band", "turn"],
    "solar_farm_panel": ["solar", "farm", "dunes", "panel", "desert", "renewable"],
    "nuclear_atom_plant": ["nuclear", "barakah", "plant", "atom", "power"],
    "crying_oil_barrel": ["barrel", "crying", "tears", "sad", "oil", "khatam", "game"],
    "glowing_blueprint_map": ["blueprint", "plan", "super", "emirates", "map", "deal", "sign"],
    "dallah_coffee_pot": ["coffee", "dallah", "tent", "chai", "pi", "cup"],
    "giant_oyster_pearl": ["oyster", "pearl", "moti", "jackpot", "sea", "dive"],
    "pirate_ship_eyepatch": ["pirate", "ship", "loot", "sea", "attack"],
    "burj_al_arab_hotel": ["burj", "arab", "hotel", "luxury", "sail"],
    "robotic_camel_mars": ["robotic", "camel", "mars", "2117", "astronaut"],
    "money_mattress_cash": ["mattress", "cash", "stacks", "needle", "paisa"],
    "water_well_dripping": ["well", "water", "dripping", "brawl", "tribes"],
    "rubber_stamp_treaty": ["stamp", "slams", "treaty", "red", "seal"],
    "oil_lantern_tent": ["lantern", "night", "fire", "tent", "star"]
}

STAMP_TRIGGERS = {
    9: {"text": "BRITISH TREATY (1820)", "color": [251, 197, 49], "words": ["treaty", "shanti", "galti", "rakhenge", "1820", "pirates"]},
    10: {"text": "MARITIME TRUCE (1853)", "color": [251, 197, 49], "words": ["truce", "peace", "treaty", "1853", "samundar", "shanti"]},
    16: {"text": "EXCLUSIVITY ACCORD (1892)", "color": [251, 197, 49], "words": ["deal", "treaty", "british", "accord", "exclusive", "1892"]},
    21: {"text": "UAE UNION ACCORD (1971)", "color": [46, 204, 113], "words": ["flag", "unfurl", "united", "emirates", "union", "announcement", "1971"]}
}

RIGHT_SIDE_PROPS = {
    "oil_derrick_monumental", "burj_khalifa_tower", "palm_jumeirah",
    "solar_farm_panel", "nuclear_atom_plant", "pirate_ship_eyepatch",
    "money_mattress_cash", "water_well_dripping", "burj_al_arab_hotel",
    "crying_oil_barrel"
}

LEFT_SIDE_PROPS = {"crash_board"}


def find_word_time(words_list, query_words, min_time=0.3):
    query_set = set(w.lower() for w in query_words)
    for item in words_list:
        if item["start"] < min_time:
            continue
        clean_w = re.sub(r'[^\w]', '', item["word"].lower())
        for q in query_set:
            if q in clean_w or clean_w in q:
                return item["start"]
    return None


def generate_beat_sheets(script_path=SCRIPT_PATH, timestamps_dir=TIMESTAMPS_DIR, output_path=OUTPUT_PATH):
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)

    scenes = script_data.get("scenes", [])
    beat_sheets = {}

    print(f"🎬 Generating narrative-aware, collision-free action beat sheets for {len(scenes)} scenes...")

    for sc in scenes:
        sc_num = sc["scene_number"]
        sc_dur = float(sc.get("duration", 14.0))
        chars = sc.get("characters", [])
        props = sc.get("props", [])
        env = sc.get("environment", "desert_dunes")

        words_file = os.path.join(timestamps_dir, f"scene_{sc_num}_words.json")
        words_list = []
        if os.path.exists(words_file):
            try:
                with open(words_file, "r", encoding="utf-8") as f:
                    words_list = json.load(f)
            except Exception:
                pass

        speech_intervals = [[w["start"], w["end"]] for w in words_list]

        # ---------------- Stage Zoning & Collision Avoidance ----------------
        has_right_prop = any(p in RIGHT_SIDE_PROPS for p in props)
        has_left_prop = any(p in LEFT_SIDE_PROPS for p in props)

        char_beats = {}
        n_chars = len(chars)

        for c_idx, char_id in enumerate(chars):
            # Dynamic Collision-Free Staging:
            if n_chars == 1:
                if env == "ocean_underwater":
                    anchor = [720, 680]
                elif has_right_prop:
                    # Prop is on right (1200+); character MUST be on left (480) looking right!
                    anchor = [480, 810]
                elif has_left_prop:
                    # Prop is on left; character MUST be on right (1440)!
                    anchor = [1440, 810]
                else:
                    # No side conflicts: if props exist, place left 480, else center 960
                    anchor = [480, 810] if props else [960, 810]
            elif n_chars == 2:
                # 2-character scenes: Left (480) & Right (1440), props in center (960)
                anchor = [480, 810] if c_idx == 0 else [1440, 810]
            else:
                spacing = 1600 // (n_chars + 1)
                anchor = [160 + (c_idx + 1) * spacing, 810]

            # Entrance style & timing
            enter_time = 0.0
            enter_style = "present"

            if char_id == "inventor_mikimoto":
                t_m = find_word_time(words_list, CHAR_TRIGGERS["inventor_mikimoto"], min_time=1.0)
                enter_time = t_m if t_m is not None else 2.5
                enter_style = "slide_from_left"
            elif char_id == "british_officer" and n_chars > 1:
                t_o = find_word_time(words_list, CHAR_TRIGGERS["british_officer"], min_time=0.8)
                enter_time = t_o if t_o is not None else 1.2
                enter_style = "slide_from_left"
            elif char_id == "robot_minister":
                t_r = find_word_time(words_list, CHAR_TRIGGERS["robot_minister"], min_time=1.0)
                enter_time = t_r if t_r is not None else 5.8
                enter_style = "slide_from_right"
            elif char_id == "sheikh_rashid" and "sheikh_zayed" in chars and sc_num != 48:
                t_rashid = find_word_time(words_list, CHAR_TRIGGERS["sheikh_rashid"], min_time=0.8)
                enter_time = t_rashid if t_rashid is not None else 2.7
                enter_style = "slide_from_left"

            # Narrative reactions
            reactions = []
            if sc_num == 1 and char_id == "pearl_diver":
                t_f = find_word_time(words_list, ["chappal", "pighal", "garmi", "faints"], min_time=2.0)
                reactions.append({"time": t_f if t_f is not None else 4.5, "type": "faint", "expression": "shocked"})
            elif sc_num == 2 and char_id == "pearl_diver":
                t_j = find_word_time(words_list, ["jackpot", "moti", "meeting", "shark"], min_time=3.0)
                reactions.append({"time": t_j if t_j is not None else 4.0, "type": "happy", "expression": "happy"})
            elif sc_num == 3 and char_id == "pearl_diver":
                t_s = find_word_time(words_list, ["artificial", "cultured", "palat", "game"], min_time=4.0)
                reactions.append({"time": t_s if t_s is not None else 5.5, "type": "shocked", "expression": "shocked"})
            elif sc_num == 4 and char_id == "pearl_diver":
                t_c = find_word_time(words_list, ["crash", "zero", "mitti", "tarse", "poverty"], min_time=2.0)
                reactions.append({"time": t_c if t_c is not None else 3.5, "type": "faint", "expression": "shocked"})
            elif sc_num in [20, 21, 22, 39, 48]:
                t_u = find_word_time(words_list, ["flag", "unfurl", "history", "united", "union"], min_time=1.5)
                reactions.append({"time": t_u if t_u is not None else 3.0, "type": "happy", "expression": "happy"})

            char_beats[char_id] = {
                "anchor_target": anchor,
                "enter_time": round(enter_time, 2),
                "enter_style": enter_style,
                "reactions": reactions
            }

        # Props configurations
        prop_beats = []
        for p in props:
            p_enter = 0.0
            p_style = "present"
            if p in ["crash_board", "treaty_table", "rubber_stamp_treaty"]:
                t_p = find_word_time(words_list, PROP_TRIGGERS.get(p, []), min_time=0.8)
                p_enter = t_p if t_p is not None else 1.5
                p_style = "slam_from_top"
            elif p in ["airplane_emirates", "supercar"]:
                t_p = find_word_time(words_list, PROP_TRIGGERS.get(p, []), min_time=0.8)
                p_enter = t_p if t_p is not None else 1.0
                p_style = "fly_through"
            elif p in ["burj_khalifa_tower", "solar_farm_panel"]:
                t_b = find_word_time(words_list, PROP_TRIGGERS.get(p, []), min_time=0.5)
                p_enter = t_b if t_b is not None else 0.5
                p_style = "grow_skywards"
            elif p in ["crying_oil_barrel", "karak_chai_glass", "oil_valve_giant"]:
                t_p = find_word_time(words_list, PROP_TRIGGERS.get(p, []), min_time=0.4)
                p_enter = t_p if t_p is not None else 0.0
                p_style = "pop_up"

            prop_beats.append({
                "name": p,
                "enter_time": round(p_enter, 2),
                "style": p_style
            })

        # Rubber Stamp configuration
        stamp_config = None
        if sc_num in STAMP_TRIGGERS:
            st = STAMP_TRIGGERS[sc_num]
            t_s = find_word_time(words_list, st["words"], min_time=1.0)
            stamp_time = t_s if t_s is not None else round(sc_dur * 0.5, 2)
            stamp_config = {
                "text": st["text"],
                "color": st["color"],
                "center": [960, 380],
                "time": round(stamp_time, 2)
            }

        # UPGRADE 4: 2.5D Virtual Camera Choreography
        if any(p in ["oil_derrick_monumental", "burj_khalifa_tower", "crying_oil_barrel", "nuclear_atom_plant"] for p in props):
            camera_preset = "dramatic_reveal_pullback"
        elif n_chars >= 2 or env in ["union_house", "treaty_room", "map_uae"]:
            camera_preset = "slow_pan_across_stage"
        else:
            camera_preset = "slow_cinematic_push_in"

        camera_config = {
            "preset": camera_preset,
            "target": "speaker" if n_chars == 1 else "stage"
        }

        beat_sheets[str(sc_num)] = {
            "scene_number": sc_num,
            "duration": sc_dur,
            "environment": env,
            "characters": char_beats,
            "props": prop_beats,
            "camera": camera_config,
            "stamp": stamp_config,
            "speech_intervals": speech_intervals
        }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(beat_sheets, f, indent=2, ensure_ascii=False)

    print(f"✅ Beat sheet successfully generated with {len(beat_sheets)} scenes saved to {output_path}")
    return beat_sheets


if __name__ == "__main__":
    generate_beat_sheets()
