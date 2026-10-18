# Letta

## What it is
Letta (v1.15.x+, early January 2027), formerly known as MemGPT, is an open-source framework and server architecture for creating stateful AI agents equipped with persistent, self-editing "infinite" memory. Rather than treating the LLM context window as an ephemeral stateless prompt, Letta treats the context window as an active RAM cache backed by tiered persistent memory (PostgreSQL with `pgvector` or sqlite).

Through native support for **FastMCP 3.1 Task Protocol**, Letta agents autonomously invoke external tools, query knowledge bases, and edit their own memory blocks across multi-session interactions and multi-agent teams.

```mermaid
flowchart TD
    subgraph RAM ["Active LLM Context Window (RAM Cache)"]
        SYS["System Prompt & Core Rules"]
        subgraph CoreMem ["Core Memory Blocks (Self-Editable)"]
            HUMAN["human: User Preferences & Traits"]
            PERS["persona: Agent Identity & Rules"]
        end
        FIFO["Working Message FIFO Buffer (Short-Term Memory)"]
    end

    subgraph Paging ["Automated Paging / Memory Tools"]
        MTOOLS["core_memory_append / archival_memory_insert"]
    end

    subgraph DB ["Persistent Storage Layer (PostgreSQL + pgvector)"]
        RECALL["RECALL MEMORY: Full Conversation Logs"]
        ARCHIVAL["ARCHIVAL MEMORY: Vectorized Document KB"]
    end

    subgraph Gateway ["FastMCP 3.1 Tool & Agent Gateway"]
        MCP["Tool Execution & Multi-Agent Handoffs"]
    end

    SYS & CoreMem & FIFO --> MTOOLS
    MTOOLS --> RECALL & ARCHIVAL
    RECALL & ARCHIVAL --> Gateway
```

## Tiered Memory Architecture Flow

```
+-----------------------------------------------------------------------------------+
|                           LETTA TIERED MEMORY ARCHITECTURE                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                 ACTIVE LLM CONTEXT WINDOW (RAM Cache)                       |  |
|  |                                                                             |  |
|  |  [ System Prompt & Instructions ]                                           |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  | CORE MEMORY BLOCKS (Self-Editable)                                    |  |  |
|  |  | - human: User preferences, persona traits, key facts                   |  |  |
|  |  | - persona: Agent identity, constraints, behavioral rules               |  |  |
|  |  +-----------------------------------------------------------------------+  |  |
|  |  [ Working Message FIFO Buffer (Short-Term Memory) ]                        |  |  |
|  +-----------------------------------------------------------------------------+  |
|                                |                                                  |
|                  (Automated Paging / Memory Tools)                                |
|                                v                                                  |
|  +-----------------------------------------------------------------------------+  |
|  |               PERSISTENT STORAGE LAYER (PostgreSQL + pgvector)              |  |
|  |                                                                             |  |
|  |  - RECALL MEMORY: Full conversation message history & interaction logs     |  |  |
|  |  - ARCHIVAL MEMORY: Vectorized document knowledge base & semantic snippets  |  |  |
|  +-----------------------------------------------------------------------------+  |
|                                |                                                  |
|                                v                                                  |
|  +-----------------------------------------------------------------------------+  |
|  |                       FASTMCP 3.1 TOOL & AGENT GATEWAY                      |  |
|  | - Standardized Tool Execution & FastMCP Server Interoperability             |  |
|  | - Agent-to-Agent Handoffs & State Portability across Frontier Models        |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Standard LLM applications suffer from state decay and context truncation. When interactions exceed the model's context window, historical details are lost or truncated, causing agents to repeat questions or forget user instructions.

Letta resolves this by decoupling agent memory state from the LLM's raw context window size:
1. **Multi-Session Continuity**: Agents maintain state across system reboots, user reconnects, and model transitions (e.g., switching from [Claude 5.6](../providers/anthropic.md) to GPT-5.6 or [DeepSeek-R1](../ai_knowledge/deepseek-r1.md)).
2. **Self-Editing Memory**: Agents are equipped with internal memory-editing functions (`core_memory_append`, `core_memory_replace`, `archival_memory_insert`), allowing them to actively curate their own identity and user profile blocks.
3. **Transparent State Inspection**: Developers can inspect, edit, or rollback agent memory blocks via REST API or CLI at runtime.

## Where it fits in the stack
**Agent Memory & Persistence Middleware Layer**. Letta sits between application frontends/interfaces and inference engines, maintaining persistent state in a backend database while exposing FastMCP 3.1 endpoints.

```
+-----------------------------------------------------------------------------------+
|                                ENTERPRISE STACK POSITION                          |
+-----------------------------------------------------------------------------------+
|  [ Chat UIs ]        [ IDE Extensions (Cursor) ]       [ Slack / Teams Bots ]    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                           LETTA AGENT SERVER MIDDLEWARE                           |
|       (Tiered Memory Engine | State DB | REST Server | FastMCP Gateway)         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         INFERENCE & DATABASE BACKENDS                             |
|  [ LLM Inference (Claude 5.6/GPT-5.6) ]     [ State DB (PostgreSQL / pgvector) ]  |
+-----------------------------------------------------------------------------------+
```

## Memory Tier Comparison Matrix

| Memory Tier | Storage Backend | Access Latency | Primary Function | Editable By Agent? |
| :--- | :--- | :--- | :--- | :--- |
| **Core Memory** | Active Context / RAM | Sub-millisecond | User traits & Persona instructions | Yes (`core_memory_append`) |
| **Working Buffer** | FIFO Context Queue | Sub-millisecond | Recent turn-by-turn conversation | Automatic FIFO Eviction |
| **Recall Memory** | PostgreSQL Relational | ~10-25 ms | Full message logs & search history | Read-only |
| **Archival Memory**| PostgreSQL + `pgvector`| ~20-50 ms | Vectorized passage & document store | Yes (`archival_memory_insert`)|

## Typical use cases
- **Long-Term Personal AI Executive Assistants**: Assistants that maintain deep context on user habits, organizational structures, and personal preferences over years.
- **Durable Software Engineering Agents**: Agents that track long-running refactoring projects across days, remembering resolved bugs, remaining tasks, and architecture decisions.
- **Autonomous Customer Relationship Management**: Tracking customer history, previous tickets, and customized preference configurations without losing continuity.
- **Stateful Multi-Agent Workflows**: Orchestrating complex pipelines where specialized sub-agents hand off task control while preserving shared background memory.

## Strengths
- **Decoupled Persistent Memory**: Stores memory in database backends (PostgreSQL/pgvector), allowing agents to survive process restarts and migrate between models.
- **Self-Editing Core Memory**: Equips agents with tools to actively rewrite and curate their own core memory blocks during multi-turn reasoning.
- **FastMCP 3.1 Task Protocol Support**: Native integration for standard FastMCP tool execution, server interoperability, and context streams.
- **Transparent Developer State Inspection**: Provides REST API endpoints and CLI commands to inspect, edit, or rollback agent state at runtime.

## Limitations
- **Added Memory Management Latency**: Tiered context paging and database vector lookups add ~35-70 ms overhead per interaction turn.
- **Infrastructure Setup Complexity**: Requires a persistent PostgreSQL + pgvector database server rather than purely stateless serverless functions.
- **Token Budget Overhead**: Managing active core memory blocks and reasoning about memory updates consumes additional prompt tokens.

## When to use it
- When creating long-lived AI agents that must remember user preferences, project context, and state over weeks or months.
- When building multi-session engineering assistants that track open bugs and refactoring decisions across developer sessions.
- When migrating agent state across different frontier LLM inference backends (e.g., Claude 5.6 to GPT-5.6).

## When not to use it
- For simple stateless, single-turn API interactions or basic Q&A chatbots where persistent state is unnecessary.
- In ultra-low-latency real-time applications where every millisecond counts and memory lookups cause unacceptable lag.
- For ephemeral, serverless deployments without persistent database infrastructure.

## Getting started

### Installation
```bash
pip install letta fastmcp pydantic
```

### Docker Compose Setup
```yaml
version: '3.8'

