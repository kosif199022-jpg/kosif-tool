# Implementation guide — browser reference modules

`implementation/browser-reference/` holds layer examples for an HTML stage rendered to video (e.g. with the repo's `tools/render_html.cjs`, Playwright + ffmpeg). They are building blocks, not a finished project: you write the shot runtime, the EDL/timeline JSON and the page that wires them together.

| File | What it gives you |
|---|---|
| `engine.js` | DOM-free core. `clamp`, `lerp`, `EASE` (linear, hold, sine, cubic, quart, expo, back, spring), `ease(name,k)`, keyframe `sample(keys,t)`, `compileLayer`/`propsAt` (layer properties at time t), camera tracks (`compileCamera`, `cameraAt`, `cropFor`, `sourceRectToStage`), subject tracking (`subjectAt`), palettes (`paletteAt`), `beatAt`, `captionAt`, `posterT(t,P)` for stop-motion stepping. |
| `picture.js` | WebGL post pipeline over a 2D comp canvas: bright-pass + downsample → separable Gaussian (bloom) → main pass (gate weave, softness, bloom/halation, grade doc / B&W / film, archive age, vignette, per-frame film grain, dust/scratches, flash). Pure function of frame index. |
| `captions.js` | `new Captions(root, data, W, H)`: word-by-word justified captions with italic serif accents. Data: `{ size, chunks:[{ t0, t1, y, lines:[[wordIndex…]], words:[{ w, t0, t1, accent }] }] }`. |
| `typeLayers.js` | Emphasis type above the graded picture. Layer: `{ id, style, text, t0, t1, x, y, size, align, color, w, enter, exit, exitDur, words:[{w,t,it}], motion:{drift,sway,swayHz,track}, posterize, halo }`. Styles: `display_sans`, `display_serif`, `serif_ink`, `sans_ink`, `credit`, `heavy`, `number`, `number_ink`, `label_box`, `typewriter`, `typewriter_ink`. `meta.typeDefaults` in the EDL is merged under every layer. |
| `split-layout.js` | `splitLayout(spec, t, rect)`: geometry of a two-panel split at time t, including the presenter push entry. |
| `fonts.js` | The three font stacks (`FONT.sans/serif/mono`), `familyOf()` for font audits, `applyFontTokens()` to sync CSS variables with canvas text. |
| `reel.css` | Stage (1920×1440, 4:3), palette variables, type classes, render-mode rules that hide the editor UI. |

## Wiring
1. Page: `#stage` with the comp `<canvas>`, a WebGL canvas for `picture.js`, and DOM planes for captions and type.
2. Expose a deterministic `seek(t)` that: draws the current shot into the comp → runs the post passes for the frame index → updates captions and type layers for `t`.
3. Render frame by frame with the HTML renderer; never rely on real-time playback for the export.
4. Captions come from your own transcript (word timings: `tools/words_convert.py` converts SRT/VTT/Whisper JSON).

## Limits
- Change the stage size in `reel.css` for 9:16 or 16:9 and re-check caption widths.
- Defaults are examples; the style guide and the new source decide the final values.
