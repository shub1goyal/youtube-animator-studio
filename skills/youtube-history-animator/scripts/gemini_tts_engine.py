"""
gemini_tts_engine.py
Gemini 3.8 Flash TTS Engine with Automated Key Rotation & Hinglish Phonetics
Voice: Charon (or selectable)
Model: gemini-3.8-flash-tts

Features:
- Automatic key rotation across 20+ API keys from api_keys.json
- Handles 429 rate limits with automatic failover and backoff
- Intelligent Hinglish phonetic engine with strict English loanword protection
- Batch scene voiceover synthesis, concatenation, and EBU R128 loudness mastering
"""

import sys
import os
import json
import base64
import time
import re
import urllib.request
import urllib.error
import argparse
import subprocess

DEFAULT_KEYS_PATH = r"c:\Users\shubh\OneDrive\Desktop\animator\api_keys.json"
FFMPEG_PATH = r"C:\Users\shubh\AppData\Local\agy\bin\ffmpeg.exe"

# Common English words that must NEVER be mutated by Hindi phonetic rules
ENGLISH_PROTECTED_WORDS = {
    "extreme", "trade", "future", "safe", "state", "empire", "line", "time", "make",
    "huge", "space", "peace", "rule", "plane", "plate", "white", "live", "size", "type",
    "date", "zone", "strike", "game", "share", "police", "marine", "base", "side", "name",
    "route", "drive", "hope", "force", "close", "pride", "change", "large", "middle",
    "little", "simple", "battle", "treaty", "century", "history", "desert", "country",
    "people", "building", "supercar", "supercars", "billionaire", "billionaires",
    "millionaire", "millionaires", "million", "billion", "trillion", "dollar", "dollars",
    "port", "airport", "airline", "airlines", "hub", "oil", "field", "wells", "tank",
    "tanks", "ship", "ships", "boat", "boats", "dhow", "dhows", "market", "pearl", "pearls",
    "culture", "cultured", "natural", "price", "tag", "tags", "crash", "treaties", "coast",
    "trucial", "british", "britain", "england", "london", "navy", "fleet", "officer", "officers",
    "pirate", "pirates", "attack", "attacks", "contract", "contracts", "sign", "signed",
    "region", "regions", "sheikh", "sheikhs", "united", "arab", "emirates", "dubai",
    "abu", "dhabi", "sharjah", "ajman", "fujairah", "flag", "flags", "union", "accord",
    "house", "leader", "leaders", "founding", "father", "schools", "hospitals", "housing",
    "free", "healthcare", "education", "citizen", "citizens", "world", "global", "tourism",
    "tax", "zero", "income", "policy", "foreign", "ownership", "probe", "mission", "mars",
    "orbit", "satellite", "satellites", "solar", "panel", "panels", "antenna", "agency",
    "city", "cities", "tech", "technology", "ai", "artificial", "intelligence", "model",
    "models", "superpower", "superpowers", "channel", "video", "videos", "subscribe",
    "comment", "comments", "like", "share", "bell", "notification", "story", "stories",
    "secret", "secrets", "odd", "odds", "heat", "degree", "degrees", "celsius", "caravan",
    "camel", "camels", "falcon", "falcons", "gucci", "sunglasses", "lambo", "lamborghini",
    "bugatti", "gold", "plated", "liquid", "black", "ground", "fountain", "explosion",
    "coins", "shower", "chime", "fortune", "miracle", "megacity", "skyline", "skyscraper",
    "skyscrapers", "tallest", "burj", "khalifa", "jumeirah", "palm", "island", "center",
    "science", "grid", "shield", "research", "lead", "leading", "the", "some", "more",
    "like", "one", "have", "here", "there", "where", "before", "became", "came", "come",
    "give", "gave", "done", "gone", "take", "took", "rate", "rates", "case", "cases",
    "place", "places", "face", "faces", "cause", "course", "source", "role", "roles",
    "hole", "whole", "scale", "stage", "stages", "range", "voice", "choice", "note", "notes",
    "vote", "votes", "move", "moved", "movement", "prove", "proved", "improve", "improved"
}