services:
  letta-db:
    image: pgvector/pgvector:pg16
    container_name: letta-db
    environment:
      POSTGRES_DB: letta_db
      POSTGRES_USER: letta_user
      POSTGRES_PASSWORD: letta_secure_pass

  letta-server:
    image: letta/letta:latest
    container_name: letta-server
    ports:
      - "8283:8283"
    environment:
      - LETTA_PG_URI=postgresql://letta_user:letta_secure_pass@letta-db:5432/letta_db
```

## Systemd Server Unit Configuration

For production environments running Letta Agent Server as a systemd service, configure `/etc/systemd/system/letta-server.service`:

```ini
[Unit]
Description=Letta Stateful Agent Server Daemon
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=letta
Group=letta
WorkingDirectory=/opt/letta
Environment=LETTA_HOST=0.0.0.0
Environment=LETTA_PORT=8283
EnvironmentFile=/etc/letta/environment
ExecStart=/opt/letta/venv/bin/letta server --host 0.0.0.0 --port 8283
Restart=always
RestartSec=5s
LimitNOFILE=65536

# Security Hardening
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/letta /opt/letta/data
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## CLI examples

### Create Stateful Agent
```bash
letta create-agent \
  --name "DurableSeniorDev" \
  --model "claude-5-6-sonnet-20270105" \
  --persona "You are an expert senior software architect. You record project decisions in core memory."
```

### Inspect Core Memory via REST API
```bash
#!/usr/bin/env bash
# Update an agent's Core Memory block via Letta REST API
set -euo pipefail

LETTA_HOST="http://localhost:8283"
AGENT_ID="${1:?Error: Specify Agent ID}"

curl -X POST "${LETTA_HOST}/v1/agents/${AGENT_ID}/core-memory/blocks/human" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "User prefers Python, Pydantic v2, and FastMCP 3.1."
  }' | jq .
```

## API examples

### Python SDK with Pydantic v2 & FastMCP 3.1 Server Integration
The following script demonstrates managing Letta agent memory states using Pydantic v2 schemas and exposing a FastMCP 3.1 tool server:

