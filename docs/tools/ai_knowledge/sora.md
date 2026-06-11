# Sora (OpenAI) - [LEGACY]

> [!CAUTION]
> **Sora is officially discontinued.** Web and app experiences were sunsetted on April 26, 2026. The Sora API is scheduled for decommissioning on September 24, 2026. For active production video generation, see [Related tools / concepts](#related-tools--concepts) for current alternatives.

## What it is
Sora was a large-scale text-to-video AI model developed by OpenAI, capable of generating high-fidelity videos up to 60 seconds long. It served as a landmark "world simulator," modeling physical world interactions through video generation.

## What problem it solves
It enabled the creation of complex video content directly from text or images, significantly reducing the overhead for cinematic prototyping and visual storytelling. It was the first model to demonstrate high temporal consistency for characters and objects in long-duration AI video.

## Where it fits in the stack
**Generative Media / Legacy Foundation Model**. Historically, it sat in the high-resolution video generation layer of the AI stack.

## Typical use cases
- **Cinematic Prototyping**: Creating high-fidelity visual concepts.
- **Educational Content**: Generating explanatory videos for complex scenarios.
- **Historical Analysis**: Studying the evolution of diffusion-based video transformers.

## Strengths
- **Temporal Consistency**: Unprecedented stability for characters across 60-second clips.
- **Scene Complexity**: Handled multi-character interactions and complex physics (at the time).
- **Resolution Support**: Native support for various aspect ratios and high-definition output.

## Limitations
- **Availability**: Remained in limited access for most of its lifecycle.
- **Physical Causality**: Occasional struggles with precise cause-and-effect (e.g., bites not leaving marks).
- **End of Life**: No longer supported or accessible for new projects.

## When to use it
- For **historical research** and benchmarking the progress of video generation models.
- When reviewing architectural patterns of early large-scale video transformers.

## When not to use it
- **Active Production**: Use modern alternatives like [Runway Gen-3](runwayml.md) or [Luma Dream Machine](luma-dream-machine.md).
- **Real-time Applications**: Sora was always an asynchronous, computationally intensive process.

## Getting started

> [!NOTE]
> Official access to Sora is no longer available. This section is preserved for historical reference.

### Historical API Implementation (OpenAI Video API)
1. **Submit**: `POST https://api.openai.com/v1/videos` with prompt.
2. **Poll**: `GET https://api.openai.com/v1/videos/{id}` to check status.
3. **Retrieve**: Download once status reached `completed`.

## CLI examples

> [!NOTE]
> CLI tools for Sora are no longer functional due to service sunsetting.

### 1. Status Polling (Historical)
```bash
# Example of what was used to check video status
curl https://api.openai.com/v1/videos/vid_123 -H "Authorization: Bearer $OPENAI_API_KEY"
```

### 2. Submission (Historical)
```bash
# Example of what was used to submit a video prompt
curl https://api.openai.com/v1/videos -d '{ "prompt": "Tokyo street...", "model": "sora-1" }'
```

### 3. Account Check
```bash
# Checking Video API quota (Legacy)
openai api video.quota.get
```

## API examples

### Historical Python Integration
The OpenAI Python library formerly supported Sora via the `videos` namespace:

```python
# [HISTORICAL EXAMPLE - NON-FUNCTIONAL]
from openai import OpenAI

client = OpenAI()

# Sora generation was asynchronous
# video = client.videos.generate(
#     model="sora-1",
#     prompt="A giant cat walks through a tiny city..."
# )
```

## Related tools / concepts
- [Runway Gen-3](runwayml.md) — Recommended production alternative.
- [Luma Dream Machine](luma-dream-machine.md) — High-fidelity video generation alternative.
- [OpenAI](openai.md) — The parent organization.
- [Project Genie](project-genie.md) — Generative world model research.
- [Midjourney](../ai_knowledge/index.md) — High-fidelity image foundation.
- [Pika Labs](../ai_knowledge/index.md) — Video generation alternative.
- [Kling AI](../ai_knowledge/index.md) — Frontier video generation competitor.

## Sources / references
- [OpenAI Sora Official Page (Archived)](https://openai.com/sora)
- [OpenAI Service Sunset Announcement (April 2026)](https://openai.com/news/sora-sunset)
- [Sora API Decommissioning Guide](https://platform.openai.com/docs/guides/legacy-video)

## Contribution Metadata
- Last reviewed: 2026-06-11
- Confidence: high
