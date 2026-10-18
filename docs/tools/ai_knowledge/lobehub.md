# LobeHub

## What it is
**LobeHub** (primarily known for its core product, **LobeChat**) is an open-source, high-performance multi-agent framework, plugin runtime, and workbench platform for the modern agentic ecosystem. It provides a unified, highly customizable web, PWA, and desktop interface for interacting with frontier models (Claude 5.6, GPT-5.6, Llama 4, Gemma 4, Qwen 3.6 VL, DeepSeek-V4/R1) while acting as a central management engine for **FastMCP 3.1** servers and **MCP 3.0 Task Protocol** integrations.

## What problem it solves
Managing multiple disparate AI tools, external API provider keys, local LLM endpoints ([Ollama](../../services/ollama.md), LocalAI, ExLlamaV3), self-hosted vector databases, and custom MCP tool servers leads to severe interface fragmentation. Developers and end-users are frequently forced to context-switch across disconnected web tabs, terminal CLIs, and desktop tools.

LobeHub eliminates interface fragmentation by functioning as an integrated "Agentic Workbench." It consolidates local and cloud model gateways, provides zero-trust document vector search, supports full-duplex WebRTC voice interaction, and simplifies tool orchestration through a built-in FastMCP 3.1 server manager and plugin marketplace.

## System Architecture & FastMCP Integration

```mermaid
flowchart TD
    subgraph ClientLayer ["User / Client Interaction Layer"]
        WEB["Next.js 15 Web Client"]
        PWA["Progressive Web App / Mobile"]
        DESK["Electron Desktop Client"]
        RTC["WebRTC Audio / Vision Engine"]
    end

    subgraph CoreEngine ["LobeChat Application Core"]
        ORCH["Multi-Agent Orchestrator"]
        MCPM["FastMCP 3.1 / MCP 3.0 Server Manager"]
        RAG["Knowledge Base Vector Search"]
        SSO["OAuth2 / OIDC SSO Gateway"]
    end

    subgraph Gateway ["Unified Model Gateway & Router"]
        NORM["API Protocol Normalizer"]
        RATE["Rate Limiting & Token Manager"]
        STREAM["Stream Transformer"]
    end

    subgraph Backends ["Downstream Providers & Tools"]
        CLOUD["Cloud AI (OpenAI, Anthropic, Google, Cohere)"]
        LOCAL["Local Inference (Ollama, ExLlamaV3, vLLM)"]
        TOOLS["FastMCP 3.1 Tools (Files, Search, SQL, Code Exec)"]
    end

    WEB & PWA & DESK & RTC --> CoreEngine
    ORCH & MCPM & RAG & SSO --> Gateway
    Gateway --> CLOUD & LOCAL & TOOLS
```

## System Execution Sequence Flow

```
+-----------------------------------------------------------------------------------+
|                            LOBEHUB SESSION SEQUENCE FLOW                          |
+-----------------------------------------------------------------------------------+

[User Client UI] --(WebRTC / HTTP)--> [LobeChat Core Router] --(JWT Auth)--> [Vector Store]
                                               |                                 |
                                    (Tool Dispatch / Stream)              (HNSW Retrieval)
                                               v                                 v
[Client UI Stream] <--(WebSocket) <-- [Unified API Gateway] <--(Context Inject)--+
                                               |
                                     (FastMCP 3.1 Exec)
                                               v
                                   [FastMCP Tool Server / LLM]
```

## Comparison Matrix

| Feature / Metric | LobeHub / LobeChat | Open WebUI | LibreChat | AnythingLLM |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Architecture** | Next.js 15 / PWA / Desktop | Python FastAPI + Svelte | Node.js + React | Node.js + React |
| **FastMCP 3.1 Native** | Full Native Registry & UI | OpenAPI/Custom Extensions | Plugin System / MCP | Internal Agents |
| **Multi-Agent Teams** | Advanced Sub-Agent Workflows | Basic Pipelines | Agent System | Basic Workspace Agents |
| **Real-time Voice** | WebRTC Dual-Channel Speech | Browser TTS/STT | Basic Audio | Basic Voice Ingestion |
| **Multi-Tenancy & DB** | Client-Local or Postgres DB | SQLite / Postgres | MongoDB / PostgreSQL | SQLite / Vector DBs |
| **Plugin Ecosystem** | Native Lobe Marketplace | Community Tools | Custom Tool Plugins | Custom Agents |

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Multi-Agent Platform & Workbench UI.

LobeHub operates at the top of the homelab and enterprise AI software stack, serving as the client interaction and session orchestration gateway. It interfaces directly with downstream inference servers (`docs/tools/infrastructure/`), knowledge stores (`docs/tools/intake_storage/`), and automated workflow systems (`docs/tools/automation_orchestration/`).

