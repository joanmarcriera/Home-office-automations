# Google Lyria

## What it is
Lyria is Google's music-generation model family from DeepMind.

## What problem it solves
It gives creators and product teams a model-native way to generate or assist with music creation.

## Where it fits in the stack
**AI & Knowledge / Generative Audio Model**. It belongs in the media-generation layer of the AI landscape.

## Typical use cases
- Music generation experiments
- Creative tooling and soundtrack prototyping
- Exploring multimodal generative product ideas

## Strengths
- Backed by DeepMind's generative media research
- Useful reference point in the music-generation landscape

## Limitations
- Access, productization, and workflow fit may be constrained
- Music-generation tools often have rights and usage questions that must be reviewed carefully

## When to use it
- When evaluating music-generation capabilities in the Google ecosystem

## When not to use it
- When your use case needs a fully open or self-hosted audio stack

## Getting started

### Accessing Lyria
1.  **Google Labs**: Many Lyria-powered experiments (like Dream Track for YouTube Shorts) are rolled out via [Google Labs](https://labs.google/).
2.  **YouTube Creator Tools**: If you are a recognized creator, check your YouTube Studio "Create" options for AI-assisted music generation features.
3.  **Google AI Studio**: Monitor the "Audio" or "Multimodal" model selections in [Google AI Studio](https://aistudio.google.com/) for experimental music generation endpoints as they become available.

### Vertex AI (Enterprise)
To use Lyria via Google Cloud Vertex AI, you need a project with the Vertex AI API enabled.

```bash
# Install the Google Cloud AI Platform SDK
pip install google-cloud-aiplatform
```

```python
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(project="your-project-id", location="us-central1")

# Note: Lyria access is typically gated via Model Garden
# This is a representative example of calling a multimodal audio model
model = GenerativeModel("lyria-002")

response = model.generate_content(
    "A 30-second lofi hip hop beat with mellow piano and slow boom-bap drums."
)

print(response.text)
```

### Replicate (Community API)
If you prefer a simpler REST API, Lyria-3 is available via Replicate.

```bash
pip install replicate
export REPLICATE_API_TOKEN=your_token_here
```

```python
import replicate

output = replicate.run(
    "google/lyria-3",
    input={
        "prompt": "A calm acoustic folk song with gentle guitar and soft strings."
    }
)
print(output.url)
```

## CLI examples
You can trigger Lyria generations via the `gcloud` CLI if you have the appropriate permissions and model access.

```bash
# Print an access token for authentication
export AUTH_TOKEN=$(gcloud auth print-access-token)

# Send a raw prediction request to the Vertex AI endpoint
curl -X POST \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/us-central1/publishers/google/models/lyria-002:predict \
  -d '{
    "instances": [
      { "prompt": "An upbeat 120 BPM pop track with bright acoustic guitar." }
    ]
  }'
```

## API examples
The Vertex AI REST API allows for fine-tuned control over generation parameters.

### Requesting multiple samples
```bash
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/us-central1/publishers/google/models/lyria-002:predict \
  -d '{
    "instances": [{ "prompt": "Dark atmospheric trap beat" }],
    "parameters": { "sample_count": 2 }
  }'
```

### Python SDK with specific parameters
```python
from google.cloud import aiplatform

aiplatform.init(project="your-project-id")

endpoint = aiplatform.Endpoint("your-endpoint-id")
response = endpoint.predict(
    instances=[{"prompt": "Jazzy upright bass line with dusty vinyl crackle"}],
    parameters={"sample_count": 1}
)
print(response.predictions)
```

## Related tools / concepts
- [ElevenLabs](elevenlabs.md)
- [Replicate](../providers/replicate.md)
- [AI Templates](aitmpl.md)
- [Google Gemini](google-gemini.md)
- [Google Opal](google-opal.md)
- [Sora](sora.md)
- [Project Genie](project-genie.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [Synthesia](synthesia.md)
- [Suno](https://suno.com/)
- [Udio](https://www.udio.com/)
- [Stable Audio](https://www.stableaudio.com/)
- [Hydra (by Rightsify)](https://hydra.rightsify.com/)

## Sources / References
- [Official Website](https://deepmind.google/models/lyria/)
- [DeepMind Blog: Lyria](https://deepmind.google/discover/blog/transforming-the-future-of-music-creation/)

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
