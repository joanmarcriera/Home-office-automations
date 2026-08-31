# Synthesia

## What it is
Synthesia is a leading AI video generation platform that enables users to create professional-quality videos with synthetic avatars and voiceovers from plain text. By early January 2027, it has expanded its capabilities to support **Real-time Interactive Avatars** via ultra-low-latency API v3 streaming, native **FastMCP 3.1** protocol endpoints, and seamless script pipelines integrated with frontier models like [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), DeepSeek-V4, Qwen 3.6 VL, and [Gemma 4](../ai_knowledge/local_llms.md).

## What problem it solves
It drastically reduces the cost and complexity of corporate video production. Traditionally, creating high-quality training or marketing videos requires expensive equipment, actors, and post-production. Synthesia allows organizations to scale video production, update content instantly by editing text, and localize videos for global audiences in 140+ languages with minimal effort while supporting automated agentic triggers.

## Where it fits in the stack
**AI & Knowledge / Generative Video Platform**. It serves as a downstream output layer for content generation, transforming text-based insights or instructions into engaging, human-led video content. It often integrates with [Dify](dify.md) or [Make.com](../automation_orchestration/make.md) for automated workflows.

## Typical use cases
- **Corporate Training (L&D)**: Building interactive learning modules with a consistent human face and multi-language support.
- **Personalized Sales Outreach**: Generating thousands of individual video messages for leads using API-driven variables.
- **Product Updates**: Creating quick video walkthroughs for new features directly from release notes.
- **Automated News/Briefings**: Transforming daily summary text into "anchor-led" video segments.
- **Interactive Customer Support**: Powering real-time video chatbots that respond with realistic human avatars via FastMCP 3.1.

## Strengths
- **Native Lip-Syncing**: High-fidelity neural lip-syncing and natural micro-gestures for 160+ ethnically diverse avatars.
- **Scale**: Ability to generate thousands of personalized videos simultaneously via API.
- **Localization**: Support for 140+ languages and accents with automated translation and cultural adaptation.
- **Interactive Avatars**: Full support for low-latency, real-time video interaction for customer service and education.
- **Frontier Integration**: Easy to pipe scripts from [Claude 5.6](../ai_knowledge/claude.md) or [GPT-5.6](../ai_knowledge/openai.md) directly into the video generation engine.

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
Programmatic integration with Synthesia API v3 requires installing standard Python request libraries and setting your authorization headers.

### Installation
```bash
pip install requests pydantic>=2.0.0
```

### Verification Script
Below is a simple Python verification script to check your API key validity and inspect active synthetic avatar endpoints:
```python
import requests

API_KEY = "your_synthesia_api_key"

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
Technical teams can utilize Synthesia CLI utilities to deploy or track ongoing video rendering tasks.

```bash
# Retrieve a list of available AI avatar identifiers
synthesia avatars list --api-key "YOUR_KEY"

# Trigger video generation using a script file and target avatar
synthesia video create --script script.txt --avatar anna_costume_1 --output output.mp4

# Poll the render pipeline status for a specific video ID
synthesia video status --id vid_9812304
```

## API examples
### Python: Video Generation with Strict Schema Validation (Pydantic v2)
Enterprise pipelines validate script parameters, voice settings, and layout options using **Pydantic v2** prior to dispatching render jobs.

```python
from pydantic import BaseModel, Field
from typing import List, Optional
import requests

class AvatarSettings(BaseModel):
    horizontal_align: str = Field(default="center", alias="horizontalAlign")
    scale: float = Field(default=1.0, ge=0.5, le=2.0, description="Scale of avatar between 0.5 and 2.0")

class VideoSegment(BaseModel):
    script_text: str = Field(..., alias="scriptText", min_length=10, description="The spoken script text")
    avatar: str = Field(default="anna_costume_1", description="Identifier of the synthetic avatar")
    avatar_settings: AvatarSettings = Field(default_factory=AvatarSettings, alias="avatarSettings")

class SynthesiaVideoRequest(BaseModel):
    test_mode: bool = Field(default=False, alias="test", description="Sandbox test mode flag")
    input_segments: List[VideoSegment] = Field(..., alias="input", description="Ordered list of video segments")

    def dispatch_render_job(self, api_key: str) -> Optional[str]:
        url = "https://api.synthesia.io/v3/videos"
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        payload = self.model_dump(by_alias=True)
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            if response.status_code == 201:
                video_id = response.json().get("id")
                print(f"Synthesia Video rendering initiated! Job ID: {video_id}")
                return video_id
            else:
                print(f"API Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Handshake failed: {e}")
            return None

if __name__ == "__main__":
    mock_payload = {
        "test": True,
        "input": [{
            "scriptText": "Welcome to our 2027 enterprise AI platform rollout with FastMCP 3.1!",
            "avatar": "anna_costume_1",
            "avatarSettings": {
                "horizontalAlign": "center",
                "scale": 1.2
            }
        }]
    }
    validated_request = SynthesiaVideoRequest.model_validate(mock_payload)
    print("Synthesia request schema successfully validated with Pydantic v2:")
    print(validated_request.model_dump_json(by_alias=True, indent=2))
```

## Related tools / concepts
- [HeyGen](heygen.md)
- [Luma Dream Machine](luma-dream-machine.md)
- [ElevenLabs](elevenlabs.md)
- [FastMCP 3.1](../automation_orchestration/mcp.md)
- [Make.com](../automation_orchestration/make.md)
- [Claude](../ai_knowledge/claude.md)
- [OpenAI](openai.md)

## Sources / References
- [Official Website](https://www.synthesia.io/)
- [Synthesia API Documentation](https://docs.synthesia.io/)
- [Synthesia Blog: Real-time Interactive Avatars](https://www.synthesia.io/blog/interactive-avatars)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
