"""The edit loop with any AI: 🧩 copies ONE package (instructions + what the picture contains + an edit program);
the user asks the AI for a change ("make the shirt red"), pastes the program the AI returns, and the studio draws
the edited picture.

The edit program is small: the original image is NOT inside it (only a reference key), so an AI can read and
change it. It edits with named tools (recolor, adjust, tint, paint, write, erase) between two markers; everything
else stays. When it comes back, the studio puts the original's bytes back in place of the key and runs it.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ORIGINALS = HERE / "code" / "originals"
KEY = "<<KOSIF:ORIGINAL:{sha}>>"

TOOLS = '''
# ── أدوات التعديل (Pillow فقط). كلها تعمل على img في مكانه. region = (x0, y0, x1, y1) بالبيكسل أو None للصورة كلها ──
def _box(region, size):
    if region is None:
        return (0, 0, size[0], size[1])
    x0, y0, x1, y1 = region
    return (max(0, int(x0)), max(0, int(y0)), min(size[0], int(x1)), min(size[1], int(y1)))


def _hsv(hexcolor):
    return Image.new("RGB", (1, 1), hexcolor).convert("HSV").getpixel((0, 0))


def color_mask(img, hexcolor, tolerance=40, region=None, soft=1.5):
    """Where the picture is close to a colour (average channel distance <= tolerance), inside region."""
    rgb = img.convert("RGB")
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, hexcolor))
    r, g, b = diff.split()
    avg = ImageChops.add(ImageChops.add(r, g, scale=2.0), b, scale=1.5)
    mask = avg.point(lambda v: 255 if v <= tolerance else 0)
    if region is not None:
        keep = Image.new("L", rgb.size, 0)
        keep.paste(255, _box(region, rgb.size))
        mask = ImageChops.multiply(mask, keep)
    return mask.filter(ImageFilter.GaussianBlur(soft)) if soft else mask


def recolor(img, src_hex, dst_hex, tolerance=40, region=None, keep_shading=True):
    """Change one colour into another. Pixels that are exactly src_hex become exactly dst_hex; darker and lighter
    pixels of it (folds, shadows, highlights) keep their relative shading when keep_shading is True, or become
    flat when it is False. Example: recolor(img, "#8a8a8a", "#c0392b", 42, (380, 420, 620, 760))  # the shirt"""
    mask = color_mask(img, src_hex, tolerance, region)
    h, s, v = img.convert("RGB").convert("HSV").split()
    sh, ss, sv = _hsv(src_hex)
    dh, ds, dv = _hsv(dst_hex)
    nh = Image.new("L", img.size, dh)
    ns = s.point(lambda x: max(0, min(255, int(x * ds / max(ss, 8) + .5) if ss > 8 else ds)))
    nv = v.point(lambda x: max(0, min(255, int(x * dv / max(sv, 1) + .5)))) if keep_shading else Image.new("L", img.size, dv)
    out = Image.merge("HSV", (nh, ns, nv)).convert("RGB")
    img.paste(out, (0, 0), mask)


def adjust(img, region=None, brightness=1.0, contrast=1.0, saturation=1.0, sharpness=1.0):
    """Brightness / contrast / saturation / sharpness of a region (1.0 = unchanged)."""
    box = _box(region, img.size)
    part = img.crop(box).convert("RGB")
    for cls, k in ((ImageEnhance.Brightness, brightness), (ImageEnhance.Contrast, contrast),
                   (ImageEnhance.Color, saturation), (ImageEnhance.Sharpness, sharpness)):
        if k != 1.0:
            part = cls(part).enhance(k)
    img.paste(part, box)


def tint(img, hexcolor, amount=0.3, region=None):
    """Wash a region with a colour (amount 0..1)."""
    box = _box(region, img.size)
    part = img.crop(box).convert("RGB")
    img.paste(Image.blend(part, Image.new("RGB", part.size, hexcolor), amount), box)


