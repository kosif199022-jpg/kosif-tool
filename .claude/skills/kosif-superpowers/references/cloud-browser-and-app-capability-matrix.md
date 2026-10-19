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
