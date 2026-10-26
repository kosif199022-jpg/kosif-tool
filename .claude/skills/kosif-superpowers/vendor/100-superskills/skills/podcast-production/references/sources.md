# مصادر «إنتاج البودكاست» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## joined-audio-transcript-drift (3323-joined-audio-transcript-drift)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/joined-audio-transcript-drift
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift
- الوصف: Keep timestamps aligned when joining many audio files into one. Use when: (1) subtitles, transcript segments, chapters or bookmarks drift later and later through a concatenated file; (2) the joined file is seconds longer than the sum of its parts; (3) ffmpeg's concat demuxer prints "Application provided invalid, non monotonically increasing dts to muxer"; (4) you are stitching TTS chunks, per-chap

```markdown
# Joined audio drifts away from its transcript

> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/joined-audio-transcript-drift/SKILL.md`).

## Problem

You join many audio pieces into one file and build a transcript, a chapter
list or a set of bookmarks by adding up each piece's duration. Early
timestamps look right. Later ones point at the wrong place, by more the
further in you go.

The cause is that a compressed piece is longer than the audio it represents.
An encoder pads the start and end of every file, and records in a header how
much to trim. `ffprobe` reports the *trimmed* duration, which is what a player
would give you, but `concat -c copy` copies whole frames and keeps the padding
of every piece. Each join therefore adds a few tens of milliseconds that your
arithmetic never sees, and they accumulate.

Measured on 181 pieces joined into one 164-minute MP3: the joined file ran
**9.1 seconds longer** than the sum of the pieces, about 50 ms per join.

## Context / Trigger conditions

- Timestamps are correct at the start of a joined file and progressively later
  toward the end.
- The joined file's duration is longer than the sum of the parts' durations.
- ffmpeg prints, during a copy-mode concat:
  `Application provided invalid, non monotonically increasing dts to muxer in stream 0`
- You are stitching synthesized speech chunks, per-chapter or per-track
  downloads, or recorded segments, and something downstream needs to seek by
  time: captions, bookmarks, chapter marks, alignment.

## Solution

### Do not trust frame counts either

The obvious repair is to compute each piece's contribution from its frame
count rather than its trimmed duration:

```bash
ffprobe -v error -select_streams a:0 -count_frames \
  -show_entries stream=nb_read_frames,sample_rate -of json piece.mp3
```

For MPEG-2 Layer III (sample rates 16/22.05/24 kHz) a frame is 576 samples;
for MPEG-1 (32/44.1/48 kHz) it is 1152. This gets closer but still does not
match: each input's header frame (Xing/Info/LAME) is copied through as well,
so the joined file carries roughly one extra frame per piece. On the same
29-minute test the frame arithmetic was still 1.3 seconds out.

### Encode once, and the arithmetic holds

Decoding everything and encoding the result once produces a single contiguous
stream whose length is the sum of the decoded pieces:

```bash
ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i list.txt \
  -c:a libmp3lame -b:a 64k -ar 24000 -ac 1 -write_xing 0 joined.mp3
```

On the same material this brought 2.51 seconds of drift down to **0.06
seconds**, and took 6 seconds for a 29-minute file. `-write_xing 0` keeps the
output from gaining a header frame of its own.
```

## transcript-to-content-pipeline (1181-transcript-to-content-pipeline)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coachlou/ambient-library/tree/2b66a4a4e764bd5884e652e8759a80cacab244fe/library/transcript-to-content-pipeline
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1181-transcript-to-content-pipeline/2789-transcript-to-content-pipeline
- الوصف: Turns a raw transcript or session notes into a full content package (article, LinkedIn variants, summary, audio script); use for "turn this into content", "write something from this transcript".

```markdown
Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/transcript-to-content-pipeline/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
```

## write-realtime-audio-code (1059-write-realtime-audio-code)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cboone/agent-harness-plugins/tree/d9e1b396852487c90500486a7b4fe94d88c64bd0/plugins/write-realtime-audio-code
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1059-write-realtime-audio-code/2342-write-realtime-audio-code
- الوصف: Write or review real-time audio callbacks: audio-thread safety, lock-free messaging, and plugin state. Not for generic queues, GUI, or offline DSP.

```markdown
# Write Real-Time Audio Code

