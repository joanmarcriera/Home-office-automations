# Picnic

## What it is
Picnic is a structured, project-centered GUI built on top of [OpenClaw](../development_ops/openclaw.md) for managing notes, files, goals, and AI-assisted workflows in a calm environment.

## What problem it solves
Raw agent environments can be chaotic and overwhelming. Picnic provides a human-friendly interface for [OpenClaw](../development_ops/openclaw.md), allowing users to organize work into projects and keep sensitive browsing behavior isolated within Picnic's own built-in browser. It makes AI collaboration safer and more deliberate for [Gemma 3](../ai_knowledge/local_llms.md), Claude 4.8 Opus, and GPT-5.5 users.

## Where it fits in the stack
**Automation runtime / desktop orchestration layer**. Picnic sits above the [OpenClaw](../development_ops/openclaw.md) core, providing a structured workspace for business, personal, and family work.

## Typical use cases
- Organizing complex business projects with AI-assisted notes and files.
- Running browser-based agent workflows safely using the built-in browser.
- Maintaining long-term context for family planning or personal journals.
- Collaborative thinking and planning where structure emerges over time.

## Strengths
- **Project Isolation**: Keeps work organized and prevents context drift.
- **Built-in Browser**: Isolates agent browsing from your primary browser session.
- **Gradual Structure**: Start with a blank page and add context cards only when needed.
- **Open Source Core**: Leverages the power and public scrutiny of [OpenClaw](../development_ops/openclaw.md).
- **MCP 3.0 Integration**: Native support for [MCP](mcp.md) tool discovery and execution.

## Limitations
- Still in beta; features and project structures are subject to change.
- Primarily GUI-driven; lacks a robust public-facing CLI or API for direct manipulation.
- Requires local resources to run the desktop application and underlying agent runtime.

## When to use it
- When you want a calmer, more organized interface for your AI work.
- When you need to manage multiple projects without mixing their context.
- When safety and browser isolation are high priorities.

## When not to use it
- If you require a headless, API-only automation engine (use [OpenClaw](../development_ops/openclaw.md) directly).
- If you prefer a simple chat interface without project management features.

## Getting started
Picnic is built on top of OpenClaw and can be deployed locally alongside its agentic daemon to programmatically coordinate projects and automation tools.

To install and run the local Picnic workspace companion server:
```bash
git clone https://github.com/openclaw/picnic.git
cd picnic
npm install
npm run start-daemon
```

Configure your local user workspace behavior by editing or creating the standard configuration file at `~/.config/picnic/config.json`:
```json
{
  "openclaw_host": "http://localhost:8000",
  "default_model": "gemma-3-27b",
  "project_directory": "~/picnic-projects",
  "sandbox_enabled": true
}
```

## CLI examples
The Picnic daemon exposes CLI commands for managing workspace states, checking daemon health, and verifying connection to the OpenClaw backbone:

### 1. Start Picnic Daemon on a Custom Port
```bash
npm run daemon -- --port 8080 --host 127.0.0.1
```

### 2. Verify OpenClaw Backend Connection
```bash
curl http://localhost:8080/api/health
```

### 3. Backup Picnic Workspace Projects
```bash
tar -czf picnic_backup.tar.gz ~/picnic-projects/
```

## API examples
Picnic exposes a local REST API via its daemon, allowing developer agents to manipulate active workspace files and query cards. Below is a Python script that programmatically reads active project directories from the workspace:

### 1. Python: Query Active Picnic Workspace Projects
```python
import os
import requests

def get_active_projects(daemon_url: str) -> list:
    endpoint = f"{daemon_url}/api/projects"
    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to Picnic daemon: {e}")
        return []

if __name__ == "__main__":
    picnic_url = os.environ.get("PICNIC_DAEMON_URL", "http://localhost:8080")
    print(f"Connecting to Picnic daemon at {picnic_url}...")
    projects_list = get_active_projects(picnic_url)
    if projects_list:
        print("Retrieved Projects:")
        for proj in projects_list:
            print(f"- {proj.get('name', 'Unnamed Project')} ({proj.get('status', 'active')})")
    else:
        print("No active projects found or daemon is offline.")
```

## Related tools / concepts
- [OpenClaw](../development_ops/openclaw.md)
- [Browser Use](browser-use.md)
- [n8n](../../services/n8n.md)
- [Home Assistant](../../services/home-assistant.md)
- [LiteLLM](../../services/litellm.md)
- [ClawRouter](../infrastructure/clawrouter.md)
- [OpenClaw Security Operations](../../knowledge_base/patterns/openclaw-security-operations.md)
- [Claude Code](../development_ops/claude-code.md)
- [Model Context Protocol](mcp.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Picnic Official Site](https://picnicos.com/)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
