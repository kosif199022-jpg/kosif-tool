#!/usr/bin/env python3
"""Black Dragon mandatory video-product protocol (one path, fixed order).

Every video product the Black Dragon makes walks the same seven stages:

  1 brief         goal, audience, platform, aspect, duration, message, hero
  2 concept       idea, visual metaphor, hook
  3 color-design  measured palette (60/30/10) and ONE accent on the hero
  4 shots         timed shot plan; every shot says where the accent is
  5 produce       real output files (hashed); paid tools need approval
  6 qa-color      the same color check, measured on the real output
  7 deliver       what was executed and what was not

Each stage also has MANDATORY CORE SKILLS: the Black Dragon's own tools
(Dragon Mind, the tool matrix, Infinite Matrices, the 86-style atlas, the
reel-hook scorer, the 25 motion-graphics repos, the renderers and the
delivery gate). `core ID --job J -- ARGS` runs one of them for real and keeps
a sealed receipt (command, exit code, log hash). A stage is refused until
every required core of that stage has a receipt with exit 0.

A stage can only be recorded after the one before it. `check` fails closed
(exit 5) when any stage is missing, out of order, edited after recording,
or when the color checks do not pass. Color stages are computed from real
pixels, never typed in by hand.

The color rule comes from the "one accent" method: two calm base colors
(about 60% + 30%) and a single accent (about 10%) placed on the element that
carries the message. Three ways to pick the accent: opposite of the
background (contrast), the color whose feeling is the idea (emotion), or a
neon when the palette is dull (neon).
"""
from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "kosif.black-dragon.video-protocol.v2"
STAGES = ("brief", "concept", "color-design", "shots", "produce", "qa-color", "deliver")
COMPUTED = {"color-design", "qa-color"}
REQUIRED = {
    "brief": ("goal", "audience", "platform", "aspect", "duration_s", "message", "hero"),
    "concept": ("idea", "metaphor", "hook"),
    "shots": ("shots",),
    "produce": ("outputs", "tool", "paid", "spend_approved"),
    "deliver": ("summary", "executed", "not_executed"),
}
RULES = ("contrast", "emotion", "neon")
# Accent share window for the final output. The method says ~10%; we allow
# a small accent (>= 0.5%) up to 18% so a close-up of the hero still passes.
ACCENT_MIN, ACCENT_MAX = 0.005, 0.18
MIN_POP = 40.0              # Delta E accent vs background: the accent must pop.
# WCAG luminance contrast is reported too, but a red on teal pops with a low
# luminance ratio, so the gate uses color distance, not luminance.
# Planned vs produced accent: renders, light and video compression shift the
# tone, so "same accent" means the same hue family and a bounded Delta E.
MAX_HUE_DRIFT = 20.0        # degrees
MAX_ACCENT_DRIFT = 45.0     # Delta E
EMOTIONS = {
    # feeling words (Arabic + English) -> accent hex
    "غضب": "#E0242B", "anger": "#E0242B", "خطر": "#E0242B", "danger": "#E0242B",
    "قوة": "#FF5A1F", "power": "#FF5A1F", "طاقة": "#FF5A1F", "energy": "#FF5A1F",
    "حماس": "#FF5A1F", "excitement": "#FF5A1F",
    "تفاؤل": "#FFC400", "فرح": "#FFC400", "joy": "#FFC400", "optimism": "#FFC400",
    "نمو": "#39FF14", "growth": "#39FF14", "جيمنج": "#39FF14", "gaming": "#39FF14",
    "تقنية": "#00E5FF", "tech": "#00E5FF", "مستقبل": "#00E5FF", "future": "#00E5FF",
    "ثقة": "#1E6BFF", "trust": "#1E6BFF", "هدوء": "#1E6BFF", "calm": "#1E6BFF",
    "فخامة": "#B000FF", "luxury": "#B000FF", "غموض": "#B000FF", "mystery": "#B000FF",
    "حب": "#FF2E88", "love": "#FF2E88", "أنوثة": "#FF2E88",
}
NEONS = ("#39FF14", "#FF5A1F", "#B000FF", "#00E5FF", "#FF2E88", "#FFE600")
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}

