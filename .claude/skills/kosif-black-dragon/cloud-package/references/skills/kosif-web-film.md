---
name: kosif-web-film
description: Direct and render a motion-design video built as a webpage (codename «التنين الأسود» / Black Dragon). Use when the user asks for a video, promo, intro, explainer or kinetic-typography film made from code, says «اعمل فيديو», «فيديو موشن», «Create videos with Opus», wants the "create a video as a webpage" skill, or asks for a cinematic story video drawn entirely by code as one continuous camera move over one world (a map, a desk, a board) synced to a voiceover (World Film mode).
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

## World Film mode: one world, one continuous camera

Use it when the brief is a cinematic story drawn entirely by code (no AI video, no stock footage) and
synced to a voiceover: one big world (a map, a desk, a board), ONE continuous camera move over it, no
cuts and no slides, real photos and documents dropped onto it as physical prints. The engine is
`world/engine.js` + `world/camera.cjs` (canvas), the director's tool is `scripts/world_film.py`.

1. **Beat table first, and show it to the owner before building.** One beat per narration line:
   time, the line, its ONE hero, any on-screen text, and the visual moment that lands on the spoken word.
   Get the line timings from word timestamps (`words`, for example from faster-whisper) or from the owner.
   Write `world.plan.json` (start from `world_film.py example --out <job>/world.plan.json`), then
   `world_film.py beats <job>/world.plan.json --out <job>/beats.md` and send that table with your questions.
2. **Plan.** `format` (default the export standard 1080x1920 at 30 fps unless the owner gives one),
   `duration` = the voiceover's exact length (`audio_duration` too, so the checker compares them),
   `objects` (desk, map, area, pin, route, photo, text, book, stamp; map objects may use `geo: [lat, lon]`),
   and `beats` (start, end, narration, hero, optional text, camera {x, y, zoom}, hits).
   Hit actions: `circle` (drawn as the word is said), `glow`, `lift`, `open` (book), `draw` (route, with
   `from`), `stamp` (slams on the beat with a small camera shake). Put `word` on a hit to have it checked.
3. **Check.** `world_film.py check <job>/world.plan.json` fails on:
   - more than one hero in a beat, an on-screen phrase shown twice, or a typed phrase the narrator says
     anywhere in the film (show it or type it, never both),
   - hero text under 84 px or any label under 46 px on screen at the beat's camera, a hero photo
     narrower than 55% of the frame, more than 7 words of text in a beat,
   - any object that is never a hero, a text or a hit target (less is more: no decorative clutter),
   - hits outside their beat or more than 1.5 frames off their word, beats that leave a gap or do not
     end exactly at the voiceover's length,
   - a camera that stops dead (under 0.35 px per frame for more than 0.4 s), jerks (speed changing by
     more than 2.5 px per frame in one frame) or jumps (more than 140 px in one frame, which reads as a cut).
4. **The camera** (`camera.cjs`, a pure function of time) arrives a little after each beat starts, keeps
   drifting toward the next target during the hold, eases every travel in and out with a quintic curve,
   pulls back to travel when the next target is more than 1.6 screens away and dives in again, and gives
   a move the time it needs to stay under its acceleration limit. Per beat: `travel` (minimum seconds),
   `split` (share of the travel before the beat boundary, to keep a hit on screen), `drift`, `pullback`;
   on the first beat `from`; on the last `end_push`. The engine adds handheld sway, motion blur on fast
   moves (sub-frame accumulation), film grain, a soft glow and a vignette.
5. **Look before rendering.** `world_film.py build <job>/world.plan.json --out <job>/film.html`, then
   `world_film.py review <job>/world.plan.json` gives still times for every beat and hit plus an 8-frame
   sequence across every camera move. Render them with
   `node tools/render_html.cjs --in <job>/film.html --out <job>/x.mp4 --stills <times> --stills-dir <job>/review --offline`,
   open the grids and fix anything cluttered, hard to read, overlapping, cut off, or that jerks.
6. **Render** with the voiceover: `node tools/render_html.cjs --in <job>/film.html --out <job>/film.mp4 --mode seek --offline --audio <voiceover>`.
   Check duration, fps and the audio proof line before delivering.

## Limits

- This is code-drawn motion design. Filmed footage or AI video goes through Montage Pro, Kling (A41) or Higgsfield.
- `check` proves structure, not taste. The stills and the final film are what you judge.
