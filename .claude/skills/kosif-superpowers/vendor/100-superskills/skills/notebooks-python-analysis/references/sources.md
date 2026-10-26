# مصادر «دفاتر Python للتحليل» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## jupyter-ml-notebook (2747-charly-jupyter)

- الترخيص: **MIT**  ·  الأصل: https://github.com/opencharly/marketplace/tree/d87e6f94bba069eaf7f4a8e68cbd669b5a8d7aeb/jupyter
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2747-charly-jupyter/10836-jupyter-ml-notebook
- الوصف: Full CUDA ML JupyterLab box with finetuning, Ollama, and LLM course notebooks, CRDT MCP server, and real-time collaboration. Base: nvidia. Port 8888. Combines jupyter-ml with 37 Unsloth fine-tuning notebooks, 6 Ollama integration notebooks, and 15 LLM course notebooks. MUST be invoked before building, deploying, or troubleshooting the jupyter-ml-notebook box.

```markdown
# jupyter-ml-notebook -- GPU ML Jupyter with Fine-tuning Notebooks

## Box Definition

```yaml
jupyter-ml-notebook:
  base: nvidia
  candy:
    - agent-forwarding
    - jupyter-ml
    - notebook-templates
    - notebook-finetuning
    - notebook-ollama
    - notebook-llm-on-supercomputers
    - notebook-openrouter
    - '@github.com/opencharly/pod-dbus'
    - charly
  ports:
    - "8888:8888"
  platforms:
    - linux/amd64
```

## What's Different from jupyter-ml

This box is identical to `jupyter-ml` with two data candy additions:
- `notebook-finetuning` — seeds 37 Unsloth fine-tuning notebooks into `/workspace/finetuning/`
- `notebook-ollama` — seeds 6 Ollama integration notebooks into `/workspace/ollama/`

The Ollama notebooks require a running `ollama` deployment. When deployed via `charly config ollama --update-all`, the `OLLAMA_HOST` env var is automatically injected via `env_provide` -- no manual configuration needed.

## Candy Composition

- `jupyter-ml` — Tier 2 environment-owning meta-layer (PyTorch >= 2.10.0, vLLM 0.19, unsloth, LangChain, CRDT MCP via jupyter-mcp sub-candy)
- `notebook-templates` — Starter notebooks (data candy, seeds /workspace)
- `notebook-finetuning` — 37 Unsloth fine-tuning notebooks (data candy, seeds /workspace/finetuning/)
- `notebook-ollama` — 6 Ollama integration notebooks (data candy, seeds /workspace/ollama/)
- `notebook-llm-on-supercomputers` — 15 LLM course notebooks (data candy, seeds /workspace/llms_on_supercomputers/)
- `agent-forwarding` — SSH/GPG agent forwarding
- `dbus` — D-Bus session bus
- `charly` — OpenCharly CLI

## Ports

| Port | Service |
|------|---------|
| 8888 | JupyterLab + MCP endpoint at `/mcp` |

## Volumes

| Name | Path | Purpose |
|------|------|---------|
| workspace | /workspace | Persistent notebook storage |
| models | ~/.cache/huggingface | HuggingFace model cache (from unsloth sub-candy) |

## Data Candies

| Candy | Target | Dest | Contents |
|-------|--------|------|----------|
| notebook-templates | workspace | *(root)* | getting-started.ipynb |
| notebook-finetuning | workspace | finetuning/ | 37 Unsloth notebooks (SFT, GRPO, DPO, RLOO, QLoRA) |
| notebook-ollama | workspace | ollama/ | 6 Ollama API notebooks (requests, OpenAI, ollama lib, GPU, HuggingFace, Anthropic) |
| notebook-llm-on-supercomputers | workspace | llms_on_supercomputers/ | 15 LLM course notebooks (prompt engineering, RAG, fine-tuning) + datasets |

## File Layout in JupyterLab

```
/workspace/
  getting-started.ipynb                    (from notebook-templates)
  finetuning/                               (from notebook-finetuning)
    .env.example
    notebooks.yaml
    00_Unsloth_Setup.ipynb
    01_FastInference_Llama.ipynb
    01_FastInference_Qwen.ipynb
    02_Vision_Training_Ministral.ipynb
