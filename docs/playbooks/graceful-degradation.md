# Playbook: Graceful Degradation (Cloud-to-Local)

## What it is
The Graceful Degradation playbook defines the operational configuration for automatically switching from cloud-based LLM APIs (such as Anthropic Claude 5.1/5.6, OpenAI GPT-5.5/5.6, or Google Gemini 4.0 Pro/Ultra) to a local inference engine ([Ollama](../services/ollama.md) or vLLM) during outages, rate-limiting, or connectivity issues. It operationalizes the [Fallback Patterns](../knowledge_base/patterns/fallback-patterns.md) by providing concrete implementation steps for [LiteLLM](../services/litellm.md) and [Open WebUI](../services/open-webui.md).

## What problem it solves
It ensures the continuity of mission-critical AI services when primary cloud providers fail. It solves for:
- **Provider Downtime**: Automatically switching to local models when a 5xx error or rate limit is received.
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
- **Quality Disparity**: Local models (e.g., Llama 4 70B, Gemma 3 27B) may not match the reasoning depth of frontier models (Claude 5.1/5.6 or GPT-5.5).
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

### Python: Request with Explicit Fallback Logic using Pydantic v2
The following script utilizes **Pydantic v2** validation to define failover policies and execute client requests with structured fallbacks and strict logging.

```python
import time
import litellm
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)

class FailoverConfig(BaseModel):
    models: List[str] = Field(..., min_items=1)
    timeout_seconds: float = Field(default=10.0, ge=1.0)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

class FailoverResult(BaseModel):
    selected_model: str
    response_text: str
    attempts: int
    elapsed_time_ms: float

def execute_with_fallback(config_payload: dict, messages_payload: List[dict]) -> dict:
    # Validate configuration and messages using Pydantic v2
    config = FailoverConfig.model_validate(config_payload)
    messages = [Message.model_validate(m) for m in messages_payload]

    start_time = time.time()
    response = None
    attempts = 0

    for model in config.models:
        attempts += 1
        try:
            print(f"Attempting completion with model: {model}")
            response = litellm.completion(
                model=model,
                messages=[m.model_dump() for m in messages],
                timeout=config.timeout_seconds,
                temperature=config.temperature
            )
            # If successful, break out of loop
            break
        except Exception as e:
            print(f"⚠️ Model {model} failed with error: {e}. Trying next fallback...")

    if not response:
        raise RuntimeError("All configured models in the failover chain failed.")

    elapsed = (time.time() - start_time) * 1000.0

    # Formulate and validate response using Pydantic v2
    result = FailoverResult(
        selected_model=model,
        response_text=response.choices[0].message.content,
        attempts=attempts,
        elapsed_time_ms=elapsed
    )

    return result.model_dump()

# Execution Example
if __name__ == "__main__":
    # Test fallback sequence: first is invalid cloud name to force fallback to local Ollama
    test_config = {
        "models": ["anthropic/invalid-model-name", "ollama/gemma3-27b-it"],
        "timeout_seconds": 5.0,
        "temperature": 0.2
    }

    test_messages = [
        {"role": "system", "content": "You are a local homelab fallback agent."},
        {"role": "user", "content": "Ping? Is local server functional?"}
    ]

    try:
        outcome = execute_with_fallback(test_config, test_messages)
        print("Validated Failover Result:", outcome)
    except Exception as e:
        print("Failover Sequence Failed:", e)
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
- Last reviewed: 2027-01-07
- Confidence: high
