#!/usr/bin/env python3
"""فحص آلي لإطارات الأنيميشن: إطارات سوداء/بيضاء، وإطارات متطابقة متتالية (تجمّد)، وقفزات حادة، وتوزيع الحركة.

usage: python qa.py --frames frames [--fps 30] [--out qa.json]
يحتاج Pillow. يخرج PASS أو REVISE مع قائمة المشكلات بأزمنتها؛ لا يحل مكان المراجعة البصرية للوحة التحقق.
"""
import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError:
    sys.exit("Pillow غير مثبت: pip install pillow")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", default="frames")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--out", default="")
    ap.add_argument("--freeze", type=float, default=1.5, help="ثوانٍ من التطابق تُعدّ تجمّداً")
    a = ap.parse_args()

    frames = sorted(Path(a.frames).glob("f_*.png"))
    if len(frames) < 2:
        sys.exit("أقل من إطارين")
    issues, diffs, prev = [], [], None
    dark, bright = [], []
    for i, p in enumerate(frames):
        src = Image.open(p)
        im = src.convert("L").resize((320, max(1, 320 * src.height // src.width)))
        mean = ImageStat.Stat(im).mean[0]
        if mean < 6:
            dark.append(i)
        if mean > 249:
            bright.append(i)
        if prev is not None:
            d = ImageStat.Stat(ImageChops.difference(im, prev)).mean[0]
            diffs.append(d)
        prev = im

    # freezes: runs of near-zero difference
    run_start = None
    for i, d in enumerate(diffs):
        if d < 0.05:
            run_start = i if run_start is None else run_start
        else:
            if run_start is not None and (i - run_start) >= a.freeze * a.fps:
                issues.append({"type": "freeze", "from_s": round(run_start / a.fps, 2), "to_s": round(i / a.fps, 2),
                               "hint": "لا شيء يتحرك؛ أضف حركة محيطية (تنفّس، انجراف) أو اقطع المدة"})
            run_start = None
    if run_start is not None and (len(diffs) - run_start) >= a.freeze * a.fps:
        issues.append({"type": "freeze", "from_s": round(run_start / a.fps, 2), "to_s": round(len(frames) / a.fps, 2),
                       "hint": "تجمّد حتى النهاية"})
    # hard jumps (cuts) — informational unless many
    jumps = [round((i + 1) / a.fps, 2) for i, d in enumerate(diffs) if d > 60]
    if len(jumps) > max(3, len(frames) / a.fps / 2):
        issues.append({"type": "too_many_cuts", "count": len(jumps), "hint": "قطعات صلبة كثيرة؛ هل هذا مقصود؟"})
    if dark:
        issues.append({"type": "black_frames", "seconds": [round(i / a.fps, 2) for i in dark[:10]], "count": len(dark),
                       "hint": "إطارات شبه سوداء؛ الخلفية الفارغة تُقرأ كـ«لم يُحمَّل»"})
    if bright:
        issues.append({"type": "white_frames", "seconds": [round(i / a.fps, 2) for i in bright[:10]], "count": len(bright)})
    motion = sum(diffs) / len(diffs)
    verdict = "PASS" if not [x for x in issues if x["type"] in ("freeze", "black_frames")] else "REVISE"
    report = {"verdict": verdict, "frames": len(frames), "duration_s": round(len(frames) / a.fps, 2),
              "mean_motion": round(motion, 2), "cuts_at_s": jumps[:20], "issues": issues}
    if a.out:
        Path(a.out).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(report, ensure_ascii=False))
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
