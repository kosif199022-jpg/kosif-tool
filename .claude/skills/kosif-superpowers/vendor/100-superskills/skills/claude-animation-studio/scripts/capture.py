#!/usr/bin/env python3
"""يصوّر مشهد HTML حتمياً إطاراً بإطار عبر Playwright: يستدعي window.render(t) لكل إطار ويحفظ PNG.

usage:
  python capture.py --html index.html [--w 1080 --h 1920] [--fps 30] [--dur 10] [--out frames]
  python capture.py --html index.html --only 0.5,3.2,7.9     # لقطات QA عند أزمنة محددة

عقد المشهد (templates/scene-2d.html يطبّقه):
  - window.render(t) يرسم الإطار عند الزمن t بالثواني ولا يقرأ ساعة الجهاز.
  - window.__ready === true بعد تحميل الخطوط والأصول.
  - الأبعاد تُؤخذ من <meta name="scene" content="w=1080;h=1920;fps=30;dur=10"> إن وُجدت ولم تُمرَّر.
يحتاج: pip install playwright، ثم Edge المثبت على ويندوز أو python -m playwright install chromium.
"""
import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sys.exit("playwright غير مثبت: pip install playwright && python -m playwright install chromium")


def scene_meta(html: Path) -> dict:
    m = re.search(r'<meta\s+name="scene"\s+content="([^"]+)"', html.read_text(encoding="utf-8", errors="ignore"))
    out = {}
    if m:
        for kv in m.group(1).split(";"):
            if "=" in kv:
                k, v = kv.split("=", 1)
                out[k.strip()] = float(v) if re.fullmatch(r"[\d.]+", v.strip()) else v.strip()
    return out


def launch(p):
    """Edge أولاً (موجود على ويندوز بلا تحميل)، ثم Chromium المثبت عبر Playwright."""
    args = ["--ignore-gpu-blocklist", "--use-angle=d3d11", "--enable-webgl", "--autoplay-policy=no-user-gesture-required"]
    for channel in ("msedge", "chrome", None):
        try:
            return p.chromium.launch(channel=channel, headless=True, args=args) if channel else p.chromium.launch(headless=True, args=args)
        except Exception:
            continue
    raise SystemExit("لا متصفح متاح: ثبّت Edge أو شغّل python -m playwright install chromium")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--w", type=int)
    ap.add_argument("--h", type=int)
    ap.add_argument("--fps", type=int)
    ap.add_argument("--dur", type=float)
    ap.add_argument("--out", default="frames")
    ap.add_argument("--only", default="", help="أزمنة مفصولة بفواصل للقطات QA فقط")
    ap.add_argument("--selector", default="", help="عنصر يُصوَّر بدل الصفحة كاملة (مثل #stage)")
    a = ap.parse_args()

    html = Path(a.html).resolve()
    meta = scene_meta(html)
    W = a.w or int(meta.get("w", 1920))
    H = a.h or int(meta.get("h", 1080))
    FPS = a.fps or int(meta.get("fps", 30))
    DUR = a.dur or float(meta.get("dur", 10))
    out = (html.parent / a.out) if not Path(a.out).is_absolute() else Path(a.out)
    if not a.only:
        shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)
    times = [float(x) for x in a.only.split(",") if x.strip()] if a.only else [i / FPS for i in range(int(round(DUR * FPS)))]

    errors, t0 = [], time.time()
    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        page.goto(html.as_uri() + "?capture=1")
        try:
            page.wait_for_function("window.__ready === true", timeout=120000)
        except Exception:
            errors.append("window.__ready لم يصبح true خلال 120 ثانية؛ تأكد أن المشهد يضبطه بعد تحميل الخطوط")
        try:
            page.evaluate("document.fonts && document.fonts.ready")
        except Exception:
            pass
        target = page.locator(a.selector) if a.selector else None
        for i, t in enumerate(times):
            page.evaluate(f"window.render({t})")
            name = f"t_{t:06.2f}.png" if a.only else f"f_{i:04d}.png"
            if target is not None:
                target.screenshot(path=str(out / name))
            else:
                page.screenshot(path=str(out / name), clip={"x": 0, "y": 0, "width": W, "height": H})
        browser.close()
    report = {"frames": len(times), "w": W, "h": H, "fps": FPS, "dur": DUR, "out": str(out),
              "seconds": round(time.time() - t0, 1), "errors": errors[:10]}
    (out.parent / "capture.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace") if hasattr(sys.stdout, "reconfigure") else None
    print(json.dumps(report, ensure_ascii=False))
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
