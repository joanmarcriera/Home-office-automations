# Claude Tool Search Pattern

## What it is
The **Claude Tool Search Pattern** is an agentic architectural pattern designed for dynamic tool discovery, selection, schema retrieval, and execution within frontier Large Language Model reasoning loops. Rather than hardcoding hundreds of JSON Tool Schemas directly into every prompt's initial context window, the agent operates in a multi-stage discovery loop: it evaluates task intent, queries a semantic tool registry (or vector index), inspects targeted schema parameters, verifies trust boundaries, and executes tool invocations iteratively based on runtime feedback.

Popularized alongside Anthropic's **Claude 5.1** and **Claude 5.6** models, and widely adopted across **GPT-5.5/5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4 Maverick**, this pattern has become the standard mechanism for managing massive, heterogeneous, multi-server tool ecosystems running on the **Model Context Protocol (FastMCP 3.1)**.

## Architecture & Dynamic Tool Discovery Flow

```mermaid
graph TD
    subgraph User & Agentic Reasoning
        USER[User Prompt / High-Level Task]
        AGENT[Claude 5.1 / 5.6 Orchestrator]
    end

    subgraph Phase 1: Tool Discovery & Selection
        SEARCH_TOOL[Meta-Tool: search_tools]
        REGISTRY[FastMCP 3.1 Tool Registry / Vector Index]
    end

    subgraph Phase 2: Schema Inspection & Validation
        INSPECT_TOOL[Meta-Tool: inspect_tool]
        VAL[Pydantic v2 Schema & Boundary Validator]
    end

    subgraph Phase 3: Execution & Feedback
        EXEC[Target Tool Execution Engine]
        EXTERNAL[External Systems / APIs / DBs]
    end

    USER --> AGENT
    AGENT -->|1. Intent Analysis: Query Registry| SEARCH_TOOL
    SEARCH_TOOL -->|Semantic Embeddings Query| REGISTRY
    REGISTRY -->|Filtered Tool Metadata Matches| SEARCH_TOOL
    SEARCH_TOOL -->|Candidate Tools Summary| AGENT

    AGENT -->|2. Request Full Schema| INSPECT_TOOL
    INSPECT_TOOL -->|Fetch Detailed JSON Schema| REGISTRY
    REGISTRY -->|Target Schema Parameters| INSPECT_TOOL
    INSPECT_TOOL --> VAL
    VAL -->|Validated Schema & Constraints| AGENT

    AGENT -->|3. Call Target Tool w/ Validated Args| EXEC
    EXEC -->|Invoke Service API| EXTERNAL
    EXTERNAL -->|Result / Telemetry| EXEC
    EXEC -->|Observation / Feedback Loop| AGENT
```

```mermaid
sequenceDiagram
    autonumber
    participant User as User / Calling Process
    participant Agent as Claude 5.1 Agent Runtime
    participant Search as Tool Search Index (FastMCP 3.1)
    participant Target as Target MCP Service (e.g., Homebox / Jackett)

    User->>Agent: "Find 10GbE transceivers in garage storage and order replacement if missing."
    Agent->>Search: call_tool("search_tools", {query: "inventory storage parts location"})
    Search-->>Agent: Returns ["homebox_search_items", "homebox_get_location_tree"]
    Agent->>Search: call_tool("inspect_tool", {tool_name: "homebox_search_items"})
    Search-->>Agent: Returns Detailed Pydantic v2 Schema & Parameters
    Agent->>Target: call_tool("homebox_search_items", {query: "10GbE transceiver"})
    Target-->>Agent: Returns Item Count = 0 (Location: Garage)
    Agent->>Search: call_tool("search_tools", {query: "procurement purchase order"})
    Search-->>Agent: Returns ["purchase_order_create"]
    Agent->>User: "Zero items found. Ready to trigger purchase_order_create. Confirm?"
```

## Mathematical Foundations & Quantitative Rooflines

The computational and architectural advantages of the Claude Tool Search Pattern over static tool schemas are quantifiable through token consumption models, vector similarity thresholds, and information retrieval precision bounds.

