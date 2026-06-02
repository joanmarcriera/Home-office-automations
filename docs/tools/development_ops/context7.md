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

## Strengths
- **Accuracy**: Targeted documentation retrieval is more reliable than general web search.
- **Latency**: Optimized for the "coding loop" to provide fast doc lookups.
- **Up-to-Date**: Specifically designed to index the latest documentation releases.

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

## Technical Integration

Context7 can be used as a "Context Provider" in modern AI editors or as a tool for autonomous agents.

### Example Agent Tool Configuration
If using a custom agent, you can define a tool to fetch documentation from Context7:

```python
import requests

def fetch_package_docs(package_name, query):
    """
    Fetches the latest documentation for a package using Context7.
    """
    url = f"https://context7.upstash.io/docs/{package_name}/search"
    response = requests.get(url, params={"q": query})
    return response.json()["content"]

# Example usage by the agent:
# content = fetch_package_docs("supabase", "how to use upsert with filters")
```

### Integration: Claude Desktop Config
You can expose Context7 to Claude via an MCP server that wraps the Context7 API.

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/mcp-server-context7"],
      "env": {
        "UPSTASH_REDIS_REST_URL": "...",
        "UPSTASH_REDIS_REST_TOKEN": "..."
      }
    }
  }
}
```

## Example company use cases
- **Internal app team**: feed current Supabase, Next.js, and Stripe docs into coding agents so generated code matches current APIs.
- **Automation team**: keep n8n, Google Workspace, and Claude-related integrations grounded in current docs instead of old examples.
- **Consulting/agency workflow**: use Context7 for client stacks you do not work with every week, so agents can ramp faster without risky guesswork.

## Selection comments
- Use **Context7** when the question is "what does the current SDK do?"
- Use **Tavily** when the question is "what is happening on the web right now?"
- Use **Claude Cookbooks** when the question is "show me a first-party implementation pattern."

## Related tools / concepts
- [Claude Code](claude-code.md)
- [Claude Context Mode](claude-context-mode.md)
- [Claude Cookbooks](claude-cookbooks.md)
- [Tavily](../providers/tavily.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [LangChain](../ai_knowledge/langchain.md)

## Sources / References
- [Context7 GitHub Repository](https://github.com/upstash/context7)
- [Upstash Website](https://upstash.com/)
- [awesome-context7](https://github.com/upstash/awesome-context7)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
