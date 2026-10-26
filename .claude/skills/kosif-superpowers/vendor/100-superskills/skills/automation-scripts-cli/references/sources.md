# مصادر «سكربتات الأتمتة وأدوات سطر الأوامر» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## go-cli-release-automation (2199-lvtd-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/LVTD-LLC/skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8098-go-cli-release-automation
- الوصف: Design, implement, and review secure Go CLI release automation with versioned tags, GoReleaser, GitHub Actions, checksums, signing, provenance, changelogs, Homebrew distribution, least-privilege credentials, verification, and recovery. Use when publishing CLI artifacts, configuring release CI, adding package-manager delivery, or diagnosing a partial or failed release.

```markdown
# Go CLI Release Automation

Treat release automation as a state transition with verifiable inputs, immutable
artifacts, least privilege, and an explicit recovery path.

## Core Workflow

1. Define version, supported targets, artifact names, and release authority.
2. Validate release configuration without publishing.
3. Build final artifacts exactly once from a clean tagged commit and generate checksums.
4. Publish through pinned, least-privilege CI with protected environments.
5. Update package-manager metadata from the published artifacts.
6. Install and smoke-test representative artifacts.
7. Record partial state and recover without silently replacing released bytes.

## Read Next

| Task | Load |
|---|---|
| Design and validate the pipeline | `guidelines.md`, `workflows/validate-release-config.md` |
| Publish a tagged release | `workflows/publish-tagged-release.md` |
| Publish Homebrew metadata | `workflows/publish-homebrew-package.md` |
| Recover a failed release | `workflows/recover-failed-release.md` |
| Review security and reproducibility | `references/release-automation/rules.md` |
| Review examples | `references/release-automation/examples.md` |

## Guardrails

- Never release from an unreviewed or dirty source state.
- Do not grant write tokens to pull-request jobs or untrusted code.
- Pin CI actions and use current, supported GoReleaser configuration.
- Do not treat build tags as authorization controls.
- Do not overwrite published artifacts under the same version.
- Do not accept locally rebuilt bytes as recovery evidence.

## Source Notes

Guidance is transformed and paraphrased from Marian Montagnino,
*Building Modern CLI Applications in Go* (Packt, 2023), Chapters 7 and 12-14,
and Ricardo Gerardi, *Powerful Command-Line Applications in Go* (2021).

Verify current configuration against https://goreleaser.com/,
https://docs.github.com/en/actions/reference/security/secure-use, and the
target package manager. Current GoReleaser deprecations must be checked before use.
```

## google-workspace-cli (150-google-workspace-cli)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/engineering-team/google-workspace-cli
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/150-google-workspace-cli/493-google-workspace-cli
- الوصف: Google Workspace administration via the gws CLI (github.com/googleworkspace/cli). Install, authenticate, and automate Gmail, Drive, Sheets, Calendar, Docs, Chat, and Tasks. Run security audits and use local recipe templates and persona bundles. Use for Google Workspace admin, gws CLI setup, Gmail automation, Drive management, or Calendar scheduling.

```markdown
# Google Workspace CLI

Expert guidance and automation for Google Workspace administration using the open-source `gws` CLI ([github.com/googleworkspace/cli](https://github.com/googleworkspace/cli), Apache-2.0). The CLI builds its command surface dynamically from Google's Discovery Service, so it covers every supported Workspace API plus `+`-prefixed helper commands. This skill adds local Python tools (doctor, auth guide, recipe catalog, security audit, output analyzer).

> **Verify before scripting:** `gws` generates commands at runtime from Google's API discovery documents, and the CLI is pre-v1.0. Always confirm a command's exact surface with `gws --help`, `gws <service> --help`, or `gws schema <service>.<resource>.<method>` before putting it in automation. Commands in this skill marked *(verify)* are illustrative of the `gws <service> <resource> <method>` pattern and must be checked against your installed version.

---

## Quick Start

### Check Installation

```bash
# Verify gws is installed and authenticated
python3 scripts/gws_doctor.py
```

### Send an Email

```bash
gws gmail +send --to "team@company.com" \
  --subject "Weekly Update" --body "Here's this week's summary..."
```

### List Drive Files

```bash
gws drive files list --params '{"pageSize": 20}' | python3 scripts/output_analyzer.py --select "name,mimeType,modifiedTime" --format table
```

---

## Installation

### npm (recommended; requires Node.js 18+)

```bash
npm install -g @googleworkspace/cli
gws --version
```

### Homebrew (macOS/Linux)

```bash
brew install googleworkspace-cli
```

### Cargo (from source)

```bash
cargo install --git https://github.com/googleworkspace/cli --locked
gws --version
```

### Pre-built Binaries

Download from [github.com/googleworkspace/cli/releases](https://github.com/googleworkspace/cli/releases) for macOS, Linux, or Windows. Nix users: `nix run github:googleworkspace/cli`.

### Verify Installation

```bash
python3 scripts/gws_doctor.py
# Checks: PATH, version, auth status, service connectivity
```

---

## Authentication

### OAuth Setup (Interactive)

```bash
# Step 1: Create Google Cloud project and OAuth credentials
python3 scripts/auth_setup_guide.py --guide oauth

