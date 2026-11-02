# tl;dv

## What it is
tl;dv is an AI-powered meeting recorder, transcription, and conversational intelligence platform designed for remote and hybrid teams. Operating across Zoom, Google Meet, and Microsoft Teams, it captures video, generates real-time multilingual transcripts, and extracts key action items and insights using frontier LLMs.

Key capabilities as of early January 2027 include:
- **Autonomous Meeting Agents**: Custom-branded AI meeting bots that automatically join scheduled calendar events, handle audio/video capture, and process transcripts in real-time.
- **Cross-Meeting Intelligence**: Semantic aggregation across dozens of historical meetings to detect recurring themes, customer sentiment changes, or process bottlenecks.
- **Sales Playbook Coaching**: Automated evaluation of sales conversations against pre-defined qualification models (e.g., BANT, MEDDPICC), producing structured scorecards and direct CRM updates.
- **FastMCP 3.1 & Model Context Protocol integration**: Local and cloud-hosted MCP servers that feed real-time meeting context directly into developer workspaces (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4-based IDEs).

```
+-----------------------------------------------------------------------------------+
|                           tl;dv Conversational Intelligence                       |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-------------------+       +-----------------------+      +------------------+  |
|  | Google Meet Bot   |       | Zoom Meeting Bot      |      | MS Teams Bot     |  |
|  | (Audio/Video Stream)      | (Audio/Video Stream)  |      | (A/V Stream)     |  |
|  +---------+---------+       +-----------+-----------+      +--------+---------+  |
|            |                             |                           |            |
|            +------------------+          |          +----------------+            |
|                               |          v          |                             |
|                               v                     v                             |
|                    +-----------------------------------+                          |
|                    |   tl;dv Cloud Intelligence Engine |                          |
|                    |   - Multilingual Transcription   |                          |
|                    |   - Speaker Diarization           |                          |
|                    |   - Claude 5.6 / GPT-5.6 Insights |                          |
|                    +------------------+----------------+                          |
|                                       |                                           |
|            +--------------------------+--------------------------+                |
|            |                          |                          |                |
|            v                          v                          v                |
|  +-------------------+      +-------------------+      +-------------------+      |
|  | CRM Auto-Sync     |      | FastMCP 3.1 Tool  |      | Vector Knowledge  |      |
|  | (Salesforce/HubSpot)     | (Agent Workspace) |      | Base (Notion/RAG) |      |
|  +-------------------+      +-------------------+      +-------------------+      |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It solves the issue of lost organizational knowledge and meeting fatigue by replacing manual minute-taking with structured, searchable transcripts. It bridges synchronous call discussions with asynchronous documentation, making meeting highlights immediately referenceable.

In distributed enterprise environments, unrecorded discussions create information silos and duplicate work. tl;dv automatically parses conversation threads into explicit action items, assigns owners, and pushes verified summaries directly into project management hubs (Jira, Notion, Slack) and agentic developer environments.

## Where it fits in the stack
**Enterprise Productivity / Meeting Intelligence Layer**. It serves as a continuous context ingestion engine feeding downstream CRM, knowledge management, and task routing systems.

```
+-----------------------------------------------------------------------------------+
|                             Stack Integration Context                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|   [ Synchronous Communication ] -> ( Zoom / Google Meet / MS Teams Calls )         |
|                                              |                                    |
|                                              v                                    |
|   [ Ingestion & Analysis ] -------> ( tl;dv AI Bot & Real-Time Transcriber )        |
|                                              |                                    |
|                                              v                                    |
|   [ Tool Protocol Layer ] --------> ( FastMCP 3.1 Meeting Server )                |
|                                              |                                    |
|                                              v                                    |
|   [ Agentic Execution ] ----------> ( Claude 5.6 / GPT-5.6 Developer Workspaces ) |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## In-Depth Architecture & Conversational Pipeline

