# Focalboard

> [!WARNING]
> This repository is currently not maintained. If you're interested in becoming a maintainer, please let the Mattermost community know. This documentation refers to the standalone Personal Server edition.

## What it is
Focalboard is a dedicated task management system that provides a Kanban-style interface for organizing work. It is designed to be a lightweight, self-hosted alternative to centralized services like Trello, Notion, and Asana. It is an open-source, multilingual, self-hosted project management tool.

## What problem it solves
It provides a structured way to track tasks, projects, and goals without relying on third-party cloud providers. It addresses the need for privacy-conscious team collaboration and personal organization within a self-hosted infrastructure.

## Where it fits in the stack
Focalboard fits into the **Project Management and Productivity** layer. It is often used alongside communication tools (like [Element](element.md) or Mattermost) and document storage (like [Nextcloud](nextcloud.md)) to provide a complete collaborative environment.

## Typical use cases
- **Personal Task Tracking**: Managing "to-do" lists and personal projects using a Kanban board.
- **Software Development**: Tracking bugs, features, and sprint progress for small teams.
- **Content Calendars**: Planning and scheduling blog posts or social media content.
- **Inventory Management**: Using custom properties to track physical assets.

## Strengths
- **Simple UI**: Familiar Kanban interface that is easy to adopt.
- **Customizable**: Add custom properties (dates, selects, text) to cards.
- **Multiple Views**: Switch between Board, Table, and Gallery views of the same data.
- **Self-Hosted**: Full control over data and user permissions.

## Limitations
- **Maintenance Status**: Currently unmaintained (see warning), which may lead to security vulnerabilities or lack of new features.
- **Feature Set**: Lacks the deep "all-in-one" database capabilities of Notion or the advanced automation of Jira.

## When to use it
- When you need a simple, self-hosted Kanban board for personal or small team use.
- To manage projects that require custom properties (e.g., "Priority", "Estimated Hours") on tasks.
- When you prefer a standalone tool for project tracking rather than one integrated into a larger suite.

## When not to use it
- For mission-critical production environments where active security maintenance is required (consider actively maintained alternatives like [Vikunja](vikunja.md)).
- When you need deep integration with version control systems (consider [Gitea](gitea.md) boards).
- If your projects require complex Gantt charts or advanced resource allocation features.

## Getting started

### Docker
To run the Focalboard Personal Server locally using the official Docker image:

```bash
docker run -d --name focalboard -p 8000:8000 mattermost/focalboard
```

### Hello World
1. Access the web interface at `http://localhost:8000`.
2. Follow the on-screen prompts to create your first user account (this account will be the admin).
3. Click **Add Board** in the sidebar.
4. Select a template like "Project Tasks" or start with an "Empty Board".
5. Drag and drop cards between columns (e.g., "To Do" to "In Progress") to see the Kanban flow in action.

## CLI examples
The `focalboard-server` binary handles imports and administrative tasks:

```bash
# Import a Trello archive into Focalboard
./focalboard-server import trello trello_export.json

# Reset the password for a specific user
./focalboard-server reset-password <username>

# Check the version of the Focalboard server
./focalboard-server version
```

## API examples
The Boards API allows for programmatic task and board management. Authentication requires a session token.

### Python Example
```python
import requests

# Fetch all boards for the authenticated user
url = "http://localhost:8000/api/v1/boards"
headers = {"Authorization": "Bearer YOUR_SESSION_TOKEN"}

response = requests.get(url, headers=headers)
if response.ok:
    boards = response.json()
    for board in boards:
        print(f"Board: {board['title']} (ID: {board['id']})")
```

### Curl Example
```bash
# Get the current user's information
curl -H "Authorization: Bearer <your_session_token>" \
     "http://localhost:8000/api/v1/users/me"
```

## Related tools / concepts
- [Vikunja](vikunja.md) — A modern, actively maintained task management alternative.
- [Kanboard](https://kanboard.org/) — A minimalist self-hosted Kanban board.
- [Nextcloud](nextcloud.md) — Offers a "Deck" app with similar Kanban functionality.
- [Gitea](gitea.md) — Provides built-in issue boards for code projects.
- [Trilium](trilium.md) — For deep personal knowledge management and notes.
- [Trello](https://trello.com/) — The cloud-based inspiration for Kanban boards.
- [Mattermost](https://mattermost.com/) — The parent project for Focalboard.
- [Obsidian](../tools/ai_knowledge/obsidian.md) — For complementary note-taking.

## Links
- [Official Website](https://www.focalboard.com/)
- [GitHub Repository](https://github.com/mattermost/focalboard)

## Backlog
- Sync with Nextcloud Tasks.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-07-15

## Sources / References
- [GitHub README](https://github.com/mattermost/focalboard#readme)
- [Developer Guide](https://developers.mattermost.com/contribute/focalboard/)
