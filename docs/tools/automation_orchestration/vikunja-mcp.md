# Vikunja MCP Server

## What it is
A Model Context Protocol (MCP) server that enables AI assistants like **Gemma 3**, **Llama 4**, **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Qwen 3.6** to interact with Vikunja task management instances.

## What problem it solves
It allows agents to manage tasks, projects, labels, and teams directly within a Vikunja instance, bridging the gap between autonomous assistants and self-hosted productivity tools. It supports both API token and JWT authentication for varying levels of access.

## Where it fits in the stack
**Tool / Automation**. It provides a domain-specific interface for task management operations within the [MCP](mcp.md) ecosystem.

## Typical use cases
- Managing personal task lists and projects via natural language.
- Automating project management workflows in a team environment.
- Batch importing tasks from CSV or JSON files.
- Exporting project data for backup or migration.

## Strengths
- **Subcommand-based tools**: Provides an intuitive structure for AI interaction.
- **Session-based authentication**: Automatically handles token management.
- **Production-ready resilience**: Uses circuit breakers and Zod-based validation for stability.
- **MCP 3.1 / FastMCP 3.1 Compatible**: Supports the latest Task Protocol and routing logic.

## Limitations
- User-specific endpoints require JWT authentication (browser-extracted).
- Some team operations are limited by the underlying Vikunja API.
- Webhook subscriptions for real-time updates are still in the roadmap.

## When to use it
- When you use Vikunja for task management and want to integrate it with MCP-compatible assistants.
- When you need to automate complex task creation or project hierarchy management.
- When you require secure, validated access to your task data.

## When not to use it
- If your task management system does not support the Vikunja API.
- If you require real-time push notifications from Vikunja to your agent (use webhooks directly).

## Getting started

Vikunja MCP is most commonly run on-demand using `npx` within your MCP client configuration (such as Claude Desktop).

### Authentication Setup
The server supports two authentication modes:
1. **API Token Authentication (Default)**: Best for general automation and task management. Create a token in Vikunja Settings → API Tokens. Format starts with `tk_`.
2. **JWT Authentication (Advanced)**: Enables user profile modifications and data exports. Extract the `token` key value from your browser's Local Storage for your Vikunja domain. Format starts with `eyJ`.

### 1. Installation
The server runs headless via Node.js or `npx`:

```bash
# Verify the package launches correctly
npx -y @democratize-technology/vikunja-mcp
```

### 2. Client Configuration (Claude Desktop)
Add the server configuration block to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vikunja-mcp": {
      "command": "npx",
      "args": ["-y", "@democratize-technology/vikunja-mcp"],
      "env": {
        "VIKUNJA_URL": "https://tasks.yourdomain.com/api/v1",
        "VIKUNJA_API_TOKEN": "tk_your_api_token_here"
      }
    }
  }
}
```

### Hello World Example
Test connection status by authenticating and listing your active tasks across all projects:

```bash
# Set environment variables
export VIKUNJA_URL="https://tasks.yourdomain.com/api/v1"
export VIKUNJA_API_TOKEN="tk_your_api_token"

# List tasks via MCP-compatible schema testing
npx @democratize-technology/vikunja-mcp
```

## CLI examples
You can tune the runtime environment, rate limits, and circuit breakers of the MCP server using environment flags:

```bash
# 1. Start the server with verbose debug logs written to stderr
DEBUG=true LOG_LEVEL=debug npx @democratize-technology/vikunja-mcp

# 2. Apply strict API rate limits to protect your self-hosted instance from DoS
RATE_LIMIT_ENABLED=true RATE_LIMIT_PER_MINUTE=60 npx @democratize-technology/vikunja-mcp

# 3. Connect using a browser-extracted JWT token to unlock advanced user tools
VIKUNJA_API_TOKEN="eyJhbGciOiJIUzI1..." npx @democratize-technology/vikunja-mcp
```

## API examples

### Programmatic Setup with Pydantic v2 Validation
To maintain the structural integrity and validation standards of task operations in late 2026, inputs to Vikunja MCP should be explicitly verified. Below is a robust Python script implementing strict **Pydantic v2** schema checks.

```python
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from datetime import datetime

# 1. Define schemas using strict Pydantic v2 annotations
class VikunjaTaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=250, description="The title of the task.")
    description: Optional[str] = Field(default=None, description="Detailed markdown task description.")
    project_id: int = Field(..., gt=0, description="The target project ID.")
    due_date: Optional[datetime] = Field(default=None, description="ISO-8601 formatted due date and time.")
    priority: int = Field(default=3, ge=1, le=5, description="Priority level from 1 (lowest) to 5 (highest).")
    repeat_after: Optional[int] = Field(default=None, ge=1, description="Interval number of days/weeks to repeat task.")
    repeat_mode: Optional[str] = Field(default=None, pattern="^(day|week|month|year)$")
    labels: List[int] = Field(default_factory=list, description="List of label IDs to apply.")

class VikunjaTaskResponse(BaseModel):
    id: int
    title: str
    project_id: int
    done: bool = False
    created_by_id: int
    created_at: datetime
    updated_at: datetime

# 2. Programmatic creation utilizing validation
def process_task_creation_request(payload: dict) -> str:
    try:
        # Strict validation of input using Pydantic v2
        task_request = VikunjaTaskCreate.model_validate(payload)
    except ValidationError as e:
        print(f"Validation failed: {e}")
        raise

    print(f"Creating task '{task_request.title}' in project {task_request.project_id}...")

    # Simulating API response from Vikunja
    simulated_api_response = {
        "id": 42019,
        "title": task_request.title,
        "project_id": task_request.project_id,
        "done": False,
        "created_by_id": 101,
        "created_at": "2026-12-24T12:00:00Z",
        "updated_at": "2026-12-24T12:00:00Z"
    }

    try:
        # Validate output payload to ensure it conforms to expectations
        validated_response = VikunjaTaskResponse.model_validate(simulated_api_response)
        return f"Successfully created Vikunja task {validated_response.id}: {validated_response.title}"
    except ValidationError as e:
        print(f"Output schema validation error: {e}")
        raise

# Example invocation in late 2026
if __name__ == "__main__":
    payload = {
        "title": "Weekly Security Audit",
        "description": "Perform dependency and container scans",
        "project_id": 1,
        "due_date": "2026-12-31T10:00:00Z",
        "priority": 4,
        "repeat_after": 7,
        "repeat_mode": "day",
        "labels": [12]
    }
    result = process_task_creation_request(payload)
    print(result)
```

## Related tools / concepts
- [Vikunja](../../services/vikunja.md)
- [Model Context Protocol](mcp.md)
- [Nextcloud](../../services/nextcloud.md)
- [Gitea](../../services/gitea.md)
- [Paperless-ngx](../../services/paperless-ngx.md)
- [Google Calendar](../calendar_tasks/google_calendar.md)
- [MCP Registry](mcp-registry.md)
- [Chronos MCP](chronos-mcp.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Vikunja MCP GitHub](https://github.com/democratize-technology/vikunja-mcp)
- [Vikunja API Documentation](https://vikunja.io/docs/api/)

## Contribution Metadata
- Last reviewed: 2026-12-24
- Confidence: high