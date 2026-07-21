# J-Wash

## What it is
J-Wash (Jacobian-Brainwash) is an open-source manual alignment, model editing, and concept-steering framework designed for large language models. Built on top of Anthropic's Jacobian Lens (`jlens`) research and J-Space (the emergent reasoning workspace within LLMs), J-Wash allows developers to visually and programmatically inspect, steer, or suppress internal model representations in real time. Crucially, J-Wash includes a specialized export pipeline that "bakes" these token-level steering edits directly into the model's weight matrices, producing standard, standalone checkpoints that run anywhere with zero-overhead inference.

## What problem it solves
Traditional LLM alignment relies on reinforcement learning (RLHF/RLAIF) or supervised fine-tuning (SFT). These methods are computationally expensive, require substantial training datasets, and often lead to unintended model degradation or "alignment tax." J-Wash solves these challenges by providing a surgical alternative: direct, localized weight editing. Instead of training, developers can target specific token paths, replace concepts (such as washing or modifying identity, bias, or safety behaviors), and export the resulting model weights without requiring fine-tuning data, massive GPU clusters, or custom inference runtimes.

## Where it fits in the stack
**AI Assistants & Knowledge / Alignment & Editing Framework**. It sits in the model post-processing and optimization layer of the stack, bridging the gap between local model exploration (such as [Ollama](../../services/ollama.md)) and direct weight optimization (such as [OpenPipe](../infrastructure/openpipe.md)). It integrates directly with Hugging Face decoder models and exports safetensors that can be deployed via high-performance inference engines like [ExLlamaV2](../infrastructure/exllamav2.md) or [llama.cpp](../infrastructure/llama-cpp.md).

## Typical use cases
- **Concept Replacement & Refinement**: Permanently changing specific model facts or behaviors (e.g., changing "I am an assistant developed by OpenAI" to "I am a custom assistant for our company") by directly editing the unembedding residual streams.
- **Surgical De-biasing & Concept Suppression**: Locating and neutralizing toxic concepts, harmful patterns, or security exploits (such as those checked by [Sourcegraph Cody](../development_ops/sourcegraph_cody.md)) without altering orthogonal reasoning capabilities.
- **Custom Alignment & Brand Identity**: Aligning open-weight models (e.g., Llama 4, Gemma 3, or Qwen 3.6) to conform to rigid brand guidelines or behavioral styles.
- **Model Editing Research**: Visually investigating the contribution of specific layers to the residual stream using Jacobian Lens visualization.

## Strengths
- **Zero Fine-Tuning Overhead**: Modifies weights directly; no need for datasets, training runs, or loss functions.
- **Exportable Results**: Edits are baked into standard PyTorch weight matrices, exportable as safetensors, custom layers, or lightweight LoRA adapters.
- **Interactive Visual Studio**: Features a live FastAPI-React dashboard that renders real-time token clouds, heatmaps, and per-layer rank curves as you chat with the model.
- **Highly Targeted Editing**: Allows editing specific token directions in J-Space while preserving overall language model performance.

## Limitations
- **Model Architecture Support**: Primarily limited to auto-regressive decoder-only transformer models (e.g., Llama, Qwen, and Gemma models).
- **GPU Memory Constraints**: Requires sufficient VRAM (NVIDIA CUDA recommended) to load the base model, lens, and editing tensors simultaneously during interactive sessions.
- **Concept Complexity**: Simple token-to-token concepts steer perfectly, but highly abstract, multi-hop reasoning behaviors can be challenging to capture via single-token directions.

## When to use it
- When you need to edit specific concepts, facts, or identities inside a model and require a direct, zero-overhead exportable checkpoint.
- For non-destructive alignment experiments where you want to inspect exact layer-level token reads during inference.
- When fine-tuning data is unavailable, but target concept steering directions are known.

## When not to use it
- For broad, open-ended style transfer or domain adaptation that requires massive knowledge absorption (where [OpenPipe](../infrastructure/openpipe.md) or standard SFT is more appropriate).
- When targeting non-transformer architectures or models lacking public unembedding weights.
- In low-resource environments lacking adequate GPU support for local model loading.

## Getting started

### Installation
J-Wash requires an NVIDIA GPU with CUDA support, Python 3.11+, and Node.js 18+.

```bash
# Clone the repository
git clone https://github.com/extraltodeus/j-wash.git
cd j-wash

# Install PyTorch with CUDA 12.4 support
pip install torch --index-url https://download.pytorch.org/whl/cu124

# Clone and install Anthropic's Jacobian Lens dependency
git clone https://github.com/anthropics/jacobian-lens vendor/jacobian-lens
pip install -e vendor/jacobian-lens

# Install backend dependencies
pip install -r requirements.txt

# Build the React Frontend UI
cd ui
npm install
npm run build
cd ..
```