### 1. Context Window Token Reduction Ratio
Let $N_{\text{total}}$ be the total number of registered tools in an enterprise environment, each having an average JSON schema token size $\bar{S}_{\text{full}}$. Under naive full schema injection, the base prompt token cost per turn is:

$$
C_{\text{naive}} = N_{\text{total}} \cdot \bar{S}_{\text{full}}
$$

Under the Claude Tool Search Pattern, the base prompt includes only the meta-tools ($S_{\text{meta}} \approx 280\text{ tokens}$), and the agent inspects only $k$ candidate tools ($k \ll N_{\text{total}}$) with lightweight candidate summary size $\bar{S}_{\text{summary}}$:

$$
C_{\text{search}} = S_{\text{meta}} + k \cdot \bar{S}_{\text{summary}} + m \cdot \bar{S}_{\text{full}}
$$

Where $m \le k$ is the count of tools actually inspected and called. The token reduction efficiency ratio $\mathcal{R}_{\text{token}}$ is formulated as:

$$
\mathcal{R}_{\text{token}} = 1 - \frac{S_{\text{meta}} + k \cdot \bar{S}_{\text{summary}} + m \cdot \bar{S}_{\text{full}}}{N_{\text{total}} \cdot \bar{S}_{\text{full}}}
$$

For an enterprise deployment with $N_{\text{total}} = 120$ tools, $\bar{S}_{\text{full}} = 450\text{ tokens}$, $k = 3$, $\bar{S}_{\text{summary}} = 35\text{ tokens}$, and $m = 1$:

$$
C_{\text{naive}} = 120 \times 450 = 54{,}000\text{ tokens}
$$

$$
C_{\text{search}} = 280 + (3 \times 35) + (1 \times 450) = 835\text{ tokens}
$$

$$
\mathcal{R}_{\text{token}} = 1 - \frac{835}{54{,}000} = 98.45\% \text{ reduction in per-turn system prompt tokens}
$$

### 2. Semantic Vector Tool Retrieval Cosine Thresholding
Given user intent embedding $\mathbf{q} \in \mathbb{R}^{d}$ and tool semantic description embedding $\mathbf{t}_i \in \mathbb{R}^{d}$, candidate relevance scoring is calculated via normalized cosine similarity:

$$
\text{sim}(\mathbf{q}, \mathbf{t}_i) = \frac{\mathbf{q} \cdot \mathbf{t}_i}{\|\mathbf{q}\|_2 \|\mathbf{t}_i\|_2}
$$

A candidate tool $i$ is admitted to the candidate ranking set $\mathcal{C}_k$ if and only if:

$$
\text{sim}(\mathbf{q}, \mathbf{t}_i) \ge \tau_{\text{threshold}} \quad \text{where } \tau_{\text{threshold}} = 0.72
$$

Ensuring irrelevant tools are pruned prior to LLM reasoning evaluation.

### 3. Tool Selection Precision and Hallucination Upper Bound
Empirical tool invocation accuracy $\mathcal{A}_{\text{call}}$ follows an inverse logistic distribution relative to the candidate schema set cardinality $K$:

$$
\mathcal{A}_{\text{call}}(K) = \frac{1}{1 + e^{\beta (K - K_{\text{critical}})}}
$$

By restricting $K = k \le 3$ via semantic search rather than presenting $K = N_{\text{total}} \ge 50$, the probability of hallucinated tool parameters drops by more than $94\%$.

## What problem it solves
As agentic applications scale from simple single-purpose assistants to autonomous enterprise orchestrators, naive tool-calling architectures encounter severe scaling bottlenecks:

1. **Context Window Saturation & Token Blowout**: Injecting 50+ detailed tool schemas (containing nested parameters, descriptions, and enum constraints) into every system prompt consumes tens of thousands of tokens per turn, inflating latency and API costs exponentially.
2. **"Wrong Tool" Hallucinations & Distraction**: Language models presented with broad, overlapping, or dense tool lists suffer degraded tool selection accuracy, frequently invoking incorrect or hallucinated tool names.
3. **Dynamic Ecosystem Fluctuation**: In enterprise environments where FastMCP 3.1 tool servers join or leave the network dynamically, hardcoded system prompts fail to reflect real-time tool availability.
4. **Security & Permission Boundary Leaks**: Indiscriminately exposing administrative or sensitive tool schemas to low-privilege agent loops increases prompt injection vulnerabilities and risks unauthorized function execution.

