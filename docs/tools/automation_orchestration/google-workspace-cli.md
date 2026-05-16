# Google Workspace CLI

## What it is
Google Workspace CLI (`gws`) is a command-line project for interacting with Google Workspace services (Drive, Docs, Sheets, Calendar, etc.) from scripts and terminal workflows.

## What problem it solves
It reduces friction when automating Google Workspace tasks that would otherwise require manual console work or complex custom API glue code. It provides a standardized, discoverable interface to the vast Google Workspace API surface.

## Where it fits in the stack
**Automation & Orchestration / SaaS Automation CLI**. It is useful when Google Workspace actions need to plug into repeatable scripts, CI/CD pipelines, or broader automation systems.

## Typical use cases
- Workspace administration (user management, permissions) from scripts.
- Automating Google Docs, Sheets, Drive, or related workflows.
- Integrating Workspace operations into broader automation systems (e.g., creating a project folder and tracker sheet on command).

## Getting started

### Installation
Install the CLI using the pre-compiled binaries or via Cargo:

```bash
cargo install google-workspace-cli
```

### Authentication
The CLI uses OAuth 2.0 for authentication. You will need to create a project in the Google Cloud Console, enable the Workspace APIs, and download your `credentials.json`.

```bash
# Initialize and authenticate
gws login --client-id <YOUR_CLIENT_ID> --client-secret <YOUR_CLIENT_SECRET>
```

### Basic Commands
List files in Google Drive:
```bash
gws drive files list
```

## Usage examples

### Drive: Creating a Project Folder
```bash
gws drive files create --name "New Project 2026" --mime-type "application/vnd.google-apps.folder"
```

### Sheets: Updating a Cell
```bash
gws sheets spreadsheets values update <SPREADSHEET_ID> A1 --value "Project Status: Active"
```

### Calendar: Listing Events
```bash
gws calendar events list primary --time-min "2026-05-16T00:00:00Z"
```

## Architecture notes

The upstream project is more dynamic than a typical Google API CLI:

- The `gws` command surface is generated at runtime from Google Discovery Service JSON documents.
- It deliberately avoids generated per-service Rust crates for standard Workspace APIs.
- Adding a new supported service is mainly a registration problem in the service map and discovery layer, not a code-generation problem across many bindings.

That architecture makes the CLI unusually adaptable for broad Workspace coverage, but it also means reliability depends on discovery-document handling and careful runtime parsing rather than static generated clients.

## Strengths
- CLI-friendly workflow for a widely used business platform.
- Extremely broad API coverage due to its discovery-driven architecture.
- Good fit for automation-heavy operations and rapid prototyping.

## Limitations
- Still subject to Workspace API and OAuth 2.0 auth complexity.
- Best for teams already comfortable with service-account or OAuth setups.
- Runtime command generation can sometimes lead to verbose or non-intuitive command paths compared to hand-rolled CLIs.

## When to use it
- When Google Workspace is part of your operational automation surface.
- When you need to automate one-off or recurring Workspace tasks without writing a full application.

## When not to use it
- When you only need occasional manual actions (use the web UI).
- For extremely high-throughput operations where a dedicated optimized client might be preferred.

## Selection comments
- Use Google Workspace CLI when Google tools are part of the company operating system, not just ad hoc utilities.
- It is best used as a reliable execution layer beneath [n8n](../../services/n8n.md), not as the only orchestration system.
- Pair it with [Gemini Canvas](../ai_knowledge/gemini-canvas.md) or [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md) when the workflow mixes document creation with AI-assisted drafting.

## Related tools / concepts
- [Google Calendar](../calendar_tasks/google_calendar.md)
- [n8n](../../services/n8n.md)
- [Zapier](zapier.md)
- [Make](make.md)
- [Gemini Canvas](../ai_knowledge/gemini-canvas.md)
- [Gemini CLI](../ai_knowledge/gemini-cli.md)
- [Chronos MCP](chronos-mcp.md)
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md)

## Sources / References
- [GitHub Repository](https://github.com/googleworkspace/cli)
- [Google Discovery Service](https://developers.google.com/discovery)

## Contribution Metadata
- Last reviewed: 2026-05-16
- Confidence: high
