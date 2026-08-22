# Focalboard

> [!WARNING]
> The standalone Focalboard project (Personal Server/Desktop) is in **community maintenance mode**. Mattermost development focus remains centered on the integrated "Boards" plugin for the Mattermost platform. Users seeking an actively developed, standalone task and project management ecosystem with native FastMCP 3.1 support should prioritize [Vikunja](vikunja.md).

## What it is
Focalboard is a dedicated task management platform that provides a Kanban-style interface for organizing work and tracking team deliverables. It is designed to be a lightweight, self-hosted alternative to SaaS solutions like Trello, Notion, and Asana. It provides a structured, multilingual environment for personal organization and small team collaboration. In early January 2027, it remains a stable, schema-consistent target for agentic task injection and visual status dashboards.

## What problem it solves
It provides a structured way to track tasks, projects, and goals without relying on third-party cloud providers. It addresses the need for privacy-conscious team collaboration within a self-hosted infrastructure. For autonomous AI agents like **Claude 5.1**, **GPT-5.5/5.6**, and **Gemini 4.0 Pro**, Focalboard provides a predictable, schema-stable Kanban target that undergoes minimal breaking API changes.

## Where it fits in the stack
**Category**: Service / Project Management. It fits into the **Productivity and Execution** layer. It is often used as a visual "Status Dashboard" for long-running agentic tasks, where human operators can visually inspect the progress of AI-driven project boards and task queues.

## Typical use cases
- **Legacy Project Archival**: Maintaining long-term access to historical Kanban boards from prior engineering cycles.
- **Agentic Task Visualization**: Utilizing local vision models (**Gemma 3**, **Qwen 3.8**, or **Llama 4 Vision**) alongside LLMs to automatically populate Kanban cards with research summaries for human inspection.
- **Personal Knowledge & Asset Archival**: Using custom properties to track and categorize physical hardware or digital homelab assets.
- **Content Calendars**: Planning and scheduling media production pipelines using visual drag-and-drop interfaces.
- **Board Sync via MCP Bridges**: Utilizing **FastMCP 3.1** custom connectors to synchronize Focalboard cards with primary execution engines like [Vikunja](vikunja.md).

## Strengths
- **Stable Interface**: A mature, highly predictable Kanban UI that is intuitive for both humans and autonomous agent tools.
- **Schema Flexibility**: Add custom properties (dates, multi-select, text, URLs) to cards to support specialized agentic metadata schemas.
- **Multi-View Support**: Effortlessly toggle between Board, Table, and Gallery views of the underlying database items.
- **Self-Hosted Data Sovereignty**: Complete local control over database storage and user permissions without cloud dependencies.
- **Robust REST API**: Well-documented endpoints that remain reliable for legacy integrations and automated script bridges.

## Limitations
- **Maintenance Mode Status**: Minimal active core development; teams must monitor dependency updates for long-term security maintenance.
- **Lacks Native Modern MCP Engine**: Requires an external **FastMCP 3.1** sidecar bridge to connect natively with frontier model tool-calling loops.
- **Mobile Experience**: Standalone mobile applications are legacy and lack support for modern mobile OS UI guidelines.

## When to use it
- When you need a simple, self-hosted Kanban board for personal productivity or historical project tracking.
- For managing projects that require custom properties not easily supported by simple checklists.
- When you prefer a standalone tool with a static, non-shifting REST API structure.

## When not to use it
- For mission-critical production environments requiring active vendor security patches (use [Vikunja](vikunja.md) instead).
- If you require advanced native automation or deep integration with modern CI/CD agentic workflows.
- When complex Gantt timelines or multi-project resource allocation features are primary requirements.

## Getting started

### Installation (Docker)
The simplest way to run Focalboard in a self-hosted environment:

```bash
docker run -d --name focalboard -p 8000:8000 mattermost/focalboard
```

### Hello World
1. Access the web interface at `http://localhost:8000`.
2. Register your initial administrator credentials.
3. Click **Add Board** in the sidebar and select the "Project Tasks" template.
4. Add a card: "Verify FastMCP Bridge" and drag it to the "In Progress" column.
5. Switch to **Table View** to inspect and bulk-edit card metadata properties.

## CLI examples

### Server Administration
Administrative tasks handled via the `focalboard-server` container binary:

```bash
# Reset the password for a specific user
docker exec focalboard ./focalboard-server reset-password <username>

# Check the current version of the Focalboard server
docker exec focalboard ./focalboard-server version

# Export a board as a structured JSON archive
docker exec focalboard ./focalboard-server export board_id > board_export_2027.json
```

## API examples

### Card Retrieval and Creation (Python with Pydantic v2)
Programmatic Python script for querying and creating boards and cards, utilizing **Pydantic v2** validation to ensure structured task payloads are sound.

```python
import os
from typing import List, Dict, Any, Optional
import requests
from pydantic import BaseModel, Field, field_validator

class BoardProperty(BaseModel):
    id: str
    name: str
    type: str
    options: List[Dict[str, Any]] = Field(default_factory=list)

class BoardSchema(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    properties: List[BoardProperty] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Board title cannot be empty")
        return value

def fetch_all_boards() -> List[BoardSchema]:
    focal_url = os.getenv("FOCALBOARD_URL", "http://localhost:8000")
    session_token = os.getenv("FOCALBOARD_TOKEN", "your_session_token_here")

    url = f"{focal_url}/api/v1/boards"
    headers = {
        "Authorization": f"Bearer {session_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    # Validate list of boards using Pydantic v2 model_validate
    return [BoardSchema.model_validate(board) for board in response.json()]

if __name__ == "__main__":
    try:
        boards = fetch_all_boards()
        for b in boards:
            print(f"Validated Board: {b.title} (ID: {b.id})")
            for prop in b.properties:
                print(f"  - Property: {prop.name} ({prop.type})")
    except Exception as e:
        print(f"Failed to query boards: {e}")
```

### Curl: User Authentication Check
```bash
# Query currently authenticated user credentials
curl -H "Authorization: Bearer <your_session_token>" \
     "http://localhost:8000/api/v1/users/me"
```

## Related tools / concepts
- [Vikunja](vikunja.md) — The recommended modern alternative for self-hosted task management.
- [Ollama](ollama.md) — For hosting local LLMs (Gemma 3, Qwen 3.8) to populate Kanban cards.
- [MCP](../tools/automation_orchestration/mcp-registry.md) — Protocol registry for connecting legacy boards to agentic workflows.
- [Nextcloud](nextcloud.md) — Offers the "Deck" app for integrated Kanban within a larger cloud suite.
- [Gitea](gitea.md) — Provides native project boards for code-centric development tasks.
- [Authentik](authentik.md) — For managing secure SSO access to the Focalboard UI.
- [Trilium](trilium.md) — For deep personal knowledge management alongside tasks.
- [Element](element.md) — For real-time communication about tasks tracked in Focalboard.

## Sources / references
- [Official Website](https://www.focalboard.com/)
- [GitHub Repository](https://github.com/mattermost/focalboard)
- [Boards Project (Mattermost)](https://mattermost.com/platform/mattermost-boards/)
- [Focalboard API Documentation](https://developers.mattermost.com/contribute/focalboard/api-reference/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
