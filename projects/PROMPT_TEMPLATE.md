# Prompt template — voice-note → synced archival motion film

Paste the block below into a new Claude Code session on `kosif199022-jpg/kosif-tool`, attach the audio, and fill in the `[brackets]` (delete any line you don't need — the defaults are what produced `projects/mafatih-al-tharwa`).

```text
Make a motion-graphics film synced to the attached audio, the same way as projects/mafatih-al-tharwa
in this repo (reuse its src/ as the starting template). Communicate in English.

INPUTS
- Audio: attached file. It is the master clock — never edit, cut or stretch it.
- Title / brand: [programme or channel name, e.g. "مفاتيح الثروة"] · presenter: [name, e.g. "كوتش أبو فيصل"]
- Format: [9:16 1080x1920 full-bleed | 16:9 1920x1080 | 1:1] · 30 fps · whole audio length
- Visual style: [archival sepia-gold documentary | modern clean | other: …]; palette [gold/cream/dark | …]
- Footage: [download public-domain archival footage that fits the story | use only my attached clips | no footage, graphics only]
- Captions: Arabic, keep the speaker's dialect, fix only mishearings and names; key words highlighted
- Must-show names/numbers/spellings: [e.g. كارنيجي، نابليون هيل، 500 مليونير]
- Facts: show only what the speaker says; flag anything doubtful instead of correcting it
- Delivery: master (voice untouched) + social copy (-14 LUFS); [send the file | also a GitHub download link via Git LFS on a feature branch — ask me before publishing anything public]

WORKFLOW (follow CLAUDE.md, AGENTS.md, the kosif-superpowers skill, the kinetic-arabic style and the
arabic-typography, audio-sync and render-pipeline playbooks)
1. Probe the audio (duration, loudness). Transcribe with faster-whisper large-v3-turbo, word timestamps
   (decode to 16 kHz WAV and pass a numpy array — PyAV's file decoding breaks). Run silencedetect and
   re-transcribe any speech gaps VAD dropped. Correct the transcript with a (time, original, fixed) list
   (src/prep_words.py) → words.json + captions.
2. Plan chapters and ~1 hero graphic per key beat (names, numbers, turning points), each triggered on the
   exact word start from words.json. Write PLAN.md, STYLE.md, KOSIF_TASK_QA.md.
3. Footage: search archive.org for items whose metadata licenseurl is public domain; download, record
   SHA-256 + licence in RIGHTS.md. Detect shots, make contact sheets, hand-pick shots per story beat
   (exclude intertitles, credits, superimposed titles). Run src/scan_shots.py to trim fades/dissolves.
4. Build the b-roll track with src/build_broll.py (cuts on caption boundaries, grade, grain, slow
   push/pull/pan, frame-exact length = audio × fps). Then sample start/middle/end of EVERY rendered clip
   and fix any title, black frame or stray shot before going on.
5. Build/adapt the deterministic overlay (src/overlay.html + overlay.js, window.__kosif.seek(t)): kinetic
   RTL captions, chapter header, progress bar, hero graphics. Arabic: whole words only, right→left wipes,
   numbers in <bdi>, local OFL fonts.
6. Preview composited stills (node src/render_film.cjs --stills …), review them visually, fix layout bugs.
7. Full render in 4 parallel chunks, concat, mux the original audio stream with -c:a copy (master), make a
   -14 LUFS / -1.5 dBTP social copy, run tools/verify_video.py on both, spot-check sync at key words and
   chunk seams, fill TEST_REPORT.md.
8. Deliver: send the video file, commit sources/docs to a feature branch (videos via Git LFS only if I asked
   for a link), and report what was verified and what is still uncertain.
```

## Tips
- Long audio (10+ min) renders in roughly 45–60 min on this machine; a 60 s reel takes a few minutes.
- To change only the look, say "keep words.json and the cut list, restyle the overlay".
- To reuse footage from this project, point to `projects/mafatih-al-tharwa/data/shots.json` and RIGHTS.md.
