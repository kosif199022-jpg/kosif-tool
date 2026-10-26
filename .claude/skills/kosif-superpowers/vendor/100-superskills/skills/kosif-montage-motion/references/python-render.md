# External Python rendering client

The Site address is fixed: https://kosif-motion-workbench.smartsphere152.chatgpt.site. The Site proxies jobs to an external Python/Pillow/FFmpeg service; the browser is not the render engine. Hosting resources and configuration are pending. A packaged client is not proof that this service is deployed. No live endpoint was called in the v5.3 client tests; the separate live transport check is documented below.

## Consent and prerequisites

- Python 3.10+ standard library. No local FFmpeg, browser or API secret is needed by this client.
- Before submitting, obtain approval for the plan contents to be processed via the public Site by the external render hosting provider, which temporarily keeps the manifest and output. Public access alone is not approval to transmit private data. `--allow-remote` records approval already obtained.
- The external service must first be provisioned by an authorized person and connected to the Site. The client never provisions hosting, creates credentials, buys resources, upgrades quotas or runs remote commands. Missing configuration/resources produce an explicit error.
- Public demo: three accepted jobs per rolling hour shared by all anonymous visitors, and one queued/running job shared. Outputs expire and may be evicted; download promptly. Do not use temporary service outputs as permanent storage.

## Commands

```bash
python scripts/render_client.py status
python scripts/render_client.py render --plan plan.json --out NEW.mp4 --allow-remote
```

Use `site_bridge.py plan` to prepare a `kosif.proplan.v1` plan. Only `intent: 2d_motion` is accepted. The render client calls `/api/validate`, requires `valid: true`, calls `/api/compile`, and submits only the strict manifest. It ignores returned HTML, handoff commands and URLs. It refuses 3D, footage-edit and prompt-only plans, arbitrary scene fields, media inputs and commands.

Accepted MP4 content is silent 2D. Duration must be 1–30 seconds in whole frames; the public plan endpoint currently requires at least 2 seconds. FPS is 24, 25 or 30; unsupported rates are rejected rather than retimed. Dimensions are downscaled proportionally to a maximum long edge of 1280, rounded down to even pixels; this can introduce less than two pixels of aspect rounding. The minimum dimension is 128. Scenes must cover the timeline contiguously. Generated output is the simple Python 2D interpretation, not authentic 3D or a pixel-identical browser composition. Review Arabic shaping, framing and the final media before delivery.

## Fixed contract and safety

1. GET `/api/render/status` must return `configured: true, ready: true`.
2. POST `/api/validate` and `/api/compile` use `{plan}`.
3. POST `/api/render/jobs` uses `{manifest}` and returns `job_id`, `job_token`.
4. Poll GET `/api/render/jobs/{id}` with `X-Job-Token`. Only fixed state names and numeric progress are printed.
5. On success, GET `/api/render/jobs/{id}/video` with the same capability; accept `video/mp4`, up to 100 MiB, and basic MP4 signature checks. This is transport verification, not full codec/media QA.
6. On Ctrl+C or a known render failure/deadline, attempt DELETE `/api/render/jobs/{id}` with the capability. If cancellation cannot be confirmed, say so. Cancellation after completion also removes remote output.

Capabilities are held only in process memory, never printed, saved, placed in query strings or taken from user-provided URLs. No authentication header or `KOSIF_SITE_TOKEN` is used by this client. No redirects, environment proxy routing, arbitrary host, media upload, subprocess or remote command execution is supported. Each network request has a timeout up to 20 seconds within a nominal 300-second job deadline; a cancellation attempt can add up to 10 seconds. There is no automatic job resubmission.

Output must be a new `.mp4` under an existing nonsymlink directory, without `..`. Bytes stream to a private exclusive `.partial` file. After validation, an atomic no-clobber hard-link publication gives the final filename, then removes the partial name. This deliberately avoids POSIX rename's overwrite behavior. Filesystems without hard-link support fail safely. Existing output files are never replaced. Partial files are removed on errors and interruption. Process termination or power loss may leave a partial file; inspect and remove it manually.

## Local tests

```bash
python -m unittest discover -s tests -p test_render_client.py -v
python -m unittest discover -s tests/bridge -v
```

These are mocked network tests only. Run status and a separately approved end-to-end render only after the deployment is configured. Do not infer production readiness from these tests.

## Deployment and transport status (2026-10-08)

The Site audience is public and its installed MCP was called successfully. A direct anonymous Python urllib request to `/api/health` was nevertheless rejected by the hosting Cloudflare layer with HTTP 403 / error 1010. Public audience does not prove anonymous Python HTTP transport works. The fixed-origin client requires both working Site API transport and a configured, ready backend; it fails closed on these blockers. Do not spoof a User-Agent, bypass the protection, guess another origin or claim this client works live.

The Python renderer source is published in private repository `kosif199022-jpg/kosif-studio`, branch `render-python-service`, commit `43329e10b86db7e1befa35e0ec92a3dab70b4904`, under `services/python-renderer`. Render Free service creation was rejected because Render could not fetch the repository; no service was created. The owner must grant Render repository access before provisioning can continue. A local Python MP4 render and nine backend tests passed, but a hosted end-to-end render remains unverified. Local success does not remove either hosting or API-transport blocker.
