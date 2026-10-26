"""The recipe catalogue of the local studio: every kmotion command the site offers, with typed fields, so the
browser builds forms, the MCP tools validate arguments, and the server builds an argv list — never a shell string.

field = (arg, kind, label_ar, default, choices)   kind: file · files · save · dir · text · number · choice · bool · set
Positional arguments are the entries whose name does not start with --; they are passed after `--` so a value that
starts with a dash can never become an option.
"""
from __future__ import annotations

import shlex

GRADES = ["restore", "teal_orange", "golden_hour", "blue_hour", "sodium_night", "cyberpunk", "vintage_film", "matrix_tech", "clean_commercial", "magma_night", "none"]
STYLES = ["reels", "tiktok", "hormozi", "boxed", "minimal", "cinema", "punchy"]
TEMPLATES = ["title-card", "lower-third", "stat-counter", "quote-card", "logo-reveal", "countdown", "end-card", "bullet-list"]
SIZES = ["1080x1920", "1920x1080", "1080x1080", "1080x1350"]
RATIOS = ["9:16", "16:9", "1:1", "4:5"]

# group → list of recipes; recipe = {id, ar, cmd, prefix, fields, out (which field names the main output)}
GROUPS = [
    ("auto", "مونتاج تلقائي", [
        {"id": "reel", "ar": "ريلز جاهز من مقطع متكلم", "cmd": "reel", "prefix": [], "out": "--out",
         "fields": [("clip", "file", "ملف الفيديو", "", None), ("--out", "save", "ملف الإخراج", "out/FINAL.mp4", None),
                    ("--model", "choice", "نموذج التفريغ", "large-v3", ["large-v3", "small", "auto"]), ("--credit", "text", "حساب صاحب المقطع", "", None),
                    ("--style", "choice", "أسلوب الترجمة", "reels", STYLES)]},
        {"id": "direct", "ar": "مونتاج موجَّه (كلمات، كاميرا، ذروة) → مشروع قابل للتعديل", "cmd": "direct", "prefix": [], "out": None,
         "fields": [("clip", "file", "ملف الفيديو", "", None), ("--name", "text", "اسم المشروع", "directed", None), ("--credit", "text", "حساب صاحب المقطع", "", None)]},
        {"id": "verse", "ar": "فيلم كلمات من صوت (أغنية، قصيدة، دعاء) → مشروع", "cmd": "verse", "prefix": [], "out": None,
         "fields": [("audio", "file", "ملف الصوت أو الفيديو", "", None), ("--name", "text", "اسم المشروع", "verse", None), ("--text", "file", "ملف الكلمات (اختياري)", "", None),
                    ("--title", "text", "العنوان", "", None), ("--mood", "choice", "المزاج", "night", ["night", "dawn", "gold", "sea", "ink"])]},
        {"id": "audio2motion", "ar": "Voice2Motion: صوت → موشن جرافيك حسب المعنى", "cmd": "audio2motion", "prefix": [], "out": "--out",
         "fields": [("audio", "file", "ملف الصوت", "", None), ("--cues", "file", "ملف الإشارات JSON (اختياري)", "", None), ("--transcript", "file", "ملف النص (اختياري)", "", None),
                    ("--out", "save", "ملف الإخراج", "out/voice2motion.mp4", None)]},
        {"id": "montage", "ar": "مونتاج لقطات على إيقاع موسيقى", "cmd": "montage", "prefix": ["cut"], "out": "--out",
         "fields": [("clips", "files", "ملفات الفيديو", "", None), ("--music", "file", "الموسيقى", "", None), ("--out", "save", "ملف الإخراج", "out/montage.mp4", None),
                    ("--grade", "choice", "التلوين", "teal_orange", GRADES), ("--ratio", "choice", "النسبة", "9:16", RATIOS), ("--seconds", "number", "المدة (فارغ = طول الموسيقى)", "", None),
                    ("--keep-audio", "bool", "إبقاء صوت اللقطات", "0", None)]},
    ]),
    ("v6", "تايملاين · لقطات · خصوصية · قوالب", [
        {"id": "timeline", "ar": "تايملاين JSON → فيلم (قصّات، انتقالات، سرعات، نصوص، موسيقى مخفوضة)", "cmd": "timeline", "prefix": [], "out": "--out",
         "fields": [("spec", "file", "ملف التايملاين JSON", "", None), ("--out", "save", "ملف الإخراج", "out/film.mp4", None),
                    ("--workers", "number", "عمليات متوازية (0 = تلقائي)", "0", None), ("--inspect", "bool", "بوابة التسليم بعد التصيير", "1", None)]},
        {"id": "studio-import", "ar": "مشروع KOSIF Studio (JSON من المحرر) → تايملاين → فيلم بجودة كاملة", "cmd": "studio-import", "prefix": [], "out": "--render",
         "fields": [("project", "file", "ملف مشروع Studio JSON", "", None), ("--out", "save", "ملف التايملاين", "out/studio.json", None), ("--media", "dir", "مجلد الوسائط (الافتراضي: مكتبة الموقع)", "", None),
                    ("--render", "save", "تصيير مباشر إلى MP4 (اختياري)", "out/studio.mp4", None)]},
        {"id": "scenes", "ar": "كشف القطعات → لقطات (JSON، لوحة، تايملاين)", "cmd": "scenes", "prefix": [], "out": "--sheet",
         "fields": [("clip", "file", "ملف الفيديو", "", None), ("--threshold", "number", "الحساسية 0–100", "10", None), ("--sheet", "save", "لوحة اللقطات PNG", "out/shots.png", None),
                    ("--timeline", "save", "تايملاين JSON (اختياري)", "", None), ("--split", "dir", "مجلد لتقسيم اللقطات (اختياري)", "", None)]},
        {"id": "privacy", "ar": "خصوصية: تبكسل/تمويه الوجوه أو منطقة", "cmd": "privacy", "prefix": [], "out": "--out",
         "fields": [("clip", "file", "ملف الفيديو", "", None), ("--out", "save", "ملف الإخراج", "out/safe.mp4", None), ("--mode", "choice", "الأسلوب", "pixelate", ["pixelate", "blur", "box"]),
                    ("--strength", "number", "القوة", "18", None), ("--region", "text", "منطقة ثابتة x,y,w,h[,من,إلى] (اختياري)", "", None)]},
        {"id": "template", "ar": "قالب موشن جاهز → مشروع", "cmd": "template", "prefix": ["new"], "out": None,
         "fields": [("name", "text", "اسم المشروع", "card1", None), ("--template", "choice", "القالب", "title-card", TEMPLATES),
                    ("--set", "set", "المعاملات: title=\"…\" sub=\"…\" accent=#E7B65A", "", None), ("--size", "choice", "المقاس", "1080x1920", SIZES),
                    ("--seconds", "number", "المدة (فارغ = الافتراضي)", "", None)]},
    ]),
    ("films", "الأفلام من الكود", [
        {"id": "new", "ar": "مشروع أنيميشن جديد (2D / 3D / مختبر)", "cmd": "new", "prefix": [], "out": None,
         "fields": [("name", "text", "اسم المشروع", "film1", None), ("--seconds", "number", "المدة", "8", None), ("--size", "choice", "المقاس", "1080x1920", SIZES),
                    ("--title", "text", "العنوان", "", None), ("--3d", "bool", "ثلاثي الأبعاد", "0", None), ("--lab", "bool", "مختبر المنتج", "0", None)]},
        {"id": "frames", "ar": "إطارات مراجعة (بوابة الثماني ثوانٍ)", "cmd": "frames", "prefix": [], "out": None,
         "fields": [("project", "dir", "مجلد المشروع", "", None), ("--times", "text", "الأزمنة", "1,4,7", None)]},
        {"id": "preview", "ar": "مسودة سريعة (نصف الحجم، 15 إطار/ث)", "cmd": "preview", "prefix": [], "out": None, "fields": [("project", "dir", "مجلد المشروع", "", None)]},
        {"id": "render", "ar": "تصيير الفيلم (متصفحات متوازية)", "cmd": "render", "prefix": [], "out": "--out",
         "fields": [("project", "dir", "مجلد المشروع", "", None), ("--engine", "choice", "المحرك", "studio", ["studio", "auto"]), ("--blur", "number", "ضبابية الحركة", "4", None),
                    ("--workers", "number", "متصفحات متوازية (0 = تلقائي)", "0", None), ("--out", "save", "ملف الإخراج (اختياري)", "", None), ("--force", "bool", "إعادة التصيير رغم الكاش", "0", None)]},
        {"id": "lint", "ar": "فحص الحتمية والذوق في مشروع", "cmd": "lint", "prefix": [], "out": None, "fields": [("project", "dir", "مجلد المشروع", "", None)]},
    ]),
    ("tools", "أدوات سريعة", [
        {"id": "silence", "ar": "قص الصمت (جامب كت)", "cmd": "silence", "prefix": [], "out": "--out", "fields": [("clip", "file", "ملف الفيديو", "", None), ("--out", "save", "ملف الإخراج", "out/cut.mp4", None)]},
        {"id": "aspect", "ar": "تحويل النسبة (قص ذكي حول الوجوه)", "cmd": "aspect", "prefix": [], "out": "--out",
         "fields": [("clip", "file", "ملف الفيديو", "", None), ("--to", "choice", "إلى", "9:16", RATIOS), ("--mode", "choice", "الطريقة", "smart", ["smart", "crop", "blur"]),
                    ("--out", "save", "ملف الإخراج", "out/vertical.mp4", None)]},
        {"id": "grade", "ar": "تلوين سينمائي", "cmd": "grade", "prefix": [], "out": "--out",
         "fields": [("video", "file", "ملف الفيديو", "", None), ("--preset", "choice", "القالب", "restore", GRADES), ("--out", "save", "ملف الإخراج", "out/graded.mp4", None)]},
        {"id": "captions", "ar": "ترجمة كاريوكي عربية محروقة", "cmd": "captions", "prefix": [], "out": "--out",
         "fields": [("video", "file", "ملف الفيديو", "", None), ("--spec", "file", "ملف captions.json", "", None), ("--style", "choice", "الأسلوب", "reels", STYLES),
                    ("--out", "save", "ملف الإخراج", "out/captioned.mp4", None)]},
        {"id": "transcribe", "ar": "تفريغ الكلام بالكلمات والأزمنة + SRT", "cmd": "transcribe", "prefix": [], "out": None,
         "fields": [("src", "file", "ملف الفيديو أو الصوت", "", None), ("--model", "choice", "النموذج", "large-v3", ["large-v3", "small", "auto"])]},
        {"id": "decaption", "ar": "إزالة الترجمة المحروقة", "cmd": "decaption", "prefix": [], "out": "--out", "fields": [("video", "file", "ملف الفيديو", "", None), ("--out", "save", "ملف الإخراج", "out/clean.mp4", None)]},
        {"id": "stabilize", "ar": "تثبيت الاهتزاز", "cmd": "stabilize", "prefix": [], "out": "--out", "fields": [("clip", "file", "ملف الفيديو", "", None), ("--out", "save", "ملف الإخراج", "out/steady.mp4", None)]},
        {"id": "trim", "ar": "قص جزء بدقة الإطار", "cmd": "trim", "prefix": [], "out": "--out",
         "fields": [("clip", "file", "ملف الفيديو", "", None), ("--from", "number", "من (ثانية)", "0", None), ("--to", "number", "إلى (ثانية)", "", None), ("--out", "save", "ملف الإخراج", "out/part.mp4", None)]},
        {"id": "export", "ar": "تصدير كل النسب (9:16، 1:1، 16:9) + بوستر", "cmd": "export", "prefix": [], "out": "--out",
         "fields": [("film", "file", "ملف الفيلم", "", None), ("--out", "dir", "مجلد الإخراج", "out/deliver", None), ("--aspects", "text", "النسب", "9:16,1:1,16:9", None),
                    ("--title", "text", "عنوان البوستر", "", None), ("--gif", "bool", "GIF", "0", None)]},
        {"id": "platforms", "ar": "تصدير لمنصات بعينها مع فحص الحدود (مدة، حجم، بتريت)", "cmd": "platforms", "prefix": [], "out": "--out",
         "fields": [("film", "file", "ملف الفيلم", "", None), ("--out", "dir", "مجلد الإخراج", "out/deliver", None),
                    ("--platforms", "text", "tiktok,reels,shorts,youtube,x,whatsapp,linkedin,snapchat", "tiktok,reels,shorts", None), ("--title", "text", "عنوان البوستر", "", None)]},
        {"id": "thumb", "ar": "غلاف بعنوان عربي", "cmd": "thumb", "prefix": [], "out": "--out",
         "fields": [("film", "file", "ملف الفيلم", "", None), ("--at", "number", "الثانية", "2", None), ("--text", "text", "العنوان", "", None), ("--out", "save", "ملف الإخراج", "out/cover.jpg", None)]},
        {"id": "score", "ar": "موسيقى أصلية على شبكة الإيقاع (WAV)", "cmd": "score", "prefix": [], "out": "out",
         "fields": [("out", "save", "ملف الإخراج WAV", "out/score.wav", None), ("--seconds", "number", "المدة", "15", None), ("--bpm", "number", "BPM", "120", None)]},
    ]),
    ("qa", "الفحص والجودة", [
        {"id": "inspect", "ar": "بوابة التسليم (أسود، تجمّد، LUFS، ذروة، تعريض)", "cmd": "inspect", "prefix": [], "out": None, "fields": [("film", "file", "ملف الفيلم", "", None)]},
        {"id": "sheet", "ar": "لوحة النقد (إطارات + عرض الهاتف)", "cmd": "sheet", "prefix": [], "out": None, "fields": [("film", "file", "ملف الفيلم", "", None)]},
        {"id": "probe", "ar": "معلومات الملف", "cmd": "probe", "prefix": [], "out": None, "fields": [("file", "file", "الملف", "", None)]},
        {"id": "doctor", "ar": "فحص البيئة", "cmd": "doctor", "prefix": [], "out": None, "fields": []},
        {"id": "transitions", "ar": "الانتقالات المتاحة", "cmd": "transitions", "prefix": [], "out": None, "fields": []},
    ]),
]
BY_ID = {r["id"]: r for _, _, rs in GROUPS for r in rs}


