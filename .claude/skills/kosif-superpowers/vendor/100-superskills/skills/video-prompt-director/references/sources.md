# مصادر «مخرج برومبتات الفيديو» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## runway-core-workflow-a (1900-runway-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/runway-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1900-runway-pack/6659-runway-core-workflow-a
- الوصف: Design a Runway text-to-video job from the current model-discriminated API contract and preserve its asynchronous evidence. Use when implementing direct model generation. Trigger with: "Runway text to video", "choose Runway video model", "submit Runway generation".

```markdown
# Model-Grounded Text-to-Video Workflow

## Overview

Treat model choice as an API-schema decision, not a marketing label. Runway request bodies are discriminated by `model`; valid ratios, durations, prompt limits, optional controls, price, and even required fields can differ between models.

## Prerequisites

- A product requirement covering quality, latency, duration, ratio, and budget
- Current Runway models, API reference, and pricing pages
- Durable task tracking and owned output storage

## Instructions

### Step 1: Define the output contract

Record modality, intended use, dimensions, duration, audio need, quality threshold, deadline, moderation policy, and maximum credits. Separate hard constraints from preferences.

### Step 2: Choose direct model or router

Use a direct model when reproducibility requires a reviewed identifier. Use a saved Model Router when policy should optimize cost, latency, or quality within approved allow and deny lists; use its dry run before billable work.

### Step 3: Read the exact variant

Inspect the current `text_to_video` schema for the chosen model. For example, `gen4.5` currently supports text input, but this skill does not transplant its ratio or duration fields to another model.

### Step 4: Freeze and submit

Persist the model or router config, normalized request, documentation fingerprint, and approval before create. Store the returned task ID immediately.

### Step 5: Observe without duplication

Use the SDK wait helper or bounded polling. Treat `THROTTLED` as queued and distinguish queue time from execution time. Recover from client interruption by retrieving the saved task.

### Step 6: Validate and preserve

On success, download output, verify media type, duration, dimensions, and checksum, then run the product quality review. On failure, apply the HTTP or task-failure policy rather than silently changing models.

## Authentication

All model, router, task, and usage calls use the server-side Runway API secret. Direct HTTP also sends the reviewed `X-Runway-Version`; temporary output URLs remain confidential until copied to controlled storage.

## Tool Discipline

Use Read and Grep to inspect application configuration, provider documentation, lockfiles, fixtures, schemas, tests, and redacted operational evidence before proposing a change. Use Write or Edit only for an approved implementation, configuration, test, runbook, or redacted receipt. Do not create, cancel, delete, retry, deploy, rotate, revoke, publish, or otherwise mutate production Runway resources without explicit operator approval.

## Output

- Reviewed model-or-router decision with current schema and price evidence
- Durable request fingerprint, task timeline, and terminal-state receipt
```

## runway-core-workflow-b (1900-runway-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/runway-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1900-runway-pack/6660-runway-core-workflow-b
- الوصف: Prepare, submit, and preserve Runway image-to-video or video-to-video work with validated media provenance. Use when a generation begins from an asset. Trigger with: "Runway image to video", "Runway video transformation", "upload media to Runway".

```markdown
# Runway Input-Media Transformation Workflow

## Overview

Input media is part of the generation contract and the security boundary. Choose public HTTPS, data URI, or an ephemeral upload deliberately; verify rights, content, size, format, crop, expiry, and model compatibility before spending credits.

## Prerequisites

- An approved source asset with provenance and usage rights
- Current input constraints and exact model variant schema
- Temporary-upload and final-output retention policies

## Instructions

### Step 1: Classify the transformation

Choose image-to-video, video-to-video, upscale, or another documented endpoint from the desired input and output—not from a copied sample. Record the expected preservation and allowed creative change.

### Step 2: Validate the asset

Check MIME type, extension, byte size, dimensions, duration, codec, orientation, and moderation policy. Review auto-crop consequences when the source aspect ratio differs from the requested output.

### Step 3: Choose transport

Use a reachable HTTPS URL for already hosted media, a data URI only for small inputs, or an ephemeral upload for local files. Never embed large video as base64 merely because a sample does.

### Step 4: Create an ephemeral upload safely

For local media, use the SDK helper or the documented two-step upload. A `runway://` URI lasts 24 hours, supports reuse within that period, and must not be treated as permanent storage.

### Step 5: Submit and track

