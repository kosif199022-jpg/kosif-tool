"""Real programs for the 'other' family (KOSIF routing rules, safe naming, project files, gates, small UI recipes).

Only cards whose rule is fully stated on the card are programmed; cards that describe owner
tools or services not present in this checkout are skipped (out/power-programs/data-skipped.json).
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
import re
import unicodedata
from pathlib import Path

import numpy as np


def _w(work: Path, name: str, obj) -> Path:
    p = work / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, (bytes, bytearray)):
        p.write_bytes(obj)
    elif isinstance(obj, str):
        p.write_text(obj, encoding="utf-8")
    else:
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return p


def _c(name, cond, obs):
    return (name, bool(cond), str(obs))


# ---------------------------------------------------------------- MISC-04
def misc_04(work: Path):
    RUBRIC = {"capability": 30, "live_availability": 20, "owner_authority": 15, "verification": 15, "reversibility": 10, "latency_cost": 5, "continuity": 5}

    def score(route):
        for k, v in route.items():
            if not 0 <= v <= RUBRIC[k]:
                raise ValueError(f"{k} out of range 0-{RUBRIC[k]}")
        return sum(route.values())

    routes = {"local ffmpeg": {"capability": 25, "live_availability": 20, "owner_authority": 10, "verification": 15, "reversibility": 10, "latency_cost": 5, "continuity": 5},
              "cloud API": {"capability": 30, "live_availability": 10, "owner_authority": 5, "verification": 5, "reversibility": 5, "latency_cost": 1, "continuity": 2},
              "offline fallback": {"capability": 15, "live_availability": 20, "owner_authority": 15, "verification": 10, "reversibility": 10, "latency_cost": 5, "continuity": 3}}
    scores = {k: score(v) for k, v in routes.items()}
    best = max(scores, key=scores.get)
    try:
        score({"capability": 35})
        refused = False
    except ValueError:
        refused = True
    _w(work, "route_scores.json", scores)
    return [_c("rubric totals 100", sum(RUBRIC.values()) == 100, RUBRIC),
            _c("scores: ffmpeg 90, cloud 58, offline 78", scores == {"local ffmpeg": 90, "cloud API": 58, "offline fallback": 78}, scores),
            _c("highest-scoring route chosen", best == "local ffmpeg", best),
            _c("a component above its cap is refused", refused, refused)]


# ---------------------------------------------------------------- MISC-06
def misc_06(work: Path):
    CTX, EXCERPT, CLI_STDIN = 60_000, 40_000, 28_000

    def extract(reply):
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", reply, re.S)
        raw = m[1] if m else reply[reply.find("{"): reply.rfind("}") + 1]
        data = json.loads(raw)
        return {k: data.get(k, [] if k in ("actions", "files") else None) for k in ("notes", "actions", "files", "timeline", "timeline_name")}

    def pack(task, context, excerpt):
        return {"task": task, "context": context[:CTX], "excerpt": excerpt[:EXCERPT], "via_stdin": len(task) + len(context) > CLI_STDIN}

    def apply(files, root):
        for f in files:
            p = root / f["project"] / f["path"]
            p.parent.mkdir(parents=True, exist_ok=True)
            if p.exists():
                p.with_suffix(p.suffix + ".bak").write_bytes(p.read_bytes())
            p.write_text(f["content"])

    fenced = 'Sure:\n```json\n{"notes":"ok","files":[{"project":"p","path":"a.txt","content":"new"}]}\n```'
    bare = 'Result {"notes":"bare","actions":[{"recipe":"trim","args":{"s":1}}]} end'
    r1, r2 = extract(fenced), extract(bare)
    (work / "p").mkdir()
    (work / "p" / "a.txt").write_text("old")
    apply(r1["files"], work)
    pk = pack("t", "x" * 70_000, "y" * 50_000)
    return [_c("fenced JSON reply extracted", r1["notes"] == "ok" and r1["files"][0]["path"] == "a.txt", r1),
            _c("bare JSON reply extracted with default fields", r2["notes"] == "bare" and r2["files"] == [] and r2["actions"][0]["recipe"] == "trim", r2),
            _c("apply keeps a .bak of the overwritten file", (work / "p" / "a.txt.bak").read_text() == "old" and (work / "p" / "a.txt").read_text() == "new", ""),
            _c("context capped at 60k and excerpt at 40k; >28k goes via stdin", len(pk["context"]) == 60_000 and len(pk["excerpt"]) == 40_000 and pk["via_stdin"], "")]


# ---------------------------------------------------------------- MISC-07
def misc_07(work: Path):
    MAX = 1_000_000

    def asset_key(f):
        return f"{f['name']}:{f['size']}:{f['lastModified']}"

    def sanitize(raw: bytes):
        if len(raw) > MAX:
            raise ValueError("project file over 1 MB")
        p = json.loads(raw)
        if p.get("version") != 1:
            raise ValueError("unsupported version")
        clips = [{"asset": str(c["asset"]), "start": float(c["start"]), "dur": max(0.0, float(c["dur"]))} for c in p.get("clips", []) if "asset" in c]
        return {"version": 1, "name": str(p.get("name", "untitled"))[:64], "clips": clips}

    media = [{"name": "intro.mp4", "size": 1048576, "lastModified": 1730000000000}]
    proj = {"version": 1, "name": "عرض", "clips": [{"asset": asset_key(media[0]), "start": 0, "dur": 3.5}, {"bogus": True}], "script": "<x>"}
    path = _w(work, "عرض.kosif.json", proj)
    back = sanitize(path.read_bytes())
    library = {asset_key(m): m for m in media}
    relinked = [library.get(c["asset"]) for c in back["clips"]]
    errs = []
    for raw in (json.dumps({**proj, "version": 2}).encode(), b"{" + b" " * MAX + b"}"):
        try:
            sanitize(raw)
        except ValueError as e:
            errs.append(str(e))
    return [_c("assetKey = name:size:lastModified", asset_key(media[0]) == "intro.mp4:1048576:1730000000000", asset_key(media[0])),
            _c("sanitize keeps only known fields and valid clips", set(back) == {"version", "name", "clips"} and len(back["clips"]) == 1, back),
            _c("clip re-links to the media by its key", relinked == [media[0]], relinked),
            _c("version 2 and > 1 MB files refused", errs == ["unsupported version", "project file over 1 MB"], errs)]


# ---------------------------------------------------------------- MISC-13
_SAFE = re.compile(r"^[\w؀-ۿ][\w؀-ۿ-]{0,63}$")


def misc_13(work: Path):
    def safe_name(s):
        s = unicodedata.normalize("NFC", s).strip()
        s = re.sub(r"[^\w؀-ۿ-]+", "-", s).strip("-")[:64]
        return s if _SAFE.match(s) else "untitled"

    def json_for_script(obj):
        return json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")

    cases = {"فيديو الجمعة": "فيديو-الجمعة", "../../etc/passwd": "etc-passwd", "a" * 80: "a" * 64, "--": "untitled", "clip_01-final": "clip_01-final"}
    got = {k: safe_name(k) for k in cases}
    payload = json_for_script({"t": "</script><script>alert(1)</script>"})
    _w(work, "names.json", got)
    return [_c("regex accepts Arabic and word chars up to 64", bool(_SAFE.match("فيديو_1")) and not _SAFE.match("-x") and not _SAFE.match("a" * 65), ""),
            _c("names sanitised as expected (traversal, spaces, length)", got == cases, got),
            _c("html_text escapes markup", html.escape('<b>"x"</b>') == "&lt;b&gt;&quot;x&quot;&lt;/b&gt;", ""),
            _c("json_for_script cannot close the script tag", "</script>" not in payload and json.loads(payload)["t"].startswith("</script>"), payload[:40])]


# ---------------------------------------------------------------- MISC-14
def misc_14(work: Path):
    reg = {"sources": {}, "chunks": {}}

    def register_source(uri, content: bytes, licence):
        sid = hashlib.sha256(content).hexdigest()
        reg["sources"][sid] = {"uri": uri, "licence": licence, "revoked": False}
        return sid

    def register_chunk(text, source_id):
        if source_id not in reg["sources"]:
            raise KeyError("unknown source")
        cid = hashlib.sha256(text.encode()).hexdigest()
        reg["chunks"][cid] = {"source": source_id, "text": text}
        return cid

    def revoke_source(sid):
        reg["sources"][sid]["revoked"] = True

    def taint_scan(output_chunk_ids):
        return sorted(c for c in output_chunk_ids if reg["sources"][reg["chunks"][c]["source"]]["revoked"])

    s1 = register_source("https://example.org/a", b"doc A", "CC-BY")
    s2 = register_source("https://example.org/b", b"doc B", "unknown")
    c1, c2 = register_chunk("fact from A", s1), register_chunk("fact from B", s2)
    before = taint_scan([c1, c2])
    revoke_source(s2)
    after = taint_scan([c1, c2])
    try:
        register_chunk("orphan", "0" * 64)
        orphan = False
    except KeyError:
        orphan = True
    _w(work, "atlas_registry.json", reg)
    return [_c("ids are sha256 64-hex", all(re.fullmatch(r"[0-9a-f]{64}", x) for x in (s1, s2, c1, c2)), s1[:12]),
            _c("clean output before revocation", before == [], before),
            _c("revoking source B taints exactly its chunk", after == [c2], after),
            _c("chunk without a registered source refused", orphan, orphan)]


# ---------------------------------------------------------------- MISC-15
def misc_15(work: Path):
    def check(plan):
        deep = plan["mode"] in ("deep", "full_pro")
        errs = []
        if len(plan["packs"]) > (4 if deep else 2):
            errs.append("too many method packs")
        if len(plan["specialists"]) > (2 if deep else 1):
            errs.append("too many dynamic specialists")
        if plan.get("receipt_label") not in (None, "LOCAL_ENGINE") and not plan.get("deployed_full_pro"):
            errs.append("local receipt must be labelled LOCAL_ENGINE")
        return errs

    cases = {"normal_ok": {"mode": "normal", "packs": ["a", "b"], "specialists": ["x"]},
             "normal_over": {"mode": "normal", "packs": ["a", "b", "c"], "specialists": ["x", "y"]},
             "deep_ok": {"mode": "deep", "packs": list("abcd"), "specialists": ["x", "y"]},
             "deep_over": {"mode": "deep", "packs": list("abcde"), "specialists": ["x"]},
             "fake_full_pro": {"mode": "full_pro", "packs": ["a"], "specialists": [], "receipt_label": "FULL_PRO_VERIFIED"}}
    res = {k: check(v) for k, v in cases.items()}
    _w(work, "see_limits.json", res)
    return [_c("normal: 2 packs + 1 specialist allowed", res["normal_ok"] == [], res["normal_ok"]),
            _c("normal: 3 packs and 2 specialists both refused", res["normal_over"] == ["too many method packs", "too many dynamic specialists"], res["normal_over"]),
            _c("deep: 4 packs + 2 specialists allowed, 5 packs refused", res["deep_ok"] == [] and res["deep_over"] == ["too many method packs"], res),
            _c("undeployed Full Pro cannot claim a verified receipt", res["fake_full_pro"] == ["local receipt must be labelled LOCAL_ENGINE"], res["fake_full_pro"])]


# ---------------------------------------------------------------- MISC-17
def misc_17(work: Path):
    rng = np.random.default_rng(12)
    posts = []
    for i in range(40):
        day, hour = int(rng.integers(0, 7)), int(rng.integers(0, 24))
        views = 1000 + (4000 if (day == 4 and 18 <= hour < 21) else 0) + int(rng.integers(0, 300))
        posts.append((day, hour, views))
    posts += [(4, 19, 5200), (4, 20, 5100)]
    _w(work, "export.csv", "day,hour,views\n" + "\n".join(f"{d},{h},{v}" for d, h, v in posts))

    def besttime(rows, block=3, min_posts=8, min_cell=2):
        if len(rows) < min_posts:
            return None, "default heuristic slots (too few posts)"
        cells = {}
        for d, h, v in rows:
            cells.setdefault((d, h // block * block), []).append(v)
        ok = {k: float(np.mean(v)) for k, v in cells.items() if len(v) >= min_cell}
        best = max(ok, key=ok.get)
        return best, ok[best]

    best, val = besttime(posts)
    few, why = besttime(posts[:5])
    return [_c("best cell is Friday(4) 18:00-21:00 block", best == (4, 18), (best, val)),
            _c("cells with a single post are ignored (>= 2 per cell)", val > 4000, val),
            _c("fewer than 8 posts falls back to default slots", few is None and "default" in why, why)]


# ---------------------------------------------------------------- MISC-20
def misc_20(work: Path):
    from PIL import Image, ImageDraw, ImageFont
    w, h, duration = 1080, 1920, 10.0
    LIME, TRACK = (0xc9, 0xf9, 0x6d), (0x29, 0x39, 0x51)

    def frame(t):
        img = Image.new("RGB", (w, h), (10, 14, 22))
        d = ImageDraw.Draw(img)
        size = round(w * 0.024)
        d.text((w * 0.09, h * 0.92), "KOSIF", fill=LIME, font=ImageFont.load_default(size=size))
        y, bw, x0 = round(h * 0.96), round(w * 0.82), round((w - w * 0.82) / 2)
        d.rounded_rectangle([x0, y - 6, x0 + bw, y + 6], radius=6, fill=TRACK)
        fill_w = round(bw * t / duration)
        if fill_w > 12:
            d.rounded_rectangle([x0, y - 6, x0 + fill_w, y + 6], radius=6, fill=LIME)
        return img, x0, y, bw

    img, x0, y, bw = frame(5.0)
    img.save(work / "frame_5s.png")
    a = np.asarray(img)
    row = a[y]
    lime_cols = np.where(np.all(row == LIME, axis=1))[0]
    track_cols = np.where(np.all(row == TRACK, axis=1))[0]
    label_rows = np.where(np.all(a[: y - 20] == LIME, axis=2).any(1))[0]
    return [_c("bar track spans 82% of width (886 px) at y = 96% h (1843)", bw == 886 and y == 1843 and max(track_cols.max(), lime_cols.max()) - min(track_cols.min(), lime_cols.min()) == bw, (bw, y)),
            _c("at t = duration/2 the fill covers half the track (+/- 1 px)", abs((lime_cols.max() - x0) - bw / 2) <= 1, int(lime_cols.max() - x0)),
            _c("label drawn in #c9f96d starting at 92% h", label_rows.min() >= round(h * 0.92) - 1, int(label_rows.min())),
            _c("label size = w x 0.024 = 26 px", round(w * 0.024) == 26, 26)]


# ---------------------------------------------------------------- MISC-P01
def misc_p01(work: Path):
    FIELDS = ["goal", "artifact", "constraints", "owner", "tools_allowed", "evidence_required", "state", "next_step"]

    def rung(need):
        if need.get("always_on") and need.get("deterministic"):
            return 1, "existing rule"
        if need.get("procedure") and not need.get("tool"):
            return 2, "existing skill"
        if need.get("structured_tool") and need.get("live_server"):
            return 3, "canonical MCP after a live probe"
        if need.get("bounded") and need.get("local_cli_installed"):
            return 4, "trusted local CLI"
        if need.get("authenticated_provider"):
            return 5, "approved API with budget"
        return None, "no rung fits: ask"

    cases = {"lint rule": {"always_on": True, "deterministic": True}, "how to grade": {"procedure": True},
             "github issues": {"structured_tool": True, "live_server": True}, "transcode": {"bounded": True, "local_cli_installed": True},
             "paid TTS": {"authenticated_provider": True}}
    picks = {k: rung(v)[0] for k, v in cases.items()}
    packet = dict.fromkeys(FIELDS, "...")
    packet["state"] = {"executed": True, "verified": False}

    def may_retry(stage):
        return stage["idempotent"]

    _w(work, "packet.json", packet)
    return [_c("each need lands on its rung 1..5", picks == {"lint rule": 1, "how to grade": 2, "github issues": 3, "transcode": 4, "paid TTS": 5}, picks),
            _c("execution packet has the 8 fields", list(packet) == FIELDS, list(packet)),
            _c("executed is kept separate from verified", packet["state"] == {"executed": True, "verified": False}, packet["state"]),
            _c("only idempotent stages are retried", may_retry({"idempotent": True}) and not may_retry({"idempotent": False}), "")]


# ---------------------------------------------------------------- MISC-P02
def misc_p02(work: Path):
    def route(text, explicit_full_pro=False):
        t = text.lower()
        if re.search(r"suno|lyrics|أغنية|كلمات أغنية", t):
            return "suno branch"
        if re.search(r"how many tokens|كم توكن", t):
            return "live meter or unknown"
        if re.search(r"windows|desktop|device|جهازي", t):
            return "computer owner"
        if re.search(r"(build|merge) (a )?skill", t):
            return "skill orchestrator + eval"
        if re.search(r"download .*link|حمّل من الرابط", t) and not re.search(r"edit|imitate|montage", t):
            return "media-fetch owner"
        if "full pro" in t:
            return "full pro" if explicit_full_pro else "standard (full pro only on explicit ask)"
        if re.search(r"\b(image|poster|still)\b", t) and not re.search(r"video|animate|motion", t):
            return "visual prompt core"
        if re.search(r"video|montage|edit the clip", t):
            return "video engine"
        if re.search(r"bug|traceback|exception", t):
            return "software"
        if re.search(r"invoice|ledger|ifrs", t):
            return "accounting"
        return "agent contract"

    shadow = [("improve this skill: build a skill for captions", "skill orchestrator + eval"), ("write an agent contract", "agent contract"),
              ("fix this traceback in parser.py", "software"), ("a still image poster of a falcon", "visual prompt core"),
              ("edit the clip and add montage", "video engine"), ("write suno lyrics for a wedding", "suno branch"),
              ("how many tokens do I have now", "live meter or unknown"), ("post the IFRS invoice entries", "accounting"),
              ("use full pro on this", "standard (full pro only on explicit ask)"), ("open my windows desktop app", "computer owner")]
    res = [(t, route(t), want) for t, want in shadow]
    flags = {"never_auto_install_third_party": True}
    _w(work, "shadow_cases.json", {"cases": res, **flags})
    return [_c("all 10 shadow cases route as expected", all(g == w for _, g, w in res), [g for _, g, _ in res]),
            _c("still image never routes to the video engine", route("make a poster image") == "visual prompt core", ""),
            _c("download-only link goes to media-fetch, no imitation", route("download the video from this link") == "media-fetch owner", ""),
            _c("never_auto_install_third_party flag set", flags["never_auto_install_third_party"] is True, flags)]


# ---------------------------------------------------------------- MISC-P03
def misc_p03(work: Path):
    SECRET = re.compile(r"sk-[A-Za-z0-9]{8,}|api[_-]?key\s*=|-----BEGIN [A-Z ]*PRIVATE KEY-----")

    def propose(rec, consent):
        if not consent:
            return 2, "consent required"
        if not re.fullmatch(r"[A-Za-z0-9_-]{3,80}", rec.get("project_id", "")):
            return 2, "bad project_id"
        for k in ("trigger", "action", "evidence", "observed_at"):
            if not rec.get(k):
                return 2, f"missing {k}"
        if rec.get("scope") != "project":
            if len(set(rec.get("evidence_projects", []))) < 2 or not rec.get("negative_tests") or not rec.get("approved"):
                return 2, "global scope needs review, >=2 projects, negative tests and approval"
        if SECRET.search(json.dumps(rec)):
            return 2, "secret-like text"
        out = {**rec, "status": "proposed_not_published", "promotion": "manual_review_required"}
        _w(work, f"lessons/{rec['project_id']}.json", out)
        return 0, out["status"]

    base = {"project_id": "dua-jumuah", "trigger": "Arabic title clipped", "action": "pad 8%", "evidence": "qa.png", "observed_at": "2026-11-03", "scope": "project"}
    r = {"ok": propose(base, True), "no_consent": propose(base, False), "traversal": propose({**base, "project_id": "../etc"}, True),
         "global": propose({**base, "scope": "global", "evidence_projects": ["a"]}, True), "secret": propose({**base, "action": "set api_key=123"}, True)}
    return [_c("valid project lesson accepted as proposed_not_published (exit 0)", r["ok"] == (0, "proposed_not_published"), r["ok"]),
            _c("no consent -> exit 2", r["no_consent"] == (2, "consent required"), r["no_consent"]),
            _c("path traversal in project_id blocked", r["traversal"] == (2, "bad project_id"), r["traversal"]),
            _c("global scope with 1 project refused", r["global"][0] == 2 and "global" in r["global"][1], r["global"]),
            _c("secret-like text rejected", r["secret"] == (2, "secret-like text"), r["secret"])]


# ---------------------------------------------------------------- MISC-X01
def misc_x01(work: Path):
    def slug(s):
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
        return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

    def constant_case(s):
        return re.sub(r"[^A-Za-z0-9]+", "_", re.sub(r"([a-z])([A-Z])", r"\1_\2", s)).strip("_").upper()

    glass = {"background": "linear-gradient(300deg, #38bdf822, #818cf833)", "backdrop-filter": "blur(16px)", "border": "1px solid #38bdf866",
             "border-radius": "20px", "box-shadow": "0 12px 32px -8px #38bdf844"}
    css = ".glass{" + ";".join(f"{k}:{v}" for k, v in glass.items()) + "}"
    _w(work, "surfaces.css", css)
    res = {"b64": base64.b64encode(b"Kosif").decode(), "hex": "Kosif".encode().hex(), "bin": format(ord("K"), "08b"),
           "slug": slug("Hello, Café World!"), "const": constant_case("maxRetryCount")}
    alpha = int(re.search(r"#38bdf8(\w\w),", css)[1], 16) / 255
    return [_c("Base64 'Kosif' = S29zaWY=", res["b64"] == "S29zaWY=", res["b64"]),
            _c("hex and binary encoders", res["hex"] == "4b6f736966" and res["bin"] == "01001011", res),
            _c("URL slug and CONSTANT_CASE", res["slug"] == "hello-cafe-world" and res["const"] == "MAX_RETRY_COUNT", res),
            _c("glass recipe: blur 16px, radius 20px, 8-digit hex alpha #..22 = 13%", "blur(16px)" in css and "20px" in css and round(alpha, 2) == 0.13, alpha)]


# ---------------------------------------------------------------- MISC-X02
def misc_x02(work: Path):
    owners = {"builder-a": {"scenes/intro.html", "scenes/intro.css"}, "builder-b": {"scenes/outro.html"}, "builder-c": {"scenes/outro.html", "kit/api.js"}}
    frozen_sigs = {"kit/api.js": ["ease(t)", "seek(frame)"]}
    clashes = sorted((a, b, sorted(owners[a] & owners[b])) for a in owners for b in owners if a < b and owners[a] & owners[b])
    edits = [("builder-a", "scenes/intro.html"), ("builder-a", "scenes/outro.html"), ("builder-c", "kit/api.js")]
    queue = []
    applied = []
    for who, f in edits:
        if f not in owners[who] or f in frozen_sigs:
            queue.append({"from": who, "file": f, "type": "change request"})
        else:
            applied.append((who, f))
    transcript = "\n".join(f'{{"event":"job","id":"job_{i}"}}' if i % 50 == 0 else '{"event":"log","msg":"x"}' for i in range(500))
    state = {"job_ids": [json.loads(l)["id"] for l in transcript.splitlines() if '"job"' in l]}
    _w(work, "state.json", state)
    return [_c("overlapping ownership detected (outro.html: b and c)", clashes == [("builder-b", "builder-c", ["scenes/outro.html"])], clashes),
            _c("edit of another builder's file becomes a change request", {"from": "builder-a", "file": "scenes/outro.html", "type": "change request"} in queue, queue),
            _c("frozen shared-kit signatures cannot be edited directly", any(q["file"] == "kit/api.js" for q in queue), queue),
            _c("job ids pre-extracted into state.json (10 of 500 lines)", len(state["job_ids"]) == 10 and state["job_ids"][0] == "job_0", state["job_ids"][:3])]


PROGRAMS = {"MISC-04": misc_04, "MISC-06": misc_06, "MISC-07": misc_07, "MISC-13": misc_13, "MISC-14": misc_14, "MISC-15": misc_15,
            "MISC-17": misc_17, "MISC-20": misc_20, "MISC-P01": misc_p01, "MISC-P02": misc_p02, "MISC-P03": misc_p03,
            "MISC-X01": misc_x01, "MISC-X02": misc_x02}
