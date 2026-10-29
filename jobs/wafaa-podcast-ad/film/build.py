#!/usr/bin/env python3
"""Build the three cuts of the «الحكاية فيها إنّ» launch ad.

Run from the job folder that holds ad.html, fonts/, assets/logo.jpg, voice/ and
scenes/s1.mp4..s4.mp4:

    python3 build.py frames          # scene clips -> 1080x1920 JPG frames at 30 fps
    python3 build.py config <cut>    # write config.js for cut 30|15|6
    python3 build.py all             # frames + render every cut into out/

Rendering uses render_html.cjs (seek driver) with the cut's voice-over
stream-copied, then re-checks duration, size and fps with ffprobe.
"""
import json, os, subprocess, sys

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))

# scene windows in seconds on each cut's timeline; "s" = scene clip number
CUTS = {
    "30": {"voice": "voice/vo_full_take2.m4a", "words": "voice/timing.json", "duration": 26.0,
           "card": 20.45,
           "scenes": [("s1", 0.0, 6.3), ("s2", 6.3, 10.2), ("s3", 10.2, 17.2), ("s4", 17.2, 26.0)]},
    "15": {"voice": "voice/vo_15s.m4a", "words": "voice/timing_15s.json", "duration": 15.0,
           "card": 11.8,
           "scenes": [("s1", 0.0, 4.5), ("s2", 4.5, 6.05), ("s3", 6.05, 9.0), ("s4", 9.0, 15.0)]},
    "6":  {"voice": "voice/vo_6s.m4a", "words": "voice/timing_6s.json", "duration": 6.0,
           "card": 4.2,
           "scenes": [("s3", 0.0, 2.3), ("s4", 2.3, 6.0)]},
}


def run(cmd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def frames():
    for n in range(1, 5):
        src = os.path.join(HERE, "scenes", f"s{n}.mp4")
        out = os.path.join(HERE, "frames", f"s{n}")
        if not os.path.exists(src):
            print("missing", src); continue
        os.makedirs(out, exist_ok=True)
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf",
             f"fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920",
             "-q:v", "2", os.path.join(out, "f_%04d.jpg")])


def count(d):
    p = os.path.join(HERE, "frames", d)
    return len([f for f in os.listdir(p) if f.endswith(".jpg")]) if os.path.isdir(p) else 0


def config(cut):
    c = CUTS[cut]
    words = json.load(open(os.path.join(HERE, c["words"])))
    fix = {"إن": "إنّ", "جواه": "جوّاه", "استنوني": "استنّوني"}
    for w in words:
        w["w"] = fix.get(w["w"], w["w"])
    words = [w for w in words if w["s"] < c["card"]]
    scenes = [{"dir": f"frames/{s}", "frames": count(s), "start": a, "end": b, "from": 0}
              for s, a, b in c["scenes"]]
    cfg = {"duration": c["duration"], "fps": FPS, "words": words, "scenes": scenes,
           "card": {"start": c["card"]}}
    open(os.path.join(HERE, "config.js"), "w").write("window.CONFIG=" + json.dumps(cfg, ensure_ascii=False) + ";")
    return c


def render(cut, preview=False):
    c = config(cut)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    out = os.path.join(HERE, "out", f"hekaya_{cut}s.mp4")
    cmd = ["node", os.path.join(HERE, "render_html.cjs"), "--in", os.path.join(HERE, "ad.html"),
           "--out", out, "--mode", "seek", "--fps", str(FPS), "--duration", str(c["duration"]),
           "--width", "1080", "--height", "1920", "--crf", "17",
           "--audio", os.path.join(HERE, c["voice"])]
    if preview:
        cmd.append("--preview")
    run(cmd)
    return out


if __name__ == "__main__":
    a = sys.argv[1:] or ["all"]
    if a[0] == "frames":
        frames()
    elif a[0] == "config":
        config(a[1])
    elif a[0] == "preview":
        render(a[1], preview=True)
    elif a[0] == "render":
        render(a[1])
    elif a[0] == "all":
        frames()
        for cut in ("30", "15", "6"):
            render(cut)
