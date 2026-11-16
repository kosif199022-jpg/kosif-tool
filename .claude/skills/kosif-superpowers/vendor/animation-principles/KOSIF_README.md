# Animation Principles داخل KOSIF Superpowers

مستودع [`dylantarre/animation-principles`](https://github.com/dylantarre/animation-principles) لديلان تار (رخصة MIT، © 2024 Dylan Tarre) منسوخ هنا من غير أي تعديل عند الـ commit `83597134ba8ff59838270f94d7ac7282ffa3b54d`: **144 مهارة** بتطبق مبادئ ديزني الاثنا عشر للأنيميشن، في 12 تصنيف، ومعاها الشروحات في `docs/`. الرخصة الأصلية محفوظة في [`LICENSE`](LICENSE) جنب الملفات، وكل ملف ليه بصمة SHA-256 في `KOSIF_INTEGRATION.json`.

Dylan Tarre's repository is copied here unchanged: 144 skills that apply Disney's 12 principles of animation, in 12 categories, plus their docs. The original MIT licence stays in `LICENSE`. The upstream `CLAUDE.md` is kept as `UPSTREAM-CLAUDE.md` so it is not loaded as this repository's instructions.

## الاستخدام / Use

من فولدر المهارة `.claude/skills/kosif-superpowers/`:

```bash
python3 scripts/hub.py find "حركة زرار لما الماوس يقف عليه"              # الباب الأمامي بيعرض مهارات مبادئ الأنيميشن المناسبة
python3 scripts/animation_principles.py find "الأنيميشن بيدوّخ الناس"     # ترتيب الـ144 مهارة للطلب
python3 scripts/animation_principles.py list                               # كلها حسب التصنيف
python3 scripts/animation_principles.py show hover-interactions --full     # المنهج كامل
python3 scripts/animation_principles.py verify                             # كل ملف مطابق لبصمته
```

بعد ما تلاقي المهارة: اقرأ `skills/<category>/<slug>/SKILL.md` وطبّق منهجها على الشغل.

## التصنيفات / Categories

| الفولدر | التصنيف | العدد |
|---|---|---|
| `01-by-domain` | حسب المجال (ويب، موبايل، ألعاب، فيديو وموشن جرافيك، 3D…) | 12 |
| `02-by-thinking-style` | حسب طريقة التفكير | 12 |
| `03-by-role-persona` | حسب الدور (مصمم موشن، مطور، مخرج…) | 12 |
| `04-by-skill-level` | حسب المستوى | 12 |
| `05-by-animation-type` | حسب نوع الحركة (دخول، خروج، هوفر، تحميل، سكرول…) | 12 |
| `06-by-emotional-outcome` | حسب الإحساس المطلوب | 12 |
| `07-by-ui-element` | حسب عنصر الواجهة (زرار، قائمة، نافذة، كارت…) | 12 |
| `08-by-industry` | حسب الصناعة | 12 |
| `09-by-tool-framework` | حسب الأداة (CSS، GSAP، Framer Motion، Lottie، After Effects، Rive…) | 12 |
| `10-by-time-scale` | حسب المدة (من 0 لـ 2000+ ملي ثانية) | 12 |
| `11-by-principle-focus` | مبدأ واحد بعمق | 12 |
| `12-by-problem-type` | حسب المشكلة (دوخة، أداء، إتاحة…) | 12 |

## اللي اتعمل في KOSIF / KOSIF changes

- مفيش أي تعديل على ملفات المصدر (`kosif_patches` فاضية). اللي اتضاف: هذا الملف، `KOSIF_INTEGRATION.json`، والأداة `scripts/animation_principles.py`، والفهرس `data/animation_principles.json`، وربطها بـ `hub.py find`، ومجموعة `animation` في `scripts/skills_lint.py`، وسطر في `THIRD_PARTY_NOTICES.md`.
- مش منسوخ: فولدر `.github/` بتاع المستودع الأصلي (قوالب issues وتمويل)، و `.gitignore` و `CONTRIBUTING.md`.
- تحديث من المصدر: `python3 scripts/animation_principles.py sync --src <checkout> --commit <sha>` ثم `verify`.
