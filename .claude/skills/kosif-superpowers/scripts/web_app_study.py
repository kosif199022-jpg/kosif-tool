#!/usr/bin/env python3
"""Read-only study of a PUBLIC web app's frontend with REA, then a facts-only report.

Written after the MagicPath study (2026-10-20); replaces a Windows-only PowerShell kit with one
cross-platform command. What it does:

  run      launch an isolated, logged-out headless Chromium (fresh profile, deleted afterwards),
           then REA: list targets → passive page capture (scripts, JSON body shapes, storage key
           NAMES only) → page-declared WebMCP tools → one screenshot → export the public scripts →
           optional bounded static JavaScript analysis (--deep). Every artifact gets a SHA-256
           receipt. The study folder must be outside any git checkout: it holds third-party code.
  report   derive FACTS ONLY from a study folder: framework, libraries (with versions when the
           bundle states them), services inferred from storage key names, WebMCP tools, page
           metrics. Evidence is a file name plus an identifier; never code.
  doctor   find REA and a Chromium/Chrome/Edge binary.

Guardrails: http(s) only, an exact-origin allow list (the URL's own origin by default), no login,
no cookies carried in or out, no form filling, one page per run. Use it on sites you may study;
borrow ideas in your own words, never their code (clean-room).
"""
from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import glob
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

VERSION = "1.0"
ARTIFACTS = ("01-targets.json", "02-page-capture.json", "04-webmcp.json", "05-screenshot.json", "06-export.json", "07-js-graph.json")

# --------------------------------------------------------------------------- fingerprints
# (category, name, regex on script text, optional version regex). Identifiers only.
SCRIPT_FINGERPRINTS = [
    ("framework", "React", r"rendererPackageName:\s*\"react-dom\"|__REACT_DEVTOOLS_GLOBAL_HOOK__", r"version:\s*\"(\d+\.\d+\.\d+[\w.-]*)\",\s*rendererPackageName:\s*\"react-dom\"|rendererPackageName:\s*\"react-dom\"[^}]{0,120}?version:\s*\"(\d+\.\d+\.\d+[\w.-]*)\""),
    ("framework", "Next.js", r"__NEXT_DATA__|next/dist/|__next_f", r"window\.next\s*=\s*\{\s*version:\s*\"(\d+\.\d+\.\d+[\w.-]*)\""),
    ("framework", "Vue", r"__VUE__|__VUE_HMR_RUNTIME__", None),
    ("framework", "Svelte", r"__svelte|svelte-[a-z0-9]{6}", None),
    ("framework", "Angular", r"ng-version|ɵcmp", None),
    ("canvas-engine", "tldraw", r"\btldraw\b|@tldraw/", None),
    ("canvas-engine", "Excalidraw", r"excalidraw", None),
    ("canvas-engine", "Konva", r"\bKonva\b", None),
    ("canvas-engine", "Fabric.js", r"\bfabric\.(?:Canvas|Object)\b", None),
    ("canvas-engine", "PixiJS", r"\bPIXI\b|pixi\.js", None),
    ("canvas-engine", "three.js", r"__THREE__|THREE\.WebGLRenderer", r"REVISION\s*=\s*\"(\d+)\""),
    ("canvas-engine", "React Flow", r"react-flow__|@xyflow/", None),
    ("realtime", "Yjs", r"\bY\.Doc\b|yjs|y-protocols", None),
    ("realtime", "Liveblocks", r"liveblocks", None),
    ("realtime", "Socket.IO", r"socket\.io", None),
    ("realtime", "PartyKit", r"partykit|partysocket", None),
    ("editor", "Monaco", r"monaco-editor|\bmonaco\.editor\b", None),
    ("editor", "CodeMirror", r"\bcm-editor\b|@codemirror/", None),
    ("editor", "Tiptap", r"\btiptap\b", None),
    ("editor", "ProseMirror", r"ProseMirror", None),
    ("styling", "Tailwind CSS", r"--tw-[a-z-]+", None),
    ("styling", "Radix UI", r"data-radix-|@radix-ui/", None),
    ("styling", "Framer Motion", r"framer-motion|\bMotionConfig\b", None),
    ("state", "Zustand", r"\bzustand\b", None),
    ("state", "TanStack Query", r"@tanstack/|QueryClientProvider", None),
    ("auth", "Firebase", r"firebaseapp\.com|identitytoolkit\.googleapis\.com|firebase-installations", None),
    ("auth", "Clerk", r"\bclerk\.[a-z]+\.(?:com|dev)|__clerk", None),
    ("auth", "Supabase", r"supabase\.co\b|@supabase/", None),
    ("analytics", "Mixpanel", r"mixpanel", None),
    ("analytics", "PostHog", r"posthog", None),
    ("analytics", "Sentry", r"sentry\.io|__SENTRY__", None),
    ("analytics", "Vercel Analytics", r"/_vercel/insights|va\.vercel-scripts\.com", None),
    ("payments", "Stripe", r"js\.stripe\.com", None),
    ("ai", "Vercel AI SDK", r"\bai/rsc\b|@ai-sdk/", None),
]
# matched only by a bare package/product name, which can appear without the library being used
# (an import adapter, a paste handler, a comment): graded "mentioned" unless versioned or seen in 3+ files
NAME_ONLY = {"tldraw", "Excalidraw", "Konva", "PixiJS", "Yjs", "Liveblocks", "Socket.IO", "PartyKit", "Monaco", "Tiptap",
             "Zustand", "Mixpanel", "PostHog", "Svelte"}
