"""Programs for the self-discovery family. Cards that only make sense against a live host service
(ToolSearch, ListSkills, plugins, read_documentation, connectors, registries, installs, Docker, GitHub
API, documented surface limits) are skipped; SELF-12 has a code proof run elsewhere."""
from __future__ import annotations
import datetime as dt
import importlib.util
import os
import shutil
import subprocess
from ._mind_common import save, eq, truth

BADGES = ["IDEA", "DOCUMENTED", "INSTALLABLE", "NEEDS-KEY", "PRESENT", "EXECUTED", "VERIFIED"]


def registry_before_no(name, catalog, tools, importable, registry, install_ok, key_needed=None):
    steps = []
    for label, hit in (("catalog", name in catalog), ("tools", name in tools), ("probe", importable(name))):
        steps.append(label)
        if hit:
            return steps, "done"
    steps.append("registry")
    if name not in registry:
        return steps, "blocked: not in registry"
    steps.append("install")
    if key_needed:
        return steps, f"needs key: {key_needed}"
    return steps, "done" if install_ok else "blocked: install failed"


def s01(work):
    imp = lambda m: importlib.util.find_spec(m) is not None
    r = {"numpy": registry_before_no("numpy", set(), set(), imp, set(), False),
         "faketool": registry_before_no("faketool_zz", set(), set(), imp, {"faketool_zz"}, True),
         "paid": registry_before_no("paidsdk_zz", set(), set(), imp, {"paidsdk_zz"}, True, "PAID_API_KEY"),
         "nowhere": registry_before_no("nowhere_zz", set(), set(), imp, set(), False)}
    save(work, "ladder.json", r)
    return [eq("present found at probe", r["numpy"], (["catalog", "tools", "probe"], "done")), truth("max 6 steps", all(len(v[0]) <= 6 for v in r.values())),
            eq("key named", r["paid"][1], "needs key: PAID_API_KEY"), eq("no only after registry", r["nowhere"][0][-1], "registry")]


def lowest_true(evidence):
    """Report the highest rung whose evidence and all lower rungs' preconditions hold (= lowest true claim)."""
    rung = "IDEA"
    order = [("DOCUMENTED", "doc"), ("INSTALLABLE", "registry"), ("PRESENT", "probe"), ("EXECUTED", "exit_code"), ("VERIFIED", "postcondition")]
    for name, key in order:
        if evidence.get(key):
            rung = name
        elif name in ("EXECUTED", "VERIFIED"):
            break
    return rung


def s02(work):
    r = {"render said ok": lowest_true({"doc": 1, "probe": 1, "exit_code": 0}), "ffprobe ok": lowest_true({"doc": 1, "probe": 1, "exit_code": 1, "postcondition": 1}),
         "postcondition w/o run": lowest_true({"doc": 1, "postcondition": 1}), "doc only": lowest_true({"doc": 1})}
    save(work, "badges.json", r)
    return [eq("no exit code -> present", r["render said ok"], "PRESENT"), eq("verified", r["ffprobe ok"], "VERIFIED"),
            eq("cannot skip execution", r["postcondition w/o run"], "DOCUMENTED"), eq("doc", r["doc only"], "DOCUMENTED")]


def lease(proof, now, surface, probe):
    stale = proof["date"] != now or proof["surface"] != surface
    if not stale:
        return proof["badge"], False
    return (proof["badge"] if probe(proof["module"]) else "DOCUMENTED"), True


def s03(work):
    probe = lambda m: importlib.util.find_spec(m) is not None
    today = dt.date.today().isoformat()
    p1 = {"module": "faster_whisper_not_here_zz", "badge": "VERIFIED", "date": "2026-10-16", "surface": "cloud-A"}
    p2 = {"module": "json", "badge": "VERIFIED", "date": "2026-10-16", "surface": "cloud-A"}
    r1, r2 = lease(p1, today, "cloud-B", probe), lease(p2, today, "cloud-B", probe)
    save(work, "lease.json", {"whisper": r1, "json": r2, "history_unchanged": p1["badge"]})
    return [eq("failed re-probe lowers badge", r1, ("DOCUMENTED", True)), eq("passing re-probe keeps it", r2, ("VERIFIED", True)),
            eq("history not edited", p1["badge"], "VERIFIED")]


