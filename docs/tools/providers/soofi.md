# Soofi

## What it is
Soofi is a sovereign, GDPR-aligned European open-source large language model suite featuring highly optimized variants such as **Soofi-30B** and **Soofi-3B**. Developed under a consortium of European digital sovereignty initiatives, Soofi is explicitly fine-tuned and steered for native proficiency in English, French, German, Spanish, and Italian. It provides localized linguistic nuance and robust logical reasoning while operating under a permissive, commercially friendly open-source license.

## What problem it solves
Enterprise automation pipelines in European jurisdictions face severe regulatory overhead when sending proprietary data to US-based proprietary cloud APIs. Soofi solves this by enabling fully offline, local inference that strictly complies with GDPR data minimization and privacy standards. It eliminates third-party transmission risks and provides European organizations with a high-performance alternative to proprietary models, ensuring complete digital sovereignty.

## Where it fits in the stack
**AI Model / Local LLM / European Sovereign Provider**. Within the home-office and enterprise stack, Soofi sits at the local model layer. It serves as a highly compliant, locally hosted reasoning core that can be orchestrated via [Ollama](../../services/ollama.md) or served via [vLLM](../infrastructure/vllm.md) to integrate with local databases, RAG systems, and [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) automation pipelines.

## Typical use cases
- **GDPR-Compliant Document Analysis**: Reviewing contracts, medical records, or user credentials locally on secure hardware without exposing personal data.
- **Sovereign Public Sector Chatbots**: Powering local government or public utility assistant tools that require strict data security compliance.
- **High-Nuance European Translation**: Executing multi-way translations across European languages with native-level grammatical accuracy and cultural awareness.
- **Private Home-Office Automation**: Acting as a privacy-focused offline smart home orchestrator that does not leak telemetry outside the local network.

## Strengths
- **Strict Compliance Design**: Developed from the ground up to prevent the ingestion and leakage of personally identifiable information (PII).
- **Strong European Multilingualism**: Outperforms comparable models in logical reasoning and fluency when evaluated in French, German, Spanish, and Italian.
- **Optimized 30B Architecture**: Strikes an ideal balance between reasoning depth and compute efficiency, enabling high-speed local serving.
- **Sovereign Control**: Allows absolute modification of model weights, steering behaviors, and fine-tuning parameters under local control.

## Limitations
- **Limited Non-European Languages**: Exhibits significantly lower logical fluency and vocabulary scope when prompted in East Asian or Middle Eastern languages.
- **Hardware Overhead for 30B**: Running the 30B parameter variant locally at high token speeds requires a minimum of 24GB VRAM (quantized) or 64GB+ unified memory.
- **Ecosystem Scale**: The community developer base and tooling ecosystem around Soofi is smaller than that of massive foundational suites like Llama.

## When to use it
- When your application is regulated under EU law (such as healthcare, banking, or municipal services) and data privacy is non-negotiable.
- When you require deep, accurate multilingual translation and reasoning among Western European languages.
- When hosting models fully offline on local GPU clusters or private European servers.

## When not to use it
- If your workflows rely heavily on non-European languages such as Chinese, Japanese, Arabic, or Hindi.
- For open-ended creative storytelling where highly conversational and sycophantic behavior is desired.
- When running on entry-level edge devices with less than 12GB of system RAM.

## Getting started
1. **Prerequisites**: Ensure you have Python 3.10+, PyTorch 2.0+, and an appropriate GPU environment.
2. **Installation**: Install the required packages via pip:
   ```bash
   pip install transformers accelerate sentencepiece torch
   ```
3. **Model Loading**: Initialize the Soofi-30B model with Hugging Face transformers:
   ```python
   import torch
   from transformers import AutoTokenizer, AutoModelForCausalLM

   model_id = "soofi/soofi-30b-chat"
   tokenizer = AutoTokenizer.from_pretrained(model_id)
   model = AutoModelForCausalLM.from_pretrained(
       model_id,
       torch_dtype=torch.bfloat16,
       device_map="auto"
   )
   ```

## CLI examples
You can run Soofi models directly in the terminal or serve them via popular orchestration stacks.

```bash
# Serve Soofi-30B locally using vLLM engine
python3 -m vllm.entrypoints.openai.api_server \
    --model soofi/soofi-30b-chat \
    --host 0.0.0.0 \
    --port 8000 \
    --dtype bfloat16

# Run Soofi-3B locally in an interactive terminal via Ollama
ollama run soofi:3b
```

## API examples
The following Python script queries a locally served Soofi-30B model via its OpenAI-compatible endpoint.

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="soofi-secure-token"
)

response = client.chat.completions.create(
    model="soofi/soofi-30b-chat",
    messages=[
        {"role": "system", "content": "You are a GDPR compliance audit assistant."},
        {"role": "user", "content": "Draft a short policy statement summarizing data minimization principles."}
    ],
    temperature=0.1,
    max_tokens=250
)

print(response.choices[0].message.content)
```

## Related tools / concepts
- [DeepSeek](./deepseek.md) — Flagship reasoning models delivering exceptional performance in localized or remote structures.
- [Mistral AI](./mistral.md) — High-performance European model suite serving both dense and MoE architectures.
- [Cohere](./cohere.md) — Enterprise-oriented model provider with robust support for secure multilingual systems.
- [Anthropic](./anthropic.md) — Leading safety-focused frontier model provider emphasizing alignment.
- [Ollama](../../services/ollama.md) — Key local orchestrator for serving, scaling, and managing offline language models.
- [vLLM](../infrastructure/vllm.md) — High-efficiency serving runtime with advanced PagedAttention management.
- [ExLlamaV2](../infrastructure/exllamav2.md) — Fast quantization and serving engine optimized for consumer NVIDIA GPUs.

## Sources / references
- [European Digital Sovereignty Association: Open LLM Workgroup](https://www.european-sovereignty.org/)
- [Reddit r/LocalLLaMA: Soofi's 30B & 3B Sovereign European Models Release](https://www.reddit.com/r/LocalLLaMA/comments/1uyysg1/soofi_s_30ba3b_european_open_source_model/)
- [Sovereign AI Initiative: High-Confidence Local Language Modeling](https://huggingface.co/soofi)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
