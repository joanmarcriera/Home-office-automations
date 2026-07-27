# Sora (OpenAI)

> [!CAUTION]
> **Sunset Notice**: OpenAI has officially discontinued Sora. The web and app experiences were sunsetted on April 26, 2026. The **Sora API will be officially decommissioned on September 24, 2026**. All active integrations, user storage buffers, and programmatic access endpoints will be permanently turned off on this date. Developers must finalize their asset migrations and switch to modern, active alternatives immediately.

## What it is
Sora was OpenAI's flagship text-to-video AI model, capable of generating visually rich, high-fidelity videos up to 60 seconds long while maintaining temporal coherence, motion consistency, and adherence to complex natural language descriptions. Now in its final deprecation phase, Sora is primarily used for historical world-simulator analysis and final data retrieval.

## What problem it solves
It temporarily solved the complexity of traditional CGI rendering, expensive physical set prototyping, and narrative visual storytelling by compiling high-level natural language prompts into cohesive, simulated 3D environments. It acted as an early-stage physical world simulator, demonstrating how neural networks could learn complex interactions and cause-and-effect patterns through video pre-training.

## Where it fits in the stack
**AI Assistants & Knowledge / Generative Media**. Transitioning to **Legacy / Decommissioned Status** in September 2026. Developers should replace Sora in their active production stacks with modern generative media pipelines.

## Typical use cases
- **Legacy Asset Archiving**: Automating the download and local archiving of historical cinematic files.
- **Credit Migration Operations**: Transferring outstanding Sora generative credits to active API services (such as Gemini 3.5 or GPT-5.5).
- **Video Stack Adaptation**: Auditing existing codebase pipelines to gracefully transition asynchronous polling calls to alternative 2026 providers.

## Strengths
- **Cinematic Coherence**: Excellent character, object, and lighting consistency across a continuous 60-second span (Legacy).
- **Complex Environment Modeling**: High-fidelity rendering of physics-driven effects such as ocean water splashes, reflective mirrors, and wind-blown foliage (Legacy).
- **Multi-Camera Simulation**: Synthesizing multiple camera angles within a single shot while retaining visual properties (Legacy).

## Limitations
- **Permanent Sunset**: The API and model endpoints are deprecated and scheduled for complete deletion on September 24, 2026.
- **Physical Inconsistencies**: Occasional failures in modeling simple cause-and-effect structures (e.g., a glass breaking without spilling, or eating food without bite marks).
- **No Long-Term Support**: Support tickets, bug fixes, and optimization features have been completely frozen since April 2026.

## When to use it
- To perform final asset audits, download historical generation buffers, and transition existing projects prior to the September 24, 2026 hard shutdown.
- For academic research into early-generation generative video architectures and prompt structures.

## When not to use it
- **All New Projects**: Absolutely do not start new production workflows, features, or pipelines using Sora. Use modern, active alternatives like **Luma Dream Machine v2.0** or **Runway Gen-4** instead.
- **Post-September 24, 2026**: The API endpoints will return standard `410 Gone` errors.

## Getting started

To safely migrate your pipeline and retrieve your video archives before the September 2026 decommission:

