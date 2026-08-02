# Model Routing Guide

## What it is
The Model Routing Guide is a technical framework for selecting the optimal Large Language Model (LLM) for a given task based on late October / November 2026 capability tiers. It provides source-backed decision logic considering cost, latency, reasoning depth (effort levels), and task-specific performance.

### Capability Tiers by Provider

| Provider | Model Family | Key Tiers / Features |
| :--- | :--- | :--- |
| **Anthropic** | Claude 5.1 | Haiku (Ultra-Speed), Sonnet (Balanced/Orchestration), Opus (Maximum Nuance & Logic) |
| **OpenAI** | GPT-5.5 | Reasoning Effort Levels (None, Low, Medium, High, Max) for precise logic control |
| **Google** | Gemini 4.0 | Flash (Efficient/High-volume), Pro (2M+ Context reasoning), Spark (Specialized edge/TUI) |
| **Meta** | Llama 4 | 70B (Orchestration & Tool calling), 405B (Distillation & High-fidelity logic) |
| **Alibaba** | Qwen 3.6 | Exceptional performance-to-size open weights, highly optimized for coding & local routing |
| **Google** | [Gemma 3](../tools/ai_knowledge/local_llms.md) | SOTA open weights for lightweight local routing on edge devices. |

## What problem it solves
Frontier models in late 2026 vary wildly in operational cost and reasoning capabilities. This guide prevents "over-engineering" (using a high-cost reasoning model like GPT-5.5 Max for simple summaries) and "under-engineering" (using a low-latency model for complex multi-step logical synthesis), ensuring token-efficiency, latency optimization, and cost-effectiveness across [Agentic Workflows](patterns/agentic-workflows.md).

## Where it fits in the stack
It is the **Decision Layer** of the AI stack, informing [Autonomous Agents](../tools/agents/README.md) and orchestration frameworks on which model to invoke for specific nodes in a computational graph. It integrates with [MCP 3.1](../tools/automation_orchestration/mcp.md) and FastMCP 3.1 for tool-aware, schema-verified routing.

## Typical use cases
- **Multi-Model Orchestration**: Routing a user query to an extremely cheap classifier (Claude 5.1 Haiku) first, then to a high-reasoning model (GPT-5.5 High) only if complex multi-step logic is requested.
- **Cost Optimization**: Dynamic switching between [Gemini 4.0 Flash](../tools/ai_knowledge/gemini.md) for high-volume structured extraction and [Claude 5.1 Sonnet](../tools/ai_knowledge/claude.md) for tool-intensive orchestration.
- **Latency-Critical Applications**: Selecting highly optimized [Qwen 3.6](../tools/ai_knowledge/qwen.md) local instances for sub-second terminal or editor completion.
- **Context-Heavy Analysis**: Routing to Gemini 4.0 Pro for 1M+ token ingestion and cross-reference tasks.

## Strengths
- **Granular Effort Control**: Leverages OpenAI's "Reasoning Effort" levels for precision accuracy vs. speed trade-offs.
- **Cost-Efficient**: Explicitly identifies the "Ultra-Low Latency" tier for high-volume preprocessing.
- **Context-Aware**: Routes based on required context window (up to 2M+ tokens for Gemini 4.0 Pro).
- **FastMCP 3.1 Compatibility**: Allows tool metadata and capability schemas to dictate routing targets dynamically.

## Limitations
- **Dynamic Pricing**: Specific token costs fluctuate; users should verify via the [Pricing Matrix](api_pricing_free_tiers.md).
- **Vibe-Dependent**: Some routing (e.g., "Creative Writing") remains subjective and dependent on specific model "personality."
- **Overhead**: Complex dynamic routing code adds execution latency, which must be offset by model-choice savings.

## When to use it
- When building autonomous agents that must manage a strict compute and token budget.
- When refactoring monolithic LLM applications into efficient multi-model pipelines.
- When selecting models for [Home Admin Agent Architecture](home-admin-agent-architecture.md).

## When not to use it
- For trivial, single-turn chat interfaces where latency and cost are negligible.
- If your application is locked into a single provider for compliance or security reasons.

## Getting started

### 1. Identify Task Complexity
Assess the task based on required context size and reasoning effort (None, Low, Medium, High, or Max).

### 2. Configure Your Router
Install a routing middleware or implement the selection logic in your application.
```bash
npm install @ai-sdk/provider-utils # Example for Vercel AI SDK routing
```

