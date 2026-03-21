# LiteLLM

## What it is

LiteLLM is an open-source AI Gateway (proxy server) and Python SDK that provides a unified OpenAI-compatible interface to 100+ LLM providers — OpenAI, Anthropic, Google Vertex AI, AWS Bedrock, Azure OpenAI, Ollama, and more. It sits between your agents and models, acting as a traffic controller with routing, fallbacks, budget enforcement, virtual keys, and observability built in.

**Backed by Y Combinator (W23).** MIT-licensed core; enterprise tier available.

## What problem it solves

When running multiple AI agents (OpenClaw, OpenHands, Aider, n8n AI nodes) against both local Ollama models and cloud providers, you quickly accumulate problems:

- Each tool has its own API format and SDK
- Secrets are scattered across configs
- There is no central cost tracking
- Provider outages cascade into agent failures
- Local Ollama models are not OpenAI-compatible by default for some tools

LiteLLM solves all of these by presenting a single OpenAI-compatible endpoint that any tool can target, while internally routing, falling back, tracking costs, and enforcing budgets.

## Where it fits in the stack

**Provider Routing / Abstraction Layer**. LiteLLM is typically the first hop after an agent makes an LLM API call.

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

## Deployment

### Docker (recommended)

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

### One-click cloud (for testing)

Deploy to Render or Railway with the official template — useful for a shared team proxy before self-hosting.

## Core configuration

### Full home-lab config (`litellm-config.yaml`)

```yaml
model_list:
  # ── Local Ollama (TrueNAS) ──────────────────────────────
  - model_name: llama3.2
    litellm_params:
      model: ollama/llama3.2
      api_base: http://192.168.0.5:30068
    model_info:
      max_tokens: 8192
      supports_function_calling: true

  - model_name: qwen2.5-coder-14b
    litellm_params:
      model: ollama/qwen2.5-coder:14b
      api_base: http://192.168.0.5:30068
    model_info:
      max_tokens: 32768
      supports_function_calling: true

  - model_name: nomic-embed
    litellm_params:
      model: ollama/nomic-embed-text
      api_base: http://192.168.0.5:30068

  # ── MacBook M4 Ollama ───────────────────────────────────
  - model_name: llama3.2-local
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434

  # ── Cloud Fallbacks ─────────────────────────────────────
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: openrouter-free
    litellm_params:
      model: openrouter/google/gemma-3-27b-it:free
      api_key: os.environ/OPENROUTER_API_KEY

router_settings:
  routing_strategy: least-busy
  fallback_model: openrouter-free
  allowed_fails: 2
  cooldown_time: 60       # seconds before retrying a failed model

litellm_settings:
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]
  request_timeout: 120

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: "postgresql://litellm:pass@localhost:5432/litellm"  # optional; enables UI + key management
```

## Virtual keys and budget management

Virtual keys allow you to give different agents or users their own API keys with individual rate limits and budget caps. All keys route through the same LiteLLM proxy but are tracked and limited independently.

```bash
# Create a virtual key for OpenHands with a $5/month budget
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "openhands-agent",
    "max_budget": 5.0,
    "budget_duration": "monthly",
    "models": ["qwen2.5-coder-14b", "claude-sonnet"],
    "rpm_limit": 60
  }'

# Create a key for OpenClaw with only local models
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key_alias": "openclaw-agent",
    "max_budget": 0,
    "models": ["llama3.2", "llama3.2-local"],
    "rpm_limit": 120
  }'
```

Agents then use their virtual key as the API key:

```bash
# OpenHands pointing at LiteLLM with its virtual key
export LLM_BASE_URL="http://192.168.0.5:4000"
export LLM_API_KEY="sk-openhands-virtual-key"
export LLM_MODEL="openai/qwen2.5-coder-14b"
```

## Guardrails

LiteLLM can block or modify requests/responses before they reach the model:

```yaml
# In litellm-config.yaml
litellm_settings:
  guardrails:
    - guardrail_name: "pii-masking"
      litellm_params:
        guardrail: "aporia"           # or "presidio" for local PII detection
        mode: "during_call"
        default_on: true

    - guardrail_name: "prompt-injection"
      litellm_params:
        guardrail: "lakera_guard"
        mode: "pre_call"
```

For purely local guardrails without third-party services, use the built-in content filter:

```yaml
litellm_settings:
  content_policy:
    outgoing:
      block_words: ["password", "api_key", "secret"]
    incoming:
      block_words: ["ignore previous instructions", "jailbreak"]
```

## Logging and observability

### Langfuse (recommended for home lab)

```yaml
litellm_settings:
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]

environment_variables:
  LANGFUSE_PUBLIC_KEY: "pk-lf-..."
  LANGFUSE_SECRET_KEY: "sk-lf-..."
  LANGFUSE_HOST: "http://192.168.0.5:3100"   # self-hosted Langfuse
```

### Prometheus metrics

```yaml
litellm_settings:
  success_callback: ["prometheus"]

# Metrics exposed at http://localhost:4000/metrics
# Track: litellm_requests_total, litellm_total_tokens, litellm_request_latency_seconds
```

## Management UI

LiteLLM ships a web UI (enabled when `database_url` is set in config):

- Accessible at `http://localhost:4000/ui`
- Login with master key credentials
- Manage virtual keys, view spend by key/model/day, set budgets, test models, view logs

