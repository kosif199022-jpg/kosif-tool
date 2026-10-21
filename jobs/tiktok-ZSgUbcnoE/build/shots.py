"""Shot list for the second Thursday dua: one clear shot per phrase, cut on the phrase onset.
Each shot is cropped to the 1080x1000 panel (no blur, no wash) with room for a slow push."""
import json, subprocess, sys, pathlib
J = pathlib.Path(__file__).resolve().parents[1]
FPS, END, HANDLE, LEAD = 30, 27.1, 0.4, 0.06
# (phrase onset s, clip, source in-point s, horizontal crop centre 0..1, transition into this shot)
SHOTS = [
    (0.00, "9998", 4, .55, "open"), (3.36, "34223", 3.0, .33, "zoom"), (4.44, "34208", 3, .45, "star"),
    (6.80, "31629", 4, .62, "sweep"), (9.78, "34251", 5, .5, "push"), (13.34, "30867", 0.2, .5, "doors"),
    (15.86, "22166", 6, .35, "dissolve"), (17.68, "21168", 3, .6, "lightwave"), (20.26, "25375", 5, .45, "rain"),
    (23.40, "11926", 8, .55, "dissolve"), (25.06, "hd_4312", 1, .5, "bloom"),
]
GRADE = "eq=contrast=1.03:saturation=1.06"
PW, PH = 1188, 1100   # panel 1080x1000 plus 10% for the push
out = []
for i, (t, cid, inp, cx, tr) in enumerate(SHOTS):
    cut = max(0.0, t - LEAD) if i else 0.0
    nxt = SHOTS[i + 1][0] - LEAD if i + 1 < len(SHOTS) else END
    a, b = max(0.0, cut - HANDLE), min(END, nxt + HANDLE)
    d = J / "build" / "frames" / f"s{i:02d}"; d.mkdir(parents=True, exist_ok=True)
    n = round((b - a) * FPS)
    ss = max(0.0, inp + (a - cut))
    cw = round(720 * 1080 / 1000)  # 778 px of a 720-high source fills the panel
    vf = (f"fps={FPS},scale=-2:720:flags=lanczos,{GRADE},crop={cw}:720:'min(max(0,iw*{cx}-{cw}/2),iw-{cw})':0,"
          f"scale={PW}:{PH}:flags=lanczos,unsharp=5:5:0.5")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-i", str(J / "stock" / f"{cid}.mp4"),
                    "-frames:v", str(n), "-vf", vf, "-q:v", "2", str(d / "a_%04d.jpg")], check=True)
    have = len(list(d.glob("a_*.jpg")))
    out.append({"i": i, "id": cid, "cut": round(cut, 3), "next": round(nxt, 3), "from": round(a, 3), "frames": have, "tr": tr})
    print(i, cid, f"{a:.2f}-{b:.2f}", have, file=sys.stderr)
json.dump({"fps": FPS, "end": END, "shots": out}, open(J / "build" / "shots.json", "w"), indent=1)
