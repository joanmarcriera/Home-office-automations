# Runway ML

## What it is
Runway is a generative AI creative platform specializing in video synthesis, image transformation, and automated media production. As of early January 2027, Runway's flagship **Gen-4** model family (Gen-4 Alpha and Gen-4 Beta) represents state-of-the-art video generation, offering photorealistic text-to-video, image-to-video, and video-to-video capabilities up to 4K resolution. Runway natively integrates with **FastMCP 3.1** (Model Context Protocol), allowing AI agents to generate and edit video assets programmatically.

## What problem it solves
It eliminates the heavy capital and time investments required for physical film shoots, location scouting, complex lighting setups, and manual CGI rendering. Powered by high-performance compute infrastructure (NVIDIA Blackwell/Rubin GPU clusters with TensorRT-LLM acceleration), Runway Gen-4 enables rapid visual asset generation and dynamic rotoscoping. It allows autonomous agents (powered by **Claude 5.1**, **GPT-5.5**, or **Gemini 4.0 Pro**) to trigger programmatic video workflows on demand.

## Where it fits in the stack
**AI & Knowledge / Generative Media**. It functions as a primary generative video production engine alongside systems like Luma Dream Machine and Sora v2, supporting agentic automation via [FastMCP 3.1](../automation_orchestration/mcp.md).

## Typical use cases
- **Cinematic Text-to-Video**: Generating 4K B-roll clips, atmospheric scenes, and concept visual sequences from text prompts.
- **Image-to-Video Animation**: Converting static reference images, character designs, or architectural renders into cinematic shots.
- **Agentic Media Generation**: Allowing autonomous AI pipelines to produce, edit, and export visual content programmatically.
- **VFX Prototyping**: Testing camera motions, dynamic lighting schemes, and subject transformations prior to full video production.

## Strengths
- **Gen-4 Motion Coherence**: Superior temporal stability across multi-second generations with minimal structural distortion.
- **Advanced Camera Controls**: Precision camera movement options (pan, tilt, zoom, orbit, truck) and depth-of-field control.
- **Professional Export Formats**: Exports high-bitrate MP4 and ProRes sequences with custom frame rates (24fps, 30fps, 60fps).
- **FastMCP 3.1 Native**: Standardized tool interface enabling AI assistants to control generation jobs, poll status, and download rendered assets.

## Limitations
- **Credit-Based Pricing**: Commercial 4K video rendering relies on usage-based cloud credits.
- **Asynchronous Latency**: High-resolution 4K video rendering requires queue processing time and is not real-time.
- **Character Continuity at Scale**: Maintaining identical character appearances across disconnected multi-minute scenes requires fine-tuning or reference image chaining.

## When to use it
- When creating high-fidelity AI video for marketing, visual effects, short films, or automated content feeds.
- For building automated media generation pipelines driven by Python or Node.js SDKs.
- When enabling AI agents (e.g., Claude 5.1 or GPT-5.5) to produce cinematic video assets via FastMCP 3.1.

## When not to use it
- For standard non-generative video editing tasks (use DaVinci Resolve or Adobe Premiere).
- For sub-50ms real-time graphics rendering in interactive applications.
- When local, offline video generation without cloud API dependencies is required.

## Getting started

### Installation
Runway provides SDKs for Python and Node.js.

```bash
# Python SDK
pip install runwayml pydantic>=2.0

# Node.js SDK
npm install @runwayml/sdk
```

### Authentication
Retrieve an API key from the Runway developer settings and set `RUNWAY_API_KEY` in your environment.

```python
import runwayml

client = runwayml.Client(api_key="YOUR_RUNWAY_API_KEY")
```

## CLI examples

### 1. Triggering Gen-4 Video Generation via cURL
```bash
curl -X POST https://api.runwayml.com/v1/video/generate \
  -H "Authorization: Bearer $RUNWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gen-4-alpha",
    "prompt": "Cinematic shot of neon rain in a futuristic city, 4K resolution, ray-traced lighting",
    "ratio": "16:9",
    "duration": 10
  }'
```

### 2. Querying Task Status
```bash
curl -s -H "Authorization: Bearer $RUNWAY_API_KEY" \
  https://api.runwayml.com/v1/tasks/task_987654321
```

## API examples

### Programmatic Gen-4 Video Generation with Pydantic v2 Validation
The following Python script demonstrates triggering a Gen-4 video generation task using strict **Pydantic v2** validation:

```python
import os
import time
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import runwayml

class RunwayVideoRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=1000, description="Detailed prompt text")
    model: str = Field(default="gen-4-alpha", description="Runway model version")
    ratio: str = Field(default="16:9")
    duration: int = Field(default=10, ge=5, le=30)

    @field_validator("ratio")
    @classmethod
    def validate_ratio(cls, v: str) -> str:
        allowed = {"16:9", "9:16", "1:1", "21:9"}
        if v not in allowed:
            raise ValueError(f"Ratio must be one of {allowed}")
        return v

def generate_video_clip(request: RunwayVideoRequest) -> str:
    api_key = os.getenv("RUNWAY_API_KEY")
    if not api_key:
        raise ValueError("RUNWAY_API_KEY environment variable is not set.")

    client = runwayml.Client(api_key=api_key)

    # Validated payload dump
    params = request.model_dump()
    print(f"Initiating Runway generation with params: {params}")

    task = client.video.generate(
        model=params["model"],
        prompt=params["prompt"],
        ratio=params["ratio"],
        duration=params["duration"]
    )
    print(f"Task created: {task.id}. Polling for completion...")

    while True:
        status_obj = client.tasks.retrieve(task.id)
        if status_obj.status in ["SUCCEEDED", "FAILED"]:
            break
        time.sleep(5)

    if status_obj.status == "SUCCEEDED":
        return str(status_obj.output_url)
    else:
        raise RuntimeError(f"Runway generation failed: {status_obj.error_message}")

# Execution example
if __name__ == "__main__":
    req = RunwayVideoRequest(
        prompt="A drone shot revealing an autonomous research station in Antarctica, cinematic dusk lighting",
        duration=10
    )
    print("Request validated successfully:")
    print(req.model_dump())
```

### FastMCP 3.1 Tool Request Schema
When an autonomous agent running **Claude 5.1** or **GPT-5.5** invokes Runway Gen-4 via FastMCP 3.1:

```json
{
  "tool": "runway_generate_video",
  "arguments": {
    "prompt": "A drone shot revealing an autonomous research station in Antarctica, cinematic dusk lighting",
    "model": "gen-4-alpha",
    "ratio": "16:9",
    "duration": 10
  }
}
```

## Related tools / concepts
- [Luma Dream Machine](luma-dream-machine.md) — High-fidelity generative video platform.
- [Sora (OpenAI)](sora.md) — Generative video foundation model.
- [Synthesia](synthesia.md) — AI avatar video generation platform.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for agentic tool integration (FastMCP 3.1).
- [NVIDIA](../providers/nvidia.md) — Compute infrastructure provider for AI model inference.
- [ComfyUI](comfyui.md) — Modular node-based UI for diffusion generation workflows.

## Sources / references
- [Runway ML Official Site](https://runwayml.com/)
- [Runway API Documentation](https://docs.runwayml.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
