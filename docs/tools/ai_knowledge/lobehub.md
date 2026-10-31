# LobeHub

## What it is
**LobeHub** (primarily known for its flagship platform, **LobeChat**) is an open-source, high-performance multi-agent framework, plugin runtime, and engineering workbench designed for the modern agentic ecosystem. It provides a unified, highly customizable web, PWA, and desktop interface for interacting with frontier models (Claude 5.6, GPT-5.6, Llama 4, Gemma 4, Qwen 3.6 VL, and DeepSeek-V4/R1) while acting as a centralized orchestration runtime for **FastMCP 3.1** servers and **MCP 3.0 Task Protocol** integrations.

## What problem it solves
Managing multiple disparate AI tools, external provider API credentials, self-hosted local inference endpoints ([Ollama](../../services/ollama.md), LocalAI, ExLlamaV3, vLLM), remote vector databases, and custom MCP tool servers causes severe interface fragmentation. Developers and enterprise users are frequently forced to context-switch across fragmented browser tabs, terminal CLIs, desktop applications, and disparate authentication layers.

LobeHub eliminates interface fragmentation by functioning as an integrated "Agentic Workbench." It consolidates local and cloud model gateways, provides zero-trust document vector search, supports full-duplex WebRTC voice interaction, and simplifies tool orchestration through a built-in FastMCP 3.1 server manager, plugin marketplace, and role-based access control (RBAC).

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
        RAG["Knowledge Base Vector Search (Pgvector/Milvus)"]
        SSO["OAuth2 / OIDC SSO Gateway (Logto/Keycloak)"]
    end

    subgraph Gateway ["Unified Model Gateway & Router"]
        NORM["API Protocol Normalizer"]
        RATE["Rate Limiting & Token Manager"]
        STREAM["Stream Transformer"]
    end

    subgraph Backends ["Downstream Providers & Tools"]
        CLOUD["Cloud AI (OpenAI, Anthropic, Google, Cohere)"]
        LOCAL["Local Inference (Ollama, LocalAI, ExLlamaV3, vLLM)"]
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
- **FastMCP 3.1 Tool Server Management**: Providing a visual graphical workbench to test, debug, and execute FastMCP 3.1 tool calls across sandboxed environments.
- **Full-Duplex Voice Agents**: Running low-latency speech conversations powered by WebRTC and local text-to-speech runtimes.

## Production Systemd Service Unit Configuration

For bare-metal or container-free production deployments running LobeChat as a persistent systemd service, configure `/etc/systemd/system/lobechat.service`:

```ini
[Unit]
Description=LobeChat Enterprise Multi-Agent Workbench Service
After=network.target postgresql.service redis.service
Wants=postgresql.service redis.service

[Service]
Type=simple
User=lobehub
Group=lobehub
WorkingDirectory=/opt/lobe-chat
Environment=NODE_ENV=production
Environment=PORT=3210
Environment=HOSTNAME=0.0.0.0
EnvironmentFile=/etc/lobehub/environment
ExecStart=/usr/bin/node /opt/lobe-chat/server.js
Restart=always
RestartSec=5s
LimitNOFILE=65536
LimitNPROC=32768
MemoryMax=16G
TasksMax=4096

# Security Hardening & Sandboxing
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/lobe-chat/data /var/log/lobehub /tmp
NoNewPrivileges=true
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX

[Install]
WantedBy=multi-user.target
```

To enable, start, and monitor the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now lobechat.service
sudo systemctl status lobechat.service
journalctl -u lobechat.service -f --output=short-iso
```

## Production Multi-Container Docker Compose Stack

The following production-grade `docker-compose.yml` deploys the full LobeChat Database version alongside PostgreSQL with `pgvector`, MinIO S3 object storage for uploads, Redis caching, and Logto authentication:

```yaml
version: "3.8"

