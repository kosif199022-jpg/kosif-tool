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
    "dragon-mind": SKILLS / "kosif-dragon-mind" / "scripts",
    "saas-animation": SKILLS / "saas-animation" / "scripts",
    "stickman-studio": SKILLS / "kosif-stickman-studio" / "scripts",
    "creative-council": SKILLS / "kosif-black-dragon" / "scripts",
    "cartoon-short": SKILLS / "cartoon-audio-short" / "kit" / "tools",
    "talking-head-reels": SKILLS / "talking-head-reels" / "scripts",
    "arena": SKILLS / "arena",
}
RECIPES = tuple(SCRIPT)
NEEDS_MEDIA = {"social", "video-editor", "motion-energy", "captions-audio", "shadow-theatre", "voice-check",
               "animation-qa", "hyperframes-beats", "montage-tools", "mimic-analyze", "talking-head-reels"}
NEEDS_MODULE = {"excel-lambdas": "openpyxl", "motion-energy": "PIL", "excel-model": "openpyxl",
                "excel-check": "openpyxl", "captions-audio": "numpy", "shadow-theatre": "numpy",
                "animation-qa": "PIL", "hyperframes-beats": "numpy", "mimic-analyze": "cv2", "pixel-painter": "cv2",
                "saas-animation": "PIL", "cartoon-short": "scipy", "talking-head-reels": "numpy"}
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
    # World Film mode: one world, one continuous camera; the checker enforces the storytelling,
    # readability and camera rules, so plant three breaks and expect all three caught.
    wt = [*PY, str(d / "world_film.py")]
    r.call("world film: write the example plan", [*wt, "example", "--out", "world.plan.json"])
    wrep = r.call("world film: check the example", [*wt, "check", "world.plan.json", "--json"], ok_codes=(0, 1))
    wres = wrep.get("receipt") or {}
    r.check("world film example passes every rule (camera included)", wres.get("ok") is True, wres.get("errors"))
    world = _json(r.work / "world.plan.json")
    by = {o["id"]: o for o in world["objects"]}
    by["t_end"]["text"] = world["beats"][1]["narration"]          # typed while the narrator says it
    by["t_place"]["size"] = 30                                     # too small to read on a phone
    world["beats"][1]["camera"]["drift"] = 0                       # park the camera on one target
    world["beats"][2]["camera"] = dict(world["beats"][1]["camera"])
    (r.work / "planted.world.json").write_text(json.dumps(world, ensure_ascii=False), encoding="utf-8")
    wbad = r.call("world film: check a plan with 3 planted breaks", [*wt, "check", "planted.world.json", "--json"],
                  ok_codes=(1,)).get("receipt") or {}
    werrs = " | ".join(wbad.get("errors") or [])
    r.check("world film check caught said-and-typed text, small type and a dead camera stop",
            "never both" in werrs and "read on a phone" in werrs and "stops dead" in werrs, werrs[:400])
    r.call("world film: build the page", [*wt, "build", "world.plan.json", "--out", "world.html"])
    r.output(r.work / "world.html")
    r.findings.append({"shots": len(plan["shots"]), "duration": plan.get("duration"),
                       "world_film_camera": (wres.get("stats") or {}).get("camera"),
                       "note": "structure only; the pages were not rendered to video here"})


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


def dragon_mind(r, d, task, clip, selftest):
    """The Dragon Mind planner: a deterministic lexical cycle over the whole catalog. It plans, never executes."""
    tool = [*PY_SIBLINGS, "-B", str(d / "dragon_mind.py")]
    r.call("think the task through", [*tool, "think", task, "--out", "think"])
    r.call("think it again (same task, same digest)", [*tool, "think", task, "--out", "again"])
    for name in ("mind_trace.json", "mind_report.md"):
        r.output(r.work / "think" / name)
    t, t2 = _json(r.work / "think" / "mind_trace.json"), _json(r.work / "again" / "mind_trace.json")
    r.check("six-step cycle: frame, explore, decide, build, verify, learn",
            [c["id"] for c in t["cycle"]] == ["frame", "explore", "decide", "build", "verify", "learn"],
            [c["id"] for c in t["cycle"]])
    r.check("tiers cover every catalog entry exactly once", sum(t["tiers"].values()) == t["inventory_total"],
            [t["tiers"], t["inventory_total"]])
    # The same set black_dragon.py loads: the reviewed registry plus generated runner registries.
    import black_dragon as _bd
    reviewed = _bd._load_adapters(_bd.REVIEWED_ADAPTERS)
    r.check("T4 executable equals the adapters black_dragon.py loads (reviewed + generated)",
            t["tiers"].get("T4-executable") == len(reviewed),
            [t["tiers"].get("T4-executable"), len(reviewed)])
    nodes = t["graph"]["nodes"]
    r.check("every graph node has a faculty, typed inputs/outputs and champions",
            bool(nodes) and all(n.get("faculty") and "inputs" in n and "outputs" in n and n.get("champions") for n in nodes),
            len(nodes))
    r.check("same task gives the same digest (deterministic)", t["digest"] == t2["digest"], t["digest"][:12])
    r.check("the trace keeps planned apart from executed", "executed" in t.get("evidence_rule", ""), t.get("evidence_rule"))
    other = r.call("think a different task", [*tool, "think", "Write a pitch deck about solar panels", "--out", "other"])
    r.check("a different task gives a different digest", _json(r.work / "other" / "mind_trace.json")["digest"] != t["digest"],
            other.get("exit_code"))
    # Thinking, Fast and Slow: the trap scanner and the page-level book record are part of the mind.
    r.check("the plan carries the book's always-on System 2 gates",
            {"tfs-wysiati", "tfs-substitution", "tfs-optimism-overconfidence"} <= {x["id"] for x in t.get("traps", [])},
            [x["id"] for x in t.get("traps", [])])
    r.call("scan a task with a planted anchor",
           [*tool, "traps", "anchor the price estimate from the first number the client said"])
    planted = r.steps[-1].get("receipt") or []
    planted = planted if isinstance(planted, list) else planted.get("traps", [])
    hit = next((x for x in planted if x["id"] == "tfs-anchoring"), None)
    r.check("the planted anchor is caught with a debiasing move and book pages",
            bool(hit and hit["score"] > 0 and hit.get("debias_en") and hit.get("pages")),
            hit and [hit["score"], hit.get("pages")])
    r.call("read page 69 of the book record", [*tool, "book", "--page", "69"])
    page = r.steps[-1].get("receipt") or {}
    r.check("the book record covers all 468 pages and returns the page gist",
            page.get("pages_total") == 468 and page.get("pages_read") == 468 and (page.get("page") or {}).get("page") == 69,
            [page.get("pages_total"), page.get("pages_read")])
    r.findings.append({"faculties_needed": t["faculties_needed"], "critic": t["critic"][:5], "tiers": t["tiers"],
                       "traps": [x["id"] for x in t.get("traps", [])],
                       "note": "a planner: nothing in the catalog was executed by this step"})


