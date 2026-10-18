#!/usr/bin/env python3
"""Proof run for the APPX family: rebuild features seen in CapCut, Canva and Premiere Pro
with open tools (FFmpeg, NumPy, OpenCV, faster-whisper) on synthetic media, and check a
measurable postcondition for each one. Writes results.json next to this file.

    python smoke.py            # needs ffmpeg/ffprobe on PATH; numpy, opencv; faster-whisper optional
"""
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
FF = shutil.which("ffmpeg")
FP = shutil.which("ffprobe")
RESULTS = []


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          stdin=subprocess.DEVNULL, timeout=600, **kw)


def ff(*args):
    p = run([FF, "-hide_banner", "-y", "-loglevel", "error", *args])
    if p.returncode:
        raise RuntimeError(p.stderr[-400:])
    return p


def probe(path, entries="format=duration:stream=width,height,codec_type,nb_frames"):
    p = run([FP, "-v", "error", "-show_entries", entries, "-of", "json", str(path)])
    return json.loads(p.stdout or "{}")


def duration(path):
    return float(probe(path)["format"]["duration"])


def frame(path, t, w=None):
    import numpy as np
    p = subprocess.run([FF, "-v", "error", "-ss", str(t), "-i", str(path), "-frames:v", "1", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
    s = probe(path)["streams"]
    v = next(x for x in s if x.get("codec_type") == "video")
    return np.frombuffer(p.stdout, dtype=np.uint8).reshape(v["height"], v["width"], 3)


def check(pid, name, fn):
    t0 = time.time()
    try:
        ok, detail = fn()
    except Exception as exc:  # a failed recipe is recorded, never hidden
        ok, detail = False, f"{type(exc).__name__}: {str(exc)[:300]}"
    RESULTS.append({"id": pid, "check": name, "ok": bool(ok), "detail": detail, "seconds": round(time.time() - t0, 2)})
    print(("PASS " if ok else "FAIL ") + pid + "  " + name + "  — " + str(detail)[:140])


def main():
    if not (FF and FP):
        print("ffmpeg/ffprobe missing", file=sys.stderr)
        return 2
    import numpy as np
    import cv2
    W = Path(tempfile.mkdtemp(prefix="appx_"))
    clip = W / "clip.mp4"       # 6 s, 1280x720, moving test pattern + 440 Hz tone
    ff("-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30:duration=6", "-f", "lavfi", "-i", "sine=f=440:d=6",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(clip))

    def speed_curve():   # CapCut "speed curve": 1x → 0.5x → 2x by segments
        out = W / "speed.mp4"
        ff("-i", str(clip), "-filter_complex",
           "[0:v]trim=0:2,setpts=PTS-STARTPTS[a];[0:v]trim=2:4,setpts=2*(PTS-STARTPTS)[b];"
           "[0:v]trim=4:6,setpts=0.5*(PTS-STARTPTS)[c];[a][b][c]concat=n=3:v=1:a=0[v]",
           "-map", "[v]", "-c:v", "libx264", str(out))
        d = duration(out)
        return abs(d - 7.0) < 0.15, f"2s@1x + 2s@0.5x + 2s@2x → {d:.2f}s (expected 7.00)"
    check("APPX-01", "speed curve by segments", speed_curve)

    def chroma():        # CapCut/Premiere chroma key
        green = W / "green.mp4"
        ff("-f", "lavfi", "-i", "color=c=0x00FF00:s=640x360:d=2", "-f", "lavfi", "-i", "color=c=red:s=200x200:d=2",
           "-filter_complex", "[0][1]overlay=220:80", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(green))
        out = W / "keyed.mp4"
        ff("-i", str(clip), "-i", str(green), "-filter_complex",
           "[1:v]chromakey=0x00FF00:0.15:0.05[k];[0:v]scale=640:360[bg];[bg][k]overlay=shortest=1",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out))
        f = frame(out, 1.0).astype(int)
        corner_green = (f[10:40, 10:40, 1] > 200) & (f[10:40, 10:40, 0] < 60)
        centre = f[150:200, 290:340]
        red_kept = centre[..., 0].mean() > 150 and centre[..., 1].mean() < 90
        return (not corner_green.mean() > 0.5) and red_kept, f"green left in corner {corner_green.mean():.2f}, subject red kept {red_kept}"
    check("APPX-02", "chroma key over new background", chroma)

    def reframe():       # Premiere Auto Reframe / CapCut 9:16: follow the moving subject
        src = W / "subject.mp4"
        ff("-f", "lavfi", "-i", "color=c=black:s=1280x720:d=4:r=25", "-f", "lavfi", "-i", "color=c=white:s=120x120:d=4:r=25",
           "-filter_complex", "[0][1]overlay=x='100+t*220':y=300", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(src))
        cap = cv2.VideoCapture(str(src)); xs = []
        while True:
            ok, im = cap.read()
            if not ok:
                break
            m = cv2.moments(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
            xs.append(m["m10"] / m["m00"] if m["m00"] else 640)
        cap.release()
        smooth = np.convolve(xs, np.ones(9) / 9, mode="same")
        cw = 404  # 720 * 9 / 16 = 405, rounded to even for yuv420p
        lefts = np.clip(smooth - cw / 2, 0, 1280 - cw).astype(int)
        # a per-frame crop expression grows past FFmpeg's parser limits on long clips: crop in OpenCV, pipe to x264
        out = W / "reframed.mp4"
        enc = subprocess.Popen([FF, "-hide_banner", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
                                "-s", f"{cw}x720", "-r", "25", "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                               stdin=subprocess.PIPE)
        cap = cv2.VideoCapture(str(src)); n = 0
        while True:
            ok, im = cap.read()
            if not ok:
                break
            enc.stdin.write(np.ascontiguousarray(im[:, lefts[min(n, len(lefts) - 1)]:][:, :cw]).tobytes()); n += 1
        cap.release(); enc.stdin.close(); enc.wait(timeout=120)
        f = frame(out, 3.0)
        inside = f[:, :, 0].max() > 200
        s = probe(out)["streams"][0]
        return inside and s["width"] == cw, f"{s['width']}x{s['height']} crop keeps the subject at t=3s: {inside}"
    check("APPX-03", "auto reframe to 9:16 following the subject", reframe)

    def scenes():        # Premiere Scene Edit Detection
        cuts = W / "cuts.mp4"
        ff("-f", "lavfi", "-i", "color=c=red:s=320x180:d=1.5:r=25", "-f", "lavfi", "-i", "color=c=blue:s=320x180:d=1.5:r=25",
           "-f", "lavfi", "-i", "testsrc=s=320x180:d=1.5:r=25", "-filter_complex", "[0][1][2]concat=n=3:v=1",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cuts))
        p = run([FF, "-hide_banner", "-i", str(cuts), "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-"])
        ts = [round(float(x), 2) for x in re.findall(r"pts_time:([\d.]+)", p.stderr)]
        return len(ts) == 2 and abs(ts[0] - 1.5) < 0.1 and abs(ts[1] - 3.0) < 0.1, f"cuts at {ts} (expected [1.5, 3.0])"
    check("APPX-04", "scene edit detection", scenes)

    def loud():          # CapCut/Premiere loudness: -14 LUFS for social
        quiet = W / "quiet.wav"
        ff("-f", "lavfi", "-i", "sine=f=330:d=8", "-af", "volume=-26dB", str(quiet))
        out = W / "loud.wav"
        ff("-i", str(quiet), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", str(out))
        p = run([FF, "-hide_banner", "-i", str(out), "-af", "ebur128", "-f", "null", "-"])
        m = re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr)
        i = float(m[-1]) if m else 0
        return abs(i + 14) < 1.0, f"integrated loudness {i} LUFS (target -14 ±1)"
    check("APPX-05", "loudness normalisation for social", loud)

    def lut():           # CapCut filters / Premiere Lumetri look via a .cube LUT
        cube = W / "warm.cube"
        n = 17
        lines = ["LUT_3D_SIZE %d" % n]
        for b in range(n):
            for g in range(n):
                for r in range(n):
                    R, G, B = r / (n - 1), g / (n - 1), b / (n - 1)
                    lines.append(f"{min(1, R * 1.12):.5f} {G:.5f} {B * 0.85:.5f}")
        cube.write_text("\n".join(lines))
        grey = W / "grey.mp4"
        ff("-f", "lavfi", "-i", "color=c=0x808080:s=320x180:d=1", "-c:v", "libx264", "-pix_fmt", "yuv444p", str(grey))
        out = W / "graded.mp4"
        ff("-i", str(grey), "-vf", f"lut3d=file='{cube.as_posix().replace(':', chr(92) + ':')}'", "-c:v", "libx264", "-pix_fmt", "yuv444p", str(out))
        f = frame(out, 0.5).reshape(-1, 3).mean(0)
        return f[0] > f[1] > f[2], f"mean RGB after warm LUT {f.round(1).tolist()} (R>G>B)"
    check("APPX-06", "colour look from a .cube LUT", lut)

    def silence():       # CapCut "remove pauses" / Premiere text-based cut
        talk = W / "talk.wav"
        ff("-f", "lavfi", "-i", "sine=f=300:d=1", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono:d=1.5",
           "-f", "lavfi", "-i", "sine=f=500:d=1", "-filter_complex", "[0][1][2]concat=n=3:v=0:a=1", str(talk))
        p = run([FF, "-hide_banner", "-i", str(talk), "-af", "silencedetect=n=-40dB:d=0.5", "-f", "null", "-"])
        st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", p.stderr)]
        en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", p.stderr)]
        out = W / "tight.wav"
        ff("-i", str(talk), "-af", "silenceremove=stop_periods=-1:stop_duration=0.5:stop_threshold=-40dB", str(out))
        d = duration(out)
        # silenceremove keeps stop_duration (0.5 s) of each pause as a natural breath
        return st and en and abs(st[0] - 1.0) < 0.05 and abs(en[0] - 2.5) < 0.05 and abs(d - 2.5) < 0.1, \
            f"pause found {st[0]:.2f}→{en[0]:.2f}s; 3.50s tightened to {d:.2f}s (1.5 s pause → 0.5 s breath)"
    check("APPX-07", "silence / pause removal", silence)

    def beats():         # CapCut auto beat markers
        import wave
        sr, bpm = 22050, 120
        x = np.zeros(sr * 4, dtype=np.float32)
        for k in range(8):
            i = int((0.1 + k * 0.5) * sr)
            x[i:i + 300] += np.hanning(300) * 0.9
        x += np.random.default_rng(7).normal(0, 0.01, x.size).astype(np.float32)
        path = W / "clicks.wav"
        with wave.open(str(path), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
        hop = 256
        frames = x[: x.size // hop * hop].reshape(-1, hop)
        energy = (frames ** 2).sum(1)
        flux = np.maximum(0, np.diff(energy, prepend=0))
        thr = flux.mean() + 2 * flux.std()
        peaks = [i for i in range(1, flux.size - 1) if flux[i] > thr and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]]
        times, last = [], -1
        for i in peaks:
            t = i * hop / sr
            if t - last > 0.2:
                times.append(round(t, 3)); last = t
        tempo = 60 / np.median(np.diff(times)) if len(times) > 1 else 0
        return len(times) == 8 and abs(tempo - bpm) < 2, f"{len(times)} beats, tempo {tempo:.1f} BPM (expected 8, 120)"
    check("APPX-08", "beat markers from audio", beats)

    def bubble():        # Canva recording studio "talking head" camera bubble over a screen capture
        cam = W / "cam.mp4"
        ff("-f", "lavfi", "-i", "color=c=0xFF8800:s=360x360:d=2", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cam))
        out = W / "bubble.mp4"
        ff("-i", str(clip), "-i", str(cam), "-filter_complex",
           "[1:v]format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lte(hypot(X-180,Y-180),178),255,0)'[c];"
           "[0:v][c]overlay=x=W-w-40:y=H-h-40:shortest=1", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out))
        f = frame(out, 1.0).astype(int)
        cx, cy = 1280 - 40 - 180, 720 - 40 - 180
        centre_orange = f[cy, cx, 0] > 200 and 100 < f[cy, cx, 1] < 170
        corner = f[720 - 40 - 355, 1280 - 40 - 355]
        corner_not_orange = not (corner[0] > 200 and 100 < corner[1] < 170 and corner[2] < 60)
        return centre_orange and corner_not_orange, f"bubble centre orange {centre_orange}, square corner shows the screen {corner_not_orange}"
    check("APPX-09", "round camera bubble over a screen recording", bubble)

    def kenburns():      # keyframed zoom (Ken Burns / punch-in)
        dot = W / "dot.png"
        im = np.zeros((720, 1280, 3), np.uint8); cv2.circle(im, (640, 360), 60, (255, 255, 255), -1); cv2.imwrite(str(dot), im)
        src = W / "dot.mp4"
        ff("-loop", "1", "-i", str(dot), "-t", "5", "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(src))
        out = W / "zoom.mp4"
        ff("-i", str(src), "-vf", "zoompan=z='min(1+0.004*on,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1280x720:fps=30",
           "-t", "4", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out))
        a, b = ((frame(out, t)[..., 0] > 128).sum() for t in (0.0, 3.9))
        return b / a > 1.9, f"subject area {a} → {b} px (×{b / a:.2f}; zoom 1.5 → ×2.25)"
    check("APPX-10", "keyframed zoom / punch-in", kenburns)

    def duck():          # CapCut/Premiere auto ducking: music dips under the voice
        voice = W / "voice.wav"; music = W / "music.wav"
        ff("-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono:d=2", "-f", "lavfi", "-i", "sine=f=800:d=2:sample_rate=44100",
           "-filter_complex", "[0][1]concat=n=2:v=0:a=1", str(voice))
        ff("-f", "lavfi", "-i", "sine=f=200:d=4:sample_rate=44100", "-af", "volume=-6dB", str(music))
        out = W / "ducked.wav"
        ff("-i", str(music), "-i", str(voice), "-filter_complex",
           "[1]asplit[sc][v];[0][sc]sidechaincompress=threshold=0.02:ratio=12:attack=20:release=300[m];[m][v]amix=inputs=2:normalize=0",
           str(out))
        def rms(path, a, b):
            p = run([FF, "-hide_banner", "-ss", str(a), "-t", str(b - a), "-i", str(path), "-af", "lowpass=f=300,astats=metadata=0",
                     "-f", "null", "-"])
            m = re.findall(r"RMS level dB: (-?[\d.]+)", p.stderr)
            return float(m[-1]) if m else 0.0
        before, during = rms(out, 0.5, 1.8), rms(out, 2.5, 3.8)
        return during < before - 6, f"music bed {before:.1f} dB → {during:.1f} dB while the voice speaks"
    check("APPX-11", "auto ducking of music under voice", duck)

    def denoise():       # Premiere "Enhance Speech" / CapCut "reduce noise" (classic DSP, not their models)
        noisy = W / "noisy.wav"
        ff("-f", "lavfi", "-i", "sine=f=400:d=4", "-f", "lavfi", "-i", "anoisesrc=d=4:c=white:a=0.08",
           "-filter_complex", "[0][1]amix=inputs=2:normalize=0", str(noisy))
        out = W / "clean.wav"
        ff("-i", str(noisy), "-af", "afftdn=nr=20:nf=-30,highpass=f=80", str(out))
        def hf(path):
            p = run([FF, "-hide_banner", "-i", str(path), "-af", "highpass=f=3000,astats=metadata=0", "-f", "null", "-"])
            m = re.findall(r"RMS level dB: (-?[\d.]+)", p.stderr)
            return float(m[-1]) if m else 0.0
        a, b = hf(noisy), hf(out)
        return b < a - 6, f"noise above 3 kHz {a:.1f} dB → {b:.1f} dB"
    check("APPX-12", "speech noise reduction", denoise)

    def captions():      # CapCut auto captions / Premiere Speech to Text
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            return False, "faster-whisper not installed"
        tts = None
        if platform.system() == "Windows":
            wav = W / "say.wav"
            ps = ("Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer;"
                  f"$s.SetOutputToWaveFile('{wav}'); $s.Speak('Hello world, this is a caption test.'); $s.Dispose()")
            if run(["powershell", "-NoProfile", "-Command", ps]).returncode == 0 and wav.exists():
                tts = wav
        elif shutil.which("espeak-ng") or shutil.which("espeak"):
            wav = W / "say.wav"
            run([shutil.which("espeak-ng") or shutil.which("espeak"), "-w", str(wav), "Hello world, this is a caption test."])
            tts = wav if wav.exists() else None
        if not tts:
            return False, "no local TTS to make a test voice"
        model = WhisperModel("base.en", device="cpu", compute_type="int8")
        segs, _ = model.transcribe(str(tts), word_timestamps=True)
        words = [w for s in segs for w in (s.words or [])]
        srt = W / "captions.srt"
        def ts(t):
            return f"{int(t // 3600):02}:{int(t % 3600 // 60):02}:{int(t % 60):02},{int(t * 1000 % 1000):03}"
        srt.write_text("".join(f"{i + 1}\n{ts(w.start)} --> {ts(w.end)}\n{w.word.strip()}\n\n" for i, w in enumerate(words)), encoding="utf-8")
        text = " ".join(w.word.strip() for w in words).lower()
        mono = all(words[i].start <= words[i + 1].start for i in range(len(words) - 1))
        return "caption" in text and "world" in text and mono, f"{len(words)} timed words: {text[:60]!r}; monotonic {mono}"
    check("APPX-13", "word-timed auto captions (SRT)", captions)

    def bgremove():      # CapCut "remove background" on a still (classic GrabCut, not their model)
        img = np.full((240, 320, 3), (40, 160, 40), np.uint8)
        cv2.circle(img, (160, 120), 60, (30, 30, 220), -1)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        mask = np.zeros(img.shape[:2], np.uint8)
        bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
        cv2.grabCut(img, mask, (80, 40, 160, 160), bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)
        fg = np.where((mask == 1) | (mask == 3), 1, 0).astype(np.uint8)
        truth = np.zeros_like(fg); cv2.circle(truth, (160, 120), 60, 1, -1)
        iou = (fg & truth).sum() / max(1, (fg | truth).sum())
        rgba = np.dstack([img, fg * 255]); cv2.imwrite(str(W / "cutout.png"), rgba)
        return iou > 0.9, f"IoU with the true subject {iou:.3f}"
    check("APPX-14", "background removal on a still", bgremove)

    def edl():           # Premiere/CapCut project interchange: CMX3600 EDL that ffmpeg can conform
        events = [("clip", 1.0, 2.5), ("clip", 4.0, 5.0)]
        def tc(t, fps=30):
            f = int(round(t * fps)); return f"{f // (3600 * fps):02}:{f // (60 * fps) % 60:02}:{f // fps % 60:02}:{f % fps:02}"
        rec, lines = 0.0, ["TITLE: KOSIF APPX", "FCM: NON-DROP FRAME", ""]
        for i, (_, a, b) in enumerate(events, 1):
            lines.append(f"{i:03}  AX       V     C        {tc(a)} {tc(b)} {tc(rec)} {tc(rec + b - a)}")
            lines.append("* FROM CLIP NAME: clip.mp4"); rec += b - a
        (W / "cut.edl").write_text("\n".join(lines) + "\n")
        parsed = re.findall(r"^\d{3}\s+AX\s+V\s+C\s+(\S+) (\S+) (\S+) (\S+)$", (W / "cut.edl").read_text(), re.M)
        def sec(s):
            h, m, x, f = map(int, s.split(":")); return h * 3600 + m * 60 + x + f / 30
        parts = []
        for k, (a, b, _, _) in enumerate(parsed):
            parts.append(f"[0:v]trim={sec(a)}:{sec(b)},setpts=PTS-STARTPTS[v{k}]")
        fc = ";".join(parts) + ";" + "".join(f"[v{k}]" for k in range(len(parts))) + f"concat=n={len(parts)}:v=1[v]"
        out = W / "conformed.mp4"
        ff("-i", str(clip), "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", str(out))
        d = duration(out)
        return len(parsed) == 2 and abs(d - 2.5) < 0.1, f"EDL with {len(parsed)} events conformed to {d:.2f}s (expected 2.50)"
    check("APPX-15", "EDL export and conform", edl)

    def freeze_reverse():   # CapCut freeze frame + reverse
        out = W / "rev.mp4"
        ff("-i", str(clip), "-vf", "trim=0:2,reverse,tpad=stop_mode=clone:stop_duration=1", "-an", "-c:v", "libx264", str(out))
        d = duration(out)
        first, src_end = frame(out, 0.0).astype(int), frame(clip, 1.96).astype(int)
        diff = np.abs(first - src_end).mean()
        return abs(d - 3.0) < 0.1 and diff < 20, f"2 s reversed + 1 s hold = {d:.2f}s; first frame matches source end (mean diff {diff:.1f})"
    check("APPX-16", "reverse and freeze frame", freeze_reverse)

    def thumbs():        # Canva/CapCut cover pick: sharpest, most colourful frame as thumbnail
        best, score = None, -1
        for t in np.linspace(0.2, 5.8, 8):
            f = frame(clip, float(t))
            g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
            s = cv2.Laplacian(g, cv2.CV_64F).var() + f.std(axis=2).mean()
            if s > score:
                best, score = float(t), s
        cv2.imwrite(str(W / "cover.jpg"), cv2.cvtColor(frame(clip, best), cv2.COLOR_RGB2BGR))
        return (W / "cover.jpg").stat().st_size > 10000, f"picked t={best:.2f}s (score {score:.0f}) as cover"
    check("APPX-17", "automatic cover / thumbnail pick", thumbs)

    out = {"date": time.strftime("%Y-%m-%d"), "host": f"{platform.system()} {platform.machine()}",
           "ffmpeg": run([FF, "-version"]).stdout.split("\n")[0][:80], "python": platform.python_version(),
           "passed": sum(r["ok"] for r in RESULTS), "total": len(RESULTS), "results": RESULTS}
    (HERE / "results.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    shutil.rmtree(W, ignore_errors=True)
    print(f"{out['passed']}/{out['total']} passed")
    return 0 if out["passed"] == out["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
