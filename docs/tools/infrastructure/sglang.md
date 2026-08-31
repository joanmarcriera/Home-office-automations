# SGLang

## What it is
SGLang is a fast serving framework for large language models and vision-language models. It makes your interaction with models faster and more controllable by optimizing the runtime with features like RadixAttention. In January 2027, it has become the standard high-performance runtime for serving complex multi-agent reasoning chains and large multimodal models like DeepSeek-V4, Qwen 3.6 VL, Gemma 4, and Claude 5.6 integrations.

## What problem it solves
LLM applications often involve repetitive prompting, structured output requirements, and complex chaining. SGLang addresses these by providing a high-performance runtime that significantly reduces latency through aggressive caching (RadixAttention) and optimized kernels for constrained generation. It specifically solves the "First Token Latency" (TTFT) problem in long-context multi-turn conversations and agent tool-calling loops.

## Where it fits in the stack
**Infrastructure / Inference Engine**. It sits in the serving layer, specifically optimized for complex agentic workflows and vision-language tasks, competing directly with [vLLM](../infrastructure/vllm.md) and [Aphrodite Engine](../infrastructure/aphrodite-engine.md).

## Typical use cases
- **Multi-turn Chat & Agents**: High-performance serving where prompt history (system prompts, context, tool descriptions) is reused across multiple turns.
- **Structured Data Extraction**: Applications requiring complex, multi-turn JSON or regex-constrained generation (e.g., [Data Copilot Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)).
- **Vision-Language Applications**: Serving models like Qwen 3.6 VL, Gemma 4, or Gemini-compatible open weights with high throughput.
- **Agentic Workflows**: Powering frameworks like [AG2](../../tools/frameworks/ag2.md) or [Langflow](../../tools/frameworks/langflow.md) where state persistence and rapid tool-calling loops are critical.

## Strengths
- **RadixAttention**: Automatically caches and reuses the KV cache across different requests with shared prefixes, saving up to 90% of prompt processing costs for agents.
- **Fast Structured Generation**: Optimized engine for constrained generation (JSON Schema, regex) using compressed finite state machines.
- **Chunked Prefill**: Efficiently handles large prompt processing without blocking small generation tasks, improving overall system throughput.
- **Comprehensive VLM Support**: Native support and high performance for vision-based models with multi-image processing.
- **Native FastMCP 3.1 Integration**: Natively processes Model Context Protocol (FastMCP 3.1 Task Protocol) tool definitions, passing structured context directly into the RadixAttention loop for sub-10ms tool routing.

## Limitations
- **Hardware Bound**: Primarily targets NVIDIA GPUs (CUDA); support for other accelerators (ROCm, Gaudi) is trailing.
- **Ecosystem Maturity**: While rapidly growing, it has fewer community-contributed adapters compared to vLLM.
- **Complexity**: The native interpreter introduces a learning curve for developers used to simple OpenAI-style API calls.

## When to use it
- When your application relies on multi-turn interactions, massive system prompts, or shared prompt prefixes.
- When you need low-latency, reliable structured generation (e.g., for [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md)).
- When serving VLMs at production scale with high concurrency.

## When not to use it
- For basic, single-prompt text generation where [vLLM](vllm.md) might be more widely documented.
- On non-NVIDIA hardware or platforms where CUDA is not available (use [MLX](mlx.md) on Apple Silicon).

## Getting started
### Installation
```bash
# Install with all dependencies for local serving on CUDA 12.8
pip install "sglang[all]" --extra-index-url https://flashinfer.ai/whl/cu128/torch2.5
```

### Basic Server Launch
```bash
python -m sglang.launch_server \
    --model-path deepseek-ai/DeepSeek-V4-Base \
    --port 30000 \
    --mem-fraction-static 0.85
```

### Hardware Verification (RTX 5080/5090 16-24 GB)
| Model size | Precision | VRAM Needed | Status | Notes |
|---|---|---|---|---|
| Gemma 4 9B | fp16 | 18 GB | ✅ | Fits natively in RTX 5080 |
| Qwen 3.6 72B | AWQ 4-bit | 42 GB | ❌ | Requires dual GPU (RTX 5090 SLI) |
| DeepSeek-V4 70B | AWQ 4-bit | 40 GB | ✅ | Dual RTX 5080/5090 setup |

## CLI examples
### Launching with Quantization
```bash
# Launching an AWQ model for low-memory environments
python -m sglang.launch_server \
    --model-path Qwen/Qwen-3.6-72B-Instruct-AWQ \
    --quantization awq \
    --port 30000
```

### Monitoring via CLI
```bash
# Check server health and stats
curl http://localhost:30000/health
curl http://localhost:30000/stats
```

## API examples
### Structured Generation (Python SDK with Pydantic v2)
SGLang allows for highly efficient constrained generation using its native interpreter and standard schema-first Pydantic classes (v2).

```python
from pydantic import BaseModel, Field
import sglang as sgl

class UserInfo(BaseModel):
    name: str = Field(description="The user's full name")
    age: int = Field(description="The user's age in years")
    role: str = Field(description="The professional role or occupation")

@sgl.function
def extract_user_info(s, text):
    s += sgl.user(f"Extract user details from: {text}")
    # Force the engine to output strictly according to the Pydantic JSON schema
    s += sgl.assistant(sgl.gen("json_output", regex=UserInfo.model_json_schema()))

# Execute via runtime endpoint
runtime = sgl.RuntimeEndpoint("http://localhost:30000")
state = extract_user_info.run(text="Dr. Elizabeth Blackburn is a 77-year-old biologist.", backend=runtime)
print(state["json_output"])
```

### OpenAI Compatible API
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:30000/v1", api_key="sglang")

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Base",
    messages=[{"role": "user", "content": "What is RadixAttention?"}]
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [vLLM](vllm.md)
- [Text Generation Inference (TGI)](tgi.md)
- [Aphrodite Engine](aphrodite-engine.md)
- [llama.cpp](llama-cpp.md)
- [Inference engines](index.md)
- [JSON Schema](https://json-schema.org/)
- [AG2](../../tools/frameworks/ag2.md)
- [Langflow](../../tools/frameworks/langflow.md)
- [Data Copilot Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md)

## Sources / References
- [Official Website](https://sgl-project.github.io/)
- [SGLang GitHub Repository](https://github.com/sgl-project/sglang)
- [RadixAttention Technical Paper](https://arxiv.org/abs/2312.04515)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
