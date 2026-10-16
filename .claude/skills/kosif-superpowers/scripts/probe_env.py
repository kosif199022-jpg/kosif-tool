#!/usr/bin/env python3
"""Probe what this machine can really do / افحص قدرات هذا الجهاز.

Prints a capability card: host type, CPU/RAM/disk/GPU, runtimes, CLI tools,
Python and Node packages, fonts (Arabic readiness), browsers, network reach
through the environment proxy, and which power families each finding unlocks.

Python 3.8+ standard library only. Read-only: it writes only inside a temp dir
(and the --write file when asked). Bounded: about 20 s in total, each check has
its own timeout of 3 s or less. It prints environment variable NAMES only, never
their values, and it never disables TLS verification.

  python3 probe_env.py                  # Markdown capability card
  python3 probe_env.py --json           # machine-readable capabilities
  python3 probe_env.py --no-network     # skip network checks (offline / CI)
  python3 probe_env.py --install-test   # also time a real venv+pip and npm install (slower)
  python3 probe_env.py --write ../references/environment.md   # dated snapshot file

Exit code is always 0; checks that run out of time are listed under timed_out.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import platform
import re
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
T0 = time.monotonic()
BUDGET = [18.0]  # seconds; list so --budget can change it

BADGE = {"ready": "🟢", "install": "📦", "key": "🔑", "missing": "❌", "unknown": "❔"}

# --------------------------------------------------------------------------- helpers


def left() -> float:
    return BUDGET[0] - (time.monotonic() - T0)


def run(cmd, timeout: float = 2.0):
    """Run a command; return (rc, text) or (None, reason). Never raises."""
    timeout = max(0.3, min(timeout, left() - 0.3))
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                           timeout=timeout, universal_newlines=True, errors="replace")
        return p.returncode, p.stdout or ""
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except (OSError, ValueError) as e:
        return None, type(e).__name__


def parallel(tasks: dict, timeout: float):
    """Run callables in daemon threads; return (results, timed_out names)."""
    results = {}

    def wrap(k, fn):
        try:
            results[k] = fn()
        except Exception as e:  # a probe must never crash the card
            results[k] = {"error": "%s: %s" % (type(e).__name__, e)}

    threads = [threading.Thread(target=wrap, args=(k, fn), daemon=True) for k, fn in tasks.items()]
    for t in threads:
        t.start()
    end = time.monotonic() + max(0.1, timeout)
    for t in threads:
        t.join(max(0.0, end - time.monotonic()))
    return results, [k for k in tasks if k not in results]


def ver(text: str) -> str:
    m = re.search(r"(\d+\.\d+(?:\.\d+)*(?:[a-z]\d*)?)", text or "")
    return m.group(1) if m else ""


def gib(n) -> float:
    return round((n or 0) / 1024 ** 3, 1)


# --------------------------------------------------------------------------- inventory tables

BINS = {
    "video": ["ffmpeg", "ffprobe", "yt-dlp", "mkvmerge", "HandBrakeCLI", "mpv"],
    "image": ["convert", "magick", "identify", "inkscape", "gimp", "rsvg-convert", "cwebp", "exiftool",
              "potrace", "optipng", "tesseract"],
    "audio": ["sox", "lame", "flac", "espeak-ng", "piper"],
    "docs": ["soffice", "libreoffice", "pandoc", "pdftotext", "pdftoppm", "qpdf", "gs", "pdflatex", "xelatex",
             "lualatex", "tectonic", "wkhtmltopdf"],
    "diagrams": ["dot", "mmdc", "plantuml", "d2"],
    "browser": ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "firefox", "playwright"],
    "data": ["sqlite3", "duckdb", "psql", "mysql", "redis-server", "redis-cli", "jq", "yq", "mongosh"],
    "dev": ["git", "gh", "rg", "fd", "make", "cmake", "gcc", "g++", "clang", "go", "rustc", "cargo", "java",
            "ruby", "php", "perl", "node", "npm", "npx", "pnpm", "yarn", "bun", "deno", "uv", "pip", "pip3",
            "pipx", "conda", "docker", "podman", "R", "julia", "dotnet"],
    "3d": ["blender", "openscad"],
    "cloud": ["gcloud", "gsutil", "bq", "aws", "az", "kubectl", "terraform", "wrangler", "vercel", "netlify",
              "flyctl", "firebase"],
    "pkg": ["apt-get", "brew", "winget", "choco", "dnf", "apk", "pacman"],
    "ml": ["nvidia-smi", "ollama"],
    "misc": ["zip", "unzip", "7z", "curl", "wget", "fc-list", "sudo"],
}

# name -> version command (run in parallel, 2-3 s each)
VERSION_CMDS = {
    "node": ["node", "-v"], "npm": ["npm", "-v"], "ffmpeg": ["ffmpeg", "-hide_banner", "-version"],
    "git": ["git", "--version"], "gh": ["gh", "--version"], "docker": ["docker", "--version"],
    "pandoc": ["pandoc", "--version"], "soffice": ["soffice", "--version"], "convert": ["convert", "-version"],
    "magick": ["magick", "-version"], "go": ["go", "version"], "rustc": ["rustc", "--version"],
    "java": ["java", "-version"], "uv": ["uv", "--version"], "tesseract": ["tesseract", "--version"],
    "gcc": ["gcc", "--version"], "bun": ["bun", "--version"], "deno": ["deno", "--version"],
    "yt-dlp": ["yt-dlp", "--version"], "blender": ["blender", "--version"], "dot": ["dot", "-V"],
    "sox": ["sox", "--version"], "playwright": ["playwright", "--version"], "jq": ["jq", "--version"],
    "psql": ["psql", "--version"], "pip": [sys.executable, "-m", "pip", "--version"],
}

PY_NOTABLE = [
    "numpy", "pandas", "polars", "pyarrow", "duckdb", "scipy", "scikit-learn", "statsmodels", "sympy",
    "matplotlib", "plotly", "seaborn", "altair", "networkx", "pillow", "opencv-python", "opencv-python-headless",
    "imageio", "imageio-ffmpeg", "moviepy", "librosa", "soundfile", "pydub", "faster-whisper", "openai-whisper",
    "torch", "transformers", "onnxruntime", "requests", "httpx", "aiohttp", "beautifulsoup4", "lxml",
    "playwright", "selenium", "openpyxl", "xlsxwriter", "python-docx", "python-pptx", "reportlab", "pypdf",
    "pypdfium2", "pdfplumber", "pymupdf", "weasyprint", "markdown", "jinja2", "arabic-reshaper", "python-bidi",
    "fonttools", "manim", "graphviz", "jupyter", "streamlit", "fastapi", "flask", "anthropic", "openai",
    "yt-dlp", "pytest",
]

ARABIC_GOOD_FONTS = ("noto naskh", "noto kufi", "noto sans arabic", "amiri", "cairo", "tajawal", "kacst",
                     "scheherazade", "vazirmatn", "ibm plex sans arabic", "reem kufi", "lateef", "harmattan",
                     "aref ruqaa", "lalezar", "almarai", "el messiri", "markazi", "changa", "noto nastaliq")

# service credentials: env NAME -> (service, families). Values are never read.
KEY_NAMES = {
    "ANTHROPIC_API_KEY": ("Claude API", ["AGENT", "GEN"]),
    "OPENAI_API_KEY": ("OpenAI API", ["GEN", "MEDIA"]),
    "GEMINI_API_KEY": ("Google Gemini API", ["GEN"]),
    "GOOGLE_API_KEY": ("Google API", ["GEN", "MAP"]),
    "HF_TOKEN": ("Hugging Face", ["GEN", "MEDIA"]),
    "HUGGINGFACE_HUB_TOKEN": ("Hugging Face", ["GEN", "MEDIA"]),
    "REPLICATE_API_TOKEN": ("Replicate", ["GEN", "MEDIA"]),
    "ELEVENLABS_API_KEY": ("ElevenLabs voice", ["VOICE", "MEDIA"]),
    "FAL_KEY": ("fal.ai generation", ["GEN"]),
    "STABILITY_API_KEY": ("Stability AI", ["GEN"]),
    "RUNWAYML_API_SECRET": ("Runway video", ["GEN"]),
    "DEEPGRAM_API_KEY": ("Deepgram speech-to-text", ["SYNC", "MEDIA"]),
    "ASSEMBLYAI_API_KEY": ("AssemblyAI speech-to-text", ["SYNC", "MEDIA"]),
    "PEXELS_API_KEY": ("Pexels stock media", ["FOOT", "MEDIA"]),
    "UNSPLASH_ACCESS_KEY": ("Unsplash stock photos", ["FOOT", "MEDIA"]),
    "PIXABAY_API_KEY": ("Pixabay stock media", ["FOOT", "MEDIA"]),
    "MAPBOX_ACCESS_TOKEN": ("Mapbox maps", ["MAP"]),
    "GH_TOKEN": ("GitHub", ["CODE", "AGENT"]),
    "GITHUB_TOKEN": ("GitHub", ["CODE", "AGENT"]),
    "AWS_ACCESS_KEY_ID": ("AWS", ["CODE", "APP"]),
    "CLOUDSDK_AUTH_ACCESS_TOKEN": ("Google Cloud", ["CODE", "ANLY"]),
    "GOOGLE_APPLICATION_CREDENTIALS": ("Google Cloud", ["CODE", "ANLY"]),
    "AZURE_OPENAI_API_KEY": ("Azure OpenAI", ["GEN"]),
    "CLOUDFLARE_API_TOKEN": ("Cloudflare", ["APP"]),
    "VERCEL_TOKEN": ("Vercel hosting", ["APP"]),
    "NETLIFY_AUTH_TOKEN": ("Netlify hosting", ["APP"]),
    "TAVILY_API_KEY": ("Tavily web search", ["WEB"]),
    "SERPAPI_API_KEY": ("SerpAPI web search", ["WEB"]),
    "BRAVE_API_KEY": ("Brave web search", ["WEB"]),
    "EXA_API_KEY": ("Exa web search", ["WEB"]),
    "NOTION_TOKEN": ("Notion", ["DOC"]),
    "SLACK_BOT_TOKEN": ("Slack", ["AGENT"]),
}

NET_HOSTS = [  # (host, url, role)
    ("pypi.org", "https://pypi.org/simple/", "pip"),
    ("registry.npmjs.org", "https://registry.npmjs.org/", "npm"),
    ("github.com", "https://github.com/", "git"),
    ("api.github.com", "https://api.github.com/", "git"),
    ("huggingface.co", "https://huggingface.co/", "models"),
    ("cdn.jsdelivr.net", "https://cdn.jsdelivr.net/", "cdn"),
    ("fonts.googleapis.com", "https://fonts.googleapis.com/css2?family=Cairo", "fonts"),
    ("api.anthropic.com", "https://api.anthropic.com/", "claude-api"),
    ("example.com", "https://example.com/", "generic"),
    ("en.wikipedia.org", "https://en.wikipedia.org/", "generic"),
]

# --------------------------------------------------------------------------- checks


def os_release() -> dict:
    out = {}
    try:
        for ln in Path("/etc/os-release").read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" in ln:
                k, v = ln.split("=", 1)
                out[k] = v.strip().strip('"')
    except OSError:
        pass
    return out


def ram_bytes():
    try:
        info = Path("/proc/meminfo").read_text()
        tot = re.search(r"MemTotal:\s+(\d+)", info)
        av = re.search(r"MemAvailable:\s+(\d+)", info)
        return int(tot.group(1)) * 1024, (int(av.group(1)) * 1024 if av else None)
    except (OSError, AttributeError):
        pass
    if sys.platform == "darwin":
        rc, out = run(["sysctl", "-n", "hw.memsize"], 1.5)
        if rc == 0 and out.strip().isdigit():
            return int(out.strip()), None
    if os.name == "nt":
        try:
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]
            m = MS()
            m.dwLength = ctypes.sizeof(MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return m.ullTotalPhys, m.ullAvailPhys
        except Exception:
            pass
    return None, None


def check_system() -> dict:
    osr = os_release()
    total, avail = ram_bytes()
    s = {
        "platform": platform.system(), "machine": platform.machine(), "kernel": platform.release(),
        "distro": osr.get("PRETTY_NAME", "") or platform.platform(), "distro_id": osr.get("ID", ""),
        "cpus": os.cpu_count(), "ram_gib": gib(total), "ram_free_gib": gib(avail) if avail else None,
        "python": platform.python_version(),
    }
    try:
        s["is_root"] = hasattr(os, "geteuid") and os.geteuid() == 0
    except Exception:
        s["is_root"] = False
    disks = {}
    for label, p in (("cwd", os.getcwd()), ("temp", tempfile.gettempdir())):
        try:
            du = shutil.disk_usage(p)
            disks[label] = {"free_gib": gib(du.free), "total_gib": gib(du.total)}
        except OSError:
            pass
    s["disk"] = disks
    # 32 MB write test inside the temp dir (deleted right away)
    try:
        blob = os.urandom(1024 * 1024)
        t = time.monotonic()
        with tempfile.NamedTemporaryFile(prefix="kosif-probe-", delete=True) as f:
            for _ in range(32):
                f.write(blob)
            f.flush()
            os.fsync(f.fileno())
        dt = max(time.monotonic() - t, 1e-3)
        s["write_test"] = {"mb": 32, "seconds": round(dt, 2), "mb_per_s": int(32 / dt)}
    except OSError as e:
        s["write_test"] = {"error": type(e).__name__}
    s["sudo_nopasswd"] = False
    if not s["is_root"] and shutil.which("sudo"):
        rc, _ = run(["sudo", "-n", "true"], 1.0)
        s["sudo_nopasswd"] = rc == 0
    s["container"] = [e for e in ("/.dockerenv", "/run/.containerenv") if os.path.exists(e)]
    try:
        cg = Path("/proc/1/cgroup").read_text(errors="replace")
        if re.search(r"docker|containerd|kubepods|lxc", cg):
            s["container"].append("/proc/1/cgroup")
    except OSError:
        pass
    return s


def check_gpu() -> dict:
    g = {"present": False, "evidence": []}
    if shutil.which("nvidia-smi"):
        rc, out = run(["nvidia-smi", "-L"], 2.5)
        if rc == 0 and "GPU" in out:
            g["present"] = True
            g["evidence"].append(out.strip().splitlines()[0][:120])
    if os.path.exists("/dev/nvidia0"):
        g["present"] = True
        g["evidence"].append("/dev/nvidia0")
    if os.path.isdir("/dev/dri") and any(n.startswith("renderD") for n in os.listdir("/dev/dri")):
        g["evidence"].append("/dev/dri render node (may be an integrated GPU)")
    if sys.platform == "darwin" and platform.machine() == "arm64":
        g["present"] = True
        g["evidence"].append("Apple silicon (Metal GPU)")
    return g


def check_bins() -> dict:
    out = {}
    for group, names in BINS.items():
        for n in names:
            p = shutil.which(n)
            if p:
                out[n] = {"path": p, "group": group, "version": ""}
    return out


def check_versions(bins: dict) -> dict:
    tasks = {}
    for name, cmd in VERSION_CMDS.items():
        if name == "pip" or name in bins:
            tasks[name] = (lambda c=cmd: run(c, 3.0 if c[0] in ("soffice", "blender", "java") else 2.0))
    res, _ = parallel(tasks, min(3.5, max(0.5, left() - 1)))
    out = {}
    for name, r in res.items():
        if isinstance(r, tuple) and r[0] is not None:
            out[name] = tool_version(name, r[1])
    return out


def tool_version(name: str, text: str) -> str:
    """Version from a --version banner; skips lines where a runtime echoes env values."""
    if name == "java":
        m = re.search(r'version "([^"]+)"', text or "")
        if m:
            return m.group(1)
    lines = [ln for ln in (text or "").splitlines()
             if ln.strip() and not ln.startswith(("Picked up", "NOTE:", "WARNING", "warning"))]
    for ln in lines[:3]:
        v = ver(ln)
        if v:
            return v
    return ""


def check_docker_daemon() -> dict:
    if not shutil.which("docker"):
        return {"client": False}
    rc, out = run(["docker", "info", "--format", "{{.ServerVersion}}"], 2.5)
    return {"client": True, "daemon": bool(rc == 0 and ver(out)), "server_version": ver(out) if rc == 0 else ""}


def check_python() -> dict:
    py = {"version": platform.python_version(), "executable_name": Path(sys.executable).name}
    try:
        import venv  # noqa: F401
        py["venv"] = True
    except ImportError:
        py["venv"] = False
    try:
        import ensurepip  # noqa: F401
        py["ensurepip"] = True
    except ImportError:
        py["ensurepip"] = False
    import importlib.util
    py["pip_module"] = importlib.util.find_spec("pip") is not None
    names = set()
    try:
        from importlib import metadata as md
        for d in md.distributions():
            try:
                n = d.metadata["Name"]
            except Exception:
                n = None
            if n:
                names.add(re.sub(r"[-_.]+", "-", n).lower())
    except Exception as e:
        py["error"] = type(e).__name__
    py["dist_count"] = len(names)
    py["notable"] = sorted(n for n in PY_NOTABLE if n in names)
    py["notable_missing"] = sorted(n for n in PY_NOTABLE if n not in names)
    py["_all"] = names
    try:
        import sqlite3
        py["sqlite3"] = sqlite3.sqlite_version
    except Exception:
        py["sqlite3"] = ""
    return py


def check_node(bins: dict) -> dict:
    nd = {"global": []}
    if "npm" not in bins:
        return nd
    rc, out = run(["npm", "root", "-g"], 3.0)
    root = out.strip().splitlines()[-1] if rc == 0 and out.strip() else ""
    if root and os.path.isdir(root):
        pk = []
        for n in sorted(os.listdir(root)):
            if n.startswith("."):
                continue
            if n.startswith("@") and os.path.isdir(os.path.join(root, n)):
                pk += ["%s/%s" % (n, m) for m in sorted(os.listdir(os.path.join(root, n)))]
            else:
                pk.append(n)
        nd["global"] = pk
    return nd


def check_fonts() -> dict:
    f = {"families": 0, "arabic": [], "arabic_good": [], "skill_fonts": []}
    if shutil.which("fc-list"):
        rc, out = run(["fc-list", ":", "family"], 3.0)
        if rc == 0:
            fams = {x.split(",")[0].strip().replace("\\-", "-") for x in out.splitlines() if x.strip()}
            f["families"] = len(fams)
        rc, out = run(["fc-list", ":lang=ar", "family"], 3.0)
        if rc == 0:
            ar = sorted({x.split(",")[0].strip().replace("\\-", "-") for x in out.splitlines() if x.strip()})
            f["arabic"] = ar
            f["arabic_good"] = [a for a in ar if any(g in a.lower() for g in ARABIC_GOOD_FONTS)]
    else:
        dirs = ["/Library/Fonts", "/System/Library/Fonts", str(Path.home() / "Library/Fonts"),
                os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")]
        files = []
        for d in dirs:
            if os.path.isdir(d):
                files += [n for n in os.listdir(d) if n.lower().endswith((".ttf", ".otf", ".ttc"))]
        f["families"] = len(files)
        f["arabic_good"] = sorted({n for n in files if any(g.replace(" ", "") in n.lower() for g in ARABIC_GOOD_FONTS)})
        f["arabic"] = list(f["arabic_good"])
    shared = ROOT / "proofs" / "_shared" / "fonts"
    if shared.is_dir():
        f["skill_fonts"] = sorted(n for n in os.listdir(str(shared)) if n.lower().endswith((".ttf", ".otf", ".woff2")))
    return f


def check_browsers(bins: dict) -> dict:
    b = {"playwright_dirs": [], "on_path": [n for n in BINS["browser"] if n in bins and n != "playwright"]}
    cands = ["/opt/pw-browsers", str(Path.home() / ".cache" / "ms-playwright"),
             str(Path.home() / "Library" / "Caches" / "ms-playwright")]
    env_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    seen = set()
    for c in ([env_path] if env_path else []) + cands:
        try:
            if c and os.path.isdir(c) and os.path.realpath(c) not in seen:
                seen.add(os.path.realpath(c))
                b["playwright_dirs"] += sorted(n for n in os.listdir(c) if re.match(r"(chromium|firefox|webkit|chrome)", n))
        except OSError:
            pass
    b["playwright_env_set"] = bool(env_path)
    b["chromium"] = any(n.startswith(("chromium", "chrome")) for n in b["playwright_dirs"]) or bool(
        set(b["on_path"]) & {"chromium", "chromium-browser", "google-chrome", "google-chrome-stable"})
    return b


def ssl_context():
    ctx = ssl.create_default_context()  # honours SSL_CERT_FILE / SSL_CERT_DIR through OpenSSL
    used = []
    for name in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"):
        p = os.environ.get(name)
        if p and os.path.isfile(p):
            try:
                ctx.load_verify_locations(cafile=p)
                used.append(name)
            except (ssl.SSLError, OSError):
                pass
    if not used and os.path.isfile("/root/.ccr/ca-bundle.crt"):
        try:
            ctx.load_verify_locations(cafile="/root/.ccr/ca-bundle.crt")
            used.append("/root/.ccr/ca-bundle.crt")
        except (ssl.SSLError, OSError):
            pass
    return ctx, used


def probe_url(opener, url: str, timeout: float) -> dict:
    t = time.monotonic()
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "kosif-probe/1.0 (+stdlib urllib)"})
    r = {}
    try:
        with opener.open(req, timeout=timeout) as resp:
            r = {"status": resp.status, "class": "ok"}
    except urllib.error.HTTPError as e:
        code = e.code
        r = {"status": code, "class": "blocked" if code == 407 else ("ok" if code < 400 else "reachable")}
    except urllib.error.URLError as e:
        reason = e.reason
        txt = str(reason)
        m = re.search(r"Tunnel connection failed:\s*(\d{3})", txt)
        if m:
            r = {"status": int(m.group(1)), "class": "blocked", "detail": "proxy refused CONNECT"}
        elif isinstance(reason, ssl.SSLError) or "CERTIFICATE" in txt.upper():
            r = {"status": None, "class": "tls-error", "detail": "certificate not trusted (do not disable verification)"}
        elif isinstance(reason, socket.timeout) or "timed out" in txt:
            r = {"status": None, "class": "offline", "detail": "timeout"}
        elif isinstance(reason, socket.gaierror):
            r = {"status": None, "class": "offline", "detail": "DNS"}
        else:
            r = {"status": None, "class": "offline", "detail": type(reason).__name__ if not isinstance(reason, str) else reason[:60]}
    except (socket.timeout, TimeoutError):
        r = {"status": None, "class": "offline", "detail": "timeout"}
    except (OSError, ValueError) as e:
        m = re.search(r"Tunnel connection failed:\s*(\d{3})", str(e))
        r = ({"status": int(m.group(1)), "class": "blocked", "detail": "proxy refused CONNECT"} if m else
             {"status": None, "class": "offline", "detail": type(e).__name__})
    r["ms"] = int((time.monotonic() - t) * 1000)
    return r


def proxy_info() -> dict:
    """Describe the proxy without printing its URL (env values stay private)."""
    names = [n for n in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "NO_PROXY", "no_proxy", "ALL_PROXY")
             if os.environ.get(n)]
    info = {"env_names": names, "local": False, "agent_proxy": None}
    raw = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if raw:
        try:
            u = urllib.parse.urlsplit(raw if "://" in raw else "http://" + raw)
            info["local"] = (u.hostname or "") in ("127.0.0.1", "localhost", "::1")
            if info["local"]:
                base = "%s://%s" % (u.scheme or "http", u.netloc.split("@")[-1])
                op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
                with op.open(base + "/__agentproxy/status", timeout=min(2.0, max(0.3, left() - 0.5))) as resp:
                    st = json.loads(resp.read(200000).decode("utf-8", "replace"))
                fails, seen = [], {}
                for f in st.get("recentRelayFailures") or []:
                    if isinstance(f, dict):
                        key = (f.get("host"), f.get("kind"))
                        if key not in seen:
                            seen[key] = {"host": key[0], "kind": key[1], "count": 0}
                            fails.append(seen[key])
                        seen[key]["count"] += 1
                info["agent_proxy"] = {
                    "enabled": st.get("enabled"), "bundleCoversEveryHost": st.get("bundleCoversEveryHost"),
                    "selective": st.get("selective"), "caBundlePath": st.get("caBundlePath"),
                    "preconfigured_clis": st.get("installedProxyPreconfiguredClis") or [],
                    "recent_relay_failures": fails[:10],
                    "readme": st.get("readmePath"),
                }
        except Exception:
            pass
    return info


def check_network(skip: bool, distro_id: str) -> dict:
    if skip:
        return {"skipped": True, "hosts": {}, "level": "unknown"}
    hosts = list(NET_HOSTS)
    apt_host = "archive.ubuntu.com" if distro_id == "ubuntu" else "deb.debian.org"
    hosts.append((apt_host, "http://%s/" % apt_host if apt_host == "archive.ubuntu.com" else "https://%s/" % apt_host, "apt"))
    ctx, ca_used = ssl_context()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler(), urllib.request.HTTPSHandler(context=ctx))
    per = min(2.5, max(0.5, left() - 1.0))
    tasks = {h: (lambda u=u: probe_url(opener, u, per)) for h, u, _role in hosts}
    res, tout = parallel(tasks, per + 0.8)
    out = {}
    for h, u, role in hosts:
        r = res.get(h) or {"status": None, "class": "offline", "detail": "probe timed out"}
        r["role"] = role
        out[h] = r
    ok = lambda h: out.get(h, {}).get("class") in ("ok", "reachable")  # noqa: E731
    reg = ok("pypi.org") or ok("registry.npmjs.org")
    generic = ok("example.com") or ok("en.wikipedia.org")
    if reg and generic:
        level = "full"
    elif reg:
        level = "registries-only"
    elif any(ok(h) for h in out):
        level = "partial"
    else:
        level = "none"
    return {"skipped": False, "hosts": out, "level": level, "ca_sources": ca_used, "apt_host": apt_host,
            "timed_out": tout}


def check_keys() -> dict:
    present = sorted(n for n in KEY_NAMES if os.environ.get(n))
    hazards = {n: bool(os.environ.get(n)) for n in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "PIP_CERT",
                                                    "NODE_EXTRA_CA_CERTS", "NODE_USE_ENV_PROXY")}
    return {"credential_names": present, "ca_env_names": hazards}


def detect_host(system: dict, proxy: dict, net: dict) -> dict:
    sc = {"claude-code-cloud": 0.0, "claude-ai-sandbox": 0.0, "ci": 0.0, "claude-code-local": 0.0, "local": 0.0,
          "generic-container": 0.0}
    ev = {k: [] for k in sc}

    def add(k, pts, why):
        sc[k] += pts
        ev[k].append(why)

    if os.path.isdir("/root/.ccr"):
        add("claude-code-cloud", 3, "/root/.ccr exists")
    if proxy.get("agent_proxy"):
        add("claude-code-cloud", 3, "local agent proxy answered /__agentproxy/status")
    if os.environ.get("CLAUDE_CODE_REMOTE"):
        add("claude-code-cloud", 3, "CLAUDE_CODE_REMOTE is set")
    if os.getcwd().startswith("/home/user"):
        add("claude-code-cloud", 1, "working dir under /home/user")
    if os.environ.get("CLAUDECODE") and not os.environ.get("CLAUDE_CODE_REMOTE"):
        add("claude-code-local", 3, "CLAUDECODE is set without CLAUDE_CODE_REMOTE")
    for p in ("/mnt/user-data", "/mnt/data"):
        if os.path.isdir(p):
            add("claude-ai-sandbox", 1, p + " exists")
    if str(Path.home()) == "/home/claude":
        add("claude-ai-sandbox", 2, "home is /home/claude")
    if not proxy.get("env_names") and net.get("level") == "none":
        add("claude-ai-sandbox", 1, "no proxy and no outbound network")
    for n in ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "BUILDKITE", "CIRCLECI"):
        if os.environ.get(n):
            add("ci", 3, n + " is set")
            break
    if system.get("platform") in ("Darwin", "Windows"):
        add("local", 3, "desktop OS " + system.get("platform"))
    if os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
        add("local", 1, "graphical display present")
    if str(Path.home()).startswith("/Users/"):
        add("local", 1, "home under /Users")
    if system.get("container"):
        add("generic-container", 1, "container markers: " + ", ".join(system["container"]))
    best = max(sc, key=lambda k: sc[k])
    if sc[best] == 0:
        best = "local" if system.get("platform") in ("Darwin", "Windows") else "unknown-linux"
    labels = {"claude-code-cloud": "Claude Code cloud session", "claude-ai-sandbox": "claude.ai code sandbox (likely)",
              "ci": "CI runner", "claude-code-local": "Claude Code on a local machine", "local": "local machine",
              "generic-container": "generic container", "unknown-linux": "Linux host (type unclear)"}
    return {"type": best, "label": labels.get(best, best), "evidence": ev.get(best, []),
            "scores": {k: v for k, v in sc.items() if v}, "claude_code": bool(os.environ.get("CLAUDECODE"))}


def catalog_install_counts() -> dict:
    """Count 📦 catalog powers by the package manager their install command needs."""
    out = {"pip": 0, "npm": 0, "apt": 0, "other": 0, "total": 0}  # other = no command named (e.g. "see arsenal")
    d = ROOT / "data" / "powers"
    if not d.is_dir():
        return out
    for p in sorted(d.glob("*.json")):
        try:
            rows = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for r in rows if isinstance(rows, list) else []:
            if not isinstance(r, dict) or r.get("status") != "install":
                continue
            cmd = str(r.get("install") or "") + " " + str(r.get("how") or "")[:200]
            out["total"] += 1
            if re.search(r"\b(pip3?|uv pip|uv add|pipx)\b", cmd):
                out["pip"] += 1
            elif re.search(r"\b(npm|npx|pnpm|yarn|bun add)\b", cmd):
                out["npm"] += 1
            elif re.search(r"\bapt(-get)?\b|\bbrew\b", cmd):
                out["apt"] += 1
            else:
                out["other"] += 1
    return out


def install_test(bins: dict) -> dict:
    """Optional: time a real venv+pip install and an npm install inside a temp dir."""
    res = {}
    with tempfile.TemporaryDirectory(prefix="kosif-probe-") as td:
        vdir = os.path.join(td, "venv")
        t = time.monotonic()
        rc, out = run([sys.executable, "-m", "venv", vdir], 60)
        vpy = os.path.join(vdir, "Scripts" if os.name == "nt" else "bin", "python")
        if rc == 0 and os.path.exists(vpy):
            rc, out = run([vpy, "-m", "pip", "install", "--disable-pip-version-check", "-q", "six"], 90)
            if rc == 0:
                rc, out = run([vpy, "-c", "import six; print(six.__version__)"], 10)
            res["venv+pip"] = {"ok": rc == 0, "seconds": round(time.monotonic() - t, 1), "package": "six",
                               "detail": "" if rc == 0 else out.strip()[-200:]}
            if "uv" in bins:
                t = time.monotonic()
                rc, out = run(["uv", "pip", "install", "--python", vpy, "-q", "packaging"], 60)
                res["uv"] = {"ok": rc == 0, "seconds": round(time.monotonic() - t, 1), "package": "packaging",
                             "detail": "" if rc == 0 else out.strip()[-200:]}
        else:
            res["venv+pip"] = {"ok": False, "seconds": round(time.monotonic() - t, 1), "detail": out.strip()[-200:]}
        if "npm" in bins and "node" in bins:
            nd = os.path.join(td, "npm")
            os.makedirs(nd)
            t = time.monotonic()
            rc, out = run(["npm", "install", "--prefix", nd, "--no-audit", "--no-fund", "--silent", "is-number"], 90)
            if rc == 0:
                rc, out = run(["node", "-e", "require(process.argv[1]);console.log('ok')",
                               os.path.join(nd, "node_modules", "is-number")], 10)
            res["npm"] = {"ok": rc == 0, "seconds": round(time.monotonic() - t, 1), "package": "is-number",
                          "detail": "" if rc == 0 else out.strip()[-200:]}
    return res


# --------------------------------------------------------------------------- analysis


def managers(c: dict) -> dict:
    bins, sysd, net = c["bins"], c["system"], c["network"]
    hosts = net.get("hosts", {})
    unknown = net.get("skipped")

    def reach(h):
        if unknown:
            return None
        return hosts.get(h, {}).get("class") in ("ok", "reachable")

    root_ok = sysd.get("is_root") or sysd.get("sudo_nopasswd")
    pip_present = c["python"].get("pip_module") or "uv" in bins or "pip" in bins or "pip3" in bins
    return {
        "pip": {"present": bool(pip_present), "network": reach("pypi.org"), "cmd": "uv pip install" if "uv" in bins else "pip install"},
        "npm": {"present": "npm" in bins, "network": reach("registry.npmjs.org"), "cmd": "npm i"},
        "apt": {"present": "apt-get" in bins and bool(root_ok), "network": reach(net.get("apt_host", "")) if not unknown else None,
                "cmd": ("" if sysd.get("is_root") else "sudo ") + "apt-get install -y"},
        "brew": {"present": "brew" in bins, "network": None if unknown else net.get("level") in ("full", "partial"), "cmd": "brew install"},
    }


def usable(m: dict, name: str):
    """True / False / None (unknown network)."""
    x = m.get(name, {})
    if not x.get("present"):
        return False
    return x.get("network")


# Domain rows: (label, families, have(c)->list of present things, fixes [(manager, cmd)])
def domain_rows(c: dict) -> list:
    bins, py, fonts, br, gpu = c["bins"], c["python"], c["fonts"], c["browsers"], c["gpu"]
    pyn = set(py.get("notable", []))
    vers = c.get("versions", {})

    def b(*names):
        return [n + (" " + vers[n] if vers.get(n) else "") for n in names if n in bins]

    def p(*names):
        return ["py:" + n for n in names if n in pyn]

    rows = [
        ("Video / فيديو", "ENG TRANS SYNC FOOT QA FMT", b("ffmpeg", "ffprobe", "yt-dlp"),
         [("apt", "ffmpeg"), ("brew", "ffmpeg"), ("pip", "imageio-ffmpeg")]),
        ("Image / صور", "MEDIA TEX", b("convert", "magick", "inkscape", "rsvg-convert") + p("pillow", "opencv-python-headless", "opencv-python"),
         [("pip", "pillow opencv-python-headless"), ("apt", "imagemagick")]),
        ("Audio / صوت", "BEAT VOICE MEDIA", b("sox", "espeak-ng", "piper") + p("librosa", "soundfile", "pydub") + (["ffmpeg"] if "ffmpeg" in bins else []),
         [("pip", "librosa soundfile"), ("apt", "sox")]),
        ("Speech-to-text / تفريغ", "SYNC VOICE MEDIA", p("faster-whisper", "openai-whisper"),
         [("pip", "faster-whisper")]),
        ("OCR", "MEDIA DOC", b("tesseract"), [("apt", "tesseract-ocr tesseract-ocr-ara"), ("brew", "tesseract tesseract-lang")]),
        ("Docs & PDF / مستندات", "DOC", b("soffice", "pandoc", "pdftotext", "qpdf") + p("python-docx", "openpyxl", "python-pptx", "reportlab", "pypdf", "pymupdf"),
         [("pip", "python-docx openpyxl python-pptx reportlab pypdf"), ("apt", "libreoffice-core pandoc poppler-utils")]),
        ("LaTeX / معادلات", "DOC EXPL", b("xelatex", "pdflatex", "lualatex", "tectonic"),
         [("apt", "texlive-xetex texlive-lang-arabic"), ("brew", "tectonic")]),
        ("Browser / متصفح", "APP WEB QA ENG UI", (["playwright: " + ", ".join(br.get("playwright_dirs", [])[:3])] if br.get("playwright_dirs") else []) + br.get("on_path", []),
         [("npm", "playwright && npx playwright install chromium"), ("pip", "playwright && python3 -m playwright install chromium")]),
        ("Data / بيانات", "ANLY DATA", p("pandas", "numpy", "polars", "duckdb", "pyarrow") + b("sqlite3", "duckdb", "jq", "psql") + (["py:sqlite3"] if py.get("sqlite3") else []),
         [("pip", "pandas duckdb")]),
        ("Charts / رسوم", "ANLY DATA", p("matplotlib", "plotly", "seaborn", "altair"),
         [("pip", "matplotlib plotly")]),
        ("Diagrams / مخططات", "GRAPH EXPL", b("dot", "mmdc", "plantuml", "d2") + p("graphviz", "networkx"),
         [("apt", "graphviz"), ("npm", "-g @mermaid-js/mermaid-cli"), ("pip", "networkx")]),
        ("Local AI / ذكاء محلي", "GEN MEDIA", (["GPU"] if gpu.get("present") else []) + p("torch", "onnxruntime", "transformers") + b("ollama"),
         [("pip", "onnxruntime")]),
        ("Arabic text / نص عربي", "ARAB ARL TYPE", fonts.get("arabic_good", [])[:4] + (["skill fonts: %d files" % len(fonts["skill_fonts"])] if fonts.get("skill_fonts") else []) + p("arabic-reshaper", "python-bidi"),
         [("apt", "fonts-noto-core fonts-kacst"), ("pip", "arabic-reshaper python-bidi")]),
        ("3D", "3D", b("blender", "openscad"), [("apt", "blender")]),
        ("Dev & build / تطوير", "CODE CHECK", b("git", "gcc", "node", "go", "rustc", "java", "docker", "make"),
         [("apt", "build-essential git")]),
        ("Repos & cloud / سحابة", "CODE APP AGENT", b("gh", "gcloud", "aws", "az", "wrangler", "vercel", "netlify", "kubectl"),
         [("apt", "gh"), ("brew", "gh"), ("npm", "-g wrangler")]),
    ]
    m = managers(c)
    out = []
    for label, fams, have, fixes in rows:
        if have:
            state = "ready"
            fix = ""
        else:
            state, fix = "missing", ""
            for mgr, pkg in fixes:
                u = usable(m, mgr)
                if u or u is None and m.get(mgr, {}).get("present"):
                    state = "install" if u else "unknown"
                    fix = "%s %s" % (m[mgr]["cmd"], pkg)
                    break
        out.append({"domain": label, "state": state, "badge": BADGE[state], "present": have, "fix": fix,
                    "families": fams.split()})
    return out


def unlocks(c: dict) -> tuple:
    bins, py, net, gpu, fonts, br = c["bins"], c["python"], c["network"], c["gpu"], c["fonts"], c["browsers"]
    vers = c.get("versions", {})
    pyn = set(py.get("notable", []))
    m = managers(c)
    cat = c.get("catalog", {})
    U, G = [], []

    def u(finding, because, fams, status):
        U.append({"finding": finding, "unlocks": because, "families": fams, "status": status, "badge": BADGE[status]})

    def gap(missing, fix, fams):
        G.append({"missing": missing, "fix_cmd": fix, "families": fams})

    def v(n):
        return (n + " " + vers.get(n, "")).strip()

    if "ffmpeg" in bins:
        u(v("ffmpeg"), "cut, concat, transcode, loudnorm −14 LUFS, burn captions (libass), frames/audio extract, xfade, probe for QA",
          ["ENG", "TRANS", "SYNC", "BEAT", "FOOT", "QA", "FMT", "MEDIA"], "ready")
    if br.get("chromium"):
        u("headless Chromium (Playwright)", "render HTML/CSS/Canvas/WebGL scenes to frames and MP4, screenshots, HTML→PDF, page checks",
          ["ENG", "UI", "EXPL", "QA", "APP", "WEB", "DOC"], "ready")
    if "soffice" in bins or "pandoc" in bins:
        u(" + ".join(x for x in (v("soffice") if "soffice" in bins else "", v("pandoc") if "pandoc" in bins else "") if x),
          "convert docx/xlsx/pptx/md/html ↔ PDF headless", ["DOC"], "ready")
    office_py = [n for n in ("python-docx", "openpyxl", "python-pptx", "reportlab", "pypdf", "pymupdf") if n in pyn]
    if office_py:
        u("python: " + ", ".join(office_py), "generate and edit Word/Excel/PowerPoint/PDF files from code", ["DOC"], "ready")
    data_py = [n for n in ("pandas", "numpy", "polars", "duckdb", "pyarrow", "scipy") if n in pyn]
    if data_py:
        u("python: " + ", ".join(data_py), "load, clean, join, aggregate and test data; sqlite3 is built in", ["ANLY", "DATA"], "ready")
    if "tesseract" in bins:
        u(v("tesseract"), "OCR of scans and video frames", ["MEDIA", "DOC"], "ready")
    if "convert" in bins or "magick" in bins or "pillow" in pyn:
        u("ImageMagick/Pillow", "resize, composite, contact sheets, format conversion", ["MEDIA", "TEX", "QA"], "ready")
    if "faster-whisper" in pyn or "openai-whisper" in pyn:
        u("whisper (python)", "word-timed transcripts for captions and sync", ["SYNC", "VOICE", "MEDIA"], "ready")
    if fonts.get("arabic_good"):
        u("Arabic fonts: " + ", ".join(fonts["arabic_good"][:3]), "render shaped Arabic text with a real Arabic face", ["ARAB", "ARL", "TYPE"], "ready")
    elif fonts.get("skill_fonts"):
        u("skill-bundled fonts (proofs/_shared/fonts)", "load Cairo/Amiri/Tajawal/Reem Kufi/Aref Ruqaa files directly (system Arabic faces are weak here)",
          ["ARAB", "ARL", "TYPE"], "ready")
    if "git" in bins:
        u(v("git") + (" + " + v("gh") if "gh" in bins else ""), "clone, branch, diff, PRs and CI logs (gh auth not checked)", ["CODE", "AGENT"], "ready")
    comp = [n for n in ("gcc", "clang", "go", "rustc", "java") if n in bins]
    if comp:
        u("compilers: " + ", ".join(comp), "build native tools from source when no package exists", ["CODE"], "ready")
    if "dot" in bins or "mmdc" in bins:
        u("graphviz/mermaid-cli", "render graphs, mind maps and flowcharts to SVG/PNG", ["GRAPH", "EXPL"], "ready")
    if "blender" in bins:
        u(v("blender"), "headless 3D scenes (CPU: slow)", ["3D"], "ready")
    dk = c.get("docker", {})
    if dk.get("client"):
        u("docker " + ("daemon %s" % dk.get("server_version") if dk.get("daemon") else "client only (daemon not reachable)"),
          "isolated services and toolchains", ["CODE", "APP"], "ready" if dk.get("daemon") else "unknown")
    # one-install-away unlocks
    pu, nu, au = usable(m, "pip"), usable(m, "npm"), usable(m, "apt")
    if pu:
        n = cat.get("pip", 0)
        u("pip%s + pypi reachable" % (" / uv" if "uv" in bins else ""),
          "any wheel library is one command away (%s)%s" % (m["pip"]["cmd"], "; %d 📦 catalog powers name a pip command" % n if n else ""),
          ["ANLY", "MEDIA", "DOC", "SYNC", "GEN"], "install")
    if nu:
        n = cat.get("npm", 0)
        u("npm + registry reachable", "Remotion, d3, three.js, lottie, Motion Canvas, mermaid-cli%s" % ("; %d 📦 catalog powers name an npm/npx command" % n if n else ""),
          ["APP", "ENG", "3D", "DATA", "UI"], "install")
    if au:
        n = cat.get("apt", 0)
        u("apt-get as root + mirror reachable", "system packages: tesseract, texlive, graphviz, blender, sox, fonts-noto%s" % ("; %d 📦 catalog powers name an apt/brew command" % n if n else ""),
          ["MEDIA", "GRAPH", "3D", "ARAB", "DOC"], "install")
    hf = net.get("hosts", {}).get("huggingface.co", {}).get("class") in ("ok", "reachable")
    if hf:
        u("huggingface.co reachable" + ("" if gpu.get("present") else " (no GPU)"),
          "download small model weights and datasets" + ("" if gpu.get("present") else "; CPU only, keep models small (whisper tiny/base)"),
          ["GEN", "MEDIA", "SYNC"], "install")
    if gpu.get("present"):
        u("GPU: " + "; ".join(gpu.get("evidence", [])[:1]), "local diffusion / LLM inference becomes practical", ["GEN"], "install")
    level = net.get("level")
    if level == "full":
        u("open outbound network", "fetch docs, papers and pages from the shell (respect licenses and robots)", ["WEB"], "ready")
    for k in c["keys"].get("credential_names", []):
        svc, fams = KEY_NAMES[k]
        u("env name %s present" % k, svc + " (value not read; it may be a proxy placeholder)", fams, "key")
    # gaps
    if "ffmpeg" not in bins:
        gap("ffmpeg", fix_for(m, [("apt", "ffmpeg"), ("brew", "ffmpeg"), ("pip", "imageio-ffmpeg")]), ["ENG", "TRANS", "SYNC"])
    if not br.get("chromium"):
        gap("headless Chromium", fix_for(m, [("npm", "playwright && npx playwright install chromium"), ("pip", "playwright && python3 -m playwright install chromium")]),
            ["ENG", "APP", "QA"])
    if "tesseract" not in bins:
        gap("tesseract OCR", fix_for(m, [("apt", "tesseract-ocr tesseract-ocr-ara"), ("brew", "tesseract tesseract-lang")]), ["MEDIA"])
    if not fonts.get("arabic_good"):
        gap("good system Arabic font", fix_for(m, [("apt", "fonts-noto-core fonts-kacst")]) or "ship the font files with the project (proofs/_shared/fonts)",
            ["ARAB", "TYPE"])
    for pkg, fams in (("matplotlib", ["ANLY", "DATA"]), ("faster-whisper", ["SYNC", "VOICE"]), ("librosa", ["BEAT"]),
                      ("opencv-python-headless", ["MEDIA", "QA"]), ("yt-dlp", ["DL"]), ("duckdb", ["ANLY"])):
        if pkg not in pyn and not (pkg == "yt-dlp" and "yt-dlp" in bins) and not (pkg == "opencv-python-headless" and "opencv-python" in pyn):
            f = fix_for(m, [("pip", pkg)])
            if f:
                gap(pkg, f, fams)
    if "dot" not in bins:
        gap("graphviz (dot)", fix_for(m, [("apt", "graphviz"), ("brew", "graphviz")]), ["GRAPH", "EXPL"])
    if not any(x in bins for x in ("xelatex", "tectonic")):
        gap("XeLaTeX (Arabic math/print)", fix_for(m, [("apt", "texlive-xetex texlive-lang-arabic"), ("brew", "tectonic")]), ["DOC"])
    if "blender" not in bins:
        gap("blender", fix_for(m, [("apt", "blender"), ("brew", "--cask blender")]), ["3D"])
    if "sox" not in bins:
        gap("sox", fix_for(m, [("apt", "sox"), ("brew", "sox")]), ["BEAT", "VOICE"])
    G = [g for g in G if g["fix_cmd"]]
    return U, G


def fix_for(m: dict, options) -> str:
    for mgr, pkg in options:
        x = usable(m, mgr)
        if x or (x is None and m.get(mgr, {}).get("present")):
            return "%s %s" % (m[mgr]["cmd"], pkg)
    return ""


# --------------------------------------------------------------------------- output


def collect(args) -> dict:
    timed_out = []
    bins = check_bins()
    first, t1 = parallel({
        "system": check_system, "gpu": check_gpu, "python": check_python, "fonts": check_fonts,
        "proxy": proxy_info, "catalog": catalog_install_counts,
        "versions": lambda: check_versions(bins), "node": lambda: check_node(bins),
        "docker": check_docker_daemon, "keys": check_keys,
    }, max(1.0, left() - 4.5))
    timed_out += t1
    system = first.get("system") or {}
    net = check_network(args.no_network or left() < 3.5, system.get("distro_id", ""))
    if not args.no_network and net.get("skipped"):
        timed_out.append("network")
    c = {
        "probe": {"script": "scripts/probe_env.py", "date": datetime.date.today().isoformat(), "version": 1},
        "host": {}, "system": system, "gpu": first.get("gpu") or {}, "bins": bins,
        "versions": first.get("versions") or {}, "python": first.get("python") or {}, "node": first.get("node") or {},
        "fonts": first.get("fonts") or {}, "browsers": check_browsers(bins), "proxy": first.get("proxy") or {},
        "network": net, "keys": first.get("keys") or {}, "docker": first.get("docker") or {},
        "catalog": first.get("catalog") or {},
    }
    for k, v in list(c.items()):
        if isinstance(v, dict) and "error" in v and len(v) == 1:
            timed_out.append(k + " (error)")
    for name, info in bins.items():
        if c["versions"].get(name):
            info["version"] = c["versions"][name]
    c["host"] = detect_host(system, c["proxy"], net)
    c["domains"] = domain_rows(c)
    c["unlocks"], c["gaps"] = unlocks(c)
    if args.install_test:
        BUDGET[0] += 240
        c["install_test"] = install_test(bins)
    c["python"].pop("_all", None)
    c["timed_out"] = timed_out + list(net.get("timed_out", []))
    c["elapsed_s"] = round(time.monotonic() - T0, 1)
    return c


def md_escape(s) -> str:
    return str(s).replace("|", "\\|")


def card(c: dict, snapshot: bool = False) -> str:
    s, h, net, py = c["system"], c["host"], c["network"], c["python"]
    disk = (s.get("disk") or {}).get("cwd") or (s.get("disk") or {}).get("temp") or {}
    gpu = "yes" if c["gpu"].get("present") else "none"
    L = []
    H = "##" if snapshot else "#"
    sub = "###" if snapshot else "##"
    L.append("%s Capability card — بطاقة القدرات" % H)
    L.append("")
    L.append("**%s** · %s · %s CPU · %s GiB RAM · %s GiB free disk · GPU: %s · network: **%s** · python %s%s · probe %.1f s" % (
        h.get("label"), s.get("distro") or s.get("platform"), s.get("cpus"), s.get("ram_gib"), disk.get("free_gib", "?"),
        gpu, net.get("level"), py.get("version", ""), (" · node " + c["versions"]["node"]) if c["versions"].get("node") else "",
        c.get("elapsed_s", 0)))
    L.append("")
    L.append("Legend: 🟢 present now (answered a version or import check) · 📦 one install command away (manager present and its "
             "registry reachable) · 🔑 needs a key, account or connector · ❌ not available here · ❔ unknown. The probe proves "
             "presence, not quality: ✅ stays reserved for powers with a real run and a proof path.")
    L.append("")
    L.append("%s Domains — المجالات" % sub)
    L.append("")
    L.append("| Domain | State | Present here | Fix if missing | Power families |")
    L.append("|---|---|---|---|---|")
    for r in c["domains"]:
        L.append("| %s | %s | %s | %s | %s |" % (r["domain"], r["badge"], md_escape(", ".join(r["present"][:6]) or "—"),
                                             ("`%s`" % r["fix"]) if r["fix"] else "—", " ".join(r["families"])))
    L.append("")
    L.append("%s Top unlocks → powers — ماذا يفتح كل اكتشاف" % sub)
    L.append("")
    order = {"ready": 0, "install": 1, "key": 2, "unknown": 3}
    for x in sorted(c["unlocks"], key=lambda x: order.get(x["status"], 9)):
        L.append("- %s **%s** → %s → `%s`" % (x["badge"], md_escape(x["finding"]), x["unlocks"], " ".join(x["families"])))
    if c.get("gaps"):
        L.append("")
        L.append("%s One-line fixes — إصلاحات بسطر واحد" % sub)
        L.append("")
        for g in c["gaps"]:
            L.append("- %s: `%s` (%s)" % (g["missing"], g["fix_cmd"], " ".join(g["families"])))
    L.append("")
    L.append("%s Network — الشبكة" % sub)
    L.append("")
    if net.get("skipped"):
        L.append("Skipped (`--no-network` or no time left).")
    else:
        px = c.get("proxy") or {}
        ap = px.get("agent_proxy")
        line = "Level **%s**. Proxy env names: %s." % (net.get("level"), ", ".join(px.get("env_names") or []) or "none")
        if net.get("ca_sources"):
            line += " CA bundle loaded from: %s (verification stays on)." % ", ".join(net["ca_sources"])
        L.append(line)
        if ap:
            fails = ", ".join("%s (%s%s)" % (f.get("host"), f.get("kind"), " ×%d" % f["count"] if f.get("count", 1) > 1 else "")
                              for f in ap.get("recent_relay_failures", [])) or "none"
            L.append("Agent proxy: enabled=%s, covers every host=%s, selective=%s, preconfigured CLIs: %s; recent relay failures: %s. "
                     "Rules: never disable TLS verification or unset the proxy; a 403/407/502 is a policy answer to report, not to route around; "
                     "Node's built-in fetch needs NODE_USE_ENV_PROXY=1; details in %s." % (
                         ap.get("enabled"), ap.get("bundleCoversEveryHost"), ap.get("selective"),
                         ", ".join(ap.get("preconfigured_clis") or []) or "none", fails, ap.get("readme") or "the proxy README"))
        L.append("")
        L.append("| Host | Role | Class | HTTP | ms |")
        L.append("|---|---|---|---|---|")
        for host, r in net.get("hosts", {}).items():
            L.append("| %s | %s | %s | %s | %s |" % (host, r.get("role"), r.get("class") + (" (%s)" % r["detail"] if r.get("detail") else ""),
                                                 r.get("status") or "—", r.get("ms")))
        L.append("")
        L.append("Classes: ok = 2xx/3xx · reachable = the host answered 4xx/5xx (normal for bare roots) · blocked = proxy refused · "
                 "offline = DNS/timeout · tls-error = certificate not trusted.")
    L.append("")
    L.append("%s Machine & runtimes — الجهاز والبيئات" % sub)
    L.append("")
    wt = s.get("write_test") or {}
    L.append("- OS: %s (%s, kernel %s) · user: %s%s · container markers: %s" % (
        s.get("distro"), s.get("machine"), s.get("kernel"), "root" if s.get("is_root") else "non-root",
        " (passwordless sudo)" if s.get("sudo_nopasswd") else "", ", ".join(s.get("container") or []) or "none"))
    L.append("- CPU %s · RAM %s GiB (%s GiB free) · disk free %s GiB of %s · temp write %s MB/s · GPU: %s" % (
        s.get("cpus"), s.get("ram_gib"), s.get("ram_free_gib"), disk.get("free_gib"), disk.get("total_gib"),
        wt.get("mb_per_s", "?"), "; ".join(c["gpu"].get("evidence") or []) or "none (CPU rendering only)"))
    vs = c.get("versions", {})
    L.append("- Versions: " + " · ".join("%s %s" % (k, vs[k]) for k in sorted(vs) if vs[k]))
    pm = managers(c)
    L.append("- Package managers: " + " · ".join("%s %s" % (k, "usable" if usable(pm, k) else ("present, network unknown" if pm[k]["present"] and usable(pm, k) is None else ("present, registry unreachable" if pm[k]["present"] else "absent"))) for k in ("pip", "npm", "apt", "brew")))
    present_by_group = {}
    for n, info in sorted(c["bins"].items()):
        present_by_group.setdefault(info["group"], []).append(n)
    L.append("- CLI tools by group: " + " · ".join("**%s** %s" % (g, ", ".join(v)) for g, v in present_by_group.items()))
    missing = [n for g, names in BINS.items() if g not in ("pkg", "misc") for n in names if n not in c["bins"]]
    L.append("- Not found on PATH: " + ", ".join(missing))
    L.append("")
    L.append("%s Python & Node packages — الحزم" % sub)
    L.append("")
    L.append("- Python %s: %s distributions; notable present: %s" % (py.get("version"), py.get("dist_count"), ", ".join(py.get("notable", [])) or "none"))
    L.append("- Notable absent (install on demand): " + (", ".join(py.get("notable_missing", [])) or "none"))
    L.append("- venv %s · ensurepip %s · pip module %s · sqlite3 %s" % (
        "yes" if py.get("venv") else "no", "yes" if py.get("ensurepip") else "no", "yes" if py.get("pip_module") else "no", py.get("sqlite3") or "no"))
    g = c.get("node", {}).get("global", [])
    L.append("- Node global packages (%d): %s" % (len(g), ", ".join(g) or "none"))
    L.append("")
    L.append("%s Fonts & browsers — الخطوط والمتصفحات" % sub)
    L.append("")
    f = c["fonts"]
    L.append("- %s font families; Arabic-capable: %s" % (f.get("families"), ", ".join(f.get("arabic", [])) or "none"))
    L.append("- Good Arabic display faces installed: %s" % (", ".join(f.get("arabic_good", [])) or "none — install fonts-noto-core or load the skill fonts"))
    if f.get("skill_fonts"):
        L.append("- Skill-bundled font files (proofs/_shared/fonts): " + ", ".join(f["skill_fonts"]))
    b = c["browsers"]
    L.append("- Playwright browsers: %s · browsers on PATH: %s" % (", ".join(b.get("playwright_dirs", [])) or "none", ", ".join(b.get("on_path", [])) or "none"))
    L.append("")
    L.append("%s Credentials & connectors — المفاتيح والموصلات" % sub)
    L.append("")
    names = c["keys"].get("credential_names", [])
    L.append("- Service credential env names present (values never read): " + (", ".join(names) or "none"))
    L.append("- MCP connectors, deferred tools and skills are invisible to this script: read your own tool list, load deferred tools "
             "with ToolSearch, and check the skills listing before deciding what you can do.")
    if c.get("install_test"):
        L.append("")
        L.append("%s Install test — اختبار التثبيت" % sub)
        L.append("")
        for k, r in c["install_test"].items():
            L.append("- %s: %s in %s s (%s)%s" % (k, "ok" if r.get("ok") else "FAILED", r.get("seconds"), r.get("package", ""),
                                                ("; " + r["detail"]) if r.get("detail") else ""))
    L.append("")
    L.append("%s Host evidence — دليل نوع المضيف" % sub)
    L.append("")
    L.append("- Type: %s (scores %s)" % (h.get("type"), ", ".join("%s=%g" % kv for kv in sorted(h.get("scores", {}).items(), key=lambda x: -x[1])) or "none"))
    for e in h.get("evidence", []):
        L.append("  - " + e)
    if c.get("timed_out"):
        L.append("- Timed out or failed: " + ", ".join(c["timed_out"]))
    return "\n".join(L) + "\n"


def snapshot_doc(c: dict) -> str:
    body = card(c, snapshot=True)
    heads = [ln[3:].strip() for ln in body.splitlines() if ln.startswith("### ")]
    out = [
        "# لقطة البيئة — Environment snapshot",
        "",
        "What this gives you: a dated capability card of the machine where the skill was last probed — runtimes, CLI tools, "
        "packages, fonts, network reach, and which power families each finding unlocks. Open it when planning what you can "
        "build, but trust it only for that machine and date: run `python3 scripts/probe_env.py` (or `python3 scripts/powers.py env`) "
        "in your own session first.",
        "",
        "> Snapshot taken %s on a **%s** by `scripts/probe_env.py`. Facts change per machine and per session — re-run to refresh; "
        "never quote these versions as timeless truth." % (c["probe"]["date"], c["host"].get("label")),
        "",
        "## الفهرس / contents",
        "",
        "- Capability card — بطاقة القدرات",
    ]
    out += ["  - " + x for x in heads]
    out += ["", body, "---", "_Generated by `python3 scripts/probe_env.py --write references/environment.md`; do not edit by hand._", ""]
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Probe this machine's real capabilities (stdlib only, read-only, ~20 s).")
    ap.add_argument("--json", action="store_true", help="print JSON instead of the Markdown card")
    ap.add_argument("--no-network", action="store_true", help="skip network checks")
    ap.add_argument("--install-test", action="store_true", help="also time a real venv+pip and npm install in a temp dir")
    ap.add_argument("--budget", type=float, default=18.0, help="seconds for the whole probe (default 18)")
    ap.add_argument("--write", metavar="PATH", help="also write a dated Markdown snapshot to PATH")
    a = ap.parse_args(argv)
    BUDGET[0] = max(3.0, a.budget)
    try:
        c = collect(a)
    except Exception as e:  # always exit 0 with whatever we know
        c = None
        print("probe failed: %s: %s" % (type(e).__name__, e), file=sys.stderr)
    if c is None:
        print(json.dumps({"error": "probe failed"}) if a.json else "probe failed — see stderr")
        return 0
    if a.write:
        try:
            Path(a.write).write_text(snapshot_doc(c), encoding="utf-8")
            print("wrote " + a.write, file=sys.stderr)
        except OSError as e:
            print("could not write %s: %s" % (a.write, e), file=sys.stderr)
    if a.json:
        print(json.dumps(c, ensure_ascii=False, indent=1, default=str))
    else:
        print(card(c), end="")
    return 0


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError, ImportError):
        pass
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
