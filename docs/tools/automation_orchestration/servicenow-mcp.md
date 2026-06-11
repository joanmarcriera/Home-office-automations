# ServiceNow MCP Server

## What it is
ServiceNow MCP Server is a Model Context Protocol server that lets AI agents read and update ServiceNow data through MCP tools. It exposes ServiceNow's IT Service Management (ITSM) capabilities as structured tools that LLMs like **Claude 4.8** and **GPT-5.5** can invoke to manage enterprise workflows.

## What problem it solves
It reduces direct API wiring work when you want agents to query incidents, change requests, or scripts in ServiceNow through a standard tool interface. It abstracts the complexity of ServiceNow's Table API into a set of well-defined MCP tools, enabling **Llama 4 Maverick** and other models to interact with enterprise systems without custom middleware.

## Where it fits in the stack
**Automation / Orchestration Tool**. It is a domain-specific MCP server used by MCP-compatible clients to bridge the gap between AI reasoning and enterprise IT operations.

## Typical use cases
- Agent-assisted incident triage against ServiceNow records
- Querying and updating tickets from coding agents
- Script include maintenance workflows in ServiceNow from agent tools
- Automated status reporting for change requests

## Strengths
- **MCP-native interface**: Standardized access for ServiceNow operations.
- **Enterprise Integration**: Supports practical record search/update workflows for ITSM.
- **Client Compatibility**: Fits existing MCP client ecosystem (Claude Desktop, Goose, etc.) without custom adapters.
- **Simplified Auth**: Centralizes authentication in the server process.

## Limitations
- **Credential Requirements**: Requires ServiceNow credentials (Service Account recommended) and environment setup.
- **Security Scoping**: Trust boundaries and permissions must be configured carefully in ServiceNow (ACLs).
- **Tool Coverage**: Coverage depends on server-supported tool set and ServiceNow API access.

## When to use it
- When your agent workflows already use MCP and need ServiceNow integration.
- When you want standardized tool-calling for ServiceNow tasks.
- For rapid prototyping of AI-driven IT support agents.

## When not to use it
- When you need full ServiceNow platform automation beyond exposed MCP tools.
- When governance rules require tightly curated direct API integrations only.
- For high-volume data migrations (use ServiceNow IntegrationHub or direct API instead).

## Getting started

### Installation
The ServiceNow MCP server is a Python-based implementation. Install it via pip:

```bash
pip install mcp-server-servicenow
```

### Configuration (Claude Desktop)
Add the server configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "servicenow": {
      "command": "python",
      "args": ["-m", "mcp_server_servicenow"],
      "env": {
        "SERVICENOW_INSTANCE_URL": "https://your-instance.service-now.com",
        "SERVICENOW_USERNAME": "your-username",
        "SERVICENOW_PASSWORD": "your-password"
      }
    }
  }
}
```

## CLI examples

### 1. Direct Execution
Run the server directly from the command line (requires environment variables set):
```bash
SERVICENOW_INSTANCE_URL=... SERVICENOW_USERNAME=... SERVICENOW_PASSWORD=... python -m mcp_server_servicenow
```

### 2. Inspector Testing
Use the MCP Inspector to test the server's tools:
```bash
npx @modelcontextprotocol/inspector python -m mcp_server_servicenow
```

### 3. Tool Discovery
Check available tools using the MCP CLI:
```bash
mcp-cli list-tools --command python --args "-m mcp_server_servicenow"
```

## API examples

### Searching for Incidents
An agent (e.g., **Claude 4.8**) can use the `search_records` tool:

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
Closing an incident via tool call from **GPT-5.5**:

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

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) — The underlying protocol.
- [MCP Registry](mcp-registry.md) — Directory of other enterprise MCP servers.
- [Atlassian Jira MCP Implementations](atlassian-jira-mcp.md) — Similar integration for Jira.
- [Claude Desktop](../agents/claude-desktop.md) — A primary client for this server.
- [Goose](../agents/goose.md) — An agent that can use ServiceNow tools.
- [Anthropic](../providers/anthropic.md) — Creators of the MCP standard.
- [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md) — Common schema for agent tasks.
- [Service Inventory](../../services/inventory.md) — Context for enterprise services.

## Sources / references
- [ServiceNow MCP Server listing](https://mcpservers.org/servers/michaelbuckner/servicenow-mcp)
- [ServiceNow MCP GitHub repository](https://github.com/michaelbuckner/servicenow-mcp)
- [ServiceNow Table API Documentation](https://developer.servicenow.com/dev.do#!/reference/api/vancouver/rest/c_TableAPI)

## Contribution Metadata
- Last reviewed: 2026-06-11
- Confidence: high
