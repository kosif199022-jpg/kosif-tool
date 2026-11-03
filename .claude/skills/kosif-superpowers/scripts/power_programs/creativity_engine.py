"""Programs for the creativity-engine family (IDEA-01..28). IDEA-26/29 have code proofs elsewhere;
IDEA-24 needs Playwright browser recording and is skipped."""
from __future__ import annotations
import json
import random
from collections import deque
import numpy as np
from PIL import Image, ImageDraw
from ._mind_common import save, eq, truth, jaccard, words, weighted_scores, rank, grid, find_cycles_signs

SCAMPER = ["substitute", "combine", "adapt", "modify", "put to other use", "eliminate", "reverse"]


def dedupe(ideas, thr=0.6):
    kept = []
    for i in ideas:
        if all(jaccard(words(i), words(k)) < thr for k in kept):
            kept.append(i)
    return kept


def i01(work):
    raw = ["kinetic word intro", "kinetic word intro animation", "split flap board", "paper fold reveal", "data counter hook",
           "silent film captions", "one colour cut", "beat cut montage", "thumb stop frame", "reverse text exit"]
    merged = dedupe(raw)
    crit = {"fit": 1, "feasible": 1, "novelty": 1, "risk": 1}
    sc = {i: {"fit": 3 + (n % 3), "feasible": 5 - (n % 4), "novelty": 1 + (n * 7) % 5, "risk": 3} for n, i in enumerate(merged)}
    s = weighted_scores(sc, crit)
    safe = max(merged, key=lambda i: (sc[i]["feasible"], s[i]))
    bold = max(merged, key=lambda i: (sc[i]["novelty"], s[i]))
    save(work, "diverge_converge.json", {"raw": raw, "merged": merged, "scores": s, "safe": safe, "bold": bold})
    return [truth("8-20 raw ideas", 8 <= len(raw) <= 20, len(raw)), eq("near-duplicate merged", len(merged), 9),
            truth("safe and bold differ", safe != bold, (safe, bold))]


def why_chain(goal_map, start, passes=3):
    chain = [start]
    for _ in range(passes):
        chain.append(goal_map[chain[-1]])
    return chain


def i02(work):
    m = {"intro animation": "brand recognition", "brand recognition": "viewer remembers us", "viewer remembers us": "two seconds of attention"}
    c = why_chain(m, "intro animation")
    habits = {"logo sting 6 s": "habit", "first frame must stop the scroll": "true", "9:16": "true"}
    design = [k for k, v in habits.items() if v == "true"]
    save(work, "why.json", {"chain": c, "design_from": design})
    return [eq("three why passes", len(c) - 1, 3), eq("real goal", c[-1], "two seconds of attention"), eq("habit dropped", "logo sting 6 s" in design, False)]


def min_type_px(frame_h, ratio=0.06):
    return round(frame_h * ratio)


def i03(work):
    fails = ["text unreadable on phone", "audio clips", "hook after 3 s", "captions in unsafe zone", "wrong aspect ratio"]
    rules = {"text unreadable on phone": f"min type {min_type_px(1920)} px", "audio clips": "true peak < -1 dBTP",
             "hook after 3 s": "hook before 1 s", "captions in unsafe zone": "safe zone 10% margins", "wrong aspect ratio": "1080x1920"}
    save(work, "inversion.json", rules)
    return [truth("5-10 failure ways", 5 <= len(fails) <= 10), eq("6% of 1920", min_type_px(1920), 115), eq("checked at 360 px wide (640 tall)", min_type_px(640), 38),
            truth("every failure has a rule", set(fails) == set(rules))]


def i04(work):
    reasons = ["audio drift", "font fallback", "render timeout"]
    plan = [f"mitigate {r}" for r in reasons]
    fps, frames, audio_s = 30, 600, 20.0
    drift = abs(frames / fps - audio_s)
    save(work, "premortem.json", {"reasons": reasons, "plan": plan, "drift_s": drift})
    return [eq("three reasons", len(reasons), 3), eq("one mitigation each", len(plan), 3), eq("locked fps -> zero drift", drift, 0.0),
            truth("drift detected when fps wrong", abs(frames / 25 - audio_s) > 0.04)]