ROOT = Path(__file__).resolve().parents[4]
_SP = ".claude/skills/kosif-superpowers/scripts/"
_SELF = ".claude/skills/kosif-black-dragon/scripts/video_protocol.py"
# Core skills of the Black Dragon. Only these repo-owned programs can be run
# by `core`; the arguments after `--` are the caller's.
CORES = {
    "mind-think": {"stage": "brief", "run": "python3",
                   "script": ".claude/skills/kosif-dragon-mind/scripts/dragon_mind.py", "sub": ["think"],
                   "ar": "عقل التنين: يفكك المهمة لـ٢٦ ملكة وست مراحل تفكير"},
    "tool-matrix": {"stage": "brief", "run": "python3", "script": _SP + "hub.py", "sub": ["find"],
                    "ar": "مصفوفة الأدوات: ٢١٠ أداة + كتالوج القدرات، مرتبة للمهمة ومين جاهز يشتغل"},
    "matrices": {"stage": "concept", "run": "python3",
                 "script": ".claude/skills/kosif-infinite-matrices/scripts/kmx.py", "sub": ["ideate"],
                 "ar": "المصفوفات اللانهائية: أنظمة بصرية وحركية جديدة من طوب سببي من ٨٦ أسلوب"},
    "style-atlas": {"stage": "concept", "run": "python3", "script": _SP + "style_atlas_bridge.py",
                    "sub": [], "ar": "أطلس الأساليب الـ٨٦: بحث، أو خطة دمج ٨٥/١٥"},
    "reel-hooks": {"stage": "concept", "run": "python3",
                   "script": ".claude/skills/kosif-reel-hooks/scripts/reel_tools.py", "sub": [],
                   "ar": "الهوكات: تقييم الهوكات وشيت الإيقاع المتوقت"},
    "motion-repos": {"stage": "shots", "run": "python3", "script": _SELF, "sub": ["repos"],
                     "ar": "مستودعات الموشن جرافيك: ٢٥ محرك + ٢٥ مصدر + مستودعاتك، مرتبة للمهمة"},
    "web-film-plan": {"stage": "shots", "run": "python3",
                      "script": ".claude/skills/kosif-web-film/scripts/web_film.py", "sub": ["plan"],
                      "ar": "خطة لقطات فيلم الويب (التنين الأسود)"},
    "montage-options": {"stage": "shots", "run": "python3", "script": _SP + "montage_pro.py",
                        "sub": ["options"], "ar": "قائمة خيارات فريق مونتاج برو على مادة مرفوعة"},
    "kmx-recipe": {"stage": "shots", "run": "python3",
                   "script": ".claude/skills/kosif-infinite-matrices/scripts/kmx.py", "sub": ["recipe"],
                   "ar": "التحقق من وصفة المصفوفات قبل التنفيذ"},
    "shadow-check": {"stage": "shots", "run": "python3",
                     "script": ".claude/skills/kosif-shadow-theatre/scripts/shadow_theatre.py",
                     "sub": ["check"], "ar": "فحص مشهد مسرح الظل"},
    "web-film-render": {"stage": "produce", "run": "node", "script": "tools/render_html.cjs", "sub": [],
                        "ar": "رندر فيلم الويب لـ MP4 أو كادرات"},
    "motion-director": {"stage": "produce", "run": "python3", "script": _SP + "motion_director.py",
                        "sub": [], "ar": "Motion Director: سكريبت متوقت ← أنيميشن SVG ← MP4"},
    "motion-runtime": {"stage": "produce", "run": "python3", "script": _SP + "motion_runtime.py",
                       "sub": [], "ar": "Motion Runtime: فيلم SVG أصلي + رندر"},
    "montage-build": {"stage": "produce", "run": "python3", "script": _SP + "montage_pro.py",
                      "sub": ["build"], "ar": "مونتاج برو: بناء الخيار المختار"},
    "cinema-run": {"stage": "produce", "run": "python3", "script": _SP + "cinematic_pro_conductor.py",
                   "sub": ["run"], "ar": "سينما برو: من المادة للرندر بفحص مستقل"},
    "kmx-experiment": {"stage": "produce", "run": "python3",
                       "script": ".claude/skills/kosif-infinite-matrices/scripts/kmx.py",
                       "sub": ["experiment"], "ar": "تجربة المصفوفات A/B/C مع رندر"},
    "shadow-render": {"stage": "produce", "run": "python3",
                      "script": ".claude/skills/kosif-shadow-theatre/scripts/shadow_theatre.py",
                      "sub": ["render"], "ar": "رندر فيلم مسرح الظل"},
    "media-verify": {"stage": "qa-color", "run": "python3", "script": _SP + "verify_video.py", "sub": [],
                     "ar": "بوابة التسليم: كودك، مقاس، فريمات، مدة، صوت"},
    "web-film-check": {"stage": "qa-color", "run": "python3",
                       "script": ".claude/skills/kosif-web-film/scripts/web_film.py", "sub": ["check"],
                       "ar": "فحص فيلم الويب: لقطات، إيقاع، seek، حتمية"},
}
# Per stage: every group is mandatory; inside a group any one core counts.
REQUIRED_CORES = {
    "brief": [("mind-think",), ("tool-matrix",)],
    "concept": [("matrices",), ("style-atlas",), ("reel-hooks",)],
    "color-design": [],
    "shots": [("motion-repos",), ("web-film-plan", "montage-options", "kmx-recipe", "shadow-check")],
    "produce": [("web-film-render", "motion-director", "motion-runtime", "montage-build",
                 "cinema-run", "kmx-experiment", "shadow-render")],
    "qa-color": [("media-verify", "web-film-check")],
    "deliver": [],
}
CORE_TIMEOUT = 1800


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(data) -> bytes:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- color math
def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.strip().lstrip("#")
    if len(h) != 6:
        raise ValueError(f"bad hex color: #{h}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(c) -> str:
    return "#%02X%02X%02X" % tuple(int(round(max(0, min(255, v)))) for v in c)


def _lin(v: float) -> float:
    v /= 255.0
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def luminance(c) -> float:
    r, g, b = (_lin(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


def lab(c):
    r, g, b = (_lin(v) for v in c)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a, b) -> float:
    return round(math.dist(lab(a), lab(b)), 1)


def hue_gap(a, b) -> float:
    ha = colorsys.rgb_to_hsv(*(v / 255 for v in a))[0] * 360
    hb = colorsys.rgb_to_hsv(*(v / 255 for v in b))[0] * 360
    d = abs(ha - hb) % 360
    return round(min(d, 360 - d), 1)


def saturation(c) -> float:
    return colorsys.rgb_to_hsv(*(v / 255 for v in c))[1]


def palette(pixels, k: int = 8, iters: int = 15):
    """Deterministic k-means on RGB pixels (numpy). Returns [(rgb, share)]."""
    import numpy as np
    px = np.asarray(pixels, dtype=np.float64).reshape(-1, 3)
    # deterministic init: quantiles of brightness then by hue spread
    order = np.argsort(px.sum(1))
    centers = px[order[np.linspace(0, len(px) - 1, k).astype(int)]].copy()
    for _ in range(iters):
        d = ((px[:, None, :] - centers[None]) ** 2).sum(2)
        lab_ = d.argmin(1)
        for j in range(k):
            m = px[lab_ == j]
            if len(m):
                centers[j] = m.mean(0)
    d = ((px[:, None, :] - centers[None]) ** 2).sum(2)
    lab_ = d.argmin(1)
    out = []
    for j in range(k):
        share = float((lab_ == j).mean())
        if share > 0:
            out.append((tuple(float(v) for v in centers[j]), share))
    # merge near-duplicates (Delta E < 8)
    merged: list[list] = []
    for c, s in sorted(out, key=lambda t: -t[1]):
        for m in merged:
            if delta_e(m[0], c) < 8:
                m[1] += s
                break
        else:
            merged.append([c, s])
    return [(tuple(c), s) for c, s in merged]


def frames_from(path: Path) -> list[Path]:
    """Images as-is; for a video grab frames at 20/50/80% with ffmpeg."""
    if path.suffix.lower() not in VIDEO_EXT:
        return [path]
    ff, fp = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ff or not fp:
        raise ValueError("ffmpeg/ffprobe needed to read video frames")
    dur = float(subprocess.run([fp, "-v", "error", "-show_entries", "format=duration", "-of",
                                "csv=p=0", str(path)], capture_output=True, text=True,
                               check=True).stdout.strip() or 0)
    tmp = Path(tempfile.mkdtemp(prefix="bd-frames-"))
    out = []
    for i, f in enumerate((0.2, 0.5, 0.8)):
        dst = tmp / f"f{i}.png"
        subprocess.run([ff, "-v", "error", "-y", "-ss", f"{dur * f:.2f}", "-i", str(path),
                        "-frames:v", "1", str(dst)], check=True)
        if dst.is_file():
            out.append(dst)
    if not out:
        raise ValueError("could not extract frames from video")
    return out


def load_pixels(path: Path, box=None):
    from PIL import Image
    img = Image.open(path).convert("RGB")
    if box:
        x, y, w, h = box
        W, H = img.size
        img = img.crop((int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)))
    img.thumbnail((160, 160))
    import numpy as np
    return np.asarray(img).reshape(-1, 3).tolist(), img.size


def suggest(background, emotion: str | None) -> dict:
    """Three accents for the three rules."""
    h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in background))
    opp = colorsys.hsv_to_rgb((h + 0.5) % 1.0, max(0.75, s), max(0.85, v))
    out = {"contrast": rgb_hex([x * 255 for x in opp])}
    key = (emotion or "").strip().lower()
    out["emotion"] = EMOTIONS.get(key) or EMOTIONS.get(emotion or "", None)
    out["neon"] = max(NEONS, key=lambda n: delta_e(hex_rgb(n), background))
    return out


