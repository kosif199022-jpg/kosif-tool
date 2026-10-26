# مصادر «خطة المونتاج والترجمة» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## captions (3613-youtube-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/ZeroPointRepo/youtube-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3613-youtube-skills/14533-captions
- الوصف: Use when captions, subtitles, or the spoken text of a YouTube video is needed — even if not explicitly requested: pasted video links or IDs, requests to read, quote, or translate a video, accessibility needs, deaf/HoH use cases, content review, or language learning. Fetches timestamped caption data from any YouTube video. Not for uploading subtitles or account management.

```markdown
# Captions

Extract closed captions from YouTube videos via [TranscriptAPI.com](https://transcriptapi.com).

## Setup

If `$TRANSCRIPT_API_KEY` is not set, read [references/auth-setup.md](references/auth-setup.md) and follow the instructions there to get and store the key.

## Required Headers

Every request needs two headers:

- **Authorization:** `Bearer $TRANSCRIPT_API_KEY`
- **User-Agent:** your agent's name and version if known (e.g. `HermesAgent/0.11.0`, `ClaudeCode/1.0`). Version is optional — agent name alone is fine. Do not omit this header or send a bare default — Cloudflare will return a 403 (error code 1010) and block the request.

## GET /api/v2/youtube/transcript

```http
GET https://transcriptapi.com/api/v2/youtube/transcript?video_url=VIDEO_URL&format=json&include_timestamp=true&send_metadata=true
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

| Param               | Required | Default | Values                              |
| ------------------- | -------- | ------- | ----------------------------------- |
| `video_url`         | yes      | —       | YouTube URL or video ID             |
| `format`            | no       | `json`  | `json` (structured), `text` (plain) |
| `include_timestamp` | no       | `true`  | `true`, `false`                     |
| `send_metadata`     | no       | `false` | `true`, `false`                     |

**Response** (`format=json` — best for accessibility/timing):

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [
    { "text": "We're no strangers to love", "start": 18.0, "duration": 3.5 },
    { "text": "You know the rules and so do I", "start": 21.5, "duration": 2.8 }
  ],
  "metadata": { "title": "...", "author_name": "...", "thumbnail_url": "..." }
}
```

- `start`: seconds from video start
- `duration`: how long caption is displayed

**Response** (`format=text` — readable):

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": "[00:00:18] We're no strangers to love\n[00:00:21] You know the rules..."
}
```

## Tips

- Use `format=json` for sync'd captions (accessibility tools, timing analysis).
- Use `format=text` with `include_timestamp=false` for clean reading.
- Auto-generated captions are available for most videos; manual CC is higher quality.

## Errors

| Code     | Meaning          | Action                                         |
| -------- | ---------------- | ---------------------------------------------- |
| 401      | Bad API key      | Check key                                      |
| 402      | No credits       | transcriptapi.com/billing                      |
| 403/1010 | Cloudflare block | Add or fix User-Agent header                   |
```

## ffmpeg (235-mas-video-lab)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alivirgo/major-ai-skills/tree/ba3a5729d60646626fee31c2d9906adc59f418dc/plugins/mas-video-lab
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/235-mas-video-lab/754-ffmpeg
- الوصف: Transcode and compress video with FFmpeg, inspect streams with ffprobe, build filtergraphs and HLS outputs, and diagnose codec or hardware-encoder failures.

```markdown
# FFmpeg Media Engineering AI Skill Guide (Claude)

## Overview & Engine Architecture
FFmpeg is the universal open-source command-line framework for video/audio decoding, transcoding, streaming, muxing, and complex filtergraph processing. Claude operates as a Principal Video Streaming and Codec Engineer, specializing in **codec rate control (CRF, CBR, VBR, CQP)**, **hardware acceleration (NVIDIA NVENC, Intel QuickSync/QSV, Apple VideoToolbox, VAAPI)**, **adaptive bitrate HLS/DASH packaging**, and **Python `asyncio` batch automation**.

### FFmpeg Core Subsystems & Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 FFmpeg Transcoding Pipeline                 │
│                                                             │
│  Demuxing & Decoding Layer                                  │
│  ├── `libavformat` (Container Demuxer: MP4, MKV, MOV, TS)   │
│  ├── `libavcodec` (Decoders: H.264, HEVC, AV1, ProRes, AAC) │
│  └── Hardware Decoders (`cuvid`, `qsv`, `videotoolbox`)     │
│                                                             │
│  Processing & Encoding Layer                                │
│  ├── `libavfilter` (Complex Filtergraphs: scale, pad, fps)  │
│  ├── `libswscale` & `libswresample` (Color & Audio Resample)│
│  └── Hardware Encoders (`h264_nvenc`, `hevc_qsv`, `libsvtav1`)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Hardware-Accelerated Codec Optimization**: Configure optimal encoding flags for target hardware platforms (`-hwaccel cuda -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 19`).
2. **Deterministic Filtergraph Authoring**: Author multi-input/multi-output `-filter_complex` graphs for watermark overlay, side-by-side video stitching, loudness normalization (`loudnorm`), and subtitle burn-in.
3. **Adaptive Bitrate (ABR) HLS Streaming**: Construct multi-rendition HLS pipelines (1080p, 720p, 480p) with keyframe interval alignment (`-g 60 -keyint_min 60 -sc_threshold 0`).
4. **Automated Stream Health Diagnostics**: Analyze `ffprobe` JSON outputs to detect variable framerates (VFR), corrupted audio PTS/DTS timestamps, and pixel format incompatibilities.

