# ComfyUI

## What it is
ComfyUI is an open-source, node-based graphical interface and inference pipeline for local image generation using diffusion models (Stable Diffusion 1.5, SDXL, Flux, SD3). Unlike linear web UIs, ComfyUI exposes the full diffusion graph as a composable canvas of nodes — each step (CLIP encode, KSampler, VAE decode, upscale) is wired visually and can be modified or extended.

## What problem it solves
Local image generation tools typically hide the pipeline in a fixed UI. ComfyUI makes every parameter of the diffusion process explicit, composable, and automatable. Workflows are saved as JSON graphs, making them version-controllable, reproducible, and callable from external tools like n8n or Python scripts.

## Where it fits in the stack
**Category**: AI & Knowledge / Local Generative Media. Complements the LLM stack by adding local image synthesis alongside Ollama. Runs entirely on-premise — no cloud API costs, no data leaving the home network.

## Typical use cases
- Generating reference images for design work or documentation without cloud costs
- Batch image pipelines triggered from n8n workflows via the ComfyUI API
- Image-to-image refinement (img2img, inpainting, ControlNet-guided generation)
- Upscaling existing images with Real-ESRGAN or ESRGAN nodes
- Generating thumbnails, illustrations, or mockups as part of a home admin agent pipeline

## Strengths
- **Reproducible workflows**: Every run is defined by a JSON graph — version-controllable and shareable
- **API-first**: The `/prompt` endpoint accepts JSON workflows, enabling full automation from n8n or Python
- **Massive community library**: Thousands of workflows on OpenArt and Civitai; ComfyUI-Manager handles custom node installation
- **Memory-efficient**: `--lowvram` and `--medvram` flags allow running on constrained GPUs (8 GB)
- **Multi-backend**: CUDA (NVIDIA), Metal (Apple Silicon), ROCm (AMD), CPU-only

## Limitations
- Steep learning curve compared to Automatic1111 or Invoke AI — the node canvas is powerful but unfamiliar at first
- No built-in image gallery or management (pair with [Immich](../../services/immich.md) for storage)
- Custom node ecosystem is fragmented; ComfyUI-Manager is required to tame it
- Checkpoint model files are large (2-20 GB each) — plan storage accordingly on ZFS

## Hardware requirements

ComfyUI supports CUDA (NVIDIA), Metal (Apple Silicon), and CPU-only backends. Launch flags control VRAM usage.

| Model | Min VRAM | RTX 4060 8 GB | M5 48 GB | Notes |
|---|---|---|---|---|
| SD 1.5 | 4 GB | ✅ Comfortable | ✅ Comfortable | Fast; 512px native; large community |
| SDXL base (fp16) | 6-8 GB | ✅ Fits | ✅ Comfortable | 1024px native; best quality/speed |
| SDXL + refiner | 10-12 GB | ⚠️ Offload refiner to CPU | ✅ Comfortable | Two-pass pipeline; use `--lowvram` |
| Flux-schnell (fp8/nf4) | 8 GB | ⚠️ Tight, use `--lowvram` | ✅ Comfortable | 4-step SOTA; quantize to fp8 |
| Flux-dev (fp16) | 16-24 GB | ❌ Not viable | ✅ Comfortable | Full quality; ~20 GB on M5 |
| SD3.5 Medium | 8 GB | ⚠️ Tight | ✅ Comfortable | MMDiT architecture |

**RTX 4060 tips**: Use `--lowvram` flag at launch. For Flux-schnell, download the fp8 or nf4 quantized checkpoint (not the full fp16). SDXL in fp16 is the practical sweet spot.

**M5 48 GB tips**: Use `--use-pytorch-mps` flag. All 48 GB unified memory is available to Metal — Flux-dev (fp16, ~20 GB) runs comfortably.

## When to use it
- When you need fully local, private image generation at zero per-image cost
- When you want repeatable, automatable image pipelines (batch generation, n8n integration)
- When SDXL or Flux quality is sufficient for your use case

## When not to use it
- When you need photorealistic video generation (use [Runway ML](runwayml.md) or [Luma Dream Machine](luma-dream-machine.md))
- On a machine with less than 4 GB VRAM (CPU-only mode works but is very slow — 5-30 min per image)
- When you need a fully managed image generation API (use Replicate or Stability AI instead)

## Getting started

### Installation

```bash
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt
```

### Launch

```bash
# RTX 4060 (CUDA) — standard
python main.py --gpu-only

# RTX 4060 — constrained VRAM (Flux-schnell, SDXL + refiner)
python main.py --lowvram

# M5 MacBook — Apple Silicon Metal
python main.py --use-pytorch-mps
```

Open `http://localhost:8188` in your browser. The node canvas loads with a default workflow.

### First image (SDXL)

1. Download an SDXL checkpoint (e.g. `sd_xl_base_1.0.safetensors`) and place it in `models/checkpoints/`
2. In ComfyUI, click **Load** and select the default SDXL workflow JSON
3. Set your prompt in the **CLIP Text Encode** (positive) node
4. Click **Queue Prompt** — your image appears in the output node when done

### Install custom nodes via ComfyUI-Manager

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager
# Restart ComfyUI, then use Manager tab to install nodes (ControlNet, IPAdapter, etc.)
```

## API automation

ComfyUI exposes a REST endpoint at `/prompt`. This enables n8n-driven batch generation or Python pipelines.

### Python example

```python
import json, urllib.request, random

def queue_prompt(workflow_json: dict, server="127.0.0.1:8188") -> str:
    payload = json.dumps({"prompt": workflow_json, "client_id": "home-agent"}).encode()
    req = urllib.request.Request(f"http://{server}/prompt", data=payload)
    response = urllib.request.urlopen(req)
    return json.loads(response.read())["prompt_id"]

# Load a saved workflow JSON, swap the positive prompt, queue it
with open("sdxl_workflow.json") as f:
    wf = json.load(f)

wf["6"]["inputs"]["text"] = "a photorealistic photo of a home office, natural light"
prompt_id = queue_prompt(wf)
print(f"Queued: {prompt_id}")
```

### n8n integration

Use an **HTTP Request** node in n8n pointing to `http://192.168.0.5:8188/prompt` with the workflow JSON as the body. Chain it after an LLM node that generates the prompt text.

## Related tools / concepts

- [Ollama](../../services/ollama.md) — LLM serving for prompt generation; pair with ComfyUI for text-to-image pipelines
- [n8n](../../services/n8n.md) — Automation; trigger ComfyUI batch jobs via HTTP Request node
- [Immich](../../services/immich.md) — Store and organise generated images
- [MLX](../infrastructure/mlx.md) — Alternative Apple Silicon inference; also supports Stable Diffusion via `mlx-community`
- [Luma Dream Machine](luma-dream-machine.md) — Cloud-based video generation when local quality is insufficient
- [Runway ML](runwayml.md) — Cloud alternative for video and advanced image generation
- [Local LLMs](local_llms.md) — LLM infrastructure reference; similar hardware considerations
- [Home Lab Hardware Reference](../../knowledge_base/home-lab-hardware-guide.md) — Hardware-specific sizing for this repo's stack

## Sources / references

- [ComfyUI GitHub Repository](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI Wiki](https://comfyui-wiki.com)
- [OpenArt ComfyUI Workflows](https://openart.ai/workflows/home)
- [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
- [Flux Model Card (Black Forest Labs)](https://huggingface.co/black-forest-labs/FLUX.1-schnell)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
