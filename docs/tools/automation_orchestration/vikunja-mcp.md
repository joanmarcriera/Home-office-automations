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

Vikunja MCP is most commonly run on-demand using `npx` within your MCP client configuration (such as Claude Desktop).

### Authentication Setup
The server supports two authentication modes:
1. **API Token Authentication (Default)**: Best for general automation and task management. Create a token in Vikunja Settings → API Tokens. Format starts with `tk_`.
2. **JWT Authentication (Advanced)**: Enables user profile modifications and data exports. Extract the `token` key value from your browser's Local Storage for your Vikunja domain. Format starts with `eyJ`.

### 1. Installation
The server runs headless via Node.js or `npx`:

```bash
# Verify the package launches correctly
npx -y @democratize-technology/vikunja-mcp
```

### 2. Client Configuration (Claude Desktop)
Add the server configuration block to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vikunja-mcp": {
      "command": "npx",
      "args": ["-y", "@democratize-technology/vikunja-mcp"],
      "env": {
        "VIKUNJA_URL": "https://tasks.yourdomain.com/api/v1",
        "VIKUNJA_API_TOKEN": "tk_your_api_token_here"
      }
    }
  }
}
```

### Hello World Example
Test connection status by authenticating and listing your active tasks across all projects:

```bash
# Set environment variables
export VIKUNJA_URL="https://tasks.yourdomain.com/api/v1"
export VIKUNJA_API_TOKEN="tk_your_api_token"

# List tasks via MCP-compatible schema testing
npx @democratize-technology/vikunja-mcp
```

## CLI examples
You can tune the runtime environment, rate limits, and circuit breakers of the MCP server using environment flags:

```bash
# 1. Start the server with verbose debug logs written to stderr
DEBUG=true LOG_LEVEL=debug npx @democratize-technology/vikunja-mcp

# 2. Apply strict API rate limits to protect your self-hosted instance from DoS
RATE_LIMIT_ENABLED=true RATE_LIMIT_PER_MINUTE=60 npx @democratize-technology/vikunja-mcp

# 3. Connect using a browser-extracted JWT token to unlock advanced user tools
VIKUNJA_API_TOKEN="eyJhbGciOiJIUzI1..." npx @democratize-technology/vikunja-mcp
```

## API examples
The Vikunja MCP server uses structured subcommand structures.

### Creating a Recurring Task (JSON Tool Input)
AI assistants create projects, labels, and tasks by invoking registered tool definitions:

```json
{
  "name": "vikunja_tasks",
  "arguments": {
    "subcommand": "create",
    "projectId": 1,
    "title": "Weekly Security Audit",
    "description": "Perform dependency and container scans",
    "dueDate": "2026-12-01T10:00:00Z",
    "priority": 4,
    "repeatAfter": 7,
    "repeatMode": "day",
    "labels": [12]
  }
}
```

### Listing Tasks with Complex Filters
Filter tasks using SQL-like expressions executed server-side with local fallback:

```json
{
  "name": "vikunja_tasks",
  "arguments": {
    "subcommand": "list",
    "filter": "(priority >= 4 && done = false) || (dueDate < now && done = false)",
    "perPage": 10
  }
}
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