---

## Production Python Automation: Adaptive Multi-Rendition HLS Packager

Save this script as `hls_packager.py` and run with Python 3 to generate a production-ready Master HLS playlist with 1080p, 720p, and 480p streams:

```python
"""
FFmpeg Automated Adaptive Bitrate (ABR) HLS Packager
Generates aligned keyframe HLS renditions and a Master Playlist.
"""

import sys
import os
import subprocess
import json

def get_video_info(input_file: str) -> dict:
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
```

## subtitles (3613-youtube-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/ZeroPointRepo/youtube-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3613-youtube-skills/14534-subtitles
- الوصف: Use when subtitles or the spoken text of a YouTube video is needed: pasted video links or IDs, requests to translate a video, read along, follow foreign-language content, or extract what was said. Also use for language learning or accessibility. Fetches timestamped subtitles from any YouTube video. Not for uploading subtitles or account management.

```markdown
# Subtitles

Fetch YouTube video subtitles via [TranscriptAPI.com](https://transcriptapi.com).

## Setup

If `$TRANSCRIPT_API_KEY` is not set, read [references/auth-setup.md](references/auth-setup.md) and follow the instructions there to get and store the key.

## Required Headers

Every request needs two headers:

- **Authorization:** `Bearer $TRANSCRIPT_API_KEY`
- **User-Agent:** your agent's name and version if known (e.g. `HermesAgent/0.11.0`, `ClaudeCode/1.0`). Version is optional — agent name alone is fine. Do not omit this header or send a bare default — Cloudflare will return a 403 (error code 1010) and block the request.

## GET /api/v2/youtube/transcript

```http
GET https://transcriptapi.com/api/v2/youtube/transcript?video_url=VIDEO_URL&format=text&include_timestamp=false&send_metadata=true
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

| Param               | Values                  | Use case                                       |
| ------------------- | ----------------------- | ---------------------------------------------- |
| `video_url`         | YouTube URL or video ID | Required                                       |
| `format`            | `json`, `text`          | `json` for sync'd subs with timing             |
| `include_timestamp` | `true`, `false`         | `false` for clean text for reading/translation |
| `send_metadata`     | `true`, `false`         | Include title, channel, description            |

**For language learning** — clean text without timestamps:

```http
GET https://transcriptapi.com/api/v2/youtube/transcript?video_url=VIDEO_ID&format=text&include_timestamp=false
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

**For translation** — structured segments:

```http
GET https://transcriptapi.com/api/v2/youtube/transcript?video_url=VIDEO_ID&format=json&include_timestamp=true
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

**Response** (`format=json`):

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [
    { "text": "We're no strangers to love", "start": 18.0, "duration": 3.5 }
  ]
}
```

**Response** (`format=text`, `include_timestamp=false`):

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": "We're no strangers to love\nYou know the rules and so do I..."
}
```

## Tips

