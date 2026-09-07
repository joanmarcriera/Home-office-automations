# Fastmail

## What it is
An independent, privacy-focused email and calendar provider that serves as a high-performance alternative to Gmail and Outlook, built on modern, open standards. As of early 2027, it is a leading provider for **JMAP-based** agentic workflows, often orchestrated via **Chronos MCP** or **FastMCP 3.1** servers with native support for task protocol execution and structured data schemas.

## What problem it solves
Provides a fast, ad-free, and private interface for email, calendar, and contacts without the data mining common in free services. It solves the "proprietary protocol" problem by being a primary driver of the **JMAP** standard, ensuring seamless interoperability for autonomous AI agents.

## Where it fits in the stack
**Category**: Calendar & Tasks / Ecosystem Provider. It acts as the "Source of Truth" for email and scheduling data in a de-Googled stack, often interfaced via **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, or specialized **FastMCP 3.1** agents.

## Typical use cases
- **Primary Communication Hub**: High-speed personal or business email and calendar hosting.
- **Privacy Management**: Using **Masked Emails** to prevent tracking across different services.
- **Agentic Mail Processing**: Leveraging JMAP for reliable, stateless interaction with email and calendar data by LLM agents via FastMCP 3.1 Task Protocol.
- **Custom Domain Hosting**: Managing professional identities with advanced alias and catch-all support.

## Strengths
- **Speed**: The web and mobile interfaces are exceptionally fast and bloat-free.
- **Privacy**: No tracking or ads; data is never sold.
- **Standards-First**: Native support for JMAP, CalDAV, and CardDAV, making it "Agent-Ready" by design.
- **Masked Email**: Deep integration with password managers and browser-based agents for instant, context-aware alias generation.

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

### Quick Setup (Masked Email)
```bash
# Create a new masked email for a specific site
fastmail masked create https://example.com --description "Batch 504 Upgrade"
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
Fastmail is a primary driver of the **JMAP** standard, which provides a clean, JSON-native alternative to legacy IMAP/CalDAV protocols.

### Fetch Calendar Events with Pydantic v2 validation (Python via JMAP)
This pattern is used by autonomous agents (e.g., **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, or **DeepSeek-V4**) to synchronize schedules without the overhead of CalDAV, utilizing the **FastMCP 3.1** Task Protocol for reliable execution.

```python
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

class JMAPMethodCall(BaseModel):
    """Schema representing a structured JMAP method call."""
    method_name: str = Field(..., description="The name of the JMAP service method, e.g., 'CalendarEvent/get'.")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary arguments validated for the method.")
    client_id: str = Field(default="0", description="Client-defined unique ID to correlate response.")

class JMAPPayload(BaseModel):
    """Schema representing a complete validated JMAP request payload for Fastmail API."""
    using: List[str] = Field(
        default_factory=lambda: ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:calendars"],
        description="Standard JMAP schemas supported by Fastmail."
    )
    method_calls: List[JMAPMethodCall] = Field(..., description="The list of method calls to execute.")

def build_and_validate_jmap_request(method: str, args: Dict[str, Any]) -> dict:
    """
    Validates the JMAP request components and converts them into a compliant
    JSON payload ready for Fastmail endpoint submission.
    """
    try:
        call = JMAPMethodCall(method_name=method, arguments=args)
        payload = JMAPPayload(method_calls=[call])
        print("Successfully validated Fastmail JMAP API payload utilizing Pydantic v2:")

        # Format matching JMAP spec layout: [ ["methodName", {args}, "clientId"] ]
        method_calls_format = [
            [item.method_name, item.arguments, item.client_id]
            for item in payload.method_calls
        ]

        return {
            "using": payload.using,
            "methodCalls": method_calls_format
        }
    except ValidationError as e:
        print("JMAP Schema Validation failed:", e)
        raise

if __name__ == "__main__":
    api_token = os.environ.get("FASTMAIL_API_TOKEN", "fastmail_test_token_val")

    # Fetch top 10 calendar events
    try:
        jmap_req = build_and_validate_jmap_request(
            method="CalendarEvent/get",
            args={"accountId": "primary", "limit": 10}
        )
        print(jmap_req)
    except ValidationError:
        pass
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

## Sources / References
- [Fastmail Official Site](https://www.fastmail.com/)
- [Fastmail Developer Documentation](https://www.fastmail.com/developer/)
- [JMAP Specification Documentation](https://jmap.io/spec-mail.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
