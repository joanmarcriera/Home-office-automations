# ComfyUI

## What it is
ComfyUI is an open-source, node-based visual interface, execution engine, and REST/WebSocket API pipeline for local generative image, video, and audio diffusion models (e.g., FLUX.1, SD3.5, Wan 2.1, HunyuanVideo, LTX Video, and Sora local adapters). Unlike linear or template-bound user interfaces, ComfyUI structures generation pipelines as composable execution graphs where every tensor transformation—CLIP/T5 text encoding, VAE latent space encoding/decoding, KSampler noise schedule calculations, ControlNet conditioning, LoRA weight injection, and latent upscaling—is visually wired, versionable as standard JSON, and programmatically executable.

In early 2027, ComfyUI serves as a native inference backend for **FastMCP 3.1** (Model Context Protocol), enabling autonomous agentic workflows where frontier reasoning models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL) programmatically inspect node graph schemas, queue non-blocking inference jobs, monitor WebSocket progress streams, and consume generated media assets within automated home-lab and enterprise operations.

## What problem it solves
- **Eliminates Black-Box Generative Pipelines**: Exposes every parameter, noise scheduler step, model weight merge, and latent space manipulation as an explicit, observable node in an execution DAG (Directed Acyclic Graph).
- **Enables Headless Programmatic Automation**: Provides native REST and WebSocket interfaces (`/prompt`, `/history`, `/ws`) that allow external scripts, automation servers (n8n), and FastMCP 3.1 agents to trigger visual generation workflows without requiring human GUI interactions.
- **Maximizes Consumer Hardware VRAM Efficiency**: Employs advanced PyTorch memory management techniques—such as smart model weight offloading (`--lowvram`, `--novram`), GGUF/FP8/FP4 quantization, and FlashAttention-3 integration—enabling multi-billion parameter diffusion models (e.g., FLUX.1 12B, Wan 2.1 14B) to execute on consumer GPUs with 8GB to 24GB VRAM.
- **Eliminates Cloud API Dependencies & Recurring Costs**: Provides zero-cost, private, local image and video generation with zero telemetry, data leakage risks, or rate limits.

## Where it fits in the stack
**AI & Knowledge / Local Generative Media Layer**. ComfyUI functions alongside local LLM engines like [Ollama](../../services/ollama.md) and vLLM. It forms the core visual and multi-modal generation engine within local AI stacks, receiving requests from client applications, agent frameworks (LangGraph, CrewAI), or n8n workflows and producing processed image or video outputs directly to self-hosted storage targets like [Immich](../../services/immich.md) or [MinIO](../intake_storage/minio.md).

```
+-----------------------------------------------------------------------------------+
|                            Agents & Orchestration Layer                           |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  | FastMCP 3.1 Server |   |  n8n Automation Hub   |   |   Claude / GPT Agent   |  |
|  | (ComfyUI Gateway)  |   | (Image Generation Flow|   | (Vision System Script) |  |
|  +---------+----------+   +-----------+-----------+   +-----------+------------+  |
+------------|--------------------------|---------------------------|---------------+
             |                          |                           |
             +--------------------------+---------------------------+
                                        |
                                        v HTTP REST / WebSocket JSON Graph
                                        |  - POST /prompt (Queue Job)
                                        |  - GET /history/{prompt_id}
                                        |  - WS /ws?clientId={id} (Live Execution Stream)
+---------------------------------------v-------------------------------------------+
|                          ComfyUI Inference Architecture                           |
|  +-----------------------------------------------------------------------------+  |
|  |                         Web Server & API Router                             |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   | Prompt Queue & Manager   |  | WebSocket Broadcast & Execution Tracker|  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|  +-----------------------------------------------------------------------------+  |
|  |                         Node Execution Engine (DAG)                         |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   | Model Loader & Offloader |  | KSampler & Noise Schedule Engine       |  |  |
|  |   | (FP8/GGUF/FlashAttention3|  | (Euler/DPM++/UniPC/Latent Conditioning) |  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   | VAE Decoder Engine       |  | Custom Node Ecosystem & Plugins        |  |  |
|  |   | (Latent -> Tensor -> PNG)|  | (ComfyUI-Manager / ControlNet / LoRA)  |  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|  +-----------------------------------------------------------------------------+  |
|  |                         Hardware Acceleration Layer                         |  |
|  |   +---------------------------------------------------------------------+   |  |
|  |   |  NVIDIA CUDA / PyTorch MPS (Apple Silicon) / ROCm AMD Acceleration  |   |  |
|  |   +---------------------------------------------------------------------+   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Headless FastMCP 3.1 Agent Media Synthesis**: Enabling AI agents to programmatically build and execute visual workflows (e.g., generating documentation diagrams, UI wireframes, synthesized training datasets, or verification screenshots).
- **Automated Content Creation Workflows**: Triggering video generation pipelines (e.g., combining text-to-speech with Wan 2.1 video synthesis and Audio-Driven Lip-Sync custom nodes) via n8n automation triggers.
- **Precision Image Control via ControlNet & IP-Adapter**: Generating brand-consistent visual assets with strict pose, openpose, depth map, or style guidance without manual repainting.
- **Batch Processing & Upscaling**: Automated batch processing pipelines for upscaling, denoising, and restoring image archives stored in [Paperless-ngx](../../services/paperless-ngx.md) or [Immich](../../services/immich.md).

## Node Graph & Execution Lifecycle

In ComfyUI, a generation request consists of an object map where keys are node IDs and values represent node properties and input connections.

```
+-------------------+      +-----------------------+
|  CheckpointLoader |----->|     CLIPTextEncode    |
|  (FLUX.1 / SD3)   | model|   (Positive Prompt)   |
+---------+---------+      +-----------+-----------+
          |                            |
          | CLIP                       | CONDITIONING
          v                            v
