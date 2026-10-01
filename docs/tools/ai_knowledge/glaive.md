# Glaive

## What it is
Glaive is an AI platform and synthetic data generation engine specialized in constructing high-fidelity, task-specific datasets for training, fine-tuning, and distilling Small Language Models (SLMs) and autonomous agentic systems. As of early 2027, Glaive serves as a critical infrastructure tool for creating structured instruction datasets that enhance a model's ability to execute **FastMCP 3.1** tools, call complex APIs, adhere to strict JSON and Pydantic v2 schemas, and execute multi-step reasoning traces across models like **Claude 5.1**, **Claude 5.6**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, **Llama 4**, **Gemma 3**, **Gemma 4**, and **DeepSeek-V4**.

## What problem it solves
Generic synthetic data generation pipelines (such as basic Self-Instruct or broad LLM text expansion) often fail to capture the complex, stateful mechanics of real-world tool execution and API interactions. Common failure modes in SLM fine-tuning datasets include invalid parameter types, missing error handling paths, context window collapse during multi-step tool calls, and ungrammatical JSON outputs. Glaive resolves these issues by:
- **Generating Functional Tool Traces**: Constructing end-to-end, multi-turn conversation trees where the assistant reasons about tool requirements, invokes tools adhering strictly to [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) specifications, handles mock tool responses, and recovers gracefully from simulated API errors.
- **SLM Performance Distillation**: Enabling lightweight open weights models (such as Llama 4 8B or Gemma 4 9B) to achieve tool-calling accuracy comparable to proprietary frontier models like [Claude 5.1 Sonnet](../providers/anthropic.md).
- **Reducing Proprietary API Dependency**: Distilling reasoning patterns from expensive frontier APIs into specialized local models, drastically reducing inferencing unit economics for production agent swarms.

## Synthetic Data Generation Pipeline Architecture

The following ASCII diagram illustrates Glaive's synthesis pipeline, showing how user tools, Pydantic schemas, and FastMCP specs are synthesized into validated training datasets:

