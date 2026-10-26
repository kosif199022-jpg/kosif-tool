# مصادر «الصور المصغّرة وتصاميم السوشيال» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## creator-thumbnail-agent (3067-youtube)

- الترخيص: **MIT**  ·  الأصل: https://github.com/sleestk/skills-pipeline/tree/cd75a3875f3b467fa5747ef71d334e1c79b83918/YouTube
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3067-youtube/13228-creator-thumbnail-agent
- الوصف: Thumbnail Agent for [Channel]'s YouTube production pipeline. Acts as [Creator]'s First Impression Architect - takes the completed Script, SEO package, Visual Director Brief, and Editor Brief and generates a full Thumbnail Creative Brief with 3 concept directions, a recommended concept, Nano Banana 2 image generation prompts, production notes for [Creator], and an A/B test recommendation if applica

```markdown
# Thumbnail Agent — First Impression Architect

You are the Thumbnail Agent for [Channel]'s YouTube production pipeline. Your job is to stop the scroll for the Builder Avatar and make them think: **"I need to know what [Creator] found at the frontier and how it applies to what I'm building."**

---

## The Builder Avatar (Your Only Audience)

The Builder Avatar is scrolling YouTube. They see 20 thumbnails in 5 seconds. Yours must create a specific thought — not "that looks cool," not "that person seems popular" — but: *"I need to know what [Creator] found and how it applies to what I'm building."*

Design exclusively for this person. Ignore everyone else.

---

## Brand Non-Negotiables (Never Break These)

- **Dark/minimal, high contrast, tech-forward.** Black or very dark backgrounds only.
- **Cyan (#00D4FF) or white as accent colors.** Never more than one accent color per thumbnail.
- **Never cluttered.** Every element earns its place or gets cut.
- **[Creator]'s face is always in long-form thumbnails.** Real face, real expression. Not the AI UGC avatar (that's for Shorts distribution only).
- **Expression categories:** Discovery (slight smirk + direct eye contact), Verdict (arms crossed, direct camera stare), or Intensity (leaning forward, focused). Never hype. Never shock-face. Builder energy only.
- **Maximum 4 words of text.** Less is more. The text works *with* the image, not over it.
- **The [Brand Mascot]** appears in select thumbnails as a brand recognition element. Flag whether this video warrants its inclusion.

---

## Your Inputs

When this skill triggers, pull from all available upstream agent outputs:
- **Script** — theme, core argument, emotional arc
- **SEO Agent** — Thumbnail Text Brief (2–4 power words) and recommended title
- **Visual Director Brief** — tone, visual language, color treatment notes
- **Editor Brief** — Thumbnail Pull (best frame from the video)

If any upstream output is missing, work with what's available and note the gap.

---

## Your Output — Thumbnail Creative Brief

Deliver everything below, in order. Also save the full brief as a `.md` file for [Creator]'s records.

---

### 1. CONCEPT DIRECTION (3 Options)

For each of the three concepts, provide all of the following:

**Layout Description**
Where is [Creator] in frame (left, right, center)? What is behind or beside him (tech visual, terminal, diagram, abstract environment)? Where does the text sit? What visual hierarchy does the eye follow?

**Expression Direction**
Exactly what should [Creator]'s face communicate? Give a specific direction — e.g., *"Slight smirk, direct eye contact — 'I found something you don't know yet.'"* or *"Arms crossed, straight into camera — 'Here's the verdict.'"*

**Text Placement and Wording**
```

## youtube-search (3613-youtube-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/ZeroPointRepo/youtube-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3613-youtube-skills/14543-youtube-search
- الوصف: Use when the user wants to find YouTube content on any topic: searching for videos or channels, finding creators who cover a subject, discovering tutorials, talks, or expert discussions, or looking up a channel by name or handle. Also use proactively when the user wants to research a topic and YouTube is a good source. Not for account management or written-source-only research.

```markdown
# YouTube Search

Search YouTube and fetch transcripts via [TranscriptAPI.com](https://transcriptapi.com).

## Setup

If `$TRANSCRIPT_API_KEY` is not set, read [references/auth-setup.md](references/auth-setup.md) and follow the instructions there to get and store the key.

## Required Headers

Every request needs two headers:

- **Authorization:** `Bearer $TRANSCRIPT_API_KEY`
- **User-Agent:** your agent's name and version if known (e.g. `HermesAgent/0.11.0`, `ClaudeCode/1.0`). Version is optional — agent name alone is fine. Do not omit this header or send a bare default — Cloudflare will return a 403 (error code 1010) and block the request.

## API Reference

Full OpenAPI spec: [transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — consult this for the latest parameters and schemas.

## GET /api/v2/youtube/search — 1 credit/page

Search YouTube globally for videos, channels, playlists, or movies.

```http
GET https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=video&limit=20
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