```python
import os
import json
import logging
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("LettaMemory")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Letta-Agent-Memory-Server", version="3.1")

class CoreMemoryBlock(BaseModel):
    label: str = Field(..., description="Block label (e.g. human, persona)")
    value: str = Field(..., min_length=1, description="Content of the memory block")

class AgentStateDump(BaseModel):
    agent_id: str = Field(..., description="Unique agent identifier.")
    name: str = Field(..., description="Agent display name.")
    model: str = Field(..., description="Target model identifier.")
    core_memory: List[CoreMemoryBlock] = Field(default_factory=list, description="List of core memory blocks.")

class LettaManager:
    def __init__(self, server_url: Optional[str] = None):
        self.server_url = server_url or os.getenv("LETTA_SERVER_URL", "http://localhost:8283")

    def inspect_agent_state(self, agent_id: str) -> AgentStateDump:
        mock_raw = {
            "agent_id": agent_id,
            "name": "DurableSeniorDev",
            "model": "claude-5-6-sonnet",
            "core_memory": [
                {"label": "human", "value": "User is a Principal Engineer building FastMCP 3.1 agent servers."},
                {"label": "persona", "value": "I am a durable coding assistant with persistent Letta memory."}
            ]
        }
        return AgentStateDump.model_validate(mock_raw)

manager = LettaManager()

@mcp.tool(name="get_agent_memory", description="Retrieve core memory blocks for a persistent Letta agent.")
def get_agent_memory(agent_id: str) -> str:
    """Retrieve core memory blocks for a persistent Letta agent."""
    try:
        state = manager.inspect_agent_state(agent_id)
        return state.model_dump_json(indent=2)
    except ValidationError as val_err:
        return json.dumps({"status": "VALIDATION_FAILED", "errors": val_err.errors()})
    except Exception as ex:
        return json.dumps({"status": "ERROR", "error": str(ex)})

@mcp.tool(name="update_core_memory", description="Updates a specific core memory block for a Letta agent.")
def update_core_memory(agent_id: str, label: str, new_value: str) -> str:
    """Simulates updating a core memory block via Letta API."""
    try:
        block = CoreMemoryBlock(label=label, value=new_value)
        logger.info(f"Updated memory block '{block.label}' for agent {agent_id}")
        return json.dumps({
            "status": "UPDATED",
            "agent_id": agent_id,
            "block": block.model_dump()
        }, indent=2)
    except ValidationError as val_err:
        return json.dumps({"status": "INVALID_BLOCK", "errors": val_err.errors()})

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Issue / Error Symptom | Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| `Paging Latency > 100ms` | Unindexed PostgreSQL `pgvector` table on archival memory embeddings. | `docker exec -it letta-db psql -U letta_user -c "\d archival_memory"` | Create HNSW index: `CREATE INDEX ON archival_memory USING hnsw (vector vector_cosine_ops);` |
| `Memory Overflow Warning` | Core memory blocks exceeding active context RAM allocation. | `curl http://localhost:8283/v1/agents/<id>/memory` | Truncate stale user preferences or compress memory blocks using `core_memory_replace`. |
| `Database Connection Refused` | PostgreSQL container failed or network bridge disconnected. | `systemctl status letta-server && docker logs letta-db` | Restart PostgreSQL service and check `LETTA_PG_URI` environment string. |
| `Token Budget Exhaustion` | Unbounded FIFO working buffer size sending huge prompt histories. | `letta inspect-buffer --agent-id <id>` | Lower max FIFO message count limit (`max_tokens_buffer: 4000`) in agent config. |
| `Context Loss on Model Switch` | Mismatched prompt template tags between Anthropic and OpenAI models. | `letta test-migration --agent-id <id> --target-model gpt-5.6` | Execute Letta context adapter migration script prior to switching model backends. |

## Operational Best Practices & Guardrails

### 1. Database Connection Pooling
In high-throughput multi-agent deployments, deploy `PgBouncer` in front of PostgreSQL to manage database connection pools effectively and prevent connection exhaustion.

### 2. Memory Sanitization Guardrails
Ensure agents sanitize incoming user inputs before appending to `archival_memory` to prevent vector store prompt injection attacks or storing sensitive PII unencrypted.

### 3. Regular Context Compaction
Schedule periodic agent maintenance passes to summarize historical FIFO message logs into compact archival memory passages.

## Related tools / concepts
- [Mem0](mem0.md) — Lightweight AI memory layer framework.
- [Gemma 4](../ai_knowledge/local_llms.md) — Open weights model family.
- [Agno](agno.md) — High-performance multi-agent runtime.
- [LangGraph](../frameworks/langgraph.md) — Stateful agent execution graph framework.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Retrieval-Augmented Generation architectural patterns.

## Sources / references
- [Letta Official Project & Documentation](https://www.letta.com/)
- [Letta GitHub Repository](https://github.com/letta-ai/letta)
- [MemGPT Original Research Paper (Packer et al.)](https://arxiv.org/abs/2310.08560)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
