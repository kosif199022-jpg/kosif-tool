# KOSIF Creative Quality Gate — evidence-backed creative decisions

This is a **real executable QA module** bundled with KOSIF Superpowers, inspired by rigorous agent evaluation and test-driven development, rather than a collection of model/tool links. It checks that generated reference-edit projects are structurally valid and that claims about what was observed remain truthful.

## Actual behavior

The Reference Edit Engine calls creative_quality_gate.inspect_plan() before completing every generated Remotion project. It validates:

- Consistent target duration and fixed FPS.
- Every shot starts immediately after the last and covers an exact positive number of frames: no gaps, overlaps or duplicate frames.
- Measured audio-transient pulse frames fall strictly inside their own shot.
- Externally aligned words are well formed and not split across a hard cut.
- Replacement clip/audio references have safe names and, when checking the generated project, the actual media files exist.
- The evidence report does not falsely state that source-video pixels were copied, that the rendered MP4 was verified, or that a song's semantic meaning was understood.

It writes quality-audit.json inside the generated editable project. The report has a clearly separated failing-gates list, measured timing metrics and unverified conditions.

## Commands

First produce a reference edit project:

    SKILL_DIR=.claude/skills/kosif-superpowers
    python3 "$SKILL_DIR/scripts/motion_reference_probe.py" ./reference.mp4 --cuts --out ./cuts.json
    python3 "$SKILL_DIR/scripts/reference_edit_engine.py" --probe ./cuts.json --out ./remotion-edit

Then independently repeat the gate against the plan and local replacement media:

    python3 "$SKILL_DIR/scripts/creative_quality_gate.py" ./remotion-edit/src/plan.json --project-dir ./remotion-edit --out ./new-qa-report.json

A broken gate returns exit code 2. File outputs are never overwritten. Claims about user-licensed assets, subjective aesthetics, characters, voice, reference resemblance and delivered MP4 must be established separately, not inferred from passing schema checks.

## What is not a verified decision

These checks do NOT prove a story is beautiful, emotionally appropriate, accurate to reference styles or comprehensible to the audience. They enforce narrow measurable conditions only. Video quality, lip synchronization, scene composition and customer approval must be reviewed on the actual MP4 by a human or calibrated external test suite.

## Regression command

    python3 -m unittest discover -s "$SKILL_DIR/evals" -p test_creative_quality_gate.py -v

This capability follows the spirit of LangGraph/DSPy/DeepEval/Promptfoo/Inspect AI evaluation patterns, but **those libraries are not bundled**. The KOSIF code uses Python standard library, explicit constraints and regression tests. Its evidence status is intentionally lower than full visual/semantic verification.
