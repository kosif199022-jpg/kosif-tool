# دمج 114 مهارة — KOSIF Superpowers × 100 Super Skills

**المصدر:** [kosif199022-jpg/100-superskills](https://github.com/kosif199022-jpg/100-superskills)  
**إصدار مثبت:** `af7a5dc3778c0e68ef935349a5c1650d15688277`  
**المكان:** `.claude/skills/kosif-superpowers/vendor/100-superskills`  
**الفهرس:** `data/100-superskills-index.json` — 114 مدخلًا مطابقًا لمجلدات `skills/` في المصدر.

## ما الذي دُمج؟
جميع ملفات `100-superskills` (114 مجلد مهارة، ومنها SKILL.md والمراجع والسكربتات والأصول ومحتوى README) متاحة عبر **Git submodule مثبت على commit محدد**. الربط مقصود للمحافظة على الملفات الثنائية وكامل تاريخ النسخة دون نسخ ناقص أو تكرار أدوات KOSIF الموجودة. المحتوى لا يتحول تلقائيًا إلى أدوات فعّالة ولا تعني إضافته تثبيت الاعتماديات.

## التثبيت والتشغيل
من جذر `kosif-tool`:
```bash
git submodule update --init --recursive
python3 .claude/skills/kosif-superpowers/scripts/superskills_bridge.py doctor
python3 .claude/skills/kosif-superpowers/scripts/superskills_bridge.py list
python3 .claude/skills/kosif-superpowers/scripts/superskills_bridge.py find "مونتاج فيديو عربي"
python3 .claude/skills/kosif-superpowers/scripts/superskills_bridge.py show kosif-mimic
python3 .claude/skills/kosif-superpowers/scripts/skill_loader.py need "بناء نموذج مالي إكسل"
```
بدون submodule مُهيّأ، يبقى الفهرس للبحث والتوجيه فقط، وليست السكربتات جاهزة للتنفيذ.

## ضوابط التشغيل
المهارات تعليمات وأدوات متفاوتة؛ لا تدّعِ تشغيل برنامج أو سكربت إلا عند التحقق. لا تثبّت برامج مدفوعة أو تُنفّذ نشرًا أو تنفق رصيدًا من غير تصريح. راعِ التراخيص وحقوق الوسائط ومصدر كل أصل. قبل أي مهمة، ابدأ بالتوجيه ثم افتح `SKILL.md` المناسب، واستخدم التحقق والتقييم الموجودين في KOSIF.

## الفهرس الكامل (114)
| # | المهارة | المجال | رابط المصدر |
|---|---|---|---|
| 1 | `ab-testing-experiments` — اختبارات A/B والتجارب | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/ab-testing-experiments/SKILL.md) |
| 2 | `accessibility-wcag` — الإتاحة WCAG | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/accessibility-wcag/SKILL.md) |
| 3 | `accounting-ifrs-journal` — المحاسبة والقيود وIFRS | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/accounting-ifrs-journal/SKILL.md) |
| 4 | `ad-creative-30s` — الإعلان الإبداعي 30 ثانية | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/ad-creative-30s/SKILL.md) |
| 5 | `agent-tool-instructions` — تعليمات الوكلاء والأدوات | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/agent-tool-instructions/SKILL.md) |
| 6 | `ai-art-style-library` — مكتبة الأساليب الفنية للتوليد | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/ai-art-style-library/SKILL.md) |
| 7 | `arabic-copywriting` — الكتابة الإعلانية العربية | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/arabic-copywriting/SKILL.md) |
| 8 | `audio-mastering-analysis` — تحليل الصوت والماسترينغ | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/audio-mastering-analysis/SKILL.md) |
| 9 | `audio-reactive-captions-studio` — استوديو الصوت التفاعلي والترجمة المتحركة | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/audio-reactive-captions-studio/SKILL.md) |
| 10 | `automation-scripts-cli` — سكربتات الأتمتة وأدوات سطر الأوامر | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/automation-scripts-cli/SKILL.md) |
| 11 | `backend-api-design` — تصميم الواجهات الخلفية وAPI | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/backend-api-design/SKILL.md) |
| 12 | `book-to-skill-knowledge` — من الكتاب إلى مهارة | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/book-to-skill-knowledge/SKILL.md) |
| 13 | `brand-identity-logo` — الهوية البصرية والشعار | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/brand-identity-logo/SKILL.md) |
| 14 | `browser-automation-playwright` — أتمتة المتصفح بـ Playwright | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/browser-automation-playwright/SKILL.md) |
| 15 | `business-plan-prd` — خطة العمل ووثيقة المنتج | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/business-plan-prd/SKILL.md) |
| 16 | `character-animation-2d` — تحريك الشخصيات 2D | `motion-animation` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/character-animation-2d/SKILL.md) |
| 17 | `cinema-director-7layers` — المخرج السينمائي (7 طبقات) | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/cinema-director-7layers/SKILL.md) |
| 18 | `cinematic-3d-scene` — مشهد سينمائي ثلاثي الأبعاد | `motion-animation` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/cinematic-3d-scene/SKILL.md) |
| 19 | `claude-animation-studio` — استوديو الأنيميشن بكلاود | `motion-animation` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/claude-animation-studio/SKILL.md) |
| 20 | `cloudflare-edge-deploy` — النشر على Cloudflare والحافة | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/cloudflare-edge-deploy/SKILL.md) |
| 21 | `code-review-refactor` — مراجعة الكود وإعادة الهيكلة | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/code-review-refactor/SKILL.md) |
| 22 | `comics-picture-books` — القصص المصوّرة وكتب الأطفال | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/comics-picture-books/SKILL.md) |
| 23 | `context-window-budget` — ميزانية نافذة السياق | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/context-window-budget/SKILL.md) |
| 24 | `curriculum-course-builder` — بناء المناهج والدورات | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/curriculum-course-builder/SKILL.md) |
| 25 | `custom-gpt-claude-project` — بناء GPT مخصص ومشروع Claude | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/custom-gpt-claude-project/SKILL.md) |
| 26 | `dashboards-dataviz` — لوحات المعلومات والتصور البياني | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/dashboards-dataviz/SKILL.md) |
| 27 | `data-in-motion` — بيانات متحركة | `motion-animation` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/data-in-motion/SKILL.md) |
| 28 | `database-schema-migrations` — مخطط قاعدة البيانات والترحيلات | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/database-schema-migrations/SKILL.md) |
| 29 | `davinci-resolve-pipeline` — خط إنتاج DaVinci Resolve الاحترافي | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/davinci-resolve-pipeline/SKILL.md) |
| 30 | `debugging-root-cause` — تصحيح الأخطاء من الجذر | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/debugging-root-cause/SKILL.md) |
| 31 | `diagrams-mermaid-architecture` — المخططات والرسوم الهندسية | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/diagrams-mermaid-architecture/SKILL.md) |
| 32 | `docker-ci-devops` — Docker وCI/CD | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/docker-ci-devops/SKILL.md) |
| 33 | `ecommerce-store-listings` — المتجر الإلكتروني وأوصاف المنتجات | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/ecommerce-store-listings/SKILL.md) |
| 34 | `excel-automation-power` — أتمتة إكسل المتقدمة (Power Query وLAMBDA وDAX) | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/excel-automation-power/SKILL.md) |
| 35 | `excel-data-cleaning-automation` — تنظيف البيانات وأتمتة إكسل | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/excel-data-cleaning-automation/SKILL.md) |
| 36 | `excel-financial-models` — النماذج المالية في إكسل | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/excel-financial-models/SKILL.md) |
| 37 | `excel-model-architect` — مهندس النماذج المالية في إكسل | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/excel-model-architect/SKILL.md) |
| 38 | `excel-power-formulas` — إكسل: الصيغ والقوة | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/excel-power-formulas/SKILL.md) |
| 39 | `explainer-edu-animation` — أنيميشن تعليمي توضيحي | `motion-animation` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/explainer-edu-animation/SKILL.md) |
| 40 | `fact-checker-verifier` — مدقّق الحقائق والمُحقِّق | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/fact-checker-verifier/SKILL.md) |
| 41 | `few-shot-dataset-curation` — تنسيق الأمثلة ومجموعات البيانات | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/few-shot-dataset-curation/SKILL.md) |
| 42 | `flashcards-quiz-exam-prep` — البطاقات والاختبارات والتحضير للامتحان | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/flashcards-quiz-exam-prep/SKILL.md) |
| 43 | `forecasting-probability` — التوقع والاحتمالات | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/forecasting-probability/SKILL.md) |
| 44 | `frontend-react-app` — تطبيق واجهة React | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/frontend-react-app/SKILL.md) |
| 45 | `fullstack-saas-starter` — منصة SaaS كاملة | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/fullstack-saas-starter/SKILL.md) |
| 46 | `game-dev-web` — تطوير الألعاب للويب | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/game-dev-web/SKILL.md) |
| 47 | `genius-council-decision` — مجلس العباقرة للقرارات | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/genius-council-decision/SKILL.md) |
| 48 | `git-github-workflow` — سير عمل Git وGitHub | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/git-github-workflow/SKILL.md) |
| 49 | `google-workspace-automation` — أتمتة Google Workspace | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/google-workspace-automation/SKILL.md) |
| 50 | `hyperframes-animation-studio` — استوديو الأنيميشن الاحترافي (HyperFrames + KOSIF Motion) | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/hyperframes-animation-studio/SKILL.md) |
| 51 | `ideation-100-ideas` — مولّد الأفكار: 100 فكرة | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/ideation-100-ideas/SKILL.md) |
| 52 | `image-critique-reverse-prompt` — نقد الصور واستخراج البرومبت | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/image-critique-reverse-prompt/SKILL.md) |
| 53 | `image-prompt-forge` — مصنع برومبتات الصور | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/image-prompt-forge/SKILL.md) |
| 54 | `invoices-quotes-contracts` — الفواتير والعروض والعقود | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/invoices-quotes-contracts/SKILL.md) |
| 55 | `kinetic-typography-arabic` — تايبوغرافي عربية متحركة | `motion-animation` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/kinetic-typography-arabic/SKILL.md) |
| 56 | `kosif-mimic` — KOSIF Mimic — محاكاة الفيديو | `kosif-special` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/kosif-mimic/SKILL.md) |
| 57 | `kosif-montage-motion` — KOSIF Montage & Motion | `kosif-special` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/kosif-montage-motion/SKILL.md) |
| 58 | `kosif-one` — KOSIF One — موزّع المهام | `kosif-special` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/kosif-one/SKILL.md) |
| 59 | `kosif-social` — KOSIF Social — السوشيال | `kosif-special` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/kosif-social/SKILL.md) |
| 60 | `landing-page-premium` — صفحة الهبوط الفاخرة | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/landing-page-premium/SKILL.md) |
| 61 | `language-coach-arabic-english` — مدرّب اللغات | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/language-coach-arabic-english/SKILL.md) |
| 62 | `legacy-code-migration` — تحديث الكود القديم والترحيل | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/legacy-code-migration/SKILL.md) |
| 63 | `llm-judge-eval-lab` — مختبر التقييم والقاضي الآلي | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/llm-judge-eval-lab/SKILL.md) |
| 64 | `llm-judge-evals` — قاضي النماذج ومجموعات التقييم | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/llm-judge-evals/SKILL.md) |
| 65 | `market-competitor-research` — بحث السوق والمنافسين | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/market-competitor-research/SKILL.md) |
| 66 | `math-science-tutor` — معلّم الرياضيات والعلوم | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/math-science-tutor/SKILL.md) |
| 67 | `mobile-app-builder` — تطبيقات الجوال | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/mobile-app-builder/SKILL.md) |
| 68 | `motion-director-pro` — مخرج الموشن المحترف (فيلم لا شرائح) | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/motion-director-pro/SKILL.md) |
| 69 | `music-song-brief` — الأغاني وموجز الموسيقى | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/music-song-brief/SKILL.md) |
| 70 | `newsletter-email-marketing` — النشرات والبريد التسويقي | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/newsletter-email-marketing/SKILL.md) |
| 71 | `notebooks-python-analysis` — دفاتر Python للتحليل | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/notebooks-python-analysis/SKILL.md) |
| 72 | `office-prompts-library` — مكتبة برومبتات أوفيس | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/office-prompts-library/SKILL.md) |
| 73 | `pdf-forms-reports` — ملفات PDF: النماذج والتقارير | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/pdf-forms-reports/SKILL.md) |
| 74 | `performance-optimization` — تحسين الأداء | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/performance-optimization/SKILL.md) |
| 75 | `photo-lighting-plan` — تخطيط الإضاءة للصور والفيديو | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/photo-lighting-plan/SKILL.md) |
| 76 | `pitch-deck-investor` — عرض المستثمرين | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/pitch-deck-investor/SKILL.md) |
| 77 | `pixel-art-game-assets` — بكسل آرت وأصول الألعاب | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/pixel-art-game-assets/SKILL.md) |
| 78 | `pixel-studio-painter` — استوديو الرسم بالبيكسل (KOSIF Studio) | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/pixel-studio-painter/SKILL.md) |
| 79 | `podcast-production` — إنتاج البودكاست | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/podcast-production/SKILL.md) |
| 80 | `powerpoint-decks` — عروض باوربوينت | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/powerpoint-decks/SKILL.md) |
| 81 | `pro-video-editor-ffmpeg` — المونتير المحترف بالكود (ffmpeg) | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/pro-video-editor-ffmpeg/SKILL.md) |
| 82 | `product-photo-mockups` — صور المنتجات والموك-أب | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/product-photo-mockups/SKILL.md) |
| 83 | `prompt-architect-reasoning-models` — مهندس البرومبت لنماذج التفكير | `advanced` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/prompt-architect-reasoning-models/SKILL.md) |
| 84 | `prompt-injection-defense` — الدفاع ضد حقن البرومبت | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/prompt-injection-defense/SKILL.md) |
| 85 | `prompt-master-pro` — سيّد البرومبتات الاحترافي | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/prompt-master-pro/SKILL.md) |
| 86 | `python-pro` — بايثون المحترف | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/python-pro/SKILL.md) |
| 87 | `rag-knowledge-base` — قاعدة المعرفة وRAG | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/rag-knowledge-base/SKILL.md) |
| 88 | `red-team-premortem` — الفريق الأحمر وتشريح ما قبل الفشل | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/red-team-premortem/SKILL.md) |
| 89 | `reels-shorts-factory` — مصنع الريلز والشورتس | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/reels-shorts-factory/SKILL.md) |
| 90 | `research-deep-citations` — البحث العميق بالمصادر | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/research-deep-citations/SKILL.md) |
| 91 | `security-audit-stride` — التدقيق الأمني STRIDE | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/security-audit-stride/SKILL.md) |
| 92 | `seo-content-architecture` — SEO وبنية المحتوى | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/seo-content-architecture/SKILL.md) |
| 93 | `software-architecture-adr` — هندسة البرمجيات والقرارات المعمارية | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/software-architecture-adr/SKILL.md) |
| 94 | `sql-data-analysis` — SQL وتحليل البيانات | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/sql-data-analysis/SKILL.md) |
| 95 | `storyboard-shotlist` — الستوري بورد وقائمة اللقطات | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/storyboard-shotlist/SKILL.md) |
| 96 | `storytelling-scripts` — القصص والسكربتات | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/storytelling-scripts/SKILL.md) |
| 97 | `strategy-decision-sensitivity` — الاستراتيجية وحساسية القرار | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/strategy-decision-sensitivity/SKILL.md) |
| 98 | `structured-output-json` — المخرجات المهيكلة JSON | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/structured-output-json/SKILL.md) |
| 99 | `svg-illustration-icons` — الرسوم المتجهة والأيقونات | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/svg-illustration-icons/SKILL.md) |
| 100 | `system-prompt-architect` — مهندس برومبتات النظام | `ai-prompts` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/system-prompt-architect/SKILL.md) |
| 101 | `technical-docs-readme` — التوثيق التقني وREADME | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/technical-docs-readme/SKILL.md) |
| 102 | `testing-suite-complete` — منظومة الاختبارات الكاملة | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/testing-suite-complete/SKILL.md) |
| 103 | `thumbnail-social-graphics` — الصور المصغّرة وتصاميم السوشيال | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/thumbnail-social-graphics/SKILL.md) |
| 104 | `translation-localization-ar` — الترجمة والتوطين العربي | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/translation-localization-ar/SKILL.md) |
| 105 | `trend-animation-styles` — أساليب الأنيميشن الترند | `motion-animation` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/trend-animation-styles/SKILL.md) |
| 106 | `typescript-node-pro` — TypeScript وNode المحترف | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/typescript-node-pro/SKILL.md) |
| 107 | `ui-motion-microinteractions` — موشن الواجهات والتفاعلات الدقيقة | `motion-animation` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/ui-motion-microinteractions/SKILL.md) |
| 108 | `video-editing-captions` — خطة المونتاج والترجمة | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/video-editing-captions/SKILL.md) |
| 109 | `video-prompt-director` — مخرج برومبتات الفيديو | `image-video-design` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/video-prompt-director/SKILL.md) |
| 110 | `voiceover-tts-direction` — التعليق الصوتي وإخراج TTS | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/voiceover-tts-direction/SKILL.md) |
| 111 | `web-scraping-automation` — جمع البيانات من الويب | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/web-scraping-automation/SKILL.md) |
| 112 | `website-design-system` — تصميم المواقع ونظام التصميم | `software-development` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/website-design-system/SKILL.md) |
| 113 | `word-documents-pro` — مستندات وورد الاحترافية | `office-data` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/word-documents-pro/SKILL.md) |
| 114 | `youtube-channel-strategy` — استراتيجية قناة يوتيوب | `business-learning` | [SKILL.md](https://github.com/kosif199022-jpg/100-superskills/blob/af7a5dc3778c0e68ef935349a5c1650d15688277/skills/youtube-channel-strategy/SKILL.md) |
