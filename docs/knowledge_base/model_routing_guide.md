# Model Routing Guide

## What it is
The Model Routing Guide is an architecture framework for selecting and dispatching requests to the optimal Large Language Model (LLM) or Vision-Language Model (VLM) based on early 2027 capability tiers. It provides source-backed decision logic considering cost, latency, reasoning depth (effort levels), context retention, and protocol compatibility across major model families (including FastMCP 3.1, Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, Gemma 3, and Qwen 3.8).

## Model Routing Pipeline Architecture

```
+-----------------------------------------------------------------------------------+
|                            Incoming User / Agent Request                          |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           Model Gateway Classifier Router                         |
|     (Analyzes Token Count, Tool Calling Needs, Security Level, & Latency Budget)  |
+-----------------------------------------------------------------------------------+
                                          |
         +--------------------------------+--------------------------------+
         |                                |                                |
         v                                v                                v
+------------------+             +------------------+             +------------------+
| Context > 500k?  |             |  High Reasoning? |             | Low-Cost Edge?   |
| (Gemini 4.0 Pro) |             | (GPT-5.6 / Opus) |             | (Qwen / Gemma 3) |
+------------------+             +------------------+             +------------------+
         |                                |                                |
         +--------------------------------+--------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Pydantic v2 Target Validation & Dispatch                   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                   Model Execution & Fallback Protection Circuit                   |
|                  (Fallback to Secondary Tier on Rate-Limit/Timeout)               |
+-----------------------------------------------------------------------------------+
```

## Capability Tiers & Model Selection Matrix (2027)

| Provider | Model Family | Key Capability Tiers | Best Fit Workloads | Cost Factor | Latency SLA |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Anthropic** | Claude 5.1 / 5.6 | Haiku (Speed), Sonnet (Balanced), Opus (Logic) | Multi-tool FastMCP orchestration, codebase engineering | Medium - High | Sub-500ms (Haiku) to 2s (Opus) |
| **OpenAI** | GPT-5.5 / 5.6 | Reasoning Effort Levels (None, Low, Med, High, Max) | Multi-step mathematical proofing, complex logic | High | Variable (Reasoning effort) |
| **Google** | Gemini 4.0 | Flash (Efficient), Pro (2M+ Context), Ultra | Ultra-large context ingestion, native video/audio RAG | Low - Medium | <300ms (Flash) |
| **DeepSeek** | DeepSeek-V4 | V4 R1 (Deep CoT), V4-Distill (Edge) | Math & code open weights, low-budget reasoning | Very Low | Fast streaming |
| **Meta** | Llama 4 | Llama 4-70B (Orchestration), Llama 4-405B | On-premise enterprise clusters, sovereign deployments | Compute cost only | Local hardware dependent |
| **Alibaba** | Qwen 3.8 | Qwen 3.8-72B / 32B | Self-hosted edge routing, fast IDE completion | Compute cost only | Low latency (<200ms) |
| **Google** | Gemma 3 | Gemma 3-27B / 12B / 4B | Privacy-preserving embedded local nodes | Free local | Extremely fast (<100ms) |

## What problem it solves
Frontier models in 2027 vary significantly in operational expense, execution latency, and token throughput. This guide prevents "over-allocation" (dispatching low-complexity tasks to high-cost frontier reasoning models like GPT-5.6 or Claude 5.6 Opus) and "under-allocation" (routing multi-step agentic workflows to low-tier models lacking tool schema adherence). It ensures token efficiency, cost control, and latency minimization across [Agentic Workflows](patterns/agentic-workflows.md).

## Where it fits in the stack
It functions at the **Decision & Gateway Layer** of the AI stack, informing [Autonomous Agents](../tools/agents/index.md) and orchestration gateways on which model endpoint to invoke for specific nodes in a computational graph. It integrates natively with FastMCP 3.1 and [Data Copilot MCP Tooling](patterns/data-copilot-mcp-tooling.md) for tool-aware, schema-verified routing.

## Typical use cases
- **Tiered Multi-Model Pipeline**: Routing incoming requests to a lightweight classifier model (Claude 5.1 Haiku or Gemma 3-12B) first, escalating to a high-reasoning model (GPT-5.6 High or Claude 5.6) only if complex reasoning is triggered.
- **Cost & Token Optimization**: Dynamic switching between [Gemini 4.0 Flash](../tools/ai_knowledge/gemini.md) for bulk document extraction and [Claude 5.6 Sonnet](../tools/ai_knowledge/claude.md) for multi-tool orchestration.
- **Latency-Critical Completion**: Routing editor inline completions or shell agent commands to local [Qwen 3.8](../tools/ai_knowledge/qwen.md) instances.
- **Ultra-Long Context Ingestion**: Routing 1M+ token repository ingests to Gemini 4.0 Pro or Ultra endpoints.

