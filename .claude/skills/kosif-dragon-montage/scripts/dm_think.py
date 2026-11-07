#!/usr/bin/env python3
"""Stations 2+3 of the Dragon Montage: «يفهم المطلوب» and «يفكر بإبداع» — the thinking brain.

    dm_think.py brief    --job DIR --task "<owner text>" [--platform reel] [--seconds 45]   -> brief.json
    dm_think.py concepts --job DIR                                                         -> concepts.json (+ council_prompt.md)

brief:    reads analysis.json when it exists (speech coverage, faces, motion, usable seconds, language) and the
          owner's words, and fills kosif.dm.brief.v1 with the evidence behind every inferred field.
concepts: three concepts that differ in ARC (and mostly in rhythm), each with a hook built from the strongest
          real sentences when a transcript exists (scored by kosif-reel-hooks/reel_tools.py) or from a
          hooks_ar.json formula when it does not; one framework per Dragon Mind stage picked from
          data/mind_registry.json for that concept's emphasis, with its output filled from the job's own data;
          a weighted decision matrix with ±1-weight sensitivity (kosif-superpowers/think.py decide); a
          pre-mortem (red-team-premortem: five failure stories with different causes); and the llm_council
          prompt pack written to council_prompt.md for Claude to run. No model API is called here.

Depth over breadth: of the ~270 registry frameworks only those whose stage and video tags fit the step are
scored, and one (concepts) or three (brief) are applied. The rest are counted as "considered", never "executed".
Deterministic, stdlib only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dm_common as C  # noqa: E402

DATA = C.SKILL / "data"
STAGES = ["frame", "explore", "decide", "build", "verify", "learn"]
AR_RE = re.compile(r"[؀-ۿ]")
LATIN_RE = re.compile(r"[A-Za-z]")
DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


# ------------------------------------------------------------------------------------------- loading
def _json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def editor_mind() -> dict:
    return _json(DATA / "editor_mind.json")


def registry() -> dict:
    f = DATA / "mind_registry.json"
    if not f.exists():
        import build_mind_registry
        build_mind_registry.main([])
    return _json(f)


def _module(name: str, path: Path):
    """Import a sibling KOSIF script by path; None when it is missing or broken (never crash a station)."""
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:  # noqa: BLE001
        return None


_CACHE: dict = {}


def reel_tools():
    if "reel" not in _CACHE:
        _CACHE["reel"] = _module("dm_reel_tools", C.HOOKS / "scripts" / "reel_tools.py")
    return _CACHE["reel"]


def think_mod():
    if "think" not in _CACHE:
        _CACHE["think"] = _module("dm_sp_think", C.SP / "think.py")
    return _CACHE["think"]


def council_mod():
    if "council" not in _CACHE:
        _CACHE["council"] = _module("dm_llm_council", C.SP / "llm_council.py")
    return _CACHE["council"]


def hooks_ar() -> dict:
    f = C.HOOKS / "data" / "hooks_ar.json"
    return _json(f) if f.exists() else {"hooks": [], "rules": []}


# ------------------------------------------------------------------------------------------- text
def fold(text: str) -> str:
    t = (text or "").lower().translate(DIGITS)
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ى", "ي"), ("ة", "ه")):
        t = t.replace(a, b)
    return t


def hits(text: str, words: list) -> int:
    t = fold(text)
    return sum(1 for w in words if fold(w) in t)


def score_hook(text: str) -> dict:
    rt = reel_tools()
    if rt is None:
        n = len(text.split())
        s = 70.0 if 4 <= n <= 10 else 40.0
        return {"score": s, "verdict": "OK" if s >= 50 else "WEAK", "weakest": "LENGTH", "engine": "fallback"}
    r = rt.score_hook(text)
    return {"score": r["score"], "verdict": r["verdict"], "weakest": r["weakest"], "engine": "reel_tools.score_hook",
            "checks": {k: v["score"] for k, v in r["checks"].items()}, "flags": r["flags"]}


# ------------------------------------------------------------------------------------------- analysis facts
def load_analysis(job: Path):
    try:
        return C.read(job, "analysis"), None
    except FileNotFoundError:
        return None, "مفيش analysis.json: البريف اتبنى من كلام صاحب الطلب بس"
    except (C.ContractError, json.JSONDecodeError) as e:
        return None, f"analysis.json مش مطابق للعقد ({e}): اتجاهلناه"


def sentences(analysis) -> list:
    """Group transcript words into sentences: break on end punctuation, a gap > 0.6 s, or 16 words."""
    out = []
    for clip in (analysis or {}).get("clips", []):
        cur = []
        words = clip.get("words") or []
        for i, w in enumerate(words):
            cur.append(w)
            nxt = words[i + 1] if i + 1 < len(words) else None
            end = (re.search(r"[.!?؟،]$", str(w.get("w", ""))) or nxt is None
                   or float(nxt.get("start", 0)) - float(w.get("end", 0)) > 0.6 or len(cur) >= 16)
            if end:
                text = " ".join(str(x.get("w", "")) for x in cur).strip()
                if text:
                    conf = [float(x.get("conf", 1.0)) for x in cur]
                    out.append({"clip": clip.get("id"), "start": round(float(cur[0].get("start", 0)), 3),
                                "end": round(float(cur[-1].get("end", 0)), 3), "text": text, "words": len(cur),
                                "conf": round(sum(conf) / len(conf), 3)})
                cur = []
    for s in out:
        h = score_hook(s["text"])
        s["hook_score"] = h["score"]
        s["hook_verdict"] = h["verdict"]
    return out


def facts(analysis) -> dict:
    f = {"clips": 0, "duration": 0.0, "speech_s": 0.0, "speech_coverage": 0.0, "shots": 0, "faces_ratio": 0.0,
         "group_ratio": 0.0, "max_faces": 0, "motion_mean": 0.0, "quality_mean": 0.0, "usable_s": 0.0,
         "shaky": [], "best_shot": None, "best_motion_shot": None, "music_beats": 0, "words": 0,
         "word_lang": None, "low_conf": 0.0}
    if not analysis:
        return f
    shots, words = [], []
    for clip in analysis.get("clips", []):
        f["clips"] += 1
        f["duration"] += float(clip.get("duration") or 0)
        shots += clip.get("shots") or []
        words += clip.get("words") or []
    f["shots"] = len(shots)
    f["words"] = len(words)
    f["speech_s"] = round(sum(max(0.0, float(w.get("end", 0)) - float(w.get("start", 0))) for w in words), 3)
    f["speech_coverage"] = round(f["speech_s"] / f["duration"], 3) if f["duration"] else 0.0
    if words:
        txt = " ".join(str(w.get("w", "")) for w in words)
        f["word_lang"] = "ar-eg" if len(AR_RE.findall(txt)) >= len(LATIN_RE.findall(txt)) else "en"
        f["low_conf"] = round(sum(1 for w in words if float(w.get("conf", 1)) < 0.6) / len(words), 3)
    if shots:
        q = lambda s: float((s.get("quality") or {}).get("score", 0.5))  # noqa: E731
        f["faces_ratio"] = round(sum(1 for s in shots if (s.get("faces") or 0) >= 1) / len(shots), 3)
        f["group_ratio"] = round(sum(1 for s in shots if (s.get("faces") or 0) >= 2) / len(shots), 3)
        f["max_faces"] = max(int(s.get("faces") or 0) for s in shots)
        f["motion_mean"] = round(sum(float(s.get("motion_energy") or 0) for s in shots) / len(shots), 3)
        f["quality_mean"] = round(sum(q(s) for s in shots) / len(shots), 3)
        f["usable_s"] = round(sum(float(s["end"]) - float(s["start"]) for s in shots
                                  if q(s) >= 0.45 and float((s.get("quality") or {}).get("shake", 0)) < 0.6), 3)
        f["shaky"] = [s["id"] for s in shots if float((s.get("quality") or {}).get("shake", 0)) >= 0.6][:8]
        f["best_shot"] = max(shots, key=lambda s: (q(s), s["id"]))["id"]
        f["best_motion_shot"] = max(shots, key=lambda s: (float(s.get("motion_energy") or 0) * q(s), s["id"]))["id"]
    else:
        f["usable_s"] = round(f["duration"], 3)
    f["music_beats"] = len((analysis.get("music") or {}).get("beats") or [])
    f["duration"] = round(f["duration"], 3)
    return f


# ------------------------------------------------------------------------------------------- brief inference
TRIGGER_WORDS = ["التنين الاسود", "التنين الأسود", "تنين", "مونتاج", "منتج", "اعمل", "اعملي", "عايز", "عاوز",
                 "ثانيه", "ثانية", "ثواني", "دقيقه", "دقيقة", "فيديو", "الفيديو", "ده", "دي", "black dragon", "montage"]


def topic_of(task: str, em: dict) -> str:
    t = re.sub(r"[«»\"'،,.:؛!؟?()\-]", " ", task or "")
    t = re.sub(r"\d+", " ", t.translate(DIGITS))
    plat = [w for ws in em["platform_words"].values() for w in ws]
    drop = {fold(w) for w in TRIGGER_WORDS + plat}
    words = [w for w in t.split() if fold(w) not in drop and len(w) > 1]
    joined = " ".join(words)
    for ph in ("التنين الاسود", "التنين الأسود"):
        joined = joined.replace(ph, " ")
    feel = {fold(w) for ws in em["feeling_words"].values() for w in ws}
    drop2 = {"التنين", "الاسود", "عايزه", "عايزة", "عاوزه", "عاوزة", "عايزين", "بإحساس", "باحساس", "احساس", "يكون",
             "يبقى", "حاجه", "حاجة", "بس", "كده", "من", "غير", "بدون"}
    words = []
    for w in joined.split():
        if fold(w) in {fold(x) for x in drop2} or fold(w) in feel or fold(w).lstrip("ب") in feel:
            continue
        words.append(w)
    neg = re.search(r"(?:من غير|بدون|مش عايز|بلاش)", task or "")
    if neg:  # what the owner wants out is not the topic
        tail = {fold(x) for x in re.sub(r"[،,.]", " ", (task or "")[neg.end():]).split()[:4]}
        words = [w for w in words if fold(w) not in tail]
    if words and words[0].startswith("ل") and len(words[0]) >= 5 and not words[0].startswith(("لو", "لا", "لي")):
        words[0] = words[0][1:]      # «مونتاج لرحلتي» -> رحلتي
    return " ".join(words[:6]) or "الفيديو ده"


def pick_platform(task: str, arg, em: dict) -> tuple:
    if arg:
        return arg, "من --platform"
    for p, ws in em["platform_words"].items():
        if hits(task, ws):
            return p, "من كلام الطلب"
    return "reel", "افتراض: ريل"


def pick_content_type(task: str, f: dict, em: dict) -> tuple:
    best, n = None, 0
    for ct, spec in em["content_types"].items():
        k = hits(task, spec["words"])
        if k > n:
            best, n = ct, k
    if best:
        return best, f"من كلام الطلب ({n} كلمة دالة)"
    if f["clips"]:
        if f["speech_coverage"] >= 0.35:
            if f["group_ratio"] >= 0.3 and f["clips"] >= 2:
                return "interview", f"كلام بيغطي {f['speech_coverage']:.0%} ووشين أو أكتر في {f['group_ratio']:.0%} من اللقطات"
            return "talking-head", (f"كلام بيغطي {f['speech_coverage']:.0%} من المدة، ووش ظاهر في "
                                    f"{f['faces_ratio']:.0%} من اللقطات")
        if f["speech_coverage"] < 0.15 and f["group_ratio"] >= 0.4:
            return "event", f"كلام قليل ({f['speech_coverage']:.0%}) وناس كتير في {f['group_ratio']:.0%} من اللقطات"
        if f["speech_coverage"] >= 0.15:
            return "talking-head", f"فيه كلام ({f['speech_coverage']:.0%}) بس مش غالب: هنعامله كلام فوق لقطات"
        return "montage", f"مفيش كلام تقريبًا ({f['speech_coverage']:.0%}): مونتاج لقطات"
    return "montage", "افتراض: مفيش تحليل ولا كلمة دالة"


def pick_feeling(task: str, ct: str, em: dict) -> tuple:
    best, n = None, 0
    for feel, ws in em["feeling_words"].items():
        k = hits(task, ws)
        if k > n:
            best, n = feel, k
    if best:
        return best, "من كلام الطلب"
    d = em["content_types"][ct]["default_feeling"]
    return d, f"افتراض نوع المحتوى ({ct})"


def pick_seconds(task: str, arg, plat: dict, f: dict) -> tuple:
    why = []
    if arg:
        sec, why = float(arg), ["من --seconds"]
    else:
        m = re.search(r"(\d+)\s*(ث|ثانيه|ثانية|ثواني|s\b|sec|second)", (task or "").translate(DIGITS))
        mm = re.search(r"(\d+)\s*(دقيقه|دقيقة|دقايق|min)", (task or "").translate(DIGITS))
        if m:
            sec, why = float(m.group(1)), ["من كلام الطلب"]
        elif mm:
            sec, why = float(mm.group(1)) * 60, ["من كلام الطلب"]
        else:
            sec, why = float(plat["default_seconds"]), [f"افتراض المنصة ({plat['default_seconds']} ث)"]
    lo, hi = plat["seconds"]
    if not arg and not (lo <= sec <= hi):
        sec = min(max(sec, lo), hi)
        why.append(f"اتظبط على مدى المنصة {lo}–{hi}")
    if f["usable_s"] and sec > f["usable_s"] * 0.9:
        new = max(5.0, round(f["usable_s"] * 0.9))
        why.append(f"المادة الصالحة {f['usable_s']:.1f} ث بس، فالمدة نزلت لـ {new:.0f}")
        sec = new
    return round(sec, 1), "؛ ".join(why)


def avoid_from_task(task: str) -> list:
    out = []
    for m in re.finditer(r"(?:من غير|بدون|مش عايز|مش عاوز|ممنوع|بلاش|without|no)\s+([^،,.\n]{2,40})", task or ""):
        out.append(m.group(1).strip())
    return out


# ------------------------------------------------------------------------------------------- frameworks
def stage_pick(reg: dict, stage: str, want: dict, task: str, n: int, avoid=(), only=None) -> tuple:
    """Score every registry framework of one stage for this step; return the top n with fillers + how many were read."""
    pool = [e for e in reg["frameworks"] if e["stage"] == stage]
    rows = []
    for e in pool:
        if only is not None and e["key"] not in only:
            continue
        tags = e["video"]["tags"]
        s = sum(w * tags.get(t, 0) for t, w in want.items())
        s += 0.08 * min(3, hits(task, e.get("triggers") or []))
        s += 0.05 * len({r["source"] for r in e["sources"]})        # agreed on by several books = sturdier
        if e["key"] in avoid:
            s -= 0.35
        rows.append((round(s, 4), e["key"], e))
    rows.sort(key=lambda r: (-r[0], r[1]))
    return [r[2] for r in rows[:n]], len(pool)


def _q(s: str, n: int = 70) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def _fillers(ctx: dict) -> dict:
    """Deterministic output of each framework the brain knows how to apply, built from this job's own facts."""
    b, f, c = ctx["brief"], ctx["facts"], ctx.get("concept") or {}
    best = ctx.get("best_sentence")
    arc_ar = c.get("arc_name_ar", "")
    secs = b["target_seconds"]
    hook = (c.get("hook") or {}).get("text") or (best or {}).get("text") or ""
    beats = c.get("beats") or []
    F = {
        "first principles": lambda: (
            f"حقايق: {f['clips']} كليب، {f['duration']:.0f} ث خام، {f['usable_s']:.0f} ث صالحة، كلام {f['speech_coverage']:.0%}"
            f"{', موسيقى بـ ' + str(f['music_beats']) + ' بيت' if f['music_beats'] else ''}. أعراف مش حقايق: "
            f"«لازم مقدمة»، «لازم كل اللقطات»، «لازم موسيقى ترند». نبني من الحقايق بس: {secs:.0f} ث من أحسن المادة."),
        "problem reframing": lambda: (
            f"الطلب مش «اعمل مونتاج»؛ السؤال الحقيقي: إزاي مشاهد {b['platform']} يفضل لحد الثانية {secs:.0f} "
            f"ويحس إنه {ctx['feeling_ar']}؟"),
        "inversion": lambda: (
            "إزاي نبوّظه؟ نبدأ بمقدمة، نسيب صمت، نكرر نفس الكادر، ترجمة غلط، نهاية مفيهاش حاجة. "
            "يبقى الخطة: هوك من أول فريم، قص الصمت، تنويع الأحجام، مراجعة الترجمة، ونهاية بتلف على الهوك."),
        "golden circle": lambda: (
            f"ليه: {ctx['one_truth']} ← إزاي: {b['content_type']} بإيقاع {c.get('rhythm') or ctx.get('default_rhythm', '…')} ← إيه: "
            f"{secs:.0f} ث {b['aspect']}."),
        "tfs framing": lambda: (
            f"نفس المادة تتقدم بإطارين: مكسب («شوف اللي هتكسبه») أو خسارة («اللي بيفوتك»). "
            f"الهوك الحالي «{_q(hook, 50)}» إطاره {'خسارة' if re.search('خسر|ضاع|غلط|متعملش|بيفوت', hook) else 'مكسب'}."),
        "tfs wysiati": lambda: (
            f"المشاهد مش شايف غير اللي على الشاشة: مش عارف مين ولا فين. لازم في أول {min(5, secs):.0f} ث "
            f"معلومة واحدة تعرّفه (كارت ≤ 6 كلمات)."),
        "jobs be done": lambda: (
            f"المشاهد «بيوظّف» الفيديو ده عشان {'يتعلم حاجة في دقيقة' if b['content_type'] in ('talking-head', 'interview') else 'يحس إحساس ' + ctx['feeling_ar'] + ' من غير مجهود'}؛ "
            f"أي لقطة مش بتخدم الشغلانة دي تتشال."),
        "beautiful question": lambda: (
            f"ماذا لو بدأنا من {'آخر جملة' if best else 'أقوى لقطة'} بدل الأولى؟ وإزاي نخلي الـ{secs:.0f} ث "
            f"سؤال واحد بيتجاوب في الآخر؟"),
        "provocation po": lambda: (
            f"Po: الفيديو يمشي بالعكس. اللي يطلع منه: نبدأ بلقطة من «{beats[-1]['id'] if beats else 'الذروة'}» ثانية واحدة "
            f"وبعدين نرجع نحكي إزاي وصلنا."),
        "scamper": lambda: (
            "S بدّل الترتيب الزمني · C ادمج لقطتين في سبليت · A استعير إيقاع تريلر · M كبّر لحظة واحدة سلو موشن · "
            "P استخدم الصمت كهوك · E اشيل المقدمة · R اعكس: النهاية الأول."),
        "tfs norms surprise causes": lambda: (
            f"المشاهد متوقع {ctx['ct_ar']} عادي؛ المفاجأة اللي تكسر التوقع: "
            f"«{_q(hook, 50) or 'أول فريم من نص الحدث'}» في أول 3 ث."),
        "lateral thinking": lambda: (
            "مدخل عشوائي: «مراية». الفكرة: لقطتين متقابلتين (قبل/بعد، هو/هي، فاضي/مليان) بنفس الكادر."),
        "morphological analysis": lambda: (
            f"المحاور: قوس × إيقاع × هوك. التوليفة دي: {c.get('arc_id', '…')} × {c.get('rhythm', '…')} × "
            f"{(c.get('hook') or {}).get('formula', '…')}."),
        "medici intersection": lambda: (
            f"نخلط {ctx['ct_ar']} مع لغة {'التريلر' if b['energy'] >= 0.6 else 'الفيلم الوثائقي'}: نفس المادة بقواعد مجال تاني."),
        "six thinking hats": lambda: (
            f"أبيض: {f['usable_s']:.0f} ث صالحة · أحمر: الإحساس {ctx['feeling_ar']} · أسود: الهوك ممكن ميوصلش · "
            f"أصفر: {'فيه كلام حقيقي نبني عليه' if best else 'المادة البصرية تكفي'} · أخضر: نهاية لوب · أزرق: نختار بالمصفوفة."),
        "pugh matrix": lambda: "المصفوفة تحت في decision.matrix: كل فكرة قصاد المعايير بالأوزان، والفايز اتختبر بتغيير ±1 في كل وزن.",
        "outside view": lambda: (
            f"المرجع: ريلز {b['platform']} الشغالة بين 15 و45 ث والهوك في أول 3 ث. هدفنا {secs:.0f} ث "
            f"{'جوه' if 15 <= secs <= 45 else 'برا'} المدى ده."),
        "tfs loss aversion": lambda: (
            f"الخسارة أتقل من المكسب: الهوك يقول اللي هيضيع على المشاهد لو قفل الفيديو، مش بس اللي هيكسبه."),
        "tfs affect heuristic": lambda: (
            f"الحكم هيتبني على الإحساس قبل المعلومة: أول 3 ث لازم توصّل «{ctx['feeling_ar']}» بالصورة والصوت."),
        "one way two way doors": lambda: "اختيار الفكرة باب بيتفتح في الاتجاهين (نعيد الرندر)، النشر بس هو الباب اللي مبيرجعش: يقف عند صاحب الطلب.",
        "essentialism": lambda: f"نختار الأقل: {len(beats) or 5} بيتس بس، وكل لقطة مش بتزود معلومة جديدة تتشال.",
        "made stick success": lambda: (
            f"بسيط: فكرة واحدة «{_q(re.sub('[«»]', '', ctx['one_truth']).split(':')[0], 45)}» · غير متوقع: الهوك · ملموس: "
            f"{'رقم/اسم في الهوك' if re.search(r'[0-9٠-٩]', hook) else 'لقطة تتلمس بدل الكلام'} · "
            f"مصداقية: لقطة حقيقية من المادة · عاطفي: {ctx['feeling_ar']} · قصة: {arc_ar or 'القوس المختار'}."),
        "resonate sparkline": lambda: (
            "نبدّل بين «اللي موجود» و«اللي ممكن يكون» كل بيت: "
            + " ↔ ".join(x["id"] for x in beats[:5]) + "، والنهاية على «اللي ممكن يكون»."),
        "timed emotional arc platform tone": lambda: (
            "قوس الإحساس بالثواني: " + " · ".join(f"{x['id']} {x['start']:.0f}–{x['end']:.0f}ث" for x in beats)
            + f"؛ النبرة: {'مباشرة وعامية' if b['platform'] in ('reel', 'story') else 'أهدى وأعمق'}."),
        "storybrand": lambda: (
            f"البطل هو المشاهد مش صاحب الفيديو؛ المشكلة في أول بيت، المرشد يظهر في «{beats[1]['id'] if len(beats) > 1 else 'التمهيد'}»، "
            f"والخطة في «{beats[-2]['id'] if len(beats) > 1 else 'الحصاد'}»."),
        "hook model": lambda: (
            f"المحفز: أول فريم · الفعل: يكمّل 3 ث · المكافأة المتغيرة: {beats[2]['id'] if len(beats) > 2 else 'اللفة'} · "
            "الاستثمار: لوب في الآخر يرجعه للأول."),
        "theory mind reader model": lambda: (
            f"المشاهد بيعمل سكرول وصوته مقفول غالبًا: الهوك لازم يتفهم من الصورة والكارت لوحدهم."),
        "look serves story inside budget": lambda: (
            f"اللوك يخدم «{arc_ar or 'القوس'}»: {ctx['grade_hint']}؛ مفيش لوك يتقرر قبل ما القصة تتقفل."),
        "via negativa": lambda: "نحسّن بالحذف: نشيل المقدمة، الصمت > 0.4 ث، التكرار، وأي لقطة جودتها أقل من 0.45.",
        "pre mortem": lambda: "شوف premortem تحت: خمس قصص فشل بأسباب مختلفة، كل واحدة ليها علامة بدري وإصلاح.",
        "red team": lambda: (
            f"أقوى 3 هجمات: (1) الهوك «{_q(hook, 40)}» ممكن يتقرا عام (2) "
            f"{'الإيقاع على البيت من غير موسيقى' if c.get('rhythm') == 'on-beat' and not f['music_beats'] else 'المدة ممكن تطوّل'} "
            "(3) النهاية ممكن تقع. الإصلاح: مراجعة يتفرج وينقد بتشيك على التلاتة."),
        "cognitive bias checklist": lambda: (
            "انحياز التأكيد: إحنا حبينا الفكرة دي، فهنقيسها بنفس المعايير زي التانيين · الهالة: لقطة حلوة متخليش الجملة الضعيفة تعدي."),
        "mental simulation chosen option": lambda: (
            "محاكاة: " + " ← ".join(f"{x['id']} ({x['end'] - x['start']:.0f}ث)" for x in beats)
            + "؛ لو أي بيت أقل من 1.5 ث أو أطول من 8 ث يبقى فيه مشكلة."),
        "tfs two selves": lambda: (
            f"المشاهد هيفتكر الذروة والنهاية بس: الذروة في «{max(beats, key=lambda x: x['end'] - x['start'])['id'] if beats else '…'}» "
            f"والنهاية في «{beats[-1]['id'] if beats else '…'}»، فدول أحسن لقطتين عندنا."),
        "after action review": lambda: "بعد الرندر: كان المفروض إيه؟ حصل إيه؟ ليه الفرق؟ هنعمل إيه المرة الجاية؟ (review.json).",
    }
    return F


