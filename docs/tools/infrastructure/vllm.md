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

## Limitations
- **Hardware Specificity**: Primarily optimized for NVIDIA GPUs; support for other backends (AMD, TPU, CPU) is evolving.
- **Complexity**: Tuning for specific latency/throughput trade-offs can be complex.

## When to use it
- When you need to serve LLMs to a large number of concurrent users.
- When maximizing GPU utilization is a priority.
- When you require an OpenAI-compatible API interface.

## When not to use it
- For low-resource environments or consumer hardware without high-end NVIDIA GPUs (consider llama.cpp).
- For models or architectures not yet supported by vLLM's kernel optimizations.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

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

### Minimal CLI Example
```bash
python -m vllm.entrypoints.openai.api_server --model facebook/opt-125m
```

## Related tools / concepts
- [Text Generation Inference (TGI)](tgi.md)
- [SGLang](sglang.md)
- [llama.cpp](llama-cpp.md)

## Sources / References
- [Official Website](https://vllm.ai/)
- [GitHub](https://github.com/vllm-project/vllm)
- [Docs](https://docs.vllm.ai/)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
