#!/usr/bin/env python3
"""Station 6 «ينفّذ» — render a kosif.dm.edl.v1 into a finished video (see ../CONTRACTS.md).

    python3 dm_render.py render --job DIR [--extra-ratios 1:1,16:9] [--preview] [--fast]

Reads  edl.json (+ analysis.json for clip paths, words and face hints, + look.json if present)
Writes render/final.mp4 (or render/preview.mp4 with --preview), render/captions.srt,
       render/captions.ass, render/words.json, render/project.fcpxml (+ Premiere XML, CapCut pack
       in render/nle/), extra ratio renders render/final_1x1.mp4 …, and render.json.

Pipeline (every ffmpeg call goes through dm_common.run → receipts.jsonl):
  timing  dm_edl.reflow is the single source of truth; events snap to whole frames (render.json.events_out);
          src ranges past the media end are clamped (warning) instead of freeze-padded.
  pass A  one filter_complex, one `-ss/-t -i` input per event (any source order, nothing extra decoded),
          ffmpeg runs in render/ so filter options only name relative files: per event trim → speed → smart cover crop to W×H (face hook) →
          camera move (punch-in / slow-push / ken-burns) → join (concat on cuts, xfade with exact
          offsets on transitions) → grade (ev.grade overrides per event) → burned ASS captions (karaoke / punchy / clean, RTL via
          libass+fribidi).  Audio: per event (silence when ev.mute) atrim/atempo with de-click fades at cuts, acrossfade on
          transitions, optional music bed ducked under speech with sidechaincompress.
  pass B  loudnorm measure (EBU R128) → pass C loudnorm linear apply to target_lufs, video copied.
  verify  kosif-superpowers/scripts/verify_video.py → render.json.verify
  export  kosif-superpowers/scripts/nle_export.py (edl → kosif.timeline.v1) → render/project.fcpxml
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dm_common as dm  # noqa: E402

STATION = "6-render"

# ----------------------------------------------------------------------------- fallback tables
# Used when data/*.json (written by another station) is missing or lacks an id.
GRADES = {
    "natural": "eq=contrast=1.02:saturation=1.04",
    "cinematic": "eq=contrast=1.08:saturation=0.92:gamma=0.98,"
                 "colorbalance=rs=-0.03:bs=0.04:rh=0.04:bh=-0.03,vignette=angle=PI/5",
    "teal_orange": "colorbalance=rs=-0.08:gs=-0.02:bs=0.10:rh=0.10:gh=0.02:bh=-0.08,"
                   "eq=saturation=1.12:contrast=1.06",
    "warm": "colorbalance=rs=0.05:bs=-0.05:rm=0.04:bm=-0.04,eq=saturation=1.05",
    "cool": "colorbalance=rs=-0.05:bs=0.05:rm=-0.03:bm=0.04,eq=saturation=0.98",
    "dramatic": "eq=contrast=1.2:saturation=0.85:brightness=-0.02,vignette=angle=PI/4",
    "vintage": "curves=preset=vintage,eq=saturation=0.85",
    "mono": "hue=s=0,eq=contrast=1.1",
}
TRANSITIONS = {"cut": "cut", "fade": "fade", "wipeleft": "wipeleft", "slideup": "slideup",
               "circleopen": "circleopen", "dissolve": "dissolve", "fadeblack": "fadeblack"}
XFADE_NAMES = {"fade", "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft", "slideright", "slideup",
               "slidedown", "circlecrop", "rectcrop", "distance", "fadeblack", "fadewhite", "radial",
               "smoothleft", "smoothright", "smoothup", "smoothdown", "circleopen", "circleclose",
               "vertopen", "vertclose", "horzopen", "horzclose", "dissolve", "pixelize", "diagtl",
               "diagtr", "diagbl", "diagbr", "hlslice", "hrslice", "vuslice", "vdslice", "hblur",
               "fadegrays", "wipetl", "wipetr", "wipebl", "wipebr", "squeezeh", "squeezev", "zoomin"}
CAMERA = {"none": {"type": "none"}, "punch-in": {"type": "static", "scale": 1.08},
          "slow-push": {"type": "push", "scale": 1.10}, "ken-burns": {"type": "pan", "scale": 1.12}}
_ASS = {"OutlineColour": "&H00000000", "BackColour": "&H80000000", "BorderStyle": 1, "Encoding": -1}
CAPTIONS = {  # ASS V4+ fields at PlayRes 1080 on the short side (Fontsize/Outline/Shadow) and H=1920 (MarginV)
    "karaoke": {"ass": {**_ASS, "Fontname": "Cairo", "Fontsize": 74, "PrimaryColour": "&H00FFFFFF",
                        "SecondaryColour": "&H0059DEFF", "Bold": -1, "Outline": 6, "Shadow": 3, "Alignment": 2,
                        "MarginV": 300}, "max_words": 5, "pop": 112, "highlight": "spoken-word"},
    "punchy": {"ass": {**_ASS, "Fontname": "Cairo", "Fontsize": 88, "PrimaryColour": "&H00FFFFFF",
                       "SecondaryColour": "&H004DE0FF", "Bold": -1, "Outline": 9, "Shadow": 0, "Alignment": 5,
                       "MarginV": 0}, "max_words": 2, "pop": 120, "highlight": "spoken-word"},
    "clean": {"ass": {**_ASS, "Fontname": "Cairo", "Fontsize": 54, "PrimaryColour": "&H00F2F2F2",
                      "SecondaryColour": "&H00F2F2F2", "Bold": 0, "Outline": 2, "Shadow": 1, "Alignment": 2,
                      "MarginV": 220}, "max_words": 7, "pop": 100, "highlight": "none"},
    "none": None,
}
FONT_FALLBACK = ["Cairo", "Tajawal", "Noto Kufi Arabic", "Noto Sans Arabic", "DejaVu Sans"]
DEFAULT_XFADE_SECONDS = 0.3
CUT_DECLICK = 0.012           # seconds of fade at each cut edge (no length change)


def _data(name: str):
    f = dm.SKILL / "data" / name
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None
    except (OSError, ValueError):
        return None


def _norm(x: str) -> str:
    return str(x).strip().lower().replace("_", "-")


def _lookup(table_file: str, key: str | None):
    """Entry `key` (id or alias, `_`≡`-`) in data/<table_file>: {list_key: [{id, aliases}]}, [{id}] or {id: {}}."""
    doc = _data(table_file)
    if doc is None or not key:
        return None
    if isinstance(doc, dict) and isinstance(doc.get(key), dict):
        return doc[key]
    items = doc
    if isinstance(doc, dict):
        items = next((v for k, v in doc.items() if isinstance(v, list) and v and isinstance(v[0], dict)), [])
    if not isinstance(items, list):
        return None
    k = _norm(key)
    for it in items:
        if isinstance(it, dict) and _norm(it.get("id", "")) == k:
            return it
    for it in items:
        if isinstance(it, dict) and k in {_norm(a) for a in it.get("aliases") or []}:
            return it
    return None


def grade_filter(gid: str | None) -> str | None:
    if not gid or gid in ("off",):
        return None
    ent = _lookup("grades.json", gid)
    if ent:
        for k in ("ffmpeg", "vf", "filter"):
            if isinstance(ent.get(k), str) and ent[k].strip():
                f = ent[k].strip()
                return None if f == "null" else f
    if gid == "none":
        return None
    return GRADES.get(gid.replace("-", "_"), GRADES["natural"])


_XF = None


def xfade_names() -> set[str]:
    """Transitions this ffmpeg's xfade knows (asked once; falls back to the 6.x list)."""
    global _XF
    if _XF is None:
        _XF = set(XFADE_NAMES)
        try:
            import subprocess
            h = subprocess.run(["ffmpeg", "-hide_banner", "-h", "filter=xfade"], capture_output=True, timeout=20,
                               **dm.TEXT).stdout
            seg = h[h.find("transition"):h.find("duration")]
            found = {ln.split()[0] for ln in seg.splitlines()[1:] if ln.strip()}
            if "fade" in found:
                _XF = found - {"custom"}
        except Exception:  # noqa: BLE001
            pass
    return _XF