def fill(key: str, ctx: dict) -> str:
    fn = _fillers(ctx).get(key)
    return fn() if fn else ""


_DUMMY = {"brief": {"target_seconds": 30}, "facts": {}, "concept": None}


def filled_keys() -> set:
    """Only frameworks with a concrete filler are applied; the rest of the registry is scored, not pretended."""
    return set(_fillers(_DUMMY))


def apply_frameworks(reg: dict, stage: str, want: dict, task: str, n: int, ctx: dict, avoid=()) -> tuple:
    chosen, considered = stage_pick(reg, stage, want, task, n, avoid=avoid, only=filled_keys())
    out = []
    for e in chosen:
        out.append({"id": e["id"], "key": e["key"], "name_ar": e["name_ar"], "stage": stage,
                    "source": "+".join(sorted({r["source"] for r in e["sources"]})),
                    "sources": [f"{r['file']}#{r['id']}" for r in e["sources"]],
                    "output": fill(e["key"], ctx)})
    return out, considered


# ------------------------------------------------------------------------------------------- brief
def build_brief(job: Path, task: str, platform=None, seconds=None) -> dict:
    em, reg = editor_mind(), registry()
    analysis, note = load_analysis(job)
    f = facts(analysis)
    sents = sentences(analysis)
    plat_id, plat_why = pick_platform(task, platform, em)
    if plat_id not in em["platforms"]:
        plat_id, plat_why = "reel", f"منصة مش معروفة ({platform}): رجعنا لريل"
    plat = em["platforms"][plat_id]
    ct, ct_why = pick_content_type(task, f, em)
    feel, feel_why = pick_feeling(task, ct, em)
    fe = em["feelings"][feel]
    sec, sec_why = pick_seconds(task, seconds, plat, f)
    energy = round(0.7 * fe["energy"] + 0.3 * f["motion_mean"], 2) if f["shots"] else fe["energy"]
    lang = f["word_lang"] or ("ar-eg" if AR_RE.search(task or "") or not task else "en")
    topic = topic_of(task, em)
    best = max(sents, key=lambda s: (s["hook_score"], -s["start"]), default=None)
    one_truth = (f"«{_q(best['text'], 90)}»: دي الجملة اللي الفيديو كله يخدمها" if best
                 else f"{topic} في {sec:.0f} ثانية بإحساس {fe['name_ar']}")
    spec = em["content_types"][ct]
    must = list(spec["keep_ar"])
    if best:
        must.insert(0, f"الجملة «{_q(best['text'], 80)}» ({best['clip']} {best['start']:.2f}–{best['end']:.2f})")
    if f["best_shot"]:
        must.append(f"أحسن لقطة جودة: {f['best_shot']}")
    avoid = avoid_from_task(task) + list(spec["avoid_ar"])
    if f["shaky"]:
        avoid.append("لقطات مهزوزة: " + "، ".join(f["shaky"]))
    audience = {"reel": "ناس بتعمل سكرول على الموبايل، صوتها مقفول غالبًا، بتقرر في 3 ثواني",
                "story": "متابعين بيعدّوا الستوري بسرعة، 15 ثانية بالكتير",
                "youtube": "مشاهد قاعد قدام الشاشة ومستعد يدي وقت لو اتشد",
                "square": "فيد إنستجرام/فيسبوك، صوت مقفول",
                "landscape": "مشاهد على شاشة عرضية"}[plat_id]
    brief = C.new("brief", task=task, one_truth=one_truth, audience=audience, platform=plat_id,
                  aspect=plat["aspect"], target_seconds=sec, feeling=feel, energy=energy, language=lang,
                  content_type=ct, must_keep=must, avoid=avoid, frameworks=[])
    ctx = {"brief": brief, "facts": f, "best_sentence": best, "one_truth": one_truth, "feeling_ar": fe["name_ar"],
           "ct_ar": spec["name_ar"], "grade_hint": fe["grade_hint"], "concept": None,
           "default_rhythm": fe["rhythm"]}
    fw, considered = apply_frameworks(reg, "frame", {"story": 1.0, "hook": 0.7, "critique": 0.4}, task, 3, ctx)
    brief["frameworks"] = fw
    brief["topic"] = topic
    brief["evidence"] = {
        "platform": plat_why, "content_type": ct_why, "feeling": feel_why, "target_seconds": sec_why,
        "language": "من التفريغ" if f["word_lang"] else "من لغة الطلب",
        "analysis": note or f"analysis.json: {f['clips']} كليب، {f['shots']} لقطة، {f['words']} كلمة",
    }
    brief["facts"] = f
    brief["hook_candidates"] = [{k: s[k] for k in ("clip", "start", "end", "text", "hook_score", "hook_verdict", "conf")}
                                for s in sorted(sents, key=lambda s: (-s["hook_score"], s["start"]))[:5]]
    brief["consulted"] = {"frame_stage_frameworks_read": considered, "applied": len(fw),
                          "editor_mind": "data/editor_mind.json"}
    return brief


