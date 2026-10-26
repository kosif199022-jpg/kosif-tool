# مصادر «التعليق الصوتي وإخراج TTS» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## elevenlabs-core-workflow-a (1847-elevenlabs-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/elevenlabs-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a
- الوصف: Implement ElevenLabs text-to-speech and voice cloning workflows. Use when building TTS features, cloning voices from audio samples, streaming speech to a chatbot, or implementing the primary ElevenLabs money-path: voice generation. Trigger with "elevenlabs TTS", "text to speech", "voice cloning elevenlabs", "clone a voice", "generate speech", "elevenlabs voice".

```markdown
# ElevenLabs Core Workflow A — TTS & Voice Cloning

## Overview

The primary ElevenLabs workflows: (1) Text-to-Speech with voice settings, (2) Instant Voice Cloning from audio samples, (3) streaming TTS via WebSocket for real-time applications, and (4) voice-library management. This SKILL.md walks the full flow at a high level and carries the first TTS example inline; the deep code for cloning, streaming, and management lives in [the full implementation walkthrough](references/implementation.md).

## Prerequisites

- Completed `elevenlabs-install-auth` setup
- Valid API key with sufficient character quota
- For voice cloning: audio recording(s) of the target voice (min 30 seconds, clean audio)

## Instructions

### Step 1: Advanced Text-to-Speech

Instantiate the client, call `textToSpeech.convert(voiceId, opts)`, and pipe the returned stream to a file. The `voice_settings` block is where you tune delivery:

```typescript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createWriteStream } from "fs";
import { Readable } from "stream";
import { pipeline } from "stream/promises";

const client = new ElevenLabsClient();

async function generateSpeech(
  text: string,
  voiceId: string,
  outputPath: string
) {
  const audio = await client.textToSpeech.convert(voiceId, {
    text,
    model_id: "eleven_multilingual_v2",
    voice_settings: {
      stability: 0.5,          // Lower = more expressive, higher = more consistent
      similarity_boost: 0.75,  // How closely to match the original voice
      style: 0.3,              // Amplify the speaker's style (adds latency if > 0)
      speed: 1.0,              // 0.7 to 1.2 range
    },
    // Optional: enforce language for multilingual model
    // language_code: "en",    // ISO 639-1
  });

  await pipeline(Readable.fromWeb(audio as any), createWriteStream(outputPath));
  console.log(`Generated: ${outputPath}`);
}

await generateSpeech("Welcome to our platform.", "21m00Tcm4TlvDq8ikWAM", "stable.mp3");
```

### Step 2: Instant Voice Cloning (IVC)

Clone a voice from 1-25 audio samples with `client.voices.add({ name, description, files })`, which returns a `voice_id` you can use immediately in `textToSpeech.convert`. Use `similarity_boost: 0.85` on cloned voices to stay close to the original. Full `cloneVoice` implementation: [implementation.md](references/implementation.md), Step 2.

### Step 3: WebSocket Streaming TTS
```

## elevenlabs-hello-world (1847-elevenlabs-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/elevenlabs-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1847-elevenlabs-pack/5519-elevenlabs-hello-world
- الوصف: Generate your first ElevenLabs text-to-speech audio file. Use when starting a new ElevenLabs integration, testing your setup, or learning basic TTS API patterns before wiring voice into a real app. Trigger with "elevenlabs hello world", "elevenlabs example", "elevenlabs quick start", "first elevenlabs TTS", "text to speech demo".

```markdown
# ElevenLabs Hello World

## Overview

Generate speech from text using the ElevenLabs TTS API. This skill covers the
core `POST /v1/text-to-speech/<voice-id>` endpoint with real voice IDs, model
selection, and audio output. Start from the minimal SDK call below, then drill
into [the full implementation](references/implementation.md) for the cURL,
streaming, and multi-language paths.

## Prerequisites

- Completed the `elevenlabs-install-auth` setup skill so the SDK is installed.
- A valid API key exported as `ELEVENLABS_API_KEY` in your shell environment.
- Node 20+ (for the TypeScript SDK path) or Python 3.9+ (for the Python path).

## Instructions

The whole workflow is one API call: pick a voice ID, pick a model, send text,
write the returned audio stream to a file. The minimal TypeScript path:

```typescript
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { createWriteStream } from "fs";
import { Readable } from "stream";
import { pipeline } from "stream/promises";

