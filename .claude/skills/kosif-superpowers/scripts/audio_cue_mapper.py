#!/usr/bin/env python3
"""Measure objective audio events in PCM WAV; import (never invent) aligned words.

This is a KOSIF-original, standard-library adapter. It estimates amplitude changes,
not musical tempo, vocal emotion, lyrics, instrument identity or musical meaning.
Do not promote a peak to a verified beat without a dedicated estimator and QA.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import statistics
import struct
import wave

MAX_SECONDS = 120
MAX_FILE_BYTES = 64 * 1024 * 1024
WINDOW_MS = 50


def finite_number(value, label, low=0.0, high=MAX_SECONDS):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{label} must be finite numeric')
    value=float(value)
    if not (low <= value <= high):
        raise ValueError(f'{label} out of range')
    return value


def measure_wav(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError('existing WAV under 64 MB required')
    try:
        with wave.open(str(path), 'rb') as stream:
            channels, width, rate, frames = (stream.getnchannels(), stream.getsampwidth(), stream.getframerate(), stream.getnframes())
            if stream.getcomptype() != 'NONE' or width != 2 or channels not in (1,2) or not (8000 <= rate <= 192000):
                raise ValueError('only uncompressed 16-bit mono/stereo PCM WAV 8–192 kHz is supported')
            duration = frames / rate
            if not (0.1 <= duration <= MAX_SECONDS):
                raise ValueError('audio must be 0.1–120 seconds')
            window_size=max(1,round(rate*WINDOW_MS/1000))
            values=[]
            while True:
                chunk=stream.readframes(window_size)
                if not chunk:
                    break
                if len(chunk) % (2*channels):
                    raise ValueError('truncated PCM frame')
                samples=struct.unpack('<'+'h'*(len(chunk)//2),chunk)
                if not samples: break
                # Average all samples over channels, with no dynamic compression.
                rms=math.sqrt(sum(s*s for s in samples)/len(samples))/32768.0
                values.append(round(rms,7))
    except (wave.Error, EOFError, struct.error) as exc:
        raise ValueError('invalid or unsupported WAV file') from exc
    if not values:
        raise ValueError('empty waveform')
    # Rising-energy boundaries are onset *candidates*, not confirmed musical beats.
    med=statistics.median(values)
    rising=[]
    previous=0.0
    refractory=0.12
    for idx,val in enumerate(values):
        t=idx*window_size/rate
        jump=val-previous
        if (jump > max(0.025, med*0.8) and val>max(0.04,med*1.45)
                and (not rising or t-rising[-1]>=refractory)):
            rising.append(round(t,3))
        previous=val
    return {
        'schema':'kosif.audio-cues.v1', 'source':path.name,
        'duration':round(duration,6),'sample_rate':rate,'channels':channels,
        'window_seconds':round(window_size/rate,8),
        'energy_rms':values,'energy_median':round(med,7),
        'onset_candidates_seconds':rising[:600],
        'bpm':None,'emotion':None,'verified_beats':False,
        'scope':'amplitude and candidate transients only; original audio is not modified',
        'master_clock':'source WAV duration',
    }


def _clean_word(raw):
    if not isinstance(raw,dict): raise ValueError('word must be object')
    spelling=raw.get('word',raw.get('text'))
    if not isinstance(spelling,str) or not spelling.strip() or len(spelling)>120 or any(ord(c)<32 for c in spelling):
        raise ValueError('invalid word text')
    start=finite_number(raw.get('start'),'word start')
    end=finite_number(raw.get('end'),'word end')
    if end <= start: raise ValueError('word ends before it starts')
    return {'text':spelling.strip(),'start':round(start,6),'end':round(end,6)}


def import_aligned_words(path, duration):
    """Import WhisperX segments[].words or existing KOSIF words[], rejecting missing times."""
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(data,dict) and isinstance(data.get('words'),list):
        records=data['words']
    elif isinstance(data,dict) and isinstance(data.get('segments'),list):
        records=[]
        for item in data['segments']:
            if not isinstance(item,dict) or not isinstance(item.get('words'),list):
                raise ValueError('each segment requires words[] with timestamps')
            records.extend(item['words'])
    else:
        raise ValueError('expected words[] or segments[].words[]')
    if len(records)>1500: raise ValueError('too many words')
    duration=finite_number(duration,'audio duration',0.1,MAX_SECONDS)
    ordered=[]
    previous=0
    for item in records:
        word=_clean_word(item)
        if word['start'] < previous-1e-5 or word['end'] > duration+1e-5:
            raise ValueError('word overlap, time reversal or exceeds audio')
        previous=word['end']
        ordered.append(word)
    return ordered


def write_json_new(path,data):
    p=Path(path)
    if not p.parent.is_dir(): raise ValueError('output parent directory missing')
    with p.open('x',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
        f.write('\n')


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('audio',help='PCM WAV (16-bit, mono/stereo)')
    ap.add_argument('--aligned-words',help='Word timings from WhisperX/KOSIF JSON (optional)')
    ap.add_argument('--out',required=True,help='Fresh JSON output path')
    args=ap.parse_args(argv)
    try:
        result=measure_wav(args.audio)
        result['words']=import_aligned_words(args.aligned_words,result['duration']) if args.aligned_words else []
        result['word_alignment_source']='user_supplied_external_timing' if args.aligned_words else 'none'
        write_json_new(args.out,result)
    except (ValueError,FileNotFoundError,OSError,json.JSONDecodeError) as exc:
        ap.error(str(exc))
    print(json.dumps({'output':args.out,'duration':result['duration'],
                      'onset_candidates':len(result['onset_candidates_seconds']),
                      'aligned_words':len(result['words']),
                      'bpm_verified':False,'emotion_inferred':False},ensure_ascii=False))


if __name__=='__main__':main()