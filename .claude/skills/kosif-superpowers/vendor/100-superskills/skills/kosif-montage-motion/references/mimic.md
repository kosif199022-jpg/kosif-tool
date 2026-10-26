# المحاكاة (Mimic) — ريل مرجعي → نفس الفيلم بلقطات جديدة

The user gives a reel someone made (typical: Pinterest clips cut together with Arabic text on top — Friday duas, Rabi'
al-Akhir, morning adhkar — over a nasheed or recitation) and wants **the same film**: same cut times to the frame, same
transitions, same words in the same place and lettering, same sound — with **new footage of the same mood** from
Pinterest. Engine: `kmotion mimic` (scripts/mimic.py). Never skip a step's check.

## 1. Study (measured, ~30 s)
```
python scripts/kmotion.py mimic study REF.mp4 --out PROJECT/study
```
Read, in this order: `shots.jpg` (every shot + transition), `strip.jpg` (a frame every 0.5 s — where the words change),
`text/shot_XX.png` (the lettering, large), `search/shot_XX.jpg` (each shot with the words painted out).
`mimic.json` holds the measurements: `boundaries` (cut / dissolve / fadeblack / fadewhite / slide*, start + dur to the
frame), `shots[].clip` (the length each new clip must have — it stays on screen through both transitions), `look`,
`text_zone`, `text_events` (hints), `fades`, `flashes`, `suspects` (gradual changes that are not edits — camera moves,
exposure fades inside a shot: look at the frames; promote one into `boundaries` only if it really is an edit), `audio`.
Measured on a known reel: every cut, dissolve and dip to black found at the exact frame and length.

## 2. Fill what only eyes can read — in `mimic.json`
- `texts[]`: every on-screen text exactly as written (keep the diacritics, line breaks with `\n`, ﷺ etc.), with
  `start`/`end` (use `text_events` + strip.jpg; a text often spans a cut), `x`/`y` = CENTRE of the block as fractions
  of the frame (from `text_zone.bbox`), `size` as a fraction of frame height (line height ≈ bbox height / lines / 1.3),
  per-text overrides (`color`, `anim`) only when they differ from `text_style`.
