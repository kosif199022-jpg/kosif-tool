# مصادر «منظومة الاختبارات الكاملة» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## playwright-testing (2172-testing-plugin)

- الترخيص: **MIT**  ·  الأصل: https://github.com/laurigates/claude-plugins/tree/9caa2be8e7b4b35823e4154c610e3846af05635c/testing-plugin
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2172-testing-plugin/7898-playwright-testing
- الوصف: Playwright E2E testing — cross-browser, visual regression, API testing, mobile emulation. Use when writing E2E tests or setting up automated UI testing for web apps.

```markdown
# Playwright Testing

Playwright is a modern end-to-end testing framework for web applications. It provides reliable, fast, and cross-browser testing with excellent developer experience.

## When to Use This Skill

| Use this skill when... | Use another skill instead when... |
|------------------------|----------------------------------|
| Writing E2E browser tests | Writing unit tests (use vitest-testing) |
| Testing across Chromium, Firefox, WebKit | Testing Python code (use python-testing) |
| Setting up visual regression testing | Analyzing test quality (use test-quality-analysis) |
| Mocking network requests in E2E tests | Generating property-based tests (use property-based-testing) |
| Testing mobile viewports | Testing API contracts only (use api-testing) |

## Core Expertise

- **Cross-browser**: Test on Chromium, Firefox, WebKit (Safari)
- **Reliable**: Auto-wait, auto-retry, no flaky tests
- **Fast**: Parallel execution, browser context isolation
- **Modern**: TypeScript-first, async/await, auto-complete
- **Multi-platform**: Windows, macOS, Linux

## Installation

```bash
bun create playwright                  # Initialize (recommended)
bun add --dev @playwright/test         # Or install manually
bunx playwright install                # Install browsers
bunx playwright install --with-deps    # With system deps (Linux)
bunx playwright --version              # Verify
```

## Configuration (playwright.config.ts)

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

## Essential Commands

```bash
bunx playwright test                           # Run all tests
bunx playwright test tests/login.spec.ts       # Specific file
bunx playwright test --headed                  # See browser
bunx playwright test --debug                   # Debug mode
bunx playwright test --project=chromium        # Specific browser
bunx playwright test --ui                      # UI mode
bunx playwright codegen http://localhost:3000  # Record tests
bunx playwright show-report                    # Last report
bunx playwright show-trace trace.zip           # Trace viewer
bunx playwright test --update-snapshots        # Update snapshots
```

## Writing Tests

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test('basic test', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});

test.describe('login flow', () => {
  test('should login successfully', async ({ page }) => {
```

## analyzing-test-coverage (1971-test-coverage-analyzer)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/testing/test-coverage-analyzer
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1971-test-coverage-analyzer/7118-analyzing-test-coverage
- الوصف: Analyze code coverage metrics and identify untested code paths.