# ------------------------------------------------------------------------------------------- concepts
CONCEPT_WANT = {
    "classic-5": {"story": 1.0, "emotion": 0.6},
    "viral-editorial": {"hook": 1.0, "contrast": 0.9},
    "problem-agitate-solve": {"hook": 0.8, "emotion": 0.7, "contrast": 0.4},
    "journey": {"story": 1.0, "emotion": 0.9, "rhythm": 0.4},
    "countdown": {"hook": 0.8, "rhythm": 0.8},
    "before-after": {"contrast": 1.0, "rhythm": 0.5},
}
RHYTHM_WANT = {"on-beat": {"rhythm": 0.6}, "speech-led": {"hook": 0.3, "story": 0.3}, "slow-burn": {"emotion": 0.5}}
STAGE_TILT = {"verify": {"critique": 1.0}, "learn": {"emotion": 0.4, "critique": 0.6}, "decide": {"critique": 0.4}}


def choose_combos(ct: str, f: dict, feel_rhythm: str, em: dict) -> list:
    pool = [tuple(x) for x in em["content_types"][ct]["pool"]]
    speech = f["words"] > 0
    out, used_arcs = [], set()
    for arc, rhythm in pool:
        if arc in used_arcs:
            continue
        if rhythm == "speech-led" and not speech:
            rhythm = "slow-burn" if all(r != "slow-burn" for _, r in out) else "on-beat"
        out.append((arc, rhythm))
        used_arcs.add(arc)
        if len(out) == 3:
            break
    for arc in em["arcs"]:          # top up if a content type lists fewer than three arcs
        if len(out) == 3:
            break
        if arc not in used_arcs:
            out.append((arc, feel_rhythm))
            used_arcs.add(arc)
    rhythms = {r for _, r in out}
    if len(rhythms) < 2:            # the three must not share one rhythm
        alt = next(r for r in ("slow-burn", "on-beat", "speech-led") if r not in rhythms
                   and (r != "speech-led" or speech))
        out[-1] = (out[-1][0], alt)
    if feel_rhythm not in {r for _, r in out} and (feel_rhythm != "speech-led" or speech):
        out[-1] = (out[-1][0], feel_rhythm)
        if len({r for _, r in out}) < 2:
            out[-2] = (out[-2][0], next(r for r in ("on-beat", "slow-burn") if r != feel_rhythm))
    return out


