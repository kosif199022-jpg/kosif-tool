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
    # (category, name, detect regex, version regex or None, strong regex or None)
    # "strong" = an identifier only the library itself ships; without it, a bare name in 1-2 files is graded "mentioned"
    ("framework", "React", r"rendererPackageName:\s*\"react-dom\"|__REACT_DEVTOOLS_GLOBAL_HOOK__",
     r"version:\s*\"(\d+\.\d+\.\d+[\w.-]*)\",\s*rendererPackageName:\s*\"react-dom\"|rendererPackageName:\s*\"react-dom\"[^}]{0,120}?version:\s*\"(\d+\.\d+\.\d+[\w.-]*)\"", None),
    ("framework", "Next.js", r"__NEXT_DATA__|next/dist/|__next_f", r"window\.next\s*=\s*\{\s*version:\s*\"(\d+\.\d+\.\d+[\w.-]*)\"", None),
    ("framework", "Vue", r"__VUE__|__VUE_HMR_RUNTIME__", None, None),
    ("framework", "Svelte", r"__svelte|svelte-[a-z0-9]{6}", None, None),
    ("framework", "Angular", r"(?<![\w-])ng-version(?![\w-])|ɵcmp", None, None),
    ("bundler", "webpack", r"webpackChunk[\w$]*|__webpack_require__", None, None),
    ("canvas-engine", "tldraw", r"\btldraw\b|@tldraw/", r"\(\s*\"tldraw\"\s*,\s*\"(\d+\.\d+\.\d+[\w.-]*)\"", r"@tldraw/editor|TLDRAW_ENV"),
    ("canvas-engine", "Excalidraw", r"@excalidraw/excalidraw|ExcalidrawElement|excalidraw-app", None, None),   # not the 'excalidraw/clipboard' paste type
    ("canvas-engine", "Konva", r"\bKonva\b", None, None),
    ("canvas-engine", "Fabric.js", r"\bfabric\.(?:Canvas|Object)\b", None, None),
    ("canvas-engine", "PixiJS", r"\bPIXI\b|pixi\.js", None, None),
    ("canvas-engine", "three.js", r"__THREE__|THREE\.WebGLRenderer", r"REVISION\s*=\s*\"(\d+)\"", None),
    ("canvas-engine", "React Flow", r"react-flow__|@xyflow/", None, None),
    ("realtime", "Yjs", r"(?<![\w])(?:yjs|y-protocols)(?![\w])|\bY\.Doc\b", None, None),   # 'linkifyjs' is not Yjs
    ("realtime", "Liveblocks", r"liveblocks", None, None),
    ("realtime", "Socket.IO", r"socket\.io", None, r"\"/engine\.io\"|/engine\.io"),
    ("realtime", "PartyKit", r"partykit|partysocket", None, None),
    ("editor", "Monaco", r"monaco-editor|\bmonaco\.editor\b", None, None),
    ("editor", "CodeMirror", r"\bcm-editor\b|@codemirror/", None, None),
    ("editor", "Tiptap", r"\btiptap\b", None, r"\[tiptap (?:error|warn)\]|tipTapConfig"),
    ("editor", "ProseMirror", r"ProseMirror", None, None),
    ("editor", "highlight.js", r"\bhljs\b.{0,200}registerLanguage|registerLanguage.{0,200}\bhljs\b", None, None),
    ("editor", "Prism", r"\bPrism\.highlight|highlightAllUnder", None, None),
    ("styling", "Tailwind CSS", r"--tw-[a-z-]+", None, None),
    ("styling", "Radix UI", r"data-radix-|@radix-ui/", None, None),
    ("styling", "shadcn/ui (data-slot)", r"data-slot[=\"']+(?:sidebar|card|tooltip|dialog|button)", None, None),
    ("styling", "Framer Motion", r"framer-motion|\bMotionConfig\b|framerAppearId", None, None),
    ("styling", "lucide icons", r"\"lucide-\"|lucide-react", None, None),
    ("styling", "sonner toasts", r"data-sonner-toaster", None, None),
    ("state", "Zustand", r"\bzustand\b", None, None),
    ("state", "TanStack Query", r"@tanstack/(?:[a-z]+-)?query|QueryClientProvider", None, None),
    ("library", "Zod", r"\$ZodType|ZodError", r"\{major:(\d+),minor:(\d+),patch:(\d+)\}", None),
    ("platform", "Firebase SDK", r"firebaseapp\.com|identitytoolkit\.googleapis\.com|firebase-installations",
     r"\(\s*\"firebase\"\s*,\s*\"(\d+\.\d+\.\d+)\"\s*,\s*\"app\"", None),
    ("auth", "Clerk", r"\bclerk\.[a-z]+\.(?:com|dev)|__clerk", None, None),
    ("auth", "Supabase", r"supabase\.co\b|@supabase/", None, None),
    ("auth", "Google Identity Services", r"accounts\.google\.com/gsi/client", None, None),
    ("auth", "reCAPTCHA", r"recaptcha/api\.js|grecaptcha\.", None, None),
    ("analytics", "Mixpanel", r"mixpanel", r"LIB_VERSION:\s*\"(\d+\.\d+\.\d+)\"", r"api-js\.mixpanel\.com|LIB_VERSION"),
    ("analytics", "PostHog", r"posthog", None, None),
    ("analytics", "Sentry", r"sentry\.io|__SENTRY__", None, r"__SENTRY__|Sentry\.init"),
    ("analytics", "Google Tag Manager", r"googletagmanager\.com/gtm\.js", None, None),
    ("analytics", "Hotjar", r"static\.hotjar\.com", None, None),
    ("analytics", "Vercel Analytics", r"/_vercel/insights|va\.vercel-scripts\.com", r"sdkv\s*=\s*\"(\d+\.\d+\.\d+)\"", None),
    ("support", "Intercom", r"widget\.intercom\.io|_intercom_npm_loader", None, None),
    ("payments", "Stripe", r"js\.stripe\.com", None, r"\bStripe\(\s*[\"']pk_"),
    ("ai", "Vercel AI SDK", r"\bai/rsc\b|@ai-sdk/|vercel\.ai\.error", None, None),
]
# matched only by a bare package/product name, which can appear without the library being used
# (an import adapter, a paste handler, a comment): graded "mentioned" unless versioned, strong or seen in 3+ files
NAME_ONLY = {"tldraw", "Excalidraw", "Konva", "PixiJS", "Yjs", "Liveblocks", "Socket.IO", "PartyKit", "Monaco", "Tiptap",
             "Zustand", "Mixpanel", "PostHog", "Svelte", "ProseMirror", "Sentry", "Stripe"}
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
    """WHATWG-style origin (scheme://host[:port]); IDN hosts in punycode, IPv6 in brackets. Credentials are refused."""
    u = urllib.parse.urlsplit(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError("only http(s) URLs with a host can be studied")
    if u.username or u.password:
        raise ValueError("credentials in the URL are a login; the study is always logged out")
    host = u.hostname
    if ":" in host:
        host = f"[{host}]"
    else:
        try:
            host = host.encode("idna").decode("ascii")
        except UnicodeError:
            raise ValueError("invalid host name") from None
        if not re.fullmatch(r"[a-z0-9.-]+", host):   # nothing a shell could reinterpret
            raise ValueError("invalid host name")
    default = {"http": 80, "https": 443}[u.scheme]
    port = f":{u.port}" if u.port and u.port != default else ""
    return f"{u.scheme}://{host}{port}"


def safe_url(url: str) -> str:
    """For receipts and reports: no userinfo, query values redacted (they can carry tokens)."""
    u = urllib.parse.urlsplit(url)
    host = u.hostname or ""
    netloc = (f"[{host}]" if ":" in host else host) + (f":{u.port}" if u.port else "")
    query = "&".join(f"{k}=…" for k, _ in urllib.parse.parse_qsl(u.query, keep_blank_values=True))
    return urllib.parse.urlunsplit((u.scheme, netloc, u.path, query, ""))


def inside_git(path: Path) -> bool:
    return any((p / ".git").exists() for p in [path, *path.parents])


def check_out_dir(out: Path) -> Path:
    out = out.expanduser().resolve()
    if inside_git(out):
        raise ValueError("the study folder holds third-party code: put it outside any git checkout")
    if out.exists() and not out.is_dir():
        raise ValueError("--out exists and is not a folder")
    if out.exists() and any(out.iterdir()):
        raise ValueError("the study folder must be new or empty")
    return out


def rea_argv() -> list | None:
    """REA without any shell: on Windows `node …/rea.mjs` instead of the rea.cmd shim (shared with rea_bridge)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from rea_bridge import rea_launcher
    return rea_launcher()


def find_rea() -> str | None:
    launcher = rea_argv()
    return " ".join(launcher) if launcher else None


def find_chromium(explicit: str | None = None) -> str | None:
    cands = [explicit, os.environ.get("KOSIF_CHROMIUM")]
    cands += [shutil.which(n) for n in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome", "msedge")]
    cands += sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"), reverse=True)
    cands += sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome")), reverse=True)
    cands += [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    return next((c for c in cands if c and Path(c).exists()), None)


def free_port() -> int:
    import socket
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def port_in_use(port: int) -> bool:
    """True when something already listens on 127.0.0.1:port — maybe someone's signed-in browser: never attach to it."""
    import socket
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def proxy_arg(proxy: str) -> list:
    if proxy == "none":
        return []
    if proxy == "auto":
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if not proxy:
        return []
    u = urllib.parse.urlsplit(proxy if "://" in proxy else "http://" + proxy)
    if u.username or u.password:
        raise ValueError("a proxy with credentials is not passed to the browser (it would show in the process list); use a local credential-less proxy")
    args = [f"--proxy-server={u.scheme}://{u.hostname}{':' + str(u.port) if u.port else ''}"]
    bypass = os.environ.get("NO_PROXY") or os.environ.get("no_proxy")
    if bypass:
        args.append("--proxy-bypass-list=" + ";".join(x.strip() for x in bypass.split(",") if x.strip()))
    return args


def browser_argv(chrome: str, url: str, profile: Path, proxy: str) -> list:
    # --remote-debugging-port=0: the browser picks a free port and writes it to <profile>/DevToolsActivePort,
    # so the study can prove it talks to the browser it started, never to someone else's
    argv = [chrome, "--headless=new", "--remote-debugging-address=127.0.0.1", "--remote-debugging-port=0",
            f"--user-data-dir={profile}", f"--disk-cache-dir={profile / 'cache'}", f"--crash-dumps-dir={profile / 'crash'}",
            "--disable-crash-reporter", "--disable-breakpad", "--no-first-run", "--no-default-browser-check", "--disable-extensions",
            "--disable-sync", "--disable-background-networking", "--disable-component-update", "--disable-default-apps",
            "--disable-domain-reliability", "--no-pings", "--window-size=1440,900", *proxy_arg(proxy)]
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


REQUIRED_STEPS = ("list-browser-targets", "inspect-web-page", "capture-web-screenshot", "export-web-scripts")


def _spawn_kwargs() -> dict:
    if os.name == "nt":
        return {"creationflags": getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)}
    kw = {"start_new_session": True}
    if platform.system() == "Linux":
        def _die_with_parent():   # the browser dies if this study process is killed outright
            try:
                import ctypes
                ctypes.CDLL("libc.so.6", use_errno=True).prctl(1, signal.SIGKILL)   # PR_SET_PDEATHSIG
            except Exception:  # noqa: BLE001
                pass
        kw["preexec_fn"] = _die_with_parent
    return kw


