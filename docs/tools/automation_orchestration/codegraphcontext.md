# CodeGraphContext

## What it is
CodeGraphContext is a specialized [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) server designed to convert codebases into graph databases. It allows AI agents to understand the relationships, dependencies, and structure of a project through a knowledge graph interface.

## What problem it solves
It addresses the challenge of "context window overload" and "hallucination" when AI agents reason over large codebases. By providing a graph-based representation, it enables 120x token reduction in some cases, allowing agents to fetch only the relevant nodes and edges rather than the entire file content.

## Where it fits in the stack
**Automation & Orchestration / MCP Server**. It acts as a bridge between an agent (like Claude or a local LLM) and the raw source code, providing a structured, semantic view of the project.

## Typical use cases
- **Semantic Code Search**: Finding functions or classes based on their relationships rather than just keyword matches.
- **Dependency Analysis**: Asking an agent to explain the impact of changing a specific module.
- **Architectural Mapping**: Generating a high-level overview of how different components of a system interact.

## Strengths
- **Massive Token Efficiency**: Dramatic reduction in context usage (up to 120x) compared to raw text ingestion.
- **Semantic Precision**: Indexes files, functions, classes, calls, imports, and inheritance at the symbol level.
- **Language Support**: Supports 14+ coding languages as of May 2026.
- **MCP Native**: Integrates seamlessly with any MCP-compliant client (e.g., Claude Desktop, Cursor, [Claude Code](../development_ops/claude-code.md)).
- **Interactive Visualization**: Generates web-based explorers for architectural mapping.

## Limitations
- **Indexing Overhead**: Initial conversion of very large codebases can be resource-intensive.
- **Tool-Calling Dependency**: Highly dependent on the agent's ability to reason over graph structures.

## When to use it
- When working with codebases that are too large to fit comfortably in a model's context window.
- When you need an agent to perform complex architectural analysis or cross-file refactoring.

## When not to use it
- For small, single-file projects where standard context ingestion is sufficient.
- If you don't have an MCP-compatible client or framework set up.

## Getting started

### Installation (via pip)
CodeGraphContext is available as a Python package:
```bash
pip install codegraphcontext
```

### Configuration (Claude Desktop)
Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "codegraph": {
      "command": "python",
      "args": ["-m", "codegraphcontext", "serve", "--path", "/path/to/your/repo"]
    }
  }
}
```

### Typical Queries
Once configured, you can ask your agent:
- "Find all functions that call the `update_user` method."
- "Show me the inheritance tree for the `BaseAgent` class."
- "What are the core dependencies of the `auth` module?"

## Related tools / concepts
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Claude Code](../development_ops/claude-code.md)
- [Qwen](../ai_knowledge/qwen.md)
- [Graph RAG](../../knowledge_base/patterns/rag.md)
- [Aider](../development_ops/openhands.md)
- [Cursor](../development_ops/index.md)
- [vLLM](../infrastructure/vllm.md)

## Sources / References
- [Official GitHub Repository](https://github.com/CodeGraphContext/CodeGraphContext)
- [Official Documentation](https://codegraphcontext.github.io/)
- [Reddit: CodeGraphContext v0.3.0 Release](https://www.reddit.com/r/mcp/comments/1rs083q/codegraphcontext_an_mcp_server_that_converts_your/)
- [CodeGraphContext Website](https://codegraphcontext.vercel.app/)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
