# Chronos MCP

## What it is
A comprehensive Model Context Protocol (MCP) server for CalDAV calendar management, built with FastMCP 2.0.

## What problem it solves
It provides advanced calendar and event management capabilities with multi-account support, allowing AI agents to interact with any CalDAV-compliant calendar server.

## Where it fits in the stack
**Tool / Automation**. It acts as a bridge between AI assistants and calendar services.

## Typical use cases
- Scheduling and managing events across multiple CalDAV accounts.
- Searching for events using full-text or field-specific criteria.
- Managing tasks (VTODO) and journal entries (VJOURNAL).
- Bulk creation and deletion of calendar events.

## Strengths
- **Multi-account Support**: Manages multiple servers simultaneously.
- **Advanced Event Management**: Supports RRULE (recurring events), attendee management, and timezone-aware operations.
- **Advanced Search**: Features a relevance ranking algorithm and multiple match types.
- **Security**: Includes secure password storage using system keyrings and RFC-compliant validation.

## Limitations
- iCalendar format support for import/export is coming soon.
- Calendar synchronization between accounts is not yet implemented.

## When to use it
- When you need an agent to manage your calendar across different providers (e.g., Nextcloud, Fastmail, Apple iCloud).
- When you require advanced search and bulk operation capabilities for calendar data.

## When not to use it
- If your calendar provider does not support CalDAV.
- If you require immediate built-in synchronization between multiple calendar accounts.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

Chronos MCP is built with FastMCP and can be configured via a JSON configuration file for use with Claude Desktop or other MCP clients.

### 1. Installation
```bash
pip install chronos-mcp
```

### 2. Configuration (Claude Desktop)
Add the server to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chronos": {
      "command": "python",
      "args": ["-m", "chronos_mcp"],
      "env": {
        "CHRONOS_CONFIG_PATH": "/path/to/your/chronos_config.yaml"
      }
    }
  }
}
```

### 3. Server Configuration (`chronos_config.yaml`)
Define your CalDAV accounts:

```yaml
accounts:
  - name: "Personal Nextcloud"
    url: "https://nextcloud.example.com/remote.php/dav"
    username: "user"
    password_env: "NEXTCLOUD_PASSWORD"
  - name: "Fastmail"
    url: "https://caldav.fastmail.com/dav/"
    username: "user@fastmail.com"
    password_env: "FASTMAIL_APP_PASSWORD"
```

## Related tools / concepts
- [CalDAV](../intake_storage/caldav.md)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Nextcloud](../../services/nextcloud.md)
- [Fastmail](../calendar_tasks/fastmail.md)
- [Vikunja MCP](vikunja-mcp.md)
- [Vault MCP](vault-mcp.md)
- [Google Calendar](../calendar_tasks/google_calendar.md)
- [Chronos CalDAV library](https://github.com/democratize-technology/chronos-mcp)

## Sources / References
- [Chronos MCP GitHub](https://github.com/democratize-technology/chronos-mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high
