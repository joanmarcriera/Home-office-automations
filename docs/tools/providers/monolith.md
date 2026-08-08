# Monolith

## What it is
Monolith is a developer-centric, agent-optimized open-source model series developed by Basalt Labs. The flagship model, **Monolith-10**, is a highly specialized dense parameter model explicitly tuned to serve as an extremely low-latency, localized engine for autonomous multi-agent loops, complex tool calling, sequential planning, and structured syntax execution.

## What problem it solves
Standard general-purpose large language models are highly prone to formatting errors (such as outputting invalid JSON during complex tool calls) and struggle with long-horizon logical planning. Monolith solves these development challenges by embedding rigid grammar alignment and agentic planning constructs directly into the model's core representation. It yields near-perfect compliance with complex JSON schemas and outputs programmatic commands with extreme speed and structural integrity.

## Where it fits in the stack
**AI Model / Local LLM / Agent & Developer Provider**. Monolith sits at the localized intelligence layer of the development stack. It acts as the core planner and orchestrator for autonomous agent nodes, integrating seamlessly with local Integrated Development Environments (IDEs), command-line dev interfaces, and [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) server architectures, such as FastMCP 3.1.

## Typical use cases
- **High-Speed Autonomous Coding**: Serving as the task-routing and structural code-generation planner in multi-agent software engineering workflows coordinating models like Claude 5.1 and GPT-5.5.
- **Rigid Structured JSON Generation**: Powering backend automation pipelines that require guaranteed compliance with structured schema templates (e.g., REST API payloads).
- **Multi-Step Tool Orchestration**: Parsing user intent, scheduling sequence actions, and calling consecutive terminal commands or external database tools.
- **Database Schema Analysis & SQL Generation**: Safely translating natural language queries into valid database queries on secure local servers.

## Strengths
- **Sub-100ms Tool Call Latency**: Highly optimized attention patterns and dense architecture enable extremely rapid time-to-first-token (TTFT) for tool routing.
- **Near-Zero JSON Validation Failures**: Specifically aligned to respect formatting constraints, preventing the parser crashes common with standard models.
- **Native Sequential Planning**: Fine-tuned using high-quality developer logs and agent trace datasets, allowing the model to decompose complex prompts into discrete logical steps.
- **Highly Compact Footprint**: The 10B parameter variant runs comfortably at high speeds on consumer GPUs.

## Limitations
- **Poor Conversational & Creative Depth**: Explicitly trained to be concise and direct; performs poorly on open-ended creative writing, poetry, or conversational humor.
- **Highly Specialized Vocabulary**: The model's token distribution is heavily biased toward programming languages, CLI commands, markdown structures, and system configurations.
- **High Quantization Sensitivity**: Requires high-fidelity quantization formats (such as 8-bit GGUF or EXL2) to preserve its rigid schema-compliance capabilities.

## When to use it
- When building local autonomous agent workforces (such as specialized coding or maintenance sub-agents).
- When your application requires high-frequency, reliable tool execution and strictly formatted JSON payloads.
- For local offline development environments where quick reasoning speeds and direct code generation are prioritized over friendly conversation.

## When not to use it
- As a general-purpose, customer-facing support chatbot where conversational empathy, storytelling, or broad general knowledge is required (where frontier models like Claude 5.1, Gemini 4.0 Pro, or GPT-5.5 excel).
- For non-technical translation tasks or creative writing brainstorm sessions.
- If your system does not utilize tool-calling, APIs, or structured program logic; standard general-purpose models like Llama 4, Qwen 3.6, or Gemma 3 are more versatile.

## Getting started
1. **Prerequisites**: Ensure you have Python 3.10+, PyTorch 2.4+, and an NVIDIA GPU or Apple Silicon system with sufficient memory.
2. **Library Setup**: Install the required Transformers framework packages and Pydantic v2:
   ```bash
   pip install transformers accelerate torch sentencepiece pydantic>=2.0.0
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
You can execute and serve Monolith-10 locally to expose a standardized high-performance API endpoint.

```bash
# Serve Monolith-10 using vLLM to expose a local OpenAI-compatible endpoint
python3 -m vllm.entrypoints.openai.api_server \
    --model basaltlabs/monolith-10 \
    --port 8000 \
    --dtype bfloat16

# Query the local model directly using curl to test strict JSON schema generation
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
The following script demonstrates how to leverage Monolith-10 to dynamically select and format tool arguments based on user input, strictly validated using **Pydantic v2**.

```python
import json
from typing import Literal, Union
from pydantic import BaseModel, Field, ValidationError
import openai

# Define strict schemas using Pydantic v2
class GCalSyncReferenceArgs(BaseModel):
    target_db_url: str = Field(..., description="Target database connection string URL.")
    force_sync: bool = Field(default=False, description="Whether to force synchronize references.")

class PaperlessExportTextArgs(BaseModel):
    export_dir: str = Field(..., description="Directory path to export text files.")

class SelectedToolCall(BaseModel):
    tool_name: Literal["gcal_sync_reference", "paperless_export_text"] = Field(..., description="The name of the tool selected.")
    arguments: Union[GCalSyncReferenceArgs, PaperlessExportTextArgs] = Field(..., description="Arguments for the selected tool.")

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="basalt-key-placeholder"
)

# Prompt detailing available tools and requesting a structured JSON decision plan
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
    # Safely load JSON content
    raw_content = response.choices[0].message.content
    parsed_json = json.loads(raw_content)

    # Strictly validate against Pydantic model
    validated_plan = SelectedToolCall.model_validate(parsed_json)

    print("Structured Agent Decision Plan (Validated with Pydantic v2):")
    print(validated_plan.model_dump_json(indent=2))
except json.JSONDecodeError:
    print("JSON Decode Error. Raw output:", response.choices[0].message.content)
except ValidationError as e:
    print("Pydantic Validation Error:", e)
```

## Related tools / concepts
- [DeepSeek](./deepseek.md) — Advanced open-source models with high coding and logical reasoning capabilities including DeepSeek-V3.
- [Mistral AI](./mistral.md) — Efficient dense and Mixture-of-Experts local models optimized for high performance.
- [Together AI](./together.md) — High-performance inference provider hosting developer and agentic models.
- [Ollama](../../services/ollama.md) — Standard framework for running, packing, and managing localized language models.
- [vLLM](../infrastructure/vllm.md) — Advanced, memory-efficient LLM serving and optimization framework.
- [Codeium](../development_ops/codeium.md) — Fast local and cloud developer assistance integrated with agent-level interfaces.
- [Sourcegraph Cody](../development_ops/sourcegraph_cody.md) — Multi-repo codebase intelligence and context-aware agent assistant.

## Sources / references
- [Basalt Labs Official Hugging Face Workspace](https://huggingface.co/basaltlabs)
- [Reddit r/LocalLLaMA: BasaltLabs Monolith-10 Agent-Optimized Release](https://www.reddit.com/r/LocalLLaMA/comments/1uzjnnb/basaltlabsaimonolith10_huggingface/)
- [Agentic Reasoning and Schema-Steering Standards](https://github.com/basaltlabs/monolith)

## Contribution Metadata
- Last reviewed: 2026-12-21
- Confidence: high