def _kill_tree(proc: subprocess.Popen) -> None:
    if proc.poll() is not None and os.name == "nt":
        return
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, timeout=30)
        else:
            try:
                os.killpg(proc.pid, signal.SIGTERM)
                proc.wait(timeout=10)
            except (subprocess.TimeoutExpired, ProcessLookupError):
                pass
            try:
                os.killpg(proc.pid, signal.SIGKILL)   # the whole group: GPU, network and crashpad children too
            except ProcessLookupError:
                pass
        proc.wait(timeout=10)
    except Exception:  # noqa: BLE001
        proc.kill()


def run_rea(rea: str, args: list, dest: Path, timeout: int) -> dict:
    import tempfile
    t0 = time.time()
    with open(dest, "wb") as fh, tempfile.TemporaryFile() as err:
        p = subprocess.Popen([*rea, *args, "--format", "json"], stdout=fh, stderr=err, **_spawn_kwargs())
        try:
            rc = p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            _kill_tree(p)
            rc = -1
        err.seek(0)
        tail = err.read()[-400:].decode("utf-8", "replace")
    rec = {"command": args[0], "rc": rc, "seconds": round(time.time() - t0, 1)}
    if rc:
        body = _load(dest)
        rec.update(code=body.get("code") or ("timeout" if rc == -1 else "failed"), message=str(body.get("message") or tail)[:300])
    return rec


