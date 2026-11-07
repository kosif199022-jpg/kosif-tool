#!/usr/bin/env python3
"""Dragon Montage station 5 «يكتب المونتاج» — the director.

  dm_direct.py direct --job DIR                  analysis+brief+concepts+look -> edl.json
  dm_direct.py direct --job DIR --apply-review   review.json fixes -> next edl.json (old kept as edl.rN.json)

How it decides (deterministic, no randomness):
  a) candidates: speech clips -> phrases cut on word gaps (fillers and pauses > 0.4 s break a phrase and are
     never kept); non-speech clips -> one window per shot, length from the pacing range of feeling/energy
     (or the reference rhythm when reference_rhythm.json exists), placed in the steady part of the shot.
  b) every candidate is scored for each arc role (hook/setup/turn/payoff/cta/…) + quality + faces + novelty.
  c) the arc of the chosen concept is filled to brief.target_seconds with per-role budgets.
  d) with music beats, non-speech cut points are snapped to the nearest downbeat/beat (±0.15 s, else the
     elastic b-roll window is re-fitted to the beat grid); speech cuts only move inside word gaps.
  e) transitions, camera (punch-in on emphasis / to hide jump cuts) and captions come from look.json.
  f) each event carries `role`, `kind` and a concrete English + Arabic `reason`.
"""
from __future__ import annotations

import argparse
import bisect
import copy
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dm_common as dm  # noqa: E402
import dm_edl  # noqa: E402

r3 = dm_edl.r3
STATION = "direct"

# ---------------------------------------------------------------------------- vocab
FILLERS = {"امم", "اممم", "ام", "مم", "اه", "آه", "ااه", "آآ", "اا", "ا", "يعني", "إيه", "ايه", "بقى", "طيب",
           "um", "uh", "umm", "uhm", "er", "erm", "ah", "eh", "like", "hmm"}
EMPHASIS = {"جدا", "جداً", "اوي", "أوي", "خالص", "مستحيل", "ابدا", "أبدا", "أبداً", "لازم", "اهم", "أهم", "السر",
            "الحقيقة", "اخطر", "أخطر", "اول", "أول", "افضل", "أفضل", "never", "always", "secret", "truth", "best",
            "first", "only", "must", "wow"}
CTA = {"تابع", "تابعني", "تابعونا", "اشترك", "اشتركوا", "لايك", "شير", "اللينك", "الرابط", "احجز", "احجزوا", "كلمني",
       "كلمنا", "جرب", "جربوا", "يلا", "متنساش", "follow", "subscribe", "link", "book", "try", "join", "comment"}
QUESTION = {"ليه", "ازاي", "إزاي", "امتى", "إمتى", "فين", "مين", "تخيل", "تخيّل", "هل", "why", "how", "what", "imagine"}
SENT_END = re.compile(r"[.!?؟…]$")
TOKEN = re.compile(r"[\w؀-ۿ]+")
TATWEEL_REPEAT = re.compile(r"(.)\1{2,}")

# Non-speech cut length range (seconds) per feeling, scaled by energy.
PACING = {"tense": (0.6, 1.6), "playful": (0.6, 1.5), "funny": (0.7, 1.8), "epic": (1.2, 2.8),
          "inspiring": (1.4, 3.0), "warm": (1.8, 3.5), "calm": (2.5, 5.0), "sad": (2.5, 5.0)}
ROLE_WEIGHT = {"hook": 0.10, "setup": 0.22, "context": 0.22, "problem": 0.18, "turn": 0.22, "build": 0.22,
               "journey": 0.25, "climax": 0.20, "reveal": 0.18, "proof": 0.18, "payoff": 0.22, "cta": 0.10,
               "outro": 0.08}
ROLE_AR = {"hook": "خطّاف", "setup": "تمهيد", "context": "سياق", "problem": "مشكلة", "turn": "تحوّل", "build": "تصاعد",
           "journey": "رحلة", "climax": "ذروة", "reveal": "كشف", "proof": "دليل", "payoff": "حصاد", "cta": "دعوة",
           "outro": "خاتمة"}
SPEECH_SHARE = {"speech-led": 0.75, "slow-burn": 0.5, "on-beat": 0.35}
SNAP_TOL = 0.15


def norm(tok: str) -> str:
    t = re.sub(r"[ً-ْـ]", "", tok.strip().casefold())   # harakat + tatweel
    t = TATWEEL_REPEAT.sub(r"\1\1", t)
    return t.strip(".,!?؟،…:;\"'()")


def is_filler(w: dict) -> bool:
    t = norm(dm_edl.word_text(w))
    return t in FILLERS or bool(re.fullmatch(r"(ا|آ|م|ه|e|u|m|h)+", t or "x"))


def tokens(s: str) -> set[str]:
    return {norm(x) for x in TOKEN.findall(str(s)) if len(x) > 1}


