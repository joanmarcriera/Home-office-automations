# Runway ML

## What it is
Runway is a comprehensive AI-powered creative platform specializing in high-fidelity generative video and professional media production. Its flagship **Gen-5** model represents the late 2026 state-of-the-art in text-to-video, image-to-video, and video-to-video generation, supporting up to 120 seconds of continuous 4K footage and native Model Context Protocol (MCP 3.1) integration.

## What problem it solves
Drastically reduces the cost and technical complexity of professional-grade video production and visual effects. It enables creators to generate cinematic footage and perform complex rotoscoping using NVIDIA Rubin GPU architecture and NIM microservices for accelerated rendering. It provides a robust generative video endpoint for agentic frameworks using Claude 5.1 and GPT-5.5.

## Where it fits in the stack
**AI & Knowledge / Generative Media**. It is the primary engine for high-end AI video generation, creative automation, and temporal diffusion research, fully compatible with [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).

## Typical use cases
- **Cinematic Generation**: Creating 4K B-roll and atmospheric scenes from text prompts or static images using Gen-5.
- **Expressive Human Animation**: Generating realistic human characters with natural movement and native lip-sync capabilities.
- **Creative Automation**: Using the Runway SDK to programmatically generate video for large-scale marketing or social media projects.
- **VFX Prototyping**: Rapidly testing camera angles, dynamic lighting, and motion paths before committing to traditional CGI production.

## Strengths
- **Gen-5 Fidelity**: Exceptional temporal consistency and native 4K visual fidelity, supporting extended clips up to 120 seconds.
- **NVIDIA Rubin Optimization**: Leverages the latest GPU architecture for ultra-fast rendering via NIM GA microservices.
- **Director Mode v2**: Advanced node-based interface for dynamic camera control (zoom, pan, tilt, truck) and physical lighting simulation.
- **Professional Suite**: Includes industry-standard tools like Alpha Channel export (ProRes 4444) and AI-driven inpainting.

## Limitations
- **Operational Cost**: High-fidelity Gen-5 generation is credit-intensive and requires premium subscriptions for professional use.
- **Render Time**: While optimized, high-resolution 4K generations can still take several minutes per clip depending on queue depth.
- **Consistency**: Character identity can still drift over long clips exceeding 60 seconds without fine-tuned models.

## When to use it
- When you need cinematic-quality AI video for filmmaking, advertising, or high-end social media content.
- For building automated video pipelines that require a robust, enterprise-ready Python/Node.js SDK.
- To provide frontier models like Claude 5.1 or GPT-5.5 with a high-fidelity visual generation endpoint.

## When not to use it
- For simple video hosting or standard non-AI editing tasks (use Premiere or DaVinci).
- If you have no budget for cloud-based rendering credits (see [Sora](sora.md) or [Luma Dream Machine](luma-dream-machine.md) for alternatives).
- When strict data privacy requirements necessitate purely local, offline execution.

## Getting started

Runway is accessed via its web studio for creators or through official SDKs for developers.

### Installation
As of late 2026, the official SDKs are available for Python and Node.js.

```bash
# Python
pip install runwayml pydantic>=2.0

# Node.js
npm install @runwayml/sdk
```

### Authentication
Obtain an API Key from the Runway dashboard under **Settings > API**.

```python
import runwayml

# Initialize the client (2026 SDK pattern)
client = runwayml.Client(api_key="YOUR_API_KEY_2026")
```

## CLI examples
> [!NOTE]
> Official CLI examples for Runway ML are primarily managed through SDK integrations or direct API calls. A standalone CLI for end-users is not currently promoted in the late 2026 documentation; developers are encouraged to use the `runwayml` Python package for terminal-based automation.

However, you can perform direct HTTP requests using `curl` to interact with the API endpoints:

```bash
# Trigger a Gen-5 video generation task
curl -X POST https://api.runwayml.com/v1/video/generate \
  -H "Authorization: Bearer $RUNWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gen-5",
    "prompt": "Cinematic shot of neon rain in Neo-Tokyo, 4K, ray-traced",
    "ratio": "16:9",
    "duration": 5
  }'

# Query the status of a specific generation task
curl -H "Authorization: Bearer $RUNWAY_API_KEY" \
  https://api.runwayml.com/v1/tasks/task_987654
```

## API examples

### Text-to-Video (Gen-5)
The following example demonstrates triggering a cinematic 4K generation using the late 2026 Python SDK with polling error handling.

```python
import runwayml
import time
from runwayml.exceptions import RunwayAPIError

client = runwayml.Client(api_key="YOUR_API_KEY")

try:
    # Start a Gen-5 generation task
    task = client.video.generate(
        model="gen-5",
        prompt="A cinematic drone shot of a futuristic neon city in the rain, 4k, hyper-realistic.",
        ratio="16:9",
        duration=10,
        motion_bucket_id=127 # 1-255 scale
    )
    print(f"Task ID: {task.id} - Processing...")

    # Poll for completion with standard retry/backoff logic
    while True:
        task = client.tasks.retrieve(task.id)
        if task.status in ["SUCCEEDED", "FAILED"]:
            break
        time.sleep(10)

    if task.status == "SUCCEEDED":
        print(f"Video URL: {task.output_url}")
    else:
        print(f"Generation failed: {task.error_message}")

except RunwayAPIError as e:
    print(f"API Connection Error: {e}")
```

### Multi-Scene Directing
Using the late 2026 "Scene Scripts" format to direct a multi-step camera move.

```python
# Conceptual example of a structured scene script
scene_script = {
    "scene_1": {
        "duration": 5,
        "camera": "zoom_in",
        "lighting": "golden_hour"
    }
}
# task = client.video.generate(model="gen-5", script=scene_script)
```

## Related tools / concepts
- [Sora (OpenAI)](sora.md) — Main competitor in high-fidelity video.
- [Luma Dream Machine](luma-dream-machine.md) — High-fidelity video generation.
- [Synthesia](synthesia.md) — Avatar-based video generation.
- [ComfyUI](comfyui.md) — Node-based interface for stable diffusion and video.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agentic integration.
- [NVIDIA](../providers/nvidia.md) — Provider of Rubin architecture and NIM GA.
- [Groq](../providers/groq.md) — High-speed inference for model control.
- [Exa AI](../providers/exa_ai.md) — Neural search for visual research.
- [Make](../automation_orchestration/make.md) — Automation hub for video workflows.

## Sources / references
- [Official Website](https://runwayml.com/)
- [Runway API Documentation](https://docs.runwayml.com/)
- [Runway Research: Gen-5 Latent Diffusion](https://runwayml.com/research/gen-5)

## Contribution Metadata
- Last reviewed: 2026-09-25
- Confidence: high
