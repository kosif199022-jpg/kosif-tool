"""KOSIF timeline — a declarative edit compiled to FFmpeg: clips with in/out points, constant speed or speed ramps,
Ken-Burns zooms, grades, any of FFmpeg's xfade transitions (with matching audio cross-fades), Arabic text overlays
and lower thirds drawn by Pillow (shaped, ordered, in a real Arabic font), images/logos, a progress bar, karaoke
captions, music with sidechain ducking under the voice (or under the footage's own speech), −14 LUFS.

    python timeline.py SPEC.json --out film.mp4 [--workers 4] [--dry-run] [--inspect]
    python timeline.py --example edit.json            a commented sample spec to start from
    python timeline.py --transitions                   the transitions this FFmpeg build offers

Spec (every key optional unless noted; times in seconds, relative to the clip for in/out):
{
  "size": "1080x1920" | "ratio": "9:16",  "fps": 30,  "background": "#0d1b2a",
  "clips": [                                               # required: in order
    {"src": "a.mp4", "in": 2.0, "out": 6.5, "speed": 1.0, "fit": "cover|contain|blur", "grade": "teal_orange",
     "zoom": {"from": 1.0, "to": 1.08}, "volume": 1.0, "mute": false,
     "transition": {"type": "circleopen", "dur": 0.6}},     # the transition INTO the next clip ("cut" = none)
    {"src": "b.mp4", "in": 0, "out": 4, "ramp": [[0, 1.0], [1.5, 0.25], [3.0, 1.0]], "interpolate": false},
    {"image": "photo.jpg", "dur": 3, "zoom": {"from": 1.0, "to": 1.15}},
    {"color": "#111111", "dur": 0.8}
  ],
  "overlays": [
    {"type": "text", "text": "عنوان الفيلم", "start": 0.5, "end": 3.5, "pos": "center", "size": 96, "color": "#ffffff",
     "box": "#00000099", "anim": "rise"},
    {"type": "lower-third", "title": "محمود", "sub": "مخرج", "start": 4, "end": 8, "accent": "#E7B65A"},
    {"type": "image", "src": "logo.png", "start": 0, "end": 12, "pos": "upper-right", "scale": 0.22, "anim": "fade"},
    {"type": "progress", "color": "#E7B65A", "height": 10, "from": "right"},
    {"type": "captions", "spec": "caps.json", "style": "tiktok"}
  ],
  "audio": {"music": {"src": "track.mp3", "gain": -6, "start": 0, "fade_in": 1.0, "fade_out": 2.0, "loop": true},
            "voice": {"src": "vo.wav", "start": 0.5}, "keep_clip_audio": true, "duck": "auto", "lufs": -14,
            "sfx": [{"src": "kit:reveal-1", "at": 0.4, "gain": -10}, {"src": "whoosh.wav", "at": 3.9}]}
}
Sound effects (audio.sfx): "kit:NAME" from scripts/kit/sfx (CC0; `kmotion sfx` lists them with their use) or a file;
"at" is when the sound starts — align it to the START of the motion it marks (an entry 0–0.1 s before the first visible
frame, a transition at its start); default gain −10 dB so effects sit under the music. Fewer cues, better timed.
Speed ramps: [[t_in_clip, speed], ...] — the speed changes linearly between keys (the time map is the exact integral, so
a 0.25× stretch really lasts 4× longer); audio is dropped under a ramp (constant speeds keep it, pitch-preserved).
Everything is deterministic: the same spec and sources give the same film.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SFX_DIR = HERE / "kit" / "sfx"                                     # CC0 effects (kmotion sfx lists them)
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

import tools  # noqa: E402
import montage  # noqa: E402

FF = tools.FF
RATIOS = tools.RATIOS

# the xfade transitions of FFmpeg ≥ 4.3; `transitions()` keeps only those this build reports
XFADE = ["fade", "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft", "slideright", "slideup", "slidedown", "circlecrop",
         "rectcrop", "distance", "fadeblack", "fadewhite", "radial", "smoothleft", "smoothright", "smoothup", "smoothdown",
         "circleopen", "circleclose", "vertopen", "vertclose", "horzopen", "horzclose", "dissolve", "pixelize", "diagtl", "diagtr",
         "diagbl", "diagbr", "hlslice", "hrslice", "vuslice", "vdslice", "hblur", "fadegrays", "wipetl", "wipetr", "wipebl", "wipebr",
         "squeezeh", "squeezev", "zoomin", "fadefast", "fadeslow", "hlwind", "hrwind", "vuwind", "vdwind", "coverleft", "coverright",
         "coverup", "coverdown", "revealleft", "revealright", "revealup", "revealdown"]
# what each family does, for the menu and the docs (Arabic)
XFADE_AR = {"fade": "تلاشٍ متقاطع", "fadeblack": "عبر الأسود", "fadewhite": "عبر الأبيض", "dissolve": "ذوبان حبيبي", "wipe": "مسح",
            "slide": "انزلاق", "smooth": "مسح ناعم", "circle": "دائرة", "rect": "مستطيل", "radial": "شعاعي", "vert": "فتح/إغلاق رأسي",
            "horz": "فتح/إغلاق أفقي", "pixelize": "تبكسل", "diag": "قطري", "slice": "شرائح", "hblur": "ضبابية أفقية", "fadegrays": "عبر الرمادي",
            "squeeze": "ضغط", "zoomin": "زووم للداخل", "wind": "ريح", "cover": "تغطية", "reveal": "كشف", "distance": "مسافة"}
_TRANS_CACHE: list[str] | None = None


def transitions() -> list[str]:
    """The xfade transitions this FFmpeg build offers (parsed from its help; the known list when parsing fails)."""
    global _TRANS_CACHE
    if _TRANS_CACHE is None:
        r = subprocess.run([FF, "-hide_banner", "-h", "filter=xfade"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        names = re.findall(r"^\s+([a-z]+)\s+\d+\s+\.\.FV", r.stdout or "", flags=re.M)
        _TRANS_CACHE = [n for n in names if n != "custom"] or list(XFADE)
    return _TRANS_CACHE


def transition_ar(name: str) -> str:
    for k in sorted(XFADE_AR, key=len, reverse=True):          # the most specific family first (fadeblack before fade)
        if name.startswith(k) or k in name:
            return XFADE_AR[k]
    return name


# ───────────────────────── speed ramps ─────────────────────────
def ramp_pieces(keys: list[list[float]], dur: float) -> tuple[list[tuple[float, float, float, float, float]], float]:
    """[(t0, t1, s0, s1, out0)] over the whole clip (keys padded to 0 and dur) and the output duration.
    Between keys the speed is linear in source time; the output time is its exact integral."""
    ks = sorted((float(t), float(s)) for t, s in keys)
    if not ks:
        raise ValueError("ramp needs at least one [time, speed] pair")
    for _, s in ks:
        if not (0.1 <= s <= 10):
            raise ValueError(f"ramp speed {s} out of range 0.1–10")
    if ks[0][0] > 0:
        ks.insert(0, (0.0, ks[0][1]))
    if ks[-1][0] < dur:
        ks.append((dur, ks[-1][1]))
    ks = [(min(max(t, 0.0), dur), s) for t, s in ks]
    pieces, out = [], 0.0
    for (t0, s0), (t1, s1) in zip(ks, ks[1:]):
        if t1 - t0 <= 1e-6:
            continue
        pieces.append((t0, t1, s0, s1, out))
        out += _piece_len(t0, t1, s0, s1)
    return pieces, out


def _piece_len(t0: float, t1: float, s0: float, s1: float) -> float:
    L = t1 - t0
    if abs(s1 - s0) < 1e-6:
        return L / s0
    b = (s1 - s0) / L
    return (math.log(s1) - math.log(s0)) / b


def ramp_map(pieces, T: float) -> float:
    """Source time → output time (the Python twin of the FFmpeg expression; used by the tests)."""
    for t0, t1, s0, s1, out0 in pieces:
        if T <= t1 or (t0, t1, s0, s1, out0) == pieces[-1]:
            if abs(s1 - s0) < 1e-6:
                return out0 + (T - t0) / s0
            b = (s1 - s0) / (t1 - t0)
            return out0 + (math.log(max(1e-9, s0 + b * (T - t0))) - math.log(s0)) / b
    return 0.0


def ramp_expr(pieces) -> str:
    """The setpts expression: nested if() over the pieces, in FFmpeg's expression language (T = source seconds)."""
    def piece(t0, t1, s0, s1, out0):
        if abs(s1 - s0) < 1e-6:
            return f"{out0:.6f}+(T-{t0:.6f})/{s0:.6f}"
        b = (s1 - s0) / (t1 - t0)
        return f"{out0:.6f}+(log({s0:.6f}+{b:.6f}*(T-{t0:.6f}))-log({s0:.6f}))/{b:.6f}"
    expr = piece(*pieces[-1])
    for p in reversed(pieces[:-1]):
        expr = f"if(lt(T,{p[1]:.6f}),{piece(*p)},{expr})"
    return f"setpts='({expr})/TB'"