# ---------------------------------------------------------------------------- inputs
def load_inputs(job: Path) -> dict:
    analysis = dm.read(job, "analysis")
    def opt(kind, default):
        try:
            return dm.read(job, kind)
        except FileNotFoundError:
            return default
    brief = opt("brief", dm.new("brief", task="", platform="reel", aspect="9:16", target_seconds=45,
                                feeling="inspiring", energy=0.5, content_type="montage", must_keep=[], avoid=[]))
    concepts = opt("concepts", dm.new("concepts", concepts=[{"id": "A", "arc": ["hook", "setup", "turn", "payoff", "cta"],
                                                              "rhythm": "on-beat", "hook": {}}],
                                      decision={"chosen": "A"}))
    look = opt("look", dm.new("look", style_id="clean", grade={"id": "none"}, transitions=[{"id": "cut"}],
                              camera=[], captions={"style": "clean", "font": "Cairo", "position": "lower"}))
    ref = None
    rf = job / "reference_rhythm.json"
    if rf.exists():
        try:
            ref = json.loads(rf.read_text(encoding="utf-8"))
        except ValueError:
            ref = None
    return {"analysis": analysis, "brief": brief, "concepts": concepts, "look": look, "reference": ref}


def chosen_concept(concepts: dict) -> dict:
    cid = (concepts.get("decision") or {}).get("chosen")
    for c in concepts.get("concepts", []):
        if c.get("id") == cid:
            return c
    return (concepts.get("concepts") or [{"id": "A", "arc": ["hook", "setup", "turn", "payoff", "cta"]}])[0]


def pacing_range(brief: dict, concept: dict, reference: dict | None) -> tuple[float, float, str]:
    if reference and (reference.get("pacing") or {}).get("mean_shot_s"):
        m = float(reference["pacing"]["mean_shot_s"])
        return max(0.4, m * 0.6), max(0.8, m * 1.5), f"reference rhythm mean {m:.2f}s"
    lo, hi = PACING.get(brief.get("feeling", ""), (1.2, 3.0))
    e = float(brief.get("energy", 0.5) if brief.get("energy") is not None else 0.5)
    f = 1.3 - 0.6 * max(0.0, min(1.0, e))
    if concept.get("rhythm") == "slow-burn":
        f *= 1.25
    return round(lo * f, 3), round(hi * f, 3), f"{brief.get('feeling', 'default')} @ energy {e:.2f}"


# ---------------------------------------------------------------------------- (a) candidates
def shot_at(clip: dict, t: float) -> dict | None:
    for s in clip.get("shots") or []:
        if s["start"] - 1e-6 <= t < s["end"] + 1e-6:
            return s
    return None


def mean_rms(clip: dict, a: float, b: float) -> float:
    en = clip.get("energy") or []
    if not en:
        return 0.0
    ts = [e["t"] for e in en]
    i, j = bisect.bisect_left(ts, a), bisect.bisect_right(ts, b)
    vals = [en[k]["rms"] for k in range(i, j)] or [en[min(i, len(en) - 1)]["rms"]]
    return sum(vals) / len(vals)


def phrases(clip: dict, max_len: float = 8.0, pause: float = 0.4) -> list[list[dict]]:
    """Split words into phrases: break on fillers, pauses > pause, silences, sentence ends, and max_len."""
    words = sorted(clip.get("words") or [], key=lambda w: (float(w["start"]), float(w["end"])))
    sil = [(float(s["start"]), float(s["end"])) for s in clip.get("silences") or [] if s["end"] - s["start"] > pause]
    out, cur = [], []
    for w in words:
        if is_filler(w):
            if cur:
                out.append(cur)
            cur = []
            continue
        if cur:
            gap_a, gap_b = float(cur[-1]["end"]), float(w["start"])
            in_sil = any(a < gap_b and b > gap_a for a, b in sil)
            if gap_b - gap_a > pause or in_sil or float(w["end"]) - float(cur[0]["start"]) > max_len:
                out.append(cur)
                cur = []
        cur.append(w)
        if SENT_END.search(dm_edl.word_text(w)):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [p for p in out if p]


def speech_candidate(clip: dict, ws: list[dict], all_words: list[dict], idx_of: dict, hook_toks: set,
                     must: set, avoid: set) -> dict:
    """A phrase -> candidate with cut points inside the gaps around it (never inside a word)."""
    first, last = ws[0], ws[-1]
    i0, i1 = idx_of[id(first)], idx_of[id(last)]
    prev_end = float(all_words[i0 - 1]["end"]) if i0 > 0 else 0.0
    next_start = float(all_words[i1 + 1]["start"]) if i1 + 1 < len(all_words) else float(clip["duration"])
    s, e = float(first["start"]), float(last["end"])
    src_in = max(prev_end + 0.02, s - 0.08, 0.0)
    src_out = min(next_start - 0.02, e + 0.12, float(clip["duration"]))
    text = " ".join(dm_edl.word_text(w) for w in ws)
    toks = tokens(text)
    shot = shot_at(clip, (s + e) / 2) or {}
    q = float((shot.get("quality") or {}).get("score", 0.5))
    emph = [dm_edl.word_text(w) for w in ws if norm(dm_edl.word_text(w)) in EMPHASIS or w.get("emphasis")
            or re.search(r"\d|!", dm_edl.word_text(w))]
    return {"kind": "speech", "clip": clip["id"], "shot": shot.get("id"), "src_in": r3(src_in), "src_out": r3(src_out),
            "dur": src_out - src_in, "text": text, "n_words": len(ws),
            "wps": len(ws) / max(0.3, e - s), "conf": sum(float(w.get("conf", 0.8)) for w in ws) / len(ws),
            "quality": q, "faces": int(shot.get("faces", 0) or 0), "motion": float(shot.get("motion_energy", 0) or 0),
            "rms": mean_rms(clip, s, e), "emphasis": emph, "question": bool(toks & QUESTION) or "؟" in text or "?" in text,
            "cta": bool(toks & CTA), "hook_overlap": len(toks & hook_toks) / max(1, len(hook_toks)) if hook_toks else 0.0,
            "must": bool(toks & must), "avoid": bool(toks & avoid), "pos": s / max(1.0, float(clip["duration"])),
            "word_gaps": [(float(ws[k]["end"]), float(ws[k + 1]["start"])) for k in range(len(ws) - 1)],
            "words": [(float(w["start"]), float(w["end"])) for w in ws],
            "pad_lo": prev_end + 0.02, "pad_hi": next_start - 0.02}


