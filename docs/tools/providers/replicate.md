# Replicate

## What it is
Replicate is a cloud platform that makes it easy to run open-source machine learning models via a simple API, covering everything from LLMs to image generation, video, and audio processing. As of January 2027, it serves as a primary hub for deploying open weights models like **Llama 4**, **DeepSeek-V4**, and multi-modal generation engines, fully supporting the **FastMCP 3.1** protocol for AI agent tool execution.

By abstracting away GPU provisioning, driver configuration, container scaling, and model weights management, Replicate allows developers and autonomous agents to execute thousands of state-of-the-art open-source models using standardized HTTP and FastMCP 3.1 interfaces.

```
+-----------------------------------------------------------------------------------+
|                               AGENT / CLIENT APPLICATION                          |
|                                                                                   |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  |  Claude 5.6 / GPT-5.6   |     |  n8n / Flowise        |     |  Python SDK /   |  |
|  |  Agent Workflows      |     |  Automation Pipelines |     |  cURL Client    |  |
|  +-----------+-----------+     +-----------+-----------+     +--------+--------+  |
|              |                             |                          |           |
+--------------|-----------------------------|--------------------------|-----------+
               |                             |                          |
               v                             v                          v
+-----------------------------------------------------------------------------------+
|                        FASTMCP 3.1 / REPLICATE API GATEWAY                        |
|                                                                                   |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  | Task Correlation ID   |     | Webhook Delivery      |     | Pydantic v2     |  |
|  | Protocol Engine       |     | Event Handler         |     | Schema Guard    |  |
|  +-----------+-----------+     +-----------+-----------+     +--------+--------+  |
+--------------|-----------------------------|--------------------------|-----------+
               |                             |                          |
               v                             v                          v
+-----------------------------------------------------------------------------------+
|                        REPLICATE SERVERLESS GPU CLUSTER                           |
|                                                                                   |
|  +------------------+   +------------------+   +------------------+   +---------+ |
|  | Llama 4 /        |   | Flux.1 / SDXL    |   | HunyuanVideo /   |   | Custom  | |
|  | DeepSeek-V4      |   | Image Generation |   | Video Generation |   | Cog     | |
|  | Text Models      |   | Models           |   | Models           |   | Models  | |
|  +------------------+   +------------------+   +------------------+   +---------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Eliminates the significant complexity of managing GPU infrastructure, CUDA drivers, Docker containers (via their open-source container standard, **Cog**), and model weights for a vast library of open-source AI models. It provides a standardized interface for accessing cutting-edge research models without local hardware requirements.

Without Replicate, running diverse open-source multi-modal models requires managing dedicated NVIDIA H100/A100 GPU instances, handling vLLM/Triton server deployments, managing memory fragmentation, and writing custom API wrappers for every distinct model architecture. Replicate standardizes model inference into a serverless execution model that scales down to zero when idle and instantly scales up under load.

## Where it fits in the stack
**Inference Provider / Multi-modal Hub**. It is an "everything store" for running almost any open-source AI model in the cloud, serving as a critical infrastructure layer for frontier models like **Claude 5.1/5.6**, **GPT-5.5/5.6**, and **Gemini 4.0 Pro/Ultra** to orchestrate multi-modal tasks.

In the enterprise AI stack hierarchy:
1. **Agent Orchestrator Layer**: FastMCP 3.1 clients, Claude Code, n8n, Flowise.
2. **Inference Gateway Layer**: Replicate REST API & FastMCP Gateway Proxy.
3. **Container Packaging Layer**: Cog open-source container specification (`cog.yaml`).
4. **Execution Layer**: Serverless NVIDIA GPU cluster (NVIDIA A100, H100, L40S).

## Typical use cases
- **Multi-modal Agent Pipelines**: Combining an LLM (Llama 4) with an image generator (Flux.1) and a video generator (HunyuanVideo) in a single automated workflow. Under the latest **FastMCP 3.1** schemas, Replicate's native support allows these pipelines to be triggered directly from agentic tools.
- **Rapid Prototyping**: Testing new research models or niche community adapters without any local setup or hardware commitment.
- **Scaling Custom Models**: Moving from a local PyTorch experiment to a global production API instantly using their open-source Cog packaging tool.
- **Automated Media Enhancement**: Running speech-to-text (Whisper), background removal, upscaling, and voice cloning in automated content creation pipelines.
- **AI Agent Tool-Use**: Providing agents with the ability to generate or transform media via a unified FastMCP API.

## Strengths
- **Unrivaled Variety**: Hosts thousands of community and frontier models for text, image, video, audio, 3D, and specialized ML tasks.
- **Cog Ecosystem**: Their open-source packaging tool (Cog) allows you to package and deploy your own custom PyTorch/TensorFlow models to Replicate easily, moving from local script to cloud API with zero infrastructure management.
- **Transparent Per-Second Billing**: Charges purely based on hardware compute duration (per second on CPU, T4, A10G, A100, or H100 GPUs), ideal for intermittent and highly varied workloads.
- **Asynchronous Webhook Support**: Built-in webhook delivery for long-running prediction jobs (e.g., video generation), eliminating the need to hold open long-lived HTTP connections.
- **Multi-modal Swiss Army Knife**: Gold standard for multi-modal access when mixing text generation, speech synthesis, and video transforms in one pipeline.

## Limitations
- **Cold Starts**: Models not in constant public use may experience cold-start delays (15–45 seconds) while serverless GPU containers initialize.
- **High Volume Cost at Scale**: For constant, continuous 24/7 high-throughput LLM text streaming, dedicated serverless LLM providers (e.g., Together AI or Groq) or reserved instances may be more cost-effective.
- **Proprietary SaaS Platform**: While it hosts open weights and uses open-source Cog tools, the Replicate cloud orchestration platform itself is proprietary software.

## When to use it
- When you need a "swiss army knife" of diverse models (especially for non-text tasks like image, video, audio, or 3D generation).
- When you want to deploy your own fine-tuned custom models without managing Kubernetes clusters or GPU drivers.
- For prototyping multi-modal workflows that will later be optimized or deployed to dedicated infrastructure.
- When working with frontier agents that need to dynamically select from a wide range of specialized models via FastMCP 3.1.

## When not to use it
- For ultra-low latency, high-volume LLM-only applications where specialized serverless providers like [Groq](groq.md) or [Together AI](together.md) excel.
- If you require strict air-gapped on-premise execution where cloud APIs are prohibited.
- For basic CRUD applications where foundation models are not required.

## Getting started

### Installation
Install the official Python SDK:

```bash
pip install replicate
```

### Basic API Call (Llama 4)
```python
import os
import replicate

