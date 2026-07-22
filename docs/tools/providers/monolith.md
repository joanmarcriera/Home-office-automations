# Monolith

## What it is
Monolith is a developer-centric, agent-optimized open-source model series developed by Basalt Labs. The flagship model, **Monolith-10**, is a highly specialized dense parameter model explicitly tuned to serve as an extremely low-latency, localized engine for autonomous multi-agent loops, complex tool calling, sequential planning, and structured syntax execution.

## What problem it solves
Standard general-purpose large language models are highly prone to formatting errors (such as outputting invalid JSON during complex tool calls) and struggle with long-horizon logical planning. Monolith solves these development challenges by embedding rigid grammar alignment and agentic planning constructs directly into the model's core representation. It yields near-perfect compliance with complex JSON schemas and outputs programmatic commands with extreme speed and structural integrity.

## Where it fits in the stack
**AI Model / Local LLM / Agent & Developer Provider**. Monolith sits at the localized intelligence layer of the development stack. It acts as the core planner and orchestrator for autonomous agent nodes, integrating seamlessly with local Integrated Development Environments (IDEs), command-line dev interfaces, and [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) server architectures.

## Typical use cases
- **High-Speed Autonomous Coding**: Serving as the task-routing and structural code-generation planner in multi-agent software engineering workflows.
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
- As a general-purpose, customer-facing support chatbot where conversational empathy, storytelling, or broad general knowledge is required.
- For non-technical translation tasks or creative writing brainstorm sessions.
- If your system does not utilize tool-calling, APIs, or structured program logic; standard general-purpose models like Llama or Gemma are more versatile.

## Getting started
1. **Prerequisites**: Ensure you have Python 3.10+, PyTorch 2.0+, and an NVIDIA GPU or Apple Silicon system with sufficient memory.
2. **Library Setup**: Install the required Transformers framework packages:
   ```bash
   pip install transformers accelerate torch sentencepiece
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
The following script demonstrates how to leverage Monolith-10 to dynamically select and format tool arguments based on user input.

```python
import json
import openai

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
        {"role": "system", "content": "You are an agent orchestrator. Output only the selected tool call in raw JSON."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.0
)

try:
    plan = json.loads(response.choices[0].message.content)
    print("Structured Agent Decision Plan:")
    print(json.dumps(plan, indent=2))
except json.JSONDecodeError:
    print("Raw output:", response.choices[0].message.content)
```

## Related tools / concepts
- [DeepSeek](./deepseek.md) — Advanced open-source models with high coding and logical reasoning capabilities.
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
- Last reviewed: 2026-07-21
- Confidence: high