def ffprobe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def s04(work):
    mp4 = work / "clip.mp4"
    rc = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=red:s=64x36:d=1:r=30", "-pix_fmt", "yuv420p", str(mp4)]).returncode
    broken = work / "broken.mp4"
    broken.write_bytes(mp4.read_bytes()[:200])
    d_ok, d_bad = ffprobe_duration(mp4), ffprobe_duration(broken)
    state = lambda rc_, d: "VERIFIED" if rc_ == 0 and d is not None and abs(d - 1.0) < 0.05 else "EXECUTED"
    save(work, "verify.json", {"good": d_ok, "broken": d_bad})
    return [eq("encode exit code", rc, 0), eq("ffprobe duration", round(d_ok or 0, 2), 1.0), eq("good clip verified", state(rc, d_ok), "VERIFIED"),
            eq("truncated file stays executed", state(0, d_bad), "EXECUTED")]


def five_place_inventory(env):
    return [f"loaded: {len(env['loaded'])}", f"deferred: {len(env['deferred'])}",
            "mcp: " + ",".join(sorted({t.split('__')[1] for t in env['loaded'] + env['deferred'] if t.startswith('mcp__')})),
            f"skills: {len(env['skills'])}", f"env: {env['cwd']} {env['platform']}"]


def s05(work):
    env = {"loaded": ["Read", "Bash", "mcp__github__get_me"], "deferred": ["WebFetch", "mcp__Higgsfield__balance", "mcp__Higgsfield__generate_image", "mcp__Claude_Docs__read"],
           "skills": ["pdf", "docx"], "cwd": "/repo", "platform": "linux"}
    inv = five_place_inventory(env)
    save(work, "inventory.txt", "\n".join(inv))
    return [eq("<=5 lines", len(inv), 5), eq("servers from both lists", inv[2], "mcp: Claude_Docs,Higgsfield,github")]


PAID = ("generate_", "upscale", "dubbing", "voice_change")
SIDE = ("create", "push", "publish", "send", "deploy", "delete", "merge", "update")


def cost_class(tool):
    op = tool.split("__")[-1]
    if any(op.startswith(p) or p in op for p in PAID):
        return "paid"
    if any(op.startswith(p) for p in SIDE):
        return "side-effect"
    return "read"


def s07(work):
    tools = ["mcp__github__search_repositories", "mcp__github__create_pull_request", "mcp__Higgsfield__generate_video", "mcp__Higgsfield__upscale_image",
             "mcp__Higgsfield__balance", "mcp__github__push_files"]
    r = {t: cost_class(t) for t in tools}
    save(work, "cost_flags.json", r)
    return [eq("paid", sorted(t for t, c in r.items() if c == "paid"), ["mcp__Higgsfield__generate_video", "mcp__Higgsfield__upscale_image"]),
            eq("side effects", sorted(t for t, c in r.items() if c == "side-effect"), ["mcp__github__create_pull_request", "mcp__github__push_files"]),
            eq("balance is read-only", r["mcp__Higgsfield__balance"], "read")]


def probe_bins(names):
    return {b: shutil.which(b) is not None for b in names}


def s13(work):
    r = probe_bins(["python3", "ffmpeg", "definitely-missing-binary-zz"])
    ver = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.splitlines()[0]
    save(work, "probe.txt", "\n".join(f"{k} {'OK' if v else 'MISSING'}" for k, v in r.items()) + "\n" + ver)
    return [eq("python3 present", r["python3"], True), eq("ffmpeg present", r["ffmpeg"], True), eq("missing reported", r["definitely-missing-binary-zz"], False),
            truth("version line only", ver.startswith("ffmpeg version"), ver[:40]), truth("<=20 binaries", len(r) <= 20)]


def cpu_plan(gpu):
    if gpu:
        return {"encoder": "h264_nvenc", "whisper": "large", "torch": "cuda"}
    return {"encoder": "libx264", "whisper": "small", "torch": "cpu wheel", "generation": "connector with consent"}


