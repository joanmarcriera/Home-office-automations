# Radicale Automation

Automated workflows and maintenance patterns for the Radicale CalDAV/CardDAV server, optimized for the early January 2027 agentic ecosystem.

## What it is
Radicale Automation refers to the set of scripts, [n8n](n8n.md) workflows, and [FastMCP 3.1 / MCP](../tools/automation_orchestration/mcp.md) integrations used to automate calendar management, contact synchronization, and server maintenance for [Radicale](radicale.md). In early January 2027, this increasingly involves the use of autonomous agents like [Gemma 3](../tools/ai_knowledge/local_llms.md), [Llama 4](../tools/ai_knowledge/local_llms.md), [GPT-5.5](../tools/providers/index.md), [Gemini 4.0 Pro](../tools/providers/index.md), and [Claude 5.1](../tools/providers/anthropic.md) to perform natural language scheduling and contact deduplication.

## What problem it solves
It reduces the manual effort required to manage self-hosted calendars and contacts. This includes automated backups of `.ics` and `.vcf` files, syncing contacts from external sources (like CRM or social media), and setting up automated alerts for server health. It specifically addresses the "silo" problem of self-hosted data by making it accessible to modern AI agents via the [FastMCP 3.1 Specification](../tools/automation_orchestration/mcp.md).

## Where it fits in the stack
**Category**: Services / Automation. It bridges the gap between raw data storage in Radicale and actionable scheduling/contact management, acting as the integration layer for the [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) server. It sits alongside other automation tools like [n8n](n8n.md) and [Home Assistant](home-assistant.md).

## Typical use cases
- **Natural Language Scheduling**: Using [Gemma 3](../tools/ai_knowledge/local_llms.md) to book appointments by simply describing them in chat.
- **Automated Contact Enrichment**: Periodically updating contact cards with information from LinkedIn or company directories via [n8n](n8n.md).
- **Multi-Source Synchronization**: Keeping family contacts from a shared [Nextcloud](nextcloud.md) instance in sync with Radicale CardDAV.
- **Proactive Health Monitoring**: Monitoring Radicale service availability and alerting via Telegram or [Home Assistant](home-assistant.md).
- **Conflict Resolution**: Using an AI agent to identify and suggest resolutions for double-booked appointments.

## Strengths
- **Simple File Format**: Since Radicale stores data as plain text files, automation via standard filesystem tools is straightforward.
- **REST-like API**: Supports standard HTTP methods for easy integration with tools like `curl` and [n8n](n8n.md).
- **MCP Compatibility**: Seamlessly exposes data to agents via the [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md).
- **Idempotency**: Plain-text storage makes it easy to write idempotent sync scripts that don't duplicate entries.

## Limitations
- **No Native Webhooks**: Relies on polling or filesystem watchers for change detection.
- **Authentication Complexity**: Requires handling `htpasswd` or LDAP credentials in automation scripts.
- **Scaling**: While fine for individuals and families, large-scale automation may hit filesystem lock contention if multiple scripts write simultaneously.

## When to use it
- To ensure your self-hosted calendar data is regularly backed up and synchronized.
- When you need to integrate your private calendar with other automation tools like [n8n](n8n.md) or [Home Assistant](home-assistant.md).
- To enable agentic scheduling via [Claude 5.1](../tools/providers/anthropic.md) or [Gemma 3](../tools/ai_knowledge/local_llms.md).
- For maintaining a private, air-gapped scheduling system.

## When not to use it
- If you only have a single user and a single device, manual management might be sufficient.
- If you require millisecond-level real-time synchronization across hundreds of concurrent users.
- If you are already fully committed to an integrated suite like [Nextcloud](nextcloud.md) which handles its own internal automation.

## Getting started

### Prerequisites
- A running [Radicale](radicale.md) instance.
- Access to the Radicale storage directory (usually `~/.var/lib/radicale/collections`).
- (Optional) [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) for agentic access.