```bash
# Start with UI enabled (requires PostgreSQL)
docker run \
  -e DATABASE_URL="postgresql://litellm:pass@postgres:5432/litellm" \
  -e LITELLM_MASTER_KEY="sk-master" \
  -p 4000:4000 \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml
```

## Python SDK (without proxy)

For scripts that don't need a persistent proxy:

```python
import litellm

# Unified call — same interface regardless of provider
response = litellm.completion(
    model="ollama/llama3.2",
    messages=[{"role": "user", "content": "Summarise this text..."}],
    api_base="http://192.168.0.5:30068",
)

# Streaming
for chunk in litellm.completion(
    model="anthropic/claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "Explain RAG"}],
    stream=True,
):
    print(chunk.choices[0].delta.content or "", end="")

# Embeddings
embeddings = litellm.embedding(
    model="ollama/nomic-embed-text",
    input=["text to embed"],
    api_base="http://192.168.0.5:30068",
)
```

## Supported endpoint types

LiteLLM proxies the full OpenAI API surface:

| Endpoint | Use |
|---|---|
| `/chat/completions` | Standard chat |
| `/completions` | Legacy text completion |
| `/embeddings` | Vector embeddings |
| `/images/generations` | Image generation (DALL-E compatible) |
| `/audio/transcriptions` | Whisper-compatible transcription |
| `/audio/speech` | TTS |
| `/batches` | Batch inference |
| `/rerank` | Document re-ranking (Cohere-compatible) |
| `/messages` | Anthropic Messages API passthrough |
| `/responses` | OpenAI Responses API |
| `/a2a` | Agent-to-agent protocol |

## Integrating with OpenHands

```bash
# docker-compose.yml — OpenHands + LiteLLM
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    volumes:
      - ./litellm.yaml:/app/config.yaml
    environment:
      LITELLM_MASTER_KEY: "${LITELLM_MASTER_KEY}"
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"
      OPENROUTER_API_KEY: "${OPENROUTER_API_KEY}"
    ports:
      - "4000:4000"
    command: --config /app/config.yaml

  openhands:
    image: docker.all-hands.dev/all-hands-ai/openhands:latest
    environment:
      LLM_BASE_URL: "http://litellm:4000"
      LLM_MODEL: "openai/qwen2.5-coder-14b"
      LLM_API_KEY: "${OPENHANDS_VIRTUAL_KEY}"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ~/.openhands-state:/.openhands-state
    ports:
      - "3000:3000"
    depends_on:
      - litellm
```

## Security considerations

- **Master key**: Set `LITELLM_MASTER_KEY` via environment variable; never hardcode in config
- **Virtual key rotation**: Revoke and regenerate agent keys periodically; each agent should have its own key
- **Secret management**: All provider API keys are loaded from environment; LiteLLM never writes them to disk
- **Network isolation**: Run the proxy on an internal Docker network; expose only port 4000 to trusted agents
- **Logging privacy**: Prompts and responses are logged to Langfuse/Prometheus; ensure your logging backend is on private infrastructure if requests contain sensitive data

## Strengths

- **Protocol normalisation**: Every agent speaks one language (OpenAI Chat Completions), regardless of backend
- **100+ provider support**: OpenAI, Anthropic, Ollama, Bedrock, Azure, Vertex AI, OpenRouter, Replicate, and more
- **Built-in fallbacks**: Automatic failover when a model is down or rate-limited
- **Cost tracking**: Per-key and per-model spend tracked in real time
- **Self-hostable**: Full control; no third-party telemetry
- **Management UI**: Visual key management and spend dashboard without external tooling
- **Embeddable**: Works as a long-running proxy or imported as a Python library

## Limitations

- **Operational overhead**: Adds a service to maintain; needs health checks and restart policies
- **PostgreSQL dependency**: Full UI + key persistence requires a Postgres instance
- **Feature parity gaps**: Not all provider-specific parameters are exposed; some advanced provider features require raw passthrough
- **Local-model latency**: Proxying through LiteLLM adds ~5–20 ms per call vs direct Ollama calls

## When to use it

- When running multiple AI agents with different LLM backends
- When you need a centralised place to track AI spend and enforce budgets
- For resilient systems that can survive provider outages via automatic fallback
- When tools only support OpenAI format but you want to use Ollama or Bedrock
- For team deployments where different people need different API key access levels

## When not to use it

- If you only ever use one provider and one agent (direct calls are simpler)
- For very simple, low-volume scripts where a proxy adds unnecessary complexity
- When sub-5 ms latency is critical and you are already calling Ollama directly

## Related tools / concepts

- [OpenRouter](../tools/ai_knowledge/openrouter.md) — cloud-based model router (alternative to LiteLLM proxy for cloud-only use)
- [Ollama](ollama.md) — local model serving backend
- [OpenHands](../tools/development_ops/openhands.md) — software engineering agent; recommended to pair with LiteLLM
- [OpenClaw](../tools/development_ops/openclaw.md) — agent platform; can use LiteLLM for model routing
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — overview of local model options
- [vLLM](../tools/infrastructure/vllm.md) — high-throughput alternative to Ollama for inference

## Sources / References

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [GitHub — BerriAI/litellm](https://github.com/BerriAI/litellm)
- [LiteLLM Proxy Quick Start](https://docs.litellm.ai/docs/proxy/docker_quick_start)
- [Virtual Keys & Budgets](https://docs.litellm.ai/docs/proxy/virtual_keys)
- [Supported Providers](https://docs.litellm.ai/docs/providers)

## Contribution Metadata

- Last reviewed: 2026-03-21
- Confidence: high
