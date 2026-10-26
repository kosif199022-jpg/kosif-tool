# مصادر «تصميم الواجهات الخلفية وAPI» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## building-graphql-server (1626-graphql-server-builder)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/api-development/graphql-server-builder
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1626-graphql-server-builder/4597-building-graphql-server
- الوصف: Build production-ready GraphQL servers with schema design, resolvers,

```markdown
# Building GraphQL Server

## Overview

Build production-ready GraphQL servers with SDL-first or code-first schema design, efficient resolver implementations with DataLoader batching, real-time subscriptions via WebSocket, and field-level authorization. Support Apollo Server, Yoga, Mercurius, and Strawberry across Node.js and Python runtimes.

## Prerequisites

- Node.js 18+ with Apollo Server/Yoga/Mercurius, or Python 3.10+ with Strawberry/Ariadne
- Database with ORM (Prisma, TypeORM, SQLAlchemy) for resolver data sources
- Redis for subscription pub/sub and DataLoader caching (production deployments)
- GraphQL client for testing: GraphiQL, Apollo Studio, or Insomnia
- `graphql-codegen` for TypeScript type generation from schema (recommended)

## Instructions

1. Examine existing data models, database schemas, and business requirements using Read and Glob to determine the entity graph and relationship structure.
2. Design the GraphQL schema with type definitions, including `Query`, `Mutation`, and `Subscription` root types, input types for mutations, and connection types for paginated lists.
3. Implement resolvers for each field, using DataLoader to batch and deduplicate database queries for nested relationships (N+1 query prevention).
4. Add input validation on mutation arguments using custom scalars (DateTime, Email, URL) and directive-based validation (`@constraint(minLength: 1, maxLength: 255)`).
5. Implement field-level authorization using schema directives (`@auth(requires: ADMIN)`) or resolver middleware that checks user roles from the GraphQL context.
6. Configure query complexity analysis and depth limiting to prevent abusive queries (maximum depth of 7, maximum complexity score of 1000).
7. Set up real-time subscriptions using `graphql-ws` protocol over WebSocket with Redis pub/sub for multi-instance message distribution.
8. Generate TypeScript types from the schema using `graphql-codegen` to ensure type safety between schema definitions and resolver implementations.
9. Write integration tests using `executeOperation` for query/mutation testing and WebSocket client tests for subscription verification.

See `${CLAUDE_SKILL_DIR}/references/implementation.md` for the full implementation guide.

## Output

- `${CLAUDE_SKILL_DIR}/src/schema/` - GraphQL SDL type definitions organized by domain
- `${CLAUDE_SKILL_DIR}/src/resolvers/` - Resolver implementations per type with DataLoader integration
- `${CLAUDE_SKILL_DIR}/src/dataloaders/` - DataLoader factories for batched database queries
- `${CLAUDE_SKILL_DIR}/src/directives/` - Custom schema directives (auth, validation, caching)
- `${CLAUDE_SKILL_DIR}/src/scalars/` - Custom scalar type definitions (DateTime, JSON, Email)
```

## backend-dev (2105-backend-dev-kit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/ksarelto/dev-ai-plugins/tree/aa2a58815f38800a8ab6d98f80ca032aa1c2fa18/app-dev-kit/backend-dev-kit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2105-backend-dev-kit/7477-backend-dev
- الوصف: Builds one Express API resource increment from a spec-dev-kit spec (and optional html-generator-kit prototype) — scoped UPSTREAM_SPEC import of entities and api-surface, hub-and-spoke (scaffold-service if needed, Zod, Drizzle, repository, service, router, OpenAPI, Vitest), quality gates, and a mandatory human review. Writes kit-result.json. Never opens a PR. Use when implementing a backend resourc

