# Forced alignment of the official lyrics on the isolated vocal stem (torchaudio MMS_FA + uroman).
import json, re, wave, numpy as np, torch, torchaudio, uroman as ur
from torchaudio.pipelines import MMS_FA as B
u = ur.Uroman(); model = B.get_model(with_star=True).eval(); tok = B.get_tokenizer(); aligner = B.get_aligner()
DICT = B.get_dict(star='*')
w = wave.open('work/vocals16k.wav'); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
A = json.load(open('work/lines_v.json')); SR = 16000
def rom(word):
    s = u.romanize_string(re.sub(r'[ً-ْـ.,:!؟?…]', '', word)).lower()
    s = ''.join(c for c in s if c in DICT and c != '*')
    return s or 'a'
out = []
for i, L in enumerate(A):
    t0 = max(0, L['start'] - 1.0); t1 = min(len(a) / SR, L['end'] + 0.8)
    if i + 1 < len(A): t1 = min(t1, A[i + 1]['start'] + 0.6)
    seg = torch.from_numpy(a[int(t0 * SR):int(t1 * SR)].copy())[None]
    with torch.inference_mode(): em, _ = model(seg)
    words = ['*'] + [rom(x['word']) for x in L['words']] + ['*']
    spans = aligner(em[0], tok(words))
    ratio = seg.shape[1] / em.shape[1] / SR
    nw = []
    for x, sp in zip(L['words'], spans[1:-1]):
        s, e = t0 + sp[0].start * ratio, t0 + sp[-1].end * ratio
        sc = float(np.mean([q.score for q in sp]))
        nw.append({'word': x['word'], 'start': round(s, 3), 'end': round(e, 3), 'score': round(sc, 3), 'whisper': x['start']})
    out.append({**L, 'start': nw[0]['start'], 'end': nw[-1]['end'], 'words': nw})
    d = nw[0]['start'] - L['start']
    print(f"{L['start']:7.2f} -> {nw[0]['start']:7.2f} ({d:+.2f})  score={np.mean([q['score'] for q in nw]):.2f}  {L['text'][:28]}")
json.dump(out, open('work/lines_fa.json', 'w'), ensure_ascii=False, indent=1)
