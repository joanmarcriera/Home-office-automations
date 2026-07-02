# Vikunja MCP Server

## What it is
A Model Context Protocol (MCP) server that enables AI assistants like [Gemma 3](../ai_knowledge/local_llms.md), Claude 4.8 Opus, and GPT-5.5 to interact with Vikunja task management instances.

## What problem it solves
It allows agents to manage tasks, projects, labels, and teams directly within a Vikunja instance, bridging the gap between autonomous assistants and self-hosted productivity tools. It supports both API token and JWT authentication for varying levels of access.

## Where it fits in the stack
**Tool / Automation**. It provides a domain-specific interface for task management operations within the [MCP](mcp.md) ecosystem.

## Typical use cases
- Managing personal task lists and projects via natural language.
- Automating project management workflows in a team environment.
- Batch importing tasks from CSV or JSON files.
- Exporting project data for backup or migration.

## Strengths
- **Subcommand-based tools**: Provides an intuitive structure for AI interaction.
- **Session-based authentication**: Automatically handles token management.
- **Production-ready resilience**: Uses circuit breakers and Zod-based validation for stability.
- **MCP 3.0 Compatible**: Supports the latest Task Protocol and routing logic.

## Limitations
- User-specific endpoints require JWT authentication (browser-extracted).
- Some team operations are limited by the underlying Vikunja API.
- Webhook subscriptions for real-time updates are still in the roadmap.

## When to use it
- When you use Vikunja for task management and want to integrate it with MCP-compatible assistants.
- When you need to automate complex task creation or project hierarchy management.
- When you require secure, validated access to your task data.

## When not to use it
- If your task management system does not support the Vikunja API.
- If you require real-time push notifications from Vikunja to your agent (use webhooks directly).

## Getting started

Vikunja MCP is best used via `npx` in your MCP client configuration.

### 1. Installation
The server is typically run directly via `npx`:
```bash
npx -y @democratize-technology/vikunja-mcp
```

### 2. Authentication
Set the following environment variables:
- `VIKUNJA_URL`: Your instance API URL (e.g., `https://tasks.example.com/api/v1`)
- `VIKUNJA_API_TOKEN`: Your API token (starts with `tk_`)

### 3. Configuration (Claude Desktop)
```json
{
  "mcpServers": {
    "vikunja": {
      "command": "npx",
      "args": ["-y", "@democratize-technology/vikunja-mcp"],
      "env": {
        "VIKUNJA_URL": "https://your-vikunja.com/api/v1",
        "VIKUNJA_API_TOKEN": "tk_yourtoken"
      }
    }
  }
}
```

## CLI examples
```bash
# Start the server with debug logging
DEBUG=true LOG_LEVEL=debug npx @democratize-technology/vikunja-mcp

# Start with custom rate limiting
RATE_LIMIT_PER_MINUTE=120 npx @democratize-technology/vikunja-mcp

# Using JWT for user-management features
VIKUNJA_API_TOKEN="eyJ..." npx @democratize-technology/vikunja-mcp
```

## API examples
Agents interact with the server using the `vikunja_tasks` toolset:
```json
// Create a new task with labels and assignees
vikunja_tasks.create({
  "projectId": 1,
  "title": "Complete 2026 Audit",
  "priority": 5,
  "labels": [10, 22],
  "dueDate": "2026-06-30T12:00:00Z"
})
```

## Related tools / concepts
- [Vikunja](../../services/vikunja.md)
- [Model Context Protocol](mcp.md)
- [Nextcloud](../../services/nextcloud.md)
- [Gitea](../../services/gitea.md)
- [Paperless-ngx](../../services/paperless-ngx.md)
- [Google Calendar](../calendar_tasks/google_calendar.md)
- [MCP Registry](mcp-registry.md)
- [Chronos MCP](chronos-mcp.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Vikunja MCP GitHub](https://github.com/democratize-technology/vikunja-mcp)
- [Vikunja API Documentation](https://vikunja.io/docs/api/)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