Validate the chosen model's input fields, persist the request fingerprint and task ID, then use bounded polling. Do not retry a failed upload URL; start a new upload as documented.

### Step 6: Validate transformed output

Copy successful output to owned storage and compare duration, dimensions, codec, visible crop, continuity, brand constraints, and safety. Preserve both source and output checksums in the receipt.

## Authentication

The Runway API secret remains server-side for uploads, generation, and task reads. Source URLs and temporary Runway/output URLs may grant access to media and must be redacted and expired according to policy.

## Tool Discipline

Use Read and Grep to inspect application configuration, provider documentation, lockfiles, fixtures, schemas, tests, and redacted operational evidence before proposing a change. Use Write or Edit only for an approved implementation, configuration, test, runbook, or redacted receipt. Do not create, cancel, delete, retry, deploy, rotate, revoke, publish, or otherwise mutate production Runway resources without explicit operator approval.

## Output

- Input provenance, validation, crop, and transport decision
- Upload and generation identifiers with state evidence
- Owned output with media, safety, and transformation review
```

## klingai-image-to-video (1874-klingai-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/klingai-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1874-klingai-pack/6075-klingai-image-to-video
- الوصف: Animate static images into video using Kling AI. Use when converting

```markdown
# Kling AI Image-to-Video

## Overview

Animate static images using the `/v1/videos/image2video` endpoint. Supports motion prompts, camera control, dynamic masks (motion brush), static masks, and tail images for start-to-end transitions.

**Endpoint:** `POST https://api.klingai.com/v1/videos/image2video`

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model_name` | string | Yes | `kling-v1-5`, `kling-v2-1`, `kling-v2-master`, etc. |
| `image` | string | Yes | URL of the source image (JPG, PNG, WebP) |
| `prompt` | string | No | Motion description for the animation |
| `negative_prompt` | string | No | What to exclude |
| `duration` | string | Yes | `"5"` or `"10"` seconds |
| `aspect_ratio` | string | No | `"16:9"` default |
| `mode` | string | No | `"standard"` or `"professional"` |
| `cfg_scale` | float | No | Prompt adherence (0.0-1.0) |
| `image_tail` | string | No | End-frame image URL (mutually exclusive with masks/camera) |
| `camera_control` | object | No | Camera movement (mutually exclusive with masks/image_tail) |
| `static_mask` | string | No | Mask image URL for fixed regions |
| `dynamic_masks` | array | No | Motion brush trajectories |
| `callback_url` | string | No | Webhook for completion |

## Basic Image-to-Video

```python
import jwt, time, os, requests

BASE = "https://api.klingai.com/v1"

def get_headers():
    ak, sk = os.environ["KLING_ACCESS_KEY"], os.environ["KLING_SECRET_KEY"]
    token = jwt.encode(
        {"iss": ak, "exp": int(time.time()) + 1800, "nbf": int(time.time()) - 5},
        sk, algorithm="HS256", headers={"alg": "HS256", "typ": "JWT"}
    )
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Animate a landscape photo
response = requests.post(f"{BASE}/videos/image2video", headers=get_headers(), json={
    "model_name": "kling-v2-1",
    "image": "https://example.com/landscape.jpg",
    "prompt": "Clouds slowly drifting across the sky, gentle wind rustling through trees",
    "negative_prompt": "static, frozen, blurry",
    "duration": "5",
    "mode": "standard",
})

task_id = response.json()["data"]["task_id"]

# Poll for result
while True:
    time.sleep(15)
    result = requests.get(
        f"{BASE}/videos/image2video/{task_id}", headers=get_headers()
    ).json()
    if result["data"]["task_status"] == "succeed":
        print(f"Video: {result['data']['task_result']['videos'][0]['url']}")
        break
    elif result["data"]["task_status"] == "failed":
        raise RuntimeError(result["data"]["task_status_msg"])
```

## Start-to-End Transition (image_tail)

Use `image_tail` to specify both the first and last frame. Kling interpolates the motion between them.

```python
```

## klingai-text-to-video (1874-klingai-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/klingai-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1874-klingai-pack/6089-klingai-text-to-video
- الوصف: Generate videos from text prompts with Kling AI. Use when creating videos

```markdown
# Kling AI Text-to-Video

## Overview

Generate videos from text prompts using the `/v1/videos/text2video` endpoint. Supports models v1 through v2.6, standard/professional modes, camera control, negative prompts, and native audio (v2.6+).

