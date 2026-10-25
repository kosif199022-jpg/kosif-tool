# Export standard — معيار التصدير

The owner approved these settings after the «داري يا قلبي» reel and asked for them on **every** future video export. Treat them as the floor: a change may raise quality (slower preset, lower CRF, better colour accuracy), never lower it.

صاحب المشروع اعتمد الإعدادات دي بعد فيديو «داري يا قلبي»، وطلب إنها تبقى الأساس في كل تصدير جاي: نفس الجودة أو أحسن، وعمرها ما تقل.

| setting | value | why |
|---|---|---|
| size | **1080×1920** (9:16) by default | TikTok/Reels show ~1080 in the end; a 941×1672 source grows only ~15% and stays sharp |
| 4K | **only when the user asks** (`render_html.cjs --scale 2`) | a 2.3× upscale makes text razor-sharp and the picture look soft next to it, which reads as lower quality |
| fps | **30** | |
| video | **H.264 High, CRF 17, preset slow**, yuv420p | near-transparent; no banding in skies and fog; `slow` packs the same quality smaller than `medium` |
| colour | converted with the **BT.709** matrix and tagged BT.709 (tv range) | stops phones guessing BT.601 and shifting reds/greens |
| colour grade | **matched to the source by measurement** | sample the source's black level, sky and skin colours and match them; never a stock LUT. Part of the "quality" feel |
| audio | the user's track **stream-copied byte for byte** when MP4 can carry it (AAC, MP3, ALAC) | prove it with `verify_video.py --audio <master>` |
| audio fallback | AAC **320k 48 kHz** only when the source cannot live in MP4 (WAV/FLAC) or a step must cut/mix/loudnorm it | keep the master untouched next to the delivery |
| file | **MP4 `+faststart`** | plays at once, before the whole file downloads |

Upload tip for the user: turn on «Upload HD» in TikTok's settings.

## Where it lives

- `.claude/skills/kosif-superpowers/scripts/export_profile.py` is the single source: `video_args()`, `audio_args(src)`, `FASTSTART`, and `python3 export_profile.py` prints the profile as JSON. New scripts should import it instead of writing their own ffmpeg flags.
- `tools/render_html.cjs` (and its skill copy `resources/motion-runtime/render_html.cjs`) encodes with exactly these settings by default.
- `montage_pro.py`, `fast_edit.py`, `look_pipeline.py`, `kosif_timeline.py`, `unified_cinematic.py`, `blender_cinematic_bridge.py`, `cinematic_broll_render.py`, `atlas_render.py`, `unified_media.py`, `creative_paint.py`, `native_3d.py`, the Blender/character renderers and `styles/dua` all use CRF 17 / preset slow.
- Previews and proxies (`--preview`, the 540p proxies, contact sheets) are not deliveries and stay fast.

## Manual encode from frames

```bash
ffmpeg -framerate 30 -i frames/frame_%06d.png -i voice.m4a -map 0:v -map 1:a \
  -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -profile:v high -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -c:a copy -t <video seconds> -movflags +faststart out/film.mp4
```

For a WAV/FLAC voice replace `-c:a copy -t …` with `-c:a aac -b:a 320k -ar 48000 -af apad -shortest`.

## Checklist before delivery

1. `ffprobe` shows 1080×1920, 30 fps, h264 High, yuv420p, bt709.
2. `python3 tools/verify_video.py out/film.mp4 --audio <master>` passes (audio identical when copied).
3. Not 4K unless the user asked for it.
