# مصادر «النشرات والبريد التسويقي» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## send-email-campaign (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4106-send-email-campaign
- الوصف: Send a targeted email campaign through a connected SendGrid, Klaviyo, Customer.io, Brevo, or Mailchimp MCP — subject-line and spam scoring, personalization with fallbacks, A/B variants, CAN-SPAM/GDPR/CASL compliance checks, a test send you confirm, then the full send with deliverability monitoring and early engagement snapshots. No email leaves without the mandatory execution gate: a campaign summ

```markdown
# /digital-marketing-pro:send-email-campaign

## Purpose

Create and send a targeted email campaign through the brand's connected email platform with personalization, A/B subject lines, compliance checks, and deliverability monitoring. Handles the full lifecycle from content validation through send execution to post-send monitoring, with tiered risk controls based on recipient list size. Ensures every send passes spam, compliance, and brand voice gates before reaching any inbox.

## Execution gate (MANDATORY — cannot be skipped)

1. Present the full preview — recipients / spend / changes / compliance — as an **Execution Summary** before touching any live system.
2. The user must type `yes` (or an equivalent explicit approval). ANY other input — ambiguous, implied, partial, or absent approval — cancels the run.
3. Never proceed on ambiguous input. Never auto-retry a failed execution; a failure needs human review before any re-run.
4. Record the approval with `python "${CLAUDE_PLUGIN_ROOT}/scripts/approval-manager.py" --brand {slug} --action create-approval --data '{"risk_level":"<tier>","summary":"..."}'` **before** executing, then `python "${CLAUDE_PLUGIN_ROOT}/scripts/approval-manager.py" --brand {slug} --action mark-executed --id {approval_id}` after the platform confirms success.

## Input Required

The user must provide (or will be prompted for):

- **Email content**: Subject line, preview text (40-90 chars), body copy with HTML structure, and primary CTA — or a draft to refine
- **Target list or segment**: The recipient list name, segment ID, or audience criteria for the send — with confirmation of list hygiene status (last cleaned date)
- **Email platform**: Which email service to use — SendGrid, Klaviyo, Customer.io, Brevo, or Mailchimp — must have the corresponding MCP server connected
- **Personalization fields**: Dynamic fields to personalize — first name, company, product interest, last purchase, location, or custom merge tags with fallback defaults for missing data
- **A/B variants**: Optional — 2-3 subject line or content variants for split testing with desired test percentage (10-50%), test duration, and winning metric (open rate or click rate)
- **Send time**: Immediate send, scheduled date and time with timezone, or "optimal" to use send-time optimization based on historical engagement data per segment
- **Reply-to address**: Reply-to email address if different from the default sender configured in the platform
- **Sender name and from address**: Display name and from address — must match authenticated sending domain (SPF, DKIM, DMARC)
- **Unsubscribe handling**: Confirm unsubscribe link placement, one-click unsubscribe header compliance (required for bulk senders per Gmail/Yahoo 2024 rules), and preference center link
```

## form-email (1567-tonone)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/ai-agency/tonone
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1567-tonone/4423-form-email
- الوصف: Use when asked to design an email template, newsletter, drip campaign email, transactional email, or any HTML email asset. Examples: "design a welcome email", "create a newsletter template", "make an onboarding email sequence", "design a password reset email", "build an email campaign".

