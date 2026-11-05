"""APPX-13 word-timed auto captions with faster-whisper (env_scope=local)."""
from __future__ import annotations
from pathlib import Path
from ._mind_common import eq, truth
from . import _local_models as L


def appx13(work):
    work = Path(work)
    wav = work / "speech.wav"
    L.piper_say(L.LINE_AR, wav)
    words, _ = L.transcribe_words(L.whisper("small"), wav, "ar")
    def ts(x):
        h, r = divmod(x, 3600); m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")
    blocks = [f"{i+1}\n{ts(w['start'])} --> {ts(w['end'])}\n{w['w']}\n" for i, w in enumerate(words)]
    (work / "auto.srt").write_text("\n".join(blocks), encoding="utf-8")
    # burn with an Arabic-capable font to prove the captions render
    font = next((p for p in Path("/home/user/kosif-tool/fonts").rglob("*.ttf")), None) if Path("/home/user/kosif-tool/fonts").is_dir() else None
    out = work / "burned.png"
    L.ffmpeg("-f", "lavfi", "-i", "color=c=black:s=720x400:d=1", "-vf",
             f"subtitles={work / 'auto.srt'}" + (f":fontsdir={font.parent}" if font else ""), "-frames:v", "1", str(out))
    return [eq("one SRT block per word", len(blocks), len(words)),
            truth("planted words heard >= 80%", L.word_match(L.LINE_AR.split(), [w["w"] for w in words]) >= 0.8),
            truth("SRT time format", all("-->" in b and "," in b.split("\n")[1] for b in blocks)),
            truth("burned frame written", out.stat().st_size > 0)]


PROGRAMS = {"APPX-13": appx13}
