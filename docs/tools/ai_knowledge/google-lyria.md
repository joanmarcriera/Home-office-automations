# Google Lyria

## What it is
Lyria is Google's state-of-the-art music generation model family developed by Google DeepMind. Designed specifically for musical creativity and multimodal audio synthesis, it allows creators, sound designers, and developers to generate, edit, and co-create high-fidelity music tracks with vocals, instrumentation, and complex song structures using natural language and structured parameters.

Key capabilities of the late August 2026 ecosystem include:
- **Unified Multimodal Synthesis**: Generates full stereophonic tracks (including vocals, harmony, melody, and drums) natively from a single unified diffusion-transformer architecture.
- **Instrument-level Stem Control**: Programmatically isolate or steer specific musical layers (e.g., separating guitar chords, drum patterns, and vocals) during generation.
- **DeepMind Watermarking**: Uses SynthID-audio to embed robust, imperceptible digital watermarks directly into generated audio signals to ensure compliance and origin tracking without compromising sound quality.
- **Vertex AI Model Garden Integration**: Scalable enterprise-grade endpoints enabling low-latency inference, custom fine-tuning of instrumental themes, and multi-track orchestration.

## What problem it solves
Traditional music generation pipelines are highly fragmented, requiring separate models for melody, harmony, vocal synthesis, and audio post-processing. Lyria unifies these components into a single end-to-end model, reducing latency and avoiding the mechanical "robotic" phase transitions common in multi-model chains. Additionally, it addresses copyright concerns through deep enterprise compliance integrations.

## Where it fits in the stack
**AI & Knowledge / Generative Audio Model**. It is situated in the generative media and sound engineering layer of the modern AI capability stack.

## Typical use cases
- **Creative Prototyping**: Generating background tracks, cinematic pads, and dynamic acoustic scores for video game developers and video creators.
- **Interactive Audio Environments**: Powering adaptive, real-time gaming soundtracks that change tempo, tone, and instrumentation based on player actions.
- **Vocal Synthesis & Harmonization**: Designing realistic backup vocals or creating scratch vocals in specific synthetic vocal profiles.
- **Sovereign Music Generation**: Building bespoke enterprise brand themes without the licensing risks associated with training on copyrighted databases.

## Strengths
- **Cohesive Song Structure**: Excels at creating multi-minute tracks with logical verse-chorus-verse transitions, bridge build-ups, and natural fade-outs.
- **Native SynthID Watermarking**: Built-in verification mechanisms for corporate accountability and protection.
- **Google Ecosystem Synergy**: Native compatibility with Gemini 3.5 audio-parsing, Google Cloud Vertex AI pipelines, and YouTube Shorts creation frameworks.

## Limitations
- **Access Restrictions**: Direct raw model weights are heavily gated; primary access is restricted to enterprise Vertex AI partners and specific Google Labs channels.
- **Inference Latency for Real-time Synthesis**: While heavily optimized in late 2026, generating 320kbps CD-quality audio still requires substantial GPU compute.

## When to use it
- When creating high-fidelity, complete musical compositions that require synchronized vocals and rich multi-instrument layers.
- For projects operating within the Google Cloud Platform (GCP) or YouTube ecosystem seeking maximum pipeline optimization.
- When SynthID watermark verification is a non-negotiable compliance requirement.

## When not to use it
- If your application requires a fully open-source, offline, or self-hosted audio generation model (use [AudioCPP](../ai_knowledge/audiocpp.md) or Stable Audio Open instead).
- If your focus is purely on text-to-speech voice generation without musical elements (use [Gemini 3.1 Flash TTS](gemini-flash-tts.md)).

## Getting started

### 1. Developer Access and Project Initialization
To programmatically generate audio with Lyria, you must use Google Vertex AI.
1. Enable the **Vertex AI API** inside your Google Cloud Console project.
2. Install the official Google Cloud AI Platform SDK:
   ```bash
   pip install google-cloud-aiplatform
   ```
3. Set your Google Application Credentials:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

### 2. First Audio Generation (Python Quickstart)
Create a script to generate a short musical loop based on natural language steering.

```python
import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# Initialize Vertex AI SDK
vertexai.init(project="your-gcp-project-id", location="us-central1")

# Load the official late 2026 Lyria music model
model = GenerativeModel("lyria-002-music")

prompt = "A 15-second upbeat electronic synthwave loop, heavy analog bassline, 120 BPM, suitable for video game menus."
response = model.generate_content(prompt)

# Retrieve audio bytes from output candidate
for part in response.candidates[0].content.parts:
    if part.inline_data:
        audio_data = part.inline_data.data
        with open("synthwave_loop.wav", "wb") as f:
            f.write(audio_data)
        print("Music loop generated successfully!")
```

