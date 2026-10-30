# A45 — YouTube download tool (yt_get)

> **متى تقرأه / when to read:** تنزيل فيديو من يوتيوب · [العودة إلى النواة / back to the core](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

**Tool:** `.claude/skills/living-site/tools/yt_get.sh <url> [out-dir]`
**Runs on:** the user's own device (Mac / PC / a-Shell). Not from a cloud sandbox.
**Output:** the video file + `receipt.json` (url, file, step, bytes, sha256, duration, resolution).

## Why it must run on the user's device (tested 2026-10-30)

From the cloud sandbox, with yt-dlp 2026.10.26 + deno 2.5.4:
- `www.youtube.com` answers `429 Too Many Requests`, then `Sign in to confirm you're not a bot`.
  YouTube blocks data-center IPs.
- Metadata for the test video `dYrEeavC3cw` could be read (title, 46 s, formats up to 1080x1920).
- The download step itself was refused by this environment's safety policy as bot-check circumvention.
  So the cloud does not download YouTube. The user's own home connection does.

## Evidence: test video downloaded on the user's iPhone (2026-10-30)

Cinema C (`cinema-c/Cinema_C_V35_iPhone.sh` (in the project folder, not this repo), a-Shell) downloaded `dYrEeavC3cw` from the phone's own
connection, no browser opened: video f137 (15.86 MiB, h264 1080x1920) + audio f140 (731 KiB, aac),
merged to MP4, then a lossless Photos-safe copy (streams copied, no re-encode).
Screenshot: project folder `protocol/v61-20261030/evidence/A45-iphone-cinema-c-dYrEeavC3cw.png` (not committed: 937 KB).

**Rule: on iPhone, YouTube downloads go through Cinema C (`c "<url>"`). On Mac/PC: `yt_get.sh` or Zajil.
From a cloud sandbox: never, hand the URL to the user's device.**

## Chain

1. `yt-dlp` plain (deno or node installed: YouTube requires a JS runtime since 2025).
2. `yt-dlp` with the user's own cookies: `YT_BROWSER=chrome` or `YT_COOKIES=cookies.txt`.
3. `yt-dlp -U`, then 1 and 2 again.
On failure it prints the fix and writes `receipt.json` with `"ok": false`.

## One-time setup on the device

```bash
python3 -m pip install -U "yt-dlp[default]"
brew install ffmpeg deno          # Mac;  on Windows: winget install ffmpeg DenoLand.Deno
```

## Use

```bash
bash yt_get.sh "https://www.youtube.com/watch?v=dYrEeavC3cw"
YT_QUALITY=720 bash yt_get.sh "<url>" ./clips
YT_BROWSER=chrome bash yt_get.sh "<url>"      # if YouTube asks for login
YT_AUDIO=1 bash yt_get.sh "<url>"             # audio only
```

iPhone: Cinema C (`cinema-c/Cinema_C_V35_iPhone.sh` (in the project folder, not this repo)) already wraps yt-dlp with cookies support.

## Gate

PASS = `receipt.json` has `"ok": true`, `bytes > 0`, and a duration close to the source.

Only download videos you own or have permission to reuse.

## GUI alternative: Zajil (زاجِل)

https://github.com/motalim-ai/zajil-download-manager — free, open source (GPL-3.0), Arabic-first,
Windows / macOS / Linux. It runs the same engine inside (a pinned, signature-checked yt-dlp plus
QuickJS as the JS runtime), adds a browser button over YouTube videos, resume, queues and playlists.
Use it on the device when a click-to-download app is easier than the script. It has the same
limit: it works from a home connection, not from a cloud sandbox.
`yt_get.sh` also accepts QuickJS (`qjs`) as the JS runtime, borrowed from Zajil.
