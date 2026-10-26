"""KOSIF scenes — shot boundaries of real footage, measured (FFmpeg scdet), so an edit can cut where the camera cut.

    python scenes.py CLIP.mp4 [--threshold 10] [--min 0.5] [--out scenes.json]      the shot list
    python scenes.py CLIP.mp4 --sheet shots.png                                     one thumbnail per shot
    python scenes.py CLIP.mp4 --split DIR                                            every shot as its own clip
    python scenes.py CLIP.mp4 --timeline edit.json [--transition fade]              a timeline spec (one clip per shot)

scenes.json: {"file", "duration", "threshold", "scenes": [{"i", "start", "end", "dur", "score"}]}
threshold: scdet's 0–100 scale (10 = the default; lower finds softer changes, higher only hard cuts).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

import tools  # noqa: E402

FF = tools.FF


def _scdet(src: Path, threshold: float) -> list[tuple[float, float]]:
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(src), "-an", "-vf", f"scdet=threshold={threshold}:sc_pass=0", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    hits = re.findall(r"lavfi\.scd\.score:\s*([\d.]+),\s*lavfi\.scd\.time:\s*([\d.]+)", r.stderr or "")
    return [(float(t), float(s)) for s, t in hits]


def _select(src: Path, threshold: float) -> list[tuple[float, float]]:
    """Fallback: the classic select=gt(scene,x) + showinfo (x on a 0–1 scale)."""
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(src), "-an", "-vf", f"select='gt(scene,{threshold / 100:.3f})',showinfo", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return [(float(t), 0.0) for t in re.findall(r"pts_time:\s*([\d.]+)", r.stderr or "")]


def detect(src: Path, threshold: float = 10.0, min_len: float = 0.5) -> dict:
    src = Path(src)
    info = tools.probe(src)
    total = info["duration"]
    hits = _scdet(src, threshold)
    method = "scdet"
    if not hits:
        hits, method = _select(src, threshold), "select"
    cuts: list[tuple[float, float]] = []
    for t, s in sorted(hits):
        if t < min_len or total - t < min_len:
            continue
        if cuts and t - cuts[-1][0] < min_len:               # two hits inside min_len: keep the stronger
            if s > cuts[-1][1]:
                cuts[-1] = (t, s)
            continue
        cuts.append((t, s))
    edges = [0.0] + [t for t, _ in cuts] + [total]
    scenes = [{"i": i, "start": round(edges[i], 3), "end": round(edges[i + 1], 3), "dur": round(edges[i + 1] - edges[i], 3),
               "score": round(cuts[i - 1][1], 2) if i > 0 else None} for i in range(len(edges) - 1)]
    return {"file": str(src), "duration": round(total, 3), "threshold": threshold, "method": method, "scenes": scenes,
            "size": f"{info['video']['w']}x{info['video']['h']}" if info["video"] else None}


def sheet(src: Path, rep: dict, out: Path, cols: int = 4, width: int = 320) -> Path:
    """One thumbnail per shot (its first clean frame + 0.1 s), tiled with the shot number and times."""
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    info = tools.probe(src)
    w, h = info["video"]["w"], info["video"]["h"]
    th = max(2, round(h * width / w))
    tiles = []
    for sc in rep["scenes"]:
        at = min(sc["start"] + 0.1, max(sc["start"], sc["end"] - 0.05))
        raw = subprocess.run([FF, "-v", "error", "-ss", f"{at:.3f}", "-i", str(src), "-frames:v", "1", "-vf", f"scale={width}:{th}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True).stdout
        if len(raw) < width * th * 3:
            tiles.append(Image.new("RGB", (width, th), (20, 20, 20)))
        else:
            tiles.append(Image.fromarray(np.frombuffer(raw[:width * th * 3], np.uint8).reshape(th, width, 3)))
    cols = max(1, min(cols, len(tiles)))
    rows = (len(tiles) + cols - 1) // cols
    pad, cap = 8, 22
    im = Image.new("RGB", (cols * (width + pad) + pad, rows * (th + cap + pad) + pad), (12, 14, 18))
    dr = ImageDraw.Draw(im)
    try:
        fp = tools.font_path(arabic=False); font = ImageFont.truetype(str(fp), 14) if fp else ImageFont.load_default()
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()
    for i, (t, sc) in enumerate(zip(tiles, rep["scenes"])):
        x, y = pad + (i % cols) * (width + pad), pad + (i // cols) * (th + cap + pad)
        im.paste(t, (x, y))
        dr.text((x + 4, y + th + 3), f"#{sc['i']}  {sc['start']:.2f}–{sc['end']:.2f}s  ({sc['dur']:.2f}s)", font=font, fill=(230, 230, 230))
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    return out


def split(src: Path, rep: dict, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    files = []
    for sc in rep["scenes"]:
        f = out_dir / f"{Path(src).stem}_shot{sc['i']:03d}.mp4"
        tools.trim(Path(src), f, sc["start"], sc["end"])
        files.append(f)
    return files


def timeline_spec(src: Path, rep: dict, transition: str | None = None) -> dict:
    clips = []
    for sc in rep["scenes"]:
        c = {"src": str(Path(src).resolve()), "in": sc["start"], "out": sc["end"]}
        if transition and transition not in ("cut", "none"):
            c["transition"] = {"type": transition, "dur": 0.5}
        clips.append(c)
    if clips and "transition" in clips[-1]:
        del clips[-1]["transition"]
    return {"size": rep.get("size") or "1080x1920", "fps": 30, "clips": clips, "overlays": [], "audio": {"keep_clip_audio": True, "lufs": -14}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip")
    ap.add_argument("--threshold", type=float, default=10.0, help="scdet 0–100 (default 10)")
    ap.add_argument("--min", dest="min_len", type=float, default=0.5, help="shortest shot in seconds")
    ap.add_argument("--out", help="scenes.json (default next to the clip)")
    ap.add_argument("--sheet", help="thumbnail sheet PNG")
    ap.add_argument("--split", help="folder for one clip per shot")
    ap.add_argument("--timeline", help="write a timeline spec JSON")
    ap.add_argument("--transition", default=None, help="transition between shots in the timeline spec (default cut)")
    a = ap.parse_args()
    src = Path(a.clip)
    rep = detect(src, a.threshold, a.min_len)
    out = Path(a.out) if a.out else src.with_suffix(".scenes.json")
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    rep["scenes_json"] = str(out)
    if a.sheet:
        rep["sheet"] = str(sheet(src, rep, Path(a.sheet)))
    if a.split:
        rep["clips"] = [str(f) for f in split(src, rep, Path(a.split))]
    if a.timeline:
        Path(a.timeline).write_text(json.dumps(timeline_spec(src, rep, a.transition), ensure_ascii=False, indent=1), encoding="utf-8")
        rep["timeline"] = a.timeline
    print(json.dumps({k: v for k, v in rep.items() if k != "scenes"} | {"shots": len(rep["scenes"])}, ensure_ascii=False, indent=1))
    for sc in rep["scenes"]:
        print(f"  #{sc['i']:<3} {sc['start']:>8.2f} → {sc['end']:>8.2f}  ({sc['dur']:.2f}s)" + (f"  score {sc['score']}" if sc["score"] is not None else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
