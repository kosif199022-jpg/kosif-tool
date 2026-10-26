"""Any image -> a standalone Python program (Pillow only) that makes the same image again, pixel for pixel.

The program has two parts:
  1. drawing  - the picture's colour regions as draw.polygon(...) calls, largest first (readable and editable:
                change a fill colour or a shape and run it again)
  2. details  - the original picture's own bytes are embedded; whatever pixel the drawing did not get exactly
                right is taken from them, so the saved file is identical to the original (it checks itself)

Run it anywhere with `python name.py` -> writes name.png. Opened in KOSIF Studio (📝 كود) it is painted step by
step and checked against the original; the studio only reads its data and does not execute it.
"""
from __future__ import annotations

import base64
import math
from pathlib import Path

from PIL import Image

import vectorize as V

TEMPLATE = '''# -*- coding: utf-8 -*-
"""KOSIF Studio image program (Pillow only).

    python {stem}.py
    -> writes {stem}.png, identical to the original ({w}x{h}), and checks that itself.

الجزء الأول يرسم أشكال الصورة بألوانها، ويمكنك تعديل أي لون أو شكل.
الجزء الثاني يكمل كل بيكسل لم يطابق الأصل من بيانات الصورة الأصلية المحفوظة في آخر الملف.
طبقات الألوان: {layers} · الأشكال: {polys}
"""
import base64
import io

from PIL import Image, ImageChops, ImageDraw

TITLE = {title!r}
SIZE = ({w}, {h})
MODE = {mode!r}


def pts(s):
    return [tuple(map(int, p.split(","))) for p in s.split()]


img = Image.new("RGBA", SIZE, (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# ── 1. الرسم: مناطق الألوان من الأكبر إلى الأصغر ─────────────────────────────────────────────
{drawing}

# ── 2. التفاصيل الدقيقة: كل بيكسل لم يطابق يأخذ قيمته الأصلية ───────────────────────────────


def finish(img):
    original = Image.open(io.BytesIO(base64.b64decode("".join(IMAGE_B64.split())))).convert("RGBA")
    diff = ImageChops.difference(img, original)
    r, g, b, a = diff.split()
    mask = ImageChops.lighter(ImageChops.lighter(r, g), ImageChops.lighter(b, a)).point(lambda v: 255 if v else 0)
    changed = sum(mask.histogram()[255:])
    img.paste(original, (0, 0), mask)
    same = ImageChops.difference(img, original).getbbox() is None
    return img, changed, same


IMAGE_B64 = (
{data}
)

if __name__ == "__main__" or __name__ == "kosif":
    img, changed, same = finish(img)
    out = img.convert(MODE) if MODE != "RGBA" else img
    out.save(TITLE + ".png")
    total = SIZE[0] * SIZE[1]
    print(f"{{TITLE}}.png: {{SIZE[0]}}x{{SIZE[1]}}، الرسم أصاب {{total - changed:,}} بيكسل، وأُكمل {{changed:,}} من الأصل، "
          f"{{'مطابقة تماماً' if same else 'تحذير: غير مطابقة'}}")
'''


def _bridge(polys: list[list[tuple[int, int]]]) -> list[tuple[int, int]]:
    """An outline and its holes as ONE polygon: every ring is joined to the first point; Pillow fills even-odd,
    so the joins cancel out and the holes stay open."""
    a = polys[0][0]
    out: list[tuple[int, int]] = []
    for p in polys:
        out += list(p) + [p[0], a]
    return out


def image_to_python(path: str | Path, title: str | None = None, max_side: int = 520, line: int = 100) -> str:
    path = Path(path)
    title = title or path.stem
    with Image.open(path) as im:
        im.load()
        w, h = im.size
        mode = "RGBA" if (im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info) else "RGB"
    data = V.trace(path, max_side=max_side)
    tw, th = data["size"]
    sx, sy = w / tw, h / th
    blocks, n_polys = [], 0
    for L in data["layers"]:
        groups, cur = [], []
        for p in L["polys"]:
            pts = [(int(round(x * sx)), int(round(y * sy))) for x, y in p["pts"]]
            dedup = [q for i, q in enumerate(pts) if i == 0 or q != pts[i - 1]]
            if len(dedup) < 3:
                continue
            if not p["hole"]:
                if cur:
                    groups.append(cur)
                cur = [dedup]
            elif cur:
                cur.append(dedup)
        if cur:
            groups.append(cur)
        lines = [f"# {L['name']} {L['color']} ({int(L['area'] * sx * sy):,} بيكسل تقريباً)"]
        for g in groups:
            ring = _bridge(g) if len(g) > 1 else g[0]
            area = abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]))) / 2
            if area < 4 and len(g) == 1:
                continue
            lines.append(f'draw.polygon(pts("{" ".join(f"{x},{y}" for x, y in ring)}"), fill="{L["color"]}")')
            n_polys += 1
        if len(lines) > 1:
            blocks.append("\n".join(lines))
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    body = "\n".join(f'    "{b64[i:i + line]}"' for i in range(0, len(b64), line))
    code = TEMPLATE.format(title=title, stem=title, w=w, h=h, mode=mode, layers=len(data["layers"]), polys=n_polys,
                           drawing="\n\n".join(blocks), data=body)
    return code


if __name__ == "__main__":
    import sys
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.stem + "_code.py")
    out.write_text(image_to_python(src), encoding="utf-8")
    print(f"{out}: {math.ceil(out.stat().st_size / 1024):,} KB")
