#!/usr/bin/env python3
"""Black Dragon skill adapters: run the program that ships inside a skill, and check it.

Usage: _black_dragon_skill.py RECIPE ARTIFACT --task=TEXT [--media=FILE]

Most skills are written methods with no code, and they stay "method
descriptions". A few skills ship a real script; each recipe here runs that
script on the task (or on --media, or on the known-answer self-test clip from
_black_dragon_media.py), keeps every output inside ARTIFACT's .work folder and
checks the result. Exit 0 only when the script ran and every required check
passed. Scripts run with `python3 -I`, no shell, no network.
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import _black_dragon_media as media

SCRIPTS = Path(__file__).resolve().parent
SKILLS = SCRIPTS.parents[1]           # .claude/skills
VENDOR = SCRIPTS.parent / "vendor" / "100-superskills" / "skills"
SCHEMA = "kosif.black-dragon.skill-adapter.v1"
PY = [sys.executable, "-I", "-B"]  # -B: never write __pycache__ into the vetted (hash-manifested) vendor folders

SCRIPT = {
    "prompt-master": VENDOR / "prompt-master-pro" / "scripts",
    "prompt-architect": VENDOR / "prompt-architect-reasoning-models" / "scripts",
    "reel-hooks": SKILLS / "kosif-reel-hooks" / "scripts",
    "excel-lambdas": VENDOR / "excel-automation-power" / "scripts",
    "social": VENDOR / "kosif-social" / "scripts",
    "video-editor": VENDOR / "pro-video-editor-ffmpeg" / "scripts",
    "motion-energy": VENDOR / "motion-director-pro" / "scripts",
    "image-prompts": VENDOR / "image-prompt-forge" / "scripts",
    "video-prompts": VENDOR / "video-prompt-director" / "scripts",
    "excel-model": VENDOR / "excel-model-architect" / "scripts",
    "excel-check": VENDOR / "excel-power-formulas" / "scripts",
    "judge-eval": VENDOR / "llm-judge-eval-lab" / "scripts",
    "captions-audio": VENDOR / "audio-reactive-captions-studio" / "scripts",
    "upload-join": SKILLS / "kosif-upload-link" / "scripts",
    "credit-ledger": SKILLS / "living-site" / "tools",
    "shadow-theatre": SKILLS / "kosif-shadow-theatre" / "scripts",
    "web-film": SKILLS / "kosif-web-film" / "scripts",
    "causal-laws": SKILLS / "kosif-infinite-matrices" / "scripts",
    "reel-research": SKILLS / "kosif-instagram-video-research",
    "voice-check": SKILLS / "kosif-voice-studio" / "scripts",
    "animation-qa": VENDOR / "claude-animation-studio" / "scripts",
    "hyperframes-beats": VENDOR / "hyperframes-animation-studio" / "scripts",
    "montage-tools": VENDOR / "kosif-montage-motion" / "scripts",
    "mimic-analyze": VENDOR / "kosif-mimic" / "scripts",
    "pixel-painter": VENDOR / "pixel-studio-painter" / "scripts",
    "kling-director": SKILLS / "kosif-kling-director" / "scripts",
}
RECIPES = tuple(SCRIPT)
NEEDS_MEDIA = {"social", "video-editor", "motion-energy", "captions-audio", "shadow-theatre", "voice-check",
               "animation-qa", "hyperframes-beats", "montage-tools", "mimic-analyze"}
NEEDS_MODULE = {"excel-lambdas": "openpyxl", "motion-energy": "PIL", "excel-model": "openpyxl",
                "excel-check": "openpyxl", "captions-audio": "numpy", "shadow-theatre": "numpy",
                "animation-qa": "PIL", "hyperframes-beats": "numpy", "mimic-analyze": "cv2", "pixel-painter": "cv2"}
# Scripts that import their sibling modules: run without -I (which drops the script's folder from
# sys.path) but still with -E -s, so no environment variable or user site-packages leaks in.
PY_SIBLINGS = [sys.executable, "-E", "-s", "-B"]  # Python packages a recipe's script imports


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def prompt_master(r, d, task, clip, selftest):
    brief = r.work / "brief.json"
    brief.write_text(json.dumps({
        "role": "KOSIF video editor", "context": task, "task": [task], "language": "العربية",
        "output_format": "خطة مونتاج مرقّمة: لقطة، توقيت، انتقال، نص على الشاشة",
        "quality_bar": ["كل انتقال على ضربة", "النص العربي مقروء"], "constraints": ["لا تخترع مصادر"],
    }, ensure_ascii=False), encoding="utf-8")
    prompt = r.work / "prompt-v1.md"
    r.call("prompt_build", [*PY, str(d / "prompt_build.py"), str(brief), "--out", str(prompt)])
    for name in ("prompt-v1.md", "prompt-v1-tests.md", "prompt-v1-variants.md", "prompt-v1-blindspots.md"):
        r.output(r.work / name)
    # exit 1 = REVISE, 3 = BLOCK: the linter's verdict on the prompt, not a broken tool.
    step = r.call("prompt_lint", [*PY, str(d / "prompt_lint.py"), str(prompt), "--json"], ok_codes=(0, 1, 3))
    lint = step.get("receipt") or {}
    r.check("prompt linted with a verdict", lint.get("verdict") in ("PASS", "REVISE", "BLOCK"), lint.get("verdict"))
    r.check("task text is inside the built prompt", task in prompt.read_text(encoding="utf-8"), len(task))
    r.findings.append({"lint_verdict": lint.get("verdict"), "lint_score": lint.get("score"),
                       "issues": [i.get("code") for i in lint.get("issues", [])]})


def prompt_architect(r, d, task, clip, selftest):
    text = r.work / "task.txt"
    text.write_text(task, encoding="utf-8")
    # The suite WRITES 20 attack cases for testing a model; it does not test one by itself.
    suite = r.call("injection_shield suite (writes 20 attack test cases)", [*PY, str(d / "injection_shield.py"), "suite"])
    cases = (suite.get("receipt") or {}).get("cases")
    r.output(r.work / "attacks.jsonl")
    r.check("attack test set has its 20 cases", cases == 20, cases)
    step = r.call("prompt_frontier on the task", [*PY, str(d / "prompt_frontier.py"), str(text), "--json"])
    r.check("frontier analysis returned", isinstance(step.get("receipt"), dict), type(step.get("receipt")).__name__)
    r.findings.append({"frontier_keys": sorted((step.get("receipt") or {}).keys())[:12]})


def reel_hooks(r, d, task, clip, selftest):
    text = r.work / "hook.txt"
    text.write_text(task, encoding="utf-8")
    step = r.call("reel_tools hook (score the task as an opening hook)",
                  [*PY, str(d / "reel_tools.py"), "hook", str(text), "--json"])
    rows = step.get("receipt") or []
    r.check("hook scored", bool(rows) and isinstance(rows[0].get("score"), (int, float)), rows[0].get("score") if rows else None)
    if rows:
        r.findings.append({"score": rows[0].get("score"), "verdict": rows[0].get("verdict"),
                           "weakest": rows[0].get("weakest")})


def excel_lambdas(r, d, task, clip, selftest):
    out = r.work / "lambdas.xlsx"
    step = r.call("lambda_library (named LAMBDA workbook)", [*PY, str(d / "lambda_library.py"), "--out", str(out)])
    r.output(out)
    funcs = (step.get("receipt") or {}).get("functions") or []
    r.check("workbook defines LAMBDA functions", len(funcs) >= 10, len(funcs))
    r.check("output is a real xlsx (zip) file", out.is_file() and out.read_bytes()[:2] == b"PK", None)


def social(r, d, task, clip, selftest):
    pack = r.work / "pack.json"
    r.call("social limits", [*PY, str(d / "social.py"), "limits"])
    r.call("social pack (post-pack skeleton from the video)",
           [*PY, str(d / "social.py"), "pack", str(clip), "--platforms", "tiktok,reels,shorts", "--out", str(pack)])
    r.output(pack)
    data = _json(pack)
    r.check("pack has the three platforms", set(data.get("posts", {})) >= {"tiktok", "reels", "shorts"},
            sorted(data.get("posts", {})))
    r.check("pack measured the video", bool((data.get("probe") or {}).get("seconds")), data.get("probe"))


def video_editor(r, d, task, clip, selftest):
    probe, wav, beats = r.work / "probe.json", r.work / "audio.wav", r.work / "beats.json"
    r.call("probe", [*PY, str(d / "probe.py"), str(clip), "--json", str(probe)])
    r.output(probe)
    r.call("extract WAV (ffmpeg)", ["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-vn", str(wav)])
    r.call("beat_cuts", [*PY, str(d / "beat_cuts.py"), str(wav), "--out", str(beats)])
    r.output(beats)
    data = _json(beats)
    r.findings.append({"bpm": data.get("bpm"), "beats": len(data.get("beats_s") or []),
                       "cut_points_s": (data.get("cut_points_s") or [])[:8]})
    if selftest:
        bpm = data.get("bpm")
        r.check(f"self-test tempo near {media.SELF_TEST['bpm']} BPM (±3)",
                isinstance(bpm, (int, float)) and abs(bpm - media.SELF_TEST["bpm"]) <= 3, bpm)


def motion_energy(r, d, task, clip, selftest):
    out = r.work / "motion_energy.json"
    # exit 1 = verdict REVISE (e.g. a frozen span): a finding about the video, not a broken tool.
    step = r.call("motion_energy", [*PY, str(d / "motion_energy.py"), str(clip), "--out", str(out)], ok_codes=(0, 1))
    r.output(out)
    data = _json(out)
    build = data.get("build") or {}
    r.check("motion measured per frame", (build.get("frames") or 0) > 0, build.get("frames"))
    r.findings.append({**{k: build.get(k) for k in ("mean", "peak", "near_still_share", "longest_still_s")},
                       "verdict": (step.get("receipt") or data).get("verdict"),
                       "issues": (step.get("receipt") or data).get("issues", [])})
    if selftest:
        r.check("self-test clip (shaking camera) is never still", (build.get("near_still_share") or 0) < 0.1,
                build.get("near_still_share"))


# --- Batch 2. Each recipe runs the skill's script twice where it can: once on the task
# (the real job) and once on an input with a PLANTED flaw, and checks that the script
# catches the flaw. A checker that cannot find a known mistake earns no receipt.

def _lint_codes(md: Path) -> list[str]:
    import re
    return re.findall(r"\[(?:REVISE|BLOCK|INFO)\] ([a-z_]+):", md.read_text(encoding="utf-8"))


def image_prompts(r, d, task, clip, selftest):
    clean = {"subject": task, "environment": "minimal studio set", "shot": "medium close-up", "angle": "eye level",
             "lens": "50mm", "lighting": "soft window key from camera left", "style": "photorealistic editorial",
             "aspect": "9:16", "negative": ["watermark", "text artifacts", "extra fingers"]}
    (r.work / "spec.json").write_text(json.dumps(clean, ensure_ascii=False), encoding="utf-8")
    # exit 1/3 = the linter's REVISE/BLOCK verdict on the spec, not a broken tool.
    r.call("image_prompt_forge on the task", [*PY, str(d / "image_prompt_forge.py"), "spec.json", "--out", "prompts.md"],
           ok_codes=(0, 1, 3))
    md = r.work / "prompts.md"
    r.output(md)
    text = md.read_text(encoding="utf-8")
    platforms = ["midjourney", "flux", "sdxl", "chatgpt", "ideogram", "nanobanana"]
    r.check("a prompt for each of the 6 platforms", all(f"## {p}" in text for p in platforms),
            [p for p in platforms if f"## {p}" not in text])
    r.check("task text is inside the prompts", task.strip().rstrip(".") in text, len(task))
    planted = {**clean, "lens": "35mm and 85mm", "aspect": "7:3", "negative": []}
    (r.work / "planted.json").write_text(json.dumps(planted, ensure_ascii=False), encoding="utf-8")
    r.call("image_prompt_forge on a spec with 3 planted flaws",
           [*PY, str(d / "image_prompt_forge.py"), "planted.json", "--out", "planted.md"], ok_codes=(1, 3))
    codes = _lint_codes(r.work / "planted.md")
    r.check("linter caught every planted flaw (two_lenses, aspect, no_negative)",
            {"two_lenses", "aspect", "no_negative"} <= set(codes), codes)
    r.findings.append({"task_spec_issues": _lint_codes(md), "planted_caught": codes})


def video_prompts(r, d, task, clip, selftest):
    doc = {"locks": {"character": "the same presenter in every shot", "style": "warm editorial realism"},
           "aspect": "9:16", "fps": 24,
           "shots": [{"n": 1, "duration": 12, "action": task, "camera": "slow push-in", "lens": "50mm"},
                     {"n": 2, "duration": 5, "action": "close-up reaction to the reveal", "camera": "static", "lens": "85mm"}]}
    (r.work / "shots.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    r.call("video_prompt_forge on the task", [*PY, str(d / "video_prompt_forge.py"), "shots.json", "--out", "prompts.md"],
           ok_codes=(0, 1, 3))
    md = r.work / "prompts.md"
    r.output(md)
    text = md.read_text(encoding="utf-8")
    r.check("task text is inside the shot prompts", task.strip().rstrip(".").lower() in text.lower(), len(task))
    # Known answer: a 12 s shot must be clamped to each platform's limit (Veo 8 s, Kling 10 s).
    r.check("12 s shot clamped to Veo's 8 s", "Duration 8 seconds" in text, None)
    r.check("12 s shot clamped to Kling's 10 s", "Length 10s" in text, None)
    planted = {**doc, "locks": {}, "shots": [{"n": 1, "duration": 6, "action": "", "camera": "push-in then orbit"}]}
    (r.work / "planted.json").write_text(json.dumps(planted, ensure_ascii=False), encoding="utf-8")
    r.call("video_prompt_forge on shots with 3 planted flaws",
           [*PY, str(d / "video_prompt_forge.py"), "planted.json", "--out", "planted.md"], ok_codes=(1, 3))
    codes = _lint_codes(r.work / "planted.md")
    r.check("linter caught every planted flaw (no_locks, multi_camera, no_action)",
            {"no_locks", "multi_camera", "no_action"} <= set(codes), codes)
    r.findings.append({"task_shot_issues": _lint_codes(md), "planted_caught": codes})


def excel_model(r, d, task, clip, selftest):
    import openpyxl
    spec = json.loads((d.parent / "templates" / "spec.example.json").read_text(encoding="utf-8"))
    spec["name"] = task[:60]
    (r.work / "spec.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    step = r.call("model_builder (3-statement model)", [*PY, str(d / "model_builder.py"), "spec.json", "--out", "model.xlsx"])
    model = r.work / "model.xlsx"
    r.output(model)
    sheets = (step.get("receipt") or {}).get("sheets") or []
    r.check("model has PnL, CF, BS and Checks sheets", {"PnL", "CF", "BS", "Checks"} <= set(sheets), sheets)
    audit = r.call("model_audit on the built model", [*PY, str(d / "model_audit.py"), "model.xlsx", "--json"], ok_codes=(0, 1))
    rep = audit.get("receipt") or {}
    r.check("built model has formulas and no hard-coded numbers",
            (rep.get("stats") or {}).get("formulas", 0) > 50 and (rep.get("stats") or {}).get("hardcoded") == 0, rep.get("stats"))
    wb = openpyxl.load_workbook(model)
    cell = next(c for row in wb["PnL"].iter_rows(min_col=4) for c in row if isinstance(c.value, str) and c.value.startswith("="))
    coordinate = cell.coordinate
    cell.value = 12345
    wb.save(r.work / "planted.xlsx")
    planted = r.call("model_audit on a copy with a planted constant",
                     [*PY, str(d / "model_audit.py"), "planted.xlsx", "--json"], ok_codes=(0, 1)).get("receipt") or {}
    r.check("built model passes the audit", rep.get("verdict") == "PASS", rep.get("verdict"))
    listed = any(f.get("cell") == f"PnL!{coordinate}" and f.get("sev") == "HIGH" and "12345" in str(f.get("issue"))
                 for f in planted.get("findings", []))
    hardcoded = (planted.get("stats") or {}).get("hardcoded") or 0
    r.check(f"audit flags the constant planted in PnL!{coordinate} (HIGH finding, hardcoded>=1, verdict not PASS)",
            listed and hardcoded >= 1 and planted.get("verdict") not in (None, "PASS"),
            {"verdict": planted.get("verdict"), "hardcoded": hardcoded, "listed": listed})
    r.findings.append({"built_verdict": rep.get("verdict"), "built_stats": rep.get("stats"),
                       "planted_cell": f"PnL!{coordinate}", "planted_verdict": planted.get("verdict"),
                       "planted_stats_hardcoded": hardcoded})


def excel_check(r, d, task, clip, selftest):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data"
    ws["A1"], ws["A2"], ws["A3"] = "Item", 10, 20
    ws["B1"], ws["B2"] = "Total", "=SUM(A2:A3)"
    good = r.work / "clean.xlsx"
    wb.save(good)
    ws["C2"], ws["C3"], ws["D2"] = "=NOW()", "=OFFSET(A2,1,0)", "42"
    wb.save(r.work / "planted.xlsx")
    clean = r.call("xlsx_check on a clean workbook", [*PY, str(d / "xlsx_check.py"), str(good), "--json"], ok_codes=(0, 1))
    r.output(good)
    rep = clean.get("receipt") or {}
    r.check("clean workbook passes", rep.get("verdict") == "PASS", rep.get("verdict"))
    bad = r.call("xlsx_check on a workbook with planted flaws",
                 [*PY, str(d / "xlsx_check.py"), "planted.xlsx", "--json"], ok_codes=(0, 1)).get("receipt") or {}
    sheet = (bad.get("sheets") or [{}])[0]
    r.check("planted volatile functions found (C2 NOW, C3 OFFSET)", set(sheet.get("volatile") or []) >= {"C2", "C3"},
            sheet.get("volatile"))
    r.check("planted number-stored-as-text found (D2)", "D2" in (sheet.get("text_numbers") or []), sheet.get("text_numbers"))
    r.findings.append({"clean_verdict": rep.get("verdict"), "planted_verdict": bad.get("verdict"),
                       "planted_issues": bad.get("issues")})


def judge_eval(r, d, task, clip, selftest):
    t = d.parent / "templates"
    judges = r.work / "judges"
    judges.mkdir()
    for name, role, s in (("j1", "standard", 8), ("j2", "standard", 8)):
        (judges / f"{name}.json").write_text(json.dumps({"judge": name, "role": role, "scores": dict.fromkeys(
            ("correctness", "security", "readability", "tests"), s)}), encoding="utf-8")
    shutil.copy(t / "judge-score.example.json", judges / "j3.json")  # adversarial: 5, 3, 7, 8
    args = [*PY, str(d / "eval_runner.py"), "score", "--rubric", str(t / "rubric.example.json"),
            "--judges", "judges/*.json", "--assertions", str(t / "assertions.example.json"), "--out", "score.json"]
    rep = r.call("eval_runner score (2 standard + 1 adversarial judge)", args, ok_codes=(0, 1)).get("receipt") or {}
    r.output(r.work / "score.json")
    # Known answer worked out by hand from the rubric weights (0.3, 0.3, 0.2, 0.2):
    # adversarial = 0.3*5 + 0.3*3 + 0.2*7 + 0.2*8 = 5.4; gap 2.6 > 1.5 -> 0.6*8 + 0.4*5.4 = 6.96 < 7 -> not passed.
    r.check("standard average is 8.0", rep.get("standard_avg") == 8.0, rep.get("standard_avg"))
    r.check("adversarial average is 5.4", rep.get("adversarial_avg") == 5.4, rep.get("adversarial_avg"))
    r.check("final score is 6.96 and does not pass 7", rep.get("final") == 6.96 and rep.get("passed") is False,
            [rep.get("final"), rep.get("passed")])
    (r.work / "baseline.json").write_text(json.dumps({"final": 8.2, "passed": True, "hard_fail": False}), encoding="utf-8")
    gate = r.call("eval_runner gate against a better baseline",
                  [*PY, str(d / "eval_runner.py"), "gate", "--run", "score.json", "--baseline", "baseline.json"],
                  ok_codes=(3,)).get("receipt") or {}
    r.check("gate blocks the regression (exit 3, drop 1.24)", gate.get("blocked") is True and gate.get("drop") == 1.24,
            gate.get("drop"))
    r.findings.append({"final": rep.get("final"), "passed": rep.get("passed"), "notes": rep.get("notes"),
                       "gate": gate, "note": "scores are fixed test judges, not a model judging the task"})


def captions_audio(r, d, task, clip, selftest):
    words, t = [], 0.1
    for w in task.split()[:40]:
        words.append({"text": w, "start": round(t, 2), "end": round(t + 0.35, 2)})
        t += 0.4
    (r.work / "words.json").write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    rtl = ["--rtl"] if any("؀" <= ch <= "ۿ" for ch in task) else []
    cap = r.call("captions_pages (pages + SRT/VTT/ASS from word timings)",
                 [*PY, str(d / "captions_pages.py"), "words.json", "--out", "captions", *rtl]).get("receipt") or {}
    for ext in (".json", ".srt", ".vtt", ".ass"):
        r.output(r.work / f"captions{ext}")
    r.check("every task word became a caption word", cap.get("words") == len(words), [cap.get("words"), len(words)])
    srt = (r.work / "captions.srt").read_text(encoding="utf-8")
    r.check("first and last task words are in the SRT", words[0]["text"] in srt and words[-1]["text"] in srt, None)
    data = r.call("extract_audio_data (per-frame energy + beats)",
                  [*PY, str(d / "extract_audio_data.py"), str(clip), "--out", "audio.json"]).get("receipt") or {}
    r.output(r.work / "audio.json")
    r.check("audio measured frame by frame", (data.get("frames") or 0) > 0, data.get("frames"))
    r.findings.append({"pages": cap.get("pages"), "rtl": bool(rtl), "bpm": data.get("bpm"), "beats": data.get("beats")})
    if selftest:
        bpm = data.get("bpm")
        r.check(f"self-test tempo near {media.SELF_TEST['bpm']} BPM (±3)",
                isinstance(bpm, (int, float)) and abs(bpm - media.SELF_TEST["bpm"]) <= 3, bpm)


def upload_join(r, d, task, clip, selftest):
    import hashlib
    import os
    original = os.urandom(300_000) + task.encode("utf-8")
    rows, parts, out = r.work / "rows", r.work / "parts", r.work / "joined"
    rows.mkdir(), parts.mkdir()
    chunks = []
    for i in range(3):
        cid = hashlib.md5(f"part-{i}".encode()).hexdigest()  # a 32-hex id, like the upload page's asset ids
        piece = original[i * 100_000:(i + 1) * 100_000 if i < 2 else None]
        (parts / f"{cid}.mp4").write_bytes(piece)
        chunks.append({"index": i, "id": cid, "size": len(piece)})
    row = {"name": "clip.mp4", "size": len(original), "parts": 3, "status": "done", "chunks": chunks}
    (rows / "clip.json").write_text(json.dumps(row), encoding="utf-8")
    r.call("join_parts (3 uploaded parts)", [*PY, str(d / "join_parts.py"), "--rows", "rows", "--parts", "parts", "--out", "joined"])
    joined = out / "clip.mp4"
    r.output(joined)
    r.check("joined file is byte-for-byte the original (sha256)",
            joined.is_file() and media.sha256(joined) == hashlib.sha256(original).hexdigest(), None)
    (parts / f"{chunks[1]['id']}.mp4").unlink()
    (rows / "clip.json").write_text(json.dumps({**row, "name": "clip-missing.mp4"}), encoding="utf-8")
    miss = r.call("join_parts with a part deleted", [*PY, str(d / "join_parts.py"), "--rows", "rows", "--parts", "parts",
                                                      "--out", "joined"], ok_codes=(1,))
    r.check("missing part reported and no file written", "MISSING" in miss.get("stdout_tail", "")
            and not (out / "clip-missing.mp4").exists(), None)
    r.findings.append({"bytes": len(original), "parts": 3})


def credit_ledger(r, d, task, clip, selftest):
    led, tool = "ledger.tsv", [*PY, str(d / "ledger.py")]
    r.call("ledger add job-1 (10 credits)", [*tool, "add", led, "kling-test", "10", "job-1", "a.mp4"])
    r.call("ledger add job-2 (12 credits)", [*tool, "add", led, "kling-test", "12", "job-2", "b.mp4"])
    again = r.call("ledger add job-2 again", [*tool, "add", led, "kling-test", "12", "job-2", "b.mp4"], ok_codes=(0, 1))
    r.output(r.work / led)
    ok = r.call("ledger sum vs quote 22", [*tool, "sum", led, "--quote", "22", "--json"]).get("receipt") or {}
    r.check("double billing refused: 2 jobs, total 22", ok.get("jobs") == 2 and ok.get("total") == 22.0,
            [ok.get("jobs"), ok.get("total")])
    over = r.call("ledger sum vs budget 15", [*tool, "sum", led, "--budget", "15", "--json"], ok_codes=(1,)).get("receipt") or {}
    r.check("over-budget total blocks the gate (exit 1)", over.get("pass") is False, over.get("problems"))
    r.findings.append({"total": ok.get("total"), "duplicate_add": ((again.get("stdout_tail") or "") + (again.get("stderr_tail") or "")).strip()[:120],
                       "over_budget": over.get("problems"), "note": "test entries only; no credits were spent"})


def shadow_theatre(r, d, task, clip, selftest):
    from PIL import Image, ImageStat
    tool = [*PY, str(d / "shadow_theatre.py")]
    scene = json.loads((d.parent / "scenes" / "lantern-keeper.json").read_text(encoding="utf-8"))
    scene["title"], scene["concept"] = task[:80], task
    (r.work / "scene.json").write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    ok = r.call("check the scene", [*tool, "check", "scene.json"])
    r.check("scene passes the style grammar", (ok.get("stdout_tail") or "").startswith("PASS"), (ok.get("stdout_tail") or "")[:120])
    bad = json.loads(json.dumps(scene))
    bad["scenes"][1]["start"] += 0.5
    for sc in bad["scenes"]:
        sc.pop("memorable", None)
    (r.work / "planted.json").write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
    fail = r.call("check a scene with 2 planted flaws", [*tool, "check", "planted.json"], ok_codes=(1,))
    text = fail.get("stdout_tail") or ""
    r.check("check caught the planted gap and the missing memorable scene",
            "gap or overlap" in text and "memorable" in text, text[:300])
    r.call("stills (preview size)", [*tool, "stills", "scene.json", "--out", "stills", "--preview"])
    stills = sorted((r.work / "stills").glob("still_*.png"))
    for png in stills:
        r.output(png)
    r.check("one still per scene", len(stills) == len(scene["scenes"]), len(stills))
    spread = [round(ImageStat.Stat(Image.open(p).convert("L")).stddev[0], 1) for p in stills]
    r.check("every still has a picture (not a flat frame)", bool(spread) and min(spread) > 5, spread)
    film = r.work / "shadow.mp4"
    r.call("render preview film", [*tool, "render", "scene.json", "--out", str(film), "--preview"], timeout=900)
    row = r.output(film, video=True)
    facts = row.get("probe") or {}
    dur = facts.get("duration")
    r.check(f"film lasts the scene's {scene['duration']} s (±0.2)",
            isinstance(dur, (int, float)) and abs(dur - scene["duration"]) <= 0.2, dur)
    r.check("film has picture and sound", "video" in facts and "audio" in facts, sorted(facts))
    r.call("analyze the input video as a shadow reference", [*tool, "analyze", str(clip), "--out", "analysis"])
    r.output(r.work / "analysis" / "analysis.json")
    r.findings.append({"check": (ok.get("stdout_tail") or "").strip()[:200], "stills_contrast": spread, "film_seconds": dur})


def web_film(r, d, task, clip, selftest):
    tool = [*PY, str(d / "web_film.py")]
    r.call("plan the film from the task", [*tool, "plan", task, "--require", task, "--out", "film.plan.json"])
    plan = _json(r.work / "film.plan.json")
    # The plan is a template a director fills; fill it plainly from the task so check can judge it.
    plan["concept"] = task
    words = task.split() or [task]
    for i, shot in enumerate(plan["shots"]):
        shot["text"] = task if i == 0 else words[i % len(words)]
        shot["motion"] = "ease-out entrance, 2% drift, exit on the cut"
    plan["shots"][0]["covers"] = [0]
    (r.work / "film.plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    r.call("scaffold the page", [*tool, "scaffold", "film.plan.json", "--out", "film.html"])
    r.output(r.work / "film.html")
    rep = r.call("check plan + page", [*tool, "check", "film.plan.json", "--html", "film.html", "--json"], ok_codes=(0, 1))
    res = rep.get("receipt") or {}
    r.check("plan and page pass every structural check", res.get("ok") is True, res.get("errors"))
    bad = json.loads(json.dumps(plan))
    bad["shots"][2]["start"] += 0.4
    bad["shots"][0]["covers"] = []
    (r.work / "planted.plan.json").write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
    caught = r.call("check a plan with 2 planted flaws", [*tool, "check", "planted.plan.json", "--json"],
                    ok_codes=(1,)).get("receipt") or {}
    errs = " | ".join(caught.get("errors") or [])
    r.check("check caught the planted gap and the uncovered requirement",
            "gap or overlap" in errs and "no shot covering" in errs, errs[:300])
    r.findings.append({"shots": len(plan["shots"]), "duration": plan.get("duration"),
                       "note": "structure only; the page was not rendered to video here"})


def causal_laws(r, d, task, clip, selftest):
    recipe = d.parent / "recipes" / "laws" / "elastic-memory.json"
    expected = json.loads(recipe.read_text(encoding="utf-8"))["provenance"]["v0_2_demo_receipt"]["metrics"]
    tool = [*PY, str(d / "kmx.py"), "laws"]
    rep = r.call("run the elastic-memory law (A coupled vs B control)", [*tool, "run", str(recipe), "--render", "lab"]
                 ).get("receipt") or {}
    report = r.work / "lab" / "report.json"
    r.output(report)
    full = [x for x in rep.get("dose") or rep.get("dose_response") or [] if x.get("factor") == 1.0]
    got = full[0].get("mean_post_light_effect") if full else None
    r.check("reproduces the recorded effect 0.097492994 at full gain", got == expected["mean_post_light_effect"],
            [got, expected["mean_post_light_effect"]])
    r.check("causal checks hold (effect, zero gain = zero effect, monotonic dose)",
            all((rep.get("checks") or {}).values()) and bool(rep.get("checks")), rep.get("checks"))
    ver = r.call("verify the report hashes", [*tool, "verify", str(report)]).get("receipt") or {}
    r.check("report verifies", ver.get("verified") is True, ver)
    frame = sorted((r.work / "lab" / "a_coupled").glob("*.svg"))[-1]
    frame.write_text(frame.read_text(encoding="utf-8") + "<!-- tampered -->", encoding="utf-8")
    bad = r.call("verify after tampering one frame", [*tool, "verify", str(report)], ok_codes=(1,)).get("receipt") or {}
    r.check("tampered frame is detected", bad.get("verified") is False, bad)
    r.findings.append({"verdict": rep.get("verdict"), "effect": got, "limits": rep.get("limits"),
                       "note": "the law runs on the stored recipe; the task text does not change it"})


def reel_research(r, d, task, clip, selftest):
    tool = [*PY, str(d / "instagram_research.py"), "--db", "research.sqlite"]
    plan = r.call("plan public-index searches for the task", [*tool, "plan", task]).get("receipt") or {}
    queries = plan.get("queries") or []
    r.check("search plan quotes the task", sum(task in q.get("query", "") for q in queries) >= 1, len(queries))
    good, other = "https://www.instagram.com/reel/KOSIFtest01/", "https://www.instagram.com/reel/KOSIFtest02/"
    a = r.call("index a reel link", [*tool, "add", good, "--title", task[:60]]).get("receipt") or {}
    r.call("index a second reel link (left unreviewed)", [*tool, "add", other])
    off = r.call("try to index a non-Instagram link", [*tool, "add", "https://example.com/reel/KOSIFtest03/"]).get("receipt") or {}
    r.check("Instagram link indexed, foreign link refused", a.get("indexed") == 1 and off.get("indexed") == 0,
            [a.get("indexed"), off.get("indexed")])
    r.call("record a named human review", [*tool, "review", good, "--reviewer", "black-dragon-test",
                                           "--mechanisms", "beat cut", "--observations", "test entry, no media examined"])
    exp = r.call("export reviewed references", [*tool, "export-reviewed", "reviewed.json"]).get("receipt") or {}
    r.output(r.work / "reviewed.json")
    refs = _json(r.work / "reviewed.json").get("references") or []
    r.check("only the reviewed reel is exported", exp.get("exported") == 1 and [x["url"] for x in refs] == [good],
            [x.get("url") for x in refs])
    r.findings.append({"queries": len(queries), "mode": plan.get("mode"),
                       "note": "no network: search links are built, not opened; no media downloaded"})


def voice_check(r, d, task, clip, selftest):
    tool = [*PY, str(d / "voice_studio.py")]
    st = r.call("voice_studio self-test (word timings, SRT/VTT, language)", [*tool, "--self-test"])
    r.check("self-test ok", "self-test: ok" in (st.get("stdout_tail") or ""), (st.get("stdout_tail") or "").strip())
    doc = r.call("doctor (which speech engines are here)", [*tool, "--json", "doctor"]).get("receipt") or {}
    wav, silent = r.work / "voice.wav", r.work / "silent.wav"
    r.call("extract the audio (ffmpeg)", ["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-vn", "-ac", "1", str(wav)])
    r.call("make a 2 s silent file (planted)", ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                                                "-i", "anullsrc=r=44100:cl=mono", "-t", "2", str(silent)])
    rep = r.call("verify the audio", [*tool, "--json", "verify", str(wav)]).get("receipt") or {}
    r.output(wav)
    truth = media.probe(wav).get("duration")
    r.check("audio passes and its duration matches ffprobe (±0.05 s)",
            rep.get("ok") is True and isinstance(truth, (int, float)) and abs(rep.get("duration_s", -1) - truth) <= 0.05,
            [rep.get("duration_s"), truth])
    bad = r.call("verify the planted silent file", [*tool, "--json", "verify", str(silent)]).get("receipt") or {}
    r.check("silent file is rejected", bad.get("ok") is False, bad.get("problem"))
    ready = sorted(k for k, v in (doc.get("engines") or {}).items() if v.get("ready"))
    r.findings.append({"engines_ready": ready, "mean_volume_db": rep.get("mean_volume_db"),
                       "note": "speech, cloning and transcription need an engine; none ran unless listed as ready"})


def animation_qa(r, d, task, clip, selftest):
    from PIL import Image
    frames, planted = r.work / "frames", r.work / "planted"
    frames.mkdir(), planted.mkdir()
    r.call("frames at 15 fps, first 8 s (ffmpeg)", ["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-t", "8",
                                         "-vf", "fps=15", str(frames / "f_%04d.png")])
    real = r.call("qa on the video's frames", [*PY, str(d / "qa.py"), "--frames", "frames", "--fps", "15",
                                                "--out", "qa.json"], ok_codes=(0, 1)).get("receipt") or {}
    r.output(r.work / "qa.json")
    names = sorted(frames.glob("f_*.png"))
    if len(names) < 60:
        raise RuntimeError(f"need at least 4 s of frames, got {len(names)}")
    for i, p in enumerate(names):  # planted copy: 2 s frozen from frame 20, and one black frame at 3.93 s
        src = names[19] if 19 <= i < 50 else p
        shutil.copy(src, planted / p.name)
    Image.new("RGB", Image.open(names[0]).size).save(planted / names[59].name)
    bad = r.call("qa on frames with a planted freeze and black frame", [*PY, str(d / "qa.py"), "--frames", "planted",
                                                                         "--fps", "15"], ok_codes=(1,)).get("receipt") or {}
    kinds = {i.get("type") for i in bad.get("issues", [])}
    r.check("qa caught the planted freeze and black frame", {"freeze", "black_frames"} <= kinds, sorted(kinds))
    r.findings.append({"verdict": real.get("verdict"), "issues": real.get("issues"), "mean_motion": real.get("mean_motion")})
    if selftest:
        r.check("self-test clip (always moving) passes", real.get("verdict") == "PASS", real.get("verdict"))


def hyperframes_beats(r, d, task, clip, selftest):
    wav = r.work / "audio.wav"
    r.call("extract WAV (ffmpeg)", ["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-vn", str(wav)])
    r.call("motion beats", [*PY_SIBLINGS, str(d / "motion.py"), "beats", str(wav), "--out", "beats.json"])
    r.output(r.work / "beats.json")
    beats = _json(r.work / "beats.json")
    if isinstance(beats.get("beats"), list):
        beats["beats"] = len(beats["beats"])
    if isinstance(beats.get("downbeats"), list):
        beats["downbeats"] = len(beats["downbeats"])
    r.check("beats found", (beats.get("beats") or 0) > 0, beats.get("beats"))
    mov = r.call("motion measure (per-frame motion)", [*PY_SIBLINGS, str(d / "motion.py"), "measure", str(clip)]
                 ).get("receipt") or {}
    r.check("motion measured", (mov.get("frames") or 0) > 0, mov.get("frames"))
    r.findings.append({"bpm": beats.get("bpm"), "beats": beats.get("beats"), "downbeats": beats.get("downbeats"),
                       "motion": mov})
    if selftest:
        r.check(f"self-test tempo near {media.SELF_TEST['bpm']} BPM (±3)",
                isinstance(beats.get("bpm"), (int, float)) and abs(beats["bpm"] - media.SELF_TEST["bpm"]) <= 3, beats.get("bpm"))
        r.check("self-test clip (shaking camera) is never still", (mov.get("near_still_share") or 0) < 0.1,
                mov.get("near_still_share"))


def montage_tools(r, d, task, clip, selftest):
    tool = [*PY, str(d / "tools.py")]
    facts = r.call("probe the video", [*tool, "probe", str(clip)]).get("receipt") or {}
    r.check("probe matches ffprobe duration (±0.05 s)",
            abs((facts.get("duration") or -1) - (media.probe(clip).get("duration") or 0)) <= 0.05, facts.get("duration"))
    vert = r.work / "vertical.mp4"
    r.call("reframe to 9:16", [*tool, "aspect", str(clip), "--to", "9:16", "--mode", "crop", "--out", str(vert)], timeout=900)
    row = r.output(vert, video=True)
    size = [((row.get("probe") or {}).get("video") or {}).get(k) for k in ("width", "height")]
    r.check("vertical output is 1080x1920", size == [1080, 1920], size)
    planted = r.work / "planted-silence.mp4"
    r.call("make a 2 s clip whose sound stops at 1.0 s (planted)", [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc2=s=640x360:d=2", "-f", "lavfi", "-i", "sine=d=1",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono:d=1.5", "-filter_complex", "[1][2]concat=n=2:v=0:a=1[a]",
        "-map", "0", "-map", "[a]", "-shortest", str(planted)])
    cut = r.call("cut the silence", [*tool, "silence", str(planted), "--out", "no-silence.mp4"]).get("receipt") or {}
    spans = cut.get("silences") or []
    r.check("silence found at 1.0 s (±0.1)", bool(spans) and abs(spans[0][0] - 1.0) <= 0.1, spans)
    r.output(r.work / "no-silence.mp4", video=True)
    r.findings.append({"input": {k: facts.get(k) for k in ("duration", "video", "audio")}, "silences": spans})


def _cut_clip(path: Path) -> list[str]:
    """ffmpeg argv for a 6 s clip with ONE hard cut at exactly 3.0 s (testsrc2 -> mandelbrot)."""
    return ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc2=s=640x360:r=30:d=3",
            "-f", "lavfi", "-i", "mandelbrot=s=640x360:r=30", "-f", "lavfi", "-i", "sine=d=6",
            "-filter_complex", "[1]trim=duration=3,setpts=PTS-STARTPTS[b];[0][b]concat=n=2:v=1:a=0[v]",
            "-map", "[v]", "-map", "2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-shortest", str(path)]


def mimic_analyze(r, d, task, clip, selftest):
    run = "import sys; sys.path.insert(0, sys.argv[1]); import mm_analyze; mm_analyze.analyze(sys.argv[2], sys.argv[3])"
    cut = r.work / "known-cut.mp4"
    r.call("make a clip with one hard cut at 3.0 s (known answer)", _cut_clip(cut))
    r.call("mm_analyze on the known-cut clip", [*PY_SIBLINGS, "-c", run, str(d), str(cut), str(r.work / "known")], timeout=900)
    known = _json(r.work / "known" / "spec.json")
    r.output(r.work / "known" / "spec.json")
    cuts = [t.get("ts_s") for t in known.get("transitions", []) if t.get("type") == "cut"]
    r.check("finds exactly 2 shots", len(known.get("shots", [])) == 2, len(known.get("shots", [])))
    r.check("finds the hard cut at 3.0 s (±0.1)", len(cuts) == 1 and abs(cuts[0] - 3.0) <= 0.1, cuts)
    ref = r.work / "reference.mp4"
    # The analyzer reads every frame; keep the first 20 s of the input so a long video stays within the timeout.
    r.call("first 20 s of the input (ffmpeg)", ["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-t", "20",
                                                "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", str(ref)], timeout=900)
    r.call("mm_analyze on the input", [*PY_SIBLINGS, "-c", run, str(d), str(ref), str(r.work / "reference")], timeout=900)
    spec = _json(r.work / "reference" / "spec.json")
    r.output(r.work / "reference" / "spec.json")
    r.output(r.work / "reference" / "analysis.md")
    r.check("input analysed into shots", len(spec.get("shots", [])) >= 1, len(spec.get("shots", [])))
    r.findings.append({"input_seconds_analysed": (spec.get("reference") or {}).get("duration"),
                       "shots": len(spec.get("shots", [])),
                       "transitions": [(t.get("type"), t.get("ts_s"), t.get("confidence")) for t in spec.get("transitions", [])][:12],
                       "texts": len(spec.get("texts", []))})


def pixel_painter(r, d, task, clip, selftest):
    from PIL import Image
    from xml.sax.saxutils import escape
    svg = r.work / "drawing.svg"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">'
                   f'<title>{escape(task)}</title><rect width="600" height="400" fill="#1030c0"/>'
                   '<circle cx="300" cy="200" r="100" fill="#e01010"/></svg>', encoding="utf-8")
    film = r.work / "drawing.mp4"
    r.call("film.py: paint the drawing pixel by pixel", [*PY_SIBLINGS, str(d / "film.py"), "drawing", str(svg),
                                                         "--out", str(film), "--seconds", "4"], timeout=900)
    row = r.output(film, video=True)
    first, last = r.work / "first.png", r.work / "last.png"
    r.call("first frame", ["ffmpeg", "-y", "-loglevel", "error", "-i", str(film), "-frames:v", "1", str(first)])
    r.call("last frame", ["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.1", "-i", str(film), "-frames:v", "1", str(last)])

    def px(path, fx, fy):
        im = Image.open(path).convert("RGB")
        return im.getpixel((int(im.width * fx), int(im.height * fy)))

    def near(a, b, tol=24):
        return all(abs(x - y) <= tol for x, y in zip(a, b))
    centre, corner = px(last, 0.5, 0.5), px(last, 0.1, 0.1)
    r.check("finished picture: red circle in the centre (#e01010 ±24)", near(centre, (224, 16, 16)), centre)
    r.check("finished picture: blue background (#1030c0 ±24)", near(corner, (16, 48, 192)), corner)
    r.check("the film starts before the paint (first frame centre is not red)", not near(px(first, 0.5, 0.5), (224, 16, 16)),
            px(first, 0.5, 0.5))
    judged = r.call("judge the finished picture", [*PY_SIBLINGS, str(d / "judge.py"), str(last), "--no-jev"]).get("receipt") or {}
    r.check("judge gave a verdict", judged.get("verdict") in ("PASS", "REVISE", "BLOCK"), judged.get("verdict"))
    r.findings.append({"film": (row.get("probe") or {}).get("duration"), "judge_verdict": judged.get("verdict"),
                       "judge_reasons": judged.get("reasons"),
                       "note": "a two-shape test drawing; the judge rates it as flat art, which is the right call"})


def kling_director(r, d, task, clip, selftest):
    tool = [*PY, str(d / "kling_director.py")]
    # The task's own words decide its lint verdict ("8K" or a camera brand fail), so exit 1 is allowed here.
    r.call("build a 45 s prompt pack from the task", [*tool, "build", "--task", task, "--seconds", "45",
                                                       "--out", "task", "--json"], ok_codes=(0, 1))
    plan = _json(r.work / "task" / "plan.json")
    for name in ("plan.json", "block_01.txt", "block_02.txt", "storyboard_01.txt", "storyboard_02.txt"):
        r.output(r.work / "task" / name)
    r.check("45 s splits into blocks 0-23 s and 23-45 s", [b["film_range_s"] for b in plan["blocks"]] == [[0, 23], [23, 45]],
            [b["film_range_s"] for b in plan["blocks"]])
    block1 = (r.work / "task" / "block_01.txt").read_text(encoding="utf-8")
    r.check("task text is inside SCENE CONTEXT", " ".join(task.split()) in block1.split("ACTIVE REFERENCES")[0], len(task))
    structural = {"duration", "headers", "timing", "refs", "limits"}
    r.check("every block's clock, headers and references pass the lint",
            all(not structural & set(b["lint"]["failed"]) for b in plan["blocks"]),
            [b["lint"]["failed"] for b in plan["blocks"]])
    board = (r.work / "task" / "storyboard_01.txt").read_text(encoding="utf-8")
    r.check("storyboard has 9 panels ending at 23.0 s", board.count("Panel ") == 9 and "-23.0s" in board, None)
    clean = r.call("build a known clean 60 s story", [*tool, "build", "--task", "A courier races the rain to deliver one last letter.",
                                                    "--seconds", "60", "--out", "clean", "--json"]).get("receipt") or {}
    r.check("known clean story: 2 blocks of 30 s, all PASS, 0 credits",
            clean.get("result") == "PASS" and len(clean.get("blocks", [])) == 2 and clean.get("credits_spent") == 0,
            clean.get("result"))
    good = (r.work / "clean" / "block_01.txt").read_text(encoding="utf-8")
    bad = good.replace("STYLE\n", "STYLE\n8K masterpiece, ", 1).replace("OPTICS\n", "OPTICS\nShot on an ARRI Alexa. ", 1)
    bad = bad.replace("AUDIO\n", "AUDIO\nHe says: «يا صاحبي استنى». ", 1).replace("6.0-12.0s — SHOT 2", "6.5-12.0s — SHOT 2", 1)
    (r.work / "planted.txt").write_text(bad, encoding="utf-8")
    planted = r.call("check a copy with 4 planted mistakes", [*tool, "check", "planted.txt", "--duration", "30", "--json"],
                     ok_codes=(1,)).get("receipt") or {}
    failed = {t["name"] for t in planted.get("tests", []) if t["status"] == "FAIL"}
    r.check("lint caught every planted mistake (polish, brands, arabic-dlg, timing)",
            {"polish", "brands", "arabic-dlg", "timing"} <= failed, sorted(failed))
    r.findings.append({"task_result": plan["result"], "task_lint_failed": [b["lint"]["failed"] for b in plan["blocks"]],
                       "planted_caught": sorted(failed), "note": "text only; nothing was generated and no credits were spent"})


RUNNERS = {"prompt-master": prompt_master, "prompt-architect": prompt_architect, "reel-hooks": reel_hooks,
           "excel-lambdas": excel_lambdas, "social": social, "video-editor": video_editor,
           "motion-energy": motion_energy, "image-prompts": image_prompts, "video-prompts": video_prompts,
           "excel-model": excel_model, "excel-check": excel_check, "judge-eval": judge_eval,
           "captions-audio": captions_audio, "upload-join": upload_join, "credit-ledger": credit_ledger,
           "shadow-theatre": shadow_theatre, "web-film": web_film, "causal-laws": causal_laws,
           "reel-research": reel_research, "voice-check": voice_check, "animation-qa": animation_qa,
           "hyperframes-beats": hyperframes_beats, "montage-tools": montage_tools,
           "mimic-analyze": mimic_analyze, "pixel-painter": pixel_painter,
           "kling-director": kling_director}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recipe", choices=RECIPES)
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--task", default="")
    ap.add_argument("--media", default="")
    a = ap.parse_args(argv)
    # Scripts that start their own Python helpers (pixel-studio's film.py) must not write __pycache__ into vendor/ either.
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    artifact = a.artifact.resolve()
    work = artifact.with_name(artifact.stem + ".work")
    work.mkdir(parents=True, exist_ok=False)
    r = media.Run(a.recipe, work)
    report = {"schema": SCHEMA, "recipe": a.recipe, "skill_scripts": str(SCRIPT[a.recipe]), "task": a.task}
    try:
        if not a.task.strip():
            raise RuntimeError("task text is required")
        clip, selftest = None, False
        if a.recipe in NEEDS_MEDIA:
            if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
                raise RuntimeError("ffmpeg and ffprobe are required")
            if a.media:
                clip = Path(a.media).expanduser().resolve()
                if not clip.is_file():
                    raise RuntimeError(f"media not found: {clip}")
                report["input"] = {"kind": "user-media", "path": str(clip), "sha256": media.sha256(clip)}
            else:
                clip, selftest = media.self_test_clip(work), True
                report["input"] = {"kind": "self-test", "path": str(clip), "sha256": media.sha256(clip),
                                   "known_answers": media.SELF_TEST,
                                   "note": "generated test clip with known answers, NOT your footage"}
        RUNNERS[a.recipe](r, SCRIPT[a.recipe], a.task, clip, selftest)
        error = None
    except (RuntimeError, OSError, ValueError, KeyError, IndexError, subprocess.SubprocessError,
            json.JSONDecodeError) as exc:
        error = str(exc)[:500]
    passed = error is None and bool(r.checks) and all(c["pass"] for c in r.checks)
    report.update(steps=r.steps, outputs=r.outputs, checks=r.checks, findings=r.findings,
                  error=error, verdict="passed" if passed else "failed")
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
