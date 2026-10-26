# مصادر «التدقيق الأمني STRIDE» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## security-audit (2582-security-audit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mqmalagris/agent-skills/tree/73cecb15d57f707e0f6568674dfa13ec37d47a87/skills/security-audit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2582-security-audit/9949-security-audit
- الوصف: Focused security review of a CHANGE (a diff, a branch, a PR), layered on the wstg-security-testing skill. Finds HIGH-CONFIDENCE, concretely exploitable vulnerabilities the change newly introduces (injection, broken authn/authz, secrets and data exposure, unsafe deserialization, crypto misuse, SSRF) and audits dependencies when a lockfile moved, using the repo's own package manager. Runs as Check 7

```markdown
# Security Audit

> **No em-dashes.** Nothing this skill writes may contain an em-dash; use a comma, colon, or parentheses instead.

A focused security pass over a change. The job is narrow on purpose: find the vulnerabilities a senior security engineer would confidently raise in review, and stay silent about everything else. A review that flags twenty theoretical issues gets ignored; one that flags the two real ones gets acted on. Noise is the enemy, not thoroughness.

**This skill layers on top of `wstg-security-testing` (`/wstg`).** That skill carries the full OWASP WSTG map: 12 categories, ~109 test cases, detection payloads, and a diff-review mode. This skill adds the two things WSTG alone does not give you: the **confidence gate** and the **false-positive precedents** that keep the report credible. Use WSTG for coverage (what to look for and its ID), use this skill's gate to decide what actually gets reported.

It runs two ways:

- **As Check 7 of `/implementation-review`**, a parallel subagent whose brief pulls in this skill's content. Diff-scoped, fast.
- **Standalone** (`/security-audit`), a deliberate pass on demand.

---

## When this is the wrong skill

**This skill reviews a change. It does not audit a codebase.** If the ask is repo-wide ("audit this project", "is my app secure", "find every IDOR", "auditoria de segurança"), stop and run **`/wstg` mode 2** instead, which carries the systematic protocol in `reference/CODEBASE-AUDIT.md`.

The distinction is not cosmetic, three things here actively break on a codebase-wide ask:

| This skill | Why it fails a posture audit |
|---|---|
| Scope resolves to a diff | No diff to resolve, so it reviews nothing and reports clean on a vulnerable repo |
| "Not pre-existing issues the diff merely sits near" | Every finding in an audit is pre-existing, that is the point |
| Precedent 9, "not the absence of defense-in-depth" | Missing RLS, a missing tenant filter, and an unvalidated secret default are all absences |

Those rules are correct **for change review**, where noise trains the reader to skip the report. They are wrong for a posture audit, where absence is the finding. `CODEBASE-AUDIT.md` states its own overrides explicitly; do not carry this file's precedents into it.

---

## The one rule that matters

**Only report a finding you can attach a concrete exploit path to, and only when you are over 80% confident it is actually exploitable.** Everything else here serves that rule.

A finding is worth reporting when you can name the untrusted input, trace it to the dangerous sink, and describe the attack in a sentence. If you cannot do that, it is a hunch, and a hunch in a security report is noise that trains the reader to skip the whole thing.

Score every candidate before reporting it:
```

## generating-security-audit-reports (1931-security-audit-reporter)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/security/security-audit-reporter
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1931-security-audit-reporter/7071-generating-security-audit-reports
- الوصف: Generate comprehensive security audit reports for applications and systems.

