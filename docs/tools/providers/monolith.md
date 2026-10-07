# Monolith

## What it is
Monolith is a developer-centric, agent-optimized open-source model series developed by Basalt Labs. The flagship model, **Monolith-10**, is a highly specialized dense parameter model explicitly tuned to serve as an extremely low-latency, localized engine for autonomous multi-agent loops, complex tool calling, sequential planning, structured syntax execution, and **FastMCP 3.1 Task Protocol** orchestration.

## What problem it solves
Standard general-purpose large language models are highly prone to formatting errors (such as outputting invalid JSON during complex tool calls) and struggle with long-horizon logical planning. Monolith solves these development challenges by embedding rigid grammar alignment and agentic planning constructs directly into the model's core representation. It yields near-perfect compliance with complex JSON schemas and outputs programmatic commands with extreme speed and structural integrity, complementing frontier and open-weight models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6 VL.

## Where it fits in the stack
**AI Model / Local LLM / Agent & Developer Provider**. Monolith sits at the localized intelligence layer of the development stack. It acts as the core planner and orchestrator for autonomous agent nodes, integrating seamlessly with local Integrated Development Environments (IDEs), command-line dev interfaces, and [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) server architectures, such as FastMCP 3.1.

```
+-----------------------------------------------------------------------------------+
|                            Developer / Agent Workstation                          |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             Monolith-10 Inference Engine                          |
|    +------------------------+  +------------------------+  +-------------------+  |
|    | vLLM / GGUF Executor   |  | Grammar-Guided Parser  |  | FastMCP 3.1 Core  |  |
|    +------------------------+  +------------------------+  +-------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        Structured Pydantic Tool Call Output                       |
|           Guaranteed valid JSON matching exact schema & arguments                 |
+-----------------------------------------------------------------------------------+
                                         |
        +--------------------------------+--------------------------------+
        |                                                                 |
        v                                                                 v
+-------------------------------+                               +-------------------+
| FastMCP Server Tool Execution |                               | Local IDE / Terminal|
+-------------------------------+                               +-------------------+
```

## Typical use cases
- **High-Speed Autonomous Coding**: Serving as the task-routing and structural code-generation planner in multi-agent software engineering workflows.
- **Rigid Structured JSON Generation**: Powering backend automation pipelines that require guaranteed compliance with Pydantic v2 structured schema templates.
- **Multi-Step Tool Orchestration**: Parsing user intent, scheduling sequence actions, and calling consecutive terminal commands or external tools using FastMCP 3.1.
- **Database Schema Analysis & SQL Generation**: Safely translating natural language queries into valid database queries on secure local servers.

## Strengths
- **Sub-100ms Tool Call Latency**: Highly optimized attention patterns and dense architecture enable extremely rapid time-to-first-token (TTFT) for tool routing.
- **Near-Zero JSON Validation Failures**: Specifically aligned to respect formatting constraints, preventing parser crashes common with standard models.
- **Native Sequential Planning**: Fine-tuned using high-quality developer logs and agent trace datasets, allowing the model to decompose complex prompts into discrete logical steps.
- **Compact Hardware Footprint**: The 10B parameter variant runs comfortably at high speeds on consumer GPUs and local developer workstations.
- **FastMCP 3.1 Native Support**: Built to generate and process FastMCP 3.1 tool call payloads out of the box.

## Limitations
- **Specialized Persona**: Explicitly trained to be concise and direct; not designed for open-ended creative writing or conversational banter.
- **Technical Vocabulary Bias**: Token distribution is heavily biased toward programming languages, CLI commands, markdown structures, and system configurations.
- **Quantization Sensitivity**: Requires high-fidelity quantization formats (such as 8-bit GGUF or EXL2) to preserve its rigid schema-compliance capabilities.

## Quantization and Local Serving Guide

Monolith-10 is optimized for local execution using either EXL2 or GGUF quantization formats.

