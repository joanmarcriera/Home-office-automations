# Calendly

## What it is
An automated scheduling platform that eliminates the back-and-forth of emails for finding the perfect time to meet. It serves as a sophisticated front-end for calendar management, supporting complex routing and automated workflow triggers.

## What problem it solves
Solves scheduling friction by allowing others to book meetings based on your real-time availability across multiple calendars, while enforcing routing rules, buffer times, and payment requirements. It eliminates the "email tag" problem for both individuals and large sales/success teams.

## Where it fits in the stack
**Category**: Calendar & Tasks / Scheduling Automation. It acts as the public-facing gatekeeper for professional and personal availability, integrating deeply with underlying calendar providers (Google, Outlook, iCloud) and downstream CRM/Automation systems.

## Typical use cases
- **Professional Outreach**: Providing a friction-free way for external clients to book discovery calls.
- **Recruitment**: Coordinating multi-stage interviews across different team members' schedules using Round Robin or Collective events.
- **Routing Forms**: Using logic to direct invitees to specific event types or team members based on their responses.
- **Agentic Calendar Orchestration (2026)**: Using MCP 3.0 to allow autonomous agents (Gemma 3, Claude 5.1) to negotiate meeting times directly on behalf of the host.

## Strengths
- **Simplicity**: Extremely easy for both the host and the invitee to use with a polished, mobile-responsive UI.
- **Workflow Automation**: Native integrations for automated reminders, follow-ups, and payment collection (Stripe/PayPal).
- **Agentic Integration**: Deep support for AI agents through robust API v2 and native MCP 3.0 server support for agentic rescheduling.
- **Routing Logic**: Advanced ability to qualify leads before they ever reach your calendar.

## Limitations
- **Customization**: Limited branding and custom CSS on lower-tier plans.
- **Cost**: Premium features (multiple event types, routing, SSO) require a subscription that can be expensive for small teams.
- **Privacy**: Requires full read/write access to your underlying calendars, which may be a concern for some security-conscious users.
- **Cloud-Only**: No self-hosted option; requires an active internet connection and reliance on Calendly's servers.

## When to use it
- If you manage a high volume of meetings with external parties.
- When you want to qualify or route meetings based on specific criteria or team availability.
- If you need a reliable "booking page" that integrates with your CRM (Salesforce, HubSpot) and automation stack (n8n).

## When not to use it
- For internal team meetings where shared calendars are already visible (use native Google/Outlook features).
- If you prefer a more private, local-first scheduling solution like [Morgen](../calendar_tasks/morgen.md).
- When you need full control over the data and infrastructure (consider open-source alternatives like Cal.com).

## Getting started
Calendly is a cloud-based service. To get started, create an account and connect your primary calendar.

### Docker / Local Setup
As Calendly is a SaaS product, there is no self-hosted Docker image. However, you can run a local **Calendly-MCP Server** to allow your local agents to interact with the API.

```bash
# Run the Calendly MCP server using npx
npx @calendly/mcp-server --api-key <YOUR_CALENDLY_API_TOKEN>
```

### Quick Setup
1. Create an account at `calendly.com`.
2. Connect your Google, Outlook, or iCloud calendar.
3. Create your first "Event Type" (e.g., "15 Minute Discovery Call").
4. Set your availability and buffers.
5. Share your unique link: `https://calendly.com/your-username/15min`.

## CLI examples
While there is no official Calendly CLI, you can use `curl` with the API v2 or use the `calendly-cli` community tool.

```bash
# Get your User URI using curl
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
- **[SavvyCal](../calendar_tasks/savvycal.md)**: Direct competitor with better "link-less" scheduling and overlay features.
- **[Akiflow](../calendar_tasks/akiflow.md)**: For consolidating tasks and calendars into a single view.
- **[Morgen](../calendar_tasks/morgen.md)**: Privacy-focused scheduling and local-first calendar client.
- **[Amie](../calendar_tasks/amie.md)**: For a more social, unified scheduling experience.
- **[n8n](../../services/n8n.md)**: For complex scheduling automation and CRM synchronization.
- **[MCP](../automation_orchestration/mcp.md)**: The foundation for agentic scheduling in July 2026.
- **[Chronos MCP](../automation_orchestration/chronos-mcp.md)**: Orchestration layer for multi-calendar agentic scheduling.
- **[Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)**: Pattern for AI-managed availability.

## Sources / References
- [Calendly Official Site](https://calendly.com/)
- [Calendly Developer Portal (API v2)](https://developer.calendly.com/)
- [Calendly MCP Server GitHub](https://github.com/calendly/mcp-server)
- [Agentic Scheduling Benchmarks (July 2026 Update)](https://calendly.com/blog/agentic-scheduling-benchmarks)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: High