```

## jupyter-mcp (2747-charly-jupyter)

- الترخيص: **MIT**  ·  الأصل: https://github.com/opencharly/marketplace/tree/d87e6f94bba069eaf7f4a8e68cbd669b5a8d7aeb/jupyter
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2747-charly-jupyter/10834-jupyter-mcp
- الوصف: JupyterLab CRDT MCP server extension exposing the notebook tools (notebook_*/cell_* + room_list + notebook_list_users) for programmatic notebook access. MUST be invoked when working with: the MCP server implementation, CRDT collaboration, the auto-attach single-room invariant, or the Tier 1 pip-only installation pattern for jupyter extensions.

```markdown
# jupyter-mcp -- JupyterLab CRDT MCP server extension

## Candy Properties

| Property | Value |
|----------|-------|
| Dependencies | *(none)* |
| Packages | *(none -- pip-only Tier 1 candy)* |
| Services | *(none)* |
| Volumes | *(none)* |
| Install files | `charly.yml`, `task:`, `jupyter_mcp/` (Python package) |

## Architecture: Tier 1 Post-Install Layer

This is a **Tier 1 "post-install"** layer — it has no `pixi.toml` and installs into whatever pixi environment exists from the parent Tier 2 candy. It follows the same pattern as `llama-cpp` and `unsloth`.

**Single source of truth:** The `jupyter_mcp` Python package lives only in this candy. Both `jupyter` (lightweight) and `jupyter-ml` (GPU ML) compose it via their `candy:` field. This prevents code duplication and ensures bug fixes propagate to all boxes.

## Usage philosophy and caveats

The MCP server **manages CRDT rooms invisibly**. Clients see notebooks and cells; the server takes care of room lifecycle. Reading or mutating any notebook just works — call `cell_get`, `cell_update`, `notebook_get` directly.

- **MCP works WITH the user.** Every `notebook_*` and `cell_*` tool auto-attaches to whichever CRDT room exists for the path (JupyterLab UI tab, another MCP session, or this one), or creates a fresh room if none exists. Calling `cell_update` on a notebook the user has open in JupyterLab edits THAT EXACT Y.Doc — the user sees changes in real time. **There is no scenario where MCP and UI work in parallel rooms.**
- **No client-side room management.** Clients do not open or close CRDT rooms. Idle rooms (no clients, no MCP activity for `MCP_ROOM_IDLE_TIMEOUT_SEC`, default 600s) are flushed and closed by a server-side sweeper. Configure the timeout via env var on the candy for fast tests.
- **`cell_update` is atomic by `cell_id`.** The cell's stable identifier is preserved across the update, so a sequence of `cell_update` calls never duplicates cells even when the room has concurrent state.
- **Path canonicalization.** Any path you pass — `"foo.ipynb"`, `"./foo.ipynb"`, `"/workspace/foo.ipynb"` — is normalized to the workspace-relative form before reaching `file_id_manager.index()`. All three converge on the same room. Host paths and `..` escapes are rejected with a clear error.
- **Single room per notebook is an INVARIANT.** Two MCP sessions plus the JupyterLab UI editing the same notebook ALL share one Y.Doc. If `room_list` ever shows two entries for the same logical file, that's a regression — open a bug.
```

## jupyter (620-jupyter-setup)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/jupyter-setup
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/620-jupyter-setup/1649-jupyter
- الوصف: Generate Jupyter notebook project setup with kernels

```markdown
Generate Jupyter notebook project setup with kernels. This plugin is part of the Plugin Hub developer tools collection.

