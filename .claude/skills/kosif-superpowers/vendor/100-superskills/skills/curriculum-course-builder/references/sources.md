# مصادر «بناء المناهج والدورات» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## curriculum (2524-curriculum)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mnox/mnox-ai/tree/50de1158b4e27879e3da104e36b7d31d4204bc15/plugins/curriculum
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2524-curriculum/9821-curriculum
- الوصف: Use when the user wants to learn a topic deeply — asks for a curriculum, learning path, self-study plan, study guide, syllabus, or says teach me X. Generates a structured, adaptive curriculum directory of markdown modules (ELI5 → Core Concepts → Deep Dive → Supporting Material → Understanding Check) plus an append-only JSONL assessment log that adapts future modules to the learner's answers. Tailo

```markdown
# Curriculum

## Overview

Generate a structured, adaptive learning curriculum for any topic the user wants to master. Each curriculum produces a directory of markdown modules with a uniform spine, plus an assessment-loop substrate (`curriculum-meta.md`, `responses.jsonl`, `progress.md`, `misconceptions.md`) that lets the agent adapt later modules to the learner's answers.

The skill has four workflows: **Create** a new curriculum, **Assess** the learner's Understanding Check answers, **Prepare** the next module with gap-remediation bridges, and **Resume** a paused curriculum in a later session.

## Quick Reference

| Scenario | Workflow | Primary script |
|----------|----------|----------------|
| User asks for a new curriculum on topic X | Create (below) | `scripts/scaffold.py` |
| User pastes answers to an Understanding Check | Assess (below) | `scripts/append_assessment.py` + `scripts/compute_progress.py` |
| User says "ready for the next module" | Prepare (below) | — (reads JSONL, edits next module) |
| User returns after a gap: "where was I?" | Resume (below) | — (reads MEMORY.md + progress.md) |

| File in a generated curriculum | Purpose |
|---|---|
| `README.md` | Curriculum map, module table, how to use |
| `curriculum-meta.md` | Adaptation rules + JSONL schema (copied from `assets/`) |
| `modules/00-orientation.md` | Motivation, goal framing, prerequisites |
| `modules/NN-*.md` | Each module follows the 5-part spine |
| `assessments/responses.jsonl` | Append-only log of (question, answer, assessment) rows |
| `assessments/progress.md` | Per-module status table (rewritten by `compute_progress.py`) |
| `assessments/misconceptions.md` | Running ledger of recurring misconceptions |
| `assessments/synthesis_prompts.md` | Cross-module synthesis questions, written every 3 modules; answers log with `module: "synthesis-<n>"` |

## Workflow: Create a new curriculum

### Step 1 — Gather Inputs

Ask these questions using the host's structured clarification mechanism when
available; otherwise ask concise plain-text questions:

1. **Topic**: what is the subject? (free text)
2. **Long-term goal**: what is the user ultimately trying to be able to *do* with this knowledge? The goal reframes every module.
3. **Emphasis areas**: which sub-topics need the deepest coverage? (multi-select or free text)
4. **Starting level**: beginner / intermediate / advanced.
5. **Output directory**: absolute path where the curriculum will be written (e.g., `./<topic>-learning` or any directory the user chooses). Default: propose `./<kebab-topic>-learning` in the current working directory.
6. **Approximate module count**: 8–12 is the default range; allow override.

If the user has already stated some of these in the prompt, skip those questions — do not re-ask.
```

## training-machine-learning-models (1592-ml-model-trainer)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/ai-ml/ml-model-trainer
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1592-ml-model-trainer/4563-training-machine-learning-models
- الوصف: Build train machine learning models with automated workflows. Analyzes