class HinglishPhoneticEngine:
    def __init__(self):
        self.exact_word_map = {
            "main": "mayn", "mein": "mayn", "me": "mayn", "aap": "aap", "tum": "tum",
            "hum": "hum", "yeh": "yeh", "ye": "yay", "woh": "voh", "wo": "voh",
            "isne": "is-nay", "usne": "us-nay", "inhone": "in-ho-nay", "unhone": "un-ho-nay",
            "unka": "un-kaa", "unke": "un-kay", "unki": "un-kee", "apna": "up-naa",
            "apne": "up-nay", "apni": "up-nee", "sabka": "sub-kaa", "sabke": "sub-kay",
            "sabse": "sub-say", "kisi": "kee-see", "kisine": "kee-see-nay", "kuch": "kuchh",
            "kya": "kyaa", "kyun": "kyoon", "kaise": "kay-say", "kahan": "ka-haan",
            "aur": "aur", "lekin": "lay-kin", "magar": "muh-gur", "parantu": "puh-run-too",
            "kyunki": "kyoon-kee", "isliye": "is-lee-yay", "par": "pur", "se": "say",
            "ko": "ko", "tak": "tuk", "saath": "saath", "bina": "bee-naa", "ke": "kay",
            "ki": "kee", "ka": "kaa", "kare": "karay", "karega": "karay-ga",
            "karegi": "karay-gee", "karenge": "karayn-gay", "karta": "kartaa",
            "karti": "kartee", "karte": "kartay", "karo": "ka-ro", "kiya": "kee-yaa",
            "kiye": "kee-yay", "bheje": "bhay-jay", "bheja": "bhay-jaa", "chale": "chalay",
            "chala": "cha-laa", "chali": "cha-lee", "dekh": "daykh", "dekho": "day-kho",
            "dekha": "day-khaa", "dekhe": "day-khay", "dekhne": "daykh-nay", "soche": "so-chay",
            "socha": "so-chaa", "socho": "so-cho", "jaane": "jaa-nay", "jaate": "jaa-tay",
            "gaya": "ga-yaa", "gaye": "ga-yay", "gayi": "ga-yee", "aaye": "aa-yay",
            "aate": "aa-tay", "chahiye": "chaa-hi-yay", "chahie": "chaa-hi-yay",
            "hoga": "ho-gaa", "hogi": "ho-gee", "honge": "hon-gay", "hua": "hoo-aa",
            "hue": "hoo-ay", "hui": "hoo-ee", "hai": "hai", "hain": "hayn",
            "tha": "thaa", "the": "thay", "thi": "thee", "rehte": "reh-tay",
            "raha": "ra-haa", "rahe": "ra-hay", "rahi": "ra-hee", "bolte": "bol-tay",
            "bola": "bo-laa", "samjha": "su-muj-haa", "samjhe": "su-muj-hay",
            "rokne": "rok-nay", "nikalne": "nee-kul-nay", "milte": "mil-tay",
            "milti": "mil-tee", "mila": "mee-laa", "mile": "mee-lay", "badla": "bud-laa",
            "palat": "pu-lut", "chuki": "choo-kee", "chuka": "choo-kaa", "banaya": "ba-naa-yaa",
            "bana": "ba-naa", "banne": "bun-nay", "lagne": "lug-nay", "laga": "la-gaa",
            "khinch": "kheench", "batao": "ba-taa-o", "bhai": "bhaai", "bhaiya": "bhaa-ee-yaa",
            "dost": "dhost", "ret": "rayt", "samundar": "su-mun-dur", "garmi": "gur-mee",
            "mehnat": "meh-nut", "kangaal": "kun-gaal", "raato-raat": "raa-to-raat",
            "chote": "cho-tay", "chota": "cho-taa", "bade": "ba-day", "bada": "ba-daa",
            "desh": "daysh", "paisa": "py-saa", "paise": "py-say", "daulat": "dau-lut",
            "kismat": "kis-mut", "jugaad": "joo-gaad", "lafda": "luff-daa", "locha": "low-chaa",
            "fayda": "faa-y-daa", "pehle": "peh-lay", "baad": "baad", "hamesha": "ha-may-shaa",
            "achhi": "aach-chee", "accha": "aach-chaa", "agla": "ug-laa", "kahaani": "ka-haa-nee",
            "poora": "poo-raa", "poori": "poo-ree", "bohot": "boh-hut", "bahut": "boh-hut",
            "angrez": "ung-rayz", "shuru": "shoo-roo", "sirf": "sirf", "moti": "mo-tee"
        }

    def phonetize(self, text):
        words = text.split()
        transformed = []
        for w in words:
            m = re.match(r"^([^\w]*)([\w'-]+)([^\w]*)$", w)
            if not m:
                transformed.append(w)
                continue
            pre, core, post = m.groups()
            core_lower = core.lower()

            if core_lower in ENGLISH_PROTECTED_WORDS:
                transformed.append(f"{pre}{core}{post}")
                continue

            if core_lower in self.exact_word_map:
                phonetic = self.exact_word_map[core_lower]
                if core.istitle():
                    phonetic = phonetic.capitalize()
                transformed.append(f"{pre}{phonetic}{post}")
            else:
                word_p = core
                if len(core) >= 4 and any(core_lower.endswith(sfx) for sfx in ["te", "ne", "ke", "se", "che", "je", "ye"]):
                    word_p = core[:-1] + "ay"
                transformed.append(f"{pre}{word_p}{post}")

        return " ".join(transformed)


