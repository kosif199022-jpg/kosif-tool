#!/usr/bin/env python3
"""KOSIF prompt forge — layered generator prompts, prompt lint and frame-exact shot lists.

مصنع البرومبتات: برومبتات طبقية لمولدات الصور والفيديو والموسيقى والصوت، وفحص البرومبت، وقائمة لقطات بإطارات دقيقة.
Prompt forge: layered prompts for still-image, video, music and voice generators, a prompt linter and a
frame-exact shot list. Standard library only, no network, deterministic, JSON on stdout.

Spec layers (spec.json): subject (required), action, setting, style, camera, light, constraints (list; items
that start with "no "/"without "/"بدون"/"لا " become an Avoid clause), and optional aspect, duration, mood,
genre, tempo_bpm, instruments, voice, pace_wpm, emotion, language, text. No brand or model names are needed:
targets are generic generator styles.

Subcommands (run from the skill root):
  forge spec.json --targets still-image,video,music,voice [--text]
      per-target prompts built from the layers, with word counts and warnings
      e.g. python3 scripts/prompt_forge.py forge spec.json --targets still-image,video
  lint prompt.txt [--target still-image|video|music|voice]
      hype words, vague adjectives, contradictions, negative-only phrasing, missing subject or camera,
      length (Arabic and English); score 0-100 with fixes
      e.g. python3 scripts/prompt_forge.py lint prompt.txt --target video
  shotlist shots.json --fps 30 --total 12 [--max-shot 10]
      per-shot video prompts whose frame counts sum exactly to total*fps (largest-remainder split of the
      shots' weights or durations); durations are frames/fps
      e.g. python3 scripts/prompt_forge.py shotlist shots.json --fps 30 --total 12
  --self-test   offline check, exits 0 on success

Bad input exits 2 with one line on stderr. Nothing is written; output goes to stdout.
"""
import argparse
import json
import re
import sys
from fractions import Fraction

TARGETS = ("still-image", "video", "music", "voice")
LENGTH = {"still-image": (15, 80), "video": (20, 100), "music": (8, 60), "voice": (5, 80)}

HYPE_EN = ["4k", "8k", "16k", "masterpiece", "ultra-detailed", "ultra detailed", "award-winning", "award winning",
           "trending on artstation", "trending", "best quality", "high quality", "hyperrealistic", "hyper-realistic",
           "ultra realistic", "stunning", "epic", "breathtaking", "insane detail", "octane render", "unreal engine"]
HYPE_AR = ["تحفة", "مذهل", "مذهلة", "خرافي", "خرافية", "فائق الجودة", "جودة عالية جدا", "جودة عالية جدًا",
           "واقعي جدا", "واقعي جدًا", "احترافي جدا", "احترافي جدًا", "أسطوري", "أسطورية", "رهيب", "رهيبة"]
VAGUE_EN = ["beautiful", "nice", "good", "cool", "amazing", "awesome", "interesting", "pretty", "great", "perfect",
            "some", "stuff", "things", "various"]
VAGUE_AR = ["جميل", "جميلة", "حلو", "حلوة", "كويس", "كويسة", "رائع", "رائعة", "حاجات", "أشياء", "شيء ما", "ممتاز"]
FIX_HINT = "replace with a physical cue (light source and direction, lens, material, texture, colour)"
CONTRADICT = [("day", "night"), ("daylight", "night"), ("sunrise", "sunset"), ("static", "dolly"),
              ("static", "pan"), ("static", "orbit"), ("static", "tracking"), ("close-up", "wide shot"),
              ("close-up", "aerial"), ("black and white", "colorful"), ("monochrome", "colorful"),
              ("minimal", "busy"), ("minimalist", "cluttered"), ("slow motion", "timelapse"),
              ("نهار", "ليل"), ("نهارا", "ليلا"), ("شروق", "غروب"), ("ثابتة", "متحركة"),
              ("لقطة قريبة", "لقطة واسعة"), ("أبيض وأسود", "ملون"), ("بسيط", "مزدحم")]
