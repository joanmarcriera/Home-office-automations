# Makefile MCP

## What it is
An MCP server that auto-discovers Makefile targets and exposes them as individual, documented tools for AI assistants like Claude 4.8 Opus, GPT-5.5, and Gemma 3. It leverages the [Model Context Protocol](../../tools/automation_orchestration/mcp.md) 3.0 to provide granular tool registration.

## What problem it solves
Traditional Makefile MCP implementations often expose a single generic `make` tool, which prevents LLMs from "seeing" available targets in their tool list. `makefile-mcp` parses the Makefile to register each documented target as its own tool with descriptions, improving discoverability and ease of use in [agentic workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Where it fits in the stack
**Tool / Automation**. It provides a discovery and execution layer for project-specific automation, bridging the gap between local build systems and frontier models. It is a key component for [development ops](../development_ops/index.md) when using AI agents.

## Typical use cases
- Exposing build, test, lint, and deploy workflows to coding agents like [Aider](../development_ops/aider.md).
- Managing multi-project workflows by dynamically switching working directories.
- Documenting available automation targets for AI assistants in complex monorepos.
- Integrating with [Claude Code](../development_ops/claude-code.md) for terminal-based automation.

## Strengths
- **Target Discovery**: Automatically parses `##` comments to provide tool descriptions.
- **Dynamic Configuration**: Allows changing the working directory at runtime via a dedicated tool.
- **Security**: No shell expansion used; supports strict inclusion/exclusion of targets.
- **Built with FastMCP**: High compatibility and performance for [MCP 3.0](../../tools/automation_orchestration/mcp.md) environments.

## Limitations
- Requires targets to be documented with `##` to be exposed as tools.
- Commands run in a specified working directory only.
- Limited to [GNU Make](gnu-make.md) compatible Makefiles.

## When to use it
- When you want your AI assistant to have direct, visible access to your project's `make` targets.
- When working on complex projects with many automation steps defined in a Makefile.
- When you need to switch contexts between different Makefiles in a single session.

## When not to use it
- If you do not use Makefiles for project automation.
- If you prefer a single generic entry point for all shell commands.
- For high-stakes production deployment targets without a "dry-run" check.

## Getting started

Makefile MCP registers documented targets as tools. Documentation is provided via `##` comments on the target line.

### 1. Installation
Install using `uv` (recommended) or `pip`:
```bash
uv pip install makefile-mcp
```

### 2. Documenting your Makefile
Add `##` comments to your targets to expose them:
```makefile
test: ## Run the test suite
	pytest tests/
```

### 3. Configuration (Claude Desktop)
Configure your MCP client to run the server:
```json
{
  "mcpServers": {
    "make": {
      "command": "uvx",
      "args": ["makefile-mcp", "--cwd", "/path/to/project"]
    }
  }
}
```

## CLI examples
```bash
# List discovered targets and exit
makefile-mcp --list

# Start server with specific include/exclude patterns
makefile-mcp --include "test,lint" --exclude "deploy"

# Set a custom tool prefix to avoid collisions
makefile-mcp --prefix "myproj_"
```

## API examples
AI agents can interact with the server's configuration tool using [MCP 3.0](../../tools/automation_orchestration/mcp.md) JSON-RPC:
```json
// Change the working directory at runtime
set_working_directory({
  "path": "/absolute/path/to/new/project"
})
```

## Related tools / concepts
- [GNU Make](gnu-make.md)
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md)
- [Aider](../development_ops/aider.md)
- [Plandex](../development_ops/plandex.md)
- [Zapier](zapier.md)
- [MCP Registry](mcp-registry.md)
- [Claude Code](../development_ops/claude-code.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / References
- [Makefile MCP GitHub](https://github.com/democratize-technology/makefile-mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP 3.0 Specification](https://modelcontextprotocol.io)

## Contribution Metadata

- Last reviewed: 2026-07-02
- Confidence: high