### 1. Request Final Archive Export
1. Navigate to the official export console at [sora.chatgpt.com/sunset](https://sora.chatgpt.com/sunset).
2. Click **"Request Full Asset Export"** to compile all historically generated videos, original prompt strings, and JSON metadata schemas into a downloadable ZIP archive.
3. Secure your assets locally or upload them to a centralized private storage bucket (e.g., S3 or Google Cloud Storage).

### 2. Move Active API Credits
Ensure that any remaining credits are rolled over by opening a billing support ticket or selecting **"Roll-Over Credits"** in your OpenAI platform billing dashboard, transforming video credits into generic API credits for GPT-5.5 or DALL-E 3.

### 3. Setup an Alternative Stack
Install and configure the SDK for an active video service such as Luma:

```bash
# Example: Install Luma SDK for 2026 video generation
pip install lumaai
```

## CLI examples

Developers should run the following commands to audit and clean up their OpenAI accounts before the decommissioning date.

### 1. Scan and List All Unexpired Sora Video IDs
Query the OpenAI API to retrieve IDs of all custom videos remaining in your account's cloud cache.

```bash
# List all video assets currently buffered in the OpenAI API storage
curl -s https://api.openai.com/v1/videos \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  | jq '.data[] | {id: .id, created_at: .created_at, status: .status}'
```

### 2. Download and Archive a Specific Legacy Video Asset
Download and save a video locally before the final deletion date.

```bash
# Fetch and download a video file via its legacy URL
curl -L -o "./archives/sora_video_102.mp4" \
  $(curl -s https://api.openai.com/v1/videos/vid_legacy_102 \
    -H "Authorization: Bearer $OPENAI_API_KEY" | jq -r '.video_url')
```

### 3. Proactively Delete an Asset from Cloud Cache
Clean your cloud buffers ahead of the automated platform wipe.

```bash
# Delete a specific video from OpenAI's storage
curl -X DELETE https://api.openai.com/v1/videos/vid_legacy_102 \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## API examples

The following legacy scripts illustrate the original Sora generation patterns alongside modern migration strategies.

### 1. Legacy Sora Generation Pipeline (Discontinuing September 24, 2026)
This asynchronous script represents the historical method used to request video compilation and poll for status.

```python
import os
import time
import requests

API_URL = "https://api.openai.com/v1/videos"
headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
}

# 1. Dispatch asynchronous generation request
def submit_legacy_generation(prompt: str) -> str:
    print("Warning: Calling deprecated Sora API. Endpoints decommission on Sept 24, 2026.")
    payload = {
        "prompt": prompt,
        "model": "sora-2-turbo",
        "aspect_ratio": "16:9",
        "duration": "10s"
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["id"]

# 2. Poll for completion (legacy pattern)
def poll_video_status(video_id: str) -> str:
    while True:
        res = requests.get(f"{API_URL}/{video_id}", headers=headers)
        res.raise_for_status()
        data = res.json()

        status = data.get("status")
        if status == "completed":
            return data["video_url"]
        elif status == "failed":
            raise Exception(f"Generation failed: {data.get('error')}")

        print("Video still rendering. Waiting 30 seconds...")
        time.sleep(30)
```

### 2. Active 2026 Alternative Video Generation (Luma SDK)
This modern, non-deprecated pattern should be used to replace Sora-based calls in your active systems.

```python
import os
from lumaai import LumaAI

# Initialize Luma SDK for September 2026 state-of-the-art generation
client = LumaAI(auth_token=os.getenv("LUMA_API_KEY"))

try:
    print("Initiating active video generation using Luma Dream Machine...")
    generation = client.generations.create(
        prompt="A continuous panning shot of an automated cleanroom laboratory, high-tech robotics...",
        aspect_ratio="16:9",
        loop=False
    )
    print(f"Luma Job Created successfully! Job ID: {generation.id}")
except Exception as e:
    print(f"Failed to create Luma generation: {str(e)}")
```

## Related tools / concepts
- [Runway ML](runwayml.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [OpenAI](openai.md)
- [Project Genie](project-genie.md)
- [Synthesia](synthesia.md)
- [Google Gemini](google-gemini.md)
- [Midjourney](../ai_knowledge/index.md)

## Sources / references
- [OpenAI Sora Discontinuation Announcement and FAQ](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation)
- [OpenAI Developer Platform Deprecation Timelines](https://developers.openai.com/api/docs/deprecations)
- [Runway Gen-4 Developer Guide](https://runwayml.com/research/gen-4)
- [Luma Dream Machine API Reference v2.0](https://docs.lumalabs.ai/dream-machine-api)

## Contribution Metadata
- Last reviewed: 2026-09-04
- Confidence: high