def atempo_chain(speed: float) -> str:
    """atempo accepts 0.5–100 per stage: slower speeds are chained."""
    parts, s = [], speed
    while s < 0.5:
        parts.append("atempo=0.5"); s /= 0.5
    parts.append(f"atempo={s:.4f}")
    return ",".join(parts)


# ───────────────────────── spec ─────────────────────────
def _hex(c: str, default: str) -> str:
    c = (c or default).strip()
    if not re.fullmatch(r"#?[0-9a-fA-F]{6}([0-9a-fA-F]{2})?", c):
        raise ValueError(f"colour {c!r}: use #rrggbb or #rrggbbaa")
    return c if c.startswith("#") else "#" + c


def _ff_color(c: str) -> str:
    """#rrggbb[aa] → FFmpeg colour (0xRRGGBB@alpha)."""
    c = _hex(c, "#000000").lstrip("#")
    a = int(c[6:8], 16) / 255 if len(c) == 8 else 1.0
    return f"0x{c[:6]}@{a:.3f}"


def load(spec: dict | str | Path, base: Path | None = None) -> dict:
    """Validate and normalise a spec (paths resolved against the spec's folder)."""
    if not isinstance(spec, dict):
        p = Path(spec)
        base = base or p.parent
        spec = json.loads(p.read_text(encoding="utf-8"))
    base = Path(base or ".")
    out = dict(spec)
    if "size" in spec:
        w, h = (int(v) for v in str(spec["size"]).lower().split("x"))
    else:
        w, h = RATIOS.get(spec.get("ratio", "9:16"), RATIOS["9:16"])
    if not (16 <= w <= 7680 and 16 <= h <= 7680):
        raise ValueError(f"size {w}x{h} out of range")
    out["W"], out["H"] = w - w % 2, h - h % 2
    out["fps"] = int(spec.get("fps", 30))
    if not (1 <= out["fps"] <= 120):
        raise ValueError("fps out of range 1–120")
    out["background"] = _hex(spec.get("background", "#000000"), "#000000")
    clips = spec.get("clips") or []
    if not clips:
        raise ValueError("the spec needs at least one clip")
    tr_ok = set(transitions())
    norm = []
    for i, c in enumerate(clips):
        c = dict(c)
        kind = "src" if c.get("src") else "image" if c.get("image") else "color" if c.get("color") else None
        if not kind:
            raise ValueError(f"clip {i}: needs src, image or color")
        if kind != "color":
            p = Path(c[kind])
            c[kind] = str(p if p.is_absolute() else base / p)
            if not Path(c[kind]).exists():
                raise ValueError(f"clip {i}: {c[kind]} not found")
        c["kind"] = kind
        if kind != "src" and not c.get("dur"):
            c["dur"] = 3.0
        sp = float(c.get("speed", 1.0))
        if not (0.1 <= sp <= 10):
            raise ValueError(f"clip {i}: speed {sp} out of range 0.1–10")
        c["speed"] = sp
        if c.get("grade", "none") not in montage.GRADES:
            raise ValueError(f"clip {i}: unknown grade {c['grade']}; one of {', '.join(montage.GRADES)}")
        if c.get("fit", "cover") not in ("cover", "contain", "blur"):
            raise ValueError(f"clip {i}: fit must be cover, contain or blur")
        if c.get("match"):                                     # per-channel colour transfer: {"r": [gain, offset], …}
            m = c["match"]
            if not isinstance(m, dict) or not all(isinstance(m.get(ch), (list, tuple)) and len(m[ch]) == 2 for ch in "rgb"):
                raise ValueError(f"clip {i}: match needs r, g and b as [gain, offset]")
            c["match"] = {ch: [float(m[ch][0]), float(m[ch][1])] for ch in "rgb"}
            if not all(0.3 <= g <= 3.0 and -160 <= o <= 160 for g, o in c["match"].values()):
                raise ValueError(f"clip {i}: match gain must be 0.3–3.0 and offset −160–160")
        t = c.get("transition")
        if isinstance(t, str):
            t = None if t in ("cut", "none", "") else {"type": t}
        if t:
            t = {"type": str(t.get("type", "fade")), "dur": float(t.get("dur", 0.6))}
            if t["type"] not in tr_ok:
                raise ValueError(f"clip {i}: unknown transition {t['type']!r}; `kmotion transitions` lists them")
            if not (0.05 <= t["dur"] <= 5):
                raise ValueError(f"clip {i}: transition dur {t['dur']} out of range 0.05–5")
        c["transition"] = t
        if c.get("zoom"):
            z = c["zoom"]; c["zoom"] = {"from": float(z.get("from", 1.0)), "to": float(z.get("to", 1.08))}
            if not all(1.0 <= v <= 3.0 for v in c["zoom"].values()):
                raise ValueError(f"clip {i}: zoom factors must be 1.0–3.0")
        norm.append(c)
    out["clips"] = norm
    ovs = []
    for i, o in enumerate(spec.get("overlays") or []):
        o = dict(o)
        kind = o.get("type", "text")
        if kind not in ("text", "lower-third", "image", "progress", "captions"):
            raise ValueError(f"overlay {i}: unknown type {kind}")
        o["type"] = kind
        for key in ("src", "spec"):
            if o.get(key):
                p = Path(o[key]); o[key] = str(p if p.is_absolute() else base / p)
                if not Path(o[key]).exists():
                    raise ValueError(f"overlay {i}: {o[key]} not found")
        if kind in ("text", "lower-third", "image"):
            o["start"] = float(o.get("start", 0.0)); o["end"] = float(o.get("end", o["start"] + 3.0))
            if o["end"] <= o["start"]:
                raise ValueError(f"overlay {i}: end must be after start")
        if kind == "captions" and o.get("style", "reels") not in montage.STYLES:
            raise ValueError(f"overlay {i}: unknown caption style {o['style']}")
        ovs.append(o)
    out["overlays"] = ovs
    au = dict(spec.get("audio") or {})
    for key in ("music", "voice"):
        if au.get(key):
            m = dict(au[key]) if isinstance(au[key], dict) else {"src": au[key]}
            p = Path(m["src"]); m["src"] = str(p if p.is_absolute() else base / p)
            if not Path(m["src"]).exists():
                raise ValueError(f"audio.{key}: {m['src']} not found")
            au[key] = m
    sfx = []
    for i, e in enumerate(au.get("sfx") or []):                     # effects: {"src": "kit:reveal-1" | path, "at": s, "gain": dB}
        e = dict(e); name = str(e.get("src", ""))
        if name.startswith("kit:"):
            cat = json.loads((SFX_DIR / "catalog.json").read_text(encoding="utf-8"))["sounds"]
            if name[4:] not in cat:
                raise ValueError(f"audio.sfx {i}: unknown kit sound {name[4:]!r} (kmotion sfx lists them)")
            e["src"] = str(SFX_DIR / cat[name[4:]]["file"])
        else:
            p = Path(name); e["src"] = str(p if p.is_absolute() else base / p)
        if not Path(e["src"]).exists():
            raise ValueError(f"audio.sfx {i}: {e['src']} not found")
        e["at"] = float(e.get("at", 0.0)); e["gain"] = float(e.get("gain", -10.0))   # effects sit under the music by default
        if e["at"] < 0:
            raise ValueError(f"audio.sfx {i}: at must be ≥ 0")
        sfx.append(e)
    au["sfx"] = sfx
    au.setdefault("keep_clip_audio", True)
    au.setdefault("duck", "auto")
    au["lufs"] = float(au.get("lufs", -14.0))
    out["audio"] = au
    return out


