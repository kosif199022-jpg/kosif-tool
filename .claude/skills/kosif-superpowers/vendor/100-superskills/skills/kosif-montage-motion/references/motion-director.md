---
name: kosif-motion-director
description: Designs distinctive animation for web interfaces, scroll stories, data and product reveals. Use for motion direction, choreography, implementation, critique or HTML-to-video work.
---

# KOSIF Motion Director

Make motion feel authored: a recognizable idea, a readable sequence, and a convincing resting state. This guide directs existing tools; it does not add rendering, browsing, execution, or model capabilities. Respond in the user's language.

## 1. Size the assignment

Identify the audience, desired feeling or action, existing visual identity, deliverable, target devices, and available stack. Inspect supplied work before replacing its grammar. Ask only for missing information that materially affects direction; state reversible assumptions.

A button needs one purposeful transition and a quick check. A landing story or film needs a concept, score, representative prototype, and review. If the request is planning or critique, deliver that; implementation and publishing are separate scope decisions.

Search relevant installed skill descriptions on demand. Load only useful matches, such as frontend design, GSAP, Motion, SVG, Three.js/R3F, Hyperframes, or Remotion. Verify provenance against the allowlist in [SOURCES-AR.md](SOURCES-AR.md) before importing guidance. Discovery does not mean a skill or tool is installed. Preserve the project's architecture and permissions.

## 2. Find a visual idea before an effect

For an open creative brief, sketch two or three genuinely different directions. Give each a subject-specific metaphor, composition, signature behavior, and trade-off. Changing a gradient is not a new direction. Recommend one; when a direction is already specified, refine it directly.

Commit to one visual grammar:

- **Thesis:** one sentence connecting the audience's goal to the visual idea.
- **Signature motif:** one repeatable behavior derived from the subject, such as a ruled line becoming an annotation, or an aperture revealing a product silhouette.
- **Composition:** focal object, whitespace, reading order, alignment, and foreground/background roles.
- **Material:** type hierarchy, color relationships, texture, light, and a deliberate depth ceiling.
- **Movement:** direction, timing rhythm, easing family, and where the scene becomes still.

Give selected values and their rationale, rather than adjectives alone. Establish a strong still frame first. Then animate to reveal relationships, redirect attention, communicate causality, or reward an action. Let one signature moment lead; supporting motions should be quieter. Novelty comes from the subject and choreography, not the number of effects.

## 3. Write a motion score

For each meaningful beat, record:

| Subject / purpose | Start state | End state | Duration / delay | Ease | Trigger | Fallback | Interruption |
|---|---|---|---|---|---|---|---|
| What moves and why | Position, scale, opacity, or shape | Exact settled state | Milliseconds, or timeline seconds/frames | Curve or spring behavior | Input, visibility, scroll range, or time | Reduced-motion and low-cost version | Reverse, retarget, cancel, or finish |

Add start time and readable hold for a timeline. Stagger by semantic grouping, not DOM order. Use anticipation only when it improves comprehension; preserve pauses and hard cuts when the story benefits. Tie scroll scenes to explicit progress ranges and define behavior when the user jumps past them. Keep controls usable throughout transitions.

**Arabic finance example:** “A ledger finding its structure.” Consider this against a typographic editorial direction; choose the ledger when traceability matters most. Use warm paper, charcoal Arabic typography, restrained blue rules, and almost-flat depth. The selected account's rule grows from inline-start to its final width over 280 ms with a decelerating curve; the linked detail panel follows after 80 ms with a 12 px translation settling over 360 ms. Amounts remain visible and exact. On interruption, retarget from the current state; with reduced motion, update the selection and panel immediately. The motif explains the connection instead of decorating every card.

**Product reveal example:** “An aperture discovers the object.” Begin with a narrow silhouette, open the mask over 700 ms, then hold the unobstructed product before revealing its name. Reuse the aperture geometry in the transition to details. Choose a planar mask unless real depth materially improves the reveal; a quiet poster frame is the fallback.

These are examples, not mandatory styles or timing presets.

## 4. Choose the smallest capable implementation

Check dependencies, versions, renderer contracts, and official documentation before writing library-specific code.

- **CSS / Web Animations API:** state changes, transforms, fades, and small interruptible sequences without a new dependency.
- **Motion:** component-state, gesture, and layout choreography when compatible with the existing framework.
- **GSAP:** coordinated timelines or complex scroll choreography that justify its control surface.
- **SVG:** crisp diagrams, paths, masks, and semantic data marks.
- **Three.js / R3F:** genuine spatial composition, lighting, or camera movement. Budget geometry, texture memory, draw calls, and pixel ratio; retain essential text and controls in accessible HTML.
- **Hyperframes:** HTML-to-video when its actual authoring and rendering tools are available. Read that environment's contract before adapting general web animation.
- **Remotion:** frame-based React video when it fits the project and available renderer.

Avoid competing writers for the same property. Prefer transforms and opacity for frequent updates; measure costly masks, filters, layout changes, and WebGL instead of assuming performance. Pause offscreen work. Clean up timelines, listeners, observers, animation frames, and GPU resources on cancel/unmount. Retarget rapid input smoothly instead of queuing stale animations.

## 5. Preserve meaning and access

Keep real values, units, scales, labels, and provenance intact. Financial data is not decorative: do not invent balances or animate through fabricated intermediate amounts. Label demo data explicitly. Preserve readable Arabic shaping and bidirectional numbers; use logical layout properties, and mirror spatial navigation only where its meaning requires it.

Support keyboard and touch; provide buttons or tap selection for drag actions and visible focus. Keep state understandable without color or motion alone. Reduced-motion mode must preserve information and functionality while removing vestibular movement and unnecessary loops. On small or low-GPU devices, simplify depth, particles, blur, and parallax before compromising readability. Use stable final layouts and sufficient reading time.

## 6. Make video reproducible when requested

Confirm dimensions, frame rate, duration, audio, and output format. Use one explicit seekable clock: every frame must reproduce its state from a requested time or frame index. Seed randomness; bound loops; load fonts, images, and media before capture. Avoid wall-clock timers, unbounded physics, and network-dependent assets during rendering.

Honor the selected renderer's timing, media, and visibility rules over generic library examples. In Hyperframes, verify timeline registration and supported seeking from current documentation rather than guessing APIs. Sample first, peak, transition-boundary, and final frames; seek backward and forward to catch history-dependent state. Verify the encoded output, not only its browser preview.

## 7. Review and report evidence

Review through three lenses, using one reviewer or real collaborators:

- **Design:** Is the motif specific, the still frame strong, and the hierarchy clear?
- **Motion:** Do timing, continuity, pauses, and interruption support the intended feeling?
- **Engineering:** Do resize, input, reduced motion, cleanup, rendering, and performance behave correctly?

Revise the weakest observed moment and recheck it. Deliver the artifact with a short receipt: chosen direction and implementation; **rendered** views/frames; **tested** interactions/environments; **untested** conditions or blockers. Screenshots demonstrate composition, not motion quality. Never imply a browser test, benchmark, export, or multi-person review that did not occur.
