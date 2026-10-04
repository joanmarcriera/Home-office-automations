# Mem0

## What it is
Mem0 (v2.5+, early 2027) is an intelligent memory and personalization layer designed for AI agents and LLM applications. Storing, prioritizing, and retrieving durable user, task, and cross-session workflow context over time, Mem0 acts as the "long-term memory" of the agentic stack.

By equipping agents powered by **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **Gemma 4** with persistent memory, Mem0 ensures personalized, consistent continuity across multi-turn interactions. It features native, first-class support for the **FastMCP 3.1 Task Protocol** specification, exposing memory retrieval, state updating, and conflict resolution mechanisms as standardized MCP tools across agent networks.

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           AGENT ORCHESTRATION LAYER                               │
│            (Claude 5.6 / GPT-5.6 / Gemini 4.0 Ultra / Gemma 4 / LangGraph)        │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │ Conversation Turns / Tool Calls
                                         ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                MEM0 MEMORY ENGINE                                 │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐  │
│  │   User-Level Scope    │  │  Session-Level Scope  │  │   Agent-Level Scope   │  │
│  │ (User Preferences)    │  │ (Active Context Runs) │  │ (Shared World Facts)  │  │
│  └───────────┬───────────┘  └───────────┬───────────┘  └───────────┬───────────┘  │
│              └──────────────────────────┼──────────────────────────┘              │
│                                         │                                         │
│                   ┌─────────────────────▼─────────────────────┐                   │
│                   │  Dynamic Extraction & Deduplication   │                   │
│                   │ (Fact Parsing / Preference Decay)  │                   │
│                   └─────────────────────┬─────────────────────┘                   │
└─────────────────────────────────────────┼─────────────────────────────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  │                                               │
┌─────────────────▼───────────────────────┐   ┌───────────────────▼─────────────────┐
│          VECTOR STORE BACKEND           │   │      FASTMCP 3.1 GATEWAY          │
│   (Qdrant / Supabase / Milvus / PGVector│   │ (Memory Tools for Multi-Agent)    │
└─────────────────────────────────────────┘   └─────────────────────────────────────┘
```

## What problem it solves
Standard Retrieval-Augmented Generation (RAG) approaches treat context retrieval as stateless: every new session starts from zero unless massive raw chat histories are re-injected into the prompt window. Re-injecting full conversation logs rapidly exhausts context window capacity, increases latency, and significantly elevates token costs.

Mem0 solves these limitations through dynamic, long-term memory management:
1. **Selective Preference Extraction**: Automatically parses conversation turns to distill key facts, preferences, constraints, and environmental layouts (e.g., "User prefers async FastAPI patterns and dark mode") while discarding trivial chit-chat.
2. **Hierarchical Context Scoping**: Isolates memories into User, Session, and Agent-level boundaries, preventing context leaks across multi-tenant environments.
3. **Adaptive Consolidation & Conflict Resolution**: Updates existing memory records when user preferences change (e.g., updating a target framework version) and deprecates outdated facts automatically.
4. **Shared Context Plane for Multi-Agent Systems**: Enables different agents (e.g., a Planner Agent and a Code Generator Agent) to read from and write to a unified, synchronized memory store.

## Where it fits in the stack
Mem0 operates in **Layer 6: Agents & Orchestration Infrastructure**, sitting as a persistent context layer between reasoning LLM engines and persistent database storage backends.

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                  LAYER 6: AGENT & MULTI-AGENT ORCHESTRATION                       │
│      (Agno / Bee Agent Framework / CrewAI / LangGraph / FastMCP 3.1 Gateways)     │
└────────────────────────────────────────┬──────────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼──────────────────────────────────────────┐
│                   PERSISTENT MEMORY & PERSONALIZATION LAYER                       │
│   ┌───────────────────────────────────────────────────────────────────────────┐   │
│   │                                  MEM0                                     │   │
│   │      (Hierarchical Scopes / Dynamic Extraction / FastMCP 3.1 Tools)      │   │
│   └────────────────────────────────────┬──────────────────────────────────────┘   │
└────────────────────────────────────────┼──────────────────────────────────────────┘
                                         │
┌────────────────────────────────────────▼──────────────────────────────────────────┐
│                   VECTOR STORAGE & DATABASE INFRASTRUCTURE                        │
│     ┌───────────────────────────────────┐   ┌───────────────────────────────┐     │
│     │   Qdrant / Supabase / PGVector    │   │  Redis / PostgreSQL Metadata  │     │
│     └───────────────────────────────────┘   └───────────────────────────────┘     │
└───────────────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases

### 1. Developer Environment & Coding Personalization
Persisting individual developer coding standards, preferred frameworks, naming conventions, and environment variables across IDE extensions and agentic coding workflows.

### 2. Multi-Session Enterprise Task Continuation
Maintaining continuity across long-running enterprise software development projects, tracking sub-task completion statuses and dependency updates over weeks or months.

### 3. Cross-Agent Knowledge Sharing
Synchronizing learned facts and intermediate investigation findings between specialized agents in a multi-agent team via FastMCP 3.1 memory tools.

### 4. On-Premise Privacy-First Local Memory
Running Mem0 locally alongside local vector stores (e.g., Qdrant or Supabase) and local models (e.g., Gemma 4) to ensure user context never leaves private infrastructure.

## Strengths
- **Hierarchical Memory Scoping**: Native support for User, Session, and Agent-level isolation.
- **FastMCP 3.1 Native Protocol**: Seamlessly exposes memory search, addition, and update capabilities as standardized MCP tools.
- **Automatic Fact Extraction**: Extracts and synthesizes concise semantic facts from raw conversation logs without manual tagging.
- **Framework Agnostic**: Integrates smoothly with Agno, Bee Agent Framework, CrewAI, LangGraph, and AutoGen.
- **Plug-and-Play Vector Store Support**: Compatible with Qdrant, Supabase, Milvus, PGVector, Pinecone, and Chroma.

## Limitations
- **Retrieval Latency Overhead**: Querying vector databases adds a network hop prior to model prompt compilation.
- **Conflict Management Complexity**: Resolving contradictory statements in high-frequency streams can occasionally require explicit rule tuning.
- **Privacy Scrutiny**: Storing long-term user profiles in cloud deployments requires robust encryption and governance controls.

## When to use it
- When agents require multi-session continuity and long-term personalization.
- To reduce prompting costs by referencing concise long-term profiles instead of injecting massive conversation logs.
- When orchestrating multi-agent networks that need a shared memory plane.

## When not to use it
- For single-turn, stateless tasks where previous user history is irrelevant.
- When simple relational database user metadata fields are sufficient for the application logic.
- In sub-10ms real-time control loops where vector store lookups introduce unacceptable latency.

## Getting started

### Installation
Install Mem0 and vector store drivers:

```bash
# Install Mem0 with Pydantic support
pip install mem0ai pydantic qdrant-client --upgrade
```

### Basic Usage
Initialize Mem0 with local Qdrant vector store and store user context:

```python
from mem0 import Memory

# Configure Mem0 with Qdrant vector store
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333}
    },
    "mcp_version": "3.1"
}