def catalogue() -> list[dict]:
    return [{"id": gid, "ar": gar, "recipes": [{**r, "fields": [{"arg": a, "kind": k, "label": l, "default": d, "choices": c} for a, k, l, d, c in r["fields"]]} for r in rs]}
            for gid, gar, rs in GROUPS]


def build_args(recipe: dict, values: dict) -> list[str]:
    """argv after the kmotion command: options first, then `--`, then positionals; unknown keys are an error."""
    fields = {a: (k, d) for a, k, _, d, _ in recipe["fields"]}
    unknown = set(values) - set(fields)
    if unknown:
        raise ValueError(f"unknown fields for {recipe['id']}: {', '.join(sorted(unknown))}")
    pos, opt = [], []
    for arg, kind, _, dflt, _ in recipe["fields"]:
        v = values.get(arg, dflt)
        v = "" if v is None else str(v).strip()
        if kind == "bool":
            if v in ("1", "true", "True", "yes", "on"):
                opt.append(arg)
            continue
        if not v:
            continue
        if "\x00" in v or "\n" in v:
            raise ValueError(f"{arg}: invalid characters")
        if kind == "files":
            items = [p.strip() for p in v.split("|") if p.strip()]
            if arg.startswith("--"):
                opt += [arg, *items]
            else:
                pos += items
        elif kind == "set":
            opt += [arg, *shlex.split(v, posix=True)]
        elif arg.startswith("--"):
            opt += [arg, v]
        else:
            pos.append(v)
    return [*recipe["prefix"], *opt, *(["--", *pos] if pos else [])]
