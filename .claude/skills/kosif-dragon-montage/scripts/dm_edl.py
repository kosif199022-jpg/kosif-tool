#!/usr/bin/env python3
"""Dragon Montage — the one canonical edit decision list (kosif.dm.edl.v1) and its converters.

  normalize / reflow      recompute rec_in + duration from src ranges, speed and xfade overlaps
  record_words            the analysis words that survive the edit, moved to record time (captions)
  to_timeline             -> kosif.timeline.v1   (kosif-superpowers/scripts/kosif_timeline.py)
  from_timeline           <- kosif.timeline.v1
  from_cut_plan           <- kosif.edl.v1        (kosif-superpowers/scripts/cinematic_cut_planner.py)
  to_pve                  -> pro-video-editor EDL JSON (vendor/.../pro-video-editor-ffmpeg/scripts/edl_render.py)
  to_nle                  -> timeline.v1 project + words.json that nle_export.py reads (FCPXML/Premiere/CapCut…)

CLI:
  dm_edl.py convert --job DIR --to timeline|pve|nle|words [--out PATH]
  dm_edl.py import  --job DIR --cut-plan PLAN.json | --timeline TL.json      (writes edl.json)
  dm_edl.py check   --job DIR

Stdlib only. Converters never read media; they map clip ids to paths with analysis.json.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dm_common as dm  # noqa: E402

TIMELINE_SCHEMA = "kosif.timeline.v1"
CUT_PLAN_SCHEMA = "kosif.edl.v1"
EDL_SCHEMA = dm.SCHEMAS["edl"]

# ffmpeg xfade names that edl_render.py accepts (kept in sync with its XFADE set).
XFADE = {"fade", "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft", "slideright", "slideup", "slidedown",
         "circleopen", "circleclose", "dissolve", "pixelize", "radial", "smoothleft", "smoothright", "fadeblack",
         "fadewhite", "distance", "hblur", "zoomin", "squeezeh", "squeezev"}


def r3(x: float) -> float:
    return round(float(x) + 0.0, 3)


# --------------------------------------------------------------------------- core helpers
_TRANSITIONS = None


def _transition_table() -> dict:
    """data/transitions.json (shared vocabulary): normalised id/alias -> {xfade, seconds}."""
    global _TRANSITIONS
    if _TRANSITIONS is None:
        _TRANSITIONS = {}
        try:
            doc = json.loads((dm.SKILL / "data" / "transitions.json").read_text(encoding="utf-8"))
            items = doc if isinstance(doc, list) else next(
                (v for v in doc.values() if isinstance(v, list) and v and isinstance(v[0], dict)), [])
            for it in items:
                if not isinstance(it, dict) or not it.get("id"):
                    continue
                for k in [it["id"], *(it.get("aliases") or [])]:
                    _TRANSITIONS.setdefault(str(k).strip().lower().replace("_", "-"), it)
        except (OSError, ValueError, StopIteration):
            pass
    return _TRANSITIONS


def xfade_name(tr: dict | None) -> str | None:
    """'xfade-fade' / 'fade' / {'xfade':'wipeleft'} / a data/transitions.json id or alias ('whip-pan')
    -> ffmpeg xfade name, or None for a hard cut. The render station uses the same answer."""
    if not tr:
        return None
    raw = str(tr.get("xfade") or tr.get("type") or tr.get("id") or "cut")
    name = raw[len("xfade-"):] if raw.startswith("xfade-") else raw
    if name in XFADE:
        return name
    ent = _transition_table().get(raw.strip().lower().replace("_", "-"))
    xf = (ent or {}).get("xfade")
    return str(xf) if xf and xf != "cut" else None


def overlap(ev: dict) -> float:
    """Seconds this event overlaps the previous one (xfade), 0 for a cut. Without explicit seconds the
    transitions.json default for that transition is used, else 0.25."""
    tr = ev.get("transition_in") or {}
    if xfade_name(tr) is None:
        return 0.0
    secs = tr.get("seconds", tr.get("duration"))
    if secs is None:
        ent = _transition_table().get(str(tr.get("id") or "").strip().lower().replace("_", "-")) or {}
        secs = ent.get("seconds") or 0.25
    return float(secs)


def event_seconds(ev: dict) -> float:
    return (float(ev["src_out"]) - float(ev["src_in"])) / float(ev.get("speed", 1.0) or 1.0)


def reflow(edl: dict) -> dict:
    """Recompute rec_in for every event (in list order) and the total duration. Mutates and returns edl."""
    t = 0.0
    for i, ev in enumerate(edl["events"]):
        ov = 0.0 if i == 0 else min(overlap(ev), event_seconds(ev) / 2, event_seconds(edl["events"][i - 1]) / 2)
        if i == 0 and ev.get("transition_in") and xfade_name(ev["transition_in"]):
            ev["transition_in"] = {"id": "cut"}
        if ov and ev.get("transition_in"):
            ev["transition_in"]["seconds"] = r3(ov)
        ev["src_in"], ev["src_out"] = r3(ev["src_in"]), r3(ev["src_out"])
        ev["rec_in"] = r3(max(0.0, t - ov))
        t = ev["rec_in"] + event_seconds(ev)
    edl["duration"] = r3(t)
    return edl


def renumber(edl: dict) -> dict:
    for i, ev in enumerate(edl["events"], 1):
        ev["id"] = f"e{i:03d}"
    return edl


def check(edl: dict) -> list[str]:
    """Contract validation plus timeline sanity. Returns a list of problems (empty = fine)."""
    problems = []
    try:
        dm.validate("edl", edl)
    except dm.ContractError as exc:
        return [str(exc)]
    prev_end = 0.0
    for i, ev in enumerate(edl["events"]):
        if ev["rec_in"] < prev_end - overlap(ev) - 0.002:
            problems.append(f"{ev['id']}: overlaps the previous event more than its transition")
        prev_end = ev["rec_in"] + event_seconds(ev)
    if abs(prev_end - edl["duration"]) > 0.01:
        problems.append(f"duration {edl['duration']} != last event end {prev_end:.3f}")
    return problems


def clip_index(analysis: dict | None) -> dict:
    return {c["id"]: c for c in (analysis or {}).get("clips", [])}


def word_text(w: dict) -> str:
    return str(w.get("w") or w.get("word") or w.get("text") or "")


def record_words(edl: dict, analysis: dict) -> list[dict]:
    """Words spoken inside the kept source ranges, re-timed to the record timeline (for captions)."""
    clips = clip_index(analysis)
    out = []
    for ev in edl["events"]:
        if ev.get("mute"):
            continue
        c = clips.get(ev["clip"]) or {}
        sp = float(ev.get("speed", 1.0) or 1.0)
        for w in c.get("words") or []:
            s, e = float(w["start"]), float(w["end"])
            if s >= ev["src_in"] - 1e-6 and e <= ev["src_out"] + 1e-6:
                out.append({"word": word_text(w), "start": r3(ev["rec_in"] + (s - ev["src_in"]) / sp),
                            "end": r3(ev["rec_in"] + (e - ev["src_in"]) / sp), "event": ev["id"]})
    return out


# --------------------------------------------------------------------------- kosif.timeline.v1
def to_timeline(edl: dict, analysis: dict, *, include_music: bool = True, name: str | None = None) -> dict:
    """kosif.timeline.v1 project. One video track (xfades become alpha fade_in on the incoming clip,
    the timeline's own crossfade model) plus an optional music track. Each clip carries `dm` metadata so
    from_timeline() can round-trip reasons, roles and cameras. Note: kosif_timeline.py itself renders at most
    60 s / 32 clips; nle_export.py reads the same document without those limits."""
    clips = clip_index(analysis)
    edl = reflow(copy.deepcopy(edl))
    vclips = []
    warnings = []
    for ev in edl["events"]:
        c = clips.get(ev["clip"])
        if c is None:
            raise ValueError(f"{ev['id']}: clip {ev['clip']} not in analysis")
        if abs(float(ev.get("speed", 1.0)) - 1.0) > 1e-6:
            warnings.append(f"{ev['id']}: speed {ev['speed']} is not carried by kosif.timeline.v1")
        ov = overlap(ev) if ev is not edl["events"][0] else 0.0
        vclips.append({
            "id": ev["id"], "path": c["path"], "start": ev["rec_in"], "duration": r3(event_seconds(ev)),
            "in": ev["src_in"], "include_audio": bool(c.get("has_audio", True)) and not ev.get("mute", False),
            "fade_in": r3(ov), "fade_out": 0,
            "dm": {k: ev[k] for k in ("clip", "shot", "reason", "role", "kind", "camera", "transition_in", "speed", "src_out")
                   if k in ev},
        })
    tracks = [{"id": "V1", "kind": "video", "layer": 0, "clips": vclips}]
    music = ((edl.get("audio") or {}).get("music") or {})
    mpath = music.get("path") or ((analysis or {}).get("music") or {}).get("path")
    if include_music and mpath:
        gain = float(music.get("gain_db", -18))
        tracks.append({"id": "A1", "kind": "audio", "layer": 0, "clips": [{
            "id": "music", "path": mpath, "start": 0, "duration": edl["duration"], "in": 0,
            "volume": r3(min(3.0, 10 ** (gain / 20))), "fade_in": 0, "fade_out": r3(min(2.0, edl["duration"] / 2))}]})
    doc = {"schema": TIMELINE_SCHEMA, "name": name or "dragon-montage", "width": int(edl["width"]),
           "height": int(edl["height"]), "fps": int(round(float(edl["fps"]))), "duration": edl["duration"],
           "background": "#000000", "tracks": tracks,
           "dm": {"grade": edl.get("grade"), "captions": edl.get("captions"), "audio": edl.get("audio")}}
    if warnings:
        doc["dm"]["warnings"] = warnings
    return doc


def from_timeline(doc: dict, analysis: dict | None = None) -> dict:
    if doc.get("schema") != TIMELINE_SCHEMA:
        raise ValueError(f"expected {TIMELINE_SCHEMA}")
    by_path = {str(Path(c["path"])): c["id"] for c in clip_index(analysis).values()}
    meta = doc.get("dm") or {}
    events, music_path, music_gain = [], None, -18.0
    vtracks = sorted([t for t in doc["tracks"] if t.get("kind") in ("video", "image")],
                     key=lambda t: int(t.get("layer", 0)))
    for t in doc["tracks"]:
        if t.get("kind") == "audio" and t.get("clips"):
            m = t["clips"][0]
            music_path = m["path"]
            vol = float(m.get("volume", 1.0))
            if vol > 0:
                import math
                music_gain = r3(20 * math.log10(vol))
    flat = sorted([c for t in vtracks for c in t.get("clips", [])], key=lambda c: (float(c["start"]), c["id"]))
    for i, c in enumerate(flat):
        m = c.get("dm") or {}
        clip_id = m.get("clip") or by_path.get(str(Path(c["path"]))) or f"x{i + 1:02d}"
        src_in = float(c.get("in", 0))
        speed = float(m.get("speed", 1.0))
        ev = {"id": c["id"] if str(c["id"]).startswith("e") else f"e{i + 1:03d}", "clip": clip_id,
              "src_in": r3(src_in), "src_out": r3(m.get("src_out", src_in + float(c["duration"]) * speed)),
              "rec_in": r3(c["start"]), "speed": speed,
              "transition_in": m.get("transition_in") or (
                  {"id": "xfade-fade", "xfade": "fade", "seconds": r3(c["fade_in"])} if float(c.get("fade_in", 0)) > 0 and i
                  else {"id": "cut"}),
              "camera": m.get("camera") or {"id": "static"},
              "reason": m.get("reason") or f"imported from kosif.timeline.v1 clip {c['id']} | مستورد من التايملاين"}
        for k in ("shot", "role", "kind"):
            if k in m:
                ev[k] = m[k]
        if not c.get("include_audio", False):
            ev["mute"] = True
        events.append(ev)
    audio = meta.get("audio") or {"music": {"path": music_path, "gain_db": music_gain, "duck_under_speech_db": -10},
                                  "voice_from": "events", "target_lufs": -14}
    edl = {"schema": EDL_SCHEMA, "width": int(doc["width"]), "height": int(doc["height"]), "fps": doc["fps"],
           "events": events, "audio": audio,
           "captions": meta.get("captions") or {"enabled": False, "style": "none", "words_from": "analysis"},
           "grade": meta.get("grade") or {"id": "none"}, "duration": 0.0}
    return reflow(edl)


# --------------------------------------------------------------------------- kosif.edl.v1 (cut planner)
def from_cut_plan(doc: dict, analysis: dict | None = None) -> dict:
    """cinematic_cut_planner scenes -> events. The planner keeps the voice-over as the audio bed, so the
    footage events are muted and the voice path (if any) is left to the render station."""
    if doc.get("schema") != CUT_PLAN_SCHEMA:
        raise ValueError(f"expected {CUT_PLAN_SCHEMA}")
    video = doc.get("video") or {}
    fps = video.get("fps", 30)
    by_path = {str(Path(c["path"])): c["id"] for c in clip_index(analysis).values()}
    extra: dict[str, str] = {}
    events = []
    for sc in doc.get("scenes") or []:
        if not sc.get("footage_path"):
            continue
        p = str(Path(sc["footage_path"]))
        cid = by_path.get(p) or extra.setdefault(p, f"c{len(by_path) + len(extra) + 1:02d}")
        seconds = (int(sc["end_frame_exclusive"]) - int(sc["start_frame"])) / float(fps)
        tin = float((sc.get("video_trim") or {}).get("in", 0.0))
        tout = float((sc.get("video_trim") or {}).get("out", tin + seconds))
        cam = (sc.get("camera") or {}).get("move")
        text = str(sc.get("spoken_text") or "").strip()
        events.append({"id": f"e{len(events) + 1:03d}", "clip": cid, "src_in": r3(tin), "src_out": r3(max(tout, tin + 1 / fps)),
                       "rec_in": r3(int(sc["start_frame"]) / float(fps)), "speed": 1.0, "transition_in": {"id": "cut"},
                       "camera": {"id": cam or "static"}, "mute": True, "role": "cover",
                       "reason": f"cut plan {sc.get('id')}: covers “{text[:60]}” | لقطة تغطي الجملة المنطوقة"})
    edl = {"schema": EDL_SCHEMA, "width": int(video.get("width", 1080)), "height": int(video.get("height", 1920)),
           "fps": fps, "events": events,
           "audio": {"music": {"path": None, "gain_db": -18, "duck_under_speech_db": -10}, "voice_from": "external",
                     "target_lufs": -14},
           "captions": {"enabled": True, "style": "clean", "words_from": "analysis"}, "grade": {"id": "none"},
           "duration": 0.0}
    if extra:
        edl["unmapped_sources"] = {v: k for k, v in extra.items()}
    reflow(edl)
    # The planner timeline may have gaps (scenes without footage); keep its record positions.
    for ev, sc in zip(edl["events"], [s for s in doc.get("scenes") or [] if s.get("footage_path")]):
        ev["rec_in"] = r3(int(sc["start_frame"]) / float(fps))
    if edl["events"]:
        last = edl["events"][-1]
        edl["duration"] = r3(last["rec_in"] + event_seconds(last))
    return edl


# --------------------------------------------------------------------------- pro-video-editor edl_render.py
def to_pve(edl: dict, analysis: dict, *, captions: str | None = None, lut: str | None = None) -> dict:
    """The JSON edl_render.py reads: fps, size, sources, clips[{src,in,out,speed,transition}], music, lut,
    captions, audio.loudnorm. edl_render.py needs an audio stream in every source (it uses [n:a])."""
    clips = clip_index(analysis)
    edl = reflow(copy.deepcopy(edl))
    sources, out_clips, notes = {}, [], []
    for ev in edl["events"]:
        c = clips.get(ev["clip"])
        if c is None:
            raise ValueError(f"{ev['id']}: clip {ev['clip']} not in analysis")
        sources.setdefault(ev["clip"], c["path"])
        if not c.get("has_audio", True):
            notes.append(f"{ev['clip']} has no audio stream; edl_render.py needs one (add a silent track)")
        name = xfade_name(ev.get("transition_in"))
        tr = {"type": "cut"} if name is None or not out_clips else {"type": name, "duration": r3(overlap(ev))}
        item = {"src": ev["clip"], "in": ev["src_in"], "out": ev["src_out"], "speed": float(ev.get("speed", 1.0)),
                "transition": tr}
        if ev.get("audio_lead"):
            item["audio_lead"] = float(ev["audio_lead"])
        out_clips.append(item)
    doc = {"fps": int(round(float(edl["fps"]))), "size": [int(edl["width"]), int(edl["height"])],
           "sources": sources, "clips": out_clips,
           "audio": {"loudnorm": {"I": float((edl.get("audio") or {}).get("target_lufs", -14)), "TP": -1.0, "LRA": 11}}}
    music = (edl.get("audio") or {}).get("music") or {}
    mpath = music.get("path") or ((analysis or {}).get("music") or {}).get("path")
    if mpath:
        doc["sources"]["music"] = mpath
        doc["music"] = {"src": "music", "gain_db": float(music.get("gain_db", -18)), "fade_out": 2.0}
    lut = lut or (edl.get("grade") or {}).get("lut")
    if lut:
        doc["lut"] = lut
    if captions:
        doc["captions"] = captions
    if notes:
        doc["notes"] = sorted(set(notes))
    return doc


# --------------------------------------------------------------------------- nle_export.py
def to_nle(edl: dict, analysis: dict, out_dir: str | Path, *, name: str = "dragon-montage") -> dict:
    """Write what nle_export.py reads: a kosif.timeline.v1 project (absolute media paths) and a words.json
    in record time for captions. Returns {'project','words','argv'} — argv runs nle_export.py export."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    proj = to_timeline(edl, analysis, name=name)
    for t in proj["tracks"]:
        for c in t["clips"]:
            c["path"] = str(Path(c["path"]).resolve())
    pf = out_dir / "nle_timeline.json"
    pf.write_text(json.dumps(proj, ensure_ascii=False, indent=2), encoding="utf-8")
    words = record_words(edl, analysis)
    wf = out_dir / "nle_words.json"
    wf.write_text(json.dumps({"words": [{"word": w["word"], "start": w["start"], "end": w["end"]} for w in words]},
                             ensure_ascii=False, indent=2), encoding="utf-8")
    argv = dm.py(dm.SP / "nle_export.py") + ["export", "--project", str(pf), "--out", str(out_dir / "nle"),
                                             "--formats", "fcpxml,xmeml,edl,otio,srt,capcut", "--name", name, "--force"]
    if not words:
        argv[argv.index("--formats") + 1] = "fcpxml,xmeml,edl,otio,capcut"
    else:
        argv += ["--words", str(wf)]
    return {"project": str(pf), "words": str(wf), "argv": argv}


# --------------------------------------------------------------------------- cli
def main(argv=None) -> int:
    dm.utf8_stdio()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    cv = sub.add_parser("convert")
    cv.add_argument("--job", required=True)
    cv.add_argument("--to", required=True, choices=["timeline", "pve", "nle", "words"])
    cv.add_argument("--out")
    im = sub.add_parser("import")
    im.add_argument("--job", required=True)
    g = im.add_mutually_exclusive_group(required=True)
    g.add_argument("--cut-plan")
    g.add_argument("--timeline")
    ck = sub.add_parser("check")
    ck.add_argument("--job", required=True)
    a = ap.parse_args(argv)
    job = Path(a.job)
    analysis = dm.read(job, "analysis")
    if a.cmd == "import":
        src = json.loads(Path(a.cut_plan or a.timeline).read_text(encoding="utf-8"))
        edl = from_cut_plan(src, analysis) if a.cut_plan else from_timeline(src, analysis)
        print(json.dumps({"written": str(dm.write(job, "edl", edl)), "events": len(edl["events"])}))
        return 0
    edl = dm.read(job, "edl")
    if a.cmd == "check":
        probs = check(edl)
        print(json.dumps({"ok": not probs, "problems": probs}, ensure_ascii=False))
        return 0 if not probs else 1
    if a.to == "nle":
        res = to_nle(edl, analysis, a.out or job / "render")
        print(json.dumps(res, ensure_ascii=False))
        return 0
    doc = {"timeline": lambda: to_timeline(edl, analysis), "pve": lambda: to_pve(edl, analysis),
           "words": lambda: {"words": record_words(edl, analysis)}}[a.to]()
    out = Path(a.out or job / f"edl.{a.to}.json")
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"written": str(out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
