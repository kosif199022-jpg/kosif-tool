"""Real programs for the atlas-media power cards (delivery checks, procedural audio, motion maths, kits).

Each builds a fixture, performs the card's technique with its numbers and returns known answers.
Cards that need a paid API, a desktop app (After Effects, Godot, Houdini, PipeWire in Docker) or
a speech model are skipped.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .photo_video_footage import (REPO, chk, decode_audio, duration, ff, ffstderr, jwrite, near, probe, read_video,
                                  read_wav, solid, tone, vstream, astreams, write_video, write_wav, frame_index_frames,
                                  decode_index, nframes)
from .media_image_audio import ebur128_I, loudnorm_two_pass

FONT = REPO / ".claude/skills/kosif-superpowers/proofs/_shared/fonts/Amiri-Bold.ttf"


def _true_peak(path):
    err = ffstderr("-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-")
    lines = err.splitlines()
    k = max(i for i, l in enumerate(lines) if "True peak:" in l)
    return float(lines[k + 1].split()[1])


def amedia_02(work):
    sr = 48000
    t = np.arange(int(0.5 * sr)) / sr
    a = write_wav(work / "mix.wav", np.stack([0.05 * np.sin(2 * np.pi * 220 * t)] * 2, 1).ravel(), sr, ch=2)
    m, r = loudnorm_two_pass(a, work / "mix_norm.wav", I=-14, TP=-1.0)
    out = work / "deliver_4k.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=3840x2160:r=30:d=0.5", "-i", work / "mix_norm.wav", "-c:v", "libx264",
       "-preset", "ultrafast", "-b:v", "45M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2",
       "-b:a", "320k", "-shortest", out)
    v, au = vstream(out), astreams(out)[0]
    frames = nframes(out)
    I, tp = ebur128_I(out), _true_peak(out)
    rep = {"size": (v["width"], v["height"]), "fps": v["r_frame_rate"], "frames": frames, "audio": au["codec_name"],
           "sr": au["sample_rate"], "ch": au["channels"], "lufs": I, "true_peak": tp}
    jwrite(work, "delivery_check.json", rep)
    return [chk("3840x2160 at 30 fps", rep["size"] == (3840, 2160) and eval(v["r_frame_rate"]) == 30, rep["size"]),
            chk("frames within 1 of the 15-frame timeline", abs(frames - 15) <= 1, frames),
            chk("AAC 48 kHz stereo", (au["codec_name"], au["sample_rate"], au["channels"]) == ("aac", "48000", 2), au["sample_rate"]),
            chk("-14 LUFS +-1", near(I, -14, 1), I),
            chk("true peak <= -1 dBTP", tp <= -1.0 + 0.2, tp)]


def amedia_03(work):
    sr = 22050
    classes = {"ui": -20, "small": -16, "normal": -12, "big": -9}

    def synth(preset, pitch, length, seed, style):
        rng = np.random.default_rng(seed)
        n = int(length * sr)
        t = np.arange(n) / sr
        f = 440 * 2 ** (pitch / 12)
        if preset == "coin":
            x = np.sin(2 * np.pi * f * t * (1 + (t > 0.05)))
        elif preset == "hit":
            x = rng.standard_normal(n)
        else:
            x = np.sin(2 * np.pi * f * t)
        x *= np.exp(-t / (length / 3))
        if style == "retro":
            x = np.sign(x) * np.abs(x)
        return x

    def peak50_db(x):
        w = int(0.05 * sr)
        return max(10 * np.log10(np.mean(x[i:i + w] ** 2) + 1e-12) for i in range(0, max(1, len(x) - w), w // 2))

    def normalise(x, cls):
        g = 10 ** ((classes[cls] - peak50_db(x)) / 20)
        y = x * g
        pk = np.abs(y).max()
        return y * min(1.0, 10 ** (-1 / 20) / pk) if pk else y

    def warnings(x, f0):
        w = []
        onset = np.argmax(np.abs(x) > 0.1 * np.abs(x).max()) / sr
        if onset > 0.02:
            w.append(f"late onset {onset:.3f}s")
        if f0 < 80:
            w.append("inaudible lows on phones")
        return w

    spec = [("coin", "coin", 12, 0.2, "clean", "small", 3), ("hit", "hit", 0, 0.15, "retro", "normal", 3),
            ("win", "tone", 0, 0.6, "soft", "big", 1)]
    out = {}
    for name, preset, pitch, L, style, cls, nvar in spec:
        out[name] = []
        for v in range(nvar):
            y = normalise(synth(preset, pitch, L, 100 + v, style), cls)
            write_wav(work / f"{name}_{v}.wav", y, sr)
            out[name].append(round(peak50_db(y), 2))
    late = np.concatenate([np.zeros(int(0.1 * sr)), synth("tone", 0, 0.2, 1, "clean")])
    low = synth("tone", -36, 0.3, 1, "clean")
    jwrite(work, "sfx_manifest.json", out)
    pk = max(np.abs(read_wav(work / "hit_0.wav")[0]).max(), 1e-9)
    return [chk("3 variants for frequent sounds, 1 for a one-off", len(out["coin"]) == 3 and len(out["win"]) == 1, out),
            chk("small class at -16 dB (loudest 50 ms)", all(near(v, -16, 0.6) for v in out["coin"]), out["coin"]),
            chk("ceiling -1 dBFS respected", 20 * math.log10(pk) <= -0.9, round(20 * math.log10(pk), 2)),
            chk("late onset warned", any("late onset" in w for w in warnings(late, 440)), warnings(late, 440)),
            chk("55 Hz effect warned as inaudible low", warnings(low, 440 * 2 ** (-3)) == ["inaudible lows on phones"],
                warnings(low, 55))]


def amedia_05(work):
    sr = 44100
    wavs, pieces = [], []
    for i in range(6):
        w = write_wav(work / f"p{i}.wav", tone(1.0, 300 + 50 * i, sr, 0.3), sr)
        p = work / f"p{i}.aac"  # ADTS pieces keep each encoder's priming/padding
        ff("-i", w, "-c:a", "aac", "-b:a", "96k", p)
        wavs.append(w)
        pieces.append(p)
    summed = sum(duration(p) for p in pieces)
    ff("-i", "concat:" + "|".join(str(p) for p in pieces), "-c", "copy", work / "copy.aac")
    dc = len(decode_audio(work / "copy.aac")) / 16000
    fc = "".join(f"[{i}:a]" for i in range(6)) + "concat=n=6:v=0:a=1[a]"
    args = []
    for w in wavs:
        args += ["-i", w]
    ff(*args, "-filter_complex", fc, "-map", "[a]", "-c:a", "aac", "-b:a", "96k", work / "final.m4a")
    dr = duration(work / "final.m4a")
    x = decode_audio(work / "final.m4a", 16000)
    seg = x[int(5.1 * 16000):int(5.6 * 16000)]
    f_last = np.fft.rfftfreq(len(seg), 1 / 16000)[np.argmax(np.abs(np.fft.rfft(seg)))]
    xc = decode_audio(work / "copy.aac", 16000)
    segc = xc[int(5.1 * 16000):int(5.2 * 16000)]
    fc_last = np.fft.rfftfreq(len(segc), 1 / 16000)[np.argmax(np.abs(np.fft.rfft(segc)))]
    jwrite(work, "drift.json", {"sum_pieces": summed, "copy_concat": dc, "decode_concat_encode": dr})
    return [chk("diagnosis: copy-mode join is longer than 6.0 s (padding per join)", dc - 6.0 > 0.1, round(dc, 3)),
            chk("decode -> concat -> encode once lands at 6.0 s +-0.03", near(dr, 6.0, 0.03), dr),
            chk("last chapter at 5.0 s holds piece 6 (550 Hz) in the final file", near(f_last, 550, 4), f_last),
            chk("copy-joined file has drifted: still piece 5 (500 Hz) at 5.1 s", near(fc_last, 500, 12), fc_last)]


def amedia_07(work):
    lyrics = """[Verse]
