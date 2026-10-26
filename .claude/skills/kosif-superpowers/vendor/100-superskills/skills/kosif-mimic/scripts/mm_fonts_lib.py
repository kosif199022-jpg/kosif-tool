"""Arabic font library: catalogue, on-demand fetch (Google Fonts via git), static instancing, system scan.

The skill ships a small core set in assets/fonts. `fetch()` adds ~40 more free Arabic families
(all SIL OFL) into the user cache. System fonts with Arabic coverage are scanned too
(Windows: Traditional Arabic, Sakkal Majalla, Arabic Typesetting…; macOS/iOS: Geeza Pro, Baghdad…).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from mm_common import ASSETS, log

CORE_DIR = ASSETS / "fonts"
CACHE_DIR = Path(os.environ.get("MIMIC_FONT_CACHE", Path.home() / ".cache" / "kosif-mimic" / "fonts"))

# (google/fonts ofl dir, family, style, spec)  spec: {"static": [...]} or {"var": file, "wght": [...], "fix": {axis: value}}
CATALOG = [
    ("amiri", "Amiri", "naskh", {"static": ["Amiri-Regular.ttf", "Amiri-Bold.ttf"]}),
    ("amiriquran", "Amiri Quran", "naskh", {"static": ["AmiriQuran-Regular.ttf"]}),
    ("arefruqaa", "Aref Ruqaa", "ruqaa", {"static": ["ArefRuqaa-Regular.ttf", "ArefRuqaa-Bold.ttf"]}),
    ("scheherazadenew", "Scheherazade New", "naskh", {"static": ["ScheherazadeNew-Regular.ttf", "ScheherazadeNew-Bold.ttf"]}),
    ("notonaskharabic", "Noto Naskh Arabic", "naskh", {"var": "NotoNaskhArabic[wght].ttf", "wght": [400, 700]}),
    ("lateef", "Lateef", "naskh", {"static": ["Lateef-Regular.ttf", "Lateef-Bold.ttf", "Lateef-ExtraBold.ttf"]}),
    ("markazitext", "Markazi Text", "naskh", {"var": "MarkaziText[wght].ttf", "wght": [400, 700]}),
    ("mirza", "Mirza", "naskh", {"static": ["Mirza-Regular.ttf", "Mirza-Bold.ttf"]}),
    ("harmattan", "Harmattan", "naskh", {"static": ["Harmattan-Regular.ttf", "Harmattan-Bold.ttf"]}),
    ("ruwudu", "Ruwudu", "naskh", {"static": ["Ruwudu-Regular.ttf", "Ruwudu-Bold.ttf"]}),
    ("alkalami", "Alkalami", "naskh", {"static": ["Alkalami-Regular.ttf"]}),
    ("katibeh", "Katibeh", "display", {"static": ["Katibeh-Regular.ttf"]}),
    ("reemkufi", "Reem Kufi", "kufi", {"var": "ReemKufi[wght].ttf", "wght": [400, 700]}),
    ("notokufiarabic", "Noto Kufi Arabic", "kufi", {"var": "NotoKufiArabic[wght].ttf", "wght": [400, 700, 900]}),
    ("kufam", "Kufam", "kufi", {"var": "Kufam[wght].ttf", "wght": [400, 700]}),
    ("qahiri", "Qahiri", "kufi", {"static": ["Qahiri-Regular.ttf"]}),
    ("cairo", "Cairo", "sans", {"var": "Cairo[slnt,wght].ttf", "wght": [400, 700, 900], "fix": {"slnt": 0}}),
    ("tajawal", "Tajawal", "sans", {"static": ["Tajawal-Regular.ttf", "Tajawal-Bold.ttf", "Tajawal-Black.ttf"]}),
    ("almarai", "Almarai", "sans", {"static": ["Almarai-Regular.ttf", "Almarai-Bold.ttf", "Almarai-ExtraBold.ttf"]}),
    ("changa", "Changa", "sans", {"var": "Changa[wght].ttf", "wght": [400, 700]}),
    ("mada", "Mada", "sans", {"var": "Mada[wght].ttf", "wght": [400, 700, 900]}),
    ("vazirmatn", "Vazirmatn", "sans", {"var": "Vazirmatn[wght].ttf", "wght": [400, 700, 900]}),
    ("ibmplexsansarabic", "IBM Plex Sans Arabic", "sans", {"static": ["IBMPlexSansArabic-Regular.ttf", "IBMPlexSansArabic-Bold.ttf"]}),
    ("notosansarabic", "Noto Sans Arabic", "sans", {"var": "NotoSansArabic[wdth,wght].ttf", "wght": [400, 700], "fix": {"wdth": 100}}),
    ("readexpro", "Readex Pro", "sans", {"var": "ReadexPro[HEXP,wght].ttf", "wght": [400, 700], "fix": {"HEXP": 0}}),
    ("alexandria", "Alexandria", "sans", {"var": "Alexandria[wght].ttf", "wght": [400, 700, 900]}),
    ("zain", "Zain", "sans", {"static": ["Zain-Regular.ttf", "Zain-Bold.ttf", "Zain-Black.ttf"]}),
    ("beiruti", "Beiruti", "sans", {"var": "Beiruti[wght].ttf", "wght": [400, 700, 900]}),
    ("baloobhaijaan2", "Baloo Bhaijaan 2", "rounded", {"var": "BalooBhaijaan2[wght].ttf", "wght": [400, 700]}),
    ("lemonada", "Lemonada", "rounded", {"var": "Lemonada[wght].ttf", "wght": [400, 700]}),
    ("elmessiri", "El Messiri", "display", {"var": "ElMessiri[wght].ttf", "wght": [400, 700]}),
    ("marhey", "Marhey", "hand", {"var": "Marhey[wght].ttf", "wght": [400, 700]}),
    ("playpensansarabic", "Playpen Sans Arabic", "hand", {"var": "PlaypenSansArabic[wght].ttf", "wght": [400, 700]}),
    ("lalezar", "Lalezar", "display", {"static": ["Lalezar-Regular.ttf"]}),
    ("rakkas", "Rakkas", "display", {"static": ["Rakkas-Regular.ttf"]}),
    ("jomhuria", "Jomhuria", "display", {"static": ["Jomhuria-Regular.ttf"]}),
    ("blaka", "Blaka", "display", {"static": ["Blaka-Regular.ttf"]}),
    ("badeendisplay", "Badeen Display", "display", {"static": ["BadeenDisplay-Regular.ttf"]}),
    ("vibes", "Vibes", "display", {"static": ["Vibes-Regular.ttf"]}),
    ("gulzar", "Gulzar", "nastaliq", {"static": ["Gulzar-Regular.ttf"]}),
    ("notonastaliqurdu", "Noto Nastaliq Urdu", "nastaliq", {"var": "NotoNastaliqUrdu[wght].ttf", "wght": [400, 700]}),
]
STYLE_AR = {"naskh": "نسخ", "ruqaa": "رقعة", "kufi": "كوفي", "sans": "حديث بسيط", "rounded": "مدوّر",
            "display": "عناوين/زخرفي", "hand": "يدوي", "nastaliq": "نستعليق", "system": "خط نظام"}
WEIGHT_NAMES = {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium", 600: "SemiBold",
                700: "Bold", 800: "ExtraBold", 900: "Black"}


def _weight_from_name(fn: str) -> int:
    low = fn.lower()
    for w, n in sorted(WEIGHT_NAMES.items(), key=lambda kv: -len(kv[1])):
        if n.lower() in low:
            return w
    return 400


def instance_variable(src: Path, dst: Path, family: str, axes: dict) -> bool:
    try:
        from fontTools.ttLib import TTFont
        from fontTools.varLib import instancer
    except Exception:
        log("fontTools missing: cannot instance", src.name)
        return False
    f = TTFont(str(src))
    loc = {}
    for ax in f["fvar"].axes:
        loc[ax.axisTag] = axes.get(ax.axisTag, ax.defaultValue)
        loc[ax.axisTag] = max(ax.minValue, min(ax.maxValue, loc[ax.axisTag]))
    st = instancer.instantiateVariableFont(f, loc, inplace=False)
    w = int(loc.get("wght", 400))
    sub = WEIGHT_NAMES.get(w, str(w))
    fam = f"{family} {sub}" if w != 400 else family
    ps = f"{family.replace(' ', '')}-{sub}"
    name = st["name"]
    for rec in list(name.names):
        if rec.nameID in (1, 2, 4, 6, 16, 17, 21, 22, 25):
            name.removeNames(nameID=rec.nameID)
    name.setName(fam, 1, 3, 1, 0x409)
    name.setName("Regular", 2, 3, 1, 0x409)
    name.setName(f"{fam}", 4, 3, 1, 0x409)
    name.setName(ps, 6, 3, 1, 0x409)
    if "OS/2" in st:
        st["OS/2"].usWeightClass = w
    st.save(str(dst))
    return True


def _entry(path: Path, family: str, weight: int, style: str, source: str) -> dict:
    return {"file": path.name, "path": str(path), "family": family, "weight": weight, "style": style,
            "style_ar": STYLE_AR.get(style, style), "source": source}


def build_from_ofl(ofl_root: Path, dest: Path, only: list[str] | None = None) -> list[dict]:
    """Copy/instance catalogue families from a google/fonts checkout (…/ofl) into dest."""
    dest.mkdir(parents=True, exist_ok=True)
    out = []
    for d, fam, style, spec in CATALOG:
        if only and d not in only:
            continue
        src_dir = ofl_root / d
        if not src_dir.exists():
            continue
        lic = src_dir / "OFL.txt"
        if lic.exists():
            shutil.copy2(lic, dest / f"OFL-{fam.replace(' ', '')}.txt")
        if "static" in spec:
            for fn in spec["static"]:
                s = src_dir / fn
                if s.exists():
                    t = dest / fn
                    if not t.exists():
                        shutil.copy2(s, t)
                    out.append(_entry(t, fam, _weight_from_name(fn), style, "Google Fonts (OFL)"))
        else:
            s = src_dir / spec["var"]
            if not s.exists():
                continue
            for w in spec["wght"]:
                t = dest / f"{fam.replace(' ', '')}-{w}.ttf"
                if not t.exists():
                    axes = dict(spec.get("fix", {}))
                    axes["wght"] = w
                    if not instance_variable(s, t, fam, axes):
                        continue
                out.append(_entry(t, fam, w, style, "Google Fonts (OFL)"))
    (dest / "fonts.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def fetch(dest: Path = CACHE_DIR, families: list[str] | None = None) -> list[dict]:
    """Download the catalogue from github.com/google/fonts with a sparse git checkout (works where
    GitHub is reachable, e.g. claude.ai's sandbox), then build static instances into dest."""
    dirs = families or [d for d, *_ in CATALOG]
    tmp = Path(tempfile.mkdtemp(prefix="gfonts-"))
    git = shutil.which("git")
    ok = False
    if git:
        try:
            subprocess.run([git, "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse",
                            "https://github.com/google/fonts", str(tmp / "g")], check=True, timeout=600)
            subprocess.run([git, "-C", str(tmp / "g"), "sparse-checkout", "set"] + [f"ofl/{d}" for d in dirs],
                           check=True, timeout=900)
            ok = True
        except Exception as e:  # pragma: no cover - network dependent
            log("git fetch failed:", e)
    if not ok:  # HTTP fallback (raw.githubusercontent.com) for machines without git
        import urllib.request
        for d, fam, style, spec in CATALOG:
            if d not in dirs:
                continue
            files = spec.get("static") or [spec["var"]]
            for fn in files + ["OFL.txt"]:
                url = f"https://raw.githubusercontent.com/google/fonts/main/ofl/{d}/{urllib.request.quote(fn)}"
                p = tmp / "g" / "ofl" / d / fn
                p.parent.mkdir(parents=True, exist_ok=True)
                try:
                    with urllib.request.urlopen(url, timeout=60) as r:
                        p.write_bytes(r.read())
                    ok = True
                except Exception as e:
                    log("download failed", url, e)
    if not ok:
        return []
    lib = build_from_ofl(tmp / "g" / "ofl", dest, only=dirs)
    shutil.rmtree(tmp, ignore_errors=True)
    log(f"font library: {len(lib)} faces in {dest}")
    return lib


def _system_dirs() -> list[Path]:
    dirs = []
    if sys.platform.startswith("win"):
        dirs += [Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts",
                 Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts"]
    elif sys.platform == "darwin":
        dirs += [Path("/System/Library/Fonts"), Path("/System/Library/Fonts/Supplemental"),
                 Path("/Library/Fonts"), Path.home() / "Library" / "Fonts"]
    else:
        dirs += [Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), Path.home() / ".fonts",
                 Path.home() / ".local" / "share" / "fonts"]
    return [d for d in dirs if d.exists()]


def _covers_arabic(path: Path) -> tuple[bool, str, int]:
    try:
        from fontTools.ttLib import TTFont
        f = TTFont(str(path), lazy=True, fontNumber=0)
        cmap = f.getBestCmap() or {}
        ok = all(cp in cmap for cp in (0x0627, 0x0644, 0x0645, 0x0647))
        fam = f["name"].getDebugName(1) or path.stem
        w = getattr(f["OS/2"], "usWeightClass", 400) if "OS/2" in f else 400
        return ok, fam, int(w)
    except Exception:
        return False, path.stem, 400


def scan_dir(d: Path, source: str, style: str = "system") -> list[dict]:
    out = []
    meta = d / "fonts.json"
    if meta.exists():
        try:
            for e in json.loads(meta.read_text(encoding="utf-8")):
                p = d / e["file"]
                if p.exists():
                    e = dict(e)
                    e["path"] = str(p)
                    out.append(e)
            known = {e["file"] for e in out}
        except Exception:
            known = set()
    else:
        known = set()
    for p in sorted(d.rglob("*")):
        if p.suffix.lower() not in (".ttf", ".otf", ".ttc") or p.name in known:
            continue
        ok, fam, w = _covers_arabic(p)
        if ok:
            out.append(_entry(p, fam, w, style, source))
    return out


def library(extra_dirs: list[Path] | None = None, include_system: bool = True) -> list[dict]:
    """All usable Arabic faces: core bundle + fetched cache + extra dirs (e.g. WORK/fonts) + system."""
    seen = set()
    lib = []
    for d, src in [(CORE_DIR, "core")] + [(CACHE_DIR, "cache")] + [(Path(x), "user") for x in (extra_dirs or [])]:
        if d.exists():
            for e in scan_dir(d, src, style="user" if src == "user" else "system"):
                key = (e["family"], e["weight"], Path(e["path"]).name)
                if key not in seen:
                    seen.add(key)
                    lib.append(e)
    if include_system:
        for d in _system_dirs():
            for e in scan_dir(d, "system"):
                key = (e["family"], e["weight"], Path(e["path"]).name)
                if key not in seen and "unifont" not in e["family"].lower():
                    seen.add(key)
                    lib.append(e)
    return lib


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Arabic font library for the mimic skill")
    ap.add_argument("cmd", choices=["list", "fetch", "build-ofl"])
    ap.add_argument("--ofl", help="path to a google/fonts 'ofl' folder (build-ofl)")
    ap.add_argument("--dest", default=str(CACHE_DIR))
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    if a.cmd == "list":
        for e in library():
            print(f"{e['family']:<26} {e['weight']:>4} {e['style']:<9} {e['source']:<7} {e['file']}")
    elif a.cmd == "fetch":
        lib = fetch(Path(a.dest), a.only)
        print(f"{len(lib)} faces → {a.dest}")
    else:
        lib = build_from_ofl(Path(a.ofl), Path(a.dest), a.only)
        print(f"{len(lib)} faces → {a.dest}")
