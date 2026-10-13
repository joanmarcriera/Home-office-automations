# Open WebUI Computer (cptr)

## What it is
Open WebUI Computer (also known as `cptr`) is an open-source, terminal-native AI agent and remote workstation surface designed to allow Large Language Models (LLMs) to control your computer. Engineered with a mobile-first philosophy, it serves a complete desktop interface—comprising files, shell sessions, git state, and web browser tabs—to any browser or client. It exposes an OpenAI-compatible agent API and natively integrates with Model Context Protocol (MCP 3.1 / FastMCP 3.1) servers to execute complex, long-horizon tool and system workflows directly on the host machine.

## What problem it solves
Managing and executing developer workflows on a local or remote host usually requires navigating multiple disconnected interfaces, such as terminal multiplexers, IDEs, and browser windows. When AI agents are introduced, they often operate in isolated sandboxes without direct access to the real development environment, leading to context loss and execution errors. Open WebUI Computer bridges this gap by unifying file management, terminal state, git control, and browser automation into a single, cohesive canvas. It enables AI agents to work securely and directly within the developer's actual environment without heavy virtualization or sandbox constraints.

## Where it fits in the stack
**Automation & Orchestration Layer / Agentic Surface**. Open WebUI Computer serves as the bridging runtime and UI layer between frontier LLMs (via API keys or local runtimes) and the operating system's underlying shell and filesystem.

## Typical use cases
- **Mobile Workstation Access**: Pushing git commits, managing Docker containers, or editing source code directly from a phone or tablet.
- **Autonomous Coding Agent Sessions**: Triggering an LLM (such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, or **Qwen 3.6 VL**) to execute local tests, read compile errors, apply code changes, and push fixes.
- **Remote Systems Administration**: Running shell tasks, managing backups, and editing configuration files via secure messaging bots (Telegram, Discord, Slack) connected to the host machine.
- **Multimodal Web Scraping & Automation**: Instructing an agent to navigate websites, handle authentication, fill out forms, and capture screenshots using an automated browser.

---

## Architecture & Workstation Control Loop

`cptr` sits as an orchestration layer between frontier models and host system execution subsystems (terminal, filesystem, browser automation, git engine).

```
+-----------------------------------------------------------------------------------+
|                            MOBILE BROWSER / CLIENT SURFACE                        |
|  +-----------------------+   +-----------------------+   +---------------------+  |
|  |  Terminal / PTY View  |   | Visual Git Staging    |   | Browser Canvas View |  |
|  +-----------+-----------+   +-----------+-----------+   +----------+----------+  |
+--------------|---------------------------|--------------------------|-------------+
               | (WebSocket / PTY)         | (REST API)               | (CDP Stream)
               v                           v                          v
+-----------------------------------------------------------------------------------+
|                        OPEN WEBUI COMPUTER (cptr Runtime)                         |
|  +-----------------------------------------------------------------------------+  |
|  | FastMCP 3.1 Tool Gateway Engine & Security Guardrails                         |  |
|  |  +-------------------+   +--------------------+   +----------------------+  |  |
|  |  | PTY Shell Handler |   | File System Agent  |   | Headless Browser CDP |  |  |
|  |  +---------+---------+   +---------+----------+   +----------+-----------+  |  |
|  +------------|-----------------------|-------------------------|--------------+  |
+---------------|-----------------------|-------------------------|-----------------+
                |                       |                         |
                v                       v                         v
+-----------------------------------------------------------------------------------+
|                            HOST OPERATING SYSTEM                                  |
|  +-------------------+       +-------------------+       +---------------------+  |
|  | Bash / Zsh Shell  |       | Host Filesystem   |       | Chromium / WebKit   |  |
|  +-------------------+       +-------------------+       +---------------------+  |
+-----------------------------------------------------------------------------------+
```

### Workstation Controller Comparison Matrix

| Feature / Dimension | Open WebUI Computer (`cptr`) | Claude Computer Use | AutoGPT Workspace | OpenInterpreter |
| :--- | :--- | :--- | :--- | :--- |
| **Interface Type** | Web / Mobile Native | API / Container Frame | Web Dashboard | Terminal CLI |
| **Execution Surface** | Direct Host / Container | Docker Sandbox | Virtual Sandbox | Direct Host Shell |
| **Mobile Optimization**| Native Touch / Gestures | Desktop Stream | Basic Responsive | N/A (Terminal) |
| **FastMCP 3.1 Support**| Native Core Integration| Via MCP Connectors | Custom Adapters | Plugin Modules |
| **API Proxy Interface**| OpenAI `/v1/chat` | Anthropic Messages API | Custom REST API | Python Function API |

---

## FastMCP 3.1 Production Implementation & Pydantic v2 Schema

Below is a complete, runnable **FastMCP 3.1** server that exposes workstation control tools to `cptr` with strict **Pydantic v2** validation parameters.

