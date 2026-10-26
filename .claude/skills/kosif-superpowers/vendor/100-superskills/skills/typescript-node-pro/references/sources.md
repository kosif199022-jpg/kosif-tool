# مصادر «TypeScript وNode المحترف» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## migrate-to-deno (2898-deno)

- الترخيص: **MIT**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/deno
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2898-deno/11718-migrate-to-deno
- الوصف: Use when moving a Node.js, npm, Yarn, pnpm, or Bun project to Deno, or when adopting Deno incrementally in an existing JavaScript or TypeScript codebase. Covers using Deno as a drop-in package manager, running existing package.json scripts, CommonJS versus ESM, node_modules layout, lockfile migration, permissions, whether to adopt the built-in toolchain, and per-tool command equivalents.

```markdown
# Migrating to Deno

Requires Deno 2.9 or later. For general Deno usage once migrated, see the `deno`
skill.

## Most Node projects already run under Deno

Deno reads an existing `package.json`, resolves the same npm packages, writes a
real `node_modules`, runs the same scripts, and supports `node:` built-ins.
TypeScript runs with no build step.

There is usually **no code to change** — only which binary you invoke. Don't
start by rewriting imports to `jsr:`, swapping dependencies for Deno-specific
ones, or restructuring directories. Proposing that is the most common way this
goes wrong.

## Migrate in rungs

Each rung is independently useful and reversible. Stop wherever suits the
project; plenty of teams stop at rung 1.

### Rung 1 — Deno as the package manager only

```bash
deno install
```

Reads `package.json`, resolves the same dependencies, writes `node_modules`, and
creates `deno.lock` — seeded from any existing `package-lock.json`, `yarn.lock`,
`bun.lock`, or pnpm lockfile, so pins and integrity hashes carry over instead of
drifting.

The app still runs under `node`; teammates are unaffected. Commit `deno.lock`
once verified. **To back out:** delete `deno.lock` and `node_modules`, then
`npm install`.

### Rung 2 — Run it with Deno

```bash
deno run -A main.js      # or: deno -A main.js
deno task build          # runs scripts.build from package.json
```

Use `-A` here. The goal is confirming the program works, not designing a
permission policy — changing both at once makes failures ambiguous.

### Rung 3 — Tighten permissions

Replace `-A` with the narrowest set that works: run it, read what it asks for,
grant exactly that.

```bash
deno run --allow-net=api.example.com --allow-read=./config --allow-env=PORT main.js
```

This buys something Node cannot offer, and is worth doing before deploying.

### Rung 4 — Optionally, adopt the built-in toolchain

`deno fmt` for prettier, `deno lint` for eslint, `deno test` for jest or vitest,
`deno check` for tsc, `deno watch` for nodemon, `deno compile` for pkg.

**Optional, and usually not worth it for an existing project.** These are not
drop-in replacements; parity is incomplete, so this is a real migration, not a
config change. A project happy with prettier, eslint, and vitest should keep
them and use Deno as runtime and package manager only. Prefer the built-in tools
for new projects. If you do move an existing one, go a tool at a time.

## Command equivalents

| Task          | npm                 | Yarn                        | pnpm                       | Bun                             | Deno              |
| ------------- | ------------------- | --------------------------- | -------------------------- | ------------------------------- | ----------------- |
```

## migrate-to-deno (2898-deno)

- الترخيص: **MIT**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/deno
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2898-deno/11723-migrate-to-deno
- الوصف: Use when moving a Node.js, npm, Yarn, pnpm, or Bun project to Deno, or when adopting Deno incrementally in an existing JavaScript or TypeScript codebase. Covers using Deno as a drop-in package manager, running existing package.json scripts, CommonJS versus ESM, node_modules layout, lockfile migration, permissions, whether to adopt the built-in toolchain, and per-tool command equivalents.