memory = Memory.from_config(config)

# Store conversational turns
messages = [
    {"role": "user", "content": "I prefer async Python using FastAPI and dark mode in VS Code."},
    {"role": "assistant", "content": "Got it! I have recorded your preferences."}
]

memory.add(messages, user_id="dev_user_77")
```

## CLI examples

### 1. Initialize Mem0 CLI Configuration
Configure API credentials and local defaults:

```bash
# Initialize CLI configuration
mem0 init --api-key your-mem0-key

# Verify installation and active profile
mem0 status
```

### 2. Manage User Memories via CLI
Directly add and query user memory items:

```bash
# Add a specific fact for a user
mem0 add "Prefers strict Pydantic v2 validation in all API models" --user-id dev_user_77

# Search memories using natural language
mem0 search "What are the coding preferences for dev_user_77?" --user-id dev_user_77

# List all memories for a user in JSON format
mem0 list --user-id dev_user_77 --format json
```

## API examples

### 1. FastMCP 3.1 Memory Protocol Tool Server
The following complete Python script creates a FastMCP 3.1 server exposing Mem0 operations as protocol tools:

```python
import json
from typing import Dict, Any, List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from mem0 import Memory

mcp = FastMCP("mem0-memory-server", version="3.1")
memory_engine = Memory()

class AddMemoryRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    text_content: str = Field(..., min_length=5, description="Fact or conversation to store")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class SearchMemoryRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    query: str = Field(..., min_length=2, description="Search query string")
    limit: int = Field(default=5, ge=1, le=20)

@mcp.tool(name="store_user_memory", description="Store long-term memory fact for a user")
def store_user_memory(req: AddMemoryRequest) -> Dict[str, Any]:
    result = memory_engine.add(req.text_content, user_id=req.user_id, metadata=req.metadata)
    return {"status": "SUCCESS", "result": result}

@mcp.tool(name="search_user_memory", description="Search long-term memory facts for a user")
def search_user_memory(req: SearchMemoryRequest) -> List[Dict[str, Any]]:
    results = memory_engine.search(query=req.query, user_id=req.user_id, limit=req.limit)
    return results

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 2. Strict Pydantic v2 Memory Payload Validation
Validate memory records retrieved from vector backends using **Pydantic v2**:

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime

class MemoryItemSchema(BaseModel):
    id: str = Field(..., description="Unique memory ID")
    text: str = Field(..., min_length=1, description="Captured fact text")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")
    categories: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MemorySearchResultPayload(BaseModel):
    user_id: str = Field(..., description="User ID scope")
    session_id: Optional[str] = Field(None)
    memories: List[MemoryItemSchema] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("user_id")
    @classmethod
    def validate_user_identifier(cls, v: str) -> str:
        if not v.isalnum() and "_" not in v and "-" not in v:
            raise ValueError("user_id must contain only alphanumeric characters, underscores, or hyphens")
        return v

def process_memory_payload(raw_json: str) -> Optional[MemorySearchResultPayload]:
    try:
        payload = MemorySearchResultPayload.model_validate_json(raw_json)
        return payload
    except ValidationError as e:
        print(f"Memory Payload Validation Failed: {e.errors()}")
        return None
```

## Related tools / concepts
- [Agno](./agno.md) — Multi-agent framework with native Mem0 integration.
- [Bee Agent Framework](./bee-agent-framework.md) — Open source TypeScript agent framework.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — FastMCP 3.1 protocol standard.
- [Supabase](../infrastructure/supabase.md) — Vector store backend for Mem0.
- [Gemma 4](../ai_knowledge/local_llms.md) — Canonical local open model.
- [Claude 5.6](../providers/anthropic.md) — Frontier reasoning model.

## Sources / references
- [Mem0 Official Website](https://mem0.ai/)
- [Mem0 GitHub Repository](https://github.com/mem0ai/mem0)
- [Mem0 Official Documentation](https://docs.mem0.ai/)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
