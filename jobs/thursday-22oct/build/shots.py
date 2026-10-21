"""Shot list for the Thursday dua film: cut on each phrase onset, extract arch + blurred-bg frames."""
import json, subprocess, sys, pathlib
J = pathlib.Path(__file__).resolve().parents[1]
FPS, END, HANDLE, LEAD = 30, 24.867, 0.3, 0.08
# (phrase onset s, mixkit id, source in-point s, horizontal crop centre 0..1)
SHOTS = [
    (0.00, 9998, 6, .55), (2.14, 6850, 4, .5), (4.90, 34223, 3.2, .28), (6.54, 11922, 5, .42),
    (9.42, 9805, 4, .5), (10.86, 21168, 3, .62), (13.50, 21114, 4, .62), (15.60, 34189, 4, .5),
    (17.14, 22166, 6, .3), (18.82, 34251, 5, .5), (20.46, 4312, 1, .5), (21.60, 17255, 8, .5),
    (23.30, 9736, 5, .6),
]
GRADE = "eq=contrast=1.06:saturation=1.12:gamma=0.98,colorbalance=rm=0.04:bm=-0.04:rh=0.03:bh=-0.03"
AW, AH = 946, 1078          # arch window 860x980 with 10% room for the slow push
out = []
for i, (t, cid, inp, cx) in enumerate(SHOTS):
    cut = max(0.0, t - LEAD) if i else 0.0
    nxt = SHOTS[i + 1][0] - LEAD if i + 1 < len(SHOTS) else END
    a, b = max(0.0, cut - HANDLE), min(END, nxt + HANDLE)
    src = J / "stock" / (f"hd_{cid}.mp4" if cid == 4312 else f"{cid}.mp4")
    d = J / "build" / "frames" / f"s{i:02d}"; d.mkdir(parents=True, exist_ok=True)
    n = round((b - a) * FPS)
    ss = inp + (a - cut)
    if ss < 0: ss = 0
    # sharp arch crop (from a 720-high source: 632 wide), then the blurred full-bleed backdrop
    arch = (f"scale=-2:720,{GRADE},crop=632:720:'min(max(0,iw*{cx}-316),iw-632)':0,"
            f"scale={AW}:{AH}:flags=lanczos,unsharp=5:5:0.6")
    bg = f"scale=-2:480,{GRADE},crop=270:480:'(iw-270)/2':0,boxblur=10:2"
    for name, vf, q in (("a", arch, 3), ("b", bg, 5)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-i", str(src), "-frames:v", str(n),
                        "-vf", f"fps={FPS},{vf}", "-q:v", str(q), str(d / f"{name}_%04d.jpg")], check=True)
    have = len(list(d.glob("a_*.jpg")))
    out.append({"i": i, "id": cid, "cut": round(cut, 3), "next": round(nxt, 3), "from": round(a, 3), "frames": have})
    print(i, cid, f"{a:.2f}-{b:.2f}", have, "frames", file=sys.stderr)
json.dump({"fps": FPS, "end": END, "shots": out}, open(J / "build" / "shots.json", "w"), indent=1)
