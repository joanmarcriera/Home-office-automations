# Focalboard

> [!WARNING]
> The standalone Focalboard project (Personal Server/Desktop) is in **community maintenance mode**. Mattermost focus has shifted to the integrated "Boards" plugin for the Mattermost platform. Users seeking an actively developed standalone project management tool with native MCP 3.0 support should prioritize [Vikunja](vikunja.md).

## What it is
Focalboard is a dedicated task management system that provides a Kanban-style interface for organizing work. It is designed to be a lightweight, self-hosted alternative to centralized services like Trello, Notion, and Asana. It provides a structured, multilingual environment for personal organization and small team collaboration. In the July 2026 landscape, it remains a stable "legacy" target for agentic task injection.

## What problem it solves
It provides a structured way to track tasks, projects, and goals without relying on third-party cloud providers. It addresses the need for privacy-conscious team collaboration within a self-hosted infrastructure. For AI agents like **Gemma 3** or **Claude 4.8**, Focalboard provides a predictable, schema-stable Kanban target that does not change as frequently as more "active" projects.

## Where it fits in the stack
**Category**: Service / Project Management. It fits into the **Productivity and Execution** layer. It is often used as a visual "Status Dashboard" for long-running agentic tasks, where a human can visually inspect the progress of an AI-driven project board.

## Typical use cases
- **Legacy Project Archival**: Maintaining access to historical Kanban boards from previous project cycles.
- **Agentic Task Visualization**: Using **Gemma 3** to automatically populate Kanban cards with research findings for human review.
- **Personal Knowledge Archival**: Using custom properties to track and categorize physical or digital assets.
- **Content Calendars**: Simple planning and scheduling for media production with visual drag-and-drop.
- **Board Sync via MCP**: Using the **Model Context Protocol (MCP 3.0)** to synchronize Focalboard cards with other task managers like [Vikunja](vikunja.md).

## Strengths
- **Stable Interface**: A mature, predictable Kanban UI that is easy for both humans and agents to navigate.
- **Schema Flexibility**: Add custom properties (dates, selects, text) to cards to support specialized agentic metadata.
- **Multi-View Support**: Toggle between Board, Table, and Gallery views of the same underlying data.
- **Self-Hosted Privacy**: Full control over database and user permissions without cloud dependency.
- **Robust REST API**: Well-documented endpoints that remain reliable for legacy integrations.

## Limitations
- **Maintenance Status**: Minimal active development; users should be aware of potential security debt in the long term.
- **Lacks Modern Orchestration**: Does not natively support some of the newer **FastMCP 3.0** features found in newer tools.
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

### Python: Fetching Boards
Standard REST interaction for legacy agents.

```python
import requests

# Fetch all boards for the authenticated user
URL = "http://localhost:8000/api/v1/boards"
TOKEN = "YOUR_SESSION_TOKEN"
headers = {"Authorization": f"Bearer {TOKEN}"}

def list_boards():
    response = requests.get(URL, headers=headers)
    if response.ok:
        for board in response.json():
            print(f"Board: {board['title']} (ID: {board['id']})")

if __name__ == "__main__":
    list_boards()
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
- [MCP 3.0](../tools/automation_orchestration/mcp.md) — Protocol for connecting legacy boards to agentic workflows.
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
- Last reviewed: 2026-07-21
- Confidence: high
