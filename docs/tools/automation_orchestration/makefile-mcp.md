# Makefile MCP

## What it is
An MCP server that auto-discovers Makefile targets and exposes them as individual, documented tools for AI assistants.

## What problem it solves
Traditional Makefile MCP implementations often expose a single generic `make` tool, which prevents LLMs from "seeing" available targets in their tool list. `makefile-mcp` parses the Makefile to register each documented target as its own tool with descriptions.

## Where it fits in the stack
**Tool / Automation**. It provides a discovery and execution layer for project-specific automation.

## Typical use cases
- Exposing build, test, lint, and deploy workflows to coding agents.
- Managing multi-project workflows by dynamically switching working directories.
- Documenting available automation targets for AI assistants.

## Strengths
- **Target Discovery**: Automatically parses `##` comments to provide tool descriptions.
- **Dynamic Configuration**: Allows changing the working directory at runtime.
- **Security**: No shell expansion used for command execution; supports exclusion of dangerous targets.
- **Built with FastMCP**: High compatibility and performance.

## Limitations
- Requires targets to be documented with `##` to be exposed as tools.
- Commands run in a specified working directory only.

## When to use it
- When you want your AI assistant to have direct, visible access to your project's `make` targets.
- When working on complex projects with many automation steps defined in a Makefile.

## When not to use it
- If you do not use Makefiles for project automation.
- If you prefer a single generic entry point for all shell commands.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

Makefile MCP registers documented targets as tools. Documentation is provided via `##` comments on the target line.

### 1. Installation
```bash
pip install makefile-mcp
```

### 2. Documenting your Makefile
Add `##` comments to your targets to expose them:

```makefile
.PHONY: help build test

## Show this help message
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

## Build the application binary
build:
	go build -o app main.go

## Run all unit tests
test:
	go test ./...
```

### 3. Configuration (Claude Desktop)
Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "project-make": {
      "command": "python",
      "args": ["-m", "makefile_mcp"],
      "env": {
        "MAKEFILE_PATH": "/path/to/your/Makefile"
      }
    }
  }
}
```

## Related tools / concepts
- [GNU Make](gnu-make.md)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Aider](../development_ops/aider.md)
- [Plandex](../development_ops/plandex.md)
- [Zapier](zapier.md)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [MCP Registry](mcp-registry.md)

## Sources / References
- [Makefile MCP GitHub](https://github.com/democratize-technology/makefile-mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high
