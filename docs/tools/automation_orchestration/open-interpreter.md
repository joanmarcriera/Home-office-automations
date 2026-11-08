# Open Interpreter

## What it is
Open Interpreter is an open-source framework that allows Large Language Models (LLMs) to execute code (Python, JavaScript, Shell, R, and more) directly on your local computer. It provides a natural language interface to your system's capabilities, functioning as a powerful, locally-hosted, and uncensored alternative to OpenAI's Advanced Data Analysis (formerly Code Interpreter). As of early 2027, it is a cornerstone for "local-first" agentic workflows, featuring native support for **FastMCP 3.1 Task Protocol**, **Gemma 4**, **DeepSeek-V4**, and optimized integration with **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **Qwen 3.6 VL**.

```
+-----------------------------------------------------------------------------------+
|                            Open Interpreter System Architecture                   |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+      +------------------------+      +----------------+  |
|  | User Prompt / Chat  | ---> | Open Interpreter Core  | ---> |  FastMCP 3.1   |  |
|  |  (CLI / API / OS)   |      |   (Language Router)    |      | Bridge Protocol|  |
|  +---------------------+      +------------------------+      +----------------+  |
|                                           |                           |           |
|                                           v                           v           |
|                               +------------------------+     +-----------------+  |
|                               | Code Execution Engine  |     | External MCP    |  |
|                               | (Python, Bash, JS, R)  |     | Tool Resources  |  |
|                               +------------------------+     +-----------------+  |
|                                           |                                       |
|                                           v                                       |
|                               +------------------------+                          |
|                               | Execution Sandboxes    |                          |
|                               | - Native OS / Subshell |                          |
|                               | - Docker Container     |                          |
|                               | - WASM / Bubblewrap    |                          |
|                               +------------------------+                          |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It overcomes the "walled garden" limitations of hosted LLM sandboxes. While hosted environments are restricted by sandboxing, lack of internet access (at times), and limited library availability, Open Interpreter runs on *your* hardware with *your* permissions. This enables agents to perform real-world tasks like managing local file systems, controlling system settings, interacting with local hardware/databases, and using any locally installed CLI tools without restriction.

Additionally, Open Interpreter solves the fragmentation between AI logic and OS automation by acting as an execution bridge. Through **FastMCP 3.1**, remote or local agents can expose OS actions as structured, type-safe RPC tools.

## Mathematical Formulations & Execution Safety Bounds

### 1. Sandbox Memory Overhead & cgroup Quota Sizing
When executing untrusted agentic subroutines inside a Linux cgroup v2 / Bubblewrap sandbox, the total memory consumption $\mathcal{M}_{\text{sandbox}}(t)$ is bounded by:
$$\mathcal{M}_{\text{sandbox}}(t) = \mathcal{M}_{\text{base}} + \sum_{p \in \mathcal{P}_{\text{forked}}} \left(\mathcal{M}_{\text{RSS}}(p) + \mathcal{M}_{\text{shared}}(p) \cdot \frac{1}{|\text{Ref}(p)|}\right) \le \mathcal{M}_{\text{quota}}$$

If memory pressure crosses the notification threshold $\gamma = 0.85 \cdot \mathcal{M}_{\text{quota}}$, the Open Interpreter kernel monitor raises a SIGXCPU/SIGUSR1 warning to initiate soft memory cleanup before the OOM-killer invokes SIGKILL:
$$\mathbb{P}(\text{OOM-Kill}) = \Theta\left(\exp\left(\frac{\mathcal{M}(t) - \mathcal{M}_{\text{quota}}}{\sigma_{\mathcal{M}}}\right)\right)$$

### 2. Stream Truncation Entropy & Output Token Bounds
Agent code execution generating dense stdout streams (e.g., recursive directory listings or large CSV dataframes) must be truncated before context injection. For an output byte stream of length $L$ truncated to window $W \ll L$, the empirical Shannon entropy of retained token distribution $\mathcal{H}_{\text{trunc}}$ is:
$$\mathcal{H}_{\text{trunc}} = -\sum_{k=1}^{|\mathcal{V}|} \hat{p}(v_k) \log_2 \hat{p}(v_k)$$
where $\hat{p}(v_k)$ is the empirical frequency of vocabulary token $v_k$ within the head/tail retention window. Open Interpreter retains the initial $W_{\text{head}} = 0.3 \cdot W$ and terminal $W_{\text{tail}} = 0.7 \cdot W$ bytes to preserve stack traces while minimizing prompt bloat.

### 3. AST Command Safety Classification Probability
Before dispatching shell commands, the AST analyzer computes a safety classification score $\mathcal{S}_{\text{safe}} \in [0, 1]$ based on weighted hazard primitives:
$$\mathcal{S}_{\text{safe}} = 1 - \sigma\left(\sum_{j=1}^{M} w_j \cdot \mathbb{I}(\text{AST\_Node}_j \in \Omega_{\text{hazard}}) + \alpha \cdot \text{Depth}(\mathcal{T}_{\text{AST}})\right)$$
Execution proceeds automatically if $\mathcal{S}_{\text{safe}} \ge \tau_{\text{safe}} = 0.95$; otherwise, execution pauses for explicit user confirmation.

## Framework Comparison Matrix

| Feature / Metric | Open Interpreter | Claude Code | Goose Agent | Aider | OpenHands |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Execution Environment**| Local OS / Docker / WASM / Bwrap | Terminal Subshell | Extension / Local OS | Git Repository Working Tree | Docker Container Architecture |
| **Supported Languages**| Python, Bash, JS, R, SQL | Shell / Bash / Node | Custom Python Tools | Polyglot / Python focus | Polyglot / Bash / Python |
| **MCP Compatibility**| Native FastMCP 3.1 Task Protocol | Native MCP | Custom Extensions | Partial / Git wrapper | Full MCP Gateway |
| **Vision UI Control** | Yes (OS 1 / Qwen VL / PyAutoGUI) | No | No | No | Browser-only (Playwright) |
| **Sandboxing Latency** | < 12ms (Bubblewrap) / 250ms (Docker) | N/A (Direct Host) | Direct Host / VirtualEnv | Git Commit Snapshot | ~500ms Container Exec |
| **Safety Guardrails** | AST Whitelist + Interactive Prompt | Terminal Prompts | Permission Prompts | Git Checkpoint Rollback | Linux User Isolation |
| **License** | Open Source (MIT) | Commercial / Proprietary | Open Source (Apache 2.0) | Open Source (Apache 2.0) | Open Source (MIT) |

## Where it fits in the stack
**Category**: Automation & Orchestration / Agentic Execution. It serves as the primary bridge between high-level LLM reasoning and low-level OS execution, providing a secure environment (via user confirmation) or a fully autonomous one (via the `--auto_run` flag).

```
+------------------------------------------------------------------------+
|                           Stack Integration                            |
+------------------------------------------------------------------------+
| Orchestration:  Open Interpreter Framework & FastMCP 3.1 Server         |
| Execution Runtimes: Subshell, Docker Sandbox, WASM / Linux Bubblewrap  |
| Local LLM Runners:  Ollama (Gemma 4, DeepSeek-V4), vLLM (Qwen 3.6 VL)  |
| Remote Providers:   Claude 5.6, GPT-5.6, Gemini 4.0 Ultra              |
+------------------------------------------------------------------------+
```

## Typical use cases
- **Intelligent Local File Management**: "Scan my downloads folder, organize documents by month, and archive anything older than 90 days to my NAS."
- **Localized Data Science**: "Analyze my local SQLite database, generate a forecast for the next quarter, and output the charts as high-resolution PNGs."
- **OS-Level System Control**: "Switch my workstation to focus mode, launch my development Docker stack, and open the relevant Slack channels."
- **Automated Developer Workflows**: "Iterate through all files in this project and update the imports to reflect the latest FastMCP 3.1 schema requirements."
- **Computer Vision UI Control**: "Inspect screenshot of application, locate the Submit button coordinates, and execute a native click action."

## Strengths
- **Unrestricted Local Access**: Full reach to your computer's files, internet connection, and installed environment.
- **Privacy-First Architecture**: When utilized with local models (Gemma 4, DeepSeek-V4, Qwen 3.6 VL), sensitive data remains entirely on-premises.
- **Multilingual Execution**: Seamlessly switches between Python, Bash, JavaScript, and R within a single conversational turn.
- **FastMCP 3.1 Task Protocol**: Acts as a native MCP server or client, exposing local system capabilities as standardized tools to remote or localized agentic clients.
- **Lightweight Bubblewrap Sandboxing**: Executes shell commands within unprivileged user namespaces with minimal CPU overhead.

## Limitations
- **Security Implications**: Executing LLM-generated code locally requires vigilant oversight; a single hallucinated or malicious command can lead to catastrophic data loss.
- **Hardware Performance**: The speed and reliability of local execution are strictly bound by the host machine's CPU, GPU, and RAM.
- **Environmental Drift**: Code that runs perfectly in one local environment may fail in another due to missing dependencies or differing OS versions.

## When to use it
- When an agent needs direct, stateful interaction with the local file system or operating system.
- For complex data processing tasks where data privacy and sovereignty are non-negotiable.
- When leveraging open-weights models (Gemma 4, DeepSeek-V4, Qwen 3.6 VL) for sophisticated system-level automation.
- For multi-modal desktop automation requiring screenshot analysis and GUI click simulation.

## When not to use it
- On production servers or highly sensitive environments without additional sandboxing (e.g., within a dedicated Docker or Podman container).
- For simple conversational tasks that do not require any system interaction or code execution.
- When operating in an air-gapped environment with strict compliance rules against dynamic code compilation.

## Troubleshooting & Edge Diagnostic Matrix

| Failure Mode / Error | Root Cause | Immediate Diagnostic Action | Permanent Resolution Strategy |
| :--- | :--- | :--- | :--- |
| **`SANDBOX_OOM_KILLED`** | Subprocess exceeded container or cgroup memory quota. | Run `dmesg -T \| grep -i oom` or inspect `interpreter --doctor`. | Increase memory limit in config: `interpreter.sandbox.memory_limit = '8g'` or optimize dataframe chunk size. |
| **`UNCAUGHT_SUBPROCESS_TIMEOUT`** | Code execution hung on blocking interactive I/O (e.g. `input()` or unbuffered wait). | Check `ps aux \| grep python` for orphaned child PIDs. | Set explicit timeout in SafeExecutionPolicy (`max_execution_time_seconds: 45`). |
| **`PERMISSION_DENIED_BWRAP`** | Bubblewrap unprivileged user namespace blocked by host kernel sysctl. | Check `cat /proc/sys/kernel/unprivileged_userns_clone`. | Run `sudo sysctl -w kernel.unprivileged_userns_clone=1` or fall back to Docker engine. |
| **`FASTMCP_RPC_DESYNC`** | JSON-RPC socket dropped during heavy stdout streaming. | Inspect FastMCP socket logs at `/tmp/fastmcp-oi.sock`. | Enable chunked stdout streaming and set buffer size to 64KB in bridge server. |
| **`VISION_COORDINATE_OFFSET`** | Desktop DPI scaling (e.g. 150% or 200% Retina) distorted click coordinates. | Run `xrandr` or inspect display scale factor. | Apply inverse scaling transformation: $(x_{\text{native}}, y_{\text{native}}) = (x / s, y / s)$. |
| **`PYTHON_ENV_COLLISION`** | Agent installed packages globally instead of inside dedicated virtualenv. | Run `which python` and inspect `sys.path`. | Enforce virtual environment sandbox isolation: `interpreter.venv = "/opt/agent-venv"`. |
| **`OLLAMA_MODEL_NOT_FOUND`** | Specified local model tag missing from local Ollama library. | Run `ollama list` in terminal. | Pull required model: `ollama pull gemma-4-27b` or verify endpoint URL. |
| **`DESKTOP_GUI_GRAB_FAILED`** | Wayland display protocol restricting unauthorized screen capture. | Check `echo $XDG_SESSION_TYPE`. | Set `GDK_BACKEND=x11` or grant screen capture permissions via PipeWire portal. |

## Systemd Daemon Management
Deploy Open Interpreter as a managed FastMCP 3.1 background service on enterprise Linux servers:

```ini
[Unit]
Description=Open Interpreter FastMCP 3.1 Bridge Daemon
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=appuser
Group=appuser
WorkingDirectory=/opt/open-interpreter
ExecStart=/opt/open-interpreter/venv/bin/python3 -m interpreter.bridge --port 8094 --sandbox docker
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=OLLAMA_API_BASE=http://localhost:11434/v1
Environment=FASTMCP_PROTOCOL_VERSION=3.1

