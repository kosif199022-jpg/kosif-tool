"""Programs for the formats-platforms family.

Encodes, reframes, packages and validates media for real with ffmpeg/ffprobe on tiny synthetic
clips (lavfi testsrc/sine), and implements the layout, platform-limit and copy rules as checkers
whose verdicts on planted good/bad fixtures are known in advance. Values are read back with
ffprobe/ebur128/cv2 rather than trusted from the arguments.
"""
from __future__ import annotations
import difflib
import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_DIRS = ["/usr/share/fonts/truetype/noto", "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation"]
LATIN = ["NotoSans-Bold.ttf", "NotoSans-Regular.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "LiberationSans-Bold.ttf"]
ARABIC = ["NotoSansArabic-Bold.ttf", "NotoSansArabic-Regular.ttf", "NotoNaskhArabic-Regular.ttf", "DejaVuSans.ttf"]
ARABIC_RE = re.compile(r"[\u0600-\u06ff]")


def font(size, arabic=False):
    for d in FONT_DIRS:
        for n in (ARABIC if arabic else LATIN):
            if (Path(d) / n).is_file():
                return ImageFont.truetype(str(Path(d) / n), size)
    raise FileNotFoundError("font")


def _raqm():
    from PIL import features
    return features.check("raqm")


def rtl_kw():
    return {"direction": "rtl"} if _raqm() else {}


def ff(*args, ok=True):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], capture_output=True, text=True)
    if ok and r.returncode:
        raise RuntimeError(r.stderr[-800:])
    return r


def ff_stderr(*args) -> str:
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *map(str, args)], capture_output=True, text=True).stderr


def probe(path, *extra) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", *extra, str(path)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def vstream(p):
    return next(s for s in probe(p)["streams"] if s["codec_type"] == "video")


def frames_of(path, w, h, fmt="rgb24", ch=3):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", fmt, "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, ch) if ch > 1 else np.frombuffer(raw, np.uint8).reshape(-1, h, w)


def testclip(work, name="src.mp4", size="64x36", dur=1, rate=30, audio=False, src="testsrc2"):
    p = work / name
    args = ["-f", "lavfi", "-i", f"{src}=size={size}:rate={rate}:duration={dur}"]
    if audio:
        args += ["-f", "lavfi", "-i", f"sine=f=440:d={dur}:sample_rate=48000"]
    args += ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p"]
    if audio:
        args += ["-c:a", "aac", "-b:a", "128k", "-shortest"]
    ff(*args, p)
    return p


def lufs(path) -> tuple:
    err = ff_stderr("-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-")
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)[-1])
    return i, tp


def normalise(src, dst, target=-14.0):
    i, _ = lufs(src)
    ff("-i", src, "-af", f"volume={target - i:.2f}dB", "-c:a", "pcm_s16le", dst)
    return lufs(dst)


def atoms(path) -> list:
    data, out, i = Path(path).read_bytes(), [], 0
    while i + 8 <= len(data):
        size = int.from_bytes(data[i:i + 4], "big")
        out.append(data[i + 4:i + 8].decode("latin1"))
        if size < 8:
            break
        i += size
    return out