## CLI examples
You can trigger Lyria predictions directly using the Google Cloud CLI `gcloud` and `curl`.

### 1. Simple Music Request via REST Endpoints
Ensure your local terminal has authenticated with standard Google Cloud credentials.

```bash
# Print GCP active access token
export AUTH_TOKEN=$(gcloud auth print-access-token)

# Predict a mellow acoustic loop using Lyria model v2
curl -X POST \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/us-central1/publishers/google/models/lyria-002-music:predict \
  -d '{
    "instances": [
      { "prompt": "A warm acoustic guitar ballad with soft violin background" }
    ],
    "parameters": {
      "duration_seconds": 30,
      "tempo_bpm": 85
    }
  }'
```

### 2. Multimodal Prompt (Music Editing via Audio Reference)
Use CLI tools to feed an existing audio track as inspiration alongside editing instructions.

```bash
# Encode a local wav file as base64
export AUDIO_BASE64=$(base64 -w 0 input_melody.wav)

curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/us-central1/publishers/google/models/lyria-002-music:predict \
  -d '{
    "instances": [
      {
        "prompt": "Keep the melody of the provided audio but change the genre to lofi hip hop with dusty vinyl crackle.",
        "audio_reference": {
          "mime_type": "audio/wav",
          "data": "'"$AUDIO_BASE64"'"
        }
      }
    ],
    "parameters": {
      "duration_seconds": 15
    }
  }'
```

## API examples
For complex multi-instrument synthesis and professional rendering pipelines, developers can leverage highly detailed parameter controls via the Python SDK.

### 1. Generating Instrumental Stems (Separate Tracks)
This advanced code block configures specific track parameters, including tempo and separate stem export configurations.

```python
from google.cloud import aiplatform

def generate_multi_track_music(prompt_text: str, project_id: str):
    aiplatform.init(project=project_id, location="us-central1")

    # Configure target endpoint
    endpoint = aiplatform.Endpoint("projects/{}/locations/us-central1/endpoints/lyria-music-endpoint".format(project_id))

    # Configure generation parameters including SynthID settings
    payload = {
        "instances": [{
            "prompt": prompt_text,
        }],
        "parameters": {
            "duration_seconds": 60,
            "tempo_bpm": 110,
            "key": "A-minor",
            "vocal_style": "female_clean",
            "export_stems": True,  # Ask Lyria to return isolated melody, drums, and vocals
            "watermark_settings": {
                "enable_synthid": True,
                "payload_id": 412948
            }
        }
    }

    response = endpoint.predict(
        instances=payload["instances"],
        parameters=payload["parameters"]
    )

    for idx, prediction in enumerate(response.predictions):
        # Extract stems if requested
        if "stems" in prediction:
            for stem_name, stem_base64 in prediction["stems"].items():
                print(f"Discovered stem: {stem_name}")
                # Save each stem natively
```

### 2. Live Music Steerability (Real-time Tempo Infilling)
Edit specific time windows inside a track to accelerate tempo or change instruments.

```python
import requests
import json

def edit_track_infill(project_id: str, track_uri: str, start_sec: float, end_sec: float) -> dict:
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/lyria-002-music:predict"
    headers = {
        "Authorization": f"Bearer {os.getenv('GCP_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }

    data = {
        "instances": [{
            "prompt": "Insert a high-energy guitar solo here",
            "gcs_track_uri": track_uri,
            "infill_window": {
                "start": start_sec,
                "end": end_sec
            }
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
```

## Related tools / concepts
- [ElevenLabs](elevenlabs.md)
- [Replicate](../providers/replicate.md)
- [Google Gemini](google-gemini.md)
- [Gemini 3.1 Flash TTS](gemini-flash-tts.md)
- [Sora](sora.md)
- [Project Genie](project-genie.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [Synthesia](synthesia.md)
- [Suno](https://suno.com/)
- [Udio](https://www.udio.com/)
- [Stable Audio](https://www.stableaudio.com/)
- [AudioCPP](../ai_knowledge/audiocpp.md)

## Sources / references
- [Google DeepMind Lyria Announcement](https://deepmind.google/models/lyria/)
- [DeepMind SynthID Audio Watermarking Details](https://deepmind.google/discover/blog/detecting-ai-generated-audio-with-synthid/)
- [Google Cloud Vertex AI Audio Model Garden](https://cloud.google.com/vertex-ai/docs/model-garden/explore-models)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
