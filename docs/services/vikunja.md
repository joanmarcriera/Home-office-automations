# Vikunja

Vikunja is an open-source, self-hosted To-do list application.

## Description
It allows you to organize all your tasks on all platforms. It features boards, lists, and a powerful filter system.

## When to use it
- When you need a powerful, self-hosted To-do list with support for Kanban boards, Gantt charts, and list views.
- For managing complex personal tasks with subtasks, labels, and relations.
- When you want a task manager that is accessible via web, desktop, and mobile (via PWA or third-party apps).

## When not to use it
- If you only need a very simple, single-list checklist (Vikunja might have more features than you need).
- If you are looking for a full project management suite with deep resource allocation and financial tracking.

## Getting started

### Docker
To get Vikunja up and running quickly with Docker:

```bash
docker run -p 3456:3456 -v $PWD/files:/app/vikunja/files -v $PWD/db:/db vikunja/vikunja
```

### Hello World
1. Navigate to `http://localhost:3456` to access the web interface.
2. Create your first account (the first user created is an admin by default).
3. Create your first **Project** and add a **Task** to see Vikunja in action.

## CLI examples

When running in Docker, execute commands using `docker exec`:

```bash
# List all registered users
docker exec <container_name> /app/vikunja/vikunja user list

# Create a new user from the command line
docker exec <container_name> /app/vikunja/vikunja user create --username newuser --email user@example.com --password secret

# Create a full dump (backup) of the database and files
docker exec <container_name> /app/vikunja/vikunja dump

# Run a series of diagnostic checks
docker exec <container_name> /app/vikunja/vikunja doctor
```

## API examples
Vikunja provides a comprehensive REST API. Authenticate using an API token or a Bearer token in the `Authorization` header.

### Python Example
```python
import requests

url = "http://localhost:3456/api/v1/tasks"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN"
}

response = requests.get(url, headers=headers)
print(response.json())
```

### Curl Example
```bash
curl -H "Authorization: Bearer <your_api_token>" \
     "http://localhost:3456/api/v1/tasks"
```

Use your own private Vikunja base URL here. Do not commit instance-specific URLs, project IDs, or tokens into this repository.

## Links
- [Official Website](https://vikunja.io/)
- [Documentation](https://vikunja.io/docs/)

## Alternatives
- [Focalboard](focalboard.md)
- [Nextcloud Tasks](nextcloud.md)

## Backlog
- Sync with CalDAV (Radicale).

## Sources / References

- [Official Documentation](https://vikunja.io/docs/)
- [CLI Reference](https://vikunja.io/docs/cli/)

## Contribution Metadata

- Last reviewed: 2026-03-15
- Confidence: high