# storage key NAMES (values are never read) → service
STORAGE_FINGERPRINTS = [
    ("Firebase", r"^firebase-|^firebase:"), ("Mixpanel", r"mixpanel|^__mpq_"), ("Google Ads", r"^_gcl_"),
    ("Google Analytics", r"^_ga(_|$)|^_gid$"), ("LinkedIn Ads", r"^li_"), ("Reddit Ads", r"^_rdt_"), ("Meta Pixel", r"^_fbp$"),
    ("TikTok Pixel", r"^_ttp$|^tt_"), ("Segment", r"^ajs_"), ("Amplitude", r"^amp_|^AMP_"), ("PostHog", r"posthog"),
    ("Intercom", r"intercom"), ("Hotjar", r"^_hj"), ("Sentry", r"sentry"),
]
HOSTING_FINGERPRINTS = [("Vercel", r"[?&]dpl=dpl_|/_vercel/"), ("Netlify", r"netlify"), ("Cloudflare", r"/cdn-cgi/")]
FRAMEWORK_URLS = [("Next.js", r"/_next/static/"), ("Nuxt", r"/_nuxt/"), ("SvelteKit", r"/_app/immutable/"), ("Astro", r"/_astro/"),
                  ("Gatsby", r"/page-data/"), ("Vite", r"/assets/index-[\w-]+\.js")]


