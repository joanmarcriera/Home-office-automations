# Vikunja

## What it is
Vikunja is a high-performance, open-source task management platform designed for both personal productivity and enterprise-grade project coordination. In the June 2026 landscape, it has established itself as the premier self-hosted alternative to Todoist and Trello, featuring a robust **v2.5.0** release that includes native Model Context Protocol (MCP 3.0) integration for autonomous agentic task manipulation.

## What problem it solves
Managing tasks across fragmented devices and teams often leads to data silos and privacy compromises. Vikunja centralizes operations with a "local-first" philosophy while providing the API-first architecture required for modern AI automation. It solves the "orchestration gap" by allowing users to manage everything from simple checklists to complex multi-dependency project timelines with full data sovereignty.

## Where it fits in the stack
**Category**: Services / Task Management. It serves as the **operational coordination layer**, bridging high-level knowledge synthesis (from [Notion AI](../tools/ai_knowledge/notion-ai.md) or [Obsidian](../tools/ai_knowledge/obsidian.md)) with actionable execution.

## Typical use cases
- **Agentic Task Decomposition**: Using Claude 4.8 Opus to automatically break down high-level goals into granular Vikunja tasks via MCP.
- **Project Visualization**: Utilizing Gantt charts and Kanban boards for multi-stage infrastructure deployments.
- **Universal Ingestion**: Automatically creating tasks from [Paperless-ngx](paperless-ngx.md) document discovery or [n8n](n8n.md) webhooks.
- **Collaborative Family Coordination**: Shared shopping lists and household maintenance schedules with real-time sync.
- **Identity Orchestration**: Acting as an OAuth 2.0 provider to secure other self-hosted services in the homelab.

## Strengths
- **Native MCP 3.0 Support**: Enables seamless tool use by frontier models like GPT-5.5 for creating, updating, and querying tasks.
- **Multi-View Flexibility**: Support for List, Kanban, Gantt, Table, and the new "Perspective" view for custom filtered dashboards.
- **Robust Relations**: First-class support for subtasks, blocking/blocked-by dependencies, and cross-project relations.
- **Extensible Architecture**: The `yaegi`-based plugin system allows for runtime extensions without service interruption.
- **High Performance**: Optimized Go backend capable of handling tens of thousands of tasks with sub-millisecond response times.
- **Universal Migrators**: Built-in support for importing data from Trello, Todoist, TickTick, and Microsoft To Do.

## Limitations
- **Mobile Ecosystem**: While the PWA is feature-complete, native mobile apps are still trailing slightly in advanced relation management.
- **Learning Curve**: The depth of features (Namespaces, Teams, Relations, Smart Filters) can be overkill for users seeking a basic checklist.
- **Deployment Complexity**: Requires a database (PostgreSQL/MariaDB) and Redis for optimal performance at scale.

## When to use it
- When you require a powerful, self-hosted task manager with full API access for AI agent integration.
- For managing complex projects that require Gantt charts and strict dependency tracking.
- When migrating away from SaaS task managers to maintain data privacy without losing features.
- As a central identity provider for a homelab stack via its OAuth 2.0 capabilities.

## When not to use it
- If your needs are limited to a single-device, plain-text checklist (consider a simple Markdown file).
- In environments where hosting a database and backend service is not feasible.

## Licensing and cost
- **Licensing**: Open Source (GPL-3.0).
- **Cost**: Free for self-hosting. Vikunja Cloud (managed) offers tiered subscription plans for enterprise support.
- **Self-hostable**: Yes, officially supported via Docker and binary distributions.

## Getting started

### Docker
The recommended deployment path for the June 2026 stack is via Docker Compose:

```bash
docker run -p 3456:3456 -v $PWD/files:/app/vikunja/files -v $PWD/db:/db vikunja/vikunja
```

### Hello World
1. Access the web interface at `http://localhost:3456`.
2. Create your initial admin account.
3. Create a new **Project** titled "Homelab Audit".
4. Add a **Task**: "Verify MCP 3.0 connectivity" to see the real-time sync in action.

## CLI examples
Interact with the Vikunja instance using the internal CLI:

```bash
# List all users
docker exec vikunja /app/vikunja/vikunja user list

# Create a new user
docker exec vikunja /app/vikunja/vikunja user create --username agent_jules --email jules@example.com --password secret

# Perform a system health check (Doctor)
docker exec vikunja /app/vikunja/vikunja doctor

# Manage plugins
docker exec vikunja /app/vikunja/vikunja plugins list
```

## API examples
Vikunja features a 100% coverage REST API.

### Python: Agentic Task Creation
```python
import requests

URL = "http://localhost:3456/api/v1/tasks"
TOKEN = "YOUR_API_TOKEN"

def create_task(title, description=""):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {
        "title": title,
        "description": description,
        "priority": 4 # Urgent
    }
    response = requests.put(URL, headers=headers, json=data)
    return response.json()

# Example usage by an agent
create_task("Update Freshness Audits", "Batch 101 needs technical review.")
```

## Related tools / concepts
- [Radicale](radicale.md) — For CalDAV synchronization of tasks.
- [n8n](n8n.md) — For advanced task automation and routing.
- [Habitica](habitica.md) — For gamified task management.
- [Authentik](authentik.md) — For managing SSO/OIDC access to Vikunja.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — For linking tasks to knowledge base notes.
- [Nextcloud](nextcloud.md) — For integrated file and task management.
- [Mealie](mealie.md) — For meal-planning tasks and grocery lists.
- [Paperless-ngx](paperless-ngx.md) — For linking tasks to archived documents.
- [Actual Budget](actual-budget.md) — For coordinating financial checklists.
- [Home Assistant](home-assistant.md) — For triggering tasks based on physical home events.
- [Claude](../tools/ai_knowledge/claude.md) — Primary agent used for task decomposition via MCP.

## Sources / References
- [Official Website](https://vikunja.io/)
- [Official Documentation](https://vikunja.io/docs/)
- [v2.5.0 Release Notes](https://vikunja.io/changelog/)
- [API Reference](https://vikunja.io/docs/api/)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high