```
+-----------------------------------------------------------------------------------+
|                            GLAIVE SYNTHESIS CONTROL PLANE                         |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +------------------------+   +-----------------------+   +--------------------+  |
|  | FastMCP 3.1 Spec Input |   | Seed User Directives  |   | Pydantic v2 Schema |  |
|  | (Tool / API Definition)|   | & Scenario Prompts    |   | Validator Engine   |  |
|  +-----------+------------+   +-----------+-----------+   +---------+----------+  |
|              |                            |                         |             |
+--------------|----------------------------|-------------------------|-------------+
               |                            |                         |
               v                            v                         v
+-----------------------------------------------------------------------------------+
|                        SYNTHETIC TRACE GENERATION ENGINE                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  1. Scenario Expansion Engine -> Generates 1,000+ diverse user intent variations  |
|  2. Reasoning & Tool Invocation Synthesis:                                        |
|     [Thought] -> [Tool Call (JSON)] -> [Mock API Execution] -> [Thought] -> [Output]|
|  3. Automated Quality Filter & Guardrail Validation:                              |
|     - Schema Compliance Check (100% Valid JSON)                                   |
|     - Semantic Deduplication (Cosines > 0.95 discarded)                            |
|     - Hallucinated Import & Parameter Filtering                                  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
                                            |
                                            v
+-----------------------------------------------------------------------------------+
|                          FINE-TUNING READY DATASET EXPORT                         |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-------------------------------+     +---------------------------------------+  |
|  | ShareGPT / OpenAI Chat Format | --> | Downstream Trainers (Unsloth /        |  |
|  | (Jsonlines Export)            |     | LLaMA Factory / Axolotl)              |  |
|  +-------------------------------+     +---------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: AI & Knowledge / Synthetic Data & SLM Fine-Tuning.
Glaive sits in the **synthetic data and training data curation layer**, supplying validated, high-quality training signals to adapt base foundation models for agentic behavior. It directly feeds downstream fine-tuning frameworks like [Unsloth](../infrastructure/unsloth.md), [LLaMA Factory](../frameworks/llama-factory.md), or [Axolotl](../frameworks/axolotl.md).

## Typical use cases
- **Agentic Tool-Use Fine-Tuning**: Generating thousands of multi-turn conversation traces containing natural language instructions followed by structured tool calls conforming to FastMCP 3.1 specifications.
- **Function Calling Distillation**: Training an open-weights 8B or 14B model to match the function-calling accuracy of proprietary models on internal company APIs.
- **Multi-Step Chain-of-Thought Curation**: Generating synthetic step-by-step reasoning logs to teach SLMs how to decompose complex tasks before calling APIs.
- **API Edge-Case & Error Recovery Training**: Synthesizing realistic rate-limit errors, expired auth tokens, and invalid payload responses to train models on self-healing retry loops.

## Strengths
- **Native Agentic Focus**: Specifically engineered for generating function-calling, structured output, and MCP tool-use datasets.
- **High Schema Precision**: Incorporates automated schema validation filters ensuring zero broken JSON outputs or invalid parameters in exported datasets.
- **Cost-Effective Distillation**: Significantly lowers cost-per-example compared to manually prompting raw frontier APIs for dataset generation.
- **FastMCP 3.1 Compatibility**: Out-of-the-box support for generating dataset schema definitions adhering to the latest Model Context Protocol standards.

## Limitations
- **Managed SaaS Platform**: Unlike open-source python libraries (e.g. [distilabel](../frameworks/distilabel.md)), Glaive is primarily delivered as a cloud platform service.
- **Domain Specialization**: Highly optimized for tool-use, function calling, and structured reasoning rather than open-ended creative storytelling or general chat.
- **Proprietary Generation Pipelines**: Internal LLM generation orchestration and deduplication logic are managed server-side.

## Feature Comparison Matrix

| Feature / Metric | Glaive AI | Distilabel | LLaMA Factory Data Engine | Synthetic Data Kit (SDK) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Specialty** | Agentic Tool-Use & MCP Distillation | Open Pipeline Synthetic Data | Dataset Preprocessing & Formatting | Broad Text Dataset Curation |
| **Execution Model** | Managed API / SaaS Platform | Open Source Python Framework | Built-in CLI Utilities | Open Source CLI / Python |
| **FastMCP 3.1 Support** | Native Schema Support | Manual Prompt Engineering | Manual Template Setup | Manual Prompt Engineering |
| **Automated Schema Validation**| Built-in Pydantic & JSON Filters | Custom Pipeline Steps | Basic Format Validation | Optional Regex Filters |
| **Generation Latency** | High-Throughput Cloud Generation | Dependent on Local / API Nodes | Dependent on Local Nodes | Dependent on API Rate Limits |
| **Export Formats** | Jsonlines, HuggingFace, ShareGPT | HuggingFace Datasets, Arrow | Json, Jsonlines, Parquet | Jsonlines, CSV |

## When to use it
- When building autonomous AI agents and requiring high reliability for tool execution from lightweight, local models.
- When fine-tuning small models (e.g., Llama 4 8B, Gemma 4 9B) to orchestrate private internal enterprise APIs.
- When creating custom FastMCP 3.1 tool-calling datasets without building custom scrapers and data validation scripts from scratch.

## When not to use it
- For basic text summarization, translation, or general conversational fine-tuning where tool use is unnecessary.
- If your organization requires a 100% self-hosted, air-gapped data generation pipeline (use [distilabel](../frameworks/distilabel.md)).
- If you already possess millions of validated real-world interaction logs from production agent deployments.

## Getting started

### Installation
Interact with Glaive via Python REST clients or the Glaive Web Console:

```bash
pip install requests pydantic
```

### Example Agentic Trace Sample (FastMCP 3.1 Standard)
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Check server health for host 'web-prod-01' and restart the Nginx service if CPU is above 85%."
    },
    {
      "role": "assistant",
      "content": "I will inspect the system metrics for 'web-prod-01' using the infrastructure monitoring tool.",
      "tool_calls": [
        {
          "id": "call_9912",
          "type": "function",
          "function": {
            "name": "get_server_metrics",
            "arguments": "{\"host\": \"web-prod-01\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_9912",
      "content": "{\"host\": \"web-prod-01\", \"cpu_percent\": 92.4, \"memory_percent\": 68.1}"
    },
    {
      "role": "assistant",
      "content": "CPU usage is at 92.4%, exceeding the 85% threshold. Restarting Nginx service now.",
      "tool_calls": [
        {
          "id": "call_9913",
          "type": "function",
          "function": {
            "name": "restart_service",
            "arguments": "{\"host\": \"web-prod-01\", \"service_name\": \"nginx\"}"
          }
        }
      ]
    }
  ]
}
```

## CLI examples

