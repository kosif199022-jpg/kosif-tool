"""Launch videos ("brag"), readability and the sound-effect kit — the /brag method (MIT, latent-spaces/brag) on the
KOSIF engine, Arabic-first. Claude writes the angle, the storyboard and the share copy; this script gathers the
material, keeps the rules and checks the result.

    python scripts/kmotion.py brag init [DIR|URL] [--tone T] [--format landscape|vertical|square] [--duration 20] [--out D]
        material (title, description, headings, calls to action, colours, fonts, images) + brag-plan.md to fill in
    python scripts/kmotion.py brag deliver OUT_DIR --film FILM.mp4 [--at T]
        poster (strongest settled frame) baked as frame 0, the gate, share-copy.txt checked → OUT_DIR/brag.mp4, brag.jpg
    python scripts/kmotion.py readable reel.json|verse.json|edit.json [--wpm-s 0.3] [--entry 0.4]
        every line a viewer must read stays settled long enough (≈ 0.3 s a word, ≥ 0.8 s), and the hook lands in 2 s
    python scripts/kmotion.py sfx                     the CC0 effects in scripts/kit/sfx with what each is for
"""
from __future__ import annotations

import argparse
import html as _html
import json
import re
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SFX = HERE / "kit" / "sfx"

TONES = {   # pacing, transitions, sound energy (from /brag's tone system)
    "default":   ("punchy, playful, clean", "4–5 scenes; soft transitions", "3–5 cues: drop/click pop-ins, reveal on the reveal, bell on success"),
    "polished":  ("serious, elegant, restrained", "3–4 scenes, long holds; soft fades", "2–3 subtle cues: bong, drop-1; nothing aggressive"),
    "yc-parody": ("deadpan startup launch, played straight", "4–5 scenes, one claim each; hard cuts", "2–3 dry cues: one reveal, one card, one payoff"),
    "chaotic":   ("FAST, LOUD, ALL CAPS", "6–8 scenes, some under 2 s; flash/zoom cuts", "dense: a cue on every beat, glitch accents"),
    "deadpan":   ("calm, dry, nothing is a joke", "3–4 scenes, big empty space; slow fades", "one quiet bed + 1–2 dry cues"),
    "cinematic": ("trailer-scale, epic claims", "4–5 scenes, big type; dramatic wipes", "2–3 big ones: bell-1 on the hero, reveal on the reveal, bell-2 out"),
    "app-store": ("clean feature cards", "4–6 scenes; smooth slides", "a light layer: drop/click per card, bell-1 on the outro"),
}
SIZES = {"landscape": (1920, 1080), "vertical": (1080, 1920), "square": (1080, 1080)}
BANNED = ["excited to share", "streamline your workflow", "game changer", "game-changer", "revolutionize", "يسعدنا أن نعلن", "يسعدني أن أشارك",
          "ثورة في عالم", "حل متكامل لجميع"]
RUBRIC = [
    ("What is it, in one sentence?", "ما هو، في جملة واحدة؟"),
    ("Who is it for, and what does it do for them?", "لمن هو، وماذا يفعل لهم؟"),
    ("What sets it apart?", "ما الذي يميّزه؟"),
    ("The most impressive or funniest claim (its own words)?", "أقوى أو أطرف ادعاء (بكلماته هو)؟"),
    ("The visual hook (first 2 s)?", "الخطّاف البصري (أول ثانيتين)؟"),
    ("Which real UI / flow is shown (entry → key action → result)?", "أي واجهة أو تدفّق حقيقي يظهر (دخول ← فعل أساسي ← نتيجة)؟"),
    ("Which tone fits, and why?", "أي نبرة تناسب، ولماذا؟"),
    ("The one-line share caption?", "سطر المشاركة الواحد؟"),
    ("How does a stranger get it (link / name)?", "كيف يصل إليه شخص لا يعرفه (رابط / اسم)؟"),
]


# ───────────────────────── material ─────────────────────────
def _text(s: str) -> str:
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


_COLOR = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|(?:rgba?|hsla?|oklch)\([^)]*\)", re.I)


