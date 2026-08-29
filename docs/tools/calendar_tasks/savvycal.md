# SavvyCal

SavvyCal is a modern scheduling tool designed to be as "sender-friendly" as it is "recipient-friendly," allowing invitees to overlay their own calendars. As of early January 2027, it has fully integrated with the **Model Context Protocol (MCP 3.1)** and the **FastMCP 3.1 Task Protocol**, enabling AI agents like [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), DeepSeek-V4, Qwen 3.6 VL, and [Gemma 4](../ai_knowledge/local_llms.md) to manage scheduling workflows autonomously while maintaining advanced availability control.

## What it is
SavvyCal is a privacy-focused, flexible scheduling platform that aims to reduce the "scheduling dance." It provides a visual way for invitees to compare their availability with the host's without leaving the booking page, using a unique calendar overlay interface.

## What problem it solves
It solves the friction and imbalance typical of standard scheduling links. Traditional tools often feel "aggressive" or one-sided; SavvyCal restores balance by letting the recipient see their own calendar on top of yours, instantly identifying mutual gaps.

## Where it fits in the stack
**Calendar & Tasks**. It acts as the scheduling automation layer, bridging the gap between raw calendar data (Google, Outlook) and external communication (Email, Slack). It is a key component for agentic productivity stacks that require human-in-the-loop meeting coordination.

## Typical use cases
- **High-Touch Professional Scheduling**: Sales, consulting, and recruitment where recipient experience is a priority.
- **Team Scheduling**: Multi-person "Collective" or "Round Robin" scheduling for distributed teams.
- **VIP Scheduling**: Creating "secret" or one-time scheduling links for priority contacts with specific overrides.
- **Agentic Meeting Coordination**: Using an AI agent (Claude 5.6 / GPT-5.6) to check availability via FastMCP 3.1 and send a personalized SavvyCal link.

## Strengths
- **Calendar Overlay**: Recipients can see their own calendar on top of yours to find gaps instantly.
- **Availability Ranking**: Order your preferred times to encourage people to book when it suits you best.
- **Meeting Polls**: Integrated, ad-free polls for group scheduling without needing separate tools like Doodle.
- **Frequency Limits**: Robust controls to prevent calendar burnout (e.g., "max 3 meetings per day").
- **MCP 3.1 & FastMCP 3.1 Task Protocol Native**: Exposes scheduling tools to AI agents via FastMCP 3.1 for automated link generation and availability checks.

## Limitations
- **No Free Tier**: Primarily a paid service with only a trial period for individuals.
- **Niche Focus**: Specifically optimized for scheduling, not intended to be a general-purpose calendar or task manager.
- **Proprietary**: Not open-source or self-hostable.

## When to use it
- If you find standard scheduling tools too "aggressive" or one-sided.
- If you value a premium, polished experience for your meeting invitees.
- When you need advanced team scheduling features (Round Robin, Collective).
- If you want your AI agent to handle scheduling via a secure protocol like FastMCP 3.1.

## When not to use it
- If you require a free-forever scheduling solution.
- For simple internal-only scheduling where basic calendar invites suffice.
- If you strictly require open-source or local-only data storage (see [Radicale](../../services/radicale.md) or [Fastmail](fastmail.md)).

## Getting started

