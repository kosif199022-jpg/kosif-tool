"""KOSIF Motion — every animation, motion, sound and edit tool behind one command.

    python kmotion.py                      an Arabic menu (pick a number, answer the questions)
    python kmotion.py help                 the full command list
    python kmotion.py COMMAND [args …]     run one tool directly (each command keeps its own --help)

Groups
  create  new · template · bundle · kit-bundle · frames · check · render · preview · sync · doctor  (motion.py, mtemplates.py — 2D / 3D / canvas films)
  sound   score · ambience · voice · beats · channels                        (score.py, ambience.py, voice.py, qa)
  edit    audio2motion · timeline · transitions · scenes · privacy · direct · verse · reel · montage · grade · captions ·
          transcribe · decaption · footage · mocap · silence · aspect · trim · concat · loop · stabilize · export · thumb
          (timeline.py, scenes.py, privacy.py, direct.py, verse.py, reel.py, montage.py, transcribe.py, decaption.py, tools.py, qa)
  check   lint · sheet · speed · study · measure · loopcheck · inspect · probe · batch · fonts · proplan · structural ·
          twinview · bridge · remote                                         (qa — the critique loop and the gate; tools.py; the gated remote clients)
  draw    web · studio                                                       (KOSIF Motion Web local studio site; KOSIF Studio pixel painter)
"""
from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(STUDIO))


def _cloud_env():
    """After `kmotion setup` in a sandbox: the recorded writable home and HOME/bin (ffmpeg, ffprobe stand-in) apply to
    every call, so tools find them without the shell keeping state between commands."""
    import json
    import os
    cfg = Path.home() / ".kosif-motion.json"
    try:
        c = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    if c.get("home") and not os.environ.get("KOSIF_MOTION_HOME"):
        os.environ["KOSIF_MOTION_HOME"] = c["home"]
    b = c.get("bin")
    if b and Path(b).is_dir() and b not in os.environ.get("PATH", "").split(os.pathsep):
        os.environ["PATH"] = b + os.pathsep + os.environ.get("PATH", "")


_cloud_env()
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

