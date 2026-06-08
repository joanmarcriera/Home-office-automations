# vLLM

## What it is
vLLM is a high-throughput and memory-efficient inference and serving engine for LLMs. It is powered by **PagedAttention**, a new attention algorithm that manages attention keys and values (KV cache) more efficiently, similar to how virtual memory works in operating systems.

## What problem it solves
LLM serving is often bottlenecked by KV cache memory management. Traditional systems suffer from significant memory fragmentation and over-reservation. vLLM's PagedAttention allows KV cache memory to be stored in non-contiguous memory spaces, reducing waste to near-zero and enabling much higher batch sizes and overall throughput.

## Where it fits in the stack
Infra

## Typical use cases
- High-concurrency production LLM serving.
- Building OpenAI-compatible API endpoints for self-hosted models.
- High-throughput offline batch inference.

## Strengths
- **State-of-the-Art Throughput**: Significantly outperforms traditional serving engines.
- **Efficient Memory Usage**: PagedAttention minimizes KV cache fragmentation.
- **Continuous Batching**: Processes new requests immediately without waiting for the whole batch to finish.
- **Broad Model Support**: Native support for Llama, Mistral, Gemma, and many others.

## Advanced Serving: Multi-LoRA
vLLM supports serving multiple LoRA (Low-Rank Adaptation) adapters simultaneously on a single base model, allowing for efficient multi-tenant serving.

```bash
# Start server with LoRA support
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/base_model \
    --enable-lora \
    --lora-modules sql-lora=/path/to/sql-adapter chat-lora=/path/to/chat-adapter
```

```python
# Request using a specific adapter
response = openai.ChatCompletion.create(
    model="sql-lora",
    messages=[{"role": "user", "content": "Write a SQL query for..."}]
)
```

## Latency Optimization: Speculative Decoding
Speculative decoding uses a smaller, faster "draft" model to predict multiple tokens at once, which are then verified in parallel by the larger "target" model, significantly reducing per-token latency.

```bash
python -m vllm.entrypoints.openai.api_server \
    --model /path/to/llama-70b \
    --speculative-model /path/to/llama-7b \
    --num-speculative-tokens 5
```

## Prefix Caching and Prompt Sharing
vLLM automatically identifies and caches common prefixes across different requests. This is particularly effective for multi-turn conversations or system prompts, as the KV cache for the common prefix only needs to be computed once.

- **Enable automatic prefix caching**: Use the `--enable-prefix-caching` flag when starting the server.
- **Benefit**: Reduces time-to-first-token (TTFT) and saves memory when multiple users share the same context.

## Limitations
- **Hardware Specificity**: Primarily optimized for NVIDIA GPUs; support for other backends (AMD, TPU, CPU) is evolving.
- **Complexity**: Tuning for specific latency/throughput trade-offs can be complex.

## Hardware requirements

vLLM requires NVIDIA GPU (CUDA). fp16 (default) exceeds 8 GB for 7B+ models; use AWQ 4-bit or fp8 quantization on the RTX 4060. vLLM does not support Apple Silicon — use [MLX](mlx.md) or [Ollama](../../services/ollama.md) on macOS.

| Model size | Precision | Min VRAM | RTX 4060 8 GB | Notes |
|---|---|---|---|---|
| 7-8B | fp16 | 14-16 GB | ❌ Not viable | Exceeds 8 GB |
| 7-8B | AWQ 4-bit | 4-5 GB | ✅ Comfortable | `--quantization awq` |
| 7-8B | fp8 (W8A8) | 7-8 GB | ⚠️ Tight | Requires Ampere/Ada (RTX 30/40xx) |
| 13-14B | AWQ 4-bit | 7-8 GB | ⚠️ Tight | Near ceiling |
| 30B+ | AWQ 4-bit | 16 GB+ | ❌ Not viable | Multi-GPU required |

**Recommended launch for RTX 4060:**
```bash
python -m vllm.entrypoints.openai.api_server \
    --model TheBloke/Mistral-7B-Instruct-v0.2-AWQ \
    --quantization awq \
    --gpu-memory-utilization 0.85
```

## When to use it
- When you need to serve LLMs to a large number of concurrent users.
- When maximizing GPU utilization is a priority.
- When you require an OpenAI-compatible API interface.

## When not to use it
- For low-resource environments or consumer hardware without high-end NVIDIA GPUs (consider llama.cpp).
- For models or architectures not yet supported by vLLM's kernel optimizations.

## Getting started

### Installation
```bash
pip install vllm
```

### Minimal Python Example
```python
from vllm import LLM, SamplingParams

prompts = ["Hello, my name is", "The capital of France is"]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

llm = LLM(model="facebook/opt-125m")

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

## Related tools / concepts
- [Text Generation Inference (TGI)](tgi.md)
- [SGLang](sglang.md)
- [llama.cpp](llama-cpp.md)
- [Ollama](../../services/ollama.md)
- [Aphrodite Engine](aphrodite-engine.md)
- [vLLM Benchmark CLI](../benchmarking/llmperf.md)
- [TGI Quantization Patterns](./tgi.md)
- [SGLang RadixAttention](./sglang.md)

## Sources / References
- [Official Website](https://vllm.ai/)
- [GitHub](https://github.com/vllm-project/vllm)
- [Docs](https://docs.vllm.ai/)

## Contribution Metadata
- Last reviewed: 2026-05-17
- Confidence: high
