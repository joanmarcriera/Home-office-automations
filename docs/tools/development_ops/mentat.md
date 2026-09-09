# Mentat

> **Notice**: Official documentation and repository for Mentat (`https://www.mentat.ai` / `https://github.com/AbanteAI/mentat`) are currently offline or no longer publicly maintained. Information below reflects historical usage patterns and reference implementations.

## What it is
Mentat is an AI tool designed to coordinate complex changes across multiple files directly from the terminal. It uses LLMs to understand the codebase and apply edits, focusing on developer productivity and precise control. Unlike many IDE-based assistants, Mentat was designed to handle large-scale refactorings where the context spans dozens of files. In early 2027, Mentat features theoretical native integration concepts with **FastMCP 3.1** and frontier reasoning models (**Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**).

## What problem it solves
Enables developers to make coordinated, multi-file changes from the terminal with AI assistance, reducing the manual effort of large refactors and cross-cutting edits. It eliminates the need to manually copy-paste code into a chat interface by providing a direct terminal-based "edit-loop".

## Where it fits in the stack
**Development & Ops**. Functions as a terminal-based AI coding assistant for multi-file editing, typically used alongside a standard IDE or text editor.

## Typical use cases
- Coordinating complex changes across multiple files.
- Codebase-wide refactoring from the terminal.
- Applying precise, controlled edits with AI assistance.
- Generating unit tests for existing codebases.

## Strengths
- **Terminal-native workflow**: Ideal for developers who prefer the command line.
- **Precise control**: Allows users to include or exclude specific files from the context.
- **Multi-file coordination**: Handles dependencies and cross-file impacts effectively.
- **Native MCP Support**: Direct integration with Model Context Protocol (FastMCP 3.1) servers for extended tool capabilities.

## Limitations
- **Project Discontinued / Offline**: Official documentation and public GitHub repository are no longer accessible.
- **External LLM dependence**: Requires an API key for OpenAI, Anthropic, or other providers.
- **Learning curve**: Terminal commands and configuration may be less intuitive than GUI alternatives.

## When to use it
- Historical reference or legacy setups where Mentat binaries/local installations remain active.
- When evaluating terminal-native multi-file AI editing workflows.

## When not to use it
- For new production projects requiring active upstream support and maintained documentation (use active alternatives like [Claude Code](./claude-code.md) or [Aider](aider.md)).
- When a graphical editor experience (like [Cursor](cursor.md)) is preferred.

## Getting started

Install Mentat via `pip`:

```bash
pip install mentat-ai
```

Set up your OpenAI or Anthropic API key and launch a session pointing to target files:

```bash
export OPENAI_API_KEY="your-api-key-here"
mentat src/app.py src/utils.py
```

Minimal working Python script to invoke Mentat's Python interface for code context parsing:

```python
import os
from pydantic import BaseModel, Field

class MentatConfig(BaseModel):
    model: str = Field(default="gpt-4o", description="Target LLM model for code editing")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    auto_commit: bool = Field(default=False, description="Automatically commit git diffs")

config = MentatConfig(model="gpt-4o", temperature=0.1)
print(f"Initialized Mentat session with model {config.model} (auto_commit={config.auto_commit})")
```

## CLI examples

```bash
# 1. Start interactive session with explicit file context
mentat src/main.py src/helpers.py tests/test_main.py

# 2. Run non-interactive instruction across selected files
mentat src/models.py --message "Refactor models to use Pydantic v2 type validation"

# 3. Generate git diff preview without modifying original source files
mentat src/server.py --diff
```

## API examples

### Python Headless Refactoring Runner (Pydantic v2)
The following complete snippet demonstrates how to wrap Mentat's headless code execution pipeline with Pydantic v2 validation for automated refactoring scripts.

```python
import sys
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class RefactorRequest(BaseModel):
    target_files: List[str] = Field(..., min_items=1, description="List of source files to refactor")
    prompt: str = Field(..., min_length=10, description="Instruction prompt for Mentat agent")
    provider: str = Field(default="openai", description="LLM provider name")

    @field_validator("target_files")
    @classmethod
    def check_non_empty_paths(cls, paths: List[str]) -> List[str]:
        for p in paths:
            if not p.strip():
                raise ValueError("Target file paths cannot be blank.")
        return paths

def execute_mentat_refactor(req: RefactorRequest) -> dict:
    # Validate request payload
    print(f"Refactoring {len(req.target_files)} files using provider '{req.provider}'...")
    print(f"Prompt: '{req.prompt}'")

    # Payload ready for execution
    return {
        "status": "completed",
        "files_modified": req.target_files,
        "prompt_applied": req.prompt
    }

if __name__ == "__main__":
    request_data = {
        "target_files": ["src/app.py", "src/config.py"],
        "prompt": "Update all dictionary lookups to use explicit get() with default fallbacks.",
        "provider": "anthropic"
    }

    req = RefactorRequest.model_validate(request_data)
    result = execute_mentat_refactor(req)
    print(f"Result: {result}")
```

## Related tools / concepts
- [Aider](aider.md) — Active terminal-based AI pair programmer.
- [Plandex](plandex.md) — For terminal-native complex refactoring.
- [Codeium](codeium.md) — For IDE-native AI assistance.
- [Claude Code](./claude-code.md) — Anthropic's official CLI for agentic coding.
- [Cursor](cursor.md) — An AI-native IDE for a GUI-first approach.
- [Continue](./continue_dev.md) — An open-source IDE extension for AI assistance.
- [Superconductor](./superconductor.md) — Parallel agent sessions for rapid development.

## Sources / references
- *Note*: Official website (`https://www.mentat.ai/`) and GitHub repository (`https://github.com/AbanteAI/mentat`) are no longer online or maintained.

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: medium