| Param          | Required    | Default     | Validation                                                        |
| -------------- | ----------- | ----------- | ------------------------------------------------------------------ |
| `q`            | conditional | —           | 1-200 chars (trimmed), first page                                  |
| `type`         | no          | `video`     | `video`, `channel`, `playlist`, `movie` (first page)               |
| `sort`         | no          | `relevance` | `relevance` or `views` (first page)                                 |
| `upload_date`  | no          | —           | `hour`, `today`, `week`, `month`, `year` — videos, first page      |
| `duration`     | no          | —           | `short` (<4m), `medium` (4-20m), `long` (>20m) — videos, first page |
| `features`     | no          | —           | comma-separated: `hd`, `subtitles`, `cc`, `live`, `4k`, `hdr`, etc. |
| `limit`        | no          | `20`        | 1-50                                                                |
| `continuation` | conditional | —           | token from a previous response (subsequent pages)                  |

Provide exactly one of `q` (first page) or `continuation` (next pages) — the token already encodes the filters. `sort`/`upload_date`/`duration`/`features` apply to the first page only.

**Find recent, most-viewed videos:**

```http
GET https://transcriptapi.com/api/v2/youtube/search?q=innovation&sort=views&duration=long&upload_date=month
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

**Search for playlists on a topic:**

```http
GET https://transcriptapi.com/api/v2/youtube/search?q=react+tutorial&type=playlist
```

## youtube-full (194-youtube-full)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/marketing-skill/skills/youtube-full
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/194-youtube-full/619-youtube-full
- الوصف: Use when the user needs YouTube transcripts, video search, channel browsing, playlist extraction, or content monitoring. Trigger phrases: 'get the transcript for', 'search YouTube for', 'what are the latest videos on', 'list this playlist', 'monitor this channel', or any request involving a YouTube URL, video ID, or @handle. Do NOT use for downloading video or audio files, YouTube engagement data 

```markdown
# youtube-full — YouTube Transcripts, Search, and Channel Data

Covers transcript extraction, video search, channel browsing, in-channel search, playlist extraction, and new-upload monitoring via TranscriptAPI.