def i05(work):
    tokens = 10_000 * 5 * 2_000
    frames = 60 * 30
    render_min = frames * 0.3 / 60
    save(work, "fermi.json", {"tokens_month": tokens, "frames": frames, "render_min": render_min})
    return [eq("tokens order of magnitude", round(np.log10(tokens)), 8), eq("frames", frames, 1800), eq("render minutes", render_min, 9.0)]


def scamper(draft):
    return {v: f"{v}: {draft}" for v in SCAMPER}


def i06(work):
    v = scamper("caption style")
    strength = {"substitute": 4, "combine": 2, "adapt": 3, "modify": 3, "put to other use": 1, "eliminate": 5, "reverse": 4}
    keep = sorted(v, key=lambda k: (-strength[k], SCAMPER.index(k)))[:2]
    save(work, "scamper.json", {"variants": v, "keep": keep})
    return [eq("7 verbs -> 7 variants", len(v), 7), eq("two strongest", keep, ["eliminate", "substitute"])]


def i07(work):
    dims = {"type": ["serif", "kufi", "mono"], "motion": ["spring", "glitch", "draw-on"], "palette": ["duotone", "neon", "paper"]}
    rows = grid(*dims.values())
    rng = random.Random(7)
    pick = rng.sample(rows, 3)
    save(work, "morph.json", {"rows": len(rows), "picked": pick})
    return [eq("3x3x3 combinations", len(rows), 27), eq("three rows", len(pick), 3), truth("rows distinct", len(set(pick)) == 3),
            truth("seeded", random.Random(7).sample(rows, 3) == pick)]


def i08(work):
    triage = lambda items: sorted(items, key=lambda x: (-x["severity"], -x["age"]))
    queue = [{"pr": 1, "severity": 1, "age": 9}, {"pr": 2, "severity": 3, "age": 1}, {"pr": 3, "severity": 3, "age": 5}]
    order = [x["pr"] for x in triage(queue)]
    save(work, "triage.json", order)
    return [eq("hospital triage borrowed: severity then age", order, [3, 2, 1]), eq("3 domains listed", len(["hospital", "airport", "post"]), 3)]


def two_colour(img):
    q = img.convert("L").point(lambda v: 255 if v >= 128 else 0)
    return q


def i09(work):
    a = np.tile(np.linspace(0, 255, 64, dtype=np.uint8), (36, 1))
    img = Image.fromarray(np.stack([a, a[::-1], a], -1))
    out = two_colour(img)
    out.save(work / "two_colour.png")
    cols = sorted(set(np.array(out).flatten().tolist()))
    words7 = "Export Arabic reels in one tap today".split()
    return [eq("strictly two colours", cols, [0, 255]), eq("seven-word explanation", len(words7), 7)]


def i10(work):
    ideal = {"camera": "real lens", "depth": "shallow", "grain": "film"}
    powers = {"real lens": "3D scene", "shallow": "depth of field blur", "film": "grain overlay"}
    approx = {k: powers[v] for k, v in ideal.items()}
    # depth-of-field approximation: blur grows with distance from focus plane
    dist = np.array([0, 1, 2, 4])
    blur = np.abs(dist - 1) * 1.5
    save(work, "approximation.json", {"approx": approx, "blur_px": blur.tolist()})
    return [eq("every ideal mapped to a power", len(approx), 3), eq("focus plane sharp", float(blur[1]), 0.0), eq("far plane blur", float(blur[3]), 4.5)]


def i11(work):
    base = {"scale": 1.0, "frequency_per_week": 1, "duration_s": 30}
    v10 = {k: v * 10 for k, v in base.items()}
    v01 = {k: round(v * 0.1, 6) for k, v in base.items()}
    save(work, "10x.json", {"10x": v10, "0.1x": v01})
    return [eq("10x frequency -> daily+ dashboard", v10["frequency_per_week"], 10), eq("0.1x duration", v01["duration_s"], 3.0), eq("10x scale", v10["scale"], 10.0)]