```markdown
# Test Coverage Analyzer

## Current State

!`ls package.json pyproject.toml Cargo.toml go.mod 2>/dev/null || echo 'No project manifest found'`
!`node -v 2>/dev/null || python3 --version 2>/dev/null || echo 'No runtime detected'`

## Overview

Analyze code coverage metrics to identify untested code paths, dead code, and coverage gaps across line, branch, function, and statement dimensions. Supports Istanbul/nyc (JavaScript/TypeScript), coverage.py (Python), JaCoCo (Java), and Go coverage tools.

## Prerequisites

- Coverage tool installed and configured (Istanbul/nyc, c8, coverage.py, JaCoCo, or `go test -cover`)
- Test suite that can run with coverage instrumentation enabled
- Coverage threshold targets defined (recommended: 80% lines, 70% branches)
- Coverage output format set to JSON or LCOV for programmatic analysis
- Git history available for coverage trend comparison

## Instructions

1. Run the test suite with coverage instrumentation enabled:
   - JavaScript: `npx jest --coverage --coverageReporters=json-summary,lcov`
   - Python: `pytest --cov=src --cov-report=json --cov-report=term-missing`
   - Go: `go test -coverprofile=coverage.out ./...`
   - Java: Configure JaCoCo Maven/Gradle plugin with XML report output.
2. Parse the coverage report and extract per-file metrics:
   - Line coverage percentage per file.
   - Branch coverage percentage per file.
   - Function coverage percentage per file.
   - Uncovered line ranges (specific line numbers).
3. Identify critical coverage gaps by prioritizing:
   - Files with coverage below the threshold (sort ascending by coverage %).
   - Files with high complexity but low coverage (use cyclomatic complexity if available).
   - Recently modified files with decreasing coverage trends.
   - Public API functions and exported modules lacking any tests.
4. Analyze uncovered branches specifically:
   - Find `if/else` blocks where only one branch is tested.
   - Identify `switch/case` statements with missing case coverage.
   - Locate error handling paths (`catch`, `except`) never exercised.
   - Check `||` and `&&` short-circuit conditions.
5. Generate a prioritized action plan:
   - List top 10 files needing coverage improvement with specific line ranges.
   - Suggest test scenarios for each uncovered branch.
   - Estimate effort (small/medium/large) for each coverage improvement.
6. Compare current coverage against the previous commit or baseline:
   - Calculate coverage delta per file.
   - Flag files where coverage decreased.
   - Verify new code added since baseline has adequate coverage.
7. Write coverage enforcement configuration (coverage thresholds in Jest config, `.coveragerc`, or CI checks).

## Output

- Coverage summary report with overall and per-file metrics
```

## e2e-testing-patterns (3476-developer-essentials)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/developer-essentials
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3476-developer-essentials/14187-e2e-testing-patterns
- الوصف: Master end-to-end testing with Playwright and Cypress to build reliable test suites that catch bugs, improve confidence, and enable fast deployment. Use when implementing E2E tests, debugging flaky tests, or establishing testing standards.

```markdown
# E2E Testing Patterns

Build reliable, fast, and maintainable end-to-end test suites that provide confidence to ship code quickly and catch regressions before users do.

## When to Use This Skill

- Implementing end-to-end test automation
- Debugging flaky or unreliable tests
- Testing critical user workflows
- Setting up CI/CD test pipelines
- Testing across multiple browsers
- Validating accessibility requirements
- Testing responsive designs
- Establishing E2E testing standards

## Core Concepts

### 1. E2E Testing Fundamentals

**What to Test with E2E:**

- Critical user journeys (login, checkout, signup)
- Complex interactions (drag-and-drop, multi-step forms)
- Cross-browser compatibility
- Real API integration
- Authentication flows

**What NOT to Test with E2E:**

- Unit-level logic (use unit tests)
- API contracts (use integration tests)
- Edge cases (too slow)
- Internal implementation details

### 2. Test Philosophy

**The Testing Pyramid:**

```
        /\
       /E2E\         ← Few, focused on critical paths
      /─────\
     /Integr\        ← More, test component interactions
    /────────\
   /Unit Tests\      ← Many, fast, isolated
  /────────────\
```

**Best Practices:**

- Test user behavior, not implementation
- Keep tests independent
- Make tests deterministic
- Optimize for speed
- Use data-testid, not CSS selectors

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

1. **Use Data Attributes**: `data-testid` or `data-cy` for stable selectors
2. **Avoid Brittle Selectors**: Don't rely on CSS classes or DOM structure
3. **Test User Behavior**: Click, type, see - not implementation details
4. **Keep Tests Independent**: Each test should run in isolation
5. **Clean Up Test Data**: Create and destroy test data in each test
6. **Use Page Objects**: Encapsulate page logic
7. **Meaningful Assertions**: Check actual user-visible behavior
8. **Optimize for Speed**: Mock when possible, parallel execution

```typescript
// ❌ Bad selectors
cy.get(".btn.btn-primary.submit-button").click();
cy.get("div > form > div:nth-child(2) > input").type("text");