> **Source:** Ported from [ZeroPointRepo/youtube-skills](https://github.com/ZeroPointRepo/youtube-skills) (MIT). Original skill authored by ZeroPointRepo contributors. Adapted for the claude-skills format.

> **BYOK / free-tier note:** TranscriptAPI is a commercial service (BYOK — you bring your own key; 100 free credits included, no card required). For local/self-hosted extraction without an API key, use `youtube-transcript-api` (Python) or `yt-dlp` as OSS fallbacks. See [Anti-Patterns](#anti-patterns) for guidance.

## API Setup

Every request to `transcriptapi.com` requires two headers:

- `Authorization: Bearer $TRANSCRIPT_API_KEY`
- `User-Agent: ClaudeCode/1.0`

If `TRANSCRIPT_API_KEY` is not set, prompt the user to get a free key at `https://transcriptapi.com` (100 free credits, no card required) and store it as `TRANSCRIPT_API_KEY`.

## Operations

### Get transcript (1 credit)

```
GET https://transcriptapi.com/api/v2/youtube/transcript
  ?video_url={URL_OR_ID}&format=text&include_timestamp=true&send_metadata=true
```

Use this for any "get transcript", "summarize video", or "extract quotes" request.

### Search YouTube (1 credit)

```
GET https://transcriptapi.com/api/v2/youtube/search
  ?q={QUERY}&type=video&limit=20
```

Use this when the user wants to find videos on a topic. Follow with transcript calls on selected results.

### Channel — latest uploads (FREE)

```
GET https://transcriptapi.com/api/v2/youtube/channel/latest
  ?channel={@HANDLE_OR_ID}
```

Returns the 15 most recent uploads with view counts and publish timestamps. Use before fetching transcripts to check whether uploads are new.

### Channel — all videos (1 credit/page)

```
GET https://transcriptapi.com/api/v2/youtube/channel/videos
  ?channel={@HANDLE_OR_ID}
```

Paginate with `?continuation=TOKEN` on subsequent pages.

### In-channel search (1 credit)

```
GET https://transcriptapi.com/api/v2/youtube/channel/search
  ?channel={@HANDLE_OR_ID}&q={QUERY}&limit=30
```

Prefer this over broad YouTube search when the user already knows the channel.

### Playlist extraction (1 credit/page)

```
GET https://transcriptapi.com/api/v2/youtube/playlist/videos
  ?playlist={PLAYLIST_URL_OR_ID}
```

Paginate with `?continuation=TOKEN`. Response includes `playlist_info`, `results`, `has_more`.

### Resolve handle (FREE)

```
GET https://transcriptapi.com/api/v2/youtube/channel/resolve
  ?input={@HANDLE_OR_URL}
```

Returns `{"channel_id": "UC...", "resolved_from": "@handle"}`.

## Credit Costs Summary

| Endpoint           | Cost     |
|--------------------|----------|
```

## youtube-api (3613-youtube-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/ZeroPointRepo/youtube-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3613-youtube-skills/14538-youtube-api
- الوصف: Use when YouTube data is needed without Google API quotas or OAuth setup: transcripts, video metadata, channel info, search results, playlists. Triggers on pasted YouTube links, creator names, @handles, topic research, video summaries, channel browsing, or any request where YouTube content would help — even if not mentioned explicitly. Not for uploads, account management, or written-source-only re

```markdown
# YouTube API

YouTube data access via [TranscriptAPI.com](https://transcriptapi.com) — no Google API quota needed.

## Setup

If `$TRANSCRIPT_API_KEY` is not set, read [references/auth-setup.md](references/auth-setup.md) and follow the instructions there to get and store the key.

## Required Headers

Every request needs two headers:

- **Authorization:** `Bearer $TRANSCRIPT_API_KEY`
- **User-Agent:** your agent's name and version if known (e.g. `HermesAgent/0.11.0`, `ClaudeCode/1.0`). Version is optional — agent name alone is fine. Do not omit this header or send a bare default — Cloudflare will return a 403 (error code 1010) and block the request.

## API Reference

Full OpenAPI spec: [transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — consult this for the latest parameters and schemas.

## Endpoint Reference

All endpoints: `https://transcriptapi.com/api/v2/youtube/...`

Channel endpoints accept `channel` — an `@handle`, channel URL, or `UC...` ID. Playlist endpoints accept `playlist` — a playlist URL or ID.

| Endpoint                              | Method | Cost     |
| -------------------------------------- | ------ | -------- |
| `/info?video_url=ID`                   | GET    | **free** |
| `/video/metadata?video_url=ID`         | GET    | 1        |
| `/transcript?video_url=ID`             | GET    | 1        |
| `/search?q=QUERY&type=video`           | GET    | 1        |
| `/channel/resolve?input=@handle`       | GET    | **free** |
| `/channel/info?channel=@handle`        | GET    | 1        |
| `/channel/latest?channel=@handle`      | GET    | **free** |
| `/channel/videos?channel=@handle`      | GET    | 1/page   |
| `/channel/search?channel=@handle&q=Q`  | GET    | 1        |
| `/channel/playlists?channel=@handle`   | GET    | 1/page   |
| `/channel/posts?channel=@handle`       | GET    | 1/page   |
| `/channel/sections?channel=@handle`    | GET    | 1        |
| `/playlist/videos?playlist=PL_ID`      | GET    | 1/page   |

`search` also takes `type=playlist` or `type=movie`, plus first-page-only filters `sort` (`relevance`/`views`), `upload_date`, `duration`, and `features`. `channel/videos` takes `tab=videos` (default), `shorts`, or `streams`, plus an optional `sort` (`latest`/`popular`/`oldest`).

> **Naming:** `/video/metadata` was previously `/video/info`. The old path still works but is deprecated — use `/video/metadata`.

## Quick Examples

**Search videos:**

```http
GET https://transcriptapi.com/api/v2/youtube/search?q=python+tutorial&type=video&limit=10
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

**Get transcript:**

```http
GET https://transcriptapi.com/api/v2/youtube/transcript?video_url=dQw4w9WgXcQ&format=text&include_timestamp=true&send_metadata=true
```

## youtube-transcript (3190-youtube-transcript)

- الترخيص: **MIT**  ·  الأصل: https://github.com/taathub/claude-code/tree/8a9ec5c20e1e578a6024b3c62b0a94fca653dd61/plugins/youtube-transcript
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3190-youtube-transcript/13537-youtube-transcript
- الوصف: YouTube動画のリンクから文字起こし(トランスクリプト/スクリプト)を取得し、要約・詳細解説・全文をMarkdownファイルに書き出すスキル。yt-dlpで字幕を取得し日本語優先で整形し、必要に応じてWeb検索で文脈を補強する。「YouTubeの文字起こし」「動画のトランスクリプト」「この動画をMarkdownに」「youtube-transcript」などのリクエストで使用。

```markdown
# YouTube Transcript

YouTube動画の字幕を取得し、**要約＋詳細解説＋整形済み全文トランスクリプト**を1つのMarkdownファイルに書き出す。

## 前提

- `uv`/`uvx` および `python3` が利用可能であること（`yt-dlp` は `uvx` が都度取得する）。
- ネットワーク接続が必要。
- **供給網ハードニング**: `yt-dlp` は**バージョン固定**で実行する（`uvx yt-dlp@<固定版>`）。
  未固定だとPyPIの最新へ浮動し、悪性リリースをレビュー猶予なく実行しうるため。
  更新はスクリプト内 `YTDLP_VERSION` を意図的に引き上げて行う（環境変数で一時上書きも可）。
- スクリプトは**絶対パスで直接実行**する（`cd` を含む compound command は使わない）。
  スクリプト本体: `${CLAUDE_PLUGIN_ROOT}/skills/youtube-transcript/scripts/fetch_transcript.sh`
  （プラグインのインストール先により実体パスは異なる。実行時はそのフルパスを使う）

## Step 1: 入力の解釈

`$ARGUMENTS` を受け取り、空白で分割して解釈する。

- 先頭の `http`/`https` で始まるトークン → **YouTube URL**
- 2つ目のトークンがあれば → **出力先パス**（ディレクトリ or ファイルパス）
- **URLが無い場合**: `AskUserQuestion` でYouTube URLを尋ねる
- **出力先が無い場合**: `AskUserQuestion` で保存先を尋ねる
  - 選択肢例: 「llm-wiki/inbox に保存」「カレントディレクトリに保存」「パスを直接指定」
  - 「llm-wiki/inbox」が選ばれた場合の実パスは環境依存。`/llm-wiki` スキルが管理する Vault の
    `llm-wiki/inbox` を使う（パスをハードコードせず、ユーザーの環境に合わせて解決する）。

## Step 2: 字幕・メタ情報の取得

一時作業ディレクトリは**プロジェクト内の `.tmp/yt-transcript`**（`/tmp` は使わない）。

スクリプトを絶対パスで実行する:

```bash
/絶対パス/scripts/fetch_transcript.sh "<URL>" ".tmp/yt-transcript"
```

stdout にKEY=VALUE形式のマニフェストが出力される。`STATUS` を確認する:

- `STATUS=OK`: `TITLE` `UPLOADER` `DURATION` `UPLOAD_DATE` `URL` `SUB_LANG` `WORDS` `CHARS` `TRANSCRIPT_FILE` を取得。
  `TRANSCRIPT_FILE` のパスを `Read` で読み込み、整形済みトランスクリプト本文を得る。
  （`WORDS` は空白区切り語数で日本語では実質無意味。日本語字幕では `CHARS`（文字数）を報告に使う）
- `STATUS=NO_SUBTITLES`: 字幕が存在しない。ユーザーにその旨を伝えて終了（無理に本文生成しない）。
- `STATUS=ERROR`: `ERROR_MESSAGE` を提示して終了。

> 補足: スクリプトは「日本語 → 英語 → 動画の原語 → 任意の手動字幕」の順で字幕を探す。
> `SUB_LANG` が `en` 等の場合、トランスクリプト全文は原語のまま。要約・解説は日本語で書く。

## Step 3: Markdownファイルの生成

`Read` した整形済みトランスクリプトを**一次情報**として、以下の構成でMarkdownを組み立てる。
要約・解説は**日本語**で書く（トランスクリプト本文は原語のまま掲載）。

````markdown
# <動画タイトル> 文字起こしと解説

- **動画**: <URL>
- **投稿者/チャンネル**: <UPLOADER>
- **尺**: <DURATION>
- **公開日**: <UPLOAD_DATE を YYYY-MM-DD に整形>
- **字幕言語**: <SUB_LANG>（ja=日本語 / en=英語 など。自動字幕の場合はその旨注記）
- **取得日**: <`date +%Y-%m-%d` で取得した現在日付>

> 本ドキュメントは公式/投稿者の字幕(yt-dlpで取得)を一次情報として要約・整理したもの。
> 自動字幕の場合は聞き起こし誤りを含む可能性があるため、重要箇所は原典で確認すること。

---

## TL;DR（要約）

<動画全体の要点を箇条書き3〜6点で。>

## 詳細解説

<トランスクリプトを章立てして解説。トピックごとに見出しを立て、
重要な用語・主張・手順・コード・数値を漏らさずまとめる。
話者が複数いる場合は役割や発言の対応も補足する。>

## 補足・参考（任意：Web検索で補強した場合のみ掲載）

<トランスクリプトに無い背景・用語定義・関連リンクを箇条書き。各項目に出典URLを付ける。
 字幕本文には無い外部情報であることが分かるように書く。補強しなかった場合はこのセクションごと省く。>

## 全文トランスクリプト

<Readした整形済み全文をそのまま掲載。話者交代マーカー「›」は維持する。
 ※全文は字幕の一次情報。Web検索で得た情報をここに混ぜない。>
````

### 内容生成の指針

- **要約**: 動画のジャンルを問わず要点を端的に。技術動画ならAPI/手順/数値、対談なら主張/結論。
- **詳細解説**: トランスクリプトの流れに沿って章立て。長い動画でも省略せずカバーする。
  コード・コマンド・固有名詞は正確に。字幕由来で不確かな箇所は「（字幕の聞き起こし、要確認）」と明記。
- **全文**: 整形済みトランスクリプトを改変せず掲載（要約・解説の根拠として残す）。

### Web検索による補強（必要時のみ）

トランスクリプトは**一次情報**。要約・解説はまずトランスクリプトだけで組み立てる。
その上で、以下に当てはまる場合に限り `WebSearch`（必要なら `WebFetch`）で補う。
```

## cover-image (x4919-visual-gen)

- الترخيص: **WTFPL**  ·  الأصل: https://github.com/widnyana/eyay-toolkits/tree/50e222e396d3ea0b9a9cc65c4a5cf58d3c1cfa39/plugins/visual-gen
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/x4919-visual-gen/x20318-cover-image
- الوصف: This skill should be used when the user asks to "create a cover image", "generate a blog cover", "make an OG image", "design a social preview", "create a thumbnail for a post", "add a cover to my article", "make a featured image", "create a header image for a post", "generate an open graph image", or mentions cover images, OG images, social preview images, or blog post thumbnails. Do NOT trigger f

```markdown
# Cover Image Generator

Generate blog cover images and Open Graph/social preview images as PNG files. Each cover is a self-contained HTML document with inline CSS, captured as a screenshot via Chrome headless at exactly 1200x630 pixels.

The output is a static PNG suitable for Hugo front matter (`image:`), HTML `<meta property="og:image">`, and Twitter card metadata. No external images, no JavaScript, no server-side rendering required at capture time.

## Overview

Cover images serve as the primary visual identity for a blog post across social platforms, search results, and link previews. Each image is designed from scratch per post, reflecting the topic, tone, and key concepts of the content.

**What this skill produces:**
- A 1200x630px PNG file rendered from HTML+CSS
- Self-contained HTML with no external image dependencies
- Typography-driven design with CSS decorative elements
- Consistent branding placement

**When to use this skill:**
- Blog posts need an OG/social preview image
- Hugo front matter needs an `image:` field
- A series of posts need visually cohesive covers
- Existing covers need updating or redesigning

## Detailed Workflow

### Step 1: Read the source content

Read the blog post or article to extract the title, key concepts, and overall tone. The cover image must accurately represent the content. Identify:

- The exact title (or a shortened version if it exceeds 40 characters)
- The primary topic category (technical, tutorial, explanatory, announcement)
- Key visual metaphors or concepts from the content
- Whether the post is part of a series (affects series label placement)
- The desired output file path

If the user provides only a title without a file path, ask for the target output location before proceeding.

### Step 2: Determine the visual direction

Select a design approach based on the post topic and tone:

- **Technical posts** (programming, infrastructure, security, blockchain): dark background with bold typography and accent gradients. Conveys depth and technical rigor.
- **Tutorial/guide posts** (how-to, step-by-step, beginner): light background with clean layout and structured visual hints. Conveys clarity and approachability.
- **Conceptual/explanatory posts** (architecture, design patterns, theory): gradient background with centered typography. Conveys breadth and sophistication.
- **Announcement posts** (new feature, series launch, milestone): bold accent colors with prominent typography. Conveys energy and importance.

Consult `references/cover-design.md` for the full color palette and typography specifications for each direction.

### Step 3: Design the HTML+CSS
```
