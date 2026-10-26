# مصادر «استوديو الصوت التفاعلي والترجمة المتحركة» من الأطلس

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

## whisper (2760-charly-tools)

- الترخيص: **MIT**  ·  الأصل: https://github.com/opencharly/marketplace/tree/d87e6f94bba069eaf7f4a8e68cbd669b5a8d7aeb/tools
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2760-charly-tools/10941-whisper
- الوصف: OpenAI Whisper local speech-to-text. Use when working with the whisper candy.

```markdown
# whisper -- OpenAI Whisper STT

## Candy Properties

| Property | Value |
|----------|-------|
| Install files | `charly.yml`, `pixi.toml` |
| Depends | `python`, `cuda`, `ffmpeg` |

## Usage

```yaml
# box charly.yml — compose the candy as an inline list in the box body
my-box:
  candy:
    base: fedora
    candy: [whisper]
```

## Used In Boxes


## Related Candies

- `/charly-languages:python` — Python runtime — required dependency
- `/charly-distros:cuda` — CUDA toolkit — required dependency
- `/charly-selkies:ffmpeg` — FFmpeg multimedia (nonfree codecs) — required dependency
- `/charly-tools:sherpa-onnx` — alternative STT engine (ONNX-based, lighter weight)

## When to Use This Skill

Use when the user asks about:
- Speech-to-text in containers
- OpenAI Whisper setup
- Audio transcription with CUDA
- The `whisper` candy

## Related

- `/charly-image:layer` — candy authoring reference (`charly.yml` schema, plan-step verbs, service declarations)
- `/charly-check:check` — declarative testing (`check:` block, `charly check box`, `charly check live`)
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

## fetch-tiktok-mentions (886-intel)

- الترخيص: **MIT**  ·  الأصل: https://github.com/blockchainian/claude/tree/0e53403fa614c5162b54ed0149cb7720ca1414a9/plugins/intel
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/886-intel/1989-fetch-tiktok-mentions
- الوصف: Fetch a brand's TikTok videos from hashtag pages, user pages and keyword searches into docs/intel/tiktok/<slug>/ — full video metadata (videos.jsonl), each video's comments with replies (comments/<id>.jsonl) and the video files (~/.local/share/tiktok/<id>.mp4, outside the repo) — through anonymous Camoufox sessions on the ISP proxy pool, plus the logged-in TikTok account of the secrets-manager sto

```markdown
# Fetch TikTok mentions

Hashtag pages, user profiles, keyword searches, comments and video files.
TikTok has no "everything about a brand" view, so coverage is the union of the sources you give.
Everything is fetched anonymously except keyword searches and user timelines, which go through
the logged-in account (see "The account").

Run from the repo root.

```
node \
  "${CLAUDE_PLUGIN_ROOT}/skills/fetch-tiktok-mentions/scripts/fetch-tiktok-mentions.mjs" \
  <slug> [--hashtag <name>]... [--user <handle>]... [--keyword <words>]... \
  [--hashtag-min-plays <n>] \
  [--source-limit <n>] [--comment-limit <n>] [--sessions <n>] [--rate <n>] [--concurrency <n>] [--no-comments] [--no-download]
```

- `slug` names the output dir `docs/intel/tiktok/<slug>/`.
- `--hashtag` and `--user` are repeatable; a name, `#tag` / `@handle`, or the tiktok.com url all work.
  The sources are saved, so a rerun needs only the slug; sources given later are added.
- `--keyword` is repeatable too: the words of one TikTok video search (quote several words). The
  search covers captions, on-screen text, hashtags and speech, so it also finds videos that mention
  the brand without its hashtag. It needs the account.
- `--hashtag-min-plays` (default 10000) drops a hashtag page's videos below that many plays. A
  user's videos and a keyword's results have no floor.
- Only English videos are kept, from every source: TikTok's `textLanguage` must be `en` or `un`
  (a caption it could not tell, in practice hashtags alone).
- `--source-limit` caps the videos one pull of a source yields (default 1000).
- `--comment-limit` caps the comments kept per video, top-level and replies together (default 1000).
  Every top-level comment is taken first; the room left goes to replies, the most liked and
  replied threads first, a page (20) per thread in turn.
- `--sessions` is how many browser sessions work at once, one per ISP slot (default: every slot).
- `--rate` is how many requests one session starts per second (default 20); `--concurrency` how many
  it may have in flight (default 12). File downloads run 4 per session: they share the slot's
  bandwidth, more only time out.
- `--no-comments` / `--no-download` skip a phase.

Invented example (Demo Fun):

```
node \
  "${CLAUDE_PLUGIN_ROOT}/skills/fetch-tiktok-mentions/scripts/fetch-tiktok-mentions.mjs" \
  demofun --hashtag demofun --hashtag demodotfun --user demo.fun --keyword "demo fun"
```

Every run does three things: collects every source (a hashtag through four sessions at once, see below; new videos are
added, held ones get fresh stats), fetches comments for the videos whose comments are not
complete, and downloads the videos without a file. Launch it in the background and reread the
log. **Rerun the same command until it exits 0.**
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
