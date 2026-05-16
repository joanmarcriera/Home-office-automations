# Synthesia

## What it is
Synthesia is an AI video generation platform that enables users to create professional-quality videos with synthetic avatars and voiceovers from plain text. It eliminates the need for cameras, microphones, or film crews, using deep learning to animate realistic human-like avatars that "speak" the provided script in over 140 languages.

## What problem it solves
It drastically reduces the cost and complexity of corporate video production. Traditionally, creating high-quality training or marketing videos requires expensive equipment, actors, and post-production. Synthesia allows organizations to scale video production, update content instantly by editing text, and localize videos for global audiences with minimal effort.

## Where it fits in the stack
**AI & Knowledge / Generative Video Platform**. It serves as a downstream output layer for content generation, transforming text-based insights or instructions into engaging, human-led video content.

## Typical use cases
- **Corporate Training (L&D)**: Building interactive learning modules with a consistent human face.
- **Personalized Sales Outreach**: Generating individual video messages for thousands of leads using API-driven variables.
- **Product Updates**: Creating quick video walkthroughs for new features directly from release notes.
- **Automated News/Briefings**: Transforming daily text summaries into "anchor-led" video segments.

## Key Features
- **AI Avatars**: 160+ ethnically diverse avatars that use neural lip-syncing and natural gestures.
- **Multi-Language Support**: Support for 140+ languages and accents with automated translation.
- **REST API**: Deep integration capabilities for automated video creation at scale.
- **Custom Avatars**: Options to create a digital twin of an actual person for brand consistency.

## Strengths
- **Production Speed**: Minutes from text input to finished video output.
- **Scalability**: Can generate thousands of unique videos simultaneously via the API.
- **Ease of Updates**: Changing a video is as simple as editing the text and clicking "Regenerate."

## Limitations
- **Creative Control**: Limited to the gestures and movements supported by the platform's AI models.
- **"Uncanny Valley"**: While highly realistic, some viewers may still perceive a slight artificiality in extreme close-ups or complex movements.
- **Cost**: Enterprise-scale API usage and custom avatars come with significant subscription costs.

## When to use it
- When you need to produce high volumes of instructional or informational video content.
- For global teams that require instant localization into multiple languages.
- When brand consistency (consistent "face" and "voice") is paramount across all video communications.

## When not to use it
- For high-stakes cinematic or artistic video production requiring complex physical acting.
- When an authentic, non-synthetic human connection is the primary goal (e.g., sensitive high-touch management updates).

## Getting started

### Basic Web Workflow
1.  Log in to the [Synthesia Dashboard](https://app.synthesia.io).
2.  Choose a **Template** or start from a blank script.
3.  Select an **Avatar** and a **Voice**.
4.  Type your **Script** into the text area.
5.  Click **Generate Video** to start the AI processing.

## Technical examples

### Automated Video Generation (Python)
Using the Synthesia REST API (`v1`), you can programmatically trigger video creation from local scripts or agents.

```python
import requests
import json

API_KEY = "YOUR_API_KEY"
URL = "https://api.synthesia.io/v1/videos"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "test": True,  # Use 'True' for testing to avoid consuming credits
    "input": [
        {
            "avatar": "anna_costume1_cameraA",
            "scriptText": "Welcome to our automated homelab update. All systems are currently nominal.",
            "avatarSettings": {
                "horizontalAlign": "center",
                "scale": 1.0
            },
            "background": "green_screen"
        }
    ],
    "title": "Homelab Status Update",
    "description": "Daily automated status report generated via Python agent."
}

response = requests.post(URL, headers=headers, data=json.dumps(payload))
video_id = response.json().get("id")
print(f"Video Generation Started. ID: {video_id}")
```

### Polling for Video Completion (cURL)
After triggering a generation, you must poll the `/v1/videos/{id}` endpoint to check the status.

```bash
# Check status of a specific video
curl -X GET "https://api.synthesia.io/v1/videos/<VIDEO_ID>" \
     -H "Authorization: <YOUR_API_KEY>"

# Expected response (partial)
# {
#   "status": "completed",
#   "download": "https://synthesia-results.s3.amazonaws.com/..."
# }
```

## Related tools / concepts
- [Sora](sora.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [Runway Gen-3](runway.md)
- [HeyGen](heygen.md) (Primary competitor)
- [ElevenLabs](../ai_knowledge/elevenlabs.md) (For high-fidelity voice cloning)
- [n8n](../../services/n8n.md) (For automating video creation triggers)
- [Agentic Video Pipelines](../../knowledge_base/patterns/data-copilot-agentic-rag.md)

## Sources / References
- [Synthesia Official Website](https://www.synthesia.io/)
- [Synthesia API Documentation](https://developers.synthesia.io/)
- [dltHub: Synthesia Python API Docs](https://dlthub.com/context/source/synthesia)

## Contribution Metadata
- Last reviewed: 2026-05-16
- Confidence: high
