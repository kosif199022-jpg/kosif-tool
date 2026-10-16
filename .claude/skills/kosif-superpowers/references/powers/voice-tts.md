# الصوت المولّد والتعليق — Voice & TTS

> **قوتك هنا:** أنت تكتب التعليق للأذن، توجّه أداءه، تولّده بالعربية **دون مفتاح** على هذا الجهاز، تقيس طوله وتستخرج توقيت كل كلمة، ثم تبني الحركة على صوته وتسلّمه عند −14 LUFS. الصوت هو ساعة الفيلم، وأنت من يضبطها.
> **أقوى دليل:** سلسلة كاملة جرت في هذه الحاوية (2026-10-16): Piper `ar_JO-kareem` → WAV عربي 7.43 ث (−16.5 LUFS) → faster-whisper → `words.json` بعشر كلمات عبر `kosif-tool/tools/words_convert.py` → فيديو 1080x1920 مرّ `kosif-tool/tools/verify_video.py` بـ 11/11. وفي الفيديوهات: `style:doodle` (حكاية بالفصحى، كلمة-بكلمة مع الصوت) و`style:pm-1stnoel-c20a89` (قراءة صوتية بتظليل الكلمة).
> **You can:** write, direct, synthesise, align, process and ship narration in Arabic first. **55 powers follow** — ✅ 12 · 🟢 6 · 📦 1 · 🔑 13 · 👁 5 · 📄 18 · 💡 0.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`)؛ «run here» = تشغيل فعلي في هذه الحاوية مع رقم مقاس.

**فحص سريع لهذه الحاوية (2026-10-16):** ffmpeg 6.1.1 ✔ (loudnorm, sidechaincompress, afftdn, deesser) · `pip install piper-tts` ✔ + صوت عربي من huggingface.co ✔ · `pip install faster-whisper` ✔ (مرّر مصفوفة numpy لا مسارًا) · Kokoro بلا صوت عربي · edge-tts: الخادم ردّ 400 · `@hyperframes/cli` غير موجود على npm · ElevenLabs / Gemini / HeyGen / OpenAI تحتاج مفاتيح · voice.py (نايف) يعمل على ويندوز فقط.

**اختيار المحرك في 10 ثوانٍ / engine pick:**

| الحاجة / need | هنا الآن / here now | على جهاز المالك / owner PC | بمفتاح / with key |
|---|---|---|---|
| تعليق عربي فصيح | Piper ar_JO-kareem (VOICE-01) | Naayf ar-SA (VOICE-02) | ElevenLabs v2/v3 (VOICE-06) |
| عامية مصرية معبّرة | — (Piper فصيح فقط) | — | Gemini + persona (VOICE-11, VOICE-26) |
| إنجليزي | Kokoro af_heart (VOICE-03) | Windows David/Zira | ElevenLabs / HeyGen |
| توقيت الكلمات | faster-whisper (VOICE-32) | transcribe.py | HeyGen Starfish (VOICE-14) |
| حوار بعدة أصوات | — | — | Gemini dialogue (VOICE-13) |

## الفهرس / contents
- **محركات الصوت المحلية بلا مفتاح — Local voice engines (no key)** — VOICE-01 … VOICE-05 (5)
- **الأصوات السحابية والاستنساخ — Cloud voices & cloning** — VOICE-06 … VOICE-17 (12)
- **كتابة التعليق وإخراجه — Script writing & voice direction** — VOICE-18 … VOICE-30 (13)
- **الصوت ساعةُ الفيلم — Voice-led timing & sync** — VOICE-31 … VOICE-38 (8)
- **معالجة الصوت ومزجه — Voice processing & mix** — VOICE-39 … VOICE-45 (7)
- **الصوت التفاعلي وواجهاته — Interactive voice & voice UI** — VOICE-46 … VOICE-52 (7)
- **الأخلاق والتكلفة — Ethics, rights & cost** — VOICE-53 … VOICE-55 (3)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## محركات الصوت المحلية بلا مفتاح — Local voice engines (no key)

_ما يعمل على الجهاز نفسه: صفر تكلفة، صفر رفع للنص، ويمكن إعادة توليده مئة مرة أثناء ضبط الإيقاع._

#### VOICE-01 · تعليق عربي محلي بـ Piper · Piper offline Arabic TTS · ✅ مُثبت هنا / proven here
- **ماذا / what:** تحوّل نصًا عربيًا إلى WAV على المعالج دون إنترنت ودون مفتاح، بصوت ar_JO-kareem. — Synthesises Arabic narration on CPU, offline and keyless, with the ar_JO-kareem voice.
- **متى أستخدمها / when:** مسودات التعليق، الأنيماتك، وأي فيلم عربي حين لا يوجد مفتاح مدفوع — drafts, animatics, any keyless Arabic film.
- **كيف / how:** Install piper-tts in a venv, download the voice model (.onnx + .onnx.json) from huggingface.co/rhasspy/piper-voices (ar/ar_JO/kareem/medium, 63 MB), pipe the text in. Output is 22.05 kHz mono; resample to 48 kHz and loudnorm before muxing (VOICE-44). One sentence per line so --sentence-silence places breaths. Ran here: a 10-word Arabic line → 7.43 s WAV at -16.5 LUFS integrated; with --length-scale 1.15 and --sentence-silence 0.35 two sentences → 7.13 s. **أرقام / params:** voice ar_JO-kareem-medium (1 speaker, 22050 Hz); inference noise_scale 0.667, noise_w 0.8, length_scale 1.0 (1.1–1.2 = slower, calmer); --sentence-silence 0.2–0.5 s; --volume 1.0.

```bash
printf 'الجملة الأولى قصيرة.\nوالثانية أطول قليلًا.\n' \
 | .venv/bin/piper -m ar_JO-kareem-medium.onnx -f vo.wav \
     --length-scale 1.1 --sentence-silence 0.35
ffmpeg -i vo.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -ac 2 vo48.wav
```

- **الدليل / proof:** `run here 2026-10-16: piper-tts 1.8.0 → ar.wav 7.43 s, -16.5 LUFS` · `probe.md: piper-tts 1.8.0 installable, huggingface.co reachable`
- **تثبيت / install:** `python3 -m venv .venv && .venv/bin/pip install piper-tts && curl -L -O https://huggingface.co/rhasspy/piper-voices/resolve/main/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx{,.json}`
- **رخصة / license:** piper-tts is GPL-3.0-or-later (call it as a CLI, do not vendor its code); the kareem dataset licence is 'see URL' on the model card — check before commercial delivery.

#### VOICE-02 · صوت ويندوز العربي (نايف) بالجدول الزمني · Windows OneCore Arabic narration (Naayf) · 📄 موصوف / documented only
- **ماذا / what:** سكربت المالك voice.py ينطق النص بأصوات ويندوز المثبتة (Microsoft Naayf ar-SA) ويُخرج مسارًا واحدًا وتوقيت كل سطر. — Owner script voice.py speaks a timed script with installed Windows voices (Microsoft Naayf ar-SA) and writes one track plus per-line timings.
- **متى أستخدمها / when:** على حاسوب المالك (ويندوز) حين يريد صوتًا عربيًا دون إنترنت — on the owner's Windows PC.
- **كيف / how:** PowerShell + SSML prosody under the hood. `python voice.py --list`; `voice.py out.wav --text '…' --voice Naayf --rate -5%`; or `--script lines.json [--seconds 15]` → out.wav + out.json [{t,end,text}] for captions and ducking. Trims silence (|x|>0.004) keeping 20 ms head / 80 ms tail, resamples to 48 kHz stereo, peak 0.89. In a composition mark it `<audio data-role="voice">` so the mux ducks other clips and normalises to -14 LUFS. The Basma editor calls the same voices through the local bridge (GET /api/voices, POST /api/voice {lines:[{t,text}],voice:'Naayf',seconds}). Owner code, but it needs powershell.exe + OneCore → it does NOT run in this Linux container; use VOICE-01 here. **أرقام / params:** default rate −4 % (CLI examples −5 %), pitch +0 %; 48 kHz stereo; peak 0.89; head 20 ms / tail 80 ms.
- **الدليل / proof:** `kosif-studio/motion/voice.py:82` · `kosif-one/tools/kosif-studio/motion/voice.py` · `100-superskills/skills/kosif-montage-motion/scripts/voice.py` · `app/public/js/00_editor.js:2638`

#### VOICE-03 · Kokoro المحلي (بلا عربية) · Kokoro local TTS (no Arabic voice) · 📦 بأمر تثبيت / one install
- **ماذا / what:** محرك محلي مجاني بـ 54 صوتًا في 8 لغات؛ أول حرف من معرّف الصوت يحدد اللغة — ولا صوت عربي فيه. — Free CPU TTS with 54 voices in 8 languages; the voice-id prefix encodes language — no Arabic voice.
- **متى أستخدمها / when:** للنسخة الإنجليزية من فيلم ثنائي اللغة أو تعليق إنجليزي سريع — the English cut of a bilingual film.
- **كيف / how:** Prefixes a/b/e/f/h/i/j/p/z = en-US/en-GB/es/fr/hi/it/ja/pt-BR/zh; good voices af_heart, af_nova, am_adam, bf_emma. Python: `pip install kokoro soundfile` (~311 MB model from huggingface.co; non-English needs espeak-ng, not installed here). JS: `npm i kokoro-js` (1.2.1). The HyperFrames wrapper `npx hyperframes tts` is NOT installable here (@hyperframes/cli 404 on npm). **أرقام / params:** speed 0.7–0.8 tutorial · 1.0 natural · 1.1–1.2 upbeat; 24 kHz output.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/tts.md` · `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/brag/skills/brag/SKILL.md` · `probe.md: kokoro 0.7.16, kokoro-js 1.2.1`
- **تثبيت / install:** `pip install kokoro soundfile   # or: npm i kokoro-js`