NEG_EN = re.compile(r"^\s*(no|not|never|without|don't|do not|avoid)\b", re.I)
NEG_AR = re.compile(r"^\s*(لا|بدون|بلا|ممنوع|من غير|دون|تجنب)(\s|$)")
NEG_PREFIX = re.compile(r"^\s*(no|without|avoid|بدون|لا|بلا|من غير|دون|تجنب)\s+", re.I)
CAMERA = ["shot", "close-up", "closeup", "wide", "medium", "lens", "mm", "angle", "dolly", "pan", "tilt", "orbit",
          "tracking", "static", "handheld", "aerial", "overhead", "macro", "push in", "pull back", "crane",
          "f/", "camera", "pov", "eye level", "low angle", "high angle",
          "لقطة", "كاميرا", "زاوية", "عدسة", "تتبع", "ثابتة", "علوية", "قريبة", "واسعة", "متوسطة"]
STOP = set("a an the of in on at with and or to for by from is are be as into over under near this that its "
           "very more most it his her their our your photo image picture shot style lighting light camera "
           "في على من إلى الى مع و أو عن هذا هذه ذلك تلك هو هي بين تحت فوق عند كل صورة لقطة اضاءة إضاءة "
           "كاميرا اسلوب أسلوب ستايل".split())


LABELS = {
    "en": {"sep": ", ", "in": "in ", "aspect": "aspect ratio ", "avoid": "Avoid: ", "static": "static camera",
           "camera": "Camera: ", "light": "Light: ", "style": "Style: ", "keep": "Keep: ",
           "dur": "Duration: %s s, one continuous shot, no scene change.", "one": "One continuous shot, no scene change."},
    "ar": {"sep": "، ", "in": "في ", "aspect": "نسبة الأبعاد ", "avoid": "تجنّب: ", "static": "كاميرا ثابتة",
           "camera": "الكاميرا: ", "light": "الإضاءة: ", "style": "الأسلوب: ", "keep": "حافظ على: ",
           "dur": "المدة: %s ث، لقطة واحدة متصلة بلا تغيير مشهد.", "one": "لقطة واحدة متصلة بلا تغيير مشهد."},
}


class Bad(Exception):
    pass


def words(s):
    return re.findall(r"[\w'’/-]+", s, re.U)


