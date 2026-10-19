# KOSIF Integrations: Drawing, 3D and an Isolated Browser Foundation

Scope (2026-10-19): public feature descriptions and 26-target research
registry. Not full source reverse engineering, a deployed cloud browser,
or verified feature parity. Each target in data/integration-target-atlas.json
has one functional gap and an original implementation route.

## Implemented now

- Browser-scout doctor lists local Playwright and curated target count with no network.
- The list and inspect commands return public URLs, categories and feature areas.
- Capture attempts a read-only screenshot in a fresh browser context from a
  separately installed Playwright engine, explicitly limited to its target host.
- Redirects and assets on other hosts are blocked, so some complex websites
  may render incorrectly; no private account, credential or cookie is used.
- No login automation, form submissions, CAPTCHA bypass or source extraction.
- Unit tests validate the URL policy. Live browser screenshot is a separate gate.

## Future genuine cloud browser (not deployed)

1. Host Playwright in a dedicated authenticated cloud service, per-user
   disposable VM or container. Block RFC1918/local IP and DNS rebinding
   at network level; do not rely on URL checks alone.
2. Isolate browser contexts, filesystem, cookies, downloads, encryption,
   sessions and screenshot exports per user and company.
3. API allows approved navigate/screenshot/click/wait/accessibility operations.
   Payments, sending messages, credentials, file changes require confirmation.
4. Session expiration, audit records, throttling and denial tests required.
5. Prove that company A cannot access company B's cookie/storage and that
   redirected URLs, private networks and downloads are blocked.

Documentation:
https://playwright.dev/docs/browser-contexts
https://playwright.dev/docs/api/class-browser

## Legally usable inspiration and open-source engines

- SVG-Edit: MIT SVG editor: https://github.com/SVG-Edit/svgedit
- Archived p5.js editor: MIT licensed: https://github.com/processing/p5.js-editor
- AutoDraw: proprietary ML/artist drawing suggestion; do not copy assets:
  https://experiments.withgoogle.com/autodraw
- Photopea: editable PSD layers, concepts only:
  https://www.photopea.com/learn/layers
- Blender/Cycles: Cycles has standalone build instructions:
  https://github.com/blender/cycles/blob/main/BUILDING.md
  Verify current file-specific licenses/dependencies before integration.
- Proprietary browsers/Claude/Codex/Maya/Canva/Pixlr/etc: documented
  APIs and public features only; no private code transfer.

## Actual completion gates

The local browser code is a prototype, not an independent browser engine
or remotely hosted service. Browser installation and actual screenshot
must be checked before claiming execution. The existing native_3d
software renderer is limited and not Blender parity. Every Atlas skill
needs separate licensing, security and runtime evidence to be trusted.

## Atlas external catalog metadata verification

The externally supplied KOSIF Atlas index snapshot contains 14,708 regular
and 85 separately licensed/copyleft records, 14,793 total. The static audit
checks every record schema, license label, source URL, risk flag and reported
security verdict without executing external scripts. The snapshot's claims are
not independent source verification. Execute:
python scripts/atlas_metadata_audit.py --index INDEX.json --copyleft INDEX_COPY.json.
On 2026-10-19 the local index snapshot passed structure checks with 0
structural errors; 9,508 records said REVIEW_BEFORE_INSTALL across both
indices. All these entries still need trust/license validation before importing.
This cannot be called a line-by-line audit of 14,793 source folders.

## Live browser probes on Windows (2026-10-19)

Fresh, unauthenticated, host-scoped Chromium sessions produced:

| Site | HTTP response | Result | Limitation |
|---|---:|---|---|
| Photopea | 200 | Screenshot captured | Cross-origin resources were intentionally denied, so feature usability is not validated |
| Canva Draw | 403 | Challenge/interstitial captured | Did not bypass the platform's protections or access a canvas |
| p5.js Editor | 200 | Screenshot captured | Response and screenshot alone do not verify sketch runtime or save features |

Screenshots retained locally in `KOSIF_RESEARCH_PRIVATE_20261019/SCOUT_{id}_20261019.png` (not pushed to a public repository). No credentials or persisted cookies. The result is a public UI survey, **not an atomic analysis of all source code**.

## Best route to rendering without the Blender application

For a portable renderer with lighting, the official [Cycles standalone engine](https://github.com/blender/cycles) exposes a CLI and example XML scenes; its GitHub standalone repository is labeled Apache-2.0, with separate dependency notices. [Build instructions](https://github.com/blender/cycles/blob/main/BUILDING.md) require an independent build and precompiled dependencies. Integrating this engine is a more realistic avenue to production path-tracing than reverse-engineering Blender's installed executable. Not yet built, installed or production-tested on this Windows device.

The original KOSIF `native_3d.py` is the tested **zero-Blender runtime** option, currently restricted to primitive geometry and simplified lighting. Its visual fidelity cannot be equated to Cycles or Blender. Prefer gradual mesh/z-buffer/shading/material improvements with pixel- and frame-level tests, not marketing feature counts.

## Fresh static Desktop `Tajriba` inventory (2026-10-19)

A **new scan of current contents** found 2,109 readable files, 18,530,811,455 bytes, 1,232 source-review candidates, 30 native binary candidates for REA/Ghidra, 137 archive-metadata candidates, 32 image assets and 3 media/project assets. The scan did NOT open executable binaries in Ghidra, unpack all archives or prove application behavior. Report location (private laptop only): `KOSIF_RESEARCH_PRIVATE_20261019/TAJRIBA_RESCAN_20261019.json`.

This replaces the historical 2,006-file static inventory as a *current file-count snapshot*. Changing archives and duplicate extracted folders explain why snapshot totals can differ; do not claim full understanding of the 18.53 GB from this scan.

GitHub CLI enumerated 24 accessible repositories for `kosif199022-jpg` and 2 for `elkosif0-cmd` in this session. Those are metadata enumeration counts, not a source-level audit of all their histories, branches, dependencies or tests.
