#!/usr/bin/env python3
"""general-media proof: render Arabic+English text with Pillow, OCR it with tesseract (ara+eng),
deskew/binarise/compress/compare images with OpenCV + Pillow + scikit-image, round-trip a QR code,
and analyse/normalise/cut audio with librosa, pyloudnorm, ffmpeg and pydub.

Usage:  python -I make_media.py <workdir>
Needs:  pillow opencv-python-headless scikit-image pytesseract qrcode numpy soundfile librosa
        pyloudnorm pydub audioop-lts(py>=3.13) arabic-reshaper python-bidi
        + apt: tesseract-ocr tesseract-ocr-ara ; ffmpeg/ffprobe on PATH. Fonts: ../_shared/fonts (OFL).
Writes: <workdir>/... ; contact.png + results.json next to this script.
"""
from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, features

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "_shared" / "fonts"
W = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/general-media").resolve()
W.mkdir(parents=True, exist_ok=True)
R: dict = {"workdir": "<workdir>/" + W.name, "checks": [], "numbers": {}, "timings_s": {}}


def check(name, ok, detail=""):
    R["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + (f" | {detail}" if detail else ""))


def sh(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=300)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\u064B-\u0652\u0640]", "", s)  # drop tashkeel + tatweel
    return re.sub(r"\s+", " ", s).strip()


def sim(a: str, b: str) -> float:
    return round(difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(), 3)


# ------------------------------------------------------------ 1. render Arabic + English (Pillow + raqm)
LINES = [("الذكاء الاصطناعي يقرأ النص العربي", "Amiri-Regular.ttf", "rtl"),
         ("سعر القهوة 15 ريالا في عام 2026", "Tajawal-Bold.ttf", "rtl"),
         ("Invoice 2026-10 total: 1,250.75 SAR", "Cairo[slnt,wght].ttf", "ltr")]
R["findings"] = []  # measured behaviour worth knowing; not pass/fail
check("Pillow wheel has raqm (HarfBuzz+FriBiDi) layout", features.check("raqm"), f"raqm {features.version('raqm')}")
img = Image.new("RGB", (1500, 470), "white")
dr = ImageDraw.Draw(img)
for i, (txt, font, direction) in enumerate(LINES):
    f = ImageFont.truetype(str(FONTS / font), 64, layout_engine=ImageFont.Layout.RAQM)
    x = 1450 if direction == "rtl" else 50
    # raw logical-order string; raqm shapes and reorders it. anchor "ra" = right edge for RTL
    dr.text((x, 40 + i * 140), txt, font=f, fill="black", direction=direction, language="ar" if direction == "rtl" else "en",
            anchor="ra" if direction == "rtl" else "la")
SRC = W / "ocr_source.png"
img.save(SRC)

# the classic recipe (reshaper + bidi) applied on top of raqm double-processes the text
import arabic_reshaper
from bidi.algorithm import get_display

strip = Image.new("RGB", (1500, 200), "white")
sd = ImageDraw.Draw(strip)
f = ImageFont.truetype(str(FONTS / "Amiri-Regular.ttf"), 54)
sd.text((1450, 10), LINES[0][0], font=f, fill="black", direction="rtl", anchor="ra")
sd.text((1450, 105), get_display(arabic_reshaper.reshape(LINES[0][0])), font=f, fill="#b00020", direction="rtl", anchor="ra")
strip.save(W / "raqm_vs_reshaper.png")

# ------------------------------------------------------------ 2. OCR with tesseract ara+eng
import pytesseract

t0 = time.time()
ocr = pytesseract.image_to_string(Image.open(SRC), lang="ara+eng", config="--oem 1 --psm 6")
R["timings_s"]["ocr"] = round(time.time() - t0, 2)
got = [l for l in ocr.splitlines() if l.strip()]
per_line = [sim(gt, got[i] if i < len(got) else "") for i, (gt, _, _) in enumerate(LINES)]
whole = sim(" ".join(t for t, _, _ in LINES), " ".join(got))
R["numbers"]["ocr_lines"] = got
R["numbers"]["ocr_similarity_per_line"] = per_line
check("tesseract ara+eng OCR of rendered Arabic+English (naskh/clean fonts, Western digits)", whole >= 0.95, f"similarity {whole} (per line {per_line}) in {R['timings_s']['ocr']} s; tesseract {pytesseract.get_tesseract_version()}")
data = pytesseract.image_to_data(Image.open(SRC), lang="ara+eng", config="--oem 1 --psm 6", output_type=pytesseract.Output.DICT)
confs = [float(c) for c in data["conf"] if float(c) >= 0]
R["numbers"]["ocr_mean_word_conf"] = round(sum(confs) / len(confs), 1)



