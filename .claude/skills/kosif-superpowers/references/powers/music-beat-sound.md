# الموسيقى والإيقاع والمؤثرات — Music, beat & sound

> فصل مُجمَّع آليًا من 303 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **294 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 294 powers deduplicated by name from 303 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 27 · 🟢 جاهز 59 · 📦 بأمر تثبيت 74 · 🔑 مفتاح/خدمة 20 · 👁 شوهد في فيديو 32 · 📄 موصوف 70 · 💡 فكرة 12

#### BEAT-01 · توحيد الجهارة بمرورين · Two-pass loudness normalisation · ✅ مُثبت هنا
- **ماذا / what:** Measure integrated loudness first, then apply the measured values linearly so the mix lands on target without pumping.
- **كيف / how:** pass1: -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - ; pass2: loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=..:measured_TP=..:measured_LRA=..:measured_thresh=..:linear=true,aresample=48000. AAC adds ~0.5 dB overshoot so aim TP -1.5 to measure ~-1 dBTP.
- **أرقام / params:** YouTube/social -14 LUFS ±1, TP ≤ -1 dBTP; broadcast EBU R128 -23; podcast -16
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/assembly-and-review.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/gotchas.md` · `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `100-superskills/skills/kosif-montage-motion/SKILL.md:201`

#### BEAT-02 · مؤثرات صوتية مصممة على الإشارات · Designed SFX on picture cues · ✅ مُثبت هنا
- **ماذا / what:** Ten synthesised effects placed at times the picture exports (contact frames, pops, settles).
- **كيف / how:** cues.json [{t, type, gain, pan}] → Score.cues
- **أرقام / params:** click 1900 Hz 50 ms; tick root×8 40 ms; pop chirp 500→1600 Hz 0.16 s; thump 70+90 Hz 0.4 s; whoosh band 400-5000 Hz 0.55 s (starts 0.12 s early); swish 1.5-9 kHz 0.22 s; chime bells root×4/×6; type 30 ms; boom; riser 1.5 s; 6 ms cos² tail; gain×0.6
- **الدليل / proof:** `kosif-studio/motion/score.py:148` · `kosif-studio/motion/projects/showreel/assets/cues.json` · `kosif-studio/motion/projects/bunny_twin/twin/cues.json` · `kosif-one/tools/kosif-studio/motion/score.py:146`

#### BEAT-03 · توقف الشريط وإقلاعه · Tape-stop / tape-start · ✅ مُثبت هنا
- **ماذا / what:** Pitch and tempo dive together to a halt then dead air; the restart spins up from zero into the next section.
- **كيف / how:** spec tape_stops_s [[t0, d]], tape_starts_s [[t0, d]]
- **أرقام / params:** read head Σ(1−u)^1.6, gain 1−u³; start gain √u; e.g. sound_ground stop 6.0 s/0.8 s, start 7.2 s/0.5 s; bunny stop 2.62/0.35
- **الدليل / proof:** `kosif-studio/motion/score.py:278` · `kosif-studio/motion/projects/sound_ground/assets/score.json` · `kosif-one/tools/kosif-studio/motion/score.py:1` · `kosif-one/tools/kosif-studio/motion/qa.py`

#### BEAT-04 · مؤثرات وحوار الرجل العصوي · Stickman foley + dialogue pacing · ✅ مُثبت هنا
- **ماذا / what:** Per-clip literal sound cues and one short line, with a dialogue speed gate.
- **كيف / how:** soundtrack per clip: soft steps/wind/cloth; shoe scuff/tap/paper; squeak/double step/cartoon pop; paper flutter/thud/silence; whoosh/tap/ending sting; clip 4 line 'Wait. What?'; gate < 2.5 words/s.
- **أرقام / params:** 2–4 SFX per clip; dialogue <2.5 w/s
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:33-34,51` · `fastify-motion-bro/skills/stickman/SKILL.md:13`

#### BEAT-05 · تصميم مؤثرات ميكانيكية · Mechanical foley design (car) · ✅ مُثبت هنا
- **ماذا / what:** Engine rise and tyre squeal on drift, tyre-air hiss, layered servo whooshes and metal separation ticks on expansion, small metallic clicks and low bass snap on reassembly, consistent room tone, no music.
- **كيف / how:** AUDIO section of car prompt 3.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/car-exploded.mjs:58`

#### BEAT-06 · مؤثرات الطعام الملموسة · Tactile food foley + tasting sounds · ✅ مُثبت هنا
- **ماذا / what:** Action-specific sounds (ice-on-glass clatter, wet sauce scrape, frying sizzle, cellophane crinkle) and 10 tasting-sound presets (crust crackle, straw slurp, fizzy sip, crispy crunch...).
- **كيف / how:** Each action pair carries its sound; SFX_EAT for final bite with generic fallback.
- **أرقام / params:** ~100 action sounds; 10 tasting presets
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/food-flow.mjs:4-28,34-45`

#### BEAT-07 · سياسات الصمت وعدم الموسيقى · Silent / no-music sound policies · ✅ مُثبت هنا
- **ماذا / what:** Per-mode audio rules: viral motion prompts no VO and no music; food has foley only; kinetic none or soft transition SFX; vox locked narrator; fitness coach voice.
- **كيف / how:** Encoded in each profile's prompt text and flags.
- **الدليل / proof:** `fastify-motion-bro/docs/PRODUCTION-GATES.md:10` · `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:43,115` · `fastify-motion-bro/scripts/viral-editorial.mjs:70`

#### BEAT-08 · مخطط ريلز الأغاني · Song reel planner (sections, excerpt, shot grid) · ✅ مُثبت هنا
- **ماذا / what:** For a song, sections are found from lyric gaps and loudness, a ~30 s excerpt is chosen on a downbeat around the loud refrain, a whole-frame shot grid cuts faster where loud, clips are assigned without repeats and kept in their section folder, lyric concepts map to stock-footage queries.
- **كيف / how:** songreel.sections_of(lines, dur, levels); choose_excerpt(… 30 s …) start ∈ downbeats, ≤32.5 s; shot_grid(spec, 30) durations .9–4.5 s, ≈1.4 s median when loud; assign(shots, clips); concepts_of(words) → SCENES keys; media_files prefers *.edit.mp4.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_songreel.py:27`

#### BEAT-09 · معايرة الصوت −14 LUFS · Loudness: −14 LUFS and BS.1770 meter · ✅ مُثبت هنا
- **ماذا / what:** Delivered mixes target −14 LUFS; the browser exporter has a BS.1770 meter (gated silence) and normalises with a −1.5 dB peak ceiling that wins on spiky content.
- **كيف / how:** offline.mjs measureLoudness(channels, sr) → lufs (1 kHz-ish sine at 1.0 in one channel = −3.01); normalizeLoudness(ch, sr, −14, −1.5) → {after, gainDb, limitedByPeak, peakDb}; timeline gate lufs −14 ±2.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/studio/offline.test.mjs:80` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:88` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:54`

#### BEAT-10 · خفض الموسيقى تحت الصوت · Music ducking under voice (sidechain) · ✅ مُثبت هنا
- **ماذا / what:** In the JSON timeline, music is ducked under clip speech with an FFmpeg sidechain compressor, with gain and fades.
- **كيف / how:** audio:{music:{src, gain −6, fade_in .3, fade_out .5}, keep_clip_audio:true, duck:'clips', lufs:−14} → graph contains sidechaincompress.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:74` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:91`

#### BEAT-11 · إزالة الصوت البشري بإلغاء المركز · Centre-cancel vocal removal (Audio Lab) · ✅ مُثبت هنا
- **ماذا / what:** A stereo track's centred voice is cancelled to keep the music bed (novoice mode); mono input is refused for music mode.
- **كيف / how:** audiolab.run(file, 'novoice'|'music', out) → {stereo, music_method, music, video}; test: 220 Hz centre band drops ≥ 4 dB.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py:48`

#### BEAT-12 · مكتبة مؤثرات CC0 داخل التايملاين · CC0 SFX kit in timelines · ✅ مُثبت هنا
- **ماذا / what:** Timeline specs can drop named kit sounds at times; default gain −10 dB; unknown names fail validation.
- **كيف / how:** audio:{sfx:[{src:'kit:reveal-1', at:.5}, {src:'kit:bell-1', at:1.2, gain:−6}]}; kit has ≥20 sounds (reveal-1..3, bell-1/2, bong, drop-1/2, click, select, glitch, card-place/slide, chips, key-1..6).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:65` · `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:104` · `100-superskills/skills/kosif-montage-motion/scripts/kit/sfx/LICENSE-SFX.md`

#### BEAT-13 · مسار الموسيقى · Soundtrack track · ✅ مُثبت هنا
- **ماذا / what:** One music file starts with the project and ends with the file or the project (no looping), with its own trim and level, mixed under clip sound.
- **كيف / how:** Add an audio asset with ＋ → project.soundtrack {assetId, trim, volume}; WebAudio gain per element during preview.
- **أرقام / params:** default volume 0.6
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:35` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:60` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/media.mjs:6`

#### BEAT-14 · كاشف الإيقاع · Beat tracker (numpy) · ✅ مُثبت هنا
- **ماذا / what:** Spectral-flux onsets, tempo by autocorrelation with a prior near 120, beat phase by comb, refined to onsets; returns bpm, beats, downbeats, hits.
- **كيف / how:** python motion.py beats TRACK.wav [--out beats.json] (qa.beats).
- **أرقام / params:** bpm range 70-180; hop 512, nfft 2048; measured 121.75 BPM on a 120 BPM synth test
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/qa.py:1`

#### BEAT-15 · نبضة الضربة · hitPulse punch envelope · ✅ مُثبت هنا
- **ماذا / what:** One shared attack/decay envelope for every punch, tick or kick so picture hits peak with their sound.
- **كيف / how:** MOTION.hitPulse(t - hitTime, attack, tau) -> 0..1; multiply into scale/brightness.
- **أرقام / params:** attack 2 frames (sine), tau 5 frames exponential at 60 fps; measured 1.00 at f2, 0.20 at f10; zero after attack+6·tau
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:47`

#### BEAT-16 · شبكة الإيقاع · Beat grid clock (beats) · ✅ مُثبت هنا
- **ماذا / what:** One clock shared by picture and sound: beat times from a BPM or from a measured beats JSON.
- **كيف / how:** const B = MOTION.beats(120, offset) -> B.at(n), B.len(n), B.beat; or MOTION.beats(json from motion.py beats) with downbeats/hits.
- **أرقام / params:** default downbeat every 4 beats when not measured
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:90`

#### BEAT-17 · كاشف الموسيقى الخلفية · Music-bed detector · ✅ مُثبت هنا
- **ماذا / what:** Decides whether a clip already carries music by listening to the gaps between words (or the quiet floor when gaps are absent), so no competing track is added.
- **كيف / how:** reel.has_music_bed(raw.wav, words)
- **أرقام / params:** gaps >0.18 s (±0.04 s trim, >80 ms); all gaps < −60 dBFS → no bed; ≥3 gaps → median > −42 dBFS; else 100 ms floor p10 > −40 dBFS
- **الدليل / proof:** `kosif-studio/motion/reel.py:57` · `kosif-studio/tests/test_studio.py:882`

#### BEAT-18 · ضبط الجهارة · Loudness mastering (−14 LUFS) · ✅ مُثبت هنا
- **ماذا / what:** Normalises to streaming loudness and catches AAC overshoot with a limiter; the composition mux uses a two-pass linear loudnorm because one-pass overshot short films.
- **كيف / how:** loudnorm + alimiter in montage/reel; two-pass in motion.mux_audio
- **أرقام / params:** loudnorm I=−14 TP=−1.5 LRA=11 + alimiter limit 0.84 (≈ −1.5 dBFS) attack 3 release 60; mux I=−14 TP=−1 linear=true
- **الدليل / proof:** `kosif-studio/motion/montage.py:203` · `kosif-studio/motion/motion.py:390`

#### BEAT-19 · قنوات الصوت لكل إطار · Per-frame sound channels · ✅ مُثبت هنا
- **ماذا / what:** Turns a track into animation curves one value per frame: loudness, bass/mid/high bands, onset strength, kicks, onsets, brightness, silence, tape-stop dive/rise, playback speed and a tape clock; plus a magma spectrogram and a height map image.
- **كيف / how:** python motion.py channels AUDIO [--fps 30 --out X.channels.json --bpm N]; MOTION.channels(ch) in pages
- **أرقام / params:** bands 20-160 / 160-2000 / 2000-12000 Hz; nfft 4096; kick low-flux >0.42 ≥0.18 s apart; onset >0.35 ≥0.06 s; silence rms<0.04; dive/rise >30 st/s or slope >15 with r²>0.9 held ≥4 frames; stop −1.6/fps, start +2.2/fps
- **الدليل / proof:** `kosif-studio/motion/qa.py:448` · `kosif-studio/tests/test_studio.py:719`

#### BEAT-20 · متتبع الإيقاع · Beat tracker (numpy only) · ✅ مُثبت هنا
- **ماذا / what:** Spectral-flux onsets → tempo by autocorrelation with a gentle prior near 120 BPM → beat phase by comb → beats snapped to onset peaks; downbeats from the strongest of four phases; strong hits listed.
- **كيف / how:** python motion.py beats TRACK.wav [--out beats.json]
- **أرقام / params:** hop 512, nfft 2048, 22.05 kHz mono; 70-180 BPM; prior σ 0.9 octave around 120; hits flux >0.35 ≥90 ms apart; measured 120.71 BPM on a 120 BPM synthetic score here
- **الدليل / proof:** `kosif-studio/motion/qa.py:304` · `kosif-studio/tests/test_studio.py:667`

#### BEAT-21 · مؤلف موسيقى على شبكة الإيقاع · Beat-grid score synthesiser · ✅ مُثبت هنا
- **ماذا / what:** Writes an original track in beats from a JSON spec (sections, chords, drops, risers, booms, end bell, tape stops), with buses, stems and seeded randomness — no samples, no downloads.
- **كيف / how:** python score.py out.wav --spec score.json [--cues cues.json --stems DIR] | --bpm 120 --seconds 15 --key A --scale minor --mood launch|calm --seed 7
- **أرقام / params:** 48 kHz stereo; scales minor, major, dorian, hijaz, pentatonic, lydian; roman chords i-vii; kick four|half; clap beats 2&4; hats 8th (0.35) + 16th ghost (0.14) panned ±0.3; bass every half beat; pad per chord; pluck 8ths, lead quarters
- **الدليل / proof:** `kosif-studio/motion/score.py:1` · `kosif-studio/motion/score.py:221` · `kosif-studio/tests/test_studio.py:667`

#### BEAT-22 · وصفات الآلات المركبة · Synth instrument recipes · ✅ مُثبت هنا
- **ماذا / what:** Closed-form drum and tone voices used by the score.
- **كيف / how:** score.kick/clap/hat/sub/pluck/bell/pad/riser/boom
- **أرقام / params:** kick 46+110·e^(−t/32 ms) Hz, decay 0.22 s, tanh 1.7; clap bursts at 0/9/19 ms band 900-3200 Hz + 90 ms tail; hat 6.5-15 kHz decay 11 ms (open 70 ms); sub sine + 0.22·2nd; pluck 13 partials k^−0.9 decay 2+0.9k; FM bell ratio 3.5 index 2.2; pad 3 detuned saws ±0.45-0.52 % LP 1500 Hz attack 0.6 s; rise…
- **الدليل / proof:** `kosif-studio/motion/score.py:70`

#### BEAT-23 · قناة المزج · Score mix bus · ✅ مُثبت هنا
- **ماذا / what:** Kick-driven pumping on bass and music, music dip under SFX, per-bus gains, short seeded room reverb, soft clip and end fade; stems optional.
- **كيف / how:** Score.mix(path, stems, silences, stops, starts)
- **أرقام / params:** duck bass/music 55 %; music −30 % under SFX (~3 dB); gains kick .9 perc .7 bass .75 music .7 fx .6 sfx .85; reverb 1.6 s noise IR τ 0.45 s wet 0.35; stop sections ×0.04; tanh 1.3 → 0.89 peak; 10 ms fade
- **الدليل / proof:** `kosif-studio/motion/score.py:299`

#### BEAT-24 · مواصفات موسيقى المشاريع · Project score specs (templates) · ✅ مُثبت هنا
- **ماذا / what:** Ready JSON scores and cue sheets from shipped films to copy or adapt.
- **كيف / how:** score.py out.wav --spec P/assets/score.json --cues P/assets/cues.json
- **أرقام / params:** showreel 120 BPM D minor seed 11 two stops + riser 12-16 + boom 16; lab 96 BPM D minor; sound_ground 120 D minor tape stop; bunny 120 E major chords I-vi-IV-V
- **الدليل / proof:** `kosif-studio/motion/projects/showreel/assets/score.json` · `kosif-studio/motion/projects/lab_rabbit_lion/assets/score.json` · `kosif-studio/motion/projects/sound_ground/assets/score.json`

#### BEAT-25 · مولد الأصوات المحيطة · Ambience synthesiser · ✅ مُثبت هنا
- **ماذا / what:** Seeded stereo beds keyed to seconds: sea swell, wind, slow pad chords, rain with droplets, thunder roll, whooshes, dawn birdsong, water plinks and a brook.
- **كيف / how:** python ambience.py out.wav --seconds 17 --rain 9.6:12.8 --thunder 10.6 --whoosh 0.6,15.3 --chords 0:A,6:F,12.6:C [--birds t0:t1 --sea 1.0 --drops t,t --brook t0:t1 --seed 7]
- **أرقام / params:** 44.1 kHz; sea LP 320 Hz swell 0.11 Hz level 0.22; wind band 300-1400 Hz 0.07 Hz 0.07; pad partials 1/1.5/2/2.5/3 detune ±0.3-0.4 Hz attack 1.8 s; rain HP 2.5 kHz + 90 ticks/s; thunder brown noise LP 120 Hz τ 0.9 s 2.6 s; whoosh 0.6 s; birds FM 2.2-4.8 kHz 2.2 phrases/s; plink 900-1800 Hz rising τ 45…
- **الدليل / proof:** `kosif-studio/motion/ambience.py:73` · `kosif-studio/tests/test_studio.py:572`

#### BEAT-26 · سياسات الصوت والموسيقى · Music/SFX policy presets · ✅ مُثبت هنا
- **ماذا / what:** Request presets: keep (voice untouched), music (licensed only, ducked under voice, -14 LUFS), sfx (short accents on key moments only), silent.
- **كيف / how:** kosif.py prompt --audio keep|music|sfx|silent|<free text>
- **أرقام / params:** -14 LUFS
- **الدليل / proof:** `kosif-tool/tools/kosif.py:74` · `kosif-tool/web/generator.js`

#### BEAT-27 · قياس الجهارة EBU R128 · EBU R128 loudness measurement · ✅ مُثبت هنا
- **ماذا / what:** Integrated LUFS, LRA and true peak parsed from ffmpeg ebur128=peak=true.
- **كيف / how:** verify_video loudness() or ffmpeg -af loudnorm=I=-14:TP=-1:LRA=11:print_format=summary
- **أرقام / params:** target -14 LUFS, TP ≤ -1
- **الدليل / proof:** `kosif-tool/tools/verify_video.py:33` · `kosif-tool/templates/TEST_REPORT.md`

#### BEAT-28 · أرض من طيف الصوت · Spectrogram canyon ground · 🟢 جاهز
- **ماذا / what:** The soundtrack's spectrogram displaced into a canyon: bass glows as a lava river, harmonics rise as ridges, a playhead traces what is heard, scrolling on the tape clock.
- **كيف / how:** motion.py channels -> spectrum_height.png; K3.makeSpectrumGround(texture, {width, depth, seconds, window, amp, glow, lava}); userData.set(t, tape, kick, head). Use K3.spectrumOnTape(img, ch) to resample onto tape time.
- **أرقام / params:** 60x30, 480x240 segs; window 4 s; amp 6; glow 1.2; lava threshold .62; light #ff9a6a fill #2a1a4a rock #1a1216; magma ramp 7 stops
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:804` · `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:862` · `100-superskills/skills/kosif-montage-motion/scripts/qa.py:455` · `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:804`

#### BEAT-29 · استخراج طاقة الترددات لكل إطار · Per-frame FFT band extraction · 🟢 جاهز
- **ماذا / what:** Decode audio, slide a large FFT window per video frame, and normalize per-band energies to 0-1 for animation data.
- **كيف / how:** ffmpeg decode to mono PCM 44.1kHz -> numpy; window 4096 samples (~10.8Hz/bin) centered on each frame (1470 samples per frame at 30fps would be too coarse for bass); log-spaced bands (8-16); normalize each band across the track; output {fps,totalFrames,frames:[{rms,bands[]}]}. Write our own script; numpy+ffmpeg exist here.
- **أرقام / params:** FFT 4096; 30fps; 8-16 bands
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/scripts/extract-audio-data.py` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/audio-reactive.md`

