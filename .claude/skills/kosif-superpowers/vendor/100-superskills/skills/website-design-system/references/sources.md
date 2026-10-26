# مصادر «تصميم المواقع ونظام التصميم» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## tailwind-design-system (3096-frontend-mobile-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/frontend-mobile-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3096-frontend-mobile-development/13267-tailwind-design-system
- الوصف: Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns. Use when creating component libraries, implementing design systems, or standardizing UI patterns.

```markdown
# Tailwind Design System (v4)

Build production-ready design systems with Tailwind CSS v4, including CSS-first configuration, design tokens, component variants, responsive patterns, and accessibility.

> **Note**: This skill targets Tailwind CSS v4 (2024+). For v3 projects, refer to the [upgrade guide](https://tailwindcss.com/docs/upgrade-guide).

## When to Use This Skill

- Creating a component library with Tailwind v4
- Implementing design tokens and theming with CSS-first configuration
- Building responsive and accessible components
- Standardizing UI patterns across a codebase
- Migrating from Tailwind v3 to v4
- Setting up dark mode with native CSS features

## Key v4 Changes

| v3 Pattern                            | v4 Pattern                                                            |
| ------------------------------------- | --------------------------------------------------------------------- |
| `tailwind.config.ts`                  | `@theme` in CSS                                                       |
| `@tailwind base/components/utilities` | `@import "tailwindcss"`                                               |
| `darkMode: "class"`                   | `@custom-variant dark (&:where(.dark, .dark *))`                      |
| `theme.extend.colors`                 | `@theme { --color-*: value }`                                         |
| `require("tailwindcss-animate")`      | CSS `@keyframes` in `@theme` + `@starting-style` for entry animations |

## Quick Start

```css
/* app.css - Tailwind v4 CSS-first configuration */
@import "tailwindcss";

/* Define your theme with @theme */
@theme {
  /* Semantic color tokens using OKLCH for better color perception */
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);

  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);

  --color-secondary: oklch(96% 0.01 264);
  --color-secondary-foreground: oklch(14.5% 0.025 264);

  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);

  --color-accent: oklch(96% 0.01 264);
  --color-accent-foreground: oklch(14.5% 0.025 264);

  --color-destructive: oklch(53% 0.22 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);

  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(14.5% 0.025 264);

  /* Ring offset for focus states */
  --color-ring-offset: oklch(100% 0 0);

  /* Radius tokens */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;

  /* Animation tokens - keyframes inside @theme are output when referenced by --animate-* variables */
  --animate-fade-in: fade-in 0.2s ease-out;
```

## tailwind-design-system (3486-frontend-mobile-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/frontend-mobile-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3486-frontend-mobile-development/14211-tailwind-design-system
- الوصف: Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive patterns. Use when creating component libraries, implementing design systems, or standardizing UI patterns.

```markdown
# Tailwind Design System (v4)

Build production-ready design systems with Tailwind CSS v4, including CSS-first configuration, design tokens, component variants, responsive patterns, and accessibility.

