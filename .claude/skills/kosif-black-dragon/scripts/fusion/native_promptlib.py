#!/usr/bin/env python3
"""native_promptlib: index/search a video-prompt case library (data/videos.json schema
of yihui-dev/awesome-opus5-5-videos, MIT) and lint a new code-as-video prompt against
patterns we derived. Own code; rules are our own wording. stdlib only."""
import argparse, json, re, sys, tempfile, os, collections

DEFAULT_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                            "data", "opus_video_cases_index.json")

# Each rule: id, label, regex (any match = present), weight, advice (our wording)
RULES = [
 ("duration", "Total length stated", r"\b\d+\s*(s|sec|secs|seconds?|-second|min|minutes?)\b", 2,
  "Say how long the piece runs; pacing cannot be planned without it."),
 ("format", "Canvas size / fps / aspect", r"\b\d{3,4}\s*[x×]\s*\d{3,4}\b|\b\d{2,3}\s*fps\b|\b(16:9|9:16|1:1|4:5)\b", 2,
  "Give resolution or aspect and frame rate so layout and export are fixed."),
 ("structure", "Beats / scenes / storyboard", r"storyboard|shot list|beat sheet|\bscene\s*\d|\bshot\s*\d|\bbars?\b|\bact\s*\d|\d+\s*scenes", 3,
  "Break the piece into numbered scenes or beats, each with one idea."),
 ("banned", "Explicit avoid-list", r"\b(banned|avoid|never|no\s+(glow|particles?|gradients?|bounce|bouncy|lens flare|neon|stock)|don'?t|do not)\b", 3,
  "Add a short list of forbidden cliches; most template-look comes from default effects."),
 ("palette", "Palette / typography named", r"#[0-9a-fA-F]{6}\b|palette|\bfont\b|typeface|monochrome|black and white|accent colou?r", 2,
  "Name colours and one typeface instead of piling adjectives."),
 ("motion", "Easing / motion language", r"\beas(e|ing)\b|\bspring|overshoot|\bmatch cut|hard cut|kinetic|dolly|parallax|morph", 2,
  "Describe how things move (easing, cuts, camera) in director terms."),
 ("determinism", "Time-driven frames", r"seek\(|\?t=|deterministic|function of (time|t)\b|timeline|requestAnimationFrame|frame-?exact", 2,
  "Make every frame a pure function of time t so it can be scrubbed and rendered in parallel."),
 ("tech", "Tech / dependency constraint", r"single[- ](file|html)|self-contained|no (external|libraries|library|dependencies|assets)|canvas|svg|three\.?js|remotion|hyperframes|gsap|p5", 2,
  "State the stack and whether external assets or libraries are allowed."),
 ("audio", "Sound plan", r"web audio|synthes|music|soundtrack|voice-?over|tts|\bbpm\b|sfx|audio", 1,
  "Say where music/voice comes from (synthesized, TTS, provided file) and tempo."),
 ("loop", "Opening/ending intent", r"\bloop|last frame|final frame|ends? (on|with)|outro|closing", 1,
  "State how it ends (loop back, hold on logo, fade)."),
 ("verify", "Self-check step", r"screenshot|inspect frames?|check (the )?frames?|verify|review your|iterate|playwright|headless", 2,
  "Ask the model to sample frames and fix overlaps before the final render."),
 ("ask_first", "Inputs / clarify first", r"ask me|<inputs>|before you (start|begin)|first (ask|show)|confirm", 1,
  "For templates, list the inputs the model must request before building."),
]
VAGUE = re.compile(r"\b(cool|epic|amazing|awesome|nice|beautiful|stunning|modern|slick|professional)\b", re.I)


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if isinstance(d, dict) and isinstance(d.get("items"), list):
        d = d["items"]  # KOSIF metadata-only index (no third-party prompt text)
    if not isinstance(d, list):
        raise SystemExit("data must be a list")
    return d


def search(data, category=None, keyword=None, tag=None, author=None, remake=None, full=False, limit=20):
    kws = [k.lower() for k in (keyword or "").split() if k]
    out = []
    for x in data:
        if category and x.get("category") != category: continue
        if tag and tag not in x.get("tech_tags", []): continue
        if author and author.lower() not in x.get("author", "").lower(): continue
        if remake is not None and bool(x.get("has_remake")) != remake: continue
        hay = (x.get("prompt", "") + " " + x.get("title", "") + " " + x.get("slug", "")).lower()
        if kws and not all(k in hay for k in kws): continue
        out.append((sum(hay.count(k) for k in kws), x))
    out.sort(key=lambda t: (-t[0], len(t[1].get("prompt", ""))))
    res = []
    for s, x in out[:limit]:
        r = {k: x.get(k) for k in ("slug", "category", "tech_tags", "author", "post_url", "title", "prompt_partial")}
        r["score"] = s
        r["prompt_len"] = len(x.get("prompt", "")) or x.get("prompt_chars", 0)
        r["prompt"] = x["prompt"] if full else x.get("prompt", "")[:200].replace("\n", " ")
        res.append(r)
    return {"total_matches": len(out), "results": res}


