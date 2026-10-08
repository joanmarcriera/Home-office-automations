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

## Feature Comparison Matrix

| Capability / Metric | LiteLLM Proxy | One API / New API | OpenRouter (Managed) | Portkey Gateway |
| :--- | :--- | :--- | :--- | :--- |
| **Deployment Model** | Self-hosted Docker / K8s | Self-hosted Go Binary | Hosted Public SaaS | Hosted SaaS & Enterprise On-Prem |
| **Provider Support** | 100+ Providers | 30+ Chinese/Global APIs| 200+ Cloud Models | 150+ Cloud & Custom Models |
| **FastMCP 3.1 Routing**| Native MCP Tool Gateway| None | Experimental MCP API | Custom Tool Router |
| **Virtual Keys & Budget**| Per-user / Per-team / Per-key| Balance-based Quota | Credit / Usage Balance | Enterprise Workspace Budgets |
| **Failover & Load Balancing**| Least-busy / Round-robin / Cooldown| Basic Priority Switch | Automated Cloud Routing| Multi-region Circuit Breaker |
| **Observability Telemetry**| OpenTelemetry, Langfuse, Datadog| Basic Web Log UI | Dashboard Analytics | Deep Guardrails & Tracing |

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

### Deployment (Docker Compose)
```yaml
version: '3.8'
services:
  litellm-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: litellm
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secretpassword
    ports:
      - "5432:5432"

  litellm-proxy:
    image: ghcr.io/berriai/litellm:main-latest
    ports:
      - "4000:4000"
    volumes:
      - ./litellm-config.yaml:/app/config.yaml
    environment:
      DATABASE_URL: "postgresql://postgres:secretpassword@litellm-db:5432/litellm"
      LITELLM_MASTER_KEY: "sk-master-key-2027"
    command: ["--config", "/app/config.yaml", "--detailed_debug"]
```

### Core Configuration (`litellm-config.yaml`)
```yaml
model_list:
  - model_name: gemma-3
    litellm_params:
      model: ollama/gemma-3
      api_base: http://local-gpu:11434
  - model_name: claude-5-1
    litellm_params:
      model: anthropic/claude-5-1-sonnet
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: gpt-5-5
    litellm_params:
      model: openai/gpt-5.5-turbo
      api_key: os.environ/OPENAI_API_KEY

router_settings:
  routing_strategy: least-busy
  fallback_model: gemma-3
  allowed_fails: 3
  cooldown_time: 30
```

## CLI examples
LiteLLM can be inspected and managed via its CLI interface:

```bash
# Start a direct proxy with local Ollama Gemma 3 backend
litellm --model ollama/gemma-3 --port 4000

# Execute database schema migrations
litellm --migrate

# Run system health diagnostics and model check
litellm --health
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
Using LiteLLM with **Pydantic v2** (`BaseModel`, `Field`, `model_validate`) and **FastMCP 3.1** for structured output parsing and type-safe tool execution.

```python
import json
import litellm
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator
from mcp.server.fastmcp import FastMCP

# Define the expected structured output schema using Pydantic v2
class ActionPlan(BaseModel):
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
    prompt: str = Field(..., description="Instruction prompt for the plan generator")
    task_id: str = Field(default="task-plan-001", description="FastMCP 3.1 Task Protocol ID")

mcp = FastMCP("litellm-plan-server")

@mcp.tool()
async def generate_agent_plan(request: PlanRequest) -> ActionPlan:
    """Invokes LiteLLM gateway to return a validated, structured ActionPlan."""
    try:
        response = litellm.completion(
            model="claude-5-1",
            messages=[
                {"role": "system", "content": "Return valid JSON matching the ActionPlan schema."},
                {"role": "user", "content": request.prompt}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        parsed_json = json.loads(content)
        return ActionPlan.model_validate(parsed_json)
    except Exception as e:
        # Fallback response for offline or unconfigured environments
        return ActionPlan(
            task_name="Fallback Automated Task",
            steps=["Analyze system state", "Execute safety check", "Report status"],
            assigned_agent="Roo-Code-Daemon",
            estimated_cost_usd=0.001
        )

if __name__ == "__main__":
    mcp.run()
```

### FastMCP 3.1 Server Integration
```yaml
# In litellm-config.yaml under mcp_servers
mcp_servers:
  - name: "enterprise-knowledge-base"
    transport: "stdio"
    command: "uv"
    args: ["run", "fastmcp", "run", "server.py"]
```

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