#### VOICE-04 · نطق المتصفح العربي ar-SA · Browser Web Speech fallback (ar-SA) · 🟢 جاهز / ready
- **ماذا / what:** حين لا توجد جلسة صوتية، يقرأ التطبيق الرد بصوت الجهاز العربي عبر Web Speech API. — With no live session, the app reads replies aloud with the device's Arabic voice via the Web Speech API.
- **متى أستخدمها / when:** واجهات تفاعلية ومعاينات داخل المتصفح، لا للتسليم النهائي — interactive UI and previews, never final delivery.
- **كيف / how:** Strip bullets/asterisks first (`text.replace(/[•*]/g,'')`), `speechSynthesis.cancel()` then speak a `SpeechSynthesisUtterance` with `lang='ar-SA'`; onstart/onend toggle the speaking state (drives VOICE-49). Voice quality depends on the viewer's OS and is not capturable by a headless render — never use it for an MP4. **أرقام / params:** lang ar-SA; default rate/pitch (owner code sets none).

```js
function speakAr(text, onState) {
  const u = new SpeechSynthesisUtterance(text.replace(/[•*]/g, ''));
  u.lang = 'ar-SA';
  u.onstart = () => onState('speaking');
  u.onend = () => onState('idle');
  speechSynthesis.cancel();
  speechSynthesis.speak(u);
}
```

- **الدليل / proof:** `kosif-audit-studio/voice.js:380` · `kosif-earth-ci-fork/ui/features/assistant.js:281`

#### VOICE-05 · أصوات Edge العصبية والمولدات المبنية عليها · Edge neural voices & scene-file generators · 📄 موصوف / documented only
- **ماذا / what:** مولدات تحول ملف مشاهد (YAML أو JSON) إلى فيديو مروي بأصوات Edge مع ترجمة تلقائية، وفي Edge أصوات عربية مصرية وسعودية. — Generators that turn a scenes file (YAML or JSON) into a narrated MP4 with Edge neural voices and auto subtitles; Edge has ar-EG and ar-SA voices.
- **متى أستخدمها / when:** على جهاز متصل حين يُقبل صوت Edge — on a connected machine where an Edge voice is acceptable.
- **كيف / how:** video-guide-creator: YAML (title-card, bullet-points, outro or screencast steps with CSS selectors) → Docker → MP4; brand presets hold colours, voice, language, logo (default en-US-AriaNeural — switch to an ar-* voice). framecraft: scenes.json → Playwright frames → Edge TTS → FFmpeg 1920x1080 with --auto-duration. Here: `pip install edge-tts` works but speech.platform.bing.com answered 400 in the probe, the Docker image is not built and uv/framecraft are external → treat as documented. Transferable idea: a KOSIF YAML → HTML scene generator feeding VOICE-01. **أرقام / params:** default en-US-AriaNeural; Arabic voices exist for ar-EG and ar-SA.
- **الدليل / proof:** `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/SKILL.md` · `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/references/slide-templates.md` · `kosif-atlas/skills/1644-framecraft/4629-demo-video` · `probe.md: speech.platform.bing.com 400`

## الأصوات السحابية والاستنساخ — Cloud voices & cloning

_أعلى جودة وأكثر تعبيرًا، لكنها تحتاج مفتاحًا ومالًا وموافقة. معاينة أولًا، ولا رصيد مدفوع بلا إذن المالك._

#### VOICE-06 · تعليق ElevenLabs بإعدادات جاهزة · ElevenLabs narration presets · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** مقطع MP3 لكل مشهد بنموذج eleven_multilingual_v2 وإعدادات صوت مضبوطة لكل استخدام. — One MP3 per scene via eleven_multilingual_v2 with tuned voice settings per use case.
- **متى أستخدمها / when:** حين يريد المالك صوتًا تجاريًا معبّرًا بالعربية أو الإنجليزية — premium expressive narration.
- **كيف / how:** POST /v1/text-to-speech/{voiceId} (or @elevenlabs/elevenlabs-js textToSpeech.convert) with model_id eleven_multilingual_v2 and voice_settings; key in env ELEVENLABS_API_KEY. Then size each scene to its file (VOICE-31: Remotion calculateMetadata sums durations). Presets: narration stability 0.5 / similarity 0.75 / style 0–0.3; conversational 0.4 / 0.6 / 0.3; cloned voice similarity 0.85. 5000 chars per request. **أرقام / params:** stability 0–1, similarity_boost 0–1, style 0–1, speed 0.7–1.2; ≤5000 chars/request.
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/voiceover.md`

#### VOICE-07 · اختيار النموذج والصيغة حسب الاستخدام · Model & output-format choice · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** جدول يختار نموذج ElevenLabs حسب زمن الاستجابة والتعبير، وصيغة المخرج حسب الوجهة. — Picks the ElevenLabs model by latency vs expressiveness and the output format by destination.
- **متى أستخدمها / when:** قبل أي طلب مدفوع — before every paid request.
- **كيف / how:** flash (~75 ms TTFB) for realtime, turbo (~150 ms), multilingual_v2 (~300 ms) for narration, v3 (~500 ms, 70+ languages incl. Arabic) for maximum expression. flash/turbo cost 0.5 credit/char, v2/v3 1.0. Format: pcm_44100 for editing, mp3_44100_128 (~16 KB/s) for delivery, mp3_22050_32 only for streaming previews. **أرقام / params:** TTFB flash 75 / turbo 150 / v2 300 / v3 500 ms; credits 0.5 vs 1.0 per char.
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5522-elevenlabs-performance-tuning` · `kosif-atlas/skills/1847-elevenlabs-pack/5516-elevenlabs-cost-tuning`

#### VOICE-08 · تقسيم النص الطويل مع حفظ النبرة · Long-script chunking with prosody context · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** يقسم النص الأطول من حد الطلب مع تمرير النص المجاور لكل قطعة كي تتصل النبرة عبر الوصلات. — Splits over-limit scripts while passing neighbouring text so intonation flows across joins.
- **متى أستخدمها / when:** أي تعليق أطول من ~5000 حرف أو دقائق عدة — any multi-minute script.
- **كيف / how:** Split on sentence ends below 5000 chars; send previous_text / next_text with each chunk; decode every chunk to WAV and concat the WAVs (or concat with re-encode) — never `-c copy` MP3s, whose frame padding drifts word timings by tens of ms per join (see VOICE-45). **أرقام / params:** chunk < 5000 chars; joins in PCM.
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a` · `kosif-atlas/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift`

#### VOICE-09 · استنساخ صوت بموافقة صاحبه · Consented voice cloning · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** صوت مخصص من عينات نظيفة قصيرة لمتحدث موافق — عبر ElevenLabs أو HeyGen. — A custom voice from short clean samples of a consenting speaker — ElevenLabs or HeyGen.
- **متى أستخدمها / when:** حين يريد المالك صوته هو أو صوت موظف وقّع موافقة — the owner's own voice or a signed-consent voice.
- **كيف / how:** ElevenLabs: client.voices.add({name,files}) with 1–25 files, ≥30 s total clean speech, no music; then similarity 0.85. HeyGen: heygen-voice.mjs clone uploads base64 mp3/wav, polls until complete (gives up at 120 s), prints the voice id; list/delete supported. Its 14 mocked tests ran green here, the real call needs HEYGEN_ACCESS_TOKEN. Consent first (VOICE-53). **أرقام / params:** min 30 s clean speech; 1–25 samples; mp3 or wav only; 120 s clone deadline.
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a` · `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/heygen-voice.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/heygen-voice.test.mjs`