// ✅ Good selectors
cy.getByRole("button", { name: "Submit" }).click();
cy.getByLabel("Email address").type("user@example.com");
cy.get('[data-testid="email-input"]').type("user@example.com");
```

## Common Pitfalls

- **Flaky Tests**: Use proper waits, not fixed timeouts
- **Slow Tests**: Mock external APIs, use parallel execution
- **Over-Testing**: Don't test every edge case with E2E
- **Coupled Tests**: Tests should not depend on each other
- **Poor Selectors**: Avoid CSS classes and nth-child
- **No Cleanup**: Clean up test data after each test
```

## unit-test (852-unit-test-gen)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/unit-test-gen
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/852-unit-test-gen/1881-unit-test
- الوصف: Generate unit tests with edge cases

```markdown
# unit-test-gen

Generate unit tests with edge cases.

## Tools Available

- **Read** — Read files from the filesystem
- **Write** — Write files to the filesystem
- **Edit** — Make targeted edits to existing files
- **Bash** — Execute shell commands
- **Grep** — Search file contents with regex
- **Glob** — Find files by pattern matching

## Usage

Invoke the `unit-test` skill to Generate unit tests with edge cases. The skill will analyze the relevant codebase context and generate appropriate output.
```

## qa/e2e-playwright (1369-boss)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/echoVic/boss-skill
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1369-boss/3147-boss/skills/qa/e2e-playwright
- الوصف: Playwright E2E 测试完整方法论，涵盖项目初始化、Page Object Model、认证复用、API Mock、视觉回归、多浏览器测试、CI 集成和调试技巧

```markdown
# Playwright E2E 测试方法论

## 适用场景

- Web 项目需要编写端到端测试
- 门禁（Gate 1）要求 E2E 测试通过
- 需要覆盖关键用户流程的自动化验证
- 需要多浏览器/多视口兼容性验证
- 需要视觉回归测试

---

## 1. 项目初始化

### 1.1 安装

```bash
# 新项目初始化（推荐）
npm init playwright@latest

# 已有项目添加
npm install -D @playwright/test
npx playwright install
```

### 1.2 配置文件（`playwright.config.ts`）

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  // 测试产物目录
  outputDir: './e2e/test-results',

  // 全局超时
  timeout: 30_000,
  expect: { timeout: 5_000 },

  // 并行执行
  fullyParallel: true,
  workers: process.env.CI ? 1 : undefined,

  // 失败重试（CI 中重试一次减少 flaky）
  retries: process.env.CI ? 1 : 0,

  // 报告
  reporter: [
    ['html', { outputFolder: './e2e/playwright-report' }],
    ['json', { outputFile: './e2e/test-results/results.json' }],
    // CI 中额外输出到 stdout
    ...(process.env.CI ? [['github'] as const] : []),
  ],

  // 全局配置
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    // 失败时自动截图
    screenshot: 'only-on-failure',
    // 失败时录制 trace
    trace: 'on-first-retry',
    // 失败时录制视频
    video: 'on-first-retry',
  },

  // 多浏览器 + 移动端视口
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 13'] } },
  ],

  // 开发服务器自动启动
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
```

**关键配置说明**：

| 配置项 | 作用 | 建议值 |
|--------|------|--------|
| `fullyParallel` | 测试文件间并行执行 | `true` |
| `workers` | 并行 worker 数 | CI 为 1，本地默认 |
| `retries` | 失败重试次数 | CI 为 1，本地为 0 |
| `trace` | 失败时生成可视化时间线 | `on-first-retry` |
| `webServer` | 自动启动开发服务器 | 必须配置 |

### 1.3 目录结构