def ocr_line(txt, font, size=56, lang="ara"):
    im = Image.new("L", (1400, 160), 255)
    ImageDraw.Draw(im).text((1370, 30), txt, font=ImageFont.truetype(str(FONTS / font), size), fill=0, direction="rtl", anchor="ra")
    out_ = pytesseract.image_to_string(im, lang=lang, config="--oem 1 --psm 7")
    return sim(txt, out_), norm(out_)


for txt, font, lang in [("سعر القهوة ١٥ ريالا في عام ٢٠٢٦", "Amiri-Regular.ttf", "ara"), ("سعر القهوة 15 ريالا في عام 2026", "Amiri-Regular.ttf", "ara"),
                        ("رقم الهاتف ٠١٢٣٤٥٦٧٨٩", "Tajawal-Bold.ttf", "ara"), ("سعر القهوة 15 ريالا في عام 2026", "Cairo[slnt,wght].ttf", "ara+eng"),
                        ("سعر القهوة 15 ريالا في عام 2026", "ReemKufi[wght].ttf", "ara")]:
    s_, got_ = ocr_line(txt, font, lang=lang)
    R["findings"].append({"what": f"OCR {lang} psm7, {font.split('[')[0].split('.')[0]} 56px", "text": txt, "similarity": s_, "ocr": got_})
    print(f"FINDING {s_:.3f} {font[:12]:12} {lang:7} {txt} -> {got_}")

