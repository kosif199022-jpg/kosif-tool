# REA × KOSIF Superpowers — evidence-first software investigation

**Status:** optional local integration, not proof REA is installed or executing.

**Upstream attribution:** morluto/rea — https://github.com/morluto/rea (MIT for REA-authored code, Copyright (c) 2026 morluto). Third-party binaries, Hopper, Ghidra, IDA, JEB and their assets retain separate terms; see https://github.com/morluto/rea/blob/main/THIRD_PARTY_NOTICES.md. This integration contains original KOSIF glue code, not copies of REA or decompiled third-party sources.

## Added abilities: evidence-backed routes

The SKILL can now route legal, consent-based software inspection, instead of confusing it with ordinary code review or internet research. The REA adapter supports a non-executing readiness check, scoped investigation plans, and an explicitly authorized local static CLI run with a SHA-256 evidence receipt. It does not fetch or install packages, probe protected sites, execute arbitrary target binaries, defeat DRM or claim verified equivalence from pseudocode.

| Route | Subject | Actual availability |
|---|---|---|
| REA-JS | JavaScript and Electron bundles, modules, sourcemaps and IPC | bridge static allowlist |
| REA-DOTNET | .NET assembly identity and CIL | bridge static allowlist |
| REA-SQLITE | SQLite tables and indexes | bridge static allowlist |
| REA-GO | Go embedded compiler and module facts | bridge static allowlist |
| REA-RUST | Rust embedded crate metadata | bridge static allowlist |
| REA-NATIVE | Native ELF, PE and Mach-O instructions and xrefs | manual provider: Hopper, Ghidra or IDA |
| REA-APK | Android classes and manifest | manual provider: JADX and Java |
| REA-BROWSER | Authorized website structure, scripts and network observations | manual browser/CDP workflow |
| REA-WASM | WebAssembly WAT, imports and exports | manual tool: WABT |
| REA-FLUTTER | Flutter snapshot/build metadata | manual workflow |
| REA-FIRMWARE | Regions and extractable resources | manual Binwalk/Unblob workflow |
| REA-NETWORK | PCAP and protocol summaries | manual TShark/capinfos workflow |
| REA-DEVICE | Android device processes, logs and packages | manual adb workflow |
| REA-CAPTURES | Captured HAR/SAZ response traces | manual REA capture guide |
| REA-PROCESS | Controlled process behavior comparisons | explicit runtime consent |
| REA-APPLE | Apple bundle anatomy and plists | manual authorized bundle workflow |
| REA-CRASH | Saved Linux crash/core registers | manual offline forensics |
| REA-SIGNAL | Recorded logic signals and decoder annotations | manual sigrok-cli workflow |

The first five are only *command plans* until REA is installed, configured, authorized and actually runs. The others are documented possibilities requiring explicit tools. These routes do not increment the official power catalog count until independently evaluated and registered in data/powers.

## Sequence and examples

1. Require rights to inspect the target. Reject credential theft, restrictions bypasses and confidential data export.
2. Detect tools and environment: python3 $SKILL_DIR/scripts/probe_env.py followed by python3 $SKILL_DIR/scripts/rea_bridge.py doctor. REA's supported Node versions: 22.x from 22.19, 24.x from 24.11, or 26+.
3. Prepare without execution: python3 $SKILL_DIR/scripts/rea_bridge.py plan javascript /absolute/path/to/extracted-app
4. If REA missing, **ask** before running the official setup: npx rea-agents setup. Never auto-install as a side-effect of reading this skill.
5. For an authorized local static analysis only, intentionally run: python3 $SKILL_DIR/scripts/rea_bridge.py run javascript /absolute/path/to/extracted-app --authorized --output ./rea-evidence.json
6. Inspect the saved result file and source anchors. Confirm at least one observation via an independent test. The bridge always returns verified=false: executing the CLI alone cannot prove functionality.
7. Derive a clean original specification and implementation if asked to build a similar feature; preserve license notices and provenance.

## Route collision / negative tests

- A reverse-marketing-funnel prompt is not reverse engineering.
- Editing an image must remain an image task.
- Imitating a video style is a media/motion task, not application decompilation.
- A repository with source code should be inspected via ordinary code search first.
- A public website URL does not grant consent to inspect private sessions or interfaces.
- A missing REA executable, unsupported Node or unavailable provider must remain non-executed, non-verified.
- Never run unfamiliar installers or binaries solely because the repository mentioned them.

## Evidence contract

Record target and scope, owner authorization, observed tool/provider versions, command and exit status, source anchor (file/module/function/offset), content digest, independent reproduction, uncertainty and provenance. Labels: documented, planned, executed_not_verified, verified. No secrets in receipts. Source code and decompiled proprietary material remain local.

Tests:
    python3 -m unittest discover -s "$SKILL_DIR/evals" -p 'test_rea_bridge.py' -v

The bridge tests establish only adapter logic and authorization gates. Proving real REA interoperability requires a separately authorized fixture and postcondition check.

Source documentation: https://github.com/morluto/rea/blob/main/docs/cli.md and https://github.com/morluto/rea/blob/main/docs/installation.md
