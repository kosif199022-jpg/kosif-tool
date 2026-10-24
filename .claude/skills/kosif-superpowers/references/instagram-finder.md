# باحث فيديوهات إنستجرام للمنتجات — Instagram product video finder

`scripts/instagram_finder.py` يدوّر جوه إنستجرام على فيديوهات تناسب منتج بتطلبه (بالعربي أو الإنجليزي)، ويحمّل اللي تختاره عن طريق أداة التحميل المدمجة `scripts/fetch_video.py` (yt-dlp).

`scripts/instagram_finder.py` finds Instagram videos that fit a product you name (Arabic or English) and downloads the ones you pick through the built-in downloader `scripts/fetch_video.py` (yt-dlp).

## الفكرة: فهرس محلي بدل بحث مقفول — The idea: a local index

إنستجرام مفيهوش بحث بالكلمات في بوستات الناس يتنفع يستخدمه سكربت من غير تسجيل دخول، وأداة yt-dlp معلّمة استخراج صفحات الحسابات عندها «CURRENTLY BROKEN». عشان كده الأداة بتبني **فهرس محلي** (`out/instagram/index.json`، مش بيترفع على git) من خمس مصادر، وبعدين بتبحث فيه هو:

| المصدر | الأمر | المحرك | محتاج |
|---|---|---|---|
| الحسابات المحفوظة (`data/instagram_sources.json`) | `index` | instaloader | جلسة حسابك (`instaloader -l USER`) غالبًا |
| هاشتاج | `index --hashtag perfume` | instaloader | جلسة حسابك إجباري |
| روابط ريلز لقيتها بنفسك أو من بحث الويب | `add-posts URL…` | yt-dlp | لا، أو `--cookies` |
| خطة بحث للويب (Google/DuckDuckGo `site:instagram.com/reel`) | `plan "منتج"` | بدون شبكة | — |

كل بوست في الفهرس معاه: الكابشن، الهاشتاجات، **الوصف التلقائي للصورة** اللي إنستجرام بيكتبه (`accessibility_caption`، زي «May be an image of perfume and bottle» — ده بيدّي مطابقة على *محتوى الصورة* مش الكلام بس)، التاريخ، المشاهدات، المدة، والصورة المصغّرة.

### الترتيب الذكي — How ranking works
- **توسيع ثنائي اللغة:** كل كلمة في طلبك بتتوسّع بمرادفاتها من `data/instagram_synonyms.json` — «برفان» تلاقي `#perfume` و«fragrance»، و«كوتشي» تلاقي «sneakers». ضيف مجموعات براحتك.
- **تطبيع عربي:** بيشيل التشكيل والتطويل، يوحّد أ/إ/آ → ا، ى → ي، ة → ه، ويشيل «ال/وال/بال».
- **الأوزان:** هاشتاج مطابق 3، جزء من هاشتاج مركّب (`#perfumephotography`) 2، كلمة في الكابشن 2، وصف الصورة 1.5، تشابه جزئي 1؛ المرادف بـ0.7 من الكلمة الأصلية. بعدين بيتضرب في نسبة كلمات طلبك اللي اتغطّت، ومكافأة لو العبارة كلها موجودة، ومكافأة صغيرة للمشاهدات.
- **فلاتر:** فيديو بس افتراضيًا (`--include-photos` للصور)، `--account`، `--min-dur/--max-dur` بالثواني، `--since YYYY-MM-DD`.
- كل نتيجة معاها `why` بيقولك اتطابقت ليه (`#perfume`, `caption:عطر`, `image:bottle`).

### شوف قبل ما تحمّل — Look before you download
`thumbs` بينزّل الصور المصغّرة لأحسن النتايج في `out/instagram/thumbs/` عشان تبصّ عليها (أو Claude يفتحها ويحكم بصريًا) قبل تحميل الفيديو الكامل.

## الأوامر — Commands
```bash
cd .claude/skills/kosif-superpowers
pip install instaloader yt-dlp curl_cffi          # مرة واحدة
python3 scripts/instagram_finder.py doctor
python3 scripts/instagram_finder.py accounts       # الحسابات المحفوظة
python3 scripts/instagram_finder.py add-account "https://www.instagram.com/name?igsh=xyz" --tag product
python3 scripts/instagram_finder.py plan "عطر رجالي"          # كلمات + هاشتاجات + روابط بحث ويب

instaloader -l MY_USERNAME                          # مرة واحدة على جهازك: يحفظ جلستك
python3 scripts/instagram_finder.py index --session-user MY_USERNAME --limit 40
python3 scripts/instagram_finder.py add-posts https://www.instagram.com/reel/XXXX/ --cookies cookies.txt

# أسهل وأأمن: استخدم تسجيل دخولك من المتصفح اللي على جهازك (الكوكيز ماتخرجش من الجهاز ومش بتتحفظ)
python3 scripts/instagram_finder.py index --browser chrome
python3 scripts/instagram_finder.py add-posts https://www.instagram.com/reel/XXXX/ --cookies-from-browser chrome

python3 scripts/instagram_finder.py search "عطر سبلاش سلوموشن" --max-dur 30 --save out/instagram/hits.json
python3 scripts/instagram_finder.py thumbs out/instagram/hits.json --top 8
python3 scripts/instagram_finder.py download out/instagram/hits.json --pick 1,4 \
    --rights permission --evidence "إذن مكتوب في DM بتاريخ 2026-10-24"
python3 scripts/instagram_finder.py download out/instagram/hits.json --top 3 --rights reference-only --dry-run
```
`download` بيشغّل `fetch_video.py` لكل رابط (بنسخة `.safe.mp4` H.264/AAC افتراضيًا)، ويكتب `instagram_rights.jsonl` فيه الرابط والحساب (للـcredit) والملف والحق اللي أعلنته والدليل.

