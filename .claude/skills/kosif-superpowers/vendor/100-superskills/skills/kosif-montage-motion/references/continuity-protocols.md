# Continuity protocols

## 360° Reference Sheet (anti-drift)
Create once, reuse verbatim.

**Character — `CHR-001`**
- Name · age range · build · skin/hair/eye colour · distinguishing marks (be concrete, no vague adjectives)
- Views: front · ¾ left · profile · back · full-body contrapposto pose
- Expressions: neutral · joy · anger · fear · determination
- Wardrobe: items with fabric, colour, wear; accessories
- **Lock text** (one paragraph, copy-pasted into every prompt)

**Location — `LOC-001`**
- Place, era, scale, layout (left/right/centre landmarks), HDRI-style 360° description, key props, time-of-day variants
- **Lock text**

Why: image/video models re-invent details each call; a verbatim lock plus a reference image is the strongest consistency lever. Reference images, when the platform supports them, beat words — say which platform feature to use and verify it live.

## Frame stitching for long video
1. Split the scene into short chunks (the user's protocol uses ~5-second chunks; use the platform's real maximum and say so).
2. For each chunk define: start state, action, end state, camera move.
3. Chunk *n+1* starts from the **last frame** of chunk *n* (use it as the image/first-frame input when the platform allows).
4. Repeat the character/location locks and the lighting direction in every chunk.
5. Cut on motion or on a hard visual match; avoid stitching mid-gesture.
6. Audio direction is written per chunk and re-checked at the join.
7. After generation, compare first/last frames of adjacent chunks (`kosif_image_analyze compare_with`) — brightness, colour temperature and framing should not jump.

## Continuity checklist
Same lock text · same light direction and Kelvin · same wardrobe state (dirt, tears persist) · same time of day · same props in the same hand · screen direction preserved (180° rule) · same aspect and frame rate.

## 9-step visible reasoning (optional output style)
Understand → intent → retrieve sources (corpus search) → analyse conflicts → synthesise → generate → verify → attach sources → final polish. Show it only when the user asks for transparent reasoning; keep private deliberation private and surface conclusions, assumptions and sources.