def paint(img, points, hexcolor, outline=None, width=1):
    """Draw a filled polygon: points = [(x, y), ...] in pixels."""
    ImageDraw.Draw(img).polygon(points, fill=hexcolor, outline=outline, width=width)


def write(img, text, xy, size=32, hexcolor="#ffffff", font_file=None):
    """Write text at xy (top-left). Latin text only renders reliably with the default font; give font_file for
    others."""
    try:
        font = ImageFont.truetype(font_file or "arial.ttf", size)
    except OSError:
        font = ImageFont.load_default(size)
    ImageDraw.Draw(img).text(xy, text, fill=hexcolor, font=font)


def erase(img, region, softness=14):
    """Remove something small: the region is filled with its blurred surroundings."""
    x0, y0, x1, y1 = _box(region, img.size)
    pad = softness * 3
    big = (max(0, x0 - pad), max(0, y0 - pad), min(img.size[0], x1 + pad), min(img.size[1], y1 + pad))
    patch = img.crop(big).convert("RGB").filter(ImageFilter.GaussianBlur(softness))
    mask = Image.new("L", patch.size, 0)
    ImageDraw.Draw(mask).rectangle([x0 - big[0], y0 - big[1], x1 - big[0], y1 - big[1]], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(softness / 2))
    img.paste(patch, big, mask)


def flip(img, horizontal=True):
    """Mirror the whole picture."""
    src = img.transpose(Image.FLIP_LEFT_RIGHT if horizontal else Image.FLIP_TOP_BOTTOM)
    img.paste(src, (0, 0))
'''

PROGRAM = '''# -*- coding: utf-8 -*-
"""KOSIF Studio edit program (Pillow only).

Picture: {title} ({w}x{h}). The original image is restored by the studio from the key below.
Edit ONLY between the markers "# EDITS START" and "# EDITS END". Keep everything else, including the IMAGE_B64 line.
"""
import base64
import io

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

TITLE = {title!r}
SIZE = ({w}, {h})
IMAGE_B64 = "{key}"
{tools}

def load_original():
    if IMAGE_B64.startswith("<<KOSIF:ORIGINAL:"):
        raise SystemExit("open this program in KOSIF Studio: it puts the original image back in place of the key")
    im = Image.open(io.BytesIO(base64.b64decode("".join(IMAGE_B64.split()))))
    im.load()
    return im.convert("RGB")


img = load_original()
draw = ImageDraw.Draw(img)       # in the studio the picture appears first, then the edits are painted over it

# EDITS START
# مثال (احذفه وضع تعديلاتك):
# recolor(img, "#8a8a8a", "#c0392b", tolerance=42, region=(380, 420, 620, 760))   # change the shirt from grey to red
# EDITS END

if __name__ == "__main__":
    img.save(TITLE + "_edited.png")
    print(TITLE + "_edited.png", SIZE)
'''

INSTRUCTIONS = '''أنت تساعد في تعديل صورة داخل برنامج KOSIF Studio. تحتك: (1) وصف لما تحتويه الصورة بالألوان والمواضع،
(2) برنامج بايثون صغير يحمّل الصورة الأصلية ويطبّق تعديلات عليها بأدوات جاهزة.

المطلوب منك: نفّذ طلب المستخدم بكتابة التعديلات بين السطرين "# EDITS START" و"# EDITS END" فقط، ثم أعد
**البرنامج كاملاً** كما هو (لا تغيّر سطر IMAGE_B64 ولا الأدوات ولا الاستيرادات). لا شرح خارج الكود.

