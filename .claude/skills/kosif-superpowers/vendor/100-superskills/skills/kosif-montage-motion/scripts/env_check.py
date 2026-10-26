"""What can this machine do? Run first, then pick the route the report names.

    python scripts/env_check.py            JSON + a short Arabic summary

Checks: Python libraries, FFmpeg (or the imageio-ffmpeg wheel), a Chromium-family browser or Playwright's own Chromium
(frame capture), Node/npm (bundling, HyperFrames), faster-whisper and cached models (transcription), the OS (Windows
voices, Direct3D GPU). Routes:
  A  full studio   — browser capture + FFmpeg: render MP4 films (2D, 3D, canvas), montage, reel, decaption, QA.
  B  footage only  — FFmpeg but no browser: montage, grade, captions, decaption, reel (if whisper), QA; films as HTML.
  C  preview only  — no FFmpeg: write the composition HTML (it plays itself with a play bar), score/WAV, references.
"""
from __future__ import annotations

import importlib
import json
import os
import platform
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent))                          # html_render sits one level up in the studio layout


def _mod(name: str) -> bool:
    try:
        importlib.import_module(name)
        return True
    except Exception:
        return False


def ffmpeg_path() -> str | None:
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def browser() -> str | None:
    try:
        import html_render
        b = html_render.browser_path()
        return b or ("playwright-chromium" if _mod("playwright") else None)
    except Exception:
        return None


def whisper_models() -> list[str]:
    hub = Path.home() / ".cache" / "huggingface" / "hub"
    return sorted(p.name.replace("models--Systran--faster-whisper-", "") for p in hub.glob("models--Systran--faster-whisper-*")) if hub.exists() else []


def _ff_filter(ff: str, name: str) -> bool:
    import re
    import subprocess
    try:
        r = subprocess.run([ff, "-hide_banner", "-filters"], capture_output=True, text=True, timeout=30)
        return bool(re.search(rf"\s{name}\s", r.stdout))
    except Exception:
        return False


def _arabic_font() -> str | None:
    try:
        import tools
        p = tools.font_path(True)
        return str(p) if p else None
    except Exception:
        return None


def check() -> dict:
    libs = {m: _mod(m) for m in ("numpy", "PIL", "cv2", "scipy", "playwright", "faster_whisper", "whisper", "arabic_reshaper", "bidi")}
    ff = ffmpeg_path()
    br = browser() if libs["playwright"] or os.name == "nt" else browser()
    node = shutil.which("node")
    rep = {
        "os": platform.system(), "python": platform.python_version(), "libs": libs, "ffmpeg": ff, "browser": br,
        "node": node, "npm_kit": (HERE / "node_modules" / "three").exists(), "k3_bundle": (HERE / "kit" / "three-kit.bundle.js").exists(),
        "whisper_models": whisper_models(), "windows_voices": platform.system() == "Windows",
        "cpus": os.cpu_count() or 1, "render_workers": min(4, os.cpu_count() or 1),
        "vidstab": _ff_filter(ff, "vidstabdetect") if ff else False, "arabic_font": _arabic_font(),
    }
    can_render = bool(ff and br and libs["playwright"] and libs["numpy"] and libs["PIL"])
    rep["route"] = "A" if can_render else ("B" if ff and libs["numpy"] and libs["cv2"] else "C")
    try:                                                      # v6: which face detector, how many xfade transitions, a Tk window
        import faces
        rep["face_detector"] = faces.which()
    except Exception:
        rep["face_detector"] = None
    try:
        import timeline
        rep["xfade_transitions"] = len(timeline.transitions()) if ff else 0
    except Exception:
        rep["xfade_transitions"] = 0
    rep["tk"] = _mod("tkinter")
    rep["can"] = {
        "timeline_transitions": bool(ff and libs["PIL"]),
        "scenes": bool(ff),
        "privacy_faces": bool(ff and libs["numpy"] and libs["scipy"]),
        "motion_templates": can_render,
        "tk_window": rep["tk"],
        "render_films": can_render,
        "montage_grade_captions": bool(ff),
        "decaption": bool(ff and libs["cv2"] and libs["numpy"]),
        "transcribe": libs["faster_whisper"] or libs["whisper"],
        "reel": bool(ff and libs["cv2"] and (libs["faster_whisper"] or libs["whisper"])),
        "reel_with_transcript": bool(ff and libs["cv2"] and libs["numpy"]),
        "direct_edit": bool(ff and libs["cv2"]),         # an auto-directed edit; words from whisper or a supplied .words.json
        "silence_aspect_export_loop": bool(ff),
        "stabilize_vidstab": bool(ff) and rep["vidstab"],
        "score_wav": libs["numpy"],
        "voice_arabic_offline": rep["windows_voices"],
        "preview_html": True,
    }
    return rep


def main():
    r = check()
    print(json.dumps(r, ensure_ascii=False, indent=1))
    names = {"A": "A — استوديو كامل: تصيير أفلام MP4 ومونتاج وفحص", "B": "B — فيديو حقيقي فقط: مونتاج وتلوين وترجمة وإزالة ترجمة؛ الأفلام كـ HTML",
             "C": "C — معاينة فقط: تركيب HTML يشتغل بزر تشغيل + موسيقى WAV"}
    print("\nالمسار المتاح هنا:", names[r["route"]])
    missing = [k for k, v in r["can"].items() if not v]
    if missing:
        print("غير متاح:", "، ".join(missing))
    print(f"التصيير المتوازي: {r['render_workers']} متصفح(ات) · خط عربي: {r['arabic_font'] or 'لا يوجد — ثبّت Noto Naskh Arabic أو Cairo'}")


if __name__ == "__main__":
    main()
