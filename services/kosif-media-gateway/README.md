# KOSIF Media Gateway (Render Free)

A small, independent cloud service that lets Claude (through MCP) and KOSIF Superpowers fetch videos the
owner may download, without the owner's iPhone or computer. It reads only what a platform serves without
signing in: no cookies, no IP or proxy rotation, no CAPTCHA, PO-token or DRM workarounds. When YouTube
refuses the host, the gateway returns the exact code and pauses YouTube calls for a cool-down instead of retrying.

Version 0.3.0. Standard library server; `yt-dlp[default]`, `imageio-ffmpeg` (static ffmpeg with libx264) and
`deno` (the JavaScript runtime yt-dlp needs for YouTube) come from `requirements.txt`.

## Deploy on Render (Free plan only)

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Branch | `main` |
| Build command | `pip install -r services/kosif-media-gateway/requirements.txt` |
| Start command | `python services/kosif-media-gateway/server.py` |
| Health check path | `/health` |
| Plan | **Free**. Never upgrade without the owner's approval. |

Environment variables (set in the Render dashboard, never in the repo):

| Name | Required | Default | Meaning |
|---|---|---|---|
| `KOSIF_GATEWAY_TOKEN` | yes | none | Bearer secret, 32+ random characters (`python3 -c "import secrets;print(secrets.token_urlsafe(32))"`) |
| `KOSIF_MAX_MB` | no | 45 | Largest file accepted |
| `KOSIF_DOWNLOADS_PER_HOUR` | no | 3 | Download attempts per hour |
| `KOSIF_FILE_TTL` | no | 600 | Seconds a finished file stays downloadable, then deleted |
| `KOSIF_BLOCK_COOLDOWN` | no | 1800 | Seconds YouTube is left alone after LOGIN_REQUIRED / 429 / 403 / proxy 502 |
| `KOSIF_DOWNLOAD_TIMEOUT` | no | 150 | Seconds for one yt-dlp download |
| `KOSIF_TRANSCODE_TIMEOUT` | no | 240 | Seconds for the libx264 fallback |
| `KOSIF_EXTRA_HOSTS` | no | empty | Extra https hosts allowed besides YouTube, Wikimedia, archive.org and Vimeo |
| `KOSIF_UPLOAD_MB` | no | 150 | Largest upload from the owner's device |
| `KOSIF_UPLOAD_TTL` | no | 3600 | Seconds an upload stays available |
| `KOSIF_PUBLIC_PROBE_EVERY` | no | 900 | Minimum seconds between unauthenticated `/health?deep=1` checks |

`RENDER_EXTERNAL_URL` is set by Render itself and is used to build absolute file links. `RENDER_GIT_COMMIT` and
`RENDER_GIT_BRANCH` (also set by Render) appear in `/health` as `build.commit` / `build.branch` (0.3.0+).

### Is Render running the latest code?

Every change to `server.py` bumps `VERSION`. `python3 services/kosif-media-gateway/deploy_check.py` (public, no
token) compares the deployed `/health` with this checkout: `FRESH`, `STALE` or `UNREACHABLE`. The workflow
**KOSIF Media Gateway live check** runs it daily and warns on `STALE`. The fix is the owner's: Render dashboard >
the service > **Manual Deploy > Deploy latest commit**, or turn **Auto-Deploy** on for `main`.
Free services sleep after ~15 idle minutes, so the first request can take up to a minute.

## API

