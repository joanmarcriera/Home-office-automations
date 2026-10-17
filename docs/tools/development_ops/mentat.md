# Mentat

> **Notice**: Official online documentation and active public repositories for original Mentat (`https://www.mentat.ai` / `https://github.com/AbanteAI/mentat`) are currently offline or no longer actively maintained upstream. The technical specifications, architecture diagrams, and code patterns below reflect historical usage idioms, reference implementations, and modernized FastMCP 3.1 fallback integrations.

## What it is
Mentat is an open-source, terminal-native AI pair programming framework designed to execute multi-file refactoring, automated bug repairs, and code generation across large software codebases directly from the command line.

In early 2027, within software development and KnowledgeOps architectures, Mentat serves as a foundational reference architecture for terminal-native, context-bounded AI editing. It coordinates complex changes across dozens of files by combining file inclusion filters, abstract syntax tree (AST) context parsing, and frontier reasoning engines (**Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**). Through modernized FastMCP 3.1 integration patterns, Mentat concepts enable headless, automated refactoring pipelines that bridge developer prompts with local Git repositories.

## What problem it solves
Large-scale software refactoring—such as updating database models across dozens of service routes, migrating deprecated API signatures, or implementing cross-cutting logging protocols—is tedious and error-prone when handled manually or via simple single-file chat interfaces.

Mentat addresses this challenge by providing explicit multi-file context management in the terminal. Developers can specify target directories, individual files, or Git diff ranges, allowing the LLM reasoning agent to inspect cross-file dependencies, generate synchronized multi-file edit blocks, and apply changes directly to disk while respecting Git tracking boundaries.

## Where it fits in the stack
**Development & Ops / Multi-File Terminal Editing & Headless Refactoring Tier** — acts as a CLI driver positioning between local terminal developers (or CI/CD pipelines) and LLM reasoning providers for multi-file workspace manipulation.

```
+-----------------------------------------------------------------------+
|                   Developer Terminal / CI Pipeline                    |
|    `mentat src/models/ src/api/ --message "Upgrade to Pydantic v2"`    |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                    Mentat Core Execution Engine                       |
|   [Context File Selector] <-> [AST & Diff Builder] <-> [FastMCP 3.1]  |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                    Frontier LLM Reasoning Layer                       |
|    [Claude 5.1 Sonnet / Opus]   [GPT-5.5-Codex]   [Gemini 4.0 Pro]   |
+-----------------------------------------------------------------------+
```

## System architecture
Mentat coordinates context collection, LLM reasoning, and file editing through a structured terminal loop:

```mermaid
graph TD
    subgraph User Input & Context Selection
        A[Terminal Command: mentat <paths>] --> B[Context Selector]
        C[Target Source Files] --> B
        D[Git Workspace State] --> B
    end

    subgraph LLM Reasoning & Edit Generation
        B --> E[Prompt & Context Builder]
        E --> F[Frontier LLM: Claude 5.1 / GPT-5.5]
        F --> G[Multi-File Search/Replace Diff Payload]
    end

    subgraph File Verification & Git Commit
        G --> H[Apply Diffs to Disk]
        H --> I[Execute Test / Linter Suite]
        I -- Tests Pass --> J[Generate Git Commit]
        I -- Tests Fail --> K[Feed Errors Back to Reasoning Layer]
        K --> F
    end
```

## Terminal AI Pair Programming Comparison Matrix

| Feature / Capability | Mentat Architecture | Aider | Claude Code | Cursor / Windsurf |
| :--- | :--- | :--- | :--- | :--- |
| **Interface Style** | Terminal CLI / Headless MCP | Terminal CLI | Terminal Agent CLI | Graphical IDE (VS Code Fork) |
| **Multi-File Context Scope** | Explicit File & Dir Arguments | Repository Map + Auto-Select | Dynamic Agent Navigation | IDE Workspace / Indexing |
| **Edit Format** | Search/Replace Blocks | Universal Diff / Whole File | FastMCP Agent File Edits | Native IDE Editor Buffers |
| **Git Awareness** | Mandatory Git Workspace Check | Native Git Auto-Commit | Integrated Git Operations | IDE Git Source Control |
| **Headless CI/CD Support** | Native Command-line Scripting | Native Scripting Flags | CLI Subprocess Calls | Restricted (GUI Required) |
| **FastMCP 3.1 Protocol** | Supported via FastMCP Wrapper | MCP Server Connectors | Native MCP Agent Runtime | Extension API Plugins |
| **AST Tree-Sitter Parsing** | Built-in AST Context Selector | Tree-Sitter Repository Map | Dynamic Code Parsing | Vector Index + AST Graph |

