#!/usr/bin/env bash
# Voice pipeline for the "arabic-voice-kinetic" proof.
#   Piper TTS (+ phoneme-timing oracle) -> 0.6 s lead pad -> two-pass loudnorm delivery copy
#   -> faster-whisper words -> waveform-refined words.json / words.js
# usage: make_voice.sh <scratch-out-dir> <venv-dir> <piper-model.onnx> <hf-cache-dir>
set -euo pipefail
OUT=$1; VENV=$2; MODEL=$3; HF=$4
HERE=$(cd "$(dirname "$0")" && pwd)
LEAD=0.6; TOTAL=11.5          # film length in seconds (= master audio length)
mkdir -p "$OUT"; cd "$OUT"

# 1. voice + ground-truth word timing from Piper's own phoneme durations
"$VENV/bin/python" -I "$HERE/synth_voice.py" "$MODEL" "$HERE/line.txt" voice_raw.wav tts_align.json

# 2. master = untouched voice, 48 kHz, 0.6 s lead-in, padded to the film length
ffmpeg -hide_banner -loglevel error -y -i voice_raw.wav \
  -af "aresample=48000,adelay=$(python3 -c "print(int($LEAD*1000))"):all=1,apad=whole_dur=$TOTAL" \
  -t $TOTAL -ac 1 -c:a pcm_s16le voice_master.wav

# 3. delivery copy: gentle glue (3:1 above -24 dB, peak ceiling -9 dBFS) then two-pass loudnorm,
#    linear mode, -14 LUFS / -1 dBTP / LRA 11, 48 kHz stereo
ffmpeg -hide_banner -loglevel error -y -i voice_master.wav \
  -af "acompressor=threshold=-24dB:ratio=3:attack=4:release=90:makeup=2,alimiter=limit=0.35:attack=2:release=60:level=false:asc=1" \
  -c:a pcm_s24le voice_pre.wav
M=$(ffmpeg -hide_banner -i voice_pre.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
get() { echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -hide_banner -loglevel error -y -i voice_pre.wav -af \
  "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true" \
  -ar 48000 -ac 2 -c:a pcm_s24le voice_delivery.wav
ffmpeg -hide_banner -nostats -i voice_delivery.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"

# 4. words: faster-whisper small (Arabic, word timestamps) on the master, then refine on the waveform
HF_HOME="$HF" "$VENV/bin/python" -I "$HERE/transcribe.py" voice_master.wav asr_raw.json
"$VENV/bin/python" -I "$HERE/align_words.py" voice_master.wav asr_raw.json "$HERE/line.txt" \
  "$HERE/words.json" "$HERE/words.js" tts_align.json $LEAD
