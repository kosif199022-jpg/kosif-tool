#!/usr/bin/env python3
"""مواصفة صورة واحدة (JSON) → برومبت مضبوط لكل منصة (Midjourney، Flux، SDXL، DALL·E/ChatGPT، Ideogram، NanoBanana) + فحص.

usage:
  python image_prompt_forge.py spec.json [--platforms midjourney,flux,sdxl,chatgpt,ideogram,nanobanana] [--out prompts.md]
spec.json (القيم بالإنجليزية لأن المولّدات تفهمها أدق؛ `text` وحده قد يكون عربياً لأنه يُرسم على الصورة):
{
 "subject": "a Saudi barista in a linen apron", "action": "pouring latte art",
 "environment": "minimal cafe with palm-wood counter", "time": "early morning",
 "shot": "medium close-up", "angle": "eye level", "lens": "85mm f/1.8",
 "lighting": "soft window key from camera left, warm 3800K, gentle fill", "palette": "cream, walnut, sage green",
 "style": "photorealistic editorial", "materials": "linen texture, ceramic glaze",
 "mood": "calm, inviting", "aspect": "4:5", "text": "صباح الخير",
 "negative": ["text artifacts", "extra fingers", "watermark"],
 "locks": {"character": "Layla, 28, warm olive skin, short curly hair, round glasses", "style": "", "location": ""}
}
الفحص يكشف: حقولاً ناقصة، وتناقض الإضاءة (مصدران)، وعدستين، وأسماء فنانين أحياء، ونسبة غير مدعومة.
"""
import argparse
import json
import re
import sys

FIELDS = ["subject", "action", "environment", "time", "shot", "angle", "lens", "lighting", "palette", "style", "materials", "mood"]
REQUIRED = ["subject", "environment", "shot", "lighting", "style", "aspect"]
MJ_AR = {"1:1", "4:5", "5:4", "3:2", "2:3", "16:9", "9:16", "4:3", "3:4", "21:9", "7:4", "4:7"}
LIVING_ARTISTS = r"\b(greg rutkowski|artgerm|loish|wlop|beeple|james jean|ross tran|ilya kuvshinov|sakimichan)\b"
LIGHT_SOURCES = r"\b(window|sun|sunset|sunrise|neon|candle|moon|studio|softbox|ring light|lamp|fire|overcast|golden hour|blue hour)\b"


def clean(s) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip().rstrip(".")


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def lint(spec: dict) -> list[dict]:
    issues = []
    for k in REQUIRED:
        if not clean(spec.get(k)):
            issues.append({"severity": "REVISE", "code": f"missing_{k}", "msg": f"الحقل {k} ناقص"})
    lights = set(re.findall(LIGHT_SOURCES, clean(spec.get("lighting")).lower()))
    if len(lights) > 2:
        issues.append({"severity": "REVISE", "code": "lighting_conflict", "msg": f"مصادر ضوء كثيرة ({', '.join(sorted(lights))}); مفتاح واحد واتجاه واحد"})
    if len(re.findall(r"\b\d{2,3}mm\b", json.dumps(spec))) > 1:
        issues.append({"severity": "REVISE", "code": "two_lenses", "msg": "أكثر من عدسة واحدة في المواصفة"})
    blob = json.dumps(spec, ensure_ascii=False).lower()
    if re.search(LIVING_ARTISTS, blob):
        issues.append({"severity": "BLOCK", "code": "living_artist", "msg": "اسم فنان حيّ؛ صِف الخصائص (brushwork, palette, era) بدل الاسم"})
    if re.search(r"\b(photo of|portrait of) (elon|trump|messi|ronaldo|taylor swift)\b", blob):
        issues.append({"severity": "BLOCK", "code": "real_person", "msg": "شخص حقيقي؛ ممنوع"})
    if spec.get("aspect") and spec["aspect"] not in MJ_AR:
        issues.append({"severity": "REVISE", "code": "aspect", "msg": f"نسبة غير شائعة {spec['aspect']}؛ المدعومة: {', '.join(sorted(MJ_AR))}"})
    if not spec.get("negative"):
        issues.append({"severity": "REVISE", "code": "no_negative", "msg": "لا قيود سلبية؛ أضف على الأقل: text artifacts, extra limbs, watermark"})
    if spec.get("text") and re.search(r"[؀-ۿ]", spec["text"]):
        issues.append({"severity": "INFO", "code": "arabic_text", "msg": "نص عربي على الصورة: Ideogram وChatGPT أفضل؛ Midjourney/SDXL يشوّهان الحروف العربية غالباً"})
    return issues


