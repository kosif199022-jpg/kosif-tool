"""KOSIF Motion — every animation, motion, sound and edit tool behind one command.

    python kmotion.py                      an Arabic menu (pick a number, answer the questions)
    python kmotion.py help                 the full command list
    python kmotion.py COMMAND [args …]     run one tool directly (each command keeps its own --help)

Groups
  create  new · bundle · frames · check · render · sync · doctor            (motion.py — 2D / 3D / canvas films)
  sound   score · ambience · voice · beats · channels                        (score.py, ambience.py, voice.py, qa)
  edit    reel · montage · grade · captions · transcribe · decaption ·        (reel.py, montage.py, transcribe.py,
          footage · mocap                                                      decaption.py, qa)
  check   lint · sheet · speed · study · measure · loopcheck · inspect       (qa — the critique loop and the gate)
  draw    studio                                                             (KOSIF Studio window, pixel painter)
"""
from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(STUDIO))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

# command → (group, module, argv prefix, Arabic label, questions for the menu)
C = {
    "new":        ("create", "motion", ["new"], "مشروع أنيميشن جديد (2D أو 3D أو canvas)", [("name", "اسم المشروع"), ("--seconds", "المدة بالثواني", "8"), ("--3d", "ثلاثي الأبعاد؟ (y/n)", "y")]),
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
    "reel":       ("edit", "reel", [], "مونتاج تلقائي كامل لمقطع متكلم → ريلز جاهز", [("clip", "ملف الفيديو"), ("--out", "ملف الإخراج", "FINAL.mp4"), ("--model", "نموذج التفريغ (large-v3/small)", "large-v3")]),
    "montage":    ("edit", "montage", ["cut"], "مونتاج لقطات على إيقاع موسيقى", [("clips", "ملفات الفيديو (مفصولة بمسافة)"), ("--music", "ملف الموسيقى"), ("--out", "ملف الإخراج", "montage.mp4")]),
    "grade":      ("edit", "montage", ["grade"], "تلوين سينمائي (restore, teal_orange, blue_hour…)", [("video", "ملف الفيديو"), ("--preset", "القالب", "restore")]),
    "captions":   ("edit", "montage", ["captions"], "ترجمة كاريوكي عربية محروقة", [("video", "ملف الفيديو"), ("--spec", "ملف captions.json")]),
    "transcribe": ("edit", "transcribe", [], "تفريغ الكلام بالكلمات والأزمنة + SRT", [("src", "ملف الفيديو أو الصوت"), ("--model", "النموذج", "large-v3")]),
    "decaption":  ("edit", "decaption", [], "إزالة الترجمة المحروقة من فيديو", [("video", "ملف الفيديو"), ("--out", "ملف الإخراج", "clean.mp4")]),
    "footage":    ("edit", "motion", ["footage"], "تجهيز لقطة حقيقية للتركيب (قابلة للبحث إطاراً بإطار)", [("video", "ملف الفيديو"), ("--out", "ملف الإخراج")]),
    "mocap":      ("edit", "motion", ["mocap"], "التقاط حركة شخص حقيقي من فيديو → جسيمات", [("video", "ملف الفيديو"), ("--out", "ملف JSON")]),
    "lint":       ("check", "motion", ["lint"], "فحص الحتمية والذوق في مشروع", [("project", "مجلد المشروع")]),
    "sheet":      ("check", "motion", ["sheet"], "لوحة النقد (إطارات + عرض الهاتف)", [("film", "ملف الفيلم")]),
    "speed":      ("check", "motion", ["speed"], "سرعة الحركة على الشاشة", [("film", "ملف الفيلم")]),
    "study":      ("check", "motion", ["study"], "دراسة فيلم مرجعي (قطعات، ألوان، إيقاع)", [("reference", "ملف المرجع")]),
    "measure":    ("check", "motion", ["measure"], "طاقة الحركة", [("film", "ملف الفيلم")]),
    "loopcheck":  ("check", "motion", ["loopcheck"], "خياطة الحلقة", [("film", "ملف الفيلم")]),
    "inspect":    ("check", "motion", ["inspect"], "بوابة التسليم (أسود، تجمّد، LUFS، ذروة، تعريض)", [("film", "ملف الفيلم")]),
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
    m = __import__(mod)
    sys.argv = [f"{mod}.py", *prefix, *args]
    try:
        r = m.main()
    except SystemExit as e:
        return int(e.code or 0) if not isinstance(e.code, str) else 1
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
        if name == "--3d":
            if ans.lower().startswith("y") or ans in ("نعم", "ن"):
                args.append("--3d")
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
