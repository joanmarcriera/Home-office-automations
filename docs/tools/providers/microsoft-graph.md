# Microsoft Graph API

## What it is
Microsoft Graph is the gateway to data and intelligence in Microsoft 365. It provides a unified programmability model that you can use to access the tremendous amount of data in Microsoft 365, Windows, and Enterprise Mobility + Security. It is a critical [provider](../providers/index.md) for enterprise-grade [agents](../agents/index.md).

## What problem it solves
It simplifies developer interaction with Microsoft services by providing a single endpoint (`https://graph.microsoft.com`) to access data across multiple services like Outlook, OneDrive, Teams, and Microsoft Entra. This allows for complex cross-service automations and enables AI agents like `claude-4-8-opus-20260528` to act as personal assistants with full context.

## Where it fits in the stack
**Providers / API Gateway**. It serves as the primary integration point for applications needing to interact with the Microsoft 365 ecosystem. It often powers [MCP servers](../automation_orchestration/mcp.md) for calendar, email, and file management in agentic workflows.

## Typical use cases
- **Personal AI Assistants**: Synchronizing calendars (Outlook) and files (OneDrive) for autonomous [Task Management](../calendar_tasks/index.md).
- **Enterprise Automation**: Managing users and groups in [Microsoft Entra ID](../enterprise/microsoft-entra-id.md).
- **Workflow Orchestration**: Automating cross-app workflows in Microsoft Teams using [n8n](../../services/n8n.md) or [Make](../automation_orchestration/make.md).
- **Knowledge Synthesis**: Extracting insights from organizational data for [Process Understanding](../process_understanding/index.md).

## Strengths
- **Unified Endpoint**: Access a wide range of services through one API, reducing integration overhead.
- **Rich Relationships**: Navigate between related resources (e.g., user to their manager to their files) easily.
- **Delta Queries**: Efficiently track changes to data without full synchronization, ideal for real-time agents.
- **Deep Identity Integration**: Native integration with [Microsoft Entra ID](../enterprise/microsoft-entra-id.md) for secure, scoped access.

## Limitations
- **API Complexity**: The breadth of the API is vast, requiring significant effort to master the various resource types.
- **Throttling**: Strict rate limits apply, requiring robust error handling and exponential backoff in [automation workflows](../automation_orchestration/index.md).
- **Permission Management**: Navigating OAuth scopes and granular permissions (Least Privilege) can be challenging for developers.

## When to use it
- When building applications or [agents](../agents/index.md) that need to read or write data within the Microsoft 365 ecosystem.
- When creating [Custom Agents](../agents/custom_agents.md) that require access to corporate knowledge and communication channels.
- To enable AI-driven productivity tools that operate on calendar, email, and document data.

## When not to use it
- For simple, personal automation where a direct, service-specific tool might be faster.
- When working entirely outside the Microsoft ecosystem (e.g., using Google Workspace exclusively).

## Getting started

### App Registration
1. Register an application in the [Microsoft Entra admin center](https://entra.microsoft.com).
2. Configure required API permissions (e.g., `User.Read`, `Calendars.Read`).
3. Obtain your Client ID, Tenant ID, and Client Secret.

### Authentication (OAuth2)
Microsoft Graph requires an OAuth2 access token for all requests.

```bash
# Example: Getting an access token via Azure CLI
az account get-access-token --resource https://graph.microsoft.com
```

## CLI examples

### Fetching Current User Profile
```bash
curl -X GET "https://graph.microsoft.com/v1.0/me" \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json"
```

### Searching for Files in OneDrive
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
        "startDateTime": "2026-06-16T00:00:00Z",
        "endDateTime": "2026-06-16T23:59:59Z"
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
- [Microsoft Entra ID](../enterprise/microsoft-entra-id.md) — for identity and access management
- [Microsoft Todo](../calendar_tasks/microsoft-todo.md) — for task-specific API endpoints
- [n8n Automation](../../services/n8n.md) — for visual workflow building
- [Make](../automation_orchestration/make.md) — an alternative automation platform
- [Google Calendar API](../calendar_tasks/google_calendar.md) — the equivalent for the Google ecosystem
- [MCP Servers](../automation_orchestration/mcp.md) — for integrating Graph with LLM agents
- [Wrangler](../development_ops/wrangler.md) — for managing secrets in edge environments

## Sources / references
- [Microsoft Graph Documentation](https://learn.microsoft.com/en-us/graph/overview)
- [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- [Microsoft Graph SDKs](https://learn.microsoft.com/en-us/graph/sdks/sdks-overview)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
