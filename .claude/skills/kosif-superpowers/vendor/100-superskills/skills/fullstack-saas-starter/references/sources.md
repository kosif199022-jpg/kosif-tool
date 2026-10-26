# مصادر «منصة SaaS كاملة» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## supabase-auth-storage-realtime-core (1908-supabase-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/supabase-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1908-supabase-pack/6845-supabase-auth-storage-realtime-core
- الوصف: Implement Supabase Auth (signUp, signIn, OAuth, session management),

```markdown
# Supabase Auth + Storage + Realtime Core

## Overview

Implement the three pillars that turn a Supabase database into a full application backend: user authentication (email/password, OAuth, magic links, session lifecycle), file storage (uploads, downloads, signed URLs, bucket-level RLS policies), and real-time subscriptions (Postgres change events, client-to-client broadcast, presence tracking). Every operation integrates with Row-Level Security through `auth.uid()`.

Each pillar below carries a lean skeleton in this file; the full, copy-paste walkthroughs live in `references/` so this file stays scannable.

## Prerequisites

- Supabase project created at [supabase.com/dashboard](https://supabase.com/dashboard)
- `@supabase/supabase-js` v2 installed (`npm install @supabase/supabase-js`)
- `SUPABASE_URL` and `SUPABASE_ANON_KEY` available from project Settings > API
- For Python: `pip install supabase` (wraps `postgrest-py`, `gotrue-py`, `storage3`, `realtime-py`)

## Instructions

Read the file (Read), edit or create the client and route/component code (Write, Edit), and grep the project (Grep) to reuse an existing Supabase client before creating a new one. Use `Bash(npm:*)` to install the SDK and `Bash(supabase:*)` to run migrations/policies.

### Step 1: Auth — registration, login, OAuth

Initialize the client once, then wire the flows your app needs. The skeleton:

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_ANON_KEY!)

// Email/password
await supabase.auth.signUp({ email, password })
await supabase.auth.signInWithPassword({ email, password })

// OAuth — redirect the user to data.url
const { data } = await supabase.auth.signInWithOAuth({ provider: 'google' })

// React to session changes (SIGNED_IN / SIGNED_OUT / TOKEN_REFRESHED)
supabase.auth.onAuthStateChange((event, session) => { /* update UI */ })
```

Full auth walkthrough — OAuth callback, magic link, session lifecycle, password reset: [references/auth.md](references/auth.md). Python: [references/python-examples.md](references/python-examples.md).

### Step 2: Storage — upload, download, secure with bucket policies

Public buckets serve via CDN URLs; private buckets require signed URLs. The skeleton:

```typescript
// Upload to the signed-in user's own folder (RLS enforces ownership)
await supabase.storage.from('avatars').upload(`${userId}/avatar.png`, file, { upsert: true })

// Public URL (public bucket) vs. time-limited signed URL (private bucket)
supabase.storage.from('avatars').getPublicUrl(`${userId}/avatar.png`)
await supabase.storage.from('documents').createSignedUrl('reports/q4.pdf', 3600)
```
```

## supabase-deploy-integration (1908-supabase-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/supabase-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1908-supabase-pack/6851-supabase-deploy-integration
- الوصف: Deploy and manage Supabase projects in production. Covers database migrations,

```markdown
# Supabase Deploy Integration

## Overview

Deploy and manage Supabase projects in production with confidence. This skill covers the full deployment lifecycle: pushing database migrations, deploying Edge Functions, managing secrets, executing zero-downtime rollouts with blue/green database branching, rolling back failed migrations, and verifying deployment health. All commands use the Supabase CLI with `--project-ref` for explicit project targeting.

