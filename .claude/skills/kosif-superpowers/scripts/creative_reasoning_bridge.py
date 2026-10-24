#!/usr/bin/env python3
"""Turn measured audio cues + user-aligned words into a reproducible KOSIF SVG storyboard.

The decision is deterministic and audit-able, NOT automatic interpretation of lyrics,
not a neural model or a substitute for an art director. It uses no 3rd-party code.

Usage (from the skill folder; the cues come from audio_cue_mapper.py first):
  python3 scripts/audio_cue_mapper.py song.wav --out cues.json [--aligned-words words.json]
  python3 scripts/creative_reasoning_bridge.py cues.json --out storyboard.json --report report.json [--style auto|doodle|cinematic|kinetic] [--landscape]
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

SKILL=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(SKILL/'scripts'))
from audio_cue_mapper import finite_number, write_json_new  # noqa: E402
from motion_director import validate  # noqa: E402

STYLES={
 'doodle': {'color':'#355b47','background':'#f4f0e6','movement':105,'name':'hand-drawn explanatory'},
 'cinematic': {'color':'#d19b56','background':'#1b2530','movement':65,'name':'low-motion cinematic'},
 'kinetic': {'color':'#236b8b','background':'#f5f2ec','movement':190,'name':'kinetic typography'},
}

def _segments(duration, words):
    """Cut near natural word boundaries at <=9 seconds, without splitting a word."""
    parts=[]; current=0.0
    while current<duration-1e-6:
        target=min(duration,current+6.0)
        if target>=duration-1e-6: next_cut=duration
        else:
            # Never split a timed word. Prefer a gap, else put cut at word end.
            candidates=[w['end'] for w in words if current+2<=w['end']<=min(current+9,duration)]
            gaps=[]
            for i,w in enumerate(words[:-1]):
                n=words[i+1]
                if n['start']-w['end']>0.3 and current+2<=w['end']<=min(current+9,duration):
                    gaps.append(w['end'])
            preferred=gaps or candidates
            next_cut=min(preferred,key=lambda t:abs(t-target)) if preferred else target
            for w in words:
                if w['start']<next_cut<w['end']:
                    next_cut=w['end']
                    break
            if next_cut>duration:next_cut=duration
        if next_cut<=current+0.001:
            next_cut=duration
        parts.append((round(current,6),round(next_cut,6)))
        current=next_cut
        if len(parts)>30: raise ValueError('too many scenes')
    return parts


def _score_style(style, onset_rate, has_words):
    """Explicit design utility, not a prediction of emotional fit or true artistic quality."""
    base={'doodle':60,'cinematic':61,'kinetic':59}[style]
    fit=(min(12,round(onset_rate*5)) if style=='kinetic' else
         10 if style=='cinematic' and onset_rate<0.8 else
         9 if style=='doodle' and has_words else 2)
    legibility=10 if has_words and style!='kinetic' else 7
    execution=10 # all use the bundled SVG/HTML engine; MP4 dependencies separate
    return {'total':base+fit+legibility+execution,
            'factors':{'design_prior':base,'audio_activity_fit':fit,'legibility_prior':legibility,'local_svg_buildability':execution},
            'rubric':'hand-written deterministic heuristic; not a validated aesthetic score'}


def build_plan(cues, style='auto',width=1080,height=1920,fps=30):
    if not isinstance(cues,dict) or cues.get('schema')!='kosif.audio-cues.v1':
        raise ValueError('expected kosif.audio-cues.v1')
    duration=finite_number(cues.get('duration'),'duration',0.1,120)
    beats=cues.get('onset_candidates_seconds',[])
    words=cues.get('words',[])
    if not isinstance(beats,list) or not isinstance(words,list) or len(words)>1500 or len(beats)>600:
        raise ValueError('invalid cue arrays')
    if not isinstance(width,int) or not isinstance(height,int) or width not in (1080,1920) or height not in (1080,1920):
        raise ValueError('use 1080x1920 or 1920x1080')
    for b in beats:
        finite_number(b,'onset candidate',0,duration)
    prev=0
    for w in words:
        if not isinstance(w,dict) or not isinstance(w.get('text'),str) or not w['text'].strip():raise ValueError('invalid timed word')
        a=finite_number(w.get('start'),'word start',0,duration)
        e=finite_number(w.get('end'),'word end',0,duration)
        if a<prev-1e-5 or e<=a: raise ValueError('overlapping or reversed words')
        prev=e
    if style not in {'auto',*STYLES}:raise ValueError('unsupported style')
    rate=len(beats)/duration
    reviews={s:_score_style(s,rate,bool(words)) for s in STYLES}
    chosen=max(STYLES,key=lambda s:(reviews[s]['total'],-list(STYLES).index(s))) if style=='auto' else style
    settings=STYLES[chosen]
    intervals=_segments(duration,words)
    scenes=[]
    for idx,(start,end) in enumerate(intervals):
        scene_words=[dict(w) for w in words if w['start']>=start-1e-5 and w['end']<=end+1e-5]
        label=' '.join(w['text'] for w in scene_words[:7])[:120] or 'حركة متزامنة مع الصوت'
        if len(label)>110:label=label[:109]
        # All element timing derived from actual audio boundaries; never invented word timestamps.
        reveal_end=min(end,start+1.5)
        movement=min(settings['movement'],width*0.25)
        camzoom=1.03 if chosen=='cinematic' else 1.07
        elements=[
            {'type':'text','text':label,'x':width//2,'y':int(height*0.23),'fontSize':64 if width<height else 58,
             'start':start,'end':reveal_end,'fill':settings['color']},
            {'type':'path','d':f'M {int(width*.15)} {int(height*.52)} C {int(width*.32)} {int(height*.46)} {int(width*.6)} {int(height*.62)} {int(width*.85)} {int(height*.49)}',
             'start':start+min(0.1,(end-start)*.1),'end':min(end,start+2.5),
             'stroke':settings['color'],'strokeWidth':8},
        ]
        if end-start>=1.2:
            elements.append({'type':'character','x':int(width*.50),'y':int(height*.69),'scale':1.6,
                             'start':start,'end':min(end,start+1.1),
                             'move':{'fromX':-movement,'toX':movement,'start':min(end,start+1.1),'end':end}})
        scenes.append({'id':f'scene_{idx+1:02d}','start':start,'end':end,
                       'background':settings['background'],
                       'camera':{'fromZoom':1,'toZoom':camzoom,'start':start,'end':end},
                       'words':scene_words,'elements':elements})
    storyboard={'version':1,'width':width,'height':height,'fps':fps,'duration':duration,'scenes':scenes}
    validated=validate(storyboard)
    return {'schema':'kosif.creative-plan.v1','decision':{
                'chosen_style':chosen,'style_override':style!='auto',
                'options':reviews,'reason':f'{chosen} won the declared heuristic' if style=='auto' else 'user selected style',
                'limitations':['amplitude onsets are not beat verification',
                               'semantic/emotional meaning is not inferred',
                               'a passing schema does not prove visual or MP4 quality']},
            'evidence':{'source_audio':cues.get('source'),
                        'audio_duration':duration,'aligned_word_count':len(words),
                        'onset_candidates':len(beats), 'original_audio_untouched':True},
            'validated_storyboard':validated,'storyboard':storyboard,
            'render_status':'unrendered_storyboard'}


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('cues',help='JSON generated by audio_cue_mapper.py')
    ap.add_argument('--style',default='auto',choices=['auto',*STYLES])
    ap.add_argument('--out',required=True,help='New editable storyboard JSON')
    ap.add_argument('--report',required=True,help='New decision/audit report JSON')
    ap.add_argument('--landscape',action='store_true')
    args=ap.parse_args(argv)
    try:
        cues=json.loads(Path(args.cues).read_text(encoding='utf-8'))
        result=build_plan(cues,args.style,1920 if args.landscape else 1080,
                          1080 if args.landscape else 1920)
        out=Path(args.out).resolve(); report=Path(args.report).resolve()
        if out==report or out.exists() or report.exists() or not out.parent.is_dir() or not report.parent.is_dir():
            raise ValueError('two distinct unused output paths in existing directories required')
        write_json_new(out,result['storyboard'])
        write_json_new(report,{k:v for k,v in result.items() if k!='storyboard'})
        print(json.dumps({'storyboard':str(out),'report':str(report),
                          'selected':result['decision']['chosen_style'],
                          'validation':result['validated_storyboard'],'rendered':False},ensure_ascii=False))
    except (ValueError,OSError,json.JSONDecodeError) as exc:ap.error(str(exc))


if __name__=='__main__':main()