#### VOICE-10 · تحويل صوت إلى صوت · Speech-to-speech re-voice · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** يعيد أداء تسجيل بشري بصوت آخر مع الحفاظ على توقيته وانفعاله. — Re-voices a recorded performance in another voice while keeping its timing and emotion.
- **متى أستخدمها / when:** حين يكون التوقيت مقفلًا على تسجيل مرشد (lip-sync أو حركة مبنية عليه) — keep a guide take's timing.
- **كيف / how:** speechToSpeech.convert(voiceId,{audio, model_id:'eleven_english_sts_v2', remove_background_noise:true}); input 1 s–5 min. Because the timing survives, the words.json you already built on the guide take stays valid. **أرقام / params:** input 1 s–5 min; remove_background_noise true.
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b`

#### VOICE-11 · Gemini TTS بثلاثين صوتًا · Gemini TTS with 30 prebuilt voices · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** محرر بصمة يسجّل التعليق العربي بـ Gemini ويضعه على الخط الزمني، ويغلف PCM بترويسة WAV. — The Basma editor records Arabic narration with Gemini TTS and drops it on the timeline, wrapping PCM as WAV.
- **متى أستخدمها / when:** تعليق عربي/مصري معبّر داخل محرر بصمة — expressive Arabic/Egyptian narration inside Basma.
- **كيف / how:** responseModalities AUDIO + prebuiltVoiceConfig; L16 PCM at 24 kHz wrapped with a 44-byte WAV header; models gemini-3.8-flash-tts (default), 3.8-flash-lite-tts, 2.5-flash-preview-tts; captions re-sync from the voice's voiced stretches. Needs a Gemini API key. **أرقام / params:** 30 voices: Kore, Puck, Charon, Zephyr, Fenrir, Leda, Orus, Aoede, Callirrhoe, Autonoe, Enceladus, Iapetus, Umbriel, Algieba, Despina, Erinome, Algenib, Rasalgethi, Laomedeia, Achernar, Alnilam, Schedar, Gacrux, Pulcherrima, Achird, Zubenelgenubi, Vindemiatrix, Sadachbia, Sadaltager, Sulafat; 24 kHz PCM; temperature ~0.85, top-p ~0.95 for persona reads.
- **الدليل / proof:** `app/public/js/00_editor.js:1927` · `app/public/js/10_studio.js:2198` · `app/public/js/10_studio.js:2193`

#### VOICE-12 · إخراج أداء الصوت بواسطة Claude · Claude-directed voice performance · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** قبل أن ينطق المحرك، تكتب أنت ملاحظة أداء JSON: النبرة والطاقة والسرعة والطبقة والوقفات والكلمات المشددة وأنسب صوت. — Before the engine speaks you write a JSON performance note: tone, energy, pace, pitch, pauses, stressed words and the best voice.
- **متى أستخدمها / when:** كل تعليق مهم — الإخراج مجاني، والتوليد فقط يحتاج مفتاحًا — every important read.
- **كيف / how:** VOICE.direct(text) → {note ≤60 words, voice, pace 2–4 wps, energy 1–10, pitch low|mid|high, stress[]}; the Gemini wrapper prefixes Cairo-colloquial pronunciation rules (ج hard g, ق glottal stop, ث → s/t, ذ → z/d). The direction half needs no key — apply the same JSON to Piper (length_scale from pace) or any engine. **أرقام / params:** pace 2–4 words/s; energy 1–10; note ≤ 60 words.

```json
{ "note": "دافئ وواثق، يبطئ عند الرقم ويبتسم في الخاتمة",
  "voice": "Charon", "pace": 2.6, "energy": 6, "pitch": "mid",
  "stress": ["ثلاث دقائق", "مجانًا"] }
```

- **الدليل / proof:** `app/public/js/10_studio.js:4112`

#### VOICE-13 · حوار بأكثر من متكلم · Multi-speaker dialogue production · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** من فكرة، تكتب نصًا قصيرًا بشخصيات، يُنطق كل سطر بصوت متكلمه ثم يُدمج في مسار حوار واحد. — From an idea you write a short multi-persona script; each line is voiced in its speaker's voice and mixed into one track.
- **متى أستخدمها / when:** إعلانات حوارية، اسكتشات، بودكاست قصير — dialogue ads, sketches, mini-podcasts.
- **كيف / how:** fromIdea(): Claude JSON {title, logline, speakers[{name,voice,persona}], lines[{speaker,text,delivery,beat}]} with a hook within 2 s and an arc hook → build → peak → turn → resolve; Gemini may critique; per-line TTS from female pools (Kore, Zephyr, Leda, Aoede…) and male pools (Puck, Charon, Fenrir, Orus…); concatenated mix; then the smart montage runs. **أرقام / params:** hook ≤ 2 s; 5-beat arc; one voice per speaker locked for the whole piece.
- **الدليل / proof:** `app/public/js/50_autoedit.js:1191`

#### VOICE-14 · HeyGen Starfish بطوابع زمنية للكلمات · HeyGen Starfish TTS with word timestamps · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** مزود يعيد طوابع زمنية للكلمات داخل الاستجابة نفسها، فلا حاجة لتفريغ لاحق. — A provider that returns word timestamps in the response itself, so no post-transcription is needed.
- **متى أستخدمها / when:** حين تريد مزامنة كلمة-بكلمة دون Whisper — word sync without a transcription pass.
- **كيف / how:** node heygen-tts.mjs …; provider order in the vendor engine: HeyGen Starfish (timestamps) → ElevenLabs (none) → Kokoro-82M; Gemini as an explicit alternative. Speed is validated before any TTS runs (0, 5, −1 and text are refused). Ran here: 24/26 mocked tests pass (the 2 failures are bundled-SFX path tests, not TTS). Real calls need HEYGEN_ACCESS_TOKEN. **أرقام / params:** speed must be a positive number in range; docs narrator ref. 145–155 wpm, music bed ~−31 LUFS under it.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/heygen-tts.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/heygen-tts.test.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/audio/references/tts.md`

#### VOICE-15 · محرك الصوت الموحد audio_meta.json · Unified audio engine (voice + words + BGM + SFX) · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** سكربت واحد يولد التعليق بتوقيت الكلمات والموسيقى والمؤثرات ويسجلها في audio_meta.json للمزامنة والترجمة. — One script generates narration with word timings, background music and SFX cues, recorded in audio_meta.json.
- **متى أستخدمها / when:** أفلام شرح كاملة من SCRIPT.md + STORYBOARD.md — full explainers from script + storyboard.
- **كيف / how:** node audio.mjs --script SCRIPT.md --storyboard STORYBOARD.md --hyperframes . --out audio_meta.json --voice <id> (run in background); wait-bgm.mjs before render when BGM is still generating. The pattern (one manifest = master clock) is reusable with VOICE-01 + VOICE-32 locally; the script itself needs provider keys. **أرقام / params:** outputs: voice wav, bgm, sfx, audio_meta.json.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/audio.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/audio.test.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/wait-bgm.mjs`

#### VOICE-16 · كتالوج Together للصوت · Together AI TTS catalog · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** واجهة مستضافة لـ Kokoro وOrpheus وCartesia Sonic عبر REST والبث وWebSocket. — Hosted TTS API for Kokoro, Orpheus and Cartesia Sonic over REST, streaming and WebSocket.
- **متى أستخدمها / when:** حين يريد المالك مزودًا رخيصًا بالجملة — cheap bulk hosted TTS.
- **كيف / how:** together>=2.0: client.audio.speech.create(model, input, voice, response_format) then write_to_file(). Key required. **أرقام / params:** Kokoro $4 / 1M chars · Orpheus $15 / 1M · Sonic-2 $65 / 1M.
- **الدليل / proof:** `kosif-atlas/skills/3214-togetherai-skills/13585-together-audio` · `kosif-atlas/skills/3214-togetherai-skills/13585-together-audio/references/tts-models.md`

#### VOICE-17 · أوضاع مخرج الصوت الخارجي · KOSIF Voice Director provider modes · 📄 موصوف / documented only
- **ماذا / what:** عقد لمزود خارجي: نص بالمشاعر، إكمال حلقة، سكربت مخرج، ووضع صوت (إخراج → اختيار أصوات → توليد) مع ذاكرة نطق وإعادة توليد دور واحد. — Contract for an external provider: Emotion Text, Full Episode Completion, Director Script, and Audio mode (direct → cast → render) with pronunciation memory and selective turn re-render.
- **متى أستخدمها / when:** فقط حين يكشف المضيف هذا المزود — only when the host exposes it.
- **كيف / how:** Stable casting across episodes; re-render only the changed turn; report backend config errors verbatim; songs go to song generation, never to TTS.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-source-router/references/providers/voice-director-v10.4.md`

## كتابة التعليق وإخراجه — Script writing & voice direction

_التعليق الجيد يُكتب للأذن لا للعين. هذه القواعد مجانية وتعمل مع كل محرك._

#### VOICE-18 · ميزانية الكلمات في الثانية · Words-per-second budget · 📄 موصوف / documented only
- **ماذا / what:** تحسب عدد الكلمات المسموح لكل مشهد من مدته قبل التوليد. — Computes the allowed word count per scene from its duration before any TTS.
- **متى أستخدمها / when:** عند كتابة كل سطر — while writing every line.
- **كيف / how:** English narration 2.5 wps (15 s ≈ 37 words, 30 s ≈ 75, 60 s ≈ 150); direction spec 2.3–2.7 wps with total within ±5 % of target. By genre: ads 150–170 wpm, narration 130–150, meditation 100–120. Scene fill: 3–4 s → 8–12 words (~70 %), 5–6 s → 15–22 (~75 %), 7–8 s → 22–30 (~80 %). Arabic carries fewer words per second than English (longer words, more syllables) — budget ~15–20 % fewer words and measure with the real voice (the Piper test line ran at ~1.35 wps). **أرقام / params:** 2.3–2.7 wps; ±5 % total; ads 150–170 / narration 130–150 / meditation 100–120 wpm.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/narration.md` · `100-superskills/skills/voiceover-tts-direction/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md` · `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### VOICE-19 · السرعة حسب المحتوى — أعد التوليد ولا تمطّ · Read speed by content — regenerate, never stretch · ✅ مُثبت هنا / proven here
- **ماذا / what:** أبطئ للشرح الكثيف وأسرع قليلًا للخطّاف، بتغيير معامل السرعة في المحرك لا بمطّ الملف. — Slower for dense explanation, slightly faster for hooks — change the engine's speed, never time-stretch the file.
- **متى أستخدمها / when:** حين لا يطابق طول التعليق المشهد — when the read does not fit the scene.
- **كيف / how:** Speed 0.7–0.8 tutorial · 1.0 natural · 1.1–1.2 upbeat; avoid ≥1.5. Piper's knob is the inverse (length_scale 1.15 = slower). Ran here: same two Arabic sentences with --length-scale 1.15 --sentence-silence 0.35 → 7.13 s; re-generation keeps formants natural where atempo/rubberband stretching smears consonants. **أرقام / params:** speed 0.7–1.2 (avoid ≥1.5); Piper length_scale ≈ 1/speed.
- **الدليل / proof:** `run here 2026-10-16: piper --length-scale 1.15 → 7.13 s` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/tts.md` · `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a`

#### VOICE-20 · نص النطق غير نص الشاشة · Spoken form vs on-screen form · 📄 موصوف / documented only
- **ماذا / what:** المحرك يقرأ النطاقات والاختصارات والأرقام حرفيًا؛ اكتب الشكل المنطوق في التعليق واترك الإملاء الحقيقي على الشاشة. — TTS reads domains, acronyms and numbers literally; write the spoken form in narration and keep the real spelling on screen.
- **متى أستخدمها / when:** كل رقم أو رابط أو اسم لاتيني أو كلمة ملتبسة — every number, URL, Latin brand or ambiguous word.
- **كيف / how:** Keep two files per scene: `say.txt` (to TTS) and `show.txt` (to captions). Pronunciation map per project: '.com' → 'دوت كوم', 'API' → 'إيه بي آي', '$1.9T' → 'قرابة تريليوني دولار', '٢٠٢٦' → 'ألفين وستة وعشرين'. Add tashkeel only on ambiguous words (عَلِم/عِلْم). Then align captions to the spoken words but display show.txt (ARAB captions family).

```json
{ "say":  { ".com": "دوت كوم", "API": "إيه بي آي", "AI": "الذكاء الاصطناعي",
            "15": "خمستاشر", "1000": "ألف" },
  "show": "kosif.ai — API — 15 دقيقة" }