# ───────────────────────── intermediates (one per clip) ─────────────────────────
def _clip_source_dur(c: dict) -> float:
    if c["kind"] != "src":
        return float(c["dur"])
    info = tools.probe(Path(c["src"]))
    total = info["duration"]
    a = float(c.get("in", 0.0)); b = float(c.get("out", total) or total)
    b = min(b, total) if total > 0 else b
    if b - a <= 0.04:
        raise ValueError(f"clip {c['src']}: out ({b}) must be after in ({a})")
    c["in"], c["out"] = a, b
    c["has_audio"] = bool(info["audio"])
    return b - a


def _fit_chain(c: dict, W: int, H: int, bg: str) -> str:
    fit = c.get("fit", "cover")
    if fit == "contain":
        return f"scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color={_ff_color(bg)},setsar=1"
    if fit == "blur":
        return (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=40,eq=brightness=-0.12:saturation=0.85[bg];"
                f"[b]scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1")
    return f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"


def _zoom_chain(z: dict, W: int, H: int, dur: float) -> str:
    """A Ken-Burns push rendered at 2× so the scale steps are half-pixel; eased with a raised cosine over the clip."""
    f, t = z["from"], z["to"]
    zexpr = f"({f:.4f}+({t:.4f}-{f:.4f})*(1-cos(PI*min(1,t/{dur:.4f})))/2)"
    return (f"scale={2 * W}:{2 * H}:flags=lanczos,scale=w='trunc({2 * W}*{zexpr}/2)*2':h='trunc({2 * H}*{zexpr}/2)*2':eval=frame,"
            f"crop={2 * W}:{2 * H},scale={W}:{H}:flags=lanczos")


