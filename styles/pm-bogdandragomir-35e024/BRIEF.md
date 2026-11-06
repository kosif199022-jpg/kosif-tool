# تعريف بمنتج قراءة بأسلوب الحبر الإلكتروني وانتقالات تحبب — Product intro synced to music

> تعريف منتج مدته 15 ثانية بأسلوب الحبر الإلكتروني: يبدأ بكبسولة حبر مجهرية تمتلئ بحبيبات بيضاء وسوداء ثم تنفرط إلى شاشة من البكسلات، وكل فصل يُبنى ويُمحى بتحبب نقطي؛ أيقونات بريد ومقالات تُسحب كذيول من الجسيمات إلى قائمة، تُجمع في عدد مجلة على ورق فاتح، تصل إلى قارئ إلكتروني، ثم الشعار بخط سيريف.
>
> A 15-second e-ink style product intro: it opens on a microscopic ink capsule filling with white and black grains that bursts into a pixel screen, and every chapter builds and erases with a dithered pixel dissolve; mail and article icons trail particle tails into a list, gather into a magazine issue on light paper, land on an e-reader, then a serif logo.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-11-06)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-11-06); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://www.promptsmotion.com/bogdandragomir-35e024
- التصنيفات / Categories: product-ui, particles, kinetic-type, music
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, HTML Canvas, Web Audio

## الفكرة
الفكرة أن تحاكي الحركة نفسها طريقة عمل شاشة الحبر الإلكتروني: لا تلاشيات ناعمة، بل حبيبات تنقلب من أسود إلى أبيض. القصة ثلاث خطوات مرقمة (اجمع، لخّص، سلّم) ينتقل فيها المحتوى من الفوضى الرقمية الداكنة إلى ورق هادئ فاتح. الخط سيريف أدبي مع كلمة مائلة في كل عنوان.

## Concept
The motion itself imitates how an e-ink screen works: no smooth fades, just grains flipping between black and white. The story is three numbered steps (collect, digest, deliver), moving content from dark digital clutter to calm light paper. Type is a literary serif with one italic word per headline.

## المشاهد المقترحة
- 0-1.3 ث: فحمي داكن مع دوائر ضبابية خلفه؛ كبسولة حبر زجاجية تمتلئ بحبيبات بيضاء وداكنة تدوّم، وتعليق مائل صغير تحتها؛ والكاميرا تبتعد لتظهر حقلاً من الكبسولات.
- 1.3-2.5 ث: الكبسولة تنفجر إلى عاصفة بكسلات متحببة تملأ الشاشة ثم تستقر في تخطيط واجهة داكن.
- 2.5-5 ث: الخطوة الأولى: عنوان سيريف يساراً بكلمة مائلة، وعنوان بريد أعلى اليمين؛ أيقونات أظرف تطير بذيول من الحبيبات البيضاء وتسقط في القائمة كصفوف جديدة تُكتب.
- 5-7.5 ث: يتبدل العنوان؛ أيقونات مشاركة ورابط وإضافة متصفح وRSS تطير من الأطراف بذيول حبيبات وتضيف صفوفاً، وأحدث صف يتحول من تشويش إلى نص.
- 7.5-10 ث: مسح متحبب يحول الشاشة إلى الفاتح: الخطوة الثانية تعرض غلاف مجلة نظيفاً بقائمة محتويات مرقمة، وصفحات إضافية تنفتح كالمروحة خلفه.
- 10-12.5 ث: الخطوة الثالثة: العدد على قارئ إلكتروني رمادي؛ جهاز أسود ثانٍ ينزلق؛ والصفحة تتحدث بومضة أسود وأبيض إلى عرض مقال بحرف استهلالي كبير.
- 12.5-15 ث: حلقة بكسلات متحببة تتسع وتمسح إلى الأبيض؛ اسم المنتج بخط سيريف أسود كبير، شعار نصي مائل رمادي، والرابط ينفك من التشويش؛ وثبات.

## Proposed scenes
- 0-1.3s: Dark charcoal with blurred circles behind; a glass ink capsule fills with swirling white and dark grains, a tiny italic caption beneath; camera pulls back to show a field of capsules.
- 1.3-2.5s: The capsule bursts into a full-screen dithered pixel storm that resolves into a dark interface layout.
- 2.5-5s: Step one: a serif headline left with an italic word, an inbox address top-right; envelope icons fly in trailing tails of white grains and drop into the list as new rows typing in.
- 5-7.5s: Headline swaps; share, link, extension and RSS icons fly in from the edges with grain tails and add more rows, the newest row scrambling from noise into text.
- 7.5-10s: A dither sweep turns the screen light: step two shows a clean magazine cover page with a numbered contents list, extra pages fanning out behind it.
- 10-12.5s: Step three: the issue sits on a grey e-reader; a second black device slides in; the page refreshes with a black-white flash to an article view with a drop cap.
- 12.5-15s: A ring of dithered pixels expands and wipes to white; the product name in large black serif, an italic grey tagline and the URL that unscrambles from noise; hold.

## قواعد الحركة
- كل انتقال تذويب بكسلات متحبب (بنمط ترتيبي)، كمسح أو حلقة تتسع، في نحو 400-700 مللي ثانية؛ بلا تلاشيات شفافية ناعمة.
- ذيول الجسيمات: الأيقونات تسير على مسارات منحنية تجر خلفها 100-300 حبيبة بيضاء تستقر في الصف المستهدف.
- النص يظهر بالتحول من رموز عشوائية وتشويش إلى النص النهائي (نحو 300 مللي ثانية) أو بالكتابة.
- اللوحة: فحمي #1f1d1b، رمادي دافئ #2a2826، أبيض ورقي #f2f1ee، رمادي الحبر الإلكتروني #d9d6cf، أسود الحبر #151515، ونص خافت #8a8580.
- الخط: سيريف كتب انتقالي للعناوين بكلمة مائلة واحدة، ووسوم صغيرة متباعدة بأحرف كبيرة للخطوات مثل «01 · اجمع».
- تحديث الجهاز: ومضة سوداء ثم بيضاء كاملة داخل شاشة القارئ (نحو 120 مللي ثانية لكل منهما) كالورق الإلكتروني الحقيقي.

## Motion rules
- Every transition is a dithered pixel dissolve (ordered/Bayer-style), as a sweep or an expanding ring, over ~400-700 ms; no soft opacity fades.
- Particle tails: icons travel on curved paths trailing 100-300 white grains that settle into the target row.
- Text appears by scrambling from random glyphs/noise into the final string (~300 ms) or typing in.
- Palette: charcoal #1f1d1b, warm grey #2a2826, paper white #f2f1ee, e-ink grey #d9d6cf, ink black #151515, muted text #8a8580.
- Type: transitional book serif for headlines with one italic word, small tracked uppercase sans for step labels like '01 · collect'.
- Device refresh: a single black-then-white full flash inside the e-reader screen (~120 ms each), like real e-paper.

## Facts stated by the source (rewritten in our words)
- The video introduces a product and is meant to be synced to music.
- The record tags product UI, music and code; the prompt is about 33 words.

## Assumptions
Observed from 24 frames sampled every ~0.63 s across 15 s: the ink capsule open, dithered pixel transitions, particle-tailed icons filling an inbox list, the magazine issue, the e-reader refresh and the serif logo close. Assumed: that transitions land on music beats (an audio track exists but was not analysed), the exact dither algorithm and hex values.

## Keywords
e-ink, dither transition, pixel dissolve, product intro, newsletter, e-reader, particle trails, serif editorial, text scramble, حبر إلكتروني, انتقال تحبب, قارئ إلكتروني, تعريف منتج, خط سيريف