```markdown
# Generating Security Audit Reports

## Overview

Aggregate vulnerability scan results, configuration analyses, and compliance assessments into a structured, auditor-ready security report. Map every finding to a CVSS severity, applicable compliance control (PCI-DSS, HIPAA, SOC 2, GDPR), and a prioritized remediation timeline.

## Prerequisites

- Vulnerability scanner outputs (Nmap, Nessus, OpenVAS, OWASP ZAP) available in `${CLAUDE_SKILL_DIR}/security/`
- Application and infrastructure configuration files accessible
- SAST/DAST tool results (e.g., Semgrep, Snyk, Trivy, Bandit)
- Applicable compliance framework documentation identified (PCI-DSS v4.0, HIPAA Security Rule, SOC 2 TSC, GDPR)
- Write permissions for report output directory `${CLAUDE_SKILL_DIR}/reports/`

## Instructions

1. Inventory all available security data sources by scanning `${CLAUDE_SKILL_DIR}/security/` for scanner outputs, log files, and configuration exports.
2. Parse vulnerability findings and normalize severity using CVSS 3.1 base scores: Critical (9.0-10.0), High (7.0-8.9), Medium (4.0-6.9), Low (0.1-3.9).
3. Cross-reference each finding against applicable compliance controls. Map to specific PCI-DSS requirements (e.g., Req 6.5 for injection flaws), HIPAA safeguards, or SOC 2 Common Criteria.
4. Deduplicate findings across scanners and merge related vulnerabilities into consolidated entries with all affected assets listed.
5. Classify access control weaknesses, encryption gaps, and authentication deficiencies into separate report sections.
6. Generate an executive summary including total findings by severity, overall risk score, and top-5 critical remediation priorities.
7. Build a detailed findings table: finding ID, CWE number, affected component, CVSS score, compliance mapping, remediation steps, and evidence links.
8. Produce a compliance status matrix showing pass/fail/partial for each applicable standard requirement.
9. Create remediation recommendations with effort estimates (hours), priority ranking, and suggested timelines.
10. Format the final report as Markdown to `${CLAUDE_SKILL_DIR}/reports/security-audit-YYYYMMDD.md`. Optionally produce JSON for Jira/ServiceNow import.

See `${CLAUDE_SKILL_DIR}/references/implementation.md` for the detailed four-phase implementation workflow.

## Output

- **Audit Report**: `${CLAUDE_SKILL_DIR}/reports/security-audit-YYYYMMDD.md` containing executive summary, detailed findings, compliance matrix, and remediation plan
- **Findings JSON**: Machine-readable findings for ticketing system import
- **Compliance Matrix**: Per-requirement pass/fail/partial status for each applicable framework
- **Remediation Backlog**: Prioritized list with effort estimates and owner assignments

## Error Handling

| Error | Cause | Solution |
```

## analyzing-security-headers (1932-security-headers-analyzer)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/security/security-headers-analyzer
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1932-security-headers-analyzer/7072-analyzing-security-headers
- الوصف: Analyze HTTP security headers of web domains to identify vulnerabilities

```markdown
# Analyzing Security Headers

## Overview

Evaluate HTTP response headers for web applications against OWASP Secure Headers Project recommendations and browser security baselines. Identify missing, misconfigured, or information-leaking headers across both HTTP and HTTPS responses.

## Prerequisites

- Target URL or domain name accessible over the network
- Authorization to perform HTTP requests against the target domain
- Network connectivity for both HTTP and HTTPS protocols
- Optional: write access to `${CLAUDE_SKILL_DIR}/security-reports/` for persisting results

## Instructions

1. Accept the target domain. If only a domain name is provided, default to `https://`. For batch analysis, accept a newline-separated list.
2. Fetch response headers using `WebFetch` for both HTTP and HTTPS endpoints. Record the full redirect chain and final destination URL.
3. Evaluate **critical headers** -- flag any that are missing or misconfigured:
   - `Strict-Transport-Security`: require `max-age>=31536000`, `includeSubDomains`, and preload eligibility
   - `Content-Security-Policy`: check for `unsafe-inline`, `unsafe-eval`, overly broad `default-src`, and missing `frame-ancestors`
   - `X-Frame-Options`: require `DENY` or `SAMEORIGIN`
   - `X-Content-Type-Options`: require `nosniff`
   - `Permissions-Policy`: verify camera, microphone, geolocation restrictions
4. Evaluate **important headers** -- report status and recommendations:
   - `Referrer-Policy`: recommend `strict-origin-when-cross-origin` or `no-referrer`
   - `Cross-Origin-Embedder-Policy` (COEP), `Cross-Origin-Opener-Policy` (COOP), `Cross-Origin-Resource-Policy` (CORP)
5. Check for **information disclosure** -- flag `Server`, `X-Powered-By`, `X-AspNet-Version`, and any header revealing technology stack or version numbers.
6. Inspect cookie attributes on `Set-Cookie` headers: verify `Secure`, `HttpOnly`, `SameSite=Lax|Strict`, and `__Host-`/`__Secure-` prefix usage.
7. Calculate a security grade: A+ (95-100), A (85-94), B (75-84), C (65-74), D (50-64), F (<50) based on weighted presence and correctness of each header.
8. Generate per-header remediation directives with configuration examples for Nginx, Apache, and Cloudflare.

See `${CLAUDE_SKILL_DIR}/references/implementation.md` for the five-phase implementation workflow.

## Output