#### BEAT-30 · عناصر تتفاعل مع الصوت · Audio-reactive UI accents · 🟢 جاهز
- **ماذا / what:** Logo pulses on bass, CTA glow on treble, background breathes with amplitude, sampled per frame from precomputed bands; no spectrum bars.
- **كيف / how:** Precompute per-frame FFT bands to JSON (numpy+ffmpeg, both available here) then per-frame gsap.set/ CSS vars at f/fps.
- **أرقام / params:** fft window 4096 @44.1kHz; 16 bands at 30fps; text/logo scale <= 1+0.04*bass (<=5%), glow <= 30% (treble*24px drop-shadow); backgrounds 10-30%
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/2702-hyperframes/10377-gsap/scripts/extract-audio-data.py` · `kosif-atlas/skills/2702-hyperframes/10377-gsap/references/effects.md`

#### BEAT-31 · قائمة قطع تلقائية من المازورات وذروات الحركة · Auto edit list from bars and motion peaks · 🟢 جاهز
- **ماذا / what:** Find the song's bar lines, pick the busiest moments of the footage by measured motion, and lay one shot per bar (title card one bar, end card on the remainder); a sync check requires the picture to change within one frame of each sound onset.
- **كيف / how:** Locally: numpy onset/tempo estimation on the music, ffmpeg scene/motion scores (select='gt(scene,x)' or frame-difference energy) on footage, write an EDL JSON, render; 9:16 version places the whole frame over a blurred fill rather than cropping action.
- **أرقام / params:** 1 shot per bar; sync tolerance 1 frame
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/SKILL.md` · `kosif-atlas/skills/1511-homie/3903-video/references/TRAILER.md`

#### BEAT-32 · القص على حدود المازورة · Bar-grid cutting · 🟢 جاهز
- **ماذا / what:** Cut every shot on bar lines of the music: title card 1 bar, shots 1 bar each, end card on the remainder.
- **كيف / how:** bar_s = beatsPerBar*60/bpm; shot boundaries at k*bar_s + offset; requires known BPM or detection.
- **أرقام / params:** 120BPM 4/4 -> 2.0s bar
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video` · `kosif-atlas/skills/1511-homie/3892-music/references/COMPOSITION.md`

#### BEAT-33 · مستويات علو المؤثرات · SFX loudness tiers · 🟢 جاهز
- **ماذا / what:** Level SFX by max momentary loudness into tiers so a set sits in a mix without rebalancing.
- **كيف / how:** Big -9/-10, actions -11/-14, frequent -15/-17, UI -15/-19 LUFS-M; or loudest-50ms classes ui -20, small -16, normal -12, big -9 dB; ceiling -1 dBFS.
- **أرقام / params:** see params
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/sfx-design.md`

#### BEAT-34 · حلقات سلسة بالرندر الثلاثي · Seamless loops render-three-keep-middle · 🟢 جاهز
- **ماذا / what:** Render a section three times back-to-back and keep the middle so reverb/echo tails are already in its head; or wrap tail onto start.
- **كيف / how:** numpy concatenation; frequencies multiples of 1/loop length; check seam_ratio <1.5 (good <0.5).
- **أرقام / params:** 8s loop -> 0.125Hz
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound` · `kosif-atlas/skills/1511-homie/3901-sound/references/TRAPS.md` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/mixing-and-loops.md`

#### BEAT-35 · تنفس الإيقاع مع الطبلة · Kick-pump duck · 🟢 جاهز
- **ماذا / what:** Pads/bass dip on every kick and recover within half a beat for breathing groove.
- **كيف / how:** duck 0.35-0.5 per instrument in score.
- **أرقام / params:** duck 0-0.95
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound/references/SCORE.md` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural`

#### BEAT-36 · توهج متفاعل مع الصوت · Audio-reactive glow and scale · 🟢 جاهز
- **ماذا / what:** Bass drives scale, treble drives glow/textShadow of captions or shapes.
- **كيف / how:** Precompute bands per frame (fps 30, 8 bands) to JSON; scale=1+bass*0.06; textShadow blur=treble*12px alpha treble*0.4; backgrounds can swing 10-30%.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/audio-reactive.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/dynamic-techniques.md`

#### BEAT-37 · قص تريلر على البار · Beat-mapped trailer cuts · 🟢 جاهز
- **ماذا / what:** Beat sheet -> cue/bar map from BPM -> EDL -> render shots -> assemble; overlays are pure functions of frame.
- **كيف / how:** Bars 1-based; fx timing in beats; flash peak 0.35 soft fades; slow-mo never slows graphics.
- **أرقام / params:** flash peak 0.35
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/SKILL.md`

#### BEAT-38 · أعمدة الطيف الصوتي · Audio spectrum bars · 🟢 جاهز
- **ماذا / what:** Frequency bands drawn as bars, rings or glows driven by pre-analysed audio, a chart-like visualizer synced to the user's music or voice.
- **كيف / how:** Pre-compute per-frame RMS and band energies from the audio (ffmpeg or WebAudio offline), store as JSON, read by frame in the page. Smooth with prev*s + raw*(1-s). Layout: horizontal bass-left treble-right, vertical bass-bottom, or circular starting at 12 o'clock clockwise. Bass drives scale/glow, treble drives shimmer, RMS drives background energy; animate only 2-3 properties; keep minimums above zero.
- **أرقام / params:** bands 4/8/16/32 (8 = basic spectrum, 16 default); smoothing 0.25 (0.1-0.2 snappy, 0.3-0.5 flowing)
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/references/effects.md` · `kosif-atlas/skills/2760-charly-tools/10938-songsee/SKILL.md`

#### BEAT-39 · أهداف ارتفاع الصوت للموسيقى المولدة · Loudness mastering targets for generated music · 🟢 جاهز
- **ماذا / what:** Master generated songs with two-pass loudness normalisation and a limiter, then measure.
- **كيف / how:** ffmpeg loudnorm two-pass + limiter; measure with ebur128=peak=true; web/streaming −14 LUFS integrated, −1 dBTP; music bed under SFX −18 LUFS, −1.5 dBTP.
- **أرقام / params:** −14 LUFS/−1 dBTP; −18 LUFS/−1.5 dBTP
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music`

#### BEAT-40 · حلقة موسيقية سلسة على حدود الموازير · Bar-aligned seamless music loop · 🟢 جاهز
- **ماذا / what:** Cut a loop exactly on measured bar lines and crossfade tail into head so a short video can loop invisibly.
- **كيف / how:** Choose e.g. 8 bars from bar 4, crossfade the tail into the head, verify the jump at the wrap against normal sample steps and the beat grid over three plays; deliver WAV/OGG, never MP3 (encoder padding breaks the loop).
- **أرقام / params:** 8 bars; WAV/OGG
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music`

#### BEAT-41 · موجة أعمدة تتفاعل مع الميكروفون · Mic-reactive bar waveform (canvas) · 🟢 جاهز
- **ماذا / what:** Canvas visualiser of 48 rounded bars: while listening, bar height follows live mic RMS with a moving sine shimmer; while the assistant speaks, a synthetic sine wave animates; quiet mode draws flat bars.
- **كيف / how:** requestAnimationFrame(drawWave); colour from CSS var --primary (speaking) or --accent; ctx.roundRect per bar; alpha .25 + wobble*.75.
- **أرقام / params:** canvas 600x72 (CSS 56px tall); 48 bars, bar width gap*.5, radius 3, min height 3px; t = Date.now()/220; speaking wobble (sin(t+i*.55)+1)/2*.55+.1; listening level*(0.4+|sin(i*.7+t)|*.9)+.04; quiet .08
- **الدليل / proof:** `kosif-audit-studio/app.js:2064` · `kosif-audit-studio/styles.css:836`

#### BEAT-42 · مقياس مستوى الميكروفون · Mic level meter (AnalyserNode RMS) · 🟢 جاهز
- **ماذا / what:** Live input level 0..1 for driving a VU bar or reactive animation.
- **كيف / how:** AudioContext + createMediaStreamSource -> AnalyserNode fftSize 256; getByteTimeDomainData; RMS of (v-128)/128; level=min(1,rms*4).
- **أرقام / params:** fftSize 256; gain x4
- **الدليل / proof:** `kosif-earth-ci-fork/ui/audit/classic/voice.js:166` · `kosif-earth-ci-fork/ui/audit/classic/voice.js:368`

#### BEAT-43 · صفارة تأكيد Web Audio · Web Audio confirmation beep · 🟢 جاهز
- **ماذا / what:** Short synthesised sine blip for scan/confirm feedback without audio files.
- **كيف / how:** beep(freq=880,dur=.12): OscillatorNode sine; gain .15 at start, exponentialRampToValueAtTime(.001, t+dur).
- **أرقام / params:** default 880 Hz / 120 ms; used 740 Hz/100 ms and 960 Hz/150 ms
- **الدليل / proof:** `kosif-earth-ci-fork/ui/features/enterprise.js:21`

#### BEAT-44 · مسار إشارات المؤثرات · SFX cue track (cues only) · 🟢 جاهز
- **ماذا / what:** Editorial scenes carry SFX timing cues (paper whoosh, subtle UI click, light mechanical thud), not generated audio.
- **كيف / how:** sfx field per scene in motion prompts and storyboard.
- **أرقام / params:** 3 cue types
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs:69,90` · `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:40`

#### BEAT-45 · كوسف: توليد موسيقى ومحيط صوتي إجرائيا · KOSIF: procedural score and ambience synthesis · 🟢 جاهز
- **ماذا / what:** numpy-only deterministic soundtrack on the beat grid (kick, clap, hat, bass, pad, riser, boom, contact SFX) and ambience (sea, wind, rain, thunder, whoosh, chords, birds, brook) with seeds; not in the vendor skills (which source/generate via HeyGen/Lyria/MusicGen).
- **كيف / how:** python3 scripts/score.py out.wav --spec score.json --cues cues.json [--bpm --key --scale --mood --seed]; python3 scripts/ambience.py out.wav --seconds N --rain t0:t1 --thunder t --whoosh t1,t2 --chords 0:A,6:F.
- **الدليل / proof:** `100-superskills/skills/hyperframes-animation-studio/scripts/score.py` · `100-superskills/skills/hyperframes-animation-studio/scripts/ambience.py`

#### BEAT-46 · مونتاج على الإيقاع · Beat-planned montage · 🟢 جاهز
- **ماذا / what:** Shot plan of quick (~1 s) and breathing (~3 s) shots cut on beats, most active window per clip, fill crop, decaying zoom punches on downbeats (2x supersampled), grade, ducking, captions; takes folders/photos, blurred-bg for landscape in vertical.
- **كيف / how:** python scripts/kmotion.py montage a.mp4 b.mp4|FOLDER --music track.wav --out M.mp4 [--grade teal_orange --no-punch]
- **أرقام / params:** ratios 9:16 1080x1920, 16:9, 1:1, 4:5 1080x1350
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### BEAT-47 · موسيقى مولدة على الإيقاع · score synthesised music on beat grid · 🟢 جاهز
- **ماذا / what:** Original score: kick/clap/hats/sub/pad/pluck/lead, risers, booms, tape stops, designed SFX from cues.
- **كيف / how:** python scripts/kmotion.py score out.wav --spec score.json
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:201` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### BEAT-48 · أجواء صوتية مولدة · ambience synthesis · 🟢 جاهز
- **ماذا / what:** Rain, sea, birds, brook, chords, whoosh, drops.
- **كيف / how:** python scripts/kmotion.py ambience [--sea 0 --drops --brook]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:201` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### BEAT-49 · تحليل الإيقاع والقنوات · beats / channels analysis · 🟢 جاهز
- **ماذا / what:** Track → beat grid, or per-frame JSON (beats, kicks, onsets, rms, bass/mid/high, centroid, silence, pitch dive/rise, tape) + spectrogram.
- **كيف / how:** python scripts/kmotion.py beats TRACK; channels TRACK
- **أرقام / params:** tape stop: pitch line r²>0.9 >15 st/s or spectrum shift >30 st/s over 0.25 s held ≥4 frames
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:201` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### BEAT-50 · مكتبة المؤثرات · SFX kit 20 CC0 cues · 🟢 جاهز
- **ماذا / what:** bell-1/2, bong, card-place, card-slide, chips, click, drop-1/2, glitch, key-1..6, reveal-1/2/3, select; cue at motion start.
- **كيف / how:** python scripts/kmotion.py sfx; timeline audio.sfx [{src:'kit:reveal-1',at:0.4,gain:-10}]
- **أرقام / params:** catalog.json brightness/HF risk
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:201` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### BEAT-51 · تحليل الصوت · Audio analysis · 🟢 جاهز
- **ماذا / what:** LUFS, peaks, BPM.
- **كيف / how:** python scripts/kmotion.py scripts/omni/audio_analyze.py
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:201` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md`

#### BEAT-52 · شبكة الإيقاع · Beat grid (beats) · 🟢 جاهز
- **ماذا / what:** One clock for picture and sound: beat times from a BPM or from the beats JSON written by motion.py beats.
- **كيف / how:** MOTION.beats(bpm, offset) or beats(json) -> {at(n), len(n), bpm, beat, list, hits, downbeats (every 4th)}; place tweens at b.at(n).
- **أرقام / params:** beat = 60/bpm s; downbeats default every 4 beats
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:90` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py:546`

#### BEAT-53 · قنوات الصوت كمحرك للحركة · Audio channels as animation drivers · 🟢 جاهز
- **ماذا / what:** Per-frame sound features (rms, bass/mid/high, onsets, kicks, beats, silence, tape clock) interpolated at any t to drive visuals.
- **كيف / how:** python motion.py channels TRACK.wav -> JSON; in page MOTION.channels(json): ch.v('bass',t), ch.kick(t), ch.onset(t), ch.beat(t), ch.tape(t), ch.silent(t), ch.near('onsets',t,0.05).
- **أرقام / params:** fps 30 default; kick attack 1 tau 5; onset 1/4; beat 1/6; silent when silence>0.5
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:97` · `100-superskills/skills/kosif-montage-motion/scripts/qa.py:455`

#### BEAT-54 · مكتبة مؤثرات صوتية · CC0 UI sound-effects kit (20 sounds) · 🟢 جاهز
- **ماذا / what:** Short reveal, bell, drop, click, glitch, card and keyboard sounds with use notes, brightness and high-frequency risk.
- **كيف / how:** Timeline JSON audio.sfx: [{src:'kit:reveal-1', at:0.4, gain:-10}]; list with python scripts/launch.py sfx (kmotion sfx).
- **أرقام / params:** 44.1 kHz; reveal-1/2/3 .18/.14/.15 s; bell-1 1.48 s; bell-2 .65 s; bong .12 s; drop-1/2 .11/.19 s; click .01 s; select .05 s; glitch .03 s; card-slide .60 s; card-place .69 s; chips .26 s; key-1..6 .25 s mono wav
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/sfx/catalog.json` · `100-superskills/skills/kosif-montage-motion/scripts/kit/sfx/LICENSE-SFX.md` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:275`

#### BEAT-55 · مواصفة موسيقى إجرائية على شبكة الإيقاع · Procedural score spec (beat-grid music) · 🟢 جاهز
- **ماذا / what:** Original music is written as a small JSON spec: tempo, key, scale, sections (in beats) with kick pattern, hats, clap, bass, pad and pluck/lead scale-degree patterns, a chord progression in Roman numerals, risers, booms, tape stops/starts and the end time.
- **كيف / how:** kmotion score out.wav --spec score.json [--cues cues.json] [--seconds N]; spec keys bpm, seconds, key, scale, seed, sections[{from,to,kick:'four'|'half',hats,clap,bass,pad,pluck:[deg|null…],lead,stop}], chords[[beat,'i'|'VI'…]], risers[[a,b]], booms[t], end_s, tape_stops_s[[t,len]], tape_starts_s[[t,len]].
- **أرقام / params:** showreel 120 BPM D minor i–VI–iii–VII–i; bunny 120 BPM E major I–vi–IV–V tape stop 2.62 s/.35; lab 96 BPM D minor i–VI–III–VII; sound_ground tape stop 6.0 s/0.8 + start 7.2 s/0.5
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/assets/score.json:1` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/twin/score.json:1` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/assets/score.json:1`

#### BEAT-56 · ورقة مؤثرات صوتية متزامنة مع الصورة · SFX cue sheet synced to picture · 🟢 جاهز
- **ماذا / what:** Sound effects are listed with time, type, gain and stereo pan and mixed into the score at render, one hit per visual event.
- **كيف / how:** cues.json [{t, type: whoosh|tick|thump|boom|pop|swish|chime|click|type, gain 0.5–1.0, pan −0.4…0.3}]; passed as --cues to kmotion score; e.g. bunny: whoosh .08, five panned ticks .92–1.32, thump 1.68, boom+pop 2.66 (the break), swish 3.47, chime 3.68.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/twin/cues.json` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/assets/cues.json` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/assets/cues.json`

#### BEAT-57 · قنوات تحليل الصوت لكل إطار · Per-frame audio analysis channels · 🟢 جاهز
- **ماذا / what:** A track is analysed into per-frame channels and event lists that any visual can read: beats, downbeats, kicks, onsets, RMS, bass/mid/high bands, spectral centroid, silence, pitch dive/rise, playback speed and a tape clock, plus a spectrogram and a height image.
- **كيف / how:** kmotion channels audio.wav → score.channels.json {fps 30, frames, seconds, bpm, beats[], downbeats[], kicks[], onsets[], rms[], bass[], mid[], high[], onset[], centroid[], silence[], pitch_dive[], pitch_rise[], speed[], tape[]} + spectrogram.png (RGB) + spectrum_height.png (gray); in page C = M.channels(ch): C.kick(t,1,6), C.onset(t,1,3), C.v('bass',t), C.silent(t), C.tape(t).
- **أرقام / params:** showreel: 452 frames, bpm 120.45, 31 beats, 25 kicks, 68 onsets
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/assets/score.channels.json` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/channels.json` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:14`

#### BEAT-58 · ملفات صوت الخلفية والموسيقى · Ambient bed and score audio files · 🟢 جاهز
- **ماذا / what:** Projects carry short rendered stereo beds: an ocean ambience and generated 5 s scores.
- **كيف / how:** night_boat/assets/ambience.wav (stereo 16-bit 44.1 kHz 5.0 s, kmotion ambience); five_sec and bunny_twin assets/score.wav (stereo 16-bit 48 kHz 5.05 s, different content).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/assets/ambience.wav` · `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/assets/score.wav` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/assets/score.wav`

#### BEAT-59 · مقام minor · Score scale minor · 🟢 جاهز
- **ماذا / what:** Synth score scale 'minor' for the numpy soundtrack generator.
- **كيف / how:** score.py out.wav --bpm 120 --seconds 15 --key A --scale minor --mood launch
- **أرقام / params:** 0 2 3 5 7 8 10
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/score.py:37`

#### BEAT-60 · مقام major · Score scale major · 🟢 جاهز
- **ماذا / what:** Synth score scale 'major' for the numpy soundtrack generator.
- **كيف / how:** score.py out.wav --bpm 120 --seconds 15 --key A --scale major --mood launch
- **أرقام / params:** 0 2 4 5 7 9 11
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/score.py:37`

#### BEAT-61 · مقام dorian · Score scale dorian · 🟢 جاهز
- **ماذا / what:** Synth score scale 'dorian' for the numpy soundtrack generator.
- **كيف / how:** score.py out.wav --bpm 120 --seconds 15 --key A --scale dorian --mood launch
- **أرقام / params:** 0 2 3 5 7 9 10
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/score.py:37`

#### BEAT-62 · مقام hijaz · Score scale hijaz · 🟢 جاهز
- **ماذا / what:** Synth score scale 'hijaz' for the numpy soundtrack generator.
- **كيف / how:** score.py out.wav --bpm 120 --seconds 15 --key A --scale hijaz --mood launch
- **أرقام / params:** 0 1 4 5 7 8 10
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/score.py:37`

#### BEAT-63 · مقام pentatonic · Score scale pentatonic · 🟢 جاهز
- **ماذا / what:** Synth score scale 'pentatonic' for the numpy soundtrack generator.
- **كيف / how:** score.py out.wav --bpm 120 --seconds 15 --key A --scale pentatonic --mood launch
- **أرقام / params:** 0 3 5 7 10
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/score.py:37`

#### BEAT-64 · مقام lydian · Score scale lydian · 🟢 جاهز
- **ماذا / what:** Synth score scale 'lydian' for the numpy soundtrack generator.
- **كيف / how:** score.py out.wav --bpm 120 --seconds 15 --key A --scale lydian --mood launch
- **أرقام / params:** 0 2 4 6 7 9 11
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/score.py:37`