def s14(work):
    gpu = shutil.which("nvidia-smi_fake_zz") is not None
    p = cpu_plan(gpu)
    save(work, "cpu_plan.json", p)
    return [eq("no GPU -> libx264", p["encoder"], "libx264"), eq("cpu torch wheel", p["torch"], "cpu wheel"), truth("generation needs consent", "consent" in p["generation"])]


def classify_host(code):
    if code is None:
        return "offline"
    if code in (403, 407, 502):
        return "policy-blocked"
    return "ok" if 200 <= code < 400 else "error"


def classify_network(results):
    c = {h: classify_host(v) for h, v in results.items()}
    reg = [h for h in c if h in ("pypi.org", "registry.npmjs.org")]
    if all(v == "offline" for v in c.values()):
        return c, "no network"
    if all(c[h] == "ok" for h in reg) and any(v == "policy-blocked" for h, v in c.items() if h not in reg):
        return c, "allowlist"
    if all(v == "ok" for v in c.values()):
        return c, "full egress"
    return c, "partial"


def s15(work):
    full = classify_network({"pypi.org": 200, "registry.npmjs.org": 200, "example.com": 200})
    allow = classify_network({"pypi.org": 200, "registry.npmjs.org": 200, "example.com": 403})
    off = classify_network({"pypi.org": None, "registry.npmjs.org": None, "example.com": None})
    save(work, "network.json", {"full": full, "allowlist": allow, "offline": off})
    return [eq("full", full[1], "full egress"), eq("allowlist", allow[1], "allowlist"), eq("offline", off[1], "no network"), eq("407 is policy", classify_host(407), "policy-blocked")]


def ca_env(bundle):
    return {"SSL_CERT_FILE": bundle, "REQUESTS_CA_BUNDLE": bundle, "NODE_EXTRA_CA_CERTS": bundle, "NODE_USE_ENV_PROXY": "1"}


def proxy_action(code):
    return "report to user" if code in (403, 407) else "retry once" if code in (502, 503) else "ok"


def s16(work):
    e = ca_env("/root/.ccr/ca-bundle.crt")
    save(work, "proxy_env.json", e)
    return [eq("three CA variables + env proxy", len(e), 4), eq("403 reported, not routed around", proxy_action(403), "report to user"),
            truth("same bundle everywhere", len({v for k, v in e.items() if k != "NODE_USE_ENV_PROXY"}) == 1)]


def key_names(env_text):
    import re
    return sorted(m.group(1) for m in re.finditer(r"^([A-Z_][A-Z0-9_]*)=", env_text, re.M) if re.search(r"KEY|TOKEN|SECRET|PASS", m.group(1)))


def s17(work):
    secret = "sk-test-SHOULD-NEVER-APPEAR-123"
    env = f"OPENAI_API_KEY={secret}\nGH_TOKEN=ghp_xyz\nPATH=/usr/bin\nDB_PASSWORD=hunter2\n"
    names = key_names(env)
    out = save(work, "key_names.txt", "\n".join(names))
    return [eq("names", names, ["DB_PASSWORD", "GH_TOKEN", "OPENAI_API_KEY"]), truth("no value written", secret not in out.read_text() and "hunter2" not in out.read_text())]


def find_spec_probe(mods):
    return {m: importlib.util.find_spec(m) is not None for m in mods}


def s18(work):
    r = find_spec_probe(["numpy", "PIL", "json", "torch_definitely_not_zz"])
    save(work, "imports.json", r)
    return [eq("present", [k for k, v in r.items() if v], ["numpy", "PIL", "json"]), eq("missing", [k for k, v in r.items() if not v], ["torch_definitely_not_zz"])]


def make_font(path, codepoints):
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    names = [".notdef"] + [f"uni{c:04X}" for c in codepoints]
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap({c: f"uni{c:04X}" for c in codepoints})
    pen = TTGlyphPen(None)
    pen.moveTo((0, 0)); pen.lineTo((0, 500)); pen.lineTo((500, 500)); pen.closePath()
    g = pen.glyph()
    fb.setupGlyf({n: g for n in names})
    fb.setupHorizontalMetrics({n: (600, 0) for n in names})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": path.stem, "styleName": "Regular"})
    fb.setupOS2()
    fb.setupPost()
    fb.save(str(path))