def _wait_for_devtools(proc, profile: Path, timeout: float = 30) -> str:
    """Endpoint of THIS browser: read DevToolsActivePort from its fresh profile and match the browser id."""
    marker = profile / "DevToolsActivePort"
    deadline = time.time() + timeout
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError("the study browser exited before opening DevTools (see browser.log)")
        if marker.exists():
            lines = marker.read_text(encoding="utf-8", errors="replace").split()
            if len(lines) >= 2 and lines[0].isdigit():
                endpoint = f"http://127.0.0.1:{lines[0]}"
                try:
                    ver = json.loads(opener.open(endpoint + "/json/version", timeout=2).read())
                except (OSError, ValueError):
                    time.sleep(0.3)
                    continue
                if str(ver.get("webSocketDebuggerUrl", "")).endswith(lines[1]):
                    return endpoint
                raise RuntimeError("the DevTools port answers for another browser; refusing to attach")
        time.sleep(0.3)
    raise RuntimeError("the study browser did not open DevTools in time")


# --------------------------------------------------------------------------- run
def run(url: str, out: str, allow=(), obs_ms: int = 3000, chromium: str | None = None, proxy: str = "auto", port: int = 0,
        deep: bool = False, keep_profile: bool = False, dry_run: bool = False, settle_s: float = 6.0) -> dict:
    origin = origin_of(url)
    origins = sorted({origin, *(origin_of(a) for a in allow)})
    out_p = check_out_dir(Path(out))
    if port:
        raise ValueError("--port is not used any more: the study browser picks a free port and is verified by its profile")
    rea, chrome = rea_argv(), find_chromium(chromium)
    profile = out_p / "isolated-profile"
    argv = browser_argv(chrome or "<chromium>", url, profile, proxy)
    plan = {"url": safe_url(url), "origins": origins, "out": str(out_p), "browser": argv,
            "rea_steps": [["list-browser-targets", "<endpoint>", *[x for o in origins for x in ("--allowed-origins", o)]]]
                         + [a for _, a in rea_steps("<endpoint>", "<target>", origins, out_p, obs_ms, deep)],
            "profile": "fresh, deleted after the run" if not keep_profile else "fresh, kept", "login": "never"}
    if dry_run:
        return {"dry_run": True, "plan": plan}
    if not rea:
        raise RuntimeError("REA not found (or only a .cmd shim without node): npm install -g rea-agents (https://github.com/morluto/rea)")
    if not chrome:
        raise RuntimeError("no Chromium/Chrome/Edge found; pass --chromium PATH")
    out_p.mkdir(parents=True, exist_ok=True)
    started = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    steps, error = [], None
    previous = {}

    def _stop(signum, _frame):
        raise SystemExit(128 + signum)

    for name in ("SIGTERM", "SIGHUP", "SIGBREAK"):   # a terminated study still closes its browser and deletes the profile
        sig = getattr(signal, name, None)
        if sig is not None:
            try:
                previous[sig] = signal.signal(sig, _stop)
            except (ValueError, OSError):
                pass
    log = open(out_p / "browser.log", "wb")
    proc = subprocess.Popen(argv, stdout=log, stderr=subprocess.STDOUT, **_spawn_kwargs())
    try:
        endpoint = _wait_for_devtools(proc, profile)
        time.sleep(settle_s)
        allow_args = [x for o in origins for x in ("--allowed-origins", o)]
        steps.append(run_rea(rea, ["list-browser-targets", endpoint, *allow_args], out_p / "01-targets.json", 120))
        targets = (_load(out_p / "01-targets.json").get("normalized_result") or {}).get("targets") or []
        target = next((t.get("target_id") for t in targets if isinstance(t, dict) and t.get("type") == "page" and t.get("origin") in origins), None)
        if not target:
            raise RuntimeError("no page target on the allowed origins (redirected elsewhere?)")
        for name, args in rea_steps(endpoint, target, origins, out_p, obs_ms, deep):
            steps.append(run_rea(rea, [a.replace("<endpoint>", endpoint) for a in args], out_p / name, 1800 if name.startswith("07") else 600))
    except RuntimeError as e:
        error = str(e)
    finally:
        _kill_tree(proc)
        log.close()
        if not keep_profile:
            for _ in range(10):
                shutil.rmtree(profile, ignore_errors=True)
                if not profile.exists():
                    break
                time.sleep(0.5)
        for sig, handler in previous.items():
            try:
                signal.signal(sig, handler)
            except (ValueError, OSError):
                pass
    shot = _load(out_p / "05-screenshot.json")
    art = (shot.get("normalized_result") or {}).get("artifact") or {}
    if isinstance(art, dict) and art.get("data_base64"):
        png = base64.b64decode(art["data_base64"])
        if hashlib.sha256(png).hexdigest() == art.get("sha256"):
            (out_p / "screenshot.png").write_bytes(png)
    ok = {s["command"]: s["rc"] == 0 for s in steps}
    complete = error is None and all(ok.get(c) for c in REQUIRED_STEPS)
    browser = ((_load(out_p / "01-targets.json").get("normalized_result") or {}).get("browser") or {}).get("product") or "unknown"
    receipts = {"tool": f"web_app_study.py {VERSION}", "rea": _version([*rea, "--version"]), "browser": browser,
                "url": safe_url(url), "origins": origins, "started_at": started, "complete": complete, "error": error,
                "profile_deleted": not profile.exists(), "login": False, "steps": steps, "artifacts": _artifact_receipts(out_p)}
    (out_p / "receipts.json").write_text(json.dumps(receipts, indent=2) + "\n", encoding="utf-8")
    rep = report(out_p)
    return {"out": str(out_p), "complete": complete, "error": error, "profile_deleted": receipts["profile_deleted"],
            "steps": steps, "report": str(out_p / "report.md"), "facts": len(rep["stack"])}


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
        data = json.loads(Path(p).read_text(encoding="utf-8")) if Path(p).exists() and Path(p).stat().st_size else {}
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def page_text(s, cap: int = 120) -> str:
    """Text the page controls (title, tool and key names): no control characters or newlines, no table or code breakers, capped."""
    s = re.sub(r"[\x00-\x1f\x7f]", " ", str(s or ""))
    s = re.sub(r"\s+", " ", s).replace("|", "¦").replace("`", "'").strip()
    return s[:cap] + ("…" if len(s) > cap else "")


