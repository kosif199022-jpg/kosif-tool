"""Build the archival b-roll track (1080x1920, 30 fps) for "مفاتيح الثروة".

Shots come from public-domain archive.org films (see RIGHTS.md). Each story beat has a
pool of hand-picked shots; clips are cut on caption boundaries where possible, graded to
a warm sepia monochrome, framed as a 960x720 "film card" over a blurred copy of itself,
then concatenated with exact frame counts so the track lines up with the voice.

usage: python3 build_broll.py <footage_dir> <shots.json> <captions.js> <out_dir> [--only N]
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

FPS = 30
DURATION = 640.29
CARD = (60, 300, 960, 720)  # x, y, w, h — must match overlay.html

# (beat start in seconds, shot ids). Ids are <film code><index> from the contact sheets.
BEATS = [
    (0.0,   ["WM20", "UB13", "UB12", "WM24"]),                                   # intro: wealth, vaults
    (14.5,  ["ST0", "CU1", "CU2", "ST3", "ST6", "CU16", "ST37", "ST40"]),        # Carnegie: mines and iron
    (28.0,  ["UB18", "SU25", "UB20", "SU31", "UB23"]),                           # the wealthy, dying with wisdom
    (37.4,  ["MB14", "SU8", "MB12", "MB11", "MB17"]),                                    # next generation, a young man
    (56.8,  ["SU24", "SU31", "SU48", "UB21", "SU25", "UB24", "SU45", "UB20", "UB23", "SU33", "SU40"]),   # Hill meets 500 millionaires
    (95.0,  ["MB0", "MB1", "MB3", "MB10", "MB15", "MB4"]),                        # collected, condensed
    (104.9, ["MB48", "MB49", "MB51", "MB54", "MB57", "MB59", "MB60", "MB63", "MB64", "MB71"]),  # the book, millions of copies
    (117.8, ["SU10", "SU8", "SU12", "SU14", "SU15", "SU18", "SU20", "SU22", "SU11", "SU16", "SU36", "UB2", "UB0", "WM1", "WM8"]),  # Bob Proctor, ordinary young man
    (178.0, ["WM28", "WM29", "UB27", "UB29", "UB19", "WM31", "UB31", "WM26"]),           # debt
    (198.0, ["MB57", "MB58", "MB53", "MB59"]),                                   # the miracle is in your hands
    (214.8, ["SU10", "SU22", "SU18"]),                                           # belief
    (226.7, ["MB57", "DY29", "WM7", "DY23", "DY24", "DY31"]),                     # reading, listening in the car
    (253.9, ["UB6", "WM30", "UB26", "UB28"]),                                    # income goal
    (266.0, ["SU20", "UB19", "SU15", "WM29", "SU22", "UB25", "UB30", "SU14", "UB35", "UB37", "WM8", "UB3", "UB9"]),                    # thinking about debt
    (309.0, ["DY17", "DY22", "ST7", "DY1", "DY13", "DY37", "DY12", "DY16", "DY5"]),                      # thinking about success
    (336.0, ["DY9", "DY2", "SU5", "SU6", "SU4", "DY3"]),                          # walking, the sign, cleaning
    (380.0, ["DY37", "DY38", "DY42", "DY43", "DY44", "SU45", "SU46", "SU38"]),    # the company grows
    (402.0, ["MB65", "MB64", "MB71", "WM44", "WM45", "SU23", "SU31"]),            # people bought the book
    (433.0, ["ST37", "ST44", "ST73", "ST90", "CU53"]),                           # persistence
    (446.0, ["UB18", "SU25", "UB23", "SU23"]),                                   # millionaires vs teaching
    (473.6, ["UB17", "UB24", "UB19", "SU24", "SU26", "UB22"]),                    # Nightingale-Conant interview
    (512.0, ["UB6", "SU36", "SU38", "SU45"]),                                    # sales up, the secret
    (526.0, ["MB0", "MB57", "MB59", "MB65", "MB71"]),                            # his book
    (536.0, ["SU31", "SU48", "SU23", "DY22", "DY17"]),                            # teaching people
    (560.0, ["SU45", "SU46", "SU38", "DY23", "ST2", "DY12", "SU47"]),                      # the new program
    (606.0, ["DY1", "DY22", "DY24", "DY17", "ST7", "DY5", "DY16"]),                              # the coach
]

SEPIA = "colorchannelmixer=rr=.393:rg=.769:rb=.189:gr=.349:gg=.686:gb=.168:br=.272:bg=.534:bb=.131"


def load_captions(path):
    txt = open(path, encoding="utf-8").read()
    return json.loads(txt.split("=", 1)[1].strip().rstrip(";"))


def plan(shots, caps):
    bounds = sorted({round(c["start"] - 0.05, 3) for c in caps})
    edges = [b[0] for b in BEATS[1:]] + [DURATION]
    clips, used = [], {}
    for (t0, pool), t1 in zip(BEATS, edges):
        t, k = t0, 0
        while t < t1 - 0.05:
            sid = pool[k % len(pool)]
            s = shots[sid]
            reuse = used.get(sid, 0)
            src_len = s["end"] - s["start"] - 0.6
            # reuse of the same shot starts further in, when the shot is long enough
            off = 0.3 + min(reuse * 4.0, max(0.0, src_len - 3.0))
            avail = s["end"] - 0.3 - (s["start"] + off)
            lo, hi, want = t + 2.4, t + min(avail, 7.0), t + 4.6
            cands = [b for b in bounds if lo <= b <= hi and b < t1 - 1.2]
            end = min(cands, key=lambda b: abs(b - want)) if cands else min(t + min(avail, 6.0), t1)
            if t1 - end < 1.2:
                end = t1 if t1 - t <= avail + 0.01 else end
            end = min(end, t1)
            clips.append({"id": sid, "film": s["film"], "src": round(s["start"] + off, 3),
                          "t0": round(t, 3), "t1": round(end, 3), "move": len(clips) % 4})
            used[sid] = reuse + 1
            t, k = end, k + 1
    # fold clips shorter than 1.6 s into their neighbour (beat edges create slivers)
    merged = []
    for c in clips:
        if merged and c["t1"] - c["t0"] < 1.6:
            merged[-1]["t1"] = c["t1"]
        else:
            merged.append(c)
    clips = merged
    # never run past the end of the source shot: start earlier, or hand the rest to another shot
    fixed = []
    for c in clips:
        s = shots[c["id"]]
        dur = c["t1"] - c["t0"]
        c["src"] = round(min(c["src"], max(s["start"] + 0.3, s["end"] - 0.3 - dur)), 3)
        avail = s["end"] - 0.3 - c["src"]
        if dur > avail + 0.04:
            pool = next(p for b, p in reversed(BEATS) if b <= c["t0"] + 1e-6)
            alt = next(i for i in pool[pool.index(c["id"]) + 1:] + pool if shots[i]["end"] - shots[i]["start"] - 0.6 >= dur - avail and i != c["id"])
            mid = round(c["t0"] + avail, 3)
            fixed.append({**c, "t1": mid})
            c = {**c, "id": alt, "film": shots[alt]["film"], "src": round(shots[alt]["start"] + 0.3, 3), "t0": mid}
        fixed.append(c)
    clips = fixed
    # frame-exact boundaries
    for c in clips:
        c["f0"], c["f1"] = round(c["t0"] * FPS), round(c["t1"] * FPS)
    clips = [c for c in clips if c["f1"] > c["f0"]]
    for a, b in zip(clips, clips[1:]):
        b["f0"] = a["f1"]
    clips[-1]["f1"] = round(DURATION * FPS)
    return clips


def zoom_expr(move, n):
    # 0 push-in, 1 pull-out, 2 pan to the right, 3 pan to the left (all on a 2x upscaled source)
    p = f"(on/{max(n - 1, 1)})"
    if move == 0:
        return f"z='1.0+0.07*{p}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'"
    if move == 1:
        return f"z='1.07-0.07*{p}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'"
    if move == 2:
        return f"z='1.08':x='(iw-iw/zoom)*{p}':y='ih/2-ih/zoom/2'"
    return f"z='1.08':x='(iw-iw/zoom)*(1-{p})':y='ih/2-ih/zoom/2'"


def render_clip(args):
    c, footage, out = args
    n = c["f1"] - c["f0"]
    path = os.path.join(out, f"clip_{c['i']:03d}.mp4")
    if os.path.exists(path):
        return path
    x, y, w, h = CARD
    fg = (f"[0:v]fps={FPS},setsar=1,hue=s=0,{SEPIA},eq=contrast=1.12:brightness=-0.03:gamma=0.95,"
          f"tpad=stop_mode=clone:stop_duration=2,split=2[a][b];"
          f"[a]scale=1440:1920,crop=1080:1920,gblur=sigma=30,eq=brightness=-0.20:saturation=0.85[bg];"
          f"[b]scale=1920:1440:flags=lanczos,zoompan={zoom_expr(c['move'], n)}:d=1:s={w}x{h}:fps={FPS}[card];"
          f"[bg][card]overlay={x}:{y},vignette=angle=PI/4.5,noise=alls=7:allf=t+u,format=yuv420p")
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(c["src"]), "-i", os.path.join(footage, c["film"] + ".mp4"),
           "-filter_complex", fg, "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "15", "-g", "60", "-pix_fmt", "yuv420p", "-r", str(FPS), path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    return path


def main():
    footage, shots_p, caps_p, out = sys.argv[1:5]
    only = int(sys.argv[sys.argv.index("--only") + 1]) if "--only" in sys.argv else None
    shots = json.load(open(shots_p))
    clips = plan(shots, load_captions(caps_p))
    for i, c in enumerate(clips):
        c["i"] = i
    os.makedirs(os.path.join(out, "clips"), exist_ok=True)
    json.dump(clips, open(os.path.join(out, "cuts.json"), "w"), indent=0)
    with open(os.path.join(out, "cuts.js"), "w") as f:
        f.write("window.CUTS=" + json.dumps([[c["f0"] / FPS, c["id"]] for c in clips]) + ";\n")
    print(len(clips), "clips; mean", round(DURATION / len(clips), 2), "s")
    todo = clips if only is None else clips[only:only + 1]
    with ThreadPoolExecutor(4) as ex:
        paths = list(ex.map(render_clip, [(c, footage, os.path.join(out, "clips")) for c in todo]))
    if only is not None:
        print(paths[0]); return
    lst = os.path.join(out, "clips.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in paths))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    os.path.join(out, "broll.mp4")], check=True)
    print("broll.mp4 written")


if __name__ == "__main__":
    main()
