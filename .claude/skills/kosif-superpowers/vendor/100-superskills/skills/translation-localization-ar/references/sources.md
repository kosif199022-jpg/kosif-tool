# مصادر «الترجمة والتوطين العربي» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## language-config (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4061-language-config
- الوصف: Configure the brand's multilingual settings in profile.json — primary and secondary languages, do-not-translate terms, preferred translation service per language (routed by language family across the translation MCPs you have connected), and locale formatting for dates, numbers, and currency — with view/add/remove/reset actions and a before/after diff on every change. Triggers on \"/digital-market

```markdown
# /digital-marketing-pro:language-config

## Purpose

Configure and manage multilingual settings for the active brand. This command controls the language infrastructure that powers all translation, localization, and multilingual audit commands in the plugin. It sets the primary content language (the source language for all translations), secondary and target languages (which markets and languages the brand operates in), do-not-translate terms (brand names, product names, trademarked phrases, and technical terms that must appear identically in every language), preferred translation service per language (routing to the optimal MCP for each language pair), and locale-specific formatting rules (date, number, currency, measurement formats per market).

This configuration persists in the brand profile and is referenced by every multilingual command — translate, transcreate, multilingual-score, language-audit, hreflang-check, and any content creation targeting non-primary languages. Getting this configuration right upfront prevents repeated corrections downstream and ensures consistent multilingual output across all workflows.

## Input Required

The user must provide (or will be prompted for):

- **Configuration action**: What to do — `view` (display all current language settings), `set-primary` (change the primary/source language), `add-language` (add a secondary/target language), `remove-language` (remove a secondary language), `add-dnt` (add a do-not-translate term), `remove-dnt` (remove a do-not-translate term), `set-translation-pref` (set preferred translation service for a language), `set-locale-format` (set locale-specific formatting for a language-region), or `reset` (restore language config to defaults)
- **Language code** (for language actions): ISO 639-1 language code with optional ISO 3166-1 region (e.g., `en`, `en-US`, `de-DE`, `hi-IN`, `ja-JP`, `pt-BR`). Required for set-primary, add-language, remove-language, set-translation-pref, and set-locale-format actions
- **Term** (for DNT actions): The exact term to add or remove from the do-not-translate list. Required for add-dnt and remove-dnt. Can be a single term or a comma-separated list of terms to add/remove in batch
- **Translation service** (for set-translation-pref): The preferred translation MCP server for the specified language — any server name the user has connected (free-form; validated as a non-empty slug). The preference is the user's explicit choice and outranks the router's capability-based selection. If the named server is not currently in `.mcp.json`, warn but still record it (the user may connect it later). Required for set-translation-pref action
```

## i18n-foundations-and-icu (2329-localization-i18n-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/localization-i18n-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu
- الوصف: Core internationalization foundations: string externalization strategy, ICU MessageFormat for plurals and gender selects, CLDR plural rules, locale-aware formatting via ECMA-402/Intl APIs, RTL/bidi layout design, Unicode encoding, and text expansion budget planning.

