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
- Enables autonomous local agents to interact with traditional email workflows without exposing cleartext credentials or message content to cloud gateways.

## Where it fits in the stack
- Sits in the **Enterprise Privacy & Intake Automation** layer.
- Connects local agent pipelines (via Proton Mail Bridge IMAP/SMTP) with secure cloud email storage under Swiss privacy laws.

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
|  |             (IMAP: 127.0.0.1:1143 / SMTP: 1025)             |  |
|  +-------------------------------------------------------------+  |
|                                ||                                 |
|                  Local encrypted IPC transport                    |
|                                ||                                 |
|                                \/                                 |
|  +-------------------------------------------------------------+  |
|  | FastMCP 3.1 Agent / Python Ingestion Engine                 |  |
|  | - Fetches IMAP messages & attachments                       |  |
|  | - Parses body & attachments with Pydantic v2 validation      |  |
|  | - Routes structured tasks to local downstream engines       |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
```

## Typical use cases

- **Confidential Document Ingestion**: Securely receiving sensitive contracts, medical reports, and financial statements for processing in local RAG architectures without exposing raw text to cloud email providers.
- **Privacy-Preserving Task Automation**: Ingesting user-submitted instructions, calendar invites, and service requests for automated parsing into ticket management systems (Paperless-ngx, Vikunja, JIRA).
- **Secure Executive Communication**: Protecting C-suite and research team communications against external surveillance and automated data scraping.
- **Encrypted Agent Telemetry & Alerts**: Transporting high-priority operational alerts and compliance reports across organizational security boundaries using PGP key encryption.


## Strengths

- **Unmatched Data Privacy**: Zero-access storage and zero-knowledge architecture guarantee strict data sovereignty governed by Swiss jurisdiction.
- **Open Standards Compliance**: Native support for OpenPGP (RFC 4880 / RFC 9580) and standard IMAP/SMTP protocols via Proton Mail Bridge.
- **Enterprise Productivity Integration**: Tightly integrated with Proton Calendar, Proton Drive, and Proton Pass for a complete privacy-first suite.
- **Agentic Compatibility**: Bridge daemon allows seamless integration with standard Python `imaplib`, `smtplib`, and FastMCP 3.1 agent tools without custom cryptographic libraries.


## Limitations

- **Client-Side Search Overhead**: Content search inside encrypted mailboxes requires client-side search index building, which can consume local RAM/CPU on large mailboxes.
- **Bridge Dependency for Scripts**: Programmatic headless automation requires local execution of the Proton Mail Bridge daemon.
- **Rate Limits & Anti-Spam Safeguards**: Outbound sending limits are enforced to prevent platform abuse, requiring custom SMTP domain reputation configuration for high-volume notification pipelines.


## When to use it

- When building AI document intake pipelines that process sensitive, regulated, or proprietary human communications.
- When absolute data privacy and regulatory compliance (GDPR, Swiss FADP, HIPAA compatibility) are required for executive and developer workflows.
- When you require a reliable, OpenPGP-compatible secure messaging platform integrated with desktop and server agent environments.


## When not to use it
- When you require high-volume automated marketing email blasts (use dedicated transactional email gateways like Postmark or Amazon SES).
- When native server-side CalDAV/IMAP endpoints are required without running local proxy daemons.

## Getting started

To run Proton Mail with automated local agents, install and launch the Proton Mail Bridge daemon on your server or workstation:

```bash
# Download and install Proton Mail Bridge (Debian/Ubuntu example)
wget https://proton.me/download/bridge/protonmail-bridge_3.12.0-1_amd64.deb
sudo apt-get install -y ./protonmail-bridge_3.12.0-1_amd64.deb

# Start Bridge in non-interactive CLI mode
protonmail-bridge --cli
```

Inside the CLI, run `login` to authenticate with your Proton username and password (including 2FA token), then run `info` to retrieve the randomly generated IMAP and SMTP passwords for your local client configuration.

## CLI examples

### Managing Proton Mail Bridge via CLI
```bash
# Launch protonmail-bridge in interactive terminal mode
protonmail-bridge -cli