```

- **الدليل / proof:** `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/references/pronunciation.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/narration.md` · `100-superskills/skills/voiceover-tts-direction/SKILL.md`

#### VOICE-21 · قواعد كتابة التعليق للمشهد · Scene narration writing rules · 📄 موصوف / documented only
- **ماذا / what:** فكرة واحدة لكل مشهد، ابدأ بالفعل، لا مصطلحات، تباين بعبارات قصيرة، وصف الحدث قبل ظهوره بلحظة. — One idea per scene, lead with the verb, no jargon, short contrast counts, describe an on-screen action just before it happens.
- **متى أستخدمها / when:** عند كتابة أي سكربت — every script.
- **كيف / how:** If a sentence needs 'and' (و) it is two scenes. Contrast in counts: '24 تبويبًا. نقرة واحدة. 5 مجموعات.' Narrate an action ~0.3–0.5 s before it appears so the eye arrives with the ear. Strong first line (hook within 2 s). Each scene's narration in its own text file feeding TTS and caption timing. The script complements the visuals; it never reads the on-screen text aloud. **أرقام / params:** 1 idea / scene; action narrated 0.3–0.5 s early; hook ≤ 2 s.
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video/SKILL.md` · `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/SKILL.md` · `kosif-one/vendor/brag/skills/brag/SKILL.md`

#### VOICE-22 · سكربت تعليق بوسوم أداء SSML · VO script with performance tags (SSML) · 📄 موصوف / documented only
- **ماذا / what:** سكربت منطوق: جمل قصيرة، أرقام وعملات وتواريخ كما تُقال، وسوم وقفة وتشديد وسرعة، ومواصفات صوت. — A spoken-style script with pauses, emphasis and rate tags plus a voice profile, for TTS or a human reader.
- **متى أستخدمها / when:** قبل أي توليد مدفوع أو تسجيل بشري — before any paid render or studio session.
- **كيف / how:** Write vo-script.md (profile: gender, age, tone, dialect, pace) + ssml.xml. Inline markup: [pause 0.5s], *emphasis*, (emotion). Map to engines: SSML <break time='500ms'/> and <prosody rate='-5%'> for Windows/Edge; sentence-silence and length_scale for Piper; voice_settings for ElevenLabs. After generation measure duration, level, peaks and mispronounced words. **أرقام / params:** duration within ±5 %; pauses 0.3–0.8 s.
- **الدليل / proof:** `100-superskills/skills/voiceover-tts-direction/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md`

#### VOICE-23 · نص التعليق المقفل SCRIPT.md · Locked narration file (SCRIPT.md) · 📄 موصوف / documented only
- **ماذا / what:** ملف تعليق مقفل: ترويسة بالمزود والإعدادات والإخراج، ثم كتلة لكل سطر بالإطار ودليل الزمن وملاحظة الأداء والنص المنطوق. — A locked narration file: header with provider/settings/direction, then one block per line with frame, time guide, delivery note and spoken text.
- **متى أستخدمها / when:** أفلام متعددة المشاهد يُعاد توليدها كثيرًا — multi-scene films that get re-rendered.
- **كيف / how:** Blocks `## Line N — label (Frame N)` with Time guide, Delivery note and the indented spoken text fed to TTS. Real timing comes from TTS word timestamps (VOICE-32), never from the Time guide.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/script-format.md`

#### VOICE-24 · توجيه الصوت باللهجات العربية · Arabic dialect voice-direction workflow · 📄 موصوف / documented only
- **ماذا / what:** خط نصي أولًا يجعل الصوت المولد طبيعيًا بالمصرية أو الفصحى أو السعودية أو الشامية أو المغربية أو الخليجية. — Text-first pipeline that makes TTS sound native in Egyptian, MSA, Saudi, Levantine, Moroccan or Gulf Arabic.
- **متى أستخدمها / when:** أي تعليق عامي — any dialect read.
- **كيف / how:** Brief → rewrite for the ear (short sentences, breath points) → pronunciation memory table (written → spoken; phonetic spelling fixes slang) → per-block direction (emotion, energy 1–5, pace, pauses, emphasis) → render only if a provider is exposed (preview first; no paid credits without approval) → measure (kosif_audio_analyze). Never mix dialects inside one block. **أرقام / params:** energy 1–5; one dialect per block.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-voice/SKILL.md`

#### VOICE-25 · اختيار اللغة واللهجة في المقابلة · Language & dialect intake field · 🟢 جاهز / ready
- **ماذا / what:** الموجز يسجل لغة النص ولهجة الصوت (فصحى، مصري، سعودي، إنجليزي؛ الافتراضي ar-EG) ويمررها إلى STYLE.md. — The brief records on-screen language and voice dialect (fusha, Egyptian, Saudi, English; default ar-EG) and passes it to STYLE.md.
- **متى أستخدمها / when:** أول سؤال في أي فيلم مروي — first intake question of any narrated film.
- **كيف / how:** brief.language in the fastify-motion-bro CLI; the voice engine and pronunciation map are then chosen from it (ar-SA → Piper/Naayf; ar-EG → Gemini persona VOICE-26). **أرقام / params:** default ar-EG.
- **الدليل / proof:** `fastify-motion-bro/docs/QUESTIONS.md:6` · `fastify-motion-bro/scripts/cli.mjs:14`

#### VOICE-26 · شخصية اليوتيوبر المصري · Egyptian YouTuber voice persona · 📄 موصوف / documented only
- **ماذا / what:** راوٍ مصري دافئ متحمس بقواعد نطق وأرقام مصرية دقيقة. — A warm, energetic Egyptian narrator persona with exact pronunciation and number rules.
- **متى أستخدمها / when:** ريلز وشروحات بالعامية المصرية — Egyptian reels and explainers.
- **كيف / how:** Fillers sparingly (يا جماعة، بصوا بقى، تمام؟، زي ما انتم شايفين); ج as hard g; ق as glottal stop; ث → s/t; ذ → z/d; natural breaths. Numbers: 11 حداشر, 12 اتناشر, 15 خمستاشر, 100 مية, 1000 ألف; جنيه = geneh. Gemini temperature ~0.85, top-p ~0.95. **أرقام / params:** ≤1 filler per 3 sentences; temperature 0.85; top-p 0.95.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-voice/SKILL.md` · `app/public/js/10_studio.js:4112`

#### VOICE-27 · صوت الراوي الوثائقي المقفل · Locked documentary narrator voice · ✅ مُثبت هنا / proven here
- **ماذا / what:** وصف صوت ثابت في كل مقطع (راوٍ ذكوري عميق جاد بصدى بكرة فيلم قديمة) وجملة واحدة أقل من 20 كلمة لكل مقطع. — An identical voice description in every clip (deep, serious male narrator, slightly reverberant like an old film reel) and one sentence under 20 words per clip.
- **متى أستخدمها / when:** أفلام الأرشيف والتاريخ على طريقة Vox — Vox-style history films.
- **كيف / how:** VOICE constant + narrate(topic,i,n) truncated to 19 words, plus projector hum and paper snaps. Locking the description prevents voice drift between generated clips. Ran here: production-profiles test 10/10 pass, asserting <20 words and the VOICE string in every 10 s clip prompt. **أرقام / params:** < 20 words per 10 s clip; same voice string in every prompt.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/vox-history.mjs:12` · `fastify-motion-bro/tests/production-profiles.test.mjs:41` · `run here 2026-10-16: node --test tests/production-profiles.test.mjs → 10/10`

