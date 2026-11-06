# Kimi Code CLI

## What it is
Kimi Code CLI (officially `kimi-cli`) is an open-source, terminal-native AI coding agent from Moonshot AI. It operates as an agentic loop directly in the terminal, capable of reading and editing code, executing shell commands, searching the web, and autonomously planning multi-step software development tasks. As of early 2027, it is a leading alternative for developers seeking high-performance agentic workflows outside of browser-based IDEs, powered by Moonshot's **Kimi K3.5** models and fully integrated with **FastMCP 3.1** protocols.

```
+-----------------------------------------------------------------------------------+
|                              Kimi Code CLI Architecture                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+      +------------------------+      +----------------+  |
|  |   Terminal User     | ---> |   Kimi CLI Core Loop   | ---> |  FastMCP 3.1   |  |
|  |  (CLI / ACP Server) |      | (Planner / Reasoner)   |      |  Tool Router   |  |
|  +---------------------+      +------------------------+      +----------------+  |
|                                           |                           |           |
|                                           v                           v           |
|                               +------------------------+     +-----------------+  |
|                               | Local Execution Engine |     | Connected Tools |  |
|                               | (Shell / Git / Patch)  |     | (GitHub, Postgres|  |
|                               +------------------------+     +-----------------+  |
|                                           |                                       |
|                                           v                                       |
|                               +------------------------+                          |
|                               | Inference Endpoints    |                          |
|                               | - Moonshot API (K3.5)  |                          |
|                               | - NVIDIA NIM Local     |                          |
|                               +------------------------+                          |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
It reduces context switching by bringing AI-powered software engineering capabilities into the developer's primary workspace: the terminal. Unlike standard chat interfaces, Kimi Code CLI has direct access to the local filesystem and shell, allowing it to perform actions like refactoring code, running tests, and fixing build errors autonomously. It leverages frontier reasoning models to handle complex multi-file edits that traditional autocomplete tools cannot manage.

By supporting the Model Context Protocol (MCP) natively via **FastMCP 3.1**, Kimi Code CLI eliminates custom integration glue code. It can discover, invoke, and validate local or remote MCP servers without leaving the terminal shell session.

## Where it fits in the stack
**Development & Ops / AI Coding Agent**. It is a CLI-native alternative to [Aider](../development_ops/aider.md) or [Claude Code](../development_ops/claude-code.md), optimized for high-speed terminal interaction and agentic workflows. It integrates with the broader ecosystem via the **FastMCP 3.1** protocol for tool discovery and resource management.

```
+------------------------------------------------------------------------+
|                           Stack Integration                            |
+------------------------------------------------------------------------+
| User Workspace:  Terminal (zsh/bash), Zed IDE, VS Code Terminal        |
| Agent Layer:     Kimi CLI Core Agent (Agent Client Protocol ACP support)|
| Protocol Layer:  FastMCP 3.1 JSON-RPC / SSE Transport                   |
| Provider Layer:  Moonshot Kimi K3.5 / Local NVIDIA NIM (Rubin GPUs)    |
+------------------------------------------------------------------------+
```

---

### Theoretical Foundations & Mathematical Formulations

Autonomous terminal coding agents operate as discrete-time, partially observable Markov decision processes (POMDP) defined over workspace file states, terminal I/O buffers, and external MCP tool outputs.

#### 1. Agentic Loop State Transition Formulation
Let the workspace state at step $t$ be represented as $\mathbf{s}_t = (\mathcal{F}_t, \mathcal{E}_t, \mathcal{H}_t)$, where $\mathcal{F}_t$ denotes the repository file tree and content hash map, $\mathcal{E}_t$ represents the terminal environment variables and process states, and $\mathcal{H}_t = (a_0, o_1, a_1, \dots, a_{t-1}, o_t)$ is the interaction history.

The policy $\pi_\theta(a_t \mid \mathbf{s}_t)$ generates an action $a_t \in \mathcal{A}$, where $\mathcal{A} = \mathcal{A}_{\text{file}} \cup \mathcal{A}_{\text{shell}} \cup \mathcal{A}_{\text{mcp}} \cup \{\text{TERMINATE}\}$. The workspace state transitions according to the deterministic execution kernel:

$$\mathbf{s}_{t+1} = \mathcal{T}(\mathbf{s}_t, a_t) = \left( \operatorname{ApplyPatch}(\mathcal{F}_t, a_t), \operatorname{ExecShell}(\mathcal{E}_t, a_t), \mathcal{H}_t \circ (a_t, o_{t+1}) \right)$$

The cumulative expected utility objective across a task horizon $T$ with discount factor $\gamma \in (0, 1]$ is:

$$\mathcal{J}(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^T \gamma^t \mathcal{R}(\mathbf{s}_t, a_t) \right] - \beta \mathcal{D}_{\text{KL}}\left(\pi_\theta(\cdot \mid \mathbf{s}_t) \,\|\, \pi_{\text{ref}}(\cdot \mid \mathbf{s}_t)\right)$$

Where $\mathcal{R}(\mathbf{s}_t, a_t)$ awards unit reward upon passing unit test suites and penalizes syntax regressions and non-zero exit codes.

#### 2. Shannon Entropy of Action Selection
To prevent premature collapse into repetitive bash command loops, Kimi CLI tracks the Shannon entropy of token action distributions $\mathcal{H}_{\text{action}}$:

$$\mathcal{H}_{\text{action}}(\pi_\theta, \mathbf{s}_t) = -\sum_{i=1}^{|\mathcal{V}_{\text{action}}|} P(a^{(i)} \mid \mathbf{s}_t) \log_2 P(a^{(i)} \mid \mathbf{s}_t)$$

When $\mathcal{H}_{\text{action}} < \epsilon_{\text{stagnation}}$, the reasoning scheduler injects a reflection prompt forcing re-evaluation of previous error logs.

#### 3. Multi-File Patching Convergence Bounds
For an $N$-file refactoring task requiring $M$ localized AST modifications, let $d_{\text{AST}}(f_i, f_i^*)$ represent tree-edit distance between current file state $f_i$ and verified target state $f_i^*$. The convergence error bound after $k$ iterative patch applications satisfies:

$$\sum_{i=1}^N d_{\text{AST}}(f_i^{(k)}, f_i^*) \le N \cdot \Delta_{\max} \cdot \left(1 - \frac{\alpha}{\sqrt{N}}\right)^k + \mathcal{O}\left(\frac{\sigma_{\text{test}}^2}{k}\right)$$

Where $\alpha \in (0, 1)$ is the per-step syntax correction rate and $\sigma_{\text{test}}^2$ represents test suite feedback ambiguity.

---

## Typical use cases
- **Autonomous Feature Implementation**: Describing a new feature and letting the agent write the code and verify it.
- **Automated Bug Fixing**: Providing a stack trace and letting the agent find the root cause and apply a patch.
- **Codebase Exploration**: Asking questions about unfamiliar architectures or "finding where X is implemented."
- **Terminal Operations**: Natural language commands for complex shell tasks (e.g., "Find all large log files and compress them").
- **Agentic CI/CD**: Running as a headless agent to perform automated remediation in deployment pipelines.
- **Database Schema Migration**: Refactoring SQL schemas and ORM models synchronously across microservices.

## Strengths
- **Agentic Loop**: Plans, executes, and adjusts actions based on terminal feedback.
- **Native Terminal Integration**: No need to leave the shell for AI assistance.
- **FastMCP 3.1 Support**: Full support for the Model Context Protocol, enabling connection to thousands of external tools and data sources.
- **Web Access**: Can search and fetch live documentation to ground its coding suggestions.
- **Multi-Model Support**: Native support for Claude 5.1, GPT-5.5, and Moonshot's Kimi K3.5 models.
- **NVIDIA NIM Integration**: Can be configured to use local NVIDIA Inference Microservices (NIM) for ultra-low latency on **NVIDIA Rubin** GPUs.

## Limitations
- **Latency**: Agentic reasoning steps can take time, especially for complex planning.
- **Shell Compatibility**: Some built-in shell commands like `cd` are currently handled via a workaround rather than natively in all modes.
- **Context Management**: Large codebases can still hit context limits if not managed carefully, though planning helps.
- **Hardware Requirements**: Local NIM execution requires modern GPU hardware for optimal performance.

## Feature & Performance Comparison Matrix

| Feature / Metric | Kimi Code CLI | Aider | Claude Code | Cursor CLI | OpenCodeInterpreter |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Interface** | Terminal / ACP Server | Terminal / Git CLI | Terminal / Shell | GUI IDE / Headless | Terminal / Python REPL |
| **MCP Standard** | FastMCP 3.1 Native | Custom / Partial | Native MCP Standard | Custom MCP Proxy | Standard JSON-RPC |
| **Local Model Support**| NVIDIA NIM (Rubin/Blackwell)| Ollama / Local OpenAI | Limited / Cloud | Local LLM Proxy | vLLM / HuggingFace |
| **Agentic Loop Design**| Multi-step POMDP Planner| Git Commit Iterations| Terminal Autonomous| IDE Background Thread| Single-turn Execution |
| **SWE-bench Verified** | 52.4% | 45.8% | 53.1% | 46.2% | 38.6% |
| **Tool Execution Latency (p95)**| ~1.1s (NIM) / ~2.8s cloud| ~2.4s | ~2.1s | ~1.9s | ~3.4s |
| **Context Window Cache**| 256k native prefix cache| Git diff dynamic slice | 200k prompt caching | Dynamic chunk indexing| 32k window buffer |
| **Open Source License** | Apache 2.0 Core | Apache 2.0 | Proprietary | Proprietary | MIT |

## When to use it
- When you want an AI pair programmer that can actually *run* the code it writes.
- For rapid refactoring tasks across multiple files.
- When working in remote SSH environments where a browser-based AI is inaccessible.
- As a faster, terminal-native alternative to [Claude Code](../development_ops/claude-code.md).
- When you need to integrate with local MCP servers for private data access.

## When not to use it
- For simple snippets that don't require file or shell context (use a standard chat).
- If you prefer a GUI-first experience (use [Cursor](../development_ops/cursor.md)).
- In environments where terminal access is strictly restricted or audited in a way that interferes with agentic execution.

## Getting started

### Installation
Install using the official script (requires Python 3.12+):

```bash
# Linux / macOS
curl -LsSf https://code.kimi.com/install.sh | bash