#### BEAT-65 · كشف الإيقاع · Beat grid detection · 🟢 جاهز
- **ماذا / what:** numpy spectral-flux onsets → autocorrelation tempo → beats/downbeats/hits.
- **كيف / how:** qa.beats(audio)
- **أرقام / params:** bpm range 70–180, prior near 120
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/qa.py:311`

#### BEAT-66 · مونتاج على الإيقاع · Beat-cut montage · 🟢 جاهز
- **ماذا / what:** Cut clips to detected beats with punch-ins, grade, captions, voice.
- **كيف / how:** montage.py cut CLIPS --music t.wav --seconds 20 --ratio 9:16 --grade teal_orange [--no-punch]
- **أرقام / params:** ratios 9:16,16:9,1:1,4:5; fps 30
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py`

#### BEAT-67 · أجواء مولدة · Synth ambience · 🟢 جاهز
- **ماذا / what:** numpy sea, wind, pad, rain, thunder, whoosh, birds, drops, brook at given seconds.
- **كيف / how:** ambience.py out.wav --seconds 17 --rain 9.6:12.8 --thunder 10.6 --whoosh 0.6 --chords 0:A
- **أرقام / params:** notes C130.81..B246.94 Hz
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/ambience.py:20`

#### BEAT-68 · موسيقى أصلية مولدة · Original score synth · 🟢 جاهز
- **ماذا / what:** Beat-grid soundtrack with kick/hats/pad/pluck on cues, stems.
- **كيف / how:** score.py out.wav --bpm 120 --seconds 15 --key A --mood launch [--cues cues.json --stems DIR]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/score.py:344`

#### BEAT-69 · ريل أغنية · Songreel lyric montage · 🟢 جاهز
- **ماذا / what:** Song sections → footage search queries → beat cuts → verse overlay.
- **كيف / how:** songreel.py analyze|queries|cut|make
- **أرقام / params:** 15 scene query sets
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/songreel.py:56`

#### BEAT-70 · المراجعة: شبكة الإيقاع مع علامة الذروة · Review: beat grid with drop marker · 🟢 جاهز
- **ماذا / what:** When the reel declares a BPM, the timeline shows a beat tick every 60/BPM seconds aligned to the drop, downbeats every 4 beats emphasised and the drop as a blue line.
- **كيف / how:** renderTL(): ticks from (drop mod beat) to duration; k = round((t−drop)/beat); class 'down' when k % 4 == 0, 'dropline' at the drop.
- **أرقام / params:** beat = 60/BPM s; downbeat every 4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:661`

#### BEAT-71 · المراجعة: تبديل الموسيقى ومستوى الصوت · Review: music swap and music/effects volume · 🟢 جاهز
- **ماذا / what:** Swap the music track, see where the beat drop lands, and set music and effects volume; music plays in sync with the video at the chosen speed.
- **كيف / how:** mediaPane(); audio.music, audio.musicVol, audio.sfxVol edits; syncMusic() sets currentTime and playbackRate.
- **أرقام / params:** volume sliders 0–1 step 0.05; defaults musicVol 0.6, sfxVol 0.8
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:776` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:534`

#### BEAT-72 · تقدير الإيقاع BPM · Tempo (BPM) estimate from spectral flux · 🟢 جاهز
- **ماذا / what:** Estimates beats per minute from the autocorrelation of positive log-spectral flux with sub-frame parabolic interpolation; reports a confidence and returns nothing for drones, tones or silence.
- **كيف / how:** tempo(mono, sr): hop 512, nfft 2048 Hann; search 60–200 BPM lags; fold result into 70–180 BPM; needs ≥ 4 s.
- **أرقام / params:** range 60–200 searched, folded to 70–180; no-onset guard: 95th percentile flux < 1.0
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/audio_analyze.py:165`

#### BEAT-73 · معايرة الصوت إلى -14 LUFS · Loudness master to -14 LUFS (loudnorm) · 🟢 جاهز
- **ماذا / what:** Normalizes the final mix for social/streaming delivery with a true-peak ceiling.
- **كيف / how:** ffmpeg ... loudnorm=I=-14:LRA=7:TP=-1.0, then -c:a aac -b:a 256k (smart_montage auto pipeline; also usable stand-alone).
- **أرقام / params:** I -14 LUFS, LRA 7, TP -1.0 dBTP, AAC 256 kb/s; gate -14 +/- 1.5 LUFS
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:220` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/SKILL.md`

#### BEAT-74 · ساعة الإيقاع للصورة · Beat clock for picture (MOTION.beats) · 🟢 جاهز
- **ماذا / what:** Picture and sound share one beat grid: from a BPM or from the JSON produced by motion.py beats.
- **كيف / how:** const B = MOTION.beats(120) or beats(json); B.at(n) beat time, B.len(n) duration of n beats, B.downbeats.
- **أرقام / params:** beat = 60/bpm s; downbeats every 4 beats by default
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:90`

#### BEAT-75 · موسيقى مولدة على الإيقاع · Synthesised score on the beat grid · 🟢 جاهز
- **ماذا / what:** An original soundtrack synthesised with numpy (no samples): sections of kick/clap/hats/sub/bass/pad/pluck/lead/bell, chord progression, risers, booms and drops.
- **كيف / how:** python score.py out.wav --spec score.json [--cues cues.json] [--stems DIR] | --bpm 120 --seconds 15 --key A --scale minor --mood launch|calm.
- **أرقام / params:** 48 kHz stereo; kick 'four'|'half'; chords in roman numerals (i, VI, III, VII); moods launch (half-time intro -> four-on-floor, stop at 55%, riser + boom) and calm (pad + pluck)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/score.py:1` · `kosif-one/tools/kosif-studio/motion/score.py:340` · `/tmp/claude-0/-home-user/39d82892-8140-5bc1-8072-589adc90e615/scratchpad/harvest/repos/run1/s.wav`

#### BEAT-76 · أصوات أجواء مولدة · Synthesised ambience · 🟢 جاهز
- **ماذا / what:** Deterministic ambience: sea swell, wind, a soft pad on chords, rain with thunder roll, whooshes, dawn birdsong, water drops and a brook.
- **كيف / how:** python ambience.py out.wav --seconds 17 [--rain 9.6:12.8] [--thunder 10.6] [--whoosh 0.6,15.3] [--chords 0:A,6:F] [--birds t0:t1] [--sea 0..1] [--drops t] [--brook t0:t1] [--seed 7].
- **أرقام / params:** 44.1 kHz stereo; birds = seeded FM chirps ~2.2 phrases/s panned L/R
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/ambience.py:1` · `kosif-one/tools/kosif-studio/motion/ambience.py:178` · `/tmp/claude-0/-home-user/39d82892-8140-5bc1-8072-589adc90e615/scratchpad/harvest/repos/run1/a.wav`

#### BEAT-77 · ضبط علو الصوت للنشر · Broadcast loudness master · 🟢 جاهز
- **ماذا / what:** Every mix normalised to -14 LUFS with a ceiling under -1 dBTP, AAC 256k 48 kHz.
- **كيف / how:** FFmpeg loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false:attack=3:release=60 (montage/reel/studio mux).
- **أرقام / params:** -14 LUFS, TP -1.5, limiter 0.84 (~-1.5 dBFS), AAC 256k
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:202` · `kosif-one/tools/kosif-studio/motion/reel.py:152`

#### BEAT-78 · خفض الموسيقى تحت الصوت · Voice-over sidechain ducking · 🟢 جاهز
- **ماذا / what:** Music bed ducks under speech with real sidechain compression.
- **كيف / how:** FFmpeg sidechaincompress threshold=0.02 ratio=12 attack=20 release=300 (montage) / ratio 10 with bed volume 0.45 (reel).
- **أرقام / params:** ~-18 dB under speech; 20 ms attack, 300 ms release
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:199` · `kosif-one/tools/kosif-studio/motion/reel.py:150`

#### BEAT-79 · موسيقى تحت الكلام · Music bed under speech (static) · 🟢 جاهز
- **ماذا / what:** Simple duck: music at -18 dB mixed under voice.
- **كيف / how:** [1:a]volume=-18dB[m];[0:a][m]amix=inputs=2:duration=first:normalize=0; EDL music.gain_db, fade_out.
- **أرقام / params:** -18 dB, fade_out 1.0 s
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `100-superskills/skills/pro-video-editor-ffmpeg/templates/edl.example.json`

#### BEAT-80 · استخراج بيانات الصوت لكل إطار · Per-frame audio feature extraction · 🟢 جاهز
- **ماذا / what:** ffmpeg->PCM, per video frame RMS, N log-spaced bands 40-10000 Hz normalised, spectral flux beats and histogram BPM.
- **كيف / how:** python extract_audio_data.py track.mp3 --fps 30 --bands 16 --out audio-data.json
- **أرقام / params:** Hann window; geomspace 40-10000 Hz; beat gaps 0.25-2.0 s 60 bins
- **الدليل / proof:** `100-superskills/skills/audio-reactive-captions-studio/scripts/extract_audio_data.py:30`

#### BEAT-81 · قالب مرئي صوتي · Two-canvas audio visualiser template · 🟢 جاهز
- **ماذا / what:** Background canvas driven by bass/RMS, foreground by bands.
- **كيف / how:** templates/audio-reactive.html
- **أرقام / params:** bg #0D1321 ink #F0EBD8 accent #F6C76B second #748CAB; Cairo
- **الدليل / proof:** `100-superskills/skills/audio-reactive-captions-studio/templates/audio-reactive.html`

#### BEAT-82 · قنوات الصوت كمحرّك · Sound channels as animation drivers · 🟢 جاهز
- **ماذا / what:** Reads per-frame audio analysis JSON so every visual value can come from the soundtrack (kick, onset, bass/mid/high, rms, tape clock, silence).
- **كيف / how:** const C = MOTION.channels(json); C.v('bass',t), C.kick(t,1,5), C.onset(t,1,4), C.beat(t), C.tape(t), C.silent(t), C.near('onsets',t,0.05). JSON from motion.py channels.
- **أرقام / params:** kick attack 1f tau 5f; onset 1f/4f; beat 1f/6f; near window 50 ms
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:97`

#### BEAT-83 · خلط صوت التركيب مع خفض الموسيقى تحت الصوت · Composition audio mux with voice ducking · 🟢 جاهز
- **ماذا / what:** After a studio render, every <audio> tag (src, data-start, data-volume, data-fade-in/out, data-role) is placed and mixed; clips marked data-role=voice duck everything else through a sidechain compressor.
- **كيف / how:** motion.mux_audio: ffmpeg adelay/afade/amix → sidechaincompress → two-pass loudnorm (measure, then linear with measured values) → AAC.
- **أرقام / params:** duck threshold 0.03 ratio 6 attack 20 ms release 380 ms; loudnorm I=-14 TP=-1 LRA=11 linear=true; AAC 256k 48 kHz
- **الدليل / proof:** `kosif-studio/motion/motion.py:347` · `kosif-studio/tests/test_studio.py:585`

#### BEAT-84 · إعدادات خفض الموسيقى تحت الكلام · Sidechain ducking presets · 🟢 جاهز
- **ماذا / what:** Music sits under speech via FFmpeg sidechaincompress with per-tool settings.
- **كيف / how:** montage.cut/voice_cut, reel, motion.mux_audio
- **أرقام / params:** montage: threshold 0.02 ratio 12 attack 20 release 300 makeup 1 (≈ −18 dB); voice_cut release 320; reel ratio 10 bed volume 0.45; mux threshold 0.03 ratio 6 release 380
- **الدليل / proof:** `kosif-studio/motion/montage.py:198` · `kosif-studio/motion/reel.py:140` · `kosif-studio/motion/motion.py:383`

#### BEAT-85 · ترتيبات جاهزة · Default arrangements launch / calm · 🟢 جاهز
- **ماذا / what:** launch: half-time intro with sparse pluck, four-on-floor build, a 2-beat stop at 55 % with riser and boom, drop with lead; calm: pad with sparse pluck.
- **كيف / how:** score.py --mood launch|calm
- **أرقام / params:** launch pluck [0,_,2,4,_,2,0,_] then [0,2,4,7,4,2], lead [7,4,5,2]
- **الدليل / proof:** `kosif-studio/motion/score.py:340`

#### BEAT-86 · موسيقى خلفية أصلية تلقائية · Auto underscore when no bed · 🟢 جاهز
- **ماذا / what:** reel/direct add a low original pad (then pad + bass) only if the clip has no music; verse --music auto adds one only when the track has no bed.
- **كيف / how:** reel --music auto|none|file; verse --music none|auto|bed.wav
- **أرقام / params:** reel/direct D minor 90 BPM seed 9, pad from beat 2, bass from 40 %, bed volume 0.45-0.5; verse D minor 80 BPM seed 11 volume 0.45
- **الدليل / proof:** `kosif-studio/motion/reel.py:131` · `kosif-studio/motion/direct.py:263` · `kosif-studio/motion/verse.py:440`

#### BEAT-87 · أعمدة طيف وموجة صوتية في ريموشن · Remotion spectrum bars & waveform · 📦 بأمر تثبيت
- **ماذا / what:** Real audio visualizers computed per frame from decoded audio.
- **كيف / how:** @remotion/media-utils: useWindowedAudioData({src, frame, fps, windowInSeconds:30}); visualizeAudio({numberOfSamples:256, optimizeFor:'speed'}) -> 0-1 bars (bass left); visualizeAudioWaveform({windowInSeconds:0.5}) + createSmoothSvgPath for a waveform line; pass frame from parent to children.
- **أرقام / params:** samples power of 2 (32-1024); window 30s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/audio-visualization.md`

#### BEAT-88 · موسيقى إجرائية بملف JSON · Procedural music score in JSON · 📦 بأمر تثبيت
- **ماذا / what:** Free deterministic synthesized themes: tempo, key, instruments with level/pan/echo/reverb/duck, sections in bars with chords and patterns, arrangement, loops.
- **كيف / how:** Write own numpy/ffmpeg synth (or vendor MIT game-audio-procedural toolkit after review). Fields: bpm 40-240, swing 0-0.5, echo 0.75 beat dotted-eighth, duck 0-0.95.
- **أرقام / params:** lead -9dB, drums -7, bass -10, pad -17
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound/references/SCORE.md` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural`

#### BEAT-89 · مكتبة توليف بايثون · Python synthesis toolkit (numpy/scipy) · 📦 بأمر تثبيت
- **ماذا / what:** PolyBLEP oscillators, FM, supersaw, noise colours, ADSR, biquads, Freeverb, chorus, bitcrush, Karplus-Strong, 808 cymbal, sidechain envelope, BS.1770 meter, look-ahead limiter.
- **كيف / how:** uv run with numpy, scipy, soundfile; 44.1kHz; seed all randomness.
- **أرقام / params:** SR 44100
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural`

#### BEAT-90 · كتابة اللحن بالخطوات · Step-notation melody writing · 📦 بأمر تثبيت
- **ماذا / what:** Write melodies/drums as one token per 16th step with rests, ties, accents, glides; chord-relative grooves.
- **كيف / how:** Song(bpm,bars,swing,seed,loop_start); notes 'C5:3 . - ! ? ~'; drums 'X x O o .'; always 16 steps/bar.
- **أرقام / params:** swing 0.1 light, 0.2-0.3 shuffle
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/music-composition.md`

#### BEAT-91 · توافق المؤثرات النغمية مع المقام · Tonal SFX key check · 📦 بأمر تثبيت
- **ماذا / what:** Pitched hits/pads must fit the actual chord at that moment, not just the song key.
- **كيف / how:** Pitch-shift tonal hits (rubberband/asetrate) to chord root.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound`

#### BEAT-92 · تتبع الإيقاع في المتصفح · Browser beat tracker (spectral flux + autocorrelation) · 📦 بأمر تثبيت
- **ماذا / what:** Finds tempo, beat grid, downbeats and onsets of any audio file locally.
- **كيف / how:** analyzeAudio(): decode, STFT N=2048 hop=512 Hann, log1p(10*|X|) positive flux, subtract +-8-frame mean, normalise; onsets >0.35 local max >= 90 ms apart; tempo by autocorrelation over 70-180 BPM with log-normal prior centred at 120 BPM (sigma 0.9 octave), confidence > 1.12, parabolic lag refinement, phase search, beat snap +-2 frames, downbeats = every 4th beat with best phase; fallback beats = onsets >= 0.3 s apart.
- **أرقام / params:** N 2048; hop 512; 70-180 BPM; prior 120; conf>1.12; file <= 160 MB
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:1032` · `app/public/js/00_editor.js:1038`

#### BEAT-93 · نمط مونتاج سريع سريع نَفَس · Editor's beat pattern (hook-quick-quick-breathe) · 📦 بأمر تثبيت
- **ماذا / what:** Plans cut points on the beat grid in an editor's rhythm: a hook, quick cuts, and breathing shots that prefer downbeats.
- **كيف / how:** planCuts(): fast = round(1 s/beat), slow = round(3 s/beat), hook = min(fast, round(1.4 s/beat)); pattern [hook,fast,fast,slow,fast,fast,fast,slow,fast,slow] in beats; slow steps snap to a downbeat within +-1 beat; min shot 0.35 s; last shot >= 0.5 s.
- **أرقام / params:** fast~1 s; slow~3 s; min 0.35 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2320`

#### BEAT-94 · توطية الموسيقى وقت الكلام · Music ducking under speech · 📦 بأمر تثبيت
- **ماذا / what:** Background music drops while someone is speaking and fades at the track edges, both live and in renders.
- **كيف / how:** level = vol * (duck && speaking ? 0.32 : 1) * edge, edge = min((t-at)/0.4, (end-t)/0.6); live gain eased 12% per frame; offline mix automates gain every 0.1 s (0.05 s in the montage mixer); montage segments get 30 ms clicks-free fades.
- **أرقام / params:** duck x0.32 (~-10 dB); fade in 0.4 s; out 0.6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:995` · `app/public/js/00_editor.js:2234` · `app/public/js/10_studio.js:3895`

