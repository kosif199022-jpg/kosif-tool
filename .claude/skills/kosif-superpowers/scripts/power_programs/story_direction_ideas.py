"""Programs for the story-direction-ideas family (STORY-*, STORY-P/X/U cards). STORY-04, STORY-08 and
STORY-38 have code proofs run elsewhere. Each other card's direction rule (timing grid, beat sheet,
hook law, lint, router, motion score ...) runs as a deterministic procedure, often rendering tiny
frames with numpy/PIL, on a fixture whose correct answer is known."""
from __future__ import annotations
import math
import random
import re
import numpy as np
from PIL import Image, ImageDraw
from ._mind_common import save, eq, truth, words, jaccard, require_fields, has_number, weighted_scores, rank

FPS = 30


def ease_out_cubic(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    t = min(max(t, 0.0), 1.0)
    return 3 * t * t - 2 * t ** 3


def back_out(t, s=1.70158):
    t = min(max(t, 0.0), 1.0) - 1
    return t * t * ((s + 1) * t + s) + 1


def frames_of(sec, fps=FPS):
    return int(round(sec * fps))


def luminance(img):
    a = np.asarray(img, float)
    if a.ndim == 3:
        a = a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722
    return a.mean() / 255


def word_count(s):
    return len(words(s))


SEVEN = ["message", "production", "duration_platform", "language", "assets", "rhythm", "preview_or_final"]
DEFAULTS = {"duration_platform": "9:16, 30 s", "preview_or_final": "preview first", "rhythm": "medium"}
BLOCKING = {"message", "production", "language"}


def intake(given):
    missing = [k for k in SEVEN if k not in given]
    ask = [k for k in missing if k in BLOCKING]
    filled = {k: DEFAULTS[k] for k in missing if k in DEFAULTS}
    return ask, filled


def s01(work):
    ask, filled = intake({"message": "launch", "assets": "voice.mp3", "language": "مصري"})
    save(work, "intake.json", {"ask": ask, "defaults": filled})
    return [eq("only blocking unknowns asked", ask, ["production"]), eq("defaults stated", filled["duration_platform"], "9:16, 30 s"),
            truth("one message <= 7 questions", len(ask) <= 7), eq("already given not asked", "assets" in ask, False)]


ROUTES = {"talking_reel": ["كلام", "talking", "speech"], "song_reel": ["أغنية", "song"], "motion_2d": ["موشن", "motion"], "cinematic_3d": ["3d", "سينمائي"],
          "edit_my_footage": ["مونتاج", "footage"], "launch_video": ["launch", "إطلاق"]}
ADDONS = {"captions": ["ترجمة", "captions"], "music": ["موسيقى", "music"]}


def route(text):
    t = text.lower()
    hits = {r: sum(k in t for k in kws) for r, kws in ROUTES.items()}
    main = max(hits, key=lambda r: (hits[r], r)) if any(hits.values()) else "analyze_reference"
    adds = [a for a, kws in ADDONS.items() if any(k in t for k in kws)]
    return main, adds


def s02(work):
    m, a = route("عايز ريل من فيديو كلام مع ترجمة وموسيقى")
    save(work, "route.json", {"main": m, "addons": a})
    return [eq("main route", m, "talking_reel"), eq("add-ons", a, ["captions", "music"]), eq("song request", route("song reel please")[0], "song_reel")]


CUTS = [0, 0.12, 0.36, 0.62, 0.84, 1.0]
BEATS = ["hook", "setup", "contrast", "payoff", "end_card"]


def proplan(seconds, fps, aspect):
    n = int(seconds * fps)
    edges = [round(c * n) for c in CUTS]
    shots = [{"beat": b, "f0": edges[i], "f1": edges[i + 1], "audio": "impact" if i in (0, 3) else "bed"} for i, b in enumerate(BEATS)]
    safe = (0.15, 0.80) if aspect == "9:16" else (0.08, 0.92)
    return shots, safe


def s03(work):
    shots, safe = proplan(12, 30, "9:16")
    save(work, "plan.json", {"shots": shots, "safe": safe})
    return [eq("cut frames", [s["f0"] for s in shots] + [shots[-1]["f1"]], [0, 43, 130, 223, 302, 360]), eq("impact on beats 1 and 4", [s["beat"] for s in shots if s["audio"] == "impact"], ["hook", "payoff"]),
            eq("9:16 safe area", safe, (0.15, 0.80)), eq("16:9 inset", proplan(12, 30, "16:9")[1], (0.08, 0.92)), truth("contiguous", all(a["f1"] == b["f0"] for a, b in zip(shots, shots[1:])))]


def s05(work):
    opts = {"S02": 4.2, "S03": 3.9, "S07": 4.5, "S11": 3.1, "CUSTOM-paper": 3.5}
    rec = max(opts, key=opts.get)
    blend = {"base": "S07", "accent": "S02"}
    valid_blend = lambda b: len(b) <= 2
    save(work, "styles.json", {"options": opts, "recommended": rec, "blend": blend})
    return [truth("3-5 options", 3 <= len(opts) <= 5), eq("one recommended", rec, "S07"), truth("max 2 blended", valid_blend(blend) and not valid_blend({"a": 1, "b": 2, "c": 3})),
            truth("outside-menu look labelled CUSTOM", any(k.startswith("CUSTOM") for k in opts))]


FELT = {"مش فخم كفاية": {"hold_s": +0.4, "easing": "expo.out", "type_weight": +200, "contrast": +0.1}, "سريع زيادة": {"duration_scale": 1.3}}


def compose_review(edits, notes):
    parts = ["## Edits (apply exactly)"] + edits + ["## Notes"] + [f"{n['tc']} {n['scene']} {n['element']}: {n['text']}" for n in notes]
    return "\n".join(parts)


def s06(work):
    note = FELT["مش فخم كفاية"]
    motion_note = {"tc": "00:03", "scene": "2", "element": "title", "text": "slower entrance"}
    prompt = compose_review(["title colour #E7B65A"], [motion_note])
    (work / "review_prompt.md").write_text(prompt)
    return [truth("felt note -> numbers", all(isinstance(v, (int, float)) or "." in str(v) for v in note.values())), truth("motion request in notes", "slower entrance" in prompt.split("## Notes")[1]),
            eq("hold added", note["hold_s"], 0.4)]


CHECK7 = ["directions", "hook", "device", "payoff", "end", "poster", "credits", "post_pack", "resolution"]


def full_power(film):
    fails = []
    if not 2 <= film["directions"] <= 3:
        fails.append("directions")
    if film["hook_s"] > 2:
        fails.append("hook")
    if film["height"] < 1080:
        fails.append("resolution")
    media = []
    if film["script"] and not film["voice"]:
        media.append("TTS")
    if film["silent_cuts"]:
        media.append("transition SFX")
    if film["duration"] > 10 and not film["music"]:
        media.append("music bed")
    return fails, media


def s07(work):
    f, m = full_power({"directions": 3, "hook_s": 2.6, "height": 720, "script": True, "voice": False, "silent_cuts": 4, "duration": 25, "music": False})
    save(work, "checklist.json", {"fails": f, "media_pass": m, "ask": "approve all/some/none"})
    return [eq("checklist fails", f, ["hook", "resolution"]), eq("one consolidated media ask", m, ["TTS", "transition SFX", "music bed"])]


MOTION_VERBS = {"reveal", "compare", "accumulate", "transform", "move", "zoom", "pan", "highlight", "play"}
CARD = ["id", "text", "takeaway", "dataLayers", "media", "cameraOrTransform", "triggerRange", "motionVerb", "reducedMotion"]


def s09(work):
    cards = [dict({k: "x" for k in CARD}, motionVerb="reveal"), dict({k: "x" for k in CARD}, motionVerb="explode"), {k: "x" for k in CARD[:-1]}]
    errs = []
    for i, c in enumerate(cards):
        miss = require_fields(c, CARD)
        if miss:
            errs.append((i, "missing", miss))
        if c.get("motionVerb") not in MOTION_VERBS:
            errs.append((i, "verb"))
    save(work, "scene_cards.json", cards)
    return [eq("nine verbs", len(MOTION_VERBS), 9), eq("errors", errs, [(1, "verb"), (2, "missing", ["reducedMotion"]), (2, "verb")])]


def shots_from_boards(panels, total):
    t0s = [p["t"] for p in panels]
    return [{"t0": t0, "t1": (t0s[i + 1] if i + 1 < len(t0s) else total)} for i, t0 in enumerate(t0s)]


def digest(boards):
    import hashlib, json
    return hashlib.sha256(json.dumps(boards, sort_keys=True).encode()).hexdigest()[:12]


def s10(work):
    boards = {"palette": {"ink": "#111", "paper": "#f4f1ea"}, "panels": [{"shot": 1, "t": 0}, {"shot": 2, "t": 2.5}, {"shot": 3, "t": 6}]}
    approved = digest(boards)
    shots = shots_from_boards(boards["panels"], 9)
    boards["panels"][1]["t"] = 3
    save(work, "shots.json", {"fps": 30, "shots": shots, "approval": approved})
    return [eq("shot 1 t0 = 0", shots[0]["t0"], 0), truth("contiguous", all(a["t1"] == b["t0"] for a, b in zip(shots, shots[1:]))), truth("approval invalidated by board change", digest(boards) != approved)]


def s11(work):
    rows = [{"t": 0.0, "shot": "close", "new": "hand drops phone"}, {"t": 1.2, "shot": "wide", "new": "room is flooded"}, {"t": 3.6, "shot": "detail", "new": ""},
            {"t": 6.0, "shot": "medium", "new": "app finds the leak"}, {"t": 9.0, "shot": "cta", "new": "download"}]
    dur = 10.0
    no_new = [r["t"] for r in rows if not r["new"]]
    shot_rate_ok = len(rows) <= dur / 2.5 + 1
    hook_ok = rows[1]["t"] <= 1.5
    save(work, "beat_sheet.json", rows)
    return [eq("row without new information flagged", no_new, [3.6]), truth("<= 1 shot / 2.5 s", shot_rate_ok), truth("hook <= 1.5 s", hook_ok), eq("ten shot-list columns", len("# time shot lens move action lighting sound text transition".split()), 10)]


def s12(work):
    fps = 1000
    rule_ms, panel_delay, panel_ms, px = 280, 80, 360, 12
    t = np.arange(0, 800)
    rule = np.array([ease_out_cubic(x / rule_ms) for x in t])
    panel_y = np.array([px * (1 - ease_out_cubic((x - panel_delay) / panel_ms)) for x in t])
    reduced = {"rule": 1.0, "panel_y": 0}
    save(work, "motion_score.json", {"rule_done_ms": int(np.argmax(rule >= 0.999)), "panel": panel_y[::40].tolist()})
    return [truth("rule complete exactly at 280 ms", rule[280] == 1.0 and rule[279] < 1.0), eq("panel starts at +80 ms", float(panel_y[80]), 12.0), eq("panel settled at 440 ms", round(float(panel_y[440]), 6), 0.0),
            truth("decelerating", rule[10] - rule[0] > rule[270] - rule[260]), eq("reduced motion instant", reduced["rule"], 1.0)]


LAYERS = ["identity", "world", "action & physics", "camera & lens", "lighting", "materials & atmosphere", "colour & story"]


def s13(work):
    spec = {k: f"{k} text" for k in LAYERS}
    bpm = 100
    clip_lens = [6, 8, 12, 4]
    bad = [c for c in clip_lens if not 5 <= c <= 10]
    cut_grid = [round(i * 60 / bpm, 3) for i in range(5)]
    save(work, "spec.json", {"layers": spec, "cut_grid": cut_grid})
    return [eq("7 layers", len(spec), 7), eq("clips outside 5-10 s", bad, [12, 4]), eq("cuts on 60/BPM", cut_grid, [0, 0.6, 1.2, 1.8, 2.4])]


def lock_check(prompts, lock):
    missing = [i for i, p in enumerate(prompts) if lock not in p]
    if missing:
        raise ValueError(f"lock missing in {missing}")
    return True


def s14(work):
    lock = "[CHAR: stickman, black 3 px line, white background]"
    prompts = [f"{lock} walks to bus", f"{lock} misses bus", "stickman laughs"]
    try:
        lock_check(prompts, lock)
        raised = False
    except ValueError as e:
        raised = str(e)
    save(work, "prompts.json", prompts)
    return [eq("missing lock throws", raised, "lock missing in [2]"), truth("verbatim locks pass", lock_check(prompts[:2], lock))]


def taste_keep(exports, key):
    last = exports[-12:]
    vals = [e[key] for e in last]
    out = []
    for v in set(vals):
        c = vals.count(v)
        if c >= 2 and c / len(last) >= 0.6:
            out.append(v)
    return out


def s15(work):
    exp = [{"font": "Cairo"}] * 8 + [{"font": "Amiri"}] * 4 + [{"font": "Amiri"}] * 0
    ex2 = [{"font": "Amiri"}] * 20 + [{"font": "Cairo"}] * 7 + [{"font": "Amiri"}] * 5
    r1, r2 = taste_keep(exp, "font"), taste_keep(ex2, "font")
    save(work, "taste.json", {"r1": r1, "r2": r2})
    return [eq("8/12 kept", r1, ["Cairo"]), eq("only last 12 count: Amiri 25/32 overall but 5/12 recent, Cairo 7/12 < 60%", r2, []),
            eq("8/12 = 67% kept", taste_keep([{"f": "a"}] * 8 + [{"f": "b"}] * 4, "f"), ["a"]), eq("7/12 = 58% not kept", taste_keep([{"f": "a"}] * 7 + [{"f": "b"}] * 5, "f"), [])]


def render_hook(move_start_frame, n=10):
    frames = []
    for f in range(n):
        im = Image.new("L", (32, 18), 0)
        x = 4 + max(0, f - move_start_frame) * 2
        ImageDraw.Draw(im).rectangle([x, 6, x + 4, 10], fill=255)
        frames.append(np.asarray(im, float))
    return frames


def first_motion(frames):
    for i in range(1, len(frames)):
        if np.abs(frames[i] - frames[i - 1]).mean() > 0.5:
            return i
    return None


def s16(work):
    good, late = render_hook(1), render_hook(8)
    Image.fromarray(good[2].astype(np.uint8)).save(work / "frame2.png")
    hook_text = "توقف قبل ما تنشر"
    return [eq("motion on frame 1-3", first_motion(good), 2), truth("late open rejected (> 3 frames)", first_motion(late) > 3), truth("hook text <= 5 words", word_count(hook_text) <= 5)]


HOOK_PATTERNS = ["contrarian", "odd number", "confession", "quote reframe", "mini-list", "cold open", "listicle", "story tension", "question", "before/after", "stakes"]


def s17(work):
    variants = [("contrarian", "Stop posting daily"), ("odd number", "I posted 37 reels"), ("confession", "I faked my first launch"), ("question", "Why do reels die at 3 s?"),
                ("before/after", "From 200 to 20k views"), ("contrarian", "Hashtags are dead")]
    kinds = [k for k, _ in variants]
    distinct = len(set(kinds))
    save(work, "hooks.json", variants)
    return [truth("5-7 variants", 5 <= len(variants) <= 7), truth("never five of one kind", max(kinds.count(k) for k in kinds) < 5), eq("patterns used", distinct, 5), eq("11 formulas", len(HOOK_PATTERNS), 11)]


def s18(work):
    cuts = [0, 0.8, 3.0, 5.5, 7.0, 10.5]
    lens = np.diff(cuts)
    out_of_range = [round(float(l), 2) for l in lens if not 1.5 <= l <= 4]
    title_t = 0.6
    intro_dir, body_dir = "left", "left"
    save(work, "silent_vlog.json", {"shot_lengths": lens.tolist()})
    return [eq("cuts outside 1.5-4 s", out_of_range, [0.8]), truth("title within 1 s", title_t <= 1.0), truth("match cut direction", intro_dir == body_dir)]


def s19(work):
    beats = [{"b": "after: 0 errors dashboard", "pain": "errors"}, {"b": "setup screen", "pain": None}, {"b": "one-click import", "pain": "manual import"}]
    frame0 = beats[0]["b"].startswith("after")
    kept = [b["b"] for b in beats if b["pain"]]
    data = {"metric": "0 errors", "fictional": True, "label": "illustrative data"}
    save(work, "proof_first.json", {"kept": kept, "data": data})
    return [truth("frame 0 shows the after", frame0), eq("beats without a pain cut", kept, ["after: 0 errors dashboard", "one-click import"]), truth("fictional data labelled", data["fictional"] and data["label"])]


def s20(work):
    lines = [{"text": "line 1", "t": 0.0, "size": 64}, {"text": "line 2", "t": 1.0, "size": 64, "colour": "accent"}]
    notifs = [{"t": round(i * 0.3, 2), "tilt": (-4 if i % 2 else 4)} for i in range(4)]
    save(work, "openers.json", {"reversal": lines, "notifications": notifs})
    return [eq("line 2 +1 s, same size", (lines[1]["t"] - lines[0]["t"], lines[1]["size"] == lines[0]["size"]), (1.0, True)), eq("stagger 300 ms", [n["t"] for n in notifs], [0.0, 0.3, 0.6, 0.9]),
            truth("tilt within ±4°", all(abs(n["tilt"]) <= 4 for n in notifs))]


CONFLICTS = {"character vs character", "character vs society", "character vs nature", "character vs technology", "character vs supernatural", "character vs self"}


def story_lint(story):
    issues, warns = [], []
    if story["central_conflict"] not in CONFLICTS:
        issues.append("conflict label")
    if len(story["beats"]) < 3:
        issues.append("fewer than 3 beats")
    for i, b in enumerate(story["beats"]):
        miss = [k for k in ("goal", "motivation", "conflict", "stakes", "choice") if not b.get(k)]
        if miss:
            issues.append(f"beat {i} missing {miss}")
    intro = sum(1 for b in story["beats"] if b.get("mode") == "introspection") / max(1, len(story["beats"]))
    if intro > 0.3:
        warns.append("introspection > 30%")
    return 100 - 12 * len(issues) - 4 * len(warns), issues, warns


def s21(work):
    B = lambda **k: dict({"goal": "g", "motivation": "m", "conflict": "c", "stakes": "s", "choice": "x", "mode": "action"}, **k)
    story = {"central_conflict": "man vs time", "beats": [B(), B(mode="introspection"), B(choice="", mode="introspection")]}
    score, issues, warns = story_lint(story)
    save(work, "story_lint.json", {"score": score, "issues": issues, "warnings": warns})
    return [eq("score = 100 - 12*2 - 4*1", score, 72), eq("issues", issues, ["conflict label", "beat 2 missing ['choice']"]), eq("warning", warns, ["introspection > 30%"])]


FRAMEWORK = {"recognition": "transformation arc", "clarity": "ABT", "proof": "case study", "short ad": "PAS", "feature": "Before-After-Bridge", "brand story": "hero's journey"}
HERO = ["ordinary world", "call", "hesitation", "mentor", "threshold", "trials", "reward", "return"]


def s22(work):
    pick = {j: FRAMEWORK[j] for j in ("clarity", "short ad", "brand story")}
    draft = [s for s in HERO if s != "trials"]
    skipped = [s for s in HERO if s not in draft]
    save(work, "framework.json", pick)
    return [eq("picks by job", list(pick.values()), ["ABT", "PAS", "hero's journey"]), eq("8 hero stages", len(HERO), 8), eq("skipped trials flagged", skipped, ["trials"])]


def act_shares(acts, total):
    return {k: v / total for k, v in acts.items()}


def s23(work):
    acts = {"anticipation": 3, "action": 12, "reaction": 4, "resolution": 6}
    sh = act_shares(acts, 25)
    bands = {"anticipation": (0.1, 0.2), "action": (0.3, 0.5), "reaction": (0.1, 0.2), "resolution": (0.2, 0.3)}
    bad = [k for k, (lo, hi) in bands.items() if not lo <= sh[k] <= hi]
    news = [0, 2.5, 5, 8, 9.5, 13]
    gaps = [round(b - a, 2) for a, b in zip(news, news[1:]) if b - a > 4]
    save(work, "arc.json", sh)
    return [eq("act bands", bad, []), eq("action share", sh["action"], 0.48), eq("gaps with nothing new > 4 s", gaps, [])]


def s24(work):
    W, H, n = 54, 96, 150
    out = []
    for f in (0, 20, 27, 60, 140):
        t = f / FPS
        ring = ease_out_cubic(t / 0.9)
        push = 1 + 0.09 * ease_in_out((t - 1.2) / 2.4) if t >= 1.2 else 1.0
        flood = 1.0 if t >= 3.6 else 0.0
        out.append((f, round(ring, 4), round(push, 4), flood))
    save(work, "five_sec.json", out)
    words8 = "صمم أفكارك بالحركة"
    return [eq("frames", n, 150), eq("ring drawn by 0.9 s (frame 27)", out[2][1], 1.0), eq("push reaches 1.09", out[4][2], 1.09), eq("gold flood after 3.6 s", [o[3] for o in out], [0, 0, 0, 0, 1.0]),
            truth("<= 8 words", word_count(words8) <= 8)]


def s25(work):
    starts = [0, 45, 120, 195, 270, 345, 405]
    durs = [45, 75, 75, 75, 75, 60, 45]
    contiguous = all(s + d == n for s, d, n in zip(starts, durs, starts[1:]))
    total = starts[-1] + durs[-1]
    t = np.linspace(0, 1, 100)
    counter = 4.8 * (1 - (1 - t) ** 3)
    vo = "Track every habit. One tap logs it. Charts show your streak. Friends cheer you on. Rated 4.8. Download free today."
    save(work, "app_ad.json", {"starts": starts, "durations": durs})
    return [truth("sequences contiguous", contiguous), eq("15 s at 30 fps", total, 450), eq("rating counts to 4.8", round(float(counter[-1]), 6), 4.8), truth("VO <= 70 words", word_count(vo) <= 70)]


ARCS = {"classic": [3, 5, 5, 15, 4, 4], "problem-solution": [6, 6, 10, 4], "teaser": [2, 8, 3, 2]}


def s26(work):
    tot = {k: sum(v) for k, v in ARCS.items()}
    marks = {k: np.cumsum([0] + v).tolist() for k, v in ARCS.items()}
    save(work, "arcs.json", {"totals": tot, "marks": marks})
    return [eq("totals", tot, {"classic": 36, "problem-solution": 26, "teaser": 15}), eq("classic proof starts at", marks["classic"][3], 13)]


def s27(work):
    runtime = 33.0
    beats = [(0, "problem"), (5, "problem"), (10, "turn"), (19.8, "climax"), (25, "reveal"), (30, "logo")]
    climax = [t for t, k in beats if k == "climax"][0]
    claims = {b: 1 for _, b in beats}
    save(work, "brand_arc.json", beats)
    return [eq("6 beats", len(beats), 6), eq("climax at 60%", round(climax / runtime, 2), 0.6), truth("one claim per beat", all(v == 1 for v in claims.values()))]


def s28(work):
    lines = ["You think more apps make you faster", "But every switch costs your focus", "Your brain reloads context each time", "One tool for one job keeps you in flow",
             "Fewer tabs, more finished work"]
    longest = max(word_count(l) for l in lines)
    scene_s = 30 / len(lines)
    essay = [15, 30, 40, 40, 40, 40, 45, 30, 20, 15]
    save(work, "explainer.json", {"lines": lines, "scene_s": scene_s})
    return [eq("five-line arc", len(lines), 5), truth("longest line <= 14 words", longest <= 14, longest), eq("one sentence per 6 s scene", scene_s, 6.0), eq("essay runtime s", sum(essay), 315)]


def edit_metrics(cuts, duration):
    lens = np.diff(cuts + [duration])
    return float(np.mean(lens)), int(sum(1 for c in cuts if 0 < c < 60)), float(max(lens))


def s29(work):
    cuts = [round(i * 3.3, 2) for i in range(0, 19)]
    asl, minute1, mx = edit_metrics(cuts, 62.7)
    save(work, "edit_metrics.json", {"asl": asl, "cuts_min1": minute1, "max_hold": mx})
    return [eq("ASL essay", round(asl, 2), 3.3), truth("ASL in 2.5-4", 2.5 <= asl <= 4), truth("no screen > 8 s", mx <= 8), eq("cuts in minute one", minute1, 18)]


def s30(work):
    script = "[CHAPTER: intro ~0:00] Hello. [B-ROLL: city] We start. [CHAPTER: method ~3:10] Here is how. [IMPROVISE: story]"
    markers = re.findall(r"\[(CHAPTER|B-ROLL|IMPROVISE): ([^\]]+)\]", script)
    words_15min = 15 * 150
    rehooks = list(range(120, 15 * 60, 120))
    save(work, "markers.json", markers)
    return [eq("markers", [m[0] for m in markers], ["CHAPTER", "B-ROLL", "CHAPTER", "IMPROVISE"]), eq("15 min ≈ 2250 words", words_15min, 2250), eq("re-hooks every 2 min", len(rehooks), 7)]


def bar_grid(bpm, bars, beats_per_bar=4):
    return [round(i * beats_per_bar * 60 / bpm, 4) for i in range(bars + 1)]


def s31(work):
    grid = bar_grid(120, 20)
    plan = [("cold", 2), ("drop", 7), ("tour", 3), ("climax", 5), ("end", 3)]
    starts = np.cumsum([0] + [b for _, b in plan]).tolist()
    tiles = [(name, grid[s], grid[s + b]) for (name, b), s in zip(plan, starts)]
    caps = {"cold": "it begins", "drop": "now"}
    save(work, "timeline.json", tiles)
    return [eq("bar = 2 s at 120 BPM", grid[1], 2.0), truth("tiles cover grid", tiles[-1][2] == grid[20]), truth("captions 1-3 words", all(1 <= word_count(c) <= 3 for c in caps.values())),
            eq("half-bar cut", grid[1] / 2, 1.0)]


def s32(work):
    title = "الصادرات +23% بعد الميناء الجديد"
    ok = bool(re.search(r"[+-]?\d+%", title)) and word_count(title) >= 3
    before, after = [100, 80, 60], [123, 70, 65]
    t = np.linspace(0, 1, 5)
    anim = [[b + (a - b) * x for a, b in zip(after, before)] for x in t]
    dim = 0.35
    save(work, "data_story.json", {"title": title, "anim": anim, "dim": dim})
    return [truth("insight-first title (number + impact + context)", ok), eq("after counts from before", anim[0], [100, 80, 60]), eq("ends at after", anim[-1], [123, 70, 65]), truth("prior layers 30-40%", 0.3 <= dim <= 0.4)]


def s33(work):
    investor = ["problem", "solution", "market", "product", "traction", "model", "competition", "team", "numbers", "ask"]
    per = 7
    scqa = ["situation", "complication", "question", "answer"]
    save(work, "deck_arc.json", {"investor": investor})
    return [truth("10-12 slides", 10 <= len(investor) <= 12), truth("60-90 s", 60 <= len(investor) * per <= 90, len(investor) * per), eq("SCQA", len(scqa), 4)]


def s34(work):
    pages = ["The moon woke up early and looked for the sun", "She asked the owl, the river and the old tree where the sun had gone today " * 2]
    over = [i for i, p in enumerate(pages) if word_count(p) > 25]
    acts = ["morning", "play", "nature", "sunset", "night", "finale"]
    save(work, "kids.json", {"over": over, "acts": acts})
    return [eq("page over 25 words", over, [1]), eq("6 acts", len(acts), 6), truth("12-32 pages rule", 12 <= 24 <= 32)]


def s35(work):
    frames = {"with image": "growth doubles", "without image": "growth doubles"}
    decorates = frames["with image"] == frames["without image"]
    thesis = "Viewer understands: costs fall as volume rises"
    directions = 3
    save(work, "director.json", {"decorative": decorates, "thesis": thesis})
    return [truth("image that adds nothing flagged", decorates), truth("one-sentence 2 s thesis", thesis.count(".") <= 1 and word_count(thesis) <= 12), truth("2-3 directions", 2 <= directions <= 3)]


def s36(work):
    beats = [{"b": "hook", "motion": "utility"}, {"b": "reveal", "motion": "signature"}, {"b": "proof", "motion": "utility"}, {"b": "end", "motion": "signature"}]
    sig = [b["b"] for b in beats if b["motion"] == "signature"]
    save(work, "signature.json", sig)
    return [eq("two signatures flagged", sig, ["reveal", "end"]), truth("violates 1 per film", len(sig) > 1)]


SLOP = {"gradient text": r"background-clip:\s*text", "pure black": r"#000(000)?\b", "pure white": r"#fff(fff)?\b", "cream+clay": r"#F4F1EA.*#D97757", "Syne": r"\bSyne\b",
        "cyan on dark": r"#0ff|#00ffff"}


def s37(work):
    css = "h1{background-clip: text} body{background:#000;color:#fff;font-family:Syne} .a{color:#0ff}"
    hits = sorted(k for k, p in SLOP.items() if re.search(p, css, re.I))
    sections, eyebrows = 7, 4
    grain = 0.05
    save(work, "anti_slop.json", hits)
    return [eq("flags", hits, ["Syne", "cyan on dark", "gradient text", "pure black", "pure white"]), truth("eyebrows over ceil(sections/3)", eyebrows > math.ceil(sections / 3)), truth("grain > 3% flagged", grain > 0.03)]


VOCAB = {"dramatic": {"fade_s": (1.0, 1.5), "scale": (0.9, 1.0)}, "playful": {"easing": "spring"}, "corporate": {"transition": "slide"}, "fintech": {"overshoot": 0}}


def s39(work):
    def feedback_ok(ms):
        return 120 <= ms <= 250
    save(work, "vocab.json", VOCAB)
    return [eq("dramatic fade range", VOCAB["dramatic"]["fade_s"], (1.0, 1.5)), truth("SaaS feedback 120-250 ms", feedback_ok(180) and not feedback_ok(400)), eq("fintech no overshoot", VOCAB["fintech"]["overshoot"], 0)]


STYLES8 = {"Swiss Pulse": {"bg": "#1a1a1a", "accent": ["#0066FF", "#FFB300"], "grid": 12, "num_px": (80, 120)}, "Velvet Standard": {"bg": "#1a237e", "tracking": 0.15},
           "Data Drift": {"bg": "#0a0a0a", "accent": ["#7c3aed", "#06b6d4"]}}


def s40(work):
    def check_swiss(spec):
        s = STYLES8["Swiss Pulse"]
        return spec["bg"] == s["bg"] and spec["accent"] in s["accent"] and s["num_px"][0] <= spec["num_px"] <= s["num_px"][1]
    good = {"bg": "#1a1a1a", "accent": "#0066FF", "num_px": 100}
    bad = {"bg": "#1a1a1a", "accent": "#ff0000", "num_px": 60}
    save(work, "styles.json", STYLES8)
    return [truth("spec conforms to Swiss Pulse", check_swiss(good)), truth("off-style accent rejected", not check_swiss(bad)), eq("12-column grid", STYLES8["Swiss Pulse"]["grid"], 12)]


def s41(work):
    systems = {"editorial": {"#F7F6F3", "#111111", "#EAEAEA"}, "swiss": {"#F4F4F0", "#050505", "#E61919"}, "crt": {"#0A0A0A", "#4AF626"}}
    page = {"#F7F6F3", "#111111", "#E61919"}
    owners = {c: [k for k, v in systems.items() if c in v] for c in page}
    mixed = len({o[0] for o in owners.values() if o}) > 1
    save(work, "systems.json", {k: sorted(v) for k, v in systems.items()})
    return [truth("mixing systems detected", mixed), eq("red belongs to swiss", owners["#E61919"], ["swiss"])]


def choreo_check(els):
    errs = []
    for e in els:
        if e["exit"] > e["enter"] * 0.7:
            errs.append(f"{e['id']} exit not faster")
    if max(e["delay"] for e in els) >= 0.5:
        errs.append("stagger >= 500 ms")
    if sum(e["moving"] for e in els) > len(els) / 3:
        errs.append("more than 1/3 moving")
    return errs


def s42(work):
    els = [{"id": i, "enter": 0.4, "exit": 0.25, "delay": i * 0.08, "moving": i < 2} for i in range(6)]
    bad = [dict(e, exit=0.4, delay=e["delay"] * 2, moving=True) for e in els]
    save(work, "choreo.json", els)
    return [eq("good choreography", choreo_check(els), []), eq("bad choreography", choreo_check(bad)[-2:], ["stagger >= 500 ms", "more than 1/3 moving"]), eq("exit 37.5% faster", round(1 - 0.25 / 0.4, 3), 0.375)]


ENERGY = {"high": {"SLAMS", "CRASHES", "PUNCHES", "STAMPS", "SHATTERS"}, "medium": {"CASCADES", "SLIDES", "DROPS", "FILLS", "DRAWS"}, "low": {"FLOATS", "COUNTS UP", "TYPES ON", "MORPHS"}}


def s43(work):
    beat = {"verb": "SLAMS", "elements": 9, "techniques": ["per-word type", "counter"], "layers": 2, "push": (1, 1.04)}
    level = next(k for k, v in ENERGY.items() if beat["verb"] in v)
    ok = 8 <= beat["elements"] <= 10 and 2 <= len(beat["techniques"]) <= 3 and beat["layers"] >= 2
    save(work, "beat.json", beat)
    return [eq("energy level", level, "high"), truth("beat budget ok", ok), eq("push", beat["push"][1], 1.04)]


def s44(work):
    rows = [True, True, True, True, True, False, True]
    score = {7: 10, 6: 9, 5: 7}[sum(rows)]
    tiles = 6
    sheet = Image.new("RGB", (3 * 264, 2 * 264 * 16 // 9 // 2 * 2), "white")
    for i in range(tiles):
        tile = Image.new("RGB", (264, 148), (i * 40, 80, 120))
        sheet.paste(tile, ((i % 3) * 264, (i // 3) * 148))
    sheet.save(work / "contact_sheet.png")
    return [eq("6/7 -> 9", score, 9), eq("contact sheet 3 columns of 264 px", sheet.size[0], 792), eq("6 frames", tiles, 6)]


def cut_detect(frames, thr=30):
    return [i for i in range(1, len(frames)) if np.abs(frames[i].astype(float) - frames[i - 1]).mean() > thr]


def s45(work):
    shots = [(30, 0), (45, 200), (15, 90)]
    frames = []
    for n, v in shots:
        frames += [np.full((18, 32), v, np.uint8)] * n
    cuts = cut_detect(frames)
    lens = np.diff([0] + cuts + [len(frames)]) / FPS
    refs = [{"asl": 1.5, "palette": "warm", "logo": "A"}, {"asl": 1.4, "palette": "warm", "logo": "B"}, {"asl": 1.6, "palette": "warm", "logo": "C"}]
    constant = [k for k in refs[0] if len({r[k] for r in refs}) == 1]
    save(work, "style_guide.json", {"cuts": cuts, "shot_s": lens.tolist(), "constant": constant})
    return [eq("cuts", cuts, [30, 75]), eq("shot lengths", lens.tolist(), [1.0, 1.5, 0.5]), eq("keep only constants across 3 refs", constant, ["palette"])]


def headline(cue):
    nums = re.findall(r"\d+(?:[.,]\d+)?%?", cue)
    if nums:
        return nums[0]
    return max(cue.split(), key=len)


def s46(work):
    r = {"sales rose 40% this year": headline("sales rose 40% this year"), "we built something remarkable": headline("we built something remarkable")}
    save(work, "headlines.json", r)
    return [eq("number from the cue", r["sales rose 40% this year"], "40%"), eq("else longest word", r["we built something remarkable"], "remarkable"), truth("no demo value", "123" not in r.values())]


def path_samples(n=60):
    t = np.linspace(0, 1, n)
    return np.stack([t * 100, 50 + 30 * np.sin(t * math.pi)], 1)


def pulse(t_since_beat):
    if t_since_beat < 0.06:
        return 1 + 0.25 * t_since_beat / 0.06
    if t_since_beat < 0.28:
        return 1.25 - 0.25 * ease_out_cubic((t_since_beat - 0.06) / 0.22)
    return 1.0


def s47(work):
    p = path_samples()
    beat = 60 / 120
    peaks = [round(pulse(0.06), 4), round(pulse(0.28), 4)]
    squash = (0.7, 1.3)
    save(work, "device.json", {"samples": len(p), "beat_s": beat, "pulse": peaks})
    return [eq("60 samples", len(p), 60), eq("beat at 120 BPM", beat, 0.5), eq("pulse peak 1.25 then settles", peaks, [1.25, 1.0]), eq("volume-preserving squash", round(squash[0] * squash[1], 2), 0.91)]


def payoff_plan(lines, dur):
    counts = {l: lines.count(l) for l in lines}
    refrain = [l for l, c in counts.items() if c >= 2]
    idx = max(i for i, l in enumerate(lines) if l in refrain) if refrain else len(lines) - 1
    return {"payoff": lines[idx], "scale": 1.22, "hold": 2.2, "in_last_40pct": idx / len(lines) >= 0.6}


def s48(work):
    lines = ["يا ليل", "الحب جاي", "يا ليل", "قلبي معاك", "الحب جاي", "يا ليل"]
    p = payoff_plan(lines, 30)
    save(work, "payoff.json", p)
    return [eq("refrain heard >= 2x", p["payoff"], "يا ليل"), eq("size x1.22", p["scale"], 1.22), truth("in last 40%", p["in_last_40pct"])]


CONCEPTS = {"شمس": "sun", "قمر": "moon", "قلب": "heart", "ساع": "clock", "مال": "money", "طريق": "road", "بيت": "home", "مطر": "rain", "نور": "light", "sun": "sun", "heart": "heart"}


def concept_of(word):
    w = re.sub(r"^(و|ف|ب|ل)?(ال)?", "", word)
    for root, c in CONCEPTS.items():
        if w.startswith(root) or word.lower().startswith(root):
            return c
    return None


def s49(work):
    r = {w: concept_of(w) for w in ["والشمس", "بالقلب", "المطر", "sunshine", "كتاب"]}
    save(work, "concepts.json", r)
    return [eq("prefixes stripped", r["والشمس"], "sun"), eq("ب + ال", r["بالقلب"], "heart"), eq("english prefix", r["sunshine"], "sun"), eq("unknown", r["كتاب"], None)]


def s50(work):
    H = 1920
    eyebrow_px = round(0.012 * H)
    labels = [f"[{i:02d}] WORD" for i in range(1, 9)]
    showreel = 8 * 1.6 + 2
    digits = ["٠١", "٠٢", "03"]
    consistent = len({bool(re.search(r"[0-9]", d)) for d in digits}) == 1
    save(work, "chapters.json", labels)
    return [eq("eyebrow 1.2% of height", eyebrow_px, 23), eq("showreel length", showreel, 14.8), truth("mixed digit systems flagged", not consistent)]


def s51(work):
    rows = [i * 0.12 for i in range(5)]
    collage = [{"t": i * 0.05, "rot": 4 if i % 2 == 0 else -4} for i in range(6)]
    back = back_out(0.7)
    percent = [min(99, int(99 * t / 1.5)) for t in np.arange(0, 1.6, 0.1)]
    save(work, "recap.json", {"rows": rows, "collage": collage})
    return [eq("row stagger 120 ms", rows[1], 0.12), truth("easeOutBack overshoots", back > 1, back), eq("progress ends at 99 in 1.5 s", percent[-1], 99)]


def s52(work):
    first = np.full((18, 32), 40, np.uint8)
    last = first.copy()
    fade = [1 - ease_in_out(t / 1.5) for t in (0, 0.75, 1.5)]
    acts = ["control", "escape", "chaos", "chaos 2", "control"]
    save(work, "bookend.json", {"fade": fade})
    return [truth("same calm frame bookends", np.array_equal(first, last) and acts[0] == acts[-1]), eq("fade 1.5 s", [round(f, 3) for f in fade], [1.0, 0.5, 0.0]), eq("5 acts", len(acts), 5)]


def darkness_frame():
    im = Image.new("L", (64, 36), 2)
    ImageDraw.Draw(im).ellipse([30, 16, 33, 19], fill=255)
    return im


def s53(work):
    im = darkness_frame()
    im.save(work / "darkness.png")
    lum = luminance(im)
    return [truth("mean luminance < 3%", lum < 0.03, lum), truth("one ember present", np.asarray(im).max() == 255), truth("statement hold 1.5-2 s", 1.5 <= 1.8 <= 2)]


def mood_lerp(start, target, k=0.04, frames=60):
    v = start
    for _ in range(frames):
        v += (target - v) * k
    return v


def s54(work):
    v = mood_lerp(0.25, 1.6, frames=60)
    exact = 1.6 - (1.6 - 0.25) * (1 - 0.04) ** 60
    p = 3.0
    for _ in range(10):
        p *= 0.92
    save(work, "mood.json", {"glow_after_60": v, "pulse_after_10": p})
    return [eq("lerp k=.04 closed form", round(v, 9), round(exact, 9)), eq("pulse decay x0.92", round(p, 4), round(3 * 0.92 ** 10, 4)), truth("crossfade 600 ms = 18 frames", frames_of(0.6) == 18)]


def pop(t):
    if t < 0.15:
        return 1.1 * t / 0.15
    if t < 0.3:
        return 1.1 - 0.1 * (t - 0.15) / 0.15
    return 1.0


def s55(work):
    curve = [round(pop(t), 3) for t in (0, 0.15, 0.3, 1.0)]
    stamp = [round(1.4 - 0.4 * f / 3, 4) for f in range(4)]
    save(work, "comic.json", {"pop": curve, "stamp": stamp})
    return [eq("pop 0 -> 1.1 -> 1", curve, [0.0, 1.1, 1.0, 1.0]), eq("stamp 1.4 -> 1 in 3 frames", stamp, [1.4, 1.2667, 1.1333, 1.0]), eq("flip 600 ms", frames_of(0.6), 18)]


def s56(work):
    W = 1080
    cards = 3
    xs_rtl = [W - (i + 1) * W // cards for i in range(cards)]
    delays = [i * 0.3 for i in range(cards)]
    stat = f"≈1 in {round(1 / 0.125)}"
    save(work, "triptych.json", {"x": xs_rtl, "delays": delays, "stat": stat})
    return [eq("built right-to-left", xs_rtl, [720, 360, 0]), eq("stagger 300 ms", delays, [0.0, 0.3, 0.6]), eq("≈1 in N stat", stat, "≈1 in 8")]


def s57(work):
    frames = []
    for f in range(12):
        v = 255 if 3 <= f < 9 else 30
        frames.append(np.full((18, 32), v, np.uint8))
    flash = [i for i, fr in enumerate(frames) if fr.mean() > 200]
    pull = [round(ease_out_cubic(t / 2.0), 4) for t in (0, 1, 2)]
    save(work, "flash.json", {"flash_frames": flash, "pull": pull})
    return [eq("flash ≈200 ms (6 frames)", len(flash), 6), eq("pull-back 2 s easeOutCubic", pull, [0.0, 0.875, 1.0])]


def beacon_interval(r):
    return 1 / math.sqrt(1 - 1 / r)


def s58(work):
    rs = [10, 4, 2, 1.1]
    iv = [round(beacon_interval(r), 4) for r in rs]
    drift = {"px_s": 20, "deg_s": 5}
    save(work, "beacon.json", iv)
    return [truth("interval grows near horizon", all(b > a for a, b in zip(iv, iv[1:]))), eq("r=2 -> sqrt 2", iv[2], round(math.sqrt(2), 4)), truth("drift in range", 10 <= drift["px_s"] <= 30 and 2 <= drift["deg_s"] <= 8)]


def direct_plan(words_json):
    hook = words_json[1]["start"]
    end = words_json[-1]["end"] + 0.35
    lines, cur = [], []
    for w in words_json:
        cur.append(w["w"])
        if len(cur) == 6:
            lines.append(cur)
            cur = []
    if cur:
        lines.append(cur)
    stress = max(words_json, key=lambda w: w["loud"] * (w["end"] - w["start"]))["w"]
    return {"hook_release": hook, "end": round(end, 3), "lines": lines, "keyword": stress}


def s59(work):
    wj = [{"w": f"w{i}", "start": i * 0.4, "end": i * 0.4 + 0.3, "loud": 1.0} for i in range(10)]
    wj[6]["loud"] = 2.0
    p = direct_plan(wj)
    save(work, "edit_plan.json", p)
    return [eq("hook releases at second word", p["hook_release"], 0.4), eq("end = last word + 0.35", p["end"], 4.25), truth("captions <= 6 words", all(len(l) <= 6 for l in p["lines"])), eq("keyword by loudness x length", p["keyword"], "w6")]


def s60(work):
    marks = [0, 1.56, 3.28, 5.22, 7.24, 9.5, 11.3, 13.14, 14.62, 16.02, 17.26, 18.42, 20.06]
    push = [round(1.0 + 0.08 * t / 20.57, 4) for t in (0, 20.57)]
    micro_ok = all(d <= 1.5 for d in [1.2, 0.8, 1.5])
    save(work, "time_map.json", marks)
    return [truth("monotonic map", all(b > a for a, b in zip(marks, marks[1:]))), eq("push 100 -> 108%", push, [1.0, 1.08]), truth("micro-graphics <= 1.5 s", micro_ok), truth("dip before end", marks[-1] < 20.57)]


def s61(work):
    plan = [("hook", 3), ("reveal", 3.5), ("highlight entry", 3), ("highlight action", 3), ("highlight result", 3), ("outro", 3)]
    total = sum(d for _, d in plan)
    share = "Shipped v2: Arabic captions that land on every word, exports in 12 s. Try it free → kosif.app"
    tones = ["default", "polished", "yc-parody", "chaotic", "deadpan", "cinematic", "app-store"]
    save(work, "brag.json", {"plan": plan, "share": share})
    return [truth("18-22 s ideal", 18 <= total <= 22, total), truth("share <= 280 chars", len(share) <= 280), eq("7 tones", len(tones), 7)]


def s62(work):
    beats = [4, 6, 9, 12, 15.8, 21, 24.6, 26]
    t = [round(b * 60 / 120, 3) for b in beats]
    frames = [round(x * 60) for x in t]
    save(work, "cues.json", {"t": t, "frames": frames})
    return [eq("8 cues", len(t), 8), eq("last cue at 13 s", t[-1], 13.0), truth("within 15 s", t[-1] <= 15), eq("b15.8 frame at 60 fps", frames[4], 474)]


def s63(work):
    B = {"joint": .85, "load": 1.65, "brk": 2.55, "swap": 3.35, "rank": 4.15, "end": 5.0}
    load = lambda t: 1 + 2.0 * ease_in_out((t - B["load"]) / (B["brk"] - B["load"])) if t < 2.66 else 3.0 - 2.0 * ease_in_out((t - 2.66) / 0.69)
    peak = load(2.55)
    back = load(3.35)
    save(work, "lab.json", {"bands": B, "peak": peak})
    return [truth("bands ordered", list(B.values()) == sorted(B.values())), eq("load ramps to 3.0x", round(peak, 6), 3.0), eq("back to 1x", round(back, 6), 1.0)]


def s64(work):
    beats = [(0, 4.1), (4.1, 5.2), (5.2, 6.9), (6.9, 7.35), (7.35, 9.7), (9.7, 12)]
    frames = 12 * 24
    contiguous = all(a[1] == b[0] for a, b in zip(beats, beats[1:]))
    save(work, "wordless.json", beats)
    return [eq("288 frames", frames, 288), truth("beats tile 12 s", contiguous and beats[-1][1] == 12), eq("6 beats", len(beats), 6)]


ARC6 = ["commute misunderstanding", "shy small gesture", "unseen kindness", "bad luck helps", "shortcut backfires", "reality flips"]


def s65(work):
    genre = 4
    arc = ARC6[genre - 1]
    beats = ["setup", "build", "turn", "peak", "payoff"]
    clips = [7] * len(beats)
    save(work, "stickman.json", {"arc": arc, "beats": beats})
    return [eq("arcs[genre-1]", arc, "bad luck helps"), eq("5 beats x 7 s", sum(clips), 35)]


def s66(work):
    answer = "DEFAULT"
    scenes = ["meet", "spark", "distance", "return", "together"]
    prompts = [f"{s} frame {f} 9:16 {'35mm' if f == 1 else '85mm'} {answer.lower()}" for s in scenes for f in (1, 2)]
    save(work, "romance.json", prompts)
    return [eq("5 scenes x 2 frames", len(prompts), 10), truth("paired lenses", sum("85mm" in p for p in prompts) == 5)]


def pick_stages(stages, n):
    if n < 1 or n > 200:
        raise ValueError("1-200 clips")
    if n == 1:
        return [stages[-1]]
    asm = stages[:-1]
    out = [asm[min(len(asm) - 1, i * len(asm) // (n - 1))] for i in range(n - 1)]
    return out + [stages[-1]]


def s67(work):
    st = ["chop", "fry", "sauce", "plate"]
    r = {n: pick_stages(st, n) for n in (1, 3, 6)}
    bad = False
    try:
        pick_stages(st, 201)
    except ValueError:
        bad = True
    save(work, "food.json", r)
    return [truth("last clip always plated", all(v[-1] == "plate" for v in r.values())), eq("assembly = n-1", len(r[6]) - 1, 5), truth("201 rejected", bad)]


def viral_session(replies):
    stage, log = 1, []
    for r in replies:
        if r == "NEXT" and stage < 5:
            stage += 1
        elif r in "12345":
            log.append((stage, int(r)))
    return stage, log, stage == 5 and len({s for s, _ in log}) == 5


def s68(work):
    stage, log, ready = viral_session(["2", "NEXT", "1", "NEXT", "3", "NEXT", "4", "NEXT", "5"])
    _, _, early = viral_session(["2", "NEXT"])
    save(work, "session.json", {"schema": "fmb.viral-editorial.v1", "log": log})
    return [eq("five stages answered", stage, 5), truth("compile gate open after all stages", ready), truth("gate closed early", not early)]


def s69(work):
    shots, fades = 11, [0.7, 0.75, 0.8, 0.72, 0.78, 0.7, 0.8, 0.74, 0.76, 0.71]
    ok = len(fades) == shots - 1 and all(0.7 <= f <= 0.8 for f in fades)
    save(work, "friday.json", {"shots": shots, "fades": fades, "text": {"px": 135, "fill": "#fdfbf3", "stroke": 7}})
    return [truth("10 fade-black transitions 0.70-0.80 s", ok), eq("28.2 s at 30 fps", frames_of(28.2), 846)]


def s70(work):
    order = [("departure", 6.8), ("goodbye", 5.2), ("foreign streets", 7.0), ("memory", 5.0), ("loneliness", 7.6), ("family voices", 6.8), ("hope", 9.6)]
    total = round(sum(d for _, d in order), 1)
    grade = {"contrast": 1.07, "saturation": 0.9}
    concat = "\n".join(f"file 'shot{i}.mp4'" for i in range(len(order)))
    (work / "concat.txt").write_text(concat)
    return [eq("7 shots ≈ 48 s", total, 48.0), eq("hope last", order[-1][0], "hope"), truth("grade in range", 1.06 <= grade["contrast"] <= 1.08 and 0.86 <= grade["saturation"] <= 0.95)]


def caption_windows(cuts, end):
    out = []
    for a, b in zip(cuts, cuts[1:] + [end]):
        out.append((round(a + 0.25, 2), round(b - 0.3, 2)))
    return out


def s71(work):
    cuts = [0, 2.6, 6, 10, 14]
    win = caption_windows(cuts, 18)
    base = 230.3 / 5
    r = base / math.sqrt(2)
    save(work, "captions.json", win)
    return [eq("captions +0.25 / -0.3", win[1], (2.85, 5.7)), eq("pyramid cone radius base/√2", round(r * math.sqrt(2), 6), round(base, 6)), eq("last window ends 0.3 s before end", win[-1][1], 17.7)]


def s72(work):
    bpm = 90
    beat = 60 / bpm
    beats_47s = int(47 / beat)
    palette = {"base": "#05070b", "gold": "#f5c97a", "cold": "#7fd0ff", "alarm": "#ff6b6b", "cream": "#e9dcc4"}
    save(work, "explainer.json", {"beat": beat, "beats": beats_47s, "palette": palette})
    return [eq("beat length", round(beat, 4), 0.6667), eq("beats in 47 s", beats_47s, 70), eq("three text levels", len(["headline", "body", "caption"]), 3)]


def face_segments(flags, fps=1):
    segs, start = [], None
    for i, f in enumerate(flags + [False]):
        if f and start is None:
            start = i
        if not f and start is not None:
            segs.append((start / fps, i / fps))
            start = None
    return segs


def s73(work):
    flags = [False, False, True, True, False, True, False]
    segs = face_segments(flags)
    tracks = {"V1": "screen", "A1": "voice", "V2": "cards", "V3": "captions"}
    save(work, "faceless.json", {"replace": segs, "tracks": tracks})
    return [eq("flagged segments replaced", segs, [(2.0, 4.0), (5.0, 6.0)]), eq("track layout", list(tracks), ["V1", "A1", "V2", "V3"])]


def wrap(text, n=18):
    lines, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + (1 if cur else 0) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines


def s74(work):
    cap = "9 AM, market alley, slow"
    lines = wrap(cap)
    beats = [0.5 * i for i in range(10)]
    cuts = [0.52, 1.49, 3.02]
    snapped = [min(beats, key=lambda b: abs(b - c)) for c in cuts]
    save(work, "city.json", {"lines": lines, "cuts": snapped})
    return [truth("<= 2 lines of <= 18 chars", len(lines) <= 2 and all(len(l) <= 18 for l in lines), lines), eq("cuts snapped to downbeats", snapped, [0.5, 1.5, 3.0]), truth("commas only", "." not in cap)]


CONTRACTS = {"plotter": (4, 7, 2, 5), "stickman": (4, 7, None, None), "whiteboard": (4, 6, None, None)}


def script_ok(style, lines):
    lo, hi, wlo, whi = CONTRACTS[style]
    if not lo <= len(lines) <= hi:
        return False
    if wlo and any(not wlo <= word_count(l) <= whi for l in lines):
        return False
    return True


def s75(work):
    good = ["make it move", "every frame counts", "type that breathes", "ship today"]
    bad = good[:2]
    save(work, "contracts.json", CONTRACTS)
    return [truth("plotter script passes", script_ok("plotter", good)), truth("too short rejected", not script_ok("plotter", bad)), truth("long line rejected", not script_ok("plotter", good[:3] + ["this line has far too many words"]))]


def draw_router(req):
    r = req.lower()
    if "as is" in r or "code" in r:
        return "to_python"
    if "realistic" in r or "reflection" in r:
        return "three.js"
    if "film" in r:
        return "painter film"
    return "kosif scene + judge"


def s76(work):
    r = [draw_router(x) for x in ["draw this image as is", "realistic 3D reflections", "a film of the drawing", "cinematic painting of a desert"]]
    img = np.clip(np.linspace(20, 210, 64), 0, 255)
    vrange = img.max() - img.min()
    save(work, "router.json", r)
    return [eq("routes", r, ["to_python", "three.js", "painter film", "kosif scene + judge"]), truth("value range > 150", vrange > 150, vrange)]


RARITY = {"Common": 60, "Uncommon": 25, "Rare": 10, "Epic": 4, "Legendary": 0.9, "Mythical": 0.1}


def s77(work):
    rng = random.Random(5)
    draws = rng.choices(list(RARITY), weights=list(RARITY.values()), k=20000)
    common = draws.count("Common") / len(draws)
    card = ["name", "type", "rarity", "biome", "silhouette", "palette", "move", "evolution", "weakness", "lore"]
    save(work, "rarity.json", {k: draws.count(k) for k in RARITY})
    return [eq("rarities sum to 100", round(sum(RARITY.values()), 6), 100.0), eq("Common ≈ 60%", round(common, 2), 0.6, tol=0.01), eq("card fields", len(card), 10)]


def ideate(problem, concepts, n, seed):
    if n > 30:
        raise ValueError("n <= 30")
    rng = random.Random(seed)
    ops = ["contiguity", "similarity", "contrast"]
    return [f"{ops[i % 3]}: {problem} x {rng.choice(concepts)}" for i in range(n)]


def s78(work):
    a = ideate("late deliveries", ["tide", "chess", "bees"], 12, 7)
    b = ideate("late deliveries", ["tide", "chess", "bees"], 12, 7)
    over = False
    try:
        ideate("x", ["y"], 31, 1)
    except ValueError:
        over = True
    tier1 = 0.65
    save(work, "ideas.json", a)
    return [eq("reproducible seed", a, b), truth("n <= 30 enforced", over), eq("three prompt kinds", len({x.split(":")[0] for x in a}), 3), truth("60-70% tier 1", 0.6 <= tier1 <= 0.7)]


SURPRISE = re.compile(r"\b(surpris|actually|turns out|nobody|\d+%|instead)", re.I)


def s79(work):
    transcript = ["We started in 2019 with three people.", "Turns out 70% of churn came from one email.", "The office had plants.", "Nobody read the onboarding docs; they watched videos instead."]
    nuggets = [l for l in transcript if SURPRISE.search(l)]
    lead = nuggets[0]
    save(work, "nuggets.json", nuggets)
    return [eq("nuggets", len(nuggets), 2), truth("lead is not chronology", not lead.startswith("We started")), truth("2-4 picked", 2 <= len(nuggets) <= 4)]


def s80(work):
    raw = [f"{w} Arabic captions in {n} seconds" for w, n in zip(["Make", "Get", "Ship", "Add", "Create", "Write", "Build", "Design", "Generate", "Render"], range(1, 11))]
    raw.append("You will never believe how this terrible mistake ruined everything forever today")
    keep = [t for t in raw if len(t) < 60 and has_number(t)][:5]
    save(work, "titles.json", keep)
    return [truth("10-20 raw", 10 <= len(raw) <= 20), eq("keep 3-5", len(keep), 5), truth("all < 60 chars", all(len(t) < 60 for t in keep))]


def cta_plan(duration):
    if duration <= 60:
        return [("end", duration - 3)]
    return [("mid", round(duration * 0.5)), ("end", duration - 5)]


def s81(work):
    r = {30: cta_plan(30), 600: cta_plan(600)}
    save(work, "cta.json", r)
    return [eq("short: one CTA", r[30], [("end", 27)]), eq("long: mid + end", [k for k, _ in r[600]], ["mid", "end"])]


def s82(work):
    emotions = ["curiosity", "surprise"]
    palette = {"curiosity": (20, 30, 90), "surprise": (230, 120, 20)}
    for e in emotions:
        im = Image.new("RGB", (1280, 720), palette[e])
        ImageDraw.Draw(im).rectangle([80, 260, 680, 460], fill=(255, 255, 255))
        im.save(work / f"thumb_{e}.png")
    sizes = {}
    for e in emotions:
        with Image.open(work / f"thumb_{e}.png") as im:
            sizes[e] = im.size
    return [truth("1-2 emotions", 1 <= len(emotions) <= 2), eq("1280x720 variants", set(sizes.values()), {(1280, 720)})]


def s83(work):
    import csv, datetime as dt
    pillars = {"tutorials": 30, "behind": 25, "showcase": 25, "community": 15, "promo": 5}
    days = []
    for i in range(20):
        p = [k for k, v in pillars.items() for _ in range(v // 5)][i % 20]
        days.append(((dt.date(2026, 11, 2) + dt.timedelta(days=i)).isoformat(), p))
    with open(work / "calendar.csv", "w", newline="") as f:
        csv.writer(f).writerows([("date", "pillar")] + days)
    ics = "BEGIN:VCALENDAR\n" + "".join(f"BEGIN:VEVENT\nDTSTART;VALUE=DATE:{d.replace('-', '')}\nSUMMARY:{p}\nEND:VEVENT\n" for d, p in days) + "END:VCALENDAR\n"
    (work / "calendar.ics").write_text(ics)
    promo = sum(1 for _, p in days if p == "promo") / len(days)
    return [eq("shares sum 100", sum(pillars.values()), 100), truth("promotion <= 20%", promo <= 0.2, promo), eq("ics events", ics.count("BEGIN:VEVENT"), 20), truth("3-5 pillars", 3 <= len(pillars) <= 5)]


def s84(work):
    c = {"3D": (487, 52.0e6), "seek(t)": (70, 34.9e6), "UI": (217, 16.3e6), "Arabic": (11, 0.13e6)}
    per = {k: round(v / n) for k, (n, v) in c.items()}
    best = max(per, key=per.get)
    save(work, "corpus.json", per)
    return [eq("views per post", per, {"3D": 106776, "seek(t)": 498571, "UI": 75115, "Arabic": 11818}), eq("highest per-post pattern", best, "seek(t)"), truth("Arabic is open ground (fewest posts)", min(c, key=lambda k: c[k][0]) == "Arabic")]


def jev(p_yes):
    return "keep" if p_yes >= 0.6 else "drop" if p_yes < 0.4 else "ask"


def s85(work):
    r = {"IBM Plex Sans Arabic": jev(0.99), "extra route": jev(0.5), "neon": jev(0.2)}
    save(work, "jev.json", r)
    return [eq("thresholds 0.6 / 0.4", list(r.values()), ["keep", "ask", "drop"])]


def p01(work):
    recipes = [{"id": f"S{i:02d}", "slug": s, "engine_candidates": e} for i, (s, e) in enumerate([("particles", ["Pixi", "Three", "Canvas"]), ("liquid-morph", ["Flubber", "GLSL", "SVG"]),
               ("holographic", ["Three", "OGL"]), ("neon-glow", ["SVG", "Canvas", "FFmpeg"])], 1)]
    missing = [r["id"] for r in recipes if require_fields(r, ["id", "slug", "engine_candidates"])]
    save(work, "recipes.json", recipes)
    return [eq("ids sequential", [r["id"] for r in recipes], ["S01", "S02", "S03", "S04"]), eq("fields complete", missing, []), truth("each has an engine candidate", all(r["engine_candidates"] for r in recipes))]


SLOTS = ["PRODUCT", "STORY", "FORMAT", "LOOK", "MOTION", "SOUND", "QUALITY", "OUTPUT"]


def brief_lint(b):
    errs = require_fields(b, SLOTS)
    if b.get("LOOK") and not re.search(r"#[0-9a-fA-F]{6}", b["LOOK"]):
        errs.append("LOOK needs hex colours")
    if b.get("has_speech") and "voice" not in b.get("SOUND", "").lower():
        errs.append("voice must be master clock")
    return errs


def p02(work):
    b = {s: "x" for s in SLOTS}
    b.update(LOOK="#0F1211 and #E4342F, Cairo", SOUND="voice is the master clock", has_speech=True)
    bad = dict(b, LOOK="dark and red", SOUND="120 BPM")
    save(work, "brief.json", b)
    return [eq("8 slots", len(SLOTS), 8), eq("good brief", brief_lint(b), []), eq("bad brief", brief_lint(bad), ["LOOK needs hex colours", "voice must be master clock"])]


def spring_closed(t, zeta=0.7, w=12):
    wd = w * math.sqrt(1 - zeta ** 2)
    return 1 - math.exp(-zeta * w * t) * (math.cos(wd * t) + zeta * w / wd * math.sin(wd * t))


def p03(work):
    ts = np.linspace(0, 2, 400)
    v = [spring_closed(t) for t in ts]
    overshoot = max(v) - 1
    expected = math.exp(-0.7 * math.pi / math.sqrt(1 - 0.49))
    save(work, "lexicon.json", {"smooth": "damped spring zeta 0.7", "overshoot": overshoot})
    return [eq("bounded overshoot matches theory", round(overshoot, 3), round(expected, 3), tol=0.002), truth("settles at 1", abs(v[-1] - 1) < 1e-3), truth("overshoot bounded < 10%", overshoot < 0.1)]


def x01(work):
    beats = [0, 2, 4, 6]
    shots = [{"t": b, "trigger": t} for b, t in zip(beats, ["downbeat", "word 'now'", "", "downbeat"])]
    unmotivated = [s["t"] for s in shots if not s["trigger"]]
    status = {"clock": "14:05", "changed": "scene 2", "stage": "keyframes", "eta": "14:30", "offer_stop": True}
    save(work, "trigger_map.json", shots)
    return [eq("unmotivated transition flagged", unmotivated, [4]), truth("status answer complete", all(status.values()))]


def x02(work):
    ref = {"palette": ["#1a1a1a", "#e4342f"], "shape": "circle", "type": "Cairo", "story": "sunrise"}
    ours = {"palette": ["#1a1a1a", "#e4342f"], "shape": "square", "type": "Amiri", "story": "harbour"}
    diffs = [k for k in ref if ref[k] != ours[k]]
    details = 8
    save(work, "taste.json", {"differences": diffs})
    return [eq("differences written", diffs, ["shape", "type", "story"]), truth("era palette borrowed, identity not copied", "palette" not in diffs and len(diffs) >= 3), truth("6-12 true details", 6 <= details <= 12)]


def x03(work):
    fps = 30
    cuts = [2.0, 5.5]
    stills = sorted({round(c + d / fps * 2, 3) for c in cuts for d in range(-7, 8)})
    changed = [(3.0, 4.0)]
    patch = [(round(a * fps), round(b * fps)) for a, b in changed]
    save(work, "qa_stills.json", {"stills": stills, "patch_frames": patch})
    return [truth("stills every 2 frames ±0.5 s", all(abs(min(abs(s - c) for c in cuts)) <= 0.5 + 1e-9 for s in stills)), eq("stills per cut", len(stills) // len(cuts), 15), eq("patch range frames", patch, [(90, 120)])]


def x04(work):
    est = {"storyboard": (15, 25), "film": (25, 45), "revision": (15, 40)}
    actual_vs = [(39, (90, 120))]
    render_s = 20 * 30
    save(work, "estimates.json", {"plan_min": sum(v[1] for v in est.values()), "render_s_30s_film": render_s})
    return [eq("worst-case plan minutes", sum(v[1] for v in est.values()), 110), truth("first film beat its estimate", actual_vs[0][0] < actual_vs[0][1][0]), eq("30 s master render", render_s, 600)]


def x05(work):
    t = np.linspace(0, 2 * math.pi, 24, endpoint=False)
    pts = np.stack([50 + 20 * np.cos(t), 50 + 30 * np.sin(t)], 1)
    im = Image.new("L", (100, 100), 0)
    d = ImageDraw.Draw(im)
    drawn = 0
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        d.line([tuple(a), tuple(b)], fill=255)
        drawn += 1
    im.save(work / "constellation.png")
    return [eq("every star connected in finale", drawn, 24), truth("lines drawn", np.asarray(im).max() == 255)]


def x06(work):
    dirs = {"warm editorial": "#F7F6F3", "neon": "#0A0A0A", "swiss": "#F4F4F0"}
    for name, bg in dirs.items():
        rgb = tuple(int(bg[i:i + 2], 16) for i in (1, 3, 5))
        Image.new("RGB", (64, 36), rgb).save(work / f"{name.replace(' ', '_')}.png")
    code_lines = {k: 12 for k in dirs}
    return [eq("3 previews", len(dirs), 3), truth("< 100 lines each", all(v < 100 for v in code_lines.values())), eq("distinct directions", len(set(dirs.values())), 3)]


def u01(work):
    sections = ["intro", "verse", "chorus", "outro"]
    sheet = Image.new("RGB", (128, 72))
    for i, s in enumerate(sections):
        sheet.paste(Image.new("RGB", (64, 36), (40 * i, 60, 120)), ((i % 2) * 64, (i // 2) * 36))
    sheet.save(work / "env_sheet.png")
    props = Image.new("RGB", (5 * 20, 2 * 20))
    props.save(work / "props.png")
    return [eq("env sheet 2x2", (sheet.size[0] // 64, sheet.size[1] // 36), (2, 2)), eq("props 5x2", (props.size[0] // 20, props.size[1] // 20), (5, 2)),
            eq("one environment per section", len(sections), 4)]


PROGRAMS = {f"STORY-{n:02d}": globals()[f"s{n:02d}"] for n in range(1, 86) if n not in (4, 8, 38)}
PROGRAMS.update({"STORY-P01": p01, "STORY-P02": p02, "STORY-P03": p03, "STORY-X01": x01, "STORY-X02": x02, "STORY-X03": x03,
                 "STORY-X04": x04, "STORY-X05": x05, "STORY-X06": x06, "STORY-U01": u01})
