"""Programs for the voice-tts family.

No TTS engine, API key or browser is used: those cards are skipped. What runs here is the voice
work that is computable offline: script and direction rules (word budgets, spoken vs shown text,
SSML mapping, SCRIPT.md parsing, dialect blocks, Egyptian numbers, locked narrator strings),
caption timing (karaoke, typewriter, draw-on, pacing), and real audio processing on synthetic
signals with ffmpeg and numpy (clean-up chain, EQ presets, voice costumes, centre-cancel stem
split, sidechain ducking, PCM vs MP3 joins, recording-spec measurement, waveform peaks).
"""
from __future__ import annotations
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from ._lang_common import (save, eq, truth, words, sentences, sha256, norm_ar, tone, write_wav, read_wav, db, peak_db,
                           band_db, ffmpeg, ffprobe_duration, ffprobe_stream, loudness)


# ---------- VOICE-12 direction JSON ----------
def direct_ok(d):
    errs = []
    if len(d["note"].split()) > 60:
        errs.append("note > 60 words")
    if not 2 <= d["pace"] <= 4:
        errs.append("pace outside 2-4 wps")
    if not 1 <= d["energy"] <= 10:
        errs.append("energy outside 1-10")
    if d["pitch"] not in ("low", "mid", "high"):
        errs.append("pitch must be low|mid|high")
    return errs


def piper_length_scale(pace, base_pace=3.0):
    return round(base_pace / pace, 3)


def v12(work: Path):
    d = {"note": "warm, unhurried, smile on the hook", "voice": "kareem", "pace": 2.5, "energy": 6, "pitch": "mid",
         "stress": ["مجانًا"]}
    bad = dict(d, note="word " * 61, pace=5, energy=0, pitch="loud")
    save(work, "direction.json", dict(d, piper_length_scale=piper_length_scale(d["pace"])))
    return [eq("valid direction", direct_ok(d), []), eq("four violations", len(direct_ok(bad)), 4),
            eq("slower pace -> longer length_scale", piper_length_scale(2.5), 1.2), eq("faster", piper_length_scale(4), 0.75)]


# ---------- VOICE-17 Voice Director ----------
class Director:
    def __init__(self):
        self.cast = {}
        self.cache = {}

    def voice_for(self, speaker, pool):
        if speaker not in self.cast:
            self.cast[speaker] = pool[len(self.cast) % len(pool)]
        return self.cast[speaker]

    def render(self, turns, kind="speech"):
        if kind == "song":
            return {"route": "song generation", "rendered": []}
        out = []
        for i, (spk, text) in enumerate(turns):
            k = sha256(f"{spk}:{text}")
            if k not in self.cache:
                self.cache[k] = f"{i}.wav"
                out.append(i)
        return {"route": "tts", "rendered": out}


def v17(work):
    d = Director()
    pool = ["Kore", "Puck", "Leda"]
    ep1 = [d.voice_for(s, pool) for s in ("Nour", "Adam")]
    ep2 = [d.voice_for(s, pool) for s in ("Adam", "Nour", "Sara")]
    r1 = d.render([("Nour", "hi"), ("Adam", "hello"), ("Nour", "bye")])
    r2 = d.render([("Nour", "hi"), ("Adam", "hello there"), ("Nour", "bye")])
    song = d.render([("Nour", "la la")], kind="song")
    save(work, "director.json", {"cast": d.cast, "r1": r1, "r2": r2, "song": song})
    return [eq("stable casting across episodes", (ep1, ep2[:2]), (["Kore", "Puck"], ["Puck", "Kore"])),
            eq("first render renders all", r1["rendered"], [0, 1, 2]), eq("only the changed turn re-renders", r2["rendered"], [1]),
            eq("songs never go to TTS", song["route"], "song generation")]


# ---------- VOICE-18 words-per-second budget ----------
def word_budget(seconds, wps=2.5, lang="en"):
    n = seconds * wps
    if lang == "ar":
        n *= 0.825          # 15-20 % fewer words: midpoint
    return int(n)


def scene_fill(seconds):
    if 3 <= seconds <= 4:
        lo, hi = 8, 12
    elif 5 <= seconds <= 6:
        lo, hi = 15, 22
    elif 7 <= seconds <= 8:
        lo, hi = 22, 30
    else:
        raise ValueError("no band")
    return lo, hi


def v18(work):
    b = {s: word_budget(s) for s in (15, 30, 60)}
    ar = word_budget(30, lang="ar")
    total_ok = lambda words_n, target_s: abs(words_n / 2.5 - target_s) / target_s <= 0.05
    save(work, "budget.json", {"en": b, "ar30": ar, "fill": {s: scene_fill(s) for s in (4, 6, 8)}})
    return [eq("15/30/60 s budgets", b, {15: 37, 30: 75, 60: 150}), eq("Arabic 30 s ~17.5% fewer", ar, 61),
            eq("scene fill bands", [scene_fill(s) for s in (4, 6, 8)], [(8, 12), (15, 22), (22, 30)]),
            truth("±5 % total check", total_ok(77, 30) and not total_ok(82, 30))]


# ---------- VOICE-19 regenerate, never stretch ----------
def speed_plan(speed, content):
    if speed >= 1.5:
        raise ValueError("avoid >= 1.5")
    if not 0.7 <= speed <= 1.2:
        raise ValueError("speed outside 0.7-1.2")
    return {"content": content, "speed": speed, "piper_length_scale": round(1 / speed, 3), "method": "regenerate",
            "atempo": None}


