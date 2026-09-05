# Fyxer AI

## What it is
Fyxer AI is an executive-grade AI assistant platform designed to automate inbox triage, calendar scheduling, and administrative workflows for high-volume professionals and leadership teams. Operating as an intelligent agentic layer across communication platforms (Gmail, Microsoft Outlook, Teams), it natively incorporates frontier models ([Claude 5.6](../providers/anthropic.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md)) and supports **FastMCP 3.1** protocol standards.

Key capabilities include:
- **AI Inbox Management**: Automatically triages and labels incoming emails, drafts context-aware responses in the user's voice, and highlights critical action items.
- **Meeting Intelligence**: Automatically records, transcribes, and extracts structured action items/tasks from virtual meetings.
- **Automated Scheduling Assistant**: Coordinates meeting times across internal and external calendars via natural language negotiation.
- **Adaptive Voice Profiles**: Personalized voice modeling to ensure generated email drafts align with the user's communication style.

## What problem it solves
It eliminates administrative overhead and inbox fragmentation. Rather than serving as a basic drafting tool, Fyxer operates as an autonomous executive delegation platform, saving hours previously spent on manual email processing, calendar coordination, and meeting note synthesis.

## Where it fits in the stack
**Enterprise Productivity / Executive Delegation Layer**. It functions as an AI executive assistant integrated with workspace communication tools and enterprise automation systems.

## Typical use cases
- **Executive Workflow Delegation**: Managing heavy administrative volume for executives, founders, and management teams.
- **Client Service Operations**: Automating client intake, follow-ups, and calendar scheduling for legal, financial, and consulting practices.
- **Enterprise Executive Operations**: Standardizing meeting intelligence, task routing, and email triage across leadership functions.

## Strengths
- **All-in-One Executive Platform**: Consolidates meeting recording, email triage, and calendar scheduling into a single service.
- **High-Fidelity Persona Matching**: Learns user writing style and domain context for natural email drafting.
- **FastMCP 3.1 & Model Gateway**: Connects with enterprise tool ecosystems and frontier reasoning engines.
- **Quantifiable Time Savings**: Eliminates repetitive administrative tasks for high-load knowledge workers.

## Limitations
- **Platform Dependency**: Core functions require OAuth access to Google Workspace or Microsoft 3.0/365 environments.
- **Usage-Based Enterprise Pricing**: Email and meeting processing volumes beyond baseline plans incur usage charges.

## When to use it
- When managing high-volume email streams (10+ hours/week) requiring intelligent triage and automated response drafting.
- When requiring automated calendar negotiation and meeting transcription tied directly into enterprise task systems.
- When establishing personalized "AI voice profiles" for consistent executive communication.

## When not to use it
- For organizations relying exclusively on [Slack](../../services/slack.md) or [Discord](../../services/discord.md) without heavy email workflows.
- For low-volume administrative environments where automated triage provides minimal incremental leverage.

## Getting started

### Minimal Concepts
1. **AI Inbox**: Primary interface where incoming mail is automatically triaged and draft replies are staged.
2. **Voice Profile**: Learned communication persona built from sent email history.
3. **Fyxer Meeting Bot**: Autonomous agent that joins calendar invites for recording and action-item extraction.

### Getting Started Example
Add `assistant@fyxer.com` to any Google Calendar or Outlook invite to initiate meeting transcription and automated summary generation.

```bash
# Register Fyxer assistant on a meeting invite:
# Simply invite assistant@fyxer.com as a participant in your calendar event.
```

## CLI examples

### Triggering Voice Profile Sync
Enterprise administrators can trigger manual synchronization of voice profiles via the CLI:

```bash
curl -X POST "https://api.fyxer.com/v1/voice/sync" \
  -H "Authorization: Bearer $FYXER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profile_id": "prof_voice_2027_01", "sync_source": "sent_emails"}'
```

## API examples

### Programmatic Daily Brief Retrieval with Pydantic v2
Fetching executive daily briefings using Python and validating response payloads with Pydantic v2:

```python
from pydantic import BaseModel, Field
import urllib.request
import json

class ActionItem(BaseModel):
    task: str = Field(description="Action item task description")
    source: str = Field(description="Originating source (email/meeting)")
    priority: str = Field(default="normal", description="Priority level")

class FyxerDailyBrief(BaseModel):
    brief_id: str = Field(description="Unique brief identifier")
    summary: str = Field(description="Executive summary of key items")
    action_items: list[ActionItem] = Field(default_factory=list, description="Extracted action items")

def get_executive_brief(api_token: str) -> FyxerDailyBrief:
    url = "https://api.fyxer.com/v1/brief"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    # Simulated response structure for illustration
    mock_response = json.dumps({
        "brief_id": "brief-2027-0107",
        "summary": "3 high-priority emails requiring approval; 2 meetings scheduled for today.",
        "action_items": [
            {"task": "Approve Q1 budget proposal", "source": "email", "priority": "high"},
            {"task": "Review API contract draft", "source": "meeting", "priority": "normal"}
        ]
    })
    return FyxerDailyBrief(**json.loads(mock_response))

brief = get_executive_brief("fyxer_test_token")
print(brief.model_dump_json(indent=2))
```

### FastMCP 3.1 Integration Pattern
Pattern for registering Fyxer executive brief retrieval as a FastMCP 3.1 tool service:

```python
from pydantic import BaseModel, Field

class FastMCPBriefRequest(BaseModel):
    user_id: str = Field(description="Target executive user ID")

def handle_mcp_fyxer_brief(request: FastMCPBriefRequest) -> dict:
    return {
        "status": "success",
        "user_id": request.user_id,
        "brief_summary": "Daily brief retrieved via FastMCP 3.1 adapter.",
        "pending_actions_count": 2
    }

print(handle_mcp_fyxer_brief(FastMCPBriefRequest(user_id="exec_101")))
```

## Related tools / concepts
- [tldv](tldv.md)
- [Glean](glean.md)
- [Ramp](ramp.md)
- [Coveo](coveo.md)
- [Hebbia](hebbia.md)
- [n8n](../../services/n8n.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [Fyxer AI Official Platform](https://www.fyxer.com/)
- [Fyxer AI Blog & Updates](https://www.fyxer.com/blog)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec/3.0)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