# --------------------------------------------------------------------------- helpers
def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def origin_of(url: str) -> str:
    u = urllib.parse.urlsplit(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError("only http(s) URLs with a host can be studied")
    default = {"http": 80, "https": 443}[u.scheme]
    port = f":{u.port}" if u.port and u.port != default else ""
    return f"{u.scheme}://{u.hostname}{port}"


def inside_git(path: Path) -> bool:
    return any((p / ".git").exists() for p in [path, *path.parents])


def check_out_dir(out: Path) -> Path:
    out = out.expanduser().resolve()
    if inside_git(out):
        raise ValueError("the study folder holds third-party code: put it outside any git checkout")
    if out.exists() and any(out.iterdir()):
        raise ValueError("the study folder must be new or empty")
    return out


def find_rea() -> str | None:
    return shutil.which("rea") or shutil.which("rea.cmd")


def find_chromium(explicit: str | None = None) -> str | None:
    cands = [explicit, os.environ.get("KOSIF_CHROMIUM")]
    cands += [shutil.which(n) for n in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome", "msedge")]
    cands += sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"), reverse=True)
    cands += sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome")), reverse=True)
    cands += [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    return next((c for c in cands if c and Path(c).exists()), None)


def proxy_arg(proxy: str) -> list:
    if proxy == "none":
        return []
    if proxy == "auto":
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    return [f"--proxy-server={proxy}"] if proxy else []


def browser_argv(chrome: str, url: str, profile: Path, port: int, proxy: str) -> list:
    argv = [chrome, "--headless=new", "--remote-debugging-address=127.0.0.1", f"--remote-debugging-port={port}",
            f"--user-data-dir={profile}", "--no-first-run", "--no-default-browser-check", "--disable-extensions",
            "--disable-sync", "--window-size=1440,900", *proxy_arg(proxy)]
    if platform.system() == "Linux" and hasattr(os, "geteuid") and os.geteuid() == 0:
        argv.append("--no-sandbox")   # Chromium refuses to start as root otherwise (containers)
    return argv + [url]


def rea_steps(endpoint: str, target: str, origins: list, out: Path, obs_ms: int, deep: bool) -> list:
    allow = [x for o in origins for x in ("--allowed-origins", o)]
    steps = [
        ("02-page-capture.json", ["inspect-web-page", endpoint, target, *allow, "--include-script-sources", "--include-json-body-shapes",
                                  "--include-storage-keys", "--observation-ms", str(obs_ms)]),
        ("04-webmcp.json", ["discover-webmcp-tools", endpoint, target, *allow, "--observation-ms", str(min(obs_ms, 2000))]),
        ("05-screenshot.json", ["capture-web-screenshot", endpoint, target, *allow]),
        ("06-export.json", ["export-web-scripts", str(out / "02-page-capture.json"), str(out / "scripts-export")]),
    ]
    if deep:
        steps.append(("07-js-graph.json", ["analyze-javascript-application", str(out / "scripts-export" / "files"), "--artifact-format", "directory",
                                           "--max-semantic-nodes", "30000", "--max-semantic-nodes-per-file", "6000",
                                           "--max-semantic-unknowns", "20000", "--max-semantic-unknowns-per-file", "4000",
                                           "--max-heap-mb", "3072", "--analysis-timeout-ms", "240000"]))
    return steps


def run_rea(rea: str, args: list, dest: Path, timeout: int) -> dict:
    t0 = time.time()
    with open(dest, "wb") as fh:
        try:
            p = subprocess.run([rea, *args, "--format", "json"], stdout=fh, stderr=subprocess.PIPE, timeout=timeout)
            rc, err = p.returncode, p.stderr.decode("utf-8", "replace")[-400:]
        except subprocess.TimeoutExpired:
            rc, err = -1, f"timeout after {timeout}s"
    return {"command": args[0], "rc": rc, "seconds": round(time.time() - t0, 1), "stderr_tail": err if rc else ""}


# --------------------------------------------------------------------------- run
def run(url: str, out: str, allow=(), obs_ms: int = 3000, chromium: str | None = None, proxy: str = "auto", port: int = 9223,
        deep: bool = False, keep_profile: bool = False, dry_run: bool = False, settle_s: float = 6.0) -> dict:
    origin = origin_of(url)
    origins = sorted({origin, *(origin_of(a) for a in allow)})
    out_p = check_out_dir(Path(out))
    rea, chrome = find_rea(), find_chromium(chromium)
    profile = out_p / "isolated-profile"
    endpoint = f"http://127.0.0.1:{port}"
    plan = {"url": url, "origins": origins, "out": str(out_p), "browser": browser_argv(chrome or "<chromium>", url, profile, port, proxy),
            "rea_steps": [["list-browser-targets", endpoint, *[x for o in origins for x in ("--allowed-origins", o)]]]
                         + [a for _, a in rea_steps(endpoint, "<target>", origins, out_p, obs_ms, deep)],
            "profile": "fresh, deleted after the run" if not keep_profile else "fresh, kept", "login": "never"}
    if dry_run:
        return {"dry_run": True, "plan": plan}
    if not rea:
        raise RuntimeError("REA not found: npm install -g rea-agents (https://github.com/morluto/rea)")
    if not chrome:
        raise RuntimeError("no Chromium/Chrome/Edge found; pass --chromium PATH")
    out_p.mkdir(parents=True, exist_ok=True)
    started = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    log = open(out_p / "browser.log", "wb")
    proc = subprocess.Popen(browser_argv(chrome, url, profile, port, proxy), stdout=log, stderr=subprocess.STDOUT,
                            start_new_session=(os.name != "nt"))
    steps = []
    try:
        deadline = time.time() + 30
        while time.time() < deadline:
            try:
                urllib.request.build_opener(urllib.request.ProxyHandler({})).open(endpoint + "/json/version", timeout=2).read()
                break
            except OSError:
                time.sleep(0.5)
        else:
            raise RuntimeError("the browser did not open its DevTools port")
        time.sleep(settle_s)
        steps.append(run_rea(rea, ["list-browser-targets", endpoint, *[x for o in origins for x in ("--allowed-origins", o)]],
                             out_p / "01-targets.json", 120))
        targets = (json.loads((out_p / "01-targets.json").read_text(encoding="utf-8") or "{}").get("normalized_result") or {}).get("targets", [])
        target = next((t["target_id"] for t in targets if t.get("type") == "page" and t.get("origin") in origins), None)
        if not target:
            raise RuntimeError("no page target on the allowed origins (redirected elsewhere?)")
        for name, args in rea_steps(endpoint, target, origins, out_p, obs_ms, deep):
            steps.append(run_rea(rea, args, out_p / name, 1800 if name.startswith("07") else 600))
    finally:
        try:
            if os.name != "nt":
                os.killpg(proc.pid, signal.SIGTERM)
            else:
                proc.terminate()
            proc.wait(timeout=15)
        except Exception:  # noqa: BLE001
            proc.kill()
        log.close()
        if not keep_profile:
            shutil.rmtree(profile, ignore_errors=True)
    shot = out_p / "05-screenshot.json"
    if shot.exists() and shot.stat().st_size:
        art = (json.loads(shot.read_text(encoding="utf-8")).get("normalized_result") or {}).get("artifact") or {}
        if art.get("data_base64"):
            png = base64.b64decode(art["data_base64"])
            if hashlib.sha256(png).hexdigest() == art.get("sha256"):
                (out_p / "screenshot.png").write_bytes(png)
    receipts = {"tool": f"web_app_study.py {VERSION}", "rea": _version([rea, "--version"]), "browser": _version([chrome, "--version"]),
                "url": url, "origins": origins, "started_at": started, "profile_deleted": not keep_profile, "login": False,
                "steps": steps, "artifacts": _artifact_receipts(out_p)}
    (out_p / "receipts.json").write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")
    rep = report(out_p)
    return {"out": str(out_p), "steps": steps, "report": str(out_p / "report.md"), "facts": len(rep["stack"])}


def _version(argv) -> str:
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=30).stdout.strip().splitlines()[0]
    except Exception:  # noqa: BLE001
        return "unknown"


def _artifact_receipts(out: Path) -> list:
    rows = []
    for p in sorted(out.iterdir()):
        if p.is_file() and p.suffix in (".json", ".png") and p.name not in ("receipts.json", "report.json"):
            rows.append({"file": p.name, "bytes": p.stat().st_size, "sha256": sha_file(p)})
    return rows


# --------------------------------------------------------------------------- report
def _load(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() and p.stat().st_size else {}
    except (OSError, ValueError):
        return {}


def report(study, json_out=None, md_out=None) -> dict:
    """Facts only, never code: what the public frontend is built with and what it declares."""
    d = Path(study).expanduser().resolve()
    cap = (_load(d / "02-page-capture.json").get("normalized_result") or {})
    resources = cap.get("resources") or []
    urls = [r.get("url", "") for r in resources] + [s.get("url", "") for s in (cap.get("scripts") or {}).get("items", []) if isinstance(s, dict)]
    stack = collections.OrderedDict()

    def add(cat, name, evidence, version=None, source=None):
        key = (cat, name)
        row = stack.setdefault(key, {"category": cat, "name": name, "version": None, "confidence": None, "evidence": [], "_files": set()})
        if version and not row["version"]:
            row["version"] = version
        if source:
            row["_files"].add(source)
        if evidence not in row["evidence"] and len(row["evidence"]) < 3:
            row["evidence"].append(evidence)

    for name, rx in FRAMEWORK_URLS:
        hit = next((u for u in urls if re.search(rx, u)), None)
        if hit:
            add("framework", name, "resource path " + re.search(rx, hit).group(0))
    for name, rx in HOSTING_FINGERPRINTS:
        if any(re.search(rx, u) for u in urls):
            add("hosting", name, "resource URL pattern")
    files = sorted((d / "scripts-export" / "files").rglob("*.js")) if (d / "scripts-export" / "files").exists() else []
    script_bytes = 0
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        script_bytes += len(text.encode("utf-8", "replace"))
        for cat, name, rx, vrx in SCRIPT_FINGERPRINTS:
            m = re.search(rx, text)
            if not m:
                continue
            ver = None
            if vrx:
                vm = re.search(vrx, text)
                ver = next((g for g in vm.groups() if g), None) if vm else None
            ident = re.sub(r"[^\w./@:-]", "", m.group(0))[:40]
            add(cat, name, f"{f.name[:24]}… identifier {ident}", ver, f.name)
    for row in stack.values():
        files_hit = len(row.pop("_files"))
        row["files"] = files_hit
        strong = row["version"] or row["name"] not in NAME_ONLY or files_hit >= 3
        row["confidence"] = "observed" if strong else "mentioned"
    storage = cap.get("storage") or {}
    keys = list(storage.get("local_storage_keys") or []) + list(storage.get("session_storage_keys") or []) + list(storage.get("indexed_db_names") or [])
    services, unclassified = collections.OrderedDict(), []
    for k in keys:
        svc = next((n for n, rx in STORAGE_FINGERPRINTS if re.search(rx, k, re.I)), None)
        if svc:
            services.setdefault(svc, []).append(k[:40])
        else:
            unclassified.append(k[:40])
    webmcp = (_load(d / "04-webmcp.json").get("normalized_result") or {})
    tools = (webmcp.get("tools") or {}).get("items") or []
    types = collections.Counter(r.get("type", "?") for r in resources)
    target = cap.get("target") or {}
    rec = _load(d / "receipts.json")
    graph = (_load(d / "07-js-graph.json").get("normalized_result") or {})
    static = None
    if graph:
        nodes = (graph.get("graph") or {}).get("nodes") or []
        kinds = collections.Counter(n.get("kind") for n in nodes)
        ep_kinds = collections.Counter(((n.get("observations") or [{}])[0].get("properties") or {}).get("endpoint_kind", "?")
                                       for n in nodes if n.get("kind") == "endpoint")
        st = graph.get("statistics") or {}
        static = {"modules": st.get("modules"), "parsed_files": st.get("parsed_javascript_files"), "findings": st.get("findings"),
                  "endpoint_references": dict(ep_kinds), "storage_references": kinds.get("storage", 0), "workers": kinds.get("worker", 0),
                  "note": "counts only: endpoint and storage names belong to the site and are not listed"}
    out = {"schema": "kosif.web-app-study.v1", "url": target.get("url") or rec.get("url"), "title": target.get("title"),
           "observed_at": (cap.get("capture_window") or {}).get("started_at") or rec.get("started_at"),
           "stack": list(stack.values()),
           "services_from_storage_key_names": [{"service": s, "keys": v[:4]} for s, v in services.items()],
           "unclassified_storage_keys": unclassified[:12],
           "webmcp": {"status": webmcp.get("status"), "tools": [t.get("name") for t in tools if isinstance(t, dict)][:50]},
           "page": {"dom_nodes": (cap.get("dom") or {}).get("total_nodes"), "resources": dict(types),
                    "scripts_exported": len(files), "script_bytes": script_bytes,
                    "network_requests_observed": len((cap.get("network") or {}).get("requests") or []),
                    "websockets_observed": len((cap.get("network") or {}).get("websocket_connections") or [])},
           "static_analysis": static,
           "screenshot_sha256": sha_file(d / "screenshot.png") if (d / "screenshot.png").exists() else None,
           "receipts": rec.get("artifacts", []),
           "boundary": "Facts derived from a logged-out public page; no code, no values of storage keys, no account data. "
                       "Borrow ideas in your own words; never copy the scripts."}
    jp = Path(json_out) if json_out else d / "report.json"
    mp = Path(md_out) if md_out else d / "report.md"
    jp.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(render_md(out), encoding="utf-8")
    return out


def render_md(r: dict) -> str:
    L = [f"# Web app study — {r.get('title') or r.get('url')}", "", f"- URL: {r.get('url')}", f"- Observed: {r.get('observed_at')}",
         f"- Boundary: {r['boundary']}", "", "## Stack (facts with evidence)", "",
         "observed = versioned, a distinctive API identifier, or 3+ files; mentioned = only a bare name in 1–2 files", "",
         "| category | name | version | confidence | evidence |", "|---|---|---|---|---|"]
    for s in r["stack"]:
        L.append(f"| {s['category']} | {s['name']} | {s['version'] or '—'} | {s['confidence']} | {'; '.join(s['evidence'])} |")
    L += ["", "## Services inferred from storage key names (values never read)", ""]
    L += [f"- {x['service']}: {', '.join(x['keys'])}" for x in r["services_from_storage_key_names"]] or ["- none"]
    if r["unclassified_storage_keys"]:
        L.append(f"- unclassified keys: {', '.join(r['unclassified_storage_keys'])}")
    p = r["page"]
    L += ["", "## Page", "", f"- DOM nodes {p['dom_nodes']} · resources {p['resources']} · scripts exported {p['scripts_exported']} ({p['script_bytes']:,} bytes)",
          f"- network requests observed {p['network_requests_observed']} · WebSockets {p['websockets_observed']}",
          f"- WebMCP: {r['webmcp']['status']} · tools: {', '.join(r['webmcp']['tools']) or 'none declared'}"]
    s = r.get("static_analysis")
    if s:
        L += ["", "## Static analysis (REA, bounded, never executed)", "",
              f"- modules {s['modules']} · parsed files {s['parsed_files']} · findings {s['findings']}",
              f"- endpoint references {s['endpoint_references']} · storage references {s['storage_references']} · workers {s['workers']}",
              f"- {s['note']}"]
    L += ["", "## Receipts", ""]
    L += [f"- {a['file']} · {a['bytes']:,} B · `{a['sha256'][:16]}…`" for a in r["receipts"]] or ["- none"]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- CLI
def doctor() -> dict:
    return {"rea": find_rea(), "chromium": find_chromium(), "ready": bool(find_rea() and find_chromium()),
            "install": "npm install -g rea-agents; any Chromium, Chrome or Edge (or Playwright's Chromium)"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    r = sub.add_parser("run", help="study one public page (isolated, logged out)")
    r.add_argument("url")
    r.add_argument("--out", required=True, help="new folder OUTSIDE any git checkout")
    r.add_argument("--allow", action="append", default=[], help="extra exact origin the page may load from")
    r.add_argument("--observation-ms", type=int, default=3000)
    r.add_argument("--chromium")
    r.add_argument("--proxy", default="auto", help="auto (HTTPS_PROXY), none, or a proxy URL")
    r.add_argument("--port", type=int, default=9223)
    r.add_argument("--deep", action="store_true", help="also run REA's bounded static JavaScript analysis (slow, memory-hungry)")
    r.add_argument("--keep-profile", action="store_true")
    r.add_argument("--dry-run", action="store_true", help="print the plan without starting anything")
    p = sub.add_parser("report", help="facts-only report from a study folder")
    p.add_argument("study")
    p.add_argument("--json")
    p.add_argument("--md")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "doctor":
            res = doctor()
        elif a.cmd == "run":
            res = run(a.url, a.out, a.allow, a.observation_ms, a.chromium, a.proxy, a.port, a.deep, a.keep_profile, a.dry_run)
        else:
            rep = report(a.study, a.json, a.md)
            res = {"stack": [f"{s['name']}{' ' + s['version'] if s['version'] else ''}" for s in rep["stack"]],
                   "services": [x["service"] for x in rep["services_from_storage_key_names"]], "webmcp_tools": len(rep["webmcp"]["tools"])}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError) as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
