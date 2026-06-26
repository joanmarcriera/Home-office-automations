# ComfyUI

## What it is
ComfyUI is an open-source, node-based graphical interface and inference pipeline for local image generation using diffusion models (Flux, SD3, SDXL, SD 1.5). Unlike linear web UIs, ComfyUI exposes the full diffusion graph as a composable canvas of nodes — each step (CLIP encode, KSampler, VAE decode, upscale) is wired visually and can be modified or extended. As of June 2026, it supports **MCP 3.0** for agentic workflow orchestration.

## What problem it solves
Local image generation tools typically hide the pipeline in a fixed UI. ComfyUI makes every parameter of the diffusion process explicit, composable, and automatable. Workflows are saved as JSON graphs, making them version-controllable, reproducible, and callable from external tools like n8n or autonomous Home Admin agents.

## Where it fits in the stack
**Category**: AI & Knowledge / Local Generative Media. Complements the LLM stack by adding local image synthesis alongside Ollama. It operates at the **Inference & Content Generation layer**, providing high-quality visuals without cloud API dependencies.

## Typical use cases
- **Automated Documentation**: Generating reference images for technical manuals or playbooks.
- **Batch Image Pipelines**: Triggering complex workflows (e.g., upscaling + inpainting) via n8n.
- **Agentic Content Creation**: Home agents using [Runway ML](runwayml.md) or local Flux models to visualize task outcomes.
- **Legacy Photo Restoration**: Restoring family archives using specialized ControlNet nodes and VAE refinement.

## Strengths
- **Reproducible workflows**: Every run is defined by a JSON graph — version-controllable and shareable.
- **API-first**: The `/prompt` endpoint accepts JSON workflows, enabling full automation from any programming language.
- **Massive community library**: Thousands of pre-built workflows available; ComfyUI-Manager handles automated node installation.
- **Memory-efficient**: Launch flags like `--lowvram` allow running SOTA models like Flux on 8GB GPUs.
- **MCP 3.0 Integration**: Agents can discover and execute ComfyUI workflows as native tools.

## Limitations
- **Learning Curve**: Steep entry barrier compared to linear UIs like Automatic1111; requires understanding of diffusion pipelines.
- **Ecosystem Fragmentation**: Custom nodes are developed independently, leading to occasional version conflicts.
- **Storage Requirements**: Model checkpoints and Loras can consume hundreds of gigabytes (best stored on ZFS/NAS).

## When to use it
- When you need fully local, private image generation with zero per-image cost.
- When you want repeatable, automatable image pipelines integrated into a larger home automation stack.
- For professional-grade ControlNet and IP-Adapter control over the generation process.

## When not to use it
- When you need photorealistic video generation (use [Runway ML](runwayml.md) or [Luma Dream Machine](luma-dream-machine.md) for temporal consistency).
- On machines without a dedicated GPU (CPU-only mode is prohibitively slow for 2026 models).
- If you require a "one-click" experience without wanting to manage nodes.

## Getting started
1. **Clone & Install**:
   ```bash
   git clone https://github.com/comfyanonymous/ComfyUI
   cd ComfyUI
   pip install -r requirements.txt
   ```
2. **Download Models**: Place your checkpoints (Flux, SDXL) in the `models/checkpoints/` directory.
3. **Launch**: Start the server using the appropriate hardware flags (see CLI examples).
4. **Manager**: Install `ComfyUI-Manager` to handle node dependencies automatically.

## CLI examples
Launch flags are critical for optimizing performance on different hardware configurations.

```bash
# Standard launch for NVIDIA GPUs (8GB+ VRAM)
python main.py --gpu-only

# Constrained VRAM launch (e.g., RTX 4060 8GB for Flux)
python main.py --lowvram

# Apple Silicon (M4/M5) launch using Metal
python main.py --use-pytorch-mps

# Headless mode for API-only use
python main.py --headless --listen 0.0.0.0
```

## API examples
ComfyUI exposes a REST endpoint at `/prompt` for remote execution.

### Queue a workflow via Python
```python
import json
import urllib.request

def queue_workflow(workflow_json: dict, server="127.0.0.1:8188"):
    payload = json.dumps({"prompt": workflow_json, "client_id": "home-admin-agent"}).encode()
    req = urllib.request.Request(f"http://{server}/prompt", data=payload)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())["prompt_id"]

# Load a saved workflow, modify the text prompt node, and queue
with open("flux_workflow.json") as f:
    wf = json.load(f)
wf["6"]["inputs"]["text"] = "a futuristic homelab with glowing blue lights"
print(f"Queued: {queue_workflow(wf)}")
```

## Related tools / concepts
- [Ollama](../../services/ollama.md): Often used to generate the text prompts for ComfyUI.
- [n8n](../../services/n8n.md): The primary orchestrator for ComfyUI API calls.
- [Immich](../../services/immich.md): Used to store and organize the generated image outputs.
- [Flux Model Card](https://huggingface.co/black-forest-labs/FLUX.1-schnell): The current state-of-the-art local model for ComfyUI.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md): The bridge for agents to call ComfyUI nodes.
- [MLX](../infrastructure/mlx.md): High-performance Apple Silicon inference alternative.
- [Runway ML](runwayml.md): Cloud-based video generation alternative.
- [Home Lab Hardware Guide](../../knowledge_base/home-lab-hardware-guide.md): Sizing GPUs for local diffusion.

## Sources / References
- [ComfyUI Official GitHub](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI Wiki & Documentation](https://comfyui-wiki.com)
- [OpenArt ComfyUI Workflows](https://openart.ai/workflows/home)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
