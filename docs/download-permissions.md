# Download and render permissions (allow list)

When Claude Code runs in auto mode, every Bash command is checked by a server-side safety classifier.
If that service has an outage, Bash fails with:

> The server-side auto mode classifier gave no verdict (error) ...

That error is on Anthropic's side and temporary. It is not a bug in this repo. What to do when it shows up
is in `CLAUDE.md` and in appendix A29 of the protocol: retry once, then continue with work that needs no shell.

Commands that match an `allow` rule in `.claude/settings.json` run without asking the classifier, so they keep
working during such an outage. This block is in `.claude/settings.json` (added with the repo owner's explicit
approval on 2026-10-25). Change it only with the owner's approval:

```json
"permissions": {
  "allow": [
    "Bash(python3 .claude/skills/kosif-superpowers/scripts/stock_fetch.py *)",
    "Bash(python3 .claude/skills/kosif-superpowers/scripts/fetch_video.py *)",
    "Bash(python3 .claude/skills/kosif-superpowers/scripts/media_sources.py *)",
    "Bash(python3 .claude/skills/kosif-superpowers/scripts/fetch_reference.py *)",
    "Bash(python3 .claude/skills/kosif-superpowers/scripts/_deps.py *)",
    "Bash(python3 .claude/skills/kosif-superpowers/scripts/verify_video.py *)",
    "Bash(python3 .claude/skills/kosif-superpowers/scripts/montage_pro.py *)",
    "Bash(python3 .claude/skills/kosif-superpowers/scripts/boot.py *)",
    "Bash(python3 .claude/skills/kosif-superpowers/scripts/hub.py *)",
    "Bash(python3 tools/kosif.py *)",
    "Bash(python3 tools/build.py *)",
    "Bash(python3 tools/validate.py *)",
    "Bash(python3 tools/verify_video.py *)",
    "Bash(node tools/render_html.cjs *)",
    "Bash(ffmpeg *)",
    "Bash(ffprobe *)",
    "Bash(yt-dlp *)",
    "Bash(mkdir -p *)",
    "Bash(tail *)"
  ],
  "deny": [
    "Bash(yt-dlp *--exec*)",
    "Bash(yt-dlp *--netrc-cmd*)",
    "Bash(yt-dlp *--config-location*)",
    "Bash(yt-dlp *--plugin-dirs*)",
    "Bash(yt-dlp *--update*)"
  ]
}
```

Why these and nothing wider:

- Each `python3` rule names one script of this repo by its path, so it is not a blanket "run any Python" rule
  (auto mode drops rules like `Bash(python3 *)` anyway).
- `ffmpeg`, `ffprobe` and `yt-dlp` only read and write media files. The `deny` rules block the yt-dlp options that
  run other programs (`--exec`, `--netrc-cmd`) or load outside code or config.
- A rule matches only a plain command that starts with the tool. A `for` loop, a pipe (`| tail`), `&&` or `$(...)`
  is split into parts and each part must match a rule, so keep download and render steps as single commands run
  from the repo root, or put a loop in a Python script.
- Desktop and phone sessions that are not in auto mode still ask before the first run, as usual.
