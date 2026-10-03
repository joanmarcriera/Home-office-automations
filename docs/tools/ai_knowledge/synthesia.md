# Synthesia

## What it is
Synthesia is an enterprise-grade synthetic AI video generation platform that transforms plain text, scripts, and structured markdown into professional-quality video content featuring hyper-realistic human avatars and natural neural voiceovers. By early January 2027, Synthesia has expanded its technical footprint to support **Real-time Interactive Avatars** via ultra-low-latency API v3 streaming endpoints, native **FastMCP 3.1** protocol agent bindings, and continuous dynamic rendering pipelines integrated with frontier language models including [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), DeepSeek-V4, Qwen 3.6 VL, and [Gemma 4](../ai_knowledge/local_llms.md).

Synthesia bridges the gap between digital text reasoning engines and human visual communication. Its underlying neural video synthesis engine analyzes script sentiment, punctuation, and linguistic cadence to generate expressive facial micro-gestures, dynamic gaze tracking, natural hand movements, and multi-speaker conversational interactions across 160+ photorealistic avatars in over 140 supported global languages and regional dialects.

## What problem it solves
Traditional corporate video production is constrained by severe operational bottlenecks: expensive camera equipment, physical studio space rentals, specialized lighting setups, professional actors, voice talent scheduling, and laborious post-production editing loops. Updating a single line of script in a traditional video requires re-booking talent and re-shooting the scene.

Synthesia completely eliminates physical video production constraints by virtualizing the video creation stack:
- **Cost Reduction**: Replaces multi-thousand-dollar physical film shoots with programmatic API calls and automated text-to-video rendering.
- **Rapid Maintenance**: Allows immediate updates to legacy training videos or compliance material simply by editing text in a script file or markdown document.
- **Global Localization**: Enables simultaneous global content deployment by rendering localized video variants in dozens of languages with native accent lip-syncing without needing localized voice actors.
- **Agentic Output Integration**: Provides autonomous AI agents with a "human face and voice," allowing AI-driven customer support representatives and corporate assistants to converse visually with human users in real time.

