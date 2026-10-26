# مصادر «بايثون المحترف» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## uv-package-manager (3510-python-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/python-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3510-python-development/14275-uv-package-manager
- الوصف: Master the uv package manager for fast Python dependency management, virtual environments, and modern Python project workflows. Use when setting up Python projects, managing dependencies, or optimizing Python development workflows with uv.

```markdown
# UV Package Manager

Comprehensive guide to using uv, an extremely fast Python package installer and resolver written in Rust, for modern Python project management and dependency workflows.

## When to Use This Skill

- Setting up new Python projects quickly
- Managing Python dependencies faster than pip
- Creating and managing virtual environments
- Installing Python interpreters
- Resolving dependency conflicts efficiently
- Migrating from pip/pip-tools/poetry
- Speeding up CI/CD pipelines
- Managing monorepo Python projects
- Working with lockfiles for reproducible builds
- Optimizing Docker builds with Python dependencies

## Core Concepts

### 1. What is uv?

- **Ultra-fast package installer**: 10-100x faster than pip
- **Written in Rust**: Leverages Rust's performance
- **Drop-in pip replacement**: Compatible with pip workflows
- **Virtual environment manager**: Create and manage venvs
- **Python installer**: Download and manage Python versions
- **Resolver**: Advanced dependency resolution
- **Lockfile support**: Reproducible installations

### 2. Key Features

- Blazing fast installation speeds
- Disk space efficient with global cache
- Compatible with pip, pip-tools, poetry
- Comprehensive dependency resolution
- Cross-platform support (Linux, macOS, Windows)
- No Python required for installation
- Built-in virtual environment support

### 3. UV vs Traditional Tools

- **vs pip**: 10-100x faster, better resolver
- **vs pip-tools**: Faster, simpler, better UX
- **vs poetry**: Faster, less opinionated, lighter
- **vs conda**: Faster, Python-focused

## Installation

### Quick Install

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pip (if you already have Python)
pip install uv

# Using Homebrew (macOS)
brew install uv

# Using cargo (if you have Rust)
cargo install --git https://github.com/astral-sh/uv uv
```

### Verify Installation

```bash
uv --version
# uv 0.x.x
```

## Quick Start

### Create a New Project

```bash
# Create new project with virtual environment
uv init my-project
cd my-project

# Or create in current directory
uv init .

# Initialize creates:
# - .python-version (Python version)
# - pyproject.toml (project config)
# - README.md
# - .gitignore
```

### Install Dependencies

```bash
# Install packages (creates venv if needed)
uv add requests pandas

# Install dev dependencies
uv add --dev pytest black ruff

# Install from requirements.txt
uv pip install -r requirements.txt

# Install from pyproject.toml
uv sync
```

## Virtual Environment Management

### Pattern 1: Creating Virtual Environments

```bash
# Create virtual environment with uv
uv venv

# Create with specific Python version
uv venv --python 3.12
```

## uv-package-manager (40-python-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/acaprino/daodan/tree/39443d215d28fcbc32d651895b3cc45c64f24b6f/exports/claude/plugins/python-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/40-python-development/61-uv-package-manager
- الوصف: Handle virtual environments, lockfiles and interpreter version pinning. TRIGGER WHEN: setting up Python projects, managing dependencies, migrating off pip/poetry, or optimizing Python development workflows with uv.

