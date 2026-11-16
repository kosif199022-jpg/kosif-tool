#!/usr/bin/env python3
"""reel_kits.py: install the three free Claude reel skills from the owner's private copy.

The kits (make-reel, reel-maker, talking-character) are shared free by the «خبير أونلاين»
page (epreneurs.link/Claude-FreeVideos) with no licence file, and this repository is
public, so they are not stored here. The owner keeps the original zips privately
(project files: reel-kits-khabeer/) and this script checks and installs them.

  python3 -I reel_kits.py list                                   the three kits and their pinned SHA-256
  python3 -I reel_kits.py install ZIP --dest out/reel-kits       verify the hash, then extract safely
  python3 -I reel_kits.py status --dest out/reel-kits [--json]   which kits are installed there
  python3 -I reel_kits.py self-test [--out DIR]                  known-answer test on synthetic zips

Safety: the zip must match its pinned SHA-256 (or pass --allow-unpinned after a review);
absolute paths, `..`, symlinks and files over 5 MB are refused; nothing in the kit is run.
Pure standard library, no network.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[4]
DEFAULT_DEST = REPO / "out" / "reel-kits"
MAX_FILE = 5 * 1024 * 1024
MARKER = ".kosif-reel-kit.json"
# Reviewed 2026-11-16: local ffmpeg/ffprobe and edge-tts only, no hooks, no keys, no remote URLs in the scripts.
KITS = {
    "make-reel": {"sha256": "fb1c080ec138fa2d8f2030a7d4c4a5a173f7fcb16e3eb7fdb94c044f2298e2e5",
                  "what": "one line -> Egyptian script with tone tags, free edge-tts voice (2 takes per line), HyperFrames paper-style scenes, SFX mix"},
    "reel-maker": {"sha256": "a918a2611c6257c5b7d1faafab6e4f2d87338244f0d7702f6be8f23231ad306c",
                   "what": "branded reel system: script formula, 4 voice routes, word-timed captions, GSAP scenes with a presenter, text-overlap scan, 4 style presets"},
    "talking-character": {"sha256": "9859fee64b02c698f1edf8786b4dbfbe3dd0563220bfa2755d348244343047ef",
                          "what": "one photo -> consistent 2D cartoon of the user that talks with lip-sync (image model + Wan 2.7, paid), dialogue reel"},
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _kit_of(zf: zipfile.ZipFile) -> str | None:
    tops = {PurePosixPath(i.filename).parts[0] for i in zf.infolist() if i.filename.strip("/")}
    found = [t for t in tops if t in KITS]
    return found[0] if len(found) == 1 else None


def install(zip_path: Path, dest: Path, allow_unpinned: bool = False, pins: dict | None = None) -> dict:
    pins = pins if pins is not None else {k: v["sha256"] for k, v in KITS.items()}
    digest = _sha(zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        kit = _kit_of(zf)
        if kit is None:
            raise SystemExit("not one of the known kits: " + ", ".join(KITS))
        if pins.get(kit) != digest and not allow_unpinned:
            raise SystemExit(f"{kit}: SHA-256 {digest} is not the reviewed one; review the new version, then pass --allow-unpinned")
        refused, files = [], []
        for info in zf.infolist():
            name = info.filename
            p = PurePosixPath(name)
            mode = info.external_attr >> 16
            if name.startswith("/") or ".." in p.parts:
                refused.append([name, "path escape"]); continue
            if stat.S_ISLNK(mode):
                refused.append([name, "symlink"]); continue
            if info.file_size > MAX_FILE:
                refused.append([name, "over 5 MB"]); continue
            if name.endswith("/"):
                continue
            files.append(info)
        if refused:
            return {"kit": kit, "installed": False, "refused": refused}
        root = (dest / kit).resolve()
        for info in files:
            rel = PurePosixPath(info.filename)
            if len(rel.parts) == 1:          # a top-level readme beside the kit folder goes inside it
                rel = PurePosixPath(kit) / rel
            target = (dest / rel).resolve()
            if root not in target.parents and target != root:
                raise SystemExit(f"escape: {info.filename}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(info))
    marker = {"kit": kit, "zip_sha256": digest, "pinned": pins.get(kit) == digest, "files": len(files)}
    (root / MARKER).write_text(json.dumps(marker, indent=1), encoding="utf-8")
    return dict(marker, installed=True, path=str(root), skill_md=(root / "SKILL.md").is_file())


def status(dest: Path) -> dict:
    out = {}
    for kit in KITS:
        m = dest / kit / MARKER
        out[kit] = json.loads(m.read_text(encoding="utf-8")) if m.is_file() else None
    return {"dest": str(dest), "kits": out}


def self_test(out: Path | None = None) -> dict:
    checks = []
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        good = t / "good.zip"
        with zipfile.ZipFile(good, "w") as z:
            z.writestr("make-reel/SKILL.md", "---\nname: make-reel\ndescription: x\n---\n")
            z.writestr("make-reel/scripts/a.py", "print(1)\n")
        bad = t / "bad.zip"
        with zipfile.ZipFile(bad, "w") as z:
            z.writestr("make-reel/SKILL.md", "x")
            z.writestr("make-reel/../../escape.txt", "x")
        pins = {"make-reel": _sha(good)}
        r = install(good, t / "dest", pins=pins)
        checks.append(["pinned kit installs with its SKILL.md", r["installed"] and r["skill_md"] and r["files"] == 2])
        try:
            install(good, t / "dest2", pins={"make-reel": "0" * 64})
            checks.append(["an unpinned hash is refused", False])
        except SystemExit:
            checks.append(["an unpinned hash is refused", True])
        r2 = install(bad, t / "dest3", allow_unpinned=True, pins={})
        checks.append(["a path escape is refused and nothing installed", not r2["installed"] and not (t / "escape.txt").exists()])
        checks.append(["status sees the installed kit", status(t / "dest")["kits"]["make-reel"]["files"] == 2])
    res = {"passed": all(c[1] for c in checks), "checks": [{"name": n, "passed": p} for n, p in checks]}
    if out:
        out.mkdir(parents=True, exist_ok=True)
        (out / "selftest.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    i = sub.add_parser("install"); i.add_argument("zip", type=Path)
    i.add_argument("--dest", type=Path, default=DEFAULT_DEST); i.add_argument("--allow-unpinned", action="store_true")
    s = sub.add_parser("status"); s.add_argument("--dest", type=Path, default=DEFAULT_DEST); s.add_argument("--json", action="store_true")
    st = sub.add_parser("self-test"); st.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "list":
        res = KITS
    elif a.cmd == "install":
        res = install(a.zip, a.dest, a.allow_unpinned)
    elif a.cmd == "status":
        res = status(a.dest)
    else:
        res = self_test(a.out)
        print(json.dumps(res, indent=1))
        return 0 if res["passed"] else 1
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return 0 if res.get("installed", True) else 1


if __name__ == "__main__":
    sys.exit(main())