#### VOICE-28 · جمل صوت المدرب · Coach voice cue lines · ✅ مُثبت هنا / proven here
- **ماذا / what:** جمل تدريب أمرية قصيرة منفصلة عن وصف اللقطة (تحكم في النزول، شد عضلات البطن). — Short imperative coaching lines kept separate from the shot description.
- **متى أستخدمها / when:** فيديوهات اللياقة والتعليم الحركي — fitness and movement tutorials.
- **كيف / how:** COACH array (5 generic) + per-muscle arrays for Abs, Chest, Back (15 lines); one cue per rep phase; keep them ≤ 6 words so they land inside a 2 s movement. Profile tests ran here (10/10). **أرقام / params:** 5 generic + 15 muscle-specific lines; ≤ 6 words each.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/fitness.mjs:16` · `run here 2026-10-16: production-profiles tests 10/10`

#### VOICE-29 · مواصفات تسجيل الصوت البشري · Human VO recording spec · 📄 موصوف / documented only
- **ماذا / what:** مواصفات تسجيل المعلق البشري حتى يصل الملف صالحًا للمزامنة والمعالجة. — Recording spec for a human voice-over so the file arrives sync- and processing-ready.
- **متى أستخدمها / when:** حين يسجل المالك صوته — when the owner records himself.
- **كيف / how:** Cardioid mic at 10–15 cm with a pop filter; peaks ≈ −12 dBFS; 48 kHz / 24-bit WAV; podcast noise floor < −60 dBFS; record room tone 5 s first (feeds afftdn). Then VOICE-39 cleanup, never re-timing. **أرقام / params:** 10–15 cm; peaks −12 dBFS; 48 kHz/24-bit; noise floor < −60 dBFS.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md`

#### VOICE-30 · مدرب اللغة الثنائي · Language Coach (AR/EN) skill · 📄 موصوف / documented only
- **ماذا / what:** مهارة المالك لتعلم اللغة بالممارسة؛ تفيد في كتابة تعليق ثنائي اللغة وترجمة سطر بسطر. — Owner skill for practice-based language learning; useful for bilingual narration and line-by-line translation.
- **متى أستخدمها / when:** أفلام تعليمية ثنائية اللغة — bilingual learning films.
- **كيف / how:** Load language-coach-arabic-english (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/language-coach-arabic-english/SKILL.md`

## الصوت ساعةُ الفيلم — Voice-led timing & sync

_التعليق هو الساعة الأساسية: يُولَّد أولًا، يُقاس، ثم تُبنى الحركة على كلماته. هذا قلب قوتك هنا._

#### VOICE-31 · مدة المشهد = طول التعليق + هامش · Scene duration from voice length · ✅ مُثبت هنا / proven here
- **ماذا / what:** تولد التعليق أولًا ثم تقيس كل ملف وتحدد مدة المشهد منه بدل العكس. — Generate narration first, measure each file, and size every scene from it — never the reverse.
- **متى أستخدمها / when:** كل فيلم مروي — every narrated film.
- **كيف / how:** Per scene: dur = ffprobe(vo_n) + 0.3–1.5 s buffer (1.5 s for demo scenes with UI to read). Remotion: calculateMetadata sums the scene durations; HTML: write the start times into the timeline JSON. Ran here: Arabic VO (loudnorm −14) muxed over a 1080x1920/30 fps plate of exactly ffprobe length → verify_video 11/11 PASS, delivered audio 7.430 s vs master 7.430 s. **أرقام / params:** buffer 0.3–1.5 s; audio vs master ±50 ms.

```bash
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 vo.wav)
ffmpeg -f lavfi -i color=c=0x0f172a:s=1080x1920:r=30 -i vo.wav -t $D \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest vo.mp4
python3 kosif-tool/tools/verify_video.py vo.mp4 --aspect 9:16 --fps 30 \
  --audio vo.wav --lufs -14
```

- **الدليل / proof:** `run here 2026-10-16: vo.mp4 verify_video 11/11, 7.430 vs 7.430 s` · `kosif-tool/tools/verify_video.py` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/voiceover.md` · `kosif-atlas/skills/166-demo-video/535-demo-video/references/scene-design-system.md`