```markdown
# UV Package Manager

Use uv - an extremely fast Python package installer and resolver written in Rust - for modern Python project management and dependency workflows.

## When to Invoke

- Setting up new Python projects or managing dependencies
- Creating and managing virtual environments
- Installing or switching Python interpreter versions
- Resolving dependency conflicts efficiently
- Migrating from pip, pip-tools, or poetry to uv
- Speeding up CI/CD pipelines with faster installs
- Working with lockfiles for reproducible builds
- Managing monorepo Python projects with workspaces

## Core Concepts

### What is uv?
- **Ultra-fast package installer**: 10-100x faster than pip
- **Written in Rust**: Leverages Rust's performance
- **Drop-in pip replacement**: Compatible with pip workflows
- **Virtual environment manager**: Create and manage venvs
- **Python installer**: Download and manage Python versions
- **Lockfile support**: Reproducible installations

### UV vs Traditional Tools
- **vs pip**: 10-100x faster, better resolver
- **vs pip-tools**: Faster, simpler, better UX
- **vs poetry**: Faster, less opinionated, lighter
- **vs conda**: Faster, Python-focused

## Installation

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pip
pip install uv

# Using Homebrew (macOS)
brew install uv

# Verify
uv --version
```

## Quick Start

```bash
# Create new project
uv init my-project
cd my-project

# Install packages (creates venv if needed)
uv add requests pandas

# Install dev dependencies
uv add --dev pytest black ruff

# Install from requirements.txt
uv pip install -r requirements.txt

# Sync from pyproject.toml
uv sync
```

## Virtual Environment Management

```bash
# Create virtual environment
uv venv
uv venv --python 3.12
uv venv my-env

# Activate
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\activate.bat         # Windows CMD
.venv\Scripts\Activate.ps1         # Windows PowerShell

# Or skip activation with uv run
uv run python script.py
uv run pytest
uv run --python 3.11 python script.py
```

## Package Management

### Adding Dependencies

```bash
uv add requests
uv add "django>=4.0,<5.0"
uv add numpy pandas matplotlib
uv add --dev pytest pytest-cov
uv add --optional docs sphinx
uv add git+https://github.com/user/repo.git
uv add git+https://github.com/user/repo.git@v1.0.0
uv add ./local-package
uv add -e ./local-package
```

### Removing and Upgrading

```bash
uv remove requests
uv remove --dev pytest
uv add --upgrade requests
uv sync --upgrade
uv tree --outdated
```

### Locking Dependencies

```bash
uv lock
uv lock --upgrade
uv lock --upgrade-package requests
uv lock --check
```

## Python Version Management

```bash
```

## uv-package-manager (80-python-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/acaprino/daodan/tree/39443d215d28fcbc32d651895b3cc45c64f24b6f/exports/codex/plugins/python-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/80-python-development/160-uv-package-manager
- الوصف: Handle virtual environments, lockfiles and interpreter version pinning. TRIGGER WHEN: setting up Python projects, managing dependencies, migrating off pip/poetry, or optimizing Python development workflows with uv.

```markdown
# UV Package Manager

Use uv - an extremely fast Python package installer and resolver written in Rust - for modern Python project management and dependency workflows.

## When to Invoke

- Setting up new Python projects or managing dependencies
- Creating and managing virtual environments
- Installing or switching Python interpreter versions
- Resolving dependency conflicts efficiently
- Migrating from pip, pip-tools, or poetry to uv
- Speeding up CI/CD pipelines with faster installs
- Working with lockfiles for reproducible builds
- Managing monorepo Python projects with workspaces

## Core Concepts

### What is uv?
- **Ultra-fast package installer**: 10-100x faster than pip
- **Written in Rust**: Leverages Rust's performance
- **Drop-in pip replacement**: Compatible with pip workflows
- **Virtual environment manager**: Create and manage venvs
- **Python installer**: Download and manage Python versions
- **Lockfile support**: Reproducible installations

### UV vs Traditional Tools
- **vs pip**: 10-100x faster, better resolver
- **vs pip-tools**: Faster, simpler, better UX
- **vs poetry**: Faster, less opinionated, lighter
- **vs conda**: Faster, Python-focused

## Installation

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pip
pip install uv

# Using Homebrew (macOS)
brew install uv

# Verify
uv --version
```

## Quick Start

```bash
# Create new project
uv init my-project
cd my-project

# Install packages (creates venv if needed)
uv add requests pandas

# Install dev dependencies
uv add --dev pytest black ruff

# Install from requirements.txt
uv pip install -r requirements.txt

# Sync from pyproject.toml
uv sync
```

