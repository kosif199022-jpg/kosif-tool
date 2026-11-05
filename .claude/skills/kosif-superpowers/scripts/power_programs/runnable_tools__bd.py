"""TOOL-130 / TOOL-132: the card is a shipped tool; run its real analyst stage on a planted clip."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path
from ._mind_common import save, eq, truth

SCRIPTS = Path(__file__).resolve().parents[1]


def _clip(work: Path, w=640, h=360, d=3):
    out = work / "clip.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc2=s={w}x{h}:d={d}:r=25", "-f", "lavfi",
                    "-i", f"sine=f=440:d={d}", "-shortest", "-c:v", "libx264", "-c:a", "aac", str(out)], check=True)
    return out


def tool130(work):
    work = Path(work)
    clip = _clip(work)
    job = work / "job"
    r = subprocess.run([sys.executable, str(SCRIPTS / "montage_pro.py"), "intake", str(clip), "--job", str(job)],
                       capture_output=True, text=True, timeout=300)
    intake = json.loads((job / "intake.json").read_text())
    p = intake["probe"]
    return [eq("intake exit", r.returncode, 0), eq("measured duration", p["duration"], 3.0, tol=0.1),
            eq("measured size", (p["video"]["width"], p["video"]["height"]), (640, 360)),
            truth("loudness measured", isinstance(intake.get("loudness", {}).get("integrated_lufs"), (int, float)))]


def tool132(work):
    """init a project, then prep a planted 16:9 clip into the engine's fixed 1080x1920 shot."""
    work = Path(work)
    clip = _clip(work)
    job = work / "job"
    run = lambda *a: subprocess.run([sys.executable, str(SCRIPTS / "dua_wednesday.py"), *a], capture_output=True,
                                    text=True, timeout=300)
    r1 = run("init", "--job", str(job))
    r2 = run("prep", "--job", str(job), str(clip))
    shot = job / "v" / "00.mp4"
    st = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", str(shot)],
                                   capture_output=True, text=True).stdout)["streams"]
    v = [x for x in st if x["codec_type"] == "video"][0]
    proj = json.loads((job / "project.json").read_text(encoding="utf-8"))
    return [eq("init exit", r1.returncode, 0), eq("prep exit", r2.returncode, 0),
            eq("shot is 9:16 1080x1920", (v["width"], v["height"]), (1080, 1920)),
            truth("project.json has lines and shots", "lines" in proj and "shots" in proj, list(proj)[:8])]


PROGRAMS = {"TOOL-130": tool130, "TOOL-132": tool132}