def v19(work):
    tut = speed_plan(0.8, "tutorial")
    up = speed_plan(1.15, "upbeat")
    errs = []
    for s in (1.5, 0.5):
        try:
            speed_plan(s, "x")
        except ValueError as e:
            errs.append(str(e))
    save(work, "speed.json", {"tutorial": tut, "upbeat": up, "refused": errs})
    return [eq("length_scale = 1/speed", (tut["piper_length_scale"], up["piper_length_scale"]), (1.25, 0.87)),
            eq("regenerate, no atempo stretch", (tut["method"], tut["atempo"]), ("regenerate", None)),
            eq("bad speeds refused", len(errs), 2)]


# ---------- VOICE-20 spoken vs on-screen ----------
PRON = {".com": " دوت كوم", "API": "إيه بي آي", "$1.9T": "قرابة تريليوني دولار", "٢٠٢٦": "ألفين وستة وعشرين"}


def say_show(text):
    say = text
    for k, v in PRON.items():
        say = say.replace(k, v)
    return say, text


def v20(work):
    say, show = say_show("زوروا kosif.com وجربوا الـ API في ٢٠٢٦")
    save(work, "say.txt", say)
    save(work, "show.txt", show)
    return [truth("say.txt is pronounced form", "دوت كوم" in say and "إيه بي آي" in say and "ألفين وستة وعشرين" in say),
            eq("show.txt untouched", show, "زوروا kosif.com وجربوا الـ API في ٢٠٢٦"),
            truth("no symbol left for TTS", ".com" not in say and "٢٠٢٦" not in say)]


# ---------- VOICE-21 scene narration rules ----------
WAW_WORDS = {"واحد", "واحده", "وقت", "وسط", "وصل", "وجه", "وزن", "وطن"}


def narration_plan(scenes, wps=2.5):
    out, issues = [], []
    for i, s in enumerate(scenes):
        conj = [w for w in s["vo"].split() if w.startswith("و") and len(w) > 3 and norm_ar(w).rstrip(".،") not in WAW_WORDS]
        if conj or " and " in s["vo"]:
            issues.append(f"scene {i}: needs 'and' -> split into two scenes")
        start = max(0.0, s["action_t"] - 0.4)
        out.append({"scene": i, "vo_start": round(start, 2), "lead": round(s["action_t"] - start, 2)})
    hook_s = len(scenes[0]["vo"].split()) / wps
    if hook_s > 2:
        issues.append("hook longer than 2 s")
    return out, issues


def v21(work):
    scenes = [{"vo": "24 تبويبًا.", "action_t": 0.5}, {"vo": "نقرة واحدة.", "action_t": 3.0},
              {"vo": "يجمعها ويرتبها", "action_t": 6.0}]
    plan, iss = narration_plan(scenes)
    save(work, "narration.json", {"plan": plan, "issues": iss})
    return [eq("narrated 0.4 s before the action", [p["vo_start"] for p in plan], [0.1, 2.6, 5.6]),
            truth("lead within 0.3-0.5 s", all(0.3 <= p["lead"] <= 0.5 for p in plan)),
            eq("و-joined line flagged", iss, ["scene 2: needs 'and' -> split into two scenes"])]


# ---------- VOICE-22 tags -> SSML ----------
def to_ssml(line):
    s = re.sub(r"\[pause (\d+(?:\.\d+)?)s\]", lambda m: f"<break time='{int(float(m.group(1)) * 1000)}ms'/>", line)
    s = re.sub(r"\*([^*]+)\*", r"<emphasis>\1</emphasis>", s)
    s = re.sub(r"\(([a-z]+)\)\s*", "", s)
    return f"<speak><prosody rate='-5%'>{s}</prosody></speak>"


def piper_from_tags(line):
    pauses = [float(x) for x in re.findall(r"\[pause (\d+(?:\.\d+)?)s\]", line)]
    return {"sentence_silence": max(pauses) if pauses else 0.2, "length_scale": 1.05}


def v22(work):
    line = "(calm) أهلًا بيكم [pause 0.5s] النهارده *مجانًا* [pause 0.3s] للكل"
    ssml = to_ssml(line)
    save(work, "ssml.xml", ssml)
    root = ET.fromstring(ssml)
    breaks = [b.get("time") for b in root.iter("break")]
    pp = piper_from_tags(line)
    return [eq("breaks", breaks, ["500ms", "300ms"]), eq("emphasis", [e.text for e in root.iter("emphasis")], ["مجانًا"]),
            truth("emotion tag not spoken", "(calm)" not in ssml), truth("pauses within 0.3-0.8 s", all(0.3 <= float(b[:-2]) / 1000 <= 0.8 for b in breaks)),
            eq("Piper mapping", pp["sentence_silence"], 0.5)]


# ---------- VOICE-23 SCRIPT.md ----------
def parse_script(md):
    out = []
    for m in re.finditer(r"^## Line (\d+) — (.+?) \(Frame (\d+)\)\n(.*?)(?=^## |\Z)", md, re.S | re.M):
        body = m.group(4)
        spoken = " ".join(l.strip() for l in body.splitlines() if l.startswith("    "))
        guide = re.search(r"Time guide: (.+)", body)
        out.append({"line": int(m.group(1)), "label": m.group(2), "frame": int(m.group(3)), "spoken": spoken,
                    "time_guide": guide.group(1) if guide else None})
    return out


