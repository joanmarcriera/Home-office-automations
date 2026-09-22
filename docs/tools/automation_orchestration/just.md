# Just

## What it is
Just (invoked as `just` and configured via a `justfile`) is a fast, handy command runner written in Rust. Inspired by GNU Make, Just is explicitly saved from the burden of being a build system. Rather than tracking file dependencies, object graphs, or compilation targets, Just focuses strictly on running project-specific command recipes. It features concise syntax, positional recipe parameters, default argument values, environment variable handling, polyglot inline scripts (Python, Node.js, bash, perl), cross-platform shell support, and clear shell completion integrations.

In early 2027, Just is a standard command execution wrapper across developer environments, local AI agent setups, and homelab operational workflows.

## What problem it solves
[GNU Make](gnu-make.md) is frequently abused as a simple task runner. However, Make's design requires file target resolution, `.PHONY` declarations to prevent conflicts with local directory names, and strict tab indentation. Moreover, passing positional CLI arguments or dynamic parameters to Makefile targets requires awkward `$(filter-out ...)` hacks or environment variable overrides. Other alternatives like heavy shell scripts lack self-documenting capabilities, listing mechanisms, or clean multi-line recipe formatting.

Just solves these friction points by providing a purpose-built syntax designed exclusively for command execution. `justfile` recipes support typed positional arguments (`recipe param1 param2="default"`), modular `import` statements, inline polyglot scripts (`#!/usr/bin/env python3`), and automated `--list` command generation with doc comments.

## Where it fits in the stack
**Automation & Orchestration / Task Execution Layer**. Operating at the root of project repositories, Just provides the primary command interface for human developers and autonomous AI agents ([Claude Code](../development_ops/claude-code.md), [Jules](../../tools/ai_knowledge/jules.md)). It delegates execution to CLI tools, container systems ([Docker](../infrastructure/docker.md)), or complex task runners ([Taskfile](taskfile.md)).

## Typical use cases
- **Developer Command Alias Suite**: Wrapping long, multi-flag development CLI commands under simple aliases (`just test`, `just lint`, `just serve`).
- **Parameterized Service Management**: Passing dynamic arguments to homelab management scripts (`just restart-service paperless`, `just backup db`).
- **Inline Polyglot Automation**: Writing inline Python, Rust, or Node.js scripts directly inside a `justfile` recipe using standard hashbangs.
- **Agent Task Execution**: Providing AI coding agents with a clean, documented list of available project tasks via `just --list`.

## Strengths
- **Purpose-Built Command Runner**: Zero build graph complexity or `.PHONY` overhead; focused entirely on command execution.
- **Clean Argument & Variable Handling**: First-class support for positional parameters, default values, variadic arguments, and `.env` loading.
- **Polyglot Recipe Hashbangs**: Allows embedding multi-line Python, Bash, or Node.js scripts directly within a recipe block using `#!/usr/bin/env ...`.
- **Fast Rust Execution**: Blazing fast CLI startup times with native binaries available for Linux, macOS, FreeBSD, and Windows.

## Limitations
- **No Dependency Fingerprinting**: Does not inspect source file modification times or checksums to skip up-to-date targets (use [Taskfile](taskfile.md) or [GNU Make](gnu-make.md) for incremental builds).
- **Not a Replacement for Complex DAG Workflows**: Lacks multi-node distributed workflow graphs or visual pipeline monitoring (use [Argo Workflows](../orchestration/argo-workflows.md) or [n8n](../../services/n8n.md)).
- **Syntax Uniqueness**: Uses custom `justfile` syntax that, while clean, requires learning Just-specific constructs for variable export and conditional evaluation.

## When to use it
- When you want a simple, zero-overhead command runner for project scripts and developer commands.
- When recipes require flexible positional command-line arguments and default fallback parameters.
- When writing multi-language inline scripts (Python + Bash) within a single task runner file.

## When not to use it
- When you need incremental file-based build tracking and dependency checksums (use [Taskfile](taskfile.md) or [GNU Make](gnu-make.md)).
- For complex, multi-server enterprise deployment pipelines requiring graphical DAG orchestration (use [n8n](../../services/n8n.md) or [Argo Workflows](../orchestration/argo-workflows.md)).
- When strictly mandated to use zero-install system tools natively present on legacy Linux servers without installing new binaries (use [GNU Make](gnu-make.md)).

## Getting started

### Installation
Install `just` via standard package managers or Rust's cargo:

```bash
# macOS (Homebrew)
brew install just

# Linux (apt / pacman / dnf / cargo)
cargo install just

# Windows (Scoop / Chocolatey)
scoop install just
```

### Initializing a justfile
Create a `justfile` in your repository root:

