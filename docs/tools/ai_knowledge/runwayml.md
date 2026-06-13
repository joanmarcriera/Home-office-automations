# Runway ML

## What it is
Runway is a comprehensive AI-powered creative platform specializing in high-fidelity generative video and professional media production. Its flagship **Gen-4** model represents the 2026 state-of-the-art in text-to-video, image-to-video, and video-to-video generation, supporting up to 60 seconds of continuous 4K footage.

## What problem it solves
Drastically reduces the cost and technical complexity of professional-grade video production and visual effects. It enables creators to generate cinematic footage, perform complex rotoscoping, and reimagining existing video content through AI-assisted workflows that previously required massive render farms and manual labor.

## Where it fits in the stack
**AI & Knowledge / Generative Media**. It is the primary engine for high-end AI video generation, creative automation, and temporal diffusion research.

## Typical use cases
- **Cinematic Generation**: Creating 4K B-roll and atmospheric scenes from text prompts or static images using Gen-4.
- **Expressive Human Animation**: Generating realistic human characters with natural movement and native lip-sync capabilities.
- **Creative Automation**: Using the Runway SDK to programmatically generate video for large-scale marketing or social media projects.
- **VFX Prototyping**: Rapidly testing camera angles and motion paths before committing to traditional CGI production.

## Strengths
- **Gen-4 Fidelity**: Exceptional temporal consistency and 4K visual fidelity, supporting clips up to 60 seconds.
- **Motion Brush 3.0**: Precise vector control over specific areas of an image to direct movement with granular speed settings.
- **Director Mode**: Node-based interface for dynamic camera control (zoom, pan, tilt, truck) and lighting physics.
- **Professional Suite**: Includes industry-standard tools like Alpha Channel export (ProRes 4444) and AI-driven inpainting.

## Limitations
- **Operational Cost**: High-fidelity Gen-4 generation is credit-intensive and requires premium subscriptions for professional use.
- **Render Time**: While optimized, high-resolution 4K generations can still take several minutes per clip.
- **Consistency**: Character identity can still drift over long clips exceeding 30 seconds without fine-tuned models.

## When to use it
- When you need cinematic-quality AI video for filmmaking, advertising, or high-end social media content.
- For building automated video pipelines that require a robust, enterprise-ready Python/Node.js SDK.
- To provide frontier models like `claude-4-8-opus-20260528` or GPT-5.5 with a high-fidelity visual generation endpoint.

## When not to use it
- For simple video hosting or standard non-AI editing tasks (use Premiere or DaVinci).
- If you have no budget for cloud-based rendering credits (see [Sora](sora.md) or [Luma Dream Machine](luma-dream-machine.md) for alternatives).
- When strict data privacy requirements necessitate purely local, offline execution.

## Getting started

Runway is accessed via its web studio for creators or through official SDKs for developers.

### Installation
As of 2026, the official SDKs are available for Python and Node.js.

```bash
# Python
pip install runwayml

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
> Official CLI examples for Runway ML are primarily managed through SDK integrations or direct API calls. A standalone CLI for end-users is not currently promoted in the 2026 documentation; developers are encouraged to use the `runwayml` Python package for terminal-based automation.

## API examples

### Text-to-Video (Gen-4)
The following example demonstrates triggering a cinematic 4K generation using the Python SDK.

```python
import runwayml
import time

client = runwayml.Client(api_key="YOUR_API_KEY")

# Start a Gen-4 generation task
task = client.video.generate(
    model="gen-4",
    prompt="A cinematic drone shot of a futuristic neon city in the rain, 4k, hyper-realistic.",
    ratio="16:9",
    duration=10,
    motion_bucket_id=127 # 1-255 scale
)

print(f"Task ID: {task.id} - Processing...")

# Poll for completion
while task.status not in ["SUCCEEDED", "FAILED"]:
    time.sleep(5)
    task = client.tasks.retrieve(task.id)

if task.status == "SUCCEEDED":
    print(f"Video URL: {task.output_url}")
```

### Multi-Scene Directing
Using the 2026 "Scene Scripts" format to direct a multi-step camera move.

```python
# Conceptual example of a structured scene script
scene_script = {
    "scene_1": {
        "duration": 5,
        "camera": "zoom_in",
        "lighting": "golden_hour"
    }
}
# task = client.video.generate(model="gen-4", script=scene_script)
```

## Related tools / concepts
- [Sora (OpenAI)](sora.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [Synthesia](synthesia.md)
- [Project Genie](project-genie.md)
- [ComfyUI](comfyui.md)
- [Groq](../providers/groq.md) (for high-speed model control)
- [Exa AI](../providers/exa_ai.md) (for visual research)
- [AI Templates](aitmpl.md)

## Sources / references
- [Official Website](https://runwayml.com/)
- [Runway API Documentation](https://docs.runwayml.com/)
- [Runway Research: Gen-4 Latent Diffusion](https://runwayml.com/research/gen-4)
- [Runway Gen-4 Guide 2026](https://aitoolsdevpro.com/ai-tools/runway-guide/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
