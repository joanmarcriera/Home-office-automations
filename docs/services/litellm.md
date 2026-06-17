# LiteLLM

## What it is

LiteLLM is an open-source AI Gateway (proxy server) and Python SDK that provides a unified OpenAI-compatible interface to 100+ LLM providers — OpenAI, Anthropic, Google Vertex AI, AWS Bedrock, Azure OpenAI, Ollama, and more. As of June 2026, it serves as the industry-standard "Inference Plane" for agentic ecosystems, supporting Claude 4.8 Opus and GPT-5.5 natively. It sits between your agents and models, acting as a traffic controller with routing, fallbacks, budget enforcement, virtual keys, and observability built in.

**Backed by Y Combinator (W23).** MIT-licensed core; enterprise tier available.

## What problem it solves

When running multiple AI agents (OpenClaw, OpenHands, Aider, n8n AI nodes) against both local Ollama models and cloud providers, you quickly accumulate problems:

- Each tool has its own API format and SDK.
- Secrets are scattered across configs.
- There is no central cost tracking.
- Provider outages cascade into agent failures.
- Local Ollama models are not OpenAI-compatible by default for some tools.

LiteLLM solves all of these by presenting a single OpenAI-compatible endpoint that any tool can target, while internally routing, falling back, tracking costs, and enforcing budgets.

## Where it fits in the stack

**Provider Routing / Abstraction Layer**. LiteLLM is typically the first hop after an agent makes an LLM API call. It functions as the "Service Mesh" for LLMs, similar to how Istio functions for microservices.

```text
┌──────────────────────────────────────────────────────────┐
│  Agents: OpenHands │ OpenClaw │ Aider │ n8n AI nodes    │
└───────────────────────────┬──────────────────────────────┘
                            │  OpenAI-compatible call
┌───────────────────────────▼──────────────────────────────┐
│                    LiteLLM Proxy (port 4000)              │
│  ┌──────────────┐  ┌────────────┐  ┌───────────────────┐ │
│  │ Virtual Keys │  │  Router    │  │ Budget / Guardrail│ │
│  └──────────────┘  └──────────┘  └───────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  Logging (Langfuse │ Prometheus │ S3 │ stdout)       │ │
│  └──────────────────────────────────────────────────────┘ │
└──────┬────────────────────┬─────────────────┬─────────────┘
       │                    │                  │
 Ollama (local)      OpenRouter          Anthropic API
 192.168.0.5:30068   (free tier)         (cloud fallback)
```

## Typical use cases
- **Multi-Agent Orchestration**: Providing a single endpoint for OpenHands, OpenClaw, and Aider to share the same model pool and budget.
- **Cost Management**: Tracking and limiting spend for local experiments vs. production cloud calls.
- **Resilient AI Pipelines**: Implementing automatic failover from local Ollama models to cloud providers (Anthropic/OpenRouter) during heavy load or local downtime.
- **Local Development**: Simulating cloud model APIs using local models (e.g., using Qwen 2.5-Coder as an OpenAI-compatible substitute).
- **Enterprise Governance**: Enforcing PII masking and prompt injection guardrails across all internal AI usage.

## Strengths

- **Protocol Normalization**: Every agent speaks one language (OpenAI Chat Completions), regardless of backend.
- **100+ Provider Support**: OpenAI, Anthropic, Ollama, Bedrock, Azure, Vertex AI, OpenRouter, Replicate, and more.
- **Built-in Fallbacks**: Automatic failover when a model is down or rate-limited.
- **Cost Tracking**: Per-key and per-model spend tracked in real time.
- **Self-Hostable**: Full control; no third-party telemetry.
- **Management UI**: Visual key management and spend dashboard without external tooling.
- **Embeddable**: Works as a long-running proxy or imported as a Python library.

## Limitations

- **Operational Overhead**: Adds a service to maintain; needs health checks and restart policies.
- **PostgreSQL Dependency**: Full UI + key persistence requires a Postgres instance.
- **Feature Parity Gaps**: Not all provider-specific parameters are exposed; some advanced provider features require raw passthrough.
- **Local-Model Latency**: Proxying through LiteLLM adds ~5–20 ms per call vs direct Ollama calls.

## When to use it

- When running multiple AI agents with different LLM backends.
- When you need a centralized place to track AI spend and enforce budgets.
- For resilient systems that can survive provider outages via automatic fallback.
- When tools only support OpenAI format but you want to use Ollama or Bedrock.
- For team deployments where different people need different API key access levels.

## When not to use it

- If you only ever use one provider and one agent (direct calls are simpler).
- For very simple, low-volume scripts where a proxy adds unnecessary complexity.
- When sub-5 ms latency is critical and you are already calling Ollama directly.

## Getting started

### Deployment (Docker)

```bash
docker run \
  -v $(pwd)/litellm-config.yaml:/app/config.yaml \
  -p 4000:4000 \
  -e OPENROUTER_API_KEY="${OPENROUTER_API_KEY}" \
  -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
  -e LITELLM_MASTER_KEY="sk-your-master-key" \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml --detailed_debug
```