## Virtual Environment Management

```bash
# Create virtual environment
uv venv
uv venv --python 3.12
uv venv my-env

# Activate
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\activate.bat         # Windows CMD
.venv\Scripts\Activate.ps1         # Windows PowerShell

# Or skip activation with uv run
uv run python script.py
uv run pytest
uv run --python 3.11 python script.py
```

## Package Management

### Adding Dependencies

```bash
uv add requests
uv add "django>=4.0,<5.0"
uv add numpy pandas matplotlib
uv add --dev pytest pytest-cov
uv add --optional docs sphinx
uv add git+https://github.com/user/repo.git
uv add git+https://github.com/user/repo.git@v1.0.0
uv add ./local-package
uv add -e ./local-package
```

### Removing and Upgrading

```bash
uv remove requests
uv remove --dev pytest
uv add --upgrade requests
uv sync --upgrade
uv tree --outdated
```

### Locking Dependencies

```bash
uv lock
uv lock --upgrade
uv lock --upgrade-package requests
uv lock --check
```

## Python Version Management

```bash
```

## uv-python-versions (2166-python-plugin)

- الترخيص: **MIT**  ·  الأصل: https://github.com/laurigates/claude-plugins/tree/9caa2be8e7b4b35823e4154c610e3846af05635c/python-plugin
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2166-python-plugin/7857-uv-python-versions
- الوصف: Install and manage Python interpreter versions with uv. Use when the user mentions installing Python versions, .python-version, uv python, or managing CPython/PyPy.

```markdown
# UV Python Version Management

Quick reference for installing and managing Python interpreter versions with UV.

## When to Use This Skill

| Use this skill when... | Use a focused sibling instead when... |
|---|---|
| Installing a specific CPython or PyPy interpreter with `uv python install` | Adding a Python library to a project — use uv-project-management |
| Pinning a project to a Python version via `.python-version` or `requires-python` | Installing a global Python CLI tool — use uv-tool-management |
| Switching between multiple installed interpreters for testing | Running a script with auto-managed Python — use uv-run |

## When This Skill Applies

- Installing specific Python versions
- Switching between multiple Python versions
- Pinning Python versions for projects
- Managing CPython and PyPy interpreters
- Finding and listing installed Python versions

## Quick Reference

### Installing Python Versions

```bash
# Install latest Python
uv python install

# Install specific version
uv python install 3.11
uv python install 3.12
uv python install 3.10 3.11 3.12

# Install exact version
uv python install 3.11.5
uv python install cpython@3.11.5

# Install PyPy
uv python install pypy@3.9
uv python install pypy@3.10
```

### Listing Python Versions

```bash
# List all available versions
uv python list

# List only installed versions
uv python list --only-installed

# List with verbose details
uv python list --verbose
```

### Pinning Python Versions

```bash
# Pin version for current project
uv python pin 3.11
uv python pin 3.12.1

# Pin PyPy
uv python pin pypy@3.9

# Pin with version file
# Creates/updates .python-version
```

### Finding Python Interpreters

```bash
# Find any Python installation
uv python find

# Find specific version
uv python find 3.11
uv python find 3.12

# Find PyPy
uv python find pypy
uv python find pypy@3.9
```

### Using Specific Python Versions

```bash
# In project commands
uv run --python 3.11 script.py
uv run --python 3.12 pytest

# Creating virtual environments
uv venv --python 3.11
uv venv --python 3.10 .venv-py310

# Initializing projects
uv init --python 3.12 my-project
```

## Python Version Sources

UV searches for Python in this order:
1. **UV-managed** - Installed via `uv python install`
2. **.python-version** - Pin file in project directory
3. **pyproject.toml** - `requires-python` field
4. **System Python** - Existing system installations
5. **Environment** - `$PATH` and standard locations

## Version Pinning

### .python-version File

```bash
# Pin creates this file
uv python pin 3.11

