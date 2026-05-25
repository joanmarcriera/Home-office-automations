# SavvyCal

## What it is
A modern scheduling tool designed to be as "sender-friendly" as it is "recipient-friendly," allowing invitees to overlay their own calendars.

## What problem it solves
Reduces the "scheduling dance" by providing a visual way for invitees to compare their availability with the host's, without leaving the booking page.

## Where it fits in the stack
**Category**: Calendar & Tasks / Scheduling Automation

## Typical use cases
- High-touch professional scheduling where recipient experience is prioritized.
- Multi-person "Collective" or "Round Robin" scheduling.
- Creating "secret" scheduling links for specific priority contacts.

## Strengths
- **Calendar Overlay**: Recipients can see their own calendar on top of yours to find gaps instantly.
- **Flexibility**: Deep controls over meeting durations, buffers, and rank-ordered availability.
- **Integration**: Strong support for Stripe, Zoom, and most major calendar providers.

## Limitations
- **No Free Tier**: Primarily a paid service with only a trial period.
- **Niche Focus**: Specifically optimized for scheduling, not a general-purpose calendar.

## When to use it
- If you find standard scheduling tools too "aggressive" or one-sided.
- If you value a premium, polished experience for your meeting invitees.

## When not to use it
- If you need a free-forever scheduling solution.
- For simple internal scheduling.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription)
- **Self-hostable**: No

## Getting started

### Installation
SavvyCal is a web-based service. There is no official CLI, but it provides a robust REST API for automation.

### Hello World (API Check)
Verify your API key using cURL:

```bash
curl -i -X GET "https://api.savvycal.com/v1/me" \
  -H "Authorization: Bearer ${SAVVYCAL_API_KEY}"
```

## CLI examples
Since there is no official CLI, you can use `curl` or a custom script to interact with the API.

```bash
# List all active scheduling links
curl -X GET "https://api.savvycal.com/v1/links?state=active" \
  -H "Authorization: Bearer ${SAVVYCAL_API_KEY}"

# List upcoming meetings
curl -X GET "https://api.savvycal.com/v1/events" \
  -H "Authorization: Bearer ${SAVVYCAL_API_KEY}"

# Create a new scheduling link via API
curl -X POST "https://api.savvycal.com/v1/links" \
  -H "Authorization: Bearer ${SAVVYCAL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Quick Sync", "slug": "quick-sync", "durations": [15, 30]}'
```

## API examples

### Fetching Availability (Python)
```python
import requests

api_key = "your_api_key"
link_id = "link_abc123"
url = f"https://api.savvycal.com/v1/links/{link_id}/slots"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

params = {
    "from": "2026-06-01",
    "to": "2026-06-07"
}

response = requests.get(url, headers=headers, params=params)
slots = response.json()

for slot in slots:
    print(f"Available: {slot['starts_at']}")
```

### Webhook Integration (Node.js)
SavvyCal can send webhooks for events like `event.created`.

```javascript
const express = require('express');
const app = express();

app.post('/webhooks/savvycal', express.json(), (req, res) => {
  const event = req.body;

  if (event.type === 'event.created') {
    console.log(`New meeting booked by ${event.data.invitee.email}`);
  }

  res.status(200).end();
});

app.listen(3000);
```

## Related tools / concepts
- [Calendly](calendly.md)
- [Morgen](morgen.md)
- [Amie](amie.md)
- [OAuth2 Authentication](https://developers.savvycal.com/api/authentication)

## Sources / References
- [SavvyCal Official Site](https://savvycal.com/)
- [SavvyCal Developer Documentation](https://developers.savvycal.com/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
