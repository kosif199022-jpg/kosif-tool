#!/usr/bin/env python3
"""KOSIF footage-first editor: audited licensed-shot selection & deterministic edit plan.

This is an original implementation of a planning/export stage. It does NOT
download clips, detect imagery, synthesize subtitles, or render an MP4.
Rights/text/person flags must come from actual inspection, not inference.
"""
from __future__ import annotations
import argparse
import json
import math
import re
from pathlib import Path

SCHEMA = "kosif.edl.v1"
CAMERAS = ("slow_push_in", "gentle_pan_right", "slow_pull_back", "gentle_pan_left")
NUMBERS = re.compile(r"\d")
ARABIC_STOP = set("في من على الى إلى و عن هذا دي هو اللي مع ثم حتى كان هي".split())


def validate_words(words, duration):
    if not isinstance(words, list) or not words:
        raise ValueError("words must be a nonempty list")
    last_start = -1.0
    for i, w in enumerate(words):
        if not isinstance(w, dict):
            raise ValueError(f"word {i} must be an object")
        start, end = float(w["start"]), float(w["end"])
        if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end <= duration + 0.001):
            raise ValueError(f"invalid timestamp at word {i}")
        if start < last_start:
            raise ValueError("words must be in ascending order")
        last_start = start
        if not (str(w.get("word") or w.get("text") or "").strip()):
            raise ValueError(f"word {i} is empty")


def to_tokens(s):
    return set(x for x in re.findall(r"[\w\u0600-\u06FF]+", str(s).casefold())
               if len(x) > 1 and x not in ARABIC_STOP)


def clean_clip(c):
    needed = ("id", "path", "duration", "width", "height", "license_verified",
              "reviewed_frames", "contains_text", "contains_excluded_people",
              "is_moving_video")
    if not all(k in c for k in needed):
        return False, "missing mandatory provenance/review fields"
    if c["license_verified"] is not True:
        return False, "license not verified"
    if c["contains_text"] is not False or c["contains_excluded_people"] is not False:
        return False, "text/person exclusion not cleared"
    if c["is_moving_video"] is not True:
        return False, "not confirmed moving footage"
    if int(c["reviewed_frames"]) < 3:
        return False, "insufficient reviewed frames"
    if float(c["duration"]) <= 0 or int(c["width"]) <= 0 or int(c["height"]) <= 0:
        return False, "invalid source metadata"
    if not str(c["path"]).strip():
        return False, "empty source path"
    return True, "accepted"


def scene_ranges(words, audio_duration, fps, max_seconds=7, pause=0.6):
    ranges = []
    start = 0
    for i, w in enumerate(words):
        next_start = float(words[i+1]["start"]) if i+1 < len(words) else audio_duration
        gap = next_start - float(w["end"])
        elapsed = float(w["end"]) - float(words[start]["start"])
        if i == len(words)-1 or gap >= pause or elapsed >= max_seconds:
            ranges.append((start, i, next_start))
            start = i + 1
    if not ranges:
        return []
    result = []
    frame_start = 0
    for ri, (a,b,right) in enumerate(ranges):
        frame_end = math.ceil(right * fps - 1e-9)
        if ri == len(ranges)-1:
            frame_end = math.ceil(audio_duration * fps)
        if frame_end <= frame_start:
            frame_end = frame_start+1
        result.append((a,b,frame_start,frame_end))
        frame_start = frame_end
    return result


def relevance(scene_text, clip):
    tokens = to_tokens(scene_text)
    clip_tokens = to_tokens(" ".join(str(x) for x in clip.get("tags", []))
                            + " " + str(clip.get("description","")))
    overlap = len(tokens & clip_tokens)
    return overlap * 7 + min(int(clip["width"]), int(clip["height"])) / 1000 if overlap else 0


def build(words, clips, audio_duration, fps=30):
    duration = float(audio_duration)
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("audio duration must be positive")
    if fps not in (24,25,30,60):
        raise ValueError("fps must be one of 24, 25, 30, 60")
    validate_words(words,duration)
    seen = set()
    accepted, rejected = [], []
    for c in clips:
        if c.get("id") in seen:
            raise ValueError(f"duplicate clip id {c.get('id')}")
        seen.add(c.get("id"))
        okay, reason = clean_clip(c)
        (accepted if okay else rejected).append(c if okay else {"id":c.get("id"),"reason":reason})
    ranges = scene_ranges(words,duration,fps)
    scenes, blockers = [], []
    for n,(a,b,f0,f1) in enumerate(ranges,1):
        text = " ".join(str(w.get("word") or w.get("text")) for w in words[a:b+1])
        seconds = (f1-f0)/fps
        candidates = [c for c in accepted if float(c["duration"]) + .0001 >= seconds
                      and relevance(text, c) > 0]
        candidates.sort(key=lambda c:(-relevance(text,c),str(c["id"])))
        chosen = candidates[0] if candidates else None
        if chosen is None:
            blockers.append({"scene":n,"reason":"no reviewed licensed moving clip long enough","seconds":seconds})
        scenes.append({
            "id":f"SCENE-{n:03d}", "start_frame":f0,"end_frame_exclusive":f1,
            "start_seconds":round(f0/fps,6),"end_seconds":round(f1/fps,6),
            "spoken_text":text,
            "word_ids":list(range(a,b+1)),
            "key_words":[{"text":str(w.get("word") or w.get("text")),
                          "start":float(w["start"])}
                         for w in words[a:b+1]
                         if w.get("emphasis") or NUMBERS.search(str(w.get("word") or w.get("text")))],
            "footage_id":chosen["id"] if chosen else None,
            "footage_path":chosen["path"] if chosen else None,
            "video_trim": {"in":0.0,"out":round(seconds,6)} if chosen else None,
            "camera": {"move":CAMERAS[(n-1)%len(CAMERAS)],
                       "easing":"easeInOutCubic","motion_is_digital":True},
            "rights_status":"verified" if chosen else "missing",
        })
    frame_count=math.ceil(duration*fps)
    if scenes and scenes[-1]["end_frame_exclusive"] != frame_count:
        raise AssertionError("timeline frame coverage broken")
    return {
        "schema":SCHEMA,"audio":{"duration":duration,"preserve_original":True,
                                  "audio_editing_allowed":False},
        "video":{"fps":fps,"width":1080,"height":1920,"frame_count":frame_count},
        "scenes":scenes,"rejected_clips":rejected,"blockers":blockers,
        "production_ready":len(blockers)==0,
        "notice":"This is an edit decision plan only. No footage or final video has been rendered.",
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--words",type=Path,required=True)
    ap.add_argument("--clips",type=Path,required=True)
    ap.add_argument("--duration",type=float,required=True)
    ap.add_argument("--fps",type=int,default=30)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    if args.fps <= 0 or args.duration <= 0:
        ap.error("--fps and --duration must be positive")
    try:
        words=json.loads(args.words.read_text(encoding="utf-8"))
        if isinstance(words, dict) and isinstance(words.get("words"), list):
            words=words["words"]  # the repo's words.json shape: {"words": [...]}
        result=build(words, json.loads(args.clips.read_text(encoding="utf-8")),args.duration,args.fps)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        ap.error(f"{type(exc).__name__}: {exc}")
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"file":str(args.out),"scenes":len(result["scenes"]),
                      "blockers":len(result["blockers"]),"ready":result["production_ready"]}))
    return 0 if result["production_ready"] else 2


if __name__=="__main__":
    raise SystemExit(main())
