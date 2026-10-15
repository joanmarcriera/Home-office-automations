# Just

## What it is
Just (invoked as `just` and configured via a `justfile`) is a fast, handy command runner written in Rust. Inspired by GNU Make, Just is explicitly saved from the burden of being a build system. Rather than tracking file dependencies, object graphs, or compilation targets, Just focuses strictly on running project-specific command recipes. It features concise syntax, positional recipe parameters, default argument values, environment variable handling, polyglot inline scripts (Python, Node.js, bash, perl), cross-platform shell support, and clear shell completion integrations.

In early 2027, Just is a standard command execution wrapper across developer environments, local AI agent setups, and homelab operational workflows.

```
+-----------------------------------------------------------------------------------+
|                           DEVELOPER / AI AGENT COMMAND LINE                       |
|   `just lint`       `just test filter="api"`       `just deploy target="prod"`    |
+------------------------------------------+----------------------------------------+
                                           |
                                           v Command Parse & Variable Interpolation
+------------------------------------------+----------------------------------------+
|                               JUST ENGINE (Rust Core)                             |
|  - .env Auto-Loading                   - Positional Parameter Resolution          |
|  - Private Recipe Hiding               - Working Directory Normalization          |
+------------------------------------------+----------------------------------------+
                                           |
                                           +----------------------------------------+
                                           |                                        |
                                           v Hashbang Script / Shell Execution      v CLI Delegation
+------------------------------------------+---+  +---------------------------------+---+
|            INLINE POLYGLOT RUNTIMES          |  |         DOWNSTREAM CLI TOOLS        |
|  #!/usr/bin/env python3  (Python Scripts)    |  |  [Docker / Podman]   [pytest / uv] |
|  #!/usr/bin/env node     (Node JS Tools)     |  |  [kubectl / Helm]    [git / gh]    |
|  #!/usr/bin/env bash     (Bash Shell Loops)  |  |  [FastMCP Servers]   [n8n Workflows]|
+----------------------------------------------+  +-------------------------------------+
```

## What problem it solves
[GNU Make](gnu-make.md) is frequently abused as a simple task runner. However, Make's design requires file target resolution, `.PHONY` declarations to prevent conflicts with local directory names, and strict tab indentation. Moreover, passing positional CLI arguments or dynamic parameters to Makefile targets requires awkward `$(filter-out ...)` hacks or environment variable overrides. Other alternatives like heavy shell scripts lack self-documenting capabilities, listing mechanisms, or clean multi-line recipe formatting.

Just solves these friction points by providing a purpose-built syntax designed exclusively for command execution. `justfile` recipes support typed positional arguments (`recipe param1 param2="default"`), modular `import` statements, inline polyglot scripts (`#!/usr/bin/env python3`), and automated `--list` command generation with doc comments.

## Where it fits in the stack
**Automation & Orchestration / Task Execution Layer**. Operating at the root of project repositories, Just provides the primary command interface for human developers and autonomous AI agents ([Claude Code](../development_ops/claude-code.md), [Jules](../../tools/ai_knowledge/jules.md)). It delegates execution to CLI tools, container systems ([Docker](../infrastructure/docker.md)), or complex task runners ([Taskfile](taskfile.md)).

```
+-----------------------------------------------------------------------------------+
|                                 ORCHESTRATION LAYER                               |
|   [Human Developer]     [Claude Code / Agent]     [n8n Automation Engine]         |
+------------------------------------------+----------------------------------------+
                                           |
                                           v Uniform Recipe Interface (`just <recipe>`)
+------------------------------------------+----------------------------------------+
|                              JUST TASK EXECUTION ENGINE                           |
|                         (Configured via Repository `justfile`)                    |
+------------------------------------------+----------------------------------------+
                                           |
                                           v Delegated Tool Commands
+------------------------------------------+----------------------------------------+
|                                 INFRASTRUCTURE LAYER                              |
|   [Docker / K3s]       [Python / Pytest / uv]       [Paperless / Homelab Apps]   |
+-----------------------------------------------------------------------------------+
```

## Task Execution Engine Comparison Matrix

| Feature / Metric | Just (`justfile`) | Task (`Taskfile.yml`) | GNU Make (`Makefile`) | npm / pnpm scripts |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Command runner | Task runner with checksums | File-based C/C++ build system | Node.js lifecycle runner |
| **Config Format** | Clean custom DSL | YAML | Tab-indented Makefile DSL | JSON (`package.json`) |
| **Positional Arguments** | Native (`recipe arg="default"`) | Complex (`vars` override) | Difficult (`filter-out` hack) | Fixed (`npm run task -- --arg`) |
| **File Fingerprinting** | None (Executes always) | Native (`sources` / `generates`) | Native (`target: dependencies`) | None |
| **Polyglot Scripts** | Native (`#!/usr/bin/env ...`) | Shell string blocks only | Tab-delimited shell blocks | JSON string escaping |
| **Execution Overhead** | Very Low (< 3ms Rust binary) | Very Low (< 5ms Go binary) | Very Low (< 2ms C binary) | Medium (Node.js cold start) |

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