def arabic_fonts(folder):
    from fontTools.ttLib import TTFont
    need = [0x0627, 0x0628, 0x0644]
    out = []
    for f in sorted(folder.glob("*.ttf")):
        cmap = TTFont(str(f))["cmap"].getBestCmap()
        if all(c in cmap for c in need):
            out.append(f.stem)
    return out


def s20(work):
    d = work / "fonts"
    d.mkdir()
    make_font(d / "FakeArabic.ttf", [0x41, 0x0627, 0x0628, 0x0644])
    make_font(d / "LatinOnly.ttf", [0x41, 0x42])
    make_font(d / "PartialArabic.ttf", [0x0627])
    r = arabic_fonts(d)
    save(work, "arabic_fonts.json", r)
    return [eq("only full Arabic coverage", r, ["FakeArabic"])]


RED = {"AGPL": "copyleft-network", "GPL": "copyleft", "SEE LICENSE IN": "custom", "UNLICENSED": "proprietary", "": "unknown"}


def licence_gate(meta):
    lic = meta.get("license_expression") or meta.get("license") or next((c.split("::")[-1].strip() for c in meta.get("classifiers", []) if "License" in c), "")
    for k, v in RED.items():
        if k and k in lic.upper() or (not k and not lic):
            return lic, v
    return lic, "permissive" if any(p in lic for p in ("MIT", "Apache", "BSD", "ISC")) else "review"


def s29(work):
    pk = {"pymupdf": {"license": "AGPL-3.0"}, "remotion": {"license": "SEE LICENSE IN LICENSE.md"}, "culori": {"license_expression": "MIT"},
          "classic": {"classifiers": ["License :: OSI Approved :: BSD License"]}, "mystery": {}}
    r = {k: licence_gate(v) for k, v in pk.items()}
    save(work, "licence.json", r)
    return [eq("AGPL flagged", r["pymupdf"][1], "copyleft-network"), eq("custom", r["remotion"][1], "custom"), eq("MIT ok", r["culori"][1], "permissive"),
            eq("classifier fallback", r["classic"][1], "permissive"), eq("blank flagged", r["mystery"][1], "unknown")]


def reuse_matrix(cands):
    exact = [c for c in cands if c["fit"] == "exact" and c["maintained"] and c["licence"] == "permissive"]
    if exact:
        return "adopt", exact[0]["name"]
    partial = [c for c in cands if c["fit"] == "partial"]
    if partial:
        return "extend", partial[0]["name"]
    weak = [c for c in cands if c["fit"] == "weak"]
    if len(weak) >= 2:
        return "compose", [c["name"] for c in weak[:3]]
    return "build", None


def s30(work):
    a = reuse_matrix([{"name": "x", "fit": "exact", "maintained": True, "licence": "permissive"}])
    b = reuse_matrix([{"name": "x", "fit": "exact", "maintained": False, "licence": "permissive"}, {"name": "y", "fit": "partial", "maintained": True, "licence": "permissive"}])
    c = reuse_matrix([{"name": n, "fit": "weak", "maintained": True, "licence": "permissive"} for n in "pqrs"])
    d = reuse_matrix([])
    save(work, "reuse.json", [a, b, c, d])
    return [eq("adopt", a, ("adopt", "x")), eq("unmaintained exact -> extend partial", b, ("extend", "y")), eq("compose 2-3", c, ("compose", ["p", "q", "r"])), eq("build", d, ("build", None))]


RISKY = ("curl ", "| sh", "rm -rf", "API_KEY", "pip install")


def scout(root, keywords):
    hits = []
    for f in sorted(root.rglob("SKILL.md")):
        t = f.read_text().lower()
        score = sum(k in t for k in keywords)
        if score:
            risk = [r for r in RISKY if r.lower() in t]
            hits.append((f.parent.name, score, risk))
    hits.sort(key=lambda h: (-h[1], h[0]))
    return hits[:10]