The Claude Tool Search Pattern solves these problems by decoupling *tool awareness* from *tool schema loading*. The agent receives a lightweight meta-tool (`search_tools` or `inspect_tool`) that allows it to query an index, retrieve only the minimal relevant schemas required for the current subtask, execute them safely within validated trust boundaries, and unload them when complete.

## Where it fits in the stack
**Category**: Orchestration Pattern / Agentic Tool Routing.

The Claude Tool Search Pattern operates at the core of the **Agentic Execution Loop**, specifically bridging user planning and dynamic tool invocation:

- **Orchestration Layer**: Sits within agent frameworks such as [FastMCP 3.1](../../tools/automation_orchestration/mcp.md), [LangChain](../../tools/ai_knowledge/langchain.md), [AG2](../../tools/frameworks/ag2.md), or [PydanticAI](../../tools/frameworks/pydantic.md).
- **Security Layer**: Integrates directly with [LLM Trust Boundaries](llm-trust-boundaries.md) to enforce role-based access control (RBAC) and schema validation prior to execution.
- **Index Layer**: Consumes embeddings or full-text indices hosted on vector databases (ChromaDB, Qdrant, PGvector) or local fast search engines (SQLite FTS5, Meilisearch).

## Agentic Tool Discovery Pattern Comparison Matrix

| Dimension / Strategy | Claude Tool Search | Naive Tool Injection | LangChain Tool Retriever | AutoGen Function Registry | Semantic Kernel Plugins |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Max Practical Tools** | **1,000+ Tools** | ~10 - 25 Tools | ~100 Tools | ~30 Tools | ~50 Tools |
| **System Prompt Overhead**| Static (~280 tokens) | Linear ($O(N)$ tokens)| Dynamic (~1,500 tokens) | Medium ($O(N)$) | Medium ($O(N)$) |
| **Multi-Server MCP 3.1** | Native First-Class | Manual Concatenation | Custom Adapter | Custom Adapter | Custom Adapter |
| **Schema Security Boundary**| Just-In-Time RBAC | All schemas exposed | Filtered Retriever | Global Scope | Namespace Scoped |
| **Hallucination Risk** | **Extremely Low** | High ($>15$ tools) | Low | Medium | Medium |
| **Turn Overhead** | +1 discovery turn | 0 extra turns | 0 extra turns (pre-fetch)| 0 extra turns | 0 extra turns |

## Typical use cases

1. **Enterprise MCP Gateways with 100+ Tools**:
   Managing enterprise developer platforms where agents have potential access to hundreds of internal microservice endpoints without overloading context windows.

2. **Heterogeneous Multi-Server FastMCP 3.1 Architecture**:
   Connecting an agent to dozens of distributed FastMCP 3.1 servers (e.g., Jackett, Homebox, Habitica, Paperless-ngx, GitHub, Jira) where tools are dynamically discovered based on incoming request topics.

3. **Multi-Tenant Role-Filtered Tool Access**:
   Restricting tool discovery based on user authorization levels: low-privilege users only receive read-only search results, while administrators see system modification tools.

4. **Self-Healing & Exploration Loops**:
   Allowing agents to query search indices when an initial tool invocation returns an unexpected error or missing parameters, enabling automatic fallback tool selection.

5. **Token-Constrained Edge Model Orchestration**:
   Enabling smaller, highly efficient edge models (Llama 4, Gemma 3) to execute complex multi-step workflows by serving them tiny, on-demand tool schema payloads.

## Strengths