# command → (group, module, argv prefix, Arabic label, questions for the menu)
C = {
    "audio2motion": ("edit", "audio2motion", [], "صوت → مشاهد موشن جرافيك حسب المعنى (Voice2Motion)", [("audio", "ملف الصوت"), ("--cues", "ملف السيناريو المؤقت JSON (أو اتركه فارغاً واستخدم --transcript)", ""), ("--transcript", "ملف نص التفريغ", ""), ("--out", "ملف الإخراج", "voice2motion.mp4")]),
    "timeline":   ("edit", "timeline", [], "تايملاين JSON → فيلم: قصّات، انتقالات xfade، سرعات متغيرة، نصوص عربية، موسيقى مخفوضة تحت الصوت (v6)", [("spec", "ملف التايملاين JSON (أو: --example edit.json)"), ("--out", "ملف الإخراج", "film.mp4")]),
    "transitions": ("edit", "timeline", ["--transitions"], "قائمة انتقالات xfade المتاحة في FFmpeg هنا (v6)", []),
    "scenes":     ("edit", "scenes", [], "كشف القطعات في فيديو حقيقي → لقطات (JSON، لوحة، تقسيم، تايملاين) (v6)", [("clip", "ملف الفيديو"), ("--sheet", "لوحة اللقطات PNG (اختياري)", ""), ("--timeline", "ملف تايملاين JSON (اختياري)", "")]),
    "privacy":    ("edit", "privacy", [], "خصوصية: تبكسل/تمويه الوجوه أو أي منطقة قبل النشر (v6)", [("clip", "ملف الفيديو"), ("--out", "ملف الإخراج", "safe.mp4"), ("--mode", "pixelate/blur/box", "pixelate")]),
    "setup":      ("check", "cloud_setup", [], "تجهيز بيئة سحابية (claude.ai) بلا كمبيوتر: مجلد قابل للكتابة، ffmpeg وبديل ffprobe، الأمثلة (v6.1)", [("--install", "ثبّت imageio-ffmpeg إن لم يوجد ffmpeg؟ (y/n)", "y")]),
    "workbench":  ("create", "workbench_cli", [], "فيلم موشن 2D بلا متصفح: مهمة → خطة → manifest → MP4 (Pillow + FFmpeg) (v6.1)", [("task", "موضوع الفيلم"), ("--aspect", "النسبة", "9:16"), ("--seconds", "المدة", "12"), ("--out", "ملف الإخراج", "workbench.mp4")]),
    "studio-import": ("edit", "studio_import", [],"مشروع KOSIF Studio 6.0 (JSON من محرر المتصفح) → تايملاين يُصيَّر بجودة كاملة (v6.1)", [("project", "ملف المشروع JSON"), ("--out", "ملف التايملاين", "edit.json"), ("--media", "مجلد الوسائط", "")]),
    "platforms":  ("edit", "platforms", [],"تصدير لمنصات بعينها (tiktok, reels, shorts, youtube, x, whatsapp, linkedin, snapchat) مع فحص الحدود (v6)", [("film", "ملف الفيلم"), ("--out", "مجلد الإخراج", "deliver"), ("--platforms", "المنصات", "tiktok,reels,shorts")]),
    "template":   ("create", "mtemplates", [],"قوالب موشن جاهزة: list · show T · new NAME --template T --set key=value (v6)", [("cmd", "list / show / new", "list")]),
    "remote":     ("check", "render_client", [], "تصيير 2D صامت على خادم Python خارجي عبر Workbench (status / render --plan --allow-remote) — موافقة صريحة (v5.3)", []),
    "web":        ("draw", None, [], "موقع الاستوديو المحلي KOSIF Motion Web: وسائط، وصفات، مشاريع، تايملاين، مهام، Workbench، MCP (v6)", [("--port", "المنفذ", "8766")]),
    "bridge":     ("check", "site_bridge", [], "مخطط Workbench العام (health/templates/plan/validate/compile/project) — POST يحتاج --allow-remote", []),
    "new":        ("create", "motion", ["new"], "مشروع أنيميشن جديد (2D أو 3D أو canvas)", [("name", "اسم المشروع"), ("--seconds", "المدة بالثواني", "8"), ("--3d", "ثلاثي الأبعاد؟ (y/n)", "y"), ("--lab", "مختبر المنتج (شخصيات قطيفة + HUD)؟ (y/n)", "n")]),
    "kit-bundle": ("create", "motion", ["kit-bundle"], "إعادة بناء حزمة العدّة ثلاثية الأبعاد (بعد تعديل three-kit.js)", []),
    "bundle":     ("create", "motion", ["bundle"], "تجميع مشهد ثلاثي الأبعاد (بعد تعديل main.js)", [("project", "مجلد المشروع (مثلاً projects/NAME)")]),
    "frames":     ("create", "motion", ["frames"], "إطارات مراجعة قبل التصيير", [("project", "مجلد المشروع"), ("--times", "الأزمنة (مثلاً 1,4,7)", "1,4,7")]),
    "check":      ("create", "motion", ["check"], "فحص HyperFrames", [("project", "مجلد المشروع")]),
    "render":     ("create", "motion", ["render"], "تصيير الفيلم MP4", [("project", "مجلد المشروع"), ("--engine", "المحرك (studio/auto)", "studio"), ("--blur", "ضبابية الحركة (1-16)", "4")]),
    "sync":       ("create", "motion", ["sync"], "تحديث العدّة داخل مشروع", [("project", "مجلد المشروع")]),
    "doctor":     ("create", "motion", ["doctor"], "فحص التثبيت", []),
    "score":      ("sound", "score", [], "موسيقى أصلية على شبكة الإيقاع", [("out", "ملف الإخراج WAV"), ("--spec", "ملف spec JSON (اتركه فارغاً للافتراضي)", ""), ("--seconds", "المدة", "15")]),
    "ambience":   ("sound", "ambience", [], "صوت محيط (مطر، بحر، طيور…)", [("out", "ملف الإخراج WAV"), ("--seconds", "المدة", "10")]),
    "voice":      ("sound", "voice", [], "تعليق صوتي عربي بلا إنترنت", [("out", "ملف الإخراج WAV"), ("--text", "النص")]),
    "beats":      ("sound", "motion", ["beats"], "إيقاع أي مقطع (BPM والنبضات)", [("audio", "ملف الصوت")]),
    "channels":   ("sound", "motion", ["channels"], "قنوات الصوت لكل إطار (كِك، باص، توقف الشريط)", [("audio", "ملف الصوت")]),
    "direct":     ("edit", "direct", [], "مونتاج موجَّه تلقائي (كلمات مفتاحية، كاميرا، رموز، ذروة) قابل للتعديل", [("clip", "ملف الفيديو"), ("--name", "اسم المشروع", "directed"), ("--credit", "حساب صاحب المقطع (اختياري)", "")]),
    "verse":      ("edit", "verse", [], "فيلم نص حركي من صوت فقط (أغنية، قصيدة، دعاء، تعليق صوتي) يتنفس مع الإيقاع", [("audio", "ملف الصوت أو الفيديو"), ("--name", "اسم المشروع", "verse"), ("--title", "العنوان (اختياري)", "")]),
    "reel":       ("edit", "reel", [], "مونتاج تلقائي كامل لمقطع متكلم → ريلز جاهز", [("clip", "ملف الفيديو"), ("--out", "ملف الإخراج", "FINAL.mp4"), ("--model", "نموذج التفريغ (large-v3/small)", "large-v3")]),
    "montage":    ("edit", "montage", ["cut"], "مونتاج لقطات على إيقاع موسيقى", [("clips", "ملفات الفيديو (مفصولة بمسافة)"), ("--music", "ملف الموسيقى"), ("--out", "ملف الإخراج", "montage.mp4")]),
    "grade":      ("edit", "montage", ["grade"], "تلوين سينمائي (restore, teal_orange, blue_hour…)", [("video", "ملف الفيديو"), ("--preset", "القالب", "restore")]),
    "captions":   ("edit", "montage", ["captions"], "ترجمة كاريوكي عربية محروقة", [("video", "ملف الفيديو"), ("--spec", "ملف captions.json")]),
    "transcribe": ("edit", "transcribe", [], "تفريغ الكلام بالكلمات والأزمنة + SRT", [("src", "ملف الفيديو أو الصوت"), ("--model", "النموذج", "large-v3")]),
    "decaption":  ("edit", "decaption", [], "إزالة الترجمة المحروقة من فيديو", [("video", "ملف الفيديو"), ("--out", "ملف الإخراج", "clean.mp4")]),
    "footage":    ("edit", "motion", ["footage"], "تجهيز لقطة حقيقية للتركيب (قابلة للبحث إطاراً بإطار)", [("video", "ملف الفيديو"), ("--out", "ملف الإخراج")]),
    "mocap":      ("edit", "motion", ["mocap"], "التقاط حركة شخص حقيقي من فيديو → جسيمات", [("video", "ملف الفيديو"), ("--out", "ملف JSON")]),
    "preview":    ("create", "motion", ["preview"], "مسودة سريعة للمراجعة (نصف الحجم، 15 إطار/ث)", [("project", "مجلد المشروع")]),
    "silence":    ("edit", "tools", ["silence"], "قص الصمت من مقطع متكلم (جامب كت)", [("clip", "ملف الفيديو"), ("--out", "ملف الإخراج", "cut.mp4")]),
    "aspect":     ("edit", "tools", ["aspect"], "تحويل النسبة (9:16 بقص ذكي حول الوجوه أو خلفية مموّهة)", [("clip", "ملف الفيديو"), ("--to", "النسبة", "9:16"), ("--mode", "smart/crop/blur", "smart"), ("--out", "ملف الإخراج", "vertical.mp4")]),
    "trim":       ("edit", "tools", ["trim"], "قص جزء بدقة الإطار", [("clip", "ملف الفيديو"), ("--from", "من (ثانية)", "0"), ("--to", "إلى (ثانية)"), ("--out", "ملف الإخراج", "part.mp4")]),
    "concat":     ("edit", "tools", ["concat"], "دمج مقاطع متتالية (أحجام مختلفة تُوفَّق)", [("clips", "ملفات الفيديو (مفصولة بمسافة)"), ("--out", "ملف الإخراج", "all.mp4")]),
    "loop":       ("edit", "tools", ["loop"], "حلقة بلا درزة (الذيل يذوب في البداية)", [("clip", "ملف الفيديو"), ("--seconds", "المدة الكلية", "30"), ("--out", "ملف الإخراج", "loop.mp4")]),
    "stabilize":  ("edit", "tools", ["stabilize"], "تثبيت اهتزاز الكاميرا", [("clip", "ملف الفيديو"), ("--out", "ملف الإخراج", "steady.mp4")]),
    "export":     ("edit", "tools", ["export"], "كل نسخ التسليم دفعة واحدة (9:16، 1:1، 16:9، بوستر، GIF)", [("film", "ملف الفيلم"), ("--out", "مجلد الإخراج", "deliver"), ("--title", "عنوان البوستر (اختياري)", "")]),
    "thumb":      ("edit", "tools", ["thumb"], "صورة غلاف بعنوان عربي", [("film", "ملف الفيلم"), ("--at", "الثانية", "2"), ("--text", "العنوان", ""), ("--out", "ملف الإخراج", "cover.jpg")]),
    "probe":      ("check", "tools", ["probe"], "معلومات الملف (الأبعاد، المدة، الصوت)", [("file", "الملف")]),
    "batch":      ("check", "tools", ["batch"], "تشغيل عدة مهام معاً من jobs.json", [("jobs", "ملف المهام JSON"), ("--parallel", "عدد المهام المتوازية", "2")]),
    "fonts":      ("check", "tools", ["fonts"], "الخطوط العربية المتاحة على هذا الجهاز", []),
    "lint":       ("check", "motion", ["lint"], "فحص الحتمية والذوق في مشروع", [("project", "مجلد المشروع")]),
    "review":     ("check", "review", [], "مراجعة مشهد بمشهد (صفحة Motion OS): init · apply · export · feedback · bump · list (v6.2)", [("cmd", "init / apply / export / feedback / bump / list", "list"), ("target", "المشروع أو التايملاين أو الفيديو أو اسم المراجعة", "")]),
    "aiprompts":  ("create", "aiprompts", [], "برومبتات فيديو ذكاء اصطناعي لكل لقطة بالطبقات السبع (Veo, Sora, Kling, Runway + إطار مفتاحي) (v6.2)", [("src", "ملف اللقطات JSON أو reel.json أو مجلد مشروع"), ("--out", "ملف الإخراج", "ai-video-prompts.json")]),
    "brag":       ("create", "launch", [], "فيديو إطلاق لمشروع أو موقع (طريقة /brag): init يجمع المادة ويكتب الخطة · deliver يضع الملصق ويفحص (v6.2)", [("cmd", "init / deliver", "init"), ("source", "مجلد المشروع أو رابط الموقع (أو مجلد الإخراج مع deliver)", ".")]),
    "poster":     ("check", "poster", [], "أقوى إطار مستقر كصورة غلاف، ويُثبَّت كإطار 0 مع --bake (v6.2)", [("film", "ملف الفيلم"), ("--bake", "ثبّته كإطار 0؟ (y/n)", "y")]),
    "readable":   ("check", "launch", ["readable"], "هل يبقى كل سطر على الشاشة وقتاً يكفي لقراءته؟ (reel.json / verse.json / تايملاين) (v6.2)", [("file", "الملف")]),
    "sfx":        ("sound", "launch", ["sfx"], "مؤثرات صوتية CC0 جاهزة للتايملاين (kit:NAME) واستعمال كل منها (v6.2)", []),
    "final":      ("create", "motion", ["final"], "التصيير النهائي بأعلى جودة: التقاط بلا فقد، CRF 16، الضلع الأقصر ≥ 1080، غلاف مثبّت وفحص (v6.2)", [("project", "مجلد المشروع"), ("--blur", "ضبابية الحركة (1-8)", "1")]),
    "analyze":    ("check", "analyze", [], "تحليل فيديو مرجعي لإعادة بنائه: لقطة بلقطة، ألوان، حركة، انتقالات، صوت + إطارات للقراءة (v6.2)", [("video", "ملف الفيديو"), ("--out", "مجلد التحليل", "")]),
    "omniprompt": ("check", "omniprompt", [], "تحويل التحليل المكتمل إلى برومبت Google Omni Flash جاهز (10 ثوانٍ) مع تعديلاتك (v6.2)", [("brief", "ملف brief.json"), ("--overrides", "ملف التعديلات JSON (اختياري)", "")]),
    "mimic":      ("edit", "mimic", [], "المحاكاة: إعادة بناء ريل مرجعي لقطة بلقطة بلقطات جديدة (نفس القطعات والانتقالات والكتابة والصوت): study · fonts · match · build · compare (v6.3)", [("cmd", "study / fonts / match / build / compare", "study")]),
    "songreel":   ("edit", "songreel", [], "أغنية → ريل: فهم الكلمات والإيقاع والمقطع الأقوى، بحث بنترست لكل مقطع، قص اللقطات على البيت حسب المعنى، كلمات متحركة فوق الفيديو (v6.3)", [("cmd", "analyze / queries / cut / build", "analyze")]),
    "fetch":      ("edit", "fetch", [], "تحميل فيديوهات وصور من Pinterest (دبوس أو لوحة) وTikTok وInstagram وغيرها إلى مكتبة الوسائط + نسخة جاهزة للمونتاج وسجل حقوق (v6.2)", [("urls", "الرابط (أو عدة روابط)"), ("--max", "أقصى عدد من اللوحة", "30")]),
    "audiolab":   ("sound", "audiolab", [], "مختبر الصوت: صوت فقط / موسيقى فقط / فيديو بلا موسيقى / فيديو بلا صوت (من Cinema C) (v6.2)", [("file", "الملف"), ("--mode", "voice / music / both / novoice / nomusic", "voice")]),
    "sheet":      ("check", "motion", ["sheet"], "لوحة النقد (إطارات + عرض الهاتف)", [("film", "ملف الفيلم")]),
    "speed":      ("check", "motion", ["speed"], "سرعة الحركة على الشاشة", [("film", "ملف الفيلم")]),
    "study":      ("check", "motion", ["study"], "دراسة فيلم مرجعي (قطعات، ألوان، إيقاع)", [("reference", "ملف المرجع")]),
    "measure":    ("check", "motion", ["measure"], "طاقة الحركة", [("film", "ملف الفيلم")]),
    "loopcheck":  ("check", "motion", ["loopcheck"], "خياطة الحلقة", [("film", "ملف الفيلم")]),
    "inspect":    ("check", "motion", ["inspect"], "بوابة التسليم (أسود، تجمّد، LUFS، ذروة، تعريض)", [("film", "ملف الفيلم")]),
    "proplan":    ("check", "proplan", [], "خطة إنتاج Pro قابلة للتدقيق (لا تدّعي Full Pro تلقائياً)", [("--task", "صف مهمة المونتاج/الموشن")]),
    "structural": ("check", "structural_twin", [], "Structural Twin: SHAPE/JOINT/LOAD/BREAK/SWAP/RANK (هيكل مفصلي 2D أو 3D)", [("--model", "ملف نموذج JSON")]),
    "twinview":   ("check", "twin_dashboard", [], "واجهة تجارب Structural Twin مستقلة بدون إنترنت", [("report", "ملف تقرير التحليل JSON"), ("--out", "ملف واجهة HTML")]),
    "studio":     ("draw", None, [], "فتح نافذة KOSIF Studio", []),
}
GROUPS = [("create", "الإنشاء والتصيير"), ("sound", "الصوت والموسيقى"), ("edit", "المونتاج والفيديو الحقيقي"), ("check", "الفحص والجودة"), ("draw", "الرسم")]


