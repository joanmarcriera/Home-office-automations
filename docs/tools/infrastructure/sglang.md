# SGLang

## What it is
SGLang is a fast serving framework for large language models and vision-language models. It makes your interaction with models faster and more controllable by optimizing the runtime with features like RadixAttention.

## What problem it solves
LLM applications often involve repetitive prompting, structured output requirements, and complex chaining. SGLang addresses these by providing a high-performance runtime that significantly reduces latency through aggressive caching (RadixAttention) and optimized kernels for constrained generation.

## Where it fits in the stack
**Infra**. It sits in the serving layer, specifically optimized for complex agentic workflows and vision-language tasks.

## Typical use cases
- **Multi-turn Chat & Agents**: High-performance serving where prompt history is reused.
- **Structured Data Extraction**: Applications requiring complex, multi-turn JSON or regex-constrained generation.
- **Vision-Language Applications**: Serving models like LLaVA or Qwen-VL with high throughput.

## Strengths
- **RadixAttention**: Automatically caches and reuses KV cache across different requests with shared prefixes, essential for agents.
- **Fast Structured Generation**: Optimized engine for constrained generation (JSON Schema, regex).
- **Chunked Prefill**: Efficiently handles large prompt processing without blocking small generation tasks.
- **Comprehensive VLM Support**: Native support and high performance for vision-based models.
- **Native Interpreter**: Includes a high-level Python interface (SGLang runtime) for complex LLM programming.

## Limitations
- **Hardware**: Primarily targets NVIDIA GPUs (CUDA).
- **Ecosystem**: Newer than vLLM; integration with some third-party orchestrators may require custom adapters.

## Hardware requirements

SGLang requires NVIDIA GPU (CUDA). Its RadixAttention cache benefit scales with model size and concurrency — most valuable for 13B+ models with many parallel requests. No Apple Silicon support — use [MLX](mlx.md) or [Ollama](../../services/ollama.md) on macOS.

| Model size | Precision | Min VRAM | RTX 4060 8 GB | Notes |
|---|---|---|---|---|
| 7-8B | fp16 | 14-16 GB | ❌ Not viable | |
| 7-8B | AWQ 4-bit | 4-5 GB | ✅ Comfortable | `--quantization awq` |
| 7-8B | fp8 | 7-8 GB | ⚠️ Tight | Ampere/Ada required |
| 13-14B | AWQ 4-bit | 7-8 GB | ⚠️ Tight | Use `--mem-fraction-static 0.80` |
| 30B+ | any | 20 GB+ | ❌ Not viable | Multi-GPU only |

**Recommended launch for RTX 4060:**
```bash
python -m sglang.launch_server \
    --model-path TheBloke/Mistral-7B-Instruct-v0.2-AWQ \
    --quantization awq \
    --port 30000 \
    --mem-fraction-static 0.80
```

## When to use it
- When your application relies on multi-turn interactions or shared prompt prefixes.
- When you need low-latency, reliable structured generation.
- When serving VLMs at production scale.

## When not to use it
- For basic, single-prompt text generation where vLLM might be more widely documented.
- On non-NVIDIA hardware or platforms where CUDA is not available.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
```bash
pip install "sglang[all]"
```

### Advanced Server Configuration
Launch the server with chunked prefill and RadixAttention enabled (default):

```bash
python -m sglang.launch_server \
    --model-path meta-llama/Llama-3.1-8B-Instruct \
    --port 30000 \
    --chunked-prefill-size 512 \
    --mem-fraction-static 0.8
```

### Structured Generation (Python SDK)
SGLang allows for highly efficient constrained generation using its native interpreter.

```python
import sglang as sgl

@sgl.function
def multi_turn_question(s, question):
    s += sgl.user(question)
    s += sgl.assistant(sgl.gen("answer", max_tokens=100))
    s += sgl.user("Summarize that in 10 words.")
    s += sgl.assistant(sgl.gen("summary", max_tokens=50))

# Execute
state = multi_turn_question.run(
    question="What is RadixAttention?",
    backend=sgl.RuntimeEndpoint("http://localhost:30000")
)

print(state["answer"])
print(state["summary"])
```

## Core Architecture: RadixAttention
Unlike traditional LRU caching, **RadixAttention** manages the KV cache as a radix tree. When multiple requests share a prefix (e.g., a system prompt or a long document), SGLang identifies the shared node in the tree and reuses the pre-computed KV cache, eliminating redundant computation and significantly reducing time-to-first-token (TTFT).

## Related tools / concepts
- [vLLM](vllm.md)
- [Text Generation Inference (TGI)](tgi.md)
- [Aphrodite Engine](aphrodite-engine.md)
- [llama.cpp](llama-cpp.md)
- [Inference engines](index.md)
- [JSON Schema](https://json-schema.org/)
- [Python SDK](https://github.com/sgl-project/sglang/tree/main/python/sglang)

## Sources / References
- [Official Website](https://sgl-project.github.io/)
- [SGLang Python SDK](https://github.com/sgl-project/sglang/tree/main/python/sglang)
- [GitHub](https://github.com/sgl-project/sglang)
- [RadixAttention Technical Paper](https://arxiv.org/abs/2312.04515)

## Contribution Metadata
- Last reviewed: 2026-06-03
- Confidence: high