- `text_style`: `color` (from `text_zone.color`), `stroke` px + `stroke_color`, `shadow` true/false, `box` (#rrggbbaa)
  if the words sit on a band, `anim` (`fade` · `rise` · `drop` · `slide-left` · `slide-right` · `none`) + `fade` length.
- Keep the harakat exactly as written: texts with harakat are drawn by the browser engine (Edge/HarfBuzz) so every
  fatha/shadda/tanween sits on its letter — Pillow here drops or misplaces them. `text_style.engine: "browser"` forces it.
- `text_style.fit_width: 0.96` = one common size for all texts, the size at which the longest line fits 96 % of the
  width on ONE line (how these reels are made: same letter height, long lines edge to edge). `stroke` ≈ 7 px at 1080.
- The fixed design (title, date, badges, salawat line, icons): `layer/overlay.png` is lifted automatically; LOOK at
  `layer/overlay_preview.jpg`. Erase the creator's handle/logo/signature with `mimic layer DIR --erase x0,y0,x1,y1`
  (never copy them); a moving badge (a bobbing medallion) with `--snap x0,y0,x1,y1@SHOT:hmin,hmax,smin,vmin` (OpenCV
  HSV, e.g. gold 18,40,80,140) taken from one shot. `layer.fade_in` when the design fades in at the start.
- Then `mimic fonts PROJECT/study` → `fonts.jpg` ranks every Arabic font on the PC against the crop; LOOK at the sheet
  and set `text_style.font` to the path that really looks the same (Naskh vs Thuluth vs Kufi vs Diwani matters more
  than the score).
- `shots[].query`: 2–4 Pinterest searches per shot from `search/shot_XX.jpg` — subject + light + mood + camera, English
  first (Pinterest's video pool is mostly English-tagged), Arabic second: "aesthetic mosque sunset clouds video",
  "rain on window night cozy", "green field wind slow motion", "مسجد غروب".

## 3. Footage from Pinterest
The user signs in to Pinterest THEMSELVES in the browser pane (never type a password; leave "confirm email" dialogs to
them). Per shot (or per group of shots with one mood):
1. `https://www.pinterest.com/search/videos/?q=<query>` → collect pin links with javascript (`a[href*="/pin/"]`).
2. Visual search when words are not enough: open the closest pin → its "More like this" related pins share the look;
   or, with Claude in Chrome (file upload), Pinterest Lens on `search/shot_XX.jpg`.
3. `kmotion fetch --list LINKS` → keep videos ≥ the shot's `clip` length (or ≥ 0.67× — `match` slows them down),
   portrait first, no burned-in text or watermarks (they clash with the new text).
4. `kmotion fetch LINKS --only video --out PROJECT/pool` — 2–3 candidates per shot; `fetch-credits.json` keeps the
   source of every clip.

## 4. Match → build → gate
```
python scripts/kmotion.py mimic match PROJECT/study --pool PROJECT/pool [--set 4=PROJECT/pool/x.edit.mp4@1.5]
python scripts/kmotion.py mimic build PROJECT/study --out PROJECT/FINAL.mp4
```
`match` picks, per shot, the pool clip + in-point closest in colour, contrast, saturation and motion (one clip per shot
while the pool allows; Hungarian assignment) and a colour transfer towards the reference look (`--strength` 0–1,
default 0.7). The math matches colour and motion, NOT meaning: LOOK at `match.jpg` (reference | choice) and at
`pool.jpg` (every pool clip), and replace off-mood picks (a Christmas sign in a Jumuah reel, a desert under a rose) with
`--set N=file@` (no time = the best clean window of that clip) or `--set N=file@seconds`. Windows holding the source's
own cut, dissolve or dip are refused (found at the clip's full frame rate — look-alike cuts too); `unclean_shots`
in match.json lists shots the pool could not serve cleanly.
`build` writes `mimic.timeline.json` (same size ratio at ≥ 1080, same fps, clip lengths, xfade transitions, texts,
the reference sound at its own loudness, fades) → the film → `compare`:
`compare.json` checks duration (±2 frames), every boundary found at ±2 frames with the same type, no extra boundaries,
the sound identical (correlation ≥ 0.95, lag ≤ 40 ms); `compare.jpg` puts reference and new film side by side at every
shot and every text. Not passing = not delivered: fix and rebuild.

## 5. Deliver
Report in Arabic: shots/transitions reproduced (numbers from compare.json), the texts, the font chosen, the Pinterest
sources (from fetch-credits.json), and what differs. Rights: the sound and the original idea belong to their owners,
and the Pinterest clips to their creators — say so; the user decides where to publish. Add the post pack
(kosif-social) when the user wants to post.

## Traps
- A clip cut short (app closed during the download) probes fine but cannot be decoded: `fetch` now decode-checks every
  edit copy and refetches a source whose file is gone; for an older pool run
  `ffmpeg -v error -xerror -i CLIP -f null -` on each and move broken ones aside.
- The gate confirms a boundary in the frames, or — when two new clips look too alike for the detector — from the
  timeline's own report at the same time and type (`seen: plan`); missing in both = fail.
- A text fading in looks like a dissolve: study leaves the text zone out of boundary detection (`ignore_mask`).
- A source clip that brightens from dark is NOT a dip to black between shots: exposure fades with the same structure
  go to `suspects`.
- Night footage is dark everywhere: a dip needs a bright side (≥ 30) and near-black frames (< 16).
- Pinterest video is usually 720p: the output is 1080 wide by upscaling — say so.
- timeline: a hard cut next to an xfade needed `settb=1/90000` after concat (fixed in v6.3).
