# Focalboard

> [!WARNING]
> The standalone Focalboard project (Personal Server/Desktop) is in **community maintenance mode**. Mattermost focus has shifted to the integrated "Boards" plugin for the Mattermost platform. Users seeking an actively developed standalone project management tool with native MCP 3.1 support should prioritize [Vikunja](vikunja.md).

## What it is
Focalboard is a dedicated task management system that provides a Kanban-style interface for organizing work. It is designed to be a lightweight, self-hosted alternative to centralized services like Trello, Notion, and Asana. It provides a structured, multilingual environment for personal organization and small team collaboration. In the late October / November 2026 landscape, it remains a stable "legacy" target for agentic task injection.

## What problem it solves
It provides a structured way to track tasks, projects, and goals without relying on third-party cloud providers. It addresses the need for privacy-conscious team collaboration within a self-hosted infrastructure. For AI agents like **Claude 5.1** or **GPT-5.5**, Focalboard provides a predictable, schema-stable Kanban target that does not change as frequently as more "active" projects.

## Where it fits in the stack
**Category**: Service / Project Management. It fits into the **Productivity and Execution** layer. It is often used as a visual "Status Dashboard" for long-running agentic tasks, where a human can visually inspect the progress of an AI-driven project board.

## Typical use cases
- **Legacy Project Archival**: Maintaining access to historical Kanban boards from previous project cycles.
- **Agentic Task Visualization**: Using **Gemma 3** or **Qwen 3.6** to automatically populate Kanban cards with research findings for human review.
- **Personal Knowledge Archival**: Using custom properties to track and categorize physical or digital assets.
- **Content Calendars**: Simple planning and scheduling for media production with visual drag-and-drop.
- **Board Sync via MCP**: Using the **Model Context Protocol (MCP 3.1)** to synchronize Focalboard cards with other task managers like [Vikunja](vikunja.md).

## Strengths
- **Stable Interface**: A mature, predictable Kanban UI that is easy for both humans and agents to navigate.
- **Schema Flexibility**: Add custom properties (dates, selects, text) to cards to support specialized agentic metadata.
- **Multi-View Support**: Toggle between Board, Table, and Gallery views of the same underlying data.
- **Self-Hosted Privacy**: Full control over database and user permissions without cloud dependency.
- **Robust REST API**: Well-documented endpoints that remain reliable for legacy integrations.

## Limitations
- **Maintenance Status**: Minimal active development; users should be aware of potential security debt in the long term.
- **Lacks Modern Orchestration**: Does not natively support some of the newer **FastMCP 3.1** features found in newer tools.
- **Mobile Experience**: Standalone mobile apps are legacy and may not support newer OS features.

## When to use it
- When you need a simple, self-hosted Kanban board for personal use or legacy project tracking.
- For managing projects that require custom properties not easily supported by simple checklists.
- When you prefer a standalone tool with a stable API that won't undergo frequent breaking changes.

## When not to use it
- For mission-critical production environments requiring active security patches (use [Vikunja](vikunja.md) instead).
- If you require advanced automation or deep integration with modern CI/CD pipelines.
- When complex Gantt charts or resource allocation features are a primary requirement.

## Getting started

### Installation (Docker)
The simplest way to run Focalboard in a modern homelab environment.

```bash
docker run -d --name focalboard -p 8000:8000 mattermost/focalboard
```

### Hello World
1. Access the web interface at `http://localhost:8000`.
2. Create your initial admin account.
3. Click **Add Board** in the sidebar and select the "Project Tasks" template.
4. Add a card: "Test MCP Bridge" and drag it to the "In Progress" column.
5. Use the **Table View** to bulk-edit properties for your cards.

## CLI examples

### Server Administration
Administrative tasks handled via the `focalboard-server` binary.

```bash
# Reset the password for a specific user
docker exec focalboard ./focalboard-server reset-password <username>

# Check the current version of the server
docker exec focalboard ./focalboard-server version

# Export a board as an archive (legacy format)
docker exec focalboard ./focalboard-server export board_id > board_export.json
```

## API examples

### Legacy Card Retrieval and Creation (Python)
Programmatic Python script for querying and creating boards and cards, utilizing **Pydantic v2** validation to ensure structured task payloads are sound.

```python
import os
from typing import List, Dict, Any, Optional
import requests
from pydantic import BaseModel, Field, field_validator

# Pydantic v2 schemas for Focalboard board and card items
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

    response = requests.get(url, headers=headers)
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

### Curl: Quick Card Check
```bash
# Get information about the currently logged-in user
curl -H "Authorization: Bearer <your_session_token>" \
     "http://localhost:8000/api/v1/users/me"
```

## Related tools / concepts
- [Vikunja](vikunja.md) — The recommended modern alternative for task management.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — For reasoning over and populating Kanban cards.
- [MCP](../tools/automation_orchestration/mcp-registry.md) — Protocol registry for connecting legacy boards to agentic workflows.
- [Nextcloud](nextcloud.md) — Offers the "Deck" app for integrated Kanban within a larger cloud suite.
- [Gitea](gitea.md) — Provides native project boards for code-centric tasks.
- [Authentik](authentik.md) — For managing secure SSO access to the Focalboard UI.
- [Trilium](trilium.md) — For deep personal knowledge management alongside tasks.
- [Element](element.md) — For real-time communication about tasks tracked in Focalboard.

## Sources / references
- [Official Website](https://www.focalboard.com/)
- [GitHub Repository](https://github.com/mattermost/focalboard)
- [Boards Project (Mattermost)](https://mattermost.com/platform/mattermost-boards/)
- [Focalboard API Documentation](https://developers.mattermost.com/contribute/focalboard/api-reference/)

## Contribution Metadata
- Last reviewed: 2026-11-07
- Confidence: high
