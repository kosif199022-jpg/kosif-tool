#!/usr/bin/env python3
"""بوابة الستوري بورد قبل البناء: تفحص scenes.json وstoryboard.json ضد قواعد الفيلم (عدد المشاهد، وأوصاف فعلية، والجسم الحامل في كل مشهد، و≤ 8 كلمات في الإطار، وتغطية البطل، واختبار الجسم لكل إيقاع، وميزانية الكاميرا).

usage: python storyboard_gate.py --scenes scenes.json [--storyboard storyboard.json] [--anchor "الشعار"]
scenes.json: [{"name":"Strike","dur":2.5,"desc":"The mark lands and throws colour across the ground","phrase":"…","body":"the mark dives","surface":"ground plate"}]
storyboard.json: {"anchor":"the mark","camera_events":[{"at":[0,2.5],"what":"push-in"}],
  "frames":[{"t":1.2,"asset":"ATTACH/mark.png","coverage_pct":35,"moving_elements":2,"words":"Fast. Simple.","anchor_visible":true}]}
الخروج 0 عند المرور، 1 عند وجود مخالفات (قائمة مفصّلة).
"""
import argparse
import json
import re
import sys

MOOD_WORDS = r"\b(sense of|feeling of|mood|vibe|energy|possibility|elegant|premium|modern|dynamic|إحساس|شعور|مزاج|أجواء|أنيق|عصري)\b"
VERB_HINT = r"\b(lands|hits|drops|slides|cuts|opens|turns|pushes|pulls|folds|snaps|becomes|strikes|dives|hammers|hops|rises|falls|swings|locks|يسقط|يضرب|ينزلق|يفتح|يصبح|يندفع|يقفز|يرتفع|يهبط)\b"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenes", required=True); ap.add_argument("--storyboard"); ap.add_argument("--anchor", default="")
    a = ap.parse_args()
    scenes = json.load(open(a.scenes, encoding="utf-8"))
    sb = json.load(open(a.storyboard, encoding="utf-8")) if a.storyboard else {}
    anchor = a.anchor or sb.get("anchor", "")
    issues, total = [], sum(float(s.get("dur", 0)) for s in scenes)
    if not (4 <= len(scenes) <= 8):
        issues.append(f"{len(scenes)} مشاهد: 6 فيلم جيد، 10 عرض شرائح (المسموح 4-8)")
    for s in scenes:
        d = s.get("desc", "")
        if not d or len(d.split()) < 5:
            issues.append(f"مشهد {s.get('name')}: الوصف أقصر من جملة")
        if re.search(MOOD_WORDS, d, re.I) and not re.search(VERB_HINT, d, re.I):
            issues.append(f"مشهد {s.get('name')}: الوصف مزاج لا حدث فيزيائي؛ سمِّ ما يحدث بفعل")
        if not s.get("body"):
            issues.append(f"مشهد {s.get('name')}: اختبار الجسم فشل؛ السطر الثاني (جسم بفعل) فارغ = بطاقة")
        elif s.get("phrase") and s["body"].strip().lower() == s["phrase"].strip().lower():
            issues.append(f"مشهد {s.get('name')}: الجسم هو العبارة نفسها؛ الكلمة ليست جسماً")
        if not s.get("surface"):
            issues.append(f"مشهد {s.get('name')}: لا سطح (ملف من المجموعة أو جزء واجهة مُعاد بناؤه)")
    if not anchor:
        issues.append("لا جسم حامل (anchor) مسمّى")
    frames = sb.get("frames", [])
    for f in frames:
        w = len(re.findall(r"[\w؀-ۿ']+", f.get("words", "")))
        if w > 8:
            issues.append(f"إطار t={f.get('t')}: {w} كلمات > 8")
        cov = f.get("coverage_pct")
        if cov is not None and cov < 25:
            issues.append(f"إطار t={f.get('t')}: تغطية البطل {cov}% < 25% من العرض")
        if f.get("moving_elements", 0) < 2 and not f.get("hold"):
            issues.append(f"إطار t={f.get('t')}: أقل من عنصرين في تحوّل (ليس احتجازاً مسمّى)")
        if anchor and f.get("anchor_visible") is False:
            issues.append(f"إطار t={f.get('t')}: الجسم الحامل غائب")
        if f.get("asset") and not re.search(r"\.(png|svg|jpg|webp)$", f["asset"], re.I):
            issues.append(f"إطار t={f.get('t')}: الأصل ليس ملفاً من المجموعة")
    cams = sb.get("camera_events", [])
    if len(cams) > 4:
        issues.append(f"{len(cams)} أحداث كاميرا > 4: الكاميرا تثبت والأجسام تعمل")
    holds = sum(1 for f in frames if f.get("hold"))
    if frames and holds > 3:
        issues.append(f"{holds} احتجازات > 3 (اثنان أو ثلاثة + اللقطة الختامية)")
    rep = {"scenes": len(scenes), "total_s": round(total, 2), "frames": len(frames), "camera_events": len(cams), "anchor": anchor, "issues": issues,
           "verdict": "PASS" if not issues else "REVISE", "next": "اعرض اللوحات على صاحب الطلب للموافقة قبل أي رندر؛ ثم ابنِ أول 5-8 ثوانٍ فقط"}
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(rep, ensure_ascii=False, indent=1)); sys.exit(0 if not issues else 1)


if __name__ == "__main__":
    main()
