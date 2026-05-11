# Vikunja

## What it is
Vikunja is an open-source, self-hosted To-do list application that allows you to organize all your tasks on all platforms. It features Kanban boards, Gantt charts, table views, and a powerful filter system.

## What problem it solves
Maintaining a consistent task list across devices while maintaining privacy can be challenging with commercial tools. Vikunja provides an enterprise-grade task management experience that you can host yourself, ensuring your data remains private while offering the flexibility to manage everything from simple groceries to complex project timelines.

## Where it fits in the stack
**Category**: Services / Task Management. It serves as the **operational coordination layer**, managing actionable items and deadlines that result from higher-level knowledge and planning.

## Typical use cases
- **Personal Task Management**: Using the web or mobile interface to track daily chores, shopping lists, and reminders.
- **Project Planning**: Utilizing Gantt charts and Kanban boards to visualize multi-stage projects with dependencies.
- **Automated Ingestion**: Creating tasks automatically via API from emails, chat messages, or CI/CD pipelines.
- **Collaborative Lists**: Sharing specific task lists with family members or team colleagues for joint coordination.

## Strengths
- **Multiple Views**: Seamlessly switch between List, Kanban, Gantt, and Table views for the same set of tasks.
- **Task Relations**: Robust support for subtasks, dependencies (blocking/blocked by), and related tasks.
- **Rich Filtering**: A powerful query language for creating smart views based on tags, dates, and priorities.
- **Self-Hosted Privacy**: Full control over data with OIDC support for secure family-wide access.

## Limitations
- **Mobile App State**: While the PWA is excellent, the native mobile apps are still in active development and may lack some advanced features.
- **Feature Density**: The sheer number of features (relations, namespaces, teams) can be overwhelming for users seeking a simple checklist.
- **Resource Usage**: Requires a database (Postgres/MySQL) and an API backend, making it heavier than "flat-file" task managers.

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

## Task Relations
Vikunja allows linking tasks together with various relation types.

### Available Relation Types
| Type | Description | Opposite |
| :--- | :--- | :--- |
| **Subtask** | The task is a subtask of another. | Parent task |
| **Parent task** | The task is a parent of another. | Subtask |
| **Blocking** | The task blocks another task. | Blocked by |
| **Blocked by** | The task is blocked by another. | Blocking |
| **Precedes** | The task comes before another. | Follows |
| **Follows** | The task comes after another. | Precedes |
| **Related** | Tasks are related (symmetric). | Related |
| **Duplicate of** | The task is a duplicate of another. | Duplicates |
| **Duplicates** | The task duplicates another. | Duplicate of |
| **Copied from** | The task was copied from another. | Copied to |
| **Copied to** | The task was copied to another. | Copied from |

### API Endpoint
Task relations are managed via the `/tasks/{id}/relations` endpoint.

## SSO & OIDC Integration
Vikunja supports OIDC for Single Sign-On via [Authentik](authentik.md).

### Configuration (`config.yml`)
Add the following to your `config.yml`:

```yaml
auth:
  openid:
    enabled: true
    providers:
      authentik:
        name: "Authentik"
        authurl: "https://authentik.example.com/application/o/vikunja/"
        clientid: "<Your Client ID>"
        clientsecret: "<Your Client Secret>"
        scope: "openid profile email"
```

In Authentik, configure the Redirect URI as: `https://vikunja.example.com/auth/openid/authentik`

## Backlog
- Sync with CalDAV (Radicale).

## Sources / References

- [Official Documentation](https://vikunja.io/docs/)
- [CLI Reference](https://vikunja.io/docs/cli/)

## Related tools / concepts
- [Radicale](radicale.md) — For CalDAV sync of tasks.
- [Habitica](habitica.md) — For gamified task management.
- [Focalboard](focalboard.md) — For an alternative Kanban-focused tool.
- [Nextcloud](nextcloud.md) — For tasks integrated into a larger suite.
- [Authentik](authentik.md) — For managing Vikunja SSO/OIDC.
- [n8n](n8n.md) — For automating task creation from emails or chats.
- [Email-to-Calendar](../playbooks/email-to-calendar.md) — Complementary playbook for scheduling.
- [Vikunja Task Routing](../reference-implementations/llm-prompts/vikunja-task-routing.md) — LLM patterns for automated task classification.

## Contribution Metadata

- Last reviewed: 2025-05-15
- Confidence: high