# Ensure REPLICATE_API_TOKEN environment variable is set
os.environ["REPLICATE_API_TOKEN"] = "r8_your_replicate_api_token"

output = replicate.run(
    "meta/meta-llama-4-70b-instruct",
    input={
        "prompt": "Write a python function to compute Fibonacci numbers efficiently.",
        "max_tokens": 512,
        "temperature": 0.2
    }
)

for item in output:
    print(item, end="")
```

### Deploying Custom Models with Cog
1. **Install Cog CLI**:
   ```bash
   sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)
   sudo chmod +x /usr/local/bin/cog
   ```

2. **Define Environment (`cog.yaml`)**:
   ```yaml
   build:
     gpu: true
     python_version: "3.11"
     python_packages:
       - "torch==2.2.0"
       - "transformers==4.38.0"
   predict: "predict.py:Predictor"
   ```

3. **Define Inference Handler (`predict.py`)**:
   ```python
   from cog import BasePredictor, Input, Path
   import torch

   class Predictor(BasePredictor):
       def setup(self):
           """Load the model into GPU memory once."""
           self.device = "cuda" if torch.cuda.is_available() else "cpu"

       def predict(
           self,
           image: Path = Input(description="Input image to process"),
           threshold: float = Input(description="Confidence threshold", default=0.5)
       ) -> str:
           """Run model prediction."""
           return f"Processed image {image} with threshold {threshold}"
   ```

4. **Deploy to Replicate**:
   ```bash
   cog login
   cog push r8.im/your-username/your-custom-model
   ```

## CLI examples

```bash
# Run a text model directly from the command line
replicate run \
  -e REPLICATE_API_TOKEN=$REPLICATE_API_TOKEN \
  meta/llama-4-70b-instruct \
  -input "prompt=Explain quantum computing in one short paragraph."

# Generate an image using Flux.1 Schnell
replicate run \
  black-forest-labs/flux-1-schnell \
  -input "prompt=A futuristic cyberpunk research laboratory in Tokyo, 8k resolution"

# Run local testing on custom Cog model before cloud deployment
cog predict -i image=@sample.jpg -i threshold=0.8
```

## API examples

### Multi-modal Generation Pipeline (Image to Video)
This script demonstrates an automated multi-modal pipeline that generates a high-definition image with Flux.1 and subsequently animates it using Stable Video Diffusion:

```python
import os
import replicate

