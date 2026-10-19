# PLAN.md — ما فرّق البحر بيننا (Egypt × Saudi salute)

Style base: `parallax-2d` (photos + 2.5D camera) with `kinetic-arabic` captions. 9:16 · 1080×1920 · 30 fps · 196.82 s (the song's length, nothing trimmed).
Master clock: the supplied song `assets/song.mp3` (unaltered). Line and word times come from `lines.js` (forced alignment, see TEST_REPORT.md).

Only one picture exists, so "motion" comes from a virtual camera rig on a 3-layer split of that photo:
background plate (sky, buildings) → wind-driven flag layer → the two men (BiRefNet cut-out), plus light, dust, confetti and grade.

| Time (s) | Section | Lyric | Camera / action | Graphics |
|---|---|---|---|---|
| 0 – 6.2 | Intro (spoken) | يا مصر… وصلتنا تحيّتكم | Fade from black, tilt down from flags to faces, letterbox 2.35 | Amiri caption, word-lit |
| 6.2 – 13.2 | Oud solo | — | Lateral pan Egyptian flag → Saudi flag | Title lock-up «ما فرّق البحر بيننا» wipes R→L, gold glint, ornament draw-on, flag chips |
| 13.2 – 20.9 | Oud solo | — | Slow push wide → two-shot; letterbox retracts | God rays, light leak |
| 20.9 – 39.4 | Verse 1 | بساحة التخرّج … قدّام البريّة | Hero tilt-up · salute close-up · whip to Saudi face (rack focus) · pull-out | Cairo karaoke captions |
| 39.4 – 57.9 | Chorus 1 | حيّيتونا يا مصر … ما فرّق البحر بيننا | Cuts on half-lines: flag → face → salute → face → orbit pan → eagle crash-zoom → full reveal; kick-synced zoom punches | Aref Ruqaa gold captions, sea-wave line draws under «البحر» |
| 57.9 – 76.3 | Verse 2 (warm) | يوم ضاق الحال … بأطيب نيّة | Dip; slow push on Egyptian face; glide to Saudi flag; Saudi face; orbit | Ship icon on «البواخر», wheat icon on «قمح» |
| 76.3 – 94.4 | Chorus 2 | (chorus) | Variant cut order of chorus 1 | as chorus 1 |
| 94.5 – 106.9 | Instrumental | — | Night grade, blurred drift, then flag pan | Map: Red Sea draws, Cairo/Riyadh pins pop, red→gold→green arc bridges the sea, headline «ما فرّق البحر بيننا» |
| 106.9 – 124.8 | Verse 3 (drums) | ولا رمى الباغي … وليّ عهدنا | Storm grade, handheld shake driven by kick energy, flash and whip cuts | captions |
| 124.8 – 140.9 | Verse 4 (steady) | قالت: ما نبي حرب … وحنا حاضرين | Locked, linear pushes; hero tilt-up | Shield icon on «درعٍ» |
| 140.9 – 159.8 | Bridge (oud) | يوم العبور … قلبٍ واحد | Letterbox returns, soft sepia, 10 s pans | Amiri captions; heart icon on «قلبٍ», halves fill red (Egypt) / green (Saudi) |
| 159.8 – 178.2 | Final chorus | (chorus) | Fastest cutting, strongest grade | Gold/green/red confetti |
| 178.2 – 188.6 | Outro chant | سلامٍ وسلاحٍ … ويحفظ المملكة | Two salutes, glide back to wide | captions |
| 188.6 – 196.82 | Instrumental tail | — | Letterbox, slow pull, fade to black at the end | End card «الله يحفظ مصر / ويحفظ المملكة», ribbon in both flags' colours |

Everything is editable in `index.html`: shot list `SH` (times, framings, easing, transitions, blur, grade), `G` (grades), overlays and caption styles.
