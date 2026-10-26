"""Stand-ins for Pinterest downloads: for every reference shot kind, a few clips with the same 'vibe'
(same generator, different seed/hue/size) plus decoys (other kinds, low resolution, burned-in text).

    python make_candidates.py OUT_DIR
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from synth import GENERATORS  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"

PLAN = [
    # name, kind, kwargs, (w, h), seconds, note
    ("pin_clouds_a", "clouds", {"seed": 21, "hue": (90, 140, 215)}, (720, 1280), 6.0, "good"),
    ("pin_clouds_b", "clouds", {"seed": 22, "hue": (210, 140, 160)}, (1080, 1920), 5.0, "pinkish"),
    ("pin_bokeh_a", "bokeh", {"seed": 23, "col": (255, 200, 110)}, (1080, 1920), 6.0, "good"),
    ("pin_bokeh_land", "bokeh", {"seed": 24, "col": (255, 170, 80)}, (1280, 720), 7.0, "landscape"),
    ("pin_rain_a", "rain", {"seed": 25}, (720, 1280), 6.0, "good"),
    ("pin_rain_lowres", "rain", {"seed": 26}, (270, 480), 6.0, "low resolution decoy"),
    ("pin_sunset_a", "sunset", {"seed": 27, "mid": (250, 140, 80)}, (1080, 1920), 6.0, "good"),
    ("pin_blossoms_a", "blossoms", {"seed": 28}, (720, 1280), 5.0, "good"),
    ("pin_blossoms_text", "blossoms", {"seed": 29}, (720, 1280), 5.0, "burned-in text decoy"),
    ("pin_candle_a", "candle", {"seed": 30}, (1080, 1920), 6.0, "good"),
    ("pin_candle_short", "candle", {"seed": 31}, (720, 1280), 1.6, "too short"),
]


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    meta = []
    for name, kind, kw, (w, h), secs, note in PLAN:
        fn = GENERATORS[kind](w, h, **kw)
        n = int(secs * 30)
        path = out / f"{name}.mp4"
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                              "-framerate", "30", "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                              "-pix_fmt", "yuv420p", str(path)], stdin=subprocess.PIPE)
        font = None
        if "text" in note:
            font = ImageFont.truetype(str(ASSETS / "fonts" / "Cairo-700.ttf"), int(w * 0.07),
                                      layout_engine=ImageFont.Layout.RAQM)
        for i in range(n):
            fr = fn(i)
            if font is not None:
                im = Image.fromarray(fr)
                ImageDraw.Draw(im).text((w // 2, int(h * 0.8)), "صباح الخير", font=font, fill=(255, 255, 255),
                                        anchor="mm", direction="rtl", language="ar")
                fr = np.asarray(im)
            p.stdin.write(fr.tobytes())
        p.stdin.close()
        p.wait()
        meta.append({"file": path.name, "kind": kind, "w": w, "h": h, "seconds": secs, "note": note})
        print("wrote", path.name)
    (out / "candidates.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
