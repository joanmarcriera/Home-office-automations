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

## Related tools / concepts
- [GNU Make](https://www.gnu.org/software/make/)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [FastMCP](https://github.com/jlowin/fastmcp)

## Sources / References
- [Makefile MCP GitHub](https://github.com/democratize-technology/makefile-mcp)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
