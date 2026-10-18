#!/usr/bin/env python3
"""Build the KOSIF Jumuah font family — بناء خط «كوسيف جمعة».

A matched typeface for the Friday-greeting typography observed in the reference video:
Arabic Naskh with Amiri's stacked ligatures (جم, محمد, الله) and the ﷺ glyph, plus Didone
figures for dates. It is assembled from two SIL Open Font License families, renamed as the
OFL requires (neither Reserved Font Name is reused):

  * Amiri Regular / Bold (Khaled Hosny, OFL 1.1)          -> Arabic script, Arabic punctuation, tatweel, ﷺ
  * Bodoni Moda (Indestructible Type, OFL 1.1), instanced -> Latin letters, European digits, punctuation
    at wght 400 / opsz 11 (Regular) and wght 600 / opsz 11 (Bold)

  python3 fonts/kosif-jumuah/build_font.py [--src DIR] [--out DIR] [--no-download]

Sources are fetched from the google/fonts repository into --src (default .kosif-cache/fonts-src),
subset to disjoint Unicode ranges, scaled to a common 1000 UPM, merged with fontTools and written
as KOSIFJumuah-{Regular,Bold}.{ttf,woff2} next to this script, together with OFL.txt.
Requires: pip install fonttools brotli
"""
from __future__ import annotations

import argparse
import io
import shutil
import sys
import urllib.request
from pathlib import Path

try:
    from fontTools import subset
    from fontTools.merge import Merger
    from fontTools.ttLib import TTFont
    from fontTools.ttLib.scaleUpem import scale_upem
    from fontTools.varLib import instancer
except ImportError:  # pragma: no cover - guidance only
    sys.exit("fontTools is required: pip install fonttools brotli")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RAW = "https://raw.githubusercontent.com/google/fonts/main/ofl"
SOURCES = {
    "amiri/Amiri-Regular.ttf": f"{RAW}/amiri/Amiri-Regular.ttf",
    "amiri/Amiri-Bold.ttf": f"{RAW}/amiri/Amiri-Bold.ttf",
    "amiri/OFL.txt": f"{RAW}/amiri/OFL.txt",
    "bodonimoda/BodoniModa[opsz,wght].ttf": f"{RAW}/bodonimoda/BodoniModa[opsz,wght].ttf",
    "bodonimoda/OFL.txt": f"{RAW}/bodonimoda/OFL.txt",
}
FAMILY = "KOSIF Jumuah"
VERSION = "1.000"
UPM = 1000

# Disjoint code-point sets: Arabic comes from Amiri, everything Latin from Bodoni Moda.
ARABIC_RANGES = [(0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF), (0xFB50, 0xFDFF), (0xFE70, 0xFEFF), (0x200C, 0x200F), (0x2066, 0x2069)]
LATIN_RANGES = [(0x0020, 0x007E), (0x00A0, 0x00FF), (0x2010, 0x2027), (0x2030, 0x203A), (0x2044, 0x2044), (0x20AC, 0x20AC), (0x2122, 0x2122)]
# Bodoni Moda lacks the Arabic percent/decimal marks, so they stay with Amiri (they are inside 0x0600-0x06FF already).


def log(*a) -> None:
    print(*a, file=sys.stderr, flush=True)


def unicodes(ranges) -> list[int]:
    return [cp for lo, hi in ranges for cp in range(lo, hi + 1)]


