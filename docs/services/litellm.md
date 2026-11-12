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

## Mathematical Formulation & Latency Roofline Analysis

In high-concurrency multi-agent clusters, total request turnaround time $T_{\text{total}}$ through the LiteLLM gateway comprises gateway proxy latency, model queueing delay, and token generation time:

$$
T_{\text{total}} = T_{\text{proxy}} + T_{\text{queue}} + \frac{N_{\text{input}}}{\beta_{\text{prompt}}} + \frac{N_{\text{output}}}{\text{TPS}_{\text{engine}}}
$$

Where:
- $T_{\text{proxy}}$ is the internal proxy traversal overhead ($T_{\text{auth}} + T_{\text{router}} + T_{\text{cache}} \approx 2.5\text{ms} - 8.2\text{ms}$).
- $T_{\text{queue}}$ represents queueing latency at the target inference backend under concurrency $C$.
- $\beta_{\text{prompt}}$ is prompt prefill ingestion bandwidth in tokens per second.
- $\text{TPS}_{\text{engine}}$ is the autoregressive token generation rate of the chosen backend.

### Caching Hit Probability & Expected Gateway Latency

When semantic caching (Redis / Vector DB) is active with cache hit probability $p_h \in [0, 1]$ and cache lookup latency $t_{\text{cache}} \le 4\text{ms}$:

$$
\mathbb{E}[T_{\text{response}}] = p_h \cdot (T_{\text{proxy}} + t_{\text{cache}}) + (1 - p_h) \cdot \left( T_{\text{proxy}} + T_{\text{upstream}} \right)
$$

For an enterprise cluster operating with $p_h = 0.35$ on repetitive agent tool-calling loops, average latency drops by:

$$
\Delta \bar{T} = p_h \cdot \left( T_{\text{upstream}} - t_{\text{cache}} \right) \approx 0.35 \times (420\text{ms} - 4\text{ms}) \approx 145.6\text{ms}
$$

### Routing Optimization Under Budget & Rate Constraints

LiteLLM routes incoming prompt vector $\mathbf{x}$ across $K$ provider deployments according to a constrained cost-latency objective:

$$
\min_{k \in \{1, \dots, K\}} \left( \lambda \cdot \text{Cost}_k(\mathbf{x}) + (1 - \lambda) \cdot \mathbb{E}[T_k] \right) \quad \text{subject to} \quad \text{RPM}_k(t) < \text{RPM}_{\max, k}, \quad \text{ErrorRate}_k < \epsilon
$$

When provider $k$ returns HTTP 429 or connection timeout, LiteLLM triggers automated exponential cooldown:

$$
\tau_{\text{cooldown}}(r) = \min\left( \tau_{\max}, \tau_{\text{base}} \cdot 2^r \right)
$$

where $r$ is the consecutive failure count, automatically preventing upstream cascading blackouts.

## Feature Comparison Matrix

| Capability / Metric | LiteLLM Proxy | One API / New API | OpenRouter (Managed) | Portkey Gateway | Cloudflare AI Gateway |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Deployment Model** | Self-hosted Docker / K8s | Self-hosted Go Binary | Hosted Public SaaS | Hosted SaaS & Enterprise On-Prem | Cloudflare Workers Edge |
| **Provider Support** | 100+ Providers | 30+ Chinese/Global APIs| 200+ Cloud Models | 150+ Cloud & Custom Models | 50+ Major Providers |
| **FastMCP 3.1 Routing**| Native MCP Tool Gateway| None | Experimental MCP API | Custom Tool Router | Limited REST Proxy |
| **Virtual Keys & Budget**| Per-user / Per-team / Per-key| Balance-based Quota | Credit / Usage Balance | Enterprise Workspace Budgets | Basic Token Capping |
| **Failover & Load Balancing**| Least-busy / Round-robin / Cooldown| Basic Priority Switch | Automated Cloud Routing| Multi-region Circuit Breaker | Tiered Fallbacks |
| **Observability Telemetry**| OpenTelemetry, Langfuse, Datadog| Basic Web Log UI | Dashboard Analytics | Deep Guardrails & Tracing | Cloudflare Analytics Logs |
| **Semantic Caching** | Native Redis / Qdrant Caching | In-Memory Token Caching | Upstream Provider Cache | Redis / Built-in Semantic | Cloudflare Edge KV Cache |
| **Streaming Overhead** | Sub-5ms TTFT Delay | ~8ms TTFT Delay | Network Egress Latency | ~10ms Gateway Hop | ~12ms Cloudflare Hop |

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
- **Latency Overhead**: Proxying and guardrail checks add a minimal latency penalty (approx. 2.5-8ms) to request roundtrips.

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
4. **Semantic Cache Invalidation**: Monitor Redis cache expiration policies (`TTL: 86400`) to prevent serving stale deterministic outputs when fine-tuned system instructions change.
5. **Observability Exporters**: Route OpenTelemetry spans directly to Langfuse or Datadog using non-blocking asynchronous collectors to eliminate telemetry pipeline backpressure.

## Getting started

### Installation
Install the LiteLLM Python package with proxy and FastMCP dependencies:
```bash
pip install "litellm[proxy]" "mcp>=1.3.0"
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
    image: redis:7.4-alpine
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
      - ./litellm-config.yaml:/app/config.yaml:ro
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
  litellm_db_data:
  litellm_redis_data:
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

### 4. Query Real-Time Model Spend via CLI
Retrieve token expenditure summaries across active virtual keys:
```bash
curl -s -X GET "http://localhost:4000/spend/calculate" \
  -H "Authorization: Bearer sk-master-key-2027" | jq .