def find_accent(pixels, background):
    """The accent = the biggest group of vivid pixels whose hue differs from
    the background. Measured per pixel, so a shaded 3D object still counts.
    Returns (rgb, share) or None."""
    import numpy as np
    px = np.asarray(pixels, dtype=np.float64).reshape(-1, 3) / 255.0
    mx, mn = px.max(1), px.min(1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0)
    vivid = (sat >= 0.45) & (mx >= 0.35)
    if vivid.sum() == 0:
        return None
    hue = np.array([colorsys.rgb_to_hsv(*p)[0] for p in px[vivid]])
    bins = (hue * 24).astype(int) % 24
    bh, bs, bv = colorsys.rgb_to_hsv(*(v / 255 for v in background))
    bg_bin = int(bh * 24) % 24 if bs >= 0.35 and bv >= 0.25 else None
    counts = np.bincount(bins, minlength=24).astype(float)
    if bg_bin is not None:
        for d in (-2, -1, 0, 1, 2):
            counts[(bg_bin + d) % 24] = 0
    # group each bin with its neighbours, pick the strongest hue family
    fam = np.array([counts[(i - 1) % 24] + counts[i] + counts[(i + 1) % 24] for i in range(24)])
    best = int(fam.argmax())
    if fam[best] == 0:
        return None
    members = np.isin(bins, [(best - 1) % 24, best, (best + 1) % 24])
    share = float(members.sum()) / len(px)
    if share < 0.005:
        return None
    sel = px[vivid][members]
    strength = sel.max(1) * (sel.max(1) - sel.min(1))
    top = sel[strength >= np.quantile(strength, 0.5)]
    rgb = tuple(float(v) * 255 for v in np.median(top, 0))
    if delta_e(rgb, background) < 25:
        return None
    return rgb, share