# Inside protonmail-bridge CLI session:
>>> login
Username: user@proton.me
Password: ********************
Two-factor code: 123456
>>> info
Account: user@proton.me
  Status: Connected
  IMAP Port: 1143
  SMTP Port: 1025
  Security: STARTTLS
  Username: user@proton.me
  Password: [generated-bridge-password]

# Test local IMAP connection using openssl / nc
nc -zv 127.0.0.1 1143
```

### Inspecting Local Encrypted Attachments with GPG
```bash
# List local OpenPGP keys managed by GPG
gpg --list-secret-keys --keyid-format LONG

# Decrypt an encrypted email payload manually for verification
gpg --decrypt --quiet intake_message.pgp > decrypted_payload.eml
```

## API examples

### FastMCP 3.1 Server for Proton Mail Management
The following Python implementation provides a complete, production-ready **FastMCP 3.1** tool server that exposes encrypted email sending and intake fetching tools to autonomous agent frameworks.

```python
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from typing import List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("ProtonMailBridgeManager", version="3.1")

# ---------------------------------------------------------------------------
# Pydantic v2 Models for Encrypted Mail Operations
# ---------------------------------------------------------------------------

class EmailFetchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bridge_host: str = Field("127.0.0.1", description="Proton Mail Bridge host address")
    imap_port: int = Field(1143, ge=1, le=65535, description="Proton Mail Bridge IMAP port")
    username: EmailStr = Field(..., description="Proton Mail account username")
    bridge_password: str = Field(..., min_length=8, description="Generated Bridge password")
    mailbox: str = Field("INBOX", description="Target mailbox folder")
    unread_only: bool = Field(True, description="Filter for unread messages only")
    max_count: int = Field(10, ge=1, le=100, description="Maximum messages to retrieve")

class EmailSendRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bridge_host: str = Field("127.0.0.1", description="Proton Mail Bridge host address")
    smtp_port: int = Field(1025, ge=1, le=65535, description="Proton Mail Bridge SMTP port")
    username: EmailStr = Field(..., description="Sender Proton Mail address")
    bridge_password: str = Field(..., min_length=8, description="Generated Bridge password")
    recipient: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, max_length=256, description="Email subject line")
    body: str = Field(..., min_length=1, description="PlainText or HTML body content")

    @field_validator("subject", "body")
    @classmethod
    def sanitize_input(cls, v: str) -> str:
        return v.strip()

class IngestedMessage(BaseModel):
    message_id: str
    sender: str
    recipient: str
    subject: str
    body_text: str
    has_attachments: bool

# ---------------------------------------------------------------------------
# FastMCP 3.1 Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def fetch_proton_emails(request: EmailFetchRequest) -> List[IngestedMessage]:
    """Fetch and parse incoming emails securely from local Proton Mail Bridge."""
    messages: List[IngestedMessage] = []

    try:
        mail = imaplib.IMAP4(request.bridge_host, request.imap_port)
        mail.starttls()
        mail.login(request.username, request.bridge_password)
        mail.select(request.mailbox)

        search_criterion = 'UNSEEN' if request.unread_only else 'ALL'
        status, response = mail.search(None, search_criterion)

        if status != "OK" or not response[0]:
            mail.logout()
            return []

        msg_ids = response[0].split()[-request.max_count:]
        for msg_id in msg_ids:
            res, msg_data = mail.fetch(msg_id, "(RFC822)")
            if res != "OK":
                continue

            for part in msg_data:
                if isinstance(part, tuple):
                    raw_msg = email.message_from_bytes(part[1])
                    raw_subj, enc = decode_header(raw_msg.get("Subject", ""))[0]
                    if isinstance(raw_subj, bytes):
                        subj = raw_subj.decode(enc or "utf-8", errors="replace")
                    else:
                        subj = str(raw_subj)

                    sender = raw_msg.get("From", "")
                    recipient = raw_msg.get("To", "")
                    body = ""
                    has_attach = False

                    if raw_msg.is_multipart():
                        for subpart in raw_msg.walk():
                            ctype = subpart.get_content_type()
                            cdisp = str(subpart.get("Content-Disposition"))
                            if ctype == "text/plain" and "attachment" not in cdisp:
                                body = subpart.get_payload(decode=True).decode("utf-8", errors="replace")
                            elif "attachment" in cdisp:
                                has_attach = True
                    else:
                        body = raw_msg.get_payload(decode=True).decode("utf-8", errors="replace")

                    messages.append(IngestedMessage(
                        message_id=msg_id.decode("utf-8"),
                        sender=sender,
                        recipient=recipient,
                        subject=subj,
                        body_text=body.strip(),
                        has_attachments=has_attach
                    ))

        mail.logout()
        return messages

    except Exception as e:
        raise RuntimeError(f"IMAP Fetch Error via Proton Bridge: {str(e)}")

