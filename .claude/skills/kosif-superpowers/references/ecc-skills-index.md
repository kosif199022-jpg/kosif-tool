# فهرس مهارات ECC الـ311 / ECC skills index (all 311)

**What this gives you:** every skill in Everything Claude Code (ECC) on one page — a one-line purpose in our own words, a normalized category and a relevance score — so you can find a method, decide what is worth installing, or avoid writing a skill that already exists, without opening 311 SKILL.md files.
**Open it when:** someone mentions ECC or asks "is there a skill for X?", before authoring a new skill (AGENT-26 skill scout), or when mapping a large skill set (GRAPH-16). Harness overview and install: [ecc-harness.md](ecc-harness.md).

> **Attribution.** ECC — https://github.com/affaan-m/ECC — **MIT License, Copyright (c) 2026 Affaan Mustafa**. Snapshot: commit `76aaa77` (2026-10-15), package `ecc-universal` 2.2.3. Each skill lives at `skills/<name>/SKILL.md` in that repo. Purposes below are paraphrased from each skill's frontmatter and body (read as data; nothing was executed). Some skills declare a different licence or a third-party origin — see the **flags** column and credit the upstream when you reuse an idea.

## المحتويات / Contents
1. Legend · 2. Counts · 3. Best picks (relevance 3) · 4. Full table (311) · 5. Read or install?

## 1. المفتاح / Legend
- **rel** = relevance to this skill's goals (capability awareness, thinking, agents, code, motion): **3** core method worth knowing by heart · **2** useful pattern · **1** niche, or a capability signal ("Claude can act as a specialist here") · **0** out of scope here (language/framework/industry reference).
- **flags:** 🔑 needs an account, key or paid service · a licence name = the skill declares a licence other than the repo's MIT · community/port = contributed or adapted from another project (credit the upstream) · stub / deprecated as noted.
- **→** = where the method is distilled in this skill (power ID).
- Categories are our normalization (15 groups); ECC itself does not categorize skills this way.

## 2. العدد / Counts
| Category | الفئة | Skills | rel 3 | rel 2 |
|---|---|---|---|---|
| Agents & orchestration | الوكلاء والتنسيق | 29 | 8 | 11 |
| Thinking & planning | التفكير والتخطيط | 21 | 8 | 6 |
| Verification, QA & tests | التحقق والاختبار | 30 | 3 | 3 |
| Security & safety | الأمان | 15 | 0 | 2 |
| Skills, memory & context | المهارات والذاكرة والسياق | 15 | 3 | 7 |
| Research, docs & knowledge | البحث والتوثيق | 16 | 3 | 7 |
| Motion, video & media | الموشن والفيديو | 15 | 12 | 3 |
| Design & UI craft | التصميم والواجهات | 7 | 2 | 1 |
| Content, marketing & business | المحتوى والأعمال | 18 | 0 | 4 |
| Data, ML & LLM ops | البيانات والتعلم الآلي | 10 | 0 | 1 |
| Integrations & connectors | التكاملات والموصلات | 11 | 0 | 1 |
| Languages, frameworks & code | اللغات والأطر | 55 | 0 | 2 |
| DevOps, tooling & infra | التشغيل والأدوات | 36 | 0 | 0 |
| Industry domain specialist | قطاعات متخصصة | 18 | 0 | 0 |
| ECC internals / host-specific | داخليات ECC | 15 | 0 | 0 |
| **Total** | **المجموع** | **311** | **39** | **48** |

Relevance totals: 3 = 39, 2 = 48, 1 = 90, 0 = 134.

## 3. أفضل الاختيارات / Best picks (relevance 3)
- **Agents & orchestration:** `agent-harness-construction`; `agent-introspection-debugging` → AGENT-19; `dynamic-workflow-mode`; `gan-style-harness` → AGENT-13; `gateguard` → CODE-06; `iterative-retrieval` → AGENT-03; `loop-design-check` → AGENT-16; `parallel-execution-optimizer` → AGENT-06
- **Thinking & planning:** `agent-self-evaluation`; `agentic-engineering` → AGENT-30; `benchmark-optimization-loop` → CODE-14; `blueprint`; `change-impact` → CODE-05; `council` → AGENT-12; `intent-driven-development`; `search-first` → CODE-01
- **Verification, QA & tests:** `eval-harness` → CODE-10; `santa-method` → AGENT-11; `verification-loop` → CODE-09
- **Skills, memory & context:** `growth-log` → AGENT-32; `skill-scout` → AGENT-26; `workspace-surface-audit`
- **Research, docs & knowledge:** `deep-research` → SEC-01; `documentation-lookup` → CODE-02; `research-ops`
- **Motion, video & media:** `fal-ai-media`; `frontend-slides`; `manim-video`; `motion-advanced`; `motion-foundations`; `remotion-video-creation`; `taste`; `taste-application`; `taste-distillation`; `tasteforge-video`; `ui-demo`; `video-editing`
- **Design & UI craft:** `frontend-design-direction`; `make-interfaces-feel-better`