def download(src: Path, allow: bool) -> None:
    for rel, url in SOURCES.items():
        dest = src / rel
        if dest.exists():
            continue
        if not allow:
            sys.exit(f"missing source {dest}; run without --no-download or place the file there")
        dest.parent.mkdir(parents=True, exist_ok=True)
        log(f"  fetching {rel}")
        req = urllib.request.Request(url, headers={"User-Agent": "KOSIF-font-build/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.write_bytes(resp.read())


def subset_font(font: TTFont, cps: list[int], keep_layout: bool) -> TTFont:
    opts = subset.Options()
    opts.layout_features = ["*"] if keep_layout else []
    opts.name_IDs = ["*"]
    opts.name_languages = ["*"]
    opts.notdef_outline = True
    opts.glyph_names = True
    opts.recalc_bounds = True
    opts.recalc_average_width = True
    opts.drop_tables += ["DSIG"]
    s = subset.Subsetter(opts)
    s.populate(unicodes=cps)
    s.subset(font)
    if not keep_layout:
        for tag in ("GSUB", "GPOS", "GDEF"):
            if tag in font:
                del font[tag]
    return font


def instance_bodoni(path: Path, wght: float, opsz: float) -> TTFont:
    vf = TTFont(path)
    static = instancer.instantiateVariableFont(vf, {"wght": wght, "opsz": opsz}, inplace=False, updateFontNames=True)
    return static


def rename(font: TTFont, style: str, copyright_lines: list[str]) -> None:
    name = font["name"]
    ps = f"KOSIFJumuah-{style}"
    full = f"{FAMILY} {style}"
    records = {
        0: "\n".join(copyright_lines),
        1: FAMILY, 2: style, 3: f"KOSIF:{ps}:{VERSION}", 4: full, 5: f"Version {VERSION}", 6: ps,
        7: "", 8: "KOSIF TOOL (assembly); Khaled Hosny (Amiri); Indestructible Type (Bodoni Moda)",
        9: "Khaled Hosny (Amiri); Owen Earl, Indestructible Type (Bodoni Moda); assembled by KOSIF TOOL",
        10: "Arabic Naskh with stacked ligatures and Didone figures, matched to the KOSIF Friday-greeting typography. Assembled from Amiri and Bodoni Moda under the SIL Open Font License 1.1; renamed as the license requires.",
        11: "https://github.com/kosif199022-jpg/kosif-tool", 12: "https://github.com/aliftype/amiri · https://github.com/indestructible-type/Bodoni",
        13: "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org",
        14: "https://openfontlicense.org", 16: FAMILY, 17: style,
    }
    name.names = []
    for nid, text in records.items():
        if text:
            name.setName(text, nid, 3, 1, 0x409)
    font["head"].fontRevision = float(VERSION)
    os2 = font["OS/2"]
    os2.usWeightClass = 700 if style == "Bold" else 400
    os2.fsSelection = (os2.fsSelection & ~0x60) | (0x20 if style == "Bold" else 0x40)
    os2.fsType = 0  # installable embedding, as permitted by the OFL sources
    font["head"].macStyle = 1 if style == "Bold" else 0


def build(style: str, src: Path, out: Path) -> list[Path]:
    arabic_src = src / "amiri" / ("Amiri-Bold.ttf" if style == "Bold" else "Amiri-Regular.ttf")
    log(f"[{style}] Arabic ← {arabic_src.name}")
    arabic = subset_font(TTFont(arabic_src), unicodes(ARABIC_RANGES), keep_layout=True)
    assert arabic["head"].unitsPerEm == UPM, "Amiri is expected at 1000 UPM"
    log(f"[{style}] Latin ← Bodoni Moda instance")
    latin = instance_bodoni(src / "bodonimoda" / "BodoniModa[opsz,wght].ttf", 600 if style == "Bold" else 400, 11)
    latin = subset_font(latin, unicodes(LATIN_RANGES), keep_layout=False)
    scale_upem(latin, UPM)
    # align vertical metrics with the Arabic master so line boxes stay stable when scripts mix
    for tag, attrs in (("hhea", ("ascent", "descent", "lineGap")), ("OS/2", ("sTypoAscender", "sTypoDescender", "sTypoLineGap", "usWinAscent", "usWinDescent"))):
        for a in attrs:
            setattr(latin[tag], a, getattr(arabic[tag], a))
    tmp_a, tmp_l = out / f"_arabic-{style}.ttf", out / f"_latin-{style}.ttf"
    arabic.save(tmp_a)
    latin.save(tmp_l)
    merged = Merger().merge([str(tmp_a), str(tmp_l)])
    tmp_a.unlink(); tmp_l.unlink()
    rename(merged, style, [
        "Copyright 2010-2024 The Amiri Project Authors (https://github.com/aliftype/amiri). Licensed under the SIL Open Font License 1.1.",
        "Copyright 2020 The Bodoni Moda Project Authors (https://github.com/indestructible-type/Bodoni). Licensed under the SIL Open Font License 1.1.",
        "KOSIF Jumuah: subset, instancing, merge and naming by KOSIF TOOL 2026, SIL Open Font License 1.1.",
    ])
    written = []
    ttf = out / f"KOSIFJumuah-{style}.ttf"
    merged.save(ttf)
    written.append(ttf)
    try:
        woff = TTFont(ttf)
        woff.flavor = "woff2"
        w2 = out / f"KOSIFJumuah-{style}.woff2"
        woff.save(w2)
        written.append(w2)
    except Exception as exc:  # brotli missing
        log(f"  woff2 skipped: {exc}")
    return written


def verify(path: Path) -> str:
    f = TTFont(path)
    cmap = f.getBestCmap()
    need = {"alef": 0x0627, "lam": 0x0644, "taa marbuta": 0x0629, "tatweel": 0x0640, "ﷺ": 0xFDFA, "fatha": 0x064E, "comma": 0x060C, "0": 0x30, "9": 0x39, "A": 0x41, "z": 0x7A, "@": 0x40, ".": 0x2E, "space": 0x20}
    missing = [k for k, cp in need.items() if cp not in cmap]
    fam = f["name"].getDebugName(1)
    return f"{path.name}: family={fam!r} glyphs={len(f.getGlyphOrder())} upm={f['head'].unitsPerEm} GSUB={'GSUB' in f} missing={missing or 'none'}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(REPO / ".kosif-cache" / "fonts-src"))
    ap.add_argument("--out", default=str(HERE))
    ap.add_argument("--no-download", action="store_true")
    a = ap.parse_args(argv)
    src, out = Path(a.src), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    download(src, not a.no_download)
    written = []
    for style in ("Regular", "Bold"):
        written += build(style, src, out)
    # one OFL.txt carrying both upstream notices
    ofl = out / "OFL.txt"
    ofl.write_text(
        "KOSIF Jumuah is assembled from two SIL Open Font License 1.1 families and is itself licensed under the OFL 1.1.\n"
        "The Reserved Font Names 'Amiri' and 'Bodoni Moda' are NOT used for this derivative, as the license requires.\n"
        "Upstream notices follow verbatim.\n\n===== Amiri =====\n\n" + (src / "amiri" / "OFL.txt").read_text(encoding="utf-8") +
        "\n\n===== Bodoni Moda =====\n\n" + (src / "bodonimoda" / "OFL.txt").read_text(encoding="utf-8"), encoding="utf-8")
    for p in written:
        log("  " + verify(p))
    log(f"wrote {len(written)} files + OFL.txt to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
