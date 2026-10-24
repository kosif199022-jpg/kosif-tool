#!/usr/bin/env python3
"""KOSIF Pro Council — an adversarial council for USIP Pro mode (USIP v5.6, appendices A13 and A30).

By default five opposing members; with --seats N (5–15) a task-fitted council drawn from the 100 unique personas of
data/council_100.json (at least one per evidence lane, the rest by request relevance), with --personas P001,P044 a
hand-picked one, and with --full all 100 (only when the user asks for the whole council).

The script does not call any model. It plans the council, writes the exact prompt for every member and round,
checks what each member returned, and computes a deterministic verdict with a receipt. The members are run by
Claude itself: five real subagents (Agent tool or Workflow) in parallel, or, when no agent tool exists, five
simulated voices in one context, which the minutes then label SIMULATED.

From the repository root:
  python3 .claude/skills/kosif-superpowers/scripts/council.py plan "<the request>" --dir out/<work>/council [--from-brief brief.json] [--options A,B,C]
        [--seats 7 | --personas P001,P022 | --full] [--personas-file data/council_100.json]
        [--roster data/experts_500.json | --no-roster]   (default: the roster index is consulted when the file exists)
  python3 .claude/skills/kosif-superpowers/scripts/council.py personas [--find "<the request>"] [--lane guardrails] [--id P021] [--seats 7]
  python3 .claude/skills/kosif-superpowers/scripts/council.py prompts --dir out/<work>/council --round 1
  python3 .claude/skills/kosif-superpowers/scripts/council.py ingest --dir out/<work>/council --round 1 --member M1 --file m1_r1.json [--simulated]
  python3 .claude/skills/kosif-superpowers/scripts/council.py status --dir out/<work>/council
  python3 .claude/skills/kosif-superpowers/scripts/council.py verdict --dir out/<work>/council

Rounds: 1 independent positions (no member sees another) · 2 cross-examination (each attacks the strongest
opposing claim and steelmans one) · 3 revised proposal and a score from 1 to 5 for every option. The verdict is
a Borda-style sum of the round-3 scores; it needs at least one recorded objection (dissent), and it is
COUNCIL_RUN only when all five members answered all three rounds as real agents with evidence.

Roster index (data/experts_500.json, built by charter_ingest.py from the user's 500-expert charter): the plan picks up
to three persona cards per member by the request/deliverable keywords and the member's lane (M5 the Guardian gets the
consent/regulated cards and a governance card from sector 50). They are an INDEX to consult, not extra members: they
never run, vote or count as evidence, and the verdict says "index consulted: N personas", never that experts ran.
Python stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _secrets  # noqa: E402

SCHEMA = "kosif.council.v1"
DEFAULT_ROSTER = HERE.parent / "data" / "experts_500.json"
DEFAULT_PERSONAS = HERE.parent / "data" / "council_100.json"
PERSONAS_SCHEMA = "kosif.council-personas.v1"
LANES = ("cross_domain", "verification", "feasibility", "audience", "guardrails")
MIN_SEATS, MAX_SEATS = 5, 15
# the brief's primary deliverable as a persona domain
PRIMARY_DOMAIN = {"reverse": "code", "text": "document"}
DIGEST_OVER = 9  # above this many members, later rounds show the others as a digest, not their full JSON
ROSTER_SCHEMA = "kosif.experts-index.v1"
PER_MEMBER = 3
# Lane affinity: keywords in a persona card and sectors of the charter that suit each evidence lane.
LANE_KEYS = {
    "cross_domain": ("ابتكار", "innovation", "مستقبل", "future", "إبداع", "creative", "تجريب", "experiment", "trend", "اتجاهات", "دمج"),
    "verification": ("جودة", "quality", "qa", "مراجع", "reviewer", "فاحص", "inspector", "مراقب", "monitor", "اختبار", "test",
                     "دقة", "accuracy", "اتساق", "consistency"),
    "feasibility": ("أدوات", "tools", "سير العمل", "workflow", "أتمتة", "automation", "render", "رندر", "تصدير", "إعدادات",
                    "pipeline", "api", "مقارن", "comparator", "تقني", "مهندس", "engineer"),
    "audience": ("جمهور", "audience", "تسويق", "marketing", "منصات", "platform", "تفاعل", "engagement", "مشاهد", "viewer",
                 "social", "نشر", "tiktok", "reels", "عمرية", "أطفال"),
    "guardrails": ("حقوق", "rights", "ملكية", "قانون", "legal", "مخاطر", "risk", "سلامة", "safety", "أصالة", "originality",
                   "ترخيص", "license", "ذوق", "taste"),
}
LANE_SECTORS = {"cross_domain": {24, 29, 49}, "verification": {5, 17}, "feasibility": {11, 12, 13, 14, 15, 16, 26},
                "audience": {18, 35}, "guardrails": {50}}
PRIMARY_KEYS = {
    "video": ("فيديو", "video", "مونتاج", "editing", "مقطع", "scene", "لقطة"),
    "motion": ("حركة", "motion", "أنيميشن", "animation", "انتقال", "transition"),
    "code": ("برمجة", "code", "programming", "automation", "api"),
    "data": ("بيانات", "data", "تحليل", "analytics"),
    "image": ("صور", "صورة", "image", "تصميم", "design"),
    "document": ("كتابة", "writing", "نصوص", "مستند", "document", "مقال", "article"),
    "research": ("بحث", "research", "مصادر"),
    "strategy": ("استراتيجية", "strategy", "تسويق", "marketing", "تسعير", "pricing", "مالية", "finance", "أعمال", "business"),
}
GOVERNANCE_SECTOR = 50
PROTOCOL = "USIP v5.6"
ROUNDS = (1, 2, 3)

# Five opposing stances; each owns a different evidence lane so the debate rests on different facts.
BASE = (
    {"id": "M1", "persona": "المبتكر الجريء", "en": "Visionary",
     "stance": "يدفع نحو الحل غير التقليدي والفكرة العابرة للمجالات، ويرفض الحل المعتاد ما لم يثبت تفوّقه",
     "lane": "cross_domain", "evidence": "قدرات بعيدة من الكتالوج (`brief` بدور cross-domain، `think.py ideas`) وأمثلة من مجالات أخرى"},
    {"id": "M2", "persona": "محامي الشيطان", "en": "Skeptic",
     "stance": "يهاجم كل ادعاء ويبحث عن سبب الفشل، ويطلب الدليل قبل القبول",
     "lane": "verification", "evidence": "اختبارات، إعادة تشغيل، قياس (`verify_video.py`، أوامر الاختبار، مطابقة الأرقام)"},
    {"id": "M3", "persona": "المهندس العملي", "en": "Builder",
     "stance": "يقيس الجدوى والوقت والتكلفة وما يعمل الآن على هذا الجهاز، ويرفض ما لا يُنفَّذ",
     "lane": "feasibility", "evidence": "`hub.py doctor` و`hub.py tool <id>` وتشغيل الأوامر وجاهزية المتطلبات"},
    {"id": "M4", "persona": "صوت الجمهور", "en": "Audience",
     "stance": "يتكلم باسم المشاهد أو المستخدم النهائي: الوضوح والأثر والمنصة واللغة، ويرفض ما يبهر الصانع ولا يصل للناس",
     "lane": "audience", "evidence": "بحث ويب ومراجع منشورة، وتحليل وسائط (لوحات لقطات، ffmpeg، وتحليل Higgsfield المأذون فقط)"},
    {"id": "M5", "persona": "الحارس", "en": "Guardian",
     "stance": "يحمي الحقوق والصدق والمال والأمان، ويعترض على أي خطوة مدفوعة أو لا رجعة فيها أو بلا رخصة",
     "lane": "guardrails", "evidence": "الرخص والأذونات والأسرار وقوانين البروتوكول (17 و25 و26)"},
)
# Domain flavour per primary deliverable: same five stances, specialised for the task.
SPECIALIZE = {
    "video": ("مخرج", "محرّر مونتاج", "مهندس رندر وموشن", "خبير منصات قصيرة", "مدقق حقوق اللقطات والصوت"),
    "motion": ("مخرج موشن", "أنيميتر ناقد", "مهندس رندر", "خبير منصات قصيرة", "مدقق حقوق الخطوط واللقطات"),
    "code": ("معماري برمجيات", "مختبِر أمان وجودة", "مهندس تنفيذ", "مستخدم المنتج", "مدقق تراخيص وأسرار"),
    "data": ("محلل استراتيجي", "مراجع حسابات", "مهندس بيانات", "صاحب القرار", "مدقق صحة الأرقام"),
    "image": ("مصمم هوية", "ناقد بصري", "مصمم إنتاج", "جمهور العلامة", "مدقق رخص الخطوط والصور"),
    "document": ("كاتب مبدع", "محرّر صارم", "منسّق مستندات", "القارئ المستهدف", "مدقق المصادر والحقوق"),
    "research": ("باحث استكشافي", "مراجع منهجي", "باحث تطبيقي", "مستفيد من البحث", "مدقق المصادر"),
    # a business decision: one seat argues against the plan and one checks the numbers before anyone commits money
    "strategy": ("مستشار استراتيجي", "محامي الشيطان ضد الخطة", "مدير مالي", "العميل المستهدف", "مدقق الافتراضات والأرقام"),
}
MEMBER_FIELDS_R1 = ("position", "claims", "proposal", "risks")
MEMBER_FIELDS_R2 = ("attacks", "steelman", "concessions")
MEMBER_FIELDS_R3 = ("final_proposal", "scores", "remaining_objection")


class CouncilError(Exception):
    def __init__(self, code: str, msg: str):
        super().__init__(msg)
        self.code = code


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def save(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CouncilError("UNREADABLE", f"{path.name}: {type(exc).__name__}") from None


def primary_of(request: str, brief: dict | None) -> str:
    if brief:
        p = ((brief.get("analysis") or {}).get("primary") or "").strip()
        if p:
            return p
    try:
        import skill_intelligence as si  # same folder
        return si.analyse(request).get("primary") or "unspecified"
    except Exception:  # analysis is a convenience: a plain council still works
        return "unspecified"


def roster(primary: str) -> list:
    spec = SPECIALIZE.get(primary)
    out = []
    for i, m in enumerate(BASE):
        r = dict(m)
        r["specialist"] = spec[i] if spec else None
        out.append(r)
    return out


def _ci():
    import charter_ingest  # same folder; shared normalisation and keyword matching
    return charter_ingest


def _stems(text: str) -> set:
    """Light-stemmed tokens plus an internal-alef-free variant (مشاهد ~ مشهد)."""
    ci = _ci()
    out = set()
    for t in ci.name_tokens(text):
        if t.isdigit():
            continue
        out.add(t)
        if t.isascii() or len(t) < 3:
            continue
        if len(t) > 3:
            out.add(t[0] + t[1:].replace("ا", ""))  # broken plurals: مشاهد ~ مشهد
        if t.endswith("ه"):
            out.add(t[:-1])  # قصه ~ قص
        if t[-1] == t[-2]:
            out.add(t[:-1])  # قصص ~ قص
    return out


def load_roster(path: Path) -> dict:
    idx = load(path)
    if idx.get("schema") != ROSTER_SCHEMA or not isinstance(idx.get("sectors"), list):
        raise CouncilError("ROSTER_INVALID", f"{path.name} is not a {ROSTER_SCHEMA} index")
    return idx


def consult_index(idx: dict, request: str, primary: str, topics: list, members: list) -> list:
    """Pick up to PER_MEMBER persona cards per member; each card goes to one member only. Deterministic."""
    ci = _ci()
    req = _stems(request + " " + " ".join(topics))
    prim = set()
    for k in PRIMARY_KEYS.get(primary, ()):
        prim |= _stems(k)
    cards = []
    for s in idx["sectors"]:
        for e in s.get("experts", []):
            fl = e.get("flags") or {}
            if fl.get("duplicate_of"):
                continue  # the earlier card of the same role stands for it
            core_text = " ".join(str(e.get(k, "")) for k in ("name_ar", "name_en", "role"))
            sec_text = s.get("name_ar", "") + " " + s.get("name_en", "")
            text = core_text + " " + str(e.get("tasks", "")) + " " + sec_text
            core, sec, st = _stems(core_text), _stems(sec_text), _stems(text)
            core_rel = len(req & core)
            rel = 3 * core_rel + 3 * len(req & sec) + len(req & _stems(str(e.get("tasks", "")))) + len(prim & st)
            padded = " " + ci.norm(text) + " "
            cards.append({"sector": s["id"], "n": e["n"], "name_ar": e.get("name_ar", ""), "role": e.get("role", ""),
                          "sensitive": fl.get("sensitive"), "boilerplate": bool(fl.get("boilerplate")), "rel": rel, "core": core_rel,
                          "lane": {lane: sum(1 for k in keys if ci._key_hit(padded, k)) + (2 if s["id"] in LANE_SECTORS[lane] else 0)
                                   for lane, keys in LANE_KEYS.items()}})
    best = max([c["rel"] for c in cards] or [0])
    floor = max(1, -(-best // 3))  # weak matches (one shared word in the tasks) do not count as relevant
    for c in cards:
        if c["rel"] < floor:
            c["rel"] = 0
    taken, picks = set(), []

    def score(c, lane):
        return 3 * c["rel"] + c["lane"][lane] - (2 if c["boilerplate"] else 0)

    guard = [m for m in members if m["lane"] == "guardrails"]
    for m in guard:  # the Guardian first: consent/regulated cards that touch the request, then a governance card
        # a consent/regulated card needs the request itself to name its role; guardrail cards need ordinary relevance
        pool = [c for c in cards if (c["sensitive"] and c["core"] > 0) or (not c["sensitive"] and c["rel"] > 0 and c["lane"]["guardrails"] > 0)]
        pool.sort(key=lambda c: (-(score(c, "guardrails") + (4 if c["sensitive"] else 0)), c["n"]))
        chosen = [c for c in pool if c["sector"] != GOVERNANCE_SECTOR and c["n"] not in taken][:PER_MEMBER - 1]
        regulated = any(c["sensitive"] == "regulated" for c in chosen)
        gov = [c for c in cards if c["sector"] == GOVERNANCE_SECTOR and c["n"] not in taken]
        want = "قانون" if regulated else "مخاطر"  # legal counsel for regulated topics, otherwise the risk manager
        gov.sort(key=lambda c: (-(c["lane"]["guardrails"] + (5 if want in ci.norm(c["name_ar"]) else 0)), c["n"]))
        chosen += gov[:1]
        for c in chosen:
            taken.add(c["n"])
            picks.append((m["id"], c))
    others = [m for m in members if m["lane"] != "guardrails"]  # consent/regulated cards stay with the Guardian
    pairs = sorted(((score(c, m["lane"]), i, c["n"], m, c) for i, m in enumerate(others) for c in cards if c["rel"] > 0 and not c["sensitive"]),
                   key=lambda t: (-t[0], t[1], t[2]))
    count = {m["id"]: 0 for m in others}
    for _sc, _i, _n, m, c in pairs:
        if c["n"] in taken or count[m["id"]] >= PER_MEMBER:
            continue
        taken.add(c["n"])
        count[m["id"]] += 1
        picks.append((m["id"], c))
    order = {m["id"]: i for i, m in enumerate(members)}
    picks.sort(key=lambda p: (order[p[0]], p[1]["n"]))
    return [{"member": mid, "sector": c["sector"], "n": c["n"], "name_ar": c["name_ar"], "role": c["role"],
             "sensitive": c["sensitive"]} for mid, c in picks]


def cmd_plan(a) -> dict:
    _secrets.refuse_secrets(request=a.request)
    d = Path(a.dir)
    if (d / "council.json").exists() and not a.force:
        raise CouncilError("EXISTS", f"{d}/council.json exists (use --force to replace it)")
    brief = load(Path(a.from_brief)) if a.from_brief else None
    if brief is not None and not (brief.get("coverage") or {}).get("complete"):
        raise CouncilError("BRIEF_INCOMPLETE", "the brief's coverage receipt is not complete=true")
    options = [o.strip() for o in (a.options or "").split(",") if o.strip()]
    if not options and brief and isinstance(brief.get("plans"), dict):
        options = sorted(k for k, v in brief["plans"].items() if v)
    if not options:
        options = ["A", "B", "C"]
    primary = primary_of(a.request, brief)
    topics = [str(t) for t in ((brief or {}).get("analysis") or {}).get("topics") or []]
    picked = [x.strip().upper() for x in (a.personas or "").split(",") if x.strip()]
    if sum(bool(x) for x in (a.seats, picked, a.full)) > 1:
        raise CouncilError("MODE_CONFLICT", "choose one of --seats, --personas or --full")
    mode, personas_meta = "classic5", None
    if a.seats or picked or a.full:
        ppath = Path(a.personas_file) if a.personas_file else DEFAULT_PERSONAS
        if not ppath.exists():
            raise CouncilError("PERSONAS_MISSING", f"{ppath} does not exist")
        pool = load_personas(ppath)
        if a.full:
            mode, chosen = "full", select_personas(pool, a.request, primary, len(pool), topics)
        elif picked:
            byid = {p["id"]: p for p in pool}
            bad = [x for x in picked if x not in byid]
            if bad:
                raise CouncilError("UNKNOWN_PERSONA", ", ".join(bad))
            if len(set(picked)) != len(picked) or not MIN_SEATS <= len(picked) <= MAX_SEATS:
                raise CouncilError("SEATS_RANGE", f"--personas needs {MIN_SEATS}–{MAX_SEATS} distinct ids")
            sc = persona_scores(pool, a.request, primary, topics)
            mode, chosen = "picked", [dict(byid[x], score=sc[x]) for x in picked]
        else:
            if not MIN_SEATS <= a.seats <= MAX_SEATS:
                raise CouncilError("SEATS_RANGE", f"--seats must be {MIN_SEATS}–{MAX_SEATS} (use --full for the whole council)")
            mode, chosen = "seats", select_personas(pool, a.request, primary, a.seats, topics)
        members = persona_members(chosen)
        personas_meta = {"file": str(ppath), "schema": PERSONAS_SCHEMA, "pool": len(pool),
                         "chosen": [{"member": m["id"], "persona": m["persona_id"], "lane": m["lane"], "score": p["score"]}
                                    for m, p in zip(members, chosen)],
                         "lanes": sorted({m["lane"] for m in members})}
    else:
        members = roster(primary)
    roster_path = None if a.no_roster else (Path(a.roster) if a.roster else (DEFAULT_ROSTER if DEFAULT_ROSTER.exists() else None))
    consulted, index_meta = [], None
    if roster_path is not None:
        if not roster_path.exists():
            raise CouncilError("ROSTER_MISSING", f"{roster_path} does not exist")
        idx = load_roster(roster_path)
        consulted = consult_index(idx, a.request, primary, topics, members)
        index_meta = {"file": str(roster_path), "schema": idx.get("schema"),
                      "source_sha256": (idx.get("source") or {}).get("sha256"),
                      "note": "index, not executed experts: persona cards consulted by members; none ran, reviewed or voted"}
    council = {
        "schema": SCHEMA, "protocol": PROTOCOL, "created_at": now_iso(), "request": a.request,
        "request_sha256": sha256_bytes(a.request.encode("utf-8")), "primary": primary, "options": options,
        "brief": {"file": a.from_brief, "recommended": brief.get("recommended")} if brief else None,
        "roster": members, "rounds": {str(r): {} for r in ROUNDS}, "mode": mode, "seats": len(members),
        "personas": personas_meta,
        "consulted_index": consulted, "roster_index": index_meta,
        "rules": [
            "Round 1 members answer independently: never show one member another's answer in round 1.",
            "Every claim names its evidence (a command run, a file read, a URL, a measurement) or says 'opinion'.",
            "Round 2 attacks the strongest opposing claim and steelmans one other member's position.",
            "Round 3 scores every option from 1 to 5 and states one remaining objection (or 'none').",
            "No member spends money, publishes, or generates media: paid or irreversible steps go to the user.",
            "Consulted persona cards are an index, not members: they never vote, run or count as evidence.",
            "A council persona is a stance prompt: the member only counts when Claude ran it as an agent (else SIMULATED).",
        ],
    }
    save(d / "council.json", council)
    return {"dir": str(d), "primary": primary, "options": options, "mode": mode, "seats": len(members),
            "index_consulted": f"index consulted: {len(consulted)} personas (an index, not executed experts)",
            "members": [f"{m['id']} {m['persona']}" + (f" ({m['specialist']})" if m["specialist"] else "") for m in council["roster"]]}


def member_prompt(c: dict, m: dict, rnd: int) -> str:
    who = m["persona"] + (f" — {m['specialist']}" if m.get("specialist") else "")
    n = len(c["roster"])
    head = (f"You are council member {m['id']} «{who}» ({m['en']}) in a {n}-member KOSIF Pro council (USIP v5.6, appendices A13/A30).\n"
            f"Your stance: {m['stance']}.\n" + persona_block(c, m) +
            f"Your evidence lane: {m['evidence']}. Gather real evidence in that lane before you claim anything;"
            " label anything without evidence as 'opinion'. Never spend money, publish, or generate images or video "
            "(Katana only through a verified zero-credit read-only analysis, never generation; other Higgsfield analysis only if the user approved its cost).\n"
            f"Request: «{c['request']}»\nOptions under debate: {', '.join(c['options'])}"
            + (f" (the USIP brief recommends {c['brief']['recommended']})" if c.get("brief") and c["brief"].get("recommended") else "") + ".\n"
            + personas_line(c, m))
    if rnd == 1:
        body = ("ROUND 1 — independent position. You have not seen the other members. Return ONLY JSON:\n"
                '{"position": "<your thesis in one sentence>", "claims": [{"claim": "...", "evidence": "<command/file/url/measurement or opinion>", '
                '"confidence": 0.0}], "proposal": "<what you would do, concretely>", "risks": ["..."]}')
    elif rnd == 2:
        others = {k: v for k, v in c["rounds"]["1"].items() if k != m["id"]}
        if n > DIGEST_OVER:
            others = digest_r1(others)
        body = ("ROUND 2 — cross-examination. These are the other members' round-1 answers:\n"
                + json.dumps(others, ensure_ascii=False, indent=1) + counterpart_line(c, m) +
                "\nAttack the strongest claim that contradicts you (with evidence), steelman one other member, and concede what you must. Return ONLY JSON:\n"
                '{"attacks": [{"target": "M?", "claim": "...", "counter": "...", "evidence": "..."}], "steelman": {"target": "M?", "why_strong": "..."}, '
                '"concessions": ["..."]}')
    else:
        r1 = c["rounds"]["1"]
        r2 = c["rounds"]["2"]
        if n > DIGEST_OVER:
            r1, r2 = digest_r1(r1), digest_r2(r2)
        body = ("ROUND 3 — convergence and vote. Round 1 positions and round 2 cross-examination:\n"
                + json.dumps({"round1": r1, "round2": r2}, ensure_ascii=False, indent=1) +
                f"\nGive your revised proposal and score EVERY option ({', '.join(c['options'])}) from 1 (worst) to 5 (best). Return ONLY JSON:\n"
                '{"final_proposal": "...", "scores": {"<option>": 1}, "changed_mind": "<what changed your view, or none>", '
                '"remaining_objection": "<your strongest objection that still stands, or none>"}')
    return head + body


def persona_block(c: dict, m: dict) -> str:
    """The persona card of a member drawn from the 100-persona roster (empty for the classic five)."""
    p = m.get("card")
    if not p:
        return ""
    return (f"Your character ({p['id']} {p['name_en']}, {p['title_en']}): {p['character_ar']}\n"
            f"Your lens: {p['lens_en']}. Your superpowers: " + "; ".join(p["superpowers"]) + ".\n"
            "Ask these signature questions of the request and of every option: " + " / ".join(p["signature_questions"]) + "\n"
            f"Your known blind spot (guard against it, and say so if it shaped your view): {p['blind_spot']}.\n"
            f"The evidence you demand before you accept a claim: {p['evidence_demand']}.\n")


def counterpart_line(c: dict, m: dict) -> str:
    p = m.get("card") or {}
    rival = next((x for x in c["roster"] if (x.get("card") or {}).get("id") == p.get("counterpart")), None)
    if not rival:
        return ""
    return (f"\nYour counterpart in this council is {rival['id']} «{rival['persona']}»: answer its strongest claim first "
            "(attack it with evidence or concede it).")


def digest_r1(r1: dict) -> dict:
    """Round-1 answers as position, proposal and evidenced claims only (keeps large-council prompts readable)."""
    return {k: {"position": v.get("position"), "proposal": v.get("proposal"),
                "claims": [{"claim": cl.get("claim"), "evidence": cl.get("evidence")} for cl in v.get("claims", [])[:3] if isinstance(cl, dict)]}
            for k, v in sorted(r1.items())}


def digest_r2(r2: dict) -> dict:
    return {k: {"attacks": [{"target": a.get("target"), "counter": a.get("counter")} for a in v.get("attacks", [])[:2] if isinstance(a, dict)],
                "steelman": (v.get("steelman") or {}).get("target")} for k, v in sorted(r2.items())}


def load_personas(path: Path) -> list:
    doc = load(path)
    ps = doc.get("personas")
    if doc.get("schema") != PERSONAS_SCHEMA or not isinstance(ps, list) or not ps:
        raise CouncilError("PERSONAS_INVALID", f"{path.name} is not a {PERSONAS_SCHEMA} roster")
    ids = [p.get("id") for p in ps]
    if len(set(ids)) != len(ids):
        raise CouncilError("PERSONAS_INVALID", f"{path.name} repeats a persona id")
    for p in ps:
        if p.get("lane") not in LANES:
            raise CouncilError("PERSONAS_INVALID", f"{p.get('id')}: unknown lane {p.get('lane')!r}")
    return ps


def persona_scores(personas: list, request: str, primary: str, topics=()) -> dict:
    """Relevance of every persona to a request: trigger words (x3), the primary deliverable's domain (+2), general (+1)."""
    req = _stems(request + " " + " ".join(topics))
    dom = PRIMARY_DOMAIN.get(primary, primary)
    out = {}
    for p in personas:
        hits = sum(1 for t in p.get("triggers", []) if _stems(t) and _stems(t) <= req)
        out[p["id"]] = 3 * hits + (2 if dom in p.get("domains", []) else 0) + (1 if "general" in p.get("domains", []) else 0)
    return out