def _video_seconds(p: Path) -> float | None:
    """The picture's length from its frame count (the AAC track pads a few tens of ms; offsets must follow the picture)."""
    r = subprocess.run([tools.FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames,r_frame_rate", "-of", "json", str(p)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        s = json.loads(r.stdout)["streams"][0]
        num, den = s["r_frame_rate"].split("/")
        n = int(s.get("nb_frames", 0))
        return n / (float(num) / float(den or 1)) if n > 0 else None
    except (ValueError, KeyError, IndexError, ZeroDivisionError):
        return None


def _intermediate(c: dict, idx: int, W: int, H: int, fps: int, bg: str, tmp: Path) -> dict:
    """One clip → a W×H, fps, yuv420p H.264 segment with a 48 kHz stereo AAC track (silence when it has none)."""
    out = tmp / f"c{idx:03d}.mp4"
    src_dur = _clip_source_dur(c)
    pieces = None
    if c.get("ramp"):
        pieces, out_dur = ramp_pieces(c["ramp"], src_dur)
    else:
        out_dur = src_dur / c["speed"]
    if c["kind"] == "src":
        ins = ["-ss", f"{c['in']:.3f}", "-t", f"{src_dur:.3f}", "-i", c["src"]]
    elif c["kind"] == "image":
        ins = ["-loop", "1", "-framerate", str(fps), "-t", f"{src_dur:.3f}", "-i", c["image"]]
    else:
        ins = ["-f", "lavfi", "-i", f"color=c={_ff_color(c['color'])}:s={W}x{H}:r={fps}:d={src_dur:.3f}"]
    vf = [_fit_chain(c, W, H, bg)]
    if pieces:
        vf.append(ramp_expr(pieces))
        vf.append(f"minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:vsbmc=1" if c.get("interpolate") else f"fps={fps}")
    elif abs(c["speed"] - 1.0) > 1e-6:
        vf.append(f"setpts=PTS/{c['speed']:.6f}")
        vf.append(f"minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:vsbmc=1" if c.get("interpolate") and c["speed"] < 1 else f"fps={fps}")
    else:
        vf.append(f"fps={fps}")
    if c.get("zoom"):
        vf.append(_zoom_chain(c["zoom"], W, H, out_dur))
    if c.get("match"):                                         # colour transfer towards a reference look (kmotion mimic)
        vf.append("format=rgb24,lutrgb=" + ":".join(f"{ch}='clip(val*{g:.4f}+{o:.2f},0,255)'" for ch, (g, o) in c["match"].items()))
    g = montage.GRADES.get(c.get("grade", "none"), "null")
    if g != "null":
        vf.append(g)
    vf.append("format=yuv420p")
    audio_ok = c["kind"] == "src" and c.get("has_audio") and not c.get("mute") and not pieces
    if audio_ok:
        af = [atempo_chain(c["speed"]) if abs(c["speed"] - 1.0) > 1e-6 else "anull", f"volume={float(c.get('volume', 1.0)):.3f}",
              "aformat=sample_rates=48000:channel_layouts=stereo", "apad"]
        graph = f"[0:v]{','.join(vf)}[v];[0:a]{','.join(af)}[a]"
        cmd = [FF, "-y", "-v", "error", *ins, "-filter_complex", graph, "-map", "[v]", "-map", "[a]"]
    else:
        graph = f"[0:v]{','.join(vf)}[v]"
        cmd = [FF, "-y", "-v", "error", *ins, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-filter_complex", graph, "-map", "[v]", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-preset", "fast", "-crf", "16", "-g", str(fps), "-keyint_min", str(fps), "-pix_fmt", "yuv420p", "-r", str(fps),
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-t", f"{out_dur:.3f}", "-video_track_timescale", "90000", str(out)]
    tools._run(cmd)
    real = _video_seconds(out) or tools.probe(out)["duration"]
    return {"file": out, "dur": round(real, 3), "planned": round(out_dur, 3), "src": c.get("src") or c.get("image") or c.get("color"),
            "kind": c["kind"], "in": c.get("in"), "out": c.get("out"), "speed": None if pieces else c["speed"], "ramp": c.get("ramp"),
            "transition": c.get("transition"), "audio": bool(audio_ok)}


# ───────────────────────── overlays drawn by Pillow ─────────────────────────
def _shape(text: str) -> str:
    if not any("؀" <= ch <= "ۿ" for ch in text):
        return text
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text))
    except ImportError:
        return text


_CMAP: dict = {}


def _font(o: dict, size: int):
    from PIL import ImageFont
    f = o.get("font")
    p = Path(f) if f and Path(f).exists() else tools.font_path(arabic=True)
    return ImageFont.truetype(str(p), size) if p else ImageFont.load_default(size), (str(p) if p else None)


def _has_glyph(font_path: str | None, ch: str) -> bool:
    """Does this font file map the character? (fontTools cmap, cached; True when nothing can be checked)."""
    if not font_path:
        return True
    if font_path not in _CMAP:
        try:
            from fontTools.ttLib import TTFont
            _CMAP[font_path] = set(TTFont(font_path, lazy=True).getBestCmap() or {})
        except Exception:  # noqa: BLE001
            _CMAP[font_path] = None
    cm = _CMAP[font_path]
    return True if cm is None else (ord(ch) in cm or ch.isspace())


def _runs(text: str, font_path: str | None) -> list[tuple[str, bool]]:
    """Visual-order text split into runs the main font can draw and runs it cannot (arrows, symbols, emoji…)."""
    runs: list[tuple[str, bool]] = []
    for ch in text:
        ok = _has_glyph(font_path, ch)
        if runs and runs[-1][1] == ok:
            runs[-1] = (runs[-1][0] + ch, ok)
        else:
            runs.append((ch, ok))
    return runs


def draw_line(dr, x: float, y: float, text: str, font, font_path: str | None, fill, anchor: str = "ma", stroke_width: int = 0, stroke_fill=None, fallback=None):
    """Draw one visual-order line; characters the main font lacks come from the fallback font (Segoe UI / Arial),
    so an arrow or a symbol inside Arabic never renders as a box. Measured as one line, drawn run by run."""
    runs = _runs(text, font_path)
    if all(ok for _, ok in runs) or fallback is None:
        dr.text((x, y), text, font=font, fill=fill, anchor=anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)
        return
    widths = [dr.textlength(seg, font=font if ok else fallback) for seg, ok in runs]
    total = sum(widths)
    cx = x - total / 2 if anchor[0] == "m" else (x if anchor[0] == "l" else x - total)
    for (seg, ok), wdt in zip(runs, widths):
        dr.text((cx, y), seg, font=font if ok else fallback, fill=fill, anchor="l" + anchor[1], stroke_width=stroke_width, stroke_fill=stroke_fill)
        cx += wdt


def _fallback_font(size: int):
    from PIL import ImageFont
    p = tools.font_path(arabic=False)
    return ImageFont.truetype(str(p), size) if p else None


def _rgba(c: str, default: str = "#ffffff") -> tuple[int, int, int, int]:
    c = _hex(c, default).lstrip("#")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16), int(c[6:8], 16) if len(c) == 8 else 255)


def text_png(o: dict, W: int, H: int, out: Path) -> dict:
    """A text block (lines by \\n, wrapped to 84 % of the width) with stroke, soft shadow and an optional rounded box,
    shaped and ordered for Arabic. Returns the PNG size so the caller can place it."""
    from PIL import Image, ImageDraw, ImageFilter
    size = int(o.get("size") or round(min(W, H) * 0.075))
    font, font_used = _font(o, size)
    pad = round(size * 0.45)
    fill = _rgba(o.get("color", "#ffffff"))
    box = _rgba(o["box"], "#00000099") if o.get("box") else None
    stroke = max(0, int(o.get("stroke", round(size / 16))))
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    lines = []
    for raw in str(o.get("text", "")).split("\n"):
        lines += tools._wrap(_shape(raw), font, W * 0.84, probe) if raw.strip() else [""]
    lh = round(size * float(o.get("line_height", 1.3)))
    tw = max([probe.textlength(ln, font=font) for ln in lines] + [1])
    w, h = int(tw + 2 * pad + 2 * stroke), int(lh * len(lines) + 2 * pad)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    if box:
        dr.rounded_rectangle((0, 0, w - 1, h - 1), radius=round(size * 0.35), fill=box)
    align = o.get("align", "center")
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    fb = _fallback_font(size)
    for i, ln in enumerate(lines):
        y = pad + i * lh
        x = w / 2 if align == "center" else (pad + stroke if align == "left" else w - pad - stroke)
        anchor = "ma" if align == "center" else ("la" if align == "left" else "ra")
        draw_line(sd, x, y + size * 0.08, ln, font, font_used, (0, 0, 0, 150), anchor, fallback=fb)
        draw_line(dr, x, y, ln, font, font_used, fill, anchor, stroke, _rgba(o.get("stroke_color", "#000000")), fallback=fb)
    if o.get("shadow", True):
        shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.08))
        im = Image.alpha_composite(shadow, im)
    im.save(out)
    return {"file": str(out), "w": w, "h": h, "font": font_used, "lines": len(lines)}


