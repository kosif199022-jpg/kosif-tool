# مصادر «المونتير المحترف بالكود (ffmpeg)» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

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

## losslesscut (235-mas-video-lab)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alivirgo/major-ai-skills/tree/ba3a5729d60646626fee31c2d9906adc59f418dc/plugins/mas-video-lab
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/235-mas-video-lab/756-losslesscut
- الوصف: Trim and join media with LosslessCut, inspect keyframe boundaries, and choose between stream copying and smart-cut rendering.

```markdown
# LosslessCut Stream Editor AI Skill Guide (Claude)

## Overview & Engine Architecture
LosslessCut is a fast, lossless video, audio, and subtitle trimming application powered by an Electron frontend and **FFmpeg stream-copying (`-c copy`)** engine. Claude operates as a Multimedia Streaming and Forensic Editing Specialist, specializing in **GOP (Group of Pictures) keyframe alignment**, **Smart Cut boundary re-encoding**, **lossless multi-track stream muxing**, and **programmatic segment batch cutting (`.llc` JSON format)**.

### Lossless Stream Copying & GOP Engine

```
┌─────────────────────────────────────────────────────────────┐
│                 LosslessCut Stream Processing               │
│                                                             │
│  GOP (Group of Pictures) Keyframe Architecture              │
│  [ I-Frame (IDR) ] ─── [ B-Frame ] ─── [ P-Frame ] ─── [ I-Frame ]│
│        ▲                                                     │
│        └── Safe Lossless Cut Point (No Re-encoding Needed)   │
│                                                             │
│  Cut Modes & Engine Mechanics                               │
│  ├── Keyframe Cut Mode (Fastest, snaps to nearest I-frame)  │
│  ├── Smart Cut Mode (Re-encodes strictly boundary GOPs)     │
│  └── Multi-Track Stream Preservation (Extract / Merge Audio)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Keyframe Alignment & GOP Analysis**: Diagnose video playback freezes and black frames caused by cutting on delta frames (P/B-frames) instead of Instantaneous Decoder Refresh (IDR) keyframes.
2. **Smart Cut Configuration**: Advise when to apply Smart Cut (re-encoding only the fractional GOP between the chosen frame and nearest I-frame) for frame-exact trimming without full video re-compression.
3. **Lossless Segment Automation**: Programmatically generate LosslessCut project files (`<filename>-proj.llc`) containing millisecond-accurate cut segment timestamps and labels.
4. **Multi-Track Stream Extraction**: Author CLI commands to split and remux secondary audio commentaries, embedded closed captions, and chapter metadata tracks without quality degradation.

---

## Production Python Automation: Exact Keyframe Slicer Tool

Save this script as `keyframe_slicer.py` to inspect input video packets via `ffprobe`, locate exact IDR keyframes, and slice video losslessly with guaranteed zero freeze frames:

```python
"""
Lossless Video Slicer: Exact Keyframe Alignment
Analyzes packet keyflags via ffprobe to guarantee freeze-free -c copy cutting.
"""

import sys
import os
import subprocess
import json

def get_nearest_keyframe(file_path: str, target_time_sec: float) -> float:
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

## low-latency-live-streaming (2387-streaming-media-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/streaming-media-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2387-streaming-media-engineering/9240-low-latency-live-streaming
- الوصف: Hit a live-streaming latency target: pick the approach (standard HLS/DASH, LL-HLS/LL-DASH with chunked CMAF, or WebRTC for sub-second/interactive) from the required end-to-end latency and scale, then budget latency across capture/encode, segment & part duration, chunked transfer, live origin, CDN, and the player live-edge buffer — trading latency against rebuffer risk deliberately. Protocol/latenc

```markdown
# Low-Latency Live Streaming

The discipline of hitting a live latency target without trading it for rebuffering. The required end-to-end latency and the concurrency you must serve pick the approach; the latency is then spent across the whole chain, not just the player.

> **Engineering judgment.** Protocol latency floors, chunked-transfer support, and player live-edge behavior move with spec and SDK versions — every latency number and support claim here is `[verify-at-use]`. No PII.

## Workflow