def select_personas(personas: list, request: str, primary: str, seats: int, topics=()) -> list:
    """Deterministic task-fitted council: the best persona of every lane first, then the most relevant of the rest."""
    sc = persona_scores(personas, request, primary, topics)
    rank = sorted(personas, key=lambda p: (-sc[p["id"]], p["id"]))
    chosen, seen = [], set()
    for lane in LANES:
        best = next((p for p in rank if p["lane"] == lane), None)
        if best:
            chosen.append(best); seen.add(best["id"])
    for p in rank:
        if len(chosen) >= seats:
            break
        if p["id"] not in seen:
            chosen.append(p); seen.add(p["id"])
    order = {lane: i for i, lane in enumerate(LANES)}
    return [dict(p, score=sc[p["id"]]) for p in sorted(chosen[:seats] if seats >= len(LANES) else chosen,
                                                       key=lambda p: (order[p["lane"]], -sc[p["id"]], p["id"]))]


def persona_members(chosen: list) -> list:
    lane_base = {b["lane"]: b for b in BASE}
    out = []
    for i, p in enumerate(chosen, 1):
        b = lane_base[p["lane"]]
        card = {k: p[k] for k in ("id", "name_ar", "name_en", "title_ar", "title_en", "character_ar", "lens_en", "superpowers",
                                  "signature_questions", "blind_spot", "evidence_demand", "counterpart") if k in p}
        out.append({"id": f"M{i}", "persona": f"{p['name_ar']} — {p['title_ar']}", "en": f"{p['name_en']}, {p['title_en']}",
                    "stance": b["stance"], "lane": p["lane"], "evidence": b["evidence"], "specialist": None,
                    "persona_id": p["id"], "card": card})
    return out


