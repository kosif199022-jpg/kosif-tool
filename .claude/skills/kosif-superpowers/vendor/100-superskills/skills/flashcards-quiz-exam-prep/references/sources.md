# مصادر «البطاقات والاختبارات والتحضير للامتحان» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## anki-flashcards (1217-anki-flashcards)

- الترخيص: **MIT**  ·  الأصل: https://github.com/dashed/claude-marketplace/tree/f6a24dbc08da57aeb80e7423da2508457d0b3398/plugins/anki-flashcards
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1217-anki-flashcards/2899-anki-flashcards
- الوصف: Create and manage Anki flashcards via the AnkiConnect API. Use when the user wants to create flashcards, add cards to Anki, manage Anki decks, review Anki statistics, or interact with Anki in any way. Requires Anki desktop app running with AnkiConnect add-on installed.

```markdown
# Anki Flashcards

Create, search, update, and manage Anki flashcards programmatically via the AnkiConnect HTTP API on `localhost:8765`. All operations use `curl` with JSON payloads — no SDK or library required.

## Prerequisites

Before using this skill, the user must have the following set up. **Do not attempt to install these — guide the user through the steps.**

### 1. Anki Desktop App

Anki must be installed and running. Download from https://apps.ankiweb.net/

### 2. AnkiConnect Add-on

Install the AnkiConnect add-on inside Anki:

1. Open Anki
2. Go to **Tools → Add-ons → Get Add-ons...**
3. Enter code: `2055492159`
4. Click **OK** and restart Anki

### 3. Platform-Specific Setup

**macOS** — Disable App Nap to prevent Anki from being suspended in the background:

```bash
defaults write net.ankiweb.dtop NSAppSleepDisabled -bool true
defaults write net.ichi2.anki NSAppSleepDisabled -bool true
defaults write org.qt-project.Qt.QtWebEngineCore NSAppSleepDisabled -bool true
```

**Windows** — Allow Anki through Windows Firewall if connections to `localhost:8765` are blocked.

### 4. Verify Connectivity

```bash
curl -s localhost:8765 -X POST -d '{"action": "requestPermission", "version": 6}'
```

Expected response includes `"permission": "granted"`. If the connection is refused, Anki is not running or AnkiConnect is not installed.

## Connectivity Check

Always verify AnkiConnect is reachable before performing any operations:

```bash
curl -s localhost:8765 -X POST -d '{"action": "requestPermission", "version": 6}'
```

If this fails, tell the user to:
1. Ensure Anki is open
2. Confirm AnkiConnect is installed (Tools → Add-ons should list AnkiConnect)
3. Restart Anki after installing the add-on

## Core Workflows

All requests use HTTP POST to `localhost:8765` with this JSON structure:

```json
{"action": "actionName", "version": 6, "params": {...}}
```

Responses return: `{"result": <value>, "error": <null or string>}`

### Creating Flashcards

**Single card (Basic model):**

```bash
curl -s localhost:8765 -X POST -d '{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "Spanish Vocabulary",
      "modelName": "Basic",
      "fields": {"Front": "casa", "Back": "house"},
      "tags": ["spanish", "beginner"]
    }
  }
}'
```

**Batch create multiple cards:**

```bash
curl -s localhost:8765 -X POST -d '{
  "action": "addNotes",
  "version": 6,
  "params": {
    "notes": [
      {
        "deckName": "Biology",
        "modelName": "Basic",
        "fields": {"Front": "What is mitosis?", "Back": "Cell division producing two identical daughter cells"},
        "tags": ["biology", "cell-division"]
      },
      {
        "deckName": "Biology",
        "modelName": "Basic",
```

## deep-learning-book (165-deep-learning-book)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/engineering/deep-learning-book
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/165-deep-learning-book/534-deep-learning-book
- الوصف: Study companion and working knowledge base for the Deep Learning textbook by Goodfellow, Bengio & Courville (MIT Press, 2016), read free at deeplearningbook.org. Indexes all 20 chapters, carries a 2016-to-2026 delta layer naming what the book got right, what was superseded (transformers, AdamW, diffusion, double descent) and what still holds, and ships four deterministic tools: a prerequisite-awar

```markdown
# Deep Learning — Study Companion

**Source book**: *Deep Learning*, Ian Goodfellow, Yoshua Bengio & Aaron Courville
(MIT Press, 2016) · 20 chapters, 3 parts · read free at
[deeplearningbook.org](https://www.deeplearningbook.org/) · companion compiled 2026-08-25.

**This is a companion, not a copy.** The book is copyrighted, and its site states that the
HTML-only format exists to discourage copying under the authors' MIT Press contract. Nothing
here reproduces its text. Every chapter file is original synthesis — what the chapter
establishes, how to use it, where it has aged — plus a link to the official chapter. Read the
book at the link; use this to navigate it, keep it current, and turn it into decisions.
See [references/rights_and_use.md](references/rights_and_use.md).

## How to Use This Skill

- **No argument** — load the core frameworks below.
- **A topic** — ask about `regularization`, `saddle points`, `partition function`; resolved
  through the Topic Index, then that chapter file is read before answering.
- **`chNN`** — load that chapter's file.
- **"is this still true?"** — the 2016→2026 delta layer, in every chapter file and in
  [references/book_to_2026_delta.md](references/book_to_2026_delta.md).
- **"where do I start?"** — run `scripts/reading_path_planner.py`.

When asked about something outside these 20 chapters, say so and route to the delta reference
rather than improvising the book's position on material published after it.

---

## Core Frameworks & Mental Models

### The (T, P, E) frame — ch05

Name the **task**, the **performance measure**, and the **experience** in one sentence before any
model code. Most failed projects failed at P: an unstated metric, or a proxy whose relationship
to the real objective was never checked.

### Every loss is a negative log-likelihood — ch03, ch06

Choose the output distribution, then take its negative log. Gaussian → MSE, Bernoulli → binary
cross-entropy, categorical → cross-entropy, Laplace → MAE. "Which loss?" is always the question
"which distribution?" in disguise. Modern contrastive and preference objectives sit outside this
frame — a real limit of the book, not a gap in your understanding.

### KL asymmetry decides your failure mode — ch03, ch19, ch20

D(p‖q) ≠ D(q‖p). Forward KL is mode-covering (blurry averages); reverse KL is mode-seeking
(sharp but partial). This single fact predicts VAE blur, GAN mode collapse, and the
characteristic over-confidence of mean-field variational posteriors.

### Train-error-first triage — ch11, ch05

High training error → capacity or optimization is the bottleneck; **more data will not help**.
Low training error with a large validation gap → data or regularization. This is the highest-value
```

## practice-health-check (3578-xbert-practice-health-check)

- الترخيص: **MIT**  ·  الأصل: https://github.com/xbertintelligence/xbert-plugins/tree/7e6bcc16a3fd1da830522d1d30f97a76c52b67aa/plugins/xbert-practice-health-check
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3578-xbert-practice-health-check/14390-practice-health-check
- الوصف: Run the XBert Practice Health Check across a Connect tenant — portfolio-wide data-quality and financial-health snapshot with diagnostic and prescriptive recommendations per client. Use when the user asks to assess practice health, sanity-check the book, identify deteriorating clients, find which clients need attention, run a monthly health check, or invokes the /practice-health-check slash command

```markdown
**Source of truth — XBert MCP:** Every figure, client record, ledger transaction, payrun, and XBert notification referenced here must come from the connected XBert MCP server. Call XBert MCP tools to fetch the data — do not invent figures, estimate from context, or substitute from chat history. If the XBert MCP is not connected, ask the user to install and authenticate it before continuing.

# Practice Health Check

A portfolio-level diagnostic that rolls up data-quality and notification signals across every client in a Connect tenant, bands the portfolio, then drills into the worst-performing N with prescriptive recommendations.

## Goal
Move beyond descriptive scores. For every flagged client, answer "what this means" and "what's likely causing it" so the principal can act, not just observe.

## Metrics
- **DQ score** — per-client data-quality score (0-100)
- **Outstanding notification load** — count and risk-weight from the notification summary
- **30-day completion rate** — from notification summary
- **Coverage** — connections per client, ledger type (Xero / QuickBooks / XPM / none)
- **Cohort age** — months since first connection

## Default thresholds (practice-configurable)
| Band | DQ score | Outstanding notifications |
|---|---|---|
| Healthy | >=85 | <10 |
| Watch | 70-84 | 10-25 |
| Risk | 55-69 | 26-50 |
| Critical | <55 | >50 |

Bands take the worst of (score band, notification band). Cohort minimum: 3 months operating history; below that, mark as "early stage — assess later".

## Process / rules
1. **Portfolio snapshot** — total clients, count per band, deteriorating count (run-over-run; v1 = single snapshot, v2 = trend).
2. **Worst-N drill-down** — default 10, user-configurable. For each:
   - Top three findings (named: e.g. "32 unreconciled bank transactions over 30 days", not "data quality issues")
   - "What this means" — business impact in one sentence
   - "What's likely causing it" — pattern-matched root cause from the data
   - One prescriptive recommendation per finding, impact-ranked
3. **Coverage variance** — non-Xero clients get fewer signals; flag this explicitly, do not lower their score for missing data we cannot see.
4. **Top portfolio issues** — three patterns repeating across the book, ranked by how many clients are affected.

## Always
- **Diagnostic, not descriptive.** Every finding paired with what it means and what's causing it.
- **Specific, not generic.** Name the client, name the issue. "Acme Pty Ltd: 32 unreconciled bank transactions" beats "data quality issues observed".
- **Graceful degradation.** Mark thin-data clients "insufficient history" — never speculate.
- **Read-only.** Suggest never apply. The user actions changes in XBert.
- **Coverage honesty.** State which clients had partial signal sets and why.
```

## practice-metrics (3579-xbert-practice-metrics)

- الترخيص: **MIT**  ·  الأصل: https://github.com/xbertintelligence/xbert-plugins/tree/7e6bcc16a3fd1da830522d1d30f97a76c52b67aa/plugins/xbert-practice-metrics
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3579-xbert-practice-metrics/14391-practice-metrics
- الوصف: Produce the XBert monthly Practice Metrics one-pager — standard partner KPIs, service-line P&L, prior-month variance commentary and RAG-banded client risk view. Use when the user asks for monthly metrics, partner-meeting pack, practice KPIs, lockup days, write-offs, WIP report, service-line P&L, or invokes the /practice-metrics slash command. Also triggers on 'monthly numbers', 'what are our KPIs 

```markdown
**Source of truth — XBert MCP:** Every figure, client record, ledger transaction, payrun, and XBert notification referenced here must come from the connected XBert MCP server. Call XBert MCP tools to fetch the data — do not invent figures, estimate from context, or substitute from chat history. If the XBert MCP is not connected, ask the user to install and authenticate it before continuing.

# Practice Metrics

A monthly partner-meeting one-pager. Same shape every month. Designed for consistency, not novelty.

## Goal
Produce a repeatable artefact partners can compare month-on-month without questioning whether definitions changed.

## Metrics
- **Revenue** — invoiced in month
- **WIP** — logged time × billing rate not yet invoiced
- **Debtors** — open AR balance (from aged receivables)
- **Lockup days** — (WIP + debtors) / annualised revenue × 365
- **Write-offs** — billed minus invoiced for completed work in month
- **Service-line P&L** — revenue and direct cost by bookkeeping / tax / advisory
- **Client risk band (RAG)** — derived from lockup, write-off rate, and outstanding work flags per client

## Default thresholds (practice-configurable)
| Threshold | Value | Used in |
|---|---|---|
| Material mover (KPI) | >=10% MoM movement OR >5pt change in lockup days | Commentary |
| Service-line significance | >=5% of total revenue | Service-line table |
| RAG: Red | Lockup >120 days OR write-off rate >15% OR >=2 escalated workflows | Client risk |
| RAG: Amber | Lockup 80-120 days OR write-off rate 8-15% OR 1 escalated workflow | Client risk |
| RAG: Green | All below amber thresholds | Client risk |

## Process / rules
1. **Compute current-month and prior-month KPIs.** Use the same source per metric across runs to keep movement comparable.
2. **Build service-line P&L.** Derive lines from XPM service codes or tags; group anything unmapped as "other" and call it out.
3. **Variance commentary.** For each material mover, write one sentence: what moved, by how much, suspected driver from the underlying data.
4. **Client risk pass.** Band every client; list any client that changed band vs prior month.
5. **One-pager layout** — KPI table on top, service-line table middle, commentary block, RAG list. Excel companion holds the per-client detail.

## Always
- **Same shape every month.** Resist the urge to add or reorder sections.
- **Same source per metric.** Comparability matters more than choosing the "best" source mid-stream.
- **Commentary explains movers, not stable numbers.** Stable months get a brief "no material movers" line.
- **Service-line tagging caveat.** If significant revenue is unmapped, state the percentage; do not silently bucket.
- **Read-only.** This is the reporting artefact, not an enactment tool.
```

## optimizing-deep-learning-models (1580-deep-learning-optimizer)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/ai-ml/deep-learning-optimizer
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1580-deep-learning-optimizer/4551-optimizing-deep-learning-models
- الوصف: Optimize deep learning models using Adam, SGD, and learning rate scheduling

```markdown
# Deep Learning Optimizer

Optimize deep learning models by tuning optimizers (Adam, SGD), learning rate schedules, and regularization strategies to improve accuracy and reduce training time.

## Overview

This skill empowers Claude to automatically optimize deep learning models, enhancing their performance and efficiency. It intelligently applies various optimization techniques based on the model's characteristics and the user's objectives.

## How It Works

1. **Analyze Model**: Examines the deep learning model's architecture, training data, and performance metrics.
2. **Identify Optimizations**: Determines the most effective optimization strategies based on the analysis, such as adjusting the learning rate, applying regularization techniques, or modifying the optimizer.
3. **Apply Optimizations**: Generates optimized code that implements the chosen strategies.
4. **Evaluate Performance**: Assesses the impact of the optimizations on model performance, providing metrics like accuracy, training time, and resource consumption.

## When to Use This Skill

This skill activates when you need to:

- Optimize the performance of a deep learning model.
- Reduce the training time of a deep learning model.
- Improve the accuracy of a deep learning model.
- Optimize the learning rate for a deep learning model.
- Reduce resource consumption during deep learning model training.

## Examples

### Example 1: Improving Model Accuracy

User request: "Optimize this deep learning model for improved image classification accuracy."

The skill will:

1. Analyze the model and identify potential areas for improvement, such as adjusting the learning rate or adding regularization.
2. Apply the selected optimization techniques and generate optimized code.
3. Evaluate the model's performance and report the improved accuracy.

### Example 2: Reducing Training Time

User request: "Reduce the training time of this deep learning model."

The skill will:

1. Analyze the model and identify bottlenecks in the training process.
2. Apply techniques like batch size adjustment or optimizer selection to reduce training time.
3. Evaluate the model's performance and report the reduced training time.

## Best Practices

- **Optimizer Selection**: Experiment with different optimizers (e.g., Adam, SGD) to find the best fit for the model and dataset.
- **Learning Rate Scheduling**: Implement learning rate scheduling to dynamically adjust the learning rate during training.
- **Regularization**: Apply regularization techniques (e.g., L1, L2 regularization) to prevent overfitting.

## Integration
```

## adapting-transfer-learning-models (1604-transfer-learning-adapter)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/ai-ml/transfer-learning-adapter
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1604-transfer-learning-adapter/4575-adapting-transfer-learning-models
- الوصف: Build this skill automates the adaptation of pre-trained machine learning

```markdown
# Transfer Learning Adapter

Adapt pre-trained models (ResNet, BERT, GPT) to new tasks and datasets through fine-tuning, layer freezing, and domain-specific optimization.

## Overview

This skill streamlines the process of adapting pre-trained machine learning models via transfer learning. It enables you to quickly fine-tune models for specific tasks, saving time and resources compared to training from scratch. It handles the complexities of model adaptation, data validation, and performance optimization.

## How It Works

1. **Analyze Requirements**: Examines the user's request to understand the target task, dataset characteristics, and desired performance metrics.
2. **Generate Adaptation Code**: Creates Python code using appropriate ML frameworks (e.g., TensorFlow, PyTorch) to fine-tune the pre-trained model on the new dataset. This includes data preprocessing steps and model architecture modifications if needed.
3. **Implement Validation and Error Handling**: Adds code to validate the data, monitor the training process, and handle potential errors gracefully.
4. **Provide Performance Metrics**: Calculates and reports key performance indicators (KPIs) such as accuracy, precision, recall, and F1-score to assess the model's effectiveness.
5. **Save Artifacts and Documentation**: Saves the adapted model, training logs, performance metrics, and automatically generates documentation outlining the adaptation process and results.

## When to Use This Skill

This skill activates when you need to:

- Fine-tune a pre-trained model for a specific task.
- Adapt a pre-trained model to a new dataset.
- Perform transfer learning to improve model performance.
- Optimize an existing model for a particular application.

## Examples

### Example 1: Adapting a Vision Model for Image Classification

User request: "Fine-tune a ResNet50 model to classify images of different types of flowers."

The skill will:

1. Download the ResNet50 model and load a flower image dataset.
2. Generate code to fine-tune the model on the flower dataset, including data augmentation and optimization techniques.

### Example 2: Adapting a Language Model for Sentiment Analysis

User request: "Adapt a BERT model to perform sentiment analysis on customer reviews."

The skill will:

1. Download the BERT model and load a dataset of customer reviews with sentiment labels.
2. Generate code to fine-tune the model on the review dataset, including tokenization, padding, and attention mechanisms.

## Best Practices

- **Data Preprocessing**: Ensure data is properly preprocessed and formatted to match the input requirements of the pre-trained model.
- **Hyperparameter Tuning**: Experiment with different hyperparameters (e.g., learning rate, batch size) to optimize model performance.
```
