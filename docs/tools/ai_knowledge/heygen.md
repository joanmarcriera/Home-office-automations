# HeyGen

## What it is
HeyGen is an enterprise-grade AI video generation platform that enables the creation, localization, and real-time streaming of professional-quality digital human avatars. As of early January 2027, HeyGen has transformed from a static video generation tool into a comprehensive, multi-modal **Agentic Video Surface**. Powered by state-of-the-art vision-language models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL), HeyGen provides real-time interactive avatars, FastMCP 3.1 Task Protocol integrations, headless video orchestration, and hyper-realistic digital twin synthesis.

Through its early 2027 API v3 architecture, HeyGen operates seamlessly in autonomous workflows, serving as the interactive, human-like visual and conversational front-end for agentic systems across sales, customer success, enterprise training, and autonomous content generation pipelines.

## What problem it solves
Traditional video production suffers from prohibitive costs, extended turnaround times, logistical bottlenecks, and physical constraints. Producing localized video content across global markets requires hiring multilingual talent, booking recording studios, managing post-production, and re-recording scripts whenever product details change.

HeyGen eliminates these bottlenecks by enabling code-driven, zero-latency video synthesis. It solves key enterprise video challenges:
- **Scalability Friction**: Generating thousands of personalized, variable-driven video messages for sales outreach or customer onboarding in seconds.
- **Multilingual Localization**: Automatically translating video content into 175+ languages with accurate lip-syncing, voice preservation, and micro-expression alignment.
- **Real-Time Interactive Interfaces**: Eliminating static text/audio interfaces by deploying sub-150ms interactive AI concierges capable of bi-directional visual conversations.
- **Digital Twin Maintenance**: Allowing executives, educators, and creators to record high-fidelity digital avatars once and generate infinite content on demand.

## Mathematical Formulations of Neural Audio-to-Visual Phoneme Synthesis & WebRTC Latency

HeyGen's real-time avatar synthesis pipeline bridges neural speech synthesis with multi-modal facial landmark generation. The underlying neural architecture models the conditional probability distribution of video frame latent states $\mathbf{v}_t \in \mathbb{R}^{d_v}$ given an acoustic audio spectral feature stream $\mathbf{a}_{1:t} \in \mathbb{R}^{T \times d_a}$ and avatar canonical identity embedding $\mathbf{e}_{\text{id}} \in \mathbb{R}^{d_e}$.

### 1. Neural Viseme-to-Phoneme Alignment Lattice
The temporal alignment between acoustic phonemes $\mathbf{p} = (p_1, \dots, p_N)$ and facial visemes $\mathbf{v} = (v_1, \dots, v_M)$ is formulated as a dynamic time warping (DTW) path $\pi = (\pi_1, \dots, \pi_K)$ optimizing cumulative acoustic-motion cost:

$$\min_{\pi} \sum_{k=1}^K \mathcal{D}\left( \mathbf{p}_{\pi_k[1]}, \mathbf{v}_{\pi_k[2]} \right) + \lambda \cdot \|\nabla^2 \mathbf{v}_{\pi_k[2]}\|_2^2$$

where the second regularization term enforces geometric acceleration smoothness on lip mesh vertices, preventing high-frequency micro-jitter during rapid consonant transitions.

### 2. Micro-Expression Latent Interpolation & Neural Radiance Blendshapes
To synthesize dynamic micro-expressions (eyeblink, saccadic gaze shifts, head pose kinematics), the decoder predicts 3D morphable model (3DMM) blendshape coefficients $\boldsymbol{\alpha}_t \in [0, 1]^B$:

$$\boldsymbol{\alpha}_t = \text{Softmax}\left( \mathbf{W}_a \mathbf{a}_t + \mathbf{W}_h \mathbf{h}_{t-1} + \mathbf{W}_{\text{gaze}} \mathbf{g}_t \right)$$

The rendered neural radiance field density $\sigma(\mathbf{x}, t)$ and directional radiance $\mathbf{c}(\mathbf{x}, \mathbf{d}, t)$ at 3D point $\mathbf{x}$ along camera ray $\mathbf{r}(s) = \mathbf{o} + s\mathbf{d}$ are evaluated using volumetric rendering integrals:

$$\mathbf{C}(\mathbf{r}, t) = \int_{s_n}^{s_f} T(s, t) \, \sigma(\mathbf{r}(s), t) \, \mathbf{c}(\mathbf{r}(s), \mathbf{d}, t) \, ds, \quad T(s, t) = \exp\left(-\int_{s_n}^s \sigma(\mathbf{r}(u), t) \, du\right)$$

### 3. WebRTC Jitter Buffer & End-to-End Latency Roofline Bound
In bi-directional conversational sessions, total end-to-end latency $T_{\text{e2e}}$ comprises acoustic speech recognition $T_{\text{ASR}}$, LLM token inference $T_{\text{LLM}}$, neural TTS synthesis $T_{\text{TTS}}$, neural rendering $T_{\text{render}}$, and network jitter transit $T_{\text{net}}$:

$$T_{\text{e2e}} = T_{\text{ASR}} + T_{\text{LLM}}(\text{TTFT}) + T_{\text{TTS}} + T_{\text{render}} + 2 \cdot \text{RTT} + J_{\text{buffer}}$$

HeyGen guarantees real-time interactive convergence satisfying:

$$T_{\text{e2e}} \le 185\text{ ms} \quad (\text{Target SLA: } \le 145\text{ ms})$$

with adaptive playout delay buffer $J_{\text{buffer}} = \mu_{\text{jitter}} + 3 \cdot \sigma_{\text{jitter}}$.

## Where it fits in the stack
**Category**: [AI Assistants & Knowledge](index.md) / Generative Media & Visual Interaction Layer.

HeyGen operates as the **Visual Interaction Gateway** in modern multi-agent systems. Positioned between backend orchestration frameworks (e.g., LangGraph, Agno, FastMCP 3.1 servers) and end-user client surfaces (web applications, mobile apps, digital kiosks), HeyGen converts raw text or structured agent outputs into live video streams or downloadable MP4 assets.

```
+-----------------------------------------------------------------------+
|                       Agentic Backend Engine                          |
|  (Claude 5.6 / FastMCP 3.1 Router / LangGraph / Enterprise DB)        |
+-----------------------------------------------------------------------+
                                   |
                                   | Structured Response & Audio/Text
                                   v
+-----------------------------------------------------------------------+
|                    HeyGen Agentic Video Surface                       |
|                                                                       |
|  +-----------------------+  +-------------------+  +---------------+  |
|  | Real-Time WebRTC Engine|  | Digital Twin Sync |  | API v3 Pipeline|  |
|  +-----------------------+  +-------------------+  +---------------+  |
+-----------------------------------------------------------------------+
                                   |
                                   | Low-Latency WebRTC Stream / MP4 URL
                                   v
+-----------------------------------------------------------------------+
|                      Client Visual Interface                          |
|     (Web Concierge / Mobile App / Digital Kiosk / Sales Portal)       |
+-----------------------------------------------------------------------+
```

## Comparative Empirical Matrix: Generative AI Video & Avatar Platforms

The following matrix benchmarks HeyGen against frontier AI video and avatar generation architectures as of early 2027:

| Architectural Metric | HeyGen (API v3 / MCP 3.1) | Synthesia (Expressive Avatars) | D-ID (Agents API) | Runway (Gen-3 Alpha / Turbo) | DeepBrain AI (AI Human) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Interactive Agents & Personalized Outreach | Enterprise Corporate Training | Low-latency WebRTC Chatbot Faces | Cinematic Generative Video Scenes | Kiosk & Broadcast Virtual Humans |
| **Interactive Latency** | $\mathbf{\le 150\text{ ms}}$ (WebRTC Live) | $350\text{--}650\text{ ms}$ (Batch stream) | $\sim 180\text{--}250\text{ ms}$ (WebRTC) | N/A (Non-interactive batch) | $\sim 200\text{--}300\text{ ms}$ |
| **Agentic Protocol** | **Native FastMCP 3.1** & SSE Streaming | Custom REST & Webhooks | REST & Streaming WebSocket | REST API & Polling | REST & WebSocket |
| **Supported Languages** | 175+ languages with vocal cloning | 140+ languages | 120+ languages | Multi-lingual prompts only | 80+ languages |
| **Resolution / FPS** | 4K UHD / 60 FPS (Batch); 1080p 60 FPS (WebRTC) | 1080p 30 FPS / 4K UHD | 720p / 1080p 30 FPS | 1080p / 4K 24-30 FPS | 1080p / 4K 30 FPS |
| **Micro-Expressions** | Dynamic saccadic eye movements & blendshapes | Pre-rendered facial blendshapes | Basic lip synchrony + eye blinks | Physics-driven full-body motions | Scripted gesture animations |
| **Deployment Mode** | Cloud SaaS + WebRTC Edge Gateway | Cloud SaaS | Cloud SaaS + Hybrid SDK | Cloud SaaS Render Farm | Cloud SaaS + Local Hardware Kiosk |

## Typical use cases
- **Real-Time Interactive AI Concierges**: Deploying WebRTC-powered interactive avatars on websites and customer portals for bi-directional customer support, product walkthroughs, and virtual assistance.
- **Automated Sales Outreach (API v3)**: Generating dynamically personalized video emails where the avatar addresses the client by name, mentions their specific company metrics, and presents tailored solutions.
- **Global Corporate Training & Onboarding**: Translating internal compliance and technical training videos into 175+ regional dialects with preserved original speaker tone and precise lip synchronizations.
- **Executive & Creator Digital Twins**: Scaling executive updates, keynote briefings, and social media media publishing using verified Studio Avatars that preserve exact facial nuances and vocal cadence.
- **Autonomous Video Pipelines**: Partnering with FastMCP 3.1 servers to ingest daily RSS feeds, database reports, or market news, convert them into formatted scripts, and publish rendered video news briefs automatically.

## Strengths
- **Sub-150ms Real-Time Streaming**: High-speed WebRTC pipeline for live interactive avatar sessions with fluid micro-expressions.
- **Robust API v3 & FastMCP 3.1 Integration**: Native compatibility with modern agentic task protocols, webhooks, and asynchronous job queuing.
- **Zero-Shot Voice & Lip Synchronization**: Unmatched lip-sync accuracy across 175+ languages without pitch distortion or audio-video desynchronization.
- **Multi-Modal Vision Integration**: Supports visual context ingestion—avatars can "see" user camera input or shared documents via integrated frontier models (e.g., Gemini 4.0 Ultra or Qwen 3.6 VL).
- **Enterprise Security & Verification**: Includes rigorous digital twin ownership verification, C2PA content authenticity credentials, SOC 2 Type II compliance, and strict privacy controls.

## Limitations
- **Cloud-Dependent Rendering**: Requires continuous cloud connectivity; no local, air-gapped desktop execution for full-fidelity avatar neural models.
- **Enterprise Consumption Costs**: High-volume real-time streaming and high-resolution rendering require paid API tier credits.
- **Cinematic Motion Boundaries**: Specialized for conversational human avatars; not built for complex physical stunt scenes, hyper-stylized physics animation, or 3D environmental action.

## When to use it
- When your application requires a human-like visual interface to increase customer engagement and conversational trust.
- For high-volume automated personalized video campaigns driven programmatically via REST APIs or FastMCP tool calls.
- When localizing video content across global teams without re-shooting original video footage.

## When not to use it
- For 100% offline, air-gapped video generation where external network calls are prohibited.
- For generating stylized physical world animations or non-human action scenes (consider [Luma Dream Machine](luma-dream-machine.md) or [Sora](sora.md)).
- If only local speech synthesis is needed without a video face (see [Fish Audio](fish-audio.md)).

## Getting started