### Recommended Quantization Variants
- **EXL2 (6.0 bits/bpw)**: Ideal for NVIDIA consumer GPUs (RTX 4080 / 4090 / 5080) with ExLlamaV2 engine for sub-50ms token latencies.
- **GGUF Q8_0**: Full 8-bit quantization recommended for Apple Silicon (M2 Ultra / M3 Max / M4 Pro) via `llama.cpp` or Ollama.
- **GGUF Q4_K_M**: Lightweight 4-bit variant requiring ~7 GB VRAM, maintaining high schema accuracy.

```bash
# Serve Monolith-10 via Ollama local runtime
ollama run basaltlabs/monolith-10

# Serve via vLLM with constrained BNF grammar enforcement
python3 -m vllm.entrypoints.openai.api_server \
    --model basaltlabs/monolith-10 \
    --guided-decoding-backend outline \
    --port 8000
```

## When to use it
- When building local autonomous agent workforces (such as specialized coding or maintenance sub-agents).
- When your application requires high-frequency, reliable tool execution and strictly formatted JSON payloads.
- For local offline development environments where quick reasoning speeds and direct code generation are prioritized over general conversation.

## When not to use it
- As a general-purpose customer-facing support chatbot where conversational empathy, storytelling, or broad general knowledge is required.
- If your system does not utilize tool-calling, APIs, or structured program logic; standard general-purpose models like Llama 4, Qwen 3.6, or Gemma 4 are more versatile.

## Getting started
1. **Prerequisites**: Ensure you have Python 3.10+, PyTorch 2.4+, and an NVIDIA GPU or Apple Silicon system with sufficient memory.
2. **Library Setup**: Install the required framework packages and Pydantic v2:
   ```bash
   pip install transformers accelerate torch sentencepiece pydantic>=2.0.0 fastmcp
   ```
3. **Model Initialization**: Load the Monolith-10 model using Hugging Face's API:
   ```python
   import torch
   from transformers import AutoTokenizer, AutoModelForCausalLM

   model_id = "basaltlabs/monolith-10"
   tokenizer = AutoTokenizer.from_pretrained(model_id)
   model = AutoModelForCausalLM.from_pretrained(
       model_id,
       torch_dtype=torch.bfloat16,
       device_map="auto"
   )
   ```

## CLI examples
Execute and serve Monolith-10 locally to expose a standardized high-performance API endpoint:

```bash
# Serve Monolith-10 using vLLM to expose a local OpenAI-compatible endpoint
python3 -m vllm.entrypoints.openai.api_server \
    --model basaltlabs/monolith-10 \
    --port 8000 \
    --dtype bfloat16

# Query the local model directly using cURL to test strict JSON schema generation
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "basaltlabs/monolith-10",
    "messages": [
      {"role": "user", "content": "Generate a JSON representation of a user profile with name, age, and verified status."}
    ],
    "response_format": { "type": "json_object" }
  }'
```

## API examples

### FastMCP 3.1 Agent Routing Server with Monolith-10

The following example demonstrates building a FastMCP 3.1 server that routes incoming natural language requests to local tools using Monolith-10 and Pydantic v2:

```python
import json
from typing import Literal, Union, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from mcp.server.fastmcp import FastMCP

# Define tool parameter schemas using Pydantic v2
class DatabaseQueryArgs(BaseModel):
    sql_query: str = Field(..., description="Valid ANSI SQL query string")
    max_rows: int = Field(100, ge=1, le=1000, description="Row limit")

class CodeLintArgs(BaseModel):
    file_path: str = Field(..., description="Target code file path")
    fix_auto: bool = Field(False, description="Automatically apply lint fixes")

class AgentRoutingDecision(BaseModel):
    selected_tool: Literal["database_query", "code_lint"] = Field(..., description="Chosen tool name")
    arguments: Union[DatabaseQueryArgs, CodeLintArgs] = Field(..., description="Validated tool arguments")
    reasoning_trace: str = Field(..., description="Monolith-10 planning rationale")

# Initialize FastMCP server
mcp = FastMCP("Monolith-Agent-Router", version="3.1.0")

@mcp.tool()
async def route_agent_action(user_prompt: str) -> str:
    """Uses Monolith-10 structured planning to route incoming requests to FastMCP tools."""
    # Simulated response from local Monolith-10 model running on vLLM
    simulated_monolith_json = {
        "selected_tool": "database_query",
        "arguments": {
            "sql_query": "SELECT user_id, email, created_at FROM users WHERE active = true;",
            "max_rows": 50
        },
        "reasoning_trace": "User requested active user records. Database query tool is appropriate."
    }

    try:
        decision = AgentRoutingDecision.model_validate(simulated_monolith_json)
        return decision.model_dump_json(indent=2)
    except ValidationError as e:
        return f"Error: Monolith output failed validation: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

### Python API Tool Selection with Pydantic v2

```python
import json
from typing import Literal, Union
from pydantic import BaseModel, Field, ValidationError
import openai

