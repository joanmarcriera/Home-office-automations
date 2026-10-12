# Sora (OpenAI)

> [!CAUTION]
> **Decommissioned / Sunset**: OpenAI officially sunsetted Sora web and application user experiences in April 2026, and fully decommissioned the Sora API on September 24, 2026. This documentation serves as a historical architectural reference, legacy asset migration guide, and technical post-mortem analysis for generative media engineers.

## What it is
Sora was a landmark, large-scale spatio-temporal diffusion transformer (DiT) text-to-video generative model developed by OpenAI. Operating as a diffusion model trained over variable-size visual patch latent spaces, Sora generated high-fidelity, high-resolution videos (up to 1080p) lasting up to 60 seconds with spatial consistency, realistic physics approximations, and multi-angle cinematic coherence.

```
+-----------------------------------------------------------------------------------+
|                            SORA ARCHITECTURAL PIPELINE                            |
+-----------------------------------------------------------------------------------+
|  [Raw Text Prompt / Image Input]                                                  |
|                │                                                                  |
|                ▼                                                                  |
|  [GPT-4o Prompt Rewriter & Spatial Decomposition]                                 |
|                │                                                                  |
|                ▼                                                                  |
|  [3D Spatio-Temporal Patch Tokenizer (Spatial x Temporal Compression)]           |
|                │                                                                  |
|                ▼                                                                  |
|  [Diffusion Transformer (DiT) Latent Denoiser - Variable Aspect Grid]            |
|                │                                                                  |
|                ▼                                                                  |
|  [Visual Latent Decoder & Frame Assembler]                                        |
|                │                                                                  |
|                ▼                                                                  |
|  [H.264 / HEVC Master Stream Output (.mp4)]                                       |
|                │                                                                  |
|                ▼                                                                  |
|  [FastMCP 3.1 Legacy Archive Indexing & Pydantic v2 Catalog Validation]           |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Prior to Sora, video generation models suffered from severe temporal distortion, visual warping over extended frame durations (>5 seconds), restricted aspect ratio constraints, and failure to model basic physical interactions (such as liquid splashes, reflections, or object persistence). Sora solved these fundamental generative media limitations by scaling transformer architectures over visual patch tokens, effectively establishing the technical paradigm for modern spatio-temporal world simulators.

## Where it fits in the stack
**AI Assistants & Knowledge / Generative Media**. Historically positioned as OpenAI's flagship generative video architecture and cloud API; currently maintained as a legacy archival dataset reference and historical benchmark in generative media pipelines.

## Typical use cases
- **Cinematic Prototyping & Storyboarding**: Generating high-fidelity previz sequences for film directors and narrative teams (Historical).
- **Physical World Simulation**: Evaluating model ability to learn 3D visual persistence, camera movement dynamics, and light transport (Historical).
- **Digital Marketing & Visual Assets**: Rapidly synthesizing custom video clips from descriptive textual prompts (Historical).
- **Legacy Asset Migration & Archive Indexing**: Extracting, cataloging, and re-indexing historical Sora video files and prompt metadata using FastMCP 3.1 tools and Pydantic v2 schemas.

## Technical Comparison Matrix

| Feature / Dimension | OpenAI Sora (Legacy) | Runway Gen-4 (2027) | Luma Dream Machine 3 | HunyuanVideo (Open Weights) |
| :--- | :--- | :--- | :--- | :--- |
| **Status (2027)** | Decommissioned | Active Commercial Cloud | Active Commercial Cloud | Active Open Weights |
| **Max Clip Duration** | 60 seconds | 30 seconds (Chainable) | 120 seconds | 16 seconds |
| **Native Resolution** | 1080p (Variable Grid) | 4K Upscaled | 1080p / 4K | 720p / 1080p |
| **Architecture** | Spatio-Temporal DiT | Latent Flow Matching DiT | Real-Time Latent DiT | Multimodal Transformer DiT |
| **Interactive Latency** | Offline Batch (~2-5 min) | Sub-15s Streaming | Near Real-Time (3s) | Dependent on Local VRAM |
| **Self-Hosting** | No (Proprietary Cloud) | No (Cloud API) | No (Cloud API) | Yes (Dual-80GB VRAM) |
| **FastMCP 3.1 Support** | Archival Catalog Only | Native Control API | Native Control API | Native Local MCP Tool |

## Strengths
- **Spatio-Temporal Consistency**: Maintained continuous object identity, character features, and background geometry across multi-second camera passes.
- **Variable Frame Geometry & Aspect Ratios**: Natively supported 1920x1080, 1080x1920, and square 1080x1080 resolutions without cropping or stretching.
- **Visual Patch Latent Architecture**: Scaled video generation analogous to language modeling by treating video slices as sequence tokens.

## Limitations
- **Full API Decommissioning**: Cloud API endpoints, WebSocket streams, and web client interfaces were entirely shut down by OpenAI in late 2026.
- **Complex Causal Physics Failures**: Frequently struggled with exact cause-and-effect physical interactions (e.g., biting a sandwich without removing material).
- **Extreme Computational Overhead**: High-resolution video sampling required massive multi-GPU cluster compute, leading to higher inference costs relative to 2027 real-time video diffusion architectures.

## When to use it
- **Historical Technical Research**: Studying the architectural transition from UNet diffusion to Spatio-Temporal Diffusion Transformers (DiT).
- **Legacy Archive Migration**: Parsing, validating, and migrating local historical Sora MP4 video archives and JSON metadata exports.

## When not to use it
- **Active Video Generation Pipelines**: Do not attempt to invoke OpenAI Sora endpoints. Use active 2027 video generation tools such as Luma Dream Machine 3, Runway Gen-4, or open-weights video models instead.
- **Real-Time Interactive Framing**: Sora's offline sampling architecture was not designed for sub-second real-time interactive generation.

## Getting started

> [!NOTE]
> OpenAI Sora is fully decommissioned. Active API access is no longer available. Instructions below cover legacy archive processing and metadata parsing.

### Installation & Environment Setup
Install tools required for inspecting local video files, parsing legacy JSON metadata, and running FastMCP 3.1 verification tools:

```bash
# Install Pydantic v2 and FastMCP 3.1 for archive management
pip install "pydantic>=2.0.0" "mcp>=1.0.0" requests

