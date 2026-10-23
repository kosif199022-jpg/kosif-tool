"""Shot list for «مطر الرحمة»: day sky → Kaaba → night under heavier rain → calm → light. Cut on phrase onsets."""
import json, subprocess, sys, pathlib
J = pathlib.Path(__file__).resolve().parents[1]
FPS, END, HANDLE, LEAD = 30, 46.9, 0.5, 0.1
# (onset, pexels id, in-point s, zoom ≥1, vertical centre 0..1, transition)
SHOTS = [
    (0.00, 20324052, 1.0, 1.00, .50, "fade"), (2.36, 35155732, 1.0, 1.00, .50, "dissolve"),
    (5.14, 35325576, 2.0, 1.25, .38, "dissolve"), (7.14, 35189276, 0.5, 1.00, .50, "dissolve"),
    (9.06, 9112700, 0.5, 1.00, .50, "dissolve"), (11.04, 27411329, 1.0, 1.35, .33, "dissolve"),
    (14.14, 20525447, 2.0, 1.00, .50, "dissolve"), (17.06, 35155761, 0.5, 1.00, .50, "glass"),
    (19.20, 34683762, 0.5, 1.00, .50, "dissolve"), (21.18, 34444589, 2.0, 1.25, .22, "dissolve"),
    (23.30, 35189259, 0.5, 1.00, .50, "dissolve"), (25.24, 34683762, 5.0, 1.15, .45, "dissolve"),
    (27.84, 34444589, 7.0, 1.25, .22, "dissolve"), (32.86, 35155761, 4.5, 1.15, .45, "dissolve"),
    (35.12, 35189259, 5.0, 1.10, .50, "dissolve"), (36.96, 34683762, 3.5, 1.20, .45, "dissolve"),
    (39.98, 20324052, 7.0, 1.10, .50, "glass"), (43.42, 35155732, 7.0, 1.10, .45, "dissolve"),
]
GRADE = "eq=contrast=1.05:saturation=0.92:gamma=0.97,colorbalance=bs=0.05:rs=-0.02:rh=0.05:bh=-0.03"
FW, FH = 1188, 2112
out = []
for i, (t, cid, inp, z, cy, tr) in enumerate(SHOTS):
    cut = max(0.0, t - LEAD) if i else 0.0
    nxt = SHOTS[i + 1][0] - LEAD if i + 1 < len(SHOTS) else END
    a, b = max(0.0, cut - HANDLE), min(END, nxt + HANDLE)
    n = round((b - a) * FPS); ss = max(0.0, inp + (a - cut))
    src = J / "stock" / f"{cid}.mp4"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                               capture_output=True, text=True).stdout)
    loop = ["-stream_loop", "-1"] if ss + n / FPS > dur else []   # short clips loop rather than freeze
    if ss >= dur: ss = 0.0
    vf = (f"fps={FPS},scale={round(FW * z)}:{round(FH * z)}:force_original_aspect_ratio=increase:flags=lanczos,"
          f"crop={FW}:{FH}:(iw-{FW})/2:'min(max(0,ih*{cy}-{FH}/2),ih-{FH})',{GRADE}")
    d = J / "build" / "frames" / f"s{i:02d}"; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", *loop, "-ss", f"{ss:.3f}", "-i", str(src), "-frames:v", str(n),
                    "-vf", vf, "-q:v", "3", str(d / "a_%04d.jpg")], check=True)
    have = len(list(d.glob("a_*.jpg")))
    out.append({"i": i, "id": cid, "cut": round(cut, 3), "next": round(nxt, 3), "from": round(a, 3), "frames": have, "tr": tr})
    print(i, cid, f"{a:.2f}-{b:.2f}", have, file=sys.stderr)
# real rain: rain-on-black, vertical crop, grey, looped in the page
r = J / "build" / "frames" / "rain"; r.mkdir(parents=True, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(J / "stock" / "36344044.mp4"), "-vf",
                "fps=30,crop=1215:2160:(iw-1215)/2:0,scale=540:960,format=gray,eq=contrast=1.4:brightness=-0.04",
                "-q:v", "4", str(r / "r_%04d.jpg")], check=True)
json.dump({"fps": FPS, "end": END, "rainFrames": len(list(r.glob("r_*.jpg"))), "shots": out},
          open(J / "build" / "shots.json", "w"), indent=1)