def transition_name(tr: dict | None) -> tuple[str, float]:
    if not tr:
        return "cut", 0.0
    raw = str(tr.get("xfade") or tr.get("id") or "cut")
    tid = raw[len("xfade-"):] if raw.startswith("xfade-") else raw
    secs = tr.get("seconds") or tr.get("duration")
    ent = _lookup("transitions.json", raw) or _lookup("transitions.json", tid)
    if ent:
        name = ent.get("xfade") or "cut"
        secs = secs or ent.get("seconds")
    else:
        name = TRANSITIONS.get(tid) or (tid if tid in xfade_names() else "fade")
    if name == "cut":
        return "cut", 0.0
    if name not in xfade_names():
        name = "fade"
    return name, float(secs or DEFAULT_XFADE_SECONDS)


def camera_filters(cam: dict | None, W: int, H: int, fps: float, dur: float) -> tuple[str, list[str]]:
    """(resolved id, filters). Uses data/camera.json templates (shared vocabulary) when present,
    else the built-in table. Runs on frames already scaled to W×H at `fps`."""
    if not cam:
        return "none", []
    cid = str(cam.get("id") or "none")
    params = {k: v for k, v in cam.items() if k != "id"}
    ent = _lookup("camera.json", cid)
    if ent and isinstance(ent.get("ffmpeg"), str):
        defaults = dict(ent.get("defaults") or {})
        p = {**defaults, **{k: v for k, v in params.items() if k in defaults}}
        if "amount" in defaults and "amount" not in params and params.get("scale"):
            p["amount"] = round(float(params["scale"]) - 1.0, 4)
        ctx = {"W": W, "H": H, "W2": W * 2, "H2": H * 2, "fps": f"{fps:g}", "frames": max(1, round(dur * fps)), **p}
        try:
            f = ent["ffmpeg"].format(**ctx)
            return ent["id"], ([] if f.strip() == "null" else [f])
        except (KeyError, IndexError, ValueError):
            pass
    spec = dict(CAMERA.get(cid) or ({"type": "static", "scale": 1.08} if cid != "none" else {"type": "none"}))
    if params.get("scale"):
        spec["scale"] = float(params["scale"])
    t, sc = spec.get("type", "none"), float(spec.get("scale") or 1.0)
    if t == "none" or sc <= 1.0001:
        return cid, []
    if t == "static":
        sw, sh = round(W * sc / 2) * 2, round(H * sc / 2) * 2
        return cid, [f"scale={sw}:{sh}:flags=bicubic", f"crop={W}:{H}:(iw-{W})/2:(ih-{H})/2"]
    k = (sc - 1.0) / max(dur, 0.1)          # progressive zoom: per-frame scale then a fixed crop
    z = f"(1+{k:.6f}*t)"
    pan = f"(iw-{W})*min(t/{max(dur, 0.1):.3f}\\,1)" if t == "pan" else f"(iw-{W})/2"
    return cid, [f"scale=w='2*trunc({W}*{z}/2)':h='2*trunc({H}*{z}/2)':eval=frame:flags=bicubic",
                 f"crop={W}:{H}:x='{pan}':y='(ih-{H})/2'"]


def caption_style(style: str, look: dict | None) -> dict | None:
    if not style or style == "none":
        return None
    base = CAPTIONS.get(style) or CAPTIONS["karaoke"]
    st = {"ass": dict(base["ass"]), "max_words": base["max_words"], "pop": base["pop"], "highlight": base["highlight"]}
    ent = _lookup("caption_styles.json", style)
    if ent and isinstance(ent.get("ass"), dict):
        st["ass"].update({k: v for k, v in ent["ass"].items() if v is not None})
        for k in ("max_words", "pop", "highlight"):
            if ent.get(k) is not None:
                st[k] = ent[k]
    st["style"] = style
    st["max_words"] = max(1, int(st["max_words"] or 1))
    lc = (look or {}).get("captions") or {}
    if lc.get("font"):
        st["ass"]["Fontname"] = lc["font"]
    if lc.get("position") in ("center", "middle"):
        st["ass"]["Alignment"], st["ass"]["MarginV"] = 5, 0
    elif lc.get("position") in ("lower", "bottom"):
        st["ass"]["Alignment"] = 2
        st["ass"]["MarginV"] = st["ass"].get("MarginV") or 300
    fb = (_data("caption_styles.json") or {}).get("font_fallback") or FONT_FALLBACK
    st["fallback"] = [st["ass"]["Fontname"]] + [f for f in fb if f != st["ass"]["Fontname"]] + ["DejaVu Sans"]
    return st


# ----------------------------------------------------------------------------- helpers
FONT_DIRS = [dm.SKILL / "assets" / "fonts", dm.VENDOR_SS / "kosif-mimic" / "assets" / "fonts",
             dm.SKILLS / "kosif-superpowers" / "proofs" / "_shared" / "fonts", dm.ROOT / "assets" / "fonts"]


SAFE_AREA = {"9:16": {"bottom": 0.22, "top": 0.10}, "4:5": {"bottom": 0.14, "top": 0.08},
             "1:1": {"bottom": 0.10, "top": 0.06}, "16:9": {"bottom": 0.08, "top": 0.06}}


