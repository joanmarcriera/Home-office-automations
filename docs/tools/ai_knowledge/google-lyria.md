# Google Lyria

## What it is
Lyria is Google DeepMind's flagship music generation model family (v3). Designed for high-fidelity generative composition, musical arrangement, and audio editing, it enables creators, sound designers, and developers to synthesize complete multi-track songs, vocal tracks, acoustic arrangements, and stem layers using natural language prompts, musical parameters, and audio conditioning.

Key capabilities as of January 2027 include:
- **Unified Multimodal Music Architecture**: Generates stereophonic, CD-quality 48kHz audio incorporating full instrumental layers, melody, vocal harmonies, and drum patterns in a single pass.
- **Stem-Level Separation & Control**: Isolate or export individual stems (e.g., bassline, lead guitar, vocal track, drums) programmatically during inference.
- **SynthID-Audio Watermarking**: DeepMind SynthID embeds imperceptible, robust digital watermarks into synthesized audio signals for origin verification and copyright compliance.
- **Vertex AI Model Garden & Google Gen AI Integration**: Enterprise-grade REST and Python SDK endpoints supporting low-latency generation, stem extraction, and dynamic track infilling.

## What problem it solves
Traditional music synthesis chains require multiple detached tools (midi generators, soft synths, vocal models, mixing tools), creating mechanical artifacts, phase misalignment, and high latency. Lyria handles melody, harmony, arrangement, and vocal synthesis natively in one diffusion-transformer model. Furthermore, it addresses enterprise licensing and safety requirements via built-in SynthID watermarking.

## Where it fits in the stack
**AI & Knowledge / Generative Audio Layer**. It provides generative music composition, background scoring, and audio stem production within creative platforms and media automation pipelines.

## Typical use cases
- **Interactive Game Audio**: Generating adaptive, dynamic soundtracks that shift genre, tempo, and stem density based on gameplay events.
- **Creative Prototyping**: Rapidly drafting backing tracks, cinematic scores, and promotional jingles for video and podcast creators.
- **Automated Stem Production**: Programmatically isolating drums, vocals, or basslines for remixing and sound design workflows.
- **Brand Audio Identity**: Synthesizing custom, royalty-clear brand soundscapes without copyright infringement risks.

## Strengths
- **Cohesive Arrangement & Structure**: Excels at generating multi-minute arrangements with natural intro-verse-chorus-bridge progressions.
- **Native Stem Export**: Direct model output of individual stem layers simplifies post-production mixing.
- **SynthID Audio Watermarking**: Transparent, verifiable origin tracking for corporate and legal compliance.

## Limitations
- **Gated Access**: Weights are proprietary and served exclusively via Google Cloud Vertex AI and Google AI Studio endpoints.
- **Inference Compute**: High-fidelity stereo rendering at 48kHz requires high GPU/TPU compute allocation for real-time applications.

## When to use it
- When generating complete multi-instrument musical compositions with vocals or stems.
- When building media creation tools integrated into Google Cloud Platform (GCP) or Vertex AI.
- When SynthID audio watermarking is required for corporate compliance.

## When not to use it
- For offline, fully local speech or music generation (use local tools like Stable Audio Open or Kokoro instead).
- For simple speech synthesis without musical elements (use [Gemini 4.0 Flash TTS](gemini-flash-tts.md) instead).

## Getting started

### 1. Installation
Install the Google Cloud AI Platform SDK and Pydantic v2:

```bash
pip install google-cloud-aiplatform pydantic
```

Set your GCP service account credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcp-service-account.json"
```

### 2. Python Generation Quickstart

```python
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI SDK
vertexai.init(project="your-gcp-project-id", location="us-central1")

# Load Lyria v3 music model
model = GenerativeModel("lyria-v3-music")

prompt = "A 15-second ambient synthwave track with warm analog bass, 110 BPM, clear synth lead, cinematic mood."
response = model.generate_content(prompt)

for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open("synthwave_theme.wav", "wb") as f:
            f.write(part.inline_data.data)
        print("Generated music loop written to synthwave_theme.wav")
```

## CLI examples

Request music synthesis via `curl` against Vertex AI:

```bash
export AUTH_TOKEN=$(gcloud auth print-access-token)

curl -X POST \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/us-central1/publishers/google/models/lyria-v3-music:predict \
  -d '{
    "instances": [
      { "prompt": "A warm acoustic guitar ballad with soft strings, 85 BPM, major key" }
    ],
    "parameters": {
      "duration_seconds": 30,
      "tempo_bpm": 85,
      "enable_synthid": true
    }
  }' > lyria_composition.json
```

## API examples

### Structured Pydantic v2 Music Generation Schema & Stem Extractor

```python
import os
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from google.cloud import aiplatform

class MusicGenerationRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    prompt: str = Field(description="Textual music prompt describing genre, instrumentation, and mood")
    duration_seconds: int = Field(default=30, ge=5, le=180, description="Track length in seconds")
    tempo_bpm: int = Field(default=120, ge=40, le=220, description="Beats per minute")
    key_signature: str = Field(default="C-major", description="Musical key")
    export_stems: bool = Field(default=True, description="Whether to return isolated audio stem tracks")
    enable_synthid: bool = Field(default=True, description="Embed SynthID digital watermark")

def generate_lyria_track(req: MusicGenerationRequest, project_id: str):
    aiplatform.init(project=project_id, location="us-central1")

    endpoint = aiplatform.Endpoint(f"projects/{project_id}/locations/us-central1/publishers/google/models/lyria-v3-music")

    payload_parameters = {
        "duration_seconds": req.duration_seconds,
        "tempo_bpm": req.tempo_bpm,
        "key": req.key_signature,
        "export_stems": req.export_stems,
        "watermark_settings": {"enable_synthid": req.enable_synthid}
    }

    response = endpoint.predict(
        instances=[{"prompt": req.prompt}],
        parameters=payload_parameters
    )

    print(f"Generated track response received for key {req.key_signature} at {req.tempo_bpm} BPM.")
    return response

if __name__ == "__main__":
    req = MusicGenerationRequest(
        prompt="Upbeat funk bassline with crisp rhythm guitar and brass stabs",
        duration_seconds=15,
        tempo_bpm=115
    )
    print("Validated Request Schema:")
    print(req.model_dump_json(indent=2))
```

## Related tools / concepts
- [Gemini 4.0 Flash TTS](gemini-flash-tts.md) — Low-latency speech synthesis engine.
- [Gemini](gemini.md) — Unified Google Gemini model family.
- [ElevenLabs](elevenlabs.md) — Voice synthesis and voice cloning model platform.
- [Replicate](../providers/replicate.md) — Cloud API provider for open audio models.

## Sources / references
- [Google DeepMind Lyria Overview](https://deepmind.google/models/lyria/)
- [DeepMind SynthID Watermarking Research](https://deepmind.google/discover/blog/detecting-ai-generated-audio-with-synthid/)
- [Google Cloud Vertex AI Model Garden](https://cloud.google.com/vertex-ai/docs/model-garden/explore-models)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