### FastMCP 3.1 Server for Just Recipe Execution
The following script exposes repository `just` recipes as FastMCP 3.1 tools that AI agents or external orchestrators can discover and execute deterministically.

```python
import subprocess
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError
from fastmcp import FastMCP

mcp = FastMCP(
    "JustTaskRunner",
    instructions="FastMCP 3.1 tool server providing agentic discovery and execution of Justfile recipes."
)

class RecipeExecutionRequest(BaseModel):
    recipe_name: str = Field(..., description="Name of the Just recipe to execute")
    args: List[str] = Field(default_factory=list, description="Positional arguments to pass to the recipe")
    working_dir: Optional[str] = Field(default=None, description="Directory containing the target justfile")

class RecipeExecutionResponse(BaseModel):
    status: str = Field(..., description="'success' or 'error'")
    exit_code: int = Field(..., description="Process exit code")
    stdout: str = Field(..., description="Command standard output")
    stderr: str = Field(..., description="Command standard error")

@mcp.tool()
def list_recipes(working_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Parses and returns the available Just recipes from the justfile as JSON AST.
    """
    cmd = ["just", "--dump", "--dump-format", "json"]
    try:
        res = subprocess.run(cmd, cwd=working_dir, capture_output=True, text=True, check=True)
        return {"status": "success", "ast": json.loads(res.stdout)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def execute_recipe(request: RecipeExecutionRequest) -> Dict[str, Any]:
    """
    Executes a specified Just recipe with optional positional parameters and returns output.
    """
    cmd = ["just", request.recipe_name] + request.args
    try:
        res = subprocess.run(cmd, cwd=request.working_dir, capture_output=True, text=True, timeout=120)
        response = RecipeExecutionResponse(
            status="success" if res.returncode == 0 else "error",
            exit_code=res.returncode,
            stdout=res.stdout,
            stderr=res.stderr
        )
        return response.model_dump()
    except ValidationError as ve:
        return {"status": "error", "error_type": "validation_error", "details": ve.errors()}
    except Exception as e:
        return {"status": "error", "error_type": "execution_error", "message": str(e)}

if __name__ == "__main__":
    mcp.run()
```

### Python Justfile Generator with Pydantic v2 Schema Validation
Programmatically generate and validate `justfile` configurations using strict **Pydantic v2** models and serialize to file.

```python
import os
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

    for k, v in schema.variables.items():
        lines.append(f'{k} := "{v}"')
    if schema.variables:
        lines.append("")

    for recipe_name, recipe in schema.recipes.items():
        if recipe.is_private:
            lines.append("[private]")
        lines.append(f"# {recipe.doc_comment}")

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

## Production Hardening & Operational Guardrails

When using Just across multi-developer projects, automated agents, or production homelab nodes:

1. **Explicit Hashbang Paths**: Always specify standard, portable environment binary paths for inline polyglot scripts (`#!/usr/bin/env python3` or `#!/usr/bin/env bash`) rather than hardcoded local system paths (`#!/bin/bash` or `#!/usr/local/bin/python`).
2. **Environment Export Safety**: Use `set export` cautiously. Prefer passing explicit variables to recipes or loading `.env` files locally (`set dotenv-load`) to prevent leaking sensitive API tokens into subshell child processes.
3. **Recipe Idempotency**: Design recipes to be safe for repeated execution (e.g., use `mkdir -p`, `docker compose up -d`, or check resource existence before modification).
4. **Agent Self-Documentation**: Always comment recipes with concise `#` headers. Autonomous agents (such as Claude Code or Jules) inspect `just --list` outputs to select actions without requiring manual prompt instructions.

## Common Troubleshooting Protocols

| Issue / Error | Primary Cause | Resolution / Verification Command |
| :--- | :--- | :--- |
| **`error: Recipe 'x' failed with exit code 127`** | Missing binary or CLI tool in user `PATH` | Verify binary availability with `which <command>` or wrap in `hash <cmd> 2>/dev/null` check. |
| **`.env` Variables Not Loading** | `dotenv-load` not explicitly enabled in `justfile` | Add `set dotenv-load` to top of `justfile` or invoke with `just --dotenv-filename .env`. |
| **Multi-line Command Context Lost** | Recipes execute each line in a separate subshell by default | Combine multi-line commands with `&& \` or write as a single inline polyglot block (`#!/usr/bin/env bash`). |
| **Windows Shell Syntax Mismatch** | `just` defaulting to Powershell / cmd on Windows | Set explicit shell in `justfile`: `set shell := ["bash", "-c"]` or `set shell := ["powershell", "-c"]`. |
| **Argument Splitting Error** | Unquoted spaces in positional string parameters | Wrap parameters in quotes during call: `just test filter="foo and bar"`. |

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
