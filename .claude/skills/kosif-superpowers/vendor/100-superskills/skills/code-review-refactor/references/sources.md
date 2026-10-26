# مصادر «مراجعة الكود وإعادة الهيكلة» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## code-review-and-quality (1120-ambient-library)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coachlou/ambient-library/tree/2b66a4a4e764bd5884e652e8759a80cacab244fe
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2649-software-dev-factory/app/.agents/skills/factory-bootstrap/upstream/addy/skills/code-review-and-quality
- الوصف: Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch.

```markdown
# Code Review and Quality

## Overview

Multi-dimensional code review with quality gates. Every change gets reviewed before merge — no exceptions. Review covers five axes: correctness, readability, architecture, security, and performance.

**The approval standard:** Approve a change when it definitely improves overall code health, even if it isn't perfect. Perfect code doesn't exist — the goal is continuous improvement. Don't block a change because it isn't exactly how you would have written it. If it improves the codebase and follows the project's conventions, approve it.

## When to Use

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code you need to evaluate
- When refactoring existing code
- After any bug fix (review both the fix and the regression test)

## The Five-Axis Review

Every review evaluates code across these dimensions:

### 1. Correctness

Does the code do what it claims to do?

- Does it match the spec or task requirements?
- Are edge cases handled (null, empty, boundary values)?
- Are error paths handled (not just the happy path)?
- Does it pass all tests? Are the tests actually testing the right things?
- Are there off-by-one errors, race conditions, or state inconsistencies?

### 2. Readability & Simplicity

Can another engineer (or agent) understand this code without the author explaining it?

- Are names descriptive and consistent with project conventions? (No `temp`, `data`, `result` without context)
- Is the control flow straightforward (avoid nested ternaries, deep callbacks)?
- Is the code organized logically (related code grouped, clear module boundaries)?
- Are there any "clever" tricks that should be simplified?
- **Could this be done in fewer lines?** (1000 lines where 100 suffice is a failure)
- **Are abstractions earning their complexity?** (Don't generalize until the third use case)
- Would comments help clarify non-obvious intent? (But don't comment obvious code.)
- Are there dead code artifacts: no-op variables (`_unused`), backwards-compat shims, or `// removed` comments?
- **Is a new conditional bolted onto an unrelated flow?** That's a design smell, not a nit — push the logic into its own helper, state, or policy instead of tangling an existing path.
- **Do repeated conditionals on the same shape appear?** They signal a missing model or dispatcher. A "temporary" branch is usually permanent debt.

### 3. Architecture

Does the change fit the system's design?

- Does it follow existing patterns or introduce a new one? If new, is it justified?
- Does it maintain clean module boundaries?
- Is there code duplication that should be shared?
- Are dependencies flowing in the right direction (no circular dependencies)?
```

## code-review-and-quality (1120-ambient-library)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coachlou/ambient-library/tree/2b66a4a4e764bd5884e652e8759a80cacab244fe
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2650-code-review-and-quality
- الوصف: Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch.

```markdown
# Code Review and Quality

## Overview

Multi-dimensional code review with quality gates. Every change gets reviewed before merge — no exceptions. Review covers five axes: correctness, readability, architecture, security, and performance.

**The approval standard:** Approve a change when it definitely improves overall code health, even if it isn't perfect. Perfect code doesn't exist — the goal is continuous improvement. Don't block a change because it isn't exactly how you would have written it. If it improves the codebase and follows the project's conventions, approve it.

## When to Use

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code you need to evaluate
- When refactoring existing code
- After any bug fix (review both the fix and the regression test)

## The Five-Axis Review

Every review evaluates code across these dimensions:

### 1. Correctness

Does the code do what it claims to do?

- Does it match the spec or task requirements?
- Are edge cases handled (null, empty, boundary values)?
- Are error paths handled (not just the happy path)?
- Does it pass all tests? Are the tests actually testing the right things?
- Are there off-by-one errors, race conditions, or state inconsistencies?

### 2. Readability & Simplicity

Can another engineer (or agent) understand this code without the author explaining it?

