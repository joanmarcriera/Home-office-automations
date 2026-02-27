# vLLM

## What it is
vLLM is a fast and easy-to-use library for LLM inference and serving. It achieves high throughput by using **PagedAttention**, an attention algorithm that manages attention keys and values efficiently, inspired by virtual memory in operating systems.

## What problem it solves
LLM inference is often bottlenecked by the memory management of KV (key-value) caches. Traditional methods lead to memory fragmentation and over-allocation. vLLM's PagedAttention allows for near-zero waste in KV cache memory, enabling significantly higher batch sizes and throughput.

## Where it fits in the stack
**Infra** — It serves as the core inference engine in the infrastructure layer, often used to power OpenAI-compatible API servers.

## Typical use cases
- High-throughput serving of LLMs (e.g., Llama 3, Mistral) in production.
- Offline batched inference for large datasets.
- Multi-GPU distributed inference via Ray or NCCL.

## Strengths
- **PagedAttention**: Efficient memory management of KV cache.
- **Continuous Batching**: High throughput by processing requests as they arrive.
- **OpenAI-Compatible**: Drop-in replacement for OpenAI API.
- **Broad Model Support**: Supports most popular transformer architectures.

## Limitations
- **Hardware Requirements**: Optimized primarily for NVIDIA GPUs (though support for AMD, Intel, and others is growing).
- **Latency vs Throughput**: While throughput is exceptional, it may not always be the lowest-latency option for single-request scenarios compared to specialized runtimes like llama.cpp for small models.

## When to use it
- When you need to serve LLMs to many concurrent users.
- When you have high-end GPUs (A100, H100) and want to maximize utilization.
- When you need an OpenAI-compatible interface for your self-hosted models.

## When not to use it
- For low-resource environments (e.g., consumer laptops without dedicated GPUs) where llama.cpp might be better.
- For non-transformer based models that are not yet supported.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install vllm
```

### Minimal Python Example (Offline Inference)
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

### Minimal CLI Example (OpenAI-Compatible Server)
```bash
python -m vllm.entrypoints.openai.api_server --model facebook/opt-125m
```

## Related tools / concepts
- [llama.cpp](llama-cpp.md)
- [Text Generation Inference (TGI)](tgi.md)
- [Ollama](../../services/ollama.md)

## Sources / References
- [Official Website](https://vllm.ai/)
- [GitHub](https://github.com/vllm-project/vllm)
- [Docs](https://docs.vllm.ai/)

## Contribution Metadata
- Last reviewed: 2026-02-27
- Confidence: high
