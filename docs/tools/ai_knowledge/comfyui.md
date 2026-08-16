# ComfyUI

## What it is
ComfyUI is an open-source, node-based visual interface, inference execution engine, and API pipeline for local generative image and video diffusion models (FLUX.1, SD3, Wan 2.1, HunyuanVideo, LTX Video, Sora local adapters). Unlike linear user interfaces, ComfyUI structures diffusion pipelines as composable execution graphs where every step—CLIP encoding, KSampler noise schedule, VAE decoding, ControlNet conditioning, and latent upscaling—is visually wired, versionable, and programmatically executable. In early 2027, ComfyUI natively integrates **FastMCP 3.1** for autonomous agentic workflow discovery and execution by frontier reasoning models like Claude 5.1 and GPT-5.5.

## What problem it solves
Eliminates opaque "black-box" generative pipelines by exposing every parameter, tensor transformation, and model conditioning step in an explicit, modular JSON graph. ComfyUI enables developers, artists, and autonomous AI agents to build reproducible, production-grade image and video synthesis workflows that run locally with complete hardware efficiency and zero per-generation API costs.

## Where it fits in the stack
**AI & Knowledge / Local Generative Media**. Serves as the primary local visual and video inference execution layer in the generative AI stack alongside [Ollama](../../services/ollama.md). It operates at the **Inference & Content Generation layer**, producing high-resolution image assets, animation sequences, and synthetic video without cloud dependencies.

## Typical use cases
- **Automated Media Generation Pipelines**: Triggering complex visual workflows (e.g., FLUX.1 image generation, Wan 2.1 video synthesis, upscaling, inpainting) programmatically via n8n or Python scripts.
- **Agentic Visual Tooling**: Enabling autonomous home agents or developer tools (via [FastMCP 3.1](../../tools/automation_orchestration/mcp.md)) to dynamically generate system diagrams, UI prototypes, or task verification screenshots.
- **Controlled Media Production**: Utilizing ControlNet, IP-Adapter, and LoRA nodes to enforce precise pose, depth, style, and brand character consistency across generated assets.
- **Video Generation & Enhancement**: Synthesizing short video clips using state-of-the-art open video models (Wan 2.1, HunyuanVideo, LTX Video) on consumer GPU hardware.

## Strengths
- **Versionable JSON Workflow Graphs**: Complete generation pipelines are stored as standard JSON files, allowing git version control, sharing, and API execution.
- **API-First Architecture**: Native REST endpoint (`/prompt`) and WebSocket API accept structured JSON graphs for full headless automation.
- **FastMCP 3.1 Support**: Native Model Context Protocol server extension allows autonomous agents to discover available workflows, inspect node inputs, and queue generations.
- **Extreme Hardware Efficiency**: Optimized memory management flags (`--lowvram`, `--novram`) and quantization support (gguf/fp8) allow running 30B+ parameter models on consumer GPUs (8GB-16GB VRAM).
- **Vast Ecosystem of Custom Nodes**: Thousands of specialized community nodes managed via `ComfyUI-Manager` for audio, video, 3D mesh, and ControlNet processing.

## Limitations
- **Steep Learning Curve**: Requires deep understanding of latent diffusion mechanics, tensor dimensions, and graph execution order compared to simple text UIs.
- **Ecosystem Node Maintenance**: Custom third-party nodes develop independently, occasionally causing dependency conflicts or breaking changes upon core updates.
- **High VRAM & Storage Footprint**: Storing modern base models, LoRAs, and control models requires hundreds of gigabytes of fast storage (NVMe / ZFS NAS).

## When to use it
- When you require fully local, private, zero-cost image or video generation with fine-grained pipeline control.
- When building automated, programmatic media pipelines integrated into larger home automation, documentation, or agentic frameworks.
- For professional-grade visual control over pose, style, depth, and character consistency using ControlNet and IP-Adapter nodes.