- **Headers Analysis Report**: overall grade, per-header status (present/missing/misconfigured), and risk impact
- **Remediation Checklist**: prioritized fixes with server configuration snippets
- **Cookie Security Assessment**: attribute compliance for each `Set-Cookie` header
- **Comparison Table**: side-by-side HTTP vs. HTTPS header differences

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
```

## security-audit (2664-project)

- الترخيص: **BSD-3-Clause**  ·  الأصل: https://github.com/neuromechanist/research-skills/tree/f0219bde233abb44d8a0c5d73f41ea27073e1493/plugins/project
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2664-project/10142-security-audit
- الوصف: This skill should be used when the user says \"security audit\", \"check for vulnerabilities\", \"security review\", \"harden project\", \"dependency audit\", \"credential scan\", \"check for secrets\", \"scan for secrets\", \"OWASP review\", \"security checklist\", \"audit dependencies\", \"find vulnerabilities\", or wants to review their project for security issues, exposed credentials, or vulne

```markdown
# Security Audit

Systematic security review of a project covering dependency vulnerabilities, credential exposure, common code vulnerabilities, and configuration hardening.

## When to Use

- Before a release or deployment
- After adding new dependencies
- When onboarding to a new codebase
- Periodic security reviews
- After receiving a vulnerability report

## Audit Checklist

### 1. Credential and Secret Scanning

Check for exposed secrets in the codebase:

```bash
# Check for common secret patterns in tracked files
git grep -n -i -E '(api_key|apikey|secret|password|token|credential|private_key)\s*[:=]' -- ':!*.md' ':!*.lock'

# Check for .env files tracked in git
git ls-files | grep -i '\.env'

# Check .gitignore covers sensitive files
for f in .env .env.local credentials.json secrets.yaml; do
  git check-ignore "$f" 2>/dev/null || echo "WARNING: $f not in .gitignore"
done
```

Files that must never be committed:
- `.env`, `.env.*` (environment variables)
- `credentials.json`, `service-account.json` (cloud credentials)
- `*.pem`, `*.key` (private keys)
- `*.p12`, `*.pfx` (certificates with private keys)

### 2. Dependency Vulnerability Scan

**Python:**
```bash
uv run pip-audit
```

**JavaScript/TypeScript:**
```bash
bun pm audit
# or check with npm for broader database
npm audit --omit=dev
```

**Go:**
```bash
govulncheck ./...
```

Review results against the severity rubric (shared with the
dependency-auditor agent):

- Critical: exploitable now or actively exploited (leaked live credential,
  known-exploited CVE in a reachable path). Must fix before release; blocks
  release-prep.
- High: known vulnerability with a plausible attack path. Fix before the next
  release.
- Medium: vulnerability with mitigating factors, or a major-version lag on a
  security-relevant package. Fix within the sprint.
- Low: outdated without known vulnerabilities; license concerns to review.
  Track in backlog.

### 3. Code Vulnerability Patterns

Scan for common vulnerability patterns:

**SQL Injection:**
```bash
# Look for string interpolation in SQL
grep -rn 'f".*SELECT\|f".*INSERT\|f".*UPDATE\|f".*DELETE' --include='*.py'
grep -rn "format.*SELECT\|format.*INSERT" --include='*.py'
```

**Command Injection:**
```bash
# Look for shell=True or unsanitized subprocess calls
grep -rn 'shell=True\|os\.system\|subprocess\.call.*shell' --include='*.py'
grep -rn 'exec(\|eval(' --include='*.py' --include='*.js' --include='*.ts'
```

**XSS (Cross-Site Scripting):**
```bash
# Look for dangerouslySetInnerHTML or unescaped output
grep -rn 'dangerouslySetInnerHTML\|innerHTML\s*=' --include='*.tsx' --include='*.jsx' --include='*.ts' --include='*.js'
```

**Path Traversal:**
```bash
```

## octopus-security-audit (2673-claude-octopus)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/nyldn/claude-octopus
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2673-claude-octopus/10190-octopus-security-audit
- الوصف: OWASP compliance, vulnerability scanning, and adversarial red team testing — use for security reviews

```markdown
> **Host: Codex CLI** — This skill was designed for Claude Code and adapted for Codex.
> Cross-reference commands use installed skill names in Codex rather than `/octo:*` slash commands.
> Use the active Codex shell and subagent tools. Do not claim a provider, model, or host subagent is available until the current session exposes it.
> For host tool equivalents, see `skills/blocks/codex-host-adapter.md`.


## Execution Contract (MANDATORY - CANNOT SKIP)

This generated Codex skill preserves an enforced workflow contract from the source skill.

**PROHIBITED:**
- Do not summarize, simulate, or skip the referenced workflow command when this skill requires execution.
- Do not claim provider output or validation artifacts exist without checking the actual files or command output.
- Do not continue silently when a required provider, command, or host capability is unavailable; report the unavailable dependency and use a supported fallback.


# Security Audit Skill

**Your first output line MUST be:** `🐙 **CLAUDE OCTOPUS ACTIVATED** - Security Audit`

Invokes the security-auditor persona for thorough security analysis during the `ink` (deliver) phase. Supports both quick OWASP scanning and full adversarial red/blue team testing.

## Usage

```bash
# Quick scan via security-auditor persona
${HOME}/.claude-octopus/plugin/scripts/orchestrate.sh spawn security-auditor "Scan for SQL injection vulnerabilities"