#### VOICE-32 · توقيت كلمات التعليق المولد بـ faster-whisper · Word timings from the generated voice (faster-whisper) · ✅ مُثبت هنا / proven here
- **ماذا / what:** تفرّغ الصوت المولد بطوابع زمنية لكل كلمة ثم تحوله إلى words.json لتتزامن الحركة والترجمة. — Transcribe the generated voice with per-word timestamps and convert to words.json so motion and captions sync.
- **متى أستخدمها / when:** بعد كل توليد صوت لا يعيد طوابع زمنية — after any TTS without native timestamps.
- **كيف / how:** pip install faster-whisper; resample to 16 kHz mono f32 and pass the numpy array (in this venv PyAV 19 rejects faster-whisper's open() kwargs, so do not pass a path); WhisperModel('small', device='cpu', compute_type='int8'), language='ar', word_timestamps=True; dump segments → `python3 kosif-tool/tools/words_convert.py ar.whisper.json words.json`. Ran in an earlier session's venv (2026-10-16; not installed in the current container, so install first): 10 words, 0.00 → 7.26 s. Lesson: Whisper split «محليًا» into «محل» + «ين» — always re-attach to the known script (VOICE-33). (code snippet in references/powers/voice-tts.md) **أرقام / params:** 16 kHz mono; model small int8 on CPU (large-v3 for final); key words ≤ 100 ms, others ≤ 150 ms.

```python
import numpy as np, subprocess, json
from faster_whisper import WhisperModel
pcm = subprocess.run(['ffmpeg','-v','error','-i','vo.wav','-ar','16000','-ac','1',
                      '-f','f32le','-'], capture_output=True).stdout
a = np.frombuffer(pcm, np.float32)
segs, _ = WhisperModel('small', device='cpu', compute_type='int8') \
          .transcribe(a, language='ar', word_timestamps=True)
json.dump({'segments': [{'start': s.start, 'end': s.end, 'text': s.text, 'words':
  [{'word': w.word, 'start': w.start, 'end': w.end} for w in s.words]} for s in segs]},
  open('vo.whisper.json', 'w'), ensure_ascii=False)
```

- **الدليل / proof:** `earlier session 2026-10-16 (venv; not installed in the current container, pip install faster-whisper): faster-whisper 1.2.1 small → words.json 10 words` · `kosif-tool/playbooks/audio-sync.md:26` · `kosif-tool/tools/words_convert.py` · `100-superskills/skills/audio-reactive-captions-studio/references/captions-rules.md`
- **تثبيت / install:** `pip install faster-whisper`

#### VOICE-33 · إعادة لصق النص المعروف على توقيت ويسبر · Re-attach the known script to Whisper timings · 📄 موصوف / documented only
- **ماذا / what:** لأنك كتبت النص بنفسك، اعرض كلماتك أنت واستعمل من ويسبر التوقيت فقط. — Because you wrote the script, display your own words and take only the timing from Whisper.
- **متى أستخدمها / when:** دائمًا مع التعليق المولد — always with generated narration.
- **كيف / how:** Normalise both sides (strip tashkeel, unify أ/إ/آ → ا, ة → ه, ى → ي); walk script words and greedily consume Whisper tokens until the normalised concatenation matches (handles splits like محل+ين and merges); start = first token start, end = last token end. If drift persists use WhisperX forced alignment (pip install whisperx). Never edit timings by hand, only text. **أرقام / params:** match on normalised text; fall back to WhisperX.
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:26` · `kosif-tool/tools/words_convert.py`

#### VOICE-34 · إيقاع يقوده التعليق · Voice-led pacing · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل فكرة بصرية تبقى بطول جملتها (~4–6 ث) مع حركات دقيقة مربوطة بالكلمات المفتاحية. — Each visual idea holds for its sentence (~4–6 s) with micro-animations tied to key words.
- **متى أستخدمها / when:** الشروح الهادئة والمحاضرات — calm explainers and lectures.
- **كيف / how:** Generate TTS first; one idea per sentence; key-word sync ≤ 100 ms; camera drifts during pauses so the frame never dies (pauses > 1.5 s need movement). Seen: the 60 s cream-paper explainer (~5 s per idea, static ratio ~0.65), the Fusha doodle parable (camera moves in pauses), a 457 s Chinese edge-tts Manim explainer (visuals step per sentence). **أرقام / params:** ~4–6 s per idea; key word ≤ 100 ms; pause > 1.5 s → ambient motion.
- **الدليل / proof:** `style:pm-1stnoel-c20a89` · `style:doodle` · `style:pm-linearuncle-5d2bae` · `kosif-tool/playbooks/audio-sync.md`

#### VOICE-35 · قراءة صوتية بتظليل الكلمة المنطوقة · Read-aloud karaoke highlight · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الجملة تبدأ رمادية وتتحول كل كلمة منطوقة إلى الحبر الداكن، والكلمة الحالية داخل صندوق تظليل. — The sentence starts grey, each spoken word turns to ink, and the current word sits in a highlight box.
- **متى أستخدمها / when:** تعليم القراءة، الآيات، الاقتباسات — reading lessons, verses, quotes.
- **كيف / how:** From words.json: all words at ink #8a7b70 (or 25 % opacity ghosts as in the doodle reel), at word.start − 60 ms tween to #1f1b17 over 120 ms; a peach box #f6cf9a slides behind the current word (x/width tween 140 ms outBack). Arabic: whole words only, RTL container (ARAB-01). Doodle variant: key word recoloured orange with a wiggling squiggle underline. **أرقام / params:** lead 60 ms; 120 ms colour tween; ghosts 25 % opacity; box #f6cf9a on #f4eee0.
- **الدليل / proof:** `style:pm-1stnoel-c20a89` · `style:doodle` · `kosif-tool/playbooks/audio-sync.md`

#### VOICE-36 · ترجمة تُكتب على توقيت الصوت · Typewriter captions on voice word times · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الكلمات تُكتب بمؤشر رفيع في اللحظة التي ينطقها الصوت، والكلمة المؤكدة بتدرج متوهج. — Words type in with a thin caret exactly as the voice speaks them; the emphasised word lands in a glowing gradient.
- **متى أستخدمها / when:** إعلانات الإطلاق القصيرة — short launch films.
- **كيف / how:** Seen in a 22 s 1:1 launch film with an ElevenLabs VO over music ducked at the drop: captions typed at the voice word table inside a glass pill, no full stops, key word filled #f06aa8 → #8a6cf5 → #5d8cf7 with a faint glow, slow camera push 1.0 → 1.04 per scene. Build: per word, reveal at word.start, caret blink 530 ms; Arabic types per word not per letter. **أرقام / params:** reveal at word.start; caret blink 530 ms; push 1.0 → 1.04.
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### VOICE-37 · موجة الصوت ومؤشر التشغيل · Voice waveform with playhead · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** رسم موجة الصوت مع رأس تشغيل يتقدم بينما الرسم التوضيحي يكتمل متزامنًا مع الكلام. — A drawn voice waveform with a progressing playhead while an illustration completes in sync with speech.
- **متى أستخدمها / when:** حين يكون المنتج نفسه صوتيًا أو لإظهار أن هناك تعليقًا — voice products, 'listen' moments.
- **كيف / how:** Pre-compute peaks: `ffmpeg -i vo.wav -ac 1 -ar 100 -f f32le -` → 100 values/s → abs → bars 3 px wide / 2 px gap, height = peak × 60 px, rounded caps, played bars #3b69f3, unplayed #5c5c6f at 30 %; playhead x = t/dur × width. Seen in a 30 s SaaS explainer on #f8f5ec with a photosynthesis diagram synced to the waveform. **أرقام / params:** 100 peaks/s; bar 3 px + gap 2 px; #3b69f3 / #5c5c6f.
- **الدليل / proof:** `style:pm-sudo-kiran-6609ed`

#### VOICE-38 · محاضرة مروية: رسم يتقدم مع الجمل · Narrated lecture: draw-on paced to sentences · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سبورة يرسم عليها قلم ظاهر عنصرًا تلو الآخر بسرعة التعليق، والترجمة تتبدل كل جملة تحت اللوح. — A whiteboard where a visible marker draws element after element at narration speed, subtitles swapping per sentence below the board.
- **متى أستخدمها / when:** الشروح العلمية الطويلة — long science explainers.
- **كيف / how:** Per narration sentence: one draw-on element (seconds per element = sentence length), marker icon rides the stroke tip and changes cap colour with ink (#1c1c1c, #c42d3f, #2b4a9b, #2f8a5b); eraser wipe between chapters; subtitles 1–2 centred lines. Seen in a 308 s lecture (static ratio 0.945 — narration carries it) and a bilingual-subtitle whiteboard walk-through. **أرقام / params:** 1 element per sentence; subtitle swap per sentence; eraser wipe between chapters.
- **الدليل / proof:** `style:pm-tak3sh8-be5012` · `style:pm-lemomo-ai-0d9cff`

## معالجة الصوت ومزجه — Voice processing & mix

_التعليق الخام ليس جاهزًا: نظّف، لوّن عند الحاجة، اخفض الموسيقى تحته، وسلّم بجهارة مقاسة._

#### VOICE-39 · سلسلة تنظيف الصوت البشري · Voice clean-up chain · ✅ مُثبت هنا / proven here
- **ماذا / what:** قطع الهدير، إزالة ضوضاء خفيفة، دفء وحضور بالمعادل، تخفيف الصفير، وضغط لطيف للمقاطع الناطقة. — High-pass, light denoise, warmth and presence EQ, de-ess and gentle compression for talking clips.
- **متى أستخدمها / when:** أي صوت بشري مسجل؛ وخفيفًا على المولد — any recorded voice; lightly on TTS.
- **كيف / how:** Owner chain in reel.py (identical in kosif-studio, kosif-one and kosif-montage-motion). Ran here on a test signal + loudnorm → −15.9 LUFS integrated, 48 kHz. **أرقام / params:** HPF 70 Hz; afftdn nr 6 nf −42; +1.2 dB @220 Hz; +2.2 dB @3.2 kHz (w 1.4); −1 dB @9 kHz; deesser i 0.35; comp thr 0.12 ratio 2.5 att 10 ms rel 160 ms makeup 1.6.

```bash
ffmpeg -i raw.wav -af "highpass=f=70,afftdn=nr=6:nf=-42,\
equalizer=f=220:t=q:w=1:g=1.2,equalizer=f=3200:t=q:w=1.4:g=2.2,\
equalizer=f=9000:t=q:w=1:g=-1,deesser=i=0.35,\
acompressor=threshold=0.12:ratio=2.5:attack=10:release=160:makeup=1.6" clean.wav
```

- **الدليل / proof:** `kosif-studio/motion/reel.py:38` · `kosif-one/tools/kosif-studio/motion/reel.py:38` · `100-superskills/skills/kosif-montage-motion/scripts/reel.py:38` · `run here 2026-10-16: chain + loudnorm → −15.9 LUFS`

#### VOICE-40 · وصفات إصلاح الصوت بالأعراض · Voice repair presets by symptom · 📄 موصوف / documented only
- **ماذا / what:** تشخيص العرض أولًا ثم إصلاح واحد: الطنين، الطين، الصندوقية، الحدة، الوضوح. — Diagnose the symptom first, then one fix: rumble, mud, boxiness, harshness, clarity.
- **متى أستخدمها / when:** حين يبدو التسجيل معيبًا لا مجرد خام — when a recording sounds wrong, not just raw.
- **كيف / how:** Vendor presets voice-clean (rumble → mud → even loudness → clarity → peak ceiling), voice-broadcast (+ boxiness, air, warmth), voice-warm (+ weight); singles rumble-cut, room-gate, boom-tame, harsh-tame. The HyperFrames fx-chain is not installable here, so apply the same numbers as ffmpeg `equalizer=f=…:t=q:w=Q:g=…`. **أرقام / params:** boom 200 Hz −4 dB Q1.4; mud 250 Hz −3 dB Q1.2; boxiness 400 Hz −3 dB Q1.4; clarity 3 kHz +2.5 dB Q1; harshness 3.2 kHz −3 dB Q1.6; rumble HPF 80 Hz.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/presets.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-audio/SKILL.md`

#### VOICE-41 · أزياء صوتية للشخصيات · Character voice costumes · ✅ مُثبت هنا / proven here
- **ماذا / what:** تلوين متعمد للصوت: هاتف، راديو AM، مكبر صوت، شريط قديم، نداء عام، إنتركم — واحد فقط في كل مرة. — Deliberate voice styling: telephone, AM radio, megaphone, lo-fi tape, PA system, intercom — never stack two.
- **متى أستخدمها / when:** مكالمة داخل القصة، إعلان مطار، فلاشباك — a call in the story, a PA announcement, a flashback.
- **كيف / how:** Vendor names 7 presets (telephone, radio-am, megaphone, lofi-tape, pa-system, intercom, doofus-worble) for its fx-chain; the ffmpeg equivalents below rendered here on the Piper Arabic line (telephone 7.43 s, megaphone 7.47 s, room 7.57 s). **أرقام / params:** telephone HPF 300 / LPF 3400 + comp 4:1; megaphone HPF 500 / LPF 4000 + acrusher 10-bit mix 0.25 + 40 ms slap; room aecho 60|140 ms.

```bash
# telephone
ffmpeg -i vo.wav -af "highpass=f=300,lowpass=f=3400,acompressor=threshold=0.1:ratio=4,volume=1.5" tel.wav
# megaphone
ffmpeg -i vo.wav -af "highpass=f=500,lowpass=f=4000,acrusher=bits=10:mix=0.25,aecho=0.8:0.6:40:0.25" mega.wav
```

- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/presets.md` · `run here 2026-10-16: tel.wav / mega.wav / reverb.wav rendered`

#### VOICE-42 · مختبر الصوت: عزل الصوت وفصل الموسيقى · Audiolab voice isolation & stem split · ✅ مُثبت هنا / proven here
- **ماذا / what:** يعزل الكلام بـ RNNoise + إزالة ضوضاء FFT، أو يلغي الموسيقى من المركز، بخمسة أوضاع. — Isolates speech with RNNoise + FFT denoise, or centre-cancels music, in five modes.
- **متى أستخدمها / when:** صوت مسجل فوق موسيقى أو ضوضاء، أو حين تريد الموسيقى بلا كلام — voice over noise/music, or a music-only bed.
- **كيف / how:** `python scripts/kmotion.py audiolab FILE --mode voice|music|both|novoice|nomusic [--strong]`; centre-cancel works on stereo only; bass below 140 Hz restored after phase cancel. Measured speech/pause contrast 11.2 → 40.9 dB. **أرقام / params:** modes voice|music|both|novoice|nomusic; --strong; bass restore < 140 Hz; contrast 11.2 → 40.9 dB.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/audiolab.py` · `100-superskills/skills/kosif-montage-motion/SKILL.md` · `100-superskills/skills/kosif-montage-motion/references/operating-manual.md`

#### VOICE-43 · خفض الموسيقى تحت التعليق · Music ducking under the voice · ✅ مُثبت هنا / proven here
- **ماذا / what:** الموسيقى تنخفض تلقائيًا كلما تكلم الصوت وتعود في الوقفات. — The music dips automatically whenever the voice speaks and returns in the pauses.
- **متى أستخدمها / when:** كل فيلم فيه تعليق وموسيقى — every film with VO + music.
- **كيف / how:** Owner convention: mark `<audio data-role="voice">` and the mux ducks the other clips. Raw ffmpeg: sidechaincompress with the voice as key. Ran here: music bed 220 Hz −31.5 dB before the voice → −48.5 dB under it (≈ 17 dB duck), then loudnorm → −14.8 LUFS. For a gentler bed use ratio 4 (≈ −8 to −12 dB). **أرقام / params:** threshold 0.03; ratio 4–8; attack 20 ms; release 400 ms; bed ~ −31 LUFS under VO.

```bash
ffmpeg -i music.wav -i vo.wav -filter_complex \
"[1]aresample=48000,asplit=2[vo][key];[0]aresample=48000[m];\
[m][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];\
[duck][vo]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[out]" \
-map "[out]" -ar 48000 mix.wav
```

- **الدليل / proof:** `kosif-studio/motion/references/hyperframes-authoring.md` · `kosif-one/tools/kosif-studio/motion/voice.py` · `run here 2026-10-16: sidechaincompress −31.5 → −48.5 dB`

#### VOICE-44 · التسليم بجهارة −14 LUFS وفحص البوابة · −14 LUFS delivery + gate · ✅ مُثبت هنا / proven here
- **ماذا / what:** تسليم الصوت عند −14 LUFS وذروة حقيقية ≤ −1 dBFS، مع فحص آلي للطول والصيغة. — Deliver at −14 LUFS with true peak ≤ −1 dBFS, verified by an automatic gate.
- **متى أستخدمها / when:** قبل أي تسليم — before every delivery.
- **كيف / how:** loudnorm=I=-14:TP=-1.5:LRA=11 (−16 for podcasts), 48 kHz stereo, AAC 192k, then `python3 kosif-tool/tools/verify_video.py film.mp4 --audio vo.wav --lufs -14`. Ran here: 11/11 PASS, −14.8 LUFS, TP −4.3 dBFS. **أرقام / params:** I −14 ±1.5 LUFS; TP ≤ −1 dBFS; ≥ 44.1 kHz; audio vs master ±50 ms.
- **الدليل / proof:** `kosif-tool/tools/verify_video.py` · `run here 2026-10-16: verify_video 11/11 PASS` · `kosif-studio/motion/references/hyperframes-authoring.md`

#### VOICE-45 · وصل المقاطع كـ WAV لا MP3 · Join chunks as PCM, not MP3 copy · 📄 موصوف / documented only
- **ماذا / what:** ضمّ قطع التعليق بعد فكها إلى WAV؛ نسخ MP3 مباشرة يضيف حشوًا يزيح توقيت الكلمات. — Concatenate narration chunks after decoding to WAV; MP3 stream-copy adds padding that drifts word timings.
- **متى أستخدمها / when:** كل تعليق مولد على دفعات — every chunked narration.
- **كيف / how:** Decode each chunk to 48 kHz PCM, concat with the concat filter (or concat demuxer on WAVs), then transcribe the JOINED file once — never add per-chunk transcripts with offsets. **أرقام / params:** MP3 encoder delay ≈ 1105 samples per chunk.
- **الدليل / proof:** `kosif-atlas/skills/3323-joined-audio-transcript-drift/13837-joined-audio-transcript-drift` · `kosif-atlas/skills/1847-elevenlabs-pack/5514-elevenlabs-core-workflow-a`

## الصوت التفاعلي وواجهاته — Interactive voice & voice UI

_حين يكون الصوت داخل المنتج نفسه: مساعد يسمع ويتكلم، وواجهة تُظهر حالته._

#### VOICE-46 · محادثة صوتية عربية لحظية عبر WebRTC · Realtime Arabic speech-to-speech (WebRTC) · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** المتصفح يفتح اتصال WebRTC ويرسل عرض SDP إلى Worker يضيف المفتاح وإعدادات الجلسة، ثم صوت باتجاهين وقناة أحداث. — The browser opens WebRTC, posts its SDP offer to a Cloudflare Worker that adds the key and session config, then streams two-way audio with an events channel.
- **متى أستخدمها / when:** مساعد صوتي داخل تطبيق المالك — a voice assistant inside an owner app.
- **كيف / how:** voice.js createVoiceAssistant().start(); worker POST /api/realtime/session → realtime calls with model gpt-realtime, input transcription gpt-4o-mini-transcribe (language ar), server_vad turn detection, output voice 'marin'; session.update injects file context (≤ 14000 chars); fallback = deterministic router VOICE-48. Needs OPENAI_API_KEY as a Worker secret. **أرقام / params:** Content-Type application/sdp; SDP ≤ 200000 bytes; data channel 'oai-events'; context ≤ 14000 chars.
- **الدليل / proof:** `kosif-audit-studio/voice.js:254` · `kosif-audit-studio/cloudflare/realtime-worker.js` · `kosif-earth-ci-fork/ui/audit/classic/voice.js`

#### VOICE-47 · مقاطعة المساعد بالكلام · Barge-in interruption · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** إذا تكلم المستخدم أثناء كلام المساعد، تنقلب الواجهة إلى الاستماع ويُلغى الرد. — If the user speaks while the assistant talks, the UI flips to listening and the response is cancelled.
- **متى أستخدمها / when:** كل مساعد صوتي — every voice assistant.
- **كيف / how:** On event input_audio_buffer.speech_started while state = speaking → emit 'interrupted'; interrupt() sends {type:'response.cancel'} over the data channel.
- **الدليل / proof:** `kosif-audit-studio/voice.js:204` · `kosif-audit-studio/voice.js:351`

#### VOICE-48 · موجه نوايا صوتي عربي حتمي · Deterministic Arabic voice intent router · ✅ مُثبت هنا / proven here
- **ماذا / what:** موجه قواعد يحول الكلام العربي المطبع إلى تنقل بين الشاشات وإجابات حالة، دون اختراع أرقام. — A rule router mapping normalised Arabic utterances to screen navigation and status answers, never inventing numbers.
- **متى أستخدمها / when:** أي واجهة صوتية يجب أن تعمل بلا ذكاء حي — voice UI that must work with no live AI.
- **كيف / how:** routeIntent(transcript, context, api) with VIEW_WORDS (18 views) and has() keyword checks; unknown → guidance reply. Ran here: node --test tests/voice.test.js → 3/3 pass (navigation, status, unknown). **أرقام / params:** 18 view vocabularies; 3 tests.
- **الدليل / proof:** `kosif-audit-studio/voice.js:45` · `kosif-audit-studio/tests/voice.test.js` · `run here 2026-10-16: voice.test.js 3/3`

#### VOICE-49 · كرة الصوت بحالاتها · Voice orb state animation · 🟢 جاهز / ready
- **ماذا / what:** كرة 44 بكسل تروي حالة الجلسة: خاملة بنفسجية، تستمع فيروزية بثلاث حلقات، تفكر بدوامة مخروطية، تتكلم بنبض تنفس. — A 44 px orb narrating the session: idle violet, listening teal with three rings, thinking conic swirl, speaking breathing pulse.
- **متى أستخدمها / when:** واجهة مساعد صوتي أو لقطة منتج صوتي في فيلم — voice UI or a voice-product shot in a film.
- **كيف / how:** Set data-state on #voiceOrb (idle|listening|thinking|speaking); keyframes orb-pulse, orb-spin, orb-breathe. **أرقام / params:** idle radial at 35% 35% #c4b5fd → #6d28d9 60% → #1e1b4b; listening #99f6e4 → #0f766e → #042f2e + 8 px halo rgba(15,118,110,.18), rings 1.8 s ease-out scale .6 → 1.9 delays 0/.6/1.2 s; thinking conic #a78bfa,#6d28d9,#0f766e spin 1.2 s linear; speaking scale 1.1 breathe 1 s + 10 px halo.

```css
#voiceOrb[data-state=listening]::before,
#voiceOrb[data-state=listening]::after { content:''; position:absolute; inset:0;
  border-radius:50%; border:2px solid #0f766e; animation:ring 1.8s ease-out infinite; }
#voiceOrb[data-state=listening]::after { animation-delay:.6s; }
@keyframes ring { from { transform:scale(.6); opacity:.8 } to { transform:scale(1.9); opacity:0 } }
#voiceOrb[data-state=speaking] { animation:breathe 1s ease-in-out infinite; }
@keyframes breathe { 50% { transform:scale(1.1) } }
```

- **الدليل / proof:** `kosif-audit-studio/styles.css:823` · `kosif-audit-studio/app.js:2049`

#### VOICE-50 · نبض حلقة زر الميكروفون العائم · Live mic FAB ring pulse · 🟢 جاهز / ready
- **ماذا / what:** زر ميكروفون عائم بتدرج يطلق حلقة متسعة طوال الجلسة الحية. — A floating gradient mic button that emits an expanding ring while the session is live.
- **متى أستخدمها / when:** واجهات صوتية ولقطات منتج — voice UI and product shots.
- **كيف / how:** .voice-fab.live .voice-fab-ring { animation: voice-ring 1.6s ease-out infinite }. **أرقام / params:** FAB 60 px (KOSIF4 50 px); gradient 140deg #6d28d9 → #0f766e (KOSIF4 135deg #453556 → #395744); ring scale 1 → 1.7, opacity .8 → 0; hover −2 px, scale 1.03.
- **الدليل / proof:** `kosif-audit-studio/styles.css:810` · `kosif-audit-studio/studio.css:118`

#### VOICE-51 · التقاط ميكروفون نظيف · Clean mic capture constraints · 🟢 جاهز / ready
- **ماذا / what:** يُفتح الميكروفون بإلغاء الصدى وكبت الضوضاء والتحكم الآلي بالكسب. — The mic opens with echo cancellation, noise suppression and auto gain.
- **متى أستخدمها / when:** أي تسجيل من المتصفح — any in-browser capture.
- **كيف / how:** navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true, noiseSuppression:true, autoGainControl:true}}). For a VO take meant for the film, turn autoGainControl OFF (it pumps) and clean later with VOICE-39.
- **الدليل / proof:** `kosif-audit-studio/voice.js:259`