def analyze(path: Path, *, box=None, emotion=None) -> dict:
    frames = frames_from(path)
    pixels = []
    for f in frames:
        pixels += load_pixels(f, box)[0]
    pal = palette(pixels)
    pal.sort(key=lambda t: -t[1])
    background = pal[0][0]
    accent = find_accent(pixels, background)
    a_share = accent[1] if accent else 0.0
    roles = [{"hex": rgb_hex(c), "share": round(s, 4),
              "role": "dominant" if i == 0 else "support",
              "saturation": round(saturation(c), 2)} for i, (c, s) in enumerate(pal)]
    return {
        "source": str(path), "frames": len(frames),
        "palette": roles,
        "background": rgb_hex(background),
        "accent": rgb_hex(accent[0]) if accent else None,
        "accent_share": round(a_share, 4),
        "accent_contrast": contrast(accent[0], background) if accent else None,
        "accent_pop": delta_e(accent[0], background) if accent else None,
        "rule_60_30_10": {"dominant": round(pal[0][1], 3),
                          "support": round(max(0.0, 1 - pal[0][1] - a_share), 3),
                          "accent": round(a_share, 3)},
        "suggestions": suggest(background, emotion),
    }


# ---------------------------------------------------------------- job files
def job_file(job: Path) -> Path:
    return job / "protocol.json"


