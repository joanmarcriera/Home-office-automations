# Proton Mail

## What it is

- **Zero-Access Encryption at Rest**: Emails and attachments are encrypted on the client device using asymmetric keys before reaching Proton servers; Proton AG has zero technical ability to decrypt mailbox contents.
- **End-to-End Encryption (E2EE)**: Automatic OpenPGP encryption for all communication between Proton Mail accounts and seamless PGP key signing/verification for external email standard interactions.
- **Proton Mail Bridge**: Local desktop and server background daemon exposing standard IMAP and SMTP endpoints for encrypted local communication with applications, desktop clients (Thunderbird, Apple Mail), and Python automation agents.
- **Enterprise Identity & Security**: Custom domain support, hardware security keys (FIDO2/WebAuthn), organization admin controls, anti-phishing safeguards, and strict compliance under Swiss data protection laws (FADP and Swiss GDPR alignment).
- **FastMCP 3.1 & Agentic Ingestion**: Encrypted intake channel for AI document parsers, automated task extractors, and privacy-first executive agentic assistants.


## What problem it solves
- Solves the security and compliance risk of handling confidential communications, sensitive document attachments, and proprietary prompt templates on unencrypted email servers.
- Prevents unauthorized data scraping and surveillance by enforcing client-side zero-access encryption.

## Where it fits in the stack
- Sits in the **Enterprise Privacy & Intake Automation** layer.
- Connects local agent pipelines (via Proton Mail Bridge IMAP/SMTP) with secure cloud email storage under Swiss privacy laws.

## Typical use cases

- **Confidential Document Ingestion**: Securely receiving sensitive contracts, medical reports, and financial statements for processing in local RAG architectures without exposing raw text to cloud email providers.
- **Privacy-Preserving Task Automation**: Ingesting user-submitted instructions, calendar invites, and service requests for automated parsing into ticket management systems (Paperless-ngx, Vikunja, JIRA).
- **Secure Executive Communication**: Protecting C-suite and research team communications against external surveillance and automated data scraping.
- **Encrypted Agent Telemetry & Alerts**: Transporting high-priority operational alerts and compliance reports across organizational security boundaries using PGP key encryption.


## Strengths

- **Unmatched Data Privacy**: Zero-access storage and zero-knowledge architecture guarantee strict data sovereignty governed by Swiss jurisdiction.
- **Open Standards Compliance**: Native support for OpenPGP (RFC 4880 / RFC 9580) and standard IMAP/SMTP protocols via Proton Mail Bridge.
- **Enterprise Productivity Integration**: Tightly integrated with Proton Calendar, Proton Drive, and Proton Pass for a complete privacy-first suite.


## Limitations

- **Client-Side Search Overhead**: Content search inside encrypted mailboxes requires client-side search index building, which can consume local RAM/CPU on large mailboxes.
- **Bridge Dependency for Scripts**: Programmatic headless automation requires local execution of the Proton Mail Bridge daemon.
- **Rate Limits & Anti-Spam Safeguards**: Outbound sending limits are enforced to prevent platform abuse, requiring custom SMTP domain reputation configuration for high-volume notification pipelines.


## When to use it

- When building AI document intake pipelines that process sensitive, regulated, or proprietary human communications.
- When absolute data privacy and regulatory compliance (GDPR, Swiss FADP, HIPAA compatibility) are required for executive and developer workflows.
- When you require a reliable, OpenPGP-compatible secure messaging platform integrated with desktop and server agent environments.


## When not to use it
- When you require high-volume automated marketing email blasts (use dedicated transactional email gateways).
- When native server-side CalDAV/IMAP endpoints are required without running local proxy daemons.

## Getting started

```
+-------------------------------------------------------------------+
|                        Proton Cloud                               |
|   +-----------------------------------------------------------+   |
|   | Encrypted Mailbox (Zero-Access Storage / Swiss Servers)   |   |
|   +-----------------------------------------------------------+   |
+-------------------------------------------------------------------+
                                 ||
                 Encrypted IMAP/SMTP over TLS / E2EE
                                 ||
                                 \/
+-------------------------------------------------------------------+
| Host / Server Environment                                         |
|                                                                   |
|  +-------------------------------------------------------------+  |
|  |                  Proton Mail Bridge Daemon                  |  |
|  +-------------------------------------------------------------+  |
|                                ||                                 |
|                  Local localhost:1143 (IMAP)                      |
|                  Local localhost:1025 (SMTP)                      |
|                                ||                                 |
|                                \/                                 |
|  +-------------------------------------------------------------+  |
|  | FastMCP 3.1 Agent / Python Ingestion Engine                 |  |
|  | - Fetches IMAP messages                                     |  |
|  | - Parses body & attachments with Pydantic v2 validation      |  |
|  | - Routes structured tasks to local downstream engines       |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
```