def personas_line(c: dict, m: dict) -> str:
    mine = [p for p in c.get("consulted_index") or [] if p.get("member") == m["id"]]
    if not mine:
        return ""
    cards = "; ".join(f"#{p['n']} {p['name_ar']} (sector {p['sector']}): {p.get('role', '')}"
                      + (f" [{p['sensitive']}]" if p.get("sensitive") else "") for p in mine)
    line = ("Personas to consult (an index, not extra members): " + cards + ". They are cards from the user's charter roster: "
            "use them as checklists for your lane; they did not run, review or vote, and they are not evidence.\n")
    if m.get("lane") == "guardrails" and any(p.get("sensitive") for p in mine):
        line += ("Sensitive cards: 'consent' needs the depicted or cloned person's documented consent and disclosure; "
                 "'regulated' (medical, legal, financial, tax, IP) needs a qualified-review disclaimer, never advice.\n")
    return line


def cmd_prompts(a) -> dict:
    d = Path(a.dir)
    c = load(d / "council.json")
    rnd = a.round
    if rnd > 1 and len(c["rounds"][str(rnd - 1)]) < len(c["roster"]):
        raise CouncilError("ROUND_INCOMPLETE", f"round {rnd - 1} has {len(c['rounds'][str(rnd - 1)])}/{len(c['roster'])} members")
    prompts = {m["id"]: member_prompt(c, m, rnd) for m in c["roster"]}
    out = d / f"prompts_r{rnd}.json"
    save(out, prompts)
    return {"round": rnd, "file": str(out), "members": list(prompts)}