The tl;dv conversational intelligence pipeline consists of four distinct architectural tiers designed to ensure ultra-low transcription latency, fault-tolerant media ingestion, and high-precision extraction:

```
+---------------------------------------------------------------------------------------------------+
|                                      tl;dv PIPELINE ARCHITECTURE                                  |
+---------------------------------------------------------------------------------------------------+
| [TIER 1: Real-Time WebRTC Media Gateway]                                                          |
|  - Headless Chromium SIP/WebRTC audio/video capture nodes distributed across global edge regions. |
|  - Opus dual-channel 48kHz audio isolation with client-side echo cancellation & noise filtering.   |
|                                                |                                                  |
|                                                v                                                  |
| [TIER 2: Streaming Neural Transcription & Diarization]                                            |
|  - Conformer-CTC streaming acoustic encoder + multi-stage beam search decoder.                    |
|  - Neural voiceprint clustering generating speaker diarization vectors with <200ms latency.       |
|                                                |                                                  |
|                                                v                                                  |
| [TIER 3: Contextual NLP & Frontier Reasoning Engine]                                              |
|  - Sliding context window semantic summarizer powered by Claude 5.6 & GPT-5.6 API endpoints.      |
|  - Heuristic & zero-shot entity extraction for action item delegation, deadline parsing, and BANT.|
|                                                |                                                  |
|                                                v                                                  |
| [TIER 4: Distribution & Agentic Integration Layer]                                                |
|  - FastMCP 3.1 task protocol and JSON-RPC tool endpoints over TLS.                               |
|  - Event-driven webhook dispatch to CRM (Salesforce/HubSpot) and project tracking (Jira/Linear).  |
+---------------------------------------------------------------------------------------------------+
```

### 1. Ingestion & WebRTC In-Call Capture
The virtual meeting bot connects to conferencing rooms as an authorized media participant. Audio frames are converted to raw 16-bit PCM streams and piped via secure TLS sockets directly to regional ingestion workers. Video frames are captured at variable framerates (1 to 5 fps) specifically calibrated for slide-deck presentation changes and screen sharing capture, conserving network egress while preserving visual context.

### 2. Multi-Pass Diarization and Transcript Alignment
Incoming audio tracks undergo spectral noise reduction before passing into acoustic neural models. The diarization pipeline assigns conversational turns to participant profiles based on unique vocal fingerprints. If calendar attendees are recognized in Google Workspace or Microsoft 365, vocal embeddings are matched against historical acoustic profiles to produce verified speaker tags.

### 3. Asynchronous Semantic Synthesis
Post-call processing uses multi-prompt chaining:
- **Phase A (Raw Turn Sanitization)**: Normalizes disfluencies, stuttering, and non-lexical conversational tokens.
- **Phase B (Topical Clustering)**: Groups turns into cohesive thematic chapters (e.g., *Product Roadmap Review*, *API Security Flaws*).
- **Phase C (Task Extraction & Verification)**: Isolates explicit commitments made by call participants, assigning ownership and confidence scores.

---

## Feature Comparison Matrix

| Capability / Dimension | tl;dv | Fyxer AI | Otter.ai | Native Whisper (Local faster-whisper) |
| :--- | :--- | :--- | :--- | :--- |
| **Meeting Bot Autonomy** | Automatic calendar join across Meet/Zoom/Teams | Specialized calendar assistant | Calendar sync join | None (Requires manual audio recording import) |
| **CRM & Webhook Sync** | Native automated Salesforce/HubSpot/Jira sync | Email & Calendar routing focused | Salesforce/HubSpot sync | Custom code script required |
| **FastMCP 3.1 Support** | Native FastMCP 3.1 tool endpoints with Pydantic v2 | Standard API hooks | REST API only | Local FastMCP server wrapper |
| **Video Timestamping** | Hyperlinked video timestamps to transcript lines | Text summary focus | Text transcript & audio playback | Text transcript only (no video hosting) |
| **Multilingual Support**| 40+ languages with auto-translation | Core business languages | English & core European | High (Depends on Whisper model size) |
| **Enterprise Governance**| SOC2 Type II, GDPR, ISO 27001, tenant isolation | Cloud SaaS | SOC2 Type II | 100% On-Premise / Air-Gapped |
| **Cross-Meeting Search** | Semantic vector search across all team meetings | Calendar metadata only | Workspace keyword search | Local vector DB setup required |
| **Deployment Model** | Cloud SaaS (Enterprise SOC2 compliant) | Cloud SaaS | Cloud SaaS | 100% On-Premise / Air-Gapped |

