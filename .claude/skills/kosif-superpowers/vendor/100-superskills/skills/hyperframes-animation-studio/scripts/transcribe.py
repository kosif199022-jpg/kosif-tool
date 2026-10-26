"""KOSIF transcribe — speech → words with times (faster-whisper, offline, models from the local Hugging Face cache).

    python transcribe.py VIDEO_OR_AUDIO [--model large-v3|small|base] [--lang ar] [--out DIR]

Writes NAME.words.json ([{start, end, text, words: [{text, start, end, p}]}]), NAME.srt (UTF-8 with BOM, for players)
and NAME.captions.json (the montage/captions spec). Times come from the audio; the words drive animation timing.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

FF = shutil.which("ffmpeg") or "ffmpeg"


def _srt_time(t: float) -> str:
    ms = int(round(max(0.0, t) * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def transcribe(src: Path, model: str = "large-v3", lang: str | None = "ar", prompt: str | None = None) -> list[dict]:
    from faster_whisper import WhisperModel
    tmp = Path(tempfile.mkdtemp(prefix="kosif_asr_")) / "a.wav"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", str(tmp)], check=True)
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(str(tmp), language=lang, word_timestamps=True, beam_size=5, initial_prompt=prompt)
    out = []
    for s in segs:
        words = [{"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "p": round(w.probability, 3)} for w in s.words]
        out.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": words})
    return out


def write_all(segs: list[dict], base: Path) -> dict:
    base.parent.mkdir(parents=True, exist_ok=True)
    (base.with_suffix(".words.json")).write_text(json.dumps(segs, ensure_ascii=False, indent=1), encoding="utf-8")
    srt = "\n".join(f"{i + 1}\n{_srt_time(s['start'])} --> {_srt_time(s['end'])}\n{s['text']}\n" for i, s in enumerate(segs))
    (base.with_suffix(".srt")).write_text(srt, encoding="utf-8-sig")
    caps = [{"start": s["start"], "end": s["end"], "text": s["text"], "words": s["words"]} for s in segs]
    (base.with_suffix(".captions.json")).write_text(json.dumps(caps, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"segments": len(segs), "words": sum(len(s["words"]) for s in segs), "srt": str(base.with_suffix(".srt")),
            "captions": str(base.with_suffix(".captions.json"))}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src"); ap.add_argument("--model", default="large-v3"); ap.add_argument("--lang", default="ar")
    ap.add_argument("--prompt"); ap.add_argument("--out")
    a = ap.parse_args()
    src = Path(a.src)
    segs = transcribe(src, a.model, None if a.lang == "auto" else a.lang, a.prompt)
    base = (Path(a.out) if a.out else src.parent) / src.stem
    rep = write_all(segs, base)
    for s in segs:
        print(f"{s['start']:6.2f}–{s['end']:6.2f}  {s['text']}")
    print(json.dumps(rep, ensure_ascii=False))


if __name__ == "__main__":
    main()