```markdown
# Migrating to Deno

Requires Deno 2.9 or later. For general Deno usage once migrated, see the `deno`
skill.

## Most Node projects already run under Deno

Deno reads an existing `package.json`, resolves the same npm packages, writes a
real `node_modules`, runs the same scripts, and supports `node:` built-ins.
TypeScript runs with no build step.

There is usually **no code to change** — only which binary you invoke. Don't
start by rewriting imports to `jsr:`, swapping dependencies for Deno-specific
ones, or restructuring directories. Proposing that is the most common way this
goes wrong.

## Migrate in rungs

Each rung is independently useful and reversible. Stop wherever suits the
project; plenty of teams stop at rung 1.

### Rung 1 — Deno as the package manager only

```bash
deno install
```

Reads `package.json`, resolves the same dependencies, writes `node_modules`, and
creates `deno.lock` — seeded from any existing `package-lock.json`, `yarn.lock`,
`bun.lock`, or pnpm lockfile, so pins and integrity hashes carry over instead of
drifting.

The app still runs under `node`; teammates are unaffected. Commit `deno.lock`
once verified. **To back out:** delete `deno.lock` and `node_modules`, then
`npm install`.

### Rung 2 — Run it with Deno

```bash
deno run -A main.js      # or: deno -A main.js
deno task build          # runs scripts.build from package.json
```

Use `-A` here. The goal is confirming the program works, not designing a
permission policy — changing both at once makes failures ambiguous.

### Rung 3 — Tighten permissions

Replace `-A` with the narrowest set that works: run it, read what it asks for,
grant exactly that.

```bash
deno run --allow-net=api.example.com --allow-read=./config --allow-env=PORT main.js
```

This buys something Node cannot offer, and is worth doing before deploying.

### Rung 4 — Optionally, adopt the built-in toolchain

`deno fmt` for prettier, `deno lint` for eslint, `deno test` for jest or vitest,
`deno check` for tsc, `deno watch` for nodemon, `deno compile` for pkg.

**Optional, and usually not worth it for an existing project.** These are not
drop-in replacements; parity is incomplete, so this is a real migration, not a
config change. A project happy with prettier, eslint, and vitest should keep
them and use Deno as runtime and package manager only. Prefer the built-in tools
for new projects. If you do move an existing one, go a tool at a time.

## Command equivalents

| Task          | npm                 | Yarn                        | pnpm                       | Bun                             | Deno              |
| ------------- | ------------------- | --------------------------- | -------------------------- | ------------------------------- | ----------------- |
```

## javascript-testing-patterns (3102-javascript-typescript)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/javascript-typescript
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3102-javascript-typescript/13274-javascript-testing-patterns
- الوصف: Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mocking, fixtures, and test-driven development. Use when writing JavaScript/TypeScript tests, setting up test infrastructure, or implementing TDD/BDD workflows.

```markdown
# JavaScript Testing Patterns

Comprehensive guide for implementing robust testing strategies in JavaScript/TypeScript applications using modern testing frameworks and best practices.

## When to Use This Skill

- Setting up test infrastructure for new projects
- Writing unit tests for functions and classes
- Creating integration tests for APIs and services
- Implementing end-to-end tests for user flows
- Mocking external dependencies and APIs
- Testing React, Vue, or other frontend components
- Implementing test-driven development (TDD)
- Setting up continuous testing in CI/CD pipelines

## Testing Frameworks

### Jest - Full-Featured Testing Framework

**Setup:**

```typescript
// jest.config.ts
import type { Config } from "jest";