### Launching the Studio
Start the FastAPI server with React frontend:
```bash
python -X utf8 run.py
```
This will start the local studio web interface at `http://localhost:8381`.

## CLI examples

### Running Concept Editing via CLI (No UI)
You can apply pre-trained lenses and apply token steering directly from the command line:

```bash
python run.py --cli \
  --model "Qwen/Qwen2.5-7B-Instruct" \
  --lens "neuronpedia/qwen2.5-7b-lens" \
  --edit "edit_rules.json" \
  --export-path "./edited-qwen-7b"
```

### Fitting a Custom Lens Locally
Fit a Jacobian Lens to a custom local model checkpoint before editing:
```bash
python run.py --fit-lens \
  --model "./my-custom-llama" \
  --dataset "./wiki-sample.jsonl" \
  --output "./lens-my-custom-llama.pt"
```

## API examples

### Programmatic Concept Suppression
You can programmatically steer model activations in a custom Python inference loop:

```python
import torch
from jlens import JacobianLens
from jwash import JWashSteerer

# Load base model and tokenizer
model_name = "meta-llama/Llama-3-8B"
lens = JacobianLens.from_pretrained("neuronpedia/llama3-8b-lens")

# Initialize J-Wash programmatic steerer
steerer = JWashSteerer(model_name, lens)

# Define concepts to suppress (e.g., suppress mention of competitors)
steerer.add_suppression_rule(
    target_token="CompetitorName",
    strength=2.5,
    layers=range(12, 24)
)

# Generate text with active steering in residual stream
prompt = "Our premier partner is"
output = steerer.generate(prompt, max_new_tokens=32)
print(output)
```

### Baking Edits into Standalone Safetensors
Apply token-level rule changes and save them directly as a standard PyTorch model:

```python
from jwash.export import bake_and_export_weights

# Load edit metadata file
edit_config = {
    "identity": {
        "source": "large language model",
        "target": "autonomous corporate droid",
        "weight": 1.8
    }
}

# Bake edits directly into weight matrices and export as safetensors
bake_and_export_weights(
    base_model_path="Qwen/Qwen2.5-7B-Base",
    lens_path="./qwen-lens.pt",
    edits=edit_config,
    output_dir="./baked-corporate-qwen"
)
```

## Related tools / concepts
- [ansigpt](ansigpt.md) — Minimalist C89 transformer engine, useful for running tiny edge-centric steered weights.
- [Project Genie](project-genie.md) — Unsupervised generative world model optimized for virtual sandboxes.
- [llama.cpp](../infrastructure/llama-cpp.md) — High-performance local GGUF inference library compatible with J-Wash baked checkpoints.
- [ExLlamaV2](../infrastructure/exllamav2.md) — Fast local transformer engine with support for custom quantizations of baked models.
- [Mycelium](../frameworks/mycelium.md) — Clojure-based cellular agent framework requiring guaranteed aligned behavior.
- [Smolagents](../frameworks/smolagents.md) — Lightweight agent engine utilizing steered and aligned code models.
- [Pydantic AI](../frameworks/pydantic-ai.md) — Strict schema-validated agent framework relying on predictable model responses.
- [Sourcegraph Cody](../development_ops/sourcegraph_cody.md) — Multi-repository reasoning assistant that benefits from custom aligned model variants.
- [Anti-Gravity](../development_ops/anti_gravity.md) — Google's premier agent execution framework leveraging steerable models.
- [LM Evaluation Harness](../benchmarking/lm-evaluation-harness.md) — Framework for evaluating the exact downstream impact of concept editing.
- [OpenPipe](../infrastructure/openpipe.md) — Platform for fine-tuning and model distillation from frontier outputs.

## Sources / references
- [Jacobian-Brainwash (J-Wash) GitHub Repository](https://github.com/Extraltodeus/J-Wash)
- [Anthropic's Jacobian Lens Library](https://github.com/anthropics/jacobian-lens)
- [Neuronpedia Pre-fitted Lenses and Feature Maps](https://www.neuronpedia.org)
- [Anthropic Research: Mapping the Mind of a Large Language Model](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)
- [Featherless AI - Qwen3.5-9B-Nikusui-v1 Model Card](https://featherless.ai/models/extraltodeus/Qwen3.5-9B-Nikusui-v1)
- [LocalLLaMA Announcement: J-Wash Release Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1uvq1i3/jwash_a_novel_way_to_brainwash_and_customize/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