## When not to use it
- If you lack a dedicated GPU with at least 8GB VRAM (CPU generation is prohibitively slow for 2027 diffusion models).
- For simple one-click image generation where simple cloud APIs or web UIs are preferred over custom node graph management.

## Getting started

1. **Clone & Install**:
   ```bash
   git clone https://github.com/comfyanonymous/ComfyUI
   cd ComfyUI
   pip install -r requirements.txt
   ```
2. **Download Models**: Place checkpoint weights (FLUX.1, Wan 2.1, SDXL) in `models/checkpoints/` or `models/diffusion_models/`.
3. **Launch Server**: Start the server using appropriate VRAM optimization flags.
4. **ComfyUI-Manager**: Install `ComfyUI-Manager` to automatically install missing custom node packages.

## CLI examples

Command-line flags are critical for optimizing tensor offloading across hardware environments.

```bash
# Standard launch for NVIDIA GPUs with 12GB+ VRAM
python main.py --gpu-only

# Optimized low-VRAM execution (RTX 4060 8GB / RTX 3060)
python main.py --lowvram --highvram-up-to 4096

# Apple Silicon (M4/M5) acceleration using PyTorch Metal
python main.py --use-pytorch-mps

# Headless API server mode on standard port 8188
python main.py --headless --listen 0.0.0.0 --port 8188
```

## API examples

### Python: Executing a ComfyUI Workflow with Pydantic v2
The following script demonstrates loading, modifying, and queueing a ComfyUI visual generation workflow using Python and **Pydantic v2**.

```python
import json
import urllib.request
import os
from pydantic import BaseModel, Field


class ComfyPromptPayload(BaseModel):
    client_id: str = Field(default="home-admin-agent")
    prompt: dict = Field(..., description="ComfyUI node graph JSON dict")


class PromptResponse(BaseModel):
    prompt_id: str
    number: int


def queue_comfy_workflow(workflow_dict: dict, server_url: str = "127.0.0.1:8188") -> PromptResponse:
    payload_obj = ComfyPromptPayload(prompt=workflow_dict)
    data_bytes = payload_obj.model_dump_json().encode("utf-8")

    req = urllib.request.Request(f"http://{server_url}/prompt", data=data_bytes, headers={"Content-Type": "application/json"})

    with urllib.request.urlopen(req, timeout=10) as response:
        resp_data = json.loads(response.read().decode("utf-8"))
        return PromptResponse(prompt_id=resp_data["prompt_id"], number=resp_data["number"])


if __name__ == "__main__":
    # Example workflow modification logic
    sample_workflow = {
        "3": {
            "inputs": {"seed": 42, "steps": 20, "cfg": 8.0, "sampler_name": "euler"},
            "class_type": "KSampler"
        },
        "6": {
            "inputs": {"text": "a futuristic home laboratory server rack with ambient blue lighting, highly detailed"},
            "class_type": "CLIPTextEncode"
        }
    }

    payload = ComfyPromptPayload(prompt=sample_workflow)
    print(f"Validated ComfyUI Payload Schema: {payload.model_dump_json()[:120]}...")
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Local text LLM engine often paired with ComfyUI prompt generation.
- [n8n](../../services/n8n.md) — Workflow automation orchestrator for triggering ComfyUI endpoints.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Protocol enabling AI agents to discover and invoke ComfyUI nodes.
- [Immich](../../services/immich.md) — Self-hosted photo and video storage for generated assets.
- [Runway ML](runwayml.md) — Cloud-based commercial video generation alternative.
- [Luma Dream Machine](luma-dream-machine.md) — Cloud video synthesis suite.

## Sources / references
- [ComfyUI Official GitHub Repository](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI Community Wiki & Documentation](https://comfyui-wiki.com)
- [Nunchaku Diffusers Inference Engine](https://huggingface.co/blog/nunchaku-diffusers)
- [Scenema Audio Integration for ComfyUI](https://www.reddit.com/r/LocalLLaMA/comments/1vgfmee/scenema_audio_comes_to_comfyui_runs_on_8gb_vram/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
