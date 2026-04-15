# Focalboard

Focalboard is an open-source, multilingual, self-hosted project management tool.

## Description
It is an alternative to Trello, Notion, and Asana, providing a Kanban-style board for task management.

## When to use it
- When you need a self-hosted, open-source alternative to Trello or Asana for team project management.
- When you prefer a Kanban-style interface for organizing tasks and projects.
- For managing personal projects or small team workflows with a lightweight server.

## When not to use it
- If you require deep integration with the full Mattermost suite but don't want to run the Mattermost server itself (use the plugin edition instead).
- If you need advanced document editing and database features similar to Notion (Focalboard is more focused on task boards).

## Getting started

### Docker
To run Focalboard locally using the official Docker image:

```bash
docker run -it -p 80:8000 mattermost/focalboard
```

### Hello World
1. Access the interface at `http://localhost`.
2. Follow the on-screen prompts to create your first user account.
3. Click **Add Board** in the sidebar and select a template (e.g., "Project Tasks") to create your first Kanban board.

## CLI examples
Focalboard provides an import tool and can be managed via `make` for development:

```bash
# Import a Trello archive into Focalboard
./bin/focalboard-server import trello trello_export.json

# Build the server and web app (requires Go and Node.js)
make prebuild && make

# Reset the admin password (if supported by your version)
./bin/focalboard-server reset-password admin
```

## API examples
The Boards API (Swagger) allows for programmatic task and board management.

### Python Example
```python
import requests

# Use your session token obtained after login
url = "http://localhost:8000/api/v1/boards"
headers = {"Authorization": "Bearer YOUR_SESSION_TOKEN"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    for board in response.json():
        print(f"Board Name: {board['title']}")
```

### Curl Example
```bash
# Get all boards
curl -H "Authorization: Bearer <your_session_token>" \
     "http://localhost:8000/api/v1/boards"
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
- Last reviewed: 2026-03-02