def broll_candidates(clip: dict, lo: float, hi: float, avoid_shots: set) -> list[dict]:
    out = []
    for s in clip.get("shots") or []:
        if s["id"] in avoid_shots:
            continue
        length = float(s["end"]) - float(s["start"])
        if length < max(0.4, lo * 0.6):
            continue
        L = min(hi, length * 0.85) if length > lo else length
        slack = length - L
        start = float(s["start"]) + slack * 0.35              # skip the settle-in, keep the steady middle
        q = float((s.get("quality") or {}).get("score", 0.5))
        out.append({"kind": "broll", "clip": clip["id"], "shot": s["id"], "src_in": r3(start), "src_out": r3(start + L),
                    "dur": L, "shot_start": float(s["start"]), "shot_end": float(s["end"]), "text": "",
                    "quality": q, "faces": int(s.get("faces", 0) or 0), "motion": float(s.get("motion_energy", 0) or 0),
                    "shake": float((s.get("quality") or {}).get("shake", 0) or 0),
                    "saturation": float((s.get("color") or {}).get("saturation", 0.4) or 0.4),
                    "pos": float(s["start"]) / max(1.0, float(clip.get("duration") or s["end"])),
                    "estimated": bool((s.get("quality") or {}).get("estimated")),
                    "emphasis": [], "must": False, "avoid": False, "cta": False, "question": False})
    return out


def build_candidates(analysis: dict, brief: dict, concept: dict, lo: float, hi: float) -> list[dict]:
    hook_toks = tokens((concept.get("hook") or {}).get("text", ""))
    must = set().union(*[tokens(x) for x in brief.get("must_keep") or []]) if brief.get("must_keep") else set()
    avoid = set().union(*[tokens(x) for x in brief.get("avoid") or []]) if brief.get("avoid") else set()
    cands = []
    for order, clip in enumerate(analysis.get("clips", [])):
        words = sorted(clip.get("words") or [], key=lambda w: (float(w["start"]), float(w["end"])))
        speech = len(words) >= 5
        if speech:
            idx_of = {id(w): i for i, w in enumerate(words)}
            clip = {**clip, "words": words}
            for ws in phrases(clip):
                if sum(not is_filler(w) for w in ws) < 2:
                    continue
                c = speech_candidate(clip, ws, words, idx_of, hook_toks, must, avoid)
                if c["dur"] >= 0.6:
                    cands.append(c)
            # wordless shots inside a talking clip can still serve as b-roll
            spoken = [(float(w["start"]), float(w["end"])) for w in words]
            quiet = {s["id"] for s in clip.get("shots") or []
                     if any(a < s["end"] and b > s["start"] for a, b in spoken)}
            cands += broll_candidates(clip, lo, hi, quiet)
        else:
            cands += broll_candidates(clip, lo, hi, set())
        for c in cands:
            c.setdefault("order", order)
    for i, c in enumerate(cands):
        c["cid"] = f"k{i:04d}"
    return cands


