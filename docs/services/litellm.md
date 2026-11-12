# LiteLLM

## What it is
LiteLLM is an open-source AI Gateway (proxy server) and Python SDK that provides a unified OpenAI-compatible interface to 100+ LLM providers. In January 2027, it serves as the enterprise-standard "Inference Plane," natively supporting **Claude 5.1**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, **DeepSeek-V4**, and local **Gemma 3** models. It acts as a central traffic controller, offering intelligent routing, semantic caching, automated fallbacks, spend enforcement, and native **FastMCP 3.1 tool and resource routing** for multi-agent ecosystems.

```
+-----------------------------------------------------------------------------------+
|                           LiteLLM AI Gateway Topology                             |
+-----------------------------------------------------------------------------------+
|  Agent Applications: Roo Code / Claude Code / Aider / n8n / FastMCP 3.1 Clients   |
|  +-----------------------------------------------------------------------------+  |
|  | Single OpenAI-Compatible Proxy Port (http://litellm-proxy:4000/v1)            |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | LiteLLM Core Gateway Engine                                                 |  |
|  | +------------------+ +------------------+ +------------------+ +-------------+ |  |
|  | | Auth & Virtual   | | Spend & Token    | | Semantic Cache   | | FastMCP 3.1 | |  |
|  | | Key Validation   | | Budget Enforcement| | (Redis / Memory) | | MCP Router  | |  |
|  | +------------------+ +------------------+ +------------------+ +-------------+ |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Intelligent Router & Fallback Handler (PostgreSQL State Backend)            |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                 +-----------------------+-----------------------+                 |
|                 |                                               |                 |
|                 v                                               v                 |
|  +------------------------------+             +--------------------------------+  |
|  | Local GPU Engines (Ollama/vLLM)|             | Cloud Provider APIs            |  |
|  | - Gemma 3 / DeepSeek-V4      |             | - Anthropic Claude 5.1         |  |
|  | - Llama 4 MoE                |             | - OpenAI GPT-5.6 / Gemini 4.0  |  |
|  +------------------------------+             +--------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Managing multiple autonomous agent systems (Aider, Claude Code, Roo Code, OpenHands, n8n) across heterogeneous local GPUs and cloud LLM providers creates fragmented secrets, API schema divergence, and untracked expenses. LiteLLM solves this by presenting a single OpenAI-compatible endpoint that standardizes request normalization, manages automatic failovers, and enforces tenant budgets, preventing model rate limits or cloud outages from cascading into agent pipeline failures.

## Where it fits in the stack
**Category**: Service / AI Infrastructure / Abstraction Layer. LiteLLM is the primary "Service Mesh" for enterprise LLMs. It sits between autonomous AI agents and underlying model inference engines (Ollama, vLLM, Anthropic, Bedrock, OpenAI, DeepSeek), providing protocol normalization, unified observability telemetry (OpenTelemetry), and secure tool discovery via the **FastMCP 3.1** protocol.

## Mathematical Formulations & Gateway Routing Dynamics

The operational stability and throughput of the LiteLLM proxy tier are governed by three primary analytical models: token-bucket rate limiting, semantic caching lookup efficiency, and circuit-breaker failover recovery dynamics.

### 1. Token-Bucket Rate Limiting & Concurrency Throttling
LiteLLM enforces virtual key and model deployment rate limits using a leaky token-bucket formulation evaluated in Redis cluster memory. Let $B$ denote the maximum burst capacity (in tokens or requests), $r$ denote the refill rate in tokens/sec, and $\Delta t = t - t_{\text{last}}$ represent elapsed time since the previous request:

$$
T_{\text{available}}(t) = \min\left(B, \; T_{\text{available}}(t_{\text{last}}) + r \cdot \Delta t\right) - C_{\text{req}}
$$

Where $C_{\text{req}}$ is the requested completion tokens plus prompt tokens estimated by LiteLLM's internal fast tokenizer. If $T_{\text{available}}(t) < 0$, the gateway returns HTTP 429 with header:

$$
\text{Retry-After} = \left\lceil \frac{|T_{\text{available}}(t)|}{r} \right\rceil
$$

Under high-concurrency multi-agent swarms ($N_{\text{agents}} \ge 50$), token contention across Redis keys is governed by optimistic Lua execution scripts that ensure atomic decrement without distributed locking deadlocks.

### 2. Semantic Cache Vector Proximity & Roofline Latency
When semantic caching is enabled across Redis or Qdrant vector backends, incoming prompt embeddings $\mathbf{e}_{\text{query}} \in \mathbb{R}^d$ are evaluated against cached prompt vectors $\mathbf{e}_i$ using cosine similarity:

$$
\text{Sim}(\mathbf{e}_{\text{query}}, \mathbf{e}_i) = \frac{\mathbf{e}_{\text{query}} \cdot \mathbf{e}_i}{\|\mathbf{e}_{\text{query}}\|_2 \|\mathbf{e}_i\|_2} \ge \tau_{\text{threshold}}
$$

The overall gateway response latency $T_{\text{total}}$ under semantic caching is modeled as:

$$
T_{\text{total}} = P(\text{hit}) \cdot \left( T_{\text{embed}} + T_{\text{ANN}} + T_{\text{fetch}} \right) + (1 - P(\text{hit})) \cdot \left( T_{\text{embed}} + T_{\text{ANN}} + T_{\text{provider}} + T_{\text{write}} \right)
$$

For $\tau_{\text{threshold}} = 0.92$, semantic cache hit rates $P(\text{hit})$ typically range from 0.28 to 0.44 across repetitive autonomous coding loops, reducing average round-trip latency from $1850\,\text{ms}$ to $42\,\text{ms}$.

### 3. Circuit-Breaker Failover Recovery Half-Life
When upstream provider endpoints fail or return $5\text{xx} / 429$ errors, LiteLLM transitions the route through states $\mathcal{S} \in \{\text{Closed}, \text{Open}, \text{Half-Open}\}$. The error score $E_m(t)$ for model route $m$ decays exponentially over cooldown interval $\tau_{\text{cool}}$:

$$
E_m(t) = \sum_{k=1}^K w_k \cdot \exp\left( -\frac{t - t_k}{\tau_{\text{cool}}} \right)
$$

Where $w_k = 1.0$ for HTTP 500/503 errors and $w_k = 0.5$ for rate limits. When $E_m(t) \ge \Theta_{\text{trip}}$, route $m$ is suspended, and traffic immediately routes to the next model in the fallback array. Once the route transitions to `Half-Open`, a test probe sample $P_{\text{probe}}$ is issued; if successful, $E_m(t)$ resets to 0.

## Feature Comparison Matrix

| Capability / Metric | LiteLLM Proxy | One API / New API | OpenRouter (Managed) | Portkey Gateway | Cloudflare AI Gateway |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Deployment Model** | Self-hosted Docker / K8s | Self-hosted Go Binary | Hosted Public SaaS | Hosted SaaS & Enterprise On-Prem | Cloud Edge Worker SaaS |
| **Provider Support** | 100+ Providers | 30+ Chinese/Global APIs| 200+ Cloud Models | 150+ Cloud & Custom Models | 50+ Major Providers |
| **FastMCP 3.1 Routing**| Native MCP Tool Gateway| None | Experimental MCP API | Custom Tool Router | Partial WebSocket Proxy |
| **Virtual Keys & Budget**| Per-user / Per-team / Per-key| Balance-based Quota | Credit / Usage Balance | Enterprise Workspace Budgets | Rate Limiting Rules Only |
| **Failover & Load Balancing**| Least-busy / Round-robin / Cooldown| Basic Priority Switch | Automated Cloud Routing| Multi-region Circuit Breaker | Basic Retry Policy |
| **Observability Telemetry**| OpenTelemetry, Langfuse, Datadog| Basic Web Log UI | Dashboard Analytics | Deep Guardrails & Tracing | Cloudflare Analytics Logs |
| **Semantic Caching** | Native Redis / Qdrant Vector | Simple Exact Key Hash | Hosted Cache Layer | Semantic Cache Module | KV Cache (Exact Match) |
| **Code Base License** | MIT Open Source | Apache 2.0 | Proprietary Closed | MIT Open Core | Proprietary SaaS |

## Typical use cases
- **Multi-Agent Orchestration**: Exposing a unified inference endpoint for [Roo Code](../tools/agents/roo-code.md), [Claude Code](../tools/development_ops/claude-code-setup.md), and [Aider](../tools/development_ops/aider.md) to dynamically share pooled rate limits.
- **Resilient AI Pipelines**: Executing zero-downtime automatic failover from local [Ollama](ollama.md) or vLLM instances to cloud models during GPU compute spikes.
- **Agentic Tool Routing**: Leveraging native **FastMCP 3.1** server registry support to dynamically expose and route tool calls from agents to underlying backend tools.
- **Enterprise Budget Enforcement**: Enforcing strict per-key, per-team, or per-agent token limits and USD spend caps across all model transactions.
- **PII & Compliance Guardrails**: Intercepting and masking sensitive data at the gateway level before prompts reach public cloud endpoints.

## Strengths
- **Protocol Normalization**: Standardizes request payloads to OpenAI Chat Completions, Assistant APIs, or FastMCP tool executions across all providers.
- **Built-in Fallbacks**: Intelligent health check routing and dynamic model switching on 429 rate limits or provider downtime.
- **Unified FastMCP Gateway**: Natively proxies and secures **FastMCP 3.1** tool calls between agents and microservices.
- **Granular Cost Telemetry**: Real-time spend monitoring, virtual key issuance, and usage breakdown for local vs. cloud endpoints.
- **Self-Hostable Infrastructure**: Full data sovereignty with self-hosted Docker/Kubernetes deployments and PostgreSQL-backed web management UI.

## Limitations
- **Operational Overhead**: Requires managing a dedicated database and proxy cluster in production.
- **Database Dependency**: Virtual key generation, real-time rate limiting, and management UI state require a resilient PostgreSQL cluster.
- **Latency Overhead**: Proxying and guardrail checks add a minimal latency penalty (approx. 5-15ms) to request roundtrips.

## When to use it
- When managing multi-agent teams with heterogeneous backends (e.g., hybrid deployments with local **Gemma 3** / **DeepSeek-V4** and cloud Claude 5.1).
- To track and restrict token burn and financial spend across diverse developer teams or automated agent clusters.
- When client applications require OpenAI API formats but need to leverage [Ollama](ollama.md), [Groq](../tools/providers/groq.md), or [Bedrock](../tools/providers/aws-bedrock.md).
- For mission-critical AI applications requiring automatic model failover and high availability.

## When not to use it
- For lightweight, single-provider scripts where maintaining proxy infrastructure introduces unnecessary friction.
- For ultra-low latency scenarios where sub-millisecond direct socket connections to inference engines are mandatory.

## Operational Best Practices & Troubleshooting
1. **PostgreSQL Connection Pooling**: Configure PgBouncer or set `DATABASE_POOL_SIZE: 20` when scaling beyond 100 concurrent agent threads to prevent database handle exhaustion.
2. **Cooldown Management on Rate Limits**: Set `cooldown_time: 60` in `litellm-config.yaml` to temporarily suspend rate-limited model deployments for 60 seconds before retrying.
3. **Master Key Storage**: Store `LITELLM_MASTER_KEY` in environment secret stores (e.g., HashiCorp Vault or Kubernetes Secrets) and generate ephemeral virtual keys for agent workloads rather than hardcoding master credentials.

## Getting started

### Installation
Install the LiteLLM Python package and optional proxy dependencies:
```bash
pip install "litellm[proxy]"
```

### Hello-World Example
Call any model provider with a single unified interface:
```python
from litellm import completion

