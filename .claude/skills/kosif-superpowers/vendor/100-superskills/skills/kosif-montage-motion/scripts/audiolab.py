"""Audio Lab — the user's Cinema C V32 lab, on the engine: split a clip's sound before the montage.

    python scripts/kmotion.py audiolab FILE --mode voice|music|both|novoice|nomusic [--strong] [--out DIR]
      voice    the speech alone: RNNoise speech isolation (arnndn, model `lq` from richardpl/arnndn-models, fetched once)
               + FFT denoise + dynamic levelling; without the model, the FFT filter alone (lower quality, said so)
      music    the music bed alone: centred vocals cancelled by phase (needs a REAL stereo mix; a mono or fake-stereo
               source is refused — say so instead of returning a damaged file), the bass restored below 140 Hz
      both     voice.wav + music.wav
      novoice  the video with the music bed only (B-roll under a new voice-over)
      nomusic  the video with the isolated voice only (a talking clip whose music must go)
Outputs are 48 kHz WAV (and MP4 for the video modes: picture copied, AAC 192k). Phase cancellation is not AI stem
separation: it removes what sits in the centre (voice, often bass and kick too) and can leave reverb tails.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FF = shutil.which("ffmpeg") or "ffmpeg"
MODEL = os.environ.get("KOSIF_RNN_MODEL", "lq")            # lq = voice vs general noise (best under music beds)
MODEL_URLS = ["https://raw.githubusercontent.com/richardpl/arnndn-models/master/{m}.rnnn",
              "https://github.com/richardpl/arnndn-models/raw/master/{m}.rnnn"]


def _models_dir() -> Path:
    d = Path(os.environ.get("KOSIF_MOTION_HOME") or HERE.parent) / "workbench" / "models"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _ff(*args, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run([FF, "-y", "-nostdin", "-hide_banner", "-loglevel", "error", *args], capture_output=True, text=True, cwd=cwd)


def has_filter(name: str) -> bool:
    r = subprocess.run([FF, "-hide_banner", "-filters"], capture_output=True, text=True)
    return f" {name} " in r.stdout


def ensure_model() -> Path | None:
    m = _models_dir() / f"{MODEL}.rnnn"
    if m.exists() and m.stat().st_size > 0:
        return m
    for u in MODEL_URLS:
        try:
            data = urllib.request.urlopen(u.format(m=MODEL), timeout=60).read(20_000_000)
            if data:
                m.write_bytes(data); return m
        except Exception:  # noqa: BLE001
            continue
    return None


def prepare(src: Path, job: Path) -> tuple[Path, bool]:
    wav = job / "source.wav"
    r = _ff("-i", str(src), "-vn", "-sn", "-dn", "-map", "0:a:0", "-ar", "48000", "-c:a", "pcm_s16le", str(wav))
    if r.returncode or not wav.exists():
        raise SystemExit(f"{src}: no readable audio track")
    info = subprocess.run([FF, "-hide_banner", "-i", str(wav)], capture_output=True, text=True).stderr
    if re.search(r"Audio:.*(mono|1 channels)", info):
        return wav, False
    side = subprocess.run([FF, "-hide_banner", "-nostdin", "-i", str(wav), "-af", "pan=mono|c0=c0-c1,volumedetect", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    m = re.search(r"max_volume:\s*(-?[\d.]+|-inf) dB", side)
    stereo = bool(m) and m.group(1) != "-inf" and float(m.group(1)) > -45      # a real side channel, not identical L/R
    return wav, stereo


def voice(wav: Path, stereo: bool, out: Path, strong: bool = False) -> dict:
    chain = ("pan=mono|c0=0.5*c0+0.5*c1," if stereo else "") + "highpass=f=80,lowpass=f=8000"
    model = ensure_model() if has_filter("arnndn") else None
    if model:
        chain += f",arnndn=m={model.name}" + (f",arnndn=m={model.name}" if strong else "")
    if has_filter("afftdn"):
        chain += ",afftdn=nf=-30" if model else ",afftdn=nr=24:nf=-28"
    chain += ",dynaudnorm=f=200:g=11,alimiter=limit=0.95"
    r = _ff("-i", str(wav.resolve()), "-af", chain, "-ar", "48000", "-c:a", "pcm_s16le", str(out.resolve()),
            cwd=str(model.parent) if model else None)                 # the model by name from its folder: no Windows path escaping
    if r.returncode:
        raise SystemExit("voice isolation failed: " + r.stderr[-300:])
    return {"voice": str(out), "voice_method": f"RNNoise ({MODEL}{', double pass' if strong else ''}) + FFT denoise" if model else "FFT denoise only (no model: lower quality)"}


def music(wav: Path, stereo: bool, out: Path) -> dict:
    if not stereo:
        raise SystemExit("music-only needs a real stereo mix: this source is mono (or identical L/R), so voice and music "
                         "cannot be split by phase — use an AI stem separator for it")
    fc = ("[0:a]asplit=2[a][b];[a]pan=stereo|c0=c0-c1|c1=c1-c0,highpass=f=140[s];"
          "[b]pan=mono|c0=0.5*c0+0.5*c1,lowpass=f=140,pan=stereo|c0=c0|c1=c0[l];"
          "[s][l]amerge=inputs=2,pan=stereo|c0=c0+c2|c1=c1+c3,alimiter=limit=0.95[out]")
    r = _ff("-i", str(wav), "-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", str(out))
    if r.returncode:
        raise SystemExit("music extraction failed: " + r.stderr[-300:])
    return {"music": str(out), "music_method": "centre cancellation (side channel) + bass restored < 140 Hz"}


def mux(video: Path, wav: Path, out: Path) -> Path:
    r = _ff("-i", str(video), "-i", str(wav), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
            "-shortest", "-movflags", "+faststart", str(out))
    if r.returncode:
        r = _ff("-i", str(video), "-i", str(wav), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", "-movflags", "+faststart", str(out))
        if r.returncode:
            raise SystemExit("mux failed: " + r.stderr[-300:])
    return out


def run(src: Path, mode: str, out_dir: Path | None = None, strong: bool = False) -> dict:
    src = Path(src)
    out_dir = Path(out_dir or src.parent / f"{src.stem}.lab")
    out_dir.mkdir(parents=True, exist_ok=True)
    job = Path(tempfile.mkdtemp(prefix="kosif_lab_"))
    wav, stereo = prepare(src, job)
    rep: dict = {"source": str(src), "stereo": stereo, "out": str(out_dir)}
    if mode in ("voice", "both", "nomusic"):
        rep.update(voice(wav, stereo, out_dir / f"{src.stem} - voice.wav", strong))
    if mode in ("music", "both", "novoice"):
        rep.update(music(wav, stereo, out_dir / f"{src.stem} - music.wav"))
    is_video = " Video: " in subprocess.run([FF, "-hide_banner", "-i", str(src)], capture_output=True, text=True).stderr
    if mode in ("novoice", "nomusic"):
        if not is_video:
            raise SystemExit(f"{mode} needs a video file")
        wav_in = Path(rep["music"] if mode == "novoice" else rep["voice"])
        rep["video"] = str(mux(src, wav_in, out_dir / f"{src.stem} - {'without voice' if mode == 'novoice' else 'without music'}.mp4"))
    shutil.rmtree(job, ignore_errors=True)
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file"); ap.add_argument("--mode", required=True, choices=["voice", "music", "both", "novoice", "nomusic"])
    ap.add_argument("--strong", action="store_true", help="a second neural pass (more noise removed, a little more colour)")
    ap.add_argument("--out")
    a = ap.parse_args()
    print(json.dumps(run(Path(a.file), a.mode, Path(a.out) if a.out else None, a.strong), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
