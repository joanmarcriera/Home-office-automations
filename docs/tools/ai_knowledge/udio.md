# Udio

## What it is
Udio is a generative AI music creation platform that synthesizes full-fidelity music tracks with vocals, multi-instrumental arrangements, and custom sound design from text prompts. It provides granular audio controls—including track extensions, inpainting, stem separation, and customizable song structures—for musicians, creators, and audio producers.

## What problem it solves
Creating professional-grade musical compositions requires specialized performance skills, arrangement expertise, and expensive studio equipment. Udio eliminates these barriers by translating natural language descriptions into structured, studio-quality music, enabling rapid audio creation and composition tweaking.

## Where it fits in the stack
**AI & Knowledge / Generative Audio Platform**. It sits in the generative sound synthesis and creative audio layer of the AI stack, alongside platforms like [Suno](suno.md), [Google Lyria](google-lyria.md), and [ElevenLabs](elevenlabs.md).

## Typical use cases
- **Music Production & Extension**: Generating introductory hooks, chorus transitions, or extending existing song stems with AI-generated audio segments.
- **Media Scoring**: Composing tailored cinematic, ambient, or pop soundtracks for podcasts, indie games, and video productions.
- **Vocal & Lyric Experimentation**: Testing vocal harmonies, lyric delivery styles, and genre shifts across synthetic vocal models.
- **Stem Inpainting & Editing**: Replacing specific time sections inside an audio track with new instrumentation or lyrics without regenerating the entire song.

## Strengths
- **Inpainting & Audio Editing**: Precision temporal controls allowing users to rewrite or re-instrument specific sections of a track.
- **Audio Quality & Fidelity**: Known for detailed acoustic separation, wide spatial mix imaging, and realistic vocal expression.
- **Track Extension Mechanics**: Supports adding custom intros, outros, and extended verses seamlessly to existing generations.
- **API & Developer Access**: Offers developer endpoints for integrating automated music generation into external software.

## Limitations
- **Cloud-Only Execution**: Proprietary hosted architecture that cannot be deployed offline or run on local GPUs.
- **Generation Time**: Complex multi-section track generation and rendering can take several seconds to minutes.
- **Copyright & Usage Terms**: Commercial licensing depends on platform subscription tier and usage terms.

## When to use it
- When you require precise control over song structure, track extension, or inpainting specific audio segments.
- For generating high-fidelity music tracks with realistic vocal performances and multi-genre blending.
- When integrating music generation into automated cloud workflows via API.

## When not to use it
- For offline, zero-dependency, or self-hosted audio synthesis on edge devices (use [AudioCPP](audiocpp.md)).
- When generating purely spoken dialogue or voiceovers without musical elements (use [ElevenLabs](elevenlabs.md) or [Gemini Flash TTS](gemini-flash-tts.md)).
- When requiring real-time MIDI parameter manipulation inside a DAW environment.

## Getting started

### Account & API Access
1. Sign up for access on [udio.com](https://www.udio.com/).
2. Obtain an API key from user account integration settings.
3. Install standard HTTP request libraries in Python:

```bash
pip install requests pydantic
```

## CLI examples

### Generating a Track via REST API
```bash
# Trigger a new audio synthesis request
curl -X POST https://api.udio.com/v1/generate \
  -H "Authorization: Bearer $UDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Cinematic orchestral theme with heavy brass, energetic percussion, and epic crescendo",
    "duration": 30
  }'
```

### Inpainting an Existing Track Segment
```bash
# Infill/edit a 5-second window inside a track
curl -X POST https://api.udio.com/v1/inpaint \
  -H "Authorization: Bearer $UDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "track_id": "udio_trk_91234",
    "start_time": 10.0,
    "end_time": 15.0,
    "prompt": "Add a soaring electric guitar solo over the drum rhythm"
  }'
```

## API examples

### Python (Track Generation & Inpainting with Pydantic v2 Validation)
The following code demonstrates defining and validating Udio generation requests using strict **Pydantic v2** schemas before calling the API.

```python
import os
from typing import Optional
from pydantic import BaseModel, Field, conint, confloat

class UdioGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="Detailed music style and instrumentation description")
    duration_seconds: conint(gt=5, le=120) = Field(30, description="Length of generated segment in seconds")
    tempo_bpm: Optional[conint(gt=40, le=240)] = Field(120, description="Target tempo in BPM")

class UdioInpaintRequest(BaseModel):
    track_id: str = Field(..., description="Target Udio track identifier")
    start_sec: confloat(ge=0.0) = Field(..., description="Start timestamp for edit window")
    end_sec: confloat(gt=0.0) = Field(..., description="End timestamp for edit window")
    edit_prompt: str = Field(..., min_length=5, description="New sound or lyrics to introduce")

class UdioResponse(BaseModel):
    track_id: str
    status: str
    audio_url: Optional[str] = None

def trigger_udio_synthesis(request: UdioGenerationRequest) -> UdioResponse:
    # Simulated API integration payload
    simulated_payload = {
        "track_id": "udio_trk_44021",
        "status": "rendering",
        "audio_url": "https://cdn.udio.com/tracks/udio_trk_44021.mp3"
    }
    return UdioResponse.model_validate(simulated_payload)

if __name__ == "__main__":
    req = UdioGenerationRequest(
        prompt="Dreamy lofi hip hop beat with warm rhodes keys and soft vinyl crackle",
        duration_seconds=45,
        tempo_bpm=85
    )
    res = trigger_udio_synthesis(req)
    print(f"Udio Track Created: {res.track_id} (Status={res.status})")
    print(f"Stream URL: {res.audio_url}")
```

### Async Track Inpainting Fragment
```python
import asyncio

async def request_infill(request: UdioInpaintRequest):
    # Perform inpainting API call and poll status
    pass
```

## Related tools / concepts
- [suno](suno.md) — AI music and song generation platform.
- [google-lyria](google-lyria.md) — Google DeepMind's generative music architecture.
- [elevenlabs](elevenlabs.md) — Generative audio and voice synthesis engine.
- [audiocpp](audiocpp.md) — Portable C++ audio synthesis framework.
- [gemini-flash-tts](gemini-flash-tts.md) — High-speed speech synthesis model.
- [sora](sora.md) — Generative video model requiring soundtrack integration.
- [project-genie](project-genie.md) — Generative world model pairing with sound design.

## Sources / references
- [Udio Official Platform](https://www.udio.com/)
- [Udio Product Overview](https://www.udio.com/about)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
