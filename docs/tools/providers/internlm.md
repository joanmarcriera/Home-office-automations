# InternLM

## What it is
InternLM is an advanced, enterprise-grade open-weight large language model series developed by the Shanghai Artificial Intelligence Laboratory (Shanghai AI Lab) and key industry partners. Culminating in the high-performance **InternLM2.5** family and the ultra-large-scale **InternLM-Interns2-Preview-397B** Mixture-of-Experts (MoE) model, InternLM is engineered for extreme bilingual proficiency (English and Chinese), superior mathematical reasoning, multi-step agent tool call workflows, and long-context processing up to 1 million tokens.

## What problem it solves
Large-scale, multi-agent enterprise automation platforms require reasoning engines that are highly stable, open-weight, and free from restrictive commercial licensing. InternLM solves these demands by delivering state-of-the-art benchmark-grade performance in coding, logical inference, and complex mathematics natively in local and hybrid cloud environments. Its MoE architecture enables cost-effective activation of subset routing weights, minimizing compute costs while maintaining extreme performance scaling.

## Where it fits in the stack
**AI Model / Local LLM / Bilingual Provider**. Within the home lab or enterprise developer stack, InternLM resides at the intelligence provider layer. It can be served locally using high-throughput engines like [vLLM](../infrastructure/vllm.md) or [SGLang](../infrastructure/sglang.md), managed via [Ollama](../../services/ollama.md), or integrated directly with [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers for autonomous tool use.

## Typical use cases
- **Complex Bilingual RAG**: Managing and retrieving structured or unstructured knowledge across highly diverse English and Chinese documentation silos.
- **Autonomous Multi-Step Agents**: Powering reasoning agent loops that require highly reliable function calling and structured JSON output.
- **Extreme Long-Context Code Analysis**: Reviewing full-code repository contexts and generating complex refactoring solutions utilizing its 1M context support.
- **Edge Math & Logic Engines**: Running sovereign quantitative financial models or legal parsing pipelines where data privacy is paramount.

## Strengths
- **Massive MoE Efficiency**: The Interns2-Preview-397B MoE model utilizes highly optimized top-2 routing, activating only a fraction of its total weights per token to minimize runtime latency.
- **Excellent Tool-Use Stability**: Demonstrates extremely high zero-shot function-calling accuracy, on par with leading proprietary cloud models.
- **1-Million Token Window**: Natively scales context length up to 1M tokens through localized rotary position embedding (RoPE) and specialized attention mechanisms.
- **Permissive Open-Weight License**: Released under free and open commercial licenses, providing maximum security for private home-office operations.

## Limitations
- **High VRAM footprint for MoE**: Hosting the 397B parameter preview requires enterprise-grade multi-GPU nodes (e.g., multiple H100 or A100 systems).
- **Quantization Complexity**: Finding optimal bits-per-weight EXL2 or GGUF profiles for the Mixture-of-Experts model is more complex than standard dense models.
- **High Base Latency without serving engines**: Requires optimized runtimes like LMDeploy or vLLM to achieve low time-to-first-token (TTFT).

## When to use it
- When you require a localized bilingual reasoning engine with state-of-the-art math and code-generation benchmark scores.
- When building multi-agent pipelines where models must reliably parse structured tool schemas and execute sequential commands.
- For local enterprise clusters equipped with high-density VRAM storage arrays.

## When not to use it
- On consumer edge hardware with limited VRAM (such as standalone laptops or edge microcomputers with less than 16GB RAM).
- For workflows that are exclusively English-language and do not benefit from bilingual multi-hop semantic mapping.
- If you require a fast, simple plug-and-play local installation; standard dense models like Llama 3B or Gemma 8B are better suited for lightweight setups.

## Getting started
1. **Prerequisites**: Python 3.10+, PyTorch 2.2+, and an NVIDIA GPU setup with CUDA 12.1+.
2. **Library Installation**: Install the Hugging Face `transformers` and accelerate libraries.
   ```bash
   pip install transformers accelerate sentencepiece protobuf torch
   ```
3. **Load Model via Python**: Create a local script to load the InternLM2.5 dense model:
   ```python
   import torch
   from transformers import AutoTokenizer, AutoModelForCausalLM

   model_id = "internlm/internlm2_5-7b-chat"
   tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
   model = AutoModelForCausalLM.from_pretrained(
       model_id,
       torch_dtype=torch.bfloat16,
       trust_remote_code=True,
       device_map="auto"
   )
   model = model.eval()
   ```

## CLI examples
You can serve InternLM using standard serving runtimes to expose an OpenAI-compatible web API.

```bash
# Serve InternLM2.5 7B Chat locally via LMDeploy
pip install lmdeploy
lmdeploy serve api_server internlm/internlm2_5-7b-chat --server-port 23333 --tp 1

# Servicing using vLLM in a multi-GPU environment
python3 -m vllm.entrypoints.openai.api_server \
    --model internlm/internlm2_5-7b-chat \
    --tensor-parallel-size 2 \
    --port 8000 \
    --trust-remote-code
```

## API examples
The following script demonstrates querying InternLM2.5 served via vLLM using the standard OpenAI client protocol.

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="local-placeholder"
)

response = client.chat.completions.create(
    model="internlm/internlm2_5-7b-chat",
    messages=[
        {"role": "system", "content": "You are a helpful software engineer assistant."},
        {"role": "user", "content": "Explain how to write a custom MCP server in Python."}
    ],
    temperature=0.2,
    max_tokens=300
)

print(response.choices[0].message.content)
```

## Related tools / concepts
- [DeepSeek](./deepseek.md) — SOTA open-source models specializing in reasoning, coding, and mathematical operations.
- [Mistral AI](./mistral.md) — Open-weight pioneer delivering highly scalable dense and MoE local models.
- [Moonshot AI](./moonshot.md) — Chinese-based proprietary provider optimizing long-context language processing.
- [Qwen](../ai_knowledge/qwen.md) — Alibaba's flagship open-weights model suite with exceptional multilingual performance.
- [Ollama](../../services/ollama.md) — Lightweight, terminal-native local LLM orchestration framework.
- [vLLM](../infrastructure/vllm.md) — Extremely high-throughput serving runtime utilizing PagedAttention.
- [SGLang](../infrastructure/sglang.md) — Fast local serving framework optimized for structured outputs and prompt compilation.

## Sources / references
- [InternLM Official GitHub Repository](https://github.com/InternLM/InternLM)
- [Shanghai AI Lab Hugging Face Hub](https://huggingface.co/internlm)
- [Reddit r/LocalLLaMA: InternLM-Interns2-Preview-397B Announcement and Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1uzifq8/internlminterns2preview397b_huggingface/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
