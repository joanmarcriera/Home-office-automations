# Fyxer AI

## What it is
Fyxer AI is an executive-grade AI assistant designed to manage email inboxes, schedule meetings, and automate administrative tasks for high-load professionals and leadership teams. It acts as an intelligent agentic layer over standard communication suites like Gmail and Outlook, natively powered by frontier models like Claude 5.1 and GPT-5.5.

Key capabilities include:
- **Inbox Management**: Automatically sorts and labels emails, drafts context-aware replies in the user's voice, and identifies priority items.
- **Meeting Support**: Joins virtual meetings to record, transcribe, and extract actionable notes/tasks.
- **Scheduling Assistant**: Handles back-and-forth coordination for meeting times based on calendar availability.
- **Voice Profiles**: Advanced persona modeling (Claude 5.1 and GPT-5.5 based) to ensure drafted emails sound exactly like the user.

## What problem it solves
It tackles "inbox overwhelm" and administrative friction. Unlike simple drafting tools, Fyxer acts as a full-service delegation layer, aiming to reduce the actual number of hours a human spends managing their inbox and calendar rather than just helping them write faster.

## Where it fits in the stack
**Enterprise Productivity / Administrative Layer**. It serves as an AI-first "Executive Assistant" sitting atop the primary communication stack.

## Typical use cases
- **Executive Assistance**: Managing the heavy admin load of startup founders or C-suite executives.
- **Professional Services**: Handling client intake and scheduling for consultants, lawyers, or finance professionals.
- **Team Coordination**: Scaling individual productivity within leadership-heavy industries.

## Strengths
- **Comprehensive Service**: Replaces multiple point solutions (notetakers, schedulers, draft tools) in one platform.
- **Ease of Adoption**: Designed to feel like a traditional assistant rather than a complex new app.
- **Direct ROI**: Focuses on reclaiming hours spent on admin (reported 14.5 million hours saved across user base in 2025).

## Limitations
- **Individual Focus**: Primarily built for solo professional efficiency; shared team inbox features are still maturing in late 2026.
- **Platform Dependency**: Core features require deep access to Gmail or Outlook environments.
- **Pricing**: Overage fees based on email volume can affect growing teams.

## When to use it
- When you are a high-load professional (executive, founder, partner) spending 10+ hours a week on email and scheduling.
- When you want an "AI twin" (Claude 5.1 or GPT-5.5 optimized) that can draft emails in your specific tone.
- When you need a unified assistant that handles both asynchronous (email) and synchronous (meetings) administrative tasks.

## When not to use it
- For teams that primarily communicate via [Slack](../../services/slack.md) or [Discord](../../services/discord.md) rather than email.
- If you have low administrative overhead and don't need automated meeting transcription or scheduling assistance.
- If you are on a tight budget and can't justify the per-user fee for productivity gains.

## Getting started
Fyxer is a SaaS platform that integrates directly with workspace accounts.

### Minimal Concepts
1.  **AI Inbox**: The primary interface where Fyxer-processed mail is managed.
2.  **Voice Profile**: The learned persona Fyxer uses to draft emails that sound like the user.
3.  **Fyxer Bot**: The meeting assistant that joins calendar invites.

### Getting started example
To start with Fyxer, a user typically connects their Google Workspace or Outlook account. Fyxer then begins "training" on their sent emails to build a voice profile.

```bash
# While Fyxer is primarily a GUI platform, users can interact with
# its meeting assistant via simple calendar invites.
# To have Fyxer join a meeting, simply add 'assistant@fyxer.com'
# as a guest to your calendar event.
```

### Licensing and cost (Late August 2026)
- **Starter**: ~$30/user/month (annual).
- **Professional**: ~$50/user/month (annual).
- **Enterprise**: Custom pricing with SSO and SCIM support.
- **Trial**: Offers a 7-day free trial.

## CLI examples
> [!NOTE]
> Fyxer AI is a managed assistant service and does not provide an official public CLI for individual users as of late August 2026. However, enterprise developers can leverage simple CLI commands using curl to trigger manual webhook synchronization of voice profiles.

### Synchronize Voice Profile
```bash
curl -X POST "https://api.fyxer.com/v1/voice/sync" \
  -H "Authorization: Bearer $FYXER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profile_id": "prof_voice_098", "sync_source": "sent_emails"}'
```

## API examples

### Python (Fetching Daily Brief)
Fyxer AI provides a REST API for enterprise partners. Below is a programmatic snippet demonstrating fetching a consolidated executive briefing.

```python
import json
import urllib.request

# Fetch Fyxer daily brief via API (2026 pattern)
API_URL = "https://api.fyxer.com/v1/brief"
API_TOKEN = "<YOUR_FYXER_API_TOKEN>"

def fetch_daily_brief():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(API_URL, headers=headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

## Related tools / concepts
- [tldv](tldv.md)
- [Glean](glean.md)
- [Ramp](ramp.md)
- [Coveo](coveo.md)
- [Hebbia](hebbia.md)
- [Notion AI](../ai_knowledge/notion-ai.md)
- [Perplexity](../providers/perplexity.md)
- [n8n](../../services/n8n.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / References
- [Fyxer AI Blog](https://www.fyxer.com/blog)
- [Official Fyxer Site](https://www.fyxer.com/)
- [Fyxer x ChatGPT Integration](https://www.fyxer.com/blog/fyxer-app-chatgpt)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
