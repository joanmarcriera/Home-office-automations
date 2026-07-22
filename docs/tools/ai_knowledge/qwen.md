# Qwen

## What it is
Qwen is a series of Large Language Models (LLMs) developed by Alibaba Cloud, including general-purpose (Qwen), coding (Qwen-Coder), and vision (Qwen-VL) models. As of July 2026, the family features standout agentic variants such as **Qwen 3.6-35B-A3B** (latest frontier variant), the highly capable **Qwen 3.6-27B** with native 262k high-context support, **Qwen 3.5-Max-Preview**, and **Qwen 3.5-Plus**. It remains one of the most capable model families available, particularly strong in coding, mathematics, and complex multi-agent workflows, often competing directly with **Claude 4.8** and **GPT-5.5** in technical benchmarks.

## What problem it solves
Provides high-performance, open-weight alternatives to proprietary models. It enables powerful local inference for coding assistants and private reasoning tasks without relying on cloud APIs. Qwen's efficiency (e.g., the A3B architecture) solves the "compute bottleneck" for high-performance local agents, allowing frontier-level intelligence on consumer-grade hardware.

## Where it fits in the stack
**LLM / Reasoning Engine (Open-weights)**. It can be used as a backend for local agents or via various inference providers. It is a core component of the [Local LLMs](local_llms.md) ecosystem and a preferred target for [Ollama](../../services/ollama.md).

## Typical use cases
- **Local Coding Assistance**: Using `Qwen3.6-35B-A3B` and `Qwen2.5-Coder` for IDE completions and agentic refactoring.
- **Agent Swarms**: Leveraging the **agentic reasoning** and **thinking preservation** introduced in Qwen 3.6 for massive parallel workflows.
- **Multilingual Applications**: Leveraging its strong performance across 29+ languages for global document extraction.
- **Large Context Analysis**: Utilizing the 256K native context window for deep repository-level analysis.
- **Edge Deployment**: Running smaller variants (e.g., 0.8B, 1.5B) on mobile or low-power devices for "Invisible AI" tasks.

## Strengths
- **State-of-the-Art Coding**: `Qwen3.6` and `Qwen3.5` variants set new bars for coding performance, often outperforming Llama 4 in specialized benchmarks.
- **Thinking Preservation**: Introduces the ability to retain reasoning context from historical messages to make iterative agentic work more stable.
- **Efficient Architecture**: Qwen 3.6-35B-A3B utilizes roughly 3B active parameters, providing a massive performance-to-compute ratio.
- **Native Long Context**: Supports up to 256K tokens natively, ideal for large codebase ingestion without RAG overhead.
- **Multimodal Capabilities**: Support for image and video input is native to the causal language model architecture.

## Limitations
- **Hardware for Large Models**: The 72B and 122B MoE models require significant VRAM (40GB+ even with quantization).
- **Update Cadence**: The rapid release cycle can make it difficult for tooling maintainers (like Llama.cpp) to keep up with architectural changes.
- **Instruction Following**: While excellent, it can occasionally exhibit different nuances in instruction-following compared to Western-tuned models like Claude.

## When to use it
- For local development where data privacy and zero latency are paramount.
- When you need a top-tier coding model that can be self-hosted on a single GPU.
- For tasks requiring long-context retrieval or complex reasoning over large document sets.
- As a cost-effective backend for agent swarms using OpenRouter or NVIDIA NIM.

## When not to use it
- If you lack the hardware (min 8GB VRAM) to run the highly-capable 7B or 35B variants.
- If your workflow is strictly tied to a proprietary ecosystem with exclusive features (e.g., Google Workspace integration).

## Getting started
1. **Ollama**: The fastest way to run Qwen locally.
   ```bash
   ollama run qwen2.5-coder:7b
   ```
2. **OpenRouter**: To access frontier Qwen 3.6 variants without local hardware.
3. **vLLM**: For high-throughput production serving of Qwen checkpoints.

## CLI examples
The Qwen family is widely supported across common LLM command-line interfaces.

```bash
# Run the specialized coding variant via Ollama
ollama run qwen2.5-coder:14b

# Run Qwen 3.6 via local vLLM server
vllm serve Qwen/Qwen3.6-35B-A3B --port 8000

# Benchmark local Qwen inference speed
python3 -m llama_cpp.server --model ./models/qwen3.6-7b.gguf --n_gpu_layers -1
```

## API examples
Qwen models are typically accessed via OpenAI-compatible APIs.

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="qwen3.6-35b-a3b",
    messages=[
        {"role": "system", "content": "You are a senior engineer."},
        {"role": "user", "content": "Refactor this n8n expression for better readability."}
    ],
    extra_body={"thinking": True} # Enable reasoning traces in supported providers
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [Ollama (Service)](../../services/ollama.md): Primary delivery mechanism for local Qwen.
- [DeepSeek](../providers/deepseek.md): Competitive open-weight alternative.
- [Local LLMs](local_llms.md): The overarching category for self-hosted models.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md): Used to connect Qwen to local tools.
- [Whisper](../../services/whisper.md): Often paired with Qwen for audio-to-knowledge pipelines.
- [Llama 4 Maverick](../providers/meta.md): The primary Western competitor.
- [vLLM](../infrastructure/vllm.md): High-performance serving framework for Qwen.
- [Unsloth](../infrastructure/unsloth.md): Optimized fine-tuning for Qwen models.

## Sources / References
- [Official Qwen Website](https://qwenlm.github.io/)
- [Qwen 3.6 27B Context Window Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1uxstxs/qwen_36_27b_is_solid_up_to_262k_context_how_high/)
- [Qwen GitHub Repository](https://github.com/QwenLM/Qwen)
- [Hugging Face: Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B)
- [NVIDIA NIM Model Card: qwen3.5-122b-a10b](https://build.nvidia.com/qwen/qwen3.5-122b-a10b/modelcard)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
