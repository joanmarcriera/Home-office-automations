# Vikunja MCP Server

## What it is
A Model Context Protocol (MCP) server that enables AI assistants to interact with Vikunja task management instances.

## What problem it solves
It allows agents to manage tasks, projects, labels, and teams directly within a Vikunja instance, bridging the gap between AI assistants and personal/team productivity tools.

## Where it fits in the stack
**Tool / Automation**. It provides a domain-specific interface for task management operations.

## Typical use cases
- Managing personal task lists and projects via natural language.
- Automating project management workflows.
- Batch importing tasks from CSV or JSON files.
- Team collaboration and webhook-driven automation.

## Strengths
- **Subcommand-based tools**: Intuitive for AI interaction.
- **Session-based authentication**: Automatic token management.
- **Full CRUD operations**: Comprehensive task and project management.
- **Hybrid Filtering**: Combines server-side and client-side filtering for optimal performance.
- **Security features**: Zod-based input validation, DoS protection, and rate limiting.

## Limitations
- User endpoints may fail with authentication errors due to known Vikunja API issues.
- Team operations are partially implemented (get, update, members are missing).
- Saved filters are currently stored in memory only.

## When to use it
- When you use Vikunja for task management and want to integrate it with MCP-compatible AI assistants like Claude Desktop.
- When you need to automate task creation or batch import tasks into Vikunja.

## When not to use it
- When you require full team management capabilities that are not yet implemented.
- When you need persistent storage for custom filters within the MCP server itself.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Vikunja](../../services/vikunja.md)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [MCP Registry](mcp-registry.md)

## Sources / References
- [Vikunja MCP GitHub](https://github.com/democratize-technology/vikunja-mcp)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
