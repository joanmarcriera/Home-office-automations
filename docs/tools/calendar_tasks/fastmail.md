# Fastmail

## What it is
An independent, privacy-focused email and calendar provider that serves as a high-performance alternative to Gmail and Outlook, built on modern, open standards.

## What problem it solves
Provides a fast, ad-free, and private interface for email, calendar, and contacts without the data mining common in free services. It is a primary driver of the **JMAP** protocol, ensuring high interoperability for agents and modern apps.

## Where it fits in the stack
**Category**: Calendar & Tasks / Ecosystem Provider. It acts as the "Source of Truth" for email and scheduling data in a [de-Googled](../../playbooks/family-admin.md) stack.

## Typical use cases
- **Primary Communication Hub**: High-speed personal or business email and calendar hosting.
- **Privacy Management**: Using [Masked Emails](#hello-world-masked-email) to prevent tracking across different services.
- **Agentic Mail Processing**: Leveraging JMAP for reliable, stateless interaction with email and calendar data by LLM agents.
- **Custom Domain Hosting**: Managing professional identities with advanced alias and catch-all support.

## Strengths
- **Speed**: The web and mobile interfaces are exceptionally fast and bloat-free.
- **Privacy**: No tracking or ads; data is never sold. Employs on-server encryption for mail at rest.
- **Standards-First**: Strong support for JMAP, CalDAV, and CardDAV.
- **Masked Email (2026)**: Deeply integrated with [1Password](https://1password.com/) and bitwarden for generating site-specific aliases.

## Limitations
- **Subscription-Based**: No free tier; subscription is required for all features.
- **Collaborative Suite**: Lacks the deep "doc" and "spreadsheet" ecosystem of Google Workspace.
- **Storage Limits**: While generous, storage is capped based on the subscription tier (Standard vs Professional).

## When to use it
- If you want to "de-Google" your personal productivity stack while maintaining high performance.
- When you value privacy and open standards (JMAP).
- If you use custom domains and need powerful alias management.

## When not to use it
- If you require a free-forever service.
- If your workflow is deeply dependent on Google Sheets/Docs for real-time collaboration.

## Licensing and cost
- **Open Source**: No (Server side), but contributes heavily to open-source protocols.
- **Cost**: Paid (Subscription)
- **Self-hostable**: No

## Getting started

### Installation (CLI)
The community-maintained `fastmail-cli` (Rust-based) provides a robust interface for interacting with Fastmail services.

```bash
# Install via Cargo
cargo install --git https://github.com/Lutra-Fs/fastmail-CLI

# Run interactive setup (requires an API token from Settings > Security > API Tokens)
fastmail setup
```

### Hello World (Masked Email)
Creating a masked email directly from the command line:
```bash
# Create a new masked email for a specific site
fastmail masked create https://example.com --description "Batch 109 Audit"
```

## CLI examples
The `fastmail-cli` tool supports mail, contacts, calendars, and masked emails.

```bash
# List all calendars associated with the account
fastmail calendar list

# List recent emails from the 'Inbox'
fastmail mail list --mailbox Inbox --limit 10

# List all active masked emails
fastmail masked list

# Create a new contact
fastmail contacts create "Jane Doe" --email "jane@example.com"
```

## API examples
Fastmail is a primary driver of the **JMAP** (JSON Meta Application Protocol) standard.

### Fetch Calendar Events (Python)
This pattern is used by agents to synchronize schedules without the overhead of CalDAV.
```python
import requests

api_token = "your_api_token"
url = "https://api.fastmail.com/jmap/api/"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

payload = {
    "using": [
        "urn:ietf:params:jmap:core",
        "urn:ietf:params:jmap:calendars"
    ],
    "methodCalls": [
        ["CalendarEvent/get", {
            "accountId": "primary",
            "ids": None,
            "position": 0,
            "limit": 10
        }, "0"]
    ]
}

response = requests.post(url, headers=headers, json=payload)
events = response.json()['methodResponses'][0][1]['list']
for event in events:
    print(f"Event: {event['title']} ({event['start']})")
```

### Generate Masked Email (cURL)
```bash
curl -X POST https://api.fastmail.com/jmap/api/ \
  -H "Authorization: Bearer $FASTMAIL_TOKEN" \
  -d '{
    "using": ["https://www.fastmail.com/dev/maskedemail"],
    "methodCalls": [
      ["MaskedEmail/set", {
        "create": {
          "m1": { "forDomain": "example.com", "state": "enabled" }
        }
      }, "0"]
    ]
  }'
```

## Related tools / concepts
- [Proton Calendar](proton_calendar.md) — Alternative privacy provider.
- [Radicale](../../services/radicale.md) — Self-hosted CalDAV alternative.
- [JMAP Protocol](https://jmap.io/) — The underlying open standard.
- [Apple Calendar](apple-calendar.md) — Often used as a client for Fastmail.

## Sources / References
- [Fastmail Official Site](https://www.fastmail.com/)
- [Fastmail Developer Documentation](https://www.fastmail.com/developer/)
- [JMAP Specification](https://jmap.io/spec-mail.html)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