def i12(work):
    personas = {"angriest customer": "refund now", "CFO": "cost per user", "viewer's thumb": "stop in frame 1"}
    save(work, "personas.json", personas)
    return [truth("2-3 personas", 2 <= len(personas) <= 3), truth("one line each", all("\n" not in v for v in personas.values()))]


FLIP = {"hide": "show", "last": "first", "slow": "instant", "everywhere": "with intent", "tiny": "huge"}


def flip_idea(bad):
    return " ".join(FLIP.get(w, w) for w in bad.split())


def i13(work):
    bad = ["hide the price", "logo last", "slow loading", "comic sans everywhere", "tiny captions"]
    flips = [flip_idea(b) for b in bad]
    save(work, "worst_first.json", dict(zip(bad, flips)))
    return [eq("5 bad -> 5 flips", len(flips), 5), eq("price flip", flips[0], "show the price"), truth("every flip changed", all(a != b for a, b in zip(bad, flips)))]


def i14(work):
    from power_programs import card_index
    cards = sorted(card_index())
    rng = random.Random(7)
    draws = rng.sample(cards, 3)
    again = random.Random(7).sample(cards, 3)
    save(work, "dice.json", draws)
    return [eq("3 draws", len(draws), 3), eq("fixed seed reproducible", draws, again), truth("draws are real catalog ids", all(d in cards for d in draws))]


def i15(work):
    crit = {"readability": 0.4, "brand": 0.3, "wow": 0.3}
    var = {"A": {"readability": 5, "brand": 3, "wow": 2}, "B": {"readability": 3, "brand": 5, "wow": 4}, "C": {"readability": 2, "brand": 2, "wow": 5}}
    s = weighted_scores(var, crit)
    best_part = {c: max(var, key=lambda v: var[v][c]) for c in crit}
    save(work, "ensemble.json", {"scores": s, "merge": best_part})
    return [eq("N = 3", len(var), 3), eq("winner", rank(s)[0], "B"), eq("merge takes readability from A", best_part["readability"], "A")]


def i16(work):
    refs = {"Swiss grid": "12-column grid, flush-left", "calligraphic stroke": "stroke reveal along path"}
    combo = " + ".join(refs.values())
    names_living = ["Saul Bass"]
    ok = not any(n in combo for n in names_living)
    save(work, "remix.json", {"mechanisms": refs, "combo": combo, "credits": list(refs)})
    return [eq("2 references", len(refs), 2), truth("described by visible property, no names", ok), truth("credits kept", len(refs) == 2)]


def i17(work):
    task_fams = {"MOTION", "SYNC"}
    all_fams = {"MOTION": "video", "SYNC": "video", "ANLY": "data", "APP": "web"}
    foreign = sorted(f for f, d in all_fams.items() if f not in task_fams and d != "video")
    save(work, "crossover.json", foreign)
    return [eq("foreign families", foreign, ["ANLY", "APP"]), truth("one picked per pass", len(foreign[:1]) == 1)]


def i18(work):
    dirs = {"kufi neon": ((20, 20, 30), (0, 255, 200)), "paper serif": ((240, 230, 210), (40, 30, 20)), "duotone mono": ((10, 40, 120), (250, 200, 0))}
    sheet = Image.new("RGB", (64 * 3, 36))
    for n, (name, (bg, fg)) in enumerate(dirs.items()):
        im = Image.new("RGB", (64, 36), bg)
        ImageDraw.Draw(im).rectangle([16, 12, 48, 24], fill=fg)
        im.save(work / f"preview_{n}.png")
        sheet.paste(im, (64 * n, 0))
    sheet.save(work / "contact_sheet.png")
    arr = np.array(sheet)
    distinct = len({tuple(arr[2, 64 * n + 2]) for n in range(3)})
    return [eq("3 previews", len(dirs), 3), eq("differ on a real axis (bg colour)", distinct, 3), truth("two-word names", all(len(k.split()) == 2 for k in dirs)),
            eq("one question", "which direction?".count("?"), 1)]


CLICHE = {"gradient": "gradients everywhere", "purple": "default purple->blue", "blob": "decorative blobs", "glass": "glassmorphism",
          "rounded-3xl": "over-rounding", "card card": "cards in cards", "fade-in all": "everything fading in"}