def to_hex(c: str) -> str | None:
    """#rgb / #rrggbb / rgb() / hsl() / oklch() → #rrggbb (alpha dropped); None when unreadable."""
    c = c.strip().lower()
    try:
        if c.startswith("#"):
            h = c[1:]
            return "#" + ("".join(ch * 2 for ch in h) if len(h) == 3 else h[:6])
        name, args = c.split("(", 1)
        nums = [x for x in re.split(r"[\s,/]+", args.rstrip(")")) if x]
        pct = lambda x, scale: float(x[:-1]) / 100 * scale if x.endswith("%") else float(x)  # noqa: E731
        if name.startswith("rgb"):
            r, g, b = (pct(x, 255) for x in nums[:3])
        elif name.startswith("hsl"):
            import colorsys
            hh = float(nums[0].replace("deg", "")) / 360
            r, g, b = (v * 255 for v in colorsys.hls_to_rgb(hh, pct(nums[2], 1), pct(nums[1], 1)))
        else:                                                   # oklch(L C h) → OKLab → linear sRGB → sRGB
            import math
            L, C, H = pct(nums[0], 1), float(nums[1]), math.radians(float(nums[2].replace("deg", "")))
            a, b_ = C * math.cos(H), C * math.sin(H)
            l_, m_, s_ = ((L + 0.3963377774 * a + 0.2158037573 * b_) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b_) ** 3,
                          (L - 0.0894841775 * a - 1.2914855480 * b_) ** 3)
            lin = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_, -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
                   -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
            enc = lambda x: 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055  # noqa: E731
            r, g, b = (enc(min(1.0, max(0.0, x))) * 255 for x in lin)
        return "#%02x%02x%02x" % tuple(int(round(min(255, max(0, v)))) for v in (r, g, b))
    except (ValueError, IndexError):
        return None


