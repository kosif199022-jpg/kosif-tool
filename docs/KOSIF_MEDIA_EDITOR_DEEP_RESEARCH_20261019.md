# KOSIF Deep Media-Editor Research — 2026-10-19

## Evidence distinctions
- **REA 6.7.0:** read-only static inspection previously performed on six locally stored installers (Premiere-labelled, CapCut, Canva, Animate, Houdini, FontLab). Installer inspection confirms file format/hash, **not the application's full capabilities**.
- **REA first-party code:** analyzed KOSIF `web/`, with four JS files parsed, 10,882 AST nodes inspected, 35 findings, zero parse failures.
- The local folder `Desktop/تجربة` contains video/design distributions plus the KOSIF source repository; locally present executables are not proof that the applications are installed or usable.

## Official editor techniques worth adopting independently

| Product | Verifiable capability | Suggested KOSIF direction |
| --- | --- | --- |
| Premiere | Scene edit detection, auto reframe | Audio-locked shot splitting and subject-aware vertical crop |
| DaVinci Resolve | Fusion node compositor, AI content search, color page | Searchable footage bins and vector compositing graph |
| Descript | Linked text/footage edit interface and captions | Immutable narration word-index timeline with independent B-roll |
| Blender | Video sequencer, masks, motion tracking | Local trackable overlays and depth-aware movement |
| Houdini | Procedural particle trails | Deterministic rain/dust/wind environmental layers |
| Remotion | Deterministic frame animation and audio visualisation | Frame-addressed Arabic titles and speech/beat events |
| OpenTimelineIO | Standard edit decision interchange | Future export of editable KOSIF timelines |

Primary documentation:
- https://helpx.adobe.com/premiere/desktop/edit-projects/change-clip-sequence/detect-edit-points-using-scene-edit-detection.html
- https://helpx.adobe.com/premiere/desktop/add-video-effects/commonly-used-effects/auto-reframe-overview.html
- https://www.blackmagicdesign.com/sa/products/davinciresolve/whatsnew
- https://www.descript.com/features
- https://docs.blender.org/manual/en/latest/video_editing/workspaces.html
- https://www.sidefx.com/docs/houdini/nodes/sop/particletrail.html
- https://www.remotion.dev/docs/audio/visualization
- https://github.com/AcademySoftwareFoundation/OpenTimelineIO

## Added original capability: REAL camera-motion B-roll renderer

`.claude/skills/kosif-superpowers/scripts/cinematic_broll_render.py`

This module accepts a frame-precise EDL created by `cinematic_cut_planner.py`, a vetted footage manifest, and the original audio. It uses FFmpeg to crop-to-fill video, apply different continuous push/pull/pan movements, produce exact frame counts, concatenate shots and stream-copy the original audio without editing narration.

It refuses mismatched source hashes, missing license evidence, unverified review flags, missing media, invalid timelines, insufficient codec support or overwriting its destination.

Usage:

```bash
python .claude/skills/kosif-superpowers/scripts/cinematic_broll_render.py --edl film_edl.json --manifest approved_footage.json --audio original.wav --out footage_master.mkv
```

The script is a **real video renderer**, but it does not yet generate Arabic caption overlays, source videos, motion particles or the final social-audio mix. Licensed video selection and visual review must precede rendering; a boolean in a manifest is not independent evidence of actual human review.

Tests `tests/test_cinematic_broll_render.py` generate their own local synthetic footage and verify an actual 60-frame, two-shot render with unchanged encoded audio-stream hash. Synthetic tests validate technical behavior, not aesthetic quality.

## Prioritized gaps
1. Source-specific rights provenance and frame review for embedded text / people.
2. Arabic word-aligned kinetic text rendered on top of genuine video.
3. Motion-aware subject-centering for 9:16 reframe and shot color matching.
4. OpenTimelineIO interchange and visual transcript editing.
5. Node-based compositing, deterministic effects, shot-context review, final QA.

No commercial code, copyrighted templates or unauthorized services are included in this contribution.
