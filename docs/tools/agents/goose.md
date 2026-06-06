# Goose

## What it is
Goose is an open-source, extensible AI agent designed to go beyond simple code suggestions. It is built to install, execute, edit, and test code autonomously or with human supervision, using any LLM that supports tool-calling.

## What problem it solves
It bridges the gap between static code completion and full-loop agentic software engineering. Goose can manage its own environment, install dependencies, and run scripts to verify its work, reducing the manual "context switching" developers often face when integrating AI-generated code.

## Where it fits in the stack
**Automation & Orchestration / Agents**. It is an agentic layer that sits on top of LLMs (like Claude, GPT-4, or local models) and interacts with the filesystem and shell. It is a direct alternative to tools like [Aider](../development_ops/aider.md) or [OpenHands](../development_ops/openhands.md).

## Typical use cases
- **Automated Bug Fixing**: Providing an issue description and letting Goose find, fix, and verify the solution.
- **Environment Setup**: Asking Goose to "set up a new React project with Tailwind and testing" and letting it handle the shell commands.
- **Refactoring**: Executing large-scale code changes across multiple files with automated test verification.
- **Continuous Integration**: Running Goose in CI pipelines to automatically attempt fixes for failing tests.

## Strengths
- **Extensible Architecture**: Built with a "plug-and-play" mindset for new tools and LLM providers.
- **Open Source**: Hosted at the Agentic AI Foundation (AAIF), ensuring long-term community-driven development.
- **Provider Agnostic**: Works with Anthropic, OpenAI, and local inference engines like [Ollama](../../services/ollama.md).
- **Deep Integration**: Can be used via CLI or integrated into other applications through its agentic API.

## Limitations
- **New Project**: As of mid-2026, the project is still evolving rapidly (transitioning from Block to AAIF), so some documentation and features may be in flux.
- **Token Usage**: Like all agentic tools that run in a loop, it can consume a significant number of tokens if not monitored.
- **Security**: Granting an agent shell and filesystem access requires careful consideration of trust boundaries and sandboxing.

## When to use it
- When you need a full-loop agentic software engineer that can fix bugs and run tests autonomously.
- When you want an open-source alternative to proprietary coding agents.
- When you need an agent that can switch between different LLM providers (Anthropic, OpenAI, local) easily.
- For automating repetitive developer tasks like environment setup or project scaffolding.

## When not to use it
- When simple code completion (like standard Copilot) is sufficient and lower latency is required.
- In highly restricted environments where giving an AI agent shell/filesystem access is not permitted.
- If you are looking for a purely visual, no-code tool (Goose is CLI-centric).

## Getting started

### Installation
Goose can be installed via common package managers or run as a standalone binary.

```bash
# Example installation using a script (check official docs for latest)
curl -fsSL https://goose.run/install.sh | sh
```

### Basic Usage
```bash
# Start an interactive session
goose session

# Ask goose to perform a task
goose run "create a python script that fetches the weather for London and saves it to a csv"
```

## Technical Patterns

### Toolkit Configuration
Goose uses "Toolkits" to extend its capabilities. You can enable or disable specific sets of tools (e.g., filesystem, developer tools, web browsing).

### Model Selection
Goose allows switching models easily:

```bash
goose session --model claude-3-5-sonnet
```

## Related tools / concepts
- [Aider](../development_ops/aider.md)
- [OpenHands](../development_ops/openhands.md)
- [Claude Code](../development_ops/claude-code.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [ServiceNow MCP Server](../automation_orchestration/servicenow-mcp.md)

## Sources / references
- [Goose GitHub Repository](https://github.com/aaif-goose/goose)
- [Goose Official Website](https://block.github.io/goose/) (Note: Redirects may apply during transition to AAIF)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
