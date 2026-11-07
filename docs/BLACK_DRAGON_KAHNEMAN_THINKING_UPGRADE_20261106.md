# Black Dragon — Thinking, Fast and Slow upgrade (2026-11-06)

## Source and boundary

Source: user-supplied 468-page English PDF of Daniel Kahneman's *Thinking, Fast and Slow*. PDF page references below are physical PDF page numbers, not book print pagination. This module **paraphrases principles**; it does not republish book passages or pretend that an LLM has a human two-system brain.

Implementation:
- .claude/skills/kosif-black-dragon/scripts/judgment_guard.py — deterministic 11-lens review.
- black_dragon.py think-review --input ... — integrated CLI.
- tests/test_black_dragon_judgment_guard.py — focused regression tests.

## Eleven thinking lenses and council use

| Book lens (PDF pages) | Practical Black Dragon behavior | Existing expert seat |
|---|---|---|
| Fast vs deliberate thought (20–24) | Start with a quick option shortlist; escalate when decisions are costly, irreversible, unsupported or incomplete | Chair |
| Question substitution (84–87) | Compare the real objective with an easy proxy (e.g., impressive transitions versus communicating the voice-over) | Analyst |
| WYSIATI / jumping to conclusions (69–76) | Identify missing evidence; do not infer quality from a coherent pitch alone | Research |
| Small samples and base rates (94–102) | Request an appropriate reference class and its sample size | Research |
| Anchoring (103–111) | Ask for a fresh cost/time estimate before looking at a provided anchor | Decision |
| Availability (112–126) | Check whether viral examples are being mistaken for general audience trends | Research |
| Expert intuition (198–206) | Separate confidence from practiced skill in predictable environments with feedback | Learning |
| Outside view / planning fallacy (207–213) | Compare time with similar completed video jobs; show sample count and median if supplied | Engineer |
| Premortem (222–223) | Consider possible edit failures before a final export | Critic |
| Framing effects (307–317) | Compare equivalent presentations of the same choice | Decision |
| Experiencing and remembering selves (318–330) | Review both the whole timeline and the strongest moment/ending; peak-end is **not** a guaranteed video-engagement formula | Audience |

These are **diagnostic questions**, not 11 empirically proven new AI abilities. The two-system distinction provides a workflow metaphor, not a literal AI cognitive architecture.

## Example: intelligent short-video direction

Input file (illustrative; actual evidence and estimates must be supplied):

~~~json
{
  "goal": "Produce a 60-second Arabic dramatic reel from voice-over",
  "stakes": "medium",
  "reversible": true,
  "target_question": "Which mix of licensed footage and code motion best conveys the scene?",
  "proxy_question": "Which style has the flashiest transitions?",
  "options": ["licensed-footage", "code-motion", "hybrid"],
  "known_evidence": ["voice-over transcript", "timing sheet"],
  "missing_evidence": ["verified usable footage", "real device preview"],
  "sample_size": 0,
  "anchor": 8,
  "recent_examples_only": true,
  "trusted_intuition": true,
  "stable_environment": false,
  "feedback_history": false,
  "failure_scenarios": ["footage mismatches narration", "Arabic captions miss the beat"],
  "storyboard": {
    "hook": "Legible emotional opening",
    "turning_point": "Shot change aligned to the audio shift",
    "ending": "Emotionally complete final scene"
  },
  "intended_audience": "Arabic short-form video viewers"
}
~~~

Commands from repo root:

~~~bash
python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py think-review \
  --input /path/to/video_brief.json --out out/judgment-review.json

python3 -m unittest discover -s tests -p 'test_black_dragon_judgment_guard.py'
~~~

**What it actually does:** reports a structured review mode, book-linked questions, assigned members of the existing **12-seat** council, evidence gaps, and a descriptive project median when durations are supplied. Review is advisory, with no mandatory debate rounds or fictitious independent experts.

**What it does not do:** determine emotional quality automatically, eliminate human bias, invoke independent model agents, render a video, certify licenses, or prove all Atlas skills are integrated. Actual video tests, independent evaluations and evidence logs are still required.

## Next qualification steps

1. Run the committed unit tests on the PR head and retain CI receipts.
2. Review three genuine editing alternatives using evidence from comparable past projects.
3. Obtain initial views without showing others' conclusions, to reduce anchoring.
4. Run a real preview, audio-text timing check, and comprehension review.
5. Record pre/post review changes and audience feedback to measure usefulness rather than assume improvement.

This is an **additive feature on PR #233**, not an automatic merge to main and not a claim that every idea in the 468-page book has been implemented.
