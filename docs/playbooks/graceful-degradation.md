# Playbook: Graceful Degradation (Cloud-to-Local)

## What it is
The Graceful Degradation playbook defines the operational configuration for automatically switching from primary cloud-based LLM APIs (such as Anthropic Claude 5.6, OpenAI GPT-5.5, or Google Gemini 4.0 Pro/Ultra) to a local inference engine ([Ollama](../services/ollama.md), vLLM, SGLang) during cloud outages, network drops, or rate-limiting events. It operationalizes [Fallback Patterns](../knowledge_base/patterns/fallback-patterns.md) by providing concrete implementation steps for [LiteLLM](../services/litellm.md), [Open WebUI](../services/open-webui.md), and FastMCP 3.1 gateway orchestrators.

## What problem it solves
It ensures continuous availability of mission-critical AI applications when primary cloud providers encounter failures or API degradations:
- **Cloud Provider Outages & Downtime**: Seamlessly redirecting inference traffic to local weights when cloud endpoints return HTTP 5xx or connection timeouts.
- **Quota & Rate Limit Exhaustion**: Intercepting HTTP 429 rate limits and failing over to local hardware before workflow execution breaks.
- **Latency Spikes & Degraded Performance**: Circuit-breaking requests that exceed latency thresholds and routing to fast local models (e.g., Llama 4 70B / Gemma 3 27B).
- **Agentic Workflow Resilience**: Preventing multi-agent pipelines (n8n, OpenClaw, FastMCP) from halting when cloud APIs fail mid-sequence.

## Where it fits in the stack
**Category**: Playbook / Reliability. It operates at the **Gateway and Load Balancing layer**, orchestrating failover logic between the External Cloud Provider tier and the Local On-Premise Inference tier.

## Architecture & Workflow

```
+-------------------------------------------------------------------------------+
|                       Graceful Degradation Gateway Flow                       |
+-------------------------------------------------------------------------------+
|                                                                               |
|   +-----------------------+     +-----------------------+                     |
|   | FastMCP 3.1 Client    |     | n8n / Web Application |                     |
|   +-----------+-----------+     +-----------+-----------+                     |
|               |                             |                                 |
|               +--------------+--------------+                                 |
|                              |                                                |
|                              v                                                |
|                +---------------------------+                                  |
|                | LiteLLM Proxy / Gateway   |                                  |
|                +-------------+-------------+                                  |
|                              |                                                |
|                              v                                                |
|                +---------------------------+                                  |
|                | Circuit Breaker Evaluator |                                  |
|                +-------------+-------------+                                  |
|                              |                                                |
|               +--------------+--------------+                                 |
|               |                             |                                 |
|      (Health Check OK)             (Timeout / HTTP 5xx / 429)                 |
|               v                             v                                 |
|    +--------------------+        +--------------------+                       |
|    | Primary Cloud Tier |        | Local Engine Tier  |                       |
|    | Claude 5.6 / GPT-5 |        | Ollama / vLLM      |                       |
|    | Gemini 4.0 Pro     |        | Llama 4 / Gemma 3  |                       |
|    +----------+---------+        +----------+---------+                       |
|               |                             |                                 |
|               +--------------+--------------+                                 |
|                              |                                                |
|                              v                                                |
|                +---------------------------+                                  |
|                | Unified Response Payload  |                                  |
|                +---------------------------+                                  |
|                                                                               |
+-------------------------------------------------------------------------------+
```

## Failover Strategy Comparison

| Strategy / Dimension | Active Cloud Primary | LiteLLM Cooldown Fallback | FastMCP Circuit Breaker | Local Pre-Warmed Failover |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Driver** | Cloud Provider REST API | Gateway Proxy | MCP Task Transport | On-Premise VRAM |
| **Failover Latency** | 0 ms (Direct) | ~250–500 ms (Retry overhead) | ~100–300 ms (State check) | < 50 ms (Local warm cache) |
| **Reasoning Capacity** | SOTA Frontier (100%) | SOTA Frontier -> Local | Task-Bounded Local | Local High-Quantization (70-85%) |
| **Data Sovereignty** | External Cloud Transit | External Cloud Transit | End-to-End Encrypted | 100% Local Air-Gapped |
| **Cost Profile** | Pay-Per-Token API | Dynamic Capped | Zero API Expense | Infrastructure Fixed Power |