Use the tools provided by the plugin-hub MCP server to accomplish tasks related to jupyter-setup.
```

## macos-python-scripting (1112-python-scripting)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cjthompson/claude-code-config/tree/6f33f44a10ad9ad209ab5c916e2e365ad8dac25a/plugins/python-scripting
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1112-python-scripting/2531-macos-python-scripting
- الوصف: Use when writing zero-setup macOS utilities for Apple's /usr/bin/python3, Command Line Tools Python 3.9, standard-library-only execution, or integration with stable macOS command-line programs.

```markdown
# macOS Python Scripting

Produce utilities that run without Homebrew, uv, pip, or a virtual environment.

- Start executable files with exactly `#!/usr/bin/python3`.
- Target Python 3.9 syntax: use `Optional[T]` and `Union[A, B]` rather than
  `T | None`; do not use `match`, `tomllib`, `typing.Self`, or newer APIs.
- Import only the Python 3.9 standard library. Do not rely on Apple-bundled or
  user `site-packages`, including `pip`, `setuptools`, `six`, or `future`.
- Use standard modules such as `argparse`, `json`, `plistlib`, `pathlib`, and
  `subprocess`. Type all functions and ambiguous containers. Treat decoded
  plist and JSON values as `object`, narrow them with `isinstance`, and avoid
  `Any` as a shortcut.
- Invoke stable macOS programs with absolute paths and argument arrays, for
  example `subprocess.run(["/usr/bin/open", url], check=True)`. Never use
  `shell=True` for data-derived arguments.
- Handle `OSError`, parse errors, and `subprocess.CalledProcessError` at the
  CLI boundary and return a nonzero exit status with a concise stderr message.
- Verify syntax, imports, and behavior without environment leakage:

  ```bash
  /usr/bin/python3 -E -s -S path/to/script.py --help
  /usr/bin/python3 -E -s -S path/to/script.py <test arguments>
  ```

  `unittest` is included with Apple Python 3.9. With `python -m unittest`,
  positional test targets are dotted module names, not filesystem paths. To run
  tests selected by directory and filename pattern, use discovery:

  ```bash
  /usr/bin/python3 -m unittest discover \
    -s <test-start-directory> \
    -p '<test-file-pattern>' -v
  ```

  Replace the placeholders with the directory to search and its test-file
  pattern. For an importable test module, pass its dotted module name instead
  of its file path.

If `/usr/bin/python3` is unavailable, report that Apple Command Line Tools are
required. Do not install or modify the interpreter.
```

## python-simple-scripts (1112-python-scripting)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cjthompson/claude-code-config/tree/6f33f44a10ad9ad209ab5c916e2e365ad8dac25a/plugins/python-scripting
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1112-python-scripting/2533-python-simple-scripts
- الوصف: Use before any Bash command that invokes Python, including Bash(python3 ...), Bash(python ...), python3 -c, python -c, Python heredocs, and temporary .py helper files. Also use whenever an agent creates a one-off Python script to inspect, transform, validate, or summarize data during a coding session, even when the user did not ask for Python or for a script.

```markdown
# Simple Python Scripts

Write the smallest trustworthy helper for the immediate task.

Loading this skill does not mean every Python invocation needs new code. If the
command only runs an existing script, module, test suite, or configured project
tool, preserve that command and do not manufacture a helper. Apply the rules
below when composing Python for the task.

## Distinguish a helper from a deliverable

For an incidental helper used by the agent during a coding session:

- Use the Python interpreter already available in the execution environment.
  Do not ask the user to choose a supported Python version.
- Do not create `pyproject.toml`, a package layout, a lockfile, a virtual
  environment, or project configuration.
- Use the standard library. Do not install or download runtime dependencies,
  formatters, linters, or type checkers for the helper.
- Keep caches out of the working tree. Prefer `python3 -B helper.py` when bytecode
  is unnecessary.
- Keep the helper temporary unless the user asks to retain it. If it is retained
  for audit, report its path.

For a script requested as a repository deliverable, stop treating it as an
incidental helper. Use applicable skills from `python-development` when
available; otherwise use applicable skills from `python-scripting`. Follow the
repository's declared Python version and toolchain. If no supported version is
declared, ask and offer Python 3.14 as the default.

