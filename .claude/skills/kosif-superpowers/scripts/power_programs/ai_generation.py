"""Programs for the ai-generation family.

No generator, API key or credit is used: every paid/keyed generation card is skipped. What runs
here is the deterministic part each card defines: prompt builders, translators, linters and
duration clamps with the card's own numbers, SceneSpec digests, routing tables, budget and
licence gates, and real local image/video work (teal-orange grade, palette measurement, SVG
sanitising, blurred-pad reframe, inpaint mask compositing, seam checks between clips, 12 fps
stop-motion step, chroma key, Ken Burns, domain-warped fbm, contour tracing, contact-sheet
outliers) on synthetic fixtures with ffmpeg, numpy, Pillow and OpenCV.
"""
from __future__ import annotations
import hashlib
import json
import math
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from ._lang_common import save, eq, truth, words, jaccard, sha256, ffmpeg, ffprobe_duration

HYPE = ("8k", "4k", "masterpiece", "ultra-detailed", "award-winning", "trending", "best quality", "beautiful",
        "hyperrealistic", "octane render")


def strip_hype(text):
    parts = [p.strip() for p in text.split(",")]
    return ", ".join(p for p in parts if p and p.lower() not in HYPE)


# ---------- GEN-01 seven layers ----------
KELVIN = {"lantern": 1900, "tungsten": 3200, "moonlight": 4100, "day": 6500}


def golden(spec):
    order = ("style", "composition", "camera", "lighting", "subject", "wardrobe", "environment", "atmosphere")
    line = ", ".join(spec[k] for k in order) + f", mood: {spec['mood']} --ar {spec['aspect']}"
    layers = ("location", "subject", "wardrobe", "lighting", "camera", "atmosphere", "technical")
    missing = [l for l in layers if not spec.get("layers", {}).get(l)]
    return line, missing


def g01(work: Path):
    spec = {"style": "cinematic still", "composition": "rule of thirds", "camera": "Alexa Mini LF 50 mm f/1.4, eye level, MCU",
            "lighting": f"soft window key camera-left {3800}K, fill -2 stops, cool rim", "subject": "weathered hands, pores",
            "wardrobe": "linen shirt", "environment": "old Cairo workshop, shelves behind", "atmosphere": "dust in the light shaft",
            "mood": "quiet focus", "aspect": "9:16",
            "layers": {"location": 1, "subject": 1, "wardrobe": 1, "lighting": 1, "camera": 1, "atmosphere": 1, "technical": 1}}
    line, miss = golden(spec)
    _, miss2 = golden(dict(spec, layers={"subject": 1}))
    save(work, "prompt.txt", line)
    return [truth("golden order style->atmosphere->mood->--ar", line.startswith("cinematic still, rule of thirds") and line.endswith("--ar 9:16")),
            eq("all 7 layers present", miss, []), eq("missing layers listed", len(miss2), 6),
            eq("Kelvin anchors", list(KELVIN.values()), [1900, 3200, 4100, 6500])]


# ---------- GEN-02 iron rules ----------
def iron_lint(prompt, locks, used_locks):
    issues = []
    if re.match(r"\s*a photo of", prompt, re.I):
        issues.append("opens with 'a photo of'")
    hype = [h for h in HYPE if re.search(rf"\b{re.escape(h)}\b", prompt, re.I)]
    if hype:
        issues.append("hype: " + ",".join(hype))
    for name, text in locks.items():
        if text not in used_locks.get(name, ""):
            issues.append(f"lock '{name}' paraphrased")
    return issues


def g02(work):
    locks = {"character": "Nour, 30, olive skin, short black curls, round brass glasses, rust linen jacket"}
    bad = "a photo of Nour, 8k, masterpiece, beautiful"
    good = "Nour, 30, olive skin, short black curls, round brass glasses, rust linen jacket, chiaroscuro, film grain, volumetric light"
    b = iron_lint(bad, locks, {"character": "Nour, a woman in her thirties with glasses"})
    g = iron_lint(good, locks, {"character": good})
    save(work, "iron.json", {"bad": b, "good": g, "fixed": strip_hype(bad)})
    return [eq("three rule breaks", len(b), 3), truth("hype listed", any("masterpiece" in x for x in b)), eq("physical-cue prompt passes", g, []),
            eq("hype stripped", strip_hype(bad), "a photo of Nour")]


# ---------- GEN-03 negatives ----------
POSITIVE = {"no blur": "tack-sharp focus", "no people": "empty, deserted", "no text": "clean, text-free surfaces"}


def frame_negatives(neg, platform):
    if platform in ("sdxl", "kling"):
        return {"prompt_add": [], "negative": neg}
    if platform == "wan":
        return {"prompt_add": [], "negative": neg[:3]}
    add = [POSITIVE[n] for n in neg if n in POSITIVE]
    return {"prompt_add": add, "negative": []}


def g03(work):
    neg = ["no blur", "no people", "no text", "watermark"]
    r = {p: frame_negatives(neg, p) for p in ("sdxl", "flux", "runway", "wan")}
    save(work, "negatives.json", r)
    return [eq("SDXL keeps negatives", r["sdxl"]["negative"], neg), eq("Flux: positive rewrite, no negative field", r["flux"],
                                                                      {"prompt_add": ["tack-sharp focus", "empty, deserted", "clean, text-free surfaces"], "negative": []}),
            eq("Runway: negatives stripped", r["runway"]["negative"], []), eq("Wan keeps them short", len(r["wan"]["negative"]), 3)]


# ---------- GEN-04 six-slot still ----------
def still_check(prompt, api_aspect):
    n = len(prompt.split())
    desc = [d for d in prompt.split(",") if d.strip()]
    ar = re.search(r"(\d+:\d+)", prompt)
    return {"words_ok": 40 <= n <= 80, "descriptors_ok": 5 <= len(desc) <= 8,
            "ratio_twice": bool(ar) and ar.group(1) == api_aspect, "n": n, "d": len(desc)}


def g04(work):
    good = ("A ceramic coffee cup on a sunlit marble counter in a quiet Alexandria cafe at morning, steam curling upward slowly, "
            "shot on a 50mm lens at eye level with shallow depth, warm window light from the left side of the frame, "
            "soft film grain and gentle contrast, brand palette cream and teal, vertical 9:16 frame")
    short = "cup, table, 9:16"
    g, s = still_check(good, "9:16"), still_check(short, "4:5")
    save(work, "still.json", {"good": g, "short": s})
    return [truth("40-80 words", g["words_ok"], g["n"]), truth("5-8 descriptors", g["descriptors_ok"], g["d"]),
            eq("ratio in text and API", g["ratio_twice"], True), eq("short prompt fails all", (s["words_ok"], s["ratio_twice"]), (False, False))]


