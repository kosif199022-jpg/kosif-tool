# فهرس المهارات والتكاملات والمكتبات

تاريخ مراجعة المصادر: 7 أكتوبر 2026. العدد: 33 بنداً متميزاً.

وجود ملف مهارة لا يعني وجود أداة تنفيذ. التفاصيل التقنية الكاملة والتراخيص والمتطلبات بالإنجليزية موجودة أيضاً في catalog.json وcatalog.csv.

## 1. مهارات Remotion وإضافة Claude Code

إنشاء فيديوهات React، التوقيت والتحريك، المعاينة والرندر، العناوين والكابتشن والخرائط المتحركة.

- الاسم الأصلي: Remotion Agent Skills / Claude Code plugin
- النوع: First-party Agent Skills and coding-agent plugin; not the old MCP
- مسار Claude: Explicitly documented by Remotion.
- المتطلبات: Claude Code or another supported coding agent; Node.js; a Remotion project and local or separately configured cloud rendering.
- الترخيص والتكلفة: Skills redistribution license not established in the inspected repository. Remotion runtime has its own source-available license: free for individuals and companies up to 3 people; paid company terms for 4+ people. AI usage and rendering infrastructure can cost extra.
- ملاحظة مهمة: Runs generated project code and package tooling. Old Remotion documentation MCP is deprecated; do not treat it as the preferred installation.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://www.remotion.dev/docs/ai/plugins)
- المصادر:
  - [source](https://www.remotion.dev/docs/ai/skills)
  - [repository](https://github.com/remotion-dev/skills)
  - [setup](https://www.remotion.dev/docs/ai/plugins)
  - [license](https://www.remotion.dev/docs/license/pricing)
  - [caution_source](https://www.remotion.dev/docs/ai/mcp)

## 2. مهارات HyperFrames لتحويل HTML إلى فيديو

موشن جرافيك وفيديوهات منتجات وشروحات من HTML/CSS مع تحريك قابل للرندر إطاراً بإطار؛ يدعم محركات مثل GSAP وThree.js وLottie.

- الاسم الأصلي: HyperFrames skills / Claude Code plugin
- النوع: First-party skill collection and Claude Code plugin, backed by a rendering framework
- مسار Claude: Explicit versioned plugin and standalone skills workflow.
- المتطلبات: Local JavaScript runtime/package tooling, HyperFrames CLI and browser/FFmpeg rendering dependencies. Optional hosted/media integrations are separate.
- الترخيص والتكلفة: Apache-2.0. Local rendering has no HeyGen credit cost or per-render fee. Agent usage, hosting, voices, avatars and generated assets may cost extra.
- ملاحظة مهمة: Skills can invoke package tooling and optional external services. Review and pin versions; do not run copied installation commands merely because they appear in the archive.
- داخل الأرشيف: ملفات نصية فعلية
- حدود النسخة: Only five selected main SKILL.md files plus LICENSE. All supporting references, code, assets, configuration and runtime omitted; reference-only, incomplete.
- مجلد الملفات: [text-snapshots/hyperframes-selected](../text-snapshots/hyperframes-selected/)
- [تعليمات الإعداد أو المصدر الرسمي](https://hyperframes.heygen.com/quickstart)
- المصادر:
  - [source](https://github.com/heygen-com/hyperframes)
  - [setup](https://hyperframes.heygen.com/quickstart)
  - [license](https://github.com/heygen-com/hyperframes/blob/main/LICENSE)

## 3. Motion Director لإخراج فيديوهات الموشن

سير عمل يبدأ بالموجز والهوية البصرية وقائمة اللقطات، ثم التزامن مع الصوت ومراجعة الفريمات وإخراج مقاسات متعددة.

- الاسم الأصلي: Motion Director (claude-motion-director)
- النوع: Community Claude Code skill built on HyperFrames
- مسار Claude: Explicitly designed for Claude Code.
- المتطلبات: Node.js 22+, FFmpeg, Python 3 with numpy/scipy; pinned HyperFrames version per project.
- الترخيص والتكلفة: MIT for the skill repository. HyperFrames, GSAP, fonts, music and other dependencies retain their own licenses. Claude usage is separate.
- ملاحظة مهمة: Small community project; documentation claims were not runtime tested. Included shell/Python helpers execute code and may install dependencies when activated.
- داخل الأرشيف: ملفات نصية فعلية
- حدود النسخة: SKILL.md, five references, critique prompt, README and LICENSE. Scripts, templates, examples and runtime omitted; reference-only, incomplete.
- مجلد الملفات: [text-snapshots/claude-motion-director](../text-snapshots/claude-motion-director/)
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/abdullatif06/claude-motion-director#requirements)
- المصادر:
  - [source](https://github.com/abdullatif06/claude-motion-director)
  - [setup](https://github.com/abdullatif06/claude-motion-director#requirements)
  - [license](https://github.com/abdullatif06/claude-motion-director/blob/main/LICENSE)

## 4. ربط Claude ببرنامج Blender

إنشاء وتعديل المجسمات والمشاهد والخامات، تنفيذ Blender Python، فحص بصري ورندر، وتكاملات اختيارية للأصول وتوليد 3D.

- الاسم الأصلي: MCP for Blender (formerly BlenderMCP / blender-mcp)
- النوع: Community local MCP server plus Blender add-on
- مسار Claude: Explicit setup documented.
- المتطلبات: Blender 3.0+, Python 3.10+, uv or documented alternative, Blender add-on; Blender must be running.
- الترخيص والتكلفة: MIT for the integration; free core. Optional premium model generation and third-party APIs/assets have separate costs and terms.
- ملاحظة مهمة: The socket has no authentication/encryption and can execute Python. Keep localhost-only; opt-in safe mode is available but not a guarantee. Save backups before agent edits.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/ahujasid/mcp-for-blender#quickstart)
- المصادر:
  - [source](https://github.com/ahujasid/mcp-for-blender)
  - [setup](https://github.com/ahujasid/mcp-for-blender#quickstart)
  - [license](https://github.com/ahujasid/mcp-for-blender/blob/main/LICENSE)

## 5. إضافة Spline الرسمية لمشاهد 3D وتصميم Hana

إنشاء وتعديل مشاهد ثلاثية الأبعاد وخامات وكاميرات؛ تصميم واجهات Hana وتوليد أصول عبر ميزات Spline AI.

- الاسم الأصلي: Spline MCP Server
- النوع: Official MCP bundled in the Spline desktop app
- مسار Claude: Explicit automatic registration supported.
- المتطلبات: Spline desktop app on macOS or Windows, running locally. Browser-only Spline does not expose this MCP.
- الترخيص والتكلفة: Proprietary service; account/feature/AI-credit costs depend on plan. No open-source redistribution grant verified for the bundled server.
- ملاحظة مهمة: Edits affect the live document. App can register MCP configurations automatically; inspect enabled clients. Local transport is localhost/origin-allowlisted, but Spline AI generation is cloud-based and the chosen AI client has its own data handling.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://spline.design/download)
- المصادر:
  - [source](https://docs.spline.design/generate/spline-mcp-server)
  - [setup](https://spline.design/download)
  - [Editable scenes, exports and publishing](https://docs.spline.design/basics/what-is-spline)
  - [Plan prices and export limits](https://spline.design/pricing)

## 6. تكامل Rive الرسمي للأنيميشن التفاعلي

أشكال وتصميمات، keyframes وأنيميشن خطي، state machines وانتقالات، ربط بيانات، سكربتات Luau وشيدر WGSL.

- الاسم الأصلي: Rive MCP Integration
- النوع: Official local MCP in the Rive desktop Editor
- مسار Claude: Official docs explicitly show Claude terminal setup using local HTTP MCP.
- المتطلبات: Current Rive desktop app for macOS/Windows kept open. Official page also refers to the Early Access app, so confirm current feature availability before setup.
- الترخيص والتكلفة: Proprietary editor/service. Exact MCP entitlement or separate charge not established from the integration guide.
- ملاحظة مهمة: Can modify/delete live file elements and run scripts/shaders. Use copies/version history and retain tool approval controls.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://rive.app/docs/editor/ai/mcp)
- المصادر:
  - [source](https://rive.app/docs/editor/ai/mcp)

## 7. ربط Meshy لتوليد وتحريك أصول 3D

تحويل نصوص وصور إلى 3D، خامات وإعادة تشكيل، rigging وتحريك، تنزيل وتحويل النماذج وإدارة المهام.

- الاسم الأصلي: Meshy MCP Server
- النوع: Official MCP server wrapping a hosted API
- مسار Claude: Explicit configuration documented.
- المتطلبات: Node.js 18+ and Meshy API key; README says API-key access requires Pro or above. Local MCP process calls Meshy cloud.
- الترخيص والتكلفة: MIT for server source. Paid API/credit usage and Meshy content/service terms remain separate.
- ملاحظة مهمة: Protect API keys; generation consumes credits and inputs go to Meshy. Review download locations and avoid broad automatic client configuration.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/meshy-dev/meshy-mcp-server#prerequisites)
- المصادر:
  - [source](https://github.com/meshy-dev/meshy-mcp-server)
  - [setup](https://github.com/meshy-dev/meshy-mcp-server#prerequisites)
  - [license](https://github.com/meshy-dev/meshy-mcp-server/blob/main/LICENSE)

## 8. تكامل Tripo الرسمي لتوليد أصول Blender

توليد أصل ثلاثي الأبعاد من وصف نصي عبر Tripo وإدخاله إلى Blender.

- الاسم الأصلي: Tripo MCP Server
- النوع: Official alpha MCP plus Tripo Blender add-on
- مسار Claude: MCP-compatible in principle, but no specific Claude Code setup verified in this alpha README.
- المتطلبات: Python 3.10+, Blender, Tripo AI Blender Addon and an eligible Tripo account/API setup.
- الترخيص والتكلفة: MIT integration. Tripo generation costs/credits and service terms are separate; exact current amount not verified.
- ملاحظة مهمة: Explicit alpha status and narrower verified capabilities than the full Tripo API. Sends generation requests to Tripo; modifies the Blender scene.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/VAST-AI-Research/tripo-mcp#quick-start)
- المصادر:
  - [source](https://github.com/VAST-AI-Research/tripo-mcp)
  - [setup](https://github.com/VAST-AI-Research/tripo-mcp#quick-start)
  - [license](https://github.com/VAST-AI-Research/tripo-mcp/blob/main/LICENSE)

## 9. إضافة Lottie Creator لصناعة الأنيميشن وتعديله

إنشاء أنيميشن بطبقات وأشكال ونصوص، keyframes وeasing، masks وتأثيرات، متغيرات لونية وحركية وتفاعلات.

- الاسم الأصلي: Lottie Creator MCP
- النوع: Official local MCP bridge to the browser-based Creator editor
- مسار Claude: Explicit setup documented.
- المتطلبات: Node.js 18+; LottieFiles Creator account/workspace; keep the Creator browser tab open and enable local MCP in Creator settings.
- الترخيص والتكلفة: Feature access follows the Creator workspace/plan. Bridge redistribution license was not separately verified, so link-only.
- ملاحظة مهمة: Can change live animation files; preserve a copy and review edits. Local bridge does not make the online Creator workspace an offline service.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://docs.lottiefiles.com/en/creator/13_ai-tools/lottie-creator-mcp)
- المصادر:
  - [source](https://docs.lottiefiles.com/en/creator/13_ai-tools/lottie-creator-mcp)
  - [Creator versus hosted account MCP distinction](https://docs.lottiefiles.com/en/platform)
  - [WebMCP compatibility caveat](https://docs.lottiefiles.com/en/creator/13_ai-tools/lottie-creator-webmcp)
  - [Free access and paid annual prices](https://lottiefiles.com/pricing)
  - [Official skill source](https://github.com/LottieFiles/motion-design-skill)
  - [MIT redistribution notice](https://github.com/LottieFiles/motion-design-skill/blob/main/LICENSE)

## 10. مهارة LottieFiles لمبادئ الحركة

اختيار التوقيت والـeasing وتسلسل الحركة والشخصية البصرية؛ مفيدة مع CSS وGSAP وLottie وغيرها.

- الاسم الأصلي: Motion Design Skill
- النوع: Official, implementation-agnostic Agent Skill; no MCP tools added
- مسار Claude: Explicitly supported in the skill README.
- المتطلبات: Skill-capable agent. It supplies guidance only; a target animation runtime/editor is still needed.
- الترخيص والتكلفة: MIT. No separate skill fee; chosen AI/runtime/service costs remain separate.
- ملاحظة مهمة: Review third-party skill instructions before enabling. This skill alone cannot render or control Lottie Creator.
- داخل الأرشيف: ملفات نصية فعلية
- حدود النسخة: Complete Markdown skill reference tree at the pinned commit, plus README and LICENSE. No editor or renderer installed.
- مجلد الملفات: [text-snapshots/lottiefiles-motion-design](../text-snapshots/lottiefiles-motion-design/)
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/LottieFiles/motion-design-skill#install)
- المصادر:
  - [source](https://github.com/LottieFiles/motion-design-skill)
  - [setup](https://github.com/LottieFiles/motion-design-skill#install)
  - [license](https://github.com/LottieFiles/motion-design-skill/blob/main/LICENSE)

## 11. تكامل إدارة مكتبة ومساحة عمل LottieFiles

استكشاف المشاريع والأنيميشن وتنفيذ عمليات API على مساحة العمل. ليس هو محرر الحركة المحلي السابق.

- الاسم الأصلي: LottieFiles MCP (Platform)
- النوع: Official remote MCP GraphQL workbench; distinct from Creator MCP
- مسار Claude: Explicit remote HTTP/OAuth setup documented.
- المتطلبات: LottieFiles account; remote MCP client with Streamable HTTP and OAuth, or Node.js 18+ for an optional bridge.
- الترخيص والتكلفة: Hosted service; account permissions and plan limits apply. No separate MCP charge verified.
- ملاحظة مهمة: graphql_execute can run write/delete/billing/admin mutations under account permissions. Review proposed mutations, scopes and revocation controls.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://docs.lottiefiles.com/en/platform/mcp/connect)
- المصادر:
  - [source](https://docs.lottiefiles.com/en/platform/mcp/connect)
  - [caution_source](https://docs.lottiefiles.com/en/platform/mcp/tools)

## 12. تكامل Figma الرسمي للتصميم والواجهات

قراءة سياق التصميم والمكونات والمتغيرات، تحويل التصميم إلى كود، وكتابة وتعديل عناصر Figma أصلية بالميزات الحالية.

- الاسم الأصلي: Figma MCP server / Figma Claude Code plugin
- النوع: Official remote/desktop MCP with first-party Claude Code plugin and workflow skills
- مسار Claude: Explicit official plugin: figma@claude-plugins-official.
- المتطلبات: Figma account and OAuth for recommended remote server; desktop alternative requires the Figma desktop app and an eligible paid Dev/Full seat.
- الترخيص والتكلفة: Remote access currently offered on all seats/plans with rate limits; native writing described as free beta that may become usage-priced. Service terms apply; no broad documentation redistribution grant assumed.
- ملاحظة مهمة: Design content is shared with the connected AI client and writes affect files. Review account scopes and preserve file versions.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)
- المصادر:
  - [source](https://help.figma.com/hc/en-us/articles/39888612464151-Claude-Code-and-Figma-Set-up-the-MCP-server)
  - [setup](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)
  - [cost_source](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
  - [Official skills and editable code-to-canvas workflows](https://help.figma.com/hc/en-us/articles/40219873508247-Workflow-lab-Code-to-canvas)

## 13. تكامل Canva للتصميمات القابلة للتعديل

إنشاء وتعديل تصميمات Canva قابلة للتحرير، عروض ومحتوى تسويقي ورسومات، العمل بالقوالب وBrand Kits.

- الاسم الأصلي: Canva MCP
- النوع: Official hosted design MCP; distinct from Canva Dev MCP
- مسار Claude: MCP-compatible coding agents supported; use hosted design MCP, not the separate developer-documentation MCP by mistake.
- المتطلبات: Canva account, compatible MCP client and OAuth authorization; remote service, no local graphics engine required.
- الترخيص والتكلفة: Proprietary service and content licenses; feature/asset access depends on plan. No separate MCP fee verified in the inspected overview.
- ملاحظة مهمة: Account designs and uploads may be read or changed; verify sharing/export/publishing actions before committing. Premium assets retain their own licensing.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://www.canva.dev/agents/)
- المصادر:
  - [source](https://www.canva.dev/solutions/mcp/)
  - [setup](https://www.canva.dev/agents/)

## 14. إضافة Manim للشروحات والرسوم الرياضية

تنفيذ سكربتات Manim وإرجاع فيديوهات، مناسب للشروحات والرسوم البيانية والهندسة المتحركة.

- الاسم الأصلي: Manim MCP Server (abhiemj/manim-mcp-server)
- النوع: Community local MCP wrapper around Manim Community Edition
- مسار Claude: Standard local MCP is plausible, but no project-specific Claude Code instructions verified.
- المتطلبات: Local Python, Manim Community Edition, MCP package and Manim's native rendering dependencies. Repository says Python 3.8+; use a Python version supported by the chosen current Manim release.
- الترخيص والتكلفة: MIT server wrapper; local compute and AI usage separate. No hosted renderer included.
- ملاحظة مهمة: Executes supplied Python scripts. Treat it as code execution, not a safe media viewer; isolate work and review scripts/cleanup operations.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/abhiemj/manim-mcp-server#integration-with-claude)
- المصادر:
  - [source](https://github.com/abhiemj/manim-mcp-server)
  - [setup](https://github.com/abhiemj/manim-mcp-server#integration-with-claude)
  - [license](https://github.com/abhiemj/manim-mcp-server/blob/main/LICENSE.txt)

## 15. مهارة Anthropic لتصميم واجهات ذات هوية واضحة

اختيار اتجاه بصري وتايبوغرافي وألوان وتخطيط وحركة مدروسة لواجهات الويب.

- الاسم الأصلي: frontend-design
- النوع: Official Anthropic example Agent Skill
- مسار Claude: Supported through Anthropic's skills marketplace/example-skills plugin or custom skill workflows.
- المتطلبات: Skills enabled; target coding/rendering tools are still needed to build and inspect an interface.
- الترخيص والتكلفة: Apache-2.0 in the skill's LICENSE.txt. No separate skill fee; Claude/account usage limits apply.
- ملاحظة مهمة: Guidance does not guarantee visual quality or accessibility. Review generated code and external dependencies.
- داخل الأرشيف: ملفات نصية فعلية
- حدود النسخة: SKILL.md and exact LICENSE.txt; other repository material is not included.
- مجلد الملفات: [text-snapshots/anthropic-skills/skills/frontend-design](../text-snapshots/anthropic-skills/skills/frontend-design/)
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/anthropics/skills#try-in-claude-code-claudeai-and-the-api)
- المصادر:
  - [source](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
  - [setup](https://github.com/anthropics/skills#try-in-claude-code-claudeai-and-the-api)
  - [license](https://github.com/anthropics/skills/blob/main/skills/frontend-design/LICENSE.txt)

## 16. مهارة Anthropic للبوسترات والرسوم الثابتة

تصميم بوسترات ولوحات ورسوم ثابتة وإخراج PNG أو PDF وفق فكرة بصرية متماسكة.

- الاسم الأصلي: canvas-design
- النوع: Official Anthropic example Agent Skill
- مسار Claude: Supported via Anthropic example skills.
- المتطلبات: Skill-capable Claude surface and suitable image/PDF generation tools. Bundled fonts have their own licenses.
- الترخيص والتكلفة: Apache-2.0 for skill text. Preserve applicable third-party font notices if including fonts; otherwise omit font binaries and mark the extract incomplete.
- ملاحظة مهمة: Static design skill, not video/3D generation. Check fonts/assets and originality rights.
- داخل الأرشيف: ملفات نصية فعلية
- حدود النسخة: SKILL.md and exact LICENSE.txt only. Fonts and other assets omitted; not a complete executable package.
- مجلد الملفات: [text-snapshots/anthropic-skills/skills/canvas-design](../text-snapshots/anthropic-skills/skills/canvas-design/)
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/anthropics/skills#try-in-claude-code-claudeai-and-the-api)
- المصادر:
  - [source](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md)
  - [setup](https://github.com/anthropics/skills#try-in-claude-code-claudeai-and-the-api)
  - [license](https://github.com/anthropics/skills/blob/main/skills/canvas-design/LICENSE.txt)

## 17. مهارة Anthropic للفن التوليدي والجزيئات

فن توليدي بـp5.js، جزيئات وحقول حركة وعشوائية ببذرة ثابتة مع واجهة تفاعلية لضبط المعاملات.

- الاسم الأصلي: algorithmic-art
- النوع: Official Anthropic example Agent Skill
- مسار Claude: Supported via Anthropic example skills.
- المتطلبات: Skill-capable Claude environment; browser for HTML output; templates use p5.js and may load CDN resources.
- الترخيص والتكلفة: Apache-2.0 for skill files; p5.js and other dependencies have separate licenses.
- ملاحظة مهمة: HTML executes JavaScript and may load network resources. Templates constrain viewer UI; this is not an image diffusion model.
- داخل الأرشيف: ملفات نصية فعلية
- حدود النسخة: SKILL.md and exact LICENSE.txt only. Executable HTML/JavaScript templates omitted; not a complete package.
- مجلد الملفات: [text-snapshots/anthropic-skills/skills/algorithmic-art](../text-snapshots/anthropic-skills/skills/algorithmic-art/)
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/anthropics/skills#try-in-claude-code-claudeai-and-the-api)
- المصادر:
  - [source](https://github.com/anthropics/skills/blob/main/skills/algorithmic-art/SKILL.md)
  - [setup](https://github.com/anthropics/skills#try-in-claude-code-claudeai-and-the-api)
  - [license](https://github.com/anthropics/skills/blob/main/skills/algorithmic-art/LICENSE.txt)

## 18. مهارة Anthropic لصناعة GIF خفيف

تجميع فريمات GIF وتحسين الحجم والألوان والتحقق من المقاسات؛ مناسب للأيقونات المتحركة والملصقات القصيرة.

- الاسم الأصلي: slack-gif-creator
- النوع: Official Anthropic example Agent Skill with Python utilities
- مسار Claude: Supported via Anthropic example skills.
- المتطلبات: Python/Pillow and the skill's helper modules when used in a local coding environment.
- الترخيص والتكلفة: Apache-2.0 for skill/helper source. Claude usage and supplied image rights remain separate.
- ملاحظة مهمة: Helpers execute Python. Generating a GIF does not authorize uploading or posting it to Slack.
- داخل الأرشيف: ملفات نصية فعلية
- حدود النسخة: SKILL.md and exact LICENSE.txt only. Python helpers omitted; not a complete package.
- مجلد الملفات: [text-snapshots/anthropic-skills/skills/slack-gif-creator](../text-snapshots/anthropic-skills/skills/slack-gif-creator/)
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/anthropics/skills#try-in-claude-code-claudeai-and-the-api)
- المصادر:
  - [source](https://github.com/anthropics/skills/blob/main/skills/slack-gif-creator/SKILL.md)
  - [setup](https://github.com/anthropics/skills#try-in-claude-code-claudeai-and-the-api)
  - [license](https://github.com/anthropics/skills/blob/main/skills/slack-gif-creator/LICENSE.txt)

## 19. Three.js

مشاهد ويب ثلاثية الأبعاد وتفاعلات وكاميرات ومؤثرات؛ مكتبة برمجية وليست إضافة Claude بحد ذاتها.

- الاسم الأصلي: Three.js
- النوع: Open-source JavaScript 3D library
- مسار Claude: Code generation using the official docs and examples. No first-party Claude MCP or skill was verified in this pass.
- المتطلبات: A JavaScript project or suitable browser module setup; compatible graphics browser/GPU; scene assets where needed.
- الترخيص والتكلفة: Library: MIT, no license fee. Hosting, assets and Claude use are separate.
- ملاحظة مهمة: A scene in a browser is not automatically an MP4 or a portable model; exports and capture need a separate workflow.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/mrdoob/three.js)
- المصادر:
  - [Purpose, renderers, usage and MIT license](https://github.com/mrdoob/three.js)
  - [Official product and examples entry point](https://threejs.org/)

## 20. React Three Fiber وDrei

بناء مشاهد 3D داخل React مع مساعدات للكاميرات والإضاءة والنصوص وتحميل النماذج.

- الاسم الأصلي: React Three Fiber + Drei
- النوع: Open-source React renderer and helper collection
- مسار Claude: Code generation. Fiber maps React components to Three.js; Drei supplies reusable helpers. No first-party Claude MCP was verified.
- المتطلبات: React and Three.js knowledge/runtime; compatible package versions. Official docs pair Fiber 8 with React 18 and Fiber 9 with React 19.
- الترخيص والتكلفة: Fiber and Drei: MIT, no license fees. Assets and deployment are separate.
- ملاحظة مهمة: These are complementary libraries, not two turnkey generative services. Check renderer compatibility for individual shader helpers.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/pmndrs/react-three-fiber)
- المصادر:
  - [React renderer, version pairing and MIT](https://github.com/pmndrs/react-three-fiber)
  - [Helper scope and MIT](https://github.com/pmndrs/drei)
  - [Practical visual use cases](https://r3f.docs.pmnd.rs/getting-started/examples)

## 21. GSAP

تايملاين دقيق وحركة عند التمرير وتحريك نصوص ومسارات SVG وعناصر الويب.

- الاسم الأصلي: GSAP
- النوع: JavaScript animation library
- مسار Claude: Claude can generate GSAP code. The official license explicitly permits AI-generated GSAP code; no first-party Claude connector was verified.
- المتطلبات: A browser/web project and the relevant GSAP plugins; separate render/capture setup for video.
- الترخيص والتكلفة: No-charge standard GSAP license, including commercial use and formerly paid plugins. This is not MIT: competing no-code visual animation builders are restricted without permission.
- ملاحظة مهمة: Do not describe the license as unrestricted open source or quote old Club GSAP pricing.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://gsap.com/pricing/)
- المصادر:
  - [Entire library currently free](https://gsap.com/pricing/)
  - [Commercial use, AI code and prohibited-use restriction](https://gsap.com/community/standard-license/)

## 22. Motion ومجموعة Motion AI Kit الرسمية

أنيميشن الواجهات والنوابض والإيماءات وتغييرات التخطيط، مع مهارة وMCP رسميين لـClaude Code.

- الاسم الأصلي: Motion + official Motion AI Kit
- النوع: Animation library with official skill and hosted MCP
- مسار Claude: Official /motion skill plus MCP for Claude Code. Current install guide uses motion-ai; free MCP searches docs and example metadata. The connection and any Motion+ sign-in are separate setup.
- المتطلبات: Supported coding agent, web project and chosen Motion runtime. Advanced tools require Motion+ access; runtime profiling requires a running site.
- الترخيص والتكلفة: Motion core is MIT. Official docs call the installer and skill free/MIT. Documentation and best practices are free; Motion+ gates premium source, spring generation, audits and transition editor. Paid price was not reliably extracted.
- ملاحظة مهمة: The current flow uses hosted MCP sign-in; older local TOKEN/API-key instructions are retired. The AI Kit repository had no root LICENSE visible, so do not bundle it without resolving the distributable notice.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://motion.dev/docs/ai-kit)
- المصادر:
  - [Official skill/MCP and free versus paid features](https://motion.dev/docs/ai-kit)
  - [Claude setup, MIT statement and current hosted authentication](https://motion.dev/docs/ai-kit-install)
  - [Core library and MIT](https://github.com/motiondivision/motion)
  - [Official AI Kit repository](https://github.com/motiondivision/ai-kit)
  - [Paid plan reference](https://motion.dev/plus)

## 23. Hana من Spline

لوحة تصميم متجه قابلة للتحرير تجمع الحركة والمؤثرات وتستخدم MCP الخاص بتطبيق Spline المكتبي.

- الاسم الأصلي: Hana by Spline
- النوع: Editable 2D design and motion canvas
- مسار Claude: Same official Spline desktop MCP as Spline 3D, routed to Hana tabs; can create and edit native design objects.
- المتطلبات: Spline desktop on macOS or Windows for MCP; supported Claude client; account and plan. Web editor alone is not the MCP route.
- الترخيص والتكلفة: Proprietary; shares Spline plans, credits and limits. Free entry tier exists; paid exports and capabilities must be checked in the current plan.
- ملاحظة مهمة: HTML/CSS round-tripping uses Hana's supported subset. A design frame does not guarantee production application logic or an encoded video.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://spline.design/hana)
- المصادر:
  - [Vector, motion and agent-driven canvas features](https://spline.design/hana)
  - [Hana editing, HTML/CSS subset and Claude requirements](https://docs.spline.design/generate/spline-mcp-server)
  - [Shared commercial plans](https://spline.design/pricing)

## 24. Rive CLI وRML

تأليف رسوم متجهة تفاعلية وملفات Rive قابلة للتحرير عبر Claude Code وواجهة أوامر؛ مسار منفصل عن Rive MCP.

- الاسم الأصلي: Rive + official CLI/RML
- النوع: Interactive graphics editor, runtime format and agent-friendly CLI
- مسار Claude: Official CLI explicitly supports Claude Code. Claude writes Rive Markup Language, scripts and shaders; CLI scaffolds AGENTS.md and CLAUDE.md, compiles, previews and inspects output. This entry covers the CLI route. The separately cataloged official Rive MCP is another integration path.
- المتطلبات: Rive CLI on Apple Silicon macOS, Linux x86_64 or Windows; coding agent and local project. Account needed when publishing, with runtime integration in the destination app.
- الترخيص والتكلفة: Runtimes are MIT; editor/CLI service terms are separate. CLI announced as unlimited free technical preview; free-plan CLI publishing adds a Rive splash, paid removes it. Editor pricing still says free creation, Cadet $9/seat/month annually or $17 monthly for exports.
- ملاحظة مهمة: Pricing/export policy is in transition: the Sept 11 CLI announcement says editor free exports with a splash are coming. Treat CLI preview and editor export rules separately and recheck before production.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://rive.app/docs/cli/overview)
- المصادر:
  - [RML, preview, .riv/.rev, inspection and account sync](https://rive.app/docs/cli/overview)
  - [Official Claude Code workflow and agent instructions](https://rive.app/docs/cli/agents)
  - [Supported systems](https://rive.app/docs/cli/getting-started)
  - [Technical preview and splash pricing nuance](https://community.rive.app/c/announcements/introducing-the-rive-cli-and-rml)
  - [Editor monthly and annual prices](https://rive.app/docs/account-admin/pricing)
  - [MIT runtimes and no runtime fee](https://rive.app/blog/rive-s-new-9-mo-plan)

## 25. Theatre.js

محرر تايملاين بصري متصل بالكود، مناسب لحركة الكاميرات والخصائص في مشاهد الويب.

- الاسم الأصلي: Theatre.js
- النوع: Code-integrated visual timeline editor
- مسار Claude: Code generation for Theatre integration and animated properties; the visual studio handles timeline refinement. No first-party Claude connector verified.
- المتطلبات: JavaScript app plus the appropriate renderer, such as Three.js; development-time studio.
- الترخيص والتكلفة: Core and most packages: Apache-2.0. Studio: AGPL-3.0. Official guidance says keep studio in development and ship core in production.
- ملاحظة مهمة: Do not label the whole stack Apache-only. The public repository states 1.0 development temporarily moved private, so verify current package/API maturity before adoption. Video output needs a separate render/capture workflow.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/theatre-js/theatre)
- المصادر:
  - [Use cases, split license and development status](https://github.com/theatre-js/theatre)

## 26. Babylon.js

محرك ويب ثلاثي الأبعاد للألعاب والتجارب والمحاكاة، مع أدوات متكاملة.

- الاسم الأصلي: Babylon.js
- النوع: Open-source web 3D engine
- مسار Claude: Code generation using official docs and Playground. No first-party Claude skill/MCP verified in this pass.
- المتطلبات: JavaScript/TypeScript project or Playground, browser/GPU support and assets.
- الترخيص والتكلفة: Apache-2.0 engine, no library license fee. Models, hosting, rendering infrastructure and agent costs remain separate.
- ملاحظة مهمة: Official repository says its public CDN is for learning/experiments, not production delivery. A browser engine does not automatically create a video file or source model.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/BabylonJS/Babylon.js)
- المصادر:
  - [License, Playground, npm and production CDN warning](https://github.com/BabylonJS/Babylon.js)
  - [Engine capabilities and examples](https://www.babylonjs.com/)

## 27. Manim Community

رندر فيديوهات تعليمية ورياضية وهندسية دقيقة من مشاهد Python؛ الإضافة MCP منفصلة.

- الاسم الأصلي: Manim Community
- النوع: Open-source Python animation engine
- مسار Claude: Claude writes Python scenes; a separate installed Manim environment renders and previews them. No first-party Claude plugin verified.
- المتطلبات: Python/Manim environment and platform dependencies. LaTeX is optional but needed for LaTeX-rendered equations.
- الترخيص والتكلفة: MIT software, no library license fee. Rendering compute and external fonts/assets can cost separately.
- ملاحظة مهمة: Manim Community and Grant Sanderson's separate manim repository have different instructions; do not mix their setup or APIs. Source generation alone is not a rendered deliverable.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/ManimCommunity/manim)
- المصادر:
  - [Purpose, usage, MIT and edition warning](https://github.com/ManimCommunity/manim)
  - [Dependency handling and optional LaTeX](https://docs.manim.community/en/stable/installation/conda.html)
  - [Current official documentation](https://docs.manim.community/en/stable/)

## 28. Three.js TSL وWebGPURenderer

مواد ومؤثرات وشيدر متقدم يكتب بصيغة JavaScript ويعمل ضمن Three.js؛ يحتاج تحققاً من توافق الأجهزة.

- الاسم الأصلي: Three.js TSL + WebGPURenderer
- النوع: Advanced shader/rendering workflow within Three.js
- مسار Claude: Code generation guided by current Three.js docs; TSL is the Three.js Shading Language, not a Claude plugin or standalone app.
- المتطلبات: Current compatible Three.js version, appropriate renderer setup and supported browser/GPU. Test target devices.
- الترخيص والتكلفة: Covered by Three.js MIT license; no separate TSL service fee.
- ملاحظة مهمة: TSL translates to WGSL or GLSL for the renderer backend. Official manual still calls WebGPURenderer experimental and notes missing features/performance differences; not every existing WebGL shader/add-on transfers unchanged.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/mrdoob/three.js/blob/dev/manual/pages/webgpurenderer.html)
- المصادر:
  - [TSL, backends, renderer integration and experimental caveat](https://github.com/mrdoob/three.js/blob/dev/manual/pages/webgpurenderer.html)
  - [MIT and official project](https://github.com/mrdoob/three.js)

## 29. Penpot MCP

تصميم واجهات وعناصر متجهة ومكونات قابلة للتحرير عبر التكامل الرسمي، مع خيارات استضافة ذاتية.

- الاسم الأصلي: Penpot official MCP
- النوع: Open design platform with editable-canvas MCP
- مسار Claude: Official MCP supports Claude and other MCP clients, with hosted or self-hosted/local setup.
- المتطلبات: Penpot account or instance, authorized design file, MCP-capable client and configured connection.
- الترخيص والتكلفة: Official MCP is free/open with no extra agent-token paywall; agent fees are separate. Cloud Professional is $0 with storage/team limits; Unlimited $7/editor/month capped at $175/month; Enterprise $25/member/month. Self-hosting adds infrastructure costs.
- ملاحظة مهمة: No paid-plan requirement should be invented for basic MCP. Do not confuse editable design/prototyping with a final video renderer or full application runtime.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://penpot.app/penpot-mcp-server)
- المصادر:
  - [Official Claude-capable MCP and hosting options](https://penpot.app/penpot-mcp-server)
  - [Free/open MCP and agent costs](https://penpot.app/ai/ai-workflows)
  - [Current USD pricing and limits](https://penpot.app/pricing)

## 30. Paper Desktop MCP

قراءة وتعديل لوحة تصميم مبنية على HTML وCSS من Claude، ضمن حدود الخطة والصلاحيات.

- الاسم الأصلي: Paper Desktop + official MCP
- النوع: HTML/CSS-based editable design canvas
- مسار Claude: Official Paper Desktop MCP reads and writes files; documented Claude extension and Claude Code plugin routes.
- المتطلبات: Paper Desktop and an open design file; supported Claude client and approved connection. The Paper CLI mediates agent communication.
- الترخيص والتكلفة: Proprietary service. Free: 100 MCP tool calls/week. Pro: $20/editor/month monthly or $16 annually, with 1M MCP calls/week and video export. Viewer seats free.
- ملاحظة مهمة: A free MCP allowance is not unlimited. The design-to-code workflow still needs a project runtime and deployment. Read/write permission should be scoped to intended files.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://paper.design/docs/mcp)
- المصادر:
  - [Official Claude setup, read/write capabilities and desktop requirement](https://paper.design/docs/mcp)
  - [Free and paid calls, prices and video export](https://paper.design/pricing)

## 31. Paper Shaders

مكتبة مؤثرات وخلفيات شيدر متحركة للويب، مستقلة عن اشتراك تطبيق Paper.

- الاسم الأصلي: Paper Shaders
- النوع: Open-source ready-made canvas shader library
- مسار Claude: Code generation using vanilla JavaScript or React package APIs; can also design settings in Paper. The library itself is not an MCP.
- المتطلبات: Browser canvas/WebGL-compatible environment; React only for its React wrapper.
- الترخيص والتكلفة: Apache-2.0; official license section permits commercial websites, apps, games, videos and other end products. This library is separate from Paper's paid app plan.
- ملاحظة مهمة: Pin package versions: repository warns of breaking changes under 0.0.x versioning. Library use does not itself provide an encoded video exporter.
- داخل الأرشيف: ملخص وروابط فقط
- حدود النسخة: Original catalog summary and source/setup links only; no upstream code, service, plugin, server, runtime or installer included.
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/paper-design/shaders)
- المصادر:
  - [Packages, effects, license and version-pinning warning](https://github.com/paper-design/shaders)
  - [Interactive examples and documentation](https://shaders.paper.design/)

## 32. PixiJS والمهارات الرسمية

جرافيك 2D مكثف وجزيئات وسبرایت وفلاتر وألعاب ويب؛ تتضمن اللقطة 26 ملف مهارة نصياً.

- الاسم الأصلي: PixiJS + official PixiJS skills
- النوع: Open-source 2D GPU rendering library and skill collection
- مسار Claude: Official skill collection supports Claude Code and supplies current PixiJS v8 practices. Claude generates code; a browser runtime executes it.
- المتطلبات: PixiJS v8 project and browser/GPU support; game/sprite assets when needed. Skills do not install the runtime.
- الترخيص والتكلفة: PixiJS library and official pixijs-skills repository: MIT, no license fees. Agent, assets and hosting separate.
- ملاحظة مهمة: Use the v8 APIs rather than old v7 patterns. The pinned snapshot includes 26 SKILL.md files: the general overview plus 25 focused skills; an official skill is guidance, not an application-controlling MCP.
- داخل الأرشيف: ملفات نصية فعلية
- حدود النسخة: Complete Markdown skill/reference tree at the pinned commit, plus README and LICENSE. Plugin configuration, runtime, demos and assets omitted.
- مجلد الملفات: [text-snapshots/pixijs-skills](../text-snapshots/pixijs-skills/)
- [تعليمات الإعداد أو المصدر الرسمي](https://github.com/pixijs/pixijs)
- المصادر:
  - [2D WebGL/WebGPU renderer, capabilities and MIT](https://github.com/pixijs/pixijs)
  - [Official Claude-compatible skill collection](https://pixijs.com/llms)
  - [Source, supported skill folders and MIT](https://github.com/pixijs/pixijs-skills)
  - [MIT redistribution notice](https://github.com/pixijs/pixijs-skills/blob/main/LICENSE)

## 33. نسختك الأصلية من KOSIF Motion Director

توجيه الإخراج البصري وتخطيط توقيت الحركة ومراجعة التفاعل، مع مراعاة العربية وإتاحة الاستخدام ودقة البيانات.

- الاسم الأصلي: KOSIF Motion Director
- النوع: Existing original custom skill preserved unchanged
- مسار Claude: Local custom-skill placement is described in the included USAGE-AR.md.
- المتطلبات: The actual rendering, development or editing tools must exist separately.
- الترخيص والتكلفة: Original user-specific material. No third-party open-source license is newly asserted for these original files.
- ملاحظة مهمة: Preserved from the previous deliverable without modification. Not the community abdullatif06/claude-motion-director project. No new Claude runtime test was performed.
- داخل الأرشيف: ملفات نصية فعلية
- حدود النسخة: All three original files copied byte-for-byte. No new test or installation performed.
- مجلد الملفات: [original-kosif-motion-director](../original-kosif-motion-director/)
- [تعليمات الإعداد أو المصدر الرسمي](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- المصادر:
  - [Claude Code skill setup](https://code.claude.com/docs/en/skills)
  - [Claude custom Skills setup](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