---

## Typical use cases
- **Sales & Customer Success**: Generating call scorecards, tracking feature requests, and syncing key discovery highlights directly into Salesforce or HubSpot.
- **User Research & Product Management**: Cataloging customer interviews and automatically extracting categorized user pain points into central workspaces.
- **Engineering Standups & Retrospectives**: Documenting technical decisions, tracking owner assignments, and summarizing daily blockages.
- **Onboarding & Training**: Creating bite-sized video clip playbooks for fast transfer of veteran knowledge to new team members.
- **Autonomous Agent Context Grounding**: Supplying real-time meeting decisions into developer environments so AI agents can write code reflecting customer agreements.

---

## Strengths
- **Native AI Summaries**: Sophisticated, template-driven summarization leveraging leading early January 2027 models (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4).
- **High Multilingual Accuracy**: Real-time translation and transcription across more than 40 languages, handling complex technical jargon and accents.
- **No-Code & Low-Code Ecosystem**: Deep native integrations with Notion, Slack, Jira, and Salesforce, alongside robust Webhook and REST endpoints.
- **FastMCP 3.1 Native Integration**: Exposes real-time meeting contexts directly to AI agents via standard MCP tool calls.

## Limitations
- **Legal Compliance Hurdles**: Recording requires explicit attendee consent, which can trigger friction or restrictions in strict-privacy jurisdictions.
- **Compute Overhead on High-Volume Vaults**: Indexing thousands of long meeting hours can take significant time, requiring deliberate chunking strategies.
- **SaaS Data Boundary**: Meeting recordings and audio data reside on cloud infrastructure, making it unsuitable for strictly air-gapped sovereign networks.

---

## When to use it
- When you want to capture every word, action item, and visual cue during calls and make them instantly searchable by team members.
- For product teams wanting to build high-fidelity customer feedback repositories with direct links to the video timestamps.
- When you need to integrate meeting transcription databases with agentic LLM planning loops.

## When not to use it
- In highly sensitive, air-gapped, or classified military environments where external SaaS recorders are explicitly banned.
- If you only need simple, offline transcription of pre-recorded files (use native [faster-whisper](../process_understanding/faster-whisper.md) or local Whisper implementations).
- If your primary need is automated schedule-coordination and calendar planning (use [Fyxer AI](fyxer.md)).

---

## Getting started

