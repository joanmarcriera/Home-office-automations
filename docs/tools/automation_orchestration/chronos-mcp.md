# Chronos MCP

## What it is
A comprehensive Model Context Protocol (MCP) server for CalDAV calendar management, built with FastMCP 2.0. It enables AI assistants like Claude 4.8 Opus and GPT-5.5 to manage events, tasks, and journals across multiple CalDAV accounts.

## What problem it solves
It provides advanced calendar management capabilities with multi-account support, allowing AI agents to interact with any CalDAV-compliant server (Nextcloud, iCloud, Fastmail, etc.). It solves the "agent-calendar gap" by exposing full CRUD operations and advanced search features.

## Where it fits in the stack
**Tool / Automation**. It acts as a bridge between frontier AI models and personal/enterprise calendar services.

## Typical use cases
- Scheduling and managing recurring events across personal and work calendars.
- Managing tasks (VTODO) and journal entries (VJOURNAL) via natural language.
- Searching for calendar data using full-text or field-specific criteria.
- Bulk creating or deleting calendar entries for project synchronization.

## Strengths
- **Multi-account Support**: Manages multiple servers and accounts simultaneously.
- **Full VTODO/VJOURNAL Support**: Comprehensive task and journal management (v2.0.0+).
- **Secure Storage**: Supports system keyring (Keychain, Windows Credential Locker) for password security.
- **Advanced Search**: Features relevance ranking and multiple match types (regex, contains, etc.).

## Limitations
- Requires a CalDAV-compliant server.
- Built-in synchronization between accounts is not yet implemented.
- iCalendar format import/export is in the roadmap.

## When to use it
- When you need an AI agent to manage calendars across different providers.
- When you require advanced search and bulk operation capabilities for CalDAV data.
- When security (system keyring) is a priority for calendar credentials.

## When not to use it
- If your calendar provider does not support CalDAV (e.g., Google Calendar use [gws](google-workspace-cli.md)).
- For simple, single-account scheduling that doesn't require an MCP interface.

## Getting started

### 1. Installation
Install via `pip`:
```bash
pip install chronos-mcp[secure]
```

### 2. Configuration
Create `~/.chronos/accounts.json` or set environment variables:
```yaml
# Example chronos_config.yaml
accounts:
  - name: "Nextcloud"
    url: "https://nextcloud.example.com/remote.php/dav"
    username: "user"
```

### 3. Run
Start the server for your MCP client:
```bash
python -m chronos_mcp
```

## CLI examples
```bash
# Start the server with a specific config path
CHRONOS_CONFIG_PATH=/path/to/config.yaml python -m chronos_mcp

# Migrate existing plain-text passwords to secure keyring
python scripts/migrate_to_keyring.py

# List all configured accounts (via MCP call)
mcp call list_accounts
```

## API examples
Agents interact with Chronos via specific tools:
```json
// Create a new task (VTODO)
create_task({
  "calendar_uid": "work",
  "summary": "Complete 2026 Freshness Audit",
  "due": "2026-06-12T23:59:59Z",
  "priority": 1
})

// Search for an event
list_events({
  "calendar_uid": "personal",
  "search_query": "Doctor appointment",
  "start_date": "2026-01-01"
})
```

## Related tools / concepts
- [CalDAV](../intake_storage/caldav.md)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Nextcloud](../../services/nextcloud.md)
- [Fastmail](../calendar_tasks/fastmail.md)
- [Vikunja MCP](vikunja-mcp.md)
- [Google Workspace CLI](google-workspace-cli.md)
- [MCP Registry](mcp-registry.md)
- [Claude Code](../development_ops/claude-code.md)

## Sources / References
- [Chronos MCP GitHub](https://github.com/democratize-technology/chronos-mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high