# Ensure ffmpeg and ffprobe are available for video validation
sudo apt-get update && sudo apt-get install -y ffmpeg jq
```

## CLI examples

### 1. Batch Verifying Local Archive Video Integrity
Run `ffmpeg` diagnostic checks across archived Sora video output files to verify stream health:

```bash
find ./sora_archive -type f -name "*.mp4" -exec ffmpeg -v error -i {} -f null - \;
```

### 2. Extracting Stream Properties via `ffprobe`
Query video resolution, frame rate, and codec parameters from historical Sora MP4 files:

```bash
ffprobe -v quiet -print_format json -show_format -show_streams ./sora_archive/vid_sora_2026_001.mp4 | jq .
```

### 3. Parsing Prompt Metadata Records with `jq`
Filter and extract prompt descriptions and video IDs from legacy bulk exports:

```bash
jq -r '.assets[] | "ID: \(.video_id) | Duration: \(.duration_seconds)s | Prompt: \(.prompt)"' sora_export_archive.json
```

### 4. Re-encoding Legacy Assets for Mobile Streaming
Optimize legacy 1080p Sora clips for fast web preview playback using `ffmpeg`:

```bash
ffmpeg -i ./sora_archive/raw_clip.mp4 -vcodec libx264 -crf 23 -preset fast -acodec aac -movflags +faststart ./sora_archive/web_optimized.mp4
```

## API examples

### Python FastMCP 3.1 & Pydantic v2 Archive Catalog Integration
The following code snippet demonstrates building a FastMCP 3.1 server that indexes, validates, and serves historical Sora video archive assets using Pydantic v2 data models:

```python
import os
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# Define Pydantic v2 models for legacy Sora asset validation
class SoraLegacyAsset(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    video_id: str = Field(..., description="Unique Sora video generation identifier (e.g., 'sora_2026_001').")
    prompt: str = Field(..., description="Text prompt used during original video generation.")
    expanded_prompt: Optional[str] = Field(None, description="GPT-4o rewritten conditioning prompt.")
    duration_seconds: int = Field(default=60, ge=1, le=60, description="Video clip length in seconds.")
    resolution: str = Field(default="1920x1080", description="Video stream spatial resolution.")
    aspect_ratio: str = Field(default="16:9", description="Target aspect ratio frame geometry.")
    file_path: str = Field(..., description="Local file path to archived MP4 file.")
    archived_at: str = Field(..., description="ISO 8601 timestamp when asset was ingested into archive.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom generation parameters (seed, CFG score).")

    @field_validator("video_id")
    @classmethod
    def validate_video_id(cls, value: str) -> str:
        if not (value.startswith("sora_") or value.startswith("vid_")):
            raise ValueError("Legacy Sora video_id must begin with 'sora_' or 'vid_' prefix.")
        return value

    @field_validator("archived_at")
    @classmethod
    def validate_timestamp(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("archived_at must be a valid ISO 8601 date string.")
        return value

class SoraCatalogSearchRequest(BaseModel):
    query_term: str = Field(..., description="Search keyword to query against archived prompts.")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum number of matched assets to return.")
    min_duration: Optional[int] = Field(None, ge=1, description="Filter clips by minimum duration.")

class SoraCatalogSearchResponse(BaseModel):
    total_matches: int = Field(..., description="Total count of matching historical assets.")
    assets: List[SoraLegacyAsset] = Field(default_factory=list, description="List of matched Sora assets.")
    execution_time_ms: float = Field(..., description="Search query latency in milliseconds.")

# Initialize FastMCP 3.1 server
mcp = FastMCP("sora-archive-catalog-server")

ARCHIVE_METADATA_FILE = "/tmp/sora_archive_catalog.json"

@mcp.tool()
async def search_sora_archive(request: SoraCatalogSearchRequest) -> SoraCatalogSearchResponse:
    """Searches historical Sora video generation archives by prompt keywords using Pydantic v2 schemas."""
    import time
    start_time = time.time()

    if not os.path.exists(ARCHIVE_METADATA_FILE):
        return SoraCatalogSearchResponse(total_matches=0, assets=[], execution_time_ms=0.0)

    with open(ARCHIVE_METADATA_FILE, "r") as f:
        raw_data = json.load(f)

    matched_assets = []
    for item in raw_data.get("assets", []):
        prompt_text = item.get("prompt", "").lower()
        if request.query_term.lower() in prompt_text:
            if request.min_duration and item.get("duration_seconds", 0) < request.min_duration:
                continue
            asset = SoraLegacyAsset(**item)
            matched_assets.append(asset)
            if len(matched_assets) >= request.max_results:
                break

    elapsed_ms = (time.time() - start_time) * 1000.0
    return SoraCatalogSearchResponse(
        total_matches=len(matched_assets),
        assets=matched_assets,
        execution_time_ms=round(elapsed_ms, 2)
    )

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Archival Migration Guide

### 1. Structural Storage Strategy for Historical Visual Assets
When preserving legacy generative media outputs, adhere to the following file hierarchy to ensure seamless FastMCP 3.1 catalog indexing:

```
sora_archive/
├── catalog.json                  # Master Pydantic v2 catalog index
├── video_assets/                 # Raw high-resolution MP4 clips
│   ├── sora_2026_001.mp4
│   └── sora_2026_002.mp4
├── metadata/                     # Per-asset JSON metadata exports
│   ├── sora_2026_001.json
│   └── sora_2026_002.json
└── thumbnails/                   # Fast preview webp extractions
    ├── sora_2026_001.webp
    └── sora_2026_002.webp
```

### 2. Migration Pipeline Execution
To convert raw legacy export dumps into validated Pydantic v2 archives, execute the following Python migration script:

```python
import os
import json
import glob
from pydantic import ValidationError

def migrate_raw_sora_dumps(source_dir: str, target_catalog_file: str):
    valid_assets = []
    errors = []

    for filepath in glob.glob(os.path.join(source_dir, "*.json")):
        with open(filepath, "r") as f:
            try:
                data = json.load(f)
                # Ensure local file reference exists
                mp4_path = filepath.replace(".json", ".mp4")
                if not os.path.exists(mp4_path):
                    errors.append(f"Missing MP4 payload for {filepath}")
                    continue
                data["file_path"] = mp4_path
                asset = SoraLegacyAsset(**data)
                valid_assets.append(asset.model_dump())
            except (json.JSONDecodeError, ValidationError) as e:
                errors.append(f"Validation failed for {filepath}: {e}")

    with open(target_catalog_file, "w") as f:
        json.dump({"assets": valid_assets, "migrated_count": len(valid_assets)}, f, indent=2)

    print(f"Migration complete. Ingested {len(valid_assets)} assets. Encountered {len(errors)} issues.")

if __name__ == "__main__":
    migrate_raw_sora_dumps("/tmp/sora_raw_exports", "/tmp/sora_archive_catalog.json")
```

## Related tools / concepts
- [Runway ML](runwayml.md) — Multimodal AI video generation platform and Gen-3/Gen-4 diffusion engines.
- [Luma Dream Machine](luma-dream-machine.md) — High-speed spatio-temporal video generation model.
- [OpenAI](openai.md) — AI research organization behind GPT-4o, DALL-E 3, and Sora.
- [Project Genie](project-genie.md) — Interactive world generation model for real-time spatial environments.
- [Model Context Protocol (FastMCP 3.1)](../../tools/automation_orchestration/mcp.md) — Standardized tool execution framework.

## Sources / references
- [OpenAI Sora Formal Discontinuation & Sunset Announcement](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation)
- [OpenAI API Deprecation Schedule & Decommission Records](https://developers.openai.com/api/docs/deprecations)
- [OpenAI Sora Technical Paper & Video Patch Architecture](https://openai.com/sora)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