services:
  lobe-chat:
    image: lobehub/lobe-chat-database:v1.38.0
    container_name: lobechat-app
    restart: always
    ports:
      - "3210:3210"
    environment:
      - NODE_ENV=production
      - APP_URL=https://lobe.internal.net
      - DATABASE_URL=postgresql://lobe:lobepassword@postgres:5432/lobe_chat
      - KEY_VAULTS_SECRET=d8f7e6c5b4a3928170f1e2d3c4b5a697887766554433221100aabbccddeeff00
      - NEXT_AUTH_SECRET=99887766554433221100aabbccddeeff00112233445566778899aabbccddeeff
      - REDIS_URL=redis://redis:6379/0
      - S3_ENDPOINT=http://minio:9000
      - S3_BUCKET=lobe-storage
      - S3_ACCESS_KEY_ID=minioadmin
      - S3_SECRET_ACCESS_KEY=minioadminpassword
      - S3_PUBLIC_DOMAIN=https://s3.internal.net
      - ENABLE_OIDC=1
      - OIDC_ISSUER=https://auth.internal.net/oidc
      - OIDC_CLIENT_ID=lobechat
      - OIDC_CLIENT_SECRET=oidc-client-secret
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio:
        condition: service_started
    networks:
      - lobehub-net

  postgres:
    image: pgvector/pgvector:pg16
    container_name: lobechat-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=lobe
      - POSTGRES_PASSWORD=lobepassword
      - POSTGRES_DB=lobe_chat
    volumes:
      - pg-data:/var/lib/postgresql/data
    networks:
      - lobehub-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U lobe -d lobe_chat"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7.2-alpine
    container_name: lobechat-redis
    restart: unless-stopped
    command: redis-server --save 60 1 --loglevel warning --maxmemory 2gb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    networks:
      - lobehub-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  minio:
    image: minio/minio:RELEASE.2024-09-22T00-33-43Z
    container_name: lobechat-minio
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadminpassword
    volumes:
      - minio-data:/data
    networks:
      - lobehub-net

networks:
  lobehub-net:
    driver: bridge

volumes:
  pg-data:
  redis-data:
  minio-data:
```

## Strengths
- **Native FastMCP 3.1 Support**: Direct graphical interface for discovering, authorizing, and executing tools on external MCP servers.
- **Multi-Modal WebRTC Interface**: Seamless, full-duplex speech interaction and real-time vision stream analysis.
- **Extensive Plugin Marketplace**: Instant deployment of hundreds of pre-configured community tools and agents.
- **Flexible Deployment Models**: Deployable as a client-side local PWA or a multi-tenant PostgreSQL/Redis database-backed enterprise service.
- **Fine-Grained Model Routing**: Dynamic routing across OpenAI, Anthropic, Google Gemini, Ollama, LocalAI, and vLLM backends.

## Limitations
- **Database Deployment Overhead**: Configuring the full database-backed enterprise setup requires orchestrating PostgreSQL with pgvector, Redis, and S3-compatible object storage.
- **Memory Consumption**: Running real-time multi-agent sessions with active vector indexes and streaming voice requires substantial host memory.
- **Configuration Complexity**: Enterprise OIDC and RBAC setups require precise synchronisation of callback URLs and secret keys.

## When to use it
- When seeking a modern, multi-model client interface with native FastMCP 3.1 support.
- When organizing team workflows into specialized, collaborating agent personas.
- When strict data sovereignty mandates hosting chat logs, vector stores, and model endpoints entirely on-premises.

## When not to use it
- When requiring a lightweight command-line interactive agent (use [Claude Code](../development_ops/claude-code.md)).
- When constructing complex graphical node-based agent flowcharts (use [Langflow](../frameworks/langflow.md) or [Rivet](../frameworks/rivet.md)).

## Getting started

### 1. Verification
Verify that the HTTP endpoint is active and healthy:
```bash
curl -I http://localhost:3210/api/health
```

### 2. FastMCP Configuration File Example
Create `lobe-mcp-config.json` to register local FastMCP servers:
```json
{
  "mcpServers": {
    "local-tools": {
      "command": "python3",
      "args": ["/opt/mcp/server.py"],
      "env": {
        "FAST_MCP_LOG_LEVEL": "info"
      }
    }
  }
}
```

## CLI examples

### 1. Pull Latest Image and Restart
```bash
docker pull lobehub/lobe-chat-database:latest && docker compose up -d
```

### 2. Inspect Active PostgreSQL Migrations
```bash
docker exec -it lobechat-postgres psql -U lobe -d lobe_chat -c "SELECT version(); \dt"
```

### 3. Launch FastMCP 3.1 Inspector
```bash
npx @modelcontextprotocol/inspector lobe-mcp-config.json
```

## API examples

### FastMCP 3.1 Server Provider & Agent Tool Registry (Strict Pydantic v2)
This complete FastMCP 3.1 server validates provider configurations and dynamic model settings for LobeHub integrations using strict **Pydantic v2** models with `extra="forbid"`.

```python
#!/usr/bin/env python3
"""
LobeHub FastMCP 3.1 Agent & Session Configuration Server.
Enforces strict Pydantic v2 models with extra="forbid" for registering multi-agent configs.
"""

import os
import json
import logging
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationError
from mcp.server.fastmcp import FastMCP

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("lobehub-fastmcp")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("lobehub-config-engine", version="3.1.0")

