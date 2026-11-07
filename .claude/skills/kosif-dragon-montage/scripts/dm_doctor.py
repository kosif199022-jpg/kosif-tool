#!/usr/bin/env python3
"""Dragon Montage doctor — which tools are installed, which station is ready.

Reads ../data/required_tools.json (the one list of every tool the protocol uses)
and checks this machine. Never installs anything.

  python3 dm_doctor.py doctor [--json] [--tier required|recommended|all]
  python3 dm_doctor.py install-plan --os linux|macos|windows|ashell [--tier ...] [--all]
  python3 dm_doctor.py fetch <tool-id> [--force]     # model files (kind "file"): download + sha256 check

doctor exits 0 when every *required* tool is present, 1 otherwise.
install-plan prints the exact commands for what is missing (or for everything
with --all); run them yourself, or use install_tools.sh / install_tools.ps1.
fetch downloads a manifest entry with a "download" block (e.g. the YuNet face
model) to its destination and refuses it unless the sha256 matches; the install
plan emits a fetch line for each such missing tool, so the install scripts get it.

Library use (other stations / dragon_montage.py):
  from dm_doctor import check_all, station_verdicts, model_path, repo_font
"""
from __future__ import annotations

import argparse
import functools
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
ROOT = SKILL.parents[2]
SKILLS = ROOT / ".claude" / "skills"
VENDOR_SS = SKILLS / "kosif-superpowers" / "vendor" / "100-superskills" / "skills"
KMM = VENDOR_SS / "kosif-montage-motion" / "scripts"
# Arabic fonts that ship inside the repo (same folders dm_render.find_font hands to libass as fontsdir).
REPO_FONT_DIRS = (SKILL / "assets" / "fonts", VENDOR_SS / "kosif-mimic" / "assets" / "fonts",
                  SKILLS / "kosif-superpowers" / "proofs" / "_shared" / "fonts", ROOT / "assets" / "fonts")
MANIFEST = SKILL / "data" / "required_tools.json"
TIERS = ("required", "recommended", "optional")
OSES = ("linux", "macos", "windows", "ashell")
TIER_AR = {"required": "لازم", "recommended": "مهمة", "optional": "إضافة"}


def load(path: Path = MANIFEST) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def tiers_for(tier: str) -> tuple[str, ...]:
    return {"required": ("required",), "recommended": ("required", "recommended")}.get(tier, TIERS)


