# SGLang

## What it is
SGLang is a fast serving framework for large language models and vision-language models. It makes your interaction with models faster and more controllable by optimizing the runtime with features like RadixAttention.

## What problem it solves
LLM applications often involve repetitive prompting, structured output requirements, and complex chaining. SGLang addresses these by providing a high-performance runtime that significantly reduces latency through aggressive caching (RadixAttention) and optimized kernels for constrained generation.

## Where it fits in the stack
Infra

## Typical use cases
- High-performance serving of LLMs and VLMs (Vision-Language Models).
- Applications requiring complex, multi-turn structured generation.
- Serving scenarios where prefix caching can significantly improve throughput (e.g., multi-turn chat, few-shot prompting).

## Strengths
- **RadixAttention**: Automatically caches and reuses KV cache across different requests with shared prefixes.
- **Fast Structured Generation**: Optimized engine for constrained generation.
- **Comprehensive VLM Support**: Excellent performance for vision-based models.
- **Native Interpreter**: Includes a high-level Python interface for complex LLM programming.

## Limitations
- **Hardware**: Primarily targets NVIDIA GPUs.
- **Ecosystem**: Newer than vLLM, so community integrations and documentation are still maturing.

## When to use it
- When your application relies on multi-turn interactions or shared prompt prefixes.
- When you need low-latency, reliable structured generation.
- When serving VLMs.

## When not to use it
- For basic, single-prompt text generation where vLLM might be more widely documented.
- On non-NVIDIA hardware.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [vLLM](vllm.md)
- [Text Generation Inference (TGI)](tgi.md)
- [Guidance](https://github.com/guidance-ai/guidance)

## Sources / References
- [Official Website](https://sgl-project.github.io/)
- [GitHub](https://github.com/sgl-project/sglang)
- [Docs](https://sgl-project.github.io/)

## Getting started

### Installation
```bash
pip install "sglang[all]"
```

### Minimal CLI Example (Launch Server)
```bash
python -m sglang.launch_server --model-path meta-llama/Llama-3.1-8B-Instruct --port 30000
```

### Minimal Python Example (OpenAI Compatible)
```python
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:30000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="default",
    messages=[{"role": "user", "content": "Explain prefix caching in one sentence."}],
)
print(response.choices[0].message.content)
```

## Contribution Metadata
- Last reviewed: 2026-03-02
- Confidence: high