Use the host contract and a stated communication protocol to make callback-reachable code safe, bounded, and compatible.

## When to Use

Apply this skill to an audio callback and all of its reachable code, including audio-to-UI paths, audio-related atomics and lifetimes, real-time verification, plugin parameters and state, event timing, smoothing, numerical behavior, and host-independent cores.

Do not activate it only because a change has a queue, an atomic, DSP mathematics, GUI code, server concurrency, or offline processing. Shared code remains in scope when a real-time callback reaches it. Check a host-specific offline-rendering contract before treating that mode as non-real-time.

## Core Constraints

An audio callback has bounded work only in the context of its host contract. Inspect transitive callees, notifications, payload copies, and final destruction. Prove that shared-memory access, state publication, storage reuse, aliases, and required output samples are legal. Preserve released identities, automation meaning, and host transitions. A race detector gives evidence about exercised access patterns; it does not measure deadline compliance.

## Read the Callback Contract First

Record these facts before choosing an implementation or review conclusion:

- The host API, lifecycle phase, symbolic thread, and any render workers.
- Buffer layouts, sample formats, aliases, lifetimes, legal block sizes, and required output behavior.
- Pending-event and process-status obligations, including reset, flush, and deactivation.
- Whether processing is real-time or an explicitly supported offline mode.

Use the downstream project's existing conventions to record relevant entry points and boundaries. Do not require a new thread annotation on every function.

## Workflow

1. Establish whether the request is a review, plan, or authorized implementation. In review and plan modes, produce findings or proposed checks without editing the downstream project, installing tools, running mutation experiments, committing, publishing, or automatically invoking companion skills that perform such actions. Existing authorization governs implementation and experiment actions; do not ask again for actions already authorized.
1. Map the changed callback call graph, lifecycle, shared storage, and host-facing transitions.
1. Read the [essential checklist](./references/essential/checklist.md), then select the detailed references that answer the remaining questions.
1. Record protocol assumptions, source and toolchain scope, capacity and work bounds, and failure policies.
1. For authorized implementation or experiments, use an instrument and a positive control suited to the claim. For a review, distinguish observed evidence from proposed checks.
```

## choose-audio-dsp-architecture (2238-audio-dsp-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/audio-dsp-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2238-audio-dsp-engineering/8508-choose-audio-dsp-architecture
- الوصف: Pick the right audio-DSP architecture for a described product by traversing the audio-DSP architecture decision tree (latency tolerance → processing model → time-vs-frequency domain → fixed-vs-float + denormals → platform/plugin format + audio I/O), then return the recommended processing model, latency & buffer-size budget, sample rate/bit depth, numeric strategy, algorithm approach (IIR/FIR/FFT-S

```markdown
# Skill: choose-audio-dsp-architecture

> **Invoked by:** `audio-dsp-architect` (primary). Also consulted by `dsp-implementation-engineer` when a build reveals the chosen architecture can't meet the latency/CPU budget.
>
> **When to invoke:** "block or sample-by-sample?"; "what latency / buffer size can we afford?"; "JUCE + VST3/AU/CLAP or Web Audio AudioWorklet?"; "fixed-point or floating-point?"; "IIR biquad vs FIR vs FFT/STFT for this effect?"; any "what audio-DSP architecture should we use?" question.
>
> **Output:** the processing model + latency/buffer budget + sample rate/bit depth + numeric strategy (fixed vs float + denormals) + algorithm approach + framework/plugin-format/audio-I/O + the 1-2 flip conditions.

## Procedure