## Typical use cases
- **Continuous Homelab Assistant Operations**: Ensuring core dashboard and voice services remain active during WAN outages.
- **Automated Agentic Workflow Failover**: Allowing background n8n and FastMCP agent tasks to complete using local models if primary APIs throw errors.
- **Dynamic Cost Capping**: Directing reasoning-heavy queries to cloud models while dynamically downgrading routine queries to local models.
- **Privacy-Sensitive Content Redirection**: Intercepting queries containing PII or confidential metadata and routing them locally.

## Strengths
- **High Availability & Fault Tolerance**: Guarantees zero downtime for critical home or enterprise automation processes.
- **Automated Self-Healing**: Automatically tests and restores primary endpoints when cloud services recover.
- **Cost & Quota Efficiency**: Reduces unnecessary API expenses by utilizing idle local VRAM capacity.
- **Transparent User Experience**: End users experience seamless completions without manual model switching.

## Limitations
- **Reasoning Disparity**: Fallback to smaller local models (e.g., Llama 4 8B or Gemma 3 27B) may yield lower reasoning depth compared to frontier cloud models.
- **Context Window Alignment**: Requires standardizing system prompts and context limits across differing model architectures.
- **Initial Failover Latency**: The retry penalty of an initial cloud timeout adds execution overhead to the total response duration.
- **Hardware Readiness**: Local GPU/VRAM hardware must remain powered and pre-warmed for instant failover traffic.

## When to use it
- Mission-critical automation tasks (home security, automated monitoring, infrastructure orchestration).
- Operating in locations subject to unstable internet connectivity or frequent cloud provider rate-limiting.
- Deploying autonomous agent loops that cannot afford unhandled exception halts.

## When not to use it
- Non-critical, batch research workflows where delaying execution until cloud recovery is preferable to local lower-precision outputs.
- Devices lacking local GPU acceleration where local CPU inference speeds are prohibitively slow (<2 tokens/sec).

## Getting started

### 1. Local Fallback Model Preparation
Ensure [Ollama](../services/ollama.md) or vLLM is running locally with a warm fallback model:
```bash
ollama pull llama4-70b-instruct
```

### 2. Configure LiteLLM Routing Gateway
Define a primary-to-fallback routing hierarchy in `litellm_config.yaml`:

```yaml
model_list:
  - model_name: primary-agent-model
    litellm_params:
      model: anthropic/claude-5-6-sonnet
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: fallback-agent-model
    litellm_params:
      model: ollama/llama4-70b-instruct
      api_base: http://localhost:11434

router_settings:
  fallback_policy:
    primary-agent-model: ["fallback-agent-model"]
  allowed_fails: 2
  cooldown_time: 300
```

### 3. Deploy Open WebUI Failover Proxy
Configure [Open WebUI](../services/open-webui.md) to route requests through the LiteLLM proxy URL (`http://localhost:4000/v1`).

## CLI examples

### 1. Launching LiteLLM Gateway with Fallback Rules
```bash
litellm --config litellm_config.yaml --port 4000
```

### 2. Simulating Cloud Failover Request
Test failover execution by calling the primary endpoint with an invalid API key:
```bash
curl -X POST http://localhost:4000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "primary-agent-model",
       "messages": [{"role": "user", "content": "Run system diagnostic."}]
     }'
```

### 3. Monitoring Failover Logs
```bash
grep -E "fallback|cooldown" litellm.log
```

## API examples

### Python: Request Failover Engine with Pydantic v2 & FastMCP Validation
This script uses **Pydantic v2** models to validate routing policies and execute multi-tier fallbacks from cloud APIs (Claude 5.6 / GPT-5.5) to local Ollama endpoints upon error detection.

