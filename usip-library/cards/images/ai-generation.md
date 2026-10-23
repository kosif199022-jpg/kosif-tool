# `ai-generation` — الصور والتحرير والتوليد (94 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/ai-generation.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/images.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`GEN-01` تشريح البرومبت السباعي والمعادلة الذهبية](#gen-01--تشريح-البرومبت-السباعي-والمعادلة-الذهبية--seven-layer-prompt-anatomy--golden-formula)
- [`GEN-02` القواعد الحديدية والكلمات القوية](#gen-02--القواعد-الحديدية-والكلمات-القوية--iron-rules-physical-cues-beat-hype-words)
- [`GEN-03` قائمة النفي الأساسية والصياغة الإيجابية](#gen-03--قائمة-النفي-الأساسية-والصياغة-الإيجابية--negative-baseline-vs-positive-framing)
- [`GEN-04` معادلة برومبت الصورة ذات الخانات الست](#gen-04--معادلة-برومبت-الصورة-ذات-الخانات-الست--six-slot-still-prompt-formula)
- [`GEN-05` برومبت سردي لنانو بنانا / Gemini](#gen-05--برومبت-سردي-لنانو-بنانا--gemini--narrative-prose-brief-for-gemini--nano-banana)
- [`GEN-06` دليل صياغة كل مولّد وترجمة صيغة ميدجورني](#gen-06--دليل-صياغة-كل-مولّد-وترجمة-صيغة-ميدجورني--per-generator-syntax--midjourneynatural-language-translation)
- [`GEN-07` معادلة برومبت لقطة الفيديو](#gen-07--معادلة-برومبت-لقطة-الفيديو--video-shot-prompt-formula)
- [`GEN-08` منع الموسيقى والترجمة المزيفة في الفيديو المولد](#gen-08--منع-الموسيقى-والترجمة-المزيفة-في-الفيديو-المولد--suppress-generated-music-bed--fake-subtitles)
- [`GEN-09` حدود مولدات الفيديو الحالية](#gen-09--حدود-مولدات-الفيديو-الحالية--known-limits-of-current-video-generators)
- [`GEN-10` مصنع البرومبت: مواصفة واحدة ← تسع منصات](#gen-10--مصنع-البرومبت-مواصفة-واحدة--تسع-منصات--prompt-forge-one-spec--9-generator-prompts)
- [`GEN-11` خصائص منصات الفيديو (DNA)](#gen-11--خصائص-منصات-الفيديو-dna--video-model-platform-dna-veo--runway--kling--sora)
- [`GEN-12` مواصفة الصورة الموحدة وستة مُنشئات](#gen-12--مواصفة-الصورة-الموحدة-وستة-مُنشئات--image-spec-schema--6-platform-builders)
- [`GEN-13` قوالب لقطات الفيديو لسبع منصات مع قص المدة](#gen-13--قوالب-لقطات-الفيديو-لسبع-منصات-مع-قص-المدة--shot-list--7-video-platform-prompts-with-duration-clamping)
- [`GEN-14` برومبتات اللقطات السباعية (kmotion aiprompts)](#gen-14--برومبتات-اللقطات-السباعية-kmotion-aiprompts--kmotion-aiprompts-7-layer-per-shot-prompts)
- [`GEN-15` من فيديو مرجعي إلى برومبت Omni Flash](#gen-15--من-فيديو-مرجعي-إلى-برومبت-omni-flash--reference-breakdown--omni-flash-generation-prompt)
- [`GEN-16` مواصفة مشهد مكتوبة وبصمة SHA-256](#gen-16--مواصفة-مشهد-مكتوبة-وبصمة-sha-256--typed-scenespec-compile--sha-256-digest)
- [`GEN-17` أقفال الشخصية والأسلوب والمكان](#gen-17--أقفال-الشخصية-والأسلوب-والمكان--character--style--location-locks)
- [`GEN-18` واجهة الأنماط المرحلية (Fastify)](#gen-18--واجهة-الأنماط-المرحلية-fastify--stage-gated-profile-cli)
- [`GEN-19` سلاسل برومبتات الأنماط الخمسة](#gen-19--سلاسل-برومبتات-الأنماط-الخمسة--five-profile-prompt-series-stickman-fitness-car-history-food)
- [`GEN-20` حزمة الكينتك فلو واللقطة النظيفة](#gen-20--حزمة-الكينتك-فلو-واللقطة-النظيفة--kinetic-flow-prompt-pack--clean-plate--overlay-sheet)
- [`GEN-21` برومبتات البوستر والحركة التحريرية](#gen-21--برومبتات-البوستر-والحركة-التحريرية--viral-editorial-poster--silent-motion-prompts)
- [`GEN-22` بذور برومبت في كل سقالة](#gen-22--بذور-برومبت-في-كل-سقالة--per-shot-ai-prompt-seeds-written-by-the-scaffold)
- [`GEN-23` تخطيط موجه لنماذج الفيديو](#gen-23--تخطيط-موجه-لنماذج-الفيديو--proplan-model-prompt-stage-with-continuity-locks)
- [`GEN-24` معادلة برومبت النماذج اللغوية ومدققها](#gen-24--معادلة-برومبت-النماذج-اللغوية-ومدققها--llm-prompt-formula--linter-prompts-for-agents--generators)
- [`GEN-25` مثال مصر 2120: حزمة برومبتات كاملة](#gen-25--مثال-مصر-2120-حزمة-برومبتات-كاملة--worked-example-egypt-2120-multi-platform-pack)
- [`GEN-26` كتالوج الأساليب المسماة (أكثر من 30 مظهرًا)](#gen-26--كتالوج-الأساليب-المسماة-أكثر-من-30-مظهرًا--named-look-catalogue-30-looks)
- [`GEN-27` مقدمات الأسلوب المتطابقة بايتًا](#gen-27--مقدمات-الأسلوب-المتطابقة-بايتًا--byte-identical-style-preambles)
- [`GEN-28` استخراج قفل الأسلوب](#gen-28--استخراج-قفل-الأسلوب--style-lock-extraction)
- [`GEN-29` مكتبات المعدِّلات حسب المجال وقوالب التصوير](#gen-29--مكتبات-المعدِّلات-حسب-المجال-وقوالب-التصوير--domain-modifiers-photo-templates--camera-bodies)
- [`GEN-30` مفردات التلوين وحزم أسلوب الفيديو](#gen-30--مفردات-التلوين-وحزم-أسلوب-الفيديو--grade-vocabulary-film-stocks--video-style-packs)
- [`GEN-31` وصفات أساليب كلينج بنطاقات cfg_scale](#gen-31--وصفات-أساليب-كلينج-بنطاقات-cfg_scale--kling-style-recipes-with-cfg_scale-bands)
- [`GEN-32` البرومبت العكسي ونقد الصورة](#gen-32--البرومبت-العكسي-ونقد-الصورة--reverse-prompt--image-critique)
- [`GEN-33` أنت المولّد: صورة من وصف بالكود (SVG / Canvas / PIL / Three.js)](#gen-33--أنت-المولّد-صورة-من-وصف-بالكود-svg--canvas--pil--threejs--you-are-the-generator-picture-from-a-description-as-code)
- [`GEN-34` استخراج الكود من رد الذكاء الاصطناعي](#gen-34--استخراج-الكود-من-رد-الذكاء-الاصطناعي--ai-reply-code-extraction)
- [`GEN-35` جسر الذكاء في الاستوديو (Claude CLI / API / يدوي)](#gen-35--جسر-الذكاء-في-الاستوديو-claude-cli--api--يدوي--studio-ai-bridge-claude-cli--api--manual)
- [`GEN-36` صورة فوتوغرافية محلية sd-turbo أو Pollinations](#gen-36--صورة-فوتوغرافية-محلية-sd-turbo-أو-pollinations--photo-from-prompt-local-sd-turbo-or-pollinations)
- [`GEN-37` توليد وتعديل الصور بـ Gemini (نانو بنانا)](#gen-37--توليد-وتعديل-الصور-بـ-gemini-نانو-بنانا--gemini--nano-banana-image-generate--edit)
- [`GEN-38` تحرير بمراجع متعددة قبل التحريك (نانو بنانا)](#gen-38--تحرير-بمراجع-متعددة-قبل-التحريك-نانو-بنانا--nano-banana-multi-reference-edit-before-animation)
- [`GEN-39` عائلة FLUX عبر Together وحلقة Kontext](#gen-39--عائلة-flux-عبر-together-وحلقة-kontext--flux-via-together--kontext-edit-round-trip--lora)
- [`GEN-40` GPT Image وIdeogram للصور ذات النص](#gen-40--gpt-image-وideogram-للصور-ذات-النص--gpt-image--ideogram-v4-text-capable-stills-edit-describe)
- [`GEN-41` صور Higgsfield (Soul v2 / Marketing Studio / gpt_image_2)](#gen-41--صور-higgsfield-soul-v2--marketing-studio--gpt_image_2--higgsfield-image-generation)
- [`GEN-42` وصفة صور الهوية: كائن معدني وكريستال (ذهبي/جليدي)](#gen-42--وصفة-صور-الهوية-كائن-معدني-وكريستال-ذهبيجليدي--brand-still-recipe-metal--crystal-object-on-brand-ground)
- [`GEN-43` لقطات بمساحة فارغة للكتابة](#gen-43--لقطات-بمساحة-فارغة-للكتابة--ai-plates-that-reserve-typography-space)
- [`GEN-44` أيقونات شفافة بثيم وشرائط سبرايت ثابتة](#gen-44--أيقونات-شفافة-بثيم-وشرائط-سبرايت-ثابتة--themed-transparent-icons--consistent-sprite-strips)
- [`GEN-45` تعديل قبل إعادة التوليد: توسيع وترميم وقص وتكبير](#gen-45--تعديل-قبل-إعادة-التوليد-توسيع-وترميم-وقص-وتكبير--edit-before-regenerate-outpaint-inpaint-cut-out-upscale)
- [`GEN-46` شجرة اختيار نموذج الصور والترخيص أولًا](#gen-46--شجرة-اختيار-نموذج-الصور-والترخيص-أولًا--image-model-routing-tree-licence-first)
- [`GEN-47` وصفات ComfyUI: المُعيِّن والجدولة وقياس منحنيات الضوضاء](#gen-47--وصفات-comfyui-المُعيِّن-والجدولة-وقياس-منحنيات-الضوضاء--comfyui-samplerscheduler-recipes--measured-sigma-curves)
- [`GEN-48` LoRA وControlNet والترميم في ComfyUI](#gen-48--lora-وcontrolnet-والترميم-في-comfyui--comfyui-lora-bands-controlnet--inpainting)
- [`GEN-49` شجرة اختيار نموذج الفيديو ومسودة رخيصة ثم نهائي](#gen-49--شجرة-اختيار-نموذج-الفيديو-ومسودة-رخيصة-ثم-نهائي--video-model-routing-tree--cheap-draft--premium-final)
- [`GEN-50` صورة مفتاحية أولًا ثم تحريكها](#gen-50--صورة-مفتاحية-أولًا-ثم-تحريكها--keyframe-first-image-to-video)
- [`GEN-51` Seedance 2.5 عبر Higgsfield (محروس ومدفوع)](#gen-51--seedance-25-عبر-higgsfield-محروس-ومدفوع--seedance-25-textimage-to-video-via-higgsfield-guarded)
- [`GEN-52` حلقات فيديو Kling للهوية وواجهة Kling](#gen-52--حلقات-فيديو-kling-للهوية-وواجهة-kling--kling-textimage-to-video-api--real-brand-loops)
- [`GEN-53` فرشاة الحركة والقناع الثابت (سينماغراف)](#gen-53--فرشاة-الحركة-والقناع-الثابت-سينماغراف--kling-motion-brush--static-mask-cinemagraph)
- [`GEN-54` تمديد فيديو Kling بالتسلسل ونظام الرصيد](#gen-54--تمديد-فيديو-kling-بالتسلسل-ونظام-الرصيد--kling-extension-chain--credit-model)
- [`GEN-55` واجهة Runway حسب النموذج والتزامن](#gen-55--واجهة-runway-حسب-النموذج-والتزامن--runway-task-api--concurrency-model)
- [`GEN-56` قواعد المراجع في Seedance 2.0 R2V](#gen-56--قواعد-المراجع-في-seedance-20-r2v--seedance-20-reference-to-video-grammar)
- [`GEN-57` لقطة أداء مولدة متزامنة مع مقطع الأغنية](#gen-57--لقطة-أداء-مولدة-متزامنة-مع-مقطع-الأغنية--reference-to-video-performance-shot-synced-to-a-song-slice)
- [`GEN-58` ثبات الصوت عبر مرجع صوتي](#gen-58--ثبات-الصوت-عبر-مرجع-صوتي--voice-continuity-via-reference-audio)
- [`GEN-59` Veo عبر Gemini وقيود Sora 2](#gen-59--veo-عبر-gemini-وقيود-sora-2--veo-via-gemini--sora-2-constraints)
- [`GEN-60` منصات التجميع: fal وTogether وWaveSpeed وHF Spaces وVertex](#gen-60--منصات-التجميع-fal-وtogether-وwavespeed-وhf-spaces-وvertex--aggregator-hubs-fal-together-wavespeed-hf-spaces-vertex)
- [`GEN-61` خياطة الإطارات وسلاسل البداية/النهاية](#gen-61--خياطة-الإطارات-وسلاسل-البدايةالنهاية--frame-stitching--startend-image-chains-for-long-ai-video)
- [`GEN-62` فيديو مفتوح الأوزان: Wan 2.x وLTX وAnimateDiff](#gen-62--فيديو-مفتوح-الأوزان-wan-2x-وltx-وanimatediff--open-weights-video-wan-2x-ltx-video-animatediff)
- [`GEN-63` وصلة Higgsfield كمسار برومبت فقط](#gen-63--وصلة-higgsfield-كمسار-برومبت-فقط--higgsfield--paid-clip-route-as-prompt-only-deliverable)
- [`GEN-64` توليد الموسيقى: Lyria وMusicGen](#gen-64--توليد-الموسيقى-lyria-وmusicgen--music-generation-lyria--musicgen)
- [`GEN-65` كلمات أغنية وموجز Suno/Udio](#gen-65--كلمات-أغنية-وموجز-sunoudio--song-lyrics--sunoudio-brief)
- [`GEN-66` أمر واحد لجلب أي وسائط](#gen-66--أمر-واحد-لجلب-أي-وسائط--media-resolve-one-verb-for-any-asset)
- [`GEN-67` مقدم افتراضي ودبلجة وترجمة فيديو وتكبير](#gen-67--مقدم-افتراضي-ودبلجة-وترجمة-فيديو-وتكبير--avatar-presenter-dub-video-translate--upscale)
- [`GEN-68` توليد مجسمات ثلاثية بالذكاء](#gen-68--توليد-مجسمات-ثلاثية-بالذكاء--textimage--3d-model-meshy-tripo-rodin-trellis)
- [`GEN-69` توجيه مزودي الإبداع وشبكة الموصلات](#gen-69--توجيه-مزودي-الإبداع-وشبكة-الموصلات--creative-provider-routing--connector-mesh)
- [`GEN-70` خوادم المالك: KOSIF Think وJev والمنصة الخاصة](#gen-70--خوادم-المالك-kosif-think-وjev-والمنصة-الخاصة--owner-mcp-runtimes-kosif-think-jev-arbiter-private-workbench)
- [`GEN-71` البحث في مكتبة برومبتات المالك](#gen-71--البحث-في-مكتبة-برومبتات-المالك--owner-prompt-system-corpus-search)
- [`GEN-72` الرسم فوق لقطات مولدة (Draw-over)](#gen-72--الرسم-فوق-لقطات-مولدة-draw-over--draw-over-on-generated-bases)
- [`GEN-73` توليد ثم تتبّع](#gen-73--توليد-ثم-تتبّع--generate-then-trace)
- [`GEN-74` واجهات «جارٍ التوليد» من HyperFrames](#gen-74--واجهات-جارٍ-التوليد-من-hyperframes--ai-ui-motion-blocks-streaming-text-typed-prompt-chat-reveal)
- [`GEN-75` بطاقات توليد من الضبابية إلى الوضوح](#gen-75--بطاقات-توليد-من-الضبابية-إلى-الوضوح--blur-to-sharp-generating-tiles)
- [`GEN-76` صورة مولدة كمحتوى بطل داخل واجهة](#gen-76--صورة-مولدة-كمحتوى-بطل-داخل-واجهة--ai-photo-as-the-result-inside-a-ui-mock)
- [`GEN-77` شريط استعراض أصول مولدة بإخراج فني واحد](#gen-77--شريط-استعراض-أصول-مولدة-بإخراج-فني-واحد--ai-generated-asset-showreel-with-one-art-direction)
- [`GEN-78` عمل فني سائل قزحي](#gen-78--عمل-فني-سائل-قزحي--iridescent-liquid-artwork-generated-or-shaded)
- [`GEN-79` لقطة صلصال مولدة](#gen-79--لقطة-صلصال-مولدة--claymation-ai-shot)
- [`GEN-80` خلفية لوحة زيتية مولدة بحركة كن برنز](#gen-80--خلفية-لوحة-زيتية-مولدة-بحركة-كن-برنز--painterly-ai-backdrop-with-slow-ken-burns)
- [`GEN-81` كولاج مقصوص وبوابات زووم لا نهائي](#gen-81--كولاج-مقصوص-وبوابات-زووم-لا-نهائي--cutout-collage-portals-for-infinite-zoom-generated-or-sourced-cutouts)
- [`GEN-82` فيلم موشن بستوري بورد يكتب Claude كوده](#gen-82--فيلم-موشن-بستوري-بورد-يكتب-claude-كوده--storyboard-first-motion-film-with-claude-written-sandboxed-scene-code)
- [`GEN-83` فرز: توليد أم تركيب](#gen-83--فرز-توليد-أم-تركيب--generate-or-compose-triage)
- [`GEN-84` النص فوق الصورة لا داخلها](#gen-84--النص-فوق-الصورة-لا-داخلها--overlay-text-never-bake-it)
- [`GEN-85` المراسي الأربع للثبات البصري](#gen-85--المراسي-الأربع-للثبات-البصري--four-anchors-of-visual-consistency)
- [`GEN-86` انضباط ميزانية التوليد المدفوع](#gen-86--انضباط-ميزانية-التوليد-المدفوع--paid-generation-budget-discipline)
- [`GEN-87` الترخيص أولًا وFirefly المحمي قانونيًا](#gen-87--الترخيص-أولًا-وfirefly-المحمي-قانونيًا--licence-first-model-choice--indemnified-firefly)
- [`GEN-88` الإفصاح عن الوسائط المصطنعة وحدود التوليد](#gen-88--الإفصاح-عن-الوسائط-المصطنعة-وحدود-التوليد--synthetic-media-disclosure-provenance--ethical-limits)
- [`GEN-89` التمييز بين البرومبت والوسائط](#gen-89--التمييز-بين-البرومبت-والوسائط--prompt--media-honesty-rule)
- [`GEN-90` خدمة الصور المصغرة المدفوعة](#gen-90--خدمة-الصور-المصغرة-المدفوعة--thumbnail-generation-via-paid-mcp)
- [`GEN-G01` خط إنتاج من موضوع إلى فيديو قصير](#gen-g01--خط-إنتاج-من-موضوع-إلى-فيديو-قصير--topic-to-short-pipeline-with-reviewable-stages)
- [`GEN-P01` مراجعة ثانية مدفوعة من Claude API بقفلين](#gen-p01--مراجعة-ثانية-مدفوعة-من-claude-api-بقفلين--optional-paid-claude-api-second-opinion-review-double-opt-in)
- [`GEN-X01` إنتاج فيديو مرجعي عبر Higgsfield](#gen-x01--إنتاج-فيديو-مرجعي-عبر-higgsfield--higgsfield-reference-video-production-parameters-and-prompt-skeleton)
- [`GEN-X02` توليد متصل ثم قص](#gen-x02--توليد-متصل-ثم-قص--one-continuous-generation-then-cut)

## البطاقات / cards

### `GEN-01` — تشريح البرومبت السباعي والمعادلة الذهبية / Seven-layer prompt anatomy & golden formula

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل برومبت صورة أو فيديو يحمل سبع طبقات فيزيائية ملموسة بترتيب ثابت. / Every image/video prompt carries seven concrete physical layers in a fixed order.

**متى:** قبل أي برومبت توليد / before any generation prompt

**كيف:** Layers: Location · Subject · Wardrobe/materials · Lighting (source + direction + Kelvin) · Camera (body, lens, f-stop, size, move) · Atmosphere (physics: haze, dust, steam) · Technical (aspect, fps, resolution). One-line order: `[STYLE], [COMPOSITION RULE], [CAMERA+LENS+f-stop], [LIGHTING+Kelvin+direction], [SUBJECT texture], [WARDROBE fabric], [ENVIRONMENT layers], [ATMOSPHERE physics], mood: [EMOTION] --ar X:Y`. Example light: soft window key camera-left 3800K, fill −2 stops, cool rim behind; camera: Alexa Mini LF 50 mm f/1.4, eye level, MCU, slow push-in. Kelvin anchors: 1900K lantern, 3200K tungsten, 4100K moonlight, 6500K day.

**المعاملات:** 7 layers; 3200K/3800K/6500K; 35mm anamorphic, 50mm f/1.4, 85mm portrait; 24/60 fps; 9:16\|16:9

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** برومبت · طبقات · prompt anatomy · seven layers · Kelvin

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/seven-layer-anatomy.md`
- `100-superskills/skills/kosif-montage-motion/references/seven-layer-anatomy.md`
- `100-superskills/skills/kosif-montage-motion/references/ai_video_models.md`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/ai_video_models.md`

#### 7. قدرات قريبة في العائلة

- `GEN-02` القواعد الحديدية والكلمات القوية / Iron rules: physical cues beat hype words (proven)
- `GEN-03` قائمة النفي الأساسية والصياغة الإيجابية / Negative baseline vs positive framing (documented)

### `GEN-02` — القواعد الحديدية والكلمات القوية / Iron rules: physical cues beat hype words

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مصنع البرومبت يحذّرك آليًا من كلمات المبالغة ويطالب بإضاءة بمصدر واتجاه وكلفن. / The forge automatically warns on hype words and demands light with source, direction and Kelvin.

**متى:** عند مراجعة أي برومبت قبل إرساله / when reviewing any prompt before sending

**كيف:** Never open with 'a photo of'. Delete 4K/8K/masterpiece/ultra-detailed/award-winning/trending/best quality/beautiful/hyperrealistic — they add noise, not quality. Replace with physical cues: volumetric light, subsurface scattering, chiaroscuro, Rembrandt triangle, anamorphic flare, film grain, atmospheric perspective, tungsten practicals. Coherent style tokens (soft watercolor, line-art, isometric 3D, flat 2D, vintage scientific illustration) keep a set together. Locks must be reused verbatim — a paraphrase is flagged. Ran here: `prompt_forge.py` returned `missing ['lens','style']: prompts will be weaker` for a spec without them.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قواعد · كلمات قوية · iron rules · weak words · lint

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/prompt_forge.py:75`
- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`
- `kosif-atlas/skills/2657-figures/10108-ai-full-figure`
- `100-superskills/skills/kosif-montage-motion/scripts/aiprompts.py:21`

#### 7. قدرات قريبة في العائلة

- `GEN-01` تشريح البرومبت السباعي والمعادلة الذهبية / Seven-layer prompt anatomy & golden formula (documented)
- `GEN-03` قائمة النفي الأساسية والصياغة الإيجابية / Negative baseline vs positive framing (documented)
- `GEN-04` معادلة برومبت الصورة ذات الخانات الست / Six-slot still prompt formula (documented)

### `GEN-03` — قائمة النفي الأساسية والصياغة الإيجابية / Negative baseline vs positive framing

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** متى تكتب برومبت سلبي طويل (SD/SDXL/Kling) ومتى تحوّل كل نفي إلى حالة إيجابية (Gemini/Flux/Runway). / When to write a long negative (SD/SDXL/Kling) and when to rewrite every exclusion as a positive state (Gemini/Flux/Runway).

**متى:** عند صياغة المستبعدات لكل منصة / when phrasing exclusions per platform

**كيف:** Baseline negatives (SDXL, Kling negative_prompt): blurry, deformed hands, extra fingers, watermark, text overlay, low quality, bad anatomy, floating objects, duplicate limbs, disfigured, cropped, jpeg artifacts + scene anachronisms. For Gemini/Flux/Runway rewrite positively: 'no blur'→'tack-sharp focus', 'no people'→'empty, deserted', 'no text'→'clean, text-free surfaces'. Runway inverts or ignores negatives — the forge strips them. Flux has no negative field; Wan keeps negatives short.

**المعاملات:** Flux negative ≈ no effect; SDXL long negatives OK; Runway: none

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** برومبت سلبي · negative prompt · positive framing

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/seven-layer-anatomy.md`
- `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`
- `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design`
- `kosif-atlas/skills/2976-pwdev-social-media/12590-prompt-craft`

#### 7. قدرات قريبة في العائلة

- `GEN-01` تشريح البرومبت السباعي والمعادلة الذهبية / Seven-layer prompt anatomy & golden formula (documented)
- `GEN-02` القواعد الحديدية والكلمات القوية / Iron rules: physical cues beat hype words (proven)
- `GEN-04` معادلة برومبت الصورة ذات الخانات الست / Six-slot still prompt formula (documented)
- `GEN-05` برومبت سردي لنانو بنانا / Gemini / Narrative prose brief for Gemini / Nano Banana (documented)

### `GEN-04` — معادلة برومبت الصورة ذات الخانات الست / Six-slot still prompt formula

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** موضوع، مكان، أسلوب، إضاءة، تكوين، مواصفة تقنية — والعنصر الإلزامي أولًا لأن المولد يزن البداية أكثر. / Subject, setting, style, light, composition, tech spec — must-have element first because generators weight the start most.

**متى:** برومبتات Flux / Ideogram / GPT-image / SDXL

**كيف:** 40–80 words, 5–8 distinct descriptors; state the aspect ratio twice (in the text and in the API parameter); append brand palette words for campaign work.

**المعاملات:** 40–80 words; 5–8 descriptors; ratio ×2

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** صورة · still prompt · six slots

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1446-marketing-skills/3504-image`
- `kosif-atlas/skills/2976-pwdev-social-media/12590-prompt-craft`

#### 7. قدرات قريبة في العائلة

- `GEN-02` القواعد الحديدية والكلمات القوية / Iron rules: physical cues beat hype words (proven)
- `GEN-03` قائمة النفي الأساسية والصياغة الإيجابية / Negative baseline vs positive framing (documented)
- `GEN-05` برومبت سردي لنانو بنانا / Gemini / Narrative prose brief for Gemini / Nano Banana (documented)
- `GEN-06` دليل صياغة كل مولّد وترجمة صيغة ميدجورني / Per-generator syntax & Midjourney→natural-language translation (documented)

### `GEN-05` — برومبت سردي لنانو بنانا / Gemini / Narrative prose brief for Gemini / Nano Banana

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نماذج Gemini للصور تستجيب لفقرات وصفية أكثر من قوائم الوسوم. / Gemini image models respond to descriptive paragraphs better than comma tag lists.

**متى:** أي توليد أو تعديل عبر Gemini

**كيف:** 1–3 short paragraphs; name body/lens/stock when photographic (85 mm f/1.4, Kodak Portra 400); weight ≈ Subject 30 % · Style 25 % · Context 15 %; end with 'ultra-realistic, high resolution' instead of tag stuffing.

**المعاملات:** 30/25/15 %

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** نانو بنانا · Gemini · prose prompt

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`

#### 7. قدرات قريبة في العائلة

- `GEN-03` قائمة النفي الأساسية والصياغة الإيجابية / Negative baseline vs positive framing (documented)
- `GEN-04` معادلة برومبت الصورة ذات الخانات الست / Six-slot still prompt formula (documented)
- `GEN-06` دليل صياغة كل مولّد وترجمة صيغة ميدجورني / Per-generator syntax & Midjourney→natural-language translation (documented)
- `GEN-07` معادلة برومبت لقطة الفيديو / Video shot prompt formula (documented)

### `GEN-06` — دليل صياغة كل مولّد وترجمة صيغة ميدجورني / Per-generator syntax & Midjourney→natural-language translation

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كيف يريد كل مولد برومبته، وكيف تنقل برومبت ميدجورني إلى نموذج بلا أعلام. / How each generator wants its prompt, and how to port a Midjourney prompt to a flag-less model.

**متى:** عند نقل برومبت بين المنصات / when porting a prompt across platforms

**كيف:** ChatGPT/GPT-image: natural sentences, constraints first, ratio in words. Midjourney V7: params at end `--ar 16:9 --style raw --s 150 --v 7 --no text,watermark`; character ref `--oref URL --ow 100` (`--cref/--cw` are V6 only), `--sref URL`, `--stylize 50–250`, `--seed N` for a series; no official API → hand the user the prompt and import the chosen still back. Flux: prose, no negative field, guidance 3–4. SDXL: comma tags, `(term:1.2)` weights, separate negative, ~1 MP canvas. Ideogram: exact on-image text first, in quotes. Translation: `--ar`→aspect parameter; drop `--v/--style raw`; `--chaos 50`→'unexpected, surreal composition'; `(word:1.5)`→'prominently featuring word'; delete '8K, masterpiece'; keep camera names.

**المعاملات:** MJ --s 150–250, --ow 100; Flux guidance 3–4; SDXL ~1 MP

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ميدجورني · Midjourney · Flux · SDXL · Ideogram · syntax

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`
- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/references/prompt-patterns.md`
- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/prompt_forge.py:152`
- `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`

#### 7. قدرات قريبة في العائلة

- `GEN-04` معادلة برومبت الصورة ذات الخانات الست / Six-slot still prompt formula (documented)
- `GEN-05` برومبت سردي لنانو بنانا / Gemini / Narrative prose brief for Gemini / Nano Banana (documented)
- `GEN-07` معادلة برومبت لقطة الفيديو / Video shot prompt formula (documented)
- `GEN-08` منع الموسيقى والترجمة المزيفة في الفيديو المولد / Suppress generated music bed & fake subtitles (documented)

### `GEN-07` — معادلة برومبت لقطة الفيديو / Video shot prompt formula

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لقطة = أقفال + فعل واحد عبر الزمن + حركة كاميرا واحدة وسرعتها + عدسة + إضاءة + حركة البيئة + مدة/fps + أسلوب + نسبة. / Shot = locks + one action over time + one camera move & speed + lens + light + environment motion + duration/fps + style + aspect.

**متى:** أي برومبت نص→فيديو أو صورة→فيديو

**كيف:** 50–100 words (Runway best <100). Always state the camera move or 'static' — it is the parameter that changes results most and is most often forgotten. One scene per clip, never a scene change inside a clip, never request on-screen text. Generate 3–4 variations, then iterate on the best. Most-used camera words: wide, close-up, low angle, tracking, handheld, slow motion, establishing, crane, pan, dutch, bird's-eye, dolly zoom, rack focus; 2.35:1 reads as cinema.

**المعاملات:** 50–100 words; 1 camera move; 3–4 variations; shot 5–10 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** فيديو · لقطة · camera move · video prompt

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/video-prompt-director/SKILL.md:23`
- `kosif-atlas/skills/1446-marketing-skills/3531-video`
- `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen`
- `kosif-studio/motion/references/book-lessons.md`

#### 7. قدرات قريبة في العائلة

- `GEN-05` برومبت سردي لنانو بنانا / Gemini / Narrative prose brief for Gemini / Nano Banana (documented)
- `GEN-06` دليل صياغة كل مولّد وترجمة صيغة ميدجورني / Per-generator syntax & Midjourney→natural-language translation (documented)
- `GEN-08` منع الموسيقى والترجمة المزيفة في الفيديو المولد / Suppress generated music bed & fake subtitles (documented)
- `GEN-09` حدود مولدات الفيديو الحالية / Known limits of current video generators (documented)

### `GEN-08` — منع الموسيقى والترجمة المزيفة في الفيديو المولد / Suppress generated music bed & fake subtitles

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نماذج الفيديو الناطقة تضيف موسيقى وتحرق ترجمة مهلوسة؛ سطران يوقفان الاثنين. / Speaking video models add a music bed and burn hallucinated captions; two short lines stop both.

**متى:** كل مقطع مولد سيُركّب عليه صوتك أو نصك / every generated clip that will carry your own audio or type

**كيف:** Append exactly `No music score. No subtitles or on-screen text.` to every segment prompt; if a reference image contains signage add 'Only the text that exists in @Image1 itself'; do not list ambient sounds. Kling/Seedance: prefer generate_audio false and add sound in post (Kling audio ≈ 5× credits).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بلا موسيقى · no subtitles · clean plate · audio off

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/259-quickdesign/865-quickdesign`
- `kosif-atlas/skills/1874-klingai-pack/6081-klingai-pricing-basics`

#### 7. قدرات قريبة في العائلة

- `GEN-06` دليل صياغة كل مولّد وترجمة صيغة ميدجورني / Per-generator syntax & Midjourney→natural-language translation (documented)
- `GEN-07` معادلة برومبت لقطة الفيديو / Video shot prompt formula (documented)
- `GEN-09` حدود مولدات الفيديو الحالية / Known limits of current video generators (documented)
- `GEN-10` مصنع البرومبت: مواصفة واحدة ← تسع منصات / Prompt forge: one spec → 9 generator prompts (proven)

### `GEN-09` — حدود مولدات الفيديو الحالية / Known limits of current video generators

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** النص على الشاشة يخرج مشوهًا، اليدان والوجوه تفشل، الاستمرارية بين اللقطات صعبة، والمقاطع قصيرة. / On-screen text comes out illegible, hands/faces still fail, cross-shot continuity is hard, clips are short.

**متى:** عند تقرير ما يُولَّد وما يُبنى بالكود / when deciding what to generate vs build in code

**كيف:** Plan cuts, not continuity; keep 1–2 subjects; compose text in the edit; build long pieces as a montage of 4–15 s clips; no subject that must stay identical across >3 shots without reference-to-video.

**المعاملات:** clips 4–15 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** حدود · limits · continuity

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `imagemagick` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen`
- `kosif-atlas/skills/1446-marketing-skills/3531-video`

#### 7. قدرات قريبة في العائلة

- `GEN-07` معادلة برومبت لقطة الفيديو / Video shot prompt formula (documented)
- `GEN-08` منع الموسيقى والترجمة المزيفة في الفيديو المولد / Suppress generated music bed & fake subtitles (documented)
- `GEN-10` مصنع البرومبت: مواصفة واحدة ← تسع منصات / Prompt forge: one spec → 9 generator prompts (proven)
- `GEN-11` خصائص منصات الفيديو (DNA) / Video-model platform DNA (Veo / Runway / Kling / Sora) (proven)

### `GEN-10` — مصنع البرومبت: مواصفة واحدة ← تسع منصات / Prompt forge: one spec → 9 generator prompts

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يحوّل مواصفة مشهد واحدة إلى برومبتات منسقة لـ ChatGPT وMidjourney وFlux وSDXL وIdeogram وSora وVeo وRunway وKling مع تحذيرات و3 تنويعات ومقياس جودة. / Turns one scene spec into correctly shaped prompts for ChatGPT image, Midjourney, Flux, SDXL, Ideogram, Sora, Veo, Runway and Kling, with warnings, 3 variations and a rubric.

**متى:** أي طلب «اكتب لي برومبت لـ…» / any 'write me a prompt for…' request

**كيف:** `echo '<spec json>' \| python3 -I kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/prompt_forge.py` (or MCP `kosif_prompt_forge`). Spec keys: mode, subject, action, environment, time, shot, angle, lens, lighting, palette, style, quality[], aspect, negative[], text, locks{}, camera_move, duration, motion, fps, dialogue, audio, platforms[]. Output keys: prompts, warnings, variations {subtle, dramatic, technical}, quality_rubric, next. SDXL canvas map 1:1 1024², 16:9 1344×768, 9:16 768×1344, 4:5 896×1152, 3:2 1216×832, 2.39:1 1536×640; SDXL CFG 5–7, 30–40 steps. Ran here on 2026-10-16 with a 9-platform video spec: valid JSON, per-platform notes, warnings returned.

**المعاملات:** 9 platforms; variations subtle/dramatic/technical; SDXL CFG 5–7, 30–40 steps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مصنع البرومبت · prompt forge · multi-platform · MCP

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/prompt_forge.py:97`
- `kosif-one/tools/kosif-omni/mcp-server/tests/test_server.py:233`
- `100-superskills/skills/kosif-montage-motion/references/visual-catalog.md`

#### 7. قدرات قريبة في العائلة

- `GEN-08` منع الموسيقى والترجمة المزيفة في الفيديو المولد / Suppress generated music bed & fake subtitles (documented)
- `GEN-09` حدود مولدات الفيديو الحالية / Known limits of current video generators (documented)
- `GEN-11` خصائص منصات الفيديو (DNA) / Video-model platform DNA (Veo / Runway / Kling / Sora) (proven)
- `GEN-12` مواصفة الصورة الموحدة وستة مُنشئات / Image spec schema → 6 platform builders (proven)

### `GEN-11` — خصائص منصات الفيديو (DNA) / Video-model platform DNA (Veo / Runway / Kling / Sora)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** القواعد الخاصة بكل نموذج فيديو التي يطبقها المصنع تلقائيًا. / Per-model rules the forge applies automatically.

**متى:** عند اختيار صياغة لكل منصة فيديو / when shaping a prompt per video platform

**كيف:** Veo: separate 'Audio:' sentence for ambience/SFX, dialogue as `Character says: "…"` (no subtitles), 4/6/8 s clips, last frame → next first frame. Runway Gen-4: one action per shot, sequential 'X, then Y', positive phrasing only, ≤ ~300 words, start from an approved keyframe, ≤3 refs, 2–10 s. Kling: start/end frames + motion brush, 5–10 s, negative prompt allowed. Sora: one continuous shot, plausible physics, 4/8/12 s, prompt ≤4000 chars. Printed in the `notes` field when the forge ran here.

**المعاملات:** Veo 4/6/8 s; Kling 5–10 s; Runway 2–10 s ≤3 refs; Sora 4/8/12 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Veo · Runway · Kling · Sora · platform rules

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/prompt_forge.py:183`
- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/references/books-drive-ledger.md`
- `kosif-atlas/skills/259-quickdesign/865-quickdesign`

#### 7. قدرات قريبة في العائلة

- `GEN-09` حدود مولدات الفيديو الحالية / Known limits of current video generators (documented)
- `GEN-10` مصنع البرومبت: مواصفة واحدة ← تسع منصات / Prompt forge: one spec → 9 generator prompts (proven)
- `GEN-12` مواصفة الصورة الموحدة وستة مُنشئات / Image spec schema → 6 platform builders (proven)
- `GEN-13` قوالب لقطات الفيديو لسبع منصات مع قص المدة / Shot list → 7 video-platform prompts with duration clamping (proven)

### `GEN-12` — مواصفة الصورة الموحدة وستة مُنشئات / Image spec schema → 6 platform builders

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ملف JSON واحد (موضوع، بيئة، لقطة، إضاءة، أسلوب، نسبة، نفي، أقفال) يولّد برومبتات Midjourney وFlux وSDXL وChatGPT وIdeogram وNanoBanana مع فحص. / One JSON spec drives Midjourney, Flux, SDXL, ChatGPT, Ideogram and NanoBanana prompts plus a lint pass.

**متى:** طلبات صور ثابتة متعددة المنصات / multi-platform still requests

**كيف:** `python3 100-superskills/skills/image-prompt-forge/scripts/image_prompt_forge.py spec.json --out prompts.md`; required: subject, environment, shot, lighting, style, aspect. Builders: MJ comma core + `--ar --s 200 --v 7 --no …`; Flux prose + 'Avoid:' clause; SDXL `(subject:1.3)` + JSON {steps 30, cfg 6.0, 1344×768 for 16:9, 768×1344 for 9:16, 896×1120 for 4:5}; ChatGPT 'Create one single image. Aspect ratio X. Do not include …' first; Ideogram quoted text first + `--ar` (best route for in-image text, still overlay Arabic yourself); NanoBanana 'Generate a single photorealistic-quality image… Exclude: …'. Ran here: all six blocks emitted, lint `PASS`.

**المعاملات:** MJ --s 200 --v 7; SDXL 30 steps cfg 6.0; 12 MJ aspects

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مواصفة صورة · image spec · Midjourney · SDXL · NanoBanana · Ideogram

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/image-prompt-forge/scripts/image_prompt_forge.py:77`
- `100-superskills/skills/image-prompt-forge/scripts/image_prompt_forge.py:102`
- `100-superskills/TESTS.md:12`

#### 7. قدرات قريبة في العائلة

- `GEN-10` مصنع البرومبت: مواصفة واحدة ← تسع منصات / Prompt forge: one spec → 9 generator prompts (proven)
- `GEN-11` خصائص منصات الفيديو (DNA) / Video-model platform DNA (Veo / Runway / Kling / Sora) (proven)
- `GEN-13` قوالب لقطات الفيديو لسبع منصات مع قص المدة / Shot list → 7 video-platform prompts with duration clamping (proven)
- `GEN-14` برومبتات اللقطات السباعية (kmotion aiprompts) / kmotion aiprompts: 7-layer per-shot prompts (proven)

### `GEN-13` — قوالب لقطات الفيديو لسبع منصات مع قص المدة / Shot list → 7 video-platform prompts with duration clamping

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قائمة لقطات JSON تتحول إلى برومبت لكل لقطة لـ Veo وSora وKling وRunway وLuma وPika وHailuo، مع قص المدة لحد كل منصة وفحص الاستمرارية. / A JSON shot list becomes per-shot prompts for Veo, Sora, Kling, Runway, Luma, Pika and Hailuo, durations clamped to each platform and continuity linted.

**متى:** خطة لقطات لفيلم مولد / a generated-film shot plan

**كيف:** `python3 100-superskills/skills/video-prompt-director/scripts/video_prompt_forge.py shots.json --platforms veo,sora,kling,runway,luma,pika,hailuo`. Limits: Veo 8, Sora 20, Kling 10, Runway 10, Luma 9, Pika 10, Hailuo 10 s. Lint: BLOCK on named real people, REVISE when no character/style lock, flags >1 camera word per shot. Put `aspect` and `fps` at the TOP level of shots.json (ran here: a per-shot aspect was ignored and 16:9 was used; a 12 s shot was clamped to 8 s for Veo).

**المعاملات:** max s: veo 8, sora 20, kling 10, runway 10, luma 9, pika 10, hailuo 10; fps 24 default

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قائمة لقطات · shot list · Luma · Pika · Hailuo · duration

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/video-prompt-director/scripts/video_prompt_forge.py:23`
- `100-superskills/skills/video-prompt-director/scripts/video_prompt_forge.py:63`
- `100-superskills/skills/video-prompt-director/SKILL.md:23`

#### 7. قدرات قريبة في العائلة

- `GEN-11` خصائص منصات الفيديو (DNA) / Video-model platform DNA (Veo / Runway / Kling / Sora) (proven)
- `GEN-12` مواصفة الصورة الموحدة وستة مُنشئات / Image spec schema → 6 platform builders (proven)
- `GEN-14` برومبتات اللقطات السباعية (kmotion aiprompts) / kmotion aiprompts: 7-layer per-shot prompts (proven)
- `GEN-15` من فيديو مرجعي إلى برومبت Omni Flash / Reference breakdown → Omni Flash generation prompt (proven)

### `GEN-14` — برومبتات اللقطات السباعية (kmotion aiprompts) / kmotion aiprompts: 7-layer per-shot prompts

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل لقطة توصف بسبع طبقات ثم تتحول إلى برومبتات Veo وSora وKling وRunway وإطار مفتاحي، بقفل أسلوب ونفي وتحذير فيزيائي. / Each shot in seven layers becomes Veo/Sora/Kling/Runway prompts plus a keyframe, with a carried style lock, negatives and a physics warning.

**متى:** من ريل أو مشروع kmotion إلى برومبتات توليد / from a kmotion reel or project to generation prompts

**كيف:** `python3 scripts/kmotion.py aiprompts SHOTS.json\|reel.json\|PROJECT --out ai-video-prompts.json`; `aiprompts.build(shots, title)` → shots[{layers, prompts{veo,sora,kling,runway}, warnings}]; Runway ≤1000 chars, Kling ≤2500 + negative_prompt; warning when lighting lacks direction or Kelvin; variations subtle/dramatic/technical; rubric 5×20. Example lock: 'photoreal 35mm film look, cool 4100K moonlight vs warm 1900K lantern'. Ran here: `AIPromptTests.test_seven_layers_per_platform` OK.

**المعاملات:** Runway ≤1000 chars; Kling ≤2500; rubric 5×20

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** kmotion · aiprompts · seven layers · per-shot

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/aiprompts.py:21`
- `100-superskills/skills/kosif-montage-motion/tests/test_review.py:121`
- `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/index.html:35`
- `100-superskills/skills/kosif-montage-motion/references/ai-video-shot-prompts.example.json`

#### 7. قدرات قريبة في العائلة

- `GEN-12` مواصفة الصورة الموحدة وستة مُنشئات / Image spec schema → 6 platform builders (proven)
- `GEN-13` قوالب لقطات الفيديو لسبع منصات مع قص المدة / Shot list → 7 video-platform prompts with duration clamping (proven)
- `GEN-15` من فيديو مرجعي إلى برومبت Omni Flash / Reference breakdown → Omni Flash generation prompt (proven)
- `GEN-16` مواصفة مشهد مكتوبة وبصمة SHA-256 / Typed SceneSpec compile + SHA-256 digest (proven)

### `GEN-15` — من فيديو مرجعي إلى برومبت Omni Flash / Reference breakdown → Omni Flash generation prompt

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تفكيك فيلم مرجعي إلى إيقاعات وألوان وطاقة، ثم برومبت توليد واحد مضغوط إلى 10 ثوانٍ. / Break a reference film into beats, palette and energy, then one compact 10 s generation prompt.

**متى:** «اعمل لي فيديو زي ده» / 'make me one like this'

**كيف:** 1) `python3 scripts/kmotion.py analyze VIDEO --out NAME.breakdown [--transcribe]` (beats from cuts/dissolves/entrances, per-beat hex, energy, LUFS/BPM, 3 stills per beat, brief.json; `--batch` → library.json/csv). 2) Fill the brief (you or the user). 3) `kmotion omniprompt brief.json [--overrides changes.json] [--markdown b.md]` → one block STYLE / SPECS / TIMELINE / ADD / BRAND MARK / TYPOGRAPHY LOCK / SOUND / FINAL FRAME / EXCLUDE, ≥1080 short side, compressed to 10 s (×0.83 for 12 s); overrides {palette:{old:new}, aspect, duration, tone, add[], remove[]}; refuses to remove what scenes are built on; an unfilled brief exits. Ran here: `Breakdown.test_omniprompt` OK (11.7 s).

**المعاملات:** 10 s native; ≥1080 short side; ×0.83 for 12 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أومني · Omni Flash · reference video · breakdown

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/omniprompt.py`
- `100-superskills/skills/kosif-montage-motion/tests/test_analyze.py:65`
- `100-superskills/skills/kosif-montage-motion/SKILL.md:455`
- `100-superskills/skills/kosif-montage-motion/references/video-breakdown.md`

#### 7. قدرات قريبة في العائلة

- `GEN-13` قوالب لقطات الفيديو لسبع منصات مع قص المدة / Shot list → 7 video-platform prompts with duration clamping (proven)
- `GEN-14` برومبتات اللقطات السباعية (kmotion aiprompts) / kmotion aiprompts: 7-layer per-shot prompts (proven)
- `GEN-16` مواصفة مشهد مكتوبة وبصمة SHA-256 / Typed SceneSpec compile + SHA-256 digest (proven)
- `GEN-17` أقفال الشخصية والأسلوب والمكان / Character / style / location locks (proven)

### `GEN-16` — مواصفة مشهد مكتوبة وبصمة SHA-256 / Typed SceneSpec compile + SHA-256 digest

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مواصفة مشهد مهيكلة تتحول إلى برومبت حتمي وبصمة؛ أي تغيير في أي حقل يغيّر البصمة فلا ينجرف البرومبت المعتمد. / A structured scene compiles to a deterministic prompt and digest; any field change changes the digest, so the approved prompt cannot drift.

**متى:** عند اعتماد برومبت مع العميل وتوثيقه / when an approved prompt must be locked and audited

**كيف:** `prompt_compiler.compile_prompt(scene)` → {prompt, negative_prompt, scene_digest, scene_spec}; 11 required fields: subject, environment, action, camera, lighting, color_grade, materials, atmosphere_vfx, composition_story, negative_constraints, aspect_ratio (W:H). Digest = sha256 over sorted compact JSON. Ran here: `prompt_compiler_self_test.py` → PASS.

**المعاملات:** 11 fields; sha256(sorted compact JSON)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** بصمة · SceneSpec · digest · deterministic

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/scripts/prompt_compiler.py`
- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/scripts/prompt_compiler_self_test.py`

#### 7. قدرات قريبة في العائلة

- `GEN-14` برومبتات اللقطات السباعية (kmotion aiprompts) / kmotion aiprompts: 7-layer per-shot prompts (proven)
- `GEN-15` من فيديو مرجعي إلى برومبت Omni Flash / Reference breakdown → Omni Flash generation prompt (proven)
- `GEN-17` أقفال الشخصية والأسلوب والمكان / Character / style / location locks (proven)
- `GEN-18` واجهة الأنماط المرحلية (Fastify) / Stage-gated profile CLI (proven)

### `GEN-17` — أقفال الشخصية والأسلوب والمكان / Character / style / location locks

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كتل نصية ثابتة تُنسخ حرفيًا في كل برومبت ولقطة لتثبيت الهوية. / Fixed text blocks copied verbatim into every prompt and shot for identity consistency.

**متى:** أي سلسلة صور أو لقطات بنفس الشخصية / any series with the same character

**كيف:** In spec.json: `locks.character` appended to the subject, `locks.style` to the style, `locks.location` at the end. One canonical sentence per character (age, skin, hair, glasses, garment fabric), never paraphrased. Both forges emit it; the video forge flags REVISE when no lock exists.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** قفل الشخصية · character lock · style lock · consistency

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/image-prompt-forge/SKILL.md:22`
- `100-superskills/skills/image-prompt-forge/scripts/image_prompt_forge.py:61`
- `kosif-atlas/skills/1094-akbun-draw/2423-akbun-draw-webtoon-b`

#### 7. قدرات قريبة في العائلة

- `GEN-15` من فيديو مرجعي إلى برومبت Omni Flash / Reference breakdown → Omni Flash generation prompt (proven)
- `GEN-16` مواصفة مشهد مكتوبة وبصمة SHA-256 / Typed SceneSpec compile + SHA-256 digest (proven)
- `GEN-18` واجهة الأنماط المرحلية (Fastify) / Stage-gated profile CLI (proven)
- `GEN-19` سلاسل برومبتات الأنماط الخمسة / Five profile prompt series (stickman, fitness, car, history, food) (proven)

### `GEN-18` — واجهة الأنماط المرحلية (Fastify) / Stage-gated profile CLI

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** واجهة سطر أوامر واحدة تقود سبعة أنماط لكتابة البرومبتات بجلسات محفوظة؛ كل مرحلة تحتاج ردًا صريحًا. / One CLI drives seven prompt-writing profiles with persistent sessions; every stage needs an explicit reply.

**متى:** عندما يطلب المستخدم نوع إنتاج محدد (stickman, food-flow…) / when the user names a production type

**كيف:** `cd fastify-motion-bro && npm run profile -- list \| start <mode> \| answer <mode> <text\|JSON> \| status \| reset \| clean-plate kinetic-flow <n>`; state in projects/profiles/<mode>/session.json; on completion writes prompts.txt + artifacts.json (schema fmb.profile.v1). Ran here: `node --test tests/viral-editorial.test.mjs tests/production-profiles.test.mjs tests/production-cli.test.mjs` → 19/19 pass.

**المعاملات:** schema fmb.profile.v1; 7 modes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** fastify · profile · CLI · stage-gated

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/scripts/profiles-cli.mjs:1-40`
- `fastify-motion-bro/scripts/profiles/core.mjs:9-10`
- `fastify-motion-bro/tests/production-cli.test.mjs:11-42`

#### 7. قدرات قريبة في العائلة

- `GEN-16` مواصفة مشهد مكتوبة وبصمة SHA-256 / Typed SceneSpec compile + SHA-256 digest (proven)
- `GEN-17` أقفال الشخصية والأسلوب والمكان / Character / style / location locks (proven)
- `GEN-19` سلاسل برومبتات الأنماط الخمسة / Five profile prompt series (stickman, fitness, car, history, food) (proven)
- `GEN-20` حزمة الكينتك فلو واللقطة النظيفة / Kinetic Flow prompt pack + clean plate & overlay sheet (proven)

### `GEN-19` — سلاسل برومبتات الأنماط الخمسة / Five profile prompt series (stickman, fitness, car, history, food)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خمس حزم جاهزة تنتج أزواج صورة/حركة أو سلاسل لقطات مع مؤثرات صوتية وتعليمات الربط. / Five ready packs producing image/motion pairs or clip series with foley and join instructions.

**متى:** طلب من نوع إنتاج معروف / a known production genre

**كيف:** Each is started with `npm run profile -- start <mode>` and answered stage by stage; outputs are prompts, never media (see the honesty rule). \| \| mode \| first answer \| output \| numbers \| \|---\|---\|---\|---\| \| stickman \| `{"image":"no","background":"paper","genre":4,"direction":"coffee shop"}` \| 5 × (IMAGE PROMPT + Flow MOTION PROMPT) \| 7 s each = 35 s; wide → medium → OTS ¾ → low → close-up; clip 5 very slow push-in \| \| fitness \| `Chest` (or 1–10) \| 5 image-to-video prompts, one gym bay, one coach line each \| 5 × 6 s = 30 s; breath/equipment SFX \| \| car-exploded \| `Toyota` → `Corolla` → `{"year":"2024","trim":"LE","color":"white"}` \| exactly 3: hero still, exploded still, animation \| 3 prompts \| \| vox-history \| `6` → topic → `10` \| N × 10 s archival-collage prompts, flagged needsFactCheck \| N 5–120; phases origins / first signal / people / turning point / public response / legacy \| \| food-flow \| `2` → `4` \| N × 10 s single-action prompts, locked scene, synced foley, tasting shot last \| N × 10 s + join order \|

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** stickman · fitness · car exploded · vox history · food flow · سلاسل

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/scripts/profiles/stickman.mjs:19-55`
- `fastify-motion-bro/scripts/profiles/fitness.mjs:17-38`
- `fastify-motion-bro/scripts/profiles/car-exploded.mjs:36-60`
- `fastify-motion-bro/scripts/profiles/vox-history.mjs:3-56`
- `fastify-motion-bro/tests/production-profiles.test.mjs:10-16`

#### 7. قدرات قريبة في العائلة

- `GEN-17` أقفال الشخصية والأسلوب والمكان / Character / style / location locks (proven)
- `GEN-18` واجهة الأنماط المرحلية (Fastify) / Stage-gated profile CLI (proven)
- `GEN-20` حزمة الكينتك فلو واللقطة النظيفة / Kinetic Flow prompt pack + clean plate & overlay sheet (proven)
- `GEN-21` برومبتات البوستر والحركة التحريرية / Viral-editorial poster + silent motion prompts (proven)

### `GEN-20` — حزمة الكينتك فلو واللقطة النظيفة / Kinetic Flow prompt pack + clean plate & overlay sheet

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** برومبت Google Flow/Veo لكل مقطع 8 أو 10 ث بالكلمات الحرفية، وعند الطلب نسخة «لقطة نظيفة» بلا نص مع ورقة نصوص للمونتاج. / One Flow/Veo prompt per 8 or 10 s clip with the exact script words; on request a text-free clean plate plus an overlay sheet for the editor.

**متى:** ريل كينتك مولّد؛ وللعربية دائمًا اللقطة النظيفة / a generated kinetic reel; for Arabic always the clean plate

**كيف:** `npm run profile -- start kinetic-flow`; `answer kinetic-flow '{"theme":"C","ratio":"9:16","length":10,"brand":"","pace":"fast","audio":"none"}'`; `answer kinetic-flow '<script>'`. Then `clean-plate kinetic-flow <n>` rewrites clip n to forbid all on-screen text/wordmarks and returns {order, words, hero, masked reveal} so you set the exact (Arabic) words in HTML/Remotion over the plate.

**المعاملات:** clip 8 s (Veo) / 10 s (Flow); 9:16\|16:9\|1:1; audio none\|sfx

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** كينتك · kinetic flow · clean plate · overlay

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:85-120`
- `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:121-129`
- `fastify-motion-bro/tests/production-cli.test.mjs:28-41`

#### 7. قدرات قريبة في العائلة

- `GEN-18` واجهة الأنماط المرحلية (Fastify) / Stage-gated profile CLI (proven)
- `GEN-19` سلاسل برومبتات الأنماط الخمسة / Five profile prompt series (stickman, fitness, car, history, food) (proven)
- `GEN-21` برومبتات البوستر والحركة التحريرية / Viral-editorial poster + silent motion prompts (proven)
- `GEN-22` بذور برومبت في كل سقالة / Per-shot AI prompt seeds written by the scaffold (ready)

### `GEN-21` — برومبتات البوستر والحركة التحريرية / Viral-editorial poster + silent motion prompts

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** برومبت إطار 9:16 لكل سطر سكربت بلوحة ألوان مقفلة وبطل واحد مقصوص، ثم برومبت حركة صامتة 6 ث بخط زمني من 4 أجزاء. / A 9:16 keyframe prompt per script line with locked palette and one cut-out hero, then a silent 6 s motion prompt with a 4-part timeline.

**متى:** ريلز تحريري ثلاثي الأبعاد / viral editorial 3D reels

**كيف:** `makePosters(state)` after palette lock: fine grid, two background lines, exactly one 3D-looking hero cutout with halftone edge, ≤2 vector accents (starburst + dotted orbit), 1–4 word type pairing bold sans + italic serif, 10 % side margin, 80/20 colour. `makeMotionPrompts(state)`: style, backgroundMotion, timeline{base, entrance, hold, exit}, camera 4 % push, easeOutCubic with 7 % overshoot, 0.6° wobble, SFX cues, music=false, voiceover=false.

**المعاملات:** 9:16; 6 s; 4 % push; 7 % overshoot; 0.6° wobble; 80/20

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تحريري · viral editorial · poster · keyframe

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/scripts/viral-editorial.mjs:52-57`
- `fastify-motion-bro/scripts/viral-editorial.mjs:58-72`
- `fastify-motion-bro/tests/viral-editorial.test.mjs:7`

#### 7. قدرات قريبة في العائلة

- `GEN-19` سلاسل برومبتات الأنماط الخمسة / Five profile prompt series (stickman, fitness, car, history, food) (proven)
- `GEN-20` حزمة الكينتك فلو واللقطة النظيفة / Kinetic Flow prompt pack + clean plate & overlay sheet (proven)
- `GEN-22` بذور برومبت في كل سقالة / Per-shot AI prompt seeds written by the scaffold (ready)
- `GEN-23` تخطيط موجه لنماذج الفيديو / ProPlan model-prompt stage with continuity locks (ready)

### `GEN-22` — بذور برومبت في كل سقالة / Per-shot AI prompt seeds written by the scaffold

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سقالة المشروع تكتب ملف JSON ببرومبتات بداية لأربعة نماذج فيديو وسطر قفل أسلوب مشترك. / The project scaffold also writes a JSON of starter prompts for four video models plus a shared style-lock line.

**متى:** عندما يريد المستخدم نسخة مولدة موازية لفيلم الكود / when the user wants a generated twin of the coded film

**كيف:** `ultra_animator new …` writes ai_prompts.json with style_lock + shots[].veo2_prompt / sora_prompt / kling_prompt / runway_gen3_prompt at 0–30 % shot times; then refine with kosif_prompt_forge and lint with kosif_image_prompt_lint. Replace the seed lock's '8k, octane render' hype words before use (iron rules).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** scaffold · seeds · ultra animator

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/ultra_animator.py:119`
- `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/scripts/projects/demo_hero/ai_prompts.json`

#### 7. قدرات قريبة في العائلة

- `GEN-20` حزمة الكينتك فلو واللقطة النظيفة / Kinetic Flow prompt pack + clean plate & overlay sheet (proven)
- `GEN-21` برومبتات البوستر والحركة التحريرية / Viral-editorial poster + silent motion prompts (proven)
- `GEN-23` تخطيط موجه لنماذج الفيديو / ProPlan model-prompt stage with continuity locks (ready)
- `GEN-24` معادلة برومبت النماذج اللغوية ومدققها / LLM prompt formula + linter (prompts for agents & generators) (ready)

### `GEN-23` — تخطيط موجه لنماذج الفيديو / ProPlan model-prompt stage with continuity locks

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المخطِّط يتعرف على طلبات برومبتات Veo/Sora/Kling/Runway ويضيف مرحلة برومبت مع أقفال الاستمرارية. / The planner recognises Veo/Sora/Kling/Runway prompt requests and inserts a stage with continuity locks.

**متى:** عند تخطيط إنتاج يجمع كودًا وتوليدًا / planning a job that mixes code and generation

**كيف:** `python3 kosif-studio/motion/proplan.py --task 'prompt for veo …'` → inserts 'model_prompt_with_continuity' locking speaker identity, font family, palette and direction of motion.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** proplan · continuity · planning

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/proplan.py:37`
- `kosif-studio/motion/proplan.py:109`

#### 7. قدرات قريبة في العائلة

- `GEN-21` برومبتات البوستر والحركة التحريرية / Viral-editorial poster + silent motion prompts (proven)
- `GEN-22` بذور برومبت في كل سقالة / Per-shot AI prompt seeds written by the scaffold (ready)
- `GEN-24` معادلة برومبت النماذج اللغوية ومدققها / LLM prompt formula + linter (prompts for agents & generators) (ready)
- `GEN-25` مثال مصر 2120: حزمة برومبتات كاملة / Worked example: Egypt 2120 multi-platform pack (documented)

### `GEN-24` — معادلة برومبت النماذج اللغوية ومدققها / LLM prompt formula + linter (prompts for agents & generators)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** هيكل وفحص حتمي لبرومبتات النظام والمهام والوكلاء — مفيد حين تكتب أنت برومبتًا لنموذج آخر أو وكيل فرعي. / Structure and deterministic lint for system/task/agent/tool prompts — for when you write prompts for another model or sub-agent.

**متى:** قبل إرسال برومبت لوكيل أو لمولد آخر / before handing a prompt to an agent or another generator

**كيف:** Formula `<role> <context> <task> <inputs> <constraints> <output_format> <edge_cases> <quality_bar>`; lint via `python3 kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/llm_prompt_lint.py` or MCP `kosif_llm_prompt_lint {prompt, kind, contract, untrusted_inputs}` → exit 0/1/3. Companion instruction-only skills: prompt-master-pro (blind-spot questions before a motion job), structured-output-json, system-prompt-architect, prompt-architect-reasoning-models.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** LLM prompt · lint · agents · system prompt

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/llm_prompt_lint.py`
- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/SKILL.md`
- `100-superskills/skills/prompt-master-pro/SKILL.md`
- `100-superskills/skills/structured-output-json/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `GEN-22` بذور برومبت في كل سقالة / Per-shot AI prompt seeds written by the scaffold (ready)
- `GEN-23` تخطيط موجه لنماذج الفيديو / ProPlan model-prompt stage with continuity locks (ready)
- `GEN-25` مثال مصر 2120: حزمة برومبتات كاملة / Worked example: Egypt 2120 multi-platform pack (documented)
- `GEN-26` كتالوج الأساليب المسماة (أكثر من 30 مظهرًا) / Named look catalogue (30+ looks) (documented)

### `GEN-25` — مثال مصر 2120: حزمة برومبتات كاملة / Worked example: Egypt 2120 multi-platform pack

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مثال جاهز لخمس لقطات سولاربانك مصرية بقفل أسلوب ونفي وتنويعات لأربع منصات. / A ready five-shot solarpunk Egypt pack with style lock, negatives and variations for four platforms.

**متى:** كقالب إدخال لأي فيلم مولد / as a template input for any generated film

**كيف:** Shots: orbit dive, Giza solar mirrors, Nile train, Cairo lotus tower, Alexandria Pharos; 9:16, 30 fps; lenses 24/35/28/24/35 mm; durations 3/4/4/4/3 s; palette gold / warm white / cyan on near-black; negatives: text artifacts, logos, watermarks, real people, distorted pyramids, dystopia, smog, flags. Kling gets an explicit negative; Runway none; Veo notes last-frame chaining.

**المعاملات:** 5 shots; 9:16 30 fps; 3/4/4/4/3 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** مصر 2120 · solarpunk · example

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/projects/egypt-2120-animation/ai-video-prompts.json`
- `100-superskills/skills/kosif-montage-motion/references/ai-video-shot-prompts.example.json`

#### 7. قدرات قريبة في العائلة

- `GEN-23` تخطيط موجه لنماذج الفيديو / ProPlan model-prompt stage with continuity locks (ready)
- `GEN-24` معادلة برومبت النماذج اللغوية ومدققها / LLM prompt formula + linter (prompts for agents & generators) (ready)
- `GEN-26` كتالوج الأساليب المسماة (أكثر من 30 مظهرًا) / Named look catalogue (30+ looks) (documented)
- `GEN-27` مقدمات الأسلوب المتطابقة بايتًا / Byte-identical style preambles (documented)

### `GEN-26` — كتالوج الأساليب المسماة (أكثر من 30 مظهرًا) / Named look catalogue (30+ looks)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** سلاسل وصف جاهزة لأساليب بصرية مسماة تُلصق في طبقة الأسلوب. / Ready descriptor strings for named visual styles, pasted into the style layer.

**متى:** اختيار المظهر في أول جلسة / choosing the look at kickoff

**كيف:** Pick one look, paste its descriptor into the style layer, then lock it (style lock). Describe traits, never a living artist's name. The library names more looks than it defines: Steampunk, Pixel Art, Low/High-poly 3D, Minimalist, Abstract, Pop Art, Fantasy, Sci-Fi, Romantic, Experimental, isometric, film look, photorealistic editorial — write their lock yourself. \| \| look \| descriptor core \| \|---\|---\| \| Cinematic Masterpiece \| ARRI Alexa 65, anamorphic flare, grain, ACES \| \| Photorealistic \| RAW, sharp, subsurface scattering, Hasselblad \| \| Anime \| Ghibli-like watercolour backgrounds, cel shading \| \| 3D Render \| Pixar-like stylised 3D, AO, GI \| \| Dark Fantasy \| gothic, volumetric fog, chiaroscuro \| \| Product Commercial \| hyper-real studio product \| \| Cyberpunk Neon \| neon, holograms, rain reflections, teal + magenta \| \| Film Noir \| B&W, venetian blinds, smoke, 1940s \| \| Vintage Film \| Portra-400 grain, warm, light leak \| \| Watercolour \| wet-on-wet, bleeding edges, paper \| \| Surrealism \| impossible physics, melting \| \| Documentary \| photojournalistic, available light \| \| Baroque Oil \| Rembrandt chiaroscuro, impasto \| \| Gothic Horror \| candlelight, fog, stone \| \| Symmetric pastel (Wes-Anderson-like) \| symmetry, pastel, centred \| \| Solarpunk \| living architecture, bioluminescence \| \| Claymation \| stop-motion, fingerprints \| \| Comic Book \| outlines, halftone \| \| Vaporwave / Synthwave \| pink-purple-cyan, glitch, 80s \| \| Ukiyo-e \| woodblock, flat planes \|

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** أساليب · looks · style catalogue · anime · noir · cyberpunk

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/visual-catalog.md`
- `100-superskills/skills/kosif-montage-motion/references/visual-catalog.md`
- `100-superskills/skills/ai-art-style-library/SKILL.md:16`

#### 7. قدرات قريبة في العائلة

- `GEN-24` معادلة برومبت النماذج اللغوية ومدققها / LLM prompt formula + linter (prompts for agents & generators) (ready)
- `GEN-25` مثال مصر 2120: حزمة برومبتات كاملة / Worked example: Egypt 2120 multi-platform pack (documented)
- `GEN-27` مقدمات الأسلوب المتطابقة بايتًا / Byte-identical style preambles (documented)
- `GEN-28` استخراج قفل الأسلوب / Style-lock extraction (documented)

### `GEN-27` — مقدمات الأسلوب المتطابقة بايتًا / Byte-identical style preambles

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | MIT (vendor scroll-world) |

**ما هي:** مقدمة أسلوب واحدة متطابقة حرفًا بحرف قبل كل برومبت صورة تبقي العالم متماسكًا. / One byte-identical style preamble before every still prompt keeps a world cohesive.

**متى:** سلسلة لقطات لعالم واحد (scroll-world، فيلم منتج) / a series of stills for one world

**كيف:** Prefix every still prompt with the preamble; inject `[BG_HEX]` and `[PALETTE]`; always end with a 'no text' tail. \| \| preamble \| core words \| \|---\|---\| \| clay diorama \| isometric low-poly floating island, matte clay, tilt-shift, soft contact shadow \| \| flat papercraft \| layered cardstock, die-cut \| \| glossy toy \| vinyl toy, rim light \| \| claymation \| plasticine thumbprints, softbox \| \| photoreal architectural \| golden hour, magazine-interior look, full-bleed, no knockout \|

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** preamble · مقدمة أسلوب · clay diorama · papercraft

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/scroll-world/skills/scroll-world/references/prompts.md:33`

#### 7. قدرات قريبة في العائلة

- `GEN-25` مثال مصر 2120: حزمة برومبتات كاملة / Worked example: Egypt 2120 multi-platform pack (documented)
- `GEN-26` كتالوج الأساليب المسماة (أكثر من 30 مظهرًا) / Named look catalogue (30+ looks) (documented)
- `GEN-28` استخراج قفل الأسلوب / Style-lock extraction (documented)
- `GEN-29` مكتبات المعدِّلات حسب المجال وقوالب التصوير / Domain modifiers, photo templates & camera bodies (documented)

### `GEN-28` — استخراج قفل الأسلوب / Style-lock extraction

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر الأسلوب حسب العاطفة والجمهور، استخرج كتلة كلمات دقيقة، طابق العدسة والإضاءة معه، واختبره على موضوعين. / Pick a style by emotion/audience, extract an exact keyword block, match lens and light to it, test on two subjects.

**متى:** قبل أي سلسلة / before any series

**كيف:** Write style-lock.txt (traits, not studio/artist names; per-style negatives) → feed as `locks.style` to image_prompt_forge; test on 2 different subjects; if both hold, freeze it.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** style lock · قفل الأسلوب · ثبات الأسلوب · توحيد اللوك · كلمات البرومبت · consistent style · style keywords

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/ai-art-style-library/SKILL.md:21`

#### 7. قدرات قريبة في العائلة

- `GEN-26` كتالوج الأساليب المسماة (أكثر من 30 مظهرًا) / Named look catalogue (30+ looks) (documented)
- `GEN-27` مقدمات الأسلوب المتطابقة بايتًا / Byte-identical style preambles (documented)
- `GEN-29` مكتبات المعدِّلات حسب المجال وقوالب التصوير / Domain modifiers, photo templates & camera bodies (documented)
- `GEN-30` مفردات التلوين وحزم أسلوب الفيديو / Grade vocabulary, film stocks & video style packs (documented)

### `GEN-29` — مكتبات المعدِّلات حسب المجال وقوالب التصوير / Domain modifiers, photo templates & camera bodies

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مفردات جاهزة لكل نوع لقطة تجعل الصورة مخرَجة لا عامة. / Ready vocabularies per shot domain that make plates look art-directed, not generic.

**متى:** كتابة طبقة الكاميرا والإضاءة / writing the camera & light layers

**كيف:** Cinema: ARRI Alexa 65 / RED V-Raptor, Cooke S7/i or anamorphic primes, Kodak Vision3 500T/250D. Product: polished marble or gradient sweep, 100 mm macro, softbox + strip rims, 45° hero or flat lay, focus-stacked 1:1. Portrait: 85/105/135 mm, f/1.4–f/5.6, Rembrandt, 4:5. Food: overhead window light, 50 mm, 4:5. Landscape: 16 mm, leading lines, foreground/mid/background layers, blue or golden hour, haze, 16:9. Bodies: Alexa 65/Mini LF, RED V-Raptor/Komodo, Venice 2, IMAX 70 mm, Hasselblad X2D, URSA 12K, Ronin 4D, iPhone/Pixel Pro, GoPro/FPV, VHS.

**المعاملات:** 85mm f/1.4; 100mm macro; 16mm; Vision3 500T

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** عدسات · lenses · camera bodies · product · portrait

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`
- `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`
- `100-superskills/skills/kosif-montage-motion/references/visual-catalog.md`

#### 7. قدرات قريبة في العائلة

- `GEN-27` مقدمات الأسلوب المتطابقة بايتًا / Byte-identical style preambles (documented)
- `GEN-28` استخراج قفل الأسلوب / Style-lock extraction (documented)
- `GEN-30` مفردات التلوين وحزم أسلوب الفيديو / Grade vocabulary, film stocks & video style packs (documented)
- `GEN-31` وصفات أساليب كلينج بنطاقات cfg_scale / Kling style recipes with cfg_scale bands (documented)

### `GEN-30` — مفردات التلوين وحزم أسلوب الفيديو / Grade vocabulary, film stocks & video style packs

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أسماء مظاهر وأفلام تصوير وحزم كلمات قصيرة توجه لون ومزاج اللقطة المولدة. / Named looks, film stocks and short keyword packs that steer the grade and mood of generated footage.

**متى:** عندما يجب أن يطابق اللقطة المولدة تلوين الفيلم / when a generated shot must match the film's grade

**كيف:** Looks: teal & orange, desaturated cold, warm vintage, high-contrast noir. Stocks: Kodak Vision3 500T (tungsten night), Vision3 250D (daylight), Fuji Eterna Vivid, Kodak Portra. Packs — Cinematic: cinematic grading, anamorphic flare, shallow DOF, film grain, 35 mm. Documentary: handheld, natural light, candid. Commercial: clean even light, bright and airy. Social: vertical 9:16, high contrast, saturated. Then grade the result for real in post (COLOR family) — prompt words only get you close.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** تلوين · film stock · grade · style pack

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/347-legends-seo-dungeon/1261-seo-image-gen/references/prompt-engineering.md`
- `kosif-atlas/skills/1446-marketing-skills/3531-video`
- `kosif-atlas/skills/1874-klingai-pack/6087-klingai-style-transfer`

#### 7. قدرات قريبة في العائلة

- `GEN-28` استخراج قفل الأسلوب / Style-lock extraction (documented)
- `GEN-29` مكتبات المعدِّلات حسب المجال وقوالب التصوير / Domain modifiers, photo templates & camera bodies (documented)
- `GEN-31` وصفات أساليب كلينج بنطاقات cfg_scale / Kling style recipes with cfg_scale bands (documented)
- `GEN-32` البرومبت العكسي ونقد الصورة / Reverse prompt & image critique (documented)

### `GEN-31` — وصفات أساليب كلينج بنطاقات cfg_scale / Kling style recipes with cfg_scale bands

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الأسلوب في Kling = كلمات + مدى التزام النموذج بها (cfg_scale 0–1). / In Kling, style = keywords + how strictly the model follows them (cfg_scale 0–1).

**متى:** توليد Kling بأسلوب محدد / styled Kling generation

**كيف:** Lower cfg for realism (model freedom), higher for strongly stylised looks. \| \| style \| keywords \| cfg_scale \| \|---\|---\|---\| \| photoreal \| — \| 0.4–0.5 \| \| cinematic \| anamorphic lens, film grain, 35mm \| 0.5–0.6 \| \| neon cyberpunk \| neon, rain reflections \| 0.5–0.6 \| \| anime \| cel-shaded, clean lines \| 0.6–0.7 \| \| vintage 8 mm \| light leaks \| 0.6–0.7 \| \| watercolor / oil \| wet edges / impasto \| 0.7–0.8 \| \| pixel art \| 16-bit limited palette \| 0.8–0.9 \|

**المعاملات:** cfg 0.4–0.9

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Kling · cfg_scale · style transfer

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1874-klingai-pack/6087-klingai-style-transfer`

#### 7. قدرات قريبة في العائلة

- `GEN-29` مكتبات المعدِّلات حسب المجال وقوالب التصوير / Domain modifiers, photo templates & camera bodies (documented)
- `GEN-30` مفردات التلوين وحزم أسلوب الفيديو / Grade vocabulary, film stocks & video style packs (documented)
- `GEN-32` البرومبت العكسي ونقد الصورة / Reverse prompt & image critique (documented)
- `GEN-33` أنت المولّد: صورة من وصف بالكود (SVG / Canvas / PIL / Three.js) / You are the generator: picture from a description as code (ready)

### `GEN-32` — البرومبت العكسي ونقد الصورة / Reverse prompt & image critique

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تحليل عربي من 11 عنوانًا ينتهي ببرومبت إنجليزي لإعادة الإنشاء، وتحويل صورة مرجعية إلى طبقات سبع. / An 11-heading Arabic analysis ending in an English recreation prompt; turn a reference image into the seven layers.

**متى:** عندما يرسل المستخدم صورة ويقول «زيها» / when the user sends an image and says 'like this'

**كيف:** Measure first, then: الخلاصة، التكوين، الكاميرا، الإضاءة، الألوان، العناصر، الجودة التقنية، مؤشرات التوليد، الدرجات /10، الإصلاحات، برومبت إعادة الإنشاء (lint it). Commands /compare, /ocr (Arabic RTL, [؟] for unreadable), /critique, /reverse, /score. No face identification. Automated captioners (Florence-2 PromptGen, WD14, BLIP) need ComfyUI; Ideogram describe returns a structured JSON prompt. Only on images the user owns or may use.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** برومبت عكسي · reverse prompt · critique · OCR

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `tesseract` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-vision/SKILL.md`
- `100-superskills/skills/image-critique-reverse-prompt/SKILL.md:25`
- `kosif-atlas/skills/2142-comfyui-plugin/7651-comfy-image-utils`

#### 7. قدرات قريبة في العائلة

- `GEN-30` مفردات التلوين وحزم أسلوب الفيديو / Grade vocabulary, film stocks & video style packs (documented)
- `GEN-31` وصفات أساليب كلينج بنطاقات cfg_scale / Kling style recipes with cfg_scale bands (documented)
- `GEN-33` أنت المولّد: صورة من وصف بالكود (SVG / Canvas / PIL / Three.js) / You are the generator: picture from a description as code (ready)
- `GEN-34` استخراج الكود من رد الذكاء الاصطناعي / AI-reply code extraction (proven)

### `GEN-33` — أنت المولّد: صورة من وصف بالكود (SVG / Canvas / PIL / Three.js) / You are the generator: picture from a description as code

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قبل أي مولد خارجي، ارسم الصورة بنفسك برنامجًا: SVG أو PIL أو مشهد KOSIF أو صفحة Three.js — قابلة للتحريك والتعديل والعربية سليمة. / Before any external model, paint the picture yourself as a program — SVG, PIL, a KOSIF scene or a Three.js page — animatable, editable, with correct Arabic.

**متى:** خلفيات، ملصقات، أيقونات، رسوم مسطحة، مشاهد بسيطة / backgrounds, stickers, icons, flat illustration, simple scenes

**كيف:** Format routing: SVG 1200×800 viewBox drawn back-to-front with no filters; PIL for raster textures; Three.js page with a `render(t)` contract (three@0.170.0 from cdn.jsdelivr.net). Sticker: 512×512, thick white outline, 2–4 palette colours, no text. SVG background: full-frame viewBox, dark ground dominant, ≤3 gradients, calm empty centre. Always sanitise: strip script, foreignObject, image, iframe, a, style, animate, set, on* attributes, external href/url() and javascript:. Studio extract_code pulls the runnable block from a reply.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** SVG · كود · picture from code · sticker · no key

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/studio.py:55`
- `kosif-studio/studio.py:856`
- `app/public/js/00_editor.js:1669`

#### 7. قدرات قريبة في العائلة

- `GEN-31` وصفات أساليب كلينج بنطاقات cfg_scale / Kling style recipes with cfg_scale bands (documented)
- `GEN-32` البرومبت العكسي ونقد الصورة / Reverse prompt & image critique (documented)
- `GEN-34` استخراج الكود من رد الذكاء الاصطناعي / AI-reply code extraction (proven)
- `GEN-35` جسر الذكاء في الاستوديو (Claude CLI / API / يدوي) / Studio AI bridge: Claude CLI → API → manual (ready)

### `GEN-34` — استخراج الكود من رد الذكاء الاصطناعي / AI-reply code extraction

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يسحب الكتلة القابلة للتشغيل من رد مغلّف بنثر وأسوار ```، مفضّلًا الكتل التي تحمل IMAGE_B64 أو imports أو markup. / Pulls the runnable block out of a prose-and-fences reply, preferring blocks with IMAGE_B64, imports or markup.

**متى:** كلما وصلك كود من نموذج آخر أو وكيل / whenever code comes back from another model or agent

**كيف:** `studio.extract_code(text)`: regex over fenced blocks; falls back to stripping lone fences; bare code returned as is. Ran here directly: prose + ```python block → 'import io\nx=1'. (Its unittest file also imports cv2: `pip install opencv-python-headless` to run the full suite.)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** extract code · fences · parser

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/studio.py:156`
- `kosif-studio/tests/test_studio.py:433`

#### 7. قدرات قريبة في العائلة

- `GEN-32` البرومبت العكسي ونقد الصورة / Reverse prompt & image critique (documented)
- `GEN-33` أنت المولّد: صورة من وصف بالكود (SVG / Canvas / PIL / Three.js) / You are the generator: picture from a description as code (ready)
- `GEN-35` جسر الذكاء في الاستوديو (Claude CLI / API / يدوي) / Studio AI bridge: Claude CLI → API → manual (ready)
- `GEN-36` صورة فوتوغرافية محلية sd-turbo أو Pollinations / Photo from prompt: local sd-turbo or Pollinations (install)

### `GEN-35` — جسر الذكاء في الاستوديو (Claude CLI / API / يدوي) / Studio AI bridge: Claude CLI → API → manual

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يختار كيف يسأل الاستوديو نموذجًا: `claude -p` محليًا أولًا، ثم Messages API بمفتاح، وإلا حزمة نسخ ولصق بتعليمات عربية. / Chooses how the studio asks a model: local `claude -p` first, then the Messages API with a key, else a copy-paste package with Arabic steps.

**متى:** تعديل صورة أو توليد صورة من وصف داخل kosif-studio / editing or creating a picture inside kosif-studio

**كيف:** `python3 kosif-studio/ai_bridge.py [prompt]`; settings.json backend auto\|cli\|api\|none; prompts ≥28 000 chars go via stdin; CLI readiness cached 10 min; defaults model <mid-tier Claude model>, max_tokens 8000, timeout 240 s. Edit flow (Ctrl+E): reply must contain IMAGE_B64 and `# EDITS START`; result drawn original-first then edit; Ctrl+Z undo. With backend none it always works (manual package).

**المعاملات:** ≥28000 chars → stdin; 10 min cache; 240 s timeout

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** AI bridge · claude -p · studio · edit

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/ai_bridge.py:56`
- `kosif-studio/ai_bridge.py:99`
- `kosif-studio/studio.py:799`

#### 7. قدرات قريبة في العائلة

- `GEN-33` أنت المولّد: صورة من وصف بالكود (SVG / Canvas / PIL / Three.js) / You are the generator: picture from a description as code (ready)
- `GEN-34` استخراج الكود من رد الذكاء الاصطناعي / AI-reply code extraction (proven)
- `GEN-36` صورة فوتوغرافية محلية sd-turbo أو Pollinations / Photo from prompt: local sd-turbo or Pollinations (install)
- `GEN-37` توليد وتعديل الصور بـ Gemini (نانو بنانا) / Gemini / Nano Banana image generate & edit (key)

### `GEN-36` — صورة فوتوغرافية محلية sd-turbo أو Pollinations / Photo from prompt: local sd-turbo or Pollinations

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | sd-turbo weights: Stability AI community licence (check commercial terms); Pollinations: service terms |

**ما هي:** عندما لا يرسم الكود صورة فوتوغرافية: sd-turbo محليًا على المعالج، أو Pollinations FLUX أونلاين بموافقة. / When code cannot paint a photograph: sd-turbo locally on CPU, or Pollinations FLUX online with consent.

**متى:** لقطة خلفية فوتوغرافية بلا مفتاح / a photographic plate without a key

**كيف:** `python3 kosif-studio/generate.py "prompt" --out out/photo.png --backend local --size 1344x768 --seed 7 [--negative …] [--code]`. Local: 4 steps, guidance 0, dims multiple of 8, ~2 GB weights from huggingface.co (reachable here); CPU only (4 cores, 15 GB RAM) — expect minutes, not seconds. Online backend: model flux, nologo, enhance false, 180 s timeout — pollinations is not in the verified-hosts list, ask before sending any prompt off-machine. `--code` also writes a Python program for the result.

**المعاملات:** 4 steps; guidance 0; ÷8 dims; seed 7

**التثبيت:** pip install diffusers torch transformers accelerate

**الوسوم:** sd-turbo · local · Pollinations · photo · CPU

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:torch` ← python3 -c "import torch" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `network` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-studio/generate.py:24`
- `kosif-studio/generate.py:53`
- `kosif-one/tools/kosif-studio/generate.py`
- `100-superskills/skills/pixel-studio-painter/scripts/generate.py`

#### 7. قدرات قريبة في العائلة

- `GEN-34` استخراج الكود من رد الذكاء الاصطناعي / AI-reply code extraction (proven)
- `GEN-35` جسر الذكاء في الاستوديو (Claude CLI / API / يدوي) / Studio AI bridge: Claude CLI → API → manual (ready)
- `GEN-37` توليد وتعديل الصور بـ Gemini (نانو بنانا) / Gemini / Nano Banana image generate & edit (key)
- `GEN-38` تحرير بمراجع متعددة قبل التحريك (نانو بنانا) / Nano Banana multi-reference edit before animation (key)

### `GEN-37` — توليد وتعديل الصور بـ Gemini (نانو بنانا) / Gemini / Nano Banana image generate & edit

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صور B-roll وخلفيات وطبقات وملصقات وتعديل صور موجودة بنسبة المشروع ولوحته. / B-roll stills, backgrounds, layers, stickers and edits of existing pictures in the project's aspect and palette.

**متى:** عندما تحتاج صورة لا يرسمها الكود / when code cannot paint the still

**كيف:** REST: `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key=$GEMINI_API_KEY` with responseModalities IMAGE (or TEXT+IMAGE), imageConfig.aspectRatio, imageSize uppercase '512'\|'1K'\|'2K'\|'4K'; decode base64 inlineData to PNG; ≤5 reference images as extra parts. Models: gemini-3.1-flash-image (default), gemini-2.5-flash-image (fixed 1K), gemini-3-pro-image. App route (basma): Claude first rewrites the request through an image formula and the film LOOK (doodle = thick friendly outlines, flat pastel; chalkboard = white chalk on dark green; product = dramatic studio light, glossy); sticker vs photo prompt; always 'no text/watermark'.

**المعاملات:** 14 ratios incl. 1:8, 8:1, 21:9; ~$0.02/0.04/0.08/0.16 per 512/1K/2K/4K; free ≈10 RPM

**التثبيت:** pip install google-genai (optional SDK)

**الوسوم:** Gemini · نانو بنانا · Nano Banana · image edit

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1481-llm-tools/3666-gemini-image`
- `app/public/js/00_editor.js:1917`
- `app/public/js/10_studio.js:4164`
- `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`

#### 7. قدرات قريبة في العائلة

- `GEN-35` جسر الذكاء في الاستوديو (Claude CLI / API / يدوي) / Studio AI bridge: Claude CLI → API → manual (ready)
- `GEN-36` صورة فوتوغرافية محلية sd-turbo أو Pollinations / Photo from prompt: local sd-turbo or Pollinations (install)
- `GEN-38` تحرير بمراجع متعددة قبل التحريك (نانو بنانا) / Nano Banana multi-reference edit before animation (key)
- `GEN-39` عائلة FLUX عبر Together وحلقة Kontext / FLUX via Together + Kontext edit round-trip + LoRA (key)

### `GEN-38` — تحرير بمراجع متعددة قبل التحريك (نانو بنانا) / Nano Banana multi-reference edit before animation

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صحّح أو ركّب الإطار الأول بتعديل صورة رخيص واعتمده قبل صرف نقاط الفيديو. / Fix or compose the first frame with a cheap image edit and approve it before spending on video.

**متى:** قبل أي صورة→فيديو / before any image-to-video

**كيف:** Label refs @Image1…(≈5 in the API, up to 14 in the app); prompt only the change: 'Edit @Image1: change pose to …; keep face, hair, lighting'; 2K default, 4K for fine product text. Recipes: decade re-style, multi-image composite, character sheet from one image (same person from back/left/right), 'retain the look' style ref, staging 'retain structure and composition', outfit swap, storyboard marker style. Forge v4 marks version-sensitive syntax unverified unless the provider is confirmed current.

**المعاملات:** image ≈12 credits vs clip 250–500

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** character sheet · multi-reference · edit · نانو بنانا

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/259-quickdesign/865-quickdesign`
- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/references/books-drive-ledger.md`
- `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/prompt_forge_v4_truth.py`

#### 7. قدرات قريبة في العائلة

- `GEN-36` صورة فوتوغرافية محلية sd-turbo أو Pollinations / Photo from prompt: local sd-turbo or Pollinations (install)
- `GEN-37` توليد وتعديل الصور بـ Gemini (نانو بنانا) / Gemini / Nano Banana image generate & edit (key)
- `GEN-39` عائلة FLUX عبر Together وحلقة Kontext / FLUX via Together + Kontext edit round-trip + LoRA (key)
- `GEN-40` GPT Image وIdeogram للصور ذات النص / GPT Image & Ideogram V4 (text-capable stills, edit, describe) (key)

### `GEN-39` — عائلة FLUX عبر Together وحلقة Kontext / FLUX via Together + Kontext edit round-trip + LoRA

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** FLUX.2 وFLUX.1 schnell وKontext وImagen 4 وغيرها خلف نقطة واحدة؛ ثم Kontext يغيّر شيئًا واحدًا ويحفظ الباقي. / FLUX.2, FLUX.1 schnell, Kontext, Imagen 4 and more behind one endpoint; then Kontext changes one thing and keeps the rest.

**متى:** مسودات رخيصة سريعة وتعديل موضعي / cheap fast drafts and targeted edits

**كيف:** `client.images.generate(model, prompt, width, height, steps, seed)` with TOGETHER_API_KEY; sizes 1024², 1344×768, 768×1344, 1248×832, 1184×864; schnell 4 steps; guidance 3.5 default (1–5 creative, 8–10 faithful). Kontext: model black-forest-labs/FLUX.1-kontext-pro (or -max), image_url = previous result, 'replace the car colour with blue', 28 steps; save both versions. FLUX.2 dev: ≤2 image_loras at scale 0.3–1.2 + reference_images. Cost = MP × price/MP × steps/default.

**المعاملات:** schnell 4 steps; Kontext 28; LoRA ≤2 @0.3–1.2

**التثبيت:** pip install together

**الوسوم:** FLUX · Kontext · Together · LoRA

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/3214-togetherai-skills/13594-together-images`

#### 7. قدرات قريبة في العائلة

- `GEN-37` توليد وتعديل الصور بـ Gemini (نانو بنانا) / Gemini / Nano Banana image generate & edit (key)
- `GEN-38` تحرير بمراجع متعددة قبل التحريك (نانو بنانا) / Nano Banana multi-reference edit before animation (key)
- `GEN-40` GPT Image وIdeogram للصور ذات النص / GPT Image & Ideogram V4 (text-capable stills, edit, describe) (key)
- `GEN-41` صور Higgsfield (Soul v2 / Marketing Studio / gpt_image_2) / Higgsfield image generation (key)

### `GEN-40` — GPT Image وIdeogram للصور ذات النص / GPT Image & Ideogram V4 (text-capable stills, edit, describe)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مسارا الصور حين يُطلب نص داخل الصورة أو تحرير بقناع أو وصف منظم. / The still routes when in-image text, masked edits or a structured description are needed.

**متى:** لافتة أو منتج عليه كلمات لاتينية / a sign or product carrying Latin words

**كيف:** GPT Image (gpt-image-1/2) via OpenAI Images API (OPENAI_API_KEY) or Codex `image_gen`; transparent background for icons; quality high when text is requested; may rewrite prompts. Ideogram V4: multipart POST https://api.ideogram.ai/v1/ideogram-v4/generate (or /async + poll), header Api-Key; JSON prompting disables magic prompt; check is_image_safe; download at once (URLs expire). Tools: mask edit, remix, describe → structured JSON (boxes 0–1000 [y_min,x_min,y_max,x_max]), bg remove/replace, reframe, upscale, text layerization; inputs ≤25 MB. Arabic: still overlay real type yourself.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** GPT Image · Ideogram · text in image · describe

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1446-marketing-skills/3504-image`
- `kosif-atlas/skills/2657-figures/10115-transparent-icons`
- `kosif-atlas/skills/1869-ideogram-pack/5946-ideogram-core-workflow-a`
- `kosif-atlas/skills/1869-ideogram-pack/5947-ideogram-core-workflow-b`

#### 7. قدرات قريبة في العائلة

- `GEN-38` تحرير بمراجع متعددة قبل التحريك (نانو بنانا) / Nano Banana multi-reference edit before animation (key)
- `GEN-39` عائلة FLUX عبر Together وحلقة Kontext / FLUX via Together + Kontext edit round-trip + LoRA (key)
- `GEN-41` صور Higgsfield (Soul v2 / Marketing Studio / gpt_image_2) / Higgsfield image generation (key)
- `GEN-42` وصفة صور الهوية: كائن معدني وكريستال (ذهبي/جليدي) / Brand-still recipe: metal + crystal object on brand ground (key)

### `GEN-41` — صور Higgsfield (Soul v2 / Marketing Studio / gpt_image_2) / Higgsfield image generation

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** توليد صور لقطات خلفية بالتوازي عبر عميل Higgsfield الرسمي. / Plate stills in parallel through the official Higgsfield client.

**متى:** عندما يملك المالك رصيد Higgsfield / when the owner's Higgsfield credit is available

**كيف:** `subscribe('marketing-studio/image', {prompt: shot + STYLE, aspect_ratio: '9:16', resolution: '2k'})` or 'higgsfield-ai/soul/v2/standard' for a credential check; ThreadPoolExecutor(6); skip files that exist; save sources.json URL map. CLI alt: `higgsfield generate create gpt_image_2 --aspect_ratio 3:2 --resolution 2k --quality high --wait` (3–8 min each; run detached). HF_KEY='key-id:key-secret' in .env.local (gitignored).

**المعاملات:** 9:16 2k; 6 workers; 3–8 min/still

**التثبيت:** pip install higgsfield-client python-dotenv

**الوسوم:** Higgsfield · Soul · marketing studio

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:higgsfield` ← python3 -c "import higgsfield" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/projects/higgsfield/image.py`
- `kosif-one/projects/whatsapp-motion/gen_images.py`
- `kosif-one/projects/whatsapp-motion/assets/sources.json`
- `kosif-one/vendor/scroll-world/skills/scroll-world/references/pipeline.md`

#### 7. قدرات قريبة في العائلة

- `GEN-39` عائلة FLUX عبر Together وحلقة Kontext / FLUX via Together + Kontext edit round-trip + LoRA (key)
- `GEN-40` GPT Image وIdeogram للصور ذات النص / GPT Image & Ideogram V4 (text-capable stills, edit, describe) (key)
- `GEN-42` وصفة صور الهوية: كائن معدني وكريستال (ذهبي/جليدي) / Brand-still recipe: metal + crystal object on brand ground (key)
- `GEN-43` لقطات بمساحة فارغة للكتابة / AI plates that reserve typography space (key)

### `GEN-42` — وصفة صور الهوية: كائن معدني وكريستال (ذهبي/جليدي) / Brand-still recipe: metal + crystal object on brand ground

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قواعد برومبت لصور قطاعات بالهوية: كائن رمزي واحد معدن مصقول + كريستال مضلّع على خلفية لون الهوية، إضاءة حافة دافئة، ونفي صارم للنص والشعارات والناس. / Prompt grammar for on-brand sector stills: one symbolic object in polished metal + faceted crystal on a flat brand ground, warm rim light, hard negative against text, logos and people.

**متى:** صور قطاعات وأغلفة لمنصة KOSIF Earth / sector & cover stills

**كيف:** Gold identity: ground #0B1F3A, metal #C9A227, 'luxury annual report' mood. Ice variant: 'ice-blue brushed metal and faceted clear crystal on a deep cobalt-night background #0B1030, cool cyan rim light #19C3D9'. Suffix: 'No text, no letters, no numbers, no logos, no people'. Higgsfield Image 2.0, quality high, 2k; post: hflip for RTL space, WebP q80 (1600 w heroes, 720×480 sectors, 1200 audit, 900 cover). Measured spend: ~$0.21/image fixed ratio, 15 images + 2 clips = $3.79.

**المعاملات:** #0B1F3A / #C9A227; ice #0B1030 / #19C3D9; WebP q80

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** هوية · brand still · crystal · navy gold · RTL hflip

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:higgsfield` ← python3 -c "import higgsfield" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-earth-ci-fork/docs/design/HIGGSFIELD_VISUALS_ar.md`
- `kosif-earth-ci-fork/AGENT_WORKLOG.md:744`

#### 7. قدرات قريبة في العائلة

- `GEN-40` GPT Image وIdeogram للصور ذات النص / GPT Image & Ideogram V4 (text-capable stills, edit, describe) (key)
- `GEN-41` صور Higgsfield (Soul v2 / Marketing Studio / gpt_image_2) / Higgsfield image generation (key)
- `GEN-43` لقطات بمساحة فارغة للكتابة / AI plates that reserve typography space (key)
- `GEN-44` أيقونات شفافة بثيم وشرائط سبرايت ثابتة / Themed transparent icons & consistent sprite strips (key)

### `GEN-43` — لقطات بمساحة فارغة للكتابة / AI plates that reserve typography space

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كل برومبت لقطة ينتهي بلاحقة أسلوب مشتركة تطلب ثلثًا علويًا/سفليًا فارغًا وبلا أي نص. / Every shot prompt ends with a shared style suffix asking for empty upper/lower thirds and no text at all.

**متى:** خلفيات سيُكتب فوقها نص عربي متحرك / plates that will carry animated Arabic type

**كيف:** Shared STYLE suffix: editorial cinematic photography, shallow depth of field, anamorphic look, grain, empty upper/lower thirds, no text, letters, logos or watermark. Example set of six plates (s1_question … s6_paths) at 9:16 2k. Then place type in the empty third with the ARAB/TYPE families.

**المعاملات:** 6 plates; 9:16 2k

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** negative space · plates · مساحة للنص

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/projects/whatsapp-motion/gen_images.py:19-37`
- `kosif-atlas/skills/2976-pwdev-social-media/12583-creative-concept/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `GEN-41` صور Higgsfield (Soul v2 / Marketing Studio / gpt_image_2) / Higgsfield image generation (key)
- `GEN-42` وصفة صور الهوية: كائن معدني وكريستال (ذهبي/جليدي) / Brand-still recipe: metal + crystal object on brand ground (key)
- `GEN-44` أيقونات شفافة بثيم وشرائط سبرايت ثابتة / Themed transparent icons & consistent sprite strips (key)
- `GEN-45` تعديل قبل إعادة التوليد: توسيع وترميم وقص وتكبير / Edit before regenerate: outpaint, inpaint, cut-out, upscale (install)

### `GEN-44` — أيقونات شفافة بثيم وشرائط سبرايت ثابتة / Themed transparent icons & consistent sprite strips

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | icons skill BSD-3-Clause; sprite skills MIT |

**ما هي:** أيقونات مسطحة بخلفية شفافة من ملف ثيم، وشريط حركة كامل بتعديل واحد من إطار بذرة معتمد. / Flat transparent icons styled by a theme JSON, and a whole animation strip in one edit from an approved seed frame.

**متى:** مجموعة أيقونات أو شخصية سبرايت لفيلم / an icon set or a sprite character

**كيف:** Icons: generate_icon.py via Codex image_gen, OpenAI Images or a flux-schnell host, --size 1024; theme {palette, stroke weight, style/negative tokens}; fallback near-white threshold or rembg. Sprites: image-edit API from the seed frame; prompt invariants: same character, facing, palette, silhouette, transparent bg, exact frame count; then Pillow normalise to one shared scale and a bottom-centre anchor.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** icons · sprite · أيقونات · transparent

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:rembg` ← python3 -c "import rembg" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/2657-figures/10115-transparent-icons`
- `kosif-atlas/skills/2696-game-studio/10368-sprite-pipeline`
- `kosif-atlas/skills/1526-gamegen/4171-game-sprites`

#### 7. قدرات قريبة في العائلة

- `GEN-42` وصفة صور الهوية: كائن معدني وكريستال (ذهبي/جليدي) / Brand-still recipe: metal + crystal object on brand ground (key)
- `GEN-43` لقطات بمساحة فارغة للكتابة / AI plates that reserve typography space (key)
- `GEN-45` تعديل قبل إعادة التوليد: توسيع وترميم وقص وتكبير / Edit before regenerate: outpaint, inpaint, cut-out, upscale (install)
- `GEN-46` شجرة اختيار نموذج الصور والترخيص أولًا / Image-model routing tree (licence first) (documented)

### `GEN-45` — تعديل قبل إعادة التوليد: توسيع وترميم وقص وتكبير / Edit before regenerate: outpaint, inpaint, cut-out, upscale

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | rembg MIT; model weights per their cards |

**ما هي:** إذا وُجد أصل معتمد فوسّعه أو رمّمه أو افصل موضوعه أو كبّره بدل رمي نرد جديد. / If an approved asset exists, outpaint, inpaint, cut out or upscale it instead of rolling a new image.

**متى:** تغيير النسبة 16:9→9:16، طبقات باراللاكس / re-aspecting, parallax layers

**كيف:** Local here: `rembg i in.png out.png` for cut-outs → parallax layers; reframing without generation = blurred-background pad in ffmpeg. External: Adobe image_generative_expand into tall (9:16/4:5) and wide (2:1/16:9) masters then crop each platform (preview 1:1, 4:5, wide first); Cloudinary URL effects e_background_removal, b_gen_fill, e_gen_replace, e_gen_remove, e_gen_background_replace (seed_), e_upscale (credit costs 230/120/100/75/50 tx); FLUX.2 Pro Outpaint; realesrgan-ncnn-vulkan ×4 (not installed).

**التثبيت:** pip install rembg

**الوسوم:** outpaint · inpaint · rembg · upscale · توسيع

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:rembg` ← python3 -c "import rembg" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/2306-generative-web-media/8854-prompt-to-asset-routing`
- `kosif-atlas/skills/103-adobe-for-creativity/232-adobe-create-social-variations/SKILL.md`
- `kosif-atlas/skills/1119-cloudinary/2560-cloudinary-transformations/references/ai-transformations.md`

#### 7. قدرات قريبة في العائلة

- `GEN-43` لقطات بمساحة فارغة للكتابة / AI plates that reserve typography space (key)
- `GEN-44` أيقونات شفافة بثيم وشرائط سبرايت ثابتة / Themed transparent icons & consistent sprite strips (key)
- `GEN-46` شجرة اختيار نموذج الصور والترخيص أولًا / Image-model routing tree (licence first) (documented)
- `GEN-47` وصفات ComfyUI: المُعيِّن والجدولة وقياس منحنيات الضوضاء / ComfyUI sampler/scheduler recipes & measured sigma curves (documented)

### `GEN-46` — شجرة اختيار نموذج الصور والترخيص أولًا / Image-model routing tree (licence first)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر المولد حسب الحاجة: نص مقروء، ثبات هوية، تعديل، متجهات، جمال أقصى، أو كمية رخيصة — بعد فحص الترخيص. / Pick the generator by need — legible text, set consistency, editing, vector, top aesthetics or cheap volume — after the licence check.

**متى:** قبل أول استدعاء مدفوع / before the first paid call

**كيف:** Text in image: Ideogram 3/4 → Gemini → GPT Image. Set consistency: Flux multi-reference, Nano Banana Pro, Recraft. Edit existing: Gemini, Flux Kontext, ChatGPT Images. Vector/SVG: Recraft V3/V4 (or draw it yourself). Max aesthetics: Flux 1.1 Pro, Midjourney v7 (manual). Volume: Flux Schnell, Gemini Flash, self-hosted SD. Never FLUX.1-dev on client work (non-commercial weights).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** routing · اختيار النموذج · Recraft · licence

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1446-marketing-skills/3504-image`
- `kosif-atlas/skills/2306-generative-web-media/8854-prompt-to-asset-routing`
- `kosif-atlas/skills/2976-pwdev-social-media/12588-image-gen`

#### 7. قدرات قريبة في العائلة

- `GEN-44` أيقونات شفافة بثيم وشرائط سبرايت ثابتة / Themed transparent icons & consistent sprite strips (key)
- `GEN-45` تعديل قبل إعادة التوليد: توسيع وترميم وقص وتكبير / Edit before regenerate: outpaint, inpaint, cut-out, upscale (install)
- `GEN-47` وصفات ComfyUI: المُعيِّن والجدولة وقياس منحنيات الضوضاء / ComfyUI sampler/scheduler recipes & measured sigma curves (documented)
- `GEN-48` LoRA وControlNet والترميم في ComfyUI / ComfyUI LoRA bands, ControlNet & inpainting (documented)

### `GEN-47` — وصفات ComfyUI: المُعيِّن والجدولة وقياس منحنيات الضوضاء / ComfyUI sampler/scheduler recipes & measured sigma curves

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لكل عائلة نماذج مُعيِّن وجدولة وخطوات وCFG تعمل، وادعاءات الجداول تُقاس لا تُصدّق. / Each model family has a working sampler, scheduler, steps and CFG; schedule claims are measured, not believed.

**متى:** عند بناء رسم ComfyUI على جهاز بمعالج رسوميات / building a ComfyUI graph on a GPU host

**كيف:** SD1.5/SDXL: dpmpp_2m + karras, 25 steps, cfg 7–8. Flux: euler + sgm_uniform/simple, ~20 steps, cfg 1–3.5. Krea: euler + simple, 20 steps (8 turbo), cfg 1. Denoise 1.0 txt2img, 0.3–0.7 img2img. Measured (high/mid/low of 20 steps): simple 3/8/9, beta57 3/6/11 (detail finishes), linear_quadratic 17/3/0 (layout exploration). No GPU and no ComfyUI in this container.

**المعاملات:** SDXL 25 steps cfg 7–8; Flux 20 steps cfg 1–3.5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ComfyUI · sampler · scheduler · sigma

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design`
- `kosif-atlas/skills/2142-comfyui-plugin/7648-comfy-corpus-validation`

#### 7. قدرات قريبة في العائلة

- `GEN-45` تعديل قبل إعادة التوليد: توسيع وترميم وقص وتكبير / Edit before regenerate: outpaint, inpaint, cut-out, upscale (install)
- `GEN-46` شجرة اختيار نموذج الصور والترخيص أولًا / Image-model routing tree (licence first) (documented)
- `GEN-48` LoRA وControlNet والترميم في ComfyUI / ComfyUI LoRA bands, ControlNet & inpainting (documented)
- `GEN-49` شجرة اختيار نموذج الفيديو ومسودة رخيصة ثم نهائي / Video-model routing tree & cheap draft → premium final (documented)

### `GEN-48` — LoRA وControlNet والترميم في ComfyUI / ComfyUI LoRA bands, ControlNet & inpainting

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قوة LoRA حسب نوعها، وتوجيه البنية بالحواف والعمق والوضعية، وترميم منطقة بقناع. / LoRA strength by kind, structure guidance from edges/depth/pose, and masked regional regeneration.

**متى:** ثبات شخصية أو تكوين على مولد محلي / character or layout control on a local model

**كيف:** LoraLoader between checkpoint and sampler: style 0.6–0.9, concept 0.4–0.6; honour trigger words. ControlNetApplyAdvanced: 0.3–0.5 loose, 0.5–0.8 balanced, 0.8–1.0 strict; start 0.0 / end 0.8 leaves detail free; stack OpenPose+Depth or Canny+Depth (preprocessors Canny, DepthAnything, DWPose, LineArt, Scribble, SoftEdge, Normal, SAM, Tile). Inpaint: white mask = regenerate; VAEEncode + SetLatentNoiseMask, denoise 0.6–0.85; RMBG/SAM nodes for cut-outs; outpaint by padding.

**المعاملات:** LoRA 0.4–0.9; ControlNet 0.3–1.0 end 0.8; denoise 0.6–0.85

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** LoRA · ControlNet · inpaint · ComfyUI

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design`
- `kosif-atlas/skills/1514-huggingface-skills/3937-huggingface-lora-space-builder`

#### 7. قدرات قريبة في العائلة

- `GEN-46` شجرة اختيار نموذج الصور والترخيص أولًا / Image-model routing tree (licence first) (documented)
- `GEN-47` وصفات ComfyUI: المُعيِّن والجدولة وقياس منحنيات الضوضاء / ComfyUI sampler/scheduler recipes & measured sigma curves (documented)
- `GEN-49` شجرة اختيار نموذج الفيديو ومسودة رخيصة ثم نهائي / Video-model routing tree & cheap draft → premium final (documented)
- `GEN-50` صورة مفتاحية أولًا ثم تحريكها / Keyframe-first image-to-video (documented)

### `GEN-49` — شجرة اختيار نموذج الفيديو ومسودة رخيصة ثم نهائي / Video-model routing tree & cheap draft → premium final

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر مولد الفيديو بما يهم: صوت متزامن، سعر الثانية، ثبات الشخصية، أوزان مفتوحة، أو صورة→فيديو؛ وارسم بالرخيص وأنهِ بالغالي مرة واحدة. / Pick the video model by what matters — synced audio, cost/second, character consistency, open weights, or image-to-video — and draft cheap, finish premium once.

**متى:** قبل أي توليد فيديو / before any video generation

**كيف:** Quality + audio: Veo 3, Sora 2. Cheap volume: Kling, Seedance. Character consistency: Hailuo/MiniMax, Seedance R2V with references. Self-hosted: Wan 2.x, HunyuanVideo, LTX. Storyboard-to-video: Runway, LTX Studio. Spoken multi-segment UGC: Seedance 2.0 R2V. Drafts: Flux Schnell / Gemini Flash 512 stills, Kling standard, Seedance 480p; finals: Veo/Runway, Kling professional, 1080p. Image-to-video from an approved frame saves credits.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** routing · draft · final · اختيار نموذج الفيديو

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1446-marketing-skills/3531-video`
- `kosif-atlas/skills/259-quickdesign/865-quickdesign`
- `kosif-atlas/skills/2306-generative-web-media/8854-prompt-to-asset-routing`

#### 7. قدرات قريبة في العائلة

- `GEN-47` وصفات ComfyUI: المُعيِّن والجدولة وقياس منحنيات الضوضاء / ComfyUI sampler/scheduler recipes & measured sigma curves (documented)
- `GEN-48` LoRA وControlNet والترميم في ComfyUI / ComfyUI LoRA bands, ControlNet & inpainting (documented)
- `GEN-50` صورة مفتاحية أولًا ثم تحريكها / Keyframe-first image-to-video (documented)
- `GEN-51` Seedance 2.5 عبر Higgsfield (محروس ومدفوع) / Seedance 2.5 text/image-to-video via Higgsfield (guarded) (key)

### `GEN-50` — صورة مفتاحية أولًا ثم تحريكها / Keyframe-first image-to-video

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اعتمد إطارًا ثابتًا أولًا ثم حرّكه ببرومبت حركة فقط؛ مقطع اختبار واحد قبل أي سلسلة. / Approve a still first, then animate it with a motion-only prompt; one test clip before any series.

**متى:** كل لقطة مولدة مهمة / every important generated shot

**كيف:** image-prompt-forge → curate → I2V with --dur 5 and a vertical ratio like 720:1280. Motion prompt shape: `[subject action], [camera move: static/pan/dolly/orbital], [pace], [duration]` — do not re-describe what the image already shows. Price clips separately from stills; redo off-style keyframes (cents) before clips (dollars).

**المعاملات:** test clip 5 s; 720:1280

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** I2V · keyframe · image to video · إطار مفتاحي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/video-prompt-director/SKILL.md:24`
- `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen`
- `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### 7. قدرات قريبة في العائلة

- `GEN-48` LoRA وControlNet والترميم في ComfyUI / ComfyUI LoRA bands, ControlNet & inpainting (documented)
- `GEN-49` شجرة اختيار نموذج الفيديو ومسودة رخيصة ثم نهائي / Video-model routing tree & cheap draft → premium final (documented)
- `GEN-51` Seedance 2.5 عبر Higgsfield (محروس ومدفوع) / Seedance 2.5 text/image-to-video via Higgsfield (guarded) (key)
- `GEN-52` حلقات فيديو Kling للهوية وواجهة Kling / Kling text/image-to-video API (+ real brand loops) (key)

### `GEN-51` — Seedance 2.5 عبر Higgsfield (محروس ومدفوع) / Seedance 2.5 text/image-to-video via Higgsfield (guarded)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Higgsfield SDK / service terms; billable |

**ما هي:** استدعاء من الخادم يرسل مهمة فيديو ولا يعلن النجاح إلا لنتيجة مكتملة برابط صالح؛ الفشل والإشراف والإلغاء ترجع غير صفر. / A server-side call that submits a video job and reports success only for a completed result with a valid URL; failed, moderated or cancelled return non-zero.

**متى:** لقطة إدراج مولدة (علم، مقدمة، حلقة هوية) بإذن المالك وتكلفته / an AI insert shot with the owner's approval and budget

**كيف:** `higgsfield_client.subscribe('bytedance/seedance-2.5/text-to-video', arguments={prompt, duration, resolution, aspect_ratio, generate_audio}, on_enqueue, on_queue_update)`; status from the last Status class (Queued, InProgress, Completed, Failed, NSFW, Cancelled); offline tests `python test_higgsfield.py`. Real outputs already in the owner repos: earth-intro (Seedance 2.5 I2V, 1280×720, 24 fps, 5.056 s, AAC 32 kHz) and the flag slow-motion insert (6 s, 1080p, 9:16, no audio: low angle, golden sunset over desert and canal, 35 mm grain, warm amber, backlit dust, no text, no people).

**المعاملات:** 5 s 720p 16:9 demo; 6 s 1080p 9:16 reel shot

**التثبيت:** pip install higgsfield-client python-dotenv

**الوسوم:** Seedance · Higgsfield · text to video · billable

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:higgsfield` ← python3 -c "import higgsfield" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-studio/main.py:20`
- `kosif-studio/HIGGSFIELD_SETUP.md`
- `kosif-one/projects/higgsfield/gen_reel_shot.py:14-23`
- `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.mp4`

#### 7. قدرات قريبة في العائلة

- `GEN-49` شجرة اختيار نموذج الفيديو ومسودة رخيصة ثم نهائي / Video-model routing tree & cheap draft → premium final (documented)
- `GEN-50` صورة مفتاحية أولًا ثم تحريكها / Keyframe-first image-to-video (documented)
- `GEN-52` حلقات فيديو Kling للهوية وواجهة Kling / Kling text/image-to-video API (+ real brand loops) (key)
- `GEN-53` فرشاة الحركة والقناع الثابت (سينماغراف) / Kling motion brush & static mask (cinemagraph) (key)

### `GEN-52` — حلقات فيديو Kling للهوية وواجهة Kling / Kling text/image-to-video API (+ real brand loops)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** واجهة Kling REST لإنشاء مهام فيديو وانتظارها؛ والمالك يملك حلقتي هوية صامتتين 5 ث صُنعتا بها. / Kling's REST API creates video tasks you poll; the owner already has two silent 5 s brand loops made with it.

**متى:** B-roll سينمائي رخيص، حلقات خلفية، دوران منتج / cheap cinematic b-roll, background loops, product turns

**كيف:** `POST https://api.klingai.com/v1/videos/text2video` with a Bearer JWT (HS256 from access/secret key, exp 30 min, regenerate per request); body model_name (kling-v2-6, v2-5-turbo, v2-master, v1-6), prompt ≤2500 chars, negative_prompt, duration as STRING '5'\|'10', aspect_ratio, mode standard\|professional, cfg_scale 0–1, callback_url; poll until succeed/failed. image2video adds image + image_tail XOR camera_control XOR masks. Kling 3 via fal: 3–15 s, explicit camera verbs. Brand loops: Kling 3.0 Standard T2V 5 s → mirrored, graded, H.264 1280 crf 27 faststart (measured 1280×720, 24 fps, 5.04 s, 2.0 / 0.94 Mbps).

**المعاملات:** duration '5'\|'10'; v2.6 1080p 30–48 fps; 8 ratios

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Kling · API · brand loop · b-roll

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1874-klingai-pack/6089-klingai-text-to-video`
- `kosif-atlas/skills/1874-klingai-pack/6075-klingai-image-to-video`
- `kosif-earth-ci-fork/ui/art/brand/door.mp4`
- `kosif-earth-ci-fork/ui/art/brand/dashboard.mp4`

#### 7. قدرات قريبة في العائلة

- `GEN-50` صورة مفتاحية أولًا ثم تحريكها / Keyframe-first image-to-video (documented)
- `GEN-51` Seedance 2.5 عبر Higgsfield (محروس ومدفوع) / Seedance 2.5 text/image-to-video via Higgsfield (guarded) (key)
- `GEN-53` فرشاة الحركة والقناع الثابت (سينماغراف) / Kling motion brush & static mask (cinemagraph) (key)
- `GEN-54` تمديد فيديو Kling بالتسلسل ونظام الرصيد / Kling extension chain & credit model (key)

### `GEN-53` — فرشاة الحركة والقناع الثابت (سينماغراف) / Kling motion brush & static mask (cinemagraph)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حرّك مناطق مختارة من صورة على مسارات مرسومة وأبقِ الباقي متجمدًا. / Animate selected regions of a still along drawn paths while the rest stays frozen.

**متى:** سينماغراف: دخان، ماء، قماش يتحرك في صورة ثابتة / cinemagraphs

**كيف:** image2video with dynamic_masks [{mask: white-region PNG, trajectories:[{x,y,t} normalised 0–1]}] — ≤6 paths on v2.6 — plus static_mask for regions that must not move. Cannot combine with camera_control or image_tail.

**المعاملات:** ≤6 trajectories; coords 0–1

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** motion brush · cinemagraph · سينماغراف

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1874-klingai-pack/6075-klingai-image-to-video`
- `kosif-atlas/skills/1874-klingai-pack/6078-klingai-known-pitfalls`

#### 7. قدرات قريبة في العائلة

- `GEN-51` Seedance 2.5 عبر Higgsfield (محروس ومدفوع) / Seedance 2.5 text/image-to-video via Higgsfield (guarded) (key)
- `GEN-52` حلقات فيديو Kling للهوية وواجهة Kling / Kling text/image-to-video API (+ real brand loops) (key)
- `GEN-54` تمديد فيديو Kling بالتسلسل ونظام الرصيد / Kling extension chain & credit model (key)
- `GEN-55` واجهة Runway حسب النموذج والتزامن / Runway task API & concurrency model (key)

### `GEN-54` — تمديد فيديو Kling بالتسلسل ونظام الرصيد / Kling extension chain & credit model

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مدّ مقطعًا منتهيًا بخطوات 5 ث، كل خطوة تكمل السابقة؛ وارسم بوضع standard وأنهِ بـ professional. / Lengthen a finished clip in 5 s steps; draft in standard mode and finish in professional.

**متى:** مشهد أطول من 10 ث بلا قطع / a shot longer than 10 s without a cut

**كيف:** `POST /v1/videos/video-extend {task_id, prompt (next story beat), duration '5', mode}`; the new task_id feeds the next step. Credits: standard 10/20 for 5/10 s, professional 35/70, with audio 50/100 and 100/200; API ≈ $0.07–0.14/s. Generate 5 s and extend rather than 10 s; add audio in post. Extras: /v1/videos/effects (hug, kiss, heart, expand, squish), /v1/images/kolors (≤2048², 1 credit) → image2video as a cheap style-first route, /v1/videos/lip-sync.

**المعاملات:** +5 s/step; std 10/20, pro 35/70; audio ×5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** extend · credits · Kling · تمديد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1874-klingai-pack/6092-klingai-video-extension`
- `kosif-atlas/skills/1874-klingai-pack/6081-klingai-pricing-basics`
- `kosif-atlas/skills/1874-klingai-pack/6079-klingai-model-catalog`

#### 7. قدرات قريبة في العائلة

- `GEN-52` حلقات فيديو Kling للهوية وواجهة Kling / Kling text/image-to-video API (+ real brand loops) (key)
- `GEN-53` فرشاة الحركة والقناع الثابت (سينماغراف) / Kling motion brush & static mask (cinemagraph) (key)
- `GEN-55` واجهة Runway حسب النموذج والتزامن / Runway task API & concurrency model (key)
- `GEN-56` قواعد المراجع في Seedance 2.0 R2V / Seedance 2.0 reference-to-video grammar (key)

### `GEN-55` — واجهة Runway حسب النموذج والتزامن / Runway task API & concurrency model

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أجسام طلب Runway تختلف حسب النموذج وكل توليد مهمة غير متزامنة، والسعة تحكمها حدود التزامن لا عدد الطلبات بالدقيقة. / Runway bodies differ per model and every generation is an async task; capacity is per-model concurrency, not requests per minute.

**متى:** لقطات من لوحة قصة بإطار معتمد / storyboard shots from approved frames

**كيف:** gen4.5 takes text or image, gen4_turbo needs an image, gen3a_turbo legacy. Server-side secret + X-Runway-Version header; submit, store the task id at once, poll with the SDK wait helper; states PENDING, RUNNING, THROTTLED (queued, not failed), SUCCEEDED, FAILED, CANCELLED. Local media → ephemeral upload → runway:// URI valid 24 h. Model Router dryRun estimates cost. Per-model semaphore below tier (5 concurrent → admit 4, reserve 1); never resubmit after a disconnect — resume from the stored id; pause on 429 daily-quota.

**المعاملات:** runway:// 24 h; 5 s smoke test

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Runway · async · concurrency

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1900-runway-pack/6659-runway-core-workflow-a`
- `kosif-atlas/skills/1900-runway-pack/6669-runway-rate-limits`
- `kosif-atlas/skills/1900-runway-pack/6661-runway-cost-tuning`

#### 7. قدرات قريبة في العائلة

- `GEN-53` فرشاة الحركة والقناع الثابت (سينماغراف) / Kling motion brush & static mask (cinemagraph) (key)
- `GEN-54` تمديد فيديو Kling بالتسلسل ونظام الرصيد / Kling extension chain & credit model (key)
- `GEN-56` قواعد المراجع في Seedance 2.0 R2V / Seedance 2.0 reference-to-video grammar (key)
- `GEN-57` لقطة أداء مولدة متزامنة مع مقطع الأغنية / Reference-to-video performance shot synced to a song slice (key)

### `GEN-56` — قواعد المراجع في Seedance 2.0 R2V / Seedance 2.0 reference-to-video grammar

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** Seedance يقرأ مراجع موسومة (@Image1 و@Audio1 و@Video1) فتأتي الهوية والملابس والمكان من الصور، والبرومبت يضيف الجديد فقط. / Seedance reads labelled references (@Image1, @Audio1, @Video1): identity, wardrobe and setting come from images, the prompt only adds what is new.

**متى:** شخصية ثابتة عبر لقطات، إعلان UGC ناطق / a consistent character across shots, spoken UGC

**كيف:** Pass each photo as a separate reference in order; prompt like '@Image2 in @Image3, holds @Image1 toward camera. The person says: "…"'; never re-describe what references show (it causes drift). Integer duration 4–15 s; 480p/720p/1080p; 9:16, 16:9, 1:1, 4:3, 3:4, 21:9; native audio on by default (turn off when your own track will play). Hosts: fal, QuickDesign, Higgsfield.

**المعاملات:** 4–15 s integer; ≈40 credits/s at 1080p

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Seedance · R2V · reference · @Image1

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:higgsfield` ← python3 -c "import higgsfield" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/259-quickdesign/865-quickdesign`
- `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### 7. قدرات قريبة في العائلة

- `GEN-54` تمديد فيديو Kling بالتسلسل ونظام الرصيد / Kling extension chain & credit model (key)
- `GEN-55` واجهة Runway حسب النموذج والتزامن / Runway task API & concurrency model (key)
- `GEN-57` لقطة أداء مولدة متزامنة مع مقطع الأغنية / Reference-to-video performance shot synced to a song slice (key)
- `GEN-58` ثبات الصوت عبر مرجع صوتي / Voice continuity via reference audio (key)

### `GEN-57` — لقطة أداء مولدة متزامنة مع مقطع الأغنية / Reference-to-video performance shot synced to a song slice

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 (skill) |

**ما هي:** شخصية تغني مقطعًا دقيقًا من الأغنية: النموذج يستلم ورقة الأسلوب وورقة الشخصية وشريحة الصوت فيقع الفم على الموسيقى بالبناء. / A character sings an exact slice of the song: style sheet, character sheet and the audio slice go in, so mouth and hits land by construction.

**متى:** فيديو موسيقي أو قصيدة مغناة / a music video or sung poem

**كيف:** Slice the song to the shot with ffmpeg (48 kHz PCM, whole-second duration); Seedance 2.5 R2V on fal; prompt: style of @Image1, the singer from @Image2 sings @Audio1 with precise lip sync, mouth closed when @Audio1 is silent, static camera, no text, one continuous shot. 480p/720p when a draw-over follows (1080p ≈ 2× cost). Picture-only shots use I2V with generate_audio false. Your master audio stays untouched; the slice is only a reference.

**المعاملات:** 48 kHz slice; integer s; 480–720p

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lip sync · music video · أداء · song slice

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/1511-homie/3903-video`
- `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### 7. قدرات قريبة في العائلة

- `GEN-55` واجهة Runway حسب النموذج والتزامن / Runway task API & concurrency model (key)
- `GEN-56` قواعد المراجع في Seedance 2.0 R2V / Seedance 2.0 reference-to-video grammar (key)
- `GEN-58` ثبات الصوت عبر مرجع صوتي / Voice continuity via reference audio (key)
- `GEN-59` Veo عبر Gemini وقيود Sora 2 / Veo via Gemini & Sora 2 constraints (key)

### `GEN-58` — ثبات الصوت عبر مرجع صوتي / Voice continuity via reference audio

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ثبّت صوتًا واحدًا عبر مقاطع مولدة بإعطاء صوت المقطع الأول كمرجع للبقية. / Lock one voice across generated segments by feeding segment 1's own audio as the reference for the rest.

**متى:** إعلان أو شرح متعدد المقاطع بشخصية ناطقة / multi-segment spoken pieces

**كيف:** Render segment 1 → `ffmpeg -i s1.mp4 -vn -acodec libmp3lame -q:a 2 ref.mp3` → pass as --reference-audio (≤3 clips, 2–15 s each, ≤15 MB) to segments 2..N → concat with `-c copy`. Avoid clone + TTS + lipsync chains (length drift, ~2× cost).

**المعاملات:** ref 2–15 s, ≤3 clips, ≤15 MB

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** voice continuity · reference audio · ثبات الصوت

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/259-quickdesign/865-quickdesign`

#### 7. قدرات قريبة في العائلة

- `GEN-56` قواعد المراجع في Seedance 2.0 R2V / Seedance 2.0 reference-to-video grammar (key)
- `GEN-57` لقطة أداء مولدة متزامنة مع مقطع الأغنية / Reference-to-video performance shot synced to a song slice (key)
- `GEN-59` Veo عبر Gemini وقيود Sora 2 / Veo via Gemini & Sora 2 constraints (key)
- `GEN-60` منصات التجميع: fal وTogether وWaveSpeed وHF Spaces وVertex / Aggregator hubs: fal, Together, WaveSpeed, HF Spaces, Vertex (key)

### `GEN-59` — Veo عبر Gemini وقيود Sora 2 / Veo via Gemini & Sora 2 constraints

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** Veo يولّد B-roll ولقطات بطولة وخلفيات حلقية عبر عملية طويلة تُستطلع؛ Sora 2 لقطة سينمائية واحدة بمدد ثابتة. / Veo makes B-roll, hero shots and loopable backgrounds via a long-running operation you poll; Sora 2 gives one cinematic shot at fixed durations.

**متى:** B-roll بصوت أصلي، خلفية حلقية هادئة / b-roll with native audio, calm loop backgrounds

**كيف:** Veo: `POST models/{veo}:predictLongRunning {instances:[{prompt}], parameters:{aspectRatio: '9:16'\|'16:9'}}`, poll every 8 s, abort after 8 min or 6 network failures; models veo-3.1-generate-preview, -fast-, -lite-; background mode appends 'slow, calm, loopable, no people, no text'; Veo prose + an 'Audio:' line, 4/6/8 s, ≤2.5 Arabic words/s of speech. Sora 2: 4, 8 or 12 s only, prompt ≤4000 chars, describe subject/setting fully (the image is a hint), fresh voice per call; Together exposes sora-2 / sora-2-pro at 8 s 1280×720.

**المعاملات:** poll 8 s; timeout 8 min; Veo 4/6/8 s; Sora 4/8/12 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Veo · Sora · Gemini · loop background

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `app/public/js/00_editor.js:1935`
- `app/public/js/00_editor.js:2097`
- `kosif-atlas/skills/259-quickdesign/865-quickdesign`
- `kosif-atlas/skills/3214-togetherai-skills/13597-together-video`

#### 7. قدرات قريبة في العائلة

- `GEN-57` لقطة أداء مولدة متزامنة مع مقطع الأغنية / Reference-to-video performance shot synced to a song slice (key)
- `GEN-58` ثبات الصوت عبر مرجع صوتي / Voice continuity via reference audio (key)
- `GEN-60` منصات التجميع: fal وTogether وWaveSpeed وHF Spaces وVertex / Aggregator hubs: fal, Together, WaveSpeed, HF Spaces, Vertex (key)
- `GEN-61` خياطة الإطارات وسلاسل البداية/النهاية / Frame stitching & start/end-image chains for long AI video (key)

### `GEN-60` — منصات التجميع: fal وTogether وWaveSpeed وHF Spaces وVertex / Aggregator hubs: fal, Together, WaveSpeed, HF Spaces, Vertex

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقطة واحدة لمئات النماذج مع تسعير وتخزين وكتالوج فيديو موحد. / One endpoint for hundreds of models with pricing, storage and a unified video catalogue.

**متى:** حين تحتاج نموذجًا معينًا بلا حساب منفصل / when you need a model without a separate account

**كيف:** fal: FAL_KEY (`Authorization: Key …`), queue https://queue.fal.run, price via https://api.fal.ai/v1/models/pricing?endpoint_id=…, upload `@file:` inputs first, hosted MCP search_models / get_model_schema / get_pricing. Together video: seconds, fps 15–60 (24), steps 10–50, guidance 6–10 (avoid >12), negative_prompt, frame_images [{input_image, frame:'first'\|'last'}]; Veo 3.0 8 s up to 1920×1080, Hailuo 02 10 s 25 fps. WaveSpeed CLI: `wavespeed models --type …` → `run <model> -h` → `--json`. HF MCP: space_search → dynamic_space(view_parameters) → invoke (bg removal, Whisper, FLUX.1-schnell). Vertex: Gemini video understanding (≈2 h default, 6 h low-res), Imagen 4, Lyria. Download results at once — signed URLs expire.

**المعاملات:** fps 15–60; steps 10–50; guidance 6–10

**التثبيت:** pip install fal-client together

**الوسوم:** fal · Together · WaveSpeed · Hugging Face · Vertex

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:faster-whisper` ← python3 -c "import faster-whisper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1511-homie/3903-video`
- `kosif-atlas/skills/3214-togetherai-skills/13597-together-video`
- `kosif-atlas/skills/3396-wavespeed-cli/13932-wavespeed-cli/SKILL.md`
- `kosif-atlas/skills/1514-huggingface-skills/3922-hf-mcp/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `GEN-58` ثبات الصوت عبر مرجع صوتي / Voice continuity via reference audio (key)
- `GEN-59` Veo عبر Gemini وقيود Sora 2 / Veo via Gemini & Sora 2 constraints (key)
- `GEN-61` خياطة الإطارات وسلاسل البداية/النهاية / Frame stitching & start/end-image chains for long AI video (key)
- `GEN-62` فيديو مفتوح الأوزان: Wan 2.x وLTX وAnimateDiff / Open-weights video: Wan 2.x, LTX-Video, AnimateDiff (documented)

### `GEN-61` — خياطة الإطارات وسلاسل البداية/النهاية / Frame stitching & start/end-image chains for long AI video

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | scroll-world MIT; mcp-higgsfield-landing has no licence — read only, never copy its prompts |

**ما هي:** بناء فيديو مولد طويل من مقاطع قصيرة يبدأ كل منها من آخر إطار في السابق، أو بنماذج تقبل إطار بداية ونهاية. / Build long generated sequences from short chunks each starting on the previous last frame, or with models that accept start and end images.

**متى:** مشهد مولد متصل أطول من حد المنصة / a continuous generated sequence beyond the platform limit

**كيف:** Chunks ~5 s (Veo 4/6/8): define start state, action, end state, camera move; last frame of n → first frame of n+1 (`ffmpeg -sseof -0.05 -i n.mp4 -frames:v 1 last.png`); repeat locks, light direction and Kelvin; keep the 180° rule, same fps/aspect; cut on motion or hard match; compare adjacent first/last frames (brightness, CCT, framing). Seam-holding models: seedance_2_0 (1080p, dive 8 s, connectors 5 s), kling3_0 (720p, --sound off), seedance_2_0_mini draft 720p; N=6 1080p chain ≈ $27. Photo-to-photo POV walk: real venue photos as first/last frames, MiniMax H3, 8 s 2K → 1080p, no cuts/fades (6 clips ≈ $5).

**المعاملات:** ~5 s chunks; N=6 ≈ $27

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** frame stitching · start frame · end frame · خياطة · POV walk

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/continuity-protocols.md`
- `100-superskills/skills/kosif-montage-motion/references/continuity-protocols.md`
- `kosif-one/vendor/scroll-world/skills/scroll-world/references/pipeline.md`
- `kosif-one/vendor/mcp-higgsfield-landing/PROMPTS.md:128`

#### 7. قدرات قريبة في العائلة

- `GEN-59` Veo عبر Gemini وقيود Sora 2 / Veo via Gemini & Sora 2 constraints (key)
- `GEN-60` منصات التجميع: fal وTogether وWaveSpeed وHF Spaces وVertex / Aggregator hubs: fal, Together, WaveSpeed, HF Spaces, Vertex (key)
- `GEN-62` فيديو مفتوح الأوزان: Wan 2.x وLTX وAnimateDiff / Open-weights video: Wan 2.x, LTX-Video, AnimateDiff (documented)
- `GEN-63` وصلة Higgsfield كمسار برومبت فقط / Higgsfield / paid clip route as prompt-only deliverable (documented)

### `GEN-62` — فيديو مفتوح الأوزان: Wan 2.x وLTX وAnimateDiff / Open-weights video: Wan 2.x, LTX-Video, AnimateDiff

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نماذج فيديو تعمل ذاتيًا على جهاز بمعالج رسوميات. / Self-hosted video models for a GPU host.

**متى:** عندما يملك المستخدم GPU ويريد بلا اشتراك / when the user has a GPU and wants no subscription

**كيف:** Wan (ComfyUI): WanVideoModelLoader → TextEncode/ImageEncode → Sampler → VAEDecode → VHS_VideoCombine; 33–81 frames, 832×480, 20–30 steps, cfg 5–7, shift 5–8, brief negatives. LTX (diffusers): LTXPipeline / LTXImageToVideoPipeline / LTXConditionPipeline (keyframes), 30–50 steps (8–12 distilled), 121 frames @24 fps, enable_vae_tiling >768 px. AnimateDiff (SD1.5): context_length 16, overlap 4, mm_sd_v15_v2, 16 frames @8 fps = 2 s loops. This container has no GPU — diffusers installs, but do not promise a render here.

**المعاملات:** Wan 832×480 33–81 f; LTX 121 f @24; AnimateDiff 16 f @8 fps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Wan · LTX · AnimateDiff · open weights · GPU

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:torch` ← python3 -c "import torch" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design`
- `kosif-atlas/skills/1514-huggingface-skills/3937-huggingface-lora-space-builder`
- `kosif-atlas/skills/3214-togetherai-skills/13597-together-video`

#### 7. قدرات قريبة في العائلة

- `GEN-60` منصات التجميع: fal وTogether وWaveSpeed وHF Spaces وVertex / Aggregator hubs: fal, Together, WaveSpeed, HF Spaces, Vertex (key)
- `GEN-61` خياطة الإطارات وسلاسل البداية/النهاية / Frame stitching & start/end-image chains for long AI video (key)
- `GEN-63` وصلة Higgsfield كمسار برومبت فقط / Higgsfield / paid clip route as prompt-only deliverable (documented)
- `GEN-64` توليد الموسيقى: Lyria وMusicGen / Music generation: Lyria & MusicGen (key)

### `GEN-63` — وصلة Higgsfield كمسار برومبت فقط / Higgsfield / paid clip route as prompt-only deliverable

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بدون مفتاح وإذن تكلفة، المُسلَّم هو لوحة قصة وبرومبتات يشغلها المستخدم بنفسه — موسومة «لم يُولَّد». / Without a key and cost approval the deliverable is a storyboard plus prompts the user runs — labelled 'not generated'.

**متى:** كل طلب توليد فيديو في هذه الحاوية / every video-generation request in this container

**كيف:** Write shot cards + platform prompts (forges above), mark each 'prompt only — none has been rendered'; Fastify keeps HF_CREDENTIALS as a placeholder and requires explicit cost approval; the linked landing example has no verified licence and must not be copied.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** prompt only · storyboard · honesty

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:higgsfield` ← python3 -c "import higgsfield" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-63` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/docs/ENGINE_ROUTER.md:6`
- `fastify-motion-bro/docs/SOURCE_AUDIT.md:7`
- `kosif-atlas/skills/2976-pwdev-social-media/12594-video-gen`

#### 7. قدرات قريبة في العائلة

- `GEN-61` خياطة الإطارات وسلاسل البداية/النهاية / Frame stitching & start/end-image chains for long AI video (key)
- `GEN-62` فيديو مفتوح الأوزان: Wan 2.x وLTX وAnimateDiff / Open-weights video: Wan 2.x, LTX-Video, AnimateDiff (documented)
- `GEN-64` توليد الموسيقى: Lyria وMusicGen / Music generation: Lyria & MusicGen (key)
- `GEN-65` كلمات أغنية وموجز Suno/Udio / Song lyrics + Suno/Udio brief (documented)

### `GEN-64` — توليد الموسيقى: Lyria وMusicGen / Music generation: Lyria & MusicGen

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0; Lyria / MusicGen output per provider/model terms |

**ما هي:** مقطع موسيقي أو أغنية بـ Gemini Lyria، أو MusicGen-small كبذرة ≤30 ث تُدار بتلاشٍ متقاطع، مع BPM حسب القطاع. / A music clip or song with Gemini Lyria, or MusicGen-small as a ≤30 s seed crossfade-looped, with BPM by industry.

**متى:** حين لا توجد موسيقى من المستخدم ولا مكتبة مرخصة / when the user gave no music and no licensed library fits

**كيف:** Basma: `POST v1beta/interactions` model lyria-3-clip-preview (30 s) or lyria-3.5 (full song); detects free-tier 'limit: 0' and falls back to the local composer. HyperFrames: `resolve --type bgm --intent …` → catalogue first, then `scripts/lyria-recipe.py --output --duration --prompt [--bpm]` detached + `wait-bgm.mjs`. BPM by industry: crypto 100, finance 92, creative 115, SaaS 108; feature cascade +10, demo loop −8. Then duck under voice and normalise (BEAT/SYNC families).

**المعاملات:** BPM 92–115; seed ≤28–30 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Lyria · MusicGen · موسيقى · BGM

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-64` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `app/public/js/10_studio.js:2554`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/references/bgm.md`
- `kosif-one/vendor/hyperframes/skills/media-use/audio/scripts/lyria-recipe.py`

#### 7. قدرات قريبة في العائلة

- `GEN-62` فيديو مفتوح الأوزان: Wan 2.x وLTX وAnimateDiff / Open-weights video: Wan 2.x, LTX-Video, AnimateDiff (documented)
- `GEN-63` وصلة Higgsfield كمسار برومبت فقط / Higgsfield / paid clip route as prompt-only deliverable (documented)
- `GEN-65` كلمات أغنية وموجز Suno/Udio / Song lyrics + Suno/Udio brief (documented)
- `GEN-66` أمر واحد لجلب أي وسائط / Media resolve: one verb for any asset (key)

### `GEN-65` — كلمات أغنية وموجز Suno/Udio / Song lyrics + Suno/Udio brief

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بنية (كوبليه/لازمة/جسر) بتوقيتات، وزن وقافية عربية، مقام، BPM، آلات، صوت، مزاج — بلا أسماء فنانين أحياء. / Structure with timings, Arabic metre and rhyme, maqam, BPM, instruments, vocal, mood — no living artist names.

**متى:** أغنية لريل أو إعلان / a song for a reel or ad

**كيف:** Write lyrics.md + music-brief.md; include a short reel cut (hook + chorus); the user runs Suno/Udio and returns the track, which you then treat as untouched master audio.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Suno · Udio · أغنية · lyrics · maqam

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-65` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `100-superskills/skills/music-song-brief/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `GEN-63` وصلة Higgsfield كمسار برومبت فقط / Higgsfield / paid clip route as prompt-only deliverable (documented)
- `GEN-64` توليد الموسيقى: Lyria وMusicGen / Music generation: Lyria & MusicGen (key)
- `GEN-66` أمر واحد لجلب أي وسائط / Media resolve: one verb for any asset (key)
- `GEN-67` مقدم افتراضي ودبلجة وترجمة فيديو وتكبير / Avatar presenter, dub, video translate & upscale (key)

### `GEN-66` — أمر واحد لجلب أي وسائط / Media resolve: one verb for any asset

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 |

**ما هي:** حلّ موسيقى أو مؤثر أو صورة أو أيقونة أو شعار أو صوت أو LUT إلى ملف محلي مجمّد وسجل، بسطر مخرجات واحد. / Resolve bgm, sfx, image, icon, logo, voice, grade or LUT into a frozen local file plus ledger record, with one output line.

**متى:** جلب الأصول في مشروع HyperFrames / fetching assets in a HyperFrames project

**كيف:** `npx hyperframes media-use resolve --type <bgm\|sfx\|image\|icon\|logo\|voice\|grade\|lut\|video> --intent '<description>' --project <dir> [--candidates] [--from file --adopt] [--json]`; catalogues 10k+ tracks, 75k+ vectors, 19 bundled SFX (catalogue access goes through the vendor service); on a catalogue miss images fall back to local FLUX via mflux (Apple Silicon) or Codex image_gen.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** media resolve · HyperFrames · assets · ledger

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-66` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/media-use/SKILL.md`
- `kosif-one/vendor/hyperframes/skills/media-use/references/resolve.md`
- `kosif-one/vendor/hyperframes/skills/media-use/references/setup-providers.md`

#### 7. قدرات قريبة في العائلة

- `GEN-64` توليد الموسيقى: Lyria وMusicGen / Music generation: Lyria & MusicGen (key)
- `GEN-65` كلمات أغنية وموجز Suno/Udio / Song lyrics + Suno/Udio brief (documented)
- `GEN-67` مقدم افتراضي ودبلجة وترجمة فيديو وتكبير / Avatar presenter, dub, video translate & upscale (key)
- `GEN-68` توليد مجسمات ثلاثية بالذكاء / Text/image → 3D model (Meshy, Tripo, Rodin, TRELLIS) (key)

### `GEN-67` — مقدم افتراضي ودبلجة وترجمة فيديو وتكبير / Avatar presenter, dub, video translate & upscale

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** فيديو مقدم افتراضي من سكربت، صورة→مقطع ناطق، دبلجة للغة أخرى، وتكبير صور ×4. / Avatar video from a script, photo → talking clip, dubbing, and ×4 image upscale.

**متى:** متحدث بلا تصوير أو نسخة بلغة ثانية / a presenter without a shoot, or a second-language version

**كيف:** HeyGen CLI: `heygen video create`, `heygen lipsync`, `heygen video-translate`; hosted HyperFrames MCP connector renders without the local CLI; Adobe Quick Cut picks highlights into 15/45/90 s reels (run ×3, user picks). Upscale `realesrgan-ncnn-vulkan -i in.png -o out.png -s 4` (not installed). Always disclose synthetic humans/voices; never a real person without consent.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** avatar · HeyGen · dub · lipsync · upscale · مقدم افتراضي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-67` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/media-use/references/operations.md`
- `kosif-one/vendor/hyperframes/docs/guides/mcp.mdx`
- `kosif-atlas/skills/103-adobe-for-creativity/236-adobe-edit-quick-cut/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `GEN-65` كلمات أغنية وموجز Suno/Udio / Song lyrics + Suno/Udio brief (documented)
- `GEN-66` أمر واحد لجلب أي وسائط / Media resolve: one verb for any asset (key)
- `GEN-68` توليد مجسمات ثلاثية بالذكاء / Text/image → 3D model (Meshy, Tripo, Rodin, TRELLIS) (key)
- `GEN-69` توجيه مزودي الإبداع وشبكة الموصلات / Creative provider routing & connector mesh (key)

### `GEN-68` — توليد مجسمات ثلاثية بالذكاء / Text/image → 3D model (Meshy, Tripo, Rodin, TRELLIS)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نص أو صورة إلى ملف GLB لاستخدامه في مشهد Three.js. / Text or image to a GLB for a Three.js scene.

**متى:** مجسم منتج أو شخصية لا يوجد له نموذج / a product or prop with no model

**كيف:** External paid APIs or MCPs (Meshy MCP, Tripo MCP); check commercial licence; then load the GLB in the 3D family's pipeline (three / @react-three/fiber are npm-installable here).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** 3D · GLB · Meshy · Tripo · مجسم

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `npm:react` ← npm ls react أو وجود node_modules/react
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-68` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2306-generative-web-media/8854-prompt-to-asset-routing`
- `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`
- `kosif-studio/motion/references/tools-catalog-2.md`

#### 7. قدرات قريبة في العائلة

- `GEN-66` أمر واحد لجلب أي وسائط / Media resolve: one verb for any asset (key)
- `GEN-67` مقدم افتراضي ودبلجة وترجمة فيديو وتكبير / Avatar presenter, dub, video translate & upscale (key)
- `GEN-69` توجيه مزودي الإبداع وشبكة الموصلات / Creative provider routing & connector mesh (key)
- `GEN-70` خوادم المالك: KOSIF Think وJev والمنصة الخاصة / Owner MCP runtimes: KOSIF Think, Jev arbiter, private Workbench (key)

### `GEN-69` — توجيه مزودي الإبداع وشبكة الموصلات / Creative provider routing & connector mesh

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جدول توجيه يكشف نية صورة/فيديو/تصميم/عرض بالعربية أو الإنجليزية ويرتب الخدمات المتصلة حسب الأولوية والتكلفة. / A routing table that detects image/video/design/presentation intent in Arabic or English and ranks connected services by priority and cost.

**متى:** حين تكون موصلات المالك متاحة في الجلسة / when the owner's connectors are live in the session

**كيف:** routeLanes(task) regexes: image /(image\|photo\|poster\|graphic\|illustration\|صورة\|بوستر\|رسم\|جرافيك\|تصوير)/, video /(video\|animation\|avatar\|motion\|reel\|فيديو\|تحريك\|أفاتار\|موشن)/, design, presentation. Priorities: Figma 100, Adobe Express 98, Adobe 90, Canva 88, Runway 88, Higgsfield 86, OpenArt 84, HeyGen 82, Gamma 82, Descript 80, Genspark 78. A registered app is not proof of a connection — check the session's tools first.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** routing · connectors · MCP · توجيه

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:higgsfield` ← python3 -c "import higgsfield" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:video-gen` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-69` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-earth-ci-fork/think-mcp/worker.js:156`
- `kosif-earth-ci-fork/think-mcp/worker.js:812`
- `kosif-one/tools/kosif-omni/.app.json`
- `kosif-studio/motion/references/tools-catalog-2.md`

#### 7. قدرات قريبة في العائلة

- `GEN-67` مقدم افتراضي ودبلجة وترجمة فيديو وتكبير / Avatar presenter, dub, video translate & upscale (key)
- `GEN-68` توليد مجسمات ثلاثية بالذكاء / Text/image → 3D model (Meshy, Tripo, Rodin, TRELLIS) (key)
- `GEN-70` خوادم المالك: KOSIF Think وJev والمنصة الخاصة / Owner MCP runtimes: KOSIF Think, Jev arbiter, private Workbench (key)
- `GEN-71` البحث في مكتبة برومبتات المالك / Owner prompt-system corpus search (documented)

### `GEN-70` — خوادم المالك: KOSIF Think وJev والمنصة الخاصة / Owner MCP runtimes: KOSIF Think, Jev arbiter, private Workbench

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خوادم MCP للمالك تنفذ مهام صور SceneSpec بإيصالات ثبات، وتختار مسارًا من مجموعة مغلقة، وتجمع مشاريع ثنائية الأبعاد من منصة خاصة. / Owner MCP servers that run SceneSpec image jobs with stability receipts, pick a route from a closed set, and compile 2D projects from a private workbench.

**متى:** عند ربط موصل KOSIF في الجلسة / when the KOSIF connector is attached

**كيف:** KOSIF Think (Cloudflare Worker): kosif_full_pro_start/execute/status, kosif_secure_image_execute, kosif_verify_evidence; tests in test/*.mjs. Jev: kosif_jev_decide (stability true). Workbench: `python3 kosif-studio/motion/site_bridge.py health\|templates\|plan\|validate\|compile\|project --allow-remote` with KOSIF_SITE_TOKEN, exact HTTPS origin, no redirects, 1 MiB limit, 20 s timeout, credential echo refused, exclusive file creation.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** KOSIF Think · MCP · workbench · Jev

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-70` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-think-live/HANDOFF-README.md`
- `kosif-one/tools/kosif-think-live/test/scene-quality.test.mjs`
- `kosif-studio/motion/site_bridge.py:1`
- `kosif-studio/tests/bridge/test_site_bridge.py:1`

#### 7. قدرات قريبة في العائلة

- `GEN-68` توليد مجسمات ثلاثية بالذكاء / Text/image → 3D model (Meshy, Tripo, Rodin, TRELLIS) (key)
- `GEN-69` توجيه مزودي الإبداع وشبكة الموصلات / Creative provider routing & connector mesh (key)
- `GEN-71` البحث في مكتبة برومبتات المالك / Owner prompt-system corpus search (documented)
- `GEN-72` الرسم فوق لقطات مولدة (Draw-over) / Draw-over on generated bases (key)

### `GEN-71` — البحث في مكتبة برومبتات المالك / Owner prompt-system corpus search

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بحث BM25 واعٍ بالعربية في ملفات أنظمة البرومبت الخاصة بالمالك (Dragon V20، Blue Jewel، Cinema AI…). / Arabic-aware BM25 search over the owner's own prompt-system files (Dragon V20, Blue Jewel, Cinema AI…).

**متى:** حين يذكر المالك نظام برومبت باسمه / when the owner names one of his prompt systems

**كيف:** kosif_corpus_configure path=<folder> → kosif_corpus_index (repeat until done) → kosif_corpus_search query=… → kosif_corpus_read file offset length (200–30000 bytes; 8 hits, 3 per file). The corpus folder is not in any repo here — ask for it.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** corpus · BM25 · prompt library

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-71` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/corpus.py`
- `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/source-index.md`

#### 7. قدرات قريبة في العائلة

- `GEN-69` توجيه مزودي الإبداع وشبكة الموصلات / Creative provider routing & connector mesh (key)
- `GEN-70` خوادم المالك: KOSIF Think وJev والمنصة الخاصة / Owner MCP runtimes: KOSIF Think, Jev arbiter, private Workbench (key)
- `GEN-72` الرسم فوق لقطات مولدة (Draw-over) / Draw-over on generated bases (key)
- `GEN-73` توليد ثم تتبّع / Generate-then-trace (idea)

### `GEN-72` — الرسم فوق لقطات مولدة (Draw-over) / Draw-over on generated bases

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 (skill) — write your own look, do not paste look.js |

**ما هي:** استخدم مقاطع الذكاء الاصطناعي قاعدة حركة فقط؛ مظهر JS مكتوب يدويًا يعيد رسم كل إطار (طباعة حبرين نصف تون، خطوط، ارتجاف 12/ث، ملمس ورق) مع نص الكلمات حدثًا رئيسيًا عكس الموضوع. / AI clips are motion bases only; a hand-written JS look redraws every frame (two-ink halftone, line work, 12/s boil, paper tooth) with lyric type as a main event opposite the subject.

**متى:** فيديو موسيقي أو قصيدة بهوية مرسومة / a music video or poem with a drawn identity

**كيف:** shots.json per shot: at, dur, base frames, baseStart, focus 0..1, type big\|quiet\|none, side; film.js renderAt(t); headless Chrome photographs every frame. 480p/720p bases suffice under a draw-over. The generated base needs a key; the draw-over look itself is pure code you can write and run here on any footage (Playwright Chromium is installed).

**المعاملات:** boil 12/s; bases 480–720p

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** draw-over · halftone · boil · رسم فوق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-72` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`
- `kosif-atlas/skills/1511-homie/3903-video/scripts/drawover/look.js`

#### 7. قدرات قريبة في العائلة

- `GEN-70` خوادم المالك: KOSIF Think وJev والمنصة الخاصة / Owner MCP runtimes: KOSIF Think, Jev arbiter, private Workbench (key)
- `GEN-71` البحث في مكتبة برومبتات المالك / Owner prompt-system corpus search (documented)
- `GEN-73` توليد ثم تتبّع / Generate-then-trace (idea)
- `GEN-74` واجهات «جارٍ التوليد» من HyperFrames / AI-UI motion blocks (streaming text, typed prompt, chat reveal…) (install)

### `GEN-73` — توليد ثم تتبّع / Generate-then-trace

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 💡 `idea`: فكرة غير مبنية |
| سقف التحقق قبل العمل (A27) | V0؛ تُعرض فكرةً لا قدرة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ولّد لقطات أساس بنموذج فيديو ثم أعد رسمها حتميًا بـ JavaScript (canvas/SVG/three) لتصبح قابلة للتحرير. / Generate base shots with a video model, then redraw them deterministically in JavaScript so they become editable.

**متى:** حين يريد المستخدم حركة طبيعية لكن مخرجًا قابلًا للتعديل / natural motion but an editable result

**كيف:** AI clip as reference only → extract frames (`ffmpeg -i base.mp4 -vf fps=12 f_%04d.png`) → trace key poses as SVG paths or vectorise (`pip install vtracer`) → animate with GSAP/Remotion at the reference timing.

**التثبيت:** pip install vtracer

**الوسوم:** trace · rotoscope · تتبع

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:vtracer` ← python3 -c "import vtracer" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 💡 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 💡 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-73` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-studio/motion/references/x-trend-2026.md`

#### 7. قدرات قريبة في العائلة

- `GEN-71` البحث في مكتبة برومبتات المالك / Owner prompt-system corpus search (documented)
- `GEN-72` الرسم فوق لقطات مولدة (Draw-over) / Draw-over on generated bases (key)
- `GEN-74` واجهات «جارٍ التوليد» من HyperFrames / AI-UI motion blocks (streaming text, typed prompt, chat reveal…) (install)
- `GEN-75` بطاقات توليد من الضبابية إلى الوضوح / Blur-to-sharp 'Generating…' tiles (seen)

### `GEN-74` — واجهات «جارٍ التوليد» من HyperFrames / AI-UI motion blocks (streaming text, typed prompt, chat reveal…)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | HyperFrames Apache-2.0; blocks run on GSAP 3.14.2 (GSAP standard 'no charge' licence) |

**ما هي:** مكونات وكتل جاهزة تحرّك واجهات الذكاء الاصطناعي نفسها: نص يتدفق كإجابة، أمر يُكتب، ترتيب إجابة، محادثة، قناع رؤية آلية. / Ready components and blocks that animate AI interfaces themselves: streamed answer text, typed prompt, answer ranking, chat exchanges, machine-vision masks.

**متى:** إعلان منتج ذكاء اصطناعي أو شرح «كيف يعمل» / an AI product ad or 'how it works' explainer

**كيف:** `npx -y hyperframes@0.8.164 add <id>` → mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index, overrides as JSON in data-variable-values; colours/fonts from the 18 theme tokens; `npx hyperframes preview` / `render`. Re-skin every chat UI to a neutral or the client's own brand — never ship a look-alike of a real assistant's product. \| \| id \| kind \| what it does \| key numbers \| \|---\|---\|---\|---\| \| streaming-text \| component \| words arrive in uneven token bursts, land grey, ink to full colour \| size 27 (18–64); tone dark-on-light / light-on-dark \| \| typed-prompt \| component \| prompt types in human cadence behind a caret, optional backspace-retype of last word \| glyph `>`; cadence uniform/human; caret blink/solid \| \| segmentation-flood \| component \| translucent masks flood a subject in scanline steps, bracket + mono label per region, 2-frame HUD flicker \| flood_at 0.8 s; accent green/blue/violet \| \| ai-answer-rank \| block \| question types, assistant lists 3 picks, re-ranks so the promoted brand slides in \| 1080×1080, 9 s; #16a34a / #18181b / #fcfcfb \| \| ai-chat-reveal \| block \| keyboard rises, question sent, answer streams with thinking dot and bullets \| 1080×1920, 19.3 s \| \| chatgpt-exchange \| block \| prompt, streamed answer, comparison table, scroll back (re-skin!) \| 1080×1920, 14.9 s \| \| claude-exchange \| block \| prompt, search/reasoning steps, streamed answer with citations (re-skin!) \| 1080×1920, 21.4 s; EB Garamond + Inter \|

**التثبيت:** npx -y hyperframes@0.8.164 add streaming-text

**الوسوم:** streaming text · typed prompt · chat · AI UI · segmentation

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-74` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/components/streaming-text/registry-item.json`
- `kosif-one/vendor/hyperframes/registry/components/typed-prompt/typed-prompt.html`
- `kosif-one/vendor/hyperframes/registry/blocks/ai-chat-reveal/ai-chat-reveal.html`
- `kosif-one/vendor/hyperframes/registry/components/segmentation-flood/registry-item.json`

#### 7. قدرات قريبة في العائلة

- `GEN-72` الرسم فوق لقطات مولدة (Draw-over) / Draw-over on generated bases (key)
- `GEN-73` توليد ثم تتبّع / Generate-then-trace (idea)
- `GEN-75` بطاقات توليد من الضبابية إلى الوضوح / Blur-to-sharp 'Generating…' tiles (seen)
- `GEN-76` صورة مولدة كمحتوى بطل داخل واجهة / AI photo as the 'result' inside a UI mock (seen)

### `GEN-75` — بطاقات توليد من الضبابية إلى الوضوح / Blur-to-sharp 'Generating…' tiles

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صف من 4 بطاقات طولية تبدأ عناصر نائبة داكنة ثم تظهر الصورة من ضبابية 40px إلى 0 مع منحنى سطوع، متتابعة يسارًا ليمين والزر يقرأ «جارٍ التوليد…». / A row of 4 portrait tiles starts as dark rounded placeholders, then reveals images from 40 px blur to 0 with a brightness ramp, staggered left to right while the button reads 'Generating…'.

**متى:** أي عرض منتج توليد صور / any image-generation product demo

**كيف:** Build: 4 cards, radius 16 px, placeholder #13181d; per card `filter: blur(40px) brightness(0.4)` → `blur(0) brightness(1)` over 1 s, ease power2.out, stagger 300 ms (RTL: right to left for Arabic UI); button label pulses opacity 0.6↔1 at 1.2 s period until the last tile lands. Palette from the reference: #070709 ground, #f2f2f2 text, neo-grotesk 600 + italic serif emphasis word. Optional skeleton shimmer (see the cream demo): 110° white gradient at 25 % opacity sweeping 1.2 s.

**المعاملات:** blur 40→0 px / 1 s; stagger 300 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** blur to sharp · generating · tiles · ضبابية

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-75` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-listudio-820c7b`
- `kosif-tool/styles/pm-listudio-820c7b`

#### 7. قدرات قريبة في العائلة

- `GEN-73` توليد ثم تتبّع / Generate-then-trace (idea)
- `GEN-74` واجهات «جارٍ التوليد» من HyperFrames / AI-UI motion blocks (streaming text, typed prompt, chat reveal…) (install)
- `GEN-76` صورة مولدة كمحتوى بطل داخل واجهة / AI photo as the 'result' inside a UI mock (seen)
- `GEN-77` شريط استعراض أصول مولدة بإخراج فني واحد / AI-generated asset showreel with one art direction (seen)

### `GEN-76` — صورة مولدة كمحتوى بطل داخل واجهة / AI photo as the 'result' inside a UI mock

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** ولّد مسبقًا صورة منتج متسقة مع الهوية واستخدمها كنتيجة داخل محاكاة الواجهة لتجعل العرض مقنعًا. / Pre-generate an on-brand product photo and use it as the 'result' inside the UI mock so the demo is believable.

**متى:** عرض منتج يتضمن «اطلب صورة فتظهر» / a demo where a request produces an image

**كيف:** Chat panel types the request → cursor clicks send → skeleton shimmer card → crossfade to the photo (300 ms) → camera glides to the email preview where the image drops in with a star sparkle. Reference: warm cream #f7f4ed / #fcfbf9, ink #1e1e1e, greens #4f7a52 / #8fc78f, Inter-like 500–600, 30 fps, 30 s. Photo: warm autumn grade, a fictional product mark (never a real brand).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** UI mock · product demo · hero image · صورة بطل

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-76` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-justincooperman-e7bbc4`
- `kosif-tool/styles/pm-justincooperman-e7bbc4`

#### 7. قدرات قريبة في العائلة

- `GEN-74` واجهات «جارٍ التوليد» من HyperFrames / AI-UI motion blocks (streaming text, typed prompt, chat reveal…) (install)
- `GEN-75` بطاقات توليد من الضبابية إلى الوضوح / Blur-to-sharp 'Generating…' tiles (seen)
- `GEN-77` شريط استعراض أصول مولدة بإخراج فني واحد / AI-generated asset showreel with one art direction (seen)
- `GEN-78` عمل فني سائل قزحي / Iridescent liquid artwork (generated or shaded) (seen)

### `GEN-77` — شريط استعراض أصول مولدة بإخراج فني واحد / AI-generated asset showreel with one art direction

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مجموعة صور/مقاطع متسقة بتوجيه فني واحد (بنفسجي + أسود، ماكرو لامع) تُقطع على الإيقاع، وكلمات ضخمة حروفها مملوءة باللقطات. / A coherent set of generated images/clips under one art direction (violet + black, glossy macro) cut on beats, with giant words whose letters are filled with the footage.

**متى:** شريط منصة توليدية أو استعراض أعمال / a generative-platform reel or portfolio

**كيف:** Generate 6–12 assets at build time with fixed seeds and cache (no placeholders) — keyed step; then in code: terminal types the generate call over a dot grid → macro hero → giant uppercase words (VIDEO / AUDIO / 3D) with `background-clip: text` over the clip → tilted 3D thumbnail wall → counter to 1,000+ → 'prompt in. pixels out.' card. Reference palette #0c0b10 / #1f132f / #2e1c4e / #9a6cf0 / #5b2bd6 / #efe9f7, heavy wide grotesk + italic serif numbers, 60 fps, 15 s.

**المعاملات:** 1 palette; fixed seeds; 6–12 assets

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** showreel · image-filled type · fixed seeds · استعراض

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-77` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-influencer-seo-ce8c33`
- `kosif-tool/styles/pm-influencer-seo-ce8c33/BRIEF.md`

#### 7. قدرات قريبة في العائلة

- `GEN-75` بطاقات توليد من الضبابية إلى الوضوح / Blur-to-sharp 'Generating…' tiles (seen)
- `GEN-76` صورة مولدة كمحتوى بطل داخل واجهة / AI photo as the 'result' inside a UI mock (seen)
- `GEN-78` عمل فني سائل قزحي / Iridescent liquid artwork (generated or shaded) (seen)
- `GEN-79` لقطة صلصال مولدة / Claymation AI shot (seen)

### `GEN-78` — عمل فني سائل قزحي / Iridescent liquid artwork (generated or shaded)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صورة سائل لؤلؤي (لافندر، سماوي، وردي، ذهبي، نعناعي) تُستخدم أصلًا بطلًا متسقًا — وبديلها شيدر يمكنك كتابته هنا بلا مفتاح. / A pearlescent fluid image (lavender, cyan, blush, gold, mint) used as a consistent hero asset — with a shader alternative you can write here, keyless.

**متى:** غلاف ألبوم أو بطاقة منتج فاخرة / an album cover or premium product card

**كيف:** Shader route (no key): domain-warped fbm — q = fbm(p), r = fbm(p + 4q + 0.15t), v = fbm(p + 4r) — mapped through a 5-stop thin-film ramp (lavender → cyan → blush → gold → mint) with a fresnel-like rim = pow(1 − \|v − 0.5\|·2, 3) added as white highlight; animate t slowly (0.05–0.1 /s). Reference stage: near-black #0d0e10 rounded rectangle over green gradient, accent #1ed760, 30 fps, 18 s.

**المعاملات:** 5-colour thin-film ramp; t 0.05–0.1/s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** iridescent · fbm · shader · قزحي · liquid

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-78` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-brainextends-e19ac3`
- `kosif-tool/styles/pm-brainextends-e19ac3`

#### 7. قدرات قريبة في العائلة

- `GEN-76` صورة مولدة كمحتوى بطل داخل واجهة / AI photo as the 'result' inside a UI mock (seen)
- `GEN-77` شريط استعراض أصول مولدة بإخراج فني واحد / AI-generated asset showreel with one art direction (seen)
- `GEN-79` لقطة صلصال مولدة / Claymation AI shot (seen)
- `GEN-80` خلفية لوحة زيتية مولدة بحركة كن برنز / Painterly AI backdrop with slow Ken Burns (seen)

### `GEN-79` — لقطة صلصال مولدة / Claymation AI shot

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مقاطع بمظهر صلصال/ستوب موشن (رجل صلصال يغني، سيارات لعب، غيوم قطن) لفيديو موسيقي. / Clay/stop-motion-look clips (a singing clay man, toy cars, cotton clouds) for a music video.

**متى:** فيديو موسيقي مرح / a playful music video

**كيف:** Per 7.5 s clip: plasticine stop-motion, thumbprints, soft studio softbox, saturated sets (#3aa3d8 sky, #d9bd23 yellow, #b66176, #e23a2a red stage); 24 fps; cut on the song's bar lines; add a 12 fps step (`ffmpeg -vf fps=12,fps=24`) for stop-motion cadence. Generated footage needs a key; disclose it as AI.

**المعاملات:** 7.5 s clips; 24 fps; 12 fps step

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** claymation · صلصال · stop motion · music video

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-79` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-davidshulmanfl-371638`
- `kosif-tool/styles/pm-davidshulmanfl-371638`

#### 7. قدرات قريبة في العائلة

- `GEN-77` شريط استعراض أصول مولدة بإخراج فني واحد / AI-generated asset showreel with one art direction (seen)
- `GEN-78` عمل فني سائل قزحي / Iridescent liquid artwork (generated or shaded) (seen)
- `GEN-80` خلفية لوحة زيتية مولدة بحركة كن برنز / Painterly AI backdrop with slow Ken Burns (seen)
- `GEN-81` كولاج مقصوص وبوابات زووم لا نهائي / Cutout collage portals for infinite zoom (generated or sourced cutouts) (seen)

### `GEN-80` — خلفية لوحة زيتية مولدة بحركة كن برنز / Painterly AI backdrop with slow Ken Burns

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوحات رسم زيتية خضراء (يد روبوت، فرسان) خلف تعليق نصي، بتحريك كن برنز بطيء ونص أسفل اليسار. / Green painterly illustrations (robot hand, knights) behind captions with a slow Ken Burns move and text bottom-left.

**متى:** فصول شرح طويلة تحتاج تنوعًا بصريًا / long explainer chapters needing visual variety

**كيف:** Generate textless plates in one style lock (keyed) or paint them in code; Ken Burns: scale 1.00 → 1.06 and 1–2 % pan over the whole hold, linear or sine.inOut; caption bottom-left (bottom-right for Arabic) at 80 px safe area. Reference palette #0a0a0a / #f4f5ef / #3ee08a / #538843 / #132216, neutral grotesk 600, 30 fps.

**المعاملات:** scale 1.00→1.06; 1–2 % pan

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** Ken Burns · painterly · لوحة زيتية · backdrop

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-80` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-imthatcarlos-e04bfe`
- `kosif-tool/styles/pm-imthatcarlos-e04bfe`

#### 7. قدرات قريبة في العائلة

- `GEN-78` عمل فني سائل قزحي / Iridescent liquid artwork (generated or shaded) (seen)
- `GEN-79` لقطة صلصال مولدة / Claymation AI shot (seen)
- `GEN-81` كولاج مقصوص وبوابات زووم لا نهائي / Cutout collage portals for infinite zoom (generated or sourced cutouts) (seen)
- `GEN-82` فيلم موشن بستوري بورد يكتب Claude كوده / Storyboard-first motion film with Claude-written, sandboxed scene code (key)

### `GEN-81` — كولاج مقصوص وبوابات زووم لا نهائي / Cutout collage portals for infinite zoom (generated or sourced cutouts)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** زووم أسّي بسرعة ثابتة عبر عوالم كولاج: كل جسم مقصوص بوابة يحمل زجاجه العالم التالي، والطبقات بباراللاكس. / A constant-speed exponential zoom through collage worlds: each cutout object is a portal whose glass already holds the next world, layers in parallax.

**متى:** افتتاحية سريالية أو انتقال بين فصول / a surreal opener or chapter transition

**كيف:** Cutouts from generated (or public-domain) images: generate the character/object on pure green #00B140, key it per frame (`ffmpeg -vf chromakey=0x00B140:0.12:0.05`) or `rembg`, ping-pong a short loop for idle motion. Zoom: scale = base^t (exponential), each world nested at the portal's centre at 1/base scale so the cut is invisible; parallax depth 0.6–1.0 per layer. Reference palette #221d17 / #332b22 / #6b746d / #a09b89 / #c4c2b3, no on-screen text, 30 fps, 10 s.

**المعاملات:** key #00B140; exponential zoom; parallax 0.6–1.0

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** infinite zoom · collage · chroma key · زووم لا نهائي

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:rembg` ← python3 -c "import rembg" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-81` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `style:pm-koldo2k-5cff87`
- `kosif-tool/styles/pm-koldo2k-5cff87`

#### 7. قدرات قريبة في العائلة

- `GEN-79` لقطة صلصال مولدة / Claymation AI shot (seen)
- `GEN-80` خلفية لوحة زيتية مولدة بحركة كن برنز / Painterly AI backdrop with slow Ken Burns (seen)
- `GEN-82` فيلم موشن بستوري بورد يكتب Claude كوده / Storyboard-first motion film with Claude-written, sandboxed scene code (key)
- `GEN-83` فرز: توليد أم تركيب / Generate-or-compose triage (documented)

### `GEN-82` — فيلم موشن بستوري بورد يكتب Claude كوده / Storyboard-first motion film with Claude-written, sandboxed scene code

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** Claude يخطط 3–6 مشاهد مجموعها طول الفيلم بالضبط، ثم يكتب لكل مشهد دالة Canvas نقية لكل إطار تُترجم في نطاق مقيد وتُختبر وتُصلح ذاتيًا. / Claude plans 3–6 scenes summing exactly to the film length, then writes a pure per-frame Canvas function per scene, compiled in a restricted scope, test-rendered and auto-repaired.

**متى:** داخل تطبيق بسمة بمفتاح؛ والنمط نفسه تطبقه هنا مباشرة / in the basma app with a key; the pattern itself you apply here directly

**كيف:** genFilm(brief, dur, cat) → JSON {title, palette, scenes[{name,dur,category,brief}], voiceover, images[≤3]}; durations rescaled to D (2–120 s); 11 categories: type, ui, phone, charts, diagrams, shapes, particles, characters, photos, music (+1). Scene contract `(ctx,t,d,W,H,P,u)` at 30 fps; compileScene shadows window/document/fetch/localStorage/XMLHttpRequest/WebSocket/navigator/Function, 'use strict', ≤300 000 loop iterations per frame; test renders at t = 0, 0.3d, 0.6d, 0.99d on 360×640. Pasted gallery prompts (≤6000 chars) are adapted to Canvas scenes with Arabic text; templates can be studied (cuts, rhythm, palette measured) and 2–4 mixed.

**المعاملات:** 3–6 scenes; 30 fps; 300000 iters/frame; tests at 0/.3/.6/.99

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** storyboard · canvas · sandbox · basma · ستوري بورد

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-82` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `app/public/js/00_editor.js:530`
- `app/public/js/00_editor.js:2024`
- `app/public/js/00_editor.js:2007`
- `app/public/js/10_studio.js:4687`

#### 7. قدرات قريبة في العائلة

- `GEN-80` خلفية لوحة زيتية مولدة بحركة كن برنز / Painterly AI backdrop with slow Ken Burns (seen)
- `GEN-81` كولاج مقصوص وبوابات زووم لا نهائي / Cutout collage portals for infinite zoom (generated or sourced cutouts) (seen)
- `GEN-83` فرز: توليد أم تركيب / Generate-or-compose triage (documented)
- `GEN-84` النص فوق الصورة لا داخلها / Overlay text, never bake it (documented)

### `GEN-83` — فرز: توليد أم تركيب / Generate-or-compose triage

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** معظم إطارات الهوية تركيب لا توليد: النص على لون مسطح والصور الموجودة والمتجهات تُبنى بالكود؛ يُولَّد فقط الخلفيات والملمس والتجريد والمشاهد المستحيلة. / Most brand frames are composition: text on flat colour, existing photos and vectors are built in code; generate only backgrounds, textures, abstractions and impossible scenes.

**متى:** أول خطوة قبل أي استدعاء مدفوع / first step before any paid call

**كيف:** Table: asset \| type \| source (compose / use-existing / photograph / generate) \| decision; report how many generations were eliminated. Generated images must reserve a clean area for text. Typography always in HTML/SVG — critical for Arabic.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** triage · compose · فرز · cost

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-83` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2976-pwdev-social-media/12582-cost-control`
- `kosif-atlas/skills/2976-pwdev-social-media/12583-creative-concept/SKILL.md`
- `kosif-atlas/skills/2976-pwdev-social-media/12588-image-gen`

#### 7. قدرات قريبة في العائلة

- `GEN-81` كولاج مقصوص وبوابات زووم لا نهائي / Cutout collage portals for infinite zoom (generated or sourced cutouts) (seen)
- `GEN-82` فيلم موشن بستوري بورد يكتب Claude كوده / Storyboard-first motion film with Claude-written, sandboxed scene code (key)
- `GEN-84` النص فوق الصورة لا داخلها / Overlay text, never bake it (documented)
- `GEN-85` المراسي الأربع للثبات البصري / Four anchors of visual consistency (documented)

### `GEN-84` — النص فوق الصورة لا داخلها / Overlay text, never bake it

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** النماذج تشوّه الحروف (خصوصًا العربية)؛ كل نص طبقة حية بتشكيل سليم، والهوية بالهيكس الدقيق فوق اللقطة. / Models garble letters (especially Arabic); every text is a live, correctly shaped layer, and the brand's exact hex sits on top of the plate.

**متى:** كل صورة أو مقطع مولد / every generated still or clip

**كيف:** Generate textless plates ('clean, text-free surfaces'); set Arabic in the HTML/Remotion layer with proper shaping (ARAB family); brand-conditioning = 3–10 on-brand reference images + post-overlay of exact hex and real type, not a pinned seed.

**المعاملات:** 3–10 refs

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** overlay text · Arabic · brand · النص فوق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-84` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2306-generative-web-media/8850-brand-conditioned-generation`
- `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:121-129`

#### 7. قدرات قريبة في العائلة

- `GEN-82` فيلم موشن بستوري بورد يكتب Claude كوده / Storyboard-first motion film with Claude-written, sandboxed scene code (key)
- `GEN-83` فرز: توليد أم تركيب / Generate-or-compose triage (documented)
- `GEN-85` المراسي الأربع للثبات البصري / Four anchors of visual consistency (documented)
- `GEN-86` انضباط ميزانية التوليد المدفوع / Paid-generation budget discipline (ready)

### `GEN-85` — المراسي الأربع للثبات البصري / Four anchors of visual consistency

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** المولدات بلا ذاكرة؛ الثبات من العملية: نموذج ونسخة ثابتان، كتلة أساس ثابتة + كتلة متغيرة، بذور مسجلة، وصورة مرجع أسلوب. / Generators are stateless; consistency comes from process: one fixed model/version, fixed base block + variable block, logged seeds, an approved style reference.

**متى:** أي حملة أو سلسلة صور / any campaign or series

**كيف:** Manifest JSON per asset {model, version, seed, base, variable, file}; render a contact sheet as an HTML grid and review side by side on palette, light direction/temperature, framing distance, texture/grain, era. One outlier → regenerate it; ≥3 → fix the base and regenerate all; after 3 failed rounds generate only backgrounds and compose the rest.

**المعاملات:** 1 outlier → regen; ≥3 → fix base

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** consistency · seed · contact sheet · ثبات

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-85` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2976-pwdev-social-media/12595-visual-consistency/SKILL.md`
- `kosif-atlas/skills/2306-generative-web-media/8850-brand-conditioned-generation`

#### 7. قدرات قريبة في العائلة

- `GEN-83` فرز: توليد أم تركيب / Generate-or-compose triage (documented)
- `GEN-84` النص فوق الصورة لا داخلها / Overlay text, never bake it (documented)
- `GEN-86` انضباط ميزانية التوليد المدفوع / Paid-generation budget discipline (ready)
- `GEN-87` الترخيص أولًا وFirefly المحمي قانونيًا / Licence-first model choice & indemnified Firefly (documented)

### `GEN-86` — انضباط ميزانية التوليد المدفوع / Paid-generation budget discipline

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 / MIT |

**ما هي:** كل توليد مدفوع مُسعَّر ومسقوف ومُجرَّب جافًا ومرسل مرة واحدة ومُوصَّل عند القبول وقابل للاستئناف فلا يُدفع مرتين. / Every paid generation is priced, capped, dry-run, sent once, receipted at acceptance and resumable, so nothing is paid twice.

**متى:** قبل كل استدعاء يكلف مالًا / before every call that costs money

**كيف:** Quote → user-approved cap → dry run → single call with --yes → receipt line → on re-run poll the stored request id. Riskiest shot first as a pilot. 2 variations in round 1; change one axis per round (subject, composition, light, style or palette); yield <30 % = weak prompt; >3 rounds on one asset = switch to composition. Estimate in calls with user-supplied unit prices, never invented currency; a budget log exits non-zero over the cap.

**المعاملات:** 2 variations; <30 % yield; >3 rounds alarm

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** budget · ميزانية · receipt · cap

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-86` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `kosif-atlas/skills/1511-homie/3903-video`
- `kosif-atlas/skills/1511-homie/3889-art`
- `kosif-atlas/skills/2976-pwdev-social-media/12582-cost-control`
- `kosif-atlas/skills/2306-generative-web-media/8852-generation-budget-guard/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `GEN-84` النص فوق الصورة لا داخلها / Overlay text, never bake it (documented)
- `GEN-85` المراسي الأربع للثبات البصري / Four anchors of visual consistency (documented)
- `GEN-87` الترخيص أولًا وFirefly المحمي قانونيًا / Licence-first model choice & indemnified Firefly (documented)
- `GEN-88` الإفصاح عن الوسائط المصطنعة وحدود التوليد / Synthetic-media disclosure, provenance & ethical limits (documented)

### `GEN-87` — الترخيص أولًا وFirefly المحمي قانونيًا / Licence-first model choice & indemnified Firefly

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قرّر الاستخدام التجاري قبل الجمال: أوزان FLUX.1-dev غير تجارية؛ والعميل الذي يحتاج تعويضًا قانونيًا يذهب إلى Firefly. / Decide commercial use before aesthetics: FLUX.1-dev weights are non-commercial; a client needing IP indemnity goes to Firefly.

**متى:** بداية كل مشروع عميل / the start of every client job

**كيف:** Tag every brief commercial / non-commercial / override; set indemnity_required for resold assets; audit media folders for non-commercial outputs before delivery. Firefly: OAuth server-to-server with enterprise entitlement, x-api-key + bearer, follow the returned statusUrl with jittered polling and a hard time limit, keep content-credential metadata.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** licence · Firefly · indemnity · ترخيص

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-87` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/2306-generative-web-media/8853-license-and-provenance-ledger`
- `kosif-atlas/skills/2248-brand-identity-studio/8558-brand-legal-and-licensing`
- `kosif-atlas/skills/1819-adobe-pack/4892-adobe-core-workflow-a`

#### 7. قدرات قريبة في العائلة

- `GEN-85` المراسي الأربع للثبات البصري / Four anchors of visual consistency (documented)
- `GEN-86` انضباط ميزانية التوليد المدفوع / Paid-generation budget discipline (ready)
- `GEN-88` الإفصاح عن الوسائط المصطنعة وحدود التوليد / Synthetic-media disclosure, provenance & ethical limits (documented)
- `GEN-89` التمييز بين البرومبت والوسائط / Prompt ≠ media honesty rule (ready)

### `GEN-88` — الإفصاح عن الوسائط المصطنعة وحدود التوليد / Synthetic-media disclosure, provenance & ethical limits

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا وجوه أو أصوات أشخاص حقيقيين، لا «بأسلوب» فنان حي، لا شعارات أو شخصيات محمية، لا مشاهد وثائقية مزيفة؛ وسم المولّد وتوثيق مصدره. / No real people's faces or voices, no living artist's style, no logos or copyrighted characters, no fake documentary scenes; label and track generated media.

**متى:** كل مخرج فيه لقطة مولدة / every deliverable containing a generated shot

**كيف:** Keep a manifest of which shots are generated; add an on-screen disclosure line or end-card note when generated humans/voices appear; EU audiences: C2PA signing (some generators add SynthID); UGC-style ads still need ad disclosure; never present generated footage as a real recording; for public-sector pieces avoid AI depictions of services, staff or beneficiaries; describe qualities instead of names.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** disclosure · C2PA · ethics · إفصاح · deepfake

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-88` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/1520-digital-marketing-pro/3975-ad-creative/SKILL.md`
- `kosif-atlas/skills/1511-homie/3903-video/references/HONESTY.md`
- `kosif-atlas/skills/2976-pwdev-social-media/12588-image-gen`

#### 7. قدرات قريبة في العائلة

- `GEN-86` انضباط ميزانية التوليد المدفوع / Paid-generation budget discipline (ready)
- `GEN-87` الترخيص أولًا وFirefly المحمي قانونيًا / Licence-first model choice & indemnified Firefly (documented)
- `GEN-89` التمييز بين البرومبت والوسائط / Prompt ≠ media honesty rule (ready)
- `GEN-90` خدمة الصور المصغرة المدفوعة / Thumbnail generation via paid MCP (key)

### `GEN-89` — التمييز بين البرومبت والوسائط / Prompt ≠ media honesty rule

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** البرومبت ليس صورة، والصورة ليست فيديو مُرندرًا، والإشارة الصوتية ليست ملفًا صوتيًا؛ كل مخرج نصي يقول «لم يُرندر شيء». / A prompt is not a still, a still is not a rendered video, an SFX cue is not an audio file; text outputs must say 'none has been rendered'.

**متى:** كل تسليم برومبتات / every prompt deliverable

**كيف:** Profiles end with explicit disclaimers; the compiled editorial storyboard carries a caveat field. In your own replies: name exactly what exists on disk (path + ffprobe numbers) versus what is only a prompt.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** honesty · prompt only · صدق

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-89` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `fastify-motion-bro/docs/PRODUCTION-GATES.md:8`
- `fastify-motion-bro/scripts/viral-editorial.mjs:91`
- `fastify-motion-bro/scripts/profiles/food-flow.mjs:98`

#### 7. قدرات قريبة في العائلة

- `GEN-87` الترخيص أولًا وFirefly المحمي قانونيًا / Licence-first model choice & indemnified Firefly (documented)
- `GEN-88` الإفصاح عن الوسائط المصطنعة وحدود التوليد / Synthetic-media disclosure, provenance & ethical limits (documented)
- `GEN-90` خدمة الصور المصغرة المدفوعة / Thumbnail generation via paid MCP (key)
- `GEN-G01` خط إنتاج من موضوع إلى فيديو قصير / Topic-to-short pipeline with reviewable stages (documented)

### `GEN-90` — خدمة الصور المصغرة المدفوعة / Thumbnail generation via paid MCP

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** استوديو صور مصغرة مستضاف: بحث اتجاهات، تحليل إطارات، نص الغلاف، محاكاة نسبة النقر، توليد ونشر. / A hosted thumbnail studio: trend research, frame analysis, overlay text options, CTR simulation, generation and publishing.

**متى:** غلاف يوتيوب حين يملك المستخدم الخدمة / a YouTube cover when the user has the service

**كيف:** Personal access token + paid plan; poll jobs every ~3 s (70–100 s typical); seeds per image ≈ Gemini 7, OpenAI 11, Grok 3; YouTube allows ~100 custom thumbnail uploads per channel per 24 h. For Arabic covers prefer local HTML composition (`kmotion poster` / frame grab + type).

**المعاملات:** poll 3 s; 70–100 s/job

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** thumbnail · غلاف · CTR

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:openai` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-90` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر
- `license_blocked` (رخصة تمنع، ميزانية 1): اقرأ الرخصة من مصدرها الأصلي ← استبدل الأصل بآخر مرخص ترخيصًا متوافقًا وسجّل المصدر · البديل: أصل أصلي تصنعه أنت (رسم بالكود، صوت مولّد محليًا) · تصعيد: أصل يصر عليه المستخدم ورخصته تمنع: اشرح ولا تنسخ

#### 6. الأدلة

- `kosif-atlas/skills/932-vidseeds/2185-vidseeds-thumbnails/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `GEN-88` الإفصاح عن الوسائط المصطنعة وحدود التوليد / Synthetic-media disclosure, provenance & ethical limits (documented)
- `GEN-89` التمييز بين البرومبت والوسائط / Prompt ≠ media honesty rule (ready)
- `GEN-G01` خط إنتاج من موضوع إلى فيديو قصير / Topic-to-short pipeline with reviewable stages (documented)
- `GEN-P01` مراجعة ثانية مدفوعة من Claude API بقفلين / Optional paid Claude API second-opinion review (double opt-in) (key)

### `GEN-G01` — خط إنتاج من موضوع إلى فيديو قصير / Topic-to-short pipeline with reviewable stages

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** موضوع ← نص ← كلمات بحث لكل جملة ← لقطات مرخصة ← صوت ← ترجمة بتوقيت الكلمات ← تجميع مع خفض الموسيقى، وكل مرحلة ملف يُراجع قبل التالية. — Topic → script → search terms per sentence → licensed clips → voice → word-timed subtitles → assembly with ducked music, each stage a file reviewed before the next.

**متى:** فيديوهات قصيرة متكررة من مواضيع / recurring short videos from topics

**كيف:** Stage files: script.md, terms.json (2-3 visual terms per sentence), clips.json (source URL, licence, in/out), voice.wav, words.json, edit.json, film.mp4 + credits.txt. Clips only from sources whose licence allows reuse (Pexels/Pixabay terms, own footage); never the user's voice cloned without consent; the user approves script and clips before render. KOSIF executors: stock_fetch.py, montage_pro.py, render_html.cjs.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** moneyprinter · automation · stock footage · tts · subtitles · shorts · فيديو قصير · أتمتة · مونتاج

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-G01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `GEN-89` التمييز بين البرومبت والوسائط / Prompt ≠ media honesty rule (ready)
- `GEN-90` خدمة الصور المصغرة المدفوعة / Thumbnail generation via paid MCP (key)
- `GEN-P01` مراجعة ثانية مدفوعة من Claude API بقفلين / Optional paid Claude API second-opinion review (double opt-in) (key)
- `GEN-X01` إنتاج فيديو مرجعي عبر Higgsfield / Higgsfield reference-video production parameters and prompt skeleton (key)

### `GEN-P01` — مراجعة ثانية مدفوعة من Claude API بقفلين / Optional paid Claude API second-opinion review (double opt-in)

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `archive` |
| الرخصة | owner package (own work) |

**ما هي:** سكربت يرسل ملف إحاطة نصيًا إلى نموذج Claude لنقد الخطة، ولا يعمل إلا بعلمين صريحين ومفتاح في البيئة. / Sends a text brief to a Claude model for critique; runs only with two explicit flags and a key in the environment.

**متى:** حين يريد المستخدم رأيا ثانيا مدفوعا من نموذج Claude ينقد خطة أو إحاطة نصية / when the user wants an optional paid Claude API critique of a text brief or plan

**كيف:** python3 tools/claude_api_review.py brief.md --model <ID from your account> --send --ack-billing --output out/review.txt. Refuses without both flags, without ANTHROPIC_API_KEY in the environment, without the anthropic SDK, for briefs > 120 KB, or for --max-tokens outside 128–4096; writes nothing if the reply has no text. It is a text plan review only — it does not render, speed up ffmpeg or unlock tools. Normal work never needs it: Claude Code itself is the director. Not run here (no key, no paid call).

**المعاملات:** --max-tokens 128–4096 (default 1200) · brief ≤120 KB

**التثبيت:** pip install anthropic

**الوسوم:** claude api · review · paid · anthropic · مراجعة · مفتاح · نقد الخطة · رأي ثاني · تقييم الإحاطة · second opinion · plan critique

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `ffmpeg` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:anthropic` ← python3 -c "import anthropic" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-P01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/claude_api_review.py`
- `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/API_MODE.md`

#### 7. قدرات قريبة في العائلة

- `GEN-90` خدمة الصور المصغرة المدفوعة / Thumbnail generation via paid MCP (key)
- `GEN-G01` خط إنتاج من موضوع إلى فيديو قصير / Topic-to-short pipeline with reviewable stages (documented)
- `GEN-X01` إنتاج فيديو مرجعي عبر Higgsfield / Higgsfield reference-video production parameters and prompt skeleton (key)
- `GEN-X02` توليد متصل ثم قص / One continuous generation, then cut (documented)

### `GEN-X01` — إنتاج فيديو مرجعي عبر Higgsfield / Higgsfield reference-video production parameters and prompt skeleton

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `archive` |
| الرخصة | owner (no LICENSE file) |

**ما هي:** معاملات إنتاج مجرّبة لتوليد لقطات فيديو من صور مرجعية عبر Higgsfield، وهيكل برومبت يصف الأداء لا الشكل فقط. — Tested production settings for generating video shots from reference images on Higgsfield, and a prompt skeleton that directs the performance, not just the look.

**متى:** المستخدم يريد لقطات مولدة وصرّح بالإنفاق — the user wants generated shots and has authorised spend.

**كيف:** Stills at 2k–4k for references; video at 1080p, high bitrate, generate_audio off, 4–30 s, delivered as 24 fps HEVC; in the owner's films ≈ 12 credits per second at 1080p, ≤ 12 jobs per batch, 3–6 min per 5 s clip, plus a ~30 % reshoot reserve. Skeleton: REFERENCE DEFINITIONS / SCENE / CHARACTERS / WORLD / ACTING TASK (motive, goal, obstacle, tactic) / SHOTS with timecodes / CAMERA AND LOOK / AUDIO / CONSTRAINTS; one continuous shot with one motivated move; open mid-motion with the money moment 1–3 s in. Model names and prices drift: list the connector's current models and quote cost before generating; never spend without explicit approval.

**المعاملات:** 1080p; 4–30 s; ≈ 12 credits/s; reserve 30 %; ≤ 12 per batch

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** higgsfield · reference video · prompt skeleton · credits · توليد فيديو · برومبت

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:higgsfield` ← python3 -c "import higgsfield" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-X01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`

#### 7. قدرات قريبة في العائلة

- `GEN-G01` خط إنتاج من موضوع إلى فيديو قصير / Topic-to-short pipeline with reviewable stages (documented)
- `GEN-P01` مراجعة ثانية مدفوعة من Claude API بقفلين / Optional paid Claude API second-opinion review (double opt-in) (key)
- `GEN-X02` توليد متصل ثم قص / One continuous generation, then cut (documented)

### `GEN-X02` — توليد متصل ثم قص / One continuous generation, then cut

| الحقل | القيمة |
|---|---|
| العائلة | `ai-generation` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/ai-generation.md)) |
| المجموعة | الصور والتحرير والتوليد (`images`) |
| نوع المخرج (A25، A27) | صور وتصميم وشعار (`image`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `url` |
| الرخصة | MIT (ECC, (c) 2026 Affaan Mustafa) |

**ما هي:** ولّد لقطة طويلة متصلة ثم قصّها على إيقاع المرجع، بدل توليد كل لقطة وحدها. — Generate one long continuous take and cut it to the reference rhythm instead of generating every shot separately.

**متى:** ريل مولّد بإيقاع قطع سريع — a generated reel with fast cutting.

**كيف:** Plan the takes from the reference's cut rhythm; prompt the continuous take so any 0.8 s window stands as its own shot; cutting one generation reached 77 % usable footage versus 21 % for one generation per shot (3 calls gave 13 s). Sample shot lengths from the reference distribution, not its mean; when supplementing footage use its detected shot boundaries; crop the capture app's UI from borrowed screen recordings (temporal-variance masks keep animated chrome). Re-encode the cuts (FOOT-X03).

**المعاملات:** any 0.8 s window = a shot; 77 % vs 21 % usable

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** generation · continuous take · cadence · reel · توليد · قص · إيقاع

#### 1. الاستقبال (A25)

- المقاس والاستخدام: افتراض مكتوب ← مقاس منصة الاستخدام المذكورة
- الهوية والألوان والخطوط: افتراض مكتوب ← لوحة ألوان مقترحة بتباين WCAG AA
- صيغة قابلة للتعديل: افتراض مكتوب ← SVG أو مصدر قابل للتعديل مع PNG
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `spec` ← المخرج `image`، والمنفّذ `method:GEN-X02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- أدوات مسجلة تخدم عائلتها (اختر ما يطابق المخرج بـ `hub.py tool <id>`): `prompt-forge`.
- مراحل النوع: المقاس والهوية ← ثلاث مصغرات ← تطوير المختارة ← اختبار التصغير والتباين ← تصدير قابل للتعديل + PNG.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: مقروء بمقاس صغير (اختبار التصغير) ← تصغير إلى 15%
- إلزامي: تباين النص ≥ 4.5:1 ← حساب نسبة التباين
- إلزامي: رخصة كل خط مؤكدة من مصدره ← ملف الرخصة
- إلزامي: أصالة بلا نسخ لعمل آخر ← مقارنة بالمراجع
- إلزامي: تشكيل الحروف العربية واتصالها صحيح ← رندر فعلي ونظرة
- أمر الحكم في الوضع 1: `think.py qa image --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `tool_error` (خطأ أداة، ميزانية 3): اقرأ آخر سطر في الخطأ ثم أول سطر من كودك فيه ← أصلح السبب المثبت وحده، ثم شغّل الاختبار المتعلق · البديل: أداة أخرى أو مسار يدوي للمرحلة نفسها · تصعيد: خطأ في أداة خارجية لا تملكها: بلّغ بإعادة الإنتاج ولا تخفه

#### 6. الأدلة

- `https://github.com/affaan-m/ECC/tree/main/skills/taste-application/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `GEN-P01` مراجعة ثانية مدفوعة من Claude API بقفلين / Optional paid Claude API second-opinion review (double opt-in) (key)
- `GEN-X01` إنتاج فيديو مرجعي عبر Higgsfield / Higgsfield reference-video production parameters and prompt skeleton (key)