def check_member(rnd: int, obj: dict, options: list) -> list:
    need = {1: MEMBER_FIELDS_R1, 2: MEMBER_FIELDS_R2, 3: MEMBER_FIELDS_R3}[rnd]
    probs = [f"missing '{k}'" for k in need if k not in obj]
    if rnd == 1 and isinstance(obj.get("claims"), list):
        for i, cl in enumerate(obj["claims"]):
            if not isinstance(cl, dict) or not str(cl.get("claim", "")).strip() or not str(cl.get("evidence", "")).strip():
                probs.append(f"claims[{i}] needs 'claim' and 'evidence' (or evidence 'opinion')")
    if rnd == 3:
        sc = obj.get("scores")
        if not isinstance(sc, dict):
            probs.append("'scores' must be an object")
        else:
            for o in options:
                v = sc.get(o)
                if not isinstance(v, (int, float)) or not 1 <= v <= 5:
                    probs.append(f"scores.{o} must be a number from 1 to 5")
    return probs


def cmd_ingest(a) -> dict:
    d = Path(a.dir)
    c = load(d / "council.json")
    ids = [m["id"] for m in c["roster"]]
    if a.member not in ids:
        raise CouncilError("UNKNOWN_MEMBER", f"{a.member} is not in the roster ({', '.join(ids)})")
    if a.round > 1 and len(c["rounds"][str(a.round - 1)]) < len(ids):
        raise CouncilError("ROUND_INCOMPLETE", f"round {a.round - 1} is not complete")
    raw = Path(a.file).read_bytes()
    text = raw.decode("utf-8-sig", errors="replace").strip()
    if text.startswith("```"):
        text = text.strip("`").split("\n", 1)[-1]
    start, end = text.find("{"), text.rfind("}")
    try:
        obj = json.loads(text[start:end + 1])
    except ValueError:
        raise CouncilError("BAD_JSON", f"{Path(a.file).name} holds no JSON object") from None
    found = _secrets.scan_object(obj)
    if found:
        raise CouncilError("SECRET", f"likely credentials at {', '.join(p for p, _ in found[:3])}")
    probs = check_member(a.round, obj, c["options"])
    if probs:
        raise CouncilError("MEMBER_INVALID", f"{a.member} round {a.round}: " + "; ".join(probs))
    obj["_receipt"] = {"sha256": sha256_bytes(raw), "simulated": bool(a.simulated), "ingested_at": now_iso()}
    c["rounds"][str(a.round)][a.member] = obj
    save(d / "council.json", c)
    return {"round": a.round, "member": a.member, "have": len(c["rounds"][str(a.round)]), "of": len(ids)}


