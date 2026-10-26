# مصادر «الإتاحة WCAG» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## pf-a11y-keyboard (2999-pf-a11y)

- الترخيص: **MIT**  ·  الأصل: https://github.com/rh-uxd/ai-helpers/tree/e8cca17430a8ccb062ed1878073165417a081b34/plugins/patternfly/pf-a11y
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2999-pf-a11y/12804-pf-a11y-keyboard
- الوصف: Test keyboard accessibility of PatternFly UIs via live browser interaction. Use when validating keyboard navigation, focus management, or interaction patterns in a running application.

```markdown
Test keyboard navigation, focus management, and interaction patterns in a running PatternFly application using live browser automation.

This skill is not a complete replacement for manual keyboard testing. It covers common, well-defined keyboard accessibility criteria, but manual testing should still be conducted for complex, dynamic, or uncommon UI patterns that may not be fully exercised by automated interaction.

## Requirements

This skill requires **Playwright MCP** for live browser interaction. If Playwright MCP tools are not available, stop and inform the user:

> **Playwright MCP is required for keyboard accessibility testing.**
> This skill tests keyboard interactions in a live browser and cannot operate without Playwright MCP.
> See the Playwright MCP documentation for installation instructions.

## Input

| Source | Required | Description |
|--------|----------|-------------|
| URL | Yes | URL to a running application (localhost or deployed) |
| Focus area | No | Specific component, page region, or interaction flow to prioritize |

The URL may point to a full consumer application or an isolated component demo (Storybook, PatternFly docs example, local dev server for a library repo like patternfly-react or chatbot). Determine the context from the page content:

- **Full application**: All criteria apply. Recommendations should suggest PatternFly components and props that resolve violations.
- **Isolated component demo**: Page-level criteria (skip navigation) may be N/A. Recommendations should address the component implementation itself — the fix lives in the component's source code, not in how a consumer uses it.

If the user provides a focus area, test that area first but still check page-level criteria (skip navigation, sequential tab order) across the full page when applicable.

## Criteria

Load these reference files from `$CLAUDE_SKILL_DIR`:

- **`references/keyboard-criteria.md`** — General keyboard accessibility criteria with expected behaviors, test procedures, and common violations. All criteria apply unless explicitly not applicable to the page (e.g., no modals present means the focus trapping criterion is N/A).
- **`references/component-specifics.md`** — Keyboard behavior expectations for specific PatternFly components (and similar custom implementations). Apply these when a matching component is identified on the page during baseline inspection.

## Workflow

### Step 0 — Prerequisites and setup

1. Verify Playwright MCP tools are available. If not, stop with the setup message above.
2. Navigate to the provided URL using Playwright. Wait for full page load.
3. Set viewport to desktop dimensions (1440 x 900).
4. Capture a baseline screenshot of the loaded page.

### Step 1 — Baseline inspection
```

## accessibility-and-inclusive-visualization (2690-build-web-data-visualization)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/build-web-data-visualization
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2690-build-web-data-visualization/10318-accessibility-and-inclusive-visualizatio
- الوصف: Make data visualizations accessible and inclusive. Use when the user needs chart or diagram accessibility guidance, text alternatives for complex visuals, color and contrast review, keyboard support, reduced-motion behavior for animation or parallax, or an accessibility QA workflow for exported figures, UML-like diagrams, and dashboards.

