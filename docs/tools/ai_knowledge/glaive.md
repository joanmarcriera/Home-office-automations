# Glaive

## What it is
Glaive is an AI platform specialized in generating high-quality synthetic data for training, fine-tuning, and distilling Small Language Models (SLMs) and agentic systems. It is a critical tool for creating specialized datasets that improve a model's ability to execute **FastMCP 3.1** tools, call structured APIs, and reason through multi-step agentic workflows for frontier pipelines powered by Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, and Gemma 3.

## What problem it solves
Generic synthetic data generation often fails to capture the nuances of real-world tool use and API interactions. Glaive addresses this by:
- **Generating Functional Data**: Creating datasets that specifically target function calling and structured output according to the latest [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) specifications.
- **Improving SLM Performance**: Enabling smaller models like Llama 4 and Gemma 3 to punch above their weight in agentic workflows.
- **Reducing Dependency on Frontier Models**: Providing a way to distill the reasoning capabilities of [Claude 5.1](../providers/anthropic.md) or [GPT-5.5](../ai_knowledge/openai.md) into smaller, more cost-effective specialized models.

## Where it fits in the stack
Glaive sits in the **AI & Knowledge / Synthetic Data** layer. It provides high-quality training signals used to adapt base models for agentic behavior, often being paired with fine-tuning tools like [Unsloth](../infrastructure/unsloth.md) or [LLaMA Factory](../frameworks/llama-factory.md).

## Typical use cases
- **Agentic Tool-Use Training**: Generating datasets of natural language prompts followed by correct tool calls using the [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) Task Protocol.
- **Function Calling Distillation**: Training an 8B model to be as reliable at function calling as [Claude 5.1 Sonnet](../providers/anthropic.md).
- **Multi-Step Reasoning**: Creating synthetic examples of "Chain of Thought" reasoning for complex problem solving in autonomous loops.
- **API Sandbox Data**: Generating realistic API responses and error states to train models on robust error handling and self-correction.

## Strengths
- **Focus on Agents**: Specifically designed for the agentic and tool-use era of AI.
- **High Quality & Diversity**: Uses sophisticated techniques to ensure synthetic data is varied and accurate.
- **SLM Optimization**: Particularly effective at making smaller models usable in production agent stacks.
- **Structured Output Mastery**: Helps models learn to strictly adhere to complex JSON and Pydantic schemas.

## Limitations
- **Platform Dependent**: Unlike local tools like [distilabel](../frameworks/distilabel.md), Glaive is primarily used as a managed platform.
- **Niche Focus**: Less focused on broad general-purpose chat data compared to frameworks like [LLaMA Factory](../frameworks/llama-factory.md).
- **Black Box Generation**: The internal generation logic may be less transparent than fully open-source pipeline tools.

## When to use it
- When you are building an autonomous agent and need it to be reliable at tool calling.
- When you want to use a small model (e.g., Llama 4 or Gemma 3) for complex API orchestration.
- When you have a specific set of tools/APIs and need a custom dataset to teach a model how to use them.

## When not to use it
- If you only need simple text summarization or chat capabilities.
- If you prefer a fully local, open-source pipeline for data generation (use [distilabel](../frameworks/distilabel.md)).
- If you already have a massive corpus of real-world interaction logs to train on.

## Getting started

### Installation
Glaive is a cloud platform; you can interact with it via its web interface or REST API. For Python integration:

```bash
pip install requests pydantic
```

### Example Dataset Structure (Agentic)
Glaive generated data follows a structured agentic trace pattern:

```json
{
  "instruction": "Check the weather in London and then book a flight if it's sunny.",
  "thought": "First, I need to check the weather in London using the weather_tool via FastMCP 3.1.",
  "tool_call": {"name": "get_weather", "parameters": {"location": "London"}},
  "tool_output": {"temperature": 22, "condition": "sunny"},
  "thought": "The weather is sunny. Now I should book a flight using the flight_tool.",
  "tool_call": {"name": "book_flight", "parameters": {"destination": "London", "from": "New York"}}
}
```

### Hello-world (API)
Create a simple synthetic data request using the Glaive API:

```python
import requests

api_key = "YOUR_GLAIVE_API_KEY"
url = "https://api.glaive.ai/v1/generate"

payload = {
    "task": "Create a dataset for a weather tool using FastMCP 3.1",
    "num_examples": 5,
    "format": "json"
}
headers = {"Authorization": f"Bearer {api_key}"}

# response = requests.post(url, json=payload, headers=headers)
# print(response.json())
```

## CLI examples

```bash
# Verify API connectivity
curl -I https://api.glaive.ai/v1/health

# Trigger a dataset generation job matching FastMCP 3.1 standard
curl -X POST https://api.glaive.ai/v1/generate \
     -H "Authorization: Bearer $GLAIVE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"task": "calculator_tool", "num_examples": 10, "mcp_version": "3.1"}'

# Download a completed dataset
curl -O https://api.glaive.ai/v1/datasets/ds_12345/download?api_key=$GLAIVE_API_KEY
```

## API examples

### Python: Generating Agentic Data with Pydantic v2 Schema Validation
```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any
import requests

class ToolParameterSchema(BaseModel):
    name: str = Field(..., description="Tool parameter name")
    type: str = Field(..., description="Data type")

class ToolDefinition(BaseModel):
    name: str = Field(..., description="Tool function name")
    description: str = Field(..., description="Functional description")
    parameters: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError("Tool name must be a valid Python identifier")
        return v

class GlaiveGenerationRequest(BaseModel):
    description: str
    tools: List[ToolDefinition]
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    mcp_version: str = Field(default="3.1")

# Example construction
weather_tool = ToolDefinition(
    name="get_weather",
    description="Get current weather for a location",
    parameters={"location": "string"}
)

req = GlaiveGenerationRequest(
    description="Generate conversations where a user requests weather checks",
    tools=[weather_tool]
)

print(f"Validated request for {req.tools[0].name} using FastMCP {req.mcp_version}")
```

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — The target workflow for Glaive data.
- [distilabel](../frameworks/distilabel.md) — An open-source alternative for synthetic data generation.
- [Unsloth](../infrastructure/unsloth.md) — Frequently used to train on Glaive-generated agent data.
- [LLaMA Factory](../frameworks/llama-factory.md) — For orchestrating the fine-tuning run.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — The core protocol Glaive supports.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The architectural pattern Glaive supports.

## Sources / references
- [Glaive AI Official Website](https://glaive.ai/)
- [Glaive AI Documentation](https://docs.glaive.ai/)
- [Training Small Models for Tool Use (Blog)](https://glaive.ai/blog)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
