# مصادر «أتمتة إكسل المتقدمة (Power Query وLAMBDA وDAX)» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## aws-http-server-on-lambda-web-adapter (3270-aws-http-server-on-lambda-web-adapter)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/aws-http-server-on-lambda-web-adapter
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3270-aws-http-server-on-lambda-web-adapter/13781-aws-http-server-on-lambda-web-adapter
- الوصف: Host a small, unmodified HTTP server (Node/Python/any) as a scale-to-zero AWS Lambda — including LLM-proxy demo apps — using the AWS Lambda Web Adapter, and work around the two gotchas that bite. Use when: (1) you want an on-demand, ~$0-idle public URL for a plain web server without rewriting it into a Lambda handler; (2) a Lambda **Function URL** returns `403 AccessDeniedException` ("Forbidden") 

```markdown
# HTTP server on Lambda via the Web Adapter (with the two gotchas)

**Canonical source:** distilled from a live deployment of a zero-dependency Node
HTTP server (static PWA + one POST endpoint proxying an LLM call) onto AWS Lambda,
fronted first by a Function URL (failed) then API Gateway (worked). Genericized;
substitute your own `<account-id>`, `<region>`, `<fn-name>`.

## 1. Run an unchanged HTTP server on Lambda (no handler rewrite)

The **AWS Lambda Web Adapter (LWA)** is a Lambda extension that translates Lambda
invokes (Function URL, API Gateway v1/v2, ALB) into plain HTTP requests to your
server on a local port. Your app needs **no code change** and still runs as a
normal container anywhere.

Dockerfile — add one COPY line; keep your normal base image and CMD:

```dockerfile
FROM node:20-slim
# The adapter as an extension; harmless when run as a plain container.
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /app
COPY . .
# LWA forwards to your app on port 8080 by default; make your server listen there.
ENV PORT=8080
EXPOSE 8080
CMD ["node", "server.js"]
```

Deploy as a **container image** Lambda:

```bash
ECR=<account-id>.dkr.ecr.<region>.amazonaws.com
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin $ECR
docker buildx build --platform linux/amd64 -t $ECR/<repo>:latest --push .   # amd64 for x86_64 Lambda
aws lambda create-function --function-name <fn-name> --package-type Image \
  --code ImageUri=$ECR/<repo>:latest --role <exec-role-arn> \
  --timeout 120 --memory-size 512 \
  --environment file://env.json          # keep secrets out of the CLI/ps
```

Notes:
- Any base image works (does NOT need an AWS Lambda base image); the adapter
  bridges the Runtime API.
- New IAM role -> `create-function` may fail for ~10-30s on role propagation;
  retry with a short sleep.

## 2. Front door: Function URL vs API Gateway

Prefer a **Lambda Function URL** — no request-duration cap (up to the 15-min
Lambda max), supports response streaming, built-in HTTPS, no extra service.

But it can fail closed: a Function URL with `AuthType=NONE` + a correct
`lambda:InvokeFunctionUrl` resource policy for `Principal:"*"` can STILL return
`403 AccessDeniedException` ("Forbidden") **with no SCP and no RCP present, even in
the Organizations management account**. Cause is an unresolved account-level quirk;
propagation retries do not fix it. Don't rabbit-hole — **pivot to API Gateway
HTTP API**, which uses `execute-api` (a different action) and is unaffected:

```bash
# Quick-create: makes the AWS_PROXY integration, $default route, default stage,
# AND the lambda invoke permission in one call.
aws apigatewayv2 create-api --name <fn-name> --protocol-type HTTP \
```

## lambda (625-lambda-builder)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/lambda-builder
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/625-lambda-builder/1654-lambda
- الوصف: Generate AWS Lambda functions

```markdown
# lambda-builder

Generate AWS Lambda functions.

## Tools

This skill uses the following tools:

- **Read** — Read files from the filesystem
- **Write** — Write files to the filesystem
- **Edit** — Make targeted edits to existing files
- **Bash** — Execute shell commands
- **Grep** — Search file contents with regex
- **Glob** — Find files by pattern matching
```

## excel-pivot-wizard (1633-excel-analyst-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/business-tools/excel-analyst-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1633-excel-analyst-pro/4606-excel-pivot-wizard
- الوصف: Create advanced Excel pivot tables with calculated fields and slicers.

```markdown
# Excel Pivot Wizard

## Overview

Creates advanced pivot tables with calculated fields, slicers, and dynamic dashboards for data analysis and reporting.

## Prerequisites

- Excel or compatible spreadsheet software
- Tabular data with headers
- Clear understanding of analysis dimensions and measures

## Instructions

1. Verify source data is in tabular format with headers
2. Create pivot table from data range
3. Configure rows, columns, values, and filters
4. Add calculated fields for custom metrics
5. Insert slicers for interactive filtering
6. Format and style for presentation

## Output

- Configured pivot table with appropriate aggregations
- Calculated fields for derived metrics
- Interactive slicers for filtering
- Dashboard-ready formatting

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Field not found | Changed source data | Refresh data connection |
| Calculated field error | Invalid formula | Check field names match exactly |
| Slicer not updating | Disconnected report | Reconnect slicer to pivot |

