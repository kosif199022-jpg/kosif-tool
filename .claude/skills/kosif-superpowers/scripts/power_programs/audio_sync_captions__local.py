"""Local speech programs for the audio-sync-captions family (faster-whisper + Piper, env_scope=local).

Fixture: Piper speaks a planted Arabic line whose words and phoneme timings are the known answer.
"""
from __future__ import annotations
import json
from pathlib import Path
from ._mind_common import save, eq, truth
from . import _local_models as L


def _spoken(work: Path, alignments=False):
    wav = Path(work) / "line.wav"
    secs, words, sr = L.piper_say(L.LINE_AR, wav, alignments=alignments)
    return wav, secs, words


def sync07(work):
    """Arabic word-timed transcription: every planted word heard, in order, with start<end times."""
    wav, secs, _ = _spoken(work)
    words, info = L.transcribe_words(L.whisper("small"), wav, "ar")
    save(work, "words.json", words)
    srt = "\n".join(f"{i+1}\n00:00:{w['start']:06.3f} --> 00:00:{w['end']:06.3f}\n{w['w']}\n".replace(".", ",")
                    for i, w in enumerate(words))
    (Path(work) / "captions.srt").write_text("\ufeff" + srt, encoding="utf-8")
    m = L.word_match(L.LINE_AR.split(), [w["w"] for w in words])
    return [truth("planted words heard >= 80%", m >= 0.8, m),
            truth("times increase", all(a["start"] <= b["start"] for a, b in zip(words, words[1:]))),
            truth("every word has start < end", all(w["start"] < w["end"] for w in words)),
            truth("last word ends inside the audio", words and words[-1]["end"] <= secs + 0.3, secs)]


def sync08(work):
    """The .en trap: an English-only model turns Arabic speech into English; the multilingual one keeps Arabic."""
    wav, _, _ = _spoken(work)
    en, info_en = L.transcribe_words(L.whisper("tiny.en"), wav, None)
    ml, info_ml = L.transcribe_words(L.whisper("small"), wav, "ar")
    has_ar = lambda ws: any("\u0600" <= ch <= "\u06ff" for w in ws for ch in w["w"])
    save(work, "en_trap.json", {"tiny.en": en, "small": ml, "tiny.en_language": info_en.language})
    return [truth(".en output has no Arabic letters", not has_ar(en), " ".join(w["w"] for w in en)),
            truth("multilingual output is Arabic", has_ar(ml), " ".join(w["w"] for w in ml)),
            eq(".en model reports english", info_en.language, "en")]


def sync09(work):
    """True word timing from Piper phonemes, checked against Whisper: one span per word, |delta| small."""
    wav, secs, spans = _spoken(work, alignments=True)
    heard, _ = L.transcribe_words(L.whisper("small"), wav, "ar")
    said = L.LINE_AR.split()
    rows = [{"word": w, "start": round(s["start"], 3), "end": round(s["end"], 3)} for w, s in zip(said, spans)]
    save(work, "words.json", rows)
    deltas = [abs(r["start"] - h["start"]) for r, h in zip(rows, heard)] if len(heard) == len(rows) else []
    return [eq("one phoneme span per planted word", len(spans), len(said)),
            truth("spans in order and inside audio", all(a["end"] <= b["start"] + 1e-6 for a, b in zip(rows, rows[1:]))
                  and rows[-1]["end"] <= secs),
            truth("whisper starts within 0.4 s of phoneme truth (median)", deltas and sorted(deltas)[len(deltas) // 2] < 0.4,
                  [round(d, 3) for d in deltas])]


def sync48(work):
    """Talking-clip reel chain on a planted clip: words -> 1080x1920 frame -> karaoke captions -> -14 LUFS."""
    work = Path(work)
    wav, secs, _ = _spoken(work)
    words, _ = L.transcribe_words(L.whisper("small"), wav, "ar")
    ass = ["[Script Info]", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Alignment, MarginV",
           "Style: K,DejaVu Sans,72,&H0000D7FF,&H00FFFFFF,&H00000000,&H64000000,1,2,320", "", "[Events]",
           "Format: Layer, Start, End, Style, Text"]
    def t(x):
        return f"0:00:{x:05.2f}"
    line = "".join("{\\k%d}%s " % (round((w["end"] - w["start"]) * 100), w["w"]) for w in words)
    ass.append(f"Dialogue: 0,{t(0)},{t(secs)},K,{line}")
    (work / "karaoke.ass").write_text("\n".join(ass) + "\n", encoding="utf-8")
    out = work / "reel.mp4"
    # two-pass loudnorm: one pass undershoots on a clip this short
    import re as _re
    first = L.subprocess.run(["ffmpeg", "-nostdin", "-i", str(wav), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                              "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(_re.findall(r"\{[^{}]*\}", first)[-1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    L.ffmpeg("-f", "lavfi", "-i", f"color=c=0x101820:s=1080x1920:d={secs:.2f}:r=30", "-i", str(wav),
             "-vf", f"ass={work / 'karaoke.ass'}", "-af", ln + ",aresample=48000",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out))
    meas = L.subprocess.run(["ffmpeg", "-nostdin", "-i", str(out), "-af", "ebur128", "-f", "null", "-"],
                            capture_output=True, text=True).stderr
    import re
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", meas)[-1])
    v = [s for s in L.probe(out)["streams"] if s["codec_type"] == "video"][0]
    return [eq("size 1080x1920", (v["width"], v["height"]), (1080, 1920)),
            eq("one karaoke tag per heard word", line.count("{\\k"), len(words)),
            eq("integrated loudness -14 LUFS", lufs, -14.0, tol=1.5),
            truth("planted words heard >= 80%", L.word_match(L.LINE_AR.split(), [w["w"] for w in words]) >= 0.8)]


PROGRAMS = {"SYNC-07": sync07, "SYNC-08": sync08, "SYNC-09": sync09, "SYNC-48": sync48}