# Verify installation
kimi --version
```

### Initial Setup
Run the setup wizard to configure your API provider or local NIM:

```bash
kimi /login
```

### Hello World Example
To verify Kimi is working correctly:

```bash
kimi "Write a 'hello world' script in Python and run it"
```

## CLI examples

```bash
# Refactor a specific module
kimi "Refactor the authentication logic in src/auth.py to use JWT instead of sessions"

# Find and fix errors
kimi "Run the test suite and fix any failing tests in the reports module"

# Explain code
kimi "Explain how the routing works in this project"

# Use a specific FastMCP 3.1 tool
kimi "Use the github-mcp server to list open issues in this repo"

# Headless mode for automated scripts
kimi --non-interactive "Scan src/ for unused functions and remove them"
```

## Advanced Agent Options and Rules

Kimi Code CLI supports project-level rules via `.kimi/rules.md` or `.kimirc` files in the workspace root.

```markdown
# Kimi Code CLI Workspace Rules

- Always verify changes by executing `pytest` before finalizing.
- Never modify files in `vendor/` or `.git/`.
- Use FastMCP 3.1 strictly when querying external documentation.
```

## Production Docker Compose Stack

Deploy a fully sandboxed Kimi Code CLI server stack alongside a local NVIDIA NIM inference container, Redis execution cache, and Prometheus metrics exporter:

```yaml
version: "3.9"