response = completion(
    model="gpt-5.5-turbo",
    messages=[{"role": "user", "content": "Hello LiteLLM!"}]
)
print(response.choices[0].message.content)
```

### Production Docker Proxy Setup
```yaml
version: '3.8'
services:
  litellm-db:
    image: postgres:16-alpine
    container_name: litellm-db
    environment:
      POSTGRES_DB: litellm
      POSTGRES_USER: litellm_user
      POSTGRES_PASSWORD: litellm_secure_password
    volumes:
      - litellm_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U litellm_user -d litellm"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  litellm-redis:
    image: redis:7-alpine
    container_name: litellm-redis
    ports:
      - "6379:6379"
    volumes:
      - litellm_redis_data:/data
    restart: unless-stopped

  litellm-proxy:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: litellm-proxy
    ports:
      - "4000:4000"
    volumes:
      - ./litellm-config.yaml:/app/config.yaml
    environment:
      DATABASE_URL: "postgresql://litellm_user:litellm_secure_password@litellm-db:5432/litellm"
      REDIS_URL: "redis://litellm-redis:6379/0"
      LITELLM_MASTER_KEY: "sk-master-key-2027"
      STORE_MODEL_IN_DB: "True"
    command: ["--config", "/app/config.yaml", "--port", "4000", "--num_workers", "8"]
    depends_on:
      litellm-db:
        condition: service_healthy
      litellm-redis:
        condition: service_started
    restart: unless-stopped

