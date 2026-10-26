# Launch videos — the /brag method on the KOSIF engine

Adapted from /brag by Shunit Haviv Hakimi (https://github.com/latent-spaces/brag, MIT, commit 7079945). KOSIF keeps
the method and swaps the runtime: compositions are KOSIF projects (`kmotion new` / `template` / `timeline`), the gate is
`kmotion inspect`, and everything is Arabic-first.

## Flow
1. `kmotion brag init DIR|URL --tone T --format landscape|vertical|square --duration 20`
   writes `brag-output/` (timestamped when one exists): `material.json` (title, description, headings, calls to action,
   colours incl. oklch/rgb/hsl → hex and named CSS variables, fonts incl. `var(--x)`, images) and `brag-plan.md`
   (rubric, shape, storyboard table, laws). A URL is fetched once; a JavaScript-built page is flagged — render it.
2. Answer the 9-question rubric, then fill the storyboard. **Plan the hook first.**
3. Build with the engine. Reuse the product's real copy, colours, fonts and images — never invent claims, numbers or
   testimonials. Sound: `kmotion sfx` + `audio.sfx` in a timeline (`kit:NAME`, cue at the START of the motion).
4. Before the full render: stills from every scene and from mid-transition; fix overflow, collisions, low contrast.
   `kmotion readable reel.json|verse.json|edit.json` — every line settled ≥ max(0.8 s, 0.3 s × words); hook ≤ 2 s.
5. `kmotion brag deliver brag-output --film film.mp4 [--at T]` → `brag.mp4` with the poster baked as frame 0 (same
   frames, same duration, sound copied), `brag.jpg`, the gate, and `share-copy.txt` checked (1–3 sentences, ≤ 280
   characters, no "excited to share" / «يسعدنا أن نعلن»). `kmotion poster FILM --bake` does the poster alone.

## Shape
Hook (2–3 s) → Reveal (2–4 s) → 2–3 sharp highlights → Punchline / outro (2–4 s). 15–25 s; 18–22 is the sweet spot.

## Tones
| Tone | Feel | Pacing / transitions | Sound |
|---|---|---|---|
| default | punchy, playful, clean | 4–5 scenes; soft transitions | 3–5 cues: drop/click pop-ins, reveal, bell on success |
| polished | serious, elegant | 3–4 scenes, long holds; soft fades | 2–3 subtle: bong, drop-1 |
| yc-parody | deadpan launch, played straight | 4–5 scenes, one claim each; hard cuts | one reveal, one card, one payoff |
| chaotic | FAST, LOUD | 6–8 scenes, some < 2 s; flash/zoom cuts | dense; glitch accents |
| deadpan | calm, dry | 3–4 scenes, empty space; slow fades | a quiet bed + 1–2 dry cues |
| cinematic | trailer-scale | 4–5 scenes, big type; dramatic wipes | bell-1 hero, reveal, bell-2 out |
| app-store | clean feature cards | 4–6 scenes; smooth slides | drop/click per card, bell-1 out |

## Laws
- Clear to a stranger after one viewing: what it is, who it is for, how to get it.
- Show the thing: the working product doing its job beats a landing page describing it. No abstract filler.
- Specific: its own copy; no generic SaaS language.
- Readable: pace comes from motion and cuts, not from pulling text away early. Fast in, then hold.
- Alive: one-by-one reveals, simulated taps, swipes, typing. Every frozen frame postable.
- Humour comes from the project's own absurdity.
- Sound and music are one piece: effects soft under the bed, in the same space; fewer cues, better timed.
- No muddy crossfade between two busy layouts: stagger (old out, then new in) or dip through the background.
- Arabic: RTL lines, no letter-spacing on Arabic, the product's Arabic font (else Cairo), numbers LTR.

## Sound kit (`scripts/kit/sfx`, CC0)
Kenney (kenney.nl) and Keyboard Soundpack #1 (unicae_games), chosen with /brag's analysis (`catalog.json`: duration,
brightness, high-frequency risk). Prefer low-risk sounds for polished films and repeated cues; `card-place` and `chips`
are bright — tiny accents only. /brag's music is not included (no redistribution licence stated); use `kmotion score`.