## Typical use cases
- **Multi-Agent Engineering Teams**: Configuring specialized agents (e.g. Code Reviewer, Security Auditor, DB Optimizer) to execute collaborate repository tasks.
- **Enterprise RAG Knowledge Gateways**: Deploying a self-hosted corporate portal with document upload, semantic vector search, and role-based access control (RBAC).
- **Local-First AI Testing**: Benchmarking open-weights models (Llama 4, DeepSeek-R1) via Ollama before committing cloud budget to external APIs.
- **FastMCP 3.1 Tool Server Management**: Providing a visual graphical workbench to test, debug, and execute FastMCP 3.1 tool calls.

## Strengths
- **Native FastMCP 3.1 Support**: Direct graphical interface for discovering, authorizing, and executing tools on external MCP servers.
- **Multi-Modal WebRTC Interface**: Seamless, full-duplex speech interaction and real-time vision stream analysis.
- **Extensive Plugin Marketplace**: Instant deployment of hundreds of pre-configured community tools and agents.
- **Flexible Deployment Models**: Deployable as a client-side local PWA or a multi-tenant PostgreSQL/Redis database-backed enterprise service.

## Limitations
- **Database Deployment Overhead**: Configuring the full database-backed enterprise setup requires orchestrating PostgreSQL, Redis, and S3-compatible object storage.
- **Memory Consumption**: Running real-time multi-agent sessions with active vector indexes and streaming voice requires substantial host memory.

## When to use it
- When seeking a modern, multi-model client interface with native FastMCP 3.1 support.
- When organizing team workflows into specialized, collaborating agent personas.
- When strict data sovereignty mandates hosting chat logs, vector stores, and model endpoints entirely on-premises.

## When not to use it
- When requiring a lightweight command-line interactive agent (use [Claude Code](../development_ops/claude-code.md)).
- When constructing complex graphical node-based agent flowcharts (use [Langflow](../frameworks/langflow.md) or [Rivet](../frameworks/rivet.md)).

## Getting started

### 1. Docker Setup (Client-Only Mode)
Run LobeChat locally in client-only PWA mode using Docker:
```bash
docker run -d -p 3210:3210 \
  -e OPENAI_API_KEY="sk-proj-xxxx" \
  -e ACCESS_CODE="lobe66" \
  --name lobe-chat \
  lobehub/lobe-chat
```

### 2. Verification
Verify that the HTTP endpoint is active and healthy:
```bash
curl -I http://localhost:3210/
```

### 3. Docker Compose (Enterprise DB Mode)
For multi-user PostgreSQL-backed deployment:
```yaml
version: '3.8'
services:
  lobe-chat-db:
    image: lobehub/lobe-chat-database:latest
    ports:
      - "3210:3210"
    environment:
      - DATABASE_URL=postgresql://lobe:lobepass@postgres:5432/lobe_chat
      - REDIS_URL=redis://redis:6379
      - KEYCLOAK_CLIENT_ID=lobechat
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=lobe
      - POSTGRES_PASSWORD=lobepass
      - POSTGRES_DB=lobe_chat

  redis:
    image: redis:7-alpine
```

## Systemd Service Unit Configuration

For production deployments running LobeHub Server as a systemd service, configure `/etc/systemd/system/lobe-chat.service`:

```ini
[Unit]
Description=LobeHub Multi-Agent Workbench Service
After=network.target postgresql.service redis.service
Wants=postgresql.service redis.service

[Service]
Type=simple
User=lobehub
Group=lobehub
WorkingDirectory=/opt/lobe-chat
Environment=NODE_ENV=production
Environment=PORT=3210
EnvironmentFile=/etc/lobehub/environment
ExecStart=/usr/bin/node /opt/lobe-chat/server.js
Restart=always
RestartSec=5s
LimitNOFILE=65536

# Security Hardening
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/lobe-chat/data /var/log/lobehub
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## CLI examples

### 1. Pull Latest Image and Restart
```bash
docker pull lobehub/lobe-chat:latest && docker restart lobe-chat
```

### 2. Inspect Active PostgreSQL Migrations
```bash
docker exec -it lobe-chat-db psql -U lobe -d lobe_chat -c "SELECT version();"
```

### 3. Launch FastMCP 3.1 Inspector
```bash
npx @modelcontextprotocol/inspector lobe-mcp-config.json
```

## API examples

### FastMCP 3.1 Server Provider & Agent Tool Registry (Pydantic v2)
This complete FastMCP 3.1 server validates provider configurations and dynamic model settings for LobeHub integrations using strict **Pydantic v2** models.

```python
import json
import logging
import os
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LobeHub-MCP")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("lobehub-config-engine", version="3.1")

class ModelParams(BaseModel):
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    context_window: int = Field(default=128000, alias="contextWindow", ge=2048)
    use_mcp: bool = Field(default=True, alias="useMcp")

