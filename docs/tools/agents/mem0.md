# Mem0

## What it is
Mem0 (v2.5+, early January 2027) is a specialized memory and personalization layer for AI agents and applications that stores, prioritizes, and retrieves durable user, task, and workflow context over time. Often described as the "long-term memory" of the agentic stack, it enables agents powered by [Claude 5.6](../providers/anthropic.md), [GPT-5.6](../ai_knowledge/chatgpt.md), [Gemini 4.0 Ultra](../providers/google.md), and [Gemma 4](../ai_knowledge/local_llms.md) to maintain personalized, consistent continuity across multi-session interactions. It features native, first-class support for the [Model Context Protocol (MCP) 3.1](../../knowledge_base/agent_protocols.md) and FastMCP 3.1 specifications.

## What problem it solves
Traditional RAG can feel like "Groundhog Day" for agents; every new session starts from scratch unless extensive chat histories are loaded, which wastes context window capacity and increases latency/cost. Mem0 externalizes this dynamic memory layer, enabling real-time learning, automatic extraction of user preferences, and cross-session persistence. Additionally, it solves the "siloed memory" bottleneck in multi-agent environments by acting as a shared, synchronized context plane.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as the **Persistent Context and Memory Layer** sitting between the core reasoning LLM and application database integrations.

## Typical use cases
- **Continuous Personalization**: Remembering user-specific coding style guidelines, API constraints, and environmental layouts across days or months.
- **Enterprise Workflow Persistence**: Tracking project schedules, task checklists, and cross-team dependencies in long-running software factory implementation runs.
- **Cross-Agent Knowledge Synchronization**: Exchanging state and learned facts between a planner agent and a code generator agent via a FastMCP 3.1 gateway.
- **Local Privacy-First Memory**: Running local vector databases (e.g., [Supabase](../infrastructure/supabase.md)) alongside [Gemma 4](../ai_knowledge/local_llms.md) to preserve sensitive on-premise user profiles.

## Strengths
- **Hierarchical Scopes**: Native separation of User, Session, and Agent-level memory boundaries.
- **FastMCP 3.1 Compatibility**: Seamlessly exposes memory retrieval and update mechanics as standard MCP tools.
- **Adaptive Learning**: Dynamically parses conversations to extract, update, or deprecate memory items without manual tagging.
- **Framework Agnostic**: Integrates natively with [Agno](./agno.md), [Bee Agent Framework](./bee-agent-framework.md), [CrewAI](../frameworks/crewai.md), and [LangGraph](../frameworks/langgraph.md).

## Limitations
- **Latency Cost**: Accessing external memory stores adds an extra lookup hop prior to prompt compilation.
- **Conflict Resolution**: Resolving contradictory statements in active, high-velocity conversation logs can occasionally require manual intervention.
- **Sovereignty Scrutiny**: For enterprise deployments, passing sensitive personal data through managed memory clouds requires strict compliance guards.

## When to use it
- When your agents require long-term context to assist users over prolonged timeframes.
- To reduce prompting costs by referencing concise long-term profiles instead of injecting massive raw chat logs.
- When orchestrating complex, multi-agent systems where agents must read from and write to a unified session record.

## When not to use it
- For completely stateless, one-off execution tasks where previous context is irrelevant.
- If a simple relational database lookup or custom metadata field on a User model satisfies the state requirement.
- In highly synchronous, real-time control loops where sub-10ms latency is mandatory.

## Getting started
### Installation
```bash
pip install mem0ai pydantic
```

### Basic Usage
Initialize Mem0 with FastMCP 3.1 configurations and store user preference data:
```python
from mem0 import Memory

# Initialize Memory with custom config
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333}
    },
    "mcp_version": "3.1"
}
m = Memory.from_config(config)

# Add a conversational interaction
messages = [
    {"role": "user", "content": "I prefer dark mode in my IDE and typically write asynchronous Python with Gemma 4."},
    {"role": "assistant", "content": "Understood. I will store those environment preferences."}
]
m.add(messages, user_id="dev_user_77")
```

## CLI examples
```bash
# Initialize Mem0 configuration on your local development machine
mem0 init --api-key your-api-key-here

# Manually register a user preference
mem0 add "Prefers strict typing in all FastAPI endpoints" --user-id dev_user_77

# Search memories using natural language
mem0 search "What are the preferred styles of user dev_user_77?" --user-id dev_user_77

# Export all scoped session memories to a JSON report
mem0 list --user-id dev_user_77 --format json
```

## API examples
### Python Schema & Memory Validation (Pydantic v2)
In production workflows, ensuring the memory payload complies with strict data contracts is crucial for downstream agent execution. The following example demonstrates how to validate incoming memory items using Pydantic v2:

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class MemoryItem(BaseModel):
    id: str = Field(..., description="Unique memory record identifier")
    text: str = Field(..., description="The captured semantic fact or preference")
    score: float = Field(..., ge=0.0, le=1.0, description="Semantic match relevance score")
    categories: List[str] = Field(default_factory=list, description="Categorization tags")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MemoryPayload(BaseModel):
    user_id: str = Field(..., description="Scoped user reference")
    session_id: Optional[str] = Field(None, description="Active session ID scope")
    memories: List[MemoryItem] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom contextual metadata")

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value: str) -> str:
        if not value.isalnum() and "_" not in value and "-" not in value:
            raise ValueError("user_id must be alphanumeric or contain underscores/hyphens")
        return value

# Sample payload from Mem0 vector store search
search_data = {
    "user_id": "dev_user_77",
    "session_id": "sess-jan-2027",
    "memories": [
        {
            "id": "mem-01J3K",
            "text": "User prefers dark mode and async FastAPI patterns.",
            "score": 0.94,
            "categories": ["editor", "backend"],
            "created_at": "2027-01-07T10:15:30Z"
        }
    ],
    "metadata": {
        "model_context": "gemma4-31b",
        "mcp_protocol_version": "3.1"
    }
}

# Perform strict validation
validated_payload = MemoryPayload(**search_data)
print(f"Validated Memory for: {validated_payload.user_id}")
print(f"Memory Text: {validated_payload.memories[0].text} (Score: {validated_payload.memories[0].score})")
```

### Direct REST Integration via cURL
Retrieve memories programmatically using the standardized REST endpoint:
```bash
curl -X POST "https://api.mem0.ai/v1/memories/search" \
     -H "Authorization: Token your-api-key" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "coding patterns",
       "user_id": "dev_user_77",
       "limit": 5
     }'
```

## Related tools / concepts
- [Agno](./agno.md)
- [Bee Agent Framework](./bee-agent-framework.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Supabase](../infrastructure/supabase.md) (Vector store database)
- [Gemma 4](../ai_knowledge/local_llms.md)
- [Claude 5.6](../providers/anthropic.md)
- [GPT-5.6](../ai_knowledge/openai.md)

## Sources / references
- [Official Website](https://mem0.ai/)
- [GitHub Repository](https://github.com/mem0ai/mem0)
- [Mem0 Documentation](https://docs.mem0.ai/)
- [FastMCP 3.1 Memory Specifications](https://docs.mem0.ai/protocols/fastmcp3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
