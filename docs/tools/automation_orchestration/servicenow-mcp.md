# ServiceNow MCP Server

## What it is
ServiceNow MCP Server is a Model Context Protocol server that lets AI agents read and update ServiceNow data through MCP tools. It exposes ServiceNow's IT Service Management (ITSM) capabilities as structured tools that LLMs can invoke.

## What problem it solves
It reduces direct API wiring work when you want agents to query incidents, change requests, or scripts in ServiceNow through a standard tool interface. It abstracts the complexity of ServiceNow's Table API into a set of well-defined MCP tools.

## Where it fits in the stack
**Automation / Orchestration Tool**. It is a domain-specific MCP server used by MCP-compatible clients to bridge the gap between AI reasoning and enterprise IT operations.

## Typical use cases
- **Natural Language Triage**: Agent-assisted incident triage using natural language queries (e.g., "Find all incidents about SAP").
- **Automated Ticket Lifecycle**: Querying and updating tickets directly from coding agents like Claude 5.1.
- **Script Maintenance**: Maintaining script includes, business rules, and background scripts in ServiceNow from agent tools.
- **Status Reporting**: Automated status reporting for change requests and critical incidents.
- **Cross-Tool Synchronization**: Bridging ServiceNow data with other tools in the homelab stack (e.g., Jira, Slack).

## Strengths
- **MCP-Native**: Built specifically for the Model Context Protocol, ensuring compatibility with Claude 5.1, GPT-5.5, Gemini 4.0, and Llama 4 Maverick.
- **Natural Language Support**: Includes specialized tools for natural language search and updates.
- **Multi-Auth Support**: Supports Basic Auth, OAuth, and Token-based authentication.
- **Unified Interface**: Simplifies authentication by centralizing it in the server process.
- **Script Management**: Provides dedicated tools for updating ServiceNow script files from local files.

## Limitations
- Requires ServiceNow credentials (Service Account recommended) and environment setup.
- Trust boundaries and permissions must be configured carefully in ServiceNow (ACLs).
- Coverage depends on server-supported tool set and ServiceNow API access.

## When to use it
- When your agent workflows already use MCP and need ServiceNow integration.
- When you want standardized tool-calling for ServiceNow tasks.
- For rapid prototyping of AI-driven IT support agents.

## When not to use it
- When you need full ServiceNow platform automation beyond exposed MCP tools.
- When governance rules require tightly curated direct API integrations only.
- For high-volume data migrations (use ServiceNow IntegrationHub or direct API instead).

## Getting started

To use the ServiceNow MCP server (early 2027 FastMCP 3.1 compatible version):

1. **Installation**:
   ```bash
   pip install mcp-server-servicenow
   ```
2. **Configuration**: Obtain your ServiceNow instance URL, username, and password.
3. **Claude Desktop Integration**: Add the server configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "servicenow": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server_servicenow.cli"
      ],
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

### Running the Server Manually
Verify your connection by running the server directly from the command line:

```bash
python -m mcp_server_servicenow.cli \
  --url "https://your-instance.service-now.com/" \
  --username "admin" \
  --password "admin-password"
```

### Listing Available Tools
If using `mcp-cli` or similar debug tools:

```bash
mcp-cli list-tools --server-command "python -m mcp_server_servicenow.cli"
```

### Inspecting Resources
ServiceNow MCP exposes resources like incidents and tables:

```bash
# Example: List recent incidents via resource URI
mcp-cli read-resource servicenow://incidents
```

## API examples

### Searching for Incidents
Agents using FastMCP 3.1 or native MCP clients can invoke the `search_records` tool:

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

### Programmatic ServiceNow Client Validation with Pydantic v2
Robust local validation (Python) of incident and record payloads prior to updating the ServiceNow instance according to early 2027 SOTA standards:

```python
import os
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

# Pydantic v2 models representing the incident and response schema
class ServiceNowIncident(BaseModel):
    sys_id: str = Field(..., description="Unique ServiceNow system identifier")
    number: str = Field(..., description="Descriptive human-readable number (e.g. INC0012345)")
    short_description: str = Field(..., alias="shortDescription", description="Brief summary of the issue")
    state: int = Field(..., ge=1, le=8, description="Standard incident state integer")
    assigned_to: Optional[str] = Field(None, alias="assignedTo", description="Assigned support agent name")

class UpdateResult(BaseModel):
    success: bool
    incident: ServiceNowIncident

def update_incident_state(sys_id: str, new_state: int) -> UpdateResult:
    # Simulating connection to ServiceNow API with validation
    mock_data = {
        "success": True,
        "incident": {
            "sys_id": sys_id,
            "number": "INC0010001",
            "shortDescription": "VPN routing fails with Gemma 3 models",
            "state": new_state,
            "assignedTo": "Jules-Agent"
        }
    }

    # Strictly validate against the early 2027 ITSM contract schema
    validated = UpdateResult.model_validate(mock_data)
    return validated

if __name__ == "__main__":
    result = update_incident_state("9bc401bca91001bc93ef0", 2)
    print(f"Incident {result.incident.number} update success: {result.success}")
    print(f"Assigned Agent: {result.incident.assigned_to}")
```

### Natural Language Update
Leveraging the specialized `natural_language_update` tool for intuitive ticket management:

```json
// Tool call from agent
{
  "name": "natural_language_update",
  "arguments": {
    "query": "Update incident INC0010001 saying I'm working on it"
  }
}
```

### Updating Script Includes
Directly updating ServiceNow business logic from an agent:

```json
{
  "name": "update_script",
  "arguments": {
    "script_name": "HelloWorld",
    "script_type": "script_include",
    "content": "var HelloWorld = Class.create(); HelloWorld.prototype = { initialize: function() {}, type: 'HelloWorld' };"
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
- [Claude Desktop](../ai_knowledge/claude-desktop.md)
- [Goose](../agents/goose.md)
- [Anthropic](../providers/anthropic.md)
- [Claude 5.1](../providers/anthropic.md)
- [FastMCP 3.1](mcp.md)
- [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md)
- [Llama 4 Maverick](../ai_knowledge/local_llms.md)

## Sources / References
- [ServiceNow MCP Server listing](https://mcpservers.org/servers/michaelbuckner/servicenow-mcp)
- [ServiceNow MCP GitHub repository](https://github.com/michaelbuckner/servicenow-mcp)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
