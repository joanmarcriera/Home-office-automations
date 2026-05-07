# mem0

## What it is
mem0 is a memory layer for AI agents and AI applications that stores and retrieves durable user, task, and workflow context over time.

## What problem it solves
It prevents every agent interaction from starting from zero. Instead of cramming long-term context into prompts, mem0 externalizes memory into a system that can be updated and retrieved as needed.

## Where it fits in the stack
**Agents / Memory Layer**. It sits between the model and application logic as persistent memory infrastructure for agents.

## Typical use cases
- Remembering user preferences across sessions
- Persisting account, project, or process context for agents
- Tracking multi-step work across long-running company workflows

## CLI examples
```bash
# Initialize the mem0 configuration and authenticate
mem0 init --api-key your-api-key --user-id alex

# Add a specific memory for a user
mem0 add "I prefer dark mode and use vim keybindings" --user-id alex

# Search for relevant memories based on a query
mem0 search "What are Alice's preferences?" --user-id alice

# List all memories associated with a user
mem0 list --user-id alex
```

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

# 2. Add a memory
messages = [
    {"role": "user", "content": "Hi, I'm Alex. I love basketball and gaming."},
    {"role": "assistant", "content": "Hey Alex! I'll remember your interests."}
]
m.add(messages, user_id="alex")

# 3. Search memories
results = m.search("What do you know about me?", filters={"user_id": "alex"})
print(results)
```

## Strengths
- Clear fit for agent memory and personalization
- Useful for cross-session continuity
- Strong complement to workflow and browser agents
- Supports multiple memory scopes: User, Session, and Agent

## Limitations
- Adds complexity if the workflow does not truly need persistence
- Poor memory design can create noisy or low-value recall

## When to use it
- When the same users, accounts, or projects recur over time
- When agents need to remember preferences, history, or prior decisions

## When not to use it
- When each task is isolated and stateless
- When a simple database table or CRM field is enough

## Example company use cases
- **Sales assistant**: remember preferred outreach angles, prior objections, and account stage per lead.
- **Ops assistant**: remember vendor-specific quirks, invoice routing rules, and approval boundaries.
- **Content team**: remember channel voice, past winning hooks, and audience-specific formatting preferences.

## Selection comments
- Use **mem0** when you need long-lived memory that should survive across sessions.
- Use **Supabase** when you need general app state and relational data but not specialized memory behavior.
- Use **n8n** when you need process execution and scheduling, not memory by itself.

## API examples
The mem0 platform provides a REST API for memory management. Example usage with `curl`:

```bash
curl -X POST "https://api.mem0.ai/v1/memories/" \
     -H "Authorization: Token your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "I am traveling to Tokyo next week."}], "user_id": "alex"}'
```

## Related tools / concepts
- [Browser Use](../automation_orchestration/browser-use.md)
- [n8n](../../services/n8n.md)
- [Supabase](../infrastructure/supabase.md)
- [LangChain](../ai_knowledge/langchain.md)
- [Agno](./agno.md)
- [Phidata](./phidata.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / References
- [Official Website](https://mem0.ai/)
- [GitHub Repository](https://github.com/mem0ai/mem0)
- [Mem0 Documentation](https://docs.mem0.ai/)
- [CLI Reference](https://docs.mem0.ai/platform/cli)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high
