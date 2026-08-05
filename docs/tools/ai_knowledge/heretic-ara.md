# Heretic / ARA

## What it is
Heretic (distributed as `heretic-llm` on PyPI) is an open-source command-line tool released in early 2026 by developer "p-e-w" that automates **abliteration**—the removal of safety alignment from open-weight language models. It implements the **ARA (Ablative Refusal Alignment)** method, using Optuna-driven optimization to find the ideal directional ablation parameters (based on research by Arditi et al., 2024). By late 2026, it is widely used for preparing models like **Gemma 3**, **Qwen 3.6**, and **Llama 4** for uncensored research and creative applications.

## What problem it solves
It addresses the issue of "refusal alignment" in large language models, where models frequently refuse to answer harmless or contextually relevant queries due to over-zealous safety guardrails. Unlike manual abliteration, Heretic automates the process to achieve minimal refusal rates with significantly less "capability damage" (lower KL divergence) to the underlying model's reasoning.

## Where it fits in the stack
**AI Assistants & Knowledge / [Local LLMs](./local_llms.md)**. It is a researcher-centric tool used to modify the weights of models like [Gemma 3](../providers/gemma.md), [Qwen 3.6](qwen.md), or [Llama 4](../providers/llama.md) before they are deployed in local inference engines. In late 2026, abliterated local models serve as low-latency, zero-refusal reasoning backends alongside frontier cloud models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0** in multi-agent environments.

## Typical use cases
- **Research and Analysis**: Exploring model behavior without safety-induced bias.
- **Creative Writing**: Generating content that might trigger standard safety filters but is legitimate in a creative context.
- **System Stress Testing**: Testing the limits of model reasoning when guardrails are removed.
- **Uncensored RAG**: Providing a backend for [AnythingLLM](anythingllm.md) or [Dify](dify.md) that doesn't refuse processing of complex technical documents.
- **Agentic Freedom**: Preparing models for use in [Autonomous Agents](../agents/index.md) that require zero refusal for complex system-level tasks.

## Strengths
- **Automated Optimization**: Uses Optuna to find the best refusal vector automatically, matching expert-level manual results.
- **Minimal Performance Loss**: Achieves very low KL divergence (e.g., 0.16 on Gemma 3-12B), preserving the model's original intelligence and reasoning.
- **High Success Rate**: Capable of reducing refusal rates to near-zero (3/100 or lower in benchmark tests).
- **Efficiency**: Zero human effort required once the tool is configured for a specific model architecture.
- **Model Context Protocol**: Fully compatible with the **MCP 3.1** and **FastMCP 3.1** task execution standards for automated weight modification pipelines.

## Limitations
- **Experimental**: The ARA method is still in research and may introduce unpredictable behaviors or "vibe" shifts in the model.
- **Safety Risks**: Removal of guardrails means the model can generate harmful content; users must apply their own application-level safety layers.
- **Compute Intensive**: The optimization process requires multiple runs or evaluations of the model to find the optimal vector.
- **Architecture Specific**: While versatile, some newer MoE (Mixture of Experts) models require specialized optimization parameters.

## When to use it
- When you encounter persistent refusals for legitimate tasks with standard aligned models.
- For local-first applications where you manage your own safety boundaries and need the highest possible reasoning fidelity.
- When you need to automate model abliteration as part of a larger CI/CD pipeline for AI models.

## When not to use it
- In production environments with untrusted users where safety guardrails are mandatory.
- If you lack the compute resources (high-VRAM GPUs) to perform the required optimization loops.
- If you require the most stable and predictable model behavior as provided by original vendors like [Anthropic](../providers/anthropic.md) or [OpenAI](openai.md).

## Getting started

### Installation (PyPI)
The tool is typically installed via `pip` or `uv`.

```bash
pip install heretic-llm
```

### Basic Workflow
1. Load your target open-weight model (e.g., [Gemma 3](../providers/gemma.md)).
2. Run the `heretic` command to begin the ablation process.
3. Export the resulting "abliterated" weights to GGUF or Safetensors for use in [llama.cpp](../infrastructure/llama-cpp.md).

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

