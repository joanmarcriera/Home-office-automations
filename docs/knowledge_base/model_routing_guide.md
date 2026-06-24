# Model Routing Guide

## What it is
The Model Routing Guide is a technical framework for selecting the optimal Large Language Model (LLM) for a given task based on June 2026 capability tiers. It provides source-backed decision logic considering cost, latency, reasoning depth (effort levels), and task-specific performance.

## What problem it solves
Frontier models in 2026 vary wildly in operational cost and reasoning capabilities. This guide prevents "over-engineering" (using a high-cost reasoning model like GPT-5.5 for simple summaries) and "under-engineering" (using a low-latency model for complex multi-step logic), ensuring token-efficiency and cost-effectiveness across [Agentic Workflows](patterns/agentic-workflows.md).

## Where it fits in the stack
It is the **Decision Layer** of the AI stack, informing [Autonomous Agents](../tools/agents/README.md) and orchestration frameworks on which model to invoke for specific nodes in a computational graph.

## Typical use cases
- **Multi-Model Orchestration**: Routing a user query to a cheap classifier (Claude 4.8 Haiku) first, then to a high-reasoning model (GPT-5.5) only if complex logic is required.
- **Cost Optimization**: Dynamic switching between [Gemini 3.5 Flash](../tools/ai_knowledge/gemini.md) for high-volume extraction and [Claude 4.8 Sonnet](../tools/ai_knowledge/claude.md) for tool-intensive orchestration.
- **Latency-Critical Applications**: Selecting [GPT-5.3 Codex Transition](../tools/development_ops/codex.md) for sub-second code completion.

## Strengths
- **Granular Effort Control**: Leverages OpenAI's "Reasoning Effort" levels for precision accuracy vs. speed trade-offs.
- **Cost-Efficient**: Explicitly identifies the "Ultra-Low Latency" tier for high-volume preprocessing.
- **Context-Aware**: Routes based on the required context window (up to 2M+ tokens for Gemini).

## Limitations
- **Dynamic Pricing**: Specific token costs fluctuate; users should verify via the [Pricing Matrix](api_pricing_free_tiers.md).
- **Vibe-Dependent**: Some routing (e.g., "Creative Writing") remains subjective and dependent on specific model "personality."

## When to use it
- When building autonomous agents that must manage a compute budget.
- When refactoring monolithic LLM applications into efficient multi-model pipelines.
- When selecting models for [Home Admin Agent Architecture](home-admin-agent-architecture.md).

## When not to use it
- For trivial, single-turn chat interfaces where latency and cost are negligible.
- If your application is locked into a single provider for compliance or security reasons.

## Anthropic (Claude 4.8)

Anthropic categorizes its models into three tiers. Choosing the right tier depends on the complexity of the reasoning and required nuance.

| Tier | Model | Best For | Decision Logic |
| :--- | :--- | :--- | :--- |
| **Haiku** | Claude 4.8 Haiku | High-volume, low-latency | Use for classification, basic extraction, and initial query triage. |
| **Sonnet** | Claude 4.8 Sonnet | General knowledge work, coding | The default choice for tool-calling and agentic orchestration. |
| **Opus** | Claude 4.8 Opus | Deep reasoning, creative nuance | Use for high-stakes strategy, complex logic, and high-fidelity writing. |

## OpenAI (GPT-5.5)

GPT-5.5 introduces explicit **Reasoning Effort** levels, allowing developers to trade compute time for accuracy.

| Level | Latency | Reasoning Depth | Recommended Use Case |
| :--- | :--- | :--- | :--- |
| **None** | Ultra-low | Surface-level | Rapid parsing, simple chat, high-speed classification. |
| **Medium** | Moderate | Balanced | Standard coding, multi-step tool orchestration. |
| **High** | High | Deep | Complex bug fixes, architectural reviews, logic verification. |
| **X-High** | Very High | Maximum | Frontier scientific reasoning, high-stakes logic puzzles. |

## Google (Gemini 3.5)

Gemini excels in multimodal tasks and massive context handling.

| Model | Key Strength | Best For |
| :--- | :--- | :--- |
| **Gemini 3.5 Flash** | Speed & Efficiency | High-volume multimodal extraction and summarization. |
| **Gemini 3.5 Pro** | 2M+ Context Window | Ingesting entire repositories or long-form video for analysis. |
| **Gemini Spark** | Autonomous Missions | Small, fast, specialized tasks within the Google ecosystem. |

## CLI examples

### Using a Router CLI (Hypothetical June 2026)
```bash
# Route a task based on complexity
model-router "Refactor this 50-file repository" --preference "context"
# Result: Routes to Gemini 3.5 Pro

model-router "Summarize this 1-page PDF" --preference "cost"
# Result: Routes to Claude 4.8 Haiku
```

## API examples

### Python Routing Logic
```python
def get_model_for_task(task_complexity, context_size):
    if context_size > 500000:
        return "gemini-3.5-pro"
    if task_complexity == "high":
        return "gpt-5.5-high-effort"
    return "claude-4.8-sonnet"

model = get_model_for_task("high", 1000)
print(f"Routing to: {model}")
```

## Related tools / concepts
- [Model Comparison and Evaluation](model_comparison_and_evaluation.md)
- [API Pricing & Free Tier Matrix](api_pricing_free_tiers.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [Home Admin Agent Architecture](home-admin-agent-architecture.md)
- [Claude](../tools/ai_knowledge/claude.md)
- [OpenAI](../tools/ai_knowledge/openai.md)
- [Gemini](../tools/ai_knowledge/gemini.md)
- [MCP 3.0](../tools/automation_orchestration/mcp.md)
- [Fallback Patterns](patterns/fallback-patterns.md)

## Sources / References
- [Anthropic Claude 4.8 Announcement](https://www.anthropic.com/news/claude-4-8)
- [OpenAI GPT-5.5 Effort Levels Guide](https://openai.com/index/gpt-5-5-reasoning-effort/)
- [Google DeepMind - Gemini 3.5 Capabilities](https://deepmind.google/technologies/gemini/3-5/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
