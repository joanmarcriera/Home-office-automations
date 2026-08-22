# Vikunja

## What it is
Vikunja is a high-performance, open-source task management platform designed for both personal productivity and enterprise-grade project coordination. In the early January 2027 landscape, it stands as the premier self-hosted task ecosystem, featuring native **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** integration for seamless autonomous agentic task manipulation, automated goal breakdown, and multi-user workflow orchestration.

## What problem it solves
Managing tasks across fragmented devices, AI agents, and teams often leads to data silos and privacy compromises. Vikunja centralizes operations with a "local-first" philosophy while providing the API-first architecture required for modern AI automation. It solves the "orchestration gap" by allowing users and autonomous agentic clusters (running frontier models like **Claude 5.1**, **GPT-5.5/5.6**, **Gemini 4.0 Pro/Ultra**, and **DeepSeek-V4**) to manage everything from simple checklists to complex multi-dependency project timelines with full data sovereignty and end-to-end security.

## Where it fits in the stack
**Category**: Services / Task Management. It serves as the **operational coordination layer**, bridging high-level knowledge synthesis (from [Notion AI](../tools/ai_knowledge/notion-ai.md) or [Obsidian](../tools/ai_knowledge/obsidian.md)) with actionable execution. It is often the primary "source of truth" for an agent's current agenda and task execution queue within homelab and enterprise architectures.

## Typical use cases
- **Agentic Task Decomposition**: Using frontier models (Claude 5.1, GPT-5.5/5.6, Gemini 4.0 Pro, Llama 4, DeepSeek-V4) to automatically break down high-level project goals into granular Vikunja tasks via FastMCP 3.1 tool calls.
- **Multimodal Project Management**: Attaching screenshots, architecture diagrams, or document scans to tasks that vision models (Gemini 4.0 Ultra, Llama 4 Vision) can inspect to update project statuses automatically.
- **Universal Ingestion**: Automatically creating tasks from [Paperless-ngx](paperless-ngx.md) document discovery, [Changedetection.io](changedetection.md) triggers, or [n8n](n8n.md) webhooks.
- **Collaborative Family & Team Coordination**: Shared shopping lists, maintenance schedules, and software sprints with real-time sync across web, mobile, and desktop clients.
- **Identity Orchestration**: Acting as an OAuth 2.0/OIDC client or provider to secure other self-hosted services within an [Authentik](authentik.md) identity mesh.

## Strengths
- **Native FastMCP 3.1 Integration**: Enables zero-latency tool calls for AI agents to query, create, re-prioritize, and close tasks using structured JSON payloads.
- **Multi-View Flexibility**: Native support for List, Kanban, Gantt, Table, and custom filtered "Perspective" views for personalized execution dashboards.
- **Robust Relations Engine**: First-class support for subtask hierarchies, blocking/blocked-by dependencies, and cross-project relations.
- **High Performance Backend**: Optimized Go backend capable of handling tens of thousands of tasks with sub-millisecond API query latencies.
- **Universal Migrators**: Built-in, automated migration tools for importing data from Trello, Todoist, TickTick, and Microsoft To Do.
- **Granular Access Controls**: Teams, Namespaces, and RBAC support for secure multi-tenant or multi-agent environments.

## Limitations
- **Mobile Ecosystem**: While the PWA is feature-complete, native iOS/Android client apps lag slightly behind the web UI in managing complex task dependencies.
- **Setup Overhead**: Depth of features (Namespaces, Teams, Custom Filters, OIDC) can require initial configuration planning compared to basic single-user lists.
- **Database Dependency**: Requires a dedicated relational database (PostgreSQL 16+/MariaDB) and Redis for high-concurrency pub/sub event notifications.

## When to use it
- When you require a powerful, self-hosted task manager with full REST API and FastMCP 3.1 access for AI agent integration.
- For managing complex engineering or operational projects that require Gantt timelines and strict dependency chains.
- When migrating away from SaaS task management tools to maintain total data privacy without sacrificing modern UI capabilities.
- As an operational backend for autonomous agent loops requiring persistent task queues.

