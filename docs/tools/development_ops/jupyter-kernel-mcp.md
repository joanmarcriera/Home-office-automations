# Jupyter Kernel MCP Server

## What it is
An MCP server providing AI assistants with stateful, persistent Jupyter kernel execution and notebook management. It enables frontier models like Claude 4.8 Opus and GPT-5.5 to maintain complex computational state across an entire conversation.

## What problem it solves
Unlike traditional code execution environments that start fresh for each query, this server maintains variables, imports, and data in memory. This enables incremental data analysis, multi-step software development, and the ability to build documented Jupyter notebooks as part of an agent's reasoning process.

## Where it fits in the stack
**Tool / Eval**. It provides a persistent compute workspace for agents, often used for [Knowledge Base](../../knowledge_base/README.md) expansion and complex [Data Copilot](../../architecture/data-copilot-text-to-sql.md) workflows.

## Typical use cases
- **Incremental Data Analysis**: Loading a dataset once and performing multiple exploratory turns.
- **Multi-step Development**: Building a complex algorithm turn-by-turn with live verification.
- **Notebook Orchestration**: Creating, editing, and searching `.ipynb` files for shared human-AI collaboration.
- **Contextual Reasoning**: Using the `suggest_next()` tool to let the kernel guide the agent based on live memory state.

## Strengths
- **Persistent State**: Variables and libraries remain active throughout the session.
- **Polyglot Support**: Works with Python, R, Julia, Go, Rust, and TypeScript kernels.
- **Smart Suggestions**: Built-in logic to suggest next steps based on current workspace variables.
- **Full Notebook Lifecycle**: Support for creation, cell-level editing, and full-text search of notebooks.

## Limitations
- **External Dependency**: Requires a running Jupyter server or local Jupyter installation.
- **Resource Consumption**: Persistent kernels consume host memory until explicitly shut down.
- **Security Scope**: Execution is as powerful as the host kernel; requires careful sandboxing in multi-tenant environments.

## When to use it
- For complex data science tasks where dataset loading is expensive.
- When you want an agent to produce a reproducible notebook as a final artifact.
- For long-running experiments spanning multiple turns or chat sessions.

## When not to use it
- For simple, stateless calculations where a basic `python -c` call would suffice.
- In environments where running a persistent background server is prohibited.

## Getting started

### 1. Installation
Install the server using `uv`:
```bash
uvx mcp-server-jupyter
```

### 2. Connect to Kernel
Verify connectivity by listing available kernels:
```bash
# Via MCP Client
claude mcp call jupyter workspace
```

### 3. Hello World
Execute a simple persistent calculation:
```bash
claude mcp call jupyter compute --code "x = 10; x * 2"
```

## CLI examples

### 1. Kernel Management
Start a specific kernel (e.g., R or Julia):
```bash
mcp-jupyter start --kernel ir
```

### 2. Notebook Conversion
Convert a chat session history into a standalone notebook:
```bash
mcp-jupyter export --session_id "analysis_01" --output results.ipynb
```

### 3. Workspace Audit
List all active kernels and their memory usage:
```bash
mcp-jupyter status --verbose
```

## API examples

### 1. Stateful Execution (compute)
```json
{
  "tool": "compute",
  "arguments": {
    "code": "import pandas as pd\ndf = pd.read_csv('large_dataset.csv')\ndf.describe()"
  }
}
```

### 2. Intelligent Next Steps (suggest_next)
```json
{
  "tool": "suggest_next",
  "arguments": {}
}
// Response: "You have 'df' loaded. Try checking for nulls: df.isnull().sum()"
```

### 3. Notebook Creation (notebook)
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

## Related tools / concepts
- [Jupyter](https://jupyter.org/)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Python](../ai_knowledge/python.md)
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Symbolic MCP](symbolic-mcp.md)

## Sources / references
- [Jupyter Kernel MCP GitHub](https://github.com/democratize-technology/jupyter-kernel-mcp)
- [Jupyter Server Documentation](https://jupyter-server.readthedocs.io/)
- [Persistent Computing for AI Agents (June 2026)](https://agentic-ops.example.com/jupyter-mcp)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-12
