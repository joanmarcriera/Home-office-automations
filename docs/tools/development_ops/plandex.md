# Plandex

## What it is
Plandex is an AI-powered engine designed for complex, multi-file software engineering tasks. It utilizes a "plan-first" methodology where it decomposes a request into a series of explicit steps before executing them across the codebase. As of June 2026, it supports a massive **2.5M token context window** and is optimized for frontier models like **Claude 4.8 Opus** (`claude-4-8-opus-20260528`) and **GPT-5.5**.

## What problem it solves
Plandex manages the complexity of large, multi-file changes by breaking them into explicit plans, making it easier to reason about and review AI-generated modifications. It solves the "context drift" problem common in chat-based AI assistants by maintaining a persistent session state that tracks pending and applied changes across the entire repository.

## Where it fits in the stack
**Development & Ops**. Serves as a plan-and-execute AI coding engine for complex, multi-file tasks, sitting between high-level orchestration and direct file editing.

## Typical use cases
- Large-scale, multi-file refactoring with explicit plans.
- Complex feature implementation spanning many files and layers (e.g., API, DB, Frontend).
- Codebase-wide migrations (e.g., moving from one library to another).
- Generating comprehensive documentation or unit tests for large modules.
- **Autonomous Repository Audits**: Leveraging the 2.5M token window to analyze entire monolithic codebases for security or performance bottlenecks.

## Strengths
- **Plan-based approach**: Provides transparency and reviewability before a single line of code is changed.
- **Persistent Sessions**: Changes are stored in a "sandbox" or "plan" until the developer chooses to apply them.
- **Extreme Context**: Handles up to 2.5M tokens, allowing it to "see" almost any modern repository in its entirety.
- **Open Source**: Fully self-hostable with support for local and cloud models.

## Limitations
- **Execution Speed**: The two-stage (plan then execute) process can be slower for trivial edits.
- **Workflow Overhead**: Requires developers to adapt to a specific command-driven session model.
- **Cloud Transition**: Plandex Cloud is officially winding down in 2026 in favor of local and self-hosted deployments.

## When to use it
- When a task spans many files and benefits from an explicit, reviewable plan.
- When you want visibility into the AI's intended changes before they are written to disk.
- For complex architectural shifts where understanding the "how" is as important as the "what".
- When you need the maximum possible context window for repository-wide reasoning.

## When not to use it
- When making quick, single-file edits (use [Aider](aider.md) or [Cursor](cursor.md) instead).
- When real-time inline completions are the primary need (use [Codeium](codeium.md)).

## Getting started

### Installation
Plandex is typically installed as a binary CLI:

```bash
curl -sL https://plandex.ai/install.sh | bash
```

### Initializing a Project
Navigate to your project root and initialize Plandex:

```bash
plandex init
```

## CLI examples

### Session and Branch Management
Plandex uses a branching model similar to Git for managing different engineering attempts:

```bash
# Create a new plan/session
plandex new refactor-auth

# Load files into the current session context
plandex load src/auth/ tests/auth/

# List all sessions and branches
plandex branch --list
```

### The Plan-Execute-Verify Loop
The core workflow involves describing a task, reviewing the plan, and executing it in a sandbox:

```bash
# Tell Plandex what to do
plandex tell "Implement OAuth2 with GitHub as a provider."

# Review the proposed plan (multi-step decomposition)
plandex plan

# Execute the plan in the isolated sandbox
plandex apply
```

### Verification and Synchronization
Once changes are applied in the sandbox, you must verify and save them:

```bash
# View the changes made in the sandbox
plandex diff

# Run tests or quality checks inside the sandbox context
plandex run npm test

# If satisfied, save sandbox changes to your project files
plandex save
```

## API examples
Plandex provides a Go-based API for custom integrations and autonomous agent pipelines.

### Integration with Go
```go
import (
    "github.com/plandex-ai/plandex/pkg/client"
)

func main() {
    c := client.NewClient("your-api-key")
    session, _ := c.CreateSession("repo-audit")

    // Load context and generate a plan
    c.LoadPath(session.ID, "./src")
    plan, _ := c.Tell(session.ID, "Analyze for security vulnerabilities")

    fmt.Printf("Proposed Plan: %s\n", plan.Steps)
}
```

## Related tools / concepts
- [Aider](aider.md) — For interactive, immediate terminal-based editing.
- [Mentat](./mentat.md) — Another terminal-native multi-file editor.
- [Claude Code](./claude-code.md) — Anthropic's agentic coding CLI.
- [OpenSwarm](./openswarm.md) — For orchestrating higher-level development workflows.
- [Sweep](./sweep_dev.md) — For automating GitHub issues into PRs.
- [Cursor](cursor.md) — An AI-native IDE for a GUI-first approach.
- [Codeium](codeium.md) — For IDE-native AI assistance.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for connecting models to tools.
- [Claude](../providers/anthropic.md) — Primary frontier model provider for Plandex.

## Sources / references
- [Official Website](https://plandex.ai/)
- [GitHub Repository](https://github.com/plandex-ai/plandex)
- [Plandex Documentation](https://docs.plandex.ai/)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