def load(job: Path) -> dict:
    p = job_file(job)
    if not p.is_file():
        raise ValueError(f"no protocol in {job}; run: start \"<task>\" --job {job}")
    return json.loads(p.read_text(encoding="utf-8"))


def save(job: Path, state: dict) -> None:
    job_file(job).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def start(task: str, job: Path) -> dict:
    if not task.strip():
        raise ValueError("task cannot be empty")
    job.mkdir(parents=True, exist_ok=True)
    if job_file(job).exists():
        raise ValueError(f"protocol already started in {job}")
    state = {"schema": SCHEMA, "task": task, "created": now(), "stages": {},
             "order": list(STAGES)}
    save(job, state)
    return {"job": str(job), "next": STAGES[0], "stages": list(STAGES)}


def _next(state: dict) -> str | None:
    for s in STAGES:
        if s not in state["stages"]:
            return s
    return None


def _seal(stage: str, data: dict) -> dict:
    data = dict(data, stage=stage, recorded=now())
    data["seal"] = hashlib.sha256(canonical({k: v for k, v in data.items() if k != "seal"})).hexdigest()
    return data


def _gate(state: dict, stage: str) -> None:
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage}; stages: {', '.join(STAGES)}")
    if stage in state["stages"]:
        raise ValueError(f"stage {stage} already recorded")
    want = _next(state)
    if stage != want:
        raise ValueError(f"stage {stage} is out of order; next mandatory stage is {want}")


def validate(stage: str, data: dict, state: dict) -> list[str]:
    errs = [f"{stage}: missing {k}" for k in REQUIRED.get(stage, ()) if data.get(k) in (None, "", [])]
    if errs:
        return errs
    if stage == "brief":
        try:
            if float(data["duration_s"]) <= 0:
                errs.append("brief: duration_s must be > 0")
        except (TypeError, ValueError):
            errs.append("brief: duration_s must be a number")
    if stage == "shots":
        shots = data["shots"]
        if not isinstance(shots, list):
            return ["shots: shots must be a list"]
        total = 0.0
        for i, s in enumerate(shots, 1):
            for k in ("duration_s", "what", "accent_on"):
                if not isinstance(s, dict) or s.get(k) in (None, ""):
                    errs.append(f"shots: shot {i} missing {k}")
            if isinstance(s, dict):
                try:
                    total += float(s.get("duration_s") or 0)
                except (TypeError, ValueError):
                    errs.append(f"shots: shot {i} duration_s must be a number")
        want = float(state["stages"]["brief"]["duration_s"])
        if not errs and not (0.8 * want <= total <= 1.2 * want):
            errs.append(f"shots: total {total:.1f}s is not within 20% of the brief's {want:g}s")
    if stage == "produce":
        if data["paid"] is True and data["spend_approved"] is not True:
            errs.append("produce: a paid tool was used without the owner's approval")
        for o in data["outputs"]:
            if not Path(o["path"]).is_file() or sha(Path(o["path"])) != o["sha256"]:
                errs.append(f"produce: output missing or changed: {o['path']}")
    return errs


def record(job: Path, stage: str, data: dict) -> dict:
    state = load(job)
    _gate(state, stage)
    if stage in COMPUTED:
        raise ValueError(f"{stage} is measured from pixels; use the `color` command")
    _require_cores(state, stage)
    if stage == "produce":
        outs = []
        for o in data.get("outputs") or []:
            p = Path(o if isinstance(o, str) else o["path"])
            if not p.is_file():
                raise ValueError(f"produce: output file not found: {p}")
            outs.append({"path": str(p), "sha256": sha(p)})
        data = dict(data, outputs=outs)
    errs = validate(stage, data, state)
    if errs:
        raise ValueError("; ".join(errs))
    state["stages"][stage] = _seal(stage, data)
    save(job, state)
    return {"recorded": stage, "next": _next(state)}