# ---------------------------------------------------------------------------- (b) scoring
def score(c: dict, role: str, hook_budget: float) -> tuple[float, str, str]:
    """Role fitness in 0..~2 plus a concrete (en, ar) reason fragment."""
    q, faces, mot = c["quality"], c["faces"], c["motion"]
    base = 0.35 * q + (0.12 if faces else 0.0) - (0.25 * c.get("shake", 0)) - (0.08 if c.get("estimated") else 0)
    if c["must"]:
        base += 0.8
    if c["avoid"]:
        base -= 1.0
    sp = c["kind"] == "speech"
    if role == "hook":
        if sp:
            short = 1.0 if c["dur"] <= hook_budget * 1.2 else max(0.0, 1 - (c["dur"] - hook_budget) / 4)
            punch = min(1.0, c["wps"] / 3.5) * 0.3 + (0.35 if c["emphasis"] else 0) + (0.3 if c["question"] else 0) \
                + 0.6 * c.get("hook_overlap", 0) + 0.4 * min(1.0, c["rms"] / 0.3)
            s = base + 0.7 * short + punch
            en = f"strongest short line ({c['dur']:.1f}s, {c['wps']:.1f} w/s{', emphasis ' + c['emphasis'][0] if c['emphasis'] else ''}{', question' if c['question'] else ''})"
            ar = f"أقوى جملة قصيرة ({c['dur']:.1f}ث){' فيها سؤال' if c['question'] else ''}{' وتأكيد «' + c['emphasis'][0] + '»' if c['emphasis'] else ''}"
        else:
            s = base + 0.9 * mot + (0.35 if faces else 0) + 0.2 * c.get("saturation", 0.4)
            en = f"most energetic shot (motion {mot:.2f}{', face' if faces else ''})"
            ar = f"أكثر لقطة فيها حركة ({mot:.2f}){' ووش واضح' if faces else ''}"
    elif role in ("setup", "context", "problem"):
        s = base + 0.6 * (1 - c["pos"]) + (0.45 if sp else 0) + (0.2 * c.get("conf", 0) if sp else 0)
        en = "early, clear statement that sets the scene" if sp else "establishing shot from early in the footage"
        ar = "جملة واضحة من الأول بتعرّف الحكاية" if sp else "لقطة تأسيسية من أول التصوير"
    elif role in ("turn", "build", "journey", "proof"):
        s = base + 0.55 * mot + 0.25 * (1 - abs(c["pos"] - 0.5) * 2) + (0.2 if c["question"] else 0)
        en = f"mid-story movement (motion {mot:.2f})" if not sp else "mid-story line that moves the story on"
        ar = f"حركة في نص الحكاية ({mot:.2f})" if not sp else "جملة من النص بتحرّك الحكاية"
    elif role in ("payoff", "climax", "reveal"):
        s = base + 0.45 * c["pos"] + (0.35 if c["emphasis"] else 0) + 0.35 * mot + 0.25 * q
        en = f"late, high-quality {'line with emphasis' if c['emphasis'] else 'moment'} (q {q:.2f})"
        ar = f"لحظة قوية متأخرة بجودة {q:.2f}{' وفيها تأكيد' if c['emphasis'] else ''}"
    elif role in ("cta", "outro"):
        s = base + (1.2 if c["cta"] else 0) + 0.5 * c["pos"] + (0.3 if sp else 0) + (0.2 if faces else 0) - 0.3 * mot
        en = "call to action spoken to camera" if c["cta"] else ("closing line" if sp else "calm closing shot")
        ar = "دعوة صريحة للمشاهد" if c["cta"] else ("جملة ختام" if sp else "لقطة ختام هادية")
    else:
        s = base + 0.3 * mot
        en, ar = "fits the arc", "مناسبة للقوس"
    return s, en, ar


# ---------------------------------------------------------------------------- (c) fill the arc
def budgets(arc: list[str], target: float, hook_first: float) -> dict:
    w = {r: ROLE_WEIGHT.get(r, 0.2) for r in arc}
    tot = sum(w.values())
    b = {r: target * w[r] / tot for r in arc}
    if "hook" in b:
        want = max(1.5, min(float(hook_first or 3.0), target * 0.15))
        diff = b["hook"] - want
        b["hook"] = want
        others = [r for r in arc if r != "hook"]
        for r in others:
            b[r] += diff / max(1, len(others))
    return b


def ranges_overlap(c: dict, used: list[dict]) -> bool:
    return any(u["clip"] == c["clip"] and c["src_in"] < u["src_out"] - 1e-6 and c["src_out"] > u["src_in"] + 1e-6
               for u in used)


def trim_speech(c: dict, max_dur: float) -> dict | None:
    """Shorten a phrase at a word gap so it fits max_dur; keeps >= 2 words. Never cuts inside a word."""
    best = None
    for k in range(len(c["words"]) - 1, 1, -1):
        end = c["words"][k - 1][1]
        nxt = c["words"][k][0]
        out = min(end + 0.12, (end + nxt) / 2)
        if out - c["src_in"] <= max_dur:
            best = (k, out)
            break
    if not best:
        return None
    k, out = best
    t = dict(c)
    t["src_out"], t["dur"] = r3(out), out - c["src_in"]
    t["words"], t["word_gaps"] = c["words"][:k], c["word_gaps"][:k - 1]
    t["pad_hi"] = c["words"][k][0] - 0.02
    t["n_words"] = k
    t["trimmed"] = True
    return t


def fit_broll(c: dict, want: float, lo: float, hi: float) -> dict:
    L = max(min(want, hi, c["shot_end"] - c["shot_start"]), min(lo, c["shot_end"] - c["shot_start"]))
    t = dict(c)
    slack = (c["shot_end"] - c["shot_start"]) - L
    t["src_in"] = r3(c["shot_start"] + slack * 0.35)
    t["src_out"] = r3(t["src_in"] + L)
    t["dur"] = L
    return t