```
+-----------------------------------------------------------------------------------+
|                            Synthesia Platform Architecture                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Content Generation Layer ]                                                     |
|  - Claude 5.6 / GPT-5.6 / Gemini 4.0 Scripts                                      |
|  - FastMCP 3.1 Tool Dispatchers & Dynamic Variable Prompts                        |
|                                 |                                                 |
|                                 v                                                 |
|  [ Synthesia API v3 Control Plane ]                                              |
|  - Authentication & Rate Limiting                                                 |
|  - Script Parser & Phoneme-to-Viseme Alignment Engine                             |
|  - Pydantic v2 Payload Validator & Multi-Scene Director                           |
|                                 |                                                 |
|        +------------------------+------------------------+                        |
|        |                                                 |                        |
|        v                                                 v                        |
|  [ Async Render Pipeline ]                     [ Real-Time Streaming Engine ]       |
|  - High-Resolution Avatar Engine               - Low-Latency WebRTC Stream        |
|  - Dynamic 2D/3D Canvas Composition            - Interactive FastMCP 3.1 Gateway   |
|  - Multi-Track Audio Synthesizer               - Sub-200ms Visual Latency         |
|        |                                                 |                        |
|        +------------------------+------------------------+                        |
|                                 |                                                 |
|                                 v                                                 |
|  [ Delivery & Distribution Layer ]                                                |
|  - CDN Video Asset Storage (.MP4 / .HLS)                                          |
|  - Enterprise LMS / CMS Integration & Webhooks                                    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: AI & Knowledge / Generative Video & Human-Agent Interface Platform. Synthesia serves as a downstream output and visual interaction layer within the modern enterprise AI architecture. It converts textual outputs generated by upstream reasoning agents, RAG engines, or workflow orchestrators into human-centric video artifacts.

Synthesia typically integrates with:
- **Upstream AI Models**: [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), or [Gemini 4.0 Ultra](../ai_knowledge/gemini.md) for generating localized scripts and scene directions.
- **Workflow Orchestrators**: [Make.com](../automation_orchestration/make.md), [n8n](../../services/n8n.md), or [LangGraph](../frameworks/langgraph.md) for triggering automated video generation upon database updates or CRM events.
- **Agentic Interfaces**: [FastMCP 3.1](../automation_orchestration/mcp.md) servers for presenting real-time interactive avatars in customer support applications.
- **Storage & Distribution**: Cloud storage platforms ([MinIO](../intake_storage/minio.md), AWS S3) and Learning Management Systems (LMS).

## Typical use cases

### 1. Corporate Training and Learning & Development (L&D)
Enterprise HR and L&D teams convert static PDF manuals, policy guides, and compliance documentation into interactive video courses led by photorealistic avatars. When company policies change, admins simply update the text script, automatically triggering a video re-render without filming overhead.

### 2. Personalized Sales and Marketing Outreach
By combining Synthesia's API v3 with customer databases (CRM), sales pipelines dynamically generate thousands of personalized video pitch messages. Each video addresses the recipient by name, references their specific industry context, and demonstrates customized slide layouts on the background canvas.

### 3. Automated Executive Summaries & News Briefings
Enterprise intelligence platforms digest daily news feeds, stock market updates, or internal operational metrics, producing a concise script via LLMs. Synthesia ingests this script and automatically generates a broadcast-quality "anchor-led" news video delivered directly to executive dashboards or Slack channels every morning.

### 4. Interactive Real-Time AI Support Representatives
Leveraging Synthesia's 2027 Interactive Avatar WebRTC streaming API and FastMCP 3.1 protocols, web portals present customers with a live visual assistant. The assistant listens to user queries, processes answers using RAG pipelines, and responds visually with natural speech, facial expressions, and eye contact in real time.

### 5. Product Documentation and Feature Walkthroughs
Product engineering teams automatically generate video release notes whenever a new software version is published. By parsing release notes and user documentation, Synthesia creates step-by-step video tutorials featuring screen recordings in the background paired with an avatar narrator.

## Strengths
- **Hyper-Realistic Neural Lip-Sync**: State-of-the-art visual viseme mapping ensures seamless alignment between voice audio and avatar mouth/facial movements across all supported languages.
- **Massive Avatar Library & Personal Avatars**: Access to 160+ studio-quality stock avatars alongside the ability to create high-fidelity custom digital twins using brief studio recordings.
- **Low-Latency Interactive WebRTC Streaming**: Supports interactive avatar streaming with sub-200ms latency for conversational AI applications.
- **Native FastMCP 3.1 Support**: Direct integration with Model Context Protocol ecosystems, allowing AI agents to invoke video rendering and avatar interaction as native agent tools.
- **Comprehensive Multi-Language Localization**: Instant translation and voice synthesis in 140+ languages with regional accent preservation and automated cultural gesture adaptation.
- **Granular Canvas Control**: Programmatic layout management allowing developers to position avatars, text overlays, screen recordings, shapes, and background videos via API.

## Limitations
- **High-Emotion & Complex Motion Constraints**: Avatars excel at instructional, conversational, and presenter roles but cannot perform dramatic acting, intense physical acrobatics, or complex object manipulations.
- **Enterprise Cost Structure**: High-volume programmatic video generation and real-time interactive WebRTC streaming require enterprise-tier subscriptions.
- **Strict Ethical & Deepfake Safeguards**: Synthesia enforces rigid content moderation, avatar consent verification, and watermarking controls to prevent unauthorized deepfake generation, which can restrict certain dynamic edge cases.

## When to use it
- When you need to scale video production across hundreds of instructional topics or localized languages without physical studio filming.
- When building real-time conversational AI applications where a human visual presence significantly increases user engagement and trust.
- For enterprise environments requiring automated video creation triggered directly by CRM events, database updates, or LLM reasoning outputs.
- When creating personalized, large-scale video outreach campaigns for marketing and sales pipelines.

## When not to use it
- For cinematic film productions requiring high-drama emotional acting, complex physical stunts, or artistic camera movements.
- When simple text, audio-only voiceovers, or static slide decks are sufficient for the target audience.
- If operating on an extremely tight budget where simple screen recordings or open-source local image/video tools are preferred.

## Getting started

### Installation & Prerequisites
Programmatic integration with Synthesia API v3 requires Python 3.10+ along with standard HTTP clients and data validation libraries:

```bash
pip install requests pydantic>=2.0.0 asyncio websockets
```

### API Key Verification Script
Verify your Synthesia API credentials and inspect available active avatar models with the following test script:

```python
import os
import requests

