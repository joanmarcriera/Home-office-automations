# CodeGraphContext

## What it is
CodeGraphContext is a specialized [Model Context Protocol (MCP)](mcp.md) server designed to convert codebases into graph databases. It allows AI agents to understand the relationships, dependencies, and structure of a project through a knowledge graph interface. As of early January 2027, it is a cornerstone of the **MCP 3.1 / FastMCP 3.1 Task Protocol** ecosystem, enabling complex multi-file reasoning for frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

## What problem it solves
It addresses the challenge of "context window overload" and "hallucination" when AI agents reason over large codebases. By providing a graph-based representation, it enables massive token reduction (up to 120x in benchmarks), allowing agents to fetch only the relevant nodes (functions, classes, calls) and edges rather than the entire file content. It solves the "lost in the middle" problem for long-context models by providing precise semantic pointers and efficient **FastMCP 3.1** tool access.

## Where it fits in the stack
**Automation & Orchestration / MCP Server**. It acts as a bridge between an agent (like [Claude Code](../development_ops/claude-code.md) or a local LLM) and the raw source code, providing a structured, semantic view of the project. It integrates natively with the **MCP 3.1 / FastMCP 3.1** ecosystem.

## Typical use cases
- **Semantic Code Search**: Finding functions or classes based on their relationships and intent rather than just keyword matches.
- **Dependency Analysis**: Asking an agent to explain the impact of changing a specific module across the entire project.
- **Architectural Mapping**: Generating a high-level overview of how different components of a system interact.
- **Onboarding Agents**: Quickly providing a new agentic loop with a "mental map" of an unfamiliar codebase.

## Strengths
- **Token Efficiency**: Dramatic reduction in context usage compared to raw text ingestion, preserving the model's reasoning capacity.
- **Semantic Precision**: Indexes files, functions, classes, calls, imports, and inheritance at the symbol level.
- **Language Support**: Supports 15+ coding languages (including Python, TypeScript, Go, and Rust) as of early 2027.
- **MCP 3.1 / FastMCP 3.1 Native**: Integrates seamlessly with any MCP-compliant client (e.g., Claude Desktop, [Cursor](../development_ops/index.md), [Claude Code](../development_ops/claude-code.md)).
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
CodeGraphContext is available as a Python package and can be integrated into MCP clients like Claude Desktop.

### Installation
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

## CLI examples
The `codegraphcontext` CLI allows for manual indexing and server management.

```bash
# Index a repository manually
codegraphcontext index --path /path/to/repo --output ./repo.graph

# Start the MCP server using a pre-indexed graph
codegraphcontext serve --db ./repo.graph

# Export the graph to a web-based visualizer
codegraphcontext visualize --db ./repo.graph --port 3000
```

## API examples

### Programmatic Setup with Pydantic v2 Validation
To maintain the safety and integrity of code-graph querying in early January 2027, structured inputs and outputs must be strictly validated. Below is a robust Python example utilizing **Pydantic v2** validation.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

# 1. Define schemas using strict Pydantic v2 annotations
class GraphQuery(BaseModel):
    query: str = Field(..., min_length=10, description="The Cypher or semantic graph query string.")
    parameters: Optional[dict] = Field(default=None, description="Optional parameters for the query.")
    timeout_ms: int = Field(default=5000, ge=1000, le=30000, description="Execution timeout limit in milliseconds.")

class NodeProperties(BaseModel):
    name: str
    type: str
    file_path: Optional[str] = None

class QueryResultNode(BaseModel):
    id: str
    properties: NodeProperties

# 2. Programmatic execution utilizing validation and MCP client interactions
async def execute_validated_graph_query(payload: dict) -> List[QueryResultNode]:
    try:
        # Strict validation of input using Pydantic v2
        validated_query = GraphQuery.model_validate(payload)
    except ValidationError as e:
        print(f"Validation failed: {e}")
        raise

    # Simulated FastMCP 3.1 connection & tool calling
    print(f"Executing validated query with timeout {validated_query.timeout_ms}ms...")

    # In a production early 2027 FastMCP 3.1 environment, this interacts with CodeGraphContext
    # Here we simulate structured response parsing and validation
    simulated_response = [
        {
            "id": "node_1",
            "properties": {
                "name": "main",
                "type": "Function",
                "file_path": "src/main.py"
            }
        },
        {
            "id": "node_2",
            "properties": {
                "name": "execute_task",
                "type": "Function",
                "file_path": "src/orchestrator.py"
            }
        }
    ]

    try:
        # Validate returned dataset against our schemas
        validated_results = [QueryResultNode.model_validate(node) for node in simulated_response]
        return validated_results
    except ValidationError as e:
        print(f"Response validation failed: {e}")
        raise

# Example invocation in early 2027
if __name__ == "__main__":
    query_payload = {
        "query": "MATCH (f:Function)-[:CALLS]->(d:Function) RETURN f, d",
        "parameters": {},
        "timeout_ms": 10000
    }
    results = asyncio.run(execute_validated_graph_query(query_payload))
    for res in results:
        print(f"Found node: {res.properties.name} ({res.properties.type}) in {res.properties.file_path}")
```

## Related tools / concepts
- [MCP (Model Context Protocol)](mcp.md) — The underlying protocol for tool communication.
- [Claude Code](../development_ops/claude-code.md) — The primary agentic CLI that uses CodeGraphContext.
- [Aider / OpenHands](../development_ops/openhands.md) — Alternative agentic coding tools.
- [Graph RAG](../../knowledge_base/patterns/rag.md) — The reasoning pattern enabled by this tool.
- [vLLM](../infrastructure/vllm.md) — High-performance inference for the agents using this context.
- [Cursor](../development_ops/index.md) — IDE with native support for similar graph-based context.
- [Gemma 4](../ai_knowledge/local_llms.md) — High-performance local model compatible with MCP 3.1 / FastMCP 3.1 Task Protocol.
- [FastMCP 3.1](mcp.md) — Accelerated tool interaction protocol for low-latency graph queries.

## Sources / references
- [Official GitHub Repository](https://github.com/CodeGraphContext/CodeGraphContext)
- [Official Documentation](https://codegraphcontext.github.io/)
- [Reddit: CodeGraphContext v0.3.0 Release](https://www.reddit.com/r/mcp/comments/1rs083q/codegraphcontext_an_mcp_server_that_converts_your/)
- [CodeGraphContext Website](https://codegraphcontext.vercel.app/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