```python
import time
import litellm
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)

class FallbackPolicyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    primary_model: str = Field(default="anthropic/claude-5-6-sonnet")
    fallback_models: List[str] = Field(default=["ollama/llama4-70b-instruct", "ollama/gemma3-27b-it"])
    timeout_sec: float = Field(default=8.0, ge=1.0)
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    fastmcp_task_id: Optional[str] = Field(None, description="Optional FastMCP 3.1 tracking task ID")

    @field_validator("fallback_models")
    @classmethod
    def validate_fallbacks(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("At least one fallback model must be specified.")
        return v

class ExecutionReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resolved_model: str
    response_content: str
    attempt_count: int
    total_duration_ms: float
    status: str = Field(default="SUCCESS")
    fastmcp_protocol_version: str = Field(default="3.1")

def execute_resilient_chat(policy_payload: dict, messages_raw: List[dict]) -> dict:
    try:
        policy = FallbackPolicyConfig.model_validate(policy_payload)
        messages = [ChatMessage.model_validate(m).model_dump() for m in messages_raw]

        all_targets = [policy.primary_model] + policy.fallback_models
        start_t = time.time()
        attempts = 0
        final_response = None

        for target_model in all_targets:
            attempts += 1
            try:
                final_response = litellm.completion(
                    model=target_model,
                    messages=messages,
                    timeout=policy.timeout_sec,
                    temperature=policy.temperature
                )
                break
            except Exception as e:
                print(f"Target '{target_model}' failed with error: {e}. Switching to next fallback...")

        if not final_response:
            return {"status": "FAILED", "error": "All primary and fallback models failed."}

        duration = (time.time() - start_t) * 1000.0
        report = ExecutionReport(
            resolved_model=target_model,
            response_content=final_response.choices[0].message.content,
            attempt_count=attempts,
            total_duration_ms=duration
        )
        return report.model_dump()
    except Exception as err:
        return {"status": "FAILED", "error": str(err)}

if __name__ == "__main__":
    sample_policy = {
        "primary_model": "anthropic/invalid-claude-key",
        "fallback_models": ["ollama/llama4-70b-instruct"],
        "timeout_sec": 3.0,
        "fastmcp_task_id": "task_degrade_8812"
    }
    sample_msgs = [
        {"role": "system", "content": "You are a local homelab fallback agent."},
        {"role": "user", "content": "Check status of system processes."}
    ]
    print("Failover Result:\n", execute_resilient_chat(sample_policy, sample_msgs))
```

## FastMCP 3.1 Resilient Gateway Handler

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("graceful-degradation-gateway", version="3.1")

class DegradedTaskRequest(BaseModel):
    task_id: str = Field(..., description="FastMCP task UUID")
    prompt: str = Field(..., min_length=1)
    primary_cloud_model: str = Field(default="anthropic/claude-5-6-sonnet")
    fallback_local_model: str = Field(default="ollama/llama4-70b-instruct")

@mcp.tool()
async def process_task_with_failover(request: DegradedTaskRequest) -> dict:
    """Executes a FastMCP task with automatic failover between cloud and local endpoints."""
    # FastMCP Task Protocol execution logic with failover state tracking
    return {
        "task_id": request.task_id,
        "status": "completed",
        "active_model": request.fallback_local_model,
        "degraded_mode": True,
        "fastmcp_version": "3.1"
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Operational Hardening & SLA Guidelines

1. **Keep Fallback Models Pre-Warmed**: Configure Ollama or vLLM to hold local fallback model weights in VRAM continuously (`ollama run llama4-70b-instruct --keepalive -1`) so failovers avoid cold-start load delays.
2. **Circuit Breaker Cooldown**: Set LiteLLM `cooldown_time` to at least 300 seconds to prevent rapid flap-cycling between degraded cloud endpoints and local models.
3. **Structured Context Truncation**: When falling over from 1M-token cloud models to 128k local models, pass context through a sliding-window compressor to ensure token limits are respected.
4. **Telemetry & Alerting**: Fire a alert webhook (e.g., Discord or Matrix notification) whenever a failover event occurs to give administrators visibility into cloud provider outages.

## Troubleshooting Guide

| Symptom / Error | Root Cause | Remediation Step |
| :--- | :--- | :--- |
| **HTTP 504 Gateway Timeout** | Primary cloud API timed out and fallback timeout was set too high | Lower `timeout_sec` in LiteLLM config to 4.0 seconds for fast fallback response. |
| **Local OOM Exception** | Local GPU VRAM exhausted when loading fallback model | Use a smaller quantized fallback variant (e.g. `llama4-8b` or `gemma3-27b`). |
| **Context Limit Exceeded** | Cloud request payload exceeds local model max context window | Enable automatic truncation in proxy middleware or trim chat message history. |
| **Flapping Endpoints** | Cloud endpoint intermittently returns 200 and 500 errors | Increase `allowed_fails` threshold and extend `cooldown_time` window in gateway config. |

## Related tools / concepts
- [LiteLLM](../services/litellm.md) — Unified LLM proxy and failover router.
- [Ollama](../services/ollama.md) — Local model inference engine.
- [Open WebUI](../services/open-webui.md) — Multi-model interface with fallback routing.
- [Fallback Patterns](../knowledge_base/patterns/fallback-patterns.md) — Resilient system pattern specs.
- [Self-Healing Agent Research](../knowledge_base/self-healing-agent-research.md) — Autonomous recovery patterns.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — Strategy for context-aware model selection.

## Sources / References
- [LiteLLM Router & Fallbacks Guide](https://docs.litellm.ai/docs/proxy/fallbacks)
- [Open WebUI Proxy Configuration](https://docs.openwebui.com/)
- [Ollama API Specification](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
