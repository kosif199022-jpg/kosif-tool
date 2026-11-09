# lemomo-ai/lemo-opuscar — REA dissection (@143f387ad774525dc9abc0ff05fb5f4bfbaa5f02, 14,056★, MIT © 2026 LemoLab)

## What it really does
A library of film "styles" for coding agents: `styles/<slug>/` = STYLE.md prompt + style.json + DEMO.md + a code-only demo film, on a shared toolkit in `core/`.
- Picture: a film is an index.html exposing `window.DUR`, a deterministic `render(t)`, `READY`, optional `EV` (sound/cue events) and `TEXTS(t)` (visible texts + boxes). serve.mjs (127.0.0.1), page.mjs (playwright-core headless Chrome), video.mjs (N workers, JPEG → ffmpeg, lossless segment join, output lock).
- Checks: readcheck.mjs, still.mjs/sheet.py, events.mjs.
- Audio: tts.py (Kokoro offline), tts_zh.py (edge-tts, online), asr_check.py (faster-whisper, numbers compared by value), sfx.py (procedural foley), sampler.py (round-robin sample libraries), pluck.py (Karplus-Strong).
- Master: mux.sh two-pass loudnorm to -14 LUFS → 4× oversampled limiter → re-encode until true peak ≤ -1 dBTP; detects truncated WAVs; atomic write.
- Method: DIRECTOR.md (brief→benchmark→story→treatment→sound→rhythm→camera→performance→delivery→rights), TECHNIQUE.md (one timeline drives picture, score, foley, subtitles).
- Per-demo QA: rhythm_report.py, cuecheck.py, camcheck.mjs, subcheck.mjs, rescheck.mjs.

Architecture: timeline → { render(t) → Chrome frames → video.mp4; TTS → ASR check → word timings; score; foley at EV; srt } → mix.py → mux.sh → film.mp4

## Capabilities (13; path:line)
1. Rhythm report — styles/briefing-board/demo/tools/rhythm_report.py:26-84 (native)
2. Reading-time check, CJK/4.5 + others/15 + 1.5 s, out-of-frame boxes — core/render/readcheck.mjs:13-55 (native, + Arabic 12 cps, SRT, titles ≥4 s)
3. Subtitle hold ≥1.8 s and ≥ speech + 0.6 s — subcheck.mjs:20-22
4. Director rules: hook ≤3 s, ≥4 camera moves, signature shot, reason per shot, ≥2 silences, ≥2 J/L cuts, pace variety, titles ≥4 s, 4/6 axes differ from the demo — DIRECTOR.md:35-132 (native lint)
5. Two-pass master with true-peak loop — core/render/mux.sh:46-129 (source-linked; our verify-video only checks)
6. render(t) contract + parallel capture — core/render/video.mjs:1-60
7. Cue check Δms — styles/art-deco/demo/tools/cuecheck.py:1-20
8. Camera smoothness + reveal guard — camcheck.mjs:1-20
9. Procedural foley — core/audio/sfx.py:9-140
10. Sampled score with credits() — core/audio/sampler.py:570-680
11. ASR check, numbers by value — core/tts/asr_check.py:42-160
12. Easing + monotone track() — core/lib.js:1-44

## Covered vs new
Covered: caption-lines (SRT speed), verify-video (loudness, verify only), video-eyes (motion energy, freezes), cinema-lab (cuts), motion-toolkit (easing), render-html (HTML→video), creative-quality-gate/prompt-forge.
New: picture+sound rhythm in one report (hit→onset ms, silences, pace CV); script-aware reading check; director-rule treatment lint incl. "not the demo again"; true-peak fixing master (linked); camera/reveal guard (linked).

## Native: native_opuscar.py (stdlib + numpy; ffmpeg for rhythm; --json)
rhythm FILM [--events --hit-types --flat --silence-db --tol-ms]; readcheck texts.json|.srt [--size --ar-cps 12 --cjk-cps 4.5 --latin-cps 15 --pad 1.5 --min 1.5]; lint treatment.json [--demo axes.json]; self-test.
Self-test:
```
readcheck: 7 texts, 4 bad as expected; srt 1/2 bad
lint: good treatment ok (5/6 differ); bad treatment 18 issues
rhythm: cuts [2.0, 4.0], 6 onsets, flat secs [0, 1, 5], silences [...], hits aligned 3/3
SELF-TEST PASS
```
Assumptions: the Arabic 12 cps rate and the camera-move vocabulary are KOSIF's, not the source's.

## License & caveats
MIT (vendor with header); fonts OFL; Poly Haven CC0; sample libraries per core/audio/INSTRUMENTS.md. 189 MB mostly media → link, don't vendor. Needs Node 20+, playwright-core, Chrome, ffmpeg 7+. tts_zh.py sends text to Microsoft (consent). DIRECTOR.md §13 (maps/borders policy) is the authors' editorial position, not imported. No installs run.

## REA log
analyze_javascript_application on core (readcheck/video/page/lib) → ev_3b0f8bb7a4db07a6351eef0279563c7441cc5293f2120d1490fd2787d96cfaf2 (parent ev_bf3312b5d434139cd45457f8bfbd104bc60b32ce3228763f8e5d0c931975e729): 4/11 files, 0 failures, 3,903 AST nodes, child-process 4 (ffmpeg), request 0. Partial coverage (selected files). No binary opened. Rest read by hand.