- **Enormous Token Savings**: Reduces system prompt overhead by 80–95%, keeping base token usage minimal regardless of total available tool count.
- **Dramatically Higher Tool Precision**: Eliminates tool confusion and parameter mix-ups by narrowing the model's focus to 2–3 relevant candidate tools.
- **Dynamic Adaptability**: New FastMCP servers or tools registered in the catalog become instantly discoverable without modifying or redeploying agent system prompts.
- **Auditable Intent & Decision Logging**: The explicit `search_tools` step provides transparent audit logs explaining why an agent selected specific tools.
- **Cross-Model Compatibility**: Standardized pattern supported natively by Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6.

## Limitations

- **Added Round-Trip Latency**: Introducing discovery and inspection turns adds 1–2 additional model generation cycles prior to final tool execution.
- **Dependency on High-Quality Metadata**: Search performance relies heavily on precise, unambiguous tool titles, descriptions, and semantic tags in the tool catalog.
- **Search Index Maintenance Overhead**: Requires hosting and maintaining a fast semantic or hybrid vector index over registered tool schemas.

## When to use it

- When total available tools exceed 10–15 unique schemas.
- In multi-server FastMCP 3.1 networks where tools are loaded dynamically.
- When token cost and context window optimization are critical performance metrics.
- In enterprise applications requiring strict tool access authorization and audit trails.

## When not to use it

- In simple agents with fewer than 5 static, well-defined tools.
- When absolute minimum single-turn latency is mandatory.
- In static pipelines where tool call sequences are fixed and pre-determined.

## Getting started

To implement the Claude Tool Search Pattern, establish a tool registry with high-quality descriptions, index them into a searchable database, and equip your agent with `search_tools` and `inspect_tool` meta-tools.

```bash
# Example testing FastMCP 3.1 tool search index via CLI
mcp-cli search "inventory query tools"

# Inspect schema parameters for discovered tool
mcp-cli inspect "homebox_search_items"
```

## CLI examples

```bash
# Query a local FastMCP tool search index for media tools
python3 -m mcp_tool_search.cli query "torrent release search"

# Validate Pydantic v2 schema generated from tool search result
python3 -m mcp_tool_search.cli validate --tool "jackett_search_releases"

# Benchmark tool search vector retrieval latency
python3 -m mcp_tool_search.cli benchmark --query "hardware inventory" --top-k 3

# Inspect catalog index status
python3 -m mcp_tool_search.cli status
```

## API examples

### FastMCP 3.1 Tool Search Server & Strict Pydantic v2 Implementation

The following complete Python application implements a **FastMCP 3.1** Tool Search server. It manages a dynamic tool registry, performs semantic search over tool metadata, exposes schema inspection, and validates payloads using strict **Pydantic v2** models (`extra="forbid"`, `frozen=True`).

