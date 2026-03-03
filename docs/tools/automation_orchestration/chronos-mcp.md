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

## Related tools / concepts
- [CalDAV](https://tools.ietf.org/html/rfc4791)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Chronos CalDAV library](https://github.com/democratize-technology/chronos-mcp)

## Sources / References
- [Chronos MCP GitHub](https://github.com/democratize-technology/chronos-mcp)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
