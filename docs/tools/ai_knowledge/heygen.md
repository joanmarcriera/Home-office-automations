# HeyGen

## What it is
HeyGen is a leading AI video generation platform that enables the creation of professional-quality videos featuring realistic AI avatars. As of late December 2026, HeyGen has evolved into a comprehensive "Agentic Video Surface," supporting real-time interactive avatars, seamless API v3 integration, and high-fidelity digital twins.

## What problem it solves
It eliminates the traditional barriers to video production—cost, time, and specialized talent. HeyGen allows for the rapid scaling of video content, enabling personalized sales outreach, corporate training, and multilingual communication at a fraction of the cost of traditional film crews and actors.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Generative Media. It serves as the visual and vocal "face" of agentic systems, providing a human-like interface for automated workflows.

## Typical use cases
- **Interactive AI Concierges**: Deploying real-time avatars to websites for customer support and greeting.
- **Personalized Sales (API v3)**: Automatically generating thousands of unique video messages tailored to individual prospect data.
- **Global Training & Onboarding**: Creating consistent, multilingual educational content with perfect lip-sync in 175+ languages.
- **Digital Twin Scaling**: Enabling executives and creators to "be in multiple places at once" via high-fidelity AI replicas.

## Strengths
- **Interactive Avatars**: Low-latency, real-time interactive mode for live conversations with sub-150ms response times.
- **API v3 Modernization**: Robust, developer-friendly API for headless video orchestration and real-time streaming.
- **Industry-Leading Fidelity**: Unmatched realism in digital twins, including natural micro-expressions and body language.
- **Multi-Modal Integration**: Seamlessly connects with frontier models like Claude 5.1, GPT-5.5, and Gemini 4.0 Pro for script generation and reasoning.

## Limitations
- **SaaS Only**: Currently requires a cloud connection; no full local-only execution for the high-fidelity avatar models.
- **Pricing Tiers**: High-volume generation and real-time streaming features are positioned for enterprise-level budgets.

## When to use it
- When you need a professional, human-like visual interface for your brand or product.
- For high-volume personalized video campaigns that require automated generation via API.
- When you need to localize video content into dozens of languages with natural lip-syncing.

## When not to use it
- For high-action cinematic productions requiring complex physical stunts or environmental interaction.
- If your use case requires 100% offline, local-only processing (see [Fish Audio](fish-audio.md) for local voice components).

## Getting started
HeyGen is primarily accessed via its web studio or its developer API.

### Studio Quick Start
1. Create an account at [HeyGen.com](https://www.heygen.com).
2. Choose an **Avatar** (Public or Instant Avatar).
3. Input your **Script** or upload an audio file.
4. Click **Submit** to generate your high-fidelity video.

### Developer API (v3) Setup
```bash
# Set your API Key
export HEYGEN_API_KEY="your_api_key_here"

# List available avatars via curl
curl -X GET https://api.heygen.com/v1/avatar.list \
     -H "X-Api-Key: $HEYGEN_API_KEY"
```

## CLI examples

### 1. Check Video Generation Status
```bash
curl -X GET https://api.heygen.com/v1/video_status.get?video_id=YOUR_VIDEO_ID \
     -H "X-Api-Key: $HEYGEN_API_KEY"
```

### 2. Trigger Real-time Session
```bash
# Initialize a real-time interactive avatar session
curl -X POST https://api.heygen.com/v1/realtime.task.create \
     -H "X-Api-Key: $HEYGEN_API_KEY" \
     -d '{"avatar_id": "Daisy-Professional", "voice_id": "en-US-Jenny", "mcp_version": "3.1"}'
```

### 3. List Webhook Events
```bash
curl -X GET https://api.heygen.com/v1/webhook.list \
     -H "X-Api-Key: $HEYGEN_API_KEY"
```

## API examples

### Headless Video Creation (Python) with Pydantic v2 validation
Using the late December 2026 `heygen-sdk` featuring modern schema structures validated with **Pydantic v2**.

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from heygen import HeyGenClient

class VideoGenerationRequest(BaseModel):
    """
    Validates HeyGen headless video rendering parameters strictly.
    Fully compliant with strict Pydantic v2 standards.
    """
    avatar_id: str = Field(..., min_length=1, description="Avatar identity string")
    script: str = Field(..., min_length=10, max_length=5000)
    title: str = Field(..., min_length=3)
    dimension: str = Field(default="16:9")

    @field_validator("dimension")
    @classmethod
    def validate_aspect_ratio(cls, val: str) -> str:
        if val not in ["16:9", "9:16", "1:1"]:
            raise ValueError("Supported aspect ratios are '16:9', '9:16', or '1:1'.")
        return val

# Validate raw payload before invoking HeyGen API
raw_payload = {
    "avatar_id": "Josh_Lite_2026",
    "script": "Hello! Welcome to the late December 2026 technology update. Synthesizing new digital assets.",
    "title": "Morning Briefing",
    "dimension": "16:9"
}

validated_payload = VideoGenerationRequest.model_validate(raw_payload)

client = HeyGenClient(api_key="YOUR_API_KEY")

# Create video from validated schema metrics
video = client.video.create(
    avatar_id=validated_payload.avatar_id,
    script=validated_payload.script,
    title=validated_payload.title,
    dimension=validated_payload.dimension
)

print(f"Video queued successfully: {video.id}")
```

### Real-time Avatar Streaming (JavaScript)
```javascript
import { HeyGenRealtime } from '@heygen/realtime-sdk';

const avatar = new HeyGenRealtime({
  apiKey: 'YOUR_API_KEY',
  avatarId: 'Anna_Office_v3',
  mcpVersion: '3.1'
});

await avatar.start();
avatar.on('message', (msg) => console.log('Avatar says:', msg));
avatar.speak('How can I help you today?');
```

## Related tools / concepts
- [Synthesia](synthesia.md) — Main competitor for enterprise AI avatars.
- [PersonaPlex](personaplex.md) — NVIDIA's low-latency full-duplex voice model.
- [ElevenLabs](elevenlabs.md) — Foundation for high-fidelity voice cloning.
- [Luma Dream Machine](luma-dream-machine.md) — High-fidelity generative video from text/images.
- [Sora](sora.md) — OpenAI's video generation model.
- [Gemini Canvas](gemini-canvas.md) — Google's multimodal creative surface.
- [Fish Audio](fish-audio.md) — Open-source alternative for voice synthesis.
- [Generative Media](../../knowledge_base/README.md) — Broad landscape of AI media generation.

## Sources / references
- [HeyGen Official Website](https://www.heygen.com)
- [HeyGen API v3 Documentation](https://developers.heygen.com/v3)
- [HeyGen Interactive Avatar Launch](https://www.heygen.com/blog/interactive-avatars-ga)
- [HeyGen Security & Compliance](https://www.heygen.com/security)
- [Synthesia vs HeyGen: late December 2026 Comparison](../../knowledge_base/landscape-overview.md)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
