# Calendly

## What it is
An automated scheduling platform that eliminates the back-and-forth of emails for finding the perfect time to meet.

## What problem it solves
Solves scheduling friction by allowing others to book meetings based on your real-time availability across multiple calendars.

## Where it fits in the stack
**Category**: Calendar & Tasks / Scheduling Automation

## Typical use cases
- Professional meeting scheduling with external clients.
- Recruitment and interview coordination.
- Managing office hours for teachers or consultants.

## Strengths
- **Simplicity**: Extremely easy for both the host and the invitee to use.
- **Workflow Automation**: Automated reminders, follow-ups, and calendar invitations.
- **Broad Integration**: Works with Google, Outlook, iCloud, and many CRMs.

## Limitations
- **Customization**: Limited branding and custom CSS on lower-tier plans.
- **Personal Use**: Can feel overly formal for casual or internal scheduling.

## When to use it
- If you manage a high volume of meetings with external parties.
- When you want to reduce the administrative overhead of scheduling.

## When not to use it
- For internal team meetings where shared calendars are already visible.
- If you prefer a more private, local-first scheduling solution.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Basic features free; advanced features paid)
- **Self-hostable**: No

## Getting started
Calendly is a cloud-based service. To get started, create an account and connect your calendar.

**Installation:**
1. Sign up at [Calendly.com](https://calendly.com/).
2. Connect your calendar (Google, Outlook, iCloud, or Exchange).

**Hello-world example:**
Create your first "Event Type" (e.g., "15 Minute Discovery Call") in the dashboard, then copy and share your unique link:
`https://calendly.com/your-username/15min`

Note: Calendly has no official public CLI documentation. CLI sections are skipped.

## API examples
Calendly provides a robust REST API (v2) for developers to integrate scheduling into their applications.

**Authentication:**
Requires a Personal Access Token or OAuth 2.0.

**Python Example (using `requests`):**
```python
import requests

API_TOKEN = "your_personal_access_token"
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Fetch information about the current user
response = requests.get("https://api.calendly.com/users/me", headers=headers)
user_data = response.json()
print(f"User Name: {user_data['resource']['name']}")

# List event types
response = requests.get("https://api.calendly.com/event_types", headers=headers)
event_types = response.json()
for et in event_types['collection']:
    print(f"Event Type: {et['name']} - {et['scheduling_url']}")
```

## Related tools / concepts
- [SavvyCal](savvycal.md)
- [Akiflow](akiflow.md)
- [Morgen](morgen.md)

## Sources / References
- [Calendly Official Site](https://calendly.com/)
- [Calendly Developer Portal (API v2)](https://developer.calendly.com/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