const client = new ElevenLabsClient();
const audio = await client.textToSpeech.convert("21m00Tcm4TlvDq8ikWAM", {
  text: "Hello! This is your first ElevenLabs text-to-speech generation.",
  model_id: "eleven_multilingual_v2",
});
await pipeline(Readable.fromWeb(audio as any), createWriteStream("output.mp3"));
```

The four generation paths, with full copy-paste code and inline commentary on
every `voice_settings` field, live in
[references/implementation.md](references/implementation.md):

1. **SDK (TypeScript / Python)** — batch generation with tuned voice settings.
2. **cURL** — the raw REST call, no SDK, for shell scripts and testing.
3. **Streaming** — the `eleven_flash_v2_5` low-latency path (~75 ms first chunk).
4. **Model / voice / output-format tables** — the exact IDs to plug in above.

Pick the path that matches your stack, swap the voice ID and text, and run it.

## Output

A single audio file written to disk (default `output.mp3`), plus a console line
confirming the write:

- `output.mp3` — MP3 at `mp3_44100_128` by default (~35–50 KB for a one-line
  greeting). Override the codec via `output_format` (see the output-format table
  in [implementation.md](references/implementation.md)).
- stdout: `Audio saved to output.mp3` (or `Streamed audio saved to
  streamed.mp3` on the streaming path).

A non-200 response returns a JSON error body instead of audio — see Error
Handling below.

## Error Handling

| Error | HTTP | Cause | Solution |
|-------|------|-------|----------|
| `voice_not_found` | 404 | Invalid voice ID | Use `GET /v1/voices` to list valid IDs |
| `invalid_api_key` | 401 | Bad or missing key | Check `ELEVENLABS_API_KEY` env var |
| `model_not_found` | 400 | Wrong model_id string | Use exact IDs from the models table |
```

## speech-recognition-and-synthesis (2261-conversational-ai-voice-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/conversational-ai-voice-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2261-conversational-ai-voice-engineering/8616-speech-recognition-and-synthesis
- الوصف: Engineer the ASR and TTS layer of a voice agent: choose STT/TTS providers on the channel (narrowband telephony vs wideband web), languages, streaming support, WER, and cost; stream transcription and synthesis to cut latency; tune VAD/endpointing; handle diarization, prosody/SSML, codecs & sample rates, and noise robustness; and measure WER on real audio. Provider/version specifics verify-at-use.

```markdown
# Speech Recognition & Synthesis

The ears and the mouth of the voice agent. A wrong transcript poisons every downstream turn, and endpointing that's mistuned either cuts the user off or adds a dead pause — so ASR/TTS engineering is where the agent feels sharp or sluggish. Build for the channel's real audio and measure on real calls.

> **Engineering judgment, provider landscape is volatile.** ASR/TTS model versions, prices, WER claims, and streaming/feature support change with every release. Every provider/version specific here is `[verify-at-use]` — confirm against the vendor docs before it drives a commitment. No PII; call audio and transcripts are sensitive — don't store them beyond task need.

## Workflow

1. **Match ASR/TTS to the channel and latency budget.** Narrowband telephony (8 kHz) vs wideband web (16 kHz+) change which models perform; take the per-hop budget from `voice-agent-architecture-and-latency`.
2. **Stream everything.** Streaming (interim) transcription and streaming TTS (start speaking on the first LLM token) are the biggest latency wins — batch calls are latency you chose to pay.
3. **Tune VAD/endpointing as a first-class problem.** Energy-based VAD, semantic endpointing, silence thresholds, and minimum-speech duration decide when the agent responds; set measurable targets and coordinate barge-in gating with the dialog layer.
4. **Handle real audio.** Noise suppression, codec/sample-rate handling (µ-law/Opus/PCM), custom vocabulary/phrase biasing (names, SKUs, jargon), diarization for multi-party — this is what keeps WER usable in the field.
5. **Shape the voice.** Voice/model choice, prosody and SSML (pacing, emphasis, pronunciation), and consistent audio format make the agent sound intentional without blowing TTS time-to-first-byte.
6. **Measure WER on representative audio.** Score WER and latency on real calls across accents, noise, and channels — not a clean demo clip.

## Metrics table

| Metric | What it tells you | Flag |
|---|---|---|
| WER on representative real audio | Recognition quality that poisons/serves downstream | `[verify-at-use]` |
| Endpoint latency (silence -> final) | How responsive vs cutting-off the agent is | `[ESTIMATE]` `[verify-at-use]` |
| STT interim/final streaming latency | Latency hidden vs paid | `[verify-at-use]` per provider |
| TTS time-to-first-byte | First-audio latency | `[verify-at-use]` per provider |
| Sample rate / codec (channel) | Which models perform on this audio | `[verify-at-use]` |

## Anti-patterns

- Benchmarking on clean studio audio, then shipping onto 8 kHz noisy phone calls.
- Using batch STT/TTS when streaming is available, and paying the latency.
- Tuning endpointing to a single silence threshold instead of the conversation's feel.
```