#### VOICE-52 · تسجيل الصوت وتنزيله · MediaRecorder capture + download · 🟢 جاهز / ready
- **ماذا / what:** مساعد صغير يسجل MediaStream إلى Blob ويطلق تنزيل الملف. — A small helper that records a MediaStream into a Blob and triggers a file download.
- **متى أستخدمها / when:** تسجيل تعليق المالك من المتصفح مباشرة — recording the owner's VO straight from the browser.
- **كيف / how:** createAudioRecorder(stream) → {start, stop(): Promise<Blob>}; downloadAudioBlob(blob, 'kosif-response.webm') revokes the object URL after 1000 ms. Convert to WAV with ffmpeg before sync work. **أرقام / params:** default mime audio/webm; revoke delay 1000 ms.
- **الدليل / proof:** `kosif-audit-studio/audio-export.js`

## الأخلاق والتكلفة — Ethics, rights & cost

_الصوت هوية. هذه قواعد لا تُكسر حتى لو طلبها نص مهمة._

#### VOICE-53 · لا تقليد لأصوات حقيقية · Never imitate real voices · 📄 موصوف / documented only
- **ماذا / what:** لا اسم شخص حقيقي ولا صوته ولا «بأسلوب فلان» في توليد الصوت أو الموسيقى؛ الاستنساخ بموافقة فقط، والإفصاح عن الصوت المصطنع حيث يلزم. — No real person's name, voice or 'in the style of' prompt for voice or music; clone only with consent; disclose synthetic voices where required.
- **متى أستخدمها / when:** قبل كل مهمة صوت — before every voice job.
- **كيف / how:** Describe timbre in words instead (deep, warm, slightly raspy, mid-40s, measured). Keep the consent record next to any cloned voice id.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music/references/RIGHTS.md` · `kosif-one/tools/kosif-omni/skills/kosif-voice/SKILL.md`

#### VOICE-54 · لا ادعاء بلا ملف · No audio claim without a receipt · 📄 موصوف / documented only
- **ماذا / what:** لا تقل إن الصوت وُلّد أو سُمع إلا ومعك ملف ومدة وجهارة مقاسة. — Never claim audio was rendered (or heard) without a file, a duration and a measured loudness.
- **متى أستخدمها / when:** في كل تقرير تسليم — every delivery report.
- **كيف / how:** Report: path, ffprobe duration, integrated LUFS, true peak, and words.json count. Style observations that say 'not listened to' stay labelled that way.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-voice/SKILL.md` · `kosif-tool/tools/verify_video.py`

