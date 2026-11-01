---
name: kosif-web-film
description: Direct and render a motion-design video built as a webpage (codename «التنين الأسود» / Black Dragon). Use when the user asks for a video, promo, intro, explainer or kinetic-typography film made from code, says «اعمل فيديو», «فيديو موشن», «Create videos with Opus», or wants the "create a video as a webpage" skill.
---

# KOSIF Web Film («التنين الأسود»)

A director's workflow for a video that is one HTML page drawn by code, then rendered frame by frame to MP4.
It adapts the "Create videos with Opus" instructions to this repository: there is no `generateWebpage` tool
here, so Claude writes the page itself, checks it with `web_film.py`, looks at real frames, fixes, then renders
with `tools/render_html.cjs` at the owner's export standard.

## 0. Prompt first

No prompt, or only "اعمل فيديو"? Ask once what the video is about (subject, message, length, language) and stop.
With a prompt, carry on and say which reading you took when it can be read more than one way.

## 1. Keep every explicit requirement

Copy each explicit requirement from the prompt (text to show, brand colours, length, ratio, language, audio,
logo, call to action) into `requirements` in the plan, word for word. Everything else is your call as director.
`web_film.py check` fails when a requirement has no shot that answers it (`covers`).

## 2. Concept before code

Write in `film.plan.json` (start with `python3 .claude/skills/kosif-web-film/scripts/web_film.py plan "<prompt>" --out <job>/film.plan.json`):

- `concept`: one sentence, the idea the whole film serves.
- `visual_language`: palette (3 to 5 colours), type (Arabic: Cairo, Tajawal, Reem Kufi from `fonts/`), shape motif, motion rule (for example "everything enters from the dragon's tail line, exits along it").
- `shots`: each with `start`, `end`, `kind`, `text`, `transition_in`, `motion`, `covers` (which requirements it answers) and a `memorable` flag on at least one shot.

Rules the checker enforces: shots tile the duration with no gap or overlap, at least 3 shots, pacing varies
(not every shot the same length), no two consecutive shots use the same transition, at least one shot is
marked memorable, and every requirement is covered.

## 3. Build the page

`python3 .claude/skills/kosif-web-film/scripts/web_film.py scaffold <job>/film.plan.json --out <job>/film.html`
writes a working starting page from the plan: a seek-driven engine (`window.__kosif = {duration, seek(t)}`),
one scene per shot, easing, transitions and a seeded random. Then direct it: replace the placeholder scenes with
the real composition, typography and motion. Keep these contracts:

- Every frame is a pure function of `t` (no `Date.now()`, no unseeded `Math.random()`, no timers driving motion).
- No network: fonts and images live next to the page or come from `fonts/` (the renderer can run `--offline`).
- Arabic text: `dir="rtl"`, real shaping (no letter-by-letter splitting of Arabic words), `playbooks/arabic-typography.md`.

## 4. Validate and fix, then look

```
python3 .claude/skills/kosif-web-film/scripts/web_film.py check <job>/film.plan.json --html <job>/film.html
node tools/render_html.cjs --in <job>/film.html --out <job>/stills --stills 0.5,2,4,6 --offline
```

`check` reads the plan and the page (seek API, duration match, no network, no wall-clock or unseeded random,
one scene per shot). The stills grid is the first real look: open it, fix what reads badly (contrast, crowding,
text cut off, dead frames), and repeat. Never say a frame looks right without having opened it.

## 5. Render

```
node tools/render_html.cjs --in <job>/film.html --out <job>/film.mp4 --mode seek --offline [--audio <file>]
```

Defaults are the export standard (1080x1920, 30 fps, CRF 17). With the user's audio it is stream-copied and the
renderer proves the packets match. Verify with `templates/TEST_REPORT.md` before delivering.

## Limits

- This is code-drawn motion design. Filmed footage or AI video goes through Montage Pro, Kling (A41) or Higgsfield.
- `check` proves structure, not taste. The stills and the final film are what you judge.
