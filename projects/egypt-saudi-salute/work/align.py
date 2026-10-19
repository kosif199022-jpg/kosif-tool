import json, re, difflib
W = json.load(open('work/whisper_turbo.json'))
ww = [w for s in W for w in s['words'] if w['word'].strip()]
def norm(s):
    s = re.sub(r'[ً-ْـ.,:!؟?…]', '', s)
    s = re.sub('[أإآ]', 'ا', s).replace('ة', 'ه').replace('ى', 'ي')
    return s.strip()
lines, section = [], None
for raw in open('work/lyrics.txt', encoding='utf-8'):
    raw = raw.strip()
    if not raw: continue
    m = re.match(r'\[(.*?)\]', raw)
    if m:
        section = m.group(1).split(':')[0].strip(); continue
    lines.append({'section': section, 'text': raw, 'words': raw.replace('...', ' ').split()})
ow = [(li, w) for li, L in enumerate(lines) for w in L['words']]
a = [norm(w) for _, w in ow]; b = [norm(w['word']) for w in ww]
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
t = [None] * len(ow)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == 'equal':
        for k in range(i2 - i1): t[i1 + k] = (ww[j1 + k]['start'], ww[j1 + k]['end'])
    elif op == 'replace' and j2 > j1:
        s0, s1 = ww[j1]['start'], ww[j2 - 1]['end']; n = i2 - i1
        for k in range(n): t[i1 + k] = (s0 + (s1 - s0) * k / n, s0 + (s1 - s0) * (k + 1) / n)
# fill gaps by interpolation
for i in range(len(t)):
    if t[i] is None:
        j = i
        while j < len(t) and t[j] is None: j += 1
        s0 = t[i - 1][1] if i else 0; s1 = t[j][0] if j < len(t) else s0 + 1
        n = j - i
        for k in range(n): t[i + k] = (s0 + (s1 - s0) * k / n, s0 + (s1 - s0) * (k + 1) / n)
        print('interp', [ow[i + k][1] for k in range(n)], round(s0, 2), round(s1, 2))
k = 0; out = []
for li, L in enumerate(lines):
    words = []
    for w in L['words']:
        words.append({'word': w, 'start': round(t[k][0], 3), 'end': round(t[k][1], 3)}); k += 1
    out.append({'section': L['section'], 'text': L['text'], 'start': words[0]['start'], 'end': words[-1]['end'], 'words': words})
    print(f"{words[0]['start']:7.2f} {words[-1]['end']:7.2f} [{L['section']}] {L['text']}")
json.dump(out, open('work/lines.json', 'w'), ensure_ascii=False, indent=1)
flat = [w for L in out for w in L['words']]
json.dump(flat, open('words.json', 'w'), ensure_ascii=False, indent=1)
