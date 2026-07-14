# Playbook: Graceful Degradation (Cloud-to-Local)

## What it is
The Graceful Degradation playbook defines the operational configuration for automatically switching from cloud-based LLM APIs (Anthropic, OpenAI) to a local inference engine ([Ollama](../services/ollama.md)) during outages, rate-limiting, or connectivity issues. It operationalizes the [Fallback Patterns](../knowledge_base/patterns/fallback-patterns.md) by providing concrete implementation steps for [LiteLLM](../services/litellm.md) and [Open WebUI](../services/open-webui.md).

## What problem it solves
It ensures the continuity of mission-critical AI services when primary cloud providers fail. It solves for:
- **Provider Downtime**: Automatically switching to local models when a 5xx error is received.
- **Rate Limit Exhaustion**: Routing traffic to local hardware when cloud quotas are exceeded.
- **Latency Spikes**: Falling back to a local model if a cloud response takes longer than a defined threshold.
- **"Agentic Deadlocks"**: Preventing workflow failure when a specific cloud model is unavailable.

## Where it fits in the stack
**Category**: Playbook / Reliability. It sits at the **Gateway and Routing layer**, acting as the logic that controls traffic flow between the Cloud Provider layer and the Local Infrastructure layer.

## Typical use cases
- **Always-Available Assistant**: Ensuring your home dashboard remains responsive even if the internet is down.
- **Critical Automation Failover**: Allowing n8n workflows to complete sensitive tasks using local models if primary APIs fail.
- **Cost-Capped Research**: Using cloud models for complex reasoning but falling back to local models for simpler, high-volume tasks.
- **Privacy Escalation**: Manually or automatically routing sensitive queries to local models based on content detection.

## Strengths
- **Resilience**: Applications remain functional during major cloud outages.
- **Autonomy**: High degree of self-healing without human intervention.
- **Cost Optimization**: Can be configured to prefer local models for specific workloads.
- **Seamless Transition**: Users often don't notice the failover occurring in the background.

## Limitations
- **Quality Disparity**: Local models (e.g., Llama 3 8B) may not match the reasoning depth of frontier models (Claude 4.8).
- **State Management**: Ensuring the conversation history is correctly transferred between different model architectures.
- **Latency Overhead**: The initial failed request adds to the total response time.
- **Hardware Demand**: Local hardware must be kept in a "ready" state to accept failover traffic.

## When to use it
- For mission-critical home automation tasks (security, climate control).
- When operating in regions with unstable internet connectivity.
- When working with providers that have restrictive Tier 1 rate limits.

## When not to use it
- For tasks where the highest level of reasoning is strictly required and local models cannot suffice.
- If local hardware is insufficient to run fallback models at usable speeds.
- For non-critical, latency-insensitive research where a manual retry later is acceptable.

## Getting started

### 1. Local Fallback Preparation
Ensure [Ollama](../services/ollama.md) is running and a capable fallback model is pulled:
```bash
ollama pull gemma3-27b-it
```

### 2. Configure LiteLLM Gateway
Create a `config.yaml` for [LiteLLM](../services/litellm.md) that includes both cloud and local targets:

```yaml
model_list:
  - model_name: frontier-model
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20240620
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: fallback-model
    litellm_params:
      model: ollama/gemma3-27b-it
      api_base: http://localhost:11434

router_settings:
  fallback_policy:
    frontier-model: ["fallback-model"]
```

### 3. Deploy Open WebUI Failover
In [Open WebUI](../services/open-webui.md), add the LiteLLM proxy as the primary OpenAI-compatible connection.

## CLI examples

### 1. Starting LiteLLM with Fallback
```bash
litellm --config config.yaml --port 4000
```

### 2. Testing Failover (Simulated)
Temporarily invalidate your cloud API key and run:
```bash
curl -X POST http://localhost:4000/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "frontier-model",
       "messages": [{"role": "user", "content": "Status report."}]
     }'
```

### 3. Monitoring Failover Events
```bash
grep "fallback" litellm.log
```

## API examples

### Python: Request with Explicit Fallback Logic
```python
import litellm

# Define the models
models = ["anthropic/claude-3-5-sonnet", "ollama/gemma3-27b-it"]

response = None
for model in models:
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": "Is the local server running?"}],
            timeout=10 # Fallback if cloud takes > 10s
        )
        break
    except Exception as e:
        print(f"Model {model} failed, trying next...")

print(response.choices[0].message.content)
```

## Related tools / concepts
- [LiteLLM](../services/litellm.md) — The primary routing engine.
- [Ollama](../services/ollama.md) — Local inference target.
- [Open WebUI](../services/open-webui.md) — Front-end support for model switching.
- [Fallback Patterns](../knowledge_base/patterns/fallback-patterns.md) — Theoretical framework.
- [Self-Healing Agent Research](../knowledge_base/self-healing-agent-research.md) — Advanced failover logic.
- [Model Routing Guide](../knowledge_base/model_routing_guide.md) — Strategy for selection.
- [n8n Error Handling](../knowledge_base/patterns/n8n-error-handling.md) — Workflow level fallbacks.

## Sources / References
- [LiteLLM Fallback Documentation](https://docs.litellm.ai/docs/proxy/fallbacks)
- [Open WebUI Model Management](https://docs.openwebui.com/features/model-management/)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
