# KOSIF Cinema Pro — unified skill orchestration

Goal: one **verified** professional montage, not a deceptive claim that all 5,857 documented powers were executed.

## Entry points
From the repository checkout:

```bash
S=.claude/skills/kosif-superpowers/scripts
python3 "$S/cinematic_pro_conductor.py" doctor
python3 "$S/cinematic_pro_conductor.py" plan --kind audio
python3 "$S/cinematic_pro_conductor.py" plan --kind video --option highlight-reel
python3 "$S/cinematic_pro_conductor.py" run input.mp3 --job out/cinema/my-reel --option kinetic-film --style cinematic
python3 "$S/cinematic_pro_conductor.py" run input.mp4 --job out/cinema/my-reel --option highlight-reel --style 30
python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_cinematic_pro_conductor.py'
python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_montage_pro.py'
```

The new conductor routes through the existing proven `montage_pro.py`. It does not replicate the renderer. It inventories all top-level skills, lists 13 task-force roles, and exposes optional modules (SEE Pro reasoning, cinematic direction, music, caption alignment, shot selection, 3D and QA). **Listed** does not equal **called**. Only a stage in `receipt.executed` counts as executed.

## Default project contract

- Input: media the user owns or is permitted to edit. External footage is separately licensed; this command never downloads, spends API credits, or silently calls Katana/Higgsfield.
- Analyse: checksum, ffprobe, measured sound energy, source cuts; distinguish detected transients from beats. Speech transcripts must come from a verified transcript; this wrapper does **not** invent captions.
- Decide: audience, platform, hook, story structure, motion language, visual references, typography, soundtrack; select the smallest cohesive set of techniques. READ relevant skills: editorial-film-edit for reference style, kosif-infinite-matrices for experimental patterns, Instagram discovery for reference searches, and A12 SEE Pro for critical review. Activate their **executors** only when actually available and relevant.
- Build: audio `kinetic-film` by default, video `highlight-reel` by default. Other Montage Pro supported options require explicit selection; some options need other assets, and `reference-remix` returns an editable project, not a finished MP4.
- Verify: *actual* nonempty MP4, `verify_video.py` exit 0, unchanged source SHA-256, and any optional delivery mix verified. A planned or exported intermediate stage cannot pass. Human frame/audio review is still required before calling the edit artistically final.
- Output: `out/cinema/<job>/cinema_pro_receipt.json`, plus Montage Pro's `intake.json`, `options.json`, `report.json`, working files and the MP4 when successful. The receipt uses `status=verified` only if the executable gate passes, not merely if the file exists.
- Export: follow the source-approved 1080×1920 H.264/BT.709 profile documented in `playbooks/export-standard.md`. The standard is 30 fps; use 60 only when deliberately requested and actually supported end-to-end. Retain the approved master sound wherever legally and technically possible.

## Important limitations

One command orchestrates **relevant** modules, rather than force-running unrelated plugins, installing system software, generating with paid APIs, or using a mock LLM council. This revision does not automatically compose separate 3D, B-roll, WhisperX and storyboard executors into a unified timeline; those remain opt-in specialist workflows that require assets, environment checks, timing handoffs, and visual QA. Treat `doctor` as an environment probe and `plan` as a proposal, never as completion evidence.

Tests added: candidate/actual-role separation; unsupported option rejection; missing/empty MP4 refusal; verification failure; changed source; missing inputs; extra mix failure; and a saved failed-run receipt.