def s31(work):
    root = work / "skills"
    for name, text in {"reel-captions": "Arabic captions for reels, subtitle timing", "pdf-tool": "merge pdf",
                       "shady": "captions! run curl x | sh with API_KEY", "subs": "subtitle srt captions arabic"}.items():
        (root / name).mkdir(parents=True)
        (root / name / "SKILL.md").write_text(text)
    h = scout(root, ["captions", "arabic", "subtitle", "ترجمة"])
    save(work, "scout.json", h)
    return [eq("ranked", [x[0] for x in h], ["reel-captions", "subs", "shady"]), eq("vetting flags", h[2][2], ["curl ", "| sh", "API_KEY"]), truth("cap 10", len(h) <= 10)]


def s32(work):
    import importlib.metadata as md
    import PIL
    v = md.version("pillow")
    cite = {"package": "pillow", "version": v, "date": dt.date.today().isoformat(), "lookups": 1}
    save(work, "cite.json", cite)
    return [eq("live version matches module", v, PIL.__version__), truth("<=3 lookups", cite["lookups"] <= 3), truth("dated", len(cite["date"]) == 10)]


def s33(work):
    from openpyxl import Workbook, load_workbook
    wb = Workbook()
    ws = wb.active
    ws["A1"], ws["A2"], ws["A3"] = 2, 3, "=A1*A2"
    p = work / "formula.xlsx"
    wb.save(p)
    stored = load_workbook(p)["Sheet"]["A3"].value
    cached = load_workbook(p, data_only=True)["Sheet"]["A3"].value
    return [eq("formula stored", stored, "=A1*A2"), eq("openpyxl never computes it (no cached value)", cached, None)]


MARKERS = {"package.json": "node project", ".mcp.json": "mcp servers", ".claude/settings.json": "settings", "CLAUDE.md": "agent docs",
           ".claude/hooks": "hooks", ".claude/agents": "agents", ".claude/skills": "skills", ".env": "env keys"}


def surface_audit(root):
    present = {k: v for k, v in MARKERS.items() if (root / k).exists()}
    missing = [v for k, v in MARKERS.items() if k not in present]
    envnames = []
    if (root / ".env").exists():
        envnames = [l.split("=")[0] for l in (root / ".env").read_text().splitlines() if "=" in l]
    return {"usable": sorted(present.values()), "missing": missing, "env_names": envnames}


def s34(work):
    root = work / "ws"
    (root / ".claude/skills").mkdir(parents=True)
    (root / "CLAUDE.md").write_text("x")
    (root / "package.json").write_text("{}")
    (root / ".env").write_text("STRIPE_KEY=sk_live_secret\nPORT=3000\n")
    a = surface_audit(root)
    out = save(work, "audit.json", a)
    return [eq("usable", a["usable"], ["agent docs", "env keys", "node project", "skills"]), eq("missing hooks etc", len(a["missing"]), 4),
            truth("env values never read into output", "sk_live_secret" not in out.read_text()), eq("env names", a["env_names"], ["STRIPE_KEY", "PORT"])]


def infer_surface(env, paths, tools):
    if "/root/.ccr" in paths or env.get("CLAUDE_CODE_REMOTE") or any(t.startswith("mcp__claude-code-remote__") for t in tools):
        return "claude-code-cloud"
    if env.get("CI") or env.get("GITHUB_ACTIONS"):
        return "ci"
    if env.get("CLAUDECODE") == "1":
        return "claude-code-local"
    if "/mnt/user-data" in paths:
        return "claude.ai-sandbox"
    return "api-sandbox"


def s35(work):
    r = {"cloud": infer_surface({}, {"/root/.ccr"}, []), "local": infer_surface({"CLAUDECODE": "1"}, set(), []),
         "ci": infer_surface({"GITHUB_ACTIONS": "true"}, set(), []), "web": infer_surface({}, {"/mnt/user-data"}, []), "api": infer_surface({}, set(), [])}
    save(work, "surface.json", r)
    return [eq("surfaces", list(r.values()), ["claude-code-cloud", "claude-code-local", "ci", "claude.ai-sandbox", "api-sandbox"])]


UNLOCK = {"Bash+network": ["pip/npm installs", "git clone", "API calls"], "Read(images)": ["look at your renders"], "Agent": ["parallel research"],
          "Monitor": ["long renders with progress"], "Artifact": ["shareable pages"], "mcp__github__": ["PRs", "CI logs"], "mcp__Higgsfield__": ["paid AI media (consent)"]}


