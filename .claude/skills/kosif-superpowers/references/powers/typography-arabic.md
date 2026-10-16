# الخط العربي المتحرك — Arabic typography

> **قوتك هنا:** أنت تحرّك العربية كما تُقرأ — كلمات كاملة متصلة الحروف، من اليمين، بخطوط مفتوحة محمّلة قبل الإطار الأول، بمحرك تشكيل واحد، ومتزامنة مع الكلمة المنطوقة. 11 منشورًا فقط من 3,984 منشور موشن رصدناها كانت عربية (`kosif-studio/motion/references/x-trend-2026.md`) — العربية المتحركة الصحيحة هي ميزتك.
> **أقوى دليل:** كاريوكي ASS عربي بحدث لكل كلمة ومرّ اختباره (`kosif-studio/tests/test_studio.py:765`) وأعدتُ رسمه في هذه الحاوية بترتيب كلمات صحيح، وقوالب الموشن المختبرة (`mtemplates.py`)، و`style:whiteboard` حيث كتبتَ عنوانًا عربيًا بقناع ناعم ورأس ماركر.
> **You can:** shape, place, reveal, punch and caption Arabic correctly in HTML, Remotion, Pillow and libass. **93 powers follow** — ✅ 19 · 🟢 36 · 📦 6 · 🔑 0 · 👁 11 · 📄 20 · 💡 1.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص سريع لهذه الحاوية (2026-10-16):** Pillow 12.3 + RAQM 0.10.5 ✔ · ffmpeg 6.1.1 مع libass وFriBiDi وHarfBuzz ✔ · arabic-reshaper/python-bidi غير مثبتين (وهذا صحيح هنا) · `fc-list :lang=ar` لا يجد خطًا عربيًا نظاميًا غير DejaVu/FreeSerif → استخدم ملفات الخطوط في المستودعات.

## الفهرس / contents
- **قوانين التشكيل والاتجاه — Shaping & direction laws** — ARAB-01 … ARAB-10 (10)
- **الخطوط والمقاسات — Fonts & scales** — ARAB-11 … ARAB-17 (7)
- **الكشف والدخول — Reveals & entrances** — ARAB-18 … ARAB-33 (16)
- **التوكيد والكلمة البطلة — Emphasis & hero words** — ARAB-34 … ARAB-48 (15)
- **العناوين والبطاقات والقوالب — Titles, cards & templates** — ARAB-49 … ARAB-61 (13)
- **الترجمة والكاريوكي والنص من الصوت — Captions, karaoke & verse from sound** — ARAB-62 … ARAB-71 (10)
- **الأرقام والعزل والتوطين — Numbers, bidi & localisation** — ARAB-72 … ARAB-83 (12)
- **المحاكاة والمطابقة ومحركات الرسم — Mimic, matching & raster engines** — ARAB-84 … ARAB-90 (7)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves
- **إضافات v2 — v2 additions** — ARAB-X01 … ARAB-X03 (3)

## قوانين التشكيل والاتجاه — Shaping & direction laws

_القواعد التي تمنع الكارثة قبل أي حركة: الوصل، الاتجاه، التحميل، ومحرك التشكيل._

#### ARAB-01 · الكلمة كاملة لا الحرف · Whole-word law · ✅ مُثبت هنا / proven here
- **ماذا / what:** الحرف العربي يتغير شكله حسب موقعه، فكل span لحرف واحد يكسر الوصل؛ حرّك الكلمة أو العبارة أو السطر كوحدة. — Arabic letters change shape by position, so per-letter spans break joining; animate words, phrases or lines as units.
- **متى أستخدمها / when:** أي نص عربي متحرك بلا استثناء — every moving Arabic text, no exceptions.
- **كيف / how:** Split on spaces only (keep ZWJ U+200D / ZWNJ U+200C inside words); one inline-block span per word inside a direction:rtl container; to 'write' a word progressively use a mask/clip wipe over the shaped word (ARAB-21/22), never letters. Latin in the same film may go per letter; Arabic goes per word or per shaped glyph-run (text-to-path). The tested canvas starter splits its title exactly this way. **أرقام / params:** Latin letter stagger 25 ms, in 40 px / 320 ms cubic-bezier(0.2,0.9,0.2,1), out 180 ms; Arabic word stagger 60–160 ms; ≤5–7 words per screen.

```js
function arabicWords(el) {           // whole words only — never letters
  const words = el.textContent.trim().split(/\s+/);
  el.textContent = ''; el.style.direction = 'rtl';
  for (const w of words) {
    const s = document.createElement('span');
    s.textContent = w; s.style.display = 'inline-block';
    s.style.marginInline = '0.12em'; el.append(s);
  }
  return [...el.children];              // animate these spans
}
```

- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:97` · `kosif-tool/playbooks/arabic-typography.md:25` · `100-superskills/skills/kinetic-typography-arabic/SKILL.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/SKILL.md`

#### ARAB-02 · حصر الاتجاه في عناصر النص · RTL scoping for renderers · ✅ مُثبت هنا / proven here
- **ماذا / what:** في HyperFrames يبدو ‎<html dir="rtl">‎ سليمًا في المعاينة لكن الرندر يخرج أسود بالكامل؛ ضع direction:rtl وunicode-bidi:isolate على عناصر النص فقط. — In HyperFrames <html dir="rtl"> previews fine but renders a fully black video; scope direction:rtl + unicode-bidi:isolate to text elements.
- **متى أستخدمها / when:** كل صفحة HTML تُرندر إلى فيديو — every HTML page that becomes video (HyperFrames, motion-kit, render_html.cjs).
- **كيف / how:** Keep <html lang="ar"> with no dir; CSS .line{direction:rtl;unicode-bidi:isolate}; Latin lockups get direction:ltr; numbers such as 24 get direction:ltr inside Arabic layouts. The vendor linter raises html_dir_attribute_breaks_render (severity error, also for dir="auto") and kosif-studio qa.py checks it too. Ordinary web pages (not renders) may keep <html dir=rtl> with logical CSS properties (margin-inline-start). **أرقام / params:** lint id html_dir_attribute_breaks_render.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/lint/src/rules/composition.ts:1150` · `kosif-one/vendor/hyperframes/packages/lint/src/rules/composition.test.ts` · `kosif-studio/motion/qa.py:62` · `kosif-studio/tests/test_studio.py:549`

#### ARAB-03 · لا تباعد ولا مطّ — الكشيدة فقط · No tracking, no stretch — kashida only · 📄 موصوف / documented only
- **ماذا / what:** letter-spacing يقطع الوصل وscaleX غير المتساوي يشوّه الضربات؛ الإطالة بالكشيدة (ـ U+0640) أو محور wdth فقط. — Letter-spacing breaks joins and non-uniform scaleX distorts strokes; elongate only with kashida or a wdth axis.
- **متى أستخدمها / when:** عناوين تحتاج عرضًا، كلمات «التوسّع»، وأي ستايل لاتيني فيه حركة تتبّع — wide titles, 'expansion' words, Latin tracking styles.
- **كيف / how:** letter-spacing:0 on every Arabic run (some owner hero CSS uses −.035em — keep that for Latin only); insert tatweel between two joining letters in designed titles, sparingly, never animated per character; scale the word uniformly (scale, never scaleX); for elastic width use a variable font's wdth axis. The Latin 'tracking 0.3em→0 in 0.6 s' entrance is Latin-only. **أرقام / params:** letter-spacing 0; kashida U+0640; uniform scale only.
- **الدليل / proof:** `kosif-tool/playbooks/arabic-typography.md:28` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md` · `100-superskills/skills/kosif-montage-motion/references/launch-video.md` · `kosif-one/tools/kosif-omni/skills/kosif-web-design/SKILL.md`

#### ARAB-04 · بوابة تحميل الخط قبل الإطار الأول · Font-ready gate before frame 0 · 🟢 جاهز / ready
- **ماذا / what:** لا يبدأ الرندر ولا القياس قبل أن يُحمَّل كل وزن خط بعيّنة عربية، وإلا يُخبز الخط البديل في الفيديو. — Never capture or measure before every weight is loaded with an Arabic sample, or fallback glyphs get baked in.
- **متى أستخدمها / when:** قبل أي التقاط إطار أو ورقة لقطات أو fitText — before any capture, contact sheet or text measurement.
- **كيف / how:** HTML: await document.fonts.load('800 62px "Cairo"', 'الأرنب') per weight, then document.fonts.ready; Basma fontsReady() gathers the caption font + Lalezar/Cairo/Reem Kufi/Plex + every family named in scene code (regex font:"…"), loads 400/700/900 with the sample 'بصمة Aa 123' and races a 4 s timeout. Remotion: loadFont({family, url: staticFile('X.woff2'), weight}) once per weight + delayRender. Measure only after the gate. **أرقام / params:** weights 400/700/900; timeout 4000 ms; sample = Arabic + Latin + digits.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:136` · `app/public/js/00_editor.js:2932` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/local-fonts.md` · `kosif-tool/playbooks/arabic-typography.md:15`

#### ARAB-05 · مساحة التشكيل وحواف الأقنعة · Harakat headroom & mask padding · 🟢 جاهز / ready
- **ماذا / what:** النقاط والحركات تخرج عن صندوق السطر، فالقناع الضيق يقصّها؛ اترك 0.15–0.25em وزِد حشوة القناع من الأسفل. — Dots and diacritics overflow the line box, so tight masks clip them; leave 0.15–0.25 em and pad masks at the bottom.
- **متى أستخدمها / when:** كل قناع أو overflow:hidden حول نص عربي — any mask or overflow:hidden around Arabic.
- **كيف / how:** motion-kit word mask = clip-path inset(-0.05em -0.05em 0 -0.05em) with padding .06em .04em .18em (extra bottom for kasra and descenders); titles line-height ≥1.25, body 1.5–1.85; line wrappers that rise from a cut line need generous line-height; inspect dots at the mask edge on a still frame. **أرقام / params:** headroom 0.15–0.25 em; mask padding .06/.04/.18 em; body lh 1.85 (v17).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:129` · `kosif-tool/playbooks/arabic-typography.md:71-73` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-audit-pro/patch/kosif-v17.css`

#### ARAB-06 · توجيه محرك التشكيل · Shaping-engine routing · ✅ مُثبت هنا / proven here
- **ماذا / what:** محرك واحد فقط يشكّل العربية: المتصفح (HarfBuzz) أو Pillow+RAQM أو libass — ولا تشكّل النص مرتين أبدًا. — Exactly one engine shapes Arabic — the browser, Pillow+RAQM or libass — never two in a row.
- **متى أستخدمها / when:** أي نص خارج المتصفح: أغلفة، إطارات Pillow، حرق ffmpeg — any non-browser text: covers, Pillow frames, ffmpeg burns.
- **كيف / how:** Chromium/Remotion/HyperFrames shape automatically and are best for full tashkeel (mimic sets engine:'browser' for harakat). Pillow here has RAQM 0.10.5 → pass RAW logical text with layout_engine=RAQM. Only when RAQM is absent use arabic_reshaper + python-bidi, and then the font must carry Presentation Forms-B (Amiri, Noto Naskh). In ffmpeg use the ass/subtitles filters (libass + HarfBuzz + FriBiDi), not drawtext. Owner model code: mm_render_text (RAQM → 'pil' engine, else 'ass' engine with two-background matting) and wbcompat._shape. Verified in this container on 2026-10-16 with Cairo: RAQM on raw text = correct; reshaper+bidi fed into RAQM = words and letters reversed; reshaper + BASIC layout = tofu on isolated forms (ا إ ر) because Cairo lacks those Presentation-Forms code points (Amiri and Noto Naskh carry FE70–FEFC); drawtext = the same tofu, and text_shaping=0 = disjoint, reversed letters. **أرقام / params:** PIL features.check('raqm') == True (0.10.5); ffmpeg 6.1.1 --enable-libass --enable-libfribidi --enable-libharfbuzz.

```python
from PIL import ImageFont, features
def arabic_font(path, size):
    eng = ImageFont.Layout.RAQM if features.check('raqm') else ImageFont.Layout.BASIC
    return ImageFont.truetype(path, size, layout_engine=eng), eng
def prep(text, eng):                     # shape once, never twice
    if eng == ImageFont.Layout.RAQM:
        return text                       # RAQM does joining + bidi itself
    import arabic_reshaper; from bidi.algorithm import get_display
    return get_display(arabic_reshaper.reshape(text))
```

- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_render_text.py` · `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:212` · `100-superskills/skills/kosif-montage-motion/references/mimic.md` · `kosif-atlas/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu/SKILL.md`

#### ARAB-07 · كشف الاتجاه تلقائيًا · Auto RTL detection · 🟢 جاهز / ready
- **ماذا / what:** تعبير منتظم واحد يلتقط الحروف العربية فيقلب اتجاه الرسم والمحاذاة وجانب البطاقة تلقائيًا. — One regex spots Arabic letters and flips drawing direction, alignment and card side automatically.
- **متى أستخدمها / when:** نصوص يكتبها المستخدم بلغات مختلطة — user text of unknown language.
- **كيف / how:** Canvas: ctx.direction = /[\u0600-\u06FF]/.test(s) ? 'rtl' : 'ltr'; lowerThird picks side and sets RTL on the box only; the review page's AR_RUN regex (U+0600–06FF, 0750–077F, FB50–FDFF, FE70–FEFF with ZWJ/ZWNJ, spaces and «») wraps each Arabic run in <bdi dir=rtl>. **أرقام / params:** ranges U+0600–06FF, 0750–077F, FB50–FDFF, FE70–FEFF.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:75` · `app/public/js/00_editor.js:17` · `kosif-studio/motion/kit/motion-kit.js:562` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:902`

#### ARAB-08 · مفتاح لغة المحتوى · Content-language switch ar|en|both · ✅ مُثبت هنا / proven here
- **ماذا / what:** خيار واحد عند تجهيز المشروع يحدد: عربي فقط، أو إنجليزي فقط، أو ثنائي اللغة مع اتجاه لكل سطر. — One scaffold flag fixes Arabic-only, English-only or bilingual with per-line direction.
- **متى أستخدمها / when:** بداية كل مشروع من الكتالوج — at scaffold time.
- **كيف / how:** python3 tools/kosif.py scaffold <style-id> <dir> --content-lang ar|en|both (default ar). ar = Arabic only, RTL, a clear Arabic face; both = Arabic and English together, each line with its own dir (English ~70% size under the Arabic, see ARAB-55). **أرقام / params:** default ar.
- **الدليل / proof:** `kosif-tool/tools/kosif.py:83` · `kosif-tool/playbooks/arabic-typography.md`

#### ARAB-09 · نص حقيقي فوق لوحات التوليد · Real type over generated plates · ✅ مُثبت هنا / proven here
- **ماذا / what:** نماذج الصور تشوّه الحروف العربية، فولّد المشهد بلا نص ثم ضع العربية طبقة HTML/SVG حقيقية بخط مفتوح. — Image models garble Arabic; generate textless art and overlay real HTML/SVG type in an open font.
- **متى أستخدمها / when:** أي صورة أو فيديو مولّد يحتاج كلامًا عربيًا — any generated plate that needs Arabic words.
- **كيف / how:** Generation fields stay English; append 'No text, no labels, no captions, no watermark'; reserve a clean band (e.g. a bottom caption bar); the owner prompt linter REVISEs any prompt containing Arabic letters and the forge emits INFO arabic_text for U+0600–06FF; then set the Arabic in SVG/HTML/Remotion with Plex or Cairo and animate it in code. Comics: panels without text, bubbles drawn in code. If text must live inside the image, quote it for Ideogram (account/key) — still check the joins. **أرقام / params:** trigger range U+0600–06FF; overlay fonts IBM Plex Sans Arabic / Cairo.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/scripts/prompt_lint.py` · `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/scripts/prompt_forge.py:121` · `100-superskills/skills/image-prompt-forge/scripts/image_prompt_forge.py:56` · `kosif-atlas/skills/1094-akbun-draw/2423-akbun-draw-webtoon-b`

#### ARAB-10 · العربية داخل مشهد ثلاثي الأبعاد · Arabic inside 3D scenes · 📄 موصوف / documented only
- **ماذا / what:** لا تبثق العربية هندسةً ثلاثية الأبعاد من خط غير مُشكّل؛ ارسمها على نسيج Canvas باتجاه rtl أو ضعها طبقة HTML فوق المشهد. — Never extrude Arabic as 3D geometry from an unshaped font; use a CanvasTexture drawn RTL or an HTML overlay.
- **متى أستخدمها / when:** عناوين داخل three.js أو R3F — titles inside three.js / R3F worlds.
- **كيف / how:** Draw the whole line on a 2D canvas after the font gate (ctx.direction='rtl', ctx.textAlign='right', fillText(wholeString)) → THREE.CanvasTexture on a plane (anisotropy on, size ×2 for sharpness); or project an HTML label per frame (ARAB-80). Check joins on a rendered still.
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:74`