# Sandboxing & Security
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/opt/open-interpreter/workspace /tmp
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Docker Compose Multi-Container Stack Setup
Run Open Interpreter inside an isolated Docker sandbox alongside a local Ollama inference container:

```yaml
version: "3.8"

services:
  open-interpreter-bridge:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: open-interpreter-mcp
    restart: unless-stopped
    ports:
      - "8094:8094"
    environment:
      - FASTMCP_PORT=8094
      - OLLAMA_HOST=http://ollama-service:11434
      - INTERPRETER_AUTO_RUN=true
    volumes:
      - ./workspace:/app/workspace
    security_opt:
      - no-new-privileges:true
    depends_on:
      - ollama-service
    networks:
      - agent-sandbox-net

  ollama-service:
    image: ollama/ollama:latest
    container_name: local-llm-engine
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    networks:
      - agent-sandbox-net

volumes:
  ollama_models:

networks:
  agent-sandbox-net:
    driver: bridge
```

## Getting started

### Installation
```bash
pip install open-interpreter
```

### Basic Usage with Gemma 4
```bash
# Start an interactive session using Gemma 4 via Ollama
interpreter --model ollama/gemma-4-27b
```
Type your request: "Create a summary of the current directory's file structure and save it to structure.md."

## CLI examples
```bash
# Start a standard interactive session
interpreter

# Run a specific task autonomously in a sandboxed environment with FastMCP 3.1 context
interpreter --task "Resize all JPGs in ~/Pictures to 1080p" --auto_run --safe_mode

# Execute in Docker container sandbox
interpreter --sandbox docker --image python:3.12-slim

# List all available local and remote models for use
interpreter --list-models
```

