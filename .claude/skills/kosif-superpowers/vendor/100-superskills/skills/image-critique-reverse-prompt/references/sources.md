# مصادر «نقد الصور واستخراج البرومبت» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## vision-inference-optimization (2259-computer-vision-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/computer-vision-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2259-computer-vision-engineering/8611-vision-inference-optimization
- الوصف: Make a trained vision model fit and run on its target: budget latency on the real device, optimize in order of leverage (quantization INT8/FP16 with calibration, then pruning, then distillation), export to the runtime the target uses (ONNX / TensorRT / CoreML / TFLite / OpenVINO), and re-check accuracy against the operating point after every step. Device/runtime numbers verify-at-use; no PII.

```markdown
# Vision Inference Optimization

The discipline of holding the latency budget without giving away the accuracy the model was built to deliver. A model that hits its metric offline but can't run inside the budget on the target has shipped nothing.

> **Engineering judgment.** Accelerator specs, runtime op-support, and quantization behavior move with hardware and SDK versions — every device number and runtime-support claim here is `[verify-at-use]`. No PII, no image data stored.

## Workflow

1. **Budget latency on the real target.** The target + required throughput fix the budget (e.g. 30 fps → ~33 ms/frame). Profile on the actual device — a desktop GPU number is not a Jetson number.
2. **Optimize in order of leverage.** Quantization (INT8/FP16 with proper calibration) usually buys the most; then pruning; then distillation to a smaller student. Stop when the budget is met.
3. **Re-check accuracy after every step.** Every optimization can move accuracy — re-run the eval harness against the operating point after each, don't assume parity. A quantization that drops the rare class below the operating point is a regression, not a speedup.
4. **Export to the runtime the target uses.** ONNX as the interchange, then TensorRT (NVIDIA), CoreML (Apple), TFLite (mobile/Coral), OpenVINO (Intel). Confirm the ops your model uses are supported on the target runtime `[verify-at-use]` before committing.
5. **Profile the whole frame, not just the forward pass.** Decode, copy, and pre/post-processing often cost more than inference — find the real bottleneck before optimizing the model further.

## Metrics table

| Metric | Target/read | Flag |
|---|---|---|
| On-target latency vs budget (ms) | At or under the frame budget | `[verify-at-use]` per device |
| Post-optimization accuracy vs operating point | Still clears the acceptance criterion | durable check |
| Precision mode (FP32 / FP16 / INT8) | Smallest that holds accuracy | `[verify-at-use]` |
| Model size / memory on target | Fits the device | `[verify-at-use]` |
| Runtime op-support for the model | All ops supported on target | `[verify-at-use]` |

## Anti-patterns

- Optimizing without an on-target latency budget.
- Assuming quantization is accuracy-free — shipping without re-running eval.
- Exporting to a runtime that doesn't support an op the model uses.
- Optimizing the model when decode/copy is the real bottleneck.

## See also

- Traverse the **deployment-target choice** tree in [`../../knowledge/cv-decision-trees.md`](../../knowledge/cv-decision-trees.md).
- Dated accelerator/runtime landscape: [`../../knowledge/cv-reference-2026.md`](../../knowledge/cv-reference-2026.md).
```

## processing-computer-vision-tasks (1576-computer-vision-processor)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/ai-ml/computer-vision-processor
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1576-computer-vision-processor/4547-processing-computer-vision-tasks
- الوصف: Process images using object detection, classification, and segmentation.