def run(cmd: str, args: list[str]) -> int:
    if cmd not in C:
        print(f"أمر غير معروف: {cmd}  — اكتب: python kmotion.py help"); return 2
    group, mod, prefix, _, _ = C[cmd]
    if cmd == "studio":
        if not (STUDIO / "studio.py").exists():
            print("نافذة KOSIF Studio غير موجودة في هذه النسخة (هي جزء من KOSIF Studio الكامل)."); return 1
        return subprocess.call([sys.executable, str(STUDIO / "studio.py"), *args])
    if cmd == "web":                                           # the site runs in its own process (uvicorn; jobs are subprocesses of it)
        return subprocess.call([sys.executable, str(HERE / "web" / "server.py"), *args])
    m = __import__(mod)
    sys.argv = [f"{mod}.py", *prefix, *args]
    try:
        r = m.main()
    except SystemExit as e:
        if isinstance(e.code, str):
            print(e.code, file=sys.stderr)
            return 1
        return int(e.code or 0)
    return int(r or 0)


def help_text() -> str:
    lines = ["KOSIF Motion — كل أدوات الأنيميشن والموشن في أداة واحدة", ""]
    for g, title in GROUPS:
        lines.append(f"■ {title}")
        for k, v in C.items():
            if v[0] == g:
                lines.append(f"   {k:<11} {v[3]}")
        lines.append("")
    lines.append("مثال: python kmotion.py reel clip.mp4 --out final.mp4      ·  تفاصيل أمر: python kmotion.py render --help")
    return "\n".join(lines)