def creative_council(r, d, task, clip, selftest):
    """The 12-seat creative council with its 525 thinking records, the Kahneman trap gates and the Atlas
    procedures, then the judgment review and the advisory verdict. It plans and scores; it renders nothing."""
    bd = [*PY_SIBLINGS, str(d / "black_dragon.py")]
    cc = [*PY_SIBLINGS, str(d / "creative_council.py")]
    r.call("convene the council on the task", [*bd, "council", task, "--out", "council.json"])
    r.call("convene it again (same task)", [*bd, "council", task, "--out", "again.json"])
    r.output(r.work / "council.json")
    c, c2 = _json(r.work / "council.json"), _json(r.work / "again.json")
    seats = [x["id"] for x in c["roles"]]
    r.check("12 distinct seats", len(seats) == 12 == len(set(seats)), seats)
    ids = [a["id"] for a in c["assignments"]]
    r.check("every thinking record has exactly one primary seat",
            c["total_source_records"] == c["primary_assigned"] == len(ids) == len(set(ids)) and len(ids) >= 525,
            [c["total_source_records"], c["primary_assigned"], len(ids)])
    r.check("every record's seat is a council seat", all(a["primary"] in seats for a in c["assignments"]))
    r.check("same task gives the same fingerprint", c["fingerprint"] == c2["fingerprint"], c["fingerprint"][:12])
    k = c["kahneman_review"]
    gates = {g["id"] for g in k["review_gates"]}
    r.check("the book's 31 traps are loaded and the three System 2 gates are on",
            k["traps_catalogued"] >= 31 and {"tfs-wysiati", "tfs-substitution", "tfs-optimism-overconfidence"} <= gates,
            [k["traps_catalogued"], sorted(gates)])
    r.check("every trap gate goes to the critic and to a primary seat",
            all("critic" in g["reviewers"] and g["primary"] in seats for g in k["review_gates"]))
    r.check("the trap questions reach the seats",
            sum(len(x.get("kahneman_review_questions", [])) for x in c["roles"]) >= len(k["review_gates"]))
    ea = c["external_atlas"]
    r.check("Atlas procedures are loaded and each routed to a seat",
            ea["candidate_procedure_count"] >= 23 and all(p["primary"] in seats for p in ea["candidate_procedures"]),
            ea["candidate_procedure_count"])
    # Judgment review: the 11 book lenses plus the full trap scan, on a brief built from the task.
    brief = r.work / "brief.json"
    brief.write_text(json.dumps({"goal": task, "options": c["options"], "stakes": "high", "reversible": True,
                                 "anchor": 5000}, ensure_ascii=False), encoding="utf-8")
    r.call("judgment review of the brief", [*bd, "think-review", "--input", str(brief), "--out", "review.json"])
    rv = _json(r.work / "review.json")
    r.output(r.work / "review.json")
    r.check("review covers the 11 book lenses", len(rv["review_checks"]) == 11, len(rv["review_checks"]))
    r.check("review also runs the full trap scan", rv["book_trap_scan"]["traps_catalogued"] >= 31
            and len(rv["book_trap_scan"]["gates"]) >= 3, len(rv["book_trap_scan"]["gates"]))
    # Decision: known-answer scores pick a winner; an unbacked INDEPENDENT claim is refused.
    a, b = c["options"][0], c["options"][1]
    sub = {"mode": "SIMULATED", "rounds": {"3": {
        "critic": {"scores": {a: {"meaning": 5, "feasibility": 5}, b: {"meaning": 2, "feasibility": 2}}},
        "decision": {"scores": {a: {"meaning": 4, "feasibility": 5}, b: {"meaning": 3, "feasibility": 2}}}}}}
    (r.work / "sub.json").write_text(json.dumps(sub), encoding="utf-8")
    r.call("score two routes", [*cc, "verdict", "--plan", "council.json", "--submissions", "sub.json",
                                "--out", "verdict.json"])
    v = _json(r.work / "verdict.json")
    r.output(r.work / "verdict.json")
    r.check("the clearly better route wins, labelled simulated",
            v["winning_route"] == a and v["status"] == "SIMULATED_NOT_EXECUTED", [v["winning_route"], v["status"]])
    sub["mode"] = "INDEPENDENT"
    (r.work / "fake.json").write_text(json.dumps(sub), encoding="utf-8")
    fake = r.call("claim independent runs with no run IDs (planted)",
                  [*cc, "verdict", "--plan", "council.json", "--submissions", "fake.json", "--out", "fake-v.json"],
                  ok_codes=(0, 1, 2))
    r.check("the planted independent claim is refused", fake["exit_code"] != 0, fake["exit_code"])
    r.findings.append({"seats": seats, "records": c["total_source_records"],
                       "trap_gates": sorted(gates), "atlas_procedures": ea["candidate_procedure_count"],
                       "winning_route": v["winning_route"],
                       "note": "planning and scoring only; no agent, model, media or paid tool was run"})


