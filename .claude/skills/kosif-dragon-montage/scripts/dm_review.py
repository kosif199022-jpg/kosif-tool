#!/usr/bin/env python3
"""Station 7 — يتفرج وينقد (watch and critique) for Dragon Montage.

    python3 dm_review.py review --job DIR [--round N]
    python3 dm_review.py review --job DIR --add-note "the hook face is too small" [--fix e007:drop:"weak shot"]

Reads render.json (+ render/final.mp4), edl.json, analysis.json, brief.json and, when
present, concepts.json / look.json. Writes review.json (kosif.dm.review.v1), a frame strip
review/r{N}_fXX.jpg and review/VISION_PROMPT.md so Claude can look at the frames and add
human-taste notes with --add-note / --fix.

Every automated check carries pass, evidence and (when it failed) the output timestamps
in "at". Each failed check maps to concrete `fixes` {event, action, detail, check}; fixes
that are not tied to one event use event "*" with a "target" (audio|grade|captions).
Reuses kosif-superpowers verify_video.py (spec + loudness) and video_eyes.py (motion,
freezes); silence and black frames come from ffmpeg silencedetect / blackdetect.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dm_common as C  # noqa: E402

STATION = "review"
ACTIONS = ("trim", "drop", "swap", "retime", "regrade", "extend", "add")
MAX_ROUNDS = 3

# thresholds (seconds unless noted)
DEAD_AIR_SILENCE = 0.7
DEAD_AIR_FLAT = 2.0
HOOK_START = 0.5
HOOK_WINDOW = 3.0
BEAT_TOL = 0.08
BEAT_RATIO_MIN = 0.6
BLACK_MIN = 0.1
SILENCE_DB = -45
PEAK_MAX = -1.0

# check id -> weight in the score; "critical" ones block ship on their own
WEIGHTS = {"technical": 1.0, "hook-in-3s": 2.0, "dead-air": 1.5, "cuts-on-beat": 0.75,
           "shot-length": 0.75, "caption-coverage": 1.0, "repetition": 1.0, "duration": 1.0,
           "safe-area": 0.75, "black-frames": 1.5, "audio-clipping": 1.0}
CRITICAL = {"hook-in-3s", "dead-air", "black-frames", "technical"}

# pacing (seconds per shot) when the brief has no explicit range
PACING = {"high": (0.8, 2.5), "mid": (1.2, 4.0), "low": (2.0, 7.0)}

SAFE = {  # fraction of height kept free of platform UI at the bottom / top (caption_styles.json safe_area wins)
    "9:16": {"bottom": 0.20, "top": 0.10}, "4:5": {"bottom": 0.12, "top": 0.08},
    "1:1": {"bottom": 0.10, "top": 0.06}, "16:9": {"bottom": 0.08, "top": 0.05},
}
DATA = Path(__file__).resolve().parent.parent / "data"
DEFAULT_HOOK_ROLES = ("hook", "problem", "question", "cold-open", "tease")
SPEECH_PACING = (1.5, 9.0)      # a spoken phrase is judged as a phrase, not as a b-roll beat


def _data(name: str) -> dict:
    try:
        return json.loads((DATA / name).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def hook_roles() -> set:
    """Roles that count as the hook — the same list dm_think and dm_direct read (editor_mind.hook_roles)."""
    return set((_data("editor_mind.json").get("hook_roles") or {}).get("roles") or DEFAULT_HOOK_ROLES)


def speech_pacing() -> tuple[float, float]:
    sp = ((_data("editor_mind.json").get("pacing_by_kind") or {}).get("speech") or {}).get("shot_s")
    return (float(sp[0]), float(sp[1])) if sp and len(sp) == 2 else SPEECH_PACING


def safe_area(aspect: str) -> dict:
    """Caption safe band per aspect: caption_styles.json `safe_area` (shared with dm_render) over the defaults."""
    sa = (_data("caption_styles.json").get("safe_area") or {}).get(aspect) or {}
    base = dict(SAFE.get(aspect, {"bottom": 0.1, "top": 0.05}))
    base.update({k: float(v) for k, v in sa.items() if k in ("bottom", "top") and v is not None})
    return base


def qscore(shot: dict | None) -> float:
    """Shot quality; null/missing (OpenCV not installed) is neutral 0.5."""
    v = ((shot or {}).get("quality") or {}).get("score")
    try:
        return float(v) if v is not None else 0.5
    except (TypeError, ValueError):
        return 0.5


def voiced_spans(edl: dict, analysis: dict) -> list[tuple[float, float]]:
    """Output spans where silence would be dead air: speech events with real, unmuted audio. Muted b-roll,
    clips without audio and b-roll with no music under it are allowed to be quiet."""
    out = []
    for ev in edl["events"]:
        clip = clip_of(analysis, ev["clip"])
        if ev.get("mute") or clip.get("has_audio") is False or not is_speech_event(ev, analysis):
            continue
        out.append(out_span(ev))
    return out


def is_speech_event(ev: dict, analysis: dict) -> bool:
    if ev.get("kind"):
        return ev["kind"] == "speech"
    a, b = float(ev["src_in"]), float(ev["src_out"])
    ws = [w for w in clip_of(analysis, ev["clip"]).get("words", []) if a <= (w["start"] + w["end"]) / 2 < b]
    return len(ws) >= 2


def has_speech(analysis: dict) -> bool:
    return any(len(c.get("words") or []) >= 5 for c in analysis.get("clips", []))


def r3(x: float) -> float:
    return round(float(x), 3)


# ----------------------------------------------------------------- loading

def load_optional(job: Path, kind: str) -> dict | None:
    try:
        return C.read(job, kind)
    except (FileNotFoundError, C.ContractError, json.JSONDecodeError):
        return None


def rel(job: Path, p: str | None) -> Path | None:
    if not p:
        return None
    q = Path(p)
    return q if q.is_absolute() else job / q


def out_span(ev: dict) -> tuple[float, float]:
    sp = float(ev.get("speed") or 1.0) or 1.0
    a = float(ev["rec_in"])
    return a, a + (float(ev["src_out"]) - float(ev["src_in"])) / sp


def src_to_out(ev: dict, t: float) -> float:
    sp = float(ev.get("speed") or 1.0) or 1.0
    return float(ev["rec_in"]) + (t - float(ev["src_in"])) / sp


def out_to_src(ev: dict, t: float) -> float:
    sp = float(ev.get("speed") or 1.0) or 1.0
    return float(ev["src_in"]) + (t - float(ev["rec_in"])) * sp


def events_in(edl: dict, a: float, b: float) -> list[dict]:
    """Events whose output span overlaps [a, b]."""
    hits = []
    for ev in edl["events"]:
        s, e = out_span(ev)
        if min(e, b) - max(s, a) > 1e-3:
            hits.append(ev)
    return hits


def clip_of(analysis: dict, cid: str) -> dict:
    return next((c for c in analysis.get("clips", []) if c.get("id") == cid), {})


def shot_of(analysis: dict, ev: dict) -> dict:
    clip = clip_of(analysis, ev["clip"])
    if ev.get("shot"):
        s = next((s for s in clip.get("shots", []) if s.get("id") == ev["shot"]), None)
        if s:
            return s
    mid = (float(ev["src_in"]) + float(ev["src_out"])) / 2
    return next((s for s in clip.get("shots", []) if s["start"] <= mid < s["end"]), {})


def output_words(edl: dict, analysis: dict) -> list[dict]:
    """Speech words that survive the edit, placed on the output timeline."""
    out = []
    for ev in edl["events"]:
        for w in clip_of(analysis, ev["clip"]).get("words", []):
            mid = (w["start"] + w["end"]) / 2
            if float(ev["src_in"]) <= mid < float(ev["src_out"]):
                out.append({"w": w.get("w", ""), "event": ev["id"],
                            "start": r3(src_to_out(ev, max(w["start"], float(ev["src_in"])))),
                            "end": r3(src_to_out(ev, min(w["end"], float(ev["src_out"]))))})
    return sorted(out, key=lambda w: w["start"])


# ----------------------------------------------------------------- measuring (all receipted)

def measure(job: Path, video: Path, brief: dict, edl: dict) -> dict:
    m: dict = {"missing": []}
    m["probe"] = C.probe(video)
    v = next((s for s in m["probe"]["streams"] if s["codec_type"] == "video"), {})
    m["width"], m["height"] = int(v.get("width") or 0), int(v.get("height") or 0)
    m["duration"] = float(m["probe"]["format"].get("duration") or 0)
    m["has_audio"] = any(s["codec_type"] == "audio" for s in m["probe"]["streams"])
    rdir = job / "review"

    vv = C.SP / "verify_video.py"
    if vv.exists():
        jpath = rdir / "verify_video.json"
        argv = [*C.py(vv), video, "--aspect", brief.get("aspect") or f"{m['width']}:{m['height']}",
                "--fps", str(edl.get("fps") or 30), "--lufs", str(edl.get("audio", {}).get("target_lufs", -14)),
                "--json", jpath]
        if not m["has_audio"]:
            argv.append("--no-audio")
        C.run(job, STATION, "verify_video", argv, out=jpath, check=False)
        m["verify"] = json.loads(jpath.read_text(encoding="utf-8")) if jpath.exists() else None
    else:
        m["missing"].append("verify_video.py")
        m["verify"] = None

    ve = C.SP / "video_eyes.py"
    m["motion"] = None
    if ve.exists():
        res = C.run(job, STATION, "video_eyes.motion",
                    [*C.py(ve), "motion", video, "--fps", "10", "--freeze", str(DEAD_AIR_FLAT), "--json"], check=False)
        try:
            m["motion"] = json.loads(res.stdout)
        except ValueError:
            m["missing"].append("video_eyes.motion")
    else:
        m["missing"].append("video_eyes.py")

    # black frames
    res = C.run(job, STATION, "ffmpeg.blackdetect",
                ["ffmpeg", "-v", "info", "-nostats", "-i", video, "-vf",
                 f"blackdetect=d={BLACK_MIN}:pix_th=0.10", "-an", "-f", "null", "-"], check=False)
    m["black"] = [{"from": r3(float(a)), "to": r3(float(b))} for a, b in
                  re.findall(r"black_start:\s*([\d.]+)\s+black_end:\s*([\d.]+)", res.stderr)]

    # silences + true peak in one pass
    m["silences"], m["true_peak"], m["lufs"] = [], None, None
    if m["has_audio"]:
        res = C.run(job, STATION, "ffmpeg.silencedetect+ebur128",
                    ["ffmpeg", "-v", "info", "-nostats", "-i", video, "-vn", "-af",
                     f"silencedetect=noise={SILENCE_DB}dB:d={DEAD_AIR_SILENCE},ebur128=peak=true",
                     "-f", "null", "-"], check=False)
        err = res.stderr
        starts = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", err)]
        ends = [float(x) for x in re.findall(r"silence_end:\s*(-?[\d.]+)", err)]
        ends += [m["duration"]] * (len(starts) - len(ends))
        m["silences"] = [{"from": r3(max(0.0, s)), "to": r3(e)} for s, e in zip(starts, ends)]
        pk = re.search(r"True peak:\s*Peak:\s*(-?[\d.]+|-inf)", err)
        m["true_peak"] = float(pk.group(1)) if pk and pk.group(1) != "-inf" else None
        il = re.search(r"Integrated loudness:\s*I:\s*(-?[\d.]+)", err)
        m["lufs"] = float(il.group(1)) if il else None
    return m


# ----------------------------------------------------------------- checks

class Review:
    def __init__(self, edl: dict):
        self.edl = edl
        self.ids = {e["id"] for e in edl["events"]}
        self.checks: list[dict] = []
        self.fixes: list[dict] = []
        self.capped: list[dict] = []

    def check(self, cid: str, ok: bool, evidence: str, **extra) -> dict:
        c = {"id": cid, "pass": bool(ok), "evidence": evidence, **extra}
        self.checks.append(c)
        return c

    def fix(self, event: str, action: str, detail: str, check: str, **extra) -> None:
        assert action in ACTIONS
        assert event == "*" or event in self.ids, event
        f = {"event": event, "action": action, "detail": detail, "check": check, "by": "auto", **extra}
        key = (event, action, check)
        if not any((x["event"], x["action"], x["check"]) == key for x in self.fixes):
            self.fixes.append(f)

    def fix_span(self, a: float, b: float, check: str, why: str, *, prefer: str = "trim") -> None:
        """Turn a bad output interval into trim/drop fixes on the events under it."""
        for ev in events_in(self.edl, a, b):
            s, e = out_span(ev)
            if a <= s + 0.05 and b >= e - 0.05:
                self.fix(ev["id"], "drop", f"{why} covers the whole event ({r3(s)}–{r3(e)}s): drop it", check)
            elif prefer == "swap":
                self.fix(ev["id"], "swap", f"{why} at {r3(a)}–{r3(b)}s: swap for a clean shot of the same length", check)
            else:
                # keep the longer clean side of the event
                left, right = max(0.0, a - s), max(0.0, e - b)
                if left >= right:
                    ns, ne = float(ev["src_in"]), out_to_src(ev, max(s, a))
                else:
                    ns, ne = out_to_src(ev, min(e, b)), float(ev["src_out"])
                if ne - ns < 0.3:
                    self.fix(ev["id"], "drop", f"{why} at {r3(a)}–{r3(b)}s leaves <0.3s usable: drop it", check)
                else:
                    self.fix(ev["id"], "trim", f"{why} at {r3(a)}–{r3(b)}s: trim source to {r3(ns)}–{r3(ne)}s", check,
                             src_in=r3(ns), src_out=r3(ne))


def run_checks(job: Path, rv: Review, m: dict, analysis: dict, brief: dict, look: dict | None,
               render: dict) -> None:
    edl, events = rv.edl, rv.edl["events"]
    dur = m["duration"]
    words = output_words(edl, analysis)

    # technical -------------------------------------------------------------------------------
    vf = m.get("verify")
    if vf:
        # true peak is its own check (audio-clipping); duration is judged against the brief below
        bad = [c for c in vf.get("checks", []) if not c.get("pass") and "true peak" not in c["check"]
               and "duration" not in c["check"] and "frame count" not in c["check"]]
        frozen = (m.get("motion") or {}).get("frozen", [])
        rv.check("technical", not bad,
                 "verify_video: " + ("; ".join(f"{c['check']} = {c['value']}" for c in bad) or
                                     f"spec ok ({vf.get('codec')} {vf.get('width')}x{vf.get('height')} @ {vf.get('fps')})")
                 + (f"; frozen stretches {len(frozen)}" if frozen else ""),
                 at=[[f["from"], f["to"]] for f in frozen], tool="verify_video+video_eyes")
        loud = [c for c in bad if "loudness" in c["check"]]
        spec = [c for c in bad if c not in loud]
        if spec:
            rv.fix("*", "regrade", "re-render with delivery spec: " + "; ".join(c["check"] for c in spec),
                   "technical", target="encode")
        if loud:
            rv.fix("*", "regrade", f"loudness {loud[0]['value']}: normalise to "
                   f"{edl.get('audio', {}).get('target_lufs', -14)} LUFS (loudnorm two-pass)", "technical",
                   target="audio")
    else:
        rv.check("technical", True, "verify_video.py not available — spec not checked", skipped=True)

    # hook in 3s -------------------------------------------------------------------------------
    first = events[0] if events else None
    if first:
        role = str(first.get("role") or first.get("reason", "")).lower()
        head = role.split(":")[0].strip()
        is_hook = bool(first.get("hook")) or head in hook_roles() or "hook" in head or "هوك" in role
        speech0 = next((w["start"] for w in words), None)
        tl = (m.get("motion") or {}).get("timeline", [])
        motion0 = tl[0]["energy"] if tl else None
        silent0 = any(s["from"] <= 0.05 and s["to"] > HOOK_START for s in m["silences"])
        speech_ok = speech0 is not None and speech0 < HOOK_START
        motion_ok = motion0 is not None and motion0 >= 0.6 and not any(b["from"] <= 0.05 for b in m["black"])
        starts = speech_ok or motion_ok
        s, e = out_span(first)
        ok = is_hook and starts
        ev_txt = (f"first event {first['id']} role={'hook' if is_hook else repr(role[:40])}; "
                  f"speech starts {speech0 if speech0 is not None else 'never'}s; motion energy 0s={motion0}"
                  f"{'; opens on silence' if silent0 else ''}")
        rv.check("hook-in-3s", ok, ev_txt, at=[[0.0, r3(min(HOOK_WINDOW, e))]])
        if not is_hook:
            if has_speech(analysis):
                # talking content: the hook is a spoken line, never a b-roll shot
                rv.fix(first["id"], "swap", "first event is not the hook: open on the strongest spoken hook line",
                       "hook-in-3s", role="hook", kind="speech")
            else:
                best = hook_candidate(analysis, events)
                rv.fix(first["id"], "swap", "first event is not the hook: open on the strongest hook shot"
                       + (f" ({best})" if best else ""), "hook-in-3s", role="hook", kind="broll",
                       **({"with_shot": best} if best else {}))
        elif not starts:
            lead = None
            if speech0 is not None and speech0 < s + (e - s):
                lead = out_to_src(first, speech0) - 0.1
            if lead and lead > float(first["src_in"]):
                rv.fix(first["id"], "trim", f"dead lead-in: speech starts at {speech0}s; start source at {r3(lead)}s",
                       "hook-in-3s", src_in=r3(lead), src_out=r3(float(first["src_out"])))
            else:
                rv.fix(first["id"], "swap", "hook opens without speech or motion in the first 0.5s: "
                       "swap for a shot that starts moving/talking immediately", "hook-in-3s")

    # dead air -----------------------------------------------------------------------------------
    gaps = []
    voiced = voiced_spans(edl, analysis)
    for sl in m["silences"]:
        if sl["from"] >= dur - 0.3:
            continue
        for a, b in voiced:                       # only silence where someone should be talking counts
            fa, fb = max(a, sl["from"]), min(b, sl["to"])
            if fb - fa >= DEAD_AIR_SILENCE:
                gaps.append({"from": r3(fa), "to": r3(fb), "kind": "silence"})
    for fz in (m.get("motion") or {}).get("frozen", []):
        if fz["to"] - fz["from"] >= DEAD_AIR_FLAT:
            gaps.append({"from": fz["from"], "to": fz["to"], "kind": "flat-motion"})
    music = bool((edl.get("audio", {}).get("music") or {}).get("path"))
    rv.check("dead-air", not gaps,
             "; ".join(f"{g['kind']} {r3(g['to'] - g['from'])}s at {g['from']}–{g['to']}s" for g in gaps)
             or f"no silence ≥{DEAD_AIR_SILENCE}s and no flat motion ≥{DEAD_AIR_FLAT}s",
             at=[[g["from"], g["to"]] for g in gaps], music=music)
    for g in gaps:
        rv.fix_span(g["from"], g["to"], "dead-air", f"{g['kind']} {r3(g['to'] - g['from'])}s")

    # cuts on beat -------------------------------------------------------------------------------
    beats = (analysis.get("music") or {}).get("beats") or []
    cuts = [float(ev["rec_in"]) for ev in events[1:]]
    if beats and cuts:
        def near(t):
            return min(beats, key=lambda b: abs(b - t))
        on = [abs(near(t) - t) <= BEAT_TOL for t in cuts]
        ratio = sum(on) / len(on)
        off = [(ev, near(float(ev["rec_in"]))) for ev, k in zip(events[1:], on) if not k]
        rv.check("cuts-on-beat", ratio >= BEAT_RATIO_MIN, f"{sum(on)}/{len(on)} cuts within {BEAT_TOL}s of a beat",
                 ratio=r3(ratio), at=[[r3(float(ev["rec_in"])), r3(float(ev["rec_in"]))] for ev, _ in off])
        if ratio < BEAT_RATIO_MIN:
            for ev, b in off:
                rv.fix(ev["id"], "retime", f"cut at {ev['rec_in']}s is off-beat: move it to beat {r3(b)}s",
                       "cuts-on-beat", rec_at=r3(b))
    else:
        rv.check("cuts-on-beat", True, "no music beats in analysis — not applicable", skipped=True)

    # shot length vs pacing ---------------------------------------------------------------------
    # speech is judged by phrase pacing (whole phrases, never cut mid-word); b-roll by the look/feeling pace
    lo, hi = pacing_range(brief)
    slo, shi = speech_pacing()
    lens = []
    for ev in events:
        sp_ev = is_speech_event(ev, analysis)
        rng = (slo, shi) if sp_ev else (lo, hi)
        lens.append((ev, out_span(ev)[1] - out_span(ev)[0], sp_ev, rng))
    off = [(ev, L, sp_ev, rng) for ev, L, sp_ev, rng in lens if L < rng[0] - 0.05 or L > rng[1] + 0.05]
    share = 1 - len(off) / max(1, len(lens))
    rv.check("shot-length", share >= 0.75,
             f"{len(lens) - len(off)}/{len(lens)} shots inside their pace (speech {slo}–{shi}s phrase-led, "
             f"b-roll {lo}–{hi}s at energy {brief.get('energy')})"
             + ("; off: " + ", ".join(f"{ev['id']}={r3(L)}s" for ev, L, _, _ in off) if off else ""),
             range=[lo, hi], speech_range=[slo, shi], at=[list(map(r3, out_span(ev))) for ev, *_ in off])
    if share < 0.75:
        for ev, L, sp_ev, (rlo, rhi) in off:
            spd = float(ev.get("speed") or 1.0)
            if L > rhi:
                cut = float(ev["src_in"]) + rhi * spd
                if sp_ev:
                    cut = phrase_cut(clip_of(analysis, ev["clip"]), float(ev["src_in"]), cut)
                    if cut is None:
                        continue
                rv.fix(ev["id"], "trim", f"{r3(L)}s is long for {'a spoken phrase' if sp_ev else 'this pace'}: "
                       f"trim to ≤{rhi}s{' at a word gap' if sp_ev else ''}", "shot-length",
                       src_in=r3(float(ev["src_in"])), src_out=r3(cut))
            elif not sp_ev:
                rv.fix(ev["id"], "extend", f"{r3(L)}s flashes by: hold it to ≥{rlo}s (inside its shot) or merge",
                       "shot-length", seconds=r3(rlo - L))

    # caption coverage ------------------------------------------------------------------------
    cues = srt_cues(rel(job, render.get("captions")))
    cap_on = bool(edl.get("captions", {}).get("enabled"))
    if words:
        covered = [w for w in words if any(a - 0.15 <= (w["start"] + w["end"]) / 2 <= b + 0.15 for a, b in cues)]
        cov = len(covered) / len(words)
        miss = [w for w in words if w not in covered]
        rv.check("caption-coverage", cov >= 0.9,
                 f"{len(covered)}/{len(words)} spoken words under a caption ({len(cues)} cues"
                 f"{', captions disabled in edl' if not cap_on else ''})",
                 ratio=r3(cov), at=[[w["start"], w["end"]] for w in miss[:20]])
        if cov < 0.9:
            rv.fix("*", "regrade", f"captions miss {len(miss)} words: regenerate captions from analysis words"
                   + ("" if cap_on else " (enable captions in edl)"), "caption-coverage", target="captions")
    else:
        rv.check("caption-coverage", True, "no speech in the cut — nothing to caption", skipped=True)

    # repetition --------------------------------------------------------------------------------
    seen, reps = [], []
    for ev in events:
        for prev in seen:
            # a talking head is often ONE long shot: two different lines from it are not a repeat
            same_shot = ev.get("shot") and ev.get("shot") == prev.get("shot") and \
                not is_speech_event(ev, analysis) and not is_speech_event(prev, analysis)
            overlap = ev["clip"] == prev["clip"] and min(float(ev["src_out"]), float(prev["src_out"])) - \
                max(float(ev["src_in"]), float(prev["src_in"])) > 0.25
            if same_shot or overlap:
                reps.append((ev, prev))
                break
        seen.append(ev)
    rv.check("repetition", not reps,
             "; ".join(f"{a['id']} repeats {b['id']} ({a['clip']} {a['src_in']}–{a['src_out']})" for a, b in reps)
             or "no source shot used twice", at=[list(map(r3, out_span(a))) for a, _ in reps])
    for a, b in reps:
        rv.fix(a["id"], "drop" if len(events) > 3 else "swap", f"repeats {b['id']} — same source shot shown twice",
               "repetition")

    # duration ----------------------------------------------------------------------------------
    tgt = float(brief.get("target_seconds") or edl.get("duration") or dur)
    tol = max(2.0, 0.15 * tgt)
    rv.check("duration", abs(dur - tgt) <= tol, f"{r3(dur)}s vs target {tgt}s (±{r3(tol)}s)",
             target=tgt, actual=r3(dur))
    if abs(dur - tgt) > tol and events:
        if dur > tgt:
            need = dur - tgt
            for ev in sorted(events[1:], key=lambda e: qscore(shot_of(analysis, e))):
                L = out_span(ev)[1] - out_span(ev)[0]
                rv.fix(ev["id"], "drop", f"{r3(dur - tgt)}s over target: drop weakest shot ({r3(L)}s)", "duration")
                need -= L
                if need <= 0:
                    break
        else:
            rv.fix("*", "add", f"{r3(tgt - dur)}s under target: add the best unused lines/shots back toward "
                   f"{tgt}s", "duration", target="timeline", seconds=r3(tgt - dur))

    # aspect + safe area -------------------------------------------------------------------------
    want = C.ASPECTS.get(brief.get("aspect", ""))
    w, h = m["width"], m["height"]
    aspect_ok = not want or abs(w / max(1, h) - want[0] / want[1]) < 0.01
    pos = ((look or {}).get("captions") or {}).get("position") or edl.get("captions", {}).get("position", "lower")
    safe = safe_area(brief.get("aspect", ""))
    margin, align = ass_margin(job, render, h)
    cap_y = None
    if align in ("4", "5", "6", "7", "8", "9"):
        pos = "center" if align in ("4", "5", "6") else "top"     # the burned file decides, not the intent
    elif margin is not None:
        cap_y = margin / max(1, h)
    # without an .ass style the margin is unknown: do not guess, leave it to the vision pass
    safe_ok = not cap_on or not words or pos == "center" or cap_y is None or cap_y >= safe["bottom"]
    rv.check("safe-area", aspect_ok and safe_ok,
             f"{w}x{h} vs brief {brief.get('aspect')}{'' if aspect_ok else ' MISMATCH'}; captions {pos}, " +
             (f"bottom margin {r3(cap_y)} of height (safe ≥{safe['bottom']})" if cap_y is not None else
              "caption margin unknown (no .ass style) — check the frames"),
             aspect_ok=aspect_ok, caption_margin=cap_y)
    if not aspect_ok:
        rv.fix("*", "regrade", f"output is {w}x{h}, brief wants {brief.get('aspect')}: re-render at {want}",
               "safe-area", target="encode")
    if not safe_ok:
        rv.fix("*", "regrade", f"raise captions to ≥{int(safe['bottom'] * 100)}% from the bottom "
               "(platform UI covers the lower band) or use position=center", "safe-area", target="captions",
               min_bottom=r3(safe["bottom"] + 0.02))

    # black frames -------------------------------------------------------------------------------
    blk = [b for b in m["black"] if b["to"] - b["from"] >= BLACK_MIN]
    rv.check("black-frames", not blk,
             "; ".join(f"black {r3(b['to'] - b['from'])}s at {b['from']}–{b['to']}s" for b in blk) or "no black frames",
             at=[[b["from"], b["to"]] for b in blk])
    for b in blk:
        rv.fix_span(b["from"], b["to"], "black-frames", f"black {r3(b['to'] - b['from'])}s")

    # audio clipping -----------------------------------------------------------------------------
    if m["has_audio"]:
        tp = m["true_peak"]
        ok = tp is None or tp <= PEAK_MAX
        rv.check("audio-clipping", ok, f"true peak {tp} dBTP (max {PEAK_MAX}); integrated {m['lufs']} LUFS",
                 true_peak=tp, lufs=m["lufs"])
        if not ok:
            rv.fix("*", "regrade", f"true peak {tp} dBTP: add a -1.5 dBTP limiter / lower voice gain", "audio-clipping",
                   target="audio")
    else:
        rv.check("audio-clipping", True, "no audio stream", skipped=True)

    cap_fixes(rv, analysis, tgt, tol, dur)


CAP_ORDER = ("shot-length", "repetition", "duration", "dead-air", "black-frames", "hook-in-3s")


def projected(rv: Review, dur: float) -> float:
    """Output length if every event fix were applied (drops and narrowing trims; extends add)."""
    by = {e["id"]: e for e in rv.edl["events"]}
    lost, dropped, seen = 0.0, set(), {}
    for f in rv.fixes:
        ev = by.get(f["event"])
        if ev is None:
            continue
        s, e = out_span(ev)
        if f["action"] == "drop" and ev["id"] not in dropped:
            dropped.add(ev["id"])
            lost += (e - s) - seen.pop(ev["id"], 0.0)
        elif f["action"] == "trim" and ev["id"] not in dropped and f.get("src_out") is not None:
            sp = float(ev.get("speed") or 1.0) or 1.0
            keep = (min(float(f["src_out"]), float(ev["src_out"])) - max(float(f.get("src_in", ev["src_in"])),
                                                                          float(ev["src_in"]))) / sp
            cut = max(0.0, (e - s) - keep)
            if cut > seen.get(ev["id"], 0.0):
                lost += cut - seen.get(ev["id"], 0.0)
                seen[ev["id"]] = cut
        elif f["action"] == "extend":
            lost -= float(f.get("seconds") or 0)
    return dur - lost


def cap_fixes(rv: Review, analysis: dict, tgt: float, tol: float, dur: float) -> None:
    """A fix set must not push the cut outside the target tolerance: shed the least critical shrinking fixes
    (pacing first, then repetition…) and ask the director to re-fill the rest with an `add` fix."""
    floor = tgt - tol
    if projected(rv, dur) >= floor:
        return
    rank = {c: i for i, c in enumerate(CAP_ORDER)}
    shrink = sorted([f for f in rv.fixes if f["action"] in ("drop", "trim") and f["check"] != "duration"],
                    key=lambda f: rank.get(f["check"], 0))
    shed = []
    for f in shrink:
        if projected(rv, dur) >= floor or f["check"] in ("dead-air", "black-frames", "hook-in-3s"):
            break                                  # critical defects are fixed anyway; re-fill covers the length
        rv.fixes.remove(f)
        shed.append(f)
    after = projected(rv, dur)
    if after < tgt - 0.5:
        rv.fixes = [f for f in rv.fixes if not (f["event"] == "*" and f["action"] == "add")]
        rv.fixes.append({"event": "*", "action": "add", "check": "duration", "by": "auto", "target": "timeline",
                         "seconds": r3(tgt - after),
                         "detail": f"fixes would leave {r3(after)}s of {tgt}s: re-fill {r3(tgt - after)}s from unused material"})
    if shed:
        rv.capped = [{"event": f["event"], "action": f["action"], "check": f["check"]} for f in shed]


def hook_candidate(analysis: dict, events: list[dict]) -> str | None:
    used = {e.get("shot") for e in events}
    best, score = None, -1.0
    for c in analysis.get("clips", []):
        for s in c.get("shots", []):
            if s["id"] in used:
                continue
            talk = any(s["start"] <= w["start"] < s["end"] for w in c.get("words", []))
            sc = qscore(s) + 0.2 * talk + 0.3 * s.get("motion_energy", 0) + 0.1 * bool(s.get("faces"))
            if sc > score:
                best, score = s["id"], sc
    return best


def phrase_cut(clip: dict, src_in: float, limit: float) -> float | None:
    """Latest cut ≤ limit that sits in a gap between words (after ≥2 words), or None."""
    ws = sorted((w for w in clip.get("words", []) if float(w["start"]) >= src_in - 0.05),
                key=lambda w: float(w["start"]))
    best = None
    for i, w in enumerate(ws):
        end = float(w["end"])
        nxt = float(ws[i + 1]["start"]) if i + 1 < len(ws) else end + 0.3
        cut = min(end + 0.12, (end + nxt) / 2)
        if cut > limit:
            break
        if i >= 1:
            best = cut
    return best


def pacing_range(brief: dict) -> tuple[float, float]:
    p = brief.get("pacing") or {}
    if isinstance(p, dict) and p.get("shot_seconds"):
        lo, hi = p["shot_seconds"]
        return float(lo), float(hi)
    e = float(brief.get("energy") if brief.get("energy") is not None else 0.5)
    return PACING["high" if e >= 0.7 else "low" if e < 0.35 else "mid"]


def srt_cues(path: Path | None) -> list[tuple[float, float]]:
    if not path or not path.exists():
        return []
    def ts(s):
        h, mm, rest = s.replace(",", ".").split(":")
        return int(h) * 3600 + int(mm) * 60 + float(rest)
    return [(ts(a), ts(b)) for a, b in re.findall(r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)",
                                                  path.read_text(encoding="utf-8", errors="replace"))]


def ass_margin(job: Path, render: dict, h: int) -> tuple[float | None, str | None]:
    """(bottom margin in output pixels, Alignment) read from the burned .ass caption file.

    Uses render.json captions_ass first. The smallest effective margin wins: the style MarginV, any non-zero
    per-Dialogue MarginV override, and any \\pos(x,y) on a bottom-aligned line (margin = PlayResY - y)."""
    cands = [rel(job, x) for x in [render.get("captions_ass"), *(render.get("extra") or [])] if x]
    cands += sorted((job / "render").glob("*.ass")) if (job / "render").exists() else []
    for p in cands:
        if not (p and p.suffix == ".ass" and p.exists()):
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        ph = re.search(r"PlayResY:\s*(\d+)", txt)
        play_h = int(ph.group(1)) if ph else h
        fmt = re.search(r"^Format:\s*(Name.*)$", txt, re.M)
        styles = re.findall(r"^Style:\s*(.*)$", txt, re.M)
        if not (fmt and styles):
            continue
        keys = [k.strip() for k in fmt.group(1).split(",")]
        d = dict(zip(keys, [v.strip() for v in styles[0].split(",")]))
        align = d.get("Alignment", "2")
        an = re.search(r"\\an(\d)", txt)
        if an:
            align = an.group(1)
        if align not in ("1", "2", "3") or "MarginV" not in d:
            return None, align
        margins = [float(d["MarginV"])]
        ef = re.search(r"^Format:\s*(Layer.*)$", txt, re.M)
        if ef:
            ek = [k.strip() for k in ef.group(1).split(",")]
            if "MarginV" in ek:
                iv = ek.index("MarginV")
                for line in re.findall(r"^Dialogue:\s*(.*)$", txt, re.M):
                    parts = line.split(",", len(ek) - 1)
                    if len(parts) > iv and parts[iv].strip().isdigit() and int(parts[iv]) > 0:
                        margins.append(float(parts[iv]))
        for y in re.findall(r"\\pos\(\s*[-\d.]+\s*,\s*([-\d.]+)\s*\)", txt):
            margins.append(max(0.0, play_h - float(y)))
        return min(margins) * h / play_h, align
    return None, None


# ----------------------------------------------------------------- creative critique

KEYWORDS = {
    "hook-in-3s": ["hook", "هوك", "بداية", "اول", "أول", "scroll", "grab", "attention", "انتباه"],
    "dead-air": ["boring", "ممل", "slow", "بطيء", "dead", "silence", "سكوت", "drag"],
    "duration": ["long", "طويل", "short", "قصير", "length", "مدة"],
    "shot-length": ["pace", "pacing", "rhythm", "ايقاع", "إيقاع", "fast", "سريع"],
    "cuts-on-beat": ["beat", "music", "موسيقى", "بيت"],
    "caption-coverage": ["caption", "subtitle", "ترجمة", "كابشن", "نص", "text"],
    "repetition": ["repeat", "تكرار", "مكرر", "same"],
    "black-frames": ["black", "اسود", "أسود"],
}


def critique(concepts: dict | None, checks: list[dict]) -> list[dict]:
    if not concepts:
        return []
    by = {c["id"]: c for c in checks}
    items = list(concepts.get("premortem") or [])
    chosen = (concepts.get("decision") or {}).get("chosen")
    for c in concepts.get("concepts", []):
        if c.get("id") == chosen:
            items += list(c.get("risks") or [])
    out = []
    for risk in items:
        low = str(risk).lower()
        rel_ids = [cid for cid, kws in KEYWORDS.items() if any(k in low for k in kws) and cid in by]
        if rel_ids:
            bad = [cid for cid in rel_ids if not by[cid]["pass"] and not by[cid].get("skipped")]
            status = "happened" if bad else "avoided"
        else:
            status, bad = "needs-eyes", []
        out.append({"risk": risk, "related_checks": rel_ids, "status": status,
                    "note": ("premortem came true: " + ", ".join(bad)) if bad else
                    ("checks say this risk was avoided" if rel_ids else "no automatic check covers it — judge from the frames")})
    return out


# ----------------------------------------------------------------- frames + vision prompt

def extract_frames(job: Path, video: Path, edl: dict, rnd: int, dur: float) -> list[dict]:
    rdir = job / "review"
    for old in rdir.glob(f"r{rnd}_f*.jpg"):
        old.unlink()
    plan = []
    hook_end = min(HOOK_WINDOW, dur)
    for t in (0.05, hook_end / 2, max(0.05, hook_end - 0.1)):
        plan.append({"t": r3(t), "event": None, "why": "hook"})
    for ev in edl["events"]:
        s, e = out_span(ev)
        plan.append({"t": r3(min(s + 0.04, max(0.0, dur - 0.05))), "event": ev["id"], "why": "event-start"})
    frames = []
    for i, p in enumerate(plan, 1):
        if p["t"] >= dur:
            continue
        if p["event"] is None:
            p["event"] = next((ev["id"] for ev in edl["events"] if out_span(ev)[0] <= p["t"] < out_span(ev)[1]), None)
        name = f"review/r{rnd}_f{i:02d}.jpg"
        res = C.run(job, STATION, "ffmpeg.frame",
                    ["ffmpeg", "-y", "-v", "error", "-ss", f"{p['t']:.3f}", "-i", video, "-frames:v", "1",
                     "-vf", "scale=480:-2", "-q:v", "4", job / name], out=job / name, check=False)
        if res.returncode == 0 and (job / name).exists():
            frames.append({"path": name, **p})
    return frames


def vision_prompt(job: Path, rnd: int, frames: list[dict], checks: list[dict], crit: list[dict], brief: dict) -> Path:
    failed = [c for c in checks if not c["pass"]]
    lines = [
        f"# Dragon Montage — عين المخرج (round {rnd})", "",
        "انت دلوقتي المخرج اللي بيتفرج. بص على الصور دي بعينك (Read كل صورة)، وقول رأيك بذوق بني آدم مش بأرقام.",
        "You are the director watching the cut. Open every frame below (Read tool), then add taste notes.", "",
        f"**Brief:** {brief.get('one_truth') or brief.get('task', '')} · feeling: {brief.get('feeling')} · "
        f"platform: {brief.get('platform')} {brief.get('aspect')} · target {brief.get('target_seconds')}s", "",
        "## الفريمات / Frames", "",
        "| frame | t (s) | event | why |", "|---|---|---|---|",
    ]
    lines += [f"| `{f['path']}` | {f['t']} | {f['event'] or '—'} | {f['why']} |" for f in frames]
    lines += ["", "## اللي الماكينة لقيته / What the machine already flagged", ""]
    lines += [f"- ❌ **{c['id']}** — {c['evidence']}" for c in failed] or ["- كله عدّى في الفحص الآلي / all automatic checks passed"]
    if crit:
        lines += ["", "## مخاطر الـ premortem / Premortem risks to judge", ""]
        lines += [f"- [{c['status']}] {c['risk']}" for c in crit]
    lines += [
        "", "## Checklist — جاوب على كل سؤال", "",
        "1. **الهوك** — أول 3 فريمات: هل توقف الصباع عن السكرول؟ فيه وش/حركة/سؤال؟ / Does the hook grab in <1s?",
        "2. **التكوين / Composition** — الموضوع في التلت؟ الراس مش مقصوص؟ فيه فراغ زيادة؟ headroom, rule of thirds, crop.",
        "3. **الإحساس / Emotion** — الصور بتوصل الإحساس المطلوب (feeling) ولا لأ؟ does each shot serve the one truth?",
        "4. **اللون / Grade** — الألوان متسقة بين اللقطات؟ جلد طبيعي؟ consistent look, natural skin.",
        "5. **الاستمرارية / Flow** — فيه نطة غريبة بين لقطتين؟ jump cut غير مقصود؟ unmotivated jumps?",
        "6. **الكابشن والمنطقة الآمنة / Captions & safe area** — مقروء؟ بعيد عن أزرار المنصة؟",
        "7. **التكرار / Repetition** — فيه لقطتين شبه بعض؟ near-duplicate shots?",
        "8. **النهاية / Payoff** — آخر لقطة فيها قفلة أو CTA واضح؟",
        "",
        "## إزاي تضيف رأيك / How to append", "",
        "```bash",
        f"python3 .claude/skills/kosif-dragon-montage/scripts/dm_review.py review --job {job} \\",
        "  --add-note \"الهوك ضعيف: الوش صغير ومفيش حركة في أول ثانية\" \\",
        "  --fix e001:swap:\"open on c02-s003 (close-up, starts talking at 0.1s)\" \\",
        "  --fix e004:trim:\"cut the dead 1s before the line seconds=1 side=head\"",
        "```",
        "",
        f"Fix format: `EVENT:ACTION:DETAIL` — ACTION ∈ {', '.join(ACTIONS)}; EVENT is an edl id (e001…) or `*` for global.",
        "Numbers go in as key=value inside DETAIL (seconds=, side=head|tail, src_in=, src_out=, speed=, rec_at=, "
        "with_shot=, target=) — the director never reads numbers out of prose.",
        "Any --fix turns the verdict into `fix`; the director applies them with `dm_direct.py --apply-review`.",
        "",
    ]
    p = job / "review" / "VISION_PROMPT.md"
    p.write_text("\n".join(lines), encoding="utf-8")
    return p


# ----------------------------------------------------------------- scoring

def score_and_verdict(checks: list[dict], fixes: list[dict], notes_fix: bool = False) -> tuple[float, str]:
    tot = sum(WEIGHTS.get(c["id"], 1.0) for c in checks)
    got = sum(WEIGHTS.get(c["id"], 1.0) for c in checks if c["pass"])
    score = round(got / tot, 3) if tot else 0.0
    crit_fail = any(not c["pass"] and c["id"] in CRITICAL for c in checks)
    verdict = "ship" if score >= 0.85 and not crit_fail and not notes_fix else "fix"
    return score, verdict


# ----------------------------------------------------------------- commands

def cmd_review(job: Path, rnd: int | None) -> dict:
    render = C.read(job, "render")
    edl = C.read(job, "edl")
    analysis = C.read(job, "analysis")
    brief = C.read(job, "brief")
    concepts = load_optional(job, "concepts")
    look = load_optional(job, "look")
    prev = load_optional(job, "review")
    if rnd is None:
        rnd = (prev["round"] + 1) if prev else 1
    video = rel(job, render["final"])
    if not video or not video.exists():
        raise FileNotFoundError(f"final video not found: {video}")
    if not (C.have("ffmpeg") and C.have("ffprobe")):
        raise RuntimeError("ffmpeg/ffprobe not on PATH")
    (job / "review").mkdir(parents=True, exist_ok=True)

    m = measure(job, video, brief, edl)
    rv = Review(edl)
    run_checks(job, rv, m, analysis, brief, look, render)
    crit = critique(concepts, rv.checks)
    frames = extract_frames(job, video, edl, rnd, m["duration"])
    score, verdict = score_and_verdict(rv.checks, rv.fixes)
    if verdict == "fix" and not rv.fixes:
        verdict = "ship" if score >= 0.7 else "fix"
    vp = vision_prompt(job, rnd, frames, rv.checks, crit, brief)
    review = C.new("review", round=rnd, checks=rv.checks, fixes=rv.fixes,
                   frames=[f["path"] for f in frames], frame_index=frames,
                   verdict=verdict, score=score, critique=crit, notes=[], capped_fixes=rv.capped,
                   rounds_left=max(0, MAX_ROUNDS - rnd), final=str(video.relative_to(job)) if video.is_relative_to(job) else str(video),
                   vision_prompt=str(vp.relative_to(job)), missing=m["missing"],
                   measured={"duration": r3(m["duration"]), "width": m["width"], "height": m["height"],
                             "lufs": m["lufs"], "true_peak": m["true_peak"], "silences": m["silences"],
                             "black": m["black"]})
    C.write(job, "review", review)
    (job / "review" / f"review_r{rnd}.json").write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    return review


def parse_fix(spec: str, ids: set[str]) -> dict:
    parts = spec.split(":", 2)
    if len(parts) < 2:
        raise SystemExit(f"--fix must be EVENT:ACTION[:DETAIL], got {spec!r}")
    ev, act = parts[0].strip(), parts[1].strip().lower()
    detail = parts[2].strip() if len(parts) > 2 else ""
    if act not in ACTIONS:
        raise SystemExit(f"--fix action must be one of {ACTIONS}, got {act!r}")
    if ev != "*" and ev not in ids:
        raise SystemExit(f"--fix event {ev!r} is not in edl.json ({', '.join(sorted(ids))})")
    fx = {"event": ev, "action": act, "detail": detail or f"{act} (claude vision)", "check": "vision", "by": "claude"}
    # structured fields ride in the detail as key=value (seconds=0.6 side=head src_in=.. src_out=.. speed=1.2
    # rec_at=.. with_shot=.. target=captions); prose is never parsed for numbers
    for k, v in re.findall(r"\b(seconds|src_in|src_out|speed|rec_at|lufs|min_bottom)=(-?\d+(?:\.\d+)?)", detail):
        fx[k] = float(v)
    for k, v in re.findall(r"\b(side|with_shot|target|grade|role|kind)=([\w.-]+)", detail):
        fx[k] = v
    return fx


def cmd_add(job: Path, notes: list[str], fixes: list[str]) -> dict:
    review = C.read(job, "review")
    ids = {e["id"] for e in C.read(job, "edl")["events"]}
    new_fixes = [parse_fix(f, ids) for f in fixes]
    review.setdefault("notes", [])
    for n in notes:
        review["notes"].append({"text": n, "by": "claude-vision", "round": review["round"]})
    review["fixes"].extend(new_fixes)
    if new_fixes:
        review["verdict"] = "fix"
    C.write(job, "review", review)
    rp = job / "review" / f"review_r{review['round']}.json"
    if rp.parent.exists():
        rp.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    return review


def main(argv=None) -> int:
    C.utf8_stdio()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("review", help="watch final.mp4 and write review.json")
    r.add_argument("--job", required=True)
    r.add_argument("--round", type=int)
    r.add_argument("--add-note", action="append", default=[], help="append a taste note to the existing review.json")
    r.add_argument("--fix", action="append", default=[], help="EVENT:ACTION:DETAIL (with --add-note mode)")
    r.add_argument("--json", action="store_true", help="print the review JSON")
    a = ap.parse_args(argv)
    job = Path(a.job).resolve()
    if a.add_note or a.fix:
        rv = cmd_add(job, a.add_note, a.fix)
    else:
        rv = cmd_review(job, a.round)
    if a.json:
        print(json.dumps(rv, ensure_ascii=False, indent=1))
    else:
        failed = [c["id"] for c in rv["checks"] if not c["pass"]]
        print(f"round {rv['round']}: verdict={rv['verdict']} score={rv.get('score')} "
              f"failed={failed or 'none'} fixes={len(rv['fixes'])} frames={len(rv.get('frames', []))} "
              f"notes={len(rv.get('notes', []))}")
    return 0


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.exit(main())
