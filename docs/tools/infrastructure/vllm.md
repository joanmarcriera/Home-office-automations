# vLLM

## What it is
vLLM is a high-throughput and memory-efficient inference and serving engine for LLMs. It is powered by **PagedAttention**, a new attention algorithm that manages attention keys and values (KV cache) more efficiently, similar to how virtual memory works in operating systems. It is the industry standard for open-source high-performance inference as of June 2026.

## What problem it solves
LLM serving is often bottlenecked by KV cache memory management. Traditional systems suffer from significant memory fragmentation and over-reservation. vLLM's PagedAttention allows KV cache memory to be stored in non-contiguous memory spaces, reducing waste to near-zero and enabling much higher batch sizes and overall throughput. This efficiency is critical for maintaining performance parity with frontier models like `claude-4-8-opus-20260528` and GPT-5.5 when running self-hosted models.

## Where it fits in the stack
**Infrastructure**. It serves as the primary inference engine and API server for self-hosted LLMs, providing an OpenAI-compatible interface.

## Typical use cases
- **High-concurrency production LLM serving**: Handling thousands of simultaneous requests efficiently.
- **OpenAI-compatible API endpoints**: Providing a drop-in replacement for proprietary APIs with self-hosted models.
- **High-throughput offline batch inference**: Processing large datasets with maximum GPU utilization.
- **Multi-LoRA serving**: Running dozens of specialized adapters on a single base model.

## Strengths
- **State-of-the-Art Throughput**: Significantly outperforms traditional serving engines through PagedAttention.
- **Efficient Memory Usage**: Minimizes KV cache fragmentation, allowing for larger batch sizes on the same hardware.
- **Continuous Batching**: Processes new requests immediately without waiting for the whole batch to finish.
- **Speculative Decoding**: Uses draft models to reduce per-token latency for large models.
- **Broad Model Support**: Native support for Llama-4 Maverick, Mistral, Gemma, and DeepSeek architectures.

## Limitations
- **Hardware Specificity**: Primarily optimized for NVIDIA GPUs; while AMD, TPU, and CPU support exists, they often lack the full performance optimizations of the CUDA backend.
- **Complexity**: Advanced features like multi-node tensor parallelism and speculative decoding require significant configuration expertise.
- **Startup Latency**: Large models and complex prefix caching configurations can lead to slow initial startup times.

## When to use it
- When you need to serve LLMs to a large number of concurrent users with minimal latency.
- When maximizing GPU utilization and throughput is the primary requirement.
- When you require an OpenAI-compatible API interface for existing application integration.
- When serving multiple LoRA adapters simultaneously is needed for multi-tenant environments.

## When not to use it
- For low-resource environments or consumer hardware without high-end NVIDIA GPUs (consider [llama.cpp](llama-cpp.md)).
- For simple, single-user local inference where [Ollama](../../services/ollama.md) provides a better UX.
- If the target model architecture is not yet supported by vLLM's optimized kernels.

## Getting started
vLLM can be installed via pip or run via Docker. NVIDIA GPU with CUDA 12+ is highly recommended.

```bash
# Installation
pip install vllm

# Start an OpenAI-compatible server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-4-Maverick-8B-Instruct \
    --quantization awq
```

## CLI examples
### 1. Basic Server Launch
Launch the OpenAI-compatible API server with a specific model.
```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000
```

### 2. Multi-LoRA Support
Start the server with support for multiple LoRA adapters.
```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
    --enable-lora \
    --lora-modules sql-lora=/path/to/sql-adapter chat-lora=/path/to/chat-adapter
```

### 3. Speculative Decoding
Run a large model with a smaller draft model to improve latency.
```bash
vllm serve meta-llama/Llama-4-Maverick-70B \
    --speculative-model meta-llama/Llama-4-Maverick-8B \
    --num-speculative-tokens 5
```

## API examples
Using the `vllm` Python library for offline batch inference.

```python
from vllm import LLM, SamplingParams

prompts = ["Explain PagedAttention in the context of June 2026 AI systems."]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=100)

llm = LLM(model="meta-llama/Llama-3.1-8B-Instruct")

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Generated text: {output.outputs[0].text}")
```

## Related tools / concepts
- [Text Generation Inference (TGI)](tgi.md) — Production-grade inference server by Hugging Face.
- [SGLang](sglang.md) — High-performance serving framework with RadixAttention.
- [llama.cpp](llama-cpp.md) — Lightweight C++ implementation for local inference.
- [Ollama](../../services/ollama.md) — Simplified local LLM management and serving.
- [Aphrodite Engine](aphrodite-engine.md) — vLLM fork optimized for creative writing.
- [vLLM Benchmark CLI](../benchmarking/llmperf.md) — Tool for benchmarking inference performance.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for connecting vLLM to agentic tools.

## Sources / references
- [Official Website](https://vllm.ai/)
- [GitHub](https://github.com/vllm-project/vllm)
- [Docs](https://docs.vllm.ai/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
