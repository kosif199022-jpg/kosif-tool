#!/usr/bin/env python3
"""Build data/taste_index.json: one tagged row per style the owner has (catalog 311 + library 500 + atlas 86).

Deterministic heuristics (no model, no randomness) — every tag comes from words already in the style's own fields:

  text      catalog: name/name_ar/category/origin + catalog/briefs.json (summary/concept/scenes) + first 1.5 KB of
            styles/<id>/SKILL.md; library500: name/look/logic/group/motif/texture (colour
            names are left out: 'red'/'dark' in a palette is not a mood — the hex palette is used numerically); atlas86: name/
            category/look/motion/technique_cues/music/tone.
  feelings  keyword lexicon per brief feeling (FEEL_WORDS) counted over the text + a prior per category/group
            (PRIOR_FEEL). The top 3 feelings with score > 0 are kept (always ≥ 1: falls back to the prior).
  energy    0.5 + 0.06·(#fast words) − 0.06·(#slow words) + category/group bias, clamped to 0.05..0.95.
  palette   library/atlas hex palettes → mean warmth (R−B), lightness, saturation → nudges grade choice.
  platform  catalog aspect_label (9:16 → reel/story, 16:9 → youtube/landscape, 1:1 → square, 4:5 → square/reel);
            no aspect → "any" (fits every platform, scored a bit lower than an exact match).
  content   CONTENT_WORDS lexicon + category/group map (product-ui → product, cartography → travel …).
  grade     first matching GRADE_RULES keyword (neon → cyberpunk, noir → mono, terminal → matrix-tech …), else the
            palette (warm/cool/mono/faded), else FEEL_GRADE[top feeling].
  transitions / camera   energy band + keyword rules (glitch → pixelize, paper → wipe, iris → circleopen …),
            every id checked against data/transitions.json and data/camera.json.
  caption   energy ≥ 0.7 → punchy; talking-head/interview fit → karaoke; calm/sad top feeling → clean; else karaoke.

Run:  python3 build_taste_index.py        (writes ../data/taste_index.json, prints counts)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dm_common as C  # noqa: E402

DATA = C.SKILL / "data"
FEELINGS = ["tense", "warm", "epic", "playful", "calm", "inspiring", "sad", "funny"]
PLATFORMS = ["reel", "story", "youtube", "square", "landscape"]
CONTENT = ["talking-head", "travel", "product", "interview", "event", "montage"]

FEEL_WORDS = {
    "tense": "dark noir horror thriller glitch crash tension storm war alarm danger warning siren rekt liquidation "
             "shadow threat chase fear suspense clock countdown fire explosion collapse x-ray thermal terminal cyber "
             "توتر ظلام خطر رعب",
    "warm": "warm golden sunset family home cozy coffee bread craft heritage paper handmade candle wood felt quilt "
            "clay latte honey amber terracotta embroidery stitch grandmother kitchen tea dua دافئ بيت عائلة",
    "epic": "epic cinematic space galaxy cosmic mountain hero trailer scale monument architecture orchestral "
            "cathedral planet universe giant vast empire launch reveal 3d volumetric ملحمي سينمائي",
    "playful": "toy cartoon kid candy bounce pop pixel game clay sticker comic kawaii memphis arcade bubble confetti "
               "doodle playful cute mascot balloon emoji fun lego voxel gameboy مرح لعب",
    "calm": "calm minimal quiet soft zen water ocean slow meditation pastel mist breath gentle watercolor ink wash "
            "sumi garden lake moon night dua prayer still هادئ سكينة",
    "inspiring": "rise growth sunrise dream future light journey success progress launch hope build achieve "
                 "chart up grow bloom spark ignite ملهم نجاح",
    "sad": "rain memory loss grey gray faded old vintage melancholy lonely winter tear goodbye grief archive "
           "dust decay ruin حزن ذكرى",
    "funny": "joke meme funny comic absurd gag rekt satire parody silly prank laugh wink pun ضحك نكتة",
}
FAST = ("fast punchy glitch kinetic beat bounce snap rapid burst flash strobe whip pop explosion energetic hype "
        "drop crash race montage music rhythm type")
SLOW = "calm slow minimal quiet soft zen meditation still gentle drift wash mist breath ambient patient"
CONTENT_WORDS = {
    "talking-head": "talk speaker explainer lesson teacher host presenter dua quote speech voice podcast face",
    "travel": "travel map city landscape mountain ocean journey trip road nature place tourism cartography",
    "product": "product ui app phone launch brand ad commerce device screen dashboard saas package shop",
    "interview": "interview conversation podcast dialogue question guest documentary",
    "event": "event wedding party concert festival stage crowd celebration sport match",
    "montage": "montage music beat rhythm kinetic collage sequence highlight recap reel",
}
PRIOR_FEEL = {  # category / group / atlas category → feeling prior
    "charts": "inspiring", "kinetic-type": "epic", "product-ui": "inspiring", "characters": "playful", "music": "epic",
    "code": "tense", "photos": "warm", "diagrams": "calm", "shapes": "playful", "particles": "epic",
    "hand-drawn": "warm", "3d": "epic", "phone": "playful", "ads": "inspiring",
    "arabic-heritage": "warm", "world-crafts": "warm", "material-fusion": "epic", "science-imaging": "calm",
    "natural-process": "calm", "architecture-drawing": "calm", "speculative-futures": "epic", "print-processes": "warm",
    "optics-light": "epic", "textile-fiber": "warm", "edible-media": "playful", "toys-miniatures": "playful",
    "interface-futures": "tense", "cartography": "inspiring", "motion-time": "epic", "sound-visual": "epic",
    "folk-naive": "playful", "type-calligraphy": "inspiring", "generative-systems": "calm", "cinematic-genres": "epic",
    "Popular Explainer Looks": "inspiring", "Painterly": "calm", "Paper & Craft": "warm", "Hand-Drawn": "warm",
    "Cosmic & Psychedelic": "epic", "Light & Imaging": "tense", "Illustration": "warm", "Print": "warm",
    "Dimensional": "playful", "Retro Digital": "playful", "Art & Design Movements": "epic",
    "Data & Information": "inspiring", "Retro UI & Neon": "tense", "Generative & Type": "calm",
}
ENERGY_BIAS = {"kinetic-type": 0.15, "music": 0.15, "particles": 0.1, "characters": 0.05, "phone": 0.05, "ads": 0.1,
               "diagrams": -0.1, "hand-drawn": -0.1, "charts": -0.03, "motion-time": 0.12, "sound-visual": 0.12,
               "natural-process": -0.12, "science-imaging": -0.08, "architecture-drawing": -0.1, "textile-fiber": -0.1,
               "toys-miniatures": 0.08, "interface-futures": 0.08, "generative-systems": -0.05,
               "Retro UI & Neon": 0.1, "Retro Digital": 0.1, "Painterly": -0.15, "Hand-Drawn": -0.08,
               "Generative & Type": 0.0, "Cosmic & Psychedelic": 0.08}
CONTENT_MAP = {"product-ui": ["product"], "phone": ["product"], "ads": ["product"], "charts": ["talking-head", "interview"],
               "diagrams": ["talking-head"], "code": ["talking-head", "product"], "kinetic-type": ["montage", "talking-head"],
               "music": ["montage", "event"], "photos": ["travel", "event"], "characters": ["talking-head", "montage"],
               "3d": ["product"], "particles": ["montage", "event"], "shapes": ["montage"], "hand-drawn": ["talking-head"],
               "cartography": ["travel"], "natural-process": ["travel"], "cinematic-genres": ["montage", "travel", "event"],
               "edible-media": ["product"], "interface-futures": ["product"], "type-calligraphy": ["talking-head"],
               "motion-time": ["montage", "event"], "sound-visual": ["montage", "event"], "arabic-heritage": ["talking-head", "travel"],
               "architecture-drawing": ["travel", "product"], "toys-miniatures": ["product", "montage"],
               "Popular Explainer Looks": ["talking-head", "product"], "Data & Information": ["talking-head", "interview"],
               "Light & Imaging": ["montage", "event"], "Retro UI & Neon": ["product", "montage"]}
GRADE_RULES = [  # (keywords, grade id) first match wins
    ("neon cyber synthwave vaporwave outrun holographic y2k chrome", "cyberpunk"),
    ("terminal matrix phosphor code crt ascii teletext hacker", "matrix-tech"),
    ("noir black-and-white monochrome 1-bit 1bit graphite pencil x-ray radiograph ink-wash sumi", "mono"),
    ("vintage film newsprint letterpress halftone sepia retro 16mm risograph zine", "vintage-film"),
    ("golden sunset honey amber latte", "golden-hour"),
    ("night moon lantern dua prayer", "night-dua"),
    ("lava magma ember fire volcano", "magma-night"),
    ("street sodium alley", "sodium-night"),
    ("product launch commercial ui app saas dashboard phone glassmorphism", "clean-commercial"),
    ("ocean deep-sea underwater blue-hour twilight", "blue-hour"),
    ("blockbuster trailer cinematic epic hero", "teal-orange"),
    ("thermal infrared heat", "dramatic"),
    ("pastel kawaii candy toy memphis confetti", "vivid"),
    ("watercolor gouache botanical paper", "bright"),
]
FEEL_GRADE = {"tense": "dramatic", "warm": "warm", "epic": "cinematic", "playful": "vivid", "calm": "cool",
              "inspiring": "teal-orange", "sad": "faded", "funny": "vivid"}
TRANS_RULES = [
    ("glitch pixel 8-bit 16-bit voxel arcade gameboy crt", ["xfade-pixelize", "xfade-hlslice"]),
    ("paper cut collage zine sticky origami page", ["xfade-wipeleft", "xfade-coverup"]),
    ("iris circle lens planet orbit cosmic", ["xfade-circleopen"]),
    ("ink watercolor wash marbling sumi", ["xfade-distance", "xfade-dissolve"]),
    ("light neon glow flash leak", ["xfade-fadewhite"]),
    ("noir shadow curtain theatre puppet", ["xfade-fadeblack", "xfade-vertopen"]),
    ("chart data graph map", ["xfade-radial", "xfade-smoothleft"]),
    ("whip speed race chase", ["xfade-hblur"]),
]
CAM_RULES = [
    ("map cartography landscape painting poster", ["ken-burns-left"]),
    ("architecture tower monument building", ["tilt-up"]),
    ("comic meme joke rekt", ["snap-zoom"]),
    ("drop impact explosion crash", ["shake-in"]),
    ("documentary handheld street", ["handheld-drift"]),
]

TOKEN = re.compile(r"[\w\-]+", re.UNICODE)


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def words(text: str) -> list[str]:
    return [w.lower() for w in TOKEN.findall(text or "")]


def count(ws: list[str], lexicon: str, joined: str) -> int:
    n = 0
    for k in lexicon.split():
        n += joined.count(k) if "-" in k or not k.isascii() else ws.count(k) + sum(1 for w in ws if w.startswith(k) and w != k and len(k) > 3)
    return n


def has(joined: str, k: str) -> bool:
    """Whole-word (prefix) match: 'ui' must not fire inside 'build' or 'quiet'."""
    return re.search(r"(?<![\w])" + re.escape(k), joined) is not None


def palette_stats(hexes: list[str]) -> dict | None:
    rgb = []
    for h in hexes or []:
        h = str(h).lstrip("#")
        if len(h) == 6:
            try:
                rgb.append(tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)))
            except ValueError:
                pass
    if not rgb:
        return None
    warm = sum(r - b for r, g, b in rgb) / len(rgb)
    light = sum((max(c) + min(c)) / 2 for c in rgb) / len(rgb)
    sat = sum(max(c) - min(c) for c in rgb) / len(rgb)
    return {"warmth": round(warm, 3), "lightness": round(light, 3), "saturation": round(sat, 3)}


def platforms_for(aspect_label: str | None) -> tuple[str, list[str]]:
    return {"9:16": ("9:16", ["reel", "story"]), "16:9": ("16:9", ["youtube", "landscape"]),
            "1:1": ("1:1", ["square"]), "4:5": ("4:5", ["square", "reel"])}.get(aspect_label or "", ("any", ["any"]))


def tag(row: dict, text: str, cats: list[str], pal: dict | None, vocab: dict) -> dict:
    ws = words(text)
    joined = " " + " ".join(ws) + " "
    fs = {f: count(ws, FEEL_WORDS[f], joined) for f in FEELINGS}
    for c in cats:
        if c in PRIOR_FEEL:
            fs[PRIOR_FEEL[c]] += 1
    ranked = sorted(FEELINGS, key=lambda f: (-fs[f], FEELINGS.index(f)))
    moods = [f for f in ranked if fs[f] > 0][:3] or [PRIOR_FEEL.get(cats[0], "calm") if cats else "calm"]
    fast, slow = count(ws, FAST, joined), count(ws, SLOW, joined)
    energy = 0.5 + 0.06 * min(fast, 6) - 0.06 * min(slow, 6) + sum(ENERGY_BIAS.get(c, 0) for c in cats)
    energy += {"tense": 0.05, "funny": 0.08, "playful": 0.06, "epic": 0.04, "calm": -0.1, "sad": -0.1}.get(moods[0], 0)
    energy = round(max(0.05, min(0.95, energy)), 2)
    cfit = {c: count(ws, CONTENT_WORDS[c], joined) for c in CONTENT}
    for c in cats:
        for ct in CONTENT_MAP.get(c, []):
            cfit[ct] += 1
    content = [c for c in sorted(CONTENT, key=lambda c: (-cfit[c], CONTENT.index(c))) if cfit[c] > 0][:3] or ["montage"]
    # grade
    grade, why_grade = None, ""
    for kws, g in GRADE_RULES:
        hit = [k for k in kws.split() if has(joined, k)]
        if hit:
            grade, why_grade = g, f"keyword:{hit[0]}"
            break
    if not grade and pal:
        if pal["saturation"] < 0.12:
            grade, why_grade = "mono", "palette:desaturated"
        elif pal["warmth"] > 0.25:
            grade, why_grade = "warm", "palette:warm"
        elif pal["warmth"] < -0.15:
            grade, why_grade = "cool", "palette:cool"
        elif pal["lightness"] > 0.72 and pal["saturation"] < 0.3:
            grade, why_grade = "faded", "palette:light-matte"
    if not grade:
        grade, why_grade = FEEL_GRADE[moods[0]], f"feeling:{moods[0]}"
    # transitions: energy band first, then keyword specials
    if energy >= 0.7:
        tr = ["cut", "jump-cut", "xfade-zoomin"]
    elif energy >= 0.45:
        tr = ["cut", "match-cut", "xfade-slideleft" if "playful" in moods or "funny" in moods else "xfade-fadeblack"]
    else:
        tr = ["cut", "xfade-fade", "xfade-dissolve"]
    for kws, ids in TRANS_RULES:
        if any(has(joined, k) for k in kws.split()):
            tr = tr[:2] + [i for i in ids if i not in tr]
            break
    if energy >= 0.7:
        cam = ["punch-in", "shake-in", "speed-ramp"]
    elif energy >= 0.45:
        cam = ["punch-in", "slow-push"]
    else:
        cam = ["slow-push", "ken-burns-left"]
    for kws, ids in CAM_RULES:
        if any(has(joined, k) for k in kws.split()):
            cam = [i for i in ids if i not in cam] + cam
            break
    tr = [t for t in tr if t in vocab["transitions"]][:4]
    cam = [c for c in cam if c in vocab["camera"]][:3]
    assert grade in vocab["grades"], grade
    if energy >= 0.7:
        cap = "punchy"
    elif {"talking-head", "interview"} & set(content):
        cap = "karaoke"
    elif moods[0] in ("calm", "sad"):
        cap = "clean"
    else:
        cap = "karaoke"
    kw = sorted({w for w in ws if len(w) > 3 and w.isalpha()}, key=lambda w: (-ws.count(w), w))[:24]
    return {**row, "moods": moods, "mood_scores": {f: fs[f] for f in FEELINGS if fs[f]}, "energy": energy,
            "content_types": content, "grade_id": grade, "grade_why": why_grade, "transition_ids": tr,
            "camera_ids": cam, "caption_style": cap, "keywords": kw}


def vocab_ids() -> dict:
    return {"grades": {g["id"] for g in load(DATA / "grades.json")["grades"]},
            "transitions": {t["id"] for t in load(DATA / "transitions.json")["transitions"]},
            "camera": {c["id"] for c in load(DATA / "camera.json")["cameras"]}}


def build() -> dict:
    vocab = vocab_ids()
    rows = []
    briefs = load(C.CATALOG / "briefs.json")
    for s in load(C.CATALOG / "styles.json"):
        b = briefs.get(s["id"], {})
        skill = C.ROOT / (s.get("skill") or f"styles/{s['id']}/SKILL.md")
        sk = skill.read_text(encoding="utf-8")[:1500] if skill.is_file() else ""
        cats = list(s.get("category") or [])
        text = " ".join(map(str, [s.get("name"), s.get("name_ar"), " ".join(cats), s.get("origin"), b.get("summary_en"),
                                  b.get("concept_en"), " ".join(b.get("scenes_en") or []), b.get("title_ar"), sk]))
        aspect, plats = platforms_for(s.get("aspect_label"))
        rows.append(tag({"id": s["id"], "source": "catalog", "name": s.get("name"), "name_ar": s.get("name_ar") or b.get("title_ar"),
                         "family": cats[0] if cats else None, "aspect": aspect, "platforms": plats,
                         "ref": f"styles/{s['id']}/STYLE.json", "has_brief": bool(b)}, text, cats, None, vocab))
    lib = load(C.SP_DATA / "style_library_500.json")
    for s in lib["styles"]:
        text = " ".join(map(str, [s.get("name"), s.get("slug"), s.get("group"), s.get("motif"), s.get("texture"), s.get("look"),
                                  s.get("logic")]))
        rows.append(tag({"id": s["id"], "source": "library500", "name": s.get("name"), "name_ar": s.get("name_ar"),
                         "family": s.get("group"), "slug": s.get("slug"), "aspect": "any", "platforms": ["any"],
                         "ref": f"kosif-superpowers/data/style_library_500.json#{s['id']}",
                         "palette": palette_stats(s.get("palette"))}, text, [s.get("group")], palette_stats(s.get("palette")), vocab))
    atlas = load(C.SP_DATA / "futurepedia_style_atlas_86.json")
    for s in atlas["styles"]:
        text = " ".join(map(str, [s.get("name"), s.get("slug"), s.get("source_style_id"), s.get("category"), s.get("look"),
                                  s.get("motion"), " ".join(s.get("technique_cues") or []), " ".join(s.get("music") or []),
                                  s.get("tone"), s.get("primary_area"), s.get("capability_ar")]))
        rows.append(tag({"id": s["id"], "source": "atlas86", "name": s.get("name"), "name_ar": s.get("capability_ar"),
                         "family": s.get("category"), "slug": s.get("slug"), "source_style_id": s.get("source_style_id"),
                         "aspect": "any", "platforms": ["any"],
                         "ref": f"kosif-superpowers/data/futurepedia_style_atlas_86.json#{s['id']}",
                         "palette": palette_stats(s.get("palette"))},
                        text, [s.get("category")], palette_stats(s.get("palette")), vocab))
    counts = {k: sum(1 for r in rows if r["source"] == k) for k in ("catalog", "library500", "atlas86")}
    return {"schema": "kosif.dm.taste_index.v1", "count": len(rows), "counts": counts,
            "heuristics": "see build_taste_index.py docstring — keyword lexicons + category priors + palette stats; deterministic",
            "feelings": FEELINGS, "platforms": PLATFORMS, "content_types": CONTENT, "styles": rows}


def main() -> int:
    idx = build()
    out = DATA / "taste_index.json"
    out.write_text(json.dumps(idx, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    from collections import Counter
    print(f"wrote {out} · {idx['count']} styles {idx['counts']}")
    print("moods:", dict(Counter(r["moods"][0] for r in idx["styles"])))
    print("grades:", dict(Counter(r["grade_id"] for r in idx["styles"])))
    print("captions:", dict(Counter(r["caption_style"] for r in idx["styles"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