### Core Configuration (`litellm-config.yaml`)

```yaml
model_list:
  - model_name: llama3.2
    litellm_params:
      model: ollama/llama3.2
      api_base: http://192.168.0.5:30068
  - model_name: qwen2.5-coder-14b
    litellm_params:
      model: ollama/qwen2.5-coder:14b
      api_base: http://192.168.0.5:30068
  - model_name: claude-opus
    litellm_params:
      model: anthropic/claude-4-8-opus-20260528
      api_key: os.environ/ANTHROPIC_API_KEY

router_settings:
  routing_strategy: least-busy
  fallback_model: claude-opus
```

### Advanced Routing Patterns
Useful for favoring a cheaper or local instance while keeping a high-performance cloud instance as a hot standby.

```yaml
model_list:
  - model_name: coder-model
    litellm_params:
      model: ollama/qwen2.5-coder:14b
      api_base: http://local-gpu:11434
      priority: 1
  - model_name: coder-model
    litellm_params:
      model: anthropic/claude-4-8-opus-20260528
      priority: 2
```

### Integrating with OpenHands

```yaml
# docker-compose.yml snippet
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    volumes:
      - ./litellm.yaml:/app/config.yaml
    ports:
      - "4000:4000"
  openhands:
    image: docker.all-hands.dev/all-hands-ai/openhands:latest
    environment:
      LLM_BASE_URL: "http://litellm:4000"
      LLM_MODEL: "openai/qwen2.5-coder-14b"
```

## CLI examples
LiteLLM can be managed via its CLI for quick testing or server management:

```bash
# Start a proxy with a specific model directly
litellm --model ollama/llama3.2

# Check the version
litellm --version

# Run migrations for the database
litellm --migrate

# View logs
docker logs -f litellm
```

## API examples

### Virtual Key Generation
Virtual keys allow you to give different agents or users their own API keys with individual rate limits and budget caps.

```bash
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "openhands-agent",
    "max_budget": 5.0,
    "budget_duration": "monthly"
  }'
```

### Python SDK Usage
Unified call — same interface regardless of provider.

```python
import litellm

response = litellm.completion(
    model="claude-4-8-opus-20260528",
    messages=[{"role": "user", "content": "Explain RAG"}]
)

# Embeddings
embeddings = litellm.embedding(
    model="ollama/nomic-embed-text",
    input=["text to embed"],
    api_base="http://192.168.0.5:30068",
)
```

### Realtime & Memory APIs
LiteLLM provides a unified WebSocket interface for Realtime multimodal models and a Memory API for long-term state.

```python
# Memory API snippet
response = litellm.completion(
    model="gpt-5.5",
    messages=[{"role": "user", "content": "My favorite color is blue."}],
    user="jules-001",
    integrate_memory=True
)
```

### MCP Gateway
Securely expose Model Context Protocol (MCP) servers to your agents via the LiteLLM proxy.

```yaml
# litellm-config.yaml
mcp_servers:
  - name: "google-drive"
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-google-drive"]
```

### Guardrails & Security
LiteLLM can block or modify requests/responses to enforce PII masking and prevent prompt injection.

```yaml
# In litellm-config.yaml
litellm_settings:
  guardrails:
    - guardrail_name: "pii-masking"
      litellm_params:
        guardrail: "presidio"
        mode: "during_call"
```

**Security considerations:**
- **Master key**: Set `LITELLM_MASTER_KEY` via environment variable.
- **Virtual key rotation**: Revoke and regenerate agent keys periodically.
- **Network isolation**: Run the proxy on an internal Docker network.

## Related tools / concepts

- [OpenRouter](../tools/ai_knowledge/openrouter.md) — Cloud-based model router.
- [Ollama](ollama.md) — Local model serving backend.
- [OpenHands](../tools/development_ops/openhands.md) — Software engineering agent.
- [OpenClaw](../tools/development_ops/openclaw.md) — Agent platform.
- [Langfuse](../tools/process_understanding/langfuse.md) — Observability backend.
- [vLLM](../tools/infrastructure/vllm.md) — High-throughput inference engine.
- [Authentik](authentik.md) — For securing the LiteLLM UI.
- [Docker](../tools/infrastructure/docker.md) — Primary deployment method.
- [n8n](n8n.md) — For LLM-powered automation workflows.
- [Home Assistant](home-assistant.md) — For AI-driven home automation.

## Sources / references

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [GitHub — BerriAI/litellm](https://github.com/BerriAI/litellm)
- [LiteLLM Proxy Quick Start](https://docs.litellm.ai/docs/proxy/docker_quick_start)
- [Virtual Keys & Budgets](https://docs.litellm.ai/docs/proxy/virtual_keys)

## Backlog
- [x] Perform quarterly technical freshness audit (June 2026).
- [ ] Implement native MCP 3.0 tool routing.

## Contribution Metadata

- Last reviewed: 2026-06-18
- Confidence: high