```just
# Default recipe listing available commands
default:
    @just --list

# Run repository linting checks
lint:
    python3 scripts/check_catalog_consistency.py
    python3 scripts/validate_new_sources.py

# Run unit tests with optional filter
test filter="":
    pytest -k "{{filter}}"

# Polyglot inline Python recipe
[private]
inspect-env:
    #!/usr/bin/env python3
    import sys, os
    print(f"Python Runtime: {sys.version}")
    print(f"Current Directory: {os.getcwd()}")
```

## CLI examples

### Listing & Executing Commands
```bash
# Display formatted list of available recipes and descriptions
just --list

# Run a parameterized recipe with custom argument
just test filter="test_catalog"

# Pass raw command line arguments through to an underlying command
just -- dry-run --verbose
```

### Working Directory & Format Controls
```bash
# Format the justfile to canonical syntax standards
just --fmt --check

# Dump evaluated justfile AST as JSON for programmatic inspection
just --dump --dump-format json
```

## API examples

### Python (Justfile Parser & Executor with Pydantic v2 Schema Validation)
The following script demonstrates programmatically generating and validating `justfile` configurations using strict **Pydantic v2** models and executing recipes via subprocess.

```python
import os
import subprocess
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator

class RecipeArgument(BaseModel):
    name: str = Field(..., description="Argument variable name")
    default_value: Optional[str] = Field(None, description="Default fallback value")

class JustRecipe(BaseModel):
    doc_comment: str = Field(..., min_length=5, description="Docstring comment for --list display")
    arguments: List[RecipeArgument] = Field(default_factory=list)
    commands: List[str] = Field(..., min_items=1, description="List of command lines")
    is_private: bool = Field(False, description="Whether to hide recipe from --list")

class JustfileSchema(BaseModel):
    variables: Dict[str, str] = Field(default_factory=dict, description="Top-level export variables")
    recipes: Dict[str, JustRecipe] = Field(..., description="Map of recipe names to definitions")

    @field_validator("recipes")
    @classmethod
    def check_default_recipe(cls, v: Dict[str, JustRecipe]) -> Dict[str, JustRecipe]:
        if "default" not in v:
            raise ValueError("Justfile schema must contain a 'default' recipe")
        return v

def generate_justfile(schema: JustfileSchema, file_path: str = "justfile") -> str:
    lines = []

    # 1. Variables
    for k, v in schema.variables.items():
        lines.append(f'{k} := "{v}"')
    if schema.variables:
        lines.append("")

    # 2. Recipes
    for recipe_name, recipe in schema.recipes.items():
        if recipe.is_private:
            lines.append("[private]")
        lines.append(f"# {recipe.doc_comment}")

        # Format arguments
        args_str = ""
        if recipe.arguments:
            formatted_args = []
            for arg in recipe.arguments:
                if arg.default_value is not None:
                    formatted_args.append(f'{arg.name}="{arg.default_value}"')
                else:
                    formatted_args.append(arg.name)
            args_str = " " + " ".join(formatted_args)

        lines.append(f"{recipe_name}{args_str}:")
        for cmd in recipe.commands:
            lines.append(f"    {cmd}")
        lines.append("")

    content = "\n".join(lines)
    with open(file_path, "w") as f:
        f.write(content)

    return content

if __name__ == "__main__":
    schema = JustfileSchema(
        variables={"PROJECT_NAME": "HomelabOps"},
        recipes={
            "default": JustRecipe(
                doc_comment="Default entrypoint listing recipes",
                commands=["@just --list"]
            ),
            "audit": JustRecipe(
                doc_comment="Run doc quality and contract checks",
                commands=["python3 scripts/check_catalog_consistency.py", "python3 scripts/validate_new_sources.py"]
            ),
            "deploy": JustRecipe(
                doc_comment="Deploy service to target environment",
                arguments=[RecipeArgument(name="target", default_value="staging")],
                commands=["echo 'Deploying {{PROJECT_NAME}} to {{target}} environment...'"]
            )
        }
    )

    print("Validated Justfile Pydantic Schema:")
    print(schema.model_dump_json(indent=2))

    justfile_text = generate_justfile(schema)
    print("\nGenerated justfile Content:\n")
    print(justfile_text)
```

## Related tools / concepts
- [GNU Make](gnu-make.md) — Classic tab-indented build runner.
- [Taskfile](taskfile.md) — YAML-based cross-platform task runner with checksum fingerprinting.
- [Docker](../infrastructure/docker.md) — Container runtime orchestrated via Just recipes.
- [Claude Code](../development_ops/claude-code.md) — AI developer agent relying on Just for workspace commands.
- [Jules](../../tools/ai_knowledge/jules.md) — Autonomous agent running Just recipes.
- [Optuna](../development_ops/optuna.md) — HPO framework executed via Just scripts.
- [n8n](../../services/n8n.md) — Workflow engine executing Just CLI commands.
- [Paperless-ngx](../../services/paperless-ngx.md) — Homelab application managed via Just scripts.

## Sources / references
- [Just GitHub Repository](https://github.com/casey/just)
- [Just Programmer's Manual](https://just.systems/man/en/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
