# KOSIF Jumuah — خط «كوسيف جمعة»

A matched typeface for the Friday-greeting typography observed in a vertical reference video: Arabic Naskh with the stacked ligatures that give words like «جمعة», «محمد» and «اللهم» their calligraphic knot, the full ﷺ glyph, kashida support, and Didone figures for dates. It is assembled under the SIL Open Font License from **Amiri** (Arabic) and **Bodoni Moda** (Latin and digits), renamed as the license requires, and ships as Regular and Bold in TTF and WOFF2 with a seek-driven demo page.

**بالعربية:** خط مطابق لتايبوغرافيا تهنئة الجمعة في فيديو مرجعي عمودي: نسخ عربي بالمركّبات المتراكبة التي تمنح «جمعة» و«محمد» و«اللهم» عقدتها الخطية، ورمز ﷺ كاملًا، والكشيدة، وأرقام ديدون للتاريخ. جُمِّع برخصة SIL المفتوحة من خط **أميري** (العربية) و**Bodoni Moda** (اللاتينية والأرقام)، وأُعيدت تسميته كما تشترط الرخصة، ويأتي بوزنين Regular وBold بصيغتي TTF وWOFF2 مع صفحة عرض تعمل بالتمرير الزمني.

| file | content |
|---|---|
| `KOSIFJumuah-Regular.ttf` / `.woff2` | Amiri Regular Arabic + Bodoni Moda wght 400 / opsz 11 Latin |
| `KOSIFJumuah-Bold.ttf` / `.woff2` | Amiri Bold Arabic + Bodoni Moda wght 600 / opsz 11 Latin |
| `OFL.txt` | the license with both upstream notices |
| `build_font.py` | reproducible build (download → subset → instance → scale → merge → rename) |
| `demo/jumuah.html` | 1080×1920, 15.5 s, `window.__kosif.seek(t)` demo of the whole type system |
| `demo/preview.png` | 8-frame contact sheet rendered by `tools/render_html.cjs --preview` |

## 1. What was observed — ما لوحظ

Reference: 576×1024, 30 fps, 15.47 s, one hard cut at 1.7 s; measured on frames at 2.5 s, 7 s and 11.5 s with colour masks (white ≥ 215 on all channels; gold R > 170, G > 120, B < 130). Positions are fractions of the frame; *observed* means measured, *assumed* means inferred from stills.

