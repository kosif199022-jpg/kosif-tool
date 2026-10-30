# KOSIF Media Gateway — Render Free proof

A small independent cloud gateway to test read-only YouTube access and download only owned or explicitly licensed videos. No login/CAPTCHA/DRM bypass. A free cloud IP may encounter the same block as GitHub.

## Deploy on Render Free

* Build: `pip install -r services/kosif-media-gateway/requirements.txt`
* Start: `python services/kosif-media-gateway/server.py`
* Environment: `KOSIF_GATEWAY_TOKEN` must be a strong secret (configured on Render, not stored in the repo).
* Plan: `free` only. Free services spin down after inactivity. Included bandwidth/build minutes are limited and overages **may be billed if a payment method is on file**.

## API

* `GET /health` dependency status only, not a YouTube download success claim.
* `POST /v1/probe`: bearer auth + JSON `{"video":"dYrEeavC3cw"}`. Returns real yt-dlp accessibility test.
* `POST /v1/download`: bearer auth + JSON `{"video":"VIDEO_ID","rights":"owned"}`. Download only authorized videos; 45 MB maximum, one task at a time, 3 per hour.
* `GET /v1/files/TICKET`: bearer auth required, 10-minute temporary MP4.
* `POST /mcp`: basic stateless JSON-RPC 2.0 MCP with `probe_youtube` and `download_permitted_video` tools. This must be tested with the target Claude MCP host before claiming client integration.

Example:

    curl -s https://SERVICE.onrender.com/health
    curl -s https://SERVICE.onrender.com/v1/probe -H "Authorization: Bearer $KOSIF_GATEWAY_TOKEN" -H 'Content-Type: application/json' -d '{"video":"dYrEeavC3cw"}'

If the cloud probe reports `YOUTUBE_LOGIN_REQUIRED` or `YOUTUBE_HTTP_429`, stop and report the block. No rotating IPs, cookies from others, challenge bypass, or covert client workarounds.

Acceptance: a deployed /health, live probe result for the exact video, and only a verified MP4 for authorized accessible content. A healthy web server alone is not proof that YouTube download works.
