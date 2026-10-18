#!/usr/bin/env python3
"""Make original stand-in assets for the «الدعاء» kit proof: 8 warm bokeh stills and a quiet stand-in tone.

    python3 make_demo_assets.py <out-dir>

Writes <out-dir>/shots/01..08.jpg (1080×1920), <out-dir>/voice_standin.m4a (15.4 s AAC) and
<out-dir>/project.json (the 8 dua lines with the measured phrase timings). Nothing here comes from the reference reel.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
# per-shot base gradient (top, bottom) inside the measured Lab range of the style: warm low-key
BASES = [((70, 46, 34), (22, 14, 10)), ((150, 80, 60), (60, 32, 24)), ((110, 70, 50), (40, 24, 16)),
         ((60, 40, 30), (20, 12, 8)), ((120, 105, 95), (50, 42, 38)), ((180, 110, 50), (70, 40, 20)),
         ((150, 30, 35), (70, 14, 18)), ((190, 120, 60), (90, 50, 25))]
BOKEH = [(255, 210, 140), (255, 180, 120), (240, 200, 170), (255, 225, 170), (230, 150, 110)]


def still(i: int) -> Image.Image:
    rng = np.random.default_rng(1000 + i)
    top, bot = BASES[i]
    y = np.linspace(0, 1, H)[:, None, None]
    img = (np.array(top) * (1 - y) + np.array(bot) * y) * np.ones((1, W, 1))
    base = Image.fromarray(img.astype(np.uint8), "RGB")
    layer = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(int(rng.integers(40, 70))):
        r = int(rng.integers(30, 120))
        x, yy = int(rng.integers(-60, W + 60)), int(rng.integers(int(H * 0.35), H + 60))
        c = BOKEH[int(rng.integers(len(BOKEH)))]
        k = float(rng.uniform(0.25, 0.7))
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=tuple(int(v * k) for v in c))
    layer = layer.filter(ImageFilter.GaussianBlur(14))
    out = np.clip(np.asarray(base, np.float32) + np.asarray(layer, np.float32) * 0.8, 0, 255)
    return Image.fromarray(out.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))


def main(out: Path) -> None:
    (out / "shots").mkdir(parents=True, exist_ok=True)
    for i in range(8):
        still(i).save(out / "shots" / f"{i + 1:02d}.jpg", quality=92)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=220:duration=15.4:sample_rate=44100",
                    "-af", "volume=0.05", "-ac", "2", "-c:a", "aac", "-b:a", "128k", str(out / "voice_standin.m4a")], check=True)
    ex = json.loads((Path(__file__).resolve().parents[5] / "styles/dua/kit/example/project.json").read_text(encoding="utf-8"))
    ex.update(clips=[f"shots/{i:02d}.jpg" for i in range(1, 9)], audio="voice_standin.m4a")
    (out / "project.json").write_text(json.dumps(ex, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", out)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