## CLI examples



## API examples

The following Python example demonstrates connecting to a local Proton Mail Bridge instance via IMAP, retrieving incoming encrypted intake messages, and validating the extracted email payload using strict **Pydantic v2** schemas.

```python
import imaplib
import email
from email.header import decode_header
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

# ---------------------------------------------------------------------------
# Pydantic v2 Email Message Schema
# ---------------------------------------------------------------------------
class IngestedEmailPayload(BaseModel):
    message_id: str = Field(..., description="Unique IMAP or Message-ID string")
    sender: str = Field(..., description="Sender email address")
    subject: str = Field(..., description="Decoded email subject line")
    body_text: str = Field(..., description="Extracted plain text body content")
    has_attachments: bool = Field(default=False, description="Whether message contains file attachments")

    @field_validator("subject", "body_text")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

# ---------------------------------------------------------------------------
# Proton Mail Bridge IMAP Ingestion Engine
# ---------------------------------------------------------------------------
class ProtonMailIngestor:
    def __init__(self, host: str = "127.0.0.1", port: int = 1143, username: str = "", password: str = ""):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def fetch_unread_intake(self) -> List[IngestedEmailPayload]:
        """Fetch and validate unread email intake from local Proton Mail Bridge."""
        results: List[IngestedEmailPayload] = []

        # Connect to Proton Mail Bridge IMAP proxy
        mail = imaplib.IMAP4(self.host, self.port)
        mail.starttls()
        mail.login(self.username, self.password)
        mail.select("INBOX")

        status, response = mail.search(None, 'UNSEEN')
        if status != "OK":
            mail.logout()
            return results

        msg_ids = response[0].split()
        for msg_id in msg_ids:
            res, msg_data = mail.fetch(msg_id, "(RFC822)")
            if res != "OK":
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    raw_msg = email.message_from_bytes(response_part[1])

                    # Decode subject line
                    raw_subject, encoding = decode_header(raw_msg.get("Subject", ""))[0]
                    if isinstance(raw_subject, bytes):
                        subject = raw_subject.decode(encoding or "utf-8", errors="replace")
                    else:
                        subject = str(raw_subject)

                    sender = raw_msg.get("From", "unknown@domain.com")
                    body = ""
                    has_attach = False

                    if raw_msg.is_multipart():
                        for part in raw_msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                            elif "attachment" in content_disposition:
                                has_attach = True
                    else:
                        body = raw_msg.get_payload(decode=True).decode("utf-8", errors="replace")

                    payload = IngestedEmailPayload(
                        message_id=msg_id.decode("utf-8"),
                        sender=sender,
                        subject=subject,
                        body_text=body,
                        has_attachments=has_attach
                    )
                    results.append(payload)

        mail.logout()
        return results

if __name__ == "__main__":
    # Demonstration instantiation (requires active local Proton Mail Bridge)
    print("Proton Mail Ingestion module ready.")
```


## Related tools / concepts

- **[Proton Calendar](../calendar_tasks/proton_calendar.md)**: Native calendar synchronization for privacy-focused scheduling and event parsing.
- **[Paperless-ngx](../intake_storage/paperless-ngx.md)**: Automated ingestion pipeline for PDF attachments retrieved via Proton Mail Bridge.
- **[FastMCP 3.1 Multi-Agent Framework](../agents/multi-agent-systems.md)**: Encapsulate encrypted email sending and reading behind MCP tool schemas.


## Sources / references

- [Proton Mail Official Security & Privacy Architecture](https://proton.me/mail/security)
- [Proton Mail Bridge Official Guide](https://proton.me/mail/bridge)
- [OpenPGP RFC Standard Specification](https://datatracker.ietf.org/doc/html/rfc9580)
- [Proton Developer Resources & Open Source Repositories](https://github.com/ProtonMail)



## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
