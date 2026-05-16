# Jupyter Kernel MCP Server

## What it is
An MCP server providing AI assistants with stateful, persistent Jupyter kernel execution and notebook management.

## What problem it solves
Unlike traditional code execution environments that start fresh for each query, this server maintains state (variables, imports, data) across an entire conversation, enabling incremental development and data analysis.

## Where it fits in the stack
**Tool / Eval**. It provides a persistent compute workspace for agents, often used for [Knowledge Base](../../knowledge_base/README.md) expansion through data analysis.

## Typical use cases
- Incremental data analysis and visualization.
- Multi-step software development and testing.
- Educational tutorials where each step builds on the previous one.
- Long-running experiments spanning multiple chat sessions.

## Strengths
- **Persistent State**: Variables and imported libraries remain available.
- **Multi-language Support**: Supports Python, R, Julia, Go, Rust, TypeScript, and more.
- **Notebook Management**: Can create, edit, and search Jupyter notebooks.
- **Context-Aware**: Features a `suggest_next()` tool that provides intelligent suggestions based on current kernel state.

## Limitations
- Requires a running Jupyter server instance.
- Performance depends on the host machine's resources for executing kernel code.

## When to use it
- For complex data science tasks where loading datasets is expensive or state must be preserved.
- When you want an agent to build and maintain a documented Jupyter notebook of its work.

## When not to use it
- For simple, stateless calculations where a basic Python interpreter would suffice.
- If you cannot run or access a Jupyter server.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Technical examples

### 1. Smart Execution (compute)
Execute code with automatic detection of whether streaming is needed based on complexity.

```json
{
  "tool": "compute",
  "arguments": {
    "code": "import pandas as pd\ndf = pd.read_csv('large_dataset.csv')\ndf.describe()"
  }
}
```

### 2. Context-Aware Suggestions (suggest_next)
Ask the server for the next logical steps based on the current variables in memory.

```json
{
  "tool": "suggest_next",
  "arguments": {}
}
// Response might include: "You have 'df' loaded. Try df.head() or checking for nulls."
```

### 3. Notebook Management (notebook)
Interact with Jupyter notebooks using natural language instructions.

```json
{
  "tool": "notebook",
  "arguments": {
    "action": "create",
    "name": "Exploratory_Analysis.ipynb",
    "content": "# Data Analysis\nThis notebook tracks our progress..."
  }
}
```

### 4. Viewing Workspace (workspace)
Get a bird's eye view of all active kernels and notebooks.

```json
{
  "tool": "workspace",
  "arguments": {}
}
```

## Related tools / concepts
- [Jupyter](https://jupyter.org/)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Python](../ai_knowledge/python.md)
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Symbolic MCP](symbolic-mcp.md)

## Sources / References
- [Jupyter Kernel MCP GitHub](https://github.com/democratize-technology/jupyter-kernel-mcp)
- [Jupyter Documentation](https://docs.jupyter.org/)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high