```markdown
# Computer Vision Processor

Process images using object detection, classification, and segmentation pipelines with configurable model backends.

## Overview

This skill empowers Claude to leverage the computer-vision-processor plugin to analyze images, detect objects, and extract meaningful information. It automates computer vision workflows, optimizes performance, and provides detailed insights based on image content.

## How It Works

1. **Analyzing the Request**: Claude identifies the need for computer vision processing based on the user's request and trigger terms.
2. **Generating Code**: Claude generates the appropriate Python code to interact with the computer-vision-processor plugin, specifying the desired analysis type (e.g., object detection, image classification).
3. **Executing the Task**: The generated code is executed using the `/process-vision` command, which processes the image and returns the results.

## When to Use This Skill

This skill activates when you need to:

- Analyze an image for specific objects or features.
- Classify an image into predefined categories.
- Segment an image to identify different regions or objects.

## Examples

### Example 1: Object Detection

User request: "Analyze this image and identify all the cars and pedestrians."

The skill will:

1. Generate code to perform object detection on the provided image using the computer-vision-processor plugin.
2. Return a list of bounding boxes and labels for each detected car and pedestrian.

### Example 2: Image Classification

User request: "Classify this image. Is it a cat or a dog?"

The skill will:

1. Generate code to perform image classification on the provided image using the computer-vision-processor plugin.
2. Return the classification result (e.g., "cat" or "dog") along with a confidence score.

## Best Practices

- **Data Validation**: Always validate the input image to ensure it's in a supported format and resolution.
- **Error Handling**: Implement robust error handling to gracefully manage potential issues during image processing.
- **Performance Optimization**: Choose the appropriate computer vision techniques and parameters to optimize performance for the specific task.

## Integration

This skill utilizes the `/process-vision` command provided by the computer-vision-processor plugin. It can be integrated with other skills to further process the results of the computer vision analysis, such as generating reports or triggering actions based on detected objects.

## Prerequisites

- Appropriate file access permissions
- Required dependencies installed

## Instructions

1. Invoke this skill when the trigger conditions are met
2. Provide necessary context and parameters
3. Review the generated output
4. Apply modifications as needed

## Output
```

## product-vision (2883-pm-product-strategy)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-product-strategy
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2883-pm-product-strategy/11660-product-vision
- الوصف: Brainstorm an inspiring, achievable, and emotional product vision that motivates teams and aligns stakeholders. Use when defining or refining a product vision, creating a vision statement, or aligning the team around a shared direction.

```markdown
# Product Vision

## Metadata
- **Name**: product-vision
- **Description**: Brainstorm an inspiring, achievable, and emotional product vision. Use when defining or refining product vision, aligning teams around a north star, or creating a vision statement.
- **Triggers**: product vision, vision statement, create vision, inspiring vision, north star vision

### Domain Context

A product **vision** answers: "How can we inspire people? What are we aspiring to achieve? What values do we uphold?" Vision evolves with strategy — it's a living statement, not a one-time exercise. It should make people feel something, not just understand the direction.

## Instructions

You are a veteran product leader developing a compelling product vision.

Your task is to brainstorm a product vision for $ARGUMENTS.

## Input Requirements
- Information about your company and product (you may read files from the user's workspace)
- Current state, market positioning, or any relevant context

## Output
Provide a vision statement that is:
1. **Inspiring** - Motivates teams to wake up and commit to the goal
2. **Achievable** - Realistic based on resources, market, and capabilities
3. **Emotional** - Creates meaning and connection

## Process
1. Review provided company and product information
2. Identify the core problem being solved
3. Envision the ideal future state for customers and the company
4. Draft multiple vision options (3-5 variations)
5. Select the strongest vision and briefly explain your rationale
6. Highlight how this vision aligns with company values and market opportunity

## Notes
- A great vision is memorable and can be communicated in one sentence
- Balance ambition with credibility
- Consider the perspective of customers, employees, and investors
- Avoid jargon; use clear, emotionally resonant language

---

### Further Reading

- [Product Vision vs Strategy vs Objectives vs Roadmap: The Advanced Edition](https://www.productcompass.pm/p/product-vision-strategy-goals-and)
- [Introducing the Product Strategy Canvas](https://www.productcompass.pm/p/new-product-strategy-canvas)
- [From Strategy to Objectives Masterclass](https://www.productcompass.pm/p/product-vision-strategy-objectives-course) (video course)
```

## vision-sft (3104-llm-finetuning)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/llm-finetuning
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3104-llm-finetuning/13295-vision-sft
- الوصف: Fine-tune vision-language models (VLMs) with supervised learning on image+text data. Use when adapting a VLM to a visual domain or task, configuring frozen-vision-tower LoRA, or debugging a VLM fine-tune that trains without learning.

