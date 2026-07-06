# Microsoft Graph API

## What it is
Microsoft Graph is the gateway to data and intelligence in Microsoft 365. It provides a unified programmability model that you can use to access the tremendous amount of data in Microsoft 365, Windows, and Enterprise Mobility + Security. In July 2026, it is the primary data backbone for **agentic workflows** using **MCP 3.0 Microsoft Graph connectors**, enabling seamless integration between LLMs and enterprise productivity data.

## What problem it solves
It simplifies developer interaction with Microsoft services by providing a single endpoint (`https://graph.microsoft.com`) to access data across multiple services like Outlook, OneDrive, Teams, and Microsoft Entra. This allows for complex cross-service automations and enables AI agents like **Claude 4.8 Opus** and **GPT-5.5** to act as personal assistants with full organizational context.

## Where it fits in the stack
**Providers / API Gateway**. It serves as the primary integration point for applications needing to interact with the Microsoft 365 ecosystem. It natively powers [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers for calendar, email, and file management, providing the "eyes and hands" for enterprise agents.

## Typical use cases
- **Personal AI Assistants**: Synchronizing calendars (Outlook) and files (OneDrive) for autonomous [Task Management](../calendar_tasks/index.md).
- **Agentic Knowledge Retrieval**: Using RAG patterns to search corporate documents via [OneDrive and SharePoint](https://learn.microsoft.com/en-us/graph/api/resources/onedrive).
- **Enterprise Automation**: Managing users and groups in [Microsoft Entra ID](../enterprise/microsoft-entra-id.md) via autonomous [Agentic Automation Canvas](../agents/agentic-automation-canvas.md) workflows.
- **Workflow Orchestration**: Automating cross-app workflows in Microsoft Teams using the [MCP 3.0 Task Protocol](../automation_orchestration/mcp.md).

## Strengths
- **Unified Endpoint**: Access a wide range of services through one API, reducing integration overhead.
- **Rich Relationships**: Navigate between related resources (e.g., user to their manager to their files) easily.
- **Delta Queries**: Efficiently track changes to data without full synchronization, ideal for real-time agents.
- **MCP 3.0 Compatibility**: Standardized tool-calling patterns for Microsoft data are widely available and well-maintained.

## Limitations
- **API Complexity**: The breadth of the API is vast, requiring significant effort to master the various resource types.
- **Throttling**: Strict rate limits apply, requiring robust error handling in high-frequency agentic loops.
- **Permission Management**: Navigating OAuth scopes and granular permissions (Least Privilege) can be challenging for autonomous agents.

## When to use it
- When building applications or agents that need to read or write data within the Microsoft 365 ecosystem.
- When creating agents that require access to corporate knowledge and communication channels.
- To enable AI-driven productivity tools that operate on calendar, email, and document data.

## When not to use it
- For simple, personal automation where a direct, service-specific tool might be faster.
- When working entirely outside the Microsoft ecosystem (e.g., using Google Workspace exclusively).

## Getting started

### App Registration
1. Register an application in the [Microsoft Entra admin center](https://entra.microsoft.com).
2. Configure required API permissions (e.g., `User.Read`, `Calendars.Read`).
3. Obtain your Client ID, Tenant ID, and Client Secret.

### MCP 3.0 Integration
The fastest way to use Graph with agents is via an MCP server:
```bash
# Example: Adding Microsoft Graph MCP server to Claude Desktop
{
  "mcpServers": {
    "microsoft-graph": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-microsoft-graph"],
      "env": {
        "CLIENT_ID": "your_id",
        "TENANT_ID": "your_tenant",
        "CLIENT_SECRET": "your_secret"
      }
    }
  }
}
```

## CLI examples

### Fetching Current User Profile
```bash
curl -X GET "https://graph.microsoft.com/v1.0/me" \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json"
```

### Searching OneDrive via CLI
```bash
curl -X GET "https://graph.microsoft.com/v1.0/me/drive/root/search(q='Project Alpha')" \
     -H "Authorization: Bearer <access_token>"
```

## API examples

### Listing Calendar Events (Python)
Using the Microsoft Graph SDK for Python.

```python
from msgraph import GraphServiceClient
from azure.identity import DefaultAzureCredential

# Initialize client with default credentials
client = GraphServiceClient(credentials=DefaultAzureCredential(), scopes=['Calendars.Read'])

# Fetch events for the current day
events = await client.me.calendar_view.get(
    query_parameters = {
        "startDateTime": "2026-07-21T00:00:00Z",
        "endDateTime": "2026-07-21T23:59:59Z"
    }
)
```

### Sending a Teams Message (Python)
```python
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.item_body import ItemBody

request_body = ChatMessage(
    body = ItemBody(content = "Hello from the Graph API!"),
)

await client.teams.by_team_id('team-id').channels.by_channel_id('channel-id').messages.post(request_body)
```

## Related tools / concepts
- [Microsoft Entra ID](../enterprise/microsoft-entra-id.md) — for identity and access management.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — standard for agent-tool communication.
- [Agentic Automation Canvas](../agents/agentic-automation-canvas.md) — for visual agent orchestration.
- [Anthropic](../providers/anthropic.md) — provider often used with Graph integrations.
- [OpenAI](../ai_knowledge/openai.md) — provider for GPT-5.5 enterprise deployments.
- [Cloudflare Pages](../development_ops/cloudflare-pages.md) — often used to host Graph-integrated web apps.
- [GitHub Copilot](../development_ops/github-copilot-cli.md) — utilizes Graph for organizational context.
- [Task Management Index](../calendar_tasks/index.md) — for related productivity tools.

## Sources / references
- [Microsoft Graph Documentation](https://learn.microsoft.com/en-us/graph/overview)
- [MCP Microsoft Graph Server](https://github.com/modelcontextprotocol/servers/tree/main/src/microsoft-graph)
- [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