class GCalSyncReferenceArgs(BaseModel):
    target_db_url: str = Field(..., description="Target database connection string URL.")
    force_sync: bool = Field(default=False, description="Whether to force synchronize references.")

class PaperlessExportTextArgs(BaseModel):
    export_dir: str = Field(..., description="Directory path to export text files.")

class SelectedToolCall(BaseModel):
    tool_name: Literal["gcal_sync_reference", "paperless_export_text"] = Field(..., description="Selected tool name.")
    arguments: Union[GCalSyncReferenceArgs, PaperlessExportTextArgs] = Field(..., description="Tool arguments.")

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="basalt-key-placeholder"
)

prompt = """
Select the appropriate tool and arguments for: 'Sync my GCal references to my secure database'.
Available tools:
1. gcal_sync_reference(target_db_url: str, force_sync: bool)
2. paperless_export_text(export_dir: str)
"""

response = client.chat.completions.create(
    model="basaltlabs/monolith-10",
    messages=[
        {"role": "system", "content": "You are an agent orchestrator. Output only the selected tool call in raw JSON matching the schema."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.0
)

try:
    raw_content = response.choices[0].message.content or "{}"
    parsed_json = json.loads(raw_content)

    validated_plan = SelectedToolCall.model_validate(parsed_json)

    print("Structured Agent Decision Plan (Validated with Pydantic v2):")
    print(validated_plan.model_dump_json(indent=2))
except json.JSONDecodeError:
    print("JSON Decode Error. Raw output:", response.choices[0].message.content)
except ValidationError as e:
    print("Pydantic Validation Error:", e)
```

## Matrix Comparison with Local Developer Models

| Feature | Monolith-10 | DeepSeek-Coder 33B | Qwen 2.5 Coder 14B | Llama 3.3 70B Instruct |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | FastMCP Tool Calling & Planning | Raw Code Generation | Polyglot Code & Math | General Instruction |
| **JSON Schema Compliance** | 99.8% | 94.2% | 96.5% | 95.1% |
| **TTFT Latency (RTX 4090)** | < 45ms | ~ 120ms | ~ 85ms | ~ 320ms |
| **VRAM Footprint (FP16)** | ~ 20 GB | ~ 66 GB | ~ 28 GB | ~ 140 GB |
| **FastMCP 3.1 Native** | Yes | Custom Prompting | Custom Prompting | Custom Prompting |

## Related tools / concepts
- [DeepSeek](./deepseek.md) — Advanced open-source models with high coding and reasoning capabilities.
- [Mistral AI](./mistral.md) — Dense and Mixture-of-Experts local models.
- [Together AI](./together.md) — High-performance inference provider hosting developer and agentic models.
- [Ollama](../../services/ollama.md) — Framework for running and managing local models.
- [vLLM](../infrastructure/vllm.md) — LLM serving and optimization framework.
- [Codeium](../development_ops/codeium.md) — Developer assistance integrated with agent interfaces.
- [Sourcegraph Cody](../development_ops/sourcegraph_cody.md) — Multi-repo codebase intelligence assistant.
- [FastMCP](../automation_orchestration/mcp.md) — High-performance Python framework for Model Context Protocol 3.1.

## Sources / references
- [Basalt Labs Official Hugging Face Workspace](https://huggingface.co/basaltlabs)
- [Agentic Reasoning and Schema-Steering Standards](https://github.com/basaltlabs/monolith)
- [Model Context Protocol FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
