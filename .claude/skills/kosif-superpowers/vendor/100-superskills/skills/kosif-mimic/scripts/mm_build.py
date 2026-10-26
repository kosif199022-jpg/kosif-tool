"""Build the remake from spec.json.

Per shot (ffmpeg): trim at the chosen in-point → speed → constant fps → fit (cover/contain/blur) →
colour transfer LUT towards the reference shot → exactly the shot's frame count.
Then one Python pass composes every output frame: Ken Burns, the measured transitions (same kind and
progress curve), vignette/grain/letterbox/fades, and the text events replayed with their measured
animation — and pipes it to ONE H.264 encode that copies the reference's original audio untouched.
"""
from __future__ import annotations

import math
import os
import time
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path

import numpy as np

import mm_color
import mm_img
import mm_transitions as TR
from mm_common import Timer, ensure_dir, ffmpeg, fps_str, load_json, log, probe, rnd, run, save_json, work_paths
from mm_textfx import EventLayer, consensus_style
from mm_video import FrameReader, FrameWriter, even


# ----------------------------------------------------------------------------- shot preparation

def _fit_filter(sw, sh, W, H, fit: str, focus=(0.5, 0.5)) -> str:
    if fit == "cover":
        k = max(W / sw, H / sh)
        nw, nh = max(W, int(math.ceil(sw * k))), max(H, int(math.ceil(sh * k)))
        fx, fy = focus
        x = int(round((nw - W) * min(1, max(0, fx))))
        y = int(round((nh - H) * min(1, max(0, fy))))
        return f"scale={nw}:{nh}:flags=lanczos,crop={W}:{H}:{x}:{y},setsar=1"
    # contain on a blurred, darkened cover of itself (the common 'blur background' fit)
    k = min(W / sw, H / sh)
    nw, nh = even(sw * k), even(sh * k)
    kc = max(W / sw, H / sh)
    cw, ch = int(math.ceil(sw * kc)), int(math.ceil(sh * kc))
    if fit == "contain":
        return f"scale={nw}:{nh}:flags=lanczos,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,setsar=1"
    return (f"split[a][b];[a]scale={cw}:{ch},crop={W}:{H},boxblur=20:2,eq=brightness=-0.06[bg];"
            f"[b]scale={nw}:{nh}:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1")


def _chain(rep: dict, info: dict, W, H, fps: Fraction, speed: float, pingpong_frames: int | None, extra: str = "") -> str:
    parts = []
    if abs(speed - 1.0) > 1e-3:
        parts.append(f"setpts=(PTS-STARTPTS)/{speed:.6f}")
    parts.append(f"fps={fps_str(fps)}")
    parts.append(_fit_filter(info["w"], info["h"], W, H, rep.get("fit", "cover"), tuple(rep.get("focus", (0.5, 0.5)))))
    if rep.get("flip"):
        parts.append("hflip")
    if pingpong_frames:
        parts.append(f"split[f][r0];[r0]reverse[r];[f][r]concat=n=2:v=1:a=0,loop=loop=-1:size={2 * pingpong_frames}:start=0")
    if extra:
        parts.append(extra)
    return ",".join(parts)