os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN", "r8_xxxx")

def generate_animated_scene(scene_description: str) -> str:
    print(f"Step 1: Generating image for prompt: '{scene_description}'...")

    # 1. Generate high quality image
    image_output = replicate.run(
        "black-forest-labs/flux-1-schnell",
        input={
            "prompt": scene_description,
            "aspect_ratio": "16:9",
            "output_format": "png"
        }
    )

    # Output is a list of image URLs
    image_url = str(image_output[0])
    print(f"Generated Image URL: {image_url}")

    print("Step 2: Animating image into video clip...")
    # 2. Animate the generated image
    video_output = replicate.run(
        "stability-ai/stable-video-diffusion:3f04571484b857470f394129e710ea5575773958ef4ac2958cf5d6f5f40177e2",
        input={
            "input_image": image_url,
            "frames_per_second": 6,
            "motion_bucket_id": 127
        }
    )

    print(f"Generated Video URL: {video_output}")
    return str(video_output)

if __name__ == "__main__":
    video_result = generate_animated_scene("A cinematic aerial shot of a tranquil waterfall in a misty pine forest")
```

### FastMCP 3.1 Replicate Gateway Server with Pydantic v2
Below is a complete FastMCP 3.1 server exposing Replicate inference capabilities with strict Pydantic v2 runtime validation and task correlation context:

```python
import os
import replicate
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError, HttpUrl
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 server
mcp = FastMCP("replicate-inference-gateway")

class TextGenerationRequest(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 task protocol correlation ID")
    prompt: str = Field(..., min_length=1, max_length=4000, description="Text prompt for LLM")
    model: str = Field(default="meta/meta-llama-4-70b-instruct", description="Target Replicate model identifier")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, ge=1, le=4096)

