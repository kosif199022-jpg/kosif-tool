# مصادر «مدرّب اللغات» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## polyglot-language-coach (1168-polyglot-language-coach)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coachlou/ambient-library/tree/2b66a4a4e764bd5884e652e8759a80cacab244fe/library/polyglot-language-coach
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1168-polyglot-language-coach/2750-polyglot-language-coach
- الوصف: Gently coaches when the user writes in a non-English language mid-conversation — corrects, teaches, logs, returns to task; applies whenever the user code-switches as practice.

```markdown
Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/polyglot-language-coach/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
```

## polyglot-language-coach (1120-ambient-library)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coachlou/ambient-library/tree/2b66a4a4e764bd5884e652e8759a80cacab244fe
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1120-ambient-library/2641-polyglot-language-coach
- الوصف: Gently coaches when the user writes in a non-English language mid-conversation — corrects, teaches, logs, returns to task; applies whenever the user code-switches as practice.

```markdown
Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/polyglot-language-coach/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
```

## akbun-learning-english (1097-akbun-learning)

- الترخيص: **MIT**  ·  الأصل: https://github.com/choisungwook/akbun-aitools/tree/b592650776c4ed1723087911010466d0b537fc6b/plugins/akbun-learning
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1097-akbun-learning/2471-akbun-learning-english
- الوصف: 

```markdown
# Learning English - Pronunciation Guide for Korean Learners

The learner is Korean with 1-3 years of English study experience (intermediate level). Respond primarily in Korean for explanations, using English only for target text and linguistic terms.

## Input Processing

1. Accept English words, sentences, or paragraphs from the user.
2. Auto-correct any typos or spelling errors in the input before processing. Silently fix them and proceed.
3. Process each sentence or logical phrase as a separate block.

## Output Format

CRITICAL formatting rules:

- Use a markdown table for each sentence breakdown to align labels and values cleanly.
- Table format: empty header row `| | |`, right-aligned labels `|---:|:---|`.
- Use markdown bold (`text`) for emphasis so the user sees clean rendered bold text.
- Organize output by sentence or phrase, not as a single wall of text.
- For multi-line values (발음 팁), use empty first-column cells for continuation rows.

### Output Order

1. Provide detailed table breakdowns, grouped by paragraph (matching the user's input paragraph breaks). Add a paragraph separator (e.g., `---` or bold paragraph label) between groups. Number sentences continuously across paragraphs.

### Required Sections (per-sentence table)

끊어 읽기: Show the original English with `/` at natural pause/breath points. Group by meaning units (subject / verb phrase / object or complement).

강세: Write Korean pronunciation with bold on stressed syllables. Use `/` at the same pause points as 끊어 읽기.

Rules:

- Bold ONLY stressed syllables. Unstressed syllables are plain text.
- Content words (nouns, main verbs, adjectives, adverbs, negative words) carry stress. Function words (articles, prepositions, auxiliary verbs, pronouns) do not.
- For multi-syllable words, bold only the stressed syllable of that word.

직독직해: Translate chunk by chunk in English reading order, Korean only. Use `/` to separate chunks. Show only the Korean translation in reading order so the learner builds English thinking patterns.

발음 팁: Actionable tips with `•` prefix, one per table row (empty label cell for continuation). Focus on:

- Linking and connected speech (연음)
- Reductions and contractions (축약)
- Sounds difficult for Korean speakers (see Korean Speaker Challenges below)

## Korean Speaker Challenges

Apply these corrections proactively whenever relevant sounds appear:

Consonants

- `f` / `v`: Korean has no `f` or `v`. Coach lip-teeth contact (아랫입술을 윗니에 가볍게 대기). `f` is NOT `ㅍ`; `v` is NOT `ㅂ`.
- `th` (voiced/unvoiced): Tongue between teeth. `θ` (think) is NOT `ㅆ`; `ð` (this) is NOT `ㄷ`.
- `l` vs `r`: `l` = tongue tip touches roof of mouth; `r` = tongue curls back without touching. Korean `ㄹ` is between the two.
- `z`: Voiced `s`. NOT `ㅈ`. Vibrate vocal cords while making `s`.
```

## agent-learning-coach (2-agent-workflow-system)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/1139030773-cmd/agent-workflow-system
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2-agent-workflow-system/4-agent-learning-coach
- الوصف: 中文学习教练技能。用于学习编程、英语、设计、产品、AI、数学或任何技能时，先诊断水平，再用讲解、练习、反馈、复习的循环推进。触发语包括"进入学习模式""我想学""带我练""帮我制定学习计划""像教练一样教我"。

