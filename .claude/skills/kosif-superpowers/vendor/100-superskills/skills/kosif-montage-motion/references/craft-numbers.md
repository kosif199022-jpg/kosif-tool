# Craft numbers — what top-tier motion films measure, and how KOSIF Motion applies them

Sources: the frame-by-frame measurements published with the open-source *cinetic* skill (MIT, github.com/Leonxlnx/cinetic,
`references/craft-rules.md`, `motion-tokens.md`, `transitions.md`, `finishing.md`), the *product-film* skill
(github.com/Rieranthony/product-film-skill), the *generative-film* skill (github.com/buildfastwithai/buildfast-skills),
HeyGen's *session-story* community skill, and the October 2026 X trend around Claude Opus 5.5 as a motion designer
(see `x-trend-2026.md`). Numbers are medians of shipped films, at 60 fps (f = frame) and 1080p. They are defaults with
a reason, not laws; the brand and the idea win when they disagree.

## The one-paragraph version
A model does not make video: it writes a program that paints the frame for any time t, a headless browser calls it
once per frame, FFmpeg encodes. The prompt is a tenth of the result; the harness is the rest: a seekable engine,
springs instead of curves, a beat grid shared by picture and sound, real motion blur, and a critique loop where the
model looks at its own frames (contact sheet, phone-width test, a strip around fast moments) and fixes the three
worst problems, at least three rounds, before the final render.

## Pacing
| Measure | Median | Range |
|---|---|---|
| Median shot | 1.46 s | 1.1–2.8 s (cut-driven 1.1–1.6; one-take 2.3–2.8) |
| Picture change | every ~0.7 s | dense loops every 0.33 s |
| First visible change | 0.10 s | 0.02–0.43 s — frame 0 is already composed and moving |
| First readable word | 0.4 s | the premise reads by ~2 s |
| Longest near-still run | 1.1 s | one designed hold of 1.0–1.6 s per film, on the key claim, under a music dropout |
| Last energy peak | 82% of runtime | a lull of 1–4 s at ~65%; a calm outro of 8–20% |
| End card | 2.2 s (9%) | assembles 1.0–1.3 s, holds 0.6–1.3 s, then cut |
| Frame difference (320 px luma) | median 1.4, p90 6.0 | calm premium films: median 0.35–0.5, >50% near-still, spikes ≥ 2.4 on transitions |

`motion.py measure` reports near-still share / mean / peak; `motion.py study REF.mp4` measures a reference the same way.

## Motion
- **Three curve families, one per role.** Arrivals: expo-out (`MOTION.E.out`, velocity ×0.92 per frame, settle 18–55 f).
  Exits into a cut: ease-in (`E.exit`, ×1.14 per frame over 10–24 f), leaving on the fastest frame. Repositioning and
  camera: steep in-out (`E.inOut`, `E.whip`) or momentum (`E.cam`, `E.rest`). Linear only for drift, data and light ramps.
- **Zero overshoot is the norm.** Just over half of top films have none on any move; the rest keep 1–4%, or spend one
  stylised overshoot on a true landing. Springs: critically damped by default (`MOTION.SPR.firm/soft/heavy`); `snap`,
  `pop`, `land` only for an object arriving at a surface, at most two per film.
- **Retargeting:** a value with many targets is the first value plus one spring per change (`MOTION.track(t, keys, SPR.firm)`),
  so it stays a pure function of t. Scale and zoom in log space (`MOTION.lmix`, `MOTION.push`, `zoomTrack`).
- **Duration grows with distance:** 0.35 s + 1.35 ms per px (`MOTION.durFor`), camera 0.6–2.4 s. The slowest move ≥ 3× the fastest.
- **Overlap:** a secondary move starts at 55–75% of the leading one, so both settle within 2 f (no stall-then-lurch).
- **The U-speed shot:** enter fast and decay, cruise slowly (1.5–8 px/f) while it reads, accelerate into the cut (`MOTION.shot`).
- **Speed limits:** text being read ≤ 3 px/f; anything over ~12–20 px/f wants motion blur; nothing over ~80 px/f (redesign:
  a cut on the beat, a match cut, a mask wipe). `motion.py speed FILM.mp4` measures px/f by optical flow and says which.
- **Weight:** shape settles 6 f before position; contact squash 8%/10% over 8 f (`MOTION.squash`); every punch uses one
  envelope (`MOTION.hitPulse(t, 2, 5)`, peaking 2 f after its sound).

## Text
- 3–4 words per card (1–7); dwell ~0.4 s per word, ≥ 0.5 s per card; a URL ≥ 1.7 s.
- Words arrive from a partial state (40% opacity, a 6–120 px rise, blur 4–12 px clearing by 60% of the move) and settle
  on one constant for all type (`MOTION.riseWords`, `revealWords`, `maskRise`). Text rarely fades out alone: it leaves with
  the cut, dims then goes, or rises out word by word.
- Type-on: headlines 15–22 chars/s; prompts ~46 chars/s, eased (55–75% in the first fifth), then a read hold of 72–120 f
  (`MOTION.typeOn`). Counters start near the final value, ease out, tabular figures (`MOTION.counter`). Decode reveals
  lock left to right (`MOTION.scramble`).

## Transitions
- About half of all beat changes are hard cuts on the grid; the rest are carried by camera moves, morphs, match cuts,
  floods and 1–2 f blends. 6–8 types per film, each ≤ 2 uses, plus one signature move used at open, middle and close.
- **No crossfades.** The workhorse is the velocity-matched cut: accelerate out, cut at peak speed, the next shot already
  moving in the same screen direction.
- Seams in the kit: `iris` / `flood` (radius in log space), `rackFocus` (cross-fade to a constant-blur copy — never animate a
  large blur), `roll` (3D flip front-loaded: 35% in the first frame, done in 10 f), `morphPath` (one shape becomes the next),
  `polarity` (stage flips only at act boundaries, riding a move).

## Camera
- A virtual 2D/2.5D camera; no handheld shake. Holds stay alive (a creep of ~4%/s or a drift of 0.3–2.5 px/f — `MOTION.breathe`).
- Pushes 1.5–3.1× over 30–70 f, peaking ~5% scale per frame; every interaction gets a 2–5× close-up.
- In 3D: one continuous camera through keys without stops (`three-kit cameraPath`, centripetal Catmull-Rom), depth of field
  focused on the look target, one tilted object per act.

## Colour, light, finish
- One accent with one meaning (≈5% of pixels, one full-bleed beat); stage polarity changes by act; arrivals tinted then
  relaxing to neutral over 12–50 f.
- No glow on type, no glassmorphism, no multi-hue gradients, no particles or lens flares standing in for ideas — unless
  the brand or the story owns them (`motion.py lint` warns).
- Motion blur is a render pass: sub-frames centred on the frame, averaged in float, quantised once
  (`motion.py render --blur 4`; 3D scenes accumulate on the GPU).
- Sound: a score synthesised on the beat grid (`score.py`), designed hits on the frames the picture exports (contact, 50% pop,
  97% settle), about 5 designed effects per 10 s, −14 LUFS integrated, true peak ≤ −1 dBTP (the mux normalises).

## The critique loop (every film, ≥ 3 rounds)
`motion.py sheet FILM.mp4` → contact (2 fps), phone (360 px), first frame, a strip around a fast moment, and `review.md`
with the rubric: hook · phone readability · motion quality · variety · composition · truth · sound sync · identity.
Fix the three worst with timestamps, re-render the affected seconds, end with "What I'd still change".