الأدوات: recolor(img, "#src", "#dst", tolerance, region, keep_shading=True) يغيّر لوناً مع الحفاظ على الظلال؛
adjust(img, region, brightness, contrast, saturation, sharpness)؛ tint(img, "#hex", amount, region)؛
paint(img, [(x,y),...], "#hex")؛ write(img, "text", (x,y), size, "#hex")؛ erase(img, region)؛ flip(img)؛
وللرسم الحر draw (ImageDraw جاهز): draw.rectangle / ellipse / polygon / line / text.
region = (x0, y0, x1, y1) بالبيكسل. الإحداثيات تبدأ من أعلى اليسار. استعمل مواضع الطبقات في الوصف لتحديد المنطقة
واللون المصدر. للقميص مثلاً: خذ لون طبقته ومربّعها من الوصف ثم recolor بلون جديد.
'''


def layers(path: str | Path, max_layers: int = 14) -> dict:
    """What the picture contains, as data: size, photo?, and the colour layers (name, colour, share, box, centre)
    from the studio's own vectoriser, in the picture's own pixel coordinates."""
    import vectorize as V
    with Image.open(path) as im:
        w, h = im.size
    data = V.trace(path, max_side=300)
    tw, th = data["size"]
    sx, sy = w / tw, h / th
    total = max(1.0, sum(L["area"] for L in data["layers"]))
    out = []
    for L in data["layers"][:max_layers]:
        xs = [p[0] for q in L["polys"] for p in q["pts"]]
        ys = [p[1] for q in L["polys"] for p in q["pts"]]
        if not xs:
            continue
        parts = []
        for q in L["polys"]:
            px = [p[0] for p in q["pts"]]
            py = [p[1] for p in q["pts"]]
            if len(px) >= 3:
                bw, bh = (max(px) - min(px)) * sx, (max(py) - min(py)) * sy
                parts.append({"box": (int(min(px) * sx), int(min(py) * sy), int(max(px) * sx) + 1, int(max(py) * sy) + 1),
                              "area": float(abs(_poly_area(q["pts"])) * sx * sy), "span": bw * bh})
        parts.sort(key=lambda p: -p["area"])
        layer_area = max(1.0, sum(p["area"] for p in parts))
        for p in parts:
            p["share"] = p["area"] / layer_area
        out.append({"name": L["name"], "color": L["color"], "share": L["area"] / total,
                    "box": (int(min(xs) * sx), int(min(ys) * sy), int(max(xs) * sx), int(max(ys) * sy)),
                    "centre": (int(L["centre"][0] * sx), int(L["centre"][1] * sy)), "parts": parts[:8]})
    return {"name": Path(path).name, "size": (w, h), "photo": bool(data["photo"]), "layers": out}


def _poly_area(pts) -> float:
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        a += x0 * y1 - x1 * y0
    return a / 2


def describe(path: str | Path, max_layers: int = 14) -> str:
    """The same, in words an AI can act on."""
    d = layers(path, max_layers)
    w, h = d["size"]
    lines = [f"الصورة: {d['name']}، {w}×{h} بيكسل، {'صورة فوتوغرافية' if d['photo'] else 'رسم أو شعار'}.",
             "الطبقات اللونية (الاسم، اللون، النسبة، المربع المحيط x0,y0,x1,y1، المركز):"]
    for L in d["layers"]:
        big = [p["box"] for p in L["parts"] if p["share"] >= 0.08][:3]
        lines.append(f"- {L['name']}: {L['color']}، {L['share']:.0%}، المربع {L['box']}، المركز {L['centre']}"
                     + (f"، أجزاؤها الكبرى {big}" if big else ""))
    lines.append("نصيحة: لتغيير شيء واحد استعمل مربع جزئه الكبير لا مربع الطبقة كلها، فالطبقة قد تضم بقعاً صغيرة بنفس اللون.")
    return "\n".join(lines)


# ── colour-to-colour requests understood without any AI ("غيّر الذهبي إلى الأزرق", "make the grey red") ──
COLOURS = {
    "#d62828": ("أحمر", "احمر", "حمراء", "red"), "#2f6fd6": ("أزرق", "ازرق", "زرقاء", "blue"), "#2e9e5b": ("أخضر", "اخضر", "خضراء", "green"),
    "#f2c94c": ("أصفر", "اصفر", "صفراء", "yellow"), "#d4a53a": ("ذهبي", "gold", "golden"), "#f08a24": ("برتقالي", "orange"),
    "#7a4b2a": ("بني", "بنية", "brown"), "#f06aa8": ("وردي", "زهري", "pink"), "#7a4fd1": ("بنفسجي", "موف", "purple", "violet"),
    "#8a8a8a": ("رمادي", "رصاصي", "grey", "gray"), "#111111": ("أسود", "اسود", "سوداء", "black"), "#f5f5f5": ("أبيض", "ابيض", "بيضاء", "white"),
    "#2fb8d6": ("سماوي", "تركواز", "فيروزي", "cyan", "turquoise", "teal"), "#c0c0c0": ("فضي", "silver"),
    "#e8d9b5": ("بيج", "كريمي", "beige", "cream"), "#7f8c2a": ("زيتي", "olive"), "#1f2d6b": ("كحلي", "navy"),
    "#7b1e2b": ("عنابي", "نبيتي", "maroon", "burgundy"),
}
_WORD_TO_HEX = {w: hx for hx, words in COLOURS.items() for w in words}
_AR_VERBS = r"(?:غي[رّ]ر?|بد[لّ]ل?|حو[لّ]ل?|اجعل|خل[يّ]|صي[رّ]ر?|لو[نّ]ن?)"
_PATTERNS = [
    re.compile(_AR_VERBS + r"\s*(?:ال)?لون\s*(?:ال)?(\S+?)\s*(?:إلى|الى|الي|ل)\s*(?:اللون\s*)?(?:ال)?(\S+)"),
    re.compile(_AR_VERBS + r"\s*(?:ال)?(\S+?)\s*(?:إلى|الى|الي)\s*(?:اللون\s*)?(?:ال)?(\S+)"),
    re.compile(r"(?:change|make|turn|recolou?r|replace)\s+(?:the\s+)?(?:colou?r\s+)?(\w+)\s+(?:to|into|with)\s+(?:the\s+)?(\w+)", re.I),
]


def _word_hex(word: str) -> str | None:
    """The colour a word names, tolerant of 'ال', tanween, feminine/adjective endings and case."""
    w = re.sub(r"[ً-ْـ]", "", word.strip("،,.!؟?;: ").lower())
    forms = [w]
    if w.startswith("ال"):
        forms.append(w[2:])
    for base in list(forms):
        for i in (1, 2, 3):
            if len(base) > i + 2 and base[-i:] in ("ا", "ة", "ي", "ه", "ية", "ياً", "يا", "ات", "ين", "ish"):
                forms.append(base[:-i])
    for form in forms:
        if form in _WORD_TO_HEX:
            return _WORD_TO_HEX[form]
    return None


def parse_colour_request(request: str) -> tuple[str, str] | None:
    """(source hex, target hex) when the request says 'change colour A to colour B' in Arabic or English: by the
    verb patterns first, otherwise the first and last colour words mentioned ('the grey shirt ... red')."""
    for pat in _PATTERNS:
        m = pat.search(request)
        if m:
            a, b = _word_hex(m.group(1)), _word_hex(m.group(2))
            if a and b:
                return a, b
    found = [hx for hx in (_word_hex(w) for w in re.findall(r"[\w؀-ۿ]+", request)) if hx]
    if len(found) >= 2 and found[0] != found[-1]:
        return found[0], found[-1]
    return None


def _hsv_dist(h1, h2) -> float:
    import colorsys
    def hsv(hx):
        r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
        return colorsys.rgb_to_hsv(r, g, b)
    (ha, sa, va), (hb, sb, vb) = hsv(h1), hsv(h2)
    dh = min(abs(ha - hb), 1 - abs(ha - hb)) * (sa + sb)        # hue matters only for saturated colours
    return 2.2 * dh + 0.9 * abs(sa - sb) + 0.6 * abs(va - vb)


def local_edit(path: str | Path, request: str) -> tuple[str, str] | None:
    """Edit lines for a colour-to-colour request, found without an AI: the picture's layer nearest to the named
    colour is recoloured to the target (shading kept). (edit lines, note) or None when the request needs an AI."""
    pair = parse_colour_request(request)
    if not pair:
        return None
    src_hex, dst_hex = pair
    d = layers(path)
    cands = [L for L in d["layers"] if L["share"] >= 0.005]
    if not cands:
        return None
    L = min(cands, key=lambda L: _hsv_dist(L["color"], src_hex))
    if _hsv_dist(L["color"], src_hex) > 0.6:
        return None
    w, h = d["size"]
    pad = max(3, int(0.01 * max(w, h)))
    boxes, covered = [], 0.0
    for p in L["parts"]:                                   # the big pieces (a headline, a badge), not the specks
        if covered >= 0.85 or len(boxes) >= 6 or p["share"] < 0.04:
            break
        x0, y0, x1, y1 = p["box"]
        boxes.append((max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad)))
        covered += p["share"]
    if not boxes:
        x0, y0, x1, y1 = L["box"]
        boxes = [(max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad))]
    lines = [f"# تعديل محلي بلا ذكاء اصطناعي: الطبقة «{L['name']}» {L['color']} ({L['share']:.0%}) → {dst_hex}، {len(boxes)} جزء"]
    lines += [f'recolor(img, "{L["color"]}", "{dst_hex}", tolerance=34, region={b})' for b in boxes]
    return "\n".join(lines), f"الطبقة {L['name']} {L['color']} → {dst_hex} في {len(boxes)} جزء"


def with_edits(program: str, edit_lines: str) -> str:
    """The program with these lines between the markers (the example comment is dropped)."""
    a = re.search(r"^# EDITS START[ \t]*$", program, re.M)
    b = re.search(r"^# EDITS END[ \t]*$", program, re.M)
    if not a or not b or b.start() < a.end():
        raise ValueError("the edit program has no marker lines")
    return program[:a.start()] + "# EDITS START\n" + edit_lines.rstrip() + "\n" + program[b.start():]


def edit_program(path: str | Path, title: str | None = None) -> tuple[str, str]:
    """(program, sha): the small edit program with a key instead of the image; the original's bytes are stored
    under code/originals/<sha>.b64 so the studio can restore them."""
    path = Path(path)
    data = path.read_bytes()
    sha = hashlib.sha1(data).hexdigest()[:16]
    ORIGINALS.mkdir(parents=True, exist_ok=True)
    (ORIGINALS / f"{sha}.b64").write_text(base64.b64encode(data).decode("ascii"), encoding="ascii")
    with Image.open(path) as im:
        w, h = im.size
    title = title or path.stem
    return PROGRAM.format(title=title, w=w, h=h, key=KEY.format(sha=sha), tools=TOOLS), sha


def package(path: str | Path, title: str | None = None, request: str = "") -> str:
    """Instructions + description + program: one text to paste into any AI."""
    program, _ = edit_program(path, title)
    parts = [INSTRUCTIONS.strip(), "", "## وصف الصورة", describe(path), "",
             "## طلب المستخدم", request.strip() or "[اكتب التعديل المطلوب هنا، مثلاً: غيّر لون القميص إلى الأحمر]", "",
             "## البرنامج", "```python", program.rstrip(), "```"]
    return "\n".join(parts)


def restore(code: str) -> tuple[str, bool]:
    """Put the original image back in place of the key. (code, restored?)"""
    import re
    m = re.search(r"""^IMAGE_B64\s*=\s*\(?\s*['"]<<KOSIF:ORIGINAL:([0-9a-f]{16})>>['"]\s*\)?[ \t]*(#[^\n]*)?$""", code, re.M)
    if not m:
        return code, False
    f = ORIGINALS / f"{m.group(1)}.b64"
    if not f.exists():
        raise FileNotFoundError(f"the original image for key {m.group(1)} is not stored on this computer")
    b64 = f.read_text(encoding="ascii")
    body = "\n".join(f'    "{b64[i:i + 100]}"' for i in range(0, len(b64), 100))
    return code[:m.start()] + f"IMAGE_B64 = (\n{body}\n)" + code[m.end():], True


if __name__ == "__main__":
    import sys
    print(package(sys.argv[1], request=" ".join(sys.argv[2:])))
