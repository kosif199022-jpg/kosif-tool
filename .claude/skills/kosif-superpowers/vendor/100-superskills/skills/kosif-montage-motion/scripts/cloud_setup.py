"""Prepare a cloud sandbox (claude.ai, Claude Code on the web, any Linux container) for KOSIF Montage & Motion —
no user PC involved. Run once per sandbox, then use `python scripts/kmotion.py …` as usual.

    python scripts/cloud_setup.py                 # check and wire what exists; nothing is installed
    python scripts/cloud_setup.py --install       # also pip-install imageio-ffmpeg when there is no ffmpeg
    python scripts/cloud_setup.py --install --browser   # … and try Playwright's Chromium (often blocked in sandboxes)

What it does:
  * a writable home (KOSIF_MOTION_HOME, default ~/kosif-motion) — the skill folder may be read-only;
  * ffmpeg: on PATH, else imageio-ffmpeg's binary (installed with --install), linked into HOME/bin;
  * ffprobe: on PATH, else a stand-in (scripts/ffprobe_shim.py) in HOME/bin;
  * the example projects copied into HOME/projects (kit scripts and fonts restored by `kmotion sync`);
  * ~/.kosif-motion.json, which kmotion.py reads so every later call finds the home and HOME/bin by itself;
  * a report of what this sandbox can render, and the folders for uploads (/mnt/user-data/uploads) and deliveries
    (/mnt/user-data/outputs) when they exist.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = Path.home() / ".kosif-motion.json"


def _writable(d: Path) -> bool:
    try:
        d.mkdir(parents=True, exist_ok=True)
        probe = d / ".kosif_write_test"
        probe.write_text("ok"); probe.unlink()
        return True
    except OSError:
        return False


def _pip(pkg: str) -> tuple[bool, str]:
    r = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", pkg], capture_output=True, text=True)
    return r.returncode == 0, (r.stderr or r.stdout or "").strip()[-300:]


def _imageio_ffmpeg(install: bool) -> tuple[str | None, str]:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe(), "imageio-ffmpeg (already installed)"
    except Exception:  # noqa: BLE001
        pass
    if not install:
        return None, "no ffmpeg; run again with --install to fetch imageio-ffmpeg"
    ok, msg = _pip("imageio-ffmpeg")
    if not ok:
        return None, f"pip install imageio-ffmpeg failed: {msg}"
    try:
        import importlib
        importlib.invalidate_caches()
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe(), "imageio-ffmpeg (installed now)"
    except Exception as e:  # noqa: BLE001
        return None, f"imageio-ffmpeg installed but unusable: {e}"


def _link(target: str, link: Path):
    """bin/NAME → target (symlink, else a copy; on Windows a .cmd wrapper)."""
    link.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":                                   # a real .exe (a .cmd wrapper would let cmd mangle | in filter graphs)
        exe = link.with_suffix(".exe")
        if not exe.exists():
            try:
                os.link(target, exe)
            except OSError:
                shutil.copy2(target, exe)
        return str(exe)
    if link.exists() or link.is_symlink():
        link.unlink()
    try:
        link.symlink_to(target)
    except OSError:
        shutil.copy2(target, link)
    link.chmod(link.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return str(link)


def _short(path: str) -> str:
    """Windows: the 8.3 short path when it is plain ASCII (cmd reads .cmd files in the OEM code page and would mangle
    an Arabic user folder); elsewhere, the path unchanged."""
    if os.name != "nt" or str(path).isascii():
        return str(path)
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(4096)
        if ctypes.windll.kernel32.GetShortPathNameW(str(path), buf, 4096) and buf.value.isascii():
            return buf.value
    except Exception:  # noqa: BLE001
        pass
    return str(path)


def _shim(bin_dir: Path, ffmpeg: str) -> str:
    shim = HERE / "ffprobe_shim.py"
    if os.name == "nt":
        w = bin_dir / "ffprobe.cmd"
        w.write_text(f'@set "KOSIF_FFMPEG={_short(ffmpeg)}"\r\n@"{_short(sys.executable)}" "{_short(str(shim))}" %*\r\n', encoding="ascii", errors="replace")
        return str(w)
    w = bin_dir / "ffprobe"
    w.write_text(f'#!/bin/sh\nKOSIF_FFMPEG="{ffmpeg}" exec "{sys.executable}" "{shim}" "$@"\n', encoding="utf-8")
    w.chmod(0o755)
    return str(w)


def _copy_examples(home: Path) -> list[str]:
    src = HERE / "projects"
    dst = home / "projects"
    done = []
    if not src.exists() or src.resolve() == dst.resolve():
        return done
    for d in sorted(p for p in src.iterdir() if p.is_dir()):
        if not (dst / d.name).exists():
            shutil.copytree(d, dst / d.name, ignore=shutil.ignore_patterns("__pycache__", "frames"))
            done.append(d.name)
    return done


def setup(home: Path | None = None, install: bool = False, browser: bool = False, examples: bool = True) -> dict:
    rep: dict = {"skill": str(HERE.parent), "skill_writable": _writable(HERE.parent / "out")}
    home = Path(home or os.environ.get("KOSIF_MOTION_HOME") or (Path.home() / "kosif-motion")).expanduser().resolve()
    if not _writable(home):
        raise SystemExit(f"cannot write to {home}: pass --home DIR")
    bin_dir = home / "bin"; bin_dir.mkdir(parents=True, exist_ok=True)
    for sub in ("projects", "out", "workbench"):
        (home / sub).mkdir(exist_ok=True)
    rep["home"] = str(home)
    # look for system tools outside our own bin (a re-run must rewrite its wrappers, not mistake them for an install)
    def _norm(p: str) -> str:
        try:
            return str(Path(p).resolve()).lower()
        except OSError:
            return p.lower()
    sys_path = os.pathsep.join(p for p in os.environ.get("PATH", "").split(os.pathsep) if p and _norm(p) != _norm(str(bin_dir)))
    which = lambda name: shutil.which(name, path=sys_path)  # noqa: E731
    # ffmpeg
    ff = which("ffmpeg")
    if ff:
        rep["ffmpeg"] = {"path": ff, "source": "PATH"}
    else:
        exe, how = _imageio_ffmpeg(install)
        rep["ffmpeg"] = {"path": _link(exe, bin_dir / "ffmpeg") if exe else None, "source": how}
        ff = exe
    # ffprobe
    fp = which("ffprobe")
    if fp:
        rep["ffprobe"] = {"path": fp, "source": "PATH"}
    elif ff:
        rep["ffprobe"] = {"path": _shim(bin_dir, ff), "source": "ffprobe_shim.py (stand-in built on ffmpeg)"}
    else:
        rep["ffprobe"] = {"path": None, "source": "needs ffmpeg first"}
    # yt-dlp for `kmotion fetch` (Pinterest, TikTok, Instagram…): optional, installed with --install
    try:
        import yt_dlp  # noqa: F401
        rep["yt_dlp"] = "installed"
    except ImportError:
        if install:
            ok, msg = _pip("yt-dlp")
            rep["yt_dlp"] = "installed now" if ok else f"pip install yt-dlp failed: {msg}"
        else:
            rep["yt_dlp"] = "missing (run again with --install for kmotion fetch)"
    # browser (frame capture of HTML compositions)
    if browser:
        ok, msg = _pip("playwright")
        if ok:
            r = subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], capture_output=True, text=True)
            rep["browser_install"] = "ok" if r.returncode == 0 else f"chromium download failed: {(r.stderr or r.stdout).strip()[-300:]}"
        else:
            rep["browser_install"] = f"pip install playwright failed: {msg}"
    rep["examples_copied"] = _copy_examples(home) if examples else []
    io = {"uploads": "/mnt/user-data/uploads", "outputs": "/mnt/user-data/outputs"}
    rep["claude_ai_folders"] = {k: v for k, v in io.items() if Path(v).exists()}
    cfg = {"home": str(home), "bin": str(bin_dir), "skill": str(HERE.parent)}
    CONFIG.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    rep["config"] = str(CONFIG)
    # what can run now
    os.environ["KOSIF_MOTION_HOME"] = str(home)
    os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ.get("PATH", "")
    sys.path.insert(0, str(HERE))
    try:
        import env_check
        env = env_check.check()
        rep["route"] = env["route"]
        rep["can"] = {k: v for k, v in env["can"].items()}
        rep["arabic_font"] = env.get("arabic_font")
        rep["browser"] = env.get("browser")
    except Exception as e:  # noqa: BLE001
        rep["env_check_error"] = str(e)[:300]
    has_ff = bool(rep["ffmpeg"]["path"])
    rep["renders_without_browser"] = ["workbench (plan → 2D film, Pillow)", "timeline", "audio2motion", "montage / grade / captions",
                                      "silence / aspect / trim / concat / loop / export / platforms / thumb", "scenes", "privacy",
                                      "studio-import", "score / ambience (WAV)", "structural"] if has_ff else ["score / ambience (WAV)", "structural", "proplan"]
    rep["needs_browser"] = ["new / render / preview / frames (HTML, 3D, lab)", "direct", "verse", "template (render)"]
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--home", help="writable home (default ~/kosif-motion or KOSIF_MOTION_HOME)")
    ap.add_argument("--install", action="store_true", help="pip-install imageio-ffmpeg when no ffmpeg exists")
    ap.add_argument("--browser", action="store_true", help="try pip playwright + chromium (often blocked)")
    ap.add_argument("--no-examples", action="store_true")
    a = ap.parse_args()
    rep = setup(Path(a.home) if a.home else None, a.install, a.browser, not a.no_examples)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    ok = bool(rep["ffmpeg"]["path"])
    print(("\nجاهز: التصيير بلا متصفح متاح." if ok else "\nلا يوجد ffmpeg: أعد التشغيل مع --install.")
          + (" المتصفح متاح أيضًا." if rep.get("browser") else " لا متصفح: تركيبات HTML تُسلَّم كملف HTML يعمل بنفسه."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
