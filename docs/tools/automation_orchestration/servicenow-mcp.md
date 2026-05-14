# ServiceNow MCP Server

## What it is
ServiceNow MCP Server is a Model Context Protocol server that lets AI agents read and update ServiceNow data through MCP tools. It exposes ServiceNow's IT Service Management (ITSM) capabilities as structured tools that LLMs can invoke.

## What problem it solves
It reduces direct API wiring work when you want agents to query incidents, change requests, or scripts in ServiceNow through a standard tool interface. It abstracts the complexity of ServiceNow's Table API into a set of well-defined MCP tools.

## Where it fits in the stack
**Automation / Orchestration Tool**. It is a domain-specific MCP server used by MCP-compatible clients to bridge the gap between AI reasoning and enterprise IT operations.

## Typical use cases
- Agent-assisted incident triage against ServiceNow records
- Querying and updating tickets from coding agents
- Script include maintenance workflows in ServiceNow from agent tools
- Automated status reporting for change requests

## Strengths
- MCP-native interface for ServiceNow operations
- Supports practical record search/update workflows
- Fits existing MCP client ecosystem without custom adapters
- Simplifies authentication by centralizing it in the server process

## Limitations
- Requires ServiceNow credentials (Service Account recommended) and environment setup
- Trust boundaries and permissions must be configured carefully in ServiceNow (ACLs)
- Coverage depends on server-supported tool set and ServiceNow API access

## When to use it
- When your agent workflows already use MCP and need ServiceNow integration
- When you want standardized tool-calling for ServiceNow tasks
- For rapid prototyping of AI-driven IT support agents

## When not to use it
- When you need full ServiceNow platform automation beyond exposed MCP tools
- When governance rules require tightly curated direct API integrations only
- For high-volume data migrations (use ServiceNow IntegrationHub or direct API instead)

## Getting started

To use the ServiceNow MCP server with a client like Claude Desktop:

1. Obtain your ServiceNow instance URL, username, and password.
2. Add the server configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "servicenow": {
      "command": "npx",
      "args": ["-y", "@michaelbuckner/servicenow-mcp"],
      "env": {
        "SERVICENOW_INSTANCE_URL": "https://your-instance.service-now.com",
        "SERVICENOW_USERNAME": "your-username",
        "SERVICENOW_PASSWORD": "your-password"
      }
    }
  }
}
```

## Technical examples

### Searching for Incidents
An agent can use the `search_records` tool to find specific incidents:

```json
// Tool call from agent
{
  "name": "search_records",
  "arguments": {
    "table_name": "incident",
    "query": "active=true^priority=1",
    "limit": 5
  }
}
```

### Updating a Record
Closing an incident via tool call:

```json
// Tool call from agent
{
  "name": "update_record",
  "arguments": {
    "table_name": "incident",
    "sys_id": "87920394871023948710239487102394",
    "data": {
      "state": "7",
      "close_notes": "Resolved by AI agent through MCP server."
    }
  }
}
```

## Licensing and cost
- **Open Source**: Yes (project listed with MIT badge in registry listing)
- **Cost**: Free software; ServiceNow usage/license costs still apply
- **Self-hostable**: Yes

## Related tools / concepts
- [MCP Registry](mcp-registry.md)
- [Model Context Protocol (MCP)](mcp.md)
- [Atlassian Jira MCP Implementations](atlassian-jira-mcp.md)
- [Service Inventory](../../services/inventory.md)
- [Claude Desktop](../agents/claude-desktop.md)
- [Goose](../agents/goose.md)
- [Anthropic](../providers/anthropic.md)
- [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md)

## Sources / References
- [ServiceNow MCP Server listing](https://mcpservers.org/servers/michaelbuckner/servicenow-mcp)
- [ServiceNow MCP GitHub repository](https://github.com/michaelbuckner/servicenow-mcp)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
