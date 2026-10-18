# STYLE.md — ما فرّق البحر بيننا

## Observed (measured from the user's files)
- Source photo: 941×1672 px, golden-hour light from the left, Egyptian and Saudi flags on gold poles, two men saluting.
- Song: 196.82 s MP3, title tag «ما فرّق البحر بيننا», artist tag melkosif57, made with Suno (per its metadata); lyrics with section markers are embedded in the file and were used verbatim for captions.
- Reference video: none supplied. The parallax-2d style reference page was not opened; this film is an original treatment.

## Assumed / chosen
- Format 9:16, 1080×1920, 30 fps (KOSIF default; the photo is already ~9:16).
- Palette: photo's own colours plus gold `#ffd36b` / `#f2c14e`, Egypt red `#ce1126`, Saudi green `#006c35`.
- Type (all OFL, files in `assets/fonts/`): Aref Ruqaa Bold (title, chorus, end card), Cairo 800 (verses), Amiri Bold (intro, bridge), Reem Kufi (small labels). Whole-word animation only, R→L wipes, no letter-spacing.
- Camera: 2.5D parallax (background 0.88–0.9× of foreground travel), constant drift and 0.35 % "breathing", rack focus by per-layer blur, whip pans with 9-tap motion blur, kick-synced 2.2 % zoom punches in choruses, energy-driven handheld in verse 3.
- Life added to the still: wind travelling through both flags (strip displacement + fold shading), dust motes, bokeh, light leak and god rays, film grain, vignette, per-section grade.
- Image prep: 2× EDSR super-resolution (OpenCV dnn_superres) for sharper close-ups; BiRefNet-portrait cut-out of the two men; inpainted background plate; flags extended behind the heads so the parallax never shows a hole.