## voice-agent-architecture-and-latency (2261-conversational-ai-voice-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/conversational-ai-voice-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2261-conversational-ai-voice-engineering/8618-voice-agent-architecture-and-latency
- الوصف: Choose the voice-agent pipeline shape (cascade STT->LLM->TTS vs speech-to-speech), the channel (telephony / web / SDK), and the build-vs-platform bet (Twilio / Vapi / Retell / LiveKit / Pipecat), then allocate the end-to-end latency budget per hop and design the turn-taking / barge-in / fallback model. Model/platform/latency specifics verify-at-use.

```markdown
# Voice-Agent Architecture & Latency

The first and most expensive voice-AI decision: what pipeline shape you build, on what platform, over what channel — and the latency budget it all has to live inside. Everything downstream — the ASR/TTS latency the pipeline engineer must hold, the turn-taking the dialog engineer can build — is fixed by this choice, so make it deliberately. In voice, latency is the product.

> **Engineering judgment, landscape is volatile.** Model versions, platform features, and provider prices change with every release. Every model/platform/latency specific here is `[verify-at-use]` — confirm against the vendor/provider docs before it drives a build commitment. No PII; call audio/transcripts are sensitive.

## Workflow

1. **State the use-case, channel, and acceptable response latency.** Inbound support, outbound reminders, in-app assistant, and IVR replacement have different latency, control, and telephony needs.
2. **Choose cascade vs speech-to-speech on the use-case.** Cascade (STT -> LLM -> TTS) buys transcripts, swappable components, and mid-turn tool calling; speech-to-speech buys latency and prosody at the cost of control/observability. Name the trade.
3. **Pick the channel.** Telephony (SIP/PSTN, 8 kHz narrowband, DTMF), WebRTC (browser/app, wideband), or SDK — the channel fixes the media constraints and part of the latency.
4. **Decide build-vs-platform.** Managed platform (Vapi/Retell) for speed, framework (LiveKit/Pipecat) for control, telephony primitives (Twilio) + your orchestration, or from scratch. Isolate the provider behind seams.
5. **Allocate the end-to-end latency budget per hop.** VAD/endpointing + STT final + LLM TTFT + TTS TTFB + network must sum under the target (conversational feel wants sub-second first audio, `[verify-at-use]`). Hand the per-hop targets to `speech-recognition-and-synthesis`.
6. **Design turn-taking, barge-in, and fallback in.** Endpointing, interruption, and the unhappy path (silence, ASR error, LLM stall, human handoff) are architecture, not later tickets.

## Metrics table

| Decision input | What it tells you | Flag |
|---|---|---|
| Target end-to-end response latency (ms) | The budget every hop shares | `[verify-at-use]` |
| Need for transcripts / mid-call tools | Cascade vs speech-to-speech | `[verify-at-use]` |
| Channel (phone / web / app / SDK) | Media constraints + transport latency | `[verify-at-use]` per channel |
| Control-vs-speed priority | Build-vs-platform bet | `[verify-at-use]` platform features |
| Barge-in / interruption requirement | Turn-taking model complexity | n/a |

## Anti-patterns

- Choosing speech-to-speech for its "naturalness" when the use-case needs mid-call tool calling and transcripts.
```

## twilio-voice-conversation-relay (2721-twilio-developer-kit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/twilio-developer-kit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2721-twilio-developer-kit/10514-twilio-voice-conversation-relay
- الوصف: Build AI-powered voice agents using Twilio ConversationRelay. Handles real-time speech recognition (ASR), text-to-speech (TTS), and bidirectional audio streaming via WebSocket. Covers TwiML setup, WebSocket message types, LLM integration, streaming responses, and voice provider configuration. Use this skill to build voice bots, IVR replacements, or real-time AI voice assistants on Twilio calls.

```markdown
## Overview

ConversationRelay connects Twilio's telephony layer to your app via a persistent WebSocket. Twilio handles ASR (speech-to-text) and TTS (text-to-speech); your app receives transcripts, calls an LLM, and sends text back for playback.

```
Caller ←→ Twilio (ASR/TTS) ←→ WebSocket ←→ Your App ←→ LLM
```

---

## Prerequisites

- Upgraded Twilio account with ConversationRelay access (requires onboarding)
  — New to Twilio? See `twilio-account-setup`
  — Start onboarding at: [Console > Voice > ConversationRelay](https://console.twilio.com/us1/voice/conversation-relay) — access is **not** instant
- A voice-capable Twilio phone number
- `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` — see `twilio-iam-auth-setup`
- WebSocket server reachable via `wss://` (TLS required)
- An LLM integration (OpenAI, Anthropic, etc.)
- For placing calls: see `twilio-voice-outbound-calls`