def cmd_status(a) -> dict:
    c = load(Path(a.dir) / "council.json")
    return {"primary": c["primary"], "options": c["options"],
            "rounds": {r: sorted(v) for r, v in c["rounds"].items()},
            "index_consulted": len(c.get("consulted_index") or [])}


def evidence_ratio(c: dict) -> float:
    claims = [cl for m in c["rounds"]["1"].values() for cl in m.get("claims", []) if isinstance(cl, dict)]
    if not claims:
        return 0.0
    real = [cl for cl in claims if str(cl.get("evidence", "")).strip().lower() not in ("opinion", "رأي", "")]
    return round(len(real) / len(claims), 3)


def cmd_verdict(a) -> dict:
    d = Path(a.dir)
    c = load(d / "council.json")
    ids = [m["id"] for m in c["roster"]]
    missing = [f"r{r}:{m}" for r in ROUNDS for m in ids if m not in c["rounds"][str(r)]]
    if missing and not a.partial:
        raise CouncilError("ROUND_INCOMPLETE", "missing " + ", ".join(missing) + " (or pass --partial)")
    r3 = c["rounds"]["3"]
    totals = {o: 0.0 for o in c["options"]}
    for m in r3.values():
        for o in c["options"]:
            totals[o] += float(m["scores"][o])
    ranked = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    winner = ranked[0][0] if ranked and r3 else None
    margin = round(ranked[0][1] - ranked[1][1], 2) if len(ranked) > 1 and r3 else None
    dissent = [{"member": k, "objection": v["remaining_objection"]} for k, v in sorted(r3.items())
               if str(v.get("remaining_objection", "")).strip().lower() not in ("", "none", "لا يوجد", "لا شيء")]
    attacks = sum(len(v.get("attacks", [])) for v in c["rounds"]["2"].values())
    simulated = any(v.get("_receipt", {}).get("simulated") for r in ROUNDS for v in c["rounds"][str(r)].values())
    warnings = []
    if not dissent:
        warnings.append("NO_DISSENT: every member withdrew every objection; ask the Skeptic for the strongest remaining risk")
    if attacks == 0 and c["rounds"]["2"]:
        warnings.append("NO_CROSS_EXAMINATION: round 2 holds no attacks")
    er = evidence_ratio(c)
    if er < 0.5:
        warnings.append(f"WEAK_EVIDENCE: only {er:.0%} of round-1 claims cite evidence")
    close = max(2.0, round(0.4 * len(ids), 2))  # five members: 2 points, as before; larger councils scale
    if margin is not None and margin <= close:
        warnings.append(f"CLOSE_CALL: {ranked[0][0]} leads {ranked[1][0]} by {margin}")
    status = ("COUNCIL_SIMULATED" if simulated else
              "COUNCIL_PARTIAL" if missing else "COUNCIL_RUN")
    receipt = sha256_bytes(json.dumps(c["rounds"], ensure_ascii=False, sort_keys=True).encode("utf-8"))
    n_index = len(c.get("consulted_index") or [])
    verdict = {"schema": "kosif.council.verdict.v1", "status": status, "winner": winner, "totals": dict(ranked),
               "margin": margin, "dissent": dissent, "attacks": attacks, "evidence_ratio": er,
               "warnings": warnings, "missing": missing, "rounds_sha256": receipt, "decided_at": now_iso(),
               "index_consulted": n_index, "mode": c.get("mode", "classic5"), "seats": len(ids),
               "personas": [m.get("persona_id") for m in c["roster"] if m.get("persona_id")],
               "index_note": f"index consulted: {n_index} personas (cards read by the five members, not experts that ran or voted)"}
    save(d / "verdict.json", verdict)
    lines = [f"# محضر المجلس — {c['request']}", "",
             f"**الحالة:** {status} · **الفائز:** {winner} · **الفارق:** {margin} · **المقاعد:** {len(ids)} · **الإيصال:** `{receipt[:16]}`", "",
             "| العضو | الموقف (جولة 1) | الاقتراح النهائي (جولة 3) | الدرجات |", "|---|---|---|---|"]
    for m in c["roster"]:
        p1 = c["rounds"]["1"].get(m["id"], {}).get("position", "—")
        p3 = r3.get(m["id"], {})
        sc = " · ".join(f"{o}={p3['scores'][o]}" for o in c["options"]) if p3 else "—"
        lines.append(f"| {m['id']} {m['persona']} | {p1} | {p3.get('final_proposal', '—')} | {sc} |")
    lines += ["", f"**الفهرس:** index consulted: {n_index} personas — بطاقات من فهرس الخبراء قرأها الأعضاء الخمسة؛ "
              "لم يُشغَّل أي خبير منها ولم يصوّت (فهرس، لا أعضاء)."]
    lines += ["", "**الرأي المخالف:**"] + ([f"- {x['member']}: {x['objection']}" for x in dissent] or ["- لا يوجد (تحذير NO_DISSENT)"])
    if warnings:
        lines += ["", "**تحذيرات:** " + " · ".join(warnings)]
    (d / "minutes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return verdict


def cmd_personas(a) -> dict:
    pool = load_personas(Path(a.personas_file) if a.personas_file else DEFAULT_PERSONAS)
    if a.id:
        hit = [p for p in pool if p["id"] == a.id.upper()]
        if not hit:
            raise CouncilError("UNKNOWN_PERSONA", a.id)
        return hit[0]
    if a.find:
        primary = primary_of(a.find, None)
        chosen = select_personas(pool, a.find, primary, a.seats, ())
        return {"request": a.find, "primary": primary, "seats": len(chosen),
                "council": [f"{p['id']} {p['name_ar']} — {p['title_ar']} [{p['lane']}] score={p['score']}" for p in chosen]}
    rows = [p for p in pool if not a.lane or p["lane"] == a.lane]
    return {"count": len(rows), "lanes": {l: sum(1 for p in pool if p["lane"] == l) for l in LANES},
            "personas": [f"{p['id']} {p['name_ar']} — {p['title_ar']} ({p['title_en']}) [{p['lane']}]" for p in rows]}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("plan", help="plan a council for a request")
    s.add_argument("request"); s.add_argument("--dir", required=True); s.add_argument("--from-brief")
    s.add_argument("--options", help="comma-separated options to score (default: the brief's plans, else A,B,C)")
    s.add_argument("--force", action="store_true")
    s.add_argument("--roster", help="experts index JSON to consult (default: data/experts_500.json when it exists)")
    s.add_argument("--no-roster", action="store_true", help="do not consult the experts index")
    s.add_argument("--seats", type=int, help=f"a task-fitted council of N ({MIN_SEATS}-{MAX_SEATS}) personas from the 100-persona roster")
    s.add_argument("--personas", help="comma-separated persona ids to seat (5-15), e.g. P001,P021,P041,P061,P081")
    s.add_argument("--full", action="store_true", help="seat all personas of the roster (only when the user asks for the whole council)")
    s.add_argument("--personas-file", help="persona roster JSON (default: data/council_100.json)")
    s = sub.add_parser("personas", help="list, search or show the 100 council personas")
    s.add_argument("--find", help="a request: show the task-fitted council it would seat")
    s.add_argument("--seats", type=int, default=7); s.add_argument("--lane", choices=LANES); s.add_argument("--id")
    s.add_argument("--personas-file")
    s = sub.add_parser("prompts", help="write the prompts for one round")
    s.add_argument("--dir", required=True); s.add_argument("--round", type=int, choices=ROUNDS, required=True)
    s = sub.add_parser("ingest", help="record one member's answer for one round")
    s.add_argument("--dir", required=True); s.add_argument("--round", type=int, choices=ROUNDS, required=True)
    s.add_argument("--member", required=True); s.add_argument("--file", required=True)
    s.add_argument("--simulated", action="store_true", help="the answer was written in Claude's own context, not by a separate agent")
    s = sub.add_parser("status", help="show which members answered which rounds")
    s.add_argument("--dir", required=True)
    s = sub.add_parser("verdict", help="score round 3, record dissent and write verdict.json + minutes.md")
    s.add_argument("--dir", required=True); s.add_argument("--partial", action="store_true")
    a = p.parse_args(argv)
    try:
        res = {"plan": cmd_plan, "prompts": cmd_prompts, "ingest": cmd_ingest, "status": cmd_status, "verdict": cmd_verdict,
               "personas": cmd_personas}[a.cmd](a)
    except _secrets.SecretError as exc:
        print(f"council: error: SECRET: {exc}", file=sys.stderr)
        return 2
    except CouncilError as exc:
        print(f"council: error: {exc.code}: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"council: error: IO: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
