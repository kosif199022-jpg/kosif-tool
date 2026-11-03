#!/usr/bin/env python3
"""Black Dragon media adapters: run a real KOSIF video/audio tool and check what it made.

Usage: _black_dragon_media.py RECIPE ARTIFACT [--media FILE]

RECIPE is one of: rhythm, audio-cues, cinema, montage, verify, eyes, look, cut.
With --media the tool works on that file (never modified). Without it the
adapter renders a self-test clip with KNOWN answers first (a 120 BPM click
track, a shaking camera, 16:9 colour bars) so the run can be checked against
the truth, and the artifact says plainly that it was a self-test clip.

Every output the tool writes stays in ARTIFACT's own .work folder. ARTIFACT
gets a JSON report: input (kind, sha256), each command with its exit code and
receipt, every output file with sha256 and ffprobe facts, and the checks.
Exit code is 0 only when the tool ran and every required check passed, so a
broken tool can never earn an 'executed' receipt. No shell, no network.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
PY = sys.executable
SCHEMA = "kosif.black-dragon.media-adapter.v1"
SELF_TEST = {"seconds": 6.0, "bpm": 120, "size": "640x360", "fps": 30}
RECIPES = ("rhythm", "audio-cues", "cinema", "montage", "verify", "eyes", "look", "cut")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


class Run:
    def __init__(self, recipe: str, work: Path):
        self.recipe, self.work = recipe, work
        self.steps, self.outputs, self.checks, self.findings = [], [], [], []

    def call(self, label: str, argv: list[str], timeout: int = 600, ok_codes=(0,)) -> dict:
        done = subprocess.run(argv, cwd=self.work, text=True, capture_output=True,
                              stdin=subprocess.DEVNULL, timeout=timeout, check=False)
        step = {"step": label, "command": argv, "exit_code": done.returncode}
        try:
            step["receipt"] = json.loads(done.stdout)
        except json.JSONDecodeError:
            step["stdout_tail"] = done.stdout[-1500:]
        if done.stderr.strip():
            step["stderr_tail"] = done.stderr[-600:]
        self.steps.append(step)
        if done.returncode not in ok_codes:
            raise RuntimeError(f"{label} exited {done.returncode}: {done.stderr[-300:]}")
        return step

    def check(self, name: str, passed: bool, value=None) -> bool:
        self.checks.append({"check": name, "pass": bool(passed), "value": value})
        return bool(passed)

    def output(self, path: Path, video: bool = False) -> dict:
        row = {"path": str(path), "exists": path.is_file()}
        if row["exists"]:
            row.update(bytes=path.stat().st_size, sha256=sha256(path))
            if video:
                row["probe"] = probe(path)
        self.outputs.append(row)
        self.check(f"output written: {path.name}", row["exists"] and row.get("bytes", 0) > 0,
                   row.get("bytes"))
        return row


def probe(path: Path) -> dict:
    done = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                           "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate",
                           "-of", "json", str(path)], text=True, capture_output=True, check=False)
    if done.returncode:
        return {"error": done.stderr[-200:]}
    raw = json.loads(done.stdout)
    out = {"duration": round(float(raw.get("format", {}).get("duration", 0) or 0), 3)}
    for s in raw.get("streams", []):
        if s.get("codec_type") == "video" and "video" not in out:
            num, _, den = str(s.get("r_frame_rate", "0/1")).partition("/")
            out["video"] = {"codec": s.get("codec_name"), "width": s.get("width"),
                            "height": s.get("height"),
                            "fps": round(float(num) / float(den or 1), 3) if float(den or 1) else None}
        if s.get("codec_type") == "audio" and "audio" not in out:
            out["audio"] = {"codec": s.get("codec_name")}
    return out


def self_test_clip(work: Path) -> Path:
    """Known-answer clip: 120 BPM clicks, shaking camera over moving colour bars."""
    clip = work / "self-test.mp4"
    t = SELF_TEST
    period = 60.0 / t["bpm"]
    audio = (f"aevalsrc='0.5*sin(2*PI*880*t)*lt(mod(t\\,{period})\\,0.06)"
             f"+0.03*sin(2*PI*110*t)':s=44100:d={t['seconds']}")
    w, h = (int(v) for v in t["size"].split("x"))
    shake = (f"crop={w - 40}:{h - 24}:20+15*sin(2*PI*3.1*t):12+9*sin(2*PI*2.3*t+1),"
             f"scale={w}:{h}")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-f", "lavfi", "-i", f"testsrc2=size={t['size']}:rate={t['fps']}:duration={t['seconds']}",
                    "-f", "lavfi", "-i", audio, "-vf", shake,
                    "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-shortest", str(clip)],
                   check=True, stdin=subprocess.DEVNULL, capture_output=True, timeout=120)
    return clip


def wav_of(r: Run, media: Path) -> Path:
    wav = r.work / "audio.wav"
    r.call("extract mono WAV (ffmpeg)", ["ffmpeg", "-y", "-loglevel", "error", "-i", str(media),
                                          "-vn", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(wav)])
    return wav


def tool(name: str) -> str:
    return str(SCRIPTS / name)


# ---------------------------------------------------------------- recipes
def rhythm(r: Run, media: Path, selftest: bool) -> None:
    wav = wav_of(r, media)
    cues, grid = r.work / "cues.json", r.work / "rhythm.json"
    r.call("audio_cue_mapper", [PY, tool("audio_cue_mapper.py"), str(wav), "--out", str(cues)])
    r.call("music_rhythm_engine", [PY, tool("music_rhythm_engine.py"), str(cues), "--out", str(grid)])
    r.output(grid)
    data = json.loads(grid.read_text(encoding="utf-8"))
    bpm, beats = data.get("candidate_tempo_bpm"), data.get("estimated_grid_seconds") or []
    r.findings.append({"tempo_bpm_candidate": bpm, "beats": len(beats), "first_beats": beats[:8],
                       "note": ("tempo is a measured hypothesis from onsets, not a verified BPM" if beats else
                                "no steady beat found in this audio: cut on the energy cues instead")})
    if selftest:
        r.check("beat grid has beats", len(beats) > 0, len(beats))
        r.check(f"self-test tempo near {SELF_TEST['bpm']} BPM (±3)",
                bpm is not None and abs(bpm - SELF_TEST["bpm"]) <= 3, bpm)


def audio_cues(r: Run, media: Path, selftest: bool) -> None:
    wav = wav_of(r, media)
    cues = r.work / "cues.json"
    r.call("audio_cue_mapper", [PY, tool("audio_cue_mapper.py"), str(wav), "--out", str(cues)])
    r.output(cues)
    data = json.loads(cues.read_text(encoding="utf-8"))
    onsets = data.get("onset_candidates_seconds") or data.get("onsets") or []
    energy = data.get("energy_rms") or []
    r.check("energy curve measured", len(energy) > 0, len(energy))
    count = r.steps[-1].get("receipt", {}).get("onset_candidates", len(onsets))
    r.findings.append({"onset_candidates": count, "energy_windows": len(energy)})
    if selftest:
        expect = int(SELF_TEST["seconds"] * SELF_TEST["bpm"] / 60)
        r.check(f"self-test clicks found ({expect} ±1)", abs(count - expect) <= 1, count)


def cinema(r: Run, media: Path, selftest: bool) -> None:
    lab = tool("cinema_lab.py")
    stab, graded, cube, vert = (r.work / n for n in ("stabilized.mp4", "graded.mp4", "look.cube", "vertical.mp4"))
    s = r.call("cinema_lab stabilize", [PY, lab, "stabilize", "--input", str(media), "--output", str(stab)])
    r.call("cinema_lab grade (LUT)", [PY, lab, "grade", "--input", str(media), "--output", str(graded),
                                      "--look", "teal-orange", "--cube-out", str(cube)])
    v = r.call("cinema_lab reframe (vertical, tracked)", [PY, lab, "reframe", "--input", str(media),
                                                           "--output", str(vert)])
    for p in (stab, graded, vert):
        r.output(p, video=True)
    r.output(cube)
    vp = r.outputs[2].get("probe", {}).get("video", {})
    r.check("reframe output is vertical 9:16", vp.get("width") and vp.get("height")
            and abs(vp["width"] / vp["height"] - 9 / 16) < 0.01, f"{vp.get('width')}x{vp.get('height')}")
    before = s.get("receipt", {}).get("shake_before", {}).get("mean_shift_px")
    after = s.get("receipt", {}).get("shake_after", {}).get("mean_shift_px")
    r.findings.append({"shake_mean_px_before": before, "shake_mean_px_after": after,
                       "camera_travel_px": v.get("receipt", {}).get("camera_travel_px")})
    if selftest:
        r.check("self-test shake reduced by stabilize", before is not None and after is not None
                and after < before, f"{before} -> {after}")


def montage(r: Run, media: Path, selftest: bool) -> None:
    mp, job = tool("montage_pro.py"), r.work / "montage-job"
    r.call("montage_pro intake (measure)", [PY, mp, "intake", str(media), "--job", str(job)])
    r.call("montage_pro options", [PY, mp, "options", str(job), "--brief", "montage on the beat"])
    intake = job / "intake.json"
    r.output(intake)
    r.output(job / "options.json")
    data = json.loads(intake.read_text(encoding="utf-8"))
    cues_ok = (data.get("audio_cues") or {}).get("ok")
    r.check("montage_pro measured audio energy cues", bool(cues_ok), cues_ok)
    cue_file = job / "work" / "cues.json"
    if cue_file.is_file():
        # Derived here from montage_pro's own measured RMS curve: calm vs peak sections.
        cues = json.loads(cue_file.read_text(encoding="utf-8"))
        rms, win = cues.get("energy_rms") or [], float(cues.get("window_seconds") or 0.05)
        per = max(1, int(round(1.0 / win)))
        secs = [sum(rms[i:i + per]) / per for i in range(0, len(rms) - per + 1, per)]  # whole seconds only
        if secs:
            ordered = sorted(secs)
            lo, hi = ordered[len(ordered) // 4], ordered[(3 * len(ordered)) // 4]
            r.findings.append({"energy_by_second": [round(x, 4) for x in secs],
                               "calm_seconds": [i for i, x in enumerate(secs) if x <= lo],
                               "peak_seconds": [i for i, x in enumerate(secs) if x >= hi],
                               "use": "calm seconds for quiet shots, peak seconds for the climax",
                               "derived_by": "this adapter, from montage_pro's measured energy_rms"})
    r.findings.append({"loudness": data.get("loudness"), "cuts": (data.get("cuts") or {}).get("count")})


def verify(r: Run, media: Path, selftest: bool) -> None:
    out = r.work / "verify.json"
    # exit 1 means "some delivery checks failed": a finding about the file, not a broken tool.
    r.call("verify_video", [PY, tool("verify_video.py"), str(media), "--json", str(out)], ok_codes=(0, 1))
    r.output(out)
    data = json.loads(out.read_text(encoding="utf-8"))
    checks = data.get("checks") or []
    r.check("delivery checks evaluated", len(checks) > 0, len(checks))
    failed = [c["check"] for c in checks if not c.get("pass")]
    r.findings.append({"delivery_checks": len(checks), "failed": failed})
    if selftest:
        r.check("self-test clip passes the delivery checks it should",
                all("loudness" in f or "peak" in f for f in failed), failed)


def eyes(r: Run, media: Path, selftest: bool) -> None:
    out = r.work / "eyes"
    # exit 3 means "flags raised" (frozen spans, clipping risk): findings about the file, not a broken tool.
    r.call("video_eyes report", [PY, tool("video_eyes.py"), "report", str(media), "--out", str(out)],
           ok_codes=(0, 3))
    for name in ("report.json", "strip.png", "REPORT.md"):
        r.output(out / name)
    if (out / "report.json").is_file():
        r.findings.append({"flags": json.loads((out / "report.json").read_text(encoding="utf-8")).get("flags", [])})
    if selftest:
        r.check("self-test clip has no frozen spans", not any("frozen" in str(f) for f in r.findings[-1]["flags"]),
                r.findings[-1]["flags"])


def look(r: Run, media: Path, selftest: bool) -> None:
    lp, graded = tool("look_pipeline.py"), r.work / "cinematic.mp4"
    step = r.call("look_pipeline verify --all (ffmpeg vs reference maths)", [PY, lp, "verify", "--all"])
    text = step.get("stdout_tail", "")
    r.check("every look matches its reference maths", "FAIL" not in text and "PASS" in text,
            text.count("PASS"))
    r.call("look_pipeline apply cinematic", [PY, lp, "apply", str(media), str(graded), "--preset", "cinematic"])
    r.output(graded, video=True)


def cut(r: Run, media: Path, selftest: bool) -> None:
    out = r.work / "cut.mp4"
    length = probe(media).get("duration") or 0
    start, end = round(length * 0.25, 3), round(length * 0.6, 3)
    r.call("fast_edit cut (exact)", [PY, tool("fast_edit.py"), "cut", "--input", str(media),
                                     "--output", str(out), "--start", str(start), "--end", str(end),
                                     "--mode", "exact"])
    row = r.output(out, video=True)
    got = row.get("probe", {}).get("duration") or 0
    r.check("cut length matches request (±0.1 s)", abs(got - (end - start)) <= 0.1, f"{got} vs {end - start:.3f}")


RUNNERS = {"rhythm": rhythm, "audio-cues": audio_cues, "cinema": cinema, "montage": montage,
           "verify": verify, "eyes": eyes, "look": look, "cut": cut}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recipe", choices=RECIPES)
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--media", default="", help="your video/audio file; empty = self-test clip")
    a = ap.parse_args(argv)
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("ffmpeg and ffprobe are required", file=sys.stderr)
        return 3
    artifact = a.artifact.resolve()
    work = artifact.with_name(artifact.stem + ".work")
    work.mkdir(parents=True, exist_ok=False)
    r = Run(a.recipe, work)
    report = {"schema": SCHEMA, "recipe": a.recipe}
    try:
        if a.media:
            media = Path(a.media).expanduser().resolve()
            if not media.is_file():
                raise RuntimeError(f"media not found: {media}")
            report["input"] = {"kind": "user-media", "path": str(media), "sha256": sha256(media)}
        else:
            media = self_test_clip(work)
            report["input"] = {"kind": "self-test", "path": str(media), "sha256": sha256(media),
                               "known_answers": SELF_TEST,
                               "note": "generated test clip with known answers, NOT your footage"}
        RUNNERS[a.recipe](r, media, not a.media)
        error = None
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        error = str(exc)[:500]
    passed = error is None and bool(r.checks) and all(c["pass"] for c in r.checks)
    report.update(steps=r.steps, outputs=r.outputs, checks=r.checks, findings=r.findings,
                  error=error, verdict="passed" if passed else "failed")
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