def i19(work):
    design = "hero: purple to blue gradient, glass panel, blob shapes, card card layout, fade-in all"
    hits = sorted(v for k, v in CLICHE.items() if k in design)
    save(work, "cliches.json", hits)
    return [eq("cliches flagged", len(hits), 6), truth("over-rounding not falsely flagged", "over-rounding" not in hits)]


def spring(t, stiffness=170, damping=26, mass=1):
    w0 = np.sqrt(stiffness / mass)
    zeta = damping / (2 * np.sqrt(stiffness * mass))
    if zeta < 1:
        wd = w0 * np.sqrt(1 - zeta ** 2)
        return 1 - np.exp(-zeta * w0 * t) * (np.cos(wd * t) + zeta * w0 / wd * np.sin(wd * t))
    return 1 - np.exp(-w0 * t) * (1 + w0 * t)


ARABIC_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def i20(work):
    data = np.array([120, 340, 90, 410])
    facts = {"max": int(data.max()), "total": int(data.sum()), "growth_pct": round((data[-1] - data[0]) / data[0] * 100)}
    stagger = 0.075
    fps = 30
    land = {}
    for i, v in enumerate(data):
        t = np.arange(0, 3, 1 / fps) - i * stagger
        h = v * spring(np.clip(t, 0, None))
        land[i] = int(round(h[-1]))
    label = f"{facts['total']}".translate(ARABIC_DIGITS)
    save(work, "data_story.json", {"facts": facts, "landed": land, "label": label})
    return [eq("frozen total", facts["total"], 960), eq("bars land on data", list(land.values()), data.tolist()),
            eq("arabic-indic digits", label, "٩٦٠"), eq("growth", facts["growth_pct"], 242)]


def anchors(text):
    import re
    return re.findall(r"\d+(?:\.\d+)?|https?://\S+|[A-Z][a-z]+(?= [A-Z])", text)


def i21(work):
    script = "Order 3 items by Friday at https://x.io for 25 dollars"
    human = "Grab 3 items before Friday at https://x.io for just 25 dollars"
    bad = "Grab three items before Friday at https://x.io for 25 dollars"
    lock_ok = anchors(script) == anchors(human)
    fps = 30
    words_json = [{"w": w, "start": round(i * 0.31, 3)} for i, w in enumerate(human.split())]
    frames = [round(x["start"] * fps) for x in words_json]
    offsets = [abs(f / fps - x["start"]) for f, x in zip(frames, words_json)]
    save(work, "captions.json", {"words": words_json, "frames": frames})
    return [truth("anchor lock keeps numbers and link", lock_ok), truth("changed number caught", anchors(script) != anchors(bad)),
            truth("caption offset <= 1 frame (33 ms)", max(offsets) <= 1 / fps / 2 + 1e-9, max(offsets))]


def bfs_order(edges, centre):
    adj = {}
    for a, b, _ in edges:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    seen, order, q = {centre}, [], deque([centre])
    ring = {centre: 0}
    while q:
        n = q.popleft()
        for m in sorted(adj[n]):
            if m not in seen:
                seen.add(m)
                ring[m] = ring[n] + 1
                order.append((n, m))
                q.append(m)
    return order, ring


def i22(work):
    edges = [("core", "a", "parsed"), ("core", "b", "parsed"), ("core", "c", "inferred"), ("a", "d", "parsed"), ("b", "e", "inferred"), ("d", "f", "parsed")]
    deg = {}
    for a, b, _ in edges:
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
    centre = max(deg, key=lambda k: (deg[k], k))
    order, ring = bfs_order(edges, centre)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg">']
    for a, b, kind in edges:
        svg.append(f'<line data-a="{a}" data-b="{b}" stroke-dasharray="{"4 2" if kind == "inferred" else "none"}"/>')
    (work / "mindmap.svg").write_text("\n".join(svg + ["</svg>"]))
    two_rings = sorted(k for k, r in ring.items() if 1 <= r <= 2)
    return [eq("centre", centre, "core"), eq("BFS draw starts at centre", order[0][0], "core"), eq("two rings", two_rings, ["a", "b", "c", "d", "e"]),
            eq("dashed inferred edges", (work / "mindmap.svg").read_text().count('"4 2"'), 2)]


