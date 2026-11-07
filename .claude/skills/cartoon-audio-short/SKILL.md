---
name: cartoon-audio-short
description: Make a vertical animated cartoon short in Arabic or English. Offers 10 ideas, writes the script, then turns the user's voiceover into a finished MP4 with quiet music and SFX under the voice. Use for any cartoon short or animated story video request, including Arabic requests such as فيديو كرتون، قصة متحركة، أنميشن، شورتس.
---

# Cartoon short: idea → script → voiceover → finished MP4

The look: flat 2D bean-head cartoon characters (canvas-drawn "cards" with plum outlines) in a colourful 3D world with black ink outlines, painted textures, depth-of-field and gliding cameras. The output is 1080x1920, 30 fps, exactly as long as the voiceover. The user's voice is unchanged. The music bed and SFX are synthesized: music **16 dB under the voice**, SFX at **50 % of the voice level** or less. Proven on "The Soldier Who Never Left" (19.7 s, 8 shots).

## If this skill arrived as files in the chat
The user may send `SKILL.md` and `cartoon-short-kit.zip` and say something like "read this skill, install it and use it" (اقرأ هذه المهارة، وثبّتها، واستخدمها). Then:
1. Read this whole file and follow it. Don't explain what a skill is and don't ask setup questions.
2. Unzip the kit to a writable folder (see 4.0). Confirm `engine/main.js` and `vendor/three.module.js` are there.
3. If this environment has a personal skills folder (for example `~/.claude/skills/`), copy `SKILL.md` and the kit into `cartoon-audio-short/` there. If it has none, don't say it's permanently installed: say in one line that it's ready for this chat and the two files need sending again in a new chat.
4. Reply in one short line and go straight to Stage 1.

## Language: Arabic or English
- **Chat:** answer in the language of the user's messages from the first reply. If they write Arabic or ask for Arabic, every message is Arabic: questions, option labels and descriptions, the task list, ideas, progress notes, errors and the delivery note. Use simple everyday words, and match their dialect if they write in one. English stays only for file names and commands, on their own line so right-to-left text doesn't scramble them.
- **Script:** the script's language follows the chat unless they ask otherwise. "أريد أفكار بالعربي" typed at any question means Stage 2, in Arabic.
- **Arabic variety:** write simple standard Arabic unless they write or ask for a dialect (Iraqi, Egyptian, Gulf, Levantine and so on). Don't stop to ask. End the script reply with one line: "تريده بلهجة ثانية؟ اكتب اللهجة وسأعيد كتابته." Never mix standard and dialect in one script unless they ask.
- **Fixed questions in Arabic.** Use this wording:
  - "من أين نبدأ؟"
    - "الصوت جاهز": ارفع الملف الصوتي، ومعه النص إن وُجد، وسأصنع الفيديو.
    - "عندي نص": سأحسّنه وأعطيك نصائح للتسجيل، ثم أصنع الفيديو بعد رفع الصوت.
    - "أحتاج إلى أفكار ونص": سأقترح عشر أفكار أصلية، ثم أكتب النص للفكرة التي تختارها.
  - "كم مدة الفيديو؟"
    - "من 20 إلى 30 ثانية (مُوصى به)": نحو 40 إلى 60 كلمة.
    - "من 30 إلى 45 ثانية": نحو 60 إلى 90 كلمة.
    - "من 45 إلى 60 ثانية": نحو 90 إلى 120 كلمة.

## Rules
- Stories, characters and shots are always original. Never recreate another creator's video shot for shot. Offer an original take on the same idea instead.
- No real, named living people as characters, and no brand mascots or logos.
- No captions unless the user asks. Diegetic text (a carved message, a sign) is fine, and it must read correctly (not mirrored). Signs, labels and headlines use the script's language: an Arabic video gets "بِيعَ", not "SOLD". Draw them as in 4.3.
- Never edit or re-time the voice. The picture is timed to it, and every visual reaction lands 0-3 frames before its word.
- **Audio levels:** the music bed sits 16 dB under the voice (gated RMS), so narration stays clear. SFX sit at 50 % or slightly less, with peaks capped so no hit pokes out over the narration. Always mix with `mix.py`, never by hand. Use no ducking or compression that would change this ratio; only one linear gain plus a peak limiter goes on the whole mix.
- Keep the user informed with a task list. Send a stills contact sheet before the long render.

