#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""arena_gate: الحلبة شرط أساسي في شغل التنين الأسود (ported from Red Dragon v2.19.0).

The mechanism comes from Jakeschincariol/arena-skill (MIT, vendored next to this file):
N sub-agents get the exact same task, each with a different strategy card (reasoning mode + workflow + strategy),
write their solution blind, then a single-elimination bracket: two attacks per match, two defences/revisions,
one judge on a written rubric, until one solution survives. Optional blind final against a rejected answer.

What this file adds (our code): the arena is now a required step, sized to the task so it never burns 100 agents
on a small job, with the cheap Haiku worker (.claude/agents/arena-fighter.md) on the first round only and the judges always
on the main model. Delivery is blocked (`gate`) until the arena has a champion or a written reason to skip it.

    python3 .claude/skills/arena/arena_gate.py size "<task>" [--depth L1|L2|L3] [--unhappy] [--agents N] [--json]
    python3 .claude/skills/arena/arena_gate.py start "<task>" --task-file .arena/task.md [--baseline-file B] [--agents N] [--unhappy] [--seed S]
    python3 .claude/skills/arena/arena_gate.py jobs spawn|attack|defend|judge|final      (bracket prompts + which agent and model runs each job)
    python3 .claude/skills/arena/arena_gate.py next | status | collect | advance | winner   (straight to the bracket)
    python3 .claude/skills/arena/arena_gate.py skip --reason "<why this task has no arena>"
    python3 .claude/skills/arena/arena_gate.py gate                                        (exit 0 only with a champion or a recorded skip)
    python3 .claude/skills/arena/arena_gate.py selftest
