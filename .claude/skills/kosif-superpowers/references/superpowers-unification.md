# KOSIF Superpowers Ultimate — Unified Claude Skill System

**Primary / canonical skill:** KOSIF Superpowers (`kosif-superpowers`).
**Complementary process-methods source:** [obra/superpowers](https://github.com/obra/superpowers), release **v7.0.0**, pinned commit `bb92a77741419a4ab5f06e711a283343f1ada0c3`.
**License:** MIT, original copyright preserved in [vendor/obra-superpowers-v7/LICENSE](https://github.com/kosif199022-jpg/kosif-tool/blob/main/.claude/skills/kosif-superpowers/vendor/obra-superpowers-v7/LICENSE). The vendor skills are retained as independent documents with their support files and references, rather than flattening or dropping content.

## What was integrated?

15 original v7 workflow skills: brainstorming, diagnosing-superpowers, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, and writing-skills.

KOSIF remains the **capability map and executor** (4,719 powers on the referenced release snapshot, check current count at runtime). The upstream 15 are workflow disciplines: thinking before building, implementation plans, systematic debugging, TDD, review, and verified delivery. They do not add 15 executable media tools or imply installed models.

## Architecture

```text
User task
  -> KOSIF master boot + environment probe + capability routing
  -> superpowers_unified.py plan "<exact task>"
  -> load selected upstream v7 workflow SKILL.md
  -> KOSIF tool discovery + prerequisites check
  -> execute task with real tooling
  -> tests, output inspection, honest status
```

Source folder:
`.claude/skills/kosif-superpowers/vendor/obra-superpowers-v7/skills/`

Router and installer:
`.claude/skills/kosif-superpowers/scripts/superpowers_unified.py`

## Commands, from repository root

```bash
python .claude/skills/kosif-superpowers/scripts/superpowers_unified.py doctor
python .claude/skills/kosif-superpowers/scripts/superpowers_unified.py plan "Build a video editor that downloads licensed footage"
python .claude/skills/kosif-superpowers/scripts/superpowers_unified.py list
python -m unittest discover -s tests -p "test_superpowers_unified.py" -v
```

**Portable Claude.ai packaging note:** Claude single-skill upload expects exactly one `SKILL.md`; its `.skill` archive therefore excludes the embedded third-party `vendor/` directory. The **full 16-skill unified suite is included in this GitHub repository** and installed through the installer below for Claude Code. For Claude.ai, import KOSIF's portable `.skill` and install the additional original process skills separately if your account supports multi-skill uploads. Do not claim the `.skill` file alone includes all 15 original process skills.

**Opt-in user-wide installation (backs up any existing CLAUDE.md, preserves unrelated skills):**

```bash
python .claude/skills/kosif-superpowers/scripts/superpowers_unified.py install
```

Installer copies KOSIF's master skill and all 15 original process skills to `~/.claude/skills`, and appends one marked policy section to `~/.claude/CLAUDE.md`. It skips colliding existing skill directories by default rather than overwriting them. `install --force` is available when explicitly approved and creates backups before replacing collisions.

**Rollback:** remove only the 16 directories that this installer created and the block between `KOSIF_SUPERPOWERS_ULTIMATE_START/END` in `~/.claude/CLAUDE.md`. For an existing file modified by installation, restore the matching copy from `~/.claude/backups/kosif-ultimate-*/CLAUDE.md`. Do not remove unrelated skills.

## Operating rules

- Preserve KOSIF capability counts, badges, vendor skill content and source attribution.
- Never make a claim of execution based solely on a skill definition.
- No automatically billable API usage, unapproved downloads requiring terms bypass, system-wide installs, publication or credential exposure.
- Do not run reverse-engineering workflows on ordinary edit tasks merely because reference matching was requested.
- The selected process skill governs **how** to work; KOSIF determines **which tools** are available in this specific session.
- The upstream may update later; upgrade only after deliberate diff review and tests. This snapshot is pinned to v7.0.0.
