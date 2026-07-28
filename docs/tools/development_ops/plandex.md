# Plandex

## What it is
Plandex is an AI-powered engine designed for complex, multi-file software engineering tasks. It utilizes a "plan-first" methodology where it decomposes a request into a series of explicit steps before executing them across the codebase. This approach ensures higher reliability and provides developers with a clear audit trail of intended changes. By late October and November 2026, it has become a standard for "Large Context Engineering," supporting massive repos via advanced indexing and frontier models like **Claude 5.1** and **GPT-5.5**.

## What problem it solves
Plandex manages the complexity of large, multi-file changes by breaking them into explicit plans, making it easier to reason about and review AI-generated modifications. It solves the "context drift" problem common in simple chat-based AI assistants by maintaining a persistent session state that tracks pending and applied changes in a structured way. This ensures that the AI doesn't "forget" the broader goal during a long refactoring session.

## Where it fits in the stack
**Development & Ops**. Serves as a plan-and-execute AI coding engine for complex, multi-file tasks, sitting between high-level orchestration (like [OpenSwarm](openswarm.md)) and direct file editing (like [Aider](aider.md)).

## Typical use cases
- Large-scale, multi-file refactoring with explicit, human-reviewable plans.
- Complex feature implementation spanning many files and layers (e.g., API, DB, Frontend).
- Codebase-wide migrations (e.g., moving from one framework to another).
- Generating comprehensive documentation or unit tests for large, legacy modules.
- Automating the resolution of complex bugs that require changes across multiple service boundaries.

## Strengths
- **Plan-based approach**: Provides transparency and reviewability before a single line of code is changed on disk.
- **Persistent Sessions**: Changes are stored in a "sandbox" or "plan" branch until the developer chooses to apply them.
- **Context Management**: Efficiently handles large file contexts and complex dependencies using RAG-based indexing.
- **Open Source**: Fully self-hostable with support for both local (via local open models like **Llama 4**) and cloud models.
- **Context Capacity**: Advanced memory management allows for processing entire large-scale projects without losing coherence.

## Limitations
- **Execution Speed**: The two-stage (plan then execute) process can be slower for trivial edits compared to inline assistants.
- **Workflow Overhead**: Requires developers to adapt to a specific command-driven session model rather than just "chatting" in an editor.
- **Infrastructure Management**: Following the Cloud wind-down, teams must manage their own server infrastructure for collaborative Plandex environments.

## When to use it
- When a task is too complex for a single-file edit and benefits from an explicit, reviewable multi-step plan.
- When you want visibility into the AI's intended changes across dozens of files before they are written.
- For complex architectural shifts where understanding the "how" (the plan) is as important as the final code.

## When not to use it
- When making quick, single-file edits (use [Aider](aider.md) or [Cursor](cursor.md) instead).
- When real-time inline completions or "ghost text" are the primary need (use [Codeium](codeium.md)).
- For simple script generation where a basic chat interface suffices.

## Getting started

### Installation
Plandex is typically installed as a binary CLI:

```bash
curl -sL https://plandex.ai/install.sh | bash
```

### Initializing a Project
Navigate to your project root and initialize Plandex to create the local configuration:

```bash
plandex init
```

## CLI examples

### Session and Branch Management
Plandex uses a branching model similar to Git for managing different engineering attempts:

```bash
# Create a new plan/session for a specific feature
plandex new feature-oauth-integration

# Load files into the current session context
plandex load src/auth/ tests/auth/ README.md

# List all active sessions and branches
plandex branch --list
```

### The Plan-Execute-Verify Loop
The core workflow involves describing a task, reviewing the plan, and executing it in a sandbox:

```bash
# Tell Plandex what to do (the task)
plandex tell "Implement OAuth2 with GitHub as a provider."

# Review the proposed plan (multi-step decomposition)
plandex plan

# Execute the plan in the isolated sandbox environment
plandex apply
```

### Verification and Synchronization
Once changes are applied in the sandbox, you must verify and save them to your workspace:

```bash
# View the changes made in the sandbox compared to current files
plandex diff

# Run tests or quality checks inside the sandbox context
plandex run npm test

# If satisfied, save sandbox changes to your actual project files
plandex save
```

## API examples

### Programmatic Plandex Session Wrapper with Pydantic v2
You can trigger and track Plandex sessions programmatically using Python and validate session metadata with Pydantic v2.

```python
import subprocess
import json
from pydantic import BaseModel, Field

class PlandexSession(BaseModel):
    session_name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    model: str = Field(default="claude-5-1-sonnet-20261022")
    loaded_paths: list[str] = Field(default_factory=list)

    def run_command(self, args: list[str]) -> str:
        cmd = ["plandex"] + args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout

    def create_session(self) -> str:
        # Create session via Plandex CLI
        return self.run_command(["new", self.session_name, "--model", self.model])

    def load_files(self) -> str:
        if not self.loaded_paths:
            return "No paths to load."
        return self.run_command(["load"] + self.loaded_paths)
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
- Last reviewed: 2026-11-01
- Confidence: high
