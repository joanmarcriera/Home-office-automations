# Open WebUI Computer (cptr)

## What it is
Open WebUI Computer (also known as `cptr`) is an open-source, terminal-native AI agent and remote workstation surface designed to allow Large Language Models (LLMs) to control your computer. Engineered with a mobile-first philosophy, it serves a complete desktop interface—comprising files, shell sessions, git state, and web browser tabs—to any browser or client. It exposes an OpenAI-compatible agent API and natively integrates with Model Context Protocol (MCP 3.1 / FastMCP 3.1) servers to execute complex, long-horizon tool and system workflows directly on the host machine.

## What problem it solves
Managing and executing developer workflows on a local or remote host usually requires navigating multiple disconnected interfaces, such as terminal multiplexers, IDEs, and browser windows. When AI agents are introduced, they often operate in isolated sandboxes without direct access to the real development environment, leading to context loss and execution errors. Open WebUI Computer bridges this gap by unifying file management, terminal state, git control, and browser automation into a single, cohesive canvas. It enables AI agents to work securely and directly within the developer's actual environment without heavy virtualization or sandbox constraints.

## Where it fits in the stack
**Automation & Orchestration Layer / Agentic Surface**. Open WebUI Computer serves as the bridging runtime and UI layer between frontier LLMs (via API keys or local runtimes) and the operating system's underlying shell and filesystem.

## System Architecture

```
                    +------------------------------------+
                    |  Web Browser / Mobile Client / UI  |
                    +-----------------+------------------+
                                      |
                     Tailscale Mesh / HTTPS (Bearer Token)
                                      |
                    +-----------------v------------------+
                    |    Open WebUI Computer Gateway    |
                    |     (OpenAI Compatible API)        |
                    +-----------------+------------------+
                                      |
                        FastMCP 3.1 Tool Transport
                                      |
          +---------------------------+---------------------------+
          |                           |                           |
+---------v---------+       +---------v---------+       +---------v---------+
| Terminal / Shell  |       | Git State Manager |       | Playwright Engine |
| Execution Context |       |  Visual Staging   |       | Headless Browser  |
+-------------------+       +-------------------+       +-------------------+
```

### Agentic Loop & Computer Vision Event Flow

```
Agent Loop / FastMCP Gateway       cptr Workspace Runtime          OS Shell / Browser
           |                                  |                               |
           |---- 1. Dispatch OS Action ------>|                               |
           |     (Click / Keypress / Shell)   |---- 2. Execute Shell/Input -->|
           |                                  |                               |
           |                                  |<--- 3. Command Output / Stderr|
           |<--- 4. Capture Frame / Screenshot|                               |
           |     & Screen Coordinates         |                               |
           |                                  |                               |
           |---- 5. Analyze Image/DOM --------|                               |
           |     (Vision Reasoning Turn)      |                               |
```

## Feature & Workstation Surface Comparison Matrix

| Feature / Dimension | Open WebUI Computer (`cptr`) | Claude Desktop CLI | Devin / OpenHands Workspace |
| :--- | :--- | :--- | :--- |
| **Interface Surface** | Mobile-First Web UI + Terminal | Desktop GUI App + CLI | Web IDE Canvas |
| **Tool Protocol** | Native FastMCP 3.1 & SKILL.md | Native MCP Client | Proprietary / Sandbox Agent API |
| **Deployment Model** | Self-Hosted Docker / Local Python | Local Binary Installation | Cloud Docker Container |
| **API Server Capability**| OpenAI `/v1/chat/completions` Router | None (Client only) | REST Agent Dispatch API |
| **Browser Automation** | Built-in Playwright Engine | Extension dependent | Built-in Browser Container |

## Typical use cases
- **Mobile Workstation Access**: Pushing git commits, managing Docker containers, or editing source code directly from a phone or tablet.
- **Autonomous Coding Agent Sessions**: Triggering an LLM (such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, or **Qwen 3.6 VL**) to execute local tests, read compile errors, apply code changes, and push fixes.
- **Remote Systems Administration**: Running shell tasks, managing backups, and editing configuration files via secure messaging bots (Telegram, Discord, Slack) connected to the host machine.
- **Multimodal Web Scraping & Automation**: Instructing an agent to navigate websites, handle authentication, fill out forms, and capture screenshots using an automated browser.

