# NVIDIA

## What it is
NVIDIA is a global leader in AI hardware and software, providing an extensive ecosystem for model training, deployment, and inference through its GPU technology and the NVIDIA AI Enterprise platform.

## What problem it solves
NVIDIA provides the high-performance compute infrastructure necessary for modern AI. Through the NVIDIA API Catalog and NVIDIA NIM (NVIDIA Inference Microservices), it offers optimized, scalable inference for a wide range of open and proprietary models.

## Where it fits in the stack
**Compute Infrastructure / Model Provider / Inference Engine**. NVIDIA provides both the hardware (GPUs) and the software stack (CUDA, TensorRT, NIM) that powers much of the AI ecosystem.

## Typical use cases
- **Enterprise Model Deployment**: Using NVIDIA NIM for production-grade inference of models like Llama 3, Mistral, and Nemotron.
- **RAG Pipelines**: Utilizing NVIDIA NeMo Retriever for high-fidelity agentic retrieval.
- **Local AI Acceleration**: Running models locally with TensorRT-LLM for maximum performance on RTX GPUs.

## Getting started
NVIDIA offers a hosted API catalog for developers to test models:

1.  Visit [build.nvidia.com](https://build.nvidia.com/).
2.  Generate an API key.
3.  Use the OpenAI-compatible API to call models:

```python
from openai import OpenAI

client = OpenAI(
  base_url="https://integrate.api.nvidia.com/v1",
  api_key="$NVIDIA_API_KEY"
)

completion = client.chat.completions.create(
  model="nvidia/nemotron-3-super-120b",
  messages=[{"role":"user","content":"Explain the 120B MoE architecture."}],
  temperature=0.5,
  top_p=1,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")
```

## Strengths
- **Performance**: Industry-leading inference speeds through hardware-software co-optimization (TensorRT-LLM).
- **Broad Model Support**: Optimized NIMs available for almost all popular open-weights models.
- **Enterprise Grade**: Focus on security, manageability, and support through NVIDIA AI Enterprise.
- **Integration**: Strong ties with all major cloud providers and local workstation hardware.

## Limitations
- **Hardware Lock-in**: Many of NVIDIA's software optimizations are specific to their own GPU architecture.
- **Complexity**: The full enterprise stack can be complex to manage compared to simpler API-only providers.

## When to use it
- When you need the absolute highest performance for model inference.
- When deploying AI models in an enterprise environment requiring NIMs.
- For local acceleration on NVIDIA RTX hardware.

## When not to use it
- If you are committed to non-NVIDIA hardware (e.g., AMD, Apple Silicon, AWS Inferentia).
- For simple, low-volume projects where a basic API-only provider (like Groq or Together) might be simpler.

## Licensing and cost
- **Inference**: Usage-based pricing on the NVIDIA API Catalog; free trial credits usually available.
- **Software**: NVIDIA AI Enterprise requires a per-GPU or per-node license.
- **Open Weights**: NVIDIA-developed models like Nemotron are often released under the NVIDIA Nemotron Open Model License.

## Related tools / concepts
- [NVIDIA Nemotron-3 Super](../ai_knowledge/nemotron.md)
- [NVIDIA NeMo Retriever](../agents/nemo-retriever.md)
- [NVIDIA PersonaPlex](../ai_knowledge/personaplex.md)
- [Groq](groq.md)
- [Together AI](together.md)

## Sources / References
- [NVIDIA Official Website](https://www.nvidia.com/)
- [NVIDIA API Catalog](https://build.nvidia.com/)
- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)

## Contribution Metadata
- Last reviewed: 2026-05-14
- Confidence: high
- Related Issues: #192, #210