def safe_area(W: int, H: int) -> tuple[str, dict]:
    """(aspect key, {bottom, top, …}) from caption_styles.json safe_area, nearest W/H wins."""
    table = {k: v for k, v in ((_data("caption_styles.json") or {}).get("safe_area") or SAFE_AREA).items()
             if isinstance(v, dict)} or SAFE_AREA

    def ratio(k):
        a, b = k.split(":")
        return float(a) / float(b)
    key = min(table, key=lambda k: abs(math.log(ratio(k)) - math.log(W / max(1, H))))
    return key, table[key]


def caption_margin_v(st: dict, W: int, H: int, min_bottom_frac: float | None = None) -> int:
    """MarginV in output pixels. Bottom-aligned captions (Alignment 1-3) are lifted out of the platform
    UI band: never below safe_area.bottom·H, nor below edl.captions.min_bottom_frac·H (review fix)."""
    a = st["ass"]
    mv = float(a.get("MarginV", 0)) * H / 1920.0
    al = int(a.get("Alignment", 2))
    _, sa = safe_area(W, H)
    if al in (1, 2, 3):
        mv = max(mv, float(sa.get("bottom", 0)) * H, float(min_bottom_frac or 0) * H)
    elif al in (7, 8, 9):
        mv = max(mv, float(sa.get("top", 0)) * H)
    return int(math.ceil(mv))


def find_font(families: list[str]) -> tuple[str, Path | None]:
    """First family found in the repo font folders (→ fontsdir for libass) or installed (fc-list)."""
    import subprocess
    installed = ""
    if shutil.which("fc-list"):
        installed = subprocess.run(["fc-list", ":", "family"], capture_output=True, timeout=30, **dm.TEXT).stdout.lower()
    for fam in families:
        key = fam.lower().replace(" ", "")
        for d in FONT_DIRS:
            if d.is_dir() and any(p.name.lower().replace(" ", "").startswith(key) for p in d.glob("*.[ot]tf")):
                return fam, d
        if fam.lower() in installed:
            return fam, None
    return "DejaVu Sans", None


def ff_quote(rel: str) -> str:
    """Quote a *relative* filename for a filtergraph option. ffmpeg runs with cwd=render/, so filter
    options never carry an absolute path: on Windows `C:\\…` breaks the filtergraph parser (':' and '\\'
    are option/escape characters)."""
    return "'" + str(rel).replace("\\", "/").replace("'", "") + "'"


def stage_fonts(font_dir: Path | None, family: str, rdir: Path) -> str | None:
    """Copy the caption family's font files next to the render (render/_fonts) so libass gets a relative
    fontsdir. Returns the relative folder name, or None when the family is installed system-wide."""
    if not font_dir or not Path(font_dir).is_dir():
        return None
    key = family.lower().replace(" ", "")
    files = [p for p in Path(font_dir).glob("*.[ot]tf") if p.name.lower().replace(" ", "").startswith(key)]
    if not files:
        return None
    dst = rdir / "_fonts"
    dst.mkdir(parents=True, exist_ok=True)
    for f in files:
        t = dst / f.name
        if not t.exists() or t.stat().st_size != f.stat().st_size:
            shutil.copyfile(f, t)
    return "_fonts"


def ratio_size(ratio: str, base_w: int, base_h: int) -> tuple[int, int]:
    if ratio in dm.ASPECTS:
        w, h = dm.ASPECTS[ratio]
    else:
        a, b = (float(x) for x in re.split(r"[:x]", ratio))
        long = max(base_w, base_h)
        w, h = (long, long * b / a) if a >= b else (long * a / b, long)
    return int(w) // 2 * 2, int(h) // 2 * 2


def atempo_chain(speed: float) -> list[str]:
    out, s = [], speed
    while s > 2.0:
        out.append("atempo=2.0")
        s /= 2.0
    while s < 0.5:
        out.append("atempo=0.5")
        s /= 0.5
    if abs(s - 1.0) > 1e-6:
        out.append(f"atempo={s:.6f}")
    return out


def resolve_media(job: Path, raw: str | None) -> Path | None:
    if not raw:
        return None
    p = Path(raw).expanduser()
    return p if p.is_absolute() else (job / p)


def face_center(ev: dict, clip: dict) -> tuple[float, float]:
    """Hook for smart crop: normalized (cx, cy) of the subject. Uses, in order, event.crop_center,
    the shot's face_center / faces_box from analysis, else the frame centre."""
    if isinstance(ev.get("crop_center"), (list, tuple)) and len(ev["crop_center"]) == 2:
        return float(ev["crop_center"][0]), float(ev["crop_center"][1])
    for sh in clip.get("shots") or []:
        if sh.get("id") == ev.get("shot") or (sh.get("start", 0) <= ev["src_in"] < sh.get("end", -1)):
            fc = sh.get("face_center")
            if isinstance(fc, (list, tuple)) and len(fc) == 2:
                return float(fc[0]), float(fc[1])
            fb = sh.get("faces_box")
            if isinstance(fb, (list, tuple)) and len(fb) == 4:
                return float(fb[0]) + float(fb[2]) / 2, float(fb[1]) + float(fb[3]) / 2
    return 0.5, 0.5


# ----------------------------------------------------------------------------- plan
def plan_timeline(edl: dict, fps: float) -> list[dict]:
    """Place every event on the output timeline in whole frames. Timing comes from dm_edl.reflow (the one
    source of truth that direct and review also use): each event starts on the frame nearest its reflowed
    rec_in and lasts round((rec_in + seconds)·fps) − round(rec_in·fps) frames; a transition overlaps by the
    frames between the previous end and that start. Cuts are made contiguous, so frame drift never builds up."""
    import copy
    import dm_edl
    e2 = dm_edl.reflow(copy.deepcopy(edl))
    plan, prev_end = [], 0
    for i, ev in enumerate(e2["events"]):
        speed = float(ev.get("speed") or 1.0)
        rec_in = float(ev["rec_in"])
        a_f = round(rec_in * fps)
        n = max(2, round((rec_in + dm_edl.event_seconds(ev)) * fps) - a_f)
        tname, td_f = "cut", 0
        if i and dm_edl.overlap(ev) > 0:
            td_f = min(prev_end - a_f, n - 1, plan[-1]["frames"] - 1)
            if td_f >= 1:
                tname = transition_name(ev.get("transition_in"))[0]
                if tname == "cut":
                    tname = "fade"
            else:
                td_f = 0
        start_f = prev_end - td_f
        plan.append({"ev": ev, "i": i, "speed": speed, "frames": n, "dur": n / fps, "start": start_f / fps,
                     "start_f": start_f, "end_f": start_f + n, "trans": tname, "td": td_f / fps, "td_f": td_f})
        prev_end = start_f + n
    return plan


