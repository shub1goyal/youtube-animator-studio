import os
import json
import time
from pathlib import Path
from faster_whisper import WhisperModel

def align_all_scenes(scenes_dir="production/audio", output_dir="production/audio/word_timestamps", num_scenes=48, prompt_hint="Hindi Hinglish educational history documentary."):
    os.makedirs(output_dir, exist_ok=True)
    
    print("Loading faster-whisper 'base' model on CPU (int8)...")
    t0 = time.time()
    model = WhisperModel("base", device="cpu", compute_type="int8")
    print(f"Model loaded in {time.time()-t0:.2f}s")
    
    results = {}
    total_words = 0
    
    for sc_num in range(1, num_scenes + 1):
        out_file = os.path.join(output_dir, f"scene_{sc_num}_words.json")
        audio_file = os.path.join(scenes_dir, f"scene_{sc_num}.wav")
        
        if not os.path.exists(audio_file):
            print(f"Warning: Audio file {audio_file} not found, skipping.")
            continue
            
        # Check if already processed
        if os.path.exists(out_file) and os.path.getsize(out_file) > 10:
            try:
                with open(out_file, "r", encoding="utf-8") as f:
                    words_data = json.load(f)
                if len(words_data) > 0:
                    print(f"Scene {sc_num:02d}: Already cached ({len(words_data)} words)")
                    results[sc_num] = words_data
                    total_words += len(words_data)
                    continue
            except Exception:
                pass
                
        print(f"Scene {sc_num:02d}: Transcribing {audio_file}...")
        t_sc = time.time()
        try:
            segments, info = model.transcribe(
                audio_file,
                word_timestamps=True,
                initial_prompt=prompt_hint
            )
            
            words_data = []
            for segment in segments:
                for word in segment.words:
                    words_data.append({
                        "word": word.word.strip(),
                        "start": round(word.start, 2),
                        "end": round(word.end, 2),
                        "probability": round(word.probability, 2)
                    })
            
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(words_data, f, indent=2, ensure_ascii=False)
                
            elapsed = time.time() - t_sc
            print(f"  -> Extracted {len(words_data)} words in {elapsed:.2f}s")
            results[sc_num] = words_data
            total_words += len(words_data)
        except Exception as e:
            print(f"  -> Error transcribing Scene {sc_num}: {e}")
            
    print(f"\n==========================================")
    print(f"Alignment Complete: Processed {len(results)} scenes, {total_words} total words.")
    print(f"Timestamps saved in {output_dir}")
    print(f"==========================================")
    return results

if __name__ == "__main__":
    align_all_scenes()

