# Radicale Automation

Automated workflows and maintenance patterns for the Radicale CalDAV/CardDAV server.

## What it is
Radicale Automation refers to the set of scripts, n8n workflows, and configuration patterns used to automate calendar management, contact synchronization, and server maintenance for [Radicale](radicale.md).

## What problem it solves
It reduces the manual effort required to manage self-hosted calendars and contacts. This includes automated backups of `.ics` and `.vcf` files, syncing contacts from external sources (like CRM or social media), and setting up automated alerts for server health.

## Where it fits in the stack
**Category**: Services / Automation. It bridges the gap between raw data storage in Radicale and actionable scheduling/contact management.

## Typical use cases
- Automated nightly backup of calendar and contact files to off-site storage.
- Synchronizing family contacts from a shared spreadsheet into Radicale CardDAV.
- Automatically creating calendar events in Radicale based on incoming emails (via n8n).
- Monitoring Radicale service availability and alerting via Telegram.

## Strengths
- **Simple File Format**: Since Radicale stores data as plain text files, automation via standard filesystem tools is straightforward.
- **REST-like API**: Supports standard HTTP methods for easy integration with tools like `curl` and n8n.
- **Python-Based**: Easy to extend with custom Python scripts.

## Limitations
- **No Native Webhooks**: Relies on polling or filesystem watchers for change detection.
- **Authentication Complexity**: Requires handling `htpasswd` or LDAP credentials in automation scripts.

## When to use it
- To ensure your self-hosted calendar data is regularly backed up and synchronized.
- When you need to integrate your private calendar with other automation tools like n8n or Home Assistant.

## When not to use it
- If you only have a single user and a single device, manual management might be sufficient.

## Getting started

### Prerequisites
- A running [Radicale](radicale.md) instance.
- Access to the Radicale storage directory (usually `~/.var/lib/radicale/collections`).

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
1. Add an **HTTP Request** node in n8n.
2. Set the Method to `PROPFIND`.
3. URL: `http://your-radicale-server:5232/user/`.
4. Authentication: Basic Auth (Radicale credentials).
5. This node will return the list of available collections, serving as a starting point for more complex scheduling automations.

## CLI examples

Automation often involves interacting with the filesystem or using `curl`.

```bash
# Verify all storage items for integrity via CLI
python3 -m radicale --verify-storage

# Use curl to create a new calendar collection automatically
curl -u user:pass -X MKCOL http://localhost:5232/user/new_calendar/

# List all files in a collection to check for recent changes
ls -ltr ~/.var/lib/radicale/collections/collection-data/user/
```

## API examples

### Python (Syncing Contacts)
```python
import requests

# Example of pushing a new VCard to Radicale
url = "http://localhost:5232/user/contacts/new-contact.vcf"
vcard_data = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
N:Doe;John;;;
EMAIL;TYPE=INTERNET:john.doe@example.com
END:VCARD"""

response = requests.put(
    url,
    data=vcard_data,
    auth=("user", "pass"),
    headers={"Content-Type": "text/vcard"}
)
print(f"Status Code: {response.status_code}")
```

### curl (Exporting Calendar)
```bash
# Download a full calendar as a single .ics file for external processing
curl -u user:pass "http://localhost:5232/user/calendar/" -o my_calendar.ics
```

## Related tools / concepts
- [Radicale](radicale.md) (The core service)
- [n8n](n8n.md) (Primary automation engine)
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) (To expose CalDAV to AI)
- [Rclone Automation](rclone-automation.md) (For cloud backups)
- [Home Assistant](home-assistant.md) (For calendar-based triggers)

## Sources / References
- https://radicale.org/v3.html
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-12