# Adversarial red team via squeeze workflow
${HOME}/.claude-octopus/plugin/scripts/orchestrate.sh squeeze "Security audit the authentication module"

# Via auto-routing (detects security intent)
${HOME}/.claude-octopus/plugin/scripts/orchestrate.sh auto "security audit the payment processing module"
```

## Modes (Auto-Detected)

| Mode | Auto-Trigger | Confidence Gate | Scope |
|------|-------------|----------------|-------|
| **Quick** (default) | Standard security scan, no sensitive files in diff | 8/10 — only high-confidence findings | Changed files only |
| **Deep** (auto-escalated) | Diff touches auth/security/CI files, OR explicit request | 2/10 — flag anything suspicious | Entire codebase |

**Auto-escalation to Deep mode:** The skill automatically switches to Deep mode when ANY of these are true:
- Diff includes files matching: `*auth*`, `*login*`, `*password*`, `*session*`, `*token*`, `*secret*`, `*crypt*`, `*oauth*`, `*saml*`, `*jwt*`, `*permission*`, `*rbac*`, `*acl*`
- Diff includes CI/CD files: `.github/workflows/*`, `Dockerfile*`, `docker-compose*`, `.gitlab-ci*`
- Diff includes dependency files: `package-lock.json`, `yarn.lock`, `Gemfile.lock`, `requirements.txt`, `go.sum`
- The user explicitly says "deep", "full", "comprehensive", or "CSO"

No user action needed — mode detection happens automatically from the git diff context.
```

## river-review-security-audit (3019-river-review)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/s977043/river-review
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3019-river-review/12922-river-review-security-audit
- الوصف: Repository または subsystem を対象に、source-only で明示的なセキュリティ監査を行う entry skill。 通常の PR セキュリティレビューとは分離し、reconnaissance、scope 固定、既存 security skill への委譲、 evidence と unresolved hypothesis、observe-only SecurityAuditCoverage、coverage critic、 structured audit artifact と repeat-run coverage を扱う。target-controlled code は実行しない。

```markdown
# Security Audit Entry

Inspired by Cloudflare's
[security-audit-skill](https://github.com/cloudflare/security-audit-skill),
but implemented as a River Review-native entry skill rather than a vendored audit engine.

This skill is the explicit entry point for repository or subsystem security audit work.
It does not replace `river-review-security`, the normal diff-oriented security review entry.

## When to Use

Use this skill only when the user explicitly asks for a security audit beyond an ordinary PR review.
Typical requests include repository-wide security audit, subsystem security audit, security assessment,
or a bounded source review of a security-sensitive surface.

Do not select this skill for a generic request such as "review this PR for security".
Route that request to `river-review-security`.

## Modes

Select exactly one mode before reviewing.

- `guidance`: use when the user wants methodology, planning, or an audit approach. Explain the method and constraints. Do not claim that audit work was executed.
- `focused`: use when the user names a bounded subsystem, path, component, or security surface. Freeze that scope and review only source evidence inside the boundary.
- `full-audit`: use only when the user explicitly requests repository-wide audit coverage. Perform repository reconnaissance and source review across the repository. Semantic coverage is observe-only and never a safety guarantee.

If the request does not clearly justify `full-audit`, use `focused` or `guidance`.

## Non-negotiable Source-only Policy

Version 0.5.0 is source-only.

Allowed evidence collection:

- file reads
- repository code search
- static diff inspection
- repository metadata and dependency manifests
- configuration and documentation inspection
- static history inspection when it supports source provenance

Prohibited execution:

- package installation or dependency fetching
- target repository build scripts
- target repository test commands
- package lifecycle scripts
- dev servers or application startup
- browsers or emulators that execute target code
- fuzzing or dynamic probes
- requests to production, shared, or external endpoints
- use of ambient credentials to reproduce a finding

If runtime evidence is required but safe execution is unavailable, keep the hypothesis unresolved.
Record the blocker and the minimum validation plan instead of executing target-controlled code.

## Responsibilities

This skill performs entry-level audit coordination only.
It must reuse existing River Review capabilities instead of creating a second workflow engine.

```text
Explicit audit request
  -> mode selection
  -> scope freeze
  -> source reconnaissance
  -> attack-class planning
  -> existing security skills
  -> candidate findings / unresolved hypotheses
```