def beats_for(arc: dict, target: float, hook_first: float) -> list:
    """Seconds per beat from the arc shares; an opening hook is capped at the hook window and the rest stretch."""
    durs = [target * b["share"] for b in arc["beats"]]
    if arc["beats"][0]["role"] == "hook" and durs[0] > hook_first and len(durs) > 1:
        extra = durs[0] - hook_first
        durs[0] = hook_first
        rest = sum(durs[1:])
        durs = [durs[0]] + [d + extra * d / rest for d in durs[1:]]
    out, t = [], 0.0
    for b, d in zip(arc["beats"], durs):
        out.append({"id": b["id"], "role": b["role"], "start": round(t, 2), "end": round(t + d, 2),
                    "purpose": b["purpose_ar"]})
        t += d
    if out:
        out[-1]["end"] = round(target, 2)
    return out


TOPIC_SLOTS = ("موضوع", "مهمة", "الحاجة", "حاجة", "جملة", "الطريقة الجديدة", "الجديدة")


def formula_hook(fid: int, topic: str, hooks: dict) -> tuple:
    """Fill a hooks_ar formula: the topic goes only into a slot that means "the subject"; every other slot stays
    {{slot}} for the owner (hooks_ar rule 7: never invent numbers, clients or results)."""
    h = next((x for x in hooks.get("hooks", []) if x["id"] == fid), None)
    if not h:
        return f"{topic}: اتفرج للآخر.", f"hooks_ar#{fid}", False
    text, placed = h["template"], False
    for slot in re.findall(r"\{([^}]+)\}", h["template"]):
        if not placed and any(w in slot for w in TOPIC_SLOTS):
            text, placed = text.replace("{" + slot + "}", topic, 1), True
        else:
            text = text.replace("{" + slot + "}", "{{" + slot + "}}", 1)
    return text, f"hooks_ar#{fid} {h['name']}", "{{" in text


