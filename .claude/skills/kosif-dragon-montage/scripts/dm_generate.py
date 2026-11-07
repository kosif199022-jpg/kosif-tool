#!/usr/bin/env python3
"""Dragon Montage — optional station «التوليد والمحاكاة» (generation proposals).

  dm_generate.py gaps   --job DIR [--min-quality 0.45] [--json]
  dm_generate.py attach --job DIR --proposal ID --file generated.mp4

gaps    reads brief/concepts/analysis/look/edl (whatever exists), finds what the
        footage cannot give (an arc role with no usable footage, footage shorter than
        the target, no music when the look wants music, a weak hook shot) and writes
        generate.json ("kosif.dm.generate.v1") + GENERATE_AR.md. Video prompts follow
        the owner's Kling director method (15-header master prompt, one camera move
        per shot, shots <= 6 s) and are linted with living-site/tools/kling_lint.py.
attach  registers a file the owner generated (after his yes) as a new clip cNN in
        analysis.json and job.json so direct/render can use it.

HARD RULE: this script spends nothing, uploads nothing and publishes nothing. Every
proposal carries consent_required: true; the MCP call in GENERATE_AR.md is made by
Claude only after the owner says yes in chat.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dm_common as C  # noqa: E402

SCHEMA = "kosif.dm.generate.v1"
KLING_DIR = C.SKILLS / "kosif-kling-director" / "scripts" / "kling_director.py"
LINT = C.SKILLS / "living-site" / "tools" / "kling_lint.py"
LEDGER = C.SKILLS / "living-site" / "tools" / "ledger.py"
METHOD = "living-site/references/level-2-kling-director.md"
SHOT_MAX = 6.0

FEELING_EN = {
    "tense": "tense, suspenseful", "warm": "warm, intimate", "epic": "grand, rising",
    "playful": "playful, light", "calm": "calm, unhurried", "inspiring": "hopeful, uplifting",
    "sad": "melancholic, quiet", "funny": "light, comic timing",
}
LIGHT_EN = {
    "tense": "one hard practical source frame-left at 3200K, deep shadows on the far side",
    "warm": "low golden sun at 3400K from frame-right, soft bounce fill",
    "epic": "late sun backlight at 4000K, long shadows, haze catching the light",
    "playful": "bright open daylight at 5600K, soft shadows",
    "calm": "soft overcast daylight at 6000K, even and gentle",
    "inspiring": "sunrise backlight at 3800K, gentle rim on the subject",
    "sad": "cool window light at 6500K, low contrast, dim corners",
    "funny": "bright even daylight at 5600K",
}
ROLE_ACTION = {
    "hook": "a striking first image that makes the viewer stop scrolling: strong shape, clear subject",
    "setup": "the place and subject are introduced calmly so the viewer knows where we are",
    "turn": "something changes: a reveal, a new angle or a shift in light",
    "payoff": "the strongest image of the piece: the promise of the hook is delivered",
    "cta": "a clean, held closing image with empty space for a call-to-action title",
    "broll": "texture and detail shots of the same world as the owner's footage",
}
ASPECT_KLING = {"9:16": "9:16", "16:9": "16:9", "1:1": "1:1", "4:5": "9:16"}


# ----------------------------------------------------------------------------- helpers

def _load(path: Path, name: str):
    if not path.is_file():
        return None
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:  # noqa: BLE001 - optional tool
        return None


def _try_read(job: Path, kind: str) -> dict | None:
    try:
        return C.read(job, kind)
    except (FileNotFoundError, C.ContractError, json.JSONDecodeError):
        return None


def _blocks(seconds: float, kd) -> list[int]:
    """Generation blocks (whole seconds, 3..30 each) covering `seconds`."""
    s = max(3, int(math.ceil(seconds)))
    if kd is not None:
        return [b - a for a, b in kd.plan(s)]
    n = max(1, math.ceil(s / 30))
    base, extra = divmod(s, n)
    return [base + (1 if i < extra else 0) for i in range(n)]


def _cuts(duration: float, parts: int, kd) -> list[tuple[float, float]]:
    if kd is not None:
        return kd.cuts(duration, parts)
    edges = [round(duration * i / parts, 1) for i in range(parts)] + [float(duration)]
    return list(zip(edges, edges[1:]))


def _clean(text: str) -> str:
    """Strip words the lint forbids from owner text (polish/brand words)."""
    t = " ".join(str(text).split())
    t = re.sub(r"(?i)\b(flawless|perfect(ly)?|8k|4k|hyper-?realistic|ultra[- ]detailed|masterpiece)\b", "", t)
    return re.sub(r"\s{2,}", " ", t).strip()


# ----------------------------------------------------------------------------- prompt builder

def kling_prompt(*, role: str, seconds: int, ratio: str, brief: dict, people: int, kd) -> str:
    """15-header master prompt (template H of the director method), one move per shot."""
    feeling = brief.get("feeling", "calm")
    mood = FEELING_EN.get(feeling, feeling)
    task = _clean(brief.get("task", ""))
    truth = _clean(brief.get("one_truth", "")) or task
    shots = _cuts(seconds, max(1, math.ceil(seconds / SHOT_MAX)), kd)
    framings = list(getattr(kd, "FRAMINGS", ())) or [
        "Wide establishing frame, 84° diagonal FOV, lens at waist height",
        "Medium shot, 47° FOV, lens at chest height", "Insert on the key detail, 29° FOV"]
    moves = ["slow dolly-in", "side-tracking", "locked-off", "crane up", "locked-off", "slow push-in"]
    if people == 0:  # no faces: skip close-ups on eyes
        framings = [f for f in framings if "eyes" not in f and "shoulder" not in f] or framings
    who = "Exactly 1 person" if people else "Exactly 0 people"
    action = ROLE_ACTION.get(role, ROLE_ACTION["broll"])
    timing = []
    for n, (a, b) in enumerate(shots, 1):
        end = "Hard cut." if n < len(shots) else "Final image holds to the last frame."
        timing.append(f"{a:.1f}-{b:.1f}s — SHOT {n} — {framings[(n - 1) % len(framings)]}, "
                      f"{moves[(n - 1) % len(moves)]}. {action[0].upper() + action[1:]}; the motion settles on a clear image. {end}")
    subject = "the main subject from the owner's footage" if people else "the place and objects from the owner's footage"
    return "\n".join([
        "SCENE CONTEXT",
        f"Block 1 of 1. {seconds} s, {ratio}. Role in the edit: {role}. Owner's brief: {task}",
        f"This block is {role} material for a short {brief.get('platform', 'reel')} montage. "
        f"It shows {subject}. Core idea: {truth}. Mood: {mood}.",
        "",
        "ACTIVE REFERENCES",
        "@Image1 — LOCATION — a still frame from the owner's own footage: controls layout, materials, palette "
        "and practical lights. The reference's camera angle and framing are not inherited.",
        "",
        "LOCATION MAP",
        "The space of @Image1: subject at frame-center about 3 m from the lens, background 10 m behind, "
        "screen direction frame-left to frame-right, camera works from the open side.",
        "",
        "FIRST FRAME AND SPATIAL BLOCKING",
        f"Frame 1 matches the composition of @Image1 at eye level. {who} in the shot.",
        "",
        "FORMAT MODE",
        (f"Controlled multi-shot sequence, {len(shots)} shots, hard cuts between shots."
         if len(shots) > 1 else "Single continuous shot."),
        "",
        "OPTICS",
        "Close-ups 47°, medium-wide 63°, wide 84°, inserts 29°; lens locked within each shot; "
        "focus on the subject at held moments.",
        "",
        "CAMERA",
        "One motivated move per shot, at most two; steady gimbal or dolly.",
        "",
        "ACTION TIMING",
        *timing,
        "",
        "ACTING TASK — SUBJECT",
        "SCENE DIRECTION (shared, unspoken): the world of the owner's footage continues. "
        "MOTIVE: carry the montage's idea. GOAL: one readable action per shot. "
        "OBSTACLE: time. TACTIC: simple natural movement with a natural blink cadence.",
        "",
        "PHYSICS",
        "Real weight and inertia; cloth, dust and light particles move with the air and the action.",
        "",
        "LIGHTING",
        LIGHT_EN.get(feeling, LIGHT_EN["calm"]) + "; matches the light seen in @Image1.",
        "",
        "AUDIO",
        "Silent acting; ambience and SFX timed to the action. Arabic voice-over is added in the edit. "
        "No music. No subtitles.",
        "",
        "STYLE",
        f"{mood.capitalize()} documentary-real look matching the owner's footage, fine film grain, "
        "natural skin texture with pores, one consistent grade.",
        "",
        "QUALITY",
        "Readable faces and hands at held moments; natural 180° shutter motion blur on fast moves; "
        "stable temporal continuity; consistent anatomy; each object stays one consistent object.",
        "",
        "POSITIVE CONSTRAINTS",
        f"{who} in every shot; screen direction stays frame-left to frame-right; "
        "the last frame is a clean, steady image that cuts well into the owner's footage.",
        "",
    ])


def lint_prompt(text: str, seconds: int, lint_mod) -> dict:
    if lint_mod is None:
        return {"tool": "kling_lint", "available": False, "result": "SKIPPED"}
    res = lint_mod.lint(text, seconds)
    failed = [t["name"] for t in res if t["status"] == "FAIL"]
    warned = [t["name"] for t in res if t["status"] == "warn"]
    return {"tool": "kling_lint", "available": True, "result": "FAIL" if failed else "PASS",
            "failed": failed, "warnings": warned}


def music_prompt(look: dict | None, brief: dict, seconds: float) -> tuple[str, list[int]]:
    music = (look or {}).get("music") or {}
    mood = music.get("mood") or brief.get("feeling", "calm")
    bpm = music.get("bpm_range") or [90, 110]
    mid = int(round(sum(bpm) / len(bpm))) if bpm else 100
    text = (f"Instrumental only, {FEELING_EN.get(mood, mood)} mood, {bpm[0]}-{bpm[-1]} BPM (aim {mid}), "
            f"clear steady beat for cutting, strong first 3 seconds, builds to a peak near "
            f"{int(seconds * 0.7)} s, clean ending at {int(math.ceil(seconds))} s, "
            f"for a {brief.get('platform', 'reel')} montage. No vocals.")
    return text, list(bpm)


# ----------------------------------------------------------------------------- gap finder

def _role_of(ev: dict) -> str | None:
    if ev.get("role"):
        return str(ev["role"]).lower()
    m = re.match(r"\s*([a-zA-Z-]+)\s*:", str(ev.get("reason", "")))
    return m.group(1).lower() if m else None


def find_gaps(job: Path, min_q: float) -> tuple[list[dict], dict]:
    brief = _try_read(job, "brief") or {}
    concepts = _try_read(job, "concepts") or {}
    analysis = _try_read(job, "analysis") or {"clips": [], "music": {}}
    look = _try_read(job, "look")
    edl = _try_read(job, "edl")
    target = float(brief.get("target_seconds") or 0)

    shots = [(c["id"], s) for c in analysis.get("clips", []) for s in c.get("shots", [])]
    score = lambda s: float(((s.get("quality") or {}).get("score")) or 0.0)  # noqa: E731
    footage = sum(float(c.get("duration") or 0) for c in analysis.get("clips", []))
    usable = sum(s["end"] - s["start"] for _, s in shots if score(s) >= min_q)
    if not shots:
        usable = footage
    people = max([int(s.get("faces") or 0) for _, s in shots] + [0])
    shot_by_id = {s["id"]: s for _, s in shots}
    best = sorted((s for _, s in shots), key=score, reverse=True)
    thumb = next((s.get("thumb") for s in best if s.get("thumb")), None)

    chosen = next((c for c in concepts.get("concepts", [])
                   if c.get("id") == (concepts.get("decision") or {}).get("chosen")), None)
    arc = [str(r).lower() for r in (chosen or {}).get("arc", [])] or ["hook", "setup", "turn", "payoff", "cta"]

    gaps: list[dict] = []
    # 1. footage shorter than target
    deficit = target - usable
    if target and deficit > 1.0:
        gaps.append({"kind": "short-footage", "role": "broll", "seconds": round(deficit, 2),
                     "evidence": f"usable footage {usable:.1f}s (quality>={min_q}) of {footage:.1f}s total; "
                                 f"target {target:.0f}s"})
    # 2. arc roles with no usable footage
    if edl:
        covered = {r for r in (_role_of(e) for e in edl.get("events", [])) if r}
        missing = [r for r in arc if r not in covered] if covered else []
        for r in missing:
            gaps.append({"kind": "missing-role", "role": r, "seconds": 3.0 if r in ("hook", "cta") else 5.0,
                         "evidence": f"edl has no event for arc role '{r}' (covered: {sorted(covered)})"})
    elif arc and usable < 1.5 * len(arc):
        for r in arc:
            gaps.append({"kind": "missing-role", "role": r, "seconds": 3.0,
                         "evidence": f"{usable:.1f}s usable footage cannot cover {len(arc)} arc roles"})
    # 3. weak hook shot
    hook_q = None
    if edl and edl.get("events"):
        sid = edl["events"][0].get("shot")
        if sid in shot_by_id:
            hook_q = score(shot_by_id[sid])
    elif best:
        hook_q = score(best[0])
    if hook_q is not None and hook_q < min_q and not any(g["role"] == "hook" for g in gaps):
        gaps.append({"kind": "weak-hook", "role": "hook", "seconds": 3.0,
                     "evidence": f"hook shot quality {hook_q:.2f} < {min_q}"})
    # 4. look wants music, none given
    have_music = bool((analysis.get("music") or {}).get("path")) or bool(
        (((edl or {}).get("audio") or {}).get("music") or {}).get("path"))
    wants = bool(look and (look.get("music") or {}).get("mood")) or (
        look is None and brief.get("content_type") in ("montage", "travel", "product", "event"))
    if wants and not have_music:
        gaps.append({"kind": "no-music", "role": "music", "seconds": target or (edl or {}).get("duration") or 30,
                     "evidence": "look.music asks for a mood but no music file in analysis/edl"})
    ctx = {"brief": brief, "look": look, "people": 1 if people else 0, "thumb": thumb,
           "aspect": brief.get("aspect", "9:16"), "usable": round(usable, 2), "footage": round(footage, 2),
           "target": target}
    return gaps, ctx


def build_proposals(gaps: list[dict], ctx: dict) -> list[dict]:
    kd = _load(KLING_DIR, "kling_director")
    lint_mod = _load(LINT, "kling_lint")
    brief = ctx["brief"] or {"task": "", "feeling": "calm"}
    ratio = ASPECT_KLING.get(ctx["aspect"], "9:16")
    props: list[dict] = []
    n = 0
    for g in gaps:
        if g["kind"] == "no-music":
            n += 1
            text, bpm = music_prompt(ctx["look"], brief, float(g["seconds"]))
            props.append({
                "id": f"g{n:02d}", "kind": "music", "role": "music", "gap": g["kind"], "evidence": g["evidence"],
                "seconds": round(float(g["seconds"]), 1), "prompt": text, "negative": "vocals, lyrics, spoken words",
                "bpm_range": bpm, "model_suggestion": "suno (instrumental)", "tool": "suno.audio-create",
                "mcp_call": {"tool": "mcp__suno__audio-create",
                             "args": {"prompt": text, "instrumental": True},
                             "note": "check the tool schema first; credits are taken from the owner's Suno plan"},
                "est_credits": "ask quote", "quote_call": {"tool": "mcp__suno__account-usage", "args": {}},
                "consent_required": True, "status": "proposed"})
            continue
        for sec in _blocks(float(g["seconds"]), kd):
            n += 1
            text = kling_prompt(role=g["role"], seconds=sec, ratio=ratio, brief=brief,
                                people=ctx["people"], kd=kd)
            props.append({
                "id": f"g{n:02d}", "kind": "video", "role": g["role"], "gap": g["kind"], "evidence": g["evidence"],
                "seconds": sec, "aspect": ratio, "prompt": text,
                "negative": "text, watermark, logos, extra people, warped hands, flicker",
                "reference_still": ctx["thumb"],
                "model_suggestion": "kling4_0", "tool": "higgsfield.generate_video",
                "mcp_call": {"tool": "mcp__Higgsfield__generate_video",
                             "args": {"model": "kling4_0", "prompt": "<prompt>", "duration": sec,
                                      "aspect_ratio": ratio, "resolution": "1080p",
                                      "mode": "image-to-video" if ctx["thumb"] else "text-to-video"},
                             "note": "uploading the reference still (media_upload) is also an upload: same yes"},
                "est_credits": "ask quote",
                "quote_call": {"tool": "mcp__Higgsfield__models_explore", "args": {"action": "get", "model": "kling4_0"}},
                "takes": 2, "method": METHOD,
                "lint": lint_prompt(text, sec, lint_mod),
                "consent_required": True, "status": "proposed"})
    return props


def write_ar(job: Path, doc: dict) -> Path:
    L = ["# اقتراحات التوليد — محتاجة موافقتك", "",
         "**القاعدة:** مفيش أي صرف كريدت ولا رفع ولا نشر غير لما صاحب الشغل يقول «أيوه» صريحة في الشات.",
         "", f"- المطلوب: {doc['context']['target']:.0f} ث · المادة الصالحة: {doc['context']['usable']:.1f} ث "
         f"من {doc['context']['footage']:.1f} ث", f"- عدد الاقتراحات: {len(doc['proposals'])}", ""]
    if not doc["proposals"]:
        L.append("المادة كفاية — مفيش حاجة محتاجة توليد.")
    for p in doc["proposals"]:
        L += [f"## {p['id']} — {p['kind']} لـ «{p['role']}» ({p['seconds']} ث)",
              f"- السبب: {p['evidence']}",
              f"- الأداة: `{p['tool']}` · الموديل: {p['model_suggestion']} · التكلفة: {p['est_credits']} "
              f"(اسأل عن السعر بـ `{p['quote_call']['tool']}` قبل ما تعرض)"]
        if p.get("lint"):
            L.append(f"- فحص كلينج (kling_lint): {p['lint']['result']}"
                     + (f" — تحذيرات: {', '.join(p['lint'].get('warnings', []))}" if p['lint'].get('warnings') else ""))
        L += ["", "**اللي تعرضه على صاحب الشغل:** البرومبت ده + السعر + عدد المحاولات"
              + (f" ({p['takes']})" if p.get("takes") else ""), "", "```text", p["prompt"], "```", "",
              "**الاستدعاء — بعد «أيوه» بس:**", "", "```json",
              json.dumps(p["mcp_call"], ensure_ascii=False, indent=1), "```", ""]
    L += ["## بعد التوليد", "",
          f"1. سجّل الكريدت: `python3 {LEDGER.relative_to(C.ROOT)} add ledger.tsv <model> <credits> <job id> <path>`",
          f"2. ضيف الملف كلقطة: `python3 {Path(__file__).relative_to(C.ROOT)} attach --job {job} --proposal <id> --file <file>`",
          "3. شغّل direct تاني عشان المونتاج يستخدم اللقطة الجديدة.", ""]
    f = job / "GENERATE_AR.md"
    f.write_text("\n".join(L), encoding="utf-8")
    return f


def cmd_gaps(a) -> int:
    job = C.job_dir(a.job)
    gaps, ctx = find_gaps(job, a.min_quality)
    props = build_proposals(gaps, ctx)
    doc = {"schema": SCHEMA, "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "rule": "consent_required: no credits, uploads or publishing without the owner's explicit yes in chat",
           "credits_spent": 0, "gaps": gaps,
           "context": {k: ctx[k] for k in ("usable", "footage", "target", "aspect", "people", "thumb")},
           "proposals": props}
    (job / "generate.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    write_ar(job, doc)
    out = {"job": str(job), "gaps": len(gaps), "proposals": len(props),
           "lint_fail": [p["id"] for p in props if (p.get("lint") or {}).get("result") == "FAIL"]}
    print(json.dumps(out if not a.json else doc, ensure_ascii=False))
    return 0


# ----------------------------------------------------------------------------- attach

def cmd_attach(a) -> int:
    job = C.job_dir(a.job)
    gen_f = job / "generate.json"
    doc = json.loads(gen_f.read_text(encoding="utf-8")) if gen_f.exists() else {"schema": SCHEMA, "proposals": []}
    prop = next((p for p in doc["proposals"] if p["id"] == a.proposal), None)
    if prop is None:
        raise SystemExit(f"proposal {a.proposal} not in generate.json")
    src = Path(a.file).resolve()
    if not src.is_file():
        raise SystemExit(f"{src} not found")
    analysis = _try_read(job, "analysis") or C.new("analysis", clips=[], music={"path": None, "bpm": None,
                                                                                 "beats": [], "downbeats": []},
                                                   tools_used=[], missing=[])
    jobf = job / "job.json"
    jd = json.loads(jobf.read_text(encoding="utf-8")) if jobf.exists() else C.new("job", clips=[])
    used = {c["id"] for c in analysis["clips"]}
    k = max([int(c[1:]) for c in used if re.fullmatch(r"c\d+", c)] + [len(jd.get("clips") or [])]) + 1
    cid = f"c{k:02d}"
    dst_dir = job / "generated"
    dst_dir.mkdir(exist_ok=True)
    dst = dst_dir / f"{cid}_{a.proposal}{src.suffix.lower()}"
    shutil.copy2(src, dst)

    if prop["kind"] == "music":
        analysis["music"] = {**(analysis.get("music") or {}), "path": str(dst), "generated": True,
                             "proposal": a.proposal}
        clip_id = None
    else:
        info = C.probe(dst)
        v = next((s for s in info["streams"] if s.get("codec_type") == "video"), {})
        dur = float(info["format"].get("duration") or v.get("duration") or prop.get("seconds") or 0)
        num, _, den = str(v.get("avg_frame_rate", "30/1")).partition("/")
        fps = round(float(num) / float(den or 1), 3) if float(den or 1) else 30.0
        clip = {"id": cid, "path": str(dst), "duration": round(dur, 3), "width": v.get("width"),
                "height": v.get("height"), "fps": fps,
                "has_audio": any(s.get("codec_type") == "audio" for s in info["streams"]),
                "loudness_lufs": None, "generated": True, "proposal": a.proposal, "role": prop.get("role"),
                "shots": [{"id": f"{cid}-s001", "start": 0.0, "end": round(dur, 3),
                           "quality": {"sharpness": None, "exposure": None, "shake": None, "score": 0.7,
                                       "estimated": True},
                           "faces": 0, "motion_energy": None, "color": {}, "thumb": None, "role": prop.get("role")}],
                "words": [], "silences": [], "energy": []}
        analysis["clips"].append(clip)
        jd.setdefault("clips", []).append(str(dst))
        jobf.write_text(json.dumps(jd, ensure_ascii=False, indent=2), encoding="utf-8")
        clip_id = cid
    C.write(job, "analysis", analysis)
    prop.update({"status": "attached", "clip": clip_id, "file": str(dst.relative_to(job)), "sha256": C.sha256(dst)})
    gen_f.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    with (job / "receipts.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"station": "generate", "tool": "attach", "argv": [a.proposal, str(src)], "rc": 0,
                             "seconds": 0.0, "owner_media": False, "sha256_out": prop["sha256"],
                             "stderr_tail": ""}, ensure_ascii=False) + "\n")
    print(json.dumps({"clip": clip_id, "file": str(dst), "proposal": a.proposal,
                      "next": "rerun the direct station so the edit can use it"}, ensure_ascii=False))
    return 0


def main(argv=None) -> int:
    C.utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gaps", help="find gaps and write consent-gated proposals")
    g.add_argument("--job", required=True)
    g.add_argument("--min-quality", type=float, default=0.45)
    g.add_argument("--json", action="store_true")
    t = sub.add_parser("attach", help="register a generated file as a new clip")
    t.add_argument("--job", required=True)
    t.add_argument("--proposal", required=True)
    t.add_argument("--file", required=True)
    a = p.parse_args(argv)
    return cmd_gaps(a) if a.cmd == "gaps" else cmd_attach(a)


if __name__ == "__main__":
    sys.exit(main())