## الخطوط والمقاسات — Fonts & scales

_أي خط، من أين، بأي وزن وحجم._

#### ARAB-11 · خريطة أصوات الخطوط · Arabic font voice map · 🟢 جاهز / ready
- **ماذا / what:** عائلات OFL مرتبة حسب «الصوت» — كوفي، سانس حديث، نسخ، رقعة، عرض — وملفاتها موجودة على القرص. — OFL families sorted by voice — Kufi, modern sans, Naskh, Ruqaa, display — with the files already on disk.
- **متى أستخدمها / when:** مرة واحدة لكل فيلم: خط عرض + خط نص — once per film: one display + one text family.
- **كيف / how:** Pick by voice (table). Files on disk: 100-superskills/skills/kosif-mimic/assets/fonts (23 TTF + OFL-LICENSES.txt), kosif-tool/.claude/skills/kosif-superpowers/proofs/_shared/fonts (Amiri, Aref Ruqaa, Cairo variable, Lalezar, Reem Kufi variable, Tajawal Bold), kosif-earth-ci-fork/ui/art/fonts (Plex/Readex/Tajawal/Naskh woff2 subsets). The full catalogue (41 families / 81 faces) lives in mm_fonts_lib; its fetch pulls from google/fonts — raw.githubusercontent.com is reachable here, github.com raw is not. **أرقام / params:** catalogue: sans 12, naskh 10, display 8, kufi 4, rounded 2, hand 2, nastaliq 2, ruqaa 1.

| الصوت / voice | على القرص / on disk | للجلب / fetch | الاستخدام / use |
|---|---|---|---|
| كوفي هندسي / geometric Kufi | Reem Kufi 400/700, Changa 700 | Noto Kufi Arabic, Kufam, Qahiri | hooks, brand, punchy captions |
| سانس حديث / modern sans | Cairo 400/700/900, Tajawal 400/700/900, Almarai 700, Plex & Readex (woff2) | Alexandria, Rubik, Noto Sans Arabic, Mada, Vazirmatn | titles, captions, UI, data |
| نسخ كتابي / book Naskh | Amiri 400/700, Noto Naskh 400/700, Lateef 400/700, Mirza 700 | Scheherazade New, Markazi Text, Harmattan | cinema subtitles, poetry, dua |
| رقعة / Ruqaa | Aref Ruqaa 400/700 | — | heritage titles, maps, chalk lessons |
| عرض ويدوي / display & hand | Lalezar, Rakkas, El Messiri 400/700, Marhey 700 | Alkalami, Katibeh, Ruwudu | hook stomps, lyric heads, whiteboard lettering |

- **الدليل / proof:** `100-superskills/skills/kosif-mimic/assets/fonts` · `kosif-one/tools/kosif-mimic/assets/fonts/fonts.json` · `100-superskills/skills/kosif-mimic/scripts/mm_fonts_lib.py:20` · `app/index.html:10`
- **⚖️ ترخيص / license:** كلها OFL-1.1؛ ما يشبه Thmanyah أو Dubai أو Diwani في المراجع خطوط مملوكة — مرجع فقط / all OFL-1.1; Thmanyah-, Dubai- and Diwani-like faces seen in references are proprietary — reference only.

#### ARAB-12 · كايرو المقسوم بنطاق يونيكود · Cairo split by unicode-range · ✅ مُثبت هنا / proven here
- **ماذا / what:** Cairo 600/800 في ملفي woff2 (عربي ولاتيني) تحت عائلة واحدة، مدمج في كل قوالب الموشن. — Cairo 600/800 shipped as Arabic + Latin woff2 subsets under one family, wired into every motion template.
- **متى أستخدمها / when:** أي مشروع HTML يحتاج خطًا عربيًا خفيفًا مضمونًا — any HTML film needing a guaranteed light Arabic face.
- **كيف / how:** @font-face family 'Cairo' for weights 800/600; the Arabic file covers U+0600-06FF, U+0750-077F, U+FB50-FDFF, U+FE70-FEFF (+U+0660-0669), the Latin file U+0000-00FF; mtemplates copies both into projects/NAME/assets/fonts; preload per ARAB-04. Earth uses the same split for Plex/Readex/Tajawal/Naskh (adds U+0870-088E). For renders use font-display:block (swap is for web pages). **أرقام / params:** Arabic 800 = 13,880 B, 600 = 13,828 B; Latin 800 = 15,256 B, 600 = 15,252 B.

```css
@font-face{font-family:Cairo;font-weight:800;font-display:block;
  src:url(assets/fonts/cairo-arabic-800-normal.woff2) format('woff2');
  unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF;}
@font-face{font-family:Cairo;font-weight:800;font-display:block;
  src:url(assets/fonts/cairo-latin-800-normal.woff2) format('woff2');
  unicode-range:U+0000-00FF;}
```

- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/fonts/cairo-arabic-800-normal.woff2` · `100-superskills/skills/kosif-montage-motion/scripts/kit/fonts/OFL-Cairo.txt` · `100-superskills/skills/kosif-montage-motion/templates/motion/title-card.html:9` · `kosif-earth-ci-fork/ui/ds/fonts.css`

#### ARAB-13 · اكتشاف الخطوط وسلسلة البدائل · Font discovery & fallback chain · 🟢 جاهز / ready
- **ماذا / what:** يبحث عن ملفات خطوط تدعم العربية في مجلدات ويندوز ولينكس وماك وkit/fonts ويرتبها حسب الاكتمال — ويتوقف بدل الاستبدال الصامت. — Finds Arabic-capable font files across OS folders and kit/fonts, ranked by completeness — stop rather than silently substitute.
- **متى أستخدمها / when:** قبل أي رندر Pillow أو ASS على جهاز جديد — before Pillow/ASS renders on a new machine.
- **كيف / how:** python kosif-studio/motion/tools.py fonts. Pillow order (tools._ARABIC): NotoNaskhArabic → NotoSansArabic → NotoKufiArabic → Cairo → Tajawal → Almarai → Amiri → Scheherazade → KacstOne → DejaVuSans. CSS chain 'KD'/'KV': Dubai 300/500/700 → Noto Kufi/Sans Arabic → DejaVu. Remotion FONT: Noto Naskh → Noto Sans → Cairo → Tajawal → Plex → Segoe UI → DejaVu → system-ui. Here `fc-list :lang=ar` shows only DejaVu/FreeSerif/FreeMono/Unifont, so always point renders at repo font files (ARAB-11) or pass fontsdir= to libass. **أرقام / params:** check: fc-list :lang=ar; fonttools cmap check before render.
- **الدليل / proof:** `kosif-studio/motion/tools.py:79` · `100-superskills/skills/kosif-montage-motion/scripts/tools.py:81` · `kosif-studio/motion/templates/directed.html` · `kosif-tool/starters/remotion/src/Film.tsx:34`
- **⚖️ ترخيص / license:** Dubai خط مملوك (مايكروسوفت/دبي) للاستخدام المحلي فقط ولا يُشحن مع المشروع؛ بدائل Noto برخصة OFL / Dubai is proprietary — local use only, never ship it; Noto fallbacks are OFL.

#### ARAB-14 · محمّل الخطوط الحي ومنتقي الخط · Live Google Fonts loader & picker · 🟢 جاهز / ready
- **ماذا / what:** حقن رابط Google Fonts عند الطلب لتبديل خط الواجهة أو العنوان مباشرة أثناء المراجعة. — Inject a Google Fonts link on demand to swap the UI or title face live during review.
- **متى أستخدمها / when:** جلسات المراجعة واختيار الخط مع المستخدم — review sessions and font picking.
- **كيف / how:** FONTS table + loadFont(id) creates <link id=sk-font-*> to fonts.googleapis.com/css2 with display=swap (+ preconnect fonts.gstatic.com), then sets --sk-font / --sk-font-display. Earth picker: Plex, Tajawal 400–800, Cairo 400–800, Almarai 400/700/800, Noto Kufi 400–800, Readex 400–700, Noto Naskh 400–700, system-ui; review page adds El Messiri, Amiri, Lalezar. fonts.googleapis.com is reachable here, but the final render must use vendored files (ARAB-12) so it never depends on the network. **أرقام / params:** 8 picker faces; review page 9 families.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/layouts/shell.js:58` · `kosif-audit-studio/index.html` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:9` · `kosif-tool/starters/html-canvas/index.html:8`

#### ARAB-15 · اقترانات الخطوط · Type pairings · ✅ مُثبت هنا / proven here
- **ماذا / what:** عنوان كوفي فوق نص Plex، أو Readex للعربي مع Fraunces للاتيني — صوتان مختلفان بإيقاع واحد. — Kufi headlines over Plex body, or Readex Arabic with Fraunces Latin — two voices, one rhythm.
- **متى أستخدمها / when:** أفلام ثنائية اللغة والهويات — bilingual films and brand systems.
- **كيف / how:** Editorial: .brand strong,h1,h2,h3 {font-family:'Noto Kufi Arabic','IBM Plex Sans Arabic'}; body Plex/Tajawal; hero h1 clamp(34px,5vw,68px) lh 1.16, hero p lh 2. Bilingual system: Fraunces 500/600 for Latin display + Readex Pro 300–700 for Arabic and UI, Latin tabular digits, scale 13/14/16/18/22/26/28 px, 4 px grid, radius 8/12/20/999. Ads: heavy Kufi with condensed uppercase Latin at matched x-height, ≥96 px. Rule: same mood, explicit size per script in tokens.json. **أرقام / params:** Kufi+Plex; Readex+Fraunces; Kufi+condensed Latin ≥96 px.
- **الدليل / proof:** `kosif-audit-studio/kosif-one-editorial-theme.css` · `kosif-one/tools/kosif-web/docs/04-design-system.md` · `kosif-tool/styles/pm-deifosv-04e4d3/BRIEF.md` · `100-superskills/skills/brand-identity-logo/SKILL.md:24`

#### ARAB-16 · سلّم أحجام الفيديو · Video type scale at 1080 px · 📄 موصوف / documented only
- **ماذا / what:** الترجمة 56–72 بكسل، العناوين 96–180، التسميات ≥32 — والعربية أكبر 10–15% من نظيرها اللاتيني. — Captions 56–72 px, titles 96–180, labels ≥32 — Arabic runs 10–15% larger than Latin.
- **متى أستخدمها / when:** تحديد الأحجام قبل أي مشهد — sizing before any scene.
- **كيف / how:** Tokens: title 700 88–120 px lh 1.15 (STYLE.md) up to hero 120–220 px (kinetic type); support 56–80; body 500 44–56 lh 1.4; label 600 32–40 lh 1.2; numerals 600 48–72, LTR inside RTL; lh 1.5–1.7 body/captions, 1.25–1.35 titles; weights 600–900 in motion (thin weights shimmer); chart labels never below ~24 px at 1080p (~12 px web); right-align paragraphs, centre titles and captions. **أرقام / params:** captions 56–72; titles 96–180; labels ≥32; +10–15% vs Latin.
- **الدليل / proof:** `kosif-tool/playbooks/arabic-typography.md:16-19` · `kosif-tool/templates/STYLE.md` · `kosif-tool/playbooks/kinetic-type.md` · `kosif-atlas/skills/345-visuals/1242-html-diagram/references/svg-primitives.md`

#### ARAB-17 · سلّم القراءة للشاشات · Screen reading scale (v17 / SQC) · 🟢 جاهز / ready
- **ماذا / what:** أربع درجات واضحة مكبّرة للنقاط والتشكيل بإيقاع عمودي واحد وقياس 78ch — للواجهات التي تظهر داخل الفيديو. — Four clear steps enlarged for dots and diacritics, one vertical rhythm, 78ch measure — for UI shown inside films.
- **متى أستخدمها / when:** شاشات تطبيقات ولوحات بيانات داخل الفيلم — app screens and dashboards in a film.
- **كيف / how:** v17 tokens xs 13, sm 14, base 15.5 (was 13.5), lg 17, xl 21, 2xl 27 px; leading 1.85 / tight 1.4; spacing 6/12/18/26/38; max-width 78ch (line 41→69 chars); print 11pt/1.6. SQC: 12/13.5/16/17/22/28 (+11) px, weights 400 body / 600 labels / 700–800 headings, no 900, body lh 1.7, one fluid title clamp(24px,1.4vw+17px,32px) 800. Stack: IBM Plex Sans Arabic → Tajawal → Noto Sans Arabic → Arial; mono IBM Plex Mono. **أرقام / params:** base 15.5 px; lh 1.85; 78ch.
- **الدليل / proof:** `kosif-audit-pro/patch/kosif-v17.css` · `kosif-earth-ci-fork/ui/ds/tokens.css:35` · `kosif-audit-pro/app/globals.css:147` · `kosif-earth-ci-fork/docs/design/SQC-IDENTITY-ar.md`

## الكشف والدخول — Reveals & entrances

_كيف تدخل الكلمات العربية الشاشة دون أن يُكسر حرف._

#### ARAB-18 · قواعد التايبوغرافي العربي الحركي · Kinetic Arabic grammar · 🟢 جاهز / ready
- **ماذا / what:** قسّم النص إلى وحدات معنى ≤5 كلمات، كلمة مفتاحية واحدة لها دخول مميز، والباقي يدخل بهدوء من اليمين. — Meaning units of ≤5 words, one keyword with a distinct entrance, the rest enters quietly from the right.
- **متى أستخدمها / when:** اقتباسات، خطافات، بيانات، أفلام الكلمات والقصائد — quotes, hooks, manifestos, lyric and narration films.
- **كيف / how:** ≤7 words on 9:16 (12 on 16:9); two sizes per scene (hero 120–220 px, support 56–80); entrance 300–450 ms translateY 40–70 px cubic-bezier(0.22,1,0.36,1), opacity in the first 60%; stagger 70–120 ms, or words.json start − 60 ms; exit 200–300 ms, always shorter than the entrance; hold ≥ 0.3 s + 0.06 s × characters; weights 300 vs 900 for contrast; 0.35 s per word when there is no audio; read every line twice on the contact sheet. Scaffold: python3 tools/kosif.py scaffold kinetic-arabic <dir>; preview node tools/render_html.cjs --preview. **أرقام / params:** ≤5 words/unit; 0.35 s/word; entrance 300–450 ms; stagger 70–120 ms.
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md` · `kosif-tool/styles/kinetic-arabic/SKILL.md` · `100-superskills/skills/kinetic-typography-arabic/SKILL.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### ARAB-19 · أقنعة الكلمات: إظهار وإخفاء · Word-mask reveal & hide · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل كلمة داخل قناعها الخاص تنزلق للأعلى واحدة بعد الأخرى، والحروف متصلة في كل إطار. — Each word slides up out of its own mask in turn, letters joined in every frame.
- **متى أستخدمها / when:** العناوين الرئيسية والجمل المهمة — hero titles and key lines.
- **كيف / how:** MOTION.words(el) → span.mk-w (mask) > span.mk-wi; MOTION.revealWords(tl, el, at, {from:'top', dur:.7, stagger:.07, ease:'expo.out'}) = yPercent 115→0, opacity 0→1; a .num child pops scale 0→1 in 0.6 s with spring 'snappy'; MOTION.hideWords(tl, el, at, {to:'down', dur:.45, stagger:.04}) power4.inOut, visibility hidden at +0.3 s. Projects tune dur 1.1 / stagger 0.12 / ease settle. Plain-JS twin (kinetic_2d): start_i = 0.3 + 0.22·i s, p = clamp((t − start)/0.7), ease = 1 − (1 − p)³, translateY((1 − ease)·100%); remove CSS transitions before capture; highlight word #f59e0b + text-shadow 0 0 35px rgba(245,158,11,.6). **أرقام / params:** reveal 0.7 s / 0.07 s expo.out; hide 0.45 s / 0.04 s power4.inOut; yPercent ±115.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:156` · `kosif-studio/motion/kit/motion-kit.js:129` · `100-superskills/skills/kosif-montage-motion/templates/motion/title-card.html` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:111`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-20 · صعود الكلمات من الضباب · Rise-from-blur words · 🟢 جاهز / ready
- **ماذا / what:** الكلمات تبدأ من حالة جزئية — شفافية 40%، أسفل قليلًا، ضبابية — ثم تستقر بسرعة؛ أنعم من القناع. — Words start partial — 40% opacity, slightly low, blurred — and settle fast; softer than a mask.
- **متى أستخدمها / when:** سطور شرح وسرد هادئ ولوحات بيانات — explainer lines, calm narration, data labels.
- **كيف / how:** MOTION.riseWords(tl, el, at, {rise:26, blur:6, dur:.4, stagger:.1}) with E.out; projects use 30–40 px / 0.55–0.6 s / stagger 0.1–0.12 (water labels 0.8 s, stagger 0.05, power4.out). Infographic line variant: overflow:hidden container, inner translateY 70%→0 + blur 6→0 px, 450 ms, 80 ms per line, fast-in slow-out, small grey eyebrow above a bold white headline. Rounded-face brief: 24→0 px in 240 ms, 60 ms stagger at 72 px. **أرقام / params:** y 26→0 px; opacity .4→1; blur 6→0; 0.4 s; stagger 0.1 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:175` · `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:70` · `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:174-182` · `style:infographic`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-21 · مسح القناع من اليمين · RTL clip wipe · 📄 موصوف / documented only
- **ماذا / what:** الكلمة مكتملة التشكيل تنكشف من اليمين إلى اليسار بقصّ clip-path — كتابة بلا كسر للحروف. — A fully shaped word is uncovered right-to-left by a clip-path — writing without breaking letters.
- **متى أستخدمها / when:** كلمة كبيرة واحدة، أو سطر يُكتب بإيقاع القراءة — a single big word or a line written at reading pace.
- **كيف / how:** clip-path inset(0 0 0 100%) → inset(0 0 0 0) in 350–600 ms ease-out quart (recipe B: 500 ms); big-word recipe: a 200 px word wiped in over 450 ms, held 1 s, wiped out the same direction in 250 ms; Canvas: draw the word offscreen and grow a ctx.rect clip from the right; long words from words.json may fill right→left across their spoken duration. **أرقام / params:** 350–600 ms; ease-out quart cubic-bezier(.25,1,.5,1).

