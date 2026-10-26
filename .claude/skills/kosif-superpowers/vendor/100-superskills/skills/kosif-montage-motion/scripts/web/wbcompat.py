"""The KOSIF Motion Workbench contract, in Python: the deterministic planner (kosif.proplan.v1), its validator, the
compiler to kosif.motion.manifest.v1 + a self-contained 2D composition (window.render(t)), and the Pillow frame
renderer of the Python render service — ported from site/lib/motion.ts and python-render-service/service.py of the
v3 source package so the local site answers exactly like the hosted one, then goes further.

Differences from the hosted service, on purpose: Arabic is shaped by RAQM when Pillow has it, else by
arabic_reshaper + python-bidi; the font is the first Arabic-capable font on this machine; the local limits are wider
(see LIMITS) because nothing leaves this PC.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
sys.path.insert(0, str(SCRIPTS))

FPS = [24, 25, 30, 50, 60]
ASPECTS = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080), "4:5": (1080, 1350)}
TEMPLATES = [
    {"id": "kinetic", "name": "حروف وحركة", "description": "مشاهد ثنائية الأبعاد قابلة للتصدير كـ HTML", "task": "مقدمة عربية أنيقة عن قوة الأفكار مع حركة نصوص وأشكال هندسية", "color": "#a7e8d0"},
    {"id": "cinematic", "name": "لقطة سينمائية", "description": "خطة كاميرا وإضاءة تُنفذ بمحرك 3D المحلي", "task": "مشهد 3D سينمائي لمنتج زجاجي بإضاءة هادئة وحركة كاميرا متصلة", "color": "#d3c0fa"},
    {"id": "montage", "name": "مونتاج بإيقاع", "description": "تخطيط لقطات للمادة الأصلية دون رفعها", "task": "مونتاج فيديو قصير يحافظ على المصدر ويوازن بين التفاصيل واللقطات الواسعة", "color": "#f5ce91"},
]
CAMERAS = ["fast_reveal", "slow_push", "match_cut", "focus_lift", "still_hold", "locked", "dolly_in", "orbit", "side_track", "push_in"]
# local render limits (the hosted demo: 1–30 s, ≤ 1280 px, 24/25/30 fps, 50 scenes)
LIMITS = {"min_seconds": 1, "max_seconds": 600, "max_px": 1920, "fps": [24, 25, 30, 50, 60], "max_scenes": 200, "max_bytes": 2 * 1024 ** 3}


class PlanError(ValueError):
    pass


def make_plan(x: dict) -> dict:
    task = str(x.get("task", "") or "").strip()
    seconds = x.get("seconds", 12); fps = x.get("fps", 30); aspect = x.get("aspect", "16:9"); mode = x.get("mode", "pro")
    if not task or len(task) > 5000:
        raise PlanError("اكتب وصفًا من 1 إلى 5000 حرف.")
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or seconds < 2 or seconds > 600:
        raise PlanError("المدة من 2 إلى 600 ثانية.")
    if isinstance(fps, bool) or not isinstance(fps, (int, float)) or fps not in FPS:
        raise PlanError("معدل الإطارات غير مدعوم.")
    if str(aspect) not in ASPECTS:
        raise PlanError("نسبة الأبعاد غير مدعومة.")
    if str(mode) not in ("standard", "pro"):
        raise PlanError("الوضع غير مدعوم.")
    if re.search(r"structural|finite element|truss|أحمال|إجهاد|الانهيار", task, re.I):
        raise PlanError("المحاكاة الإنشائية خارج نطاق الموقع. استخدم الأدوات المتخصصة مع مراجعة هندسية.")
    if re.search(r"برومبت|prompt|veo|sora|kling", task, re.I):
        intent = "prompt"
    elif re.search(r"مونتاج|تعديل فيديو|video edit|caption|subtitle|ريل", task, re.I):
        intent = "footage_edit"
    elif re.search(r"ثلاثي|3d|three\.js|c4d", task, re.I):
        intent = "3d_motion"
    else:
        intent = "2d_motion"
    fps = int(fps)
    total = round(seconds * fps)
    cuts = [round(total * r) for r in (0, .12, .36, .62, .84, 1)]
    beats = ["hook", "setup", "contrast", "payoff", "end_card"]
    cams = ["dolly_in", "orbit", "side_track", "push_in", "locked"] if intent == "3d_motion" else ["fast_reveal", "slow_push", "match_cut", "focus_lift", "still_hold"]
    shots = [{"beat": b, "start_frame": cuts[i], "end_frame_exclusive": cuts[i + 1], "start_s": cuts[i] / fps, "end_s": cuts[i + 1] / fps, "camera_move": cams[i],
              "asset_source": "user_media" if intent == "footage_edit" else "local_generated", "audio_intent": "impact" if i in (0, 3) else "underscore",
              "text_policy": "Arabic shaping, RTL, safe margins; verify font and readability"} for i, b in enumerate(beats)]
    commands = [] if intent == "prompt" else (["montage", "inspect", "sheet"] if intent == "footage_edit" else ["new", "frames", "render", "inspect", "sheet"])
    return {"schema": "kosif.proplan.v1", "version": "1.1.0-site", "request_summary": task, "mode": str(mode), "intent": intent, "route": "remote_planning_only",
            "full_pro_status": "NOT_FULL_PRO", "timeline": {"fps": fps, "seconds": total / fps, "total_frames": total, "aspect": str(aspect), "shots": shots},
            "available_commands": commands, "stages": ["brief", "shot_plan", "storyboard", "timeline", "local_execution", "visual_quality_review"],
            "gates": {"source_permission": "required", "actual_render_required_for_claim": True, "arabic_text_review": True},
            "limitations": ["تخطيط حتمي بقواعد ثابتة، وليس توليد فيديو بالذكاء الاصطناعي.",
                            "رندر MP4 الخادمي متاح لمشاهد 2D فقط بعد ربط محرك Python؛ 3D ومعالجة الوسائط تحتاج محركًا إضافيًا.",
                            "لا يتم رفع الوسائط الأصلية أو حفظ المشاريع على الخادم."],
            "side_effects_performed": False}


def validate_plan(p) -> dict:
    errors: list[str] = []
    warnings = ["يجب مراجعة الحقوق والخطوط والصوت والإطارات فعليًا قبل اعتماد الفيديو."]
    if not isinstance(p, dict):
        return {"valid": False, "errors": ["الخطة يجب أن تكون كائن JSON."], "warnings": warnings, "summary": None}
    t = p.get("timeline") if isinstance(p.get("timeline"), dict) else None
    if p.get("schema") != "kosif.proplan.v1":
        errors.append("schema غير مدعوم.")
    rs = p.get("request_summary")
    if not isinstance(rs, str) or not rs.strip() or len(rs) > 5000:
        errors.append("وصف الخطة غير صالح.")
    if p.get("intent") not in ("2d_motion", "3d_motion", "footage_edit", "prompt"):
        errors.append("نوع المهمة غير مدعوم.")
    def num(v):
        return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
    if (not t or t.get("fps") not in FPS or not num(t.get("seconds")) or t["seconds"] < 2 or t["seconds"] > 600 or not isinstance(t.get("total_frames"), int)
            or isinstance(t.get("total_frames"), bool) or abs(t["total_frames"] - t["seconds"] * t["fps"]) > .01 or t.get("aspect") not in ASPECTS):
        errors.append("إعدادات الخط الزمني غير صالحة.")
    shots = t.get("shots") if t else None
    if not isinstance(shots, list) or not (1 <= len(shots) <= 100):
        errors.append("عدد اللقطات من 1 إلى 100.")
    else:
        end = 0
        for i, s in enumerate(shots):
            ok = isinstance(s, dict) and isinstance(s.get("start_frame"), int) and isinstance(s.get("end_frame_exclusive"), int) and s["start_frame"] == end and s["end_frame_exclusive"] > s["start_frame"]
            if not ok:
                errors.append(f"تداخل أو فجوة أو مدة غير صالحة في اللقطة {i + 1}.")
            for k in ("beat", "camera_move"):
                if not isinstance(s, dict) or not isinstance(s.get(k), str) or len(s[k]) > 150:
                    errors.append(f"حقل {k} غير صالح.")
            end = s.get("end_frame_exclusive") if isinstance(s, dict) else None
        if t and end != t.get("total_frames"):
            errors.append("اللقطات لا تغطي طول المشروع بالكامل.")
    if p.get("intent") != "2d_motion":
        warnings.append("معاينة الموقع مخطط مبسط. التنفيذ الفعلي لهذا النوع يتم في المحرك المحلي.")
    summary = {"shots": len(shots) if isinstance(shots, list) else 0, "frames": t.get("total_frames"), "seconds": t.get("seconds"), "fps": t.get("fps"), "aspect": t.get("aspect")} if t else None
    return {"valid": not errors, "errors": errors, "warnings": warnings, "summary": summary}


PLAYER_JS = (HERE / "static" / "manifest-player.js")


def project_html(m: dict) -> str:
    """A self-contained composition: a canvas, the manifest as data, window.render(t) + window.__ready — the same
    contract the hosted site exports and the one the local renderer (kmotion render) understands."""
    data = json.dumps(m, ensure_ascii=False).replace("<", "\\u003c")
    draw = PLAYER_JS.read_text(encoding="utf-8")
    return ("<!doctype html><html lang=\"ar\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>KOSIF Motion composition</title><style>html,body{margin:0;background:#11171b;width:100%;height:100%;overflow:hidden}"
            "canvas{display:block;width:100%;height:100%;object-fit:contain}</style></head>"
            f"<body data-composition-id=\"kosif-site\" data-width=\"{m['width']}\" data-height=\"{m['height']}\" data-duration=\"{m['duration']}\" data-fps=\"{m['fps']}\">"
            f"<canvas id=\"frame\"></canvas><script>const manifest={data};{draw}\nwindow.__duration=manifest.duration;"
            "window.render=function(t){drawFrame(document.getElementById('frame'),manifest,t);window.__ready=true;};window.render(0);window.__ready=true;</script></body></html>")


def compile_plan(p: dict) -> dict:
    v = validate_plan(p)
    if not v["valid"]:
        raise PlanError(" ".join(v["errors"]))
    width, height = ASPECTS[p["timeline"]["aspect"]]
    names = ["فكرة تبدأ", "تفاصيل تتضح", "من زاوية أخرى", "لحظة الأثر", "المشهد التالي"]
    manifest = {"schema": "kosif.motion.manifest.v1", "title": p["request_summary"], "width": width, "height": height, "fps": p["timeline"]["fps"],
                "duration": p["timeline"]["seconds"],
                "scenes": [{"id": f"shot-{i + 1}", "start_frame": s["start_frame"], "end_frame_exclusive": s["end_frame_exclusive"], "title": names[i % 5],
                            "subtitle": p["request_summary"][:85], "camera": s["camera_move"], "accent": ["#a7e8d0", "#d3c0fa", "#f5ce91"][i % 3]}
                           for i, s in enumerate(p["timeline"]["shots"])]}
    two_d = p["intent"] == "2d_motion"
    return {"manifest": manifest, "project_html": project_html(manifest) if two_d else None,
            "handoff": {"execution": "local_only", "commands": [["python", "scripts/motion.py", "render", "PROJECT_DIRECTORY"]] if two_d else [],
                        "note": "راجع اسم نقطة دخول المحرك ومتطلبات البيئة قبل تشغيل الأوامر؛ الموقع لا ينفذها."},
            "warnings": v["warnings"]}


# ───────────────────────── manifest validation (the render service's model) ─────────────────────────
def validate_manifest(m) -> dict:
    """The service's strict model (extra keys forbidden, even sizes, whole frames, gapless scenes) with the local LIMITS.
    Returns the normalised manifest; raises ValueError with one message."""
    if not isinstance(m, dict):
        raise ValueError("manifest must be an object")
    allowed = {"schema", "title", "width", "height", "fps", "duration", "scenes"}
    extra = set(m) - allowed
    if extra:
        raise ValueError(f"unsupported manifest keys: {', '.join(sorted(extra))}")
    if m.get("schema") != "kosif.motion.manifest.v1":
        raise ValueError("schema must be kosif.motion.manifest.v1")
    title = m.get("title")
    if not isinstance(title, str) or not (1 <= len(title) <= 5000):
        raise ValueError("title 1–5000 chars")
    w, h, fps, dur = m.get("width"), m.get("height"), m.get("fps"), m.get("duration")
    for v, name in ((w, "width"), (h, "height")):
        if not isinstance(v, int) or isinstance(v, bool) or not (128 <= v <= LIMITS["max_px"]) or v % 2:
            raise ValueError(f"{name}: even integer 128–{LIMITS['max_px']}")
    if isinstance(fps, bool) or fps not in LIMITS["fps"]:
        raise ValueError(f"fps one of {LIMITS['fps']}")
    if isinstance(dur, bool) or not isinstance(dur, (int, float)) or not math.isfinite(dur) or not (LIMITS["min_seconds"] <= dur <= LIMITS["max_seconds"]):
        raise ValueError(f"duration {LIMITS['min_seconds']}–{LIMITS['max_seconds']} s")
    frames = round(dur * fps)
    if abs(frames - dur * fps) > 0.001:
        raise ValueError("whole frames required")
    scenes = m.get("scenes")
    if not isinstance(scenes, list) or not (1 <= len(scenes) <= LIMITS["max_scenes"]):
        raise ValueError(f"scenes 1–{LIMITS['max_scenes']}")
    end, ids = 0, set()
    s_allowed = {"id", "start_frame", "end_frame_exclusive", "title", "subtitle", "camera", "accent"}
    for s in scenes:
        if not isinstance(s, dict) or set(s) - s_allowed or s_allowed - set(s):
            raise ValueError("scene fields: id, start_frame, end_frame_exclusive, title, subtitle, camera, accent")
        if not isinstance(s["id"], str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", s["id"]) or s["id"] in ids:
            raise ValueError("scene id: unique, [A-Za-z0-9_-]{1,64}")
        for k in ("start_frame", "end_frame_exclusive"):
            if not isinstance(s[k], int) or isinstance(s[k], bool) or s[k] < 0:
                raise ValueError(f"scene {k} must be a non-negative integer")
        if s["start_frame"] != end or s["end_frame_exclusive"] <= end:
            raise ValueError("Scenes must cover timeline without gaps or overlaps")
        if not isinstance(s["title"], str) or len(s["title"]) > 120 or not isinstance(s["subtitle"], str) or len(s["subtitle"]) > 300:
            raise ValueError("title ≤ 120, subtitle ≤ 300 chars")
        if s["camera"] not in CAMERAS:
            raise ValueError(f"camera one of {CAMERAS}")
        if not isinstance(s["accent"], str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", s["accent"]):
            raise ValueError("accent #rrggbb")
        ids.add(s["id"]); end = s["end_frame_exclusive"]
    if end != frames:
        raise ValueError("Scene coverage must match duration")
    out = dict(m); out["frames"] = frames
    return out


# ───────────────────────── the Pillow frame (the render service's picture) ─────────────────────────
_FONT_CACHE: dict = {}
_SHAPE = None


def _font(size: int):
    from PIL import ImageFont, features
    import tools
    key = max(9, int(size))
    if key not in _FONT_CACHE:
        p = tools.font_path(arabic=True)
        if p is None:
            _FONT_CACHE[key] = ImageFont.load_default(key)
        elif features.check("raqm"):
            _FONT_CACHE[key] = ImageFont.truetype(str(p), key, layout_engine=ImageFont.Layout.RAQM)
        else:
            _FONT_CACHE[key] = ImageFont.truetype(str(p), key)
    return _FONT_CACHE[key]


def shape(text: str) -> str:
    """Arabic joined and ordered for Pillow when RAQM is absent (RAQM shapes by itself)."""
    global _SHAPE
    from PIL import features
    if features.check("raqm") or not re.search(r"[؀-ۿ]", text):
        return text
    if _SHAPE is None:
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            _SHAPE = lambda s: get_display(arabic_reshaper.reshape(s))  # noqa: E731
        except ImportError:
            _SHAPE = lambda s: s  # noqa: E731
    return _SHAPE(text)


def frame(m: dict, index: int):
    """One frame of a validated manifest as a PIL RGB image — the service's composition: dim accent gradient, grid,
    three breathing ellipses, the accent dot, title/subtitle (shaped Arabic), the KOSIF mark and the progress bar."""
    from PIL import Image, ImageDraw
    scene = next(s for s in m["scenes"] if s["start_frame"] <= index < s["end_frame_exclusive"])
    w, h, fps, frames = m["width"], m["height"], m["fps"], m["frames"]
    unit = min(w, h)
    image = Image.new("RGB", (w, h), "#11171b"); draw = ImageDraw.Draw(image)
    accent = tuple(bytes.fromhex(scene["accent"][1:])); dim = tuple(int(c * .14 + 17 * .86) for c in accent)
    step = max(1, h // 60)
    for y in range(0, h, step):
        q = max(0, 1 - y / h); color = tuple(int(v * q + 17 * (1 - q)) for v in dim)
        draw.rectangle((0, y, w, y + step), fill=color)
    spacing = max(8, int(unit / 12))
    for x in range(0, w, spacing):
        draw.line((x, 0, x, h), fill="#202a2d")
    for y in range(0, h, spacing):
        draw.line((0, y, w, y), fill="#202a2d")
    u = (index - scene["start_frame"]) / max(1, scene["end_frame_exclusive"] - scene["start_frame"])
    ease = 1 - (1 - min(1, u * 4)) ** 3
    for k in range(3):
        r = unit * (.17 + k * .045) * (.7 + .3 * ease); cx = w * .5 + math.sin(index / fps * .4) * unit * .025; cy = h * .4
        draw.ellipse((cx - r, cy - r * .72, cx + r, cy + r * .72), outline=tuple(int(c * (.3 + k * .2)) for c in accent), width=max(1, int(unit * .003)))
    r = unit * .026; draw.ellipse((w * .5 - r, h * .4 - r, w * .5 + r, h * .4 + r), fill=accent)

    def textfit(text, y, size, color):
        text = shape(text)
        font = _font(size)
        while draw.textlength(text, font=font) > w * .84 and font.size > 9:
            font = _font(font.size - 1)
        while text and draw.textlength(text, font=font) > w * .84:
            text = text[:-1]
        draw.text((w * .5, y), text, font=font, anchor="mm", fill=color)
    textfit(scene["title"], h * .67 + (1 - ease) * unit * .05, unit * .066, "#f2f4f3")
    textfit(scene["subtitle"], h * .77, unit * .03, "#bbc7c9")
    draw.text((w * .07, h * .07), "KOSIF / MOTION", font=_font(max(10, int(unit * .025))), fill=accent)
    draw.rectangle((0, h - max(2, int(unit * .006)), w * (index + 1) / frames, h), fill=accent)
    return image


def render_manifest(m: dict, out: Path, progress=None, cancelled=None, preset: str = "veryfast", crf: int = 20) -> dict:
    """Frames → FFmpeg (rawvideo pipe) → silent H.264 MP4, then an FFprobe verification exactly like the service's."""
    import shutil
    import subprocess
    ff = shutil.which("ffmpeg") or "ffmpeg"; fp = shutil.which("ffprobe") or "ffprobe"
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ff, "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{m['width']}x{m['height']}",
           "-framerate", str(m["fps"]), "-i", "pipe:0", "-an", "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for i in range(m["frames"]):
            if cancelled and cancelled():
                raise InterruptedError("cancelled")
            p.stdin.write(frame(m, i).tobytes())
            if progress:
                progress(round((i + 1) / m["frames"] * .95, 3))
        p.stdin.close(); p.wait()
        if p.returncode != 0:
            raise RuntimeError("encoding incomplete")
    except BaseException:
        try:
            p.stdin.close()
        except Exception:  # noqa: BLE001
            pass
        p.kill(); p.wait()
        out.unlink(missing_ok=True)
        raise
    info = json.loads(subprocess.check_output([fp, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(out)]))
    streams = info["streams"]; s = streams[0]
    if (len(streams) != 1 or s["codec_type"] != "video" or s["codec_name"] != "h264" or s["width"] != m["width"] or s["height"] != m["height"]
            or int(s.get("nb_frames", 0)) != m["frames"] or abs(float(info["format"]["duration"]) - m["duration"]) > 1 / m["fps"]):
        raise RuntimeError("verification mismatch")
    from PIL import features
    return {"width": m["width"], "height": m["height"], "fps": m["fps"], "duration": m["duration"], "frames": m["frames"], "bytes": out.stat().st_size,
            "mime_type": "video/mp4", "audio": False, "font": "RAQM shaping" if features.check("raqm") else "arabic_reshaper + bidi shaping"}
