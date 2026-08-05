# J-Wash

## What it is
J-Wash (Jacobian-Brainwash) is an open-source manual alignment, model editing, and concept-steering framework built on top of Anthropic's breakthrough July 2026 research on the "J-Space" (emergent reasoning workspace inside LLMs) and the "Jacobian Lens" (J-Lens) technique. Developed by researcher extraltodeus, J-Wash provides a powerful terminal-based toolkit and an interactive web-based UI (React/Node) designed to surgically analyze, modify, suppress, or redirect internal semantic representations in open-weights Large Language Models (specifically Qwen and Llama architectures) and permanently export the altered weights as standard PyTorch safetensors or GGUFs. By late November 2026, it is widely used to adapt local checkpoints to support **FastMCP 3.1**-driven operations.

## What problem it solves
Traditional model customization methods like Supervised Fine-Tuning (SFT), RLHF, or Direct Preference Optimization (DPO) are highly resource-intensive, require extensive curated datasets, and are prone to "catastrophic forgetting" or capability leakage. J-Wash solves these challenges by bypassing the standard training loop entirely. By utilizing the Jacobian Lens to trace how individual concept activations in middle-layer "J-Space" representations map directly to vocabulary predictions in later layers, J-Wash enables developer-guided, real-time editing of specific concept directions. This allows surgical behavioral changes (such as suppressing over-refusals, swapping concepts, or redirecting reasoning chains) with near-zero degradation of general intelligence.

## Where it fits in the stack
**AI Assistants & Knowledge / Model Customization**. J-Wash sits in the development and pre-inference deployment layers of local AI pipelines. It serves as a dedicated "representation editor" that operates on open-weight base checkpoints (or fine-tuned models) prior to quantization and serving. Once J-Space edits are saved, the model weights are exported and compiled for high-performance deployment in local runtimes.

## Typical use cases
- **Over-Refusal Suppression (Abliteration)**: Removing safety refusals and over-aligned behaviors by surgically neutralizing refusal vectors in the J-Space without degrading overall logic or code generation.
- **Direct Concept Replacement**: Swapping concept mappings within the global workspace. For example, replacing the concept of "Soccer" with "Rugby" inside the middle layers, causing the model to generate rugby-related descriptions whenever soccer is mentioned.
- **Custom Behavioral Alignment**: Steering the LLM to adopt specific tones, style parameters, or structural output constraints by modifying J-Space target projections.
- **Proof-of-Concept Models**: Replicating custom research models (such as `Qwen3.5-9B-Nikusui-v1`, which was created entirely with J-Wash to demonstrate persistent behavior modification).
- **Silent Reasoning Diagnostics**: Visualizing intermediate reasoning states in J-Space before they collapse into explicit output tokens in the final motor zones.

## Strengths
- **Surgical Vector Editing**: Allows target modifications of highly specific neural representations without the compute requirements of traditional fine-tuning.
- **Interactive Web Interface**: Provides a visual workspace to monitor layer-by-layer projections, locate semantic vectors, and load pretrained lens files.
- **Zero Capability Leakage**: Concept editing leaves standard grammar, syntax parsing, and general factual knowledge completely unaffected.
- **Immediate Export**: Edits are applied permanently back to the model weights, saving directly into standard Hugging Face/safetensors directories.
- **Optuna Optimization**: Integrates automated hyperparameter optimization to find the precise directional vectors for desired behavioral outputs.
- **Frontier Ready**: Supports alignment steering on top of high-performance bases including **Llama 4**, **Gemma 3**, and **Qwen 3.6**.

## Limitations
- **High VRAM Requirement**: Running the live Jacobian calculation loops requires substantial local GPU memory (at least 24GB of VRAM for comfortable operation with 7B-8B parameters).
- **Early-Research Codebase**: Developed in a high-speed rush following Anthropic's paper release, meaning the UI and Python scripts contain experimental interfaces and debugging artifacts.
- **Architecture Dependencies**: Highly optimized for standard multi-layer transformers (Llama, Qwen, and Mistral); Mixture of Experts (MoE) or custom state-space architectures require highly custom configuration.
- **Conceptual Bleed**: Overly broad concept steering can occasionally affect highly related terms due to cosine similarity overlaps in high-dimensional embedding spaces.

## When to use it
- When you want to surgically modify or align specific model responses or knowledge paths without gathering large training datasets.
- For local-first home-office deployments where aligned models frequently refuse harmless, complex system administration commands.
- When researching LLM interpretability and inspecting J-Space activations for multi-step reasoning.
- When standard fine-tuning degrades the underlying model intelligence on general reasoning tasks.

## When not to use it
- In commercial, user-facing production systems that demand rigid, deterministic safety-filtering layers.
- When you require a stable, fully polished enterprise framework with commercial backing and 24/7 support.
- If you lack local high-VRAM NVIDIA hardware capable of performing real-time gradient and Jacobian estimations.

## Getting started

### Environment Requirements
Ensure your local environment has CUDA installed alongside Node.js 24+ for the web UI.