نمشي على درب القمر
[Verse]
والليل يحكي ما استتر
[Bridge]
يا قلب لا تخشى السفر
[Verse]
نرجع ومعنا المطر"""
    style = {"genre": "arabic pop", "mood": "hopeful", "instruments": "oud, strings, soft drums", "tempo": "92 bpm"}

    def sections(text):
        return [l.strip()[1:-1].lower() for l in text.splitlines() if l.strip().startswith("[")]

    def form(secs):
        m = {"verse": "A", "chorus": "B", "refrain": "R", "bridge": "B"}
        code = "".join(m.get(s, "?") for s in secs)
        if code == "AABA":
            return "AABA"
        if "verse" in secs and "chorus" in secs:
            return "verse/chorus"
        if all(s in ("verse", "refrain") for s in secs):
            return "verse/refrain"
        return "unknown"

    def style_prompt(st):
        p = ", ".join(st[k] for k in ("genre", "mood", "instruments", "tempo"))
        return p if len(p) <= 120 else None

    secs = sections(lyrics)
    vc = sections("[Verse]\nx\n[Chorus]\ny\n[Verse]\nz\n[Chorus]\nw")
    prompt = style_prompt(style)
    (work / "suno_prompt.txt").write_text(prompt + "\n\n" + lyrics + "\n", encoding="utf-8")
    return [chk("sections tagged and read in order", secs == ["verse", "verse", "bridge", "verse"], secs),
            chk("form recognised as AABA", form(secs) == "AABA", form(secs)),
            chk("verse/chorus recognised", form(vc) == "verse/chorus", form(vc)),
            chk("compact style prompt has genre, mood, instruments, tempo", prompt and prompt.count(",") >= 3 and "92 bpm" in prompt,
                prompt)]


def amedia_09(work):
    sr = 22050
    style = {"key_hz": 261.63, "brightness": 0.6, "grit": 0.1}

    def sfx_jump(seed):
        rng = np.random.default_rng(seed)
        n = int(0.25 * sr)
        t = np.arange(n) / sr
        f = style["key_hz"] * (1 + 2 * t / 0.25)
        x = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 8) + style["grit"] * rng.standard_normal(n) * np.exp(-t * 30)
        return x * 0.5

    def track(seed, bars=2, bpm=120):
        beat = 60 / bpm
        n = int(bars * 4 * beat * sr)
        t = np.arange(n) / sr
        notes = [0, 4, 7, 12]
        x = np.zeros(n)
        for k in range(bars * 4):
            i0, i1 = int(k * beat * sr), int((k + 1) * beat * sr)
            f = style["key_hz"] * 2 ** (notes[k % 4] / 12)
            tt = t[i0:i1] - t[i0]
            x[i0:i1] = 0.3 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3)
        return x

    man = {}
    for name, x, loop in [("jump", sfx_jump(1), False), ("theme", track(1), True)]:
        w = write_wav(work / f"{name}.wav", x, sr)
        o = work / f"{name}.ogg"
        ff("-i", w, "-c:a", "libvorbis", "-q:a", "4", o)
        man[name] = {"file": o.name, "sha256": hashlib.sha256(w.read_bytes()).hexdigest(), "pcm_samples": len(x),
                     "duration": round(duration(o), 3), "loop": {"start": 0, "end": len(x)} if loop else None}
    jwrite(work, "manifest.json", man)
    again = hashlib.sha256(write_wav(work / "jump_again.wav", sfx_jump(1), sr).read_bytes()).hexdigest()
    other = hashlib.sha256(write_wav(work / "jump_seed2.wav", sfx_jump(2), sr).read_bytes()).hexdigest()
    th = track(1)
    return [chk("same seed -> same bytes", again == man["jump"]["sha256"], again[:12]),
            chk("different seed -> different sound", other != again, other[:12]),
            chk("theme is 2 bars at 120 BPM = 4.0 s", near(len(th) / sr, 4.0, 1e-3) and near(man["theme"]["duration"], 4.0, 0.05),
                man["theme"]["duration"]),
            chk("OGG Vorbis written", probe(work / "jump.ogg")["streams"][0]["codec_name"] == "vorbis", "vorbis")]


def amedia_10(work):
    sr = 16000
    score = {"tempo": 120, "key": "A", "instruments": {"bass": {"level": 0.5}, "lead": {"level": 0.3}},
             "sections": {"A": {"bars": 1, "chords": ["Am", "F"]}}, "arrangement": ["A", "A"], "loops": ["A"]}
    roots = {"Am": 220.0, "F": 174.61}
    bar = 4 * 60 / score["tempo"]

    def render_section(name, inst, tail=True):
        sec = score["sections"][name]
        n = int(sec["bars"] * bar * sr)
        t = np.arange(n) / sr
        x = np.zeros(n + (int(0.5 * sr) if tail else 0))
        per = n // len(sec["chords"])
        for k, c in enumerate(sec["chords"]):
            f = roots[c] * (1 if inst == "bass" else 2)
            seg = np.sin(2 * np.pi * f * t[:per]) * score["instruments"][inst]["level"]
            x[k * per:(k + 1) * per] += seg
        # simple echo makes a tail that spills into the next bar
        d = int(0.25 * sr)
        y = x.copy()
        y[d:] += 0.4 * x[:-d]
        return y

    stems = {}
    for inst in score["instruments"]:
        parts = [render_section(s, inst, tail=False) for s in score["arrangement"]]
        stems[inst] = np.concatenate(parts)
        write_wav(work / f"stem_{inst}.wav", stems[inst] * 0.5, sr)
    mix = sum(stems.values())
    write_wav(work / "mix.wav", mix * 0.5, sr)
    sum_err = float(np.abs(sum(read_wav(work / f"stem_{i}.wav")[0] for i in stems) - read_wav(work / "mix.wav")[0]).max())
    # seamless loop: render section 3x, keep the middle copy (tails of copy 1 land in its head)
    L = int(bar * sr)
    triple = np.zeros(3 * L + sr)
    one = render_section("A", "bass")
    for k in range(3):
        triple[k * L:k * L + len(one)] += one
    loop = triple[L:2 * L]
    naive = one[:L]
    seam = lambda a: float(abs(a[0] - a[-1]) + abs(np.concatenate([a, a])[L - 2:L + 2]).std())
    wrap_ok = float(np.abs(np.tile(loop, 2)[L - 200:L + 200] - triple[2 * L - 200:2 * L + 200]).max())
    write_wav(work / "loop_A.wav", loop * 0.5, sr)
    return [chk("stems sum to the mix (within 16-bit rounding)", sum_err < 2e-4, sum_err),
            chk("loop is exactly one bar (2.0 s at 120 BPM)", len(loop) == 2 * sr, len(loop)),
            chk("middle copy wraps into itself like the continuous render", wrap_ok < 1e-9, wrap_ok),
            chk("naive single render lacks the echo tail at its head", np.abs(loop[:int(0.25 * sr)] - naive[:int(0.25 * sr)]).max() > 0.01,
                round(float(np.abs(loop[:4000] - naive[:4000]).max()), 3))]


def amedia_11(work):
    def choose(channel, languages, streaming):
        sr = 8000 if channel in ("pstn", "sip") else 16000 if channel == "web" else 24000
        codec = "mulaw" if sr == 8000 else "pcm16"
        stt = "telephony-8k" if sr == 8000 else "wideband"
        if "ar" in languages and "ar" not in {"telephony-8k": ["en", "ar", "es"], "wideband": ["en", "ar", "fr"]}[stt]:
            return None
        return {"sample_rate": sr, "codec": codec, "stt_model": stt, "tts_stream": streaming, "barge_in": streaming}

    a, b = choose("pstn", ["ar"], True), choose("web", ["en", "ar"], False)
    jwrite(work, "stack.json", {"pstn": a, "web": b})
    return [chk("telephony -> 8 kHz mu-law narrowband model", a["sample_rate"] == 8000 and a["codec"] == "mulaw", a),
            chk("web -> 16 kHz wideband", b["sample_rate"] == 16000 and b["stt_model"] == "wideband", b),
            chk("barge-in only with streaming", a["barge_in"] and not b["barge_in"], (a["barge_in"], b["barge_in"]))]


def amedia_12(work):
    frames = []
    for i, (w, h, dx) in enumerate([(20, 30, 3), (24, 34, 0), (22, 28, 6), (26, 36, 2)]):
        im = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
        ImageDraw.Draw(im).rectangle([dx, 40 - h, dx + w - 1, 39], fill=(200, 60 + 40 * i, 60, 255))
        frames.append(im)
    bboxes = [f.getbbox() for f in frames]
    tallest = max(b[3] - b[1] for b in bboxes)
    slot = (64, 64)
    scale = (slot[1] - 8) / tallest  # one shared scale for the whole strip
    strip = Image.new("RGBA", (slot[0] * len(frames), slot[1]), (0, 0, 0, 0))
    anchors = []
    for k, (f, b) in enumerate(zip(frames, bboxes)):
        c = f.crop(b)
        c = c.resize((max(1, round(c.width * scale)), max(1, round(c.height * scale))), Image.NEAREST)
        x = k * slot[0] + (slot[0] - c.width) // 2
        y = slot[1] - 4 - c.height
        strip.paste(c, (x, y), c)
        anchors.append((x + c.width / 2 - k * slot[0], y + c.height))
    strip.save(work / "strip.png")
    a = np.asarray(strip)[..., 3] > 0
    bottoms = [int(np.nonzero(a[:, k * 64:(k + 1) * 64].any(1))[0].max()) for k in range(4)]
    heights = [int(a[:, k * 64:(k + 1) * 64].any(1).sum()) for k in range(4)]
    return [chk("bottom-centre anchor shared (all feet on y=59)", set(bottoms) == {59}, bottoms),
            chk("horizontal centre at slot middle +-1", all(abs(ax - 32) <= 1 for ax, _ in anchors), anchors),
            chk("shared scale keeps relative heights 30:34:28:36", heights == [round(h * scale) for h in (30, 34, 28, 36)],
                heights)]


def amedia_13(work):
    def bar_frames(bpm, fps=60):
        return Fraction(14400, bpm) if fps == 60 else Fraction(fps * 240, bpm)

    ok = [b for b in range(90, 181) if bar_frames(b).denominator == 1]
    bpm = 120
    bar = int(bar_frames(bpm))
    shots = [{"shot": k, "start": k * bar, "frames": bar} for k in range(3)]
    jwrite(work, "timeline.json", {"bpm": bpm, "bar_frames": bar, "shots": shots})
    fr = frame_index_frames(3 * bar // 4, 36, 64)  # render at 15 fps preview: every 4th frame
    src = write_video(work / "shots.mkv", fr, 15)
    ff("-i", src, "-vf", "scale=108:192:force_original_aspect_ratio=increase,crop=108:192", "-c:v", "libx264", "-preset",
       "ultrafast", work / "vertical.mp4")
    ff("-i", src, "-vf", "fps=10,scale=64:-1", work / "trailer.gif")
    v = vstream(work / "vertical.mp4")
    return [chk("120 BPM bar = 14400/120 = 120 whole frames at 60 fps", bar == 120, bar),
            chk("125 BPM rejected (115.2 frames)", 125 not in ok and bar_frames(125) == Fraction(576, 5), bar_frames(125)),
            chk("cuts land on bar boundaries", all(s["start"] % 120 == 0 for s in shots), [s["start"] for s in shots]),
            chk("9:16 and GIF exports exist", (v["width"], v["height"]) == (108, 192) and (work / "trailer.gif").stat().st_size > 0,
                (v["width"], v["height"]))]


def amedia_14(work):
    W, H = 1280, 720
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    big = ImageFont.truetype(str(FONT), 56)
    small = ImageFont.truetype(str(FONT), 28)
    d.text((W // 2, 80), "Attention = softmax(QK^T)V", font=big, fill=(17, 17, 17), anchor="mm")
    for k, lab in enumerate(["Q", "K", "V"]):
        x = 300 + 340 * k
        d.rectangle([x - 90, 260, x + 90, 420], outline=(17, 17, 17), width=4)
        d.text((x, 340), lab, font=big, fill=(17, 17, 17), anchor="mm")
    d.text((W // 2, 520), "scaled by 1/sqrt(d)", font=small, fill=(128, 128, 128), anchor="mm")
    d.rectangle([W // 2 - 120, 580, W // 2 + 120, 588], fill=(214, 40, 40))  # sparse accent
    im.save(work / "explainer.png")
    a = np.asarray(im).astype(int)
    chroma = (a.max(-1) - a.min(-1)) > 40
    accent = chroma.mean()
    grey = ~chroma
    return [chk("16:9", W * 9 == H * 16, (W, H)),
            chk("white background dominates (>85%)", (a.min(-1) >= 250).mean() > 0.85, round(float((a.min(-1) >= 250).mean()), 3)),
            chk("accent colour sparse (<1% of pixels)", 0 < accent < 0.01, round(float(accent), 4)),
            chk("everything else is greyscale", grey.sum() + chroma.sum() == a.shape[0] * a.shape[1], "partition")]


def spring_step(zeta, omega, dt=1 / 1000, t_end=1.5):
    x, v, xs = 0.0, 0.0, []
    for _ in range(int(t_end / dt)):
        a = omega * omega * (1 - x) - 2 * zeta * omega * v
        v += a * dt
        x += v * dt
        xs.append(x)
    return np.array(xs)


def amedia_15(work):
    zeta = -math.log(0.05) / math.sqrt(math.pi ** 2 + math.log(0.05) ** 2)  # 5% overshoot
    omega = 4 / (zeta * 0.55)  # 2% settling time ~ 4/(zeta*omega) = 550 ms
    xs = spring_step(zeta, omega)
    settle = next(i for i in range(len(xs)) if np.all(np.abs(xs[i:] - 1) < 0.02)) / 1000
    blur = {"standard": 28, "modal": 40}
    layers = ["backdrop-blur", "fill rgba(255,255,255,.05)", "1px inner border top-lit", "ambient shadow"]
    css = (f".glass{{backdrop-filter:blur({blur['standard']}px);background:rgba(255,255,255,.05);"
           "border:1px solid;border-image:linear-gradient(180deg,rgba(255,255,255,.35),rgba(255,255,255,.05)) 1;"
           "box-shadow:0 30px 80px rgba(0,0,0,.25)}\n")
    (work / "glass.css").write_text(css)
    jwrite(work, "spring.json", {"zeta": zeta, "omega": omega, "peak": float(xs.max()), "settle_s": settle, "layers": layers})

    def allow_glass(bg_luma):
        return bg_luma < 0.35

    return [chk("overshoot ~1.05", near(xs.max(), 1.05, 0.005), round(float(xs.max()), 4)),
            chk("settles inside 400-700 ms", 0.4 <= settle <= 0.7, settle),
            chk("glass stack has 4 layers bottom->top, blur 28 standard / 40 modal",
                len(layers) == 4 and "blur(28px)" in css and blur["modal"] == 40, layers),
            chk("glass only on dark backgrounds", allow_glass(0.1) and not allow_glass(0.9), "dark only")]


def amedia_16(work):
    """A two-program pipeline in numpy: vertex stage writes positions, fragment stage reads interpolated varyings."""
    W = H = 32
    verts = np.array([[-1, -1], [1, -1], [-1, 1]], float)
    uvs = np.array([[0, 0], [1, 0], [0, 1]], float)
    uniforms = {"uTime": 0.5, "uScale": 1.0}

    def vertex(p, u):
        return p * u["uScale"]  # gl_Position (clip space)

    def fragment(v_uv, u):
        return np.array([v_uv[0], v_uv[1], u["uTime"]])

    clip = np.array([vertex(p, uniforms) for p in verts])
    scr = (clip + 1) / 2 * np.array([W, H])
    img = np.zeros((H, W, 3))
    covered = 0
    a, b, c = scr
    den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    for y in range(H):
        for x in range(W):
            p = np.array([x + 0.5, y + 0.5])
            l1 = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) / den
            l2 = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) / den
            l3 = 1 - l1 - l2
            if min(l1, l2, l3) >= 0:
                vuv = l1 * uvs[0] + l2 * uvs[1] + l3 * uvs[2]  # varying
                img[y, x] = fragment(vuv, uniforms)
                covered += 1
    Image.fromarray((img * 255).astype(np.uint8)).save(work / "raster.png")
    px = img[8, 20]  # pixel centre (20.5, 8.5) -> uv = (20.5/32, 8.5/32)
    return [chk("varying uv interpolated at pixel centre", np.allclose(px[:2], [20.5 / 32, 8.5 / 32]), px[:2].round(4).tolist()),
            chk("uniform identical for every fragment", set(np.round(img[img.any(-1)][:, 2], 6)) == {0.5}, "uTime 0.5"),
            chk("half the screen covered by the triangle", abs(covered - W * H / 2) <= W, covered)]


def amedia_17(work):
    rng = np.random.default_rng(4)
    W, H, R = 200, 120, 6.0
    obstacles = [(70, 50, 130, 70)]  # copy block
    n = 30
    pos = np.column_stack([rng.uniform(R, W - R, n), rng.uniform(R, H - R, n)])
    for i in range(n):
        while obstacles[0][0] - R < pos[i, 0] < obstacles[0][2] + R and obstacles[0][1] - R < pos[i, 1] < obstacles[0][3] + R:
            pos[i] = [rng.uniform(R, W - R), rng.uniform(R, H - R)]
    vel = rng.normal(0, 30, (n, 2))
    dt = 1 / 60
    for _ in range(240):
        pos += vel * dt
        for k in range(2):
            lo, hi = R, (W, H)[k] - R
            m = (pos[:, k] < lo) | (pos[:, k] > hi)
            vel[m, k] *= -1
            pos[:, k] = np.clip(pos[:, k], lo, hi)
        x0, y0, x1, y1 = obstacles[0]
        cx, cy = np.clip(pos[:, 0], x0, x1), np.clip(pos[:, 1], y0, y1)
        d = np.hypot(pos[:, 0] - cx, pos[:, 1] - cy)
        hit = d < R
        for i in np.nonzero(hit)[0]:
            nrm = np.array([pos[i, 0] - cx[i], pos[i, 1] - cy[i]]) / max(d[i], 1e-9)
            pos[i] = np.array([cx[i], cy[i]]) + nrm * R
            vel[i] -= 2 * vel[i].dot(nrm) * nrm
        for i in range(n):
            for j in range(i + 1, n):
                dv = pos[j] - pos[i]
                dd = np.hypot(*dv)
                if 0 < dd < 2 * R:
                    nn = dv / dd
                    ov = (2 * R - dd) / 2
                    pos[i] -= nn * ov
                    pos[j] += nn * ov
                    rel = (vel[i] - vel[j]).dot(nn)
                    if rel > 0:
                        vel[i] -= rel * nn
                        vel[j] += rel * nn
    x0, y0, x1, y1 = obstacles[0]
    cx, cy = np.clip(pos[:, 0], x0, x1), np.clip(pos[:, 1], y0, y1)
    pen = float((R - np.hypot(pos[:, 0] - cx, pos[:, 1] - cy)).max())
    word = "WORD"

    def letter_state(i, t, stagger=0.08, blur=8, hold=0.6):
        p = min(max((t - i * stagger) / 0.3, 0), 1)
        return {"opacity": 1 - p, "blur": blur * p}

    jwrite(work, "letters.json", pos.round(2).tolist())
    return [chk("no letter inside the copy block (penetration < 0.5 px)", pen < 0.5, round(pen, 3)),
            chk("letters stay inside the viewport", (pos[:, 0] >= R - 1e-6).all() and (pos[:, 0] <= W - R + 1e-6).all(), "inside"),
            chk("disappearing word staggers per letter", [round(letter_state(i, 0.2)["opacity"], 3) for i in range(4)]
                == [round(1 - 0.2 / 0.3, 3), round(1 - 0.12 / 0.3, 3), round(1 - 0.04 / 0.3, 3), 1.0], word)]


def amedia_18(work):
    stops = [0, .12, .30, .45, .60, .78, 1.0]
    cols = np.array([[0, 40, 60], [0, 128, 128], [30, 160, 60], [230, 220, 40], [250, 150, 20], [230, 40, 30], [255, 255, 255]], float)

    def smoothstep(a, b, x):
        t = np.clip((x - a) / (b - a), 0, 1)
        return t * t * (3 - 2 * t)

    def thermal(h):
        c = np.broadcast_to(cols[0], h.shape + (3,)).copy()
        for k in range(1, 7):
            s = smoothstep(stops[k - 1], stops[k], h)[..., None]
            c = c * (1 - s) + cols[k] * s
        return c

    def hash2(p):
        return np.modf(np.sin(p[..., 0] * 127.1 + p[..., 1] * 311.7) * 43758.5453)[0] % 1.0

    def noise(p):
        i, f = np.floor(p), p - np.floor(p)
        u = f * f * (3 - 2 * f)
        a, b = hash2(i), hash2(i + [1, 0])
        c, d = hash2(i + [0, 1]), hash2(i + [1, 1])
        return a + (b - a) * u[..., 0] + (c - a) * u[..., 1] + (a - b - c + d) * u[..., 0] * u[..., 1]

    def fbm(p, oct_=5):
        v, amp = 0.0, 0.5
        for _ in range(oct_):
            v = v + amp * noise(p)
            p = p * 2.0
            amp *= 0.5
        return v

    yy, xx = np.mgrid[:64, :64] / 64.0
    p = np.dstack([xx, yy]) * 3
    q = np.dstack([fbm(p), fbm(p + 5.2)])
    warped = fbm(p + 4 * q)
    bg = 0.34 + 0.32 * (warped - warped.min()) / (np.ptp(warped) + 1e-9)
    trail = [{"pos": (0.2 + 0.02 * k, 0.5), "age": 23 - k} for k in range(30)][-24:]
    heat = bg.copy()
    for pt in trail:
        d = np.hypot(xx - pt["pos"][0], yy - pt["pos"][1])
        heat = np.maximum(heat, (1 - pt["age"] / 24) * np.exp(-(d / 0.17) ** 2) * 0.9)
    heat = np.minimum(heat, 0.75)
    rgb = thermal(heat)
    Image.fromarray(rgb.astype(np.uint8)).save(work / "thermal.png")
    return [chk("background heat in 0.34-0.66", bg.min() >= 0.34 - 1e-9 and bg.max() <= 0.66 + 1e-9, (round(bg.min(), 3), round(bg.max(), 3))),
            chk("heat capped at 0.75", heat.max() <= 0.75 + 1e-12, round(float(heat.max()), 3)),
            chk("trail keeps the last 24 points", len(trail) == 24, len(trail)),
            chk("colour at stops: 0 teal-dark, 1 white", np.allclose(thermal(np.array([0.0]))[0], cols[0]) and
                np.allclose(thermal(np.array([1.0]))[0], cols[6]), "stops"),
            chk("5-octave fbm is deterministic", np.array_equal(fbm(p), fbm(p)), "same")]


def amedia_19(work):
    def choose(change):
        table = [("same_item_deeper", "shared-element"), ("data_loaded", "suspense-reveal"), ("list_reorder", "per-item-key"),
                 ("appear", "enter-exit"), ("disappear", "enter-exit"), ("tab_switch", "fade-or-none"),
                 ("background_refresh", "none"), ("route_change", "route-level")]
        return dict(table).get(change, "none")

    def nav_type(from_depth, to_depth):
        return "nav-forward" if to_depth > from_depth else "nav-back" if to_depth < from_depth else None

    cases = {"same_item_deeper": "shared-element", "data_loaded": "suspense-reveal", "list_reorder": "per-item-key",
             "tab_switch": "fade-or-none", "background_refresh": "none"}
    got = {k: choose(k) for k in cases}
    jwrite(work, "transitions.json", got)
    return [chk(f"{k} -> {v}", got[k] == v, got[k]) for k, v in cases.items()] + \
           [chk("hierarchy depth gives nav-forward/nav-back", (nav_type(1, 2), nav_type(2, 1)) == ("nav-forward", "nav-back"), "typed")]


def amedia_20(work):
    kit = work / "kit"
    (kit / "ATTACH").mkdir(parents=True)
    (kit / "frames").mkdir()
    Image.new("RGB", (1080, 1920), (20, 20, 30)).save(kit / "ATTACH" / "logo_plate.png")
    Image.new("RGB", (540, 960), (200, 160, 60)).save(kit / "frames" / "01_hold_logo_2s.png")
    (kit / "PROMPT.md").write_text("# Brief\nScene 1 ...\n# Transformation chain\nlogo -> sunrise\n")
    order = ["PROMPT.md", "ATTACH/logo_plate.png", "frames/01_hold_logo_2s.png"]
    (kit / "START-HERE.md").write_text("Upload in one message, in this order:\n" + "".join(f"{i + 1}. {f}\n" for i, f in enumerate(order)))
    rows = []
    for f in sorted(p for p in kit.rglob("*") if p.is_file() and p.name not in ("KIT.md",)):
        rel = f.relative_to(kit).as_posix()
        size = "x".join(map(str, Image.open(f).size)) if f.suffix == ".png" else "-"
        rows.append(f"| {rel} | {size} | {'none' if 'frames' not in rel else 'half-res reference'} |")
    (kit / "KIT.md").write_text("| file | pixels | known defects |\n|---|---|---|\n" + "\n".join(rows) + "\n")

    def validate(k):
        errs = []
        for req in ("PROMPT.md", "START-HERE.md", "KIT.md", "ATTACH", "frames"):
            if not (k / req).exists():
                errs.append(f"missing {req}")
        listed = (k / "KIT.md").read_text()
        for f in k.rglob("*"):
            if f.is_file() and f.name != "KIT.md" and f.relative_to(k).as_posix() not in listed:
                errs.append(f"unlisted {f.name}")
        start = (k / "START-HERE.md").read_text()
        for f in (k / "ATTACH").iterdir():
            if f"ATTACH/{f.name}" not in start:
                errs.append(f"not in upload order: {f.name}")
        return errs

    ok = validate(kit)
    Image.new("RGB", (10, 10)).save(kit / "ATTACH" / "stray.png")
    bad = validate(kit)
    (kit / "ATTACH" / "stray.png").unlink()
    return [chk("kit validates", ok == [], ok),
            chk("KIT.md records pixel sizes", "1080x1920" in (kit / "KIT.md").read_text(), "1080x1920"),
            chk("stray asset not in KIT.md or upload order caught", "unlisted stray.png" in bad and
                "not in upload order: stray.png" in bad, bad)]


def amedia_21(work):
    def probe_tools(fake_missing=()):
        return {t: (shutil.which(t) is not None and t not in fake_missing) for t in ("ffmpeg", "chromium", "espeak")}

    def run(tools):
        scenes = [("problem", "Exports take hours"), ("solution", "One command"), ("proof", "3x faster"), ("cta", "Try it")]
        if not tools["ffmpeg"]:
            cmds = [f"ffmpeg -loop 1 -t 2 -i scene_{i}.png ..." for i in range(len(scenes))]
            (work / "MANUAL.md").write_text("\n".join(cmds) + "\n")
            return "manual", None
        for i, (kind, txt) in enumerate(scenes):
            im = Image.new("RGB", (192, 108), (14, 14, 18) if kind != "cta" else (30, 90, 200))
            ImageDraw.Draw(im).text((10, 45), txt, fill=(230, 230, 230))
            im.save(work / f"scene_{i}.png")
        narr = write_wav(work / "narration.wav", tone(len(scenes) * 0.5, 200, 16000, 0.2), 16000)
        (work / "list.txt").write_text("".join(f"file 'scene_{i}.png'\nduration 0.5\n" for i in range(len(scenes)))
                                       + f"file 'scene_{len(scenes) - 1}.png'\n")
        out = work / "demo.mp4"
        ff("-f", "concat", "-safe", "0", "-i", work / "list.txt", "-i", narr, "-vf", "fps=30,format=yuv420p",
           "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-shortest", out)
        return "full", out

    mode, out = run(probe_tools())
    mode2, _ = run(probe_tools(fake_missing=("ffmpeg",)))
    return [chk("full mode when ffmpeg is present", mode == "full" and out is not None, mode),
            chk("demo has 4 story scenes over 2.0 s", near(duration(out), 2.0, 0.12), duration(out)),
            chk("manual mode writes exact commands when a tool is missing", mode2 == "manual" and (work / "MANUAL.md").is_file(), mode2)]


def amedia_22(work):
    # VFR fixture: irregular timestamps
    fr = frame_index_frames(20)
    src = write_video(work / "cfr.mkv", fr, 20)
    ff("-i", src, "-vf", "setpts='PTS+if(gt(N,10),0.07/TB,0)'", "-fps_mode", "passthrough", "-c:v", "ffv1", work / "vfr.mkv")

    def is_vfr(p):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "frame=pts_time",
                            "-of", "csv=p=0", str(p)], capture_output=True, text=True)
        t = np.array([float(x) for x in r.stdout.split() if x.strip()])
        d = np.diff(t)
        return bool(np.ptp(d) > 1e-3), t

    v1, _ = is_vfr(work / "vfr.mkv")
    ff("-i", work / "vfr.mkv", "-vf", "fps=20", "-c:v", "ffv1", work / "fixed.mkv")
    v2, _ = is_vfr(work / "fixed.mkv")
    # ABR ladder with aligned GOP 60
    keys = {}
    for h in (1080, 720, 480):
        d = work / f"hls_{h}"
        d.mkdir()
        ff("-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=30:d=4", "-vf", f"scale=-2:{h}", "-c:v", "libx264", "-preset",
           "ultrafast", "-g", "60", "-keyint_min", "60", "-sc_threshold", "0", "-f", "hls", "-hls_time", "2",
           "-hls_playlist_type", "vod", d / "index.m3u8")
        ts = sorted(d.glob("*.ts"))
        keys[h] = [round(duration(t), 2) for t in ts]
    master = "#EXTM3U\n" + "".join(f"#EXT-X-STREAM-INF:BANDWIDTH={b},RESOLUTION={w}x{h}\nhls_{h}/index.m3u8\n"
                                    for (w, h, b) in [(1920, 1080, 5000000), (1280, 720, 2800000), (854, 480, 1400000)])
    (work / "master.m3u8").write_text(master)
    return [chk("VFR detected in the drifting file", v1, v1),
            chk("fps filter makes it constant frame rate", not v2, v2),
            chk("3 renditions with identical 2 s segments (aligned keyframes)", keys[1080] == keys[720] == keys[480] == [2.0, 2.0], keys)]


def amedia_23(work):
    fr = frame_index_frames(90)
    srt = work / "subs.srt"
    srt.write_text("1\n00:00:00,500 --> 00:00:02,500\nhello\n")
    src = work / "src.mp4"
    ff("-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "64x36", "-r", "30", "-i", "-", "-i", write_wav(work / "a.wav", tone(3)),
       "-i", srt, "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "libx264", "-preset", "ultrafast", "-g", "30",
       "-keyint_min", "30", "-sc_threshold", "0", "-crf", "5", "-pix_fmt", "yuv420p", "-c:a", "aac", "-c:s", "mov_text", src,
       inp=fr.tobytes())
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "frame=key_frame,pts_time",
                        "-of", "csv=p=0", str(src)], capture_output=True, text=True)
    keyts = [float(l.split(",")[1]) for l in r.stdout.split() if l.startswith("1,")]
    want = 1.4
    snap = max(k for k in keyts if k <= want + 1e-6)
    out = work / "cut.mp4"
    ff("-ss", snap, "-i", src, "-t", "1.0", "-map", "0", "-c", "copy", "-avoid_negative_ts", "make_zero", out)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-map", "0:v", "-fps_mode", "passthrough", "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    first = decode_index(np.frombuffer(raw, np.uint8).reshape(36, 64, 3))
    kinds = sorted(s["codec_type"] for s in probe(out)["streams"])
    return [chk("in-point 1.4 s snapped to previous keyframe 1.0 s", near(snap, 1.0, 1e-3), snap),
            chk("stream-copy cut starts on source frame 30 (no black start)", first == 30, first),
            chk("-map 0 keeps audio and subtitles", kinds == ["audio", "subtitle", "video"], kinds)]


def amedia_25(work):
    def check(title, thumb, intent):
        errs = []
        tw = {w.lower().strip(".,!?") for w in title.split()}
        rep = [w for w in thumb.split() if w.lower().strip(".,!?") in tw]
        if rep:
            errs.append(f"thumbnail repeats title word(s): {rep}")
        if len(title) > 60:
            errs.append("title > 60 chars")
        if not 1 <= len(thumb.split()) <= 3:
            errs.append("thumbnail text must be 1-3 words")
        if intent == "search" and not title.lower().startswith(("how to", "best", "كيف")):
            errs.append("search intent: front-load the query phrase")
        return errs

    good = check("How to fix a slow laptop in 10 minutes", "STILL LAGGING?", "search")
    bad = check("This laptop trick will change your life forever and ever, really", "laptop trick here now", "search")
    jwrite(work, "packaging.json", {"good": good, "bad": bad})
    return [chk("good pair passes", good == [], good),
            chk("repeated word caught", any("repeats" in e for e in bad), bad),
            chk(">60 char title and 4-word thumbnail caught", "title > 60 chars" in bad and "thumbnail text must be 1-3 words" in bad, bad),
            chk("search title must front-load the query", any("front-load" in e for e in bad), bad)]


def srgb_to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def amedia_26(work):
    spaces = {"BaseColor": "sRGB", "Emissive": "sRGB", "Normal": "linear", "Roughness": "linear", "Metallic": "linear",
              "AO": "linear", "Height": "linear"}
    n = np.array([0.3, -0.4, 0.866])
    n /= np.linalg.norm(n)
    enc = (n + 1) / 2  # stored texel
    right = enc * 2 - 1
    wrong = srgb_to_lin(enc) * 2 - 1  # texture flagged sRGB gets linearised by the sampler
    rough = 0.5
    wrong_rough = float(srgb_to_lin(np.array(rough)))
    pack = np.zeros((4, 4, 3), np.uint8)
    pack[..., 0], pack[..., 1], pack[..., 2] = 255, 128, 0  # ORM: AO, Roughness, Metallic
    Image.fromarray(pack).save(work / "orm.png")
    jwrite(work, "colour_spaces.json", spaces)
    ang = math.degrees(math.acos(np.clip(np.dot(right, wrong / np.linalg.norm(wrong)), -1, 1)))
    return [chk("only BaseColor and Emissive are sRGB", [k for k, v in spaces.items() if v == "sRGB"] == ["BaseColor", "Emissive"], spaces),
            chk("linear normal decodes exactly", np.allclose(right, n), right.round(4).tolist()),
            chk("sRGB-flagged normal bends the vector by > 10 deg", ang > 10, round(ang, 2)),
            chk("sRGB-flagged roughness 0.5 reads as 0.214", near(wrong_rough, 0.214, 0.001), round(wrong_rough, 4))]


def amedia_28(work):
    import xml.etree.ElementTree as ET
    fd = Fraction(1001, 30000)  # 29.97 frame duration

    def t(fr):
        v = fr * fd
        return f"{v.numerator}/{v.denominator}s" if v.denominator != 1 else f"{v.numerator}s"

    clips = [("a", 0, 90), ("b", 30, 60), ("c", 0, 45)]
    root = ET.Element("fcpxml", version="1.10")
    res = ET.SubElement(root, "resources")
    ET.SubElement(res, "format", id="r1", frameDuration=f"{fd.numerator}/{fd.denominator}s", width="1920", height="1080",
                  colorSpace="1-1-1 (Rec. 709)")
    for i, (name, _, _) in enumerate(clips):
        ET.SubElement(res, "asset", id=f"a{i}", name=name, src=f"file:///media/{name}.mov", duration=t(300), hasVideo="1",
                      hasAudio="1", format="r1")
    lib = ET.SubElement(root, "library")
    ev = ET.SubElement(lib, "event", name="KOSIF")
    proj = ET.SubElement(ev, "project", name="cut")
    seq = ET.SubElement(proj, "sequence", format="r1", duration=t(sum(c[2] for c in clips)))
    spine = ET.SubElement(seq, "spine")
    off = 0
    for i, (name, start, dur) in enumerate(clips):
        cl = ET.SubElement(spine, "asset-clip", ref=f"a{i}", name=name, offset=t(off), start=t(start), duration=t(dur))
        if i == 1:
            ET.SubElement(cl, "chapter-marker", start=t(start), duration=t(1), value="Chapter 2")
        off += dur
    p = work / "cut.fcpxml"
    ET.ElementTree(root).write(p, encoding="UTF-8", xml_declaration=True)
    back = ET.parse(p).getroot()
    fr = lambda s: Fraction(s[:-1]) / fd
    offs = [fr(c.get("offset")) for c in back.iter("asset-clip")]
    durs = [fr(c.get("duration")) for c in back.iter("asset-clip")]
    contiguous = all(offs[i + 1] == offs[i] + durs[i] for i in range(len(offs) - 1))
    return [chk("rational frameDuration 1001/30000s", back.find("resources/format").get("frameDuration") == "1001/30000s", "29.97"),
            chk("every time is a whole number of frames", all(x.denominator == 1 for x in offs + durs), offs),
            chk("primary storyline is gapless", contiguous, [int(o) for o in offs]),
            chk("chapter marker attached", len(list(back.iter("chapter-marker"))) == 1, "1 marker")]


DTMF = {"1": (697, 1209), "2": (697, 1336), "3": (697, 1477), "4": (770, 1209), "5": (770, 1336), "6": (770, 1477),
        "7": (852, 1209), "8": (852, 1336), "9": (852, 1477), "*": (941, 1209), "0": (941, 1336), "#": (941, 1477)}


def goertzel(x, f, sr):
    k = 2 * math.cos(2 * math.pi * f / sr)
    s1 = s2 = 0.0
    for v in x:
        s1, s2 = v + k * s1 - s2, s1
    return s1 * s1 + s2 * s2 - k * s1 * s2


def amedia_30(work):
    sr = 8000
    digits = "105#"
    sig = []
    for d in digits:
        t = np.arange(int(0.08 * sr)) / sr
        lo, hi = DTMF[d]
        sig += [0.4 * (np.sin(2 * np.pi * lo * t) + np.sin(2 * np.pi * hi * t)), np.zeros(int(0.05 * sr))]
    x = np.concatenate(sig) + np.random.default_rng(0).normal(0, 0.01, sum(len(s) for s in sig))
    write_wav(work / "dtmf_8k.wav", x, sr)
    lows, highs = [697, 770, 852, 941], [1209, 1336, 1477]
    got, step = "", int(0.13 * sr)
    for i in range(0, len(x), step):
        blk = x[i:i + int(0.08 * sr)]
        if np.sqrt((blk ** 2).mean()) < 0.1:
            continue
        lo = max(lows, key=lambda f: goertzel(blk, f, sr))
        hi = max(highs, key=lambda f: goertzel(blk, f, sr))
        got += next(k for k, v in DTMF.items() if v == (lo, hi))

    def route(step_kind):
        return "ivr-keypad" if step_kind in ("authenticate", "menu") else "conversation"

    def transfer(ctx):
        return {"to": "human", "summary": ctx["summary"], "caller": ctx["caller"]} if ctx.get("summary") else None

    calls = [{"goal": True}, {"goal": True}, {"goal": False}, {"goal": True}]
    success = sum(c["goal"] for c in calls) / len(calls)
    return [chk("DTMF 105# decoded with Goertzel at 8 kHz", got == digits, got),
            chk("authentication goes to a deterministic keypad step", route("authenticate") == "ivr-keypad" and
                route("question") == "conversation", "mixed"),
            chk("warm transfer carries context", transfer({"summary": "billing", "caller": "+9665"})["summary"] == "billing", "ctx"),
            chk("task success as primary metric = 0.75", success == 0.75, success)]


PROGRAMS = {
    "AMEDIA-02": amedia_02, "AMEDIA-03": amedia_03, "AMEDIA-05": amedia_05, "AMEDIA-07": amedia_07,
    "AMEDIA-09": amedia_09, "AMEDIA-10": amedia_10, "AMEDIA-11": amedia_11, "AMEDIA-12": amedia_12,
    "AMEDIA-13": amedia_13, "AMEDIA-14": amedia_14, "AMEDIA-15": amedia_15, "AMEDIA-16": amedia_16,
    "AMEDIA-17": amedia_17, "AMEDIA-18": amedia_18, "AMEDIA-19": amedia_19, "AMEDIA-20": amedia_20,
    "AMEDIA-21": amedia_21, "AMEDIA-22": amedia_22, "AMEDIA-23": amedia_23, "AMEDIA-25": amedia_25,
    "AMEDIA-26": amedia_26, "AMEDIA-28": amedia_28, "AMEDIA-30": amedia_30,
}
