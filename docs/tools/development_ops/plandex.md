# Plandex

## What it is
Plandex is an AI-powered engine designed for complex, multi-file software engineering tasks. It utilizes a "plan-first" methodology where it decomposes a request into a series of explicit steps before executing them across the codebase. This approach ensures higher reliability and provides developers with a clear audit trail of intended changes. By June 2026, it has become a standard for "Large Context Engineering," supporting massive repos via advanced indexing and frontier models like **Claude 4.8 Opus**.

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
- **Open Source**: Fully self-hostable with support for both local (via **Llama 4 Maverick**) and cloud models.
- **Context Capacity**: Advanced memory management allows for processing entire large-scale projects without losing coherence.

## Limitations
- **Execution Speed**: The two-stage (plan then execute) process can be slower for trivial edits compared to inline assistants.
- **Workflow Overhead**: Requires developers to adapt to a specific command-driven session model rather than just "chatting" in an editor.
- **Infrastructure Management**: Following the 2026 Cloud wind-down, teams must manage their own server infrastructure for collaborative Plandex environments.

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

### Non-Interactive Task Triggering
You can trigger Plandex tasks from scripts by piping instructions, useful for automated maintenance:

```bash
echo "Add JSDoc comments to all exported functions in lib/utils.js" | plandex tell --non-interactive
```

### Sandbox Execution API
Plandex provides an internal API for programmatically executing commands within its isolated sandbox context:

```bash
# Verify formatting inside the plan sandbox before saving
plandex run "npx prettier --check ."
```

## Related tools / concepts
- [Aider](aider.md) — For interactive, immediate terminal-based editing.
- [Mentat](./mentat.md) — Terminal-native multi-file editor with context-aware features.
- [Claude Code](./claude-code.md) — Anthropic's agentic coding CLI for high-speed development.
- [OpenSwarm](./openswarm.md) — For orchestrating higher-level development workflows and agent teams.
- [Sweep](./sweep_dev.md) — For automating GitHub issues directly into Pull Requests.
- [Cursor](cursor.md) — An AI-native IDE for a GUI-first approach to multi-file editing.
- [Codeium](codeium.md) — For IDE-native AI assistance and real-time completions.
- [Agent Protocols](../../knowledge_base/agent_protocols.md) — Understanding the underlying agent communication standards like MCP 3.0.

## Sources / references
- [Plandex Official Website](https://plandex.ai/)
- [Plandex GitHub Repository](https://github.com/plandex-ai/plandex)
- [Plandex Documentation](https://docs.plandex.ai/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
