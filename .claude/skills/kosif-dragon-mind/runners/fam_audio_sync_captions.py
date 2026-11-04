"""Runners for the audio-sync-captions family: timed transcripts, alignment, voiced spans, caption pages and styles,
silence detection, joins and muxes. Each card builds a deterministic fixture in wd (synthetic speech-like audio with
known voiced spans, known word timings), runs the repo's own engine where one exists (transcribe.load_transcript,
verse.align / voiced_spans / estimate, montage.word_times / ass, captions_pages.py, silence_cut.py, audio2motion.py,
the HyperFrames CLI) or ffmpeg/numpy for the stated formula, and measures the output against the known answer, with a
negative control on the unprocessed input. Helpers are duplicated from fam_music_beat_sound on purpose (each runner
module loads standalone)."""
import hashlib
import importlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

from _harness import card, check, fx

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]
VSK = SKILLS / "kosif-superpowers/vendor/100-superskills/skills"
VEND = VSK / "kosif-montage-motion/scripts"
ARC = VSK / "audio-reactive-captions-studio/scripts"
PVE = VSK / "pro-video-editor-ffmpeg/scripts"
SR = 48000
GAPS = {}


def vmod(name, where=VEND):
    if str(where) not in sys.path:
        sys.path.insert(0, str(where))
    return importlib.import_module(name)


def sh(cmd, cwd=None, timeout=60, env=None):
    done = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout, cwd=cwd,
                          stdin=subprocess.DEVNULL, env=env)
    if done.returncode:
        raise RuntimeError("command failed (%d): %s %s" % (done.returncode, " ".join(map(str, cmd[:3])), (done.stderr or done.stdout)[-400:]))
    return done.stdout


def ff(*args):
    sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args])


def ffe(*args):
    """ffmpeg run whose stderr (filter logs) is returned."""
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *map(str, args)], capture_output=True, text=True).stderr


def tt(secs, sr=SR):
    return np.arange(int(round(secs * sr))) / sr


def save(wd, name, x, sr=SR):
    p = Path(wd) / name
    fx.write_wav(p, np.clip(np.asarray(x, float), -1, 1), sr)
    return p


def load_any(p, sr=SR):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(float), sr


def dbfs(x):
    return 20 * math.log10(math.sqrt(float(np.mean(np.square(x)))) + 1e-12)


def seg_db(x, sr, a, b):
    return dbfs(x[int(a * sr):max(int(a * sr) + 1, int(b * sr))])


def band_db(x, sr, lo, hi):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / sr)
    m = (f >= lo) & (f < hi)
    return 10 * math.log10(float(X[m].sum()) + 1e-20)


def speechlike(secs, spans, f0=170.0, amp=0.3, sr=SR, seed=4):
    """Voiced spans of a harmonic buzz with a syllable-rate (5 Hz) envelope; digital silence elsewhere."""
    t = tt(secs, sr)
    x = sum(np.sin(2 * np.pi * f0 * k * t) / k for k in range(1, 8))
    syl = 0.6 + 0.4 * np.sin(2 * np.pi * 5 * t) ** 2
    gate = np.zeros_like(t)
    for a, b in spans:
        gate[(t >= a) & (t < b)] = 1
    ramp = int(0.01 * sr)
    gate = np.convolve(gate, np.ones(ramp) / ramp, mode="same")
    return amp * x / np.abs(x).max() * syl * gate