## Stage 1: Intake (always first)
If an audio file is already attached, skip to Stage 4. If a script was also given, use it for the timing.
Otherwise ask one AskUserQuestion (or plain text if that tool is missing): **"Where are you starting from?"**
- **Voiceover ready**: ask them to upload it, plus the script text if they have it (the script makes the timing exact). Go to Stage 4 when it arrives.
- **I have a script, need the voiceover**: tighten the script per Stage 3 if needed, give it back with recording tips, ask for the upload, then go to Stage 4.
- **Need video ideas and a script**: go to Stage 2.
Also ask the target length if they haven't said. The default is 20-30 s; 45-60 s is allowed. In an Arabic chat, use the wording under Language.

## Stage 2: 10 video ideas
Give exactly 10 ideas in one reply, numbered, and ask the user to reply with a number (or "more"). Each idea gets:
- **Title** (5-8 words, curiosity-driven, e.g. "The Soldier Who Never Left").
- **Hook line**: the first spoken sentence, a paradox stated as fact ("A man sold the Eiffel Tower. Twice.").
- **The twist** in one line (the ironic payoff that ends the video).
- **Why it animates well**: the 2-3 big visual moments (a collapse, a reveal, a chase).
- **True or legend**: say plainly whether it is documented history, a disputed account or folklore.

What makes an idea "perfect" for this format:
- One surprising story with a physical cause and effect you can show.
- A clear everyman character, stakes that escalate, and a twist in the last line.
- A setting that can be built from simple 3D shapes plus cartoon cards (towns, bridges, ships, castles, deserts, labs, palaces).
- Mix the 10 across eras and themes: ancient, medieval, 1800s, modern, science, animals, inventions, disasters, weird laws, lucky accidents.
- For anything presented as true, verify the key facts with a web search before offering it. Don't present a viral legend as fact. If the user wants it anyway, frame it as "legend says".
- No real living people as the butt of a joke, nothing graphic and nothing political.

For Arabic ideas:
- Write the title, hook, twist and notes in Arabic. Write the hook as a natural Arabic sentence, not a translation. Give foreign names their usual Arabic spelling.
- Mix stories from Arab and Islamic history and science with world stories, so the list feels made for this audience.
- Search in Arabic as well as English. Popular Arabic stories spread without sources too, so label them with **True or legend** in the same way.
- Never show prophets, their companions or other sacred figures as characters. Don't joke about religion, sects, tribes or nationalities.

## Stage 3: Script (after they pick)
Write the narration only (no stage directions in the spoken text). English is sized at about 3.7 words/s: 20 s ≈ 75 words, 30 s ≈ 110, 60 s ≈ 220. **Arabic is slower, about 2 words/s: 20 s ≈ 40 words, 30 s ≈ 60, 60 s ≈ 120.** Arabic words carry more syllables, and real Arabic voices measured 1.6-2.1 words/s. Formula:
1. **Hook** (sentence 1, no setup): the absurd fact.
2. **Setting** in 1-2 lines: when, where, who, a concrete detail.
3. **Escalation**, 2-4 beats, each bigger. Others doubt or mock. Use one exaggeration joke.
4. **Mystery or pivot**: "But when..." / "You see," introduces the real mechanism, often with an everyday analogy.
5. **Twist / payoff**: short, ironic, and the last words of the video.
Use plain spoken English, contractions, sentences around 8-15 words, and numbers written as words. Never describe what the viewer already sees.