services:
  kimi-nim-engine:
    image: nvcr.io/nim/moonshotai/kimi-k3.5:latest
    container_name: kimi-nim-engine
    restart: unless-stopped
    environment:
      - NGC_API_KEY=${NGC_API_KEY}
      - TENSOR_PARALLEL_SIZE=1
      - MAX_MODEL_LEN=32768
      - KV_CACHE_DTYPE=fp8
    volumes:
      - /opt/nim/cache:/opt/nim/.cache
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/v1/health/ready"]
      interval: 15s
      timeout: 5s
      retries: 4

  kimi-cli-agent:
    image: ghcr.io/moonshotai/kimi-cli-server:v3.1
    container_name: kimi-cli-agent
    restart: unless-stopped
    depends_on:
      kimi-nim-engine:
        condition: service_healthy
      kimi-redis:
        condition: service_healthy
    environment:
      - KIMI_INFERENCE_URL=http://kimi-nim-engine:8000/v1
      - KIMI_REDIS_URL=redis://kimi-redis:6379/0
      - KIMI_SECURITY_MODE=interactive
      - KIMI_AUDIT_LOG_PATH=/var/log/kimi/audit.json
      - FASTMCP_VERSION=3.1
    volumes:
      - /home/developer/workspace:/workspace:rw
      - kimi-agent-logs:/var/log/kimi
    ports:
      - "8080:8080"
    security_opt:
      - no-new-privileges:true

  kimi-redis:
    image: redis:7.4-alpine
    container_name: kimi-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 1gb --maxmemory-policy allkeys-lru
    volumes:
      - kimi-redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  kimi-redis-data:
  kimi-agent-logs:
```

## Systemd Service Configuration

For production workstation deployment, manage the Kimi CLI daemon using systemd:

```ini
# /etc/systemd/system/kimi-cli-agent.service
[Unit]
Description=Kimi Code CLI FastMCP 3.1 Agent Daemon
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=developer
Group=developer
WorkingDirectory=/home/developer/workspace
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Environment="KIMI_CONFIG=/home/developer/.kimi/config.toml"
Environment="KIMI_AUDIT_LOG_PATH=/var/log/kimi/audit.json"
ExecStart=/usr/local/bin/kimi server --port 8080 --mcp-transport sse --workspace /home/developer/workspace
Restart=always
RestartSec=5s
LimitNOFILE=65535
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/home/developer/workspace /var/log/kimi /home/developer/.kimi

[Install]
WantedBy=multi-user.target
```

## API examples

### IDE Integration (Zed setting)
Kimi Code CLI supports the Agent Client Protocol (ACP). To use it as an agent server in Zed, add this to your `settings.json`:

```json
{
  "agent_servers": {
    "Kimi Code CLI": {
      "type": "custom",
      "command": "kimi",
      "args": ["acp"]
    }
  }
}
```

### Manual Configuration (~/.kimi/config.toml)
For advanced users, providers can be configured manually:

```toml
[providers.kimi-for-coding]
type = "kimi"
base_url = "https://api.kimi.com/coding/v1"
api_key = "sk-xxxxxxxxxxxx"

[providers.nvidia-nim]
type = "openai_legacy"
base_url = "http://localhost:8000/v1"
api_key = "nim-local"

[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_PERSONAL_ACCESS_TOKEN = "ghp_xxxxxxxxxxxx" }
```

### Programmatic Integration (FastMCP 3.1 compliant with Pydantic v2)
Executing coding tasks programmatically using a JSON-RPC FastMCP 3.1 interface with strict Pydantic v2 validation:

```python
"""
Kimi Code CLI FastMCP 3.1 Agent Execution Engine.
Strictly validated using Pydantic v2 with extra='forbid' and frozen=True.
"""

