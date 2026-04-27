# Qwen

## What it is
Qwen is a series of Large Language Models (LLMs) developed by Alibaba Cloud, including general-purpose (Qwen), coding (Qwen-Coder), and vision (Qwen-VL) models. It is one of the most capable open-weight model families available, particularly strong in coding, mathematics, and multilingual tasks.

## What problem it solves
Provides high-performance, open-weight alternatives to proprietary models like GPT-4o. It enables powerful local inference for coding assistants and private reasoning tasks without relying on cloud APIs.

## Where it fits in the stack
**LLM / Reasoning Engine (Open-weights)**. It can be used as a backend for local agents or via various inference providers.

## Typical use cases
- **Local Coding Assistance**: Using `Qwen3.5-Coder` and `Qwen2.5-Coder` for IDE completions and agentic refactoring. Qwen 3.5 4B has demonstrated the ability to "vibe code" fully working OS web apps in one go.
- **Multilingual Applications**: Leveraging its strong performance across 29+ languages.
- **Large Context Analysis**: Utilizing the 256K context window of Qwen3 models for document processing.
- **Edge Deployment**: Running smaller variants (e.g., 0.8B, 1.5B, 3B, 4B) on mobile or low-power devices. The 0.8B model is capable of running on a watch.
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
- **State-of-the-Art Coding**: `Qwen3.5` and `Qwen3.6` variants continue to push coding performance. The **Qwen3.6-35B-A3B** model (and its 3.5 predecessor) are standouts, achieving 37.8% on SWE-bench Verified Hard, matching or exceeding much larger proprietary models like Claude Opus 4.6.
- **Efficient Architecture**: Qwen3-Coder-Next and Qwen 3.5 variants use Mixture-of-Experts (MoE). The **35B-A3B** variant specifically utilizes roughly 3B active parameters, providing a massive performance-to-compute ratio under an Apache 2.0 license.
- **Native Long Context**: Supports up to 256K tokens natively, ideal for large codebases. The tiny 0.8B model has demonstrated the ability to reason over a 100-file repository.
- **Wide Model Range**: Scales from tiny edge models (0.8B, 2B, 4B) to massive 72B+ and 122B parameter powerhouses.
- **Multimodal Capabilities**: Qwen3.5-4B shows strong handwriting recognition performance.
- **Community Optimizations**: `ik_llama.cpp` dramatically outperforms mainline for Qwen3.5 on CPU. Unsloth provides optimized GGUF updates for the series.
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
- [Whisper](../../services/whisper.md) (Qwen3 ASR has been noted to outperform Whisper in almost every aspect)
- [Ollama (Service)](../../services/ollama.md)
- [DeepSeek](deepseek.md)
- [Local LLMs](local_llms.md)

## Sources / References
- [Official Website](https://qwenlm.github.io/)
- [Qwen GitHub](https://github.com/QwenLM/Qwen)
- [Hugging Face Collection](https://huggingface.co/Qwen)
- [Qwen 3.5 SWE-bench Results](https://www.reddit.com/r/LocalLLaMA/comments/1rkdlqi/qwen3535ba3b_hits_378_on_swebench_verified_hard/)
- [Qwen3.6-35B-A3B Agentic Coding](https://www.reddit.com/r/AIToolsPerformance/comments/1sn9okz/qwen3635ba3b_drops_with_apache_20_agentic_coding/)
- [NVIDIA NIM model card: qwen3.5-122b-a10b](https://build.nvidia.com/qwen/qwen3.5-122b-a10b/modelcard)
- [Final Qwen 3.5 Unsloth GGUF Update](https://www.reddit.com/r/LocalLLaMA/comments/1rlkptk/final_qwen35_unsloth_gguf_update/)
- [Qwen 3.5 0.8B reasoning over 100-file repo](https://www.reddit.com/r/LocalLLaMA/comments/1rmpdkc/i_made_a_tiny_08b_qwen_model_reason_over_a/)
- [Qwen 3.5 4B handwriting recognition](https://www.reddit.com/r/LocalLLaMA/comments/1rprouf/qwen354b_handwriting_recognition_is_really_good/)
- [Ryzen AI Max 395+ Benchmarks](https://www.reddit.com/r/LocalLLaMA/comments/1rpw17y/ryzen_ai_max_395_128gb_qwen_35_35b122b_benchmarks/)

## Contribution Metadata

- Last reviewed: 2026-04-27
- Confidence: high