# ------------------------------------------------------------------ checks
def _version_tuple(s: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", s)[:3])


def _repo_venv_has(module: str) -> str | None:
    """Module installed in one of the repo's side venvs (.venv, .venv-ml, …)?"""
    top = module.split(".")[0]
    for pattern in (".venv*/lib/python*/site-packages", ".venv*/Lib/site-packages"):
        for sp in glob.glob(str(ROOT / pattern)):
            if (Path(sp) / top).is_dir() or glob.glob(str(Path(sp) / f"{top}.py")) \
                    or glob.glob(str(Path(sp) / f"{top}*.so")) or glob.glob(str(Path(sp) / f"{top}*.pyd")):
                spp = Path(sp)
                return spp.parents[1 if spp.parent.name == "Lib" else 2].name
    return None


@functools.lru_cache(maxsize=1)
def _node_roots() -> tuple[Path, ...]:
    roots = [ROOT / "node_modules", ROOT / ".kosif-node" / "node_modules",
             ROOT / "starters" / "remotion" / "node_modules", Path("/opt/node-tools/node_modules")]
    roots += [Path(p) for p in os.environ.get("NODE_PATH", "").split(os.pathsep) if p]
    if os.environ.get("APPDATA"):
        roots.append(Path(os.environ["APPDATA"]) / "npm" / "node_modules")
    npm = shutil.which("npm")
    if npm:
        try:
            r = subprocess.run([npm, "root", "-g"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10)
            if r.returncode == 0 and r.stdout.strip():
                roots.append(Path(r.stdout.strip()))
        except (OSError, subprocess.SubprocessError):
            pass
    return tuple(roots)


def _browser_dirs() -> list[Path]:
    dirs = []
    if os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        dirs.append(Path(os.environ["PLAYWRIGHT_BROWSERS_PATH"]))
    home = Path.home()
    dirs += [home / ".cache" / "ms-playwright", home / "Library" / "Caches" / "ms-playwright"]
    if os.environ.get("LOCALAPPDATA"):
        dirs.append(Path(os.environ["LOCALAPPDATA"]) / "ms-playwright")
    return dirs


@functools.lru_cache(maxsize=1)
def _font_families() -> str:
    """Lower-case blob of installed font family names / file names."""
    parts = []
    if shutil.which("fc-list"):
        try:
            r = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20)
            parts.append(r.stdout)
        except (OSError, subprocess.SubprocessError):
            pass
    dirs = [Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), Path.home() / ".fonts",
            Path.home() / ".local" / "share" / "fonts", Path("/Library/Fonts"), Path("/System/Library/Fonts"),
            Path.home() / "Library" / "Fonts"]
    if os.environ.get("WINDIR"):
        dirs.append(Path(os.environ["WINDIR"]) / "Fonts")
    if os.environ.get("LOCALAPPDATA"):
        dirs.append(Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts")
    for d in dirs:
        if d.is_dir():
            for f in d.rglob("*"):
                if f.suffix.lower() in (".ttf", ".otf", ".ttc"):
                    parts.append(f.stem)
    return "\n".join(parts).lower().replace(" ", "").replace("-", "").replace("_", "")


def _fkey(s: str) -> str:
    return s.lower().replace(" ", "").replace("-", "").replace("_", "")


def repo_font(name: str) -> Path | None:
    """A .ttf/.otf of family `name` bundled in the repo (libass uses it through fontsdir, so it
    satisfies the caption font even when nothing is installed system-wide)."""
    key = _fkey(name)
    for d in REPO_FONT_DIRS:
        if d.is_dir():
            for f in sorted(d.iterdir()):
                if f.suffix.lower() in (".ttf", ".otf", ".ttc") and _fkey(f.stem).startswith(key):
                    return f
    return None


def expand(p: str) -> Path:
    """Manifest path placeholders: {skill} {root} {kmm} and ~."""
    return Path(p.replace("{skill}", str(SKILL)).replace("{root}", str(ROOT)).replace("{kmm}", str(KMM))).expanduser()


def _file_check(c: dict) -> Path | None:
    env = c.get("env")
    if env and os.environ.get(env) and Path(os.environ[env]).expanduser().is_file():
        return Path(os.environ[env]).expanduser()
    for d in c.get("dirs", []):
        f = expand(d) / c["name"]
        if f.is_file() and f.stat().st_size > 1024:   # a git-lfs pointer is ~130 bytes
            return f
    return None


def model_path(tool_id: str = "yunet-face-model", manifest: dict | None = None) -> Path | None:
    """Where a doctor-managed model file is on this machine, or None."""
    m = manifest or load()
    for t in m["tools"]:
        if t["id"] == tool_id:
            for c in t["check"]:
                if c.get("kind") == "file":
                    f = _file_check(c)
                    if f:
                        return f
    return None


def _sha256(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(tool_id: str, force: bool = False, manifest: dict | None = None, dest: Path | None = None) -> Path:
    """Download a tool's "download" file (url, then mirrors) and keep it only if sha256 matches."""
    import tempfile
    import urllib.request
    m = manifest or load()
    t = next((x for x in m["tools"] if x["id"] == tool_id), None)
    if not t or not t.get("download"):
        raise ValueError(f"{tool_id}: no download block in the manifest")
    dl = t["download"]
    dest = Path(dest) if dest else expand(dl["dest"])
    if dest.is_file() and not force and _sha256(dest) == dl["sha256"]:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    errors = []
    for url in [dl["url"], *dl.get("mirrors", [])]:
        fd, tmp = tempfile.mkstemp(prefix=".dl_", dir=dest.parent)
        os.close(fd)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "kosif-dm-doctor"})
            with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as out:
                shutil.copyfileobj(r, out)
            got = _sha256(Path(tmp))
            if got != dl["sha256"]:
                raise ValueError(f"sha256 {got} != {dl['sha256']}")
            os.replace(tmp, dest)
            return dest
        except Exception as e:  # noqa: BLE001 — try the next mirror
            errors.append(f"{url}: {e}")
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    raise RuntimeError("download failed:\n  " + "\n  ".join(errors))