def v23(work):
    md = ("# Script\n## Line 1 — hook (Frame 1)\nTime guide: 0-2 s\nDelivery: bright\n    القهوة دي مختلفة.\n\n"
          "## Line 2 — proof (Frame 3)\nTime guide: 2-6 s\nDelivery: calm\n    محمصة النهارده الصبح\n    في وسط البلد.\n")
    rows = parse_script(md)
    (work / "SCRIPT.md").write_text(md, encoding="utf-8")
    save(work, "tts_lines.json", rows)
    return [eq("two blocks", [r["line"] for r in rows], [1, 2]), eq("frames", [r["frame"] for r in rows], [1, 3]),
            eq("only indented text goes to TTS", rows[1]["spoken"], "محمصة النهارده الصبح في وسط البلد."),
            truth("time guide kept as a guide, not timing", rows[0]["time_guide"] == "0-2 s")]


# ---------- VOICE-24 dialect voice direction ----------
DIALECT = {"egyptian": ("مش", "ازاي", "دلوقتي", "ده", "دي"), "levantine": ("شو", "هلق", "منيح"), "gulf": ("شلون", "وايد")}


def block_dialects(text):
    toks = {norm_ar(t) for t in re.findall(r"[ء-ي]+", text)}
    return sorted(d for d, ms in DIALECT.items() if any(norm_ar(m) in toks for m in ms))


def direct_blocks(blocks, pron):
    out = []
    for b in blocks:
        ds = block_dialects(b["text"])
        spoken = b["text"]
        for w, s in pron.items():
            spoken = spoken.replace(w, s)
        errs = []
        if len(ds) > 1:
            errs.append("mixed dialects in one block")
        if not 1 <= b["energy"] <= 5:
            errs.append("energy must be 1-5")
        out.append({"spoken": spoken, "dialects": ds, "errors": errs})
    return out


def v24(work):
    pron = {"الـ AI": "الإيه آي", "واتساب": "واتس آب"}
    r = direct_blocks([{"text": "مش هتصدق ازاي الـ AI بيرد على واتساب", "energy": 4},
                       {"text": "مش عارف شو صار هلق", "energy": 3}, {"text": "ده سهل", "energy": 7}], pron)
    save(work, "direction_blocks.json", r)
    return [eq("pronunciation memory applied", r[0]["spoken"], "مش هتصدق ازاي الإيه آي بيرد على واتس آب"),
            eq("clean block", r[0]["errors"], []), eq("dialect mix flagged", r[1]["errors"], ["mixed dialects in one block"]),
            eq("energy scale 1-5", r[2]["errors"], ["energy must be 1-5"])]


# ---------- VOICE-25 language intake ----------
def voice_route(brief):
    lang = brief.get("language") or "ar-EG"
    return {"language": lang, "engine": {"ar-SA": "Piper/Naayf", "ar-EG": "Gemini persona (VOICE-26)"}.get(lang, "ask"),
            "pron_map": f"pron_{lang}.json"}


def v25(work):
    r = [voice_route({}), voice_route({"language": "ar-SA"}), voice_route({"language": "fr-FR"})]
    save(work, "intake.json", r)
    return [eq("default ar-EG", r[0]["language"], "ar-EG"), eq("ar-SA -> Piper/Naayf", r[1]["engine"], "Piper/Naayf"),
            eq("unknown language asks", r[2]["engine"], "ask"), eq("pronunciation map follows language", r[1]["pron_map"], "pron_ar-SA.json")]


# ---------- VOICE-26 Egyptian persona ----------
EG_NUM = {11: "حداشر", 12: "اتناشر", 15: "خمستاشر", 100: "مية", 1000: "ألف"}
FILLERS = ("يا جماعة", "بصوا بقى", "تمام؟", "زي ما انتم شايفين")


def egyptianise(text):
    t = re.sub(r"\b(\d+)\b", lambda m: EG_NUM.get(int(m.group(1)), m.group(1)), text)
    t = t.replace("جنيه", "جنيه [geneh]")
    return t


