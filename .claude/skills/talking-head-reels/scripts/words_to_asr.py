#!/usr/bin/env python3
"""KOSIF addition: use a kosif-voice-studio transcript instead of faster-whisper.

    python3 scripts/words_to_asr.py PROJECT_DIR words.json [--gap 0.6]

words.json is `[{word, start, end}]` in source seconds (kosif-voice-studio `transcribe`,
or any word-timed transcript in that shape). Writes analysis/asr.json in the shape
transcribe.py writes, so cut_pauses.py and the rest of the pipeline run unchanged.
A new segment starts after sentence punctuation (. ! ? ؟) or a silence longer than --gap.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_json, project_config, save_json  # noqa: E402

ENDS = ('.', '!', '?', '؟', '…')


def convert(words, gap=0.6):
    rows = []
    for w in words:
        text = str(w.get('word', w.get('w', ''))).strip()
        s, e = float(w.get('start', w.get('s'))), float(w.get('end', w.get('e')))
        if not text or e < s:
            raise ValueError('bad word entry: %r' % (w,))
        rows.append(dict(s=round(s, 3), e=round(e, 3), w=' ' + text, p=float(w.get('p', 1.0))))
    rows.sort(key=lambda r: r['s'])
    segs, cur = [], []
    for r in rows:
        if cur and (r['s'] - cur[-1]['e'] > gap or cur[-1]['w'].rstrip().endswith(ENDS)):
            segs.append(cur)
            cur = []
        cur.append(r)
    if cur:
        segs.append(cur)
    return [dict(start=c[0]['s'], end=c[-1]['e'], text=''.join(r['w'] for r in c), words=c) for c in segs]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('project')
    ap.add_argument('words')
    ap.add_argument('--gap', type=float, default=0.6, help='silence (s) that starts a new segment')
    ap.add_argument('--language', default=None, help='language code stored in project.json, e.g. ar')
    a = ap.parse_args()
    cfg = project_config(a.project)
    data = load_json(a.words)
    if isinstance(data, dict):
        data = data.get('words') or []
    if not data:
        sys.exit('ERROR: no words in ' + a.words)
    segs = convert(data, a.gap)
    save_json(segs, os.path.join(cfg['project_dir'], 'analysis', 'asr.json'))
    if a.language:
        cfg['language'] = a.language
        save_json(cfg, os.path.join(cfg['project_dir'], 'project.json'))
    for s in segs:
        print('%6.2f-%6.2f%s' % (s['start'], s['end'], s['text']))
    print('\nsegments: %d   words: %d' % (len(segs), sum(len(s['words']) for s in segs)))


if __name__ == '__main__':
    main()