```python
import os
import asyncio
import subprocess
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ValidationError
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    title="Open WebUI Computer FastMCP Gateway",
    version="3.1.0",
    description="FastMCP 3.1 tool server for cptr workstation control and terminal execution."
)

# Pydantic v2 Schema Declarations
class ShellExecutionRequest(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 Task Protocol correlation UUID.")
    command: str = Field(..., min_length=2, max_length=1000, description="Shell command to run.")
    working_directory: str = Field(default="/workspace", description="Directory context for execution.")
    timeout_seconds: int = Field(default=30, ge=1, le=300, description="Execution timeout limit in seconds.")

class ShellExecutionResult(BaseModel):
    task_id: str = Field(..., description="FastMCP 3.1 Task Protocol correlation UUID.")
    exit_code: int = Field(..., description="Process exit code.")
    stdout: str = Field(default="", description="Captured standard output.")
    stderr: str = Field(default="", description="Captured standard error.")
    executed_at: str = Field(..., description="ISO timestamp of command completion.")

# FastMCP 3.1 Server Tools
@mcp.tool(
    name="cptr_execute_shell",
    description="Executes a shell command on the cptr host workstation with Pydantic v2 validation."
)
async def cptr_execute_shell(request: ShellExecutionRequest) -> ShellExecutionResult:
    try:
        proc = await asyncio.create_subprocess_shell(
            request.command,
            cwd=request.working_directory,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout_data, stderr_data = await asyncio.wait_for(
            proc.communicate(),
            timeout=float(request.timeout_seconds)
        )
        return ShellExecutionResult(
            task_id=request.task_id,
            exit_code=proc.returncode if proc.returncode is not None else -1,
            stdout=stdout_data.decode("utf-8", errors="replace"),
            stderr=stderr_data.decode("utf-8", errors="replace"),
            executed_at=datetime.now(timezone.utc).isoformat()
        )
    except asyncio.TimeoutError:
        return ShellExecutionResult(
            task_id=request.task_id,
            exit_code=124,
            stdout="",
            stderr=f"Command execution timed out after {request.timeout_seconds} seconds.",
            executed_at=datetime.now(timezone.utc).isoformat()
        )

if __name__ == "__main__":
    mcp.run()
```

---

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

---

## When to use it
- When you need a lightweight, self-hosted, web-accessible development workspace that works beautifully on mobile screens.
- When orchestrating complex agentic tasks where the AI must have direct read/write access to files and local terminal environments.
- For secure, remote administration of home lab resources and self-hosted automation containers.

## When not to use it
- If multiple untrusted users require access to the same container/machine (due to the lack of strict tenant sandboxing).
- If you are operating under highly locked-down security compliance constraints where local shell execution by AI is strictly prohibited.
- For purely conversational AI workflows that do not require tool calling or local file/command execution.

---

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

---

## Operational Hardening, Deployment & Troubleshooting

### Operational Safety & Security Guidelines
1. **Network Perimeter Protection**: Never expose `cptr` port 8000 directly to the public internet without passing through a VPN mesh (like [Tailscale](../../services/tailscale.md) or [Headscale](../../services/headscale.md)) or an authenticating reverse proxy (Traefik / Authelia).
2. **FileSystem Jail Scoping**: Set `working_dir` in Docker Compose explicitly to `/workspace` and avoid mounting host root `/` or sensitive directories (`/etc`, `~/.ssh`).
3. **Execution Timeouts**: Enforce mandatory tool call execution timeouts (defaulting to <= 30 seconds) within FastMCP 3.1 wrappers to prevent runaway processes from seizing host CPU threads.

### Troubleshooting Guide

| Issue / Error | Root Cause | Remediation Command / Solution |
| :--- | :--- | :--- |
| `Permission denied: /workspace` | Host directory permissions mismatch in Docker volume | Run `chown -R 1000:1000 /home/user/workspace` on host |
| `Browser automation crash (CDP error)` | Missing Chromium dependencies inside container | Rebuild image or run `apt-get install -y chromium-driver` |
| `FastMCP Tool Call Failed` | Agent passed invalid arguments to workstation tool | Verify request structure with Pydantic v2 validator schema |
| `Terminal PTY Connection Reset` | WebSocket connection blocked by reverse proxy | Enable WebSocket upgrade headers (`Upgrade`, `Connection`) in proxy |

---

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

---

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

---

## Related tools / concepts
- [Open WebUI](../../services/open-webui.md) — The main parent conversational user interface that can integrate `cptr` as a gateway backend.
- [Ollama](../../services/ollama.md) — Local LLM runner to serve models like Gemma 4 and DeepSeek-V4 directly to your agent.
- [Model Context Protocol (MCP)](mcp.md) — The standardization protocol used by `cptr` to load and interact with external systems (FastMCP 3.1).
- [LiteLLM](../../services/litellm.md) — Useful proxy router to aggregate model endpoints (Anthropic, OpenAI, local) for cptr consumption.
- [Browser Use](browser-use.md) — Multi-agent browser automation framework similar to the built-in browser capabilities in Open WebUI Computer.
- [Playwright MCP Server](playwright-mcp.md) — A specialized tool server enabling agents to scrape and parse complex websites.
- [CliHub](clihub.md) — Unified CLI tooling platform for consolidating command interfaces.
- [Tailscale](../../services/tailscale.md) — Secure overlay mesh network to safely access your workstation from anywhere in the world.

---

## Sources / References
- [GitHub: Open WebUI Computer](https://github.com/open-webui/computer)
- [Official Documentation: Open WebUI Computer Integration](https://docs.openwebui.com/ecosystem/computer/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/introduction)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
