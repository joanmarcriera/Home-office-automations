# mem0

## What it is
mem0 is a specialized memory layer for AI agents and applications that stores and retrieves durable user, task, and workflow context over time. In the June 2026 landscape, it provides the "long-term memory" required for agents using **Claude 4.8 Opus** and **GPT-5.5** to maintain personality and continuity across multi-session interactions.

## What problem it solves
It prevents every agent interaction from starting from zero ("Groundhog Day" effect). Instead of cramming massive amounts of historical context into prompt windows—which increases latency and cost—mem0 externalizes memory into a system that can be dynamically updated and retrieved based on relevance.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as a **Persistent Memory Layer** that sits between the LLM and the application logic.

## Typical use cases
- **Personalized Assistants**: Remembering user preferences, habits, and past feedback across sessions.
- **Enterprise Workflows**: Persisting account, project, or process context for agents operating in long-running business cycles.
- **Agent Self-Improvement**: Tracking an agent's own performance and prior decisions to refine its future actions.

## Strengths
- **Multi-level Scopes**: Supports memory at the User, Session, and Agent levels.
- **Hybrid Search**: Combines semantic search with structured filters for precise recall.
- **Framework Agnostic**: Integrates seamlessly with LangChain, CrewAI, Agno, and other orchestration frameworks.
- **Context Management**: Optimized for reducing prompt bloat by providing only the most relevant memories.

## Limitations
- **Latency**: Retrieving external memories adds a small overhead to the initial prompt generation.
- **Privacy**: Requires careful handling of User ID and data scoping to ensure compliance with data protection standards.

## When to use it
- When agents need to "know" the user over days, weeks, or months.
- For complex projects where context exceeds the efficient reasoning capacity of the context window.
- To reduce token costs by externalizing historical data.

## When not to use it
- For stateless, one-off tasks where prior context is irrelevant.
- When simple database lookups (e.g., a CRM) are sufficient for the required context.

## Getting started
### Installation
```bash
pip install mem0ai
```

### Basic Usage (Python SDK)
```python
from mem0 import Memory

# 1. Initialize Memory
m = Memory()

# 2. Add a memory for a user
messages = [
    {"role": "user", "content": "I am working on a Rust project using Claude 4.8."},
    {"role": "assistant", "content": "I'll remember you're using Rust and Claude 4.8 for your project."}
]
m.add(messages, user_id="dev_user_123")

# 3. Search memories
results = m.search("What is the user's current project?", filters={"user_id": "dev_user_123"})
print(results)
```

## CLI examples
```bash
# Initialize the mem0 configuration
mem0 init --api-key your-api-key --user-id dev_user

# Add a specific memory
mem0 add "User prefers async/await patterns in Python" --user-id dev_user

# Search for relevant memories
mem0 search "Python preferences" --user-id dev_user

# List all memories associated with a user
mem0 list --user-id dev_user
```

## API examples
The mem0 platform provides a REST API for memory management. Example usage with `curl`:

```bash
curl -X POST "https://api.mem0.ai/v1/memories/" \
     -H "Authorization: Token your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "I prefer dark mode in my IDE."}], "user_id": "dev_user"}'
```

## Related tools / concepts
- [Agno](./agno.md)
- [Phidata](phidata.md)
- [LangChain](../ai_knowledge/langchain.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Supabase](../infrastructure/supabase.md) (Alternative for general state)
- [Browser Use](../automation_orchestration/browser-use.md)

## Sources / references
- [Official Website](https://mem0.ai/)
- [GitHub Repository](https://github.com/mem0ai/mem0)
- [Mem0 Documentation](https://docs.mem0.ai/)
- [CLI Reference](https://docs.mem0.ai/platform/cli)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
