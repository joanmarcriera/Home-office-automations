# Focalboard

Focalboard is an open-source, multilingual, self-hosted project management tool.

## Description
It is an alternative to Trello, Notion, and Asana, providing a Kanban-style board for task management.

## Getting started

### Docker
To run Focalboard locally using the official Docker image:

```bash
docker run -it -p 80:8000 mattermost/focalboard
```

Access the interface at `http://localhost`.

## CLI examples
Focalboard is primarily a web-based application. Development and build tasks are managed via `make`:

```bash
# Build the server
make

# Run the server binary
./bin/focalboard-server

# Build the web app
make webapp
```

## API examples
The Boards API can be accessed via `curl`. Use your session token for authentication:

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