class ImageGenerationRequest(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 task protocol correlation ID")
    prompt: str = Field(..., min_length=1, max_length=1000, description="Image prompt")
    aspect_ratio: str = Field(default="1:1", pattern=r"^(1:1|16:9|9:16|4:3|3:4)$")
    seed: Optional[int] = Field(default=None, description="Random seed for reproducibility")

@mcp.tool()
async def run_text_inference(request_payload: Dict[str, Any]) -> str:
    """Executes open-weights LLM text generation via Replicate with FastMCP 3.1 task correlation."""
    try:
        req = TextGenerationRequest.model_validate(request_payload)
    except ValidationError as e:
        return f"Task Rejected - Contract Violation: {e.errors()}"

    try:
        output = replicate.run(
            req.model,
            input={
                "prompt": req.prompt,
                "temperature": req.temperature,
                "max_tokens": req.max_tokens
            }
        )
        response_text = "".join([str(chunk) for chunk in output])
        return f"Task {req.task_id} Completed:\n{response_text}"
    except Exception as err:
        return f"Task {req.task_id} Failed - Replicate Error: {str(err)}"

@mcp.tool()
async def run_image_generation(request_payload: Dict[str, Any]) -> str:
    """Generates images using Flux.1 on Replicate with Pydantic v2 validation."""
    try:
        req = ImageGenerationRequest.model_validate(request_payload)
    except ValidationError as e:
        return f"Task Rejected - Schema Violation: {e.errors()}"

    try:
        inputs = {
            "prompt": req.prompt,
            "aspect_ratio": req.aspect_ratio
        }
        if req.seed is not None:
            inputs["seed"] = req.seed

        output = replicate.run("black-forest-labs/flux-1-schnell", input=inputs)
        image_url = str(output[0])
        return f"Task {req.task_id} Image Generated: {image_url}"
    except Exception as err:
        return f"Task {req.task_id} Image Generation Failed: {str(err)}"

if __name__ == "__main__":
    mcp.run()
```

## Provider Comparison Matrix

| Feature / Dimension | Replicate | Together AI | Groq | Hugging Face Endpoints |
| :--- | :--- | :--- | :--- | :--- |
| **Model Scope** | Multi-modal (Text, Image, Video, Audio) | Text LLMs & Code Focus | LLMs & Whisper Speech | Open Source Repository Models |
| **Custom Model Deployment** | Excellent (Via Cog Containers) | Fine-tuning Endpoints | Fixed Hardware Models | Docker / Container Endpoints |
| **FastMCP 3.1 Support** | Excellent (Native Gateway) | Adapter Required | Adapter Required | Community Adapters |
| **Billing Model** | Per-second GPU Hardware Duration | Per-million Tokens | Per-million Tokens | Per-hour Dedicated Instance |
| **Cold Start Behavior** | 15–45s for cold models | Warm Serverless Pools | Instant Warm Pools | Dedicated Warm Instances |
| **Video & 3D Support** | Industry Standard | Limited | None | Community Models |

## Performance & Cost Benchmarks

The following table summarizes average cold-start latencies, execution speeds, and approximate billing rates across hardware tiers on Replicate:

| Hardware Tier | GPU Memory | Primary Model Types | Avg Execution Latency | Approx Billing Rate (USD) |
| :--- | :--- | :--- | :--- | :--- |
| **NVIDIA T4** | 16 GB VRAM | Lightweight Audio/Speech, Whisper | 1.2s - 4.5s | ~$0.000225 / sec |
| **NVIDIA A10G** | 24 GB VRAM | SDXL, Flux.1 Schnell, Code Models | 0.8s - 3.2s | ~$0.000725 / sec |
| **NVIDIA A100 (80GB)**| 80 GB VRAM | Llama 4 70B, DeepSeek-V4, SD Video| 2.5s - 12.0s | ~$0.001400 / sec |
| **NVIDIA 8x A100** | 640 GB VRAM | Large Multi-modal / Video Gen | 15.0s - 45.0s | ~$0.011200 / sec |

## Operational Runbooks & Troubleshooting

### Issue 1: Replicate API `401 Unauthorized` Errors
- **Symptom**: SDK or cURL commands fail with `replicate.exceptions.ReplicateError: 401 Unauthorized`.
- **Root Cause**: `REPLICATE_API_TOKEN` environment variable is missing or contains an expired API token.
- **Resolution**:
  1. Retrieve a valid API token from `https://replicate.com/account/api-tokens`.
  2. Export the variable in your active shell or `.env` file:
     ```bash
     export REPLICATE_API_TOKEN="r8_your_valid_token_here"
     ```
  3. Verify token validity:
     ```bash
     curl -s -H "Authorization: Bearer $REPLICATE_API_TOKEN" https://api.replicate.com/v1/account
     ```

### Issue 2: Prediction Timeout / Long Cold Starts
- **Symptom**: Synchronous prediction calls time out after 60 seconds when invoking lesser-used community models.
- **Root Cause**: The model container is undergoing a cold start, exceeding the default HTTP request timeout.
- **Resolution**:
  1. Switch long-running model calls to use webhooks or background async polling:
     ```python
     prediction = replicate.predictions.create(
         version="model_version_hash",
         input={"prompt": "long background job"},
         webhook="https://example.com/api/replicate-webhook",
         webhook_events_filter=["completed"]
     )
     ```
  2. Increase client timeout parameters when using SDK integrations.

### Issue 3: Cog Container Build Failure (`CUDA Out of Memory`)
- **Symptom**: `cog push` fails during local image building or GPU testing phase with `CUDA out of memory`.
- **Root Cause**: Batch size or model weights exceed local test GPU memory limits specified in `cog.yaml`.
- **Resolution**:
  1. Lower batch size in `predict.py` setup parameters.
  2. Enable half-precision model loading in PyTorch:
     ```python
     self.model = AutoModelForCausalLM.from_pretrained(
         "model_path",
         torch_dtype=torch.float16,
         device_map="auto"
     )
     ```

## Related tools / concepts
- [Hugging Face](huggingface.md) — The primary alternative for open model hosting and dataset storage.
- [Together AI](together.md) — Fast serverless endpoints for open LLMs.
- [OpenRouter](../ai_knowledge/openrouter.md) — Unified multi-provider API for diverse foundation models.
- [Tavily](tavily.md) — AI-native search for RAG workflows.
- [Supabase](../infrastructure/supabase.md) — Vector database and backend storage for AI apps.
- [Groq](groq.md) — Ultra-low latency LLM inference provider.
- [Fireworks AI](fireworks.md) — High-throughput serverless inference for open weights.
- [Mistral AI](mistral.md) — European alternative for open-weights LLMs.
- [LibreChat](../ai_knowledge/librechat.md) — Open source chat interface supporting Replicate gateways.

## Sources / references
- [Official Replicate Website](https://replicate.com/)
- [Replicate API Documentation](https://replicate.com/docs)
- [Model Explorer Catalog](https://replicate.com/explore)
- [Cog Container Packaging Guide](https://github.com/replicate/cog)
- [FastMCP 3.1 Specification](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Licensing and Cost: Paid (Per-second / Usage-based compute). Cog is open-source (Apache 2.0).
- Last reviewed: 2027-01-07
- Confidence: high