```markdown
# Backend Dev

**Command**: `/backend-dev [resource-slug or request]`
**Pipeline driver**: `backend-orchestrator`
**Blackboard**: `.spec/backend/<slug>.md`

This skill runs in the **main conversation**. It owns every `AskUserQuestion` call. The
orchestrator is a subagent and must never ask the user.

---

## Resolve KIT_DIR

1. `{this SKILL.md directory}/../..` (or `${CLAUDE_SKILL_DIR}/../..`).
2. `app-dev-kit/backend-dev-kit` relative to the workspace root.
3. `.spec/backend-dev-kit`.

Scripts live at `{KIT_DIR}/skills/backend-dev/…`.

---

## Companion files

| Path | When |
|------|------|
| `references/pipeline-flow.md` | before starting |
| `references/upstream-contract.md` | Station 0 |
| `references/backend-spec-format.md` | blackboard schema |
| `references/packets.md` | packet types |
| `references/context-budget.md` | hub + workers |
| `references/quality-gates.md` | Station 5 |
| `references/human-review-protocol.md` | Station 12 |
| `scripts/import-upstream.mjs` | Station 0 |
| `scripts/new-backend.sh` | Station 0 |
| `scripts/validate-backend-spec.mjs` | Station 0.5 |
| `scripts/run-gates.sh` | Station 5 |
| `scripts/write-kit-result.mjs` | Station 12 / abort |

---

## Prerequisites

| Check | If missing |
|-------|-----------|
| Git repo | STOP |
| `create-app.ts` **or** ability to invoke `scaffold-service` | STOP if human declines scaffold |
| Clean working tree | Ask commit / stash |

---

## Arguments

Structured fields from `orchestrate-app` or the human: `UPSTREAM_SPEC`, `TASK_ID`, `SLICE_REF`,
`ENTITY_REFS`, `API_REFS`, `STORY_REFS`, `AC_REFS`, `PROTOTYPE_REF`,
`SLUG_HINT`, `RESULT_OUT`. `REQUEST` is one line when those are set.

```
/backend-dev
/backend-dev profile
/backend-dev "profiles CRUD with requireAuth"
```

---

## Steps

Read `references/pipeline-flow.md`.

### Station 0 — Intake

1. Resume if `.spec/backend/{slug}.md` matches the argument. If its `status` is `done`, report complete and stop unless the matching work-plan task is `pending` with `blocked-reason: spec changed`. Import then sets `status: approved`; skip Station 0.5 and continue at station 1.
2. Else derive slug from `SLUG_HINT` (never the app `metadata.slug`).
   If `UPSTREAM_SPEC` is empty, read `.spec/app/current.json` and set `UPSTREAM_SPEC` from
   `spec_path` and `PROTOTYPE_REF` from `prototype_ref`. Do not glob for a spec.
3. `bash {KIT_DIR}/skills/backend-dev/scripts/new-backend.sh {slug}`
4. If `UPSTREAM_SPEC` is set:

   ```bash
   node {KIT_DIR}/skills/backend-dev/scripts/import-upstream.mjs \
     --spec {UPSTREAM_SPEC} --out .spec/backend/{slug}.md \
     --task-id {TASK_ID} --slice-ref {SLICE_REF or omit} \
     --entity-refs {ENTITY_REFS} --api-refs {API_REFS} \
     --story-refs {STORY_REFS} --ac-refs {AC_REFS} \
```

## api-plugin-openapi-hygiene (2336-microsoft-365-copilot)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/microsoft-365-copilot
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2336-microsoft-365-copilot/8970-api-plugin-openapi-hygiene
- الوصف: Make a REST API safe and correct to expose as a Microsoft 365 Copilot API plugin — lay out the four files (app manifest + plugin manifest + OpenAPI + adaptive cards), verify the plugin-manifest↔OpenAPI `operationId` mapping both ways, respect the OpenAPI-for-Copilot subset, write model-readable operation descriptions, budget responses to ~66% of the 25-item/~4096-token wall, and wire Entra OAuth2/

```markdown
# API-plugin OpenAPI hygiene

Playbook for `api-plugin-engineer`. Source of truth: [`../../knowledge/api-plugins-and-auth-2026.md`](../../knowledge/api-plugins-and-auth-2026.md). Template: [`../../templates/api-plugin-pair.md`](../../templates/api-plugin-pair.md).

## 1. The four files
App manifest + **plugin manifest** + **OpenAPI spec** + adaptive-card templates. Source-control all four.

