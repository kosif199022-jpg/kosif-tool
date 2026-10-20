# REA × KOSIF Superpowers — evidence-first software investigation

**Status:** optional local integration. On 2026-10-18 REA v6.7.0 was installed in a scratch folder and run here: 19 commands produced Evidence records, 11 refused correctly for missing engines — see [proofs/rea-static-runs](../proofs/rea-static-runs/README.md). All 153 CLI commands plus the 76 MCP-only tools and 6 MCP prompts are registered as powers REA-001…REA-235 in [software-investigation](powers/software-investigation.md) (`python3 $SKILL_DIR/scripts/rea_bridge.py catalog <word>` lists them).

**Upstream attribution:** morluto/rea — https://github.com/morluto/rea (MIT for REA-authored code, Copyright (c) 2026 morluto). Third-party binaries, Hopper, Ghidra, IDA, JEB and their assets retain separate terms; see https://github.com/morluto/rea/blob/main/THIRD_PARTY_NOTICES.md. This integration contains original KOSIF glue code, not copies of REA or decompiled third-party sources.

## Contents
- [Added abilities: evidence-backed routes](#added-abilities-evidence-backed-routes)
- [Full inventory by requirement (REA 6.7.0: 153 CLI commands, 207 MCP tools, 6 prompts)](#full-inventory-by-requirement-rea-670-153-cli-commands-207-mcp-tools-6-prompts)
- [Sequence and examples](#sequence-and-examples)
- [Route collision / negative tests](#route-collision--negative-tests)
- [Evidence contract](#evidence-contract)
- [Refreshed upstream discovery (2026-10-18)](#refreshed-upstream-discovery-2026-10-18)
- [Windows installers and desktop apps (added 2026-10-18, run on Windows 11)](#windows-installers-and-desktop-apps-added-2026-10-18-run-on-windows-11)

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

Verified here (✅ in the catalog): analyze-javascript-application, inspect-analysis-view, trace-application-feature, inspect-go-binary, inspect-rust-binary, inspect-artifact, extract-artifact, inspect-electron-fuses, inspect-evm-interface, inspect-with-objdump, list-objdump-architectures, list-browser-targets, inspect-web-page, analyze-web-bundle, capture-web-screenshot, inspect-web-event-listeners, doctor, capabilities, providers. Everything else is 📦 (REA alone or a plain input) or 📄 (bring-your-own engine: Hopper, Ghidra 12.1, IDA MCP, Kuna, JEB, jadx-headless-mcp, apktool, adb device, Frida, Rizin/Cutter, GDB, WABT, tshark, Binwalk, sigrok, Wakaru, macOS toolchain). The badge is the lowest level that is true on this machine; a different machine with those engines configured raises it only after a real run.

## Engines installed here (2026-10-18)

gdb 15.1, WABT 1.0.34, TShark 4.2.2, sigrok-cli 0.7.2, apktool 2.7.0 and adb 34.0.4 were installed in this container, so five more read-only commands now pass (inspect-pcap-client, inspect-packet-fields, inspect-signal-decoders, inspect-apktool-client, inspect-adb-client — see proofs/rea-static-runs). REA pins exact engine versions: WABT 1.0.42 is required, so inspect-wasm-artifact stays unavailable with 1.0.34. Native disassembly still needs Ghidra, Hopper or IDA, which the proxy here cannot download.

## Full inventory by requirement (REA 6.7.0: 153 CLI commands, 207 MCP tools, 6 prompts)

| group | commands | needs | badge |
|---|---|---|---|
| JavaScript & web (static graph, feature trace, version compare, source-to-bundle, CDP page/bundle/screenshot/listeners/session/execution, WebMCP discovery, HAR/mitmproxy/SAZ/qlog captures, source-map traces) | 23 | REA; loopback CDP browser for observation; Wakaru for source recovery | ✅/📦 |
| Evidence & core (inspect/extract artifact, EVM via evmole, evidence import/export/compare/bundle, reconstruction ledger and coverage, process capture and compare, capabilities, providers, doctor, setup, update, uninstall) | 21 | REA | ✅/📦 |
| Native binaries (analyze, inspect, decompile, function, xrefs, trace, instructions, search, bytes, addresses, data types, load images, call targets, def-use, UI actions, annotations) | 18 | Hopper / Ghidra / IDA / Kuna | 📄 |
| Android device, jadx and apktool (30 adb commands incl. pull/push/install/start/stop/logcat/bugreport, class/method/references, resource decoding) | 30 | adb-authorized device, jadx-headless-mcp JAR, apktool | 📄 |
| Static APK parsing (inspect-android-package, identify-flutter-build, inspect-dart-aot) | 3 | an APK | 📦 |
| Apple (Mach-O, signatures, plists, Swift demangle, asset catalogs, Interface Builder, keyed archives, dylib resolution, native UI/calls observation, Apple app graph) | 15 | macOS toolchain | 📄 |
| Electron / Node runtime (targets, pages, scenarios, runtime observation and reconciliation) | 7 | consented local Inspector target | 📦 |
| .NET managed (identity, members, P/Invoke boundaries, compare, verify, reconstruction import, app graph) | 7 | REA (rea-dotnet-static) | 📦 |
| Others: Rizin/Cutter 4, JEB 4, pcap/tshark 4, Frida 3, WASM/WABT 2, sigrok 2, firmware/Binwalk 2, objdump 2 (✅), GDB 1, ELF layout/pwntools 1, PE resources 1, recorded crash 1, SQLite (Node 24.15+) 1, HarmonyOS 1 | 29 | as named | 📄/📦 |

Prompts shipped by the MCP server: investigate_feature, compare_application_versions, verify_reconstruction, trace_crash, audit_residual_unknowns, prepare_bounded_process_capture. Use them through a connected client; the CLI covers the same catalog with `--format`, `--token-limit` and `--filter-output` to keep context small.

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

## Refreshed upstream discovery (2026-10-18)
Upstream REA 6.7.0 (package.json at inspection) exposes far more than the static `run` kinds the current bridge wraps (`python3 $SKILL_DIR/scripts/rea_bridge.py run --help` lists them). Use `scripts/rea_family_router.py list` and `route <intent>` for 16 evidence/inspection families, and [current REA family matrix](rea-upstream-capabilities.md). The upstream skill moved to `.agents/skills/reverse-engineer-anything/SKILL.md`, with a package-matched runtime on installation. This **does not claim** 16 locally runnable categories. Existing `rea_bridge.py` remains canonical for authorized safe static subset.

## Windows installers and desktop apps (added 2026-10-18, run on Windows 11)

REA's artifact graph reports an NSIS, Inno or UPX installer as **one PE with no child entries**, so the app inside is never reached. Run the triage first ([proof](../proofs/windows-installers-rea/README.md)):

    python $SKILL_DIR/scripts/installer_triage.py scan "<folder or setup.exe>"           # NSIS/Inno/UPX/7z/MSI/Burn/Squirrel, Electron, .NET, signature slot, version info
    python $SKILL_DIR/scripts/installer_triage.py unpack setup.exe --to ./unpacked --authorized   # 7-Zip into an ABSENT folder; never runs the target
    python $SKILL_DIR/scripts/installer_triage.py fingerprint ./unpacked/.../resources/app.asar  # Electron capability anchors, file associations, windows, RTL
    python $SKILL_DIR/scripts/installer_triage.py route ./unpacked/...                    # the REA command for each artifact

Lessons from Canva 1.126.1, CapCut and the Adobe Premiere Pro setup:

| Symptom | Cause | Do this |
|---|---|---|
| `inspect-pe-resources`: "PE section raw bytes overlap headers" | UPX-packed stub | unpack a copy with `upx -d`, or skip resources |
| `inspect-managed-artifact`: `resource_constraint` | 213 MB file > 128 MiB snapshot budget | inspect the extracted DLLs, not the installer |
| `analyze-javascript-application`: `provider_timeout` at 300 s | one huge vendor chunk | `--source-path <main> --source-path <preload>` first |
| 0 Electron APIs in a 6.8 MB main bundle | minified aliases hide `require('electron')`; per-file cap 20,000 semantic nodes | `installer_triage.py fingerprint` for anchor counts; raise `--max-semantic-nodes-per-file` if needed |
| small signed setup with downloader DLLs | online bootstrapper | the product is not in the file; analyse the installed folder instead |

**Windows notes:** use `python` (or `py -3`) where this guide says `python3`. `rea_bridge.py` now runs `node <rea-agents>/scripts/rea.mjs` instead of the `rea.cmd` shim (no cmd.exe argument re-parsing); point `REA_BIN` at a local install, raise `--timeout` (default 600 s) for big bundles, and pass `--source-path` to scope a JavaScript run. Verify Authenticode before anything else: `Get-AuthenticodeSignature <file>`.

What the three apps can do became powers: [app-feature-transfer](app-feature-transfer.md) (APPX-01…30).
