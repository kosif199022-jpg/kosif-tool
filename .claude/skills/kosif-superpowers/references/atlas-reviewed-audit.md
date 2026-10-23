# KOSIF Atlas source audit - 2026-10-20

Scope is a prioritized sample, not all 14,793 indexed skills. Third-party instructions remain untrusted data.

## Evidence counts

- Actual SKILL.md bodies read: 1000.
- Selected source code files read: 862.
- Skills with static risk-review indicators: 222.
- Indicator categories (counting skills): {'secret_collection': 41, 'prompt_instruction_override': 2, 'shell_mutation': 149, 'destructive_shell': 62, 'remote_script_execution': 11}.
- REA successful code-group analyses: 7; parsed JS files: 14; AST nodes: 11299; structural findings: 159.
Source presence and code parsing are not runtime feature verification.

## Tool selection

REA inspects supported JavaScript/TypeScript; Ghidra handles native binary inputs.
No native .exe, .dll, .so or .wasm artifact was declared in the full Atlas index file inventories.
The prior REA plus Ghidra end-to-end proof on an authorized Windows executable remains valid, but cannot substitute for analysis of external skill source.

## Extractable concepts - CANDIDATES ONLY

- Critical thinking, scientific evidence and uncertainty checking.
- Motion and video rendering using Remotion plus already verified KOSIF Blender Cycles/FFmpeg pipeline.
- Permission-gated browser automation and app validation.
- Data safety checks, financial audit logging and versioned evidence receipts.
- Repeatable workflow orchestration and accountable verification.

## Manually reviewed warning examples

- 1943 superloopy-research: prompt-injection phrase is quoted as an example to reject, not an attack instruction.
- 5838 grammarly-document-evaluator: mentions secrets while documenting environment-only OAuth handling; not a confirmed leak.
- 7735 evaluate-context-engineering: regex matches sensitive actions to protect against them; not an executed harmful command.
- 10459 temporal-cloud-setup: contains real cloud setup and secret-handling workflows; requires separate authorization and code audit.

## Activation gates

1. Do not run external skill code by default.
2. Require matching license, dependencies, permissions and per-task safety review.
3. Treat static detection as a review signal, not proof of malicious behavior.
4. Copyleft source stays reference-only until redistribution duties are reviewed.
5. Require real functional tests before marking a skill runnable.

Metadata-only evidence in data/atlas-reviewed/manifest.json.
Full third-party source and REA JSON evidence remain on the authorized computer in a private location.