**Onboarding:** Complete via Console > Voice > ConversationRelay > Onboarding. Select TTS/ASR providers:
- **TTS:** Deepgram, Amazon Polly, Google Cloud TTS, ElevenLabs
- **ASR:** Deepgram, Google Cloud STT

---

## Quickstart

**Step 1 — Return TwiML pointing to your WebSocket server**

**Python (Flask)**
```python
from flask import Flask
from twilio.twiml.voice_response import VoiceResponse, Connect, ConversationRelay

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    connect = Connect()
    connect.conversation_relay(
        url="wss://yourapp.com/ws/voice",
        welcome_greeting="Hello! How can I help you today?"
    )
    response.append(connect)
    return str(response)
```

**Node.js (Express)**
```node
const { VoiceResponse } = require("twilio").twiml;

app.post("/voice", (req, res) => {
    const response = new VoiceResponse();
    const connect = response.connect();
    connect.conversationRelay({
        url: "wss://yourapp.com/ws/voice",
        welcomeGreeting: "Hello! How can I help you today?",
    });
    res.type("text/xml").send(response.toString());
});
```

**Step 2 — Handle WebSocket events and respond with text**

**Python (websockets)**
```python
import asyncio, json, websockets

async def handle_call(websocket):
    async for message in websocket:
        event = json.loads(message)
        if event["type"] == "prompt":
            ai_response = await call_llm(event["voicePrompt"])
            await websocket.send(json.dumps({"type": "text", "token": ai_response, "last": True}))

async def main():
    async with websockets.serve(handle_call, "0.0.0.0", 8080):
        await asyncio.Future()

asyncio.run(main())
```

**Node.js (ws)**
```node
const WebSocket = require("ws");
const wss = new WebSocket.Server({ port: 8080 });

wss.on("connection", (ws) => {
    ws.on("message", async (data) => {
```

## human-voice (2029-voice)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jrichlen/agent-plugins/tree/013353ad6ae0efb71384e0e14a0196b1be1884f6/plugins/voice
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2029-voice/7199-human-voice
- الوصف: Style for prose a human reads — answers, recommendations, explanations, research summaries, comparisons. Use on every conversational reply that contains prose for a person to read: triage intent, lead with the verdict, keep it scannable, tag claim confidence. Reach for it whenever answering a technical question, comparing options, or making a recommendation, even when the user says nothing about s

```markdown
# Human Voice

Prose a human reads. Everything `machine-voice`'s list does not name.

## Invariant

**ALWAYS** put the verdict first, and let no load-bearing claim survive
unverified without being marked. **NEVER** invoke `second-opinion` unprompted —
offer it and wait.

"Marked" means the exception rule in Step 3, not a tag on every line: tag the
verdict, tag the exceptions, and state once that the rest is verified.

## The partition

The split is **per output element, not per response**. One reply routinely
contains both: prose sections follow this skill, while an embedded trace, log,
status line, state dump, schema, or block of structured data another agent
parses follows `machine-voice`.

- Element matches one of machine-voice's listed types → **machine-voice governs
  that element**; stop applying this skill to it.
- Every other element → **this skill**.

**Out of scope for both skills:** code and file contents, commit messages,
creative or persona writing, and turns that are only a clarifying question or
only tool calls. Ship those unstyled — skip Steps 2–4 and the self-check.

**Out of scope wins over machine-voice's list.** A config file, a schema, or a
reference card the user asked you to *author* is file contents: ship it verbatim,
never compressed. `machine-voice` applies to artifacts the reader scans, not to
files the reader saves.

**An element serving surrounding prose stays here.** A comparison table inside a
recommendation is the explanation's evidence, not a standalone reference card —
it takes this skill's confidence tags, never machine-voice's status glyphs.

**`ai-writing-mistakes` is a pass, not a fourth voice.** It never claims an
element and never competes with this partition: this skill decides layout,
ordering, and tags; that one decides wording inside whatever this one placed.
Run it over every element this skill governs, and over prose you were asked to
author into a file — those are exempt from layout, not from being written well.

## Step 1 — Intent triage

Classify before writing. Spend seconds, not paragraphs. **Never emit any text
about the classification** — no "This looks like a decision-support question."

| Intent | Signal | Layout and obligations |
|---|---|---|
| **Quick fact** | One verifiable answer exists | 1–3 sentences + confidence tag. No key-facts layer, no depth offer. |
| **Decision support** | "Should I / which / vs / recommend" | Full layered layout below. |
| **Exploration** | "What's out there / examples / options" | Ranked shortlist first, then a verdict if one earns it. |
| **Execution** | "Do X / build / fix / write" | Do the work. Summary ≤3 lines + confidence tag; depth offer optional. |
| **Ambiguous** | Two+ intents fit and the layouts differ | Ask — don't guess. |
```