### Automated Backup Script
Create a simple bash script to backup your collections:

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups/radicale_$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"
cp -r ~/.var/lib/radicale/collections/* "$BACKUP_DIR"
tar -czf "${BACKUP_DIR}.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"
```

### Hello World (n8n)
1. Add an **HTTP Request** node in [n8n](n8n.md).
2. Set the Method to `PROPFIND`.
3. URL: `http://your-radicale-server:5232/user/`.
4. Authentication: Basic Auth (Radicale credentials).
5. This node will return the list of available collections in XML format.

## CLI examples

Automation often involves interacting with the filesystem or using `curl`.

```bash
# Verify all storage items for integrity via CLI
python3 -m radicale --verify-storage

# Use curl to create a new calendar collection automatically
curl -u user:pass -X MKCOL http://localhost:5232/user/new_calendar/

# List all files in a collection to check for recent changes
ls -ltr ~/.var/lib/radicale/collections/collection-data/user/

# Create a new collection for automated tasks via CalDAV (raw XML)
curl -u user:pass -X MKCOL \
     -H "Content-Type: text/xml" \
     -d '<?xml version="1.0" encoding="utf-8" ?><D:mkcol xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav"><D:set><D:prop><D:displayname>Automated Tasks</D:displayname><C:resourcetype><D:collection/><C:calendar/></C:resourcetype></D:prop></D:set></D:mkcol>' \
     "http://localhost:5232/user/automated-tasks/"
```

### Agentic Interaction via MCP
```bash
# If using the Chronos MCP server, an agent can list events:
mcp-client chronos list-events --calendar "personal" --start "2026-11-01"
```

## API examples

### Python (Syncing Contacts with Pydantic v2 Validation)
In early January 2027, programmatic interactions between AI schedulers and CardDAV/CalDAV servers are strictly typed. Below is an example validating a contact schema using **Pydantic v2** prior to putting it to Radicale:

```python
import httpx
import asyncio
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class RadicaleContactModel(BaseModel):
    first_name: str = Field(..., description="Given name of the contact")
    last_name: str = Field(..., description="Family name of the contact")
    email: EmailStr = Field(..., description="Validated primary email address")
    phone: Optional[str] = Field(None, description="Optional phone number")

    def to_vcard(self) -> str:
        """Serializes the model fields into RFC-compliant vCard v3.0 format."""
        vcard = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{self.first_name} {self.last_name}",
            f"N:{self.last_name};{self.first_name};;;",
            f"EMAIL;TYPE=INTERNET:{self.email}"
        ]
        if self.phone:
            vcard.append(f"TEL;TYPE=CELL:{self.phone}")
        vcard.append("END:VCARD")
        return "\n".join(vcard)

async def upload_contact(base_url: str, collection_path: str, contact: RadicaleContactModel, auth_tuple: tuple):
    vcard_data = contact.to_vcard()
    filename = f"{contact.first_name.lower()}-{contact.last_name.lower()}.vcf"
    target_url = f"{base_url.rstrip('/')}/{collection_path.lstrip('/')}/{filename}"

    async with httpx.AsyncClient() as client:
        response = await client.put(
            target_url,
            content=vcard_data,
            auth=auth_tuple,
            headers={"Content-Type": "text/vcard; charset=utf-8"}
        )
        response.raise_for_status()
        print(f"Uploaded contact successfully: {contact.first_name} {contact.last_name}")

async def main():
    # Instantiate and validate input via Pydantic v2
    contact = RadicaleContactModel(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        phone="+15550199"
    )

    try:
        await upload_contact(
            base_url="http://localhost:5232",
            collection_path="/user/contacts",
            contact=contact,
            auth_tuple=("user", "pass")
        )
    except Exception as e:
        print(f"Radicale automation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### curl (Exporting Calendar)
```bash
# Download a full calendar as a single .ics file for external processing
curl -u user:pass "http://localhost:5232/user/calendar/" -o my_calendar.ics
```

## Related tools / concepts
- [Radicale](radicale.md) (The core service)
- [n8n](n8n.md) (Primary automation engine)
- [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) (To expose CalDAV to AI)
- [Home Assistant](home-assistant.md) (For calendar-based triggers)
- [Nextcloud](nextcloud.md) — For federated calendar and contact synchronization.
- [Authentik](authentik.md) — For centralized authentication and identity management.
- [Vikunja](vikunja.md) — For task-based coordination often synced with Radicale.
- [Model Context Protocol](../tools/automation_orchestration/mcp.md) — Standard for agentic scheduling.

## Sources / References
- https://radicale.org/v3.html
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/
- https://agentskills.io/spec/chronos-caldav/

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