def check_one(c: dict) -> tuple[bool, str]:
    """Return (present, where) for one check alternative."""
    kind, name = c.get("kind"), c.get("name", "")
    if kind == "python":
        ok = sys.version_info[:3] >= _version_tuple(c.get("min", "3"))
        return ok, f"python {sys.version.split()[0]}"
    if kind == "bin":
        p = shutil.which(name)
        return bool(p), p or ""
    if kind == "py":
        try:
            if importlib.util.find_spec(name) is not None:
                return True, f"import {name}"
        except (ImportError, ValueError):
            pass
        venv = _repo_venv_has(name)
        return (True, f"{name} in {venv}") if venv else (False, "")
    if kind == "node":
        for r in _node_roots():
            if (r / name / "package.json").is_file():
                return True, str(r / name)
        return False, ""
    if kind == "browser":
        for d in _browser_dirs():
            if d.is_dir() and any(x.name.startswith(name) for x in d.iterdir()):
                return True, str(d)
        for b in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
            if shutil.which(b):
                return True, shutil.which(b)
        return False, ""
    if kind == "font":
        key = name.lower().replace(" ", "")
        if key in _font_families():
            return True, f"font {name}"
        f = repo_font(name)
        return (True, f"font {name} (repo: {f.relative_to(ROOT)})") if f else (False, "")
    if kind == "file":
        f = _file_check(c)
        return (True, str(f)) if f else (False, "")
    return False, f"unknown check kind {kind!r}"


def check_tool(tool: dict) -> dict:
    """present = usable by this Python / PATH. A module found only in a side venv of the repo
    (.venv, .venv-ml …) counts for optional tools (they are run through that venv) and is
    reported as `elsewhere` for the others."""
    elsewhere = ""
    for c in tool["check"]:
        ok, where = check_one(c)
        if ok and " in .venv" in where and tool.get("tier") != "optional":
            elsewhere = elsewhere or where
            continue
        if ok:
            return {"id": tool["id"], "present": True, "where": where}
    return {"id": tool["id"], "present": False, "where": "", "elsewhere": elsewhere}


def check_services(manifest: dict) -> list[dict]:
    out = []
    for s in manifest.get("services", []):
        env = s.get("env", [])
        found = [e for e in env if os.environ.get(e)]
        configured = (len(found) == len(env)) if s.get("env_all") else bool(found)
        out.append({"id": s["id"], "name": s["name"], "env": env, "configured": bool(env) and configured,
                    "connector": s.get("connector"), "stations": s["stations"], "env_all": bool(s.get("env_all"))})
    return out


def check_all(tier: str = "all", manifest: dict | None = None) -> dict:
    """Check every tool; `tier` only narrows the `tools` list shown. Required tools always
    decide `ready`."""
    m = manifest or load()
    keep = tiers_for(tier)
    results = {t["id"]: check_tool(t) for t in m["tools"]}
    tools = [{**results[t["id"]], "name": t["name"], "tier": t["tier"], "stations": t["stations"],
              "purpose_ar": t["purpose"]["ar"], "breaks_without": t.get("breaks_without", "")}
             for t in m["tools"] if t["tier"] in keep]
    present = {i: r["present"] for i, r in results.items()}
    missing_required = [t["id"] for t in m["tools"] if t["tier"] == "required" and not present[t["id"]]]
    return {"schema": "kosif.dm.doctor.v1", "tier": tier, "tools": tools, "services": check_services(m),
            "stations": station_verdicts(m, present), "missing_required": missing_required,
            "ready": not missing_required, "python": sys.executable, "platform": sys.platform}


def station_verdicts(manifest: dict | None = None, present: dict | None = None) -> dict:
    m = manifest or load()
    if present is None:
        present = {t["id"]: check_tool(t)["present"] for t in m["tools"]}
    services = check_services(m)
    out = {}
    for sid, label in m["stations"].items():
        req = [t["id"] for t in m["tools"] if sid in t["stations"] and t["tier"] == "required"]
        rec = [t["id"] for t in m["tools"] if sid in t["stations"] and t["tier"] == "recommended"]
        opt = [t["id"] for t in m["tools"] if sid in t["stations"] and t["tier"] == "optional"]
        miss_req = [i for i in req if not present.get(i)]
        miss_rec = [i for i in rec if not present.get(i)]
        svc = [s["id"] for s in services if sid in s["stations"] and s["configured"]]
        level = "not-ready" if miss_req else ("full" if not miss_rec else "basic")
        out[sid] = {"ar": label["ar"], "ready": not miss_req, "level": level, "required": req,
                    "missing_required": miss_req, "missing_recommended": miss_rec,
                    "optional_present": [i for i in opt if present.get(i)], "services_configured": svc}
    return out