# ------------------------------------------------------------ 3. deskew: rotate 4 deg, OCR, detect angle, fix, OCR again
SKEW = 12.0
gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
pad = cv2.copyMakeBorder(gray, 200, 200, 100, 100, cv2.BORDER_CONSTANT, value=255)  # room to rotate without cropping
h, w_ = pad.shape
M = cv2.getRotationMatrix2D((w_ / 2, h / 2), SKEW, 1.0)
rot = cv2.warpAffine(pad, M, (w_, h), flags=cv2.INTER_CUBIC, borderValue=255)
noisy = np.clip(rot.astype(np.int16) + np.random.default_rng(3).normal(0, 18, rot.shape), 0, 255).astype(np.uint8)
cv2.imwrite(str(W / "skewed_noisy.png"), noisy)
ocr_skew = pytesseract.image_to_string(Image.fromarray(noisy), lang="ara+eng", config="--oem 1 --psm 6")
# angle estimate: fit a min-area rectangle around the ink (Otsu threshold of the denoised image)
den = cv2.medianBlur(noisy, 3)
_, ink = cv2.threshold(den, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
ink = cv2.morphologyEx(ink, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
lines_mask = cv2.dilate(ink, cv2.getStructuringElement(cv2.MORPH_RECT, (60, 5)))  # merge words into line blobs
cnts, _ = cv2.findContours(lines_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
angles = []
for c in cnts:
    if cv2.contourArea(c) < 5000:
        continue
    (cx, cy), (rw, rh), ang = cv2.minAreaRect(c)
    if rw < rh:
        ang -= 90
    angles.append(ang)
est = float(np.median(angles)) if angles else 0.0
fixed = cv2.warpAffine(den, cv2.getRotationMatrix2D((w_ / 2, h / 2), est, 1.0), (w_, h), flags=cv2.INTER_CUBIC, borderValue=255)
cv2.imwrite(str(W / "deskewed.png"), fixed)
ocr_fixed = pytesseract.image_to_string(Image.fromarray(fixed), lang="ara+eng", config="--oem 1 --psm 6")
binar = cv2.adaptiveThreshold(fixed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15)
ocr_bin = pytesseract.image_to_string(Image.fromarray(binar), lang="ara+eng", config="--oem 1 --psm 6")
gt_all = " ".join(t for t, _, _ in LINES)
s_skew, s_fixed, s_bin = sim(gt_all, ocr_skew), sim(gt_all, ocr_fixed), sim(gt_all, ocr_bin)
R["numbers"].update(skew_true_deg=SKEW, skew_estimated_deg=round(est, 2), ocr_sim_skewed=s_skew, ocr_sim_deskewed=s_fixed)
R["findings"].append({"what": "adaptive threshold (31, C=15) after deskew on gaussian-noise scan", "similarity": s_bin,
                      "note": "binarising blindly can HURT tesseract 5 (LSTM works on grayscale); measure before adding preprocessing"})
check("OpenCV deskew: minAreaRect angle within 0.5 deg of truth", abs(abs(est) - SKEW) < 0.5, f"estimated {est:.2f} deg (true {SKEW:.2f})")
check("deskew (median 3 + rotate back) recovers OCR on a 12 deg noisy scan", s_fixed >= 0.85 and s_fixed > s_skew + 0.15, f"similarity skewed+noisy {s_skew} -> deskewed {s_fixed} (binarised: {s_bin})")

# ------------------------------------------------------------ 4. edges, compression, quality metrics
edges = cv2.Canny(gray, 80, 160)
cv2.imwrite(str(W / "edges.png"), edges)
photo = np.zeros((480, 640, 3), np.uint8)  # synthetic "photo": gradient + discs, so codecs have work to do
yy, xx = np.mgrid[0:480, 0:640]
photo[..., 0] = (xx / 640 * 255).astype(np.uint8)
photo[..., 1] = (yy / 480 * 255).astype(np.uint8)
photo[..., 2] = 128
for cx_, cy_, r_, col in [(200, 240, 90, (230, 80, 40)), (440, 200, 70, (30, 170, 120)), (330, 360, 60, (240, 190, 0))]:
    cv2.circle(photo, (cx_, cy_), r_, col, -1, lineType=cv2.LINE_AA)
pim = Image.fromarray(photo)
sizes = {}
for fmt, kw in [("png", {"optimize": True}), ("webp", {"quality": 80}), ("avif", {"quality": 50}), ("jpeg", {"quality": 85})]:
    p_ = W / f"photo.{fmt}"
    pim.save(p_, **kw)
    sizes[fmt] = p_.stat().st_size
from skimage.metrics import structural_similarity as ssim

back = np.array(Image.open(W / "photo.webp").convert("RGB"))
psnr = cv2.PSNR(photo, back)
ss = ssim(photo, back, channel_axis=2)
R["numbers"].update(sizes_B=sizes, webp_psnr_db=round(psnr, 2), webp_ssim=round(float(ss), 4))
check("Pillow encodes PNG/WebP/AVIF/JPEG; WebP q80 keeps SSIM >= 0.95", ss >= 0.95 and sizes["webp"] < sizes["png"], f"{sizes}; PSNR {psnr:.1f} dB, SSIM {ss:.4f}")
# dominant colours by k-means (k=4) should recover the three disc colours
flat = np.full((240, 320, 3), 235, np.uint8)  # flat light background + 3 discs + sensor noise
for cx_, cy_, r_, col in [(80, 120, 50, (230, 80, 40)), (180, 90, 40, (30, 170, 120)), (250, 170, 45, (240, 190, 0))]:
    cv2.circle(flat, (cx_, cy_), r_, col, -1)
flat = np.clip(flat.astype(np.int16) + np.random.default_rng(5).normal(0, 6, flat.shape), 0, 255).astype(np.uint8)
Z = flat.reshape(-1, 3).astype(np.float32)
_, labels, centers = cv2.kmeans(Z, 4, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5), 4, cv2.KMEANS_PP_CENTERS)
found = [min(np.linalg.norm(centers - np.array(c), axis=1)) for c in [(230, 80, 40), (30, 170, 120), (240, 190, 0)]]
check("OpenCV k-means (k=4) palette recovers the 3 disc colours (< 10 RGB units)", max(found) < 10, f"distances {[round(float(d), 1) for d in found]}")

# ImageMagick 6 CLI (`convert`; the v7 `magick` binary is absent here): resize + grayscale + unsharp
im6 = sh(["convert", str(W / "ocr_source.png"), "-resize", "50%", "-colorspace", "Gray", "-unsharp", "0x1", str(W / "im6_small.png")])
idf = sh(["identify", "-format", "%w %h %[colorspace]", str(W / "im6_small.png")]).stdout.strip()
check("ImageMagick convert: resize 50% + Gray + unsharp; identify confirms", im6.returncode == 0 and idf.startswith("750 235 Gray"), idf)

# ------------------------------------------------------------ 5. QR round trip (qrcode -> OpenCV decode)
import qrcode

payload = "https://example.com/menu?item=قهوة&lang=ar"
qrcode.make(payload, box_size=8, border=4).save(W / "qr.png")
dec, pts, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(str(W / "qr.png")))
check("QR: qrcode encodes UTF-8 Arabic URL, OpenCV decodes it back", dec == payload, dec)

# ------------------------------------------------------------ 6. audio: synthesise, analyse, normalise, cut
import librosa
import pyloudnorm as pyln
import soundfile as sf

SR = 48_000
t = np.arange(int(SR * 2.0)) / SR
tone = 0.2 * np.sin(2 * np.pi * 440 * t)                      # 0-2 s: 440 Hz
gap = np.zeros(int(SR * 1.0))                                  # 2-3 s: silence
clicks = np.zeros(int(SR * 3.0))                               # 3-6 s: clicks at 120 BPM
for k in range(6):
    s0 = int(k * 0.5 * SR)
    n = int(0.03 * SR)
    clicks[s0:s0 + n] += 0.25 * np.sin(2 * np.pi * 1000 * np.arange(n) / SR) * np.exp(-np.arange(n) / (0.006 * SR))
sig = np.concatenate([tone, gap, clicks]).astype(np.float32)
WAV = W / "test.wav"
sf.write(WAV, sig, SR, subtype="PCM_16")
y, sr = librosa.load(WAV, sr=None)
f0 = librosa.yin(y[: 2 * sr], fmin=100, fmax=1000, sr=sr)
pitch = float(np.median(f0))
onsets = librosa.onset.onset_detect(y=y[int(2.9 * sr):], sr=sr, units="time", backtrack=False)  # start 0.1 s early: an onset at sample 0 is never detected
ioi = float(np.median(np.diff(onsets))) if len(onsets) > 1 else 0
check("librosa YIN pitch of the 440 Hz segment", abs(pitch - 440) < 2, f"{pitch:.1f} Hz")
check("librosa onsets of 120 BPM clicks: median spacing 0.5 s", abs(ioi - 0.5) < 0.02 and len(onsets) == 6, f"{len(onsets)} onsets, median IOI {ioi:.3f} s -> {60 / ioi if ioi else 0:.1f} BPM")
meter = pyln.Meter(SR)
lufs_in = meter.integrated_loudness(sig.astype(np.float64))
# two-pass ffmpeg loudnorm to -14 LUFS / -1 dBTP (pass 1 measures, pass 2 applies linear gain)
p1 = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", str(WAV), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"])
m = json.loads(p1.stderr[p1.stderr.rindex("{"):p1.stderr.rindex("}") + 1])
NORM = W / "test_norm.wav"
# linear (pure gain) mode only happens when measured LRA <= target LRA and the true peak has headroom;
# otherwise ffmpeg silently switches to dynamic compression. Raise LRA above the measured value to stay linear.
lra = max(11.0, round(float(m["input_lra"]) + 1, 1))
R["numbers"]["loudnorm_pass1"] = {k: m[k] for k in ("input_i", "input_tp", "input_lra", "normalization_type")}
af = (f"loudnorm=I=-14:TP=-1:LRA={lra}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
p2 = sh(["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", str(WAV), "-af", af + ":print_format=json", "-ar", str(SR), str(NORM)])
mode = json.loads(p2.stderr[p2.stderr.rindex("{"):p2.stderr.rindex("}") + 1])["normalization_type"]  # 'linear' or silently 'dynamic'
R["numbers"]["loudnorm_pass2_mode"] = mode
yn, _ = sf.read(NORM)
lufs_out = meter.integrated_loudness(yn)
eb = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", str(NORM), "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
eb_i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1])
R["numbers"].update(pitch_hz=round(pitch, 1), onsets=len(onsets), lufs_in=round(lufs_in, 2), lufs_out_pyloudnorm=round(lufs_out, 2), lufs_out_ebur128=eb_i)
check("ffmpeg 2-pass loudnorm (linear) hits -14 LUFS; pyloudnorm and ebur128 agree within 0.5 LU", mode == "linear" and abs(lufs_out + 14) < 0.5 and abs(eb_i + 14) < 0.5,
      f"in {lufs_in:.2f} -> out {lufs_out:.2f} (pyloudnorm) / {eb_i} (ebur128), pass-2 mode {mode}")