| role | text | observed | decision |
|---|---|---|---|
| title | «الجُمُعَة» | white, right edge at 0.88 W, ink 0.32 W × 0.05 H, centre y 0.215 H, Thuluth-style composition with diacritics | *assumed* hand-set Thuluth lettering; no open-licensed Thuluth exists, so the kit uses KOSIF Jumuah Bold (Amiri's stacked «الجمعة») as the stand-in |
| date | «22.08.2025» | Didone figures with hairline serifs and ball terminals, "22" ≈ 1.4× the rest, right edge 0.885 W, centre y 0.28 H, ink 0.47 W × 0.033 H | Bodoni Moda, weight 400, optical size 11 (hairlines visible at phone size) |
| gold line | «ليلة جمعة مبـــاركة» | #f5cc76, centred, 0.50 W wide, centre y 0.385 H, three tatweels in «مباركة», stacked «جم» | Amiri Bold |
| body | «اللهم صل وسلم وبارك على / نبينا محمد ﷺ» … | #fcfbf9, centred, widest line 0.68 W, centre y 0.48–0.51 H, stacked «محمد», three-row ﷺ, soft dark shadow | Amiri Bold (the video's weight sits between Regular and Bold once compression blur is accounted for) |
| handle | «@…» | small Latin serif, centre y 0.60 H, 0.17 W, white at 92 % | the kit's Latin master; the video's face is a Times-like serif (*assumed*) |

**بالعربية:** العنوان خط ثلث مركّب (مفترض، لا يوجد خط ثلث مفتوح الرخصة)، التاريخ أرقام ديدون بشعيرات رفيعة، السطر الذهبي والنصوص البيضاء نسخ بمركّبات متراكبة وكشيدة ورمز ﷺ ثلاثي الصفوف، والمعرّف خط لاتيني مسنّن صغير.

## 2. How the match was made — كيف تمت المطابقة

1. **Frames → boxes.** `ffmpeg` contact sheet and full-resolution frames; colour masks gave each text line's box, centre and mean colour (table above).
2. **Candidates.** Twelve open Arabic faces (Amiri Regular/Bold, Amiri Quran, Scheherazade New Regular/Bold, Noto Naskh Arabic 400/700, Lateef, Markazi Text 400/700, Aref Ruqaa Regular/Bold) and six Latin faces (Bodoni Moda at three weight/optical-size settings, Playfair Display, Cormorant Garamond, Times) rendered the exact lines through Chromium (HarfBuzz shaping) with `.claude/skills/kosif-superpowers/scripts/render_text.cjs`.
3. **Fingerprints.** Size-independent ratios between line widths and heights were compared with the video; they are only a tie-breaker here because the video elongates several words with kashida.
4. **Signatures.** Side-by-side sheets settled it: the stacked «جم» in «جمعة», the stacked «محمد», the three-row ﷺ and the shapes of ك and ة appear only in Amiri among the candidates; Scheherazade and Noto set those words flat. For the date, Bodoni Moda's ball-terminal "2" and vertical-stress "0" match; Playfair's figures are old-style and Times is too plain.
5. **Verification.** The merged font was rendered again over the same lines and compared with the video crops; the demo page was rendered to a contact sheet with the repository's own renderer.

**بالعربية:** قياس الصناديق من الإطارات، ثم عرض السطور نفسها باثني عشر خطًا عربيًا وستة لاتينية عبر Chromium، ثم مقارنة النِّسب والبصمات البصرية: المركّبات المتراكبة في «جمعة» و«محمد» ورمز ﷺ لا تظهر إلا في أميري، وأرقام Bodoni Moda تطابق التاريخ. ثم أُعيد العرض بالخط المدمج للتحقق.

## 3. Build — البناء

```bash
pip install fonttools brotli
python3 fonts/kosif-jumuah/build_font.py            # downloads the sources into .kosif-cache/fonts-src, then builds
python3 fonts/kosif-jumuah/build_font.py --no-download --src path/to/sources
```

Steps performed by the script: fetch Amiri and Bodoni Moda from the google/fonts repository → subset Amiri to the Arabic blocks (U+0600–06FF, 0750–077F, 08A0–08FF, FB50–FDFF, FE70–FEFF, joiners) keeping all OpenType features → instance Bodoni Moda at wght 400/opsz 11 (Regular) and wght 600/opsz 11 (Bold), subset to Basic Latin, Latin-1 and general punctuation without layout tables → scale the Latin master to 1000 UPM and copy the Arabic vertical metrics → merge with `fontTools.merge` → write the name table (family *KOSIF Jumuah*, both copyrights, OFL 1.1) → save TTF and WOFF2 → write `OFL.txt`.

**بالعربية:** تنزيل المصدرين، اقتطاع أميري إلى كتل العربية مع إبقاء كل ميزات OpenType، استخراج وزن ثابت من Bodoni Moda واقتطاعه إلى اللاتينية، توحيد وحدات القياس والمقاييس الرأسية، الدمج، كتابة جدول الأسماء، ثم حفظ TTF وWOFF2 ورخصة OFL.

## 4. Use — الاستخدام

```css
@font-face { font-family: "KOSIF Jumuah"; font-weight: 400; src: url("fonts/kosif-jumuah/KOSIFJumuah-Regular.woff2") format("woff2"); }
@font-face { font-family: "KOSIF Jumuah"; font-weight: 700; src: url("fonts/kosif-jumuah/KOSIFJumuah-Bold.woff2") format("woff2"); }
.gold { font-family: "KOSIF Jumuah"; font-weight: 700; color: #f5cc76; }
.body { font-family: "KOSIF Jumuah"; font-weight: 700; color: #fcfbf9; text-shadow: 0 .012em .06em rgba(0,0,0,.55); }
.date { font-family: "KOSIF Jumuah"; font-weight: 400; direction: ltr; }
```

Type system of the reference, as fractions of the frame width (the demo fits these at load): title 0.32 W wide, date 0.47 W with the day at 1.42×, gold line 0.50 W, body lines 0.68 W for the widest line, handle ≈ 0.0165 H tall. Kashida is a plain U+0640 (`ـ`) repeated inside the word; Arabic shaping and the stacked ligatures come from the font's own GSUB, so nothing special is needed in HTML. Preview the demo with the repository renderer:

```bash
node tools/render_html.cjs --in fonts/kosif-jumuah/demo/jumuah.html --out out/preview.png --preview
node tools/render_html.cjs --in fonts/kosif-jumuah/demo/jumuah.html --out out/film.mp4 --fps 30
```

In a scaffolded film, copy the two WOFF2 files next to `index.html`, paste the `@font-face` block, and wait for `document.fonts.ready` inside `window.__kosifReady` so no frame renders with a fallback face.

**بالعربية:** ضع ملفي WOFF2 بجانب صفحة الفيلم، الصق كتلة `@font-face`، وانتظر تحميل الخطوط داخل `__kosifReady`. الكشيدة حرف U+0640 عادي داخل الكلمة، والمركّبات المتراكبة تأتي من الخط نفسه.

## 5. License — الترخيص

KOSIF Jumuah is licensed under the SIL Open Font License 1.1 (`OFL.txt`). It is a modification of Amiri (© The Amiri Project Authors, https://github.com/aliftype/amiri) and Bodoni Moda (© The Bodoni Moda Project Authors, https://github.com/indestructible-type/Bodoni); the Reserved Font Names "Amiri" and "Bodoni Moda" are not used for this derivative, as the OFL requires. You may embed it in films, websites and apps, modify it further and sell works made with it; keep the license file with any redistribution and do not sell the font files on their own.

**بالعربية:** الخط برخصة SIL المفتوحة 1.1؛ وهو تعديل لخطي أميري وBodoni Moda مع عدم استخدام اسميهما المحجوزين. يجوز تضمينه في الأفلام والمواقع والتطبيقات وتعديله وبيع الأعمال المصنوعة به، مع إبقاء ملف الرخصة وعدم بيع ملفات الخط وحدها.

## 6. Limits — الحدود

- The calligraphic title is a Thuluth composition that no open-licensed font reproduces; commission a calligrapher or license a Thuluth face for an exact match, and keep the kit's Bold as the consistent fallback.
- The reference's white text weight is read through compression blur; if a side-by-side at full size looks heavy, use Regular with the same shadow.
- Latin letters in the kit are Didone (Bodoni Moda) to match the date; the reference's small handle is a Times-like serif.
- Emoji (🤲 in the last line) come from the platform's colour emoji font, not from this family.

**بالعربية:** عنوان الثلث لا يعيده خط مفتوح؛ وزن النص الأبيض مقدَّر عبر ضبابية الضغط؛ الحروف اللاتينية ديدون لمطابقة التاريخ؛ والرموز التعبيرية من خط النظام.