```markdown
# Codex 学习教练

身份：**执行者**。让用户通过练习真正掌握技能，不只讲不练。

> 遵守统一行为规范（职能隔离 / 动作校验 / 状态机 / 五级纠错 / 回滚 / 证据链）。

## 📍 阶段位置

```
[●入口] → [●引导] → [●策划] → [◉执行] → [○审计] → [○收尾]
 当前角色: 执行者·教学 | 上一站: 策划 | 下一站: 审计
```

> 当前阶段自动写入 `STATE_SNAPSHOT.md` 的 `current_phase` 字段。

## 硬边界

| 允许 | 禁止 |
|------|------|
| 诊断水平、制定学习计划 | **偏离到项目管理** |
| 讲解、出练习、批改反馈 | **变成纯讲不练** |
| 记录薄弱点和复习安排 | **跳过自检** |
| 建议 agent-drift-auditor 检查方向 | **静默改变学习目标** |

## 工作流程

1. 诊断水平（≤3 题）
2. 明确学习目标（范围检查：在边界内？）
3. 拆成可练习的小技能
4. 每次只教一个小点
5. 给例子 → 练习 → 批改反馈
6. 记录薄弱点 → 安排复习

## 每轮输出

- 今天学什么 / 为什么学
- 简短讲解 / 例子 / 练习 / 判断标准
- 自检 + 证据链（动作序号 + 校验结果）

## 自检（对齐行为规范）

- [ ] 教学在范围内？未偏离到项目/功能开发？
- [ ] 用户能否独立完成？/ 需降难度？/ 需复习？
- [ ] 若方向跑偏 → 建议 `agent-drift-auditor`
- [ ] 交互预算：每次只给 1 个练习或问题？

## 偏离处理

| 级别 | 动作 |
|------|------|
| 第 1 级 | 自查纠正，记录证据链 |
| 第 2 级 | 审计者轻量诊断，输出纠正建议 |
| 第 3 级 | 深度检查 + 回滚到上一合法状态，暂停前进 |
| 第 4 级 | 冻结任务队列 + 完整偏离报告，标记人工介入 |
| 第 5 级 | 强制人工介入，系统锁定 |
| ≥5 级 | 等待人工解锁，停止所有自动动作 |

## 禁止事项

- 不一次塞太多概念 / 不只讲不练
- 不默认用户懂专业术语 / 不偏离到项目管理
```

## 9454-curate-language (2435-domain-driven-design)

- الترخيص: **MIT**  ·  الأصل: https://github.com/melodic-software/claude-code-plugins/tree/c8fa858c9059d3183cfc08f646e4a97f44b33973/plugins/domain-driven-design
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2435-domain-driven-design/9454-curate-language
- الوصف: Actively maintain a consuming project's ubiquitous-language glossary as domain understanding changes: resolve ambiguous or overloaded terms, choose canonical language, record rejected synonyms, sharpen what-it-IS definitions, and route terms to an already-known bounded context. Use when: 'update the domain glossary', 'define this domain term', 'standardize this vocabulary', 'these names conflict',

```markdown
## Variables

Request: `$ARGUMENTS`

## Purpose

Maintain the consuming project's active, committed vocabulary record. The glossary is not a static
dictionary and not the domain model by itself: it records language the team has actually resolved so
the same model language can be used consistently in conversation, documentation, tests, and code.

This skill owns **changing** that record. Merely reading the nearest glossary so another skill uses
the right words is a one-line habit and does not require this workflow.

Entry discipline, the convention-resolution ladder, and the multi-context rules live in
[context/glossary-contract.md](context/glossary-contract.md). Read that file before resolving a
convention or writing an entry.

## Workflow

### 1. Establish what is resolved

Start from the conversation, `$ARGUMENTS`, existing glossary entries, and relevant project artifacts.
Identify the concrete language change:

- a new project-specific concept has a stable meaning
- one term is being used for two concepts
- several names compete for one concept
- an existing definition no longer matches the team's model
- the same spelling intentionally means different things in different known contexts

Exercise the candidate language in one or two domain scenarios. If the meaning, canonical term, or
context is still disputed, ask one focused question and do not write yet. Never manufacture consensus.
When the proposed meaning describes existing software behavior, inspect the relevant code and tests.
If they contradict the conversation, surface the mismatch and resolve which model is intended before
writing; do not silently treat either source as authoritative.

### 2. Resolve the consumer's convention

Gather the evidence the ladder in `context/glossary-contract.md` ranks: the consuming project's
`AGENTS.md`, `CLAUDE.md`, `.claude/rules`, and declared documentation conventions, then, from the
files and domain area in scope, walk toward the repository root looking for an existing
domain-vocabulary file or context map. Work the ladder in order and stop at the first rung that
resolves both format and location.

Preserve whatever the winning convention already fixes: filename, location, headings, ordering, and
entry syntax. Do not impose a fixed filename of your own. Re-read the target file immediately
before editing it. Another turn or agent may have changed it.

### 3. Route to a known language context

Use an existing context map or explicit project convention first. Otherwise infer the applicable
**already-known** context from the task, touched files, and accepted design/workshop artifacts. If two
contexts remain plausible, ask rather than putting the term in both.
```

