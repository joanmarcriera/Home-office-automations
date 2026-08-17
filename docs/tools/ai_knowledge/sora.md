# Sora (OpenAI)

> [!CAUTION]
> **Decommissioned / Sunset**: OpenAI officially sunsetted Sora web and app experiences in April 2026, and fully decommissioned the Sora API on September 24, 2026. This entry serves as a historical reference and legacy asset migration guide for developers.

## What it is
Sora was a large-scale text-to-video AI model developed by OpenAI. It was capable of generating high-fidelity, high-resolution videos up to 60 seconds long while maintaining visual quality, motion consistency, and adherence to complex user prompts.

## What problem it solves
It enabled the creation of complex video content directly from text, significantly reducing the overhead for video production, prototyping, and visual storytelling. It served as an early world simulator, capable of modeling physical world interactions through video generation.

## Where it fits in the stack
**AI Assistants & Knowledge / Generative Media**. Historically a flagship model for high-resolution video generation, now fully decommissioned.

## Typical use cases
- **Cinematic Prototyping**: Creating high-fidelity visual concepts for filmmakers (Historical).
- **Educational Content**: Generating explanatory videos for complex scenarios (Historical).
- **Digital Advertising**: Producing high-quality video assets from text descriptions (Historical).
- **Legacy Asset Archiving**: Retrieving historical Sora output files and metadata for archival pipelines.

## Strengths
- **Consistency**: High temporal consistency for characters and objects across long durations (up to 1 minute).
- **Complexity**: Handled multi-character scenes and complex physical interactions (e.g., liquid splashes, wind movement).
- **Resolution**: Supported various aspect ratios and high-definition output.

## Limitations
- **Decommissioned**: API and model endpoints were completely shut down in late 2026.
- **Physics**: Frequently struggled with precise cause-and-effect (e.g., a cookie bite that didn't leave a mark).
- **Generation Time**: High-fidelity generation was computationally expensive and slow compared to 2027 real-time diffusion models.

## When to use it
- **Historical Analysis**: Studying the evolution of video generation world simulators.
- **Legacy Archive Auditing**: Parsing previously downloaded Sora generation metadata and MP4 files.

## When not to use it
- **New Projects**: Do not attempt to call OpenAI Sora APIs; use active 2027 alternative video generation platforms instead (e.g., Luma Dream Machine 3, Runway Gen-4, Sora 2 legacy open archives).
- **Real-time Generation**: The API is no longer active.

## Getting started

> [!NOTE]
> OpenAI Sora is officially decommissioned. No active cloud API or SDK endpoint is maintained for new video generation requests.

### Installation
For offline metadata processing and legacy archive validation:

```bash
pip install pydantic>=2.0.0 requests
```

### Hello-world example
Inspect and validate local archived Sora metadata:

```python
# Verify local archived Sora prompt metadata
import json

sora_metadata = {"video_id": "sora_legacy_001", "status": "decommissioned", "prompt": "Cyberpunk city in rain"}
print(f"Loaded archived Sora prompt: {sora_metadata['prompt']}")
```

## CLI examples

### 1. Auditing Offline Sora Metadata
Parse local metadata exports for prompt strings and video IDs:

```bash
jq -r '.data[] | "\(.id): \(.prompt)"' legacy_sora_export.json
```

### 2. Batch Verifying Local MP4 Integrity
Run ffmpeg integrity check on archived video files:

```bash
find ./sora_archive -name "*.mp4" -exec ffmpeg -v error -i {} -f null - \;
```

### 3. Inspecting Video Stream Properties
Extract stream codec and duration details from archived MP4 files using ffprobe:

```bash
ffprobe -v quiet -print_format json -show_format -show_streams ./sora_archive/sample_sora.mp4
```

## API examples

### Legacy Sora Asset Parser (Pydantic v2 Schema)
The following Python script demonstrates how to parse and validate legacy Sora video asset metadata from offline exports using Pydantic v2.

```python
import json
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

class LegacySoraAsset(BaseModel):
    video_id: str = Field(..., description="Unique legacy Sora video identifier.")
    prompt: str = Field(..., description="Prompt text used for generation.")
    duration_seconds: int = Field(default=60, ge=1, le=60)
    archived_file_path: Optional[str] = None

    @field_validator('video_id')
    @classmethod
    def validate_video_id(cls, v: str) -> str:
        if not (v.startswith("vid_") or v.startswith("sora_")):
            raise ValueError("Invalid Sora video_id format")
        return v

class SoraArchiveCatalog(BaseModel):
    catalog_version: str = Field(default="2027.1")
    assets: List[LegacySoraAsset]

def parse_sora_archive(json_content: str) -> SoraArchiveCatalog:
    raw_data = json.loads(json_content)
    return SoraArchiveCatalog(
        assets=[LegacySoraAsset(**item) for item in raw_data.get("assets", [])]
    )

# Example usage:
# sample_json = '{"assets": [{"video_id": "vid_2026_001", "prompt": "Tokyo rain", "duration_seconds": 30}]}'
# catalog = parse_sora_archive(sample_json)
# print(catalog.assets[0].prompt)
```

## Related tools / concepts
- [Runway ML](runwayml.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [OpenAI](openai.md)
- [Project Genie](project-genie.md)
- [Synthesia](synthesia.md)
- [Gemini](gemini.md)

## Sources / references
- [OpenAI Sora Discontinuation Notice](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation)
- [OpenAI API Deprecations and Sunset Schedule](https://developers.openai.com/api/docs/deprecations)
- [OpenAI Sora Official Page](https://openai.com/sora)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