def menu() -> int:
    keys = list(C)
    print("KOSIF Motion — اختر رقماً:\n")
    n = 0
    for g, title in GROUPS:
        print(f"■ {title}")
        for k in keys:
            if C[k][0] == g:
                n += 1
                print(f"  {n:>2}. {C[k][3]}   ({k})")
    order = [k for g, _ in GROUPS for k in keys if C[k][0] == g]
    try:
        pick = input("\nالرقم (أو Enter للخروج): ").strip()
    except EOFError:
        return 0
    if not pick:
        return 0
    if not pick.isdigit() or not (1 <= int(pick) <= len(order)):
        print("رقم غير صحيح"); return 2
    cmd = order[int(pick) - 1]
    args: list[str] = []
    for q in C[cmd][4]:
        name, label, default = q[0], q[1], (q[2] if len(q) > 2 else None)
        ans = input(f"{label}{f' [{default}]' if default is not None else ''}: ").strip() or (default or "")
        if name in ("--3d", "--lab", "--install"):
            if ans.lower().startswith("y") or ans in ("نعم", "ن"):
                args.append(name)
            continue
        if not ans:
            continue
        vals = shlex.split(ans, posix=False) if name in ("clips",) else [ans.strip('"')]
        args += vals if not name.startswith("--") else [name, *vals]
    print(f"\n▶ python kmotion.py {cmd} {' '.join(args)}\n")
    return run(cmd, args)


def main():
    if len(sys.argv) < 2:
        sys.exit(menu())
    cmd = sys.argv[1]
    if cmd in ("help", "-h", "--help"):
        print(help_text()); return
    sys.exit(run(cmd, sys.argv[2:]))


if __name__ == "__main__":
    main()
