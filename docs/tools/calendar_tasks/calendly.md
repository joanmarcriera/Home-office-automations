# Calendly

## What it is
An automated scheduling platform that eliminates the back-and-forth of emails for finding the perfect time to meet.

## What problem it solves
Solves scheduling friction by allowing others to book meetings based on your real-time availability across multiple calendars, while enforcing routing rules and buffer times.

## Where it fits in the stack
**Category**: Calendar & Tasks / Scheduling Automation. It acts as the public-facing gatekeeper for professional and personal availability.

## Typical use cases
- **Professional Outreach**: Providing a friction-free way for external clients to book discovery calls.
- **Recruitment**: Coordinating multi-stage interviews across different team members' schedules.
- **Routing Forms**: Using logic to direct invitees to specific event types or team members based on their responses.
- **AI-Managed Inbox (2026)**: Leveraging 'Callie', Calendly's AI assistant, to negotiate meeting times directly via email CC.

## Strengths
- **Simplicity**: Extremely easy for both the host and the invitee to use.
- **Workflow Automation**: Native integrations for automated reminders, follow-ups, and payment collection (Stripe/PayPal).
- **Agentic Integration**: Deep support for AI agents through robust API v2 and email-based negotiation (Callie).
- **Routing Logic**: Advanced ability to qualify leads before they ever reach your calendar.

## Limitations
- **Customization**: Limited branding and custom CSS on lower-tier plans.
- **Cost**: Premium features (multiple event types, routing) require a subscription that can be expensive for small teams.
- **Privacy**: Requires full read/write access to your underlying calendars (Google/Outlook/iCloud).

## When to use it
- If you manage a high volume of meetings with external parties.
- When you want to qualify or route meetings based on specific criteria.
- If you need a reliable "booking page" that integrates with your CRM (Salesforce, HubSpot).

## When not to use it
- For internal team meetings where shared calendars are already visible (use native Google/Outlook features).
- If you prefer a more private, local-first scheduling solution like [Morgen](morgen.md) or [Akiflow](akiflow.md).

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Basic features free; Standard/Teams plans paid)
- **Self-hostable**: No

## Getting started
Calendly is a cloud-based service. To get started, create an account and connect your primary calendar.

### Hello-world example
Create your first "Event Type" (e.g., "15 Minute Discovery Call") in the dashboard, set your availability, then copy and share your unique link:
`https://calendly.com/your-username/15min`

### AI Scheduling Assistant (Callie)
In May 2026, you can CC `callie@calendly.com` on any email thread.
- **Request**: "Hey Callie, please find a 30-minute slot for us next Tuesday afternoon."
- **Action**: Callie reads the thread, checks your real-time availability, and replies with 3 suggested slots.

## CLI examples
While there is no official Calendly CLI, you can use `curl` with the API v2 to manage your availability programmatically.

```bash
# Get your User URI
curl --request GET \
  --url https://api.calendly.com/users/me \
  --header 'Authorization: Bearer <YOUR_TOKEN>'

# List all active Event Types for your account
curl --request GET \
  --url 'https://api.calendly.com/event_types?user=<YOUR_USER_URI>' \
  --header 'Authorization: Bearer <YOUR_TOKEN>'
```

## API examples
Calendly provides a robust REST API (v2) for developers and agents.

### List Scheduled Events (Python)
This pattern is used by [n8n](../../services/n8n.md) or custom agents to trigger workflows after a meeting is booked.
```python
import requests

API_TOKEN = "your_personal_access_token"
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Fetch upcoming scheduled events
params = {
    "organization": "https://api.calendly.com/organizations/<ORG_ID>",
    "status": "active",
    "sort": "start_time:asc"
}

response = requests.get("https://api.calendly.com/scheduled_events", headers=headers, params=params)
events = response.json().get('collection', [])

for event in events:
    print(f"Meeting: {event['name']} with {event['invitees_counter']['total']} people")
    print(f"Time: {event['start_time']} - {event['end_time']}")
```

### Webhook Subscription
To react in real-time to new bookings:
```python
# Create a webhook for 'invitee.created' events
webhook_payload = {
    "url": "https://your-agent-endpoint.com/webhook",
    "events": ["invitee.created"],
    "organization": "https://api.calendly.com/organizations/<ORG_ID>",
    "scope": "organization"
}

response = requests.post("https://api.calendly.com/webhook_subscriptions",
                         headers=headers, json=webhook_payload)
```

## Related tools / concepts
- [SavvyCal](savvycal.md) — The most direct competitor with better "link-less" scheduling.
- [Akiflow](akiflow.md) — For consolidating tasks and calendars.
- [Morgen](morgen.md) — Privacy-focused scheduling and calendar client.
- [Amie](amie.md) — For a more social scheduling experience.
- [n8n](../../services/n8n.md) — For complex scheduling automation.

## Sources / References
- [Calendly Official Site](https://calendly.com/)
- [Calendly Developer Portal (API v2)](https://developer.calendly.com/)
- [AI Assistant 'Callie' Documentation](https://calendly.com/help/ai-scheduling-assistant-callie-overview)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