def redact_key(k: str) -> str:
    """Storage key names can embed site or visitor ids: mask any run of 12+ hex/base62 characters."""
    return re.sub(r"[A-Za-z0-9]{12,}", lambda m: m.group(0)[:3] + "…" if not m.group(0).isalpha() or len(m.group(0)) > 24 else m.group(0), k)[:40]


def report(study, json_out=None, md_out=None) -> dict:
    """Facts only, never code: what the public frontend is built with and what it declares."""
    d = Path(study).expanduser().resolve()
    if not d.is_dir():
        raise ValueError(f"no study folder at {d}")
    D = lambda x: x if isinstance(x, dict) else {}   # noqa: E731  (odd or partial artifacts never crash the report)
    L = lambda x: [i for i in x if isinstance(i, dict)] if isinstance(x, list) else []   # noqa: E731
    cap = D(_load(d / "02-page-capture.json").get("normalized_result"))
    resources = L(cap.get("resources"))
    urls = [str(r.get("url", "")) for r in resources] + [str(s.get("url", "")) for s in L(D(cap.get("scripts")).get("items"))]
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
        for cat, name, rx, vrx, srx in SCRIPT_FINGERPRINTS:
            m = re.search(rx, text)
            if not m:
                continue
            ver = None
            if vrx:
                vm = re.search(vrx, text)
                if vm:
                    groups = [g for g in vm.groups() if g]
                    ver = ".".join(groups) if len(groups) > 1 and all(g.isdigit() for g in groups) else (groups[0] if groups else None)
            ident = re.sub(r"[^\w./@:-]", "", m.group(0))[:40]
            add(cat, name, f"{f.name[:24]}… identifier {ident}", ver, f.name)
            if srx and re.search(srx, text):
                stack[(cat, name)]["_strong"] = True
    for row in stack.values():
        files_hit = len(row.pop("_files"))
        row["files"] = files_hit
        strong = row.pop("_strong", False) or row["version"] or row["name"] not in NAME_ONLY or files_hit >= 3
        row["confidence"] = "observed" if strong else "mentioned"
    storage = D(cap.get("storage"))
    keys = [str(k) for f in ("local_storage_keys", "session_storage_keys", "indexed_db_names") for k in (storage.get(f) or []) if isinstance(storage.get(f), list)]
    services, unclassified = collections.OrderedDict(), []
    for k in keys:
        svc = next((n for n, rx in STORAGE_FINGERPRINTS if re.search(rx, k, re.I)), None)
        if svc:
            services.setdefault(svc, []).append(page_text(redact_key(k), 40))
        else:
            unclassified.append(page_text(redact_key(k), 40))
    rec = _load(d / "receipts.json")
    failed = {s.get("command"): s.get("code") or "failed" for s in L(rec.get("steps")) if s.get("rc")}
    webmcp = D(_load(d / "04-webmcp.json").get("normalized_result"))
    if "discover-webmcp-tools" in failed:
        webmcp = {"status": f"step failed: {failed['discover-webmcp-tools']}"}
    tools = L(D(webmcp.get("tools")).get("items"))
    types = collections.Counter(str(r.get("type", "?")) for r in resources)
    target = D(cap.get("target"))
    graph = D(_load(d / "07-js-graph.json").get("normalized_result"))
    static = None
    if graph:
        nodes = L(D(graph.get("graph")).get("nodes"))
        kinds = collections.Counter(n.get("kind") for n in nodes)
        ep_kinds = collections.Counter(D(D((L(n.get("observations")) or [{}])[0]).get("properties")).get("endpoint_kind", "?")
                                       for n in nodes if n.get("kind") == "endpoint")
        st = D(graph.get("statistics"))
        static = {"modules": st.get("modules"), "parsed_files": st.get("parsed_javascript_files"), "findings": st.get("findings"),
                  "endpoint_references": dict(ep_kinds), "storage_references": kinds.get("storage", 0), "workers": kinds.get("worker", 0),
                  "note": "counts only: endpoint and storage names belong to the site and are not listed"}
    out = {"schema": "kosif.web-app-study.v1", "url": safe_url(str(target.get("url") or rec.get("url") or "")) if (target.get("url") or rec.get("url")) else None,
           "title": page_text(target.get("title")) if target.get("title") else None,
           "page_supplied_fields": ["title", "webmcp.tools", "storage key names"], "complete": rec.get("complete"), "failed_steps": failed,
           "observed_at": (cap.get("capture_window") or {}).get("started_at") or rec.get("started_at"),
           "stack": list(stack.values()),
           "services_from_storage_key_names": [{"service": s, "keys": v[:4]} for s, v in services.items()],
           "unclassified_storage_keys": unclassified[:12],
           "webmcp": {"status": webmcp.get("status") or "not run", "checked": webmcp.get("status") == "available",
                      "tools": [page_text(t.get("name"), 64) for t in tools][:50]},
           "page": {"dom_nodes": (cap.get("dom") or {}).get("total_nodes"), "resources": dict(types),
                    "scripts_exported": len(files), "script_bytes": script_bytes,
                    "network_requests_observed": len((cap.get("network") or {}).get("requests") or []),
                    "websockets_observed": len((cap.get("network") or {}).get("websocket_connections") or [])},
           "static_analysis": static,
           "screenshot_sha256": sha_file(d / "screenshot.png") if (d / "screenshot.png").exists() else None,
           "receipts": L(rec.get("artifacts")),
           "boundary": "Facts derived from a logged-out public page; no code, no values of storage keys, no account data. "
                       "Borrow ideas in your own words; never copy the scripts."}
    jp = Path(json_out) if json_out else d / "report.json"
    mp = Path(md_out) if md_out else d / "report.md"
    jp.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(render_md(out), encoding="utf-8")
    return out


