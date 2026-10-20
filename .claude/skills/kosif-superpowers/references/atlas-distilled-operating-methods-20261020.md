# KOSIF Superpowers — Distilled Atlas Methods v2 (20 Oct 2026)

**Canonical skill:** `.claude/skills/kosif-superpowers/SKILL.md`, branch `main`. Continue using the existing KOSIF-native 4,751-power index first. This document adds **source-backed method recipes**, not new installed executors or 14,793 live skills. Do not import unreviewed third-party executable scripts into the skill.

## Evidence / limits

- Atlas snapshot: `kosif199022-jpg/kosif-atlas@99bb108d`.
- Index: 14,793 skill records including 85 copyleft reference-only records; 12,287 distinct normalized skill names; 1,427 names reused across 3,933 records, so naive wholesale copying duplicates names.
- Static source sample: **395 distinct `SKILL.md` files** (read only); 258 method candidates not flagged by the sampled heuristic gate; 137 require manual review. Source warning labels (not necessarily vulnerabilities): credential references 19, prompt override text 7, destructive shell 3, one-line install 6, protection-disable text 1, data-upload instruction 2, encoded/remote command text 2. Warning categories can overlap.
- Source identities, licenses as *claimed by Atlas*, paths and SHA-256 digests are in `data/atlas-method-provenance-20261020.json`. 15 named method patterns have first-hand text inspection receipts there.
- No third-party method was executed; source inspection does not establish correctness, code security, license authenticity, or compatibility with the user's installed programs.
- REA 6.7.0 and Ghidra 12.1.4 passed Ghidra-scoped doctor on Windows. Atlas at this commit had no tracked `.exe/.dll/.so/.dylib/.wasm/.jar/.class` files. No Ghidra binary analysis was performed **on Atlas** because there was no applicable native artifact. REA MCP was aligned with Claude Code locally but not directly exposed in this chat.

## Imported guidance, not code

The following is an original synthesis of methods from selected source files. Refer to the machine-readable manifest for exact evidence; read the specific source before any further transfer. All examples are general practices to be adapted to the current authorized execution environment.

