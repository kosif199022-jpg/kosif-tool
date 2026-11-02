# Black Dragon: real media execution (Superpowers)

This workflow closes a genuine integration gap: the three existing media programs can now process *one explicitly supplied* media asset with a durable evidence report.

**Important:** The full Black Dragon inventory contains descriptions, playbooks, skills and executable programs. A description with no executable adapter is **not broken code** and is never counted as executed. The media runner does **not** relabel the ~7k catalog entries as runnable. The number of reviewed adapters is taken from the live registry rather than a fixed historical number.

## Commands (from repository root)

```bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon_media.py doctor

# Analyze a video and make genuinely processed video exports (explicit local approval):
python3 .claude/skills/kosif-superpowers/scripts/black_dragon_media.py run \
  --input "/path/to/owned_clip.mp4" --job-name my-video-001 --execute \
  --stabilize --reframe --grade-look teal-orange

# No transformations: analysis, scene detection and rhythm map only
python3 .claude/skills/kosif-superpowers/scripts/black_dragon_media.py run \
  --input "/path/to/owned_audio.wav" --job-name my-audio-001 --execute

python3 .claude/skills/kosif-superpowers/scripts/black_dragon_media.py verify --job-name my-video-001
```

## What *actually* runs

1. **montage_pro intake:** probes the supplied file, analyzes loudness, measures source audio and, on video, obtains a cut/contact-sheet analysis. Does *not* transcribe or download models.
2. **audio_cue_mapper:** measures RMS/onset candidates; for long media, analyzes a separately extracted first-120-second excerpt (clearly labeled partial coverage).
3. **music_rhythm_engine:** estimates possible BPM and beat grid from *measured* transients, explicitly not verified musical ground truth or emotional interpretation.
4. **cinema_lab scenes:** for video, produces a real scene segmentation file, default ffmpeg engine. Pass `--skip-scenes` to omit it.
5. **cinema_lab stabilize/reframe/grade:** only with the explicitly requested flags. Processes the source in the order stabilization → 9:16 subject-guided reframe → selected named grade. Written MP4s appear under `out/black-dragon-media/JOB/exports/`.

Outputs include `black_dragon_media_report.json`, `rhythm.json` when audio exists, a `scenes/scenes.json` when video scenes are requested, plus intermediate media analysis and optional actual MP4s. The receipt records commands, exit codes, file sizes, hashes, and failure details. `verify` independently re-hashes every reported stage output and rejects mismatches, missing paths and symlink references.

The runner refuses to overwrite an existing job and requires `--execute`. It uses local ffmpeg and bundled repository scripts; no web calls, installation, Higgsfield/Kling charges, or paid model selection. Media processing uses the current OS user's permissions, **not a process sandbox**. Before processing confidential media, use an appropriate isolated OS environment.

**Limitations:** The mere presence of tools does not prove their installed dependencies or cinematic quality; test with real input and visually inspect the results. Rhythm hypotheses are not word-level sync. This workflow is **not** autonomous film generation and **not** evidence that the entire catalog executed. For word-level sync, supply separately aligned transcript data to the project's supported transcription/alignment workflow. For full Black Dragon orchestration, use `black_dragon.py` and its reviewed adapter approval gates.

## Tests

```bash
python3 -m unittest discover -s tests -p 'test_black_dragon_media.py' -v
```

The tests cover rejected paths, explicit consent, tamper detection and a generated original WAV actually processed through the bundled audio tools (ffmpeg required). The new workflow's integration test runs independently of the legacy catalog plan and never claims whole-catalog coverage.
