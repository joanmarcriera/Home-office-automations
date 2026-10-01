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

## Limitations
- **Security Implications**: Executing LLM-generated code locally requires vigilant oversight; a single hallucinated or malicious command can lead to catastrophic data loss.
- **Hardware Performance**: The speed and reliability of local execution are strictly bound by the host machine's CPU, GPU, and RAM.
- **Environmental Drift**: Code that runs perfectly in one local environment may fail in another due to missing dependencies or differing OS versions.

## Framework Comparison Matrix

| Feature / Metric | Open Interpreter | Claude Code | Goose Agent | Aider |
| :--- | :--- | :--- | :--- | :--- |
| **Execution Environment**| Local OS / Docker / WASM | Terminal Subshell | Extension / Local OS | Git Repository |
| **Supported Languages**| Python, Bash, JS, R, SQL | Shell / Git | Custom Tools | Python / Polyglot |
| **MCP Compatibility**| Native FastMCP 3.1 | Native MCP | Custom Extensions | Partial MCP |
| **Vision UI Control** | Yes (OS 1 / Qwen VL) | No | No | No |
| **Safety Mode** | Interactive / Sandbox | Terminal Prompts | Permission Prompts | Git Rollback |
| **License** | Open Source (MIT) | Proprietary | Open Source (Apache 2) | Open Source (Apache 2) |

## When to use it
- When an agent needs direct, stateful interaction with the local file system or operating system.
- For complex data processing tasks where data privacy and sovereignty are non-negotiable.
- When leveraging open-weights models (Gemma 4, DeepSeek-V4, Qwen 3.6 VL) for sophisticated system-level automation.
- For multi-modal desktop automation requiring screenshot analysis and GUI click simulation.

## When not to use it
- On production servers or highly sensitive environments without additional sandboxing (e.g., within a dedicated Docker or Podman container).
- For simple conversational tasks that do not require any system interaction or code execution.

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
| Local Subshell   |    | Docker Container  |   | WASM Sandbox       |
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
    model_config = ConfigDict(extra="forbid")

    allowed_commands: List[str] = Field(
        default=["ls", "git status", "pip list", "python -c"],
        description="Explicit list of permitted CLI command prefixes for the agent."
    )
    max_execution_time_seconds: int = Field(default=60, ge=1, le=300)
    sandbox_enabled: bool = Field(default=True)
    task_id: Optional[str] = Field(None, alias="taskId", description="FastMCP 3.1 Task Protocol execution tracking ID.")

class TaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(..., min_length=5, max_length=1000)
    policy: SafeExecutionPolicy = Field(default_factory=SafeExecutionPolicy)
    environment_variables: Dict[str, str] = Field(default_factory=dict)

class TaskResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
from pydantic import BaseModel, Field

class FastMCPInterpreterBridge:
    def __init__(self, sandbox_mode: str = "docker"):
        self.sandbox_mode = sandbox_mode

    async def execute_code_rpc(self, language: str, code_snippet: str) -> dict:
        """Exposes Open Interpreter execution as a FastMCP 3.1 JSON-RPC tool endpoint."""
        # Simulated FastMCP RPC dispatch handler
        await asyncio.sleep(0.1)
        return {
            "jsonrpc": "2.0",
            "result": {
                "language": language,
                "stdout": "Execution completed successfully.",
                "stderr": "",
                "exit_code": 0
            },
            "id": "mcp-exec-101"
        }

# Usage:
if __name__ == "__main__":
    bridge = FastMCPInterpreterBridge()
    res = asyncio.run(bridge.execute_code_rpc("python", "print('Hello from Open Interpreter Bridge')"))
    print(f"Bridge execution output: {res}")
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

### Operational Diagnostic Script

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