def make_hook(arc_id: str, idx: int, sents: list, used: set, topic: str, em: dict, hooks: dict, f: dict) -> dict:
    formulas = em["hook_rules"]["arc_formulas"].get(arc_id, [3])
    fid = formulas[0]
    window = em["hook_rules"]["window_s"]
    ranked = [s for s in sorted(sents, key=lambda s: (-s["hook_score"], s["start"])) if s["text"] not in used]
    short = [s for s in ranked if s["end"] - s["start"] <= window * 2.2]
    pick = None
    if ranked:
        pool = short or ranked
        # the second and third concepts look further down the list so the three hooks differ in substance
        pick = pool[min(idx, len(pool) - 1)] if arc_id != "journey" else max(pool, key=lambda s: (s["start"], s["text"]))
    if pick:
        used.add(pick["text"])
        sc = score_hook(pick["text"])
        return {"text": pick["text"], "formula": f"transcript:{pick['clip']}@{pick['start']:.2f}-{pick['end']:.2f}",
                "closest_formula": f"hooks_ar#{fid}", "score": round(sc["score"] / 100, 2),
                "verdict": sc["verdict"], "weakest": sc["weakest"],
                "first_seconds": round(min(window, max(1.0, pick["end"] - pick["start"])), 2),
                "src": {"clip": pick["clip"], "start": pick["start"], "end": pick["end"]},
                "on_screen": " ".join(pick["text"].split()[:6]), "engine": sc["engine"],
                "visual": f"وش المتكلم أو {f['best_motion_shot']}" if f["best_motion_shot"] else "وش المتكلم"}
    text, formula, needs = formula_hook(formulas[min(idx, len(formulas) - 1)] if formulas else fid, topic, hooks)
    sc = score_hook(text.replace("{{", "").replace("}}", ""))
    return {"text": text, "formula": formula, "score": round(sc["score"] / 100, 2), "verdict": sc["verdict"],
            "weakest": sc["weakest"], "first_seconds": window, "src": None,
            "on_screen": " ".join(topic.split()[:6]),
            "needs_owner_fill": needs, "engine": sc["engine"],
            "visual": f"أعلى لقطة حركة × جودة: {f['best_motion_shot']}" if f["best_motion_shot"] else "أول لقطة فيها حركة",
            "note": "مفيش تفريغ كلام: الهوك كارت على الشاشة فوق أقوى لقطة. أي {{خانة}} يملاها صاحب الطلب، ممنوع نخترع أرقام."}


