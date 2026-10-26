"""A filled video breakdown (brief.json from `kmotion analyze`) → one copy-paste generation block for Google Omni
Flash (native 10 s clips): a dense style line, specs, a beat-by-beat timeline compressed proportionally to the target
length, a locked typography line, a sound line on the same beats, the final held frame, and what to exclude. Custom
changes are applied before writing; anything not overridden stays faithful to the analysis.

    python scripts/kmotion.py omniprompt BREAKDOWN/brief.json [--seconds 10] [--overrides changes.json] [--out prompt.txt]

changes.json (every key optional):
    {"brand": {"from": "Horse Tinder", "to": "Qahwa", "logo": "a coffee bean inside a rounded square"},
     "palette": {"#c28136": "#0f766e", "#171411": "#0b1220"},     "text": {"Dating, for horses.": "قهوتك جاهزة."},
     "duration": 8, "aspect": "9:16", "tone": "calmer, premium", "style": "a whole new style line", "add": ["a subtle grain overlay"], "remove": ["confetti"]}
A removed element the scenes are built on (a main subject) stops the build: rewrite those beats in a copy of brief.json.
It recreates style, pacing and structure — write the original's copyrighted specifics (its logo, its characters, its
exact copy) only when they are the user's own or replaced by overrides.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FIELDS = ["composition", "camera", "subjects", "text", "typography", "icons_ui", "lighting_texture", "motion", "transition_out", "audio"]
TOP = ["style_line", "typography_lock", "sound_line", "final_frame"]
NATIVE_S = 10.0


def _apply(s: str, ov: dict) -> str:
    if not isinstance(s, str):
        return s
    for a, b in (ov.get("text") or {}).items():
        s = s.replace(a, b)
    br = ov.get("brand") or {}
    if br.get("from") and br.get("to"):
        s = re.sub(re.escape(br["from"]), br["to"], s, flags=re.I)
    for a, b in (ov.get("palette") or {}).items():
        s = re.sub(re.escape(a), b, s, flags=re.I)
    return s


def _removals(brief: dict, ov: dict) -> None:
    """A removed element that the scenes are built on cannot be find-and-replaced (a coffee cup does not gallop):
    those beats are rewritten in a copy of brief.json, keeping timing, camera, light and motion."""
    rm = ov.get("remove") or []
    hits = {r: [b["i"] for b in brief["beats"] if re.search(rf"\b{re.escape(r)}", json.dumps(b, ensure_ascii=False), re.I)] for r in rm}
    hits = {r: v for r, v in hits.items() if v}
    if hits:
        raise SystemExit("removed elements still carry scenes: " + "; ".join(f"{r!r} in beats {v}" for r, v in hits.items())
                         + " — copy brief.json, rewrite those beats around the new subject (keep timing, camera, light and motion), "
                           "then run omniprompt on the copy")


def check(brief: dict) -> list[str]:
    miss = [f"top: {k}" for k in TOP if not str(brief.get(k, "")).strip()]
    for b in brief.get("beats", []):
        miss += [f"beat {b['i']}: {k}" for k in FIELDS if not str(b.get(k, "")).strip()]
    return miss


def build(brief: dict, seconds: float | None = None, ov: dict | None = None) -> str:
    ov = ov or {}
    miss = check(brief)
    if miss:
        raise SystemExit("the breakdown is not filled — look at the frames and fill: " + ", ".join(miss[:20]) + (" …" if len(miss) > 20 else ""))
    _removals(brief, ov)
    src = float(brief["duration"])
    target = float(ov.get("duration") or seconds or (NATIVE_S if src > NATIVE_S else src))
    k = target / src
    w, h = (int(x) for x in brief["size"].split("x"))
    aspect = ov.get("aspect") or brief["aspect"]
    if ov.get("aspect") and ov["aspect"] != brief["aspect"]:
        a, b = (int(x) for x in ov["aspect"].split(":"))
        w, h = (1920, round(1920 * b / a)) if a >= b else (round(1920 * a / b), 1920)
    if min(w, h) < 1080:                                      # never ask for less than 1080 on the short side
        s = 1080 / min(w, h); w, h = round(w * s / 2) * 2, round(h * s / 2) * 2
    fps = round(float(brief.get("fps") or 30))
    style = ov.get("style") or _apply(brief["style_line"], ov)
    if ov.get("tone"):
        style = style.rstrip(". ") + f"; tone shifted: {ov['tone']}."
    L = [f"STYLE: {style}",
         f"SPECS: {w}x{h} ({aspect}), {fps} fps, {target:.1f} s, one continuous generation, pacing {brief.get('pace', '')}"
         + (f", compressed from {src:.1f} s (all timings ×{k:.2f})" if abs(k - 1) > 0.01 else "") + ", no letterbox, no watermark.",
         "TIMELINE:"]
    for b in brief["beats"]:
        t0, t1 = b["t0"] * k, b["t1"] * k
        parts = [f"{_apply(b['composition'], ov)}", f"camera: {_apply(b['camera'], ov)}", f"subjects: {_apply(b['subjects'], ov)}",
                 f"on-screen text: {_apply(b['text'], ov)} ({_apply(b['typography'], ov)})", f"icons/UI: {_apply(b['icons_ui'], ov)}",
                 f"light/texture: {_apply(b['lighting_texture'], ov)}", f"motion: {_apply(b['motion'], ov)}", f"exit: {_apply(b['transition_out'], ov)}"]
        cols = ", ".join((b.get("measured") or {}).get("palette", [])[:4])
        if cols:
            parts.insert(1, "colours " + _apply(cols, ov))
        empty = re.compile(r":\s*(none|unchanged|-)?\s*(\((none|unchanged)\))?$", re.I)
        L.append(f"[{t0:05.2f}–{t1:05.2f}s] " + "; ".join(p for p in parts if not empty.search(p)) + ".")
    if ov.get("add"):
        L.append("ADD: " + "; ".join(ov["add"]) + " — integrated in the same style, never covering the main text.")
    br = ov.get("brand") or {}
    if br.get("logo"):
        L.append(f"BRAND MARK: {br['logo']}" + (f", for the name «{br['to']}»" if br.get("to") else "") + "; it appears wherever the original shows its logo.")
    L.append(f"TYPOGRAPHY LOCK: {_apply(brief['typography_lock'], ov)}")
    beats_audio = "; ".join(f"[{b['t0'] * k:05.2f}s] {_apply(b['audio'], ov)}" for b in brief["beats"] if b.get("audio") and b["audio"].lower() not in ("none", "-"))
    L.append(f"SOUND: {_apply(brief['sound_line'], ov).rstrip('. ')}." + (f" Cues: {beats_audio}." if beats_audio else ""))
    L.append(f"FINAL FRAME (held from {brief['beats'][-1]['t0'] * k:.2f}s to {target:.2f}s): {_apply(brief['final_frame'], ov)}")
    excl = ["no extra text beyond the listed copy", "no misspelled or garbled letters", "no logos or brands not listed", "no camera shake unless listed"]
    if ov.get("remove"):
        excl = [f"no {r}" for r in ov["remove"]] + excl
    L.append("EXCLUDE: " + "; ".join(excl) + ".")
    text = "\n".join(L)
    text = text.replace("?", "")                              # one direct block: no questions
    return text


def breakdown_md(brief: dict, analysis: dict | None = None) -> str:
    """The shot-by-shot breakdown as a document another creator can rebuild from without the original."""
    a = analysis or {}
    au = a.get("audio") or {}
    L = [f"# Breakdown — {Path(str(brief.get('source', ''))).name}", "",
         f"**{brief['duration']:.2f} s · {brief['size']} ({brief['aspect']}) · {brief['fps']:g} fps** — {brief['style_line']}", "",
         f"- Pacing: {brief.get('pace')}" + (f" — {a.get('beat_count')} beats, mean {a.get('mean_beat_s')} s, {a.get('cuts_per_10s')} hard cuts / 10 s, "
                                              f"{a.get('scenes')} scenes" if a else ""),
         f"- Recurring motif: {brief.get('recurring_motif') or '—'}",
         f"- Palette (measured): {' '.join(c['hex'] for c in a.get('palette', [])[:8])}" if a else "",
         f"- Audio (measured): {au.get('lufs')} LUFS, true peak {au.get('true_peak')} dBTP, ~{au.get('bpm')} BPM, "
         f"{int(round((au.get('sfx_alignment') or 0) * 100))}% of beat edges on an onset" if au else "- Audio: none",
         f"- Typography lock: {brief['typography_lock']}", f"- Sound: {brief['sound_line']}", ""]
    for b in brief["beats"]:
        m = b.get("measured") or {}
        L += [f"## Beat {b['i']} · {b['t0']:.2f}–{b['t1']:.2f} s" + (f" · enters by {m.get('in')}" if m.get("in") else ""), "",
              f"- **Composition**: {b['composition']}", f"- **Camera**: {b['camera']}" + (f" (measured: {m['camera_guess']})" if m.get("camera_guess") else ""),
              f"- **Subjects**: {b['subjects']}", f"- **Text**: {b['text']}", f"- **Typography**: {b['typography']}", f"- **Icons / UI**: {b['icons_ui']}",
              f"- **Colour**: background {m.get('background', '—')}; palette {' '.join(m.get('palette', []))}", f"- **Light / texture**: {b['lighting_texture']}",
              f"- **Motion**: {b['motion']}", f"- **Exit**: {b['transition_out']}", f"- **Audio**: {b['audio']}", ""]
    L += [f"## Final frame", "", brief["final_frame"], ""]
    return "\n".join(x for x in L if x is not None)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("brief"); ap.add_argument("--seconds", type=float); ap.add_argument("--overrides"); ap.add_argument("--out")
    ap.add_argument("--markdown", help="also write the shot-by-shot breakdown document here")
    a = ap.parse_args()
    brief = json.loads(Path(a.brief).read_text(encoding="utf-8"))
    if a.markdown:
        an = Path(a.brief).with_name("analysis.json")
        Path(a.markdown).write_text(breakdown_md(brief, json.loads(an.read_text(encoding="utf-8")) if an.exists() else None), encoding="utf-8")
    ov = json.loads(Path(a.overrides).read_text(encoding="utf-8")) if a.overrides else {}
    text = build(brief, a.seconds, ov)
    if a.out:
        Path(a.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
