# SGLang

## What it is
SGLang (Structured Generation Language) is a fast serving framework designed for Large Language Models and Vision Language Models. It focuses on accelerating "structured" generation where LLM outputs need to follow a specific format (e.g., JSON, multiple-choice) or involve complex prompting workflows.

## What problem it solves
Complex LLM workflows often involve repetitive prompts, multiple calls, and structured output requirements, which can be slow and inefficient. SGLang optimizes these by using a **RadixAttention** mechanism for prefix caching across multiple requests and a fast runtime for constrained/structured generation.

## Where it fits in the stack
**Infra** — It is a high-performance inference runtime and server, particularly suited for agentic workflows and structured data extraction.

## Typical use cases
- Fast serving of LLMs for agentic workflows with long, shared system prompts.
- Structured data extraction (JSON, YAML) with high reliability and speed.
- Serving Vision Language Models (VLMs).

## Strengths
- **RadixAttention**: Automatically caches and reuses KV cache prefixes across requests.
- **Fast Structured Output**: Highly optimized engine for constrained generation.
- **VLM Support**: Excellent performance for vision-based models.
- **OpenAI-Compatible**: Provides a standard API interface.

## Limitations
- **Newer Ecosystem**: Documentation and community resources are still growing compared to vLLM.
- **Hardware**: Primarily optimized for NVIDIA GPUs.

## When to use it
- When your application uses complex, multi-turn dialogues or shared prefixes (e.g., agents).
- When you need low-latency structured generation.
- When you are working with VLMs.

## When not to use it
- For very simple, single-prompt text generation where vLLM might be more straightforward.
- In CPU-only environments.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install "sglang[all]"
```

### Minimal CLI Example (Launch Server)
```bash
python -m sglang.launch_server --model-path meta-llama/Llama-3.1-8B-Instruct --port 30000
```

### Querying with Python (OpenAI-Compatible)
```python
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:30000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="default",
    messages=[{"role": "user", "content": "Explain quantum entanglement."}],
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [vLLM](vllm.md)
- [Text Generation Inference (TGI)](tgi.md)
- [Guidance](https://github.com/guidance-ai/guidance) (Structured generation framework)

## Sources / References
- [GitHub](https://github.com/sgl-project/sglang)
- [Official Documentation](https://sgl-project.github.io/)

## Contribution Metadata
- Last reviewed: 2026-02-28
- Confidence: high