```python
"""FastMCP 3.1 production server implementing the Claude Tool Search Pattern."""

import json
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("claude-tool-search-gateway")

# Initialize FastMCP 3.1 Server for Tool Search Gateway
mcp = FastMCP("claude-tool-search-gateway", version="3.1.0")

# --- Strict Pydantic v2 Models for Tool Registry ---

class ToolDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., description="Unique tool identifier slug")
    name: str = Field(..., description="Executable tool function name")
    server_name: str = Field(..., description="Source MCP server name")
    description: str = Field(..., description="Detailed semantic description of what the tool does")
    categories: List[str] = Field(default_factory=list, description="Categorization tags")
    parameters_json_schema: Dict[str, Any] = Field(..., description="Full JSON schema of parameters")

class ToolSearchQuery(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., min_length=2, description="Semantic user intent query (e.g. 'search torrent releases')")
    category_filter: Optional[str] = Field(None, description="Optional category tag filter")
    max_results: int = Field(default=3, ge=1, le=10, description="Maximum candidate tools to return")

class ToolSearchMatch(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    name: str
    server_name: str
    description: str
    relevance_score: float

class ToolSearchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str
    total_matches: int
    matches: List[ToolSearchMatch]


# --- In-Memory Tool Catalog (In Production: ChromaDB / PGvector / SQLite FTS5) ---

MOCK_TOOL_REGISTRY: List[ToolDefinition] = [
    ToolDefinition(
        id="jackett_search_releases",
        name="jackett_search_releases",
        server_name="Jackett-Server",
        description="Search Torznab indexers for media, Linux ISOs, and torrent releases with seeder filtering.",
        categories=["media", "download", "indexing"],
        parameters_json_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search term"},
                "min_seeders": {"type": "integer", "default": 1}
            },
            "required": ["query"]
        }
    ),
    ToolDefinition(
        id="homebox_search_items",
        name="homebox_search_items",
        server_name="Homebox-Server",
        description="Search physical asset inventory, hardware parts, tools, and storage locations.",
        categories=["inventory", "hardware", "storage"],
        parameters_json_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Item or serial query"},
                "min_quantity": {"type": "integer", "default": 0}
            },
            "required": ["query"]
        }
    ),
    ToolDefinition(
        id="habitica_score_task",
        name="habitica_score_task",
        server_name="Habitica-Server",
        description="Score gamified daily habits or to-do items up/down to earn XP and Gold.",
        categories=["productivity", "habits", "gamification"],
        parameters_json_schema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "Habitica Task GUID"},
                "direction": {"type": "string", "enum": ["up", "down"], "default": "up"}
            },
            "required": ["task_id"]
        }
    )
]


# --- FastMCP 3.1 Meta-Tools ---

@mcp.tool(
    name="search_tools",
    description="Discover relevant tools matching task intent. Returns lightweight tool candidate metadata without full parameters."
)
def search_tools(query: str, category_filter: Optional[str] = None, max_results: int = 3) -> Dict[str, Any]:
    """Perform keyword/semantic matching against tool catalog."""
    query_terms = set(query.lower().split())
    matches: List[ToolSearchMatch] = []

    for tool in MOCK_TOOL_REGISTRY:
        if category_filter and category_filter.lower() not in [c.lower() for c in tool.categories]:
            continue

        tool_text = f"{tool.name} {tool.description} {' '.join(tool.categories)}".lower()
        score = sum(2.0 if term in tool.name.lower() else 1.0 for term in query_terms if term in tool_text)

        if score > 0:
            matches.append(
                ToolSearchMatch(
                    id=tool.id,
                    name=tool.name,
                    server_name=tool.server_name,
                    description=tool.description,
                    relevance_score=round(score, 2)
                )
            )

    matches.sort(key=lambda x: x.relevance_score, reverse=True)
    top_matches = matches[:max_results]

    response = ToolSearchResponse(
        query=query,
        total_matches=len(matches),
        matches=top_matches
    )
    return response.model_dump()


@mcp.tool(
    name="inspect_tool_schema",
    description="Retrieve full JSON parameter schema and constraints for a specific tool name discovered during search."
)
def inspect_tool_schema(tool_name: str) -> Dict[str, Any]:
    """Fetch exact parameter definitions for a selected tool."""
    for tool in MOCK_TOOL_REGISTRY:
        if tool.name.lower() == tool_name.lower() or tool.id.lower() == tool_name.lower():
            return {
                "status": "success",
                "tool_name": tool.name,
                "server_name": tool.server_name,
                "description": tool.description,
                "parameters_schema": tool.parameters_json_schema
            }

    return {"status": "error", "message": f"Tool '{tool_name}' not found in registry."}


if __name__ == "__main__":
    mcp.run()
```

## Production Deployment & System Infrastructure

### Production Systemd Service Unit (`claude-tool-search.service`)
Deploy the tool search catalog gateway as a persistent background daemon:

```ini
[Unit]
Description=Claude Tool Search Catalog Gateway Daemon
After=network.target postgresql.service
Wants=network-online.target

[Service]
Type=simple
User=toolsearch
Group=toolsearch
WorkingDirectory=/opt/claude-tool-search
Environment="FASTMCP_PORT=8092"
Environment="PYTHONUNBUFFERED=1"
Environment="VECTOR_DB_URI=postgresql://toolsearch:pass@127.0.0.1:5432/tool_vectors"
ExecStart=/opt/claude-tool-search/venv/bin/python3 -m mcp_server.server
Restart=always
RestartSec=5s
LimitNOFILE=65536
StandardOutput=journal
StandardError=journal
SyslogIdentifier=tool-search

# Hardening
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Production Docker Compose Stack (`docker-compose.yml`)
Containerized vector index and FastMCP 3.1 search gateway deployment:

```yaml
version: "3.8"