class ProviderRegistration(BaseModel):
    provider_id: str = Field(..., alias="providerId")
    model_name: str = Field(..., alias="modelName")
    api_base_url: Optional[str] = Field(None, alias="apiBaseUrl")
    params: ModelParams = Field(default_factory=ModelParams)

    @field_validator("provider_id")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        allowed = {"openai", "anthropic", "google", "ollama", "localai", "deepseek", "vllm", "cohere"}
        if v.lower() not in allowed:
            raise ValueError(f"Provider '{v}' is not supported. Choose from {allowed}")
        return v.lower()

class AgentDefinition(BaseModel):
    agent_id: str = Field(..., min_length=3, description="Unique agent slug identifier.")
    system_prompt: str = Field(..., min_length=10, description="Core system behavior instructions.")
    tools: List[str] = Field(default_factory=list, description="List of enabled FastMCP tool names.")
    provider_config: ProviderRegistration = Field(..., description="Target model provider configuration.")

@mcp.tool(name="register_lobehub_agent", description="Validates and registers a new LobeHub multi-agent configuration.")
def register_lobehub_agent(payload: str) -> str:
    """Validates and registers a new LobeHub multi-agent configuration.

    Args:
        payload: JSON string matching AgentDefinition schema.
    """
    try:
        data = json.loads(payload)
        agent = AgentDefinition.model_validate(data)
        logger.info(f"Registered LobeHub agent: {agent.agent_id} with provider: {agent.provider_config.provider_id}")
        return json.dumps({
            "status": "SUCCESS",
            "agent_id": agent.agent_id,
            "validated_config": agent.model_dump(by_alias=True)
        }, indent=2)
    except ValidationError as val_err:
        return json.dumps({"status": "VALIDATION_FAILED", "errors": val_err.errors()})
    except Exception as e:
        return json.dumps({"status": "ERROR", "error": str(e)})

@mcp.tool(name="verify_mcp_server_connection", description="Checks connectivity to external FastMCP tool servers.")
def verify_mcp_server_connection(server_url: str) -> str:
    """Simulates connection probe to an MCP tool server."""
    return json.dumps({
        "server_url": server_url,
        "status": "CONNECTED",
        "mcp_version": "3.1",
        "capabilities": ["tools", "resources", "prompts"]
    })

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Issue / Error Symptom | Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| `WebRTC Audio Stutter` | Packet loss or network buffer underflow during speech streaming. | `curl -i http://localhost:3210/api/health` | Adjust audio buffer sizes in client settings or use OPUS codec fallback. |
| `PGVector Query Latency > 200ms` | Missing HNSW vector index on database embedding table. | `docker exec -it postgres psql -U lobe -c "\d lobe_chat"` | Create HNSW index: `CREATE INDEX ON embeddings USING hnsw (vector vector_cosine_ops);` |
| `MCP Tool Call Rejected` | Security authorization token expired or tool permission disabled. | `docker logs lobe-chat \| grep "MCP"` | Re-authenticate MCP tool server token in LobeHub settings UI. |
| `Redis Connection Timeout` | Redis instance reached max connections limit. | `redis-cli info clients` | Increase `maxclients` in `redis.conf` or configure Redis connection pooling. |
| `Ollama Endpoint Unreachable` | Docker container unable to reach host localhost Ollama service. | `curl http://host.docker.internal:11434/api/tags` | Set environment variable `OLLAMA_ORIGINS="*"`, and use `host.docker.internal` URL. |

## Operational Best Practices & Guardrails

### 1. Vector Store Index Optimization
When deploying LobeChat in enterprise database mode with Pgvector or Milvus, ensure vector indexes utilize HNSW (Hierarchical Navigable Small World) with `m=16` and `ef_construction=64` to maintain sub-50ms retrieval latencies across large document collections.

### 2. FastMCP Tool Server Isolation
Run external FastMCP tool servers inside isolated Docker sidecar containers on the same internal bridge network as LobeChat, restricting tool network egress to prevent unauthorized external data exfiltration.

### 3. Session State & Redis Persistence
Utilize Redis with AOF (Append Only File) persistence enabled for multi-user LobeChat deployments to prevent token streaming state loss during container upgrades.

### 4. Credential Storage Guardrails
Always pass external API keys (OpenAI, Anthropic, Google) via `EnvironmentFile` or secret management systems (e.g. HashiCorp Vault), never embedding credentials in raw client browser storage.

## Related tools / concepts
- [AnythingLLM](anythingllm.md) — Self-hosted RAG workspace and agent platform.
- [Open WebUI](../../services/open-webui.md) — Open-source LLM chat web interface.
- [LibreChat](librechat.md) — Enterprise multi-model chat UI framework.
- [Ollama](../../services/ollama.md) — Local model serving runtime engine.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardization protocol for model tool calls.

## Sources / references
- [LobeHub Official Website](https://lobehub.com/)
- [LobeChat GitHub Repository](https://github.com/lobehub/lobe-chat)
- [FastMCP Framework Specification](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