def risks_for(arc_id: str, rhythm: str, f: dict, brief: dict, arc: dict, hook: dict) -> list:
    r = []
    if rhythm == "on-beat" and not f["music_beats"]:
        r.append("مفيش موسيقى متحللة بالـ beats: هنقطع على الحركة أو نختار تراك ونحلله قبل الرندر")
    if rhythm == "speech-led" and f["low_conf"] > 0.15:
        r.append(f"{f['low_conf']:.0%} من الكلمات ثقة التفريغ فيها واطية: الترجمة محتاجة مراجعة")
    if rhythm == "slow-burn" and brief["target_seconds"] < 20:
        r.append("نار هادية في أقل من 20 ث ممكن تبان بطيئة بدل ما تبان عميقة")
    if brief["target_seconds"] < arc["min_seconds"]:
        r.append(f"القوس ده محتاج {arc['min_seconds']} ث على الأقل والهدف {brief['target_seconds']:.0f}")
    if hook.get("needs_owner_fill"):
        r.append("الهوك فيه خانة محتاجة رقم أو معلومة من صاحب الطلب")
    if hook.get("verdict") == "WEAK":
        r.append(f"الهوك ضعيف في «{hook.get('weakest')}» حسب reel_tools")
    if f["shaky"]:
        r.append(f"{len(f['shaky'])} لقطة مهزوزة لازم تتشال أو تتثبت")
    if not r:
        r.append("مفيش خطر واضح من البيانات؛ الخطر الباقي إن الهوك ميشدش في الواقع")
    return r


