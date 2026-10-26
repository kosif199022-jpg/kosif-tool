"""KOSIF workbench — a 2D motion film with no browser: the Workbench contract (plan → validate → manifest) drawn frame
by frame with Pillow and encoded by FFmpeg, then verified with ffprobe. Works in a cloud sandbox (claude.ai) as well as
on a PC.

    python workbench_cli.py "مقدمة عن قوة الأفكار" --seconds 12 --aspect 9:16 --out film.mp4
    python workbench_cli.py "…" --titles "فكرة|تتضح|زاوية|الأثر|التالي" --subtitle "سطر ثانٍ" --accents "#E7B65A,#5BD1A5" --out film.mp4
    python workbench_cli.py --manifest my_manifest.json --out film.mp4          # a hand-edited kosif.motion.manifest.v1
    python workbench_cli.py "…" --plan-only --out plan_dir                         # write plan.json + manifest.json only

Silent 2D (titles, subtitles, accents, the five-beat timing). For sound, mux a score afterwards (kmotion score) or use
`kmotion timeline`; for richer motion use a composition (needs a browser) or KOSIF Studio Cloud.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / "web"))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

import wbcompat  # noqa: E402


def make_manifest(task: str, seconds: float, fps: int, aspect: str, titles: list[str] | None, subtitle: str | None,
                  accents: list[str] | None) -> tuple[dict, dict]:
    plan = wbcompat.make_plan({"task": task, "seconds": seconds, "fps": fps, "aspect": aspect})
    v = wbcompat.validate_plan(plan)
    if not v["valid"]:
        raise SystemExit("plan invalid: " + " ".join(v["errors"]))
    plan["intent"] = "2d_motion"                                  # this command always draws the 2D composition
    m = wbcompat.compile_plan(plan)["manifest"]
    for i, sc in enumerate(m["scenes"]):
        if titles and i < len(titles) and titles[i].strip():
            sc["title"] = titles[i].strip()[:120]
        if subtitle is not None:
            sc["subtitle"] = subtitle[:300]
        if accents:
            sc["accent"] = accents[i % len(accents)]
    return plan, m


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", nargs="?", help="what the film is about (Arabic or English)")
    ap.add_argument("--seconds", type=float, default=12); ap.add_argument("--fps", type=int, default=30, choices=[24, 25, 30, 50, 60])
    ap.add_argument("--aspect", default="16:9", choices=list(wbcompat.ASPECTS))
    ap.add_argument("--titles", help="scene titles separated by |  (five beats)"); ap.add_argument("--subtitle", help="one line under every title")
    ap.add_argument("--accents", help="comma-separated #rrggbb accents, cycled over the scenes")
    ap.add_argument("--manifest", help="render this manifest JSON instead of planning")
    ap.add_argument("--out", required=True, help="film .mp4 (or a folder with --plan-only)")
    ap.add_argument("--plan-only", action="store_true")
    a = ap.parse_args()
    if a.manifest:
        m = json.loads(Path(a.manifest).read_text(encoding="utf-8")); plan = None
    else:
        if not a.task:
            ap.error("give a task or --manifest")
        accents = [c.strip() for c in a.accents.split(",")] if a.accents else None
        if accents and not all(len(c) == 7 and c.startswith("#") for c in accents):
            ap.error("--accents: #rrggbb,#rrggbb")
        plan, m = make_manifest(a.task, a.seconds, a.fps, a.aspect, a.titles.split("|") if a.titles else None, a.subtitle, accents)
    if a.plan_only:
        d = Path(a.out); d.mkdir(parents=True, exist_ok=True)
        if plan:
            (d / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
        (d / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
        (d / "index.html").write_text(wbcompat.project_html(m), encoding="utf-8")
        print(json.dumps({"dir": str(d), "scenes": len(m["scenes"]), "seconds": m["duration"]}, ensure_ascii=False)); return 0
    vm = wbcompat.validate_manifest(m)
    out = Path(a.out)
    last = [-1]

    def progress(p):
        pct = int(p * 100)
        if pct // 10 != last[0]:
            last[0] = pct // 10; print(f"  {pct}%", file=sys.stderr, flush=True)
    meta = wbcompat.render_manifest(vm, out, progress)
    (out.with_suffix(".manifest.json")).write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"file": str(out), **meta}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
