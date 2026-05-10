# tl;dv

## What it is
tl;dv is an AI-powered meeting recorder and transcription tool designed for remote and hybrid teams. It integrates with platforms like Zoom, Google Meet, and Microsoft Teams to capture meetings, generate transcripts, and summarize key insights.

## What problem it solves
It eliminates the need for manual note-taking and ensures that meeting knowledge is accessible and searchable across the organization. It helps in catching up on missed meetings quickly through AI-generated summaries and "clips" of important moments.

## Where it fits in the stack
**Category**: Enterprise Productivity / Meeting Intelligence

## Typical use cases
- **Sales Calls**: Capturing customer feedback and requirements.
- **Product Interviews**: Transcribing user research sessions.
- **Team Syncs**: Summarizing action items and decisions for stakeholders.
- **Onboarding**: Sharing recorded knowledge with new team members.

## Strengths
- **Multi-platform Support**: Works seamlessly with major video conferencing tools.
- **AI Summarization**: Automatically extracts action items and key takeaways.
- **Deep Integration**: Syncs meeting insights with CRM and project management tools (e.g., Notion, Slack, Salesforce).
- **Freemium Model**: Offers a generous free tier for individuals and small teams.

## Limitations
- **Privacy Compliance**: Recording meetings requires consent and may be restricted in certain jurisdictions or industries.
- **Transcription Accuracy**: May struggle with technical jargon or heavy accents, though it allows for manual correction.

## When to use it
- When you want to ensure that institutional knowledge shared during meetings is searchable and documented.
- For teams that need to share "clips" of specific meeting moments with stakeholders who couldn't attend the full session.
- When you want to automate the extraction of action items and sync them directly to your CRM or project management tool.

## When not to use it
- For highly confidential or sensitive discussions where recording and cloud-based transcription are prohibited by policy.
- If you primarily need a real-time assistant to help *manage* your inbox and schedule (use [Fyxer AI](fyxer.md) instead).
- If you only need simple audio transcription for pre-recorded files without the meeting platform integration (use [Whisper](../../services/whisper.md) or [Audiobookshelf](../../services/audiobookshelf.md) for self-hosting).

## Getting started
1.  **Install**: Add the tl;dv extension to your browser or invite the bot to your calendar.
2.  **Record**: Start your meeting and ensure tl;dv is active.
3.  **Review**: After the meeting, access the dashboard to view the transcript and AI summary.

### Integration Example
tl;dv can be integrated with [Notion](../../ai_knowledge/notion-ai.md) to automatically create a database entry for every meeting.

```bash
# While the integration is typically configured via the tl;dv dashboard:
# 1. Connect your Notion workspace in tl;dv settings.
# 2. Select the database where you want meetings to be saved.
# 3. Choose the properties to sync (e.g., Summary, Action Items, Link to Clip).
```

## Pricing
- **Free**: Unlimited recordings and transcripts for individuals.
- **Pro**: Advanced AI features, CRM integrations, and team collaboration tools.
- **Enterprise**: Custom security, SSO, and dedicated support.

## Related tools / concepts
- [Fyxer AI](fyxer.md)
- [Glean](glean.md)
- [Hebbia](hebbia.md)
- [Otter.ai](https://otter.ai/)
- [Notion AI](../../ai_knowledge/notion-ai.md) (Meeting notes and knowledge base)
- [Whisper](../../services/whisper.md) (Self-hosted speech-to-text)
- [n8n](../../services/n8n.md) (Workflow automation for meeting data)
- [Ramp](ramp.md) (Expense management for SaaS subscriptions)
- [Langfuse](../process_understanding/langfuse.md) (Observability for AI services)

## Sources / References
- [tl;dv Official Website](https://tldv.io/)
- [Top AI Productivity Tools (Reddit)](https://www.reddit.com/r/Anthropic/comments/1orkcqt/top_ai_productivity_tools/)

## Contribution Metadata
- Last reviewed: 2026-05-10
- Confidence: high