HARAKAT = set("\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670")


def text_png_browser(o: dict, W: int, H: int, out: Path) -> dict | None:
    """The same text block drawn by a real browser (Edge/Chromium through Playwright: HarfBuzz shaping), so harakat sit
    on their letters in any font — Pillow here has no RAQM and drops or misplaces them. Outline = a stroked copy
    behind the fill. None when no browser is available (the caller falls back to Pillow)."""
    import html as _html
    try:
        import html_render as HR
        sp = HR._playwright()
        exe = HR.browser_path()
    except Exception:
        return None
    if not sp:
        return None
    size = int(o.get("size") or round(min(W, H) * 0.075))
    font, font_used = _font(o, size)
    stroke = max(0, int(o.get("stroke", round(size / 16))))
    pad = round(size * 0.45) + stroke
    lh = float(o.get("line_height", 1.3))
    color, sc = o.get("color", "#ffffff"), o.get("stroke_color", "#000000")
    box = f"background:{o['box']};border-radius:{round(size * 0.35)}px;" if o.get("box") else ""
    shadow = f"filter:drop-shadow(0 {size * 0.08:.1f}px {size * 0.08:.1f}px rgba(0,0,0,.6));" if o.get("shadow", True) else ""
    txt = _html.escape(str(o.get("text", "")))
    rtl = any("\u0600" <= ch <= "\u06ff" for ch in str(o.get("text", "")))
    face = f"@font-face{{font-family:K;src:url('{Path(font_used).resolve().as_uri()}');}}" if font_used else ""
    ws = "pre" if o.get("nowrap") else "pre-wrap"
    common = (f"font-family:K,'Segoe UI',sans-serif;font-size:{size}px;line-height:{lh};white-space:{ws};"
              f"text-align:{o.get('align', 'center')};direction:{'rtl' if rtl else 'ltr'};")
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>{face}html,body{{margin:0;background:transparent}}"
            f"#t{{display:inline-block;position:relative;padding:{pad}px;max-width:{'none' if o.get('nowrap') else str(int(W * 0.84)) + 'px'};{box}{shadow}}}"
            f"#t span{{{common}display:block}}#b{{position:absolute;inset:{pad}px;color:{sc};"
            f"-webkit-text-stroke:{2 * stroke}px {sc}}}#f{{position:relative;color:{color}}}</style></head>"
            f"<body><div id='t'><span id='b'>{txt}</span><span id='f'>{txt}</span></div></body></html>")
    hp = out.with_suffix(".html"); hp.write_text(page, encoding="utf-8")
    with sp() as pw:
        br = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H})
        pg.goto(hp.resolve().as_uri()); pg.evaluate("document.fonts.ready")
        pg.locator("#t").screenshot(path=str(out), omit_background=True)
        br.close()
    from PIL import Image
    w, h = Image.open(out).size
    return {"file": str(out), "w": w, "h": h, "font": font_used, "engine": "browser"}


def fit_size(texts: list[str], font: str | None, size: int, width: float) -> int | None:
    """One common font size at which every line of every text fits `width` px on one line (browser-measured, one launch).
    None when no browser is available."""
    import html as _html
    try:
        import html_render as HR
        sp = HR._playwright(); exe = HR.browser_path()
    except Exception:
        return None
    if not sp:
        return None
    face = f"@font-face{{font-family:K;src:url('{Path(font).resolve().as_uri()}');}}" if font else ""
    spans = "".join(f"<span style='font-family:K;font-size:{size}px;white-space:pre;display:inline-block'>{_html.escape(ln)}</span><br>"
                    for t in texts for ln in str(t).split("\n"))
    with sp() as pw:
        br = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        pg = br.new_page(viewport={"width": 4000, "height": 2000})
        # a file page, not set_content: about:blank may not load a file:// font, and the size would fit the fallback font
        import tempfile
        hp = Path(tempfile.mkdtemp(prefix="kosif_fit_")) / "fit.html"
        hp.write_text(f"<!doctype html><meta charset='utf-8'><style>{face}</style><body dir='rtl'>{spans}</body>", encoding="utf-8")
        pg.goto(hp.as_uri()); pg.evaluate("document.fonts.ready")
        if font and not pg.evaluate("document.fonts.check('16px K')"):
            br.close(); raise RuntimeError(f"browser could not load the font {font}")
        widest = max(pg.evaluate("[...document.querySelectorAll('span')].map(s => s.getBoundingClientRect().width)") or [1])
        br.close()
    return max(8, int(size * min(1.0, width / max(widest, 1))))


def lower_third_png(o: dict, W: int, H: int, out: Path) -> dict:
    """Name + role on an accent bar, in the lower safe area; RTL when the text is Arabic."""
    from PIL import Image, ImageDraw
    size = int(o.get("size") or round(min(W, H) * 0.052))
    font, font_used = _font(o, size)
    small, _ = _font(o, round(size * 0.58))
    fb, fb_small = _fallback_font(size), _fallback_font(round(size * 0.58))
    title, sub = _shape(str(o.get("title", ""))), _shape(str(o.get("sub", "")))
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = max(probe.textlength(title, font=font), probe.textlength(sub, font=small), 1)
    pad, bar = round(size * 0.5), max(4, round(size * 0.12))
    w, h = int(tw + 2 * pad + bar * 2), int(size * 1.25 + size * 0.58 * 1.3 + 2 * pad)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    rtl = any("؀" <= ch <= "ۿ" for ch in str(o.get("title", "")) + str(o.get("sub", "")))
    dr.rounded_rectangle((0, 0, w - 1, h - 1), radius=round(size * 0.3), fill=_rgba(o.get("box", "#0b1220cc"), "#0b1220cc"))
    accent = _rgba(o.get("accent", "#E7B65A"))
    if rtl:
        dr.rectangle((w - bar, 0, w, h), fill=accent); x, anchor = w - bar - pad, "ra"
    else:
        dr.rectangle((0, 0, bar, h), fill=accent); x, anchor = bar + pad, "la"
    draw_line(dr, x, pad, title, font, font_used, _rgba(o.get("color", "#ffffff")), anchor, fallback=fb)
    draw_line(dr, x, pad + size * 1.25, sub, small, font_used, _rgba(o.get("sub_color", "#ffffffbb"), "#ffffffbb"), anchor, fallback=fb_small)
    im.save(out)
    return {"file": str(out), "w": w, "h": h, "rtl": rtl}


