# REA upstream v6.7.0 capability atlas for KOSIF Superpowers

Verified upstream GitHub source (2026-10-18): https://github.com/morluto/rea , package `rea-agents`, package.json version **6.7.0**, MIT licensed code with third-party tools covered separately, Node engines `^22.19.0 || ^24.11.0 || >=26.0.0`.

**Use the upstream skill:** `.agents/skills/reverse-engineer-anything/SKILL.md` (not the older pre-6.7 path). Read its current package-matched version before using the CLI; GitHub main and an installed npm version may differ.

## Capability coverage matrix
| Family | Task | Requirement | Safe KOSIF behavior |
|---|---|---|---|
| Native binaries | ELF/Mach-O/PE, function dossiers, pseudocode/callgraph | approved target; supported Hopper/Ghidra | plan-only until provider and authorization |
| Managed .NET | CIL metadata, P/Invoke, versions | local managed artifact | existing `rea_bridge.py plan dotnet` |
| JavaScript/Electron | bundle, ASAR, sourcemaps, app graph | local user-owned artifact | existing `rea_bridge.py plan javascript` |
| Android | APK manifests/classes | JADX/Java when supported | verify prerequisite; do not assume |
| Artifact/package graph | ZIP/APK/IPA/MSIX/AppX, member inventory | owned package | no execution by default |
| Browser/CDP | exact-origin passive state, screenshot, timelines | user-approved session and origins | never auto-attach to live user browser |
| Electron renderer | root-bound page observation | owned app scope | no unapproved Electron API execution |
| Node Inspector | exact approved passive script/contexts | approved target, no instrumentation | preserve no-eval boundaries |
| Network captures | recorded HAR/SAZ/qlog evidence | provided capture | no credential or payload exfiltration |
| Process behavior | controlled capture and replay/diff | explicit sandbox and consent | no hidden execution |
| Firmware | extraction/regions | supported binary and tools | proposal until authorized |
| SQLite | schema/index analysis | local database | existing `rea_bridge.py plan sqlite` |
| Go/Rust | embedded metadata | local executable without executing it | existing bridge plans |
| App-version compare | source-vs-compiled differences and evidence graph | two approved versions | retain provenance and unknowns |
| iOS/macOS artifacts | plist, signatures, Mach-O metadata | approved local bundle and prerequisites | report platform support |
| Provider-neutral evidence | references, immutable evidence and residual unknowns | upstream verified result | independent reproduction before “verified” |

**Current supported installation route:** on supported local machines, inspect `npx -y rea-agents@latest doctor --client claude_code --json` and `setup --client claude_code --dry-run --json`. `npx` may download/cache code; **ask before running installs or setup**. Review planned modifications and obtain approval; avoid `curl | bash`. Installation must be version-pinned for repeatability.

**Legal/technical boundary:** only inspect authorized targets; no DRM/credential bypass, hidden website sessions, bulk copying of third-party application source or pretending reverse-engineered pseudocode proves behavioral equivalence.

**KOSIF integration truth:** the existing `scripts/rea_bridge.py` implements a small safe subset. This atlas links the rest to upstream capability routing; it does not install REA, Hopper, Ghidra, or 100+ live tools. Test `scripts/rea_bridge.py doctor` on the execution host and independently verify the chosen task.