1. **State the required end-to-end latency and scale.** "Glass-to-glass" seconds and peak concurrency decide the approach; sub-second interactive is a different architecture from few-second live.
2. **Pick the approach.** Standard HLS/DASH (highest latency, cheapest at scale), LL-HLS / LL-DASH with chunked CMAF (few-second, CDN-scalable), or WebRTC (sub-second, interactive, harder to scale). Name the trade — lower latency costs scale and robustness.
3. **Budget latency across the chain.** Capture/encode, segment + part duration, chunked transfer, live origin/packager, CDN delivery, and the player's live-edge target buffer each add latency. Attack the biggest term, not the easiest.
4. **Tune the client and edge together.** A player chasing the live edge too hard trades latency for rebuffering; the edge must support chunked/partial-segment delivery. Tune both against the QoE targets from `playback-qoe-and-delivery`.
5. **Validate under real network + scale.** Low-latency live degrades fastest on poor networks and at peak concurrency — measure glass-to-glass and rebuffer together, not in isolation.

## Metrics table

| Metric | Target/read | Flag |
|---|---|---|
| Glass-to-glass latency (s) | Meets the stated target | `[verify-at-use]` per approach |
| Segment / part duration (s) | Small enough for the target, big enough for cache | `[verify-at-use]` |
| Live-edge rebuffer ratio | Low at target latency | `[ESTIMATE]` |
| CDN chunked-transfer support | Required for LL-HLS/LL-DASH | `[verify-at-use]` per CDN |
| Peak concurrency the approach holds | Within scale budget | `[verify-at-use]` |

## Anti-patterns

- Choosing WebRTC for one-way live at massive scale because it's lowest latency — paying interactive cost you don't need.
- Chasing the live edge so hard the player rebuffers on any jitter.
- Cutting segment duration without confirming CDN chunked-transfer support.
- Measuring latency on a perfect network and ignoring rebuffer at the edge.

## See also

- Traverse the **low-latency approach** tree in [`../../knowledge/streaming-decision-trees.md`](../../knowledge/streaming-decision-trees.md).
- Dated protocol/latency landscape: [`../../knowledge/streaming-reference-2026.md`](../../knowledge/streaming-reference-2026.md).
```

## streaming-architecture-and-protocol-selection (2387-streaming-media-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/streaming-media-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2387-streaming-media-engineering/9242-streaming-architecture-and-protocol-sele
- الوصف: Choose VOD vs live and the streaming protocol (HLS / MPEG-DASH / CMAF / LL-HLS / WebRTC) on the use-case, latency target, and device/browser reach — then commit to a packaging format (CMAF hedge), an origin/edge design, a single-vs-multi-CDN strategy, and the multi-DRM matrix (Widevine / FairPlay / PlayReady) the reach implies. Protocol/DRM/CDN specifics verify-at-use.

```markdown
# Streaming Architecture & Protocol Selection

The first and most expensive streaming decision: VOD vs live, the protocol, the packaging, the CDN, and the DRM. Everything downstream — the encoding ladder, the players, the latency the audience feels, the egress bill — is shaped by this choice, so make it deliberately.

> **Engineering judgment, protocol/DRM landscape is volatile.** Protocol support, DRM system reach, and CDN features change with browser, OS, and vendor releases. Every specific here is `[verify-at-use]` — confirm against the spec/vendor docs before it drives a build commitment. Not legal/DRM-licensing advice. No PII.

## Workflow

1. **State the use-case and the reach.** On-demand catalog, live linear, or interactive/real-time — and the device/browser matrix the audience actually uses. These fix the constraints.
2. **Decide VOD vs live, then the latency target.** For live, the required end-to-end latency (standard / low-latency / real-time) dominates the protocol choice more than anything else.
3. **Pick the protocol on latency + reach.** HLS (broadest reach, Apple-native), DASH (open, non-Apple), CMAF (shared-fragment hedge for both), LL-HLS/LL-DASH (few-second live), WebRTC (sub-second interactive). Name the trade.
4. **Decide DRM + packaging early.** Map reach to the multi-DRM matrix (Widevine / FairPlay / PlayReady) and package once (CMAF/CENC) to serve them. Retrofitting encryption is a rebuild.
5. **Design origin/edge and the CDN strategy.** Origin + mid-tier/shield + edge for cache-hit and cost; single-CDN (simple) vs multi-CDN (resilience/leverage at cost). Hand the ABR-ladder philosophy to `transcoding-and-abr-ladder`.