## مثال كامل — Worked example
عايز فيديوهات لـ«ساعة يد فخمة» من الحسابات المحفوظة:
1. `plan "ساعة يد فخمة"` → بيطلع `#watch`, `#watches`, `#watchphotography`… وروابط بحث `site:instagram.com/reel`.
2. `index --session-user me` → يقرأ آخر 40 بوست من كل حساب من الخمسة (8 ثواني بين كل حساب).
3. افتح روابط البحث، وانسخ الريلز الحلوة: `add-posts <links>`.
4. `search "ساعة يد فخمة" --save out/instagram/hits.json` → قائمة مرتبة بسبب كل نتيجة.
5. `thumbs … --top 8` → بص على الصور.
6. `download … --pick 2,5 --rights permission --evidence "<رابط الإذن>"`.

## الحسابات المحفوظة — Saved source accounts
محفوظة في `data/instagram_sources.json` من غير باراميترات التتبع (`cplk`, `xtok`, `dlrf`, `obrf`, `rpxt`, `igsh`…):
`@mcydro`, `@ayman_mamdouh_ph`, `@suki.shotz`, `@asirgokerr`, `@brkn.land`.
وجود حساب هنا معناه إنه مصدر بنبحث فيه، **مش** ترخيص باستخدام محتواه.

## الحدود — Limits (اقرأها)
- **تسجيل الدخول:** إنستجرام غالبًا بيطلب تسجيل دخول لقراءة صفحات الحسابات والهاشتاجات. أسهل طريقة `--browser chrome` (للفهرسة) و`--cookies-from-browser chrome` (للروابط والتحميل): بتقرأ تسجيل دخولك من المتصفح اللي على جهازك من غير ما تنسخه أو تحفظه. أو جلستك (`instaloader -l`) أو `cookies.txt`. ماتلزقش الكوكيز في شات ولا تحفظها في المستودع: دي زي الباسورد. ويُفضّل حساب إنستجرام تاني مش الأساسي، لأن السحب الكتير ممكن يوقف الحساب مؤقتًا.
- **للسحابة (Claude on the web):** حط `INSTAGRAM_SESSIONID=<قيمة sessionid>` في Environment variables بتاعة بيئة المشروع (مع Full network access). الأداة بتقراها لوحدها: instaloader للفهرسة، وملف كوكيز مؤقت صلاحياته 0600 بيتمسح في آخر التشغيل لـyt-dlp. `doctor` بيقول إنها موجودة من غير ما يطبع قيمتها. أي حد يقدر يفتح إعدادات البيئة يقدر يشوفها، فاستخدم حساب تاني.
- **الريلز العامة من غير حساب:** رابط ريل عام غالبًا بيتحمّل بـyt-dlp من غير تسجيل دخول؛ صفحات الحسابات والهاشتاجات لأ.
- **الحسابات الخاصة:** مش هتشتغل غير لو حسابك متابعها ومقبول.
- **مفيش API رسمي هنا:** Instagram Graph API بيبحث في الهاشتاجات لحسابات Business بس وبموافقة تطبيق؛ الأداة مش بتستخدمه. instaloader وyt-dlp بيقروا الصفحات العامة، فممكن يقفوا لما إنستجرام يغيّر حاجة (`pip install -U instaloader yt-dlp`).
- **حدود المعدّل:** افتراضيًا 40 بوست لكل حساب (أقصى 200)، 8 ثواني بين الحسابات، 4 ثواني بين الروابط، 5 ثواني بين التحميلات، وأقصى 25 تحميل في التشغيلة (`--max` لحد 100). لو إنستجرام قال «استنى» (429) الأداة بتقف. ماتقلّلش الانتظار.
- **من السحابة:** في حاوية Claude هنا الوصول لـinstagram.com مقفول من البروكسي (403)، فالفهرسة والتحميل لازم يشتغلوا على جهازك. الاختبارات بتشتغل بـyt-dlp مزيّف.
- **الحقوق:** `--rights` إجباري: `owned` (محتواك)، `permission` أو `licensed` (لازم `--evidence`)، أو `reference-only` (مرجع خاص للدراسة والإلهام، ماينفعش يتنشر أو يتقص في شغل نهائي). شروط إنستجرام بتمنع إعادة نشر محتوى الغير من غير إذن؛ اكتب credit للحساب دايمًا.
- **الصور المصغّرة** روابطها بتنتهي بعد فترة؛ أعد `index`/`add-posts` لو `thumbs` فشل.