sil = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", str(WAV), "-af", "silencedetect=noise=-50dB:d=0.5", "-f", "null", "-"]).stderr
s_start = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", sil)]
s_end = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", sil)]
check("ffmpeg silencedetect finds the 2.0-3.0 s gap", any(abs(a - 2.0) < 0.05 for a in s_start) and any(abs(b - 3.0) < 0.1 for b in s_end), f"starts {s_start}, ends {s_end}")
sh(["ffmpeg", "-hide_banner", "-y", "-i", str(WAV), "-filter_complex", "showwavespic=s=1200x200:colors=#2a78d6", "-frames:v", "1", str(W / "wave.png")])
sh(["ffmpeg", "-hide_banner", "-y", "-i", str(WAV), "-lavfi", "showspectrumpic=s=1200x300:legend=0", str(W / "spectrum.png")])
check("ffmpeg draws waveform + spectrogram PNGs", (W / "wave.png").exists() and (W / "spectrum.png").exists())
# pydub (needs audioop-lts on Python 3.13+): cut the tone, fade, export MP3; verify with ffprobe
from pydub import AudioSegment

seg = AudioSegment.from_wav(WAV)[:2000].fade_in(200).fade_out(400)
seg.export(W / "tone.mp3", format="mp3", bitrate="128k")
dur = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(W / "tone.mp3")]).stdout)
check("pydub slice + fades + MP3 export (ffprobe duration ~2.0 s)", abs(dur - 2.0) < 0.06, f"{dur:.3f} s")
sh(["ffmpeg", "-hide_banner", "-y", "-i", str(NORM), "-c:a", "aac", "-b:a", "96k", str(W / "test.m4a")])
dur_o = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(W / "test.m4a")]).stdout)
check("ffmpeg transcode to AAC 96k (.m4a) keeps duration", abs(dur_o - 6.0) < 0.05, f"{dur_o:.3f} s, {(W / 'test.m4a').stat().st_size} B")

