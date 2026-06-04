# Glaive

## What it is
Glaive is an AI platform specialized in generating high-quality synthetic data for training and fine-tuning Small Language Models (SLMs) and agentic systems. It focuses on creating datasets that improve a model's ability to use tools, call APIs, and reason through complex, multi-step tasks, which are critical capabilities for autonomous agents.

## What problem it solves
Generic synthetic data generation often fails to capture the nuances of real-world tool use and API interactions. Glaive addresses this by:
- **Generating Functional Data**: Creating datasets that specifically target function calling and structured output.
- **Improving SLM Performance**: Enabling smaller, more efficient models to punch above their weight in agentic workflows.
- **Reducing Dependency on Frontier Models**: Providing a way to distill the reasoning capabilities of large models into smaller, more cost-effective specialized models.

## Where it fits in the stack
Glaive sits in the **AI & Knowledge/Synthetic-Data** layer. It provides the high-quality training signals used to adapt base models for agentic behavior, often being paired with fine-tuning tools like [Unsloth](../infrastructure/unsloth.md) or [LLaMA Factory](../frameworks/llama-factory.md).

## Typical use cases
- **Agentic Tool-Use Training**: Generating datasets of natural language prompts followed by correct tool calls (JSON/Python).
- **Function Calling Distillation**: Training a 7B or 8B model to be as reliable at function calling as GPT-4o.
- **Multi-Step Reasoning**: Creating synthetic examples of "Chain of Thought" reasoning for complex problem solving.
- **API Sandbox Data**: Generating realistic API responses and error states to train models on robust error handling.

## Strengths
- **Focus on Agents**: Specifically designed for the agentic and tool-use era of AI.
- **High Quality & Diversity**: Uses sophisticated techniques to ensure synthetic data is varied and accurate.
- **SLM Optimization**: Particularly effective at making smaller models usable in production agent stacks.
- **Structured Output Mastery**: Helps models learn to strictly adhere to complex JSON schemas.

## Limitations
- **Platform Dependent**: Unlike local tools like [distilabel](../frameworks/distilabel.md), Glaive is often used as a managed platform/service.
- **Niche Focus**: Less focused on broad general-purpose chat data compared to frameworks like [LLaMA Factory](../frameworks/llama-factory.md).
- **Black Box Generation**: The internal generation logic may be less transparent than fully open-source pipeline tools.

## When to use it
- When you are building an autonomous agent and need it to be reliable at tool calling.
- When you want to use a small model (e.g., Llama 3 8B or Phi-3) for complex API orchestration.
- When you have a specific set of tools/APIs and need a custom dataset to teach a model how to use them.

## When not to use it
- If you only need simple text summarization or chat capabilities.
- If you prefer a fully local, open-source pipeline for data generation (use [distilabel](../frameworks/distilabel.md)).
- If you already have a massive corpus of real-world interaction logs to train on.

## Getting started

### Overview
Glaive typically operates as a platform where you define your tools and the desired interactions. The output is a dataset ready for fine-tuning.

### Example Dataset Structure (Agentic)
Glaive generated data often follows a pattern like this:

```json
{
  "instruction": "Check the weather in London and then book a flight if it's sunny.",
  "thought": "First, I need to check the weather in London using the weather_tool.",
  "tool_call": {"name": "get_weather", "parameters": {"location": "London"}},
  "tool_output": {"temperature": 22, "condition": "sunny"},
  "thought": "The weather is sunny. Now I should book a flight using the flight_tool.",
  "tool_call": {"name": "book_flight", "parameters": {"destination": "London", "from": "New York"}}
}
```

### Usage with Fine-tuning Tools
Once the dataset is generated, it can be exported and used with [Unsloth](../infrastructure/unsloth.md):

```python
from datasets import load_dataset
dataset = load_dataset("json", data_files="glaive_agent_data.json")
# Proceed to fine-tune with Unsloth or Axolotl
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — The target workflow for Glaive data.
- [distilabel](../frameworks/distilabel.md) — An open-source alternative for synthetic data generation.
- [Unsloth](../infrastructure/unsloth.md) — Frequently used to train on Glaive-generated agent data.
- [llama-factory](../frameworks/llama-factory.md) — For orchestrating the fine-tuning run.
- [axolotl](../frameworks/axolotl.md) — For config-based training on Glaive datasets.
- [Tool Calling & MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — The core capability Glaive aims to improve.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The architectural pattern Glaive supports.

## Sources / references
- [Glaive AI Official Website](https://glaive.ai/)
- [Glaive AI on X/Twitter](https://x.com/glaiveai)
- [Training Small Models for Tool Use (Blog)](https://glaive.ai/blog)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
