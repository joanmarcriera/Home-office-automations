# Model Routing Guide

This guide provides source-backed decision logic for selecting the optimal model and configuration for specific task types, balancing latency, cost, and reasoning depth.

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

## Related Concepts
- [Model Comparison and Evaluation](model_comparison_and_evaluation.md)
- [Model Classes](model_classes.md)
- [API Pricing & Free Tier Matrix](api_pricing_free_tiers.md)

## Sources / References
- [Introducing GPT-5.4 (OpenAI)](https://openai.com/index/introducing-gpt-5-4/)
- [Claude 3.5 Model Family (Anthropic)](https://www.anthropic.com/news/claude-3-5-sonnet)

## Contribution Metadata
- Last reviewed: 2026-04-20
- Confidence: high
