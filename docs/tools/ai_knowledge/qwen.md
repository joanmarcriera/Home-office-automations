# Qwen

## What it is
Qwen is a series of Large Language Models (LLMs) developed by Alibaba Cloud, including general-purpose (Qwen), coding (Qwen-Coder), and vision (Qwen-VL) models. It is one of the most capable open-weight model families available, particularly strong in coding, mathematics, and multilingual tasks.

## What problem it solves
Provides high-performance, open-weight alternatives to proprietary models like GPT-4o. It enables powerful local inference for coding assistants and private reasoning tasks without relying on cloud APIs.

## Where it fits in the stack
**LLM / Reasoning Engine (Open-weights)**. It can be used as a backend for local agents or via various inference providers.

## Typical use cases
- **Local Coding Assistance**: Using `Qwen2.5-Coder` for IDE completions and agentic refactoring.
- **Multilingual Applications**: Leveraging its strong performance across 29+ languages.
- **Large Context Analysis**: Utilizing the 256K context window of Qwen3 models for document processing.
- **Edge Deployment**: Running smaller variants (e.g., 0.5B, 1.5B, 3B) on mobile or low-power devices.
- **Hosted agent backends**: Using frontier Qwen variants through providers such as NVIDIA NIM when you want multimodal and tool-calling support without self-hosting the biggest checkpoints.

## Hosted inference notes

NVIDIA's March 2026 model card for `qwen3.5-122b-a10b` is a useful signal for how Qwen is being packaged for production inference:

- It is a 122B Mixture-of-Experts model with 10B active parameters.
- The published deployment supports text, image, and video inputs.
- The model is explicitly positioned for reasoning, coding, multimodal chat, and tool-calling agent workflows.
- Native context length is listed at 262,144 tokens, with YaRN-based extension to 1,010,000 tokens.

That matters because it shows Qwen is no longer only a self-hosted or Hugging Face story; there is now a clearer provider path for large, agent-ready Qwen deployments.

## Getting started

### Installation (via Ollama)
The easiest way to run Qwen locally is through Ollama.

```bash
ollama run qwen2.5-coder:7b
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
- **State-of-the-Art Coding**: `Qwen2.5-Coder` rivals much larger models in coding benchmarks.
- **Efficient Architecture**: Qwen3-Coder-Next uses a Mixture-of-Experts (MoE) architecture (e.g., 3B activated / 80B total parameters) for high performance with lower compute requirements.
- **Native Long Context**: Supports up to 256K tokens natively, ideal for large codebases.
- **Wide Model Range**: Scales from tiny edge models to massive 72B+ parameter powerhouses.
- **Growing hosted availability**: Provider-packaged deployments such as NVIDIA NIM make large multimodal Qwen variants easier to consume operationally.

## Limitations
- **Hardware for Large Models**: The 72B and 80B MoE models require significant VRAM (40GB+ even with quantization).
- **Nuance in Western Contexts**: Like other non-Western models, it may have different cultural biases or instruction-following nuances compared to Llama or GPT.

## When to use it
- For local development where data privacy is paramount.
- When you need a top-tier coding model that can be self-hosted.
- For tasks requiring long-context retrieval or reasoning.

## When not to use it
- If you lack the hardware to run models larger than 7B comfortably.
- If your workflow is strictly tied to a proprietary ecosystem (e.g., exclusive use of Claude Artifacts).

## Licensing and cost
- **Open Source**: Yes (Apache 2.0 or Qwen License depending on version)
- **Cost**: Free (Self-hosted) / Paid (via providers like Groq or Together AI)
- **Self-hostable**: Yes

## Related tools / concepts
- [Ollama (Service)](../../services/ollama.md)
- [DeepSeek](deepseek.md)
- [Local LLMs](local_llms.md)

## Sources / References
- [Official Website](https://qwenlm.github.io/)
- [Qwen GitHub](https://github.com/QwenLM/Qwen)
- [Hugging Face Collection](https://huggingface.co/Qwen)
- [NVIDIA NIM model card: qwen3.5-122b-a10b](https://build.nvidia.com/qwen/qwen3.5-122b-a10b/modelcard)

## Contribution Metadata

- Last reviewed: 2026-03-29
- Confidence: high