```markdown
# Vision-Language SFT

This skill assumes `finetuning-method-selection`
already routed here: the data shape is
image+text demonstrations, not preference pairs
or a verifiable reward signal, and the base is a
vision-language model rather than a text-only
one. `lora-qlora-recipes` covers the text-only
LoRA/QLoRA recipe this skill specializes for the
vision tower and projector; read that skill first
if the LoRA fundamentals (rank, alpha, target
modules) aren't already familiar.

**Input:** an image+text dataset and a VLM base
model already picked from the model catalog.
**Output format:** a validated adapter config —
which components are frozen, LoRA target modules,
and a `min_pixels`/`max_pixels` budget — that
`llm-finetuning-training-engineer` consumes
directly when it generates a runnable script.

## Quick Reference

| Situation | Default |
|---|---|
| Adapting behavior on familiar images | Frozen tower+projector, LoRA r=8–16, α=16–32 |
| Visual domain shift | Unfreeze last-6 ViT layers, vision LR 5–10x lower |
| Doesn't fit in bf16 at target rank | QLoRA — frozen vision tower only |
| `fast_inference=True` | `finetune_vision_layers=False` |
| Loss normal, eval not improving | Check the Two Silent Killers below first |

## The Consensus Recipe

Freeze the vision tower and the projector. Put
LoRA on the LLM only, all-linear (the same
attention + MLP target list as text-only SFT —
see `lora-qlora-recipes`), at **r=8–16,
α=16–32**. This is the settled default for
adapting a VLM's behavior without disturbing how
it sees.

- **The vision tower and projector stay frozen by
  default.** They already encode a general visual
  representation; retraining them is rarely
  necessary and adds risk without adding
  capability for most tasks.
- **LoRA rank runs lower than the text-only
  general default** (r=8–16 here vs r=16–32 for
  text-only SFT) because the LLM-only adapter is
  adapting behavior, not injecting new visual
  knowledge.
- **QLoRA is permitted only with a frozen vision
  tower.** Quantizing the base while also
  unfreezing and training vision layers is
  unsupported and unstable — treat this as a hard
  pairing rule, not a tunable. If the vision tower
  needs to unfreeze, drop QLoRA and use bf16 LoRA
  instead.

```python
# freeze tower + projector; LoRA on LLM only
for name, param in model.named_parameters():
    if "vision_tower" in name or "projector" in name:
        param.requires_grad = False

target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]  # LLM-only, all-linear — r=8-16, alpha=16-32
```

## When to Unfreeze

Unfreezing vision layers is a deliberate
escalation, not a default decision — reach
for it only when the domain shift is
visual, not textual.
```

## vision-sft (3499-llm-finetuning)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/llm-finetuning
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3499-llm-finetuning/14242-vision-sft
- الوصف: Fine-tune vision-language models (VLMs) with supervised learning on image+text data. Use when adapting a VLM to a visual domain or task, configuring frozen-vision-tower LoRA, or debugging a VLM fine-tune that trains without learning.

```markdown
# Vision-Language SFT

This skill assumes `finetuning-method-selection`
already routed here: the data shape is
image+text demonstrations, not preference pairs
or a verifiable reward signal, and the base is a
vision-language model rather than a text-only
one. `lora-qlora-recipes` covers the text-only
LoRA/QLoRA recipe this skill specializes for the
vision tower and projector; read that skill first
if the LoRA fundamentals (rank, alpha, target
modules) aren't already familiar.

**Input:** an image+text dataset and a VLM base
model already picked from the model catalog.
**Output format:** a validated adapter config —
which components are frozen, LoRA target modules,
and a `min_pixels`/`max_pixels` budget — that
`llm-finetuning-training-engineer` consumes
directly when it generates a runnable script.

## Quick Reference

| Situation | Default |
|---|---|
| Adapting behavior on familiar images | Frozen tower+projector, LoRA r=8–16, α=16–32 |
| Visual domain shift | Unfreeze last-6 ViT layers, vision LR 5–10x lower |
| Doesn't fit in bf16 at target rank | QLoRA — frozen vision tower only |
| `fast_inference=True` | `finetune_vision_layers=False` |
| Loss normal, eval not improving | Check the Two Silent Killers below first |

## The Consensus Recipe

Freeze the vision tower and the projector. Put
LoRA on the LLM only, all-linear (the same
attention + MLP target list as text-only SFT —
see `lora-qlora-recipes`), at **r=8–16,
α=16–32**. This is the settled default for
adapting a VLM's behavior without disturbing how
it sees.

- **The vision tower and projector stay frozen by
  default.** They already encode a general visual
  representation; retraining them is rarely
  necessary and adds risk without adding
  capability for most tasks.
- **LoRA rank runs lower than the text-only
  general default** (r=8–16 here vs r=16–32 for
  text-only SFT) because the LLM-only adapter is
  adapting behavior, not injecting new visual
  knowledge.
- **QLoRA is permitted only with a frozen vision
  tower.** Quantizing the base while also
  unfreezing and training vision layers is
  unsupported and unstable — treat this as a hard
  pairing rule, not a tunable. If the vision tower
  needs to unfreeze, drop QLoRA and use bf16 LoRA
  instead.

```python
# freeze tower + projector; LoRA on LLM only
for name, param in model.named_parameters():
    if "vision_tower" in name or "projector" in name:
        param.requires_grad = False