```
e2e/
├── playwright.config.ts        # 配置文件（或放在项目根目录）
├── fixtures/                   # 自定义 fixtures
│   ├── base.ts                 # 扩展 base test
│   └── auth.ts                 # 认证 fixture
├── pages/                      # Page Object Models
│   ├── login.page.ts
│   ├── dashboard.page.ts
│   └── components/             # 可复用组件 POM
│       ├── navbar.component.ts
│       └── modal.component.ts
├── specs/                      # 测试用例
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── register.spec.ts
│   ├── dashboard/
│   │   └── dashboard.spec.ts
│   └── crud/
│       └── user-management.spec.ts
├── helpers/                    # 测试工具
│   ├── seed.ts                 # 数据种子
│   └── cleanup.ts              # 数据清理
├── test-results/               # 测试产物（gitignore）
└── playwright-report/          # HTML 报告（gitignore）
```

---
```

## qa/e2e-playwright (1369-boss)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/echoVic/boss-skill
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1369-boss/3164-qa-e2e-playwright
- الوصف: Playwright E2E 测试完整方法论，涵盖项目初始化、Page Object Model、认证复用、API Mock、视觉回归、多浏览器测试、CI 集成和调试技巧

```markdown
# Playwright E2E 测试方法论

## 适用场景

- Web 项目需要编写端到端测试
- 门禁（Gate 1）要求 E2E 测试通过
- 需要覆盖关键用户流程的自动化验证
- 需要多浏览器/多视口兼容性验证
- 需要视觉回归测试

---

## 1. 项目初始化

### 1.1 安装

```bash
# 新项目初始化（推荐）
npm init playwright@latest

# 已有项目添加
npm install -D @playwright/test
npx playwright install
```

### 1.2 配置文件（`playwright.config.ts`）

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  // 测试产物目录
  outputDir: './e2e/test-results',

  // 全局超时
  timeout: 30_000,
  expect: { timeout: 5_000 },

  // 并行执行
  fullyParallel: true,
  workers: process.env.CI ? 1 : undefined,

  // 失败重试（CI 中重试一次减少 flaky）
  retries: process.env.CI ? 1 : 0,

  // 报告
  reporter: [
    ['html', { outputFolder: './e2e/playwright-report' }],
    ['json', { outputFile: './e2e/test-results/results.json' }],
    // CI 中额外输出到 stdout
    ...(process.env.CI ? [['github'] as const] : []),
  ],

  // 全局配置
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    // 失败时自动截图
    screenshot: 'only-on-failure',
    // 失败时录制 trace
    trace: 'on-first-retry',
    // 失败时录制视频
    video: 'on-first-retry',
  },

  // 多浏览器 + 移动端视口
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 13'] } },
  ],

  // 开发服务器自动启动
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
```

**关键配置说明**：

| 配置项 | 作用 | 建议值 |
|--------|------|--------|
| `fullyParallel` | 测试文件间并行执行 | `true` |
| `workers` | 并行 worker 数 | CI 为 1，本地默认 |
| `retries` | 失败重试次数 | CI 为 1，本地为 0 |
| `trace` | 失败时生成可视化时间线 | `on-first-retry` |
| `webServer` | 自动启动开发服务器 | 必须配置 |

### 1.3 目录结构

```
e2e/
├── playwright.config.ts        # 配置文件（或放在项目根目录）
├── fixtures/                   # 自定义 fixtures
│   ├── base.ts                 # 扩展 base test
│   └── auth.ts                 # 认证 fixture
├── pages/                      # Page Object Models
│   ├── login.page.ts
│   ├── dashboard.page.ts
│   └── components/             # 可复用组件 POM
│       ├── navbar.component.ts
│       └── modal.component.ts
├── specs/                      # 测试用例
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── register.spec.ts
│   ├── dashboard/
│   │   └── dashboard.spec.ts
│   └── crud/
│       └── user-management.spec.ts
├── helpers/                    # 测试工具
│   ├── seed.ts                 # 数据种子
│   └── cleanup.ts              # 数据清理
├── test-results/               # 测试产物（gitignore）
└── playwright-report/          # HTML 报告（gitignore）
```

---
```
