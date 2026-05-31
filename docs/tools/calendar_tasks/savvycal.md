# SavvyCal

SavvyCal is a modern scheduling tool designed to be as "sender-friendly" as it is "recipient-friendly," allowing invitees to overlay their own calendars. As of May 2026, it remains a top-tier choice for professionals who prioritize guest experience and advanced availability control.

## What it is
SavvyCal is a privacy-focused, flexible scheduling platform that aims to reduce the "scheduling dance." It provides a visual way for invitees to compare their availability with the host's without leaving the booking page, using a unique calendar overlay interface.

## What problem it solves
It solves the friction and imbalance typical of standard scheduling links. Traditional tools often feel "aggressive" or one-sided; SavvyCal restores balance by letting the recipient see their own calendar on top of yours, instantly identifying mutual gaps.

## Where it fits in the stack
- **Category**: [Calendar & Tasks](../calendar_tasks/index.md) / Scheduling Automation
- **Layer**: [Productivity & Operations](../../architecture/README.md)

## Typical use cases
- **High-Touch Professional Scheduling**: Sales, consulting, and recruitment where recipient experience is a priority.
- **Team Scheduling**: Multi-person "Collective" or "Round Robin" scheduling for distributed teams.
- **VIP Scheduling**: Creating "secret" or one-time scheduling links for priority contacts with specific overrides.
- **Workflow Automation**: Automating meeting lifecycle messages (reminders, follow-ups) directly within the app.

## Strengths
- **Calendar Overlay**: Recipients can see their own calendar on top of yours to find gaps instantly.
- **Availability Ranking**: Order your preferred times to encourage people to book when it suits you best.
- **Meeting Polls**: Integrated, ad-free polls for group scheduling without needing separate tools like Doodle.
- **Frequency Limits**: Robust controls to prevent calendar burnout (e.g., "max 3 meetings per day").
- **Clustered Meetings**: Encourages booking near existing appointments to preserve blocks of deep work.

## Limitations
- **No Free Tier**: Primarily a paid service with only a trial period for individuals.
- **Niche Focus**: Specifically optimized for scheduling, not intended to be a general-purpose calendar or task manager.
- **Proprietary**: Not open-source or self-hostable.

## When to use it
- If you find standard scheduling tools too "aggressive" or one-sided.
- If you value a premium, polished experience for your meeting invitees.
- When you need advanced team scheduling features (Round Robin, Collective).

## When not to use it
- If you require a free-forever scheduling solution.
- For simple internal-only scheduling where basic calendar invites suffice.
- If you strictly require open-source or local-only data storage.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription-based, typically starting around $12/user/month).
- **Self-hostable**: No

## Getting started

### Installation
SavvyCal is a web-based service. There is no official CLI, but it provides a robust REST API for automation. You can integrate it into your homelab stack via webhooks or API calls.

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

### Fetching Availability (Python)
This script fetches available slots for a specific link to use in custom dashboarding.

```python
import requests
import os
from datetime import datetime, timedelta

API_KEY = os.environ.get("SAVVYCAL_API_KEY")
LINK_ID = "link_abc123" # Replace with actual Link ID
BASE_URL = f"https://api.savvycal.com/v1/links/{LINK_ID}/slots"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

# Check availability for the next 48 hours
params = {
    "from": datetime.now().strftime("%Y-%m-%d"),
    "to": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
}

response = requests.get(BASE_URL, headers=headers, params=params)
if response.status_code == 200:
    slots = response.json()
    for slot in slots:
        print(f"Available Slot: {slot['starts_at']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
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

## Links
- [Official Website](https://savvycal.com/)
- [Developer Documentation](https://developers.savvycal.com/)
- [Changelog](https://savvycal.com/changelog)
- [Meeting Polls Tool](https://savvycal.com/polls)

## Backlog
- [x] Perform quarterly technical freshness audit (May 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-31

## Sources / References
- https://savvycal.com/features
- https://developers.savvycal.com/api
- https://savvycal.com/changelog
- KnowledgeOps Triage (2026-05-31)