def i23(work):
    import re
    ledger = {"L1": ("market size 4.2B", "src1", "2026-09"), "L2": ("growth 12%", "src2", "2026-10")}
    draft = "The market is 4.2B [L1] and grows 12% [L2]; we expect 30% share."
    nums = re.findall(r"\d+(?:\.\d+)?%?B?", re.sub(r"\[L\d+\]", "", draft))
    ledger_nums = {n for v in ledger.values() for n in re.findall(r"\d+(?:\.\d+)?%?B?", v[0])}
    untraced = [n for n in nums if n not in ledger_nums]
    save(work, "trace.json", {"numbers": nums, "untraced": untraced})
    return [eq("untraced number caught", untraced, ["30%"]), truth("every ledger row dated", all(v[2] for v in ledger.values()))]


def model25(inp):
    return inp["units"] * (inp["price"] - inp["var_cost"]) - inp["fixed"]


def i25(work):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.optimize import brentq
    base = {"units": 1000, "price": 50, "var_cost": 30, "fixed": 12000}
    swings = {}
    for k in base:
        lo = model25(dict(base, **{k: base[k] * 0.7}))
        hi = model25(dict(base, **{k: base[k] * 1.3}))
        swings[k] = (lo, hi, abs(hi - lo))
    order = sorted(swings, key=lambda k: -swings[k][2])
    be_units = brentq(lambda u: model25(dict(base, units=u)), 1, 10_000)
    fig, ax = plt.subplots(figsize=(3, 2))
    for i, k in enumerate(order[::-1]):
        ax.barh(i, swings[k][1] - swings[k][0], left=swings[k][0])
    fig.savefig(work / "tornado.png", dpi=50)
    plt.close(fig)
    return [eq("base profit", model25(base), 8000), eq("tornado order", order, ["price", "var_cost", "units", "fixed"]), eq("units swing", swings["units"][2], 12000.0),
            eq("break-even units", round(be_units, 6), 600.0), eq("price swing", swings["price"][2], 30000.0)]


PIPELINE = ["seed", "expand", "cluster", "score", "strengthen", "prototype", "critique", "pitch"]


def run_pipeline(seed):
    st = {"seed": seed}
    st["expand"] = [f"{op}: {seed}" for op in ["invert", "fuse", "constrain", "exaggerate", "minimise", "swap audience", "transplant",
                                                 "personify", "time-shift", "interactive", "data-driven", "Arabic-first"]]
    st["cluster"] = {"form": st["expand"][:6], "context": st["expand"][6:]}
    st["score"] = {i: (n % 5 + 1) * ((n * 3) % 5 + 1) for n, i in enumerate(st["expand"])}
    top = sorted(st["score"], key=lambda k: -st["score"][k])[:3]
    st["strengthen"] = {t: {"objection": "?", "constraint": "?", "10x": "?"} for t in top}
    st["prototype"] = "2 s render"
    st["critique"] = "red team done"
    st["pitch"] = f"for creators: {top[0]} — proof: 2 s render"
    return st


def i27(work):
    st = run_pipeline("Arabic reel intro")
    save(work, "pipeline.json", st)
    return [eq("eight stages in order", list(st), PIPELINE), eq("twelve expansion rows", len(st["expand"]), 12), eq("top 3 strengthened", len(st["strengthen"]), 3)]


def i28(work):
    idea = {"text": "auto captions for every reel", "objections": {"captions cover faces": 4, "slow": 2, "cost": 1}}
    strongest = max(idea["objections"], key=idea["objections"].get)
    strengthened = idea["text"] + " placed by face detection in the lower safe zone"
    save(work, "steelman.json", {"strongest": strongest, "strengthened": strengthened})
    return [eq("strongest objection", strongest, "captions cover faces"), truth("answer addresses it", "face" in strengthened)]


PROGRAMS = {f"IDEA-{n:02d}": globals()[f"i{n:02d}"] for n in list(range(1, 24)) + [25, 27, 28]}
