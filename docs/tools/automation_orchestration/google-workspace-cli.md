# Google Workspace CLI (gws)

## What it is
Google Workspace CLI (`gws`) is a dynamic command-line tool for interacting with all Google Workspace services (Drive, Gmail, Calendar, Sheets, etc.), built for both humans and AI agents like Claude 4.8 Opus and GPT-5.5.

## What problem it solves
It eliminates the need to write custom `curl` calls or complex API glue code for Google Workspace tasks. By building its command surface dynamically from Google's Discovery Service, it ensures 100% API coverage and provides structured JSON output that is perfect for agentic consumption.

## Where it fits in the stack
**Automation & Orchestration / SaaS Automation CLI**. It acts as a bridge between terminal workflows, CI/CD pipelines, and frontier AI agents needing direct access to Workspace data.

## Typical use cases
- Automating Workspace administration (user management, permissions).
- Performing complex operations across Drive, Sheets, and Gmail via scripts.
- Providing AI agents with a "skill" to manage calendars or draft emails directly.
- Migrating data or creating templated project structures in Drive.

## Strengths
- **Full API Coverage**: Dynamically generated from Google's Discovery Service.
- **Agent-Ready**: Structured JSON output and 100+ included "skills" for LLM integration.
- **Helper Commands**: Includes high-level helpers (prefixed with `+`) for common tasks like `+agenda` or `+send`.
- **Security**: Supports OAuth 2.0, service accounts, and encrypted credential storage.

## Limitations
- Requires initial OAuth setup which can be complex for new users.
- Subject to Google Workspace API rate limits and quotas.
- Dynamic command generation can result in verbose command paths for some services.

## When to use it
- When you need a reliable, scriptable interface for Google Workspace.
- When integrating Google Workspace with autonomous AI agents.
- When you need to automate recurring administrative tasks across the Workspace suite.

## When not to use it
- For occasional manual actions (use the web UI).
- If you are not comfortable managing Google Cloud project credentials or OAuth flows.

## Getting started

### 1. Installation
Install via `npm` or download a pre-built binary:
```bash
npm install -g @googleworkspace/cli
```

### 2. Setup
Initialize and create your Google Cloud project credentials:
```bash
gws auth setup
```

### 3. Login
Authenticate your session:
```bash
gws auth login
```

## CLI examples
```bash
# Show today's agenda using the helper command
gws calendar +agenda

# Send an email with a helper command
gws gmail +send --to user@example.com --subject "2026 Audit" --body "Draft attached."

# List files in a specific Drive folder
gws drive files list --params '{"q": "'\''folder-id'\'' in parents"}'
```

## API examples
While primarily a CLI, agents use the structured JSON output to reason about Workspace state:
```bash
# Agents can introspect schemas
gws schema drive.files.list
```
> [!NOTE]
> For direct API integration, use the standard Google Workspace client libraries or the included AI agent skills.

## Related tools / concepts
- [Google Calendar](../calendar_tasks/google_calendar.md)
- [n8n](../../services/n8n.md)
- [Zapier](zapier.md)
- [Make](make.md)
- [Gemini Canvas](../ai_knowledge/gemini-canvas.md)
- [Chronos MCP](chronos-mcp.md)
- [Claude Code](../development_ops/claude-code.md)
- [OpenClaw](../development_ops/openclaw.md)

## Sources / References
- [Google Workspace CLI GitHub](https://github.com/googleworkspace/cli)
- [Google API Discovery Service](https://developers.google.com/discovery)

## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high
