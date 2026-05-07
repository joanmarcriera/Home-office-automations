# Cline

## What it is
Cline (formerly Claude Dev) is an open-source, autonomous AI coding agent that runs directly inside VS Code and JetBrains IDEs. It has full access to the project files, terminal, and browser, allowing it to perform complex software development tasks.

## What problem it solves
It eliminates the "copy-paste" loop between an IDE and an AI chat interface. Instead of just suggesting code snippets, Cline can read the entire codebase, create or edit files, execute terminal commands (e.g., running tests, installing dependencies), and automate browser-based tasks.

## Where it fits in the stack
**Agent / IDE Extension / CLI / Developer Experience (DX)**.

## Typical use cases
- **Feature Implementation**: Implementing new features from a high-level description across multiple files.
- **Bug Fixing**: Running tests, identifying the cause of failures, and applying fixes autonomously.
- **Refactoring**: Performing large-scale refactors with human-in-the-loop approval.
- **Research & Browsing**: Using its built-in browser to research documentation or debug UI issues.

## Patterns
- **Plan vs Act Mode**: Cline can switch between "Plan" (proposing changes without execution) and "Act" (executing tools and modifying files) modes to manage safety and token cost.
- **MCP Integration**: Uses the [Model Context Protocol](../automation_orchestration/mcp.md) to extend its capabilities with external tools like Google Search, Slack, or database connectors.
- **.clinerules**: Supports a repository-level `.clinerules` file to provide persistent, project-specific instructions to the agent.

## Strengths
- **Fully Open Source**: Transparent and inspectable (Apache 2.0 license).
- **Human-in-the-Loop**: Asks for permission before executing commands or saving file changes.
- **Provider Agnostic**: Supports Anthropic, OpenAI, Google, AWS Bedrock, OpenRouter, and local models (via Ollama/LM Studio).
- **CLI and IDE Native**: Offers both a VS Code sidebar and a standalone terminal CLI for automated workflows.

## Limitations
- **Latency**: Complex tasks using large context windows can be slow.
- **Token Cost**: Extensive "Act Mode" sessions can consume significant tokens.
- **Context Management**: While good, extremely large repositories can still challenge its attention.

## When to use it
- When you want an autonomous agent that stays inside your existing VS Code environment.
- For tasks that require iterating over terminal outputs (e.g., fixing test failures).
- When you need to integrate agentic coding into CI/CD pipelines via the CLI.

## When not to use it
- For very small, single-file edits where a simple chat prompt is faster.
- In highly restricted environments where terminal access cannot be granted to an extension.

## CLI examples
```bash
# Install Cline CLI globally
npm install -g cline

# Authenticate with your preferred provider
cline auth

# Run a task in "Headless" mode (auto-approve all actions)
cline -y "Refactor the authentication logic to use JWT"
```

## Getting started
### Installation
1. **IDE**: Install the **Cline** extension from the VS Code Marketplace.
2. **CLI**: Run `npm install -g cline` in your terminal.
3. Configure your API provider (e.g., OpenRouter, Anthropic, or OpenAI) via `cline auth` or in the extension settings.

### Basic Usage
1. Open the Cline sidebar (robot icon) or run `cline` in your terminal.
2. Type a natural language task (e.g., "Add a login page using Tailwind CSS").
3. Review the plan proposed by Cline and grant permissions for file/terminal actions.

## API examples
Cline exposes an internal API for MCP servers to communicate. A minimal MCP tool definition that Cline can use looks like this:

```json
{
  "name": "get_weather",
  "description": "Get current weather for a city",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": { "type": "string" }
    }
  }
}
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: Free (Extension/CLI) + LLM API costs.
- **Self-hostable**: Yes (local models supported).

## Related tools / concepts
- [Roo Code](roo-code.md) (Popular fork/alternative)
- [Aider](../development_ops/aider.md) (Terminal-based agent)
- [Windsurf](../development_ops/windsurf.md) (Agentic IDE)
- [Continue.dev](../development_ops/continue_dev.md) (IDE Extension)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Cursor](../development_ops/cursor.md) (AI-native IDE)

## Sources / References
- [Official GitHub](https://github.com/cline/cline)
- [Cline Documentation](https://docs.cline.bot/)
- [Cline CLI Reference](https://docs.cline.bot/cline-cli/cli-reference)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
