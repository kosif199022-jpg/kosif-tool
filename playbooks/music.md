# Music and beat sync — الموسيقى والمزامنة الإيقاعية

This playbook covers films driven by music: BPM grids, cutting and accenting on beats, audio-reactive motion, lyric and poem films, ducking music under narration, and loudness delivery. Use it whenever a style's categories include `music`. Use only music the user provides or that is licensed for the use.

يغطي هذا الدليل الأفلام التي تقودها الموسيقى: شبكة الإيقاع، القطع والتأكيد على الضربات، الحركة المتفاعلة مع الصوت، أفلام الكلمات والقصائد، خفض الموسيقى تحت التعليق، ومستوى الجهارة عند التسليم. استخدم فقط موسيقى قدّمها المستخدم أو مرخّصة.

## 1. When to use — متى تستخدمه

Use when rhythm structures the film: launch teasers, showreels, lyric videos, beat-cut montages and any film whose pacing should feel musical.

**بالعربية:** عندما يبني الإيقاعُ الفيلم: إعلانات تشويقية، عروض أعمال، أفلام كلمات، مونتاج على الإيقاع.

## 2. Visual grammar — القواعد البصرية

- Map the song structure first (intro, verse, build, drop, outro) and give each section a visual mode.
- Strong beats (1 and 3 in 4/4) get cuts or big moves; weak beats get small accents (scale 2–4%, opacity flicker, colour change).
- The drop gets the boldest frame of the film; do not spend it earlier.

**بالعربية:** ارسم بنية المقطوعة أولًا وأعط كل قسم أسلوبًا بصريًا. الضربات القوية للقطع والحركات الكبيرة، والضعيفة للتأكيدات الصغيرة. لحظة الذروة لأقوى إطار في الفيلم.

## 3. Motion mechanics — ميكانيكا الحركة

- Beat period = 60 / BPM seconds (120 BPM → 500 ms). At 30 fps one beat is 15 frames; place cuts on the nearest frame and log the rounding.
- Measure beats, do not guess: use an onset/beat detector (e.g. `aubio`, `librosa.beat.beat_track`) or tap the tempo, then verify five beats by listening.
- Cut on the beat or 1 frame before it (the eye needs a frame to register); never 2+ frames late.
- Accent envelope: attack 1–2 frames, decay 150–300 ms with ease-out; scale pulse 1 → 1.04 → 1.
- Audio-reactive values (RMS, bands) are smoothed with a 100–200 ms window and clamped so motion never jitters.
- Lyric films: each line enters 80–120 ms before it is sung, holds while sung, exits within 200 ms after.

**بالعربية:** طول الضربة = 60 ÷ BPM ثانية. قِس الإيقاع بأداة كشف الضربات ولا تخمّن. اقطع على الضربة أو قبلها بإطار. تأكيد بهجوم 1–2 إطار وتلاشٍ 150–300 مللي ثانية. نعّم القيم المتفاعلة مع الصوت. سطر الكلمات يدخل قبل غنائه بـ 80–120 مللي ثانية.

## 4. Scene recipes — وصفات المشاهد

**A — Build and drop (التصاعد والذروة)**

| start | end | action | easing |
|---|---|---|---|
| bar 1 | bar 4 | cuts every 2 beats, camera push 1% per bar | linear |
| bar 5 | bar 7 | cuts every beat, scale pulses on weak beats | ease-out decay |
| bar 8 beat 4 | drop | 1 beat of black or silence frame | hard cut |
| drop | +2 bars | hero frame, biggest type, full colour | spring 14/160 |

**B — Lyric line (سطر غنائي):** line in on its sung onset − 100 ms (mask wipe 350 ms), stressed word pops on its syllable, line out 150 ms after the last word.

**C — Equalizer bars (أعمدة المعادل):** 24–48 bars from FFT bands, each smoothed 120 ms, mirrored for symmetry, height capped at 60% of frame.

**D — Beat-cut montage (مونتاج إيقاعي):** clips change on every strong beat, each clip trimmed to its most active 15 frames.

## 5. Implementation — التنفيذ

Remotion beat grid:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
export const BeatPulse: React.FC<{ bpm: number; offset: number; children: React.ReactNode }> = ({ bpm, offset, children }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const beat = (60 / bpm) * fps;
  const since = ((f - offset * fps) % beat + beat) % beat;          // frames since last beat
  const s = interpolate(since, [0, 2, 8], [1, 1.04, 1], { extrapolateRight: 'clamp' });
  return <div style={{ transform: `scale(${s})` }}>{children}</div>;
};
```

For audio-reactive work in Remotion use `useAudioData` + `visualizeAudio` from `@remotion/media-utils`. In the html-canvas starter, precompute an envelope JSON offline (e.g. RMS every 1/30 s with ffmpeg `astats` or Python) and read it by frame index, which keeps renders deterministic.

## 6. Arabic and RTL notes — ملاحظات العربية

Arabic lyric lines stay whole; emphasise a word by weight or colour, never by splitting letters. For Qur'anic recitation, nasheed or poetry, follow the reciter's pauses (waqf) rather than a beat grid, and avoid flashy effects.

**بالعربية:** سطر الكلمات العربي يبقى كاملًا والتأكيد بالوزن أو اللون. في التلاوة والأناشيد والشعر اتبع وقفات القارئ لا شبكة الإيقاع، وتجنّب المؤثرات الصاخبة.

## 7. Audio sync — المزامنة مع الصوت

Narration over music: duck the music 8–12 dB under voice with 150 ms attack and 400 ms release. Deliver at −14 LUFS integrated, true peak ≤ −1 dBTP, and check with `python3 tools/verify_video.py film.mp4 --lufs -14`.

**بالعربية:** اخفض الموسيقى 8–12 ديسيبل تحت الصوت، وسلّم بجهارة −14 LUFS وذروة ≤ −1 dBTP وافحص بـ `tools/verify_video.py`.

## 8. Quality checklist — قائمة الفحص

1. BPM measured and verified by ear?
2. Cuts on or 1 frame before beats?
3. Drop reserved for the strongest frame?
4. Reactive values smoothed, no jitter?
5. Lyric lines lead the voice by about 100 ms?
6. Music licensed or user-provided?
7. Voice intelligible over music?
8. −14 LUFS ±1.5 and true peak ≤ −1 dBTP?
9. Arabic lyric lines whole?
10. Ending lands on the final musical hit?

## 9. Anti-patterns — أخطاء شائعة

Everything pulsing on every beat; cutting late; waveform visualisers as filler; strobe flashes (also an accessibility risk: keep flashes under 3 per second); unlicensed music.

**بالعربية:** نبض كل شيء مع كل ضربة، القطع المتأخر، أشكال موجية كحشو، وميض متكرر (أكثر من 3 في الثانية خطر على المشاهدين)، وموسيقى غير مرخّصة.

## 10. Related styles — استايلات ذات صلة

- audio-wave — موجة صوت
- subtitle-punch — كلمات متحركة
- viral-mixed-media — مونتاج مختلط
- pm-samaote-5e2fc2 — Synced lyrics motion video
- pm-prasenx-8d9323 — Motion showreel with a fully code-synthesized soundtrack
- pm-macrohou-33959d — Ren app launch video