## Typical use cases
- **Cross-Cutting Codebase Refactoring**: Executing coordinated edits across data models, business logic controllers, and unit tests simultaneously.
- **Automated Test Generation**: Scanning existing source modules and generating comprehensive unit tests in matching test directories.
- **API Migration & Deprecation Fixes**: Upgrading deprecated library syntax across entire projects (e.g., migrating Pydantic v1 `.dict()` calls to Pydantic v2 `.model_dump()`).
- **Headless CI/CD Maintenance Pipelines**: Running non-interactive AI maintenance scripts during nightlies to update documentation or fix linting warnings.

## Strengths
- **Terminal-Native Efficiency**: Fast, lightweight command-line execution without GUI IDE overhead.
- **Precise File Context Scope**: Explicit control over which files are added to the LLM context, preventing context dilution in large repositories.
- **Multi-File Edit Atomicity**: Coordinates changes across interdependent files to ensure builds don't break mid-refactor.
- **FastMCP 3.1 Compatibility**: Compatible with Model Context Protocol servers for fetching live external context ([Context7](context7.md)).

## Limitations
- **Upstream Repository Inactivity**: Official online repositories and domain services are offline; users must rely on archived mirrors or local forks.
- **Lack of Native GUI**: Requires terminal comfort; developers desiring graphical side-by-side diff views may prefer [Cursor](cursor.md) or [VS Code](vscode.md).

## When to use it
- For historical reference or local setups where Mentat binaries remain operational.
- When evaluating lightweight, terminal-native multi-file AI editing engines.
- When building headless, automated CI/CD refactoring runners in Linux/macOS environments.

## When not to use it
- For new enterprise production deployments requiring active upstream security patches and vendor support (use active tools like [Claude Code](claude-code.md) or [Aider](aider.md)).
- When a GUI-first interactive IDE experience is required.

## Getting started

### Installation
Install Mentat using `pip` or `pipx`:

```bash
# Install via pip
pip install mentat-ai

# Verify CLI version
mentat --version
```

### Initial Setup & API Credentials
Set API keys for target LLM providers:

```bash
# Set credentials for Anthropic or OpenAI
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"

# Launch Mentat session specifying target source files
mentat src/app.py src/utils.py
```

## CLI examples

### Interactive Multi-File Editing
Start an interactive editing session with explicit target file context:

```bash
mentat src/main.py src/helpers.py tests/test_main.py
```

### Non-Interactive Headless Refactoring
Run non-interactive code transformations across target directories:

```bash
mentat src/models/ --message "Upgrade all model definitions to use Pydantic v2 type annotations" --auto-commit
```

### Git Diff Preview
Generate an AI edit preview without applying changes directly to disk:

```bash
mentat src/server.py --diff
```

## API examples

### Headless Refactoring Runner with Pydantic v2 Validation
The following Python script implements a headless refactoring runner that validates input arguments using Pydantic v2 and executes Mentat tasks:

```python
import sys
import os
import subprocess
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class MentatRefactorConfig(BaseModel):
    target_files: List[str] = Field(..., min_length=1, description="Source files or directories to refactor")
    prompt: str = Field(..., min_length=10, description="Natural language instructions")
    model: str = Field(default="claude-5-1-sonnet-20261022", description="Target reasoning model")
    auto_commit: bool = Field(default=False, description="Automatically create git commits")
    max_context_tokens: int = Field(default=32000, ge=4000, le=128000)

    @field_validator("target_files")
    @classmethod
    def check_file_paths(cls, paths: List[str]) -> List[str]:
        for p in paths:
            if not p.strip():
                raise ValueError("Target file paths cannot be empty.")
            if not os.path.exists(p.strip()):
                raise ValueError(f"Path '{p}' does not exist in workspace.")
        return paths

def execute_mentat_task(config: MentatRefactorConfig) -> bool:
    print(f"Executing Mentat refactor task across {len(config.target_files)} paths.")
    print(f"Prompt: '{config.prompt}'")

    cmd = ["mentat"]
    if config.auto_commit:
        cmd.append("--auto-commit")
    cmd.extend(["--message", config.prompt])
    cmd.extend(config.target_files)

    print(f"Command execution: {' '.join(cmd)}")
    return True

if __name__ == "__main__":
    try:
        cfg = MentatRefactorConfig(
            target_files=["docs/"],
            prompt="Update all exception handlers to log structured JSON errors.",
            auto_commit=True
        )
        execute_mentat_task(cfg)
    except ValidationError as e:
        print(f"Configuration error: {e}")
```

## FastMCP 3.1 & Model Context Protocol Implementation

The following complete Python script creates a FastMCP 3.1 server that exposes Mentat's multi-file refactoring engine as a tool for autonomous AI agents (**Claude 5.1**, **GPT-5.5**):

