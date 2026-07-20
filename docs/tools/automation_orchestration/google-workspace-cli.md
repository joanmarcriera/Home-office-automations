# Google Workspace CLI (gws)

## What it is
Google Workspace CLI (`gws`) is a dynamic command-line tool for interacting with all Google Workspace services (Drive, Gmail, Calendar, Sheets, etc.), built for both humans and AI agents like [Gemma 3](../ai_knowledge/local_llms.md), Claude 4.8 Opus, and GPT-5.5.

## What problem it solves
It eliminates the need to write custom `curl` calls or complex API glue code for Google Workspace tasks. By building its command surface dynamically from Google's Discovery Service, it ensures 100% API coverage and provides structured JSON output that is perfect for agentic consumption.

## Where it fits in the stack
**Automation & Orchestration / SaaS Automation CLI**. It acts as a bridge between terminal workflows, CI/CD pipelines, and frontier AI agents needing direct access to Workspace data via the [Model Context Protocol](mcp.md).

## Typical use cases
- Automating Workspace administration (user management, permissions).
- Performing complex operations across Drive, Sheets, and Gmail via scripts.
- Providing AI agents with a "skill" to manage calendars or draft emails directly.
- Migrating data or creating templated project structures in Drive.

## Strengths
- **Full API Coverage**: Dynamically generated from Google's Discovery Service.
- **Agent-Ready**: Structured JSON output and 100+ included "skills" for LLM integration.
- **MCP 3.0 Support**: Can be exposed as an MCP server using specialized adapters.
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

### Installation
You can install `gws` via NPM, Homebrew, Cargo, or Nix:

```bash
# Recommended for Node environments
npm install -g @googleworkspace/cli

# On macOS and Linux via Homebrew
brew install googleworkspace-cli

# From source using Cargo
cargo install --git https://github.com/googleworkspace/cli --locked

# Run instantly using Nix
nix run github:googleworkspace/cli
```

### Setup & Authentication
To use `gws`, you must configure a Google Cloud project with OAuth credentials:

1. **Automatic Setup**:
   ```bash
   gws auth setup   # Automatically guides you through GCP project config
   ```
2. **Login & Scopes**:
   Select individual services to stay within unverified app limits (Google limits unverified OAuth consent screens to ~25 scopes):
   ```bash
   gws auth login --scopes drive,gmail,calendar
   ```

> [!WARNING]
> If your OAuth application is in "Testing" mode, you **must** add your Google Account email as a "Test user" under the GCP Console → APIs & Services → OAuth consent screen, otherwise authentication will fail with a generic `Access blocked` or `403` error.

### Hello World Example
Retrieve your most recent Google Drive files formatted in structured JSON to verify a successful connection:

```bash
gws drive files list --params '{"pageSize": 5}'
```

## CLI examples
The CLI features built-in custom commands prefixed with `+` (such as `+agenda` and `+send`) that wrap complex, multi-step API workflows:

```bash
# 1. Fetch today's calendar agenda formatted in your account's timezone
gws calendar +agenda

# 2. Append rows dynamically to a Google Sheet with shell escaping protection
gws sheets +append --spreadsheet "SPREADSHEET_ID" --values "Alice,95"

# 3. Send a thread-aware email via Gmail
gws gmail +send --to recipient@example.com --subject "Automation Update" --body "Task completed successfully via gws CLI."
```

## API examples
`gws` outputs standard, structured JSON to stdout. AI agents or external scripts can programmatically inspect API endpoint schemas or export headless credentials for automated runs:

### Schema Introspection
To dynamically build payload structures, query the schema definition of any target method:
```bash
gws schema drive.files.list
```

### Programmatic Credential Usage (Python Integration)
Complete interactive login on your workstation, export the token securely, and reuse it inside an automated script:

```python
import subprocess
import json

# Export the plaintext credentials from your local OS keyring
try:
    result = subprocess.run(
        ["gws", "auth", "export", "--unmasked"],
        capture_output=True,
        text=True,
        check=True
    )
    credentials = json.loads(result.stdout)
    access_token = credentials.get("access_token")
    print(f"Programmatic access token retrieved: {access_token[:10]}...")
except subprocess.CalledProcessError as e:
    print(f"Failed to export gws credentials: {e.stderr}")
```

## Related tools / concepts
- [Google Calendar](../calendar_tasks/google_calendar.md)
- [n8n](../../services/n8n.md)
- [Zapier](zapier.md)
- [Make](make.md)
- [Gemini Canvas](../ai_knowledge/gemini-canvas.md)
- [Chronos MCP](chronos-mcp.md)
- [Claude Code](../development_ops/claude-code.md)
- [OpenClaw](../development_ops/openclaw.md)
- [Model Context Protocol](mcp.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Google Workspace CLI GitHub](https://github.com/googleworkspace/cli)
- [Google API Discovery Service](https://developers.google.com/discovery)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
