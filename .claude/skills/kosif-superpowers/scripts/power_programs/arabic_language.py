"""Programs for the arabic-language family (cards without an existing proof script).

ARL-09 tashkeel policy, ARL-17 dialect markers and register, ARL-19 agreement after editing run as
deterministic rule procedures on planted Arabic sentences whose correct verdicts are known.
Cards needing camel-tools models, Java, Argos packages or spaCy are skipped; cards proven by
proofs/general-writing scripts are left to that proof runner.
"""
from __future__ import annotations
import re
from pathlib import Path

from ._lang_common import save, eq, truth, norm_ar, HARAKAT

# ---------- ARL-09 tashkeel policy ----------
SACRED = {"quran", "hadith", "poetry"}
AMBIGUOUS = {"علم", "عقد", "حمل"}           # bare forms a reader could misread (عَلِم/عُلِم/عِلْم)
COMMON = {"في", "من", "على", "الى", "هذا", "التي", "الذي", "كان", "مع", "عن"}


def tashkeel_for(text, kind, purpose):
    if purpose == "match":
        return HARAKAT.sub("", text)                  # keys only
    if kind in SACRED:
        return text                                   # never fix or strip
    return text


def tashkeel_tells(text):
    """Partial tashkeel on common words is a style tell; on ambiguous words it is justified."""
    tells, justified = [], []
    for w in text.split():
        if HARAKAT.search(w):
            bare = norm_ar(w)
            if bare in COMMON:
                tells.append(w)
            elif bare in AMBIGUOUS:
                justified.append(w)
    return tells, justified


def arl09(work: Path):
    ayah = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    out_display = tashkeel_for(ayah, "quran", "display")
    key = tashkeel_for(ayah, "quran", "match")
    prose = "ذهبَ الطالب فِي الصباح إلى المكتبة وقد عُلِم الخبر مِن صديقه"
    tells, ok = tashkeel_tells(prose)
    save(work, "tashkeel_policy.json", {"display": out_display, "match_key": key, "tells": tells, "justified": ok})
    return [eq("sacred text displayed byte-identical", out_display, ayah),
            truth("matching key has no harakat", not HARAKAT.search(key), key),
            eq("random tashkeel on common words flagged", tells, ["فِي", "مِن"]),
            eq("tashkeel on ambiguous word kept as justified", ok, ["عُلِم"])]


# ---------- ARL-17 dialect markers ----------
MARKERS = {"egyptian": ["مش", "اللي", "ده", "دي", "دول", "ازاي", "دلوقتي", "هيعمل", "حيعمل"],
           "levantine": ["شو", "هلق", "كتير", "منيح", "هيك"],
           "gulf": ["وايد", "شلون", "زين", "الحين"],
           "maghrebi": ["برشا", "بزاف", "واش"]}


def dialect_scores(text):
    toks = [norm_ar(t) for t in re.findall(r"[ء-يً-ْ]+", text)]
    sc = {d: sum(1 for m in ms for t in toks if norm_ar(m) in (t, t[1:] if t[:1] in "وفب" else t))
          for d, ms in MARKERS.items()}
    hits = {d: s for d, s in sc.items() if s}
    if not hits:
        return "msa", hits, False
    top = max(hits, key=hits.get)
    return top, hits, len(hits) > 1


def arl17(work):
    samples = {"eg": "انا مش فاهم ازاي ده حصل دلوقتي", "lev": "شو صار هلق؟ كتير منيح",
               "gulf": "شلون الحال؟ وايد زين", "mag": "عجبني برشا والله بزاف", "msa": "ذهب الطالب إلى المكتبة صباحا",
               "mixed": "انا مش فاهم شو صار هلق"}
    r = {k: dialect_scores(v) for k, v in samples.items()}
    save(work, "dialects.json", {k: {"dialect": v[0], "hits": v[1], "mixed": v[2]} for k, v in r.items()})
    return [eq("dialects identified", [r[k][0] for k in ("eg", "lev", "gulf", "mag", "msa")],
               ["egyptian", "levantine", "gulf", "maghrebi", "msa"]),
            truth("one-spelling register kept: pure samples not mixed", not any(r[k][2] for k in ("eg", "lev", "gulf", "mag"))),
            truth("dialect leak inside one reply flagged", r["mixed"][2], r["mixed"][1])]


# ---------- ARL-19 agreement ----------
MASC = {"يوم": "ايام", "كتاب": "كتب", "طالب": "طلاب", "رجل": "رجال"}
FEM = {"ساعه": "ساعات", "سياره": "سيارات", "ورقه": "اوراق", "طالبه": "طالبات"}
NUM_M = {"ثلاثه": 3, "اربعه": 4, "خمسه": 5, "سته": 6, "سبعه": 7, "ثمانيه": 8, "تسعه": 9, "عشره": 10}
NUM_F = {"ثلاث": 3, "اربع": 4, "خمس": 5, "ست": 6, "سبع": 7, "ثماني": 8, "تسع": 9, "عشر": 10}
PLURAL_SUBJ = {"الطلاب", "الرجال", "المهندسون", "الاطباء"}
FEM_SUBJ = {"اللجنه", "الحكومه", "الشركه"}


def agreement_errors(sentence):
    t = [norm_ar(x) for x in sentence.split()]
    errs = []
    for i in range(len(t) - 1):
        a, b = t[i], t[i + 1]
        # 3-10: reversed gender with a plural noun
        if a in NUM_M or a in NUM_F:
            sing = {v: k for k, v in {**MASC, **FEM}.items()}.get(b)
            if sing:
                masc_noun = sing in MASC
                if masc_noun and a in NUM_F:
                    errs.append(f"{a} {b}: masculine noun needs feminine-form numeral (ثلاثة)")
                if not masc_noun and a in NUM_M:
                    errs.append(f"{a} {b}: feminine noun needs masculine-form numeral (ثلاث)")
        # 11-99: singular accusative noun after the compound
        if a in ("عشر", "عشره") and i > 0 and (t[i - 1] in NUM_M or t[i - 1] in NUM_F or t[i - 1] in ("احد", "اثنا")):
            bare = b[:-1] if b.endswith("ا") else b      # drop accusative tanween alif
            if bare in MASC.values() or bare in FEM.values():
                errs.append(f"{t[i-1]} {a} {b}: 11-99 take a singular noun")
        # verb before plural subject stays singular
        if b in PLURAL_SUBJ and re.fullmatch(r"\w+وا", a):
            errs.append(f"{a} {b}: verb before a plural subject stays singular")
        if b in FEM_SUBJ and i == 0 and not a.endswith("ت") and a.startswith(("ا", "ق", "ر", "ح")):
            errs.append(f"{a} {b}: feminine subject takes a feminine verb")
    return errs


def arl19(work):
    cases = {"ثلاثة أيام": 0, "ثلاث أيام": 1, "ثلاث ساعات": 0, "ثلاثة ساعات": 1, "حضر الطلاب": 0, "حضروا الطلاب": 1,
             "خمسة عشر يوما": 0, "خمسة عشر أياما": 1, "أجّلت اللجنة الاجتماع": 0, "أجّل اللجنة الاجتماع": 1}
    got = {s: agreement_errors(s) for s in cases}
    save(work, "agreement.json", got)
    return [eq("error counts per sentence", {s: len(v) for s, v in got.items()}, cases),
            truth("3-10 gender reversal explained", "ثلاثة" in got["ثلاث أيام"][0]),
            truth("verb-subject rule explained", "singular" in got["حضروا الطلاب"][0])]


PROGRAMS = {"ARL-09": arl09, "ARL-17": arl17, "ARL-19": arl19}