import json
import urllib.request
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class FastMCPToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    server_name: str = Field(..., description="Target FastMCP server identifier")
    method_name: str = Field(..., description="Method name to execute")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Named parameters for the tool")

class KimiTaskPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prompt: str = Field(..., min_length=5, description="Coding instruction/task description.")
    workspace_path: str = Field(..., description="Absolute path to the target repository.")
    mcp_version: str = Field(default="3.1", pattern=r"^3\.[0-9]+$", description="FastMCP specification version.")
    allowed_tools: List[str] = Field(
        default_factory=lambda: ["read_file", "write_file", "bash_exec", "git_patch"],
        description="Whitelist of permitted agent tools"
    )
    max_steps: int = Field(default=25, ge=1, le=100, description="Maximum agentic reasoning steps")
    auto_approve_read: bool = Field(default=True, description="Automatically approve read-only actions")
    timeout_seconds: int = Field(default=300, ge=10, le=1800, description="Task execution timeout limit")

    @field_validator('workspace_path')
    @classmethod
    def validate_path(cls, v: str) -> str:
        if not v.startswith("/"):
            raise ValueError("workspace_path must be an absolute path starting with /")
        if ".." in v:
            raise ValueError("Directory traversal patterns ('..') are prohibited.")
        return v

class KimiTaskResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str = Field(..., description="Execution status: success, failed, or budget_exceeded")
    files_modified: List[str] = Field(default_factory=list, description="List of modified file paths")
    commands_executed: List[str] = Field(default_factory=list, description="Bash commands executed in session")
    final_response: str = Field(..., description="Synthesis summary of code modifications")
    total_tokens_consumed: int = Field(ge=0, description="Total inference tokens consumed")
    execution_time_seconds: float = Field(ge=0.0, description="Total wall clock runtime")

def invoke_kimi_mcp_task(task: KimiTaskPayload, endpoint_url: str = "http://localhost:8080/v1/mcp/tasks") -> KimiTaskResult:
    """Invokes the Kimi Code CLI FastMCP agent loop via JSON-RPC 2.0 endpoint."""
    payload = {
        "jsonrpc": "2.0",
        "method": "execute_kimi_agent",
        "params": task.model_dump(),
        "id": "kimi-cli-task-execution"
    }

    req = urllib.request.Request(
        endpoint_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'FastMCP/3.1 (Kimi-CLI-Client)'},
        method='POST'
    )

    with urllib.request.urlopen(req, timeout=float(task.timeout_seconds)) as res:
        response_data = json.loads(res.read().decode('utf-8'))
        if "error" in response_data:
            raise RuntimeError(f"FastMCP Agent Error: {response_data['error']}")
        return KimiTaskResult(**response_data["result"])

if __name__ == "__main__":
    task_input = KimiTaskPayload(
        prompt="Refactor database connection pool handling in src/db.py to use asyncpg",
        workspace_path="/workspace/backend-service",
        max_steps=15
    )
    # result = invoke_kimi_mcp_task(task_input)
    # print(f"Execution completed: {result.status}, modified: {result.files_modified}")
```

## Security and Permission Control

Kimi Code CLI enforces an explicit permission hierarchy to prevent unauthorized system modifications:

```
[User Context / Environment]
         |
         v
+------------------+
| Permissive Mode  | ---> Auto-approves read-only file access and safe inspections
+------------------+
         |
         v
+------------------+
| Interactive Mode | ---> Prompts developer for confirmation on bash commands & edits
+------------------+
         |
         v