const config: Config = {
  preset: "ts-jest",
  testEnvironment: "node",
  roots: ["<rootDir>/src"],
  testMatch: ["**/__tests__/**/*.ts", "**/?(*.)+(spec|test).ts"],
  collectCoverageFrom: [
    "src/**/*.ts",
    "!src/**/*.d.ts",
    "!src/**/*.interface.ts",
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  setupFilesAfterEnv: ["<rootDir>/src/test/setup.ts"],
};

export default config;
```

### Vitest - Fast, Vite-Native Testing

**Setup:**

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["**/*.d.ts", "**/*.config.ts", "**/dist/**"],
    },
    setupFiles: ["./src/test/setup.ts"],
  },
});
```

## Unit Testing Patterns

### Pattern 1: Testing Pure Functions

```typescript
// utils/calculator.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}

// utils/calculator.test.ts
import { describe, it, expect } from "vitest";
import { add, divide } from "./calculator";

describe("Calculator", () => {
  describe("add", () => {
    it("should add two positive numbers", () => {
      expect(add(2, 3)).toBe(5);
    });

    it("should add negative numbers", () => {
      expect(add(-2, -3)).toBe(-5);
    });

    it("should handle zero", () => {
      expect(add(0, 5)).toBe(5);
      expect(add(5, 0)).toBe(5);
    });
  });

  describe("divide", () => {
    it("should divide two numbers", () => {
      expect(divide(10, 2)).toBe(5);
    });

    it("should handle decimal results", () => {
      expect(divide(5, 2)).toBe(2.5);
    });

    it("should throw error when dividing by zero", () => {
      expect(() => divide(10, 0)).toThrow("Division by zero");
    });
  });
});
```
```

## javascript-testing-patterns (3495-javascript-typescript)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/javascript-typescript
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3495-javascript-typescript/14221-javascript-testing-patterns
- الوصف: Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mocking, fixtures, and test-driven development. Use when writing JavaScript/TypeScript tests, setting up test infrastructure, or implementing TDD/BDD workflows.

```markdown
# JavaScript Testing Patterns

Comprehensive guide for implementing robust testing strategies in JavaScript/TypeScript applications using modern testing frameworks and best practices.

## When to Use This Skill

- Setting up test infrastructure for new projects
- Writing unit tests for functions and classes
- Creating integration tests for APIs and services
- Implementing end-to-end tests for user flows
- Mocking external dependencies and APIs
- Testing React, Vue, or other frontend components
- Implementing test-driven development (TDD)
- Setting up continuous testing in CI/CD pipelines

## Testing Frameworks

### Jest - Full-Featured Testing Framework

**Setup:**

```typescript
// jest.config.ts
import type { Config } from "jest";

const config: Config = {
  preset: "ts-jest",
  testEnvironment: "node",
  roots: ["<rootDir>/src"],
  testMatch: ["**/__tests__/**/*.ts", "**/?(*.)+(spec|test).ts"],
  collectCoverageFrom: [
    "src/**/*.ts",
    "!src/**/*.d.ts",
    "!src/**/*.interface.ts",
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  setupFilesAfterEnv: ["<rootDir>/src/test/setup.ts"],
};

export default config;
```

### Vitest - Fast, Vite-Native Testing

**Setup:**

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["**/*.d.ts", "**/*.config.ts", "**/dist/**"],
    },
    setupFiles: ["./src/test/setup.ts"],
  },
});
```

## Unit Testing Patterns

### Pattern 1: Testing Pure Functions

```typescript
// utils/calculator.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}

// utils/calculator.test.ts
import { describe, it, expect } from "vitest";
import { add, divide } from "./calculator";

describe("Calculator", () => {
  describe("add", () => {
    it("should add two positive numbers", () => {
      expect(add(2, 3)).toBe(5);
    });

    it("should add negative numbers", () => {
      expect(add(-2, -3)).toBe(-5);
    });

    it("should handle zero", () => {
      expect(add(0, 5)).toBe(5);
      expect(add(5, 0)).toBe(5);
    });
  });

  describe("divide", () => {
    it("should divide two numbers", () => {
      expect(divide(10, 2)).toBe(5);
    });

    it("should handle decimal results", () => {
      expect(divide(5, 2)).toBe(2.5);
    });

    it("should throw error when dividing by zero", () => {
      expect(() => divide(10, 0)).toThrow("Division by zero");
    });
  });
});
```
```

## typescript-debugging (2174-typescript-plugin)

- الترخيص: **MIT**  ·  الأصل: https://github.com/laurigates/claude-plugins/tree/9caa2be8e7b4b35823e4154c610e3846af05635c/typescript-plugin
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2174-typescript-plugin/7942-typescript-debugging
- الوصف: Modern TypeScript/JavaScript debugging with Bun — inspector flags, debug.bun.sh, VSCode launch.json, memory profiling, heap analysis. Use when setting up interactive debugging, investigating leaks, CPU profiling with `--cpu-prof`, or sourcemaps.

```markdown
# TypeScript Debugging

## When to Use This Skill

| Scenario | Use this skill | Alternative |
|----------|---------------|-------------|
| Setting up Bun inspector for debugging | Yes | N/A |
| Configuring VSCode launch.json for Bun | Yes | N/A |
| Investigating memory leaks with heap snapshots | Yes | N/A |
| CPU profiling TypeScript applications | Yes | N/A |
| Debugging network requests with verbose fetch | Yes | N/A |
| Setting up sourcemaps for debugging | Yes | `bun-development` for build-time sourcemap flags |
| Monitoring errors in production | No - use `typescript-sentry` | N/A |
| Running tests to find failures | No - use `bun-development` | `bun-test` for quick test runs |

## Core Expertise

Modern debugging for TypeScript/JavaScript with Bun runtime:
- WebKit Inspector Protocol (debug.bun.sh)
- VSCode integration with Bun extension
- Memory profiling with V8 heap snapshots
- Automatic sourcemap generation for TypeScript
- Chrome DevTools for heap analysis

## Inspector Flags

### Basic Debugging

```bash
# Start with debugger enabled
bun --inspect script.ts

# Custom port
bun --inspect=4000 script.ts