# File contents
3.11

# Exact version
uv python pin 3.11.5
```

### pyproject.toml

```toml
[project]
requires-python = ">=3.11"

# UV respects this constraint
```

## Supported Python Implementations

### CPython

```bash
```

## python-typing-reference (1111-python-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cjthompson/claude-code-config/tree/6f33f44a10ad9ad209ab5c916e2e365ad8dac25a/plugins/python-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1111-python-development/2529-python-typing-reference
- الوصف: Answer detailed or normative questions about Python's type system using the complete vendored typing specification. Use for subtle assignability, generics, variance, protocols, overloads, narrowing, qualifiers, TypedDict, or checker-semantics questions that exceed everyday annotation guidance.

```markdown
# Python Typing Reference

Use the vendored specification as the authority rather than relying on recollection.

1. Read `references/topic-index.md` to select the smallest relevant specification files.
2. Read those files under `../../vendor/typing-spec/` completely enough to capture definitions, rules, examples, and exceptions.
3. Distinguish normative typing rules from a particular checker's implementation or extension.
4. State version-sensitive assumptions and use the project's declared Python version and checker.
5. Explain the result with the smallest useful example and name the source files consulted.
```

## python-typing (1112-python-scripting)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cjthompson/claude-code-config/tree/6f33f44a10ad9ad209ab5c916e2e365ad8dac25a/plugins/python-scripting
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1112-python-scripting/2534-python-typing
- الوصف: Use when writing or editing typed Python scripts, parsing untyped input, choosing lightweight data shapes, or resolving common checker errors without project-scale type-system research.

```markdown
# Python Typing

Make untyped boundaries narrow and typed internals boring.

## Establish the target

- Follow the project's minimum Python version before choosing annotation
  syntax or imports from `typing`.
- Type every function parameter and return value, including `-> None`.
- Annotate empty containers, mutable state, and values crossing an untyped
  library boundary when inference is ambiguous.

## Type the boundary first

- Treat JSON, plist data, environment values, and other untrusted input as
  `object`, then narrow with `isinstance`. Untrusted does not mean `Any`.
- Validate container shape and each required value before constructing the
  typed internal representation.
- Remember that `bool` is an `int` subclass: reject it explicitly when a true
  integer is required.
- Parse CLI and text inputs at the edge. Pass typed values into the script's
  working functions.

```python
def require_count(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("count must be an integer")
    return value
```

## Pick the smallest useful model

- Use `TypedDict` when validated data must remain dictionary-shaped, such as a
  JSON record.
- Use a frozen dataclass for an internal value object with behavior or useful
  construction semantics.
- Use `Literal` or an enum for a genuinely closed set of values; otherwise use
  `str` plus validation.
- Do not add Pydantic or another runtime model dependency to a small script
  unless runtime schema features justify it.

## Make relationships honest

- Use `T | None` only when absence is valid, and narrow it before use.
- Prefer precise concrete types inside the implementation. At call boundaries,
  accept `Sequence`, `Mapping`, `Iterable`, or `Callable` when callers benefit
  and the function requires only that behavior.
- Type callbacks with their real parameters and result rather than `Callable`
  without arguments.
- Add `Protocol`, overloads, generics, type guards, or `Self` only when the
  implementation establishes the relationship they express.
- Let inference handle obvious local values; annotations should communicate or
  constrain, not repeat every literal.

## Deal with uncertainty visibly

- Avoid `cast()`, broad unions, `Any`, and `# type: ignore` as ways to silence a
  checker. Prefer validation, narrowing, or a small typed adapter.
- If a dependency is genuinely untyped, contain `Any` in one adapter and return
  a validated precise type from it.
- If an ignore is unavoidable, use the narrow error code supported by the
  configured checker and explain the external limitation.

Run the configured checker after editing and fix the source rather than merely
reducing the error count.
```
