# Sora (OpenAI)

> [!CAUTION]
> **Sunset Notice**: As of late 2026, OpenAI has discontinued Sora. The web and app experiences were sunsetted on April 26, 2026. The **Sora API is officially scheduled for full decommission on September 24, 2026**. Developers must migrate to alternative video generation platforms immediately.

## What it is
Sora is a large-scale text-to-video AI model developed by OpenAI, currently in its final sunset phase. It is capable of generating high-fidelity videos up to 60 seconds long while maintaining visual quality, motion consistency, and adherence to complex user prompts.

## What problem it solves
It enabled the creation of complex video content directly from text, significantly reducing the overhead for video production, prototyping, and visual storytelling. It served as an early world simulator, capable of modeling physical world interactions through video generation.

## Where it fits in the stack
**AI Assistants & Knowledge / Generative Media**. Historically a flagship model for high-resolution video generation, now transitioning to legacy status.

## Typical use cases
- **Cinematic Prototyping**: Creating high-fidelity visual concepts for filmmakers (Legacy).
- **Educational Content**: Generating explanatory videos for complex scenarios (Legacy).
- **Digital Advertising**: Producing high-quality video assets from text descriptions (Legacy).
- **Data Export & Archiving**: Current primary use case for existing Sora users before the final September 24, 2026 shutdown.

## Strengths
- **Consistency**: High temporal consistency for characters and objects across long durations (up to 1 minute).
- **Complexity**: Handles multi-character scenes and complex physical interactions (e.g., liquid splashes, wind movement).
- **Resolution**: Supports various aspect ratios and high-definition output.

## Limitations
- **Access**: Not available for new public use.
- **Physics**: May still struggle with precise cause-and-effect (e.g., a cookie bite that doesn't leave a mark).
- **Generation Time**: High-fidelity generation is computationally expensive and takes significant time.
- **Sunset Status**: No new features or improvements; API decommission scheduled for September 24, 2026.

## When to use it
- **Historical Analysis**: Studying the evolution of video generation world simulators.
- **Legacy Projects**: Completing existing projects before the September 24, 2026 API shutdown.
- **Data Retrieval**: Exporting and archiving generated assets from the `sora.chatgpt.com/sunset` portal.

## When not to use it
- **New Projects**: Do not start new commercial projects on Sora; use modern alternative video generation platforms instead (e.g., Luma Dream Machine, Runway Gen-3).
- **Real-time Generation**: Sora is computationally intensive and operates on an asynchronous polling pattern.
- **Post-September 2026**: The API and model weights will be completely unavailable for public/API use.

## Getting started

To manage your final Sora assets before the 2026 shutdown:

1. **Export Data**: Visit [sora.chatgpt.com/sunset](https://sora.chatgpt.com/sunset) and click **Export**.
2. **API Migration**: If you have active API integrations, begin switching to alternative video providers (e.g., Luma, Runway, or Pika).
3. **Credit Transfer**: Unused Sora credits can typically be used for other OpenAI models like GPT-5.5 or GPT-4o.

## CLI examples

### Final Asset Audit
Developers can use the CLI to list and download final video assets before deletion:

```bash
# List all video IDs generated on your account
curl https://api.openai.com/v1/videos \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.data[].id'
```

### Checking Generation Status
If generation is still active (prior to API shutdown):

```bash
# Poll for status of a legacy generation job
curl https://api.openai.com/v1/videos/vid_legacy_123 \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Deleting Specific Assets
Proactively deleting assets from OpenAI's final storage buffer:

```bash
curl -X DELETE https://api.openai.com/v1/videos/vid_legacy_123 \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## API examples

### Submitting a Final Generation
Legacy generation pattern (available until September 24, 2026):

```python
import requests

API_URL = "https://api.openai.com/v1/videos"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Submit a 60-second video generation request
response = requests.post(API_URL, headers=headers, json={
    "prompt": "A stylish woman walks down a Tokyo street...",
    "model": "sora-2"
})
video_id = response.json().get("id")
```

### Polling for Completion (with Pydantic v2 validation)
Asynchronous generation status check with modern Pydantic schema validation:

```python
import time
import requests
from pydantic import BaseModel, Field
from typing import Optional

class VideoGenerationStatus(BaseModel):
    id: str
    status: str = Field(..., description="The state of generation (e.g., processing, completed, failed)")
    video_url: Optional[str] = None

def poll_video_status(video_id: str) -> Optional[str]:
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    while True:
        res = requests.get(f"{API_URL}/{video_id}", headers=headers)
        data = res.json()

        # Validate response
        job = VideoGenerationStatus(
            id=data.get("id"),
            status=data.get("status"),
            video_url=data.get("video_url")
        )

        if job.status == "completed":
            return job.video_url
        elif job.status == "failed":
            raise Exception("Generation failed")

        time.sleep(20) # Polling at 20s intervals
```

## Related tools / concepts
- [Runway ML](runwayml.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [OpenAI](openai.md)
- [Project Genie](project-genie.md)
- [Synthesia](synthesia.md)
- [Gemini](gemini.md)
- [Midjourney](../ai_knowledge/index.md)

## Sources / references
- [OpenAI Sora Discontinuation FAQ](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation)
- [OpenAI API Deprecations](https://developers.openai.com/api/docs/deprecations)
- [OpenAI Sora Official Page (Sunset Notice)](https://openai.com/sora)
- [Video generation with Sora (Legacy API Guide)](https://platform.openai.com/docs/guides/video-generation)

## Contribution Metadata
- Last reviewed: 2026-09-03
- Confidence: high