```markdown
# Ml Model Trainer

Train machine learning models with configurable architectures, loss functions, and optimization strategies across classification, regression, and other task types.

## Overview

This skill empowers Claude to automatically train and evaluate machine learning models. It streamlines the model development process by handling data analysis, model selection, training, and evaluation, ultimately providing a persisted model artifact.

## How It Works

1. **Data Analysis and Preparation**: The skill analyzes the provided dataset and identifies the target variable, determining the appropriate model type (classification, regression, etc.).
2. **Model Selection and Training**: Based on the data analysis, the skill selects a suitable machine learning model and configures the training parameters. It then trains the model using cross-validation techniques.
3. **Performance Evaluation and Persistence**: After training, the skill generates performance metrics to evaluate the model's effectiveness. Finally, it saves the trained model artifact for future use.

## When to Use This Skill

This skill activates when you need to:

- Train a machine learning model on a given dataset.
- Evaluate the performance of a machine learning model.
- Automate the machine learning model training process.

## Examples

### Example 1: Training a Classification Model

User request: "Train a classification model on this dataset of customer churn data."

The skill will:

1. Analyze the customer churn data, identify the churn status as the target variable, and determine that a classification model is appropriate.
2. Select a suitable classification algorithm (e.g., Logistic Regression, Random Forest), train the model using cross-validation, and generate performance metrics such as accuracy, precision, and recall.

### Example 2: Training a Regression Model

User request: "Train a regression model to predict house prices based on features like size, location, and number of bedrooms."

The skill will:

1. Analyze the house price data, identify the price as the target variable, and determine that a regression model is appropriate.
2. Select a suitable regression algorithm (e.g., Linear Regression, Support Vector Regression), train the model using cross-validation, and generate performance metrics such as Mean Squared Error (MSE) and R-squared.

## Best Practices

- **Data Quality**: Ensure the dataset is clean and properly formatted before training the model.
- **Feature Engineering**: Consider feature engineering techniques to improve model performance.
- **Hyperparameter Tuning**: Experiment with different hyperparameter settings to optimize model performance.

## Integration
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

## syllabus (227-syllabus)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/research/syllabus
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/227-syllabus/704-syllabus
- الوصف: Generates a curated supplementary reading list from any course syllabus using Consensus academic search. Grill-me intake (syllabus input format + course audience + year range) plus a grouping forcing-options checkpoint before any search runs — so the reading list matches the course's level and recency need. Parses the syllabus to extract topics and learning outcomes, searches Consensus for recent 

```markdown
# Syllabus — Course Supplementary Reading List

> **Portability:** Requires a Consensus MCP connection, Node.js with `docx` package, and file reading capability for the syllabus. Works in Claude Code CLI natively. In Claude.ai with Consensus MCP + Code Execution + file upload, the workflow is supported.

For an instructor or student with a course syllabus, produce a professional supplementary reading list as `.docx` containing recent peer-reviewed papers per course section.

## Architectural Pattern: Bundled Script

This skill uses a **bundled JavaScript helper script** for DOCX generation rather than inlining the 300+ lines of layout code:

- DOCX generation logic is reusable + complex
- Better separation of concerns: skill = orchestration + intelligence; script = mechanical document assembly
- Token-efficient: skill doesn't re-derive layout each run
- Easier to maintain and version

The bundled script is at `scripts/generate_reading_list.js`. The skill orchestrates the pipeline + invokes the script with JSON input.

## Agent Integrity Rules (Research-Pack Convention)

Locked verbatim per PR #657 audit.

- **Only use what Consensus returns.** Every paper title, author, journal, year, URL must come from this session's tool calls. Training-knowledge papers labeled `[Not from Consensus — model knowledge]` and excluded.
- **Confirm before moving on.** A search isn't complete until response received and inspected.
- **Track three counts.** Queries sent / papers received / papers cited. Surface in audit summary.
- **Surface gaps, don't fill them.** Section with one paper + note about limited results > section padded with fabrications.

## Phase 0: Grill-Me Intake (3 forcing questions)

### Q1 (root) — Syllabus input

> **Provide the syllabus — pick one:**
>
> 1. File path (PDF, DOCX, text) — I'll read it
> 2. Pasted content — paste below
> 3. Image of a printed syllabus — attach the image
>
> *Why I'm asking:* Each format needs a different reader (PDF / DOCX parser / vision). Picking upfront prevents wasted attempts.

Forcing choice. Refuse to start without a syllabus.

### Q2 (depends on Q1) — Course audience

> **Course audience — pick one:**
>
> 1. Undergraduate (intro level)
> 2. Undergraduate (advanced / upper division)
> 3. Graduate (Masters / early PhD)
> 4. Graduate (doctoral / advanced)
> 5. Professional / continuing education
> 6. Mixed
>
> *Why I'm asking:* Audience dictates summary jargon level and discussion-question complexity. Undergrad summaries define every term; grad summaries assume technical fluency. Discussion questions for undergrads test analysis; for grads test critique and extension.

See [`references/audience_calibration.md`](references/audience_calibration.md) for the canon.

### Q3 (depends on Q1) — Year range
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