# Step 2: Run interactive auth setup (uses gcloud if available)
gws auth setup

# Step 3: Log in, requesting only the scopes you need
gws auth login -s drive,gmail,sheets
```

### Headless/CI

```bash
# Generate setup instructions
python3 scripts/auth_setup_guide.py --guide service-account

# Export credentials from an interactive machine, then point the CLI at them
gws auth export --unmasked > credentials.json
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/credentials.json
```

### Environment Variables

```bash
# Generate .env template
```

## cli-design-and-arg-parsing (2255-cli-tooling-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/cli-tooling-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2255-cli-tooling-engineering/8587-cli-design-and-arg-parsing
- الوصف: Design a CLI's command/subcommand surface, flags vs positionals, and config precedence (flags > env > file > default), then pick the idiomatic parser for the language. Use when starting a CLI or reworking a messy one.

```markdown
# CLI Design & Argument Parsing

## The command surface

| Tool shape | Use |
|---|---|
| `tool [flags] <input>` (flat) | Single-purpose tool (one operation) |
| `tool <noun> <verb> [flags]` (subcommands) | Multi-feature tool — `git`, `docker`, `kubectl` style |
| Library + thin CLI | Logic other programs should call |

- **Positional** = *what* the command acts on (required input). **Flag** = *how* it behaves (optional, with a sensible default).
- Separate **global** flags (apply to all subcommands) from **command-local** ones.
- Reserve the conventional flags: `-h/--help`, `--version`, `-v/--verbose`, `-q/--quiet`, `--json`, `--no-color`, `--force`/`-y/--yes`.
- Make the common case need **no flags** — good defaults beat required configuration.

## Config precedence (highest wins)

`flag > env var > project config file > user config file > built-in default`

Resolve all sources into **one config object** early; pass it down. Never let a file silently beat an explicit flag. Discover user config via XDG (`$XDG_CONFIG_HOME` → `~/.config`).

## Pick the idiomatic parser (never hand-roll argv)

| Language | Parser |
|---|---|
| Go | Cobra + pflag |
| Rust | clap (derive) |
| Python | argparse (stdlib) / Click / Typer |
| Node/TS | oclif (multi-command) / yargs / commander |

The parser gives you help generation, value validation, and shell completions for free — losing those is the cost of hand-rolling.

See [`../../knowledge/cli-tooling-decision-trees.md`](../../knowledge/cli-tooling-decision-trees.md) for the command-surface and framework-choice trees.
```

## cli-cfg (449-cli-config)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/cli-config
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/449-cli-config/1478-cli-cfg
- الوصف: Generate CLI configuration file management

```markdown
Generate CLI configuration file management. This plugin is part of the Plugin Hub developer tools collection.

Use the tools provided by the plugin-hub MCP server to accomplish tasks related to cli-config.
```

## add-scrut-cli-tests (1002-add-scrut-cli-tests)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cboone/agent-harness-plugins/tree/d9e1b396852487c90500486a7b4fe94d88c64bd0/plugins/add-scrut-cli-tests
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1002-add-scrut-cli-tests/2286-add-scrut-cli-tests
- الوصف: Set up scrut snapshot testing in a CLI project that lacks it. Use for "add scrut tests" or "set up CLI integration tests".

```markdown
# Add Scrut CLI Tests

