# Focalboard

> [!WARNING]
> This repository is currently not maintained. If you're interested in becoming a maintainer, please let the Mattermost community know. This documentation refers to the standalone Personal Server edition.

Focalboard is an open-source, multilingual, self-hosted project management tool.

## Description
It is an alternative to Trello, Notion, and Asana, providing a Kanban-style board for task management. It comes in two primary editions: Personal Desktop (standalone app) and Personal Server (multi-user server).

## When to use it
- When you need a self-hosted, open-source alternative to Trello or Asana for team project management.
- When you prefer a Kanban-style interface for organizing tasks and projects.
- For managing personal projects or small team workflows with a lightweight server.

## When not to use it
- If you require deep integration with the full Mattermost suite but don't want to run the Mattermost server itself (use the plugin edition instead).
- If you need advanced document editing and database features similar to Notion (Focalboard is more focused on task boards).

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

## Links
- [Official Website](https://www.focalboard.com/)
- [GitHub Repository](https://github.com/mattermost/focalboard)

## Alternatives
- [Kanboard](https://kanboard.org/)
- [Vikunja](vikunja.md)

## Backlog
- Sync with Nextcloud Tasks.

## Sources / References
- [GitHub README](https://github.com/mattermost/focalboard#readme)
- [Developer Guide](https://developers.mattermost.com/contribute/focalboard/)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-04
