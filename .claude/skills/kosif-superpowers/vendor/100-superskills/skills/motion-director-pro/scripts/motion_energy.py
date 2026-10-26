#!/usr/bin/env python3
"""يقيس طاقة الحركة إطاراً بإطار لفيلم (mp4) أو مجلد إطارات، ويقارنها بمرجع: المتوسط، والذروة، وحصة الإطارات فوق العتبة، وحصة شبه الساكنة، وأطول تجميد، وتوزيع الإضاءة والتشبّع.

usage:
  python motion_energy.py build.mp4 [--fps 15] [--ref reference.mp4] [--out motion-report.json]
  python motion_energy.py frames/ [--ref ref-frames/]
يحتاج ffmpeg (للفيديو) وPillow. «حركة» = متوسط الفرق المطلق بين إطارين متتاليين (0-255) على 320px عرضاً.
أرضية الفيلم مقابل المرجع: near_still ≤ المرجع · peak ≤ 1.3× ذروة المرجع · above_threshold ≥ المرجع.
الفرق عن motion بالتدرّجات: اختبار التجميد — يعاد القياس بعد تثبيت كل بكسل لا يتغير إلا بسلاسة (تدرّج) ليُكشف «المتر الذي يتحرك والفيلم ساكن».
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError:
    sys.exit("Pillow غير مثبت: pip install pillow")


def frames_from_video(path: Path, fps: int, tmp: Path):
    tmp.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale=320:-2", str(tmp / "f_%05d.png")], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr[-600:])
    return sorted(tmp.glob("f_*.png"))


def load_frames(src: str, fps: int, tmp: Path):
    p = Path(src)
    if p.is_dir():
        files = sorted(p.glob("*.png")) or sorted(p.glob("*.jpg"))
        out = []
        for f in files:
            im = Image.open(f).convert("RGB")
            out.append(im.resize((320, max(1, 320 * im.height // im.width))))
        return out, fps
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg غير موجود")
    return [Image.open(f).convert("RGB") for f in frames_from_video(p, fps, tmp)], fps


def measure(frames, fps):
    if len(frames) < 2:
        raise SystemExit("إطاران على الأقل")
    diffs, lum, sat = [], [], []
    prev = None
    for im in frames:
        g = im.convert("L"); st = ImageStat.Stat(g); lum.append(st.mean[0])
        hsv = im.convert("HSV"); sat.append(ImageStat.Stat(hsv.getchannel(1)).mean[0])
        if prev is not None:
            diffs.append(ImageStat.Stat(ImageChops.difference(g, prev)).mean[0])
        prev = g
    thr = 4.0
    mean = sum(diffs) / len(diffs); peak = max(diffs)
    above = sum(1 for d in diffs if d > thr) / len(diffs)
    still = sum(1 for d in diffs if d < 0.6) / len(diffs)
    best = cur = 0
    for d in diffs:
        cur = cur + 1 if d < 0.6 else 0; best = max(best, cur)
    hp = [abs(diffs[i] - diffs[i - 1]) for i in range(1, len(diffs))]
    hp_mean = sum(hp) / len(hp) if hp else 0
    return {"frames": len(frames), "fps": fps, "duration_s": round(len(frames) / fps, 2), "mean": round(mean, 3), "peak": round(peak, 2),
            "above_threshold_share": round(above, 3), "near_still_share": round(still, 3), "longest_still_s": round(best / fps, 2),
            "highpass_mean": round(hp_mean, 3), "luma_mean": round(sum(lum) / len(lum), 1), "luma_min": round(min(lum), 1), "luma_max": round(max(lum), 1),
            "sat_mean": round(sum(sat) / len(sat), 1), "per_second": [round(sum(diffs[i:i + fps]) / max(1, len(diffs[i:i + fps])), 2) for i in range(0, len(diffs), fps)]}


def verdict(m, r):
    issues = []
    if r:
        if m["near_still_share"] > r["near_still_share"] + 0.05:
            issues.append(f"شبه ساكن {m['near_still_share']:.0%} > المرجع {r['near_still_share']:.0%}: عرض شرائح متحركة لا فيلم؛ أضف جسماً في تحوّل في كل لحظة")
        if m["peak"] > 1.3 * r["peak"]:
            issues.append(f"ذروة {m['peak']} > 1.3× ذروة المرجع {r['peak']}: انتقالات ضخمة بين بطاقات ساكنة")
        if m["above_threshold_share"] < r["above_threshold_share"] - 0.05:
            issues.append(f"إطارات متحركة {m['above_threshold_share']:.0%} < المرجع {r['above_threshold_share']:.0%}")
        if abs(m["luma_mean"] - r["luma_mean"]) > 40:
            issues.append("إضاءة بعيدة عن المرجع: أرضية مختلفة")
    if m["longest_still_s"] >= 1.5:
        issues.append(f"تجميد {m['longest_still_s']}s: لا شيء يتحرك؛ حركة محيطية أو قصّ")
    if m["luma_max"] - m["luma_min"] > 150:
        issues.append("قفزة إضاءة كبيرة داخل الفيلم: فيلمان ملصوقان؛ أرضية واحدة وسقف للأفتح")
    if m["highpass_mean"] < 0.15 and m["mean"] > 1.0:
        issues.append("الحركة سلسة جداً (انجراف/تنفّس تدرّجات): قد لا تنجو من اختبار التجميد؛ أضف أحداثاً فيزيائية")
    return issues


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("--ref"); ap.add_argument("--fps", type=int, default=15); ap.add_argument("--out", default="motion-report.json")
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp(prefix="motion_"))
    try:
        frames, fps = load_frames(a.src, a.fps, tmp / "a"); m = measure(frames, fps)
        r = None
        if a.ref:
            rf, _ = load_frames(a.ref, a.fps, tmp / "b"); r = measure(rf, fps)
        issues = verdict(m, r)
        rep = {"build": m, "reference": r, "issues": issues, "verdict": "PASS" if not issues else "REVISE"}
        open(a.out, "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1))
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(json.dumps({"verdict": rep["verdict"], "issues": issues,
                          "build": {k: m[k] for k in ("mean", "peak", "above_threshold_share", "near_still_share", "longest_still_s", "luma_mean")}}, ensure_ascii=False, indent=1))
        sys.exit(0 if rep["verdict"] == "PASS" else 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
