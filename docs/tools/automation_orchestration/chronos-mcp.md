# Chronos MCP

## What it is
Chronos MCP is a high-performance Model Context Protocol (MCP) server for CalDAV calendar and task management. As of July 2026, it is built on **FastMCP 3.0** and supports the **MCP 3.0** Task Protocol, enabling frontier models like **Gemma 3**, Claude 4.8 Opus, and GPT-5.5 to perform deep orchestration across multiple CalDAV-compliant servers including Nextcloud, iCloud, and Fastmail.

## What problem it solves
It bridges the gap between autonomous AI agents and standard calendar protocols (RFC 4791, RFC 4918). Chronos allows agents to manage complex scheduling, task lists (VTODO), and journals (VJOURNAL) without needing bespoke integrations for every calendar provider, while maintaining high security through system-level keyring integration.

## Where it fits in the stack
**Automation & Orchestration Layer**. It serves as a specialized tool for agents requiring persistent, multi-account access to temporal and task-based data, sitting between the LLM reasoning engine and the DAV storage layer.

## Typical use cases
- **Multi-Account Orchestration**: Coordinating events between a personal Fastmail account and a corporate Nextcloud instance.
- **Agentic Task Management**: Allowing AI assistants to create, update, and prioritize VTODO tasks based on conversation context.
- **Search & Synthesis**: Performing complex, ranked searches across years of calendar data to answer "When was the last time I met with X?".
- **Automated Logging**: Using VJOURNAL entries to maintain an agentic work log or technical journal.

## Strengths
- **Native FastMCP 3.0**: Leverages the latest MCP features for improved tool discovery and type safety.
- **Advanced Search Engine**: Includes relevance-ranked search with regex and fuzzy-match capabilities.
- **Keyring Security**: Securely stores credentials using OS-native secret managers (Keychain, Windows Credential Locker).
- **Comprehensive VObject Support**: Handles Events, Tasks, and Journals with full CRUD operations.

## Limitations
- **CalDAV Only**: Does not support proprietary APIs (e.g., Google Calendar, Microsoft Graph) directly.
- **No Conflict Resolution**: Concurrent edits on the server-side may lead to standard CalDAV sync conflicts that the agent must handle.
- **Network Dependency**: Requires a stable connection to the remote CalDAV server for real-time operations.

## When to use it
- When an agent needs to manage calendars or tasks across multiple providers simultaneously.
- When you require a standardized MCP interface for CalDAV data.
- When security and credential isolation are top priorities.

## When not to use it
- For Google Workspace environments (use [Google Workspace CLI](google-workspace-cli.md) or the native Google MCP).
- If your calendar provider does not support standard CalDAV (e.g., older Outlook versions).
- For simple, non-agentic calendar access where a basic CLI or UI suffices.

## Getting started

### 1. Installation
Chronos MCP is available via `pip` with optional security features:
```bash
pip install chronos-mcp[secure]
```

### 2. Configuration
Configure accounts in `~/.chronos/accounts.yaml` or via environment variables:
```yaml
# ~/.chronos/accounts.yaml
accounts:
  - name: "Home"
    url: "https://dav.example.com/remote.php/dav"
    username: "jules"
    calendars: ["work", "personal"]
```

### 3. Execution
Start the server for your MCP client (e.g., Claude Desktop, Gemma CLI):
```bash
python -m chronos_mcp
```

## CLI examples
```bash
# Verify configuration and server health
CHRONOS_CONFIG_PATH=/path/to/config.yaml python -m chronos_mcp --check

# List all available tools in the current MCP session
mcp list-tools --server chronos-mcp

# Migrate legacy plain-text passwords to secure keyring storage
chronos-mcp-migrate-keyring
```

## API examples
Agents interact with Chronos via the following standard MCP tools:

### Create a Task (VTODO)
```json
{
  "method": "call_tool",
  "params": {
    "name": "create_task",
    "arguments": {
      "account": "Nextcloud",
      "summary": "Implement MCP 3.0 Routing Logic",
      "due": "2026-07-20T17:00:00Z",
      "priority": 1
    }
  }
}
```

### Search Events
```json
{
  "method": "call_tool",
  "params": {
    "name": "search_events",
    "arguments": {
      "query": "Project Gemma",
      "start_date": "2026-07-01",
      "end_date": "2026-07-31"
    }
  }
}
```

## Related tools / concepts
- [Model Context Protocol](mcp.md) — The underlying communication standard.
- [CalDAV](../intake_storage/caldav.md) — The target calendar protocol.
- [Nextcloud](../../services/nextcloud.md) — Common open-source CalDAV provider.
- [Fastmail](../calendar_tasks/fastmail.md) — Enterprise-grade CalDAV and email service.
- [Vikunja MCP](vikunja-mcp.md) — Specialized task management MCP server.
- [Google Workspace CLI](google-workspace-cli.md) — Comparison tool for Google ecosystems.
- [Claude Code](../development_ops/claude-code.md) — Agentic CLI that utilizes Chronos.
- [Gemma 3](../ai_knowledge/local_llms.md) — Native support for MCP 3.0 tool calling.
- [MCP Registry](mcp-registry.md) — Discover other servers.

## Sources / references
- [Chronos MCP GitHub Repository](https://github.com/democratize-technology/chronos-mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [RFC 4791 - CalDAV Specification](https://datatracker.ietf.org/doc/html/rfc4791)
- [MCP 3.0 Release Notes](../../knowledge_base/agent_protocols.md)

## Contribution Metadata
- Last reviewed: 2026-07-02
- Confidence: high
