#!/usr/bin/env python3
"""Shared helpers for the Dragon Montage stations (see ../CONTRACTS.md).

Stdlib only. Every station uses these to read/write job files, run tools with a
receipt, and find the existing KOSIF tools it reuses.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
ROOT = SKILL.parents[2]                      # repo root
SKILLS = ROOT / ".claude" / "skills"
SP = SKILLS / "kosif-superpowers" / "scripts"
SP_DATA = SKILLS / "kosif-superpowers" / "data"
VENDOR_SS = SKILLS / "kosif-superpowers" / "vendor" / "100-superskills" / "skills"
KMM = VENDOR_SS / "kosif-montage-motion" / "scripts"
PVE = VENDOR_SS / "pro-video-editor-ffmpeg" / "scripts"
MIND = SKILLS / "kosif-dragon-mind"
MATRICES = SKILLS / "kosif-infinite-matrices"
HOOKS = SKILLS / "kosif-reel-hooks"
CATALOG = ROOT / "catalog"

SCHEMAS = {
    "job": "kosif.dm.job.v1",
    "analysis": "kosif.dm.analysis.v1",
    "brief": "kosif.dm.brief.v1",
    "concepts": "kosif.dm.concepts.v1",
    "look": "kosif.dm.look.v1",
    "edl": "kosif.dm.edl.v1",
    "render": "kosif.dm.render.v1",
    "review": "kosif.dm.review.v1",
}

# Minimal required keys per file; stations may add more.
REQUIRED = {
    "analysis": ["clips", "music", "tools_used", "missing"],
    "brief": ["task", "platform", "aspect", "target_seconds", "feeling", "content_type"],
    "concepts": ["concepts", "decision"],
    "look": ["style_id", "grade", "transitions", "captions"],
    "edl": ["width", "height", "fps", "events", "audio", "captions", "duration"],
    "render": ["final", "verify"],
    "review": ["round", "checks", "fixes", "verdict"],
}

ASPECTS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}


class ContractError(ValueError):
    pass


def validate(kind: str, data: dict) -> dict:
    if not isinstance(data, dict):
        raise ContractError(f"{kind}: not an object")
    want = SCHEMAS[kind]
    if data.get("schema") != want:
        raise ContractError(f"{kind}: schema must be {want}, got {data.get('schema')!r}")
    missing = [k for k in REQUIRED.get(kind, []) if k not in data]
    if missing:
        raise ContractError(f"{kind}: missing keys {missing}")
    if kind == "edl":
        for i, ev in enumerate(data["events"]):
            for k in ("id", "clip", "src_in", "src_out", "rec_in", "reason"):
                if k not in ev:
                    raise ContractError(f"edl.events[{i}] missing {k}")
            if not ev["src_out"] > ev["src_in"]:
                raise ContractError(f"edl.events[{i}] src_out must be > src_in")
            if not str(ev["reason"]).strip():
                raise ContractError(f"edl.events[{i}] needs a reason")
    return data


def new(kind: str, **fields) -> dict:
    return {"schema": SCHEMAS[kind], **fields}


def job_dir(path: str | Path) -> Path:
    p = Path(path).resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p


def read(job: Path, kind: str) -> dict:
    f = Path(job) / f"{kind}.json"
    if not f.exists():
        raise FileNotFoundError(f"{f} not found: run the station that writes {kind}.json first")
    return validate(kind, json.loads(f.read_text(encoding="utf-8")))


def write(job: Path, kind: str, data: dict) -> Path:
    validate(kind, data)
    f = Path(job) / f"{kind}.json"
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return f


def sha256(path: str | Path) -> str | None:
    p = Path(path)
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def have(binary: str) -> bool:
    return shutil.which(binary) is not None


def have_module(name: str) -> bool:
    import importlib.util
    return importlib.util.find_spec(name) is not None


def run(job: Path, station: str, tool: str, argv: list[str], *, out: str | Path | None = None,
        timeout: int = 900, owner_media: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and append a receipt line to receipts.jsonl."""
    t0 = time.time()
    res = subprocess.run([str(a) for a in argv], capture_output=True, text=True, timeout=timeout)
    rec = {
        "station": station, "tool": tool, "argv": [str(a) for a in argv][:40], "rc": res.returncode,
        "seconds": round(time.time() - t0, 3), "owner_media": owner_media,
        "sha256_out": sha256(out) if out else None,
        "stderr_tail": res.stderr[-400:] if res.returncode else "",
    }
    with (Path(job) / "receipts.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    if check and res.returncode != 0:
        raise RuntimeError(f"{tool} failed rc={res.returncode}: {res.stderr[-600:]}")
    return res


def py(script: Path) -> list[str]:
    return [sys.executable, str(script)]


def receipts(job: Path) -> list[dict]:
    f = Path(job) / "receipts.jsonl"
    if not f.exists():
        return []
    return [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]


def probe(path: str | Path) -> dict:
    res = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                         capture_output=True, text=True, timeout=60, check=True)
    return json.loads(res.stdout)


def make_test_clip(path: Path, seconds: float = 6.0, *, tone: int = 440, size: str = "1280x720",
                   color: str = "testsrc2") -> Path:
    """Synthetic clip for tests: moving pattern + tone, with a hard scene change half way."""
    half = seconds / 2
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-f", "lavfi", "-i", f"{color}=size={size}:rate=30:duration={half}",
        "-f", "lavfi", "-i", f"smptebars=size={size}:rate=30:duration={half}",
        "-f", "lavfi", "-i", f"sine=frequency={tone}:duration={seconds}",
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
        "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac",
        "-shortest", str(path)], check=True, timeout=120)
    return path