```markdown
# Accessibility and Inclusive Visualization

## Overview

Use this skill when a visualization must be understandable by more people, in more contexts, with more assistive needs. Accessibility is not a post-processing step. It shapes chart selection, color, labeling, interaction, fallback text, and export strategy.

Default assumption: every important visualization should have a non-visual path to the key insight, whether through surrounding text, direct labels, data tables, or formal text alternatives.

## Working Pattern

1. Identify whether the chart is exploratory, explanatory, interactive, or exported.
2. Decide which information must remain available without hover, color discrimination, pointer precision, expanded panels, private persisted state, permission-gated capabilities, or a strong connection.
3. If the story uses generated imagery, illustration, WebGL, particles, 3D, maps, scrollytelling, parallax, or animation, separate what the asset shows from what the data proves.
4. If Codex image generation was used for a layout, figure, page-integration, asset, or key-frame concept, verify that the large-screen and mobile concept images were shown with concise plan and interaction bullets, the user approved the generated design set before project changes or implementation code began, and the semantic design contract from `../../references/foundations/meaning-preserving-visual-design-workflow.md` exists: the accessible path must preserve the same claim, caveat, source context, evidence hierarchy, locked layout elements, mobile continuation, and interaction meaning as the visual design.
5. If the view is a UML-like, ERD, state machine, workflow, dependency, or architecture diagram, preserve a text outline of nodes, groups, relationships, and selected paths; use `../uml-and-software-architecture-visualization/SKILL.md` for diagram-specific semantics.
6. Use `../../references/foundations/mobile-first-responsive-visualization.md` to verify touch targets, drag alternatives, keyboard-open visual viewport behavior, main-visualization visibility, spotty-connection states, and fallbacks for AR, camera, motion, vibration, notifications, and geolocation.
7. Provide direct labels, strong contrast, redundant encodings, keyboard paths, reduced-motion alternatives, accessible disclosure controls, and text alternatives.
8. For interactive visualizations, check that shared URLs, saved views, refresh, and back/forward navigation preserve the same accessible state summaries as the visual surface.
9. Test both the chart or diagram and the surrounding narrative.

## Output Expectations

- Name the accessibility risks specific to the chart, not just generic WCAG items.
- Provide fallback strategies for screen readers, PDFs, and static exports.
```

## accessibility-implementation (2133-accessibility-plugin)

- الترخيص: **MIT**  ·  الأصل: https://github.com/laurigates/claude-plugins/tree/9caa2be8e7b4b35823e4154c610e3846af05635c/accessibility-plugin
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2133-accessibility-plugin/7559-accessibility-implementation
- الوصف: WCAG 2.1/2.2 compliance, ARIA patterns, keyboard nav, focus management, a11y testing. Use when implementing accessible components or user mentions WCAG/ARIA/screen readers.

```markdown
# Accessibility Implementation

Technical implementation of WCAG guidelines, ARIA patterns, and assistive technology support.

## When to Use This Skill

| Use this skill when... | Use design-tokens instead when... |
|---|---|
| Implementing WCAG 2.1/2.2 success criteria in code | Setting up CSS custom properties or theme systems |
| Adding ARIA roles, states, or live regions | Defining semantic colour tokens used by themes |
| Wiring keyboard navigation, focus traps, or skip links | Organizing primitive/semantic/component token tiers |
| Auditing components with axe-core, jest-axe, or Playwright | Implementing light/dark mode token overrides |

## Core Expertise

- **WCAG Compliance**: Implementing WCAG 2.1/2.2 success criteria in code
- **ARIA Patterns**: Correct usage of roles, states, and properties
- **Keyboard Navigation**: Focus management, key handlers, logical tab order
- **Screen Readers**: Content structure, announcements, live regions
- **Testing**: Automated and manual accessibility testing

## WCAG Quick Reference

### Level A (Must Have)

| Criterion | Implementation |
|-----------|----------------|
| 1.1.1 Non-text Content | `alt` for images, labels for inputs |
| 1.3.1 Info and Relationships | Semantic HTML, ARIA relationships |
| 2.1.1 Keyboard | All interactive elements keyboard accessible |
| 2.4.1 Bypass Blocks | Skip links, landmarks |
| 4.1.2 Name, Role, Value | ARIA labels, roles for custom widgets |

### Level AA (Should Have)

| Criterion | Implementation |
|-----------|----------------|
| 1.4.3 Contrast (Minimum) | 4.5:1 text, 3:1 large text |
| 1.4.11 Non-text Contrast | 3:1 for UI components |
| 2.4.6 Headings and Labels | Descriptive, hierarchical headings |
| 2.4.7 Focus Visible | Visible focus indicator (2px+ outline) |

## Best Practices

### Semantic HTML First
Use native HTML elements before ARIA. A `<button>` is better than `<div role="button">`.

### Don't Override Default Behavior
Native elements have built-in accessibility. Don't break it with JavaScript.

### Test with Real Users
Automated tools catch ~30% of issues. Manual testing with assistive technology is essential.

### Provide Multiple Ways
Offer keyboard, mouse, and touch alternatives for all interactions.

## References

- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- axe-core Rules: https://dequeuniversity.com/rules/axe/
- A11y Project Checklist: https://www.a11yproject.com/checklist/

For full ARIA widget patterns, keyboard navigation implementations, testing recipes, common fixes, and CSS utilities, see [REFERENCE.md](REFERENCE.md).
```