# Custom host:port
bun --inspect=localhost:4000 script.ts
```

### Break on Start

```bash
# Break at first line (for fast scripts)
bun --inspect-brk script.ts

# Wait for debugger before running
bun --inspect-wait script.ts
```

### Debugging Tests

```bash
# Debug test file
bun --inspect test

# Break before tests run
bun --inspect-brk test auth.test.ts
```

## Web Debugger (debug.bun.sh)

Bun's built-in web debugger is a modified WebKit Web Inspector:

```bash
# Start debugging - outputs debug URL
bun --inspect script.ts
# ------------------- Bun Inspector -------------------
# Listening: ws://localhost:6499/
# Open: debug.bun.sh/#localhost:6499
# -----------------------------------------------------
```

### Features

| Feature | Description |
|---------|-------------|
| Source view | View original TypeScript/JSX with sourcemaps |
| Breakpoints | Click line numbers to set/remove |
| Console | Execute code in current context |
| Call stack | Inspect execution frames |
| Scope | View local/closure/global variables |
| Watch | Add expressions to monitor |

### Execution Controls

| Control | Action |
|---------|--------|
| Continue (F8) | Run until next breakpoint |
| Step Over (F10) | Execute line, skip into functions |
| Step Into (F11) | Enter function call |
| Step Out (Shift+F11) | Complete function, return to caller |

## VSCode Integration

### Extension Setup

Install [Bun for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=oven.bun-vscode).

### launch.json Configuration

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "bun",
      "request": "launch",
```

## mastering-typescript (52-typescript-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/acaprino/daodan/tree/39443d215d28fcbc32d651895b3cc45c64f24b6f/exports/claude/plugins/typescript-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/52-typescript-development/77-mastering-typescript
- الوصف: Deep reference for advanced TypeScript. TRIGGER WHEN: migrating JavaScript to TypeScript, bootstrapping a TS project (strict tsconfig, ESLint, Vite/Vitest, pnpm), writing generics, mapped or conditional types, `satisfies`, branded types, discriminated unions or template literal types, designing Zod schemas for runtime validation, building type-safe NestJS APIs, deep React and TypeScript typing, ty

```markdown
Source: SpillwaveSolutions/mastering-typescript-skill - `mastering-typescript/SKILL.md`

# Mastering Modern TypeScript

Build enterprise-grade, type-safe applications with TypeScript 5.9+.

> **Compatibility:** TypeScript 5.9+, Node.js 22 LTS, Vite 7, NestJS 11, React 19

## Quick Start

```bash
# Initialize TypeScript project with ESM
pnpm create vite@latest my-app --template vanilla-ts
cd my-app && pnpm install

# Configure strict TypeScript
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2024",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
EOF
```

## When to Use This Skill

Use when:
- Building type-safe React, NestJS, or Node.js applications
- Migrating JavaScript codebases to TypeScript
- Implementing advanced type patterns (generics, mapped types, conditional types)
- Configuring modern TypeScript toolchains (Vite, pnpm, ESLint)
- Designing type-safe API contracts with Zod validation
- Comparing TypeScript approaches with Java or Python

## Project Setup Checklist

Before starting any TypeScript project:

```
- [ ] Use pnpm for package management (faster, disk-efficient)
- [ ] Configure ESM-first (type: "module" in package.json)
- [ ] Enable strict mode in tsconfig.json
- [ ] Set up ESLint with @typescript-eslint
- [ ] Add Prettier for consistent formatting
- [ ] Configure Vitest for testing
```

## Type System Quick Reference

### Primitive Types

```typescript
const name: string = "Alice";
const age: number = 30;
const active: boolean = true;
const id: bigint = 9007199254740991n;
const key: symbol = Symbol("unique");
```

### Union and Intersection Types

```typescript
// Union: value can be one of several types
type Status = "pending" | "approved" | "rejected";

// Intersection: value must satisfy all types
type Employee = Person & { employeeId: string };

// Discriminated union for type-safe handling
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function handleResult<T>(result: Result<T>): T | null {
  if (result.success) {
    return result.data; // TypeScript knows data exists here
  }
  console.error(result.error);
  return null;
}
```

### Type Guards

```typescript
// typeof guard
function process(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toFixed(2);
}

// Custom type guard
interface User { type: "user"; name: string }
interface Admin { type: "admin"; permissions: string[] }

function isAdmin(person: User | Admin): person is Admin {
  return person.type === "admin";
}
```

### The `satisfies` Operator (TS 5.0+)
```
