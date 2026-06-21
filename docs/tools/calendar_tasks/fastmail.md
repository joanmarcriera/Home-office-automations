# Fastmail

## What it is
An independent, privacy-focused email and calendar provider that serves as a high-performance alternative to Gmail and Outlook, built on modern, open standards. In June 2026, it is a leading provider for **JMAP-based** agentic workflows.

## What problem it solves
Provides a fast, ad-free, and private interface for email, calendar, and contacts without the data mining common in free services. It solves the "proprietary protocol" problem by being a primary driver of the **JMAP** protocol, ensuring high interoperability for AI agents.

## Where it fits in the stack
**Category**: Calendar & Tasks / Ecosystem Provider. It acts as the "Source of Truth" for email and scheduling data in a [de-Googled](../../playbooks/family-admin.md) stack, often interfaced via **Claude 4.8** or **GPT-5.5**.

## Typical use cases
- **Primary Communication Hub**: High-speed personal or business email and calendar hosting.
- **Privacy Management**: Using **Masked Emails** to prevent tracking across different services.
- **Agentic Mail Processing**: Leveraging JMAP for reliable, stateless interaction with email and calendar data by LLM agents via MCP 3.0.
- **Custom Domain Hosting**: Managing professional identities with advanced alias and catch-all support.

## Strengths
- **Speed**: The web and mobile interfaces are exceptionally fast and bloat-free.
- **Privacy**: No tracking or ads; data is never sold.
- **Standards-First**: Strong support for JMAP, CalDAV, and CardDAV, making it "Agent-Ready" by design.
- **Masked Email (June 2026 Update)**: Improved integration with password managers and browser-based agents for instant alias generation.

## Limitations
- **Subscription-Based**: No free tier; subscription is required for all features.
- **Collaborative Suite**: Lacks the deep "doc" and "spreadsheet" ecosystem of Google Workspace.
- **Storage Limits**: Storage is capped based on the subscription tier.

## When to use it
- If you want to "de-Google" your personal productivity stack while maintaining high performance.
- When you value privacy and open standards like **JMAP**.
- If you use custom domains and need powerful alias management.

## When not to use it
- If you require a free-forever service.
- If your workflow is deeply dependent on Google Sheets/Docs for real-time collaboration.
- If you need a fully self-hosted solution (consider [Radicale](../../services/radicale.md)).

## Getting started
The community-maintained `fastmail-cli` (Rust-based) provides a robust interface for interacting with Fastmail services.

### Installation (CLI)
```bash
# Install via Cargo
cargo install --git https://github.com/Lutra-Fs/fastmail-CLI

# Run interactive setup
fastmail setup
```

### Hello World (Masked Email)
```bash
# Create a new masked email for a specific site
fastmail masked create https://example.com --description "Batch 120 Audit"
```

## CLI examples
The `fastmail-cli` tool supports mail, contacts, calendars, and masked emails.

```bash
# List all calendars associated with the account
fastmail calendar list

# List recent emails from the 'Inbox'
fastmail mail list --mailbox Inbox --limit 10

# Create a new contact
fastmail contacts create "Jane Doe" --email "jane@example.com"
```

## API examples
Fastmail is a primary driver of the **JMAP** standard, which is much more agent-friendly than IMAP.

### Fetch Calendar Events (Python via JMAP)
This pattern is used by agents (e.g., **Claude 4.8**) to synchronize schedules without the overhead of CalDAV.
```python
import requests

api_token = "your_api_token"
url = "https://api.fastmail.com/jmap/api/"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

payload = {
    "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:calendars"],
    "methodCalls": [
        ["CalendarEvent/get", {"accountId": "primary", "limit": 10}, "0"]
    ]
}

response = requests.post(url, headers=headers, json=payload)
events = response.json()['methodResponses'][0][1]['list']
```

## Related tools / concepts
- [Apple Calendar](apple-calendar.md) — Native client often used with Fastmail.
- [Fantastical](fantastical.md) — Premium client that excels with Fastmail's performance.
- [Microsoft To Do](microsoft-todo.md) — Task management often synced alongside Fastmail.
- [Radicale](../../services/radicale.md) — Self-hosted CalDAV alternative.
- [JMAP Protocol](https://jmap.io/) — The underlying open standard for agentic mail/calendar.
- [Claude Code](../development_ops/claude-code.md) — CLI agent that can interface with JMAP APIs.
- [n8n](../../services/n8n.md) — For orchestrating email-driven AI workflows.
- [Proton Calendar](proton_calendar.md) — Alternative privacy-focused provider.

## Licensing and cost
- **Open Source**: No (Server side), but contributes to open standards.
- **Cost**: Paid (Subscription)
- **Self-hostable**: No

## Sources / References
- [Fastmail Official Site](https://www.fastmail.com/)
- [Fastmail Developer Documentation](https://www.fastmail.com/developer/)
- [JMAP Specification (June 2026 Update)](https://jmap.io/spec-mail.html)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
