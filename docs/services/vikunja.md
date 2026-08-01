# Vikunja

## What it is
Vikunja is a high-performance, open-source task management platform designed for both personal productivity and enterprise-grade project coordination. In the late October / November 2026 landscape, it stands as the premier self-hosted task ecosystem, featuring native **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** integration for seamless autonomous agentic task manipulation.

## What problem it solves
Managing tasks across fragmented devices and teams often leads to data silos and privacy compromises. Vikunja centralizes operations with a "local-first" philosophy while providing the API-first architecture required for modern AI automation. It solves the "orchestration gap" by allowing users and agents to manage everything from simple checklists to complex multi-dependency project timelines with full data sovereignty.

## Where it fits in the stack
**Category**: Services / Task Management. It serves as the **operational coordination layer**, bridging high-level knowledge synthesis (from [Notion AI](../tools/ai_knowledge/notion-ai.md) or [Obsidian](../tools/ai_knowledge/obsidian.md)) with actionable execution. It is often the primary "source of truth" for an agent's current agenda.

## Typical use cases
- **Agentic Task Decomposition**: Using frontier models (Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, Qwen 3.6) to automatically break down high-level project goals into granular Vikunja tasks via MCP 3.1.
- **Multimodal Project Management**: Attaching screenshots or diagrams to tasks that Gemma 3 or Qwen 3.6 vision models can reason over to provide status updates.
- **Universal Ingestion**: Automatically creating tasks from [Paperless-ngx](paperless-ngx.md) document discovery or [n8n](n8n.md) webhooks.
- **Collaborative Family Coordination**: Shared shopping lists and household maintenance schedules with real-time sync across mobile and desktop.
- **Identity Orchestration**: Acting as an OAuth 2.0/OIDC provider to secure other self-hosted services in the homelab.

## Strengths
- **Native MCP 3.1 Support**: Enables seamless tool use by frontier models for creating, updating, and querying tasks with standardized metadata.
- **Multi-View Flexibility**: Support for List, Kanban, Gantt, Table, and the "Perspective" view for custom filtered dashboards.
- **Robust Relations**: First-class support for subtasks, blocking/blocked-by dependencies, and cross-project relations.
- **FastMCP Integration**: Optimized for low-latency task retrieval in agentic loops using MCP 3.1 payloads.
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

## Getting started

### Docker Compose
The recommended deployment path for the late 2026 stack is via Docker Compose:

```yaml
services:
  vikunja:
    image: vikunja/vikunja:latest
    container_name: vikunja
    ports:
      - 3456:3456
    volumes:
      - ./files:/app/vikunja/files
      - ./db:/db
    environment:
      - VIKUNJA_DATABASE_TYPE=sqlite
      - VIKUNJA_DATABASE_PATH=/db/vikunja.db
      - VIKUNJA_SERVICE_JWTSECRET=use-a-secure-secret
    restart: unless-stopped
```

### Hello World
1. Access the web interface at `http://localhost:3456`.
2. Create your initial admin account.
3. Create a new **Project** titled "Homelab Audit".
4. Add a **Task**: "Verify MCP 3.1 connectivity" to see the real-time sync in action.

## CLI examples
Interact with the Vikunja instance using the internal CLI:

```bash
# List all users
docker exec vikunja /app/vikunja/vikunja user list

# Create a new user
docker exec vikunja /app/vikunja/vikunja user create --username agent_jules --email jules@example.com --password secret

# Perform a system health check (Doctor)
docker exec vikunja /app/vikunja/vikunja doctor

# Export all data as JSON
docker exec vikunja /app/vikunja/vikunja dump
```

## API examples

### Python: Agentic Task Creation (Pydantic v2)
Using Python and Pydantic v2 to programmatically register and validate incoming task schedules and payloads.

```python
import requests
from pydantic import BaseModel, Field, conint
from typing import Optional, List

class VikunjaTask(BaseModel):
    title: str = Field(..., description="The brief title of the task")
    description: Optional[str] = Field("", description="Detailed markdown task notes")
    priority: conint(ge=1, le=5) = Field(3, description="Task execution priority level (1=Lowest, 5=Highest)")
    labels: List[str] = Field(default_factory=list, description="Categorization labels")

def create_task(api_url: str, token: str, project_id: int, task_data: VikunjaTask) -> dict:
    url = f"{api_url}/projects/{project_id}/tasks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # Convert validated model to JSON-safe dict
    payload = task_data.model_dump(by_alias=True)
    response = requests.put(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Complete sample task execution block
    new_task = VikunjaTask(
        title="Upgrade SOTA freshness audits",
        description="Verify Claude 5.1 / GPT-5.5 / FastMCP 3.1 consistency.",
        priority=5,
        labels=["maintenance", "ai-knowledgeops"]
    )
    print("Vikunja validation model instantiated:", new_task.title)
```

### FastMCP 3.1 Task Tool (TypeScript)
TypeScript definition for FastMCP 3.1 task integration.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP("vikunja-tasks");

mcp.addTool({
  name: "add_vikunja_task",
  description: "Create a new task in Vikunja",
  parameters: {
    title: { type: "string", description: "The task title" },
    projectId: { type: "number", description: "The project ID" }
  },
  execute: async ({ title, projectId }) => {
    const res = await fetch(`http://vikunja:3456/api/v1/projects/${projectId}/tasks`, {
      method: "PUT",
      headers: { "Authorization": `Bearer ${process.env.VIKUNJA_TOKEN}`, "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });
    return res.json();
  }
});

mcp.serve();
```

## Related tools / concepts
- [Radicale](radicale.md) — For CalDAV synchronization of tasks.
- [n8n](n8n.md) — For advanced task automation and routing.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Primary agent used for task reasoning and decomposition.
- [MCP 3.1](../tools/automation_orchestration/mcp.md) — Standard protocol for task manipulation by agents.
- [Authentik](authentik.md) — For managing SSO/OIDC access to Vikunja.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — For linking tasks to knowledge base notes.
- [Paperless-ngx](paperless-ngx.md) — For linking tasks to archived documents.
- [Home Assistant](home-assistant.md) — For triggering tasks based on physical home events.
- [Mealie](mealie.md) — For meal-planning tasks and grocery lists.
- [Actual Budget](actual-budget.md) — For coordinating financial checklists.

## Sources / References
- [Official Website](https://vikunja.io/)
- [Official Documentation](https://vikunja.io/docs/)
- [Vikunja API Reference](https://vikunja.io/docs/api/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2026-11-06
- Confidence: high
