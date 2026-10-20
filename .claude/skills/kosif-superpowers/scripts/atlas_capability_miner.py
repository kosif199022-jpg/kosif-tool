#!/usr/bin/env python3
"""KOSIF Atlas capability miner — تعدين القدرات من مكتبة KOSIF Atlas.

Deep, deterministic, non-executing analysis of the third-party skill mirror at
https://github.com/kosif199022-jpg/kosif-atlas (14,708 permissive + 85 copyleft
skills). It never imports, runs or installs any Atlas skill. Python 3.8+ stdlib.

  python3 atlas_capability_miner.py index  --atlas /path/to/kosif-atlas --out data/atlas_capability_index.json.gz
  python3 atlas_capability_miner.py stats  --index data/atlas_capability_index.json.gz
  python3 atlas_capability_miner.py search "code review security" --index ... --top 10
  python3 atlas_capability_miner.py batches --index ... --out DIR --size 220      # agent reading batches (scratch)
  python3 atlas_capability_miner.py rea-batch --atlas ... --candidates FILE --out DIR --authorized [--limit N --timeout S]
  python3 atlas_capability_miner.py rea-receipts --runs DIR/runs.json --out proofs/atlas-rea-runs/runs.json

What each step proves — ماذا يثبت كل أمر:
  index        metadata + SKILL.md frontmatter read as inert text; a keyword taxonomy assigns every skill one
               KOSIF domain and theme (deterministic, reviewable, not a judgement of quality).
  rea-batch    REA (morluto/rea, MIT) `analyze-javascript-application` run on selected skill folders that
               contain JavaScript/TypeScript. REA parses them as inert text and returns an Evidence record with
               external package specifiers, boundaries, tasks and explicit limitations. Static ≠ executed.
  Nothing here verifies that any Atlas skill works, is safe, or is licensed as claimed.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCHEMA = "kosif.atlas.capability-index.v1"
ATLAS_REPO = "https://github.com/kosif199022-jpg/kosif-atlas"
ATLAS_RAW = "https://raw.githubusercontent.com/kosif199022-jpg/kosif-atlas/main/"
SCRIPT_EXT = (".py", ".js", ".mjs", ".cjs", ".ts", ".mts", ".tsx", ".jsx", ".sh", ".ps1", ".rb", ".go", ".rs")
JS_EXT = (".js", ".mjs", ".cjs", ".ts", ".mts", ".tsx", ".jsx")
DOMAINS = ("mind", "craft", "code", "data", "docs", "research", "build", "media", "strategy", "motion")

# --------------------------------------------------------------------------- taxonomy
# theme → (domain, Arabic label, English label, keywords). Keywords are matched as whole words (lower-case) in
# name + description + tags; a name match counts double. Order matters only for ties (earlier wins).
THEMES = collections.OrderedDict([
    ("agent-workflow", ("mind", "سير عمل الوكلاء", "Agent workflows & orchestration",
        ["agent", "agents", "subagent", "subagents", "orchestrat", "orchestration", "workflow", "workflows", "handoff",
         "checkpoint", "session", "sessions", "memory", "context", "autonomy", "autonomous", "swarm", "fleet", "dispatch",
         "multi-agent", "delegate", "delegation", "coordinator", "pipeline", "loop", "resume", "state", "worktree"])),
    ("planning-specs", ("mind", "التخطيط والمواصفات", "Planning, specs & decisions",
        ["plan", "planning", "spec", "specs", "specification", "requirements", "adr", "decision", "decisions", "rfc",
         "design doc", "prd", "roadmap", "estimate", "estimation", "retro", "retrospective", "brainstorm", "brainstorming",
         "scope", "milestone", "backlog", "task breakdown", "epic", "user story", "user stories", "grill"])),
    ("verification-review", ("mind", "المراجعة والتحقق", "Review, verification & quality gates",
        ["review", "reviewer", "verify", "verification", "audit", "auditing", "lint", "linting", "quality", "checklist",
         "validation", "validate", "eval", "evals", "evaluation", "grade", "grading", "score", "scoring", "critique",
         "check", "checks", "inspect", "compliance check", "gate", "gates"])),
    ("prompt-skill-engineering", ("craft", "هندسة البرومبت والمهارات", "Prompt, skill & plugin engineering",
        ["prompt", "prompts", "prompting", "skill creator", "skill-creator", "create skill", "skill authoring", "plugin",
         "plugins", "hook", "hooks", "slash command", "slash commands", "claude.md", "agents.md", "cursor rules", "rules",
         "system prompt", "instructions", "meta-prompt", "skill", "skills", "marketplace", "mcp server config"])),
    ("writing-content", ("craft", "الكتابة والمحتوى", "Writing & content",
        ["write", "writing", "writer", "copy", "copywriting", "blog", "article", "articles", "newsletter", "email",
         "emails", "tone", "voice", "editorial", "humanize", "humanizer", "story", "storytelling", "script",
         "screenplay", "novel", "fiction", "essay", "headline", "proofread", "editing", "summarize", "summary",
         "summaries", "rewrite", "paraphrase", "draft", "post", "posts", "linkedin", "tweet", "thread"])),
    ("localization-language", ("craft", "الترجمة واللغات", "Translation & languages",
        ["translate", "translation", "i18n", "l10n", "localization", "localisation", "chinese", "korean", "japanese",
         "arabic", "spanish", "french", "german", "portuguese", "grammar", "language learning", "multilingual",
         "bilingual", "transliterat", "dictionary", "vocabulary", "中文", "翻译", "한국어", "번역"])),
    ("documentation", ("docs", "التوثيق", "Documentation",
        ["readme", "docs", "documentation", "document", "documenting", "changelog", "api docs", "jsdoc", "docstring",
         "mkdocs", "docusaurus", "wiki", "guide", "handbook", "manual", "tutorial", "release notes", "comments",
         "annotate", "technical writing", "runbook", "onboarding doc"])),
    ("office-documents", ("docs", "ملفات المكتب", "Office documents & PDF",
        ["docx", "word", "excel", "xlsx", "spreadsheet", "spreadsheets", "pptx", "powerpoint", "presentation",
         "presentations", "slides", "slide deck", "deck", "pdf", "pdfs", "google docs", "google sheets", "google slides",
         "sheets", "forms", "form filling", "epub", "latex", "markdown export", "report generation", "invoice template"])),
    ("diagrams-visual-docs", ("docs", "المخططات", "Diagrams & visual documentation",
        ["mermaid", "diagram", "diagrams", "uml", "flowchart", "c4", "plantuml", "excalidraw", "sequence diagram",
         "architecture diagram", "erd", "mind map", "mindmap", "wireframe", "sketch", "graphviz", "visual plan"])),
    ("frontend-ui-design", ("build", "الواجهات والتصميم", "Front-end, UI & design systems",
        ["ui", "ux", "design system", "design systems", "tailwind", "css", "scss", "component", "components",
         "accessibility", "a11y", "wcag", "responsive", "figma", "shadcn", "radix", "storybook", "layout", "typography",
         "theme", "theming", "dark mode", "animation ui", "landing page", "frontend", "front-end", "html", "web design",
         "design", "designer", "icons", "patternfly", "material ui", "chakra", "bootstrap", "ui5"])),
    ("web-frameworks", ("code", "أطر الويب", "Web frameworks & languages",
        ["react", "next.js", "nextjs", "next", "vue", "nuxt", "svelte", "sveltekit", "angular", "astro", "remix",
         "typescript", "javascript", "node", "node.js", "nodejs", "bun", "deno", "express", "nestjs", "fastify", "hono",
         "python", "django", "fastapi", "flask", "rust", "golang", "go", "java", "spring", "kotlin", "swift", "swiftui",
         "flutter", "dart", "laravel", "php", "ruby", "rails", "dotnet", ".net", "c#", "csharp", "elixir", "phoenix",
         "scala", "haskell", "c++", "cpp", "zig", "ocaml", "wordpress", "drupal", "htmx", "tanstack", "zod", "trpc",
         "solid", "qwik", "lit", "web components", "vite", "webpack", "esbuild", "turbopack", "pnpm", "npm", "yarn"])),
    ("testing-tdd", ("code", "الاختبار", "Testing & TDD",
        ["test", "tests", "testing", "tdd", "jest", "pytest", "playwright test", "cypress", "vitest", "coverage",
         "e2e", "end-to-end", "unit test", "integration test", "mutation", "snapshot test", "bdd", "cucumber",
         "test-driven", "mock", "mocking", "fixture", "fixtures", "qa", "regression", "flaky", "assert", "property-based"])),
    ("debugging", ("code", "التصحيح", "Debugging & diagnosis",
        ["debug", "debugging", "debugger", "diagnose", "diagnosis", "root cause", "root-cause", "fix", "fixes", "fixing",
         "error", "errors", "troubleshoot", "troubleshooting", "bug", "bugs", "crash", "stack trace", "exception",
         "incident", "postmortem", "post-mortem", "logs", "logging", "observability", "trace", "tracing", "failure"])),
    ("refactoring-architecture", ("code", "إعادة الهيكلة والمعمارية", "Refactoring, architecture & patterns",
        ["refactor", "refactoring", "architecture", "architectural", "clean code", "solid", "design pattern",
         "design patterns", "ddd", "domain-driven", "microservice", "microservices", "monorepo", "modular", "module",
         "modules", "hexagonal", "clean architecture", "event-driven", "cqrs", "technical debt", "tech debt",
         "legacy", "migration", "migrate", "modernization", "modernize", "upgrade", "rewrite code", "simplify",
         "code quality", "smell", "smells", "dependency injection", "coupling", "cohesion", "scalability"])),
    ("git-release", ("code", "Git والإصدار", "Git, pull requests & releases",
        ["commit", "commits", "pr", "prs", "pull request", "pull requests", "branch", "branches", "merge", "rebase",
         "worktree", "worktrees", "git", "github", "gitlab", "release", "releases", "changelog", "version", "versioning",
         "semver", "tag", "tags", "issue", "issues", "code owners", "conventional commits", "squash", "cherry-pick",
         "monitor pr", "ship", "publish package", "npm publish", "goreleaser", "homebrew"])),
    ("devops-cloud", ("code", "DevOps والسحابة", "DevOps, CI/CD, cloud & infrastructure",
        ["ci", "cd", "ci/cd", "github actions", "docker", "dockerfile", "container", "containers", "kubernetes", "k8s",
         "helm", "terraform", "pulumi", "ansible", "deploy", "deployment", "deployments", "infrastructure", "iac",
         "aws", "gcp", "google cloud", "azure", "cloudflare", "vercel", "netlify", "serverless", "lambda", "nginx",
         "linux", "shell", "bash", "zsh", "systemd", "devops", "sre", "monitoring", "prometheus", "grafana",
         "datadog", "sentry", "cost", "finops", "runner", "runners", "workflow yaml", "jfrog", "artifactory", "cdn",
         "dns", "ssl", "tls", "certificate", "backup", "cron", "scheduler", "homelab", "proxmox", "vps", "ssh"])),
    ("databases", ("code", "قواعد البيانات", "Databases & storage",
        ["sql", "postgres", "postgresql", "mysql", "sqlite", "mongodb", "mongo", "redis", "clickhouse", "supabase",
         "prisma", "drizzle", "migration schema", "schema", "orm", "database", "databases", "db", "query", "queries",
         "index", "indexes", "neon", "planetscale", "firebase", "firestore", "dynamodb", "cassandra", "duckdb",
         "vector database", "pgvector", "elasticsearch", "opensearch", "kafka", "queue", "rabbitmq", "s3", "storage"])),
    ("api-backend", ("code", "واجهات API والخلفية", "APIs, backends & auth",
        ["api", "apis", "rest", "restful", "graphql", "grpc", "openapi", "swagger", "webhook", "webhooks", "endpoint",
         "endpoints", "auth", "authentication", "authorization", "oauth", "oauth2", "jwt", "sso", "saml", "oidc",
         "backend", "back-end", "server", "middleware", "rate limit", "rate limiting", "pagination", "sdk", "client",
         "websocket", "websockets", "sse", "http", "stripe", "payments", "payment", "billing", "twilio", "sendgrid"])),
    ("security", ("code", "الأمان", "Security & compliance",
        ["security", "secure", "vulnerability", "vulnerabilities", "owasp", "secret", "secrets", "pentest",
         "penetration", "cve", "threat", "threat model", "threat modeling", "encrypt", "encryption", "sast", "dast",
         "compliance", "gdpr", "soc2", "soc 2", "hipaa", "pci", "iso 27001", "privacy", "hardening", "exploit",
         "ctf", "malware", "forensics", "zero trust", "iam", "permissions", "rbac", "supply chain", "sbom",
         "dependency audit", "cors", "csrf", "xss", "injection", "data safety", "red team", "blue team", "siem"])),
    ("performance", ("code", "الأداء", "Performance & optimisation",
        ["performance", "performant", "optimize", "optimization", "optimise", "optimisation", "profiling", "profiler",
         "benchmark", "benchmarks", "benchmarking", "cache", "caching", "latency", "memory leak", "throughput",
         "core web vitals", "lighthouse", "bundle size", "lazy loading", "concurrency", "parallel", "async", "speed"])),
    ("code-understanding", ("code", "فهم الكود", "Codebase understanding & impact",
        ["codebase", "explore", "exploration", "map", "mapping", "dependency", "dependencies", "impact", "graph",
         "onboarding", "explain", "explanation", "understand", "understanding", "navigate", "navigation", "symbol",
         "symbols", "call graph", "ast", "semantic search", "code search", "grep", "repo", "repository", "overview",
         "architecture map", "knowledge graph", "ontology", "software graph", "legacy code", "reading code"])),
    ("mcp-tooling", ("code", "أدوات MCP والتكاملات", "MCP servers, tools & integrations",
        ["mcp", "model context protocol", "mcp server", "mcp servers", "tool", "tools", "tooling", "integration",
         "integrations", "cli", "command line", "command-line", "terminal", "automation", "automate", "script",
         "scripts", "scripting", "extension", "extensions", "vscode", "vs code", "ide", "jetbrains", "neovim", "vim",
         "tmux", "dotfiles", "setup", "install", "installation", "configure", "configuration", "config", "env",
         "environment", "bootstrap", "init", "initialize", "scaffold", "scaffolding", "boilerplate", "starter",
         "template", "templates", "generator", "generate", "codegen", "code generation"])),
    ("mobile", ("code", "الجوال", "Mobile development",
        ["ios", "android", "mobile", "react native", "expo", "flutter app", "xcode", "app store", "play store",
         "swift package", "jetpack compose", "compose", "kotlin multiplatform", "capacitor", "ionic", "apple tv",
         "tvos", "watchos", "visionos", "widget", "widgets", "push notification", "push notifications"])),
    ("ai-llm-engineering", ("code", "هندسة النماذج اللغوية", "LLM & AI engineering",
        ["llm", "llms", "rag", "retrieval", "embedding", "embeddings", "vector", "vectors", "fine-tune", "fine-tuning",
         "finetune", "langchain", "langgraph", "llamaindex", "openai", "anthropic", "claude api", "gemini", "ollama",
         "hugging face", "huggingface", "transformers", "agent sdk", "agents sdk", "token", "tokens", "prompt caching",
         "structured output", "function calling", "tool calling", "guardrails", "hallucination", "model", "models",
         "inference", "gpu", "cuda", "vllm", "chatbot", "chat bot", "assistant", "copilot", "ai", "generative",
         "genai", "diffusion", "whisper", "speech to text", "computer vision model", "yolo", "mlops"])),
    ("blockchain-web3", ("code", "البلوكتشين", "Blockchain & web3",
        ["solidity", "smart contract", "smart contracts", "evm", "web3", "ethereum", "solana", "blockchain", "defi",
         "nft", "wallet", "crypto", "token contract", "hardhat", "foundry", "anchor", "cosmos", "polkadot", "hedera",
         "hashgraph", "chain", "on-chain", "dapp", "dapps", "erc20", "erc721", "bitcoin", "lightning", "starknet"])),
    ("game-dev", ("build", "تطوير الألعاب", "Game development",
        ["game", "games", "gamedev", "game dev", "unity", "unreal", "godot", "phaser", "pixi", "roblox", "minecraft",
         "level design", "sprite", "sprites", "tilemap", "physics engine", "shader", "shaders", "gameplay", "npc",
         "procedural generation", "pygame", "bevy", "love2d", "rpg", "puzzle"])),
    ("hardware-embedded", ("code", "الأنظمة المدمجة", "Embedded, hardware & IoT",
        ["embedded", "firmware", "arduino", "raspberry pi", "raspberry", "iot", "esp32", "esp8266", "microcontroller",
         "stm32", "rtos", "freertos", "zephyr", "sensor", "sensors", "gpio", "i2c", "spi", "uart", "robot", "robotics",
         "ros", "ros2", "drone", "plc", "modbus", "can bus", "fpga", "verilog", "vhdl", "kicad", "pcb", "3d print",
         "3d printing", "cnc", "home assistant", "zigbee", "ble", "bluetooth"])),
    ("data-analysis", ("data", "تحليل البيانات", "Data analysis & statistics",
        ["pandas", "dataframe", "csv", "analysis", "analyze", "analyse", "analytics", "statistics", "statistical",
         "jupyter", "notebook", "notebooks", "eda", "exploratory", "polars", "numpy", "scipy", "r language",
         "regression", "forecast", "forecasting", "time series", "hypothesis", "a/b test", "ab test", "experiment",
         "metrics", "kpi", "kpis", "cohort", "funnel", "retention", "posthog", "mixpanel", "amplitude", "segment",
         "data quality", "profiling data", "survey", "quantitative", "qualitative", "insights"])),
    ("data-engineering", ("data", "هندسة البيانات", "Data engineering & pipelines",
        ["etl", "elt", "data pipeline", "data pipelines", "airflow", "dagster", "prefect", "dbt", "spark", "pyspark",
         "warehouse", "data warehouse", "bigquery", "snowflake", "databricks", "redshift", "lakehouse", "data lake",
         "iceberg", "delta lake", "parquet", "arrow", "ingestion", "cdc", "streaming", "flink", "beam", "data model",
         "data modeling", "dimensional", "star schema", "fivetran", "airbyte", "data catalog", "lineage", "data mesh"])),
    ("ml-datascience", ("data", "التعلم الآلي", "Machine learning & data science",
        ["machine learning", "ml", "model training", "training", "pytorch", "tensorflow", "keras", "sklearn",
         "scikit-learn", "scikit", "xgboost", "lightgbm", "feature engineering", "features", "classification",
         "clustering", "neural network", "neural networks", "deep learning", "dataset", "datasets", "data science",
         "kaggle", "experiment tracking", "mlflow", "weights & biases", "wandb", "hyperparameter", "evaluation metrics",
         "recommendation", "recommender", "anomaly detection", "nlp", "computer vision", "reinforcement learning"])),
    ("visualization-dashboards", ("data", "التصوير البياني ولوحات المعلومات", "Charts, dashboards & visualisation",
        ["chart", "charts", "plot", "plots", "plotting", "dashboard", "dashboards", "visualization", "visualisation",
         "visualize", "visualise", "matplotlib", "plotly", "d3", "d3.js", "recharts", "vega", "altair", "seaborn",
         "grafana dashboard", "tableau", "power bi", "looker", "metabase", "superset", "infographic", "heatmap",
         "data viz", "dataviz", "graph plotting", "bar chart", "line chart", "map visualization", "geospatial"])),
    ("web-research", ("research", "البحث على الويب", "Research, search & fact-checking",
        ["research", "researcher", "search", "searching", "fetch", "scrape", "scraping", "scraper", "crawl", "crawler",
         "crawling", "web search", "cite", "citation", "citations", "sources", "fact-check", "fact check",
         "literature", "arxiv", "paper", "papers", "academic", "scholar", "survey of", "competitive analysis",
         "market research", "due diligence", "investigate", "investigation", "intel", "intelligence", "osint",
         "news", "trend", "trends", "deep research", "wikipedia", "reddit", "hacker news", "rss", "feed",
         "web page", "website content", "extract content", "readability", "firecrawl", "jina", "exa", "tavily", "perplexity"])),
    ("knowledge-management", ("research", "إدارة المعرفة", "Notes, knowledge bases & personal memory",
        ["notes", "note", "note-taking", "obsidian", "notion", "knowledge base", "knowledge-base", "zettelkasten",
         "second brain", "pkm", "journal", "journaling", "daily note", "logseq", "roam", "bookmark", "bookmarks",
         "reading list", "highlights", "readwise", "kindle", "capture", "recall", "remember", "memories", "learnings",
         "lessons learned", "devlog", "digest", "briefing", "brief", "weekly review", "tldr", "wiki page"])),
    ("browser-automation", ("build", "أتمتة المتصفح", "Browser automation & web apps testing",
        ["browser", "browsers", "playwright", "puppeteer", "selenium", "chrome", "chromium", "chrome extension",
         "browser extension", "headless", "screenshot", "screenshots", "web automation", "form automation", "cdp",
         "devtools", "dom", "scrape with browser", "login automation", "captcha", "turnstile", "cookie", "cookies",
         "web app testing", "visual regression", "lighthouse audit", "pagespeed", "webmcp", "stagehand", "browserbase"])),
    ("productivity-integrations", ("build", "تكاملات الإنتاجية", "Productivity & SaaS integrations",
        ["slack", "gmail", "google calendar", "calendar", "jira", "linear", "notion api", "zapier", "make.com", "n8n",
         "trello", "asana", "clickup", "monday", "feishu", "lark", "dingtalk", "wechat", "zoom", "teams", "microsoft 365",
         "outlook", "google workspace", "google drive", "drive", "dropbox", "airtable", "hubspot", "salesforce",
         "zendesk", "intercom", "discord", "telegram", "whatsapp", "twitter api", "x api", "youtube api", "sheets api",
         "calendly", "todoist", "things", "reminders", "inbox", "triage", "meeting", "meetings", "transcript",
         "standup", "status update", "ticket", "tickets", "crm", "erp", "sap", "servicenow", "workday"])),
    ("app-building", ("build", "بناء التطبيقات", "App building, SaaS & product engineering",
        ["app", "apps", "application", "applications", "saas", "mvp", "prototype", "prototyping", "full-stack",
         "fullstack", "full stack", "web app", "webapp", "startup app", "ship", "launch", "build", "builder",
         "no-code", "low-code", "lowcode", "bubble", "webflow", "wix", "shopify", "ecommerce", "e-commerce", "store",
         "cart", "checkout", "subscription", "multi-tenant", "tenant", "admin panel", "dashboard app", "crud",
         "auth flow", "onboarding flow", "feature flag", "feature flags", "experimentation", "pwa", "electron",
         "tauri", "desktop app", "chrome app", "widget app", "micro-saas", "internal tool", "internal tools", "retool"])),
    ("image-design-media", ("media", "الصور والتصميم", "Images, graphics & generation",
        ["image", "images", "photo", "photos", "picture", "stable diffusion", "midjourney", "dall-e", "dalle", "flux",
         "upscale", "upscaling", "background removal", "remove background", "svg", "icon", "icon set", "logo", "logos",
         "illustration", "illustrations", "thumbnail", "thumbnails", "banner", "poster", "canvas", "pixel", "imagemagick",
         "pillow", "opencv", "image generation", "image editing", "photoshop", "gimp", "figma export", "color palette",
         "palette", "colors", "colour", "gradient", "texture", "textures", "3d model", "3d", "blender", "render",
         "rendering", "ocr", "vision", "meme", "memes", "emoji", "avatar", "avatars", "qr code", "barcode"])),
    ("audio-voice", ("media", "الصوت", "Audio, voice & music",
        ["audio", "voice", "voices", "tts", "text-to-speech", "text to speech", "speech", "transcription", "transcribe",
         "stt", "speech-to-text", "whisper", "podcast", "podcasts", "music", "song", "songs", "lyrics", "melody",
         "midi", "sound", "sounds", "sfx", "audiobook", "voiceover", "voice over", "dubbing", "elevenlabs", "suno",
         "spotify", "playlist", "dj", "mixing", "mastering", "beat", "beats", "bpm", "guitar", "chord", "chords"])),
    ("video-motion", ("motion", "الفيديو والموشن", "Video, animation & motion graphics",
        ["video", "videos", "animation", "animations", "animate", "animated", "motion", "motion graphics", "remotion",
         "lottie", "gsap", "three.js", "threejs", "webgl", "webgpu", "after effects", "ffmpeg", "subtitle", "subtitles",
         "caption", "captions", "montage", "edit video", "video editing", "reel", "reels", "shorts", "tiktok",
         "youtube video", "film", "cinematic", "storyboard", "b-roll", "keyframe", "keyframes", "easing", "timeline",
         "transition", "transitions", "particles", "scene", "scenes", "camera", "kinetic typography", "explainer",
         "screencast", "screen recording", "gif", "clip", "clips", "stream", "streaming video", "obs", "twitch"])),
    ("product-management", ("strategy", "إدارة المنتج", "Product management",
        ["product", "products", "product manager", "pm", "prd", "user research", "user interview", "persona", "personas",
         "feature prioritization", "prioritization", "prioritisation", "okr", "okrs", "north star", "discovery",
         "customer feedback", "feedback", "nps", "churn", "activation", "growth loop", "pricing page", "positioning",
         "value proposition", "jobs to be done", "jtbd", "product strategy", "launch plan", "go-to-market", "gtm",
         "competitor", "competitors", "competitive", "benchmarking products", "product analytics", "experiment plan"])),
    ("marketing-seo", ("strategy", "التسويق وSEO", "Marketing, SEO & growth",
        ["marketing", "marketer", "seo", "sem", "growth", "campaign", "campaigns", "social media", "ads", "advertising",
         "ad copy", "content strategy", "content calendar", "brand", "branding", "brand voice", "landing page copy",
         "email marketing", "drip", "funnel marketing", "conversion", "cro", "keyword", "keywords", "backlink",
         "backlinks", "google ads", "meta ads", "facebook ads", "instagram", "influencer", "pr", "press release",
         "press", "launch announcement", "product hunt", "community", "newsletter growth", "analytics ga4", "ga4",
         "google analytics", "search console", "schema markup", "sitemap", "robots.txt", "copy testing", "audience"])),
    ("business-finance", ("strategy", "الأعمال والمال", "Business, finance & legal",
        ["finance", "financial", "pricing", "invoice", "invoices", "invoicing", "accounting", "bookkeeping", "budget",
         "budgeting", "investor", "investors", "pitch", "pitch deck", "fundraising", "startup", "startups", "business",
         "business plan", "business model", "legal", "contract", "contracts", "nda", "terms", "license", "licensing",
         "tax", "taxes", "payroll", "expense", "expenses", "forecast revenue", "revenue", "valuation", "cap table",
         "equity", "stock", "stocks", "trading", "portfolio", "investing", "investment", "loan", "mortgage", "insurance",
         "procurement", "vendor", "rfp", "proposal", "quote", "quotation", "consulting", "strategy", "strategic",
         "swot", "okr planning", "board", "executive", "memo", "policy", "policies", "governance", "risk", "risk register"])),
    ("sales-customer", ("strategy", "المبيعات والعملاء", "Sales, CRM & customer success",
        ["sales", "sell", "selling", "crm", "hubspot", "salesforce", "lead", "leads", "lead generation", "outreach",
         "cold email", "prospect", "prospecting", "pipeline sales", "deal", "deals", "quota", "demo", "proposal sales",
         "customer success", "customer support", "support ticket", "help desk", "helpdesk", "faq", "faqs", "chat support",
         "onboarding customers", "account management", "upsell", "renewal", "churn prevention", "objection", "objections",
         "discovery call", "call notes", "meeting notes", "follow-up", "follow up", "linkedin outreach", "b2b", "b2c"])),
    ("hr-career", ("strategy", "الموارد البشرية والمسار المهني", "HR, hiring & careers",
        ["resume", "cv", "cover letter", "interview", "interviews", "interviewing", "hiring", "recruit", "recruiting",
         "recruitment", "job", "jobs", "job description", "career", "careers", "onboarding employee", "performance review",
         "1:1", "one-on-one", "manager", "management", "leadership", "team", "teams culture", "engineering manager",
         "promotion", "feedback employee", "salary", "compensation", "offer", "negotiation", "linkedin profile",
         "portfolio site", "personal brand", "mentoring", "mentor", "coaching", "coach", "skills assessment"])),
    ("education-learning", ("strategy", "التعليم والتعلم", "Teaching, learning & study",
        ["teach", "teaching", "teacher", "learn", "learning", "learner", "tutor", "tutoring", "course", "courses",
         "study", "studying", "lesson", "lessons", "lesson plan", "quiz", "quizzes", "flashcard", "flashcards", "anki",
         "exam", "exams", "homework", "curriculum", "syllabus", "student", "students", "classroom", "school",
         "university", "math", "mathematics", "physics", "chemistry", "biology", "history", "philosophy", "science",
         "explain like", "eli5", "socratic", "practice problems", "textbook", "certification", "exam prep"])),
    ("personal-lifestyle", ("strategy", "الحياة الشخصية", "Personal life, health & hobbies",
        ["recipe", "recipes", "cooking", "meal", "meals", "diet", "nutrition", "fitness", "workout", "exercise", "health",
         "medical", "doctor", "symptom", "symptoms", "sleep", "travel", "trip", "itinerary", "bible", "quran", "prayer",
         "meditation", "mindfulness", "habit", "habits", "journal prompts", "gratitude", "therapy", "mental health",
         "relationship", "parenting", "kids", "baby", "pet", "pets", "dog", "cat", "garden", "gardening", "home",
         "diy", "car", "shopping", "gift", "gifts", "wedding", "event planning", "party", "hobby", "hobbies", "chess",
         "poker", "fantasy", "sports", "football", "soccer", "nba", "weather", "astrology", "tarot", "horoscope"])),
    ("compliance-industry", ("strategy", "القطاعات المنظّمة", "Regulated industries & domain expertise",
        ["healthcare", "clinical", "fhir", "hl7", "patient", "pharma", "fda", "medical device", "fintech", "banking",
         "bank", "kyc", "aml", "insurance claims", "real estate", "property", "construction", "architecture building",
         "manufacturing", "supply chain", "logistics", "shipping", "retail", "hospitality", "hotel", "restaurant",
         "education sector", "government", "public sector", "nonprofit", "ngo", "energy", "oil", "solar", "agriculture",
         "legal practice", "law firm", "litigation", "patent", "trademark", "regulatory", "regulation", "regulations",
         "audit trail", "iso", "sox", "esg", "sustainability", "carbon", "climate", "aviation", "automotive", "telecom"])),
])
THEME_DOMAIN = {k: v[0] for k, v in THEMES.items()}
FALLBACK_THEME = "general-dev-workflow"
FALLBACK = ("code", "سير عمل تطوير عام", "General development workflow")

_WORD = re.compile(r"[a-z0-9][a-z0-9+#./-]*")


def tokens(text: str) -> list:
    return _WORD.findall((text or "").lower())


def _compile_keywords():
    """Return theme → list of (keyword, is_phrase)."""
    out = {}
    for theme, (_d, _a, _e, kws) in THEMES.items():
        out[theme] = [(k.lower(), " " in k) for k in kws]
    return out


KW = _compile_keywords()


def classify(name: str, description: str, tags) -> dict:
    """Score every theme for one skill; return {theme, domain, scores(top3)}. Deterministic."""
    name_l = (name or "").lower().replace("-", " ").replace("_", " ")
    desc_l = (description or "").lower()
    tag_l = " ".join(str(t) for t in (tags or [])).lower()
    name_tok = set(tokens(name_l))
    desc_tok = collections.Counter(tokens(desc_l))
    tag_tok = set(tokens(tag_l))
    joined_desc = " " + re.sub(r"[^a-z0-9+#./ -]+", " ", desc_l) + " "
    joined_name = " " + re.sub(r"[^a-z0-9+#./ -]+", " ", name_l) + " "
    scores = {}
    for theme, kws in KW.items():
        s = 0.0
        for k, phrase in kws:
            if phrase:
                if (" " + k + " ") in joined_name:
                    s += 3.0
                if (" " + k + " ") in joined_desc:
                    s += 1.5
            else:
                if k in name_tok:
                    s += 2.0
                if k in tag_tok:
                    s += 1.0
                c = desc_tok.get(k, 0)
                if c:
                    s += min(c, 3) * 0.6
        if s:
            scores[theme] = round(s, 2)
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], list(THEMES).index(kv[0])))
    if not ranked:
        return {"theme": FALLBACK_THEME, "domain": FALLBACK[0], "scores": []}
    theme = ranked[0][0]
    return {"theme": theme, "domain": THEME_DOMAIN[theme], "scores": ranked[:3]}


# --------------------------------------------------------------------------- Atlas reading
def read_frontmatter(path: Path) -> dict:
    """Minimal YAML-ish frontmatter reader (inert text; no yaml module, no execution)."""
    out = {}
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            first = fh.readline()
            if first.strip() != "---":
                return out
            key = None
            for _ in range(200):
                line = fh.readline()
                if not line or line.strip() == "---":
                    break
                m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
                if m:
                    key, val = m.group(1).lower(), m.group(2).strip()
                    if val.startswith(("'", '"')) and val.endswith(("'", '"')) and len(val) >= 2:
                        val = val[1:-1]
                    out[key] = val
                elif key and line.startswith((" ", "\t", "-")):
                    out[key] = (out.get(key, "") + " " + line.strip().lstrip("- ")).strip()
    except OSError:
        pass
    return out


def lang_of(text: str) -> str:
    if re.search(r"[؀-ۿ]", text):
        return "ar"
    if re.search(r"[一-鿿]", text):
        return "zh"
    if re.search(r"[぀-ヿ]", text):
        return "ja"
    if re.search(r"[가-힯]", text):
        return "ko"
    if re.search(r"[Ѐ-ӿ]", text):
        return "ru"
    return "en"


def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def load_atlas(atlas: Path) -> list:
    rows = []
    for fname, copyleft in (("index.json", False), ("index-copyleft.json", True)):
        p = atlas / fname
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
            raise ValueError("bad Atlas schema in " + fname)
        for r in data["skills"]:
            r = dict(r)
            r["copyleft"] = copyleft
            rows.append(r)
    if not rows:
        raise FileNotFoundError("index.json / index-copyleft.json not found under " + str(atlas))
    return rows


def build_index(atlas: Path, read_skill_md: bool = True) -> dict:
    rows = load_atlas(atlas)
    skills = []
    desc_seen = {}
    for r in rows:
        files = r.get("files") or []
        exts = collections.Counter((os.path.splitext(f)[1].lower() or "(none)") for f in files)
        fm = {}
        md_bytes = 0
        if read_skill_md:
            md = atlas / r["path"] / "SKILL.md"
            if md.is_file():
                try:
                    md_bytes = md.stat().st_size
                except OSError:
                    md_bytes = 0
                fm = read_frontmatter(md)
        desc = (r.get("description") or fm.get("description") or "").strip()
        tags = [t.strip() for t in re.split(r"[,\[\]]", fm.get("tags", "")) if t.strip()] if fm.get("tags") else []
        cls = classify(r.get("skill", ""), desc + " " + fm.get("name", ""), tags)
        dh = hashlib.sha1(re.sub(r"\s+", " ", desc.lower()).encode("utf-8")).hexdigest()[:12]
        desc_seen.setdefault(dh, []).append(r["id"])
        skills.append({
            "id": r["id"], "plugin": r.get("plugin", ""), "skill": r.get("skill", ""), "norm": norm_name(r.get("skill", "")),
            "desc": desc[:240], "desc_hash": dh, "lang": lang_of(desc),
            "license": r.get("license", ""), "copyleft": r["copyleft"], "verdict": r.get("verdict", ""),
            "risk": list(r.get("risk_flags") or []), "complete": bool(r.get("complete")),
            "path": r.get("path", ""), "source": r.get("source", ""),
            "files": len(files), "md_bytes": md_bytes,
            "py": sum(exts[e] for e in exts if e == ".py"), "js": sum(exts[e] for e in exts if e in JS_EXT),
            "sh": exts.get(".sh", 0) + exts.get(".ps1", 0), "scripts": sum(exts[e] for e in exts if e in SCRIPT_EXT),
            "tools": fm.get("allowed-tools", "")[:160], "user_invocable": fm.get("user-invocable", fm.get("user_invocable", "")),
            "theme": cls["theme"], "domain": cls["domain"], "theme2": cls["scores"][1][0] if len(cls["scores"]) > 1 else "",
        })
    for s in skills:
        s["desc_dupes"] = len(desc_seen[s["desc_hash"]]) - 1
    return {"schema": SCHEMA, "atlas": ATLAS_REPO, "raw_base": ATLAS_RAW, "count": len(skills),
            "themes": {k: {"domain": v[0], "ar": v[1], "en": v[2]} for k, v in THEMES.items()},
            "fallback_theme": {FALLBACK_THEME: {"domain": FALLBACK[0], "ar": FALLBACK[1], "en": FALLBACK[2]}},
            "note": ("Metadata and SKILL.md frontmatter read as inert text; keyword taxonomy; no Atlas code was imported, "
                     "executed or installed. Theme = a reading aid, not a verdict on quality or safety."),
            "skills": skills}


def stats(idx: dict) -> dict:
    sk = idx["skills"]
    by = lambda key: collections.OrderedDict(sorted(collections.Counter(s[key] for s in sk).items(), key=lambda kv: (-kv[1], str(kv[0]))))
    themes = collections.Counter(s["theme"] for s in sk)
    theme_rows = []
    for t, n in themes.most_common():
        meta = THEMES.get(t) or FALLBACK
        sub = [s for s in sk if s["theme"] == t]
        theme_rows.append({"theme": t, "domain": meta[0], "ar": meta[1], "en": meta[2], "skills": n,
                           "plugins": len({s["plugin"] for s in sub}), "with_scripts": sum(1 for s in sub if s["scripts"]),
                           "unique_descriptions": len({s["desc_hash"] for s in sub}),
                           "top_plugins": [p for p, _ in collections.Counter(s["plugin"] for s in sub).most_common(6)]})
    names = collections.Counter(s["norm"] for s in sk)
    return {"skills": len(sk), "plugins": len({s["plugin"] for s in sk}), "copyleft": sum(1 for s in sk if s["copyleft"]),
            "unique_descriptions": len({s["desc_hash"] for s in sk}),
            "duplicate_description_records": sum(1 for s in sk if s["desc_dupes"]),
            "unique_skill_names": len(names), "repeated_names_top": names.most_common(20),
            "with_scripts": sum(1 for s in sk if s["scripts"]), "with_python": sum(1 for s in sk if s["py"]),
            "with_javascript": sum(1 for s in sk if s["js"]), "with_shell": sum(1 for s in sk if s["sh"]),
            "mcp_server_flag": sum(1 for s in sk if "mcp_server" in s["risk"]), "hooks_flag": sum(1 for s in sk if "hooks" in s["risk"]),
            "by_domain": by("domain"), "by_lang": by("lang"), "by_license": by("license"), "by_verdict": by("verdict"),
            "fallback_theme_records": themes.get(FALLBACK_THEME, 0), "themes": theme_rows}


# Small Arabic → English bridge so a brief written in Arabic reaches the (mostly English) Atlas descriptions.
AR_ALIASES = {
    "موشن": "motion animation", "جرافيك": "graphics", "فيديو": "video", "مونتاج": "video editing", "ريلز": "reels short video",
    "كود": "code", "برمجة": "code programming", "مراجعة": "review", "أمان": "security", "امان": "security", "ثغرات": "vulnerability security",
    "بحث": "research search", "كتابة": "writing", "تسويق": "marketing", "بيانات": "data", "تحليل": "analysis", "قاعدة": "database",
    "اختبار": "test testing", "اختبارات": "tests", "تصحيح": "debug", "تصميم": "design", "واجهة": "ui", "صور": "image", "صورة": "image",
    "صوت": "audio voice", "ترجمة": "translate translation", "مستند": "document", "مستندات": "documents", "عرض": "presentation slides",
    "شرائح": "slides", "جدول": "spreadsheet excel", "وكيل": "agent", "وكلاء": "agents", "تخطيط": "plan planning", "خطة": "plan",
    "عربي": "arabic", "عربية": "arabic", "نشر": "deploy release", "إصدار": "release", "سحابة": "cloud", "خادم": "server backend",
    "تطبيق": "app application", "موقع": "website web", "جوال": "mobile", "لعبة": "game", "تعلم": "learning", "تعليم": "teaching",
    "مبيعات": "sales", "عملاء": "customer crm", "مالية": "finance", "قانوني": "legal contract", "سيرة": "resume cv", "مقابلة": "interview",
    "توثيق": "documentation", "ملاحظات": "notes", "ذاكرة": "memory", "أداء": "performance", "تحسين": "optimize", "هجرة": "migration",
    "رسم": "diagram chart drawing", "مخطط": "diagram", "لوحة": "dashboard", "ذكاء": "ai llm", "نموذج": "model llm", "برومبت": "prompt",
    "مهارة": "skill", "إضافة": "plugin", "متصفح": "browser", "أتمتة": "automation", "git": "git", "التزام": "commit",
}


def expand_query(query: str) -> list:
    words = []
    for w in re.split(r"\s+", (query or "").strip()):
        key = w.strip("ـ،,.!?؟\"'()[]{}").lstrip("وبلكف").replace("ال", "", 1) if re.search(r"[\u0600-\u06FF]", w) else w
        if re.search(r"[\u0600-\u06FF]", w):
            hit = AR_ALIASES.get(w.strip("،,.!?؟")) or AR_ALIASES.get(key) or AR_ALIASES.get("ال" + key)
            if hit:
                words.extend(hit.split())
        else:
            words.append(w)
    return tokens(" ".join(words))


def search(idx: dict, query: str, top: int = 10, domain: str = None) -> list:
    q = expand_query(query)
    if not q:
        return []
    df = collections.Counter()
    docs = []
    for s in idx["skills"]:
        t = collections.Counter(tokens(s["skill"].replace("-", " ") + " " + s["desc"] + " " + s["plugin"].replace("-", " ")))
        docs.append(t)
        for w in t:
            df[w] += 1
    n = len(docs)
    out = []
    for s, t in zip(idx["skills"], docs):
        if domain and s["domain"] != domain:
            continue
        score = 0.0
        for w in q:
            if t.get(w):
                score += (1 + min(t[w], 3) * 0.3) * (1.0 + (n / (1 + df[w])) ** 0.35)
            if w in s["norm"].split("-"):
                score += 2.0
        if score:
            out.append((round(score, 2), s))
    out.sort(key=lambda x: (-x[0], str(x[1]["id"])))
    return [{"score": sc, "id": s["id"], "plugin": s["plugin"], "skill": s["skill"], "theme": s["theme"], "domain": s["domain"],
             "license": s["license"], "verdict": s["verdict"], "path": s["path"], "online_url": ATLAS_REPO + "/tree/main/" + s["path"],
             "desc": s["desc"][:200]} for sc, s in out[:top]]


def write_batches(idx: dict, out: Path, size: int = 220) -> dict:
    """Write theme-coherent reading batches (one JSON per batch) for the LLM extraction phase.
    Records sharing a description hash are collapsed to one representative plus a `mirrors` count."""
    out.mkdir(parents=True, exist_ok=True)
    groups = collections.OrderedDict()
    for s in sorted(idx["skills"], key=lambda s: (s["theme"], s["plugin"], s["id"])):
        groups.setdefault(s["theme"], []).append(s)
    manifest = []
    n = 0
    for theme, rows in groups.items():
        seen = {}
        uniq = []
        for s in rows:
            if s["desc_hash"] in seen:
                seen[s["desc_hash"]]["mirrors"] += 1
                seen[s["desc_hash"]]["mirror_ids"].append(s["id"])
                continue
            rec = {"id": s["id"], "plugin": s["plugin"], "skill": s["skill"], "lang": s["lang"], "license": s["license"],
                   "verdict": s["verdict"], "risk": s["risk"], "py": s["py"], "js": s["js"], "sh": s["sh"], "files": s["files"],
                   "tools": s["tools"], "path": s["path"], "desc": s["desc"][:320], "mirrors": 0, "mirror_ids": []}
            seen[s["desc_hash"]] = rec
            uniq.append(rec)
        meta = THEMES.get(theme) or FALLBACK
        for i in range(0, len(uniq), size):
            n += 1
            chunk = uniq[i:i + size]
            bid = "b%03d-%s-%d" % (n, theme, i // size + 1)
            payload = {"batch_id": bid, "theme": theme, "domain": meta[0], "theme_ar": meta[1], "theme_en": meta[2],
                       "records": len(chunk), "mirrored_records": sum(c["mirrors"] for c in chunk), "skills": chunk}
            (out / (bid + ".json")).write_text(json.dumps(payload, ensure_ascii=False, indent=0), encoding="utf-8")
            manifest.append({"batch_id": bid, "file": str(out / (bid + ".json")), "theme": theme, "domain": meta[0],
                             "theme_en": meta[2], "records": len(chunk), "mirrored": payload["mirrored_records"]})
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"batches": len(manifest), "themes": len(groups), "manifest": str(out / "manifest.json")}


# --------------------------------------------------------------------------- REA batch (opt-in)
def rea_launcher():
    env = os.environ.get("REA_BIN")
    found = env if env and Path(env).is_file() else shutil.which("rea")
    if not found:
        return None
    p = Path(found)
    if p.suffix.lower() in (".cmd", ".bat", ".ps1") or os.name == "nt":
        node = shutil.which("node")
        for mjs in (p.parent / "node_modules" / "rea-agents" / "scripts" / "rea.mjs",
                    p.parent.parent / "rea-agents" / "scripts" / "rea.mjs"):
            if mjs.is_file() and node:
                return [node, str(mjs)]
        return None
    return [str(p)]


def summarize_evidence(ev: dict) -> dict:
    """Compact, path-free facts from one REA JavaScriptApplication Evidence record."""
    nr = ev.get("normalized_result") or {}
    g = nr.get("graph") or {}
    sg = nr.get("semantic_graph") or {}
    kinds = collections.Counter(n.get("kind") for n in g.get("nodes", []))
    external = collections.Counter()
    unresolved = 0
    inline_html = 0
    vendor = collections.Counter()
    for n in g.get("nodes", []):
        for o in n.get("observations", []):
            p = o.get("properties") or {}
            spec = p.get("declared_specifier")
            if spec:
                st = p.get("resolution_status")
                if st == "external":
                    bare = spec.split("/")[0] if not spec.startswith("@") else "/".join(spec.split("/")[:2])
                    external[bare] += 1
                elif st in ("not-found", "unavailable"):
                    unresolved += 1
            if p.get("inline_script_count"):
                inline_html += int(p.get("inline_script_count") or 0)
            for v in p.get("vendor_markers") or []:
                vendor[v] += 1
    rel = collections.Counter(e.get("relation") for e in g.get("edges", []))
    skinds = collections.Counter(n.get("kind") for n in sg.get("nodes", []))
    bounds = collections.Counter()
    for n in sg.get("nodes", []):
        if n.get("kind") == "boundary":
            lab = (n.get("label") or n.get("name") or "")
            props = n.get("properties") or {}
            bounds[str(props.get("boundary_kind") or props.get("kind") or lab)[:60]] += 1
    st = nr.get("statistics") or {}
    return {"evidence_id": ev.get("evidence_id"), "root_sha256": nr.get("root_artifact_sha256"),
            "provider": (ev.get("provider") or {}).get("id"), "predicate": ev.get("predicate_type"),
            "statistics": {k: st.get(k) for k in ("relevant_files", "parsed_javascript_files", "skipped_javascript_files",
                                                   "text_bytes_read", "visited_ast_nodes", "findings", "parse_failures")},
            "graph_nodes": sum(kinds.values()), "graph_edges": sum(rel.values()), "node_kinds": dict(kinds),
            "edge_relations": dict(rel.most_common(12)), "semantic_node_kinds": dict(skinds.most_common(16)),
            "external_packages": dict(external.most_common(40)), "unresolved_local_imports": unresolved,
            "inline_html_scripts_not_analyzed": inline_html, "vendor_markers": dict(vendor),
            "boundaries": dict(bounds.most_common(12)), "unknowns": len(sg.get("unknowns") or []),
            "electron_summary": nr.get("summary"), "limitations": list(nr.get("limitations") or [])[:12],
            "integrity_contradictions": len(nr.get("integrity_contradictions") or [])}


def rea_batch(atlas: Path, candidates: Path, out: Path, authorized: bool, limit: int, timeout: int, keep: bool) -> dict:
    if not authorized:
        return {"status": "authorization_required", "analysis_executed": False}
    launcher = rea_launcher()
    if not launcher:
        return {"status": "rea_runtime_unavailable", "analysis_executed": False}
    cands = json.loads(candidates.read_text(encoding="utf-8"))
    out.mkdir(parents=True, exist_ok=True)
    runs_path = out / "runs.json"
    runs = json.loads(runs_path.read_text(encoding="utf-8")) if runs_path.exists() else []
    done = {r["id"] for r in runs}
    version = "unknown"
    try:
        v = subprocess.run(launcher + ["--version"], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=20, check=False)
        version = (v.stdout or v.stderr).strip().splitlines()[-1][:20] if (v.stdout or v.stderr).strip() else "unknown"
    except (OSError, subprocess.TimeoutExpired):
        pass
    n = 0
    for c in cands:
        if n >= limit:
            break
        if c["id"] in done:
            continue
        target = (atlas / c["path"]).resolve()
        if not target.is_dir() or atlas.resolve() not in target.parents:
            runs.append({"id": c["id"], "status": "target_missing_or_outside_atlas"})
            continue
        n += 1
        ev_file = out / ("ev-%s.json" % c["id"])
        t0 = time.time()
        rec = {"id": c["id"], "plugin": c["plugin"], "skill": c["skill"], "path": c["path"], "license": c.get("license"),
               "verdict": c.get("verdict"), "command": "rea analyze-javascript-application <atlas>/%s --json" % c["path"],
               "rea_version": version, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0))}
        try:
            with ev_file.open("w", encoding="utf-8") as fh:
                proc = subprocess.run(launcher + ["analyze-javascript-application", str(target), "--json"], stdout=fh,
                                      stderr=subprocess.PIPE, text=True, stdin=subprocess.DEVNULL, timeout=timeout, check=False)
            rec["exit"] = proc.returncode
            rec["stderr_tail"] = (proc.stderr or "")[-400:].replace(str(atlas), "<atlas>")
        except subprocess.TimeoutExpired:
            rec["exit"] = None
            rec["status"] = "timeout_%ss" % timeout
        except OSError as exc:
            rec["exit"] = None
            rec["status"] = "launch_error: " + str(exc)[:200]
        rec["seconds"] = round(time.time() - t0, 1)
        if rec.get("exit") == 0 and ev_file.exists():
            try:
                ev = json.loads(ev_file.read_text(encoding="utf-8"))
                rec["status"] = "evidence"
                rec["evidence_sha256"] = hashlib.sha256(ev_file.read_bytes()).hexdigest()
                rec["evidence_bytes"] = ev_file.stat().st_size
                rec["summary"] = summarize_evidence(ev)
            except (ValueError, OSError) as exc:
                rec["status"] = "unparseable_output: " + str(exc)[:120]
        elif "status" not in rec:
            rec["status"] = "rea_refused_or_failed"
        if not keep and ev_file.exists():
            ev_file.unlink()   # full Evidence carries local paths and is large; the receipt keeps the facts
        runs.append(rec)
        runs_path.write_text(json.dumps(runs, ensure_ascii=False, indent=1), encoding="utf-8")
        print("%s %s/%s exit=%s %ss %s" % (rec["status"], c["plugin"], c["skill"], rec.get("exit"), rec["seconds"],
                                          ("pkgs=%d" % len(rec["summary"]["external_packages"])) if rec.get("summary") else ""), flush=True)
    return {"status": "done", "executed": n, "runs_file": str(runs_path), "total_runs": len(runs)}


def rea_receipts(runs: Path) -> dict:
    data = json.loads(runs.read_text(encoding="utf-8"))
    ok = [r for r in data if r.get("status") == "evidence"]
    pkgs = collections.Counter()
    bounds = collections.Counter()
    for r in ok:
        for p, c in (r["summary"].get("external_packages") or {}).items():
            pkgs[p] += 1
        for b, c in (r["summary"].get("boundaries") or {}).items():
            bounds[b] += c
    return {"schema": "kosif.atlas.rea-receipts.v1", "tool": "morluto/rea (MIT) analyze-javascript-application",
            "rea_version": next((r.get("rea_version") for r in data if r.get("rea_version")), "unknown"),
            "runs": len(data), "evidence_records": len(ok),
            "refused_or_failed": [{"id": r["id"], "status": r.get("status"), "exit": r.get("exit")} for r in data if r.get("status") != "evidence"],
            "total_parsed_javascript_files": sum((r["summary"]["statistics"].get("parsed_javascript_files") or 0) for r in ok),
            "total_graph_nodes": sum(r["summary"]["graph_nodes"] for r in ok),
            "total_semantic_unknowns": sum(r["summary"]["unknowns"] for r in ok),
            "packages_by_skill_count": pkgs.most_common(60), "boundary_kinds": bounds.most_common(20),
            "note": ("Static parse of inert text by REA; nothing executed; 'external_packages' are declared import specifiers, "
                     "not proof the dependency is installed or used at runtime. Full Evidence JSON (local paths) is not committed."),
            "receipts": [{k: r.get(k) for k in ("id", "plugin", "skill", "path", "license", "verdict", "command", "rea_version",
                                                "started", "exit", "seconds", "evidence_sha256", "evidence_bytes")}
                         | {"evidence_id": r["summary"]["evidence_id"], "root_sha256": r["summary"]["root_sha256"],
                            "parsed_javascript_files": r["summary"]["statistics"].get("parsed_javascript_files"),
                            "graph_nodes": r["summary"]["graph_nodes"], "graph_edges": r["summary"]["graph_edges"],
                            "external_packages": r["summary"]["external_packages"], "boundaries": r["summary"]["boundaries"],
                            "unresolved_local_imports": r["summary"]["unresolved_local_imports"],
                            "inline_html_scripts_not_analyzed": r["summary"]["inline_html_scripts_not_analyzed"],
                            "semantic_unknowns": r["summary"]["unknowns"], "limitations": r["summary"]["limitations"][:6]}
                         for r in ok]}


def load_index(p: Path) -> dict:
    """Read the index from .json or .json.gz (the committed copy is gzip-compressed to stay small)."""
    if p.suffix == ".gz" or (not p.exists() and p.with_name(p.name + ".gz").exists()):
        if not p.exists():
            p = p.with_name(p.name + ".gz")
        with gzip.open(p, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads(p.read_text(encoding="utf-8"))


def save_index(idx: dict, p: Path) -> None:
    text = json.dumps(idx, ensure_ascii=False, separators=(",", ":"))
    if p.suffix == ".gz":
        with gzip.open(p, "wt", encoding="utf-8", compresslevel=9) as fh:
            fh.write(text)
    else:
        p.write_text(text, encoding="utf-8")


# --------------------------------------------------------------------------- CLI
def _new_file(p: Path, force: bool = False) -> Path:
    if p.exists() and not force:
        raise SystemExit("refusing to overwrite %s (use --force)" % p)
    if p.is_symlink() or not p.parent.is_dir():
        raise SystemExit("unsafe output path %s" % p)
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("index"); a.add_argument("--atlas", type=Path, required=True); a.add_argument("--out", type=Path, required=True)
    a.add_argument("--force", action="store_true"); a.add_argument("--no-skill-md", action="store_true")
    b = sub.add_parser("stats"); b.add_argument("--index", type=Path, required=True); b.add_argument("--json", action="store_true")
    c = sub.add_parser("search"); c.add_argument("query"); c.add_argument("--index", type=Path, required=True)
    c.add_argument("--top", type=int, default=10); c.add_argument("--domain", choices=DOMAINS); c.add_argument("--json", action="store_true")
    d = sub.add_parser("batches"); d.add_argument("--index", type=Path, required=True); d.add_argument("--out", type=Path, required=True)
    d.add_argument("--size", type=int, default=220)
    e = sub.add_parser("rea-batch"); e.add_argument("--atlas", type=Path, required=True); e.add_argument("--candidates", type=Path, required=True)
    e.add_argument("--out", type=Path, required=True); e.add_argument("--authorized", action="store_true")
    e.add_argument("--limit", type=int, default=20); e.add_argument("--timeout", type=int, default=300); e.add_argument("--keep-evidence", action="store_true")
    f = sub.add_parser("rea-receipts"); f.add_argument("--runs", type=Path, required=True); f.add_argument("--out", type=Path)
    f.add_argument("--force", action="store_true")
    g = sub.add_parser("themes")
    args = ap.parse_args(argv)
    if args.cmd == "index":
        idx = build_index(args.atlas, read_skill_md=not args.no_skill_md)
        p = _new_file(args.out, args.force)
        save_index(idx, p)
        st = stats(idx)
        print("indexed %d skills from %d plugins → %s (%s domains, %d themes, %d fallback)" % (
            st["skills"], st["plugins"], p, len(st["by_domain"]), len(st["themes"]), st["fallback_theme_records"]))
        return 0
    if args.cmd == "stats":
        st = stats(load_index(args.index))
        if args.json:
            print(json.dumps(st, ensure_ascii=False, indent=1)); return 0
        print("skills %d · plugins %d · copyleft %d · unique descriptions %d (%d mirrored records) · unique names %d" % (
            st["skills"], st["plugins"], st["copyleft"], st["unique_descriptions"], st["duplicate_description_records"], st["unique_skill_names"]))
        print("with scripts %d (py %d · js %d · sh %d) · mcp_server flag %d · hooks flag %d" % (
            st["with_scripts"], st["with_python"], st["with_javascript"], st["with_shell"], st["mcp_server_flag"], st["hooks_flag"]))
        print("domains: " + " · ".join("%s %d" % kv for kv in st["by_domain"].items()))
        print("langs: " + " · ".join("%s %d" % kv for kv in st["by_lang"].items()))
        for t in st["themes"]:
            print("%6d  %-26s %-9s plugins %4d scripts %4d uniq %5d  %s" % (t["skills"], t["theme"], t["domain"], t["plugins"], t["with_scripts"], t["unique_descriptions"], t["en"]))
        return 0
    if args.cmd == "search":
        res = search(load_index(args.index), args.query, args.top, args.domain)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=1)); return 0
        for r in res:
            print("%6.2f  #%-5d %-28s %-30s %-24s %s" % (r["score"], r["id"], r["plugin"][:28], r["skill"][:30], r["theme"], r["license"]))
            print("        " + r["desc"][:150])
        return 0
    if args.cmd == "batches":
        print(json.dumps(write_batches(load_index(args.index), args.out, args.size), ensure_ascii=False)); return 0
    if args.cmd == "rea-batch":
        print(json.dumps(rea_batch(args.atlas, args.candidates, args.out, args.authorized, args.limit, args.timeout, args.keep_evidence), ensure_ascii=False)); return 0
    if args.cmd == "rea-receipts":
        rec = rea_receipts(args.runs)
        text = json.dumps(rec, ensure_ascii=False, indent=1)
        if args.out:
            _new_file(args.out, args.force).write_text(text + "\n", encoding="utf-8")
            print("wrote %s: %d evidence records of %d runs" % (args.out, rec["evidence_records"], rec["runs"]))
        else:
            print(text)
        return 0
    if args.cmd == "themes":
        for t, (dom, ar, en, kws) in THEMES.items():
            print("%-26s %-9s %s — %s (%d keywords)" % (t, dom, ar, en, len(kws)))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
