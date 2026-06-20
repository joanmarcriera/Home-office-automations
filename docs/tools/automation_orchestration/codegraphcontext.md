# CodeGraphContext

## What it is
CodeGraphContext is a specialized [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) server designed to convert codebases into graph databases. It allows AI agents to understand the relationships, dependencies, and structure of a project through a knowledge graph interface. It was one of the first major MCP servers to demonstrate the power of graph-based context for agents.

## What problem it solves
It addresses the challenge of "context window overload" and "hallucination" when AI agents reason over large codebases. By providing a graph-based representation, it enables massive token reduction (up to 120x in June 2026 benchmarks), allowing agents to fetch only the relevant nodes (functions, classes, calls) and edges rather than the entire file content. It solves the "lost in the middle" problem for long-context models by providing precise semantic pointers.

## Where it fits in the stack
**Automation & Orchestration / MCP Server**. It acts as a bridge between an agent (like [Claude Code](../development_ops/claude-code.md) or a local LLM) and the raw source code, providing a structured, semantic view of the project. It integrates with the [MCP 3.0](../../tools/automation_orchestration/mcp.md) ecosystem.

## Typical use cases
- **Semantic Code Search**: Finding functions or classes based on their relationships and intent rather than just keyword matches.
- **Dependency Analysis**: Asking an agent to explain the impact of changing a specific module across the entire project.
- **Architectural Mapping**: Generating a high-level overview of how different components of a system interact.
- **Onboarding Agents**: Quickly providing a new agentic loop with a "mental map" of an unfamiliar codebase.

## Strengths
- **Token Efficiency**: Dramatic reduction in context usage compared to raw text ingestion, preserving the model's reasoning capacity.
- **Semantic Precision**: Indexes files, functions, classes, calls, imports, and inheritance at the symbol level.
- **Language Support**: Supports 15+ coding languages (including Python, TypeScript, Go, and Rust) as of June 2026.
- **MCP 3.0 Native**: Integrates seamlessly with any MCP-compliant client (e.g., Claude Desktop, [Cursor](../development_ops/index.md), [Claude Code](../development_ops/claude-code.md)).
- **Graph RAG Integration**: Supports Graph RAG patterns for more accurate multi-step reasoning over code.

## Limitations
- **Indexing Overhead**: Initial conversion and indexing of very large codebases (e.g., millions of lines) can be resource-intensive.
- **Tool-Calling Dependency**: Highly dependent on the agent's ability to efficiently reason over and query graph structures.
- **Local Execution**: Primarily designed for local or private server execution; requires local filesystem access for indexing.

## When to use it
- When working with codebases that exceed the model's comfortable context window.
- When you need an agent to perform complex architectural analysis or cross-file refactoring tasks.
- For improving the reliability of agentic coding assistants in large, enterprise-grade repositories.
- To reduce API costs associated with sending large amounts of source code in every prompt.

## When not to use it
- For small, single-file projects where standard context ingestion is faster and sufficient.
- If you don't have an MCP-compatible client or framework set up.
- For non-code documents where general RAG solutions are more appropriate.

## Getting started

### Installation (via pip)
CodeGraphContext is available as a Python package:
```bash
pip install codegraphcontext
```

### Configuration (Claude Desktop)
Add the following to your `claude_desktop_config.json` to enable the server:

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
- "Find all functions that call the `update_user` method and show their signatures."
- "Show me the inheritance tree for the `BaseAgent` class in this repo."
- "What are the core dependencies of the `auth` module?"
- "Map the data flow from the API endpoint to the database layer."

## CLI examples
The `codegraphcontext` CLI allows for manual indexing and server management:

```bash
# Index a repository manually
codegraphcontext index --path /path/to/repo --output ./repo.graph

# Start the MCP server using a pre-indexed graph
codegraphcontext serve --db ./repo.graph

# Export the graph to a web-based visualizer
codegraphcontext visualize --db ./repo.graph --port 3000
```

## API examples
As an MCP server, CodeGraphContext exposes tools that can be called programmatically via the MCP protocol:

```python
# Example MCP tool call (concept)
tool_call = {
    "method": "tools/call",
    "params": {
        "name": "query_graph",
        "arguments": {
            "query": "MATCH (f:Function {name: 'main'})-[:CALLS]->(d) RETURN d.name"
        }
    }
}
```

## Related tools / concepts
- [MCP (Model Context Protocol)](../../tools/automation_orchestration/mcp.md) — The underlying protocol for tool communication.
- [Claude Code](../development_ops/claude-code.md) — The primary agentic CLI that uses CodeGraphContext.
- [Aider / OpenHands](../development_ops/openhands.md) — Alternative agentic coding tools.
- [Graph RAG](../../knowledge_base/patterns/rag.md) — The reasoning pattern enabled by this tool.
- [vLLM](../infrastructure/vllm.md) — High-performance inference for the agents using this context.
- [Cursor](../development_ops/index.md) — IDE with native support for similar graph-based context.

## Sources / references
- [Official GitHub Repository](https://github.com/CodeGraphContext/CodeGraphContext)
- [Official Documentation](https://codegraphcontext.github.io/)
- [Reddit: CodeGraphContext v0.3.0 Release](https://www.reddit.com/r/mcp/comments/1rs083q/codegraphcontext_an_mcp_server_that_converts_your/)
- [CodeGraphContext Website](https://codegraphcontext.vercel.app/)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