def direct_plan(inp: dict) -> tuple[list[dict], dict, list[dict]]:
    analysis, brief, look = inp["analysis"], inp["brief"], inp["look"]
    concept = chosen_concept(inp["concepts"])
    arc = list(concept.get("arc") or ["hook", "setup", "turn", "payoff", "cta"])
    target = float(brief.get("target_seconds") or 45)
    lo, hi, pace_why = pacing_range(brief, concept, inp["reference"])
    cands = build_candidates(analysis, brief, concept, lo, hi)
    has_speech = any(c["kind"] == "speech" for c in cands)
    has_broll = any(c["kind"] == "broll" for c in cands)
    share = SPEECH_SHARE.get(concept.get("rhythm", ""), 0.5) if has_speech and has_broll else (1.0 if has_speech else 0.0)
    hook_first = float((concept.get("hook") or {}).get("first_seconds") or 3)
    bud = budgets(arc, target, hook_first)
    used: list[dict] = []
    used_shots_broll: set = set()
    shot_uses: dict = {}
    used_texts: list[set] = []
    plan: list[dict] = []
    totals = {"speech": 0.0, "broll": 0.0}
    carry = 0.0
    for role in arc:
        budget = bud[role] + carry
        filled = 0.0
        picks = []
        for _ in range(40):
            remaining = budget - filled
            if remaining < max(0.4, lo * 0.5):
                break
            best = None
            for c in cands:
                if ranges_overlap(c, used) or (c["kind"] == "broll" and c["shot"] in used_shots_broll):
                    continue
                if c["kind"] == "speech":
                    cc = c
                    slack = 1.6 if role == "hook" else 1.25
                    if c["dur"] > remaining * slack + 0.5:
                        cc = trim_speech(c, remaining * slack + 0.3)
                        if cc is None:
                            continue
                else:
                    if remaining < lo * 0.6:
                        continue
                    cc = fit_broll(c, remaining if remaining < hi else hi, lo, hi)
                s, en, ar = score(cc, role, bud.get("hook", 3.0))
                if role != "hook" and 0 < share < 1:
                    done = totals["speech"] + totals["broll"]
                    cur = totals["speech"] / done if done else share
                    want_speech = cur < share
                    s += 0.4 if (cc["kind"] == "speech") == want_speech else -0.15
                if cc.get("shot") and cc["kind"] == "speech":
                    s -= 0.05 * shot_uses.get(cc["shot"], 0)          # novelty: same talking shot again
                if cc.get("trimmed"):
                    s -= 0.15
                if cc["kind"] == "speech":
                    toks = tokens(cc["text"])
                    if any(len(toks & u) / max(1, len(toks | u)) >= 0.6 for u in used_texts):
                        s -= 1.5                                         # novelty: never say the same line twice
                    if cc["cta"] and role not in ("cta", "outro"):
                        s -= 0.6                                         # keep the ask for the end
                key = (round(s, 6), -cc["order"], -cc["src_in"])
                if best is None or key > best[0]:
                    best = (key, cc, en, ar, s)
            if best is None:
                break
            _, cc, en, ar, s = best
            cc = dict(cc, role=role, why_en=en, why_ar=ar, score=round(s, 3))
            used.append(cc)
            picks.append(cc)
            if cc["kind"] == "broll":
                used_shots_broll.add(cc["shot"])
            if cc.get("shot"):
                shot_uses[cc["shot"]] = shot_uses.get(cc["shot"], 0) + 1
            totals[cc["kind"]] += cc["dur"]
            if cc["kind"] == "speech":
                used_texts.append(tokens(cc["text"]))
            filled += cc["dur"]
            if role == "hook":
                break
        carry = budget - filled
        plan += order_role(picks, role)
    meta = {"concept": concept.get("id"), "arc": arc, "target_seconds": target, "pacing": [lo, hi], "pacing_why": pace_why,
            "speech_share_target": share, "budgets": {k: round(v, 2) for k, v in bud.items()},
            "candidates": len(cands), "candidates_speech": sum(c["kind"] == "speech" for c in cands),
            "candidates_broll": sum(c["kind"] == "broll" for c in cands)}
    return plan, meta, cands


def order_role(picks: list[dict], role: str) -> list[dict]:
    """Inside a role: speech stays chronological, b-roll is interleaved between lines (best kind first)."""
    if role == "hook" or len(picks) <= 1:
        return picks
    speech = sorted([p for p in picks if p["kind"] == "speech"], key=lambda p: (p["order"], p["src_in"]))
    broll = sorted([p for p in picks if p["kind"] == "broll"], key=lambda p: (p["order"], p["src_in"]))
    first = picks[0]["kind"]
    a, b = (speech, broll) if first == "speech" else (broll, speech)
    out = []
    while a or b:
        if a:
            out.append(a.pop(0))
        if b:
            out.append(b.pop(0))
    return out


# ---------------------------------------------------------------------------- (d) beats
def beat_grid(analysis: dict) -> tuple[list[float], list[float]]:
    m = analysis.get("music") or {}
    return sorted(float(x) for x in m.get("beats") or []), sorted(float(x) for x in m.get("downbeats") or [])


def nearest(grid: list[float], t: float) -> float | None:
    if not grid:
        return None
    i = bisect.bisect_left(grid, t)
    opts = [grid[j] for j in (i - 1, i) if 0 <= j < len(grid)]
    return min(opts, key=lambda g: (abs(g - t), g))


