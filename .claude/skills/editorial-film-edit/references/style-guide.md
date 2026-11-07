# Style guide — soft archival editorial

The values below are the defaults of the bundled browser modules (`implementation/browser-reference/`). They describe the look; the new source decides the content.

## Picture
- **Grain**: real film grain that changes every frame and is sampled in film coordinates (it moves with the gate weave, never slides over the picture as a static overlay). Two octaves: fine ≈1.15 px cells carry most of the variance, coarse ≈2.6 px cells only ≈10 %. Less grain in deep shadows and highlights. Never repeat the grain sequence (no frame-index modulo).
- **Bloom / halation**: bright-pass → quarter-resolution Gaussian blur → added back softly around highlights. Subtle on faces; stronger on lamps, screens, windows.
- **Grade**: three looks — documentary colour, light neutral black & white, film print. Keep skin natural; B&W is neutral, not blue or sepia, unless the story asks.
- **Archive age** (for inserts only, not the presenter): light gate weave, softness, rare dust and scratches, gentle vignette. The presenter stays clean and sharp.
- **Flash**: a short white flash is a transition accent, used rarely.

## Colour
Paper `#f2efe8`, ink `#111114`, one accent orange `#ff5a1f`, neon red `#ff2a3d` for warnings/emphasis, white. One accent colour per scene.

## Type (three families only)
| Role | Family (fallbacks) |
|---|---|
| Sans: captions, heavy words, UI | Helvetica Neue → Helvetica → Arial |
| Display serif + italic accents, numerals | Didot → Bodoni 72 → Bodoni Moda |
| Mono: credits, sources, typewriter | Menlo → SF Mono → DejaVu Sans Mono |

Heavy words are weight 800 of the sans, not a fourth family. For Arabic, pair a clean Arabic sans (e.g. IBM Plex Sans Arabic / Noto Sans Arabic) with an Arabic display face (e.g. Amiri) and keep the same three roles.

## Captions
- Words appear one by one **in their final position** exactly when spoken; lines are justified to a shared width.
- Key words: italic display serif at ≈1.2× size.
- Arrival: expo-out ≈0.24 s with a small rise and light blur; the whole block drifts up very slowly (≈0.025 em/s) while on screen.
- A caption chunk keeps one position for its whole life, also across a picture cut.

## Emphasis type layers
Enter: `soft`, `blur`, `rise`, `cut`, `type` (typewriter), `wipe`, `slam`, `pop`, `blurpop`, `draw`, `flicker`. Exit: `cut`, `blur`, `fade`, `drift`.
Continuous motion (drift, sway, track) runs over the layer's whole life and does not reset at cuts. `*word*` = italic serif accent. Optional stop-motion stepping (`posterize`) affects only the type, never the picture.

## Splits and masks
- Horizontal split with one presenter: a restrained push entry (≈0.4 s, sine in-out). The insert keeps its final crop; the presenter is re-cropped, never squeezed.
- Masks: clean, feathered edges; check both sides of every transition for stray frames from adjacent takes.

## Motion and timing
Everything is a function of programme time, so preview, scrubbing and render match. Prefer expo/cubic-out entrances and one overshoot spring at most. Long videos get fewer inserts and more reading time.

## Sound
Keep the original speech and its timing. Music, if added, sits under the voice (duck it); always deliver a version without music too.
