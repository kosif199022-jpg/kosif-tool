import sys, json, numpy as np, wave
from faster_whisper import WhisperModel
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
wf=wave.open("work/voice16.wav"); a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768
res={}
for t0,t1 in [(214.0,227.0),(261.0,267.0),(116.0,118.2),(155.8,158.4)]:
    segs,_=m.transcribe(a[int(t0*16000):int(t1*16000)], language="ar", word_timestamps=True, vad_filter=False, beam_size=5, condition_on_previous_text=False)
    ws=[]
    for s in segs:
        for w in s.words: ws.append({"w":w.word.strip(),"start":round(w.start+t0,3),"end":round(w.end+t0,3),"p":round(w.probability,3)})
    res[f"{t0}-{t1}"]=ws; print(t0,t1," ".join(f"{w['w']}({w['start']})" for w in ws), flush=True)
json.dump(res,open("work/fill.json","w"),ensure_ascii=False,indent=1)