@mcp.tool()
def send_proton_email(request: EmailSendRequest) -> dict:
    """Dispatch an outgoing email through local Proton Mail Bridge SMTP proxy."""
    msg = MIMEMultipart()
    msg['From'] = request.username
    msg['To'] = request.recipient
    msg['Subject'] = request.subject
    msg.attach(MIMEText(request.body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP(request.bridge_host, request.smtp_port)
        server.starttls()
        server.login(request.username, request.bridge_password)
        server.sendmail(request.username, request.recipient, msg.as_string())
        server.quit()
        return {"status": "success", "recipient": request.recipient, "subject": request.subject}
    except Exception as e:
        raise RuntimeError(f"SMTP Dispatch Error via Proton Bridge: {str(e)}")

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Guide

| Symptom / Error | Root Cause | Remediation Step |
| :--- | :--- | :--- |
| `imaplib.error: b'STARTTLS failed'` | Bridge daemon not initialized with STARTTLS or invalid SSL cert trust | Ensure `mail.starttls()` is called; configure Bridge to allow local self-signed SSL/TLS parameters. |
| `AUTHENTICATIONFAILED` | Using raw Proton account password instead of Bridge-generated password | Log into `protonmail-bridge --cli`, execute `info`, and copy the specific Bridge application password. |
| Connection Refused on `127.0.0.1:1143` | Proton Mail Bridge daemon is not running in background | Check systemd service status (`systemctl status protonmail-bridge`) or re-launch `protonmail-bridge --cli`. |
| Excessive local memory consumption | Vault client index building on large mailboxes with >50,000 emails | Compact local search index in Bridge settings or set folder split rules in Proton Web UI. |
| Outbound SMTP 451/421 rate limit | Exceeded Proton daily outgoing email limits | Throttle automated notification agent output or configure custom SMTP domain DKIM/SPF settings. |

## Operational Guardrails & Best Practices

1. **Systemd Headless Daemon Management**: Always configure Proton Mail Bridge as a restricted `systemd` user service with `Restart=always` and `PrivateTmp=true` to guarantee high availability across server reboots.
2. **Decrypted Payload Lifecycle**: Decrypted email bodies and attachments processed by FastMCP 3.1 tools must be held strictly in volatile RAM (`tmpfs`) and scrubbed immediately after RAG ingestion to preserve zero-access security boundaries.
3. **Bridge Password Vaulting**: Store generated Bridge credentials in system keyring services (e.g., `secret-service`, `kwallet`, or environment secrets encrypted via Vault) rather than hardcoding in script files.
4. **Key Pinning & OpenPGP Validation**: Ensure all incoming messages from external contacts undergo OpenPGP signature verification before parsing attachments inside automated document processing pipelines.

## Related tools / concepts

- **[Proton Calendar](../calendar_tasks/proton_calendar.md)**: Native calendar synchronization for privacy-focused scheduling and event parsing.
- **[Paperless-ngx](../../services/paperless-ngx.md)**: Automated ingestion pipeline for PDF attachments retrieved via Proton Mail Bridge.
- **[FastMCP 3.1 Multi-Agent Framework](../agents/multi-agent-systems.md)**: Encapsulate encrypted email sending and reading behind MCP tool schemas.
- **[Vault Secret Management](../automation_orchestration/vault-mcp.md)**: Secure storage for local Proton Mail Bridge application passwords.


## Sources / references

- [Proton Mail Official Security & Privacy Architecture](https://proton.me/mail/security)
- [Proton Mail Bridge Official Guide](https://proton.me/mail/bridge)
- [OpenPGP RFC Standard Specification](https://datatracker.ietf.org/doc/html/rfc9580)
- [Proton Developer Resources & Open Source Repositories](https://github.com/ProtonMail)



## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