def clamp_to_media(job: Path, edl: dict, clips: dict) -> tuple[dict, list[str]]:
    """Copy of edl whose src ranges stay inside each clip's real duration (analysis, else ffprobe).
    Asking for frames past the end used to freeze-pad silently; now the range is clamped (or the event
    dropped when nothing is left) and render.json says so."""
    import copy
    edl = copy.deepcopy(edl)
    fps = float(edl.get("fps") or 30)
    warnings, keep, durs = [], [], {}
    for ev in edl["events"]:
        cid = ev["clip"]
        if cid not in durs:
            d = (clips.get(cid) or {}).get("duration")
            src = resolve_media(job, ev.get("path") or (clips.get(cid) or {}).get("path"))
            if not d and src and src.is_file():
                try:
                    d = float(dm.probe(src).get("format", {}).get("duration") or 0) or None
                except Exception:  # noqa: BLE001
                    d = None
            durs[cid] = float(d) if d else None
        d = durs[cid]
        if d and float(ev["src_out"]) > d + 1e-3:
            if float(ev["src_in"]) >= d - 2 / fps:
                warnings.append(f"{ev['id']}: src {ev['src_in']}–{ev['src_out']}s is past the end of {cid} "
                                f"({d:.3f}s): event dropped")
                continue
            warnings.append(f"{ev['id']}: src_out {ev['src_out']}s > {cid} duration {d:.3f}s: clamped to {d:.3f}s")
            ev["src_out"] = round(d, 3)
        keep.append(ev)
    if not keep:
        raise RuntimeError("no event left inside its media after clamping src ranges to clip durations")
    edl["events"] = keep
    return edl, warnings


def event_grade(ev: dict) -> str | None:
    g = ev.get("grade")
    return (g.get("id") if isinstance(g, dict) else g) or None


def remap_words(plan: list[dict], clips: dict) -> list[dict]:
    """Source-time words → output-timeline words (only words inside each event's window)."""
    out = []
    for p in plan:
        ev, clip = p["ev"], clips.get(p["ev"]["clip"]) or {}
        if ev.get("mute"):                     # muted b-roll: its natural sound is not heard, so no captions
            continue
        a, b, s = float(ev["src_in"]), float(ev["src_out"]), p["speed"]
        lo = p["start"] + (p["td"] / 2 if p["td"] else 0)
        hi = p["start"] + p["dur"]
        for w in clip.get("words") or []:
            text = str(w.get("w") or w.get("word") or w.get("text") or "").strip()
            ws, we = float(w["start"]), float(w["end"])
            if not text or we <= a or ws >= b:
                continue
            mid = (max(ws, a) + min(we, b)) / 2
            if not (a <= mid <= b):
                continue
            t0 = max(lo, p["start"] + (max(ws, a) - a) / s)
            t1 = min(hi, p["start"] + (min(we, b) - a) / s)
            if t1 - t0 >= 0.04:
                out.append({"word": text, "start": round(t0, 3), "end": round(t1, 3), "event": ev["id"]})
    out.sort(key=lambda w: w["start"])
    for i in range(1, len(out)):              # no overlaps after xfades
        if out[i]["start"] < out[i - 1]["end"]:
            out[i - 1]["end"] = out[i]["start"]
    return [w for w in out if w["end"] - w["start"] >= 0.03]


def phrases(words: list[dict], max_words: int, pause: float = 0.45, max_chars: int = 32) -> list[list[dict]]:
    out, cur = [], []
    for w in words:
        if cur and (w["start"] - cur[-1]["end"] > pause or len(cur) >= max_words
                    or w.get("event") != cur[-1].get("event")
                    or len(" ".join(x["word"] for x in cur)) + len(w["word"]) + 1 > max_chars):
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return out