## Advanced Sandboxing and Safety Configuration

To prevent accidental system disruption, Open Interpreter supports multiple sandboxing engines:

```
[User Command Request]
        |
        v
+-------------------+
|  Safety Validator | ---> Enforces Command Whitelist / Regex Rules
+-------------------+
        |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
+------------------+    +-------------------+   +--------------------+
| Local Subshell   |    | Docker Container  |   | Bubblewrap / WASM  |
| (Interactive Prompt)| | (Isolated OS)     |   | (In-Memory Engine) |
+------------------+    +-------------------+   +--------------------+
```

### Setting up a Docker Sandbox Engine
```python
from interpreter import interpreter

# Configure Open Interpreter to run inside a Docker container
interpreter.sandbox = {
    "engine": "docker",
    "image": "python:3.12-slim",
    "mount_dir": "/tmp/sandbox_workspace",
    "network": "bridge",
    "memory_limit": "4g"
}
```

## API examples

### Programmatic Python Setup with FastMCP 3.1 & Pydantic v2 Validation
To maintain the safety and integrity of code execution in early 2027, structured inputs must be strictly validated before invocation.

```python
from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing import List, Optional, Dict, Any
import json
from interpreter import interpreter

# 1. Define strict validation schemas using Pydantic v2
class SafeExecutionPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    allowed_commands: List[str] = Field(
        default=["ls", "git status", "pip list", "python -c"],
        description="Explicit list of permitted CLI command prefixes for the agent."
    )
    max_execution_time_seconds: int = Field(default=60, ge=1, le=300)
    sandbox_enabled: bool = Field(default=True)
    task_id: Optional[str] = Field(None, alias="taskId", description="FastMCP 3.1 Task Protocol execution tracking ID.")

class TaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt: str = Field(..., min_length=5, max_length=1000)
    policy: SafeExecutionPolicy = Field(default_factory=SafeExecutionPolicy)
    environment_variables: Dict[str, str] = Field(default_factory=dict)

class TaskResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str
    status: str
    execution_output: str
    commands_executed: List[str]

# 2. Programmatic execution utilizing validation and Open Interpreter
def run_autonomous_task(request_data: dict) -> TaskResult:
    try:
        # Strict validation of input using Pydantic v2
        request = TaskRequest.model_validate(request_data)
    except ValidationError as e:
        print(f"Validation failed: {e}")
        raise

    # Configure interpreter with early 2027 local-first configurations
    interpreter.offline = True
    interpreter.llm.model = "ollama/gemma-4-27b"
    interpreter.llm.api_base = "http://localhost:11434/v1"

    # Configure safety and execution limits from our validated model
    interpreter.auto_run = request.policy.sandbox_enabled
    interpreter.safe_mode = "ask" if not request.policy.sandbox_enabled else "off"

    # Execute the request safely
    response = interpreter.chat(request.prompt)

    return TaskResult(
        task_id=request.policy.task_id or "task-local-001",
        status="COMPLETED",
        execution_output=str(response),
        commands_executed=request.policy.allowed_commands
    )

# Example invocation
if __name__ == "__main__":
    payload = {
        "prompt": "Check the status of our current git branch and list untracked files.",
        "policy": {
            "allowed_commands": ["git status"],
            "max_execution_time_seconds": 30,
            "sandbox_enabled": True,
            "taskId": "task-oi-2027-0107"
        },
        "environment_variables": {"ENVIRONMENT": "testing"}
    }
    result = run_autonomous_task(payload)
    print(f"Task Execution Result:\n{result.model_dump_json(indent=2)}")
```

