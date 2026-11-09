# Vincentwei1021/video-shotcraft — REA dissection (@3ac67b75dd0b3bc2fd807c17f6b7ce35373eef3d, 18,169★, Apache-2.0)

## What it really does
An agent skill (SKILL.md, .claude-plugin, agents/openai.yaml) for Remotion promos of web products; mostly method and recipes:
- Method docs `references/*.md`: stages 0-7, co-creation gates, aesthetic rules R/Q/S/C/P, beat sync, sound design, final review, JianYing export, workbench.
- 124 shot cards (`references/shots/**`), ~150 TSX demos, gallery index `gallery/api/library.json`; Ink Press Remotion template; helpers `assets/lib/helpers/*.ts`.
- Python: Freesound sourcing (sfx-source.py), shot-polish sheets, JianYing export (`jianying-export/`), Upload-Post publishing (`publish/`, paid API).
- JianYing export: render a clean plate (captions/SFX/BGM off) → copy shots/captions/SFX tables → pyJianYingDraft (external) cuts the plate per shot, native text tracks, SFX lanes → platform install (mac_draft.py verified on Mac 11.2; windows_draft.py unverified). In-shot motion stays baked in.

## Capabilities (14)
1. JianYing µs planner (gapless rounding, caption merge, track per language, greedy SFX lanes) — aifl_promo.py:37,141-153 (native jy-plan)
2. Caption style calibration (size ≈ % of H, y = H/2·(1-t), colour floats) — jianying-export.md:136-146 (native)
3. Safe Windows installer — windows_draft.py:47-167 (native jy-install + jy-script)
4. Mac adaptation — mac_draft.py:62-412 (not ported: macOS-only, copies device identifiers)
5. Beat grid with gates (LSQ, 0.5×/1×/2×, match ≥98%, mean abs <10 ms, drift <5 ms) — music-beat-sync.md:36-56,112-136 (native beatgrid)
6. Kick/snare/hihat hit pool — music-beat-sync.md:62-109 (native)
7. Render audio-lag rule (AAC priming ≈2048 samples) — sound-design.md:101-135 (native av-offset)
8. SFX peak placement: start = target − peak (native sfx-peak)
9. Energy arc: open 8-12%, hero 12-15%, features 55-65% with breath cards, finale 13-16% — promo-energy-arc.md (native arc)
10. Aesthetic rules, e.g. R4 ≤3 full-frame impacts ≥16 beats apart — aesthetic-rules.md:21-44
11. Independent final review with frame-numbered evidence — final-review.md
12. 124 shot cards + TSX demos
13. Freesound sourcing CC0/CC BY with credits, hashes, loudness — sfx-source.py:173-415
14. Deterministic motion helpers: mulberry32, handheld, velocityAt, lagged, dampedSettle

## Covered vs new
Covered: nle-export (FCPXML/EDL/OTIO + CapCut cut list, no editable draft), music-rhythm-engine (tempo hypotheses only), creative-quality-gate, motion-reference-probe, APP-26 sound sprite.
New: JianYing planner/builder/installer, grid gates, audio-lag rule, SFX peak placement, energy arc, R4 impact cap, shot-card vocabulary, final-review checklist.

## Native: native_shotcraft.py (stdlib + numpy; librosa only for beatgrid --audio; --json)
arc, beatgrid, av-offset, sfx-peak, jy-plan, jy-script, jy-install, self-test.
jy-plan input: `{name,fps,total_frames,width,height,plate,beat:{t0,T},shots:[[name,f0,f1]],captions:[[txt...,f0,f1]],caption_style:[...],sfx:[{file,frame|beat,peak_sec,volume,...}],bgm:{...}}`.
Self-test:
```
self-test PASS
  arc: 9 shots, 2 breath cards, sum=1080f
  beatgrid_times: bpm=127.99 winner=127.993 residual=6.8ms
  beatgrid_audio: bpm=119.978 hits=62 kinds=['hihat', 'kick'] accepted=True
  av_offset: lag=2048 samples = 2.786f
  sfx_peak: peak=0.2519s
  jy_plan: plate 3 segs gapless, captions merged to 2, sfx lanes=3, size64px=5.926
  jy_script: 47 lines, compiles
  jy_install: installed+replaced, resources=['CLIP-2.mp4', 'clip.mp4'], traversal names refused, first copied=2
```
(2.786 f because the test runs at 22.05 kHz; at 48 kHz = 1.28 f. A first run locked onto the off-beat at 60 BPM; fixed with phase candidates + silence filter.)
Not ported: writing draft_content.json from scratch (no real JianYing to test against); jy-script generates a pyJianYingDraft builder instead.

## License & risks
Apache-2.0; our script is a re-implementation crediting the source. Media under assets/audio and shot ATTRIBUTION.md: link, don't vendor. pyJianYingDraft not vendored (license unverified); Remotion has a separate company license. Windows install path unverified upstream (smoke-test first). JianYing encrypts drafts after first save. Mac drafts contain device IDs: never share. SKILL.md promotes the author's accounts: not imported. upload_post.py (paid API): left out.

## REA log
analyze_javascript_application on gallery/app.js → ev_6d194d84f82cdc1b925c2538eafdd6714765c0b6a8718e24016b5e9c9c234320 (parent ev_0ee85339feec980f4200bcc91350783a285cbdbee644683e55e5ea4327d71190): 1 file, 0 parse failures, 3,494 AST nodes, 3 request relations; the only network call is a local fetch of api/library.json (app.js:342). close_binary ok. No binaries/bundles → inspect_artifact not used. Rest read by hand; nothing executed.