## Strengths
- **Persistent Sessions**: Terminal processes and agent execution keep running in the background even if the browser tab is closed or disconnected.
- **Mobile-First Design**: A responsive interface crafted specifically for touch inputs, swipe gestures, and portrait layouts.
- **Extensible Agent Capabilities**: Built-in agentic modes supporting web search, voice control (speech-to-text/text-to-speech), reasoning trace rendering (e.g., FastMCP 3.1 thought blocks), and custom instruction sets (SKILL.md files).
- **Gateway API Integration**: Exposes an `/v1/chat/completions` API that turns any workspace into an OpenAI-compatible model, making it easy to plug into larger multi-agent frameworks.
- **Comprehensive Tooling**: Out-of-the-box support for visual git staging/diffs, syntax-highlighted code editing, file searching, and multi-pane terminal layouts.

## Limitations
- **No Per-User Isolation**: Exposing the UI provides root/user-level access equivalent to an open SSH port on the host machine, making it unsuitable for multi-tenant, untrusted user hosting.
- **High Resource Requirements**: Running browser automation, local inference, or background agent pipelines simultaneously requires substantial CPU, GPU, and VRAM resources.
- **Security Warning**: Exposing the instance to the public internet without secure VPN/tunnels (like Tailscale) or proper JWT/credential guards poses a major security hazard.

## When to use it
- When you need a lightweight, self-hosted, web-accessible development workspace that works beautifully on mobile screens.
- When orchestrating complex agentic tasks where the AI must have direct read/write access to files and local terminal environments.
- For secure, remote administration of home lab resources and self-hosted automation containers.

## When not to use it
- If multiple untrusted users require access to the same container/machine (due to the lack of strict tenant sandboxing).
- If you are operating under highly locked-down security compliance constraints where local shell execution by AI is strictly prohibited.
- For purely conversational AI workflows that do not require tool calling or local file/command execution.

## Getting started

### Quickstart Installation
Install the package using pip or uv, and spin up the server:

```bash
# Install with recommended MCP dependencies
pip install 'cptr[mcp]'

# Run the Open WebUI Computer server
cptr run --host 0.0.0.0 --port 8000
```

### Docker Compose Configuration
For standard homelab deployments, running `cptr` alongside your model router or local LLM server is the recommended pattern.

```yaml
services:
  cptr:
    image: ghcr.io/open-webui/computer:latest
    container_name: cptr
    ports:
      - "8000:8000"
    volumes:
      - cptr-data:/data
      - /home/user/workspace:/workspace
    working_dir: /workspace
    environment:
      - OPENAI_API_BASE=http://litellm:4000/v1
      - OPENAI_API_KEY=your-api-key-here
    restart: unless-stopped

volumes:
  cptr-data:
```

## CLI examples
The `cptr` CLI command provides simple administration controls:

```bash
# Bind to all network interfaces to allow mobile access on local Wi-Fi
cptr run --host 0.0.0.0 --port 8000

# Start cptr with diagnostic logging enabled
cptr run --log-level debug --log-format json

# Use uvx to run cptr instantly without permanent global installation
uvx cptr@latest run
```

## FastMCP 3.1 Computer Interaction Server