def snap_to_beats(events: list[dict], plans: list[dict], analysis: dict, lo: float, hi: float) -> int:
    beats, downs = beat_grid(analysis)
    if not beats:
        return 0
    snapped = 0
    edl = {"events": events}
    for i, (ev, p) in enumerate(zip(events, plans)):
        dm_edl.reflow(edl)
        if i == len(events) - 1:
            break
        nxt = events[i + 1]
        cut = ev["rec_in"] + dm_edl.event_seconds(ev) - dm_edl.overlap(nxt)
        sp = float(ev.get("speed", 1.0))
        if p["kind"] == "broll":
            lo_out = ev["src_in"] + max(0.4, lo * 0.7) * sp
            hi_out = min(p["shot_end"], ev["src_in"] + hi * 1.3 * sp)
            choice = None
            d = nearest(downs, cut)
            b = nearest(beats, cut)
            for g, label in ((d, "downbeat"), (b, "beat")):
                if g is not None and abs(g - cut) <= SNAP_TOL and lo_out <= ev["src_out"] + (g - cut) * sp <= hi_out:
                    choice = (g, label)
                    break
            if choice is None:      # elastic b-roll: re-fit to the beat grid
                for g in sorted({x for x in beats if abs(x - cut) <= 0.75}, key=lambda x: (abs(x - cut), x)):
                    if lo_out <= ev["src_out"] + (g - cut) * sp <= hi_out:
                        choice = (g, "beat (re-fit)")
                        break
            if choice:
                g, label = choice
                ev["src_out"] = r3(ev["src_out"] + (g - cut) * sp)
                ev["beat"] = {"at": r3(g), "type": label, "moved": r3(g - cut)}
                snapped += 1
        else:
            # speech: may only move inside the gap after the last kept word
            last_word_end = p["words"][-1][1]
            g_lo, g_hi = last_word_end + 0.03, p["pad_hi"]
            for g in (nearest(downs, cut), nearest(beats, cut)):
                if g is None or abs(g - cut) > SNAP_TOL:
                    continue
                new_out = ev["src_out"] + (g - cut) * sp
                if g_lo <= new_out <= g_hi:
                    ev["src_out"] = r3(new_out)
                    ev["beat"] = {"at": r3(g), "type": "beat (inside word gap)", "moved": r3(g - cut)}
                    snapped += 1
                    break
    dm_edl.reflow(edl)
    return snapped


# ---------------------------------------------------------------------------- (e) look
def look_transition(look: dict) -> dict | None:
    for t in look.get("transitions") or []:
        name = dm_edl.xfade_name(t)
        if name:
            return {"id": t.get("id", name), "xfade": name, "seconds": float(t.get("seconds", t.get("duration", 0.25)))}
    return None


def look_camera(look: dict) -> dict | None:
    for c in look.get("camera") or []:
        if c.get("id") and c["id"] not in ("static", "none"):
            return dict(c)
    return None


def apply_look(events: list[dict], plans: list[dict], look: dict) -> None:
    xf = look_transition(look)
    cam = look_camera(look)
    prev = None
    for ev, p in zip(events, plans):
        role_change = prev is not None and prev["role"] != p["role"]
        if xf and role_change and prev["kind"] == "broll" and p["kind"] == "broll":
            ev["transition_in"] = dict(xf)
            ev["reason"] += f"; {xf['xfade']} {xf['seconds']}s into the {p['role']} section (look) | انتقال {xf['xfade']} لبداية قسم {ROLE_AR.get(p['role'], p['role'])} حسب الذوق"
        else:
            ev["transition_in"] = {"id": "cut"}
        jump = prev is not None and p["kind"] == "speech" and prev["kind"] == "speech" and p.get("shot") == prev.get("shot")
        if cam and p["kind"] == "speech" and (p["emphasis"] or jump) and not (jump and prev_cam_punched(events, ev)):
            ev["camera"] = dict(cam)
            if p["emphasis"]:
                ev["reason"] += f"; {cam['id']} on «{p['emphasis'][0]}» | {cam['id']} على كلمة «{p['emphasis'][0]}»"
            else:
                ev["reason"] += f"; {cam['id']} hides the jump cut | {cam['id']} عشان يخفي القفزة"
        elif cam and p["kind"] == "broll" and p["role"] in ("hook", "climax", "payoff") and cam["id"] != "punch-in":
            ev["camera"] = dict(cam)
        else:
            ev["camera"] = {"id": "static"}
        prev = p


def prev_cam_punched(events: list[dict], ev: dict) -> bool:
    i = events.index(ev)
    return i > 0 and events[i - 1].get("camera", {}).get("id") not in (None, "static")


# ---------------------------------------------------------------------------- assemble
def to_events(plan: list[dict]) -> list[dict]:
    evs = []
    for i, p in enumerate(plan, 1):
        role_ar = ROLE_AR.get(p["role"], p["role"])
        detail = f"«{' '.join(p['text'].split()[:8])}»" if p["kind"] == "speech" else f"shot {p['shot']}"
        reason = (f"{p['role']}: {p['why_en']}, quality {p['quality']:.2f}{', face' if p['faces'] else ''} — {detail}"
                  f" | {role_ar}: {p['why_ar']}، جودة {p['quality']:.2f}")
        if p.get("trimmed"):
            reason += " (trimmed at a word gap | اتقصّت عند فاصل بين كلمتين)"
        ev = {"id": f"e{i:03d}", "clip": p["clip"], "src_in": p["src_in"], "src_out": p["src_out"], "rec_in": 0.0,
              "speed": 1.0, "transition_in": {"id": "cut"}, "camera": {"id": "static"}, "reason": reason,
              "role": p["role"], "kind": p["kind"], "shot": p.get("shot"), "score": p["score"]}
        if p["kind"] == "speech":
            ev["text"] = p["text"]
        evs.append(ev)
    return evs