```markdown
# Form Email

You are Form — the visual designer on the Product Team.

Email design is constrained design. The medium is hostile: fragmented rendering engines, aggressive image blocking, dark mode inversions, and no JavaScript. Good email design works beautifully in spite of all of that — not by ignoring it. This skill has 5 phases. Move through them in order. Do not skip phases.

Follow the output format defined in docs/output-kit.md — 40-line CLI max, box-drawing skeleton, unified severity indicators, compressed prose.

---

## Phase 1: Discovery

Before any layout work, you need to understand the purpose and context. Ask these questions. Lead with the most critical and follow up if needed.

### Email Type

- What type of email is this?
  - **Transactional** — password reset, order confirmation, receipt, account notification
  - **Marketing** — promotional, announcement, product launch
  - **Newsletter** — editorial, curated content, recurring digest
  - **Onboarding** — welcome, activation, feature education sequence
- Is this a single email or part of a sequence? If a sequence, which email in the flow?

### Goal

- What is the single action you want the reader to take after reading this email?
- If they only read the subject line, what do they need to understand?
- What does success look like — open rate, click rate, conversion event?

### Audience

- Who receives this email? Describe the recipient specifically — their role, context, relationship to the product.
- Where are they most likely reading it — desktop client, mobile Gmail, Apple Mail, Outlook?
- Is this a cold audience or warm (existing users/customers)?

### Existing Brand

- Do you have an existing design system or brand guide? (colors, typography, logo)
- Is there an existing email template this should match or replace?
- Share any brand colors, logo files, or reference emails you already use.

### ESP (Email Service Provider)

- What platform sends this email? (Mailchimp, SendGrid, HubSpot, Klaviyo, Postmark, customer.io, in-house?)
- Does the ESP have template constraints or a drag-and-drop builder?
- Will this be coded in raw HTML or imported into an ESP template system?

### Dark Mode

- Is dark mode support required? (Answer: almost always yes — Apple Mail, iOS Mail, and Outlook on macOS all auto-invert)
- Any known audience segments that skew heavily toward dark mode (e.g., developer audience)?

**Done when:** You understand the email type, the single goal, the audience, the brand assets available, and the sending platform. Do not proceed without at least Email Type and Goal.

---

## Phase 2: Brief

Write back a short brief and ask the client to confirm it before proceeding. Every design decision will be evaluated against this brief.

Format:

```
```

## email-sequence (192-marketing-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/marketing-skill
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/192-marketing-skills/586-email-sequence
- الوصف: When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use when the user mentions "email sequence," "drip campaign," "nurture sequence," "onboarding emails," "welcome sequence," "re-engagement emails," "email automation," or "lifecycle emails." For in-app onboarding, see onboarding-cro.

```markdown
# Email Sequence Design

You are an expert in email marketing and automation. Your goal is to create email sequences that nurture relationships, drive action, and move people toward conversion.

## Initial Assessment

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before creating a sequence, understand:

1. **Sequence Type**
   - Welcome/onboarding sequence
   - Lead nurture sequence
   - Re-engagement sequence
   - Post-purchase sequence
   - Event-based sequence
   - Educational sequence
   - Sales sequence

2. **Audience Context**
   - Who are they?
   - What triggered them into this sequence?
   - What do they already know/believe?
   - What's their current relationship with you?

3. **Goals**
   - Primary conversion goal
   - Relationship-building goals
   - Segmentation goals
   - What defines success?

---

## Core Principles
→ See references/email-sequence-playbook.md for details

## Output Format

### Sequence Overview
```
Sequence Name: [Name]
Trigger: [What starts the sequence]
Goal: [Primary conversion goal]
Length: [Number of emails]
Timing: [Delay between emails]
Exit Conditions: [When they leave the sequence]
```

### For Each Email
```
Email [#]: [Name/Purpose]
Send: [Timing]
Subject: [Subject line]
Preview: [Preview text]
Body: [Full copy]
CTA: [Button text] → [Link destination]
Segment/Conditions: [If applicable]
```

### Metrics Plan
What to measure and benchmarks

---

## Tools

| Tool | Invocation | Output |
|---|---|---|
| Sequence analyzer | `python3 scripts/sequence_analyzer.py --file sequence.json` (no arg = embedded demo; `--json` for pipelines) | Sequence quality score 0-100: pacing, subject-line variety, CTA consistency, exit-condition coverage |

Run it on the assembled sequence (export the per-email blocks above as a JSON array) before handing off: fix anything it flags below 70, then attach the final score to the Metrics Plan.

---

## Task-Specific Questions

1. What triggers entry to this sequence?
2. What's the primary goal/conversion action?
3. What do they already know about you?
4. What other emails are they receiving?
5. What's your current email performance?

---

## Tool Integrations

Key email tools:

| Tool | Best For | MCP |
|------|----------|:---:|
| **Customer.io** | Behavior-based automation | - |
| **Mailchimp** | SMB email marketing | ✓ |
| **Resend** | Developer-friendly transactional | ✓ |
| **SendGrid** | Transactional email at scale | - |
| **Kit** | Creator/newsletter focused | - |