## mcp-language-server-orphan-fd-exhaustion (3330-mcp-language-server-orphan-fd-exhaustion)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/mcp-language-server-orphan-fd-exhaustion
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3330-mcp-language-server-orphan-fd-exhaustion/13844-mcp-language-server-orphan-fd-exhaustion
- الوصف: Diagnose and clear a system-wide file-descriptor exhaustion on a macOS workstation caused by orphaned `mcp-language-server` (LSP-to-MCP bridge) processes leaking file descriptors until the kernel file table is full. The symptom masquerades as whatever tool happens to open a file next - "ENFILE: file table overflow" from a CLI, terraform failing, DNS lookups timing out - so it reads as that tool's 

```markdown
> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/mcp-language-server-orphan-fd-exhaustion/SKILL.md`).
> Updates go through the repo's worktree + PR workflow - open an issue,
> branch, PR.

# Orphaned mcp-language-server processes exhaust the macOS file table

## Problem

Mid-session, a CLI invocation (a Codex review run, in the observed case)
died with:

```
ENFILE: file table overflow
```

Nothing about the failing tool was wrong. `ENFILE` is errno 23 - the
**system-wide** kernel file table is full (unlike `EMFILE`, the per-process
limit, which `ulimit` governs). Once the table is nearly full, *every*
process that next opens a file, socket, or pipe fails: terraform, DNS
resolution, editors, shells. The error surfaces in whichever tool loses the
race first, so it masquerades as that tool's bug and gets debugged in the
wrong place.

The actual cause: `mcp-language-server` - the generic Go LSP-to-MCP bridge
(github.com/isaacphi/mcp-language-server) that agent sessions register
per-project to get LSP for languages their curated LSP set lacks - is
spawned per session, and sessions that end abruptly leave their bridge
running. The orphans reparent to PID 1 and keep accumulating open fds.
Twenty of them were alive on the observed machine, holding a quarter of a
million descriptors between them.

## Diagnosis (three commands)

1. **Is the file table actually full?**

   ```bash
   sysctl kern.num_files kern.maxfiles
   ```

   Observed at failure: `kern.num_files: 275146` / `kern.maxfiles: 276480`
   - 99.5% full. Anything above ~90% explains random `ENFILE`s.

2. **Who holds the descriptors?**

   ```bash
   lsof 2>/dev/null | awk '{print $1}' | sort | uniq -c | sort -rn | head
   ```

   Observed: `mcp-language-server` held **255,298** fds. (`lsof` over a
   full table is slow - minutes, not seconds. Let it run.)

3. **Are they orphans?**

   ```bash
   ps -axo pid,ppid,etime,command | grep -E 'mcp-language-server|terraform-ls' | grep -v grep
   ```

   PPID 1 means the parent (the agent session that spawned the bridge)
   exited without reaping it. Observed: 20 processes, all PPID 1.

Capture the three outputs to a file before killing anything - the evidence
is gone the moment the fix runs.

## Fix

```bash
pkill -9 -f mcp-language-server
pkill -9 -f terraform-ls
```

Both are disposable and respawn on demand the next time a session needs
them (`terraform-ls` is the language server the bridge commonly fronts, and
leaks alongside it). Preconditions worth a five-second check:

- No terraform apply/destroy in flight (killing `terraform-ls` is safe for
  state, but do not yank tooling mid-operation on principle).
- This does not touch editors' own state - IDE-embedded language servers
```
