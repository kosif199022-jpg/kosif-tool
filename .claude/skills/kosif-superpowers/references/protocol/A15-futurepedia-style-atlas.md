# A15 — Futurepedia AI Style Atlas: all 86 methods + the KOSIF explainer engine

> **متى تقرأه / when to read:** أي طلب لأسلوب بصري أو فيلم شرح (explainer) أو دمج أساليب الرسم/الموشن/المونتاج؛ «سبورة، طباشير، نيون، نوار، أيزومتري، بكسل، صلصال، مانغا، ريزو، خريطة، تيليتكست…»؛ أو طلب «أساليب Futurepedia». Any request for a visual style, an animated explainer, or a fusion of looks.
>
> **Canonical routing:** [PROTOCOL.md](../../PROTOCOL.md) → [A14 drawing academy](A14-drawing-cinematic-academy.md) → [A8 motion brain](A8-motion-brain.md).

## الفهرس / contents

1. [Provenance and boundary](#provenance-and-boundary)
2. [What the atlas taught (method layer)](#what-the-atlas-taught-method-layer)
3. [The KOSIF explainer engine (execution layer)](#the-kosif-explainer-engine-execution-layer)
4. [Medium-native grammar: transitions, arrows, labels, counters, emphasis](#medium-native-grammar)
5. [Finishing passes and render techniques](#finishing-passes-and-render-techniques)
6. [Sound design](#sound-design)
7. [Catalog: 86 methods in 14 families](#catalog-86-methods-in-14-families)
8. [Commands](#commands)
9. [Acceptance gates](#acceptance-gates)
10. [Refreshing the catalog](#refreshing-the-catalog)

## Provenance and boundary

Source page: https://www.futurepedia.io/resources/ai-style-atlas/view — reviewed **in full on 2026-10-23 (86 of 86 styles, 14 families)** in a browser session. Each style there offers an explainer video, a short style clip, a poster, and a *Copy prompt* payload (67–124k characters) made of: a shared workflow brief, a per-style **style card** (name, family, look, motion, how it explains), a shared ~7k-char canvas helper library, a shared ~22k-char synthesized Web-Audio sound kit, and a 31–87k-char per-style reference animation source.

What this skill keeps: **paraphrased** method cards (look / motion / explainer grammar / Arabic capability line) and **factual observations** from analysing every payload — fonts loaded, the most frequent colours, canvas compositing modes, render techniques, named sounds and beds, helper-function names (as recipe hints). What it does **not** keep: any prompt text, reference source code, video, poster or sound. The engine below is original KOSIF code written from the observed *contract*, not from the reference files (repo rule: no third-party prompts, code or media without a compatible licence).

Data: [`data/futurepedia_style_atlas_86.json`](../../data/futurepedia_style_atlas_86.json) (schema `kosif.style.atlas.v2`). The earlier 15-entry file [`data/futurepedia_style_methods_15.json`](../../data/futurepedia_style_methods_15.json) stays valid (same IDs/slugs FA-01..15) for older recipes.

## What the atlas taught (method layer)

The atlas is not 86 prompts — it is **one production contract applied to 86 media**. KOSIF's version of that contract (`PRODUCTION_CONTRACT` in `scripts/style_atlas_bridge.py`):

| rule | KOSIF contract |
|---|---|
| storyboard first | 6–10 beats; one key frame per beat drawn with the *real* style functions; caption = beat number, start–end, on-screen text, how it connects to the previous beat (continuous carry-over vs. scene change and why), key sounds; list assumed facts; wait for OK, then reuse the same drawing code |
| canvas + player | 1280×720 logical canvas, letterboxed; play/pause, scrub, time, sound toggle, loop on; expose `window.seek(t)`, `window.DURATION`, `window.scoreSound` |
| determinism | every frame is a pure function of t; seeded random/noise only; static textures may be cached |
| legibility (phone first) | headlines ≥44 px, story-critical labels ≥28 px, key numbers ≥64 px; each beat fills most of the frame; <100 ms per frame |
| medium truth | keep surface texture + finishing passes on **every** frame; change only story, text, subjects; draw subjects accurately; check facts; don't carry over the reference's props |
| structure | hook gone in ~2 s; something changes every 1–2 s; arrows draw on for cause/flow; labels land on what they name; counters tick ≤12/s and ease into the value |
| flow | ideas that build stay continuous (elements move/grow/transform, camera travels the same world); real topic jumps get a full scene change **in the medium's own way**; mix both |
| sound | frame-exact with picture times; score landings; quiet medium-true bed; music ≤0.6 only if it suits; ≤3 sounds at once with small silences; voice-over mode ducks |
| render | headless Chromium → `seek(i/fps)` → frames → ffmpeg; offline-render the score to WAV and mux |

## The KOSIF explainer engine (execution layer)

| file | role |
|---|---|
| [`assets/atlas_harness.js`](../../assets/atlas_harness.js) | `KH`: seeded rng, gradient noise + fbm + curl, easing (incl. spring, steps, back, elastic), `span/onFps/beats` timeline helpers, colour mix, cached layers, finishing passes (`grain`, `paper`, `vignette`, `bloom`, `misregister`, `halftone`), drawing vocabulary (`wobble`, `drawOn`, `roughStroke`, `arrowHead`, `typeOn`, `counter`, `fitText`), 2D camera (`camera`, `camAt`) and a 3D `project` |
| [`assets/atlas_sound.js`](../../assets/atlas_sound.js) | `KSound`: synthesized kit — 37 named sounds (pop, tick, click, tock, blip, whoosh, swish, riser, thud, impact, stamp, ding, success, error, buzz, sparkle, glitch, shutter, count, stroke with 8 materials, paper, slap, tape, press, erase, typing, bell, boot, crtOn, neon, coin, jump, hurt, powerup, select, drip, chime), 8 beds (room, hiss, hum, rain, projector, vinyl, water, wind), 3 music beds (pad, pulse, chip), buses + compressor + reverb, voice-over mode, `live()` and `renderOffline()` |
| [`templates/atlas_explainer.html`](../../templates/atlas_explainer.html) | the player + a complete working demo (FA-23 Chalkboard, Arabic «كيف يتعلّم الذكاء الاصطناعي؟», 6 beats, 17 s, camera travelling one long slate); `?storyboard=1` renders the approval grid |
| [`scripts/atlas_render.py`](../../scripts/atlas_render.py) | `check` (determinism + ms/frame), `storyboard`, `still`, `render` (MP4 with muxed score; `--voiceover` ducking), `bundle` (single self-contained HTML) |
| [`scripts/style_atlas_bridge.py`](../../scripts/style_atlas_bridge.py) | `list`, `families`, `search` (Arabic aliases), `show`, `plan` (85/15 fusion recipe), `brief` (storyboard-first production brief), `scaffold` (engine + style card wired into a new project), `study-svg` |

Proof: [proofs/style-atlas-86](../../proofs/style-atlas-86/README.md) — 510 frames, 1280×720, h264 + aac, deterministic, 29 ms/frame.

## Medium-native grammar

The deepest lesson of the atlas: **every device of an explainer is rebuilt in the medium's own material.** Use this table to invent the grammar for any new look.

| device | examples from the 86 methods |
|---|---|
| scene change | eraser wipe leaving ghost residue (whiteboard), lamp dimmed/raised or curtains (shadow puppet), plates sliding off and re-registering (riso), proof peeled off (linocut), new sheet slapped on (zine, napkin), page turn (manga, newsprint, sketchbook), card flip (holo, tarot), V-hold roll (CRT), NUC shutter click (thermal), tape cut / fast-forward (vaporwave), palette fade (handheld), mosaic or battle swirl (16-bit), gold elevator doors (art deco), red wedge (constructivist), kaleidoscope (psychedelic), tesserae pried up (mosaic), re-dab sweep (pointillism), shake (etch toy), whip-pan smears (light painting, neon), descent (deep sea), page number search (teletext) |
| arrow / flow | marker or chalk strokes, loaded brush strokes, rolled clay coils, creased paper strips, gouged channels, glass strips in lead, chase-light tubes, beam strokes, thread with nail barbs, stitched backstitch, chains of voxels, flat isotype arrows, metro lines, light pulses on connectors, ribbons, ruled leaders |
| label | tags dropped onto the thing, plaques on strings, mugshot placards, tent cards, woven tags, kraft tags, grease pencil, inverse-video status line, bracketed HUD tags, pills, katakana SFX, sticky notes |
| counter | re-written by hand each change, rolling odometer, swapped cut digits, re-stamped type, 7-segment from thread, LED pixel stick, tape counter, dot-matrix board, inflated chrome digits, sampler-font stitches |
| emphasis | coloured ring (chalk, red pen, alizarin, grease pencil), rubber stamp, highlighter sweep, seal stamp, starburst, spotlight, bloom flare, focus-line burst, flash attribute, WRONG burst + shake |
| model / metaphor | a physical object whose parts are the weights: knobs, moons, buttons with thread X, string wraps, Truchet tiles, lathe rosette, marbling bath, flow-field core, jellyfish nerve net, lens sphere |

## Finishing passes and render techniques

Observed frequency across the 86 references (a technique appears in N styles): pixel-level ops 70 · linear gradients 69 · seeded noise 69 · radial gradients 66 · bezier paths 66 · clip masks 64 · blur filter 55 · vignette 50 · grain 43 · dashed strokes 31 · shadow-blur glow 31 · own 3D projection 11 · paper pass 8 · nearest-neighbour pixel scaling 7. Compositing modes used: multiply, screen, lighter (additive glow), overlay, soft-light, hard-light, color-dodge, difference, lighten, source-atop/in, destination-in/out.

Rule of thumb by family: print → misregistration + multiply + paper; light & imaging → additive `lighter` + bloom + vignette; retro digital → nearest-neighbour scaling + scanline/CRT pass; painterly → layered low-alpha strokes + paper; dimensional → own projection + depth sort; data → hairline vectors + quiet grain.

## Sound design

Use `KSound` names that match the medium (chalk → `stroke {material:'chalk'}` + `tick`; print → `press`, `stamp`, `slap`, `paper`; screens → `crtOn`, `blip`, `typing`, `glitch`; games → `coin`, `jump`, `hurt`, `powerup`, `select`; reveals → `ding`, `success`, `sparkle`). Observed beds in the references: room (most), hum, hiss, projector, vinyl; music beds: pad, pulse. Keep ≤3 simultaneous sounds and let silence frame the big hits.

## Catalog: 86 methods in 14 families

**Popular Explainer Looks — أشكال الشرح الشائعة (7)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-01 | Flat-Vector Science | رسوم علمية مسطحة بتدرجات فضائية وشخصيات دائرية لطيفة | Fredoka, Nunito | PX, RAD, LIN, NOISE, CLIP |
| FA-06 | Tech Glow Explainer | موشن تقني بتوهج وعُقد متصلة ونبضات ضوء | Inter, Space Grotesk | BLUR, SHB, RAD, LIN, VIG |
| FA-07 | Papercraft Models | نماذج كرتون مطبوعة تنطوي وتتجمع ثلاثية الأبعاد | Fredoka, Space Grotesk, Space Mono | BLUR, RAD, LIN, NOISE, GRAIN |
| FA-09 | Manim-Style Math | رياضيات متحركة بأسلوب Manim: معادلات تُكتب ومحاور ومنحنيات | STIX Two Text | DASH, CURVE |
| FA-11 | Editorial Essay Collage | كولاج مقالات تحريرية بقصاصات وهايلايتر | Anton, Libre Baskerville, Oswald | PX, BLUR, SHB, RAD, LIN |
| FA-13 | Product Launch Reveal | عرض منتج فاخر بإضاءة استوديو وانعكاسات | Inter | PX, BLUR, SHB, RAD, LIN |
| FA-20 | Kawaii Anime | أنمي كاواي بشخصيات تشيبي وألوان حلوى | Fredoka, Zen Maru Gothic | SHB, RAD, LIN, CURVE |

**Painterly — تصوير زيتي/مائي (6)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-02 | Watercolor Wash | ألوان مائية شفافة بطبقات وحواف صبغة على ورق | Caveat | PX, BLUR, RAD, LIN, CLIP |
| FA-25 | Cathedral Glass | زجاج معشق كاتدرائي مضاء | Cormorant Garamond, UnifrakturMaguntia | PX, BLUR, SHB, RAD, LIN |
| FA-32 | Sumi-e Ink Wash | حبر سومي ياباني بغسلات رمادية وفراغ | Cormorant Garamond, Noto Serif JP | PX, BLUR, SHB, RAD, LIN |
| FA-38 | Impasto Night | ألوان زيتية كثيفة بضربات دوامية | Fraunces | PX, BLUR, NOSMOOTH, RAD, LIN |
| FA-49 | Gouache Travel Poster | ملصق سفر جواش بألوان مسطحة معتمة | Bebas Neue, Oswald | PX, BLUR, NOISE, CLIP, CURVE |
| FA-71 | Pointillist Afternoon | تنقيطية بنقاط لون صافٍ متجاورة | Playfair Display | PX, BLUR, SHB, RAD, LIN |

**Paper & Craft — ورق وحِرف (7)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-03 | Shadow Puppet Theatre | مسرح ظل بقصاصات سوداء مفصلية أمام ستارة مضاءة | IM Fell English, Libre Baskerville | PX, BLUR, RAD, NOISE, VIG |
| FA-18 | Claymation Set | صلصال ستوب موشن ببصمات وأسطح شمعية | Fredoka | PX, BLUR, SHB, RAD, LIN |
| FA-24 | Cut-Paper Diorama | ديوراما ورق مقصوص بطبقات وظلال | Archivo Black | PX, SHB, RAD, NOISE, GRAIN |
| FA-28 | Origami Studio | أوريغامي ورق مطوي بإضاءة استوديو | Space Grotesk, Space Mono | PX, BLUR, RAD, LIN, NOISE |
| FA-35 | Punk Zine Collage | زين بانك مصور بقصاصات وحروف فدية | Abril Fatface, Anton, Archivo Black | PX, RAD, LIN, NOISE, CLIP |
| FA-44 | Felt & Patchwork | لحاف مرقع ولباد مخيط بالغرز | Fredoka | PX, BLUR, SHB, RAD, LIN |
| FA-57 | Cross-Stitch Sampler | تطريز كروس ستيتش على قماش في طارة | — | PX, SHB, RAD, LIN, NOISE |

**Hand-Drawn — رسم يدوي (7)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-04 | Whiteboard Explainer | سبورة بيضاء بقلم ماركر يرسم مباشرة مع أثر المسح | Kalam, Permanent Marker | BLUR, RAD, LIN, NOISE, GRAIN |
| FA-23 | Chalkboard Lesson | سبورة طباشير خضراء بغبار وآثار مسح | Kalam, Patrick Hand | PX, BLUR, RAD, LIN, NOISE |
| FA-33 | Etch A Sketch Toy | لعبة الرسم بخط واحد متصل ومقبضين | — | PX, SHB, RAD, LIN, NOISE |
| FA-37 | Engineering Blueprint | مخطط هندسي سيانوتايب بخطوط بيضاء | IBM Plex Mono, Space Mono | PX, BLUR, RAD, LIN, NOISE |
| FA-50 | Napkin Sketch | رسم على منديل مقهى بقلم ماركر | Permanent Marker | PX, BLUR, RAD, LIN, NOISE |
| FA-68 | Ballpoint Notebook | دفتر بقلم جاف أزرق بتظليل متقاطع | Fredoka, Gloria Hallelujah | PX, BLUR, RAD, LIN, NOISE |
| FA-78 | Sketchbook Graphite | رسم رصاص في كراسة بخطوط إنشائية | Caveat, IBM Plex Mono | PX, BLUR, RAD, LIN, NOISE |

**Cosmic & Psychedelic — كوني وسايكيديلك (2)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-05 | Psychedelic Poster | بوستر سايكيديلك بألوان متضادة ودوامات سائلة وتناظر | Righteous, Shrikhand | PX, LIN, NOISE, VIG, CLIP |
| FA-34 | Cosmic Star Chart | خريطة نجمية كونية مع سدم ومدارات منقوشة | Cormorant Garamond, Libre Baskerville, Syne | PX, SHB, RAD, LIN, NOISE |

**Light & Imaging — ضوء وتصوير (7)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-08 | 1940s Film Noir | فيلم نوار أبيض وأسود بظلال الستائر وحبيبات الفيلم | Anton, Courier Prime, Limelight | PX, BLUR, SHB, RAD, LIN |
| FA-12 | Bioluminescent Deep Sea | أعماق البحر بإضاءة حيوية متوهجة على أسود | Fraunces, IBM Plex Mono, Space Grotesk | PX, BLUR, SHB, RAD, LIN |
| FA-19 | Neon Sign at Night | لافتة نيون ليلية على طوب مبلل | Gloria Hallelujah, Poiret One | PX, BLUR, LIN, NOISE, GRAIN |
| FA-30 | Holographic Foil Card | بطاقة هولوغرام بقوس قزح متغير وزوايا لامعة | Inter, Russo One | PX, BLUR, RAD, LIN, NOISE |
| FA-36 | Thermal Camera | كاميرا حرارية بلوحة ألوان حديدية وواجهة قياس | IBM Plex Mono, Inter | PX, BLUR, RAD, LIN, NOISE |
| FA-43 | Light Painting | رسم بالضوء بتعريض طويل وشرائط ملونة | Caveat | PX, BLUR, RAD, LIN, NOISE |
| FA-52 | Radiograph on Lightbox | صورة أشعة سينية على صندوق إضاءة | Caveat, Courier Prime, Permanent Marker | PX, BLUR, LIN, NOISE, GRAIN |

**Illustration — رسم توضيحي (7)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-10 | Illuminated Manuscript | مخطوطة مذهبة بحروف أولى مزخرفة وورق رق | IM Fell English, Grenze Gotisch, UnifrakturMaguntia | PX, BLUR, SHB, RAD, LIN |
| FA-41 | Manga Page | صفحة مانغا بخطوط تركيز وتون نقطي | Archivo Black, Patrick Hand, VT323 | PX, BLUR, RAD, LIN, NOISE |
| FA-47 | Tarot Card | بطاقة تاروت آرت نوفو بذهب ومخمل | Cormorant Garamond | PX, BLUR, RAD, LIN, NOISE |
| FA-60 | Botanical Plate | لوحة نباتية محفورة ملونة يدويًا | Cormorant Garamond, Libre Baskerville | PX, BLUR, RAD, LIN, NOISE |
| FA-62 | Byzantine Mosaic | فسيفساء بيزنطية بقطع ذهبية تتبع الشكل | Cormorant Garamond, Libre Baskerville | PX, NOSMOOTH, RAD, LIN, NOISE |
| FA-64 | Sticky-Note Wall | حائط ملاحظات لاصقة وخيوط حمراء | Caveat, Gloria Hallelujah, Kalam | PX, BLUR, RAD, LIN, NOISE |
| FA-73 | Patent Drawing | رسم براءة اختراع بخطوط حبر وتظليل | Cormorant Garamond, Courier Prime, Libre Baskerville | PX, BLUR, RAD, LIN, NOISE |

**Print — طباعة (6)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-14 | Halftone Pop Panel | لوحة كوميكس بنقاط هاف تون وخطوط حبر سميكة | Bangers | PX, NOISE, CLIP, DASH, CURVE |
| FA-17 | Risograph Zine | طباعة ريزوغراف بأحبار فلورية وانزياح تسجيل | Archivo Black, Space Mono | PX, RAD, LIN, NOISE, CLIP |
| FA-29 | Linocut Relief Print | حفر لينو بطبعتين أحمر وأسود | Archivo Black, Caveat, Kalam | PX, BLUR, NOISE, VIG, CLIP |
| FA-42 | Wood Type Letterpress | طباعة حروف خشبية بحبرين وانطباع عميق | Abril Fatface, Anton, Bebas Neue | PX, BLUR, SHB, RAD, NOISE |
| FA-65 | Vintage Newsprint | صفحة جريدة قديمة بعنوان عريض وصورة نقطية | Libre Baskerville, Oswald, Playfair Display | PX, BLUR, SHB, RAD, LIN |
| FA-80 | Silkscreen Grid | طباعة سلك سكرين متكررة بألوان صارخة | Anton | PX, RAD, LIN, NOISE, CLIP |

**Dimensional — أبعاد ثلاثية (6)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-15 | Isometric Pastel | رسم أيزومتري باستيل بإسقاط 30 درجة | Inter | BLUR, SHB, RAD, LIN, CLIP |
| FA-31 | Voxel Diorama | ديوراما فوكسل بمكعبات وظلال لعبة | Fredoka, Silkscreen | PX, BLUR, SHB, RAD, LIN |
| FA-40 | Low-Poly Faceted | لو بولي ثلاثي الأبعاد بأوجه مسطحة وضباب | Space Grotesk | RAD, LIN, NOISE, 3D, CLIP |
| FA-46 | Glassmorphism UI | واجهة زجاج مصنفر فوق تدرجات حية | Inter | PX, BLUR, SHB, RAD, LIN |
| FA-56 | Soft 3D Clay | أيقونات ثلاثية ناعمة كالصلصال الباستيل | Fredoka | BLUR, SHB, RAD, LIN, GRAIN |
| FA-66 | Hidden-Line Wireframe | تضاريس سلكية بإزالة الخطوط المخفية | IBM Plex Mono, Space Mono | BLUR, SHB, RAD, LIN, NOISE |

**Retro Digital — رقمي كلاسيكي (7)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-16 | Oscilloscope Vector Art | رسم بشعاع راسم الذبذبات الأخضر | Inter, Space Grotesk | BLUR, SHB, RAD, LIN, NOISE |
| FA-22 | 16-Bit Pixel Odyssey | بكسل آرت 16 بت بأسلوب ألعاب RPG | Press Start 2P | PX, NOSMOOTH, NOISE, 3D |
| FA-45 | Phosphor Terminal | شاشة طرفية فوسفورية خضراء بانحناء CRT | Space Mono, VT323 | PX, BLUR, SHB, RAD, LIN |
| FA-59 | Pocket Monochrome | شاشة جيم بوي بأربع درجات أخضر | Inter, Press Start 2P | PX, SHB, RAD, LIN, NOISE |
| FA-72 | Vector Arcade 1980 | ألعاب أركيد فيكتور بخطوط فوسفورية | — | PX, BLUR, RAD, LIN, VIG |
| FA-82 | ASCII Demoscene | ديموسين ASCII بحروف ومجسم ثلاثي | IBM Plex Mono, Press Start 2P | PX, BLUR, SHB, NOISE, VIG |
| FA-85 | MacPaint 1984 | ماك 1984 أبيض وأسود بتنقيط أتكنسون | Inter, Libre Baskerville, Silkscreen | PX, NOSMOOTH, RAD, LIN, CLIP |

**Art & Design Movements — حركات فنية وتصميم (6)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-21 | Ukiyo-e Woodblock | طباعة خشبية يابانية بأمواج وتدرج أزرق | Noto Serif JP | PX, RAD, LIN, NOISE, VIG |
| FA-51 | Art Deco Foil | آرت ديكو أسود وذهبي بأشعة متناظرة | Limelight, Poiret One | PX, RAD, LIN, NOISE, GRAIN |
| FA-58 | Constructivist Propaganda | بوستر بنائي سوفييتي أحمر وأسود بقطريات | Anton, Oswald, Russo One | PX, RAD, LIN, NOISE, GRAIN |
| FA-67 | Memphis Group | ممفيس ثمانينات بأشكال جريئة وظلال صلبة | Fredoka, Rubik Mono One | GRAIN, CURVE |
| FA-74 | Bauhaus Poster | بوستر باوهاوس بأشكال هندسية أساسية | Space Grotesk, Syne | PX, RAD, LIN, NOISE, GRAIN |
| FA-83 | International Typographic Style | طراز سويسري بشبكة 12 عمود وخط جروتسك | Inter | PX, BLUR, NOISE, VIG, CLIP |

**Data & Information — بيانات ومعلومات (6)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-26 | Editorial Chart | رسم بياني صحفي فاخر بخط واحد مميز | Caveat, Inter, Libre Baskerville | LIN, GRAIN, CLIP, DASH, CURVE |
| FA-48 | Transit Map | خريطة مترو بخطوط ملونة 45 درجة | Inter, Libre Baskerville, VT323 | PX, BLUR, NOSMOOTH, RAD, LIN |
| FA-55 | ISOTYPE Pictograms | إحصاء تصويري إيزوتايب برموز متكررة | Space Grotesk | PX, NOISE, GRAIN, PAPER, CLIP |
| FA-70 | Topographic Survey | خريطة طبوغرافية بخطوط كنتور ومسار متقطع | Inter, Libre Baskerville | PX, RAD, LIN, NOISE, GRAIN |
| FA-77 | Ridgeline | خطوط متراكبة بأسلوب الريدجلاين | Space Mono | PX, BLUR, RAD, NOISE, GRAIN |
| FA-84 | Flow Field | حقل تدفق بخطوط دقيقة حول نواة | Space Mono | BLUR, RAD, LIN, NOISE, GRAIN |

**Retro UI & Neon — واجهات قديمة ونيون (6)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-27 | Synthwave Outrun | سينث ويف ثمانينات بشبكة نيون وشمس مخططة | Caveat, Orbitron | BLUR, SHB, RAD, LIN, NOISE |
| FA-39 | Win95 Desktop | سطح مكتب ويندوز 95 بأزرار مشطوفة | Inter | PX, NOSMOOTH |
| FA-53 | Vaporwave | فيبورويف بألوان باستيل نيون وتشويش VHS | Inter, Noto Serif JP, VT323 | PX, BLUR, SHB, RAD, LIN |
| FA-63 | Y2K Liquid Chrome | كروم سائل Y2K بفقاعات وانعكاسات قزحية | Fredoka, Orbitron, Space Grotesk | PX, BLUR, SHB, RAD, LIN |
| FA-75 | Bitmap Paint Doodle | رسم بالرسام القديم ببكسلات ودلو تعبئة | Inter, Patrick Hand | PX, NOSMOOTH, LIN, CLIP |
| FA-79 | Teletext Page | صفحة تيليتكست بشبكة 40×25 وثمانية ألوان | Archivo Black, VT323 | PX, BLUR, SHB, RAD, LIN |

**Generative & Type — توليدي وحروف (6)**

| ID | method | القدرة | fonts | key techniques |
|---|---|---|---|---|
| FA-54 | Ebru Paper Marbling | رخامة الإبرو التركية بتحويلات القطرات والمشط | Libre Baskerville | PX, BLUR, LIN, NOISE, VIG |
| FA-61 | Kinetic Type | تايبوغرافي حركي بكلمات على الإيقاع ولونين | Anton, Inter, Space Mono | NOISE, GRAIN, CLIP, DASH |
| FA-69 | Op Art Sphere | فن بصري أوب آرت بشطرنج منتفخ | Archivo Black, Space Grotesk | PX, NOISE, VIG |
| FA-76 | Nail & Thread String Art | فن الخيوط والمسامير على خشب | Caveat | PX, BLUR, RAD, LIN, NOISE |
| FA-81 | Guilloché Security Print | زخرفة غيلوشيه كالعملات الورقية | Cormorant Garamond, Courier Prime, Inter | LIN, GRAIN, PAPER, VIG, CLIP |
| FA-86 | Multi-scale Truchet | تبليط تروشيه متعدد المقاييس | Rubik Mono One | PX, NOISE, GRAIN, VIG, CLIP |

## Commands

Run from the skill folder (`.claude/skills/kosif-superpowers/`):

```bash
python3 scripts/style_atlas_bridge.py families
python3 scripts/style_atlas_bridge.py search "طباشير"
python3 scripts/style_atlas_bridge.py show FA-45
python3 scripts/style_atlas_bridge.py brief --topic "كيف تعمل البطارية" --style FA-45 --accent FA-16 --duration 20 --out out/atlas/brief.md
python3 scripts/style_atlas_bridge.py scaffold --style FA-45 --out out/atlas/battery
python3 scripts/atlas_render.py storyboard --in out/atlas/battery/explainer.html --out out/atlas/storyboard.png
python3 scripts/atlas_render.py check --in out/atlas/battery/explainer.html
python3 scripts/atlas_render.py render --in out/atlas/battery/explainer.html --out out/atlas/battery.mp4
python3 scripts/atlas_render.py bundle --in out/atlas/battery/explainer.html --out out/atlas/battery_single.html
python3 scripts/style_atlas_bridge.py plan --topic "كيف يتعلم الذكاء" --style FA-04 --accent FA-06 --out out/atlas/fusion.json
python3 -m unittest evals/test_style_atlas_bridge.py evals/test_atlas_render.py
```

Outputs never overwrite existing files (`--force` only on atlas_render). A scaffold copies the *chalkboard demo* as a working example of the contract: rewrite its medium functions, BEATS, `explainer()` and `scoreSound()` for the chosen method before rendering.

## Acceptance gates

- Registry: exactly 86 methods, IDs FA-01..FA-86, unique slugs, 14 families with the site's counts (7,6,6,7,7,6,7,6,6,7,6,6,7,2); every card has look, motion, explainer grammar, Arabic line; `executor_verified` false.
- Storyboard approved before the full build (or the user explicitly skipped it).
- `atlas_render.py check`: deterministic true, <100 ms/frame, `scoreSound` present.
- Render probe: real h264 + aac streams, expected duration; look at stills and listen before delivery.
- Legibility minimums met; Arabic shaped (render whole strings, RTL direction); facts checked for the user's topic.
- Never claim a method was "rendered" until its own page passed `check` and `render`.
- **Katana/Higgsfield:** analysis only through a verified zero-cost read-only interface; never generate or spend credits from this workflow.

## Refreshing the catalog

If the site adds styles, re-harvest in a browser tab on the atlas page (Claude in Chrome `javascript_tool`) and re-paraphrase new entries by hand; never paste their descriptions or prompts into the repo:

```js
let all = []; for (let p = 1; p <= 10; p++) { const j = await (await fetch('/api/style-atlas/styles?category=All&page=' + p)).json(); all = all.concat(j.styles); if (!j.hasMore) break; }
all.map(s => [s.order, s.styleId, s.category, s.name].join(' | ')).join('\n');
```
