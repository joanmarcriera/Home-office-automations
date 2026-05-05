# Goose

## What it is
Goose is an open-source AI agent framework developed by Block (formerly Square) that allows LLMs to interact with your local environment through a "toolkit" approach. It is designed to be a reliable, extensible assistant that can perform engineering tasks, manage infrastructure, and automate workflows.

## What problem it solves
Goose addresses the need for a standardized, extensible way for agents to interact with system tools. By providing a clear interface for "tools" (executables, APIs, scripts), Goose allows developers to build agents that are grounded in real-world actions rather than just generating text.

## Where it fits in the stack
**Category**: Automation & Orchestration / Agent Frameworks

## Typical use cases
- **DevOps Automation**: Automating deployments, checking logs, and managing Kubernetes clusters via CLI.
- **Engineering Assistance**: Helping with code refactoring, running tests, and managing Git branches.
- **Tool Orchestration**: Combining multiple disparate CLI tools into a single natural language workflow.

## Strengths
- **Extensible Architecture**: Easy to add new "skills" or tools to the agent's repertoire.
- **Local-First**: Designed to run and act locally, ensuring speed and data privacy.
- **Block Ecosystem**: Benefits from the engineering standards and patterns used at Block.
- **Modular**: Separates the agent's reasoning (LLM) from the tools it uses.

## Limitations
- **Newer Project**: Community and ecosystem are still growing compared to older frameworks.
- **Complexity**: Might require more setup than "zero-config" tools like Open Interpreter.

## Getting started

### Installation
Goose is typically installed as a CLI tool.

```bash
# Example (Check official repo for latest installation methods)
curl -fsSL https://github.com/block/goose/releases/latest/download/goose_install.sh | sh
```

### Basic Usage
```bash
goose session
```

## CLI examples
```bash
# Start a new interactive Goose session
goose session

# Run a specific task directly via the CLI
goose run "Scan the current directory for security vulnerabilities"

# List all available tools and skills in Goose
goose tools list
```

## API examples
Goose is primarily a CLI-driven tool, but its toolset can be extended via the Model Context Protocol (MCP) or by writing custom Python toolkits.

```python
# Custom tool definition for Goose (following MCP-like patterns)
def my_custom_tool(param: str) -> str:
    """
    A descriptive docstring that Goose uses to understand when to call this tool.
    """
    return f"Processed {param}"

# Tools are typically registered in a goose-config.yaml or via MCP
```

## Related tools / concepts
- [Open Interpreter](open-interpreter.md)
- [Claude Code](../development_ops/claude-code.md)
- [Model Context Protocol (MCP)](mcp.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Aider](../development_ops/aider.md)
- [Cline](../agents/cline.md)

## Sources / references
- [Goose GitHub Repository](https://github.com/block/goose)
- [Block Engineering Blog](https://developer.squareup.com/blog/)

## Contribution Metadata
- Last reviewed: 2026-05-22
- Confidence: high
