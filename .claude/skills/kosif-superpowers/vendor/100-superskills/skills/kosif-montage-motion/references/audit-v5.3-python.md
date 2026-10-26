# v5.3-python verification — 2026-10-08

## Scope and result

Added `scripts/render_client.py`, its mocked safety suite, and current English/Arabic render documentation. The public bridge, its existing tests, legacy scripts, templates, examples and legacy references remain unchanged except the current `references/site-bridge.md` routing documentation. No Site mutation, live HTTP request, hosting purchase, renderer deployment or Library upload was performed by this package-update worker. Deployment and transport findings below were supplied by the coordinating task; they are separate from the mocked client tests.

- Initial red test: missing render client caused import failure before implementation.
- New client suite: 13 tests passed.
- Preserved public bridge suite: 31 tests passed.
- Tested fixed URLs/redirect refusal, anonymous no-auth requests, capability headers, approved transmission, status/configuration failure, non-2D rejection, validation/compilation, scaling/rate/duration bounds, Ctrl+C cancellation, JSON bounds, MP4 content type/signature/size checks, exclusive output and racing output creation, and suppression of capabilities from progress output.
- Only fixed, whitelisted states and numeric progress are surfaced; remote error bodies, job tokens and commands are not printed/executed.
- Download publication uses a no-clobber hard link followed by partial unlink instead of POSIX rename, preventing overwrite even if the final file appears while the download is in flight. Unsupported filesystems fail safely.

## Limits

Mocked tests do not prove external hosting exists or a live render works. External Python provisioning remains pending. The renderer must be explicitly configured before an approved end-to-end check. Public demo has three admissions/hour shared and one active job shared, ephemeral outputs and silent 2D only. No client test validates all preserved legacy tools. MP4 magic/content-type checks do not replace a decoder, media probe or visual quality review.

## Deployment and transport status (2026-10-08)

The Site audience is public and its installed MCP was called successfully. A direct anonymous Python urllib request to `/api/health` was nevertheless rejected by the hosting Cloudflare layer with HTTP 403 / error 1010. Public audience does not prove anonymous Python HTTP transport works. The fixed-origin client requires both working Site API transport and a configured, ready backend; it fails closed on these blockers. Do not spoof a User-Agent, bypass the protection, guess another origin or claim this client works live.

The Python renderer source is published in private repository `kosif199022-jpg/kosif-studio`, branch `render-python-service`, commit `43329e10b86db7e1befa35e0ec92a3dab70b4904`, under `services/python-renderer`. Render Free service creation was rejected because Render could not fetch the repository; no service was created. The owner must grant Render repository access before provisioning can continue. A local Python MP4 render and nine backend tests passed, but a hosted end-to-end render remains unverified. Local success does not remove either hosting or API-transport blocker.