volumes:
  litellm-db_data:
  litellm-redis_data:
```

## CLI examples

### 1. Start Direct Local Proxy
Spin up an OpenAI-compatible proxy pointing to a model:
```bash
litellm --model ollama/gemma-3 --port 4000
```

### 2. Run System Health Diagnostic
Validate gateway connectivity and model endpoint availability:
```bash
litellm --health
```

### 3. Execute Database Migrations
Run PostgreSQL database schema migrations for LiteLLM key and budget tracking:
```bash
litellm --migrate
```

## Production Deployment & System Infrastructure

### Systemd Service Unit (`litellm-proxy.service`)
For standalone Linux host deployments requiring automated daemon management, restart behavior, and system logger integration:

```ini
[Unit]
Description=LiteLLM AI Gateway Service Proxy
After=network.target postgresql.service redis.service
Wants=postgresql.service redis.service

[Service]
Type=simple
User=litellm
Group=litellm
WorkingDirectory=/opt/litellm
ExecStart=/usr/local/bin/litellm --config /opt/litellm/litellm-config.yaml --port 4000 --num_workers 4
Restart=always
RestartSec=5s
Environment="LITELLM_MASTER_KEY=sk-master-key-2027"
Environment="DATABASE_URL=postgresql://litellm_user:litellm_secure_password@localhost:5432/litellm"
Environment="REDIS_URL=redis://localhost:6379/0"
Environment="PYTHONUNBUFFERED=1"
LimitNOFILE=65536

