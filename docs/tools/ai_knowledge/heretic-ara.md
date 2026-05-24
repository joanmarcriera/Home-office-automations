# Heretic / ARA

## What it is
Heretic is an experimental AI model project that implements the **ARA (Ablative Refusal Alignment)** decensoring method. It aims to provide high-performance models with minimal to no refusal behavior while maintaining reasoning capabilities by surgically removing the "refusal vector" from the model's weights.

## What problem it solves
It addresses the issue of "refusal alignment" in large language models, where models frequently refuse to answer harmless or contextually relevant queries due to over-zealous safety guardrails. This is particularly useful for [Local LLMs](../../knowledge_base/local_llms.md) where users want full control over their model's output.

## Where it fits in the stack
**AI Assistants & Knowledge / Local Models**. It is typically used by researchers and enthusiasts who require uncensored or "abliterated" models for specific use cases within a [self-hosted infrastructure](../../architecture/infrastructure.md).

## Typical use cases
- **Research and Analysis**: Exploring model behavior without safety-induced bias.
- **Creative Writing**: Generating content that might trigger standard safety filters but is legitimate in a creative context.
- **System Stress Testing**: Testing the limits of model reasoning when guardrails are removed.
- **Uncensored RAG**: Providing a backend for [AnythingLLM](anythingllm.md) or [Dify](dify.md) that doesn't refuse processing of complex technical documents.

## Key Features
- **Ablative Refusal Alignment (ARA)**: A technique that identifies and "ablates" the specific neurons or directions responsible for refusal.
- **Zero-Shot Decensoring**: Does not require fine-tuning on harmful data; instead, it modifies the existing weights of models like [Qwen](qwen.md) or Llama.
- **Weight Orthogonalization**: Ensures that removing refusal behavior doesn't degrade performance on standard [Benchmarking](../benchmarking/README.md) tasks.

## Strengths
- **Minimal Refusal**: High success rate in answering queries that standard models refuse.
- **Preserved Reasoning**: Aims to maintain the underlying logic and reasoning of the base model despite decensoring.
- **Local Execution**: Compatible with common local inference engines like [llama.cpp](../infrastructure/llama-cpp.md) and [Ollama](../../services/ollama.md).

## Limitations
- **Experimental**: The ARA method is still in research and may introduce unpredictable behaviors.
- **Safety Risks**: Removal of guardrails means the model can generate harmful content if prompted; users must apply their own safety layers.
- **Hard to Reproduce**: The exact vectors for ablation can vary between model versions and architectures.

## When to use it
- When you encounter persistent refusals for legitimate tasks with standard aligned models.
- For local-first applications where you manage your own safety boundaries.

## When not to use it
- In production environments with untrusted users where safety guardrails are mandatory.
- If you require the most stable and predictable model behavior.

## Getting started

### Installation (Ollama)
Heretic models are often shared as GGUF files or via [Ollama](../../services/ollama.md).

```bash
# Pull a Heretic-based model (if available in the library)
ollama run heretic-qwen-7b

# Or create a model from a GGUF file
echo "FROM ./heretic-ara-model.gguf" > Modelfile
ollama create heretic-local -f Modelfile
```

## Technical examples

### ARA Vector Identification (Python)
Researchers use techniques like Orthogonalization to find the refusal vector.

```python
import torch
from transformers import AutoModelForCausalLM

# Load model
model = AutoModelForCausalLM.from_pretrained("base-model-path")

# Define refusal directions (example placeholder)
refusal_dirs = torch.load("ara_vectors.pt")

# Apply ablation to specific layers
for i, layer in enumerate(model.model.layers):
    if i in [10, 11, 12]: # Target middle layers
        layer.self_attn.o_proj.weight.data -= refusal_dirs[i]
```

## Maintenance & Troubleshooting
- **Perplexity Check**: If the model starts outputting gibberish after ablation, the refusal vector was likely too broad. Check against [MMLU](../../knowledge_base/mmlu.md) to ensure reasoning is intact.
- **Vibe Check**: Use a "vibe-check" prompt (e.g., "Tell me a joke about a lawyer") to confirm the model is actually decensored.

## Related tools / concepts
- [Qwen](qwen.md)
- [Local LLMs](../../knowledge_base/local_llms.md)
- [llama.cpp](../infrastructure/llama-cpp.md)
- [Ollama](../../services/ollama.md)
- [AnythingLLM](anythingllm.md)
- [Dify](dify.md)
- [MMLU](../../knowledge_base/mmlu.md)
- [Infrastructure Overview](../../architecture/infrastructure.md)

## Sources / References
- [Heretic has finally defeated GPT-OSS with a new decensoring method ARA](https://www.reddit.com/r/LocalLLaMA/comments/1rnic0a/heretic_has_finally_defeated_gptoss_with_a_new/)
- [Orthogonalization of LLM Refusal Vectors (Research Paper)](https://arxiv.org/abs/2406.11717)

## Contribution Metadata
- Last reviewed: 2026-05-24
- Confidence: high