## When not to use it
- If your requirements are limited to single-device, plain-text checklists (consider a simple Markdown file or Todo.txt).
- In lightweight environments where hosting a database and backend service container is unfeasible.

## Getting started

### Docker Compose
The recommended deployment path for the early 2027 stack is via Docker Compose:

```yaml
services:
  vikunja:
    image: vikunja/vikunja:latest
    container_name: vikunja
    ports:
      - "3456:3456"
    volumes:
      - ./files:/app/vikunja/files
      - ./db:/db
    environment:
      - VIKUNJA_DATABASE_TYPE=sqlite
      - VIKUNJA_DATABASE_PATH=/db/vikunja.db
      - VIKUNJA_SERVICE_JWTSECRET=use-a-secure-secret-key-2027
    restart: unless-stopped
```

### Hello World
1. Access the web interface at `http://localhost:3456`.
2. Register your administrative account.
3. Create a new **Project** titled "Homelab Automation 2027".
4. Add a **Task**: "Verify FastMCP 3.1 agent connectivity" to test live task tracking.

## CLI examples
Interact with the Vikunja instance using the internal CLI:

```bash
# List all registered users
docker exec vikunja /app/vikunja/vikunja user list

# Create a new service account for AI agents
docker exec vikunja /app/vikunja/vikunja user create --username agent_jules --email jules@example.com --password secretpass

# Perform system health check and database migration status
docker exec vikunja /app/vikunja/vikunja doctor

# Export total system data state as structured JSON
docker exec vikunja /app/vikunja/vikunja dump
```

## API examples

### Python: Agentic Task Creation (Pydantic v2)
Using Python and Pydantic v2 to programmatically register and validate incoming task schedules and agent payloads in early 2027.

```python
import requests
from pydantic import BaseModel, Field, conint
from typing import Optional, List

class VikunjaTask(BaseModel):
    title: str = Field(..., description="The brief title of the task")
    description: Optional[str] = Field("", description="Detailed markdown task notes and context")
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
    new_task = VikunjaTask(
        title="Execute 2027 SOTA freshness audit",
        description="Audit frontier model capability references (Claude 5.1, FastMCP 3.1).",
        priority=5,
        labels=["maintenance", "ai-knowledgeops"]
    )
    print("Vikunja validation model initialized for task:", new_task.title)
```

### FastMCP 3.1 Task Tool (TypeScript)
TypeScript tool registration for FastMCP 3.1 task integration.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP({
  name: "vikunja-tasks",
  version: "3.1.0"
});

mcp.addTool({
  name: "add_vikunja_task",
  description: "Create a new task in Vikunja project board",
  parameters: {
    title: { type: "string", description: "The task title" },
    projectId: { type: "number", description: "Target project ID" },
    description: { type: "string", description: "Detailed task description" }
  },
  execute: async ({ title, projectId, description }) => {
    const res = await fetch(`http://vikunja:3456/api/v1/projects/${projectId}/tasks`, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${process.env.VIKUNJA_TOKEN}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ title, description })
    });
    return res.json();
  }
});

mcp.start();
```

## Related tools / concepts
- [Radicale](radicale.md) — For CalDAV synchronization of tasks across desktop clients.
- [n8n](n8n.md) — For advanced task automation, webhook triggers, and external API routing.
- [Ollama](ollama.md) — For hosting local LLMs used in task reasoning and automated prioritization.
- [MCP](../tools/automation_orchestration/mcp-registry.md) — Standard protocol for task manipulation by autonomous agent loops.
- [Authentik](authentik.md) — For managing SSO/OIDC authentication access to Vikunja.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — For linking tasks to knowledge base notes.
- [Paperless-ngx](paperless-ngx.md) — For linking tasks to archived documents.
- [Home Assistant](home-assistant.md) — For triggering physical home tasks based on system events.
- [Mealie](mealie.md) — For sync of meal-planning tasks and grocery checklists.

## Sources / references
- [Official Website](https://vikunja.io/)
- [Official Documentation](https://vikunja.io/docs/)
- [Vikunja API Reference](https://vikunja.io/docs/api/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