1. **Restate the situation in the tree's terms.** Capture: the **use case** (live monitoring / mixing / mastering / game engine / embedded pedal / browser), the **latency tolerance** (single-digit ms for monitoring, tens of ms OK for mastering), the **platform** (desktop DAW, iOS/AUv3, web, an ARM DSP), the **signal** (mono/stereo/multichannel/ambisonic + sample rate), and the **CPU/power budget**.
2. **Set the latency budget first — it drives the processing model.** Ultra-low latency → small buffers, no lookahead, and sample-by-sample only where a tight feedback loop demands it; relaxed latency → block + lookahead (linear-phase FIR, large FFT) is allowed. Everything downstream is spent from this budget.
3. **Choose the domain from the effect.** Resonant EQ / filter / dynamics / delay → **time-domain** (IIR biquad or FIR); a spectral operation (linear-phase EQ, spectral gate, convolution reverb, pitch/time-stretch) → **frequency-domain** (FFT/STFT + overlap-add). For frequency-domain, pick the FFT size & hop for the resolution/latency you can afford.
4. **Traverse the decision tree** in [`../../knowledge/audio-dsp-decision-tree.md`](../../knowledge/audio-dsp-decision-tree.md) against those inputs:
   - ultra-low latency + tight feedback → **sample-by-sample**; otherwise → **block/buffer**; relaxed → **block + lookahead**,
   - minimum-phase cheap filter → **IIR biquad**; linear-phase / exact IR → **FIR / partitioned convolution**; spectral → **FFT/STFT overlap-add**,
   - any nonlinearity → wrap it in **oversampling** (2–8x) with band-limiting up/down filters,
   - target has an FPU → **32-bit float** (+ flush-to-zero); FPU-less/power-constrained → **fixed-point Q-format** (+ CMSIS-DSP),
   - desktop plugin → **JUCE/iPlug2** (VST3/AU/AAX/CLAP); browser → **Web Audio AudioWorklet**; iOS → **AUv3**; Linux pro-audio → **LV2/CLAP + JACK**; embedded → **bare-metal/RTOS + I2S**.
```

## implement-and-optimize-realtime-audio (2238-audio-dsp-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/audio-dsp-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2238-audio-dsp-engineering/8510-implement-and-optimize-realtime-audio
- الوصف: Implement a DSP stage as real-time-safe code in the audio callback (no locks, no allocation, no syscalls, no unbounded work — everything pre-allocated at prepare time), handle denormals with flush-to-zero, pass parameters lock-free (atomic / SPSC FIFO) with per-sample smoothing, then optimize the profiled hot loop with SIMD (SSE/AVX/NEON/CMSIS-DSP) and verify with objective measurement (null test,

```markdown
# Skill: implement-and-optimize-realtime-audio

> **Invoked by:** `dsp-implementation-engineer` (primary). Also consulted by `audio-dsp-architect` to sanity-check that a chosen architecture is real-time-safe and implementable.
>
> **When to invoke:** "Write the real-time-safe `processBlock` for <effect>"; "optimize this DSP hot loop (SIMD/denormals)"; "pass parameters from the UI thread without a data race or a click"; "null-test / measure THD+N / plot the frequency response"; any move from a spec to running, measured DSP code.
>
> **Output:** real-time-safe DSP code (or an optimization/measurement) with the callback invariants held, denormals handled, lock-free parameters + smoothing, SIMD where profiling justifies it, and objective pass/fail measurements.

## Procedure