## pf-a11y-test-gen (2999-pf-a11y)

- الترخيص: **MIT**  ·  الأصل: https://github.com/rh-uxd/ai-helpers/tree/e8cca17430a8ccb062ed1878073165417a081b34/plugins/patternfly/pf-a11y
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2999-pf-a11y/12805-pf-a11y-test-gen
- الوصف: Generate accessibility test files for any frontend framework covering ARIA attributes, keyboard interaction, and focus management. Use when adding a11y test coverage or writing ARIA/keyboard/focus tests.

```markdown
Generate dedicated accessibility test files for UI components. Framework-agnostic — works with any frontend setup. Produces persistent test artifacts that run in CI. Complements `pf-test-gen` (general unit tests), `pf-a11y-audit` (static code analysis), and `pf-a11y-keyboard` (live browser testing).

## Input

| Source | Required | Description |
|--------|----------|-------------|
| Component/module file | Yes | Path to the component or UI module to generate a11y tests for |
| Focus area | No | Specific a11y category to prioritize: `aria`, `keyboard`, `focus`, or `axe` |

Read the component source before generating tests.

## Context Detection

### Phase 1 — Framework detection

Determine the frontend framework from the component source and project dependencies. The framework determines the test rendering approach. If it cannot be determined, ask the user.

### Phase 2 — Audience

Determine if the codebase is a PatternFly org repo or a consumer/standalone project.

**PatternFly developer** (signals: `@patternfly` in package name, `packages/` with PF component source, `patternfly` GitHub org) — test that ARIA attributes are correctly wired to component props, components expose the right a11y API surface, and default accessible names are sensible.

**Consumer/standalone** — test that accessible names are explicitly provided, multiple instances have unique labels, and live regions are used for dynamic content.

### Phase 3 — Test library detection

Scan the nearest `package.json` for testing libraries in `devDependencies` and `dependencies`. Look for unit/component testing libraries, test runners, integration/E2E libraries (Cypress, Playwright), and axe-core integrations. Also check for test runner config files.

### Phase 4 — Convention detection

Find existing test files near the component. Analyze file naming, test structure, a11y test organization (separate files vs. inline describe blocks), query patterns, and setup conventions. Mirror all detected conventions in generated tests.

## Test Library Evaluation

Load `$CLAUDE_SKILL_DIR/references/test-library-matrix.md` and apply its decision rules to assign a11y test categories to detected libraries.

- Unit test libraries handle ARIA attributes and basic keyboard activation
- axe-core integrations handle automated violation scans
- Cypress/Playwright handles focus management, focus traps, and complex keyboard flows
- Generate at most **2 test files** per component (one per library target)

If only one library is available, all applicable tests go to that library with coverage limitations noted in the gap report.

## A11y Test Categories

Load sibling reference files from `$CLAUDE_SKILL_DIR` selectively based on what the component needs:
```

## a11y-audit (149-a11y-audit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/engineering-team/a11y-audit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/149-a11y-audit/492-a11y-audit
- الوصف: Accessibility audit skill for scanning, fixing, and verifying WCAG 2.2 Level A and AA compliance across React, Next.js, Vue, Angular, Svelte, and plain HTML codebases. Use when auditing accessibility, fixing a11y violations, checking color contrast, generating compliance reports, or integrating accessibility checks into CI/CD pipelines.

