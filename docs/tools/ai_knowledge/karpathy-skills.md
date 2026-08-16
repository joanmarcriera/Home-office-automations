# Andrej Karpathy Skills

## What it is
Andrej Karpathy Skills is a curated collection of software development principles, system prompt instructions, and agentic execution guidelines inspired by Andrej Karpathy's philosophy on AI engineering and software simplicity. Designed for frontier models (including Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, and Gemma 3), these skills steer agents away from over-complication, speculative code generation, and "hallucination of complexity," promoting surgical and minimalist implementations compatible with **FastMCP 3.1** server guards.

## What problem it solves
It solves the pervasive issue of modern, highly capable AI models over-engineering simple solutions. When tasked with a basic bug fix or a lightweight utility, frontier models frequently invent unnecessary abstractions, import bloated third-party dependencies, or rewrite entire files. Codifying "Karpathy instincts" enforces constraint-based, goal-driven, and minimalist software engineering habits directly into an agent's reasoning loop.

## Where it fits in the stack
**AI & Knowledge / Best Practices**. Operating at the reasoning and planning layer, these rules act as a "simplicity filter" and code reviewer standard before an agent executes file modifications, fully compatible with custom **FastMCP 3.1** server guards.

## Typical use cases
- **Agent System Initialization**: Standardizing thinking and execution boundaries inside files like `CLAUDE.md` or system prompts.
- **Agentic Workflows**: Restricting autonomous models (like Jules, OpenClaw, or Claude Code) to perform minimal, targeted file edits.
- **Surgical Code Reviews**: Acting as a programmatic or cognitive checklist for verifying that changes are clean and preserve the existing codebase structure.
- **FastMCP 3.1 Constraint Configuration**: Configuring FastMCP 3.1 server tools to enforce structural simplicity and restrict unauthorized framework installations.

## Strengths
- **Surgical Execution**: Prioritizes tiny, highly specific edits over broad, destructive file rewrites.
- **Simplicity First**: Eliminates "hallucinated library bloat" by enforcing native, standard-library-first solutions.
- **Extremely Low Overhead**: Implemented as lightweight Markdown guidelines, Pydantic v2 guard rails, or IDE configuration rules without heavy infrastructure.
- **Enhanced Agent Predictability**: Makes autonomous code generation and problem resolution significantly more deterministic and auditable.

## Limitations
- **Highly Opinionated**: Minimalist standards might clash with enterprise architectures that strictly mandate verbose boilerplate or complex micro-abstractions.
- **Requires Cognitive Alignment**: Demands that the underlying model possesses strong reasoning capability (e.g., Claude 5.1 or GPT-5.5) to understand and apply abstract constraints.
- **Manual Bootstrapping**: Requires developers to actively configure and bootstrap the guidelines into their target agent environments.

## When to use it
- When your AI coding assistant repeatedly over-complicates pull requests or introduces unrelated changes.
- At the outset of a new codebase to prevent technical debt and keep dependency lists clean.
- In automated test-driven development (TDD) environments to keep test cases and solutions highly focused.

## When not to use it
- In legacy, massive enterprise Java or C# systems where heavy structural boilerplate is a hard architecture requirement.
- During unstructured brainstorming or wild creative exploratory coding phases where constraints might hinder ideation.

## Getting started

### Installation (Claude Code Plugin)
To load Karpathy simplicity standards as a custom plugin inside Claude Code:
```bash
/plugin install andrej-karpathy-skills@latest
```

### Prompt Injection Configuration
Embed the following "Karpathy Instincts" block into your local developer instruction files or agent settings:
```markdown
## Karpathy Simplicity Instincts
1. **Surgical Edits**: Touch the minimum number of lines required to solve the task. Do not rewrite surrounding code.
2. **Standard Library First**: Solve problems using language-native APIs before importing third-party libraries.
3. **Verify Locally**: Run immediate compilation or unit test checks after every file edit.
```

## CLI examples

### Adhering to Constraints via CLI Plugin
```bash
# Verify the current directory adheres to Karpathy simplicity constraints
/plugin run karpathy-skills --audit --threshold=strict

# Automatically clean up speculative changes made during generation
/plugin run karpathy-skills --prune-unused-imports

# List all actively registered simplicity constraint rules
/constraints list
```

## API examples

### Programmatic Constraint Checker (Python + Strict Pydantic v2)
Using Pydantic v2 to validate that generated code matches Karpathy simplicity criteria before committing to disk.

```python
from pydantic import BaseModel, Field, field_validator
import re

class ComplexityGuard(BaseModel):
    code_snippet: str = Field(..., description="The generated code to review.")
    max_imports: int = Field(default=5, description="Maximum allowed imports.")
    max_lines_changed: int = Field(default=15, description="Maximum lines allowed to change.")

    @field_validator("code_snippet")
    @classmethod
    def check_speculative_bloat(cls, value: str) -> str:
        # Flag common anti-patterns like placeholder comments or massive frameworks
        if "TODO" in value or "placeholder" in value:
            raise ValueError("Surgical code must be complete; placeholders are prohibited.")
        import_count = len(re.findall(r"^(import\s+|from\s+)", value, re.MULTILINE))
        if import_count > 5:
            raise ValueError(f"Too many imports ({import_count}). Keep dependencies minimal.")
        return value

# Example validation
try:
    guard = ComplexityGuard(
        code_snippet="import sys\nimport os\n\ndef main():\n    print('Surgical run!')",
        max_lines_changed=5
    )
    print("Code passes simplicity audit!")
except ValueError as e:
    print(f"Audit failed: {e}")
```

### FastMCP 3.1 Constraint Prompt Schema (Agentic JSON)
Under FastMCP 3.1, constraint and prompt policies are served to autonomous agents dynamically:

```json
{
  "tool": "enforce_simplicity_policy",
  "arguments": {
    "policy_name": "surgical_changes_only",
    "target_files": ["src/main.py"],
    "allowed_dependencies": ["pydantic", "fastapi"]
  }
}
```

## Related tools / concepts
- [Matt Pocock Skills](matt-pocock-skills.md) — Complementary development practices focusing on strict test-driven workflows.
- [Claude Code](../development_ops/claude-code.md) — Primary local agent environment for CLI development.
- [Model Context Protocol (FastMCP 3.1)](../../tools/automation_orchestration/mcp.md) — Standardized tool connection protocol.
- [Jules (Agent)](jules.md) — Specialized autonomous agent optimized for surgical edits.
- [Cline](../agents/cline.md) — Multi-agent system that leverages custom simplicity rulebooks.

## Sources / references
- [Andrej Karpathy's Personal Blog & Recommendations](https://karpathy.ai/)
- [Andrej Karpathy Skills (GitHub Community Platform)](https://github.com/forrestchang/andrej-karpathy-skills)
- [The 'Simplicity First' Engineering Philosophy](https://karpathy.ai/blog/simplicity.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
