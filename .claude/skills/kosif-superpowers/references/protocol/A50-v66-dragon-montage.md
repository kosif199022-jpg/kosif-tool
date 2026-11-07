# A50 — USIP v6.6: بروتوكول مونتاج التنين الأسود (Dragon Montage)

> **متى تقرأه / when to read:** «التنين الأسود، مونتاج»، أو فيديوهات معاها طلب مونتاج أو ريل، أو «اعمل زي الفيديو ده» · [العودة إلى النواة / back to the core](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

**Trigger:** «التنين الأسود، مونتاج» / «مونتاج بالتنين» / «اعمل ريل من الفيديو ده» / «اعمل زي الفيديو ده», with one or more videos.

**Runs:** `black_dragon.py montage edit "<task>" --clip … [--music …] [--reference …]`
(entry point `.claude/skills/kosif-dragon-montage/scripts/dragon_montage.py`, skill `kosif-dragon-montage`).

## Why it exists
The A48/A49 dragon assigns every catalog entry to a task, but ~90% are text cards and no part of it
decides where to cut. A50 changes the rule for video work: **depth over breadth**. Each of eight
stations uses the few tools that fit, and every station writes a file whose decisions can be read.

## Stations
1. العين الأولى → analysis.json (shots + quality, words, silences, beats, faces, loudness, colour)
2. يفهم المطلوب → brief.json
3. يفكر بإبداع → concepts.json: three concepts that differ in arc or rhythm, a scored decision with
   sensitivity, pre-mortem, council prompt pack (Claude runs the council when the decision is fragile)
4. يختار الذوق → look.json from the taste index (897 styles), executable grades/transitions/camera/captions, matrices for `--invent`
5. يكتب المونتاج → edl.json, one canonical EDL, every cut with a reason
6. ينفّذ → final.mp4 + captions + editable project (FCPXML, Premiere XML, OTIO, EDL, CapCut pack)
7. يتفرج وينقد → review.json: automated checks + frames for Claude's eyes + concrete fixes
8. يصلّح ويسلّم → apply fixes, re-render, up to three rounds, keep the best round, report.md

## Report line (replaces the A49 line for montage work)
«التنين-مونتاج: consulted · ran_on_your_video · missing · rounds · verdict»
Never present consulted cards as executed.

## Open-licence footage («دوّر في Pexels»)
When the owner asks for stock, `edit --stock "<english query>"` searches the free sites (Pexels, Pixabay,
Mixkit, Coverr, Wikimedia Commons, Internet Archive, NASA, Library of Congress) through `free_footage.py`,
downloads the best-licensed clips with a sidecar each and `stock/ATTRIBUTION.md`, and adds them to the edit;
the report lists every credit line. Paid stock sites are never searched.

## Consent
Generation (Kling/Higgsfield/Suno) is proposal-only: `generate.json` + `GENERATE_AR.md`. The owner's
yes in chat is required before any paid call. Nothing installs, uploads or publishes by itself.

## Tools
`dm_doctor.py doctor` and `install-plan --os linux|macos|windows|ashell` state exactly what must be
installed. Manifest: `kosif-dragon-montage/data/required_tools.json`; Arabic guide: `references/TOOLS_AR.md`.