| Call | Auth | What it does |
|---|---|---|
| `GET /health` | none | Version, deployed commit (`build`), dependencies actually executed (`yt-dlp --version`, `ffmpeg -version`, libx264, JS runtime), limits, the last YouTube result and cool-down |
| `GET /health?deep=1` | none | Same, plus a fixed-video check (`dYrEeavC3cw`, metadata and the first ~10 KB of a stream), at most every 15 min |
| `POST /v1/probe` | Bearer | `{"video": "ID or URL", "media_check": true}`: metadata and, with `media_check`, a real 10 KB stream read |
| `POST /v1/download` | Bearer | `{"video": "ID or URL", "rights": "cc-licensed", "quality": 720}` |
| `GET /v1/files/<ticket>` | Bearer | The file; `X-Content-SHA256` header carries its hash |
| `POST /mcp` | Bearer | MCP Streamable HTTP (stateless JSON responses) |
| `POST /v1/upload` | Bearer | Raw video body (`--data-binary @file`, headers `X-Filename`, `X-Source-Url`): verified like a download, kept `KOSIF_UPLOAD_TTL` (default 1 h), max `KOSIF_UPLOAD_MB` (default 150). `Expect: 100-continue` is refused before any byte for a bad token or size |
| `GET /v1/inbox` | Bearer | Uploads still held, newest first (MCP tool `list_uploads`) |
| `GET /kosif-send.sh` | none | The a-Shell script below (contains no secrets) |
| `GET /browser` | none | KOSIF Video Browser: paste a YouTube link, watch it in YouTube's official embed, read public oEmbed data, thumbnails and duration. It does not download: the page cannot read the player's media (cross-origin) and YouTube blocks direct requests (CORS) |

`rights` must be one of `owned`, `written-permission`, `public-domain`, `cc-licensed`, `youtube-authorized`.
`quality` (360/480/720/1080) caps the **shorter side** (Cinema C V34 rule), so a portrait 1080x1920 Short counts as 1080.

What a download does:
1. yt-dlp with the V34 selector: H.264 + AAC first, any codec as fallback, `--max-filesize`.
2. The original is checked with a real decoder: full demux, first frames, the last 2 seconds, audio, and the
   duration against the platform's. A partial, corrupt or short file is deleted and the call fails.
3. A compatible MP4 is made: lossless stream copy with `+faststart` when the original is already H.264/AAC,
   libx264 + AAC otherwise; it is verified the same way. The original is always kept as its own file.
4. Both files get SHA-256, size, duration, display size (rotation aware), orientation and codecs, and a
   bearer-protected link that expires after `KOSIF_FILE_TTL`.

Errors are exact: `YOUTUBE_LOGIN_REQUIRED`, `YOUTUBE_HTTP_429`, `YOUTUBE_HTTP_403`, `YOUTUBE_PROXY_502`,
`DRM_PROTECTED`, `ACCESS_RESTRICTED`, `FILE_TOO_LARGE`, `CORRUPT_OR_INCOMPLETE`, `INCOMPLETE_DURATION`,
`DOWNLOAD_TIMEOUT`, `BUSY_ONE_DOWNLOAD_AT_A_TIME` (409), `RATE_LIMIT_PER_HOUR` (429), `INVALID_SOURCE` (400).

## Test it

```sh
G=https://kosif-media-gateway-free-20261030.onrender.com
curl -s $G/health
curl -s "$G/health?deep=1"
curl -s $G/v1/probe -H "Authorization: Bearer $KOSIF_GATEWAY_TOKEN" -H 'Content-Type: application/json' \
     -d '{"video":"dYrEeavC3cw","media_check":true}'
curl -s $G/mcp -H "Authorization: Bearer $KOSIF_GATEWAY_TOKEN" -H 'Content-Type: application/json' \
     -H 'Accept: application/json, text/event-stream' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
# a real MCP client (official SDK): initialize, tools/list, tools/call
python3 services/kosif-media-gateway/mcp_client_check.py $G/mcp --probe dYrEeavC3cw --out mcp-report.json
```

Keep the token in an environment variable; never paste it into chat, commits or logs.

Full live check (health, MCP with the official SDK, wrong-token rejection, and a real verified download of a
public-domain archive.org film pulled back and decoded locally):

```sh
python3 services/kosif-media-gateway/live_check.py --out live-report.json
```

