#!/usr/bin/env python3
"""Build the Aghnam Alwadi ads in the Higgsfield sandbox.

Layout (sandbox): ~/wadi/film/ holds this file, wadi.html, shots.json, fonts/, voice/, assets/logo.png,
render_html.cjs; ~/wadi/raw/ holds the downloaded clips; ~/wadi/music/<id>.mp3 the Mixkit tracks.

  python3 build.py frames v1      # extract the frames each shot needs
  python3 build.py config v1      # write config.js for v1
  python3 build.py audio v1       # mixed track (voice + ducked music, -14 LUFS)
  python3 build.py render v1 [music|voice] [--preview]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/wadi/raw")
MUSIC = os.path.expanduser("~/wadi/music")
FPS = 30
TAG = {"v1": "الطازج اللي يستاهلك", "v2": "ذبيحتك على كيفك… اطلب الحين", "v3": "لعزايمكم اللي تستاهل"}


def run(cmd):
    print("+", " ".join(cmd)[:200], flush=True)
    subprocess.run(cmd, check=True)


def plan(v):
    return json.load(open(os.path.join(HERE, "shots.json")))[v]


def frames(v):
    p = plan(v)
    for i, s in enumerate(p["shots"]):
        if s["clip"].startswith("@"):
            continue
        out = os.path.join(HERE, "frames", v, f"s{i:02d}")
        os.makedirs(out, exist_ok=True)
        dur = s["t1"] - s["t0"] + 0.1
        if s["mode"] == "fill":
            vf = f"fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920"
        else:
            vf = f"fps={FPS},scale=1000:562:force_original_aspect_ratio=increase:flags=lanczos,crop=1000:562"
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(s["from"]), "-t", f"{dur:.3f}", "-i",
             os.path.join(RAW, s["clip"] + ".mp4"), "-vf", vf, "-q:v", "3", os.path.join(out, "f_%04d.jpg")])


def config(v):
    p = plan(v)
    tm = json.load(open(os.path.join(HERE, "voice", f"timing_{v}.json")))
    shots = []
    for i, s in enumerate(p["shots"]):
        d = dict(s)
        if not s["clip"].startswith("@"):
            fdir = os.path.join(HERE, "frames", v, f"s{i:02d}")
            d["dir"] = f"frames/{v}/s{i:02d}"
            d["frames"] = len([f for f in os.listdir(fdir) if f.endswith(".jpg")])
        shots.append(d)
    words = tm["words"]
    cfg = {"duration": p["duration"], "fps": FPS, "words": words, "shots": shots, "badges": p["badges"],
           "card": p["card"], "tag": TAG[v], "nocap": p.get("nocap", [])}
    open(os.path.join(HERE, "config.js"), "w").write("window.CONFIG=" + json.dumps(cfg, ensure_ascii=False) + ";")


def audio(v):
    p = plan(v)
    D = p["duration"]
    vo = os.path.join(HERE, "voice", f"{v}.m4a")
    mu = os.path.join(MUSIC, p["music"] + ".mp3")
    out = os.path.join(HERE, "out", f"{v}_mix.m4a")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fc = (f"[0:a]aresample=48000,apad=whole_dur={D},asplit=2[vo][sc];"
          f"[1:a]aresample=48000,atrim=0:{D},afade=t=in:st=0:d=0.6,afade=t=out:st={D-1.8}:d=1.8,volume=0.42[m];"
          f"[m][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[md];"
          f"[vo][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    run(["ffmpeg", "-v", "error", "-y", "-i", vo, "-i", mu, "-filter_complex", fc, "-map", "[a]",
         "-t", str(D), "-ar", "48000", "-c:a", "aac", "-b:a", "320k", out])
    return out


def render(v, kind="music", preview=False):
    config(v)
    p = plan(v)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    a = audio(v) if kind == "music" else os.path.join(HERE, "voice", f"{v}.m4a")
    out = os.path.join(HERE, "out", f"aghnam_alwadi_{v}_{kind}.mp4")
    cmd = ["node", os.path.join(HERE, "render_html.cjs"), "--in", os.path.join(HERE, "wadi.html"), "--out", out,
           "--mode", "seek", "--fps", str(FPS), "--duration", str(p["duration"]), "--width", "1080", "--height", "1920",
           "--crf", "17", "--audio", a]
    if preview:
        cmd.append("--preview")
    run(cmd)


if __name__ == "__main__":
    a = sys.argv[1:]
    {"frames": lambda: frames(a[1]), "config": lambda: config(a[1]), "audio": lambda: audio(a[1]),
     "render": lambda: render(a[1], a[2] if len(a) > 2 and not a[2].startswith("--") else "music", "--preview" in a)}[a[0]]()