## 2. operationId mapping (verify both ways)
Each plugin-manifest function/runtime → a concrete OpenAPI `operationId`. Check: every function maps to an existing `operationId`, and every exposed `operationId` is intentional. A mismatch = Copilot can't invoke (or invokes the wrong op).

## 3. Model-readable descriptions
Copilot decides *whether* and *how* to call from the operation `description` + parameter descriptions. Write them for the model, not for humans only. Vague descriptions = wrong/no invocation.

## 4. Respect the Copilot OpenAPI subset
Supported verbs/parameters/response shapes only `[verify-at-build]`. Bounded payloads.

## 5. Budget the response
Keep responses within **~66%** of the 25-item / ~4,096-token plugin-response budget. Trim fields; paginate; shape adaptive cards for citation.

## 6. Auth
Entra OAuth2 (incl. OBO) or API-key, declared as a connection. **No secrets in the files.** App registration → `azure-cloud/entra-identity-engineer`; the **verdict** → `ravenclaude-core/security-reviewer` (mandatory). Surface the **GCC-High not-supported caveat** `[verify-at-build]`.

## 7. Licensing impact
Copilot seats + any downstream API cost/quota.

## Anti-patterns
- operationId mismatch; full-OpenAPI features Copilot doesn't support; vague descriptions; unbounded responses; secrets in the manifest; ignoring the GCC-High caveat.
```

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

## fastapi-app (1065-app-starter)

- الترخيص: **MIT**  ·  الأصل: https://github.com/ccplugins/awesome-claude-code-plugins/tree/5bd4f168edf7c18a8303cbfde20708ff62aabc4d/plugins/app-starter
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1065-app-starter/2350-fastapi-app
- الوصف: Bootstrap a new FastAPI backend with async SQLAlchemy 2.0, asyncpg, Alembic, Pydantic v2, and no deprecated APIs. Use when the user wants to start, scaffold, or set up a new FastAPI service, a Python REST API, an async backend, or asks to "create a new fastapi app" or "new python backend". Handles JWT auth, layered app structure, Docker + Postgres, and Vercel or container deploy.

```markdown
# fastapi-app

Bootstrap a new FastAPI backend the way this owner builds them: async SQLAlchemy
2.0 with asyncpg, Alembic migrations, Pydantic v2 settings, a layered structure
(routers, services, models, schemas), JWT auth, and the house git and CI
workflow. Deployable to a container or Vercel.

First read the shared rules (they override anything you remember):
`../shared/house-rules.md`, `../shared/no-ai-attribution.md`,
`../shared/git-and-ci.md`, `../shared/docs-and-context.md`,
`../shared/hardening.md`, and (for public repos) `../shared/open-source-docs.md`.

## Step 0. Get the brief, then ask the variant questions (hard stop)

This is a hard stop. Do not run any scaffolding command until the user has
answered.

First, get the project brief: one paragraph on what the service does, its main
resources and endpoints, who calls it, and any hard constraints. If the user has
not given one, ask for it. The brief drives naming, the domain modules, and the
data model.

Then ask the variant questions. If a choice has multiple options, ask; do not
assume. Ask in one batch, then proceed.

1. Repo visibility: private, open-source, or private-plus-open-source.
2. Auth: JWT (python-jose or PyJWT), OAuth (Google), API-key, or none yet.
3. Database: Postgres via async SQLAlchemy + asyncpg (default), or none yet.
4. Dependency tooling: `uv` (default, fast) or `pip` + `requirements.txt`.
5. Admin UI: SQLAdmin, or none.
6. Deploy target: Docker container (default) or Vercel serverless.

If the user already answered some, do not re-ask.

## Step 1. Verify environment and current versions

- Check Python (`python3 --version`, want a current supported 3.x).
- Run `scripts/check-latest.sh` for current stable versions from PyPI. Pin those,
  not versions from memory (`../shared/house-rules.md` rule 2).
- Pull current FastAPI, SQLAlchemy 2.0, and Pydantic v2 docs via Context7 before
  writing code (`../shared/docs-and-context.md`). SQLAlchemy 2.0 async and
  Pydantic v2 both broke v1 patterns; do not write v1-era code from memory.