def save_json(work, name, obj):
    (work / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def contrast(a, b):
    def L(rgb): return 0.2126 * _lin(rgb[0]) + 0.7152 * _lin(rgb[1]) + 0.0722 * _lin(rgb[2])
    la, lb = sorted((L(a), L(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


def clamp01(p): return max(0.0, min(1.0, p))
def power4_in_out(p): return 8 * p ** 4 if p < 0.5 else 1 - (-2 * p + 2) ** 4 / 2


# ---------------------------------------------------------------- FMT-03
def bar_height(W, H, ratio=2.39):
    return round((H - W / ratio) / 2)


def letterbox_reveal(t, D, start_cap=2.4, dur=2.2, h0=70):
    start = min(start_cap, 0.15 * D)
    return h0 * (1 - power4_in_out(clamp01((t - start) / dur)))


def fmt_03(work):
    W, H = 1280, 720
    b = bar_height(W, H)
    src = work / "src.png"
    Image.new("RGB", (W, H), (200, 120, 60)).save(src)
    out = work / "letterbox.png"
    ff("-i", src, "-vf", f"drawbox=x=0:y=0:w=iw:h={b}:color=black:t=fill,drawbox=x=0:y=ih-{b}:w=iw:h={b}:color=black:t=fill", out)
    a = np.asarray(Image.open(out).convert("L"))
    dark = np.nonzero(a.max(axis=1) < 10)[0]
    top = int((dark < H / 2).sum())
    return [("bar = (H - W/2.39)/2 -> 138 px at 1080p", bar_height(1920, 1080) == 138, bar_height(1920, 1080)),
            ("bar -> 92 px at 720p", b == 92, b),
            ("burned bars measured 92 rows top and bottom", top == 92 and len(dark) == 184, (top, len(dark))),
            ("reveal starts at min(2.4, 15% D): D=10 -> 1.5 s", letterbox_reveal(1.5, 10) == 70 and letterbox_reveal(3.7, 10) == 0, letterbox_reveal(2.6, 10)),
            ("power4.inOut midpoint (1.1 s in) = 35 px", abs(letterbox_reveal(1.5 + 1.1, 10) - 35) < 1e-9, letterbox_reveal(2.6, 10))]


# ---------------------------------------------------------------- FMT-04
def stage_fit(vw, vh, sw=1920, sh=1080):
    s = min(vw / sw, vh / sh)
    return {"scale": s, "x": (vw - sw * s) / 2, "y": (vh - sh * s) / 2, "box": "letterbox" if vw / vh < sw / sh else "pillarbox" if vw / vh > sw / sh else "exact"}


def fmt_04(work):
    phone, wide, exact = stage_fit(390, 844), stage_fit(2560, 1080), stage_fit(1280, 720)
    im = Image.new("L", (390, 844), 0)
    s = phone["scale"]
    ImageDraw.Draw(im).rectangle([phone["x"], phone["y"], phone["x"] + 1920 * s - 1, phone["y"] + 1080 * s - 1], fill=255)
    im.save(work / "phone_fit.png")
    rows = np.nonzero(np.asarray(im).max(axis=1))[0]
    save_json(work, "fits.json", [phone, wide, exact])
    return [("390x844 -> scale 0.2031, letterboxed", abs(phone["scale"] - 390 / 1920) < 1e-12 and phone["box"] == "letterbox", phone),
            ("2560x1080 -> scale 1, pillarbox x=320", wide["scale"] == 1 and wide["x"] == 320 and wide["box"] == "pillarbox", wide),
            ("1280x720 -> exact 2/3", abs(exact["scale"] - 2 / 3) < 1e-12 and exact["box"] == "exact", exact),
            ("rendered stage height 219 px centred", len(rows) in (219, 220) and abs(rows.mean() - 421.5) <= 1, (len(rows), float(rows.mean())))]


# ---------------------------------------------------------------- FMT-05
TOKENS = {"9:16": {"caption": 56, "body": 48, "floor": 36}, "16:9": {"caption": 44, "body": 36, "floor": 28}}


def fit_caption(text, aspect, width=1080, margin=0.1):
    tok = TOKENS[aspect]
    size = tok["caption"] * width / 1080
    fnt = font(int(size))
    usable = width * (1 - 2 * margin)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= usable:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    cards = [lines[i:i + 2] for i in range(0, len(lines), 2)]
    return {"size": size, "cards": cards}


def fmt_05(work):
    short = fit_caption("Save this for later", "9:16")
    long = fit_caption("The three numbers every founder should check on Monday morning before the team meeting starts", "9:16")
    save_json(work, "captions.json", [short, long])
    return [("9:16 caption token 56 px >= 48 at 1080 wide", short["size"] >= 48, short["size"]),
            ("floor never below 36 px", all(t["floor"] >= 28 and (k != "9:16" or t["floor"] == 36) for k, t in TOKENS.items()), TOKENS["9:16"]),
            ("short caption fits one card", len(short["cards"]) == 1, short["cards"]),
            ("long caption splits into cards, size unchanged", len(long["cards"]) >= 2 and long["size"] == 56, (len(long["cards"]), long["size"])),
            ("each card <= 2 lines", all(len(c) <= 2 for c in long["cards"]), [len(c) for c in long["cards"]])]


# ---------------------------------------------------------------- FMT-06
def data_layout(aspect):
    vertical = aspect in ("9:16", "4:5")
    return {"ticks": 4 if vertical else 6, "legend": "below" if vertical else "right", "panels": "stacked" if vertical else "side-by-side",
            "plate": (2700, 3840) if vertical else (3840, 2160)}


def fmt_06(work):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    res = {}
    for asp, size in (("9:16", (2.7, 4.8)), ("16:9", (4.8, 2.7))):
        L = data_layout(asp)
        fig, axes = plt.subplots(2 if L["panels"] == "stacked" else 1, 1 if L["panels"] == "stacked" else 2, figsize=size)
        for ax in axes:
            ax.plot(range(0, 101, 5), [x ** 0.5 for x in range(0, 101, 5)])
            ax.xaxis.set_major_locator(MaxNLocator(L["ticks"]))
        fig.savefig(work / f"chart_{asp.replace(':', 'x')}.png", dpi=60)
        n = len([t for t in axes[0].get_xticks() if 0 <= t <= 100])
        res[asp] = {"ticks": n, "layout": L}
        plt.close(fig)
    save_json(work, "layouts.json", res)
    return [("9:16 has 3-5 ticks", 3 <= res["9:16"]["ticks"] <= 5, res["9:16"]["ticks"]),
            ("16:9 has 4-7 ticks", 4 <= res["16:9"]["ticks"] <= 7, res["16:9"]["ticks"]),
            ("9:16 stacks panels with legend below", res["9:16"]["layout"]["panels"] == "stacked" and res["9:16"]["layout"]["legend"] == "below", res["9:16"]["layout"]),
            ("map plates 3840x2160 / 2700x3840", data_layout("16:9")["plate"] == (3840, 2160) and data_layout("9:16")["plate"] == (2700, 3840), "plates")]


# ---------------------------------------------------------------- FMT-09
SOCIAL = {"linkedin_post": (1200, 627, 100), "x_card": (1200, 675, 80), "ig_square": (1080, 1080, 108), "ig_landscape": (1080, 566, 80),
          "fb_post": (1200, 630, 100), "yt_thumb": (1280, 720, 72), "github_preview": (1280, 640, None)}


def safe_rect(name):
    w, h, m = SOCIAL[name]
    m = m if m is not None else round(0.1 * min(w, h))
    return (m, m, w - m, h - m)


def channel_art_safe(w=2560, h=1440, sw=1546, sh=423):
    return ((w - sw) / 2, (h - sh) / 2, (w + sw) / 2, (h + sh) / 2)


def fmt_09(work):
    w, h, _ = SOCIAL["ig_square"]
    im = Image.new("RGB", (w, h), (240, 240, 240))
    r = safe_rect("ig_square")
    ImageDraw.Draw(im).rectangle(r, outline=(255, 0, 0), width=2)
    im.save(work / "ig_square_safe.png")
    im.convert("RGB").save(work / "github_preview.jpg", quality=85)
    ca = channel_art_safe()
    a = np.asarray(im)
    red_cols = np.nonzero((a[540, :, 0] == 255) & (a[540, :, 1] == 0))[0]
    return [("IG square margin 108 px = 10%", r == (108, 108, 972, 972) and 108 / 1080 == 0.1, r),
            ("rendered safe box edge at x=108", int(red_cols.min()) == 108, int(red_cols.min())),
            ("channel art safe 1546x423 centred at (507, 508.5)", ca == (507.0, 508.5, 2053.0, 931.5), ca),
            ("X card 1200x675 with 80 px margin", safe_rect("x_card") == (80, 80, 1120, 595), safe_rect("x_card")),
            ("GitHub preview <= 1 MB", (work / "github_preview.jpg").stat().st_size <= 1_000_000, (work / "github_preview.jpg").stat().st_size)]


# ---------------------------------------------------------------- FMT-10
def caption_box(W, H, lines, vertical=True):
    m = 0.05
    x0, x1 = W * m, W * (1 - (0.12 if vertical else m))
    y_centre = H * 0.70
    lh = 0.035 * H
    y0 = y_centre - lines * lh / 2
    y1 = y_centre + lines * lh / 2
    limit = H * (0.80 if vertical else 1 - m)
    return {"box": (x0, y0, x1, y1), "ok": lines <= 2 and y1 <= limit and y0 >= H * m}


def fmt_10(work):
    b = caption_box(1080, 1920, 2)
    b3 = caption_box(1080, 1920, 3)
    im = Image.new("RGB", (1080, 1920), (20, 20, 20))
    ImageDraw.Draw(im).rectangle(b["box"], fill=(255, 255, 255))
    im.resize((270, 480)).save(work / "caption_safe.png")
    return [("2-line caption inside 9:16 safe zone", b["ok"], b),
            ("right 12% kept clear (x1 = 950.4)", abs(b["box"][2] - 950.4) < 1e-9, b["box"][2]),
            ("caption bottom above the bottom 20% (<= 1536)", b["box"][3] <= 1536, b["box"][3]),
            ("3 lines refused", not b3["ok"], b3["ok"]),
            ("white on #141414 >= 7:1", contrast((255, 255, 255), (20, 20, 20)) >= 7, contrast((255, 255, 255), (20, 20, 20))),
            ("#888 on white fails 4.5:1", contrast((136, 136, 136), (255, 255, 255)) < 4.5, contrast((136, 136, 136), (255, 255, 255)))]


# ---------------------------------------------------------------- FMT-12
def density(mode, bullets):
    lo, hi = (1, 3) if mode == "narrated" else (4, 8)
    return lo <= len(bullets) <= hi


def vtt(cues):
    def ts(s): return f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{s % 60:06.3f}"
    return "WEBVTT\n\n" + "\n\n".join(f"{ts(a)} --> {ts(b)}\n{t}" for a, b, t in cues) + "\n"


def parse_vtt(text):
    out = []
    for m in re.finditer(r"(\d\d):(\d\d):(\d\d\.\d{3}) --> (\d\d):(\d\d):(\d\d\.\d{3})\n(.+)", text):
        g = m.groups()
        out.append((int(g[0]) * 3600 + int(g[1]) * 60 + float(g[2]), int(g[3]) * 3600 + int(g[4]) * 60 + float(g[5]), g[6]))
    return out


def fmt_12(work):
    cues = [(0.0, 1.8, "ثلاث أدوات"), (1.8, 3.5, "تختصر يومك"), (61.25, 63.0, "احفظ المنشور")]
    text = vtt(cues)
    (work / "captions.vtt").write_text(text, encoding="utf-8")
    back = parse_vtt(text)
    return [("speaker-led accepts 3 bullets, rejects 5", density("narrated", list("abc")) and not density("narrated", list("abcde")), "narrated"),
            ("read-first accepts 6, rejects 2", density("read", list("abcdef")) and not density("read", list("ab")), "read"),
            ("captions.vtt round-trips exactly", back == cues, back),
            ("cue past one minute written 00:01:01.250", "00:01:01.250 --> 00:01:03.000" in text, "61.25")]


# ---------------------------------------------------------------- FMT-13
def subject_centre(frame):
    import cv2
    g = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    _, m = cv2.threshold(g, 200, 255, cv2.THRESH_BINARY)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(max(cs, key=cv2.contourArea))
    return x + w / 2, y + h / 2


def fmt_13(work):
    W, H = 192, 108
    im = Image.new("RGB", (W, H), (60, 90, 140))
    ImageDraw.Draw(im).ellipse([140, 30, 170, 70], fill=(250, 250, 250))
    src = work / "src.png"
    im.save(src)
    cx, _ = subject_centre(np.asarray(im))
    ow = round(H * 4 / 5 / 2) * 2   # 4:5 window on the source, output 112x140 (exact 4:5, even)
    x = int(min(max(cx - ow / 2, 0), W - ow))
    smart = work / "smart_4x5.png"
    ff("-i", src, "-vf", f"crop={ow}:{H}:{x}:0,scale=112:140", smart)
    blur = work / "blur_4x5.png"
    ff("-i", src, "-filter_complex",
       "[0]split[a][b];[b]scale=112:140:force_original_aspect_ratio=increase,crop=112:140,gblur=sigma=40,eq=brightness=-0.12:saturation=0.85[bg];"
       "[a]scale=112:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2", blur)
    s = np.asarray(Image.open(smart).convert("RGB"))
    scx, _ = subject_centre(s)
    b = np.asarray(Image.open(blur).convert("RGB")).astype(int)
    top = b[2:8, 50].mean(axis=0)
    src_c = np.array([60, 90, 140])
    sat = lambda c: c.max() - c.min()  # chroma: brightness shifts all channels, saturation scales the spread
    return [("smart 4:5 output 112x140", Image.open(smart).size == (112, 140), Image.open(smart).size),
            ("subject kept near the centre of the reframe", abs(scx - 56) < 12, scx),
            ("blur fill darker than the source (brightness -0.12)", top.mean() < src_c.mean() - 15, (top.round(1).tolist(), src_c.tolist())),
            ("blur fill less saturated (0.85)", sat(top) < sat(src_c), (round(sat(top), 3), round(sat(src_c), 3))),
            ("blur output 112x140", Image.open(blur).size == (112, 140), Image.open(blur).size)]


# ---------------------------------------------------------------- FMT-14
def fmt_14(work):
    src = testclip(work, size="192x108", dur=0.2)
    out = work / "vertical.mp4"
    ff("-i", src, "-filter_complex",
       "[0]split[a][b];[b]scale=108:192:force_original_aspect_ratio=increase,crop=108:192,boxblur=20,eq=brightness=-0.15[bg];"
       "[a]scale=108:-2[fg];[bg][fg]overlay=0:(H-h)/2", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", out)
    v = vstream(out)
    f = frames_of(out, 108, 192)[0].astype(int)
    fg_h = round(108 * 108 / 192 / 2) * 2
    y0 = (192 - fg_h) // 2
    band_var = f[y0 + 4:y0 + fg_h - 4].std()
    bg_var = f[5:y0 - 5].std()
    ref = frames_of(src, 192, 108)[0]
    return [("output 108x192 (9:16)", (v["width"], v["height"]) == (108, 192), (v["width"], v["height"])),
            ("foreground fills full width (fg 1080-wide rule)", fg_h == 60, fg_h),
            ("sharp band vs boxblur 20 background (std ratio > 2)", band_var > 2 * bg_var, (round(band_var, 1), round(bg_var, 1))),
            ("background darker than source (-0.15)", f[5:y0 - 5].mean() < ref.mean() - 15, (round(f[5:y0 - 5].mean(), 1), round(ref.mean(), 1)))]


# ---------------------------------------------------------------- FMT-15
def fmt_15(work):
    src = work / "src.png"
    Image.new("RGB", (192, 108), (255, 0, 0)).save(src)
    pad = work / "pad.png"
    ff("-i", src, "-vf", "scale=108:192:force_original_aspect_ratio=decrease,pad=108:192:(ow-iw)/2:(oh-ih)/2", pad)
    crop = work / "crop.png"
    ff("-i", src, "-vf", "crop=ih*9/16:ih,scale=108:192", crop)
    p = np.asarray(Image.open(pad).convert("RGB"))
    red_rows = np.nonzero(p[:, 54, 0] > 200)[0]
    c = Image.open(crop)
    return [("pad keeps whole frame: 108x60 band centred", len(red_rows) in (60, 61) and abs(red_rows.mean() - 95.5) <= 1, (len(red_rows), float(red_rows.mean()))),
            ("pad output 108x192", Image.open(pad).size == (108, 192), Image.open(pad).size),
            ("centre crop ih*9/16 -> 108x192 all source pixels", c.size == (108, 192) and np.asarray(c.convert("RGB"))[:, :, 0].min() > 200, c.size)]


# ---------------------------------------------------------------- FMT-17
def shorts_plan(src_dur, peaks, length=60, handle=15):
    if src_dur < length + 2 * handle:
        return {"feasible": False, "need": length + 2 * handle}
    out = []
    for p in peaks:
        a = p - length / 2 - handle
        b = p + length / 2 + handle
        if a < 0 or b > src_dur:
            continue
        out.append((a, b))
    return {"feasible": True, "clips": out}


def fmt_17(work):
    ok = shorts_plan(600, [50, 300, 590])
    no = shorts_plan(80, [40])
    save_json(work, "plan.json", ok)
    src = testclip(work, dur=2)
    cut = work / "cut.mp4"
    ff("-ss", 0.5, "-i", src, "-t", 0.9, "-c:v", "libx264", "-preset", "ultrafast", cut)
    d = float(probe(cut)["format"]["duration"])
    return [("60 s + 2x15 s handles needs 90 s: 80 s source refused", no == {"feasible": False, "need": 90}, no),
            ("peak at 300 s -> trim 255..345 s", (255.0, 345.0) in ok["clips"], ok["clips"]),
            ("candidates that would overrun the source are dropped (590)", len(ok["clips"]) == 2, ok["clips"]),
            ("ffmpeg trim returns the planned length (0.9 s +-1 frame)", abs(d - 0.9) <= 1 / 30 + 1e-3, d)]


# ---------------------------------------------------------------- FMT-18
LAYOUT = {"16:9": {"title": (0.06, 0.40), "size": 0.09}, "9:16": {"title": (0.08, 0.18), "size": 0.06},
          "1:1": {"title": (0.08, 0.30), "size": 0.08}, "4:5": {"title": (0.08, 0.25), "size": 0.075}}
RATIO = {"16:9": (320, 180), "9:16": (180, 320), "1:1": (240, 240), "4:5": (216, 270)}


def render_ratio(aspect, title="Launch day"):
    W, H = RATIO[aspect]
    tok = LAYOUT[aspect]
    im = Image.new("L", (W, H), 0)
    sz = int(tok["size"] * max(W, H))
    ImageDraw.Draw(im).text((tok["title"][0] * W, tok["title"][1] * H), title, font=font(sz), fill=255)
    return im


def fmt_18(work):
    res = {}
    for a in RATIO:
        im = render_ratio(a)
        im.save(work / f"title_{a.replace(':', 'x')}.png")
        arr = np.asarray(im)
        xs = np.nonzero(arr.max(axis=0))[0]
        res[a] = (int(xs.min()), int(xs.max()), im.width)
    crop = np.asarray(render_ratio("16:9"))[:, 70:250]
    cut_title = crop[:, 0].max() > 0 or crop[:, -1].max() > 0
    return [("title fully inside every ratio (no edge contact)", all(lo > 0 and hi < w - 1 for lo, hi, w in res.values()), res),
            ("four ratios rendered from one composition", len(res) == 4, list(res)),
            ("blind centre-crop of 16:9 to 9:16 cuts the title (why we recompose)", bool(cut_title), bool(cut_title))]


# ---------------------------------------------------------------- FMT-20
def fmt_20(work):
    out = work / "master.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=size=64x36:rate=30:duration=3", "-f", "lavfi", "-i", "sine=d=3:sample_rate=48000",
       "-c:v", "libx264", "-preset", "medium", "-crf", 18, "-g", 60, "-pix_fmt", "yuv420p",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-ar", 48000, "-movflags", "+faststart", out)
    v = vstream(out)
    a = next(s for s in probe(out)["streams"] if s["codec_type"] == "audio")
    keys = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-skip_frame", "nokey", "-show_entries", "frame=pts_time",
                           "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.split()
    at = atoms(out)
    return [("bt709 primaries/trc/matrix read back", (v.get("color_primaries"), v.get("color_transfer"), v.get("color_space")) == ("bt709", "bt709", "bt709"),
             (v.get("color_primaries"), v.get("color_transfer"), v.get("color_space"))),
            ("moov before mdat (+faststart)", at.index("moov") < at.index("mdat"), at),
            ("GOP 2xfps: keyframes at 0 and 2 s", [round(float(k.strip(",")), 2) for k in keys] == [0.0, 2.0], keys),
            ("AAC 48 kHz", a["codec_name"] == "aac" and a["sample_rate"] == "48000", (a["codec_name"], a["sample_rate"])),
            ("yuv420p H.264", v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p", (v["codec_name"], v["pix_fmt"]))]


# ---------------------------------------------------------------- FMT-21
def fmt_21(work):
    src = work / "tone.wav"
    ff("-f", "lavfi", "-i", "sine=f=1000:d=3:sample_rate=48000", src)
    i, tp = normalise(src, work / "norm.wav")
    vid = work / "v.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=size=64x36:rate=30:duration=1", "-c:v", "libx264", "-preset", "ultrafast", "-b:v", "45M",
       "-maxrate", "50M", "-bufsize", "90M", vid)
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames",
                            "-of", "csv=p=0", str(vid)], capture_output=True, text=True).stdout.strip())
    mux = work / "aac.mp4"
    ff("-i", vid, "-i", work / "norm.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", mux)
    a = next(s for s in probe(mux)["streams"] if s["codec_type"] == "audio")

    def vmd5(p):
        return subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:v", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()
    return [("integrated loudness -14 LUFS +-1 (ebur128)", abs(i + 14) <= 1, i),
            ("true peak <= -1 dBTP", tp <= -1, tp),
            ("frame count within 1 of the 30-frame timeline", abs(n - 30) <= 1, n),
            ("PCM -> AAC remux, video packets copied unchanged", a["codec_name"] == "aac" and vmd5(mux) == vmd5(vid), (a["codec_name"], vmd5(mux)[:20]))]


# ---------------------------------------------------------------- FMT-22
def fmt_22(work):
    src = work / "rgba.png"
    im = Image.new("RGBA", (64, 36), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([16, 4, 48, 32], fill=(255, 200, 0, 255))
    im.save(src)
    webm = work / "alpha.webm"
    ff("-loop", 1, "-i", src, "-t", 0.2, "-r", 10, "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "200k", webm)
    mov = work / "alpha.mov"
    ff("-loop", 1, "-i", src, "-t", 0.2, "-r", 10, "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", mov)
    w = vstream(webm)
    m = vstream(mov)
    dec = frames_of(mov, 64, 36, fmt="rgba", ch=4)[0]
    return [("VP9 stream tagged alpha_mode=1", str(w.get("tags", {}).get("alpha_mode", w.get("tags", {}).get("ALPHA_MODE"))) == "1", w.get("tags")),
            ("ProRes 4444 keeps alpha (yuva444p1x)", m["pix_fmt"].startswith("yuva444p1"), m["pix_fmt"]),
            ("decoded corner transparent, centre opaque", dec[0, 0, 3] == 0 and dec[18, 32, 3] == 255, (int(dec[0, 0, 3]), int(dec[18, 32, 3])))]


# ---------------------------------------------------------------- FMT-23
def fmt_23(work):
    out = work / "hdr.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=size=64x36:rate=30:duration=0.3", "-c:v", "libx265", "-preset", "ultrafast", "-pix_fmt", "yuv420p10le",
       "-x265-params", "log-level=error:colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc",
       "-color_primaries", "bt2020", "-color_trc", "smpte2084", "-colorspace", "bt2020nc", "-tag:v", "hvc1", out)
    v = vstream(out)
    sdr = testclip(work)
    vs = vstream(sdr)
    return [("HEVC 10-bit", v["codec_name"] == "hevc" and v["pix_fmt"] == "yuv420p10le", (v["codec_name"], v["pix_fmt"])),
            ("PQ transfer + BT.2020 primaries read back", (v.get("color_transfer"), v.get("color_primaries")) == ("smpte2084", "bt2020"),
             (v.get("color_transfer"), v.get("color_primaries"))),
            ("social default stays 8-bit SDR", vs["pix_fmt"] == "yuv420p", vs["pix_fmt"])]


# ---------------------------------------------------------------- FMT-24
def hls(work, per_audio=True):
    d = work / ("hls" if per_audio else "hls_bad")
    d.mkdir(exist_ok=True)
    amap = ["-map", "0:a"] * 3 if per_audio else ["-map", "0:a"]
    args = ["-f", "lavfi", "-i", "testsrc2=size=96x54:rate=30:duration=8", "-f", "lavfi", "-i", "sine=d=8:sample_rate=48000",
            "-filter_complex", "[0:v]split=3[a][b][c];[a]scale=96:54[v0];[b]scale=64:36[v1];[c]scale=32:18[v2]",
            "-map", "[v0]", "-map", "[v1]", "-map", "[v2]"]
    args = args[:8] + args[8:]
    r = ff(*args, *["-map", "1:a"] * (3 if per_audio else 1), "-c:v", "libx264", "-preset", "ultrafast", "-g", 60, "-keyint_min", 60, "-sc_threshold", 0,
           "-b:v:0", "5000k", "-b:v:1", "2800k", "-b:v:2", "1400k", "-c:a", "aac", "-b:a", "96k",
           "-f", "hls", "-hls_time", 4, "-hls_playlist_type", "vod", "-master_pl_name", "master.m3u8",
           "-var_stream_map", "v:0,a:0 v:1,a:1 v:2,a:2", str(d / "v%v.m3u8"), ok=False)
    return d, r


def fmt_24(work):
    d, r = hls(work)
    master = (d / "master.m3u8").read_text() if (d / "master.m3u8").exists() else ""
    v0 = (d / "v0.m3u8").read_text() if (d / "v0.m3u8").exists() else ""
    bw = [int(x) for x in re.findall(r"BANDWIDTH=(\d+)", master)]
    _, bad = hls(work, per_audio=False)
    return [("ladder encodes", r.returncode == 0, r.stderr[-200:]),
            ("master.m3u8 has 3 STREAM-INF", master.count("#EXT-X-STREAM-INF") == 3, master.count("#EXT-X-STREAM-INF")),
            ("bandwidths ordered 5000k > 2800k > 1400k", len(bw) == 3 and bw == sorted(bw, reverse=True), bw),
            ("4 s segments: TARGETDURATION 4, two segments for 8 s", "#EXT-X-TARGETDURATION:4" in v0 and v0.count("#EXTINF") == 2, v0.count("#EXTINF")),
            ("gotcha reproduced: one shared audio map fails", bad.returncode != 0, bad.stderr[-120:])]


# ---------------------------------------------------------------- FMT-27
def loop_seam(x):
    return float(abs(x[0] - x[-1]))


def music_receipt_ok(r):
    if r.get("provider") == "elevenlabs" and r.get("plan") == "free" and r.get("use") == "commercial":
        return False
    return all(r.get(k) for k in ("provider", "plan", "rights", "rendered_at"))


def fmt_27(work):
    sr = 48000
    n = sr  # 1 s, 440 Hz -> 440 whole cycles
    t = np.arange(n) / sr
    good = np.sin(2 * np.pi * 440 * t)
    bad = np.sin(2 * np.pi * 437.3 * t)
    (work / "loop.raw").write_bytes((good * 30000).astype("<i2").tobytes())
    ff("-f", "s16le", "-ar", sr, "-ac", 1, "-i", work / "loop.raw", "-c:a", "pcm_s16le", work / "loop.wav")
    ff("-i", work / "loop.wav", "-c:a", "libopus", "-b:a", "96k", work / "loop.opus")
    step = 2 * np.pi * 440 / sr
    wrap_good = abs(math.sin(2 * np.pi * 440 * n / sr) - good[0])
    wrap_bad = abs(math.sin(2 * np.pi * 437.3 * n / sr) - bad[0])
    o = next(s for s in probe(work / "loop.opus")["streams"] if s["codec_type"] == "audio")
    return [("whole-cycle loop wraps seamlessly (next sample == first)", wrap_good < 1e-9, wrap_good),
            ("non-integer cycle loop clicks at the seam", wrap_bad > step * 2, round(wrap_bad, 4)),
            ("opus and pcm_s16le written", o["codec_name"] == "opus" and vstream_or_none(work / "loop.wav") == "pcm_s16le", o["codec_name"]),
            ("free ElevenLabs plan refused for commercial use", not music_receipt_ok({"provider": "elevenlabs", "plan": "free", "use": "commercial", "rights": "x", "rendered_at": "t"}), "refused"),
            ("paid receipt with plan/rights/time accepted", music_receipt_ok({"provider": "elevenlabs", "plan": "creator", "use": "commercial", "rights": "commercial", "rendered_at": "2026-11-03T10:00Z"}), "ok")]


def vstream_or_none(p):
    return probe(p)["streams"][0]["codec_name"]


# ---------------------------------------------------------------- FMT-28
def appstore_ok(meta):
    v, a = meta["v"], meta["a"]
    fps = eval(v["r_frame_rate"])
    errs = []
    if v["codec_name"] != "h264":
        errs.append("codec")
    if fps > 30:
        errs.append("fps")
    if int(a["channels"]) != 2 or a["sample_rate"] not in ("44100", "48000"):
        errs.append("audio")
    if not 15 <= meta["dur"] <= 30:
        errs.append("duration")
    return errs


def fmt_28(work):
    out = work / "preview.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=size=64x36:rate=60:duration=1", "-f", "lavfi", "-i", "sine=d=1:sample_rate=48000",
       "-c:v", "libx264", "-preset", "ultrafast", "-b:v", "11M", "-maxrate", "12M", "-bufsize", "12M", "-r", 30,
       "-c:a", "aac", "-b:a", "256k", "-ar", 48000, "-ac", 2, out)
    p = probe(out)
    meta = {"v": next(s for s in p["streams"] if s["codec_type"] == "video"), "a": next(s for s in p["streams"] if s["codec_type"] == "audio"),
            "dur": float(p["format"]["duration"])}
    errs = appstore_ok(meta)
    long = dict(meta, dur=20.0)
    return [("60 fps source delivered at 30 fps", eval(meta["v"]["r_frame_rate"]) == 30, meta["v"]["r_frame_rate"]),
            ("stereo AAC 48 kHz", (meta["a"]["channels"], meta["a"]["sample_rate"]) == (2, "48000"), (meta["a"]["channels"], meta["a"]["sample_rate"])),
            ("1 s clip rejected (15-30 s rule)", errs == ["duration"], errs),
            ("same encode at 20 s passes the spec", appstore_ok(long) == [], appstore_ok(long))]


# ---------------------------------------------------------------- FMT-29
def fmt_29(work):
    src = testclip(work, size="160x90", dur=1)
    poster = work / "poster.jpg"
    ff("-i", src, "-frames:v", 1, poster)
    img = Image.new("RGB", (1600, 900))
    a = np.zeros((900, 1600, 3), np.uint8)
    a[..., 0] = np.linspace(0, 255, 1600)[None]
    a[..., 1] = np.linspace(0, 255, 900)[:, None]
    img = Image.fromarray(a)
    widths = [1600, 1200, 900]
    for w in widths:
        img.resize((w, w * 9 // 16)).save(work / f"hero_{w}.webp", quality=80)
        img.resize((w, w * 9 // 16)).save(work / f"hero_{w}.jpg", quality=80)
    srcset = ", ".join(f"hero_{w}.webp {w}w" for w in widths)
    html = (f'<picture><source type="image/avif" srcset="{srcset.replace(".webp", ".avif")}"><source type="image/webp" srcset="{srcset}">'
            f'<img src="hero_1200.jpg" width="1600" height="900" fetchpriority="high" alt=""></picture>'
            f'<video poster="poster.jpg" width="160" height="90" muted playsinline></video>')
    (work / "embed.html").write_text(html)
    from bs4 import BeautifulSoup
    s = BeautifulSoup(html, "html.parser")
    order = [x["type"] for x in s.find_all("source")]
    sizes = sorted(Image.open(work / f"hero_{w}.webp").size[0] for w in widths)
    return [("poster is one frame of the clip", Image.open(poster).size == (160, 90), Image.open(poster).size),
            ("AVIF -> WebP -> JPEG fallback order", order == ["image/avif", "image/webp"] and s.img["src"].endswith(".jpg"), order),
            ("WebP at 900/1200/1600 widths", sizes == [900, 1200, 1600], sizes),
            ("explicit width/height on img and video (CLS)", all(t.get("width") and t.get("height") for t in (s.img, s.video)), "dims"),
            ("hero fetchpriority high", s.img.get("fetchpriority") == "high", s.img.get("fetchpriority"))]


# ---------------------------------------------------------------- FMT-30
def fmt_30(work):
    src = testclip(work, size="1280x820", dur=0.5, rate=30)
    mp4 = work / "clip.mp4"
    ff("-i", src, "-vf", "scale=1280:-2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", 26, "-preset", "veryfast", "-movflags", "+faststart", "-an", mp4)
    pal = work / "pal.png"
    ff("-i", mp4, "-vf", "fps=12,scale=960:-1:flags=lanczos,palettegen", pal)
    gif = work / "clip.gif"
    ff("-i", mp4, "-i", pal, "-lavfi", "fps=12,scale=960:-1:flags=lanczos[x];[x][1:v]paletteuse", gif)
    g = Image.open(gif)
    n = getattr(g, "n_frames", 1)
    dur = g.info.get("duration")
    streams = [s["codec_type"] for s in probe(mp4)["streams"]]
    return [("MP4 has no audio (-an)", streams == ["video"], streams),
            ("GIF 960 px wide", g.size[0] == 960, g.size),
            ("GIF at 12 fps: 6 frames in 0.5 s (~83 ms each)", n == 6 and dur in (80, 83, 90), (n, dur)),
            ("palette is at most 256 colours", Image.open(pal).size == (16, 16), Image.open(pal).size)]


# ---------------------------------------------------------------- FMT-31
PLATFORMS = {"tiktok": {"size": (1080, 1920), "max_s": 600, "max_mb": 287, "v": 12000, "a": 192},
             "reels": {"size": (1080, 1920), "max_s": 180, "max_mb": 250}, "shorts": {"size": (1080, 1920), "max_s": 180, "max_mb": 256},
             "youtube": {"size": (1920, 1080), "max_s": None, "max_mb": 2000, "v": 16000, "a": 256},
             "x": {"size": (1280, 720), "max_s": 140, "max_mb": 512, "v": 8000, "a": 160},
             "whatsapp": {"size": (720, 1280), "max_s": 30, "max_mb": 16, "v": 2200, "a": 96},
             "linkedin": {"size": (1080, 1080), "max_s": 600, "max_mb": 200, "v": 8000}, "snapchat": {"size": (1080, 1920), "max_s": 60, "max_mb": 32, "v": 6000, "a": 128}}


def platform_warnings(duration):
    return {p: [f"over {s['max_s']} s"] for p, s in PLATFORMS.items() if s["max_s"] and duration > s["max_s"]}


def fmt_31(work):
    src = testclip(work, size="128x72", dur=1, audio=True)
    out = work / "FILM_whatsapp.mp4"
    s = PLATFORMS["whatsapp"]
    ff("-i", src, "-vf", f"scale={s['size'][0]}:{s['size'][1]}:force_original_aspect_ratio=increase,crop={s['size'][0]}:{s['size'][1]}",
       "-c:v", "libx264", "-profile:v", "high", "-preset", "veryfast", "-crf", 20, "-maxrate", f"{s['v']}k", "-bufsize", f"{2 * s['v']}k",
       "-c:a", "aac", "-b:a", f"{s['a']}k", "-ar", 48000, "-movflags", "+faststart", out)
    v = vstream(out)
    warn = platform_warnings(45)
    save_json(work, "FILM.platforms.json", {"whatsapp": {"file": out.name, "bytes": out.stat().st_size}, "warnings": warn})
    mb = out.stat().st_size / 1e6
    return [("whatsapp render 720x1280 high profile", (v["width"], v["height"], v["profile"]) == (720, 1280, "High"), (v["width"], v["height"], v["profile"])),
            ("within whatsapp 16 MB", mb <= 16, round(mb, 3)),
            ("a 45 s film warns for whatsapp (30 s) only", warn == {"whatsapp": ["over 30 s"]}, warn),
            ("8 platforms in the table", len(PLATFORMS) == 8, list(PLATFORMS))]


# ---------------------------------------------------------------- FMT-32
def fmt_32(work):
    src = testclip(work, size="320x180", dur=1, rate=30)
    outs = {}
    for asp, (w, h) in {"9x16": (90, 160), "1x1": (120, 120), "16x9": (160, 90)}.items():
        p = work / f"FILM_{asp}.mp4"
        ff("-i", src, "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}", "-c:v", "libx264", "-preset", "ultrafast", p)
        v = vstream(p)
        outs[asp] = (v["width"], v["height"])
    ff("-ss", 0.5, "-i", src, "-frames:v", 1, work / "FILM_poster.jpg")
    ff("-i", src, "-vf", "fps=12,scale=480:-1:flags=lanczos,palettegen=max_colors=160", work / "pal.png")
    ff("-i", src, "-i", work / "pal.png", "-lavfi", "fps=12,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4", work / "FILM.gif")
    ff("-i", src, "-vf", "fps=15,scale=540:-1", "-c:v", "libwebp_anim", "-quality", 70, "-loop", 0, work / "FILM.webp")
    g = Image.open(work / "FILM.gif")
    cols = len(np.unique(np.asarray(Image.open(work / "pal.png").convert("RGB")).reshape(-1, 3), axis=0))
    g.seek(0)
    first = len(g.convert("RGB").getcolors(1 << 16))
    wp = Image.open(work / "FILM.webp")
    save_json(work, "FILM.export.json", {"aspects": outs})
    return [("three aspects with exact ratios", outs == {"9x16": (90, 160), "1x1": (120, 120), "16x9": (160, 90)}, outs),
            ("GIF 480 px, 12 frames for 1 s", g.size[0] == 480 and g.n_frames == 12, (g.size, g.n_frames)),
            ("GIF palette <= 160 colours (palette and first frame)", cols <= 160 and first <= 160, (cols, first)),
            ("WebP 540 px, 15 frames", wp.size[0] == 540 and getattr(wp, "n_frames", 1) == 15, (wp.size, getattr(wp, "n_frames", 1))),
            ("poster written", (work / "FILM_poster.jpg").stat().st_size > 0, "poster")]


# ---------------------------------------------------------------- FMT-34
LIMITS = {"tiktok": {"chars": 4000, "secs": 600}, "reels": {"chars": 2200, "secs": 180, "tags": 5}, "x": {"chars": 280, "secs": 140, "images": 4},
          "linkedin": {"chars": 3000, "visible": 210}, "facebook": {"chars": 63206}}


def post_check(platform, caption, secs=0, tags=0, images=0):
    L, errs = LIMITS[platform], []
    if len(caption) > L["chars"]:
        errs.append("chars")
    if "secs" in L and secs > L["secs"]:
        errs.append("secs")
    if "tags" in L and tags > L["tags"]:
        errs.append("tags")
    if "images" in L and images > L["images"]:
        errs.append("images")
    return errs


def fmt_34(work):
    res = {"x_281": post_check("x", "a" * 281), "x_280": post_check("x", "a" * 280), "reels_6tags": post_check("reels", "hi", tags=6),
           "x_5img": post_check("x", "hi", images=5), "tiktok_601s": post_check("tiktok", "hi", secs=601)}
    save_json(work, "limits.json", res)
    fold = "x" * 250
    return [("X: 280 chars ok, 281 rejected", res["x_280"] == [] and res["x_281"] == ["chars"], res),
            ("Reels: 6 hashtags rejected (max 5)", res["reels_6tags"] == ["tags"], res["reels_6tags"]),
            ("X: 5 images rejected (max 4)", res["x_5img"] == ["images"], res["x_5img"]),
            ("TikTok: 601 s rejected", res["tiktok_601s"] == ["secs"], res["tiktok_601s"]),
            ("LinkedIn shows 210 chars before 'see more'", fold[:LIMITS["linkedin"]["visible"]] == "x" * 210, LIMITS["linkedin"]["visible"])]


# ---------------------------------------------------------------- FMT-35
CTA_WORDS = ("احفظ", "شارك", "علّق", "تابع", "save", "share", "comment", "follow")


def hook_type(line):
    if "?" in line or "؟" in line:
        return "question"
    if re.search(r"\d|[٠-٩]", line):
        return "number"
    if re.search(r"\b(but|not|لكن|ليس|لا)\b", line, re.I):
        return "contradiction"
    if re.search(r"(saved|doubled|وفّر|ضاعف|result)", line, re.I):
        return "result"
    return None


def post_rules(text):
    tags = re.findall(r"#\w+", text)
    lines = [l for l in text.splitlines() if l.strip()]
    ctas = sum(1 for w in CTA_WORDS if w in text.lower())
    return {"tags": len(tags) <= 5, "cta": ctas == 1, "hook": hook_type(lines[0]) is not None}


def fmt_35(work):
    good = "٣ أخطاء تكلّفك عملاء\nالشرح في الفيديو\nاحفظ المنشور\n#تسويق #مبيعات"
    bad = "Welcome to our channel\nsave this and share it and follow\n#a #b #c #d #e #f"
    g, b = post_rules(good), post_rules(bad)
    save_json(work, "rules.json", {"good": g, "bad": b})
    return [("good post passes all rules", all(g.values()), g),
            ("6 tags rejected", not b["tags"], b),
            ("three CTAs rejected (one CTA rule)", not b["cta"], b),
            ("bland opener has no hook", not b["hook"], b),
            ("hook types: number / question", hook_type("٣ أخطاء") == "number" and hook_type("Why does it fail?") == "question", "types")]


# ---------------------------------------------------------------- FMT-36
def placeholders(s):
    return sorted(re.findall(r"{\w+}", s))


def tm_lookup(src, memory, lo=0.75):
    best = max(((difflib.SequenceMatcher(None, src, k).ratio(), k) for k in memory), default=(0, None))
    return (memory[best[1]], round(best[0], 3)) if best[0] >= lo else (None, round(best[0], 3))


def localise(scene, strings, glossary):
    out, errs = {}, []
    for key, src in scene.items():
        tr = strings.get(key)
        if tr is None:
            errs.append(f"missing {key}")
            continue
        if placeholders(tr) != placeholders(src):
            errs.append(f"placeholder {key}")
        for term in glossary:
            if term in src and term not in tr:
                errs.append(f"glossary {key}")
        out[key] = tr
    return out, errs


def refit(text, max_w, size, arabic):
    s = size
    while font(s, arabic).getlength(text) > max_w and s > 10:
        s -= 1
    return s


def fmt_36(work):
    scene = {"title": "KOSIF saves {n} hours", "cta": "Try KOSIF"}
    ar = {"title": "KOSIF يوفر {n} ساعات", "cta": "جرّب KOSIF"}
    broken = {"title": "يوفر ساعات", "cta": "جرّب"}
    out, errs = localise(scene, ar, ["KOSIF"])
    _, berrs = localise(scene, broken, ["KOSIF"])
    mem = {"Try KOSIF today": "جرّب KOSIF اليوم"}
    hit, score = tm_lookup("Try KOSIF now", mem)
    miss, mscore = tm_lookup("Completely unrelated sentence", mem)
    s_en = refit("KOSIF saves 12 hours", 200, 40, False)
    save_json(work, "locales.json", {"ar": out})
    return [("Arabic version passes placeholder + glossary checks", errs == [], errs),
            ("dropped {n} and translated brand caught", "placeholder title" in berrs and "glossary cta" in berrs, berrs),
            ("fuzzy TM hit >= 75%", hit == "جرّب KOSIF اليوم" and score >= 0.75, score),
            ("unrelated sentence below 75% -> no TM", miss is None and mscore < 0.75, mscore),
            ("refit shrinks to fit 200 px", font(s_en).getlength("KOSIF saves 12 hours") <= 200 < font(s_en + 1).getlength("KOSIF saves 12 hours"), s_en)]


# ---------------------------------------------------------------- FMT-37
def batch_render(rows, template, out_pat, work):
    done, errs = [], []
    keys = set(re.findall(r"{(\w+)}", template))
    for r in rows:
        missing = keys - set(r)
        if missing:
            errs.append((r.get("name"), sorted(missing)))
            continue
        text = template.format(**r)
        im = Image.new("RGB", (160, 90), tuple(int(r["color"][i:i + 2], 16) for i in (1, 3, 5)))
        ImageDraw.Draw(im).text((8, 36), text, font=font(14), fill="white")
        p = work / out_pat.format(**r)
        p.parent.mkdir(parents=True, exist_ok=True)
        im.save(p)
        done.append(p)
    return done, errs


def fmt_37(work):
    rows = [{"name": "riyadh", "city": "Riyadh", "color": "#0a5c36"}, {"name": "jeddah", "city": "Jeddah", "color": "#1b2a49"},
            {"name": "broken", "color": "#000000"}]
    done, errs = batch_render(rows, "Open in {city}", "renders/{name}.png", work)
    px = Image.open(work / "renders/jeddah.png").getpixel((2, 2))
    return [("one render per valid row, named from the row", sorted(p.name for p in done) == ["jeddah.png", "riyadh.png"], [p.name for p in done]),
            ("row variables reach the render (jeddah colour #1b2a49)", px == (0x1b, 0x2a, 0x49), px),
            ("row missing {city} reported, not rendered", errs == [("broken", ["city"])], errs)]


# ---------------------------------------------------------------- FMT-43
def envelope_ok(obj):
    need = {"title", "analysis", "confidence", "sources", "json", "next"}
    if not need <= set(obj):
        return False
    if not 0 <= obj["confidence"] <= 1 or not isinstance(obj["sources"], list):
        return False
    return {"tool_output", "prompts", "imageSpecs"} <= set(obj["json"])


def fmt_43(work):
    instr = "You are KOSIF. " * 266
    good = {"title": "t", "analysis": "a", "confidence": 0.8, "sources": ["s"], "json": {"tool_output": {}, "prompts": [], "imageSpecs": []}, "next": "n"}
    bad = dict(good, confidence=1.4)
    (work / "instructions.md").write_text(instr)
    save_json(work, "envelope.json", good)
    return [("instructions within 8,000 chars (3,990 here)", len(instr) <= 8000 and len(instr) == 3990, len(instr)),
            ("well-formed envelope accepted", envelope_ok(good), "ok"),
            ("confidence 1.4 rejected", not envelope_ok(bad), "bad"),
            ("missing json.imageSpecs rejected", not envelope_ok(dict(good, json={"tool_output": {}, "prompts": []})), "bad"),
            ("round trip through JSON parser", json.loads((work / "envelope.json").read_text()) == good, "parsed")]


# ---------------------------------------------------------------- FMT-44
def fmt_44(work):
    src = testclip(work, size="64x36", dur=1, audio=True)
    pick = work / "pick.png"
    ff("-ss", 0.5, "-i", src, "-frames:v", 1, pick)
    out = work / "baked.mp4"
    ff("-i", src, "-i", pick, "-filter_complex", "[0:v][1:v]overlay=enable='eq(n,0)'", "-c:v", "libx264", "-preset", "ultrafast",
       "-pix_fmt", "yuv420p", "-c:a", "copy", out)

    def count(p):
        return int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames",
                                   "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())

    def amd5(p):
        return subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True).stdout.strip()
    f_out = frames_of(out, 64, 36).astype(int)
    f_src = frames_of(src, 64, 36).astype(int)
    d0_pick = np.abs(f_out[0] - f_src[15]).mean()
    d1 = np.abs(f_out[1] - f_src[1]).mean()
    return [("frame count unchanged", count(out) == count(src), (count(out), count(src))),
            ("frame 0 now shows the 0.5 s poster", d0_pick < 6, round(d0_pick, 2)),
            ("frame 1 untouched", d1 < 6, round(d1, 2)),
            ("audio copied byte for byte (md5)", amd5(out) == amd5(src), amd5(out)[:30])]


# ---------------------------------------------------------------- FMT-45
def fmt_45(work):
    import cv2
    frames = []
    rng = np.random.default_rng(1)
    for i in range(30):
        base = np.full((36, 64), 40 if i < 10 else 140 if i < 20 else 220, np.uint8)
        sharp = (rng.random((36, 64)) * 60).astype(np.uint8)
        f = base + sharp // 6
        if i == 25:
            f = base.copy()
            f[::2, ::2] = base[0, 0] - 25
            f[1::2, 1::2] = base[0, 0] + 25
        frames.append(np.dstack([f] * 3))
    raw = work / "clip.rgb"
    raw.write_bytes(b"".join(f.tobytes() for f in frames))
    clip = work / "clip.mp4"
    ff("-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "64x36", "-r", 30, "-i", raw, "-c:v", "libx264", "-preset", "ultrafast", "-crf", 0, "-pix_fmt", "yuv444p", clip)
    raw.unlink()
    err = ff_stderr("-i", clip, "-vf", "select='gt(scene,0.3)',showinfo", "-vsync", "vfr", "-f", "null", "-")
    cuts = [round(float(x) * 30) for x in re.findall(r"pts_time:\s*([\d.]+)", err)]
    dec = frames_of(clip, 64, 36)
    sharp = [cv2.Laplacian(cv2.cvtColor(f, cv2.COLOR_RGB2GRAY), cv2.CV_64F).var() for f in dec]
    best = int(np.argmax(sharp))
    ff("-i", clip, "-vf", "select='not(mod(n,10))',tile=3x1", "-frames:v", 1, work / "contact.png")
    return [("scene > 0.3 finds the 2 planted cuts (frames 10, 20)", cuts == [10, 20], cuts),
            ("Laplacian variance picks the planted sharp frame 25", best == 25, best),
            ("contact sheet tiles 3 frames (192x36)", Image.open(work / "contact.png").size == (192, 36), Image.open(work / "contact.png").size)]


# ---------------------------------------------------------------- FMT-46
def fmt_46(work):
    src = work / "film.mp4"
    ff("-f", "lavfi", "-i", "color=c=red:size=128x72:rate=10:duration=1", "-f", "lavfi", "-i", "color=c=blue:size=128x72:rate=10:duration=2",
       "-filter_complex", "[0][1]concat=n=2:v=1", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", src)
    fr = work / "frame.png"
    ff("-ss", 2, "-i", src, "-frames:v", 1, fr)
    im = Image.open(fr).convert("RGB").resize((1280, 720))
    d = ImageDraw.Draw(im)
    d.text((1240, 600), "سر الإنتاج", font=font(96, True), fill="white", anchor="rs", stroke_width=6, stroke_fill="black", **rtl_kw())
    im.save(work / "cover.jpg", quality=90)
    a = np.asarray(im)
    white = np.all(a > 240, axis=2)
    xs = np.nonzero(white.any(axis=0))[0]
    return [("cover is 1280x720", im.size == (1280, 720), im.size),
            ("frame taken at 2 s (blue segment)", a[50, 50, 2] > 180 and a[50, 50, 0] < 60, tuple(a[50, 50])),
            ("Arabic title drawn, right-aligned at x<=1240", white.sum() > 2000 and xs.max() <= 1242, (int(white.sum()), int(xs.max())))]


# ---------------------------------------------------------------- FMT-47
def ab_valid(a, b):
    diff = [k for k in a if a[k] != b.get(k)]
    return len(diff) == 1, diff


def fmt_47(work):
    concepts = [{"bg": "rim light teal", "face": "surprised", "title": "سر واحد", "crop": "mcu"},
                {"bg": "warm studio", "face": "smiling", "title": "٣ خطوات", "crop": "mcu"},
                {"bg": "dark contrast", "face": "serious", "title": "لا تفعل هذا", "crop": "close"}]
    variant = dict(concepts[0], title="سر لا يقال")
    bad = dict(concepts[0], title="x", bg="y")
    save_json(work, "concepts.json", {"concepts": concepts, "test_hours": 48, "size": [1280, 720]})
    ok, diff = ab_valid(concepts[0], variant)
    nok, ndiff = ab_valid(concepts[0], bad)
    return [("three concepts", len(concepts) == 3, len(concepts)),
            ("A/B varies exactly one element (title)", ok and diff == ["title"], diff),
            ("two changed elements rejected", not nok and sorted(ndiff) == ["bg", "title"], ndiff),
            ("concepts differ from each other on >= 3 fields", all(sum(a[k] != b[k] for k in a) >= 3 for i, a in enumerate(concepts) for b in concepts[i + 1:]), "distinct")]


# ---------------------------------------------------------------- FMT-48
def thumb_rules(thumb_text, title):
    words_t = set(re.findall(r"\w+", thumb_text.lower()))
    words_title = set(re.findall(r"\w+", title.lower()))
    return {"thumb_words": 1 <= len(thumb_text.split()) <= 3, "title_len": len(title) <= 60, "no_overlap": not (words_t & words_title)}


def fmt_48(work):
    pairs = [("سر واحد", "كيف ضاعفت مبيعاتي في شهر بدون إعلانات"), ("لا تفعل هذا", "أخطاء التسعير التي يقع فيها كل مستقل"),
             ("أنا كنت مثلك", "رحلتي من موظف إلى صاحب مشروع ناجح")]
    res = [thumb_rules(a, b) for a, b in pairs]
    bad = thumb_rules("مبيعاتي في شهر واحد", "كيف ضاعفت مبيعاتي في شهر بدون إعلانات ولا ميزانية ولا فريق ولا خبرة سابقة")
    save_json(work, "pairs.json", {"pairs": pairs, "checks": res})
    return [("3 pairs at different angles all pass", len(res) == 3 and all(all(r.values()) for r in res), res),
            ("Arabic counted in words: 'لا تفعل هذا' = 3 words", len("لا تفعل هذا".split()) == 3, 3),
            ("4-word thumbnail rejected", not bad["thumb_words"], bad),
            ("title over 60 chars rejected", not bad["title_len"], bad),
            ("shared words between thumb and title rejected", not bad["no_overlap"], bad)]


# ---------------------------------------------------------------- FMT-49
def og_direction(topic):
    return {"technical": ("dark", "#0d1117"), "tutorial": ("light", "#f7f7f2"), "conceptual": ("gradient", "#1b2a49")}[topic]


def og_image(title, topic, W=1200, H=630):
    if len(title) > 40:
        raise ValueError("title over 40 chars")
    mode, bg = og_direction(topic)
    im = Image.new("RGB", (W, H), tuple(int(bg[i:i + 2], 16) for i in (1, 3, 5)))
    d = ImageDraw.Draw(im)
    fg = (255, 255, 255) if mode != "light" else (20, 20, 20)
    d.text((80, H // 2), title, font=font(64), fill=fg, anchor="lm")
    d.text((80, H - 80), "kosif.dev", font=font(28), fill=fg, anchor="lm")
    return im, {"fonts": 1, "mode": mode}


def fmt_49(work):
    im, meta = og_image("Ship motion films from code", "technical")
    im.save(work / "og.png")
    try:
        og_image("x" * 41, "tutorial")
        rej = False
    except ValueError:
        rej = True
    a = np.asarray(im)
    return [("OG is exactly 1200x630", im.size == (1200, 630), im.size),
            ("technical -> dark background", tuple(a[5, 5]) == (13, 17, 23) and meta["mode"] == "dark", tuple(a[5, 5])),
            ("<= 2 fonts", meta["fonts"] <= 2, meta["fonts"]),
            ("41-char title refused", rej, rej),
            ("text drawn inside the frame (no overflow)", np.nonzero(a.max(axis=2).max(axis=0) > 200)[0].max() < 1200 - 40, "inside")]


# ---------------------------------------------------------------- FMT-50
def mark(size):
    im = Image.new("RGBA", (size, size), (29, 24, 20, 255))
    d = ImageDraw.Draw(im)
    d.ellipse([size * 0.25, size * 0.25, size * 0.75, size * 0.75], fill=(232, 189, 118, 255))
    return im


def fmt_50(work):
    big = mark(512)
    big.save(work / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    for s, n in ((180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        mark(s).save(work / n)
    for (w, h), n in (((1200, 630), "og.png"), ((1200, 675), "x.png")):
        Image.new("RGB", (w, h), (29, 24, 20)).save(work / n)
    (work / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><style>circle{fill:#1d1814}'
                                      '@media (prefers-color-scheme:dark){circle{fill:#e8bd76}}</style><circle cx="16" cy="16" r="8"/></svg>')
    manifest = {"lang": "ar", "dir": "rtl", "theme_color": "#1d1814", "icons": [{"src": "icon-192.png", "sizes": "192x192"}, {"src": "icon-512.png", "sizes": "512x512"}]}
    save_json(work, "manifest.webmanifest", manifest)
    ico = Image.open(work / "favicon.ico")
    sizes = sorted(ico.info.get("sizes", set()))
    return [("favicon.ico holds 16/32/48", sizes == [(16, 16), (32, 32), (48, 48)], sizes),
            ("apple 180, PWA 192/512", [Image.open(work / n).size[0] for n in ("apple-touch-icon.png", "icon-192.png", "icon-512.png")] == [180, 192, 512], "sizes"),
            ("OG 1200x630 and X 1200x675", Image.open(work / "og.png").size == (1200, 630) and Image.open(work / "x.png").size == (1200, 675), "og"),
            ("favicon.svg switches in dark mode", "prefers-color-scheme:dark" in (work / "favicon.svg").read_text(), "svg"),
            ("manifest Arabic RTL with theme_color", (manifest["lang"], manifest["dir"], manifest["theme_color"]) == ("ar", "rtl", "#1d1814"), manifest["dir"])]


# ---------------------------------------------------------------- FMT-51
def resolve_vars(css_vars, value):
    m = re.fullmatch(r"var\((--[\w-]+)\)", value.strip())
    if not m:
        return value
    if m.group(1) not in css_vars:
        raise KeyError(m.group(1))
    return resolve_vars(css_vars, css_vars[m.group(1)])


def export_fig(series, colour, work, fmt="png", scale=2, css_vars=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    try:
        col = resolve_vars(css_vars or {}, colour)
    except KeyError:
        fmt, col = "svg", "#000000"
    fig = plt.figure(figsize=(3, 2), dpi=50)
    plt.bar(range(len(series)), series, color=col)
    p = work / f"chart.{fmt}"
    fig.savefig(p, dpi=50 * scale if fmt == "png" else 50, format=fmt)
    plt.close(fig)
    return p


def fmt_51(work):
    v = {"--accent": "var(--brand)", "--brand": "#d9530e"}
    png = export_fig([3, 5, 2], "var(--accent)", work, css_vars=v)
    w, h = Image.open(png).size
    svgp = export_fig([3, 5, 2], "var(--accent)", work, fmt="svg", css_vars=v)
    svg = svgp.read_text()
    fb = export_fig([1, 2], "var(--missing)", work / "", css_vars=v)
    return [("PNG at 2x (300x200 for a 150x100 figure)", (w, h) == (300, 200), (w, h)),
            ("CSS var resolved through aliases to #d9530e in SVG", "#d9530e" in svg and "var(" not in svg, "#d9530e" in svg),
            ("unresolvable colour falls back to SVG", fb.suffix == ".svg", fb.name)]


# ---------------------------------------------------------------- FMT-52
def colour_svg(img: Image.Image, scale=2):
    a = np.asarray(img.convert("RGB"))
    paths = []
    for col in np.unique(a.reshape(-1, 3), axis=0):
        mask = np.all(a == col, axis=2)
        d = []
        for y, x in zip(*np.nonzero(mask)):
            d.append(f"M{x * scale} {y * scale}h{scale}v{scale}h-{scale}z")
        paths.append(f'<path fill="#{col[0]:02x}{col[1]:02x}{col[2]:02x}" fill-rule="evenodd" d="{"".join(d)}"/>')
    h, w = a.shape[:2]
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w * scale} {h * scale}">' + "".join(paths) + "</svg>"


def painting(W, H):
    im = Image.new("RGB", (W, H), (250, 245, 235))
    d = ImageDraw.Draw(im)
    d.ellipse([W * .2, H * .2, W * .5, H * .7], fill=(200, 40, 40))
    d.rectangle([W * .55, H * .3, W * .85, H * .8], fill=(30, 60, 150))
    return im


def fmt_52(work):
    painting(1200, 800).save(work / "painting.png")
    hi = painting(round(1200 * 3.2), round(800 * 3.2))
    hi.save(work / "painting_4k.png", compress_level=1)
    small = painting(24, 16)
    svg = colour_svg(small, 2)
    (work / "painting.svg").write_text(svg)
    ncol = len(np.unique(np.asarray(small).reshape(-1, 3), axis=0))
    film = work / "painting.mp4"
    ff("-loop", 1, "-i", work / "painting.png", "-t", 0.2, "-r", 30, "-vf", "scale=120:80", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", film)
    v = vstream(film)
    return [("high-res = 1200x800 x 3.2 = 3840x2560", hi.size == (3840, 2560), hi.size),
            ("SVG: one even-odd path per colour", svg.count("<path") == ncol and svg.count('fill-rule="evenodd"') == ncol, (svg.count("<path"), ncol)),
            ("SVG scale 2 viewBox 48x32", 'viewBox="0 0 48 32"' in svg, "48x32"),
            ("film 30 fps H.264", v["codec_name"] == "h264" and v["r_frame_rate"] == "30/1", v["r_frame_rate"])]


# ---------------------------------------------------------------- FMT-53
def mm_px(mm, dpi):
    return round(mm / 25.4 * dpi)


def fmt_53(work):
    import cv2
    import segno
    qr = segno.make("https://kosif.dev/r/2026-11", error="m", micro=False, boost_error=False)
    qr.save(work / "qr.png", scale=6, border=4)
    img = cv2.imread(str(work / "qr.png"))
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    rw = mm_px(80, 203.2)  # 8 dots/mm thermal head
    rec = Image.new("L", (rw, 400), 255)
    q = Image.open(work / "qr.png").convert("L")
    rec.paste(q, ((rw - q.width) // 2, 200))
    rec.save(work / "receipt.png")
    label = Image.new("L", (mm_px(60, 300), mm_px(40, 300)), 255)
    label.save(work / "label.png")
    css = "@media print{.topbar,.rail{display:none}.panel{break-inside:avoid;box-shadow:none}body{font:11pt/1.6 Amiri,'Noto Naskh Arabic';color:#2b1a0f}}"
    (work / "print.css").write_text(css)
    return [("QR ECC level M", qr.error == "M", qr.error),
            ("QR decodes back to the payload (cv2)", data == "https://kosif.dev/r/2026-11", data),
            ("80 mm receipt at 203 dpi (8 dots/mm) = 640 px", rw == 640 and rec.width == 640, rw),
            ("60x40 mm label at 300 dpi = 709x472", label.size == (709, 472), label.size),
            ("print CSS: 11pt/1.6, chrome hidden", "11pt/1.6" in css and "display:none" in css, "css")]


# ---------------------------------------------------------------- FMT-54
def slides_of(doc):
    slides, cur = [], None
    for line in doc.splitlines():
        m = re.match(r"^(#{1,2})\s+(.*)", line)
        if m:
            cur = {"title": m.group(2), "level": len(m.group(1)), "body": []}
            slides.append(cur)
        elif line.strip() and cur:
            cur["body"].append(line.strip())
    return slides


def fmt_54(work):
    doc = "# تقرير الربع\nملخص\n## المبيعات\nارتفعت ١٢٪\n## التكاليف\nثابتة\n## الخطوة التالية\nتوسع"
    s = slides_of(doc)
    html = "".join(
        f'<section class="{"title" if x["level"] == 1 else "slide"}" style="{"background:linear-gradient(135deg,#0b1030 0%,#2a3fae 60%,#2340c4 100%)" if x["level"] == 1 else ""}'
        f';padding:clamp(12px,3vw,40px) clamp(12px,4vw,56px)"><h1 style="font:800 clamp(22px,4vw,44px) sans-serif">{x["title"]}</h1>'
        + "".join(f"<p>{b}</p>" for b in x["body"]) + "</section>" for x in s)
    (work / "deck.html").write_text(html, encoding="utf-8")
    return [("4 slides from 1 title + 3 headings", len(s) == 4, [x["title"] for x in s]),
            ("first is the title slide with the 135deg gradient", html.startswith('<section class="title"') and "135deg,#0b1030 0%,#2a3fae 60%,#2340c4 100%" in html, "title"),
            ("body lines stay under their heading", s[1]["body"] == ["ارتفعت ١٢٪"], s[1]["body"])]


# ---------------------------------------------------------------- FMT-55
AD = {6: [(0, 2, "hook"), (2, 5, "message"), (5, 6, "end")], 15: [(0, 1.5, "hook"), (1.5, 5, "message"), (5, 12, "features"), (12, 15, "end")]}
CODE = {"hook": 60, "message": 120, "features": 180, "end": 240}


def ad_frame(slots, t):
    lab = next(l for a, b, l in slots if a <= t < b or (t == slots[-1][1] and l == slots[-1][2]))
    return np.full((9, 16), CODE[lab], np.uint8)


def cut_ok(cuts, lo=1.0, hi=2.0):
    gaps = np.diff(cuts)
    return bool(np.all((gaps >= lo - 1e-9) & (gaps <= hi + 1e-9)))


def fmt_55(work):
    stills = {t: ad_frame(AD[15], t) for t in (1.0, 2.0, 4.99, 5.0, 14.9)}
    for t, a in stills.items():
        Image.fromarray(a).save(work / f"still_{t}.png")
    inv = {v: k for k, v in CODE.items()}
    seen = {t: inv[int(a[0, 0])] for t, a in stills.items()}
    return [("hook visible at 1 s, message at the 2 s marker", seen[1.0] == "hook" and seen[2.0] == "message", seen),
            ("key message lands before 5 s (pre-roll rule)", seen[4.99] == "message", seen[4.99]),
            ("end card on the final still", seen[14.9] == "end", seen[14.9]),
            ("cuts every 1-2 s accepted, a 3 s gap rejected", cut_ok([0, 1.5, 3, 4.2]) and not cut_ok([0, 1.5, 4.5]), "cuts")]


# ---------------------------------------------------------------- FMT-56
def cutdown(beats, target, grid=0.5):
    keep = list(beats)
    while sum(b["dur"] for b in keep) > target:
        opt = [b for b in keep if b["priority"] > 1]
        if not opt:
            raise ValueError("cannot reach target without dropping must-keep beats")
        keep.remove(max(opt, key=lambda b: (b["priority"], b["dur"])))
    extra = target - sum(b["dur"] for b in keep)
    keep[-1] = dict(keep[-1], dur=keep[-1]["dur"] + extra)
    t, out = 0.0, []
    for b in keep:
        out.append(dict(b, start=round(round(t / grid) * grid, 3)))
        t += b["dur"]
    return out


def fmt_56(work):
    beats = [{"id": "hook", "dur": 3, "priority": 1}, {"id": "problem", "dur": 9, "priority": 2}, {"id": "demo", "dur": 15, "priority": 2},
             {"id": "proof", "dur": 12, "priority": 3}, {"id": "detail", "dur": 12, "priority": 3}, {"id": "offer", "dur": 5, "priority": 2},
             {"id": "cta", "dur": 4, "priority": 1}]
    res = {n: cutdown(beats, n) for n in (60, 30, 15)}
    save_json(work, "cutdowns.json", res)
    ids = {n: [b["id"] for b in r] for n, r in res.items()}
    try:
        cutdown(beats, 5)
        rej = False
    except ValueError:
        rej = True
    return [("each version totals exactly its length", all(abs(sum(b["dur"] for b in r) - n) < 1e-9 for n, r in res.items()), {n: sum(b["dur"] for b in r) for n, r in res.items()}),
            ("hook first and CTA last in every version", all(i[0] == "hook" and i[-1] == "cta" for i in ids.values()), ids),
            ("15 s drops optional beats", "detail" not in ids[15] and "proof" not in ids[15], ids[15]),
            ("starts snap to the 0.5 s audio grid", all((b["start"] * 2) % 1 == 0 for r in res.values() for b in r), "grid"),
            ("impossible 5 s cut refused", rej, rej)]


# ---------------------------------------------------------------- FMT-57
def atomise(md):
    chapters = re.findall(r"^## (.+)$", md, re.M)
    prose = "\n".join(l for l in md.splitlines() if not re.match(r"^(#|\d+\. )", l))
    stats = re.findall(r"[^.\n]*\d+%[^.\n]*", prose)
    steps = re.findall(r"^\d+\. (.+)$", md, re.M)
    concl = re.search(r"^## (?:Conclusion|الخلاصة)\n(.+)", md, re.M)
    return {"chapters": chapters, "pull_quotes": [s.strip() for s in stats], "segments": steps, "short": concl.group(1) if concl else None}


def standalone(script):
    return not re.search(r"as (discussed|mentioned) (above|earlier|before)|كما ذكرنا", script, re.I)


def words_fit(script, lo=20, hi=45, wps=3.3):
    n = len(script.split())
    return 80 <= n <= 150 and lo <= n / wps <= hi


def fmt_57(work):
    md = "# Pricing guide\n## Why price matters\nRaising prices 10% lifted profit 33% in our test.\n## How to test\n1. Pick one product\n2. Raise 10%\n3. Watch churn\n## Conclusion\nTest one price this week."
    a = atomise(md)
    save_json(work, "atoms.json", a)
    good = " ".join(["word"] * 100)
    return [("H2s become chapters", a["chapters"] == ["Why price matters", "How to test", "Conclusion"], a["chapters"]),
            ("stat sentence becomes a pull quote", a["pull_quotes"] == ["Raising prices 10% lifted profit 33% in our test"], a["pull_quotes"]),
            ("3 steps become tutorial segments", len(a["segments"]) == 3, a["segments"]),
            ("conclusion becomes the short", a["short"] == "Test one price this week.", a["short"]),
            ("'as discussed above' fails the standalone test", not standalone("As discussed above, raise prices") and standalone("Raise one price"), "standalone"),
            ("100 words = 30 s fits; 40 words does not", words_fit(good) and not words_fit(" ".join(["w"] * 40)), "words")]


# ---------------------------------------------------------------- FMT-58
TRAILER = {"x": (30, 45), "youtube": (30, 90), "shorts": (15, 45), "store": (60, 120)}


def fmt_58(work):
    gif = work / "loop.gif"
    ff("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=20:duration=4", "-vf", "split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse", gif)
    g = Image.open(gif)
    secs = sum(g.seek(i) or g.info["duration"] for i in range(g.n_frames)) / 1000
    mb = gif.stat().st_size / 1e6
    ok = {p: lo <= 40 <= hi for p, (lo, hi) in TRAILER.items()}
    return [("GIF 640 px wide", g.size[0] == 640, g.size),
            ("GIF loop 4-8 s at 20 fps (80 frames, 4.0 s)", g.n_frames == 80 and abs(secs - 4.0) < 0.05, (g.n_frames, secs)),
            ("GIF under 15 MB", mb < 15, round(mb, 2)),
            ("40 s cut fits X/YouTube/Shorts, not store pages", ok == {"x": True, "youtube": True, "shorts": True, "store": False}, ok)]


# ---------------------------------------------------------------- FMT-59
def chapter_list(markers):
    def ts(s): return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60:02d}:{s % 60:02d}"
    errs = []
    if len(markers) < 3:
        errs.append("fewer than 3")
    if markers[0][0] != 0:
        errs.append("first not 00:00")
    if any(b[0] - a[0] < 10 for a, b in zip(markers, markers[1:])):
        errs.append("closer than 10 s")
    return "\n".join(f"{ts(t)} {n}" for t, n in markers), errs


def fmt_59(work):
    marks = [(0, "المقدمة"), (12, "الفكرة"), (25, "الخلاصة")]
    text, errs = chapter_list(marks)
    _, bad = chapter_list([(3, "a"), (8, "b")])
    _, longf = chapter_list([(0, "a"), (3725, "b"), (3800, "c")])
    meta = ";FFMETADATA1\n" + "".join(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={t * 1000}\nEND={(marks[i + 1][0] if i + 1 < len(marks) else 30) * 1000}\ntitle={n}\n"
                                      for i, (t, n) in enumerate(marks))
    (work / "ch.txt").write_text(meta, encoding="utf-8")
    src = work / "src.mp4"
    ff("-f", "lavfi", "-i", "color=c=gray:size=32x18:rate=5:duration=30", "-c:v", "libx264", "-preset", "ultrafast", src)
    out = work / "chaptered.mp4"
    ff("-i", src, "-i", work / "ch.txt", "-map_metadata", 1, "-map_chapters", 1, "-c", "copy", out)
    chs = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_chapters", "-print_format", "json", str(out)], capture_output=True, text=True).stdout)["chapters"]
    (work / "description.txt").write_text(text, encoding="utf-8")
    return [("description list starts '00:00 المقدمة'", text.splitlines()[0] == "00:00 المقدمة" and errs == [], text.splitlines()),
            ("bad list: first not 00:00, too few, too close", sorted(bad) == ["closer than 10 s", "fewer than 3", "first not 00:00"], bad),
            ("past 60 min uses h:mm:ss", "1:02:05 b" in chapter_list([(0, "a"), (3725, "b"), (3800, "c")])[0], "1:02:05"),
            ("Arabic chapter titles read back by ffprobe", [c["tags"]["title"] for c in chs] == ["المقدمة", "الفكرة", "الخلاصة"], [c["tags"]["title"] for c in chs]),
            ("chapter 2 starts at 12 s", float(chs[1]["start_time"]) == 12.0, chs[1]["start_time"])]


# ---------------------------------------------------------------- FMT-60
def carousel_check(slides):
    errs = []
    for i, s in enumerate(slides):
        if len(s["title"].split()) > 8:
            errs.append(f"{i}: title words")
        if len(s.get("body", "").split()) > 30:
            errs.append(f"{i}: body words")
    if slides[0]["variant"] != "cover" or slides[-1]["variant"] != "closing":
        errs.append("cover/closing")
    return errs


def render_slide(i, n, s, W=1080, H=1350, edge=80):
    im = Image.new("RGB", (W, H), (245, 240, 230))
    d = ImageDraw.Draw(im)
    d.text((W - edge, edge + 40), s["title"], font=font(56, True), fill=(20, 20, 20), anchor="ra", **rtl_kw())
    bar = (W - 2 * edge) * (i + 1) / n
    d.rectangle([W - edge - bar, H - edge + 30, W - edge, H - edge + 40], fill=(217, 83, 14))
    return im


def fmt_60(work):
    slides = [{"variant": "cover", "title": "٥ أخطاء في التسعير"}, {"variant": "content", "title": "لا تبدأ بالأرخص", "body": "السعر رسالة"},
              {"variant": "data", "title": "٧٠٪ يقارنون", "body": "قبل الشراء"}, {"variant": "contrast", "title": "قبل وبعد"},
              {"variant": "closing", "title": "احفظ المنشور"}]
    errs = carousel_check(slides)
    bars = []
    for i, s in enumerate(slides):
        im = render_slide(i, len(slides), s)
        im.resize((216, 270)).save(work / f"slide_{i + 1}.png")
        a = np.asarray(im)
        row = a[1350 - 80 + 35]
        bars.append(int((np.abs(row.astype(int) - (217, 83, 14)).sum(axis=1) < 10).sum()))
    bad = carousel_check([{"variant": "content", "title": "one two three four five six seven eight nine"}] + slides)
    return [("valid 5-slide carousel", errs == [], errs),
            ("progress bar grows each slide, full on the last", bars == sorted(bars) and bars[-1] == 1080 - 160 + 1, bars),
            ("9-word title and non-cover first slide rejected", "0: title words" in bad and "cover/closing" in bad, bad),
            ("1080x1350 slide with 80 px edge", render_slide(0, 5, slides[0]).size == (1080, 1350), "size")]


# ---------------------------------------------------------------- FMT-61
MG = {"MG-061": [(0, 0.9, "card1"), (0.9, 1.8, "card2"), (1.8, 2.7, "card3"), (2.7, 4, "topic")],
      "MG-062": [(0, 1.5, "question"), (1.5, 2.5, "split"), (2.5, 5, "answer")],
      "MG-063": [(0, 4, "tip1"), (4, 8, "tip2"), (8, 12, "tip3")],
      "MG-066": [(0, 2, "result"), (2, 3, "shrink"), (3, 8, "steps"), (8, 10, "back")]}


def phase(mg, t):
    for a, b, n in MG[mg]:
        if a <= t < b:
            return n
    return "end"


def word_mask_times(words, start, per=0.25):
    return [round(start + i * per, 3) for i in range(len(words))]


def fmt_61(work):
    durs = {k: v[-1][1] for k, v in MG.items()}
    contiguous = all(all(a[1] == b[0] for a, b in zip(v, v[1:])) and v[0][0] == 0 for v in MG.values())
    times = word_mask_times("أسرار التسويق بالمحتوى".split(), 2.7)
    save_json(work, "openers.json", {"durations": durs, "mask_times": times})
    prog = [round(t / 12, 3) for t in (0, 6, 12)]
    return [("durations MG-061 4 / 062 5 / 063 12 / 066 10 s", durs == {"MG-061": 4, "MG-062": 5, "MG-063": 12, "MG-066": 10}, durs),
            ("phases are contiguous from 0", contiguous, contiguous),
            ("MG-062 at 2.0 s is the split, 3 s the answer", (phase("MG-062", 2.0), phase("MG-062", 3)) == ("split", "answer"), "phases"),
            ("topic masks per whole word from 2.7 s", times == [2.7, 2.95, 3.2], times),
            ("MG-063 real progress bar 0 / 50% / 100%", prog == [0, 0.5, 1], prog)]


# ---------------------------------------------------------------- FMT-62
def loop_frame(i, N=30, W=32, H=18):
    t = i / N
    a = np.zeros((H, W), np.uint8)
    x = int(round((W - 4) * (0.5 + 0.5 * math.sin(2 * math.pi * t))))
    a[6:12, x:x + 4] = 255
    return a


def fmt_62(work):
    N = 30
    raw = work / "f.gray"
    raw.write_bytes(b"".join(loop_frame(i).tobytes() for i in range(N)))
    clip = work / "loop.mp4"
    ff("-f", "rawvideo", "-pix_fmt", "gray", "-s", "32x18", "-r", 30, "-i", raw, "-c:v", "libx264", "-preset", "ultrafast", "-crf", 0, "-pix_fmt", "yuv444p", clip)
    raw.unlink()
    twice = work / "twice.mp4"
    ff("-stream_loop", 1, "-i", clip, "-c:v", "libx264", "-preset", "ultrafast", "-crf", 0, "-pix_fmt", "yuv444p", twice)
    fr = frames_of(twice, 32, 18, fmt="gray", ch=1).astype(int)
    diffs = [np.abs(fr[i + 1] - fr[i]).mean() for i in range(len(fr) - 1)]
    seam = diffs[N - 1]
    pal = work / "pal.png"
    ff("-i", clip, "-vf", "palettegen=stats_mode=diff:max_colors=192", pal)
    ff("-i", clip, "-i", pal, "-lavfi", "paletteuse=dither=sierra2_4a:diff_mode=rectangle", work / "loop.gif")
    return [("60 frames after one -stream_loop", len(fr) == 60, len(fr)),
            ("t=D equals t=0 (frame N not exported)", np.array_equal(loop_frame(N), loop_frame(0)), "equal"),
            ("seam step no larger than the largest in-loop step", seam <= max(diffs[:N - 1]) + 1e-9, (round(seam, 2), round(max(diffs[:N - 1]), 2))),
            ("no duplicate frame at the seam (motion continues)", seam > 0, round(seam, 2)),
            ("GIF written with diff palette", (work / "loop.gif").stat().st_size > 0, "gif")]


# ---------------------------------------------------------------- FMT-63
def end_card_frame(t, D=6.0, W=108, H=192):
    top, bot = np.array((0x1b, 0x2a, 0x49)), np.array((0x0d, 0x1b, 0x2a))
    a = (top + (bot - top) * np.linspace(0, 1, H)[:, None]).round().astype(np.uint8)
    a = np.repeat(a[:, None, :], W, axis=1)
    p = clamp01(t / (D - 0.4))
    a[H - 6:H - 3, 8:8 + int(round((W - 16) * p))] = (0xE7, 0xB6, 0x5A)
    return a


def fmt_63(work):
    f0, fm, fe = end_card_frame(0), end_card_frame(2.8), end_card_frame(5.6)
    Image.fromarray(fe).save(work / "endcard_end.png")
    def bar(a): return int((np.abs(a[188].astype(int) - (0xE7, 0xB6, 0x5A)).sum(axis=1) == 0).sum())
    return [("background top #1b2a49, bottom #0d1b2a", tuple(f0[0, 0]) == (0x1b, 0x2a, 0x49) and tuple(f0[-1, 0]) == (0x0d, 0x1b, 0x2a), (tuple(f0[0, 0]), tuple(f0[-1, 0]))),
            ("bar empty at 0 s", bar(f0) == 0, bar(f0)),
            ("bar half at 2.8 s (linear over D-0.4 = 5.6 s)", bar(fm) == 46, bar(fm)),
            ("bar full at 5.6 s, accent #E7B65A", bar(fe) == 92, bar(fe))]


# ---------------------------------------------------------------- FMT-64
def store_card(t, D=4.0, W=270, H=480):
    im = Image.new("RGB", (W, H), (0xec, 0xef, 0xfa))
    d = ImageDraw.Draw(im)
    a = clamp01(t / 0.3)
    col = tuple(int(round(c + (20 - c) * a)) for c in (0xec, 0xef, 0xfa))
    d.rounded_rectangle([60, 380, 210, 428], radius=24 // 4, fill=col)  # pill r 24 px at quarter scale
    feats = ["سريع", "آمن", "عربي"]
    x = 230
    for i, f in enumerate(feats):
        d.text((x, 300), f, font=font(18, True), fill=(30, 30, 30), anchor="rm", **rtl_kw())
        x -= 70
        if i < len(feats) - 1:
            d.ellipse([x + 26, 297, x + 32, 303], fill=(220, 30, 30))
    return im


def fmt_64(work):
    im = store_card(0.3)
    im.save(work / "store_card.png")
    a = np.asarray(im).astype(int)
    early = np.asarray(store_card(0.0)).astype(int)
    red = np.all(np.abs(a - (220, 30, 30)) < 20, axis=2)
    import cv2
    n_dots = cv2.connectedComponents(red.astype(np.uint8))[0] - 1
    hold = [store_card(t).tobytes() == store_card(4.0).tobytes() for t in (3.5, 3.8)]
    return [("pill fully visible by 300 ms", tuple(a[404, 135]) == (20, 20, 20), tuple(a[404, 135])),
            ("pill invisible at 0 ms", tuple(early[404, 135]) == (0xec, 0xef, 0xfa), tuple(early[404, 135])),
            ("features separated by 2 red dots", n_dots == 2, n_dots),
            ("last 500 ms is a frozen hold", all(hold), hold)]


# ---------------------------------------------------------------- FMT-66
def counter_at(t, events):
    return sum(1 for e in events if e <= t)


def hook_frame(t, events, W=270, H=480):
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    d.rectangle([20, int(0.12 * H), W - 20, int(0.20 * H)], fill=200)
    d.text((W // 2, H // 2), f"{counter_at(t, events):03d}", font=font(40), fill=255, anchor="mm")
    if t < 3:
        d.rectangle([90, 420, 180, 440], fill=120)
    return im


def fmt_66(work):
    events = [0.5, 1.0, 1.7, 2.2, 4.0]
    f = np.asarray(hook_frame(2.0, events))
    Image.fromarray(f).save(work / "hook_2s.png")
    rows = np.nonzero((f == 200).any(axis=1))[0]
    fnt = font(40)
    adv = {fnt.getlength(c) for c in "0123456789"}
    pill_on = np.asarray(hook_frame(2.9, events))[430, 135]
    pill_off = np.asarray(hook_frame(3.0, events))[430, 135]
    return [("question band within the top 12-20%", rows.min() >= 0.12 * 480 - 1 and rows.max() <= 0.20 * 480, (int(rows.min()), int(rows.max()))),
            ("counter = events so far (3 at 2.0 s, 5 at 4.0 s)", counter_at(2.0, events) == 3 and counter_at(4.0, events) == 5, counter_at(2.0, events)),
            ("tabular digits: one advance width", len(adv) == 1, sorted(adv)),
            ("'sound on' pill gone at 3 s", pill_on == 120 and pill_off == 0, (int(pill_on), int(pill_off)))]


# ---------------------------------------------------------------- FMT-67
def promo_layout(W=1080, H=1080, margin=80, arabic=True, product_h=0.45):
    text = (W - margin - 400, margin, W - margin, margin + 200) if arabic else (margin, margin, margin + 400, margin + 200)
    ph = product_h * H
    product = (W / 2 - ph / 2, H - margin - ph, W / 2 + ph / 2, H - margin)
    return {"text": text, "product": product, "ok": product_h >= 0.4 and text[1] >= margin and product[3] <= H - margin}


def spring_settle(k=180, c=14, m=1.0, fps=60):
    x, v, out = 0.0, 0.0, []
    for _ in range(fps * 2):
        for _ in range(20):
            a = (-k * (x - 1) - c * v) / m
            v += a / fps / 20
            x += v / fps / 20
        out.append(x)
    return np.array(out)


def fmt_67(work):
    L = promo_layout()
    im = Image.new("RGB", (1080, 1080), "white")
    d = ImageDraw.Draw(im)
    d.rectangle(L["text"], fill=(20, 20, 20))
    d.rectangle(L["product"], fill=(200, 40, 40))
    im.resize((270, 270)).save(work / "promo.png")
    s = spring_settle()
    z = 14 / (2 * math.sqrt(180))
    over = math.exp(-z * math.pi / math.sqrt(1 - z * z))
    bad = promo_layout(product_h=0.3)
    return [("Arabic text block top-right inside 80 px", L["text"][2] == 1000 and L["text"][1] == 80, L["text"]),
            ("product >= 40% of frame height", (L["product"][3] - L["product"][1]) / 1080 >= 0.4, (L["product"][3] - L["product"][1]) / 1080),
            ("30% product refused", not bad["ok"], bad["ok"]),
            ("price-card spring 14/180 overshoot matches analytic", abs((s.max() - 1) - over) < 0.004, (round(s.max() - 1, 4), round(over, 4)))]


# ---------------------------------------------------------------- FMT-X01
def fmt_x01(work):
    tone = work / "music.wav"
    ff("-f", "lavfi", "-i", "sine=f=220:d=3:sample_rate=48000", tone)
    i, tp = normalise(tone, work / "music_n.wav")
    master = work / "master.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=size=64x36:rate=24:duration=1", "-i", work / "music_n.wav", "-c:v", "libx264", "-profile:v", "high", "-preset", "veryfast",
       "-b:v", "20M", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
       "-c:a", "aac", "-b:a", "256k", "-shortest", master)
    nos = work / "master_nosound.mp4"
    ff("-i", master, "-c:v", "copy", "-an", nos)
    v = vstream(master)
    kinds = [s["codec_type"] for s in probe(nos)["streams"]]
    bed_i, _ = normalise(tone, work / "bed.wav", target=-21.0)
    voice_db, music_db = i, bed_i
    return [("master H.264 High BT.709 24 fps", (v["profile"], v.get("color_primaries"), v["r_frame_rate"]) == ("High", "bt709", "24/1"),
             (v["profile"], v.get("color_primaries"), v["r_frame_rate"])),
            ("_nosound copy has video only", kinds == ["video"], kinds),
            ("mix normalised to -14 LUFS +-1", abs(i + 14) <= 1, i),
            ("true peak <= -1.2 dBTP", tp <= -1.2, tp),
            ("payoff line measured >= 6 LU above a -21 LUFS bed", voice_db - music_db >= 6, round(voice_db - music_db, 2))]


PROGRAMS = {"FMT-03": fmt_03, "FMT-04": fmt_04, "FMT-05": fmt_05, "FMT-06": fmt_06, "FMT-09": fmt_09, "FMT-10": fmt_10, "FMT-12": fmt_12,
            "FMT-13": fmt_13, "FMT-14": fmt_14, "FMT-15": fmt_15, "FMT-17": fmt_17, "FMT-18": fmt_18, "FMT-20": fmt_20, "FMT-21": fmt_21,
            "FMT-22": fmt_22, "FMT-23": fmt_23, "FMT-24": fmt_24, "FMT-27": fmt_27, "FMT-28": fmt_28, "FMT-29": fmt_29, "FMT-30": fmt_30,
            "FMT-31": fmt_31, "FMT-32": fmt_32, "FMT-34": fmt_34, "FMT-35": fmt_35, "FMT-36": fmt_36, "FMT-37": fmt_37, "FMT-43": fmt_43,
            "FMT-44": fmt_44, "FMT-45": fmt_45, "FMT-46": fmt_46, "FMT-47": fmt_47, "FMT-48": fmt_48, "FMT-49": fmt_49, "FMT-50": fmt_50,
            "FMT-51": fmt_51, "FMT-52": fmt_52, "FMT-53": fmt_53, "FMT-54": fmt_54, "FMT-55": fmt_55, "FMT-56": fmt_56, "FMT-57": fmt_57,
            "FMT-58": fmt_58, "FMT-59": fmt_59, "FMT-60": fmt_60, "FMT-61": fmt_61, "FMT-62": fmt_62, "FMT-63": fmt_63, "FMT-64": fmt_64,
            "FMT-66": fmt_66, "FMT-67": fmt_67, "FMT-X01": fmt_x01}