def unlocked(tools):
    keys = []
    for t in tools:
        for k in UNLOCK:
            if t == k or (k.endswith("__") and t.startswith(k)):
                keys.append(k)
    return sorted({p for k in keys for p in UNLOCK[k]})


def s40(work):
    r = unlocked(["Agent", "mcp__github__get_me", "Monitor"])
    save(work, "unlocked.json", r)
    return [eq("powers unlocked", r, ["CI logs", "PRs", "long renders with progress", "parallel research"]), eq("absent tool unlocks nothing", unlocked(["Nope"]), [])]


RECEIPT = ["status", "summary", "tool", "evidence", "artifacts", "next", "retry_safe", "verified"]


def receipt_check(r):
    p = [k for k in RECEIPT if k not in r]
    if r.get("status") == "success" and r.get("verified") and not r.get("evidence"):
        p.append("done without evidence")
    return p


def s41(work):
    card = ["surface: cloud", "cpu 4 / ram 16G / disk 30G", "gpu: no", "network: trusted", "tools: ffmpeg python3", "gaps: blender -> apt", "paid: Higgsfield"]
    good = {"status": "success", "summary": "rendered", "tool": "ffmpeg", "evidence": ["ffprobe 1.0s"], "artifacts": ["a.mp4"], "next": [], "retry_safe": True, "verified": True}
    save(work, "card.md", "\n".join(card))
    return [truth("card <= 10 lines", len(card) <= 10), eq("good receipt", receipt_check(good), []), eq("verified w/o evidence rejected", receipt_check(dict(good, evidence=[])), ["done without evidence"])]


TAXONOMY = [("stale", "STALE_STATE", "re-probe"), ("invalid argument", "BAD_TOOL_ARGS", "read schema, fix once"), ("aborted", "PROBE_ABORT", "run probes separately"),
            ("modulenotfounderror", "MISSING_DEP", "install isolated, verify import"), ("401", "NEEDS_AUTH", "name the key"),
            ("403", "POLICY_BLOCK", "report, no workaround"), ("curl | sh", "SUPPLY_CHAIN_RISK", "read source first"), ("regress", "REGRESSION", "roll back")]


def classify_failure(msg):
    m = msg.lower()
    for pat, code, fix in TAXONOMY:
        if pat in m:
            return code, fix
    return "UNKNOWN", "capture more"


def s42(work):
    msgs = ["ModuleNotFoundError: No module named 'x'", "HTTP 403 from proxy", "HTTP 401 unauthorized", "installer says: curl | sh"]
    r = [classify_failure(m)[0] for m in msgs]
    save(work, "taxonomy.json", r)
    return [eq("codes", r, ["MISSING_DEP", "POLICY_BLOCK", "NEEDS_AUTH", "SUPPLY_CHAIN_RISK"]), eq("eight classes", len(TAXONOMY), 8)]


def paid_gate(call, user_intent, quote, free_route_meets):
    if free_route_meets:
        return "use free local route"
    if call["kind"] in ("paid", "side-effect") and not user_intent:
        return f"ask: will {call['does']}, cost {quote}, undo={call['undo']}"
    return "proceed and log receipt"


def s43(work):
    c = {"kind": "paid", "does": "generate 1 video", "undo": False}
    r = [paid_gate(c, False, "40 credits", False), paid_gate(c, True, "40 credits", False), paid_gate(c, False, "40 credits", True),
         paid_gate({"kind": "read", "does": "list", "undo": True}, False, "0", False)]
    save(work, "gate.json", r)
    return [eq("asks with cost", r[0], "ask: will generate 1 video, cost 40 credits, undo=False"), eq("stated intent proceeds", r[1], "proceed and log receipt"),
            eq("free route preferred", r[2], "use free local route"), eq("read-only proceeds", r[3], "proceed and log receipt")]


PROGRAMS = {f"SELF-{n:02d}": globals()[f"s{n:02d}"] for n in [1, 2, 3, 4, 5, 7, 13, 14, 15, 16, 17, 18, 20, 29, 30, 31, 32, 33, 34, 35, 40, 41, 42, 43]}