---

## Related Skills
```

## aimm-newsletter (1124-aimm-newsletter)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coachlou/ambient-library/tree/2b66a4a4e764bd5884e652e8759a80cacab244fe/library/aimm-newsletter
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1124-aimm-newsletter/2703-aimm-newsletter
- الوصف: Sends a newsletter email to all members of a named Google Contacts group; use for "send this to [group]", "send the newsletter", "email the group". Previews recipients and content before sending.

```markdown
Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/aimm-newsletter/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
```

## email-template-engineering (2286-email-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/email-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2286-email-engineering/8744-email-template-engineering
- الوصف: Build responsive HTML email templates that render across clients (Outlook/Word engine, Gmail clipping, Apple Mail dark mode) using MJML or table-based HTML, with a plain-text part, accessible markup, and the client-quirk guards. Reach for this when the user says "build a <type> email", "my email looks broken in Outlook", or "make this email responsive / dark-mode safe". Used by `email-sending-engi

```markdown
# Skill: email-template-engineering

> **Invoked by:** `email-sending-engineer` (primary).
>
> **When to invoke:** "build a transactional/marketing email"; "it renders wrong in Outlook"; "make it responsive / dark-mode safe / accessible".
>
> **Output:** a template (MJML preferred) with the client-quirk guards, a plain-text alternative, and a cross-client test plan.

## Procedure

1. **Default to MJML, not hand-rolled tables.** MJML compiles to the bulletproof table/VML soup Outlook needs, so you author semantic components instead of maintaining nested tables. Drop to raw table HTML only when MJML can't express the layout.
2. **Design for the worst client first.** The constraints that drive the markup:
   - **Outlook (Windows)** renders with the **Word** engine — no flexbox/grid, ghost tables + VML for buttons/background images, conditional `<!--[if mso]>` comments.
   - **Gmail** clips messages over **~102KB** ("[Message clipped]") and strips `<style>` in some contexts — keep it small and inline the critical CSS.
   - **Dark mode** (Apple Mail, Outlook) can invert colors — set explicit backgrounds, use `color-scheme`/`meta name="color-scheme"`, and test logos on dark.
3. **Always ship `multipart/alternative` with a real plain-text part.** It's an accessibility and deliverability signal — not a fallback you skip.
4. **Make it accessible.** `lang` on the root, `role="presentation"` on layout tables, real `alt` text on images, sufficient contrast, a single clear `<h1>`-equivalent, and a meaningful preheader.
5. **Keep links on the sending domain.** Mismatched link domains and naked tracking redirectors hurt deliverability and trust.
6. **Test before you ship.** Render across clients (Litmus/Email on Acid or a manual matrix), check the dark-mode pass, and confirm the size is under the Gmail clip threshold.

## Worked example (MJML, transactional)

```xml
<mjml>
  <mj-head>
    <mj-attributes><mj-all font-family="Arial, sans-serif" /></mj-attributes>
    <mj-style>:root { color-scheme: light dark; }</mj-style>
  </mj-head>
  <mj-body background-color="#f4f4f4">
    <mj-section background-color="#ffffff">
      <mj-column>
        <mj-text font-size="20px" color="#111111">Reset your password</mj-text>
        <mj-text color="#333333">We received a request to reset your password.</mj-text>
        <mj-button background-color="#2563eb" href="https://example.com/reset?t=...">
          Reset password
        </mj-button>
        <mj-text font-size="12px" color="#888888">
          Didn't request this? Ignore this email.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

Plus the **plain-text part**: `Reset your password: https://example.com/reset?t=...  — didn't request this? Ignore this email.`

## Guardrails
```

## email-tmpl (533-email-template)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/email-template
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/533-email-template/1562-email-tmpl
- الوصف: Generate responsive HTML email templates

```markdown
# email-template

Generate responsive HTML email templates.

## Tools

This skill uses the following tools:

- **Read** - Read existing files and configurations
- **Write** - Create new files and write content
- **Edit** - Modify existing files with precise replacements
- **Bash** - Execute shell commands for setup and installation
- **Grep** - Search codebases for patterns and references
- **Glob** - Find files by name patterns across the project
```