## Metrics table

| Decision input | What it tells you | Flag |
|---|---|---|
| Required end-to-end latency (s) | Standard vs low-latency vs real-time protocol | `[verify-at-use]` per protocol |
| Device/browser reach matrix | Which DRM systems + codecs are mandatory | `[verify-at-use]` |
| VOD vs live + concurrency | Origin/edge design and egress scale | `[verify-at-use]` |
| DRM reach (Widevine/FairPlay/PlayReady) | Packaging + key-delivery architecture | `[verify-at-use]` |
| CDN cache-hit ratio target | Single vs multi-CDN, shield tier, cost | `[ESTIMATE]` `[verify-at-use]` |

## Anti-patterns

- Choosing WebRTC for a one-way catalog because "it's lowest latency" — paying real-time cost for latency you don't need.
- Forking HLS and DASH packaging instead of hedging with CMAF.
- Deferring the DRM matrix until after packaging, then re-encrypting.
- Assuming single-CDN scales to launch concurrency without a failover plan.

## See also

- Traverse the **VOD vs live** and **protocol choice** trees in [`../../knowledge/streaming-decision-trees.md`](../../knowledge/streaming-decision-trees.md).
```

## joined-audio-transcript-drift (3323-joined-audio-transcript-drift)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/joined-audio-transcript-drift
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift
- الوصف: Keep timestamps aligned when joining many audio files into one. Use when: (1) subtitles, transcript segments, chapters or bookmarks drift later and later through a concatenated file; (2) the joined file is seconds longer than the sum of its parts; (3) ffmpeg's concat demuxer prints "Application provided invalid, non monotonically increasing dts to muxer"; (4) you are stitching TTS chunks, per-chap

```markdown
# Joined audio drifts away from its transcript

> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/joined-audio-transcript-drift/SKILL.md`).

## Problem

You join many audio pieces into one file and build a transcript, a chapter
list or a set of bookmarks by adding up each piece's duration. Early
timestamps look right. Later ones point at the wrong place, by more the
further in you go.

The cause is that a compressed piece is longer than the audio it represents.
An encoder pads the start and end of every file, and records in a header how
much to trim. `ffprobe` reports the *trimmed* duration, which is what a player
would give you, but `concat -c copy` copies whole frames and keeps the padding
of every piece. Each join therefore adds a few tens of milliseconds that your
arithmetic never sees, and they accumulate.

Measured on 181 pieces joined into one 164-minute MP3: the joined file ran
**9.1 seconds longer** than the sum of the pieces, about 50 ms per join.

## Context / Trigger conditions

- Timestamps are correct at the start of a joined file and progressively later
  toward the end.
- The joined file's duration is longer than the sum of the parts' durations.
- ffmpeg prints, during a copy-mode concat:
  `Application provided invalid, non monotonically increasing dts to muxer in stream 0`
- You are stitching synthesized speech chunks, per-chapter or per-track
  downloads, or recorded segments, and something downstream needs to seek by
  time: captions, bookmarks, chapter marks, alignment.

## Solution

### Do not trust frame counts either

The obvious repair is to compute each piece's contribution from its frame
count rather than its trimmed duration:

```bash
ffprobe -v error -select_streams a:0 -count_frames \
  -show_entries stream=nb_read_frames,sample_rate -of json piece.mp3
```

For MPEG-2 Layer III (sample rates 16/22.05/24 kHz) a frame is 576 samples;
for MPEG-1 (32/44.1/48 kHz) it is 1152. This gets closer but still does not
match: each input's header frame (Xing/Info/LAME) is copied through as well,
so the joined file carries roughly one extra frame per piece. On the same
29-minute test the frame arithmetic was still 1.3 seconds out.

### Encode once, and the arithmetic holds

Decoding everything and encoding the result once produces a single contiguous
stream whose length is the sum of the decoded pieces:

```bash
ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i list.txt \
  -c:a libmp3lame -b:a 64k -ar 24000 -ac 1 -write_xing 0 joined.mp3
```

On the same material this brought 2.51 seconds of drift down to **0.06
seconds**, and took 6 seconds for a 29-minute file. `-write_xing 0` keeps the
output from gaining a header frame of its own.
```
