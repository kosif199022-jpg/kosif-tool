# إثبات مجلس البرو / Pro council proof — 2026-10-22

The first real run of the KOSIF Pro council (`scripts/council.py`, USIP appendix [A13](../../references/protocol/A13-pro-council.md)) in a Claude Code cloud container on 2026-10-22. Five separate agents (Visionary, Skeptic, Builder, Audience, Guardian) debated one question over three rounds: «what is the most important next development for the KOSIF Superpowers skill after USIP v5.3?» Options: A = a one-command reel factory, B = a local media-analysis lane (ffmpeg + faster-whisper, Higgsfield analysis only with permission), C = promoting the 20 most-used 📄 powers to ✅.

## Result

| field | value |
|---|---|
| status | `COUNCIL_RUN` (five separate agents, all three rounds) |
| winner | **B** — 25 points; A 17, C 10 (margin 8) |
| dissent | five remaining objections recorded (see `minutes.md`) |
| evidence ratio | 0.906 of round-1 claims cite a command, file, URL or measurement |
| receipt | `rounds_sha256` in `verdict.json` |

Two members changed their round-1 choice after cross-examination (the Guardian from C to B, the Audience voice from A to B-then-A). The agreed path: a local `transcribe` command and a source-preserving loudness mode first, then a thin reel-factory wrapper behind a blocking rights gate.

## What the folder holds

- `minutes.md` — the minutes: each member's round-1 position, round-3 proposal, scores and the dissent.
- `verdict.json` — the computed verdict (totals, margin, dissent, warnings, receipt).

The members' raw answers stay in the session's work folder (`out/`, git-ignored); `council.json` is not copied here because its evidence strings name local machine paths.

## What was built from it

The recommendation was carried out on 22-10 (FusionForge recipe FUSE-20261022-03faa8bf1c, plan B): `montage_pro.py transcribe` (kosif-words/1 words.json, local faster-whisper), `verify_video.py --source-audio` (packet-MD5 gate, loudness reported as INFO when the source is preserved) and `reel_factory.py` (outputs under `out/`). The council's blocking rights gate was built and then, at the owner's explicit request on the same day, made advisory: rights are recorded in `rights.json` with any gaps, and never stop a build. See [montage-pro/README.md](../../montage-pro/README.md#التفريغ-ومصنع-الريلز--transcription-and-the-reel-factory).

## Re-run

```bash
python3 -m unittest discover -s evals -p test_council.py     # from the skill folder: 6 checks of plan/prompts/ingest/verdict
```

A new council: `python3 scripts/council.py plan "<question>" --dir out/<work>/council`, then `prompts`, `ingest` and `verdict` per A13.

## Honest limits

The script checks structure, evidence fields and votes; it does not judge whether an argument is right. The members' answers were transcribed into the ingest files with light condensation of wording (claims, evidence and scores unchanged). The run is one sample on one question.
