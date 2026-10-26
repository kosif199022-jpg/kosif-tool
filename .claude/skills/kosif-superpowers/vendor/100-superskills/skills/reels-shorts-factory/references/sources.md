# مصادر «مصنع الريلز والشورتس» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## story-reels (2976-pwdev-social-media)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/pwdev-solucoes/pwdev-claude-marketplace/tree/c7b210504bd3a6b5ff32636c999fc6a2ccc5c44a/plugins/pwdev-social-media
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2976-pwdev-social-media/12592-story-reels
- الوصف: Monta peças verticais 9:16 — story, reels, shorts, TikTok — respeitando as áreas seguras da interface. Use quando o usuário disser "story", "reels", "shorts", "vertical", "9:16", "TikTok", "capa de reels", "template de story". A restrição dominante aqui é a UI do app, que cobre topo, base e lateral.

```markdown
# Vertical 9:16

Você monta no formato onde o app **come parte da tela**. Ignorar isso é o erro
que mais gera republicação.

## Princípio central

> A tela tem 1080 × 1920. A área utilizável tem cerca de **900 × 1350**.
> Projetar para 1920 de altura é projetar para ser coberto.

## Áreas seguras

Base 1080 × 1920:

```
topo         250 px   perfil, som, indicador de sequência
base         320 px   legenda, CTA, barra de progresso
direita      120 px   curtir, comentar, compartilhar
esquerda      60 px   margem visual
```

Área confiável: **900 × 1350 centralizada, deslocada para cima.**

> Erro mais comum: chamada no rodapé, onde a legenda do app cobre.
> Segundo mais comum: elemento à direita, atrás dos botões de ação.

**Ressalva de validade:** áreas seguras mudam a cada atualização de app. Os
valores acima são conservadores. Confirme antes de campanha grande e atualize
`references/formatos.md`.

## Estrutura

```
0-1s     gancho — precisa funcionar mudo e sem contexto
1-3s     desenvolvimento
3s-fim   entrega
final    CTA dentro da área segura
```

Story em sequência: cada card precisa sobreviver sozinho. As pessoas entram no
meio da sequência o tempo todo.

## Vídeo

- **Legenda embutida é obrigatória.** A maioria assiste sem som — e sem legenda
  a peça é inacessível para pessoa surda. Não é preferência, é acessibilidade.
- Legenda dentro da área segura, nunca no rodapé
- Sem piscar acima de 3 Hz — risco de convulsão fotossensível
- Texto na tela: mínimo 32 px, alto contraste, tempo de leitura suficiente

## Montagem

**Portão:** `/figma-use` antes de `use_figma`.

1. Criar frame 1080 × 1920
2. **Criar guias da área segura como primeira ação** — antes de qualquer conteúdo
3. Montar o conteúdo inteiro dentro de 900 × 1350
4. Conferir com `get_screenshot` que nada crítico saiu da área
5. Nomear `{{campanha}}/9x16/{{n}}`

Faça um componente `Story base` com as guias — assim toda peça nasce correta.

## Anti-padrões

- CTA no rodapé
- Elemento importante na faixa direita
- Texto colado na borda superior
- Vídeo sem legenda
- Reaproveitar peça 4:5 esticada para 9:16
- Texto pequeno "porque é vertical" — a distância de leitura é a mesma

## Limites

- Não edita nem gera vídeo — ver `video-gen`
- Não escreve copy — ver `pwdev-copy`
- Não publica
- Não garante área segura além da data de atualização de `formatos.md`

## Skills relacionadas

- `creative-concept`, `figma-pipeline`, `creative-review`, `video-gen`, `format-specs`
```

## social-video-hooks (101-video-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/adamperlis/adam-plugins/tree/e41984f68ab8a53f028d078c6070ec8658fd41ac/plugins/video-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/101-video-skills/218-social-video-hooks
- الوصف: Write short-form video hooks and beat sheets for Reels, TikTok, Shorts, and similar feeds. Use when planning an opening, improving retention, or giving a creator precise shooting instructions.