Without a local machine: add the repository secret `KOSIF_GATEWAY_TOKEN` (GitHub Settings > Secrets and
variables > Actions) and run the **KOSIF Media Gateway live check** workflow; it uploads `live-report.json`
(token-free) as an artifact.

## Connect Claude Code

```sh
claude mcp add --transport http kosif-media https://kosif-media-gateway-free-20261030.onrender.com/mcp \
  --header "Authorization: Bearer $KOSIF_GATEWAY_TOKEN"
claude mcp list        # expect: kosif-media ... ✓ Connected
```

Tools: `gateway_status`, `list_uploads`, `probe_youtube`, `download_permitted_video`.

## From the iPhone: kosif-send (share button)

YouTube refuses cloud hosts, but the owner's iPhone downloads fine (Cinema C). `kosif-send` downloads on the
phone with a-Shell and uploads the verified file here, so Claude can fetch it with `list_uploads` or
`_media_gateway.py pull`.

In a-Shell, once:

```sh
mkdir -p ~/Documents/bin
curl -fsSL https://kosif-media-gateway-free-20261030.onrender.com/kosif-send.sh -o ~/Documents/bin/kosif-send
chmod +x ~/Documents/bin/kosif-send
kosif-send --setup        # paste the token; saved in ~/Documents/.kosif/token (mode 600)
kosif-send --check
```

Use: `kosif-send "https://youtube.com/shorts/..."` (Arabic text around the link is ignored) or
`kosif-send --file ~/Documents/Cinema_Downloads/clip.mp4`. Shortcuts: an iOS shortcut that accepts URLs from the
Share Sheet and runs a-Shell's **Execute Command** action with `kosif-send "<Shortcut Input>"`.
The token never appears on a command line; curl reads it from a temporary private header file.

## KOSIF Superpowers

`fetch_video.py URL --gateway cc-licensed` tries the local machine first (yt-dlp, TikTok, Pinterest, stock
sites unchanged) and, only if that fails, asks the gateway once. The client is
`.claude/skills/kosif-superpowers/scripts/_media_gateway.py` (`health`, `probe`, `download`); it needs
`KOSIF_GATEWAY_TOKEN` and optionally `KOSIF_GATEWAY_URL`, re-checks each file's SHA-256 and size, and writes
files atomically. `_media_gateway.py inbox` lists what the iPhone sent; `pull [UPLOAD_ID] -o DIR` fetches it.

## Tests

```sh
pip install imageio-ffmpeg mcp
python3 -m unittest discover -s services/kosif-media-gateway/tests -v
```

Offline (stub yt-dlp, real ffmpeg, real HTTP server, official MCP SDK client): auth failures, malformed ids,
SSRF guard, oversized bodies, keep-alive after 401, LOGIN_REQUIRED / 429 / 403 / proxy 502 cool-down with no
second request, corrupt and short files rejected and cleaned, size limit, timeout, one-at-a-time, hourly
limit, expiry, lossless remux, libx264 fallback, and the Superpowers client's hash check.
CI: `.github/workflows/media-gateway.yml`.

## Measured status (2026-10-31)

`/health?deep=1` from the live service: `YOUTUBE_LOGIN_REQUIRED` for `dYrEeavC3cw`, `youtube_download_verified: false`.
YouTube refuses Render's data-center IP, as it refuses the Claude sandbox. Use the gateway as an inbox for files the
phone downloaded (`kosif-send`, then `list_uploads`) and for archive.org / Wikimedia / Vimeo. Protocol appendix A47.

## Honest limits

A healthy `/health` or a successful metadata probe does not prove a download will work: YouTube can serve
metadata and still refuse the media stream (HTTP 403) to data-center IPs. Only a `download` that returns
`verified: true` with a SHA-256 is proof. If Render's IP is refused, the options are the owner's own device
(Cinema C), an uploaded file, or a provider the owner is authorized to use; the gateway will not work around it.