def _ts_ass(t: float) -> str:
    cs = max(0, round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _ts_srt(t: float) -> str:
    ms = max(0, round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _ass_text(s: str) -> str:
    return s.replace("\\", "⧵").replace("{", "(").replace("}", ")").replace("\n", " ")


def write_srt(path: Path, words: list[dict]) -> int:
    ph = phrases(words, 7, max_chars=42)
    path.write_text("\n".join(f"{i}\n{_ts_srt(p[0]['start'])} --> {_ts_srt(p[-1]['end'])}\n"
                              f"{' '.join(w['word'] for w in p)}\n" for i, p in enumerate(ph, 1)),
                    encoding="utf-8")
    return len(ph)


def write_ass(path: Path, words: list[dict], st: dict, W: int, H: int) -> int:
    """RTL-safe ASS. Each word gets its own Dialogue showing the whole phrase with the spoken word
    recoloured (+ a small pop). No \\k sweep (it runs left-to-right and breaks on Arabic), no manual
    reshaping: Encoding -1 lets libass (fribidi + HarfBuzz) find the RTL paragraph direction."""
    a = st["ass"]
    k_short = min(W, H) / 1080.0
    size = max(14, round(float(a["Fontsize"]) * k_short))
    outline = round(float(a.get("Outline", 4)) * k_short, 1)
    shadow = round(float(a.get("Shadow", 0)) * k_short, 1)
    marg_v = caption_margin_v(st, W, H, st.get("min_bottom_frac"))
    marg_lr = round(W * 0.07)
    head = (
        "[Script Info]\nScriptType: v4.00+\nWrapStyle: 0\nScaledBorderAndShadow: yes\n"
        f"PlayResX: {W}\nPlayResY: {H}\nYCbCr Matrix: TV.709\n\n"
        "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, "
        "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Cap,{st['font']},{size},{a['PrimaryColour']},{a['SecondaryColour']},{a['OutlineColour']},"
        f"{a['BackColour']},{-1 if int(a.get('Bold', 0)) else 0},0,0,0,100,100,0,0,{a.get('BorderStyle', 1)},"
        f"{outline},{shadow},{a.get('Alignment', 2)},{marg_lr},{marg_lr},{marg_v},{a.get('Encoding', -1)}\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    lines = []
    hl = st.get("highlight") not in (None, "none", False) and a["SecondaryColour"] != a["PrimaryColour"]
    hcol = a["SecondaryColour"].rstrip("&") + "&"
    pop = int(st.get("pop") or 100)
    for ph in phrases(words, st["max_words"]):
        if hl:
            for k, w in enumerate(ph):
                end = ph[k + 1]["start"] if k + 1 < len(ph) else w["end"]
                parts = []
                for j, x in enumerate(ph):
                    t = _ass_text(x["word"])
                    if j == k:
                        tag = f"\\c{hcol}" + (f"\\fscx{pop}\\fscy{pop}" if pop != 100 else "")
                        t = "{" + tag + "}" + t + "{\\r}"
                    parts.append(t)
                lines.append(f"Dialogue: 0,{_ts_ass(w['start'])},{_ts_ass(end)},Cap,,0,0,0,," + " ".join(parts))
        else:
            lines.append(f"Dialogue: 0,{_ts_ass(ph[0]['start'])},{_ts_ass(ph[-1]['end'])},Cap,,0,0,0,,"
                         + " ".join(_ass_text(x["word"]) for x in ph))
    path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


# ----------------------------------------------------------------------------- graph
def build_graph(job: Path, edl: dict, plan: list[dict], clips: dict, W: int, H: int, fps: float,
                grade: str | None, ass: str | None, font_dir: str | None, music: dict | None,
                global_grade_id: str | None = None) -> tuple[list, str, float, list]:
    """inputs + filtergraph. Every event is its own input, opened with `-ss in -t len` (fast seek, then
    exact): events from one source in any order never share a decoder (a shared [0:a] fed to two atrims
    starves acrossfade when the later one needs earlier source time → silent output), nothing past the
    event is decoded, and no frames are queued for later events. `ass`/`font_dir` are names relative to
    render/ (ffmpeg runs there). A per-event grade (ev.grade, set by a review regrade) replaces the
    global grade for that event; muted events (ev.mute) contribute silence."""
    inputs, warnings, has_audio = [], [], {}
    n_in = 0
    ev_in = []
    for p in plan:
        ev = p["ev"]
        cid = ev["clip"]
        src = resolve_media(job, ev.get("path") or (clips.get(cid) or {}).get("path"))
        if not src or not src.is_file():
            raise FileNotFoundError(f"event {ev['id']}: media for clip {cid} not found ({src})")
        if cid not in has_audio:
            c = clips.get(cid) or {}
            if "has_audio" in c:
                has_audio[cid] = bool(c["has_audio"])
            else:
                pr = dm.probe(src)
                has_audio[cid] = any(s.get("codec_type") == "audio" for s in pr.get("streams", []))
        a, b = float(ev["src_in"]), float(ev["src_out"])
        inputs += ["-ss", f"{a:.4f}", "-t", f"{b - a + 0.25:.4f}", "-i", str(src.resolve())]
        ev_in.append(n_in)
        n_in += 1
    per_event_grade = any(event_grade(p["ev"]) for p in plan)
    F = f"{fps:g}"
    g = []
    for p, i in zip(plan, ev_in):
        ev, k = p["ev"], p["i"]
        a, b, s = float(ev["src_in"]), float(ev["src_out"]), p["speed"]
        cx, cy = face_center(ev, clips.get(ev["clip"]) or {})
        cx, cy = min(max(cx, 0.0), 1.0), min(max(cy, 0.0), 1.0)
        gf = None
        if per_event_grade:
            gid = event_grade(ev) or global_grade_id
            gf = grade_filter(gid) if gid else grade
        vf = ["setpts=PTS-STARTPTS", f"trim=end={b - a:.4f}", f"setpts=(PTS-STARTPTS)/{s:.6f}",
              f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=bicubic",
              f"crop={W}:{H}:x='clip(iw*{cx:.4f}-{W / 2:g},0,iw-{W})':y='clip(ih*{cy:.4f}-{H / 2:g},0,ih-{H})'", "setsar=1",
              f"fps={F}", "tpad=stop_mode=clone:stop_duration=2", f"trim=end_frame={p['frames']}",
              "setpts=PTS-STARTPTS",
              *camera_filters(ev.get("camera"), W, H, fps, p["dur"])[1],
              *([gf] if gf else []),
              f"fps={F}", "setsar=1", "format=yuv420p", "settb=AVTB"]
        g.append(f"[{i}:v]" + ",".join(vf) + f"[v{k}]")
        d = f"{p['dur']:.6f}"
        fades = [f"afade=t=in:d={CUT_DECLICK}", f"afade=t=out:st={p['dur'] - CUT_DECLICK:.6f}:d={CUT_DECLICK}"]
        if has_audio[ev["clip"]] and not ev.get("mute"):
            af = ["asetpts=PTS-STARTPTS", f"atrim=end={b - a:.4f}", "asetpts=PTS-STARTPTS", *atempo_chain(s),
                  "aresample=48000", "aformat=sample_fmts=fltp:channel_layouts=stereo",
                  "apad", f"atrim=end={d}", "asetpts=PTS-STARTPTS", *fades]
            g.append(f"[{i}:a]" + ",".join(af) + f"[a{k}]")
        else:
            g.append(f"anullsrc=r=48000:cl=stereo,atrim=end={d},aformat=sample_fmts=fltp[a{k}]")
    # join
    vacc, aacc = "v0", "a0"
    for p in plan[1:]:
        k = p["i"]
        if p["trans"] == "cut":
            g.append(f"[{vacc}][v{k}]concat=n=2:v=1:a=0[vj{k}]")
            g.append(f"[{aacc}][a{k}]concat=n=2:v=0:a=1[aj{k}]")
        else:
            g.append(f"[{vacc}][v{k}]xfade=transition={p['trans']}:duration={p['td']:.6f}:offset={p['start']:.6f}[vj{k}]")
            g.append(f"[{aacc}][a{k}]acrossfade=d={p['td']:.6f}:c1=tri:c2=tri[aj{k}]")
        vacc, aacc = f"vj{k}", f"aj{k}"
    L = plan[-1]["end_f"] / fps
    post = []
    if grade and not per_event_grade:
        post.append(grade)
    if ass:
        post.append(f"ass=filename={ff_quote(ass)}" + (f":fontsdir={ff_quote(font_dir)}" if font_dir else ""))
    post += ["format=yuv420p"]
    g.append(f"[{vacc}]" + ",".join(post) + "[vout]")
    voice = f"[{aacc}]"
    any_voice = any(has_audio[p["ev"]["clip"]] and not p["ev"].get("mute") for p in plan)
    if music:
        mi = n_in
        inputs = inputs + ["-stream_loop", "-1", "-i", str(Path(music["path"]).resolve())]
        gain = float(music.get("gain_db", -18))
        duck = abs(float(music.get("duck_under_speech_db", -10)))
        g.append(f"[{mi}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
                 f"atrim=end={L:.6f},asetpts=PTS-STARTPTS,volume={gain}dB,"
                 f"afade=t=in:d=0.5,afade=t=out:st={max(0.0, L - 1.0):.3f}:d=1.0[mus]")
        if any_voice and duck > 0:
            ratio = min(20.0, max(2.0, 10 ** (duck / 20) * 2))
            g.append(f"{voice}asplit=2[vo][sc]")
            g.append(f"[mus][sc]sidechaincompress=threshold=0.03:ratio={ratio:.2f}:attack=15:release=350:"
                     f"makeup=1[duck]")
            g.append("[vo][duck]amix=inputs=2:duration=first:normalize=0,"
                     f"apad,atrim=end={L:.6f}[aout]")
        else:
            g.append(f"{voice}[mus]amix=inputs=2:duration=first:normalize=0,apad,atrim=end={L:.6f}[aout]")
    else:
        g.append(f"{voice}apad,atrim=end={L:.6f}[aout]")
    return inputs, ";\n".join(g), L, warnings


# ----------------------------------------------------------------------------- loudnorm
TP_CEILING = -1.0      # dBTP the delivered file must stay under (verify_video / dm_review audio-clipping)
TP_INTERNAL = -1.5     # loudnorm TP target; the true-peak limiter below sits under it (AAC adds overshoot)


def measure_true_peak(job: Path, media: Path, owner_media: bool = True) -> float | None:
    """True peak (dBTP, 4x oversampled ebur128) of the delivered file's audio."""
    res = dm.run(job, STATION, "ffmpeg.ebur128-truepeak", ["ffmpeg", "-hide_banner", "-nostats", "-i", media,
                 "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"], owner_media=owner_media, check=False)
    m = re.findall(r"Peak:\s+(-?[\d.]+|-inf)\s+dBFS", res.stderr)
    if not m:
        return None
    return float("-inf") if m[-1] == "-inf" else float(m[-1])


def loudnorm(job: Path, master: Path, out: Path, target: float, tp: float, owner_media: bool,
             limiter_tp: float | None = None) -> dict:
    """Two-pass loudnorm, then a 4x-oversampled limiter at `limiter_tp` (edl.audio.limiter_tp, lowered by
    dm_direct --apply-review after an audio-clipping fail). The AAC file is measured; if it still peaks above
    min(TP_CEILING, limiter_tp) it is re-encoded once with the excess (+0.3 dB) taken off."""
    lra = 11
    ceiling = min(TP_CEILING, float(limiter_tp)) if limiter_tp is not None else TP_CEILING
    tp = min(tp, ceiling - 0.5)
    lim_db = ceiling - 0.8                     # head-room for AAC inter-sample overshoot
    res = dm.run(job, STATION, "ffmpeg.loudnorm-measure",
                 ["ffmpeg", "-hide_banner", "-nostats", "-i", master, "-map", "0:a:0",
                  "-af", f"loudnorm=I={target}:TP={tp}:LRA={lra}:print_format=json", "-f", "null", "-"],
                 owner_media=owner_media)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", res.stderr, re.S)
    meas = json.loads(m.group(0)) if m else {}
    norm = f"loudnorm=I={target}:TP={tp}:LRA={lra}"
    if meas and all(math.isfinite(float(meas.get(k, "nan"))) for k in ("input_i", "input_tp", "input_lra", "input_thresh")):
        norm += (f":measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:measured_LRA={meas['input_lra']}"
                 f":measured_thresh={meas['input_thresh']}:offset={meas.get('target_offset', 0)}:linear=true")

    try:   # keep the audio exactly as long as the picture (resampling/AAC priming can add a few frames)
        def _sdur(st):   # mp4 has stream duration; mkv keeps it in tags.DURATION (HH:MM:SS.ns)
            if st.get("duration"):
                return float(st["duration"])
            h, m_, sec = (st.get("tags") or {}).get("DURATION", "").split(":")
            return int(h) * 3600 + int(m_) * 60 + float(sec)
        vdur = next(_sdur(st) for st in dm.probe(master)["streams"] if st.get("codec_type") == "video")
    except Exception:
        vdur = None

    def apply(extra_db: float = 0.0):
        chain = [norm, "aresample=192000",
                 f"alimiter=limit={10 ** (lim_db / 20):.5f}:attack=1:release=60:level=disabled",
                 "aresample=48000"]
        if extra_db:
            chain.insert(1, f"volume={extra_db:.2f}dB")
        dm.run(job, STATION, "ffmpeg.loudnorm-apply",
               ["ffmpeg", "-y", "-hide_banner", "-v", "error", "-i", master, "-map", "0:v:0", "-map", "0:a:0",
                "-c:v", "copy", "-af", ",".join(chain + ([f"atrim=end={max(0.0, vdur - 1024 / 48000):.6f}"] if vdur else [])),
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out], out=out, owner_media=owner_media)
        return measure_true_peak(job, out, owner_media)

    peak = apply()
    passes = 1
    if peak is not None and math.isfinite(peak) and peak > ceiling - 0.1:
        peak = apply(-(peak - ceiling + 0.4))
        passes = 2
    meas = dict(meas)
    meas["limiter"] = {"ceiling_dbtp": ceiling, "limit_db": round(lim_db, 2), "loudnorm_tp": tp,
                       "output_true_peak": peak, "passes": passes}
    return meas


# ----------------------------------------------------------------------------- one render
def render_one(job: Path, edl: dict, analysis: dict, look: dict | None, W: int, H: int, out: Path,
               preview: bool, fast: bool, tag: str = "") -> dict:
    fps = float(edl.get("fps") or 30)
    clips = {c["id"]: c for c in (analysis or {}).get("clips", [])}
    plan = plan_timeline(edl, fps)
    rdir = job / "render"
    words = remap_words(plan, clips)
    cap = edl.get("captions") or {}
    style_id = cap.get("style") or ((look or {}).get("captions") or {}).get("style") or "karaoke"
    st = caption_style(style_id, look) if cap.get("enabled", True) else None
    ass, font_dir, n_cues = None, None, 0
    if st:
        st["min_bottom_frac"] = cap.get("min_bottom_frac")   # set by dm_direct --apply-review on a safe-area fail
    if st and words:
        st["font"], font_dir = find_font(st["fallback"])   # DejaVu Sans has Arabic glyphs as last resort
        ass = rdir / f"captions{tag}.ass"
        n_cues = write_ass(ass, words, st, W, H)
    fonts_rel = stage_fonts(font_dir, st["font"], rdir) if (st and ass) else None
    safe = None
    if st:
        akey, sa = safe_area(W, H)
        mv = caption_margin_v(st, W, H, st.get("min_bottom_frac"))
        safe = {"aspect": akey, "bottom_frac": sa.get("bottom"), "alignment": int(st["ass"].get("Alignment", 2)),
                "margin_v": mv, "margin_v_frac": round(mv / H, 4)}
    gid = (edl.get("grade") or {}).get("id") or ((look or {}).get("grade") or {}).get("id")
    gf = grade_filter(gid)
    mus = (edl.get("audio") or {}).get("music") or {}
    music = None
    if mus.get("path"):
        mp = resolve_media(job, mus["path"])
        if mp and mp.is_file():
            music = {**mus, "path": mp}
    inputs, graph, L, warnings = build_graph(job, edl, plan, clips, W, H, fps, gf, ass.name if ass else None,
                                             fonts_rel, music, gid)
    if mus.get("path") and not music:
        warnings.append(f"music bed not found: {mus['path']}")
    gfile = rdir / f"graph{tag}.txt"
    gfile.write_text(graph, encoding="utf-8")
    master = rdir / f"_master{tag}.mkv"
    venc = (["-c:v", "libx264", "-preset", "ultrafast", "-crf", "30"] if preview else
            ["-c:v", "libx264", "-preset", "veryfast" if fast else "medium", "-crf", "20" if fast else "18"])
    # cwd=render/: the filtergraph names captions*.ass and _fonts relatively (Windows drive paths break it)
    dm.run(job, STATION, "ffmpeg.render", ["ffmpeg", "-y", "-hide_banner", "-v", "error", *inputs,
           "-filter_complex_script", gfile.name, "-map", "[vout]", "-map", "[aout]", *venc,
           "-pix_fmt", "yuv420p", "-r", f"{fps:g}", "-c:a", "pcm_s16le", "-ar", "48000", master.name],
           out=master, timeout=3600, cwd=rdir)
    target = float((edl.get("audio") or {}).get("target_lufs", -14))
    meas = loudnorm(job, master, out, target, TP_INTERNAL, True, (edl.get("audio") or {}).get("limiter_tp"))
    master.unlink(missing_ok=True)
    return {"out": out, "duration": round(L, 3), "words": words, "ass": ass, "cues": n_cues,
            "font_dir": str(font_dir) if font_dir else None, "font": st["font"] if st else None,
            "grade": gid, "grade_filter": gf, "music": bool(music), "loudnorm_measured": meas,
            "plan": plan, "warnings": warnings, "fps": fps, "safe": safe}


# ----------------------------------------------------------------------------- verify + export
def verify(job: Path, video: Path, W: int, H: int, fps: float, duration: float, lufs: float) -> dict:
    vj = video.with_suffix(".verify.json")
    script = dm.SP / "verify_video.py"
    if not script.exists():
        return {"tool": "verify_video", "pass": None, "error": "verify_video.py missing"}
    res = dm.run(job, STATION, "verify_video", [*dm.py(script), video, "--aspect", f"{W}x{H}", "--fps", f"{fps:g}",
                 "--duration", f"{duration:.3f}", "--lufs", f"{lufs:g}", "--json", vj], check=False)
    rep = json.loads(vj.read_text(encoding="utf-8")) if vj.exists() else {}
    lu = rep.get("loudness") or {}
    return {"tool": "verify_video", "pass": res.returncode == 0, "rc": res.returncode,
            "lufs": lu.get("integrated_lufs"), "true_peak": lu.get("true_peak_dbfs"),
            "duration": rep.get("duration_s"), "width": rep.get("width"), "height": rep.get("height"),
            "failed": [c["check"] for c in rep.get("checks", []) if c.get("pass") is False or c.get("status") == "FAIL"],
            "report": str(vj.relative_to(job))}


def _absolute(job: Path, edl: dict, analysis: dict) -> tuple[dict, dict]:
    """Copies of edl/analysis whose media paths are absolute (converters resolve against the cwd)."""
    import copy
    edl, analysis = copy.deepcopy(edl), copy.deepcopy(analysis or {"clips": []})
    for c in analysis.get("clips", []):
        if c.get("path"):
            c["path"] = str(resolve_media(job, c["path"]).resolve())
    mus = (edl.get("audio") or {}).get("music") or {}
    if mus.get("path"):
        mp = resolve_media(job, mus["path"])
        mus["path"] = str(mp.resolve()) if mp and mp.is_file() else None
    return edl, analysis


def edl_to_timeline(edl: dict, analysis: dict, job: Path, fps: float) -> dict:
    """Local kosif.dm.edl.v1 → kosif.timeline.v1 (nle_export input), used when dm_edl.py is absent.
    Speed is not carried by nle_export: such clips keep their source in-point and output length."""
    clips = {c["id"]: c for c in (analysis or {}).get("clips", [])}
    plan = plan_timeline(edl, fps)
    vclips = []
    for p in plan:
        ev = p["ev"]
        src = resolve_media(job, ev.get("path") or (clips.get(ev["clip"]) or {}).get("path"))
        vclips.append({"id": ev["id"], "path": str(src), "start": round(p["start"], 3), "duration": round(p["dur"], 3),
                       "in": float(ev["src_in"]), "include_audio": bool((clips.get(ev["clip"]) or {}).get("has_audio", True)),
                       "fade_in": round(p["td"], 3) if p["td"] else 0})
    tracks = [{"id": "V1", "kind": "video", "clips": vclips}]
    total = max(p["start"] + p["dur"] for p in plan)
    mus = (edl.get("audio") or {}).get("music") or {}
    if mus.get("path"):
        tracks.append({"id": "A1", "kind": "audio", "clips": [{"id": "music", "path": mus["path"], "start": 0,
                       "duration": round(total, 3), "in": 0,
                       "volume": round(10 ** (float(mus.get("gain_db", -18)) / 20), 4)}]})
    return {"schema": "kosif.timeline.v1", "name": "project", "fps": fps, "width": edl["width"],
            "height": edl["height"], "duration": round(total, 3), "tracks": tracks}


def export_project(job: Path, edl: dict, analysis: dict, fps: float, words: list[dict]) -> dict:
    """render/nle/project.{fcpxml,premiere.xml,otio,edl,srt,capcut.md} via nle_export.py; project.fcpxml
    is copied to render/. Prefers station 5's converter dm_edl.to_nle, else converts locally."""
    script = dm.SP / "nle_export.py"
    rdir = job / "render"
    if not script.exists():
        return {"error": "nle_export.py missing"}
    edl_a, an_a = _absolute(job, edl, analysis)
    argv, conv = None, "local"
    try:
        import dm_edl  # station 5's shared converters
        argv = [str(x) for x in dm_edl.to_nle(edl_a, an_a, rdir, name="project")["argv"]]
        conv = "dm_edl.to_nle"
    except Exception as exc:  # noqa: BLE001 — fall back to the local converter
        conv = f"local ({type(exc).__name__}: {str(exc)[:120]})"
    if argv is None:
        tfile = rdir / "nle_timeline.json"
        tfile.write_text(json.dumps(edl_to_timeline(edl_a, an_a, job, fps), ensure_ascii=False, indent=2),
                         encoding="utf-8")
        argv = [*dm.py(script), "export", "--project", str(tfile), "--out", str(rdir / "nle"),
                "--formats", "fcpxml,xmeml,edl,otio,capcut", "--name", "project", "--force"]
        if words:
            wf = rdir / "nle_words.json"
            wf.write_text(json.dumps({"words": [{k: w[k] for k in ("word", "start", "end")} for w in words]},
                                     ensure_ascii=False), encoding="utf-8")
            argv[argv.index("--formats") + 1] += ",srt"
            argv += ["--words", str(wf)]
    res = dm.run(job, STATION, "nle_export", argv, check=False, owner_media=False)
    nle = rdir / "nle"
    fx = nle / "project.fcpxml"
    if res.returncode != 0 or not fx.exists():
        return {"error": (res.stdout or res.stderr)[-400:], "converter": conv}
    shutil.copyfile(fx, rdir / "project.fcpxml")
    files = sorted(str(p.relative_to(job)) for p in nle.iterdir() if p.is_file())
    return {"fcpxml": "render/project.fcpxml", "files": files, "converter": conv,
            "warnings": [f"speed {p['speed']}x on {p['ev']['id']} not carried by the NLE export"
                         for p in plan_timeline(edl, fps) if abs(p["speed"] - 1) > 1e-6]}


# ----------------------------------------------------------------------------- main
def render(job: Path, extra_ratios: list[str], preview: bool = False, fast: bool = False,
           do_verify: bool = True, do_export: bool = True) -> dict:
    job = Path(job).resolve()
    edl = dm.read(job, "edl")
    try:
        analysis = dm.read(job, "analysis")
    except FileNotFoundError:
        analysis = {"clips": []}
    try:
        look = dm.read(job, "look")
    except (FileNotFoundError, dm.ContractError):
        look = None
    rdir = job / "render"
    rdir.mkdir(parents=True, exist_ok=True)
    W, H = int(edl["width"]), int(edl["height"])
    if preview:
        W, H = max(2, W // 3 // 2 * 2), max(2, H // 3 // 2 * 2)
    main = rdir / ("preview.mp4" if preview else "final.mp4")
    edl_in = edl
    edl, clamp_warn = clamp_to_media(job, edl, {c["id"]: c for c in (analysis or {}).get("clips", [])})
    r = render_one(job, edl, analysis, look, W, H, main, preview, fast)
    fps, warnings = r["fps"], clamp_warn + list(r["warnings"])
    wfile = rdir / "words.json"
    wfile.write_text(json.dumps({"words": r["words"]}, ensure_ascii=False, indent=1), encoding="utf-8")
    srt = rdir / "captions.srt"
    n_srt = write_srt(srt, r["words"]) if r["words"] else 0
    if not r["words"]:
        srt.write_text("", encoding="utf-8")
        warnings.append("no words in analysis: captions.srt is empty and nothing was burned")
    if abs(r["duration"] - float(edl_in["duration"])) > 0.3:
        warnings.append(f"timeline is {r['duration']}s but edl.duration says {edl_in['duration']}s "
                        + ("(src ranges clamped to the media)" if clamp_warn else
                           "(edl.json was not reflowed: run dm_edl.reflow)"))
    target = float((edl.get("audio") or {}).get("target_lufs", -14))
    extra = []
    for ratio in [x.strip() for x in extra_ratios if x.strip()]:
        ew, eh = ratio_size(ratio, int(edl["width"]), int(edl["height"]))
        if preview:
            ew, eh = max(2, ew // 3 // 2 * 2), max(2, eh // 3 // 2 * 2)
        tag = "_" + ratio.replace(":", "x")
        o = rdir / f"{'preview' if preview else 'final'}{tag}.mp4"
        render_one(job, edl, analysis, look, ew, eh, o, preview, fast, tag)
        extra.append({"ratio": ratio, "path": str(o.relative_to(job)), "width": ew, "height": eh})
    v = verify(job, main, W, H, fps, r["duration"], target) if do_verify else {"tool": "verify_video", "pass": None,
                                                                                "skipped": True}
    for e in extra:
        e["verify"] = verify(job, job / e["path"], e["width"], e["height"], fps, r["duration"], target) if do_verify else None
    proj = export_project(job, edl, analysis, fps, r["words"]) if do_export else {"skipped": True}
    if proj.get("error"):
        warnings.append(f"nle export failed: {proj['error']}")
    warnings += proj.get("warnings", [])
    doc = dm.new("render", final=str(main.relative_to(job)), extra=[e["path"] for e in extra],
                 extra_detail=extra, preview=preview,
                 captions=str(srt.relative_to(job)), captions_ass=str(r["ass"].relative_to(job)) if r["ass"] else None,
                 caption_cues=n_srt, caption_font=r["font"], font_dir=r["font_dir"], caption_safe_area=r["safe"],
                 project=proj.get("fcpxml"), project_files=proj.get("files", []), project_converter=proj.get("converter"),
                 width=W, height=H, fps=fps, duration=r["duration"], edl_duration=edl_in["duration"],
                 grade={"id": r["grade"], "filter": r["grade_filter"],
                        "per_event": {p["ev"]["id"]: event_grade(p["ev"]) for p in r["plan"] if event_grade(p["ev"])}},
                 music=r["music"], muted=[p["ev"]["id"] for p in r["plan"] if p["ev"].get("mute")],
                 loudness={"target_lufs": target, "true_peak_ceiling": (r["loudnorm_measured"].get("limiter") or {}).get("ceiling_dbtp", TP_CEILING),
                           "internal_tp": (r["loudnorm_measured"].get("limiter") or {}).get("loudnorm_tp", TP_INTERNAL),
                           "limiter_tp": (edl.get("audio") or {}).get("limiter_tp"),
                           "measured_before": r["loudnorm_measured"]},
                 events=[{"id": p["ev"]["id"], "start": round(p["start"], 3), "dur": round(p["dur"], 3),
                          "transition": p["trans"], "td": round(p["td"], 3),
                          "camera": camera_filters(p["ev"].get("camera"), W, H, fps, p["dur"])[0]} for p in r["plan"]],
                 # exact output span of every event in final.mp4 (seconds; frame-snapped, xfade overlaps
                 # included): review maps a time on the video to an event with these, nothing else.
                 events_out=[{"id": p["ev"]["id"], "out_in": round(p["start_f"] / fps, 3),
                              "out_out": round(p["end_f"] / fps, 3)} for p in r["plan"]],
                 verify=v, warnings=warnings, graph="render/graph.txt")
    dm.write(job, "render", doc)
    return doc


def main(argv=None) -> int:
    dm.utf8_stdio()
    ap = argparse.ArgumentParser(prog="dm_render.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render", help="render edl.json → render/final.mp4 + render.json")
    r.add_argument("--job", required=True)
    r.add_argument("--extra-ratios", default="", help="comma list, e.g. 1:1,16:9")
    r.add_argument("--preview", action="store_true", help="fast low-res render (render/preview.mp4)")
    r.add_argument("--fast", action="store_true", help="faster x264 preset at full size")
    r.add_argument("--no-verify", action="store_true")
    r.add_argument("--no-export", action="store_true")
    a = ap.parse_args(argv)
    try:
        doc = render(Path(a.job), a.extra_ratios.split(","), a.preview, a.fast, not a.no_verify, not a.no_export)
    except (FileNotFoundError, dm.ContractError, RuntimeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)[-1200:]}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "rendered", "final": doc["final"], "duration": doc["duration"],
                      "verify_pass": doc["verify"].get("pass"), "lufs": doc["verify"].get("lufs"),
                      "extra": doc["extra"], "project": doc["project"], "warnings": doc["warnings"]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
