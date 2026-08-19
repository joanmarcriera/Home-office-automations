# Plandex

## What it is
Plandex is an open-source, AI-powered development engine designed for complex, multi-file software engineering tasks. It utilizes a "plan-first" methodology, decomposing high-level development directives into explicit, reviewable action plans before making modifications to codebase files. As of early 2027, it serves as a primary tool for "Large Context Engineering," supporting massive repositories via AST indexing, persistent sandboxed session trees, and frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Llama 4**.

## What problem it solves
Plandex addresses the reliability and predictability challenges of automated multi-file code modifications. Traditional chat-based assistants often suffer from context drift or hallucinate broken imports during complex refactoring operations. Plandex mitigates these failure modes through:
- **Explicit Plan Decomposition**: Generating step-by-step human-reviewable plans before modifying codebase disk state.
- **Context Drift Prevention**: Maintaining persistent session state and sandbox branches that track pending vs. committed changes.
- **Large Repository Indexing**: Efficiently processing monorepo contexts using hierarchical AST indexing and RAG retrieval pipelines.

## Where it fits in the stack
**Development & Ops**. Serves as a plan-and-execute AI coding engine for multi-file architectural changes, positioning itself between high-level multi-agent orchestration frameworks (like [OpenSwarm](openswarm.md)) and fast single-file terminal editors (like [Aider](aider.md)).

## Typical use cases
- **Multi-File Refactoring**: Architecting and executing cross-cutting refactors across API endpoints, data models, and test suites.
- **Framework & Schema Migrations**: Automating structural codebase migrations (e.g., upgrading to Pydantic v2 or FastMCP 3.1).
- **Feature Implementation**: Implementing complex features spanning backend microservices, database migrations, and frontend UI components.
- **Comprehensive Test Generation**: Generating end-to-end integration and unit test suites across entire legacy packages.

## Strengths
- **Plan-First Transparency**: Developers inspect, refine, or reject multi-step change blueprints before file modifications execute.
- **Isolated Sandbox Execution**: Modifications are applied in isolated sandbox branches without dirtying the working Git directory.
- **Persistent Context Management**: Handles large context windows cleanly across long-running engineering sessions.
- **Self-Hostable Infrastructure**: Fully open-source and deployable on self-hosted infrastructure with support for local models via [Ollama](../../services/ollama.md).
- **FastMCP 3.1 Integration**: Compatible with FastMCP 3.1 tool servers for automated database, logging, and deployment verification.

## Limitations
- **Workflow Latency**: The two-phase plan-then-execute model introduces additional review overhead compared to instant inline completions.
- **Session State Management**: Requires engineers to adopt a command-driven session lifecycle (`plandex new`, `load`, `tell`, `apply`, `save`).
- **Infrastructure Overhead**: Self-hosted team deployments require managing Plandex server instances and Postgres/Vector storage nodes.

## When to use it
- When implementing complex features or refactors that span dozens of files across multiple modules.
- When team policy requires reviewing explicit step-by-step change plans before code modification.
- When executing long-running engineering sessions that span multiple hours or sub-tasks without context decay.

## When not to use it
- For quick, single-file edits or simple bug fixes (use [Aider](aider.md) or [Cursor](cursor.md)).
- When real-time inline ghost-text code completions are desired (use [Codeium](codeium.md)).
- For basic single-prompt script generation where multi-file context tracking is unnecessary.

## Getting started

### Installation
Plandex CLI can be installed directly via shell installer script:

```bash
curl -sL https://plandex.ai/install.sh | bash
```

### Initializing a Project
Navigate to the root directory of your project repository and initialize Plandex:

```bash
plandex init
```

## CLI examples

### Session and Branch Management
Plandex provides session branching for managing concurrent engineering attempts:

```bash
# Create a new plan session for an OAuth feature implementation
plandex new feature-oauth2-integration

# Load relevant codebase paths into the session context
plandex load src/auth/ tests/auth/ docs/architecture/

# List active branches and session trees
plandex branch --list
```

### The Plan-Execute-Verify Loop
```bash
# Provide the architectural directive to Plandex
plandex tell "Implement OAuth2 authentication using FastMCP 3.1 protocol."

# Inspect the generated multi-step plan
plandex plan

# Execute the plan in the isolated sandbox environment
plandex apply
```

### Verification and Persistence
```bash
# Inspect sandbox changes relative to current workspace files
plandex diff

# Execute automated tests within the Plandex sandbox context
plandex run pytest

# Commit and save sandbox modifications to actual project files
plandex save
```

## API examples

### Programmatic Plandex Session Wrapper with Pydantic v2
This Python script programmatically invokes and manages Plandex CLI sessions while validating metadata using **Pydantic v2**.

```python
import subprocess
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class PlandexSessionConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    session_name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$", description="Unique session identifier")
    model: str = Field(default="anthropic/claude-5-1", description="Frontier model target for plan generation")
    loaded_paths: List[str] = Field(default_factory=list, description="Target directory or file paths in context")

    def run_cli(self, args: List[str]) -> str:
        cmd = ["plandex"] + args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout

    def initialize_session(self) -> str:
        return self.run_cli(["new", self.session_name, "--model", self.model])

    def load_context(self) -> str:
        if not self.loaded_paths:
            return "No paths specified for loading."
        return self.run_cli(["load"] + self.loaded_paths)

if __name__ == "__main__":
    session = PlandexSessionConfig(
        session_name="refactor-pydantic-v2",
        model="anthropic/claude-5-1",
        loaded_paths=["src/models/", "tests/test_models.py"]
    )
    print(f"Configured Plandex session '{session.session_name}' using target model {session.model}.")
```

## Related tools / concepts
- [Aider](aider.md) — For interactive, immediate terminal-based editing.
- [Mentat](./mentat.md) — Terminal-native multi-file editor with context-aware features.
- [Claude Code](./claude-code.md) — Anthropic's agentic coding CLI for high-speed development.
- [OpenSwarm](./openswarm.md) — For orchestrating higher-level development workflows and agent teams.
- [Sweep](./sweep_dev.md) — For automating GitHub issues directly into Pull Requests.
- [Cursor](cursor.md) — An AI-native IDE for a GUI-first approach to multi-file editing.
- [Codeium](codeium.md) — For IDE-native AI assistance and real-time completions.
- [Superconductor](./superconductor.md) — Parallel agent sessions for rapid development.

## Sources / references
- [Plandex Official Website](https://plandex.ai/)
- [Plandex GitHub Repository](https://github.com/plandex-ai/plandex)
- [Plandex Documentation](https://docs.plandex.ai/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