```markdown
# Social video hooks

Make the opening understandable in one second: show a meaningful action or result, say why it matters, and use on-screen text only when it adds clarity. The visual, spoken line, and title should support the same idea without repeating the same words.

## Choose the hook

- **Result first:** show the finished outcome before the process.
- **Visible test:** start a comparison or challenge the viewer can follow.
- **Specific problem:** show a familiar frustration in its real setting.
- **Surprising action:** begin with behavior that creates a question the rest of the clip answers.
- **Direct question:** ask something the intended viewer can answer from experience.

Choose one primary hook. Add a second visual or text cue only when it clarifies the premise. Do not promise a result the video cannot show.

## Write a timed beat sheet

For each beat, give the exact spoken words, the camera or screen action, and what new information the viewer gets. Example:

| Time | Say | Show | New information |
|---|---|---|---|
| 0:00 | “Can this finish before my coffee?” | Start the task and timer | The test begins |

Place the proof before a long explanation. Change framing or introduce new evidence when the current image has finished making its point. A cut, caption, or zoom is useful only if it advances understanding. Finish with one call to action that follows from the video.

## Check the script

- The opening makes sense with sound off and with sound on.
- Every spoken line can be performed naturally.
- The visuals prove the main claim.
- No beat is held past the point where the viewer has understood it.
- The call to action is clear and proportionate to what was shown.

Deliver the beat sheet and a short shot list. If a promised result requires data or footage that is missing, flag it before treating the script as shoot-ready.
```

## davinciresolve-youtube-shorts (1096-akbun-editvideo)

- الترخيص: **MIT**  ·  الأصل: https://github.com/choisungwook/akbun-aitools/tree/b592650776c4ed1723087911010466d0b537fc6b/plugins/akbun-editvideo
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1096-akbun-editvideo/2466-davinciresolve-youtube-shorts
- الوصف: Create vertical YouTube Shorts candidates from the selected DaVinci Resolve timeline, preserve its media and audio processing, and publish the approved exports.

```markdown
# DaVinci Resolve YouTube Shorts

Use the currently selected timeline as the source. Before editing, record its name, start/end frames, frame rate, video/audio track counts, per-track item counts, and resolution. Do not modify the source timeline.

Create a candidate list first: each of the 20 suggestions needs a distinct hook and exact short in/out timecodes. Candidates may overlap; do not imply they are independent sections when they reuse footage. Convert seconds to frames using the source frame rate and compute `short duration + pre-handle + post-handle` before creating anything. Check each candidate against the timeline start/end bounds.

For each feasible candidate, duplicate the source into a uniquely named timeline. Confirm the duplicate retains the original audio track count, per-track item counts, and processing before changing settings. Set custom timeline settings before setting portrait 2160×3840, square pixels, and fill-screen scaling. Check every API return value and re-read settings to confirm the applied dimensions, frame rate, and scaling. If a duplicate, setting, or re-read check fails, stop and report the completed candidates; do not silently continue with a partial batch.

Run Smart Reframe on each video clip and check the call result. Inspect representative frames for clipped or misplaced subjects. A successful API call is not proof that framing is acceptable. Preserve source audio tracks and processing. Add a duration marker spanning only the suggested short; use a frame position relative to the timeline start plus its start frame, and a duration in frames. Verify the marker stays within the duplicate's bounds and has the intended duration.

Check feasibility first: a 60-second short plus two 15-second handles requires at least 90 seconds of usable timeline. If the source is shorter, report the maximum feasible short duration and handle lengths, and ask which constraint to relax before creating candidate timelines. Do not pad with black, silently shorten the short, or claim unavailable handles.

Render only the requested candidates using an available vertical YouTube 2160p preset. Do not assume a preset named `YouTube - 2160p` is portrait: inspect the selected preset and confirm the output is 2160×3840. Before upload, inspect the rendered dimensions, duration, audio, title, description, category, location, thumbnail, and visibility. Upload only when explicitly requested; default visibility to Private. Report each timeline name, marker range, render path, and upload status.

After the batch, compare the source timeline's name, bounds, settings, and track counts with the preflight record. Report any mismatch instead of claiming the source was preserved.
```

## block-no-verify-hook (3073-block-no-verify)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/block-no-verify
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3073-block-no-verify/13239-block-no-verify-hook
- الوصف: Configure a PreToolUse hook to prevent AI agents from skipping git pre-commit hooks with --no-verify and other bypass flags. Use when setting up Claude Code projects that enforce commit quality gates.

```markdown
# Block No-Verify Hook

PreToolUse hook configuration that intercepts and blocks bypass-flag usage before execution, ensuring AI agents cannot skip pre-commit hooks, GPG signing, or other git safety mechanisms.

## Overview

AI coding agents (Claude Code, Codex, etc.) can run shell commands with flags like `--no-verify` that bypass pre-commit hooks. This defeats the purpose of linting, formatting, testing, and security checks configured in pre-commit hooks. The block-no-verify hook adds a PreToolUse guard that rejects any tool call containing bypass flags before execution.

## Problem

When AI agents commit code, they may use bypass flags to avoid hook failures:

```bash
# These commands skip pre-commit hooks entirely
git commit --no-verify -m "quick fix"
git push --no-verify
git commit --no-gpg-sign -m "unsigned commit"
git merge --no-verify feature-branch
```

This allows:
- Unformatted code to enter the repository
- Linting errors to bypass checks
- Security scanning to be skipped
- Unsigned commits to bypass signing policies
- Test suites to be circumvented

## Solution

Add a `PreToolUse` hook to `.claude/settings.json` that inspects every Bash tool call and blocks commands containing bypass flags.

### Configuration

Add the following to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hook": {
          "type": "command",
          "command": "if printf '%s' \"$TOOL_INPUT\" | grep -qE '(^|&&|;|\\|)\\s*git\\s+.*--(no-verify|no-gpg-sign)'; then echo 'BLOCKED: --no-verify and --no-gpg-sign flags are not allowed. Run the commit without bypass flags so that pre-commit hooks execute properly.' >&2; exit 2; fi"
        }
      }
    ]
  }
}
```

