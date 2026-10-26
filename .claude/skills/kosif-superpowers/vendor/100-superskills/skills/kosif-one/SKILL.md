---
name: kosif-one
description: "KOSIF One — the single front door for every KOSIF skill. The user writes ONE request (Arabic or English); this skill plans it, asks the live Jev arbiter for the production route, combines tools in one pipeline when needed (montage-motion, hyperframes, ultra-motion, motion-os, pixel studio, kosif-social, 100 Super Skills, KOSIF Omni) and delivers one gated result. Covers video, montage, reels, Pinterest/TikTok/YouTube downloads, 2D/3D motion, kinetic Arabic text, launch/ad videos, films from songs/poems/verses, reference breakdowns, AI video/image prompts, logos, thumbnails, pixel redraws, audio cleanup/mastering, UI motion, and social media (captions, hashtags, carousels, content calendars, posting times, A/B); anything else goes to KOSIF Omni. Use when the user says kosif one, كوسيف, «مهارة واحدة», «اعمل لي», or any creative/media request where the skill is unclear. Arabic: فيديو، مونتاج، ريل، موشن، انيميشن، تحميل، بنترست، صورة، لوجو، غلاف، صوت، برومبت، سوشيال، كابشن، هاشتاج، كاروسيل، خطة محتوى."
argument-hint: "[طلبك في جملة واحدة — ارفق ملفات أو الصق روابط]"
---

# KOSIF One — طلب واحد، توزيع تلقائي

The user should never have to pick a skill. You take the request, Jev picks the route, you run the steps.
Talk to the user in Egyptian/plain Arabic; keep skill names out of the conversation unless they ask.

## 1. Plan (deterministic, ~0.1 s)

```bash
python ~/.claude/skills/kosif-one/scripts/plan.py --json "<the user's request, verbatim>"
```

Returns `ranking` (keyword evidence), `addons` (captions, voice, music, 9:16/16:9, review, poster, privacy,
grade, prompts, cloud, social_pack), `steps` for the fallback route, and a ready `jev_packet`.
Add to `jev_packet.evidence` anything you know that the words don't say (attached files and their types/durations,
pasted links, earlier turns). Never put secrets or personal data in it.

## 2. Jev decides the route

Call `kosif_jev_decide` with the packet exactly (mode `choice`, `stability: true`). (Load it with ToolSearch
`select:mcp__plugin_kosif-omni_kosif-omni__kosif_jev_decide` if deferred.)

- `stable: true` → use `decision.choice`. Get its steps:
  `python ~/.claude/skills/kosif-one/scripts/plan.py --route <choice>`
- unstable, or Jev unreachable → use `fallback_route` if `fallback_confident`; otherwise ask the user ONE short
  question with 2–3 route choices in Arabic (labels from `ROUTES[*].ar`).
- **Authority:** explicit user words beat Jev (if they name a tool, a style, a duration or a format, keep it). Jev
  ranks; it never authorises downloads, purchases, posting or anything outward-facing.
## 2b. Combine tools when one isn't enough

A request often needs more than one route (Pinterest clips + kinetic Arabic text + a song; a 3D world + moving
words; a launch video + its thumbnail + AI prompts). Combining is normal — use it whenever it makes the result better.

1. Candidates = `combo_packets` from step 1 (routes with keyword hits) **plus any route you yourself judge useful**
   from the request, the attached material or the goal. Rebuild them around Jev's main route:
   `python ~/.claude/skills/kosif-one/scripts/plan.py --json --main <main> --extra <r1,r2> "<request>"`
2. Send every combo packet to `kosif_jev_decide` (mode `noul`, stability on) — **in parallel**, one call each.
3. Decide per candidate:
   - `p_yes ≥ 0.6` and stable → add it.
   - `0.4–0.6` → add it only if you have a concrete reason Jev didn't see (an attached audio file, a link, an earlier
     turn); say that reason in the report. Otherwise drop it.
   - `< 0.4` → drop.
   - The user explicitly asked for it → always add, whatever Jev says.
4. Merge: `python ~/.claude/skills/kosif-one/scripts/plan.py --combine <main> <added...>` → one pipeline in
   production order (gather → design → build → finish → gate), shared steps run once (`from` lists the routes
   that need a step). Max 4 routes; beyond that, split the job into deliveries and tell the user.
5. Build so the parts fit: one aspect ratio, one palette and one font set across parts; layers that belong in
   one frame (3D world + kinetic text, footage + captions) are composited in one render, not stacked as separate films.

Skip 2b only for one-shot answers (a single prompt, a single image critique) where one route clearly suffices.

## 2c. Full power — what every video request is checked against

Before running, walk this list and add whatever makes the result better (say in one line what you added and why):
- **Material**: the user's files · Pinterest (browser pane, user signs in; search per section by MEANING, look at one
  frame per clip, drop text/watermark/landscape/< 360p/off-mood clips) · TikTok/IG/YouTube links (`kmotion fetch`).
- **Understanding**: lyrics/speech on their times (`transcribe`, `--vad auto` for singing) · beats/BPM · sections,
  refrain, peak, strongest excerpt (`songreel analyze`) · a reference's shots/transitions/text (`kmotion analyze`,
  `kmotion mimic study`, `kosif-mimic` for exact transition curves, text animation curves and font match).
- **Picture**: beat cut by meaning (`songreel cut`, `montage`) · per-section grades (night → dawn) · 2D kinetic Arabic
  type (verse, hyperframes) · 3D worlds (three-kit, ultra-motion-montage, shape kit characters) · symbols by meaning,
  counters, payoff light sweep · Voice2Motion · face-aware 9:16 · face privacy.
