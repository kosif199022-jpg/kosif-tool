---
name: kosif-voice-studio
description: >-
  Voice-over, voice cloning, voice design and transcription in Egyptian Arabic,
  MSA, English and 600+ languages - text to speech with word timings
  (words.json) for montage, cloning the user's own voice, designing a voice
  from a description, and audio to SRT/VTT. Uses a running VoiceStudio
  backend when there is one, else free edge-tts, offline piper and
  faster-whisper. Use when the user wants «تعليق صوتي», «صوت», «اقرأ النص ده»,
  «استنسخ صوتي», «فرّغ الصوت», «ترجمة الفيديو», TTS, dubbing or subtitles.
---

# KOSIF Voice Studio - صوت، استنساخ، وتفريغ

One CLI for speech and listening. Every result is measured (ffprobe duration,
codec, loudness) and written with a receipt next to it, so nothing is called
audio until it plays.

```bash
T=.claude/skills/kosif-voice-studio/scripts/voice_studio.py
python3 $T doctor                                        # what runs here, install line for the rest
python3 $T speak "صباح الفل يا جماعة" --out out/<job>/voice.mp3     # + words.json + receipt
python3 $T speak --file script.txt --voice ar-EG-ShakirNeural --rate +5% --out out/<job>/voice.mp3
python3 $T transcribe voice.mp3 --out out/<job>/voice.srt --lang ar   # + words.json
python3 $T voices --engine edge --lang ar                # Arabic voices
python3 $T clone me.wav --name "King" --ref-text "النص المقروء" --i-own-this-voice   # VoiceStudio
python3 $T design "راجل كبير في السن صوته عميق وهادي" --name Grandpa [--save]        # VoiceStudio
python3 $T verify any.wav                                # measured, never assumed
```

Add `--json` before the command for one-line machine output. Run from the
repo root. Behind a proxy with its own CA, set `SSL_CERT_FILE` to the bundle.

## Engines and what each really does

| Engine | How it is reached | Does | Needs |
|---|---|---|---|
| **VoiceStudio** | its HTTP API on `http://localhost:3900` (or `--url` / `$VOICESTUDIO_URL`, `$VOICESTUDIO_TOKEN`) | speech in saved/cloned/designed voices, clone from a clean reference, design from words, transcription, dubbing, 646 languages, its own MCP at `/mcp/` | the user's installed app (desktop, Docker, or server); GPU optional, CPU is slower; first use downloads its model (~2.3 GB) after asking |
| **edge** (edge-tts) | Microsoft's online read-aloud voices | speech, Egyptian `ar-EG-SalmaNeural` (female, default for Arabic) and `ar-EG-ShakirNeural` (male), word timings | `pip install edge-tts`, internet, no key. No cloning |
| **piper** | local ONNX voice on the CPU | speech fully offline (`ar_JO-kareem-medium` for Arabic) | `pip install piper-tts` + one voice download (`doctor` prints it). No cloning |
| **whisper** (faster-whisper) | local model | transcription with word timings, SRT/VTT/TXT/JSON | `pip install faster-whisper`; model downloads on first run. Use `--model small` (default) or `medium` for Arabic; `tiny` is too weak for Egyptian |

`--engine auto` (default) tries VoiceStudio, then edge, then piper for
speech, and VoiceStudio, then whisper for transcription. The receipt lists
what was skipped and why. Pass `--engine` to force one; then a failure is an
error, not a silent switch.

Tested in a cloud session on 2026-11-02: edge (Egyptian voice + 8 word
timings), piper (Arabic offline) and whisper (Arabic SRT) ran for real. The
VoiceStudio path is tested against a fake backend with the same routes; it
was not run against the real app here (no app in the cloud machine).

## The loop for a voice-over

1. **Script first.** Short spoken lines in the user's dialect. For long text
   run `python3 .claude/skills/kosif-superpowers/scripts/tts_script.py chunk|estimate`
   to check length before spending anything.
2. **Pick the voice.** The user's own cloned voice (VoiceStudio) > a designed
   one > `ar-EG-SalmaNeural`/`ShakirNeural`. Say which one was used.
3. **Speak** with `speak`. It writes the audio, `<out>.receipt.json` and
   `words.json` (`[{word,start,end}]`, sorted, non-overlapping - the format of
   `playbooks/audio-sync.md`). edge gives word timings directly; for other
   engines run `transcribe` on the result to get them.
4. **Into the film.** `words.json` drives the motion timing in
   `kosif-web-film`, Montage Pro and the Remotion starters; the audio export
   rules in `playbooks/export-standard.md` still apply.
5. **Report** engine, voice, measured duration and the receipt path.

## Cloning and design (VoiceStudio)

- **Consent:** clone only the user's own voice or a speaker who agreed. The
  tool refuses without `--i-own-this-voice`. Never clone a public figure.
- **Reference:** 5 to 15 seconds, one speaker, no music or room echo, and
  `--ref-text` with exactly what is said improves the match.
- `clone` prints the new profile id; use it as `speak --engine voicestudio --voice <id>`.
- `design "<words>"` first shows how VoiceStudio maps the description
  (gender, age, pitch, style, accent, and the words it could not map);
  `--save` creates the profile. A description that maps to nothing is refused.
- Routes are found from the running version's `/openapi.json`, so a moved
  prefix does not break the tool; a missing route is reported by name.
- Dubbing, long-form audiobooks and batch jobs: use the app or its OpenAPI
  directly (they are asynchronous jobs with ids); this CLI does not wrap them yet.

## Without VoiceStudio

- Clone or change a voice in the cloud: Higgsfield MCP `create_voice`,
  `voice_change`, `dubbing`, `generate_audio`. They spend credits: show the
  text and voice, get the user's yes first.
- Music and songs are not this skill: Suno first (appendix A46).

## Rules

- Never say a file is audio, or a transcript is done, without the tool's
  measurement. An HTTP error body saved as `.wav` fails `verify`.
- Never download a model, install the app, or call a paid service without
  the user's yes; `doctor` only prints the install line.
- Keep the user's original audio untouched; outputs go to `out/<job>/`.
- Tokens stay in the environment; the tool never prints them.

## Credit and licence

The capabilities map to [VoiceStudio](https://github.com/debpalash/VoiceStudio)
by Palash Debnath and contributors (AGPL-3.0; its OmniVoice model code is
Apache-2.0 and the default weights are CC-BY-NC, so check before commercial
use). This skill talks to a running VoiceStudio over its public HTTP API and
contains none of its code or text. `voice_studio.py` is new KOSIF code. See
`THIRD_PARTY_NOTICES.md`.