def has_term(text, term):
    t = text.lower()
    if re.search(r"[؀-ۿ]", term):
        return re.search(r"(^|[^؀-ۿ])(و|ب|ال|وال|بال)?" + re.escape(term) + r"($|[^؀-ۿ])", t) is not None
    if re.match(r"^[\w ]+$", term):
        return re.search(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", t) is not None
    return term in t


def split_constraints(items):
    keep, avoid = [], []
    for c in items or []:
        c = str(c).strip()
        if not c:
            continue
        if NEG_PREFIX.match(c):
            avoid.append(NEG_PREFIX.sub("", c, count=1).strip())
        else:
            keep.append(c)
    return keep, avoid


def is_ar(spec):
    lang = str(spec.get("language", "")).lower()
    return lang in ("ar", "arabic", "عربي", "العربية") or bool(re.search(r"[؀-ۿ]", str(spec.get("subject", ""))))


def clause(*parts):
    return " ".join(p.strip() for p in parts if p and str(p).strip())


def build(spec, target):
    if not isinstance(spec, dict) or not str(spec.get("subject", "")).strip():
        raise Bad("spec needs a non-empty 'subject'")
    g = lambda k: str(spec.get(k, "") or "").strip()  # noqa: E731
    keep, avoid = split_constraints(spec.get("constraints"))
    ar = is_ar(spec)
    L = LABELS["ar" if ar else "en"]
    sep = L["sep"]
    warn = []
    if target == "still-image":
        head = sep.join(x for x in [g("style"), clause(g("subject"), g("action"))] if x)
        body = [head]
        if g("setting"):
            body.append(L["in"] + g("setting"))
        for k in ("light", "camera"):
            if g(k):
                body.append(g(k))
            else:
                warn.append("missing layer: " + k)
        body += keep
        if g("aspect"):
            body.append(L["aspect"] + g("aspect"))
        else:
            warn.append("no aspect ratio; state it in the text and in the generator parameter")
        prompt = sep.join(body) + "."
        if avoid:
            prompt += " " + L["avoid"] + sep.join(avoid) + "."
    elif target == "video":
        if not g("action"):
            warn.append("video needs one clear action; none given")
        cam = g("camera") or L["static"]
        if not g("camera"):
            warn.append("no camera move given; defaulted to 'static camera'")
        s1 = clause(g("subject"), g("action")) + ((sep + L["in"] + g("setting")) if g("setting") else "") + "."
        s2 = L["camera"] + cam + "."
        s3 = (L["light"] + g("light") + ".") if g("light") else ""
        s4 = (L["style"] + g("style") + ".") if g("style") else ""
        dur = spec.get("duration")
        s5 = (L["dur"] % _num(dur)) if dur else L["one"]
        s6 = (L["keep"] + sep.join(keep) + ".") if keep else ""
        s7 = (L["avoid"] + sep.join(avoid) + ".") if avoid else ""
        prompt = " ".join(x for x in [s1, s2, s3, s4, s5, s6, s7] if x)
    elif target == "music":
        genre = g("genre") or g("style")
        if not genre:
            warn.append("no genre/style given")
        parts = [genre or "instrumental"]
        if g("mood"):
            parts.append(g("mood") + " mood")
        if spec.get("tempo_bpm"):
            parts.append("%s BPM" % _num(spec["tempo_bpm"]))
        else:
            warn.append("no tempo_bpm given")
        if spec.get("instruments"):
            ins = spec["instruments"]
            parts.append("instruments: " + (", ".join(map(str, ins)) if isinstance(ins, list) else str(ins)))
        parts.append("theme: " + g("subject"))
        if spec.get("duration"):
            parts.append("%s seconds" % _num(spec["duration"]))
        parts += keep
        prompt = sep.join(parts) + "."
        if avoid:
            prompt += " " + L["avoid"] + sep.join(avoid) + "."
    elif target == "voice":
        text = g("text")
        if not text:
            warn.append("no 'text' to speak; the subject is used as the line")
            text = g("subject")
        d = []
        if g("voice"):
            d.append("voice: " + g("voice"))
        if g("emotion") or g("mood"):
            d.append("emotion: " + (g("emotion") or g("mood")))
        if spec.get("pace_wpm"):
            d.append("pace: %s words per minute" % _num(spec["pace_wpm"]))
        if g("language"):
            d.append("language: " + g("language"))
        d += keep
        prompt = ("Delivery — " + "; ".join(d) + ". " if d else "") + 'Line: "' + text + '"'
        if avoid:
            prompt += " " + L["avoid"] + sep.join(avoid) + "."
    else:
        raise Bad("unknown target %r (use %s)" % (target, ",".join(TARGETS)))
    n = len(words(prompt))
    lo, hi = LENGTH[target]
    if n < lo:
        warn.append("short: %d words (aim %d-%d)" % (n, lo, hi))
    if n > hi:
        warn.append("long: %d words (aim %d-%d)" % (n, lo, hi))
    hype = [h for h in HYPE_EN + HYPE_AR if has_term(prompt, h)]
    if hype:
        warn.append("hype words in layers: " + ", ".join(hype))
    return {"prompt": prompt, "words": n, "chars": len(prompt), "warnings": warn}


def _num(x):
    try:
        f = float(x)
    except (TypeError, ValueError):
        raise Bad("not a number: %r" % (x,))
    return int(f) if f == int(f) else round(f, 3)


def forge(spec, targets):
    ts = [t.strip() for t in targets.split(",") if t.strip()]
    if not ts:
        raise Bad("--targets is empty")
    for t in ts:
        if t not in TARGETS:
            raise Bad("unknown target %r (use %s)" % (t, ",".join(TARGETS)))
    return {"kind": "kosif.prompt_forge.forge.v1", "subject": spec.get("subject"),
            "targets": {t: build(spec, t) for t in ts}}


def lint(text, target=None):
    if target and target not in TARGETS:
        raise Bad("unknown target %r" % target)
    t = text.strip()
    if not t:
        raise Bad("prompt is empty")
    low = t.lower()
    f = []

    def add(code, sev, msg, fix):
        f.append({"code": code, "severity": sev, "message": msg, "fix": fix})

    for h in HYPE_EN + HYPE_AR:
        if has_term(t, h):
            add("HYPE", "warn", "hype word '%s' adds noise, not quality" % h, FIX_HINT)
    for v in VAGUE_EN + VAGUE_AR:
        if has_term(t, v):
            add("VAGUE", "warn", "vague adjective '%s'" % v, FIX_HINT)
    if re.match(r"^\s*(a|an)\s+(photo|picture|image)\s+of\b", low) or re.match(r"^\s*صورة\s+(ل|لـ)", t):
        add("OPENER", "warn", "opens with 'a photo of'", "start with the style or the subject itself")
    for a, b in CONTRADICT:
        if has_term(t, a) and has_term(t, b):
            add("CONTRADICTION", "error", "contradictory terms '%s' and '%s'" % (a, b), "keep one of them")
    clauses = [c for c in re.split(r"[.,;،؛\n!?؟]+", t) if c.strip()]
    neg = [c for c in clauses if NEG_EN.match(c) or NEG_AR.match(c)]
    if clauses and len(neg) == len(clauses):
        add("NEGATIVE_ONLY", "error", "every clause is a negation; generators need what to show",
            "describe the subject positively, move exclusions to one Avoid clause")
    elif len(neg) > len(clauses) / 2:
        add("NEGATIVE_HEAVY", "warn", "%d of %d clauses are negations" % (len(neg), len(clauses)),
            "rephrase as positive descriptions")
    content = [w for w in words(low) if w not in STOP and not re.match(r"^\d", w)
               and not any(has_term(w, x) for x in HYPE_EN + HYPE_AR + VAGUE_EN + VAGUE_AR + CAMERA)
               and not NEG_EN.match(w) and not NEG_AR.match(w)]
    if len(content) < 2:
        add("MISSING_SUBJECT", "error", "no clear subject (fewer than 2 content words)", "name who/what is in frame")
    if target in (None, "still-image", "video") and not any(has_term(t, c) for c in CAMERA):
        add("MISSING_CAMERA", "error" if target == "video" else "warn", "no camera or shot term",
            "state shot size and move (e.g. 'medium shot, slow dolly in' or 'static')")
    n = len(words(t))
    lo, hi = LENGTH.get(target or "still-image")
    if n < lo:
        add("LENGTH", "warn", "short: %d words (aim %d-%d)" % (n, lo, hi), "add setting, light and camera layers")
    if n > hi:
        add("LENGTH", "warn", "long: %d words (aim %d-%d)" % (n, lo, hi), "cut repeated descriptors")
    errors = sum(x["severity"] == "error" for x in f)
    warns = len(f) - errors
    score = max(0, 100 - 20 * errors - 5 * warns)
    return {"kind": "kosif.prompt_forge.lint.v1", "target": target, "words": n,
            "arabic": bool(re.search(r"[؀-ۿ]", t)), "score": score,
            "verdict": "fail" if errors else ("revise" if warns else "pass"), "findings": f}


def split_frames(weights, total_frames):
    s = sum(weights)
    raw = [Fraction(w) * total_frames / s for w in weights]
    base = [int(r) for r in raw]
    left = total_frames - sum(base)
    order = sorted(range(len(raw)), key=lambda i: (-(raw[i] - base[i]), i))
    for i in order[:left]:
        base[i] += 1
    return base


def shotlist(data, fps, total, max_shot=None):
    shots = data.get("shots") if isinstance(data, dict) else data
    if not isinstance(shots, list) or not shots:
        raise Bad("shots.json needs a non-empty list (or {\"shots\": [...]})")
    if fps <= 0 or total <= 0:
        raise Bad("--fps and --total must be positive")
    tf = Fraction(str(total)) * Fraction(str(fps))
    if tf.denominator != 1:
        raise Bad("total*fps must be a whole number of frames (got %s)" % float(tf))
    tf = int(tf)
    if tf < len(shots):
        raise Bad("%d frames cannot hold %d shots" % (tf, len(shots)))
    base = data if isinstance(data, dict) else {}
    weights = []
    for i, s in enumerate(shots):
        if not isinstance(s, dict) or not str(s.get("subject", base.get("subject", ""))).strip():
            raise Bad("shot %d needs a 'subject' (or a top-level subject)" % (i + 1))
        w = s.get("weight", s.get("duration", 1))
        try:
            w = Fraction(str(w))
        except (ValueError, ZeroDivisionError):
            raise Bad("shot %d has a bad weight/duration %r" % (i + 1, w))
        if w <= 0:
            raise Bad("shot %d weight must be positive" % (i + 1))
        weights.append(w)
    frames = split_frames(weights, tf)
    if min(frames) < 1:
        raise Bad("a shot would get 0 frames; raise --total or merge shots")
    out, start = [], 0
    shared = {k: v for k, v in base.items() if k != "shots"}
    for i, (s, n) in enumerate(zip(shots, frames)):
        spec = dict(shared)
        spec.update(s)
        spec["duration"] = round(n / fps, 4)
        p = build(spec, "video")
        if i < len(shots) - 1:
            p["prompt"] += " End on a frame that can open the next shot."
        if max_shot and n / fps > max_shot:
            p["warnings"].append("shot is %.3f s, above --max-shot %s s; split it" % (n / fps, max_shot))
        out.append({"n": i + 1, "start_frame": start, "frames": n, "end_frame": start + n - 1,
                    "start_s": round(start / fps, 4), "duration_s": round(n / fps, 4),
                    "prompt": p["prompt"], "warnings": p["warnings"]})
        start += n
    return {"kind": "kosif.prompt_forge.shotlist.v1", "fps": fps, "total_s": total, "total_frames": tf,
            "frames_sum": sum(frames), "exact": sum(frames) == tf, "shots": out}


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        raise Bad("cannot read JSON %s: %s" % (path, e))


def self_test():
    spec = {"subject": "an old fisherman", "action": "mends a net", "setting": "a wooden pier at dawn",
            "style": "documentary photograph", "camera": "medium shot, 50 mm, eye level",
            "light": "low warm sun from the left", "constraints": ["no text", "weathered hands visible"],
            "aspect": "4:5"}
    r = forge(spec, "still-image,video")
    assert "Avoid: text." in r["targets"]["still-image"]["prompt"]
    assert lint("no text, no watermark")["verdict"] == "fail"
    assert lint("masterpiece 8k beautiful cat")["score"] < 100
    s = shotlist({"subject": "a kite", "shots": [{"action": "rises"}, {"action": "dips"}, {"action": "lands"}]}, 30, 10)
    assert s["frames_sum"] == 300 and [x["frames"] for x in s["shots"]] == [100, 100, 100]
    print("self-test: OK")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(prog="prompt_forge.py",
                                 description="مصنع البرومبتات — KOSIF prompt forge: layered prompts, lint, shot lists")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("forge", help="per-target prompts from a layered spec")
    a.add_argument("spec")
    a.add_argument("--targets", default="still-image")
    a.add_argument("--text", action="store_true", help="print only the prompts as text")
    b = sub.add_parser("lint", help="lint a prompt file")
    b.add_argument("prompt")
    b.add_argument("--target", choices=TARGETS)
    c = sub.add_parser("shotlist", help="frame-exact shot list")
    c.add_argument("shots")
    c.add_argument("--fps", type=float, required=True)
    c.add_argument("--total", type=float, required=True, help="target duration in seconds")
    c.add_argument("--max-shot", type=float)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "forge":
            r = forge(load_json(args.spec), args.targets)
            if args.text:
                for t, v in r["targets"].items():
                    print("[%s]\n%s\n" % (t, v["prompt"]))
                return 0
        elif args.cmd == "lint":
            try:
                with open(args.prompt, encoding="utf-8") as fh:
                    txt = fh.read()
            except OSError as e:
                raise Bad("cannot read %s: %s" % (args.prompt, e))
            r = lint(txt, args.target)
        else:
            fps = int(args.fps) if args.fps == int(args.fps) else args.fps
            total = int(args.total) if args.total == int(args.total) else args.total
            r = shotlist(load_json(args.shots), fps, total, args.max_shot)
    except Bad as e:
        print("prompt_forge: " + str(e), file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
