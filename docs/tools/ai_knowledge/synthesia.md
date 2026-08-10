# Synthesia

## What it is
Synthesia is a leading AI video generation platform that enables users to create professional-quality videos with synthetic avatars and voiceovers from plain text. By late July 2026, it has expanded its capabilities to support **Real-time Interactive Avatars** via ultra-low-latency API v3 streaming, and seamless script pipelines with frontier models like [Claude](claude.md) and [GPT-5.5](openai.md).

## What problem it solves
It drastically reduces the cost and complexity of corporate video production. Traditionally, creating high-quality training or marketing videos requires expensive equipment, actors, and post-production. Synthesia allows organizations to scale video production, update content instantly by editing text, and localize videos for global audiences in 140+ languages with minimal effort.

## Where it fits in the stack
**AI & Knowledge / Generative Video Platform**. It serves as a downstream output layer for content generation, transforming text-based insights or instructions into engaging, human-led video content. It often integrates with [Dify](dify.md) or [Make.com](../automation_orchestration/make.md) for automated workflows.

## Typical use cases
- **Corporate Training (L&D)**: Building interactive learning modules with a consistent human face and multi-language support.
- **Personalized Sales Outreach**: Generating thousands of individual video messages for leads using API-driven variables.
- **Product Updates**: Creating quick video walkthroughs for new features directly from release notes.
- **Automated News/Briefings**: Transforming daily summary text into "anchor-led" video segments.
- **Interactive Customer Support**: Powering real-time video chatbots that respond with realistic human avatars.

## Strengths
- **Native Lip-Syncing**: High-fidelity neural lip-syncing and natural micro-gestures for 160+ ethnically diverse avatars.
- **Scale**: Ability to generate thousands of personalized videos simultaneously via API.
- **Localization**: Support for 140+ languages and accents with automated translation and cultural adaptation.
- **Interactive Avatars**: Full support for low-latency, real-time video interaction for customer service and education.
- **Frontier Integration**: Easy to pipe scripts from [Claude](claude.md) or [OpenAI](openai.md) directly into the video generation engine.

## Limitations
- **Creative Control**: While highly realistic, avatars are less suitable for high-emotion acting or complex physical actions compared to traditional film.
- **Cost**: Enterprise-tier pricing can be high for large-scale video generation compared to simple text or image generation.
- **Trust & Ethics**: Synthetic media requires clear disclosure and robust safeguards to prevent misuse for deepfakes or misinformation.

## When to use it
- When you need to create consistent, high-quality informational or training videos at scale.
- For global organizations requiring rapid localization of video content into dozens of languages.
- When building interactive video experiences where a human face improves user engagement and trust.

## When not to use it
- For high-budget cinematic productions requiring complex physical acting and emotional depth.
- When a simple screen recording or text document is sufficient for the task.
- If you lack the budget for a premium generative video service and only need occasional, low-fidelity content.

## Getting started

To get started with Synthesia's programmatic platform, you can install the required dependencies and execute a basic HTTP handshake.

### Installation
```bash
# Synthesia APIs are RESTful; install requests for programmatic integration
pip install requests
```

### Hello-World Example
Below is a simple Python verification script to check your API key validity and print the available video models/voices:
```python
import requests

API_KEY = "your_synthesia_api_key"

# Perform a lightweight request to verify integration
headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

try:
    response = requests.get("https://api.synthesia.io/v3/voices", headers=headers, timeout=10)
    if response.status_code == 200:
        print("Connected successfully! Supported voices:", response.json().get("data")[:3])
    else:
        print(f"Connection returned status code: {response.status_code}")
except Exception as e:
    print(f"Connection verification failed: {e}")
```

## CLI examples

While Synthesia is primarily configured in the cloud dashboard, technical teams can utilize their batch CLI tool to deploy or track ongoing video rendering tasks.

```bash
# 1. Retrieve a list of available AI avatar identifiers
synthesia avatars list --api-key "YOUR_KEY"

# 2. Trigger video generation using a script file and target avatar
synthesia video create --script script.txt --avatar anna_costume_1 --output output.mp4

# 3. Poll the render pipeline status for a specific video ID
synthesia video status --id vid_9812304
```

## API examples

### Python (Creating an AI Video)
For backend pipelines, you can easily request a video generation job by sending a POST request to Synthesia's v3 streaming endpoint.

```python
import requests

API_KEY = "YOUR_API_KEY"
API_URL = "https://api.synthesia.io/v3/videos"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

# Video metadata and avatar behavior payload
payload = {
    "test": False,
    "input": [{
        "scriptText": "Welcome to our July 2026 product update!",
        "avatar": "anna_costume_1",
        "avatarSettings": {
            "horizontalAlign": "center",
            "scale": 1.0
        }
    }]
}

try:
    response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
    if response.status_code == 201:
        print("Video rendering initiated. ID:", response.json().get("id"))
    else:
        print(f"API request failed with code {response.status_code}: {response.text}")
except Exception as e:
    print("API connection error:", e)
```

## Related tools / concepts
- [HeyGen](heygen.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [Sora](sora.md)
- [RunwayML](runwayml.md)
- [ElevenLabs](elevenlabs.md)
- [Dify](dify.md)
- [Make.com](../automation_orchestration/make.md)
- [Zapier](../automation_orchestration/zapier.md)
- [Claude](claude.md)
- [GPT-5.5](openai.md)

## Sources / References
- [Official Website](https://www.synthesia.io/)
- [Synthesia API Documentation](https://docs.synthesia.io/)
- [Synthesia Blog: Real-time Interactive Avatars](https://www.synthesia.io/blog/interactive-avatars)
- [Generative Video Market Report 2026](https://www.synthesia.io/reports/2026-video-trends)

## Contribution Metadata
- Last reviewed: 2026-07-27
- Confidence: high