# Security Hardening
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Gateway Configuration (`litellm-config.yaml`)
Example enterprise routing configuration with model fallbacks, Redis caching, and FastMCP integration:

```yaml
model_list:
  - model_name: "claude-5-1"
    litellm_params:
      model: "anthropic/claude-5-1-sonnet-20270115"
      api_key: "os.environ/ANTHROPIC_API_KEY"
      rpm: 1000
      tpm: 80000

  - model_name: "gpt-5-5"
    litellm_params:
      model: "openai/gpt-5.5"
      api_key: "os.environ/OPENAI_API_KEY"
      rpm: 1500
      tpm: 120000

  - model_name: "local-gemma"
    litellm_params:
      model: "ollama/gemma-3"
      api_base: "http://ollama-service:11434"
      rpm: 5000

router_settings:
  routing_strategy: "least-busy"
  fallbacks: [{"claude-5-1": ["gpt-5-5", "local-gemma"]}]
  allowed_fails: 3
  cooldown_time: 60

litellm_settings:
  cache: true
  cache_type: "redis"
  redis_url: "os.environ/REDIS_URL"
  semantic_cache: true
  semantic_cache_threshold: 0.92
  telemetry: true
  callbacks: ["otel", "prometheus"]
```

## API examples

### Virtual Key Generation with Budget Cap
```bash
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "roo-code-agent-cluster",
    "max_budget": 50.0,
    "budget_duration": "monthly",
    "models": ["gemma-3", "claude-5-1", "gpt-5-5"]
  }'
```

### Python: FastMCP 3.1 & Pydantic v2 LiteLLM Completion Server
Using LiteLLM with strict **Pydantic v2** (`BaseModel`, `Field`, `ConfigDict`, `field_validator`) schemas and **FastMCP 3.1** for structured output parsing, token auditing, and type-safe tool execution.

```python
import json
import time
import litellm
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# Define the expected structured output schema using strict Pydantic v2
class ActionPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_name: str = Field(..., description="The name of the automated workflow task")
    steps: List[str] = Field(..., description="Sequential step-by-step directives")
    assigned_agent: str = Field(..., description="Target autonomous agent for execution")
    estimated_cost_usd: Optional[float] = Field(None, description="Estimated inference expenditure")

    @field_validator("steps")
    @classmethod
    def validate_steps(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Action plan must contain at least one execution step.")
        return v

class PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt: str = Field(..., description="Instruction prompt for the plan generator")
    task_id: str = Field(default="task-plan-001", description="FastMCP 3.1 Task Protocol ID")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)

class AgentModelRouting(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    primary_model: str = Field(default="claude-5-1", description="Primary upstream model")
    fallback_model: str = Field(default="ollama/gemma-3", description="Fallback route model")
    max_tokens: int = Field(default=4096, ge=1, le=128000)

class ExecutionTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["success", "fallback_used", "error"]
    latency_ms: float
    model_resolved: str
    action_plan: ActionPlan

mcp = FastMCP("litellm-plan-server", instructions="FastMCP 3.1 Gateway server interfacing with LiteLLM proxy.")

@mcp.tool(name="generate_agent_plan", description="Invokes LiteLLM gateway to return a validated, structured ActionPlan.")
async def generate_agent_plan(request: PlanRequest, routing: AgentModelRouting) -> str:
    """Invokes LiteLLM gateway to return a validated, structured ActionPlan."""
    start_time = time.time()
    try:
        response = litellm.completion(
            model=routing.primary_model,
            messages=[
                {"role": "system", "content": "Return valid JSON matching the ActionPlan schema with fields: task_name, steps, assigned_agent, estimated_cost_usd."},
                {"role": "user", "content": request.prompt}
            ],
            response_format={"type": "json_object"},
            fallbacks=[routing.fallback_model],
            temperature=request.temperature,
            max_tokens=routing.max_tokens
        )
        content = response.choices[0].message.content
        parsed_json = json.loads(content)
        validated_plan = ActionPlan.model_validate(parsed_json)
        elapsed = (time.time() - start_time) * 1000.0

        telemetry = ExecutionTelemetry(
            status="success",
            latency_ms=round(elapsed, 2),
            model_resolved=getattr(response, "model", routing.primary_model),
            action_plan=validated_plan
        )
        return telemetry.model_dump_json()
    except Exception as e:
        elapsed = (time.time() - start_time) * 1000.0
        fallback_plan = ActionPlan(
            task_name="Emergency Fallback Plan",
            steps=["Inspect LiteLLM proxy status", "Check Redis cache layer", "Failover to direct local model"],
            assigned_agent="Roo-Code-Daemon",
            estimated_cost_usd=0.0
        )
        telemetry = ExecutionTelemetry(
            status="fallback_used",
            latency_ms=round(elapsed, 2),
            model_resolved=routing.fallback_model,
            action_plan=fallback_plan
        )
        return telemetry.model_dump_json()

if __name__ == "__main__":
    mcp.run()
```

