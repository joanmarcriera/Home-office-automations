# Google Tasks

## What it is
Google Tasks is a lightweight, low-latency task management service integrated natively within the Google Workspace ecosystem. As of late July 2026, it serves as a critical "Surface" for autonomous task execution and state tracking via the [Model Context Protocol (MCP 3.1)](../automation_orchestration/mcp.md) and the Google Graph API, enabling frontier models (such as Claude 5.1, GPT-5.5, and Gemini 3.5 Pro/Ultra) to dynamically manage and synchronize to-do items across Gmail, Calendar, and mobile devices.

## What problem it solves
It solves the issue of task fragmentation across multi-agent pipelines and human-in-the-loop (HITL) workflows. By offering a minimalist, high-availability capture point, Google Tasks allows [Autonomous Agents](../agents/README.md) to convert conversational or email context into structured, actionable items, ensuring that autonomous sub-tasks remain visible and manageable in the user's daily productivity environment.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management. It acts as the "Durable Task and Execution Tracking Layer" for Google-native agentic environments, sitting directly between the **Orchestration Layer** (powered by tools like [LangGraph](../frameworks/langgraph.md)) and the user's personal organization interface.

## Typical use cases
- **Agentic Orchestration**: An agent powered by [Gemini Spark](../ai_knowledge/google-gemini.md) identifying actionable tasks in an incoming email and programmatically creating them in Google Tasks.
- **Workflow Automation**: Using [n8n](../../services/n8n.md) to synchronize [GitHub Issues](../development_ops/github.md) or git commits to a personal Google Tasks list.
- **Contextual Capture**: Automatically transforming [Google Calendar](google_calendar.md) event action items or follow-ups into tasks.
- **Unified Task Ingestion**: Utilizing the [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md) to append system alerts or cron job failures to a designated administrative queue.

## Strengths
- **Native Ecosystem Integration**: Deep, out-of-the-box integration with Gmail, Google Calendar, and Google Drive.
- **MCP 3.1 Compatibility**: Out-of-the-box support for the official Google MCP server, allowing LLMs to perform schema-validated tool-calling with proper auth boundaries.
- **Minimalist Interface**: Low-overhead design focused on ultra-fast retrieval and completion.
- **Reliable Synchronization**: Instantaneous synchronization across web interfaces, sidebars, and dedicated mobile applications.

## Limitations
- **Limited Metadata Support**: Lacks advanced project management capabilities such as arbitrary nesting depth (limited to a single subtask level), custom tags/labels, or complex priority fields.
- **Basic Collaboration**: Sharing and assigning tasks within shared lists is heavily restricted compared to enterprise tools like [Todoist](todoist.md) or [TickTick](ticktick.md).
- **Rich Text Limits**: Note fields are limited to plaintext with no native Markdown or rich-text formatting support.

## When to use it
- When operating primarily within a Google Workspace-centric home-office or enterprise ecosystem.
- For managing low-complexity, personal task lists requiring visibility in [Google Calendar](google_calendar.md).
- When configuring agentic workflows that require a simple, high-reliability, and low-latency task storage backend.

## When not to use it
- For enterprise-grade or multi-member team project management (consider using [Gitea](../../services/gitea.md) or [Linear](../enterprise/linear.md)).
- If your task workflows rely heavily on tags, custom filters, kanban views, or complex dependency charts.
- If your system-wide notes or tasks are fundamentally Markdown-based (consider [Obsidian](../ai_knowledge/obsidian.md) or [Logseq](../ai_knowledge/logseq.md)).

## Getting started
1. **Access Google Tasks**: Open Google Tasks directly within the Gmail or Google Calendar sidebar, or download the dedicated mobile app.
2. **Enable the API**: Navigate to the [Google Cloud Console](https://console.cloud.google.com/), create a project, and enable the Google Tasks API.
3. **Configure OAuth 2.0 credentials**: Set up your OAuth consent screen and download the `credentials.json` file.
4. **Deploy MCP Server**: For LLM integration, launch the official Google Tasks MCP server with your authorized token.

## CLI examples

### Using Google Workspace CLI
```bash
# List all tasks within the default task list
gworkspace tasks list --status all

# Create a new task with a due date and notes
gworkspace tasks create \
  --title "Review home-office network diagrams" \
  --notes "Focus on MCP 3.1 gateway security and routing rules" \
  --due "2026-08-01T12:00:00Z"
```

### Using MCP 3.1 Tool Call (JSON-RPC)
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "google_tasks_create_task",
    "arguments": {
      "tasklist": "@default",
      "title": "Upgrade LLM evaluation runner to lm-eval v0.4.x+",
      "notes": "Verify multi-GPU pipeline optimization across Claude 5.1 and GPT-5.5"
    }
  },
  "id": 1
}
```

## API examples

### Python (Google API Client v2 with OAuth Flow)
```python
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/tasks']

def get_tasks_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('tasks', 'v1', credentials=creds)

def create_task(title, notes=None, due_date=None):
    service = get_tasks_service()
    task_body = {
        'title': title,
        'notes': notes
    }
    if due_date:
        task_body['due'] = due_date # Format: YYYY-MM-DDTHH:MM:SS.000Z

    result = service.tasks().insert(tasklist='@default', body=task_body).execute()
    print(f"Successfully created task: {result.get('title')} (ID: {result.get('id')})")
    return result

if __name__ == "__main__":
    create_task(
        title="Verify MCP 3.1 Server Connections",
        notes="Check token expiration and active scopes on Google Cloud Console",
        due_date="2026-07-31T23:59:59.000Z"
    )
```

### Node.js (MCP 3.1 Tool Handlers with TypeScript)
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { google } from "googleapis";

const oauth2Client = new google.auth.OAuth2(
  process.env.CLIENT_ID,
  process.env.CLIENT_SECRET,
  process.env.REDIRECT_URI
);
oauth2Client.setCredentials({ refresh_token: process.env.REFRESH_TOKEN });

const tasksService = google.tasks({ version: 'v1', auth: oauth2Client });

export function registerTasksTools(server: Server) {
  server.setRequestHandler(
    "tools/call",
    async (request) => {
      const { name, arguments: args } = request.params;

      if (name === "google_tasks_create") {
        const { title, notes } = args as { title: string; notes?: string };
        try {
          const res = await tasksService.tasks.insert({
            tasklist: '@default',
            requestBody: { title, notes },
          });
          return {
            content: [{ type: "text", text: `Created task: ${res.data.title} (ID: ${res.data.id})` }]
          };
        } catch (error: any) {
          return {
            isError: true,
            content: [{ type: "text", text: `Error: ${error.message}` }]
          };
        }
      }
      throw new Error(`Tool ${name} not found`);
    }
  );
}
```

## Related tools / concepts
- [Google Calendar](google_calendar.md)
- [Todoist](todoist.md)
- [TickTick](ticktick.md)
- [n8n](../../services/n8n.md)
- [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md)
- [Chronos MCP](../automation_orchestration/chronos-mcp.md)
- [Gemini](../ai_knowledge/google-gemini.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Microsoft To Do](microsoft-todo.md)

## Sources / References
- [Google Tasks Official Support](https://support.google.com/tasks/answer/7675772)
- [Google Tasks API Reference](https://developers.google.com/workspace/tasks)
- [Google Cloud Console Project Settings](https://console.cloud.google.com/)
- [Model Context Protocol (MCP) v3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-07-24
- Confidence: high