def _place(o: dict, W: int, H: int, w: int, h: int, captions: bool = False) -> tuple[str, str]:
    """x, y of an overlay as FFmpeg expressions: a named position, fractions of the frame, pixels, or raw expressions.
    With karaoke captions in the film, the lower band belongs to them: bottom-anchored overlays move up above it."""
    pos = o.get("pos")
    m = round(min(W, H) * 0.06)
    safe_top = round(H * (0.14 if H > W else 0.08))
    safe_bottom = round(H * ((0.66 if captions else 0.80) if H > W else (0.74 if captions else 0.90)))
    named = {"center": ((W - w) // 2, (H - h) // 2), "top": ((W - w) // 2, safe_top), "bottom": ((W - w) // 2, safe_bottom - h),
             "lower-left": (m, safe_bottom - h), "lower-right": (W - w - m, safe_bottom - h), "upper-left": (m, safe_top),
             "upper-right": (W - w - m, safe_top), "lower-third": (W - w - m, safe_bottom - h)}
    if pos in named:
        x, y = named[pos]
    else:
        x, y = (W - w) // 2, (H - h) // 2
    def val(v, full, own, cur):
        if v is None:
            return str(cur)
        if isinstance(v, str):
            return v
        v = float(v)
        return str(int(v * (full - own))) if 0 <= v <= 1 else str(int(v))
    return val(o.get("x"), W, w, x), val(o.get("y"), H, h, y)


def _anim(o: dict, x: str, y: str, s: float, e: float) -> tuple[str, str, float]:
    """Entrance/exit as overlay position expressions plus the alpha fade length."""
    anim = o.get("anim", "fade"); f = float(o.get("fade", 0.35)); d = max(0.05, min(f, (e - s) / 2))
    ease_in = f"(1-pow(1-min(1,(t-{s:.3f})/{d + 0.1:.3f}),3))"       # cubic out over the entrance
    if anim == "rise":
        y = f"({y})+40*(1-{ease_in})"
    elif anim == "drop":
        y = f"({y})-40*(1-{ease_in})"
    elif anim == "slide-left":
        x = f"({x})+W*(1-{ease_in})"
    elif anim == "slide-right":
        x = f"({x})-W*(1-{ease_in})"
    elif anim == "none":
        d = 0.0
    return x, y, d


# ───────────────────────── the film ─────────────────────────
def _normalize_audio(raw: Path, out: Path, target: float) -> float | None:
    """Two-pass loudness: measure the mix, then normalise linearly to `target` LUFS (loudnorm's linear mode; it falls
    back to dynamic only when the true-peak ceiling forbids the gain). One-pass loudnorm undershoots or overshoots on
    short films (a 7.9 s timeline landed at -15.9 LUFS). A limiter catches encoder overshoot. Returns the measured
    loudness of the raw mix (None for silence)."""
    norm = f"loudnorm=I={target:.1f}:TP=-1.5:LRA=11"
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(raw), "-af", norm + ":print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr or "")
    measured = None
    if m:
        v = json.loads(m.group(0))
        try:
            measured = float(v["input_i"])
        except (TypeError, ValueError):
            measured = None
        if measured is not None and measured > -70:
            norm += (f":measured_I={v['input_i']}:measured_TP={v['input_tp']}:measured_LRA={v['input_lra']}"
                     f":measured_thresh={v['input_thresh']}:offset={v['target_offset']}:linear=true")
    tools._run([FF, "-y", "-v", "error", "-i", str(raw), "-af", norm + ",aresample=48000,alimiter=limit=0.84:level=false:attack=3:release=60",
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(out)])
    return measured


def build(spec: dict | str | Path, out: Path, workers: int = 0, dry_run: bool = False, inspect: bool = False, keep_tmp: bool = False) -> dict:
    sp = load(spec) if not (isinstance(spec, dict) and "W" in spec) else spec
    W, H, fps, bg = sp["W"], sp["H"], sp["fps"], sp["background"]
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="kosif_timeline_"))
    clips = sp["clips"]
    n_workers = max(1, min(workers or (os_cpu() // 2 or 1), len(clips), 6))
    with ThreadPoolExecutor(n_workers) as ex:
        segs = list(ex.map(lambda ic: _intermediate(ic[1], ic[0], W, H, fps, bg, tmp), enumerate(clips)))
    # the chain: transitions (xfade + acrossfade) and cuts (concat). Picture and sound are two graphs rendered as two
    # passes and joined losslessly: one graph carrying both stalls on some FFmpeg builds (7.1: the AAC encoder gets
    # no samples unless logging slows the scheduler down), and two passes also run side by side.
    ins: list[str] = []
    for s in segs:
        ins += ["-i", str(s["file"])]
    gv: list[str] = []
    ga: list[str] = []
    v, a, total = "[0:v]", "[0:a]", segs[0]["dur"]
    used_tr = []
    for i in range(1, len(segs)):
        tr = segs[i - 1]["transition"]
        d_i = segs[i]["dur"]
        if tr:
            d = min(tr["dur"], total * 0.5, d_i * 0.5)
            off = total - d
            gv.append(f"{v}[{i}:v]xfade=transition={tr['type']}:duration={d:.3f}:offset={off:.3f}[v{i}]")
            ga.append(f"{a}[{i}:a]acrossfade=d={d:.3f}:c1=tri:c2=tri[a{i}]")
            total = total + d_i - d
            used_tr.append({"after_clip": i - 1, "type": tr["type"], "dur": round(d, 3), "at": round(off, 3)})
        else:
            # concat outputs AV_TIME_BASE (1/1000000); a following xfade needs both inputs on the segments' 1/90000
            gv.append(f"{v}[{i}:v]concat=n=2:v=1:a=0,settb=1/90000[v{i}]")
            ga.append(f"{a}[{i}:a]concat=n=2:v=0:a=1[a{i}]")
            total += d_i
        v, a = f"[v{i}]", f"[a{i}]"
    nin = len(segs)
    # overlays
    ov_report = []
    for k, o in enumerate(sp["overlays"]):
        if o["type"] in ("text", "lower-third", "image"):
            s, e = max(0.0, o["start"]), min(total, o["end"])
            if e - s < 0.1:
                ov_report.append({"skipped": k, "why": "outside the film"}); continue
            if o["type"] == "image":
                from PIL import Image
                im = Image.open(o["src"]).convert("RGBA")
                sc = float(o.get("scale", 1.0))
                tw = int(o.get("width") or round(im.width * sc * (W / 1080 if W <= H else H / 1080)))
                tw = max(2, min(tw, W)); th = max(2, round(im.height * tw / im.width))
                png = tmp / f"ov{k:03d}.png"; im.resize((tw, th)).save(png)
                info = {"w": tw, "h": th}
            elif o["type"] == "lower-third":
                png = tmp / f"ov{k:03d}.png"; info = lower_third_png(o, W, H, png)
                if "pos" not in o and "x" not in o:
                    o["pos"] = "lower-right" if info["rtl"] else "lower-left"
                if "anim" not in o:
                    o["anim"] = "slide-left" if info["rtl"] else "slide-right"
            else:
                png = tmp / f"ov{k:03d}.png"
                eng = o.get("engine", "auto")                        # browser = HarfBuzz; auto = browser when harakat
                info = text_png_browser(o, W, H, png) if eng == "browser" or (eng == "auto" and HARAKAT & set(str(o.get("text", "")))) else None
                info = info or text_png(o, W, H, png)
            x, y = _place(o, W, H, info["w"], info["h"], captions=any(ov["type"] == "captions" for ov in sp["overlays"]))
            x, y, fd = _anim(o, x, y, s, e)
            ins += ["-loop", "1", "-framerate", str(fps), "-t", f"{e - s:.3f}", "-i", str(png)]
            chain = "format=rgba"
            fin = min(float(o.get("fade_in", fd)), (e - s) / 2); fout = min(float(o.get("fade_out", fd)), (e - s) / 2)   # separate in/out (mimic dips)
            if fin > 0:
                chain += f",fade=t=in:st=0:d={fin:.3f}:alpha=1"
            if fout > 0:
                chain += f",fade=t=out:st={max(0.0, e - s - fout):.3f}:d={fout:.3f}:alpha=1"
            chain += f",setpts=PTS+{s:.3f}/TB"
            gv.append(f"[{nin}:v]{chain}[ov{k}]")
            gv.append(f"{v}[ov{k}]overlay=x='{x}':y='{y}':eval=frame:eof_action=pass:enable='between(t,{s:.3f},{e:.3f})'[vo{k}]")
            v = f"[vo{k}]"; nin += 1
            ov_report.append({"overlay": k, "type": o["type"], "start": s, "end": e, "png": str(png), "x": x, "y": y})
        elif o["type"] == "progress":
            hgt = max(2, int(o.get("height", round(H * 0.006))))
            ins += ["-f", "lavfi", "-i", f"color=c={_ff_color(o.get('color', '#E7B65A'))}:s={W}x{hgt}:r={fps}:d={total:.3f}"]
            xexpr = f"W-W*t/{total:.3f}" if o.get("from", "right") == "right" else f"-W+W*t/{total:.3f}"
            yv = o.get("y", "bottom")
            yexpr = "0" if yv == "top" else (f"H-{hgt}" if yv == "bottom" else str(int(yv)))
            gv.append(f"{v}[{nin}:v]overlay=x='{xexpr}':y='{yexpr}':eval=frame:eof_action=pass[vo{k}]")
            v = f"[vo{k}]"; nin += 1
            ov_report.append({"overlay": k, "type": "progress"})
    caps = next((o for o in sp["overlays"] if o["type"] == "captions"), None)
    last_v = "[vout]"
    if caps:
        spec_c = json.loads(Path(caps["spec"]).read_text(encoding="utf-8"))
        ass_path = tmp / "caps.ass"
        ass_path.write_text(montage.ass(spec_c, W, H, caps.get("style", "reels"), int(caps.get("max_words", montage.STYLES[caps.get("style", "reels")].get("max_words", 6)))), encoding="utf-8")
        gv.append(f"{v}ass='{tools._ff_path(ass_path)}'[vout]")
    else:
        gv.append(f"{v}null[vout]")
    # audio
    au = sp["audio"]
    film_vol = 1.0 if au.get("keep_clip_audio", True) else 0.0
    music, voice = au.get("music"), au.get("voice")
    duck = au.get("duck", "auto")
    if duck == "auto":
        duck = "voice" if voice else ("clips" if (film_vol > 0 and music) else "none")
    if duck not in ("voice", "clips", "none"):
        raise ValueError("audio.duck must be auto, voice, clips or none")
    if duck == "voice" and not voice:
        duck = "none"
    if duck == "clips" and not music:
        duck = "none"
    film_chain = f"{a}volume={film_vol:.3f},aformat=sample_rates=48000:channel_layouts=stereo"
    key_src = None
    if duck == "clips":                                          # the footage's own speech ducks the music
        ga.append(film_chain + ",asplit=2[film][ck]"); key_src = "[ck]"
    else:
        ga.append(film_chain + "[film]")
    mix_in = ["[film]"]
    if voice:
        ins += ["-i", voice["src"]]
        delay = int(float(voice.get("start", 0.0)) * 1000)
        vchain = f"[{nin}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={delay}:all=1,volume={float(voice.get('gain', 0)):.2f}dB"
        nin += 1
        if duck == "voice" and music:
            ga.append(vchain + ",asplit=2[vk][vm]"); key_src = "[vk]"
        else:
            ga.append(vchain + "[vm]")
        mix_in.append("[vm]")
    if music:
        loop = ["-stream_loop", "-1"] if music.get("loop", True) else []
        ins += [*loop, "-i", music["src"]]
        delay = int(float(music.get("start", 0.0)) * 1000)
        fi, fo = float(music.get("fade_in", 0.0)), float(music.get("fade_out", 1.5))
        mchain = [f"[{nin}:a]aformat=sample_rates=48000:channel_layouts=stereo", f"atrim=0:{max(0.1, total - delay / 1000):.3f}", "asetpts=N/SR/TB"]
        if fi > 0:
            mchain.append(f"afade=t=in:st=0:d={fi:.3f}")
        if fo > 0:
            mchain.append(f"afade=t=out:st={max(0.0, total - delay / 1000 - fo):.3f}:d={fo:.3f}")
        if delay:
            mchain.append(f"adelay={delay}:all=1")
        mchain.append(f"volume={float(music.get('gain', 0)):.2f}dB")
        ga.append(",".join(mchain) + "[bed0]")
        nin += 1
        if key_src:
            ga.append(f"[bed0]{key_src}sidechaincompress=threshold=0.02:ratio=12:attack=20:release=300:makeup=1[bed]")
        else:
            ga.append("[bed0]anull[bed]")
        mix_in.append("[bed]")
    for j, e in enumerate(au.get("sfx") or []):
        if e["at"] >= total:
            continue
        ins += ["-i", e["src"]]
        ga.append(f"[{nin}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(e['at'] * 1000)}:all=1,volume={e['gain']:.2f}dB[fx{j}]")
        nin += 1; mix_in.append(f"[fx{j}]")
    if len(mix_in) > 1:
        ga.append(f"{''.join(mix_in)}amix=inputs={len(mix_in)}:normalize=0:duration=first[pre]")
    else:
        ga.append(f"{mix_in[0]}anull[pre]")
    ga.append("[pre]aformat=sample_fmts=flt:sample_rates=48000:channel_layouts=stereo[aout]")   # raw mix; loudness is set after measuring
    pic, raw, snd = tmp / "picture.mp4", tmp / "mix.wav", tmp / "sound.m4a"
    cmd_v = [FF, "-y", "-v", "error", *ins, "-filter_complex", ";".join(gv), "-map", last_v, "-an",
             "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-t", f"{total:.3f}", str(pic)]
    cmd_a = [FF, "-y", "-v", "error", *ins, "-filter_complex", ";".join(ga), "-map", "[aout]", "-vn",
             "-c:a", "pcm_f32le", "-t", f"{total:.3f}", str(raw)]
    cmd_mux = [FF, "-y", "-v", "error", "-i", str(pic), "-i", str(snd), "-map", "0:v:0", "-map", "1:a:0", "-c", "copy",
               "-movflags", "+faststart", "-t", f"{total:.3f}", str(out)]
    rep = {"file": str(out), "size": f"{W}x{H}", "fps": fps, "seconds": round(total, 3), "clips": [{k: v for k, v in s.items() if k != "file"} for s in segs],
           "transitions": used_tr, "overlays": ov_report, "audio": {"music": bool(music), "voice": bool(voice), "sfx": len(au.get("sfx") or []), "duck": duck, "keep_clip_audio": film_vol > 0, "lufs": au["lufs"]},
           "workers": n_workers}
    if dry_run:
        rep["command"] = "\n".join(subprocess.list2cmdline(c) for c in (cmd_v, cmd_a, cmd_mux))
        rep["graph"] = gv + ga
        shutil.rmtree(tmp, ignore_errors=True)
        return rep
    with ThreadPoolExecutor(2) as ex:                               # picture and sound side by side
        list(ex.map(tools._run, (cmd_v, cmd_a)))
    rep["audio"]["measured_lufs"] = _normalize_audio(raw, snd, au["lufs"])
    tools._run(cmd_mux)
    (tmp / "graph.txt").write_text("\n".join(gv + ["", "# sound"] + ga), encoding="utf-8")
    if inspect:
        import qa
        gate = qa.inspect(out)
        rep["gate"] = {k: gate.get(k) for k in ("ok", "issues", "warnings", "lufs", "true_peak", "duration")}
    out.with_suffix(".timeline.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    if not keep_tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    else:
        rep["tmp"] = str(tmp)
    return rep


def os_cpu() -> int:
    import os
    return os.cpu_count() or 2


def summary(spec: dict | str | Path) -> dict:
    """What the film will be, without encoding: per-clip output durations (speed/ramp applied), transition points,
    overlay windows and the total — for the site's timeline strip and for a quick check before a render."""
    sp = load(spec)
    clips, total, points = [], 0.0, []
    for i, c in enumerate(sp["clips"]):
        src_dur = _clip_source_dur(c)
        if c.get("ramp"):
            _, out_dur = ramp_pieces(c["ramp"], src_dur)
        else:
            out_dur = src_dur / c["speed"]
        tr = c.get("transition")
        d_tr = min(tr["dur"], out_dur * 0.5) if tr else 0.0
        start = total
        if i > 0 and clips[-1]["transition"]:
            start = total - clips[-1]["transition"]["dur"]
        clips.append({"i": i, "kind": c["kind"], "src": c.get("src") or c.get("image") or c.get("color"), "in": c.get("in"), "out": c.get("out"),
                      "source_dur": round(src_dur, 3), "dur": round(out_dur, 3), "speed": None if c.get("ramp") else c["speed"], "ramp": c.get("ramp"),
                      "zoom": c.get("zoom"), "grade": c.get("grade", "none"), "transition": ({**tr, "dur": round(d_tr, 3)} if tr else None), "start": round(start, 3)})
        total = start + out_dur
        if tr:
            points.append({"after_clip": i, "type": tr["type"], "at": round(total - d_tr, 3), "dur": round(d_tr, 3)})
    if clips and clips[-1]["transition"]:
        clips[-1]["transition"] = None; points = points[:-1]
    ovs = [{k: o.get(k) for k in ("type", "text", "title", "src", "start", "end", "pos", "anim", "style")} for o in sp["overlays"]]
    return {"size": f"{sp['W']}x{sp['H']}", "fps": sp["fps"], "seconds": round(total, 3), "clips": clips, "transitions": points, "overlays": ovs,
            "audio": {k: (bool(v) if k in ("music", "voice") else [{"src": Path(e["src"]).name, "at": e["at"]} for e in v] if k == "sfx" else v) for k, v in sp["audio"].items()}}


EXAMPLE = {
    "ratio": "9:16", "fps": 30, "background": "#0d1b2a",
    "clips": [
        {"src": "clip_a.mp4", "in": 0, "out": 4.0, "zoom": {"from": 1.0, "to": 1.08}, "grade": "teal_orange", "transition": {"type": "circleopen", "dur": 0.6}},
        {"src": "clip_b.mp4", "in": 2.0, "out": 7.0, "ramp": [[0, 1.0], [2.0, 0.3], [4.0, 1.0]], "transition": "slideup"},
        {"image": "photo.jpg", "dur": 3.0, "zoom": {"from": 1.0, "to": 1.15}, "transition": {"type": "fadeblack", "dur": 0.8}},
        {"color": "#000000", "dur": 0.8},
    ],
    "overlays": [
        {"type": "text", "text": "عنوان الفيلم", "start": 0.4, "end": 3.4, "pos": "center", "size": 110, "anim": "rise", "box": "#00000080"},
        {"type": "lower-third", "title": "اسم المتحدث", "sub": "الوظيفة", "start": 4.5, "end": 8.5, "accent": "#E7B65A"},
        {"type": "progress", "color": "#E7B65A", "height": 10, "from": "right"},
    ],
    "audio": {"music": {"src": "music.wav", "gain": -4, "fade_in": 0.8, "fade_out": 2.0}, "keep_clip_audio": True, "duck": "auto", "lufs": -14},
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?", help="timeline JSON")
    ap.add_argument("--out", help="film MP4")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true", help="print the FFmpeg command and graph instead of rendering")
    ap.add_argument("--inspect", action="store_true", help="run the delivery gate on the result")
    ap.add_argument("--keep-tmp", action="store_true")
    ap.add_argument("--example", metavar="OUT.json", help="write a sample spec")
    ap.add_argument("--transitions", action="store_true", help="list the transitions of this FFmpeg build")
    a = ap.parse_args()
    if a.transitions:
        for t in transitions():
            print(f"{t:<14} {transition_ar(t)}")
        return 0
    if a.example:
        Path(a.example).write_text(json.dumps(EXAMPLE, ensure_ascii=False, indent=1), encoding="utf-8")
        print(a.example); return 0
    if not a.spec or not a.out:
        ap.error("SPEC.json and --out are required (or --example / --transitions)")
    rep = build(a.spec, Path(a.out), a.workers, a.dry_run, a.inspect, a.keep_tmp)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("graph",)}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
