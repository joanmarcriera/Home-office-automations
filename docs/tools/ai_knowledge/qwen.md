# Qwen

## What it is
Qwen is a series of Large Language Models (LLMs) developed by Alibaba Cloud, including general-purpose (Qwen), coding (Qwen-Coder), and vision (Qwen-VL) models. As of June 2026, the family features standout agentic variants such as **Qwen 3.6-35B-A3B** (latest frontier variant), **Qwen 3.5-Max-Preview**, and **Qwen 3.5-Plus**, which continue to push the boundaries of reasoning and agentic performance. It remains one of the most capable model families available, particularly strong in coding, mathematics, and complex multi-agent workflows, often competing directly with **Claude 4.7** and **GPT-5.5** in technical benchmarks.

## What problem it solves
Provides high-performance, open-weight alternatives to proprietary models. It enables powerful local inference for coding assistants and private reasoning tasks without relying on cloud APIs. Qwen's efficiency (e.g., the A3B architecture) solves the "compute bottleneck" for high-performance local agents.

## Where it fits in the stack
**LLM / Reasoning Engine (Open-weights)**. It can be used as a backend for local agents or via various inference providers. It is a core component of the [Local LLMs](local_llms.md) ecosystem.

## Typical use cases
- **Local Coding Assistance**: Using `Qwen3.6-35B-A3B` and `Qwen2.5-Coder` for IDE completions and agentic refactoring. Qwen 3.5 4B has demonstrated the ability to "vibe code" fully working OS web apps in one go.
- **Agent Swarms**: Leveraging the **agentic reasoning** and **thinking preservation** introduced in Qwen 3.6 for massive parallel workflows and complex reasoning tasks.
- **Multilingual Applications**: Leveraging its strong performance across 29+ languages.
- **Large Context Analysis**: Utilizing the 256K context window for deep document processing.
- **Edge Deployment**: Running smaller variants (e.g., 0.8B, 1.5B, 3B, 4B) on mobile or low-power devices. The 0.8B model is capable of running on a watch.
- **Hosted agent backends**: Using frontier Qwen variants through providers such as NVIDIA NIM or OpenRouter when you want multimodal and tool-calling support without self-hosting the biggest checkpoints.

## Hosted inference notes

NVIDIA's March 2026 model card for `qwen3.5-122b-a10b` and OpenRouter's April 2026 release of `qwen3.6-35b-a3b` are useful signals for how Qwen is being packaged for production inference:

- **Qwen 3.6-35B-A3B**: A 35B parameter MoE model with only 3B active parameters per token. It uses a hybrid sparse mixture-of-experts architecture combining Gated DeltaNet linear attention with standard gated attention layers.
- **Context & Multimodal**: These models support a 262K token native context window (extensible to 1M via YaRN) and accept text, image, and video inputs.
- **Agent Readiness**: Published deployments explicitly support function calling, structured output, and "integrated thinking mode" with reasoning traces.

## Getting started

### Installation (via Ollama)
The easiest way to run Qwen locally is through Ollama.

```bash
ollama run qwen2.5-coder:7b
# Qwen 3.6 variants arriving shortly to Ollama library
```

### Minimal Python Example (via OpenAI-compatible API)
If running via Ollama, you can use the OpenAI client:

```python
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama', # required but unused
)

response = client.chat.completions.create(
  model="qwen2.5-coder:7b",
  messages=[
    {"role": "user", "content": "Write a python function to calculate fibonacci numbers."}
  ]
)
print(response.choices[0].message.content)
```

## Strengths
- **State-of-the-Art Coding**: `Qwen3.6` and `Qwen3.5` variants set new bars for coding performance. The **Qwen 3.6-35B-A3B** variant achieves frontier-style coding and agent performance with only 3B active parameters.
- **Thinking Preservation**: Introduces the ability to retain reasoning context from historical messages to make iterative agentic work more stable and efficient.
- **Efficient Architecture**: Qwen 3.6-35B-A3B utilizes roughly 3B active parameters, providing a massive performance-to-compute ratio under an Apache 2.0 license.
- **Native Long Context**: Supports up to 256K tokens natively, ideal for large codebases. The tiny 0.8B model has demonstrated the ability to reason over a 100-file repository.
- **Wide Model Range**: Scales from tiny edge models (0.8B, 2B, 4B) to massive 72B+ and 122B parameter powerhouses.
- **Multimodal Capabilities**: Qwen3.6-35B-A3B is a multimodal causal language model with a vision encoder, supporting image and video input.
- **Community Optimizations**: `ik_llama.cpp` dramatically outperforms mainline for Qwen3.5/3.6 on CPU. Unsloth provides optimized GGUF updates for the series.

## Limitations
- **Hardware for Large Models**: The 72B and 122B MoE models require significant VRAM (40GB+ even with quantization).
- **Nuance in Western Contexts**: Like other non-Western models, it may have different cultural biases or instruction-following nuances compared to Llama or GPT.
- **Update Cadence**: The rapid release cycle can make it difficult for tooling maintainers to keep up with the latest architectural changes.

## When to use it
- For local development where data privacy is paramount.
- When you need a top-tier coding model that can be self-hosted.
- For tasks requiring long-context retrieval or reasoning (e.g., repository-level analysis).
- As a specialized tool-calling model in a multi-agent swarm.

## When not to use it
- If you lack the hardware to run models larger than 7B comfortably.
- If your workflow is strictly tied to a proprietary ecosystem (e.g., exclusive use of Claude Artifacts).

## Licensing and cost
- **Open Source**: Yes (Apache 2.0 or Qwen License depending on version)
- **Cost**: Free (Self-hosted) / Paid (via providers like Groq, Together AI, or OpenRouter)
- **Self-hostable**: Yes

## Related tools / concepts
- [Whisper](../../services/whisper.md) (Qwen3 ASR has been noted to outperform Whisper in almost every aspect)
- [Ollama (Service)](../../services/ollama.md)
- [DeepSeek](../providers/deepseek.md)
- [Local LLMs](local_llms.md)
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md)
- [Claude 4.7 Comparison](claude.md)
- [Llama 4 Maverick Comparison](../providers/meta.md)

## Sources / References
- [Official Website](https://qwenlm.github.io/)
- [Qwen 3.5 Release Blog](https://qwenlm.github.io/blog/qwen2.5-coder/)
- [Qwen GitHub](https://github.com/QwenLM/Qwen)
- [Hugging Face: Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B)
- [OpenRouter: Qwen3.6 35B A3B](https://openrouter.ai/qwen/qwen3.6-35b-a3b)
- [NVIDIA NIM model card: qwen3.5-122b-a10b](https://build.nvidia.com/qwen/qwen3.5-122b-a10b/modelcard)

## Contribution Metadata

- Last reviewed: 2026-06-08
- Confidence: high
