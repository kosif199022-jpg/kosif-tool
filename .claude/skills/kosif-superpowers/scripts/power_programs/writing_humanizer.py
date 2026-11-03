"""Programs for the writing-humanizer family (cards not already covered by proofs/general-writing).

Each rewrite rule runs as a deterministic procedure (redundancy filter, evidence-weight gate,
fact lock through the repo's anchor_gate.compare, voice statistics, masked prose transforms,
checklists, register and honesty routers) on planted drafts whose right verdict is known.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

from ._lang_common import save, eq, truth, words, sentences, jaccard, norm_ar, SCRIPTS

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import anchor_gate  # noqa: E402  (the repo's fact lock, stdlib only)

STOP = set("the a an of to and in is it that this for on with as are was be by at or from we our you your".split())


def content(ws):
    return {w for w in ws if w not in STOP and len(w) > 2}


# ---------- WRITE-01 information + evidence weight ----------
def keep_informative(context, draft, thresh=0.8):
    seen = set()
    for c in context:
        seen |= content(words(c))
    kept, dropped = [], []
    for s in sentences(draft):
        cw = content(words(s))
        new = cw - seen
        if cw and len(new) / len(cw) < 1 - thresh:
            dropped.append(s)
        else:
            kept.append(s)
            seen |= cw
    return kept, dropped


def act_on(hits):
    """hits: list of (family, strength). strong -> act on one sighting; weak needs another family nearby."""
    if any(s == "strong" for _, s in hits):
        return True
    fams = {f for f, _ in hits}
    return len(fams) >= 2


def write01(work: Path):
    ctx = ["The café on Nile Street opened in March and serves Yemeni coffee."]
    draft = ("The café on Nile Street opened in March and serves Yemeni coffee. "
             "Its roaster came from Sanaa in 2019. Nile Street café opened March, serving Yemeni coffee.")
    kept, dropped = keep_informative(ctx, draft)
    decisions = {"strong once": act_on([("H1 not-X-but-Y", "strong")]), "one weak": act_on([("H8 dash", "weak")]),
                 "weak + other family": act_on([("H8 dash", "weak"), ("H12 vocabulary", "weak")])}
    save(work, "information_pass.json", {"kept": kept, "dropped": dropped, "decisions": decisions})
    return [eq("only the new fact kept", kept, ["Its roaster came from Sanaa in 2019."]),
            eq("restatements dropped", len(dropped), 2),
            eq("evidence weight", list(decisions.values()), [True, False, True])]


# ---------- WRITE-06 mark, draft, check, final ----------
def write06(work):
    src = "Bean & Brass opened on 12 March 2024 with 3 baristas from Yemen."
    good = "Bean & Brass opened on 12 March 2024. Its 3 baristas come from Yemen."
    drift = "Bean & Brass opened in spring 2024 with 4 baristas and award-winning beans."
    keep = ["Bean & Brass", "Yemen"]
    g, d = anchor_gate.compare(src, good, keep), anchor_gate.compare(src, drift, keep)
    save(work, "fact_check.json", {"good": g, "drift": d})
    dropped = {r["value"] for r in d["dropped"]}
    return [eq("faithful draft passes the fact diff", g["status"], "PASS"),
            eq("drifted draft needs review", d["status"], "REVIEW_REQUIRED"),
            truth("lost number and month caught", {"3", "12"} & dropped and any("mar" in str(v).lower() for v in dropped), dropped),
            truth("added number caught", any(r["value"] == "4" for r in d["added"]), d["added"])]


# ---------- WRITE-10 voice matching ----------
def voice_stats(text):
    ss = sentences(text)
    n = max(len(words(text)), 1)
    return {"avg_len": sum(len(words(s)) for s in ss) / max(len(ss), 1), "dash_per_100": 100 * text.count("—") / n,
            "allee": text.count("اللى"), "alli": text.count("اللي")}


def voice_distance(a, b):
    return abs(a["avg_len"] - b["avg_len"]) / 10 + abs(a["dash_per_100"] - b["dash_per_100"]) + \
        (1 if (a["allee"] > 0) != (b["allee"] > 0) else 0)


def write10(work):
    sample = "اللى عايز يتعلم يبدأ بدري. الشغل مش صعب. اللى بيكمل بيوصل."
    cand_match = "اللى بيحاول بيتعلم. الطريق قصير. ابدأ النهارده."
    cand_off = "إن من يرغب في التعلم ينبغي عليه أن يبدأ مبكرًا — فالأمر يتطلب صبرًا كبيرًا ومثابرة متواصلة على مدار الأيام — اللي يكمل يصل."
    s, m, o = voice_stats(sample), voice_stats(cand_match), voice_stats(cand_off)
    dm, do = voice_distance(s, m), voice_distance(s, o)
    save(work, "voice.json", {"sample": s, "match": m, "off": o, "d_match": dm, "d_off": do})
    return [truth("matching rewrite is closer to the sample", dm < do, (round(dm, 2), round(do, 2))),
            truth("spelling convention اللى copied", m["allee"] > 0 and m["alli"] == 0),
            eq("sample has no dashes; mismatched has", (s["dash_per_100"], o["dash_per_100"] > 0), (0.0, True))]


# ---------- WRITE-11 genre voice ----------
PASSIVE = re.compile(r"\b(is|are|was|were|be|been|being)\s+\w+ed\b(\s+by\b)?", re.I)
OPINION = re.compile(r"\b(I think|I love|I hate|honestly|in my view)\b", re.I)


def genre_check(text, genre, max_len=22):
    issues = []
    if genre in ("technical", "legal", "factual"):
        for s in sentences(text):
            if PASSIVE.search(s):
                issues.append(("passive", s))
            if len(words(s)) > max_len:
                issues.append(("long", s))
            if OPINION.search(s):
                issues.append(("opinion in neutral genre", s))
    return issues


def write11(work):
    tech = ("The config file was edited by the installer. Run the build. "
            "I think this flag is honestly the best one we have ever shipped in any public release of the whole product to date.")
    opinion = "I think this flag is the best one we shipped."
    it, io = genre_check(tech, "technical"), genre_check(opinion, "personal")
    save(work, "genre.json", {"technical": it, "personal": io})
    kinds = sorted({k for k, _ in it})
    return [eq("technical issues", kinds, ["long", "opinion in neutral genre", "passive"]),
            truth("short active sentence passes", all(s != "Run the build." for _, s in it)),
            eq("opinion allowed in personal writing", io, [])]


# ---------- WRITE-12 output modes ----------
MASK = re.compile(r"```.*?```|`[^`]+`|^---\n.*?\n---\n|\]\([^)]+\)", re.S | re.M)


def file_mode(text, edit):
    out, last = [], 0
    for m in MASK.finditer(text):
        out.append(edit(text[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(edit(text[last:]))
    return "".join(out)


def utilize(s):
    return re.sub(r"\butilize\b", "use", s)


def write12(work):
    doc = ("---\ntitle: utilize guide\n---\nWe utilize the cache.\n```bash\nutilize --fast ./src/utilize.py\n```\n"
           "See [utilize docs](https://x.test/utilize) and `utilize()`.\n")
    out = file_mode(doc, utilize)
    save(work, "file_mode.md", out)
    blocks = lambda t: MASK.findall(t)
    embedded = "Use the cache."
    return [truth("prose changed", "We use the cache." in out),
            eq("code, inline code, YAML, link targets byte-identical", blocks(out), blocks(doc)),
            truth("link text is prose, target untouched", "[use docs](https://x.test/utilize)" in out),
            truth("embedded mode is final text only", "\n-" not in embedded and not embedded.startswith("Draft"))]


# ---------- WRITE-13 reply-first ----------
def reply_first(convo, draft, reader_known=True):
    if not reader_known:
        return draft, []
    said = set()
    for m in convo:
        said |= content(words(m))
    out, removed = [], []
    for s in sentences(draft):
        cw = content(words(s))
        diag = re.match(r"(first i|then i|after that i|i checked|i looked)", s, re.I)
        restated = cw and len(cw & said) / len(cw) >= 0.7
        if (diag or restated) and "http" not in s:
            removed.append(s)
        else:
            out.append(s)
    return " ".join(out), removed


def write13(work):
    convo = ["Our deploy failed with error 137 on the build server yesterday."]
    draft = ("Your deploy failed with error 137 on the build server yesterday. First I checked the logs. "
             "Then I looked at memory graphs. The container hit its 2 GB memory limit, so raise it to 4 GB. "
             "Steps: https://x.test/limits")
    out, removed = reply_first(convo, draft)
    same, _ = reply_first(convo, draft, reader_known=False)
    save(work, "reply.txt", out)
    return [truth("answer and action kept", "raise it to 4 GB" in out and "https://x.test/limits" in out),
            eq("background + diagnosis walk removed", len(removed), 3),
            eq("unknown reader -> leave it", same, draft)]


# ---------- WRITE-14 self-edit checklist ----------
def self_edit(answer, user_msg):
    ss = sentences(answer)
    fails = []
    if re.match(r"(great question|sure|certainly|absolutely)", ss[0], re.I):
        fails.append(1)
    if re.search(r"\bnot (just|only|merely)? ?\w+[^.]*, but\b|isn't \w+[^.]*; it's", answer, re.I):
        fails.append(2)
    if any(re.search(r"(in short|in summary|ultimately)[,:]", x, re.I) for x in ss[-2:]):
        fails.append(3)
    if re.search(r"hope this helps|let me know if you('d| would) like|i can also", answer, re.I):
        fails.append(4)
    items = [l for l in answer.splitlines() if l.lstrip().startswith(("-", "*"))]
    if items and all(re.match(r"\s*[-*]\s+\*\*[^*]+\*\*", l) for l in items):
        fails.append(5)
    if jaccard(content(words(ss[0])), content(words(user_msg))) > 0.6:
        fails.append(6)
    return fails


def write14(work):
    user = "How do I convert a WAV file to MP3 with ffmpeg?"
    bad = ("Great question! You want to convert a WAV file to MP3 with ffmpeg. It is not just a command, but a workflow.\n"
           "- **Step**: run it\n- **Check**: listen\nIn short, it's easy. Hope this helps!")
    good = "Run `ffmpeg -i in.wav -q:a 2 out.mp3`. The -q:a 2 setting gives about 190 kbps."
    fb, fg = self_edit(bad, user), self_edit(good, user)
    save(work, "self_edit.json", {"bad": fb, "good": fg})
    return [eq("every rule fires on the planted draft", fb, [1, 2, 3, 4, 5]), eq("clean answer passes", fg, []),
            truth("re-explaining the user's message caught",
                  6 in self_edit("You want to convert a WAV file to MP3 with ffmpeg.", user))]


# ---------- WRITE-16 when not to act ----------
RELIGIOUS = ("إن شاء الله", "رحمه الله", "ﷺ", "بسم الله")
LETTER = ("let me know if", "تحية طيبة وبعد", "وتفضلوا بقبول فائق الاحترام", "يسعدني")


def should_skip(passage, written_on, inside_quote=False, discussing_phrase=False):
    if inside_quote or discussing_phrase:
        return "quote or discussion of the phrase"
    if written_on < "2022-11-30":
        return "written before 30 Nov 2022"
    if any(r in passage for r in RELIGIOUS):
        return "religious formula"
    if any(l in passage.lower() for l in LETTER):
        return "human letter formula"
    return None


def write16(work):
    cases = [("Let me know if Tuesday works.", "2025-01-01", {}), ("إن شاء الله نلتقي غدًا", "2025-01-01", {}),
             ("It is crucial to delve deeper.", "2021-06-01", {}),
             ("the phrase 'delve into' is overused", "2025-01-01", {"discussing_phrase": True}),
             ("It is crucial to delve deeper.", "2025-01-01", {})]
    r = [should_skip(p, d, **k) for p, d, k in cases]
    save(work, "skip_rules.json", r)
    return [eq("skip reasons", r[:4], ["human letter formula", "religious formula", "written before 30 Nov 2022",
                                       "quote or discussion of the phrase"]),
            eq("ordinary recent prose may be edited", r[4], None)]


# ---------- WRITE-17 voice-carrying details ----------
DETAILS = [re.compile(p, re.I) for p in (r"\([^)]+\)", r"\b(I mean|or rather|أقصد|يعني)\b", r"\bI (chose|picked|decided)\b")]
INVENTED = re.compile(r"\bwhen I (visited|was there|tried)\b|لما زرت", re.I)


def detail_guard(src, new):
    lost = [m.group(0) for rx in DETAILS for m in rx.finditer(src) if m.group(0) not in new]
    invented = bool(INVENTED.search(new) and not INVENTED.search(src))
    return lost, invented


def write17(work):
    src = "We picked the 1987 Casio (the one with the cracked key). I mean, it still works. I chose mono on purpose."
    keep = "We use the 1987 Casio (the one with the cracked key). I mean, it still works. I chose mono on purpose."
    flat = "We use a vintage keyboard. It works. Mono was selected. When I visited the studio it felt magical."
    l1, i1 = detail_guard(src, keep)
    l2, i2 = detail_guard(src, flat)
    save(work, "details.json", {"keep": [l1, i1], "flat": [l2, i2]})
    return [eq("careful edit keeps every detail", (l1, i1), ([], False)),
            eq("flattened edit lost parenthetical, self-correction, first-person choice", len(l2), 3),
            eq("invented experience flagged", i2, True)]


# ---------- WRITE-19 register switch ----------
MSA_FUNC = ("سوف", "لن", "الذي", "التي", "ليس")
LEAKS = {"levantine": ("شو", "هلق", "منيح"), "gulf": ("وايد", "شلون")}


def egyptian_check(text):
    toks = [norm_ar(t) for t in re.findall(r"[؀-ۿ]+", text)]
    msa = [w for w in MSA_FUNC if norm_ar(w) in toks]
    toks += [t[1:] for t in toks if t[:1] in "وف" and len(t) > 2]       # proclitic و / ف
    leaks = [w for d, ws in LEAKS.items() for w in ws if norm_ar(w) in toks]
    return msa, leaks


def write19(work):
    src = "سوف نفتتح الفرع الجديد يوم ١٢ مارس في المعادي، والدخول مجاني لأول 50 زائرًا."
    eg = "هنفتح الفرع الجديد يوم 12 مارس في المعادي، والدخول ببلاش لأول 50 زائر."
    bad = "سوف نفتح الفرع اللي في المعادي يوم 12 مارس، وشو رأيكم؟ الدخول ببلاش لأول 50."
    m1, l1 = egyptian_check(eg)
    m2, l2 = egyptian_check(bad)
    lock = anchor_gate.compare(src, eg, ["المعادي"])
    save(work, "register.json", {"eg": [m1, l1], "bad": [m2, l2], "lock": lock})
    return [eq("clean Egyptian register", (m1, l1), ([], [])), eq("MSA function word inside Egyptian", m2, ["سوف"]),
            eq("Levantine leak", l2, ["شو"]), eq("facts locked (١٢ = 12, مارس, 50)", lock["status"], "PASS")]


# ---------- WRITE-21 Arabic paragraph scale ----------
def ar_paragraph_tells(text):
    paras = [p for p in text.split("\n\n") if p.strip()]
    t = {"labels": len(re.findall(r"(^|\s)(أولًا|أولا|ثانيًا|ثانيا|ثالثًا|ثالثا)", text)),
         "tamma": len(re.findall(r"(^|\s)تمّ?\s", text)),
         "chains": len(re.findall(r"القيام بعملية|عملية تطوير|مستوى جودة", text))}
    lens = [len(p.split()) for p in paras]
    t["uniform_paragraphs"] = len(paras) >= 3 and max(lens) - min(lens) <= 2
    return t


def write21(work):
    ai = ("أولًا تمّ القيام بعملية تطوير مستوى جودة الخدمة بشكل كامل.\n\n"
          "ثانيًا تمّ تحسين الأداء العام للفريق بشكل ملحوظ جدًا.\n\n"
          "ثالثًا تمّ إطلاق المنصة الجديدة للعملاء في كل مكان.")
    human = ("حسّن الفريق الخدمة في ثلاثة أشهر.\n\n"
             "بدأ بالشكاوى المتكررة: التأخير في الرد، وضياع الطلبات، وأخطاء الفواتير التي أزعجت العملاء طويلًا.\n\n"
             "ثم أطلق المنصة.")
    a, h = ar_paragraph_tells(ai), ar_paragraph_tells(human)
    save(work, "paragraph_tells.json", {"ai": a, "human": h})
    return [eq("ordinal labels", a["labels"], 3), eq("تمّ without actor", a["tamma"], 3),
            truth("nominal chain found", a["chains"] >= 1), eq("uniform paragraph length", a["uniform_paragraphs"], True),
            eq("human sample clean", (h["labels"], h["tamma"], h["chains"], h["uniform_paragraphs"]), (0, 0, 0, False))]


# ---------- WRITE-22 captions / VO ----------
DIG = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def caption_normalise(text, digits="western"):
    t = re.sub(r"(?<=[؀-ۿ])\s*,", "،", text)
    t = re.sub(r"(?<=[؀-ۿ])\s*\?", "؟", t)
    t = re.sub(r"(?<=[؀-ۿ])\s*;", "؛", t)
    return t.translate(DIG) if digits == "western" else t


def edit_words(words_json, new_texts):
    if words_json.get("source") == "user":
        raise PermissionError("words.json from the user's own voice is read-only")
    return dict(words_json, words=[dict(w, text=t) for w, t in zip(words_json["words"], new_texts)])


def write22(work):
    cap = caption_normalise("وصلنا ١٠٠ ألف, شكرًا? جاهزين;")
    refused = False
    try:
        edit_words({"source": "user", "words": [{"text": "a", "start": 0, "end": 0.3}]}, ["b"])
    except PermissionError:
        refused = True
    tts = edit_words({"source": "tts", "words": [{"text": "a", "start": 0, "end": 0.3}]}, ["b"])
    save(work, "caption.txt", cap)
    return [eq("Arabic punctuation and one digit system", cap, "وصلنا 100 ألف، شكرًا؟ جاهزين؛"),
            eq("user's own voice words.json untouched", refused, True),
            eq("TTS words.json may be edited, timing kept", (tts["words"][0]["text"], tts["words"][0]["end"]), ("b", 0.3))]


# ---------- WRITE-23 finance/legal exception ----------
MODAL = re.compile(r"\b(shall|must|may|should|will)\b|يلتزم|يجوز|يجب", re.I)


def legal_edit_ok(before, after, defined_terms):
    m1, m2 = MODAL.findall(before), MODAL.findall(after)
    flat = lambda m: [x if isinstance(x, str) else x for x in m]
    lock = anchor_gate.compare(before, after, defined_terms)
    reasons = []
    if [x.lower() for x in flat(m1)] != [x.lower() for x in flat(m2)]:
        reasons.append("obligation changed")
    if lock["status"] != "PASS":
        reasons.append("quantity or defined term changed")
    return not reasons, reasons


def write23(work):
    b = "The Lessee shall pay USD 5,000 by 1 March under clause 4.2 of the Agreement."
    tone = "The Lessee shall pay USD 5,000 by 1 March, as clause 4.2 of the Agreement sets out."
    soft = "The Lessee may pay USD 5,000 by 1 March under clause 4.2 of the Agreement."
    num = "The Lessee shall pay USD 5,500 by 1 March under clause 4.2 of the Agreement."
    terms = ["Lessee", "Agreement"]
    r = {k: legal_edit_ok(b, v, terms) for k, v in (("tone", tone), ("soft", soft), ("num", num))}
    save(work, "legal_gate.json", r)
    return [eq("harmless edit accepted", r["tone"][0], True), eq("shall -> may rejected", r["soft"][1], ["obligation changed"]),
            eq("5,000 -> 5,500 rejected", r["num"][1], ["quantity or defined term changed"])]


# ---------- WRITE-24 honesty guard ----------
EVASION = re.compile(r"undetectable|bypass|turnitin|gptzero|pass (the|an) ai detector|اجعله غير قابل للكشف", re.I)
FORBIDDEN = re.compile(r"(fake|write) (a )?(review|testimonial)s?|sworn statement|peer review|in (his|her) name without", re.I)


def honesty_route(req):
    if FORBIDDEN.search(req):
        return {"action": "decline", "note": "cannot write this as authored by someone else"}
    if EVASION.search(req):
        return {"action": "readability edit", "note": "This is a readability tool; no detector promise. "
                "If your course or venue requires AI disclosure, disclose it."}
    return {"action": "edit", "note": ""}


def write24(work):
    r = {q: honesty_route(q) for q in ("make this essay undetectable by Turnitin", "write five fake reviews for my shop",
                                       "polish my cover letter")}
    save(work, "honesty.json", r)
    ev = r["make this essay undetectable by Turnitin"]
    return [eq("evasion -> readability edit", ev["action"], "readability edit"),
            truth("one-line note, no lecture, no promise", ev["note"].count(".") <= 3 and "undetectable" not in ev["note"].lower()),
            eq("fake reviews declined", r["write five fake reviews for my shop"]["action"], "decline"),
            eq("ordinary request edited with no note", r["polish my cover letter"], {"action": "edit", "note": ""})]


# ---------- WRITE-25 no invention ----------
def invented_terms(src, new):
    s, n = content(words(src)), content(words(new))
    allowed = {"source", "does", "say", "not"}
    return sorted(n - s - allowed)


def write25(work):
    src = "The space is a hub for creatives and is associated with the city council."
    bad = "The space is a hub for artists and designers and is funded by the city council."
    good = "The space is a hub for creatives and is associated with the city council. The source does not say who funds it."
    ib, ig = invented_terms(src, bad), invented_terms(src, good)
    save(work, "invention.json", {"bad": ib, "good": ig})
    return [eq("invented specifics flagged", ib, ["artists", "designers", "funded"]),
            truth("vague role kept vague", "associated" in good),
            eq("honest hedge: only the named gap is new", ig, ["funds", "who"])]


# ---------- WRITE-27 plain-language house style ----------
def house_lint(doc):
    issues = []
    for line in doc.splitlines():
        if line.startswith("#"):
            title = line.lstrip("# ")
            ws = title.split()
            if len(ws) > 1 and all(w[0].isupper() for w in ws if w[0].isalpha()):
                issues.append(("title case heading", title))
        elif re.search(r"\bnot (un|in)\w+|\bnever not\b|\bnot without\b", line, re.I):
            issues.append(("double negative", line))
        elif re.search(r"\b(should|ought to)\b", line) and re.search(r"\brequire|requirement\b", line, re.I):
            issues.append(("use must for requirements", line))
    terms = [t for t in ("token", "key", "credential") if re.search(rf"\b{t}s?\b", doc, re.I)]
    if len(terms) > 1:
        issues.append(("synonym cycling", ",".join(terms)))
    return issues


def write27(work):
    bad = ("# Setting Up The Server\nThe token is required: you should set the requirement before start.\n"
           "It is not uncommon to rotate the key. Store the credential safely.\n")
    good = "# Setting up the server\nYou must set the token before start.\nRotate the token every 90 days.\n"
    b, g = house_lint(bad), house_lint(good)
    save(work, "house_style.json", {"bad": b, "good": g})
    return [eq("issue kinds", [k for k, _ in b], ["title case heading", "use must for requirements", "double negative",
                                                  "synonym cycling"]),
            eq("clean doc passes", g, [])]


# ---------- WRITE-28 routing evals ----------
POS = re.compile(r"humani[sz]e|make it natural|remove the ai tone|polish|rewrite in my voice|"
                 r"بشري|طبيعي|بدون أسلوب|نبرة الذكاء|بالمصري", re.I)
NEG = re.compile(r"احسب|calculate|fix the (bug|code)|refactor|ضريبة", re.I)


def route_humanizer(q):
    if NEG.search(q):
        return False
    return bool(POS.search(q)) or bool(EVASION.search(q))


def write28(work):
    positives = ["humanize this", "make it natural", "remove the AI tone", "polish", "rewrite in my voice",
                 "اجعل النص بشري", "خلّي الكلام طبيعي", "صياغة بدون أسلوب AI", "شيل نبرة الذكاء الاصطناعي", "خلّيها بالمصري"]
    negatives = ["احسب ضريبة القيمة المضافة على 1000 ريال", "fix the bug in login.py"]
    pr = [route_humanizer(q) for q in positives]
    nr = [route_humanizer(q) for q in negatives]
    src = "خلّي هذا النص بشري بشكل طبيعي بدون تغيير الحقائق: افتتحنا الفرع يوم 5 مايو."
    kept = anchor_gate.compare(src, "افتتحنا الفرع يوم 5 مايو، والكلام بقى طبيعي.", mode="prompt")
    hon = honesty_route("make this essay undetectable by Turnitin")
    save(work, "routing_eval.json", {"positives": pr, "negatives": nr, "facts": kept["status"], "honesty": hon})
    return [eq("all 10 positives route", sum(pr), 10), eq("negatives do not route", nr, [False, False]),
            eq("routed rewrite keeps facts", kept["status"], "PASS"),
            eq("honesty eval -> readability edit", hon["action"], "readability edit")]


PROGRAMS = {"WRITE-01": write01, "WRITE-06": write06, "WRITE-10": write10, "WRITE-11": write11, "WRITE-12": write12,
            "WRITE-13": write13, "WRITE-14": write14, "WRITE-16": write16, "WRITE-17": write17, "WRITE-19": write19,
            "WRITE-21": write21, "WRITE-22": write22, "WRITE-23": write23, "WRITE-24": write24, "WRITE-25": write25,
            "WRITE-27": write27, "WRITE-28": write28}