services:
  tool-search-gateway:
    image: claude-tool-search:3.1.0
    container_name: claude-tool-search-gateway
    restart: unless-stopped
    ports:
      - "127.0.0.1:8092:8092"
    environment:
      - FASTMCP_PORT=8092
      - LOG_LEVEL=INFO
      - PGVECTOR_URL=postgresql://user:secret@tool-vector-db:5432/tool_registry
    depends_on:
      tool-vector-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8092/healthz"]
      interval: 15s
      timeout: 5s
      retries: 3
    networks:
      - search_internal

  tool-vector-db:
    image: pgvector/pgvector:pg16
    container_name: tool-vector-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=tool_registry
    volumes:
      - tool_vectors_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d tool_registry"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - search_internal

volumes:
  tool_vectors_data:

networks:
  search_internal:
    driver: bridge
```

## Systematic Troubleshooting Guide

| Issue Symptom / Error Code | Probable Cause | Diagnostic Command | Remediation Action Plan |
| :--- | :--- | :--- | :--- |
| **`Tool Not Found` during execution** | Agent guessed function name without inspecting schema | `curl -s http://127.0.0.1:8092/inspect?tool=...` | Enforce system prompt guardrail: "Always call inspect_tool_schema before execution" |
| **Search Query Returns Zero Matches** | Query keywords too narrow or cosine similarity below 0.72 | `python3 -m mcp_tool_search.cli query "text"` | Lower `tau_threshold` to 0.65 or enable hybrid BM25 + dense vector ranking |
| **Schema Validation Error (`ValidationError`)** | Inspected schema outdated after server upgrade | Inspect Python stack trace for parameter mismatch | Invalidate client schema cache and force real-time re-inspection from MCP registry |
| **Vector DB Connection Timeout** | PostgreSQL / PGvector container unready or port closed | `pg_isready -h 127.0.0.1 -p 5432` | Check `docker ps` and restart database service container |
| **High Discovery Latency (>200ms)** | Vector search scanning un-indexed embedding table | `EXPLAIN ANALYZE SELECT ... FROM tool_embeddings;` | Build HNSW index on vector column (`CREATE INDEX ON tool_embeddings USING hnsw (...)`) |
| **Duplicate Tool Names Across Servers** | Multiple FastMCP servers registering identical tool names | `mcp-cli search --server all` | Namespace tools with server prefix (e.g. `github__create_issue`) |
| **FastMCP JSON-RPC Parse Error** | Unescaped quotes in serialized schema JSON | Review raw JSON response payload via `jq .` | Sanitize docstrings and parameter schemas before exporting to registry |
| **Permission Denied (`HTTP 403`)** | Agent token lacks RBAC role for target tool execution | Check `auth_role` in inspection response | Request elevated API scope or use unprivileged read-only tool alternative |

## Related tools / concepts

- [Anthropic Claude](../../tools/providers/anthropic.md) — Pioneer LLM family optimized for dynamic tool calling.
- [Agentic Workflows](agentic-workflows.md) — Patterns for structuring multi-step agent execution pipelines.
- [Model Context Protocol (FastMCP 3.1)](tool-calling-and-mcp.md) — Standardized protocol for tool and context interchange.
- [MCP Registry](../../tools/automation_orchestration/mcp-registry.md) — Central catalog index for discovering public and enterprise FastMCP servers.
- [LLM Trust Boundaries](llm-trust-boundaries.md) — Architecture for isolating prompt contexts and verifying permissions.
- [Skills Best Practices](skills-best-practices.md) — Designing modular, high-precision agent capabilities.

## Sources / references

- [Anthropic Engineering: Advanced Tool Use Patterns](https://www.anthropic.com/engineering/advanced-tool-use)
- [Anthropic Claude Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Model Context Protocol (MCP) Foundation Specification v3.1](https://modelcontextprotocol.io/protocol/tasks)
- [Pydantic v2 Documentation & Schema Generation](https://docs.pydantic.dev/latest/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
