# Video breakdown → rebuild → generation prompt

How to analyse any reference film (motion graphics, animation, product demo, SaaS explainer, ad) so that another
creator — or this engine — can rebuild it without seeing it, and how to turn that analysis into one copy-paste prompt
for a 10-second generator (Google Omni Flash). Measure first, look second, write third. Never describe a part you
have not looked at.

## 1. Measure the whole film (never only the opening)
`kmotion analyze VIDEO --out NAME.breakdown` (add `--transcribe` when there is speech). It gives, for the entire duration:
- specs: duration, resolution, aspect, fps, codec, audio stream;
- **beats**: hard cuts, soft scene changes (dissolve / dip / wipe, by colour-histogram jumps) and element entrances
  (bursts of on-screen change after calm) — every beat ≤ 3 s, so a held layout still gets read in parts;
- per beat: palette (hex + share), background colour, brightness, saturation, motion energy, global pan/tilt
  (% of frame width per second), how it is entered (cut, dissolve, dip to black/white, whip, same-shot entrance);
- audio: integrated LUFS and true peak, tempo (BPM), onsets, which beat edges an onset lands on (SFX sync), silence share,
  level per beat; optional transcript (voice-over);
- `overview.jpg` (every beat's middle frame), `timeline.jpg` (a still every 0.5 s), and `frames/` — three full-resolution
  stills per beat (in, middle, out).

## 2. Look at every beat
Read `timeline.jpg` for the whole arc, `overview.jpg` for the beat map, then the full-resolution stills of each beat
(in, middle, out — the out frame shows where the motion lands and how it leaves). Read small UI text at full size.
If the measured beat map disagrees with what you see (a beat that is two moves, two beats that are one), trust the
frames and say so.

## 3. Write the breakdown (brief.json — every field filled)
Top line: total duration · resolution · fps · the visual style in ONE line · pacing (measured: cuts/10 s, mean beat) ·
the recurring motif (the device that comes back: an accent colour, a shape, a camera move, a type treatment).
Per beat:
| field | what it must say |
|---|---|
| time | t0–t1 (from the analysis) |
| composition | framing, aspect, layout grid, where the focal point sits, depth layers |
| camera | locked / push / pull / pan / orbit / parallax, speed, depth of field, focal point |
| subjects | every object, icon, illustration, photo or 3D element: shape, style, position (thirds / % of frame), size |
| text | the exact wording (or its role, if it is the original's copyrighted copy you will not reuse) |
| typography | family class (serif / grotesk / geometric / mono / display), weight, style, size hierarchy in px at 1080p, colour hex, tracking, animation |
| icons_ui | geometry: corner radii, stroke widths, fills, shadows, chips, buttons, device frames, states (pressed, toggled) |
| lighting_texture | key/fill/rim, colour temperature, gradients with hex stops, shadows (blur, opacity), grain, glow, vignette |
| motion | the move, its distance, duration, easing (ease-out, spring with overshoot, linear), stagger between items |
| transition_out | how it hands over to the next beat (cut, dissolve and its length, push, match cut, dip, morph) |
| audio | music character, SFX on this beat and what they are synced to, voice-over line |
Plus: `style_line` (one dense sentence: mood, lighting, colour grading, camera, finish quality), `typography_lock`
(one line that fixes every type style for the whole film), `sound_line` (the bed, its tempo and level, the SFX palette,
the voice), `final_frame` (the last held frame, exactly).

## 4. The generation prompt
`kmotion omniprompt NAME.breakdown/brief.json [--overrides changes.json]` writes ONE block, no questions, no commentary:
`STYLE:` · `SPECS:` (resolution ≥ 1080 on the short side, aspect, fps, duration — a longer source is compressed
proportionally to Omni Flash's native 10 s and the factor is stated) · `TIMELINE:` one line per beat with scaled
times, colours, typography, icon/shape geometry, motion, exit · `ADD:` · `BRAND MARK:` · `TYPOGRAPHY LOCK:` ·
`SOUND:` with cues on the same scaled beats · `FINAL FRAME:` · `EXCLUDE:`.
Custom changes are applied before writing (brand name/logo, palette mapping, text/copy, duration, aspect, tone,
whole style line, elements to add or remove); everything not changed stays faithful to the analysis. Removing a
subject the scenes are built on stops the build: rewrite those beats in a copy of brief.json first (a find-and-replace
would make "a coffee cup gallop").
Recreate style, pacing and structure — not the original's copyrighted specifics (its logo, characters, exact copy,
footage) unless they are the user's own.

## 5. Rebuild with the engine instead (when the user wants the film, not a prompt)
The same breakdown drives a KOSIF composition: `kmotion new` / `template` / `timeline`, beat times as the timeline,
the typography lock as CSS, the palette as `:root` variables, the SFX cues as `audio.sfx`; review rounds with
`kmotion preview`, delivery with `kmotion final` (lossless capture, CRF 16, ≥ 1080, poster, gate).

## 6. Many references at once
`kmotion analyze --batch FOLDER --out style-library` measures every video (no stills kept) into `library.json` /
`library.csv`: pace, beats, cut rate, palette, motion energy, loudness, tempo, transitions. Use it to find the house
style of a set of references (median beat length, typical palette, how often they cut, how loud they are) before
designing a new film in that family, and pick the closest references to analyse in full.

## Habits that make the analysis good
- Every second of the film is covered; the end card and the last held frame matter as much as the hook.
- Numbers over adjectives: px, %, s, hex, BPM, LUFS, easing names.
- Say what was measured and what was judged by eye; when a value is a guess, mark it "≈".
- Motion graphics are built from entrances: describe each element's entry, hold and exit, not only the layout.
- Note the readability rhythm: how long each line stays settled (≈ 0.3 s a word is the floor).
- Sound is part of the edit: which cuts land on beats, which entrances have an SFX, where the music lifts.
