# KOSIF Motion Web — the local studio site (v6)

The site is the hands; Claude is the brain. It runs on the user's PC over the kmotion engine (route A here: FFmpeg,
Edge/Playwright, faster-whisper), binds to 127.0.0.1 and keeps every file local: `workbench/media` (uploads),
`workbench/jobs` (logs), `workbench/renders` (manifest renders), `workbench/timelines`, `out/` (deliveries), `projects/`.

```
python scripts/kmotion.py web --port 8766          # or: KOSIF Motion Web.bat   (opens http://127.0.0.1:8766/)
python -m unittest tests.test_web -v               # 9 offline tests (contract, render jobs, jobs, media, projects, timeline, Claude, MCP)
```

## The UI (Arabic, RTL)
الوسائط (drag-drop upload, probe, copy path) · الوصفات (every recipe as a form; file fields pick from the library; the
command line is shown before it runs) · المشاريع (create 2D/3D/lab/canvas or a motion template; iframe preview of the
self-playing composition; edit index.html / edit.json / verse.json in place with a .bak; frames · draft · render · lint)
· التايملاين (JSON editor + a strip of clips/transitions/overlays computed by the server; validate · save · render) ·
المهام (live log over SSE, outputs with download and inline player) · Workbench (plan → validate → compile → canvas
preview → local MP4 render → project from the manifest) · Claude (ask / copy package / paste reply / apply) · البيئة.

## The Workbench v3 contract, kept
| Route | Same as the hosted site | Local difference |
|---|---|---|
| `GET /api/health`, `GET /api/templates` | yes | `local_version`, `motion_templates` added |
| `POST /api/plan` `{task, seconds, fps, aspect, mode}` | `kosif.proplan.v1`, same rules, same errors (400/415) | — |
| `POST /api/validate` `{plan}` / `POST /api/compile` `{plan}` | same errors/warnings; manifest `kosif.motion.manifest.v1`; `project_html` for 2D | the HTML's `window.render(t)` is also what `kmotion render` drives |
| `GET /api/render/status` | `configured`, `ready` | `limits` (1–600 s, ≤ 1920 px, 24/25/30/50/60 fps, 200 scenes) |
| `POST /api/render/jobs` `{manifest}` → 202 `{job_id, job_token}`; `GET/DELETE /api/render/jobs/ID`; `GET …/video` | `X-Job-Token` capability, 404 for a missing/wrong token, 409 before success, ffprobe verification (frames, size, duration) | silent 2D rendered by the ported Pillow frame; Arabic shaped by RAQM or arabic_reshaper+bidi; the first Arabic font on the machine |
| `POST /mcp` JSON-RPC | `motion_plan`, `motion_validate`, `motion_compile`, `motion_templates` | + the studio tools below |

The skill clients `site_bridge.py` / `render_client.py` are fixed to the hosted origin on purpose; point a copy at
`http://127.0.0.1:8766` to use them against the local site.

## The studio API
`GET /api/env` · `GET /api/recipes` · `POST /api/jobs {recipe, args, note}` → 202 · `GET /api/jobs[/ID]` ·
`GET /api/jobs/ID/log` (SSE, `event: end` carries the final job) · `GET /api/jobs/ID/log.txt` · `POST /api/jobs/ID/cancel` ·
`GET/POST /api/media` (multipart `file`), `DELETE /api/media/NAME`, files at `/media/NAME` ·
`GET /api/projects`, `POST /api/projects {name, kind: new|template|manifest, …}`, `GET /api/projects/NAME/files`,
`GET/POST /api/projects/NAME/file {path, content}` (text files inside the project only; `.bak` kept), previews at `/projects/NAME/index.html` ·
`GET /api/file?path=` (only under the package home, the workbench, or a job's listed outputs) ·
`POST /api/timeline/validate {spec}` → summary (durations, transitions, overlays) · `GET /api/timeline/example` · `/list` · `/save` · `/NAME` · `GET /api/transitions` ·
`GET /api/claude/status` · `POST /api/claude/settings` · `POST /api/claude/ask` · `POST /api/claude/package` · `POST /api/claude/apply {plan}`.

Arguments never touch a shell: a recipe's declared fields become an argv list (options, then `--`, then positionals),
so a value starting with a dash stays a value. Unknown fields are refused.

## Claude: three ways in
1. **MCP (always works):** Claude Code drives the site. Register once:
   `claude mcp add --transport http kosif-web http://127.0.0.1:8766/mcp` — then Claude can list media, write a composition
   into a project (`kosif_project_write`), run `kosif_run` (reel, direct, verse, timeline, render…), poll `kosif_job`,
   render a manifest (`kosif_render_manifest`) and check a timeline (`kosif_timeline_check`).
2. **CLI:** when `claude` (Claude Code CLI) is installed and logged in, the Claude tab sends the package with `claude -p`.
3. **Copy / paste:** the Claude tab copies the same package (rules + live context + the task) to the clipboard; paste it
   into any Claude chat, paste the reply back, press تطبيق. An Anthropic API key can be stored locally in
   `workbench/settings.json` as a fourth route (never shown back in full).

The reply contract is one ```json block: `{"notes", "actions": [{"recipe", "args"}], "files": [{"project", "path", "content"}], "timeline": {...}}`.
Nothing runs on arrival: the plan is shown and applied only when the user presses تطبيق (files are written with a
`.bak`, timelines saved under `workbench/timelines`, actions queued as jobs).

## Honesty
- The hosted site is unchanged; this is a local site. Hosting, Render and the private repository are not touched.
- A render claim always comes with the file: the job's outputs list, the inline player, and `kmotion inspect` when asked.
- Browser verification of the UI was done in the desktop app's browser pane (see CHANGELOG v6.0 for what was clicked).

## v6.1 additions
- `/studio/` — KOSIF Studio 6.0 (from the Workbench v4 source) with «تصدير MP4 دقيق» (offline WebCodecs + mp4-muxer,
  −14 LUFS) next to «تسجيل مباشر» (MediaRecorder). `/examples/` — the v4 cat and MIDNIGHT pages.
- `POST /api/studio/import {project, name?, media_dir?, size?}` → `{saved, spec, report}`: a Studio project → a timeline
  spec saved in `workbench/timelines` (media matched by name in the library unless `media_dir` names another folder
  inside the studio home). The timeline tab has «استيراد مشروع Studio».
- Cross-origin guard: POST/PUT/DELETE on `/api/*` and `/mcp` answer 403 when the browser says the request came from
  another site (`Origin` host not 127.0.0.1/localhost/[::1], or `Sec-Fetch-Site: cross-site|same-site`). GETs and
  clients without an Origin (curl, scripts, MCP clients) are unaffected.
- Upload names that arrive as cp1256 or UTF-8 bytes read as Latin-1 are restored to Arabic.
- KOSIF Studio Cloud: `python scripts/web/build_studio_cloud.py --out studio-cloud.html --home-url URL` builds the
  one-page artifact (modules scoped, mp4-muxer@5.2.1 from jsDelivr, saves through the `downloads` capability).