def stats(data):
    c = collections.Counter
    full = [x for x in data if not x.get("prompt_partial")]
    return {"count": len(data), "full_prompts": len(full),
            "categories": c(x["category"] for x in data),
            "tech_tags": c(t for x in data for t in x.get("tech_tags", [])).most_common(),
            "rule_prevalence": ({r[0]: sum(bool(re.search(r[2], x.get("prompt", ""), re.I)) for x in full) for r in RULES}
                                if any(x.get("prompt") for x in full) else "n/a: metadata-only index (prompt texts not bundled)")}


def lint(text):
    findings, score, maxs = [], 0, 0
    for rid, label, rx, w, adv in RULES:
        maxs += w
        if re.search(rx, text, re.I): score += w
        else: findings.append({"rule": rid, "missing": label, "advice": adv, "weight": w})
    words = len(text.split())
    notes = []
    if words < 25: notes.append("Very short: fine for a one-liner experiment, expect the model to pick everything.")
    if words > 1500: notes.append("Very long: split into spec + storyboard files.")
    v = sorted(set(m.group(0).lower() for m in VAGUE.finditer(text)))
    if v: notes.append("Vague adjectives without specifics: " + ", ".join(v))
    findings.sort(key=lambda f: -f["weight"])
    return {"score": score, "max": maxs, "pct": round(100 * score / maxs), "words": words,
            "findings": findings, "notes": notes}


def self_test():
    d = tempfile.mkdtemp(prefix="promptlib_")
    p = os.path.join(d, "videos.json")
    data = [
     {"slug": "a-1", "author": "A", "category": "motion", "tech_tags": ["svg"], "prompt": "A 15 seconds 1920x1080 30fps SVG kinetic piece. Scene 1 logo, scene 2 chart. Banned: glow, bouncy easing. Font Inter, palette #111111. Seek(t) deterministic. Verify with screenshot. Ends on last frame loop. Music 120 BPM.", "prompt_partial": False, "has_remake": True},
     {"slug": "b-2", "author": "B", "category": "3d", "tech_tags": ["threejs"], "prompt": "make a cool island scene", "prompt_partial": False, "has_remake": False},
     {"slug": "c-3", "author": "C", "category": "motion", "tech_tags": ["canvas"], "prompt": "", "prompt_partial": True, "has_remake": False}]
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f)
    L = load(p)
    r = search(L, category="motion", keyword="chart")
    assert r["total_matches"] == 1 and r["results"][0]["slug"] == "a-1"
    assert search(L, tag="threejs")["total_matches"] == 1
    assert search(L)["total_matches"] == 3
    s = stats(L)
    assert s["count"] == 3 and s["full_prompts"] == 2 and s["categories"]["motion"] == 2
    good, bad = lint(data[0]["prompt"]), lint(data[1]["prompt"])
    assert good["pct"] >= 85, good
    assert bad["pct"] <= 25 and any("cool" in n for n in bad["notes"]), bad
    assert bad["findings"][0]["weight"] == 3
    print("self-test OK: search/stats/lint verified; good=%d%% bad=%d%% (tmp %s)" % (good["pct"], bad["pct"], d))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="JSON output (always JSON; flag kept for the Dragon convention)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("search"); s.add_argument("--data", default=DEFAULT_DATA)
    s.add_argument("--category"); s.add_argument("--keyword"); s.add_argument("--tag"); s.add_argument("--author")
    s.add_argument("--remake", choices=["yes", "no"]); s.add_argument("--full", action="store_true"); s.add_argument("--limit", type=int, default=20)
    t = sp.add_parser("stats"); t.add_argument("--data", default=DEFAULT_DATA)
    l = sp.add_parser("lint"); g = l.add_mutually_exclusive_group(required=True)
    g.add_argument("--text"); g.add_argument("--file")
    sp.add_parser("patterns"); sp.add_parser("self-test")
    a = ap.parse_args()
    if a.cmd == "self-test": return self_test()
    if a.cmd == "patterns":
        out = [{"id": r[0], "label": r[1], "weight": r[3], "advice": r[4]} for r in RULES]
    elif a.cmd == "search":
        out = search(load(a.data), a.category, a.keyword, a.tag, a.author,
                     None if not a.remake else a.remake == "yes", a.full, a.limit)
    elif a.cmd == "stats":
        out = stats(load(a.data))
    else:
        txt = a.text if a.text is not None else open(a.file, encoding="utf-8").read()
        out = lint(txt)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