def fit_duration(events: list[dict], plans: list[dict], target: float, lo: float, hi: float) -> None:
    """Final ±10% guard: stretch or shrink elastic b-roll windows inside their shots."""
    edl = {"events": events}
    dm_edl.reflow(edl)
    for _ in range(3):
        diff = target - edl["duration"]
        if abs(diff) <= target * 0.05:
            return
        elastic = [(e, p) for e, p in zip(events, plans) if p["kind"] == "broll"]
        if not elastic:
            return
        per = diff / len(elastic)
        for e, p in elastic:
            new_out = min(p["shot_end"], max(e["src_in"] + max(0.4, lo * 0.7), e["src_out"] + per))
            new_out = min(new_out, e["src_in"] + hi * 1.3)
            e["src_out"] = r3(new_out)
        dm_edl.reflow(edl)


def direct(job: Path) -> dict:
    inp = load_inputs(job)
    analysis, brief, look = inp["analysis"], inp["brief"], inp["look"]
    plan, meta, _ = direct_plan(inp)
    if not plan:
        raise SystemExit("no usable footage: analysis has no shots and no words")
    lo, hi = meta["pacing"]
    events = to_events(plan)
    fit_duration(events, plan, meta["target_seconds"], lo, hi)
    apply_look(events, plan, look)
    meta["snapped_cuts"] = snap_to_beats(events, plan, analysis, lo, hi)
    w, h = dm.ASPECTS.get(brief.get("aspect", "9:16"), (1080, 1920))
    caps = look.get("captions") or {}
    style = caps.get("style", "clean")
    music = analysis.get("music") or {}
    has_speech = any(e["kind"] == "speech" for e in events)
    for e in events:
        if e["kind"] == "broll" and music.get("path"):
            e["mute"] = True            # natural sound off under the music bed
    edl = dm.new("edl", width=w, height=h, fps=30, events=events,
                 audio={"music": {"path": music.get("path"), "gain_db": -18 if has_speech else -8,
                                  "duck_under_speech_db": -10}, "voice_from": "events",
                        "target_lufs": -14 if brief.get("platform") != "youtube" else -14},
                 captions={"enabled": style != "none" and has_speech, "style": style, "font": caps.get("font", "Cairo"),
                           "position": caps.get("position", "lower"), "words_from": "analysis"},
                 grade=dict(look.get("grade") or {"id": "none"}), duration=0.0)
    dm_edl.reflow(edl)
    edl["revision"] = 0
    edl["meta"] = {**meta, "station": STATION, "look": look.get("style_id"), "events": len(events),
                   "deviation_pct": round(100 * (edl["duration"] - meta["target_seconds"]) / meta["target_seconds"], 1)}
    problems = dm_edl.check(edl)
    if problems:
        raise SystemExit("edl check failed: " + "; ".join(problems))
    dm.write(job, "edl", edl)
    return edl


# ---------------------------------------------------------------------------- --apply-review
def _num(detail: str, default: float) -> float:
    m = re.search(r"(-?\d+(?:\.\d+)?)", detail or "")
    return float(m.group(1)) if m else default


def _word_safe(clip: dict, t: float, *, side: str) -> float:
    """Move t out of any word: to the gap before (side='in') or after (side='out')."""
    for w in clip.get("words") or []:
        s, e = float(w["start"]), float(w["end"])
        if s < t < e:
            return r3(s - 0.02) if side == "out" else r3(e + 0.02)
    return r3(t)


