# Lophius

## What it is
Lophius is an open-source, modular research workbench and evaluation environment designed for language model internal state inspection, activation steering, and mechanistic interpretability experiments. Released in August 2026, Lophius provides researchers and AI safety engineers with fine-grained controls to record, analyze, and perturb latent model activations during inference across frontier open-weights LLMs (such as [Llama 4](../../knowledge_base/model_classes.md), [Gemma 3](../ai_knowledge/local_llms.md), and [Qwen 3.8](../ai_knowledge/qwen.md)).

## What problem it solves
Understanding internal representation dynamics in transformer architectures often requires complex custom PyTorch hooks, manual tensor manipulations, and fragmented tooling. Lophius solves this friction by unifying latent activation logging, Sparse Autoencoder (SAE) feature extraction, and real-time activation steering vectors into a single high-performance research interface. It empowers researchers to rapidly audit model trust boundaries, detect hidden chain-of-thought deviations, and verify safety alignment.

## Where it fits in the stack
**Development & Ops / Interpretability & Model Analysis**. Lophius acts as an advanced model debugging and research workbench, connecting directly to local inference engines like [vLLM](../infrastructure/vllm.md) or [llama.cpp](../infrastructure/llama-cpp.md) via hook-enabled execution passes.

## Typical use cases
- **Latent Feature Extraction**: Training and evaluating Sparse Autoencoders (SAEs) on internal transformer activations to isolate interpretable concepts.
- **Activation Steering & Safety Verification**: Injecting steering vectors during token generation to test and enforce system safety parameters without retraining.
- **Hallucination & Deception Auditing**: Tracking attention entropy and latent linear probe confidence to flag low-certainty or deceptive output trajectories.
- **Model Editing & Fine-Tuning Debugging**: Monitoring representation shifts across pre- and post-fine-tuned checkpoints.

## Strengths
- **Modular Architecture**: Pluggable components for hook injection, tensor recording, probe training, and visualization.
- **High Efficiency**: Zero-copy CUDA tensor sharing for minimal inference slowdown during full-layer activation logging.
- **FastMCP 3.1 & Pydantic v2 Native**: Seamlessly exposes interpretability inspection tools over [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).
- **Extensible Web & CLI Interface**: Interactive dashboard for dynamic activation vector heatmaps and steering control sliders.

## Limitations
- **High GPU Memory Footprint**: Logging dense activation tensors across deep transformer models requires substantial VRAM headroom.
- **Open-Weights Constraint**: Full mechanistic interpretability requires access to internal model weights and intermediate activations, limiting utility on closed API endpoints.

## When to use it
- When performing mechanistic interpretability research or Sparse Autoencoder (SAE) feature analyses.
- When prototyping latent activation steering controls to prevent hallucination or policy violations in local LLMs.
- For deep diagnostic auditing of fine-tuned model checkpoints before production deployment.

## When not to use it
- For standard production inference serving where intermediate tensor logging overhead is unnecessary.
- When interacting exclusively with closed API providers (e.g., [Anthropic](../providers/anthropic.md) or [OpenAI](../ai_knowledge/openai.md)) that do not expose intermediate layer weights.

## Getting started

### Installation
```bash
pip install lophius torch
```

### Starting the Lophius Inspection Dashboard
```bash
lophius-workbench --model meta-llama/Llama-4-8B-Instruct --port 8080
```

## CLI examples

### Recording Layer Activations to Disk
```bash
# Record activations for layer 16 to 24 during a prompt pass
lophius-cli record \
  --model Qwen/Qwen3.8-7B \
  --prompt "Analyze system safety boundaries" \
  --layers 16..24 \
  --output ./activations/qwen_run.pt
```

## API examples

### Python Activation Steering & Pydantic v2 Schema Validation
The following Python example demonstrates how to configure a Lophius steering experiment and validate latent feature inspection outputs using **Pydantic v2**:

```python
import os
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class LatentFeatureProbe(BaseModel):
    feature_id: int = Field(..., ge=0, description="Sparse Autoencoder feature index")
    feature_label: str = Field(..., description="Interpreted concept label")
    activation_score: float = Field(..., ge=0.0, description="Magnitude of activation")
    layer_index: int = Field(..., ge=0, description="Transformer layer index where probe was attached")

class InterpretabilityReport(BaseModel):
    model_name: str = Field(..., description="Target model evaluated")
    prompt_evaluated: str = Field(..., description="Prompt input evaluated")
    detected_features: List[LatentFeatureProbe] = Field(..., description="Top active latent concepts detected")
    steering_vector_applied: bool = Field(default=False, description="Whether steering was active during generation")

def run_lophius_interpretability_audit(model_name: str, prompt: str) -> InterpretabilityReport:
    """Simulates a Lophius interpretability audit pass with Pydantic v2 validation."""
    raw_response = {
        "model_name": model_name,
        "prompt_evaluated": prompt,
        "detected_features": [
            {
                "feature_id": 1042,
                "feature_label": "Code Refactoring Concept",
                "activation_score": 0.89,
                "layer_index": 20
            },
            {
                "feature_id": 512,
                "feature_label": "System Security Boundary",
                "activation_score": 0.74,
                "layer_index": 22
            }
        ],
        "steering_vector_applied": True
    }

    try:
        return InterpretabilityReport.model_validate(raw_response)
    except ValidationError as ve:
        print(f"Validation error in Lophius report: {ve}")
        return InterpretabilityReport(
            model_name=model_name,
            prompt_evaluated=prompt,
            detected_features=[],
            steering_vector_applied=False
        )

if __name__ == "__main__":
    report = run_lophius_interpretability_audit("Llama-4-8B-Instruct", "Write an optimized Python script")
    print(f"Lophius Interpretability Report Verified:")
    print(f"Model: {report.model_name}")
    print(f"Steering Applied: {report.steering_vector_applied}")
    print(f"Top Features Detected: {len(report.detected_features)}")
    for f in report.detected_features:
        print(f" - Layer {f.layer_index} [{f.feature_label}]: Score {f.activation_score}")
```

## Related tools / concepts
- [vLLM](../infrastructure/vllm.md) — High-performance inference engine for local weight execution.
- [Helicone](../process_understanding/helicone.md) — LLM observability and logging.
- [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md) — Safety architecture pattern.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agent tools.

## Sources / references
- [Lophius Workbench Announcement on Reddit r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1vjt4vi/lophius_a_workbench_for_language_model_research/)
- [Lophius Interpretability Research Core](https://github.com/lophius-ai/lophius)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