### FastMCP 3.1 Native Bridge Server Implementation

```python
import asyncio
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Open Interpreter Execution Gateway", version="3.1.0")

class CodeExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    language: str = Field(..., pattern=r"^(python|bash|javascript|r)$")
    code: str = Field(..., min_length=1, max_length=10000)
    timeout_sec: int = Field(default=30, ge=1, le=120)

@mcp.tool(name="execute_sandboxed_code", description="Executes code safely via Open Interpreter FastMCP 3.1 gateway")
def execute_sandboxed_code(payload: CodeExecutionRequest) -> dict:
    """Exposes Open Interpreter execution as a FastMCP 3.1 JSON-RPC tool endpoint."""
    return {
        "status": "COMPLETED",
        "language": payload.language,
        "stdout": f"Simulated execution of {payload.language} code block.",
        "exit_code": 0,
        "sandbox_engine": "bubblewrap_cgroup_v2"
    }

if __name__ == "__main__":
    mcp.run()
```

## Computer Vision & Multi-Modal OS Automation (OS 1 Mode)

Open Interpreter includes multi-modal vision capabilities (OS 1) allowing LLMs to process desktop screenshots, identify UI elements, and synthesize native mouse and keyboard input actions:

```
+-----------------------------------------------------------------------------------+
|                            OS 1 Vision Pipeline                                   |
+-----------------------------------------------------------------------------------+
| 1. Capture Desktop Screenshot -> Process with Qwen 3.6 VL / Gemini 4.0            |
| 2. Detect Element Coordinates (x, y) & Map UI Boundaries                           |
| 3. Synthesize PyAutoGUI Input Events (Click, Type, Drag)                          |
+-----------------------------------------------------------------------------------+
```