#### VOICE-55 · نظافة تكلفة الحروف · TTS character-cost hygiene · 📄 موصوف / documented only
- **ماذا / what:** انزع markdown وHTML وخزّن الأسطر المكررة قبل الدفع بالحرف. — Strip markdown/HTML and cache repeated lines before paying per character.
- **متى أستخدمها / when:** أي مزود مدفوع — any paid provider.
- **كيف / how:** Pre-clean text; cache key sha256(voice:model:settings:text); re-render only changed lines (the Voice Director's selective re-render follows the same idea). **أرقام / params:** saves 5–15 % characters; 80–95 % cache hits on iterations.
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5516-elevenlabs-cost-tuning` · `kosif-atlas/skills/1847-elevenlabs-pack/5522-elevenlabs-performance-tuning`

## توليفات قوية / power combos

1. **فيلم عربي مروي بلا مفتاح / keyless Arabic narrated film:** VOICE-21 (كتابة) → VOICE-20 (نص النطق) → VOICE-01 (Piper) → VOICE-31 (المدة من الصوت) → VOICE-32 + VOICE-33 (words.json) → ترجمة كاريوكي عربية (ARAB-62 … ARAB-71) → VOICE-44 (−14 LUFS + البوابة). كل حلقة فيها جرت هنا.
2. **قراءة صوتية تعليمية / read-aloud lesson:** VOICE-01 + VOICE-32 → VOICE-35 (تظليل الكلمة المنطوقة) + كلمة كاملة RTL (ARAB-01) + عائلة الألوان (ورق كريمي #f4eee0).
3. **إعلان إطلاق بإيقاع موسيقي / launch film on a beat:** VOICE-06 أو VOICE-01 → VOICE-36 (آلة كاتبة على توقيت الصوت) → VOICE-43 (خفض الموسيقى ومعه ذروة الموسيقى في الوقفة) + عائلة الموسيقى والإيقاع للقطع على الضربة.
4. **محاضرة سبورة / whiteboard lecture:** VOICE-18 (ميزانية الكلمات) → VOICE-38 (عنصر مرسوم لكل جملة) + عائلة الرسم اليدوي draw-on + VOICE-34 (حركة في الوقفات > 1.5 ث).
5. **ريلز متحدث / talking-head reel:** VOICE-42 (عزل الصوت) → VOICE-39 (تنظيف) → VOICE-32 (توقيت) → ترجمة كاريوكي ASS (ARAB-62 …) → VOICE-44. هذا خط reel.py نفسه.
6. **قصة بشخصيات / character sketch:** VOICE-13 (حوار متعدد الأصوات) + VOICE-41 (زي صوتي واحد: مكالمة هاتفية داخل القصة) + عائلة الشخصيات والتحريك (مزامنة الفم على words.json).
7. **فيلم تاريخي على طريقة Vox / Vox history:** VOICE-27 (راوٍ مقفل < 20 كلمة لكل 10 ث) + VOICE-41 (صدى بكرة قديمة) + عائلة الملمس والحبيبات وعائلة الألوان (سيبيا).
8. **فيلم منتج صوتي / voice-product demo:** VOICE-49 (كرة الصوت) + VOICE-50 (حلقة الميكروفون) + VOICE-37 (موجة ورأس تشغيل) + عائلة الواجهات والأجهزة (UI داخل هاتف).
9. **Voice2Motion:** صوت المالك → VOICE-32 → `kosif-studio/motion/audio2motion.py` (مشاهد دلالية من الكلمات) → VOICE-44.

## أخطاء ممنوعة / never do

- **لا تمطّ الصوت ليناسب الحركة** (atempo/rubberband على التعليق) — يلطخ الحروف ويكسر الأداء؛ أعد التوليد بسرعة أخرى (VOICE-19) أو حرّك الصورة. Never time-stretch narration.
- **لا تعدّل صوت المستخدم المرفق ولا تعيد أخذ عيناته لمطابقة الصورة** — الصوت المرفق ساعة مقدسة (kosif-tool/playbooks/audio-sync.md). The user's audio is untouched.
- **لا تعرض نص ويسبر كما هو** — يقسم الكلمات العربية (محل+ين)؛ اعرض نصك واستعمل توقيته فقط (VOICE-33).
- **لا تصل MP3 بـ `-c copy`** — حشو المرمّز يزيح التوقيت عشرات المللي ثانية لكل وصلة (VOICE-45).
- **لا تقلد صوت شخص حقيقي ولا «بأسلوب فلان»** ولا تستنسخ دون موافقة موثقة (VOICE-53).
- **لا تقل «ولّدت الصوت» أو «سمعته» بلا ملف ومدة وLUFS** — كثير من ملاحظات الفيديو تقول «not listened»؛ أبقها كذلك (VOICE-54).
- **لا تستخدم Kokoro للعربية ولا نطق المتصفح لملف نهائي** — الأول بلا صوت عربي، والثاني يختلف حسب جهاز المشاهد ولا يُلتقط في الرندر.
- **لا تخلط لهجتين في كتلة واحدة** ولا تغيّر صوت الراوي بين المقاطع — صِف الصوت مرة وأقفله (VOICE-24, VOICE-27).
- **لا تكتب للعين** (أرقام وروابط واختصارات كما تُكتب) — المحرك يقرؤها حرفيًا (VOICE-20).
- **لا تصرف رصيدًا مدفوعًا بلا موافقة ومعاينة** — ولّد مسودة Piper أولًا لضبط الإيقاع، ثم المدفوع مرة واحدة (VOICE-55).
- **لا تكدّس زيين صوتيين** (هاتف + مكبر) — زي واحد في كل مرة (VOICE-41).

## أقوى 5 حركات توقيع / 5 signature moves

1. **الصوت أولًا ثم الفيلم / voice-first timeline** — VOICE-01 → VOICE-31: ولّد، قِس بـ ffprobe، وابنِ المشاهد على الطول الحقيقي. مُثبت هنا بـ 11/11.
2. **كلمة تُنطق = كلمة تتحرك / spoken word = moving word** — VOICE-32 + VOICE-33 + VOICE-35: words.json من صوتك، ابدأ كل حركة قبل الكلمة بـ 40–80 ms.
3. **ملاحظة الأداء قبل التوليد / performance note before render** — VOICE-12 + VOICE-20: JSON بالسرعة والطاقة والكلمات المشددة، ونص منطوق منفصل عن نص الشاشة.
4. **مزج يتنفس / a breathing mix** — VOICE-39 → VOICE-43 → VOICE-44: تنظيف، خفض الموسيقى ≈ 17 dB تحت الكلام، تسليم −14 LUFS.
5. **راوٍ مقفل الهوية / a locked narrator** — VOICE-27 + VOICE-24: صوت واحد ولهجة واحدة وجملة < 20 كلمة لكل مقطع، طوال الفيلم.