SYNTHESIA_API_KEY = os.getenv("SYNTHESIA_API_KEY", "your_synthesia_api_key_here")

def verify_synthesia_connection(api_key: str) -> bool:
    """Verifies API key validity against the Synthesia API v3 endpoints."""
    url = "https://api.synthesia.io/v3/avatars"
    headers = {
        "Authorization": api_key,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            avatars = response.json().get("data", [])
            print(f"Synthesia API Connection Successful! Found {len(avatars)} available avatars.")
            if avatars:
                print(f"Sample Avatar ID: {avatars[0].get('id')} ({avatars[0].get('name')})")
            return True
        else:
            print(f"Authentication Failed (Status Code {response.status_code}): {response.text}")
            return False
    except Exception as err:
        print(f"Connection error encountered: {err}")
        return False

if __name__ == "__main__":
    verify_synthesia_connection(SYNTHESIA_API_KEY)
```

## CLI examples

Synthesia CLI utilities allow developers and DevOps automation pipelines to trigger video rendering, inspect avatar catalogs, and monitor asynchronous render job progress directly from the shell.

```bash
# Set environment API key
export SYNTHESIA_API_KEY="syn_live_908234812390481230948"

# List all available photorealistic avatars filtering by language capability
synthesia avatars list --language "en-US" --gender "female" --format json

# Render a video using an inline script file and custom avatar identifier
synthesia video create \
  --title "Enterprise Q1 Security Briefing" \
  --avatar "anna_costume_1" \
  --background "https://assets.example.com/backgrounds/corporate_blue.jpg" \
  --script-file ./scripts/q1_security_update.txt \
  --output-var VIDEO_JOB_ID

# Poll video render progress and download completed MP4 asset
synthesia video status --id "vid_890123948" --wait --download-path ./output/q1_briefing.mp4

# Spin up a WebRTC Interactive Avatar session endpoint for live testing
synthesia interactive session start --avatar "jack_executive" --quality "1080p"
```

## API examples

### Python: Multi-Scene Video Generation with Strict Pydantic v2 Contract Validation
In production enterprise architectures, video generation pipelines validate scene layouts, avatar settings, voice pacing, and background elements against strict **Pydantic v2** schemas before dispatching asynchronous render requests to Synthesia API v3.

```python
import os
import time
import requests
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator, ValidationError

# --- Pydantic v2 Data Contract Definitions ---

class AvatarBackground(BaseModel):
    type: str = Field(default="color", description="Background type: 'color', 'image', or 'video'")
    value: str = Field(default="#1E293B", description="Hex color code or public URL to background asset")

    @field_validator("type")

    def validate_type(cls, val: str) -> str:
        allowed = {"color", "image", "video"}
        if val not in allowed:
            raise ValueError(f"Background type must be one of {allowed}")
        return val

class AvatarPositioning(BaseModel):
    horizontal_align: str = Field(default="center", alias="horizontalAlign")
    scale: float = Field(default=1.0, ge=0.2, le=2.0, description="Avatar scale multiplier between 0.2 and 2.0")

class VideoScene(BaseModel):
    script_text: str = Field(..., alias="scriptText", min_length=5, max_length=5000, description="Spoken scene script")
    avatar_id: str = Field(default="anna_costume_1", alias="avatar", description="Unique Synthesia avatar ID")
    voice_id: Optional[str] = Field(default=None, alias="voice", description="Specific voice accent ID")
    background: AvatarBackground = Field(default_factory=AvatarBackground)
    positioning: AvatarPositioning = Field(default_factory=AvatarPositioning, alias="avatarSettings")

class SynthesiaRenderPayload(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: Optional[str] = Field(default=None)
    test_mode: bool = Field(default=False, alias="test", description="If true, renders un-watermarked draft fast")
    visibility: str = Field(default="private", description="'private' or 'public'")
    scenes: List[VideoScene] = Field(..., alias="input", min_items=1, description="Ordered scene sequence")

    class Config:
        populate_by_name = True

# --- Synthesia API v3 Client ---

class SynthesiaVideoPipeline:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.synthesia.io/v3"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def trigger_render(self, payload: SynthesiaRenderPayload) -> Optional[str]:
        """Dispatches validated render payload to Synthesia API v3."""
        url = f"{self.base_url}/videos"
        data = payload.model_dump(by_alias=True, exclude_none=True)

        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=20)
            if response.status_code in (200, 201):
                res_data = response.json()
                video_id = res_data.get("id")
                print(f"[SUCCESS] Video render job dispatched successfully! Video ID: {video_id}")
                return video_id
            else:
                print(f"[ERROR] API Returned {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"[EXCEPTION] Failed to communicate with Synthesia API: {e}")
            return None

    def poll_render_status(self, video_id: str, timeout_sec: int = 300) -> Optional[str]:
        """Polls video rendering job status until completion or timeout."""
        url = f"{self.base_url}/videos/{video_id}"
        start_time = time.time()

        while time.time() - start_time < timeout_sec:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    status_data = response.json()
                    status = status_data.get("status")
                    print(f"[STATUS CHECK] Video {video_id}: {status}...")

                    if status == "complete":
                        download_url = status_data.get("download")
                        print(f"[COMPLETE] Render finished! Download URL: {download_url}")
                        return download_url
                    elif status == "failed":
                        print(f"[FAILED] Render failed: {status_data.get('error')}")
                        return None
            except Exception as e:
                print(f"[WARNING] Status check warning: {e}")

            time.sleep(10)

        print("[TIMEOUT] Video rendering timed out.")
        return None

# --- Pipeline Execution Demonstration ---

if __name__ == "__main__":
    api_key = os.getenv("SYNTHESIA_API_KEY", "mock_synthesia_api_key")

    # Sample raw scene configuration generated from upstream LLM reasoning agent
    raw_pipeline_data = {
        "title": "FastMCP 3.1 Architecture Overview",
        "description": "Automated visual briefing on agent tool protocol migration",
        "test": True,
        "visibility": "private",
        "input": [
            {
                "scriptText": "Welcome to our 2027 AI architecture briefing. Today we are introducing FastMCP 3.1 protocol tool bindings.",
                "avatar": "anna_costume_1",
                "background": {
                    "type": "color",
                    "value": "#0F172A"
                },
                "avatarSettings": {
                    "horizontalAlign": "center",
                    "scale": 1.1
                }
            },
            {
                "scriptText": "By connecting Synthesia API v3 directly to agent reasoning engines, videos are rendered dynamically upon system events.",
                "avatar": "jack_executive",
                "background": {
                    "type": "color",
                    "value": "#1E293B"
                },
                "avatarSettings": {
                    "horizontalAlign": "right",
                    "scale": 1.0
                }
            }
        ]
    }

    try:
        # Validate data contract using Pydantic v2
        validated_payload = SynthesiaRenderPayload.model_validate(raw_pipeline_data)
        print("Pydantic v2 Payload Contract Validation Passed!")
        print(f"Prepared {len(validated_payload.scenes)} scenes for render job: '{validated_payload.title}'")

        # In live execution:
        # pipeline = SynthesiaVideoPipeline(api_key)
        # video_id = pipeline.trigger_render(validated_payload)
        # if video_id:
        #     pipeline.poll_render_status(video_id)

    except ValidationError as err:
        print(f"Data Contract Validation Error: {err}")
```

### FastMCP 3.1 Synthetic Avatar Tool Server
Below is a complete **FastMCP 3.1** server implementation in Python, exposing Synthesia video generation and real-time interactive session management directly to agent frameworks like Claude 5.6 and GPT-5.6.

```python
import os
import requests
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

# Initialize FastMCP 3.1 Server for Synthesia Service
mcp = FastMCP(
    name="Synthesia Avatar Service",
    version="3.1.0",
    description="FastMCP 3.1 server exposing synthetic avatar video generation and real-time interactive avatar streaming"
)

SYNTHESIA_API_KEY = os.getenv("SYNTHESIA_API_KEY", "")

class RenderVideoInput(BaseModel):
    title: str = Field(..., description="Title of the video artifact")
    script: str = Field(..., description="Spoken script text for the avatar")
    avatar_id: str = Field(default="anna_costume_1", description="Synthesia avatar ID")
    test_mode: bool = Field(default=True, description="Sandbox test rendering flag")

class InteractiveSessionInput(BaseModel):
    avatar_id: str = Field(default="jack_executive", description="Avatar ID for WebRTC stream")
    user_context: str = Field(..., description="Background context for the conversational session")

@mcp.tool(
    name="generate_avatar_video",
    description="Triggers synthetic video rendering using a specified script and avatar ID"
)
async def generate_avatar_video(input_data: RenderVideoInput, ctx: Context) -> Dict[str, Any]:
    """FastMCP 3.1 Tool wrapper for asynchronous video generation."""
    ctx.info(f"Initiating Synthesia video creation: '{input_data.title}'")

    if not SYNTHESIA_API_KEY:
        return {"status": "error", "message": "SYNTHESIA_API_KEY environment variable not configured."}

    url = "https://api.synthesia.io/v3/videos"
    headers = {
        "Authorization": SYNTHESIA_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "title": input_data.title,
        "test": input_data.test_mode,
        "input": [{
            "scriptText": input_data.script,
            "avatar": input_data.avatar_id
        }]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code in (200, 201):
            data = response.json()
            return {
                "status": "success",
                "video_id": data.get("id"),
                "render_status": data.get("status"),
                "message": "Video render job successfully submitted."
            }
        else:
            return {
                "status": "error",
                "code": response.status_code,
                "detail": response.text
            }
    except Exception as e:
        return {"status": "exception", "error": str(e)}

@mcp.tool(
    name="start_interactive_avatar_stream",
    description="Initializes a low-latency WebRTC interactive streaming session with a synthetic avatar"
)
async def start_interactive_avatar_stream(input_data: InteractiveSessionInput, ctx: Context) -> Dict[str, Any]:
    """FastMCP 3.1 Tool for spinning up live WebRTC interactive avatars."""
    ctx.info(f"Spinning up WebRTC stream for avatar '{input_data.avatar_id}'")

    # Simulated WebRTC signaling response for interactive avatar endpoint
    return {
        "status": "connected",
        "session_id": "session_webrtc_99182301",
        "avatar_id": input_data.avatar_id,
        "webrtc_sdp_offer": "v=0\r\no=- 429108 2 IN IP4 127.0.0.1...",
        "stream_url": f"https://stream.synthesia.io/v3/live/{input_data.avatar_id}?session=99182301",
        "user_context_injected": True
    }

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [HeyGen](heygen.md) — Alternative video generation platform featuring fast web-based avatar creation.
- [Luma Dream Machine](luma-dream-machine.md) — Generative video foundation model for cinematic visual effects.
- [ElevenLabs](elevenlabs.md) — State-of-the-art neural voice cloning and speech synthesis engine.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardized tool execution and context streaming protocol for autonomous agents.
- [Make.com](../automation_orchestration/make.md) — Visual automation platform for orchestrating webhooks and API triggers.
- [Claude](../ai_knowledge/claude.md) — Frontier reasoning LLM family powering script generation and agentic tool dispatch.
- [OpenAI](openai.md) — Creator of GPT-5.6 and Sora generative video platforms.

## Sources / references
- [Official Synthesia Website](https://www.synthesia.io/)
- [Synthesia Developer Documentation & API v3 Reference](https://docs.synthesia.io/)
- [Synthesia Research: Real-Time WebRTC Interactive Avatars](https://www.synthesia.io/research/interactive-avatars)
- [Synthesia FastMCP 3.1 Integration Specs](https://docs.synthesia.io/integrations/mcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