"""
import argparse, datetime, json, math, os, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRACKET = HERE / "bracket.py"
ROOT = ".arena"

# tier -> competitors. 100 only when the owner names it ("100", "الحلبة الكاملة", --agents 100).
TIERS = {"skip": 0, "duel": 4, "quick": 8, "standard": 16, "full": 100}
TIER_AR = {"skip": "من غير حلبة", "duel": "نزال صغير", "quick": "حلبة سريعة", "standard": "حلبة كاملة الجولات", "full": "حلبة الـ 100"}

CHAT = re.compile(r"^\s*(شكرا|تمام|اوك|ok|ماشي|السلام|سلام|ازيك|hi|hello|thanks)\b", re.I)
FACT = re.compile(r"^\s*(فين|اسمه ايه|اسمه إيه|مدته كام|كام|امتى|إمتى|هل|ايه هو|إيه هو|what is|where|when)\b", re.I)
ROUTINE = re.compile(r"(حمّل|حمل|نزّل|نزل|تحميل|download|yt-dlp|ffprobe|حوّل|convert|انسخ|انقل|سمّي|rename|zip|اضغط|sha256|checksum|selftest|جرد|ارفع|push|commit)", re.I)
TASTE = re.compile(r"(صمم|تصميم|ارسم|اكتب|كتابة|ابتكر|اختار|قرار|خطة|خطط|نقد|رأي|ستوري ?بورد|كونسبت|اتجاه|هوك|مونتاج|موشن|سكريبت|اسكريبت|كابشن|عنوان|فكرة|افكار|أفكار|استراتيجي|معماري|(?<!\S)حلّ?(?!\S)|طوّر|طور|اعمل|ابني|reel|ريل|design|write|plan|hook|script|idea)", re.I)
BIG = re.compile(r"(مشروع|كامل|كاملة|فيلم|تطبيق|موقع|سيستم|نظام|معمارية|استراتيجية|حملة|سلسلة|برنامج|app|architecture|strategy|campaign|series)", re.I)
UNHAPPY = re.compile(r"(وحش|وحشة|مش عاجب|مش حلو|غلط|تاني|أحسن من كده|احسن من كده|ماعجبنيش|معجبنيش|bad answer|try again|do better|خليهم يتنافسوا|يتخانقوا|يتعاركوا|الحلبة|حلبة|arena)", re.I)
TASTE_VERB = re.compile(r"(صمم|ارسم|اكتب|ابتكر|اختار|خطط|طوّر|طور|اعمل|ابني|design|write|plan)", re.I)
FULL = re.compile(r"(\b100\b|١٠٠|الحلبة الكاملة|full arena|مية وكيل|100 وكيل)", re.I)


def bracket_sizes(n):
    s = [n]
    while s[-1] > 1:
        s.append((s[-1] + 1) // 2)
    return s


def model_plan(n):
    """Calls per model. Round 1 attack/defend + every spawn on Haiku (arena-fighter); later rounds on Sonnet;
    every judge and the final on the main model, never Haiku: the judge decides, and deciding is not a cheap job."""
    sizes = bracket_sizes(n)
    rows, haiku, sonnet, main = [], n, 0, 0
    for r, alive in enumerate(sizes[:-1], 1):
        m = alive // 2
        ad = 4 * m
        if r == 1:
            haiku += ad
        else:
            sonnet += ad
        main += m
        rows.append({"round": r, "alive": alive, "matches": m, "bye": alive % 2 == 1,
                     "attack_defend": "haiku" if r == 1 else "sonnet", "judge": "main"})
    return {"agents": n, "rounds": len(sizes) - 1, "calls": haiku + sonnet + main, "haiku": haiku, "sonnet": sonnet, "main": main,
            "alive": sizes, "rows": rows}


def size(text, depth=None, unhappy=None, agents=None):
    t = (text or "").strip()
    unhappy = bool(UNHAPPY.search(t)) if unhappy is None else unhappy
    if agents:
        tier = next((k for k, v in TIERS.items() if v == agents), "custom")
        return _out(tier, agents, "العدد اتحدد بالاسم", unhappy)
    if FULL.search(t):
        return _out("full", 100, "صاحب الشغل طلب الـ 100 بالاسم", unhappy)
    if not t or CHAT.search(t):
        return _out("skip", 0, "دردشة أو تأكيد: مفيش مهمة تتنافس عليها", unhappy)
    taste, routine = bool(TASTE.search(t)), bool(ROUTINE.search(t))
    if routine and not taste and not unhappy:
        return _out("skip", 0, "خطوة روتينية ليها إجابة واحدة بتتقاس (تحميل، تحويل، نسخ، فحص): الحلبة مالهاش لازمة", unhappy)
    if FACT.search(t) and not TASTE_VERB.search(t) and not unhappy:
        return _out("skip", 0, "سؤال معلومة ليه إجابة واحدة: دوّر وجاوب", unhappy)
    if not taste and not BIG.search(t) and not unhappy:
        return _out("skip", 0, "تعديل محدد ليه إجابة واحدة (مفيش ذوق ولا قرار مفتوح): نفّذ واتأكد", unhappy)
    score = {"L1": 1, "L2": 2, "L3": 3}.get(depth or "", 1 + (len(t) > 160) + (len(t) > 400))
    score += 1 if taste else 0
    score += min(2, len({m.group(0) for m in BIG.finditer(t)}))
    if unhappy:
        score = max(score, 4)
    tier = "duel" if score <= 2 else "quick" if score == 3 else "standard"
    why = {"duel": "مهمة صغيرة فيها ذوق أو قرار: 4 نسخ تكفي تكشف البديل الأحسن",
           "quick": "مهمة متوسطة فيها أكتر من طريقة صح",
           "standard": "مهمة كبيرة أو الإجابة اترفضت: 16 نسخة زي الـ --quick الأصلي"}[tier]
    return _out(tier, TIERS[tier], why, unhappy)


def _out(tier, n, why, unhappy):
    r = {"tier": tier, "tier_ar": TIER_AR.get(tier, f"{n} وكيل"), "agents": n, "why": why, "unhappy": unhappy}
    if n:
        r["plan"] = model_plan(n)
        r["ask_first"] = n >= 100      # the 100 always needs an explicit yes (cost)
    return r


def render_size(r):
    if not r["agents"]:
        return f"⚔️ الحلبة: {r['tier_ar']}: {r['why']}.\n   سجّل السبب قبل التسليم: python3 .claude/skills/arena/arena_gate.py skip --reason \"{r['why']}\""
    p = r["plan"]
    L = [f"⚔️ الحلبة: {r['tier_ar']}: {r['agents']} وكيل، {p['rounds']} جولات، {p['calls']} نداء ({r['why']}).",
         f"   الموديلات: Haiku (arena-fighter) {p['haiku']} نداء للحلول والجولة الأولى · Sonnet {p['sonnet']} للجولات اللي بعدها · الموديل الأساسي {p['main']} للحكام.",
         f"   الباقي بعد كل جولة: {' ← '.join(map(str, p['alive']))}"]
    if r.get("ask_first"):
        L.append("   ⚠️ 100 وكيل تكلفتها عالية: اعرض الرقم واستنى «موافق» قبل ما تبدأ.")
    if r["unhappy"]:
        L.append("   الإجابة اللي اترفضت تتكتب حرفيًا في .arena/baseline.md وتدخل النهائي الأعمى.")
    return "\n".join(L)


# ---------------------------------------------------------------- bracket passthrough
def bracket(args, capture=False):
    if not BRACKET.is_file():
        raise SystemExit(f"الحلبة مش موجودة: {BRACKET}")
    cmd = [sys.executable, "-X", "utf8", str(BRACKET)] + list(args)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    if capture:
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    return subprocess.call(cmd, env=env)


def latest_dir():
    p = Path(ROOT) / "LATEST"
    return Path(p.read_text(encoding="utf-8").strip()) if p.is_file() else None


def state():
    d = latest_dir()
    f = d / "arena.json" if d else None
    return json.loads(f.read_text(encoding="utf-8")) if f and f.is_file() else None


def start(text, task_file, baseline=None, agents=None, unhappy=None, seed=None, depth=None):
    r = size(text, depth=depth, unhappy=unhappy, agents=agents)
    if not r["agents"]:
        print(render_size(r))
        return 2
    if r.get("ask_first") and not agents:
        print(render_size(r))
        print("   ابدأها بـ --agents 100 بعد موافقة صاحب الشغل.")
        return 3
    args = ["init", "--agents", str(r["agents"]), "--task-file", task_file]
    if baseline:
        args += ["--baseline-file", baseline]
    if seed is not None:
        args += ["--seed", str(seed)]
    code = bracket(args)
    if code == 0 and latest_dir():
        (latest_dir() / "rd_models.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        print(render_size(r))
        print("   الخطوة الجاية: python3 .claude/skills/arena/arena_gate.py next")
    return code


def agent_for(phase, rnd):
    if phase == "spawn" or (phase in ("attack", "defend") and rnd == 1):
        return {"subagent_type": "arena-fighter", "model": "haiku"}
    if phase in ("attack", "defend"):
        return {"subagent_type": "general-purpose", "model": "sonnet"}
    return {"subagent_type": "general-purpose", "model": None}      # judge / final: main model


def jobs(phase):
    r = bracket(["prompts", phase], capture=True)
    sys.stdout.write(r.stdout)
    if r.returncode:
        sys.stderr.write(r.stderr)
        return r.returncode
    st = state() or {}
    rnd = len(st.get("rounds", [])) if phase != "spawn" else 0
    a = agent_for(phase, rnd)
    m = f", model: \"{a['model']}\"" if a["model"] else " (من غير model: الموديل الأساسي)"
    print("")
    print(f"⚔️ التنين: كل job في المرحلة دي = Agent(subagent_type: \"{a['subagent_type']}\"{m}).")
    if a["subagent_type"] == "arena-fighter":
        print("   لو arena-fighter مش متثبت: انسخ .claude/agents/arena-fighter.md لـ ~/.claude/agents، أو general-purpose بـ model \"haiku\".")
    print("   الحكام دايمًا على الموديل الأساسي. المنسّق (إنت) مابيحكمش ومابيقراش الحلول لحد winner.")
    return 0


def skip(reason):
    Path(ROOT).mkdir(exist_ok=True)
    row = {"t": datetime.datetime.now().isoformat(timespec="seconds"), "reason": reason}
    (Path(ROOT) / "SKIP.json").write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"⚔️ اتسجّل: الشغل ده من غير حلبة: {reason}")
    return 0


def gate():
    st = state()
    sk = Path(ROOT) / "SKIP.json"
    if st and st.get("champion"):
        fin = st.get("final")
        if fin and not fin.get("result"):
            print("❌ الحلبة ليها بطل، بس النهائي الأعمى قدام الإجابة المرفوضة لسه ماتعملش: python3 .claude/skills/arena/arena_gate.py next")
            return 1
        print(f"✅ الحلبة خلصت: البطل {st['champion']} بعد {len(st.get('rounds', []))} جولات. python3 .claude/skills/arena/arena_gate.py winner")
        return 0
    if st:
        print("❌ الحلبة شغالة ولسه مفيش بطل: python3 .claude/skills/arena/arena_gate.py next. ممنوع التسليم قبلها.")
        return 1
    if sk.is_file():
        row = json.loads(sk.read_text(encoding="utf-8"))
        print(f"✅ من غير حلبة، والسبب مكتوب: {row['reason']}")
        return 0
    print("❌ مفيش حلبة ولا سبب مكتوب لتخطيها. شغّل python3 .claude/skills/arena/arena_gate.py size \"<المهمة>\" وبعدها start أو skip.")
    return 1


# ---------------------------------------------------------------- selftest
CASES = [
    ("شكرا", "skip"), ("حمّل الفيديو ده وحوّله mp3", "skip"), ("فين ملف الريل بتاع امبارح", "skip"),
    ("عدّل لون الخلفية للأحمر", "skip"), ("اكتب هوك لريل عن الإصرار", "duel"), ("اعمل مونتاج ريل 30 ثانية لميار", "duel"),
    ("ابني تطبيق كامل لإدارة المخزن", "standard"),
    ("صمم لي اتجاه بصري لحملة كاملة على إنستجرام لمدة شهر", "standard"),
    ("الإجابة وحشة، هاتلي أحسن من كده", "standard"),
    ("خليهم يتعاركوا 100 وكيل على السكريبت", "full"),
]


def selftest():
    bad = []
    for q, want in CASES:
        got = size(q)["tier"]
        if got != want:
            bad.append(f"«{q}»: {got} ≠ {want}")
    p = model_plan(16)
    if (p["rounds"], p["calls"]) != (4, 91):
        bad.append(f"16 وكيل: {p['rounds']} جولات/{p['calls']} نداء ≠ 4/91 (أرقام arena-skill الأصلية)")
    if model_plan(100)["calls"] != 595:
        bad.append("100 وكيل ≠ 595 نداء")
    if p["haiku"] != 16 + 32 or p["main"] != 15:
        bad.append(f"توزيع الموديلات غلط: {p}")
    if agent_for("judge", 1)["model"] is not None or agent_for("spawn", 0)["model"] != "haiku" or agent_for("attack", 2)["model"] != "sonnet":
        bad.append("agent_for: الحكام لازم على الموديل الأساسي")
    # a real 4-agent bracket: init, gate refuses, skip/gate
    if BRACKET.is_file():
        cwd = os.getcwd()
        d = tempfile.mkdtemp()
        try:
            os.chdir(d)
            Path(ROOT).mkdir()
            (Path(ROOT) / "task.md").write_text("اكتب هوك لريل عن الإصرار.", encoding="utf-8")
            if gate() == 0:
                bad.append("gate عدّى من غير حلبة ولا سبب")
            r = bracket(["init", "--agents", "4", "--seed", "7", "--task-file", ".arena/task.md"], capture=True)
            if r.returncode or not state():
                bad.append("bracket init فشل: " + (r.stderr or r.stdout)[-200:])
            elif gate() == 0:
                bad.append("gate عدّى والحلبة لسه مفيهاش بطل")
            st = state() or {}
            if len(st.get("agents", {})) != 4:
                bad.append("init ماطلّعش 4 مقاتلين")
        finally:
            os.chdir(cwd)
        d2 = tempfile.mkdtemp()
        try:
            os.chdir(d2)
            skip("اختبار")
            if gate() != 0:
                bad.append("gate رفض رغم إن السبب مكتوب")
        finally:
            os.chdir(cwd)
    for b in bad:
        print("FAIL", b)
    print(f"arena-gate selftest: {'ok' if not bad else str(len(bad)) + ' problem(s)'} ({len(CASES)} sizing cases + bracket)")
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog="arena", description="الحلبة شرط أساسي: Red Dragon arena gate")
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("size"); s.add_argument("text"); s.add_argument("--depth"); s.add_argument("--unhappy", action="store_true", default=None)
    s.add_argument("--agents", type=int); s.add_argument("--json", action="store_true")
    s = sp.add_parser("start"); s.add_argument("text"); s.add_argument("--task-file", required=True); s.add_argument("--baseline-file")
    s.add_argument("--agents", type=int); s.add_argument("--unhappy", action="store_true", default=None); s.add_argument("--seed", type=int); s.add_argument("--depth")
    s = sp.add_parser("jobs"); s.add_argument("phase", choices=["spawn", "attack", "defend", "judge", "final"])
    s = sp.add_parser("skip"); s.add_argument("--reason", required=True)
    sp.add_parser("gate"); sp.add_parser("selftest")
    for n in ("next", "status", "collect", "advance", "winner", "pairings", "plan", "check", "record", "card"):
        s = sp.add_parser(n); s.add_argument("rest", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)
    if a.cmd == "size":
        r = size(a.text, depth=a.depth, unhappy=a.unhappy, agents=a.agents)
        print(json.dumps(r, ensure_ascii=False, indent=1) if a.json else render_size(r))
        return 0
    if a.cmd == "start":
        return start(a.text, a.task_file, a.baseline_file, a.agents, a.unhappy, a.seed, a.depth)
    if a.cmd == "jobs":
        return jobs(a.phase)
    if a.cmd == "skip":
        return skip(a.reason)
    if a.cmd == "gate":
        return gate()
    if a.cmd == "selftest":
        return selftest()
    return bracket([a.cmd] + a.rest)


if __name__ == "__main__":
    sys.exit(main())
