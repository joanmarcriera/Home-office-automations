# Model Routing Guide

## What it is
The Model Routing Guide is an architecture framework for selecting and dispatching requests to the optimal Large Language Model (LLM) or Vision-Language Model (VLM) based on early 2027 capability tiers. It provides source-backed decision logic considering cost, latency, reasoning depth (effort levels), context retention, and protocol compatibility across major model families (including FastMCP 3.1, Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, Gemma 3, and Qwen 3.8).

### Capability Tiers by Provider (2027)

| Provider | Model Family | Key Tiers / Features | Primary Routing Target |
| :--- | :--- | :--- | :--- |
| **Anthropic** | Claude 5.1 / 5.6 | Haiku (Ultra-Speed/Low-Cost), Sonnet (Balanced/Orchestration), Opus (Maximum Logic) | Multi-tool FastMCP orchestration, complex coding |
| **OpenAI** | GPT-5.5 / 5.6 | Reasoning Effort Levels (None, Low, Medium, High, Max) & o5 reasoning series | Extended logical proofing, mathematical reasoning |
| **Google** | Gemini 4.0 | Flash (Efficient/High-volume), Pro (2M+ Context), Ultra (Frontier multimodal) | Ultra-large context ingestion, multimodal video/audio |
| **DeepSeek** | DeepSeek-V4 | V4 R1 (Deep CoT Reasoning), V4-Distill (Lightweight local) | Math/Coding open weights, budget reasoning |
| **Meta** | Llama 4 | Llama 4-70B (Orchestration & Tool calling), Llama 4-405B (High-fidelity logic) | On-premise enterprise deployments, open reasoning |
| **Alibaba** | Qwen 3.8 | Qwen 3.8-72B / 32B (Exceptional coding & math open weights) | Self-hosted edge routing, fast IDE completions |
| **Google** | Gemma 3 | Gemma 3-27B / 12B / 4B (SOTA open-weights edge) | Embedded local devices, privacy-sensitive local agent nodes |

## What problem it solves
Frontier models in 2027 vary significantly in operational expense, execution latency, and token throughput. This guide prevents "over-allocation" (dispatching low-complexity tasks to high-cost frontier reasoning models like GPT-5.6 or Claude 5.6 Opus) and "under-allocation" (routing multi-step agentic workflows to low-tier models lacking tool schema adherence). It ensures token efficiency, cost control, and latency minimization across [Agentic Workflows](patterns/agentic-workflows.md).

## Where it fits in the stack
It functions at the **Decision & Gateway Layer** of the AI stack, informing [Autonomous Agents](../tools/agents/README.md) and orchestration gateways on which model endpoint to invoke for specific nodes in a computational graph. It integrates natively with FastMCP 3.1 and [Data Copilot MCP Tooling](patterns/data-copilot-mcp-tooling.md) for tool-aware, schema-verified routing.

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

### Python Routing Logic with FastMCP 3.1 & Pydantic v2 Validation
This example demonstrates a tool-aware model router utilizing FastMCP 3.1 schemas and Pydantic v2 validation:

```python
from typing import Literal, Optional
from pydantic import BaseModel, Field, conint

class RoutingRequest(BaseModel):
    """Pydantic v2 schema for incoming routing decision requests."""
    task_description: str = Field(..., description="Description of the task to be processed.")
    estimated_context_tokens: conint(ge=0) = Field(default=1000, description="Expected input context size in tokens.")
    reasoning_priority: Literal["low_latency", "cost_saving", "max_reasoning"] = Field(
        default="cost_saving",
        description="Primary optimization driver for model selection."
    )
    requires_fastmcp_31: bool = Field(default=True, description="Whether FastMCP 3.1 tool compliance is required.")

class ModelRoutingDecision(BaseModel):
    """Pydantic v2 schema for validated routing outputs."""
    selected_model: str = Field(..., description="Canonical provider model identifier.")
    reasoning_effort: Optional[str] = Field(None, description="Reasoning effort parameter (e.g. 'high' for GPT-5.6).")
    estimated_cost_multiplier: float = Field(..., description="Relative cost factor relative to baseline.")

def determine_optimal_route(request: RoutingRequest) -> ModelRoutingDecision:
    # Context window override for long-context tasks
    if request.estimated_context_tokens > 500000:
        return ModelRoutingDecision(
            selected_model="google/gemini-4.0-pro",
            reasoning_effort=None,
            estimated_cost_multiplier=0.35
        )

    if request.reasoning_priority == "max_reasoning":
        return ModelRoutingDecision(
            selected_model="openai/gpt-5.6",
            reasoning_effort="high",
            estimated_cost_multiplier=1.0
        )

    if request.reasoning_priority == "low_latency":
        if request.requires_fastmcp_31:
            return ModelRoutingDecision(
                selected_model="anthropic/claude-5.1-haiku",
                reasoning_effort=None,
                estimated_cost_multiplier=0.10
            )
        else:
            return ModelRoutingDecision(
                selected_model="qwen/qwen-3.8-32b-local",
                reasoning_effort=None,
                estimated_cost_multiplier=0.02
            )

    # Default balanced orchestration routing
    return ModelRoutingDecision(
        selected_model="anthropic/claude-5.6-sonnet",
        reasoning_effort=None,
        estimated_cost_multiplier=0.30
    )

# Validate input request and compute routing decision
raw_payload = {
    "task_description": "Execute schema validation on 50,000 logs using FastMCP 3.1",
    "estimated_context_tokens": 150000,
    "reasoning_priority": "low_latency",
    "requires_fastmcp_31": True
}

request_obj = RoutingRequest.model_validate(raw_payload)
decision_obj = determine_optimal_route(request_obj)
print(f"Routed Model Endpoint: {decision_obj.selected_model}")
print(f"Cost Multiplier: {decision_obj.estimated_cost_multiplier:.2f}")
```

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