For Apple's `/usr/bin/python3` or a zero-setup macOS utility, also use
`macos-python-scripting` and follow its Python 3.9 constraints.

## Choose a proportionate form

- Use `python3 -c` only for a short expression whose shell quoting is obvious.
- Use a small temporary `.py` file for multiline logic, structured data,
  nontrivial error handling, or anything worth rerunning.
- Prefer one helper over a chain of opaque shell pipelines.
- Do not add a second verifier, framework, abstraction layer, or generalized
  CLI unless the task's risk or reuse justifies it.

For a multiline helper, normally use focused functions, complete function
signatures, a `main()` entry point, and an explicit exit status. Let inference
handle obvious local values rather than annotating every literal.

## Cross the shell boundary safely

- Prefer a temporary `.py` file once code is multiline or contains nested
  quoting. Do not compress substantial logic into `python3 -c`.
- If a heredoc is genuinely the clearest form, quote its delimiter as
  `<<'PY'` so Bash does not expand `$`, backticks, or backslashes inside the
  Python source.
- Never splice paths, JSON, user text, or command output into Python source.
  Pass dynamic values through positional arguments, stdin, or environment
  variables, then parse them in Python.
```

## python-guidelines (1433-python-skills)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/fcakyon/claude-codex-settings/tree/d3974af4e8991489df54c87b51989e13d3d6f265/plugins/python-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1433-python-skills/3415-python-guidelines
- الوصف: This skill should be used when writing, reviewing, or refactoring Python code. Covers code integration, idiomatic patterns, docstring formatting, anti-abstraction rules, and software engineering basics.

```markdown
# Python Guidelines

**Integrate into existing code. Don't append to it.**

> Simple is better than complex. Flat is better than nested.
> Errors should never pass silently. Unless explicitly silenced.
> If the implementation is hard to explain, it's a bad idea.
>
> -- The Zen of Python (PEP 20)

## Code Philosophy

- Match existing naming, importing, and signature patterns. Use existing utilities and data structures.
- Functions have a single purpose. Don't hardcode behavior that makes them less general.
- No trivial wrappers for 2 lines or less. Inline it.
- Inline single-use variables at the usage site.
- No try/except unless critical. Let errors surface.
- No duplicate code.
- Functions handle their own input validation. No if-else checks in main.
- Use pathlib, not os.path.
- Consider API and time costs for MongoDB/Gemini/OpenAI/Claude/Voyage.

Don't do this:

```python
# Generate comment report only if requested
if include_comments:
    comment_report = generate_comments_report(start_date, end_date, team, verbose)
else:
    comment_report = ""
    print("   Skipping comment analysis (disabled)")
```

Do this:

```python
comment_report = generate_comments_report(start_date, end_date, team, verbose) if include_comments else ""
```

Ask yourself: "Am I adding code, or integrating into what exists?"

## Simplicity Over Abstraction

**YAGNI: You Aren't Gonna Need It.**

Don't build for hypothetical future requirements. Add complexity only when the current task demands it.

Avoid:

- Abstract base classes for a single implementation
- Configuration options nobody asked for
- Error handling for impossible scenarios
- Wrapper classes around a single function
- Dependency injection when direct calls work
- Generic type parameters for one concrete type

Three similar lines of code is better than a premature abstraction. Refactor when the third real use case appears, not before.

But simplicity does not mean chaos. Always maintain:

- Clear function names that describe what they do
- Logical grouping of related code into modules
- Consistent naming conventions across the project
- Clean separation between I/O and logic
- Explicit parameters over global state or side effects

Ask yourself: "Is this abstraction solving a problem I have right now, or one I'm imagining?"

## Environment

- **Package manager**: uv (NOT pip)
- **Virtual env**: `source .venv/bin/activate` or `uv run python -c "..."`
- **3rd party packages**: Find source with `python -c "import pkg; print(pkg.__file__)"`, then Read.

## Testing Discipline

Never assume anything. Run `python -c "..."` to verify hypotheses about code behavior, package functions, or data structures before suggesting a plan or exiting plan mode.
```
