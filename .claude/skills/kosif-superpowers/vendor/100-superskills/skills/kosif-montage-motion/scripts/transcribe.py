"""KOSIF transcribe — speech → words with times (faster-whisper, offline, models from the local Hugging Face cache).

    python transcribe.py VIDEO_OR_AUDIO [--model large-v3|small|base|auto] [--lang ar] [--out DIR] [--no-batch]

Writes NAME.words.json ([{start, end, text, words: [{text, start, end, p}]}]), NAME.srt (UTF-8 with BOM, for players)
and NAME.captions.json (the montage/captions spec). Times come from the audio; the words drive animation timing.
"""
from __future__ import annotations

import argparse
import json
import math
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


def cached_models() -> list[str]:
    hub = Path.home() / ".cache" / "huggingface" / "hub"
    return sorted(p.name.replace("models--Systran--faster-whisper-", "") for p in hub.glob("models--Systran--faster-whisper-*")) if hub.exists() else []


def pick_model(model: str) -> str:
    """'auto' = the best model already on this machine (no download), else large-v3."""
    if model != "auto":
        return model
    have = cached_models()
    for m in ("large-v3", "large-v2", "medium", "small", "base"):
        if m in have:
            return m
    return "large-v3"


def transcribe(src: Path, model: str = "large-v3", lang: str | None = "ar", prompt: str | None = None, fast: bool = True,
               vad: bool | None = None) -> list[dict]:
    """Words with times. faster-whisper first — its batched pipeline (v1.1+) is 3-4× quicker on CPU with the same
    words; openai-whisper as a fallback when faster-whisper is not installed.
    vad: True = speech filter on, False = off, None (default) = on, and when it keeps nothing — singing under a music
    bed, which the speech filter drops entirely — once more with it off (the plain decoder, no context carry-over, so a
    long instrumental cannot start a repetition loop)."""
    model = pick_model(model)
    tmp = Path(tempfile.mkdtemp(prefix="kosif_asr_")) / "a.wav"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", str(tmp)], check=True)
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return _transcribe_openai(tmp, model, lang, prompt)
    import os
    m = WhisperModel(model, device="cpu", compute_type="int8", cpu_threads=max(1, os.cpu_count() or 1))

    def run(use_vad: bool) -> list[dict]:
        kw = dict(language=lang, word_timestamps=True, beam_size=5, initial_prompt=prompt, vad_filter=use_vad)
        try:
            if not fast or not use_vad:                       # the batched pipeline needs VAD chunks
                raise ImportError
            from faster_whisper import BatchedInferencePipeline
            segs, _ = BatchedInferencePipeline(model=m).transcribe(str(tmp), batch_size=8, **kw)
        except ImportError:
            if not use_vad:
                kw["condition_on_previous_text"] = False
            segs, _ = m.transcribe(str(tmp), **kw)
        out = []
        for s in segs:
            words = [{"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "p": round(w.probability, 3)} for w in (s.words or [])]
            if words:
                out.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": words})
        return out

    out = run(vad is not False)
    if vad is None and not any(s["words"] for s in out):
        out = run(False)
    return out


def _transcribe_openai(wav: Path, model: str, lang: str | None, prompt: str | None) -> list[dict]:
    try:
        import whisper
    except ImportError:
        raise SystemExit("no speech model here: pip install faster-whisper   (or: pip install openai-whisper)")
    name = {"large-v3": "large-v3", "large-v2": "large-v2"}.get(model, model)
    m = whisper.load_model(name)
    r = m.transcribe(str(wav), language=lang, word_timestamps=True, initial_prompt=prompt)
    out = []
    for s in r["segments"]:
        words = [{"text": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3), "p": round(float(w.get("probability", 1.0)), 3)}
                 for w in s.get("words", [])]
        out.append({"start": round(s["start"], 3), "end": round(s["end"], 3), "text": s["text"].strip(), "words": words})
    return out

def load_transcript(path: Path, duration: float | None = None) -> list[dict]:
    """Accept timestamped words produced by this tool, never invented timing from plain text."""
    if path is None or not Path(path).is_file():
        raise ValueError("Transcript .words.json file does not exist")
    if Path(path).stat().st_size > 10_000_000:
        raise ValueError("Transcript exceeds 10MB size budget")
    segments = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(segments, list) or not segments or len(segments) > 20_000:
        raise ValueError("Expected a non-empty list of timed segments")
    prev_end = 0.0
    for i, s in enumerate(segments):
        if not isinstance(s, dict) or not isinstance(s.get("words"), list) or not s["words"]:
            raise ValueError(f"segment {i}: requires non-empty timed words")
        start, end = float(s.get("start", -1)), float(s.get("end", -1))
        if not (math.isfinite(start) and math.isfinite(end)) or start < 0 or end <= start or start < prev_end - 0.02:
            raise ValueError(f"segment {i}: invalid/nonmonotonic timing")
        if duration is not None and end > duration + 0.15:
            raise ValueError(f"segment {i}: timing exceeds source duration")
        prev_word_end = start
        for j, w in enumerate(s["words"]):
            if not isinstance(w, dict) or not str(w.get("text", "")).strip():
                raise ValueError(f"segment {i} word {j}: missing text")
            a, b = float(w.get("start", -1)), float(w.get("end", -1))
            if not (math.isfinite(a) and math.isfinite(b)) or a < start - 0.02 or b <= a or b > end + 0.02 or a < prev_word_end - 0.02:
                raise ValueError(f"segment {i} word {j}: invalid/nonmonotonic timing")
            prev_word_end = b
        prev_end = end
        s["text"] = str(s.get("text", " ".join(str(w["text"]) for w in s["words"])))
    return segments

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
    ap.add_argument("--prompt"); ap.add_argument("--out"); ap.add_argument("--no-batch", action="store_true", help="the plain (slower) decoder")
    ap.add_argument("--vad", choices=["auto", "on", "off"], default="auto",
                    help="speech filter: auto = on, retried off when it keeps nothing (songs); off for singing over music")
    a = ap.parse_args()
    src = Path(a.src)
    segs = transcribe(src, a.model, None if a.lang == "auto" else a.lang, a.prompt, not a.no_batch,
                      {"auto": None, "on": True, "off": False}[a.vad])
    base = (Path(a.out) if a.out else src.parent) / src.stem
    rep = write_all(segs, base)
    for s in segs:
        print(f"{s['start']:6.2f}–{s['end']:6.2f}  {s['text']}")
    print(json.dumps(rep, ensure_ascii=False))


if __name__ == "__main__":
    main()
