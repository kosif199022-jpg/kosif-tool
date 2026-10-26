# The Opus 5.5 motion wave on X (Sept 22 – Oct 7, 2026) — what worked, and what KOSIF Motion took from it

**Corpus:** 3,984 posts read (searches for the release, its motion claims and their replies; 140 on Sept 22, 860 on Sept 23, 402 on Sept 24, then 10–40 a day), 1,948 of them about making motion with the model, 1,535 with a video or image, 203 M views in total. Languages: English 1,566 · Chinese 87 · Japanese 71 · Turkish 29 · Spanish 27 · French 12 · Portuguese 10 · Arabic 11 (posts tagged by X; 106 untagged).
Collected from the owner's X account with the search UI (no API), in time windows from the release day to Oct 7, plus
the 230 entries of prompt-motion.com (each motion video next to the prompt or skill that made it), the 12-step course
thread by @0xMovez (2.1M views), and four open-source skills (cinetic, product-film, generative-film, session-story).
Quotes are paraphrased; handles are kept so a reader can find the source.

## 1. What people actually made
| Theme (keyword families, a post can count twice) | Posts | Views |
|---|---|---|
| three.js / 3D scenes | 487 | 52.0 M |
| seek(t) / frame-by-frame rendering | 70 | 34.9 M |
| UI / product / SaaS films | 217 | 16.3 M |
| AI video models alongside (Seedance, Veo, Kling) | 128 | 10.5 M |
| games | 153 | 10.3 M |
| sound / music | 302 | 9.2 M |
| showreels | 55 | 5.3 M |
| one shot / one prompt | 264 | 4.7 M |
| After Effects comparisons | 48 | 4.1 M |
| reference video or frame | 87 | 3.9 M |
| skill / CLAUDE.md shared | 77 | 3.5 M |
| story / short film / character | 145 | 3.4 M |
| explainers | 109 | 3.2 M |
| critique / iterate loops | 141 | 2.9 M |
| effort xhigh / max named | 30 | 2.9 M |
| shaders / GLSL | 18 | 2.6 M |
| critical or skeptical | 60 | 2.3 M |
| Blender / Spline | 90 | 2.1 M |
| HyperFrames | 61 | 1.9 M |
| Remotion | 49 | 0.9 M |
| physics / particles | 53 | 0.9 M |
| voice / ElevenLabs | 48 | 0.6 M |
| Arabic | 11 | 0.13 M |

Read it as attention, not quality: 3D and the frame-by-frame harness took 43 % of all views with 14 % of the posts;
"one prompt" posts were many but drew modest views each; the critique loop was rarer than the results it produced.

## 2. How the good ones were made (the harness, not the prompt)
- **The program is the film.** Opus writes a function that paints the frame for any time `t`; a headless browser calls it
  once per frame and FFmpeg encodes. Nothing depends on a clock, so a fix is one edit and a re-render.
  Left alone it picks "route A": one `index.html`, `window.seek(t)`, Playwright frame-by-frame, FFmpeg — it skipped
  Remotion and HyperFrames unless told (@__morse dug into a one-shot). → KOSIF: `motion.py new --canvas`, `film.py` seeks
  `render(t)` or `seek(t)`.
- **Springs, not curves.** The viral UI morphs specify closed-form springs; a value with several targets is the sum of
  one spring per change, so frame 812 renders without simulating 0–811. → `MOTION.SPR`, `MOTION.track`.
- **4 sub-frames per frame, averaged** — real motion blur on fast moves. → `--blur 4` for every page.
- **One clock for picture and sound:** a beat grid (measured from a supplied track, or the BPM of a synthesised one);
  cuts and state changes on beats, designed hits on contact frames, −14 LUFS. → `motion.py beats`, `score.py`, `MOTION.beats`.
- **Opus watches its own frames.** The clips that went viral were iterated: contact sheets, a strip around fast moves, a
  phone-width test, scores on 6–8 criteria, the 3 worst problems fixed, ≥ 3 rounds. Several authors were candid: 163 model
  calls and ~7 hours for a 45-second watercolour short; 5 minutes of dictation and 12 hours of autonomous work for a
  142-second music video. → `motion.py sheet` + `review.md`, the critique gate in skill 110.
- **Effort:** every celebrated one-shot ran at xhigh or max effort. Where authors gave numbers: median 20 minutes (p90 57) for a short clip from one prompt (171 posts), median 4 hours for the celebrated pieces (62 posts), median $10 of tokens (p90 $200, 237 posts). The long end is real: 7 hours and 163 calls for a 45-second watercolour short; 12 hours of autonomous work for a 142-second music video.

## 3. Five prompt patterns that kept working
1. **The one-liner showreel** — "a dynamic 15-second motion graphics video that shows what an incredible motion designer you
   are, like a showreel for a résumé; go all out". Works because it names a genre with known rules and makes the model the
   subject. Its weakness ("brief contagion"): hundreds of near-identical reels.
