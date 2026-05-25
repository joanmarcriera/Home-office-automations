# Fastmail

## What it is
An independent, privacy-focused email and calendar provider that offers a high-performance alternative to Gmail and Outlook.

## What problem it solves
Provides a fast, ad-free, and private surface for email, calendar, and contacts without the data mining common in free services.

## Where it fits in the stack
**Category**: Calendar & Tasks / Ecosystem Provider

## Typical use cases
- Primary personal or business email and calendar hosting.
- Managing custom domain email with advanced alias support.
- Synchronizing calendars across devices via standard protocols (JMAP/CalDAV).

## Strengths
- **Speed**: The web and mobile interfaces are exceptionally fast.
- **Privacy**: No tracking or ads; data is never sold.
- **Standards-First**: Strong support for JMAP, CalDAV, and CardDAV, making it easy to use with third-party clients.

## Limitations
- **Cost**: No free tier; subscription is required.
- **Ecosystem**: Lacks the deep "doc" and "spreadsheet" ecosystem of Google Workspace.

## When to use it
- If you want to "de-Google" your personal productivity stack.
- If you value speed and privacy over free services.

## When not to use it
- If you require a free-forever email and calendar service.
- If your workflow is deeply dependent on Google Sheets/Docs collaboration.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription)
- **Self-hostable**: No

## Getting started

### Installation (CLI)
The community-maintained `fastmail-cli` provides a robust interface for interacting with Fastmail services.

```bash
# Install via Cargo
cargo install --git https://github.com/Lutra-Fs/fastmail-CLI

# Run interactive setup (requires an API token from Settings > Security > API Tokens)
fastmail setup
```

### Hello World (Masked Email)
```bash
# Create a new masked email for a specific site
fastmail masked create https://example.com --description "Trial Signup"
```

## CLI examples
The `fastmail-cli` tool supports mail, contacts, calendars, and masked emails.

```bash
# List recent emails
fastmail mail list --limit 10

# List all calendars
fastmail calendar list

# Create a new contact
fastmail contacts create "Jane Doe" --email "jane@example.com"
```

## API examples
Fastmail is a primary driver of the **JMAP** (JSON Meta Application Protocol) standard.

### Minimal JMAP Session Request (cURL)
```bash
curl -X GET \
  -H "Authorization: Bearer ${FASTMAIL_API_TOKEN}" \
  -H "Content-Type: application/json" \
  https://api.fastmail.com/jmap/session
```

### Fetch Mailboxes (Python)
```python
import requests

api_token = "your_api_token"
url = "https://api.fastmail.com/jmap/api/"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

payload = {
    "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
    "methodCalls": [
        ["Mailbox/get", {"accountId": None, "ids": None}, "0"]
    ]
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

## Related tools / concepts
- [Proton Calendar](proton_calendar.md)
- [Google Calendar](google_calendar.md)
- [Radicale](../../services/radicale.md)
- [JMAP Protocol](https://jmap.io/)

## Sources / References
- [Fastmail Official Site](https://www.fastmail.com/)
- [Fastmail Developer Documentation](https://www.fastmail.com/developer/)
- [Lutra-Fs/fastmail-CLI](https://github.com/Lutra-Fs/fastmail-CLI)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