- Are names descriptive and consistent with project conventions? (No `temp`, `data`, `result` without context)
- Is the control flow straightforward (avoid nested ternaries, deep callbacks)?
- Is the code organized logically (related code grouped, clear module boundaries)?
- Are there any "clever" tricks that should be simplified?
- **Could this be done in fewer lines?** (1000 lines where 100 suffice is a failure)
- **Are abstractions earning their complexity?** (Don't generalize until the third use case)
- Would comments help clarify non-obvious intent? (But don't comment obvious code.)
- Are there dead code artifacts: no-op variables (`_unused`), backwards-compat shims, or `// removed` comments?
- **Is a new conditional bolted onto an unrelated flow?** That's a design smell, not a nit — push the logic into its own helper, state, or policy instead of tangling an existing path.
- **Do repeated conditionals on the same shape appear?** They signal a missing model or dispatcher. A "temporary" branch is usually permanent debt.

### 3. Architecture

Does the change fit the system's design?

- Does it follow existing patterns or introduce a new one? If new, is it justified?
- Does it maintain clean module boundaries?
- Is there code duplication that should be shared?
- Are dependencies flowing in the right direction (no circular dependencies)?
```

## code-review-and-quality (1176-software-dev-factory)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coachlou/ambient-library/tree/2b66a4a4e764bd5884e652e8759a80cacab244fe/library/software-dev-factory
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1176-software-dev-factory/2758-software-dev-factory/app/.agents/skills/factory-bootstrap/upstream/addy/skills/code-review-and-quality
- الوصف: Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch.

```markdown
# Code Review and Quality

## Overview

Multi-dimensional code review with quality gates. Every change gets reviewed before merge — no exceptions. Review covers five axes: correctness, readability, architecture, security, and performance.

**The approval standard:** Approve a change when it definitely improves overall code health, even if it isn't perfect. Perfect code doesn't exist — the goal is continuous improvement. Don't block a change because it isn't exactly how you would have written it. If it improves the codebase and follows the project's conventions, approve it.

## When to Use

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code you need to evaluate
- When refactoring existing code
- After any bug fix (review both the fix and the regression test)

## The Five-Axis Review

Every review evaluates code across these dimensions:

### 1. Correctness

Does the code do what it claims to do?

- Does it match the spec or task requirements?
- Are edge cases handled (null, empty, boundary values)?
- Are error paths handled (not just the happy path)?
- Does it pass all tests? Are the tests actually testing the right things?
- Are there off-by-one errors, race conditions, or state inconsistencies?

### 2. Readability & Simplicity

Can another engineer (or agent) understand this code without the author explaining it?

- Are names descriptive and consistent with project conventions? (No `temp`, `data`, `result` without context)
- Is the control flow straightforward (avoid nested ternaries, deep callbacks)?
- Is the code organized logically (related code grouped, clear module boundaries)?
- Are there any "clever" tricks that should be simplified?
- **Could this be done in fewer lines?** (1000 lines where 100 suffice is a failure)
- **Are abstractions earning their complexity?** (Don't generalize until the third use case)
- Would comments help clarify non-obvious intent? (But don't comment obvious code.)
- Are there dead code artifacts: no-op variables (`_unused`), backwards-compat shims, or `// removed` comments?
- **Is a new conditional bolted onto an unrelated flow?** That's a design smell, not a nit — push the logic into its own helper, state, or policy instead of tangling an existing path.
- **Do repeated conditionals on the same shape appear?** They signal a missing model or dispatcher. A "temporary" branch is usually permanent debt.

### 3. Architecture

Does the change fit the system's design?

- Does it follow existing patterns or introduce a new one? If new, is it justified?
- Does it maintain clean module boundaries?
- Is there code duplication that should be shared?
- Are dependencies flowing in the right direction (no circular dependencies)?
```

## code-review-and-quality (1176-software-dev-factory)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coachlou/ambient-library/tree/2b66a4a4e764bd5884e652e8759a80cacab244fe/library/software-dev-factory
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1176-software-dev-factory/2759-code-review-and-quality
- الوصف: Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch.

```markdown
# Code Review and Quality

## Overview

Multi-dimensional code review with quality gates. Every change gets reviewed before merge — no exceptions. Review covers five axes: correctness, readability, architecture, security, and performance.

**The approval standard:** Approve a change when it definitely improves overall code health, even if it isn't perfect. Perfect code doesn't exist — the goal is continuous improvement. Don't block a change because it isn't exactly how you would have written it. If it improves the codebase and follows the project's conventions, approve it.

## When to Use

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code you need to evaluate
- When refactoring existing code
- After any bug fix (review both the fix and the regression test)

## The Five-Axis Review

Every review evaluates code across these dimensions:

### 1. Correctness

Does the code do what it claims to do?

- Does it match the spec or task requirements?
- Are edge cases handled (null, empty, boundary values)?
- Are error paths handled (not just the happy path)?
- Does it pass all tests? Are the tests actually testing the right things?
- Are there off-by-one errors, race conditions, or state inconsistencies?

### 2. Readability & Simplicity

Can another engineer (or agent) understand this code without the author explaining it?

- Are names descriptive and consistent with project conventions? (No `temp`, `data`, `result` without context)
- Is the control flow straightforward (avoid nested ternaries, deep callbacks)?
- Is the code organized logically (related code grouped, clear module boundaries)?
- Are there any "clever" tricks that should be simplified?
- **Could this be done in fewer lines?** (1000 lines where 100 suffice is a failure)
- **Are abstractions earning their complexity?** (Don't generalize until the third use case)
- Would comments help clarify non-obvious intent? (But don't comment obvious code.)
- Are there dead code artifacts: no-op variables (`_unused`), backwards-compat shims, or `// removed` comments?
- **Is a new conditional bolted onto an unrelated flow?** That's a design smell, not a nit — push the logic into its own helper, state, or policy instead of tangling an existing path.
- **Do repeated conditionals on the same shape appear?** They signal a missing model or dispatcher. A "temporary" branch is usually permanent debt.

### 3. Architecture

Does the change fit the system's design?

- Does it follow existing patterns or introduce a new one? If new, is it justified?
- Does it maintain clean module boundaries?
- Is there code duplication that should be shared?
- Are dependencies flowing in the right direction (no circular dependencies)?
```

## code-review (239-code-review)

- الترخيص: **MIT**  ·  الأصل: https://github.com/allada-homelab/agent-harness-marketplace/tree/074044f115d3d94adf0986b4d113d31f2d9afc88/modules/code-review
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/239-code-review/776-code-review
- الوصف: Review a GitHub pull request and post one comment with only the high-confidence issues. A small or docs/generated-only change (under 50 changed lines, or every changed path documentation or generated) gets one combined reviewer covering all five lenses with inline scoring; any other change gets five parallel lens reviewers plus one batch scorer that rates every candidate 0-100 and drops anything u

```markdown
# Code review

Provide a code review for the pull request. Review target: $ARGUMENTS — when
none is given, the pull request of the current branch (`gh pr view`).

Everything here is read-only: use `gh` (`gh pr view`, `gh pr diff`, `gh pr
list`, `gh search`, `gh issue`, `gh api`) and the local checkout to read, and
`gh pr comment` once at the end to write. Never edit files, never run a build,
typecheck or test suite — CI runs those separately and they are not part of
this review — and never use web fetching where `gh` will do.

## Agents

Three agents ship beside this skill; name them by type and dispatch them with
whatever this harness has:

| Type | Job |
|---|---|
| `code-review:triage` | eligibility check · size · guideline-file discovery · change summary |
| `code-review:reviewer` | one review lens per dispatch, or (small tier) all five lenses combined with inline scoring |
| `code-review:scorer` | one batch of confidence scores — every candidate issue of this review, in a single dispatch |

- **Claude Code**: the Agent tool with `subagent_type` set to the type above.
- **pi and dsh**: the `delegate_agent` tool with `agent_type` set to the type
  above. On pi the tool is inactive until this skill is invoked; if it is
  missing, run `/agents` once.
- **No delegation tool at all**: do each step yourself, sequentially, using the
  agent's body as your brief. The definitions are in `./../../agents/` beside
  this skill.

Every child sees none of this conversation: give it the pull request reference,
its duty or lens, and every input the step names. Issue independent calls
together in one message so they run in parallel.

## Steps

Outline these steps as a task list first, then follow them precisely.

1. **Eligibility.** Dispatch `code-review:triage` with duty *eligibility*. Stop
   if it answers `SKIP` — the pull request is closed, a draft, needs no review
   (automated, or trivially and obviously fine), or already has a `### Code
   review` comment from an earlier run.
2. **Size, guideline files, summary.** Dispatch `code-review:triage` three
   times — duty *size*, duty *guideline files*, duty *summary* — together;
   none of the three depends on the others. Size returns `FILES`, `LINES` and
   `GENERATED_ONLY`; guideline files returns paths only (the root
   `CLAUDE.md` / `AGENTS.md` and any in the directories the pull request
   touches); summary returns a short description of the change.
3. **Pick a tier.** **small** when `LINES` from step 2 is under 50, or
   `GENERATED_ONLY` is `yes`; **normal** otherwise. Below 50 changed lines
   there is rarely more than one class of issue for five independent lenses
   to disagree about, and a docs- or lockfile-only diff has no logic for them
```

## clean-code-workflow (59-clean-code)

- الترخيص: **MIT**  ·  الأصل: https://github.com/acaprino/daodan/tree/39443d215d28fcbc32d651895b3cc45c64f24b6f/exports/codex/plugins/clean-code
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/59-clean-code/92-clean-code-workflow
- الوصف: Readability-only rewrite of existing source. TRIGGER WHEN: the user asks to clean up code, improve naming, remove AI-generated boilerplate, simplify structure, or make code more maintainable without changing behavior. DO NOT TRIGGER WHEN: the target is prose or text (use /text-humanizer:humanize-text), or deep architectural refactoring (use /python-development:python-refactor).

```markdown
> Arguments: `<file or directory> [--dry-run] [--strict] [--yes] [--force]`. Wherever `<arguments>` appears below, substitute the text the user typed after the skill name.


# Clean Code

Use the `clean-code-agent` to rewrite source code for readability without changing behavior.

## Rules

1. **Validate before and after.** Establish a baseline with type checker + tests + linter, then verify no regressions.
2. **If `--dry-run`, preview only.** Show proposed changes without modifying files.
3. **Revert on failure.** If any validation fails after a change, revert with `git restore <file>` immediately.
4. **Ask for confirmation** at Steps 2 and 3, unless `--yes` flag is provided.
5. **Block without validation tools.** If no tests AND no type checker exist, require `--force` to proceed.

## Step 1: Identify Target

From `<arguments>`, determine files to clean:
- If a file path: clean that file
- If a directory: clean all source files in it
- Filter out test files (unless they reference renamed symbols)

List the files to be cleaned and their language.

## Step 2: Establish Validation Baseline

Detect available validation tools by inspecting project files:

| Tool | How to detect | Command |
|------|--------------|---------|
| **Type checker** | `tsconfig.json` | `tsc --noEmit` |
| | `mypy.ini`, `pyrightconfig.json`, or mypy/pyright in `pyproject.toml` | `mypy .` or `pyright` |
| | `Cargo.toml` | `cargo check` |
| | `go.mod` | `go vet ./...` |
| **Test runner** | `package.json` | `npm test` |
| | `pyproject.toml` or `setup.py` | `pytest` |
| | `Cargo.toml` | `cargo test` |
| | `go.mod` | `go test ./...` |
| | `Makefile` with test target | `make test` |
| **Linter** | `ruff.toml` or ruff config in `pyproject.toml` | `ruff check` |
| | `.eslintrc*` or `eslint.config.*` | `eslint` |
| | `Cargo.toml` | `cargo clippy` |

Run all detected tools and capture both stdout and stderr. Record the baseline.

**Hard gate:** if NO tests AND NO type checker are found, stop and tell the user:

```
No tests or type checker found. Cannot validate that changes are safe.

1. Cancel: set up tests or type checking first (recommended)
2. Proceed with --force: I'll be careful but regressions may go undetected
```

`--yes` alone does NOT bypass this gate. Only `--force` does.

## Step 3: Preview Changes (always for --dry-run, ask otherwise)

If `--dry-run` flag is set, or if the target is a directory with >3 files, show a preview first.
If `--yes` flag is provided, apply all changes after showing the preview without asking.

For each file, analyze and propose:
- Variable/function renames (vague -> domain-meaningful)
- Boilerplate comments to remove (paraphrase comments, empty docstrings)
- Why-comments to add (non-obvious business logic)
```
