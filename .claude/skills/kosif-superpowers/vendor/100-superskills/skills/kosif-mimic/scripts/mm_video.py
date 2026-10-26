"""Frame-exact video I/O through ffmpeg pipes (raw RGB24), single-frame grabs and audio extraction."""
from __future__ import annotations

import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np

from mm_common import ffmpeg, fps_str, log, run


def even(x: float) -> int:
    v = int(round(x))
    return v - (v % 2)


def fit_short_side(w: int, h: int, short: int) -> tuple[int, int]:
    if min(w, h) <= short:
        return even(w), even(h)
    s = short / min(w, h)
    return even(w * s), even(h * s)


class FrameReader:
    """Iterate RGB frames of a video at a constant frame rate, optionally scaled and trimmed.

    start/duration are in seconds (input-side accurate seek). fps forces CFR (frame n ↔ n/fps)."""

    def __init__(self, path, size: tuple[int, int] | None = None, fps: Fraction | None = None,
                 start: float | None = None, duration: float | None = None, frames: int | None = None,
                 vf_pre: str | None = None, vf_post: str | None = None, gray: bool = False,
                 interp: str = "area"):
        self.path = str(path)
        self.size = size
        self.gray = gray
        filters = []
        if vf_pre:
            filters.append(vf_pre)
        if fps:
            filters.append(f"fps={fps_str(fps)}")
        if size:
            filters.append(f"scale={size[0]}:{size[1]}:flags={interp}")
        if vf_post:
            filters.append(vf_post)
        pix = "gray" if gray else "rgb24"
        filters.append(f"format={pix}")
        cmd = [ffmpeg(), "-v", "error", "-nostdin"]
        if start is not None and start > 0:
            cmd += ["-ss", f"{start:.6f}"]
        cmd += ["-i", self.path]
        if duration is not None:
            cmd += ["-t", f"{duration:.6f}"]
        cmd += ["-an", "-sn", "-vf", ",".join(filters)]
        if frames is not None:
            cmd += ["-frames:v", str(int(frames))]
        cmd += ["-f", "rawvideo", "-pix_fmt", pix, "-"]
        if size is None:
            from mm_common import probe
            info = probe(self.path)
            self.size = (info["w"], info["h"])
        self.w, self.h = self.size
        self.ch = 1 if gray else 3
        self.nbytes = self.w * self.h * self.ch
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=self.nbytes * 4)
        self.count = 0
        self.last = None

    def read(self) -> np.ndarray | None:
        buf = self.proc.stdout.read(self.nbytes)
        if not buf or len(buf) < self.nbytes:
            return None
        self.count += 1
        arr = np.frombuffer(buf, np.uint8)
        self.last = arr.reshape(self.h, self.w) if self.gray else arr.reshape(self.h, self.w, 3)
        return self.last

    def read_or_last(self) -> np.ndarray:
        """Next frame, or the last good frame again when the stream ran out (keeps timelines exact)."""
        fr = self.read()
        if fr is None:
            if self.last is None:
                return np.zeros((self.h, self.w) if self.gray else (self.h, self.w, 3), np.uint8)
            return self.last
        return fr

    def __iter__(self):
        while True:
            fr = self.read()
            if fr is None:
                break
            yield fr

    def close(self):
        try:
            if self.proc.stdout:
                self.proc.stdout.close()
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class FrameWriter:
    """Encode RGB frames to H.264 (optionally muxing an audio stream copied from another file)."""

    def __init__(self, out, w: int, h: int, fps: Fraction, audio_from: str | None = None,
                 audio_copy: bool = True, crf: int = 17, preset: str = "medium", extra_v: list | None = None,
                 lossless_intermediate: bool = False, audio_map: str = "1:a:0?", tune: str | None = None):
        self.out = str(out)
        self.w, self.h = w, h
        cmd = [ffmpeg(), "-v", "error", "-y", "-nostdin", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{w}x{h}", "-framerate", fps_str(fps), "-i", "-"]
        if audio_from:
            cmd += ["-i", str(audio_from)]
        cmd += ["-map", "0:v:0"]
        if audio_from:
            cmd += ["-map", audio_map]
        if lossless_intermediate:
            cmd += ["-c:v", "libx264", "-preset", "veryfast", "-qp", "0", "-pix_fmt", "yuv444p"]
        else:
            cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                    "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-profile:v", "high",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-color_range", "tv"]
            if tune:
                cmd += ["-tune", tune]
        if extra_v:
            cmd += extra_v
        if audio_from:
            cmd += ["-c:a", "copy"] if audio_copy else ["-c:a", "aac", "-b:a", "256k", "-ar", "48000"]
        cmd += ["-movflags", "+faststart", self.out]
        log("encode →", Path(self.out).name)
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.count = 0

    def write(self, frame: np.ndarray):
        if frame.dtype != np.uint8:
            frame = np.clip(frame, 0, 255).astype(np.uint8)
        if frame.shape[0] != self.h or frame.shape[1] != self.w:
            raise ValueError(f"frame {frame.shape} does not match writer {self.w}x{self.h}")
        self.proc.stdin.write(np.ascontiguousarray(frame).tobytes())
        self.count += 1

    def close(self):
        self.proc.stdin.close()
        err = self.proc.stderr.read().decode("utf-8", "replace")
        rc = self.proc.wait()
        if rc != 0:
            raise RuntimeError(f"encoder failed ({rc}): {err[-2000:]}")
        return self.out


def grab_frame(path, t: float, size: tuple[int, int] | None = None) -> np.ndarray:
    """One RGB frame at time t (seconds), accurate seek."""
    r = FrameReader(path, size=size, start=max(0.0, t), frames=1)
    fr = r.read()
    r.close()
    if fr is None:  # past the end → last frame
        r = FrameReader(path, size=size, start=max(0.0, t - 0.5), duration=0.6)
        last = None
        for f in r:
            last = f
        r.close()
        fr = last
    return None if fr is None else fr.copy()


def grab_frames_at(path, frame_idx: list[int], fps: Fraction, size=None) -> dict[int, np.ndarray]:
    """Several frames by CFR index in one sequential decode (uses select)."""
    want = sorted(set(int(i) for i in frame_idx))
    if not want:
        return {}
    out = {}
    r = FrameReader(path, size=size, fps=fps)
    wi = 0
    n = 0
    for fr in r:
        if n == want[wi]:
            out[n] = fr.copy()
            wi += 1
            if wi >= len(want):
                break
        n += 1
    r.close()
    if len(out) < len(want) and out:
        last = out[max(out)]
        for i in want:
            out.setdefault(i, last)
    return out


def extract_audio(src, out_dir) -> dict:
    """Copy the original audio stream untouched (container chosen by codec) + a 48 kHz WAV for analysis."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    from mm_common import probe
    info = probe(src)
    if not info.get("has_audio"):
        return {"has_audio": False}
    codec = (info.get("audio") or {}).get("codec") or "aac"
    ext = {"aac": "m4a", "mp3": "mp3", "opus": "opus", "vorbis": "ogg", "flac": "flac", "alac": "m4a",
           "pcm_s16le": "wav", "pcm_s24le": "wav"}.get(codec, "mka")
    orig = out_dir / f"original_audio.{ext}"
    run([ffmpeg(), "-v", "error", "-y", "-i", str(src), "-vn", "-map", "0:a:0", "-c:a", "copy", str(orig)])
    wav = out_dir / "analysis_48k.wav"
    run([ffmpeg(), "-v", "error", "-y", "-i", str(src), "-vn", "-map", "0:a:0", "-ac", "2", "-ar", "48000",
         "-c:a", "pcm_s16le", str(wav)])
    return {"has_audio": True, "codec": codec, "original": str(orig), "wav": str(wav),
            "sr": (info.get("audio") or {}).get("sr"), "channels": (info.get("audio") or {}).get("channels")}


def audio_envelope(wav_path, fps: Fraction, n_frames: int) -> np.ndarray:
    """Per-video-frame RMS (dBFS) of an audio file — used to look at text/voice sync."""
    import wave
    with wave.open(str(wav_path), "rb") as wf:
        sr = wf.getframerate()
        ch = wf.getnchannels()
        data = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        data = data.reshape(-1, ch).mean(1)
    spf = sr / float(fps)
    env = np.full(n_frames, -90.0, np.float32)
    for i in range(n_frames):
        a, b = int(i * spf), int((i + 1) * spf)
        seg = data[a:b]
        if len(seg):
            env[i] = 20 * np.log10(max(1e-6, float(np.sqrt(np.mean(seg * seg)))))
    return env
