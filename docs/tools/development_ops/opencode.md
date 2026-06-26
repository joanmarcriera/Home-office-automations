# Oh My OpenAgent (OmO) / oh-my-opencode

## What it is
Oh My OpenAgent (previously oh-my-opencode) is an open-source agent harness designed to provide a "world-class" development experience across multiple LLM providers. It acts as an orchestration layer on top of OpenCode, offering a full AI developer team in your terminal. It is a free, self-hostable tool released under the SUL 1.0 license.

## What problem it solves
It solves the "harness problem" where models fail not because of intelligence, but because of poor edit tools and narrow context. It provides reliable multi-model orchestration, surgical editing via Hashline (content hashes), and a "Discipline Agent" system that ensures tasks are driven to 100% completion using frontier models like **Claude 4.8** and **GPT-5.5**.

## Where it fits in the stack
**Development & Ops / Agent Harness**. It is the open-source alternative to proprietary "walled garden" agents like [Claude Code](claude-code.md) or [Windsurf](windsurf.md).

## Typical use cases
- **Complex Feature Building**: Using the `ultrawork` command to trigger a multi-agent plan-and-execute loop.
- **Large-scale Refactoring**: Leveraging LSP and AST-Grep integration for deterministic code changes (e.g., workspace-level renames).
- **Autonomous Debugging**: Deploying specialized agents (Oracle, Librarian) to root cause and fix elusive bugs.
- **Browser Automation**: Using the built-in Playwright skill for UI testing or data scraping.
- **Context Injection**: Auto-generating hierarchical `AGENTS.md` files for lean, project-specific context.

## Key Agents (The Sisyphus Team)
OmO uses a "Discipline Agent" system where specialized agents collaborate in parallel:
- **Sisyphus**: The main orchestrator. Plans, delegates, and ensures tasks never stop halfway.
- **Hephaestus**: The "Deep Worker" (Implementer). Explores codebases and executes edits using Hashline.
- **Prometheus**: The Strategic Planner. Interviews the user to refine requirements before execution starts.
- **Oracle**: The Reasoner. Specialized in architecture decisions and deep debugging.
- **Librarian**: Focuses on documentation and context retrieval.
- **Explore**: Handles web search and research via Exa MCP.

## Strengths
- **Multi-Model Orchestration**: Routes tasks to the best model (e.g., Claude 4.8 for logic, Gemini 3.5 for creativity).
- **Hashline (Hash-Anchored Edits)**: Edits lines by referencing content hashes, eliminating stale-line errors.
- **Claude Code Compatibility**: Supports `CLAUDE.md` and `AGENTS.md` skills, hooks, and MCP 3.0.
- **LSP + AST-Grep**: IDE-quality refactoring and AST-aware code search/rewrites.
- **Transparent & Open**: No vendor lock-in; supports local models like [Llama 4 Maverick](../ai_knowledge/local_llms.md).

## Limitations
- **Setup Complexity**: While improved with `/init-deep`, advanced multi-model configuration requires API key management for several providers.
- **Resource Usage**: Running multiple specialized agents in parallel can consume more tokens than a single-agent approach.
- **CLI-Centric**: Lacks a native heavy-GUI for users who prefer visual IDE integrations over terminal-based workflows.

## When to use it
- When you want a "Ubuntu" like experience for AI coding—stable, open, and powerful.
- When surgical precision and high success rates for complex edits are more important than speed.
- For large-scale refactors where AST-aware tools are required.

## When not to use it
- For trivial, single-file changes where a simple chat interface suffices.
- If you prefer the simplicity of a single-provider, managed experience.
- In resource-constrained environments where running multiple agent loops is prohibitive.

## Getting started

### Installation
You can install OmO via npm:

```bash
npm install -g oh-my-opencode
```

### Initializing a Project
Run the deep initialization to set up hierarchical context for your agents:

```bash
/init-deep
```

### Basic Example
```bash
omo "Explain how the authentication flow works in this project"
```

## CLI examples
```bash
# Start the "Ultrawork" loop (Plan -> Execute -> Verify)
ultrawork "Implement the authentication flow using NextAuth"

# Trigger a planning session with Prometheus
/start-work

# Self-referential loop until 100% done
/ulw-loop "Fix all linting errors and update dependencies"

# Run project diagnostics
bunx oh-my-opencode doctor
```

## API examples
OmO can be integrated into custom scripts using its CLI-first interface or by importing its core modules in a Bun/Node environment.

```typescript
// Example using the internal task runner
import { Sisyphus } from "oh-my-openagent/core";

const task = await Sisyphus.plan("Refactor the payment gateway to use Stripe v2026");
await task.execute();
```

## Related tools / concepts
- [Aider](aider.md)
- [Claude Code](claude-code.md)
- [Windsurf](windsurf.md)
- [MCP](../automation_orchestration/mcp.md)
- [OpenHands](openhands.md)
- [Llama 4 Maverick](../ai_knowledge/local_llms.md)
- [Claude](../providers/anthropic.md)
- [Gemini](../ai_knowledge/gemini.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / references
- [Oh My OpenAgent (GitHub)](https://github.com/code-yeongyu/oh-my-openagent)
- [The Harness Problem (Can Bölük)](https://blog.can.ac/2026/02/12/the-harness-problem/)
- [Oh My OpenCode Documentation](https://opencode.ai/docs/)
- [OmO Agent Deep Dive](https://www.glukhov.org/ai-devtools/opencode/oh-my-opencode-agents/)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high