## 4. الجدول الكامل / Full table (311, alphabetical as in the repo)
| # | skill | purpose (our words) | category | rel | flags / → |
|---|---|---|---|---|---|
| 1 | accessibility | WCAG 2.2 AA across web/iOS/Android: roles, labels, traits, focus | Design & UI craft | 1 |  |
| 2 | agent-architecture-audit | audit 12-layer agent stack (wrapper regression, memory pollution, tool discipline) | Agents & orchestration | 2 | third-party origin |
| 3 | agent-eval | head-to-head eval of coding agents: pass rate, cost, time, consistency | Agents & orchestration | 2 |  |
| 4 | agent-harness-construction | design action space, observation shape, recovery contract, context budget | Agents & orchestration | 3 |  |
| 5 | agent-introspection-debugging | capture→diagnose→contained recovery→report when agent loops/fails | Agents & orchestration | 3 | → AGENT-19 |
| 6 | agent-payment-x402 | x402 payments, budgets, wallets for agents | Industry domain specialist | 0 | 🔑, community/port |
| 7 | agent-runtime-gateway-smoke-test | smoke-test local agent API + tunnel + sandbox callback | DevOps, tooling & infra | 0 |  |
| 8 | agent-security-hardening | hardening for agents touching untrusted content/tools/files | Security & safety | 2 | → SEC-04 |
| 9 | agent-self-evaluation | 5-axis self-rating after non-trivial task | Thinking & planning | 3 |  |
| 10 | agent-sort | sort ECC components into DAILY vs LIBRARY install buckets | ECC internals / host-specific | 1 |  |
| 11 | agentic-engineering | eval-first, 15-min units, model routing | Thinking & planning | 3 | → AGENT-30 |
| 12 | agentic-os | persistent multi-agent OS on Claude Code: kernel, memory files, schedules | Agents & orchestration | 2 |  |
| 13 | ai-first-engineering | team operating model when AI writes most code | Thinking & planning | 1 |  |
| 14 | ai-regression-testing | regression tests for AI-written code, sandbox API tests | Verification, QA & tests | 1 |  |
| 15 | android-clean-architecture | Android/KMP clean architecture | Languages, frameworks & code | 0 |  |
| 16 | angular-developer | Angular codegen/signals guidance | Languages, frameworks & code | 0 |  |
| 17 | api-connector-builder | add an integration by matching repo's existing pattern exactly | Languages, frameworks & code | 1 | community/port; → CODE-07 |
| 18 | api-design | REST naming, status codes, pagination, versioning | Languages, frameworks & code | 0 |  |
| 19 | architecture-decision-records | numbered ADRs in docs/adr/ | Thinking & planning | 1 | → CODE-19 |
| 20 | article-writing | long-form writing in a voice derived from examples | Content, marketing & business | 2 |  |
| 21 | automation-audit-ops | inventory/overlap audit of jobs, hooks, MCPs | DevOps, tooling & infra | 1 |  |
| 22 | autonomous-agent-harness | autonomous Claude Code: memory, schedules, computer use, queues | Agents & orchestration | 2 |  |
| 23 | autonomous-loops | loop architectures: sequential pipelines to DAG multi-agent | Agents & orchestration | 2 |  |
| 24 | backend-patterns | Node/Express/Next backend patterns | Languages, frameworks & code | 0 |  |
| 25 | benchmark | CWV, API p-latency, build baselines | DevOps, tooling & infra | 1 |  |
| 26 | benchmark-methodology | 9-dimension weighted competitor scoring cards | Content, marketing & business | 1 |  |
| 27 | benchmark-optimization-loop | bounded measured optimization loop | Thinking & planning | 3 | → CODE-14 |
| 28 | bengali-nlp | Bangla Unicode normalization/tokenization (pattern analog for Arabic) | Data, ML & LLM ops | 1 |  |
| 29 | blender-motion-state-inspection | inspect Blender rigs/poses/retarget with evidence (motion domain) | Motion, video & media | 2 |  |
| 30 | blueprint | objective → cold-start multi-PR plan with adversarial review | Thinking & planning | 3 | community/port |
| 31 | brand-discovery | 8-module resumable brand interview | Content, marketing & business | 1 |  |
| 32 | brand-voice | extract reusable VOICE PROFILE from 5-20 samples | Content, marketing & business | 2 |  |
| 33 | brownfield-retrospective | retroactive process audit with 4-axis gap register | Thinking & planning | 1 |  |
| 34 | browser-qa | post-deploy UI verification with browser MCP | Verification, QA & tests | 2 |  |
| 35 | bun-runtime | Bun vs Node | DevOps, tooling & infra | 0 |  |
| 36 | canary-watch | monitor deployed URL after release | DevOps, tooling & infra | 1 |  |
| 37 | carrier-relationship-management | truckload carrier sourcing/rates | Industry domain specialist | 0 |  |
| 38 | change-impact | evidence-backed blast radius before change, reconcile after | Thinking & planning | 3 | → CODE-05 |
| 39 | cisco-ios-patterns | Cisco IOS review | DevOps, tooling & infra | 0 | community/port |
| 40 | ck | per-project memory via /ck node commands | Skills, memory & context | 1 | community/port |
| 41 | claude-devfleet | parallel agents in worktrees via DevFleet | Agents & orchestration | 1 | 🔑, community/port |
| 42 | click-path-audit | trace each button's state writes to find handlers that undo each other | Verification, QA & tests | 2 | community/port; → CODE-13 |
| 43 | clickhouse-io | ClickHouse patterns | Data, ML & LLM ops | 0 |  |
| 44 | code-tour | CodeTour .tour walkthroughs | Research, docs & knowledge | 1 |  |
| 45 | codebase-onboarding | map unfamiliar repo → onboarding guide + starter CLAUDE.md | Research, docs & knowledge | 2 | → CODE-04 |
| 46 | codehealth-mcp | CodeScene MCP (🔑 service) | Integrations & connectors | 0 | 🔑, community/port |
| 47 | coding-standards | naming/readability conventions | Languages, frameworks & code | 0 |  |
| 48 | competitive-platform-analysis | scope & filter competitor set | Content, marketing & business | 1 |  |
| 49 | competitive-report-structure | assemble competitor report | Content, marketing & business | 1 |  |
| 50 | compose-multiplatform-patterns | Compose MP | Languages, frameworks & code | 0 |  |
| 51 | config-gc | garbage-collect ~/.claude config | Skills, memory & context | 1 |  |
| 52 | configure-ecc | ECC setup wizard | ECC internals / host-specific | 0 |  |
| 53 | connections-optimizer | X/LinkedIn network pruning | Content, marketing & business | 0 |  |
| 54 | content-engine | platform-native content systems (X, TikTok, YouTube) — relevant to reels | Content, marketing & business | 2 |  |
| 55 | content-hash-cache-pattern | SHA-256 content-hash cache for expensive file processing (render caching) | Languages, frameworks & code | 2 | → CODE-21 |
| 56 | context-and-decisions | CONTEXT.md glossary vs ADR routing | Thinking & planning | 1 |  |
| 57 | context-budget | route to native /context; bounded opt-in static audit | Skills, memory & context | 2 | → AGENT-29 |
| 58 | continuous-agent-loop | loop with gates/evals/recovery (pointer) | Agents & orchestration | 1 |  |
| 59 | continuous-learning | v1, superseded | Skills, memory & context | 0 | deprecated (use v2) |
| 60 | continuous-learning-v2 | hook-observed atomic "instincts" with confidence 0.3-0.9 | Skills, memory & context | 2 | → AGENT-32 |
| 61 | contract-first | one machine-checkable contract (OpenAPI etc.) | Languages, frameworks & code | 1 |  |
| 62 | conventional-commit-review | Conventional Commits drafting | DevOps, tooling & infra | 0 | → CODE-22 |
| 63 | cost-aware-llm-pipeline | model routing, budgets, caching | Data, ML & LLM ops | 1 |  |
| 64 | cost-tracking | ECC cost log reporting | ECC internals / host-specific | 0 | community/port |
| 65 | council | 4-voice decision council with fresh subagents | Thinking & planning | 3 | → AGENT-12 |
| 66 | council-multi-model | add external Codex critique (Codex-specific) | Thinking & planning | 1 | needs Codex CLI |
| 67 | counterparty-channel-discipline | agents in shared channels: mention gating | Agents & orchestration | 1 |  |
| 68 | cpp-coding-standards | C++ Core Guidelines | Languages, frameworks & code | 0 |  |
| 69 | cpp-testing | GoogleTest | Verification, QA & tests | 0 |  |
| 70 | crosspost | adapt one post per platform | Content, marketing & business | 1 |  |
| 71 | csharp-testing | xUnit | Verification, QA & tests | 0 |  |
| 72 | customer-billing-ops | Stripe-like billing ops (🔑) | Content, marketing & business | 0 | 🔑 |
| 73 | customs-trade-compliance | HS codes, Incoterms | Industry domain specialist | 0 |  |
| 74 | dart-flutter-patterns | Flutter | Languages, frameworks & code | 0 |  |
| 75 | dashboard-builder | dashboards that answer operator questions | Data, ML & LLM ops | 1 | community/port |
| 76 | data-scraper-agent | scheduled scraping agent with AI enrichment (capability example) | Agents & orchestration | 2 | community/port |
| 77 | data-throughput-accelerator | isolate bottleneck in large data movement | DevOps, tooling & infra | 1 |  |
| 78 | database-migrations | expand-contract migrations | Languages, frameworks & code | 0 |  |
| 79 | deep-research | cited multi-source research with untrusted-source rules | Research, docs & knowledge | 3 | 🔑; → SEC-01 |
| 80 | deepseek-harness-setup | ECC on DeepSeek harness | ECC internals / host-specific | 0 | community/port |
| 81 | defi-amm-security | Solidity AMM checklist | Industry domain specialist | 0 | community/port |
| 82 | delivery-gate | Stop hook blocking finish until checks pass; detects rationalization phrases | Verification, QA & tests | 2 | → AGENT-21 |
| 83 | deployment-patterns | CI/CD, Docker, rollback | DevOps, tooling & infra | 0 |  |
| 84 | design-system | extract tokens; 10-dim visual audit; AI-slop detection | Design & UI craft | 2 |  |
| 85 | dev-team | PM/Architect/Dev/QA personas respond to one problem | Thinking & planning | 2 | community/port; → AGENT-15 |
| 86 | django-celery | background jobs and scheduled tasks in Django with Celery: retries, beat, workflows, tests | Languages, frameworks & code | 0 |  |
| 87 | django-patterns | Django and DRF architecture: ORM use, caching, signals, middleware | Languages, frameworks & code | 0 |  |
| 88 | django-security | Django hardening: authn/authz, CSRF, injection and XSS defences, safe deploy settings | Security & safety | 0 |  |
| 89 | django-tdd | test-first Django with pytest-django, factories, mocks and API tests | Verification, QA & tests | 0 |  |
| 90 | django-verification | Django pre-merge loop: lint/types, migration safety, tests, dependency and code scans | Verification, QA & tests | 0 |  |
| 91 | dmux-workflows | tmux parallel agents | Agents & orchestration | 1 |  |
| 92 | docker-patterns | Docker and Compose for local dev: networking, volumes, multi-service setups, container security | DevOps, tooling & infra | 0 |  |
| 93 | docs-governance | ECC doc routing | ECC internals / host-specific | 0 |  |
| 94 | documentation-lookup | fetch live library docs (Context7) instead of memory | Research, docs & knowledge | 3 | → CODE-02 |
| 95 | dotnet-patterns | idiomatic C#/.NET: dependency injection, async/await, conventions | Languages, frameworks & code | 0 |  |
| 96 | dynamic-workflow-mode | when to build a task-local harness; objective/inputs/outputs/eval/handoff | Agents & orchestration | 3 |  |
| 97 | e2e-testing | Playwright POM, flaky strategies | Verification, QA & tests | 1 |  |
| 98 | ecc-guide | answer from live repo surface, not memory (pattern relevant) | ECC internals / host-specific | 1 | community/port |
| 99 | ecc-recipes | map workflow to ECC command group | ECC internals / host-specific | 0 | community/port |
| 100 | ecc-tools-cost-audit | ECC billing audit | ECC internals / host-specific | 0 |  |
| 101 | email-ops | mailbox triage | DevOps, tooling & infra | 0 |  |
| 102 | energy-procurement | electricity/gas procurement | Industry domain specialist | 0 |  |
| 103 | enterprise-agent-ops | lifecycle/observability for long-lived agents | DevOps, tooling & infra | 1 |  |
| 104 | error-handling | typed errors, retries, circuit breakers TS/Py/Go | Languages, frameworks & code | 1 | → CODE-15 |
| 105 | esign-field-placement | Deterministic placing of signature/date fields in web e-sign composer via browser automation (fixed page, numeric location panel) | DevOps, tooling & infra | 1 |  |
| 106 | eval-harness | Eval-driven development: capability+regression evals, code/model/human graders, pass@k and pass^k | Verification, QA & tests | 3 | → CODE-10 |
| 107 | evm-token-decimals | Runtime ERC-20 decimals lookup, chain-aware caching, bridged precision drift | Industry domain specialist | 0 |  |
| 108 | exa-search | Exa MCP neural web/code/company search + untrusted-result rules | Research, docs & knowledge | 2 | 🔑; → SEC-01 |
| 109 | fal-ai-media | fal.ai MCP image/video/audio generation (Nano Banana, Seedance, Kling, Veo 3, CSM-1B), params, cost estimate | Motion, video & media | 3 | 🔑 |
| 110 | fastapi-patterns | FastAPI structure, Pydantic v2, DI, auth, tests | Languages, frameworks & code | 1 |  |
| 111 | finance-billing-ops | Evidence-first revenue/pricing/refund truth workflow (ECC-specific) | Content, marketing & business | 0 |  |
| 112 | flox-environments | Reproducible Nix-based dev envs with Flox | DevOps, tooling & infra | 1 |  |
| 113 | flutter-dart-code-review | Flutter/Dart review checklist | Languages, frameworks & code | 0 |  |
| 114 | foundation-models-on-device | Apple FoundationModels on-device LLM, @Generable, iOS 26 | Languages, frameworks & code | 1 |  |
| 115 | frontend-a11y | React/Next a11y: semantics, ARIA, focus, keyboard | Design & UI craft | 1 |  |
| 116 | frontend-design-direction | Pick purpose/audience/tone/memorable detail before UI; content-state matrix; rendered evidence gate with JSON checker | Design & UI craft | 3 | community/port |
| 117 | frontend-patterns | React/Next patterns, state, perf | Languages, frameworks & code | 1 |  |
| 118 | frontend-slides | Zero-dependency animated HTML decks, 3 style previews, viewport-fit rules, PPTX conversion | Motion, video & media | 3 |  |
| 119 | fsharp-testing | F# xUnit/FsCheck | Verification, QA & tests | 0 |  |
| 120 | gan-style-harness | Planner/Generator/Evaluator loop with weighted 4-criterion rubric, Playwright evaluator, 5-15 iterations | Agents & orchestration | 3 | paraphrases an Anthropic engineering post; → AGENT-13 |
| 121 | gateguard | PreToolUse hook: deny first edit until concrete facts (importers, API, schema, verbatim instruction) are presented | Agents & orchestration | 3 | community/port; → CODE-06 |
| 122 | generating-python-installer | Nuitka + Inno Setup Windows installers, DLL slimming | DevOps, tooling & infra | 1 |  |
| 123 | git-workflow | Branching, commits, rebase vs merge, conflicts | DevOps, tooling & infra | 1 |  |
| 124 | github-ops | gh CLI issue/PR/CI/release ops | DevOps, tooling & infra | 1 |  |
| 125 | golang-patterns | Idiomatic Go | Languages, frameworks & code | 0 |  |
| 126 | golang-testing | Go table tests, fuzzing, bench | Verification, QA & tests | 0 |  |
| 127 | google-workspace-ops | Drive/Docs/Sheets/Slides as one workflow surface | Integrations & connectors | 2 | 🔑 |
| 128 | growth-log | Learning entries = root cause + transferable rule + signal; Bole merge principle | Skills, memory & context | 3 | → AGENT-32 |
| 129 | healthcare-cdss-patterns | Drug interaction, NEWS2/qSOFA scoring | Industry domain specialist | 0 |  |
| 130 | healthcare-emr-patterns | EMR workflows | Industry domain specialist | 0 |  |
| 131 | healthcare-eval-harness | Patient-safety eval suites | Industry domain specialist | 0 |  |
| 132 | healthcare-phi-compliance | PHI classification, RLS, audit trails | Security & safety | 0 |  |
| 133 | hermes-imports | Convert Hermes workflows into sanitized ECC skills | ECC internals / host-specific | 0 |  |
| 134 | hexagonal-architecture | Ports & adapters design | Thinking & planning | 1 |  |
| 135 | hipaa-compliance | HIPAA entrypoint | Security & safety | 0 |  |
| 136 | homelab-network-readiness | VLAN/DNS/WireGuard readiness checklist | DevOps, tooling & infra | 0 |  |
| 137 | homelab-network-setup | Home network planning | DevOps, tooling & infra | 0 |  |
| 138 | homelab-pihole-dns | Pi-hole setup | DevOps, tooling & infra | 0 |  |
| 139 | homelab-vlan-segmentation | VLANs on UniFi/pfSense/MikroTik | DevOps, tooling & infra | 0 |  |
| 140 | homelab-wireguard-vpn | WireGuard setup | DevOps, tooling & infra | 0 |  |
| 141 | hookify-rules | Markdown+YAML rules that warn/block bash/file/prompt/stop events | Agents & orchestration | 2 | → AGENT-20 |
| 142 | i18n-sync | Translate/sync JSON locale files with terminology checks | Languages, frameworks & code | 1 |  |
| 143 | inherit-legacy-style | Scan codebase for implicit conventions, resolve conflicts one at a time, write .ai-style-rules | Languages, frameworks & code | 2 | → CODE-07 |
| 144 | intent-driven-development | Turn ambiguous requests into observable acceptance criteria (Quick Capture vs Full Brief) | Thinking & planning | 3 |  |
| 145 | inventory-demand-planning | Demand forecasting, ABC/XYZ, safety stock (Apache-2.0) | Industry domain specialist | 0 | Apache-2.0 |
| 146 | investor-materials | Pitch decks, memos, models | Content, marketing & business | 1 |  |
| 147 | investor-outreach | Investor emails | Content, marketing & business | 0 |  |
| 148 | ios-icon-gen | iOS icons from SF Symbols / Iconify API (275k icons) | Design & UI craft | 1 |  |
| 149 | iterative-retrieval | Dispatch/Evaluate/Refine/Loop context retrieval, max 3 cycles, relevance thresholds | Agents & orchestration | 3 | → AGENT-03 |
| 150 | ito-baskets | Itô prediction-market data | Integrations & connectors | 0 | 🔑 |
| 151 | ito-compute | Itô GPU RFQ | Integrations & connectors | 0 | 🔑 |
| 152 | ito-inference | Itô serving handoff | Integrations & connectors | 0 | 🔑 |
| 153 | ito-training | Itô training handoff | Integrations & connectors | 0 | 🔑 |
| 154 | java-coding-standards | Java/Spring standards | Languages, frameworks & code | 0 |  |
| 155 | jira-integration | Jira via MCP/REST | Integrations & connectors | 1 | 🔑 |
| 156 | jpa-patterns | JPA/Hibernate | Languages, frameworks & code | 0 |  |
| 157 | knowledge-ops | 6-layer knowledge architecture + ingestion classify/dedupe | Skills, memory & context | 2 | → AGENT-33 |
| 158 | kotlin-coroutines-flows | Kotlin coroutines | Languages, frameworks & code | 0 |  |
| 159 | kotlin-exposed-patterns | Exposed ORM | Languages, frameworks & code | 0 |  |
| 160 | kotlin-ktor-patterns | Ktor server | Languages, frameworks & code | 0 |  |
| 161 | kotlin-patterns | Idiomatic Kotlin | Languages, frameworks & code | 0 |  |
| 162 | kotlin-testing | Kotest/MockK | Verification, QA & tests | 0 |  |
| 163 | kubernetes-patterns | K8s workloads, probes, RBAC | DevOps, tooling & infra | 1 |  |
| 164 | laravel-patterns | Laravel architecture | Languages, frameworks & code | 0 |  |
| 165 | laravel-plugin-discovery | Find Laravel packages via LaraPlugins MCP | Research, docs & knowledge | 1 | 🔑 |
| 166 | laravel-security | Laravel security | Security & safety | 0 |  |
| 167 | laravel-tdd | Laravel tests | Verification, QA & tests | 0 |  |
| 168 | laravel-verification | Verification loop: env, lint, static, tests, scans | Verification, QA & tests | 1 |  |
| 169 | latency-critical-systems | p50/p95/p99, freshness tracking (MIT) | DevOps, tooling & infra | 1 |  |
| 170 | lead-intelligence | Agent lead scoring and outreach pipeline | Content, marketing & business | 0 |  |
| 171 | liquid-glass-design | iOS 26 Liquid Glass material in SwiftUI | Design & UI craft | 1 |  |
| 172 | living-docs-governance | Assign docs constitution/map/status/history roles to stop rot | Research, docs & knowledge | 2 |  |
| 173 | llm-trading-agent-security | Spend limits, simulation, circuit breakers for trading agents | Security & safety | 1 |  |
| 174 | logistics-exception-management | Freight exceptions (Apache-2.0) | Industry domain specialist | 0 | Apache-2.0 |
| 175 | loop-design-check | Design/review agent loops: machine-decidable goal, boundaries, damping, 5 failure modes | Agents & orchestration | 3 | → AGENT-16 |
| 176 | mailtrap-email-integration | Mailtrap email API | Integrations & connectors | 0 | 🔑 |
| 177 | make-interfaces-feel-better | Concrete UI polish: concentric radius, tabular-nums, transitions, 40-44px hit areas | Design & UI craft | 3 | community/port |
| 178 | manim-video | Manim technical explainers: thesis, 3-6 scenes, low-quality smoke render first | Motion, video & media | 3 |  |
| 179 | market-research | Market/competitor research with source attribution | Research, docs & knowledge | 2 |  |
| 180 | marketing-campaign | Campaign planning: audience, angle, copy, short-form | Content, marketing & business | 2 |  |
| 181 | master-agreement-generator | Legal agreement drafts from template + JSON spec | Content, marketing & business | 1 |  |
| 182 | mcp-dependency-review | Static classification of MCP package pinning (SAFE/HIGH/MEDIUM/REVIEW) | Security & safety | 2 | → AGENT-22, SEC-10 |
| 183 | mcp-server-patterns | Build MCP servers with TS SDK, Zod, stdio vs HTTP | Agents & orchestration | 2 |  |
| 184 | messages-ops | Evidence-first reading of texts/DMs, OTP recovery | DevOps, tooling & infra | 0 |  |
| 185 | ml-adoption-playbook | Add ML to non-ML codebases | Data, ML & LLM ops | 1 |  |
| 186 | mle-workflow | Production ML: data contracts, reproducible training, rollback (MIT) | Data, ML & LLM ops | 1 |  |
| 187 | module-regression | keep a REGRESSION.md ledger of each module's consumers and acceptance command; rerun them after a change | Verification, QA & tests | 1 | → CODE-10 |
| 188 | motion-advanced | motion/react drag, gestures, text anim, SVG path draw, useAnimate | Motion, video & media | 3 |  |
| 189 | motion-foundations | Motion tokens, 5 spring presets, reduced motion, SSR-safe initial states | Motion, video & media | 3 |  |
| 190 | motion-patterns | Button/modal/toast/stagger/page/scroll/layout animations | Motion, video & media | 2 |  |
| 191 | mybatis-patterns | MyBatis | Languages, frameworks & code | 0 |  |
| 192 | mysql-patterns | MySQL/MariaDB | Languages, frameworks & code | 0 |  |
| 193 | nanoclaw-repl | ECC REPL ops | ECC internals / host-specific | 0 | stub |
| 194 | nasiko-control-plane | Nasiko CLI lifecycle | ECC internals / host-specific | 0 | stub |
| 195 | nestjs-patterns | NestJS | Languages, frameworks & code | 0 |  |
| 196 | netmiko-ssh-automation | Netmiko SSH automation | DevOps, tooling & infra | 0 |  |
| 197 | network-bgp-diagnostics | BGP diagnostics | DevOps, tooling & infra | 0 |  |
| 198 | network-config-validation | Router config checks | DevOps, tooling & infra | 0 |  |
| 199 | network-interface-health | Interface errors | DevOps, tooling & infra | 0 |  |
| 200 | nextjs-turbopack | Next 16 Turbopack notes | Languages, frameworks & code | 0 |  |
| 201 | nodejs-keccak256 | Keccak-256 vs SHA3 pitfall | Industry domain specialist | 0 |  |
| 202 | nutrient-document-processing | Nutrient DWS API: convert/OCR/redact/sign docs | Integrations & connectors | 1 | 🔑 |
| 203 | nuxt4-patterns | Nuxt 4 | Languages, frameworks & code | 0 |  |
| 204 | openclaw-persona-forge | (Chinese) agent persona/SOUL.md generator with random "card draw", avatar prompts | Content, marketing & business | 1 |  |
| 205 | opensource-pipeline | Fork, sanitize, package private project for public release (3 agents) | DevOps, tooling & infra | 1 |  |
| 206 | operator-approval-loop | Approval contract for agent-drafted outbound messages, hashed drafts, receipts | Security & safety | 1 | → SEC-16 |
| 207 | orch-add-feature | Research→plan→TDD→review→gated commit via ECC agents | Agents & orchestration | 1 |  |
| 208 | orch-build-mvp | SDD/PRD → thin vertical slices → generator-evaluator loop | Agents & orchestration | 2 |  |
| 209 | orch-change-feature | change existing behavior: update tests to the new spec, then the code, then review, then a gated commit | Agents & orchestration | 1 |  |
| 210 | orch-fix-defect | reproduce the bug as a failing regression test, fix to green, review, commit | Agents & orchestration | 1 |  |
| 211 | orch-pipeline | shared engine: size classifier, Research-Plan-TDD-Review-Commit phases, 2 human gates | Agents & orchestration | 2 | → AGENT-10 |
| 212 | orch-refine-code | behavior-preserving refactor with tests kept green | Agents & orchestration | 1 |  |
| 213 | osint-investigation | sparse-clue investigation method (CTF, geolocation, entity linking) | Research, docs & knowledge | 2 | CC-BY-SA-4.0 (ideas only) |
| 214 | parallel-execution-optimizer | dependency graph of parallel lanes, isolated write surfaces, verification table | Agents & orchestration | 3 | → AGENT-06 |
| 215 | perl-patterns | modern Perl 5.36 idioms | Languages, frameworks & code | 0 |  |
| 216 | perl-security | taint mode, DBI, perlcritic | Security & safety | 0 |  |
| 217 | perl-testing | Test2::V0, prove, Devel::Cover | Verification, QA & tests | 0 |  |
| 218 | plan-canvas | annotate and approve plans or HTML in a local browser canvas | ECC internals / host-specific | 1 |  |
| 219 | plan-orchestrate | plan doc to steps, each mapped to an ECC slash command | ECC internals / host-specific | 1 |  |
| 220 | plankton-code-quality | write-time format, lint and fix via hooks (Plankton) | DevOps, tooling & infra | 1 |  |
| 221 | postgres-patterns | indexes, RLS, query tuning | Languages, frameworks & code | 0 | from Supabase skills (MIT) |
| 222 | prediction-market-oracle-research | markets as probability signals | Industry domain specialist | 1 |  |
| 223 | prediction-market-risk-review | compliance and risk review for trading agents | Industry domain specialist | 0 |  |
| 224 | prisma-patterns | Prisma ORM traps | Languages, frameworks & code | 0 |  |
| 225 | product-capability | PRD to an implementation-ready capability contract | Thinking & planning | 2 |  |
| 226 | product-lens | why-before-build diagnostics, ICE scoring | Thinking & planning | 2 |  |
| 227 | production-audit | local-evidence production-readiness audit | Verification, QA & tests | 1 |  |
| 228 | production-scheduling | manufacturing scheduling expertise | Industry domain specialist | 0 | Apache-2.0 |
| 229 | project-flow-ops | GitHub plus Linear triage | DevOps, tooling & infra | 0 |  |
| 230 | prompt-caching-strategy | prompt-cache layout for LLM APIs | Data, ML & LLM ops | 1 |  |
| 231 | prompt-optimizer | diagnose a draft prompt (intent, scope, missing context), output an improved prompt | Thinking & planning | 2 | community/port |
| 232 | python-patterns | Pythonic idioms | Languages, frameworks & code | 0 |  |
| 233 | python-testing | pytest and TDD | Verification, QA & tests | 0 |  |
| 234 | pytorch-patterns | training-loop practice | Data, ML & LLM ops | 1 |  |
| 235 | quality-nonconformance | NCR, 5-Why, 8D root cause | Industry domain specialist | 1 | Apache-2.0 |
| 236 | quarkus-patterns | Java Quarkus | Languages, frameworks & code | 0 |  |
| 237 | quarkus-security | Quarkus security: JWT/OIDC, role checks, validation, safe queries | Security & safety | 0 |  |
| 238 | quarkus-tdd | test-first Quarkus services with JUnit 5, mocks, REST tests and coverage | Verification, QA & tests | 0 |  |
| 239 | quarkus-verification | Quarkus pre-merge loop: build, static analysis, coverage, dependency and container scans | Verification, QA & tests | 0 |  |
| 240 | rails-patterns | Rails 7/8 | Languages, frameworks & code | 0 |  |
| 241 | ralphinho-rfc-pipeline | RFC to a multi-agent DAG of work units with acceptance tests | Agents & orchestration | 2 |  |
| 242 | react-native-patterns | Expo and RN | Languages, frameworks & code | 0 |  |
| 243 | react-patterns | React 18/19 | Languages, frameworks & code | 1 |  |
| 244 | react-performance | 70+ perf rules (Vercel-derived) | Languages, frameworks & code | 0 | from Vercel rules (MIT) |
| 245 | react-testing | RTL, MSW, axe | Verification, QA & tests | 0 |  |
| 246 | recsys-pipeline-architect | Source, Hydrator, Filter, Scorer, Selector, SideEffect | Data, ML & LLM ops | 1 |  |
| 247 | recursive-decision-ledger | append-only ledger for repeated rollouts; confidence is never approval | Thinking & planning | 2 |  |
| 248 | redis-patterns | caching and locks | Languages, frameworks & code | 0 |  |
| 249 | regex-vs-llm-structured-text | regex first, confidence score, LLM only on the low-confidence tail | Data, ML & LLM ops | 2 | → CODE-20 |
| 250 | remotion-video-creation | index of 29 Remotion rule files | Motion, video & media | 3 | mirrors Remotion rules (Remotion licence) |
| 251 | repo-scan | installs an external skill from a pinned commit | DevOps, tooling & infra | 0 |  |
| 252 | research-ops | evidence-first current-state research, labeled evidence types | Research, docs & knowledge | 3 |  |
| 253 | returns-reverse-logistics | returns-ops expertise | Industry domain specialist | 0 | Apache-2.0 |
| 254 | rules-distill | scan skills, pull out cross-cutting principles, turn them into rules | Skills, memory & context | 2 |  |
| 255 | rust-patterns | Rust | Languages, frameworks & code | 0 |  |
| 256 | rust-testing | Rust tests | Verification, QA & tests | 0 |  |
| 257 | safety-guard | careful, freeze and guard modes for destructive commands | Security & safety | 1 | → SEC-15 |
| 258 | santa-method | two context-isolated reviewers on the same rubric, both must pass, fix loop with a cap | Verification, QA & tests | 3 | community/port; → AGENT-11 |
| 259 | scientific-db-pubmed-database | PubMed E-utilities | Research, docs & knowledge | 1 |  |
| 260 | scientific-db-uspto-database | USPTO PatentSearch and TSDR | Research, docs & knowledge | 1 |  |
| 261 | scientific-pkg-gget | gget genomics CLI | Research, docs & knowledge | 1 |  |
| 262 | scientific-thinking-literature-review | systematic review workflow | Research, docs & knowledge | 2 |  |
| 263 | scientific-thinking-scholar-evaluation | evaluate papers and evidence quality | Research, docs & knowledge | 2 |  |
| 264 | search-first | search for an existing package, MCP, skill or repo before building; adopt, extend, compose or build | Thinking & planning | 3 | → CODE-01 |
| 265 | security-bounty-hunter | remotely reachable vulnerability hunting | Security & safety | 0 |  |
| 266 | security-review | appsec checklist | Security & safety | 1 | → SEC-08 |
| 267 | security-scan | AgentShield scan of .claude config | Security & safety | 1 | → SEC-09 |
| 268 | seo | technical SEO | Content, marketing & business | 0 |  |
| 269 | skill-comply | measure whether skills or rules are followed, using scenarios at 3 strictness levels | Skills, memory & context | 2 | → AGENT-27 |
| 270 | skill-host-compat | lint skill frontmatter for Codex/Cursor | ECC internals / host-specific | 0 |  |
| 271 | skill-scout | search local, marketplace and GitHub skills before creating one; vet; rank | Skills, memory & context | 3 | community/port; → AGENT-26 |
| 272 | skill-stocktake | audit skill quality, quick or full | Skills, memory & context | 2 |  |
| 273 | social-graph-ranker | warm-intro graph scoring | Industry domain specialist | 0 |  |
| 274 | social-publisher | post to 13 platforms via SocialClaw | Integrations & connectors | 1 | 🔑 |
| 275 | springboot-patterns | Java | Languages, frameworks & code | 0 |  |
| 276 | springboot-security | Spring Security review: authn/authz, validation, CSRF, headers, rate limits, secrets | Security & safety | 0 |  |
| 277 | springboot-tdd | test-first Spring Boot with JUnit 5, MockMvc and Testcontainers | Verification, QA & tests | 0 |  |
| 278 | springboot-verification | Spring Boot pre-merge loop: build, static analysis, integration tests, coverage, dependency scans | Verification, QA & tests | 0 |  |
| 279 | story-lifecycle | file-based epic, story, sprint loop | Thinking & planning | 0 |  |
| 280 | strategic-compact | compact context at phase boundaries; what survives compaction | Skills, memory & context | 2 | → AGENT-29 |
| 281 | swift-actor-persistence | Swift actors | Languages, frameworks & code | 0 |  |
| 282 | swift-concurrency-6-2 | Swift 6.2 | Languages, frameworks & code | 0 |  |
| 283 | swift-protocol-di-testing | Swift DI | Languages, frameworks & code | 0 |  |
| 284 | swiftui-patterns | SwiftUI | Languages, frameworks & code | 0 |  |
| 285 | taste | creative-direction vocabulary (angelcore, hyperpop): mood, colour, beat | Motion, video & media | 3 |  |
| 286 | taste-application | generate or cut against a measured style pack: LUT grade, cadence, overlays | Motion, video & media | 3 |  |
| 287 | taste-distillation | measure reference videos into a style pack (LUT, cut cadence, stills, plates) | Motion, video & media | 3 |  |
| 288 | tasteforge-video | packaged offline engine CLI: interview, validate, apply, export EDL/FCPXML, provenance | Motion, video & media | 3 |  |
| 289 | tdd-workflow | red-green-refactor, 80% coverage | Verification, QA & tests | 1 | → CODE-08 |
| 290 | team-agent-orchestration | agent squads, kanban, merge gates | Agents & orchestration | 1 |  |
| 291 | team-builder | pick up to 5 agent personas and dispatch | Agents & orchestration | 1 |  |
| 292 | terminal-opener | shell-free launch plan for a visible terminal | DevOps, tooling & infra | 0 |  |
| 293 | terminal-ops | evidence-first repo execution with exact status words | Thinking & planning | 2 | → AGENT-05, CODE-22 |
| 294 | test-collaboration | TEST-ID traceability | Verification, QA & tests | 0 |  |
| 295 | tinystruct-patterns | tinystruct Java framework | Languages, frameworks & code | 0 |  |
| 296 | token-budget-advisor | offer a 25/50/75/100% depth choice with token estimates | Skills, memory & context | 1 |  |
| 297 | token-card | usage stat card from CLI logs | ECC internals / host-specific | 0 |  |
| 298 | ui-demo | record polished UI demo videos with Playwright (WebM) | Motion, video & media | 3 |  |
| 299 | ui-to-vue | screenshots to Vue 3 components | Languages, frameworks & code | 1 |  |
| 300 | uncloud | Uncloud cluster ops | DevOps, tooling & infra | 0 |  |
| 301 | unified-memory | cross-agent memory vault and handoffs | Skills, memory & context | 1 |  |
| 302 | unified-notifications-ops | alert routing | DevOps, tooling & infra | 0 |  |
| 303 | verification-loop | 6-phase build, types, lint, tests, security grep, diff report | Verification, QA & tests | 3 | → CODE-09 |
| 304 | video-editing | footage pipeline: capture, LLM structure, FFmpeg, Remotion, AI audio and visuals, finish | Motion, video & media | 3 |  |
| 305 | videodb | VideoDB SDK: index, search and edit video and audio, RTSP | Motion, video & media | 2 | 🔑 |
| 306 | visa-doc-translate | OCR plus a bilingual PDF | Research, docs & knowledge | 1 |  |
| 307 | vite-patterns | Vite | Languages, frameworks & code | 0 |  |
| 308 | vue-patterns | Vue 3 | Languages, frameworks & code | 0 |  |
| 309 | windows-desktop-e2e | pywinauto UIA tests | Verification, QA & tests | 0 |  |
| 310 | workspace-surface-audit | inventory what this workspace or machine can do now: MCPs, plugins, env key names; gaps | Skills, memory & context | 3 |  |
| 311 | x-api | X API posting and OAuth | Integrations & connectors | 1 | 🔑 |

## 5. اقرأ أم ثبّت؟ / Read or install?
- **Read the method** (default): open `skills/<name>/SKILL.md` on GitHub (or a local clone treated as data), take the idea, write it in your own words, credit ECC. Most rel-3 methods are already distilled here (→ column).
- **Install one skill**: copy the skill folder into `.claude/skills/<name>/` (project) or `~/.claude/skills/<name>/` (personal) after reading every script it ships (SEC-10); or from a clone `./install.sh --target claude --skills <a>,<b>` (flag documented in ECC's installer; not run here).
- **Install everything**: see AGENT-34 / [ecc-harness.md](ecc-harness.md) §2 — only with the user's consent, one install method per harness.
- Skills flagged 🔑 call external services (Context7, Exa, fal.ai, VideoDB, Jira, X, Nutrient, …): check the key/connector first and tell the user about cost.
- Motion-domain skills in ECC (Remotion rules, video-editing, taste-*, manim-video, ui-demo, frontend-slides, motion-*) complement this skill's motion chapters; Remotion itself has its own company licence for commercial use.
