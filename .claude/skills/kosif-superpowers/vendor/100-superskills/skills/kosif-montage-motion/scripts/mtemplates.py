"""KOSIF motion templates — ready-made Arabic-first motion-graphic compositions, filled from the command line and
rendered by the same engine as any project (frames → preview → render --engine studio).

    python mtemplates.py list
    python mtemplates.py new NAME --template title-card --set title="عنوان" sub="سطر ثانٍ" accent="#E7B65A" [--seconds 6] [--size 1080x1920] [--fps 30]
    python mtemplates.py show title-card                      the template's parameters and defaults

Templates (templates/motion/*.html): title-card · lower-third · stat-counter · quote-card · logo-reveal · countdown ·
end-card · bullet-list. Each is a HyperFrames composition on the motion kit (word masks, springs, pen strokes, camera)
with no wall clock and no randomness, so a render is reproducible. The project remembers its parameters in
template.json; edit index.html freely afterwards.
"""
from __future__ import annotations

import argparse
import html as _html
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

import motion  # noqa: E402

TDIR = next((p for p in (HERE / "templates" / "motion", HERE.parent / "templates" / "motion") if p.exists()), HERE.parent / "templates" / "motion")
FONTS = HERE / "kit" / "fonts"

# name → (Arabic label, default seconds, params: key → (default, Arabic hint))
TEMPLATES: dict[str, dict] = {
    "title-card": {"ar": "بطاقة عنوان: عنوان كبير بأقنعة كلمات + سطر ثانٍ + خط مرسوم + دفعة كاميرا", "seconds": 6,
                   "params": {"title": ("عنوان الفيلم", "العنوان"), "sub": ("سطر تعريفي قصير", "السطر الثاني"), "accent": ("#E7B65A", "لون التمييز"),
                              "bg1": ("#1b2a49", "لون الخلفية العلوي"), "bg2": ("#0d1b2a", "لون الخلفية السفلي")}},
    "lower-third": {"ar": "شريط اسم ووظيفة في المنطقة الآمنة السفلية (عربي آمن)", "seconds": 6,
                    "params": {"title": ("اسم المتحدث", "الاسم"), "sub": ("الوظيفة أو الصفة", "الوصف"), "accent": ("#E7B65A", "لون الشريط"),
                               "bg1": ("#22313f", "لون الخلفية العلوي"), "bg2": ("#0b141c", "لون الخلفية السفلي")}},
    "stat-counter": {"ar": "رقم يعدّ تصاعدياً مع حلقة تُرسم وتسمية", "seconds": 6,
                     "params": {"value": ("1250", "القيمة النهائية"), "label": ("عميل يثق بنا", "التسمية"), "prefix": ("", "قبل الرقم"), "suffix": ("+", "بعد الرقم"),
                                "decimals": ("0", "المنازل العشرية"), "accent": ("#5BD1A5", "لون التمييز"), "bg1": ("#10233a", "لون الخلفية العلوي"), "bg2": ("#071321", "لون الخلفية السفلي")}},
    "quote-card": {"ar": "اقتباس يصعد سطراً سطراً مع اسم القائل", "seconds": 7,
                   "params": {"quote": ("ما نراه اليوم|هو ما اخترناه بالأمس", "الاقتباس (افصل الأسطر بـ |)"), "author": ("حكمة", "القائل"), "accent": ("#F2C879", "لون التمييز"),
                              "bg1": ("#2b1e3a", "لون الخلفية العلوي"), "bg2": ("#120a1e", "لون الخلفية السفلي")}},
    "logo-reveal": {"ar": "شعار يُرسم بالقلم ثم يمتلئ ويظهر الاسم والشعار النصي", "seconds": 6,
                    "params": {"name": ("KOSIF", "الاسم"), "tagline": ("حركة لها معنى", "الشعار النصي"), "accent": ("#E7B65A", "لون التمييز"),
                               "path": ("M 60 20 L 100 44 L 100 92 L 60 116 L 20 92 L 20 44 Z M 60 44 L 78 55 L 78 81 L 60 92 L 42 81 L 42 55 Z", "مسار SVG للشعار (viewBox 120×136)"),
                               "bg1": ("#0f1a2b", "لون الخلفية العلوي"), "bg2": ("#06101c", "لون الخلفية السفلي")}},
    "countdown": {"ar": "عدّ تنازلي بقفزات ونبضات ثم كلمة الانطلاق", "seconds": None,
                  "params": {"from": ("5", "يبدأ من (≤ 10)"), "go": ("انطلق", "كلمة النهاية"), "accent": ("#FF6B6B", "لون التمييز"),
                             "bg1": ("#1a1a2e", "لون الخلفية العلوي"), "bg2": ("#0b0b14", "لون الخلفية السفلي")}},
    "end-card": {"ar": "بطاقة ختام: دعوة للمتابعة + الحساب + أيقونات تتوالى + شريط تقدم", "seconds": 6,
                 "params": {"cta": ("تابعنا للمزيد", "الدعوة"), "handle": ("@kosif", "الحساب"), "accent": ("#E7B65A", "لون التمييز"),
                            "bg1": ("#1b2a49", "لون الخلفية العلوي"), "bg2": ("#0d1b2a", "لون الخلفية السفلي")}},
    "bullet-list": {"ar": "عنوان ونقاط تتوالى مع علامة صح تُرسم لكل نقطة", "seconds": 8,
                    "params": {"title": ("ثلاث خطوات", "العنوان"), "items": ("خطّط|نفّذ|راجع", "النقاط (افصلها بـ |، حتى 6)"), "accent": ("#5BD1A5", "لون التمييز"),
                               "bg1": ("#10233a", "لون الخلفية العلوي"), "bg2": ("#071321", "لون الخلفية السفلي")}},
}