class GeminiTTSManager:
    def __init__(self, keys_file=DEFAULT_KEYS_PATH, model="gemini-3.8-flash-tts", voice="Charon"):
        self.keys_file = keys_file
        self.model = model
        self.voice = voice
        self.phonetic_engine = HinglishPhoneticEngine()

        with open(keys_file, "r") as f:
            raw_keys = json.load(f)
        fastest_first = ["AIzaSyD9NDYTDEtXkf41zHHuGO_qjpLdevCQFv0"]
        aiza_keys = [k for k in raw_keys if k.startswith("AIzaSy") and k not in fastest_first]
        other_keys = [k for k in raw_keys if not k.startswith("AIzaSy")]
        self.keys = fastest_first + aiza_keys + other_keys
        self.current_key_idx = 0

    def get_next_key(self):
        key = self.keys[self.current_key_idx]
        self.current_key_idx = (self.current_key_idx + 1) % len(self.keys)
        return key

    def synthesize(self, text, output_wav_path, max_retries=35):
        phonetic_text = self.phonetic_engine.phonetize(text)
        payload = {
            "contents": [{"parts": [{"text": phonetic_text}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": self.voice
                        }
                    }
                }
            }
        }
        data = json.dumps(payload).encode("utf-8")
        models_pool = [self.model, "gemini-2.5-flash-preview-tts", "gemini-3.1-flash-tts-preview"]

        for attempt in range(max_retries):
            api_key = self.get_next_key()
            masked_key = api_key[:8] + "..." + api_key[-4:]
            cur_model = models_pool[attempt % len(models_pool)]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{cur_model}:generateContent?key={api_key}"
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                t0 = time.time()
                with urllib.request.urlopen(req, timeout=30) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    elapsed = time.time() - t0
                    candidate = resp_data["candidates"][0]
                    part = candidate["content"]["parts"][0]
                    inline_data = part.get("inlineData") or part.get("inline_data")
                    audio_b64 = inline_data["data"]
                    audio_bytes = base64.b64decode(audio_b64)

                    # Ensure standard RIFF WAV format (headerless PCM to WAV container)
                    if not audio_bytes.startswith(b"RIFF"):
                        import io, wave
                        wav_buf = io.BytesIO()
                        with wave.open(wav_buf, "wb") as wf:
                            wf.setnchannels(1)
                            wf.setsampwidth(2)
                            wf.setframerate(24000)
                            wf.writeframes(audio_bytes)
                        audio_bytes = wav_buf.getvalue()

                    os.makedirs(os.path.dirname(os.path.abspath(output_wav_path)), exist_ok=True)
                    with open(output_wav_path, "wb") as f_out:
                        f_out.write(audio_bytes)

                    print(f"Synthesized voiceover [{self.voice}] -> {output_wav_path} ({elapsed:.2f}s, key: {masked_key})")
                    return output_wav_path
            except urllib.error.HTTPError as e:
                backoff = min(12.0, 1.5 * (1.4 ** (attempt % 6)))
                time.sleep(backoff)
            except Exception as e:
                time.sleep(1.0)

        raise RuntimeError(f"Failed to synthesize TTS after {max_retries} retries across keys.")

    def generate_scene_voiceovers(self, scenes, output_dir, mode="long_form"):
        """Synthesizes each scene's audio, stitches them, and masters to -14.0 LUFS (-12 LUFS shorts)."""
        os.makedirs(output_dir, exist_ok=True)
        wav_files = []
        for scene in scenes:
            num = scene.get("scene_number", 1)
            text = scene.get("vo_phonetic_tts") or scene.get("vo_hinglish", "")
            out_path = os.path.join(output_dir, f"scene_{num}.wav")
            self.synthesize(text, out_path)
            wav_files.append(out_path)

        # Stitch all scene wavs
        concat_txt = os.path.join(output_dir, "concat.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for w in wav_files:
                f.write(f"file '{w.replace(chr(92), '/')}'\n")

        raw_stitched = os.path.join(output_dir, "raw_stitched.wav")
        cmd_concat = [
            FFMPEG_PATH, "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", raw_stitched, "-y"
        ]
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Loudness mastering
        target_lufs = "-14.0" if mode == "long_form" else "-12.0"
        final_master = os.path.join(output_dir, "final_mastered_voiceover.wav")
        cmd_norm = [
            FFMPEG_PATH, "-i", raw_stitched,
            "-af", f"loudnorm=I={target_lufs}:TP=-1.0:LRA=7.0",
            final_master, "-y"
        ]
        subprocess.run(cmd_norm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Voiceover mastered to {target_lufs} LUFS: {final_master}")
        return final_master


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument("--out", required=True, help="Output WAV path")
    parser.add_argument("--voice", default="Charon", help="Gemini Voice Name")
    args = parser.parse_args()

    mgr = GeminiTTSManager(voice=args.voice)
    mgr.synthesize(args.text, args.out)