def saas_animation(r, d, task, clip, selftest):
    from PIL import Image, ImageDraw
    # Known-answer stills: three frames, each a flat colour, named by their time like render.mjs writes them.
    stills = r.work / "stills"
    stills.mkdir()
    colours = {"0.50": (200, 30, 30), "1.20": (30, 200, 30), "2.00": (30, 30, 200)}
    for t, c in colours.items():
        Image.new("RGB", (1920, 1080), c).save(stills / f"{t}.jpg", quality=95)
    sheet = r.work / "sheet.jpg"
    step = r.call("contact_sheet.py: tile the stills", [*PY, str(d / "contact_sheet.py"), str(stills), str(sheet)])
    r.output(sheet)
    im = Image.open(sheet).convert("RGB")
    r.check("sheet is 4 columns x 1 row of 640x360 tiles", im.size == (2560, 360), im.size)
    got = [im.getpixel((x * 640 + 320, 200)) for x in range(3)]
    r.check("tiles are in time order (red, green, blue)",
            all(all(abs(a - b) <= 24 for a, b in zip(g, c)) for g, c in zip(got, colours.values())), got)
    r.check("script reports 3 frames", "3 frames" in step.get("stdout_tail", ""), step.get("stdout_tail"))
    # A cut-out with a white square on a transparent field, split into a layer by one polygon.
    cut = r.work / "cutout.png"
    a = Image.new("RGBA", (400, 300), (0, 0, 0, 0))
    ImageDraw.Draw(a).rectangle([100, 100, 199, 199], fill=(255, 255, 255, 255))
    a.save(cut)
    r.call("split.py: cut the square into its own layer",
           [*PY, str(d / "split.py"), str(cut), json.dumps({"card": [[90, 90], [210, 90], [210, 210], [90, 210]]})])
    layer, base = r.work / "cutout-card.png", r.work / "cutout-base.png"
    r.output(layer)
    r.output(base)
    lay, bas = Image.open(layer), Image.open(base)
    r.check("layer keeps the square, base loses it",
            lay.getpixel((150, 150))[3] == 255 and bas.getpixel((150, 150))[3] == 0,
            [lay.getpixel((150, 150)), bas.getpixel((150, 150))])
    grid = r.work / "grid.jpg"
    r.call("grid.py: coordinate grid over the cut-out", [*PY, str(d / "grid.py"), str(cut), str(grid)])
    r.output(grid)
    g = Image.open(grid).convert("RGB")
    r.check("grid keeps the image size and fills transparency with red",
            g.size == (400, 300) and g.getpixel((350, 250))[0] > 200 and g.getpixel((350, 250))[1] < 100,
            [g.size, g.getpixel((350, 250))])
    r.findings.append({"note": "image tools only; render.mjs needs Chrome and was not run here, "
                               "and the sound and Blender scripts need scipy and Blender"})


def stickman_studio(r, d, task, clip, selftest):
    """The GrowKaz kit itself is not in the repo (no licence); this runs KOSIF's installer on a synthetic plugin."""
    out = r.work / "selftest"
    r.call("stickman_kit.py: known-answer install self-test", [*PY, str(d / "stickman_kit.py"), "self-test", "--out", str(out)])
    res = _json(out / "selftest.json")
    r.output(out / "selftest.json")
    names = {c["name"]: c["passed"] for c in res["checks"]}
    r.check("all 13 self-test checks pass", res["passed"] and len(names) == 13, names)
    r.check("parent path and symlink are refused", names.get("parent path refused") and names.get("symlink refused"), None)
    r.check("the owner's projects/ folder survives an install", names.get("user's projects/ kept"), None)
    r.check("nothing is written outside the destination", names.get("nothing escaped dest"), None)
    r.findings.append({"note": "installer only; the GrowKaz renderer needs the owner's plugin, Node, Chromium and ffmpeg "
                               "and is not run by the Dragon"})