def from_html(page: str, css: str = "") -> dict:
    meta = lambda k: (re.search(rf'<meta[^>]+(?:name|property)=["\']{k}["\'][^>]+content=["\']([^"\']*)', page, re.I) or [None, ""])[1]  # noqa: E731
    title = _text((re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I) or [None, ""])[1]) or meta("og:title")
    heads = [_text(h) for h in re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", page, re.S | re.I)]
    ctas = [_text(b) for b in re.findall(r"<(?:button|a)[^>]*(?:btn|button|cta)[^>]*>(.*?)</(?:button|a)>", page, re.S | re.I)]
    allcss = css + " ".join(re.findall(r"<style[^>]*>(.*?)</style>", page, re.S | re.I)) + " ".join(re.findall(r'style="([^"]*)"', page))
    cvars = dict(re.findall(r"--([\w-]+)\s*:\s*([^;}{]+)", allcss))
    named = {k: to_hex(v.strip()) for k, v in cvars.items() if _COLOR.fullmatch(v.strip())}
    colors = Counter(x for x in (to_hex(c) for c in _COLOR.findall(allcss)) if x)

    def family(v: str) -> str:
        v = v.strip()
        m = re.match(r"var\(--([\w-]+)", v)
        if m and m.group(1) in cvars:
            v = cvars[m.group(1)]
        return v.split(",")[0].strip().strip("'\"")
    fonts = Counter(f for f in (family(ff) for ff in re.findall(r"font-family\s*:\s*([^;}{]+)", allcss)) if f and not f.startswith("var("))
    fonts.update(family(v) for k, v in cvars.items() if re.search(r"font|serif|sans|mono|display|heading|body", k) and not _COLOR.fullmatch(v.strip()))
    gfonts = [g.replace("+", " ") for g in re.findall(r"fonts\.googleapis\.com/css2?\?family=([\w+]+)", page)]
    images = [m for m in re.findall(r'<img[^>]+src=["\']([^"\']+)', page, re.I)][:12] + [meta("og:image")]
    return {"title": title, "description": meta("description") or meta("og:description"), "headings": [h for h in heads if h][:14],
            "ctas": list(dict.fromkeys(c for c in ctas if c))[:8], "colors": [c for c, _ in colors.most_common(8)], "palette": {k: v for k, v in named.items() if v},
            "fonts": list(dict.fromkeys(gfonts + [f for f, _ in fonts.most_common(4) if f])), "images": [i for i in images if i],
            "lang": (re.search(r'<html[^>]+lang=["\']([\w-]+)', page, re.I) or [None, ""])[1]}


def from_dir(d: Path) -> dict:
    page = next((p for p in (d / "index.html", d / "public" / "index.html", d / "dist" / "index.html", d / "docs" / "index.html") if p.exists()), None)
    css = " ".join(p.read_text(encoding="utf-8", errors="replace")[:200_000] for p in list(d.glob("*.css")) + list(d.glob("src/**/*.css"))[:20])
    m = from_html(page.read_text(encoding="utf-8", errors="replace"), css) if page else {"title": "", "description": "", "headings": [], "ctas": [], "colors": [], "fonts": [], "images": [], "lang": ""}
    readme = next((p for p in d.glob("README*") if p.is_file()), None)
    if readme:
        txt = readme.read_text(encoding="utf-8", errors="replace")
        m["title"] = m["title"] or (re.search(r"^#\s+(.+)$", txt, re.M) or [None, d.name])[1].strip()
        para = next((p.strip() for p in re.split(r"\n\s*\n", txt) if p.strip() and not p.lstrip().startswith(("#", "!", "[", "<", "```", "|"))), "")
        m["readme"] = para[:600]
    pkg = d / "package.json"
    if pkg.exists():
        try:
            pj = json.loads(pkg.read_text(encoding="utf-8")); m["title"] = m["title"] or pj.get("name", ""); m["description"] = m["description"] or pj.get("description", "")
        except ValueError:
            pass
    m["source"] = str(d.resolve()); m["page"] = str(page) if page else None
    return m


def from_url(url: str) -> dict:
    if not re.match(r"^https?://", url):
        url = "https://" + url
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (KOSIF brag; +local)"})
    page = urllib.request.urlopen(req, timeout=25).read(3_000_000).decode("utf-8", "replace")
    m = from_html(page); m["source"] = url
    if len(_text(page)) < 300:
        m["note"] = "the page is built by JavaScript: render it in a headless browser (kmotion frames / Playwright) for its real copy"
    return m


def plan_md(m: dict, tone: str, fmt: str, seconds: float) -> str:
    W, H = SIZES[fmt]
    t = TONES.get(tone, TONES["default"])
    L = [f"# brag-plan — {m.get('title') or 'project'}", "", f"Source: {m.get('source')}  ·  {W}×{H}, 30 fps  ·  ≈ {seconds:g} s  ·  tone: **{tone}** ({t[0]})", "",
         "## Material (from the source — use its own words, never invent claims, numbers or testimonials)", ""]
    for k in ("title", "description", "readme"):
        if m.get(k):
            L.append(f"- **{k}**: {m[k]}")
    if m.get("palette"):
        L.append("- **palette**: " + " · ".join(f"{k} {v}" for k, v in m["palette"].items()))
    for k in ("headings", "ctas", "colors", "fonts", "images"):
        if m.get(k):
            L.append(f"- **{k}**: " + " · ".join(map(str, m[k])))
    if m.get("note"):
        L.append(f"- ⚠ {m['note']}")
    L += ["", "## Rubric (answer every line before the storyboard)", ""]
    L += [f"{i}. {en} / {ar}\n   → " for i, (en, ar) in enumerate(RUBRIC, 1)]
    L += ["", "## Shape", "", "Hook (2–3 s) → Reveal (2–4 s) → 2–3 sharp highlights → Punchline / outro (2–4 s). A starting shape, not a template.",
          f"Tone pacing: {t[1]}. Sound: {t[2]} (`kmotion sfx`).", "",
          "## Storyboard (durations must sum to the target)", "",
          "| # | Beat | Start–end (s) | On screen (real UI / copy) | Text a viewer must read | Motion | Transition | SFX (kit:NAME at s) |",
          "|---|---|---|---|---|---|---|---|", "| 1 | Hook |  |  |  |  |  |  |", "| 2 | Reveal |  |  |  |  |  |  |",
          "| 3 | Highlight |  |  |  |  |  |  |", "| 4 | Highlight |  |  |  |  |  |  |", "| 5 | Punchline / outro |  |  |  |  |  |  |", "",
          "## Laws", "",
          "- **Short**: 15–25 s (18–22 the sweet spot). **Hook first**: plan the first 2 s before anything else.",
          "- **Show the thing**: the product's real UI, copy, colours, fonts and images — reused, not re-drawn. No abstract filler.",
          "- **Specific**: made for this exact project; no generic SaaS language.",
          "- **Readable**: fast in, then hold — a line stays settled ≈ 0.3 s a word (≥ 0.8 s); check with `kmotion readable`.",
          "- **Alive**: things appear one by one, simulated taps, swipes, typing — not static slides. **Every frame postable.**",
          "- **Arabic**: RTL lines, no letter-spacing on Arabic, Cairo/the product's own Arabic font; numbers stay LTR.",
          "- **Sound**: music and effects as one piece — effects soft under the bed, the same space; fewer cues, better timed (cue at the START of the motion).",
          "- **Transitions**: never a muddy crossfade of two busy layouts — stagger (old out, then new in) or dip through the background.",
          "", "## Deliver", "", "`kmotion brag deliver OUT --film film.mp4` → brag.mp4 (poster baked as frame 0), brag.jpg, share-copy.txt (1–3 sentences, specific, tone-matched)."]
    return "\n".join(L) + "\n"


def init(source: str | None, tone: str, fmt: str, seconds: float, out: Path | None) -> dict:
    src = source or "."
    m = from_url(src) if re.match(r"^(https?://|[\w-]+\.[a-z]{2,}(/|$))", src) and not Path(src).exists() else from_dir(Path(src))
    base = Path(out) if out else Path("brag-output")
    if base.exists() and any(base.iterdir()) and not out:
        base = Path(time.strftime("brag-output-%Y-%m-%d-%H%M%S"))
    (base / "work").mkdir(parents=True, exist_ok=True)
    (base / "material.json").write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    (base / "brag-plan.md").write_text(plan_md(m, tone, fmt, seconds), encoding="utf-8")
    return {"out": str(base), "title": m.get("title"), "colors": m.get("colors"), "fonts": m.get("fonts"), "headings": len(m.get("headings", [])),
            "next": "answer the rubric and fill the storyboard in brag-plan.md, build the composition (kmotion new / template / timeline), render, then `kmotion brag deliver`"}


# ───────────────────────── share copy + deliver ─────────────────────────
def check_copy(text: str) -> list[str]:
    issues = []
    sents = [s for s in re.split(r"(?<=[.!?؟。])\s+|\n+", text.strip()) if s.strip()]
    if not text.strip():
        issues.append("share-copy.txt is empty")
    if len(sents) > 3:
        issues.append(f"{len(sents)} sentences: keep it to 1–3")
    low = text.lower()
    issues += [f"banned phrase: {b!r}" for b in BANNED if b.lower() in low]
    if len(text) > 280:
        issues.append(f"{len(text)} characters: over a post's 280")
    return issues


def deliver(out: Path, film: Path, at: float | None) -> dict:
    import poster
    import qa
    out.mkdir(parents=True, exist_ok=True)
    dst = out / "brag.mp4"
    if film.resolve() != dst.resolve():
        import shutil
        shutil.copy2(film, dst)
    t = at if at is not None else poster.pick(dst)["t"]
    jpg = poster.extract(dst, t, out / "brag.jpg")
    baked = poster.bake(dst, jpg, dst)
    gate = qa.inspect(dst)
    sc = out / "share-copy.txt"
    copy_issues = check_copy(sc.read_text(encoding="utf-8")) if sc.exists() else ["share-copy.txt missing: write 1–3 postable sentences"]
    return {"film": str(dst), "poster": str(jpg), "poster_t": t, "baked": baked, "gate_ok": gate.get("ok"), "gate_issues": gate.get("issues"),
            "lufs": gate.get("lufs"), "share_copy_issues": copy_issues}


# ───────────────────────── readability ─────────────────────────
def _items(path: Path) -> list[dict]:
    d = json.loads(path.read_text(encoding="utf-8"))
    out = []
    if isinstance(d, dict) and "scenes" in d:                                        # reel.json
        for s in d["scenes"]:
            for e in s.get("els", []):
                for k, p in (e.get("props") or {}).items():
                    if p.get("type") in ("text", "longtext") and str(p.get("v", "")).strip():
                        out.append({"what": f"{s['id']}/{e['id']}.{k}", "text": str(p["v"]), "t0": float(e["t"][0]), "t1": float(e["t"][1])})
    elif isinstance(d, dict) and "lines" in d:                                       # verse.json
        for i, ln in enumerate(d["lines"]):
            ws = ln.get("words") or []
            if ws:
                out.append({"what": f"line {i + 1}", "text": " ".join(w["text"] for w in ws), "t0": float(ws[-1]["t"]), "t1": float(ln["end"]), "settled_from_last_word": True})
    elif isinstance(d, dict) and "overlays" in d:                                    # timeline spec
        for i, o in enumerate(d["overlays"]):
            if o.get("type", "text") in ("text", "lower-third"):
                txt = o.get("text") or " ".join(x for x in (o.get("title"), o.get("sub")) if x)
                out.append({"what": f"overlay {i}", "text": str(txt), "t0": float(o.get("start", 0)), "t1": float(o.get("end", float(o.get("start", 0)) + 3))})
    return out


def readable(path: Path, per_word: float = 0.3, entry: float = 0.4, floor: float = 0.8) -> dict:
    items, rows = _items(path), []
    for it in items:
        n = len(it["text"].split())
        need = max(floor, per_word * n)
        settled = it["t1"] - it["t0"] - (0.0 if it.get("settled_from_last_word") else entry)
        rows.append({**{k: it[k] for k in ("what", "text")}, "words": n, "settled_s": round(settled, 2), "need_s": round(need, 2), "ok": settled + 1e-6 >= need})
    first = min((it["t0"] for it in items), default=None)
    return {"file": str(path), "items": len(rows), "too_short": [r for r in rows if not r["ok"]], "all": rows,
            "hook": {"first_text_at": first, "ok": first is not None and first <= 2.0},
            "rule": f"settled ≥ max({floor}s, {per_word}s × words), counted after a {entry}s entry"}


def sfx_list() -> dict:
    cat = json.loads((SFX / "catalog.json").read_text(encoding="utf-8"))
    return {"dir": str(SFX), "use_in_timeline": '"audio": {"sfx": [{"src": "kit:NAME", "at": SECONDS, "gain": -10}]}', "credit": cat["credit"],
            "sounds": {k: f"{v['use']} — {v['duration']}s, {v['brightness']}, HF risk {v['hf_risk']}" for k, v in cat["sounds"].items()}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("source", nargs="?"); p.add_argument("--tone", default="default")
    p.add_argument("--format", default="landscape", choices=list(SIZES)); p.add_argument("--duration", type=float, default=20); p.add_argument("--out")
    p = sub.add_parser("deliver"); p.add_argument("out"); p.add_argument("--film", required=True); p.add_argument("--at", type=float)
    p = sub.add_parser("readable"); p.add_argument("file"); p.add_argument("--wpm-s", type=float, default=0.3); p.add_argument("--entry", type=float, default=0.4)
    sub.add_parser("sfx")
    a = ap.parse_args()
    if a.cmd == "init":
        res = init(a.source, a.tone, a.format, a.duration, Path(a.out) if a.out else None)
    elif a.cmd == "deliver":
        res = deliver(Path(a.out), Path(a.film), a.at)
    elif a.cmd == "readable":
        res = readable(Path(a.file), a.wpm_s, a.entry); res.pop("all")
    else:
        res = sfx_list()
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
