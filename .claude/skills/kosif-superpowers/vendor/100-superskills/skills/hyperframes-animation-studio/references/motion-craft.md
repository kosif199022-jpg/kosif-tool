# Motion craft — what the research pack adds to KOSIF Motion

Distilled on 2026-10-07 from the user's research archive (`Claude-Motion-3D-Graphics-Research-2026-10-07.zip`):
HyperFrames' own skills (Apache-2.0, HeyGen), the community *Motion Director* (MIT, Abdullatif), LottieFiles'
*motion-design* (MIT), Anthropic's design skills (Apache-2.0). Paraphrased rules only; no code or assets copied.

## 1. Motion has mass: springs, not curves

- Cheap motion goes A→B on a fixed curve; expensive motion accelerates, overshoots a hair and settles. The kit has
  `MOTION.spring("snappy" | "default" | "heavy" | "playful")` (overshoot ≈ 3 % / 1 % / 0 / visible) as GSAP eases,
  `MOTION.track(t, [[time, value], …], preset)` for a value that changes target several times (one spring per
  change, continuous, a pure function of t), and `MOTION.zoomTrack` (log space: 1×→2× feels like 2×→4×).
- Keyframe times are when a move **starts**; a spring settles over ≈ 0.5 s. Start early, let the payoff hold.
- Never linear on spatial movement (linear only for rotation, progress, timers). Entrances ease-out, exits ease-in,
  on-screen ease-in-out, ambient loops sine. Entrance ≥ exit duration (exit ≈ 65–75 %).
- Durations by element (LottieFiles): micro 80–120 ms · button 120–180 · icon 150–250 · card 200–350 · modal
  300–400 · page 400–600 · dramatic reveal 600–1200 · ambient 2–20 s. Scale with distance (100 px = 1×, full
  screen = 1.8–2×). Overshoot budget: premium 0 %, feedback 2–5 %, success 5–10 %, celebration 15–25 %.
- Stagger totals stay under 500 ms (micro 20–40 ms, standard 50–100, dramatic 100–200); same easing family, vary
  only start times; the last element may overshoot as punctuation.

## 2. Choreography

- Lead with the hero (largest displacement, strongest ease); supporting elements subtler in every dimension.
- One spatial origin per entrance group; counter-motion at 20–30 % (hero enters left → background drifts right;
  lifts → shadow spreads). Depth through speed: foreground 1×, mid 0.5×, background 0.2×.
- The 1/3 rules: no motion travels more than a third of the frame without an intermediate key; with 3+ animated
  elements at most a third move at once. Something new every 2–4 s; no hold longer than a beat and a half.
- Four acts: anticipation (10–20 %) → action (30–50 %) → reaction (10–20 %: shadows, siblings, environment) →
  resolution (20–30 %: overshoot settle, 100–200 ms of breathing room).
- Scenes hand over through a shared shape: a scene's last frame equals the next scene's first frame — never a cut,
  never a crossfade (Motion Director). A dot grows into a pill, the pill into a card.
- Camera: one transform on one container, one move at a time, zoom in log space, still between events.

## 3. Time in beats, sound on the hit

- `MOTION.beats(bpm, offset)` → `at(n)` / `len(n)`; picture and sound read the same clock; big moments on downbeats;
  the music drop lands on the payoff.
- Real recordings beat synthesised sound (KOSIF's `ambience.py` is the fallback when no licensed recording is
  available — say so in the delivery note). One effect per visible event; effects peak late, so align the *hit*,
  not the file start. The mix is normalised to **−14 LUFS, true peak −1 dB** (`motion.py` mux does this).
- Assume no sound: every beat must also work as text on screen.

## 4. Render contract reminders (HyperFrames core / animation)

- Centre with flex/inset, never a CSS `transform` on a node GSAP also tweens (`gsap_css_transform_conflict`);
  initial states go in `fromTo`. Spatial motion through `x / y / scale / rotation` only; never `width/height/top/left`.
- Never tween `visibility` / `autoAlpha` / `display` on a `.clip`; animate a child. `<audio>` needs an `id`.
- Rising text through clip-path masks, not `overflow:hidden` (the layout check reports masked words as overflowing;
  the kit now uses `clip-path`). No `will-change` on anything the camera scales (blurry text).
- Pre-compute layout constants; never `getBoundingClientRect()` at tween time. No clocks, no `Math.random`,
  no network; `repeat: -1` only under a finite root `data-duration`.
- Motion blur: HyperFrames has none built in; KOSIF Motion's 3D renderer accumulates k sub-frames on the GPU
  (`motion.py render --blur 4`, shutter 0.5). Blur must never show a value that does not exist: keep counters sharp.

## 5. The critique loop (Motion Director)

Look at your own frames: stills before every render, contact sheet + phone-width + first-frame after. Score 1–10:

| # | Criterion | 8+ means |
|---|---|---|
| 1 | Hook | the first 2 s stop the scroll; frame one says the pain or the promise in words |
| 2 | Readability | every word reads at 360 px wide; nothing important under 28 px at full size |
| 3 | Motion quality | springs, no linear slides, no fades-in, no dead frames, no pops |
| 4 | Variety | something new every 2–4 s; no hold longer than a beat and a half |
| 5 | Composition | one focal point per shot, safe margins, reframed per format |
| 6 | Truth | real UI, real data; illustrative data labelled |
| 7 | Sound sync | every visible event has its sound on the beat; the drop lands on the key moment |
| 8 | Brand | colours, fonts, voice match the style guide |

Fix the three worst problems (timestamp + wanted result, not just the fix), re-check stills, re-render, log the
round; minimum three rounds; end every delivery with **What I'd still change** and what the tools cannot judge
(they cannot hear).

## 6. Banned looks (product films; explainers may keep numbered stages)

Centred title on a gradient · everything fading in · blur-in text · crossfades between scenes · dark scene with a
green/purple glow · generic particle bursts and lens flares "for their own sake" · frame borders, corner labels,
"01 · STEP" labels · invented logos · synthesised beeps · holds longer than a beat and a half.

## 7. Quality checklist (LottieFiles, abridged)

Elements > 40 px for motion · readable at full speed · clear primary / secondary / ambient layers · natural arcs ·
follow-through 50–150 ms on children · not opacity-only for important changes · < 20 animated elements per
viewport · primary motion on transform + opacity · a reduced-motion alternative where the piece is interactive.

## Where each idea came from

Springs/track/zoom/beats/sound/critique/banned looks → claude-motion-director (MIT). Timing tables, Disney
principles, choreography, 1/3 rules, checklist → lottiefiles/motion-design (MIT). Render-contract lints, clip
rules, adapters, motion-blur note → heygen-com/hyperframes skills (Apache-2.0). Seeded generative aesthetics →
anthropics/skills algorithmic-art (Apache-2.0). The pack's own catalog of 33 tools is `tools-catalog-2.md`.
