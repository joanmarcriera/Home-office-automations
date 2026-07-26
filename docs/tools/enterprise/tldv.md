# tl;dv

## What it is
tl;dv is an AI-powered meeting recorder, transcription, and conversational intelligence platform designed for remote and hybrid teams. Operating across Zoom, Google Meet, and Microsoft Teams, it captures video, generates real-time multilingual transcripts, and extracts key action items and insights using frontier LLMs.

Key capabilities include:
- **Autonomous Meeting Agents**: Custom-branded AI meeting bots that automatically join scheduled calendar events, handle audio/video capture, and process transcripts in real-time.
- **Cross-Meeting Intelligence**: Semantic aggregation across dozens of historical meetings to detect recurring themes, customer sentiment changes, or process bottlenecks.
- **Sales Playbook Coaching**: Automated evaluation of sales conversations against pre-defined qualification models (e.g., BANT, MEDDPICC), producing structured scorecards and direct CRM updates.
- **Model Context Protocol (MCP 3.1) integration**: Local and cloud-hosted MCP servers that feed real-time meeting context directly into developer workspaces (such as Claude 5.1 and GPT-5.5-based IDEs).

## What problem it solves
It solves the issue of lost organizational knowledge and meeting fatigue by replacing manual minute-taking with structured, searchable transcripts. It bridges synchronous call discussions with asynchronous documentation, making meeting highlights immediately referenceable.

## Where it fits in the stack
**Enterprise Productivity / Meeting Intelligence Layer**. It serves as a continuous context ingestion engine feeding downstream CRM, knowledge management, and task routing systems.

## Typical use cases
- **Sales & Customer Success**: Generating call scorecards, tracking feature requests, and syncing key discovery highlights directly into Salesforce or HubSpot.
- **User Research & Product Management**: Cataloging customer interviews and automatically extracting categorized user pain points into central workspaces.
- **Engineering Standups & Retrospectives**: Documenting technical decisions, tracking owner assignments, and summarizing daily blockages.
- **Onboarding & Training**: Creating bite-sized video clip playbooks for fast transfer of veteran knowledge to new team members.

## Strengths
- **Native AI Summaries**: Sophisticated, template-driven summarization leveraging leading late August 2026 models (Claude 5.1, GPT-5.5).
- **High Multilingual Accuracy**: Real-time translation and transcription across more than 40 languages, handling complex technical jargon and accents.
- **No-Code & Low-Code Ecosystem**: Deep native integrations with Notion, Slack, Jira, and Salesforce, alongside robust Webhook and REST endpoints.

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

### 3. Register a Custom Webhook Endpoint
Configure a real-time event subscription for when meeting processing finishes.

```bash
curl -s -X POST "https://api.tldv.io/v1/webhooks" \
  -H "Authorization: Bearer $TLDV_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://api.homelab.local/v1/tldv-ingestion",
    "events": ["meeting.processed"],
    "secret": "hmac_secret_2026_xyz"
  }'
```

## API examples
To build highly automated workflows, developers can programmatically fetch meeting data and validate payload structures using Python and Pydantic v2.

### 1. Fetching and Validating Meeting Summaries (Python SDK / REST API)
Below is a complete script demonstrating how to fetch summary metadata, parse it safely using modern Pydantic v2 structures, and integrate it with custom agents.

```python
import os
import requests
from typing import List, Optional
from pydantic import BaseModel, Field

# Ensure you have your environment variable set
# export TLDV_API_KEY="your_api_key_here"

class ActionItem(BaseModel):
    owner: str = Field(..., description="The person assigned to the task")
    description: str = Field(..., description="A detailed description of the task")
    due_date: Optional[str] = Field(None, description="Due date if mentioned")

class MeetingSummary(BaseModel):
    meeting_id: str = Field(..., alias="id")
    title: str
    duration_seconds: int = Field(..., alias="duration")
    key_takeaways: List[str] = Field(default=[])
    action_items: List[ActionItem] = Field(default=[])

def fetch_meeting_analysis(meeting_id: str) -> MeetingSummary:
    api_key = os.getenv("TLDV_API_KEY")
    if not api_key:
        raise ValueError("TLDV_API_KEY is not configured in the environment.")

    url = f"https://api.tldv.io/v1/meetings/{meeting_id}/summary"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse payload using Pydantic v2
    return MeetingSummary.model_validate(response.json())

if __name__ == "__main__":
    try:
        summary = fetch_meeting_analysis("meet_882947dfb21")
        print(f"Meeting: {summary.title}")
        print("Action Items:")
        for idx, item in enumerate(summary.action_items, 1):
            print(f"{idx}. [{item.owner}] {item.description} (Due: {item.due_date})")
    except Exception as e:
        print(f"Failed to fetch and parse meeting summary: {e}")
```

### 2. Streaming Meeting Video and Audio Sub-Clips
Fetch the high-speed download URL of a specific highlight clip for archive storage.

```python
import requests

def get_clip_download_url(meeting_id: str, clip_id: str) -> str:
    headers = {"Authorization": f"Bearer {os.getenv('TLDV_API_KEY')}"}
    url = f"https://api.tldv.io/v1/meetings/{meeting_id}/clips/{clip_id}/download"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("download_url")
```

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
- [Google Meet MCP Integration & Virtual Meetings](https://tldv.io/blog/google-meet-mcp/)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