def prep_shot(shot: dict, work: Path, W: int, H: int, fps: Fraction, out_dir: Path, look_key: str,
              grade_strength: float, fast: bool = False) -> dict:
    rep = shot["replacement"]
    src = Path(rep["path"])
    if not src.is_absolute():
        src = (work / src).resolve()
    info = probe(src)
    n = shot["end"] - shot["start"]
    need = n / float(fps)
    t_in = float(rep.get("in", 0.0))
    speed = float(rep.get("speed", 1.0))
    avail = max(0.05, info["duration"] - t_in)
    pingpong = None
    if avail / speed < need:
        if avail / need >= 0.6:
            speed = max(0.6, avail / need * 0.985)
            log(f"shot {shot['id']}: clip short → slowed to {speed:.2f}×")
        else:
            t_in = max(0.0, min(t_in, info["duration"] - avail))
            pingpong = max(2, int(avail * float(fps) / speed) - 1)
            log(f"shot {shot['id']}: clip too short even slowed → ping-pong loop")
    rep["_used"] = {"in": rnd(t_in), "speed": rnd(speed, 4), "pingpong": bool(pingpong)}
    # 1) colour statistics of the fitted clip (small) → Reinhard LUT towards the reference shot
    lut_path = None
    target = shot.get(look_key) or shot.get("lab")
    if target and grade_strength > 0 and rep.get("grade", "auto") != "none":
        sw, sh = even(W / 6), even(H / 6)
        chain = _chain(rep, info, sw, sh, fps, speed, None)
        r = FrameReader(src, size=(sw, sh), start=t_in, duration=min(avail, need * speed + 0.1), vf_pre=chain)
        frs = [f.copy() for f in r]
        r.close()
        if frs:
            pick = [frs[i] for i in np.linspace(0, len(frs) - 1, num=min(8, len(frs))).round().astype(int)]
            if look_key == "lab_center":
                h_, w_ = pick[0].shape[:2]
                yy, xx = np.mgrid[0:h_, 0:w_]
                rr = np.sqrt(((xx - w_ / 2) / (w_ / 2)) ** 2 + ((yy - h_ / 2) / (h_ / 2)) ** 2) / math.sqrt(2)
                cm = rr < 0.6
                src_stats = mm_color.merge_stats([mm_color.lab_stats(p, cm) for p in pick])
            else:
                src_stats = mm_color.merge_stats([mm_color.lab_stats(p) for p in pick])
            lut = mm_color.reinhard_lut(src_stats, target, size=33, strength=grade_strength,
                                        chroma_strength=min(1.0, grade_strength + 0.05))
            lut_path = out_dir / f"shot{shot['id']:02d}.cube"
            mm_color.write_cube(lut_path, lut, 33, title=f"shot {shot['id']}")
            rep["_used"]["grade_from"] = src_stats
    extra = f"lut3d=file='{lut_path.as_posix()}'" if lut_path else ""
    chain = _chain(rep, info, W, H, fps, speed, pingpong, extra)
    out = out_dir / f"prep{shot['id']:02d}.mkv"
    cmd = [ffmpeg(), "-v", "error", "-y", "-nostdin"]
    if t_in > 0:
        cmd += ["-ss", f"{t_in:.6f}"]
    cmd += ["-i", str(src), "-an", "-sn", "-filter_complex", f"[0:v]{chain}[v]", "-map", "[v]",
            "-frames:v", str(n), "-c:v", "libx264", "-preset", "ultrafast" if fast else "veryfast",
            "-crf", "14" if fast else "10", "-pix_fmt", "yuv444p", str(out)]
    run(cmd, quiet=True)
    return {"id": shot["id"], "path": str(out), "frames": n, "speed": speed, "in": t_in}


# ----------------------------------------------------------------------------- look helpers

def _radial(W, H):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    return np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)


def vignette_mask(W, H, strength: float) -> np.ndarray:
    r = _radial(W, H)
    return (1.0 - strength * np.clip(r, 0, 1) ** 2.2).astype(np.float32)[..., None]


def solve_vignette(ref_ratio: float, plate_ratio: float, W=96, H=170) -> float:
    r = _radial(W, H)
    cr = float((r[r > 0.85] ** 2.2).mean())
    cc = float((r[r < 0.25] ** 2.2).mean())
    R = ref_ratio / max(1e-3, plate_ratio)
    if R >= 0.995:
        return 0.0
    v = (1 - R) / max(1e-3, cr - R * cc)
    return float(np.clip(v, 0, 0.9))


_GRAIN_K = {}