> **Note**: This skill targets Tailwind CSS v4 (2024+). For v3 projects, refer to the [upgrade guide](https://tailwindcss.com/docs/upgrade-guide).

## When to Use This Skill

- Creating a component library with Tailwind v4
- Implementing design tokens and theming with CSS-first configuration
- Building responsive and accessible components
- Standardizing UI patterns across a codebase
- Migrating from Tailwind v3 to v4
- Setting up dark mode with native CSS features

## Key v4 Changes

| v3 Pattern                            | v4 Pattern                                                            |
| ------------------------------------- | --------------------------------------------------------------------- |
| `tailwind.config.ts`                  | `@theme` in CSS                                                       |
| `@tailwind base/components/utilities` | `@import "tailwindcss"`                                               |
| `darkMode: "class"`                   | `@custom-variant dark (&:where(.dark, .dark *))`                      |
| `theme.extend.colors`                 | `@theme { --color-*: value }`                                         |
| `require("tailwindcss-animate")`      | CSS `@keyframes` in `@theme` + `@starting-style` for entry animations |

## Quick Start

```css
/* app.css - Tailwind v4 CSS-first configuration */
@import "tailwindcss";

/* Define your theme with @theme */
@theme {
  /* Semantic color tokens using OKLCH for better color perception */
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);

  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);

  --color-secondary: oklch(96% 0.01 264);
  --color-secondary-foreground: oklch(14.5% 0.025 264);

  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);

  --color-accent: oklch(96% 0.01 264);
  --color-accent-foreground: oklch(14.5% 0.025 264);

  --color-destructive: oklch(53% 0.22 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);

  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(14.5% 0.025 264);

  /* Ring offset for focus states */
  --color-ring-offset: oklch(100% 0 0);

  /* Radius tokens */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;

  /* Animation tokens - keyframes inside @theme are output when referenced by --animate-* variables */
  --animate-fade-in: fade-in 0.2s ease-out;
```

## tailwind-best-practices (1483-tailwind)

- الترخيص: **MIT**  ·  الأصل: https://github.com/gopherguides/gopher-ai/tree/953b31bdf242c5d05ae91d7ca4cf997c0adbe051/plugins/tailwind
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1483-tailwind/3674-tailwind-best-practices
- الوصف: Tailwind CSS v4 guidance: utility-first patterns, @theme directive for color/spacing/font config, @source for content paths, dark mode, responsive design, oklch colors, custom variants, v4 vs v3 differences. Use when user writes Tailwind utility classes, configures @theme or @source in CSS, asks about v4 syntax, or styles components.

```markdown
# Tailwind CSS v4 Best Practices

Use the bundled references for Tailwind CSS v4 guidance. Consult the linked official documentation when current upstream behavior matters.

## Reference Files

Read the relevant file for detailed patterns, code examples, and documentation URLs:

### `docs-urls.md` — Official Documentation URLs
URL tables organized by category (Getting Started, Core Concepts, Layout, Spacing, Sizing, Typography, Backgrounds & Borders, Effects, Transforms & Animation, Interactivity). Use with WebFetch when current upstream behavior needs verification.

### `v4-syntax.md` — Tailwind CSS v4 Core Syntax
**CRITICAL**: v4 changed significantly from v3. Covers `@import "tailwindcss"`, `@theme` directive for CSS-based configuration (colors, fonts, spacing), `@source` for detection, class-based `@custom-variant dark` plus `.dark` selectors, `@layer components` for extraction, and `@plugin` for plugins.

### `best-practices.md` — Best Practices
Class ordering convention (layout → spacing → sizing → typography → colors → effects → interactive), responsive design (mobile-first, breakpoint reference), component extraction rule (3+ times), theme variables over hardcoded values, accessibility (focus-visible, sr-only, contrast).

### `anti-patterns.md` — v4 Anti-Patterns
v3 → v4 migration table (tailwind.config.js → @theme, @tailwind → @import, etc.), common mistakes (inline styles, px values, duplicate/conflicting utilities).

### `quick-reference.md` — Quick Reference
Response guidelines for helping with Tailwind, example response flow, spacing scale table, common utility patterns (centered content, card, responsive grid, truncation, gradient, fixed header).

---

*For the latest documentation, always refer to https://tailwindcss.com/docs*
```

## ui-design-system (198-product-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/product-team
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/198-product-skills/643-ui-design-system
- الوصف: UI design system toolkit for Senior UI Designer including design token generation, component documentation, responsive design calculations, and developer handoff tools. Use when creating design systems, generating design tokens, maintaining visual consistency, or facilitating design-dev collaboration and developer handoff.

```markdown
# UI Design System

Generate design tokens, create color palettes, calculate typography scales, build component systems, and prepare developer handoff documentation.

---

## Table of Contents

- [Trigger Terms](#trigger-terms)
- [Workflows](#workflows)
  - [Workflow 1: Generate Design Tokens](#workflow-1-generate-design-tokens)
  - [Workflow 2: Create Component System](#workflow-2-create-component-system)
  - [Workflow 3: Responsive Design](#workflow-3-responsive-design)
  - [Workflow 4: Developer Handoff](#workflow-4-developer-handoff)
- [Tool Reference](#tool-reference)
- [Quick Reference Tables](#quick-reference-tables)
- [Knowledge Base](#knowledge-base)

---

## Trigger Terms

Use this skill when you need to:

- "generate design tokens"
- "create color palette"
- "build typography scale"
- "calculate spacing system"
- "create design system"
- "generate CSS variables"
- "export SCSS tokens"
- "set up component architecture"
- "document component library"
- "calculate responsive breakpoints"
- "prepare developer handoff"
- "convert brand color to palette"
- "check WCAG contrast"
- "build 8pt grid system"

---

## Workflows

### Workflow 1: Generate Design Tokens

**Situation:** You have a brand color and need a complete design token system.

**Steps:**

1. **Identify brand color and style**
   - Brand primary color (hex format)
   - Style preference: `modern` | `classic` | `playful`

2. **Generate tokens using script**
   ```bash
   python scripts/design_token_generator.py "#0066CC" modern json
   ```

3. **Review generated categories**
   - Colors: primary, secondary, neutral, semantic, surface
   - Typography: fontFamily, fontSize, fontWeight, lineHeight
   - Spacing: 8pt grid-based scale (0-64)
   - Borders: radius, width
   - Shadows: none through 2xl
   - Animation: duration, easing
   - Breakpoints: xs through 2xl

4. **Export in target format**
   ```bash
   # CSS custom properties
   python scripts/design_token_generator.py "#0066CC" modern css > design-tokens.css

   # SCSS variables
   python scripts/design_token_generator.py "#0066CC" modern scss > _design-tokens.scss

   # JSON for Figma/tooling
   python scripts/design_token_generator.py "#0066CC" modern json > design-tokens.json
   ```

5. **Validate accessibility**
   - Check color contrast meets WCAG AA (4.5:1 normal, 3:1 large text)
   - Verify semantic colors have contrast colors defined

---

### Workflow 2: Create Component System

**Situation:** You need to structure a component library using design tokens.

**Steps:**

1. **Define component hierarchy**
   - Atoms: Button, Input, Icon, Label, Badge
   - Molecules: FormField, SearchBar, Card, ListItem
   - Organisms: Header, Footer, DataTable, Modal
   - Templates: DashboardLayout, AuthLayout

2. **Map tokens to components**
```

## nuxt-ui (2920-nuxt-ui)

- الترخيص: **MIT**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/nuxt-ui
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2920-nuxt-ui/12116-nuxt-ui
- الوصف: Build UIs with @nuxt/ui v4 — 125+ accessible Vue components with Tailwind CSS theming. Use when creating interfaces, customizing themes to match a brand, building forms, or composing layouts like dashboards, docs sites, and chat interfaces.

```markdown
# Nuxt UI

Vue component library built on [Reka UI](https://reka-ui.com/) + [Tailwind CSS](https://tailwindcss.com/) + [Tailwind Variants](https://www.tailwind-variants.org/). Works with Nuxt, Vue (Vite), Laravel (Vite + Inertia), and AdonisJS (Vite + Inertia).

## MCP Server

For component API details (props, slots, events, full documentation, examples), use the [Nuxt UI MCP server](https://ui.nuxt.com/docs/getting-started/ai/mcp). If not already configured, add it:

**Cursor** — `.cursor/mcp.json`:

```json
{ "mcpServers": { "nuxt-ui": { "type": "http", "url": "https://ui.nuxt.com/mcp" } } }
```

**Claude Code**:

```bash
claude mcp add --transport http nuxt-ui https://ui.nuxt.com/mcp
```

Key MCP tools:
- `search-components` — find components by name, category, or intent (no params = list all)
- `search-composables` — find composables by name or description (no params = list all)
- `search-icons` — search Iconify icons (defaults to `lucide`), returns `i-{prefix}-{name}` names
- `get-component` — full component documentation with usage examples
- `get-component-metadata` — props, slots, events (lightweight, no docs content)
- `get-example` — real-world code examples

When you need to know **what a component accepts** or **how its API works**, use the MCP. This skill teaches you **when to use which component** and **how to build well**.

## Core rules (always apply)

1. **Always wrap the app in `UApp`** — required for toasts, tooltips, and programmatic overlays. Accepts a `locale` prop for i18n.
2. **Always use semantic colors** — `text-default`, `bg-elevated`, `border-muted`, etc. Never use raw Tailwind palette colors like `text-gray-500`.
3. **Read generated theme files for slot names** — Nuxt: `.nuxt/ui/<component>.ts`, Vue: `node_modules/.nuxt-ui/ui/<component>.ts`. These show every slot, variant, and default class for any component.
4. **Override priority** (highest wins): `ui` prop / `class` prop → global config → theme defaults.
5. **Icons use `i-{collection}-{name}` format** — `lucide` is the default collection. Use the MCP `search-icons` tool to find icons, or browse at [icones.js.org](https://icones.js.org).

## How to use this skill

Based on the task, load the relevant reference files **before writing any code**. Don't load everything — only what's needed.

### Reference files

**Guidelines** — design decisions and conventions:
- [design-system](references/guidelines/design-system.md) — semantic colors, theming, brand customization, variants, the `ui` prop
- [component-selection](references/guidelines/component-selection.md) — decision matrices: when to use Modal vs Slideover, Select vs SelectMenu, Toast vs Alert, etc.
```

## nuxt-ui (2920-nuxt-ui)

- الترخيص: **MIT**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/nuxt-ui
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2920-nuxt-ui/12117-nuxt-ui
- الوصف: Build UIs with @nuxt/ui v4 — 125+ accessible Vue components with Tailwind CSS theming. Use when creating interfaces, customizing themes to match a brand, building forms, or composing layouts like dashboards, docs sites, and chat interfaces.

```markdown
# Nuxt UI

Vue component library built on [Reka UI](https://reka-ui.com/) + [Tailwind CSS](https://tailwindcss.com/) + [Tailwind Variants](https://www.tailwind-variants.org/). Works with Nuxt, Vue (Vite), Laravel (Vite + Inertia), and AdonisJS (Vite + Inertia).

## MCP Server

For component API details (props, slots, events, full documentation, examples), use the [Nuxt UI MCP server](https://ui.nuxt.com/docs/getting-started/ai/mcp). If not already configured, add it:

**Cursor** — `.cursor/mcp.json`:

```json
{ "mcpServers": { "nuxt-ui": { "type": "http", "url": "https://ui.nuxt.com/mcp" } } }
```

**Claude Code**:

```bash
claude mcp add --transport http nuxt-ui https://ui.nuxt.com/mcp
```

Key MCP tools:
- `search-components` — find components by name, category, or intent (no params = list all)
- `search-composables` — find composables by name or description (no params = list all)
- `search-icons` — search Iconify icons (defaults to `lucide`), returns `i-{prefix}-{name}` names
- `get-component` — full component documentation with usage examples
- `get-component-metadata` — props, slots, events (lightweight, no docs content)
- `get-example` — real-world code examples

When you need to know **what a component accepts** or **how its API works**, use the MCP. This skill teaches you **when to use which component** and **how to build well**.

## Core rules (always apply)

1. **Always wrap the app in `UApp`** — required for toasts, tooltips, and programmatic overlays. Accepts a `locale` prop for i18n.
2. **Always use semantic colors** — `text-default`, `bg-elevated`, `border-muted`, etc. Never use raw Tailwind palette colors like `text-gray-500`.
3. **Read generated theme files for slot names** — Nuxt: `.nuxt/ui/<component>.ts`, Vue: `node_modules/.nuxt-ui/ui/<component>.ts`. These show every slot, variant, and default class for any component.
4. **Override priority** (highest wins): `ui` prop / `class` prop → global config → theme defaults.
5. **Icons use `i-{collection}-{name}` format** — `lucide` is the default collection. Use the MCP `search-icons` tool to find icons, or browse at [icones.js.org](https://icones.js.org).

## How to use this skill

Based on the task, load the relevant reference files **before writing any code**. Don't load everything — only what's needed.

### Reference files

**Guidelines** — design decisions and conventions:
- [design-system](references/guidelines/design-system.md) — semantic colors, theming, brand customization, variants, the `ui` prop
- [component-selection](references/guidelines/component-selection.md) — decision matrices: when to use Modal vs Slideover, Select vs SelectMenu, Toast vs Alert, etc.
```
