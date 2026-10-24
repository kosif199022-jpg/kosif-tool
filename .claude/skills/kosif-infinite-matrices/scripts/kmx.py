#!/usr/bin/env python3
"""KOSIF Infinite Matrices — one front door for the whole skill.

  doctor                         what this machine can run (python, node+playwright, ffmpeg, data, ledger chain)
  recipe validate R.json         six bricks, three distinct parents/families, operators tagged in the 86-card index
  experiment --recipe R --out D  A/B/C counterfactual + replication over seeds + dose-response -> report.json/.md,
             [--render] [--mp4]  scene.html; --render adds stills + pixel A/B/C diff (Chromium), --mp4 a video
             [--record]          append the result to memory/ledger.jsonl (refuses an already-recorded recipe hash)
  scene --recipe R --out F.html  only the playable scene (atlas page contract)
  ledger stats|list|verify       cumulative memory of experiments, ideas, ratings and hypothesis statuses
  rate --experiment EXP-0001 --score 4 --by NAME [--notes ..]   human rating (research feedback)
  ideate --count N [--seed S] [--record]   new parent/role triples, never one already in the 283 seeds or ledger,
                                 biased by rated/confirmed operators (Beta posterior), labelled PROPOSED
  hypotheses stats|show ID|mark ID --status S --evidence FILE
  sources list|add|verify        registry of every source by sha256 (rights, relevance, use)
  bricks summary|show ID         the REA + static-code decomposition of the 86 styles
  probe                          the original numeric glass probe (kept for compatibility)
Stdlib only for everything except --render/--mp4 (node + Playwright + Chromium, ffmpeg for MP4).
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kmx_engine as E  # noqa: E402
import kmx_memory as MEM  # noqa: E402

SKILL = HERE.parent
REPO = SKILL.parents[2]
CATALOG = SKILL / "data" / "86_style_research_database.json"
RENDER_HTML = REPO / "tools" / "render_html.cjs"


def emit(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")


def catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))["styles"]


def _node_playwright():
    if not shutil.which("node"):
        return False
    code = ("for (const s of [()=>require.resolve('playwright',{paths:[process.cwd()]}),()=>'/opt/node-tools/node_modules/playwright',"
            "()=>process.env.KOSIF_PLAYWRIGHT,()=>'playwright']) { try { const p=s(); if (p && require(p).chromium) { process.exit(0) } } catch(e){} } process.exit(1)")
    return subprocess.run(["node", "-e", code], capture_output=True).returncode == 0


def cmd_doctor(a):
    chain = MEM.verify_ledger()
    rep = {"python": sys.version.split()[0], "node": bool(shutil.which("node")), "node_playwright": _node_playwright(),
           "ffmpeg": bool(shutil.which("ffmpeg")), "render_html_cjs": RENDER_HTML.exists(),
           "atlas_assets": all((REPO / ".claude/skills/kosif-superpowers/assets" / f).exists() for f in ("atlas_harness.js", "atlas_sound.js")),
           "catalog_86": len(catalog()) == 86, "hypotheses_283": MEM.hypothesis_status()[1],
           "code_bricks": (SKILL / "data" / "86_style_code_bricks.json").exists(),
           "ledger": chain, "sources": len(MEM.read_registry()["sources"]),
           "network": False}
    rep["can_render"] = rep["node_playwright"]
    rep["can_mp4"] = rep["node_playwright"] and rep["ffmpeg"] and rep["render_html_cjs"]
    emit(rep)
    return 0 if chain["ok"] and rep["catalog_86"] else 1


def lineage_conflicts(parent_ids):
    """Pairs of parents whose code shares function bodies (REA fingerprints): not independent sources."""
    f = SKILL / "data" / "86_style_code_bricks.json"
    if not f.exists():
        return []
    shares = {s["style_id"]: set((s.get("rea") or {}).get("shares_function_bodies_with", []))
              for s in json.loads(f.read_text(encoding="utf-8"))["styles"]}
    return ["%s+%s" % (a, b) for i, a in enumerate(parent_ids) for b in parent_ids[i + 1:] if b in shares.get(a, ())]


def cmd_recipe(a):
    rec = json.loads(Path(a.path).read_text(encoding="utf-8"))
    errs = E.validate_recipe(rec, catalog())
    errs += ["parents share code lineage (REA): " + c for c in lineage_conflicts([p.get("style_id") for p in rec.get("parents", [])])]
    emit({"recipe": rec.get("id"), "valid": not errs, "errors": errs, "recipe_hash": E.recipe_hash(rec) if not errs else None})
    return 0 if not errs else 1


def _report_md(r, rec):
    m, eff = r["main"], r["effect"]
    lines = ["# %s — %s" % (rec["id"], rec["title_en"]), "", "**%s** · %s" % (rec["title_ar"], r["verdict"]), "",
             r["claim_scope"], "", "## Six bricks", ""]
    lines += ["- **%s:** %s" % (b, rec["bricks"][b]) for b in E.BRICKS]
    lines += ["", "## Parents (one role each, three families)", ""]
    lines += ["- %s → `%s` (%s), operator `%s`: %s" % (p["role"], p["style_id"], p["family"], p["operator"], p["why"]) for p in rec["parents"]]
    lines += ["", "## Conditions (same stimulus, same seed, one factor changed)", "", "| condition | change | motes on trace after beam off | memory after off | same memory as A |", "|---|---|---|---|---|"]
    for k, c in rec["conditions"].items():
        lines.append("| %s | `%s` | %.1f%% | %.2f | %s |" % (k, json.dumps(c.get("set") or {}), 100 * m[k]["capture_mean_after_off"],
                                                              m[k]["memory_after_off"], m[k].get("same_memory_as_A", "—")))
    lines += ["", "Chance level (share of the pane that is on the trace): %.1f%%." % (100 * m["_chance_level"]), "",
              "## Replication over %d seeds" % len(r["replication"]), "", "| A minus | mean | sd | min | positive | sign test p |", "|---|---|---|---|---|---|"]
    for k, e in eff.items():
        lines.append("| %s | %+.3f | %.3f | %+.3f | %s | %s |" % (k, e["mean_capture_gain_A_minus"], e["sd"], e["min"], e["positive_in"], e["sign_test_p_one_sided"]))
    lines += ["", "## Dose-response (coupling gain × factor)", "", "| factor | capture A |", "|---|---|"]
    lines += ["| %.2f | %.1f%% |" % (row["gain_factor"], 100 * row["capture_A"]) for row in r["dose_response"]["rows"]]
    lines += ["", "Spearman ρ = %.3f." % r["dose_response"]["spearman_rho"], "", "## Checks", ""]
    lines += ["- %s %s" % ("✅" if v else "❌", k) for k, v in r["checks"].items()]
    if r.get("render"):
        rd = r["render"]
        lines += ["", "## Render evidence", "", "- deterministic (same t → same pixels): %s" % rd.get("same_t_same_pixels"),
                  "- page errors: %d" % len(rd.get("page_errors") or [])]
        for t, d in sorted((rd.get("pixel_diff") or {}).items(), key=lambda kv: float(kv[0])):
            ab = d.get("A_full|B_no_coupling", {}); ac = d.get("A_full|C_no_memory", {})
            lines.append("- t=%ss: A vs B changed pixels %.1f%%, A vs C %.1f%%" % (t, 100 * ab.get("changed_pixel_share", 0), 100 * ac.get("changed_pixel_share", 0)))
        if rd.get("mp4"):
            lines.append("- video: %s" % rd["mp4"])
    lines += ["", "## Limits", "", "- The causal claim holds inside this numerical model; it says nothing about real glass optics.",
              "- Particles read memory but do not write it (one-directional chain, v1).",
              "- Visual quality and meaning still need a human rating (`kmx.py rate`).",
              "- Not a claim of global novelty; parents come from a third-party reference atlas analysed locally.", ""]
    return "\n".join(lines)


def cmd_experiment(a):
    import kmx_scene as S
    rec = E.load_recipe(a.recipe)
    errs = E.validate_recipe(rec, catalog())
    errs += ["parents share code lineage (REA): " + c for c in lineage_conflicts([p["style_id"] for p in rec["parents"]])]
    if errs:
        emit({"valid": False, "errors": errs}); return 1
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    seeds = [int(x) for x in a.seeds.split(",")] if a.seeds else None
    report, runs, ref = E.experiment(rec, seeds=seeds)
    report["roles"] = {p["role"]: p["operator"] for p in rec["parents"]}
    report["parents"] = [p["style_id"] for p in rec["parents"]]
    report["status"] = "NUMERIC_TESTED"
    _, _, main = E.run_conditions(rec)
    scene = S.write_scene(out / "scene.html", rec, runs, main, report["verdict"])
    if a.render:
        if not _node_playwright():
            emit({"error": "render needs node + Playwright + Chromium (see doctor)"}); return 2
        off = rec["stimulus"]["on"][1]
        times = [round(off * 0.6, 2), round(off - 0.1, 2), round(off + 2.0, 2), round(rec["duration"] - 0.1, 2)]
        cap = subprocess.run(["node", str(HERE / "kmx_capture.cjs"), "--in", str(out / "scene.html"), "--out-dir", str(out / "stills"),
                              "--times", ",".join(map(str, times)), "--views", "grid,A_full"]
                             + (["--wav", str(Path(tempfile.gettempdir()) / ("kmx-%s.wav" % rec["slug"]))] if a.mp4 else []),
                             capture_output=True, text=True)
        if cap.returncode != 0:
            emit({"error": "capture failed", "stderr": cap.stderr[-2000:]}); return 1
        rd = json.loads(cap.stdout.strip().splitlines()[-1])
        rd["stills"] = [str(Path(p).relative_to(out)) for p in rd["stills"]]
        wav_tmp = rd.pop("wav", None)
        rd["wav"] = wav_tmp
        after = [d for t, d in rd["pixel_diff"].items() if float(t) > off]
        rd["visible_difference_after_off"] = all(d["A_full|B_no_coupling"]["changed_pixel_share"] > 0.01 for d in after) if after else False
        if a.mp4:
            mp4 = out / (rec["slug"] + ".mp4")
            r = subprocess.run(["node", str(RENDER_HTML), "--in", str(out / "scene.html"), "--out", str(mp4), "--width", "1280", "--height", "720",
                                "--fps", str(rec["fps"]), "--duration", str(rec["duration"])] + (["--audio", rd["wav"]] if rd.get("wav") else []),
                               capture_output=True, text=True)
            rd["mp4"] = mp4.name if r.returncode == 0 else None
            rd["mp4_log"] = [l.replace(str(out.resolve()) + "/", "").replace(str(out) + "/", "")
                             for l in (r.stdout + r.stderr).splitlines() if "VERIFY" in l][-1:]
        if rd.get("wav"):
            Path(rd["wav"]).unlink(missing_ok=True)
        rd.pop("wav", None)
        report["render"] = rd
        if not rd["page_errors"] and rd["same_t_same_pixels"] and rd["visible_difference_after_off"]:
            report["status"] = "RENDER_TESTED"
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (out / "report.md").write_text(_report_md(report, rec), encoding="utf-8")
    summary = {"verdict": report["verdict"], "status": report["status"], "checks": report["checks"], "effect": report["effect"],
               "scene": scene, "out": str(out)}
    if a.record:
        arts = {}
        for p in sorted(out.rglob("*")):
            if p.is_file() and p.suffix in (".json", ".md", ".png", ".jpg", ".html", ".mp4"):
                arts[str(p.relative_to(out))] = MEM.sha256_file(p)
        rel = str(out.resolve().relative_to(REPO)) if str(out.resolve()).startswith(str(REPO)) else str(out)
        ev = MEM.record_experiment(report, {"dir": rel, "sha256": arts}, replication=a.replication,
                                   sources=[s for s in (a.sources or "").split(",") if s])
        summary["ledger"] = {"id": ev["id"], "type": ev["type"], "seq": ev["seq"]}
    emit(summary)
    return 0 if report["verdict"] == "CONFIRMED_IN_MODEL" else 3


def cmd_scene(a):
    import kmx_scene as S
    rec = E.load_recipe(a.recipe)
    runs, ref, m = E.run_conditions(rec)
    emit(S.write_scene(a.out, rec, runs, m))
    return 0


def cmd_ledger(a):
    if a.action == "verify":
        r = MEM.verify_ledger(); emit(r); return 0 if r["ok"] else 1
    if a.action == "list":
        emit([{k: e.get(k) for k in ("seq", "type", "id", "recipe_id", "hypothesis", "experiment", "status", "verdict", "score", "at")}
              for e in MEM.read_ledger()]); return 0
    emit(MEM.stats()); return 0


def cmd_rate(a):
    emit(MEM.record_rating(a.experiment, a.score, a.by, a.notes or "")); return 0


def cmd_ideate(a):
    import matrices
    scores = MEM.operator_scores()
    known = MEM.known_signatures()
    rows = catalog()
    pool = matrices.generate(rows, min(4000, a.count * 40), a.seed)
    weight = lambda h: 1.0 + sum(scores.get(r + ":" + op, {}).get("posterior_mean", 0.5) - 0.5 for r, op in h["roles"].items())
    ranked = sorted(pool, key=lambda h: (-weight(h), h["id"]))
    bricks_file = SKILL / "data" / "86_style_code_bricks.json"
    shares = {}
    if bricks_file.exists():
        for s in json.loads(bricks_file.read_text(encoding="utf-8"))["styles"]:
            shares[s["style_id"]] = set((s.get("rea") or {}).get("shares_function_bodies_with", []))
    out, skipped_lineage = [], 0
    for h in ranked:
        sig = MEM.signature(h["parents"], h["roles"])
        if sig in known:
            continue
        ps = h["parents"]
        if any(b in shares.get(a, ()) for i, a in enumerate(ps) for b in ps[i + 1:]):
            skipped_lineage += 1  # parents reuse the same code (REA fingerprint): not an independent combination
            continue
        known.add(sig)
        idea = {"id": h["id"], "parents": h["parents"], "parent_families": h["parent_families"], "roles": h["roles"],
                "status": "PROPOSED", "weight": round(weight(h), 4), "next_step": "write a recipe (six bricks + conditions) and run kmx.py experiment",
                "origin": "ideate seed=%d" % a.seed}
        out.append(idea)
        if len(out) == a.count:
            break
    recorded = []
    if a.record:
        for i in out:
            recorded.append(MEM.record_idea(i)["seq"])
    emit({"count": len(out), "recorded": recorded, "skipped_shared_code_lineage": skipped_lineage, "ideas": out,
          "note": "Ideas are proposals; nothing was rendered or tested. Weights use ledger feedback only."})
    return 0


def cmd_hyp(a):
    status, counts = MEM.hypothesis_status()
    if a.action == "stats":
        emit({"total": len(status), "by_status": counts}); return 0
    if not a.id:
        emit({"error": "give a hypothesis id"}); return 2
    if a.action == "show":
        seeds = json.loads(MEM.SEEDS.read_text(encoding="utf-8"))["hypotheses"]
        h = next((x for x in seeds if x["id"] == a.id), None)
        if not h:
            emit({"error": "unknown id"}); return 2
        emit(dict(h, current_status=status[a.id])); return 0
    emit(MEM.mark_hypothesis(a.id, a.status, a.evidence, a.note or "")); return 0


def cmd_sources(a):
    if a.action == "list":
        emit(MEM.read_registry()); return 0
    if a.action == "verify":
        s = MEM.verify_source(a.file); emit({"registered": bool(s), "source": s}); return 0 if s else 1
    s, new = MEM.add_source(a.title, a.relevance, a.rights, [u for u in (a.used_for or "").split(";") if u], file=a.file, url=a.url,
                            name=a.name, kind=a.kind, note=a.note or "", pages=a.pages)
    emit({"new": new, "source": s}); return 0


def cmd_bricks(a):
    import kmx_bricks
    return kmx_bricks.main([a.action] + ([a.id] if a.id else []))


def cmd_laws(a):
    import kmx_laws
    return kmx_laws.main(a.rest)


def cmd_probe(a):
    import glass_memory_probe
    emit(glass_memory_probe.probe()); return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor").set_defaults(fn=cmd_doctor)
    p = sub.add_parser("recipe"); p.add_argument("action", choices=["validate"]); p.add_argument("path"); p.set_defaults(fn=cmd_recipe)
    p = sub.add_parser("experiment"); p.add_argument("--recipe", required=True); p.add_argument("--out", required=True)
    p.add_argument("--seeds"); p.add_argument("--render", action="store_true"); p.add_argument("--mp4", action="store_true")
    p.add_argument("--record", action="store_true"); p.add_argument("--replication", action="store_true")
    p.add_argument("--sources", help="comma-separated SRC ids that fed this experiment"); p.set_defaults(fn=cmd_experiment)
    p = sub.add_parser("scene"); p.add_argument("--recipe", required=True); p.add_argument("--out", required=True); p.set_defaults(fn=cmd_scene)
    p = sub.add_parser("ledger"); p.add_argument("action", choices=["stats", "list", "verify"], nargs="?", default="stats"); p.set_defaults(fn=cmd_ledger)
    p = sub.add_parser("rate"); p.add_argument("--experiment", required=True); p.add_argument("--score", type=float, required=True)
    p.add_argument("--by", required=True); p.add_argument("--notes"); p.set_defaults(fn=cmd_rate)
    p = sub.add_parser("ideate"); p.add_argument("--count", type=int, default=10); p.add_argument("--seed", type=int, default=20261025)
    p.add_argument("--record", action="store_true"); p.set_defaults(fn=cmd_ideate)
    p = sub.add_parser("hypotheses"); p.add_argument("action", choices=["stats", "show", "mark"]); p.add_argument("id", nargs="?")
    p.add_argument("--status", choices=MEM.HYP_STATUSES); p.add_argument("--evidence"); p.add_argument("--note"); p.set_defaults(fn=cmd_hyp)
    p = sub.add_parser("sources"); p.add_argument("action", choices=["list", "add", "verify"]); p.add_argument("--file"); p.add_argument("--url")
    p.add_argument("--title"); p.add_argument("--name"); p.add_argument("--kind"); p.add_argument("--relevance", choices=MEM.RELEVANCE)
    p.add_argument("--rights"); p.add_argument("--used-for", dest="used_for", help="semicolon-separated uses"); p.add_argument("--note")
    p.add_argument("--pages", type=int); p.set_defaults(fn=cmd_sources)
    p = sub.add_parser("bricks"); p.add_argument("action", choices=["summary", "show"]); p.add_argument("id", nargs="?"); p.set_defaults(fn=cmd_bricks)
    sub.add_parser("probe").set_defaults(fn=cmd_probe)
    p = sub.add_parser("laws", help="four typed causal laws from v0.2: list | run <recipe> [--render DIR] | verify <report> | atoms")
    p.add_argument("rest", nargs=argparse.REMAINDER); p.set_defaults(fn=cmd_laws)
    a = ap.parse_args(argv)
    if a.cmd == "sources" and a.action == "add" and not (a.title and a.relevance and a.rights):
        ap.error("sources add needs --title, --relevance and --rights")
    if a.cmd == "hypotheses" and a.action == "mark" and not a.status:
        ap.error("hypotheses mark needs --status")
    try:
        return a.fn(a)
    except ValueError as e:
        emit({"error": str(e)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
