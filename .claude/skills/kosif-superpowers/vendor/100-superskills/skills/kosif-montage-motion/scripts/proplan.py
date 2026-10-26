"""KOSIF ProPlan v1 — deterministic, truthful, read-only preflight for media jobs.

Does not claim KOSIF Full Pro runtime. Full Pro requires actual host-exposed
KOSIF Think runtime, request-bound receipts and an authorized external executor.
No third-party skills or executables are automatically loaded or run.
"""
from __future__ import annotations
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to a legacy code page
import argparse
import hashlib
import json
from pathlib import Path
from env_check import check

ENGINE_VERSION = "1.0.0"
CAP = 4


def plan(task: str, mode: str = "pro", media: str | None = None, full_pro_receipts: dict | None = None,
         seconds: float = 12, fps: int = 30, aspect: str = "9:16") -> dict:
    task = (task or "").strip()
    if not task:
        raise ValueError("Task must not be empty")
    if len(task) > 5000:
        raise ValueError("Task is too long (maximum 5000 characters)")
    if not (2 <= seconds <= 600):
        raise ValueError("Duration must be 2 to 600 seconds")
    if fps not in (24, 25, 30, 50, 60):
        raise ValueError("FPS must be one of 24, 25, 30, 50, 60")
    if aspect not in ("9:16", "16:9", "1:1", "4:5"):
        raise ValueError("Unsupported aspect ratio")
    q = task.casefold()
    is_structural = (any(v in q for v in ("وصلا", "أحمال", "الانهيار", "إجهاد", "failure", "structural", "truss", "joint", "load", "finite element", "stress")) and
                     any(v in q for v in ("3d", "مجسم", "هيكل", "جزء", "قطعة", "قوة", "جسر", "structure", "model", "simulation", "محاكاة", "وصلات", "أحمال")))
    is_edit = any(v in q for v in ("مونتاج", "تعديل", "ريل", "video edit", "cut", "caption", "ترجم", "subtitle", "تلوين", "edit this", "قص "))
    is_3d = any(v in q for v in ("ثلاثي", "3d", "three.js", "c4d", "cinema 4d"))
    is_audio = any(v in q for v in ("صوت", "موسيقى", "تعليق", "audio", "music", "voice", "lufs"))
    is_prompt = any(v in q for v in ("برومبت", "prompt", "veo", "sora", "kling", "runway"))
    is_caption = any(v in q for v in ("ترجم", "subtitle", "caption", "كلمات", "كاريوكي"))
    is_reel = any(v in q for v in ("ريل", "reel", "shorts", "tiktok"))
    env = check()
    stages = ["brief", "shot_plan", "storyboard", "motion_score", "timeline", "quality_review"]
    commands = []
    if is_prompt:
        stages.insert(2, "model_prompt_with_continuity")
    elif is_structural:
        stages = ["input_geometry_with_units", "joint_and_support_constraints", "force_and_material_definition", "validate_geometry_and_stability", "deterministic_linear_solve", "idealized_failure_ranking", "part_swap_and_resolve", "interactive_report_and_warnings"]
        commands = ["structural", "twinview"]
    elif is_edit:
        stages.insert(2, "transcript_or_timed_words")
        stages.insert(3, "source_plate_preservation")
        commands.append("reel" if is_reel else "montage")
        if is_caption:
            commands.append("captions")
        commands.extend(["inspect", "sheet"])
    else:
        stages.insert(2, "create_3d_composition" if is_3d else "create_2d_composition")
        commands.extend(["new", "frames", "render", "inspect", "sheet"])
    if is_audio and not is_prompt:
        stages.insert(-1, "audio_mix_and_loudness")
        commands.append("score")
    # Method selection is bounded. Skills are guidance, not claim of execution.
    skills = ["kosif-media-motion"]
    if is_edit or is_3d or is_structural:
        skills.append("kosif-engineering-reliability")
    skills.append("kosif-eval-trust")
    if mode == "pro":
        skills.append("kosif-skill-orchestrator")
    skills = skills[:CAP]
    missing = []
    if commands and "render" in commands and not env["can"]["render_films"]:
        missing.append("MP4 frame render requires browser+FFmpeg")
    if "reel" in commands and not env["can"]["reel"]:
        missing.append("Automatic transcription unavailable; use --transcript with pre-timed words JSON")
    if is_caption and not env["can"]["montage_grade_captions"]:
        missing.append("Burned captions require FFmpeg")
    if is_audio and not env["can"]["score_wav"]:
        missing.append("Offline music synthesis requires numpy")
    if media and not Path(media).is_file():
        missing.append("Input media not found: " + media)
    # Local JSON cannot prove execution or authorization: it is caller-controlled.
    # Only the live KOSIF Full Pro runtime can issue trusted request-bound receipts.
    status = "NOT_FULL_PRO"
    total_frames = round(seconds * fps)
    cut_ratios = (0, .12, .29, .47, .64, .82, 1) if is_structural and not is_prompt else (0, .12, .36, .62, .84, 1)
    cut_frames = [round(total_frames * r) for r in cut_ratios]
    if len(set(cut_frames)) != len(cut_frames):
        raise ValueError("Insufficient frames for selected storyboard beats")
    beat_labels = ("shape", "joint", "load", "break", "swap", "rank") if is_structural and not is_prompt else ("hook", "setup", "contrast", "payoff", "end_card")
    cameras = (("orbit_schematic", "joint_closeup", "force_vector_overlay", "failure_path_overlay", "before_after_split", "ranking_hold") if is_structural and not is_prompt else
               ("dolly_in", "orbit", "side_track", "push_in", "locked") if is_3d else
               ("fast_reveal", "slow_push", "match_cut", "focus_lift", "still_hold"))
    shotlist = []
    for i, beat in enumerate(beat_labels):
        shotlist.append({
            "beat": beat, "start_frame": cut_frames[i], "end_frame_exclusive": cut_frames[i+1],
            "start_s": round(cut_frames[i] / fps, 3), "end_s": round(cut_frames[i+1] / fps, 3),
            "camera_move": cameras[i], "asset_source": "user_media" if is_edit else "local_generated",
            "audio_intent": "voice_first" if is_edit else ("impact" if i in (0,3) else "underscore"),
            "text_policy": "Arabic shaping + RTL inside safe area; maximum 2 lines",
        })
    result = {
        "schema": "kosif.proplan.v1", "version": ENGINE_VERSION,
        "request_digest": hashlib.sha256(task.encode("utf-8")).hexdigest(),
        "request_summary": task, "mode": mode, "full_pro_status": status,
        "full_pro_note": "Requires independent host runtime/executor/QA receipts; local method plans are not Full Pro.",
        "intent": "prompt" if is_prompt else ("structural_twin" if is_structural else "footage_edit" if is_edit else "3d_motion" if is_3d else "2d_motion"),
        "media_provided": bool(media), "route": env["route"],
        "timeline": {"fps":fps,"seconds":seconds,"total_frames":total_frames,"aspect":aspect,
                     "shots":shotlist, "continuity_locks":["speaker_identity","font_family","palette","direction_of_motion"],
                     "safe_area": {"text_top_pct":15,"text_bottom_pct":80} if aspect=="9:16" else {"text_inset_pct":8}},
        "selected_skills": skills, "available_commands": commands, "stages": stages,
        "limitations": missing,
        "deliverable_contract": ["timed_storyboard", "source_attribution", "frame_preview", "final_mp4_or_html", "QA_receipt"],
        "gates": {"source_permission": "required", "preserve_real_identity": True,
                  "audio_target_lufs": -14, "true_peak_ceiling_dbtp": -1,
                  "arabic_text_review": True, "actual_render_required_for_claim": True},
        "external_skills": "KOSIF Atlas finalists only after provenance/license/risk screening; no bulk 15k load",
        "physics_scope": "illustrative 2D/3D pin-jointed axial truss only (no bending, buckling or material nonlinearity); not certified FEA" if is_structural else None,
        "side_effects_performed": False,
    }
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--task", required=True)
    ap.add_argument("--mode", choices=["standard", "pro"], default="pro")
    ap.add_argument("--media", help="Optional local source footage")
    ap.add_argument("--seconds", type=float, default=12)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--aspect", choices=["9:16","16:9","1:1","4:5"], default="9:16")
    ap.add_argument("--out", type=Path, help="Save plan JSON here")
    ap.add_argument("--require-full-pro", action="store_true", help="Fail closed without validated Full Pro receipts")
    ap.add_argument("--receipts-json", type=Path, help="Untrusted diagnostic receipts; never upgrades a local plan to Full Pro")
    args = ap.parse_args()
    receipts = json.loads(args.receipts_json.read_text(encoding="utf-8")) if args.receipts_json else None
    p = plan(args.task, args.mode, args.media, receipts, args.seconds, args.fps, args.aspect)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(p, ensure_ascii=False, indent=2))
    if args.require_full_pro and p["full_pro_status"] != "VERIFIED_FULL_PRO":
        raise SystemExit(3)

if __name__ == "__main__":
    main()
