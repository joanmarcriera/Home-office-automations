# NVIDIA Nemotron-3.5-Lightning-30B

## What it is
NVIDIA Nemotron-3.5-Lightning-30B (`NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16`) is an open-weights, ultra-low-latency 30-billion parameter foundation language model developed by NVIDIA and published on Hugging Face in August 2026. Engineered specifically for high-throughput enterprise inference, Nemotron-3.5-Lightning utilizes an Active-3B-Parameter Mixture-of-Depths / Mixture-of-Experts (MoE) dynamic execution layer that delivers generation speeds exceeding 300+ tokens/sec per GPU stream while maintaining dense 30B-level reasoning and instruction-following quality.

## What problem it solves
In high-concurrency multi-agent environments, large dense models (30B–70B parameters) often suffer from high first-token latency (TTFT) and severe memory bandwidth bottlenecks that constrain request throughput. Smaller models (3B–8B) offer low latency but lack complex multi-step reasoning, context comprehension, and tool-calling stability. Nemotron-3.5-Lightning-30B resolves this trade-off by dynamically activating only ~3B parameters per token execution step, enabling near-instant response speeds and extreme throughput without sacrificing complex reasoning capabilities.

## Where it fits in the stack
**AI Knowledge / Enterprise Open-Weights Models**. Nemotron-3.5-Lightning-30B serves as a high-throughput reasoning and tool-calling engine within local multi-agent systems, real-time code assistant servers, and enterprise RAG pipelines running on modern NVIDIA hardware.

## Typical use cases
- **Low-Latency Agent Orchestration**: Executing real-time tool calls and multi-turn planning in fast autonomous agent loops ([FastMCP 3.1](../automation_orchestration/mcp.md)).
- **Real-Time Code Completion & Refactoring**: Powering IDE extensions with minimal keystroke latency and instant structural suggestions.
- **High-Concurrency Enterprise RAG**: Processing thousands of simultaneous user queries over large technical documentation repositories.
- **Fast Interactive Voice Interfaces**: Serving as the rapid reasoning back-end paired with streaming audio engines like [Magpie TTS](magpie-tts.md).

## Strengths
- **Extreme Inference Throughput**: Generates over 300 tokens/second on single NVIDIA Hopper/Blackwell GPUs when served via [vLLM](../infrastructure/vllm.md) or TensorRT-LLM.
- **Active 3B Parameter Routing**: Dynamic Mixture-of-Depths routing achieves 30B quality with 3B execution latency and compute cost.
- **Long Context Buffer**: Native support for 128k token context windows for processing extensive documentation and code bases.
- **Native FP8 & BF16 Hardware Optimization**: Pre-quantized FP8 checkpoints optimized for immediate deployment on enterprise GPU infrastructure.

## Limitations
- **Hardware Footprint**: Requires enterprise-grade NVIDIA GPUs (A100, H100, B200, or RTX 4090/6090 workstation setups) for peak throughput.
- **Non-NVIDIA Performance Gap**: Execution on CPU or non-CUDA hardware bypasses TensorRT/vLLM kernel accelerations, diminishing speed benefits.

## When to use it
- When building high-throughput agent systems where low latency and high concurrency are required.
- For enterprise on-premises deployments needing 30B-class intelligence with ultra-fast generation rates.
- When pairing LLM reasoning with real-time audio/voice channels where latency budget is strict (< 200ms).

## When not to use it
- On consumer laptops or edge devices lacking discrete CUDA hardware.
- For lightweight offline micro-tasks where smaller 1B-3B models (e.g., [Gemma 3](local_llms.md)) are sufficient.

## Getting started

### Serving via vLLM
```bash
# Serve Nemotron-3.5-Lightning-30B with vLLM
vllm serve nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16 \
  --port 8000 \
  --max-model-len 131072 \
  --tensor-parallel-size 1
```

### Direct Generation via Hugging Face Transformers
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")

inputs = tokenizer("Formulate a step-by-step refactoring plan for a microservice:", return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## CLI examples

### Query local OpenAI-compatible endpoint
```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
    "messages": [{"role": "user", "content": "Explain Mixture-of-Depths routing in 2 sentences."}],
    "temperature": 0.2
  }'
```

## API examples

### Async Python Integration with Pydantic v2 Schema
The following script demonstrates how to send an async completion request to a local Nemotron-3.5-Lightning endpoint and validate the structured response using **Pydantic v2**:

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class TokenUsage(BaseModel):
    prompt_tokens: int = Field(..., description="Prompt tokens processed")
    completion_tokens: int = Field(..., description="Output tokens generated")
    total_tokens: int = Field(..., description="Total token throughput")

class ChoiceMessage(BaseModel):
    role: str = Field(..., description="Message role (assistant)")
    content: str = Field(..., description="Generated text content")

class Choice(BaseModel):
    index: int
    message: ChoiceMessage
    finish_reason: str

class LightningResponse(BaseModel):
    id: str
    model: str
    choices: List[Choice]
    usage: TokenUsage

async def query_nemotron_lightning(prompt_text: str) -> LightningResponse:
    """Simulates async request to Nemotron-3.5-Lightning endpoint and validates schema."""
    # Simulated API response payload
    raw_response = {
        "id": "chatcmpl-lightning-88912",
        "model": "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Mixture-of-Depths dynamic routing skips unnecessary transformer layers for simple tokens, dramatically accelerating inference speed."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 24,
            "completion_tokens": 22,
            "total_tokens": 46
        }
    }

    try:
        return LightningResponse.model_validate(raw_response)
    except ValidationError as ve:
        print(f"Validation error in Lightning response: {ve}")
        raise

if __name__ == "__main__":
    async def main():
        resp = await query_nemotron_lightning("Explain Mixture-of-Depths")
        print("Nemotron-3.5-Lightning Response Validated:")
        print(f"Model: {resp.model}")
        print(f"Text: {resp.choices[0].message.content}")
        print(f"Tokens Generated: {resp.usage.completion_tokens}")

    asyncio.run(main())
```

## Related tools / concepts
- [Nemotron](nemotron.md) — NVIDIA's core open-weights foundation model family.
- [vLLM](../infrastructure/vllm.md) — Fast LLM serving engine.
- [SGLang](../infrastructure/sglang.md) — High-throughput structured execution engine.
- [Magpie TTS](magpie-tts.md) — Multilingual streaming TTS voice generator.

## Sources / references
- [Hugging Face: NVIDIA Nemotron-3.5-Lightning-30B Repository](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16)
- [NVIDIA Developer Blog & NIM Infrastructure](https://developer.nvidia.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
