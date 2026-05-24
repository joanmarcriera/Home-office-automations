# Microsoft Graph API

## What it is
Microsoft Graph is the gateway to data and intelligence in Microsoft 365. It provides a unified programmability model that you can use to access the tremendous amount of data in Microsoft 365, Windows, and Enterprise Mobility + Security. It is a critical [provider](../providers/README.md) for enterprise-grade [agents](../agents/README.md).

## What problem it solves
It simplifies developer interaction with Microsoft services by providing a single endpoint (`https://graph.microsoft.com`) to access data across multiple services like Outlook, OneDrive, Teams, and Microsoft Entra (formerly Azure AD). This allows for complex cross-service automations, such as those found in [Enterprise Suites](../enterprise/README.md).

## Where it fits in the stack
**Providers / API Gateway**. It serves as the primary integration point for applications needing to interact with the Microsoft 365 ecosystem. It often powers [MCP servers](../automation_orchestration/mcp.md) for calendar and file management.

## Typical use cases
- Synchronizing calendars (Outlook) and files (OneDrive) for [Task Management](../calendar_tasks/README.md).
- Managing users and groups in Microsoft Entra (Azure AD).
- Automating workflows in Microsoft Teams using [n8n](../../services/n8n.md) or [Make](../automation_orchestration/make.md).
- Extracting insights from organizational data for [Process Understanding](../process_understanding/README.md).

## Key Features
- **Unified API**: Access Outlook, OneDrive, Teams, Planner, and more via one endpoint.
- **Delta Queries**: Efficiently track changes to data without full synchronization.
- **Webhooks**: Receive real-time notifications for data changes (e.g., new emails or calendar events).
- **Microsoft Graph Explorer**: An interactive tool for testing and discovering API capabilities.

## Strengths
- **Unified Endpoint**: Access a wide range of services through one API.
- **Rich Relationships**: Navigate between related resources easily.
- **Extensive Documentation**: Well-supported with SDKs for multiple languages.
- **Identity Integration**: Deeply integrated with [Microsoft Entra ID](../enterprise/microsoft-entra-id.md).

## Limitations
- **Complexity**: The sheer breadth of the API can be overwhelming.
- **Throttling**: Strict rate limits apply, requiring robust error handling in [automation workflows](../automation_orchestration/README.md).
- **Permission Granularity**: Managing OAuth scopes and permissions requires careful planning.

## When to use it
- When building applications that need to read or write data within Microsoft 365 services.
- When creating [Custom Agents](../agents/custom_agents.md) that need access to corporate knowledge.

## When not to use it
- For small-scale, personal automation where simpler, service-specific tools might suffice.
- When working entirely outside the Microsoft ecosystem.

## Getting started

### Authentication (OAuth2)
Microsoft Graph requires an Azure AD application registration and an OAuth2 token.

```bash
# Example: Getting an access token via CLI (Conceptual)
az account get-access-token --resource https://graph.microsoft.com
```

## Technical examples

### Fetching User Profile (cURL)
Standard GET request to the unified endpoint.

```bash
curl -X GET "https://graph.microsoft.com/v1.0/me" \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json"
```

### Listing Calendar Events (Python)
Using the Microsoft Graph SDK for Python.

```python
from msgraph import GraphServiceClient

# Initialize client with credentials
client = GraphServiceClient(credentials, scopes=['Calendars.Read'])

# Fetch events
events = await client.me.calendar_view.get(
    query_parameters = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetQueryParameters(
        start_date_time='2026-05-24T00:00:00Z',
        end_date_time='2026-05-25T00:00:00Z'
    )
)
```

## Maintenance & Troubleshooting
- **Token Expiry**: Ensure your application handles token refresh logic or uses [Wrangler](../development_ops/wrangler.md) for secret management in edge environments.
- **Throttling (429)**: Implement exponential backoff in your [n8n](../../services/n8n.md) or [Make](../automation_orchestration/make.md) nodes.

## Related tools / concepts
- [Microsoft Entra ID](../enterprise/microsoft-entra-id.md)
- [Microsoft Todo](../calendar_tasks/microsoft-todo.md)
- [n8n Automation](../../services/n8n.md)
- [Make](../automation_orchestration/make.md)
- [Enterprise Suite Overview](../enterprise/README.md)
- [Google Calendar API](../calendar_tasks/google_calendar.md)
- [MCP Servers](../automation_orchestration/mcp.md)

## Sources / references
- [Microsoft Graph Overview](https://learn.microsoft.com/en-us/graph/overview)
- [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- [Microsoft Graph SDKs](https://learn.microsoft.com/en-us/graph/sdks/sdks-overview)

## Contribution Metadata
- Last reviewed: 2026-05-24
- Confidence: high
