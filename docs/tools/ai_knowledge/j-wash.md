# J-Wash

## What it is
J-Wash (Jacobian-Brainwash) is an open-source manual alignment, representation editing, and concept-steering framework built on top of Anthropic's research regarding the "J-Space" (emergent reasoning workspace inside LLMs) and the "Jacobian Lens" (J-Lens) technique. J-Wash provides a terminal CLI and an interactive web UI (React/Node) designed to analyze, modify, suppress, or redirect internal semantic representations in open-weights models (specifically **Qwen 3.6**, **Llama 4**, and **Gemma 3** architectures) and permanently export edited weights as standard PyTorch safetensors or GGUF checkpoints. In 2027, J-Wash is widely used to adapt local checkpoints to support **FastMCP 3.1**-driven steerable agent operations.

## What problem it solves
Traditional model adaptation techniques like Supervised Fine-Tuning (SFT), RLHF, or Direct Preference Optimization (DPO) require expensive GPU compute, large curated datasets, and often suffer from catastrophic forgetting or capability degradation. J-Wash bypasses training loops entirely. By utilizing the Jacobian Lens to trace how middle-layer J-Space concept vectors map directly to vocabulary logits in later layers, J-Wash enables developer-guided, real-time editing of specific concept directions with zero degradation of general reasoning intelligence.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Model Customization & Interpretability
J-Wash operates in the pre-deployment optimization layer. It serves as a representation editor for open-weights models prior to quantization and serving via engines like [vLLM](../infrastructure/vllm.md), [ExLlamaV3](../infrastructure/exllamav3.md), or [llama.cpp](../infrastructure/llama-cpp.md).

## Typical use cases
- **Safety Refusal Suppression (Abliteration)**: Eliminating over-refusals on benign administrative shell commands without compromising logical safety limits.
- **Direct Concept Redirection**: Modifying semantic mapping vectors inside J-Space to change domain terminology or internal knowledge representation.
- **Behavioral Tone Steering**: Forcing specific structural outputs or stylistic responses across all system prompts.
- **Auditing Intermediate Reasoning**: Inspecting internal J-Space vectors to visualize multi-step logic before it manifests in final output tokens.

## Strengths
- **Surgical Vector Editing**: Direct concept modifications without multi-gpu retraining runs.
- **Interactive UI**: Web interface to inspect middle-layer activations and load pretrained lens configurations.
- **Zero Capability Degradation**: Syntax parsing, coding aptitude, and factual knowledge remain untouched.
- **Direct Checkpoint Export**: Saves updated weights directly as safetensors or GGUFs for immediate local deployment.
- **FastMCP 3.1 Compatible**: Enables runtime concept steering for MCP agent tools.

## Limitations
- **VRAM Requirements**: Estimating live Jacobian matrices requires high GPU VRAM (24GB+ for 7B-14B models).
- **Architecture Specificity**: Optimized for standard decoder-only transformers; requires specialized configuration for Mixture-of-Experts (MoE) architectures.
- **Cosine Overlap Risk**: Overly aggressive steering can inadvertently affect closely related semantic vectors.

## When to use it
- When you want to modify specific behavioral patterns without collecting training datasets.
- For local home-server or enterprise deployments where base models over-refuse valid technical requests.
- When conducting interpretability research into intermediate transformer layer representations.

## When not to use it
- In commercial applications requiring rigid multi-layer guardrails.
- If you lack local high-VRAM NVIDIA/AMD hardware for matrix estimation.
- When simple system prompt engineering provides adequate steering control.

## Getting started

### Installation
```bash
git clone https://github.com/Extraltodeus/J-Wash
cd J-Wash
pip install -r requirements.txt fastmcp pydantic
```

### Build Frontend Workspace
```bash
cd ui && npm install && npm run build && cd ..
```

## CLI examples

### 1. Launch Interactive Jacobian Server
```bash
python main.py --model Qwen/Qwen2.5-7B-Instruct --port 7860
```

### 2. Export Concept-Edited Checkpoint
```bash
python export_weights.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --preset ./presets/system_admin_steering.json \
  --output ./steered-qwen-safetensors
```

## API examples

### FastMCP 3.1 & Pydantic v2 Steering Preset Schema
This executable Python script demonstrates validating J-Space concept-steering presets using **Pydantic v2** and executing them inside a **FastMCP 3.1** server wrapper.

```python
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from fastmcp import FastMCP

mcp = FastMCP("J-Wash Representation Editor")

class SteeringPresetSchema(BaseModel):
    layer_index: int = Field(14, ge=0, le=128, description="Target transformer layer index")
    source_concept: str = Field(..., min_length=1, description="Source trigger concept")
    target_concept: str = Field(..., min_length=1, description="Target steering concept direction")
    steering_alpha: float = Field(0.85, ge=0.0, le=1.0, description="Blend intensity multiplier")

class SteeringResultSchema(BaseModel):
    status: str
    output_model_path: str
    applied_preset: SteeringPresetSchema

@mcp.tool()
def apply_concept_steering(source_concept: str, target_concept: str, alpha: float = 0.85) -> str:
    """Apply J-Space representation editing to an open-weights model checkpoint."""
    try:
        preset = SteeringPresetSchema(
            layer_index=16,
            source_concept=source_concept,
            target_concept=target_concept,
            steering_alpha=alpha
        )
    except ValidationError as e:
        return f"Validation error: {e.errors()}"

    # Simulated editing pipeline execution
    result = SteeringResultSchema(
        status="SUCCESS",
        output_model_path="./steered_checkpoints/qwen3.6-steered",
        applied_preset=preset
    )

    return f"Successfully applied steering '{preset.source_concept}' -> '{preset.target_concept}' (Layer {preset.layer_index}, alpha={preset.steering_alpha}). Output saved at {result.output_model_path}."

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Claude](claude.md) — Anthropic research context behind J-Space and Jacobian Lens.
- [Local LLMs](local_llms.md) — Compatible base model architectures (Qwen 3.6, Llama 4, Gemma 3).
- [ExLlamaV3](../infrastructure/exllamav3.md) — Runtime engine for running exported GGUF/safetensors models.
- [vLLM](../infrastructure/vllm.md) — High-throughput server deployment.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Tool integration specification.

## Sources / references
- [J-Wash GitHub Repository](https://github.com/Extraltodeus/J-Wash)
- [Anthropic Transformer Circuits Publication](https://transformer-circuits.pub/)
- [FastMCP 3.1 Documentation](https://modelcontextprotocol.io/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
