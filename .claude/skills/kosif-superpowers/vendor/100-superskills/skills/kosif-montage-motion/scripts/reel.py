"""KOSIF reel — one command from a raw talking clip to a finished vertical short.

    python reel.py CLIP.mp4 --out FINAL.mp4 [--size 1080x1920] [--model large-v3|small] [--music auto|none|score.wav]
                   [--style reels|cinema|punchy] [--no-decaption] [--no-captions] [--credit "insta: name"] [--transcript NAME.words.json]

1 transcribe (faster-whisper, word times) → 2 erase burned-in captions if any (decaption) → 3 restore: light temporal
denoise, Lanczos upscale/reframe to the target, a gentle grade (cleaner blacks, highlight roll-off, warmer mids),
contrast-adaptive sharpening → 4 voice chain (high-pass, light denoise, clarity/warmth EQ, de-ess, gentle compression)
→ 5 music: none if the clip already carries a bed (heard in the pauses), else an original low underscore ducked under
the voice → 6 karaoke captions from the word times (one ASS event per word, Arabic-safe) → 7 −14 LUFS / ≤ −1 dBTP,
48 kHz AAC → 8 the delivery gate (motion.py inspect). Writes FINAL.mp4, FINAL.srt and FINAL.reel.json.
For a hand-directed edit (custom graphics per idea) build a composition project instead (motion.py new … + <video>).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe") or "ffprobe"
RESTORE = ("hqdn3d=1.2:1.2:3:3,{scale},eq=contrast=1.12:brightness=-0.015:saturation=1.07:gamma=0.97,"
           "curves=all='0/0 0.06/0.035 0.25/0.22 0.5/0.5 0.8/0.82 0.94/0.93 1/0.97',"
           "colorbalance=rs=0.012:bs=-0.01:rm=0.025:gm=0.005:bm=-0.02,cas=0.3")
VOICE = ("highpass=f=70,afftdn=nr=6:nf=-42,equalizer=f=220:t=q:w=1:g=1.2,equalizer=f=3200:t=q:w=1.4:g=2.2,"
         "equalizer=f=9000:t=q:w=1:g=-1,deesser=i=0.35,acompressor=threshold=0.12:ratio=2.5:attack=10:release=160:makeup=1.6")


def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(r.stderr[-1500:])
    return r


def _probe(p: Path) -> dict:
    j = json.loads(_run([FP, "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "json", str(p)]).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    num, den = v["r_frame_rate"].split("/")
    return {"w": int(v["width"]), "h": int(v["height"]), "fps": float(num) / float(den or 1), "dur": float(j["format"]["duration"]),
            "audio": any(s["codec_type"] == "audio" for s in j["streams"])}


def has_music_bed(audio: Path, words: list[dict]) -> bool:
    """A bed is present when the gaps between words are not silent (> −42 dBFS) and carry stereo difference or tones."""
    with wave.open(str(audio)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    x = x.reshape(-1, ch) if ch > 1 else x[:, None]
    spans, last = [], 0.0
    for wd in words:
        if wd["start"] - last > 0.18:
            spans.append((last + 0.04, wd["start"] - 0.04))
        last = max(last, wd["end"])
    levels = []
    for a, b in spans:
        seg = x[int(a * sr):int(b * sr)]
        if len(seg) > sr * 0.08:
            levels.append(20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9))
    if levels and max(levels) < -60:                                   # the pauses we could measure are silent: no bed
        return False
    if len(levels) >= 3:
        return float(np.median(levels)) > -42
    # word times without pauses (large models stretch each word to the next): judge by the quiet floor instead —
    # speech alone falls below about −45 dBFS between words, a music bed keeps the floor up
    hop = int(sr * 0.1)
    mono = x.mean(1)
    lv = [20 * np.log10(np.sqrt(np.mean(mono[i:i + hop] ** 2)) + 1e-9) for i in range(0, max(hop, len(mono) - hop), hop)]
    lv = [v for v in lv if v > -80]                                    # ignore digital silence (fades, black tails)
    return bool(lv) and float(np.percentile(lv, 10)) > -40


def _raw_mix(src: Path, tmp: Path) -> Path:
    raw = tmp / "raw.wav"
    _run([FF, "-y", "-v", "error", "-i", str(src), "-vn", "-ac", "2", "-ar", "48000", str(raw)])
    return raw


def reel(src: Path, out: Path, size=(1080, 1920), model="large-v3", music="auto", style="reels", decap=True, captions=True,
         credit: str | None = None, transcript: Path | None = None) -> dict:
    import transcribe as T
    import montage
    import qa
    src, out = Path(src), Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="kosif_reel_"))
    info = _probe(src)
    W, H = size
    rep = {"source": str(src), "size": f"{W}x{H}"}
    # 1 + 2 together: words (whisper, CPU) and burned captions (OpenCV, CPU) are independent — run side by side
    from concurrent.futures import ThreadPoolExecutor
    base = src

    def _asr():
        return T.load_transcript(transcript, duration=info["dur"]) if transcript else T.transcribe(src, model)

    def _decap():
        import decaption as D
        return D.decaption(src, tmp / "clean.mp4")
    with ThreadPoolExecutor(2) as ex:
        f_asr = ex.submit(_asr)
        f_dec = ex.submit(_decap) if decap else None
        segs = f_asr.result()
        if f_dec is not None:
            r = f_dec.result()
            rep["decaption"] = {k: v for k, v in r.items() if k != "shots"}
            base = tmp / "clean.mp4"
    T.write_all(segs, out.with_suffix(""))
    words = [w for s in segs for w in s["words"]]
    rep["transcript"] = [s["text"] for s in segs]
    # 3 restore + reframe (fill the target, centre crop)
    scale = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
    # an intermediate that the caption pass re-encodes anyway: near-lossless and quick (crf 12 / fast), not slow
    _run([FF, "-y", "-v", "error", "-i", str(base), "-an", "-vf", RESTORE.format(scale=scale) + ",format=yuv420p",
          "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-r", f"{info['fps']:.5f}", str(tmp / "picture.mp4")])
    # 4 voice
    _run([FF, "-y", "-v", "error", "-i", str(src), "-vn", "-ac", "2", "-ar", "48000", "-af", VOICE, str(tmp / "voice.wav")])
    # 5 music
    bed = None
    if music not in ("none", "auto"):
        bed = Path(music)
    elif music == "auto" and not has_music_bed(_raw_mix(src, tmp), words):   # judged on the raw mix (denoising lowers a bed)
        import score as SC
        sc = SC.Score(90, info["dur"], "D", "minor", seed=9)
        b = info["dur"] / (60 / 90)
        sc.arrange({"sections": [{"from": 2, "to": b * 0.4, "pad": True}, {"from": b * 0.4, "to": b, "pad": True, "bass": True}],
                    "chords": [[0, "i"], [12, "VI"], [18, "III"], [24, "VII"]]})
        bed = sc.mix(tmp / "bed.wav")
    rep["music"] = "original bed kept" if bed is None else str(bed)
    # 6 + 7 mix, captions, master
    ins = ["-i", str(tmp / "picture.mp4"), "-i", str(tmp / "voice.wav")]
    graph = "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v]"
    mixlabel = "v"
    if bed is not None:
        ins += ["-i", str(bed)]
        graph += (";[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.45[b];[v]asplit=2[vk][vm];"
                  "[b][vk]sidechaincompress=threshold=0.02:ratio=10:attack=20:release=300[d];[d][vm]amix=inputs=2:normalize=0:duration=first[m]")
        mixlabel = "m"
    graph += f";[{mixlabel}]loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false[a]"
    mixed = tmp / "mixed.mp4"
    _run([FF, "-y", "-v", "error", *ins, "-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
          "-b:a", "256k", "-ar", "48000", "-shortest", str(mixed)])
    # captions and the credit line burn in one encode (each extra pass costs minutes and a generation)
    vf = []
    if captions and words:
        spec = [{"start": s["start"], "end": s["end"], "text": s["text"], "words": s["words"]} for s in segs]
        ass_file = tmp / "caps.ass"
        ass_file.write_text(montage.ass(spec, W, H, style), encoding="utf-8")
        vf.append(f"ass='{ass_file.as_posix().replace(':', chr(92) + ':')}'")
    if credit:
        import tools
        credit_file = tmp / "credit.txt"                       # untrusted text stays out of the FFmpeg filter grammar
        credit_file.write_text(credit[:300].replace("\n", " ").replace("\r", " "), encoding="utf-8")
        fp = tools.font_path(arabic=any("\u0600" <= ch <= "\u06ff" for ch in credit))
        font_opt = f":fontfile='{tools._ff_path(fp)}'" if fp else ""
        vf.append(f"drawtext=textfile='{tools._ff_path(credit_file)}'{font_opt}:fontsize={round(H * 0.013)}:fontcolor=white@0.5:x=(w-tw)/2:y=h*0.905")
    if vf:
        _run([FF, "-y", "-v", "error", "-i", str(mixed), "-vf", ",".join(vf) + ",format=yuv420p", "-c:v", "libx264", "-preset", "medium",
              "-crf", "16", "-c:a", "copy", "-movflags", "+faststart", str(out)])
    else:
        shutil.copy2(mixed, out)
    # 8 gate
    gate = qa.inspect(out)
    rep["gate"] = {k: gate[k] for k in ("ok", "issues", "warnings", "lufs", "true_peak")}
    out.with_suffix(".reel.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip"); ap.add_argument("--out", required=True); ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--model", default="large-v3"); ap.add_argument("--music", default="auto"); ap.add_argument("--style", default="reels")
    ap.add_argument("--no-decaption", action="store_true"); ap.add_argument("--no-captions", action="store_true"); ap.add_argument("--credit")
    ap.add_argument("--transcript", type=Path, help="a pre-timed NAME.words.json (a reel without Whisper installed)")
    a = ap.parse_args()
    W, H = (int(v) for v in a.size.lower().split("x"))
    rep = reel(Path(a.clip), Path(a.out), (W, H), a.model, a.music, a.style, not a.no_decaption, not a.no_captions, a.credit, a.transcript)
    print(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