def color(job: Path, stage: str, image: Path, *, rule=None, accent=None, box=None) -> dict:
    state = load(job)
    if stage not in COMPUTED:
        raise ValueError("color stage must be color-design or qa-color")
    _gate(state, stage)
    _require_cores(state, stage)
    if not image.is_file():
        raise ValueError(f"image or video not found: {image}")
    emotion = state["stages"].get("concept", {}).get("emotion")
    res = analyze(image, box=box, emotion=emotion)
    res["source_sha256"] = sha(image)
    checks = {}
    if stage == "color-design":
        if rule not in RULES:
            raise ValueError("color-design needs --rule contrast|emotion|neon")
        chosen = accent or res["suggestions"].get(rule)
        if not chosen:
            raise ValueError("rule emotion needs an `emotion` word in the concept stage, or pass --accent")
        bg = hex_rgb(res["background"])
        res.update(rule=rule, chosen_accent=chosen.upper(),
                   hero=state["stages"]["brief"]["hero"])
        checks["one_accent_only"] = True
        checks["accent_contrast"] = contrast(hex_rgb(chosen), bg)
        checks["accent_pop"] = delta_e(hex_rgb(chosen), bg)
        checks["accent_pop_ok"] = checks["accent_pop"] >= MIN_POP
        res["passed"] = checks["accent_pop_ok"]
    else:
        planned = state["stages"]["color-design"]["chosen_accent"]
        produced = state["stages"]["produce"]["outputs"]
        checks["output_is_produced_file"] = any(o["sha256"] == res["source_sha256"] for o in produced)
        checks["accent_found"] = res["accent"] is not None
        checks["accent_share_ok"] = ACCENT_MIN <= res["accent_share"] <= ACCENT_MAX
        checks["accent_drift"] = delta_e(hex_rgb(res["accent"]), hex_rgb(planned)) if res["accent"] else None
        checks["hue_drift"] = hue_gap(hex_rgb(res["accent"]), hex_rgb(planned)) if res["accent"] else None
        checks["accent_matches_plan"] = (checks["accent_drift"] is not None
                                         and checks["accent_drift"] <= MAX_ACCENT_DRIFT
                                         and checks["hue_drift"] <= MAX_HUE_DRIFT)
        checks["accent_pop_ok"] = (res["accent_pop"] or 0) >= MIN_POP
        res["passed"] = all(checks[k] for k in ("output_is_produced_file", "accent_found",
                                                  "accent_share_ok", "accent_matches_plan",
                                                  "accent_pop_ok"))
    res["checks"] = checks
    state["stages"][stage] = _seal(stage, res)
    save(job, state)
    return {"recorded": stage, "passed": res["passed"], "checks": checks,
            "accent": res.get("chosen_accent") or res["accent"],
            "suggestions": res["suggestions"], "next": _next(state)}


def _receipts(state: dict, stage: str) -> list[dict]:
    return [r for r in state.get("cores", []) if r["stage"] == stage and r["exit"] == 0]


def missing_cores(state: dict, stage: str) -> list[tuple]:
    done = {r["core"] for r in _receipts(state, stage)}
    return [g for g in REQUIRED_CORES.get(stage, []) if not done & set(g)]


def _require_cores(state: dict, stage: str) -> None:
    miss = missing_cores(state, stage)
    if miss:
        need = "; ".join(" or ".join(g) for g in miss)
        raise ValueError(f"stage {stage} needs its core skills first: {need} "
                         f"(run: core <id> --job <job> -- <args>; list: cores)")


def run_core(job: Path, core: str, args: list[str], *, root: Path = ROOT) -> dict:
    """Run one core skill for real and keep a sealed receipt."""
    state = load(job)
    if core not in CORES:
        raise ValueError(f"unknown core {core}; see: cores")
    spec = CORES[core]
    want = _next(state)
    if spec["stage"] != want:
        raise ValueError(f"core {core} belongs to stage {spec['stage']}; the current stage is {want}")
    script = root / spec["script"]
    if not script.is_file():
        raise ValueError(f"core program missing: {spec['script']}")
    runner = sys.executable if spec["run"] == "python3" else shutil.which(spec["run"])
    if not runner:
        raise ValueError(f"{spec['run']} is not installed")
    sub = [a for a in spec["sub"] if not args or args[0] != a]
    cmd = [runner, str(script), *sub, *args]
    logs = job / "core"
    logs.mkdir(exist_ok=True)
    n = len(state.get("cores", [])) + 1
    log = logs / f"{n:02d}-{core}.log"
    started = now()
    try:
        proc = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=CORE_TIMEOUT)
        code, out, err = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        code, out, err = 124, exc.stdout or "", f"timeout after {CORE_TIMEOUT}s"
        out = out.decode() if isinstance(out, bytes) else out
    log.write_text(f"$ {' '.join(cmd[1:])}\n--- stdout\n{out}\n--- stderr\n{err}", encoding="utf-8")
    rec = {"core": core, "stage": spec["stage"], "cmd": [spec["run"], spec["script"], *sub, *args],
           "exit": code, "started": started, "log": str(log), "log_sha256": sha(log)}
    rec["seal"] = hashlib.sha256(canonical(rec)).hexdigest()
    state.setdefault("cores", []).append(rec)
    save(job, state)
    return {"core": core, "exit": code, "log": str(log), "tail": (out or err)[-600:],
            "stage_missing": [" or ".join(g) for g in missing_cores(state, spec["stage"])]}