1. **Hold the callback real-time-safety invariant first.** Before any effect logic, confirm the plan has **no lock, no heap allocation, no syscall/file/log I/O, no unbounded work** inside the audio callback (`processBlock` / `AudioWorkletProcessor.process`). Everything is **pre-allocated at `prepareToPlay(sampleRate, blockSize)`** — delay lines, FFT scratch, smoothing state, ring buffers. See the contract in [`../../knowledge/audio-dsp-patterns-2026.md`](../../knowledge/audio-dsp-patterns-2026.md).
2. **Implement the DSP from the right primitive.** Biquad (Direct Form II transposed) for IIR; FIR / partitioned convolution for linear-phase/IR; FFT + windowed (Hann/COLA) overlap-add for spectral; ring-buffer delay lines for time effects. Size all state at prepare time; wrap ring buffers without allocating.
3. **Kill denormals.** Set **flush-to-zero / denormals-are-zero** on the audio thread (once per callback entry), or inject a tiny DC/dither into feedback paths, so decaying tails don't 10–100x the CPU.
4. **Pass parameters lock-free with smoothing.** UI/message thread → audio thread via `std::atomic<float>` (scalars) or a **lock-free SPSC FIFO** (events) — never a mutex the audio thread can block on. **Smooth every audio-path parameter per-sample** (one-pole ramp) so a slider move doesn't zipper; never read a raw UI value in the loop.
5. **Profile before you optimize.** Measure the actual hot loop as a fraction of the buffer deadline. Process in blocks for cache locality. Only then **vectorize** the bottleneck with SIMD (SSE/AVX on x86, **NEON** on ARM, **CMSIS-DSP** on Cortex-M) — mind alignment and the scalar remainder. Often the biggest real win is just fixing denormals (step 3).
```

## interview-me (3225-interview-me)

- الترخيص: **MIT**  ·  الأصل: https://github.com/ulebule/claude-skills/tree/cb320c21990e92391f5e0bf4207a150515d1ff19/plugins/interview-me
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3225-interview-me/13638-interview-me
- الوصف: Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time interview until ~95% confidence about the underlying intent. Use when an ask is underspecified ("build me X" without "for whom" or "why now"), when the user explicitly invokes ("interview me", "grill me", "are we sure?", "stress-test my thinking"), or when you catch yours

```markdown
# Interview Me

## Overview

What people ask for and what they actually want are different things. They ask for "a dashboard" because that's what one asks for, not because a dashboard solves their problem. They say "make it faster" without a number to hit.

The cheapest moment to find this gap is before any plan, spec, or code exists. Once you've started building, switching costs are real, and the user will rationalize the wrong thing into a "good enough" thing. The misfit gets locked in.

This skill closes the gap before it costs anything. The other Define-phase skills assume you already know roughly what you want: `idea-refine` generates variations from an idea, `spec-driven-development` writes the requirements down, `doubt-driven-development` stress-tests a plan after you've drafted one. Interview-me is the part before all of those, where you ask one question at a time, with your best guess attached, until you can predict what the user is going to say before they say it.

## When to Use

Apply this skill when:

- The ask is missing at least one of: **who** the user is, **why** they want it, what **success** looks like, what the binding **constraint** is
- The request is conventional rather than specific ("build me X", "make it faster") and you can't unpack the convention without guessing
- You're tempted to start with assumptions you haven't surfaced
- The user hasn't said which value they're optimizing for when two reasonable ones are in tension (simplicity vs. flexibility, cost vs. speed)
- The user explicitly invokes: "interview me", "grill me", "before we start, are we sure?", "stress-test my thinking"

**When NOT to use:**

- The ask is unambiguous and self-contained ("rename this variable", "fix this typo")
- The user has explicitly asked for speed over verification
- Pure information requests ("how does X work?", "what does this code do?")
- Mechanical operations (renames, formats, file moves)
- You already have ≥95% confidence; re-read the stop condition below before assuming you don't

## Loading Constraints

This skill needs a live, responsive user. **Do not invoke in non-interactive contexts** like CI pipelines, scheduled runs, `/loop`, or autonomous-loop. If you're in one of those and the ask is underspecified, flag that as a blocker for the user instead of guessing.

## The Process

### Step 1: Hypothesize, with a confidence number

Before asking anything, write down your current best read of what the user wants in **one sentence**, plus an honest confidence number (0–100%):

```
HYPOTHESIS: You want a way to answer "how are we doing?" in standup, and "dashboard" was the convention that came to mind.
CONFIDENCE: ~30% — missing: who it's for, what "metrics" means in context, and what success looks like
```
```
