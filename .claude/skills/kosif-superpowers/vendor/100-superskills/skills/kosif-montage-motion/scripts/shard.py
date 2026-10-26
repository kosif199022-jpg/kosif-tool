"""Split one render across machines (GitHub Actions runners, several PCs): each renders a frame range of the same
deterministic page to its own lossless-joinable segment; one machine joins them, adds the sound, bakes the poster and
runs the gate. The quality settings match `kmotion final` (PNG capture, libx264 slow / CRF 16).

    python scripts/shard.py render PROJECT --shard 0 --of 6 [--blur 4] --out seg00.mp4
    python scripts/shard.py join PROJECT seg00.mp4 seg01.mp4 … --out FILM.mp4
    python scripts/shard.py plan PROJECT --of 6            the frame ranges, as JSON (for a CI matrix)
Workflow: .github/workflows/kosif-render.yml in the render-lab repository (see references/render-farm.md).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def _page(project: str):
    import motion
    d = motion.project_dir(project)
    index = d / "index.html"
    w, h = motion._size(index)
    fps = motion._fps(index)
    seconds = motion.duration_of(index)
    return d, index, w, h, fps, seconds, int(round(seconds * fps))


def plan(project: str, of: int) -> dict:
    _, _, w, h, fps, seconds, n = _page(project)
    b = [round(n * i / of) for i in range(of + 1)]
    return {"frames": n, "fps": fps, "size": f"{w}x{h}", "seconds": seconds, "shards": [{"shard": i, "i0": b[i], "i1": b[i + 1]} for i in range(of)]}


def render(project: str, shard: int, of: int, out: Path, blur: int = 1, frame0_t: float | None = None) -> dict:
    import film
    _, index, w, h, fps, seconds, n = _page(project)
    b = [round(n * i / of) for i in range(of + 1)]
    job = {"src": str(index), "w": w, "h": h, "fps": fps, "blur": max(1, blur), "shutter": 0.5, "stack": "average", "start": 0.0,
           "capture": "png", "preset": "slow", "crf": 16, "scale": 1.0, "frames_dir": None, "i0": b[shard], "i1": b[shard + 1], "seg": str(out), "frame0_t": frame0_t}
    t0 = time.perf_counter()
    rep = film._render_chunk(job)
    return {"shard": shard, "of": of, "frames": b[shard + 1] - b[shard], "seconds": round(time.perf_counter() - t0, 1), "out": str(out), **{k: rep.get(k) for k in ("native_blur",)}}


def join(project: str, segs: list[Path], out: Path, bake: bool = True, poster_drawn: bool = False) -> dict:
    import film
    import motion
    import qa
    _, index, *_ = _page(project)
    film._concat(sorted(segs), out)
    motion.mux_audio(index, out)
    rep: dict = {"out": str(out), "segments": len(segs)}
    if poster_drawn:                                         # frame 0 already shows the poster moment: just save the still
        import poster
        rep["poster"] = {"jpg": str(poster.extract(out, 0.0, out.with_suffix(".poster.jpg"))), "method": "drawn as frame 0 (no re-encode)"}
    elif bake:
        import poster
        t = poster.pick(out)["t"]
        jpg = poster.extract(out, t, out.with_suffix(".poster.jpg"))
        rep["poster"] = {"t": t, **poster.bake(out, jpg, out)}
    g = qa.inspect(out)
    rep["gate"] = {k: g.get(k) for k in ("ok", "issues", "lufs", "true_peak", "size", "fps", "seconds")}
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("project"); p.add_argument("--of", type=int, default=6)
    p = sub.add_parser("render"); p.add_argument("project"); p.add_argument("--shard", type=int, required=True); p.add_argument("--of", type=int, required=True)
    p.add_argument("--blur", type=int, default=1); p.add_argument("--out", required=True)
    p.add_argument("--frame0-t", type=float, help="draw frame 0 at this time (the poster moment)")
    p = sub.add_parser("join"); p.add_argument("project"); p.add_argument("segs", nargs="+"); p.add_argument("--out", required=True); p.add_argument("--no-poster", action="store_true")
    p.add_argument("--poster-drawn", action="store_true", help="the shards drew frame 0 at the poster moment")
    a = ap.parse_args()
    if a.cmd == "plan":
        res = plan(a.project, a.of)
    elif a.cmd == "render":
        res = render(a.project, a.shard, a.of, Path(a.out), a.blur, a.frame0_t)
    else:
        res = join(a.project, [Path(s) for s in a.segs], Path(a.out), not a.no_poster, a.poster_drawn)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