# ------------------------------------------------------------------ install plan
def _needs_closure(m: dict, ids: list[str]) -> list[str]:
    by = {t["id"]: t for t in m["tools"]}
    seen: list[str] = []
    visiting: set[str] = set()

    def add(i):
        if i in seen or i in visiting or i not in by:
            return
        visiting.add(i)
        for d in by[i].get("needs", []):
            add(d)
        seen.append(i)
    for i in ids:
        add(i)
    return seen


def install_plan(os_name: str, tier: str = "recommended", everything: bool = False,
                 manifest: dict | None = None, python: str | None = None) -> list[str]:
    """Exact commands for what is missing. `python` (e.g. a venv's interpreter) replaces the
    default `python3` / `py` in the pip lines."""
    if os_name not in OSES:
        raise ValueError(f"--os must be one of {OSES}")
    m = manifest or load()
    by = {t["id"]: t for t in m["tools"]}
    keep = tiers_for(tier)
    want = [t["id"] for t in m["tools"] if t["tier"] in keep and (everything or not check_tool(t)["present"])]
    ids = [i for i in _needs_closure(m, want) if everything or not check_tool(by[i])["present"]]
    pip_cmd = {"linux": "python3 -m pip install", "macos": "python3 -m pip install",
               "windows": "py -m pip install", "ashell": "pip install"}[os_name]
    if python and os_name != "ashell":
        pip_cmd = (f'& "{python}"' if os_name == "windows" else f'"{python}"') + " -m pip install"
    sysp: dict[str, list[str]] = {"apt": [], "brew": [], "cask": [], "winget": [], "choco": []}
    pips, npms, pre, post, notes, fetches = [], [], [], [], [], []
    py_cmd = {"linux": "python3", "macos": "python3", "windows": "py", "ashell": "python3"}[os_name]
    if python and os_name != "ashell":
        py_cmd = f'& "{python}"' if os_name == "windows" else f'"{python}"'
    doctor_rel = os.path.join(".claude", "skills", SKILL.name, "scripts", "dm_doctor.py")
    for i in ids:
        t = by[i]
        ins = t.get("install", {})
        osd = ins.get(os_name, {})
        if t.get("download"):
            fetches.append(f"{py_cmd} {doctor_rel} fetch {t['id']}")
        if os_name == "ashell":
            if osd.get("builtin"):
                notes.append(f"# {t['name']}: موجود في a-Shell")
                continue
            if osd.get("cmd"):
                pre += osd["cmd"]
            elif osd.get("note"):
                notes.append(f"# {t['name']}: {osd['note']}")
            else:
                notes.append(f"# {t['name']}: مش متاح على a-Shell (اشتغل بيه على الكمبيوتر)")
            continue
        for k in sysp:
            sysp[k] += [x for x in osd.get(k, []) if x not in sysp[k]]
        pips += [x for x in ins.get("pip", []) if x not in pips]
        npms += [x for x in ins.get("npm", []) if x not in npms]
        pre += osd.get("cmd", [])  # before pip (e.g. CPU torch before demucs)
        post += ins.get("post", {}).get(os_name, [])  # after npm (e.g. playwright browsers)
    lines = [f"# Dragon Montage install plan — {os_name} — tier={tier}" + (" (all)" if everything else " (missing only)"),
             "# شغّل الأوامر دي من فولدر الريبو (kosif-tool). الـ doctor نفسه مبيثبتش حاجة."]
    if not ids:
        lines.append("# كل حاجة متثبتة ✅")
        return lines
    if os_name == "linux" and sysp["apt"]:
        lines.append("sudo apt-get update && sudo apt-get install -y " + " ".join(sysp["apt"]))
    if os_name == "macos":
        if sysp["brew"]:
            lines.append("brew install " + " ".join(sysp["brew"]))
        if sysp["cask"]:
            lines.append("brew install --cask " + " ".join(sysp["cask"]))
    if os_name == "windows":
        for w in sysp["winget"]:
            lines.append(f"winget install -e --id {w}")
        if sysp["choco"]:
            lines.append("# أو بـ Chocolatey: choco install -y " + " ".join(sysp["choco"]))
    lines += pre
    if pips:
        lines.append(f"{pip_cmd} " + " ".join(f'"{p}"' if any(ch in p for ch in "<>=") else p for p in pips))
    if npms:
        lines.append("npm install --prefix .kosif-node " + " ".join(npms))
    lines += post
    lines += fetches
    lines += notes
    return lines


