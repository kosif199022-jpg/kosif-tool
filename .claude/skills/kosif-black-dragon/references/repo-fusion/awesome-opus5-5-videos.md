# awesome-opus5-5-videos (MIT, @92aee2f, ≈14.5k★) + opus-video-prompts (no license, @7977c80, ≈1k★)

## Structure
- awesome-opus5-5-videos `data/videos.json`: 703 items {slug, author, author_url, post_url, category, tech_tags[], prompt, prompt_partial, poster_url, skillry_url, added, has_remake, title(285)}; `prompts/*.md` one per item. Categories: motion 369, 3d 117, explainer 116, interactive 101. Tags: canvas 267, svg 183, threejs 131, shader 92, gsap 86, css 57, audio 39, playable 22, particles 17, pixel 15, webgl 9, physics 9, ai-image 6. 207 partial prompts (link only); median 221 chars, max 15.6k. Prompt rights stay with their authors (credit via post_url).
- opus-video-prompts (Chinese): 54 metadata rows in cases.json (category, title, author, how, cost, url), 18 prompt files, lessons in README.md:486-494. **No license → links and metadata only; no prompt text copied.**

## Prompt-writing patterns (our wording)
1. State total duration, canvas size and fps first.
2. Split into numbered scenes/beats, one idea each; best cases ask for a storyboard before code.
3. Short banned list (glow, particle bursts, bouncy easing, UI gradients): the "template look" comes from defaults.
4. Name colours and one typeface instead of adjectives.
5. Describe motion like a director: easing, spring, match cut, camera move, loop point.
6. Every frame a pure function of t (seek or ?t=), no timers/state, so frames render in parallel.
7. Fix the stack and dependency limits (single file, no external assets, or Remotion/HyperFrames).
8. Say where audio comes from (synth, TTS, file) and the tempo; a BPM grid gives each beat an event.
9. Ask the model to take screenshots and fix overlaps before the final render.
10. For templates: start with an inputs block the model must ask about.

Rule frequency in the 496 complete prompts (our regexes): duration 171, tech 138, audio 123, format 80, banned 73, loop 59, motion 54, determinism 52, verify 51, structure 50, palette 42, ask-first 39.

## Native module: `native_promptlib.py` (stdlib)
Commands: search (category/tag/keywords/author/remake), stats, lint (text or file; 12 weighted rules with tips and vague-adjective notes), patterns, self-test; `--data <videos.json>`; output is always JSON.
Self-test: `self-test OK: search/stats/lint verified; good=96% bad=0%`. Real data: explainer + "bpm" → 7 cases; a vague sentence → 0/23 with ranked tips. Lint is regex-based and tuned on English; Arabic/Chinese prompts score low.

Dragon coverage: visual-forge already lints image/Kling prompts; new = video-as-code prompt lint + searchable case index. Stages: concept, shots (lint before produce).

## REA evidence log
`open_binary` on videos.json → unsupported_target / file_format_rejected; `inspect_artifact` therefore not run; no Evidence ids. Analysis via python -I scripts and manual reading (plain JSON/Markdown).