+-------------------+      +-----------------------+      +-------------------+
|   EmptyLatentImage|----->|        KSampler       |----->|    VAEDecode      |----> Output Image
|   (1024x1024)     | latent|  (Noise Scheduler)   | latent|  (Tensor -> PNG) |      (PNG/WebP)
+-------------------+      +-----------------------+      +-------------------+
```

During execution:
1. **Validation & Topological Sort**: The server evaluates the JSON payload, checks node input/output data types, constructs a Directed Acyclic Graph (DAG), and orders execution.
2. **Dynamic Weight Management**: Checkpoint model weights, LoRA adapters, and CLIP encoders are selectively loaded into VRAM. Standard nodes offload unneeded model tensors back to System RAM as execution shifts between text encoding, sampling, and VAE decoding.
3. **Execution Stream via WebSockets**: Real-time progress percentage, execution errors, node preview images, and step timings are pushed over the active WebSocket channel (`/ws`).

## Strengths
- **Versionable Graph Schemas**: Workflows are plain JSON documents, easily stored in Git, diffed, modified by scripts, or generated dynamically by LLMs.
- **Native Non-Blocking REST API**: Decoupled prompt queue architecture handles incoming API generation requests asynchronously without freezing the frontend UI.
- **FastMCP 3.1 Tool Compatibility**: Clean separation of input parameters allows wrappers to expose workflow inputs as validated agent tools.
- **Extensive Community Node Ecosystem**: Thousands of custom nodes managed via `ComfyUI-Manager` extend core capabilities to audio synthesis, 3D mesh rendering, video interpolation, and LLM vision integration.
- **State-of-the-Art Multi-Modal Support**: Day-one implementation for frontier open models (FLUX.1, Wan 2.1, SD3.5, HunyuanVideo, LTX Video).

## Limitations
- **Ecosystem Node Version Drift**: Third-party custom nodes can introduce dependency conflicts or fail when core ComfyUI node definitions undergo breaking changes.
- **Large VRAM & Disk Storage Footprint**: Multi-model video and image pipelines require significant high-speed storage (hundreds of gigabytes on fast NVMe SSDs) and 12GB+ GPU VRAM for fluid execution.
- **Graph Complexity for Beginners**: Requires an understanding of tensor shapes, latent space dimensions, and sampling algorithms compared to monolithic web UIs.

## When to use it
- When operating a self-hosted visual generation pipeline with programmatic access for n8n or FastMCP 3.1 agent frameworks.
- When you need precise, reproducible control over multi-stage image/video workflows (ControlNet, IP-Adapter, LoRA, Upscaling).
- For local, private generation requiring multi-GPU or low-VRAM optimizations on consumer hardware.

## When not to use it
- If you lack a CUDA/MPS-capable GPU with at least 8GB VRAM.
- For single-click, conversational web UI creation where simplified text-to-image prompt boxes are preferred over custom node graph design.

## Getting started

```bash
# Clone official repository
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Install PyTorch and core requirements
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt

# Install ComfyUI-Manager for automated node management
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
cd ..

# Launch API server with low-VRAM optimization
python main.py --lowvram --listen 0.0.0.0 --port 8188
```

## CLI examples

ComfyUI flags configure VRAM management, execution backends, and listening ports:

```bash
# Standard deployment for high-VRAM GPUs (24GB+)
python main.py --gpu-only --highvram --port 8188

# Optimized memory setting for consumer GPUs (8GB - 12GB VRAM)
python main.py --lowvram --highvram-up-to 4096 --listen 127.0.0.1

# Apple Silicon (M-Series MPS) optimized execution
python main.py --use-pytorch-mps --use-split-cross-attention