def _esc(s: str) -> str:
    return _html.escape(str(s), quote=True)


def _colour(c: str, default: str) -> str:
    c = (c or default).strip()
    return c if re.fullmatch(r"#[0-9a-fA-F]{6}", c) else default


def render_html(template: str, params: dict, w: int, h: int, seconds: float, fps: int) -> str:
    """The template filled: text keys HTML-escaped, colours validated, lists expanded, SVG paths kept to path syntax."""
    t = TEMPLATES[template]
    src = (TDIR / f"{template}.html").read_text(encoding="utf-8")
    vals = {k: str(params.get(k, d[0])) for k, d in t["params"].items()}
    out = src.replace("{{W}}", str(w)).replace("{{H}}", str(h)).replace("{{SECONDS}}", f"{seconds:g}").replace("{{FPS}}", str(fps))
    for k, v in vals.items():
        if k in ("accent", "bg1", "bg2"):
            v = _colour(v, t["params"][k][0])
        elif k == "path":
            v = v if re.fullmatch(r"[MmLlHhVvCcSsQqTtAaZz0-9 ,.\-]+", v) else t["params"][k][0]
        elif k in ("value", "decimals", "from"):
            v = v if re.fullmatch(r"-?\d+(\.\d+)?", v) else t["params"][k][0]
        elif k in ("items", "quote"):
            lines = [ln.strip() for ln in v.split("|") if ln.strip()][:6]
            v = "".join(f'<div class="line">{_esc(ln)}</div>' for ln in lines) if lines else ""
            out = out.replace("{{" + k.upper() + "_N}}", str(len(lines)))
        else:
            v = _esc(v)
        out = out.replace("{{" + k.upper() + "}}", v)
    if left := re.findall(r"\{\{[A-Z_0-9]+\}\}", out):
        raise SystemExit(f"template {template}: unfilled placeholders {sorted(set(left))}")
    return out


def create(name: str, template: str, params: dict, seconds: float | None = None, fps: int = 30, size: str = "1080x1920") -> Path:
    if template not in TEMPLATES:
        raise SystemExit(f"unknown template {template}; one of: {', '.join(TEMPLATES)}")
    name = motion.safe_name(name)
    w, h = (int(v) for v in size.lower().split("x"))
    if not (16 <= w <= 7680 and 16 <= h <= 7680) or not (1 <= int(fps) <= 120):
        raise SystemExit(f"out of range: size {size}, fps {fps}")
    t = TEMPLATES[template]
    if seconds is None:
        seconds = t["seconds"] if t["seconds"] else (int(float(params.get("from", t["params"]["from"][0]))) + 1.6)
    if not (0.5 <= float(seconds) <= 600):
        raise SystemExit("seconds out of range 0.5–600")
    d = motion.PROJECTS / name
    (d / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(render_html(template, params, w, h, float(seconds), int(fps)), encoding="utf-8")
    if FONTS.exists():
        for f in FONTS.glob("*.woff2"):
            shutil.copy2(f, d / "assets" / "fonts" / f.name)
    motion.sync_assets(d)
    (d / "template.json").write_text(json.dumps({"template": template, "params": params, "seconds": seconds, "fps": fps, "size": size}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(d)
    return d


def parse_set(items: list[str]) -> dict:
    out = {}
    for it in items:
        if "=" not in it:
            raise SystemExit(f"--set expects key=value, got {it!r}")
        k, v = it.split("=", 1)
        out[k.strip().lower()] = v.strip().strip('"')
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p = sub.add_parser("show"); p.add_argument("template")
    p = sub.add_parser("new"); p.add_argument("name"); p.add_argument("--template", required=True, choices=list(TEMPLATES))
    p.add_argument("--set", nargs="*", default=[], help="key=value …"); p.add_argument("--seconds", type=float); p.add_argument("--fps", type=int, default=30)
    p.add_argument("--size", default="1080x1920")
    a = ap.parse_args()
    if a.cmd == "list":
        for k, t in TEMPLATES.items():
            print(f"{k:<13} {t['ar']}")
        return 0
    if a.cmd == "show":
        t = TEMPLATES.get(a.template) or ap.error("unknown template")
        print(t["ar"])
        for k, (dflt, hint) in t["params"].items():
            print(f"  {k:<9} {hint:<40} [{dflt}]")
        return 0
    create(a.name, a.template, parse_set(a.set), a.seconds, a.fps, a.size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
