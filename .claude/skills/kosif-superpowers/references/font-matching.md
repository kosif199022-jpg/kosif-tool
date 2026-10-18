# Font matching — مطابقة الخطوط

Part of the **arabic** and **observe** superpowers: how to identify the typeface a reference uses, pick the closest open-licensed face, and — when one family cannot cover every role — assemble a matched family under the SIL Open Font License. Worked example: [`fonts/kosif-jumuah/`](../../../../fonts/kosif-jumuah/README.md), built for a Friday-greeting video (Amiri Arabic + Bodoni Moda figures).

**بالعربية:** كيف تتعرّف على خط المرجع، وتختار أقرب خط مفتوح الرخصة، وتجمّع عائلة مطابقة برخصة OFL عندما لا يغطي خط واحد كل الأدوار. المثال المنفَّذ: `fonts/kosif-jumuah/`.

## 1. Observe the type — ارصد الخط

1. Fetch permitted frames (`scripts/fetch_reference.py`, or `ffmpeg -ss T -i reference.mp4 -frames:v 1 frame.png` on the user's file).
2. Mask each text colour (white: all channels ≥ 215; a brand colour: distance to its hex) and read the line boxes: height, width, centre, mean colour. Store them as fractions of the frame so they survive a change of resolution.
3. Note the signatures that identify a face faster than metrics: stacked ligatures (جم، محمد، الله), the shape of ك / ة / ع, diacritic placement, the ﷺ form, old-style versus lining figures, ball terminals, hairline contrast, kashida use.

**بالعربية:** اقتطع الإطارات، اعزل لون كل نص لقياس صناديق السطور كنِسب من الإطار، وسجّل البصمات (المركّبات المتراكبة، أشكال ك/ة/ع، التشكيل، شكل ﷺ، نوع الأرقام، التباين).

## 2. Render the candidates — اعرض المرشّحين

Write a spec and run the harness; it embeds each font, shapes the text with HarfBuzz and screenshots a tight crop:

```bash
node .claude/skills/kosif-superpowers/scripts/render_text.cjs spec.json out/
```

```json
{"width": 1600, "height": 300, "background": "#000", "items": [
  {"id": "amiri-b__gold", "text": "ليلة جمعة مبـــاركة", "font": "/abs/Amiri-Bold.ttf", "weight": 700, "size": 48, "color": "#fff"},
  {"id": "noto-700__gold", "text": "ليلة جمعة مبـــاركة", "font": "/abs/NotoNaskhArabic[wght].ttf", "weight": 700, "size": 48, "variation": "'wght' 700"},
  {"id": "bodoni__date", "text": "22.08.2025", "font": "/abs/BodoniModa[opsz,wght].ttf", "size": 48, "direction": "ltr", "variation": "'wght' 400, 'opsz' 11"}
]}
```

Candidate pools that cover most Arabic references (all OFL, from the google/fonts repository): Naskh — Amiri, Amiri Quran, Scheherazade New, Noto Naskh Arabic, Lateef, Markazi Text; Kufi/geometric — Reem Kufi, Noto Kufi Arabic, Cairo, Tajawal, Almarai, Readex Pro, IBM Plex Sans Arabic; display/hand — Aref Ruqaa, Lalezar, Rakkas, Katibeh, Mirza, Jomhuria. Latin figures — Bodoni Moda, Playfair Display, Cormorant, Libre Caslon, Inter, Roboto.

**بالعربية:** اكتب ملف المواصفات وشغّل الأداة؛ تضمّن كل خط وتشكّله بـ HarfBuzz وتلتقط قصاصة ضيقة. المجموعات المرشّحة أعلاه تغطي أغلب المراجع العربية.

## 3. Decide — قرّر

- Build side-by-side sheets with Pillow: the video crop on top, each candidate scaled to the same width below. Signatures decide; metrics (width ratios between lines, ink height ÷ width) are tie-breakers only, because kashida, shadows and compression distort them.
- Record the verdict in STYLE.md as *observed* (what matched) and *assumed* (weight read through blur, a hand-lettered title, a face you could not identify).
- When no open face matches a role (Thuluth titles, custom lettering), say so, propose a calligrapher or a licensed face, and keep the nearest open face as the consistent fallback.

**بالعربية:** لوحات مقارنة جنبًا إلى جنب، والبصمات تحسم والقياسات تُرجّح فقط. سجّل في STYLE.md ما طابق وما افترضته، وصرّح حين لا يوجد خط مفتوح يطابق دورًا ما.

## 4. Assemble a matched family — جمّع عائلة مطابقة

When the Arabic and the figures come from different designs, merge two OFL masters with fontTools (`pip install fonttools brotli`) — the kit's `build_font.py` is the template: subset each master to disjoint Unicode ranges (Arabic blocks from one, Latin from the other), instance variable fonts to static weights, scale to a common UPM, copy the Arabic vertical metrics onto the Latin master so line boxes stay stable, merge, then write the name table with a **new family name**, both copyright notices and the OFL text. Never reuse a Reserved Font Name; ship `OFL.txt`; set `fsType` to 0 only when both sources allow installable embedding (OFL does).

Verify: render the merged font over the same lines with the harness and compare with the crops again; check `GSUB` survived (shaping, ligatures), the required code points (letters, tatweel U+0640, ﷺ U+FDFA, digits, punctuation) and both weights.

**بالعربية:** اقتطع كل مصدر إلى نطاقات يونيكود منفصلة، ثبّت الأوزان، وحّد وحدات القياس والمقاييس الرأسية، ادمج، ثم اكتب جدول الأسماء باسم عائلة جديد مع حقوق المصدرين ورخصة OFL. لا تعد استخدام اسم محجوز. وتحقّق بعرض الخط المدمج ومقارنته مجددًا.

## 5. Pitfalls — مزالق

- `@font-face` from `file://` fails silently under `page.setContent`; embed the font as a data URL (the harness does) or open the page with `--allow-file-access-from-files` (as `tools/render_html.cjs` does).
- Diacritics on stacked ligatures float high in Amiri; drop them in display titles or set the word unstacked.
- Pillow cannot shape Arabic without libraqm — render through Chromium, measure with Pillow.
- Bidi: a Latin handle inside an RTL paragraph reorders its "@"; give such spans `direction: ltr`.
- Emoji come from the platform's colour font; list it as a fallback family.
- Licensing: copy no glyph outlines from the reference; identify, then use the open face. A reference's own font may be commercial — name it as an option, never vendor it.

**بالعربية:** خطوط `file://` لا تُحمَّل تحت `setContent` فضمّنها كـ data URL؛ التشكيل يعلو فوق المركّبات المتراكبة؛ Pillow لا يشكّل العربية فاعرض عبر Chromium؛ المعرّف اللاتيني يحتاج `direction: ltr`؛ لا تنسخ حدود الحروف من المرجع أبدًا.