```css
.wipe{clip-path:inset(0 0 0 100%);
  animation:wipe .5s cubic-bezier(.25,1,.5,1) forwards}
@keyframes wipe{to{clip-path:inset(0 0 0 0)}}   /* right side appears first */
```

- **الدليل / proof:** `kosif-tool/playbooks/arabic-typography.md:26` · `kosif-tool/playbooks/kinetic-type.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md` · `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### ARAB-22 · كتابة بقناع ناعم ورأس قلم · Feathered RTL write-on with pen head · 📦 بأمر تثبيت / one install
- **ماذا / what:** الكلمة تظهر من اليمين بحافة ناعمة، وقلم أو ماركر يتبع الحافة كأنه يكتبها بيده. — A word appears from the right behind a soft edge while a pen or marker rides the edge as if writing it.
- **متى أستخدمها / when:** سبورة، طباشير، دفتر، شرح تعليمي — whiteboard, chalk, notebook explainers.
- **كيف / how:** Basma TX.reveal(c, x0, x1, y0, y1, k, rtl, paint): clip up to the edge, then 6 thin slices with falling alpha form a feather of max(6 px, 8% width); it returns the edge x for the pen sprite. HTML (whiteboard reference): keep the text as HTML, mask-image linear-gradient(to left, #000 X%, transparent X+4%), X 0→100 over ~0.6 s per word, marker tip on the mask edge, 2° wiggle for 150 ms when a word completes. Chalk variant: chalk sprite takes the stroke colour, dust particles spawn at the last ~14 tip positions and fade in ~0.5 s. **أرقام / params:** feather max(6 px, 8%); 6 slices; ~0.6 s per word; wiggle 2° / 150 ms.

```js
// p: 0..1 across the word; returns the pen x (viewport px)
function writeOn(el, p) {
  const x = p * 104;                       // 4% feather
  const m = `linear-gradient(to left, #000 ${x - 4}%, transparent ${x}%)`;
  el.style.maskImage = el.style.webkitMaskImage = m;
  const r = el.getBoundingClientRect();
  return r.right - p * r.width;            // marker follows the edge
}
```

- **الدليل / proof:** `app/public/js/10_studio.js:194` · `kosif-tool/playbooks/hand-drawn.md:75` · `kosif-tool/styles/handwriting-reveal/SKILL.md` · `style:whiteboard`
- **📦 تثبيت / install:** `cd app && npm install`

#### ARAB-23 · قناع ضربة فرشاة · Brush-stroke mask write-on · 📄 موصوف / documented only
- **ماذا / what:** ضربة فرشاة SVG تُرسم وتعمل قناعًا يكشف عبارة مكتملة من اليمين إلى اليسار. — An SVG brush stroke draws on and acts as a mask that uncovers a finished phrase right-to-left.
- **متى أستخدمها / when:** عناوين فنية، أفلام الخط والتراث — artistic titles, calligraphic/heritage films.
- **كيف / how:** SVG <mask> holding a thick round-cap brush path (pathLength=1, stroke-dasharray 1, stroke-dashoffset 1→0) drawn from right to left over the intact text; 0–0.5 s start, 0.5–2.5 s reveal, 2.5–4 s read. **أرقام / params:** 4 s total; reveal 2 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md` · `kosif-tool/playbooks/hand-drawn.md:75`

#### ARAB-24 · سطور تصعد من خلف خط قطع · Lines rising behind a cut line · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل سطر من عنوان ثلاثي يصعد من خلف خط قطع غير مرئي بتأخير محسوب. — Each line of a three-line title rises from behind an invisible cut line with a measured delay.
- **متى أستخدمها / when:** اقتباسات وعناوين متعددة الأسطر — quotes and multi-line titles.
- **كيف / how:** One overflow:hidden wrapper per line, inner translateY 100%→0; reveal 0–1.2 s, read 1.2–2.6 s, out 2.6–3 s. quote-card template: quote mark springs in, lines split by '|' (≤6) rise .22 s apart, accent bar, author rises last. Give the wrapper extra line-height so dots are not clipped (ARAB-05). **أرقام / params:** 3 s cycle; line stagger .22 s; quote 6.4u.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/motion/quote-card.html` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:45` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-25 · انزلاق سطور عربية على Canvas · Canvas RTL staggered line slide · 🟢 جاهز / ready
- **ماذا / what:** نص المشهد يُلفّ إلى ≤4 أسطر عربية تنزلق من اليمين وتظهر تباعًا — بلا أي مكتبة. — Scene text wraps to ≤4 Arabic lines that slide in from the right one after another — no library.
- **متى أستخدمها / when:** مشاهد Canvas خفيفة ومولدات سريعة — lightweight canvas scenes and quick generators.
- **كيف / how:** splitArabic(text, maxChars) greedy by whole words (16 chars vertical / 26 horizontal, default 18), slice(0,4); ctx.direction='rtl'; font '700 {w·.074 | w·.051}px …'; centre y = 0.68h; line height 1.25em; per line a = clamp(4p − 0.18k), x offset (1 − easeOutCubic(a))·0.4w; maxWidth 0.9w; shadow #0b1228 blur 0.03w. The source uses Tahoma — swap in Cairo after the font gate. **أرقام / params:** ≤4 lines; stagger 0.18 of progress; slide 40% width.
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:3`

#### ARAB-26 · عنوان كلمات بنابض كل 160 مللي ثانية · Spring word-stagger title · ✅ مُثبت هنا / proven here
- **ماذا / what:** عنوان عربي من كلمات كاملة تصعد 70 بكسل وتكبر 0.92→1 بنابض، كلمة كل 160 ms، ثم تخرج معًا. — Whole Arabic words rise 70 px and scale 0.92→1 on a spring, 160 ms apart, then exit together.
- **متى أستخدمها / when:** افتتاح أي فيلم HTML من الكتالوج — the default opener in catalog HTML films.
- **كيف / how:** Per word a = 0.25 + 0.16·i s; prog(t, a, a + 0.55, spring 170/16); exit prog(t, 3.0, 3.35, inBack) translateY −60; Cairo 900 128 px, lh 1.25, gap 28 px, accent word #7ee8d2. Playbook twin (Remotion ArabicTitle): p = (frame − 4i)/12 → translateY (1 − p)·50; recipe A: rise 50 px over 400 ms ease-out quint, 120 ms stagger, key word 700–980 ms → accent + scale 1.08 spring 12/180; Cairo 900 140 px lh 1.3. **أرقام / params:** stagger 160 ms; spring 170/16; exit 3.0–3.35 s inBack.
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:139` · `kosif-tool/playbooks/arabic-typography.md:35-63`