### 1. Root-cause proof chain
**Trigger:** operational bug, QA incident, inventory discrepancy with a causal question. Based on Atlas `5why-root-cause` (#12659, declared MIT). Define the measured symptom; investigate one causal path at a time; distinguish cause of occurrence from **why the control failed to detect it**; check each link against actual evidence; attempt a reversal or elimination test; name a prevent/detect regression. Do not stop at “human error.”

### 2. Premortem before major changes
**Trigger:** risky architectural merge or rollout. Based on `pre-mortem` (#7548, MIT). State the intended success condition, plausible failure stories, leading signals and abort/reversal condition. Assign a simple verification owner and deadline only when the workflow actually has one.

### 3. Agent safety layered gates
**Trigger:** adding agents, MCP tools, remote execution or permissions. Based on `agent-runtime-guardrails` (#13086, MIT). Validate inbound schema and untrusted-source provenance; freeze tool allowlist and task goal; require approvals for irreversible actions; validate output and secrets; enforce bounded steps/costs; record observability and stop switch. A tool “available” flag is not a successful run.

### 4. Tool and data trust map
**Trigger:** agent security/threat model. Based on `agentic-threat-model` (#13122, MIT). Map each identity, permission, external instruction surface and write destination, then assess goal hijacking, tool misuse, escalation, unsafe code, poisoned memory, inter-agent messages, and failure cascades. Keep an explicit risk register, mitigation and test. Do not import the source's authority claims uncritically.

### 5. Binary evidence pathway
**Trigger:** authorized shipped native artifact that source code cannot explain. Based on `binary-analysis-patterns` (#14279, MIT). Capture exact artifact identity/hash, target platform, disassembly strings, call graph/control-flow evidence, data-structure inference and uncertainty before claiming behavior. Use actual exposed REA/Ghidra runner only if there is a binary and authorization. Never claim that Markdown skills were decompiled or remote server code recovered.

### 6. Cash forecast, 13-week horizon
**Trigger:** business treasury planning. Based on `cashflow-13week` (#14370, MIT). Derive week-by-week: opening balance + probabilistic receivables − dated payables − payroll/statutory outflows; model customer delay and variability; highlight the week and causes of cash shortfall; verify each successive opening equals prior closing. **Do not copy source's USD default thresholds into a SAR entity**; set buffer and materiality with the user/records. This is a method, not access to XBert MCP or private balances.

### 7. Tax reconciliation by ledger evidence
**Trigger:** match return to GL and VAT/tax accounts. Based on `tax-reconciliation` (#14396, MIT). Separate return inputs, GL control account, exempt or special lines, reversals, adjustments, dates and jurisdiction-specific rules; produce a signed reconciliation and unresolved exception list. For Saudi VAT use actual ZATCA requirements, not foreign defaults.

### 8. Renderable React video compositions
**Trigger:** Remotion project with authorized runtime. Based on `remotion` (#757, MIT). Define composition, dimensions, timing, input assets and text direction; render a short representative preview; probe output FPS/audio/duration and inspect frames before promising final MP4. A methodology in Atlas does not mean Remotion is installed.

### 9. Media transcode QA
**Trigger:** FFmpeg audio/video conversion. Based on `ffmpeg` (#754, MIT). Distinguish source streams, codec/containers, frame rate, pixel format, audio stream and delivery settings; use real `ffprobe` or equivalent output and decode test after encoding; preserve user-provided source and lawful rights. No output file → no export success claim.

### 10. Consistent UI constraints
**Trigger:** application design/spacing/refactor. Based on `design-constraints` (#205, MIT). Respect existing design tokens first; otherwise enforce a small spacing system, coherent nested radii, limited typography variation, RTL/mobile responsiveness and screenshot-based QA. Run over representative screens and real breakpoints, not aesthetics alone.

### 11. Claims-to-citations verification
**Trigger:** research and claim audit. Based on `ai-citation-verification` (#715, MIT). Extract claims; connect each to direct passage, date, population, unit, and original source when possible; label supported/partial/contradicted/unavailable; correct wording without fabricating citations.

### 12. UI/browser functional tests
**Trigger:** browser/front-end change. Based on `frontend-testing-debugging` (#10313, MIT). Define expected user path and selectors, exercise critical interactions, check mobile/desktop, RTL, console/runtime errors and data isolation, then show actual pass/fail outcomes. A screenshot alone doesn't prove the workflow works.

### 13. Redaction and provenance
**Trigger:** sanitized documents. Based on `redaction-and-provenance` (#2838, MIT). Select a technique which removes source text as required instead of drawing a black box; validate inaccessible underlying sensitive content, preserve a hash/report for the sanitized derivative, separate originals from outputs. Real PDF rasterization may sacrifice searchability.

### 14. Report readiness gate (specialized)
**Trigger only:** the particular **XBert IAS** workflow, not generic IFRS `IAS 16` or Saudi accounting standards. Based on `ias-prep` (#14383, MIT). Block reporting until mandatory source records and period/label consistency pass; never infer a specific tax standard from the acronym.

### 15. Human-language fidelity checks
**Trigger:** rewrite for natural Arabic/English style. Based on `anti-ai-writing-patterns` (#182, MIT). Avoid rote formulaic wording, but preserve all numbers, legal obligations and intent; do not introduce fabricated biographical details or change the requested dialect.

## How Superpowers invokes this bridge

1. Native `scripts/capability_atlas.py` or `scripts/capability_runtime_router.py` selects a KOSIF-native capability.
2. If a substantive gap exists and the task mentions a relevant method, run `scripts/atlas_task_method_router.py --task "<user request>"` (reads the local source-provenance manifest). Maximum two additional method patterns per request.
3. Read the specific source-backed recipe in this document and enforce its acceptance criteria. The selection response explicitly says *guidance only*.
4. For a new method outside the 15 curated entries, query `atlas_deep_fusion.py` and inspect a narrow source excerpt using `atlas_bulk_source_audit.py`; human-review code, permission, license and provenance before any actual integration.
5. Never execute third-party content or mark a capability as "installed", "proven" or "working" from a text match. For device side effects follow canonical authorized connector execution and real postcondition evidence.

## Repeatable analysis

From the existing checked-out project, with `$atlas` pointing at the local Atlas root:

~~~powershell
$skill = '.claude/skills/kosif-superpowers'
python "$skill/scripts/atlas_bulk_source_audit.py" plan --index "$atlas/index.json" --copyleft "$atlas/index-copyleft.json" --output sample-plan.json
# Review and selectively check out only listed skill directories, no automatic execution.
python "$skill/scripts/atlas_bulk_source_audit.py" audit --index "$atlas/index.json" --copyleft "$atlas/index-copyleft.json" --root "$atlas" --plan-file sample-plan.json --output source-review.json
python "$skill/scripts/atlas_review_summary.py" --review source-review.json --output method-provenance.json
python "$skill/scripts/atlas_task_method_router.py" --task "حلل السبب الجذري لأخطاء الجرد"
python -m unittest discover -s "$skill/scripts" -p 'test_atlas_*py' -v
~~~

The source-review plan uses a deterministically selected **sample**; other 14,398 `SKILL.md` files were not read in this round. Coverage shall only be increased with explicit bounded iterations, resource limits, and actual read receipts.