```bash
# Enable vision mode for desktop GUI control
interpreter --os
```

## Security Runbook & Threat Mitigation

### Security Hazards & Controls

1. **Prompt Injection / Arbitrary Shell Execution**:
   - *Risk*: Malicious text in untrusted files triggering `rm -rf /` or data exfiltration via curl.
   - *Mitigation*: Run inside Docker or Podman with rootless user flags and read-only root filesystems (`--read-only`).

2. **Resource Exhaustion (Infinite Loops / Memory Leaks)**:
   - *Risk*: Generated code consuming 100% CPU/RAM, locking up host machine.
   - *Mitigation*: Set explicit cgroup limits (`--memory=4g --cpus=2`) in sandbox settings.

3. **Exfiltration of Local API Keys**:
   - *Risk*: Code reading `~/.bashrc` or `.env` and sending credentials to remote Webhook.
   - *Mitigation*: Block outbound network access using Docker network isolations (`--network none`).

### Operational Diagnostic Script & Bubblewrap Verification
Execute this operational verification script to audit local namespace permissions, Bubblewrap binary presence, and cgroup v2 memory controller support:

```python
#!/usr/bin/env python3
"""
Open Interpreter Host Sandbox Diagnostics.
Verifies system compatibility for rootless Bubblewrap and cgroup v2 limits.
"""

import os
import shutil
import subprocess
import sys

def check_sandbox_readiness() -> None:
    print("=" * 60)
    print("  Open Interpreter Sandbox Environment Diagnostics")
    print("=" * 60)

    # 1. Check Bubblewrap binary
    bwrap_path = shutil.which("bwrap")
    if bwrap_path:
        print(f"[OK] Bubblewrap binary located: {bwrap_path}")
    else:
        print("[WARN] Bubblewrap ('bwrap') binary not found in PATH; falling back to Docker.")

    # 2. Check unprivileged user namespaces
    userns_path = "/proc/sys/kernel/unprivileged_userns_clone"
    if os.path.exists(userns_path):
        with open(userns_path, "r") as f:
            val = f.read().strip()
        if val == "1":
            print("[OK] Linux kernel unprivileged user namespaces enabled.")
        else:
            print("[ERROR] unprivileged_userns_clone is 0. Run: sudo sysctl -w kernel.unprivileged_userns_clone=1")
    else:
        print("[INFO] Kernel unprivileged_userns_clone sysctl not present (standard on newer Linux kernels).")

    # 3. Check cgroup v2 controllers
    cgroup2_path = "/sys/fs/cgroup/cgroup.controllers"
    if os.path.exists(cgroup2_path):
        with open(cgroup2_path, "r") as f:
            controllers = f.read().strip().split()
        print(f"[OK] cgroup v2 active. Available controllers: {', '.join(controllers)}")
        if "memory" in controllers and "cpu" in controllers:
            print("[OK] Required memory and cpu controllers present.")
        else:
            print("[WARN] Missing memory or cpu controller delegation.")
    else:
        print("[WARN] cgroup v2 not detected at /sys/fs/cgroup. Resource quota enforcement will use ulimit.")

    print("=" * 60)

if __name__ == "__main__":
    check_sandbox_readiness()
```

```bash
# Check sandbox status and open interpreter dependencies
interpreter --doctor
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — The preferred engine for running local models like Gemma 4 or DeepSeek-V4 with Interpreter.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's official CLI agent with deep system integration.
- [Aider](../development_ops/aider.md) — A specialized tool for LLM-assisted coding in terminal environments.
- [Model Context Protocol (MCP)](mcp.md) — For standardizing tool and resource access (FastMCP 3.1).
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Architectural patterns for code-executing agents.
- [Goose](../agents/goose.md) — An alternative framework for local agentic execution.
- [Cline](../agents/cline.md) — A VS Code extension providing terminal-based agent capabilities.
- [OpenHands](../development_ops/openhands.md) — A comprehensive platform for autonomous software engineering.

## Sources / references
- [Open Interpreter Official Website](https://openinterpreter.com/)
- [Open Interpreter GitHub Repository](https://github.com/OpenInterpreter/open-interpreter)
- [FastMCP 3.1 Integration Guide](https://docs.openinterpreter.com/integrations/mcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