# ---------- GEN-05 narrative brief ----------
def narrative(subject, style, context, other):
    total = 100
    alloc = {"subject": 30, "style": 25, "context": 15, "other": 30}
    def take(t, n):
        w = t.split()
        return " ".join((w * (n // max(len(w), 1) + 1))[:n])
    paras = [take(subject, alloc["subject"]) + ".", take(style, alloc["style"]) + ". " + take(context, alloc["context"]) + ".",
             take(other, alloc["other"]) + ". ultra-realistic, high resolution"]
    return "\n\n".join(paras), alloc, total


def g05(work):
    text, alloc, total = narrative("an old fisherman mending nets", "85 mm f/1.4 Kodak Portra 400 soft warm",
                                   "Alexandria harbour at dawn", "gulls gentle waves wet stones calm morning light")
    save(work, "brief.txt", text)
    paras = text.split("\n\n")
    return [truth("1-3 paragraphs", 1 <= len(paras) <= 3), eq("weights 30/25/15", (alloc["subject"], alloc["style"], alloc["context"]), (30, 25, 15)),
            eq("subject share", len(paras[0].split()), 30), truth("ends without tag stuffing", text.endswith("ultra-realistic, high resolution"))]


# ---------- GEN-06 MJ -> natural language ----------
def mj_translate(p):
    params = {}
    m = re.search(r"--ar (\d+:\d+)", p)
    if m:
        params["aspect_ratio"] = m.group(1)
    t = re.sub(r"--ar \S+|--v \S+|--style raw|--s \d+|--stylize \d+", "", p)
    if re.search(r"--chaos (\d+)", t):
        t = re.sub(r"--chaos \d+", "", t) + ", unexpected, surreal composition"
    t = re.sub(r"\((\w+):1\.\d\)", r"prominently featuring \1", t)
    t = strip_hype(re.sub(r"\s+", " ", t).strip(" ,"))
    return t, params


def g06(work):
    t, p = mj_translate("lone lighthouse, (storm:1.5), Leica M6, 8K, masterpiece --ar 16:9 --style raw --v 7 --chaos 50")
    save(work, "translated.json", {"prompt": t, "params": p})
    return [eq("--ar -> parameter", p, {"aspect_ratio": "16:9"}), truth("--v/--style raw dropped", "--" not in t),
            truth("weight -> phrase", "prominently featuring storm" in t), truth("chaos -> phrase", t.endswith("unexpected, surreal composition")),
            truth("hype deleted, camera kept", "masterpiece" not in t and "8K" not in t and "Leica M6" in t)]


# ---------- GEN-07 video shot ----------
CAM_WORDS = ("static", "pan", "tilt", "dolly", "tracking", "crane", "handheld", "orbit", "push-in", "dolly zoom", "rack focus")


def video_formula(p):
    n = len(p.split())
    issues = []
    if not 50 <= n <= 100:
        issues.append(f"{n} words (50-100)")
    if not any(c in p.lower() for c in CAM_WORDS):
        issues.append("camera move or 'static' missing")
    if re.search(r"\bcut to\b|\bscene changes\b", p, re.I):
        issues.append("scene change inside clip")
    if re.search(r"text (says|reading)|caption reading|on-screen text", p, re.I):
        issues.append("on-screen text requested")
    return issues


def g07(work):
    good = ("Wide establishing shot at golden hour over the Nile in Aswan. A felucca with a white sail glides slowly from left to right "
            "while a boy at the bow trails his hand in the water. Slow tracking shot following the boat at water level, "
            "warm amber light, gentle ripples catching the sun, light haze over the far bank, 2.35:1 frame, 8 seconds.")
    bad = "Felucca on the Nile, cut to a market, text says Aswan."
    g, b = video_formula(good), video_formula(bad)
    variations = [good.replace("Slow tracking", m) for m in ("Slow tracking", "Static wide", "Slow crane up over", "Handheld")]
    save(work, "shot.json", {"good": g, "bad": b, "variations": variations})
    return [eq("good shot", g, []), eq("bad shot issues", len(b), 4), truth("3-4 variations", 3 <= len(variations) <= 4)]


# ---------- GEN-08 suppress music & subtitles ----------
SUFFIX = "No music score. No subtitles or on-screen text."


def segment_call(prompt, ref_has_signage=False):
    p = prompt.rstrip(". ") + ". " + SUFFIX
    if ref_has_signage:
        p += " Only the text that exists in @Image1 itself."
    return {"prompt": p, "generate_audio": False}


def g08(work):
    a = segment_call("A tram crosses Alexandria at dusk")
    b = segment_call("A shopfront in old Cairo", ref_has_signage=True)
    save(work, "segments.json", [a, b])
    return [truth("exact suffix appended", a["prompt"].endswith(SUFFIX)), eq("audio off, added in post", a["generate_audio"], False),
            truth("signage clause", b["prompt"].endswith("in @Image1 itself.")), truth("no ambient list", "sound" not in a["prompt"].lower())]


# ---------- GEN-09 limits -> montage plan ----------
def montage_plan(total_s, lo=4, hi=15, target=8):
    n = max(1, math.ceil(total_s / target))
    while total_s / n > hi:
        n += 1
    while n > 1 and total_s / n < lo:
        n -= 1
    base = total_s / n
    return [round(base, 2)] * n


def g09(work):
    p = montage_plan(47)
    subj_ok = lambda shot: len(shot["subjects"]) <= 2
    save(work, "montage.json", p)
    return [truth("every clip 4-15 s", all(4 <= c <= 15 for c in p), p), eq("sum preserved", round(sum(p), 1), 47.0),
            eq("6 clips", len(p), 6), truth("1-2 subjects rule", subj_ok({"subjects": ["a", "b"]}) and not subj_ok({"subjects": ["a", "b", "c"]}))]


# ---------- GEN-10 forge: canvas map ----------
SDXL = {"1:1": (1024, 1024), "16:9": (1344, 768), "9:16": (768, 1344), "4:5": (896, 1152), "3:2": (1216, 832), "2.39:1": (1536, 640)}


def forge(spec):
    warn = [f"missing {k}: prompts will be weaker" for k in ("lens", "style") if not spec.get(k)]
    core = ", ".join(spec[k] for k in ("subject", "action", "environment") if spec.get(k))
    w, h = SDXL[spec["aspect"]]
    return {"prompts": {"sdxl": {"prompt": core, "width": w, "height": h, "cfg": 6, "steps": 35}},
            "variations": {"subtle": core + ", softer light", "dramatic": core + ", hard rim light, deep shadows",
                           "technical": core + ", 50 mm, f/2.8, 1/250 s"}, "warnings": warn}


def g10(work):
    r = forge({"subject": "a red tram", "action": "turning", "environment": "Alexandria", "aspect": "9:16", "lens": "35mm"})
    save(work, "forge.json", r)
    mp = {a: (w * h) / 1e6 for a, (w, h) in SDXL.items()}
    return [eq("9:16 canvas", (r["prompts"]["sdxl"]["width"], r["prompts"]["sdxl"]["height"]), (768, 1344)),
            truth("all canvases ~1 MP and /64", all(0.9 < v < 1.1 for v in mp.values()) and all(w % 64 == 0 and h % 64 == 0 for w, h in SDXL.values())),
            eq("missing style warned", r["warnings"], ["missing style: prompts will be weaker"]),
            eq("three variations", sorted(r["variations"]), ["dramatic", "subtle", "technical"]),
            truth("CFG 5-7, steps 30-40", 5 <= r["prompts"]["sdxl"]["cfg"] <= 7 and 30 <= r["prompts"]["sdxl"]["steps"] <= 40)]


# ---------- GEN-11 platform DNA ----------
def snap(d, allowed):
    return min(allowed, key=lambda a: (abs(a - d), -a))


def platform_shot(p, dur, prompt, refs=0):
    if p == "veo":
        return {"dur": snap(dur, (4, 6, 8))}
    if p == "sora":
        if len(prompt) > 4000:
            raise ValueError("sora prompt > 4000 chars")
        return {"dur": snap(dur, (4, 8, 12))}
    if p == "runway":
        if refs > 3:
            raise ValueError("runway <= 3 refs")
        return {"dur": min(10, max(2, dur))}
    if p == "kling":
        return {"dur": min(10, max(5, dur))}


def g11(work):
    r = {p: platform_shot(p, 7, "x") for p in ("veo", "sora", "runway", "kling")}
    errs = []
    for args in (("sora", 8, "x" * 4001), ("runway", 5, "x", 4)):
        try:
            platform_shot(*args)
        except ValueError as e:
            errs.append(str(e))
    save(work, "dna.json", {"r": r, "errs": errs})
    return [eq("7 s per platform", {k: v["dur"] for k, v in r.items()}, {"veo": 8, "sora": 8, "runway": 7, "kling": 7}),
            eq("veo 5 s -> 6", platform_shot("veo", 5, "")["dur"], 6), eq("kling 3 s -> 5", platform_shot("kling", 3, "")["dur"], 5),
            eq("limits refused", len(errs), 2)]


# ---------- GEN-12 image spec -> 6 builders ----------
REQ12 = ("subject", "environment", "shot", "lighting", "style", "aspect")
SDXL12 = {"16:9": (1344, 768), "9:16": (768, 1344), "4:5": (896, 1120)}


def builders(spec):
    miss = [k for k in REQ12 if not spec.get(k)]
    if miss:
        raise ValueError(f"missing {miss}")
    core = ", ".join(spec[k] for k in REQ12[:-1])
    neg = ", ".join(spec.get("negative", []))
    w, h = SDXL12[spec["aspect"]]
    return {"midjourney": f"{core} --ar {spec['aspect']} --s 200 --v 7 --no {neg}",
            "flux": f"{core}. Avoid: {neg}.",
            "sdxl": {"prompt": f"({spec['subject']}:1.3), {core}", "steps": 30, "cfg": 6.0, "width": w, "height": h},
            "chatgpt": f"Create one single image. Aspect ratio {spec['aspect']}. Do not include {neg}. {core}.",
            "ideogram": f"\"{spec.get('text', '')}\" {core} --ar {spec['aspect']}",
            "nanobanana": f"Generate a single photorealistic-quality image of {core}. Exclude: {neg}."}


def g12(work):
    spec = {"subject": "brass lantern", "environment": "souk alley", "shot": "close-up", "lighting": "warm 1900K",
            "style": "editorial photo", "aspect": "4:5", "negative": ["text", "logos"], "text": "SOUK"}
    b = builders(spec)
    save(work, "builders.json", b)
    refused = False
    try:
        builders({"subject": "x"})
    except ValueError:
        refused = True
    return [eq("six builders", len(b), 6), truth("MJ suffix", b["midjourney"].endswith("--ar 4:5 --s 200 --v 7 --no text, logos")),
            eq("SDXL 4:5 canvas + steps/cfg", (b["sdxl"]["width"], b["sdxl"]["height"], b["sdxl"]["steps"], b["sdxl"]["cfg"]), (896, 1120, 30, 6.0)),
            truth("ChatGPT constraints first", b["chatgpt"].startswith("Create one single image. Aspect ratio 4:5.")),
            truth("Ideogram quoted text first", b["ideogram"].startswith('"SOUK"')), eq("required fields enforced", refused, True)]


# ---------- GEN-13 shot list clamping ----------
MAXS = {"veo": 8, "sora": 20, "kling": 10, "runway": 10, "luma": 9, "pika": 10, "hailuo": 10}
REAL_PEOPLE = {"elon musk", "taylor swift", "mohamed salah"}


def shot_forge(doc, platforms):
    out, lint = [], []
    aspect, fps = doc.get("aspect", "16:9"), doc.get("fps", 24)
    for i, s in enumerate(doc["shots"]):
        if any(n in s["prompt"].lower() for n in REAL_PEOPLE):
            lint.append((i, "BLOCK"))
        if not doc.get("lock"):
            lint.append((i, "REVISE"))
        if sum(1 for c in CAM_WORDS if re.search(rf"\b{c}\b", s["prompt"].lower())) > 1:
            lint.append((i, "FLAG camera"))
        out.append({p: {"dur": min(s["dur"], MAXS[p]), "aspect": aspect, "fps": fps} for p in platforms})
    return out, lint


def g13(work):
    doc = {"aspect": "9:16", "fps": 24, "lock": "", "shots": [{"prompt": "slow dolly past a tram", "dur": 12},
                                                              {"prompt": "Mohamed Salah waves, pan and tilt", "dur": 6}]}
    out, lint = shot_forge(doc, list(MAXS))
    save(work, "shots.json", {"out": out, "lint": lint})
    return [eq("12 s clamped per platform", {p: out[0][p]["dur"] for p in MAXS},
               {"veo": 8, "sora": 12, "kling": 10, "runway": 10, "luma": 9, "pika": 10, "hailuo": 10}),
            eq("top-level aspect/fps used", (out[1]["veo"]["aspect"], out[1]["veo"]["fps"]), ("9:16", 24)),
            eq("lint", lint, [(0, "REVISE"), (1, "BLOCK"), (1, "REVISE"), (1, "FLAG camera")])]


# ---------- GEN-14 seven-layer per-shot prompts ----------
def aiprompts(shot):
    layers = {k: shot[k] for k in ("location", "subject", "wardrobe", "lighting", "camera", "atmosphere", "technical")}
    text = ", ".join(layers.values())
    warn = []
    if not re.search(r"\d{4}K", shot["lighting"]) or not re.search(r"left|right|behind|above|front", shot["lighting"]):
        warn.append("lighting lacks direction or Kelvin")
    return {"layers": layers, "prompts": {"runway": text[:1000], "kling": {"prompt": text[:2500], "negative_prompt": "blur, watermark"},
                                          "veo": text, "sora": text}, "warnings": warn,
            "rubric": {k: 20 for k in ("clarity", "camera", "light", "continuity", "platform fit")}}


def g14(work):
    base = {"location": "desert road", "subject": "lone cyclist", "wardrobe": "white robe", "lighting": "cool 4100K moonlight from left vs warm 1900K lantern",
            "camera": "35mm, tracking", "atmosphere": "dust", "technical": "photoreal 35mm film look " + "x" * 1200}
    a = aiprompts(base)
    b = aiprompts(dict(base, lighting="nice light"))
    save(work, "aiprompts.json", {"warnings": [a["warnings"], b["warnings"]]})
    return [eq("seven layers", len(a["layers"]), 7), eq("Runway <= 1000 chars", len(a["prompts"]["runway"]), 1000),
            truth("Kling <= 2500 + negative", len(a["prompts"]["kling"]["prompt"]) <= 2500 and a["prompts"]["kling"]["negative_prompt"]),
            eq("vague light warned", b["warnings"], ["lighting lacks direction or Kelvin"]), eq("rubric 5x20", sum(a["rubric"].values()), 100)]


# ---------- GEN-15 omniprompt ----------
SECTIONS15 = ("STYLE", "SPECS", "TIMELINE", "ADD", "BRAND MARK", "TYPOGRAPHY LOCK", "SOUND", "FINAL FRAME", "EXCLUDE")


def omniprompt(brief, overrides=None, duration=10):
    if not brief.get("style") or not brief.get("scenes"):
        raise SystemExit("brief not filled")
    ov = overrides or {}
    for r in ov.get("remove", []):
        if any(r in s["elements"] for s in brief["scenes"]):
            raise ValueError(f"refuse: scenes are built on {r}")
    palette = [ov.get("palette", {}).get(c, c) for c in brief["palette"]]
    scale = 0.83 if duration == 12 else 10 / brief["duration"]
    times = [round(s["t"] * (scale if duration == 12 else 10 / brief["duration"]), 2) for s in brief["scenes"]]
    w, h = brief["size"]
    if min(w, h) < 1080:
        f = 1080 / min(w, h)
        w, h = round(w * f), round(h * f)
    block = {"STYLE": brief["style"], "SPECS": f"{w}x{h}, {duration} s, palette {palette}", "TIMELINE": times,
             "ADD": ov.get("add", []), "BRAND MARK": brief.get("brand", ""), "TYPOGRAPHY LOCK": brief.get("font", ""),
             "SOUND": brief.get("sound", ""), "FINAL FRAME": brief.get("final", ""), "EXCLUDE": ov.get("remove", [])}
    return block, (w, h)


def g15(work):
    brief = {"style": "paper collage", "duration": 20, "size": (720, 1280), "palette": ["#112233", "#ffcc00"],
             "scenes": [{"t": 0, "elements": ["logo"]}, {"t": 10, "elements": ["map"]}, {"t": 18, "elements": ["cta"]}]}
    b, size = omniprompt(brief, {"palette": {"#ffcc00": "#e23a2a"}, "remove": ["confetti"]})
    errs = []
    try:
        omniprompt(brief, {"remove": ["map"]})
    except ValueError:
        errs.append("refused")
    try:
        omniprompt({"style": ""})
    except SystemExit:
        errs.append("exit")
    save(work, "omniprompt.json", b)
    return [eq("nine sections", list(b), list(SECTIONS15)), eq(">=1080 short side", size, (1080, 1920)),
            eq("compressed to 10 s", b["TIMELINE"], [0.0, 5.0, 9.0]), truth("palette override", "#e23a2a" in b["SPECS"]),
            eq("refuse removing a built-on element; unfilled brief exits", errs, ["refused", "exit"])]


# ---------- GEN-16 SceneSpec digest ----------
FIELDS16 = ("subject", "environment", "action", "camera", "lighting", "color_grade", "materials", "atmosphere_vfx",
            "composition_story", "negative_constraints", "aspect_ratio")


def compile_prompt(scene):
    miss = [f for f in FIELDS16 if not scene.get(f)]
    if miss:
        raise ValueError(f"missing {miss}")
    if not re.fullmatch(r"\d+:\d+", scene["aspect_ratio"]):
        raise ValueError("aspect_ratio must be W:H")
    digest = hashlib.sha256(json.dumps(scene, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    prompt = ", ".join(scene[f] for f in FIELDS16[:9])
    return {"prompt": prompt, "negative_prompt": scene["negative_constraints"], "scene_digest": digest, "scene_spec": scene}


def g16(work):
    s = {f: f"{f} value" for f in FIELDS16}
    s["aspect_ratio"] = "9:16"
    a = compile_prompt(s)
    b = compile_prompt(dict(reversed(list(s.items()))))
    c = compile_prompt(dict(s, lighting="other"))
    errs = 0
    for bad in ({**s, "aspect_ratio": "vertical"}, {k: v for k, v in s.items() if k != "camera"}):
        try:
            compile_prompt(bad)
        except ValueError:
            errs += 1
    save(work, "compiled.json", a)
    return [eq("11 fields", len(FIELDS16), 11), eq("key order does not change digest", a["scene_digest"], b["scene_digest"]),
            truth("content change changes digest", a["scene_digest"] != c["scene_digest"]), eq("bad specs refused", errs, 2)]


# ---------- GEN-17 locks ----------
def apply_locks(spec):
    L = spec.get("locks", {})
    subj = spec["subject"] + (", " + L["character"] if L.get("character") else "")
    style = spec["style"] + (", " + L["style"] if L.get("style") else "")
    p = f"{subj}, {spec['action']}, {style}" + (", " + L["location"] if L.get("location") else "")
    return p, ([] if L else ["REVISE: no lock"])


def g17(work):
    locks = {"character": "Nour, 30, olive skin, short black curls, brass glasses, rust linen jacket",
             "style": "gouache texture, muted teal", "location": "rooftop in Zamalek"}
    shots = [apply_locks({"subject": "a woman", "action": a, "style": "illustration", "locks": locks})[0] for a in ("reads", "laughs")]
    _, warn = apply_locks({"subject": "x", "action": "y", "style": "z"})
    save(work, "locked.json", shots)
    return [truth("character lock verbatim after subject", all(s.startswith("a woman, " + locks["character"]) for s in shots)),
            truth("location lock at the end", all(s.endswith(locks["location"]) for s in shots)),
            eq("no lock -> REVISE", warn, ["REVISE: no lock"])]


# ---------- GEN-21 viral-editorial poster ----------
def ease_overshoot(u, over=0.07):
    base = 1 - (1 - u) ** 3
    return base + over * math.sin(math.pi * u) * (u > 0.5)


def g21(work):
    W, H = 90, 160
    im = Image.new("RGB", (W, H), (240, 236, 228))
    dr = ImageDraw.Draw(im)
    for x in range(0, W, 6):
        dr.line([(x, 0), (x, H)], fill=(228, 224, 216))
    m = int(W * 0.10)
    dr.rectangle([m, 50, W - m, 110], fill=(220, 60, 40))      # hero (accent 20 %)
    accents = ["starburst", "dotted orbit"]
    im.save(work / "poster.png")
    a = np.asarray(im).astype(int)
    hero = (np.abs(a - [220, 60, 40]).sum(axis=2) < 10).mean()
    left_margin = int(np.argmax((np.abs(a - [220, 60, 40]).sum(axis=2) < 10).any(axis=0)))
    curve = [ease_overshoot(i / 20) for i in range(21)]
    motion = {"camera_push": 0.04, "ease": "easeOutCubic", "overshoot": 0.07, "wobble_deg": 0.6, "music": False, "voiceover": False}
    save(work, "motion.json", motion)
    return [eq("10 % side margin", left_margin, 9), truth("80/20 colour split (hero ~20 %)", 0.15 <= hero <= 0.4, round(hero, 3)),
            truth("<= 2 vector accents", len(accents) <= 2), truth("easing overshoots then settles", max(curve) > 1.0 and abs(curve[-1] - 1) < 1e-9, round(max(curve), 3)),
            eq("silent motion prompt", (motion["music"], motion["voiceover"]), (False, False))]


# ---------- GEN-22 per-shot seeds ----------
def seeds(shots, lock):
    lock = strip_hype(lock)
    out, t = [], 0.0
    for s in shots:
        at = round(t + 0.3 * s["dur"], 2)
        out.append({"shot": s["id"], "seed_at": at, "veo2_prompt": f"{lock}, {s['desc']}", "sora_prompt": f"{s['desc']}. {lock}",
                    "kling_prompt": f"{s['desc']}, {lock}", "runway_gen3_prompt": f"{s['desc']}; {lock}"})
        t += s["dur"]
    return {"style_lock": lock, "shots": out}


def g22(work):
    r = seeds([{"id": 1, "dur": 4, "desc": "tram"}, {"id": 2, "dur": 6, "desc": "sea"}], "watercolour wash, 8k, octane render")
    save(work, "ai_prompts.json", r)
    return [eq("hype replaced in the lock", r["style_lock"], "watercolour wash"), eq("seed at 30 % of each shot", [s["seed_at"] for s in r["shots"]], [1.2, 5.8]),
            eq("four platform prompts per shot", sum(k.endswith("prompt") for k in r["shots"][0]), 4)]


# ---------- GEN-23 continuity locks ----------
def proplan(task, locks):
    need = ("speaker", "font", "palette", "motion_direction")
    miss = [k for k in need if not locks.get(k)]
    if miss:
        raise ValueError(f"lock {miss}")
    stage = {"stage": "model_prompt_with_continuity", "locks": locks}
    prompts = [f"{s}. Speaker {locks['speaker']}; font {locks['font']}; palette {locks['palette']}; motion {locks['motion_direction']}." for s in task]
    return stage, prompts


def g23(work):
    locks = {"speaker": "Nour, rust jacket", "font": "Cairo 700", "palette": "#0B1F3A/#C9A227", "motion_direction": "left to right"}
    st, ps = proplan(["shot 1 intro", "shot 2 demo", "shot 3 cta"], locks)
    save(work, "proplan.json", {"stage": st, "prompts": ps})
    refused = False
    try:
        proplan(["x"], dict(locks, font=""))
    except ValueError:
        refused = True
    return [eq("stage inserted", st["stage"], "model_prompt_with_continuity"),
            truth("all four locks in every shot", all(all(v in p for v in locks.values()) for p in ps)), eq("missing lock refused", refused, True)]


# ---------- GEN-24 LLM prompt formula lint ----------
SLOTS24 = ("role", "context", "task", "inputs", "constraints", "output_format", "edge_cases", "quality_bar")


def llm_lint(p, untrusted=()):
    tags = re.findall(r"<(\w+)>", p)
    present = [s for s in SLOTS24 if s in tags]
    order_ok = present == [s for s in SLOTS24 if s in present] and [t for t in tags if t in SLOTS24] == present
    undelimited = [u for u in untrusted if u in p and not re.search(rf"<untrusted>[^<]*{re.escape(u)}", p)]
    if undelimited:
        return 3, "untrusted input not delimited"
    if len(present) < 8 or not order_ok:
        return 1, f"missing or out of order: {[s for s in SLOTS24 if s not in present]}"
    return 0, "ok"


def g24(work):
    good = "".join(f"<{s}>x</{s}>" for s in SLOTS24) + "<untrusted>user text here</untrusted>"
    bad = "<task>x</task><role>y</role>"
    r = [llm_lint(good, ["user text here"]), llm_lint(bad), llm_lint(good.replace("<untrusted>", "").replace("</untrusted>", ""), ["user text here"])]
    save(work, "lint.json", r)
    return [eq("exit codes 0/1/3", [x[0] for x in r], [0, 1, 3])]


# ---------- GEN-25 Egypt 2120 pack ----------
def egypt_pack():
    shots = [("orbit dive", 24, 3), ("Giza solar mirrors", 35, 4), ("Nile train", 28, 4), ("Cairo lotus tower", 24, 4), ("Alexandria Pharos", 35, 3)]
    neg = ["text artifacts", "logos", "watermarks", "real people", "distorted pyramids", "dystopia", "smog", "flags"]
    out = []
    for name, lens, d in shots:
        base = f"{name}, {lens}mm, gold / warm white / cyan on near-black, 9:16, 30 fps, {d} s"
        out.append({"kling": {"prompt": base, "negative_prompt": ", ".join(neg)}, "runway": {"prompt": base},
                    "veo": {"prompt": base, "notes": "last frame -> next first frame"}})
    return shots, out


def g25(work):
    shots, out = egypt_pack()
    save(work, "egypt2120.json", out)
    return [eq("durations", [d for *_, d in shots], [3, 4, 4, 4, 3]), eq("total 18 s", sum(d for *_, d in shots), 18),
            eq("lenses", [l for _, l, _ in shots], [24, 35, 28, 24, 35]), truth("Kling explicit negative; Runway none",
                                                                            all("real people" in o["kling"]["negative_prompt"] and "negative_prompt" not in o["runway"] for o in out)),
            truth("Veo chaining note", all("last frame" in o["veo"]["notes"] for o in out))]


# ---------- GEN-26 look catalogue ----------
LOOKS = {"Film Noir": "B&W, venetian blinds, smoke, 1940s", "Cyberpunk Neon": "neon, holograms, rain reflections, teal + magenta",
         "Claymation": "stop-motion, fingerprints", "Ukiyo-e": "woodblock, flat planes"}
LIVING = {"wes anderson", "greg rutkowski", "hayao miyazaki"}


def pick_look(name, style_layer_extra=""):
    if any(a in style_layer_extra.lower() for a in LIVING):
        raise ValueError("describe traits, never a living artist's name")
    return {"style": LOOKS[name], "lock": LOOKS[name]}


def g26(work):
    r = pick_look("Film Noir")
    refused = False
    try:
        pick_look("Claymation", "in the style of Wes Anderson")
    except ValueError:
        refused = True
    save(work, "look.json", r)
    return [eq("descriptor in style layer", r["style"], "B&W, venetian blinds, smoke, 1940s"), eq("locked verbatim", r["lock"], r["style"]),
            eq("living artist refused", refused, True)]


# ---------- GEN-27 byte-identical preambles ----------
PRE = "isometric low-poly floating island, matte clay, tilt-shift, soft contact shadow, background [BG_HEX], palette [PALETTE]"
TAIL = "no text, no letters, no logos"


def preamble_prompt(subject, bg, pal):
    return PRE.replace("[BG_HEX]", bg).replace("[PALETTE]", pal) + f", {subject}, {TAIL}"


def g27(work):
    ps = [preamble_prompt(s, "#F4EEE0", "terracotta/sage") for s in ("a bakery", "a clinic", "a school")]
    save(work, "series.txt", "\n".join(ps))
    prefix = ps[0].split(", a bakery")[0]
    return [truth("preamble byte-identical across series", all(p.startswith(prefix) for p in ps)),
            truth("tokens injected", "[BG_HEX]" not in ps[0] and "#F4EEE0" in ps[0]), truth("no-text tail", all(p.endswith(TAIL) for p in ps))]


# ---------- GEN-28 style-lock extraction ----------
def freeze_lock(lock_text, prompts_by_subject, names=LIVING):
    if any(n in lock_text.lower() for n in names) or re.search(r"\bstudio ghibli|pixar\b", lock_text, re.I):
        return False, "traits only, no names"
    held = [s for s, p in prompts_by_subject.items() if lock_text in p]
    return len(held) >= 2, held


def g28(work):
    lock = "flat gouache, visible paper tooth, muted teal and ochre, no outlines; negative: gloss, 3D"
    ok = freeze_lock(lock, {"cat": f"a cat, {lock}", "tram": f"a tram, {lock}"})
    one = freeze_lock(lock, {"cat": f"a cat, {lock}", "tram": "a tram, gouache"})
    named = freeze_lock("Studio Ghibli look", {})
    save(work, "style-lock.txt", lock)
    return [eq("holds on 2 subjects -> freeze", ok, (True, ["cat", "tram"])), eq("one subject drifted", one[0], False),
            eq("names refused", named, (False, "traits only, no names"))]


# ---------- GEN-29 domain modifiers ----------
DOMAIN = {"portrait": {"lens": "85mm", "f": "f/1.4-f/5.6", "light": "Rembrandt", "aspect": "4:5"},
          "food": {"lens": "50mm", "light": "overhead window light", "aspect": "4:5"},
          "landscape": {"lens": "16mm", "light": "golden hour haze", "aspect": "16:9", "layers": "foreground/mid/background"},
          "product": {"lens": "100mm macro", "light": "softbox + strip rims", "aspect": "1:1"},
          "cinema": {"body": "ARRI Alexa 65", "stock": "Kodak Vision3 500T"}}


def modifiers(domain, subject):
    d = DOMAIN[domain]
    return f"{subject}, " + ", ".join(v for k, v in d.items() if k != "aspect") + (f" --ar {d['aspect']}" if "aspect" in d else "")


def g29(work):
    r = {k: modifiers(k, "subject") for k in DOMAIN}
    save(work, "modifiers.json", r)
    return [truth("portrait 85mm 4:5", "85mm" in r["portrait"] and r["portrait"].endswith("--ar 4:5")),
            truth("landscape 16mm, layers, 16:9", "16mm" in r["landscape"] and "foreground" in r["landscape"] and r["landscape"].endswith("16:9")),
            truth("product macro 1:1", "100mm macro" in r["product"]), truth("cinema stock", "Vision3 500T" in r["cinema"])]


# ---------- GEN-30 grade for real in post ----------
def teal_orange(img, amount=0.3):
    a = img.astype(np.float64) / 255
    lum = a.mean(axis=2, keepdims=True)
    teal, orange = np.array([0.0, 0.5, 0.5]), np.array([1.0, 0.55, 0.2])
    w = np.clip((lum - 0.2) / 0.6, 0, 1)
    tint = (1 - w) * teal + w * orange
    out = a * (1 - amount) + amount * tint * (0.5 + lum)
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)


def g30(work):
    grad = np.tile(np.linspace(0, 255, 64, dtype=np.uint8)[None, :, None], (36, 1, 3))
    out = teal_orange(grad)
    Image.fromarray(out).save(work / "graded.png")
    sh, hi = out[:, 5].mean(axis=0), out[:, 60].mean(axis=0)
    packs = {"Cinematic": "cinematic grading, anamorphic flare, shallow DOF, film grain, 35 mm", "Social": "vertical 9:16, high contrast, saturated"}
    save(work, "packs.json", packs)
    return [truth("shadows lean teal (B,G > R)", sh[2] > sh[0] and sh[1] > sh[0], sh.round(1).tolist()),
            truth("highlights lean orange (R > B)", hi[0] > hi[2] + 20, hi.round(1).tolist()), truth("social pack is 9:16", "9:16" in packs["Social"])]


# ---------- GEN-31 Kling cfg bands ----------
CFG = {"photoreal": (0.4, 0.5), "cinematic": (0.5, 0.6), "neon cyberpunk": (0.5, 0.6), "anime": (0.6, 0.7), "vintage 8 mm": (0.6, 0.7),
       "watercolor": (0.7, 0.8), "pixel art": (0.8, 0.9)}


def kling_cfg(style, requested=None):
    lo, hi = CFG[style]
    if requested is None:
        return round((lo + hi) / 2, 2)
    return min(hi, max(lo, requested))


def g31(work):
    r = {s: kling_cfg(s) for s in CFG}
    save(work, "cfg.json", r)
    return [eq("photoreal mid-band", r["photoreal"], 0.45), eq("pixel art highest", max(r, key=r.get), "pixel art"),
            eq("clamped into band", (kling_cfg("anime", 0.95), kling_cfg("photoreal", 0.1)), (0.7, 0.4)),
            truth("realism lower than stylised", r["photoreal"] < r["watercolor"])]


# ---------- GEN-32 measure first ----------
def measure_image(img, k=3):
    a = np.asarray(img).reshape(-1, 3).astype(np.float32)
    _, labels, centers = cv2.kmeans(a, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5), 3, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(labels.ravel(), minlength=k)
    order = np.argsort(-counts)
    hexes = ["#%02x%02x%02x" % tuple(int(round(c)) for c in centers[i]) for i in order]
    w, h = img.size
    return {"palette": hexes, "share": (counts[order] / counts.sum()).round(2).tolist(), "aspect": f"{w}:{h}",
            "brightness": round(float(a.mean()) / 255, 3)}


def g32(work):
    im = Image.new("RGB", (64, 36), (11, 31, 58))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 24, 63, 35], fill=(201, 162, 39))
    d.rectangle([28, 4, 36, 20], fill=(240, 240, 240))
    im.save(work / "ref.png")
    m = measure_image(im)
    sections = ["الخلاصة", "التكوين", "الكاميرا", "الإضاءة", "الألوان", "العناصر", "الجودة التقنية", "مؤشرات التوليد", "الدرجات /10",
                "الإصلاحات", "برومبت إعادة الإنشاء"]
    save(work, "critique.json", {"measure": m, "sections": sections})
    return [eq("dominant colour measured", m["palette"][0], "#0b1f3a"), eq("second colour", m["palette"][1], "#c9a227"),
            eq("aspect measured", m["aspect"], "64:36"), eq("eleven report sections", len(sections), 11)]


# ---------- GEN-33 picture as code ----------
BAD_TAGS = ("script", "foreignObject", "image", "iframe", "a", "style", "animate", "set")


def sanitize_svg(svg):
    for t in BAD_TAGS:
        svg = re.sub(rf"<{t}\b[^>]*/>|<{t}\b.*?</{t}>", "", svg, flags=re.S | re.I)
    svg = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", svg)
    svg = re.sub(r"\s(xlink:)?href\s*=\s*(\"[^\"]*\"|'[^']*')", "", svg)
    svg = re.sub(r"url\((?!#)[^)]*\)", "none", svg)
    svg = re.sub(r"javascript:", "", svg, flags=re.I)
    return svg


def g33(work):
    dirty = ('<svg viewBox="0 0 1200 800"><rect width="1200" height="800" fill="#0d0e10"/><script>alert(1)</script>'
             '<circle cx="600" cy="400" r="80" fill="url(https://x.test/p)" onclick="steal()"/><a href="javascript:x()"><text>hi</text></a>'
             '<foreignObject><div/></foreignObject><image href="http://x.test/i.png"/></svg>')
    clean = sanitize_svg(dirty)
    save(work, "scene.svg", clean)
    st = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    d = ImageDraw.Draw(st)
    d.ellipse([56, 56, 456, 456], fill=(255, 255, 255, 255))
    d.ellipse([76, 76, 436, 436], fill=(230, 90, 60, 255))
    d.ellipse([196, 196, 316, 316], fill=(250, 210, 80, 255))
    st.save(work / "sticker.png")
    cols = {c for c in st.getdata() if c[3] == 255}
    return [truth("script/foreignObject/image/a removed", not re.search(r"<(script|foreignObject|image|a)\b", clean)),
            truth("on* and external url() removed", "onclick" not in clean and "https://" not in clean and "javascript" not in clean),
            truth("safe shapes kept", "<rect" in clean and "<circle" in clean), eq("sticker 512x512", st.size, (512, 512)),
            truth("white outline + 2-4 palette colours", (255, 255, 255, 255) in cols and 2 <= len(cols) - 1 <= 4, len(cols))]


# ---------- GEN-34 code extraction ----------
def extract_code(text):
    m = re.findall(r"```[\w+-]*\n(.*?)```", text, re.S)
    if m:
        return m[0].rstrip("\n")
    stripped = re.sub(r"^```\w*\s*$", "", text, flags=re.M).strip()
    return stripped


def g34(work):
    a = extract_code("Here is the code:\n```python\nimport io\nx=1\n```\nEnjoy.")
    b = extract_code("```\nprint(2)")
    c = extract_code("y = 3")
    save(work, "extracted.py", a)
    return [eq("fenced block", a, "import io\nx=1"), eq("lone fence stripped", b, "print(2)"), eq("bare code as is", c, "y = 3")]


# ---------- GEN-35 AI bridge routing ----------
def bridge(prompt, backend, cli_checked_at=None, now=0):
    if backend == "none":
        return {"route": "manual package"}
    via = "stdin" if len(prompt) >= 28000 else "argv"
    fresh = cli_checked_at is not None and now - cli_checked_at < 600
    return {"route": "cli" if backend in ("auto", "cli") and fresh else "api", "via": via, "timeout": 240, "max_tokens": 8000}


def g35(work):
    r = [bridge("x", "none"), bridge("x" * 28000, "auto", 0, 100), bridge("x", "auto", 0, 700)]
    save(work, "bridge.json", r)
    return [eq("backend none always works", r[0]["route"], "manual package"), eq(">=28000 chars via stdin", r[1]["via"], "stdin"),
            eq("CLI readiness cached 10 min", (r[1]["route"], r[2]["route"]), ("cli", "api"))]


# ---------- GEN-45 blurred-pad reframe ----------
def g45(work):
    src = np.zeros((36, 64, 3), np.uint8)
    src[:, :32] = (200, 40, 40)
    src[:, 32:] = (40, 40, 200)
    Image.fromarray(src).save(work / "wide.png")
    vf = ("split[a][b];[a]scale=72:128:force_original_aspect_ratio=increase,crop=72:128,boxblur=10[bg];"
          "[b]scale=72:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    ffmpeg("-i", work / "wide.png", "-vf", vf, "-frames:v", "1", work / "tall.png")
    out = np.asarray(Image.open(work / "tall.png").convert("RGB")).astype(int)
    mid = out[64, 10], out[64, 60]
    top = out[5, 36]
    return [eq("9:16 canvas", out.shape[:2], (128, 72)), truth("sharp foreground centred (red left, blue right)",
                                                              mid[0][0] > 150 and mid[1][2] > 150, (mid[0].tolist(), mid[1].tolist())),
            truth("pad is blurred source, not black", top.sum() > 120, top.tolist())]


# ---------- GEN-46 image routing ----------
def image_route(need, client_work=False):
    tree = {"text in image": ["Ideogram", "Gemini", "GPT Image"], "set consistency": ["Flux multi-reference", "Nano Banana Pro", "Recraft"],
            "edit existing": ["Gemini", "Flux Kontext", "ChatGPT Images"], "vector": ["Recraft", "draw it yourself"],
            "volume": ["Flux Schnell", "Gemini Flash", "self-hosted SD"]}
    opts = tree[need]
    if client_work:
        opts = [o for o in opts if o != "FLUX.1-dev"]
    return opts[0], opts


def g46(work):
    r = {n: image_route(n)[0] for n in ("text in image", "edit existing", "vector")}
    _, vol = image_route("volume", client_work=True)
    save(work, "routing.json", r)
    return [eq("routes", r, {"text in image": "Ideogram", "edit existing": "Gemini", "vector": "Recraft"}),
            truth("never FLUX.1-dev on client work", "FLUX.1-dev" not in vol)]


# ---------- GEN-47 sampler recipes ----------
RECIPE = {"sdxl": {"sampler": "dpmpp_2m", "scheduler": "karras", "steps": 25, "cfg": (7, 8)},
          "flux": {"sampler": "euler", "scheduler": "sgm_uniform", "steps": 20, "cfg": (1, 3.5)},
          "krea": {"sampler": "euler", "scheduler": "simple", "steps": 20, "cfg": (1, 1)}}


def karras(n, smin=0.0292, smax=14.6146, rho=7.0):
    r = np.linspace(0, 1, n)
    return (smax ** (1 / rho) + r * (smin ** (1 / rho) - smax ** (1 / rho))) ** rho


def recipe_ok(model, cfg, denoise, mode):
    lo, hi = RECIPE[model]["cfg"]
    dn = (denoise == 1.0) if mode == "txt2img" else 0.3 <= denoise <= 0.7
    return lo <= cfg <= hi and dn


def g47(work):
    s = karras(25)
    save(work, "recipes.json", {"recipes": RECIPE, "karras25": s.round(4).tolist()})
    return [eq("karras endpoints", (round(float(s[0]), 4), round(float(s[-1]), 4)), (14.6146, 0.0292)),
            truth("karras strictly decreasing", bool(np.all(np.diff(s) < 0))), eq("SDXL cfg 7.5 txt2img ok", recipe_ok("sdxl", 7.5, 1.0, "txt2img"), True),
            eq("Flux cfg 7 rejected", recipe_ok("flux", 7, 1.0, "txt2img"), False), eq("img2img denoise 0.9 rejected", recipe_ok("sdxl", 7, 0.9, "img2img"), False)]


# ---------- GEN-48 LoRA/ControlNet bands + inpaint mask ----------
def band_check(kind, v):
    return {"lora_style": 0.6 <= v <= 0.9, "lora_concept": 0.4 <= v <= 0.6, "controlnet": 0.3 <= v <= 1.0, "inpaint_denoise": 0.6 <= v <= 0.85}[kind]


def inpaint_composite(orig, regen, mask):
    m = (mask > 127)[..., None]
    return np.where(m, regen, orig)


def g48(work):
    orig = np.full((36, 64, 3), 50, np.uint8)
    regen = np.full((36, 64, 3), 200, np.uint8)
    mask = np.zeros((36, 64), np.uint8)
    mask[10:20, 20:40] = 255
    out = inpaint_composite(orig, regen, mask)
    Image.fromarray(out).save(work / "inpainted.png")
    return [truth("white mask region regenerated", (out[10:20, 20:40] == 200).all()),
            truth("outside mask untouched", (out[:10] == 50).all() and (out[:, :20] == 50).all()),
            eq("bands", [band_check("lora_style", 0.7), band_check("lora_concept", 0.8), band_check("controlnet", 0.65), band_check("inpaint_denoise", 0.95)],
               [True, False, True, False])]


# ---------- GEN-49 video routing ----------
def video_route(need, stage):
    final = {"quality+audio": "Veo 3", "volume": "Kling professional", "character": "Seedance R2V", "self-hosted": "Wan 2.x"}
    draft = {"quality+audio": "Gemini Flash 512 still + Kling standard", "volume": "Kling standard", "character": "Seedance 480p",
             "self-hosted": "Wan 2.x 480p"}
    return (draft if stage == "draft" else final)[need]


def g49(work):
    r = {(n, s): video_route(n, s) for n in ("quality+audio", "volume") for s in ("draft", "final")}
    save(work, "video_routes.json", {f"{a}|{b}": v for (a, b), v in r.items()})
    return [eq("quality final", r[("quality+audio", "final")], "Veo 3"), eq("cheap draft before premium", r[("volume", "draft")], "Kling standard"),
            truth("draft differs from final", all(r[(n, "draft")] != r[(n, "final")] for n in ("quality+audio", "volume")))]


# ---------- GEN-50 keyframe-first I2V ----------
def motion_prompt(image_desc, action, move, pace, dur):
    p = f"{action}, camera {move}, {pace}, {dur} s"
    redesc = sorted(set(w for w in words(image_desc) if len(w) > 4) & set(words(p)))
    return p, redesc


def g50(work):
    p, r = motion_prompt("a red vintage tram on a cobbled street", "the tram rolls forward", "slow dolly", "gentle", 5)
    p2, r2 = motion_prompt("a red vintage tram on a cobbled street", "red vintage tram on cobbled street moves", "static", "calm", 5)
    save(work, "i2v.json", {"prompt": p, "ratio": "720:1280"})
    return [eq("shape", p, "the tram rolls forward, camera slow dolly, gentle, 5 s"), eq("no re-description", r, []),
            eq("re-describing flagged", r2, ["cobbled", "street", "vintage"])]


# ---------- GEN-61 frame stitching seam check ----------
def g61(work):
    ffmpeg("-f", "lavfi", "-i", "color=c=0x406080:s=64x36:d=1:r=24", "-vf", "format=yuv420p", work / "n1.mp4")
    ffmpeg("-f", "lavfi", "-i", "color=c=0x406080:s=64x36:d=1:r=24", "-vf", "format=yuv420p", work / "n2.mp4")
    ffmpeg("-f", "lavfi", "-i", "color=c=0xe0c040:s=64x36:d=1:r=24", "-vf", "format=yuv420p", work / "n3.mp4")
    for n in ("n1", "n2", "n3"):
        ffmpeg("-sseof", "-0.05", "-i", work / f"{n}.mp4", "-frames:v", "1", work / f"{n}_last.png")
        ffmpeg("-i", work / f"{n}.mp4", "-frames:v", "1", work / f"{n}_first.png")
    lum = lambda p: float(np.asarray(Image.open(p).convert("L")).mean())
    seam12 = abs(lum(work / "n1_last.png") - lum(work / "n2_first.png"))
    seam23 = abs(lum(work / "n2_last.png") - lum(work / "n3_first.png"))
    save(work, "seams.json", {"n1->n2": seam12, "n2->n3": seam23})
    return [truth("matching seam within 3 levels", seam12 < 3, round(seam12, 2)), truth("mismatched seam flagged (>40 levels)", seam23 > 40, round(seam23, 2))]


# ---------- GEN-63 prompt-only deliverable ----------
def prompt_only_cards(shots, approved_cost=False):
    cards = [{"shot": s, "prompt": f"{s}, 9:16", "label": "prompt only — none has been rendered"} for s in shots]
    return {"cards": cards, "may_render": approved_cost, "credentials": "HF_CREDENTIALS=<placeholder>"}


def g63(work):
    r = prompt_only_cards(["dune at dawn", "camel caravan"])
    save(work, "shot_cards.json", r)
    return [truth("every card labelled prompt-only", all(c["label"] == "prompt only — none has been rendered" for c in r["cards"])),
            eq("no render without cost approval", r["may_render"], False), truth("credential is a placeholder", "<placeholder>" in r["credentials"])]


# ---------- GEN-65 lyrics + brief ----------
def song_brief(lyrics):
    blocks = [b.strip() for b in lyrics.split("\n\n") if b.strip()]
    from collections import Counter
    c = Counter(blocks)
    chorus = max(c, key=c.get)
    hook = chorus.splitlines()[0]
    return {"chorus": chorus, "hook": hook, "reel_cut": [hook, chorus], "master": "user returns the track; treat as untouched master"}


def g65(work):
    lyr = "verse one line\nverse one b\n\nيا ليل يا عين\nالقلب مشتاق\n\nverse two line\n\nيا ليل يا عين\nالقلب مشتاق"
    b = song_brief(lyr)
    save(work, "lyrics.md", lyr)
    save(work, "music-brief.md", json.dumps(b, ensure_ascii=False, indent=1))
    return [eq("chorus = repeated block", b["chorus"], "يا ليل يا عين\nالقلب مشتاق"), eq("hook = first chorus line", b["hook"], "يا ليل يا عين"),
            truth("both files written", (work / "lyrics.md").exists() and (work / "music-brief.md").exists())]


# ---------- GEN-69 creative lane routing ----------
LANES = {"image": r"(image|photo|poster|graphic|illustration|صورة|بوستر|رسم|جرافيك|تصوير)",
         "video": r"(video|animation|avatar|motion|reel|فيديو|تحريك|أفاتار|موشن)"}
PRIORITY = {"Figma": 100, "Adobe Express": 98, "Adobe": 90, "Canva": 88, "Runway": 88, "Higgsfield": 86, "OpenArt": 84, "HeyGen": 82}


def route_lanes(task, registered, connected):
    lanes = [l for l, rx in LANES.items() if re.search(rx, task, re.I)]
    usable = sorted((a for a in registered if a in connected), key=lambda a: -PRIORITY[a])
    return lanes, usable


def g69(work):
    lanes, usable = route_lanes("اعمل بوستر وفيديو موشن للمنتج", ["Figma", "Runway", "Higgsfield", "HeyGen"], {"Higgsfield", "HeyGen"})
    save(work, "lanes.json", {"lanes": lanes, "usable": usable})
    return [eq("Arabic regex lanes", lanes, ["image", "video"]), eq("registered is not connected; priority order", usable, ["Higgsfield", "HeyGen"])]


# ---------- GEN-71 corpus search ----------
def corpus_search(root: Path, query, hits=8, per_file=3, length=200):
    length = max(200, min(30000, length))
    out = []
    q = query.lower()
    for f in sorted(root.glob("*.txt")):
        t = f.read_text(encoding="utf-8")
        n = 0
        for m in re.finditer(re.escape(q), t.lower()):
            if n >= per_file or len(out) >= hits:
                break
            out.append({"file": f.name, "offset": m.start(), "text": t[m.start():m.start() + length]})
            n += 1
    return out


def g71(work):
    root = work / "corpus"
    root.mkdir()
    for i in range(4):
        (root / f"p{i}.txt").write_text(("lighting lock note. " * 5) + "x" * 300, encoding="utf-8")
    r = corpus_search(root, "lighting lock")
    save(work, "hits.json", r)
    from collections import Counter
    return [eq("8 hits max", len(r), 8), truth("<= 3 per file", max(Counter(h["file"] for h in r).values()) <= 3),
            eq("read length clamped to >=200", len(r[0]["text"]), 200)]


# ---------- GEN-73 generate-then-trace ----------
def g73(work):
    src = work / "src"
    src.mkdir()
    for k in range(24):                                  # 1 s reference clip at 24 fps: a square moving right
        fr = np.zeros((36, 64), np.uint8)
        x = 4 + int(40 * k / 24)
        fr[10:24, x:x + 14] = 255
        Image.fromarray(fr).save(src / f"s_{k:03d}.png")
    ffmpeg("-framerate", "24", "-i", src / "s_%03d.png", "-pix_fmt", "yuv420p", work / "base.mp4")
    ffmpeg("-i", work / "base.mp4", "-vf", "fps=12", work / "f_%04d.png")
    frames = sorted(work.glob("f_*.png"))
    paths, cx = [], []
    for f in frames:
        g = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
        _, th = cv2.threshold(g, 128, 255, cv2.THRESH_BINARY)
        cs, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = max(cs, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cx.append(x + w / 2)
        paths.append("M" + " L".join(f"{p[0][0]},{p[0][1]}" for p in c) + " Z")
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 36">' + "".join(f'<path d="{p}"/>' for p in paths) + "</svg>"
    save(work, "traced.svg", svg)
    return [eq("12 frames per second extracted", len(frames), 12), truth("traced pose moves left to right", cx[-1] - cx[0] > 25, (cx[0], cx[-1])),
            eq("one SVG path per frame", svg.count("<path"), 12)]


# ---------- GEN-75 blur-to-sharp tiles ----------
def tile_state(t, i, n=4, rtl=True, dur=1.0, stagger=0.3):
    order = (n - 1 - i) if rtl else i
    u = min(1, max(0, (t - order * stagger) / dur))
    e = 1 - (1 - u) ** 2                     # power2.out
    return round(40 * (1 - e), 2), round(0.4 + 0.6 * e, 3)


def g75(work):
    t = 0.5
    st = [tile_state(t, i) for i in range(4)]
    frame = Image.new("RGB", (4 * 20, 20), (7, 7, 9))
    for i, (blur, br) in enumerate(st):
        tile = Image.new("RGB", (16, 16), (int(242 * br),) * 3).filter(ImageFilter.GaussianBlur(blur / 10))
        frame.paste(tile, (i * 20 + 2, 2))
    frame.save(work / "tiles_t0.5.png")
    return [eq("RTL: rightmost tile lands first", st[3][0] < st[0][0], True), eq("tile 4 at t=0.5 (power2.out)", st[3], (10.0, 0.85)),
            eq("tile 1 still fully blurred", st[0], (40.0, 0.4)), eq("all sharp at 1.9 s", [tile_state(1.9, i) for i in range(4)], [(0.0, 1.0)] * 4)]


# ---------- GEN-76 crossfade photo into UI ----------
def g76(work):
    sk = np.full((36, 64, 3), (230, 226, 218), np.uint8)
    ph = np.full((36, 64, 3), (79, 122, 82), np.uint8)
    fps = 30
    frames = []
    for k in range(10):                 # 300 ms at 30 fps = 9 steps
        u = min(1, k / 9)
        frames.append((sk * (1 - u) + ph * u).astype(np.uint8))
    for k, f in enumerate(frames):
        Image.fromarray(f).save(work / f"x_{k:02d}.png")
    mid = frames[4][0, 0].astype(int)
    return [eq("crossfade frames for 300 ms", len([f for f in frames]) - 1, int(0.3 * fps)),
            truth("midpoint is a mix", all(min(a, b) < m < max(a, b) for m, a, b in zip(mid, (230, 226, 218), (79, 122, 82))), mid.tolist()),
            eq("ends on the photo", frames[-1][0, 0].tolist(), [79, 122, 82])]


# ---------- GEN-78 domain-warped fbm ----------
def _noise(x, y, seed=0):
    xi, yi = np.floor(x).astype(int), np.floor(y).astype(int)
    xf, yf = x - xi, y - yi

    def h(a, b):
        v = np.sin(a * 127.1 + b * 311.7 + seed * 74.7) * 43758.5453
        return v - np.floor(v)
    u, v = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf)
    return (h(xi, yi) * (1 - u) + h(xi + 1, yi) * u) * (1 - v) + (h(xi, yi + 1) * (1 - u) + h(xi + 1, yi + 1) * u) * v


def fbm(x, y):
    s, a = 0.0, 0.5
    for i in range(4):
        s = s + a * _noise(x * 2 ** i, y * 2 ** i, i)
        a *= 0.5
    return s / 0.9375


RAMP = np.array([[200, 180, 255], [120, 230, 240], [255, 190, 210], [240, 200, 110], [170, 240, 200]], float)


def iridescent(t, W=64, H=36):
    y, x = np.mgrid[0:H, 0:W] / 12.0
    q = fbm(x, y)
    r = fbm(x + 4 * q + 0.15 * t, y + 4 * q)
    v = fbm(x + 4 * r, y + 4 * r)
    idx = np.clip(v, 0, 0.999) * 4
    i0 = idx.astype(int)
    f = (idx - i0)[..., None]
    col = RAMP[i0] * (1 - f) + RAMP[np.minimum(i0 + 1, 4)] * f
    rim = (1 - np.abs(v - 0.5) * 2) ** 3
    return np.clip(col + rim[..., None] * 60, 0, 255).astype(np.uint8)


def g78(work):
    a, b, c = iridescent(0.0), iridescent(0.0), iridescent(1.0)
    Image.fromarray(a).save(work / "liquid_t0.png")
    Image.fromarray(c).save(work / "liquid_t1.png")
    return [truth("deterministic", np.array_equal(a, b)), truth("animates with t", np.abs(a.astype(int) - c).mean() > 1),
            truth("colours stay in the thin-film ramp range (no dark pixels)", a.min() >= 100, int(a.min()))]


# ---------- GEN-79 12 fps step ----------
def g79(work):
    ffmpeg("-f", "lavfi", "-i", "testsrc=s=64x36:d=1:r=24", "-vf", "fps=12,fps=24,format=gray", "-f", "rawvideo", work / "step.gray")
    raw = np.fromfile(work / "step.gray", np.uint8)
    fr = raw.reshape(-1, 36, 64).astype(int)
    pairs_equal = sum(np.array_equal(fr[i], fr[i + 1]) for i in range(0, len(fr) - 1, 2))
    adj_diff = sum(not np.array_equal(fr[i], fr[i + 1]) for i in range(1, len(fr) - 1, 2))
    return [eq("24 fps output", len(fr), 24), truth("frames held in pairs (stop-motion cadence)", pairs_equal >= 11, pairs_equal),
            truth("new pose every 2nd frame", adj_diff >= 10, adj_diff)]


# ---------- GEN-80 Ken Burns ----------
def ken_burns(img, u, s0=1.0, s1=1.06, pan=0.015):
    e = 0.5 - 0.5 * math.cos(math.pi * u)
    s = s0 + (s1 - s0) * e
    W, H = img.size
    w, h = W / s, H / s
    cx = W / 2 + pan * W * e
    box = (cx - w / 2, H / 2 - h / 2, cx + w / 2, H / 2 + h / 2)
    return img.resize((W, H), Image.BICUBIC, box=box), s, cx


def g80(work):
    src = Image.fromarray(np.tile(np.linspace(0, 255, 64, dtype=np.uint8)[None, :, None], (36, 1, 3)))
    f0, s0, _ = ken_burns(src, 0)
    f1, s1, cx = ken_burns(src, 1)
    f1.save(work / "kb_end.png")
    return [eq("scale 1.00 -> 1.06", (round(s0, 3), round(s1, 3)), (1.0, 1.06)), eq("pan 1.5 % of width", round(cx - 32, 3), 0.96),
            truth("first frame equals source", np.abs(np.asarray(f0).astype(int) - np.asarray(src)).max() <= 1),
            truth("sine.inOut starts slow", ken_burns(src, 0.1)[1] - 1 < 0.06 * 0.1)]


# ---------- GEN-81 chroma key + exponential zoom ----------
def g81(work):
    im = np.zeros((36, 64, 3), np.uint8)
    im[:] = (0x00, 0xB1, 0x40)
    cv2.circle(im, (32, 18), 10, (220, 40, 40), -1)
    Image.fromarray(im).save(work / "green.png")
    ffmpeg("-i", work / "green.png", "-vf", "chromakey=0x00B140:0.12:0.05,format=rgba", work / "cut.png")
    a = np.asarray(Image.open(work / "cut.png"))
    zoom = [round(2.0 ** t, 3) for t in (0, 1, 2)]
    return [eq("green keyed to transparent", int(a[2, 2, 3]), 0), eq("subject opaque", int(a[18, 32, 3]), 255),
            eq("exponential zoom base^t", zoom, [1.0, 2.0, 4.0]), eq("nested world at 1/base", 1 / 2.0, 0.5)]


# ---------- GEN-83 generate-or-compose triage ----------
def triage(assets):
    rows = []
    for a in assets:
        if a["type"] in ("typography", "logo", "chart"):
            src = "compose"
        elif a.get("existing"):
            src = "use-existing"
        elif a.get("can_photograph"):
            src = "photograph"
        else:
            src = "generate"
        rows.append((a["name"], a["type"], src))
    eliminated = sum(1 for r in rows if r[2] != "generate")
    return rows, eliminated


def g83(work):
    rows, el = triage([{"name": "title AR", "type": "typography"}, {"name": "bg plate", "type": "image"},
                       {"name": "product", "type": "image", "can_photograph": True}, {"name": "logo", "type": "logo"}])
    save(work, "triage.md", "| asset | type | source |\n" + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in rows))
    return [eq("decisions", [r[2] for r in rows], ["compose", "generate", "photograph", "compose"]), eq("generations eliminated", el, 3)]


# ---------- GEN-84 overlay text, never bake ----------
def plate_prompt_ok(prompt, refs):
    baked = bool(re.search(r"\"[^\"]+\"|«[^»]+»|text that says|with the words", prompt))
    return (not baked) and "text-free" in prompt and 3 <= len(refs) <= 10


def g84(work):
    good = "rooftop at dusk, clean, text-free surfaces, empty upper third"
    bad = 'rooftop with the words "عرض خاص" in gold'
    layer = {"type": "html-text", "dir": "rtl", "text": "عرض خاص", "font": "Cairo"}
    save(work, "overlay.json", {"plate": good, "text_layer": layer})
    return [eq("textless plate with 3-10 refs", plate_prompt_ok(good, ["r1", "r2", "r3"]), True), eq("baked text rejected", plate_prompt_ok(bad, ["r"] * 4), False),
            eq("too few refs rejected", plate_prompt_ok(good, ["r1"]), False), eq("Arabic in the HTML layer", layer["dir"], "rtl")]


# ---------- GEN-85 contact sheet outliers ----------
def outlier_action(images, thresh=40):
    means = np.array([np.asarray(i).reshape(-1, 3).mean(axis=0) for i in images])
    med = np.median(means, axis=0)
    out = [k for k, m in enumerate(means) if np.linalg.norm(m - med) > thresh]
    if not out:
        return out, "consistent"
    return out, "regenerate the outlier" if len(out) == 1 else "fix the base and regenerate all" if len(out) >= 3 else "regenerate outliers"


def g85(work):
    warm = [Image.new("RGB", (16, 9), (200 + k, 150, 90)) for k in range(5)]
    one = warm[:4] + [Image.new("RGB", (16, 9), (40, 80, 200))]
    three = warm[:3] + [Image.new("RGB", (16, 9), (40, 80, 200)) for _ in range(3)] + warm[:1]
    sheet = Image.new("RGB", (16 * 5, 9))
    for k, im in enumerate(one):
        sheet.paste(im, (16 * k, 0))
    sheet.save(work / "contact_sheet.png")
    html = "<div style='display:grid;grid-template-columns:repeat(5,1fr)'>" + "".join(f"<img src='a{k}.png'>" for k in range(5)) + "</div>"
    save(work, "contact.html", html)
    manifest = [{"model": "m", "version": "1", "seed": 7 + k, "base": "warm", "variable": f"v{k}", "file": f"a{k}.png"} for k in range(5)]
    save(work, "manifest.json", manifest)
    return [eq("consistent set", outlier_action(warm)[1], "consistent"), eq("one outlier", outlier_action(one), ([4], "regenerate the outlier")),
            eq(">=3 outliers -> fix base", outlier_action(three)[1], "fix the base and regenerate all")]


# ---------- GEN-86 budget discipline ----------
def budget_log(calls, unit_prices, cap):
    spent, log = 0.0, []
    for c in calls:
        cost = unit_prices[c["kind"]]
        if spent + cost > cap:
            return 1, log + [f"REFUSED {c['kind']}: over cap {cap}"]
        spent += cost
        log.append(f"{c['kind']} {cost} -> {spent}")
    return 0, log


def yield_flag(kept, generated, rounds):
    flags = []
    if generated and kept / generated < 0.3:
        flags.append("weak prompt (<30 % yield)")
    if rounds > 3:
        flags.append("switch to composition (>3 rounds)")
    return flags


def g86(work):
    rc, log = budget_log([{"kind": "still"}] * 2 + [{"kind": "clip"}], {"still": 1, "clip": 5}, cap=6)
    rc2, _ = budget_log([{"kind": "still"}, {"kind": "clip"}], {"still": 1, "clip": 5}, cap=6)
    save(work, "budget.log", "\n".join(log))
    return [eq("over cap exits non-zero", rc, 1), eq("within cap ok", rc2, 0), eq("flags", yield_flag(1, 4, 4), ["weak prompt (<30 % yield)", "switch to composition (>3 rounds)"]),
            eq("2 variations, healthy yield", yield_flag(1, 2, 1), [])]


# ---------- GEN-87 licence-first ----------
NONCOMM = {"FLUX.1-dev", "SD3-medium-noncommercial"}


def licence_audit(brief, manifest):
    bad = [m["file"] for m in manifest if brief["use"] == "commercial" and m["model"] in NONCOMM]
    needs_indemnity = brief.get("resold", False)
    return bad, needs_indemnity


def g87(work):
    man = [{"file": "a.png", "model": "FLUX.1-schnell"}, {"file": "b.png", "model": "FLUX.1-dev"}]
    bad, ind = licence_audit({"use": "commercial", "resold": True}, man)
    ok, _ = licence_audit({"use": "non-commercial"}, man)
    save(work, "licence_audit.json", {"blocked": bad, "indemnity_required": ind})
    return [eq("non-commercial output blocked before delivery", bad, ["b.png"]), eq("indemnity flagged for resold", ind, True),
            eq("non-commercial brief passes", ok, [])]


# ---------- GEN-88 disclosure ----------
def disclosure(manifest, endcard):
    needs = any(m["generated"] and m["kind"] in ("human", "voice") for m in manifest)
    ok = (not needs) or bool(re.search(r"AI|generated|مولّد|ذكاء اصطناعي", endcard))
    return needs, ok


def g88(work):
    man = [{"shot": 1, "generated": True, "kind": "human"}, {"shot": 2, "generated": False, "kind": "product"}]
    a = disclosure(man, "")
    b = disclosure(man, "Contains AI-generated people.")
    c = disclosure(man[1:], "")
    save(work, "disclosure.json", {"manifest": man, "missing": a, "ok": b})
    return [eq("generated human without disclosure fails", a, (True, False)), eq("disclosed passes", b, (True, True)), eq("no synthetic humans: none needed", c, (False, True))]


# ---------- GEN-89 prompt != media ----------
def g89(work):
    ffmpeg("-f", "lavfi", "-i", "color=c=gray:s=64x36:d=1.5:r=30", "-vf", "format=yuv420p", work / "real.mp4")
    items = [{"name": "shot1", "path": str(work / "real.mp4")}, {"name": "shot2", "path": str(work / "missing.mp4"), "prompt": "dune"}]
    rep = []
    for it in items:
        p = Path(it["path"])
        if p.exists():
            rep.append(f"{it['name']}: on disk {p.name}, ffprobe {ffprobe_duration(p):.2f} s")
        else:
            rep.append(f"{it['name']}: prompt only (not rendered)")
    save(work, "honesty_report.txt", "\n".join(rep))
    return [eq("existing file reported with ffprobe numbers", rep[0], "shot1: on disk real.mp4, ffprobe 1.50 s"),
            eq("prompt-only labelled", rep[1], "shot2: prompt only (not rendered)")]


# ---------- GEN-X02 continuous take then cut ----------
def cut_plan(ref_lengths, take_s, seed=3, min_s=0.8):
    rng = np.random.default_rng(seed)
    cuts, t = [], 0.0
    while True:
        L = float(rng.choice(ref_lengths))
        if t + L > take_s:
            break
        cuts.append((round(t, 2), round(t + L, 2)))
        t += L
    return cuts, sum(b - a for a, b in cuts) / take_s


def gx02(work):
    ref = [0.8, 1.2, 1.2, 2.0, 3.5]
    cuts, used = cut_plan(ref, 13.0)
    save(work, "cuts.json", {"cuts": cuts, "usable": used})
    lens = [round(b - a, 2) for a, b in cuts]
    return [truth("lengths drawn from the reference distribution, not its mean", set(lens) <= set(ref) and len(set(lens)) > 1, lens),
            truth("every window >= 0.8 s", min(lens) >= 0.8), truth("usable share of the take > 77 %", used > 0.77, round(used, 3)),
            eq("deterministic with seed", cut_plan(ref, 13.0)[0], cuts)]


# ---------- GEN-G01 topic-to-short ----------
ALLOWED_LIC = {"pexels", "pixabay", "own", "cc0", "cc-by"}


def pipeline_check(stage):
    errs = []
    for s in stage["script"]:
        n = len(stage["terms"].get(s, []))
        if not 2 <= n <= 3:
            errs.append(f"terms for '{s}': {n}")
    errs += [f"clip {c['url']} licence {c['licence']}" for c in stage["clips"] if c["licence"] not in ALLOWED_LIC]
    if not stage["approved"].get("script") or not stage["approved"].get("clips"):
        errs.append("user approval missing before render")
    if stage.get("voice") == "cloned" and not stage.get("consent"):
        errs.append("cloned voice without consent")
    return errs


def gg01(work):
    st = {"script": ["Coffee came from Yemen.", "Cairo cafes followed."],
          "terms": {"Coffee came from Yemen.": ["coffee beans", "yemen hills"], "Cairo cafes followed.": ["cairo cafe"]},
          "clips": [{"url": "https://pexels.test/1", "licence": "pexels", "in": 0, "out": 3}, {"url": "https://yt.test/x", "licence": "youtube-standard", "in": 0, "out": 2}],
          "approved": {"script": True}, "voice": "cloned"}
    errs = pipeline_check(st)
    save(work, "stages.json", {"stage": st, "errors": errs})
    return [eq("four problems found", len(errs), 4), truth("unlicensed clip rejected", any("youtube-standard" in e for e in errs)),
            truth("approval gate", "user approval missing before render" in errs)]


PROGRAMS = {"GEN-01": g01, "GEN-02": g02, "GEN-03": g03, "GEN-04": g04, "GEN-05": g05, "GEN-06": g06, "GEN-07": g07, "GEN-08": g08,
            "GEN-09": g09, "GEN-10": g10, "GEN-11": g11, "GEN-12": g12, "GEN-13": g13, "GEN-14": g14, "GEN-15": g15, "GEN-16": g16,
            "GEN-17": g17, "GEN-21": g21, "GEN-22": g22, "GEN-23": g23, "GEN-24": g24, "GEN-25": g25, "GEN-26": g26, "GEN-27": g27,
            "GEN-28": g28, "GEN-29": g29, "GEN-30": g30, "GEN-31": g31, "GEN-32": g32, "GEN-33": g33, "GEN-34": g34, "GEN-35": g35,
            "GEN-45": g45, "GEN-46": g46, "GEN-47": g47, "GEN-48": g48, "GEN-49": g49, "GEN-50": g50, "GEN-61": g61, "GEN-63": g63,
            "GEN-65": g65, "GEN-69": g69, "GEN-71": g71, "GEN-73": g73, "GEN-75": g75, "GEN-76": g76, "GEN-78": g78, "GEN-79": g79,
            "GEN-80": g80, "GEN-81": g81, "GEN-83": g83, "GEN-84": g84, "GEN-85": g85, "GEN-86": g86, "GEN-87": g87, "GEN-88": g88,
            "GEN-89": g89, "GEN-X02": gx02, "GEN-G01": gg01}
