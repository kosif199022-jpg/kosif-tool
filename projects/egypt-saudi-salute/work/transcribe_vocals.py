import json, sys
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2], device="cpu", compute_type="int8", cpu_threads=4)
prompt = "يا مصر وصلتنا تحيتكم. حييتونا يا مصر والرد منا بأحسن من التحية هذا علومنا"
import wave, numpy as np; _w=wave.open("work/vocals16k.wav"); a=np.frombuffer(_w.readframes(_w.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs, info = m.transcribe(a, language="ar", word_timestamps=True, beam_size=5, initial_prompt=prompt, condition_on_previous_text=False, vad_filter=False)
out = []
for s in segs:
    print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text}", flush=True)
    out.append({"start": s.start, "end": s.end, "text": s.text, "words": [{"word": w.word.strip(), "start": w.start, "end": w.end, "p": w.probability} for w in (s.words or [])]})
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("DONE")
