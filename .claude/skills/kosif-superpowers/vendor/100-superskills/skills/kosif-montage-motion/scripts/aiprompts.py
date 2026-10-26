"""Per-shot AI-video prompts with the 7-layer anatomy (references/seven-layer-anatomy.md), for a realistic version of
a film on Veo, Sora, Kling, Runway, plus a Midjourney/Flux keyframe. Recovered from ultra-motion-montage
(`ultra_animator ai_prompts`) and the Egypt-2120 project (ai-video-prompts.json), now deterministic and local.

    python scripts/kmotion.py aiprompts SHOTS.json   [--out ai-video-prompts.json]
    python scripts/kmotion.py aiprompts reel.json    (scenes with an "ai" block, from `kmotion review init`)
    python scripts/kmotion.py aiprompts PROJECT_DIR  (the kosif-reel block of index.html)

A shot: {"subject", "action", "environment", "time", "wardrobe", "shot", "angle", "lens", "camera_move", "lighting",
"palette", "motion", "atmosphere", "duration", "aspect", "fps", "negative": [...], "locks": {"style": ..., "character": ...}}.
Locks repeat word for word in every shot (continuity). Nothing is sent anywhere: this writes text for the user to paste.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLATFORMS = ("veo", "sora", "kling", "runway", "keyframe")
LIMITS = {"runway": 1000, "kling": 2500}
NEG_BASE = ["blurry", "deformed hands", "extra fingers", "watermark", "text overlay", "low quality", "jpeg artifacts", "flicker", "warped geometry"]
WEAK = ("4k", "8k", "hq", "best quality", "masterpiece", "beautiful", "stunning", "amazing", "ultra realistic", "high quality")
STRONG = ("volumetric", "subsurface", "chiaroscuro", "rembrandt", "anamorphic", "film grain", "atmospheric perspective", "kelvin", "f/",
          "specular", "caustic", "rim light", "backlit", "haze", "bokeh", "motion blur", "shallow depth", "dolly", "crane", "tracking")


def _s(v) -> str:
    return ", ".join(map(str, v)) if isinstance(v, (list, tuple)) else str(v or "").strip()


def layers(sh: dict) -> dict:
    return {
        "location": ", ".join(x for x in (_s(sh.get("environment")), _s(sh.get("time")), _s(sh.get("weather"))) if x),
        "subject": ", ".join(x for x in (_s(sh.get("subject")), _s(sh.get("action"))) if x),
        "wardrobe": _s(sh.get("wardrobe")) or _s(sh.get("materials")),
        "lighting": _s(sh.get("lighting")),
        "camera": ", ".join(x for x in (_s(sh.get("shot")), _s(sh.get("angle")), _s(sh.get("lens")), _s(sh.get("camera_move"))) if x),
        "atmosphere": ", ".join(x for x in (_s(sh.get("atmosphere")), _s(sh.get("motion")), ("palette " + _s(sh.get("palette"))) if sh.get("palette") else "") if x),
        "technical": f"{sh.get('aspect', '16:9')}, {sh.get('fps', 24)} fps, {sh.get('duration', '5s')}",
    }


def warnings(sh: dict, L: dict) -> list[str]:
    w = [f"layer {k} is empty" for k, v in L.items() if not v and k != "wardrobe"]
    light = L["lighting"].lower()
    if light and not (re.search(r"\d{4}\s*k\b", light) and re.search(r"left|right|behind|above|below|front|back|side|top", light)):
        w.append("lighting should state physics: source, direction and colour temperature (e.g. 'moon key from upper left, 4100K')")
    text = " ".join(L.values()).lower()
    weak = [x for x in WEAK if re.search(rf"\b{re.escape(x)}\b", text)]
    if weak:
        w.append(f"weak words add little: {weak}")
    if not (sh.get("locks") or {}).get("style"):
        w.append("no style lock: shots will drift apart")
    return w


def score(text: str) -> int:
    t = text.lower()
    return max(0, min(100, 40 + 6 * sum(x in t for x in STRONG) - 8 * sum(bool(re.search(rf"\b{re.escape(x)}\b", t)) for x in WEAK)))


def platform_prompts(sh: dict, L: dict) -> dict:
    locks = sh.get("locks") or {}
    lock = " ".join(f"[{v}]" for v in locks.values() if v)
    neg = list(dict.fromkeys([*NEG_BASE, *(sh.get("negative") or [])]))
    body = (f"{L['subject']}. Setting: {L['location']}." + (f" Wardrobe and materials: {L['wardrobe']}." if L["wardrobe"] else "")
            + f" Camera: {L['camera']}. Lighting: {L['lighting']}. Atmosphere: {L['atmosphere']}.")
    out = {
        "veo": {"prompt": f"{lock} {body} {L['technical']}." + (f" Sound: {_s(sh.get('sound'))}." if sh.get("sound") else ""), "negative": ", ".join(neg)},
        "sora": {"prompt": f"{lock} A {sh.get('duration', '5s')} cinematic shot. {body} Physically plausible motion, consistent scale. {L['technical']}."},
        "kling": {"prompt": f"{lock} {body}", "negative_prompt": ", ".join(neg), "settings": {"aspect_ratio": sh.get("aspect", "16:9"), "duration": sh.get("duration", "5s"), "mode": "professional"}},
        "runway": {"prompt": f"{L['camera']}: {L['subject']}. {L['location']}. {L['lighting']}. {L['atmosphere']}.", "note": "Runway reads the camera move first; keep it under 1000 characters"},
        "keyframe": {"prompt": f"{lock} {L['subject']}, {L['location']}, {L['camera']}, {L['lighting']}, {L['atmosphere']} --ar {sh.get('aspect', '16:9')} --no {', '.join(neg[:8])}",
                     "use": "Midjourney / Flux first frame; feed it to image-to-video for continuity"},
    }
    for k, lim in LIMITS.items():
        p = out[k]["prompt"]
        if len(p) > lim:
            out[k]["prompt"] = p[:lim - 1].rsplit(" ", 1)[0] + "…"; out[k]["trimmed"] = True
    for k in out:
        out[k]["prompt"] = re.sub(r"\s+", " ", out[k]["prompt"]).strip()
        out[k]["chars"] = len(out[k]["prompt"])
    return out


def build(shots: list[dict], title: str = "") -> dict:
    res = []
    shared = {}
    for i, sh in enumerate(shots):
        sh = {**shared, **sh}
        if sh.get("locks"):
            shared["locks"] = sh["locks"]                          # a lock set once carries into every later shot
        for k in ("aspect", "fps"):
            if sh.get(k):
                shared[k] = sh[k]
        L = layers(sh)
        pp = platform_prompts(sh, L)
        res.append({"shot": sh.get("shot", i + 1), "time": sh.get("t"), "layers": L, "prompts": pp, "warnings": warnings(sh, L),
                    "score": score(" ".join(L.values())),
                    "variations": {"subtle": "same shot, gentler contrast, slower move", "dramatic": "same shot, low-key chiaroscuro, harder rim, tighter frame",
                                   "technical": f"same shot, {sh.get('lens') or '35mm'}, exact exposure notes, named materials"}})
    return {"title": title, "shots": res, "platforms": list(PLATFORMS),
            "how": "paste each prompt into its platform; generate the keyframe first, then image-to-video with the same locks"}


def load_shots(src: Path) -> tuple[list[dict], str]:
    if src.is_dir():
        html = (src / "index.html").read_text(encoding="utf-8")
        m = re.search(r'<script[^>]*id="kosif-reel"[^>]*>(.*?)</script>', html, re.S)
        if not m:
            raise SystemExit("no kosif-reel block in index.html (scenes need an \"ai\" object each)")
        d = json.loads(m.group(1)); title = (re.search(r"<title>(.*?)</title>", html) or [None, src.name])[1]
        W = int((re.search(r'data-width="(\d+)"', html) or [0, 1920])[1]); H = int((re.search(r'data-height="(\d+)"', html) or [0, 1080])[1])
        aspect = "9:16" if H > W else "16:9" if W > H else "1:1"
        return [{"shot": s["id"], "t": s.get("t"), "aspect": aspect, "duration": f"{s['t'][1] - s['t'][0]:.1f}s" if s.get("t") else "5s", **(d.get("ai") or {}), **s["ai"]}
                for s in d["scenes"] if s.get("ai")], title
    d = json.loads(src.read_text(encoding="utf-8"))
    if isinstance(d, dict) and "scenes" in d:                     # reel.json
        aspect = "9:16" if d.get("h", 0) > d.get("w", 0) else "16:9"
        return [{"shot": s["id"], "t": s.get("t"), "aspect": aspect, "duration": f"{s['t'][1] - s['t'][0]:.1f}s", **s["ai"]} for s in d["scenes"] if s.get("ai")], d.get("title", "")
    if isinstance(d, dict) and "shots" in d:
        return d["shots"], d.get("title", "")
    return [x.get("args", x) for x in d], ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src"); ap.add_argument("--out")
    a = ap.parse_args()
    shots, title = load_shots(Path(a.src))
    if not shots:
        raise SystemExit("no shots found")
    res = build(shots, title)
    text = json.dumps(res, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(json.dumps({"out": a.out, "shots": len(res["shots"]), "scores": [s["score"] for s in res["shots"]],
                          "warnings": sum(len(s["warnings"]) for s in res["shots"])}, ensure_ascii=False))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
