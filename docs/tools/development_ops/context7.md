# Context7

## What it is
Context7 is an Upstash project that gives coding agents and AI editors access to current library and framework documentation through a dedicated context layer. It acts as a specialized RAG (Retrieval-Augmented Generation) source specifically for software documentation.

## What problem it solves
It reduces one of the biggest failure modes in coding agents: confidently using stale or hallucinated package APIs because the base model does not know the latest docs. By providing "up-to-the-minute" documentation, it ensures agents use the correct parameters and methods for fast-moving libraries.

## Where it fits in the stack
**Development & Ops / Context Retrieval**. It acts as a live documentation layer for coding agents rather than a general-purpose search engine.

## Typical use cases
- **Grounding Agents**: Keeping agents accurate when working with beta or rapidly changing SDKs.
- **API Reference**: Supplying the agent with exact method signatures during implementation.
- **Upgrading Dependencies**: Helping an agent migrate code by providing the latest documentation for the target version.
- **MCP-based Tooling**: Providing documentation as a tool for [Model Context Protocol](../automation_orchestration/mcp.md) compatible agents.

## Strengths
- **Accuracy**: Targeted documentation retrieval is more reliable than general web search.
- **Latency**: Optimized for the "coding loop" to provide fast doc lookups.
- **Up-to-Date**: Specifically designed to index the latest documentation releases.
- **Developer-Friendly**: Seamless integration with [Claude Code](claude-code.md), [Aider](aider.md), and [Cursor](cursor.md).

## Limitations
- **Scope**: Best for popular libraries and frameworks; may lack coverage for obscure or internal private docs.
- **Dependency**: Requires an active connection to the Context7 service (or its API).

## When to use it
- When the task depends on up-to-date SDK or framework behavior (e.g., Next.js App Router, latest LangChain).
- When coding agents repeatedly guess outdated APIs or use deprecated methods.
- When working in an ecosystem (like JS/TS) where libraries evolve quickly.

## When not to use it
- When the work is entirely repo-local and no external docs are needed.
- When general web research (news, sentiment, trends) matters more than package documentation.

## Getting started

### Installation
For most users, Context7 is used via the official MCP server:

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
You can test the MCP server directly using `mcp-cli`:

```bash
# Search for documentation on a specific package
mcp-cli call context7 search --package "supabase" --query "how to use upsert"

# Get specific documentation sections
mcp-cli call context7 get_section --package "nextjs" --section "routing/app-router"

# List available packages in Context7 index
mcp-cli call context7 list_packages
```

## API examples

### Python Integration
Context7 can be used programmatically to ground your custom agents:

```python
import requests

def fetch_package_docs(package_name, query):
    """
    Fetches the latest documentation for a package using Context7.
    """
    url = f"https://context7.upstash.io/docs/{package_name}/search"
    response = requests.get(url, params={"q": query})
    return response.json()["content"]

# Usage
# content = fetch_package_docs("langchain", "how to use FastMCP 3.0")
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
- [OpenSwarm](openswarm.md) — For orchestrating documentation lookups in multi-agent swarms.

## Sources / references
- [Context7 GitHub Repository](https://github.com/upstash/context7)
- [Upstash Website](https://upstash.com/)
- [Upstash Documentation](https://docs.upstash.com/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