```markdown
# i18n Foundations and ICU MessageFormat

**Purpose:** give every application the structural foundations it needs to be localized correctly —
string externalization, ICU MessageFormat, locale-aware formatting, RTL/bidi, Unicode encoding, and
text expansion awareness.

## The operating loop

1. **Audit the externalization surface.** Grep the codebase for user-facing string literals in
   render, return, setText, `$t`, or template expression positions. Every hit is an i18n bug.
   Scope the extraction: UI strings, error messages, validation messages, notification text, ARIA
   labels, `<title>`, and `<meta>` description — but not log messages, internal IDs, or test
   fixtures.

2. **Choose a string format and key convention.** Select the format for the project type (see the
   decision tree). Establish a key-naming convention: flat keys (`user.profile.title`) vs. nested
   objects (`{ user: { profile: { title: "…" } } }`). Flat keys are more portable for TMS tools;
   nested objects map naturally to namespaces. Pick one; document it.

3. **Apply ICU MessageFormat for every message that varies.** Plural, gender, and select messages
   require ICU syntax — not branching in application code.

   - **Plural:** `{count, plural, one{# item} other{# items}}`. For target locales with more plural
     categories (Arabic: `zero`, `one`, `two`, `few`, `many`, `other`; Russian: `one`, `few`,
     `many`, `other`), provide all required categories. Consult CLDR plural rules at
     https://www.unicode.org/cldr/charts/latest/supplemental/language_plural_rules.html.
   - **Gender select:** `{gender, select, male{He uploaded} female{She uploaded} other{They uploaded}}`.
   - **Ordinal:** `{position, selectordinal, one{#st} two{#nd} few{#rd} other{#th}}`.
   - **Date/time skeleton:** `{date, date, ::yMMMd}` (CLDR skeleton; not a hard-coded format string).
   - **Number skeleton:** `{amount, number, ::currency/USD sign-accounting}`.

4. **Replace all `new Date().toLocaleString()` calls with explicit locale.** Pass the user's
   current locale: `new Date().toLocaleString(locale, options)`. Similarly for `Intl.NumberFormat`
   and `Intl.RelativeTimeFormat`. Never call these without a locale argument.

5. **Audit for RTL/bidi readiness.** Check that:
   - Layout uses CSS logical properties (`margin-inline-start`, `padding-block-end`, `inset-inline`)
     rather than physical properties (`margin-left`, `padding-bottom`, `left`).
   - The root element sets `dir` dynamically from the locale: `document.documentElement.dir = isRTL ? 'rtl' : 'ltr'`.
   - Icons and directional images are mirrored for RTL (back arrow, progress indicators).
   - Text alignment uses `text-align: start` not `text-align: left`.

6. **Audit encoding.** Verify UTF-8 end-to-end:
```

## localization-qa-and-pseudo-loc (2329-localization-i18n-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/localization-i18n-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2329-localization-i18n-engineering/8942-localization-qa-and-pseudo-loc
- الوصف: Localization quality assurance methodology: pseudo-localization CI gate design (accent, expansion, bidi variants), l10n linting rules (missing keys, empty values, placeholder consistency, ICU syntax), visual and overflow QA techniques, locale-coverage test matrix, and false-positive triage for l10n lint.

```markdown
# Localization QA and Pseudo-Localization

**Purpose:** build automated quality gates that catch i18n and l10n bugs before they reach
translators, before they block a release, and before users encounter them in production.

## The operating loop

1. **Generate pseudo-locale strings.** Pseudo-localization is a deterministic transformation of
   source strings that preserves the string structure but makes it visually distinct. Implement or
   configure a pseudo-localizer with these variants (use all three for maximum coverage):

   | Variant | Transform | What it catches |
   |---|---|---|
   | **Accent** | Replace ASCII vowels with accented equivalents (`a→ä`, `e→ë`, `o→ö`, `u→ü`) | Hard-coded English strings (they don't get transformed); non-UTF-8 rendering |
   | **Expansion** | Wrap string in `[` / `]` and pad to ~140 % of original length (`[Héllo Wörld!!!]`) | UI overflow, truncation, container width constraints |
   | **Bidi/RTL** | Wrap in Unicode RLI/PDF markers or reverse word order | RTL layout bugs, bidi algorithm edge cases, CSS `dir` not applied |
   | **Double-length** | Repeat string content to 200 % of original length | Worst-case expansion for Finnish, Hindi, Thai |

2. **Add pseudo-loc as a CI gate.** The pseudo-locale build must be a blocking check:
   - Generate pseudo-locale files from source strings at CI start.
   - Run the full test suite (unit + integration) against the pseudo-locale.
   - Run screenshot/snapshot tests against the pseudo-locale (Playwright, Cypress, Storybook).
   - Fail the build if: any UI screenshot shows clipped/overflowed text, any test fails due to
     a string mismatch, or any hard-coded string is detected (compare rendered output against
     expected pseudo-transformed output).
   - The pseudo-locale files are generated at build time — do NOT commit them to the repo.

3. **Configure l10n lint rules.** Choose a lint tool appropriate to the project:
   - **JavaScript/TypeScript:** `i18next-lint`, `eslint-plugin-i18n-json`, `@formatjs/cli lint`.
   - **Python:** `django-admin check` (i18n checks), custom script against PO files.
   - **General XLIFF:** `xliff-lint`, TMS-integrated validation.
   - **Custom:** a small script that reads source and target locale JSON/XLIFF and checks rules.

   Standard rule set:
   - **Missing key:** every key in the source locale must exist in every target locale.
   - **Extra key:** every key in a target locale must exist in the source locale (orphan detection).
   - **Empty value:** a translated value that is an empty string is almost always a bug.
   - **Untranslated value:** a translated value identical to the source value may be intentional
     (proper nouns, URLs) or a miss — flag for review with a suppression path.
```

## language-audit (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4060-language-audit
- الوصف: Audit multilingual integrity across every language version of a site or content set — hreflang implementation, content parity (missing, outdated, or structurally divergent translations), translation-quality spot checks via language-router.py, regional compliance per market (GDPR, DPDPA, LGPD, PIPA, APPI, CCPA), and locale formatting — producing 0-100 scores per dimension and a severity-ranked fix 

```markdown
# /digital-marketing-pro:language-audit

## Purpose

Comprehensive multilingual consistency audit across all language versions of a brand's content. Checks that all language versions are properly linked with correct hreflang annotations, that content parity exists across languages (no missing translations, no outdated versions, no significant structural deviations), that regional compliance requirements are met per target market, and that translation quality meets brand standards. Covers the full spectrum of multilingual integrity: technical SEO implementation, content completeness, linguistic quality, legal compliance, and locale-specific formatting.

Essential for brands operating across multiple markets where multilingual website and campaign integrity directly impacts search visibility, user experience, and regulatory standing. Surfaces issues that silently erode international performance — orphaned hreflang tags sending search engines conflicting signals, outdated translations creating brand inconsistency, missing compliance elements exposing the brand to legal risk, and incomplete localization undermining trust with local audiences.

## Input Required

The user must provide (or will be prompted for):

- **Website URL or content set**: The URL to audit (homepage, specific section, or full site) or a set of content assets (email campaigns, landing pages, ad copy) with their language versions. For websites, the user may provide a sitemap URL, a list of page URLs, or HTML source containing hreflang annotations. For content sets, provide all language versions of each asset
- **Languages to check**: Specific language-region codes to audit (e.g., en-US, de-DE, fr-FR, hi-IN) or "all configured" to audit every language in the brand's language configuration. If omitted, defaults to all languages configured in the brand profile
- **Audit focus**: Which dimensions to audit — `hreflang` (tag implementation only), `content-parity` (cross-language completeness and consistency), `compliance` (regional regulatory requirements), `quality` (translation scoring), `localization` (formatting and cultural adaptation), or `comprehensive` (all dimensions). Defaults to comprehensive if not specified

## Process
```

## 9454-curate-language (2435-domain-driven-design)

- الترخيص: **MIT**  ·  الأصل: https://github.com/melodic-software/claude-code-plugins/tree/c8fa858c9059d3183cfc08f646e4a97f44b33973/plugins/domain-driven-design
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2435-domain-driven-design/9454-curate-language
- الوصف: Actively maintain a consuming project's ubiquitous-language glossary as domain understanding changes: resolve ambiguous or overloaded terms, choose canonical language, record rejected synonyms, sharpen what-it-IS definitions, and route terms to an already-known bounded context. Use when: 'update the domain glossary', 'define this domain term', 'standardize this vocabulary', 'these names conflict',

```markdown
## Variables

Request: `$ARGUMENTS`

## Purpose

Maintain the consuming project's active, committed vocabulary record. The glossary is not a static
dictionary and not the domain model by itself: it records language the team has actually resolved so
the same model language can be used consistently in conversation, documentation, tests, and code.

This skill owns **changing** that record. Merely reading the nearest glossary so another skill uses
the right words is a one-line habit and does not require this workflow.

Entry discipline, the convention-resolution ladder, and the multi-context rules live in
[context/glossary-contract.md](context/glossary-contract.md). Read that file before resolving a
convention or writing an entry.

## Workflow

### 1. Establish what is resolved

Start from the conversation, `$ARGUMENTS`, existing glossary entries, and relevant project artifacts.
Identify the concrete language change:

- a new project-specific concept has a stable meaning
- one term is being used for two concepts
- several names compete for one concept
- an existing definition no longer matches the team's model
- the same spelling intentionally means different things in different known contexts

Exercise the candidate language in one or two domain scenarios. If the meaning, canonical term, or
context is still disputed, ask one focused question and do not write yet. Never manufacture consensus.
When the proposed meaning describes existing software behavior, inspect the relevant code and tests.
If they contradict the conversation, surface the mismatch and resolve which model is intended before
writing; do not silently treat either source as authoritative.

### 2. Resolve the consumer's convention

Gather the evidence the ladder in `context/glossary-contract.md` ranks: the consuming project's
`AGENTS.md`, `CLAUDE.md`, `.claude/rules`, and declared documentation conventions, then, from the
files and domain area in scope, walk toward the repository root looking for an existing
domain-vocabulary file or context map. Work the ladder in order and stop at the first rung that
resolves both format and location.

Preserve whatever the winning convention already fixes: filename, location, headings, ordering, and
entry syntax. Do not impose a fixed filename of your own. Re-read the target file immediately
before editing it. Another turn or agent may have changed it.

### 3. Route to a known language context

Use an existing context map or explicit project convention first. Otherwise infer the applicable
**already-known** context from the task, touched files, and accepted design/workshop artifacts. If two
contexts remain plausible, ask rather than putting the term in both.
```

## nuxt-i18n (2918-nuxt-i18n)

- الترخيص: **MIT**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/nuxt-i18n
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2918-nuxt-i18n/12112-nuxt-i18n
- الوصف: Nuxt i18n internationalization module for locale routing, lazy-loaded translations, SEO, browser detection, and multi-domain setups. Use when working with @nuxtjs/i18n, locale switching, translated routes, or i18n composables.

```markdown
Nuxt i18n is an internationalization module for Nuxt powered by Vue i18n. It provides locale-based routing, lazy-loaded translations, browser language detection, SEO metadata, and multi-domain locale support.

> The skill is based on @nuxtjs/i18n v10.x, generated at 2026-03-28.

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Configuration | Module setup, locales, Vue I18n config, key options | [core-configuration](references/core-configuration.md) |
| Routing | Strategies, custom route paths, ignoring localized routes | [core-routing](references/core-routing.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Detection & Switching | Browser detection, lang switcher, locale fallback, cookies | [features-detection-switching](references/features-detection-switching.md) |
| SEO | useLocaleHead, hreflang, canonical links, OpenGraph | [features-seo](references/features-seo.md) |
| Lazy Loading | Lazy-loaded translations, multiple files, dynamic API loading | [features-lazy-loading](references/features-lazy-loading.md) |
| Per-Component | i18n custom blocks in SFCs, local scope translations | [features-per-component](references/features-per-component.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Domains | Different domains, multi-domain locales, runtime env vars | [advanced-domains](references/advanced-domains.md) |
| Server & Hooks | Server-side translations, runtime hooks, module integration, layers | [advanced-server-hooks](references/advanced-server-hooks.md) |

## API

| Topic | Description | Reference |
|-------|-------------|-----------|
| API Reference | Composables, components, helper functions, instance properties | [api-reference](references/api-reference.md) |

## Full Documentation

For details beyond these references, fetch the complete official documentation:

- **llms.txt** (overview): https://i18n.nuxtjs.org/llms.txt
- **llms-full.txt** (full docs): https://i18n.nuxtjs.org/llms-full.txt
```