#### BEAT-95 · مكتبة المؤثرات الصوتية المولدة · Synthesised SFX library (16) · 📦 بأمر تثبيت
- **ماذا / what:** Sixteen deterministic sound effects synthesised in the browser with no downloads.
- **كيف / how:** SND.makeSfx(): seeded mulberry32 noise, band-pass/one-pole filters, sweeps, tones, envelopes, normalised peaks: tick (50 ms, 2.5-9 kHz, -8 dB), click (80 ms, -7), type (9 keys over 0.7 s, -9), pop (900->300 Hz 0.12 s, -6), blip (1320+2640 Hz, -10), hit (120->45 Hz 0.45 s, -3), impact (90->32 Hz 0.9 s, -2), whoosh (0.4 s, 300->5000 Hz, -8), swish (0.9 s, 200->2500 Hz, -12), riser (1.6 s, 200->7000 Hz + 180->720 Hz tone, -9), swell (2 s pad A-C#-E-A, -14), shimmer (2637-4699 Hz, -16), glitch (0.35…
- **أرقام / params:** SR 44100
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:89`

#### BEAT-96 · تركيب طبقة المؤثرات · SFX stem compositor · 📦 بأمر تثبيت
- **ماذا / what:** Places named effects at event times so their perceived peak lands on the event, with pan and a soft clipper, and writes a stereo WAV track.
- **كيف / how:** SND.stem(events,dur): start = t - PEAK[name]; equal-ish pan law; tanh soft clip; SND.wav writes 16-bit PCM stereo; MON.addStem adds it as an auto 'sfx' track at volume 0.7.
- **أرقام / params:** default vol 0.6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:161` · `app/public/js/10_studio.js:2110`

#### BEAT-97 · مؤلف موسيقى خلفية محلي · Procedural music bed composer · 📦 بأمر تثبيت
- **ماذا / what:** Generates a royalty-free background bed (pads, sub bass, arpeggio, kick, hats) for a given duration and mood, and returns its beat times.
- **كيف / how:** SND.music(dur,mood,bpm): moods calm 80 / tech 108 / bright 116 / epic 92 BPM; chords every 8 beats, progression minor-based (bright major-based); pads = triad+octave with 6 harmonics, +-0.25% stereo detune; calm = sustained sub, others = pulsing bass; tech/bright/epic add 16th arpeggio with pan; tech/epic add 110->45 Hz kick every 2 beats; hats on off-beats; 2 s fade-in, 3 s fade-out, normalised to -3 dBFS.
- **أرقام / params:** calm 80|tech 108|bright 116|epic 92 BPM
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:125`

#### BEAT-98 · توزيع المؤثرات على كلمات الفيلم · Film SFX auto-placement · 📦 بأمر تثبيت
- **ماذا / what:** Each motion-film style declares sound roles; effects are placed on line starts, emphasised words, moves, writing and counting.
- **كيف / how:** KIT.sfxEvents: move 0.75 s before each line for travelling styles (pan +-0.3), line sound at start-0.04 (vol 0.42), emphasis on starred words (0.5), writing every 0.95 s (0.26), count ticks every 70 ms for 1.2 s on numbers, product style type/click/impact, end sound 0.35 s after the last line.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:967`

#### BEAT-99 · مؤثرات المونتاج على القطعات · Montage SFX rules · 📦 بأمر تثبيت
- **ماذا / what:** Montage cuts and camera accents get matching effects automatically.
- **كيف / how:** MON.sfx: whip/zoomblur/spin cuts -> whoosh 0.35 alternating pan; flash -> click, glitch -> glitch; otherwise tick every 4th cut; punch_in -> hit 0.32; crash_zoom -> impact 0.45; swell 1.6 s before the end.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:2105`

#### BEAT-100 · تحسين الكلام التلقائي · Automatic speech enhancement chain · 📦 بأمر تثبيت
- **ماذا / what:** Measures the main speech and cleans it live and in renders: rumble cut, presence lift, gain to a broadcast-like level, compression and a limiter.
- **كيف / how:** AUD.chain(ac,cfg): highpass 90 Hz (120 Hz if SNR < 14 dB) Q 0.7 -> peaking 3.2 kHz +2 dB Q 0.8 -> gain to speech RMS -20 dBFS (clamp -12..+26 dB) -> compressor threshold -24+(1-k)*12 dB, ratio 2+4k, knee 12, attack 4 ms, release 180 ms -> limiter -2 dB ratio 20 attack 1 ms release 80 ms -> make-up k*1.5 dB.
- **أرقام / params:** target -20 dBFS RMS (~-17 LUFS); HPF 90/120 Hz; presence 3.2 kHz +2 dB
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:3843` · `app/public/js/10_studio.js:3861`

#### BEAT-101 · بوابة ضوضاء بين الكلمات · Downward expander between words · 📦 بأمر تثبيت
- **ماذا / what:** In renders the room noise between words is pushed down so the gain that lifts speech does not lift the room.
- **كيف / how:** AUD.gate: envelope attack 4 ms / release 40 ms; close threshold min(quiet25%+1.5 dB, speech-12 dB), open = min(close+5, speech-7); gain eases to -10 dB floor with attack 5 ms, release 160 ms.
- **أرقام / params:** floor -10 dB; attack 5 ms; release 160 ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:3895`

#### BEAT-102 · موجات الصوت · Audio visualiser (bars / circle) · 📦 بأمر تثبيت
- **ماذا / what:** Audio-only clips get an animated spectrum: 48 rounded bars or a circular ring around a disc.
- **كيف / how:** drawBackdrop(): AnalyserNode fftSize 256; bars = 80% width, height 8 + v*22% H; circle radius 20% short side at 42% height, bar length 0.15R+0.7vR; demo uses synthetic sines.
- **أرقام / params:** 48 bars; fft 256
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:143`

#### BEAT-103 · النبض مع الإيقاع · Beat-reactive pulse · 📦 بأمر تثبيت
- **ماذا / what:** Picture, captions and progress bar pulse on each detected beat.
- **كيف / how:** beatPulse(t)=exp(-(t-lastBeat)*9); zoom extra = pulse*0.012 (calm) or 0.035; captions scale 1+0.045*pulse; progress bar height x(1+0.6 pulse); exposed to code scenes as u.beat().
- **أرقام / params:** decay rate 9/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:181` · `app/public/js/00_editor.js:255`

#### BEAT-104 · فيديو لملف صوت فقط · Audio-only clip visuals · 📦 بأمر تثبيت
- **ماذا / what:** An audio-only upload becomes a video: animated gradient or pattern background, visualiser bars or circle, big centred captions and beat pulse.
- **كيف / how:** S.kind 'audio' path in draw(): drawBackdrop + TYPE_DEFAULTS aud_talk (bars, centre captions size 10 chunk 2, speech sync) / aud_music (circle viz, react, pattern sync).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:143` · `app/public/js/00_editor.js:2789`

#### BEAT-105 · أمر: استخراج الإيقاع · CLI: beats · 📦 بأمر تثبيت
- **ماذا / what:** Detect beat times + BPM from project audio (bpm-detective) -> JSON {ok,file,count,bpm}.
- **كيف / how:** npx hyperframes beats ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Detect beat times + BPM from project audio (bpm-detective) -> JSON {ok,file,count,bpm}.
- **تثبيت / install:** `npx hyperframes beats`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### BEAT-106 · أمر: تسوية الصوت · CLI: normalize-audio · 📦 بأمر تثبيت
- **ماذا / what:** Loudness-match target to reference audio; default target -16 LUFS; --write, --lufs negative.
- **كيف / how:** npx hyperframes normalize-audio ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Loudness-match target to reference audio; default target -16 LUFS; --write, --lufs negative.
- **تثبيت / install:** `npx hyperframes normalize-audio`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### BEAT-107 · سلسلة مؤثرات صوتية · Audio fx chain (WebAudio-style) · 📦 بأمر تثبيت
- **ماذا / what:** Per-clip/group effects in signal order: highpass/lowpass/peaking/shelves, gain, compressor, limiter, gate, saturate (9 curves), bitcrush, delay, reverb, chorus, phaser, pitchshift ±12 st.
- **كيف / how:** data-fx-chain JSON on <audio>/<video>/<hf-audio-group>.
- **أرقام / params:** compressor -24dB 4:1 20/250ms; limiter -1dB; reverb size .7 wet .35
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/reference/audio-effects.mdx`

#### BEAT-108 · أتمتة الصوت · Audio automation lanes · 📦 بأمر تثبيت
- **ماذا / what:** Envelope points on volume or fx.<node>.<param> with curve -1..1 or via-points.
- **كيف / how:** data-automation JSON {target,points:[{t,v,curve}]}.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/reference/audio-effects.mdx`

#### BEAT-109 · مونتاج على الإيقاع · Music-to-video beat grid · 📦 بأمر تثبيت
- **ماذا / what:** Cut footage/lyrics to detected beats.
- **كيف / how:** hyperframes beats -> beat JSON; registry beat-freeze-cut, beat-pulse-background.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/music-to-video.mdx`

#### BEAT-110 · لسعة الإيقاع · Beat Accent · 📦 بأمر تثبيت
- **ماذا / what:** A one-hit music sting: white/accent impact flash, tiny scale pulse on the subject and instant decay.
- **كيف / how:** Install with `npx hyperframes add beat-accent` (copies to compositions/components/beat-accent.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** flashColor accent|soft|bright; intensity 1; vars: text=BOOM; flashColor=accent[accent|soft|bright]; intensity=1(0.5..2)
- **تثبيت / install:** `npx hyperframes add beat-accent` (copies to compositions/components/beat-accent`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/beat-accent/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/beat-accent/beat-accent.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/beat-accent.mdx`

#### BEAT-111 · خلفية نابضة على الإيقاع · Beat Pulse Background · 📦 بأمر تثبيت
- **ماذا / what:** Backdrop glow and saturation pulse on a supplied list of beat times (seconds), so the background breathes with music.
- **كيف / how:** Install with `npx hyperframes add beat-pulse-background` (copies to compositions/components/beat-pulse-background.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (head…
- **أرقام / params:** beats list "0.5,1.0,..."; intensity subtle|club; vars: beats=0.5,1.0,1.5,2.0,2.5,3.0,3.5; accent=green[green|blue|violet]; intensity=subtle[subtle|club]
- **تثبيت / install:** `npx hyperframes add beat-pulse-background` (copies to compositions/components/beat-pulse-background`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/beat-pulse-background/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/beat-pulse-background/beat-pulse-background.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/beat-pulse-background.mdx`

#### BEAT-112 · تجميد على الإيقاع · Beat Freeze Cut · 📦 بأمر تثبيت
- **ماذا / what:** Music-led sequence: speed ramp, beat-locked freeze-frame hit (flash, contour, outline, FREEZE badge) and hard cut.
- **كيف / how:** Install with `npx hyperframes add beat-freeze-cut` (copies the full composition to compositions/beat-freeze-cut.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** beat1 0.7 s; beat2 2.2 s; 6 s; Google Fonts: Inter; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add beat-freeze-cut` (copies the full composition to compositions/beat-freeze-cut`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/beat-freeze-cut/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/beat-freeze-cut/beat-freeze-cut.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/beat-freeze-cut.mdx`

#### BEAT-113 · موجة صوتية · Waveform · 📦 بأمر تثبيت
- **ماذا / what:** Blue-to-pink equaliser bars pulsing like an audio visualiser (procedural, not audio-reactive). A 2 s WebGPU shader background/object from the Shaders library.
- **كيف / how:** Install `npx hyperframes add waveform` or place lib/shaders.iife.js beside the HTML and declare <canvas data-shader="Waveform" width=1920 height=1080> inside a composition root marked data-requires-webgpu data-no-timeline; layer it under titles as a background plate; render needs a WebGPU-capable Chromium.
- **أرقام / params:** data-shader="Waveform"; 1920x1080; duration 2 s; shaders.iife.js 1,444,793 bytes (shaders 4.0.0)
- **تثبيت / install:** `npx hyperframes add waveform` or place lib/shaders`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/waveform/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/waveform/waveform.html` · `kosif-one/vendor/hyperframes/registry/blocks/waveform/lib/shaders.THIRD-PARTY-LICENSES.txt`

#### BEAT-114 · التلاشي وخفض الموسيقى عبر مسار الأتمتة · Volume fades and ducking via automation lane · 📦 بأمر تثبيت
- **ماذا / what:** One rule: volume over time is a data-automation volume lane with clip-local points; a lane wins over a GSAP volume tween (lint audio_volume_double_automation).
- **كيف / how:** Example envelope fade-in 0-1 s, duck to 0.3 at 2-2.2 s, hold, back up 3-3.2 s, fade-out 4-5 s.
- **أرقام / params:** duck level 0.3; ramps 0.2 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### BEAT-115 · مزامنة مؤثر صوتي مع حدث مرئي · Align a sound to an on-screen event · 📦 بأمر تثبيت
- **ماذا / what:** SFX clip data-start is set to the timeline position of the visual hit (tween position), with audio alignment recipes for offsetting transients.
- **كيف / how:** creator-editing-recipes.md §Audio alignment / §Align a sound to an on-screen event.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### BEAT-116 · مرئيات تتفاعل مع الصوت · Audio-reactive visuals from precomputed bands · 📦 بأمر تثبيت
- **ماذا / what:** Pre-extracted per-frame frequency bands drive GSAP properties: bass -> scale pulse, treble (bands 12-14) -> glow shadows, amplitude -> opacity/y/background, mids (4-8) -> radius/shape.
- **كيف / how:** python <skill>/scripts/extract-audio-data.py <audio> -> AUDIO_DATA {fps:30,totalFrames,frames[{bands[]}]} sampled per frame with tl.call; each band normalized 0-1.
- **أرقام / params:** fps 30; bands 0..14
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/audio-reactive.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/scripts/extract-audio-data.py` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/techniques.md`

#### BEAT-117 · سلسلة المؤثرات الصوتية على المسار · Audio FX chain on any track (data-fx-chain) · 📦 بأمر تثبيت
- **ماذا / what:** Effects are declared in signal order as JSON on the <audio>/<video> element; preview (live AudioContext) and render (OfflineAudioContext in headless Chrome) run the same Web Audio graph so what you scrub is what renders.
- **كيف / how:** data-fx-chain='{"version":1,"nodes":[{"type":"compressor","id":"c1","params":{"threshold":-18,"ratio":3}}]}'; order: subtract (filters) -> level (dynamics) -> relationships (carve) -> character -> ceiling (limiter last).
- **أرقام / params:** families: gain, highpass, lowpass, peaking, lowshelf, highshelf, compressor, limiter, gate, saturate, delay, reverb, chorus, phaser, bitcrush
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/attributes.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/fx-registry.md`

#### BEAT-118 · سجل معاملات المؤثرات · Effect parameter registry (ranges and defaults) · 📦 بأمر تثبيت
- **ماذا / what:** Exact parameters per effect, e.g. highpass 20-20000 Hz default 300; lowpass default 8000; peaking gain -40..40 dB q default 1; compressor threshold -24 dB ratio 4 attack 20 ms release 250 ms knee 2.83; limiter -1 dB attack 5 ms release 50 ms; gate -35 dB range -24 ratio 10; saturate types tanh/atan/…
- **كيف / how:** Read references/fx-registry.md; AUTO-marked params are automatable lanes; worklet effects (compressor, limiter, gate, bitcrush) are not automatable.
- **أرقام / params:** see what
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/fx-registry.md`

#### BEAT-119 · نحت الموسيقى تحت التعليق الصوتي · Voiceover carve (spectral sidechain ducking) · 📦 بأمر تثبيت
- **ماذا / what:** Instead of ducking the whole bed, the bed is dipped only in the bands the voice occupies, as envelopes following the speech level, plus a slow-release level-match gain; settings live on the bed and name the voice sources; required whenever music plays under a voice.
- **كيف / how:** node <skill>/scripts/carve.mjs --comp index.html [--bed id] [--voice id] [--strength 0.8] [--dry-run]; writes data-fx-carve, data-fx-chain (peaking xN + gain, tagged fromCarve) and data-automation; verify with `npx hyperframes check`.
- **أرقام / params:** strength 0.8 default: bands 250/400/630/1000/2500 Hz -7.4 dB q2.06 and 1600 Hz -14.8 dB, 273-point envelope floor -19.2 dB; 0.25 -> 6 dB dip; 0.5 -> 10 dB (audible as effect)
- **تثبيت / install:** `npx hyperframes check``
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-audio/scripts/carve.mjs` · `kosif-one/vendor/hyperframes/skills/hyperframes-audio/scripts/carve.test.mjs`

#### BEAT-120 · حافلة المزج الفرعي · Submix bus <hf-audio-group> · 📦 بأمر تثبيت
- **ماذا / what:** One chain, one fader and one automation clock for several tracks (e.g. all narration clips) so a compressor hears the whole voice.
- **كيف / how:** <hf-audio-group id=voiceover data-volume=0.9 data-fx-chain=...> + <audio data-audio-group=voiceover>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/SKILL.md`

#### BEAT-121 · منحنيات الأتمتة للصوت والمؤثرات · Automation envelopes on volume or any effect param · 📦 بأمر تثبيت
- **ماذا / what:** data-automation lanes ({target, points:[{t,v}]}) ride volume, rate or fx.<node>.<param>, and fx.preset.<id> fades a whole preset via presetAmount 0..1.
- **كيف / how:** references/attributes.md lane rules; volume lane is baked into PCM by the engine mixer.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/attributes.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/presets.md`

#### BEAT-122 · إعدادات الفضاء والصدى · Space / reverb presets · 📦 بأمر تثبيت
- **ماذا / what:** room-tight, room-natural, hall, slap-echo, dub-throw for putting something behind something else; keep wet lower than sounds right solo.
- **كيف / how:** preset in data-fx-chain; one-knob Space profile on reverb.
- **أرقام / params:** 5 presets
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/presets.md`

#### BEAT-123 · ملفات المقبض الواحد للمؤثرات · One-knob effect profiles · 📦 بأمر تثبيت
- **ماذا / what:** Single 0..1 knobs: compressor Evenness, gate Tightness, saturate Warmth, reverb Space, bitcrush Crush.
- **كيف / how:** references/presets.md § One-knob profiles.
- **أرقام / params:** 0..1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/presets.md`

#### BEAT-124 · مفردات نطاقات التردد · Frequency band vocabulary · 📦 بأمر تثبيت
- **ماذا / what:** Rumble 20-80 Hz, Weight 80-250, Mud 250-600, Middle 600-2000, Presence 2000-5000, Edge 5000-10000, Air 10000-20000 Hz; voice and music fight mostly in 1-3 kHz.
- **كيف / how:** Use to name problems before choosing a fix.
- **أرقام / params:** 7 bands
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/presets.md`

#### BEAT-125 · شبكة الإيقاع لاستوديو · Studio beat grid (beats command) · 📦 بأمر تثبيت
- **ماذا / what:** Analyzes a project's local music <audio> (data-timeline-role=music or id containing music/bgm/soundtrack) in headless Chrome and writes a Studio-compatible beat file.
- **كيف / how:** npx hyperframes beats [dir] [--json]; for full beat-synced films use music-to-video's analyze-beatgrid.py instead.
- **تثبيت / install:** `npx hyperframes beats [dir] [--json]`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/beats.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/beats.ts`

#### BEAT-126 · خفض تلقائي من بيانات الصوت · Auto-duck lane from audio_meta · 📦 بأمر تثبيت
- **ماذا / what:** Emits a data-automation volume lane on the BGM element under narration (clip-local times) or bakes ducking for export.
- **كيف / how:** node <skill>/scripts/audio-duck.mjs --meta audio_meta.json --target '#bgm' --composition index.html.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/scripts/audio-duck.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/lib/duck.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/references/operations.md`

#### BEAT-127 · مكتبة المؤثرات الصوتية المرفقة · Bundled SFX library (19 files) · 📦 بأمر تثبيت
- **ماذا / what:** chime 2.5 s, click-soft 0.37, click 0.37, error 1.62, glitch-1 2.64, glitch-2 3.5, glitch-3 3.1, impact-bass-1 2.12, impact-bass-2 2.59, key-press 0.4, notification 2.46, ping 1.32, pop 0.72, riser 10.03, sparkle 1.8, typing 1.5, whoosh-cinematic 5.54, whoosh-short 0.57, whoosh 0.57; let impact deca…
- **كيف / how:** resolve --type sfx --intent 'whoosh' (bundled answers without credentials).
- **أرقام / params:** 19 cues
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/audio/assets/sfx/manifest.json` · `kosif-one/vendor/hyperframes/skills/media-use/audio/assets/sfx/CREDITS.md` · `kosif-one/vendor/hyperframes/skills/media-use/audio/references/sfx.md`

#### BEAT-128 · فيديو متزامن مع إيقاع الموسيقى · Music-to-video beat-synced workflow · 📦 بأمر تثبيت
- **ماذا / what:** Track is the spine: setup bgm -> analyze once to audiomap.json -> frame skeleton in STORYBOARD.md -> plan (brand preset + per-frame groups: template, free-compose or asset treatment) -> frame workers build compositions/frames/NN-*.html -> assemble -> verify -> render; lyric videos time lines by tran…
- **كيف / how:** npx hyperframes init videos/<p> --non-interactive --example=blank --skill=music-to-video; scripts/stage-assets.mjs; scripts/validate-plan.mjs; scripts/assemble-index.mjs.
- **أرقام / params:** frames >~6 s need 2+ groups
- **تثبيت / install:** `npx hyperframes init videos/<p> --non-interactive --example=blank --skill=music-to-video`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/SKILL.md` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/planning.md` · `kosif-one/vendor/hyperframes/skills/music-to-video/scripts/validate-plan.mjs`

#### BEAT-129 · محلل شبكة الإيقاع · Beat-grid analyzer (audiomap.json) · 📦 بأمر تثبيت
- **ماذا / what:** librosa analysis producing energy phases (level/density/feel), onsets + onset_rate, rolls, silences, hard_stops, key_moments, phrases, tempo/grid; bpm and beats_sec trusted only on genuinely rhythmic music.
- **كيف / how:** python3 <skill>/scripts/analyze-beatgrid.py assets/bgm.mp3 -o audiomap.json --print (needs librosa numpy soundfile).
- **أرقام / params:** 542-line analyzer
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/scripts/analyze-beatgrid.py` · `kosif-one/vendor/hyperframes/skills/hyperframes/references/capability-menu.md`

#### BEAT-130 · حركات إيقاعية موثقة فقط · Beat motion primitives without demo folders · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued moves without a standalone demo: chromatic-pressure (RGB tension on transients 0.1-0.5 s), color-grid-shuffle (cells recolored per onset), content-swap (0 ms percussive swap, the workhorse), freeze-hold (freeze system 0.5-2 s), negative-space-hold (one mark in empty space 1-6 s), overlay-…
- **كيف / how:** references/motion-primitive-catalog.md.
- **أرقام / params:** 9 moves
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### BEAT-131 · مساعدات مدة الإطار ومستوى الموسيقى · Pad frame duration and BGM volume helpers · 📦 بأمر تثبيت
- **ماذا / what:** Pads frame durations to fit audio and computes BGM volume relative to narration.
- **كيف / how:** scripts/lib/pad-frame-duration.mjs, lib/bgm-volume.mjs.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/product-launch-video/scripts/lib/pad-frame-duration.test.mjs` · `kosif-one/vendor/hyperframes/skills/product-launch-video/scripts/lib/bgm-volume.mjs`

#### BEAT-132 · الصوت يحرك الصورة · Sound-driven picture · 📦 بأمر تثبيت
- **ماذا / what:** Spectrogram canyon ground, glitch pass (chroma, slice, negative tear, mono freeze, warp), sparks on tape clock, MOTION.channels.
- **كيف / how:** three-kit.js (window.K3) in a --3d project; render --engine studio
- **أرقام / params:** makeSpectrumGround, makeGlitchPass, makeSparks, spectrumOnTape
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:106` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### BEAT-133 · وادٍ من المخطط الطيفي · Spectrogram canyon (sound as terrain) · 📦 بأمر تثبيت
- **ماذا / what:** The music's spectrogram becomes a heightfield canyon the camera travels through, with a lava river from the bass and glowing walls, scrolled by the tape clock.
- **كيف / how:** spectrumOnTape(img, channels) → {texture, seconds}; makeSpectrumGround(texture, {width 120, depth 90, half 17, segX 960, segZ 420, window 8, seconds, amp 5.2, glow 1.0, lava .72, light (1,.32,.18), lightColor 0xff8a50, fillColor 0x5a3a90, rock 0x30262c}); ground.userData.set(t, tape, kick, glow).
- **أرقام / params:** 8 tape-seconds across 120 m (15 m/s)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:41` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/spectrum_height.png`

#### BEAT-134 · ساعة شبكة إيقاع لفيلم كامل · Beat-grid clock for a whole film · 📦 بأمر تثبيت
- **ماذا / what:** All events are scheduled in beats rather than seconds so picture and score lock together.
- **كيف / how:** const B = M.beats(120), b = B.at → b(n) = n × 0.5 s; every tween uses b(1), b(3.6), b(15.8)…; the score is written at the same bpm (120) with matching stops/risers/booms.
- **أرقام / params:** 120 BPM, 15 s = 30 beats
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:61` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/assets/score.json:2`

#### BEAT-135 · توقف الشريط ووقت الرصاصة ولمسات الخلل · Tape-stop bullet time and glitch accents · 📦 بأمر تثبيت
- **ماذا / what:** When the music tape-stops the world freezes on the tape clock while the camera keeps moving on the wall clock; glitch accents are keyed to analysis: onsets split colour, tape acceleration slices the frame, the first frames of silence tear in negative, standing tape turns the world cold silver.
- **كيف / how:** makeGlitchPass() inserted before OutputPass; userData.set({chroma: .35·on + .6·kick + .5·clamp(dsp/2) + tear, slice: .35·clamp(dsp/2) + .9·tear, negative: tear ? .9 : 0, mono: clamp((.25−speed)/.25), warp: (1−speed)·.6, frame}); dsp = |speed(t+1/60) − speed(t−1/60)|·30.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:1` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:134`

#### BEAT-136 · مرئيات تتفاعل مع الصوت · Audio-reactive visuals (kick/bass mapping) · 📦 بأمر تثبيت
- **ماذا / what:** Kick, bass and onset values map directly to physical motion: orb bob and squash, exposure pump, fov punch, camera shake/roll, spark bursts, ground glow and sky corona.
- **كيف / how:** orb y = 1.45 + .35·bass; exposure ×(.85+.25·kick); fov +3.5·kick; shake .05·kick; ground glow (.35+.9·onset)·(silent?0:1); warmth .45+.3·bass.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js:99`

#### BEAT-137 · خفض الموسيقى تحت الصوت · Sidechain auto-ducking · 📦 بأمر تثبيت
- **ماذا / what:** Music dips under speech automatically.
- **كيف / how:** timeline audio.duck auto|voice|clips|none
- **أرقام / params:** ~-18 dB; threshold 0.02, ratio 12, attack 20 ms, release 300 ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### BEAT-138 · ساعة الإيقاع · Beat clock MOTION.beats · 📦 بأمر تثبيت
- **ماذا / what:** Shared beat clock for picture and sound.
- **كيف / how:** MOTION.beats(bpm,offset).at(n)/len(n); motion.py beats
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### BEAT-139 · صوت محيطي مُركّب · Synth ambience fallback · 📦 بأمر تثبيت
- **ماذا / what:** Synthesised ambience when no licensed recording; disclose it.
- **كيف / how:** kmotion ambience / ambience.py
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `100-superskills/skills/kosif-montage-motion/scripts/ambience.py`

#### BEAT-140 · موسيقى أصلية · Original music score · 📦 بأمر تثبيت
- **ماذا / what:** Synthesises an original track by BPM, length, mood.
- **كيف / how:** kmotion score out.wav --bpm --seconds --mood
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/score.py`

#### BEAT-141 · قنوات الصوت · Audio channels + tape-stop · 📦 بأمر تثبيت
- **ماذا / what:** Per-frame kick/bass/onset/centroid/silence/pitch channels; tape-stop detection.
- **كيف / how:** motion.py channels; MOTION.channels; score.py tape_stops_s; motion.py loopcheck
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/x-trend-2026.md`

#### BEAT-142 · كاشف الإيقاع وسرعة BPM · Kick-band beat & BPM detector · 📦 بأمر تثبيت
- **ماذا / what:** Finds tempo, a regular beat grid and transient onsets from any audio/video file so cuts can land on beats.
- **كيف / how:** python scripts/beat_detector.py music.mp3 [--json] [--limit 20]; ffmpeg decodes to mono f32 22050 Hz; Butterworth order-4 band-pass 50-250 Hz (SOS); 10 ms RMS envelope; half-wave onset difference; autocorrelation over 60-180 BPM; find_peaks height .15 distance .25 s; grid from first onset every 60/BPM.
- **أرقام / params:** sr 22050, band 50-250 Hz, hop 10 ms (100 Hz envelope), BPM range 60-180, peak height 0.15, min gap 0.25 s; outputs bpm, beat_interval, first_downbeat, grid_beats, onsets
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/beat_detector.py:42` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/beat_detector.py:106`

#### BEAT-143 · خفض الموسيقى تحت الصوت · Music ducking under voice (spec vs code) · 📦 بأمر تثبيت
- **ماذا / what:** Background music should drop while narration plays.
- **كيف / how:** Spec: sidechain -18 dB, attack 20 ms, release 300 ms. Actual smart_montage code just sets music volume 0.35 and amixes it with voice (static, no sidechain). Real ducking with ffmpeg: [music][voice]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300[ducked] then amix.
- **أرقام / params:** spec -18 dB / 20 ms / 300 ms; code static gain 0.35 (about -9.1 dB)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/smart_montage.py:210` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/SKILL.md`

#### BEAT-144 · موسيقى حجاز مركّبة بلا عينات · Hijaz synth soundtrack (numpy/scipy, no samples) · 📦 بأمر تثبيت
- **ماذا / what:** An original 18 s score generated in code with an Egyptian colour: Hijaz on D, qanun-like plucks, warm pads following the shots, risers and impacts on every cut, a pulse through the night city and a D-major resolve.
- **كيف / how:** numpy + scipy: drone D2/D3; pad = 3 detuned saws per note (-0.07/0/+0.08 semitone) through 2-pole Butterworth LP 2600-4200 Hz with ADSR (.6/.4/.85/.9) and 12 ms delay for width; Karplus-Strong pluck (decay .996, exp tau .55 s) on a 16-step motif at 112 BPM (8ths then 16ths from Cairo); kick with pitch sweep 42+90e^-30t; band-pass noise risers 0.7 s before each cut; impact = kick + LP noise; shimmer sines on Hijaz degrees; chords D, Gm, Cm(addEb), D(b9), Bb, D.
- **أرقام / params:** 48 kHz stereo 16-bit; BPM 112; cuts 2.6/6.0/9.5/13.5/16.5; scale D Eb F# G A Bb C (MIDI 62,63,66,67,69,70,72,74); seed 2120
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/audio.py:1-123`

#### BEAT-145 · سلسلة ماسترنج ذاتية · Self-mastering chain (reverb, shelf, loudness, true-peak guard) · 📦 بأمر تثبيت
- **ماذا / what:** A code-only master: convolution reverb from a synthetic decaying noise impulse, high-pass, presence/air shelf for phone speakers, RMS normalisation, soft tanh limiter and a 4x oversampled true-peak check.
- **كيف / how:** IR 2.4 s exp decay tau .55 s low-passed 5 kHz, fftconvolve, wet .28; HP 35 Hz; +0.9 x high-pass(2500) shelf; target RMS -15 dBFS; lim(x)=tanh(1.1x)*.89; -2.05 dB trim; resample_poly x4 peak <= -1.2 dBTP; 0.6 s end fade.
- **أرقام / params:** README measurement: -15.7 LUFS, true peak -2.4 dBTP, 0 clipping, 112 BPM
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/audio.py:125-148` · `kosif-one/projects/egypt-2120-animation/README.md`

#### BEAT-146 · تنفس الهالة على ضربات الإيقاع · Downbeat-synced halo breathing · 📦 بأمر تثبيت
- **ماذا / what:** The sun halo dips and recovers on every musical downbeat measured from the voice/music track, so the picture breathes with the sound.
- **كيف / how:** DOWN = channels.json downbeats (13 values from 1.429 to 24.373 s); per downbeat: halo opacity 1 -> .7 in 0.5 s (E.out) then back in 0.6 s (sine.inOut).
- **أرقام / params:** BPM 125.56, 52 beats, 13 downbeats, 63 kicks, 87 onsets
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:110` · `kosif-one/projects/thursday-dua-animation/source/index.html:161` · `kosif-one/projects/thursday-dua-animation/source/src/channels.json`

#### BEAT-147 · قنوات الصوت لكل إطار · Audio channels JSON (per-frame features) · 📦 بأمر تثبيت
- **ماذا / what:** A per-frame analysis of the soundtrack that any visual can read: tempo, beat/downbeat/kick/onset lists and per-frame curves (rms, bass, mid, high, onset, centroid, silence, pitch dive/rise, speed, tape clock).
- **كيف / how:** Produced by motion.py channels TRACK.wav --fps 30; consumed by M.channels(json): ch.v('bass',t), ch.kick(t), ch.onset(t), ch.beat(t), ch.tape(t), ch.silent(t), ch.near('onsets',t).
- **أرقام / params:** fps 30, 744 frames, 24.8 s, bpm 125.56
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/src/channels.json` · `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:94-107`

#### BEAT-148 · مواصفة موسيقى خلفية للكلام · Talking-voice score spec (90 BPM D minor) · 📦 بأمر تثبيت
- **ماذا / what:** A sectioned arrangement written in beats so music follows the talk: pad only under the opening, bass and half-time kick in the story, plucks and hats in the joy section, a tape stop exactly on the act change, a riser into a boom at the payoff.
- **كيف / how:** score.json -> python score.py score.wav --spec score.json --cues cues.json (numpy synthesis); mixed under voice at volume .42 with 1.2 s fade-out.
- **أرقام / params:** bpm 90, 47 s, key D minor; chords i VI i VII III VII VI III VII i VI III; tape stop at 23.9 s for 0.6 s; riser beats 61-65; boom 65
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/score.json` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:49`

#### BEAT-149 · قائمة مؤثرات صوتية مصممة · Designed SFX cue sheet · 📦 بأمر تثبيت
- **ماذا / what:** Every sound effect is tied to something visible: thump on the first keyword, whoosh on scene changes, tick on numbers, pop on counters, boom on the punch, swish on the split, chime on the 'moment' rings.
- **كيف / how:** cues.json [{t,type,gain}] rendered by score.py sfx(): click, tick, pop, thump, whoosh, swish, chime, type, boom, riser (6 ms cos^2 tail).
- **أرقام / params:** 18 cues: thump .7/.8, whoosh .5-.7, tick .5/.6, pop .5/.6, boom .5/.8, swish .6/.8, chime .5/.6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/cues.json`

#### BEAT-150 · شبكة الإيقاع · Beat grid helper · 📦 بأمر تثبيت
- **ماذا / what:** Converts BPM or a measured beats JSON into times so picture and sound read the same clock.
- **كيف / how:** M.beats(120) -> {at(n), len(n), beat}; M.beats(json) -> list, hits, downbeats (every 4th if missing).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:89-93`

#### BEAT-151 · نقاط قطع على الإيقاع · Beat/onset cut points · 📦 بأمر تثبيت
- **ماذا / what:** Spectral-flux onsets, peak picking and rough BPM to propose cut points.
- **كيف / how:** python3 beat_cuts.py audio --every 2 --min-gap 0.5 --out beats.json (ffmpeg decode + numpy).
- **أرقام / params:** every 2nd beat, min gap 0.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/scripts/beat_cuts.py:72`

#### BEAT-152 · مستويات الصوت · Loudness targets · 📦 بأمر تثبيت
- **ماذا / what:** -14 LUFS integrated, -1 dBTP peak, music bed -18 dB under speech; measured not guessed.
- **كيف / how:** ffmpeg loudnorm I=-14:TP=-1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/video-editing-captions/SKILL.md:23`

#### BEAT-153 · طيف على ساعة الشريط · Spectrum on tape clock · 📦 بأمر تثبيت
- **ماذا / what:** Resamples the spectrogram image onto tape time so the visible terrain is what is heard, freezing on tape stops.
- **كيف / how:** K3.spectrumOnTape(img, channels, {width}).
- **أرقام / params:** width ≈ end·fps·2 (≥64)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:862`

#### BEAT-154 · هالة وجسيمات تتفاعل مع الصوت · Sound-reactive halo, motes and kick rings · 📦 بأمر تثبيت
- **ماذا / what:** Canvas light layer: halo breathes with rms, swells on kicks and flares at payoff; 72 rising motes lifted by onsets; expanding rings from kicks in the last 1.3 s.
- **كيف / how:** draw(t) in verse.html using MOTION.channels(window.SOUND).
- **أرقام / params:** halo R .62·min(W,H)·(1+.05 rms+.06 kick+.25 flare); motes r 2-9 px rise .006-.026/s; rings alpha .22·(1-dt/1.3)², 'lighter' blend
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/templates/verse.html`

#### BEAT-155 · فيلم يستمع بالرياضيات · Listen-with-math music film · 📦 بأمر تثبيت
- **ماذا / what:** Every visual value is a measured per-frame channel; the world runs on a tape clock (freezes on tape stops) while the camera keeps orbiting (bullet time); spectrogram ground; glitch accents; proven loop seam.
- **كيف / how:** motion.py channels TRACK -> MOTION.channels / spectrumOnTape / makeSpectrumGround / makeGlitchPass / makeSparks; motion.py loopcheck.
- **أرقام / params:** tape stop detection: pitch line r² > .9 and > 15 st/s, or whole-spectrum shift > 30 st/s over .25 s, held ≥ 4 frames
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/references/x-trend-2026.md` · `kosif-studio/motion/references/hyperframes-authoring.md`

#### BEAT-156 · موجة صوت · Style: Audio wave (audio-wave) · 📦 بأمر تثبيت
- **ماذا / what:** Audio-reactive waveform/bars driven by the voice or music.
- **كيف / how:** Precompute RMS envelope per 1/30s (ffmpeg astats) or Remotion visualizeAudio; smooth 100-200ms; accent attack 1-2 frames decay 150-300ms. Scaffold: python3 tools/kosif.py scaffold audio-wave <dir>.
- **أرقام / params:** pulse 1->1.04
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:audio-wave` · `kosif-tool/playbooks/music.md`

#### BEAT-157 · موسيقى · Category: Music · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'music' (49 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/music.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category music.
- **أرقام / params:** beat=60/BPM; cut on or 1 frame before beat; accent attack 1-2f decay 150-300ms; duck 8-12dB 150/400ms; -14 LUFS, TP<=-1 dBTP
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/music.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### BEAT-158 · خفض الموسيقى والجهارة · Music ducking and loudness · 📦 بأمر تثبيت
- **ماذا / what:** Duck music under voice and deliver at platform loudness.
- **كيف / how:** ffmpeg sidechain/volume automation; verify via tools/verify_video.py --lufs -14.
- **أرقام / params:** duck 8-12 dB, attack 150ms release 400ms; -14 LUFS +-1.5; TP<=-1 dBTP
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/music.md:74` · `kosif-tool/tools/verify_video.py`

#### BEAT-159 · كشف الإيقاع بالقياس · Measured beat detection · 📦 بأمر تثبيت
- **ماذا / what:** Detect beats with aubio or librosa.beat.beat_track, or tap tempo; verify 5 beats by ear.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/music.md:24`

#### BEAT-160 · غلاف التأكيد · Accent envelope / BeatPulse · 📦 بأمر تثبيت
- **ماذا / what:** Fast attack and eased decay scale pulse on each beat.
- **كيف / how:** Remotion BeatPulse: since = ((f−offset·fps) mod beat); interpolate(since,[0,2,8],[1,1.04,1]).
- **أرقام / params:** attack 1–2 frames; decay 150–300 ms; 1→1.04→1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/music.md:26` · `kosif-tool/playbooks/music.md:53-61`

#### BEAT-161 · توليد مؤثرات صوتية من وصف نصي · Text-to-sound-effects generation · 🔑 مفتاح/خدمة
- **ماذا / what:** Describe a sound (rain on tin roof, laser, forest loop) and get a rendered SFX file.
- **كيف / how:** ElevenLabs textToSoundEffects.convert({text,duration_seconds,prompt_influence}); billed per generation.
- **أرقام / params:** duration 0.5-30s, prompt_influence 0-1
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b`

#### BEAT-162 · مكتبة مؤثرات صوتية · SFX library by URL · 🔑 مفتاح/خدمة
- **ماذا / what:** A set of short hosted SFX (whoosh, whip, page-turn, switch, mouse-click, shutter, ding, record-scratch and meme sounds).
- **كيف / how:** <Audio src='https://remotion.media/whoosh.wav'/>; needs network at render; license of individual meme sounds unclear - prefer generating or licensing our own whooshes for commercial work.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/sfx.md`

#### BEAT-163 · توليد مؤثرات صوتية من نص · Text-to-SFX generation · 🔑 مفتاح/خدمة
- **ماذا / what:** Generate custom whooshes/impacts/ambiences from a prompt.
- **كيف / how:** ElevenLabs POST /v1/sound-generation with duration_seconds 0.5-30 and prompt_influence 0-1 (API key, paid). Offline alternative: synthesise with numpy/sox noise sweeps.
- **أرقام / params:** 0.5-30 s
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b/SKILL.md`

#### BEAT-164 · خطة تأليف موسيقى ElevenLabs · ElevenLabs Music composition plan · 🔑 مفتاح/خدمة
- **ماذا / what:** Generate produced/sung music as sections in whole bars with global styles, negatives, and per-section lyrics so section starts land on bar lines for video cuts.
- **كيف / how:** elevenlabs CLI or API music_v2 composition plan; section 3-120s, song 3s-10min, line <=200 chars, ~1 line/bar; instrumental sections '{instrumental, no vocals}'. Paid.
- **أرقام / params:** ~27.5 credits/s; mp3_48000_192
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music` · `kosif-atlas/skills/1511-homie/3892-music/references/COMPOSITION.md`

#### BEAT-165 · الكلمات داخل أقسام الخطة فقط · Lyrics only via plan sections · 🔑 مفتاح/خدمة
- **ماذا / what:** A prompt with lyrics beside it can return nothing sung; put words in plan sections and verify with STT; short hooks/contractions drift.
- **كيف / how:** Scribe re-transcription check, pass at ~75% word match.
- **أرقام / params:** 75%
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music/references/COMPOSITION.md`

#### BEAT-166 · برومبت الأسلوب السداسي في Suno · Suno six-layer style prompt · 🔑 مفتاح/خدمة
- **ماذا / what:** Order style descriptors genre → mood → instrumentation → vocal → BPM → production, with the genre front-loaded.
- **كيف / how:** Write 5-8 tags: specific subgenre+era, 2-3 related moods, named instruments, acoustic vocal descriptors (breathy, raspy), numeric BPM, production words; Custom mode for tags; style field ≈1000 chars, lyrics hard cap 5000 with sweet spot ≈3000, title ≈100.
- **أرقام / params:** 5-8 tags; style ≈1000 chars; lyrics ≤5000 (≈3000 best)
- **الدليل / proof:** `kosif-atlas/skills/2475-songwriting/9607-suno`

#### BEAT-167 · تجاوز الأسلوب لكل مقطع في Suno · Suno per-section style overrides · 🔑 مفتاح/خدمة
- **ماذا / what:** The lyrics field acts as a second style channel: each section tag can carry its own instrumentation and dynamics, building verse-chorus contrast for an edit.
- **كيف / how:** Use [Verse: piano only, no drums, intimate] or [Bridge | dark | sparse]; 4-7 descriptors per block (8+ gets muddy); escalate drums/harmonies chorus by chorus; strip the bridge; standard labels only (non-standard ones get sung).
- **أرقام / params:** 4-7 descriptors per section
- **الدليل / proof:** `kosif-atlas/skills/2475-songwriting/9607-suno`

#### BEAT-168 · تصنيف وسوم Suno والتلميحات المضمنة · Suno tag taxonomy and inline cues · 🔑 مفتاح/خدمة
- **ماذا / what:** Structural tags ([Intro], [Verse 1], [Pre-Chorus], [Chorus], [Bridge], [Build-Up], [Drop], [Instrumental Break], [Outro], [End], [Fade Out]), vocal tags ([Whispered], [Belted], [Falsetto], [Choir], [Rapped], [Spoken Word]) and effect tags ([Crescendo], [Silence], [Echo]).
- **كيف / how:** Tags on their own line; inline performance cues in parentheses of 1-3 words (longer gets sung); [End] for a hard stop that edits cleanly vs [Fade Out].
- **أرقام / params:** cues 1-3 words
- **الدليل / proof:** `kosif-atlas/skills/2475-songwriting/9607-suno`

#### BEAT-169 · حيل الأداء الصوتي في Suno · Suno vocal performance tricks · 🔑 مفتاح/خدمة
- **ماذا / what:** Community-validated lyric formatting that shapes delivery (medium confidence).
- **كيف / how:** ALL-CAPS on 1-2 turning-point words per section for grit; 3-5 extra vowels for melisma (20+ glitches); '...' gives a 0.5-2 s breath pause; hyphenated letters for staccato; one phrase per line for melodic separation.
- **أرقام / params:** caps 1-2 words; +3-5 vowels; pause 0.5-2 s
- **الدليل / proof:** `kosif-atlas/skills/2475-songwriting/9607-suno`

#### BEAT-170 · أخطاء Suno الشائعة وحلولها · Suno anti-patterns and fixes · 🔑 مفتاح/خدمة
- **ماذا / what:** Common prompt mistakes and the rewrites that fix them.
- **كيف / how:** Artist names are blocked → describe the sound; '(x2)' is ignored → write the line twice; 'no drums' alone fails → 'piano only, no drums'; 3+ equal genres mush → one anchor + one accent ('synth-pop with dream-pop textures'); unwanted vocals → lyrics '[Melodic Instrumental]' + 'instrumental, no vocals'; drop gender descriptors when a Voice/Custom Model is active.
- **أرقام / params:** ≤2 genres (anchor+accent)
- **الدليل / proof:** `kosif-atlas/skills/2475-songwriting/9607-suno`

#### BEAT-171 · تحرير Suno: الغلاف والتمديد واستبدال المقطع · Suno editing: Cover, Extend, Replace Section, Personas · 🔑 مفتاح/خدمة
- **ماذا / what:** Re-style a song keeping its melody (Cover), lengthen from a chosen point (Extend + Get Whole Song), regenerate one middle section with 2 alternates (Replace Section, Pro/Premier), and reuse a song's vibe (Persona).
- **كيف / how:** Use Replace Section to fix one bad verse instead of regenerating; set 'Make Same Length' off for longer breaks; use a structural tag in extension lyrics; sliders Weirdness/Style Influence (community starts: polished pop 30/75, experimental 75/50), Audio Influence ≈80 + Style 70 for faithful upload extension; Duration slider reported 10 s-6 min in 5 s steps.
- **أرقام / params:** Weirdness 30/Style 75 pop; Audio Influence ≈80
- **الدليل / proof:** `kosif-atlas/skills/2475-songwriting/9607-suno`

#### BEAT-172 · تقسيم Suno إلى مسارات وملفات بإيقاع مقفل · Suno stems, tempo-locked WAV and MIDI for editing · 🔑 مفتاح/خدمة
- **ماذا / what:** Suno exports stems that snap to a DAW grid, which makes beat-cut editing and ducking easier.
- **كيف / how:** Split from Mix (2 stems) and Auto Split (up to 12) on Pro/Premier, Advanced Split (~100 instruments) Premier only; export MP3, WAV, Tempo-Locked WAV, MIDI; Get MIDI costs 10 credits; Warp Markers fix timing; use the drum stem for onset/beat detection to drive cuts.
- **أرقام / params:** 2 / 12 / ~100 stems; MIDI 10 credits
- **الدليل / proof:** `kosif-atlas/skills/2475-songwriting/9607-suno`

#### BEAT-173 · اللغة والأنماط العربية في Suno · Suno language and Arabic-flavoured genres · 🔑 مفتاح/خدمة
- **ماذا / what:** Suno auto-detects language from the lyrics; the sourced top tier is English, Spanish, Portuguese, French, Japanese, Korean, Mandarin, while Arabic quality is unsourced.
- **كيف / how:** Write lyrics directly in Arabic, name the language/style in the style field, and prefer instrumental beds when diction matters; genre taxonomy lists Rai (90-130 BPM, modal, synth + accordion + darbouka + bass); describe maqam colour with instruments rather than artist names.
- **أرقام / params:** Rai 90-130 BPM
- **الدليل / proof:** `kosif-atlas/skills/2475-songwriting/9607-suno`

#### BEAT-174 · قوالب الأنماط الموسيقية في Suno · Suno genre templates · 🔑 مفتاح/خدمة
- **ماذا / what:** Twelve ready genre templates (pop, rock, hip-hop, trap, edm, jazz, classical, folk, metal, ambient, lofi, rnb) each with style prompt, lyric shell and tweak knobs, plus a taxonomy with BPM ranges.
- **كيف / how:** Example dark ambient bed: 60 BPM, no percussion, infinite reverb tail, field recordings, [Melodic Instrumental]; trailer music 90-140 BPM with big drums, brass swells, string ostinati, risers — good under motion-graphics reveals.
- **أرقام / params:** ambient 60 BPM; trailer 90-140 BPM
- **الدليل / proof:** `kosif-atlas/skills/2475-songwriting/9607-suno`

#### BEAT-175 · خطة تأليف ElevenLabs بالموازير · ElevenLabs Music composition plan in whole bars · 🔑 مفتاح/خدمة
- **ماذا / what:** music_v2 accepts a composition plan of sections, each with exact length and its own styles, so section starts land on bar lines that cuts can use.
- **كيف / how:** Section seconds = bars × beatsPerBar × 60 / bpm (rounded to ms); first chunk carries global styles, tempo and key; later chunks repeat tempo and add local styles; avoid list → negative styles; instrumental sections get '{instrumental, no vocals}'; sung words only inside plan sections (lyrics beside a prompt came back unsung); output_format is a query option (mp3_48000_192).
- **أرقام / params:** section 3-120 s; song 3 s-10 min; line ≤200 chars; ≈27.5 credits/s
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3892-music`

#### BEAT-176 · عزل الحوار بالذكاء الاصطناعي قبل المونتاج · AI dialogue isolation before editing · 🔑 مفتاح/خدمة
- **ماذا / what:** Strip background noise/music from a user's voice track to get clean speech for captions and ducking.
- **كيف / how:** ElevenLabs POST /v1/audio-isolation (or /stream); keep the original untouched and work on a copy; then transcribe for word timing.
- **أرقام / params:** ≤500 MB; ≤1 h; MP3/WAV/M4A/FLAC/OGG/WEBM
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b`

#### BEAT-177 · تنظيف الصوت محلياً · Local voice cleaning via bridge (audiolab.py) · 🔑 مفتاح/خدمة
- **ماذا / what:** Optional denoise/voice isolation on the user's own machine through the KOSIF bridge; the cleaned WAV is added as a voice track.
- **كيف / how:** POST BRIDGE/api/clean with {mode:'voice'} + file; header X-Basma-Method names the method. Bridge script basma_bridge.py is not in this repo.
- **الدليل / proof:** `app/public/js/00_editor.js:2645`

#### BEAT-178 · حزمة أغنية لـ Suno/Udio · Suno/Udio song package · 🔑 مفتاح/خدمة
- **ماذا / what:** Everything an AI music generator needs to produce a usable song, including Arabic dialect and maqam guidance.
- **كيف / how:** Title + English style prompt (<= 200 chars: genre, mood, BPM, key, instruments, vocal, era) + exclude styles + lyrics with [Intro][Verse 1][Pre-Chorus][Chorus][Verse 2][Bridge][Final Chorus][Outro], hook repeated 2-4x, rhyme scheme; tashkeel on risky words; alt-genre version + 15 s reel hook. Suno tag order [Genre][BPM][Mood][Instruments][Vocal][Era].
- **أرقام / params:** style prompt <= 200 chars; dialects Khaleeji, Egyptian, Levantine, Iraqi, Sudanese, Maghrebi, Fusha
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/references/books-drive-ledger.md`

#### BEAT-179 · جدول تصميم المؤثرات الصوتية · SFX design sheet · 🔑 مفتاح/خدمة
- **ماذا / what:** Timecoded sound-design plan with prompts for AI SFX tools.
- **كيف / how:** Table: timecode | layer (ambience/foley/hard FX/music/UI) | description | level dBFS | pan | prompt for ElevenLabs SFX or Stable Audio.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md`

#### BEAT-180 · حزمة الأطلس للصوت والقصة · Atlas skill pack: audio/voice/story skills · 🔑 مفتاح/خدمة
- **ماذا / what:** Skill ids curated for the audio engineer, voice director and storyteller agents.
- **كيف / how:** kosif_atlas_read skill_id=<id>.
- **أرقام / params:** audio: elevenlabs-core-workflow-b 5515, game-audio-procedural 4163, transcribe 1994, hyperframes 10378 (Apache), music 3892, sound 3901, write-realtime-audio-code 2280, choose-audio-dsp-architecture 8508; voice: elevenlabs 5514/5519, speech-recognition-and-synthesis 8616, voice-agent-architecture-an…
- **الدليل / proof:** `kosif-one/tools/kosif-omni/tools/swarm_skillpacks.json`

#### BEAT-181 · قطع متزامن مع الإيقاع · Beat-locked cuts · 👁 شوهد في فيديو
- **ماذا / what:** cut every 2 or 4 beats (0.4/0.8 s)
- **الدليل / proof:** `style:pm-topi-003-b0e12c` · `style:pm-zaqailo-212ad3`

#### BEAT-182 · صوت خربشة طباشير مولّد · Procedural chalk scratch sound · 👁 شوهد في فيديو
- **ماذا / what:** band-pass noise 0.7-4.5 kHz, modulated by 7-11 Hz pressure pulses, plus short grain crackles; gate it while the chalk is drawing
- **أرقام / params:** per-stroke envelope
- **الدليل / proof:** `style:chalkboard`

#### BEAT-183 · مونتاج كلمات خاطفة على الإيقاع · Flash-word beat montage · 👁 شوهد في فيديو
- **ماذا / what:** Hard-cut one giant uppercase word per beat with small footer label and page counter 01/05
- **أرقام / params:** ~233 ms per word (~4 per second), 5 words
- **الدليل / proof:** `style:pm-0xfemyn-e114d3`

#### BEAT-184 · انفجار ذروة متزامن مع الموسيقى · Explosion climax on beat · 👁 شوهد في فيديو
- **ماذا / what:** countdown → white flash → fireball (noise-displaced emissive sphere expanding) timed to music hit
- **أرقام / params:** flash at beat, fireball expand 1.5 s ease-out
- **الدليل / proof:** `style:pm-ajith-io-4c248f`

#### BEAT-185 · قطع على شبكة الإيقاع · Beat-grid cuts · 👁 شوهد في فيديو
- **ماذا / what:** scene change every 4 beats at 120 BPM
- **أرقام / params:** 1.875 s
- **الدليل / proof:** `style:pm-ajith-io-b5626e`

#### BEAT-186 · دفعة لقطات على الإيقاع مع شارة اسم الصانع · Beat-cut reel burst with handle chips · 👁 شوهد في فيديو
- **ماذا / what:** on the music drop hard-cut 3 full-bleed clips one beat each; each carries a dark rounded chip with avatar + @handle inside the safe area bottom-left
- **أرقام / params:** 120 BPM = 0.5 s per cut, chip #111 radius 999 px, text white 600
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### BEAT-187 · مخطط أعمدة يتزامن مع الإيقاع · Beat-synced bar chart · 👁 شوهد في فيديو
- **ماذا / what:** Compute beat times (e.g., 128 BPM = 0.469 s); playhead sweeps, a bar spikes on each beat with a timestamp label; caption states that the chart is the music
- **أرقام / params:** beat interval 60/BPM; spike 100 ms attack, 300 ms decay
- **الدليل / proof:** `style:pm-fionntobin-97b7af`

#### BEAT-188 · إطار HUD بعداد المقاطع ونصوص مشفرة تتفكك · Beat-bar HUD with scramble labels · 👁 شوهد في فيديو
- **ماذا / what:** corner brackets + mono labels; bottom-right 'BPM · BAR n/08' increments every bar (60/BPM*4 s); chapter name decodes from random glyphs to final over ~300 ms
- **أرقام / params:** 128 BPM -> bar 1.875 s; scramble charset A-Z0-9*+_
- **الدليل / proof:** `style:pm-ghinaiya-nirmal-5d8fec`

#### BEAT-189 · مسار قفز مربوط بالإيقاع · Beat-mapped bounce path · 👁 شوهد في فيديو
- **ماذا / what:** Precompute beat times; place platform i so ballistic arc from platform i-1 lands exactly at beat[i]; solve vy = (dy + 0.5 g t^2)/t per hop
- **أرقام / params:** g≈-20 u/s², hop duration = beat interval (~0.4-0.6 s)
- **الدليل / proof:** `style:pm-gorden-sun-041f56`

#### BEAT-190 · حروف مفرغة تمتلئ مع موجة صوتية · Outline-to-fill letters with waveform · 👁 شوهد في فيديو
- **ماذا / what:** start with stroke-only letters, fill them left->right with footage while a row of thin bars below animates to audio amplitude
- **أرقام / params:** fill 120 ms stagger per letter, 60 bars
- **الدليل / proof:** `style:pm-influencer-seo-ce8c33`

#### BEAT-191 · مونتاج إيقاعي · Beat montage · 👁 شوهد في فيديو
- **ماذا / what:** cut every beat 0.2-0.5 s
- **الدليل / proof:** `style:pm-jacksonfall-54b2ac`

#### BEAT-192 · جدولة النغمات بمقذوفات عكسية · Inverse-ballistic note scheduling · 👁 شوهد في فيديو
- **ماذا / what:** For each note time t and key position, solve launch velocity from launcher so the parabola hits the key exactly at t (v = (dx/T, (dy - 0.5 g T²)/T)); fire at t - T
- **أرقام / params:** g = 1500 px/s², flight T 0.6-1.2 s
- **الدليل / proof:** `style:pm-kamstudiolabs-447565`

#### BEAT-193 · كل ارتداد يعزف النغمة التالية · Bounce-to-note sonification · 👁 شوهد في فيديو
- **ماذا / what:** precompute collision times from the deterministic sim; at each, schedule next note of a melody/scale via Web Audio oscillator (short pluck envelope) or render offline with OfflineAudioContext
- **أرقام / params:** attack 5 ms, decay 300 ms, pentatonic scale
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### BEAT-194 · كشف كلمة مع موجة صوتية · Waveform word reveal · 👁 شوهد في فيديو
- **ماذا / what:** Draw dense vertical coral bars as audio waveform beneath a serif line; amplitude from audio RMS per frame
- **أرقام / params:** ~200 bars, gap 2px, height ∝ RMS
- **الدليل / proof:** `style:pm-kloss-xyz-15182a`

#### BEAT-195 · لحظة سواد قبل الذروة · Silence-before-drop black beat · 👁 شوهد في فيديو
- **ماذا / what:** cut to near-black with only a tiny mono code line for ~0.5-1 s, then flash into the climax on the drop
- **أرقام / params:** hold 0.5-1 s
- **الدليل / proof:** `style:pm-maxalexweber-67688b`

#### BEAT-196 · قطعات حادة مضبوطة على الإيقاع · Beat-locked hard cuts · 👁 شوهد في فيديو
- **ماذا / what:** Compute beat times from BPM (t = offset + k*60/BPM) and place hard cuts ~2 frames before chosen beats; add whoosh SFX peaking on the cut
- **أرقام / params:** 124 BPM, beat = 0.484 s
- **الدليل / proof:** `style:pm-notdwd-7de38a`

#### BEAT-197 · كلمة بين أعمدة موجة صوتية · Waveform-flanked word · 👁 شوهد في فيديو
- **ماذا / what:** vertical bars left/right of the word driven by audio amplitude (or synthetic), word sits on top
- **أرقام / params:** 60-80 bars, coral
- **الدليل / proof:** `style:pm-prasenx-8d9323`

#### BEAT-198 · موسيقى مولّدة بالكود ومقفلة على القطعات · Code-synthesized beat-locked soundtrack · 👁 شوهد في فيديو
- **ماذا / what:** define BPM, compute beat times, synthesize kick/snare/bass/arp with oscillators+noise in OfflineAudioContext or numpy; schedule every visual cut on beat frames
- **أرقام / params:** ~120-130 BPM, cuts on 1/8 notes in climax
- **الدليل / proof:** `style:pm-prasenx-8d9323`

#### BEAT-199 · شيفرة تتوهج مع الإيقاع · Beat-highlighted code · 👁 شوهد في فيديو
- **ماذا / what:** Highlight token box on each step event
- **أرقام / params:** per 1/16
- **الدليل / proof:** `style:pm-rames-jusso-589f80`

#### BEAT-200 · بطاقة نتيجة تتبدل أسلوبها على إيقاع النوتات · Style-roll result card on 16th notes · 👁 شوهد في فيديو
- **ماذا / what:** Swap the result image every 16th note (60/BPM/4 s) among style variants of the same subject; a black pill chip rolls vertically to the new style name; thumbnail strip highlights current
- **أرقام / params:** 130 BPM -> 115 ms per swap, chip roll 80 ms
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### BEAT-201 · واجهة عداد البارات الإيقاعية · Bar-counter HUD · 👁 شوهد في فيديو
- **ماذا / what:** HUD showing BPM, 4 beat squares filled by beat index, 'BAR n/8' and a bottom progress line; switch scene exactly on bar boundaries
- **أرقام / params:** 128 BPM → beat 469 ms, bar 1.875 s
- **الدليل / proof:** `style:pm-roundtablespace-d3a1be`

#### BEAT-202 · قطع الفصول على المازورة · Bar-locked chapter cuts · 👁 شوهد في فيديو
- **ماذا / what:** Each chapter lasts exactly one bar at the stated BPM; HUD bar counter advances on each cut
- **أرقام / params:** 128 BPM -> 1.875 s per chapter, 8 chapters
- **الدليل / proof:** `style:pm-sahildesigner23-ee3155`

#### BEAT-203 · شريط موجة الإيقاع · Beat waveform bar strip · 👁 شوهد في فيديو
- **ماذا / what:** row of thin vertical bars across the frame whose heights pulse with the beat; every Nth bar in accent colour
- **أرقام / params:** 144 BPM, bar 3px, accent lime
- **الدليل / proof:** `style:pm-shneural-2abdfa`

#### BEAT-204 · قطع على الإيقاع · BPM beat cuts · 👁 شوهد في فيديو
- **ماذا / what:** scene every 3 beats at 120 BPM = 1.5 s
- **الدليل / proof:** `style:pm-sudiyasa-f48ac9`

#### BEAT-205 · عدّاد مازورة وضربة في الواجهة · Beat/bar HUD counter · 👁 شوهد في فيديو
- **ماذا / what:** derive bar = floor(t*BPM/60/4)+1, beat = floor(t*BPM/60)%4+1 and print 'BAR 04 · BEAT 4' + timecode each frame
- **أرقام / params:** BPM 120, mono 11 px
- **الدليل / proof:** `style:pm-tankazunori0914-0fc886`

#### BEAT-206 · خط زمني مقفل على الإيقاع · BPM beat grid timeline · 👁 شوهد في فيديو
- **ماذا / what:** Define bpm=120 -> beat=0.5 s; schedule every hit on beat indices, show 'Bxx/40' counter; phrases of 8 beats (4 s) per message
- **أرقام / params:** 120 BPM; 40 beats; phrase 8
- **الدليل / proof:** `style:pm-techhalla-7acbc2`

#### BEAT-207 · كلمات تتبدل على الإيقاع · BPM beat-cut word flashes · 👁 شوهد في فيديو
- **ماذا / what:** at 120 BPM place hard cuts on beats/half-beats (0.5/0.25 s); each cut shows one word or a full colour flash
- **أرقام / params:** beat = 60/BPM s; 6-8 cuts in 2 s
- **الدليل / proof:** `style:pm-tequilafunks-97f6c9`

#### BEAT-208 · أعمدة إيقاع تحت كلمة · Equaliser under word · 👁 شوهد في فيديو
- **ماذا / what:** Row of thin bars with heights from audio FFT or noise, under condensed headline
- **أرقام / params:** 40–60 bars
- **الدليل / proof:** `style:pm-tolgayhickiran-e90799`

#### BEAT-209 · شبكة تنبض مع الإيقاع · Beat grid pulse · 👁 شوهد في فيديو
- **ماذا / what:** Grid of diamonds scale/colour per beat index
- **أرقام / params:** 12x8
- **الدليل / proof:** `style:pm-topi-003-9ca6b5`

#### BEAT-210 · قطع على إيقاع البار · BPM bar cut grid · 👁 شوهد في فيديو
- **ماذا / what:** cut every 4 beats: 60/BPM*4
- **أرقام / params:** 128 BPM -> 1.875 s
- **الدليل / proof:** `style:pm-umangratani-57f86a`

#### BEAT-211 · قطع على شبكة الإيقاع · Beat-grid cutting · 👁 شوهد في فيديو
- **ماذا / what:** cut every 0.47 s, stutter cuts 60ms near climax
- **الدليل / proof:** `style:pm-zheke-38deff`

#### BEAT-212 · صوت ماركر مولد بالكود · Procedural marker squeak · 👁 شوهد في فيديو
- **ماذا / what:** filtered noise 1.8-7 kHz, amplitude modulated by 9-14 Hz pulses with short squeaks; click per word; cap snap at end
- **أرقام / params:** gate per stroke
- **الدليل / proof:** `style:whiteboard`

#### BEAT-213 · ربط الترددات بخصائص بصرية · Audio-to-visual property mapping · 📄 موصوف
- **ماذا / what:** Bass drives scale pulses, mids drive shape morphs, treble drives glow; text stays subtle, shapes can swing hard.
- **كيف / how:** bands[0] -> scale; bands[4-8] -> borderRadius/width; bands[12-14] -> textShadow/boxShadow glow; text 3-6% scale variation; backgrounds/shapes 10-30%. Animate the content, not a generic equalizer.
- **أرقام / params:** text 3-6%; shapes 10-30%
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/audio-reactive.md`

#### BEAT-214 · ترجمة تتفاعل مع الصوت · Audio-reactive captions at build time · 📄 موصوف
- **ماذا / what:** For music, read per-frame band energy for each caption group's time range and bake scale/glow into the tweens instead of per-frame callbacks.
- **كيف / how:** peakBass from bands[0..1], peakTreble from bands[6..7]; tl.to(group,{scale:1+peakBass*0.06, textShadow:`0 0 ${peakTreble*12}px rgba(255,255,255,${peakTreble*0.4})`, duration:0.3}, start); reset at end-0.15.
- **أرقام / params:** scale +6% max; glow 12px
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/dynamic-techniques.md`

#### BEAT-215 · مونتاج على شبكة الإيقاع · Beat-grid trailer edit · 📄 موصوف
- **ماذا / what:** Cut footage so every cut lands on a bar line of the music, title on the first bar, shots of one bar each, slow push-in on each shot.
- **كيف / how:** Read tempo/beat/bar times; title card one bar; each shot one bar (two beats if a bar >2.6s); end card >=2.5s; choose busiest non-overlapping motion windows; push-in to 1.25x toward highest-change area; verify every cut within one frame of its beat; capture 2-3x target length.
- **أرقام / params:** push 1.25x; end card >=2.5s; sync within 1 frame
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/TRAILER.md` · `kosif-atlas/skills/1511-homie/3903-video/SKILL.md`

#### BEAT-216 · أطوال أصوات واجهة الاستخدام · UI sound feedback lengths · 📄 موصوف
- **ماذا / what:** Short UI sound durations and characters to pair with on-screen clicks in product films.
- **كيف / how:** Synthesize with WebAudio/sox or pick licensed SFX; place on the frame where the press ring appears.
- **أرقام / params:** confirmations 50-200ms (completions up to 1s); success rising pitch 100-300ms; error low buzz 100-200ms; notification chime 200-500ms; typing click 20-50ms; delete whoosh 200-400ms
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md`

#### BEAT-217 · مقطع دعائي مقصوص على الإيقاع · Beat-grid trailer from a capture · 📄 موصوف
- **ماذا / what:** Find the song's bar lines, pick the busiest motion moments from the capture, one bar per shot, title card one bar, end card on the remainder; verify each cut lands within one frame of a sound onset.
- **كيف / how:** Beat/onset detection (librosa/aubio if installed, or ffmpeg + numpy energy), motion score via frame differencing, EDL JSON, ffmpeg concat.
- **أرقام / params:** every cut on a bar line; sync tolerance 1 frame; 30 fps
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video` · `kosif-atlas/skills/1511-homie/3903-video/references/TRAILER.md`

#### BEAT-218 · توجيه الموسيقى مقطعًا بمقطع · Section-by-section music direction · 📄 موصوف
- **ماذا / what:** Music is planned per section with an emotional target: intro bright/curious, core focused and under the voice, key reveal with a lift or swell, outro resolving; music dips under insights and rises slightly in B-roll and demos.
- **كيف / how:** Create a table Section | emotional target | music direction | notes, flag hard cuts and swells on brand moments; implement as volume automation/sidechain ducking in ffmpeg (sidechaincompress) or Web Audio gain envelopes in the HTML timeline. Never alter the user's voice track.
- **الدليل / proof:** `kosif-atlas/skills/3067-youtube/13229-creator-visual-director/SKILL.md` · `kosif-atlas/skills/3067-youtube/13224-creator-editor-brief/SKILL.md`

#### BEAT-219 · مزامنة المؤثرات وترتيب المكساج · Sound design sync and mix order · 📄 موصوف
- **ماذا / what:** Align the audible transient of an effect (not the file start) to the visible action at one-frame accuracy; avoid fixed relative fader rules; work clip gain -> EQ -> dynamics -> time automation/ducking -> bus; time ducking entries and exits to sentences and breaths to avoid pumping; check mono.
- **كيف / how:** In ffmpeg: adelay to the transient offset, sidechaincompress or volume automation for ducking; detect transients with a simple onset envelope in numpy.
- **أرقام / params:** 1-frame sync
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound/SKILL.md`

#### BEAT-220 · جدول تحويل الإيقاع إلى إطارات · Tempo-to-frame grid table · 📄 موصوف
- **ماذا / what:** Exact cuts on a musical grid need a whole number of frames per bar: at 60 fps frames/bar = 14400 / BPM and frames/beat = 3600 / BPM.
- **كيف / how:** Good tempos at 60 fps: 75 BPM 192 f/bar 3.2 s; 90 BPM 160 f/bar; 100 BPM 144 f/bar 2.4 s; 120 BPM 120 f/bar 2.0 s; 144 BPM 100 f/bar; 150 BPM 96 f/bar 1.6 s; 180 BPM 80 f/bar. Half-bar cuts need even frames/bar; quarter-bar cuts need integer frames/beat (fails at 96 and 160). At 30 fps halve the frame counts. Use to choose a beat grid when the user's music tempo is known (detect BPM with librosa/aubio or numpy onset autocorrelation).
- **أرقام / params:** frames/bar=14400/BPM @60fps; frames/beat=3600/BPM
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/concept-and-music.md`

#### BEAT-221 · ربط ضربات المونتاج بنبضات الموسيقى · Edit hits married to music transients · 📄 موصوف
- **ماذا / what:** Every edit accent (cut, caption slam, flash, logo slam) has a matching transient in the cue (crash, impact, stab, kick); cue structure follows the beat sheet (riser into cold-open hit, half-time sting, full drop, breakdown building to climax, hit-stop gap, logo slam, cadence fading within the last b…
- **كيف / how:** Master the cue around -16 LUFS integrated with peaks under -1 dBFS before adding SFX, then normalise the final mix to -14; verify every hit onset within 10 ms of its bar position. With the user's own music, detect onsets and snap cut points to them instead.
- **أرقام / params:** hit tolerance 10 ms; cue -16 LUFS; final -14 LUFS
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/concept-and-music.md`

#### BEAT-222 · MG-028 توقيع صوتي موجز · MG-028 Sonic-logo pulses · 📄 موصوف
- **ماذا / what:** The symbol pulses three times on the sound logo's hits, then returns to its true proportions.
- **كيف / how:** 0-1.2 s three pulses, 1.2-1.8 s settle, 1.8-3 s hold; markers on hits then a limited scale per pulse, never beyond the brand guideline's allowance. Hit times from the audio (ffmpeg astats/silencedetect onsets or manual markers).
- **أرقام / params:** 3 s; 3 pulses
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-brand-identity.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### BEAT-223 · MG-091/099 نص على الضربات وتقطيع على الجملة الموسيقية · MG-091/099 Beat-locked words and phrase cuts · 📄 موصوف
- **ماذا / what:** Each beat reveals one word of a short phrase, then the whole phrase holds (MG-091); four short shots then a longer hold at the end of a musical phrase so the montage breathes (MG-099).
- **كيف / how:** MG-091: 0-2 four words on beats, 2-4 read - skip beats rather than exceed reading speed. MG-099: 0-4 four shots, 4-8 closing shot; markers on the musical build, consistent simple transitions, match shot motion so rhythm doesn't override meaning. Beats from the real file (librosa/aubio need install; ffmpeg onset heuristics or manual markers otherwise).
- **أرقام / params:** 4 s / 8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-music-sports.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### BEAT-224 · MG-094/098 مسار الكرة وخطوط السرعة · MG-094/098 Trajectory path and local speed lines · 📄 موصوف
- **ماذا / what:** After a freeze a dashed path shows the ball's direction and end point (MG-094); short lines appear behind a moving body and vanish when it stops (MG-098).
- **كيف / how:** MG-094: 0-2 play, 2-3 freeze, 3-5 draw, 5-6 resume; an estimated path is not a measurement. MG-098: 0-0.5 prep, 0.5-3 lines, 3-4 out; line direction tied to the body's speed, never over faces or the key action. SVG dashed paths over ffmpeg tpad freeze.
- **أرقام / params:** 6 s / 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-music-sports.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### BEAT-225 · MG-096 موجة صوت حول الغلاف · MG-096 Amplitude-reactive bars around cover art · 📄 موصوف
- **ماذا / what:** A few bars around a cover image react to the track's loudness.
- **كيف / how:** 0-1 enter, 1-7 react, 7-8 exit; convert audio to per-frame values and bind scale within a limited range. Call it loudness-reactive unless real frequency analysis is done. Local: ffmpeg astats/ebur128 per frame (or showfreqs for real spectrum) -> JSON -> HTML bars.
- **أرقام / params:** 8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-music-sports.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### BEAT-226 · جدول سرعات تناسب شبكة الإيقاع · Beat-grid friendly BPM table · 📄 موصوف
- **ماذا / what:** Cuts land exactly on the music only if a bar is a whole number of video frames and of audio samples. At 60 fps frames/bar = 14400/BPM, frames/beat = 3600/BPM.
- **كيف / how:** Choose BPM from: 75 (192 f/bar), 90 (160), 100 (144), 120 (120), 144 (100), 150 (96), 180 (80) at 60 fps; quarter-bar cuts need integer frames/beat (avoid 96/160 frame bars). At 30 fps halve the counts.
- **أرقام / params:** 75/90/100/120/144/150/180 BPM
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/concept-and-music.md`

#### BEAT-227 · عزل الصوت وتنظيفه · Audio isolation / voice cleanup · 📄 موصوف
- **ماذا / what:** Remove background noise from dialogue before transcription or mixing.
- **كيف / how:** Local: ffmpeg afftdn=nf=-25, arnndn=m=model.rnnn (RNNoise; model file needed), anlmdn, highpass=f=80,lowpass=f=12000, adeclick. Cloud: ElevenLabs POST /v1/audio-isolation.
- **أرقام / params:** afftdn nf -25 dB; HPF 80 Hz
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b/SKILL.md` · `kosif-atlas/skills/2261-conversational-ai-voice-engineering/8616-speech-recognition-and-synthesis/SKILL.md`

#### BEAT-228 · أدوار طبقات الصوت · Sound layer roles · 📄 موصوف
- **ماذا / what:** Build sound in roles: dialogue, room tone/ambience, real action foley, creative SFX (whoosh, impact, riser, graphic accents — never logged as real sound), tonal layers (pads/drones) and music; each layer must differ in frequency/attack/body/tail — duplicating a sample is not texture.
- **كيف / how:** Lay per-role tracks; sync the audible transient (not file start) to the action at 1-frame precision; ffmpeg adelay/atrim/amix
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound/references/sound-design-reference.md`

#### BEAT-229 · إيقاف الموسيقى وعودتها · Music stop/re-entry grammar · 📄 موصوف
- **ماذا / what:** Make room for speech by pulling drum/melody stems or ending music at a phrase end and holding space with room tone/pad/drone; when music stops keep the reverb tail; land reverse swells/risers on the next downbeat or scene change; switch songs at phrase ends — crossfade if compatible, else tail -> am…
- **كيف / how:** ffmpeg: areverse+afade for reverse swell, acrossfade=d=..:c1=tri:c2=tri, afade out on phrase end; keep tails as separate derived files
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound/SKILL.md`

#### BEAT-230 · خفض الموسيقى تحت الكلام · Speech-first ducking · 📄 موصوف
- **ماذا / what:** Do not rely on fixed -6/-12 dB offsets; decide the hero sound per passage and go clip gain -> EQ carve -> dynamics -> automation/sidechain ducking -> bus.
- **كيف / how:** ffmpeg: [music][voice]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[ducked]; amix; or volume automation from transcript speech spans; EQ notch 2-4 kHz on music
- **أرقام / params:** ratio 6-10; attack 20 ms; release 250-400 ms
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound/SKILL.md` · `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/gotchas.md`

#### BEAT-231 · تجهيز الموسيقى قبل الميكس · Hero music premaster · 📄 موصوف
- **ماذا / what:** Master the music cue around -16 LUFS with peaks under -1 dBFS so SFX can sit on top before the final -14 LUFS pass; cue sample rate resampled to 48 kHz for video.
- **كيف / how:** loudnorm=I=-16:TP=-1 on cue; aresample=48000
- **أرقام / params:** -16 LUFS cue, -14 final
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4173-game-trailer/references/gotchas.md`

#### BEAT-232 · صوت كتابة تحت ظهور النص · Typing SFX under caption reveal · 📄 موصوف
- **ماذا / what:** Lay a soft keyboard-typing SFX across the exact reveal span of a typewriter caption.
- **كيف / how:** SFX track aligned to reveal start/end from timeline.
- **أرقام / params:** ~2s
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template`

#### BEAT-233 · الموجة والطيف كعنصر بصري · Waveform/spectrum as a visual asset · 📄 موصوف
- **ماذا / what:** When on-brief (podcast, music promo), render animated waveform or spectrum bars.
- **كيف / how:** ffmpeg showwaves/showspectrum/avectorscope filters, or SVG/Canvas from band JSON.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10377-gsap/scripts/extract-audio-data.py` · `kosif-atlas/skills/2760-charly-tools/10938-songsee`

#### BEAT-234 · لوحات الأنواع الموسيقية · Genre palettes (BPM/swing/instrument) · 📄 موصوف
- **ماذا / what:** Starting points: synth-funk 140-160 swing .08-.12; DnB 165-180; boss rock 160-180; chiptune 120-180; synth-pop 120-135; ambient 60-90; horror 50-80.
- **كيف / how:** Feed into score JSON.
- **أرقام / params:** see what
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/music-composition.md`

#### BEAT-235 · ألحان أصلية فقط · Original melodies only · 📄 موصوف
- **ماذا / what:** Never transcribe or imitate a recognisable tune; 'in the spirit of' means genre conventions.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural`

#### BEAT-236 · تشريح المؤثر بثلاث طبقات · SFX three-layer anatomy · 📄 موصوف
- **ماذا / what:** Build hits/whooshes as transient (0-20ms, material), body (20-300ms, meaning), tail (100ms-2s, space).
- **كيف / how:** numpy synth or layered samples; transient on the visual contact frame; end envelope at zero, 0.5ms/<=15ms fades.
- **أرقام / params:** 0-20 / 20-300 / 100-2000 ms
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/sfx-design.md`

#### BEAT-237 · دلالات النغمة · Pitch/interval semantics · 📄 موصوف
- **ماذا / what:** Rising = gain/positive, falling = loss; major intervals/bells = reward; minor 2nds/tritones = danger; low thump = weight; low-pass = distance.
- **كيف / how:** Choose SFX gestures to match on-screen meaning.
- **أرقام / params:** jump 80-200ms, 1-1.6 oct
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/sfx-design.md`

#### BEAT-238 · وضوح الصوت على سماعة الهاتف · Phone-speaker audibility · 📄 موصوف
- **ماذا / what:** Below ~300Hz phones play almost nothing: add a knock/click above to any thud; danger cues need 1-4kHz content.
- **كيف / how:** EQ layering; check through phone-speaker band sim.
- **أرقام / params:** 300Hz, 1-4kHz
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/sfx-design.md`

#### BEAT-239 · تنويع لتجنب الملل · Anti-fatigue variants · 📄 موصوف
- **ماذا / what:** Repeated SFX get 3-4 round-robin variants (pitch ±1 semitone, filter ±15%) or runtime pitch jitter ±3-5%.
- **كيف / how:** Render variants with seeds; alternate.
- **أرقام / params:** 3 variants
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound` · `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/sfx-design.md`

#### BEAT-240 · بداية المؤثر بلا تأخير · Zero-latency transient start · 📄 موصوف
- **ماذا / what:** An effect starting 30ms late feels laggy; trim leading silence, align audible transient not file start.
- **كيف / how:** ffmpeg silenceremove start; align transient to action frame.
- **أرقام / params:** 30ms
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound` · `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound`

#### BEAT-241 · ورقة توزيع أدوار الصوت · Sound-role cue sheet · 📄 موصوف
- **ماذا / what:** Classify every sound: voice/location, room tone/ambience, Foley, creative SFX (whoosh/impact/riser), tonal/music, and deliberate silence; log cue id, TC, intent, asset, review reason.
- **كيف / how:** Cue sheet CSV feeding timeline tracks SFX_DETAIL, SFX_TRANSITION, TONAL, MUSIC_A/B.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound`

#### BEAT-242 · ملء الصمت بنبرة الغرفة · Room tone fills · 📄 موصوف
- **ماذا / what:** Fill digital-silence holes from cuts with matching room tone to keep space continuous.
- **كيف / how:** Loop a clean room-tone segment under speech gaps.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound`

#### BEAT-243 · تعديل طول الموسيقى على الجمل · Edit music to length on phrases · 📄 موصوف
- **ماذا / what:** Shorten/extend a track by cutting at matching phrase/bar/downbeat points.
- **كيف / how:** Detect bars, cut at bar n and splice at bar m with 10-30ms crossfade.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound` · `kosif-atlas/skills/1511-homie/3903-video`

#### BEAT-244 · خفض الموسيقى تحت الصوت · Ducking music under voice · 📄 موصوف
- **ماذا / what:** Dip music under narration automatically, judged on representative passages rather than fixed -6/-12 dB offsets.
- **كيف / how:** ffmpeg sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300 with voice as key, or stem-level cuts (drums/melody) at phrase ends.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2459-davinciresolve-sfx-epidemicsound` · `kosif-atlas/skills/1511-homie/3901-sound`

#### BEAT-245 · عرض ستيريو آمن للمونو · Mono-safe stereo width · 📄 موصوف
- **ماذا / what:** 1-3ms inter-channel delay cancels held tones in mono (-4dB loss); widen by detune/panning, offset only transients.
- **كيف / how:** Check stereo correlation via ffmpeg aphasemeter.
- **أرقام / params:** corr -0.2 bad
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound/references/TRAPS.md`

#### BEAT-246 · سلسلة ماسترينج · Music mastering chain · 📄 موصوف
- **ماذا / what:** 28Hz high-pass, -1.5dB shelf at 10kHz, iterate normalize->limit until within 0.15 LU of target; sample ceiling -1.5 dBFS for Vorbis.
- **كيف / how:** numpy or ffmpeg highpass=f=28,treble=g=-1.5:f=10000,alimiter.
- **أرقام / params:** 0.15 LU, 4 iterations
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4163-game-audio-procedural/references/mixing-and-loops.md`

#### BEAT-247 · انحناء النغمة بتكامل الطور · Phase-integrated pitch bends · 📄 موصوف
- **ماذا / what:** Pitch glides must integrate frequency into phase; sin(2πf(t)t) sweeps twice too fast.
- **كيف / how:** phase += 2π f[n]/SR per sample; vibrato ±0.4% (~7 cents).
- **أرقام / params:** ±0.4%
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3901-sound/references/TRAPS.md`

#### BEAT-248 · توحيد الجهارة للنشر · Publish loudness normalization · 📄 موصوف
- **ماذا / what:** Two-pass loudnorm: measure then apply measured values; socials -14 LUFS, podcast -16 LUFS, true peak -1.5, LRA 11.
- **كيف / how:** ffmpeg -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json (pass 1) then with measured_I/TP/LRA (pass 2).
- **أرقام / params:** -14 LUFS social; -16 LUFS podcast; TP -1.5; LRA 11
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/references/operations.md`

#### BEAT-249 · كثافة المؤثرات · Sound design density · 📄 موصوف
- **ماذا / what:** Designed hits on contact/50% pop/97% settle frames; about 5 effects per 10 s.
- **كيف / how:** Apply as defaults while authoring; verify with kmotion measure/speed/sheet
- **أرقام / params:** −14 LUFS, TP ≤ −1 dBTP
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### BEAT-250 · معادلة زمن النبضة · Beat interval formula · 📄 موصوف
- **ماذا / what:** Beat seconds = 60/BPM; place big visual changes on downbeats, punch zooms/keywords on off-beats.
- **كيف / how:** compute 60/BPM grid
- **أرقام / params:** 120 BPM=0.500 s; 100=0.600; 85=0.705
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md`

#### BEAT-251 · رايزر قبل القطع · Riser/whoosh before cut · 📄 موصوف
- **ماذا / what:** Build anticipation with a riser 0.3-0.5 s before a cut.
- **كيف / how:** audio.sfx kit cues
- **أرقام / params:** 0.3-0.5 s lead
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md`

#### BEAT-252 · ضربة على القطع · Impact/sub-drop on cut · 📄 موصوف
- **ماذا / what:** Impact or sub-drop exactly at the cut frame.
- **كيف / how:** audio.sfx
- **أرقام / params:** 0 ms offset; align hit not file start
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md` · `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### BEAT-253 · مونتاج لقطات على إيقاع الموسيقى · Beat-cut montage to music · 📄 موصوف
- **ماذا / what:** Cuts a set of clips on the beat of a music track with a colour grade and a target ratio; length follows the music unless set.
- **كيف / how:** From the studio: recipe 'montage' (form in the الوصفات tab, POST /api/jobs {recipe:'montage', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py montage …`.
- **أرقام / params:** clips (files, '|' separated); --music; --out out/montage.mp4; --grade (default teal_orange, any of 10 grades or none); --ratio 9:16|16:9|1:1|4:5; --seconds; --keep-audio
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:33`

#### BEAT-254 · موسيقى أصلية على شبكة الإيقاع · Original beat-grid score (WAV) · 📄 موصوف
- **ماذا / what:** Synthesises an original music bed on a tempo grid as WAV, so a film can have royalty-free sound.
- **كيف / how:** From the studio: recipe 'score' (form in the الوصفات tab, POST /api/jobs {recipe:'score', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py score …`.
- **أرقام / params:** out out/score.wav; --seconds 15; --bpm 120
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:92`

#### BEAT-255 · مؤثر صاعد قبل القطع وضربة عنده · Riser/whoosh before cut, impact on cut · 📄 موصوف
- **ماذا / what:** Sound design rule that sells transitions: build anticipation just before the cut and land a hit exactly on it.
- **كيف / how:** Place riser/whoosh 0.3-0.5 s before the cut point; place impact/sub-drop on the cut frame. No SFX library ships in this repo; generate or source licensed SFX.
- **أرقام / params:** lead 0.3-0.5 s
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md`

#### BEAT-256 · سلسلة المكساج والماستر · Mix/master processing chain with numbers · 📄 موصوف
- **ماذا / what:** A concrete processing order for voice and music.
- **كيف / how:** HPF -> corrective EQ -> compression -> de-ess -> space -> glue -> limiter at target TP -> loudness to target; implement with ffmpeg (highpass, equalizer, acompressor, deesser, aecho, alimiter, loudnorm) when no DAW.
- **أرقام / params:** HPF 20-30 Hz (voice 80-100); cut mud 200-400, box 400-800, harsh 2.5-5k; air shelf 10-12k; voice comp 3:1 attack 10 ms release 80 ms 3-6 dB GR; bus 2:1 1-2 dB; de-esser 5-8 kHz; reverb pre-delay 20-40 ms; delay ms = 60000/BPM; export WAV 24-bit/48 kHz, MP3 320, AAC 256
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/SKILL.md`

#### BEAT-257 · لوحة المقامات العربية · Arabic maqam palette · 📄 موصوف
- **ماذا / what:** Mood-to-maqam map with prompt hints for scoring Arabic content.
- **كيف / how:** Choose maqam by emotion, add the hint to the music prompt.
- **أرقام / params:** Rast (noble, anthems), Bayati (warm, folk/Khaleeji), Hijaz (longing, mystical, cinematic; ney), Saba (grief), Nahawand (romantic minor), Kurd (tender modern pop), Ajam (bright, weddings), Sikah (spiritual, Sufi)
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/references/arabic-music.md`

#### BEAT-258 · الإيقاعات العربية · Arabic rhythm (iqa') patterns · 📄 موصوف
- **ماذا / what:** Named Arabic rhythms with meters and stroke patterns for beat-synced edits and music prompts.
- **كيف / how:** Pick by feel; for cut timing use the BPM of the chosen rhythm.
- **أرقام / params:** Maqsum 4/4 D T - T D - T -; Baladi 4/4 D D - T D - T -; Saidi 4/4 D T - D D - T -; Malfuf 2/4; Khaleeji 2/4 shuffle + claps; Ayoub 2/4 (zar trance); Samai Thaqil 10/8; Wahda 4/4 slow; Chobi/Dabke 4/4
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/references/arabic-music.md`

#### BEAT-259 · الآلات العربية · Arabic instrument palette · 📄 موصوف
- **ماذا / what:** Instrument names for music prompts and sound design.
- **كيف / how:** Name 2-4 instruments in the style prompt.
- **أرقام / params:** oud, qanun, ney, violin section, darbuka/tabla, riq, daf, bendir, mizmar, rababa, buzuq, kawala, Khaleeji hand-claps (tasfiq), synth pads
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audio/references/arabic-music.md`

#### BEAT-260 · موجز الأغنية ومدد الإيقاع · Song brief spec + beat durations · 📄 موصوف
- **ماذا / what:** Original-lyrics song brief and the beat/bar timings for cutting video to music.
- **كيف / how:** Genre/maqam, BPM, structure, rhyme (قافية), hook line, instrumentation, vocal character, reference feel (no living-artist imitation); kosif_kcl_probe name=beat bpm=... returns beat, bar and 8-bar durations.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-voice/SKILL.md` · `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/tools_scripts.py:255`

#### BEAT-261 · أهداف الجهارة · Loudness targets per platform · 📄 موصوف
- **ماذا / what:** Platform/video -14 LUFS, podcast -16 LUFS stereo (-19 mono), true peak -1 dBTP, adjacent scenes differ <=6 dB.
- **كيف / how:** Measure with loudnorm/ebur128, never estimate.
- **أرقام / params:** -14/-16/-19 LUFS, -1 dBTP, 6 dB
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `100-superskills/skills/podcast-production/SKILL.md` · `100-superskills/skills/audio-mastering-analysis/SKILL.md`

#### BEAT-262 · ducking حقيقي · Sidechain ducking · 📄 موصوف
- **ماذا / what:** Music compressed by voice signal.
- **كيف / how:** [1:a][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=400[m];amix normalize=0
- **أرقام / params:** thr 0.05, ratio 8, attack 20 ms, release 400 ms
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### BEAT-263 · سلسلة ماسترينغ · Audio mastering chain · 📄 موصوف
- **ماذا / what:** Measure integrated LUFS, true peak, LRA, spectrum, clipping; clean (noise, hum) -> corrective EQ -> compression -> limiter; re-measure; before/after report.
- **كيف / how:** ffmpeg loudnorm two-pass or Python; outputs analysis.json, master.wav/mp3, report.md
- **أرقام / params:** -14/-16 LUFS, -1 dBTP
- **الدليل / proof:** `100-superskills/skills/audio-mastering-analysis/SKILL.md`

#### BEAT-264 · ربط الحركة بالصوت · Audio-reactive mapping rules · 📄 موصوف
- **ماذا / what:** Bass drives big moves (scale/glow/offset), treble details (sparkle/edges), RMS background brightness; 2-3 properties max; floor above zero; smoothing prev*s+raw*(1-s).
- **كيف / how:** Load JSON synchronously; recompute smoothing from frame 0.
- **أرقام / params:** s=0.25 (0.1-0.2 sharp, 0.3-0.5 fluid); bands 4/8/16/32
- **الدليل / proof:** `100-superskills/skills/audio-reactive-captions-studio/references/captions-rules.md`

#### BEAT-265 · القطع على الإيقاع · Beat-cut rules · 📄 موصوف
- **ماذا / what:** Cut every 1-2 beats; period 60/BPM; visual hit scale 1.06 for 0.35 s on beat; talking reels max one cut per 2.5 s.
- **كيف / how:** Feed beats to edl.json or scene times.
- **أرقام / params:** 1.06 / 0.35 s
- **الدليل / proof:** `100-superskills/skills/audio-reactive-captions-studio/references/captions-rules.md`

#### BEAT-266 · قطع على الإيقاع · Beat/sentence cut points from BPM · 📄 موصوف
- **ماذا / what:** Cut every beat or sentence; beat interval = 60/BPM.
- **كيف / how:** edit-plan.md
- **الدليل / proof:** `100-superskills/skills/video-editing-captions/SKILL.md:21`

#### BEAT-267 · قواعد صوت الإعلان · Ad audio rules · 📄 موصوف
- **ماذا / what:** Cuts on music grid, voice-over leads features, logo on final hit, deliver loudness target.
- **أرقام / params:** -14 LUFS
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:83`

#### BEAT-268 · خفض الموسيقى تحت الصوت · Music ducking under voice · 📄 موصوف
- **ماذا / what:** Sidechain-duck music beneath narration.
- **كيف / how:** ffmpeg sidechaincompress or keyframed volume.
- **أرقام / params:** 8–12 dB duck; attack 150 ms; release 400 ms
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:82` · `kosif-tool/playbooks/music.md:74`

#### BEAT-269 · تطبيع الجهارة -14 LUFS · Loudness normalisation -14 LUFS · 📄 موصوف
- **ماذا / what:** Normalize final mix for social delivery.
- **كيف / how:** ffmpeg -af loudnorm=I=-14:TP=-1:LRA=11 (two-pass for precision).
- **أرقام / params:** -14 LUFS integrated ±1.5; TP ≤ -1 dBTP; LRA 11
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:84`

#### BEAT-270 · أصوات مفاتيح خافتة · Soft key-click SFX · 📄 موصوف
- **ماذا / what:** Optional quiet key clicks; execution on beat/pause.
- **أرقام / params:** -24 dB
- **الدليل / proof:** `kosif-tool/playbooks/code.md:79`

#### BEAT-271 · مستوى صوت الرسم · Drawing SFX level · 📄 موصوف
- **ماذا / what:** Soft marker/chalk sounds only while drawing; objects finish on spoken names.
- **أرقام / params:** -22 dB
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:81`

#### BEAT-272 · خريطة بنية المقطوعة · Song structure map · 📄 موصوف
- **ماذا / what:** Map intro/verse/build/drop/outro and assign visual modes; save boldest frame for drop.
- **الدليل / proof:** `kosif-tool/playbooks/music.md:15-17`

#### BEAT-273 · تأكيد الضربات القوية والضعيفة · Strong/weak beat accents · 📄 موصوف
- **ماذا / what:** Strong beats (1,3 in 4/4) get cuts/big moves; weak beats small accents.
- **أرقام / params:** weak accents scale 2–4%
- **الدليل / proof:** `kosif-tool/playbooks/music.md:16`

#### BEAT-274 · حساب طول الضربة · Beat period math · 📄 موصوف
- **ماذا / what:** Beat = 60/BPM s; round cuts to nearest frame and log rounding.
- **أرقام / params:** 120 BPM → 500 ms = 15 frames at 30 fps
- **الدليل / proof:** `kosif-tool/playbooks/music.md:23`

#### BEAT-275 · قيم متفاعلة منعّمة · Smoothed audio-reactive values · 📄 موصوف
- **ماذا / what:** RMS/bands smoothed and clamped; precompute envelope offline for determinism.
- **كيف / how:** Remotion useAudioData + visualizeAudio (@remotion/media-utils); or ffmpeg astats / Python RMS every 1/30 s to JSON.
- **أرقام / params:** window 100–200 ms
- **الدليل / proof:** `kosif-tool/playbooks/music.md:27` · `kosif-tool/playbooks/music.md:64`

#### BEAT-276 · وصفة التصاعد والذروة · Build and drop recipe · 📄 موصوف
- **ماذا / what:** Accelerating cuts, a beat of black before drop, hero frame on drop.
- **أرقام / params:** bars 1–4 cuts every 2 beats + 1%/bar push; bars 5–7 every beat; bar 8 beat 4 black; drop +2 bars hero spring 14/160
- **الدليل / proof:** `kosif-tool/playbooks/music.md:36-41`

#### BEAT-277 · أعمدة المعادل · Equalizer bars · 📄 موصوف
- **ماذا / what:** FFT band bars, smoothed, mirrored.
- **أرقام / params:** 24–48 bars; 120 ms smoothing; height ≤ 60% frame
- **الدليل / proof:** `kosif-tool/playbooks/music.md:45`

#### BEAT-278 · ترخيص الموسيقى · Music licensing rule · 📄 موصوف
- **ماذا / what:** Only user-provided or licensed music.
- **الدليل / proof:** `kosif-tool/playbooks/music.md:3` · `kosif-tool/playbooks/music.md:85`

#### BEAT-279 · مستويات مؤثرات النقر والسحب · Tap/swipe SFX levels · 📄 موصوف
- **ماذا / what:** Optional licensed SFX at fixed levels, ducked under voice.
- **أرقام / params:** click 30–50 ms at −18 dBFS; whoosh ≤ 250 ms; ducked 10 dB
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:204`

#### BEAT-280 · تصميم صوت شحيح للواجهة · Sparse UI sound design · 📄 موصوف
- **ماذا / what:** One click per press, one swish per screen change, nothing on hovers/list items; press within ±100 ms of verb.
- **أرقام / params:** click 10–30 ms transient, 12–18 dB below voice
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:220-222`

#### BEAT-281 · مكتبة مؤثرات Kenney · Kenney CC0 SFX library · 📄 موصوف
- **ماذا / what:** Bundled UI/interface/impact/casino/keyboard OGG SFX with analysis (brightness, HF risk, envelope).
- **كيف / how:** Read sfx-analysis.md, pick low-HF-risk for repeated moments, copy into composition/assets.
- **أرقام / params:** ~238 files; impactSoft_medium 0.12-0.18 s warm
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/assets/sfx/sfx-analysis.md` · `kosif-one/vendor/brag/skills/brag/references/audio.md`

#### BEAT-282 · إشارات الموسيقى الجاهزة · Music cue presets · 📄 موصوف
- **ماذا / what:** Per-track JSON/MD with tempo, beat grid and strongCue timestamps for planning first 20-25 s.
- **كيف / how:** Read cues/<stem>.music-cues.json; place major moments on strongCues.
- **أرقام / params:** vol-1: 163.96 s, 120.19 BPM, first beat ~3.02 s
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/assets/music/cues/happy-beats-business-moves-vol-1-by-ende-dot-app.music-cues.json` · `kosif-one/vendor/brag/skills/brag/assets/music/README.md`

#### BEAT-283 · أوديوجرام للبودكاست · Podcast audiogram · 💡 فكرة
- **ماذا / what:** Turn a podcast clip into a vertical video: denoised voice, -16 LUFS, word captions, subtle amplitude-driven glow on speaker card.
- **كيف / how:** whisper + band JSON + Remotion/GSAP; loudnorm I=-16.
- **أرقام / params:** -16 LUFS speech
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/audio-reactive.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/captions.md` · `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b`

#### BEAT-284 · مؤثرات صوتية مولدة · Synthesized Web Audio SFX on frame clock · 💡 فكرة
- **ماذا / what:** Every sound (boing, xylophone, click, rustle) synthesized by oscillators and scheduled from the animation clock.
- **كيف / how:** Web Audio OscillatorNode + gain envelope; schedule at frame time.
- **أرقام / params:** attack 5 ms, decay 120 ms
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`

#### BEAT-285 · مؤثر واحد لكل عنصر · One soft SFX per element · 💡 فكرة
- **ماذا / what:** Each appearing element gets one soft tick; otherwise silence, no music bed.
- **كيف / how:** SFX track keyed to entrances.
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### BEAT-286 · شبكة 110 نبضة · 110 BPM beat grid derivation · 💡 فكرة
- **ماذا / what:** Every hit, mouth swap, set change derived from a beat grid; nothing off-grid.
- **كيف / how:** beat=545 ms.
- **أرقام / params:** ~110 BPM; wipes every 8 beats; prop swap every 2 beats
- **الدليل / proof:** `style:pm-davidshulmanfl-371638`

#### BEAT-287 · كشف الإيقاع · BPM-detect beat grid · 💡 فكرة
- **ماذا / what:** Detect track BPM and place all cuts on downbeats within 1 frame.
- **كيف / how:** librosa/aubio beat track.
- **أرقام / params:** 128-140 BPM; ≤1 frame drift @30 fps
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### BEAT-288 · ضربات على النبض · Beat-locked punch-ins · 💡 فكرة
- **ماذا / what:** Punch-ins within 2 frames of beat marker; final lockup ≥48 frames.
- **أرقام / params:** 100-110 BPM; ±2 frames
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### BEAT-289 · موسيقى مع خفض · Arc-scored music with typing duck · 💡 فكرة
- **ماذا / what:** Score density follows session arc; ducks under typing sounds.
- **كيف / how:** Sidechain/volume automation.
- **أرقام / params:** -6 dB duck
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### BEAT-290 · قطع على الصوت · Sound-first cuts with held silence · 💡 فكرة
- **ماذا / what:** Cuts land on sound events; silence held ≥2 s once; no narration; one 1 s fade to black.
- **أرقام / params:** cuts ≥1 s
- **الدليل / proof:** `style:pm-kamstudiolabs-0b0824`

#### BEAT-291 · نغمة متصاعدة · Rising pitch per pass · 💡 فكرة
- **ماذا / what:** Each gap pass raises pitch.
- **كيف / how:** Synth pitch step.
- **الدليل / proof:** `style:pm-kantamk-61f410`

#### BEAT-292 · تفاعل على الإيقاع · Frame-accurate beat reactions · 💡 فكرة
- **ماذا / what:** Every reaction within 1-2 frames of beat from shared timing table.
- **أرقام / params:** 128 BPM = 469 ms/beat
- **الدليل / proof:** `style:pm-reflex-cloud-72ffe5`

#### BEAT-293 · نبض على الكيك · Kick pulse exponential decay · 💡 فكرة
- **ماذا / what:** scale 1.0->1.06 on kick, exp decay 300 ms; push 2%/4 bars
- **الدليل / proof:** `style:pm-samaote-5e2fc2`

#### BEAT-294 · أصوات مولدة · Event-synthesized UI tones · 💡 فكرة
- **ماذا / what:** Tones per UI event, pitch from y.
- **كيف / how:** OfflineAudioContext.
- **أرقام / params:** 48 kHz; normalise -14 LUFS
- **الدليل / proof:** `style:pm-xelandre-363f00`

## إضافات من Cinematic Director PRO v5

_مستخلصة من حزمة المالك KOSIF Claude Cinematic Director PRO v5 (انظر [cinematic-director-pro.md](../cinematic-director-pro.md)). مسارات الدليل `owner-upload:` تشير إلى ملفات داخل أرشيف المالك، لا إلى هذا المستودع._

#### BEAT-P01 · نقرات صوتية مولّدة على لحظات الحركة · Code-synthesised chirp ticks on motion events · ✅ مُثبت هنا / proven here
- **ماذا / what:** مؤثرات صغيرة تُكتب بمعادلة على موعد كل حدث بصري، فوق طنين منخفض خفيف، بلا ملفات صوت خارجية. / Short chirps written as a formula at each visual event over a faint low bed — no external audio files.
- **كيف / how:** sr 24 kHz mono 16-bit. Bed: 0.009·sin(2π·160·t)·sin²(πt/D). For each event time a: z = t−a; add 0.075·e^(−50z)·sin(2π(320+190z)z) for 0 ≤ z < 0.14 s (a rising chirp that dies in ~100 ms). Event list = the same times that drive the picture (0.3, 1.0, 1.85, 2.7, 4.3, 5.35 s), so sound and motion share one clock. Clip to ±1, write WAV, mux AAC with -shortest. **أرقام / params:** peak 0.075 · decay 50/s · 320 Hz + 190 Hz/s sweep · 140 ms · bed 160 Hz at 0.009
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/render_continuous_line.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Continuous_Line_Logo_Story.wav`