## Examples

**Example: Sales Dashboard**
Request: "Create a pivot summarizing sales by region and product"
Result: Pivot with region rows, product columns, revenue values, and date slicer

**Example: Financial Analysis**
Request: "Build a pivot showing monthly trends by cost center"
Result: Time-series pivot with calculated YoY growth fields

## Resources

- [Microsoft Pivot Table Guide](https://support.microsoft.com/)
- `${CLAUDE_SKILL_DIR}/references/pivot-formulas.md` for calculated field syntax
```

## aws-lambda-durable-functions (370-aws-serverless)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/awslabs/agent-plugins/tree/097fe8ad56d8a1d5e2c81d7880adf145553cf244/plugins/aws-serverless
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/370-aws-serverless/1368-aws-lambda-durable-functions
- الوصف: Build resilient, long-running, multi-step applications with AWS Lambda durable functions with automatic state persistence, retry logic, and orchestration for long-running executions. Covers the critical replay model, step operations, wait/callback patterns, error handling with saga pattern, testing with LocalDurableTestRunner. Triggers on phrases like: lambda durable functions, workflow orchestrat

```markdown
# AWS Lambda durable functions

Build resilient multi-step applications and AI workflows that can execute for up to 1 year while maintaining reliable progress despite interruptions.

## Onboarding

### Step 1: Validate Prerequisites

Before using AWS Lambda durable functions, verify:

1. **AWS CLI** is installed (2.33.22 or higher) and configured:

   ```bash
   aws --version
   aws sts get-caller-identity
   ```

2. **Runtime environment** is ready:
   - For TypeScript/JavaScript: Node.js 22+ (`node --version`)
   - For Python: Python 3.11+ (`python --version`. Note that currently only Lambda runtime environments 3.13+ come with the Durable Execution SDK pre-installed. 3.11 is the min supported Python version by the Durable SDK itself, however, you could use OCI to bring your own container image with your own Python runtime + Durable SDK.)

3. **Deployment capability** exists (one of):
   - AWS SAM CLI (`sam --version`) 1.153.1 or higher
   - AWS CDK (`cdk --version`) v2.237.1 or higher
   - Direct Lambda deployment access

### Step 2: Select language and IaC framework

### Language Selection

Default: TypeScript

Override syntax:

- "use Python" → Generate Python code
- "use JavaScript" → Generate JavaScript code

When not specified, ALWAYS use TypeScript

### IaC framework selection

Default: CDK

Override syntax:

- "use CloudFormation" → Generate YAML templates
- "use SAM" → Generate YAML templates

When not specified, ALWAYS use CDK

### Error Scenarios

#### Unsupported Language

- List detected language
- State: "Durable Execution SDK is not yet available for [framework]"
- Suggest supported languages as alternatives

#### Unsupported IaC Framework

- List detected framework
- State: "[framework] might not support Lambda durable functions yet"
- Suggest supported frameworks as alternatives

### Serverless MCP Server Unavailable

- Inform user: "AWS Serverless MCP not responding"
- Ask: "Proceed without MCP support?"
- DO NOT continue without user confirmation

### Step 3: Install SDK

**For TypeScript/JavaScript:**

```bash
npm install @aws/durable-execution-sdk-js
npm install --save-dev @aws/durable-execution-sdk-js-testing
```

**For Python:**

```bash
pip install aws-durable-execution-sdk-python
pip install aws-durable-execution-sdk-python-testing
```

## When to Load Reference Files

Load the appropriate reference file based on what the user is working on:

- **Getting started**, **basic setup**, **example**, **ESLint**, or **Jest setup** -> see [getting-started.md](references/getting-started.md)
- **Understanding replay model**, **determinism**, or **non-deterministic errors** -> see [replay-model-rules.md](references/replay-model-rules.md)
```

## aws-lambda-managed-instances (370-aws-serverless)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/awslabs/agent-plugins/tree/097fe8ad56d8a1d5e2c81d7880adf145553cf244/plugins/aws-serverless
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/370-aws-serverless/1369-aws-lambda-managed-instances
- الوصف: Evaluate, configure, and migrate workloads to AWS Lambda Managed Instances (LMI). Triggers on: Lambda Managed Instances, LMI, capacity provider, multi-concurrency Lambda, dedicated instance Lambda, EC2-backed Lambda, cold start elimination, Graviton Lambda, instance type for Lambda, scheduled scaling for LMI, Lambda cost optimization with Reserved Instances or Savings Plans. Also trigger when user

```markdown
# AWS Lambda Managed Instances (LMI)

Run Lambda functions on current-generation EC2 instances in your account while AWS manages provisioning, patching, scaling, routing, and load balancing. Combines Lambda's developer experience with EC2's pricing and hardware options.

For standard Lambda development, see [aws-lambda skill](../aws-lambda/). For SAM/CDK deployment, see [aws-serverless-deployment skill](../aws-serverless-deployment/).

## When to Load Reference Files

- **Cost comparison**, **pricing analysis**, **Lambda vs LMI cost**, **Savings Plans**, or **Reserved Instances** -> see [references/cost-comparison.md](references/cost-comparison.md)
- **Instance types**, **memory sizing**, **vCPU ratios**, **scaling tuning**, **scheduled scaling**, or **capacity provider config** -> see [references/configuration-guide.md](references/configuration-guide.md)
- **Thread safety**, **concurrency model**, **code review checklist**, **Powertools compatibility**, or **multi-concurrency readiness** -> see [references/thread-safety.md](references/thread-safety.md)
- **Before/after code examples**, **runtime-specific migration** (Node.js, Python, Java, .NET), or **connection pooling** -> see [references/migration-patterns.md](references/migration-patterns.md)
- **IAM roles**, **VPC setup**, **CLI commands**, **SAM template**, **CDK example**, or **scheduled scaling setup (EventBridge Scheduler)** -> see [references/infrastructure-setup.md](references/infrastructure-setup.md) and [scripts/setup-lmi.sh](scripts/setup-lmi.sh)
- **Errors**, **throttling**, **debugging**, **stuck deployments**, **tuning configuration**, or **adjusting after deployment** -> see [references/troubleshooting.md](references/troubleshooting.md)

## Quick Decision: Is LMI Right for This Workload?

| Signal         | LMI is a strong fit                                                                     | Standard Lambda is better                              |
| -------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Traffic        | Steady, predictable, 50M+ req/mo                                                        | Bursty, unpredictable, long idle                       |
| Cost           | Duration-heavy spend at scale                                                           | Low or sporadic invocations                            |
| Cold starts    | Unacceptable (LMI eliminates for provisioned capacity; scale-out may have brief delays) | Tolerable or mitigated by SnapStart                    |
| Compute        | Latest CPUs, specific families, high network bandwidth                                  | Standard Lambda memory/CPU sufficient                  |
```

## lean-startup (3432-product-innovation)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wondelai/skills/tree/c172996495bed0fcd26896a9416b2093fd7073f0/plugins/product-innovation
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3432-product-innovation/14092-lean-startup
- الوصف: Design MVPs, validated learning experiments, and pivot-or-persevere decisions using Build-Measure-Learn. Use when the user mentions "MVP scope", "validated learning", "pivot or persevere", "vanity metrics", "test assumptions", "innovation accounting", "build-measure-learn", "minimum viable experiment", "should we pivot", "test a business idea cheaply", or "build the smallest version first". Also t

```markdown
# Lean Startup Methodology

A systematic approach to building startups and launching new products that shortens development cycles and rapidly discovers whether a business model is viable.

## Core Principle

**Entrepreneurship is a form of management.** Success doesn't require a perfect plan or brilliant insight—it requires a systematic process for testing assumptions, learning from customers, and iterating rapidly. Most startups fail not because they couldn't build what they planned, but because they built the wrong thing: treat every plan as a set of hypotheses to falsify, and spend effort to eliminate waste and accelerate **validated learning**, not to execute a fixed roadmap.

## Scoring

**Goal: 10/10.** Score a plan, experiment, or metric set by the five Quick Diagnostic rows—**1 point each** when the answer is yes, **2 points** when it is also backed by evidence on the Validation Ladder (Level 3+):

- **9-10:** every leap-of-faith assumption named and ranked by risk, the riskiest tested by a real MVP, actionable metrics defined, and explicit pivot criteria set before building.
- **5-6:** a hypothesis and some MVP exist, but metrics are vanity or pivot criteria are undefined—decisions can't be made from the data.
- **≤3:** waterfall thinking—building the full product first, asking customers what they want, or scaling before product/market fit.

State the current score and the lowest-scoring diagnostic row to fix next.

## The Build-Measure-Learn Loop

The fundamental cycle: **IDEAS → BUILD (product) → MEASURE (data) → LEARN (knowledge) → back to IDEAS.**

**Critical insight:** Plan the loop backward:
1. **What do we want to learn?** (hypothesis to test)
2. **How will we know if we learned it?** (metrics)
3. **What's the minimum we can build?** (MVP)

**Goal:** Minimize total time through the loop.

See [references/build-measure-learn.md](references/build-measure-learn.md) when planning an experiment—reverse-planning sequence, an experiment-design template, per-product-type loop examples, and the build/vanity-metric loop traps.

## Validated Learning

Learning what customers really want through experiments on real behavior—not feature requests, surveys, or focus groups (people mispredict their own behavior). Measure what customers *do*, not what they *say*, and run experiments that could falsify your assumptions. Vanity wins (downloads, signups without engagement) are not learning.

**The Validation Ladder:**

| Level | Evidence | Strength |
|-------|----------|----------|
| 1 | "I think customers want this" | Weakest (opinion) |
| 2 | "Customers said they want this" | Weak (stated preference) |
| 3 | "Customers signed up for early access" | Medium (low commitment) |
| 4 | "Customers paid a deposit" | Strong (real commitment) |
```