def grain_gain(crf: int) -> float:
    """How much of a Gaussian grain survives our H.264 encode (measured once per crf)."""
    if crf in _GRAIN_K:
        return _GRAIN_K[crf]
    import subprocess
    import tempfile
    w, h, sig = 320, 568, 6.0
    rng = np.random.default_rng(1)
    tmp = Path(tempfile.mkdtemp()) / "g.mp4"
    p = subprocess.Popen([ffmpeg(), "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                          "-framerate", "30", "-i", "-", "-c:v", "libx264", "-crf", str(crf), "-preset", "medium",
                          "-pix_fmt", "yuv420p", str(tmp)], stdin=subprocess.PIPE)
    base = np.full((h, w, 3), 128.0, np.float32)
    for _ in range(12):
        n_ = rng.normal(0, sig, (h, w, 1)).astype(np.float32)
        p.stdin.write(np.clip(base + n_, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close()
    p.wait()
    meas = []
    r = FrameReader(tmp, size=(w, h))
    for fr in r:
        g = mm_img.to_gray(fr)
        hp = g - mm_img.gaussian_blur(g, 1.2)
        meas.append(1.4826 * float(np.median(np.abs(hp))))
    r.close()
    tmp.unlink(missing_ok=True)
    # analyser measures on a downscaled copy; the build adds grain at full size — same estimator at 1:1 here
    k = float(np.median(meas)) / sig if meas else 0.5
    _GRAIN_K[crf] = max(0.05, k)
    return _GRAIN_K[crf]


# ----------------------------------------------------------------------------- placeholder

def placeholder_frames(shot: dict, W: int, H: int, n: int):
    pal = shot.get("palette") or [{"hex": "#334455"}, {"hex": "#AABBCC"}]
    c1 = np.array(mm_color.rgb_of(pal[0]["hex"]), np.float32)
    c2 = np.array(mm_color.rgb_of(pal[min(1, len(pal) - 1)]["hex"]), np.float32)
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    for k in range(n):
        ph = 0.15 * math.sin(k / 25.0)
        g = np.clip(y + ph, 0, 1)
        yield (c1 * (1 - g) + c2 * g).repeat(W, axis=1)


# ----------------------------------------------------------------------------- build

class ShotSource:
    def __init__(self, shot, prep: dict | None, W, H, fps, kenburns: bool):
        self.shot = shot
        self.n = shot["end"] - shot["start"]
        self.W, self.H = W, H
        self.fps = float(fps)
        self.k = 0
        self.reader = FrameReader(prep["path"], size=(W, H)) if prep else None
        self.gen = None if prep else placeholder_frames(shot, W, H, self.n)
        kb = shot.get("kenburns") if kenburns else None
        self.kb = kb if kb and kb.get("apply") else None

    def next(self) -> np.ndarray:
        if self.reader:
            fr = self.reader.read_or_last().astype(np.float32)
        else:
            fr = next(self.gen, None)
            if fr is None:
                fr = np.zeros((self.H, self.W, 3), np.float32)
        if self.kb:
            zps = float(self.kb.get("zoom_per_s", 1.0))
            t = self.k / self.fps
            dur = self.n / self.fps
            z = zps ** t if zps >= 1 else zps ** (t - dur)
            if abs(z - 1) > 1e-4:
                M = np.array([[z, 0, (1 - z) * self.W / 2], [0, z, (1 - z) * self.H / 2]], np.float32)
                fr = mm_img.warp_affine(fr, M, (self.W, self.H), border="reflect")
        self.k += 1
        return fr

    def close(self):
        if self.reader:
            self.reader.close()


def build(work: str, out: str | None = None, preview: bool = False, placeholder: bool = False,
          crf: int = 17, preset: str = "medium", engine: str = "auto", kenburns: bool = True,
          grade_strength: float = 0.85, jobs: int = 2, frames: tuple[int, int] | None = None) -> dict:
    t0 = time.time()
    P = work_paths(work)
    spec = load_json(P["spec"])
    ref = spec["reference"]
    fps = Fraction(ref["fps"])
    W0, H0, N = ref["w"], ref["h"], ref["frames"]
    scale = 0.5 if preview else 1.0
    W, H = even(W0 * scale), even(H0 * scale)
    bdir = ensure_dir(P["build"] / ("preview" if preview else "full"))
    out = Path(out) if out else P["root"] / ("remake_preview.mp4" if preview else "remake.mp4")
    shots = spec["shots"]
    missing = [s["id"] for s in shots if not (s.get("replacement") or {}).get("path")]
    if missing and not placeholder:
        raise SystemExit(f"shots without replacement footage: {missing}. Run `mimic match` / set "
                         f"shots[].replacement.path, or build with --placeholder for a draft.")
    look = spec.get("look", {})
    vig_ref = (look.get("vignette") or {})
    use_vig = (vig_ref.get("strength") or 0) > 0.02
    look_key = "lab_center" if use_vig else "lab"
    # 1. prepare shots (parallel)
    preps: dict[int, dict] = {}
    with Timer("prepare shots"):
        todo = [s for s in shots if (s.get("replacement") or {}).get("path")]
        with ThreadPoolExecutor(max_workers=max(1, jobs)) as ex:
            futs = {ex.submit(prep_shot, s, P["root"], W, H, fps, bdir, look_key, grade_strength, preview): s["id"]
                    for s in todo}
            for f, sid in futs.items():
                preps[sid] = f.result()
    # 2. text layers
    cons = consensus_style(spec.get("texts", []))
    tw = min(W0, H0)
    analysis_w = (540 if tw > 540 else tw) * (W0 / tw)
    layers = []
    with Timer("typeset text"):
        for ev in spec.get("texts", []):
            evs = _scaled_event(ev, scale) if scale != 1 else ev
            L = EventLayer(evs, W, H, analysis_w * scale, engine, consensus=_scale_style(cons, scale))
            if L.ok:
                layers.append(L)
    # 3. look calibration
    vmask = None
    vig_strength = 0.0
    if use_vig:
        plate_ratio = _plate_corner_ratio(shots, preps, W, H)
        vig_strength = solve_vignette(vig_ref.get("corner_ratio", 0.8), plate_ratio) if plate_ratio else vig_ref["strength"]
        vmask = vignette_mask(W, H, vig_strength) if vig_strength > 0.01 else None
    g_ref = float((look.get("grain") or {}).get("sigma") or 0)
    grain_sigma = 0.0
    if g_ref > 0.35:
        k = grain_gain(crf)
        # the analyser measured on a 360-px-short-side copy; noise shrinks ~1/sqrt(downscale) per pixel
        ds = max(1.0, min(W0, H0) / 360.0)
        grain_sigma = float(np.clip(g_ref * math.sqrt(ds) / k * scale ** 0.5, 0, 25))
    tiles = None
    if grain_sigma > 0.2:
        rng = np.random.default_rng(11)
        tiles = [rng.normal(0, grain_sigma, (H, W, 1)).astype(np.float32) for _ in range(6)]
    lb = look.get("letterbox") or {}
    lb_top, lb_bot = int(round((lb.get("top") or 0) * H)), int(round((lb.get("bottom") or 0) * H))
    fin, fout = int(look.get("fade_in_frames") or 0), int(look.get("fade_out_frames") or 0)
    # 4. compose + encode
    trans = {t["ts"]: t for t in spec["transitions"] if t["frames"] > 0}
    f0, f1 = (0, N) if frames is None else frames
    audio_src = ref["path"] if (ref.get("audio") or {}).get("has_audio") and frames is None else None
    writer = FrameWriter(out, W, H, fps, audio_from=audio_src, crf=crf, preset="veryfast" if preview else preset)
    sources: dict[int, ShotSource] = {}

    def src(i):
        s = shots[i]
        if s["id"] not in sources:
            sources[s["id"]] = ShotSource(s, preps.get(s["id"]), W, H, fps, kenburns)
        return sources[s["id"]]

    with Timer("compose + encode"):
        cur = 0
        n = 0
        stats = {"frames": 0, "transition_frames": 0}
        while n < N:
            while cur + 1 < len(shots) and n >= shots[cur]["end"]:
                sources.pop(shots[cur]["id"]).close() if shots[cur]["id"] in sources else None
                cur += 1
            t = None
            if cur + 1 < len(shots):
                t = next((tt for tt in spec["transitions"] if tt["frames"] > 0 and tt["ts"] <= n < tt["te"]
                          and tt.get("between", [0])[0] == shots[cur]["id"]), None)
            A = src(cur).next()
            if t is not None:
                B = src(cur + 1).next()
                j = n - t["ts"]
                D = t["te"] - t["ts"]
                prog = t.get("progress") or []
                q = prog[j] if len(prog) == D else (j + 1) / (D + 1)
                frame = TR.render(t["type"], A, B, 1.0 - q, **(t.get("params") or {}))
                stats["transition_frames"] += 1
            else:
                frame = A
            if vmask is not None:
                frame = frame * vmask
            if tiles is not None:
                frame = frame + tiles[n % len(tiles)]
            if lb_top:
                frame[:lb_top] = 0
            if lb_bot:
                frame[H - lb_bot:] = 0
            if fin and n < fin:
                frame = frame * ((n + 1) / (fin + 1))
            if fout and n >= N - fout:
                frame = frame * ((N - n) / (fout + 1))
            frame = np.clip(frame, 0, 255).astype(np.uint8)
            for L in layers:
                frame = L.draw(frame, n)
            if f0 <= n < f1:
                writer.write(frame)
                stats["frames"] += 1
            n += 1
        for s in list(sources.values()):
            s.close()
        writer.close()
    info = probe(out)
    report = {"output": str(out), "w": W, "h": H, "fps": fps_str(fps), "frames_written": stats["frames"],
              "frames_expected": (f1 - f0), "duration": rnd(info.get("duration")), "audio": "original stream copied" if audio_src else "none",
              "vignette_strength": rnd(vig_strength), "grain_sigma": rnd(grain_sigma, 2),
              "texts_rendered": [L.id for L in layers], "font_files": sorted({Path(L.font).name for L in layers}),
              "shots": [{"id": s["id"], **(s.get("replacement") or {}).get("_used", {})} for s in shots],
              "seconds": rnd(time.time() - t0, 1), "preview": preview}
    save_json(bdir / "build_report.json", report)
    spec_out = load_json(P["spec"])
    for s_new, s_old in zip(spec_out["shots"], shots):
        if s_old.get("replacement") and s_new.get("replacement"):
            s_new["replacement"]["_used"] = s_old["replacement"].get("_used")
    save_json(P["spec"], spec_out)
    log(f"remake → {out} ({stats['frames']} frames, {report['seconds']}s)")
    return report


def _plate_corner_ratio(shots, preps, W, H) -> float | None:
    ratios = []
    r = _radial(96, 170) if H > W else _radial(170, 96)
    for s in shots:
        p = preps.get(s["id"])
        if not p:
            continue
        rd = FrameReader(p["path"], size=(r.shape[1], r.shape[0]), frames=min(30, p["frames"]))
        for k, fr in enumerate(rd):
            if k % 6:
                continue
            g = mm_img.to_gray(fr)
            ratios.append(float(g[r > 0.85].mean() / max(1e-3, g[r < 0.25].mean())))
        rd.close()
    return float(np.median(ratios)) if ratios else None


def _scale_style(st: dict, s: float) -> dict:
    if not st or s == 1:
        return st
    out = {}
    for k, v in st.items():
        if isinstance(v, dict):
            out[k] = {kk: (vv * s if kk.endswith("_px") else vv) for kk, vv in v.items()}
        else:
            out[k] = v
    return out


def _scaled_event(ev: dict, s: float) -> dict:
    import copy
    e = copy.deepcopy(ev)
    for ln in e.get("lines", []):
        ln["bbox"] = [v * s for v in ln["bbox"]]
        ln["ink_h"] = ln["ink_h"] * s
        if ln.get("ink_w"):
            ln["ink_w"] = ln["ink_w"] * s
    e["style"] = _scale_style(e.get("style") or {}, s)
    for k in ("anim_in", "anim_out"):
        an = e.get(k) or {}
        c = an.get("curves") or {}
        for key in ("dx", "dy"):
            if key in c:
                c[key] = [v * s for v in c[key]]
        for key in ("word_onsets", "word_offsets"):
            for d in an.get(key) or []:
                if d.get("box"):
                    d["box"] = [v * s for v in d["box"]]
    return e