def jdump(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(p)


def probe_dur(p):
    return float(fx.probe(p)["format"]["duration"])


WORDS = [("مرحبا", 0.50, 0.90), ("بكم", 0.95, 1.30), ("في", 1.35, 1.50), ("البرنامج", 1.55, 2.20),
         ("اليوم", 2.80, 3.20), ("نتكلم", 3.25, 3.70), ("عن", 3.75, 3.90), ("الصوت", 3.95, 4.50)]
SPANS = [(0.5, 2.2), (2.8, 4.5)]


def segs_of(words=WORDS):
    a, b = words[:4], words[4:]
    return [{"start": s[0][1], "end": s[-1][2], "text": " ".join(w for w, _, _ in s),
             "words": [{"text": w, "start": x, "end": y} for w, x, y in s]} for s in (a, b)]


# ───────────────────────── transcripts and alignment ─────────────────────────
@card("SYNC-06")
def pretimed_transcript(task, wd):
    """transcribe.load_transcript(NAME.words.json, duration): accepts tool-made timed words; rejects > 10 MB, > 20,000 segments,
    non-monotonic timing (0.02 s tolerance), words outside their segment, and ends past duration + 0.15 s."""
    T = vmod("transcribe")
    good = jdump(Path(wd) / "talk.words.json", segs_of())
    segs = T.load_transcript(good, duration=4.6)
    bad_cases = {
        "end past duration": (segs_of(), 4.3),
        "non-monotonic segments": ([segs_of()[1], segs_of()[0]], 4.6),
        "word outside its segment": ([dict(segs_of()[0], words=[{"text": "x", "start": 0.1, "end": 0.3}])], 4.6),
        "plain text, no times": ([{"text": "مرحبا بكم"}], 4.6),
    }
    rejected = {}
    for name, (obj, dur) in bad_cases.items():
        p = jdump(Path(wd) / ("bad_%d.json" % len(rejected)), obj)
        try:
            T.load_transcript(p, duration=dur)
            rejected[name] = False
        except ValueError:
            rejected[name] = True
    ok_edge = jdump(Path(wd) / "edge.json", segs_of())
    edge = len(T.load_transcript(ok_edge, duration=4.36)) == 2                # 4.5 ≤ 4.36 + 0.15 → still accepted
    return [check("valid words.json loads with segment text", len(segs) == 2 and segs[0]["text"] == "مرحبا بكم في البرنامج", [s["text"] for s in segs], 2),
            check("end within duration + 0.15 s accepted", edge, edge, True),
            check("negative control: every malformed transcript is rejected", all(rejected.values()), rejected, "all rejected")], [good]


@card("SYNC-10")
def true_text_alignment(task, wd):
    """verse.align(lines, asr): difflib on normalised words; equal / one-to-one blocks take the ASR word's time, a missed word
    sits between its timed neighbours (step ≥ 0.05 s, min word 0.05 s); verse.segment caps lines at 7 words."""
    VS = vmod("verse")
    asr = [{"text": w, "start": a, "end": b} for w, a, b in WORDS]
    asr[3] = dict(asr[3], text="البرنامح")                                 # one misrecognised word (one-to-one replace)
    del asr[6]                                                              # one word the ASR missed ("عن")
    lines = [[w for w, _, _ in WORDS[:4]], [w for w, _, _ in WORDS[4:]]]
    out = VS.align(lines, asr)
    jdump(Path(wd) / "aligned.json", out)
    flat = [w for ln in out for w in ln]
    exact = all(abs(flat[i]["start"] - WORDS[i][1]) < 1e-6 for i in (0, 1, 2, 3, 4, 5, 7))
    missed = flat[6]
    long = [{"text": "w%d" % i, "start": i * 0.3, "end": i * 0.3 + 0.25} for i in range(12)]
    segd = VS.segment(long)
    raw_text = [w["text"] for w in asr]
    return [check("true words inherit ASR times (equal + one-to-one replace)", exact, [w["start"] for w in flat], [w[1] for w in WORDS]),
            check("missed word placed between its neighbours", flat[5]["end"] <= missed["start"] + 1e-6 and missed["end"] <= flat[7]["start"] + 1e-6 and missed["end"] - missed["start"] >= 0.05,
                  missed, "between 3.70 and 3.95"),
            check("true spelling kept (البرنامج, not the ASR's)", flat[3]["text"] == "البرنامج", flat[3]["text"], "البرنامج"),
            check("segment() keeps lines ≤ 7 words", all(len(s) <= 7 for s in segd) and sum(len(s) for s in segd) == 12, [len(s) for s in segd], "≤ 7"),
            check("negative control: the raw ASR text differs from the true lines", raw_text != [w for w, _, _ in WORDS], len(raw_text), 8)], [Path(wd) / "aligned.json"]


@card("SYNC-17")
def voiced_span_estimate(task, wd):
    """verse.voiced_spans: 50 ms frames, threshold max(−45 dB, p20 + 6 dB), merge gaps < 0.35 s, keep spans > 0.15 s;
    estimate() lays the text's words over those spans by length (marked estimated)."""
    VS = vmod("verse")
    spans = [(0.5, 1.4), (1.6, 2.2), (2.8, 4.5)]                            # 0.2 s breath inside the first phrase
    p = save(wd, "voice.wav", speechlike(5.0, spans))
    got = VS.voiced_spans(p)
    lines = [[w for w, _, _ in WORDS[:4]], [w for w, _, _ in WORDS[4:]]]
    est = VS.estimate(lines, p)
    jdump(Path(wd) / "estimated.json", est)
    flat = [w for ln in est for w in ln]
    y, _ = load_any(p)
    hop = int(0.05 * SR)
    lv = np.array([dbfs(y[i:i + hop]) for i in range(0, len(y) - hop, hop)])
    on = lv > max(-45.0, float(np.percentile(lv, 20)) + 6)
    raw_n = int(on[0]) + int(np.sum(on[1:] & ~on[:-1]))
    inside = all(any(a - 0.06 <= w["start"] <= b for a, b in got) for w in flat) and all(u["start"] < v["start"] for u, v in zip(flat, flat[1:]))
    return [check("two phrases found (breath < 0.35 s merged)", len(got) == 2, got, [(0.5, 2.2), (2.8, 4.5)]),
            check("span edges within one 50 ms frame", len(got) == 2 and max(abs(a - b) for g, e in zip(got, SPANS) for a, b in zip(g, e)) <= 0.06, got, SPANS),
            check("every estimated word starts inside a voiced span, in order", inside, [(w["start"], w["end"]) for w in flat][:4], "inside"),
            check("negative control: the same 50 ms threshold without the merge rule splits the phrase (3 raw spans)", raw_n == 3, raw_n, 3)], [Path(wd) / "estimated.json"]


@card("SYNC-18")
def word_times_by_length(task, wd):
    """montage.word_times(cap): words of a line share its span with weight = len(word) + 2; given word times pass through."""
    M = vmod("montage")
    cap = {"text": "أ بب تتتت ثثثثثثثث", "start": 1.0, "end": 3.0}
    wt = M.word_times(cap)
    jdump(Path(wd) / "word_times.json", wt)
    w = np.array([len(x) + 2 for x in cap["text"].split()], float)
    want = 2.0 * w / w.sum()
    got = np.array([b - a for _, a, b in wt])
    given = M.word_times({"text": "x y", "start": 0, "end": 1, "words": [{"text": "x", "start": 0.1, "end": 0.4}, {"text": "y", "start": 0.6, "end": 0.9}]})
    return [check("durations ∝ len + 2", np.allclose(got, want, atol=1e-5), got.round(4).tolist(), want.round(4).tolist()),
            check("words tile the line span", abs(wt[0][1] - 1.0) < 1e-6 and abs(wt[-1][2] - 3.0) < 1e-5, [wt[0][1], wt[-1][2]], [1.0, 3.0]),
            check("given word times are kept", given == [("x", 0.1, 0.4), ("y", 0.6, 0.9)], given, "kept"),
            check("negative control: an even split would not match", not np.allclose(got, np.full(4, 0.5), atol=1e-3), got.round(3).tolist(), "≠ 0.5 each")], [Path(wd) / "word_times.json"]


@card("SYNC-15")
def hf_transcript_import(task, wd):
    """npx hyperframes transcribe <existing .srt> normalises an existing transcript into a word array (no model needed);
    exporting back with --to vtt. (Transcribing raw audio needs Whisper weights: not exercised here.)"""
    srt = Path(wd) / "talk.srt"
    srt.write_text("1\n00:00:00,500 --> 00:00:02,200\nمرحبا بكم في البرنامج\n\n2\n00:00:02,800 --> 00:00:04,500\nاليوم نتكلم عن الصوت\n", encoding="utf-8")
    env = dict(os.environ, DO_NOT_TRACK="1")
    res = json.loads(sh(["hyperframes", "transcribe", srt, "--json", "--dir", wd], cwd=wd, env=env))
    tr = json.loads(Path(res["transcriptPath"]).read_text(encoding="utf-8"))
    vtt = Path(wd) / "talk.vtt"
    sh(["hyperframes", "transcribe", res["transcriptPath"], "--to", "vtt", "-o", vtt, "--dir", wd], cwd=wd, env=env)
    v = vtt.read_text(encoding="utf-8")
    bad = Path(wd) / "bad.srt"
    bad.write_text("not a transcript\n", encoding="utf-8")
    r2 = subprocess.run(["hyperframes", "transcribe", str(bad), "--json", "--dir", str(wd)], capture_output=True, text=True, env=env, cwd=wd)
    return [check("srt imported: 2 timed entries with their text", res["ok"] and [(w["start"], w["end"]) for w in tr] == [(0.5, 2.2), (2.8, 4.5)], [(w["start"], w["end"], w["text"]) for w in tr], [(0.5, 2.2), (2.8, 4.5)]),
            check("VTT export carries the cue times", v.startswith("WEBVTT") and "00:00:02.800" in v and "الصوت" in v, v[:80], "WEBVTT"),
            check("negative control: a non-transcript file is not imported", r2.returncode != 0 or '"ok":true' not in r2.stdout.replace(" ", ""), r2.returncode, "failure")], [vtt, Path(res["transcriptPath"])]


# ───────────────────────── STT prep, silence, joins, mux ─────────────────────────
@card("SYNC-13")
def stt_prep(task, wd):
    """STT prep: highpass 200 / lowpass 3000, 16 kHz mono PCM. Timing trap: silence removal shifts every later word, so words
    are taken from the untouched timeline."""
    t = tt(4.5)
    x = speechlike(4.5, SPANS) + 0.05 * np.sin(2 * np.pi * 60 * t) + 0.05 * np.sin(2 * np.pi * 6000 * t)
    src = save(wd, "talk.wav", x)
    prep = Path(wd) / "stt.wav"
    ff("-i", src, "-af", "highpass=f=200,lowpass=f=3000", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", prep)
    st = fx.probe(prep)["streams"][0]
    y, _ = load_any(prep, 16000)
    x16, _ = load_any(src, 16000)
    hum = band_db(y, 16000, 50, 70) - band_db(x16, 16000, 50, 70)
    hiss = band_db(y, 16000, 5800, 6200) - band_db(x16, 16000, 5800, 6200)
    cut = Path(wd) / "stt_silence_removed.wav"
    ff("-i", prep, "-af", "silenceremove=stop_periods=-1:stop_duration=0.2:stop_threshold=-30dB", cut)
    def second_onset(s, sr):
        e = np.array([np.abs(s[i:i + 160]).max() for i in range(0, len(s) - 160, 160)])
        quiet = np.flatnonzero((e < 0.02) & (np.arange(len(e)) > 150))[0]
        return (quiet + np.flatnonzero(e[quiet:] > 0.02)[0]) * 0.01
    on_prep = second_onset(y, 16000)
    z, _ = load_any(cut, 16000)
    on_cut = second_onset(z, 16000)
    return [check("16 kHz mono 16-bit", st["sample_rate"] == "16000" and st["channels"] == 1 and st["codec_name"] == "pcm_s16le", [st["sample_rate"], st["channels"]], ["16000", 1]),
            check("60 Hz hum cut by >= 15 dB, 6 kHz hiss by >= 10 dB (2-pole filters)", hum <= -15 and hiss <= -10, [hum, hiss], "<= -15 / -10"),
            check("prepped file keeps the second phrase at 2.8 s (±20 ms)", abs(on_prep - 2.8) < 0.02, on_prep, 2.8),
            check("negative control: in the silence-removed copy the phrase starts early (> 0.2 s), so its times are not the source's", on_cut < 2.8 - 0.2, on_cut, "< 2.6")], [prep]


def _silences(stderr):
    s = [float(v) for v in re.findall(r"silence_start: (-?[\d.]+)", stderr)]
    e = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", stderr)]
    return list(zip(s, e))


@card("SYNC-53")
def silence_detection(task, wd):
    """Fixed: silencedetect=n=-35dB:d=0.5; adaptive: loudnorm print_format=json → input_thresh → silencedetect; EDL writer
    silence_cut.py --db -35 --min 0.6 --pad 0.12."""
    voice = speechlike(5.0, [(0.3, 1.0), (2.0, 3.2), (3.5, 4.6)]) + 10 ** (-60 / 20) * np.random.default_rng(1).standard_normal(int(5 * SR))
    p = save(wd, "talk.wav", voice)
    fixed = _silences(ffe("-i", p, "-af", "silencedetect=n=-35dB:d=0.5", "-f", "null", "-"))
    err = ffe("-i", p, "-af", "loudnorm=print_format=json", "-f", "null", "-")
    thr = float(json.loads(err[err.rindex("{"):err.rindex("}") + 1])["input_thresh"])
    adapt = _silences(ffe("-i", p, "-af", "silencedetect=noise=%sdB:d=0.5" % thr, "-f", "null", "-"))
    edl = Path(wd) / "edl.json"
    sh([sys.executable, PVE / "silence_cut.py", p, "--db", "-35", "--min", "0.6", "--pad", "0.12", "--out", edl], cwd=wd)
    e = json.loads(edl.read_text())
    keep = [[c["in"], c["out"]] for c in e["clips"]]
    return [check("fixed: the 1.0 s gap reported 1.0-2.0 s (±20 ms); the 0.3 s gap ignored", len(fixed) == 1 and abs(fixed[0][0] - 1.0) < 0.02 and abs(fixed[0][1] - 2.0) < 0.02, fixed, [(1.0, 2.0)]),
            check("adaptive threshold from loudnorm finds the same gap", any(abs(a - 1.0) < 0.05 and abs(b - 2.0) < 0.05 for a, b in adapt), [thr, adapt], "1.0-2.0"),
            check("EDL keeps speech with 0.12 s pads around the gap", any(abs(k[1] - 1.12) < 0.02 for k in keep) and any(abs(k[0] - 1.88) < 0.02 for k in keep), keep, "[..1.12] [1.88..]"),
            check("negative control: the same detector on unbroken speech finds no silence",
                  not _silences(ffe("-i", save(wd, "solid.wav", speechlike(3.0, [(0, 3.0)])), "-af", "silencedetect=n=-35dB:d=0.5", "-f", "null", "-")), 0, 0)], [edl]


@card("SYNC-54")
def joined_audio_drift(task, wd):
    """MP3 joins add ~a frame of padding each (1152/576-sample frames); verify joined duration vs the sum of parts, and join
    as PCM/WAV then encode once."""
    parts, total = [], 0.0
    for i in range(20):
        d = 0.3 + 0.01 * i
        x = speechlike(d, [(0.02, d - 0.02)], f0=150 + 5 * i, sr=24000)
        w = save(wd, "p%02d.wav" % i, x, 24000)
        m = Path(wd) / ("p%02d.mp3" % i)
        ff("-i", w, "-c:a", "libmp3lame", "-b:a", "64k", "-ar", "24000", "-ac", "1", m)
        parts.append((w, m))
        total += len(x) / 24000
    for k, ext in ((0, "wav"), (1, "mp3")):
        (Path(wd) / ("list_%s.txt" % ext)).write_text("".join("file '%s'\n" % p[k].name for p in parts))
    jw, jm = Path(wd) / "joined.wav", Path(wd) / "joined_mp3.mp3"
    ff("-f", "concat", "-safe", "0", "-i", Path(wd) / "list_wav.txt", "-c", "copy", jw)
    ff("-f", "concat", "-safe", "0", "-i", Path(wd) / "list_mp3.txt", "-c", "copy", jm)
    once = Path(wd) / "joined_once.mp3"
    ff("-i", jw, "-c:a", "libmp3lame", "-b:a", "64k", "-write_xing", "0", once)
    dw = len(load_any(jw, 24000)[0]) / 24000 - total
    dm = len(load_any(jm, 24000)[0]) / 24000 - total
    d1 = len(load_any(once, 24000)[0]) / 24000 - total
    return [check("WAV join drift < 1 ms over 20 parts", abs(dw) < 0.001, dw, "< 0.001"),
            check("encode-once MP3: one fixed encoder delay only (< 0.1 s), not per join", abs(d1) < 0.1, d1, "< 0.1"),
            check("negative control: stream-joining 20 MP3 parts drifts > 0.3 s (padding per join)", dm > 0.3, dm, "> 0.3")], [jw, once]


@card("SYNC-56")
def concat_with_original_audio(task, wd):
    """ffmpeg -f concat -i concat.txt -i song -map 0:v:0 -map 1:a:0 -t DUR -c:v copy -c:a aac; gentle edge fades only if asked
    (in 0.3 s, out 1.3 s); record the source audio's sha256."""
    clips = []
    for i, c in enumerate(("red", "green", "blue")):
        v = Path(wd) / ("c%d.mp4" % i)
        ff("-f", "lavfi", "-i", "color=c=%s:s=96x54:r=30:d=1.5" % c, "-c:v", "libx264", "-pix_fmt", "yuv420p", v)
        clips.append(v)
    (Path(wd) / "concat.txt").write_text("".join("file '%s'\n" % v.name for v in clips))
    song = save(wd, "song.wav", 0.4 * np.sin(2 * np.pi * 440 * tt(6.0)))
    sha = hashlib.sha256(song.read_bytes()).hexdigest()
    out = Path(wd) / "film.mp4"
    ff("-f", "concat", "-safe", "0", "-i", Path(wd) / "concat.txt", "-i", song, "-map", "0:v:0", "-map", "1:a:0", "-t", "4.5",
       "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "afade=t=in:d=0.3,afade=t=out:st=3.2:d=1.3", out)
    jdump(Path(wd) / "audio_source.json", {"source": song.name, "sha256": sha})
    a, _ = load_any(out)
    f = np.abs(np.fft.rfft(a[int(1 * SR):int(2 * SR)]))
    peak = np.fft.rfftfreq(SR, 1 / SR)[np.argmax(f)]
    st = {s["codec_type"]: s for s in fx.probe(out)["streams"]}
    return [check("video stream copied from the concat (h264), audio from the song (aac)", st["video"]["codec_name"] == "h264" and st["audio"]["codec_name"] == "aac", [st["video"]["codec_name"], st["audio"]["codec_name"]], ["h264", "aac"]),
            check("audio is the song (440 Hz) cut at -t 4.5 s", abs(peak - 440) < 2 and abs(probe_dur(out) - 4.5) < 0.1, [peak, probe_dur(out)], [440, 4.5]),
            check("fade-in 0.3 s: first 30 ms far below 1-2 s", seg_db(a, SR, 0.0, 0.03) < seg_db(a, SR, 1, 2) - 15, seg_db(a, SR, 0.0, 0.03), "faded"),
            check("source sha256 recorded and matches the file", json.loads((Path(wd) / "audio_source.json").read_text())["sha256"] == hashlib.sha256(song.read_bytes()).hexdigest(), sha[:12], "match"),
            check("negative control: the clips alone have no audio stream", all(all(s["codec_type"] != "audio" for s in fx.probe(c)["streams"]) for c in clips), 0, "no audio")], [out]


# ───────────────────────── caption files and pages ─────────────────────────
def srt_time(t):
    ms = int(round(t * 1000))
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


@card("SYNC-25")
def verbatim_soft_track(task, wd):
    """Caption text diffed against words.json in QA; deliverables .srt + .vtt; soft track inside MP4 with
    -c:s mov_text -metadata:s:s:0 language=ara (not burned)."""
    segs = segs_of()
    srt = Path(wd) / "talk.srt"
    srt.write_text("".join("%d\n%s --> %s\n%s\n\n" % (i + 1, srt_time(s["start"]), srt_time(s["end"]), s["text"]) for i, s in enumerate(segs)), encoding="utf-8")
    vtt = Path(wd) / "talk.vtt"
    ff("-i", srt, vtt)
    v = Path(wd) / "talk.mp4"
    ff("-f", "lavfi", "-i", "color=c=black:s=96x54:r=30:d=5", "-i", srt, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:s", "mov_text", "-metadata:s:s:0", "language=ara", v)
    subs = [s for s in fx.probe(v)["streams"] if s["codec_type"] == "subtitle"]
    back = Path(wd) / "back.srt"
    ff("-i", v, "-map", "0:s:0", back)
    cap_words = re.sub(r"\d+\n[\d:,]+ --> [\d:,]+\n", "", back.read_text(encoding="utf-8")).split()
    truth = [w for w, _, _ in WORDS]
    para = cap_words[:3] + ["البرامج"] + cap_words[4:]
    return [check("soft mov_text track tagged 'ara'", len(subs) == 1 and subs[0]["codec_name"] == "mov_text" and subs[0].get("tags", {}).get("language") == "ara", [(s["codec_name"], s.get("tags", {}).get("language")) for s in subs], ("mov_text", "ara")),
            check("VTT written with cue times", vtt.read_text(encoding="utf-8").startswith("WEBVTT") and "00:02.800" in vtt.read_text(encoding="utf-8"), "WEBVTT", "WEBVTT"),
            check("verbatim: caption words read back from the MP4 equal words.json", cap_words == truth, cap_words, truth),
            check("negative control: a paraphrased caption fails the diff", para != truth, para[3], "≠ البرنامج")], [v, srt, vtt]


@card("SYNC-29")
def caption_pages_script(task, wd):
    """captions_pages.py words.json --page-ms 1200 --max-chars 42 --rtl --out captions → JSON/SRT/VTT/ASS pages; expects
    [{text,start,end}] (a KOSIF {word,…} file must be renamed first)."""
    words = [{"text": w, "start": a, "end": b} for w, a, b in WORDS]
    wj = jdump(Path(wd) / "words.json", words)
    sh([sys.executable, ARC / "captions_pages.py", wj, "--page-ms", "1200", "--max-chars", "42", "--rtl", "--out", Path(wd) / "captions"], cwd=wd)
    files = sorted(p.name for p in Path(wd).glob("captions*"))
    js = next(Path(wd).glob("captions*.json"))
    pages = json.loads(js.read_text(encoding="utf-8"))
    pages = pages.get("pages", pages) if isinstance(pages, dict) else pages
    span = lambda p: (p["endMs"] - p["startMs"]) / 1000
    texts = [p.get("text", "") for p in pages]
    kw = jdump(Path(wd) / "kosif.words.json", [{"word": w, "start": a, "end": b} for w, a, b in WORDS])
    r = subprocess.run([sys.executable, str(ARC / "captions_pages.py"), str(kw), "--out", str(Path(wd) / "kx")], capture_output=True, text=True, cwd=wd)
    return [check("4 files (json, srt, vtt, ass)", len(files) >= 4, files, ">= 4"),
            check("every page <= 42 chars and the words all present in order", all(len(t) <= 42 for t in texts) and " ".join(texts).split() == [w for w, _, _ in WORDS], texts, "8 words"),
            check("page 2 starts at the 2.8 s word after the pause; pages last <= 7 s", len(pages) == 2 and pages[1]["startMs"] == 2800 and all(0 < span(p) <= 7 for p in pages), [(p["startMs"], p["endMs"]) for p in pages], "2 pages"),
            check("negative control: a {word,…} KOSIF file is refused (KeyError 'text')", r.returncode != 0 and "text" in r.stderr, r.returncode, "error")], [Path(wd) / f for f in files]


@card("SYNC-21")
def caption_pages_1200ms(task, wd):
    """Group tokens into pages: combine tokens while the page is within 1200 ms (createTikTokStyleCaptions
    combineTokensWithinMilliseconds), new page after a pause > 150 ms; one page visible at a time; ≤ 6 Arabic words."""
    def pages_of(words, combine=1.2, pause=0.15, cap=6):
        pages = []
        for w, a, b in words:
            if pages and a - pages[-1]["end"] <= pause and b - pages[-1]["start"] <= combine and len(pages[-1]["words"]) < cap:
                pages[-1]["words"].append(w)
                pages[-1]["end"] = b
            else:
                pages.append({"words": [w], "start": a, "end": b})
        return pages
    pg = pages_of(WORDS)
    out = jdump(Path(wd) / "pages.json", pg)
    overlap = any(p["end"] > q["start"] for p, q in zip(pg, pg[1:]))
    return [check("every page spans <= 1.2 s", all(p["end"] - p["start"] <= 1.2 + 1e-9 for p in pg), [round(p["end"] - p["start"], 2) for p in pg], "<= 1.2"),
            check("the 0.6 s pause starts a new page", any(p["start"] == 2.8 for p in pg), [p["start"] for p in pg], "2.8 starts"),
            check("one page at a time (no overlaps), all 8 words kept", not overlap and sum(len(p["words"]) for p in pg) == 8, len(pg), "no overlap"),
            check("negative control: without grouping every word is its own page", len(pages_of(WORDS, combine=0)) == 8 and len(pg) < 8, len(pg), "< 8")], [out]


@card("SYNC-20")
def timestamped_script_parser(task, wd):
    """parseTimestamps: ^(\\d+(\\.\\d+)?)\\s*[–—-]\\s*(\\d+(\\.\\d+)?)s?\\s*:\\s*(.+)$ per line; clip index = floor(start / clip length)."""
    rx = re.compile(r"^(\d+(\.\d+)?)\s*[–—-]\s*(\d+(\.\d+)?)s?\s*:\s*(.+)$")
    script = "0-3s: افتتاح\n3 – 7.5s : المشكلة\n7.5—12: الحل\nملاحظة بلا وقت\n12-15s:الخاتمة"
    rows = [(float(m.group(1)), float(m.group(3)), m.group(5).strip()) for m in (rx.match(l.strip()) for l in script.splitlines()) if m]
    clip_len = 5.0
    idx = [int(math.floor(a / clip_len)) for a, _, _ in rows]
    out = jdump(Path(wd) / "timed_script.json", [{"start": a, "end": b, "text": t, "clip": i} for (a, b, t), i in zip(rows, idx)])
    return [check("4 timed lines parsed (hyphen, en dash, em dash, optional s)", [(a, b) for a, b, _ in rows] == [(0, 3), (3, 7.5), (7.5, 12), (12, 15)], [(a, b) for a, b, _ in rows], "4 rows"),
            check("text after the colon kept", [t for *_, t in rows] == ["افتتاح", "المشكلة", "الحل", "الخاتمة"], [t for *_, t in rows], "texts"),
            check("clip index floor(start/5)", idx == [0, 0, 1, 2], idx, [0, 0, 1, 2]),
            check("negative control: an untimed line does not match", rx.match("ملاحظة بلا وقت") is None, None, None)], [out]


@card("SYNC-26")
def automatic_emphasis(task, wd):
    """autoEm stars words with a digit; loudPeaks: 0.25 s smoothed dB envelope, local maxima ≥ 4 dB above the median within
    ±3 s, ≥ 1.2 s apart, 3-12 per clip."""
    secs = 10.0
    x = speechlike(secs, [(0.2, 9.8)], amp=0.1)
    loud = [1.5, 3.4, 6.0, 8.2]
    t = tt(secs)
    for c in loud:
        x *= 1 + 2.5 * np.exp(-((t - c) / 0.15) ** 2)
    p = save(wd, "talk.wav", x)
    y, _ = load_any(p)
    hop = int(0.05 * SR)
    lv = np.array([dbfs(y[i:i + hop]) for i in range(0, len(y) - hop, hop)])
    k = 5
    sm = np.convolve(lv, np.ones(k) / k, mode="same")
    peaks = []
    for i in range(1, len(sm) - 1):
        lo, hi = max(0, i - 60), min(len(sm), i + 60)
        if sm[i] >= sm[i - 1] and sm[i] > sm[i + 1] and sm[i] >= np.median(sm[lo:hi]) + 4:
            ti = i * 0.05
            if not peaks or ti - peaks[-1] >= 1.2:
                peaks.append(ti)
    peaks = peaks[:12]
    em = ["*%s*" % w if re.search(r"[\d٠-٩]", w) else w for w in "وفرنا 30 بالمية في ٣ شهور".split()]
    out = jdump(Path(wd) / "emphasis.json", {"peaks": peaks, "words": em})
    flat = save(wd, "flat.wav", speechlike(secs, [(0.2, 9.8)], amp=0.1))
    fl, _ = load_any(flat)
    fv = np.convolve(np.array([dbfs(fl[i:i + hop]) for i in range(0, len(fl) - hop, hop)]), np.ones(k) / k, mode="same")
    flat_peaks = sum(1 for i in range(1, len(fv) - 1) if fv[i] >= fv[i - 1] and fv[i] > fv[i + 1] and fv[i] >= np.median(fv[max(0, i - 60):i + 60]) + 4)
    return [check("the 4 loud moments found (±0.15 s), 3-12 per clip", len(peaks) == 4 and max(abs(a - b) for a, b in zip(peaks, loud)) <= 0.15, peaks, loud),
            check("peaks >= 1.2 s apart", all(b - a >= 1.2 for a, b in zip(peaks, peaks[1:])), np.diff(peaks).tolist(), ">= 1.2"),
            check("digits starred (Latin and Arabic-Indic)", em == ["وفرنا", "*30*", "بالمية", "في", "*٣*", "شهور"], em, "30 and ٣ starred"),
            check("negative control: an even-level clip has no ≥ 4 dB peaks", flat_peaks == 0, flat_peaks, 0)], [out]


@card("SYNC-27")
def ass_karaoke_per_word(task, wd):
    """montage.ass(spec, W, H, style): one Dialogue per word with the highlight colour and a 112 % → 100 % pop in 120 ms
    (\\fscx112\\fscy112\\t(0,120,…)); Encoding −1 for libass paragraph direction; ≤ max words per screen."""
    M = vmod("montage")
    spec = [{"text": " ".join(w for w, _, _ in WORDS[:4]), "start": 0.5, "end": 2.2, "words": [{"text": w, "start": a, "end": b} for w, a, b in WORDS[:4]]}]
    txt = M.ass(spec, 1080, 1920, "reels")
    p = Path(wd) / "caps.ass"
    p.write_text(txt, encoding="utf-8")
    dia = [l for l in txt.splitlines() if l.startswith("Dialogue:")]
    style = next(l for l in txt.splitlines() if l.startswith("Style:"))
    pops = [l for l in dia if re.search(r"\\fscx1\d\d\\fscy1\d\d\\t\(0,\d+,\\fscx100\\fscy100\)", l)]
    starts = [l.split(",")[1] for l in dia]
    return [check("one Dialogue per word", len(dia) == 4, len(dia), 4),
            check("each word event pops back to 100 %", len(pops) == 4, len(pops), 4),
            check("events start at the words' times", starts == ["0:00:00.50", "0:00:00.95", "0:00:01.35", "0:00:01.55"], starts, "word starts"),
            check("style Encoding −1 and PlayRes = frame", style.rstrip().endswith(",-1") and "PlayResX: 1080" in txt and "PlayResY: 1920" in txt, style[-20:], "-1"),
            check("negative control: a plain SRT has no per-word pop", "\\fscx" not in "1\n00:00:00,500 --> 00:00:02,200\n" + spec[0]["text"], 0, 0)], [p]


@card("SYNC-28")
def seven_caption_styles(task, wd):
    """montage.ass(spec, W, H, style) for the seven named styles: colours as ASS &HAABBGGRR; sizes per 1080 px of the short side,
    margins per 1920 of height."""
    M = vmod("montage")
    spec = [{"text": "مرحبا بكم", "start": 0.5, "end": 1.3}]
    styles = list(M.STYLES)
    rows, outs = {}, []
    for st in styles:
        for (W, H) in ((1080, 1920), (540, 960)):
            txt = M.ass(spec, W, H, st)
            line = next(l for l in txt.splitlines() if l.startswith("Style:")).split(",")
            rows[(st, W)] = (int(line[2]), int(line[-2]), line[3])
        p = Path(wd) / ("%s.ass" % st)
        p.write_text(M.ass(spec, 1080, 1920, st), encoding="utf-8")
        outs.append(p)
    half = all(abs(rows[(s, 540)][0] - rows[(s, 1080)][0] / 2) <= 1 for s in styles)
    mv = all(abs(rows[(s, 540)][1] - rows[(s, 1080)][1] / 2) <= 1 for s in styles)
    col = all(re.fullmatch(r"&H[0-9A-Fa-f]{8}", rows[(s, 1080)][2]) for s in styles)
    sizes = {s: rows[(s, 1080)][0] for s in styles}
    return [check("seven named styles", len(styles) >= 7, styles, ">= 7"),
            check("font size scales with the short side (540 → half)", half, {s: (rows[(s, 1080)][0], rows[(s, 540)][0]) for s in styles}, "half"),
            check("MarginV scales with height (960 → half)", mv, {s: (rows[(s, 1080)][1], rows[(s, 540)][1]) for s in styles}, "half"),
            check("primary colours in &HAABBGGRR", col, {s: rows[(s, 1080)][2] for s in styles}, "&HAABBGGRR"),
            check("negative control: the styles are not one size", len(set(sizes.values())) > 1, sizes, "> 1 distinct")], outs


@card("SYNC-39")
def grapheme_typewriter(task, wd):
    """Voice-timed typewriter: letters ~30-50 ms each inside [start, end]; Arabic typed by grapheme clusters (Intl.Segmenter),
    never by code unit, so a letter keeps its harakat."""
    word = "مُحَمَّدٌ"
    js = Path(wd) / "seg.cjs"
    js.write_text("const s=new Intl.Segmenter('ar',{granularity:'grapheme'});const w=%s;"
                  "console.log(JSON.stringify({g:[...s.segment(w)].map(x=>x.segment),u:w.split('')}));" % json.dumps(word), encoding="utf-8")
    r = json.loads(sh(["node", js], cwd=wd))
    g, u = r["g"], r["u"]
    start, end = 1.0, 1.0 + 0.04 * len(g)
    sched = [{"text": "".join(g[:k + 1]), "t": round(start + k * (end - start) / len(g), 4)} for k in range(len(g))]
    out = jdump(Path(wd) / "typewriter.json", sched)
    lonely = lambda parts: any(re.fullmatch(r"[\u064B-\u0652]+", p) for p in parts)
    step = (end - start) / len(g)
    return [check("4 grapheme clusters (each letter with its harakat)", len(g) == 4 and "".join(g) == word, g, 4),
            check("30-50 ms per letter inside [start, end]", 0.03 <= step <= 0.05 and sched[-1]["t"] < end, step, "0.03-0.05"),
            check("no frame shows a bare haraka", not lonely(g), False, False),
            check("negative control: code-unit typing leaves bare harakat (%d units)" % len(u), lonely(u) and len(u) > len(g), len(u), "> 4")], [out]


@card("SYNC-16")
def retake_detection(task, wd):
    """Retakes: sentences whose first 10 normalised characters repeat within 60 s are takes of one line; the last take is the
    default, earlier ones go to the 'unused sentences' list; the hook beat must pose the question within 10 s."""
    sents = [(2.0, "ليه الصوت مهم في الفيديو؟"), (6.0, "ليه الصوت مهم في الفيديو يا جماعة؟"), (12.0, "لأن العين تسامح والأذن لا."),
             (20.0, "خلينا نبدأ بالميكروفون."), (95.0, "ليه الصوت مهم في الفيديو؟ ملخص")]
    norm = lambda s: re.sub(r"[^\w]", "", s)[:10]
    keep, unused = [], []
    for i, (t, s) in enumerate(sents):
        later = [j for j in range(i + 1, len(sents)) if norm(sents[j][1]) == norm(s) and sents[j][0] - t <= 60]
        (unused if later else keep).append((t, s))
    out = jdump(Path(wd) / "beats.json", {"beats": keep, "unused": unused})
    hook_ok = keep[0][0] <= 10 and keep[0][1].endswith("؟")
    return [check("first take marked unused, retake kept", unused == [sents[0]] and sents[1] in keep, unused, [sents[0]]),
            check("a repeat after 60 s is a new line, not a retake", sents[4] in keep, sents[4][0], "kept"),
            check("hook poses the question within 10 s", hook_ok, keep[0], "≤ 10 s, ends in ؟"),
            check("negative control: different openings are never merged", norm(sents[2][1]) != norm(sents[3][1]), [norm(sents[2][1]), norm(sents[3][1])], "differ")], [out]


@card("SYNC-46")
def voice2motion_plan(task, wd):
    """audio2motion.py AUDIO --transcript t.txt --plan-only: 50 Hz envelope from 8 kHz mono, semantic scene plan; refuses an
    empty transcript and never claims ASR timing."""
    p = save(wd, "voice.wav", speechlike(4.6, SPANS))
    txt = Path(wd) / "t.txt"
    txt.write_text("الشمس تشرق على الطريق\nوالقلب يحلم بالنجاح\n", encoding="utf-8")
    plan = Path(wd) / "plan.json"
    sh([sys.executable, VEND / "audio2motion.py", p, "--transcript", txt, "--plan-only", "--plan-out", plan], cwd=wd, timeout=60)
    d = json.loads(plan.read_text(encoding="utf-8"))
    blob = json.dumps(d, ensure_ascii=False)
    empty = Path(wd) / "empty.txt"
    empty.write_text("  \n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(VEND / "audio2motion.py"), str(p), "--transcript", str(empty), "--plan-only", "--plan-out", str(Path(wd) / "e.json")], capture_output=True, text=True, cwd=wd)
    asr_claim = re.search(r'"timing"\s*:\s*"(asr|whisper)"', blob)
    return [check("plan written with scenes for the transcript lines", len(blob) > 50 and ("الشمس" in blob or "sun" in blob), len(blob), "> 50"),
            check("timing not claimed as ASR", asr_claim is None, bool(asr_claim), False),
            check("negative control: an empty transcript is refused", r.returncode != 0, r.returncode, "!= 0")], [plan]


GAPS.update({
    "SYNC-08": "the .en-model trap and model ladder need faster-whisper / whisper.cpp weights (75 MB-3.1 GB downloads) to demonstrate",
    "SYNC-14": "cloud STT with diarisation needs paid keys (Deepgram, ElevenLabs Scribe, AssemblyAI, Together, Gemini)",
    "SYNC-45": "verse film from sound renders through HyperFrames after faster-whisper timing (network model download); the estimated path writes into the vendor projects/ folder",
    "SYNC-48": "the talking-clip reel needs faster-whisper weights (or a real transcript) and a decaption/restoration chain on a real clip",
    "SYNC-51": "songreel needs faster-whisper large-v3 weights and a footage pool fetched with yt-dlp (network)",
    "SYNC-19": "narration word budgets are a planning rule of thumb (words per minute); the real check is a TTS duration, which needs a TTS engine",
})