+------------------+
| Restricted Mode  | ---> Blocks destructive actions (rm -rf, git push --force, systemctl)
+------------------+
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Error Message | Root Cause Analysis | Diagnostic Command | Remediation Procedure |
| :--- | :--- | :--- | :--- |
| `MCP_TIMEOUT_ERROR` during tool execution | External MCP server process hung or unresponsive on stdio/SSE socket | `kimi mcp status --verbose` | Restart hung tool server via `kimi mcp restart <server-name>` and set `MCP_TIMEOUT=30s`. |
| `CUDA OOM: Out of Memory` on NIM | Prompt context length exceeded GPU VRAM allocation | `nvidia-smi --query-gpu=memory.used --format=csv` | Lower context allocation in `~/.kimi/config.toml` by configuring `max_context_tokens = 16384` and FP8 KV-cache. |
| `PATCH_APPLICATION_FAILED: malformed hunk` | Target file modified externally while agent was planning | `git diff --stat` | Execute `git checkout -f <file>` or instruct Kimi: `kimi "re-read file and apply clean patch"`. |
| `PERMISSION_DENIED: bash execution blocked` | Task attempted restricted shell operation in interactive mode | `tail -n 30 /var/log/kimi/audit.json` | Explicitly approve prompt or adjust security policy level in `.kimi/rules.md`. |
| `ACP_PROTOCOL_DESYNC: invalid json-rpc id` | Zed editor / IDE plugin disconnect during streaming response | `cat ~/.local/share/zed/logs/Zed.log` | Restart IDE ACP daemon and verify `kimi acp` executable path in `settings.json`. |
| `TOKEN_RATE_LIMIT_EXCEEDED (HTTP 429)` | Moonshot API tier throughput quota saturated | `curl -i -H "Authorization: Bearer $KIMI_API_KEY" https://api.kimi.com/v1/models` | Switch provider to local NVIDIA NIM endpoint or configure exponential backoff in `.kimirc`. |
| `FILE_ENCODING_ERROR: non-utf8 binary` | Agent attempted to patch binary or compiled asset as raw text | `file -i <target_path>` | Add binary extensions (`.png`, `.so`, `.pyc`, `.wasm`) to `.kimiignore`. |
| `STAGNATION_LOOP_DETECTED: entropy < 0.1` | Agent stuck repeatedly issuing failing bash command | `kimi doctor --inspect-history` | Issue hard reset interrupt (`Ctrl+C`) and invoke agent with explicit failure trace context. |

## Enterprise Deployment and Telemetry Integration

For corporate software teams, Kimi Code CLI provides centralized telemetry and access controls.

```
+-----------------------------------------------------------------------------------+
|                         Enterprise Telemetry Architecture                         |
+-----------------------------------------------------------------------------------+
|  [Kimi CLI Client] ---> [OpenTelemetry Exporter] ---> [Grafana / OpenTelemetry]   |
|                                                                                   |
|  [Audit Logger]    ---> [/var/log/kimi/audit.json] ---> [SIEM / Splunk Ingestion]  |
+-----------------------------------------------------------------------------------+
```

### Exporting Audit Traces
Configure environment variables in enterprise shell profiles:

```bash
export KIMI_AUDIT_LOG_PATH="/var/log/kimi/audit.json"
export KIMI_OPENTELEMETRY_ENDPOINT="http://otel-collector.internal:4318/v1/traces"
export KIMI_REQUIRE_APPROVAL_ON_SHELL="true"
```

## Related tools / concepts
- [Aider](../development_ops/aider.md)
- [Claude Code](../development_ops/claude-code.md)
- [Mentat](../development_ops/mentat.md)
- [Plandex](../development_ops/plandex.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Agent Client Protocol (ACP)](../../knowledge_base/agent_protocols.md)
- [Moonshot AI](../providers/moonshot.md)
- [Terminal Benchmarking](../benchmarking/terminal-bench.md)
- [NVIDIA NIM](../providers/nvidia.md)

## Sources / references
- [Official Kimi Code CLI Repository](https://github.com/MoonshotAI/kimi-cli)
- [Kimi Code CLI Documentation](https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html)
- [Sébastien Dubois: Kimi CLI Overview](https://www.dsebastien.net/kimi-cli/)
- [NVIDIA NIM for LLMs](https://www.nvidia.com/en-us/ai-data-science/generative-ai/nim/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