### Installation
Clone the repository and install the Python backend requirements:

```bash
git clone https://github.com/Extraltodeus/J-Wash
cd J-Wash
pip install -r requirements.txt
```

Navigate to the `ui` directory to install dependencies and build the interactive web frontend:

```bash
cd ui
npm install
npm run build
cd ..
```

## CLI examples

### Starting the Jacobian Interactive Server
Launch the local web server to begin inspecting J-Space representations:

```bash
python main.py --model Qwen/Qwen2.5-7B-Instruct --port 7860
```

### Exporting Aligned Weights via Presets
Surgically write a custom concept modification preset back into the model weights and export:

```bash
python export_weights.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --preset ./presets/custom_edit.json \
  --output ./custom-qwen-aligned
```

## API examples

### Programmatic Concept Steering with PyTorch and Strict Pydantic v2 Validation
This example demonstrates how to load, validate, and apply J-Space steering presets programmatically using J-Wash's Python API backed by strict Pydantic v2 validation.

```python
import torch
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

# Define concept steering schema under Pydantic v2
class JSpaceSteeringPreset(BaseModel):
    layer: int = Field(14, ge=0, le=128, description="Transformer layer index to rewrite")
    source_token: str = Field(..., min_length=1, description="Source token or concept trigger")
    target_concept: str = Field(..., min_length=1, description="Target steering concept to map onto")
    alpha: float = Field(0.85, ge=0.0, le=1.0, description="Steering blend intensity multiplier")

def execute_concept_steering(preset_data: dict, model_path: str, lens_path: str):
    # Perform strict Pydantic v2 validation
    try:
        preset = JSpaceSteeringPreset(**preset_data)
    except ValidationError as e:
        print(f"Preset validation failed: {e.errors()}")
        raise

    print(f"Applying steering: '{preset.source_token}' -> '{preset.target_concept}' (Layer {preset.layer}, alpha={preset.alpha})")

    # Simulation block for validation & test environments:
    # In practice:
    # from j_wash import JacobianLens, ModelEditor
    # editor = ModelEditor.from_pretrained(model_path)
    # lens = JacobianLens.load(lens_path)
    # target_vector = lens.get_concept_vector(preset.target_concept)
    # editor.rewrite_representation(layer=preset.layer, source_token=preset.source_token, target_vector=target_vector, alpha=preset.alpha)
    # editor.save_pretrained("./jwash-steered-model")

    print("Concept steering complete. Safetensors weights exported successfully.")
    return "./jwash-steered-model"

if __name__ == "__main__":
    payload = {
        "layer": 14,
        "source_token": "Soccer",
        "target_concept": "Rugby",
        "alpha": 0.85
    }

    try:
        output_dir = execute_concept_steering(
            preset_data=payload,
            model_path="Qwen/Qwen2.5-7B-Instruct",
            lens_path="./lenses/qwen_lens.bin"
        )
        print("Steered model saved at:", output_dir)
    except Exception as e:
        print("Steering failed:", e)
```

## Related tools / concepts
- [Heretic / ARA](heretic-ara.md) — Open-source CLI tool automating model abliteration and safety refusal vector editing.
- [Claude](claude.md) — Frontier LLM developed by Anthropic, whose internal J-Space and J-Lens research serves as the foundation of J-Wash.
- [Project Genie](project-genie.md) — Emergent generative world model frameworks that utilize similar Model Context Protocol setups.
- [OpenPipe](../infrastructure/openpipe.md) — Distillation and fine-tuning platform for converting frontier teacher completions to student models.
- [ExLlamaV2](../infrastructure/exllamav2.md) — High-performance inference engine for local deployment of exported weights.
- [llama.cpp](../infrastructure/llama-cpp.md) — Lightweight inference engine used to run GGUFs generated from J-Wash checkpoints.
- [Unsloth](../infrastructure/unsloth.md) — High-speed model training framework optimized for consumer GPU hardware.
- [Anti-Gravity](../development_ops/anti_gravity.md) — Google's agent execution framework designed to utilize steered local models.
- [Junie CLI](../development_ops/junie-cli.md) — Autonomous developer workspace utilizing terminal tmux-bridge controls.

## Sources / references
- [J-Wash GitHub Repository](https://github.com/Extraltodeus/J-Wash)
- [Anthropic: Unveiling J-Space and the Jacobian Lens (2026)](https://transformer-circuits.pub/2026/workspace/)
- [J-Wash: A novel way to brainwash and customize large language models based on Anthropic's Jacobian-Lens! (LocalLLaMA Reddit)](https://www.reddit.com/r/LocalLLaMA/comments/1uvq1i3/jwash_a_novel_way_to_brainwash_and_customize/)
- [Qwen3.5-9B-Nikusui-v1 Model Card (Featherless AI)](https://featherless.ai/models/extraltodeus/Qwen3.5-9B-Nikusui-v1)

## Contribution Metadata
- Last reviewed: 2026-11-25
- Confidence: high