def cartoon_short(r, d, task, clip, selftest):
    import re
    import wave
    import numpy as np
    from PIL import Image
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg and ffprobe are required")
    sr = 48000

    def write(path, x):
        with wave.open(str(path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())

    # Known-answer voice: three spoken spans (1.0 s, 2.0 s, 1.0 s) with silences between them.
    spans = [(0.30, 1.30), (1.90, 3.90), (4.50, 5.50)]
    total = 5.80
    t = np.arange(int(total * sr)) / sr
    voice = np.zeros_like(t)
    for a, b in spans:
        on = (t >= a) & (t < b)
        voice[on] = 0.5 * np.sin(2 * np.pi * 220 * t[on]) * (0.8 + 0.2 * np.sin(2 * np.pi * 4 * t[on]))
    voice_wav = r.work / "voice.wav"
    write(voice_wav, voice)
    # The script as pasted into a voice generator: an audio tag and tashkeel, which timing.py must strip.
    script = r.work / "script.txt"
    script.write_text("[serious] جُنْدِيٌّ وَاحِدٌ بَقِيَ. ظل يحرس الجسر القديم ثلاثين سنة كاملة بعد الحرب، "
                      "ولم يخبره أحد أنها انتهت. والسبب؟", encoding="utf-8")
    out = r.work / "timing"
    r.call("timing.py: align the Arabic script to the voice by silences",
           [*PY, str(d / "timing.py"), str(voice_wav), str(script), "--out", str(out)])
    r.output(out / "phrases.json")
    r.output(out / "words.json")
    ph = json.loads((out / "phrases.json").read_text(encoding="utf-8"))
    starts = [p["s"] for p in ph["phrases"]]
    r.check("three phrases, one per spoken span", len(starts) == 3, [p["text"] for p in ph["phrases"]])
    r.check("each phrase starts within 0.1 s of its span",
            len(starts) == 3 and all(abs(s - a) <= 0.1 for s, (a, _) in zip(starts, spans)), starts)
    text = " ".join(p["text"] for p in ph["phrases"])
    r.check("tag and tashkeel removed, Arabic detected",
            ph["language"] == "ar" and "[" not in text and not re.search("[\u064b-\u0652]", text), text)
    r.check("frame count is duration x 30", ph["frames30"] == round(ph["duration"] * 30), ph["frames30"])
    # Word times in kosif-voice-studio's words.json format, with one misheard word: the script's own word must win.
    asr = [{"word": w, "start": s, "end": e} for w, s, e in [("جندي", .3, .6), ("واحد", .6, 1.0), ("بقى", 1.0, 1.3)]]
    asr_file = r.work / "asr.json"
    asr_file.write_text(json.dumps(asr, ensure_ascii=False), encoding="utf-8")
    script2 = r.work / "script2.txt"
    script2.write_text("جندي واحد بقي.", encoding="utf-8")
    out2 = r.work / "timing-asr"
    r.call("timing.py: map the script onto recognised word times",
           [*PY, str(d / "timing.py"), str(voice_wav), str(script2), "--out", str(out2), "--asr-words", str(asr_file)])
    w2 = json.loads((out2 / "words.json").read_text(encoding="utf-8"))
    r.output(out2 / "words.json")
    r.check("script words kept over misheard ones, with the recognised times",
            [w["w"] for w in w2] == ["جندي", "واحد", "بقي."] and w2[2]["s"] == 1.0, w2)
    # Mix: a loud music bed and a 2 ms click in a silence. At 50 % RMS the click would peak far above
    # the voice, so the 0.7x peak cap has to act.
    music = 0.6 * np.sin(2 * np.pi * 110 * t)
    sfx = np.zeros_like(t)
    sfx[(t >= 1.50) & (t < 1.502)] = 0.95
    hit = (t >= 1.45) & (t < 1.65)
    write(r.work / "music.wav", music)
    write(r.work / "sfx.wav", sfx)
    step = r.call("mix.py: lock music and SFX under the voice",
                  [*PY, str(d / "mix.py"), str(voice_wav), str(r.work / "music.wav"), str(r.work / "sfx.wav")])
    mixed = r.work / "mix_raw.wav"
    r.output(mixed)
    with wave.open(str(mixed)) as w:
        m = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32767
    r.check("mix is exactly as long as the voice", len(m) == len(voice), [len(m), len(voice)])
    h = int(.05 * sr)
    blocks = np.sqrt((voice[:len(voice) // h * h].reshape(-1, h) ** 2).mean(1))
    vr = float(np.sqrt((blocks[blocks > blocks.max() * 0.01] ** 2).mean()))
    lead = m[int(.05 * sr):int(.25 * sr)]  # before the voice and the hit: music alone
    music_db = 20 * np.log10(np.sqrt((lead ** 2).mean()) / vr)
    r.check("music sits 16 dB under the voice (measured in the mix)", abs(music_db + 16) <= 0.3, round(music_db, 2))
    # In the gap the mix is music + click; the music's own peak is known from its level.
    click = np.abs(m[hit]).max() - 10 ** (-16 / 20) * vr * np.sqrt(2)
    r.check("SFX click capped at 0.7x the voice peak (measured in the mix)",
            click <= 0.7 * np.abs(voice).max() + 0.01, round(float(click), 4))
    said = re.search(r"music ([-+\d.]+) dB.*sfx ([-+\d.]+) dB.*sfx peak ([-+\d.]+) dB", step.get("stdout_tail", ""))
    r.check("script reports music -16.0 dB, SFX at or under -6 dB and the peak cap at -3.1 dB",
            bool(said) and float(said[1]) == -16.0 and float(said[2]) <= -6.0 and float(said[3]) == -3.1,
            step.get("stdout_tail"))
    # Contact sheet of vertical stills, in frame order.
    stills = r.work / "stills"
    stills.mkdir()
    colours = [(200, 30, 30), (30, 200, 30), (30, 30, 200)]
    for i, c in enumerate(colours):
        Image.new("RGB", (1080, 1920), c).save(stills / f"f{i * 40:04d}.jpg", quality=95)
    sheet = r.work / "sheet.jpg"
    r.call("sheet.py: tile the stills", [*PY, str(d / "sheet.py"), str(stills), str(sheet)])
    r.output(sheet)
    im = Image.open(sheet).convert("RGB")
    got = [im.getpixel((x * 270 + 135, 240)) for x in range(3)]
    r.check("sheet is 3 vertical 270x480 tiles in frame order", im.size == (810, 480) and
            all(all(abs(a - b) <= 24 for a, b in zip(g, c)) for g, c in zip(got, colours)), [im.size, got])
    r.findings.append({"note": "kit: timing, mix and contact sheet only; render.mjs needs Chromium with WebGL and "
                               "finish.sh needs rendered frames, so neither ran here"})
    animated_shorts_upstream(r, d.parents[1] / "upstream" / "claude-animated-shorts" / "templates")


# Library code has no CLI: this small driver imports the upstream dsp/sfx_gen modules and prints JSON.
ANIMATED_SHORTS_DRIVER = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
import dsp, sfx_gen
out = sys.argv[2]
t = dsp.tt(4.0)
tone = 0.5 * np.sin(dsp.TAU * 1000 * t)
dsp.write_wav(out + "/tone.wav", np.vstack([tone, tone]))
# A sine at SR/4 with a 45 degree phase: every sample sits at 0.707 of the real (inter-sample) peak.
q = np.sin(dsp.TAU * (dsp.SR / 4) * dsp.tt(0.5) + np.pi / 4)
r = dsp.rng(7)
made = {}
for name, x in (("whoosh", sfx_gen.whoosh(0.8, r)), ("hammer_hit", sfx_gen.hammer_hit(r)), ("applause", sfx_gen.applause(1.5, r))):
    x = np.asarray(x, float)
    dsp.write_wav(out + "/" + name + ".wav", x)
    # Synths come out unscaled; norm_to sets each event's loudest 400 ms to a target, as sfx.py does.
    made[name] = {"seconds": round(x.shape[-1] / dsp.SR, 3), "peak": float(np.abs(x).max()),
                  "finite": bool(np.isfinite(x).all()),
                  "normed_lufs": round(float(dsp.momentary_max(dsp.norm_to(x, -20.0))), 2)}
print(json.dumps({"tone_lufs": round(float(dsp.integrated(np.vstack([tone, tone]))), 2),
                  "sample_peak_db": round(float(20 * np.log10(np.abs(q).max())), 2),
                  "true_peak_db": round(float(dsp.true_peak(q)), 2), "sfx": made}))
"""


def animated_shorts_upstream(r, d):
    """The vendored claude-animated-shorts templates (d): its audio library and QA scripts."""
    import re
    from PIL import Image
    driver = r.work / "driver.py"
    driver.write_text(ANIMATED_SHORTS_DRIVER, encoding="utf-8")
    step = r.call("dsp.py + sfx_gen.py: loudness, true peak and three SFX synths",
                  [*PY, str(driver), str(d / "audio"), str(r.work)])
    got = step.get("receipt") or {}
    for name in ("tone.wav", "whoosh.wav", "hammer_hit.wav", "applause.wav"):
        r.output(r.work / name)
    ff = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(r.work / "tone.wav"), "-af", "ebur128",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    ref = re.findall(r"I:\s+(-?[\d.]+) LUFS", ff)
    r.check("BS.1770 integrated loudness matches ffmpeg ebur128 within 0.2 LU",
            bool(ref) and "tone_lufs" in got and abs(got["tone_lufs"] - float(ref[-1])) <= 0.2,
            [got.get("tone_lufs"), ref[-1:] or None])
    r.check("true peak finds the inter-sample peak (0 dBTP) where samples show -3 dB",
            abs(got.get("true_peak_db", 9) - 0.0) <= 0.2 and abs(got.get("sample_peak_db", 9) + 3.01) <= 0.05,
            [got.get("sample_peak_db"), got.get("true_peak_db")])
    sfx = got.get("sfx", {})
    r.check("three SFX synths render finite, audible sound that norm_to sets to -20 LUFS momentary",
            len(sfx) == 3 and all(v["finite"] and v["peak"] > 0.01 and v["seconds"] > 0.05
                                  and abs(v["normed_lufs"] + 20) <= 0.05 for v in sfx.values()), sfx)
    # A short with a planted 1 s black span (frames 60-89) after 2 s of moving picture, plus a tone.
    vid = r.work / "short.mp4"
    r.call("ffmpeg: build the test short", [
        "ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=180x320:r=30:d=2",
        "-f", "lavfi", "-i", "color=c=black:s=180x320:r=30:d=1", "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]", "-map", "[v]", "-map", "2:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(vid)])
    qa = r.work / "qa"
    r.call("short_qa.py: frame-by-frame QA", [*PY, str(d / "scripts" / "short_qa.py"), str(vid), str(qa)])
    rep = qa / "report.md"
    r.output(rep)
    text = rep.read_text(encoding="utf-8") if rep.is_file() else ""
    black = re.search(r"black \[([^\]]*)\]", text)
    frames = [int(x) for x in re.findall(r"\d+", black[1])] if black else []
    r.check("QA finds the planted black span and no black in the moving part",
            bool(frames) and min(frames) >= 59 and 60 in frames, frames[:20])
    r.check("QA reports specs and loudness", "SPECS 180x320" in text and "LOUDNESS" in text, text[:300])
    # Side-by-side sheet: two of ours over one reference, all scaled to 200 px high.
    ims = []
    for name, size, c in (("a", (100, 200), (200, 30, 30)), ("b", (100, 200), (30, 200, 30)), ("ref", (200, 400), (30, 30, 200))):
        path = r.work / f"{name}.jpg"
        Image.new("RGB", size, c).save(path, quality=95)
        ims.append(str(path))
    sheet = r.work / "sbs.jpg"
    r.call("sbs_sheet.py: ours over the reference",
           [*PY, str(d / "scripts" / "sbs_sheet.py"), str(sheet), "--ours", *ims[:2], "--ref", ims[2], "--h", "200"])
    r.output(sheet)
    im = Image.open(sheet).convert("RGB")
    r.check("sheet is 2 rows of 200 px with ours on top, reference below",
            im.size == (208, 416) and im.getpixel((50, 100))[0] > 150 and im.getpixel((50, 316))[2] > 150,
            [im.size, im.getpixel((50, 100)), im.getpixel((50, 316))])
    r.findings.append({"note": "upstream: audio library and QA scripts only; the Remotion bridge template, music.py "
                               "and mix.py are story-specific and need the bridge project, so they did not run here"})


def talking_head_reels(r, d, task, clip, selftest):
    """Known-answer reel: a 7 s 'talk' with speech at 0.3-1.3, 2.8-3.8 and 5.3-6.3 s, cut, mastered, planned,
    validated and rendered by the skill's own scripts; Arabic text must reveal word by word."""
    from PIL import Image, ImageStat
    tool = lambda name, *a: [*PY_SIBLINGS, str(d / name), *a]
    jumuah = SKILLS.parents[1] / "fonts" / "kosif-jumuah" / "KOSIFJumuah-Bold.ttf"
    if not jumuah.is_file():
        raise RuntimeError(f"Arabic font missing: {jumuah}")
    os.environ["REEL_FONT_FILES"] = str(jumuah)
    talk = r.work / "talk.mp4"
    speech = "+".join(f"between(t\\,{a}\\,{b})" for a, b in ((0.3, 1.3), (2.8, 3.8), (5.3, 6.3)))
    r.call("make the known-answer talk (ffmpeg)", [
        "ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=25:duration=7",
        "-f", "lavfi", "-i", f"aevalsrc='0.3*sin(2*PI*220*t)*({speech})+0.001*sin(2*PI*50*t)':s=48000:d=7",
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-shortest", str(talk)])
    P = r.work / "P"
    r.call("prepare_project.py", tool("prepare_project.py", str(talk), "--project", str(P)))
    cfg = _json(P / "project.json")
    r.check("project reads the 7 s source", abs(cfg["src_dur"] - 7.0) <= 0.1, cfg["src_dur"])
    words = [{"word": "أهلاً", "start": 0.3, "end": 0.8}, {"word": "بيكم.", "start": 0.8, "end": 1.3},
             {"word": "ده", "start": 2.8, "end": 3.8}, {"word": "شغال", "start": 5.3, "end": 5.8},
             {"word": "دلوقتي", "start": 5.8, "end": 6.3}]
    (r.work / "words.json").write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    r.call("words_to_asr.py (voice-studio words.json)", tool("words_to_asr.py", str(P), "words.json", "--language", "ar"))
    asr = _json(P / "analysis" / "asr.json")
    r.check("transcript splits after the full stop and the long silence", len(asr) == 3, [s["text"] for s in asr])
    cut = r.call("cut_pauses.py", tool("cut_pauses.py", str(P)))
    cfg = _json(P / "project.json")
    prog = cfg.get("program_dur") or 0
    r.check("pauses tightened: 3 speech segments kept, more than 2.5 s of air removed",
            "segments 3" in (cut.get("stdout_tail") or "") and 3.0 <= prog <= 7.0 - 2.5, prog)
    pw = _json(P / "analysis" / "program_words.json")
    r.check("every word re-timed onto the program", len(pw) == len(words) and all(w["s"] < prog for w in pw), len(pw))
    r.call("master_audio.py", tool("master_audio.py", str(P)))
    master = P / "audio" / "program_master.wav"
    loud = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(master), "-af", "ebur128", "-f", "null", "-"],
                          capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=120).stderr
    lufs = [float(l.split("I:")[1].split("LUFS")[0]) for l in loud.splitlines() if l.strip().startswith("I:")]
    r.check("voice mastered to -14 LUFS (±0.7), measured by ffmpeg ebur128", bool(lufs) and abs(lufs[-1] + 14) <= 0.7, lufs[-1:])
    t1, t2 = pw[2]["s"], pw[3]["s"]
    edl = {"name": "selftest", "W": 1080, "H": 1920, "accent": "#ED3B22",
           "fonts": {"serif": "Anton-Regular", "didot": "Anton-Regular", "sub": "Anton-Regular", "ar": "KOSIFJumuah-Bold"},
           "zoom": [[0.0, t1, "tight"], [t1, prog, "wide"]],
           "inserts": [{"id": "num", "t0": t1, "t1": t2, "kind": "number", "label": "SAVED", "from": 0, "to": 42,
                        "suffix": "%", "count": [0.1, 0.6], "trans": "zoom"}],
           "text": [{"font": "anton", "text": (task.split() or ["REEL"])[0][:12].upper(), "t0": 0, "t1": t1, "x": 540, "y": 1100, "size": 150},
                    {"font": "ar", "text": "ده شغال دلوقتي", "t0": t2, "t1": prog, "x": 540, "y": 1100, "size": 120,
                     "color": "#ED3B22", "anim": "build"}]}
    (P / "edl.json").write_text(json.dumps(edl, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = r.call("validate_edl.py", tool("validate_edl.py", str(P / "edl.json")))
    out = ok.get("stdout_tail") or ""
    r.check("EDL passes with 0 errors", " 0 error(s)" in out, out[-200:])
    r.check("validator flags Arabic 'build' (rendered word by word)", "Arabic text cannot build" in out, None)
    bad = json.loads(json.dumps(edl))
    bad["inserts"].append(dict(bad["inserts"][0], id="clash", t0=t1 + 0.2))
    bad["text"][0]["font"] = "comic"
    (P / "planted.json").write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
    caught = r.call("validate a plan with 2 planted flaws", tool("validate_edl.py", str(P / "planted.json")), ok_codes=(1,))
    msg = caught.get("stdout_tail") or ""
    r.check("validator caught the overlapping insert and the unknown font", "overlaps num" in msg and "font must be" in msg, msg[-300:])
    times = [round(t1 / 2, 2), round((t1 + t2) / 2, 2), round(t2 + 0.06, 2), round(prog - 0.25, 2)]
    r.call("render_reel.py --stills", tool("render_reel.py", str(P / "edl.json"), "--stills", *map(str, times),
                                           "--out-dir", str(P / "qa" / "stills")), timeout=900)
    pngs = sorted((P / "qa" / "stills").glob("f_*.png"))
    for png in pngs:
        r.output(png)
    r.output(P / "qa" / "stills" / "sheet.jpg")
    sizes = {Image.open(p).size for p in pngs}
    r.check("one 1080x1920 still per asked moment", len(pngs) == len(times) and sizes == {(1080, 1920)}, [len(pngs), sorted(sizes)])
    spread = [round(ImageStat.Stat(Image.open(p).convert("L")).stddev[0], 1) for p in pngs]
    r.check("every still has a picture", bool(spread) and min(spread) > 5, spread)
    def red_width(p):
        im = Image.open(p).convert("RGB").crop((0, 980, 1080, 1220))
        xs = [x for x in range(0, 1080, 2) for y in range(0, 240, 4) if (lambda c: c[0] > 180 and c[1] < 110 and c[2] < 90)(im.getpixel((x, y)))]
        return (max(xs) - min(xs)) if xs else 0
    early, late = red_width(pngs[2]), red_width(pngs[3])
    r.check("Arabic line reveals word by word (first word narrower than the full line)", 0 < early < late * 0.6, [early, late])
    film = P / "render" / "selftest_v1.mp4"
    r.call("render_reel.py full render", tool("render_reel.py", str(P / "edl.json"), "--out", str(film)), timeout=1800)
    row = r.output(film, video=True)
    facts = row.get("probe") or {}
    v = facts.get("video") or {}
    r.check("reel is 1080x1920 with sound", (v.get("width"), v.get("height")) == (1080, 1920) and "audio" in facts, facts)
    r.check(f"reel lasts the program's {prog} s (±0.15)", abs((facts.get("duration") or 0) - prog) <= 0.15, facts.get("duration"))
    if clip is not None and not selftest:
        r.call("prepare_project.py on your media", tool("prepare_project.py", str(clip), "--project", str(r.work / "yours")), ok_codes=(0, 1))
    r.findings.append({"program_seconds": prog, "lufs": lufs[-1:], "stills_contrast": spread, "arabic_reveal_px": [early, late],
                       "note": "Apple Vision mattes (macOS) and faster-whisper were not used; words came from a voice-studio words.json"})


def arena(r, d, task, clip, selftest):
    """Known-answer tournament through the arena skill's own bracket.py, with stand-in agents (no model is called).
    Each stand-in solution has a known quality; the planted fatal one carries the best scores and must still lose."""
    import hashlib
    import importlib.util
    tool = lambda *a: [*PY, str(d / "bracket.py"), *map(str, a)]
    def tree_hash(root):
        h = hashlib.sha256()
        for f in sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
            h.update(str(f.relative_to(root)).encode() + media.sha256(f).encode())
        return h.hexdigest()
    before = tree_hash(d)
    spec = importlib.util.spec_from_file_location("kosif_arena_bracket", d / "bracket.py")
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)  # read-only helpers (job paths); every state change goes through the CLI
    plan = r.call("bracket.py plan --agents 100", tool("plan", "--agents", 100)).get("stdout_tail") or ""
    total = next((l.split() for l in plan.splitlines() if l.strip().startswith("total")), [])
    r.check("100 agents: 7 rounds, 595 sub-agent calls, 70 waves", total[1:3] == ["595", "70"] and "7 rounds" in plan, total)
    quick = r.call("bracket.py plan --quick", tool("plan", "--quick")).get("stdout_tail") or ""
    qt = next((l.split() for l in quick.splitlines() if l.strip().startswith("total")), [])
    r.check("--quick: 16 agents, 91 calls, 16 waves", qt[1:3] == ["91", "16"], qt)
    run, twin = r.work / "run", r.work / "twin"
    (r.work / "task.md").write_text(task, encoding="utf-8")
    baseline = r.work / "baseline.md"
    baseline.write_text("REJECTED ANSWER: too vague.", encoding="utf-8")
    r.call("bracket.py init 16 agents, seed 7, with the rejected answer",
           tool("init", "--agents", 16, "--seed", 7, "--task-file", "task.md", "--baseline-file", "baseline.md", "--dir", run))
    r.call("bracket.py init again with the same seed", tool("init", "--agents", 16, "--seed", 7, "--task-file", "task.md", "--dir", twin))
    state = _json(run / "arena.json")
    cards = {a: tuple(v["card"][k]["id"] for k in ("reasoning", "workflow", "strategy")) for a, v in state["agents"].items()}
    twin_cards = {a: tuple(v["card"][k]["id"] for k in ("reasoning", "workflow", "strategy"))
                  for a, v in _json(twin / "arena.json")["agents"].items()}
    r.check("16 different cards, and the same seed deals the same cards", len(set(cards.values())) == 16 and cards == twin_cards,
            len(set(cards.values())))
    r.check("16 cards cover every reasoning mode", len({c[0] for c in cards.values()}) == min(16, len(B.load_strategies()["reasoning"])),
            len({c[0] for c in cards.values()}))
    quality = {a: 3 + (i * 7) % 16 for i, a in enumerate(sorted(state["agents"]))}  # known, all different
    first = state["rounds"][0]["matches"][0]
    planted = first["a"] if quality[first["a"]] > quality[first["b"]] else first["b"]
    honest = first["b"] if planted == first["a"] else first["a"]
    def score(q, fatal=False):
        v = max(0, min(10, round(q * 10 / 18)))
        return {"correctness": v, "completeness": v, "specificity": v, "robustness": v, "clarity": v, "fatal": fatal}
    def jobs(phase):
        return B.phase_jobs(_json(run / "arena.json"), phase)
    def write(path, text):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text, encoding="utf-8")
    r.call("bracket.py prompts spawn", tool("prompts", "spawn", "--dir", run))
    briefs = [Path(j["prompt"]).read_text(encoding="utf-8") for j in jobs("spawn")]
    r.check("every one of the 16 spawn briefs carries the task byte for byte", len(briefs) == 16 and all(task in b for b in briefs),
            sum(task in b for b in briefs))
    for j in jobs("spawn"):
        write(j["outputs"][0], f"SOLUTION {j['agent']} quality {quality[j['agent']]}")
    planted_lost, rounds = None, 0
    while True:
        nxt = r.call("bracket.py next", tool("next", "--dir", run)).get("stdout_tail") or ""
        st = _json(run / "arena.json")
        if st["champion"] and (st.get("final") or {}).get("result"):
            break
        if st["champion"]:
            r.call("bracket.py prompts final", tool("prompts", "final", "--dir", run))
            fin = st["final"]
            x = (run / "final" / "X.md").read_text(encoding="utf-8")
            y = (run / "final" / "Y.md").read_text(encoding="utf-8")
            fprompt = Path(jobs("final")[0]["prompt"]).read_text(encoding="utf-8")
            r.check("final check is blind: X/Y copies, no champion id or baseline path in the brief",
                    {x, y} == {(run / "baseline.md").read_text(encoding="utf-8"), Path(st["agents"][st["champion"]]["solution"]).read_text(encoding="utf-8")}
                    and st["champion"] not in fprompt and "baseline.md" not in fprompt, fin)
            champ = "x" if fin["X"] == "champion" else "y"
            write(jobs("final")[0]["outputs"][0], json.dumps({"scores": {champ.upper(): score(17), ("Y" if champ == "x" else "X"): score(4)},
                                                               "winner": champ.upper(), "reason": "known answer", "fixed": ["vague"]}))
            r.call("bracket.py collect (final)", tool("collect", "--dir", run))
            continue
        rd = st["rounds"][-1]
        rounds = rd["n"]
        for j in jobs("attack"):
            write(j["outputs"][0], f"ATTACK 1 [MINOR] stand-in\nWhere: all\nProblem: known answer")
        for j in jobs("defend"):
            prev = Path(st["agents"][j["agent"]]["solution"]).read_text(encoding="utf-8")
            write(j["outputs"][0], "ATTACK 1: CONCEDE. fixed")
            write(j["outputs"][1], prev)
        for j in jobs("judge"):
            a, b = j["a"], j["b"]
            fatal = {planted} & {a, b} and rd["n"] == 1
            sa, sb = score(quality[a], a == planted and bool(fatal)), score(quality[b], b == planted and bool(fatal))
            pick = a if quality[a] > quality[b] else b
            write(j["outputs"][0], json.dumps({"match": j["match"], "scores": {a: sa, b: sb}, "winner": pick,
                                               "reason": "known answer", "survived": ["stand-in attack"], "standing": {a: [], b: []}}))
        r.call(f"bracket.py collect round {rd['n']}", tool("collect", "--dir", run))
        if rd["n"] == 1:
            m = next(x for x in _json(run / "arena.json")["rounds"][0]["matches"] if x["id"] == first["id"])
            planted_lost = m["winner"] == honest
        r.call(f"bracket.py advance round {rd['n']}", tool("advance", "--dir", run))
        if rounds > 8:
            raise RuntimeError("bracket did not converge")
    r.check("planted fatal solution lost although its scores were higher", planted_lost is True, [planted, honest])
    st = _json(run / "arena.json")
    alive = [a for a, v in st["agents"].items() if v["alive"]]
    best = max((a for a in quality if a != planted), key=lambda a: quality[a])
    r.check("bracket ends with one champion after 4 rounds", alive == [st["champion"]] and rounds == 4, [alive, rounds])
    r.check("the best honest solution won", st["champion"] == best, [st["champion"], best])
    w = r.call("bracket.py winner --json", tool("winner", "--json", "--dir", run)).get("receipt") or {}
    r.check("winner report names the champion and the final check", w.get("champion") == best and bool(st["final"]["result"])
            and st["final"]["result"]["better"] == "champion", {k: w.get(k) for k in ("champion", "rounds")})
    r.check("the skill folder is unchanged by the run", tree_hash(d) == before, None)
    r.output(run / "arena.json")
    r.findings.append({"champion": st["champion"], "card": cards[st["champion"]], "rounds": rounds,
                       "note": "stand-in agents with known answers: this proves the bracket, not the quality of any model answer"})


RUNNERS = {"prompt-master": prompt_master, "prompt-architect": prompt_architect, "reel-hooks": reel_hooks,
           "excel-lambdas": excel_lambdas, "social": social, "video-editor": video_editor,
           "motion-energy": motion_energy, "image-prompts": image_prompts, "video-prompts": video_prompts,
           "excel-model": excel_model, "excel-check": excel_check, "judge-eval": judge_eval,
           "captions-audio": captions_audio, "upload-join": upload_join, "credit-ledger": credit_ledger,
           "shadow-theatre": shadow_theatre, "web-film": web_film, "causal-laws": causal_laws,
           "reel-research": reel_research, "voice-check": voice_check, "animation-qa": animation_qa,
           "hyperframes-beats": hyperframes_beats, "montage-tools": montage_tools,
           "mimic-analyze": mimic_analyze, "pixel-painter": pixel_painter,
           "kling-director": kling_director, "dragon-mind": dragon_mind, "saas-animation": saas_animation,
           "creative-council": creative_council, "cartoon-short": cartoon_short, "talking-head-reels": talking_head_reels,
           "arena": arena, "stickman-studio": stickman_studio}


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
