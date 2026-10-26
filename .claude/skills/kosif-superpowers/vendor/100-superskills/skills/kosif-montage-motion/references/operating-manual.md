# KOSIF operating manual — how we work on every video request

One request from the user ("اعمل لي فيديو…", a clip, a link, a voice note, a Pinterest idea) → you choose the tools
below yourself, in this order of thinking. Speak Arabic with the user; measure before you claim; show, don't describe.

## 0. Read the request
- What is delivered (motion film, montage of footage, reel of a talking clip, lyric/voice film, launch video, a copy of a
  reference, a generation prompt), the duration, the shape (9:16 reels/TikTok, 16:9 YouTube, 1:1), the language and
  tone, the brand (colours, logo, font), the sound (music, voice-over, the user's audio), and the deadline.
- If something essential is missing and cannot be inferred, ask ONE short question; otherwise decide and say what
  you decided.
- On a PC (Claude Code) everything below runs; on claude.ai first run `python scripts/cloud_setup.py --install`
  (no browser there: HTML/3D renders, verse and the review page are not available — say so and use the timeline route).

## 1. Gather material
| source | tool |
|---|---|
| files the user attached | read them; `kmotion probe` / `kmotion analyze` for video |
| **Pinterest** (search, a pin, a board) | the user signs in in the browser pane THEMSELVES (never type a password); open `https://www.pinterest.com/search/videos/?q=…` or `/search/pins/?q=…`, collect pin links with javascript (`a[href*="/pin/"]`), check them with `kmotion fetch --list LINKS`, choose by mood/shape/length, then `kmotion fetch LINKS --out workbench/media/<project>` |
| TikTok, Instagram, Facebook, YouTube, X | `kmotion fetch URL` (yt-dlp; the Cinema C method) |
| **a reel to imitate shot for shot with new footage (المحاكاة)** | `kmotion mimic study REF` → texts/style/layer/fonts → Pinterest pool → `mimic match` → `mimic build` (references/mimic.md) |
| a reference to copy | `kmotion analyze VIDEO` → read every beat's stills → fill brief.json (references/video-breakdown.md) |
| music | the user's track, or an original one: `kmotion score out.wav --bpm … --seconds … --mood …`; ambience: `kmotion ambience` |
| voice | the user's recording; clean it with `kmotion audiolab FILE --mode voice`; Arabic TTS: `kmotion voice` |
| split a clip's sound | `kmotion audiolab FILE --mode voice|music|novoice|nomusic` |
Fetched pins are their creators' work: references, or used in a published film only with rights; `fetch-credits.json` and
`FILM.credits.txt` keep the sources — tell the user which pins went in.
Choose material that agrees: one mood, one light (night with night, warm with warm), the shape of the output (portrait
for 9:16), real resolution (Pinterest video is usually 720p — say so when the output is 1080).

## 2. Choose the route
| the user wants | route |
|---|---|
| footage/photos cut to music | `kmotion montage MEDIA_FOLDER --music track --ratio 9:16 [--grade …] [--voice vo.wav] [--captions caps.json]` — beats, best windows, photos with slow push, landscape media shown whole over a blurred copy, −14 LUFS, credits |
| a precise edit (in/out points, transitions, titles, speed ramps, lower thirds, SFX) | a timeline spec → `kmotion timeline spec.json` (`audio.sfx` with `kit:` cues) |
| a talking clip → reel | `kmotion reel CLIP` or `kmotion direct CLIP` (auto-directed), `silence`, `aspect`, `captions` |
| a film from a voice / song / dua / poem | `kmotion verse AUDIO` (symbols by meaning, counters) or `kmotion audio2motion AUDIO` |
| **a song → a lyric reel cut from Pinterest/collected footage** | `kmotion songreel analyze SONG --name N --lyrics lyrics.txt [--seconds 45] [--start S]` (structure pass with `small`, cached; read the excerpt + the 2 alternatives and choose as a director) → write each section's `queries` (and `grade`, e.g. golden_hour for a dawn section) into songreel.json by the MEANING of its words → Pinterest search per query in the browser pane (the user signs in), collect pin links, `kmotion fetch LINKS --only video --out MEDIA/sNN` → LOOK at one frame per clip and move off-mood, text-heavy, landscape or < 360p clips out of MEDIA → `songreel cut N --media MEDIA` → `songreel build N --title … --model large-v3 --draft` → look at frames → `--render` → gate, poster, credits, post pack |
| motion graphics / 2D / 3D animation | `kmotion new NAME [--3d]` or `kmotion template …`; write the scene (three-kit, motion-kit, shape-kit); `kmotion frames` and LOOK |
| a launch video for a site or app | `kmotion brag init DIR|URL` → plan → build → `kmotion brag deliver` (references/launch-video.md) |
| a prompt for Veo / Sora / Kling / Runway / Omni Flash | `kmotion aiprompts`, or `kmotion analyze` + `kmotion omniprompt` with the user's overrides |

## 3. Review loop (fast)
- `kmotion preview PROJECT` (draft) for every round; look at `kmotion sheet` and full-size stills yourself; fix P0/P1.
- `kmotion readable FILE` — every line readable (≈ 0.3 s a word), the hook in the first 2 s.
- Let the user mark it up: `kmotion review init …` → `http://127.0.0.1:8766/review/NAME/` (start the site with
  `kmotion web`), then `kmotion review feedback NAME` / `apply NAME`.

## 4. Deliver (quality first, ≥ 1080)
- HTML/3D: `kmotion final PROJECT [--blur 4]` (lossless capture, CRF 16, poster drawn as frame 0, gate).
- Timeline/montage: the output is already gated; `kmotion poster FILM --bake` when it opens on a fade.
- `kmotion inspect FILM` must pass (H.264 yuv420p, −14 ±1.5 LUFS, true peak ≤ −1, no black/frozen frames);
  `kmotion platforms FILM --to tiktok,reels,…` for per-platform copies.
- Save to `Desktop/الاداة/outputs/`, send the file, say what you measured, what you could not verify, and the credits.
- For a platform video, finish with the **post pack** (skill `kosif-social`): `social.py pack FILM --platforms …`
  → a caption/hashtags/CTA (YouTube: title + description) written per platform → `social.py check` passes. A
  carousel (`social.py carousel`), a content calendar (`calendar`, `besttime` from the account's export) or an A/B
  plan (`abplan`/`abread`) when asked. Nothing is posted or scheduled on a platform.

## 5. Memory and publishing
- New capability or fix → tests (`python -m unittest discover -s tests`), rebuild the packages
  (`scripts/build_package.py`, the `--claude-ai` one ≤ 200 files), refresh `~/.claude/skills/kosif-montage-motion`.
- Before pushing anything public, scan the package for the user's private brand terms (kept in memory, never written in the skill) and for local paths; push with git/gh from this PC
  (branch → PR → merge) only when the user asked; never commit ultra-motion-montage, settings.json or .env files.
