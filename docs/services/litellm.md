# LiteLLM

## What it is
LiteLLM is an open-source AI Gateway (proxy server) and Python SDK that provides a unified OpenAI-compatible interface to 100+ LLM providers. In January 2027, it serves as the enterprise-standard "Inference Plane," natively supporting **Claude 5.1**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, **DeepSeek-V4**, and local **Gemma 3** models. It acts as a central traffic controller, offering intelligent routing, semantic caching, automated fallbacks, spend enforcement, and native **FastMCP 3.1 tool and resource routing** for multi-agent ecosystems.

## What problem it solves
Managing multiple autonomous agent systems (Aider, Claude Code, Roo Code, OpenHands, n8n) across heterogeneous local GPUs and cloud LLM providers creates fragmented secrets, API schema divergence, and untracked expenses. LiteLLM solves this by presenting a single OpenAI-compatible endpoint that standardizes request normalization, manages automatic failovers, and enforces tenant budgets, preventing model rate limits or cloud outages from cascading into agent pipeline failures.

## Where it fits in the stack
**Category**: Service / AI Infrastructure / Abstraction Layer. LiteLLM is the primary "Service Mesh" for enterprise LLMs. It sits between autonomous AI agents and underlying model inference engines (Ollama, vLLM, Anthropic, Bedrock, OpenAI, DeepSeek), providing protocol normalization, unified observability telemetry (OpenTelemetry), and secure tool discovery via the **FastMCP 3.1** protocol.

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

### Python: Robust Completion with Pydantic v2 Validation
Using LiteLLM with **Pydantic v2** (`BaseModel`, `Field`, `model_validate`) for structured output parsing and type validation.

```python
import json
import litellm
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

# Define the expected structured output schema using Pydantic v2
class ActionPlan(BaseModel):
    task_name: str = Field(..., description="The name of the automated workflow task")
    steps: List[str] = Field(..., description="Sequential step-by-step directives")
    assigned_agent: str = Field(..., description="Target autonomous agent for execution")
    estimated_cost_usd: Optional[float] = Field(None, description="Estimated inference expenditure")

def get_agent_plan(prompt: str) -> ActionPlan:
    response = litellm.completion(
        model="claude-5-1",
        messages=[
            {"role": "system", "content": "Return valid JSON matching the ActionPlan schema."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    try:
        parsed_json = json.loads(content)
        validated_plan = ActionPlan.model_validate(parsed_json)
        return validated_plan
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Failed to validate LiteLLM structured output: {e}")
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