**Endpoint:** `POST https://api.klingai.com/v1/videos/text2video`

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model_name` | string | Yes | Model version (see model catalog) |
| `prompt` | string | Yes | Video description, max 2500 chars |
| `negative_prompt` | string | No | What to exclude from generation |
| `duration` | string | Yes | `"5"` or `"10"` seconds |
| `aspect_ratio` | string | No | `"16:9"` (default), `"9:16"`, `"1:1"`, etc. |
| `mode` | string | No | `"standard"` (default) or `"professional"` |
| `cfg_scale` | float | No | Prompt adherence (0.0-1.0, default 0.5) |
| `camera_control` | object | No | Camera movement config |
| `callback_url` | string | No | Webhook URL for completion notification |

## Complete Example — Python

```python
import jwt, time, os, requests

BASE = "https://api.klingai.com/v1"

def get_headers():
    ak, sk = os.environ["KLING_ACCESS_KEY"], os.environ["KLING_SECRET_KEY"]
    token = jwt.encode(
        {"iss": ak, "exp": int(time.time()) + 1800, "nbf": int(time.time()) - 5},
        sk, algorithm="HS256", headers={"alg": "HS256", "typ": "JWT"}
    )
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Create text-to-video task
response = requests.post(f"{BASE}/videos/text2video", headers=get_headers(), json={
    "model_name": "kling-v2-6",
    "prompt": "Aerial drone shot of a coral reef at golden hour, "
              "tropical fish swimming through crystal clear water, "
              "sun rays penetrating the surface, cinematic 4K",
    "negative_prompt": "blurry, low quality, distorted, watermark",
    "duration": "5",
    "aspect_ratio": "16:9",
    "mode": "professional",
    "cfg_scale": 0.5,
})

task = response.json()
task_id = task["data"]["task_id"]

# Poll for completion
while True:
    time.sleep(15)
    result = requests.get(
        f"{BASE}/videos/text2video/{task_id}", headers=get_headers()
    ).json()

    status = result["data"]["task_status"]
    if status == "succeed":
        video = result["data"]["task_result"]["videos"][0]
        print(f"Video URL: {video['url']}")
        print(f"Duration: {video['duration']}s")
        break
    elif status == "failed":
        raise RuntimeError(result["data"]["task_status_msg"])
    # else: submitted/processing — keep polling