def render_md(r: dict) -> str:
    L = [f"# Web app study — {r.get('title') or r.get('url')}", "", f"- URL: {r.get('url')}", f"- Observed: {r.get('observed_at')}",
         f"- Boundary: {r['boundary']}"]
    if r.get("complete") is False or r.get("failed_steps"):
        L.append(f"- **Incomplete study:** failed steps {r.get('failed_steps') or '—'}; what those steps would show is unknown, not absent")
    L += ["", "## Stack (facts with evidence)", "",
         "observed = versioned, a distinctive identifier the library itself ships, or 3+ files; mentioned = only a bare name in 1–2 files", "",
         "| category | name | version | confidence | evidence |", "|---|---|---|---|---|"]
    for s in r["stack"]:
        L.append(f"| {s['category']} | {s['name']} | {s['version'] or '—'} | {s['confidence']} | {'; '.join(s['evidence'])} |")
    L += ["", "## Services inferred from storage key names (values never read)", ""]
    L += [f"- {x['service']}: {', '.join(x['keys'])}" for x in r["services_from_storage_key_names"]] or ["- none"]
    if r["unclassified_storage_keys"]:
        L.append(f"- unclassified keys: {', '.join(r['unclassified_storage_keys'])}")
    p = r["page"]
    L += ["", "## Page", "", f"- DOM nodes {p['dom_nodes']} · resources {p['resources']} · scripts exported {p['scripts_exported']} ({p['script_bytes']:,} bytes)",
          f"- network requests observed {p['network_requests_observed']} · WebSockets {p['websockets_observed']} (observation starts after the page loaded: absence is not evidence)",
          ("- WebMCP: " + (f"tools: {', '.join(r['webmcp']['tools']) or 'none declared'}" if r["webmcp"]["checked"]
                           else f"not checked ({r['webmcp']['status']}) — unknown, not zero"))]
    s = r.get("static_analysis")
    if s:
        L += ["", "## Static analysis (REA, bounded, never executed)", "",
              f"- modules {s['modules']} · parsed files {s['parsed_files']} · findings {s['findings']}",
              f"- endpoint references {s['endpoint_references']} · storage references {s['storage_references']} · workers {s['workers']}",
              f"- {s['note']}"]
    L += ["", "## Receipts", ""]
    L += [f"- {a.get('file')} · {a.get('bytes', 0):,} B · `{str(a.get('sha256', ''))[:16]}…`" for a in r["receipts"]] or ["- none"]
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
            res = run(a.url, a.out, a.allow, a.observation_ms, a.chromium, a.proxy, 0, a.deep, a.keep_profile, a.dry_run)
            if not a.dry_run and not (res.get("complete") and res.get("profile_deleted", True)):
                print(json.dumps(res, ensure_ascii=False, indent=2))
                return 2   # incomplete study or a profile that could not be deleted
        else:
            rep = report(a.study, a.json, a.md)
            res = {"stack": [f"{s['name']}{' ' + s['version'] if s['version'] else ''}" for s in rep["stack"]],
                   "services": [x["service"] for x in rep["services_from_storage_key_names"]], "webmcp_tools": len(rep["webmcp"]["tools"])}
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError, OSError) as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