```markdown
# Accessibility Audit

WCAG 2.2 Accessibility Audit and Remediation Skill

## Description

The a11y-audit skill provides a complete accessibility audit pipeline for modern web applications. It implements a three-phase workflow -- Scan, Fix, Verify -- that identifies WCAG 2.2 Level A and AA violations, generates exact fix code per framework, and produces stakeholder-ready compliance reports.

For every violation it finds, it provides the precise before/after code fix tailored to your framework (React, Next.js, Vue, Angular, Svelte, or plain HTML).

**What this skill does:**

1. **Scans** your codebase for every WCAG 2.2 Level A and AA violation, categorized by severity (Critical, Major, Minor)
2. **Fixes** each violation with framework-specific before/after code patterns
3. **Verifies** that fixes resolve the original violations and introduces no regressions
4. **Reports** findings in a structured format suitable for developers, PMs, and compliance stakeholders
5. **Integrates** into CI/CD pipelines to prevent accessibility regressions

## Features

| Feature | Description |
|---------|-------------|
| **Full WCAG 2.2 Scan** | Checks all Level A and AA success criteria across your codebase |
| **Framework Detection** | Auto-detects React, Next.js, Vue, Angular, Svelte, or plain HTML |
| **Severity Classification** | Categorizes each violation as Critical, Major, or Minor |
| **Fix Code Generation** | Produces before/after code diffs for every issue |
| **Color Contrast Checker** | Validates foreground/background pairs against AA and AAA ratios |
| **Compliance Reporting** | Generates stakeholder reports with pass/fail summaries |
| **CI/CD Integration** | GitHub Actions, GitLab CI, Azure DevOps pipeline configs |
| **Keyboard Navigation Audit** | Detects missing focus management and tab order issues |
| **ARIA Validation** | Checks for incorrect, redundant, or missing ARIA attributes |

### Severity Definitions

| Severity | Definition | Example | SLA |
|----------|-----------|---------|-----|
| **Critical** | Blocks access for entire user groups | Missing alt text, no keyboard access to navigation | Fix before release |
| **Major** | Significant barrier that degrades experience | Insufficient color contrast, missing form labels | Fix within current sprint |
| **Minor** | Usability issue that causes friction | Redundant ARIA roles, suboptimal heading hierarchy | Fix within next 2 sprints |

## Usage

### Quick Start

```bash
# Scan entire project
python scripts/a11y_scanner.py /path/to/project

# Scan with JSON output for tooling
python scripts/a11y_scanner.py /path/to/project --json

# Check color contrast for specific values
python scripts/contrast_checker.py --fg "#777777" --bg "#ffffff"

# Check contrast across a CSS/Tailwind file
```

## pf-a11y-keyboard (2998-patternfly)

- الترخيص: **MIT**  ·  الأصل: https://github.com/rh-uxd/ai-helpers/tree/e8cca17430a8ccb062ed1878073165417a081b34/plugins/patternfly
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2998-patternfly/12754-pf-a11y-keyboard
- الوصف: Test keyboard accessibility of PatternFly UIs via live browser interaction. Use when validating keyboard navigation, focus management, or interaction patterns in a running application.

```markdown
Test keyboard navigation, focus management, and interaction patterns in a running PatternFly application using live browser automation.

This skill is not a complete replacement for manual keyboard testing. It covers common, well-defined keyboard accessibility criteria, but manual testing should still be conducted for complex, dynamic, or uncommon UI patterns that may not be fully exercised by automated interaction.

## Requirements

This skill requires **Playwright MCP** for live browser interaction. If Playwright MCP tools are not available, stop and inform the user:

> **Playwright MCP is required for keyboard accessibility testing.**
> This skill tests keyboard interactions in a live browser and cannot operate without Playwright MCP.
> See the Playwright MCP documentation for installation instructions.

## Input

| Source | Required | Description |
|--------|----------|-------------|
| URL | Yes | URL to a running application (localhost or deployed) |
| Focus area | No | Specific component, page region, or interaction flow to prioritize |

The URL may point to a full consumer application or an isolated component demo (Storybook, PatternFly docs example, local dev server for a library repo like patternfly-react or chatbot). Determine the context from the page content:

- **Full application**: All criteria apply. Recommendations should suggest PatternFly components and props that resolve violations.
- **Isolated component demo**: Page-level criteria (skip navigation) may be N/A. Recommendations should address the component implementation itself — the fix lives in the component's source code, not in how a consumer uses it.

If the user provides a focus area, test that area first but still check page-level criteria (skip navigation, sequential tab order) across the full page when applicable.

## Criteria

Load these reference files from `$CLAUDE_SKILL_DIR`:

- **`references/keyboard-criteria.md`** — General keyboard accessibility criteria with expected behaviors, test procedures, and common violations. All criteria apply unless explicitly not applicable to the page (e.g., no modals present means the focus trapping criterion is N/A).
- **`references/component-specifics.md`** — Keyboard behavior expectations for specific PatternFly components (and similar custom implementations). Apply these when a matching component is identified on the page during baseline inspection.

## Workflow

### Step 0 — Prerequisites and setup

1. Verify Playwright MCP tools are available. If not, stop with the setup message above.
2. Navigate to the provided URL using Playwright. Wait for full page load.
3. Set viewport to desktop dimensions (1440 x 900).
4. Capture a baseline screenshot of the loaded page.

### Step 1 — Baseline inspection
```