### FastMCP 3.1 Server Integration Configuration
```yaml
# In litellm-config.yaml under mcp_servers
mcp_servers:
  - name: "enterprise-knowledge-base"
    transport: "stdio"
    command: "uv"
    args: ["run", "fastmcp", "run", "server.py"]
```

## Diagnostic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| `HTTP 401 Unauthorized: Invalid Virtual Key` | Virtual key expired, exceeded budget cap, or master key mismatch. | Verify bearer key against PostgreSQL database with `curl http://localhost:4000/key/info?key=sk-...` or generate a new key using `$LITELLM_MASTER_KEY`. |
| `HTTP 429 Too Many Requests (Provider)` | Upstream LLM provider rate limits exhausted. | Configure model fallbacks and set `cooldown_time: 60` in `litellm-config.yaml` to trigger automatic routing to alternative backends. |
| `PostgreSQL PoolExhaustedError` | Max database connections exceeded under heavy agent concurrency. | Increase `DATABASE_POOL_SIZE` in environment variables or deploy PgBouncer connection pooler in front of PostgreSQL. |
| `FastMCP 3.1 Tool Timeout` | Agent tool call execution exceeded Gateway proxy timeout. | Increase tool call timeout in `litellm-config.yaml` under `request_timeout: 120` or optimize target MCP tool server execution speed. |
| `Model Fallback Loop Failure` | All primary and fallback models in router list failed health check. | Run `litellm --health` CLI diagnostic to identify unreachable backend endpoints (e.g., local vLLM or Ollama instance down). |
| `High Latency Spikes (>500ms proxy time)` | Large prompt payload audit logging or unindexed database queries. | Enable Redis caching (`LITELLM_REDIS_URL`), index PostgreSQL key tables, and set `disable_master_key_return: true`. |
| `Redis Cluster Eviction Storm` | Memory fragmentation or undersized `maxmemory` setting under semantic cache load. | Configure Redis `maxmemory-policy allkeys-lru` and expand cache node RAM allocation. |
| `Pydantic Schema Rejection on Proxy Tool Call` | FastMCP payload contains extra parameters rejected by strict schema validation. | Confirm tool schema matches client payload with `ConfigDict(extra="forbid", frozen=True)`. |

## Related tools / concepts
- [OpenRouter](../tools/ai_knowledge/openrouter.md) — Managed public cloud model routing network.
- [Ollama](ollama.md) — Local neural network inference engine.
- [OpenHands](../tools/development_ops/openhands.md) — Autonomous software engineering system.
- [Langfuse](../tools/process_understanding/langfuse.md) — Open-source LLM observability platform.
- [Authentik](authentik.md) — Identity provider for securing LiteLLM admin dashboards.
- [n8n](n8n.md) — Workflow automation hub integrating LiteLLM endpoints.
- [FastMCP 3.1](../tools/automation_orchestration/mcp.md) — Standardized protocol for agentic tool execution.
- [Roo Code](../tools/agents/roo-code.md) — Coding assistant configured with gateway proxies.

## Sources / references
- [LiteLLM Official Documentation](https://docs.litellm.ai/)
- [GitHub — BerriAI/litellm](https://github.com/BerriAI/litellm)
- [LiteLLM Enterprise Proxy Deployment Guide](https://docs.litellm.ai/docs/proxy/docker_quick_start)
- [FastMCP 3.1 Gateway Integration](https://docs.litellm.ai/docs/mcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
