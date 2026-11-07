#!/usr/bin/env python3
"""Dragon Montage — «التنين الأسود، مونتاج».

One command that runs the eight stations of the Black Dragon montage protocol:

  1 analyze  العين الأولى      footage → analysis.json
  2 brief    يفهم المطلوب      task → brief.json
  3 concepts يفكر بإبداع       3 different concepts + decision → concepts.json
  4 taste    يختار الذوق       style/grade/transitions/camera/captions → look.json
  5 direct   يكتب المونتاج     real edit decisions → edl.json
  5b preview يوريك الشكل        storyboard + movement matrix (preview/PLAN_AR.md) → the owner approves
  6 render   ينفّذ             final.mp4 + captions + editable project
  7 review   يتفرج وينقد       checks + frames + fixes → review.json
  8 fix      يصلّح ويسلّم       apply fixes, re-render (max 3 rounds), report.md

Optional: generate (proposals only, consent required) and mimic (copy a
reference video's rhythm). Nothing here spends credits, uploads or publishes.

Usage (the protocol: plan, show the owner, then go):
  dragon_montage.py plan "<task>" --clip a.mp4 … [--animatic]   stops before the render
  dragon_montage.py go --job DIR [--preview] [--rounds 3]        after the owner says yes
  dragon_montage.py edit "<task>" --clip a.mp4 [--clip b.mp4] [--music m.mp3]
        [--job out/dragon-montage/<id>] [--platform reel] [--seconds 45]
        [--style ID] [--invent] [--reference ref.mp4] [--rounds 3] [--preview]
  dragon_montage.py doctor [--json]
  dragon_montage.py station <name> --job DIR [extra args…]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dm_common as C  # noqa: E402

STATIONS = {
    "doctor": ("dm_doctor.py", []),
    "analyze": ("dm_analyze.py", []),
    "brief": ("dm_think.py", ["brief"]),
    "concepts": ("dm_think.py", ["concepts"]),
    "taste": ("dm_taste.py", ["pick"]),
    "direct": ("dm_direct.py", ["direct"]),
    "render": ("dm_render.py", ["render"]),
    "review": ("dm_review.py", ["review"]),
    "generate": ("dm_generate.py", ["gaps"]),
    "mimic": ("dm_mimic.py", ["mimic"]),
    "stock-search": ("dm_stock.py", ["search"]),
    "stock-fetch": ("dm_stock.py", ["fetch"]),
    "storyboard": ("dm_storyboard.py", ["storyboard"]),
}

ARABIC = {
    "analyze": "العين الأولى", "brief": "يفهم المطلوب", "concepts": "يفكر بإبداع",
    "taste": "يختار الذوق", "direct": "يكتب المونتاج", "render": "ينفّذ",
    "review": "يتفرج وينقد", "generate": "اقتراحات التوليد", "mimic": "المحاكاة",
    "stock-search": "يدوّر في المواقع المفتوحة", "stock-fetch": "ينزّل اللقطات بترخيصها",
    "storyboard": "يوريك الشكل قبل ما ينفّذ",
}


def station(name: str, args: list[str], *, log: list[dict]) -> subprocess.CompletedProcess:
    script, sub = STATIONS[name]
    argv = [sys.executable, str(HERE / script), *sub, *args]
    t0 = time.time()
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    res = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    log.append({"station": name, "rc": res.returncode, "seconds": round(time.time() - t0, 2),
                "stderr_tail": res.stderr[-500:] if res.returncode else ""})
    sys.stderr.write(f"[{name}] {ARABIC.get(name, name)}: {'✓' if res.returncode == 0 else '✗'}\n")
    if res.returncode != 0:
        raise SystemExit(f"station {name} failed:\n{res.stderr[-2000:]}\n{res.stdout[-1000:]}")
    return res


SNAP = (("render/final.mp4", "render/round{n}.mp4"), ("edl.json", "edl.round{n}.json"),
        ("review.json", "review.round{n}.json"), ("render.json", "render.round{n}.json"))


def snapshot(job: Path, n: int) -> None:
    import shutil
    for src, dst in SNAP:
        if (job / src).exists():
            shutil.copy2(job / src, job / dst.format(n=n))


def restore(job: Path, n: int) -> None:
    import shutil
    for src, dst in SNAP:
        if (job / dst.format(n=n)).exists():
            shutil.copy2(job / dst.format(n=n), job / src)


def job_status(job: Path, log: list[dict], extra: dict) -> None:
    data = C.new("job", **extra, stations=log)
    (job / "job.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def prepare(a) -> tuple[Path, list[dict], dict]:
    """Stations 1-5 plus the preview: everything up to (not including) the render."""
    job = C.job_dir(a.job or f"out/dragon-montage/{time.strftime('%Y%m%d-%H%M%S')}")
    log: list[dict] = []
    meta = {"task": a.task, "clips": [str(Path(c).resolve()) for c in (a.clip or [])],
            "music": str(Path(a.music).resolve()) if a.music else None,
            "options": {k: getattr(a, k, None) for k in ("platform", "seconds", "style", "invent", "rounds", "preview")}}
    job_status(job, log, meta)
    J = ["--job", str(job)]

    clips = list(a.clip or [])
    if a.stock:                               # only when the owner asks: open-licence sites (Pexels, Mixkit, …)
        sq = [*J, "--query", a.stock] + (["--commercial"] if a.stock_commercial else [])
        if a.platform in ("reel", "story"):
            sq += ["--orientation", "portrait"]
        elif a.platform in ("youtube", "landscape"):
            sq += ["--orientation", "landscape"]
        station("stock-search", sq, log=log)
        res = station("stock-fetch", [*J, "--top", str(a.stock_top)], log=log)
        try:
            clips += json.loads(res.stdout.strip().splitlines()[-1]).get("downloaded", [])
        except (ValueError, IndexError):
            pass
        meta["stock_clips"] = clips[len(a.clip or []):]
        job_status(job, log, meta)
    if not clips:
        raise SystemExit("no footage: pass --clip and/or --stock \"<query>\"")

    an = [*J]
    for c in clips:
        an += ["--clip", c]
    if a.music:
        an += ["--music", a.music]
    if a.no_transcribe:
        an += ["--no-transcribe"]
    station("analyze", an, log=log)

    br = [*J, "--task", a.task]
    if a.platform:
        br += ["--platform", a.platform]
    if a.seconds:
        br += ["--seconds", str(a.seconds)]
    station("brief", br, log=log)
    station("concepts", J, log=log)

    for stale in ("look_override.json", "reference_rhythm.json"):
        if not a.reference and (job / stale).exists():
            (job / stale).unlink()            # left over from an earlier --reference run
    if a.reference:
        station("mimic", [*J, "--reference", a.reference], log=log)
    tp = [*J]
    if a.style:
        tp += ["--style", a.style]
    if a.invent:
        tp += ["--invent"]
    station("taste", tp, log=log)
    station("direct", J, log=log)
    station("generate", J, log=log)          # proposals only; nothing is spent
    station("storyboard", J + (["--animatic"] if getattr(a, "animatic", False) else []), log=log)
    return job, log, meta


def cmd_plan(a) -> int:
    """Stop before the render: the owner sees preview/PLAN_AR.md + storyboard.jpg and says yes or asks for changes."""
    job, log, meta = prepare(a)
    meta["status"] = "awaiting_owner_approval"
    job_status(job, log, meta)
    pv = job / "preview"
    print(json.dumps({"job": str(job), "status": "awaiting_owner_approval", "plan": str(pv / "PLAN_AR.md"),
                      "storyboard": str(pv / "storyboard.jpg") if (pv / "storyboard.jpg").exists() else None,
                      "animatic": str(pv / "animatic.mp4") if (pv / "animatic.mp4").exists() else None,
                      "next": f"dragon_montage.py go --job {job}"}, ensure_ascii=False))
    return 0


def cmd_go(a) -> int:
    """The owner approved the preview: render, review and fix the EDL that is in the job now."""
    job = C.job_dir(a.job)
    if not (job / "edl.json").exists():
        raise SystemExit(f"no edl.json in {job}: run `dragon_montage.py plan …` first")
    old = json.loads((job / "job.json").read_text(encoding="utf-8")) if (job / "job.json").exists() else {}
    log = list(old.get("stations") or [])
    meta = {k: v for k, v in old.items() if k not in ("schema", "stations")}
    opts = meta.get("options") or {}
    preview = a.preview if a.preview is not None else bool(opts.get("preview"))
    rounds = a.rounds or opts.get("rounds") or 3
    station("storyboard", ["--job", str(job)], log=log)   # the plan file matches the EDL that gets rendered
    meta["status"] = "approved"
    meta["approved_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    return finish(job, log, meta, preview=preview, rounds=rounds)


def cmd_edit(a) -> int:
    job, log, meta = prepare(a)
    return finish(job, log, meta, preview=a.preview, rounds=a.rounds)


def finish(job: Path, log: list[dict], meta: dict, *, preview: bool, rounds: int) -> int:
    J = ["--job", str(job)]
    rr = [*J] + (["--preview"] if preview else [])
    rounds = max(1, min(3, int(rounds)))
    review = None
    scores: dict[int, float] = {}
    for n in range(1, rounds + 1):
        station("render", rr, log=log)
        station("review", [*J, "--round", str(n)], log=log)
        review = C.read(job, "review")
        snapshot(job, n)
        scores[n] = float(review.get("score") or 0.0)
        if review["verdict"] == "ship" or not review["fixes"] or n == rounds:
            break
        station("direct", [*J, "--apply-review"], log=log)
    best = max(scores, key=lambda k: (scores[k], k))
    if best != max(scores):
        restore(job, best)                    # a fix round made it worse: keep the better cut
        review = C.read(job, "review")
    meta["rounds"] = {"scores": scores, "kept": best}

    job_status(job, log, meta)
    write_report(job, log, review)
    print(json.dumps({"job": str(job), "final": str(job / C.read(job, "render")["final"]),
                      "verdict": review["verdict"] if review else None,
                      "report": str(job / "report.md")}, ensure_ascii=False))
    return 0


def write_report(job: Path, log: list[dict], review: dict | None) -> None:
    rec = C.receipts(job)
    ran = sorted({r["tool"] for r in rec if r.get("owner_media") and r["rc"] == 0})
    analysis = C.read(job, "analysis")
    brief = C.read(job, "brief")
    concepts = C.read(job, "concepts")
    look = C.read(job, "look")
    edl = C.read(job, "edl")
    render = C.read(job, "render")
    chosen = next((c for c in concepts["concepts"] if c["id"] == concepts["decision"].get("chosen")), {})
    consulted = sum(len(c.get("frameworks", [])) for c in concepts["concepts"]) + len(brief.get("frameworks", []))
    lines = [
        "# تقرير مونتاج التنين الأسود", "",
        f"**المهمة:** {brief['task']}", "",
        f"**الفيديو النهائي:** `{render['final']}` · المدة {edl['duration']:.1f} ثانية · {edl['width']}×{edl['height']}", "",
        f"**الفكرة المختارة:** {chosen.get('title', '—')} — {chosen.get('logline', '')}",
        f"**الهوك المقترح في الفكرة:** {chosen.get('hook', {}).get('text', '—')}",
        f"**أول لقطة فعلاً في المونتاج:** {edl['events'][0]['reason'] if edl['events'] else '—'}",
        f"**ليه الفكرة دي:** {concepts['decision'].get('why', '')}", "",
        f"**اللوك:** {look['style_id']} · لون {look['grade'].get('id')} · كابشن {look['captions'].get('style')}",
        f"**ليه:** {look.get('why', '')}", "",
        "## الأرقام بأمانة",
        f"- أطر تفكير اتقرت واتطبقت على الفكرة: {consulted}",
        f"- أدوات اشتغلت على فيديوك إنت: {len(ran)} ({', '.join(ran)})",
        f"- أدوات ناقصة: {', '.join(analysis.get('missing', [])) or 'مفيش'}",
        f"- قطعات في المونتاج: {len(edl['events'])}",
        f"- فحص الجودة التقني: {'عدّى' if render['verify'].get('pass') else 'ما عدّاش'}",
        f"- لفات النقد والتصليح: {review['round'] if review else 0} · الحكم: {review['verdict'] if review else '—'} · الدرجة: {review.get('score', '—') if review else '—'}", "",
        "## كل قطعة وسببها",
    ]
    for ev in edl["events"]:
        lines.append(f"- `{ev['id']}` {ev['clip']} {ev['src_in']:.2f}→{ev['src_out']:.2f}: {ev['reason']}")
    if review:
        failed = [c for c in review["checks"] if not c.get("pass")]
        if failed:
            lines += ["", "## ملاحظات لسه مفتوحة"] + [f"- {c['id']}: {c.get('evidence', '')}" for c in failed]
    gen = job / "generate.json"
    if gen.exists():
        props = json.loads(gen.read_text(encoding="utf-8")).get("proposals", [])
        if props:
            lines += ["", "## اقتراحات توليد (محتاجة موافقتك قبل أي صرف)"]
            lines += [f"- {p['id']}: {p['kind']} لـ {p.get('role', '')} ({p.get('seconds', '?')} ث)" for p in props]
    stock = job / "stock.json"
    if stock.exists():
        got = json.loads(stock.read_text(encoding="utf-8")).get("downloaded", [])
        if got:
            lines += ["", "## لقطات من مواقع مفتوحة المصدر (بترخيصها)"]
            lines += [f"- {g.get('attribution') or g['path']}" for g in got]
            lines += ["- ملف النسب الكامل: `stock/ATTRIBUTION.md`"]
    lines += ["", "## المراحل", *[f"- {ARABIC.get(s['station'], s['station'])}: {'✓' if s['rc'] == 0 else '✗'} ({s['seconds']} ث)" for s in log]]
    (job / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("edit", help="all stations in one go, no approval stop (tests, or when the owner says «نفّذ مباشرة»)")
    pl = sub.add_parser("plan", help="stations 1-5 + preview (storyboard, movement matrix); stops for the owner's yes")
    g = sub.add_parser("go", help="the owner approved the preview: render, review, fix")
    g.add_argument("--job", required=True)
    g.add_argument("--rounds", type=int)
    g.add_argument("--preview", action="store_true", default=None)
    pl.add_argument("--animatic", action="store_true", help="also a fast low-res draft video of the plan")
    for e in (e, pl):
        _edit_args(e)
    sub.add_parser("doctor", help="which tools are installed / missing (passes extra flags to dm_doctor)")
    s = sub.add_parser("station", help="run one station")
    s.add_argument("name", choices=sorted(STATIONS))
    a, rest = p.parse_known_args(argv)
    if a.cmd in ("edit", "plan", "go") and rest:
        p.error(f"unrecognized arguments: {' '.join(rest)}")
    a.rest = rest
    if a.cmd == "edit":
        return cmd_edit(a)
    if a.cmd == "plan":
        return cmd_plan(a)
    if a.cmd == "go":
        return cmd_go(a)
    if a.cmd == "doctor":
        script, sub_ = STATIONS["doctor"]
        return subprocess.call([sys.executable, str(HERE / script), "doctor", *a.rest])
    script, sub_ = STATIONS[a.name]
    return subprocess.call([sys.executable, str(HERE / script), *sub_, *a.rest])


def _edit_args(e) -> None:
    e.add_argument("task")
    e.add_argument("--clip", action="append")
    e.add_argument("--stock", help="search open-licence sites for this (English) query and add the best clips")
    e.add_argument("--stock-top", type=int, default=3)
    e.add_argument("--stock-commercial", action="store_true", help="keep only licences that allow commercial use")
    e.add_argument("--music")
    e.add_argument("--job")
    e.add_argument("--platform")
    e.add_argument("--seconds", type=float)
    e.add_argument("--style")
    e.add_argument("--invent", action="store_true")
    e.add_argument("--reference")
    e.add_argument("--rounds", type=int, default=3)
    e.add_argument("--preview", action="store_true")
    e.add_argument("--no-transcribe", action="store_true")


if __name__ == "__main__":
    raise SystemExit(main())