### Account Setup
SavvyCal is a web-based service.
1. Sign up at [SavvyCal.com](https://savvycal.com/).
2. Connect your primary calendars (Google, Microsoft, or Fastmail via JMAP).
3. Create your first "Scheduling Link" and customize the availability preferences.

### API Authentication
Generate an API key in your [SavvyCal Settings](https://savvycal.com/settings/api).

```bash
# Verify your API key using cURL
curl -i -X GET "https://api.savvycal.com/v1/me" \
  -H "Authorization: Bearer ${SAVVYCAL_API_KEY}"
```

## CLI examples
While there is no official binary, you can use `curl` for automation tasks:

```bash
# List all active scheduling links
curl -X GET "https://api.savvycal.com/v1/links?state=active" \
  -H "Authorization: Bearer ${SAVVYCAL_API_KEY}"

# List upcoming meetings for the next 7 days
curl -X GET "https://api.savvycal.com/v1/events?from=$(date +%Y-%m-%d)&to=$(date -d '+7 days' +%Y-%m-%d)" \
  -H "Authorization: Bearer ${SAVVYCAL_API_KEY}"

# Create a new, single-use scheduling link
curl -X POST "https://api.savvycal.com/v1/links" \
  -H "Authorization: Bearer ${SAVVYCAL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "One-time Consult",
    "slug": "consult-$(date +%s)",
    "type": "one_off",
    "durations": [30]
  }'
```

## API examples

### Fetching Availability with Python and Pydantic v2
This script fetches available slots for a specific link and strictly validates the returned structures using **Pydantic v2**.

```python
import os
import requests
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel, Field, ValidationError

class SavvyCalSlot(BaseModel):
    starts_at: datetime = Field(..., description="ISO 8601 start time of the available slot.")
    ends_at: datetime = Field(..., description="ISO 8601 end time of the available slot.")

class SavvyCalSlotsResponse(BaseModel):
    slots: List[SavvyCalSlot] = Field(..., description="A list of returned available time slots.")

def get_savvycal_slots(link_id: str) -> List[dict]:
    """
    Fetches and validates SavvyCal slots using Pydantic v2.
    """
    api_key = os.environ.get("SAVVYCAL_API_KEY")
    base_url = f"https://api.savvycal.com/v1/links/{link_id}/slots"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    params = {
        "from": datetime.now().strftime("%Y-%m-%d"),
        "to": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    }

    # In actual usage:
    # response = requests.get(base_url, headers=headers, params=params)
    # response.raise_for_status()
    # data = {"slots": response.json()}

    # Mocking successful API response for testing
    mock_api_data = {
        "slots": [
            {"starts_at": "2027-01-08T10:00:00Z", "ends_at": "2027-01-08T10:30:00Z"},
            {"starts_at": "2027-01-08T11:00:00Z", "ends_at": "2027-01-08T11:30:00Z"}
        ]
    }

    try:
        validated_response = SavvyCalSlotsResponse.model_validate(mock_api_data)
        print("SavvyCal slots validated successfully with Pydantic v2.")
        return [slot.model_dump() for slot in validated_response.slots]
    except ValidationError as e:
        print("Schema validation failed for SavvyCal Slots response:")
        raise e

get_savvycal_slots("link_abc123")
```

### Webhook Integration (n8n / Node.js)
SavvyCal supports webhooks for lifecycle events like `event.created` and `event.cancelled`.

```javascript
// Sample n8n Code Node for processing a SavvyCal 'event.created' webhook
const event = $json.body;

if (event.type === 'event.created') {
  return {
    summary: `New meeting: ${event.data.name}`,
    invitee: event.data.invitee.email,
    start_time: event.data.starts_at,
    meeting_link: event.data.location.url
  };
}
return null;
```

## Related tools / concepts
- [Calendly](calendly.md) — The primary market competitor.
- [Morgen](morgen.md) — Unified calendar and task manager.
- [Amie](amie.md) — Visual productivity and scheduling app.
- [n8n](../../services/n8n.md) — For advanced scheduling workflows.
- [Zapier](../automation_orchestration/zapier.md) — Official integration available.
- [Google Calendar](google_calendar.md) — Primary sync provider.
- [Microsoft To Do](microsoft-todo.md) — Can be synced via workflows.
- [Fastmail](fastmail.md) — Privacy-focused backend provider.
- [Gemma 4](../ai_knowledge/local_llms.md) — Local intelligence for scheduling.

## Sources / references
- [Official Website](https://savvycal.com/)
- [Developer Documentation](https://developers.savvycal.com/)
- [Changelog](https://savvycal.com/changelog)
- [Meeting Polls Tool](https://savvycal.com/polls)
- [SavvyCal FastMCP Server (GitHub)](https://github.com/savvycal/mcp-server)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
