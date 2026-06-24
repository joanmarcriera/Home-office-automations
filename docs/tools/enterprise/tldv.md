# tl;dv

## What it is
tl;dv is an AI-powered meeting recorder and transcription tool designed for remote and hybrid teams. It integrates with platforms like Zoom, Google Meet, and Microsoft Teams to capture meetings, generate transcripts, and summarize key insights.

## What problem it solves
It eliminates the need for manual note-taking and ensures that meeting knowledge is accessible and searchable across the organization. It helps in catching up on missed meetings quickly through AI-generated summaries and "clips" of important moments.

## Where it fits in the stack
**Category**: Enterprise Productivity / Meeting Intelligence

## Key Features
- **AI Agent for Meetings**: An autonomous assistant that joins meetings to handle capture, transcription, and real-time insight generation.
- **Multi-Meeting AI Insights**: Synthesizes data across multiple meetings to identify trends, recurring issues, or sentiment shifts.
- **Sales Coaching & Playbooks**: Automatically evaluates sales calls against pre-defined playbooks and provides personalized coaching scorecards.
- **Google Meet MCP**: Integration with Model Context Protocol to enhance virtual meeting features and improve context sharing.
- **AI Notes & Summaries**: Effortlessly captures and shares key information (Claude 4.7 and GPT-5.5 optimized).
- **Multi-platform Support**: Works seamlessly with major video conferencing tools (Zoom, Meet, Teams).

## Typical use cases
- **Sales Calls**: Capturing customer feedback and requirements for CRM sync.
- **Product Interviews**: Transcribing user research sessions and distilling insights.
- **Team Syncs**: Summarizing action items and decisions for stakeholders.
- **Onboarding**: Sharing recorded knowledge with new team members.

## Getting started
1.  **Install**: Add the tl;dv extension to your browser or invite the bot to your calendar.
2.  **Record**: Start your meeting and ensure tl;dv is active.
3.  **Review**: After the meeting, access the dashboard to view the transcript and AI summary.

### Integration Example
tl;dv can be integrated with [Notion](../ai_knowledge/notion-ai.md) to automatically create a database entry for every meeting.

```bash
# While the integration is typically configured via the tl;dv dashboard:
# 1. Connect your Notion workspace in tl;dv settings.
# 2. Select the database where you want meetings to be saved.
# 3. Choose the properties to sync (e.g., Summary, Action Items, Link to Clip).
```

## CLI examples
> [!NOTE]
> tl;dv is primarily a browser-based and desktop-app platform. There is no official public CLI for individual meeting management as of June 2026.

## API examples
> [!NOTE]
> tl;dv provides a REST API and Zapier integration for Professional and Enterprise users. Below is a conceptual snippet for fetching a meeting summary (2026 pattern).

```python
import requests

API_URL = "https://api.tldv.io/v1/meetings/{meeting_id}/summary"
API_KEY = "<YOUR_API_KEY>"

def get_meeting_summary(meeting_id):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(API_URL.format(meeting_id=meeting_id), headers=headers)
    return response.json()
```

## Strengths
- **Native AI Insights**: Superior summarization compared to basic transcript-only tools.
- **Deep Integration**: Seamlessly syncs meeting data with 5000+ tools via Zapier and native connectors.
- **Freemium Model**: Offers a generous free tier for individuals and small teams.

## Limitations
- **Privacy Compliance**: Recording meetings requires consent and may be restricted in certain jurisdictions.
- **Transcription Accuracy**: May struggle with heavy technical jargon, though it allows for manual correction.

## When to use it
- When you want to ensure that institutional knowledge shared during meetings is searchable and documented.
- For teams that need to share "clips" of specific meeting moments with stakeholders.
- When you want an AI assistant (Claude 4.7 or GPT-5.5 based) to automate action item extraction.

## When not to use it
- For highly confidential or sensitive discussions where recording is prohibited by policy.
- If you primarily need a real-time assistant to help *manage* your inbox and schedule (use [Fyxer AI](fyxer.md)).
- If you only need simple audio transcription for pre-recorded files (use [Whisper](../../services/whisper.md)).

## Related tools / concepts
- [Fyxer AI](fyxer.md)
- [Glean](glean.md)
- [Hebbia](hebbia.md)
- [Coveo](coveo.md)
- [Notion AI](../ai_knowledge/notion-ai.md) (Meeting notes and knowledge base)
- [Whisper](../../services/whisper.md) (Self-hosted speech-to-text)
- [n8n](../../services/n8n.md) (Workflow automation)
- [Ramp](ramp.md) (Expense management)
- [Langfuse](../process_understanding/langfuse.md) (Observability)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) (Standard for tool-agent connectivity)

## Sources / References
- [tl;dv Official Website](https://tldv.io/)
- [tl;dv Blog](https://tldv.io/blog/)
- [Google Meet MCP: The Future of Virtual Meetings](https://tldv.io/blog/google-meet-mcp/)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high