def premortem(brief: dict, f: dict, chosen: dict) -> list:
    """red-team-premortem: five failure stories with different causes, each with an early sign and a fix."""
    hook = chosen["hook"]
    return [
        {"cause": "hook", "story": f"الناس قفلت في أول 3 ث لأن «{_q(hook['text'], 40)}» متقريش كوعد",
         "early_sign": "retention بيقع تحت 60% في الثانية 3", "fix": "كارت ≤ 6 كلمات من أول فريم + حركة في أول لقطة"},
        {"cause": "rhythm", "story": f"الإيقاع ({chosen['rhythm']}) زهّق في النص: بيت أطول من 6 ث من غير تغيير",
         "early_sign": "review: dead-air أو لقطة أطول من max_hold", "fix": "punch-in أو B-roll كل 2–4 ث"},
        {"cause": "material", "story": f"المادة الصالحة ({f['usable_s']:.0f} ث) مكفتش وفيه لقطات اتكررت",
         "early_sign": "نفس الشوت مرتين في الـ EDL", "fix": "قصّر المدة أو اقترح لقطات تتصور/تتولد (dm_generate)"},
        {"cause": "words", "story": "الترجمة فيها كلمة غلط أو متأخرة فالمعنى باظ",
         "early_sign": f"{f['low_conf']:.0%} كلمات ثقتها واطية", "fix": "مراجعة الترجمة على الكلمات قبل الحرق"},
        {"cause": "ending", "story": "النهاية وقعت: مفيش لوب ولا دعوة فالفيديو ماتعادش",
         "early_sign": "آخر جملة مفيهاش ولا كلمة من الهوك", "fix": "آخر بيت يكرر كلمة من الهوك أو يرجع لأول لقطة"},
    ]


def council_pack(job: Path, brief: dict, concepts: list, decision: dict) -> dict:
    lc = council_mod()
    opts = "; ".join(f"{c['id']}: {c['title']} — {c['logline']}" for c in concepts)
    question = (f"«{brief['task']}» — between {opts} — which concept should the Black Dragon cut, what does it miss, "
                "and what would change the choice?")
    constraints = ["لا نخترع أرقام أو نتايج مش موجودة في المادة", f"المدة {brief['target_seconds']:.0f} ثانية {brief['aspect']}",
                   "النشر بيقف عند صاحب الطلب"]
    evidence = [brief["evidence"]["analysis"],
                f"decision matrix (think.py decide): winner {decision['chosen']}, margin {decision['sensitivity'].get('margin')}, "
                f"robust={decision['sensitivity'].get('robust')}"]
    unknowns = ["رد فعل الجمهور الحقيقي (retention) مجهول لحد النشر"]
    if lc is None:
        text = f"# Council prompt pack\n\n{question}\n\n(llm_council.py not importable; run the five voices by hand)\n"
        gate = {"depth": "STANDARD", "reason": "fallback"}
    else:
        gate = lc.gate("L2", options=3)
        framed = lc.framed_text(question, ["brief.json", "concepts.json", "analysis.json"],
                                "a wrong concept wastes a render round and the owner's trust", evidence, unknowns,
                                constraints=constraints)
        bare = lc.framed_text(question, [], "a wrong concept wastes a render round", [], [], with_context=False,
                              constraints=constraints)
        parts = ["# مجلس الخمسة — حزمة البرومنتات (Dragon Montage, station 3)", "",
                 f"Depth / العمق: **{gate['depth']}** — {gate['reason']}", "",
                 "Claude يشغّل الأصوات الخمسة (subagents بالتوازي في STANDARD/FULL، أو سطرين لكل صوت في LIGHT)، "
                 "وبعدين يكتب الحكم ويحدّث `concepts.json → decision.council.verdict`. السكربت ده ما بينادي أي موديل.", ""]
        for a in lc.ADVISORS:
            parts += [f"## {a['ar']} / {a['name']}", "", "```", lc.advisor_prompt(a, bare if a["id"] == "outsider" else framed), "```", ""]
        parts += ["## الرئيس / Chairman", "",
                  "اكتب الحكم بالأقسام: أين اتفق المجلس · أين اختلف المجلس · النقاط العمياء · التوصية (حرف الفكرة) · أول خطوة.", ""]
        text = "\n".join(parts)
    (job / "council_prompt.md").write_text(text, encoding="utf-8")
    return {"used": "llm_council", "status": "prompt_pack_ready", "prompt": "council_prompt.md", "depth": gate["depth"],
            "verdict": f"لسه: المجلس متشغّلش. الاختيار الحالي {decision['chosen']} من المصفوفة؛ Claude يشغّل council_prompt.md ويحدّث الحكم."}