**SDK**: `@supabase/supabase-js` — [supabase.com/docs](https://supabase.com/docs)

## Prerequisites

- Supabase CLI installed (`npm install -g supabase` or `npx supabase`)
- Supabase project linked (`npx supabase link --project-ref <your-ref>`)
- Database migrations in `supabase/migrations/` directory
- Edge Functions in `supabase/functions/` directory (if deploying functions)
- `SUPABASE_ACCESS_TOKEN` set for CI/non-interactive environments

## Instructions

### Step 1 — Push Database Migrations and Deploy Edge Functions

Apply pending database migrations to your production project, then deploy Edge Functions with their required secrets.

**Database migrations:**

```bash
# Apply all pending migrations to production
npx supabase db push --project-ref $PROJECT_REF

# Preview what will run without applying (dry run)
npx supabase db push --project-ref $PROJECT_REF --dry-run

# Check current migration status
npx supabase migration list --project-ref $PROJECT_REF
```

Each migration file in `supabase/migrations/` is applied in timestamp order. The CLI tracks which migrations have already been applied and only runs new ones.

**Edge Functions deployment:**

```bash
# Deploy a single Edge Function
npx supabase functions deploy process-webhook --project-ref $PROJECT_REF

# Deploy all Edge Functions at once
npx supabase functions deploy --project-ref $PROJECT_REF
```

**Secrets management — set environment variables for Edge Functions:**

```bash
# Set individual secrets
npx supabase secrets set STRIPE_KEY=sk_live_xxx --project-ref $PROJECT_REF
npx supabase secrets set WEBHOOK_SECRET=whsec_xxx --project-ref $PROJECT_REF

# Set multiple secrets at once
npx supabase secrets set API_KEY=value1 SIGNING_KEY=value2 --project-ref $PROJECT_REF

# List current secrets (names only, values hidden)
npx supabase secrets list --project-ref $PROJECT_REF

# Remove a secret
npx supabase secrets unset OLD_KEY --project-ref $PROJECT_REF
```

### Step 2 — Zero-Downtime Deployments and Blue/Green Branching

Use Supabase database branching to test migrations against a production-like environment before cutting over.

**Blue/green deployment via database branching:**

```bash
# Create a preview branch (clones schema, not data)
npx supabase branches create staging-v2 --project-ref $PROJECT_REF
```

## supabase-js (3065-supabase-js)

- الترخيص: **MIT**  ·  الأصل: https://github.com/sleestk/skills-pipeline/tree/cd75a3875f3b467fa5747ef71d334e1c79b83918/SaaS/supabase-js
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3065-supabase-js/13222-supabase-js
- الوصف: Full-stack Supabase developer skill for building Next.js applications with Supabase. Covers Database (Postgres tables, schemas, views, indexes, joins, JSON, RLS, CLS, roles, functions, triggers, webhooks, event triggers), Auth (email/password, magic link, OTP, OAuth, anonymous sign-ins, MFA, SSR/PKCE flows, sessions, redirect URLs, user management), the JavaScript client (`@supabase/supabase-js` —

```markdown
# Supabase Developer Skill

A comprehensive skill for building Next.js applications with Supabase. Covers four domains: **Database**, **Auth**, **JavaScript Client**, and **Next.js Integration**.

## Architecture

This skill uses progressive disclosure with nested routing:

```
supabase/
├── SKILL.md                          ← You are here (orchestrator)
├── references/
│   ├── database/
│   │   ├── README.md                 ← Database router
│   │   ├── fundamentals.md           ← Connecting, importing, securing
│   │   ├── basics.md                 ← Tables, views, arrays, indexes, joins, JSON
│   │   ├── intermediate.md           ← Cascade deletes, enums, functions, triggers, webhooks, event triggers
│   │   └── access-security.md        ← RLS, CLS, Postgres roles, custom roles
│   ├── auth.md                       ← Full auth reference
│   ├── js-client.md                  ← @supabase/supabase-js API reference
│   └── nextjs.md                     ← @supabase/ssr + Next.js integration
```

## Routing

When the user's request arrives, determine which domain(s) it touches, then read the appropriate reference file(s):

### Database
If the request involves tables, schemas, views, columns, data types, indexes, joins, foreign keys, JSON/JSONB, importing data, connecting to the database, or any SQL DDL/DML:
→ Read `references/database/README.md` first. It will route you to the correct sub-file.

### Auth
If the request involves sign up, sign in, sign out, password reset, OAuth, magic link, OTP, MFA, sessions, JWTs, RLS policies tied to `auth.uid()`, redirect URLs, user management, or the `auth` schema:
→ Read `references/auth.md`

### JavaScript Client
If the request involves `supabase.from()`, `.select()`, `.insert()`, `.update()`, `.delete()`, `.rpc()`, filters (`.eq()`, `.neq()`, `.in()`, etc.), modifiers (`.order()`, `.limit()`, `.single()`), or any `supabase.auth.*` method calls:
→ Read `references/js-client.md`

### Next.js Integration
If the request involves `@supabase/ssr`, `createBrowserClient`, `createServerClient`, middleware/proxy auth, cookie-based sessions, server components with Supabase, or wiring Supabase into a Next.js app:
→ Read `references/nextjs.md`

### Multiple Domains
Many requests touch multiple domains. For example, "set up auth with email/password in my Next.js app" requires **Auth** + **Next.js** + **JS Client**. Read all relevant files.

## Default Stack

- **Framework**: Next.js (App Router)
- **Client library**: `@supabase/supabase-js` v2
- **SSR package**: `@supabase/ssr`
- **Language**: TypeScript
- **ORM**: None (direct supabase-js queries)

## Key Principles

1. **Always enable RLS** on public-facing tables. No exceptions.
2. **Use `(select auth.uid())` in RLS policies** (wrapped in select for performance).
```

## stripe-developer (3064-stripe-developer)

- الترخيص: **MIT**  ·  الأصل: https://github.com/sleestk/skills-pipeline/tree/cd75a3875f3b467fa5747ef71d334e1c79b83918/SaaS/stripe-developer
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3064-stripe-developer/13221-stripe-developer
- الوصف: Full-stack Stripe developer skill for building payment integrations with Next.js and Supabase. Covers Checkout (hosted and embedded), Products & Prices, Subscriptions & Billing, Webhooks (signature verification, event handling), Customer Portal, the Stripe Node.js SDK, client-side Stripe.js, and the Stripe CLI. Use this skill whenever the user mentions Stripe, payments, checkout, subscriptions, bi

```markdown
# Stripe Developer Skill

A comprehensive skill for building payment integrations in Next.js applications with Stripe. Covers five domains: **Checkout & Payments**, **Products & Pricing**, **Subscriptions & Billing**, **Webhooks**, and **Customer Portal**.

## Architecture

This skill uses progressive disclosure with reference files:

```
stripe-developer/
├── SKILL.md                          ← You are here (orchestrator)
├── references/
│   ├── checkout.md                   ← Checkout Sessions (hosted + embedded)
│   ├── products-prices.md            ← Products, Prices, and pricing models
│   ├── subscriptions.md              ← Subscriptions, billing lifecycle, metered/tiered
│   ├── webhooks.md                   ← Webhook endpoints, signature verification, event handling
│   ├── customer-portal.md            ← Self-service subscription management
│   └── nextjs-supabase-integration.md ← Cross-stack wiring patterns
```

## Routing

When the user's request arrives, determine which domain(s) it touches, then read the appropriate reference file(s):

### Checkout & Payments
If the request involves creating a checkout session, one-time payments, payment pages, redirecting to Stripe, embedded checkout, or the Stripe payment form:
→ Read `references/checkout.md`

### Products & Pricing
If the request involves creating products, setting prices, pricing tiers, free vs. pro plans, price IDs, or configuring what you sell:
→ Read `references/products-prices.md`

### Subscriptions & Billing
If the request involves recurring payments, subscription lifecycle (create, upgrade, downgrade, cancel, renew), billing intervals, trial periods, metered billing, or subscription status management:
→ Read `references/subscriptions.md`

### Webhooks
If the request involves listening for Stripe events, webhook endpoints, signature verification, handling `checkout.session.completed`, `invoice.paid`, `customer.subscription.updated`, or any event-driven payment logic:
→ Read `references/webhooks.md`

### Customer Portal
If the request involves letting customers manage their own subscriptions, update payment methods, view invoices, cancel subscriptions, or self-service billing:
→ Read `references/customer-portal.md`

### Cross-Stack Integration (Next.js + Supabase + Vercel)
If the request involves wiring Stripe into a Next.js + Supabase stack, syncing subscription status to the database, gating features behind payment status, deploying with Stripe env vars on Vercel, or building a complete SaaS payment flow:
→ Read `references/nextjs-supabase-integration.md`

### Multiple Domains
```

## supabase (1438-supabase-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/fcakyon/claude-codex-settings/tree/d3974af4e8991489df54c87b51989e13d3d6f265/plugins/supabase-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1438-supabase-skills/3437-supabase
- الوصف: Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrati

```markdown
# Supabase

## Core Principles

**1. Supabase changes frequently — verify against changelog and current docs before implementing.**
Do not rely on training data for Supabase features. Function signatures, config.toml settings, and API conventions change between versions.

First, fetch `https://supabase.com/changelog.md` (a lightweight summary index — not a heavy pull), scan for `breaking-change` tags relevant to your task, and follow the linked page for any that apply. Then look up the relevant topic using the documentation access methods below.

**2. Verify your work.**
After implementing any fix, run a test query to confirm the change works. A fix without verification is incomplete.

**3. Recover from errors, don't loop.**
If an approach fails after 2-3 attempts, stop and reconsider. Try a different method, check documentation, inspect the error more carefully, and review relevant logs when available. Supabase issues are not always solved by retrying the same command, and the answer is not always in the logs, but logs are often worth checking before proceeding.

**4. Exposing tables to the Data API:** Depending on the user's [Data API settings](https://supabase.com/dashboard/project/<ref>/integrations/data_api/settings), newly created tables may not be automatically exposed via the Data (REST) API. If this is the case, `anon` and `authenticated` roles will need to be explicitly granted access.

> Note that this is separate from RLS, which controls which _rows_ are visible once a table is accessible, not whether the table is accessible at all.

When a user reports a SQL-created table is unexpectedly inaccessible, check their Data API settings and whether the roles have been granted access via explicit `GRANT` SQL. When granting public (`anon`/`authenticated`) access, always enable RLS too. See [Exposing a Table to the Data API](https://supabase.com/docs/guides/api/securing-your-api.md) for the full setup workflow.

**5. RLS in exposed schemas.**
Enable RLS on every table in any exposed schema, which includes `public` by default. This is critical in Supabase because tables in exposed schemas can be reachable through the Data API when the `anon`/`authenticated` roles have access (see [Exposing a Table to the Data API](https://supabase.com/docs/guides/api/securing-your-api.md)). For private schemas, prefer RLS as defense in depth. After enabling RLS, create policies that match the actual access model rather than defaulting every table to the same `auth.uid()` pattern.

**6. Security checklist.**
When working on any Supabase task that touches auth, RLS, views, storage, or user data, run through this checklist. These are Supabase-specific security traps that silently create vulnerabilities:

- **Auth and session security**
```

## saas-scaffolder (198-product-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/product-team
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/198-product-skills/641-saas-scaffolder
- الوصف: Generates complete, production-ready SaaS project boilerplate including authentication, database schemas, billing integration, API routes, and a working dashboard using Next.js 14+ App Router, TypeScript, Tailwind CSS, shadcn/ui, Drizzle ORM, and Stripe. Use when the user wants to create a new SaaS app, start a subscription-based web project, scaffold a Next.js application, or mentions terms like 

```markdown
# SaaS Scaffolder

**Tier:** POWERFUL
**Category:** Product Team
**Domain:** Full-Stack Development / Project Bootstrapping

---

## Input Format

```
Product: [name]
Description: [1-3 sentences]
Auth: nextauth | clerk | supabase
Database: neondb | supabase | planetscale
Payments: stripe | lemonsqueezy | none
Features: [comma-separated list]
```

---

## File Tree Output

```
my-saas/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── layout.tsx
│   ├── (dashboard)/
│   │   ├── dashboard/page.tsx
│   │   ├── settings/page.tsx
│   │   ├── billing/page.tsx
│   │   └── layout.tsx
│   ├── (marketing)/
│   │   ├── page.tsx
│   │   ├── pricing/page.tsx
│   │   └── layout.tsx
│   ├── api/
│   │   ├── auth/[...nextauth]/route.ts
│   │   ├── webhooks/stripe/route.ts
│   │   ├── billing/checkout/route.ts
│   │   └── billing/portal/route.ts
│   └── layout.tsx
├── components/
│   ├── ui/
│   ├── auth/
│   │   ├── login-form.tsx
│   │   └── register-form.tsx
│   ├── dashboard/
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   └── stats-card.tsx
│   ├── marketing/
│   │   ├── hero.tsx
│   │   ├── features.tsx
│   │   ├── pricing.tsx
│   │   └── footer.tsx
│   └── billing/
│       ├── plan-card.tsx
│       └── usage-meter.tsx
├── lib/
│   ├── auth.ts
│   ├── db.ts
│   ├── stripe.ts
│   ├── validations.ts
│   └── utils.ts
├── db/
│   ├── schema.ts
│   └── migrations/
├── hooks/
│   ├── use-subscription.ts
│   └── use-user.ts
├── types/index.ts
├── middleware.ts
├── .env.example
├── drizzle.config.ts
└── next.config.ts
```

---

## Key Component Patterns

### Auth Config (NextAuth)

```typescript
// lib/auth.ts
import { NextAuthOptions } from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import { DrizzleAdapter } from "@auth/drizzle-adapter"
import { db } from "./db"

export const authOptions: NextAuthOptions = {
  adapter: DrizzleAdapter(db),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    session: async ({ session, user }) => ({
      ...session,
      user: {
        ...session.user,
        id: user.id,
        subscriptionStatus: user.subscriptionStatus,
      },
    }),
  },
  pages: { signIn: "/login" },
}
```

### Database Schema (Drizzle + NeonDB)

```typescript
// db/schema.ts
import { pgTable, text, timestamp, integer } from "drizzle-orm/pg-core"

export const users = pgTable("users", {
  id: text("id").primaryKey().$defaultFn(() => crypto.randomUUID()),
  name: text("name"),
  email: text("email").notNull().unique(),
  emailVerified: timestamp("emailVerified"),
  image: text("image"),
  stripeCustomerId: text("stripe_customer_id").unique(),
```
