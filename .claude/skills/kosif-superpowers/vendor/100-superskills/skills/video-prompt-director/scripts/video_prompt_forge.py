#!/usr/bin/env python3
"""قائمة لقطات (JSON) → برومبت فيديو لكل لقطة ولكل منصة (Veo، Sora، Kling، Runway، Luma، Pika، Hailuo) + فحص الاستمرارية.

usage: python video_prompt_forge.py shots.json [--platforms veo,sora,kling,runway,luma,pika,hailuo] [--out prompts.md]
shots.json:
{
 "locks": {"character": "Layla, 28, olive skin, short curly hair, round glasses, linen apron",
           "style": "warm editorial realism, soft film grain", "location": "minimal cafe, palm-wood counter, big east window"},
 "aspect": "9:16", "fps": 24,
 "shots": [
  {"n": 1, "duration": 6, "action": "Layla pours latte art; steam rises slowly", "camera": "slow push-in", "lens": "50mm",
   "lighting": "soft window key from camera left, warm", "environment_motion": "dust in light, steam", "grade": "teal-amber, lifted blacks"},
  {"n": 2, "duration": 5, "action": "she slides the cup across the counter and smiles", "camera": "static, locked-off", "lens": "85mm", ...}
 ]
}
القواعد: حركة كاميرا واحدة لكل لقطة؛ المدة ضمن حدود المنصة؛ الأقفال تُعاد حرفياً في كل لقطة؛ لا أشخاص حقيقيين.
"""
import argparse
import json
import re
import sys

LIMITS = {"veo": 8, "sora": 20, "kling": 10, "runway": 10, "luma": 9, "pika": 10, "hailuo": 10}
CAMERA_WORDS = r"\b(push[- ]in|pull[- ]out|dolly|tracking|orbit|arc|crane|handheld|whip pan|pan|tilt|rack focus|dolly[- ]zoom|drone|flyover|static|locked[- ]off|pov|zoom)\b"


def clean(s) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip().rstrip(".")


def lint(doc: dict) -> list[dict]:
    issues = []
    locks = doc.get("locks", {}) or {}
    if not locks.get("character") and not locks.get("style"):
        issues.append({"severity": "REVISE", "code": "no_locks", "msg": "لا أقفال؛ بدون Character/Style Lock تنجرف الهوية بين اللقطات"})
    blob = json.dumps(doc, ensure_ascii=False).lower()
    if re.search(r"\b(elon musk|donald trump|messi|ronaldo|taylor swift|mr ?beast)\b", blob):
        issues.append({"severity": "BLOCK", "code": "real_person", "msg": "شخص حقيقي؛ ممنوع (تزييف)"})
    for s in doc.get("shots", []):
        cams = set(m.lower() for m in re.findall(CAMERA_WORDS, clean(s.get("camera")).lower()))
        cams.discard("static"); cams.discard("locked-off"); cams.discard("locked off")
        if len(cams) > 1:
            issues.append({"severity": "REVISE", "code": "multi_camera", "msg": f"اللقطة {s.get('n')}: حركتا كاميرا ({', '.join(sorted(cams))}); واحدة فقط"})
        if not clean(s.get("action")):
            issues.append({"severity": "REVISE", "code": "no_action", "msg": f"اللقطة {s.get('n')}: لا فعل عبر الزمن"})
        d = float(s.get("duration", 0) or 0)
        if d <= 0:
            issues.append({"severity": "REVISE", "code": "no_duration", "msg": f"اللقطة {s.get('n')}: لا مدة"})
    return issues


def shot_text(doc: dict, s: dict, platform: str) -> str:
    L = doc.get("locks", {}) or {}
    parts = []
    if L.get("character"):
        parts.append(clean(L["character"]))
    if L.get("location"):
        parts.append(clean(L["location"]))
    parts.append(clean(s.get("action")))
    cam = clean(s.get("camera"))
    if cam:
        parts.append(f"camera: {cam}" + (f", {clean(s['lens'])} lens" if s.get("lens") else ""))
    for k in ("lighting", "environment_motion", "grade"):
        if clean(s.get(k)):
            parts.append(clean(s[k]))
    if L.get("style"):
        parts.append(clean(L["style"]))
    dur = min(float(s.get("duration", 5) or 5), LIMITS.get(platform, 10))
    fps = doc.get("fps", 24)
    aspect = doc.get("aspect", "16:9")
    body = ". ".join(p[:1].upper() + p[1:] for p in parts if p) + "."
    if platform == "veo":
        return f"{body} Duration {dur:g} seconds, {aspect}, {fps} fps, natural motion, no on-screen text."
    if platform == "sora":
        return f"{body} {dur:g}-second continuous shot, {aspect}. Keep the subject's identity consistent; realistic physics; no text or logos."
    if platform == "kling":
        return f"{body} Length {dur:g}s, ratio {aspect}, motion: moderate, camera as described only. Negative: text, logo, extra limbs, flicker."
    if platform == "runway":
        return f"[{cam or 'static camera'}] {body} {aspect}, {dur:g}s. Consistent character; cinematic; no text."
    if platform in ("luma", "pika", "hailuo"):
        return f"{body} {dur:g}s, {aspect}. No text, no watermark, stable identity."
    return body


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("shots")
    ap.add_argument("--platforms", default="veo,sora,kling,runway")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    doc = json.load(open(a.shots, encoding="utf-8"))
    issues = lint(doc)
    plats = [p for p in a.platforms.split(",") if p in LIMITS]
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    md = ["# برومبتات الفيديو لقطة بلقطة", "", "| # | المدة | الكاميرا | الفعل |", "|---|---|---|---|"]
    for s in doc.get("shots", []):
        md.append(f"| {s.get('n')} | {s.get('duration')}s | {clean(s.get('camera'))} | {clean(s.get('action'))[:70]} |")
    md.append("")
    for s in doc.get("shots", []):
        md += [f"## اللقطة {s.get('n')}", ""]
        for p in plats:
            md += [f"**{p}**", "```", shot_text(doc, s, p), "```", ""]
    md += ["## الفحص", ""] + ([f"- [{i['severity']}] {i['code']}: {i['msg']}" for i in issues] or ["- PASS"])
    md += ["", "## QA بعد التوليد (لكل لقطة)", "- انجراف الهوية؟ الأيدي والوجوه؟ الفيزياء؟ نص غريب؟ استمرارية الملابس والإضاءة؟ ← أعد اللقطة الفاشلة فقط."]
    text = "\n".join(md)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text + "\n")
    print(text)
    sys.exit(3 if any(i["severity"] == "BLOCK" for i in issues) else 1 if issues else 0)


if __name__ == "__main__":
    main()