def build_concepts(job: Path) -> dict:
    em, reg, hooks = editor_mind(), registry(), hooks_ar()
    brief = C.read(job, "brief")
    analysis, _ = load_analysis(job)
    f = facts(analysis)
    sents = sentences(analysis)
    best = max(sents, key=lambda s: (s["hook_score"], -s["start"]), default=None)
    fe = em["feelings"][brief["feeling"]]
    ct = brief["content_type"] if brief["content_type"] in em["content_types"] else "montage"
    target = float(brief["target_seconds"])
    topic = brief.get("topic") or topic_of(brief["task"], em)
    combos = choose_combos(ct, f, fe["rhythm"], em)
    used_hooks, used_fw, concepts, consulted = set(), set(), [], 0
    for i, (arc_id, rhythm) in enumerate(combos):
        cid = "ABC"[i]
        arc, rh = em["arcs"][arc_id], em["rhythms"][rhythm]
        hook = make_hook(arc_id, i, sents, used_hooks, topic, em, hooks, f)
        beats = beats_for(arc, target, float(hook["first_seconds"]))
        c = {"id": cid, "title": f"{arc['name_ar'].split(':')[0]} × {rh['name_ar']}",
             "logline": (f"{topic}: {' ← '.join(b['purpose'].split('،')[0] for b in beats[:3])}… "
                         f"في {target:.0f} ث، {rh['name_ar']}"),
             "arc": [b["role"] for b in beats], "arc_id": arc_id, "arc_name_ar": arc["name_ar"], "beats": beats,
             "hook": hook, "rhythm": rhythm,
             "style_hint": (f"{fe['name_ar']}: {fe['grade_hint']}؛ قطع {rh['avg_cut_s'][0]}–{rh['avg_cut_s'][1]} ث؛ "
                            f"انتقالات {'/'.join(rh['transitions'])}؛ ترجمة {em['content_types'][ct]['captions']}"),
             "cut_rule": rh["cut_rule"]}
        c["risks"] = risks_for(arc_id, rhythm, f, brief, arc, hook)
        ctx = {"brief": brief, "facts": f, "best_sentence": best, "one_truth": brief.get("one_truth", ""),
               "feeling_ar": fe["name_ar"], "ct_ar": em["content_types"][ct]["name_ar"], "grade_hint": fe["grade_hint"],
               "concept": c}
        fws = []
        for st in STAGES:
            want = dict(CONCEPT_WANT.get(arc_id, {"story": 1.0}))
            for k, v in RHYTHM_WANT[rhythm].items():
                want[k] = want.get(k, 0) + v
            for k, v in STAGE_TILT.get(st, {}).items():
                want[k] = want.get(k, 0) + v
            got, n = apply_frameworks(reg, st, want, brief["task"], 1, ctx, avoid=used_fw)
            consulted += n
            for g in got:
                used_fw.add(g["key"])
            fws += got
        c["frameworks"] = fws
        concepts.append(c)

    # --- decision: weighted matrix + ±1 sensitivity (think.py decide)
    weights = {"hook": 3, "clarity": 2, "novelty": 2, "fit": 3, "feasibility": 2}
    scores = {}
    for i, c in enumerate(concepts):
        arc = em["arcs"][c["arc_id"]]
        avg_beat = target / max(1, len(c["beats"]))
        clarity = 5 - max(0, len(c["beats"]) - 4) - (1 if target < arc["min_seconds"] else 0) - (1 if avg_beat < 2.5 else 0)
        fit = 5 - i + (1 if c["rhythm"] == fe["rhythm"] else 0) - (1 if ct not in arc["best_for"] else 0)
        feas = 5
        if c["rhythm"] == "speech-led" and not f["words"]:
            feas -= 3
        if c["rhythm"] == "on-beat" and not f["music_beats"] and f["motion_mean"] < 0.3:
            feas -= 2
        if c["rhythm"] == "slow-burn" and f["usable_s"] and f["usable_s"] < target * 1.5:
            feas -= 1
        if c["hook"].get("needs_owner_fill"):
            feas -= 1
        hook_pts = 1 + round(c["hook"]["score"] * 4) - (1 if c["hook"].get("needs_owner_fill") else 0)
        scores[c["id"]] = {"hook": max(1, min(5, hook_pts)),
                           "clarity": max(1, min(5, clarity)), "novelty": [3, 4, 5][i],
                           "fit": max(1, min(5, fit)), "feasibility": max(1, min(5, feas))}
    tm = think_mod()
    if tm is not None:
        res = tm.decide({"criteria": weights, "scores": scores})
        engine = "kosif-superpowers/scripts/think.py decide"
    else:
        tot = {o: sum(weights[k] * s[k] for k in weights) for o, s in scores.items()}
        w = max(tot, key=tot.get)
        res = {"totals": tot, "winner": w, "margin": None, "robust": None, "flips": []}
        engine = "fallback (think.py not importable)"
    matrix = [{"id": cid, "scores": s, "total": res["totals"][cid]} for cid, s in scores.items()]
    chosen = res["winner"]
    ch = next(c for c in concepts if c["id"] == chosen)
    ranked = sorted(res["totals"].items(), key=lambda kv: (-kv[1], kv[0]))
    sens = {"engine": engine, "weights": weights, "robust": res["robust"], "margin": res["margin"], "flips": res["flips"]}
    flip_txt = ("الاختيار ثابت لو غيّرنا أي وزن ±1" if res["robust"]
                else "الاختيار بيتقلب لو: " + "، ".join(f"{x['criterion']} {x['delta']:+d} ← {x['new_winner']}" for x in res["flips"][:3]))
    tie = res["totals"][chosen] == ranked[1][1]
    why = (f"{chosen} «{ch['title']}» {'اتعادل' if tie else 'كسب'} بـ {res['totals'][chosen]:g} نقطة قصاد {ranked[1][0]} ({ranked[1][1]:g})"
           f"{'، والتعادل اتكسر لصالح الأقرب لنوع المحتوى' if tie else ''}. "
           f"الهوك: «{_q(ch['hook']['text'], 60)}» ({ch['hook']['score']:.2f}). {flip_txt}"
           f"{'؛ القرار هش، فالمجلس لازم يتشغّل قبل الرندر' if not res['robust'] else ''}.")
    decision = {"chosen": chosen, "matrix": matrix, "why": why, "sensitivity": sens}
    decision["council"] = council_pack(job, brief, concepts, decision)
    pm = premortem(brief, f, ch)
    out = C.new("concepts", concepts=concepts, decision=decision,
                premortem=[f"{p['story']} — علامة بدري: {p['early_sign']} — الإصلاح: {p['fix']}" for p in pm])
    out["premortem_detail"] = pm
    out["consulted"] = {"registry_frameworks_scored": consulted, "frameworks_applied": sum(len(c["frameworks"]) for c in concepts),
                        "registry_size": len(reg["frameworks"]), "hook_sentences_scored": len(sents),
                        "hook_formulas": len(hooks.get("hooks", [])),
                        "note": "consulted = اتقرا واتقاس؛ applied = اتطبق على بيانات الشغلانة دي. ولا واحد منهم «اتنفذ» على الفيديو."}
    return out


# ------------------------------------------------------------------------------------------- cli
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Dragon Montage stations 2+3: brief and concepts")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("brief", help="«يفهم المطلوب» -> brief.json")
    b.add_argument("--job", required=True)
    b.add_argument("--task", required=True)
    b.add_argument("--platform")
    b.add_argument("--seconds", type=float)
    c = sub.add_parser("concepts", help="«يفكر بإبداع» -> concepts.json + council_prompt.md")
    c.add_argument("--job", required=True)
    a = ap.parse_args(argv)
    job = C.job_dir(a.job)
    if a.cmd == "brief":
        br = build_brief(job, a.task, a.platform, a.seconds)
        p = C.write(job, "brief", br)
        print(f"brief: {br['content_type']} · {br['platform']} {br['aspect']} · {br['target_seconds']:g}s · "
              f"{br['feeling']} · frameworks {[x['id'] for x in br['frameworks']]} -> {p}")
    else:
        cc = build_concepts(job)
        p = C.write(job, "concepts", cc)
        for x in cc["concepts"]:
            print(f"{x['id']}: {x['arc_id']} × {x['rhythm']} · hook {x['hook']['score']:.2f} «{_q(x['hook']['text'], 50)}»")
        print(f"chosen {cc['decision']['chosen']} · robust={cc['decision']['sensitivity']['robust']} -> {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
