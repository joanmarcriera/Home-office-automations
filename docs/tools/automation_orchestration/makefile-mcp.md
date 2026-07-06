# Makefile MCP

## What it is
An MCP server that auto-discovers Makefile targets and exposes them as individual, documented tools for AI assistants like [Gemma 3](../ai_knowledge/local_llms.md), Claude 4.8 Opus, and GPT-5.5.

## What problem it solves
Traditional Makefile MCP implementations often expose a single generic `make` tool, which prevents LLMs from "seeing" available targets in their tool list. `makefile-mcp` parses the Makefile to register each documented target as its own tool with descriptions, improving discoverability and ease of use in agentic workflows.

## Where it fits in the stack
**Tool / Automation**. It provides a discovery and execution layer for project-specific automation, bridging the gap between local build systems and frontier models using the [Model Context Protocol](mcp.md).

## Typical use cases
- Exposing build, test, lint, and deploy workflows to coding agents.
- Managing multi-project workflows by dynamically switching working directories.
- Documenting available automation targets for AI assistants in complex monorepos.

## Strengths
- **Target Discovery**: Automatically parses `##` comments to provide tool descriptions.
- **Dynamic Configuration**: Allows changing the working directory at runtime via a dedicated tool.
- **Security**: No shell expansion used; supports strict inclusion/exclusion of targets.
- **Built with FastMCP**: Full support for MCP 3.0 routing logic and task protocol.

## Limitations
- Requires targets to be documented with `##` to be exposed as tools.
- Commands run in a specified working directory only.
- Limited to GNU Make compatible Makefiles.

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

### 2. Configuration (Claude Desktop)
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

### Hello World Example
Preview which targets will be discovered as tools in your current directory:
```bash
makefile-mcp --list
```

## CLI examples
```bash
# Start server with specific include/exclude patterns
makefile-mcp --include "test,lint" --exclude "deploy"

# Set a custom tool prefix to avoid collisions
makefile-mcp --prefix "myproj_"

# Use a specific Makefile and working directory
makefile-mcp --makefile ./build/Makefile --cwd ./build
```

## API examples
AI agents use the `set_working_directory` tool to switch context between projects at runtime:

```json
// Change the working directory to a new project
set_working_directory({
  "path": "/absolute/path/to/new/project"
})
```

## Related tools / concepts
- [GNU Make](gnu-make.md)
- [Model Context Protocol](mcp.md)
- [Aider](../development_ops/aider.md)
- [Plandex](../development_ops/plandex.md)
- [Zapier](zapier.md)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [MCP Registry](mcp-registry.md)
- [Claude Code](../development_ops/claude-code.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Makefile MCP GitHub](https://github.com/democratize-technology/makefile-mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