```

## With Camera Control

```python
# Camera movement types: pan, tilt, zoom, roll
response = requests.post(f"{BASE}/videos/text2video", headers=get_headers(), json={
```

## video (1446-marketing-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/frankdays/bigslick/tree/c03d1dbe25c239301a3c5af3b0618353f3940720/upstream/marketingskills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1446-marketing-skills/3531-video
- الوصف: When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks. Also use when the user mentions 'video production,' 'AI video,' 'Remotion,' 'Hyperframes,' 'HeyGen,' 'Synthesia,' 'Veo,' 'Sora,' 'Runway,' 'Kling,' 'Seedance,' 'Hailuo,' 'MiniMax,' 'Pika,' 'Hunyuan,' 'Wan,' 'video generation,' 'AI avatar,' 'talking head video,' 'programmatic video,' 'video 

```markdown
# Video

You are an expert video producer who helps create marketing videos using AI generation models, AI avatars, and programmatic video frameworks. Your goal is to help users produce professional video content efficiently — from product demos and explainers to social clips and ads.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Video Goal
- What type of video? (Product demo, explainer, testimonial, social clip, ad, tutorial)
- What's the target platform? (YouTube, TikTok/Reels/Shorts, website, ads, sales deck)
- What's the desired length?

### 2. Production Approach
- Do you need a human presenter? (AI avatar vs. voiceover vs. screen recording)
- Do you have existing footage or assets? (Screenshots, logos, product UI)
- Do you need generated footage? (AI-generated scenes, B-roll)
- Is this a one-off or a template for repeated use?

### 3. Technical Context
- What's your tech stack? (Node.js, Python, etc.)
- Do you have API keys for any video tools?
- Budget constraints? (Some tools charge per minute of video)

---

## Choosing Your Approach

Pick the right tool for the job:

| Approach | Best For | Tools | When to Use |
|----------|----------|-------|-------------|
| **Programmatic** | Templated, data-driven, batch video | Remotion, Hyperframes | Product updates, personalized videos, recurring content |
| **AI Generation** | Original footage from text/image prompts | Veo 3, Sora 2, Runway, Kling, Seedance | B-roll, hero shots, creative visuals you can't film |
| **AI Avatars** | Talking-head presenter without filming | HeyGen, Synthesia | Explainers, tutorials, multilingual content |
| **Editing/Repurposing** | Cutting long-form into short clips | Descript, Opus Clip, CapCut | Podcast/webinar → social clips |

---

## Programmatic Video

Build videos with code. Best for repeatable, templated, or data-driven video at scale.

### Hyperframes (HTML/CSS — recommended for agents)

Open-source, Apache 2.0, from HeyGen. Uses plain HTML/CSS/JS — no framework DSL to learn. LLM-native: AI models generate better HTML than React components.

```bash
npm install hyperframes
```

**Key concept:** Each frame is an HTML document. Compose frames into a timeline, render to MP4.

```typescript
import { render } from "hyperframes";

await render({
  frames: [
    { html: "<h1>Welcome to Acme</h1>", duration: 3 },
    { html: "<h2>Here's what we built</h2>", duration: 3 },
    { html: "<p>Try it free →</p>", duration: 2 },
```

## cfo-advisor (138-c-level-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/c-level-advisor
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/138-c-level-skills/412-cfo-advisor
- الوصف: Financial leadership for startups and scaling companies. Financial modeling, unit economics, fundraising strategy, cash management, and board financial packages. Use when building financial models, analyzing unit economics, planning fundraising, managing cash runway, preparing board materials, or when user mentions CFO, burn rate, runway, fundraising, unit economics, LTV, CAC, term sheets, or fina

```markdown
# CFO Advisor

Strategic financial frameworks for startup CFOs and finance leaders. Numbers-driven, decisions-focused.

This is **not** a financial analyst skill. This is strategic: models that drive decisions, fundraises that don't kill the company, board packages that earn trust.

## Keywords
CFO, chief financial officer, burn rate, runway, unit economics, LTV, CAC, fundraising, Series A, Series B, term sheet, cap table, dilution, financial model, cash flow, board financials, FP&A, SaaS metrics, ARR, MRR, net dollar retention, gross margin, scenario planning, cash management, treasury, working capital, burn multiple, rule of 40

## Quick Start

```bash
# Burn rate & runway scenarios (base/bull/bear)
python scripts/burn_rate_calculator.py

# Per-cohort LTV, per-channel CAC, payback periods
python scripts/unit_economics_analyzer.py

# Dilution modeling, cap table projections, round scenarios
python scripts/fundraising_model.py
```

## Key Questions (ask these first)

- **What's your burn multiple?** (Net burn ÷ Net new ARR. > 2x is a problem.)
- **If fundraising takes 6 months instead of 3, do you survive?** (If not, you're already behind.)
- **Show me unit economics per cohort, not blended.** (Blended hides deterioration.)
- **What's your NDR?** (> 100% means you grow without signing a single new customer.)
- **What are your decision triggers?** (At what runway do you start cutting? Define now, not in a crisis.)

## Core Responsibilities

| Area | What It Covers | Reference |
|------|---------------|-----------|
| **Financial Modeling** | Bottoms-up P&L, three-statement model, headcount cost model | `references/financial_planning.md` |
| **Unit Economics** | LTV by cohort, CAC by channel, payback periods | `references/financial_planning.md` |
| **Burn & Runway** | Gross/net burn, burn multiple, scenario planning, decision triggers | `references/cash_management.md` |
| **Fundraising** | Timing, valuation, dilution, term sheets, data room | `references/fundraising_playbook.md` |
| **Board Financials** | What boards want, board pack structure, BvA | `references/financial_planning.md` |
| **Cash Management** | Treasury, AR/AP optimization, runway extension tactics | `references/cash_management.md` |
| **Budget Process** | Driver-based budgeting, allocation frameworks | `references/financial_planning.md` |

## CFO Metrics Dashboard

| Category | Metric | Target | Frequency |
|----------|--------|--------|-----------|
| **Efficiency** | Burn Multiple | < 1.5x | Monthly |
| **Efficiency** | Rule of 40 | > 40 | Quarterly |
| **Efficiency** | Revenue per FTE | Track trend | Quarterly |
| **Revenue** | ARR growth (YoY) | > 2x at Series A/B | Monthly |
| **Revenue** | Net Dollar Retention | > 110% | Monthly |
| **Revenue** | Gross Margin | > 65% | Monthly |
```