def filler_ok(text):
    ss = [s for s in re.split(r"[.!؟?]\s*", text) if s.strip()]
    n = sum(text.count(f) for f in FILLERS)
    return n <= max(1, len(ss) // 3), n, len(ss)


def v26(work):
    t = egyptianise("السعر 15 جنيه بدل 100 والعرض 12 يوم")
    ok = filler_ok("يا جماعة النهارده عندنا عرض. السعر حلو. بصوا بقى الجودة. تمام؟ يلا.")
    ok2 = filler_ok("يا جماعة القهوة دي جديدة. محمصة النهارده. جربوها.")
    save(work, "persona.txt", t)
    return [eq("Egyptian numbers", t, "السعر خمستاشر جنيه [geneh] بدل مية والعرض اتناشر يوم"),
            eq("too many fillers flagged", ok[0], False), eq("one filler per 3 sentences ok", ok2[0], True)]


# ---------- VOICE-27 locked narrator ----------
VOICE = "Narrator: deep, warm, slightly raspy male, mid-40s, measured documentary pace"


def narrate(topic_words, i, n):
    line = " ".join(topic_words[i * 19:(i + 1) * 19][:19])
    return f"{VOICE}. Clip {i + 1}/{n}, 10 s. Says: \"{line}\". Sound: projector hum, paper snaps."


def v27(work):
    topic = [f"w{k}" for k in range(100)]
    clips = [narrate(topic, i, 5) for i in range(5)]
    save(work, "clips.json", clips)
    spoken = [re.search(r'Says: "([^"]*)"', c).group(1).split() for c in clips]
    return [truth("< 20 words per 10 s clip", all(len(s) < 20 for s in spoken)), truth("same voice string in every prompt",
                                                                                     all(c.startswith(VOICE) for c in clips)),
            eq("5 clips", len(clips), 5)]


# ---------- VOICE-28 coach cues ----------
COACH = ["Breathe out, push.", "Slow on the way down.", "Keep your core tight.", "Two more, strong.", "Hold, then release."]
MUSCLE = {"Abs": ["Ribs down, crunch.", "Exhale at the top.", "Lower slowly now.", "No neck pulling.", "Squeeze and hold."],
          "Chest": ["Elbows at forty-five.", "Press up, exhale.", "Lower to chest level.", "Shoulders back, down.", "Full stretch, control."],
          "Back": ["Pull elbows to hips.", "Squeeze shoulder blades.", "Chest up, pull.", "Slow return, control.", "Lead with elbows."]}


def cue_for_rep(muscle, phase):
    lines = MUSCLE[muscle]
    return lines[phase % len(lines)]


def v28(work):
    allc = COACH + [l for ls in MUSCLE.values() for l in ls]
    save(work, "cues.json", {"generic": COACH, "muscle": MUSCLE})
    return [eq("5 generic + 15 muscle lines", (len(COACH), sum(len(v) for v in MUSCLE.values())), (5, 15)),
            truth("every cue <= 6 words", all(len(c.split()) <= 6 for c in allc), max(len(c.split()) for c in allc)),
            eq("one cue per rep phase", [cue_for_rep("Back", p) for p in (0, 1)], ["Pull elbows to hips.", "Squeeze shoulder blades."])]


# ---------- VOICE-29 human VO spec ----------
def vo_spec_check(path):
    x, sr, bits = read_wav(path)
    x = x.mean(axis=1)
    room = x[: sr]                       # first 1 s is room tone
    return {"sr": sr, "bits": bits, "peak_db": round(peak_db(x), 2), "noise_floor_db": round(db(room), 1),
            "pass": sr == 48000 and bits == 24 and abs(peak_db(x) + 12) <= 1 and db(room) < -60}


def v29(work):
    rng = np.random.default_rng(1)
    sr = 48000
    room = rng.normal(0, 10 ** (-72 / 20), sr)
    speech = tone(220, 1.0, sr, amp=10 ** (-12 / 20)) * np.hanning(sr)
    write_wav(work / "take_ok.wav", np.concatenate([room, speech + rng.normal(0, 10 ** (-72 / 20), sr)]), sr, bits=24)
    sr2 = 44100
    room2 = rng.normal(0, 10 ** (-50 / 20), sr2)
    write_wav(work / "take_bad.wav", np.concatenate([room2, tone(220, 1.0, sr2, amp=0.9)]), sr2, bits=16)
    g, b = vo_spec_check(work / "take_ok.wav"), vo_spec_check(work / "take_bad.wav")
    save(work, "spec.json", {"ok": g, "bad": b})
    return [eq("48 kHz / 24-bit", (g["sr"], g["bits"]), (48000, 24)), eq("peak ≈ -12 dBFS", g["peak_db"], -12.0, tol=0.5),
            truth("noise floor < -60 dBFS", g["noise_floor_db"] < -60, g["noise_floor_db"]), eq("good take passes", g["pass"], True),
            eq("44.1k/16-bit/-50 dB room take fails", b["pass"], False)]


# ---------- VOICE-34 voice-led pacing ----------
def pacing(words_json, cues):
    gaps = []
    for a, b in zip(words_json, words_json[1:]):
        if b["start"] - a["end"] > 1.5:
            gaps.append({"from": a["end"], "to": b["start"], "motion": "camera drift"})
    sync = {c["word"]: round(abs(c["t"] - next(w["start"] for w in words_json if w["w"] == c["word"])) * 1000) for c in cues}
    return gaps, sync


def v34(work):
    wj = [{"w": "القهوة", "start": 0.0, "end": 0.5}, {"w": "دي", "start": 0.55, "end": 0.8},
          {"w": "مختلفة", "start": 2.6, "end": 3.1}, {"w": "جدًا", "start": 3.2, "end": 3.6}]
    gaps, sync = pacing(wj, [{"word": "مختلفة", "t": 2.68}, {"word": "القهوة", "t": 0.15}])
    save(work, "pacing.json", {"gaps": gaps, "sync_ms": sync})
    return [eq("pause > 1.5 s gets ambient motion", gaps, [{"from": 0.8, "to": 2.6, "motion": "camera drift"}]),
            eq("key-word sync ms", sync, {"مختلفة": 80, "القهوة": 150}),
            eq("within 100 ms only for the key word", [k for k, v in sync.items() if v <= 100], ["مختلفة"])]


# ---------- VOICE-35 karaoke highlight ----------
INK, DONE = (0x8a, 0x7b, 0x70), (0x1f, 0x1b, 0x17)


def lerp(a, b, u):
    return tuple(round(x + (y - x) * u) for x, y in zip(a, b))


def word_colour(t, start, lead=0.06, dur=0.12):
    u = min(1.0, max(0.0, (t - (start - lead)) / dur))
    return lerp(INK, DONE, u)


def out_back(u, s=1.70158):
    u -= 1
    return u * u * ((s + 1) * u + s) + 1


def v35(work):
    start = 1.0
    c_before, c_mid, c_end = word_colour(0.94, start), word_colour(1.0, start), word_colour(1.06, start)
    xs = [out_back(i / 20) for i in range(21)]
    im = Image.new("RGB", (120, 30), (0xf4, 0xee, 0xe0))
    dr = ImageDraw.Draw(im)
    dr.rectangle([10, 5, 50, 25], fill=(0xf6, 0xcf, 0x9a))
    dr.rectangle([15, 10, 45, 20], fill=c_end)
    im.save(work / "karaoke_frame.png")
    return [eq("ink until start-60 ms", c_before, INK), truth("halfway at start", all(abs(a - b) <= 1 for a, b in zip(c_mid, lerp(INK, DONE, 0.5))), c_mid),
            eq("done colour after 120 ms", c_end, DONE), truth("box tween overshoots (outBack)", max(xs) > 1.0, round(max(xs), 3)),
            eq("box lands exactly", xs[-1], 1.0, tol=1e-9)]


# ---------- VOICE-36 typewriter captions ----------
def typed_at(t, wj):
    shown = [w["w"] for w in wj if w["start"] <= t]
    caret = int(t / 0.53) % 2 == 0
    return " ".join(shown), caret


def v36(work):
    wj = [{"w": "جرّب", "start": 0.2}, {"w": "الجديد", "start": 0.7}, {"w": "اليوم", "start": 1.4}]
    states = {t: typed_at(t, wj) for t in (0.1, 0.7, 1.0, 1.5)}
    save(work, "typewriter.json", {str(k): v for k, v in states.items()})
    return [eq("nothing before first word", states[0.1][0], ""), eq("word revealed at word.start", states[0.7][0], "جرّب الجديد"),
            truth("Arabic revealed per whole word", all(w in ("جرّب", "الجديد", "اليوم") for w in states[1.5][0].split())),
            eq("caret blink 530 ms", [typed_at(t, wj)[1] for t in (0.0, 0.52, 0.54, 1.07)], [True, True, False, True])]


# ---------- VOICE-37 waveform with playhead ----------
def v37(work):
    sr = 16000
    sig = np.concatenate([tone(300, 1.0, sr, 0.1), tone(300, 1.0, sr, 0.8)])
    write_wav(work / "vo.wav", sig, sr)
    raw = work / "vo.f32"
    ffmpeg("-i", work / "vo.wav", "-ac", "1", "-f", "f32le", raw)
    x = np.fromfile(raw, dtype="<f4")
    win = sr // 100
    peaks = np.abs(x[: len(x) // win * win]).reshape(-1, win).max(axis=1)
    bar, gap = 3, 2
    width = len(peaks) * (bar + gap)
    im = Image.new("RGB", (width, 64), (0xf8, 0xf5, 0xec))
    dr = ImageDraw.Draw(im)
    t, dur = 1.0, 2.0
    play_x = t / dur * width
    for i, p in enumerate(peaks):
        h = p * 60
        x0 = i * (bar + gap)
        col = (0x3b, 0x69, 0xf3) if x0 < play_x else (0x5c, 0x5c, 0x6f)
        dr.rectangle([x0, 32 - h / 2, x0 + bar - 1, 32 + h / 2], fill=col)
    im.save(work / "waveform.png")
    return [eq("100 peaks per second", len(peaks), 200), eq("quiet half bar height", round(float(peaks[50]) * 60, 1), 6.0, tol=0.3),
            eq("loud half bar height", round(float(peaks[150]) * 60, 1), 48.0, tol=0.5), eq("playhead x at t/dur", play_x, 500.0)]


# ---------- VOICE-38 draw-on paced to sentences ----------
def lecture_plan(sents, chapters):
    t, plan = 0.0, []
    for ch, idx in chapters:
        for i in idx:
            s = sents[i]
            lines = wrap_lines(s["text"], 28)
            plan.append({"t": round(t, 2), "draw_s": s["dur"], "element": f"el{i}", "subtitle": lines})
            t += s["dur"]
        plan.append({"t": round(t, 2), "eraser": ch})
        t += 0.6
    return plan


def wrap_lines(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    out.append(cur)
    return out


def v38(work):
    sents = [{"text": "Light hits the leaf.", "dur": 2.0}, {"text": "Chlorophyll absorbs red and blue light strongly.", "dur": 3.5},
             {"text": "Sugar is made.", "dur": 1.5}]
    plan = lecture_plan(sents, [("ch1", [0, 1]), ("ch2", [2])])
    save(work, "lecture_plan.json", plan)
    els = [p for p in plan if "element" in p]
    return [eq("one element per sentence, seconds = sentence length", [e["draw_s"] for e in els], [2.0, 3.5, 1.5]),
            eq("eraser wipe between chapters", [p.get("eraser") for p in plan if "eraser" in p], ["ch1", "ch2"]),
            truth("subtitles 1-2 lines", all(1 <= len(e["subtitle"]) <= 2 for e in els)), eq("chapter 2 starts after wipe", els[2]["t"], 6.1)]


# ---------- audio helpers for processing cards ----------
def _proc(work, name, sig, sr, af, out_sr=None):
    src = write_wav(work / f"{name}_in.wav", sig, sr)
    dst = work / f"{name}_out.wav"
    extra = ["-ar", str(out_sr)] if out_sr else []
    ffmpeg("-i", src, "-af", af, *extra, "-c:a", "pcm_s16le", dst)
    y, ysr, _ = read_wav(dst)
    return y.mean(axis=1), ysr


# ---------- VOICE-39 clean-up chain ----------
CHAIN39 = ("highpass=f=70,afftdn=nr=6:nf=-42,equalizer=f=220:t=q:w=1:g=1.2,equalizer=f=3200:t=q:w=1.4:g=2.2,"
           "equalizer=f=9000:t=q:w=1:g=-1,deesser=i=0.35,"
           "acompressor=threshold=0.12:ratio=2.5:attack=10:release=160:makeup=1.6,loudnorm=I=-16:TP=-1.5:LRA=11")


def v39(work):
    sr = 48000
    t = np.arange(3 * sr) / sr
    env = 0.5 + 0.5 * np.sin(2 * np.pi * 3 * t)
    voice = env * (0.3 * np.sin(2 * np.pi * 1000 * t) + 0.2 * np.sin(2 * np.pi * 300 * t))
    rumble = 0.2 * np.sin(2 * np.pi * 35 * t)
    sig = voice + rumble
    y, ysr = _proc(work, "voice", sig, sr, CHAIN39, out_sr=48000)
    rel_in = band_db(sig, sr, 35) - band_db(sig, sr, 1000)
    rel_out = band_db(y, ysr, 35) - band_db(y, ysr, 1000)
    L = loudness(work / "voice_out.wav")
    save(work, "chain.json", {"chain": CHAIN39, "rumble_rel_in": rel_in, "rumble_rel_out": rel_out, "loudness": L})
    return [eq("48 kHz out", ysr, 48000), truth("HPF 70 Hz cuts 35 Hz rumble >= 8 dB", rel_in - rel_out >= 8, round(rel_in - rel_out, 1)),
            truth("loudnorm near -16 LUFS", L["I"] is not None and abs(L["I"] + 16) <= 2, L)]


# ---------- VOICE-40 repair presets ----------
PRESETS = {"boom": ("equalizer=f=200:t=q:w=1.4:g=-4", 200, -4.0), "mud": ("equalizer=f=250:t=q:w=1.2:g=-3", 250, -3.0),
           "boxiness": ("equalizer=f=400:t=q:w=1.4:g=-3", 400, -3.0), "clarity": ("equalizer=f=3000:t=q:w=1:g=2.5", 3000, 2.5),
           "harshness": ("equalizer=f=3200:t=q:w=1.6:g=-3", 3200, -3.0)}


def v40(work):
    sr = 48000
    gains = {}
    for name, (af, f, _) in PRESETS.items():
        sig = tone(f, 1.0, sr, 0.3)
        y, _ = _proc(work, name, sig, sr, af)
        gains[name] = round(db(y[sr // 4:]) - db(sig[sr // 4:]), 2)
    r, _ = _proc(work, "rumble", tone(40, 1.0, sr, 0.3), sr, "highpass=f=80")
    gains["rumble_cut_40Hz"] = round(db(r[sr // 4:]) - db(tone(40, 1.0, sr, 0.3)[sr // 4:]), 2)
    save(work, "preset_gains.json", gains)
    return [truth(f"{n} centre gain {g} dB", abs(gains[n] - g) <= 0.5, gains[n]) for n, (_, _, g) in PRESETS.items()] + \
        [truth("rumble HPF 80 Hz cuts 40 Hz by >= 6 dB", gains["rumble_cut_40Hz"] <= -6, gains["rumble_cut_40Hz"])]


# ---------- VOICE-41 voice costumes ----------
COSTUME = {"telephone": "highpass=f=300,lowpass=f=3400,acompressor=ratio=4",
           "megaphone": "highpass=f=500,lowpass=f=4000,acrusher=bits=10:mix=0.25,aecho=0.8:0.5:40:0.4",
           "room": "aecho=0.8:0.7:60|140:0.4|0.3"}


def v41(work):
    sr = 48000
    sig = tone(100, 1, sr, 0.2) + tone(1000, 1, sr, 0.2) + tone(7000, 1, sr, 0.2)
    tel, _ = _proc(work, "tel", sig, sr, COSTUME["telephone"])
    keep = band_db(tel, sr, 1000)
    lo, hi = keep - band_db(tel, sr, 100), keep - band_db(tel, sr, 7000)
    meg, _ = _proc(work, "meg", sig, sr, COSTUME["megaphone"])
    imp = np.zeros(sr // 2)
    imp[0] = 0.9
    room, _ = _proc(work, "room", imp, sr, COSTUME["room"])
    e60 = abs(room[int(0.060 * sr)])
    e140 = abs(room[int(0.140 * sr)])
    save(work, "costumes.json", {"tel_lo_cut": lo, "tel_hi_cut": hi, "echo_60": e60, "echo_140": e140})
    return [truth("telephone cuts 100 Hz by >= 10 dB vs 1 kHz", lo >= 10, round(lo, 1)),
            truth("telephone cuts 7 kHz by >= 10 dB vs 1 kHz", hi >= 10, round(hi, 1)),
            truth("megaphone band-limits below 500 Hz", band_db(meg, sr, 1000) - band_db(meg, sr, 100) >= 10),
            truth("room echoes at 60 and 140 ms", e60 > 0.1 and e140 > 0.05, (round(e60, 3), round(e140, 3)))]


# ---------- VOICE-42 centre-cancel stem split ----------
def butter_lp(x, sr, fc):
    from scipy.signal import butter, sosfiltfilt
    return sosfiltfilt(butter(4, fc, "low", fs=sr, output="sos"), x)


def audiolab(stereo, sr, mode):
    if stereo.ndim != 2 or stereo.shape[1] != 2:
        raise ValueError("centre-cancel works on stereo only")
    L, R = stereo[:, 0], stereo[:, 1]
    mid, side = (L + R) / 2, (L - R) / 2
    if mode == "novoice":
        return side + butter_lp(mid, sr, 140)        # restore bass below 140 Hz after phase cancel
    if mode == "voice":
        return mid - butter_lp(mid, sr, 140)
    raise ValueError(mode)


def v42(work):
    sr = 16000
    voice = tone(1000, 1, sr, 0.3)
    bass = tone(80, 1, sr, 0.3)
    music_l, music_r = tone(500, 1, sr, 0.3), -tone(500, 1, sr, 0.3)
    st = np.stack([voice + bass + music_l, voice + bass + music_r], axis=1)
    write_wav(work / "mix.wav", st, sr)
    nv = audiolab(st, sr, "novoice")
    write_wav(work / "novoice.wav", nv, sr)
    v_in, v_out = band_db(st, sr, 1000), band_db(nv, sr, 1000)
    refused = False
    try:
        audiolab(voice, sr, "novoice")
    except ValueError:
        refused = True
    return [truth("centre voice removed >= 40 dB", v_in - v_out >= 40, round(v_in - v_out, 1)),
            eq("bass < 140 Hz restored", band_db(nv, sr, 80), band_db(st, sr, 80), tol=1.0),
            truth("side music kept", band_db(nv, sr, 500) > band_db(st, sr, 500) - 1), eq("mono refused", refused, True)]


# ---------- VOICE-43 ducking ----------
def v43(work):
    sr = 16000
    music = tone(220, 3, sr, 0.0376)
    voice = np.zeros(3 * sr)
    voice[sr:2 * sr] = tone(1000, 1, sr, 0.5)
    write_wav(work / "music.wav", music, sr)
    write_wav(work / "voice.wav", voice, sr)

    def duck(ratio):
        out = work / f"ducked_r{ratio}.wav"
        ffmpeg("-i", work / "music.wav", "-i", work / "voice.wav", "-filter_complex",
               f"[0:a][1:a]sidechaincompress=threshold=0.03:ratio={ratio}:attack=20:release=400[d]", "-map", "[d]",
               "-c:a", "pcm_s16le", out)
        y, _, _ = read_wav(out)
        y = y[:, 0]
        return db(y[int(0.2 * sr):int(0.9 * sr)]) - db(y[int(1.4 * sr):int(1.9 * sr)])
    d8, d4 = duck(8), duck(4)
    save(work, "duck.json", {"duck_db_ratio8": d8, "duck_db_ratio4": d4})
    return [truth("bed ducks >= 8 dB under the voice (ratio 8)", d8 >= 8, round(d8, 1)),
            truth("ratio 4 is gentler", 0 < d4 < d8, round(d4, 1)), eq("bed level before voice ≈ -31.5 dB", round(db(music), 1), -31.5, tol=0.3)]


# ---------- VOICE-45 PCM joins ----------
def v45(work):
    sr = 48000
    parts = []
    for i, f in enumerate((300, 400, 500)):
        p = write_wav(work / f"c{i}.wav", tone(f, 0.5, sr, 0.3), sr)
        parts.append(p)
        ffmpeg("-i", p, "-c:a", "libmp3lame", "-b:a", "128k", work / f"c{i}.mp3")
    inputs = sum((["-i", str(p)] for p in parts), [])
    ffmpeg(*inputs, "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1[a]", "-map", "[a]", work / "joined_pcm.wav")
    (work / "list.txt").write_text("".join(f"file 'c{i}.mp3'\n" for i in range(3)))
    ffmpeg("-f", "concat", "-safe", "0", "-i", work / "list.txt", "-c", "copy", work / "joined_copy.mp3")
    ffmpeg("-i", work / "joined_copy.mp3", work / "joined_copy.wav")
    pcm = read_wav(work / "joined_pcm.wav")[0].shape[0]
    mp3 = read_wav(work / "joined_copy.wav")[0].shape[0]
    return [eq("PCM join is sample-exact", pcm, 3 * 24000), truth("MP3 copy-join drifts by encoder padding (>= 1000 samples)",
                                                                  abs(mp3 - 72000) >= 1000, mp3 - 72000)]


# ---------- VOICE-48 intent router ----------
VIEW_WORDS = {"home": ["الرئيسية", "home"], "projects": ["المشاريع", "projects"], "editor": ["المحرر", "editor"],
              "settings": ["الإعدادات", "settings"]}


def route_intent(transcript, ctx):
    t = transcript.lower()
    has = lambda *ws: any(w in t for w in ws)
    if has("افتح", "روح", "open", "go to"):
        for v, ws in VIEW_WORDS.items():
            if has(*ws):
                return {"action": "navigate", "view": v}
    if has("حالة", "status", "وصل فين"):
        return {"action": "status", "reply": f"render {ctx['render']}%"}
    return {"action": "guidance", "reply": "قول مثلًا: افتح المشاريع"}


def v48(work):
    r = [route_intent("افتح المشاريع", {"render": 40}), route_intent("الريندر وصل فين؟", {"render": 40}),
         route_intent("احكيلي نكتة", {"render": 40})]
    save(work, "intents.json", r)
    return [eq("navigation", r[0], {"action": "navigate", "view": "projects"}), eq("status", r[1]["reply"], "render 40%"),
            eq("unknown -> guidance", r[2]["action"], "guidance")]


# ---------- VOICE-49 / VOICE-50 orb and FAB ----------
def ease_out(u):
    return 1 - (1 - u) ** 3


def ring_scale(t, delay, dur=1.8, a=0.6, b=1.9):
    u = ((t - delay) % dur) / dur if t >= delay else 0.0
    return a + (b - a) * ease_out(u)


def v49(work):
    css = ("#voiceOrb[data-state=idle]{background:radial-gradient(circle at 35% 35%,#c4b5fd,#6d28d9 60%,#1e1b4b)}\n"
           "#voiceOrb[data-state=listening] .ring{animation:orb-pulse 1.8s ease-out infinite}\n"
           ".ring:nth-child(2){animation-delay:.6s}.ring:nth-child(3){animation-delay:1.2s}\n"
           "#voiceOrb[data-state=thinking]{animation:orb-spin 1.2s linear infinite}\n"
           "#voiceOrb[data-state=speaking]{animation:orb-breathe 1s ease-in-out infinite;transform:scale(1.1)}\n"
           "@keyframes orb-pulse{from{transform:scale(.6)}to{transform:scale(1.9);opacity:0}}\n")
    save(work, "orb.css", css)
    s = [round(ring_scale(0.9, d), 3) for d in (0, 0.6, 1.2)]
    return [eq("ring starts at .6", ring_scale(0, 0), 0.6), eq("staggered rings at t=0.9", s, [round(0.6 + 1.3 * ease_out(0.5), 3),
                                                                                        round(0.6 + 1.3 * ease_out(0.3 / 1.8), 3), 0.6]),
            truth("four states styled", all(f"data-state={k}" in css for k in ("idle", "listening", "thinking", "speaking"))),
            truth("delays 0/.6/1.2 s", ".6s" in css and "1.2s}" in css)]


def fab(t, dur=1.6):
    u = (t % dur) / dur
    e = ease_out(u)
    return round(1 + 0.7 * e, 4), round(0.8 * (1 - e), 4)


def v50(work):
    css = (".voice-fab{width:60px;height:60px;background:linear-gradient(140deg,#6d28d9,#0f766e)}\n"
           ".voice-fab.live .voice-fab-ring{animation:voice-ring 1.6s ease-out infinite}\n"
           "@keyframes voice-ring{from{transform:scale(1);opacity:.8}to{transform:scale(1.7);opacity:0}}\n"
           ".voice-fab:hover{transform:translateY(-2px) scale(1.03)}\n")
    save(work, "fab.css", css)
    return [eq("ring at start", fab(0), (1.0, 0.8)), eq("ring near end", fab(1.5999), (1.7, 0.0)),
            truth("eases out: past half way at half time", fab(0.8)[0] > 1.35), truth("1.6 s loop", fab(1.6) == fab(0))]


# ---------- VOICE-51 mic constraints ----------
def mic_constraints(purpose):
    c = {"echoCancellation": True, "noiseSuppression": True, "autoGainControl": True}
    if purpose == "vo-take":
        c["autoGainControl"] = False
    return {"audio": c}


def v51(work):
    a, b = mic_constraints("chat"), mic_constraints("vo-take")
    save(work, "constraints.json", {"chat": a, "vo": b})
    return [eq("assistant capture", a["audio"], {"echoCancellation": True, "noiseSuppression": True, "autoGainControl": True}),
            eq("VO take: AGC off (it pumps)", b["audio"]["autoGainControl"], False)]


# ---------- VOICE-53 never imitate real voices ----------
REAL = {"amr diab", "fairuz", "morgan freeman", "عمرو دياب", "فيروز"}


def voice_request(req, clone=None):
    low = req.lower()
    hit = [n for n in REAL if n in low]
    if hit:
        return {"action": "describe timbre instead", "named": hit}
    if clone and not clone.get("consent_record"):
        return {"action": "refuse clone: no consent record"}
    return {"action": "ok"}


def v53(work):
    r = [voice_request("make it sound like Morgan Freeman"), voice_request("deep warm narrator", {"voice_id": "v1"}),
         voice_request("deep warm narrator", {"voice_id": "v1", "consent_record": "consent/v1.pdf"})]
    save(work, "voice_policy.json", r)
    return [eq("real voice -> timbre words", r[0]["action"], "describe timbre instead"),
            eq("clone without consent refused", r[1]["action"], "refuse clone: no consent record"), eq("consented clone ok", r[2]["action"], "ok")]


# ---------- VOICE-55 cost hygiene ----------
def preclean(t):
    return re.sub(r"\s+", " ", re.sub(r"[*_#>`]", "", t)).strip()


def tts_batch(lines, cache, voice="kareem", model="m1", settings="s1"):
    hits = miss = chars = 0
    for l in lines:
        t = preclean(l)
        k = sha256(f"{voice}:{model}:{settings}:{t}")
        if k in cache:
            hits += 1
        else:
            cache[k] = f"{k[:8]}.wav"
            miss += 1
            chars += len(t)
    return hits, miss, chars


def v55(work):
    lines = [f"**Line {i}**  of the   script." for i in range(10)]
    cache = {}
    h1, m1, c1 = tts_batch(lines, cache)
    raw = sum(len(l) for l in lines)
    lines[3] = "Line 3 rewritten."
    h2, m2, _ = tts_batch(lines, cache)
    h3, m3, _ = tts_batch(lines, cache, settings="s2")
    save(work, "cache.json", {"first": [h1, m1, c1], "second": [h2, m2], "settings_change": [h3, m3]})
    return [eq("first pass renders all", (h1, m1), (0, 10)), truth("pre-clean saves characters", c1 < raw, (c1, raw)),
            eq("only the changed line re-renders (90 % hits)", (h2, m2), (9, 1)), eq("settings are part of the key", m3, 10)]


PROGRAMS = {"VOICE-12": v12, "VOICE-17": v17, "VOICE-18": v18, "VOICE-19": v19, "VOICE-20": v20, "VOICE-21": v21,
            "VOICE-22": v22, "VOICE-23": v23, "VOICE-24": v24, "VOICE-25": v25, "VOICE-26": v26, "VOICE-27": v27,
            "VOICE-28": v28, "VOICE-29": v29, "VOICE-34": v34, "VOICE-35": v35, "VOICE-36": v36, "VOICE-37": v37,
            "VOICE-38": v38, "VOICE-39": v39, "VOICE-40": v40, "VOICE-41": v41, "VOICE-42": v42, "VOICE-43": v43,
            "VOICE-45": v45, "VOICE-48": v48, "VOICE-49": v49, "VOICE-50": v50, "VOICE-51": v51, "VOICE-53": v53,
            "VOICE-55": v55}
