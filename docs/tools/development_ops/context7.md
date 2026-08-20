# Context7

## What it is
Context7 is an Upstash project that gives coding agents and AI editors access to current library and framework documentation through a dedicated context layer. It acts as a specialized RAG (Retrieval-Augmented Generation) source specifically for software documentation using FastMCP 3.1 protocols.

## What problem it solves
It reduces one of the biggest failure modes in coding agents: confidently using stale or hallucinated package APIs because the base model does not know the latest docs. By providing "up-to-the-minute" documentation, it ensures agents use the correct parameters and methods for fast-moving libraries. This is particularly crucial when coordinating state-of-the-art models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **DeepSeek-V4**.

## Where it fits in the stack
**Development & Ops / Context Retrieval**. It acts as a live documentation layer for coding agents rather than a general-purpose search engine.

## Typical use cases
- **Grounding Agents**: Keeping agents accurate when working with beta or rapidly changing SDKs.
- **API Reference**: Supplying the agent with exact method signatures during implementation.
- **Upgrading Dependencies**: Helping an agent migrate code by providing the latest documentation for the target version.
- **MCP-based Tooling**: Providing documentation as a tool for [Model Context Protocol](../automation_orchestration/mcp.md) compatible agents.

## Strengths
- **Accuracy**: Targeted documentation retrieval is more reliable than general web search.
- **Latency**: Optimized for the "coding loop" to provide fast doc lookups via FastMCP 3.1 transport.
- **Up-to-Date**: Specifically designed to index the latest documentation releases.
- **Developer-Friendly**: Seamless integration with [Claude Code](claude-code.md), [Aider](aider.md), and [Cursor](cursor.md).

## Limitations
- **Scope**: Best for popular libraries and frameworks; may lack coverage for obscure or internal private docs.
- **Dependency**: Requires an active connection to the Context7 service (or its API).

## When to use it
- When the task depends on up-to-date SDK or framework behavior (e.g., Next.js App Router, latest LangChain, Pydantic v2.10+).
- When coding agents repeatedly guess outdated APIs or use deprecated methods.
- When working in an ecosystem (like JS/TS or Python) where libraries evolve quickly.

## When not to use it
- When the work is entirely repo-local and no external docs are needed.
- When general web research (news, sentiment, trends) matters more than package documentation.

## Getting started

### Installation
For most users, Context7 is used via the official FastMCP server:

```bash
npx -y @upstash/mcp-server-context7
```

### Configuration for Claude Desktop
Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/mcp-server-context7"],
      "env": {
        "UPSTASH_REDIS_REST_URL": "YOUR_URL",
        "UPSTASH_REDIS_REST_TOKEN": "YOUR_TOKEN"
      }
    }
  }
}
```

## CLI examples

### Querying Documentation via MCP CLI
You can test the MCP server directly using `mcp-cli` under FastMCP 3.1:

```bash
# Search for documentation on a specific package
mcp-cli call context7 search --package "supabase" --query "how to use upsert"

# Get specific documentation sections
mcp-cli call context7 get_section --package "nextjs" --section "routing/app-router"

# List available packages in Context7 index
mcp-cli call context7 list_packages
```

## API examples

### Python Integration (Pydantic v2 Validation)
Context7 can be used programmatically to ground custom agent workflows (such as those using **Claude 5.1**, **GPT-5.5**, or **Gemini 4.0 Pro**). Below is a fully validated implementation utilizing Pydantic v2:

```python
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
import requests

class Context7SearchResult(BaseModel):
    package_name: str = Field(..., description="Name of the queried package")
    query: str = Field(..., description="The search query submitted")
    content: str = Field(..., description="The retrieved documentation context")
    relevance_score: float = Field(..., description="The relevance confidence score of the match")
    source_url: Optional[HttpUrl] = Field(None, description="Direct link to the canonical documentation page")

def fetch_package_docs(package_name: str, query: str) -> Context7SearchResult:
    """
    Fetches the latest documentation for a package using Context7.
    Validates and formats the result using Pydantic v2.
    """
    url = f"https://context7.upstash.io/docs/{package_name}/search"
    response = requests.get(url, params={"q": query}, timeout=10)
    response.raise_for_status()

    # Parse and validate response using Pydantic v2 model_validate
    payload = response.json()
    return Context7SearchResult.model_validate(payload)

# Usage
# result = fetch_package_docs("langchain", "how to use FastMCP 3.1")
# print(f"Context relevance: {result.relevance_score}")
# print(result.content)
```

## Related tools / concepts
- [Claude Code](claude-code.md) — Anthropic's agentic coding CLI.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for tool integration.
- [Aider](aider.md) — Terminal-native pair programmer.
- [Cursor](cursor.md) — AI-native IDE.
- [Tavily](../providers/tavily.md) — General web search for AI agents.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — The underlying architecture for Context7.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Used for indexing and retrieval patterns.
- [FastMCP](../automation_orchestration/mcp.md) — Standard for high-speed MCP server development.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) — For agentic calendar orchestration.
- [Free Will MCP](free-will-mcp.md) — For AI autonomy and self-prompting.

## Sources / References
- [Context7 GitHub Repository](https://github.com/upstash/context7)
- [Upstash Website](https://upstash.com/)
- [Upstash Documentation](https://docs.upstash.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
