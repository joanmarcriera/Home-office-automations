# Picnic

## What it is
Picnic is a structured, project-centered GUI built on top of [OpenClaw](../development_ops/openclaw.md) for managing notes, files, goals, and AI-assisted workflows in a calm, focused environment. Designed specifically to interface with modern agentic architectures, it simplifies workspace management for power users and orchestrates multi-modal AI interactions seamlessly using the **FastMCP 3.1** Task Protocol.

## What problem it solves
Raw agent environments can be chaotic, leading to context drift, resource exhaustion, and complex setup requirements. Picnic provides a human-focused, reliable interface for [OpenClaw](../development_ops/openclaw.md), allowing users to organize work into logical, project-bound workspaces. It keeps sensitive browsing behavior isolated within Picnic's own built-in browser engine and structures AI collaboration deliberately for frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

## Where it fits in the stack
**Automation runtime / desktop orchestration layer**. Picnic sits above the [OpenClaw](../development_ops/openclaw.md) core, providing a structured workspace for business, personal, and family automation tasks.

## Typical use cases
- **Multi-Agent Project Scaffolding**: Organizing complex business projects with AI-assisted notes and partitioned files.
- **Isolated Browser Agent Runs**: Running browser-based agent workflows safely using the built-in Chromium sandbox.
- **Context Preservation**: Maintaining long-term context for family planning, personal development, or engineering journals without token bloat.
- **Collaborative Ideation**: Structured brainwriting and planning where structured cards, tasks, and notes emerge over time with model-guided curation.

## Strengths
- **Project Isolation**: Keeps tasks organized under strict directories to prevent cross-contamination.
- **Sandbox Browser**: Isolates agent browsing from your primary host system's cookies and sessions.
- **Gradual Context Cards**: Start with a clean, low-clutter canvas and add rich content cards as projects evolve.
- **OpenClaw Backbone**: Leverages the power, security protocols, and community review of the underlying [OpenClaw](../development_ops/openclaw.md) system.
- **FastMCP 3.1 Compliance**: Native support for early 2027 Model Context Protocol standard discovery, task tracking, and dynamic client handshakes.

## Limitations
- **GUI Overhead**: Lacks the lightning-fast headless response of CLI-only agent runs.
- **Local Compute Demands**: Requires substantial local hardware capabilities if running local model runtimes alongside the desktop companion.
- **Sync Latency**: Heavy database and file state sync can introduce minor UI lockups during massive agent folder updates.

## When to use it
- When you want a structured, distraction-free visual environment for complex agentic workflows.
- When managing multiple concurrent client or personal projects where context mixing must be strictly forbidden.
- When executing web-browsing tasks where host browser isolation is a high priority.

## When not to use it
- For headless, automated cron-like automation workflows (use [OpenClaw](../development_ops/openclaw.md) or [n8n](../../services/n8n.md) directly).
- If you prefer a barebones, single-session CLI terminal chat interface.

## Getting started
Picnic connects directly to a running OpenClaw instance or can launch its own local workspace companion daemon to coordinate tools and filesystem resources.

To install and initialize the companion daemon locally:
```bash
git clone https://github.com/openclaw/picnic.git
cd picnic
npm install
npm run start-daemon
```

Configure your user workspace settings inside the companion daemon's standard JSON configuration file at `~/.config/picnic/config.json`:
```json
{
  "openclaw_host": "http://localhost:8000",
  "default_model": "qwen-3.6-72b",
  "project_directory": "~/picnic-projects",
  "sandbox_enabled": true
}
```

## CLI examples
The Picnic companion daemon features command-line utility tools to facilitate remote administration and daemon configuration checks:

### 1. Launch Daemon on Custom Host/Port
```bash
picnic-companion --port 8085 --host 127.0.0.1
```

### 2. Quick Ping to Check Daemon Health
```bash
curl http://127.0.0.1:8085/api/health
```

### 3. Compress and Backup Local Projects
```bash
tar -czf picnic_backup.tar.gz -C ~/ picnic-projects/
```

## API examples
Picnic exposes a secure REST API via its local daemon, allowing developers to query active projects, inspect metadata, and inject workspace cards. Below is a Python script that retrieves active projects and validates the workspace schemas utilizing **Pydantic v2** and **FastMCP 3.1** task context parameters:

### 1. Python: Query and Validate Picnic Projects
```python
import os
from typing import List, Optional
import requests
from pydantic import BaseModel, Field, ValidationError

# Define strict schemas matching Picnic's early 2027 API contract with FastMCP 3.1 task protocol support
class ProjectSchema(BaseModel):
    id: str = Field(..., description="Unique alphanumeric identifier for the project")
    name: str = Field(..., min_length=2, max_length=100, description="The display name of the project")
    status: str = Field("active", description="Active status of the workspace (e.g., active, archived, suspended)")
    model_alignment: str = Field(..., description="Frontier model mapped to this project, e.g., Claude 5.6")
    card_count: int = Field(default=0, ge=0, description="Total count of workspace context cards")

class PicnicWorkspace(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 Task Protocol correlation tracking ID.")
    projects: List[ProjectSchema] = Field(..., description="List of projects present in the active Picnic workspace")

def fetch_and_validate_workspace(daemon_url: str, task_id: str = "task-picnic-2027-0107") -> Optional[PicnicWorkspace]:
    endpoint = f"{daemon_url}/api/projects"
    try:
        response = requests.get(endpoint, timeout=5)
        response.raise_for_status()
        raw_data = response.json()

        # Wrap raw JSON in expected schema structure and validate using Pydantic v2
        workspace_data = {"task_id": task_id, "projects": raw_data}
        validated_workspace = PicnicWorkspace.model_validate(workspace_data)
        return validated_workspace
    except requests.exceptions.RequestException as e:
        print(f"Connection failure to Picnic daemon: {e}")
        return None
    except ValidationError as e:
        print(f"Data validation failed. The API contract does not match our schema: {e}")
        return None

if __name__ == "__main__":
    picnic_url = os.environ.get("PICNIC_DAEMON_URL", "http://localhost:8085")
    print(f"Initializing connection to Picnic daemon at: {picnic_url}...")

    workspace = fetch_and_validate_workspace(picnic_url)
    if workspace:
        print(f"[Task {workspace.task_id}] Successfully validated {len(workspace.projects)} active projects:")
        for project in workspace.projects:
            print(f"- {project.name} | Status: {project.status} | Model: {project.model_alignment} | Cards: {project.card_count}")
    else:
        print("Failed to retrieve or validate workspace projects.")
```

## Related tools / concepts
- [OpenClaw](../development_ops/openclaw.md) — The fundamental orchestration backend.
- [Browser Use](browser-use.md) — Web navigation library.
- [n8n](../../services/n8n.md) — Self-hosted workflow orchestration engine.
- [Home Assistant](../../services/home-assistant.md) — Smart home controller.
- [ClawRouter](../infrastructure/clawrouter.md) — Advanced routing and sandboxing wrapper.
- [OpenClaw Security Operations](../../knowledge_base/patterns/openclaw-security-operations.md) — Standard enterprise hardiness guides.
- [Claude Code](../development_ops/claude-code.md) — Developer-focused CLI companion.
- [Model Context Protocol](mcp.md) — Standardized tool and resource sharing protocol.
- [Local LLMs](../ai_knowledge/local_llms.md) — Local model inference tooling.

## Sources / References
- [Picnic Official Website](https://picnicos.com/)
- [OpenClaw Project Repository](https://github.com/openclaw/openclaw)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