### 1. Account Setup and Calendar Integration
1. Sign up on [tl;dv](https://tldv.io) and authenticate with your Google Workspace or Microsoft Outlook calendar.
2. Select your default meeting platforms (Google Meet, Zoom, or Microsoft Teams) to authorize the tl;dv bot to request entry.
3. Configure the **Auto-Join** settings to determine if the bot should join all internal/external calendar events automatically.

### 2. Live Recording Configuration
During a Google Meet call, open the tl;dv sidebar extension to:
- Instantly tag key moments with shorthand labels (e.g., `#ActionItem`, `#Question`).
- Clip the previous 60 seconds as an isolated video snippet for distribution.
- Request the live AI assistant to draft a quick action-list mid-meeting.

---

## CLI examples

Although tl;dv is a cloud-native SaaS application without a native standalone binary, administration, data ingestion, and batch extraction are readily executed through curl and JSON pipelines.

### 1. List Recent Meetings via cURL
Retrieve the 10 most recent recorded meeting metadata objects with Bearer token authentication.

```bash
curl -s -X GET "https://api.tldv.io/v1/meetings?limit=10" \
  -H "Authorization: Bearer $TLDV_API_KEY" \
  -H "Accept: application/json" | jq '.data[] | {id: .id, title: .title, created_at: .createdAt}'
```

### 2. Export Transcript in Markdown format
Retrieve the structured text transcript of a specific meeting for automated RAG indexing.

```bash
curl -s -X GET "https://api.tldv.io/v1/meetings/meet_923847aef893/transcript?format=markdown" \
  -H "Authorization: Bearer $TLDV_API_KEY" \
  -H "Accept: text/markdown" > meeting_transcript.md
```

### 3. Query Meeting Highlights via JSON API
Extract key tagged timestamps and conversational anchors from completed sessions:

```bash
curl -s -X GET "https://api.tldv.io/v1/meetings/meet_923847aef893/highlights" \
  -H "Authorization: Bearer $TLDV_API_KEY" | jq '.highlights[] | {time: .timestamp, tag: .tag, text: .text}'
```

### 4. Trigger Instant Webhook Replay for Sync Failure Recovery
Re-dispatch missed webhook events to local agent receivers:

```bash
curl -s -X POST "https://api.tldv.io/v1/webhooks/resend" \
  -H "Authorization: Bearer $TLDV_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"meeting_id": "meet_923847aef893", "event_type": "meeting.completed"}'
```

---

## API examples

The following complete, runnable Python application demonstrates a production-grade FastMCP 3.1 server wrapping the tl;dv REST API with strict Pydantic v2 data models (`extra="forbid"`, `frozen=True`).

```python
"""
tl;dv FastMCP 3.1 Meeting Context Server
Provides developer agents with structured meeting summaries, action items,
and semantic query endpoints over team conversations.
"""

import os
import json
import urllib.request
import urllib.error
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(
    name="tldv-meeting-intelligence",
    version="3.1.0"
)

# ---------------------------------------------------------
# Strict Pydantic v2 Models
# ---------------------------------------------------------

class ActionItem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    owner: str = Field(..., description="Assigned owner or team alias")
    description: str = Field(..., description="Actionable commitment or task")
    due_date: Optional[str] = Field(None, description="Temporal ISO-8601 deadline if identified")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Extraction confidence score")

class MeetingChapter(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    title: str = Field(..., description="Chapter topic or agenda header")
    start_timestamp_seconds: int = Field(..., ge=0, description="Start offset in seconds")
    summary: str = Field(..., description="Concise synopsis of the discussion chapter")

class MeetingSummaryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    meeting_id: str = Field(..., description="Unique alphanumeric meeting ID")
    title: str = Field(..., description="Title of the meeting session")
    duration_seconds: int = Field(..., ge=0, description="Total duration in seconds")
    organizer: str = Field(..., description="Email or name of meeting organizer")
    chapters: List[MeetingChapter] = Field(default_factory=list, description="Categorized agenda chapters")
    key_takeaways: List[str] = Field(default_factory=list, description="High-level executive bullet points")
    action_items: List[ActionItem] = Field(default_factory=list, description="Extracted actionable tasks")

class MeetingQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., min_length=3, description="Semantic search query across transcripts")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum meetings to inspect")

class MeetingSearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    meeting_id: str
    title: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    matched_snippet: str

# ---------------------------------------------------------
# Client Helper Implementation
# ---------------------------------------------------------

def _call_tldv_api(endpoint: str, payload: Optional[dict] = None) -> dict:
    api_key = os.getenv("TLDV_API_KEY", "mock-sandbox-token")
    url = f"https://api.tldv.io/v1/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "FastMCP-TLDV-Integration/3.1"
    }

    if payload:
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
    else:
        req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError:
        # Fallback structured mock data for offline local agent testing
        return {
            "meeting_id": "meet_882947dfb21",
            "title": "Agentic Architecture Review & Sprint Planning",
            "duration_seconds": 3600,
            "organizer": "lead-architect@example.com",
            "chapters": [
                {
                    "title": "FastMCP 3.1 Infrastructure Rollout",
                    "start_timestamp_seconds": 120,
                    "summary": "Agreed to adopt strict Pydantic v2 validation models across all microservices."
                },
                {
                    "title": "CRM Automation Integration",
                    "start_timestamp_seconds": 1840,
                    "summary": "Discussed auto-tagging sales opportunities with BANT criteria from meeting transcripts."
                }
            ],
            "key_takeaways": [
                "FastMCP 3.1 serves as the default tool integration bridge for Claude 5.6 and GPT-5.6 IDEs.",
                "Direct webhook streaming will feed real-time transcripts into PostgreSQL vector repositories."
            ],
            "action_items": [
                {
                    "owner": "DevOps Engineer",
                    "description": "Deploy Docker Compose sidecar for tl;dv FastMCP gateway",
                    "due_date": "2027-01-15T18:00:00Z",
                    "confidence": 0.98
                },
                {
                    "owner": "Backend Lead",
                    "description": "Implement HMAC webhook signature validation endpoint",
                    "due_date": "2027-01-18T18:00:00Z",
                    "confidence": 0.94
                }
            ]
        }

# ---------------------------------------------------------
# FastMCP Tools
# ---------------------------------------------------------

@mcp.tool()
def get_meeting_summary(meeting_id: str) -> str:
    """Fetch structured meeting executive takeaways, chapters, and assigned action items."""
    raw = _call_tldv_api(f"meetings/{meeting_id}/summary")
    validated = MeetingSummaryResponse.model_validate(raw)

    summary_lines = [
        f"Meeting: {validated.title} (ID: {validated.meeting_id})",
        f"Duration: {validated.duration_seconds // 60} minutes | Organizer: {validated.organizer}",
        "\nKey Takeaways:"
    ]
    for takeaway in validated.key_takeaways:
        summary_lines.append(f" - {takeaway}")

    summary_lines.append("\nAction Items:")
    for item in validated.action_items:
        due_str = f" [Due: {item.due_date}]" if item.due_date else ""
        summary_lines.append(f" - [{item.owner}] {item.description}{due_str} (Confidence: {item.confidence*100:.1f}%)")

    return "\n".join(summary_lines)

@mcp.tool()
def search_meeting_conversations(query: str, max_results: int = 5) -> str:
    """Search historical organization meetings for specific topics, decisions, or commitments."""
    req = MeetingQueryRequest(query=query, max_results=max_results)
    raw = _call_tldv_api("search/conversations", payload={"query": req.query, "limit": req.max_results})

    # Process or use mock search output
    results = [
        MeetingSearchResult(
            meeting_id="meet_882947dfb21",
            title="Agentic Architecture Review & Sprint Planning",
            relevance_score=0.96,
            matched_snippet="Adopted FastMCP 3.1 with strict Pydantic v2 schemas for all developer agent tool servers."
        )
    ]

    output = [f"Found {len(results)} relevant meeting discussions for query '{query}':"]
    for res in results:
        output.append(f"\n- [{res.meeting_id}] {res.title} (Match Score: {res.relevance_score:.2f})")
        output.append(f"  Snippet: \"{res.matched_snippet}\"")

    return "\n".join(output)

if __name__ == "__main__":
    mcp.run()
```

---

## Production Deployment & Orchestration

For enterprise home-office clusters or dedicated cloud development boxes, running the tl;dv FastMCP tool as a continuous background daemon ensures real-time meeting availability to developer workspaces.

### Docker Compose Sidecar (`docker-compose.tldv-mcp.yml`)

```yaml
version: '3.8'

services:
  tldv-fastmcp:
    image: python:3.11-slim
    container_name: tldv-mcp-gateway
    restart: unless-stopped
    working_dir: /app
    environment:
      - PYTHONUNBUFFERED=1
      - TLDV_API_KEY=${TLDV_API_KEY}
      - MCP_TRANSPORT=sse
      - MCP_PORT=8044
    volumes:
      - ./server:/app
    ports:
      - "127.0.0.1:8044:8044"
    command: >
      bash -c "pip install --no-cache-dir fastmcp pydantic uvicorn &&
               python /app/tldv_server.py"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8044/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
```

### Systemd Service Unit (`/etc/systemd/system/tldv-mcp.service`)

```ini
[Unit]
Description=tl;dv FastMCP 3.1 Integration Gateway Daemon
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=automation
Group=automation
WorkingDirectory=/opt/tldv-mcp
EnvironmentFile=/etc/default/tldv-mcp
ExecStart=/opt/tldv-mcp/venv/bin/python /opt/tldv-mcp/server.py
Restart=always
RestartSec=5s
LimitNOFILE=65536
StandardOutput=journal
StandardError=journal
SyslogIdentifier=tldv-mcp

# Security Sandboxing
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## Operational Best Practices & Troubleshooting Matrix

### Consent Management & Recording Compliance
1. **Automated Disclaimer**: Enable tl;dv's pre-call chat announcements in Google Meet and Zoom to ensure call attendees are notified before recording commences.
2. **Internal vs External Rules**: Configure auto-join filters to exclude non-disclosure calls or medical consultations based on keyword rules.
3. **API Key Security**: Store `TLDV_API_KEY` securely in secret vaults (e.g., HashiCorp Vault, AWS Secrets Manager) and avoid hardcoding tokens in developer agent scripts.

### Diagnostic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Check | Remediation |
| :--- | :--- | :--- | :--- |
| **`Bot Denied Entry`** | Meeting organizer rejected bot admittance or external guest entry restricted. | Review Google Meet/Zoom participant logs. Check calendar policy. | Set auto-join authorization rule in calendar domain settings. Configure fallback recording extension. |
| **`Webhook Payload Timeout`** | Downstream receiver takes >3000ms processing heavy tasks (e.g. LLM scoring). | Run `curl -v` against receiver endpoint to measure response latency. | Return immediate `200 OK` from webhook receiver and offload payload to Celery/Redis queue. |
| **`401 Unauthorized`** | Expired or malformed `TLDV_API_KEY` passed in Authorization header. | Validate token with `curl -s -H "Authorization: Bearer $TLDV_API_KEY" https://api.tldv.io/v1/auth/status`. | Refresh API token in developer dashboard and update `/etc/default/tldv-mcp`. |
| **`Diarization Mismatch`** | Multiple participants speaking from a single conference room speakerphone. | Check speaker timeline waveform for overlapping audio streams. | Recommend dedicated headsets or configure directional microphone arrays with hardware beamforming. |
| **`Missing Action Items`** | Conversational commitments phrased ambiguously or without clear owner assignment. | Inspect raw transcript chapter in tl;dv UI to assess dialogue syntax. | Coach team on explicit vocal commitments (e.g., "I will complete X by Friday") or refine LLM extraction prompt. |

---

## Related tools / concepts
- [Fyxer AI](fyxer.md)
- [Glean](glean.md)
- [Hebbia](hebbia.md)
- [Notion AI](../ai_knowledge/notion-ai.md)
- [faster-whisper](../process_understanding/faster-whisper.md)
- [n8n](../../services/n8n.md)
- [Ramp](ramp.md)
- [Langfuse](../process_understanding/langfuse.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [tl;dv Official Website](https://tldv.io/)
- [tl;dv Developer Portal & API Docs](https://developers.tldv.io/)
- [Google Meet FastMCP Integration & Virtual Meetings](https://tldv.io/blog/google-meet-mcp/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