```

### 5. Benchmark Gateway Round-Trip Latency
Measure proxy forwarding latency compared to direct inference:
```bash
python3 -m litellm.benchmark --proxy "http://localhost:4000" --model "gpt-5.5-turbo" --concurrency 10
```

## Production Deployment & System Infrastructure

### Gateway Configuration (`litellm-config.yaml`)
```yaml
model_list:
  - model_name: gpt-5.5-turbo
    litellm_params:
      model: openai/gpt-5.5-turbo
      api_key: os.environ/OPENAI_API_KEY
      rpm: 1000
      tpm: 1000000

  - model_name: claude-5-1
    litellm_params:
      model: anthropic/claude-5-1
      api_key: os.environ/ANTHROPIC_API_KEY
      rpm: 800

  - model_name: deepseek-v4-local
    litellm_params:
      model: ollama/deepseek-v4
      api_base: http://localhost:11434
      rpm: 300

router_settings:
  routing_strategy: least-busy
  model_group_alias:
    smart-agent: ["claude-5-1", "gpt-5.5-turbo", "deepseek-v4-local"]
  fallbacks:
    - claude-5-1: ["gpt-5.5-turbo", "deepseek-v4-local"]
  cooldown_time: 60
  allowed_fails: 3

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
```

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
Using LiteLLM with **Pydantic v2** (`BaseModel`, `Field`, `ConfigDict`, `model_validate`, `field_validator`) and **FastMCP 3.1** for structured output parsing, strict schema enforcement, and type-safe tool execution.

```python
"""LiteLLM FastMCP 3.1 Gateway Server with Pydantic v2 Schema Validation."""

import json
import litellm
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator
from mcp.server.fastmcp import FastMCP

# Define strict structured output schemas using Pydantic v2
class ActionStep(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    step_id: int = Field(..., description="Monotonically increasing execution index")
    instruction: str = Field(..., description="Specific tool or command directive")
    estimated_ms: int = Field(default=500, description="Estimated execution latency in ms")

class ActionPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_name: str = Field(..., description="The name of the automated workflow task")
    steps: List[ActionStep] = Field(..., description="Sequential step-by-step directives")
    assigned_agent: str = Field(..., description="Target autonomous agent for execution")
    estimated_cost_usd: Optional[float] = Field(None, description="Estimated inference expenditure")

    @field_validator("steps")
    @classmethod
    def validate_steps(cls, v: List[ActionStep]) -> List[ActionStep]:
        if not v:
            raise ValueError("Action plan must contain at least one execution step.")
        return v

class PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt: str = Field(..., min_length=5, description="Instruction prompt for the plan generator")
    task_id: str = Field(default="task-plan-001", description="FastMCP 3.1 Task Protocol ID")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0, description="Sampling randomness")

class AgentModelRouting(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    primary_model: str = Field(default="claude-5-1")
    fallback_model: str = Field(default="ollama/gemma-3")
    max_tokens: int = Field(default=4096, ge=1, le=128000)

class SpendTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    total_tokens: int = Field(..., ge=0)
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    cost_usd: float = Field(..., ge=0.0)

mcp = FastMCP("litellm-plan-server")

@mcp.tool()
async def generate_agent_plan(request: PlanRequest, routing: AgentModelRouting) -> Dict[str, Any]:
    """Invokes LiteLLM gateway to return a validated, structured ActionPlan with telemetry."""
    try:
        response = litellm.completion(
            model=routing.primary_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Generate an execution plan. Return JSON strictly complying with: "
                        '{"task_name": str, "steps": [{"step_id": int, "instruction": str, "estimated_ms": int}], '
                        '"assigned_agent": str, "estimated_cost_usd": float}'
                    )
                },
                {"role": "user", "content": request.prompt}
            ],
            temperature=request.temperature,
            max_tokens=routing.max_tokens,
            response_format={"type": "json_object"},
            fallbacks=[routing.fallback_model]
        )
        content = response.choices[0].message.content
        parsed_json = json.loads(content)
        validated_plan = ActionPlan.model_validate(parsed_json)

        usage = response.usage
        telemetry = SpendTelemetry(
            total_tokens=usage.total_tokens,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            cost_usd=float(getattr(response, "_response_cost", 0.001))
        )

        return {
            "status": "success",
            "plan": validated_plan.model_dump(),
            "telemetry": telemetry.model_dump()
        }
    except Exception as exc:
        fallback_plan = ActionPlan(
            task_name=f"Fallback Plan: {request.task_id}",
            steps=[
                ActionStep(step_id=1, instruction="Audit gateway connectivity", estimated_ms=200),
                ActionStep(step_id=2, instruction="Execute deterministic recovery loop", estimated_ms=800)
            ],
            assigned_agent="Roo-Code-Daemon",
            estimated_cost_usd=0.0
        )
        return {
            "status": "degraded_fallback",
            "error_detail": str(exc),
            "plan": fallback_plan.model_dump(),
            "telemetry": SpendTelemetry(
                total_tokens=0, prompt_tokens=0, completion_tokens=0, cost_usd=0.0
            ).model_dump()
        }

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
| `Semantic Cache Stale Response (HTTP 200)` | Redis vector embedding cache key collided across different model system prompts. | Prefix cache keys with system prompt hash in `litellm-config.yaml` and set Redis semantic cache similarity threshold to `>= 0.95`. |
| `CORS / WebSocket Handshake Failure` | Web UI or agent client connecting from disallowed origin or missing proxy upgrade headers. | Set `CORS_ORIGIN="*"` or domain whitelist and verify reverse proxy (Nginx/Traefik) passes `Upgrade $http_upgrade` headers. |

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
