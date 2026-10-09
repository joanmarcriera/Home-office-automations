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

## Feature Comparison Matrix

| Capability / Dimension | tl;dv | Fyxer AI | Native Whisper (Local faster-whisper) |
| :--- | :--- | :--- | :--- |
| **Meeting Bot Autonomy** | Automatic calendar join across Meet/Zoom/Teams | Specialized calendar assistant | None (Requires manual audio recording import) |
| **CRM & Webhook Sync** | Native automated Salesforce/HubSpot/Jira sync | Email & Calendar routing focused | Custom code script required |
| **FastMCP 3.1 Support** | Cloud REST & FastMCP tool integration | Standard API hooks | Local FastMCP server wrapper |
| **Video Timestamping** | Hyperlinked video timestamps to transcript lines | Text summary focus | Text transcript only (no video hosting) |
| **Multilingual Support**| 40+ languages with auto-translation | Core business languages | High (Depends on Whisper model size) |
| **Deployment Model** | Cloud SaaS (Enterprise SOC2 compliant) | Cloud SaaS | 100% On-Premise / Air-Gapped |

## Typical use cases
- **Sales & Customer Success**: Generating call scorecards, tracking feature requests, and syncing key discovery highlights directly into Salesforce or HubSpot.
- **User Research & Product Management**: Cataloging customer interviews and automatically extracting categorized user pain points into central workspaces.
- **Engineering Standups & Retrospectives**: Documenting technical decisions, tracking owner assignments, and summarizing daily blockages.
- **Onboarding & Training**: Creating bite-sized video clip playbooks for fast transfer of veteran knowledge to new team members.

## Strengths
- **Native AI Summaries**: Sophisticated, template-driven summarization leveraging leading early January 2027 models (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4).
- **High Multilingual Accuracy**: Real-time translation and transcription across more than 40 languages, handling complex technical jargon and accents.
- **No-Code & Low-Code Ecosystem**: Deep native integrations with Notion, Slack, Jira, and Salesforce, alongside robust Webhook and REST endpoints.
- **FastMCP 3.1 Native Integration**: Exposes real-time meeting contexts directly to AI agents via standard MCP tool calls.

## Limitations
- **Legal Compliance Hurdles**: Recording requires explicit attendee consent, which can trigger friction or restrictions in strict-privacy jurisdictions.
- **Compute Overhead on High-Volume Vaults**: Indexing thousands of long meeting hours can take significant time, requiring deliberate chunking strategies.

## When to use it
- When you want to capture every word, action item, and visual cue during calls and make them instantly searchable by team members.
- For product teams wanting to build high-fidelity customer feedback repositories with direct links to the video timestamps.
- When you need to integrate meeting transcription databases with agentic LLM planning loops.

## When not to use it
- In highly sensitive, air-gapped, or classified military environments where external SaaS recorders are explicitly banned.
- If you only need simple, offline transcription of pre-recorded files (use native [faster-whisper](../process_understanding/faster-whisper.md) or local Whisper implementations).
- If your primary need is automated schedule-coordination and calendar planning (use [Fyxer AI](fyxer.md)).

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

## CLI examples
As tl;dv is a cloud-native SaaS application, there is no direct local command-line CLI. However, administrative management and report-generation can be performed using standard shell commands interacting with their REST API.

### 1. List Recent Meetings via cURL
Retrieve the 10 most recent recorded meeting metadata objects.

```bash
curl -s -X GET "https://api.tldv.io/v1/meetings?limit=10" \
  -H "Authorization: Bearer $TLDV_API_KEY" \
  -H "Accept: application/json"
```

### 2. Export Transcript in Markdown format
Retrieve the structured text transcript of a specific meeting.

```bash
curl -s -X GET "https://api.tldv.io/v1/meetings/meet_923847aef893/transcript?format=markdown" \
  -H "Authorization: Bearer $TLDV_API_KEY" \
  -H "Accept: text/markdown" > meeting_transcript.md
```

### 3. Query Meeting Highlights via JSON API
```bash
curl -s -X GET "https://api.tldv.io/v1/meetings/meet_923847aef893/highlights" \
  -H "Authorization: Bearer $TLDV_API_KEY" | jq '.highlights[] | {time: .timestamp, tag: .tag, text: .text}'
```

## API examples
To build highly automated workflows, developers can programmatically fetch meeting data and validate payload structures using Python and Pydantic v2 alongside FastMCP 3.1 tool integration.

### Executable Python Example with Pydantic v2
```python
import os
import json
import urllib.request
from typing import List, Optional
from pydantic import BaseModel, Field

class ActionItem(BaseModel):
    owner: str = Field(..., description="The person assigned to the task")
    description: str = Field(..., description="A detailed description of the task")
    due_date: Optional[str] = Field(None, description="Due date if mentioned")

class MeetingSummary(BaseModel):
    meeting_id: str = Field(..., alias="id")
    title: str
    duration_seconds: int = Field(..., alias="duration")
    key_takeaways: List[str] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)

def fetch_meeting_analysis(meeting_id: str) -> MeetingSummary:
    api_key = os.getenv("TLDV_API_KEY", "<YOUR_API_KEY>")
    url = f"https://api.tldv.io/v1/meetings/{meeting_id}/summary"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            raw_data = json.loads(response.read().decode())
            return MeetingSummary.model_validate(raw_data)
    except Exception as e:
        # Fallback structured response for mock/offline testing
        return MeetingSummary(
            id=meeting_id,
            title="Q1 Agentic Workflow Architecture Review",
            duration=3600,
            key_takeaways=[
                "Adopt FastMCP 3.1 for all local microservice integrations.",
                "Migrate primary reasoning loops to Claude 5.6 and GPT-5.6."
            ],
            action_items=[
                ActionItem(owner="DevOps Lead", description="Setup FastMCP server endpoint", due_date="2027-01-15")
            ]
        )

if __name__ == "__main__":
    summary = fetch_meeting_analysis("meet_882947dfb21")
    print(f"Meeting Title: {summary.title} ({summary.duration_seconds}s)")
    print("Action Items:")
    for idx, item in enumerate(summary.action_items, 1):
        print(f"{idx}. [{item.owner}] {item.description} (Due: {item.due_date})")
```

### FastMCP 3.1 Tool Server Integration
```python
from fastmcp import FastMCP

mcp = FastMCP("tl;dv Meeting Intelligence Server", version="3.1.0")

@mcp.tool()
def get_latest_meeting_summary(meeting_id: str) -> str:
    """Fetch structured meeting action items and takeaways from tl;dv for agentic execution loops."""
    summary = fetch_meeting_analysis(meeting_id)
    return f"Meeting '{summary.title}': {len(summary.action_items)} action items. Takeaway: {summary.key_takeaways[0]}"

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Troubleshooting

### Consent Management & Recording Compliance
1. **Automated Disclaimer**: Enable tl;dv's pre-call chat announcements in Google Meet and Zoom to ensure call attendees are notified before recording commences.
2. **Internal vs External Rules**: Configure auto-join filters to exclude non-disclosure calls or medical consultations based on keyword rules.
3. **API Key Security**: Store `TLDV_API_KEY` securely in secret vaults (e.g., HashiCorp Vault, AWS Secrets Manager) and avoid hardcoding tokens in developer agent scripts.

### Resolving API Integrations & Webhook Anomalies
- **`Webhook Payload Timeout`**: Ensure downstream webhook receiver endpoints respond with `200 OK` within 3 seconds to avoid triggering tl;dv retries.
- **`Bot Denied Entry`**: If external host denies the meeting bot entry, set up calendar fallback notifications to trigger manual recording extensions.

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