2. **Point it at a brand** — the URL, "use the real screenshots, logo, colours and fonts", "must have music"; the model fetches
   the assets itself. Same session per brand: the second film is faster because the renderer already exists.
3. **Name a look and feed a reference** — a frame, a video (extract a frame every 0.5 s, write `style_guide.md` and a shot list
   first), or a whole image library. Take the grammar, never the content. → `motion.py study REF.mp4`.
4. **The XML spec** — `<inputs>` (ask for these, with defaults) · `<direction>` (feel, palette, banned looks) · `<structure>`
   (a beat-by-beat state list on a 120 BPM grid; something happens on every beat) · `<build>` (seek(t), springs, sub-frames)
   · `<gotchas>` · `<start>` (show the state list before any code). The most-bookmarked prompt of the week (a single shape
   morphing through 12 UI states) used it.
5. **The director's brief** for long pieces (9.5k–19k characters): the film in one line, references, tools and keys,
   a character bible, a beat sheet with a payoff every 3–5 s, text-on-screen rules, workflow gates (plan → stills → animatic
   → full pass → polish → audio → render), the critique loop, deliverables. Sub-agents get an `ANIMATION_GUIDE.md` first.
   One variant generates base shots with a video model and has Opus redraw them in JavaScript ("generate-then-trace").

## 4. What separated "insane" from "mid"
- 60 posts (2.3 M views) were openly skeptical (paraphrased): the reels show off the harness more than taste, the showreels look alike,
  physics that breaks the moment anything has weight, text that jitters under scale, audio pasted on rather than scored.
- 83 posts argued about jobs ("cooked" was the keyword); the counter-argument that recurred was craft: the model gets the
  first draft fast, while timing, weight and restraint still decide whether the piece is good.
- The defaults that read as generated: a centred title on a gradient, everything fading in, corner labels and frame
  borders, glow on UI chrome, particle bursts, bouncy easing, crossfades, the same reel as everyone else.
- What fixed it: a reference, a real product or story, one device carried through every shot, one accent colour, a
  measured motion system, and rounds of critique on rendered frames. → `references/craft-numbers.md`, `motion.py lint`.
- Physics is still where it breaks (the viral "cow that runs on its udder"); realism needs real modelling — the koi pond
  (`examples/koi_pond`) shows the v3 blocks.

## 5. Links that recur
- github.com was the most linked domain (100 links): heygen-com/hyperframes (the composition format KOSIF Motion
  writes), browser-use/video-use, cth9191/motion-design, tugrawork-creator/saas-motion-kit,
  buildwithhanif/claude-animation-skill, riba2534/claude-opus-5-5-demo, dgreenheck/tidewater (water shading),
  GordenSun/neon-pixel-city, mike007jd/voxel-musou, SkyeShark/eidoverse-video, Vincentwei1021/video-shotcraft and
  video-talkcraft, Bingeljell/image-to-3dlab.
- Also recurring: threejseval.com (three.js scenes scored side by side), prompt-motion.com (motion next to its prompt),
  tripo3d.ai (image → 3D model for a scene), codepen.io pens, youtube cuts of longer pieces.

## 5b. Two posts studied frame by frame
- **@kloss_xyz — "listen with math"**: a music piece where every visual value is a per-frame channel measured from the
  track (kick, bass, onset, centroid, silence, pitch dives), the picture runs on a *tape clock* (the integral of playback
  speed, so it freezes when the track tape-stops), the ground is the spectrogram in a magma ramp, and glitch accents are
  keyed to the analysis, with a seamless loop proved at the seam. → `motion.py channels` (tape-stop detection by pitch-line
  fit and spectral-shift rate, speed state machine), `MOTION.channels`, `spectrumOnTape`, `makeSpectrumGround`,
  `makeGlitchPass` (chroma, slice, negative tear, freeze monochrome, warp), `makeSparks` on the tape clock,
  `motion.py loopcheck`, `score.py tape_stops_s`; example `projects/sound_ground`.
- **@aicreataro — "measure real motion"**: one fixed-camera video of a real performer becomes the motion of a particle
  body; AI is used only for the character's look and the background. → `motion.py mocap` (median background, difference,
  morphology, seeded point sampling → JSON), `makeParticleBody`, `loadModel` (GLB with its animation sought to t).

## 6. Arabic-language posts
Only 11 posts (133 k views) were in Arabic, mostly reposts of English demos plus a few asking whether RTL text
survives the pipeline. The gap is the opening: no one showed Arabic kinetic type done properly. KOSIF Motion's answers:
word masks that keep Arabic shaping intact (`MOTION.revealWords`), direction on text elements and never on `<html>`
(lint rule), offline Arabic narration (`voice.py`, Microsoft Naayf), and karaoke captions that colour the spoken word in
an event per word so the line is shaped and ordered correctly (`montage.py captions`, Noto Sans/Kufi/Naskh Arabic).