For an Arabic script:
- Keep sentences to about 6-12 words, and use the same five-part formula. Pivots such as "لكن عندما…" and "والسبب؟" work well.
- Write numbers and years as words (ألف وتسعمئة وأربعة وتسعون), and spell foreign words and brand names in Arabic letters, so the voice reads them correctly.
- Punctuate for the voice: "،" and "." for breaths, "…" for a pause before a reveal, and "؟" for questions. The timing also uses this punctuation.
- Give one copyable voice block ready to paste into the voice generator:
  - **Tashkeel** on every word, which helps most on names and words with more than one reading. Leave off case endings a narrator wouldn't say, and write dialect as it is spoken. If they ask for no tashkeel, or it sounds wrong, remove it.
  - **Audio tags** for Eleven v3 in English, such as [excited], [curious], [serious], [whispers], [warmly]. Use one or two per sentence group at most, only where the words earn them.
  - **Iraqi "g":** write گ and چ where the spoken sound needs them (تِگْدَر, لْگِيت), since ك reads as "k".
  - **Parts:** for a script over about 700 characters, split it into numbered parts at sentence ends.
- Word count and length use the Arabic rate above, with tags and tashkeel ignored.

Then reply with:
- The script in a copyable block, with the word count and estimated length.
- A one-paragraph visual plan (the shots you'll animate).
- Recording tips: one steady, warm narrator voice; ElevenLabs works well (a deep narrator voice, speed about 1.05-1.1, stability about 45-55 %). Mp3 or wav is fine. Leave natural pauses at sentence ends. Export without music.
- Arabic recording tips: use Eleven v3, because older models read the [tags] aloud. Start with Stability on Natural and speed about 0.95, and try the first sentences before generating everything. With another generator, delete the tags first. Their own voice works too, without the tags or tashkeel.
- The ask: **"Upload the voiceover when it's ready and I'll make the full video."**
Keep the final script text. It drives the timing in Stage 4, so no speech recognition is needed. If they recorded a changed version, ask for the final text.

## Stage 4: Build the video (after the voiceover is uploaded)
Do everything from here without stopping. Ask only if the timing cannot be resolved.

### 4.0 Get the kit
The code kit contains the engine, tools, worked example, vendored three.js r160, the `toon.ts` Pen library from github.com/mromidev/claude-animated-shorts (both MIT) and the Lalezar Arabic font (SIL OFL). Find it in this order, and treat it as read-only:
1. A `kit/` folder next to this `SKILL.md`, found with `find / -name SKILL.md -path "*cartoon-audio-short*" 2>/dev/null`.
2. An already unzipped `cartoon-short-kit` folder.
3. `cartoon-short-kit.zip` among the files sent in this chat: `find / -name "cartoon-short-kit*.zip" 2>/dev/null`, then unzip it to `~/cartoon-short-kit-src/`. The kit is the folder inside that holds `engine/`.

Then run `bash <kit>/tools/setup.sh ~/shorts/<slug>`. It copies the engine and tools into the project, installs the vendored three.js, strips the types from `toon.ts` with Node 22 `module.stripTypeScriptTypes`, and links Playwright. No network is needed. If the vendored files are missing, it falls back to npm or a git clone.
- Requirements: Node 22.6+, Python 3 with numpy + Pillow, ffmpeg, and Playwright with Chromium (`npm i -g playwright && npx playwright install chromium` if missing).
- If package registries are blocked, git over GitHub usually works. Never disable TLS or route around the proxy.
- Chromium: use the pre-installed Playwright browser with `--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`. That gives CPU WebGL at about 3-10 s per frame.

### 4.1 Timing
Run `python3 timing.py voice.mp3 script.txt --out work`. Add `--lang ar` for Arabic if there's no script. The script can be the exact voice block: it strips [tags] and tashkeel, and it splits phrases at Arabic punctuation too.
- With whisper or faster-whisper installed, it uses word timestamps. For Arabic it uses a multilingual model, and it keeps the script's own words, so a misheard dialect word can't change the text.
- Otherwise it aligns script phrases (split at punctuation) to silence-detected speech segments, with a DP that matches syllables to duration and penalises sentence ends inside a segment and long gaps inside a phrase.
- With no ASR and no script, ask for the script. Claude cannot hear audio.
- Check `work/phrases.json`: pauses should fall at sentence ends. Total frames = round(duration × 30).

### 4.2 Shot plan (`work/PLAN.md` before code)
Make one row per shot: frames, words, setting, light, camera move, characters/poses/expressions, effects and SFX cue.
- Frame 0 is already the hook image.
- Usually one shot per phrase. Merge tiny phrases into the next shot.
- Illustrate every sentence literally. Props carry the jokes.
- Vary shot sizes: hook MCU → wide reveal → two-shot → insert close-up on the key object → reaction close-up → environment move for the payoff.
- Use light for beats: day for normal, golden for decline or drama, night-blue for explanation. A time jump gets a 6-frame white flash.
- The twist line gets a sting (music stops, low hit, push-in with roll). The last shot's physical payoff lands on the final word.

### 4.3 World (`web/main.js`)
Keep the engine sections: toon materials, ink contract, `add`/`tbox`, sky, lights, cards, render targets/post, `applyLight`, `drawActors`, `swapForNd`, `renderFrame`. Replace the example world between `// ---------- world ----------` and `// ---------- cards ----------`, plus the story parts of `worldState()`.
- Build from primitives with painted canvas textures (`paint.js`: planks, beams, rotten wood, stone, moss/ivy, grass, dirt, plaster, roof tiles, marble, banners, carved text). Write new painters in the same flat-with-dark-seams style.
- Use `tbox` for constant texel density, a 2-step toon gradient, and fog = horizon colour.
- Background: hills (half-buried spheres), mountains (cones + snow caps), cypress/pine trees, distant houses, painted cloud billboards.
- Set pieces (collapses, falls, doors) are pivoted groups driven by 0..1 progress from `worldAt(f)`, with eased and staggered parts.
- Curved diegetic text uses planar UVs. Check it isn't mirrored.
- **Arabic text on anything:** use `P.signCanvas(text, opts)` with `P.tex()` for signs and tags, `P.drawText()` on your own canvas, or `P.carvedText()` for engraving. They load the bundled font, set right-to-left and draw whole strings. Never draw Arabic letter by letter, add letter spacing, reverse the string or use a font that has no Arabic letters. Keep it short: one to four words with no tashkeel reads best on a sign.

### 4.4 Cast (`web/roman.js` → `web/toon.js`)
- `romanFront(p, outfitKey, opts)` draws on a 600x1000 design canvas with soles at y=975. The card is 2.25 m tall, so 1 unit = 0.00225 m.
- Add outfits to `OUTFITS` (tunic/cape/armor/helmet/hair/cap/beard/apron/dress/toga) and new headgear and props in the same style.
- Arm poses: hang, spear, point, up, wave, hip, belly, temple (+swirl), lift, reach (+lift), cheek, shield, cross, thumb.
- Expressions: the toon.ts FACE set plus snore, stubborn, squint. Extend FACE for more.
- Rebuild after edits with `cat web/toonbase.js web/roman.js > web/toon.js`. Render a character test sheet before using new designs.
- Billboards turn on yaw only, get a contact blob and an alpha-tested shadow, and are never inked by the world pass.
- Build card keys from `q()`-rounded values (so the canvas redraws only on visible change).
- A detached part (e.g. a lifted helmet) is its own card, aligned with `headCenter(seed)`: y = DECK + (partY − hc) × 0.00225.

### 4.5 Motion: smooth and alive (`web/motion.js`)
- **Cameras**: `camFromKeys(keys, f, {kicks})`. Use smootherstep glides (18-45 f), `easeOut` for reveals and whips, and `path` via-points (Catmull-Rom) for curved moves. Every hold creeps and nothing is static for 4+ frames. Use 3-5° rolls on drama and 7-frame flip-shakes on impacts.
- **Continuity**: prefer continuous moves (pull back from a close-up into the wide, rack focus, crane through the deck, push into an object). Hard cut only on place or time jumps, with a flash.
- **Characters never freeze**: apply `idle(f, seed)` to every card, `blinkAt` blinks, and head bobs on stressed words.
- **Actions**: anticipation → `back` overshoot → `spring` settle. A stamp is a 2-frame dip + dust puff + kick. Laughs are an alternating tilt + bob.
- **Secondary motion**: banner cloth waves, leaves/dust/drips/Zzz effect cards, flowing water. Something always moves.
- **Walks**: `walk()` gives distance + step phase. Feet planted, bob 3-7 %.
- **Lens**: DOF on close-ups and mediums (cInf 8-14 px), focus on the eyes. Wides are sharp. Racks take ~14 f.

### 4.6 Look check (before the full render)
Render stills at each shot's middle plus the transitions and key actions: `node render.mjs stills/a "5,40,..."` then `python3 sheet.py stills/a stills/sheet_a.jpg`. Look at the sheet and fix these traps:
- **Narrow vertical frame**: horizontal half-width = d·tan(hfov/2), with hfov = 2·atan(tan(vfov/2)·0.5625). At 4 m and fov 40 that is ±0.8 m, so stage characters in depth.
- Railings or posts across faces (camera inside the rail or ~2.5 m up). The camera path through houses, roofs or bushes. Foreground props under ~2 m away. The hero hidden behind a pillar.
- Mirrored text. A detached-part card offset the wrong way.
- Arabic text with separated letters, reversed word order or empty boxes. Zoom in on every sign before the full render.
- Extrude material groups: 0 = caps, 1 = sides+top.
- Missing ink: debug the edge-only output. Ink radius ~2.5 px at 1080. The sky counts as far depth, not a card.
Send the sheet to the user with a one-line shot summary, then start the full render.

### 4.7 Sound (`audio.py` → stems → `mix.py`)
Rewrite the cue table for the story; the synths stay. `audio.py` writes only stems (`music.wav`, `sfx.wav`).
- Music: a short march-like loop (kick/snare, plucked bass, brass pad). It stops at the twist line, then a low drone continues.
- SFX on events (in frames/30): whooshes on big moves, thunk on stamps, rumble+crash on collapses, scrape on metal, ting on reveals, sting on the twist, creaks, snap, splash, snore, leaves, water ambience.
- Mix with `python3 mix.py voice.mp3 music.wav sfx.wav`. It sets music to 16 dB under the voice's gated RMS and SFX to 50 % (−6 dB) with peaks capped at 0.7× the voice peak. It prints the measured levels: confirm music shows −16.0 dB vs voice and SFX is at or below −6 dB.
- Lock picture timing before making sound. Any timing change means re-running audio.py and mix.py.

### 4.8 Render + finish
- Run `node render.mjs frames "0-<N-1>"` with Bash `run_in_background`, watched by a Monitor loop that reports progress and catches errors or process exit. `RESUME=1` continues after an interruption. Don't run heavy Python at the same time on small machines.
- Run `bash finish.sh "Title"`. It applies one linear gain to about −14 LUFS plus a −1 dBFS peak limiter, encodes H.264 CRF 17 + AAC, runs freeze/black and loudness QA, and writes `out/qa_sheet.jpg`. Look at the sheet. Frozen spans ≥0.4 s or black frames need a fix.
- Deliver the MP4 with SendUserFile and a few lines on what each shot shows, in the chat's language. Offer captions, tweaks, or the next idea from the list. If they want Arabic captions, draw whole phrases right to left with the bundled font, inside the safe area.

## Inside KOSIF (Black Dragon)
In this repository the kit sits in `kit/` next to this file, so step 4.0 finds it first. Run `setup.sh` from there; never edit the kit in place.
- **Delivery gate:** after `finish.sh`, check the MP4 with the repo's gate before sending it: `python3 tools/verify_video.py out/<Title>.mp4 --aspect 9:16 --fps 30 --duration <seconds> --audio voice.mp3 --lufs -14`. Every line must be PASS.
- **Black Dragon adapter:** `skill:cartoon-audio-short` in `.claude/skills/kosif-superpowers/data/black_dragon_adapters.json` runs `timing.py` (also on a voice-studio `words.json`), `mix.py` and `sheet.py` on known answers and checks them by measurement. Run it alone with `python3 .claude/skills/kosif-superpowers/scripts/_black_dragon_skill.py cartoon-short out/cartoon.txt --task="<the request>"`, or with every adapter through `black_dragon.py run ... --execute-adapters`.
- **Voice:** a voiceover made with `kosif-voice-studio` (with its `words.json`) goes straight to `timing.py voice.mp3 script.txt --asr-words words.json`, so the timing uses its word times and the script keeps its own words.
- **Music:** if the user wants a real song instead of the synthesized bed, make it with Suno after a yes (appendix A46), then still mix with `mix.py` so the 16 dB rule holds.
- **Upstream depth:** `upstream/claude-animated-shorts/` holds the full original skill (MIT) this kit grew from. Reach for it when a short needs more: `templates/audio/sfx_gen.py` has 40+ SFX synths (creaks, splashes, crowds, birds, hammer) and `dsp.py` a BS.1770 meter and true-peak check; `templates/scripts/short_qa.py out/<Title>.mp4 out/qa` checks every frame (black, white, frozen, pops) after `finish.sh`; `references/reports/*.md` measure motion, depth, textures, characters, lighting, ink and grade. Its Remotion bridge template is reference code; the kit renders without Remotion. See `upstream/README.md`.
- Licenses of the bundled files are listed in `THIRD_PARTY_NOTICES.md`.

## Engine gotchas (kept in the kit; keep them if rebuilding)
- `#include <fog_vertex>` / `<fog_fragment>` go on their own lines.
- The final pass writes `linearToOutputTexel(...)` (render targets are linear HalfFloat).
- The normal+depth pass swaps materials per mesh: world → normal/depth, cards → alpha-tested mask (rgb 0, a = depth), blobs/clouds/sky hidden, water → flat normal. Fog and shadows are off during it.
- Ink goes on the near side of depth jumps only. Creases come from the normal dot. Card neighbours are skipped. Ink fades at ~140-520 m.
- DOF: 48 taps with a per-sample CoC test (no foreground bleed).
- The sun comes from az/el per light preset. The shadow camera is centred on each shot's action.

## Architecture (reference for editing the kit)
- `web/index.html` loads `main.js` (ES module) over a local HTTP server.
- `main.js`: renderer, toon materials, world, cards (1200x2000 CanvasTexture planes, origin at soles), passes colour (RT samples 4) → normal/depth → ink+grade (saturation, gain/lift, vignette, flash) → DOF to screen. It exposes `window.renderFrame(f)` and `window.ready`.
- `story.js` exports SHOTS, `shotAt`, `camAt`, `dofAt`, LIGHTS/`lightFor`, `worldAt`, `actorsAt(f, T)`, `fxAt(f, T)`. All are pure functions of the frame.
- `render.mjs`: Playwright → `renderFrame(f)` → `toDataURL('image/jpeg', .95)` → `frames/f0000.jpg`.
- `mix.py`: gated-RMS level lock (music 16 dB under the voice, SFX at 50 %). `finish.sh`: linear loudness gain, limiter, encode, QA.
- Characters: the Pen API from mromidev/claude-animated-shorts `templates/bridge/toon.ts`, extended in the same module scope by the cast file.