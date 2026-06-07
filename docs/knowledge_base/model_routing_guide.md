# Model Routing Guide

## What it is
The Model Routing Guide is a technical framework for selecting the optimal Large Language Model (LLM) for a given task. It provides source-backed decision logic based on capability tiers, reasoning effort levels, and task-specific performance.

## What problem it solves
Frontier models vary wildly in cost, latency, and reasoning depth. This guide prevents "over-engineering" (using a high-cost reasoning model for simple summaries) and "under-engineering" (using a low-latency model for complex logic), ensuring token-efficiency and cost-effectiveness across agentic workflows.

## Where it fits in the stack
It is the **Decision Layer** of the AI stack, informing the [Agentic Workflows](patterns/agentic-workflows.md) and [Home Admin Agent Architecture](home-admin-agent-architecture.md) on which model to invoke for specific nodes in a computational graph.

## Typical use cases
- **Multi-Model Orchestration**: Routing a user query to a cheap classifier first, then to a high-reasoning model only if complex logic is detected.
- **Cost Optimization**: Switching from GPT-4o to Claude 3.5 Haiku for high-volume extraction tasks to save 90% on API costs.
- **Latency-Critical Applications**: Selecting GPT-5.3 Codex for real-time code completion where sub-second response is mandatory.

## Strengths
- **Granular Control**: Leverages new frontier features like OpenAI's "Reasoning Effort" levels.
- **Cost-Efficient**: Explicitly identifies "low-latency, high-volume" tiers for bulk processing.
- **Source-Backed**: Decision logic is derived from official provider documentation and real-world benchmarks.

## Limitations
- **Dynamic Pricing**: While it identifies tiers, specific token costs change frequently and should be verified via the [Pricing Matrix](api_pricing_free_tiers.md).
- **Vibe-Dependent**: Some routing decisions (like "Creative Writing") remain subjective and depend on the specific tone required.

## When to use it
- When building autonomous agents that need to manage their own compute budget.
- When refactoring a monolithic LLM application into a more efficient multi-model pipeline.

## When not to use it
- For trivial, single-turn chat interfaces where cost and latency are not primary concerns.
- If your application is locked into a single model (e.g., due to strict enterprise compliance).

## Anthropic (Claude)

Anthropic models are categorized into three "tiers" of capability. Choosing the right tier depends on the complexity of the reasoning required.

| Tier | Model | Best For | Decision Logic |
| :--- | :--- | :--- | :--- |
| **Haiku** | Claude 3.5 Haiku | Low-latency, high-volume tasks | Use for basic extraction, classification, and simple summarization where speed is critical. |
| **Sonnet** | Claude 3.5 Sonnet | General knowledge work, coding, and tool use | The default choice for most agentic workflows. High intelligence with manageable latency. |
| **Opus** | Claude 3 Opus | Complex reasoning, large-scale strategy, and high-fidelity creative work | Use when Sonnet fails on extreme logic puzzles or when maximum creative "nuance" is required. |

## OpenAI

OpenAI's latest frontier models (starting with GPT-5.4) introduce explicit **Reasoning Effort** levels, allowing developers to trade time/compute for accuracy.

### GPT-5.4 Effort Levels

| Level | Latency | Reasoning Depth | Recommended Use Case |
| :--- | :--- | :--- | :--- |
| **None** | Ultra-low | Surface-level | Rapid document parsing, simple chat responses. |
| **Medium** | Moderate | Balanced | Standard coding tasks, multi-step tool orchestration. |
| **High** | High | Deep | Complex bug fixes, architecture reviews. |
| **X-High** | Very High | Maximum | Frontier scientific reasoning, high-stakes logic verification. |

### GPT-5.3 Codex Transition

GPT-5.4 incorporates the specialized coding strengths of **GPT-5.3-Codex**.
- **Legacy Decision**: If a workflow specifically requires the legacy Codex behavior (deterministic code completion), continue using GPT-5.3-Codex.
- **Modern Decision**: For agentic coding where the model must use tools and iterate, GPT-5.4 (at Medium/High effort) is the recommended successor.

## Task-Based Routing Summary

| Task Type | Recommended Model | Effort/Tier |
| :--- | :--- | :--- |
| **Simple Extraction** | Claude 3.5 Haiku | N/A |
| **Standard Coding** | Claude 3.5 Sonnet | N/A |
| **Complex Debugging** | GPT-5.4 | High / X-High |
| **Creative Writing** | Claude 3 Opus | N/A |
| **Agentic Tool Use** | Claude 3.5 Sonnet | N/A |
| **Document Summarization** | Claude 3.5 Haiku | N/A |
| **Rapid Code Completion** | GPT-5.3 Codex | N/A |

## Related tools / concepts
- [Model Comparison and Evaluation](model_comparison_and_evaluation.md)
- [Model Classes](model_classes.md)
- [API Pricing & Free Tier Matrix](api_pricing_free_tiers.md)
- [AI Tool Access Matrix](ai_tool_access_matrix.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [Home Admin Agent Architecture](home-admin-agent-architecture.md)
- [OpenAI](../tools/ai_knowledge/openai.md)
- [Claude](../tools/ai_knowledge/claude.md)
- [Gemini](../tools/ai_knowledge/gemini.md)

## Sources / References
- [Introducing GPT-5.4 (OpenAI)](https://openai.com/index/introducing-gpt-5-4/)
- [Claude 3.5 Model Family (Anthropic)](https://www.anthropic.com/news/claude-3-5-sonnet)
- [Gemini 1.5 Pro & Flash (Google)](https://deepmind.google/technologies/gemini/pro/)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