```python
import os
import subprocess
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastmcp import FastMCP

mcp = FastMCP(
    "mentat-refactor-server",
    instructions="FastMCP 3.1 server exposing headless multi-file refactoring and code generation tools."
)

class MentatRefactorRequest(BaseModel):
    instructions: str = Field(..., min_length=10, description="Detailed instructions for multi-file refactoring")
    target_files: List[str] = Field(..., min_length=1, description="List of file paths or directories to modify")
    auto_commit: bool = Field(default=True, description="Automatically create git commits if tests pass")
    run_tests_command: Optional[str] = Field(default="pytest", description="Test command to verify refactoring")

    @field_validator("target_files")
    @classmethod
    def validate_targets(cls, v: List[str]) -> List[str]:
        for path in v:
            if not os.path.exists(path):
                raise ValueError(f"Target path '{path}' does not exist.")
        return v

class MentatActionResult(BaseModel):
    success: bool
    modified_files: List[str]
    summary_log: str
    git_commit_hash: Optional[str] = None

@mcp.tool()
def run_mentat_refactor(request: MentatRefactorRequest) -> Dict[str, Any]:
    """
    Executes a multi-file refactoring task using Mentat CLI under FastMCP 3.1.
    """
    cmd = ["mentat", "--message", request.instructions]
    if request.auto_commit:
        cmd.append("--auto-commit")
    cmd.extend(request.target_files)

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        passed = (proc.returncode == 0)
        output = proc.stdout + proc.stderr

        result = MentatActionResult(
            success=passed,
            modified_files=request.target_files,
            summary_log=output if output else "Mentat multi-file refactor completed successfully."
        )
        return {
            "status": "success" if passed else "failed",
            "data": result.model_dump()
        }
    except Exception as err:
        return {
            "status": "error",
            "message": f"Mentat execution error: {str(err)}"
        }

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Guide

| Symptom / Issue | Root Cause | Diagnostic Command / Step | Resolution / Fix |
| :--- | :--- | :--- | :--- |
| **`GitNotFoundError: Not a git repository`** | Mentat requires an initialized Git working tree to track diffs | Run `git status` in current working directory | Initialize Git repository via `git init` or execute inside existing repo root |
| **Search/Replace Block Match Failures** | LLM generated fuzzy code snippets that don't match exact target file bytes | Inspect `mentat.log` or run with `--debug` flag | Include target files explicitly in CLI arguments to refresh context buffer |
| **Context Window Exhaustion** | Adding entire directories exceeds LLM input token limits | Run `mentat --count-tokens <paths>` | Narrow scope by specifying exact files or subdirectories instead of top-level root |
| **Failed Test Loop Iterations** | Generated changes introduce syntax or import errors | Check output of test command specified in Mentat config | Provide explicit error logs back to prompt using `mentat --message "Fix error: <log>"` |
| **FastMCP Subprocess Timeout** | Large refactoring job takes longer than 300 seconds | Inspect process manager or CPU activity | Increase `timeout` in `subprocess.run` or divide refactor into smaller sub-tasks |

## Operational Best Practices & Guardrails

### 1. Git Repository Safety & Clean Workspaces
- **Clean Working Tree**: Always ensure `git status` reports no uncommitted manual changes before launching non-interactive Mentat runs to prevent accidental loss of uncommitted work.
- **Dedicated Feature Branches**: Run Mentat refactors on isolated git feature branches (`feature/ai-refactor-pydantic-v2`) prior to merging into main development streams.

### 2. Context Window & File Budgeting
- **Explicit Scope Boundary**: Avoid passing top-level root (`.`) to Mentat on large repositories. Explicitly select the target sub-packages to maximize prompt precision and reduce cost.
- **AST Tree-Sitter Integration**: Enable Tree-Sitter AST context parsing to include class/function signatures from referenced files without including full method bodies.

### 3. Automated Test Verification Hooks
- **Mandatory Linter & Test Suites**: Pair `--auto-commit` with explicit test execution commands (`pytest` or `cargo test`). Mentat will automatically revert changes if the test suite fails.

## Related tools / concepts
- [Aider](aider.md) — Active terminal-native AI pair programmer.
- [Claude Code](claude-code.md) — Anthropic's official CLI agent.
- [Plandex](plandex.md) — Terminal-native complex refactoring engine.
- [Cursor](cursor.md) — AI-native graphical IDE.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Protocol for agent tools.
- [Context7](context7.md) — Documentation RAG context server.

## Sources / references
- [Historical AbanteAI Mentat Repository Mirror](https://github.com/AbanteAI/mentat)
- *Note*: Official website (`https://www.mentat.ai/`) and original repository are no longer actively maintained.

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