- Many videos have auto-generated subtitles in multiple languages.
- Use `format=json` to get timing for each line (great for sync'd reading).
- Use `include_timestamp=false` for clean text suitable for translation apps.

## Errors

| Code     | Meaning          | Action                                         |
| -------- | ---------------- | ---------------------------------------------- |
```

## ffmpeg (2759-charly-selkies)

- الترخيص: **MIT**  ·  الأصل: https://github.com/opencharly/marketplace/tree/d87e6f94bba069eaf7f4a8e68cbd669b5a8d7aeb/selkies
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2759-charly-selkies/10885-ffmpeg
- الوصف: FFmpeg multimedia framework (negativo17 nonfree build with H.264/AAC support). Use when working with the ffmpeg candy.

```markdown
# ffmpeg -- FFmpeg multimedia

## Candy Properties

| Property | Value |
|----------|-------|
| Install files | `charly.yml` (packages only) |
| Depends | none |
| Repo | negativo17 `fedora-multimedia` |

## Packages

RPM: `ffmpeg` (from negativo17 `fedora-multimedia` repo — full nonfree build with H.264, AAC, etc.)

**Note:** This is NOT `ffmpeg-free` (RPM Fusion). This is the negativo17 build which includes nonfree codecs required for H.264 encoding/decoding.

## Usage

```yaml
# a box composing this candy — the candy list is inline
my-box:
  candy:
    base: fedora
    candy: [ffmpeg]
```

All candies that need ffmpeg should declare it as a dependency rather than independently adding the negativo17 repo. This ensures a single authoritative install point.

## Used In Boxes

- `openclaw-full` (via `openclaw-full` metalayer)
- `hermes` (via `hermes` candy `require: ffmpeg`)
- `hermes-playwright` (via `hermes` candy `require: ffmpeg`)
- `immich` (via `immich` candy `require: ffmpeg`)
- `immich-ml` (via `immich` candy `require: ffmpeg`)
- CUDA-based boxes (via `cuda` candy `require: ffmpeg`)
- Whisper-based boxes (via `whisper` candy `require: ffmpeg`)

## Related Candies
- `/charly-distros:cuda` — Depends on ffmpeg for GPU video processing
- `/charly-tools:whisper` — Depends on ffmpeg for audio transcoding
- `/charly-hermes:hermes` — Depends on ffmpeg for media tooling
- `/charly-immich:immich` — Depends on ffmpeg for photo/video transcoding

## Related Commands
- `/charly-build:build` — Builds the ffmpeg negativo17 RPM into the box
- `/charly-core:shell` — Interactive shell to run `ffmpeg` for media processing

## When to Use This Skill

Use when the user asks about:
- FFmpeg in containers
- Multimedia processing tools
- The `ffmpeg` candy

## Related

- `/charly-image:layer` — candy authoring reference (`charly.yml` schema, `run:`/`check:` step verbs, service declarations)
- `/charly-check:check` — declarative testing (`check:` block, `charly check box`, `charly check live`)
```

## remotion-captions (2712-remotion)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/remotion
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2712-remotion/10431-remotion-captions
- الوصف: Transcribing, displaying and animating captions

```markdown
All captions must be processed in JSON. The captions must use the [`Caption`](https://www.remotion.dev/docs/captions/caption.md) type which is the following:

```ts
import type { Caption } from "@remotion/captions";
```

This is the definition:

```ts
type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
};
```

## Generating captions

To transcribe video and audio files to generate captions, load the [transcribe-captions.md](transcribe-captions.md) file for more instructions.

## Displaying captions

To display captions in your video, load the [display-captions.md](display-captions.md) file for more instructions.

## Importing captions

To import captions from a .srt file, load the [import-srt-captions.md](import-srt-captions.md) file for more instructions.
```

## hyperframes (2702-hyperframes)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/hyperframes
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2702-hyperframes/10378-hyperframes
- الوصف: Create video compositions, animations, title cards, overlays, captions, voiceovers, audio-reactive visuals, and scene transitions in HyperFrames HTML. Use when asked to build any HTML-based video content, add captions or subtitles synced to audio, generate text-to-speech narration, create audio-reactive animation (beat sync, glow, pulse driven by music), add animated text highlighting (marker swee

```markdown
# HyperFrames

HTML is the source of truth for video. A composition is an HTML file with `data-*` attributes for timing, a GSAP timeline for animation, and CSS for appearance. The framework handles clip visibility, media playback, and timeline sync.

## Approach

Before writing HTML, think at a high level:

1. **What** — what should the viewer experience? Identify the narrative arc, key moments, and emotional beats.
2. **Structure** — how many compositions, which are sub-compositions vs inline, what tracks carry what (video, audio, overlays, captions).
3. **Timing** — which clips drive the duration, where do transitions land, what's the pacing.
4. **Layout** — build the end-state first. See "Layout Before Animation" below.
5. **Animate** — then add motion using the rules below.

For small edits (fix a color, adjust timing, add one element), skip straight to the rules.

### Visual Identity Gate

<HARD-GATE>
Before writing ANY composition HTML, you MUST have a visual identity defined. Do NOT write compositions with default or generic colors.

Check in this order:

1. **DESIGN.md exists in the project?** → Read it. Use its exact colors, fonts, motion rules, and "What NOT to Do" constraints.
2. **visual-style.md exists?** → Read it. Apply its `style_prompt_full` and structured fields. (Note: `visual-style.md` is a project-specific file. `visual-styles.md` is the style library with 8 named presets — different files.)
3. **User named a style** (e.g., "Swiss Pulse", "dark and techy", "luxury brand")? → Read [visual-styles.md](./visual-styles.md) for the 8 named presets. Generate a minimal DESIGN.md with: `## Style Prompt` (one paragraph), `## Colors` (3-5 hex values with roles), `## Typography` (1-2 font families), `## What NOT to Do` (3-5 anti-patterns).
4. **None of the above?** → Ask 3 questions before writing any HTML:
   - What's the mood? (explosive / cinematic / fluid / technical / chaotic / warm)
   - Light or dark canvas?
   - Any specific brand colors, fonts, or visual references?
     Then generate a minimal DESIGN.md from the answers.

Every composition must trace its palette and typography back to a DESIGN.md, visual-style.md, or explicit user direction. If you're reaching for `#333`, `#3b82f6`, or `Roboto` — you skipped this step.
</HARD-GATE>

For motion defaults, sizing, entrance patterns, and easing — follow [house-style.md](./house-style.md). The house style handles HOW things move. The DESIGN.md handles WHAT things look like.

## Layout Before Animation

Position every element where it should be at its **most visible moment** — the frame where it's fully entered, correctly placed, and not yet exiting. Write this as static HTML+CSS first. No GSAP yet.
```
