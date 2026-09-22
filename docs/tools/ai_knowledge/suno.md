# Suno

## What it is
Suno is a generative AI music creation platform that produces high-fidelity, full-length songs with vocals, instrumentation, lyrics, and arrangements from natural language prompts. It enables creators, sound designers, and developers to generate radio-ready music across diverse genres without requiring traditional music production software or recording hardware.

## What problem it solves
Traditional music composition and recording require specialised instrument proficiency, digital audio workstation (DAW) expertise, and recording equipment. Suno democratises audio creation by allowing users to generate full songs, background tracks, and vocal stems using simple text descriptions, drastically lowering the barrier to custom music production for media and gaming.

## Where it fits in the stack
**AI & Knowledge / Generative Audio Platform**. It sits in the generative media and audio creation layer of the AI stack, alongside voice synthesis platforms like [ElevenLabs](elevenlabs.md) and foundation music models like [Google Lyria](google-lyria.md).

## Typical use cases
- **Content Creation Soundtracks**: Generating custom background music and theme songs for videos, podcasts, and livestreams.
- **Rapid Lyric & Melody Prototyping**: Testing song structures, vocal melodies, and chord progressions before studio recording.
- **Game & Interactive Audio**: Producing dynamic background scores and ambient soundtracks for indie games.
- **Commercial Audio Mockups**: Drafting jingles, promo music, and mood-setting tracks for marketing campaigns.

## Strengths
- **Full Song Composition**: Generates vocals, backing instruments, structural transitions (verses, choruses, bridges), and mastering in a single request.
- **Genre & Style Versatility**: Operates across hundreds of musical genres, vocal styles, and acoustic arrangements.
- **Custom Lyrics Support**: Accepts user-written lyrics or generates lyrics using integrated language models.
- **API & Developer Ecosystem**: Offers API integrations for automated content pipelines and audio workflows.

## Limitations
- **Closed Source Weights**: Proprietary hosted model; model weights cannot be run offline or self-hosted.
- **Multi-Track Isolation**: Stem separation (isolating drums, vocals, bass) requires high-tier platform plans or post-processing tools.
- **Licensing Restrictions**: Commercial use of generated tracks depends on active subscription tier terms.

## When to use it
- When you need full-length, broadcast-quality songs with realistic singing vocals from a text prompt.
- For rapid prototyping of musical ideas and custom soundtracks for digital media.
- When working within cloud-connected workflows where API access is preferred over local execution.

## When not to use it
- When offline, self-hosted, or zero-cost local audio generation is required (use [AudioCPP](audiocpp.md) or open-weights models).
- For pure text-to-speech voiceovers or spoken dialogue (use [ElevenLabs](elevenlabs.md) or [Gemini Flash TTS](gemini-flash-tts.md)).
- When precise MIDI-level note manipulation and DAW track isolation are required.

## Getting started

### Web & API Access
1. Sign up for an account at [suno.com](https://suno.com/).
2. Obtain an API key from the developer settings for programmatic generation.
3. Install standard HTTP client libraries or Python packages for API integration:

```bash
pip install requests pydantic
```

## CLI examples

### Generating a Song via cURL
```bash
# Send song generation request to Suno API
curl -X POST https://api.suno.com/v1/generate \
  -H "Authorization: Bearer $SUNO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "An upbeat 80s synthwave pop track with driving bass, energetic female vocals, and catchy hooks",
    "make_instrumental": false,
    "wait_audio": true
  }'
```

### Checking Generation Job Status
```bash
# Query status of a pending generation task
curl -s -H "Authorization: Bearer $SUNO_API_KEY" \
  https://api.suno.com/v1/tasks/task_98312a7
```

## API examples

### Python (Generation Pipeline with Pydantic v2 Validation)
The following script demonstrates validating song generation parameters with strict **Pydantic v2** schemas before calling the Suno API.

```python
import os
import requests
from typing import Optional
from pydantic import BaseModel, Field, conint

class SunoSongRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="Detailed genre, style, and mood prompt")
    lyrics: Optional[str] = Field(None, description="Custom lyrics for the song")
    instrumental: bool = Field(False, description="Whether to omit vocals")
    title: Optional[str] = Field(None, description="Title for the generated track")

class SunoTaskResponse(BaseModel):
    task_id: str
    status: str
    audio_url: Optional[str] = None

def generate_suno_song(request: SunoSongRequest) -> SunoTaskResponse:
    api_key = os.getenv("SUNO_API_KEY", "dummy_key")
    url = "https://api.suno.com/v1/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": request.prompt,
        "custom_lyrics": request.lyrics,
        "make_instrumental": request.instrumental,
        "title": request.title
    }

    # In production: response = requests.post(url, headers=headers, json=payload)
    # Simulated response payload:
    simulated_payload = {
        "task_id": "suno_task_89123",
        "status": "completed",
        "audio_url": "https://cdn.suno.com/audio/suno_task_89123.mp3"
    }

    return SunoTaskResponse.model_validate(simulated_payload)

if __name__ == "__main__":
    req = SunoSongRequest(
        prompt="A energetic indie rock song with driving guitars and upbeat drums",
        title="Summer Driving",
        instrumental=False
    )
    result = generate_suno_song(req)
    print(f"Song Generation Task ({result.task_id}): Status={result.status}")
    print(f"Audio Download URL: {result.audio_url}")
```

### Async Polling Fragment
```python
import asyncio

async def poll_suno_task(task_id: str, api_key: str):
    while True:
        # Check task endpoint
        await asyncio.sleep(5)
        # Parse status until completed or failed
        break
```

## Related tools / concepts
- [google-lyria](google-lyria.md) — Google DeepMind's generative music model.
- [elevenlabs](elevenlabs.md) — Voice synthesis and audio generation platform.
- [audiocpp](audiocpp.md) — Lightweight C++ audio synthesis framework.
- [gemini-flash-tts](gemini-flash-tts.md) — High-speed text-to-speech voice generation model.
- [sora](sora.md) — Generative video platform needing audio soundtrack pairing.
- [replicate](../providers/replicate.md) — Cloud provider hosting open audio generation models.
- [luma-dream-machine](luma-dream-machine.md) — Visual AI tool frequently combined with Suno soundtracks.

## Sources / references
- [Suno Official Platform](https://suno.com/)
- [Suno Product Documentation](https://suno.com/docs)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
