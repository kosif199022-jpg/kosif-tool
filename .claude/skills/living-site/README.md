# Living Site

A Claude Code skill that builds a website in three living levels:

1. **Live 3D** with Spline: one showpiece the visitor can play with.
2. **Film and images** with Higgsfield: a one-shot scroll film and stills from the same world.
3. **Living motion graphics** drawn by Claude in code: diagrams that explain the product and never stop moving.

## Start here

1. **Grab a Higgsfield account:** set up image and video generation at higgsfield.ai. Already have one? Use your existing account.
2. **Install this skill:** follow the install steps below and add it to Claude Code.
3. **Connect your tools:** connect Spline to Claude and sign in to the Higgsfield CLI with your own account.
4. **Start building:** type `/living-site` in Claude Code and describe the website you want to make.

Generating images and video may use credits. Review the cost before starting a generation.

## Install
```bash
mkdir -p ~/.claude/skills && cp -r living-site ~/.claude/skills/
cd ~/.claude/skills/living-site/tools && npm install
```
You also need: the Higgsfield CLI (logged in), the Spline MCP connected in Claude Code, ffmpeg, Python 3 with Pillow and NumPy, Node 18+.

## Use
In Claude Code, say: `/living-site` and name a site you love as the reference, or just describe your brand.

## What is inside
- `SKILL.md`: the five stages and their gates.
- `references/`: one guide per level, the page laws, the copy rules.
- `recipes/`: drop-in pieces (living pipeline, split film, word light, eclipse CTA, LED eyes, live counters, reveal).
- `runtime/`: the scroll film engine (with frame blending), the motion switch, the scroll shield for 3D.
- `tools/`: image and film generation, the chained film builder, cut scan, continuity gate, seamless loops, screenshots.
- `check.py`: the gate for a finished page (`--levels`, `--json`).
- `tools/ledger.py`: the credit ledger as a gate (`add`, `sum --quote --budget`).
- `tools/kling_lint.py`: the gate for a Kling 4.0 master prompt (timing adds up, references have roles, no polish words or brand names, no Arabic dialogue), plus `plan <seconds>`. The worked example is `recipes/kling-master-prompt.txt`, the method is `references/level-2-kling-director.md`.
- `tests/test_tools.py`: self-tests for the gate tools (`python3 tests/test_tools.py`).
- `KOSIF.md`: the KOSIF adaptation (Arabic RTL, Higgsfield MCP mapping, what changed in v5.9, v5.10 and v5.11).