def cores_table(stage: str | None = None) -> dict:
    out = {}
    for st in STAGES:
        if stage and st != stage:
            continue
        out[st] = {"required": [list(g) for g in REQUIRED_CORES[st]],
                   "cores": {k: {"program": v["script"], "what": v["ar"]}
                             for k, v in CORES.items() if v["stage"] == st}}
    return out


def _tokens(text: str) -> set[str]:
    import re
    return {w for w in re.split(r"[^\w]+", text.lower()) if len(w) > 1}


def repos(query: str, *, root: Path = ROOT, limit: int = 8) -> dict:
    """Rank the motion-graphics repositories for a task (engines, sources, owned)."""
    data = root / ".claude/skills/kosif-superpowers/data"
    items = []
    eng = json.loads((data / "motion_engines.json").read_text(encoding="utf-8"))["engines"]
    for e in eng:
        items.append({"kind": "engine", "repo": e["repo"], "family": e.get("family", ""),
                      "license": e.get("license_note", ""), "status": e.get("status", ""),
                      "text": " ".join([e["repo"], e.get("family", ""), " ".join(e.get("capabilities", [])),
                                        e.get("integration", ""), e.get("builtin_equivalent", "")])})
    for m in json.loads((data / "motion_sources.json").read_text(encoding="utf-8"))["sources"]:
        items.append({"kind": "source", "repo": m["repo"], "family": m.get("role", ""),
                      "license": m.get("license_hint", ""), "status": m.get("runtime_state", ""),
                      "text": " ".join([m["repo"], m.get("name", ""), m.get("role", ""), m.get("capability", "")])})
    for r in json.loads((data / "owned_repos.json").read_text(encoding="utf-8"))["repos"]:
        if "motion" in r.get("groups", []) or "3d" in r.get("groups", []):
            items.append({"kind": "owned", "repo": r["repo"], "family": ",".join(r.get("groups", [])),
                          "license": r.get("visibility", ""), "status": r.get("state", ""),
                          "text": " ".join([r["repo"], r.get("purpose_ar", ""), r.get("purpose_en", "")])})
    q = _tokens(query) | {"motion", "video", "animation", "render", "mp4"}
    for it in items:
        it["score"] = len(_tokens(it.pop("text")) & q) + (2 if it["kind"] == "owned" else 0)
    items.sort(key=lambda x: (-x["score"], x["kind"], x["repo"]))
    return {"query": query, "total": len(items),
            "counts": {k: sum(1 for i in items if i["kind"] == k) for k in ("engine", "source", "owned")},
            "top": items[:limit],
            "note": "Licence notes are hints: check each repo's licence before reusing its code."}


def check(job: Path) -> dict:
    state = load(job)
    problems = []
    for s in STAGES:
        d = state["stages"].get(s)
        if d is None:
            problems.append(f"missing stage: {s}")
            continue
        body = {k: v for k, v in d.items() if k != "seal"}
        if hashlib.sha256(canonical(body)).hexdigest() != d.get("seal"):
            problems.append(f"stage {s} was edited after it was recorded")
        if s in COMPUTED and not d.get("passed"):
            problems.append(f"stage {s} did not pass: {d.get('checks')}")
        if s in COMPUTED and Path(d["source"]).is_file() and sha(Path(d["source"])) != d["source_sha256"]:
            problems.append(f"stage {s}: measured file changed after the check")
    for r in state.get("cores", []):
        body = {k: v for k, v in r.items() if k != "seal"}
        if hashlib.sha256(canonical(body)).hexdigest() != r.get("seal"):
            problems.append(f"core receipt {r['core']} was edited")
        elif not Path(r["log"]).is_file() or sha(Path(r["log"])) != r["log_sha256"]:
            problems.append(f"core log missing or changed: {r['log']}")
    for st in STAGES:
        for g in missing_cores(state, st):
            problems.append(f"stage {st}: core skill not run: {' or '.join(g)}")
    if list(state["stages"]) != [s for s in STAGES if s in state["stages"]]:
        problems.append("stages were recorded out of order")
    for o in state["stages"].get("produce", {}).get("outputs", []):
        if not Path(o["path"]).is_file() or sha(Path(o["path"])) != o["sha256"]:
            problems.append(f"output missing or changed: {o['path']}")
    used = sorted({r["core"] for r in state.get("cores", []) if r["exit"] == 0})
    return {"job": str(job), "task": state["task"], "passed": not problems,
            "cores_used": used,
            "done": [s for s in STAGES if s in state["stages"]],
            "next": _next(state), "problems": problems}