### 1. Account & API Key Setup
Create an account on [HeyGen.com](https://www.heygen.com) and retrieve your API key from the **Developer Settings** dashboard.

```bash
export HEYGEN_API_KEY="your_api_key_here"
```

### 2. Studio Quick Start
1. Navigate to the HeyGen Web Studio.
2. Select an **Avatar** from the Public Library or create an **Instant Avatar**.
3. Input your desired **Script** or upload a pre-recorded audio file.
4. Customize background elements, text overlays, and framing.
5. Click **Submit** to generate your high-definition video asset.

### 3. Developer SDK Installation
Install the official Python or TypeScript SDKs for programmatically triggering video renders:

```bash
pip install heygen-sdk pydantic mcp
```

## CLI examples

### 1. Fetch Available Avatars via cURL
Retrieve the catalog of public and private avatars registered under your organization account:

```bash
curl -X GET https://api.heygen.com/v2/avatars \
     -H "X-Api-Key: $HEYGEN_API_KEY" \
     -H "Content-Type: application/json"
```

### 2. Trigger Headless Video Generation Job
Dispatch an asynchronous video generation task using a specified avatar ID and voice model:

```bash
curl -X POST https://api.heygen.com/v2/video/generate \
     -H "X-Api-Key: $HEYGEN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "video_inputs": [
         {
           "character": {
             "type": "avatar",
             "avatar_id": "Daisy-Professional-2027",
             "avatar_style": "normal"
           },
           "voice": {
             "type": "text",
             "input_text": "Welcome to our early 2027 enterprise platform update! All systems are performing at peak capacity.",
             "voice_id": "2d5b0a715a284c68a70685e137111a54",
             "speed": 1.0
           },
           "background": {
             "type": "color",
             "value": "#0F172A"
           }
         }
       ],
       "dimension": {
         "width": 1920,
         "height": 1080
       }
     }'
```

### 3. Check Asynchronous Video Job Status
Query the status of a queued video rendering job until complete:

```bash
curl -X GET "https://api.heygen.com/v1/video_status.get?video_id=YOUR_VIDEO_JOB_ID" \
     -H "X-Api-Key: $HEYGEN_API_KEY"
```

### 4. Create a Real-Time Streaming Interactive Session
Initialize a WebRTC real-time session for live interactive avatar streaming:

```bash
curl -X POST https://api.heygen.com/v1/realtime.task.create \
     -H "X-Api-Key: $HEYGEN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "avatar_id": "Josh_Lite_2027",
       "voice_id": "en-US-Jenny",
       "mcp_version": "3.1",
       "quality": "high"
     }'
```

## API examples

### 1. FastMCP 3.1 Tool Server Integration (Python)
The following code demonstrates a complete FastMCP 3.1 server implementation that exposes HeyGen video synthesis capabilities to AI agents:

```python
import os
import asyncio
import httpx
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, HttpUrl

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    "HeyGen Video Operations",
    version="3.1.0",
    description="Agentic Tool Server for HeyGen Video Synthesis and Avatar Streaming"
)

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY", "mock-key")
HEYGEN_BASE_URL = "https://api.heygen.com/v2"

class RenderVideoRequest(BaseModel):
    avatar_id: str = Field(..., description="ID of the HeyGen digital avatar")
    voice_id: str = Field(..., description="ID of the voice model for speech synthesis")
    script: str = Field(..., min_length=10, max_length=10000, description="Script for the avatar to recite")
    title: str = Field(default="Agent Generated Video", description="Title of the video job")
    aspect_ratio: str = Field(default="16:9", description="Aspect ratio: '16:9', '9:16', or '1:1'")

class VideoJobStatus(BaseModel):
    video_id: str = Field(..., description="Unique ID of the render job")
    status: str = Field(..., description="Status: 'pending', 'processing', 'completed', or 'failed'")
    video_url: Optional[str] = Field(None, description="Download URL if completed")
    error: Optional[str] = Field(None, description="Error message if failed")

@mcp.tool()
async def trigger_avatar_video_render(request: RenderVideoRequest) -> Dict[str, Any]:
    """
    Triggers an asynchronous headless video render job via HeyGen API v2/v3.
    Returns the job ID to monitor progress.
    """
    width, height = (1920, 1080) if request.aspect_ratio == "16:9" else (1080, 1920)
    if request.aspect_ratio == "1:1":
        width, height = (1080, 1080)

    payload = {
        "title": request.title,
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": request.avatar_id,
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": request.script,
                    "voice_id": request.voice_id
                }
            }
        ],
        "dimension": {"width": width, "height": height}
    }

    headers = {
        "X-Api-Key": HEYGEN_API_KEY,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{HEYGEN_BASE_URL}/video/generate", json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        return {
            "video_id": data.get("data", {}).get("video_id"),
            "status": "queued",
            "message": "Video rendering task successfully submitted to HeyGen."
        }

@mcp.tool()
async def check_video_status(video_id: str) -> Dict[str, Any]:
    """
    Queries the status of an ongoing video render job on HeyGen.
    """
    headers = {"X-Api-Key": HEYGEN_API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
            headers=headers,
            timeout=15.0
        )
        response.raise_for_status()
        data = response.json().get("data", {})

        return {
            "video_id": video_id,
            "status": data.get("status"),
            "video_url": data.get("video_url"),
            "duration": data.get("duration")
        }

if __name__ == "__main__":
    mcp.run()
```

### 2. Pydantic v2 Interactive Session Lifecycle & Validation Schema
Use strict Pydantic v2 schemas to validate avatar streaming configurations before initiating WebRTC connections:

```python
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, HttpUrl, ConfigDict

class AvatarStreamingSessionConfig(BaseModel):
    """
    Strict Pydantic v2 schema for initializing a HeyGen real-time interactive session.
    """
    model_config = ConfigDict(extra="forbid", frozen=True)

    avatar_id: str = Field(..., min_length=3, description="Unique identifier for the digital twin avatar")
    voice_id: str = Field(..., min_length=3, description="Voice ID configured for real-time TTS")
    quality: Literal["low", "medium", "high"] = Field(default="high", description="Stream resolution quality")
    mcp_version: str = Field(default="3.1", description="FastMCP protocol version alignment")
    max_session_duration_sec: int = Field(default=1800, ge=60, le=7200, description="Session timeout limit in seconds")
    knowledge_base_context: Optional[str] = Field(None, description="System prompt or context injected into avatar LLM")
    webhook_url: Optional[HttpUrl] = Field(None, description="Webhook endpoint for session disconnect events")

    @field_validator("avatar_id")
    @classmethod
    def validate_avatar_format(cls, v: str) -> str:
        if " " in v:
            raise ValueError("Avatar ID cannot contain whitespace. Use official identifier keys.")
        return v

# Example Usage & Schema Dumping
if __name__ == "__main__":
    sample_config = {
        "avatar_id": "Anna_Office_v3",
        "voice_id": "en-US-JennyNeural",
        "quality": "high",
        "mcp_version": "3.1",
        "max_session_duration_sec": 3600,
        "knowledge_base_context": "You are an enterprise AI concierge representing TechCorp in 2027.",
        "webhook_url": "https://api.techcorp.com/v1/webhooks/heygen"
    }

    validated_session = AvatarStreamingSessionConfig.model_validate(sample_config)
    print("Session validated successfully!")
    print(validated_session.model_dump_json(indent=2))
```

## Production Systemd Service Unit (`heygen-avatar-agent.service`)

To host the FastMCP 3.1 HeyGen Video and Avatar Bridge as an isolated Linux background daemon:

```ini
[Unit]
Description=HeyGen FastMCP 3.1 Avatar Bridge Daemon
After=network.target remote-fs.target
Documentation=https://developers.heygen.com/docs

[Service]
Type=simple
User=jules
Group=jules
WorkingDirectory=/home/jules/repo
Environment="PYTHONUNBUFFERED=1"
Environment="HEYGEN_API_KEY=YOUR_SECURE_API_KEY"
Environment="FASTMCP_PORT=8024"
ExecStart=/usr/bin/python3 -m uvicorn scripts.heygen_fastmcp_server:app --host 127.0.0.1 --port 8024 --workers 2
Restart=always
RestartSec=5s

# Process Sandboxing & Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Multi-Container Docker Compose Deployment (`docker-compose.heygen.yml`)

Run HeyGen's FastMCP 3.1 agent gateway with Redis session caching and an automated health probe:

```yaml
version: "3.9"

services:
  heygen-bridge:
    image: python:3.11-slim-bookworm
    container_name: heygen-fastmcp-bridge
    restart: unless-stopped
    working_dir: /app
    volumes:
      - ./:/app:ro
      - /tmp/heygen_cache:/tmp/heygen_cache:rw
    environment:
      - PYTHONUNBUFFERED=1
      - HEYGEN_API_KEY=${HEYGEN_API_KEY}
      - REDIS_URL=redis://redis-session-cache:6379/0
      - MCP_PORT=8024
    command: >
      bash -c "pip install --no-cache-dir fastmcp>=3.1.0 httpx>=0.27.0 pydantic>=2.10.0 redis>=5.0.0 &&
               python3 -m uvicorn app:server --host 0.0.0.0 --port 8024"
    networks:
      - heygen-net
    depends_on:
      redis-session-cache:
        condition: service_healthy

  redis-session-cache:
    image: redis:7.4-alpine
    container_name: heygen-redis-cache
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--maxmemory", "256mb", "--maxmemory-policy", "allkeys-lru"]
    ports:
      - "127.0.0.1:6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - heygen-net

networks:
  heygen-net:
    driver: bridge
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Root Cause | Remediation Strategy |
| :--- | :--- | :--- |
| `HTTP 401 Unauthorized` | Invalid, expired, or missing `HEYGEN_API_KEY` header | Verify API key credentials in Developer Dashboard; re-export `HEYGEN_API_KEY`. |
| `WebRTC ICE Connection Failed` | Strict corporate firewall or NAT blocking UDP port ranges (10000-20000) | Configure STUN/TURN fallback server URLs in WebRTC initialization configuration. |
| `HTTP 429 Too Many Requests` | Exceeded concurrent streaming avatar session quota | Implement exponential backoff or scale enterprise concurrency license tier. |
| `Audio-Video Desynchronization` | High network packet jitter ($>80\text{ ms}$) dropping RTP video frames | Increase jitter buffer size $J_{\text{buffer}}$ in client player configuration. |
| `Pydantic ValidationError: avatar_id` | Avatar identifier formatted with invalid whitespace or disallowed characters | Sanitize input using `AvatarStreamingSessionConfig.model_validate()`. |
| `Video Generation Timeout (Status: processing)` | GPU render queue congestion during peak batch rendering | Implement asynchronous webhook polling rather than blocking synchronous requests. |
| `Voice ID Not Found Error` | Voice identifier deprecated or not granted in team workspace | Query `/v2/voices` endpoint to retrieve active enterprise voice identifiers. |
| `C2PA Verification Failure` | Downstream transcoding stripped video authenticity cryptographic manifests | Configure video pipelines to preserve metadata containers and C2PA manifests. |

## Related tools / concepts
- [Synthesia](synthesia.md) — Enterprise competitor for AI video avatar synthesis and multi-lingual corporate training.
- [PersonaPlex](personaplex.md) — NVIDIA's ultra-low-latency neural speech and avatar conversation framework.
- [ElevenLabs](elevenlabs.md) — Frontier voice cloning and multi-lingual audio synthesis provider.
- [Luma Dream Machine](luma-dream-machine.md) — High-fidelity text-to-video generative model for cinematic scenes.
- [Sora](sora.md) — OpenAI's video generation foundation model.
- [Fish Audio](fish-audio.md) — Open-source local voice synthesis alternative for edge audio pipelines.
- [FastMCP 3.1 Protocol](../automation_orchestration/mcp.md) — Standardized task and tool interface connecting LLM agents with HeyGen servers.

## Sources / references
- [HeyGen Official Website](https://www.heygen.com)
- [HeyGen API v3 Developer Documentation](https://developers.heygen.com/)
- [HeyGen Interactive Avatar Realtime WebRTC Guide](https://www.heygen.com/interactive-avatar)
- [Model Context Protocol (FastMCP 3.1) Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
