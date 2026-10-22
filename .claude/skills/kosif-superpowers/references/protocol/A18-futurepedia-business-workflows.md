# A18 — Futurepedia «For Business», workflows, directory and courses → Claude-native runbooks

> **متى تقرأه / when to read:** طلب عمل تجاري بالذكاء الاصطناعي حسب الوظيفة (مبيعات، تسويق، دعم، عمليات، توظيف، تمويل، محتوى)، أو «اعمل لي workflow / خطة أتمتة»، أو «أي أداة أستخدم لـ…»، أو «فور بيزنس». Any business-function AI request, a workflow/playbook request, or "which AI tool for X".
>
> **Canonical routing:** [PROTOCOL.md](../../PROTOCOL.md) → this appendix → `scripts/business_workflows.py`.

## الفهرس / contents

1. [Provenance and boundary](#provenance-and-boundary)
2. [What each section of the site is for](#what-each-section-of-the-site-is-for)
3. [Business functions (adoption index)](#business-functions-adoption-index)
4. [Workflow anatomy and the routing idea](#workflow-anatomy-and-the-routing-idea)
5. [The 64 workflows](#the-64-workflows)
6. [Commands](#commands)
7. [Gates](#gates)

## Provenance and boundary

Reviewed in a browser on 2026-10-23: `/business`, `/workflows` (library 36 + creator playbooks 28 via the site's public JSON listing), `/ai-tools` (directory taxonomy), `/courses` + `/learn` (Skill Leap catalogue) and `/whats-new` (news feed). Stored in [`data/futurepedia_business_workflows.json`](../../data/futurepedia_business_workflows.json): **facts only** — function names, adoption %, example companies, category names/counts, workflow names, goals, durations, difficulty, step titles and the tool each step names. Not stored: the workflows' copy-ready prompts and tips, course lessons (paid, not opened), or editorial text.

## What each section of the site is for

| section | what it is | how KOSIF uses it |
|---|---|---|
| **For Business** (`/business`) | an adoption index of AI use by 9 business functions, with tool categories, trending courses and real-company examples | `business_workflows.py functions`: pick where to start, then jump to matching workflows |
| **Workflows** (`/workflows`) | 36 step-by-step playbooks by role + 28 creator playbooks; each step = title + tool + copy-ready prompt + tip; users can also build their own | `list/search/show` + `plan`: each step re-routed to what Claude does itself, with approval gates |
| **AI Directory** (`/ai-tools`) | ~3,700+ tools in 10 groups / 50+ categories | the taxonomy tells which kind of tool a task needs; Claude checks connectors before suggesting any |
| **Learn / Courses** (`/learn`, `/courses`) | Skill Leap: 27 paid courses (free: 14-Day AI Boot Camp + Prompting Essentials), $29.99/mo | a curriculum map only; KOSIF teaches by doing the workflow, not by reproducing lessons |
| **What's New** (`/whats-new`) | dated release notes per AI tool (major releases, features, pricing, integrations, fixes) | re-read live when a plan depends on a tool's current feature or price; never trust a stored copy |
| **Style Atlas** | 86 explainer styles | see [A15](A15-futurepedia-style-atlas.md) |

## Business functions (adoption index)

| function | الوظيفة | adoption | what AI does there | KOSIF workflows |
|---|---|---|---|---|
| Writing & Editing | الكتابة والتحرير | 85% | generate, edit and rephrase content | content-creation-pipeline, content-repurposing-engine, customer-case-study-builder, reusable-customer-reply-skill |
| Design & Creative | التصميم والإبداع | 83% | graphics, video editing and content creation | ai-powered-design-sprint, brand-identity-generator, video-content-repurposing, create-explainer-graphics-and-video-inserts, compare-image-tools-with-real-tests |
| Customer Service & Support | خدمة العملاء والدعم | 80% | chatbots, automated responses, sentiment analysis | customer-support-automation, route-customer-support-with-ai, reusable-customer-reply-skill |
| Growth & Marketing | النمو والتسويق | 69% | campaign optimisation, customer data, personalisation | seo-content-strategy, social-media-campaign-launch, email-marketing-automation, webinar-funnel-builder, landing-page-optimization, influencer-collaboration-pipeline |
| Technology & IT | التقنية | 63% | website builders, e-commerce, code assistants | build-an-internal-tool-with-codex, client-micro-app-in-a-day, pick-the-right-no-code-ai-build-path, research-led-landing-page |
| Workflow Automation | أتمتة سير العمل | 60% | agents run multi-step work with a human checking the result | agency-operations-autopilot, document-processing-pipeline, automate-a-purchase-to-subscriber-handoff, delegate-a-research-task-to-an-ai-agent |
| Sales | المبيعات | 33% | CRM prediction, automated outreach, personalised pitches | lead-generation-automation, deal-intelligence-pipeline, cold-outreach-at-scale, outbound-avatar-video-funnel |
| Operations | العمليات | 25% | scheduling, prioritisation, forecasting | meeting-notes-and-action-items, weekly-kpi-dashboard, okr-planning-sprint, personal-productivity-reset, prepare-a-pre-meeting-brief |
| Back Office | المكتب الخلفي | 20% | HR, accounting and document management | document-processing-pipeline, investor-update-automation, hiring-pipeline-kickoff |

Reading it: the high-adoption functions (writing, design, support) are where Claude alone already covers most steps; the low-adoption ones (back office 20%, operations 25%, sales 33%) are where connectors and approvals matter most — and where a careful, gated runbook adds the most value.

## Workflow anatomy and the routing idea

A Futurepedia workflow = **goal + role + time + difficulty + 3–6 steps**, each step = **title + one named tool + a structured copy-ready prompt + a one-line rule of thumb**. The creator playbooks add safety habits worth keeping everywhere: consent before recording people, test with non-sensitive or redacted data, review before sending, verify every claim, choose one reversible next action.

KOSIF's upgrade: the named tool is replaceable. Every step is mapped to one of 13 routes and executed by what is actually available in the session:

| route | what Claude uses here | source tools mapped |
|---|---|---|
| `write` | Claude (native writing/reasoning; my-writing-style when drafting as the user) | Claude, ChatGPT, Jasper, Anyword, Grammarly, Codex |
| `research` | WebSearch/WebFetch + anthropic-skills:deep-research (cited sources); rank/monitoring data needs a connector | Perplexity, Google Gemini, NotebookLM, Do Anything, Semrush One, Surfer, Brandwatch, Browse AI |
| `data` | python (pandas/duckdb) + charts (dataviz) + Sheets artifact or xlsx skill | Julius AI, Rows AI |
| `slides` | Slides artifact type (or pptx skill when a .pptx is named) | Gamma |
| `design` | Design artifact / creative_paint.py / unified_draw.py; paid image generation (Higgsfield) only with explicit approval | Canva, Figma AI, Leonardo AI, Uizard |
| `docs` | Claude Docs (living doc) or Notion connector when the user asks for Notion | Notion AI |
| `transcribe` | faster-whisper via montage_pro.py intake (consent of every participant first) | Descript, Otter.ai, Fireflies.ai, Granola, Whisper, Wispr Flow |
| `video` | montage_pro.py / kosif-montage-motion (clips, captions, 9:16) | Opus Clip, VEED.IO |
| `voice_avatar` | local TTS (Piper) or a connected voice/avatar service; consent + spend approval required | ElevenLabs, HeyGen, OpenAI API |
| `build` | Artifact (hosted page/app) or code in the repo; test with non-sensitive sample data | Lovable, Hostinger AI Website Builder |
| `automate` | scheduled tasks (create_trigger/send_later) + local scripts; third-party automations through their connector | Zapier, Make, n8n, MagicForm AI |
| `crm_comms` | connector via SearchMcpRegistry; Claude drafts, the user approves every send/post/update | Superhuman, HubSpot, Apollo, Outreach, Gong, Intercom, Zendesk, Hootsuite, Asana, Motion, Reclaim.ai, Reclaim, Lindy.ai, Fyxer, Howie |
| `manual` | the user does this step (export, payment, real-world action) | - |

Measured over the 64 workflows (286 steps): **220 steps (77%) run Claude-natively**; 28 workflows are 100% native, 44 are ≥75%, 58 are ≥50%; the rest depend on mail/CRM/calendar/automation connectors and the user's approval.

## The 64 workflows

| ID | workflow | role | goal | time | native |
|---|---|---|---|---|---|
| FW-01 | Client Deliverable Factory | صاحب وكالة | Scale client work | 90min | 83% |
| FW-02 | Agency Operations Autopilot | صاحب وكالة | Run agency on autopilot | 2hour | 0% |
| FW-03 | Data Analysis & Reporting | محلل | Get insights faster | 60min | 100% |
| FW-04 | Market Research Deep Dive | محلل | Understand market trends | 90min | 100% |
| FW-05 | Content Creation Pipeline | صانع محتوى | Create content faster | 30min | 80% |
| FW-06 | Video Content Repurposing | صانع محتوى | Create videos faster | 60min | 80% |
| FW-07 | Podcast to Content Empire | صانع محتوى | Maximize content output | 45min | 100% |
| FW-08 | AI-Powered Design Sprint | مصمم | Design faster | 2hour | 100% |
| FW-09 | Brand Identity Generator | مصمم | Build brand assets | 3hour | 100% |
| FW-10 | Meeting Notes & Action Items | مؤسس/مدير | Automate admin tasks | 20min | 50% |
| FW-11 | Investor Update Automation | مؤسس/مدير | Save time on reporting | 45min | 83% |
| FW-12 | Competitive Intelligence Tracker | مؤسس/مدير | Stay ahead of competition | 60min | 67% |
| FW-13 | Fundraising Pipeline Manager | مؤسس/مدير | Close your next round faster | 90min | 60% |
| FW-14 | Customer Discovery Synthesis | مؤسس/مدير | Find product-market fit faster | 2hour | 67% |
| FW-15 | Weekly KPI Dashboard | مؤسس/مدير | Stay on top of the numbers | 30min | 67% |
| FW-16 | Board Meeting Prep | مؤسس/مدير | Prepare for board meetings faster | 90min | 75% |
| FW-17 | Product Launch Checklist | مؤسس/مدير | Launch without chaos | 60min | 75% |
| FW-18 | Hiring Pipeline Kickoff | مؤسس/مدير | Start hiring faster | 45min | 75% |
| FW-19 | OKR Planning Sprint | مؤسس/مدير | Plan the quarter with clarity | 60min | 100% |
| FW-20 | SEO Content Strategy | مسوّق | Get more leads | 90min | 100% |
| FW-21 | Social Media Campaign Launch | مسوّق | Boost brand awareness | 60min | 67% |
| FW-22 | Email Marketing Automation | مسوّق | Increase conversions | 75min | 67% |
| FW-23 | Webinar Funnel Builder | مسوّق | Generate leads from webinars | 75min | 75% |
| FW-24 | Landing Page Optimization | مسوّق | Increase conversion rates | 45min | 100% |
| FW-25 | Influencer Collaboration Pipeline | مسوّق | Drive awareness through creators | 60min | 100% |
| FW-26 | Content Repurposing Engine | مسوّق | Get more mileage from every piece of content | 45min | 75% |
| FW-27 | Customer Case Study Builder | مسوّق | Build sales proof points | 60min | 80% |
| FW-28 | Customer Support Automation | عمليات | Improve customer support | 2hour | 50% |
| FW-29 | Document Processing Pipeline | عمليات | Eliminate manual data entry | 90min | 60% |
| FW-30 | Learn Any New Skill with AI | عام | Learn new skills faster | 25min | 75% |
| FW-31 | Personal Productivity Reset | عام | Save time on repetitive work | 20min | 75% |
| FW-32 | AI-Powered Talent Sourcing | توظيف | Hire faster | 45min | 67% |
| FW-33 | Interview Prep & Debrief Pipeline | توظيف | Improve hiring decisions | 30min | 100% |
| FW-34 | Lead Generation Automation | مبيعات | Get more leads | 45min | 40% |
| FW-35 | Deal Intelligence Pipeline | مبيعات | Close more deals | 30min | 67% |
| FW-36 | Cold Outreach at Scale | مبيعات | Book more meetings | 60min | 50% |
| FP-01 | Reusable Customer Reply Skill (Kevin (Futurepedia)) | عمليات | Draft consistent customer replies you can review before sending | 30min | 100% |
| FP-02 | Compare Image Tools with Real Tests (Kevin (Futurepedia)) | مصمم | Choose the right image tool based on your own results | 45min | 100% |
| FP-03 | Research into a Reusable Knowledge Base (Kevin (Futurepedia)) | محلل | Save a reusable, source-linked research note | 30min | 100% |
| FP-04 | Build an Internal Tool with Codex (Kevin (Futurepedia)) | عمليات | Test one useful internal tool with real sample data | 60min | 100% |
| FP-05 | Automate a Purchase-to-Subscriber Handoff (Kevin (Futurepedia)) | عمليات | Test a purchase event updating the correct subscriber status | 45min | 50% |
| FP-06 | Create Explainer Graphics and Video Inserts (Kevin (Futurepedia)) | صانع محتوى | Produce a checked diagram or visual insert for a video | 30min | 100% |
| FP-07 | Turn Meeting Notes into Reviewed Actions (Kevin (Futurepedia)) | مؤسس/مدير | Save a reviewed action list without losing uncertainty | 20min | 100% |
| FP-08 | Turn Shorts into Posts for Every Platform (Saj (Skill Leap AI)) | صانع محتوى | Prepare a complete social-post package from one short video | 60min | 100% |
| FP-09 | Meeting Notes to an Actionable Recap (Saj (Skill Leap AI)) | مؤسس/مدير | Prepare a reviewed meeting recap with clear owners and due dates | 15min | 100% |
| FP-10 | Creating Courses and Presentations (Saj (Skill Leap AI)) | صانع محتوى | Create a reviewed lesson outline, teaching deck, and learner handout | 90min | 100% |
| FP-11 | Client Micro-App in a Day (Saj (Skill Leap AI)) | صاحب وكالة | Ship a paid AI tool fast | 6hour | 100% |
| FP-12 | Outbound Avatar Video Funnel (Saj (Skill Leap AI)) | مبيعات | Book real sales calls with the right people | 2hour | 50% |
| FP-13 | Pick the Right No-Code AI Build Path (Saj (Skill Leap AI)) | مؤسس/مدير | Ship the simplest tool that actually does the job | 15min | 100% |
| FP-14 | Clarify Your Goals with ChatGPT (My First Million) | عام | Choose realistic priorities and next-week actions | 25min | 100% |
| FP-15 | Turn a Voice Note into an Action Brief (My First Million) | مؤسس/مدير | Capture an idea and create a usable action brief | 15min | 100% |
| FP-16 | Prepare a Pre-Meeting Brief (My First Million) | مؤسس/مدير | Receive a concise brief before one test meeting | 45min | 0% |
| FP-17 | Triage Your Inbox and Schedule a Follow-Up (My First Million) | مؤسس/مدير | Review reply drafts and coordinate one meeting | 30min | 25% |
| FP-18 | Build a Source-Grounded Business Biography (My First Million) | مؤسس/مدير | Create a cited founder timeline and lessons for your own situation | 40min | 100% |
| FP-19 | Delegate a Research Task to an AI Agent (My First Million) | عام | Receive a research deliverable you can inspect before acting | 30min | 100% |
| FP-20 | Research to an Interactive Audio Brief (Marketing Against the Grain) | محلل | Create a source-grounded briefing on one topic | 30min | 100% |
| FP-21 | Research-Led Landing Page (Marketing Against the Grain) | مسوّق | Create a landing-page draft grounded in real product information | 60min | 100% |
| FP-22 | Test-Every-Tool Friday (Matt Wolfe) | صانع محتوى | Stay first to cover new tools | 5hour | 100% |
| FP-23 | Build Your Own Channel Producer AI (Matt Wolfe) | صانع محتوى | Make every title and thumbnail call with real data, not a gut feeling | 45min | 75% |
| FP-24 | One-Person SaaS Validation Sprint (Starter Story) | مؤسس/مدير | Test the idea before you build it | 1week | 80% |
| FP-25 | Faceless YouTube Channel Engine (Starter Story) | صانع محتوى | Build a steady stream of content without filming | 3hour | 80% |
| FP-26 | 2-Week AI Build Accelerator (Starter Story) | مؤسس/مدير | Ship a working product in under 2 weeks | 2week | 75% |
| FP-27 | Research to an Audio Learning Brief (Tina Huang) | محلل | Create a sourced audio brief on a topic you want to learn | 45min | 25% |
| FP-28 | Route Customer Support with AI (Tina Huang) | عمليات | Test a support-routing workflow with safe escalation | 60min | 0% |

## Commands

```bash
python3 scripts/business_workflows.py functions
python3 scripts/business_workflows.py search "بودكاست"
python3 scripts/business_workflows.py list --role sales
python3 scripts/business_workflows.py show FW-07
python3 scripts/business_workflows.py coverage
python3 scripts/business_workflows.py plan --workflow FW-07 --context "حلقة بودكاست عربية 40 دقيقة" --out out/biz/podcast-plan.md
python3 -m unittest evals/test_business_workflows.py
```

## Gates

- A plan is `PLAN_ONLY` until each step is executed and its output reviewed.
- Send, post, update an external system, spend, schedule a standing automation, record or voice-clone a person: **explicit approval each time** (USIP safe defaults).
- Before naming a third-party tool, check connectors (SearchMcpRegistry); prefer what the session can do; never invent tool output.
- Tool features and prices change: re-check `/whats-new` or the vendor before relying on them.
- Never paste the site's workflow prompts or course material into the repository; write KOSIF's own.