target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]  # LLM-only, all-linear — r=8-16, alpha=16-32
```

## When to Unfreeze

Unfreezing vision layers is a deliberate
escalation, not a default decision — reach
for it only when the domain shift is
visual, not textual.
```

## pdf-ocr-adding (1387-pdf-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/erich3000/ji-agent-skills/tree/f729e5b38535f4d9889a383729843fb4e2fd01e4/plugins/pdf-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1387-pdf-skills/3268-pdf-ocr-adding
- الوصف: This skill should be used when a PDF has no text layer and cannot be searched or grepped — when the user asks to "make this pdf searchable", "run OCR", "PDF durchsuchbar machen", "Texterkennung", "das PDF lässt sich nicht durchsuchen", "warum findet die Suche nichts", or "run pdf-ocr-adding". Adds an invisible text layer with ocrmypdf while leaving the page images untouched. Complements pdf-compre

```markdown
# pdf-ocr-adding

Scanned PDFs carry no text. Every `grep`, `pdftotext` and full-text search over them silently returns
nothing — not an error, just no hits, which is the dangerous part. This skill adds an invisible OCR
text layer so the document becomes searchable, without touching how it looks.

## When this matters

Run the check **before** concluding that something is not in a document. A search that finds nothing
in a text-free PDF proves nothing at all.

```bash
pdftotext -layout "file.pdf" - | wc -c
```

A 12-page document returning a handful of bytes is a pure image scan. Real text runs to thousands of
characters per page.

## Workflow

### 1. Check the prerequisites

```bash
which ocrmypdf
tesseract --list-langs
```

If `ocrmypdf` is missing or `deu` is not among the languages, install both. Tell the user first, the
language pack is large:

```bash
brew install ocrmypdf tesseract-lang          # macOS
sudo apt install ocrmypdf tesseract-ocr-deu    # Debian/Ubuntu, one package per language
```

`tesseract-lang` is about 686 MB because it carries every language. Reversible with
`brew uninstall ocrmypdf tesseract-lang`.

### 2. Run the OCR into a scratchpad file

Never write directly over the original.

```bash
ocrmypdf -l deu --output-type pdf "input.pdf" "<scratchpad>/ocr_out.pdf"
```

- Set `-l` to the document's language: `deu` for German, `deu+eng` for mixed, `fra`, `ita` and so
  on. The default is English, which breaks umlauts and accents on other languages.
- ⚠️ **Do not use `--deskew` or `--rotate-pages` on documents that are already straight.** They force
  a re-encode of every page image. On a 842 KB contract this produced an 8.5 MB output, ten times the
  original. Without them, ocrmypdf's image optimisation usually makes the file *smaller*.
- If ocrmypdf reports that a page already has text, the file may be partly digital. `--force-ocr`
  rasterises everything and loses existing real text, `--redo-ocr` is the safer repair. Neither is
  needed for a plain scan.

### 2b. Pages with bad existing text: `--redo-ocr`

`--skip-text` silently leaves a page alone if it already carries text — including text from a *bad*
earlier OCR. Symptom: German words full of mangled characters, `FŠttigkeitsmitteilungen` instead of
`Fälligkeitsmitteilungen`. Such a file will not appear in a "no text layer" scan at all, because it
technically has one.

```bash
ocrmypdf -l deu --redo-ocr --output-type pdf "input.pdf" "<scratchpad>/ocr_out.pdf"
```

`--redo-ocr` strips the existing OCR layer and redoes it, while leaving genuine digital text alone.
Prefer it over `--force-ocr`, which rasterises the whole page and destroys real text.

### 3. Verify before replacing

Two checks, both cheap:

```bash
pdftotext -layout "<scratchpad>/ocr_out.pdf" - | wc -c
```
```
