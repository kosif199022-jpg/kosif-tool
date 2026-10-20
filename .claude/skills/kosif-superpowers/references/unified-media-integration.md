# Unified Media: photographs + drawing + 2D motion

**Tested original KOSIF integration**, not a Photoshop clone or 3D renderer.

The `scripts/unified_media.py` entrypoint composes **three existing KOSIF runtimes** in one reproducible job:

1. **App Studio** (`scripts/app_studio.py`) pre-processes an authorized local image with a strictly named operation: `none`, `develop`, `ink-sketch`, or `pencil-sketch`.
2. **Unified Draw** (`scripts/unified_draw.py`) converts ordered strokes, geometric shapes, and their optional keyframes into a layered scene.
3. **Creative Paint** composites time-varying transparent drawing layers onto the source image. Pillow produces PNG/GIF; FFmpeg produces H.264 MP4.

## Demo

From `.claude/skills/kosif-superpowers/`:

```powershell
python scripts/unified_media.py doctor
python scripts/unified_media.py render --photo templates/unified-media-demo-photo.png --scene templates/unified-draw-motion-demo.json --output ./photo-draw.png --effect develop --exposure 0.4
python scripts/unified_media.py render --photo templates/unified-media-demo-photo.png --scene templates/unified-draw-motion-demo.json --output ./photo-motion.mp4 --effect develop --exposure 0.4 --fps 12 --duration 2
python scripts/test_unified_media.py
```

Use unused output filenames; outputs do not overwrite existing files. Input photos must be local JPG/JPEG/PNG/WebP (at most 30 MB / 32 megapixels). Canvas fit is a centered crop (cover), so if photo and canvas aspect ratios differ, edge content may be cropped. A screenshot, user's authorized photo or synthetic image works; the included example is **procedurally generated**, not a real photograph. All image types are decoded via Pillow; no remote URLs or unknown effects are accepted.

### Limits and guarantees

Animation is 2D layer positioning/opacity/rotation/scaling, **not** photorealistic 3D or a Blender render. Output options: PNG, GIF, MP4. Animation: 1-60 FPS, <=30 seconds and no more than 300 frames, with an additional GIF pixel budget. GIF uses RGB frames, and video has no audio track. Image adjustments are applied once to the background, not independently per animated frame. The output is flattened; original editable layer source remains the `kosif.unified-draw.v1` JSON.

The App Studio source cited analyzed commercial applications, but this integration only invokes original, existing KOSIF implementations. It does not import any vendor proprietary code.

## Tests and provenance

2026-10-20, Windows laptop:

- **9/9** new `test_unified_media.py` tests passed: photo+shape pixels, animation pixels, PNG SHA-256 receipt, actual App Studio photo exposure, GIF, FFprobe-verified H.264 MP4, input and overwrite validation, effect allowlist, bounded frames and missing dependency.
- Previous Unified Draw suites (6+7 tests) and original Smart Draw/Creative Paint suites remain separately runnable.
- Acceptance: **3 processed PNGs plus 24-frame GIF and 24-frame H.264 MP4, 640×480 at 12 FPS for 2 seconds**, with hashes and FFprobe metadata in `proofs/unified-media-acceptance-20261020.json`.
- Outputs are stored on the authorized Windows computer under `C:\Users\Public\KOSIF-UNIFIED-MEDIA-ACCEPTANCE-20261020`; GitHub stores the original demo asset and receipt, not a user's photograph.

This is a tested **inter-group workflow (photo editing + drawing + 2D video)**, not full operational unification of all 5,185 catalog entries.
