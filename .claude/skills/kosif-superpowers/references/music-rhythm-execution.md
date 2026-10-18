# KOSIF Music Rhythm Intelligence — executable tempo and motion

New original KOSIF Superpowers runnable module. It estimates alternative tempo hypotheses and relative audio energy sections from **measured local RMS/onset timestamps**, then connects timed transients to real animated Remotion scenes. It does not identify songs, infer lyrics, musical key, instruments, emotion, performers or other semantic content.

## Commands (original audio is master clock)

    SKILL_DIR=.claude/skills/kosif-superpowers
    python3 "$SKILL_DIR/scripts/audio_cue_mapper.py" ./voice.wav --out ./cues.json
    python3 "$SKILL_DIR/scripts/music_rhythm_engine.py" ./cues.json --out ./rhythm.json

Inspect candidate_tempo_bpm, tempo_hypotheses, estimated_grid_seconds and relative_energy_sections. The beat grid and BPM remain **unverified hypotheses**, even with high periodic alignment, due to possible half/double-time ambiguities and noisy audio.

When you also have a licensed video reference, build an original editing project:

    python3 "$SKILL_DIR/scripts/motion_reference_probe.py" ./reference.mp4 --cuts --out ./cuts.json
    python3 "$SKILL_DIR/scripts/reference_edit_engine.py" --probe ./cuts.json --cues ./cues.json --out ./editable-remotion-project

The generator now adds a pulseFrames array for actual measured transient candidates per shot. Original React source consumes that array and animates scale/zoom continuously, even with no external visual assets. This is executable music-responsive animation, not a static slideshow and not a proprietary Katana clone.

Before running Remotion from the new project, check its special commercial license, authorize local npm installation, preview with npm run studio and independently validate the rendered MP4. KOSIF does not silently download external packages or change original media.

## Exactly what is measured

- RMS amplitude and rising-energy transient candidates from a real uncompressed PCM WAV.
- Multiple tempo hypotheses from alignment of onset timestamps to plausible beat grids, with an explicit alignment score. Insufficient events => no BPM returned.
- Per-second relative energy compared with the median of the recording.
- Deterministic frame-level pulse movement in a new Remotion project (a separate renderer must verify MP4 output).

## What still needs independent licensed adapters

Librosa for deeper onset and beat inference; Essentia for descriptors (pay attention to AGPL source licensing); Meyda, Tone.js and Wavesurfer for additional browser audio control; WhisperX for original song-word alignment (existing KOSIF importer already accepts its JSON); and SAM2/CoTracker for actual video object motion. These are **not** silently installed or counted as proven here.

## Tests

    python3 -m unittest discover -s "$SKILL_DIR/evals" -p test_music_rhythm_engine.py -v
    python3 -m unittest discover -s "$SKILL_DIR/evals" -p test_reference_edit_engine.py -v

Synthetic test clips prove the algorithm and source generation; they do not prove audio-emotion interpretation or final commercial film quality.
