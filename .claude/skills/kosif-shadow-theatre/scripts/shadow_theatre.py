#!/usr/bin/env python3
"""KOSIF Shadow Theatre — analyse a shadow-theatre video, check a scene spec, render stills and the film.

    python3 shadow_theatre.py doctor
    python3 shadow_theatre.py analyze <video> --out <dir>          # cuts, palette, silhouette coverage, contact sheet
    python3 shadow_theatre.py check <scene.json>                   # style grammar + timing rules
    python3 shadow_theatre.py stills <scene.json> --out <dir> [--times 1,4.5,9]
    python3 shadow_theatre.py render <scene.json> --out <film.mp4> [--preview] [--no-audio]
    python3 shadow_theatre.py library                              # poses, props, backdrops, iris shapes

Needs Python 3.10+, numpy, Pillow and ffmpeg (for analyze/render).
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shadow_engine as E  # noqa: E402

REPO = HERE.parents[3]
try:
    sys.path.insert(0, str(REPO / ".claude/skills/kosif-superpowers/scripts"))
    import export_profile as XP  # owner's export standard

    VIDEO_ARGS = XP.video_args()
    FASTSTART = XP.FASTSTART
except Exception:  # standalone copy of the skill
    VIDEO_ARGS = ["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
                  "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
    FASTSTART = ["-movflags", "+faststart"]

TECHNIQUES = {
    "body-build": "several bodies lock together into one object (tree, boat, building, animal)",
    "depth-scale": "an actor moves toward the lamp: the shadow grows and softens (depth > 0.3 somewhere)",
    "iris": "a shaped light window (circle, heart, star, arch) opens or closes the scene",
    "spotlight": "a radial pool of light isolates one or two figures",
    "walk-in": "a figure enters from the edge with a walk cycle",
    "morph": "the same bodies change pose to turn one picture into the next without a cut",
    "prop-cutout": "a prop with punched holes lets light through (windows, lantern, stars)",
    "blackout": "the lamp dims to the unlit cloth between chapters",
}


# --------------------------------------------------------------------------- spec helpers


def load_spec(path: str | Path) -> dict:
    spec = json.loads(Path(path).read_text(encoding="utf-8"))
    for s in spec["scenes"]:
        for a in s.get("actors", []):
            a.setdefault("keys", [{"t": 0}])
            a["keys"] = sorted(a["keys"], key=lambda k: k["t"])
    spec.setdefault("duration", spec["scenes"][-1]["end"])
    return spec


def check_spec(spec: dict) -> list[str]:
    """Return a list of problems; empty means the spec passes."""
    errs = []
    scenes = spec.get("scenes", [])
    if len(scenes) < 3:
        errs.append("need at least 3 scenes (chapters)")
    t = 0.0
    for i, s in enumerate(scenes):
        if abs(s["start"] - t) > 1e-6:
            errs.append(f"scene {i} starts at {s['start']} but the previous ended at {t}: gap or overlap")
        if s["end"] <= s["start"]:
            errs.append(f"scene {i} has no length")
        t = s["end"]
        if not s.get("actors"):
            errs.append(f"scene {i} has no actors: a shadow scene needs a silhouette")
        if s.get("backdrop", "night-blue") not in E.BACKDROPS and not isinstance(s.get("backdrop"), dict):
            errs.append(f"scene {i}: unknown backdrop {s.get('backdrop')!r}")
        for a in s.get("actors", []):
            try:
                if a.get("type", "human") == "human":
                    for k in a.get("keys", []):
                        if "pose" in k:
                            E.resolve_pose(k["pose"])
                    if a.get("costume", "plain") not in E.COSTUMES:
                        errs.append(f"scene {i}: unknown costume {a.get('costume')!r}")
                else:
                    img = Image.new("L", (64, 64))
                    E.draw_prop(img, a["shape"], 32, 32, 20, 0, 0, a.get("params", {}))
            except KeyError as e:
                errs.append(f"scene {i}: {e.args[0]}")
            ks = [k["t"] for k in a.get("keys", [])]
            if ks and (min(ks) < 0 or max(ks) > s["end"] - s["start"] + 1e-6):
                errs.append(f"scene {i}: a key time is outside the scene ({min(ks)}..{max(ks)})")
    if scenes and abs(t - float(spec.get("duration", t))) > 1e-6:
        errs.append(f"scenes end at {t} but duration is {spec.get('duration')}")
    trans = [s.get("transition_in", "blackout") for s in scenes]
    for i in range(1, len(trans)):
        if trans[i] == trans[i - 1] and trans[i] != "blackout":
            errs.append(f"scenes {i - 1} and {i} use the same transition {trans[i]!r} back to back")
    lengths = [round(s["end"] - s["start"], 2) for s in scenes]
    if len(scenes) >= 3 and len(set(lengths)) == 1:
        errs.append("every scene has the same length: vary the pacing")
    used = set()
    for s in scenes:
        used.update(s.get("techniques", []))
        if s.get("iris"):
            used.add("iris")
        if s.get("spot") or E.BACKDROPS.get(s.get("backdrop", ""), {}).get("spot"):
            used.add("spotlight")
        for a in s.get("actors", []):
            if any(float(k.get("depth", 0)) > 0.3 for k in a.get("keys", [])):
                used.add("depth-scale")
            if a.get("cycle", {}).get("type") == "walk":
                used.add("walk-in")
    unknown = used - set(TECHNIQUES)
    if unknown:
        errs.append(f"unknown techniques {sorted(unknown)}")
    if len(used & set(TECHNIQUES)) < 4:
        errs.append(f"only {sorted(used)} used: the style needs at least 4 of {sorted(TECHNIQUES)}")
    if "body-build" not in used:
        errs.append("no body-build moment: the signature of the style is bodies forming one object")
    if not any(s.get("memorable") for s in scenes):
        errs.append("mark one scene memorable: the image the audience keeps")
    return errs


def techniques_used(spec):
    used = set()
    for s in spec["scenes"]:
        used.update(s.get("techniques", []))
    return sorted(used)


# --------------------------------------------------------------------------- audio (original synth score)

NOTE = {"C": -9, "C#": -8, "Db": -8, "D": -7, "D#": -6, "Eb": -6, "E": -5, "F": -4, "F#": -3, "Gb": -3,
        "G": -2, "G#": -1, "Ab": -1, "A": 0, "A#": 1, "Bb": 1, "B": 2}


def hz(name: str) -> float:
    pitch, octv = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((NOTE[pitch] + 12 * (octv - 4)) / 12)


def synth_score(spec: dict, path: Path, sr: int = 48000):
    """A slow pad per chapter plus a low swell on each cue. Original, generated here, no samples."""
    dur = float(spec["duration"])
    n = int(dur * sr)
    t = np.arange(n) / sr
    L = np.zeros(n, np.float32)
    R = np.zeros(n, np.float32)
    default = [["D3", "A3", "D4", "F#4"], ["B2", "F#3", "B3", "D4"], ["G2", "D3", "G3", "B3"], ["A2", "E3", "A3", "C#4"]]
    for i, s in enumerate(spec["scenes"]):
        chord = s.get("chord") or default[i % len(default)]
        a, b = int(s["start"] * sr), min(n, int((s["end"] + 0.8) * sr))
        tt = t[a:b] - s["start"]
        env = np.minimum(1, tt / 1.4) * np.clip((s["end"] + 0.8 - s["start"] - tt) / 1.6, 0, 1)
        trem = 0.85 + 0.15 * np.sin(2 * np.pi * 0.23 * tt + i)
        for j, nm in enumerate(chord):
            f = hz(nm)
            v = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt + 0.3) + 0.12 * np.sin(2 * np.pi * 3 * f * tt)) * 0.06
            L[a:b] += (v * env * trem * (1.0 if j % 2 else 0.8)).astype(np.float32)
            R[a:b] += (np.sin(2 * np.pi * f * 1.003 * tt + 0.5) * 0.06 * env * trem * (0.8 if j % 2 else 1.0)).astype(np.float32)
    for c in [s["start"] for s in spec["scenes"]] + [float(x) for x in spec.get("cues", [])]:
        a = int(c * sr)
        m = min(n - a, int(3.0 * sr))
        if m <= 0:
            continue
        tt = t[:m]
        boom = np.sin(2 * np.pi * (48 + 20 * np.exp(-tt * 6)) * tt) * np.exp(-tt * 2.2) * 0.35
        bell = sum(np.sin(2 * np.pi * 1046.5 * k * tt) * np.exp(-tt * (2.5 + k)) / (k * 6) for k in (1, 2.76, 5.4))
        L[a:a + m] += (boom + bell * 0.8).astype(np.float32)
        R[a:a + m] += (boom + bell).astype(np.float32)
    for d, g in ((0.113, 0.32), (0.229, 0.22), (0.347, 0.15), (0.61, 0.08)):  # small room
        k = int(d * sr)
        L[k:] += R[:-k] * g
        R[k:] += L[:-k] * g
    fade = np.clip((dur - t) / 1.5, 0, 1)
    L, R = L * fade, R * fade
    peak = max(1e-6, float(np.abs(np.concatenate([L, R])).max()))
    st = (np.stack([L, R], 1) / peak * 0.7 * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(st.tobytes())


# --------------------------------------------------------------------------- commands


def cmd_doctor(_):
    rows = {"python": sys.version.split()[0], "numpy": np.__version__, "Pillow": Image.__version__,
            "ffmpeg": shutil.which("ffmpeg") or "MISSING", "ffprobe": shutil.which("ffprobe") or "MISSING",
            "export_profile": "repo" if "XP" in globals() else "built-in fallback"}
    for k, v in rows.items():
        print(f"{k:15} {v}")
    ok = rows["ffmpeg"] != "MISSING"
    print("status         " + ("ready: check, stills, render, analyze" if ok else "stills/check only: install ffmpeg to render"))
    return 0 if ok else 1


def _probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height,r_frame_rate,codec_type",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def cmd_analyze(a):
    """Measure a reference shadow-theatre video: cuts, lit-screen palette, silhouette share, edge softness."""
    src, out = Path(a.video), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    info = _probe(src)
    dur = float(info["format"]["duration"])
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-an", "-vf", f"scale=320:-2,select='gt(scene,{a.threshold})',showinfo",
                        "-f", "null", "-"], capture_output=True, text=True)
    cuts = [round(float(x.split("pts_time:")[1].split()[0]), 2) for x in r.stderr.splitlines() if "pts_time:" in x]
    step = max(0.5, dur / a.samples)
    times = [round(i * step, 2) for i in range(int(dur / step))]
    samples = []
    for tt in times:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(tt), "-i", str(src), "-frames:v", "1", "-vf", "scale=320:180",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        if len(raw) < 320 * 180 * 3:
            continue
        f = np.frombuffer(raw, np.uint8).reshape(180, 320, 3).astype(np.float32)
        lum = f.mean(2)
        lit = lum > 60  # the projected screen
        dark_inside = (lum < 35)[30:150, 50:270]
        bright = f[lit]
        # silhouette shot heuristic: a large bright screen whose middle has hard dark regions
        is_shadow = lit.mean() > 0.25 and 0.04 < dark_inside.mean() < 0.75
        gy, gx = np.gradient(lum)
        g = np.hypot(gx, gy)
        edges = g[(g > 25)]
        samples.append({
            "t": tt, "shadow_shot": bool(is_shadow), "lit_share": round(float(lit.mean()), 3),
            "silhouette_share": round(float(dark_inside.mean()), 3),
            "screen_rgb_top": [int(v) for v in f[20:60, 120:200].reshape(-1, 3).mean(0)],
            "screen_rgb_mid": [int(v) for v in f[80:110, 120:200].reshape(-1, 3).mean(0)],
            "screen_mean_rgb": [int(v) for v in bright.mean(0)] if bright.size else None,
            "edge_strength": round(float(edges.mean()), 1) if edges.size else 0.0,
        })
    shadow = [s for s in samples if s["shadow_shot"]]
    summary = {
        "schema": "kosif.shadow-theatre.analysis.v1", "source": src.name, "duration_s": round(dur, 2),
        "camera_cuts": cuts, "samples": len(samples), "shadow_shot_share": round(len(shadow) / max(1, len(samples)), 3),
        "mean_silhouette_share": round(float(np.mean([s["silhouette_share"] for s in shadow])), 3) if shadow else None,
        "palette_top": [s["screen_rgb_top"] for s in shadow][:: max(1, len(shadow) // 8)],
        "notes": "cuts are camera/edit cuts; inside the act the picture changes by morph, blackout and iris, not by cuts",
    }
    (out / "analysis.json").write_text(json.dumps({"summary": summary, "samples": samples}, indent=2), encoding="utf-8")
    sheet = out / "contact.jpg"
    cols = 6
    rows = math.ceil(min(36, len(times)) / cols)
    every = max(1.0, dur / (cols * rows))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", f"fps=1/{every:.3f},scale=320:-2,tile={cols}x{rows}",
                    "-frames:v", "1", str(sheet)], check=False)
    print(json.dumps(summary, indent=2))
    print(f"wrote {out / 'analysis.json'} and {sheet}")
    return 0


def cmd_check(a):
    spec = load_spec(a.scene)
    errs = check_spec(spec)
    if errs:
        for e in errs:
            print("FAIL", e)
        return 1
    print(f"PASS {len(spec['scenes'])} scenes, {spec['duration']}s, techniques: {', '.join(techniques_used(spec))}")
    return 0


def _renderer(spec, preview):
    if preview:
        spec = dict(spec, width=spec.get("width", 1080) // 2, height=spec.get("height", 1920) // 2, fps=min(15, spec.get("fps", 30)))
    return E.ShadowRenderer(spec), spec


def cmd_stills(a):
    spec = load_spec(a.scene)
    rnd, spec = _renderer(spec, a.preview)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    times = [float(x) for x in a.times.split(",")] if a.times else [round((s["start"] + s["end"]) / 2, 2) for s in spec["scenes"]]
    paths = []
    for tt in times:
        p = out / f"still_{tt:06.2f}.png"
        Image.fromarray(rnd.render(tt).rgb).save(p)
        paths.append(p)
        print(p)
    if len(paths) > 1:
        ims = [Image.open(p) for p in paths]
        w, h = ims[0].size
        k = 480 / w
        tw, th = int(w * k), int(h * k)
        sheet = Image.new("RGB", (tw * len(ims), th))
        for i, im in enumerate(ims):
            sheet.paste(im.resize((tw, th)), (i * tw, 0))
        sheet.save(out / "stills_sheet.jpg", quality=88)
        print(out / "stills_sheet.jpg")
    return 0


def cmd_render(a):
    spec = load_spec(a.scene)
    errs = check_spec(spec)
    if errs and not a.force:
        for e in errs:
            print("FAIL", e)
        print("fix the spec or pass --force")
        return 1
    rnd, spec = _renderer(spec, a.preview)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fps = spec.get("fps", 30)
    n = int(round(float(spec["duration"]) * fps))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{rnd.W}x{rnd.H}", "-r", str(fps), "-i", "-"]
    wav = None
    if not a.no_audio:
        wav = out.with_suffix(".score.wav")
        synth_score(spec, wav)
        cmd += ["-i", str(wav)]
    cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv", *VIDEO_ARGS]
    if wav:
        cmd += ["-c:a", "aac", "-b:a", "320k", "-shortest"]  # mixed synth track -> AAC 320k per the export standard
    cmd += [*FASTSTART, str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        proc.stdin.write(rnd.render(i / fps).rgb.tobytes())
        if i % max(1, n // 10) == 0:
            print(f"frame {i}/{n}", flush=True)
    proc.stdin.close()
    rc = proc.wait()
    if wav and not a.keep_wav:
        wav.unlink(missing_ok=True)
    if rc:
        print("ffmpeg failed", rc)
        return rc
    info = _probe(out)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    print(json.dumps({"out": str(out), "width": v["width"], "height": v["height"], "fps": v["r_frame_rate"],
                      "duration": round(float(info["format"]["duration"]), 2),
                      "audio": any(s["codec_type"] == "audio" for s in info["streams"])}))
    return 0


def cmd_library(_):
    print("poses:     " + ", ".join(sorted(E.POSES)))
    print("costumes:  " + ", ".join(sorted(E.COSTUMES)))
    print("cycles:    walk, sway, wave, breathe, flutter")
    print("props:     sun, crescent, bird, palm, skyline, dunes, waves, lantern, hand, circle, heart, star, arch")
    print("iris:      circle, heart, star, arch")
    print("backdrops: " + ", ".join(E.BACKDROPS))
    print("easing:    " + ", ".join(E.EASES))
    print("techniques:")
    for k, v in TECHNIQUES.items():
        print(f"  {k:12} {v}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    sub.add_parser("library")
    s = sub.add_parser("analyze")
    s.add_argument("video")
    s.add_argument("--out", required=True)
    s.add_argument("--samples", type=int, default=60)
    s.add_argument("--threshold", type=float, default=0.35)
    s = sub.add_parser("check")
    s.add_argument("scene")
    s = sub.add_parser("stills")
    s.add_argument("scene")
    s.add_argument("--out", required=True)
    s.add_argument("--times")
    s.add_argument("--preview", action="store_true")
    s = sub.add_parser("render")
    s.add_argument("scene")
    s.add_argument("--out", required=True)
    s.add_argument("--preview", action="store_true", help="half size, 15 fps")
    s.add_argument("--no-audio", action="store_true")
    s.add_argument("--keep-wav", action="store_true")
    s.add_argument("--force", action="store_true")
    a = p.parse_args(argv)
    return {"doctor": cmd_doctor, "library": cmd_library, "analyze": cmd_analyze, "check": cmd_check,
            "stills": cmd_stills, "render": cmd_render}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
