# Heretic / ARA

## What it is
Heretic (distributed as `heretic-llm` on PyPI) is an open-source command-line tool released in early 2026 by developer "p-e-w" that automates **abliteration**—the removal of safety alignment from open-weight language models. It implements the **ARA (Ablative Refusal Alignment)** method, using Optuna-driven optimization to find the ideal directional ablation parameters (based on research by Arditi et al., 2024).

## What problem it solves
It addresses the issue of "refusal alignment" in large language models, where models frequently refuse to answer harmless or contextually relevant queries due to over-zealous safety guardrails. Unlike manual abliteration, Heretic automates the process to achieve minimal refusal rates with significantly less "capability damage" (lower KL divergence) to the underlying model's reasoning.

## Where it fits in the stack
**AI Assistants & Knowledge / Local Models**. It is a researcher-centric tool used to modify the weights of models like [Gemma 3](../providers/gemma.md), [Qwen](../providers/qwen.md), or [Llama 4](../providers/llama.md) before they are deployed in local inference engines.

## Typical use cases
- **Research and Analysis**: Exploring model behavior without safety-induced bias.
- **Creative Writing**: Generating content that might trigger standard safety filters but is legitimate in a creative context.
- **System Stress Testing**: Testing the limits of model reasoning when guardrails are removed.
- **Uncensored RAG**: Providing a backend for [AnythingLLM](anythingllm.md) or [Dify](dify.md) that doesn't refuse processing of complex technical documents.

## Strengths
- **Automated Optimization**: Uses Optuna to find the best refusal vector automatically, matching expert-level manual results.
- **Minimal Performance Loss**: Achieves very low KL divergence (e.g., 0.16 on Gemma 3-12B), preserving the model's original intelligence and reasoning.
- **High Success Rate**: Capable of reducing refusal rates to near-zero (3/100 or lower in benchmark tests).
- **Efficiency**: Zero human effort required once the tool is configured for a specific model architecture.

## Limitations
- **Experimental**: The ARA method is still in research and may introduce unpredictable behaviors or "vibe" shifts in the model.
- **Safety Risks**: Removal of guardrails means the model can generate harmful content; users must apply their own application-level safety layers.
- **Compute Intensive**: The optimization process requires multiple runs or evaluations of the model to find the optimal vector.

## When to use it
- When you encounter persistent refusals for legitimate tasks with standard aligned models.
- For local-first applications where you manage your own safety boundaries and need the highest possible reasoning fidelity.

## When not to use it
- In production environments with untrusted users where safety guardrails are mandatory.
- If you lack the compute resources to perform the required optimization loops.
- If you require the most stable and predictable model behavior as provided by original vendors like [Anthropic](../providers/anthropic.md).

## Getting started

### Installation (PyPI)
The tool is typically installed via `pip` or `uv`.

```bash
pip install heretic-llm
```

### Basic Workflow
1. Load your target open-weight model.
2. Run the `heretic` command to begin the ablation process.
3. Export the resulting "abliterated" weights to GGUF or Safetensors.

## CLI examples

### Running Ablation
Automatically optimize the refusal vector for a local Llama 4 model.

```bash
heretic ablate --model ./llama-4-8b-it --eval-set custom_refusal_bench.json --output ./llama-4-8b-ablated
```

### Listing Vectors
List identified refusal vectors in a previously ablated model.

```bash
heretic list-vectors --model ./llama-4-8b-ablated
```

## API examples

### Programmatic Ablation (Python)
Researchers can use the `heretic` library to integrate ablation into custom fine-tuning pipelines.

```python
import torch
from heretic import Abliterator
from transformers import AutoModelForCausalLM

# Load model
model = AutoModelForCausalLM.from_pretrained("./base-model")

# Initialize abliterator with Optuna optimization
abliterator = Abliterator(model, optimization="optuna")

# Find and apply the refusal vector
ablated_model = abliterator.run(trials=50)

# Save the abliterated model
ablated_model.save_pretrained("./abliterated-model")
```

## Related tools / concepts
- [Qwen](../providers/qwen.md)
- [Local LLMs](../../knowledge_base/local_llms.md)
- [llama.cpp](../infrastructure/llama-cpp.md)
- [Ollama](../../services/ollama.md)
- [AnythingLLM](anythingllm.md)
- [Dify](dify.md)
- [MMLU](../benchmarking/mmlu.md)
- [Gemma](../providers/gemma.md)
- [Llama](../providers/llama.md)
- [Optuna](https://optuna.org/)

## Sources / References
- [Heretic vs Abliterated LLMs: Refusal Rates & Benchmarks (2026)](https://aithinkerlab.com/heretic-ai-abliteration-benchmarks-2026/)
- [Orthogonalization of LLM Refusal Vectors (Arditi et al., NeurIPS 2024)](https://arxiv.org/abs/2406.11717)
- [Heretic: Automated Abliteration Tool (GitHub)](https://github.com/p-e-w/heretic)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
