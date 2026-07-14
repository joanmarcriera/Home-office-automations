# LiteLLM

## What it is
LiteLLM is an open-source AI Gateway (proxy server) and Python SDK that provides a unified OpenAI-compatible interface to 100+ LLM providers. In July 2026, it serves as the industry-standard "Inference Plane," natively supporting **Gemma 3**, Claude 4.8, and GPT-5.5. It acts as a central traffic controller, offering routing, fallbacks, budget enforcement, and native **MCP 3.0 tool routing** for agentic ecosystems.

## What problem it solves
Managing multiple agents (Aider, OpenHands, n8n) against various local and cloud LLMs creates fragmented secrets, inconsistent APIs, and untracked costs. LiteLLM solves this by presenting a single OpenAI-compatible endpoint that handles internal routing, automatic fallbacks, and centralized cost tracking, preventing provider outages from cascading into agent failures.

## Where it fits in the stack
**Category**: Service / AI Infrastructure / Abstraction Layer. LiteLLM is the primary "Service Mesh" for LLMs. It sits between agents and model providers (Ollama, Anthropic, Bedrock), providing protocol normalization and secure tool discovery via the **Model Context Protocol (MCP 3.0)**.

## Typical use cases
- **Multi-Agent Orchestration**: Providing a unified endpoint for [OpenHands](../tools/development_ops/openhands.md) and [Aider](../tools/development_ops/aider.md) to share model pools.
- **Resilient AI Pipelines**: Implementing automatic failover from local [Ollama](ollama.md) models to cloud providers during load spikes.
- **Agentic Tool Routing**: Using native **MCP 3.0** support to route tool calls from agents to the appropriate backend service.
- **Cost & Budget Enforcement**: Setting per-key or per-agent spend limits across all LLM usage.
- **PII Masking**: Enforcing data privacy guardrails at the gateway level before prompts reach cloud providers.

## Strengths
- **Protocol Normalization**: Every agent speaks OpenAI Chat Completions, regardless of the actual backend.
- **Built-in Fallbacks**: Automatic failover to healthy models during rate limits or outages.
- **Unified MCP Gateway**: Securely exposes and routes **MCP 3.0** servers to connected agents.
- **Cost Tracking**: Real-time spend monitoring for local vs. cloud calls.
- **Self-Hostable**: Full control over data and keys with a built-in management UI.

## Limitations
- **Operational Overhead**: Adds another service to maintain in the stack.
- **PostgreSQL Dependency**: Persistence of virtual keys and UI data requires a Postgres instance.
- **Latency Overhead**: Proxying adds a small (5-20ms) latency to each call.

## When to use it
- When running multiple AI agents with different LLM backends (e.g., local **Gemma 3** and cloud Claude 4.8).
- To track and limit AI spend across a team or an automated agent cluster.
- When tools only support OpenAI APIs but you want to utilize [Ollama](ollama.md) or [Bedrock](../tools/providers/aws-bedrock.md).
- For resilient systems requiring automatic model failover.

## When not to use it
- For simple, single-provider scripts where a proxy adds unnecessary complexity.
- When absolute sub-5ms latency is the primary requirement.

## Getting started

### Deployment (Docker)
```bash
docker run \
  -v $(pwd)/litellm-config.yaml:/app/config.yaml \
  -p 4000:4000 \
  -e LITELLM_MASTER_KEY="sk-your-master-key" \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml
```

### Core Configuration (`litellm-config.yaml`)
```yaml
model_list:
  - model_name: gemma-3
    litellm_params:
      model: ollama/gemma-3
      api_base: http://local-gpu:11434
  - model_name: claude-4-8
    litellm_params:
      model: anthropic/claude-4-8-opus-20260528
      api_key: os.environ/ANTHROPIC_API_KEY

router_settings:
  routing_strategy: least-busy
  fallback_model: gemma-3
```

## CLI examples
LiteLLM can be managed via its CLI for testing and server operations.

```bash
# Start a proxy with a specific model directly
litellm --model ollama/gemma-3

# Run database migrations for the management UI
litellm --migrate

# Check version and health
litellm --version
```

## API examples

### Virtual Key Generation
```bash
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "openhands-agent",
    "max_budget": 10.0,
    "budget_duration": "monthly"
  }'
```

### Python SDK Usage
Unified call interface for any provider.

```python
import litellm

response = litellm.completion(
    model="gemma-3",
    messages=[{"role": "user", "content": "Analyze this code..."}]
)
print(response.choices[0].message.content)
```

### MCP Server Integration
```yaml
# In litellm-config.yaml
mcp_servers:
  - name: "google-drive"
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-google-drive"]
```

## Related tools / concepts
- [OpenRouter](../tools/ai_knowledge/openrouter.md) — Cloud-based model router.
- [Ollama](ollama.md) — Local model serving backend.
- [OpenHands](../tools/development_ops/openhands.md) — Software engineering agent.
- [Langfuse](../tools/process_understanding/langfuse.md) — Observability backend.
- [Authentik](authentik.md) — For securing the LiteLLM UI.
- [n8n](n8n.md) — For LLM-powered automation workflows.
- [Home Assistant](home-assistant.md) — For AI-driven home automation.
- [MCP 3.0](../tools/automation_orchestration/mcp.md) — Protocol for agentic tool discovery.

## Sources / references
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [GitHub — BerriAI/litellm](https://github.com/BerriAI/litellm)
- [LiteLLM Proxy Quick Start](https://docs.litellm.ai/docs/proxy/docker_quick_start)
- [Virtual Keys & Budgets](https://docs.litellm.ai/docs/proxy/virtual_keys)

## Contribution Metadata
- Last reviewed: 2026-07-06
- Confidence: high