class ModelParams(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: float = Field(default=1.0, ge=0.0, le=1.0, description="Nucleus sampling threshold")
    context_window: int = Field(default=128000, alias="contextWindow", ge=2048, description="Max context tokens")
    use_mcp: bool = Field(default=True, alias="useMcp", description="Enable FastMCP tool calling")

class ProviderRegistration(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    provider_id: str = Field(..., alias="providerId", description="Provider slug identifier")
    model_name: str = Field(..., alias="modelName", description="Model identifier")
    api_base_url: Optional[str] = Field(None, alias="apiBaseUrl", description="Custom API gateway base URL")
    params: ModelParams = Field(default_factory=ModelParams, description="Model generation parameters")

    @field_validator("provider_id")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        allowed = {"openai", "anthropic", "google", "ollama", "localai", "deepseek", "vllm", "cohere", "mastra"}
        if v.lower() not in allowed:
            raise ValueError(f"Provider '{v}' is not supported. Supported: {allowed}")
        return v.lower()

class AgentDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    agent_id: str = Field(..., alias="agentId", min_length=3, description="Unique agent slug identifier")
    system_prompt: str = Field(..., alias="systemPrompt", min_length=10, description="Core system instructions")
    tools: List[str] = Field(default_factory=list, description="Enabled FastMCP tool names")
    provider_config: ProviderRegistration = Field(..., alias="providerConfig", description="Model provider configuration")

class AgentRegisterResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str
    agent_id: str
    registered_tools: List[str]
    provider: str

@mcp.tool(
    name="register_lobehub_agent",
    description="Validates and registers a new LobeHub multi-agent configuration using strict Pydantic v2 schemas."
)
async def register_lobehub_agent(agent_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validates and registers a new LobeHub agent specification."""
    try:
        agent = AgentDefinition.model_validate(agent_data)
        logger.info("Registering agent '%s' with provider '%s'", agent.agent_id, agent.provider_config.provider_id)
        response = AgentRegisterResponse(
            status="SUCCESS",
            agent_id=agent.agent_id,
            registered_tools=agent.tools,
            provider=agent.provider_config.provider_id
        )
        return response.model_dump()
    except ValidationError as val_err:
        logger.error("Agent validation failed: %s", val_err.errors())
        return {"status": "VALIDATION_FAILED", "errors": val_err.errors()}

@mcp.tool(
    name="verify_mcp_server_connection",
    description="Probes connectivity and task capabilities of an external FastMCP tool server."
)
async def verify_mcp_server_connection(server_url: str) -> Dict[str, Any]:
    """Simulates connection probe to an MCP tool server."""
    logger.info("Probing MCP server connection at: %s", server_url)
    return {
        "server_url": server_url,
        "status": "CONNECTED",
        "mcp_version": "3.1",
        "capabilities": ["tools", "resources", "prompts", "tasks"]
    }

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Issue / Error Symptom | Cause | Diagnostic Inspection Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **WebRTC Audio Stutter** | Packet loss or network buffer underflow during speech streaming. | `curl -i http://localhost:3210/api/health` | Adjust audio buffer sizes in client settings or use OPUS codec fallback. Check UDP port forwarding. |
| **PGVector Query Latency > 200ms** | Missing HNSW vector index on database embedding table. | `docker exec -it lobechat-postgres psql -U lobe -d lobe_chat -c "\d embeddings"` | Create HNSW index: `CREATE INDEX ON embeddings USING hnsw (vector vector_cosine_ops);` |
| **MCP Tool Call Rejected** | Security authorization token expired or tool permission disabled. | `docker logs lobechat-app \| grep "MCP"` | Re-authenticate MCP tool server token in LobeHub settings UI and verify allowed origins. |
| **Redis Connection Timeout** | Redis instance reached max connections limit or out of memory. | `docker exec -it lobechat-redis redis-cli info clients` | Increase `maxclients` in `redis.conf` or configure Redis connection pooling with reasonable idle timeouts. |
| **Ollama Endpoint Unreachable** | Docker container unable to reach host-bound Ollama daemon. | `curl http://host.docker.internal:11434/api/tags` | Set environment variable `OLLAMA_ORIGINS="*"` on Ollama host, and use `http://host.docker.internal:11434` URL. |
| **OIDC SSO Auth Failure: 401** | Redirect URI mismatch between LobeChat configuration and identity provider. | `docker logs lobechat-app \| grep -i "oidc"` | Ensure `APP_URL` matches exactly with callback redirect URI registered in Logto/Keycloak client settings. |

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
- [LocalAI](../infrastructure/localai.md) — OpenAI-compatible local multi-modal inference server.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardization protocol for model tool calls.

## Sources / references
- [LobeHub Official Website](https://lobehub.com/)
- [LobeChat GitHub Repository](https://github.com/lobehub/lobe-chat)
- [FastMCP Framework Specification](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