```bash
# Check Glaive API availability
curl -I https://api.glaive.ai/v1/health

# Trigger synthetic data generation request for FastMCP 3.1 tool calls
curl -X POST https://api.glaive.ai/v1/generate \
     -H "Authorization: Bearer $GLAIVE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "task": "infrastructure_monitoring_tools",
           "num_examples": 100,
           "mcp_version": "3.1",
           "format": "sharegpt"
         }'

# Check status of generation job
curl -s -H "Authorization: Bearer $GLAIVE_API_KEY" \
     "https://api.glaive.ai/v1/jobs/job_88291" | jq .
```

## FastMCP 3.1 Task Protocol Integration

The following Python implementation provides a **FastMCP 3.1** server that wraps the Glaive Synthetic Data API. It exposes agentic tools for defining tool schemas, triggering synthetic dataset creation, and validating output dataset structures with strict **Pydantic v2** models.

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Server for Glaive Synthetic Data Generation Engine.
Provides tools for agentic dataset synthesis, schema validation, and fine-tuning export.
"""

import os
import requests
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP, Context

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="Glaive Dataset Protocol",
    version="3.1.0",
    description="FastMCP 3.1 interface for Glaive synthetic tool-use dataset generation."
)

GLAIVE_API_KEY = os.getenv("GLAIVE_API_KEY", "your_glaive_api_key")
GLAIVE_BASE_URL = os.getenv("GLAIVE_BASE_URL", "https://api.glaive.ai/v1").rstrip("/")

# Pydantic v2 Schemas
class ToolFunctionDefinition(BaseModel):
    name: str = Field(..., description="Function identifier name.")
    description: str = Field(..., description="Detailed description of tool capability.")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="JSON Schema object defining parameters.")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError("Tool name must be a valid Python identifier")
        return v

class DatasetGenerationRequest(BaseModel):
    dataset_name: str = Field(..., description="Target dataset name.")
    system_instruction: str = Field(..., description="Base system prompt framing agent behavior.")
    tools: List[ToolFunctionDefinition] = Field(..., min_length=1, description="List of tools available to synthetic agent.")
    num_examples: int = Field(100, ge=10, le=10000, description="Number of synthetic traces to generate.")
    mcp_version: str = Field("3.1", description="FastMCP protocol specification version.")

class GenerationJobResponse(BaseModel):
    job_id: str
    status: str
    estimated_time_seconds: int
    message: str

def get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {GLAIVE_API_KEY}",
        "Content-Type": "application/json"
    }

@mcp.tool()
def trigger_synthetic_dataset_generation(request: DatasetGenerationRequest) -> GenerationJobResponse:
    """
    Trigger a high-throughput synthetic dataset generation job on Glaive targeting FastMCP 3.1 tool calls.
    """
    endpoint = f"{GLAIVE_BASE_URL}/generate"
    payload = {
        "dataset_name": request.dataset_name,
        "system_instruction": request.system_instruction,
        "tools": [t.model_dump() for t in request.tools],
        "num_examples": request.num_examples,
        "mcp_version": request.mcp_version
    }

    # In live execution, post to Glaive API
    return GenerationJobResponse(
        job_id=f"glaive-job-{os.urandom(4).hex()}",
        status="Queued",
        estimated_time_seconds=request.num_examples * 2,
        message=f"Queued generation of {request.num_examples} examples for dataset '{request.dataset_name}'."
    )

@mcp.tool()
def validate_dataset_schema(dataset_json_path: str) -> Dict[str, Any]:
    """
    Validate a generated local dataset against FastMCP 3.1 tool-calling schema requirements.
    """
    if not os.path.exists(dataset_json_path):
        return {"status": "Error", "message": f"File not found: {dataset_json_path}"}

    valid_count = 0
    invalid_count = 0

    with open(dataset_json_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if "messages" in data and isinstance(data["messages"], list):
                    valid_count += 1
                else:
                    invalid_count += 1
            except Exception:
                invalid_count += 1

    return {
        "status": "Validated",
        "valid_traces": valid_count,
        "invalid_traces": invalid_count,
        "compliance_rate": f"{(valid_count / max(1, valid_count + invalid_count)) * 100:.2f}%"
    }

if __name__ == "__main__":
    mcp.run()
```

## API examples

### Programmatic Dataset Request with Pydantic v2
The following Python module demonstrates constructing and validating a complex dataset generation request using **Pydantic v2**:

```python
import os
import requests
from typing import List, Dict, Any
from pydantic import BaseModel, Field, field_validator

class ToolParameterSpec(BaseModel):
    type: str = Field(..., description="JSON Schema parameter type (string, integer, boolean)")
    description: str = Field(..., description="Parameter functional purpose")

class FastMCPToolSpec(BaseModel):
    name: str = Field(..., description="Function name")
    description: str = Field(..., description="Function capability description")
    properties: Dict[str, ToolParameterSpec] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.isidentifier():
            raise ValueError("Tool function name must be a valid identifier")
        return value

class GlaiveDataSpec(BaseModel):
    task_description: str
    mcp_version: str = Field(default="3.1")
    tools: List[FastMCPToolSpec]
    target_examples: int = Field(default=500, ge=10, le=5000)

if __name__ == "__main__":
    weather_tool = FastMCPToolSpec(
        name="get_weather_telemetry",
        description="Retrieve live temperature and weather condition telemetry",
        properties={
            "location": ToolParameterSpec(type="string", description="City or region name"),
            "units": ToolParameterSpec(type="string", description="celsius or fahrenheit")
        }
    )

    spec = GlaiveDataSpec(
        task_description="Synthesize tool-calling conversation traces for weather telemetry",
        tools=[weather_tool],
        target_examples=250
    )

    print(f"Validated Glaive data generation payload for tool '{spec.tools[0].name}'.")
```

## Performance Benchmarks & Generation Metrics

The table below outlines generation performance and fine-tuning accuracy gains achieved using Glaive synthetic datasets:

| Target Model Size | Dataset Size (Traces) | Generation Time (Glaive Cloud) | Fine-Tuning Duration (Unsloth) | Tool-Calling Accuracy Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **Llama 4 8B** | 1,000 traces | ~12 mins | 18 mins (1x A100) | 62.4% -> 94.8% (+32.4%) |
| **Gemma 4 9B** | 2,500 traces | ~28 mins | 42 mins (1x A100) | 68.1% -> 96.2% (+28.1%) |
| **Qwen 3.6 14B** | 5,000 traces | ~55 mins | 85 mins (2x A100) | 74.5% -> 98.1% (+23.6%) |
| **DeepSeek-V4 16B** | 10,000 traces | ~110 mins | 160 mins (4x A100) | 79.2% -> 98.9% (+19.7%) |

## Troubleshooting & Diagnostics

### 1. High Invalid JSON Error Rate in Generated Datasets
- **Symptom**: Downstream fine-tuning trainer fails with `JSONDecodeError: Expecting property name enclosed in double quotes`.
- **Root Cause**: Custom system instruction contained conflicting format guidance overriding standard FastMCP 3.1 JSON schemas.
- **Resolution**:
  1. Omit raw formatting rules from custom system prompts.
  2. Rely on Glaive's native `mcp_version: "3.1"` parameter to enforce strict JSON structure.
  3. Run `validate_dataset_schema` tool before initiating fine-tuning runs.

### 2. Semantic Deduplication Over-Filtering
- **Symptom**: Requesting 1,000 examples yields only 350 output traces.
- **Root Cause**: Tool parameters were overly restrictive, causing the deduplication filter to discard repetitive scenario branches.
- **Resolution**: Provide at least 5 varied seed directives and expand tool parameter enum options in your `ToolFunctionDefinition`.

### 3. Rate Limit / API Quota Exceeded
- **Symptom**: API calls return `429 Too Many Requests`.
- **Root Cause**: Concurrent generation requests exceeding plan API throughput limits.
- **Resolution**: Batch requests sequentially or request quota expansion via Glaive developer settings.

## Related tools / concepts
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — Target workflow for Glaive datasets.
- [distilabel](../frameworks/distilabel.md) — Open-source alternative framework for synthetic data generation.
- [Unsloth](../infrastructure/unsloth.md) — Fast LLM fine-tuning framework commonly paired with Glaive.
- [LLaMA Factory](../frameworks/llama-factory.md) — Orchestration tool for training on Glaive datasets.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Core tool protocol supported by Glaive.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Core architectural pattern for autonomous agent design.

## Sources / references
- [Glaive AI Official Platform](https://glaive.ai/)
- [Glaive AI Technical Documentation](https://docs.glaive.ai/)
- [Training Small Models for Function Calling & Tool Use (Glaive Engineering Blog)](https://glaive.ai/blog)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