def _box(text: str | None):
    if not text:
        return None
    vals = [float(v) for v in text.split(",")]
    if len(vals) != 4 or not all(0 <= v <= 1 for v in vals):
        raise ValueError("--hero-box is x,y,w,h as fractions 0..1")
    return vals


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("start", help="open a protocol job for a video product")
    p.add_argument("task"); p.add_argument("--job", type=Path, required=True)
    r = sub.add_parser("record", help="record a typed stage from a JSON file")
    r.add_argument("stage"); r.add_argument("--job", type=Path, required=True)
    r.add_argument("--data", type=Path, required=True, help="JSON file with the stage fields")
    c = sub.add_parser("color", help="measure color-design or qa-color from real pixels")
    c.add_argument("stage", choices=sorted(COMPUTED)); c.add_argument("image", type=Path)
    c.add_argument("--job", type=Path, required=True)
    c.add_argument("--rule", choices=RULES); c.add_argument("--accent", help="override hex, e.g. #FF5A1F")
    c.add_argument("--hero-box", help="x,y,w,h fractions to measure only the hero area")
    a = sub.add_parser("analyze", help="palette + three accent suggestions, no job needed")
    a.add_argument("image", type=Path); a.add_argument("--emotion")
    a.add_argument("--hero-box")
    k = sub.add_parser("check", help="fail closed unless all seven stages passed in order")
    k.add_argument("--job", type=Path, required=True)
    sub.add_parser("stages", help="print the mandatory stages")
    o = sub.add_parser("core", help="run one mandatory core skill and keep a receipt")
    o.add_argument("core", choices=sorted(CORES)); o.add_argument("--job", type=Path, required=True)
    o.epilog = "Pass the program's own arguments after --"
    t = sub.add_parser("cores", help="list core skills per stage")
    t.add_argument("--stage", choices=STAGES)
    q = sub.add_parser("repos", help="rank the motion-graphics repositories for a task")
    q.add_argument("query"); q.add_argument("--limit", type=int, default=8)
    argv = list(sys.argv[1:] if argv is None else argv)
    extra: list[str] = []
    if "--" in argv:
        i = argv.index("--")
        argv, extra = argv[:i], argv[i + 1:]
    args = ap.parse_args(argv)
    try:
        if args.cmd == "start":
            out = start(args.task, args.job)
        elif args.cmd == "record":
            out = record(args.job, args.stage, json.loads(args.data.read_text(encoding="utf-8")))
        elif args.cmd == "color":
            out = color(args.job, args.stage, args.image, rule=args.rule, accent=args.accent,
                        box=_box(args.hero_box))
        elif args.cmd == "analyze":
            out = analyze(args.image, box=_box(args.hero_box), emotion=args.emotion)
        elif args.cmd == "core":
            out = run_core(args.job, args.core, extra)
        elif args.cmd == "cores":
            out = cores_table(args.stage)
        elif args.cmd == "repos":
            out = repos(args.query, limit=args.limit)
        elif args.cmd == "stages":
            out = {"stages": list(STAGES), "required": {k: list(v) for k, v in REQUIRED.items()},
                   "computed": sorted(COMPUTED),
                   "required_cores": {k: [list(g) for g in v] for k, v in REQUIRED_CORES.items()}}
        else:
            out = check(args.job)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        if args.cmd == "core":
            return 0 if out["exit"] == 0 else 6
        return 5 if args.cmd == "check" and not out["passed"] else 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError,
            subprocess.CalledProcessError) as exc:
        print("black-dragon-video-protocol: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