# ------------------------------------------------------------------ printing
def print_report(rep: dict) -> None:
    mark = {True: "✅", False: "❌"}
    print("🐉 دكتور مونتاج التنين — الأدوات اللي على الجهاز ده\n")
    print(f"{'':2} {'الأداة':<34} {'المستوى':<7} ليه")
    for tier in TIERS:
        rows = [t for t in rep["tools"] if t["tier"] == tier]
        for t in rows:
            print(f"{mark[t['present']]} {t['name'][:34]:<34} {TIER_AR[tier]:<7} {t['purpose_ar']}")
            if not t["present"] and t.get("elsewhere"):
                print(f"   ↳ متثبتة في venv تاني ({t['elsewhere']}) — شغّل المونتاج بالـ python بتاعه")
            elif not t["present"] and tier != "optional":
                print(f"   ↳ من غيرها: {t['breaks_without']}")
    print("\n🔑 خدمات مدفوعة/مفاتيح (مش تثبيت):")
    for s in rep["services"]:
        if s["configured"]:
            st = "✅ متظبط"
        elif s["connector"] and not s["env"]:
            st = f"🔌 بيشتغل من {s['connector']} (مش هقدر أتأكد من هنا)"
        else:
            st = "➖ مش متظبط: " + (" و ".join(s["env"]) if s["env_all"] else " أو ".join(s["env"])) + (f" (أو {s['connector']})" if s["connector"] else "")
        print(f"  {s['name']:<18} {st}")
    print("\n🎬 المحطات:")
    lvl = {"full": "🟢 جاهزة كاملة", "basic": "🟡 جاهزة (ناقصها حاجات مهمة)", "not-ready": "🔴 مش جاهزة"}
    for sid, v in rep["stations"].items():
        extra = ""
        if v["missing_required"]:
            extra = " — ناقص: " + ", ".join(v["missing_required"])
        elif v["missing_recommended"]:
            extra = " — يفضّل: " + ", ".join(v["missing_recommended"])
        print(f"  {sid:<9} {v['ar']:<24} {lvl[v['level']]}{extra}")
    print()
    if rep["ready"]:
        print("✅ الحكم: النظام جاهز يشتغل (كل الأدوات اللازمة موجودة).")
    else:
        print("❌ الحكم: مش جاهز. ناقص: " + ", ".join(rep["missing_required"]))
    print("   لأوامر التثبيت: python3 dm_doctor.py install-plan --os windows|macos|linux|ashell")


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("doctor", help="check this machine")
    d.add_argument("--json", action="store_true")
    d.add_argument("--tier", choices=["required", "recommended", "all"], default="all")
    d.add_argument("--manifest", type=Path, default=MANIFEST)
    p = sub.add_parser("install-plan", help="print install commands (never runs them)")
    p.add_argument("--os", dest="os_name", choices=OSES, required=True)
    p.add_argument("--tier", choices=["required", "recommended", "all"], default="recommended")
    p.add_argument("--all", action="store_true", help="include tools already installed")
    p.add_argument("--python", help="interpreter for the pip lines (default python3 / py)")
    p.add_argument("--manifest", type=Path, default=MANIFEST)
    f = sub.add_parser("fetch", help="download a model file listed with a download block (sha256-checked)")
    f.add_argument("tool_id")
    f.add_argument("--force", action="store_true")
    f.add_argument("--manifest", type=Path, default=MANIFEST)
    a = ap.parse_args(argv)
    m = load(a.manifest)
    if a.cmd == "fetch":
        try:
            path = fetch(a.tool_id, a.force, m)
        except (ValueError, RuntimeError) as e:
            print(f"❌ {e}", file=sys.stderr)
            return 1
        print(f"✅ {a.tool_id} → {path}")
        return 0
    if a.cmd == "doctor":
        rep = check_all(a.tier, m)
        if a.json:
            print(json.dumps(rep, ensure_ascii=False, indent=2))
        else:
            print_report(rep)
        return 0 if rep["ready"] else 1
    print("\n".join(install_plan(a.os_name, a.tier, a.all, m, a.python)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