Set up [scrut](https://github.com/facebookincubator/scrut) snapshot-based CLI integration testing for a CLI project with Makefile targets and CI workflow integration.

## Prerequisites

- A CLI project that produces a binary or has an executable entry point
- A `.github/workflows/ci.yml` workflow (or equivalent CI workflow file) is recommended for CI integration

## Workflow

### 1. Detect the Project Type

Identify the project language by checking for manifest files:

| Marker(s)                        | Language |
| -------------------------------- | -------- |
| `go.mod`                         | Go       |
| `Package.swift`                  | Swift    |
| `Cargo.toml`                     | Rust     |
| `build.zig`                      | Zig      |
| `pyproject.toml`, `setup.py`     | Python   |
| `Gemfile`, `*.gemspec`           | Ruby     |
| Executable scripts (no manifest) | Shell    |

If no manifest is found and executable shell scripts exist in the root, `bin/`, or `scripts/`, treat the project as a shell script CLI.

If the project type cannot be determined, ask the user what language the project uses and where the binary or executable is located.

Check for an existing `tests/scrut/` directory; if present, warn and ask whether to add to it or abort.

### 2. Gather Project Information

Collect the following, inferring from existing files where possible:

- **Binary name**: determine by project type:
  - **Go**: check the Makefile `build` target for the output binary name (look for `-o bin/NAME` or `-o NAME`), or derive from the last segment of the module path in `go.mod`
  - **Swift**: check `Package.swift` for executable target names, or check the Makefile `build` target
  - **Rust**: check `Cargo.toml` for `[[bin]]` entries or the `name` field under `[package]`
  - **Zig**: check `build.zig` for `b.addExecutable(.{ .name = "..." })` and use the `.name` value, or use the directory name
  - **Python**: check `pyproject.toml` for `[project.scripts]` entries
  - **Ruby**: check the gemspec for `executables` or look in `bin/` or `exe/`
  - **Shell**: use the script filename as the binary name
- **Binary path**: determine the full path used to run the binary:
  - **Compiled languages** (Go, Swift, Rust, Zig): typically `bin/NAME` or a build output directory (e.g., `$(CURDIR)/bin/NAME` for Go, `$(CURDIR)/zig-out/bin/NAME` for Zig)
  - **Interpreted languages** (Python, Ruby, Shell): the script path itself (e.g., `bin/NAME`, `./NAME`)
- **Environment variable name**: derive from the binary name, uppercased with hyphens replaced by underscores, suffixed with `_BIN` (e.g., `bopca` becomes `BOPCA_BIN`, `my-tool` becomes `MY_TOOL_BIN`)
```

## scaffold-go-cli (1033-scaffold-go-cli)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cboone/agent-harness-plugins/tree/d9e1b396852487c90500486a7b4fe94d88c64bd0/plugins/scaffold-go-cli
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1033-scaffold-go-cli/2316-scaffold-go-cli
- الوصف: Scaffold a Go CLI with Cobra, GoReleaser, CI, and Homebrew publishing. Use for "scaffold a Go CLI"; for a library, use scaffold-go-library.

```markdown
# Scaffold Go CLI

Generate the full boilerplate for a new Go CLI project.

## Workflow

### 1. Gather Project Information

If the user provided a project name in their request, use it as the project name and skip asking for it. Still ask for the remaining parameters (description, Viper, Charmbracelet TUI) unless already provided in the user's initial request.

Ask the user for these parameters:

- **Project name** -- kebab-case, used as the binary name, module path, and directory name (e.g., `my-tool`)
- **Short description** -- one sentence, used in README, GoReleaser Homebrew cask, and the Cobra root command `Short` field
- **Include Viper?** -- whether to add Viper for config file management (adds `--config` flag and `~/.config/<name>/config.yaml` support)
- **Include Charmbracelet TUI?** -- whether to add bubbletea, lipgloss, and bubbles dependencies

If the user already provided some or all of these in their initial request, do not re-ask. Derive what you can from context.

### 2. Detect User Identity

Detect the user's GitHub username and full name for use in templates:

```bash
# GitHub username (for module paths, URLs, Homebrew tap)
gh api user -q .login
```

```bash
# Full name (for LICENSE copyright)
git config user.name
```

If either command fails or produces no output, ask the user to provide the value. Use the GitHub username wherever templates reference `GITHUB-USERNAME` and the full name wherever they reference `COPYRIGHT-HOLDER`.

### 3. Verify the Target Directory

The project should be scaffolded in a directory named after the project. If the current directory is already named after the project and is empty (or nearly empty), use it. Otherwise, create a subdirectory.

If the directory already contains Go files, warn the user before proceeding.

### 4. Initialize Git

Skip if already inside a git repository.

```bash
git init
```

### 5. Generate main.go

Read `./references/main-go.md` for the `main.go` template and create the file from it.

- Replace `PROJECT-NAME` with the project name
- Replace `GITHUB-USERNAME` with the detected GitHub username

### 6. Generate cmd/root.go

Choose the template based on the Viper parameter:

- **Without Viper**: read `./references/root-go-without-viper.md`
- **With Viper**: read `./references/root-go-with-viper.md`

Replace in the chosen template:

- `PROJECT-NAME` with the project name
- `PROJECT-DESCRIPTION` with the short description

### 7. Initialize go.mod and Install Dependencies

Read `./references/go-mod.md` for the canonical setup commands. The base sequence:

```bash
go mod init github.com/GITHUB-USERNAME/PROJECT-NAME
go get github.com/spf13/cobra@latest
```

If Viper was selected:

```bash
go get github.com/spf13/viper@latest
```

If Charmbracelet TUI was selected:

```bash
```
