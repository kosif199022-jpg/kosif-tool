#!/usr/bin/env python3
"""ينشئ مجلد مشروع أنيميشن جديد من القالب: index.html (2D أو 3D) + DESIGN.md + STORYBOARD.md + run.md.

usage:
  python new_scene.py --name my-anim --title "عنوان" --ratio 9:16 --dur 12 [--fps 30] [--kind 2d|3d] [--dir .]
النسب: 9:16 → 1080×1920، 16:9 → 1920×1080، 1:1 → 1080×1080، 4:5 → 1080×1350.
"""
import argparse
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE.parent / "templates"
SIZES = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}

DESIGN = """# DESIGN: «{title}»

## Style Prompt
(جملة أو جملتان: المزاج، الكثافة، الحقبة، المرجع البصري. مثال: مسطّح دافئ بخلفية حية وحركة هادئة متصلة.)

## Colors (3–5 ألوان لها أدوار؛ لا #333 ولا #3b82f6)
| الدور | اللون |
|---|---|
| الخلفية | `#0F1A2B` |
| النص الرئيسي | `#F4F7FF` |
| التمييز | `#F6C76B` |
| ثانوي | `#2B86E0` |

## Typography
- عربي: Cairo (800 للعناوين، 600 للنص). لاتيني: Fraunces أو Space Grotesk. لا Inter/Roboto/Poppins.
- أحجام الفيديو: عناوين 72px+، نص 40px+ على 1080p.

## Motion
- دخول: power3.out / spring. خروج: power2.in وأسرع من الدخول. انتقال بين المواضع: inOut.
- كل مشهد: بناء 30% ← تنفّس 40% (حركة محيطية واحدة) ← حسم 30%.
- أول حركة تبدأ عند 0.15 ثانية لا عند الصفر.

## What NOT to Do
- لا تدخل كل العناصر من نفس الاتجاه وبنفس السرعة.
- لا خلفية صمّاء: طبقة حية (توهج، حبيبات، خطوط) دائماً.
- لا نص أصغر من 40px ولا أكثر من سطرين في الظهور الواحد.
- لا معلومات غير مؤكدة على الشاشة.
"""

STORY = """# STORYBOARD: «{title}» ({dur} ثانية، {ratio})

| البند | القيمة |
|---|---|
| المنصة | |
| المقاس | {w}×{h} |
| الإطارات | {fps} fps ({frames} إطاراً) |
| الهدف | |
| الجمهور | |
| الخطّاف (أول 1.5 ث) | |
| النداء الختامي | |

## الإيقاعات
| # | الوقت | الإيقاع | ما يظهر | الحركة | التعليق الصوتي |
|---|---|---|---|---|---|
| 1 | 0.0 – 1.5 | الخطّاف | | | |
| 2 | 1.5 – | | | | |
| 3 | | | | | |
| N | – {dur} | الختام | | | |

- الكاميرا:
- الصوت:
"""

RUN = """# تشغيل «{name}»

```bash
python "{scripts}/capture.py" --html index.html
python "{scripts}/encode.py" --frames frames --fps {fps} --out {name}.mp4 --gif preview.gif
python "{scripts}/qa.py" --frames frames --fps {fps} --out qa.json
```
افتح index.html في المتصفح للمعاينة الحية (يعيد التشغيل تلقائياً؛ النقر يوقف). راجع contact-sheet.png قبل التسليم.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--ratio", default="9:16", choices=SIZES.keys())
    ap.add_argument("--dur", type=float, default=10)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--kind", default="2d", choices=("2d", "3d"))
    ap.add_argument("--dir", default=".")
    a = ap.parse_args()
    w, h = SIZES[a.ratio]
    name = re.sub(r"[^\w\-]+", "-", a.name).strip("-")
    title = a.title or a.name
    d = Path(a.dir) / name
    d.mkdir(parents=True, exist_ok=True)
    tpl = (TPL / f"scene-{a.kind}.html").read_text(encoding="utf-8")
    html = (tpl.replace("{{TITLE}}", title).replace("{{W}}", str(w)).replace("{{H}}", str(h))
            .replace("{{FPS}}", str(a.fps)).replace("{{DUR}}", str(a.dur)))
    (d / "index.html").write_text(html, encoding="utf-8")
    (d / "DESIGN.md").write_text(DESIGN.format(title=title), encoding="utf-8")
    (d / "STORYBOARD.md").write_text(STORY.format(title=title, dur=a.dur, ratio=a.ratio, w=w, h=h, fps=a.fps,
                                                  frames=int(a.dur * a.fps)), encoding="utf-8")
    (d / "run.md").write_text(RUN.format(name=name, scripts=HERE.as_posix(), fps=a.fps), encoding="utf-8")
    print(f"created {d} ({w}x{h}, {a.fps} fps, {a.dur}s, {a.kind})")


if __name__ == "__main__":
    main()