def apply_review(job: Path) -> dict:
    inp = load_inputs(job)
    analysis = inp["analysis"]
    review = dm.read(job, "review")
    edl = dm.read(job, "edl")
    rev = int(edl.get("revision", 0))
    (job / f"edl.r{rev}.json").write_text(json.dumps(edl, ensure_ascii=False, indent=2), encoding="utf-8")
    edl = copy.deepcopy(edl)
    clips = dm_edl.clip_index(analysis)
    by_id = {e["id"]: e for e in edl["events"]}
    applied, skipped = [], []
    rnd = review.get("round", rev + 1)
    tag_en, tag_ar = f"review r{rnd}", f"مراجعة {rnd}"
    for fx in review.get("fixes") or []:
        act, eid, detail = fx.get("action"), fx.get("event"), str(fx.get("detail", ""))
        if eid in (None, "*"):
            if act == "regrade":
                tgt = fx.get("target", "grade")
                if tgt == "audio":
                    edl["audio"]["target_lufs"] = float(fx.get("lufs", edl["audio"].get("target_lufs", -14)))
                    edl["audio"].setdefault("limiter_tp", -1.0)
                else:
                    edl["grade"] = {**edl.get("grade", {}), **({"id": fx["grade"]} if fx.get("grade") else {}),
                                    "note": detail}
                applied.append({**fx, "result": f"global {tgt}"})
            else:
                skipped.append({**fx, "why": "global fix without an event only supports regrade"})
            continue
        ev = by_id.get(eid)
        if ev is None:
            skipped.append({**fx, "why": "unknown event"})
            continue
        clip = clips.get(ev["clip"], {})
        speech = ev.get("kind") == "speech"
        note = ""
        if act == "drop":
            edl["events"].remove(ev)
            by_id.pop(eid)
            applied.append({**fx, "result": "dropped"})
            continue
        if act == "trim":
            if "src_in" in fx or "src_out" in fx:
                a = float(fx.get("src_in", ev["src_in"]))
                b = float(fx.get("src_out", ev["src_out"]))
            else:
                secs = _num(detail, 0.5)
                head = bool(re.search(r"head|start|أول|بداية|البداية", detail))
                a, b = (ev["src_in"] + secs, ev["src_out"]) if head else (ev["src_in"], ev["src_out"] - secs)
            if speech:
                a, b = _word_safe(clip, a, side="in"), _word_safe(clip, b, side="out")
            if b - a < 0.3:
                skipped.append({**fx, "why": "trim would leave < 0.3 s"})
                continue
            ev["src_in"], ev["src_out"] = r3(a), r3(b)
            note = f"trimmed to {a:.2f}-{b:.2f}"
        elif act == "retime":
            if "speed" in fx:
                ev["speed"] = max(0.5, min(2.0, float(fx["speed"])))
                note = f"speed {ev['speed']}"
            elif "rec_at" in fx:
                # move this event's out-cut to output time rec_at by changing its src_out
                dm_edl.reflow(edl)
                end_now = ev["rec_in"] + dm_edl.event_seconds(ev)
                b = ev["src_out"] + (float(fx["rec_at"]) - end_now) * float(ev.get("speed", 1.0))
                if speech:
                    b = _word_safe(clip, b, side="out")
                b = min(b, float(clip.get("duration", b)))
                if b - ev["src_in"] < 0.3:
                    skipped.append({**fx, "why": "retime would leave < 0.3 s"})
                    continue
                ev["src_out"] = r3(b)
                note = f"cut moved to {float(fx['rec_at']):.2f}s"
            else:
                ev["speed"] = max(0.5, min(2.0, _num(detail, 1.0)))
                note = f"speed {ev['speed']}"
        elif act == "regrade":
            ev["grade"] = {"id": fx.get("grade") or detail or "neutral"}
            note = f"grade {ev['grade']['id']}"
        elif act == "swap":
            new = swap_source(ev, edl, inp, fx.get("with_shot") or fx.get("with"))
            if new is None:
                skipped.append({**fx, "why": "no unused replacement"})
                continue
            ev.update(new)
            note = f"swapped to {ev['shot']}"
        else:
            skipped.append({**fx, "why": f"unknown action {act}"})
            continue
        ev["reason"] += f"; {tag_en}: {act} ({fx.get('check', detail)[:60]}) {note} | {tag_ar}: {act}"
        applied.append({**fx, "result": note})
    dm_edl.reflow(edl)
    edl["revision"] = rev + 1
    hist = edl.setdefault("history", [])
    hist.append({"revision": rev + 1, "from": f"edl.r{rev}.json", "review_round": rnd,
                 "applied": applied, "skipped": skipped})
    problems = dm_edl.check(edl)
    if problems:
        raise SystemExit("edl check failed after review: " + "; ".join(problems))
    dm.write(job, "edl", edl)
    return edl


def swap_source(ev: dict, edl: dict, inp: dict, with_shot: str | None) -> dict | None:
    brief = inp["brief"]
    concept = chosen_concept(inp["concepts"])
    lo, hi, _ = pacing_range(brief, concept, inp["reference"])
    cands = build_candidates(inp["analysis"], brief, concept, lo, hi)
    others = [e for e in edl["events"] if e is not ev]
    used_shots = {e.get("shot") for e in others if e.get("kind") == "broll"} | {ev.get("shot")}
    want = dm_edl.event_seconds(ev)
    pool = []
    for c in cands:
        if ranges_overlap(c, others) or c["kind"] != ev.get("kind", c["kind"]):
            continue
        if with_shot and c.get("shot") != with_shot:
            continue
        if not with_shot and c.get("shot") in used_shots:
            continue
        cc = fit_broll(c, want, lo, hi) if c["kind"] == "broll" else c
        s, en, ar = score(cc, ev.get("role", "turn"), 3.0)
        pool.append((-s, cc["cid"], cc, en, ar))
    if not pool:
        return None
    pool.sort(key=lambda x: (x[0], x[1]))
    _, _, c, en, ar = pool[0]
    return {"clip": c["clip"], "shot": c["shot"], "src_in": c["src_in"], "src_out": c["src_out"],
            "reason": f"{ev.get('role', 'turn')}: {en} (swap) | {ROLE_AR.get(ev.get('role'), '')}: {ar} (استبدال)"}


# ---------------------------------------------------------------------------- cli
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("direct")
    d.add_argument("--job", required=True)
    d.add_argument("--apply-review", action="store_true")
    r = sub.add_parser("apply-review")
    r.add_argument("--job", required=True)
    a = ap.parse_args(argv)
    job = Path(a.job)
    if a.cmd == "apply-review" or getattr(a, "apply_review", False):
        edl = apply_review(job)
        h = edl["history"][-1]
        print(json.dumps({"edl": str(job / "edl.json"), "revision": edl["revision"], "events": len(edl["events"]),
                          "duration": edl["duration"], "applied": len(h["applied"]), "skipped": len(h["skipped"])},
                         ensure_ascii=False))
        return 0
    edl = direct(job)
    print(json.dumps({"edl": str(job / "edl.json"), "events": len(edl["events"]), "duration": edl["duration"],
                      "target": edl["meta"]["target_seconds"], "snapped_cuts": edl["meta"]["snapped_cuts"],
                      "concept": edl["meta"]["concept"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
