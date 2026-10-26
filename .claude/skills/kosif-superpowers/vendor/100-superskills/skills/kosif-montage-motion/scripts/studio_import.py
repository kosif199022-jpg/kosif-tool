"""KOSIF studio_import — a KOSIF Studio 6.0 project (the browser montage editor's JSON, version 1) → a timeline spec,
so a cut made quickly in the browser renders offline at full quality (FFmpeg, −14 LUFS, MP4) instead of a real-time
MediaRecorder capture.

    python studio_import.py project.json --out edit.json [--media DIR] [--size WxH]
    python studio_import.py project.json --out edit.json --render film.mp4      # convert and render in one go

Mapping (every decision is listed in the report):
  clip video  → {src, in: trim, out: trim+duration, volume, fit}      clip image → {image, dur, fit}
  clip demo   → a colour card in the preset's colour (aurora/sunset/grid) + the preset's name as a note
  overlay text → text overlay (x/y % → fractions of the frame, size % of the height → px, fade/rise/zoom → fade/rise/fade)
  overlay shape → skipped (reported); soundtrack → audio.music {src, start: -trim, gain dB from volume}
Assets are matched by name inside --media (the Studio keeps bytes on the user's device; the JSON holds names only).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

SIZES = {"16:9": "1280x720", "9:16": "720x1280", "1:1": "720x720"}
PRESET_COLOURS = {"aurora": "#0b2a3a", "sunset": "#3a1a12", "grid": "#101828"}
ANIM = {"none": "none", "fade": "fade", "rise": "rise", "zoom": "fade"}
MEDIA_EXT = (".mp4", ".mov", ".mkv", ".webm", ".m4v", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")


def find_asset(asset: dict, media_dir: Path | None) -> Path | None:
    """The asset's file by exact name under --media (recursively), else by stem, else None."""
    if not media_dir or not media_dir.exists():
        return None
    name = str(asset.get("name", ""))
    direct = media_dir / name
    if direct.is_file():
        return direct
    hits = [p for p in media_dir.rglob("*") if p.is_file() and p.name == name]
    if not hits:
        stem = Path(name).stem.lower()
        hits = [p for p in media_dir.rglob("*") if p.is_file() and p.stem.lower() == stem and p.suffix.lower() in MEDIA_EXT]
    return hits[0] if hits else None


def convert(project: dict, media_dir: Path | None = None, size: str | None = None) -> tuple[dict, dict]:
    if not isinstance(project, dict) or project.get("version") != 1:
        raise ValueError("a KOSIF Studio project (version 1) is required")
    assets = {a.get("id"): a for a in project.get("assets") or [] if isinstance(a, dict)}
    report: dict = {"name": project.get("name"), "clips": [], "overlays": [], "skipped": [], "missing_media": [], "notes": []}
    w, h = (int(v) for v in (size or SIZES.get(project.get("aspect", "16:9"), SIZES["16:9"])).lower().split("x"))
    spec: dict = {"size": f"{w}x{h}", "fps": 30, "background": project.get("background") or "#07111e", "clips": [], "overlays": [],
                  "audio": {"keep_clip_audio": True, "duck": "none", "lufs": -14}}
    total = 0.0
    for i, c in enumerate(project.get("clips") or []):
        kind = c.get("type", "demo"); dur = float(c.get("duration", 5)); fit = c.get("fit", "cover")
        if kind in ("video", "image"):
            a = assets.get(c.get("assetId")) or {}
            f = find_asset(a, media_dir)
            if not f:
                report["missing_media"].append(a.get("name") or c.get("assetId"))
                spec["clips"].append({"color": "#202020", "dur": dur})
                report["clips"].append({"i": i, "type": kind, "asset": a.get("name"), "mapped": "placeholder colour (media not found)"})
            elif kind == "video":
                trim = float(c.get("trim", 0.0))
                spec["clips"].append({"src": str(f), "in": round(trim, 3), "out": round(trim + dur, 3), "volume": float(c.get("volume", 1.0)), "fit": fit})
                report["clips"].append({"i": i, "type": "video", "asset": f.name, "in": trim, "out": trim + dur})
            else:
                spec["clips"].append({"image": str(f), "dur": dur, "fit": fit})
                report["clips"].append({"i": i, "type": "image", "asset": f.name, "dur": dur})
        else:
            preset = c.get("preset", "aurora")
            spec["clips"].append({"color": PRESET_COLOURS.get(preset, "#101828"), "dur": dur})
            report["clips"].append({"i": i, "type": "demo", "preset": preset, "mapped": "colour card (the Studio's procedural preset has no offline twin yet)"})
        total += dur
    if not spec["clips"]:
        raise ValueError("the project has no clips")
    for i, o in enumerate(project.get("overlays") or []):
        if o.get("type") != "text":
            report["skipped"].append({"i": i, "type": o.get("type"), "why": "shapes are not mapped yet"}); continue
        start = float(o.get("start", 0.0)); end = min(total, start + float(o.get("duration", 4.0)))
        if end - start < 0.1:
            report["skipped"].append({"i": i, "type": "text", "why": "outside the film"}); continue
        size_px = max(14, round(h * float(o.get("size", 8)) / 100))
        x, y = float(o.get("x", 50)) / 100, float(o.get("y", 50)) / 100
        ov = {"type": "text", "text": str(o.get("text", "")), "start": round(start, 3), "end": round(end, 3), "size": size_px, "color": o.get("color", "#ffffff"),
              "x": round(x, 4), "y": round(y, 4), "anim": ANIM.get(o.get("animation", "fade"), "fade"), "shadow": True}
        if float(o.get("opacity", 1.0)) < 1.0:
            a = max(0, min(255, round(255 * float(o["opacity"]))))
            ov["color"] = (o.get("color", "#ffffff") + f"{a:02x}")
        spec["overlays"].append(ov)
        report["overlays"].append({"i": i, "text": ov["text"][:40], "start": start, "end": end})
    st = project.get("soundtrack")
    if isinstance(st, dict):
        a = assets.get(st.get("assetId")) or {}
        f = find_asset(a, media_dir)
        if f:
            vol = float(st.get("volume", 0.6)); gain = round(20 * math.log10(max(0.01, vol)), 2)
            spec["audio"]["music"] = {"src": str(f), "gain": gain, "fade_in": 0.3, "fade_out": 1.0, "loop": False}
            if float(st.get("trim", 0.0)) > 0:
                report["notes"].append(f"soundtrack trim {st['trim']} s is not applied (the timeline starts music at 0); trim the file or set audio.music.start")
            spec["audio"]["duck"] = "clips" if any("src" in c for c in spec["clips"]) else "none"
        else:
            report["missing_media"].append(a.get("name") or st.get("assetId"))
    report["seconds"] = round(total, 3)
    report["size"] = spec["size"]
    return spec, report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project"); ap.add_argument("--out", required=True, help="timeline spec JSON")
    ap.add_argument("--media", help="folder holding the project's media files (matched by name)")
    ap.add_argument("--size", help="override WxH (default from the project's aspect: 1280x720 / 720x1280 / 720x720)")
    ap.add_argument("--render", help="also render the timeline to this MP4")
    a = ap.parse_args()
    project = json.loads(Path(a.project).read_text(encoding="utf-8"))
    spec, report = convert(project, Path(a.media) if a.media else None, a.size)
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    report["spec"] = str(out)
    if a.render:
        import timeline
        rep = timeline.build(spec, Path(a.render), inspect=True)
        report["film"] = rep["file"]; report["gate"] = rep.get("gate")
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
