# Public Workbench API and bridge

## Anonymous access and content approval

Origin: https://kosif-motion-workbench.smartsphere152.chatgpt.site

The public Site supports anonymous requests without a token or authentication header. An optional, existing, explicitly authorized `KOSIF_SITE_TOKEN` can still be supplied through the environment and sent in `OAI-Sites-Authorization` to the exact origin. No credential creation, lookup or acquisition is included. Never put a token into the command line, a saved project, chat, a log, or source control. Access denial, redirects, non-JSON responses and bounded transfer failures stop the call; there is no automatic retry, credential acquisition or origin fallback.

`--allow-remote` is required for POST requests. It must reflect the user's permission to send the actual task/plan contents to this Site. It is not permission to share unrelated private information. `health` and `templates` send no task contents and need no token. No media upload endpoint exists.

## Contract

- GET `/api/health`: service status, not proof of rendering capability.
- GET `/api/templates`: available planning presets.
- POST `/api/plan`: `{task, seconds, fps, aspect, mode}`. Task is 1–5000 characters; seconds 2–600; fps 24, 25, 30, 50 or 60; aspect 9:16, 16:9, 1:1 or 4:5; mode standard or pro.
- Plan response: `schema: "kosif.proplan.v1"`, `route: "remote_planning_only"`, intent, timeline `{fps, seconds, total_frames, aspect, shots}`, stages, commands, limitations and gates. This service never verifies Full Pro execution receipts. Structural requests are unsupported.
- POST `/api/validate`: `{plan}` → `{valid, errors, warnings, summary}`. Read `valid`; HTTP success alone does not certify a plan.
- POST `/api/compile`: `{plan}` → `{manifest, handoff, warnings, project_html}`. Manifest schema `kosif.motion.manifest.v1` includes title, width, height, fps, duration and scenes. Handoff has `execution: "local_only"` and command argument arrays. They are guidance, not automatically executed instructions.
- `project_html` is a simple self-contained deterministic 2D canvas composition only when supported. Otherwise it is null. 3D, prompt-only and footage requests do not become authentic rendered content merely by compiling a plan.

The new manifest is not directly accepted by legacy `motion.py`. For unsupported generated HTML cases, a human or authorized agent authors the existing HTML/template project using the planned shots, then renders locally.

## External Python rendering

The current rendering route is an external Python server behind the Site proxy, not browser video export. Hosting/provisioning remains pending. The unchanged planning bridge writes JSON/HTML only; use the separate [render client](python-render.md) for silent 2D MP4 once the backend reports ready. Its public demo mode needs no secret API key. This does not imply live rendering is available.

## CLI

Run `python scripts/site_bridge.py --help` or a subcommand's `--help`.

```bash
python scripts/site_bridge.py health
python scripts/site_bridge.py templates --out templates.json
python scripts/site_bridge.py plan --task "An Arabic 12-second launch teaser" --seconds 12 --fps 30 --aspect 9:16 --mode pro --allow-remote --out plan.json
python scripts/site_bridge.py validate --plan plan.json --allow-remote --out validation.json
python scripts/site_bridge.py compile --plan plan.json --allow-remote --out compiled.json
python scripts/site_bridge.py project --plan plan.json --allow-remote --out-dir ./launch-preview
```

Outputs use exclusive creation: existing files are never overwritten. The `project` destination must be new, its parent must exist, and the path must contain no symlink or `..`. It writes only `index.html`; review the returned code before rendering. The client never opens a browser, runs a renderer, interprets handoff commands or uploads local files. It uses a 20-second request timeout, 1 MiB request/response bounds and exact-origin HTTPS without redirects or environment proxies. The bridge consumes local JSON plan contents only when explicitly requested.

After review and separate authorization for local execution, the existing deterministic renderer can consume a supported project's HTML:

```bash
python scripts/motion.py render ./launch-preview --engine studio --out launch.mp4
python scripts/motion.py inspect launch.mp4
```

Local prerequisites include Python dependencies, FFmpeg and Playwright/Chromium. These commands are examples, not a claim that rendering has been tested in this release. The 2D preview uses canvas typography; inspect Arabic shaping and line layout in the target browser before final delivery.

## Verification

Run only the reviewed bridge suite:

```bash
python -m unittest discover -s tests/bridge -v
```

This suite tests payload formation, approval gates, anonymous success without a token, optional-token access failure, exact-origin handling, refused redirects, token-echo suppression, bounded transfers, JSON parsing and safe project creation. It uses mocked HTTP; it does not prove live Site availability or an actual media render. Legacy tests are retained separately and require their own review and appropriate runtime before execution.