## Strengths
- **Granular Effort Tuning**: Leverages native reasoning effort settings (None, Low, Medium, High, Max) for precise latency vs. accuracy trade-offs.
- **Economic Efficiency**: Minimizes API costs by enforcing strict tier-based threshold routing.
- **Context-Aware Routing**: Evaluates context window requirements (up to 2M+ tokens) before dispatching to model backends.
- **FastMCP 3.1 Native Integration**: Utilizes tool definitions and Pydantic v2 schemas to validate routing criteria dynamically.

## Limitations
- **API Pricing Dynamics**: Token pricing fluctuates; live pricing should be verified via the [Pricing Matrix](api_pricing_free_tiers.md).
- **Subjective Routing Criteria**: Niche creative tasks or tone matching remain partially subjective and difficult to evaluate automatically.
- **Router Overhead**: Multi-tier routing code introduces minor network/decision overhead that must be offset by model-tier cost savings.

## When to use it
- When building multi-agent systems with strict compute, latency, and financial budget constraints.
- When refactoring monolithic single-model backends into modular multi-model pipelines.
- When configuring model routing for enterprise architectures like [Home Admin Agent Architecture](home-admin-agent-architecture.md).

## When not to use it
- For simple single-turn applications where throughput and token costs are negligible.
- If your system is legally or technically restricted to a single cloud provider or local model checkpoint.

## Getting started

### 1. Evaluate Task Complexity
Classify the task based on required context tokens, tool-calling complexity, and reasoning depth (None, Low, Medium, High, or Max).

### 2. Configure Model Gateway
Install a routing SDK or construct selection logic within your gateway pipeline:
```bash
npm install @ai-sdk/provider-utils
```

### 3. Establish Fallback Handlers
Incorporate resilient [Fallback Patterns](patterns/fallback-patterns.md) to automatically failover if a selected endpoint experiences rate limits or downtime.

## CLI examples

### CLI Model Selection & Query Dispatch
Using `model-router` CLI to select backends dynamically:

```bash
# Route a large repository refactoring task based on context size and FastMCP requirements
model-router "Refactor this 80-file codebase with FastMCP 3.1 tool hooks" --preference "context" --mcp-version "3.1"
# Target: Gemini 4.0 Pro / Claude 5.6 Sonnet

# Route a brief text summarization task for cost efficiency
model-router "Summarize this 2-page document" --preference "cost"
# Target: Claude 5.1 Haiku / Gemma 3-27B
```

## API examples

### FastMCP 3.1 Model Router Tool with Pydantic v2 Contracts
The following complete Python script implements a FastMCP 3.1 tool that acts as a production model router, using **Pydantic v2** validation to ensure schema-compliant dispatch decisions:

```python
import json
from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Router Server
mcp = FastMCP(
    name="Model-Routing-Gateway",
    instructions="FastMCP 3.1 model selection and gateway dispatch server."
)

class RoutingCriteria(BaseModel):
    task_description: str = Field(..., description="High-level prompt or problem summary")
    estimated_context_tokens: int = Field(default=1000, ge=0, description="Expected context payload size in tokens")
    reasoning_priority: Literal["low_latency", "cost_saving", "max_reasoning"] = Field(
        default="cost_saving",
        description="Primary optimization metric for routing"
    )
    requires_fastmcp_31: bool = Field(default=True, description="Whether tool execution requires FastMCP 3.1 support")
    max_budget_usd: float = Field(default=0.05, ge=0.0, description="Maximum allowable token budget for request")

class DispatchDecision(BaseModel):
    selected_provider: str = Field(..., description="Target model provider name")
    selected_model: str = Field(..., description="Canonical model identifier endpoint")
    reasoning_effort: Optional[str] = Field(None, description="Reasoning effort level (e.g., 'high', 'medium')")
    fallback_model: str = Field(..., description="Failover endpoint if primary model experiences downtime")
    estimated_cost_usd: float = Field(..., description="Estimated cost for processing request")

@mcp.tool()
def route_model_request(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates routing rules and dispatches prompt to optimal LLM backend.
    """
    try:
        criteria = RoutingCriteria.model_validate(raw_payload)

        # Context window override for long-context RAG
        if criteria.estimated_context_tokens > 500000:
            decision = DispatchDecision(
                selected_provider="google",
                selected_model="google/gemini-4.0-pro",
                reasoning_effort=None,
                fallback_model="anthropic/claude-5.6-sonnet",
                estimated_cost_usd=0.015
            )
            return {"status": "success", "decision": decision.model_dump()}

        # Maximum reasoning depth requirement
        if criteria.reasoning_priority == "max_reasoning":
            decision = DispatchDecision(
                selected_provider="openai",
                selected_model="openai/gpt-5.6",
                reasoning_effort="high",
                fallback_model="anthropic/claude-5.6-opus",
                estimated_cost_usd=0.045
            )
            return {"status": "success", "decision": decision.model_dump()}

        # Low latency tool calling requirement
        if criteria.reasoning_priority == "low_latency":
            selected = "anthropic/claude-5.1-haiku" if criteria.requires_fastmcp_31 else "qwen/qwen-3.8-32b-local"
            decision = DispatchDecision(
                selected_provider="anthropic" if criteria.requires_fastmcp_31 else "alibaba",
                selected_model=selected,
                reasoning_effort=None,
                fallback_model="google/gemini-4.0-flash",
                estimated_cost_usd=0.002
            )
            return {"status": "success", "decision": decision.model_dump()}

        # Standard balanced default routing
        decision = DispatchDecision(
            selected_provider="anthropic",
            selected_model="anthropic/claude-5.6-sonnet",
            reasoning_effort=None,
            fallback_model="google/gemini-4.0-flash",
            estimated_cost_usd=0.008
        )
        return {"status": "success", "decision": decision.model_dump()}

    except ValidationError as val_err:
        return {"status": "error", "error_type": "validation_error", "details": val_err.errors()}
    except Exception as ex:
        return {"status": "error", "error_type": "execution_error", "details": str(ex)}

if __name__ == "__main__":
    mcp.run()
```

## Production Hardening & Operational Rules

1. **Pre-Flight Context Sizing**: Always calculate token counts before invoking model APIs to prevent unexpected truncation or context overflow errors.
2. **Circuit Breaker Integration**: Implement automatic failover logic (swapping to fallback models) when a target model endpoint hits HTTP 429 (Rate Limit) or 5xx errors.
3. **Pydantic Contract Enforcement**: Validate both input payloads and model outputs against explicit Pydantic v2 schemas to ensure robust tool execution.
4. **Latency Budget Enforcement**: Apply per-tier HTTP timeouts (e.g., 2s for fast tier, 15s for high reasoning tier) to keep multi-agent pipelines responsive.

## Troubleshooting Matrix

| Issue / Symptom | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| **`Context Limit Exceeded Error`** | Request size exceeded model's maximum context window | Route requests >500k tokens to `google/gemini-4.0-pro` or break document into sub-chunks. |
| **`Tool Call Schema Mismatch`** | Model tier failed to output structured JSON conforming to tool schema | Upgrade routing rule to `claude-5.6-sonnet` or enforce FastMCP 3.1 constrained decoding. |
| **`High First Token Latency (TTFT)`** | Request sent to high reasoning tier (`gpt-5.6` max effort) for simple task | Lower `reasoning_priority` parameter to `low_latency` or use `claude-5.1-haiku`. |
| **`Primary Endpoint Rate-Limited (HTTP 429)`** | API quota exceeded on primary provider endpoint | Configure automatic failover to designated secondary provider in `DispatchDecision`. |

## Related tools / concepts
- [Model Comparison and Evaluation](model_comparison_and_evaluation.md) — Quantitative evaluation metrics.
- [API Pricing & Free Tier Matrix](api_pricing_free_tiers.md) — Live pricing data.
- [Agentic Workflows](patterns/agentic-workflows.md) — Multi-agent orchestration patterns.
- [Home Admin Agent Architecture](home-admin-agent-architecture.md) — Edge and cloud routing architecture.
- [FastMCP 3.1 Specification](patterns/tool-calling-and-mcp.md) — Tool integration standard.
- [Fallback Patterns](patterns/fallback-patterns.md) — Failover routing mechanisms.

## Sources / References
- [Anthropic Claude 5 Series Specifications](https://www.anthropic.com/news/claude-5-series)
- [OpenAI GPT-5.6 Reasoning Effort Documentation](https://openai.com/index/gpt-5-6-reasoning-effort/)
- [Google DeepMind Gemini 4.0 Architecture Details](https://deepmind.google/technologies/gemini/4-0/)
- [Model Context Protocol (FastMCP 3.1) Specification](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
