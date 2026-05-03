# Oh My OpenAgent (OmO) / oh-my-opencode

## What it is
Oh My OpenAgent (previously oh-my-opencode) is an open-source agent harness designed to provide a "world-class" development experience across multiple LLM providers. It acts as an orchestration layer on top of OpenCode, offering a full AI developer team in your terminal.

## What problem it solves
It solves the "harness problem" where models fail not because of intelligence, but because of poor edit tools and narrow context. It provides reliable multi-model orchestration, surgical editing via content hashes, and a "Discipline Agent" system that ensures tasks are driven to 100% completion.

## Where it fits in the stack
**Development & Ops / Agent Harness**. It is the open-source alternative to proprietary "walled garden" agents like Claude Code or AmpCode.

## Typical use cases
- **Complex Feature Building**: Using the `ultrawork` command to trigger a multi-agent plan-and-execute loop.
- **Large-scale Refactoring**: Leveraging LSP and AST-Grep integration for deterministic code changes.
- **Autonomous Debugging**: Deploying specialized agents (Oracle, Librarian) to root cause and fix elusive bugs.
- **Browser Automation**: Using the built-in Playwright skill for UI testing or data scraping.

## Key Agents
OmO uses a "Discipline Agent" system where specialized agents collaborate:
- **Sisyphus**: The main orchestrator. Plans, delegates, and ensures tasks never stop halfway.
- **Hephaestus**: The "Deep Worker." Explores codebases and executes goals without hand-holding.
- **Prometheus**: The Strategic Planner. Interviews the user to refine requirements before execution starts.
- **Oracle**: Specialized in architecture decisions and deep debugging.

## Strengths
- **Multi-Model Orchestration**: Routes tasks to the best model for the job (Claude for logic, Gemini for creativity, etc.).
- **Hashline (Hash-Anchored Edits)**: Edits lines by referencing content hashes, eliminating stale-line errors and whitespace issues.
- **Claude Code Compatibility**: Support for Claude Code skills, hooks, and MCPs.
- **Transparent & Open**: No "walled garden" lock-in; you control the providers and the tokens.

## Limitations
- **Setup Complexity**: While improved with `init-deep`, advanced multi-model configuration requires API key management for several providers.
- **Resource Usage**: Running multiple specialized agents in parallel can consume more tokens than a single-agent approach.

## When to use it
- When you want a "Ubuntu" like experience for AI coding—stable, open, and powerful.
- When surgical precision and high success rates for complex edits are more important than speed.

## When not to use it
- For trivial, single-file changes where a simple chat interface suffices.
- If you prefer the simplicity of a single-provider, managed experience.

## Licensing and cost
- **Open Source**: Yes (SUL 1.0)
- **Cost**: Free software; pay-per-token for whichever providers you use.
- **Self-hostable**: Yes.

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

## Related tools / concepts
- [Aider](aider.md)
- [Claude Code](claude-code.md)
- [OpenCode (MCP)](../automation_orchestration/mcp.md)
- [OpenHands](openhands.md)
- [OpenSwarm](openswarm.md)

## Sources / References
- [Oh My OpenAgent (GitHub)](https://github.com/code-yeongyu/oh-my-openagent)
- [The Harness Problem (Can Bölük)](https://blog.can.ac/2026/02/12/the-harness-problem/)
- [Oh My OpenCode Documentation](https://opencode.ai/docs/)

## Contribution Metadata
- Last reviewed: 2026-05-12
- Confidence: high