Below is a complete FastMCP 3.1 server implementation for programmatic computer action dispatching, terminal command validation, and screenshot capturing using Pydantic v2 schemas.

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Server Tool for Open WebUI Computer Automation & Control
"""

import os
import sys
import httpx
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ValidationError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cptr-automation-gateway", version="1.4.0")

CPTR_BASE_URL = os.getenv("CPTR_BASE_URL", "http://localhost:8000")
CPTR_API_TOKEN = os.getenv("CPTR_API_TOKEN", "workspace-bearer-token")

class ShellExecutionParams(BaseModel):
    workspace_id: str = Field("default", pattern=r"^[a-zA-Z0-9_\-]+$")
    command: str = Field(..., min_length=2, max_length=1000, description="Shell command payload")
    timeout_seconds: int = Field(30, ge=1, le=300, description="Command execution timeout in seconds")

class ExecutionOutputPayload(BaseModel):
    workspace_id: str
    exit_code: int = Field(0, description="Return code of shell process")
    stdout: str = Field("", description="Standard output log")
    stderr: str = Field("", description="Standard error log")
    execution_time_ms: float = Field(..., description="Wall-clock execution time")

@mcp.tool()
async def run_workspace_terminal_command(
    command: str,
    workspace_id: str = "default",
    timeout_seconds: int = 30
) -> Dict[str, Any]:
    """
    Executes a shell command inside an Open WebUI Computer workspace with Pydantic v2 schema enforcement.
    """
    try:
        params = ShellExecutionParams(
            workspace_id=workspace_id,
            command=command,
            timeout_seconds=timeout_seconds
        )
    except ValidationError as err:
        return {"error": f"Invalid parameter schema: {err.json()}"}

    headers = {
        "Authorization": f"Bearer {CPTR_API_TOKEN}",
        "Content-Type": "application/json"
    }

    url = f"{CPTR_BASE_URL}/api/v1/workspaces/{params.workspace_id}/terminal/execute"
    payload = {
        "command": params.command,
        "timeout": params.timeout_seconds
    }

    async with httpx.AsyncClient(timeout=float(params.timeout_seconds + 5)) as client:
        try:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

            out_schema = ExecutionOutputPayload(
                workspace_id=params.workspace_id,
                exit_code=data.get("exitCode", 0),
                stdout=data.get("stdout", ""),
                stderr=data.get("stderr", ""),
                execution_time_ms=data.get("executionTimeMs", 0.0)
            )
            return out_schema.model_dump()

        except Exception as exc:
            return {"error": f"Execution request failed: {str(exc)}"}

if __name__ == "__main__":
    mcp.run()
```

## API examples

### Gateway Chat Completion Request
Open WebUI Computer acts as an OpenAI-compatible server. You can dispatch prompt/message lists directly to your workspace:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer workspace-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "workspace-agent",
    "messages": [
      {
        "role": "user",
        "content": "Analyze the codebase structure and draft a README.md file in the project root."
      }
    ]
  }'
```

### Dynamic Shell Command Invocation (Python Client with FastMCP 3.1 & Pydantic v2)
To satisfy technical robustness requirements and KnowledgeOps contract compliance in early 2027, shell command execution requests are strictly validated using Pydantic v2 before transmission.

```python
import requests
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

# 1. Define strict validation schemas using Pydantic v2
class TerminalCommand(BaseModel):
    command: str = Field(..., min_length=2, max_length=500, description="Shell command to execute.")
    timeout_seconds: int = Field(default=30, ge=1, le=300, description="Execution timeout limit.")
    task_id: Optional[str] = Field(None, alias="taskId", description="FastMCP 3.1 Task Protocol context ID.")

class ExecutionRequest(BaseModel):
    workspace_id: str = Field(default="default", pattern=r"^[a-zA-Z0-9_\-]+$")
    payload: TerminalCommand

# 2. Programmatic execution utilizing validation and cptr REST API
def execute_cptr_command(request_data: dict) -> str:
    try:
        # Strict validation of input using Pydantic v2
        request = ExecutionRequest.model_validate(request_data)
    except ValidationError as e:
        print(f"Execution request schema validation failed: {e}")
        raise

    url = f"http://localhost:8000/api/v1/workspaces/{request.workspace_id}/terminal/execute"
    headers = {
        "Authorization": "Bearer workspace-api-token",
        "Content-Type": "application/json"
    }

    # Post verified schema (serialized with mode="json")
    response = requests.post(url, json=request.payload.model_dump(mode="json"), headers=headers)
    response.raise_for_status()
    return response.json().get("output", "")

# Example invocation
if __name__ == "__main__":
    payload = {
        "workspace_id": "prod-environment",
        "payload": {
            "command": "git diff --stat",
            "timeout_seconds": 15,
            "taskId": "task-cptr-2027-0107"
        }
    }
    try:
        output = execute_cptr_command(payload)
        print(f"Command executed successfully. Output:\n{output}")
    except Exception as e:
        pass
```

## Production Systemd Service Unit (`open-webui-computer.service`)

Deploying the Open WebUI Computer service on Linux workstations using systemd:

```ini
[Unit]
Description=Open WebUI Computer Agent Workstation Daemon
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=simple
User=cptr-runner
Group=cptr-runner
WorkingDirectory=/home/cptr-runner/workspace
Environment=OPENAI_API_BASE=http://127.0.0.1:4000/v1
Environment=OPENAI_API_KEY=sk-local-litellm-key
ExecStart=/usr/local/bin/cptr run --host 127.0.0.1 --port 8000 --log-format json
Restart=always
RestartSec=5s
LimitNOFILE=65536
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
ProtectSystem=full
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Diagnostic Troubleshooting Matrix

| Issue / Symptom | Probable Cause | Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **Terminal Commands Hang indefinitely** | Subprocess waiting for interactive stdin input | `cptr run --log-level debug` | Pass `-y` or `--non-interactive` flags to shell tools (e.g., `apt-get -y install`). |
| **Playwright Browser Launch Fails** | Missing system dependencies (X11 / Chromium libs) | `playwright install-deps` | Run `playwright install --with-deps chromium` in container / host runtime. |
| **HTTP 401 Unauthorized Gateway Error** | API token mismatch in client request header | `curl -Iv http://localhost:8000/v1/models` | Verify Bearer token in request header matches `CPTR_API_TOKEN` environment variable. |
| **Out of Memory on Vision Capture** | Concurrent high-res screenshot rendering consuming RAM | `free -h` / `dmesg \| grep oom` | Set lower resolution canvas limits in `cptr` configuration file. |

## Operational Security Hardening & Deployment Guidelines

- **Tailscale Overlay Network**: Never expose `cptr` port `8000` directly to public IP addresses without protection. Bind the daemon to a Tailscale mesh IP (`100.x.y.z`) or localhost behind an authenticating reverse proxy.
- **Dedicated Service User**: Run `cptr` under an unprivileged host system user account (e.g. `cptr-runner`) to limit blast radius in case of untrusted tool execution.
- **Command Exclusion Rules**: Use workspace shell wrapper scripts to restrict dangerous destructive commands (e.g. `rm -rf /`, `dd`, `mkfs`) when allowing autonomous loop execution.
- **FastMCP 3.1 Telemetry Auditing**: Enable JSON structured event logging (`--log-format json`) to record full prompt, shell command execution, and tool parameter history for compliance auditing.

## Related tools / concepts
- [Open WebUI](../../services/open-webui.md) — The main parent conversational user interface that can integrate `cptr` as a gateway backend.
- [Ollama](../../services/ollama.md) — Local LLM runner to serve models like Gemma 4 and DeepSeek-V4 directly to your agent.
- [Model Context Protocol (MCP)](mcp.md) — The standardization protocol used by `cptr` to load and interact with external systems (FastMCP 3.1).
- [LiteLLM](../../services/litellm.md) — Useful proxy router to aggregate model endpoints (Anthropic, OpenAI, local) for cptr consumption.
- [Browser Use](browser-use.md) — Multi-agent browser automation framework similar to the built-in browser capabilities in Open WebUI Computer.
- [Playwright MCP Server](playwright-mcp.md) — A specialized tool server enabling agents to scrape and parse complex websites.
- [CliHub](clihub.md) — Unified CLI tooling platform for consolidating command interfaces.
- [Tailscale](../../services/tailscale.md) — Secure overlay mesh network to safely access your workstation from anywhere in the world.

## Sources / References
- [GitHub: Open WebUI Computer](https://github.com/open-webui/computer)
- [Official Documentation: Open WebUI Computer Integration](https://docs.openwebui.com/ecosystem/computer/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/introduction)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