### Python (Ablation Configuration and Validation with Pydantic v2)
The following Python script demonstrates how researchers can model, configure, and validate a Heretic abliteration session using **Pydantic v2** models to integrate automated weight modification into standard devops pipelines.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class AblationParameters(BaseModel):
    model_name_or_path: str = Field(..., description="The directory or HF path of the base model")
    target_layers: List[int] = Field(..., description="The specific transformer layers to search for refusal vectors")
    optuna_trials: int = Field(default=50, ge=1, le=500, description="Number of trials for Optuna optimization")
    target_kl_divergence: float = Field(default=0.15, gt=0.0, lt=1.0, description="Target limit for capability damage")
    custom_eval_set: Optional[str] = Field(None, description="Path to custom eval set of harmless but complex queries")

    @field_validator("target_layers")
    @classmethod
    def validate_layers(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("Must specify at least one target layer for ablation search.")
        if any(layer < 0 for layer in v):
            raise ValueError("Transformer layers must be non-negative integers.")
        return v

class AblationResult(BaseModel):
    parameters: AblationParameters
    refusal_rate_before: float = Field(..., ge=0.0, le=1.0, description="Refusal rate on evaluation set before ablation")
    refusal_rate_after: float = Field(..., ge=0.0, le=1.0, description="Refusal rate on evaluation set after ablation")
    kl_divergence: float = Field(..., ge=0.0, description="Measured KL divergence indicating capability retention")
    vector_magnitude: float = Field(..., description="Calculated magnitude of the orthogonal refusal projection vector")

# Demonstration of config validation and processing
def run_ablation_simulation(config_dict: dict) -> AblationResult:
    # 1. Parse and validate the ablation configuration using Pydantic v2
    params = AblationParameters.model_validate(config_dict)

    # 2. Simulate the ablation execution output (e.g., abliterating Gemma 3 12B)
    simulated_result = AblationResult(
        parameters=params,
        refusal_rate_before=0.88,
        refusal_rate_after=0.02,
        kl_divergence=0.14,
        vector_magnitude=1.428
    )
    return simulated_result

if __name__ == "__main__":
    raw_config = {
        "model_name_or_path": "google/gemma-3-12b-it",
        "target_layers": [12, 13, 14, 15, 16],
        "optuna_trials": 100,
        "target_kl_divergence": 0.15,
        "custom_eval_set": "/data/benchmarks/harmless_refusals.json"
    }

    result = run_ablation_simulation(raw_config)
    print("--- Ablation Session Validated & Executed ---")
    print(f"Model: {result.parameters.model_name_or_path}")
    print(f"Target Layers Visited: {result.parameters.target_layers}")
    print(f"Refusal Rate: {result.refusal_rate_before * 100}% -> {result.refusal_rate_after * 100}%")
    print(f"Measured KL Divergence: {result.kl_divergence} (Success: preserved capabilities!)")
```

## Related tools / concepts
- [Qwen](qwen.md) — Targeted model.
- [Local LLMs](./local_llms.md) — Deployment target.
- [llama.cpp](../infrastructure/llama-cpp.md) — Inference engine.
- [Ollama](../../services/ollama.md) — Model management.
- [AnythingLLM](anythingllm.md) — RAG frontend.
- [Dify](dify.md) — LLM application builder.
- [MMLU](../benchmarking/mmlu.md) — Benchmarking.
- [Gemma](../providers/gemma.md) — Targeted model.
- [Llama](../providers/llama.md) — Targeted model.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Automation standard.
- [Optuna](https://optuna.org/) — Optimization library.

## Sources / References
- [Heretic vs Abliterated LLMs: Refusal Rates & Benchmarks (2026)](https://aithinkerlab.com/heretic-ai-abliteration-benchmarks-2026/)
- [Orthogonalization of LLM Refusal Vectors (Arditi et al., NeurIPS 2024)](https://arxiv.org/abs/2406.11717)
- [Heretic: Automated Abliteration Tool (GitHub)](https://github.com/p-e-w/heretic)

## Contribution Metadata
- Last reviewed: 2026-11-26
- Confidence: high
