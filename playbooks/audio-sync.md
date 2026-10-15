# Word-level audio sync pipeline — خط أنابيب المزامنة الصوتية على مستوى الكلمة

This playbook explains how a supplied voice-over becomes the master clock of a KOSIF film: transcription and alignment, the `words.json` format, tolerances, silence handling, music ducking, loudness delivery and verification. Read it whenever the user provides audio.

يشرح هذا الدليل كيف يصبح التعليق الصوتي المرفق الساعةَ الأساسية للفيلم: التفريغ والمحاذاة، صيغة `words.json`، حدود التسامح، التعامل مع الصمت، خفض الموسيقى، الجهارة عند التسليم والتحقق.

## 1. When to use — متى تستخدمه

Whenever the user attaches narration, a recitation, a song or a talking-head video.

**بالعربية:** كلما أرفق المستخدم تعليقًا صوتيًا أو تلاوة أو أغنية أو فيديو متحدث.

## 2. Visual grammar — القواعد البصرية

- The audio is never edited, stretched or resampled to fit the animation; the animation fits the audio.
- Every scene in PLAN.md has start/end times taken from the audio, rounded to frames.
- Captions show at most one phrase (a pause > 400 ms ends a phrase).

**بالعربية:** لا يُعدَّل الصوت ولا يُمطّ ليناسب الحركة؛ الحركة هي التي تناسب الصوت. كل مشهد في PLAN.md له بداية ونهاية من الصوت.

## 3. Motion mechanics — ميكانيكا الحركة

**Pipeline:**

1. Probe the file: `ffprobe -v error -show_entries format=duration -of csv=p=0 voice.mp3`. The film duration equals the audio duration (plus optional tail).
2. Transcribe with word timestamps: `whisper voice.mp3 --language ar --word_timestamps True --output_format json` (openai-whisper), or faster-whisper / WhisperX for forced alignment. If the user supplies the exact script, align it rather than trusting free transcription.
3. Convert to `words.json`: `python3 tools/words_convert.py voice.json words.json` (also accepts SRT, VTT, CSV). For the html-canvas starter, write `words.js` instead.
4. Correct the transcript text by hand where needed; keep the timings.
5. Animate: each word or element starts at `word.start − 0.04…0.08 s`.
6. Verify (section 7).

**Format:** `[{"word": "مرحبا", "start": 0.12, "end": 0.48}, ...]`, seconds as floats, sorted, non-overlapping.

**Tolerances:** key words (emphasis, names, numbers) ≤ 100 ms from speech onset; other words ≤ 150 ms; cuts on pauses, never mid-word.

**Silence:** pauses > 600 ms are scene-change opportunities; pauses > 1.5 s need visual movement (camera drift, ambient loop) so the frame does not die.

**بالعربية:** افحص مدة الملف، فرّغ بطوابع زمنية للكلمات (Whisper أو WhisperX)، وإن توفر النص فاستخدم المحاذاة القسرية. حوّل إلى `words.json` بـ `tools/words_convert.py`، صحّح النص يدويًا مع إبقاء التوقيت، وابدأ كل حركة قبل الكلمة بـ 40–80 مللي ثانية. التسامح ≤ 100 مللي ثانية للكلمات المهمة. الوقفة الأطول من 600 مللي ثانية فرصة لتغيير المشهد.

## 4. Scene recipes — وصفات المشاهد

**A — Narrated explainer (شرح بتعليق صوتي)**

| start | end | action | easing |
|---|---|---|---|
| phrase.start − 0.15 s | phrase.start | caption phrase fades in | ease-out |
| word.start − 0.06 s | word.end | word highlighted | outBack 140 ms |
| key word start | +0.3 s | matching visual pops | spring |
| phrase.end | +0.4 s | caption fades out | ease-in-out |

**B — Recitation or poem (تلاوة أو قصيدة):** one verse per screen, change on waqf/pause, slow cross-fades 600–900 ms, no bouncy effects.

**C — Talking head + captions (متحدث مع ترجمة):** keep the speaker's video untouched, captions in the bottom safe area, emphasis words enlarged.

## 5. Implementation — التنفيذ

Remotion with audio as master:

```tsx
import { Audio, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import words from '../public/words.json';
export const Synced: React.FC = () => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const i = words.findIndex((w) => t >= w.start - 0.06 && t < w.end);
  return (<>
    <Audio src={staticFile('voice.mp3')} />
    <div dir="rtl" style={{ fontSize: 64 }}>{words.map((w, k) => <span key={k} style={{ color: k === i ? '#7ee8d2' : '#fff' }}>{w.word} </span>)}</div>
  </>);
};
```

Set the composition's `durationInFrames = Math.ceil(audioSeconds * fps)`. With the html-canvas starter, render with `node tools/render_html.cjs --in index.html --out film.mp4 --audio voice.mp3`: the audio is muxed without resampling.

## 6. Arabic and RTL notes — ملاحظات العربية

Whisper may return Arabic words with attached punctuation or split clitics; merge them so each entry is a displayable word. Keep diacritics if the user's script has them. For Qur'anic text use the user's exact text, never the transcript.

**بالعربية:** قد يُرجع Whisper كلمات بعلامات ترقيم ملتصقة أو سوابق منفصلة؛ ادمجها لتصبح كل خانة كلمة قابلة للعرض. للنص القرآني استخدم نص المستخدم الدقيق لا التفريغ.

## 7. Audio sync — المزامنة مع الصوت

**Music under voice:** duck 8–12 dB with 150 ms attack, 400 ms release (ffmpeg `sidechaincompress` or keyframed volume).

**Loudness:** normalize the final mix to −14 LUFS integrated, true peak ≤ −1 dBTP: `ffmpeg -i mix.wav -af loudnorm=I=-14:TP=-1:LRA=11 out.wav` (two-pass for precision).

**Verify:** `python3 tools/verify_video.py film.mp4 --aspect 9:16 --fps 30 --duration <s> --audio voice.mp3` checks streams, duration, frame count, loudness and that the delivered audio length matches the master within 50 ms. Then spot-check sync at three timestamps per scene by watching with sound.

**بالعربية:** اخفض الموسيقى 8–12 ديسيبل تحت الصوت، وطبّع المزيج إلى −14 LUFS، ثم افحص بـ `tools/verify_video.py` وتحقق بالمشاهدة في ثلاث لحظات لكل مشهد.

## 8. Quality checklist — قائمة الفحص

1. Audio untouched (same duration as master ±50 ms)?
2. words.json sorted, non-overlapping, text corrected?
3. Key words within 100 ms?
4. No cut in the middle of a word?
5. Long pauses still have motion?
6. Music ducked under voice?
7. −14 LUFS ±1.5, true peak ≤ −1 dBTP?
8. verify_video passes?
9. Sync spot-checked at 3 points per scene?
10. Sacred or exact texts taken from the user's script?

## 9. Anti-patterns — أخطاء شائعة

Time-stretching the voice to fit animation; captions lagging the voice; whole paragraphs on screen; music louder than speech; trusting an uncorrected transcript for names and numbers.

**بالعربية:** مطّ الصوت ليناسب الحركة، ترجمة متأخرة عن الصوت، فقرات كاملة على الشاشة، موسيقى أعلى من الكلام، والثقة بتفريغ غير مصحح للأسماء والأرقام.

## 10. Related styles — استايلات ذات صلة

- subtitle-punch — كلمات متحركة
- kinetic-arabic — تايبوغرافي عربي
- audio-wave — موجة صوت
- pm-samaote-5e2fc2 — Synced lyrics motion video
- pm-sab8a-364a5a — Talking-head clip edit
