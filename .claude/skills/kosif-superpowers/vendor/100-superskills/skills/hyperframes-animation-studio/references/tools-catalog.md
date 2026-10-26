# دليل أدوات إنتاج الفيديو حول HyperFrames — خلاصة عملية للمهارة

المصدر: ملف المستخدم «Hyperframes-tools-catalog-ar.html» (مراجعة 2026-10-06): 500 أداة؛ مباشرة 22 · مجاورة 254 · مكملة 224.
الأداة المرجعية: HyperFrames (https://github.com/heygen-com/hyperframes). ما يستخدمه KOSIF Motion فعلاً: HyperFrames (التصيير)، GSAP (الحركة)، FFmpeg (الترميز)، Playwright/Edge (المسار البديل)، numpy (الصوت).

## الأدوات المباشرة (تؤلف الفيديو بالكود أو الخط الزمني)

| # | الأداة | الفئة | الوصف | الترخيص | الرابط |
|---|---|---|---|---|---|
| 1 | Editly | توليد الفيديو بالكود · سطر أوامر / مكتبة | محرر فيديو تصريحي يعمل من سطر الأوامر وعبر واجهة برمجية. | غير موثق في هذه المراجعة | https://github.com/mifi/editly |
| 2 | FFCreator | توليد الفيديو بالكود · مكتبة | مكتبة Node.js لإنشاء الفيديو اعتماداً على الصور والنصوص ومواد الوسائط. | غير موثق في هذه المراجعة | https://github.com/tnfe/FFCreator |
| 3 | fframes | توليد الفيديو بالكود · إطار عمل / سطر أوامر | إطار لكتابة الفيديو باستخدام Rust وSVG وتصييره على GPU مع أدوات فحص للوكيل. | MIT | https://github.com/dmtrKovalenko/fframes |
| 4 | Manim Community | توليد الفيديو بالكود · إطار عمل / سطر أوامر | إطار Python لإنشاء مشاهد ورسوم متحركة دقيقة برمجياً، مع تركيز على الشرح الرياضي والتعليمي. | MIT؛ مجاني ومفتوح المصدر | https://www.manim.community/ |
| 5 | Motion Canvas | توليد الفيديو بالكود · إطار عمل | بيئة TypeScript لإنشاء وتحريك عروض مرئية برمجياً. | غير موثق في هذه المراجعة | https://motioncanvas.io/ |
| 6 | MoviePy | توليد الفيديو بالكود · مكتبة | مكتبة Python لتحرير المقاطع وتركيبها ومعالجتها برمجياً. | غير موثق في هذه المراجعة | https://zulko.github.io/moviepy/ |
| 7 | Remotion | توليد الفيديو بالكود · إطار عمل | إنشاء الفيديو والموشن غرافيك باستخدام React مع تصيير برمجي وتوليد دفعات. | ترخيص مجاني بشروط؛ ترخيص شركة للفرق الأك | https://www.remotion.dev/ |
| 8 | Rendervid | توليد الفيديو بالكود · إطار عمل | محرك تصيير عديم الحالة يحول قوالب JSON ومكونات React إلى فيديو وصور. | FlowHunt Attribution License؛ مجاني مع ا | https://github.com/QualityUnit/rendervid |
| 9 | Revideo | توليد الفيديو بالكود · إطار عمل | إطار لإنشاء فيديوهات برمجية ذات مشاهد ومتغيرات ومعاينة وتصيير عبر API. | غير موثق في هذه المراجعة | https://midrender.com/revideo |
| 10 | VideoFlow | توليد الفيديو بالكود · إطار عمل | يحوّل وصف TypeScript إلى JSON قابل للنقل ثم يصيّره إلى MP4 بالمتصفح أو الخادم. | Apache-2.0 | https://github.com/ybouane/VideoFlow |
| 11 | VideoRenderingEngine | توليد الفيديو بالكود · إطار عمل / واجهة API | محرك Node.js يركب مشاهد متعددة الطبقات باستخدام Canvas وFFmpeg. | غير موثق في هذه المراجعة | https://github.com/suhail472/VideoRenderingEngine |
| 12 | VidPy | توليد الفيديو بالكود · مكتبة | تحرير وتركيب الفيديو بلغة Python بالاعتماد على MLT وmelt. | غير موثق في هذه المراجعة | https://github.com/antiboredom/vidpy |
| 13 | WebMotion | توليد الفيديو بالكود · إطار عمل | تأليف مشاهد HTML أو Canvas مع زمن قائم على الإطارات وتصدير MP4 بالمتصفح. | MIT | https://github.com/superhq-ai/webmotion |
| 14 | Diffusion Studio Core | محركات تحرير الويب · مكتبة | محرك تركيب فيديو يعمل في المتصفح باستخدام WebCodecs. | غير موثق في هذه المراجعة | https://github.com/diffusionstudio/core |
| 15 | Etro | محركات تحرير الويب · مكتبة | مكتبة TypeScript لطبقات الفيديو والصور والنصوص والمؤثرات وتسجيل الناتج. | GPL-3.0 | https://etrojs.dev/ |
| 16 | Movie Masher | محركات تحرير الويب · إطار عمل | مكتبات TypeScript لتحرير الفيديو في المتصفح وتصيير الناتج عبر خادم FFmpeg. | MPL-2.0 | https://github.com/moviemasher/moviemasher.js |
| 17 | Twick | محركات تحرير الويب · حزمة تطوير | SDK React لتحرير الخط الزمني مع معاينة وتصدير MP4 محلي أو خادمي. | Sustainable Use License v1.0 | https://github.com/ncounterspecialist/twick |
| 18 | WebAV | محركات تحرير الويب · حزمة تطوير | SDK لتحرير الفيديو في الويب مبني على WebCodecs. | غير موثق في هذه المراجعة | https://github.com/WebAV-Tech/WebAV |
| 19 | Creatomate | واجهات إنشاء الفيديو · واجهة API / خدمة ويب | خدمة API لأتمتة إنشاء الفيديو باستخدام قوالب وتركيبات قابلة للتخصيص. | غير موثق في هذه المراجعة | https://creatomate.com/ |
| 20 | iLoveVideoEditor | واجهات إنشاء الفيديو · واجهة API / خدمة ويب | API سحابي يصير وصف مشهد JSON أو قالباً متغيراً إلى MP4 أو WebM. | غير موثق في هذه المراجعة | https://github.com/ilovevideoeditor/sdk-node |
| 21 | JSON2Video | واجهات إنشاء الفيديو · واجهة API / خدمة ويب | واجهة لتحرير وإنشاء الفيديو اعتماداً على وصف JSON. | غير موثق في هذه المراجعة | https://json2video.com/ |
| 22 | Shotstack | واجهات إنشاء الفيديو · واجهة API / خدمة ويب | API سحابي لتحرير الفيديو وإنشائه عبر تعريفات برمجية. | غير موثق في هذه المراجعة | https://shotstack.io/ |

## متى تختار ماذا (قرار المهارة)

- **HTML/CSS/GSAP + HyperFrames** (الافتراضي هنا): موشن غرافيك، شروح، إعلانات، نص عربي متحرك؛ حتمي وقابل للقفز إطاراً بإطار.
- **Three.js داخل الصفحة نفسها**: مشاهد ثلاثية الأبعاد واقعية (المواد، الإضاءة، البلوم) — نفس خط الأنابيب (render(t)).
- **Manim**: شروح رياضية دقيقة بالمعادلات؛ **MoviePy/FFmpeg**: التجميع والقطع والصوت؛ **Remotion/Motion Canvas/Revideo**: بدائل برمجية إن كان الفريق React/TS.
- **Lottie/Rive**: أصول متحركة جاهزة تُركَّب داخل التركيب؛ **Blender**: نمذجة أصول ثلاثية الأبعاد ثم تُصدَّر GLB.

## الفئات الأكثر صلة في الدليل (مع العدد)

- **منصات توليد الفيديو بالذكاء الاصطناعي · منصة ويب** (32): Adobe Firefly، AIVideo، Argil، Artlist، BasedLabs، Decohere، DomoAI، Dreamina
- **الرسوم المتحركة ثنائية الأبعاد · تطبيق مكتبي** (25): Adobe Animate، CreateStudio، Doodly، Mango Animation Maker، Synfig Studio، Adobe Character Animator، Animation Paper، Aseprite
- **تحرير الفيديو · تطبيق مكتبي** (21): Adobe Premiere، Avid Media Composer، Camtasia، Cinelerra-GG Infinity، Corel VideoStudio، DaVinci Resolve، EDIUS، Flowblade
- **إنشاء الفيديو من النصوص والقوالب · منصة ويب** (19): Animaker، Animoto، Biteable، FlexClip، Fliki، Fliz، Hypernatural، Lumen5
- **محررات فيديو بمساعدة الذكاء الاصطناعي · منصة ويب** (18): Canva، Capsule، Captions، Clipfly، Descript، Gling، InVideo، Kapwing
- **أتمتة الفيديو التسويقي والإعلانات · منصة ويب** (16): AdCreative.ai، Arcads، Creatify، Designs.ai، KreadoAI، Lovino (formerly LensGo)، MakeUGC، Munch Studio
- **محركات تحريك JavaScript · مكتبة** (15): Anime.js، CreateJS TweenJS، FAT، GSAP، Just Animate، KUTE.js، mo.js، Motion
- **استخراج المقاطع وإعادة استخدام المحتوى · منصة ويب** (15): 2short.ai، Choppity، ContentFries، Crayo، Exemplary AI، Klap، OpusClip، quso.ai
- **محركات تصيير ثلاثية الأبعاد · محرك تصيير** (15): appleseed، Arnold، Corona، Indigo Renderer، LuxCoreRender، Maxwell Render، Mitsuba، MoonRay
- **الموشن جرافيك والتركيب · تطبيق مكتبي** (14): Adobe After Effects، Apple Motion، Cavalry، Expressive Animator، Friction، Fusion، Google Web Designer، Hippani Animator
- **محركات ومكتبات ثلاثية الأبعاد للويب · مكتبة** (14): A-Frame، Babylon.js، ClayGL، MathBox، OGL، PlayCanvas، React Three Fiber، regl
- **برمجة إبداعية وموشن غرافيك آني · تطبيق مكتبي أو ويب** (12): cables، Field2، Gem، Isadora، Max (Jitter)، Notch، ossia score، PraxisLIVE
- **شخصيات افتراضية ومقدمو فيديو بالذكاء الاصطناعي · منصة ويب** (12): AI Studios، AKOOL، BHuman، Colossyan، D-ID، DeepReel، Elai، HeyGen
- **واجهات معالجة الفيديو · واجهة API / خدمة ويب** (12): Cloudinary Video، Rendi، api.video، AWS Elemental MediaConvert، Bitmovin Encoding، Brightcove Zencoder، Coconut، Encoding.com
- **تحريك مكونات الويب · مكتبة** (12): AutoAnimate، React Animate Height، React Awesome Reveal، React Flip Move، React Flip Toolkit، React Motion، React Move، React Spring
- **تصورات بيانات لمشاهد الفيديو · مكتبة** (12): amCharts، Apache ECharts، ApexCharts، C3.js، Chart.js، Chartist، D3، Nivo
- **تأليف وتحريك ثلاثي الأبعاد · تطبيق ثلاثي الأبعاد** (11): 3ds Max، Art of Illusion، Blender، Cascadeur، Cinema 4D، Daz Studio، Houdini، iClone
- **نصوص وأرقام متحركة · مكتبة** (10): CountUp.js، Odometer، ProgressBar.js، Shuffle Letters، Splitting.js، SplitType، TheaterJS، Typed.js
- **تصميم وعروض ثلاثية الأبعاد · تطبيق تصميم ثلاثي الأبعاد** (9): Blockbench، D5 Render، KeyShot Studio، Lumion، Marmoset Toolbag، Spline، Terragen، Twinmotion
- **رسم وتحريك Canvas ثنائي الأبعاد · مكتبة** (9): EaselJS، Konva، p5.js، Two.js، Fabric.js، oCanvas، Pts.js، Rough.js
- **مكتبات معالجة الفيديو · مكتبة** (9): Bramp FFmpeg CLI Wrapper، ffmpeg-go، ffmpeg-python، FFMpegCore، JavaCV، JCodec، PHP-FFMpeg، PyAV
- **تأليف حركة CSS · مكتبة CSS** (8): Animate.css، AnimXYZ، CSShake، Foundation Motion UI، Hover.css، Magic Animations، Vivify، WickedCSS
- **رسم وتحريك SVG · مكتبة** (7): BonsaiJS، Snap.svg، SVG.js، Lazy Line Painter، Raphaël، Vivus، Walkway
- **تأثيرات الحركة والتمرير · مكتبة** (7): AOS، Lax.js، Parallax.js، Rellax، ScrollMagic، ScrollReveal، Skrollr
- **شيدر وبرمجة مرئيات حية · أداة شيدر** (7): Bonzomatic، GLSL Sandbox، glslViewer، Hydra، KodeLife، SHADERed، The Force
- **توليد الفيديو بالكود · إطار عمل** (6): Motion Canvas، Remotion، Rendervid، Revideo، VideoFlow، WebMotion
- **حزم تحرير الفيديو · حزمة تطوير** (6): Banuba Video Editor SDK، BytePlus Video Editor SDK، IMG.LY CreativeEditor SDK، Medialooks MFormats SDK، Meishe Video Editing SDK، VisioForge Video Edit SDK .NET
- **واجهات إنشاء الفيديو · واجهة API / خدمة ويب** (5): Creatomate، iLoveVideoEditor، JSON2Video، Shotstack، Bannerbear
- **برمجة إبداعية وموشن غرافيك آني · إطار عمل** (5): Cinder، nannou، openFrameworks، OPENRNDR، Processing
- **حزم تحرير الفيديو · مكتبة** (5): Kadr، Transcoder by natario1، VideoProcessor، LinkedIn LiTr، NextLevelSessionExporter

## مكتبات الحركة والرسم التي تعمل داخل صفحة HyperFrames مباشرة

- EaselJS — مكتبة لعرض كائنات Canvas وإدارة التسلسل الهرمي والتفاعل. (https://github.com/CreateJS/EaselJS)
- Konva — مكتبة Canvas ثنائية الأبعاد لإدارة الأشكال والأحداث والتحريكات. (https://konvajs.org/)
- p5.js — مكتبة للبرمجة الإبداعية والرسم والتحريك باستخدام JavaScript. (https://p5js.org/)
- Two.js — واجهة رسم وتحريك ثنائية الأبعاد تعمل مع عدة أنواع تصيير للويب. (https://two.js.org/)
- Fabric.js — مكتبة كائنات رسومية فوق Canvas لتأليف وتعديل المشاهد. (https://www.fabricjs.com/)
- oCanvas — مكتبة Canvas قائمة على الكائنات للرسم والأحداث والتحريك. (https://ocanvas.org/)
- Pts.js — مكتبة للبرمجة الإبداعية والتصورات الهندسية والتفاعلية. (https://ptsjs.org/)
- Rough.js — مكتبة لإنتاج أشكال SVG وCanvas بأسلوب الرسم اليدوي. (https://roughjs.com/)
- ZRender — محرك رسم ثنائي الأبعاد للويب من منظومة ECharts. (https://ecomfe.github.io/zrender/)
- BonsaiJS — مكتبة رسومية ومحرك تصيير لإنشاء المحتوى المتحرك. (https://github.com/uxebu/bonsai)
- Snap.svg — مكتبة JavaScript للتعامل مع رسومات SVG الحديثة. (https://github.com/adobe-webplatform/Snap.svg)
- SVG.js — مكتبة لإنشاء SVG وتعديل أحجامه وألوانه وتحويلاته وتحريكه. (https://svgjs.dev/docs/3.0/)
- Lazy Line Painter — مكتبة JavaScript لتحريك مسارات SVG مع أداة تأليف بصرية مرتبطة. (https://github.com/merri-ment/lazy-line-painter)
- Raphaël — مكتبة JavaScript للرسم المتجهي على الويب مع أمثلة للتحريك والمسارات. (https://dmitrybaranovskiy.github.io/raphael/)
- Vivus — مكتبة لإظهار SVG وكأنه يُرسم تدريجياً مع تحكم بتوقيت المسارات. (https://maxwellito.github.io/vivus/)
- Walkway — مكتبة لتحريك رسم مسارات SVG والخطوط ومتعددات الخطوط. (https://github.com/ConnorAtherton/walkway)
- Anime.js — مكتبة تحريك للويب تتضمن خطوطاً زمنية ومفاتيح حركة وتشكيل SVG ومساراته. (https://animejs.com/)
- CreateJS TweenJS — مكتبة لإنشاء انتقالات وتحريك خصائص JavaScript ضمن CreateJS. (https://github.com/CreateJS/TweenJS)
- FAT — أداة JavaScript خفيفة لتحريك عناصر الويب. (https://github.com/nextapps-de/fat)
- GSAP — محرك JavaScript لتنسيق تسلسلات الحركة وتحريك DOM وSVG والنصوص. (https://gsap.com/)
- Just Animate — مكتبة لتبسيط إنشاء تسلسلات حركة الويب. (https://github.com/just-animate/just-animate)
- KUTE.js — محرك JavaScript لتحريك خصائص CSS وSVG. (https://thednp.github.io/kute.js/)
- mo.js — مكتبة موشن غرافيك للويب لإنشاء حركات الأشكال والمؤثرات. (https://mojs.github.io/)
- Motion — مكتبة تحريك للويب وReact وVue تشمل النوابض والإيماءات والتسلسلات. (https://motion.dev/)
- Popmotion — أدوات منخفضة المستوى لتحريك الأرقام والألوان والسلاسل بالمفاتيح والنوابض. (https://github.com/Popmotion/popmotion)
- Scene.js — مكتبة JavaScript لتأليف مشاهد وتحريكات زمنية. (https://daybrush.com/scenejs/)
- Shifty — محرك TypeScript للاستيفاء والتحريك بين القيم. (https://github.com/jeremyckahn/shifty)
- Snabbt.js — مكتبة حركة تعتمد JavaScript وتحويلات CSS. (https://github.com/daniel-lundin/snabbt.js)
- Tween.js — محرك JavaScript وTypeScript للاستيفاء التدريجي بين قيم الخصائص. (https://github.com/tweenjs/tween.js)
- Velocity.js — محرك لتحريك خصائص عناصر الويب باستخدام JavaScript. (https://github.com/julianshapiro/velocity)
- Dynamics.js — مكتبة لإنشاء حركات مبنية على المحاكاة الفيزيائية. (https://github.com/michaelvillar/dynamics.js)
- AniJS — مكتبة لتوصيف تفاعلات وتحريكات الويب بسمات HTML. (https://anijs.github.io/)
- Animate.css — مجموعة تحريكات CSS جاهزة تعمل عبر المتصفحات. (https://animate.style/)
- AnimXYZ — مجموعة أدوات لتكوين تحريكات CSS باستخدام متغيرات وأصناف. (https://animxyz.com/)
- CSShake — مكتبة أصناف CSS لتأثيرات الاهتزاز. (https://elrumordelaluz.github.io/csshake/)
- Foundation Motion UI — مكتبة انتقالات وتحريكات CSS ضمن منظومة Foundation. (https://get.foundation/sites/docs/motion-ui.html)
- Hover.css — مجموعة مؤثرات CSS لحالات التحويم على العناصر. (https://ianlunn.github.io/Hover/)
- Magic Animations — حزمة مؤثرات وتحولات جاهزة مبنية على CSS3. (https://www.minimamente.com/project/magic/)
- Vivify — مكتبة مجانية لمؤثرات حركة CSS. (https://github.com/Martz90/vivify)
- WickedCSS — مكتبة تحريكات CSS3 ذات تأثيرات واضحة وحيوية. (https://github.com/kristofferandreasen/wickedCSS)
- Animista — أداة ويب لمعاينة تحريكات CSS وتخصيصها والحصول على كودها. (https://animista.net/)
- Bounce.js — أداة ومكتبة لإنشاء تحريكات CSS3 ذات ارتدادات وتحولات. (https://github.com/tictail/bounce.js)
- AutoAnimate — أداة تضيف تلقائياً حركة عند إضافة عناصر DOM أو حذفها أو نقلها. (https://auto-animate.formkit.com/)
- React Animate Height — مكوّن React خفيف لتحريك ارتفاع العناصر بواسطة انتقالات CSS. (https://github.com/Stanko/react-animate-height)
- React Awesome Reveal — مكونات React لمؤثرات الظهور باستخدام CSS وIntersection Observer. (https://github.com/awesome-reveal/react-awesome-reveal)
- React Flip Move — أداة لتحريك تغيرات DOM وإعادة ترتيب القوائم في React. (https://github.com/joshwcomeau/react-flip-move)
- React Flip Toolkit — مكتبة انتقالات تخطيط مرنة تعتمد تقنية FLIP. (https://github.com/aholachek/react-flip-toolkit)
- React Motion — مكتبة تحريك نابضي لمكونات React. (https://github.com/chenglou/react-motion)
- React Move — مكونات React لتحريكات تستند إلى تغيّر البيانات. (https://github.com/sghall/react-move)
- React Spring — مكتبة React لتحريك القيم والمكونات باستخدام حركة نابضية. (https://www.react-spring.dev/)
- React Transition Group — مكونات لإدارة مراحل دخول وخروج عناصر React وتحولاتها. (https://reactcommunity.org/react-transition-group/)
- React Tweenful — محرك تحريك مصمم لمكونات React. (https://github.com/teodosii/react-tweenful)
- Vue Kinesis — مكتبة Vue لإنشاء تحريكات تفاعلية مركبة. (https://github.com/amineyarman/vue-kinesis)
- VueUse Motion — أدوات تحريك تصريحية لتطبيقات Vue. (https://motion.vueuse.org/)
- amCharts — مكتبة لإنشاء الرسوم البيانية والخرائط ومخططات الأسهم والمهام. (https://www.amcharts.com/)
- Apache ECharts — مكتبة تصورات بيانات تدعم عدة أنواع مخططات وتصير Canvas أو SVG. (https://echarts.apache.org/en/index.html)
- ApexCharts — مكتبة مخططات JavaScript قابلة للتفاعل والتخصيص. (https://apexcharts.com/)
- C3.js — مكتبة مخططات قابلة لإعادة الاستخدام مبنية على D3. (https://c3js.org/)
- Chart.js — مكتبة مخططات Canvas تتضمن انتقالات قابلة لضبط خصائصها. (https://www.chartjs.org/)
- Chartist — مكتبة مخططات SVG متجاوبة. (https://github.com/chartist-js/chartist)
- D3 — مكتبة JavaScript لإنشاء تصورات بيانات مخصصة وتحديث DOM وتحريكه. (https://d3js.org/)
- Nivo — مجموعة مكونات تصورات بيانات لتطبيقات React. (https://nivo.rocks/)
- Observable Plot — مكتبة JavaScript عالية المستوى للتصور الاستكشافي للبيانات. (https://observablehq.github.io/plot/)
- Plotly.js — مكتبة مخططات تصريحية تدعم الرسوم العلمية والخرائط والتحريكات. (https://plotly.com/javascript/)
- Recharts — مكتبة مكونات React لبناء مخططات البيانات. (https://recharts.github.io/)
- Victory — مكونات React قابلة للتركيب لبناء تصورات بيانات تفاعلية. (https://github.com/FormidableLabs/victory)
- AnyChart — مكتبة JavaScript للمخططات والتصورات التفاعلية. (https://www.anychart.com/)
- CanvasJS — مكتبة JavaScript لإنشاء مخططات باستخدام Canvas. (https://canvasjs.com/)
- FusionCharts — مجموعة مخططات JavaScript وخرائط للواجهات والتقارير. (https://www.fusioncharts.com/)
- Highcharts — مكتبة JavaScript لإنشاء مخططات وتصورات بيانات لتطبيقات الويب. (https://www.highcharts.com/)
- ZingChart — مكتبة مخططات JavaScript تصريحية. (https://www.zingchart.com/)
- Vega — قواعد تصريحية لبناء تصورات بيانات تفاعلية. (https://vega.github.io/vega/)
- Vega-Lite — لغة عالية المستوى لإنشاء رسوم تفاعلية من مواصفات مختصرة. (https://vega.github.io/vega-lite/)
- Paper.js — إطار برمجة رسومية متجهة يعمل فوق HTML5 Canvas. (https://paperjs.org/)
- SpriteJS — نظام رسومي متعدد المنصات لإنشاء وإدارة الرسوم والعناصر. (https://github.com/spritejs/spritejs)
- Bonzomatic — أداة برمجة حية لشيدر البكسل، موجهة لتوليد المؤثرات أثناء الأداء. (https://github.com/Gargaj/Bonzomatic)
- GLSL Sandbox — محرر ومعرض شيدر يعملان بالويب لتجربة مؤثرات ورسوم GLSL. (https://github.com/mrdoob/glsl-sandbox)
- glslViewer — عارض GLSL يعمل من الطرفية لتجربة شيدر ثنائي وثلاثي الأبعاد. (https://github.com/patriciogonzalezvivo/glslViewer)
- Hydra — مُركّب مرئي حي في المتصفح لإنشاء أنماط ومؤثرات فيديو عبر الشيفرة. (https://github.com/ojack/hydra)
- KodeLife — بيئة تطوير شيدر آنية لكتابة مؤثرات GPU ومعاينتها أثناء العمل. (https://hexler.net/kodelife)
- SHADERed — بيئة تطوير شيدر متعددة المنصات تتيح بناء خطوط تصيير ومعاينتها. (https://github.com/dfranx/SHADERed)
- The Force — بيئة WebGL للبرمجة الحية وتقديم المؤثرات البصرية أثناء الأداء. (https://github.com/shawnlawson/The_Force)
- Web Animations JS — تنفيذ JavaScript لواجهة Web Animations API. (https://github.com/web-animations/web-animations-js)
- A-Frame — إطار تصريحي لبناء مشاهد وتجارب ثلاثية الأبعاد وواقع افتراضي بعناصر HTML. (https://github.com/aframevr/aframe)
- Babylon.js — محرك JavaScript للمشاهد ثلاثية الأبعاد والتصيير والتفاعلات داخل المتصفح. (https://github.com/BabylonJS/Babylon.js)
- ClayGL — مكتبة WebGL لبناء تطبيقات وعروض ثلاثية الأبعاد قابلة للتوسع. (https://github.com/pissang/claygl)
- MathBox — مكتبة WebGL لإنشاء عروض رياضية ورسوم ثلاثية الأبعاد بجودة مناسبة للتقديم. (https://github.com/unconed/mathbox)
- OGL — مكتبة WebGL خفيفة لبناء رسوم ومؤثرات ومشاهد ثلاثية الأبعاد. (https://github.com/oframe/ogl)
- PlayCanvas — محرك رسوم للويب يدعم WebGL وWebGPU وWebXR وأصول glTF. (https://github.com/playcanvas/engine)
- React Three Fiber — عارض React لمكتبة Three.js لبناء المشاهد ثلاثية الأبعاد كمكونات. (https://github.com/pmndrs/react-three-fiber)
- regl — واجهة وظيفية لـWebGL لتنظيم أوامر الرسم وتمرير بيانات الشيدر. (https://github.com/regl-project/regl)
- Three.js — مكتبة JavaScript لبناء مشاهد وكاميرات وإضاءة وتحريك ثلاثي الأبعاد باستخدام WebGL وWebGPU. (https://github.com/mrdoob/three.js)
- Threlte — إطار ثلاثي الأبعاد لمنظومة Svelte يوفر أسلوباً تصريحياً لبناء المشاهد. (https://github.com/threlte/threlte)
- TresJS — طبقة مكونات Vue لتأليف مشاهد Three.js بصورة تصريحية. (https://github.com/Tresjs/tres)
- TWGL — مكتبة مساعدة صغيرة تقلل الشيفرة اللازمة للتعامل مع WebGL. (https://github.com/greggman/twgl.js)
- X_ITE — عارض ومكتبة JavaScript لنشر مشاهد X3D وVRML وglTF داخل صفحات الويب. (https://github.com/create3000/x_ite)
- X3DOM — إطار يدمج مشاهد X3D في HTML وDOM للتحكم البرمجي فيها. (https://github.com/x3dom/x3dom)
- CountUp.js — مكتبة لتحريك العدّ من قيمة رقمية إلى أخرى. (https://inorganik.github.io/countUp.js/)
- Odometer — مكتبة انتقالات رقمية بأسلوب عداد متحرك. (https://github.hubspot.com/odometer/docs/welcome/)
- ProgressBar.js — مكتبة لإنشاء مؤشرات تقدم متحركة باستخدام JavaScript. (https://kimmobrunfeldt.github.io/progressbar.js/)
- Shuffle Letters — مكتبة لتبديل حروف عنصر DOM بتأثير متحرك. (https://github.com/georapbox/shuffle-letters)
- Splitting.js — أداة تقسيم للعناصر والنصوص تسهل بناء تأثيرات CSS متسلسلة. (https://splitting.js.org/)
- SplitType — أداة تقسم النص إلى أسطر وكلمات وحروف قابلة للتحريك منفردة. (https://github.com/lukePeavey/SplitType)
- TheaterJS — مكتبة تحاكي سلوك الكتابة البشرية. (https://github.com/zhouzi/TheaterJS)
- Typed.js — مكتبة لتأثير الكتابة التدريجية للنصوص. (https://mattboldt.com/demos/typed-js/)
- TypeIt — مكتبة لمحاكاة الكتابة والحذف وتحريك المؤشر مع وقفات قابلة للضبط. (https://www.typeitjs.com/)
- TypewriterJS — مكتبة JavaScript لتأثير كتابة النص حرفاً بحرف. (https://github.com/tameemsafi/typewriterjs)
- jQuery Circle Progress — إضافة لرسم مؤشرات تقدم دائرية متحركة. (https://github.com/kottenator/jquery-circle-progress)
- Lettering.js — إضافة jQuery للتحكم في حروف النص وكلماته وأسطره. (https://letteringjs.com/)
- Textillate.js — أداة لتكوين حركات نصية باستخدام مكتبات CSS وتقسيم الحروف. (https://textillate.js.org/)