### How It Works

1. **Matcher**: The hook targets only `Bash` tool calls, so it does not interfere with other tools (Read, Edit, Grep, etc.).
2. **Inspection**: The `$TOOL_INPUT` environment variable contains the full command the agent is about to execute. The hook uses `printf` to safely pass input (avoiding `echo` pitfalls with special characters) and checks for `--no-verify` or `--no-gpg-sign` flags only when preceded by a `git` command.
3. **Blocking**: If a bypass flag is found in a git command, the hook exits with code 2 and prints an error message. Exit code 2 signals Claude Code to reject the tool call entirely.
4. **Pass-through**: If no bypass flag is found, the hook exits with code 0 and the command executes normally.

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Allow the tool call to proceed |
| 1 | Error (tool call still proceeds, warning shown) |
| 2 | Block the tool call entirely |

## Blocked Flags

| Flag | Purpose | Why Blocked |
|------|---------|-------------|
```

## block-no-verify-hook (3452-block-no-verify)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/block-no-verify
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3452-block-no-verify/14155-block-no-verify-hook
- الوصف: Configure a PreToolUse hook to prevent AI agents from skipping git pre-commit hooks with --no-verify and other bypass flags. Use when setting up Claude Code projects that enforce commit quality gates.

```markdown
# Block No-Verify Hook

PreToolUse hook configuration that intercepts and blocks bypass-flag usage before execution, ensuring AI agents cannot skip pre-commit hooks, GPG signing, or other git safety mechanisms.

## Overview

AI coding agents (Claude Code, Codex, etc.) can run shell commands with flags like `--no-verify` that bypass pre-commit hooks. This defeats the purpose of linting, formatting, testing, and security checks configured in pre-commit hooks. The block-no-verify hook adds a PreToolUse guard that rejects any tool call containing bypass flags before execution.

## Problem

When AI agents commit code, they may use bypass flags to avoid hook failures:

```bash
# These commands skip pre-commit hooks entirely
git commit --no-verify -m "quick fix"
git push --no-verify
git commit --no-gpg-sign -m "unsigned commit"
git merge --no-verify feature-branch
```

This allows:
- Unformatted code to enter the repository
- Linting errors to bypass checks
- Security scanning to be skipped
- Unsigned commits to bypass signing policies
- Test suites to be circumvented

## Solution

Add a `PreToolUse` hook to `.claude/settings.json` that inspects every Bash tool call and blocks commands containing bypass flags.

### Configuration

Add the following to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if grep -qE '\"command\"[[:space:]]*:[[:space:]]*\"([^\"\\\\]|\\\\.)*(--no-(ver|g)|commit([^\"\\\\]|\\\\.)*([[:space:]]|\\\\[tn])-[a-zA-Z]*n)'; then echo 'BLOCKED: --no-verify and --no-gpg-sign flags are not allowed. Run the commit without bypass flags so that pre-commit hooks execute properly.' >&2; exit 2; fi"
          }
        ]
      }
    ]
  }
}
```

### How It Works

1. **Matcher**: The hook targets only `Bash` tool calls, so it does not interfere with other tools (Read, Edit, Grep, etc.).
2. **Inspection**: Claude Code sends the tool call to the hook as JSON on stdin and sets no `$TOOL_INPUT` variable. The hook searches the `command` value in that JSON with `grep -E`, so it needs no `jq` or `node`, and text in other fields, such as `cwd` or the tool call's description, can't trigger it. It blocks `--no-verify`, `--no-gpg-sign`, and any shorter prefix of them that git accepts, e.g., `--no-veri`. It also blocks a short option group with `n` that follows `commit` in the same command, e.g., `-n` or `-nm`, because `-n` is the short form of `--no-verify`. The hook doesn't look for the word `git`, so it also catches `if git ...`, `sudo git ...`, and `g=git; $g commit --no-verify`. A false match, such as a commit message that mentions a flag, blocks the call, which is the safe way to fail.
```

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
