---
name: kosif-mimic
description: مهارة المحاكاة (التقليد) — Remake a reference video with NEW footage while copying everything else exactly - original audio, same text with the same fonts, positions, colors and shadows, same text animations synced to the audio (fade, word-by-word, slide, pop, blur), same transitions with the same timing, same color mood. Finds similar clips on Pinterest (or builds an intermediary links page when Pinterest is unreachable). Use whenever the user uploads a video and wants one like it, a copy, remake, template, محاكاة، تقليد، نفس الفيديو بلقطات تانية، فيديو شبهه، أدعية، بنترست.
---

# مهارة المحاكاة — KOSIF Mimic

Scripts live in `scripts/` (Python 3.10+, numpy, Pillow; OpenCV/SciPy optional; ffmpeg with libass).

## Workflow
1. **Analyse** the uploaded reference:
   `python scripts/mm_analyze.py`-style entry: `python -c "import sys;sys.path.insert(0,'scripts');import mm_analyze;mm_analyze.analyze('REF.mp4','work')"`
   → `work/spec.json`, `work/analysis.md`, sheets in `work/sheets/` (shots, transitions, texts), original audio copied untouched to `work/audio/`.
2. **Look at the sheets** (Read the PNGs). Fill `spec.texts[].lines[].text` with the EXACT text (OCR draft is in `ocr`); never invent text. Describe each shot in `shots[].describe` and write 3–5 Pinterest queries (English + Arabic) in `shots[].queries`.
3. **Fonts**: `mm_fonts.match('work')` ranks ~80 free Arabic faces (core set in `assets/fonts`; `python scripts/mm_fonts_lib.py fetch` adds the rest via GitHub) + system fonts; check `sheets/fonts_evNN.png`. If the original is a commercial font, say so and use the closest; user can drop the real .ttf into `work/fonts/`.
4. **Footage from Pinterest** (high quality, ≥720p, no watermarks/burned text, no faces unless the original has them):
   - If `www.pinterest.com` and `*.pinimg.com` are reachable from the shell: search pins, prefer video pins, download the best variant (HLS master → highest resolution via ffmpeg, else V_720P mp4). API notes: `/resource/BaseSearchResource/get/` (`scope: pins`, `rs: typed`), `/resource/PinResource/get/` (`field_set_key: unauth_react_main_pin`), video URLs in `videos.video_list` or `story_pin_data.pages[].blocks[].video.video_list`; pin.it links resolve via `api.pinterest.com/url_shortener/CODE/redirect/`.
   - If blocked (claude.ai sandbox): use WebSearch with `allowed_domains: ["pinterest.com"]` per shot query to collect pin links, then publish an **intermediary page** (artifact) with each shot's clean keyframe, ready search buttons (`pinterest.com/search/videos/?q=…`), the found links, and paste boxes; the user downloads (Pinterest app → download, or a PC script) and uploads the clips. Never route around a blocked domain.
5. **Assign** clips: `shots[i].replacement = {"path": "...", "in": seconds, "fit": "cover", "focus": [0.5,0.5]}` — pick the clip/in-point whose look is closest (view frames).
6. **Build**: `mm_build.build('work', preview=True)` first, then full. Output keeps exact frame count, fps, size and copies the original audio stream; colors matched per shot via LUT; transitions replay the measured kind+progress curve; text replays measured curves.
7. **Check**: compare frames side by side at each shot and text event; fix spec and rebuild. Deliver remake + list of source pin links (credit).

## Rules
- Audio and text are copied, footage is new. Report anything approximated (font substitute, blur timing, unverifiable Pinterest steps).
