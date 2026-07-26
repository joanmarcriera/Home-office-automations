# Claude Tool Search Pattern

## What it is
A tool-selection pattern where Claude discovers and chooses tools based on task intent, tool metadata, and iterative execution feedback. It involves a "planning" or "discovery" step where the model explicitly searches for the most relevant tool before attempting an execution. This pattern has become the industry standard for Claude 5.1 and GPT-5.5 agents managing heterogeneous toolsets.

## What problem it solves
Naive tool-calling often fails when an agent is presented with a large or overlapping tool catalog. The Claude Tool Search pattern improves reliability by making tool selection an explicit, model-guided process, reducing "wrong tool" hallucinations and improving first-shot accuracy in complex workflows. It specifically addresses the "context window saturation" problem encountered when passing 100+ tool definitions to Llama 4 Maverick models.

## Where it fits in the stack
Orchestration Layer — sits in the agentic loop, specifically at the intersection of planning and tool routing. It is commonly implemented within [Agentic Workflows](agentic-workflows.md) using frameworks like [LangChain](../../tools/ai_knowledge/langchain.md), [AG2](../../tools/frameworks/ag2.md), or [FastMCP](../../tools/automation_orchestration/mcp.md).

## Typical use cases
- **Massive Tool Catalogs**: Managing agents that have access to 50+ specialized tools where a single prompt cannot reliably include all schemas.
- **Dynamic Capabilities**: Environments where tools are added or removed frequently, and the agent must "explore" what is currently available.
- **Ambiguous Intents**: When a user request (e.g., "Check my status") could map to multiple systems (Jira, GitHub, Vikunja) and the agent needs to search tool descriptions to disambiguate.
- **MCP 3.1 Task Protocol Discovery**: Querying remote MCP servers for dynamic task specifications and parameters in September 2026 workflows.

## Strengths
- **Improved Accuracy**: Higher success rates in complex tool selection scenarios.
- **Scalability**: Allows agents to handle far more tools than would fit in a standard context window.
- **Transparency**: The explicit search step provides an audit trail of *why* a particular tool was chosen.
- **Model Agnostic**: Works effectively across Claude 5.1 (Opus/Sonnet), GPT-5.5 (Omni), and Llama 4 Maverick.

## Limitations
- **Latency**: Adding a discovery step increases the time to the first action.
- **Token Cost**: Multiple round-trips for search and then execution increase token consumption.
- **Description Sensitivity**: Highly dependent on high-quality, semantic tool descriptions.
- **Consistency Risks**: If tool-indexing is incomplete, search results may drop viable candidates.

## When to use it
- When an agent has access to a broad, diverse toolset where overlap is possible.
- In RAG-style tool selection (Retrieval Augmented Tool Selection).
- When building multi-agent systems where a "supervisor" routes tasks to specialized workers.

## When not to use it
- For simple, deterministic tasks with a small (< 5) toolset.
- When ultra-low latency is the primary performance metric.
- In scenarios where tool execution is strictly sequential and pre-defined.

## Getting started
To implement this pattern, you first need a centralized tool registry. As of September 2026, the [Model Context Protocol (MCP 3.1)](tool-calling-and-mcp.md) is the recommended standard.

1.  **Define Tool Metadata**: Ensure every tool has a descriptive `description` field for semantic search.
2.  **Index Tools**: Use a vector database like [ChromaDB](../vector-db-comparison.md) to store tool schemas and descriptions.
3.  **Create the Search Tool**: Implement a tool that performs a semantic search over the index.

## CLI examples
> [!NOTE]
> This is a design pattern, not a standalone CLI tool. However, it can be tested using the [FastMCP CLI](../../tools/automation_orchestration/mcp.md).

```bash
# Search for available tools via FastMCP
mcp search "calendar"

# Inspect a specific tool schema under MCP 3.1 task protocol
mcp inspect "gcal_create_event" --protocol mcp-3.1

# Execute a tool with manual parameters for testing
mcp call "gcal_create_event" --params '{"summary": "Test"}'
```

## API examples
Example of implementing the discovery logic in Python using the Anthropic Claude 5.1 SDK:

```python
import anthropic

client = anthropic.Anthropic()

# The system prompt instructs the model to use the search_tools first
response = client.messages.create(
    model="claude-5-1-opus-20260831",
    max_tokens=1024,
    system="Search for tools before execution if you are unsure which one to use.",
    tools=[{
        "name": "search_tools",
        "description": "Searches for tool schemas by semantic query",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}}
        }
    }],
    messages=[{"role": "user", "content": "Schedule a meeting for tomorrow."}]
)
```

### Technical Implementation Example
A common implementation involves a two-stage approach:

#### Phase 1: Tool Discovery
The agent is given a `search_tools` tool that allows it to query a tool registry (e.g., [MCP Registry](../../tools/automation_orchestration/mcp-registry.md)).

```json
{
  "name": "search_tools",
  "description": "Searches the tool registry for tools matching the query.",
  "parameters": {
    "query": "search for calendar management tools"
  }
}
```

#### Phase 2: Targeted Execution
Once the relevant tool ID is found, the agent calls the specific tool with the required parameters.

```json
{
  "name": "gcal_create_event",
  "parameters": {
    "summary": "Meeting with Team",
    "start_time": "2026-09-03T10:00:00Z"
  }
}
```

## Related tools / concepts
- [Anthropic Claude](../../tools/providers/anthropic.md)
- [Agentic Workflows](agentic-workflows.md)
- [Model Context Protocol (MCP 3.0/3.1)](tool-calling-and-mcp.md)
- [MCP Registry](../../tools/automation_orchestration/mcp-registry.md)
- [Agent Protocols](../agent_protocols.md)
- [Skills Best Practices](skills-best-practices.md)
- [Tool Calling Guide](tool-calling-and-mcp.md)
- [LangChain](../../tools/ai_knowledge/langchain.md)
- [LLM Trust Boundaries](llm-trust-boundaries.md)

## Sources / References
- [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use)
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [MCP Foundation Specification v3.1 (August 2026)](https://mcp-foundation.org/spec)

## Contribution Metadata
- Last reviewed: 2026-09-02
- Confidence: high
