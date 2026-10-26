# وصفات ffmpeg للمونتير (خلاصة mas-video-lab/ffmpeg + losslesscut + remotion/ffmpeg + خبرة الاداة)

## القاعدتان اللتان لا تُخالَفان
1. **للويب:** `-pix_fmt yuv420p -movflags +faststart` دائماً (ألوان صحيحة على iOS/QuickTime وتشغيل فوري).
2. **القصّ بلا ترميز (`-c copy`) على إطار مفتاحي فقط**، وإلا تجمّد الصورة 2-5 ثوانٍ في البداية. اعرف الإطارات المفتاحية بـ `probe.py --keyframes`، أو استخدم Smart-cut (إعادة ترميز الجزء بين نقطة القطع وأقرب I-frame فقط).

## الفحص
```bash
ffprobe -v error -print_format json -show_format -show_streams in.mp4
ffprobe -v error -select_streams v:0 -show_packets -show_entries packet=pts_time,flags -print_format json in.mp4   # flags فيها K = مفتاحي
```

## القصّ
```bash
# دقيق إطارياً (إعادة ترميز)
ffmpeg -ss 00:00:12.400 -i in.mp4 -to 00:00:08.000 -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -pix_fmt yuv420p -movflags +faststart out.mp4
# بلا فقد (على إطار مفتاحي؛ -ss قبل -i للسرعة)
ffmpeg -ss 12.0 -i in.mp4 -to 8.0 -c copy -avoid_negative_ts make_zero -movflags +faststart out.mp4
```
`-avoid_negative_ts make_zero` يمنع «الصوت يعمل والصورة متجمدة» بعد التصدير.

## الدمج
```bash
# نفس الكودك والدقة: concat demuxer بلا ترميز
printf "file 'a.mp4'\nfile 'b.mp4'\n" > list.txt && ffmpeg -f concat -safe 0 -i list.txt -c copy -movflags +faststart merged.mp4
# مصادر مختلفة: concat filter مع توحيد
ffmpeg -i a.mp4 -i b.mov -filter_complex "[0:v]fps=30,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[v0];[1:v]fps=30,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -pix_fmt yuv420p out.mp4
```

## الانتقالات (xfade) والصوت المتقاطع
```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=5.5[v];[0:a][1:a]acrossfade=d=0.5[a]" -map "[v]" -map "[a]" out.mp4
```
`offset` = مدة المقطع الأول − مدة الانتقال. الأنواع: fade, dissolve, wipeleft/right/up/down, slideleft/right/up/down, circleopen/close, pixelize, radial, fadeblack, fadewhite, zoomin, hblur. **المعنى:** قطع صلب = تغيير/استيقاظ، تلاشٍ = استمرار، ذوبان بطيء = انجراف. لا أكثر من نوعين في الفيلم.

## قطع J وL
J-cut: صوت المقطع التالي يبدأ قبل صورته (`audio_lead` في EDL = atrim يبدأ أبكر). L-cut: صوت المقطع السابق يستمر تحت الصورة الجديدة (أطل atrim للمقطع السابق وامزج بـ amix). كلاهما يربط المشاهد ويخفي القطع.

## السرعة
```bash
# 2× (الفيديو setpts، والصوت atempo بين 0.5 و2؛ سلسل atempo لأكثر)
-filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"
# حركة بطيئة ناعمة 0.5× مع استيفاء إطارات
-filter_complex "[0:v]minterpolate=fps=60:mi_mode=mci,setpts=2.0*PTS[v]"
```

## الصوت
```bash
# تطبيع بمرورين (الصحيح): قياس
ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -
# ثم تطبيق بالقيم المقاسة
-af loudnorm=I=-14:TP=-1:LRA=11:measured_I=-23.1:measured_TP=-5.2:measured_LRA=9.8:measured_thresh=-33.4:offset=0.3:linear=true
# موسيقى تحت الكلام (ducking بسيط)
-filter_complex "[1:a]volume=-18dB[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]"
# ducking حقيقي بـ sidechaincompress
-filter_complex "[1:a][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=400[m];[0:a][m]amix=inputs=2:normalize=0[a]"
```
الأهداف: −14 LUFS للمنصات، −16 للبودكاست، قمة −1 dBTP، فرق المشاهد المتجاورة ≤ 6 dB.

## التدرّج اللوني
```bash
-vf "lut3d=file=look.cube"                       # LUT
-vf "eq=contrast=1.08:saturation=1.1:gamma=1.02"  # تصحيح خفيف
-vf "curves=preset=increase_contrast"             # منحنيات
```
القاعدة: تصحيح تقني (تعريض، توازن أبيض، تباين، تشبّع) أولاً، ثم لوك إبداعي منفصل. الصور من الهاتف عالية التباين أصلاً؛ خفّف.

## الترجمة
```bash
ffmpeg -i in.mp4 -vf "subtitles=captions.srt:force_style='FontName=Cairo,FontSize=22,Outline=2,MarginV=60'" -c:a copy out.mp4   # حرق
ffmpeg -i in.mp4 -i captions.srt -c copy -c:s mov_text -metadata:s:s:0 language=ara out.mp4                                      # تضمين قابل للإيقاف
```
42 حرفاً للسطر، سطران، 1-7 ثوانٍ، داخل المنطقة الآمنة؛ لا تغطية للوجوه.

## النسب والقصّ الذكي
```bash
# 16:9 → 9:16 بقصّ من المنتصف (أو بتعبئة ضبابية)
-vf "crop=ih*9/16:ih,scale=1080:1920"
-filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2"
```

## التصدير
| الهدف | الإعداد |
|---|---|
| ويب/سوشيال | `libx264 -crf 18..23 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k` |
| حجم أصغر | `libx265 -crf 24 -tag:v hvc1` (توافق أقل) |
| GPU سريع | `-hwaccel cuda -c:v h264_nvenc -preset p6 -cq 20` (تحقق بـ `ffmpeg -encoders | grep nvenc`) |
| HLS | `-g 60 -keyint_min 60 -sc_threshold 0 -f hls -hls_time 4 -hls_playlist_type vod` |
| إطارات → فيديو | `-framerate 30 -i f_%04d.png -c:v libx264 -pix_fmt yuv420p` |
| GIF معاينة | `fps=12,scale=360:-1,split[a][b];[a]palettegen[p];[b][p]paletteuse` |

## تشخيص
| العرض | السبب | الحل |
|---|---|---|
| انزياح صوت/صورة | معدل إطارات متغير (هاتف/تسجيل شاشة) | `-vf fps=30` أو `-vsync cfr -r 30` + `aresample=async=1` |
| Non-monotonous DTS | طوابع زمنية فاسدة | `-fflags +genpts` قبل `-i`، أو remux بـ `-c copy -avoid_negative_ts make_zero` |
| ألوان باهتة على iOS | 4:2:2/4:4:4 أو وسوم لون ناقصة | `-pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709` |
| Invalid NAL unit size | حاوية تالفة | `ffmpeg -i in.mp4 -c copy -movflags +faststart fixed.mp4` ثم القصّ |
| تجمّد أول ثوانٍ | قطع -c copy خارج إطار مفتاحي | انحز إلى I-frame أو أعد الترميز |