### 3. Set Fallbacks
Ensure [Fallback Patterns](patterns/fallback-patterns.md) are in place if the primary routed model fails.

## CLI examples

### Using a Router CLI (Late 2026)
```bash
# Route a task based on complexity and schema requirements
model-router "Refactor this 50-file repository" --preference "context" --mcp-version "3.1"
# Result: Routes to Gemini 4.0 Pro

model-router "Summarize this 1-page PDF" --preference "cost"
# Result: Routes to Claude 5.1 Haiku
```

## API examples

### Python Routing Logic with Pydantic v2 Validation
This script implements a tool-aware model selector utilizing FastMCP 3.1 schemas and Pydantic v2 for robust validation.

```python
from typing import Literal, Optional
from pydantic import BaseModel, Field, conint

class RoutingRequest(BaseModel):
    task_description: str = Field(..., description="The main description of the task to run")
    estimated_context_tokens: conint(ge=0) = Field(default=1000, description="The expected size of input context")
    reasoning_priority: Literal["low_latency", "cost_saving", "max_reasoning"] = Field(
        default="cost_saving",
        description="Priority driver for the decision logic"
    )
    requires_mcp_v31: bool = Field(default=True, description="Whether MCP 3.1 compliance is required")

class ModelRoutingDecision(BaseModel):
    selected_model: str = Field(..., description="The canonical identifier of the recommended model")
    reasoning_effort: Optional[str] = Field(None, description="The reasoning effort config (e.g., 'medium' for GPT-5.5)")
    estimated_cost_multiplier: float = Field(..., description="Approximate relative cost factor")

def determine_optimal_route(request: RoutingRequest) -> ModelRoutingDecision:
    # High context overrides all other preferences
    if request.estimated_context_tokens > 500000:
        return ModelRoutingDecision(
            selected_model="gemini-4.0-pro",
            reasoning_effort=None,
            estimated_cost_multiplier=0.4
        )

    if request.reasoning_priority == "max_reasoning":
        return ModelRoutingDecision(
            selected_model="gpt-5.5",
            reasoning_effort="high",
            estimated_cost_multiplier=1.0
        )

    if request.reasoning_priority == "low_latency":
        if request.requires_mcp_v31:
            return ModelRoutingDecision(
                selected_model="claude-5.1-haiku",
                reasoning_effort=None,
                estimated_cost_multiplier=0.1
            )
        else:
            return ModelRoutingDecision(
                selected_model="qwen-3.6-35b-local",
                reasoning_effort=None,
                estimated_cost_multiplier=0.0
            )

    # Default to balanced sonnet routing
    return ModelRoutingDecision(
        selected_model="claude-5.1-sonnet",
        reasoning_effort=None,
        estimated_cost_multiplier=0.3
    )

# Validate incoming routing request and make decision
raw_input = {
    "task_description": "Validate 10,000 JSON entries against a Pydantic v2 schema",
    "estimated_context_tokens": 120000,
    "reasoning_priority": "low_latency",
    "requires_mcp_v31": True
}

request = RoutingRequest.model_validate(raw_input)
decision = determine_optimal_route(request)
print(f"Optimal model: {decision.selected_model} (Relative cost factor: {decision.estimated_cost_multiplier})")
```

## Related tools / concepts
- [Model Comparison and Evaluation](model_comparison_and_evaluation.md)
- [API Pricing & Free Tier Matrix](api_pricing_free_tiers.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [Home Admin Agent Architecture](home-admin-agent-architecture.md)
- [Claude](../tools/ai_knowledge/claude.md)
- [OpenAI](../tools/ai_knowledge/openai.md)
- [Gemini](../tools/ai_knowledge/gemini.md)
- [MCP 3.1](../tools/automation_orchestration/mcp.md)
- [Fallback Patterns](patterns/fallback-patterns.md)

## Sources / References
- [Anthropic Claude 5.1 Technical Roadmap](https://www.anthropic.com/news/claude-5-1)
- [OpenAI GPT-5.5 Dynamic Reasoning Effort Manual](https://openai.com/index/gpt-5-5-reasoning-effort/)
- [Google DeepMind - Gemini 4.0 Architecture Details](https://deepmind.google/technologies/gemini/4-0/)
- [Model Context Protocol 3.1 Specification](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2026-11-20
- Confidence: high
