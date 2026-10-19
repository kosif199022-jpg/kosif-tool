"""Find the usable (non-faded) part of every pooled shot.

Samples luma at 5 fps over each shot and keeps the longest run whose mean luma stays
above max(floor, 60% of the shot's median) — fades through black dip far below the
median even when they never reach true black — and does not jump (a jump means a dissolve/second shot the cut detector
missed). Writes data/shot_trims.json, which build_broll.py applies on top of shots.json.

usage: python3 scan_shots.py <footage_dir> <shots.json> <out.json>
"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import build_broll as B

FLOOR, JUMP, STEP = 22.0, 30.0, 0.2


def lumas(film, a, b):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", film,
                        "-vf", f"fps={1 / STEP:.0f},scale=64:48,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
                        "-f", "null", "-"], capture_output=True, text=True)
    return [float(l.split("=")[1]) for l in r.stderr.splitlines() + r.stdout.splitlines() if "YAVG=" in l]


def scan(args):
    sid, s, footage = args
    ys = lumas(f"{footage}/{s['film']}.mp4", s["start"], s["end"])
    floor = max(FLOOR, 0.6 * sorted(ys)[len(ys) // 2]) if ys else FLOOR
    best, cur = (0, 0), None
    for i, y in enumerate(ys):
        ok = y >= floor and (i == 0 or abs(y - ys[i - 1]) < JUMP)
        if ok:
            cur = (cur[0], i + 1) if cur and (i == 0 or abs(y - ys[i - 1]) < JUMP) else (i, i + 1)
            if cur[1] - cur[0] > best[1] - best[0]:
                best = cur
        else:
            cur = (i, i + 1) if y >= floor else None
    a = s["start"] + best[0] * STEP
    b = s["start"] + best[1] * STEP
    return sid, round(a, 2), round(b, 2), round(min(ys) if ys else 0, 1)


if __name__ == "__main__":
    footage, shots_p, out = sys.argv[1:4]
    shots = json.load(open(shots_p))
    ids = sorted({i for _, pool in B.BEATS for i in pool})
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(scan, [(i, shots[i], footage) for i in ids]))
    trims = {}
    for sid, a, b, ymin in res:
        s = shots[sid]
        if a > s["start"] + 0.25 or b < s["end"] - 0.25:
            trims[sid] = [a, b]
            print(f"{sid:6s} {s['start']:.1f}-{s['end']:.1f} -> {a:.1f}-{b:.1f} (min luma {ymin})")
    json.dump(trims, open(out, "w"), indent=0)
    print(len(trims), "of", len(ids), "shots trimmed")