#### ARAB-27 · عنوان Remotion بنابض وأقراص كلمات · Remotion spring title + keyword pills · 📦 بأمر تثبيت / one install
- **ماذا / what:** خط لوني ينمو إلى 180 بكسل، ثم كلمات العنوان تقفز كل 5 إطارات، ثم أقراص الكلمات المفتاحية كل 4 إطارات. — An accent rule grows to 180 px, title words spring in every 5 frames, keyword pills every 4.
- **متى أستخدمها / when:** أفلام React/Remotion قابلة للتحرير بالـ props — editable React/Remotion films driven by props.
- **كيف / how:** Title: spring damping 14, stiffness 120, mass .9, rise 80 px, scale .85→1, staggerStart(i, 5, 6); pills: damping 12, stiffness 150; title 112 px 800 lh 1.3 #f4f1ea; pills 40 px 600, padding 12×30, radius 999, border 3 px accent@.9, bg accent@.14; chart/axis numbers via Intl.NumberFormat(lang === 'ar' ? 'ar-EG' : 'en-US'). **أرقام / params:** title every 5 frames; pills every 4 frames.
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Film.tsx:130` · `kosif-tool/starters/remotion/src/Film.tsx:303`
- **📦 تثبيت / install:** `cd kosif-tool/starters/remotion && npm ci`
- **⚖️ ترخيص / license:** Remotion: مجاني للأفراد والشركات الصغيرة، والشركات الأكبر تحتاج رخصة شركة / free for individuals and small companies; larger companies need a Remotion company license (pinned 4.0.535).

#### ARAB-28 · دخول الكلمة من العمق · 3D word turn-in from depth · 🟢 جاهز / ready
- **ماذا / what:** كل كلمة تنقلب واقفة من العمق (rotationX) مع انقشاع الضباب وظل ناعم. — Each word tips up from depth (rotationX) as blur clears, with a soft shadow.
- **متى أستخدمها / when:** أفلام القصائد والأدعية والأغاني — verse, dua and song films.
- **كيف / how:** GSAP from y 46k, z −220, rotationX −78, transformPerspective 900, transformOrigin 50% 100%, blur 10 px → 0; 0.62 s back.out(1.4) starting 0.1 s before the word's time; drop-shadow 0 5px 12px rgba(0,0,0,.65). The whole word turns, so shaping is never at risk. Render: node kosif-tool/tools/render_html.cjs --in index.html --out x.mp4 --mode virtual. **أرقام / params:** rotationX −78°; z −220; perspective 900; 0.62 s back.out(1.4).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/verse.html:222`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-29 · الآلة الكاتبة بمؤشر · Typewriter with caret · 🟢 جاهز / ready
- **ماذا / what:** النص يُكتب بامتداد السلسلة نفسها فيعيد المتصفح تشكيل البادئة كل إطار، تمامًا كالكتابة على لوحة المفاتيح. — Text grows as a string so the browser reshapes the prefix each frame — exactly like keyboard typing.
- **متى أستخدمها / when:** مربعات الأوامر والبحث والدردشة داخل الفيلم — prompt, search and chat boxes on screen.
- **كيف / how:** MOTION.typeOn(tl, el, text, at, {cps:46, caret:true, hold:1}): dur = clamp(len/cps, 0.5, 1.2) s, writes text.slice(0, n) + '|', caret blinks at 2 Hz while held; projects use cps 22–46, hold 0.5–0.6 s. Arabic-safe because it never wraps letters in spans; the last letter shows its final form until the next arrives. For tashkeel-heavy text step by grapheme (Intl.Segmenter) so a harakah never appears alone. **أرقام / params:** cps 22–46; dur 0.5–1.2 s; caret 2 Hz.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:193` · `kosif-studio/motion/projects/showreel/index.html:74`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-30 · كلمة ضخمة من الضباب تنكمش إلى سطر · Blur-in hero word that shrinks into the sentence · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الكلمة الأولى تدخل ضخمة من ضبابية ثم يصغر حجمها لتصير أول جملة تتوالى كلماتها. — The first word lands huge out of blur, then shrinks to become the start of a sentence whose words follow.
- **متى أستخدمها / when:** إطلاق منتج وكلمة وعد واحدة — product launches and one-word promises.
- **كيف / how:** Build: word1 opacity 0→1, blur 20→0 px, scale 1.1→1 in 0.5 s; then animate font-size ~22% → ~7% of frame height over 0.6 s ease-in-out (font-size re-shapes cleanly; never scaleX) while words 2..n enter 180 ms apart with cubic-bezier(.22,1,.36,1); exit = blur + translateX 40 px toward the line end. **أرقام / params:** blur 20 px; stagger 180 ms; size 22%→7% H.
- **الدليل / proof:** `style:product` · `kosif-tool/styles/product`

#### ARAB-31 · كبسولة الكلمات الدوّارة · Rolling word pill with growing rings · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كبسولة تتدحرج فيها الكلمات عموديًا (أيام ← ساعات ← دقائق) وحلقات خلفها تكبر مع كل خطوة. — Words roll vertically inside a pill (days → hours → minutes) while rings behind it grow each step.
- **متى أستخدمها / when:** مقارنة سرعة أو توفير وقت — speed or time-saving claims.
- **كيف / how:** Build: pill overflow:hidden; stacked words translateY −100% per step, ease-out 0.4 s; concentric pill outlines behind grow +40 px per step (3 steps), soft purple shadow. **أرقام / params:** 3 steps; +40 px per ring; 0.4 s.
- **الدليل / proof:** `style:product`

#### ARAB-32 · كشف بالحبر وسحب التركيز · Ink-bleed / focus-pull word reveal · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل كلمة تتجسد من ضبابية خفيفة كأن الحبر يتشربها، والكلمة السابقة ما زالت تنقشع. — Each word condenses from a light blur like ink bleeding in while the previous one is still clearing.
- **متى أستخدمها / when:** شعر وأغانٍ هادئة على مشهد طبيعي — calm poetry and songs over landscapes.
- **كيف / how:** Per word: opacity 0→1 + blur 4 px→0 + scale 0.96→1 in 200–300 ms with 80% overlap to the next; on vocal onset (words.json) the incoming word sharpens while the trailing one is still soft; colour adapts to background brightness (dark ink on bright sky, white on dark). Seen per character (CJK) and per word (Latin lyric); for Arabic it is per word only. **أرقام / params:** 200–300 ms per unit; 80% overlap; blur 4 px.
- **الدليل / proof:** `style:pm-demitiyageekzen-7770ad` · `style:pm-samaote-5e2fc2` · `kosif-tool/styles/pm-samaote-5e2fc2/BRIEF.md`

#### ARAB-33 · كلمات على مسار دائري · Words on a circular path · 📄 موصوف / documented only
- **ماذا / what:** عبارة تدور ببطء حول منتج أو شمس ثم تتوقف والجزء المقروء في الأعلى. — A phrase circles a product or sun slowly and stops with the readable part on top.
- **متى أستخدمها / when:** ختم أو شعار دائري أو أغنية حول عنصر مركزي — seals, round badges, songs around a central object.
- **كيف / how:** 0–1 s appear, 1–3.5 s rotate, 3.5–5 s stop; place whole Arabic words by angle (each word its own rotated element) instead of per-glyph textPath; keep the rotation slow. Reference: words placed along an arc around the sun in a synced Latin lyric film. **أرقام / params:** 5 s loop.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

## التوكيد والكلمة البطلة — Emphasis & hero words

_كيف تجعل كلمة واحدة تضرب._

#### ARAB-34 · ضربة الكلمة المفتاحية بقناع صاعد · Keyword slam with upward mask · 🟢 جاهز / ready
- **ماذا / what:** الكلمة المنبورة تهبط بثقل: أصغر قليلًا، منخفضة، ضبابية، يكشفها قناع ينفتح للأعلى فتستقر حادة في ثلث ثانية. — The stressed word lands with weight: slightly small, low and blurred, uncovered by an upward-opening mask, sharp in a third of a second.
- **متى أستخدمها / when:** الكلمة المفتاحية في كل جملة منطوقة — the keyword of each spoken line.
- **كيف / how:** slam(el, at, {from, y, blur, dur, ease, tail}): fromTo {opacity 0, scale .94, y 24·k, filter blur(10px), clipPath inset(100% −10% −45% −10%)} → {opacity 1, scale 1, y 0, blur 0, clipPath inset(−25% −10% −45% −10%)} in 0.34–0.36 s expo.out; keyword size 200·k, weight 700. Variants: from 1.12 / blur 14 / 0.18 s for a sharp 'إطلاقاً', blur 16 / 0.24 s for 'في الفعل'. Pick the word with ARAB-68. **أرقام / params:** scale .94→1; y 24k; blur 10→0; 0.34 s expo.out.
- **الدليل / proof:** `kosif-studio/motion/templates/directed.html` · `100-superskills/skills/kosif-montage-motion/templates/directed.html:82` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:182`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-35 · كلمة ترتطم وتستقر · Slam-and-settle word · 📄 موصوف / documented only
- **ماذا / what:** الكلمة تسقط أبعد قليلًا من مكانها، ترتد مرة واحدة ثم تثبت — افتتاح إعلاني بثقل. — The word drops slightly past its slot, rebounds once and locks — a weighty ad opener.
- **متى أستخدمها / when:** أول كلمة في إعلان أو خطاف — the first word of an ad or hook.
- **كيف / how:** 0–0.4 s drop past the slot, 0.4–0.8 s one rebound (back.out(1.6) or cubic-bezier(.34,1.56,.64,1)), 0.8–2 s read; animate the word block (translateY + scale), never letters; one muted thud SFX on contact. **أرقام / params:** 2 s; overshoot back.out 1.6.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### ARAB-36 · ضربة الكلمة البطلة بتوهج · Hero-word punch with bloom · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كلمة عربية ثقيلة بحجم 40% من ارتفاع الإطار تضرب للداخل من تكبير وضباب مع هالة متوهجة. — A heavy Arabic word at ~40% of frame height punches in from scale and blur with a glowing halo.
- **متى أستخدمها / when:** ذروة الفكرة أو الكلمة الأقوى في المقطع — the climax word.
- **كيف / how:** Build: weight 900, ~40% of frame height; scale 1.15→1 and blur 8→0 px in 300 ms; glow = a duplicate of the word blurred 20 px at 40% opacity (white or orange #f27525) behind it. Climax variant: a giant glyph/word with a fire-texture glow, fade in 300 ms, hold 1 s. **أرقام / params:** 300 ms; glow copy blur 20 px @40%.
- **الدليل / proof:** `style:plotter` · `style:pm-chrisjdimarco-f068db`

#### ARAB-37 · الكلمة تمثّل معناها · Word acts out its meaning · 📄 موصوف / documented only
- **ماذا / what:** كلمة واحدة تؤدي معناها — «توسّع» تتسع، «سقوط» تسقط — والجملة ثابتة حولها. — One word performs its meaning — 'expansion' widens, 'fall' drops — while the sentence holds still.
- **متى أستخدمها / when:** أفعال وصفات قوية في السرد — strong verbs and adjectives.
- **كيف / how:** MG-014: 0–0.6 s sentence, 0.6–1.5 s the word acts, 1.5–3 s read. Widen with uniform scale of the whole block or kashida/wdth, never scaleX; drop, shake or blur the word block. The reference showreel used squash/stretch, overshoot springs, motion blur and chromatic split on Latin words — for Arabic apply them to the whole word only. **أرقام / params:** 3 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### ARAB-38 · صدى طباعي يتلاشى · Typographic echo · 📄 موصوف / documented only
- **ماذا / what:** ثلاث نسخ متأخرة تلاحق الكلمة ثم تلتقي عليها وتختفي، فتمنح العنوان طاقة. — Three delayed copies trail a word, converge on it and vanish, energising the headline.
- **متى أستخدمها / when:** كلمة عنوان تحتاج طاقة بلا ألوان إضافية — a headline word needing energy without new colours.
- **كيف / how:** 3–5 clones with delayed transforms and opacity 0.6→0.1; 0–0.7 s push, 0.7–1.2 s copies converge on the master, 1.2–2.5 s read; the master stays crisp and high-contrast; short tail-pulse SFX. **أرقام / params:** 2.5 s; 3 echoes; opacity 0.6→0.1.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### ARAB-39 · تعبئات مذهّبة ومتدرجة ولمعة عابرة · Gilded, gradient & sweeping fills · 🟢 جاهز / ready
- **ماذا / what:** التدرج يملأ الحروف (background-clip:text) على الكلمة المشكّلة كاملة — ذهبي للفخامة، سماوي للتقني، ولمعة تمر على كلمة الذروة. — Gradients fill the glyphs of the whole shaped word — gold for luxury, sky for tech, a light sweep across the payoff word.
- **متى أستخدمها / when:** عناوين فخمة، أدعية ليلية، إطلاق تقني — luxury titles, night duas, tech launches.
- **كيف / how:** -webkit-background-clip:text + -webkit-text-fill-color:transparent on the word element (table). Light sweep: background-size 300% and animate background-position across the payoff word once. **أرقام / params:** see table.

| الوصفة / recipe | التدرج / gradient | إضافات / extras |
|---|---|---|
| كلمات مذهبة / gilded words | 180deg #FFFDF6 → #F7EBD0 55% → #E9D3A4 | keywords #FFF1BF → #F4C766 45% → #C98A2B |
| خطاف ذهبي / gold hook | 180deg #FFF7E2 → #F6C76B 55% → #E08A2E | drop-shadow 0 0 28px rgba(246,199,107,.55) + 0 0 80px rgba(255,140,60,.35); Cairo 900 210 px |
| سينمائي سماوي / cinematic sky | 135deg #fff → #cbd5e1 50% → #38bdf8 | drop-shadow 0 4px 20px rgba(0,0,0,.8); 72 px 900; fades up 40 px over 1.5 s |
| لمعة عابرة / light sweep | 300% gradient band | background-position sweep on the payoff word (premium edit) |

- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/cinematic_3d.html:51` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:37` · `kosif-one/projects/egypt-2120-animation/index.html:8-29` · `kosif-studio/motion/projects/premium_edit/index.html:8`

#### ARAB-40 · هرمية بثلاث مستويات · Three-level type hierarchy · 🟢 جاهز / ready
- **ماذا / what:** الكلام صغير، العبارة متوسطة، الكلمة المفتاحية ضخمة — فتعرف العين ماذا تقرأ أولًا. — Speech small, phrase medium, keyword huge — the eye knows what to read first.
- **متى أستخدمها / when:** مونتاج صوتي وريلز شرح — voice-led edits and explainer reels.
- **كيف / how:** Premium edit (1080×1920, one family 300/500/700): .l1 speech 54 px/500 at y 1452; .l2 phrase 96/700 at 1236; .l3 keyword 220/700 at 1196; an extreme word at 400 px doubles as a transition plane; payoff 250 px; soft 300-weight line at 150 px; credit 25 px/300 at 48% alpha; ivory text with double shadow 0 3px 16px .45 + 0 1px 2px .35; words land on their syllables. Explainer variant: captions 50 px at y 1400, keywords 48–150 px in the upper half (y 330–1220), section chips 40 px (ARAB-54). **أرقام / params:** 54 / 96 / 220 px (+400 plane).
- **الدليل / proof:** `kosif-studio/motion/projects/premium_edit/index.html:8` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:24` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:28-40` · `kosif-studio/out/FINAL_EDIT/EDIT_NOTES.txt`
- **⚖️ ترخيص / license:** المشروع الأصلي يستخدم Dubai (مملوك) — استبدله بـ Cairo/Tajawal عند الشحن؛ GSAP مدمج / original uses proprietary Dubai — swap to Cairo/Tajawal for shipping; GSAP vendored (standard no-charge license).

#### ARAB-41 · تمييز الكلمة بالنجمة · *Asterisk* emphasis convention · 🟢 جاهز / ready
- **ماذا / what:** المستخدم أو Claude يضع *نجمتين* حول كلمة واحدة في السطر، وكل ترجمة وستايل يقرأها فيلوّنها أو يضيئها. — The user or Claude wraps one word per line in *asterisks*; every caption and style reads it to colour or glow that word.
- **متى أستخدمها / when:** كتابة السكربت قبل الرندر — when writing the script.
- **كيف / how:** MK.mkLine/parseScript split lines, strip [brackets] and '...', keep {w, em}; drawCaptions/capWords render a *word* in the accent colour at 1.1× scale; one starred word per line. **أرقام / params:** 1 starred word per line; accent + 1.1× scale.
- **الدليل / proof:** `app/public/js/10_studio.js:44` · `app/public/js/10_studio.js:57` · `app/public/js/00_editor.js:345`

#### ARAB-42 · خط متموّج تحت الكلمة المفتاحية · Squiggle underline highlight · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الكلمة المفتاحية تتلون برتقاليًا بتوهج دافئ، وتحتها خط موجي مرسوم باليد يتماوج ببطء. — The keyword turns orange with a warm glow over a hand-drawn sine underline that slowly phase-shifts.
- **متى أستخدمها / when:** أفلام الدودل والقصص المصورة — doodle and storybook films.
- **كيف / how:** Build: key word #f07f2e, glow #ffd0a0 blur 12 px; SVG sine underline amplitude 3 px, period 18 px, drawn right→left under the Arabic word, phase shifted slowly (rebuild d per frame). **أرقام / params:** #f07f2e; glow #ffd0a0 12 px; amp 3 px; period 18 px.
- **الدليل / proof:** `style:doodle` · `kosif-tool/styles/doodle`

#### ARAB-43 · ممسحة التظليل من اليمين · RTL highlighter swipe · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مستطيل أصفر مستدير يتمدد خلف الكلمة المفتاحية من اليمين إلى اليسار كقلم تظليل. — A rounded yellow bar grows behind the keyword from the right like a highlighter.
- **متى أستخدمها / when:** عناوين الشرح والكوميديا التعليمية — explainer and comedy titles.
- **كيف / how:** Build: rounded rect behind the key word, #f2c94c at 70%, height 35% of the text, width 0→100% with transform-origin right under a bold title. Slanted variant: a skewed teal bar wipes in behind the key line while earlier lines dim (ARAB-48). **أرقام / params:** #f2c94c @70%; height 35%.
- **الدليل / proof:** `style:stickman` · `style:pm-deifosv-04e4d3`

#### ARAB-44 · ختم أحمر يرتطم · Rubber-stamp slam · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ختم نصي أحمر مائل يرتطم بالبطاقة مع صوت ختم واهتزاز صغير. — A tilted red text stamp slams onto the card with a stamp sound and a micro shake.
- **متى أستخدمها / when:** قاعدة، حكم، «افعلها الآن» — rules, verdicts, calls to act.
- **كيف / how:** Build: red outlined text box #eb5757, border 4 px, rotated ≈ −4°, scale 1.6→1 with slight overshoot and opacity 0→1 in ~200 ms, synced to a stamp SFX and a micro camera shake. **أرقام / params:** #eb5757; 4 px; −4°; 1.6→1; ~200 ms.
- **الدليل / proof:** `style:stickman`

#### ARAB-45 · علامة استفهام عملاقة مفرّغة · Giant outlined question mark · 🟢 جاهز / ready
- **ماذا / what:** «؟» مجوّفة عملاقة ترتطم دائرةً خلف السؤال، تستقر ثم تخفت وتنكمش. — A huge hollow '؟' slams in rotated behind the question, settles, dims and implodes.
- **متى أستخدمها / when:** مشاهد السؤال والتشويق — question and suspense beats.
- **كيف / how:** '؟' (U+061F) 420 px, color transparent, -webkit-text-stroke 3px #f5c97a; from scale 2.4, rotation −12, opacity 0 → 1 in 0.7 s E.out; fill eases to rgba(245,201,122,.18); out: scale .2 in 0.25 s E.in. MK.lineMeta flags questions so a style can trigger it (ARAB-75). **أرقام / params:** 420 px; stroke 3 px #f5c97a; 0.7 s in / 0.25 s out.
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:39-40` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:218-221`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-46 · ظل مزدوج مزاح · Offset duotone shadow hero · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كلمة كبيرة بالخط المحلي خلفها نسختان مزاحتان بالوردي والأزرق. — A big native-script word with two offset copies in pink and blue behind it.
- **متى أستخدمها / when:** تاريخ وثقافة وهوية بطابع بوستر — history and culture films with a poster feel.
- **كيف / how:** Build: render the word large; two duplicates behind offset 6–10 px (8 px default) in pink and blue; fade/slide the stack in. Seen with Devanagari; for Arabic keep each copy a whole word. **أرقام / params:** offset 8 px; 2 colours.
- **الدليل / proof:** `style:pm-buildfastwithai-53234e`

#### ARAB-47 · خط مضيء يتمدد تحت العنوان · Growing glow rule under the title · 🟢 جاهز / ready
- **ماذا / what:** بعد هبوط العنوان العربي يتمدد تحته خط رفيع متوهج ثم يتبعه سطر فرعي. — After the Arabic title lands, a thin glowing rule grows beneath it, then a subtitle follows.
- **متى أستخدمها / when:** بطاقات عنوان هادئة وليلية — calm and night title cards.
- **كيف / how:** #rule height 3 px, background #e0a35a, box-shadow 0 0 14px; tl.fromTo(rule, {width:0}, {width:240, duration:1.1, ease:'power4.out'}, T + 0.35); title 92 px/800 right-aligned, sub 34 px/600 at T + 0.45; titleAt 1.7 s; anchor the rule on the right (transform-origin right) for RTL. **أرقام / params:** 3 px #e0a35a; 0→240 px in 1.1 s power4.out.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/index.html:18` · `100-superskills/skills/kosif-montage-motion/scripts/projects/night_boat/index.html:61`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-48 · سطور تتكدس وتخفت · Stacked headline lines that dim · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سطر عنوان مع كل نبضة؛ الجديد بكامل لونه والسابق يخفت إلى رمادي 40%. — One headline line per beat; the new one in full colour while earlier lines dim to ~40% grey.
- **متى أستخدمها / when:** تريلرات وإعلانات على الإيقاع — trailers and beat-driven ads.
- **كيف / how:** Build: lines stack one per beat (from the right for Arabic); each new line enters at full colour while the earlier ones tween to ~40% grey; two-tone headlines (cream + lime); the key line sits on a slanted highlighter bar (ARAB-43). **أرقام / params:** earlier lines → 40%.
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

## العناوين والبطاقات والقوالب — Titles, cards & templates

_قطع جاهزة تُركّب في دقائق._

#### ARAB-49 · قوالب الموشن العربية الثمانية · Eight Arabic motion templates · ✅ مُثبت هنا / proven here
- **ماذا / what:** ثمانية قوالب HTML/GSAP حتمية تتحول بأمر واحد إلى مشروع قابل للتعديل بخط Cairo وأقنعة كلمات. — Eight deterministic HTML/GSAP templates that become an editable Cairo/word-mask project with one command.
- **متى أستخدمها / when:** عنوان، شريط اسم، اقتباس، عدّ، ختام، نقاط، رقم، شعار — كلها في دقائق / quick branded pieces.
- **كيف / how:** python scripts/mtemplates.py list | show NAME | new PROJECT --template NAME --set key=value … [--seconds S --size 1080x1920 --fps 30] → projects/PROJECT/index.html + assets (fonts, gsap, motion-kit); text is HTML-escaped and colours validated (#RRGGBB); render with motion.py render or kosif-tool/tools/render_html.cjs --mode virtual. Also from the web studio ('قالب موشن…'), MCP kosif_project_create {kind:'template'}, GET /api/templates. title-card, lower-third and quote-card are tested; the rest are code. **أرقام / params:** see table.

| القالب | ما يفعله / what it does | المدة | لكنة · خلفية |
|---|---|---|---|
| title-card | word-mask title + second line + pen-drawn rule + push 1.0→1.06, halo, 34 sparkles, landing flash .62 s; Cairo 800 9.5u / 600 4.2u; vignette .38, grain .05 | 6 s | #E7B65A · #1b2a49→#0d1b2a |
| lower-third | name + role in the lower safe band (20% H portrait, 12% landscape), RTL on the box only | 6 s | #E7B65A · #22313f→#0b141c |
| quote-card | quote mark springs, lines (split by \|, ≤6) rise .22 s apart, author last | 7 s | #F2C879 · #2b1e3a→#120a1e |
| countdown | jumps and pulses from ≤10 (default 5) to 'انطلق' | — | #FF6B6B · #1a1a2e→#0b0b14 |
| end-card | 'تابعنا للمزيد' + @handle + icons in sequence + progress bar | 6 s | #E7B65A · #1b2a49→#0d1b2a |
| bullet-list | title + up to 6 items, a check drawn for each | 8 s | — |
| stat-counter | number counts up + ring draws + label | — | — |
| logo-reveal | logo pen-drawn, fills, then name + tagline | — | — |

- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:35` · `100-superskills/skills/kosif-montage-motion/templates/motion/title-card.html` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:14` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:127`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-50 · شريط اسم سفلي تلقائي الاتجاه · Auto-RTL lower third · ✅ مُثبت هنا / proven here
- **ماذا / what:** بطاقة اسم ووظيفة في المنطقة الآمنة السفلية؛ تكتشف العربية فتنقل الجانب وتقلب الاتجاه على الصندوق فقط. — Name + role card in the lower safe area; detects Arabic, flips side, and applies RTL to the box only.
- **متى أستخدمها / when:** مقابلات، متحدثون، تعريف شخص — interviews and speaker IDs.
- **كيف / how:** MOTION.lowerThird(tl, root, at, {title, sub, accent, size, inset, bottom, barWidth, side, hold, font}): accent bar 4 px #E7B65A grows to 120 px in 0.4 s; title 44 px bold at +0.12 s; sub 0.55× size rgba(255,255,255,.75) at +0.24 s; inset 72 px, bottom 160 px; exit 0.3 s. Timeline JSON equivalent: overlays type lower-third {title, sub, accent}. **أرقام / params:** bar 4×120 px; title 44 px; sub 55%; in .4/.5 s; out .3 s.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:562` · `100-superskills/skills/kosif-montage-motion/templates/motion/lower-third.html` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:39` · `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT).

#### ARAB-51 · ثلاثة أشكال لعنوان الخطاف · Hook title looks: box · kinetic · minimal · 📦 بأمر تثبيت / one install
- **ماذا / what:** عنوان يظهر في أول 3 ثوانٍ بأحد ثلاثة أشكال: صندوق ينزلق، كلمات تدق، أو سطر هادئ بخط تحتي. — A hook title for the first 3 s in one of three looks: sliding box, stomping words, or a minimal line with an underline.
- **متى أستخدمها / when:** أول 3 ثوانٍ من أي ريل — the first 3 seconds of a reel.
- **كيف / how:** drawTitle(): box = easeBack slide from +0.6W over 0.45 s, Lalezar at 8.5% of the short side on a rounded primary box; kinetic = Lalezar 12%, each word stomps from scale 2.3 (1 + 1.3) to 1 over 0.18 s, 0.16 s apart, black stroke, alternating accent; minimal = IBM Plex Sans Arabic 700 at 6%, ease-out rise 0.6 s, accent underline grows from the right over 0.8 s; all fade out 2.65–3 s. **أرقام / params:** visible 0–3 s; fade 0.35 s.
- **الدليل / proof:** `app/public/js/00_editor.js:318`
- **📦 تثبيت / install:** `cd app && npm install`

#### ARAB-52 · صندوق عنوان يحافظ على مركزه · Centre-locked resizing title box · 📄 موصوف / documented only
- **ماذا / what:** عبارة قصيرة تُستبدل بأطول بينما الصندوق خلفها يتمدد بنعومة حول مركز ثابت. — A short phrase swaps for a longer one while its box stretches smoothly around a fixed centre.
- **متى أستخدمها / when:** تبديل كلمة ضمن نفس الإطار — swapping a word in place.
- **كيف / how:** 0–1 s first phrase, 1–2 s swap + resize, 2–4 s second phrase; measure the real shaped text (getBBox / measureText after the font gate) and tween the rect width to it; test the longest string; leave margin for tashkeel; RTL anchor = centre. **أرقام / params:** 4 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### ARAB-53 · ترويسة اليوم بالهجري والميلادي · Hijri + Gregorian day header · 🟢 جاهز / ready
- **ماذا / what:** اسم اليوم بخط خطاطي كبير، وفوقه الشهر الهجري وتحته التاريخ الميلادي مع خطين ذهبيين يُرسمان. — A big calligraphic day name with the Hijri month above, the Gregorian date below and two drawn gold rules.
- **متى أستخدمها / when:** منشورات يومية وجمعة ودعاء — daily, Friday and dua posts.
- **كيف / how:** #day 170 px #ffe7a8 with glow, blur-in (y 46, scale .92, blur 10 px → 0) at 0.25 s; #month Amiri Bold 54 px #f4cf6b via revealWords ('ربيع الثاني ٢٧'); #date Amiri Bold 50 px LTR, letter-spacing 3 px on the Latin digits only ('08 . 10 . 2026'); two gold rules drawn at 0.8 / 0.95 s. Hijri text from Intl.DateTimeFormat('ar-SA-u-ca-islamic-umalqura', {day:'numeric', month:'long'}). **أرقام / params:** day 170 px; month 54 px; date 50 px; rules at 0.8/0.95 s.
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html:18-21` · `kosif-one/projects/thursday-dua-animation/source/index.html:95-101` · `kosif-one/projects/thursday-dua-animation/source/index.html:190-194`
- **⚖️ ترخيص / license:** اسم اليوم بخط Aldhabi (خط ويندوز مملوك لمايكروسوفت) — محلي فقط؛ للشحن استخدم Aref Ruqaa أو Amiri (OFL)؛ GSAP مدمج / Aldhabi is a Microsoft Windows font — local only; ship with Aref Ruqaa/Amiri; GSAP vendored.

#### ARAB-54 · أقراص وشارات وأرقام مرقّمة · Pills, chips & numbered badges · 🟢 جاهز / ready
- **ماذا / what:** شارات صغيرة تنبثق، رقائق أقسام، ودوائر زجاجية بأرقام هندية — طبقة التنظيم فوق المشهد. — Pop-in tags, section chips and frosted badges with Arabic-Indic numerals — the organising layer over a scene.
- **متى أستخدمها / when:** مراحل الشرح، أقسام الفيديو، تسميات العالم — explainer stages, section labels, world tags.
- **كيف / how:** Tag pill: padding 10×24 px, 24 px/800, radius 8, gradient 135deg #f59e0b → #d97706, shadow 0 10px 25px rgba(245,158,11,.4), scale 0.8→1 + fade in 0–0.5 s; description fades up 30 px at 1.0–1.8 s (34 px/500 #a1a1aa lh 1.5). Section chips 'تعريف ١': 40 px pill, radius 999, 2 px currentColor border, bg rgba(5,7,11,.45) + blur(6px). Glass step badge: .num 54 px circle rgba(255,255,255,.14), 1.5 px white .75 border, backdrop-filter blur(6px), digits ١ ٢ ٣ ٤; label 46/700 + line 25/300. Floating language chips: pop 90 ms apart, drift 6 px sine over 3 s. **أرقام / params:** pill 24 px/800; chip 40 px; badge 54 px.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html:40` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/index.html:17` · `kosif-one/projects/whatsapp-motion/projects/success/index.html:74-106` · `style:isometric`

#### ARAB-55 · مكدّس عربي/إنجليزي · Bilingual Arabic/English stacks & HUD · 🟢 جاهز / ready
- **ماذا / what:** سطر عربي في الأعلى وترجمة إنجليزية أصغر تحته، أو HUD يجمع عنوانًا عربيًا وسطرًا تقنيًا إنجليزيًا. — Arabic line on top with a smaller English line below, or a HUD pairing an Arabic headline with a technical English line.
- **متى أستخدمها / when:** محتوى لجمهور مزدوج أو شرح تقني — dual audiences and technical explainers.
- **كيف / how:** Arabic block RTL on top, English block LTR beneath at ~70% size (the doodle reference sits near 2.8:1 with muted blue English), each block with its own dir. HUD per stage: #ar Cairo 800 62 px rising 26 px over 0.2 s; #en mono 21 px built from live numbers; colour by stage — #ffb4a2 failure, #d0ff6a success, #eaffed default. **أرقام / params:** EN ≈70% of AR (doodle 2.8:1); HUD 62 / 21 px.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:82` · `kosif-tool/playbooks/arabic-typography.md` · `style:doodle`

#### ARAB-56 · بطاقة شخصية من اليمين · RTL character card · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** صورة مؤطرة يسارًا، وعلى اليمين شارة ودور واسم ضخم وسطر تعريف. — Framed avatar left; right-aligned tag pill, role, huge name and a one-line bio.
- **متى أستخدمها / when:** تاريخ سياسي، شخصيات، فرق عمل — history timelines, characters, teams.
- **كيف / how:** Build: avatar frame on the left; right-aligned stack: tag pill, small role, huge name, one-line bio; gold/cream on navy and burgundy (#172237, #731521, #e9d5b0, #e0b23a); cards slide/fade about every 1.7 s; party names in pop-in pills. **أرقام / params:** card every ~1.7 s.
- **الدليل / proof:** `style:pm-triglyceee-bd5b08`

#### ARAB-57 · عنوان عربي سينمائي فوق الفيديو · Cinematic Arabic headline over footage · 🟢 جاهز / ready
- **ماذا / what:** عنوان عربي كبير متوازن بظل داكن ناعم وسطر علوي صغير، في الركن السفلي من بداية القراءة فوق اللقطات. — A large balanced Arabic headline with a soft dark shadow and a small eyebrow, bottom-start over footage.
- **متى أستخدمها / when:** مقدمات الأفلام والوثائقيات فوق لقطات حقيقية — documentary intros over real footage.
- **كيف / how:** h2 font-size clamp(31px,4.9vw,65px), lh 1.18, weight 700, text-wrap:balance, text-shadow 0 3px 30px rgba(0,0,0,.45); eyebrow 12 px/700 (its .16em tracking only on Latin); description clamp(13px,1.7vw,17px) lh 1.9; phone h2 clamp(29px,8vw,42px); box width min(560px, 100% − 44px), inset-inline-start clamp(22px,6vw,110px). Drop the source's −.035em tracking on Arabic (ARAB-03). **أرقام / params:** lh 1.18; shadow 0 3px 30px .45.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.css` · `kosif-audit-studio/styles.css:166` · `kosif-audit-studio/continuous-review.css:1`

#### ARAB-58 · عنوان ASS متحرك لكل لقطة · Per-shot ASS animated title card · 🟢 جاهز / ready
- **ماذا / what:** ملف ASS لكل لقطة فيه كلمة بطلة وسطر تفصيل يصعدان ويتلاشيان وشعار ثابت في الزاوية — يُحرق بـ libass بلا متصفح. — One ASS file per shot: hero word + detail line that rise and fade, plus a fixed corner tag — burned by libass, no browser.
- **متى أستخدمها / when:** مونتاج ffmpeg سريع لعشرات اللقطات — fast ffmpeg edits across many shots.
- **كيف / how:** ASS v4.00+ (PlayResX/Y = frame size, WrapStyle 2, UTF-8 BOM), three styles. Hero 60 px bold, outline 2.5, shadow 1.3, MarginV 210: {\an2\move(x,766,x,740,0,900)\fad(650,700)}; Detail 32 px, outline 1.4: {\move(x,812,x,793,300,1050)\fad(650,600)} starting +0.45 s; Tag 21 px {\an7\pos(30,38)\fad(400,600)}; burn with ffmpeg -vf "ass=scene_XX.ass:fontsdir=fonts"; style Encoding −1 (ARAB-62). **أرقام / params:** hero 60 px, move 26 px over 0.9 s; detail +0.45 s.
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/KOSIF_Ghorba_Render.py:39-63`
- **⚖️ ترخيص / license:** الأصل يستخدم Dubai (مملوك) — استبدله بـ Cairo من proofs/_shared/fonts / original uses proprietary Dubai — swap to Cairo from proofs/_shared/fonts.

#### ARAB-59 · غلاف بعنوان عربي مشكّل · Shaped Arabic cover / thumbnail · 🟢 جاهز / ready
- **ماذا / what:** يأخذ إطارًا من الفيلم، يعتّم أسفله بتدرج منحنٍ، ويكتب عنوانًا عربيًا مشكّلًا (≤3 أسطر) وسطرًا ذهبيًا. — Grabs a frame, darkens the lower part with a curved gradient and sets a shaped Arabic title (≤3 lines) plus a gold subtitle.
- **متى أستخدمها / when:** غلاف كل فيلم قبل النشر — the cover for every delivery.
- **كيف / how:** python kosif-studio/motion/tools.py thumb FILM --out cover.jpg [--at 2.0 --text 'عنوان' --sub '…' --size 1080x1920] (same as kmotion thumb): optional reframe; gradient alpha 0.78·t² from 45% height; title 8.5% of the short side, stroke size/18, lh 1.25, wrap at 84% width, block ending at 80% H; sub 50% size #E7B65A; JPEG q93. It is correct here because Pillow RAQM shapes the raw text — do not install arabic-reshaper in this container (ARAB-06). **أرقام / params:** title 8.5% short side; gradient 0.78·t²; q93.
- **الدليل / proof:** `kosif-studio/motion/tools.py:317` · `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### ARAB-60 · كاروسيل عربي PNG/PDF · Arabic carousel renderer · 🟢 جاهز / ready
- **ماذا / what:** يرسم شرائح كاروسيل عربية مع PDF وورقة لقطات، ويصغّر العناوين تلقائيًا إلى ≤4 أسطر. — Renders Arabic carousel slides + PDF + contact sheet, auto-shrinking titles to ≤4 lines.
- **متى أستخدمها / when:** منشورات إنستغرام ولينكدإن المصاحبة للفيلم — companion social posts.
- **كيف / how:** python3 100-superskills/skills/kosif-social/scripts/social.py carousel spec.json --out dir → slide_NN.png + carousel.pdf + contact sheet; 1080×1350 or 1080×1440; Latin fallback font; brand bg/fg/accent/handle. Shaping here is Pillow RAQM on raw text (its reshaper import falls back). Font search prefers NotoKufiArabic-Bold → Cairo-Bold → Tajawal-Bold …; drop Cairo-Bold.ttf into ~/.fonts so it is not left on DejaVu. **أرقام / params:** 1080×1350 | 1080×1440; ≤4 title lines.
- **الدليل / proof:** `100-superskills/skills/kosif-social/scripts/social.py:316` · `100-superskills/skills/kosif-social/examples/carousel.json`

#### ARAB-61 · طبقات نص الخط الزمني JSON · Timeline-JSON text overlays · 🟢 جاهز / ready
- **ماذا / what:** نص أو شريط اسم يُعلن في ملف الخط الزمني بموضع وحجم وحركة جاهزة، فيُرسم مشكّلًا فوق اللقطات. — Text or lower thirds declared in the timeline JSON with position, size and a preset move, drawn shaped over footage.
- **متى أستخدمها / when:** مونتاج من JSON بدون صفحة HTML — JSON-driven edits without an HTML page.
- **كيف / how:** overlays: type text {pos, size, color, box, stroke, anim: fade|rise|drop|slide-left|slide-right|none}, fade 0.35 s, 9:16 safe band 14–80% of height; type lower-third {title, sub, accent #E7B65A}. For full tashkeel switch the mimic text_style.engine to 'browser'. **أرقام / params:** anims fade|rise|drop|slide-left|slide-right|none; fade 0.35 s; safe 14–80%.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md` · `100-superskills/skills/kosif-montage-motion/references/mimic.md`

## الترجمة والكاريوكي والنص من الصوت — Captions, karaoke & verse from sound

_حين يكون الصوت هو الساعة._

#### ARAB-62 · كاريوكي ASS عربي بثلاثة أنماط · Arabic ASS karaoke captions (reels · cinema · punchy) · ✅ مُثبت هنا / proven here
- **ماذا / what:** ترجمة تُحرق في الفيديو بحدث لكل كلمة منطوقة: لون التمييز ونبضة 112%→100% في 120 ms، وترتيب الكلمات العربي سليم. — Burned captions with one event per spoken word: highlight colour and a 112%→100% pop in 120 ms, Arabic word order intact.
- **متى أستخدمها / when:** كل ريل فيه كلام — every reel with speech.
- **كيف / how:** python kosif-studio/motion/montage.py captions VIDEO --spec caps.json --style reels|cinema|punchy (also inside cut/voicecut). PlayRes = frame; sizes scale with the short side; side margins 6% W; ≤6 words per on-screen chunk; one Dialogue per word with {\1c<hi>\fscx112\fscy112\t(0,120,\fscx100\fscy100)}word{\r}; missing word times are split by letters + 2; style Encoding −1 so libass detects the RTL paragraph; burn ass=caps.ass,format=yuv420p, libx264 crf 17, audio copied untouched. Verified here with Cairo via fontsdir: Encoding −1 keeps 'كل إطار يسمع الموسيقى' in order; Encoding 1 + an override flips it to 'الموسيقى يسمع كل إطار'. Noto Arabic is not installed system-wide here, so pass fontsdir= (or register the repo fonts) or libass falls back. **أرقام / params:** pop 112%→100% / 120 ms; ≤6 words; Encoding −1.

| النمط / style | الخط / font | الحجم لكل 1080 | الأساسي | التمييز | حد | ظل | هامش سفلي /1920 |
|---|---|---|---|---|---|---|---|
| reels | Noto Sans Arabic | 74 | #FFFFFF | #FFDE59 (&H0059DEFF) | 6 | 3 | 300 |
| cinema | Noto Naskh Arabic | 46 | #EAEAEA | #FFE6A8 (&H00A8E6FF) | 3 | 2 | 150 |
| punchy | Noto Kufi Arabic | 72 | #FFFFFF | #38BDF8 (&H00F8BD38) | 8 | 4 | 330 |


```ass
Style: Cap,Cairo,74,&H00FFFFFF,&H0059DEFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,65,65,300,-1
Dialogue: 0,0:00:01.00,0:00:01.45,Cap,,0,0,0,,كل {\1c&H0059DEFF&\fscx112\fscy112\t(0,120,\fscx100\fscy100)}إطار{\r} يسمع الموسيقى
; ffmpeg -i in.mp4 -vf "ass=caps.ass:fontsdir=fonts,format=yuv420p" -c:a copy out.mp4
```

- **الدليل / proof:** `kosif-studio/motion/montage.py:321` · `kosif-studio/tests/test_studio.py:765` · `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### ARAB-63 · قانون زمن القراءة والكثافة · Reading-time & density law · 📄 موصوف / documented only
- **ماذا / what:** كم كلمة على الشاشة وكم تبقى: معادلات ثابتة بدل التخمين. — How many words on screen and for how long — fixed formulas instead of guessing.
- **متى أستخدمها / when:** قبل توقيت أي بطاقة نصية أو خطاف — before timing any text card or hook.
- **كيف / how:** Hook text: cold-open line bold and larger (0.16 of frame vs 0.12), ≤12 characters; other lines ≤18; max 2 lines; display = max(0.15 s × characters, 2 s), capped at 6 s; enter 0.3 s after a cut, leave 0.3 s before the next; count graphemes after shaping. Cards: 3–4 words (1–7), ~0.4 s per word, ≥0.5 s per card, a URL ≥1.7 s. Line hold ≥ 0.3 s + 0.06 s × characters after the last word lands. Captions 5–7 words. **أرقام / params:** t = max(0.15·chars, 2) ≤ 6 s; 0.3 s offsets; 0.4 s/word.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2441-akbun-davinciresolve-searchhook/SKILL.md` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `kosif-tool/playbooks/kinetic-type.md`

#### ARAB-64 · منطقة الترجمة الآمنة وشكلها · Caption safe zone & look · 📄 موصوف / documented only
- **ماذا / what:** أين تجلس الترجمة وبأي سماكة حدّ وكم كلمة — للسينما وللمنصات. — Where captions sit, how thick the outline is and how many words — for cinema and for social.
- **متى أستخدمها / when:** أي ترجمة ثابتة أو مقروءة على الهاتف — every subtitle.
- **كيف / how:** Cinema: bottom-centre white, thin black outline 1–2, no box, no animation; one line preferred, max two growing upward; glyph height 3.5–4.5% of H, side margin ≥8%, bottom 8–10% (ASS Alignment=2, Shadow=0, MarginV ≈ 9% H; BorderStyle=3 gives an opaque box). Social: bold clear face (Cairo/Almarai), outline 6–8 px, deep shadow, 5–7 words, ≥280 px from the bottom on 9:16, safe band 14–80% of height; Naskh captions ≤8 words, mono only for code. Use OFL fonts only and stop if missing (fc-list | grep -i <font>) rather than substitute. **أرقام / params:** glyph 3.5–4.5% H; margins 8%; outline 6–8 px social; ≥280 px bottom.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template/SKILL.md` · `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md` · `kosif-atlas/skills/1096-akbun-editvideo/2464-davinciresolve-subtitle-devtalk/SKILL.md` · `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`

#### ARAB-65 · الكلمة المنطوقة تضيء · Spoken-word illumination (HTML captions) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الجملة كلها ظاهرة كشبح باهت، وكل كلمة تتجسد وتأخذ اللون لحظة نطقها. — The whole line sits as a faint ghost; each word solidifies and takes colour as it is spoken.
- **متى أستخدمها / when:** سرد بصوت حقيقي في أفلام HTML — voiced narration in HTML films.
- **كيف / how:** Build: phrase at 25–60% opacity (doodle ghost ~25%, playbook recipe 60%); at words.json start − 40…80 ms the word goes to 100% + accent; emphasis words orange (#f27525 plotter / #f07f2e doodle); optional accent pill that hops word to word, scale 0.96→1.08 over 140 ms; long words may fill right→left over their duration; never change transcript words. **أرقام / params:** ghost 25–60%; lead 40–80 ms; pill 0.96→1.08 / 140 ms.
- **الدليل / proof:** `style:doodle` · `style:plotter` · `kosif-tool/playbooks/kinetic-type.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### ARAB-66 · فيلم الكلمات من الصوت · Verse film from sound (song · poem · dua) · 📦 بأمر تثبيت / one install
- **ماذا / what:** من أغنية أو قصيدة أو دعاء: كلمات محاذاة، أسطر مقروءة، مقاطع عند الوقفات، كلمة مفتاحية لكل سطر، وضوء يقوده الصوت — في verse.json قابل للتعديل. — From a song, poem or dua: aligned words, readable lines, sections at pauses, one keyword per line and sound-driven light — written to an editable verse.json.
- **متى أستخدمها / when:** أي صوت يُراد تحويله إلى كلمات متحركة — any audio that should become moving words.
- **كيف / how:** python kosif-studio/motion/verse.py AUDIO --name N [--text lyrics.txt] [--words X.words.json] [--mood night|dawn|gold|sea|ink] [--accent #E7B65A] [--font 'Aref Ruqaa'] [--images …] [--music none|auto] [--flat] [--render] (kmotion verse is the same). True text is aligned onto Whisper word times, diacritic/hamza tolerant (ARAB-69); lines 1.1–3.6 s, ≤7 words (ARAB-67); pause ≥3 s → new section, ≥4.5 s → interlude with an 8-point rosette; ~12 s sections; keywords ≥2 s apart (ARAB-68); concept icons sun, moon, heart, clock, money, trophy, road, question, check, home, rain, light; 3D words (ARAB-28), gilded fill (ARAB-39), dust and light rays; title/end cards 128k/42k with .25 s stagger, 0.7 s power3.out; custom display face from assets/display.ttf. Music is none by default — recitations stay unaccompanied. Arabic transcription wants a multilingual large-v3 model. **أرقام / params:** lines ≤7 words, 1.1–3.6 s; section pause 3 s; interlude 4.5 s; 24.8 s dua → 743 frames.
- **الدليل / proof:** `kosif-studio/motion/verse.py` · `kosif-one/tools/kosif-studio/motion/verse.py:1` · `kosif-one/tools/kosif-studio/motion/projects/verse_dua/verse.json` · `100-superskills/skills/kosif-montage-motion/scripts/verse.py:199`
- **📦 تثبيت / install:** `pip install faster-whisper`
- **⚖️ ترخيص / license:** GSAP مدمج (gsap.min.js) برخصة GSAP القياسية «بلا مقابل» — ليست MIT / vendored GSAP, standard no-charge license (not MIT). | faster-whisper MIT.

#### ARAB-67 · تقسيم الأسطر بالبرمجة الديناميكية · DP line breaking for lyrics & dua · ✅ مُثبت هنا / proven here
- **ماذا / what:** يختار نقاط القطع بحيث يكون كل سطر مقروءًا: لا قصير ولا طويل، عند الوقفات والترقيم وبدايات العبارات، ولا يقطع بعد حرف جر ولا داخل دعاء ثابت. — Chooses cut points so every line reads well — at pauses, punctuation and phrase openers, never after a particle or inside a fixed invocation.
- **متى أستخدمها / when:** أي نص منطوق طويل يتحول لأسطر — any long spoken text turned into lines.
- **كيف / how:** verse.segment(words, max_words=7): dynamic programming over cut points; target 1.1–3.6 s per line; break bonus 8·min(gap, 1) + punctuation 1.0 + phrase opener 0.8 (اللهم، يا، إلا، and dua imperatives اجعل/اغفر/ارحم…) + و-clause 0.6 + ف-clause 0.5; penalties: after a particle −0.7, inside numbers −0.8, a 'يا … يا' chain −1.0. **أرقام / params:** ≤7 words; 1.1–3.6 s; bonuses 8/1.0/0.8/0.6/0.5; penalties −0.7/−0.8/−1.0.
- **الدليل / proof:** `kosif-studio/motion/verse.py:203` · `kosif-studio/motion/verse.py:217` · `kosif-studio/tests/test_studio.py:943`

#### ARAB-68 · اختيار الكلمة المفتاحية بالنبر · Stress-based keyword picking · ✅ مُثبت هنا / proven here
- **ماذا / what:** يقيس نبر كل كلمة من علو الصوت وطولها ويختار كلمة واحدة لكل سطر، ولا يختار الحشو ولا الوحدات بعد الأرقام. — Scores each word's stress from loudness and length and picks one keyword per line — never fillers or units after numbers.
- **متى أستخدمها / when:** قبل أي ضربة أو تلوين كلمة — before any slam or highlight.
- **كيف / how:** stress = 0.65·z(log rms) + 0.35·z(length); score = stress + 0.9·(i+1)/n (end focus) + 0.5 if the word recurs 2–3×; a unit after a number −3; ~130 stop/filler words excluded (MSA + Egyptian: ده، دي، كده، بس، يعني، اوي…); each keyword used once; spacing ≥1.2 s (direct) or score ≥0.75 and ≥2 s apart (verse). **أرقام / params:** 0.65/0.35 weights; end focus 0.9; recurrence +0.5; spacing 1.2 s / 2 s.
- **الدليل / proof:** `kosif-studio/motion/direct.py:87` · `kosif-studio/motion/direct.py:143` · `kosif-studio/motion/verse.py:300` · `kosif-studio/motion/direct.py:36`

#### ARAB-69 · توحيد النص العربي للمطابقة · Arabic normalisation for alignment & matching · ✅ مُثبت هنا / proven here
- **ماذا / what:** شكل مقارن للكلمة: بلا تشكيل ولا تطويل، ألفات موحدة، ى←ي، ة←ه، ؤ←و، ئ←ي، وأرقام لاتينية. — A comparable form of each word: no harakat or tatweel, unified alefs, ى→ي, ة→ه, ؤ→و, ئ→ي, Latin digits.
- **متى أستخدمها / when:** محاذاة النص مع Whisper، البحث، إزالة تكرار الهاشتاج — whisper alignment, search, hashtag dedupe.
- **كيف / how:** NFKC; strip U+064B–U+065F, U+0670 and tatweel; أ إ آ ٱ → ا; ى → ي; ة → ه; ؤ → و; ئ → ي; ٠–٩ (and ۰–۹) → 0–9; drop punctuation; collapse spaces. Display text keeps its tashkeel — normalise only the matching copy.

```python
import re, unicodedata
H = re.compile('[\u064B-\u065F\u0670\u0640]')          # harakat + tatweel
MAP = str.maketrans('أإآٱىةؤئ٠١٢٣٤٥٦٧٨٩', 'اااايهوي0123456789')
def norm_ar(s):
    s = H.sub('', unicodedata.normalize('NFKC', s)).translate(MAP)
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', s)).strip().lower()
# norm_ar('إِنَّ الصَّلاةَ مُؤْمِنَةٌ ٢٠٢٦') -> 'ان الصلاه مومنه 2026'
```

- **الدليل / proof:** `kosif-audit-studio/engine.js:31` · `kosif-audit-studio/tests/voice.test.js:14` · `kosif-studio/motion/verse.py:64` · `kosif-one/tools/kosif-social/scripts/social.py`

#### ARAB-70 · النص المشكول مصدرًا للتوقيت · Vowelled source text over ASR · 📄 موصوف / documented only
- **ماذا / what:** احتفظ بالتشكيل الكامل ووقفات الشاعر «..» في ملف الكلمات واجعله مصدر المحاذاة بدل الثقة بالتفريغ الآلي للغناء. — Keep full tashkeel and the poet's '..' pauses in the lyric file and align it, instead of trusting ASR on singing.
- **متى أستخدمها / when:** الأغاني والقصائد المغناة — sung material.
- **كيف / how:** lyrics.txt with complete harakat; pass it with --text so ASR only provides timing; split on '..' for phrase cards; display harakat through the browser engine (ARAB-06). Example: 31 vowelled lines. **أرقام / params:** 31 lines example.
- **الدليل / proof:** `kosif-one/projects/songreel-ghorba/lyrics.txt`

#### ARAB-71 · ستايل الكلمات العاطفي · Emotional lyric style preset · 📦 بأمر تثبيت / one install
- **ماذا / what:** كلمات كبيرة لليلة بلونين تدفأ على الكلمات المميزة، بوكيه سابح، تسرّب ضوء يتنفس، والسطر السابق يطفو بعيدًا. — Big words on a two-colour night that warms on emphasised words, drifting bokeh, a breathing light leak, the previous line floating away.
- **متى أستخدمها / when:** أغانٍ وقصائد وصوت عاطفي — songs, poems, emotional voice.
- **كيف / how:** STY.lyric: 9:16, calm, 2.0 words/s; Lalezar heads + Cairo body; bg #0E0A16 → bg2 #2A1236, ink #F7EFE6, dim rgba(247,239,230,.28), accent #FFB35C, glow #FF7A59; an underline grows with the voice; sfx shimmer/pop/swell; uses the real song words when audio exists. **أرقام / params:** 2.0 wps; #0E0A16/#2A1236/#F7EFE6/#FFB35C/#FF7A59.
- **الدليل / proof:** `app/public/js/10_studio.js:551`
- **📦 تثبيت / install:** `cd app && npm install`

## الأرقام والعزل والتوطين — Numbers, bidi & localisation

_الأرقام والأسماء اللاتينية داخل الجملة العربية، والجمع، والترميز._

#### ARAB-72 · العزل الاتجاهي · Bidi isolation · 🟢 جاهز / ready
- **ماذا / what:** الأسماء اللاتينية والأرقام داخل جملة عربية تقلب الترقيم وترتيبها ما لم تُعزل. — Latin names and numbers inside Arabic flip punctuation and order unless isolated.
- **متى أستخدمها / when:** أي سطر مختلط عربي/لاتيني/أرقام — every mixed line.
- **كيف / how:** <bdi> or unicode-bidi:isolate (plaintext for whole mixed lines) around Latin names, numbers, code and timecodes; control chars RLI U+2067 / LRI U+2066 / PDI U+2069; in ASS/ffmpeg add RLM U+200F at line edges; the review page wraps every Arabic run in <bdi dir=rtl> (AR_RUN regex); code blocks dir=ltr + isolate inside RTL pages; mirror arrows and progress fills, never logos, media or time axes. **أرقام / params:** RLI 2067 / LRI 2066 / PDI 2069 / RLM 200F.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:902` · `kosif-tool/playbooks/arabic-typography.md:48` · `kosif-atlas/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu/SKILL.md` · `kosif-tool/playbooks/code.md:73`

#### ARAB-73 · نظام أرقام واحد وأرقام جدولية · One digit system + tabular figures · 🟢 جاهز / ready
- **ماذا / what:** اختر أرقامًا غربية أو هندية للفيلم كله، واجعلها جدولية حتى لا يرتجف العدّاد. — Choose Western or Arabic-Indic digits for the whole film and make them tabular so counters never jitter.
- **متى أستخدمها / when:** كل عدّاد وجدول ورسم بياني — every counter, table and chart.
- **كيف / how:** font-variant-numeric: tabular-nums; font-feature-settings "tnum" 1, "lnum" 1; Intl.NumberFormat('ar-EG') → ٠–٩, 'ar-SA-u-nu-latn' → 0–9 with Arabic grouping; toLocaleString('ar-EG') for quick Arabic-Indic; codes and dates in mono inside <bdi>; numerals LTR inside RTL; right-align numeric columns. **أرقام / params:** tnum + lnum; one digit system per film.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/tokens.css:304` · `kosif-earth-ci-fork/ui/components/charts.js:17` · `kosif-tool/starters/remotion/src/Film.tsx:303` · `kosif-tool/playbooks/charts.md:190`

#### ARAB-74 · منسّق الأرقام الهندية الحتمي · Deterministic Arabic-Indic money formatter · ✅ مُثبت هنا / proven here
- **ماذا / what:** يحوّل المبالغ بالوحدات الصغرى إلى نص مجمّع بعملة وأرقام هندية بلا Intl، بنفس الناتج في Node والمتصفح. — Formats minor-unit amounts into grouped money strings with Arabic-Indic digits and no Intl — identical in Node and browser.
- **متى أستخدمها / when:** أرقام مالية في الفيديو يجب أن تطابق الحسابات — financial figures that must match the books.
- **كيف / how:** import { formatMinor, toArabicDigits, formatPercent } from kosif-audit-pro/lib/kosif/format.mjs; formatMinor(minor, {exp:2, arabicDigits:true, currency:'ر.س'}); thousands ','; half-away-from-zero rounding; wrap the result in <bdi> (ARAB-72). **أرقام / params:** digits ٠١٢٣٤٥٦٧٨٩; exp 2; half-away-from-zero.
- **الدليل / proof:** `kosif-audit-pro/lib/kosif/format.mjs` · `kosif-audit-pro/tests/kosif-engine.test.mjs:94`

#### ARAB-75 · قراءة الأرقام والوحدات العربية · Digit parsing & number/unit detection · 🟢 جاهز / ready
- **ماذا / what:** يحوّل الأرقام الهندية والفارسية إلى لاتينية ويكتشف الرقم ووحدته في سطر السكربت ليحرّكه ستايل العدّاد. — Maps Arabic-Indic and Persian digits to Latin and detects the figure and unit in a script line so a counter can animate it.
- **متى أستخدمها / when:** سكربت فيه أرقام وإحصاءات — scripts with statistics.
- **كيف / how:** MK.latin maps ٠–٩, ۰–۹ and ٫/٬; MK.lineMeta regex picks the first number with units %, ٪, ألف, مليون, مليار, k, M; it also flags questions (؟) and quotes («) so styles can trigger ARAB-45 or a quote card. **أرقام / params:** units %, ٪, ألف, مليون, مليار, k, M.
- **الدليل / proof:** `app/public/js/10_studio.js:33` · `app/public/js/10_studio.js:34`

#### ARAB-76 · صيغ الجمع ومطابقة العدد · Plural & count agreement · 🟢 جاهز / ready
- **ماذا / what:** العربية لها ست صيغ عددية؛ 1 و2 لهما لفظ خاص، و3–10 جمع، و11 فما فوق مفرد منصوب. — Arabic has six plural categories; 1 and 2 have their own words, 3–10 take the plural, 11+ the singular accusative.
- **متى أستخدمها / when:** أي عدّاد أو تسمية فيها معدود — every counted label.
- **كيف / how:** new Intl.PluralRules('ar').select(n) → zero/one/two/few/many/other, or ICU MessageFormat; UI rule: n=1 singular phrase, n=2 dual ('تعديلان بانتظار الإرسال'), 3–10 plural, ≥11 'N تعديلاً'; translation is meaning-based, glossary first, keeping {{vars}} and HTML. **أرقام / params:** 6 CLDR forms.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:571` · `kosif-atlas/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu/SKILL.md` · `100-superskills/skills/translation-localization-ar/SKILL.md`

#### ARAB-77 · رقم يتحول إلى عنوان · Number → headline · 📄 موصوف / documented only
- **ماذا / what:** إحصائية كبيرة تعدّ ثم تتنحى لتفسح للجملة الشارحة بوحدتها ومصدرها الصغير. — A big statistic counts up, then steps aside for the explanatory sentence with its unit and a small source.
- **متى أستخدمها / when:** رقم صادم في بداية شرح — a striking number opening an explainer.
- **كيف / how:** 0–1.5 s the number counts up in tabular digits of the chosen system, 1.5–2.5 s it moves aside, 2.5–5 s the sentence mask-reveals (ARAB-19) with unit and source line; never invent a number. The infographic reference shows the counter side: odometer columns where lower digits spin more turns, hero number at 12–15% of height. **أرقام / params:** 5 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md` · `style:infographic`

#### ARAB-78 · حوار طباعي · Typographic dialogue · 📄 موصوف / documented only
- **ماذا / what:** سؤال يستقر على اليمين ثم ينسحب قليلًا ويدخل الجواب من الجهة المقابلة بلون ثانٍ. — A question settles on the right, withdraws slightly, and the answer enters from the other side in a second colour.
- **متى أستخدمها / when:** سؤال وجواب، رأيان، حوار شخصين — Q&A and two voices.
- **كيف / how:** 0–2 s question, 2–2.6 s transition, 2.6–6 s answer with enough reading delay; two layers, two masks, alternating positions; never present an illustrative example as a real quote. **أرقام / params:** 6 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/motion-typography.md`

#### ARAB-79 · الدعوة والسعر بالعربية · Arabic CTA & price isolation · 📄 موصوف / documented only
- **ماذا / what:** الدعوة بفعل أمر، ونظام أرقام واحد، والعملة والرقم في وسم معزول واحد. — CTAs use an imperative verb, one digit system, and currency + number in one isolated span.
- **متى أستخدمها / when:** نهاية الإعلانات وبطاقات السعر — ad endings and price cards.
- **كيف / how:** Verbs: اشترك، حمّل، اطلب؛ <bdi>٤٩ ر.س</bdi>; end-card CTA 'تابعنا للمزيد' (ARAB-49).
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:77`

#### ARAB-80 · تسميات عربية مُسقطة على الخرائط والعوالم · Projected Arabic labels (maps · isometric · charts) · 📦 بأمر تثبيت / one install
- **ماذا / what:** التسميات عناصر HTML تُوضع كل إطار بإسقاط إحداثياتها على الشاشة، فتأخذ خط الفيلم العربي كاملًا. — Labels are HTML elements placed each frame by projecting their coordinates, so they get the film's full Arabic typography.
- **متى أستخدمها / when:** خرائط متحركة، عوالم أيزومترية، مخططات — animated maps, isometric worlds, charts.
- **كيف / how:** Per frame p = map.project([lng, lat]) → {x, y, reveal}; absolutely positioned divs in the film's Arabic font, rise-and-fade ~0.7 s with an accent rule, pointer-events none; on a fixed plate apply the same translate/scale to label positions. Inside MapLibre symbol layers Arabic needs the RTL text plugin and Arabic glyph PBFs — overlays are safer. SVG worlds: HTML layer above the SVG, positioned by projecting world points; avoid SVG <text> with text-anchor end + rtl (misplaces). Charts: Arabic family on Arabic labels, measure with the real font, ≥24 px at 1080p, decide axis mirroring and digit style once. **أرقام / params:** label reveal ~0.7 s; ≥24 px at 1080p.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md` · `kosif-atlas/skills/345-visuals/1242-html-diagram/references/svg-primitives.md` · `style:isometric`
- **📦 تثبيت / install:** `npm i maplibre-gl`

#### ARAB-81 · إصلاح أسماء الملفات العربية المشوّهة · Arabic file-name mojibake repair · ✅ مُثبت هنا / proven here
- **ماذا / what:** يستعيد أسماء الملفات العربية التي تصل بترميز خاطئ ولا يقبل التخمين إلا إذا أنتج حرفين عربيين على الأقل. — Restores Arabic upload names that arrive mis-decoded, accepting a guess only if it yields at least two Arabic letters.
- **متى أستخدمها / when:** ملفات يرفعها المستخدم من ويندوز أو متصفحات قديمة — uploads from Windows or old browsers.
- **كيف / how:** server._unmojibake(): tries (latin-1→utf-8), (cp1252→utf-8), (latin-1→cp1256); then _safe_name() keeps word chars, '-', '.', space, the Arabic block U+0600–06FF and parentheses. **أرقام / params:** ≥2 Arabic letters to accept.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:77` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:235`

#### ARAB-82 · سطر الحقوق الآمن · Safe credit-line burn · 🟢 جاهز / ready
- **ماذا / what:** يضيف اسم صاحب المادة صغيرًا أسفل الفيديو من ملف نصي، فلا يدخل نص غير موثوق إلى قواعد مرشحات ffmpeg. — Adds the source creator's credit small at the bottom from a text file, so untrusted text never enters the ffmpeg filter grammar.
- **متى أستخدمها / when:** ريلز من مواد الآخرين المرخّصة — reels using licensed third-party clips.
- **كيف / how:** reel --credit 'insta: name' → drawtext textfile=…, ≤300 chars, fontsize 1.3% H, white@0.5, y = 0.905·h. Latin handles only: drawtext here shapes Arabic through FriBiDi presentation forms and shows tofu with modern fonts (verified) — burn an Arabic credit as a one-line ASS event (ARAB-58/62) instead. **أرقام / params:** 1.3% H; white@0.5; y 0.905h; ≤300 chars.
- **الدليل / proof:** `kosif-studio/motion/reel.py:163`

#### ARAB-83 · تسمية الألوان بالعربية · Arabic colour naming · 🟢 جاهز / ready
- **ماذا / what:** يعطي أي لون اسمًا عربيًا تقريبيًا (الأحمر الداكن، الأخضر الزيتي، الكريمي…) من تدرجه وتشبعه وقيمته. — Gives any RGB colour a rough Arabic name (dark red, olive green, cream…) from hue, saturation and value.
- **متى أستخدمها / when:** تسميات خطوات الرسم ولوحات الألوان والسرد — step labels, palette cards, narration.
- **كيف / how:** vectorize.name_ar(rgb); HSV thresholds: s < .14 or v < .12 → neutral; hue bands at 15/45/62/165/260/300/340°. **أرقام / params:** hue bands 15/45/62/165/260/300/340.
- **الدليل / proof:** `kosif-studio/vectorize.py:105`

## المحاكاة والمطابقة ومحركات الرسم — Mimic, matching & raster engines

_حين يُطلب «مثل هذا المرجع» أو يُرسم النص خارج المتصفح._

#### ARAB-84 · التقاط ستايل النص وإعادة تركيبه · Text-style capture & compositing · ✅ مُثبت هنا / proven here
- **ماذا / what:** يقيس لون التعبئة وسماكة الحد والظل والتوهج والصندوق والمحاذاة لنص المرجع ثم يركّب النص الجديد بنفس الشكل. — Measures fill, outline, shadow, glow, box and alignment of reference text and composes new text with the same look.
- **متى أستخدمها / when:** «اعمل مثل هذا الفيديو» — 'make it look like this reference'.
- **كيف / how:** mm_text style pass (consensus medians over events; OCR draft with Arabic tessdata only when tesseract exists — it does not here) → mm_render_text.compose(alpha, style) → RGBA with fill/outline/shadow (dx, dy, blur, opacity)/glow/box. mimic.json text_style {font, size as frame fraction, color, stroke, stroke_color, shadow, anim, fade, line_height, align, fit_width, engine:'browser'}; texts[] with start/end and x/y centre fractions (line h = bbox h / lines / 1.3). Example study: Diwani at 0.08 H (135 px at 1920), #fdfbf3, stroke 7 #000000, fade .35 s, lh 1.25. **أرقام / params:** stroke ~7 px at 1080; anim fade|rise|drop|slide-left|slide-right|none.
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_text.py` · `kosif-one/tools/kosif-mimic/scripts/mm_render_text.py` · `kosif-one/projects/mimic-jumuah/study/mimic.json` · `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### ARAB-85 · قياس حركة النص وتصنيفها · Text-animation measurement & replay · 🟢 جاهز / ready
- **ماذا / what:** يجد أحداث النص في المرجع ويقيس دخولها وخروجها ويصنّفها إلى 11 نوعًا، ثم يعيد تشغيل المنحنى نفسه بالخط المطابق. — Finds text events in a reference, measures entrance/exit, classifies 11 kinds and replays the same curve in the matched font.
- **متى أستخدمها / when:** نسخ إيقاع حركة النص من مرجع — copying a reference's text timing.
- **كيف / how:** mm_text.analyze_text measures visibility, displacement, scale, sharpness and per-word onsets → classify_anim; mm_textfx.EventLayer replays the normalised alpha/offset/scale/blur/word curves frame by frame. Kinds: cut, words, slide_up, slide_down, slide_left, slide_right, pop (overshoot > 1.03), zoom_in, zoom_out, blur, fade. Imports checked here (numpy + Pillow + ffmpeg; OpenCV optional and absent). **أرقام / params:** 11 kinds; pop when scale overshoot > 1.03.
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_text.py` · `kosif-one/tools/kosif-mimic/scripts/mm_textfx.py` · `100-superskills/skills/kosif-mimic/scripts/mm_text.py:737` · `100-superskills/skills/kosif-mimic/scripts/mm_textfx.py:185`

#### ARAB-86 · مطابقة الخط بالحبر · Font matching by ink · 🟢 جاهز / ready
- **ماذا / what:** يكتب النص نفسه بكل خط في المكتبة ويقارنه بحبر المرجع (النسبة، التقاطع المتسامح، سماكة الضربة) ويرتب النتائج في ورقة. — Renders the same text in every library face and ranks them against the reference ink (aspect, tolerant IoU, stroke thickness) on a sheet.
- **متى أستخدمها / when:** مرجع بخط عربي مجهول — a reference with an unknown Arabic face.
- **كيف / how:** mm_fonts.match('work') at NORM_H 64 → spec.texts[i].font + sheets/fonts_evNN.png; mimic fonts PROJECT/study → fonts.jpg to pick visually (Naskh/Thuluth/Kufi/Diwani). Top scores are often close (≈0.334–0.339 in the Friday study) — always confirm on the sheet. **أرقام / params:** NORM_H 64.
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/scripts/mm_fonts.py` · `100-superskills/skills/kosif-mimic/scripts/mm_fonts.py:1` · `kosif-one/projects/mimic-jumuah/study/mimic.json`

#### ARAB-87 · ملاءمة العرض والتصغير التلقائي · Fit-width & shrink-to-fit · 🟢 جاهز / ready
- **ماذا / what:** حجم واحد يجعل أطول سطر يملأ 96% من العرض، أو تصغير تدريجي حتى يدخل النص في عدد أسطر محدد. — One shared size so the longest line fills 96% of the width, or stepwise shrinking until text fits a row budget.
- **متى أستخدمها / when:** عناوين متغيرة الطول ونصوص المستخدم — variable-length titles and user text.
- **كيف / how:** mimic text_style.fit_width .96; Basma TX.layout lays rows RTL from the right (space × 1.08, per-word centre x) and TX.fitLayout multiplies size by 0.9 up to 14 times until rows ≤ maxRows, lh 1.42·size; wbcompat textfit shrinks 1 px at a time to 84% width (min 9 px) then truncates; carousels stop at 4 lines. **أرقام / params:** fit .96; ×0.9 ×14; lh 1.42; 84% width.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/wbcompat.py:268` · `app/public/js/10_studio.js:182` · `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### ARAB-88 · نص مشكّل في المشاهد المرسومة واستيراد SVG · Shaped text in painted scenes & SVG import · 📄 موصوف / documented only
- **ماذا / what:** عملية نص في استوديو الرسم ترسم العربية بحجم الإخراج (حادة حتى 4K) بتعبئة متدرجة، وتستورد ‎<text>‎ من SVG. — A painter-scene text op drawing Arabic at output size (sharp to 4K) with gradient fills, plus SVG <text> import.
- **متى أستخدمها / when:** مشاهد مرسومة بالكود في KOSIF Studio — code-painted scenes.
- **كيف / how:** text(s, x, y, size, colour|gradient, anchor 'ms'|'mm'|'ls'|'rs', bold, family 'sans'|'serif'|'mono', alpha, mode), supersampled; SVG <text>/<tspan> import honours font-size, text-anchor, weight ≥600 and gradient fills (first stop). Caveat in this container: its font table points at Windows files (Segoe UI/Arial/Tahoma) and falls back to Pillow's default font on Linux — map it to an OFL Arabic file before trusting it. **أرقام / params:** anchors ms/mm/ls/rs; weight ≥600 → bold.
- **الدليل / proof:** `kosif-studio/render.py:446` · `kosif-studio/svg_import.py:369` · `kosif-studio/scenes/ad_whole_sheep.py:99` · `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### ARAB-89 · طبقات نص عربي على Canvas · Canvas RTL text-layer helpers · 🟢 جاهز / ready
- **ماذا / what:** دوال ترسم العربية كلمات كاملة باتجاه تلقائي وحدّ وشفافية، وطبقات نص بنسب من الإطار حتى 5 أسطر. — Helpers that draw Arabic as whole words with auto direction, stroke and alpha, plus text layers sized in frame percentages up to 5 lines.
- **متى أستخدمها / when:** محررات ومشاهد Canvas — canvas editors and scenes.
- **كيف / how:** U.text(str, x, y, size, color, {font, weight, align, alpha, stroke}) sets ctx.direction='rtl' when Arabic is detected, round-joined stroke; U.width() measures (default Lalezar → Cairo). Studio layer: weight 700, textAlign center, shadow #0009 blur 15, ≤5 lines split on \n at lh 1.35·size, max width 91%, ≤180 chars, size 2–60% of the short side (default 7%), x/y 0–100%. Playbook: ctx.textAlign='right' + fillText(wholeString) — the browser shapes it. **أرقام / params:** ≤5 lines; lh 1.35; max width 91%; size 2–60%.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:76` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:158` · `app/public/js/00_editor.js:17` · `kosif-tool/playbooks/arabic-typography.md:65`

#### ARAB-90 · دوران كتلة النص 90° ككاميرا · Type-block 90° rotation as camera move · 💡 فكرة / idea
- **ماذا / what:** تدور كتلة النص العربي كلها 90° كأن الكاميرا انقلبت، ويُكمل السطر التالي على المحور الجديد. — The whole Arabic text block rotates 90° as if the camera rolled, and the next line continues on the new axis.
- **متى أستخدمها / when:** شوريلات التايبوغرافي وانتقالات بين الأفكار — type showreels and idea transitions.
- **كيف / how:** Untested idea from a brief: rotate the block (never single letters) 90° with a band of background at 60% to hide the turn; lay the next line out on the rotated axis; keep each word whole. **أرقام / params:** 90°; band = bg at 60%.
- **الدليل / proof:** `kosif-tool/styles/pm-zheke-38deff/BRIEF.md`

## توليفات قوية / power combos

- **ريل كلام بترجمة كاريوكي / talking reel:** ARAB-62 + ARAB-68 + ARAB-34 + SYNC (words.json من التفريغ) + BEAT (خفض الموسيقى تحت الصوت) — الكلمة المنطوقة تتلون، والكلمة المنبورة تضرب فوقها بقناع صاعد في 0.34 s، والصوت الأصلي لا يُمس.
- **فيلم دعاء ليلي / night dua film:** ARAB-66 + ARAB-67 + ARAB-28 + ARAB-39 + GLOW (أشعة ضوء) + PART (غبار) + VOICE (بلا موسيقى) — أسطر مقسومة عند الوقفات، كلمات تنقلب من العمق بتعبئة ذهبية، والتلاوة بلا مرافقة.
- **سبورة تعليمية / whiteboard explainer:** ARAB-22 + ARAB-11 (Marhey/Lalezar) + DRAW (رسم بالماركر والتهشير) + CAM (اقتراب لكل جزء) — العنوان يُكتب من اليمين برأس ماركر ثم تُرسم الأشكال بلونها وتسمّى بالعربية — كما في style:whiteboard.
- **ريل شرح بثلاث طبقات / layered explainer:** ARAB-40 + ARAB-54 + ARAB-19 + TRANS (الكلمة الضخمة كسطح انتقال) + EASE (expo.out / power4.inOut) — ترجمة صغيرة، كلمات مفتاحية كبيرة، رقائق أقسام، وكلمة 400 بكسل تمسح إلى المشهد التالي.
- **رحلة على خريطة / map journey:** ARAB-80 + ARAB-11 (Aref Ruqaa + Amiri) + ARAB-73 + MAP (رسم المسار) + DATA (عدّاد المسافة) — أسماء المدن بخط رقعة مُسقطة على الخريطة، والعداد بأرقام جدولية من نظام واحد — كما في style:map-journey.
- **غلاف بلا تشويه / generated cover:** GEN (لوحة بلا نص) + ARAB-09 + ARAB-59 + COLOR — الصورة المولدة بلا حروف، والعنوان العربي يُكتب فوقها مشكّلًا بـ RAQM.
- **إطلاق منتج / product launch:** ARAB-30 + ARAB-31 + ARAB-29 + ARAB-39 + UI (نافذة واجهة ثلاثية) — كلمة وعد ضخمة تنكمش لجملة، كبسولة أيام←دقائق، آلة كاتبة في مربع الأوامر، وكلمة مفتاحية بتدرج — كما في style:product.
- **«اعمل مثل هذا» / match a reference:** ARAB-84 + ARAB-85 + ARAB-86 + FOOT (المرجع) + QA (ورقة لقطات قبل/بعد) — تقيس ستايل النص وحركته وتطابق الخط، ثم تعيد التشغيل بنص المستخدم وتتحقق على ورقة لقطات.
- **إنفوغراف أرقام / number infographic:** ARAB-77 + ARAB-73 + ARAB-75 + ARAB-76 + DATA (عدّاد بأعمدة أرقام دوّارة) — الرقم يُقرأ من السكربت، يعدّ بأرقام جدولية، ثم يتنحى لجملة صحيحة الجمع ومصدر.

## أخطاء ممنوعة / never do

1. **لا تقسم العربية إلى حروف (SplitText chars، span لكل حرف، typewriter بالـ spans)** — الحروف تنفصل وتظهر بأشكالها المعزولة — حرّك الكلمة أو استخدم قناعًا (ARAB-01/21).
2. **لا letter-spacing ولا حركة «انكماش التتبع» ولا scaleX على العربية** — يقطع الوصل ويشوّه الضربات؛ الإطالة بالكشيدة أو wdth فقط (ARAB-03).
3. **لا dir="rtl" على <html> في صفحات تُرندر** — HyperFrames يُخرج فيديو أسود صامتًا؛ ضع الاتجاه على عناصر النص (ARAB-02).
4. **لا تشكّل النص مرتين (arabic_reshaper + bidi ثم Pillow RAQM)** — جربتها هنا: الكلمات والحروف تنقلب. ولا تثبّت arabic-reshaper في هذه الحاوية فأدوات الغلاف والكاروسيل تسقط حاليًا إلى RAQM الصحيح (ARAB-06).
5. **لا drawtext لنص عربي في ffmpeg** — جربتها هنا: FriBiDi يحوّل إلى أشكال العرض فتظهر مربعات فارغة مكان الحروف المنفصلة (ا، إ، ر) مع Cairo؛ استخدم ass/subtitles (ARAB-62).
6. **لا Encoding ثابت (1) في نمط ASS مع تلوين كلمة** — جربتها هنا: ترتيب الكلمات ينعكس إلى «الموسيقى يسمع كل إطار»؛ استخدم −1.
7. **لا ترندر قبل تحميل الخطوط، ولا تعتمد على خطوط النظام هنا** — يُخبز الخط البديل؛ fc-list لا يجد خطًا عربيًا نظاميًا في هذه الحاوية (ARAB-04/13).
8. **لا تطلب من مولد صور أو فيديو كتابة العربية** — يشوّه الحروف؛ ولّد بلا نص وضع طبقة نص حقيقية (ARAB-09).
9. **لا تبثق العربية كهندسة 3D من خط غير مشكّل** — تخرج الحروف مفككة ومعكوسة؛ استخدم CanvasTexture أو طبقة HTML (ARAB-10).
10. **لا scramble بمجموعة حروف لاتينية على نص عربي** — دالة scramble في motion-kit تستخدم A–Z وأرقامًا افتراضيًا، فتظهر حروف لاتينية داخل الكلمة؛ مرّر pool عربيًا أو استخدم قناعًا.
11. **لا أقنعة ضيقة بلا هامش سفلي** — تقص النقاط والكسرة؛ حشوة .18em ومسافة 0.15–0.25em (ARAB-05).
12. **لا تخلط نظامي أرقام ولا تترك رقمًا غير معزول ولا تخترع رقمًا** — الترتيب ينقلب داخل الجملة، والرقم المخترع يكسر الثقة (ARAB-72/73/77).

## أقوى 5 حركات توقيع / 5 signature moves

1. **ARAB-19 — أقنعة الكلمات:** أول ما تمد يدك إليه لأي عنوان: 0.7 s، فاصل 0.07 s، expo.out — عربي آمن ومختبر في قالب title-card.
2. **ARAB-62 — كاريوكي ASS بنمط reels:** حدث لكل كلمة، تمييز #FFDE59 ونبضة 112%→100% في 120 ms، Encoding −1 — ترجمة ريلز مضمونة الترتيب بلا متصفح.
3. **ARAB-34 — ضربة الكلمة المفتاحية:** 0.94→1، ضبابية 10→0، قناع ينفتح للأعلى في 0.34 s — على الكلمة التي يختارها ARAB-68.
4. **ARAB-22 — كتابة بقناع ناعم ورأس قلم:** العربية تُكتب من اليمين بحافة 4–8% وماركر يتبعها — توقيع الشرح التعليمي.
5. **ARAB-66 — فيلم الكلمات من الصوت:** أغنية أو دعاء ← أسطر بالبرمجة الديناميكية، كلمات مفتاحية بالنبر، كلمات من العمق، وضوء يقوده الصوت.

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### ARAB-X01 · كشف الكلمة العربية كاملة من اليمين · RTL whole-word lyric reveal with key-word pop · 📄 موصوف / documented only
- **ماذا / what:** كل كلمة عربية تنكشف كاملة بقناع يتحرك من اليمين إلى اليسار قبل نطقها بقليل، والكلمة المفتاحية أكبر وتنبض وتلمع بذهب متحرك. — Each Arabic word is revealed whole by a mask moving right to left just before it is sung; the key word is larger, pops and carries a moving gold sheen.
- **متى أستخدمها / when:** فيلم كلمات أغنية أو شعر عربي — an Arabic lyric or poetry film.
- **كيف / how:** canvas direction = 'rtl'; a clip rect grows right → left with an eOut3 curve over 0.5 s, starting 0.1 s before the word; rise 34 px; key word ×1.3 with a decaying pop 1 + 0.08·e^(−Δt/0.35) and a moving gold gradient; the active word gets an additive glow; exit with blur ≤ 10 px and rising seeded gold sparks. Letters are never split, so Arabic joining survives. **أرقام / params:** mask 0.5 s from −0.1 s; rise 34 px; key ×1.3, pop 0.08·e^(−Δt/0.35).
- **الرخصة / license:** owner (song audio and lyrics are third-party; not included)
- **المصدر / source:** `owner-upload:film_project/film/film.js`
- **الدليل / proof:** `owner-upload:film_project/film/film.js`

#### ARAB-X02 · ترشيح الخط لا الجزم به · Font matches are candidates, not identities · 📄 موصوف / documented only
- **ماذا / what:** عند تقليد فيديو لا تقل «هذا الخط هو X» دون دليل؛ قدّم مرشحين بدرجة ثقة، وتأكد من الاحتياطي اللاتيني كي لا تظهر مربعات فارغة. — When imitating a video never state 'this font is X' without evidence; offer ranked candidates, and make sure there is a Latin fallback so no empty boxes appear.
- **متى أستخدمها / when:** محاكاة فيديو مرجعي أو مطابقة هوية بصرية — imitating a reference video or matching a visual identity.
- **كيف / how:** Report font candidates with evidence (shapes compared, sample frames); shape Arabic through HarfBuzz/RAQM; check mixed Arabic + Latin + digits in every label. Lesson from the owner's catalog renderer: a single Arabic font with no Latin fallback drew tofu boxes for 'Parallax', 'BPM', 'WebGL' inside Arabic labels.
- **الرخصة / license:** owner
- **المصدر / source:** `owner-upload:KOSIF_SEE_Humanizer_Optimize_Graphify_v1.7.5/skills/kosif-see/references/VIDEO_IMITATION_ROUTING_V1.md`
- **الدليل / proof:** `owner-upload:KOSIF_SEE_Humanizer_Optimize_Graphify_v1.7.5/skills/kosif-see/references/VIDEO_IMITATION_ROUTING_V1.md` · `session-2026-10-16:see-atlas#11.7`

#### ARAB-X03 · الزخرفة والكشيدة للنبذة فقط · Unicode ornaments and kashida: bios only · 📄 موصوف / documented only
- **ماذا / what:** النص المزخرف بالرموز والمطوّل بالكشيدة يصلح لنبذة حساب، لكنه يكسر تشكيل الحروف العربية في الفيديو المرندر. — Ornament-wrapped and kashida-stretched text is fine for a social bio but breaks Arabic shaping in rendered video.
- **متى أستخدمها / when:** طلب «زخرفة اسم» أو نص مزين لمنصة — a request to 'decorate a name' or style text for a platform.
- **كيف / how:** Generate decorated bio text inline when asked (frames, stars, crescents, kashida), but in motion graphics animate real words with real fonts and stretch with font features or layout, never with tatweel characters. This is the useful core of the owner's 150 text-decoration methods (30 base styles × 5 variants).
- **الرخصة / license:** owner
- **المصدر / source:** `owner-upload:kosif-tool-ultra/kosif-500-methods.json`
- **الدليل / proof:** `session-2026-10-16:motion-leftovers#5` · `owner-upload:kosif-tool-ultra/kosif-500-methods.json`
