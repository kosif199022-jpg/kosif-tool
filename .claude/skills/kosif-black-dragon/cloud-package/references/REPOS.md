# أهم مستودعات المونتاج (اتراجعت 2026-11-08)

| # | المستودع | الرخصة | بيعمل إيه للتنين | سحابة / جهاز |
|---|---|---|---|---|
| 1 | browser-use/video-use | MIT | مونتاج كامل بإيد Claude Code: يقص «ااه» والسكتات، يلوّن، يحرق ترجمة، ويراجع بعد الرندر. خد منه طريقة الشغل | الاتنين (فكرته مطبقة في `dragon_montage`) |
| 2 | heygen-com/hyperframes | Apache-2.0 | HTML يطلع فيديو، معمول للإيجنتس؛ العربي بيترسم صح في المتصفح | الاتنين (`npm i hyperframes`)؛ بديله الجاهز `web_film` + `render.cjs` |
| 3 | m-bain/whisperX | BSD-2 | توقيت كل كلمة بدقة عالية (كاريوكي) | جهاز بـ GPU (`dragon.py setup --gpu`)؛ في السحابة `faster-whisper` (`--full`) |
| 4 | WyattBlue/auto-editor | Unlicense | يقص السكتات من سطر واحد ويصدّر لبريمير ودافنشي | الاتنين (بيتثبت في `setup`) |
| 5 | facebookresearch/demucs | MIT | يفصل الصوت عن المزيكا | جهاز (`--gpu`)؛ بطيء في السحابة |
| 6 | Rikorose/DeepFilterNet | MIT/Apache | يشيل الدوشة | جهاز |
| 7 | librosa/librosa | ISC | البيت والإيقاع | الاتنين (`dragon beats`) |
| 8 | remotion-dev/remotion | مجاني لـ ≤3 أشخاص | فيديو بـ React | جهاز؛ انتبه للرخصة |
| 9 | Zulko/moviepy | MIT | مونتاج بالبايثون | الاتنين |
| 10 | ManimCommunity/manim | MIT | شروحات ورسوم بيانية | جهاز |
| 11 | google-ai-edge/mediapipe | Apache-2.0 | تتبع الوش للقص 9:16 | الاتنين (موديل YuNet مدمج في `dragon_montage/models`) |
| 12 | facebookresearch/sam2 | Apache-2.0 | عزل أي حاجة (نص ورا الشخص) | جهاز بـ GPU |
| 13 | hzwer/ECCV2022-RIFE | MIT | سلو موشن بفريمات متولدة | جهاز بـ GPU |
| 14 | danielgatis/rembg | MIT | شيل الخلفية | الاتنين (بطيء في السحابة) |
| 15 | harry0703/MoneyPrinterTurbo | MIT | فيديوهات قصيرة أوتوماتيك (أفكار) | مرجع |
| 16 | veedstudio/open-edit | Apache-2.0 | مونتاج بالإيجنتس + whisperX | مرجع (أجزاء محتاجة حساب VEED) |
| 17 | mifi/lossless-cut | GPL-2.0 | قص من غير رندر، يدوي | جهاز، كأداة منفصلة |

**تحذير الرخص:** أي حاجة GPL أو AGPL (lossless-cut، RobustVideoMatting، video2x، whisper-timestamped) تتشغل كبرنامج منفصل، ماتتدمجش جوه الكود.

**الموجود فعلًا:** FFmpeg وfaster-whisper وPySceneDetect وOpenCV، وBlender على الجهاز. محركات الموشن الـ25 (three.js، GSAP، Remotion، Lottie، Manim، motion-canvas…) ومستودعات KOSIF (kosif-one، fastify-motion-bro، kosif-studio) بتتلاقي بـ `dragon find`.
