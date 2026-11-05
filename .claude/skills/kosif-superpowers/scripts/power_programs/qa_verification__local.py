"""QA-216 sung/spoken-line verification by speech-to-text, with the 75% per-line pass rule (env_scope=local).
Uses local faster-whisper instead of the paid Scribe API named on the card."""
from __future__ import annotations
from pathlib import Path
from ._mind_common import save, eq, truth
from . import _local_models as L


def qa216(work):
    work = Path(work)
    planned = [L.LINE_AR, "سأرفع راية مصر عاليا"]
    wavs = []
    for i, line in enumerate(planned):
        w = work / f"l{i}.wav"; L.piper_say(line, w); wavs.append(w)
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{w}'\n" for w in wavs))
    render = work / "render.wav"
    L.ffmpeg("-f", "concat", "-safe", "0", "-i", str(lst), str(render))
    heard, _ = L.transcribe_words(L.whisper("small"), render, "ar")
    hw = [h["w"] for h in heard]
    # a line that was never in the render must fail the same check
    decoy = "هذا السطر لم يغن ابدا في التسجيل"
    rows = [{"line": l, "match": round(L.word_match(l.split(), hw), 2)} for l in planned + [decoy]]
    for r in rows:
        r["pass"] = r["match"] >= 0.75
    save(work, "lyric_check.json", rows)
    return [truth("both planned lines pass at 75%", rows[0]["pass"] and rows[1]["pass"], rows[:2]),
            eq("decoy line fails", rows[2]["pass"], False)]


PROGRAMS = {"QA-216": qa216}
