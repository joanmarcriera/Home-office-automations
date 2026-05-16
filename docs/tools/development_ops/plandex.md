# Plandex

## What it is
Plandex is an AI-powered engine designed for complex, multi-file software engineering tasks. It utilizes a "plan-first" methodology where it decomposes a request into a series of explicit steps before executing them across the codebase. This approach ensures higher reliability and provides developers with a clear audit trail of intended changes.

## What problem it solves
Plandex manages the complexity of large, multi-file changes by breaking them into explicit plans, making it easier to reason about and review AI-generated modifications. It solves the "context drift" problem common in chat-based AI assistants by maintaining a persistent session state that tracks pending and applied changes.

## Where it fits in the stack
**Development & Ops**. Serves as a plan-and-execute AI coding engine for complex, multi-file tasks, sitting between high-level orchestration and direct file editing.

## Typical use cases
- Large-scale, multi-file refactoring with explicit plans.
- Complex feature implementation spanning many files and layers (e.g., API, DB, Frontend).
- Codebase-wide migrations (e.g., moving from one library to another).
- Generating comprehensive documentation or unit tests for large modules.

## Strengths
- **Plan-based approach**: Provides transparency and reviewability before a single line of code is changed.
- **Persistent Sessions**: Changes are stored in a "sandbox" or "plan" until the developer chooses to apply them.
- **Context Management**: Efficiently handles large file contexts and complex dependencies.
- **Open Source**: Fully self-hostable with support for local and cloud models.

## Limitations
- **Execution Speed**: The two-stage (plan then execute) process can be slower for trivial edits.
- **Workflow Overhead**: Requires developers to adapt to a specific command-driven session model.

## When to use it
- When a task spans many files and benefits from an explicit, reviewable plan.
- When you want visibility into the AI's intended changes before they are written to disk.
- For complex architectural shifts where understanding the "how" is as important as the "what".

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

### Creating a Plan
Start a new session and describe a complex change:

```bash
plandex new
plandex load src/ tests/
plandex tell "Refactor the authentication flow to use JWT instead of sessions. Update all middleware and tests."
```

### Reviewing and Executing
Review the generated plan and then execute it:

```bash
plandex plan      # Review the proposed steps
plandex apply     # Execute the plan in the sandbox
```

### Verifying and Committing
Check the diffs in the sandbox and commit them to your local files if satisfied:

```bash
plandex diff      # See changes made in the sandbox
plandex save      # Save sandbox changes to your actual files
```

## Related tools / concepts
- [Aider](aider.md) — For interactive, immediate terminal-based editing.
- [Mentat](./mentat.md) — Another terminal-native multi-file editor.
- [Claude Code](./claude-code.md) — Anthropic's agentic coding CLI.
- [OpenSwarm](./openswarm.md) — For orchestrating higher-level development workflows.
- [Sweep](./sweep_dev.md) — For automating GitHub issues into PRs.
- [Cursor](cursor.md) — An AI-native IDE for a GUI-first approach.
- [Codeium](codeium.md) — For IDE-native AI assistance.
- [Agent Protocols](../../knowledge_base/agent_protocols.md) — Understanding the underlying agent communication standards.

## Sources / references
- [Official Website](https://plandex.ai/)
- [GitHub Repository](https://github.com/plandex-ai/plandex)
- [Plandex Documentation](https://docs.plandex.ai/)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