# ------------------------------------------------------------ 7. contact sheet
lab_font = ImageFont.truetype(str(FONTS / "Cairo[slnt,wght].ttf"), 20)
panels = [("1 rendered with Pillow+raqm (OCR source)", W / "ocr_source.png"), ("2 rotated 12 deg + noise", W / "skewed_noisy.png"),
          ("3 deskewed (angle from minAreaRect)", W / "deskewed.png"), ("4 top: raqm raw (right) / bottom red: reshaper+bidi on raqm (reversed)", W / "raqm_vs_reshaper.png"),
          ("5 Canny edges", W / "edges.png"), ("6 waveform (ffmpeg showwavespic)", W / "wave.png"), ("7 spectrogram (ffmpeg showspectrumpic)", W / "spectrum.png")]
tiles = []
for label, p_ in panels:
    im = Image.open(p_).convert("RGB")
    im.thumbnail((900, 300))
    tile = Image.new("RGB", (920, im.height + 44), "white")
    tile.paste(im, (10, 38))
    ImageDraw.Draw(tile).text((10, 4), label, fill="#b00020", font=lab_font)
    tiles.append(tile)
qr = Image.open(W / "qr.png").convert("RGB")
qr.thumbnail((240, 240))
tile = Image.new("RGB", (920, 290), "white")
tile.paste(qr, (10, 40))
ImageDraw.Draw(tile).text((10, 4), "8 QR (decoded back by OpenCV)", fill="#b00020", font=lab_font)
ImageDraw.Draw(tile).text((270, 120), dec, fill="black", direction="ltr", font=ImageFont.truetype(str(FONTS / "Cairo[slnt,wght].ttf"), 22, layout_engine=ImageFont.Layout.RAQM))
tiles.append(tile)
col_h = [0, 0]
cols = [[], []]
for t_ in tiles:
    i = 0 if col_h[0] <= col_h[1] else 1
    cols[i].append(t_)
    col_h[i] += t_.height + 8
sheet = Image.new("RGB", (1860, max(col_h)), "#dddddd")
for ci, col in enumerate(cols):
    y_ = 0
    for t_ in col:
        sheet.paste(t_, (ci * 940, y_))
        y_ += t_.height + 8
sheet = sheet.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
sheet.save(HERE / "contact.png", optimize=True)
check("contact.png < 300 KB", (HERE / "contact.png").stat().st_size < 300_000, f"{(HERE / 'contact.png').stat().st_size} B")

from importlib.metadata import version as v
R["versions"] = {k: v(k) for k in ("pillow", "opencv-python-headless", "scikit-image", "pytesseract", "qrcode", "librosa", "soundfile", "pyloudnorm", "pydub", "numpy")}
R["versions"]["tesseract"] = str(pytesseract.get_tesseract_version())
R["versions"]["ffmpeg"] = sh(["ffmpeg", "-version"]).stdout.splitlines()[0]
R["summary"] = f"{sum(c['ok'] for c in R['checks'])}/{len(R['checks'])} checks passed"
print(R["summary"])
(HERE / "results.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
