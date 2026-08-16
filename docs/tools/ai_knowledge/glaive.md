# Glaive

## What it is
Glaive is an AI platform specialized in generating high-quality synthetic data for training and fine-tuning Small Language Models (SLMs) and agentic systems. As of early January 2027, Glaive v2.4 provides multi-turn trajectory synthesis and FastMCP 3.1 protocol tool call schemas, enabling developers to distil reasoning from frontier models like Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Llama 4 into compact 3B-14B models (e.g. Gemma 3, Qwen 3.8, Llama 4 8B).

## What problem it solves
Generic synthetic data generation often fails to capture the nuances of real-world tool use and API interactions. Glaive addresses this by:
- **Generating Functional Data**: Creating datasets that specifically target function calling and structured output according to the latest [MCP 3.1](../../tools/automation_orchestration/mcp.md) specifications.
- **Improving SLM Performance**: Enabling smaller models like [Llama 4 Maverick](../ai_knowledge/local_llms.md) and Gemma 3 to punch above their weight in agentic workflows.
- **Reducing Dependency on Frontier Models**: Providing a way to distill the reasoning capabilities of [Claude 5.1 Sonnet](../providers/anthropic.md) or [GPT-5.5](../ai_knowledge/openai.md) into smaller, more cost-effective specialized models.

## Where it fits in the stack
Glaive sits in the **AI & Knowledge / Synthetic Data** layer. It provides high-quality training signals used to adapt base models for agentic behavior, often being paired with fine-tuning tools like [Unsloth](../infrastructure/unsloth.md) or [LLaMA Factory](../frameworks/llama-factory.md).

## Typical use cases
- **Agentic Tool-Use Training**: Generating datasets of natural language prompts followed by correct tool calls using the [MCP 3.1](../../tools/automation_orchestration/mcp.md) Task Protocol.
- **Function Calling Distillation**: Training a 7B or 8B model to be as reliable at function calling as [Claude 5.1 Sonnet](../providers/anthropic.md).
- **Multi-Step Reasoning**: Creating synthetic examples of "Chain of Thought" reasoning for complex problem solving in autonomous loops.
- **API Sandbox Data**: Generating realistic API responses and error states to train models on robust error handling and self-correction.

## Strengths
- **Focus on Agents**: Specifically designed for the agentic and tool-use era of AI.
- **High Quality & Diversity**: Uses sophisticated techniques to ensure synthetic data is varied and accurate.
- **SLM Optimization**: Particularly effective at making smaller models usable in production agent stacks.
- **Structured Output Mastery**: Helps models learn to strictly adhere to complex JSON schemas.

## Limitations
- **Platform Dependent**: Unlike local tools like [distilabel](../frameworks/distilabel.md), Glaive is primarily used as a managed platform.
- **Niche Focus**: Less focused on broad general-purpose chat data compared to frameworks like [LLaMA Factory](../frameworks/llama-factory.md).
- **Black Box Generation**: The internal generation logic may be less transparent than fully open-source pipeline tools.

## When to use it
- When you are building an autonomous agent and need it to be reliable at tool calling.
- When you want to use a small model (e.g., Llama 4 8B or Gemma 3) for complex API orchestration.
- When you have a specific set of tools/APIs and need a custom dataset to teach a model how to use them.

## When not to use it
- If you only need simple text summarization or chat capabilities.
- If you prefer a fully local, open-source pipeline for data generation (use [distilabel](../frameworks/distilabel.md)).
- If you already have a massive corpus of real-world interaction logs to train on.

## Getting started

### Installation
Glaive is a cloud platform; you can interact with it via its web interface or REST API. For Python integration:

```bash
pip install requests
```

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

### Programmatic Synthetic Task Request (Pydantic v2 Schema)
Create a validated synthetic data request using Glaive API payloads:

```python
import urllib.request
import json
from pydantic import BaseModel, Field, field_validator

class GlaiveGenerateRequest(BaseModel):
    task: str = Field(..., description="Description of the synthetic dataset task.")
    num_examples: int = Field(default=10, ge=1, le=1000)
    format: str = Field(default="json", description="Data format output.")
    fastmcp_version: str = Field(default="3.1", description="FastMCP protocol standard.")

    @field_validator('format')
    @classmethod
    def validate_format(cls, v: str) -> str:
        allowed = {'json', 'jsonl', 'parquet'}
        if v.lower() not in allowed:
            raise ValueError(f"Format must be one of {allowed}")
        return v.lower()

payload = GlaiveGenerateRequest(
    task="Create an agentic tool-use dataset for SQLite querying and Pydantic validation.",
    num_examples=25,
    format="jsonl"
).model_dump()

req = urllib.request.Request(
    "https://api.glaive.ai/v1/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": "Bearer YOUR_GLAIVE_API_KEY",
        "Content-Type": "application/json"
    },
    method="POST"
)
# with urllib.request.urlopen(req) as res:
#     data = json.loads(res.read().decode("utf-8"))
```

## CLI examples

```bash
# Verify API connectivity
curl -I https://api.glaive.ai/v1/health

# Trigger a dataset generation job matching MCP 3.1 standard
curl -X POST https://api.glaive.ai/v1/generate \
     -H "Authorization: Bearer $GLAIVE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"task": "calculator_tool", "num_examples": 10, "mcp_version": "3.1"}'

# Download a completed dataset
curl -O https://api.glaive.ai/v1/datasets/ds_12345/download?api_key=$GLAIVE_API_KEY
```

## API examples

### Python: Generating Agentic Data
```python
import requests

def generate_tool_data(tool_definition):
    payload = {
        "description": "Generate conversations where a user asks to use this tool",
        "tools": [tool_definition],
        "temperature": 0.7,
        "mcp_version": "3.1"
    }
    # r = requests.post("https://api.glaive.ai/v1/generate", json=payload)
    # return r.json()

weather_tool = {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "parameters": {"location": "string"}
}
# data = generate_tool_data(weather_tool)
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — The target workflow for Glaive data.
- [distilabel](../frameworks/distilabel.md) — An open-source alternative for synthetic data generation.
- [Unsloth](../infrastructure/unsloth.md) — Frequently used to train on Glaive-generated agent data.
- [LLaMA Factory](../frameworks/llama-factory.md) — For orchestrating the fine-tuning run.
- [Axolotl](../frameworks/axolotl.md) — For config-based training on Glaive datasets.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The core protocol Glaive aims to support.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The architectural pattern Glaive supports.
- [Llama 4 Maverick](local_llms.md) — Primary target for SLM distillation using Glaive data.

## Sources / references
- [Glaive AI Official Website](https://glaive.ai/)
- [Glaive AI Documentation](https://docs.glaive.ai/)
- [Glaive AI on X/Twitter](https://x.com/glaiveai)
- [Training Small Models for Tool Use (Blog)](https://glaive.ai/blog)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
