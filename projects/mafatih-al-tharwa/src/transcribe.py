import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2], device="cpu", compute_type="int8", cpu_threads=4)
import numpy as np, wave
wf=wave.open(sys.argv[1]); audio=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs, info = m.transcribe(audio, word_timestamps=True, beam_size=5, vad_filter=True, language=None)
print("lang", info.language, info.language_probability, flush=True)
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text.strip(),"words":[{"w":w.word.strip(),"start":round(w.start,3),"end":round(w.end,3),"p":round(w.probability,3)} for w in s.words]})
    print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text}", flush=True)
json.dump({"language":info.language,"segments":out}, open(sys.argv[3],"w"), ensure_ascii=False, indent=1)