# Headless server mode for Docker or background systemd services
python main.py --headless --listen 0.0.0.0 --port 8188 --no-preview
```

## API examples

### FastMCP 3.1 Server Executing ComfyUI API Workflows

The following production implementation demonstrates a FastMCP 3.1 tool server exposing a ComfyUI generation tool with strict Pydantic v2 input validation, JSON workflow modification, and asynchronous REST queueing:

```python
import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError, field_validator

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Sovereign-ComfyUI-Gateway")

COMFY_HOST = os.getenv("COMFYUI_HOST", "127.0.0.1:8188")

# --- Pydantic v2 Validation Schemas ---

class TextToImageInput(BaseModel):
    positive_prompt: str = Field(..., min_length=3, max_length=2000, description="Detailed text prompt describing desired visual output")
    negative_prompt: Optional[str] = Field(default="blurry, distorted, low quality, artifacts", description="Unwanted visual elements")
    seed: Optional[int] = Field(default=42, ge=0, le=2**64 - 1, description="Random seed for deterministic sampling")
    steps: int = Field(default=20, ge=1, le=100, description="KSampler execution step count")
    cfg_scale: float = Field(default=7.5, ge=1.0, le=20.0, description="Classifier-Free Guidance scale")
    width: int = Field(default=1024, ge=512, le=2048, description="Target latent width")
    height: int = Field(default=1024, ge=512, le=2048, description="Target latent height")

    @field_validator("width", "height")
    def validate_dimension_multiples(cls, v: int) -> int:
        if v % 64 != 0:
            raise ValueError("Dimensions must be multiples of 64 for VAE latent space alignment")
        return v

class ComfyPromptPayload(BaseModel):
    client_id: str = Field(default="fastmcp-agent-client")
    prompt: Dict[str, Any] = Field(..., description="Topologically sorted node execution graph JSON")

class ComfyQueueResponse(BaseModel):
    prompt_id: str = Field(..., description="Unique UUID tracking the queued job in ComfyUI")
    number: int = Field(..., description="Queue order position integer")

# --- Default Node Template Generator ---

def build_default_flux_workflow(params: TextToImageInput) -> Dict[str, Any]:
    """Constructs a basic API node graph for ComfyUI execution."""
    return {
        "3": {
            "inputs": {
                "seed": params.seed,
                "steps": params.steps,
                "cfg": params.cfg_scale,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {
                "ckpt_name": "flux1-dev-fp8.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {
                "width": params.width,
                "height": params.height,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {
                "text": params.positive_prompt,
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": params.negative_prompt or "",
                "clip": ["4", 1]
            },
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            },
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": "FastMCP_Agent_Output",
                "images": ["8", 0]
            },
            "class_type": "SaveImage"
        }
    }

# --- FastMCP 3.1 Tool Definitions ---

@mcp.tool(
    name="generate_image",
    description="Queues a local image generation workflow on ComfyUI via API with validated parameters."
)
def generate_image(input_params: TextToImageInput) -> ComfyQueueResponse:
    """Validates prompt params, constructs a ComfyUI node graph, and posts to /prompt endpoint."""
    graph_dict = build_default_flux_workflow(input_params)

    payload = ComfyPromptPayload(
        client_id="fastmcp-media-agent",
        prompt=graph_dict
    )

    data_bytes = payload.model_dump_json().encode("utf-8")
    req = urllib.request.Request(
        f"http://{COMFY_HOST}/prompt",
        data=data_bytes,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            resp_bytes = response.read()
            resp_json = json.loads(resp_bytes.decode("utf-8"))
            return ComfyQueueResponse.model_validate(resp_json)
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to communicate with ComfyUI server at {COMFY_HOST}: {e}")

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Ollama](../../services/ollama.md): Local LLM inference engine frequently paired with ComfyUI for prompt expansion.
- [n8n](../../services/n8n.md): Automation hub for triggering headless ComfyUI workflows via HTTP REST nodes.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): Standard for connecting AI agents to local tool capabilities.
- [Immich](../../services/immich.md): Self-hosted media library engine for auto-ingesting ComfyUI output images and videos.
- [MinIO](../intake_storage/minio.md): Object storage platform for archiving generative media assets.
- [Runway ML](runwayml.md): Cloud commercial video generation platform.
- [Luma Dream Machine](luma-dream-machine.md): Proprietary video synthesis backend.

## Sources / references
- [ComfyUI Official Source Code Repository](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI API & Execution Architecture Documentation](https://docs.comfy.org/)
- [ComfyUI-Manager Plugin Ecosystem Catalog](https://github.com/ltdrdata/ComfyUI-Manager)
- [FastMCP 3.1 Specification & Task Protocol](https://modelcontextprotocol.io/3.1/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