- **Sound**: the song itself, `audiolab` (voice/music split), original score/ambience, SFX on cuts, −14 LUFS.
- **Finish**: draft → LOOK at frames (P0/P1) → final ≥ 1080 → gate → poster → credits (fetch-credits) →
  per-platform files (`kmotion platforms`) → post pack (`kosif-social`) → AI-video prompts per shot when useful.
- **Ideas**: 2–3 directions before building (hook in the first 2 s, one carried device, a payoff, a deliberate end).
The user may end a request with the "full power" line (Arabic or English, see references/catalog.md) — treat it as
permission to combine routes freely; it never authorises posting, purchases or sign-ins.

## 3. Run the steps

Each step lists where the capability lives (`use[]`, first entry = default):
- `how: "Skill tool"` → invoke that skill (`kosif-montage-motion`, `hyperframes-animation-studio`,
  `ultra-motion-montage`, `motion-os`, `pixel-studio-painter`, `kosif-social`, `kosif-omni:*`) and follow it for that step only.
- `how: "Read playbook file"` → Read the `path` (100 Super Skills playbook) and apply it. If `exists` is false,
  use `kosif_skill_read` / `kosif_skill_auto` with the playbook name instead.
- `how: "MCP tool"` → call that KOSIF Omni tool.
- Optional steps (`optional: true`) run only when the request, an add-on or the material needs them.
- For video/motion work the engine is `kmotion` (`~/.claude/skills/kosif-montage-motion/scripts/kmotion.py`);
  read its `references/operating-manual.md` once per session before the first render — it holds the one-command
  flows (fetch → montage → final), quality settings and traps.
- Add-ons map to: captions → karaoke captions step; voice → `kosif-omni:kosif-voice`; music → user track or
  ambience score; 9:16/16:9 → output size; review → motion-os page; poster → poster frame 0; privacy → face blur;
  grade → colour grade; prompts → aiprompts/video-prompt-director; cloud → `kmotion setup` (claude.ai, no PC);
  social_pack → the `post_pack` step (`kosif-social`: `social.py pack` → write each platform's caption/hashtags/title
  → `social.py check` must pass). Run `post_pack` after the gate whenever the video is meant for a platform, even
  unasked; it never posts.
- The full merged map (which old skill went into which department) is in `references/catalog.md`.

Downloads: only the user's own links or public material they asked for; Pinterest/other sign-ins are done by the
user themselves in the browser pane. Keep `fetch-credits.json`. Never post/publish anywhere without asking.

## 4. Gate and report

- Video: run the montage-motion delivery gate (black/freeze/LUFS −14/peak/exposure) and `kosif_delivery_gate`
  when available. Images/prompts: `kosif_image_prompt_lint` / `kosif_story_lint` where they fit.
- Optional final check for consequential deliveries: `kosif_jev_decide mode=score` with levels
  `["not ready","needs fixes","good","excellent"]` and the measured facts as evidence. Jev's score never replaces
  a failed measurement.
- Report in Arabic, short: the main route and any combined routes (with Jev's p_yes for each, stable/unstable), the steps that ran, the
  output file paths as links, the measured numbers (duration, size, LUFS, gate result), and what was NOT done.

## Routes (Jev's closed set)

| route | بالعربي | main skills |
|---|---|---|
| reel_from_web | ريل من مواد الإنترنت | kmotion fetch → montage |
| edit_my_footage | مونتاج فيديوهاتي/صوري | kmotion montage/timeline, pro-video-editor-ffmpeg |
| talking_reel | ريل فيديو كلام | audiolab, transcribe, kmotion reel, reels-shorts-factory |
| motion_2d | موشن جرافيك 2D | hyperframes (flat), kinetic-typography-arabic, data-in-motion, explainer, character-2d |
| cinematic_3d | مشهد سينمائي 3D | hyperframes three-kit, ultra-motion-montage, cinematic-3d-scene |
| launch_video | فيديو إطلاق/إعلان | kmotion brag + motion-os review + final |
| sound_to_film | فيلم من صوت/أغنية/قصيدة | audio analyze, verse / Voice2Motion, audio-reactive captions |
| song_reel | أغنية → ريل من بنترست بكلمات متحركة | kmotion songreel analyze → Pinterest per section → cut → build (verse over footage) |
| analyze_reference | تحليل فيديو مرجعي | kmotion analyze + omniprompt |
| ai_video_prompts | برومبتات فيديو وسينما | cinema director, video-prompt-director, lighting |
| image_graphics | صور وتصميم جرافيك | image-prompt-forge, thumbnails, logo, mockups, pixel art, critique |
| pixel_redraw | رسم/تعديل بيكسل ببيكسل | pixel-studio-painter |
| audio_only | صوت فقط | audiolab, audio-mastering-analysis, kosif-audio, kosif-voice |
| ui_web_motion | حركة مواقع وتطبيقات | ui-motion-microinteractions, website-design-system |
| social_content | سوشيال ميديا: بوستات وخطة نشر | kosif-social (pack/check, carousel, calendar, besttime, A/B) + arabic-copywriting, youtube-channel-strategy, ideation, competitor research |
| not_media | طلب غير بصري | kosif-omni front door |

To add or change a route: edit `ROUTES` / `STEP_SKILLS` in `scripts/plan.py`, then run
`python ~/.claude/skills/kosif-one/tests/test_plan.py`.