def core(spec: dict) -> list[str]:
    parts = []
    locks = spec.get("locks", {}) or {}
    subj = clean(spec.get("subject"))
    if locks.get("character") and locks["character"].lower() not in subj.lower():
        subj = f"{subj} ({clean(locks['character'])})"
    parts.append(subj)
    for k in ("action", "environment", "time"):
        if clean(spec.get(k)):
            parts.append(clean(spec[k]))
    cam = ", ".join(clean(spec.get(k)) for k in ("shot", "angle", "lens") if clean(spec.get(k)))
    if cam:
        parts.append(cam)
    for k in ("lighting", "materials", "palette", "mood"):
        if clean(spec.get(k)):
            parts.append(clean(spec[k]))
    style = clean(spec.get("style"))
    if locks.get("style"):
        style = f"{style}, {clean(locks['style'])}" if style else clean(locks["style"])
    if style:
        parts.append(style)
    if locks.get("location"):
        parts.append(clean(locks["location"]))
    return parts


def midjourney(spec: dict) -> str:
    p = ", ".join(core(spec))
    if spec.get("text"):
        p += f', the text "{spec["text"]}"'
    neg = ", ".join(spec.get("negative", []))
    ar = spec.get("aspect", "1:1")
    out = f"{p} --ar {ar} --s 200 --v 7"
    if neg:
        out += f" --no {neg}"
    return out


def flux(spec: dict) -> str:
    c = core(spec)
    s = f"{cap(c[0])}"
    if len(c) > 1:
        s += ", " + ", ".join(c[1:3]) + ". "
    s += " ".join(cap(x) + "." for x in c[3:])
    if spec.get("text"):
        s += f' The image includes the text "{spec["text"]}" rendered clearly.'
    if spec.get("negative"):
        s += " Avoid: " + ", ".join(spec["negative"]) + "."
    return s.strip()


def sdxl(spec: dict) -> dict:
    c = core(spec)
    weighted = [f"({c[0]}:1.3)"] + c[1:]
    pos = ", ".join(weighted) + ", highly detailed, sharp focus"
    neg = ", ".join(spec.get("negative", []) + ["lowres", "blurry", "deformed", "bad anatomy", "jpeg artifacts"])
    w, h = {"1:1": (1024, 1024), "4:5": (896, 1120), "5:4": (1120, 896), "3:2": (1216, 832), "2:3": (832, 1216),
            "16:9": (1344, 768), "9:16": (768, 1344), "4:3": (1152, 896), "3:4": (896, 1152)}.get(spec.get("aspect", "1:1"), (1024, 1024))
    return {"prompt": pos, "negative_prompt": neg, "width": w, "height": h, "steps": 30, "cfg": 6.0}


def chatgpt(spec: dict) -> str:
    c = core(spec)
    rules = ["Create one single image.", f"Aspect ratio {spec.get('aspect', '1:1')}."]
    if spec.get("negative"):
        rules.append("Do not include: " + ", ".join(spec["negative"]) + ".")
    body = f"Subject: {c[0]}. " + " ".join(cap(x) + "." for x in c[1:])
    if spec.get("text"):
        body += f' Render the exact text "{spec["text"]}" legibly with correct letterforms; no other text.'
    return " ".join(rules) + " " + body


def ideogram(spec: dict) -> str:
    c = core(spec)
    s = ", ".join(c)
    if spec.get("text"):
        s = f'Text "{spec["text"]}" in a clean legible typeface, {s}'
    return s + f" --ar {spec.get('aspect', '1:1')}"


def nanobanana(spec: dict) -> str:
    c = core(spec)
    s = "Generate a single photorealistic-quality image. " + cap(c[0]) + ". " + " ".join(cap(x) + "." for x in c[1:])
    if spec.get("text"):
        s += f' Include the text "{spec["text"]}" exactly as written.'
    s += f" Aspect ratio {spec.get('aspect', '1:1')}."
    if spec.get("negative"):
        s += " Exclude: " + ", ".join(spec["negative"]) + "."
    return s


BUILDERS = {"midjourney": midjourney, "flux": flux, "sdxl": sdxl, "chatgpt": chatgpt, "ideogram": ideogram, "nanobanana": nanobanana}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--platforms", default=",".join(BUILDERS))
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    issues = lint(spec)
    prompts = {p: BUILDERS[p](spec) for p in a.platforms.split(",") if p in BUILDERS}
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    md = ["# برومبتات الصورة", ""]
    for p, v in prompts.items():
        md += [f"## {p}", "```" + ("json" if isinstance(v, dict) else ""), json.dumps(v, ensure_ascii=False, indent=1) if isinstance(v, dict) else v, "```", ""]
    md += ["## الفحص", ""] + ([f"- [{i['severity']}] {i['code']}: {i['msg']}" for i in issues] or ["- PASS: لا مشكلات"])
    text = "\n".join(md)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text + "\n")
    print(text)
    sys.exit(3 if any(i["severity"] == "BLOCK" for i in issues) else 1 if any(i["severity"] == "REVISE" for i in issues) else 0)


if __name__ == "__main__":
    main()