## Step 2. Scaffold the project

Create a virtualenv and the layout from `references/structure.md`. With `uv`:

```
uv init <name> && cd <name>
uv add fastapi "uvicorn[standard]" "sqlalchemy[asyncio]" asyncpg alembic \
       pydantic-settings python-jose[cryptography] httpx python-multipart
uv add --dev ruff pytest pytest-asyncio
```

With pip, install the same set and freeze into `requirements.txt`. Let the tool
resolve current versions; do not force numbers you remember.

## Step 3. Apply structure and conventions

- Layered app structure, async DB session, dependency-injected DB, settings, JWT
  auth: `references/structure.md`.
- Best practices, scalable domain-modular architecture, and nothing hardcoded:
  `references/best-practices.md`.
```

## backend/api-development (1369-boss)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/echoVic/boss-skill
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1369-boss/3147-boss/skills/backend/api-development
- الوصف: 后端API开发方法论，包括RESTful/GraphQL设计、请求验证、错误处理和安全实现

```markdown
# 后端 API 开发方法论

## API 契约管理

### 契约来源

实现 API 前，**必须**阅读 `architecture.md` §5（API 设计），获取：
- API 规范（RESTful/GraphQL）
- 接口列表（方法、路径、描述、认证要求）
- 请求/响应格式约定
- 错误码规范

### 契约遵守原则

1. **严格实现**：API 端点的方法、路径、参数必须与 architecture.md §5 一致
2. **响应格式**：遵循统一的成功/错误响应结构
3. **偏差记录**：如需偏离契约，必须在输出报告中标注原因
4. **类型导出**：将请求/响应类型导出到共享文件，供前端引用

## RESTful API 设计

### 资源命名规范

| 操作 | HTTP 方法 | 路径 | 说明 |
|------|-----------|------|------|
| 列表 | GET | `/api/users` | 获取用户列表 |
| 详情 | GET | `/api/users/:id` | 获取单个用户 |
| 创建 | POST | `/api/users` | 创建新用户 |
| 更新 | PUT/PATCH | `/api/users/:id` | 更新用户 |
| 删除 | DELETE | `/api/users/:id` | 删除用户 |

### 统一响应格式

**成功响应**：
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

**错误响应**：
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

### 分页规范

**请求参数**：
```
GET /api/users?page=1&pageSize=20&sortBy=createdAt&order=desc
```

**响应格式**：
```json
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```

## 请求验证

### 输入验证层级

1. **路由层**：验证路径参数和查询参数
2. **中间件层**：验证请求体格式和必填字段
3. **Service 层**：验证业务规则

### 验证示例

```typescript
// 使用验证库（如 Zod、Joi、class-validator）
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
});

// 在路由处理器中验证
app.post('/api/users', async (req, res) => {
  try {
    const validatedData = CreateUserSchema.parse(req.body);
    const user = await userService.create(validatedData);
    res.json({ success: true, data: user });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input data',
          details: error.errors,
        },
      });
    }
  }
});
```

### 常见验证规则

- **必填字段**：确保关键字段存在
- **类型检查**：字符串、数字、布尔值、日期
- **格式验证**：邮箱、URL、手机号、UUID
- **范围限制**：最小/最大长度、数值范围
- **业务规则**：唯一性、外键存在性

## 错误处理

### 错误分类

| 错误类型 | HTTP 状态码 | 错误码 | 说明 |
|----------|-------------|--------|------|
| 验证错误 | 400 | VALIDATION_ERROR | 输入数据不合法 |
| 认证错误 | 401 | UNAUTHORIZED | 未登录或 Token 无效 |
| 权限错误 | 403 | FORBIDDEN | 无权限访问资源 |
| 资源不存在 | 404 | NOT_FOUND | 请求的资源不存在 |
| 冲突错误 | 409 | CONFLICT | 资源冲突（如重复创建） |
| 服务器错误 | 500 | INTERNAL_ERROR | 服务器内部错误 |

### 统一错误处理中间件

```typescript
// errorHandler.ts
export function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  console.error(err);

  if (err instanceof ValidationError) {
    return res.status(400).json({
```
