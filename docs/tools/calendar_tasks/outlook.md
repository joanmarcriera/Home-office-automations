# Outlook Calendar

## What it is
The calendar and scheduling component of Microsoft Outlook, integrated with the Microsoft 365 suite.

## What problem it solves
Provides professional-grade scheduling, meeting management, and resource booking integrated with email and corporate directories.

## Where it fits in the stack
**Category**: Calendar & Tasks / Personal Information Management

## Typical use cases
- Enterprise meeting scheduling
- Shared team calendars
- Resource (room) booking

## Strengths
- Deep integration with Microsoft 365 and Teams
- Robust enterprise security and compliance
- Advanced delegate and resource management

## Limitations
- Can be complex to configure outside the Microsoft ecosystem
- API access (Microsoft Graph) requires significant OAuth setup

## When to use it
- In corporate environments already using Microsoft 365
- When deep integration with Outlook email is required

## When not to use it
- For personal use cases where simpler, free alternatives suffice
- When looking for a local-first or open-source solution

## Getting started

### Microsoft Graph API (Python)
To interact with Outlook Calendar programmatically, use the `MSAL` library for authentication and the Graph API.

```python
import msal
import requests

# Configuration
client_id = 'YOUR_CLIENT_ID'
tenant_id = 'YOUR_TENANT_ID'
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["Calendars.ReadWrite"]

# Authenticate
app = msal.PublicClientApplication(client_id, authority=authority)
result = app.acquire_token_interactive(scopes=scope)

if "access_token" in result:
    # Create an event
    endpoint = "https://graph.microsoft.com/v1.0/me/events"
    event = {
        "subject": "AI Project Sync",
        "start": {"dateTime": "2026-06-01T10:00:00", "timeZone": "UTC"},
        "end": {"dateTime": "2026-06-01T11:00:00", "timeZone": "UTC"}
    }
    headers = {'Authorization': f'Bearer {result["access_token"]}'}
    response = requests.post(endpoint, json=event, headers=headers)
    print(response.json())
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (part of Microsoft 365), Free (Outlook.com)
- **Self-hostable**: No (Cloud), Yes (Exchange Server)

## Related tools / concepts
- [Google Calendar](google_calendar.md)
- [Microsoft Graph](../providers/microsoft-graph.md)
- [Proton Calendar](proton_calendar.md)
- [Microsoft To Do](microsoft-todo.md)
- [SavvyCal](savvycal.md)

## Sources / References
- [Microsoft Outlook](https://outlook.live.com/)
- [Microsoft Graph API](https://developer.microsoft.com/en-us/graph)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
