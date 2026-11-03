# Junie CLI

## What it is
Junie CLI is an AI-driven, high-speed, terminal-native codebase navigation engine, semantic search indexer, and autonomous software engineering assistant developed under the JetBrains AI Lab initiative. In early 2027, the stable **v2.5+** release operates as a lightweight enterprise background daemon and CLI companion. Built with native support for the **FastMCP 3.1 Task Protocol**, Junie CLI combines JetBrains AST-based code analysis models with frontier reasoning engines (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL) to deliver sub-second repository search, tmux-native test orchestration, and automated git patch generation.

```
+-----------------------------------------------------------------------------------+
|                           Junie CLI Daemon Architecture                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------+                    +--------------------------------+  |
|  | Developer Terminal    |                    | Junie CLI Core Daemon          |  |
|  | - Neovim / Helix / Zsh| -- FastMCP 3.1 --> |  - Rust AST Code Indexer       |  |
|  | - Tmux Split Panes    |    (STDIO/IPC)     |  - Semantic Vector Cache       |  |
|  +-----------------------+                    |  - FastMCP 3.1 Task Manager    |  |
|                                               +---------------+----------------+  |
|                                                               |                   |
|                                                               v                   |
|                                               +--------------------------------+  |
|                                               | Tmux-Bridge Execution Loop     |  |
|                                               |  - Background Test Monitoring  |  |
|                                               |  - Buffer Capture & Parse      |  |
|                                               +---------------+----------------+  |
|                                                               |                   |
|                                                               v                   |
|                                               +--------------------------------+  |
|                                               | JetBrains AST & Model Gateway  |  |
|                                               |  - Local Codebase Graph DB     |  |
|                                               |  - Claude 5.6 / GPT-5.6 APIs   |  |
|                                               +--------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Developing software in complex, million-line repositories over remote SSH connections or inside multi-pane terminal multiplexers (`tmux`) often suffers from high context switching overhead and resource degradation caused by heavy graphical IDEs.

Junie CLI eliminates these friction points by:
1. **Sub-Second Codebase Navigation**: Combining high-performance Rust AST indexing with local vector embeddings to return instant semantic lookups without relying on GUI file trees.
2. **Tmux-Bridge Autonomous Refactoring**: Spawning isolated background tmux panes to execute test suites, capture stdout/stderr build failures, and apply self-correcting code diffs autonomously.
3. **AST-Guided Patch Accuracy**: Utilizing JetBrains code analysis trees to ensure patches strictly adhere to language grammar and type definitions before modifying files.
4. **FastMCP 3.1 Sub-Agent Interoperability**: Exposing local repository inspection and refactoring capabilities as standardized FastMCP tools for external AI agent swarms.

## Where it fits in the stack
**Development & Ops Layer**. Junie CLI acts as an **AI-Native Shell Companion and Code Orchestrator**. It sits directly inside the developer's terminal environment, interacting with local shells (zsh/bash), Neovim/Helix text editors, Git version control, and FastMCP model servers.

## Comparative Analysis: Terminal AI Coding Companions

| Feature / Dimension | Junie CLI (v2.5+) | Claude Code | Aider | OpenHands | Mentat |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Architecture** | Background Daemon + Rust AST | Standalone Terminal CLI | Interactive Git-Bound CLI | Containerized Web/CLI Agent | Interactive Context CLI |
| **Multiplexer Bridge** | **Native Tmux-Bridge PTY** | Subshell invocation | Terminal Subprocess | Docker sandbox runtime | Subshell execution |
| **AST Analysis Engine** | **JetBrains PSI / Tree-sitter** | Ripgrep / AST grep | Tree-sitter repository map | Basic regex / parser | Tree-sitter parser |
| **FastMCP 3.1 Support** | **Native Dual Client/Server** | Client-only tool runner | Experimental wrapper | Custom server hooks | None |
| **Memory Footprint** | **<50 MB RSS** | ~180 MB RSS (Node.js) | ~120 MB RSS (Python) | >1.5 GB RSS (Docker) | ~110 MB RSS (Python) |
| **Schema Governance** | **Strict Pydantic v2 Models** | JSON-Schema v7 | Python TypedDict | Pydantic v1/v2 mixed | Python dataclasses |
| **Multi-File Safe Diffs** | **AST-Grammar Gatekeeper** | Model proposed patch | Git unified diff parser | Git patch executor | Custom diff block parser |

## Operational Service Level Agreements (SLAs)

| Operational Tier | Metric / Target | SLA Guarantee | Monitoring Mechanism | Failover / Remediation |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: AST Indexing** | Cold repository initial parse | < 8.0s per 100k LOC | SQLite WAL index telemetry | Fallback to incremental cache |
| **Tier 2: Semantic Lookup** | Symbol & vector search latency | < 350ms (p95) | FastMCP execution timer | Fallback to ripgrep regex scan |
| **Tier 3: Tmux Execution** | Pane lifecycle & buffer capture | < 50ms per poll cycle | Unix domain socket heartbeat | Re-spawn orphaned tmux window |
| **Tier 4: AST Patch Audit** | Syntax check before disk write | < 120ms per diff file | Tree-sitter validation hook | Reject patch; request re-generation |
| **Tier 5: Daemon Availability**| Continuous background uptime | 99.95% availability | Systemd watchdog / Docker health | Auto-restart with state recovery |

## System Architecture & Technical Deep-Dive

```mermaid
graph TD
    DeveloperCLI[Terminal Input / Neovim Keybinding] -->|1. Natural Language Task| JunieDaemon[Junie Daemon Engine]

    JunieDaemon -->|2. AST Code Graph Query| RustIndexer[Rust AST & Vector Indexer]
    RustIndexer -->|3. Relevant Context Snippets| JunieDaemon

    JunieDaemon -->|4. Construct Agentic Task| ModelGateway[Frontier Model Gateway]
    ModelGateway -->|5. Refactoring Plan & Diff| JunieDaemon

    JunieDaemon -->|6. Spawn Background Split| TmuxBridge[Tmux-Bridge Executor]
    TmuxBridge -->|7. Run Tests & Linter| TerminalPane[Isolated Background Tmux Pane]

    TerminalPane -->|8. Terminal Output Buffer| TmuxBridge
    TmuxBridge -->|9. Pass Output / Failures| JunieDaemon

    JunieDaemon -->|10. Self-Correcting Iteration| ModelGateway
    JunieDaemon -->|11. Final Validated Git Patch| DeveloperCLI
```

### 1. High-Performance Rust AST Indexer
Junie CLI embeds a multi-threaded Rust indexing engine that parses source code files into Abstract Syntax Trees (AST) using Tree-sitter. It indexes symbols, function signatures, class inheritance hierarchies, and variable scopes, maintaining a local SQLite database for instant zero-latency queries.

### 2. Tmux-Bridge Orchestrator
To execute multi-step agentic workflows (e.g. "Fix broken unit tests in `src/auth/`"), Junie CLI uses its **Tmux-Bridge** component. It creates dedicated, non-blocking background tmux windows, runs build commands, captures terminal buffer outputs using `tmux capture-pane`, and analyzes stdout/stderr logs in real time.

### 3. AST-Aware Diff Generator & Safety Gate
When applying automated code edits, Junie CLI verifies proposed changes against the language's syntax graph. If a proposed edit introduces syntax errors or breaks imports, Junie CLI rejects the diff locally and prompts the reasoning engine for a corrected patch before altering files on disk.

### 4. FastMCP 3.1 Task Protocol Integration
Junie CLI operates as both an MCP client and an MCP server. It can consume tools from remote MCP servers (e.g. Sentry, GitHub, Jira) and expose its own repository indexing and refactoring tools over standard STDIO or HTTP/SSE transports.

## Typical use cases
- **Remote SSH Workspace Refactoring**: Performing complex codebase refactoring over SSH connections in lightweight terminal environments.
- **Tmux-Native Test-Driven Development (TDD)**: Running autonomous loops that edit code, execute tests in a background tmux pane, read failure stack traces, and re-apply fixes until all tests pass.
- **Sub-Second Code Navigation**: Querying code structure and dependency graphs via natural language (`junie ask "Where are user sessions initialized?"`).
- **Pre-Commit Security & Ruleset Auditing**: Scanning staged git changes against enterprise architecture guidelines before pushing code.

## Strengths
- **Tmux-Native Background Automation**: Non-blocking background task execution with direct terminal buffer inspection.
- **Sub-Second AST Indexing**: Blazing fast codebase indexing with minimal system memory footprint (<50MB RAM).
- **JetBrains AST Code Intelligence**: Leverages deep language grammar parsing for precision code modifications.
- **FastMCP 3.1 Protocol Client/Server**: Native support for modern agent tool schemas and sub-agent task routing.
- **Keyboard-Driven Design**: Integrates directly with Neovim, Helix, Vim, zsh, and tmux.

## Limitations
- **Terminal Only**: Lacks visual drag-and-drop diff view UI; requires terminal-comfortable developers.
- **Tmux Requirement for Background Loops**: Background execution features require `tmux` installed in the shell environment.
- **API Token Dependent**: Autonomous multi-file refactoring runs require access to frontier model API keys (Claude 5.6 or GPT-5.6).

## When to use it
- When working in keyboard-centric terminal environments (Neovim, Helix, tmux) on local or SSH remote development servers.
- When executing complex multi-step refactoring runs that require continuous test verification.
- When querying large million-line codebases with zero-latency semantic lookups.

## When not to use it
- When developer workflows depend entirely on graphical mouse-driven IDEs (e.g. full JetBrains IntelliJ GUI or VS Code GUI).
- In air-gapped environments lacking local LLM setups or external API connectivity.

## Getting started

### Installation
Install Junie CLI v2.5+ via Cargo or global NPM:

```bash
# Global installation via Cargo (recommended)
cargo install junie-cli

# Or install via NPM package manager
npm install -g @jetbrains/junie-cli
```

### Initial Workspace Configuration
Initialize the local AST vector index and configure model credentials:

```bash
# Navigate to project repository root
cd /path/to/project

# Initialize AST indexer and local SQLite cache
junie init

# Configure frontier reasoning model provider
junie config set model claude-5.6
junie config set provider anthropic
```

## CLI examples

### 1. Natural Language Semantic Query
Query repository architecture and dependency relationships instantly:

```bash
junie ask "How are JWT token refresh cycles handled in the FastMCP authentication pipeline?"
```

### 2. Tmux-Native Refactoring Run with Automated Test Verification
Execute an autonomous refactoring loop in a background tmux pane:

```bash
junie run \
  "Refactor all authentication middleware in src/auth/ to pass FastMCP 3.1 headers. Run 'cargo test' and fix any failures." \
  --tmux-bridge \
  --max-iterations 5
```

### 3. Architecture Ruleset Compliance Audit
Scan codebase against enterprise architectural rulesets:

```bash
junie audit \
  --ruleset "./config/fastmcp-3.1-rules.json" \
  --format markdown \
  --output "./reports/codebase-compliance.md"
```

## Production Docker Compose Daemon Stack

For shared remote development nodes or centralized CI runner environments, Junie CLI can be deployed as an autonomous background container alongside an ephemeral Redis event broker:

```yaml
version: "3.8"

services:
  junie-daemon:
    image: jetbrains/junie-cli:2.5.2
    container_name: junie-core-daemon
    restart: unless-stopped
    environment:
      - JUNIE_LOG_LEVEL=info
      - JUNIE_IPC_SOCKET=/var/run/junie/junie.sock
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REDIS_URL=redis://junie-event-broker:6379/0
      - FASTMCP_SERVER_PORT=8089
    volumes:
      - ./workspace:/workspace:rw
      - junie_ipc_data:/var/run/junie:rw
      - junie_ast_cache:/root/.cache/junie:rw
    ports:
      - "127.0.0.1:8089:8089"
    command: ["junie", "daemon", "--listen-ipc", "/var/run/junie/junie.sock", "--mcp-port", "8089"]
    healthcheck:
      test: ["CMD", "junie", "ping", "--socket", "/var/run/junie/junie.sock"]
      interval: 15s
      timeout: 5s
      retries: 3
    depends_on:
      - junie-event-broker

  junie-event-broker:
    image: redis:7.2-alpine
    container_name: junie-event-broker
    restart: unless-stopped
    command: ["redis-server", "--save", "", "--appendonly", "no"]
    volumes:
      - redis_event_data:/data

volumes:
  junie_ipc_data:
  junie_ast_cache:
  redis_event_data:
```

## Production Systemd Daemon Service (`junie-daemon.service`)

Deploy Junie CLI as a managed, self-healing systemd service in multi-developer Linux workstation hosts:

```ini
[Unit]
Description=Junie CLI AST Indexer and FastMCP Daemon
After=network.target tmux.service
Wants=tmux.service

[Service]
Type=simple
User=developer
Group=developer
WorkingDirectory=/home/developer/workspace
EnvironmentFile=/etc/junie/daemon.env
ExecStart=/usr/local/bin/junie daemon --listen-mcp 127.0.0.1:8089 --log-level info
Restart=on-failure
RestartSec=5s
LimitNOFILE=65535
MemoryHigh=2G
MemoryMax=3G
CPUQuota=200%
StandardOutput=journal
StandardError=journal
SyslogIdentifier=junie-daemon

[Install]
WantedBy=multi-user.target
```

## API examples

### FastMCP 3.1 Python Integration Server
The following script exposes Junie CLI workspace refactoring capabilities as an agentic FastMCP tool server with strict Pydantic v2 schemas:

```python
import os
import json
import subprocess
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict

mcp = FastMCP(
    name="Junie Workspace Controller",
    instructions="FastMCP 3.1 interface for executing Junie CLI codebase refactoring and semantic navigation"
)

class JunieRefactorRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_description: str = Field(..., description="High-level description of refactoring task")
    target_directory: str = Field(".", description="Relative directory path to restrict refactoring focus")
    use_tmux_bridge: bool = Field(True, description="Execute test loops in background tmux pane")
    max_iterations: int = Field(5, ge=1, le=10, description="Maximum automated self-correction cycles")
    timeout_seconds: int = Field(300, ge=30, le=900, description="Execution timeout limit")

class JunieRefactorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    success: bool
    applied_patches_count: int
    iterations_used: int
    summary: str
    target_files_modified: List[str] = Field(default_factory=list)

@mcp.tool()
def execute_junie_refactor(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes an autonomous refactoring task using the Junie CLI daemon.
    """
    try:
        req = JunieRefactorRequest.model_validate(request_data)

        cmd = [
            "junie", "run", req.task_description,
            "--path", req.target_directory,
            "--max-iterations", str(req.max_iterations),
            "--format", "json"
        ]

        if req.use_tmux_bridge:
            cmd.append("--tmux-bridge")

        res = subprocess.run(cmd, capture_output=True, text=True, timeout=req.timeout_seconds)

        if res.returncode == 0:
            parsed = json.loads(res.stdout) if res.stdout else {}
            response_obj = JunieRefactorResponse(
                success=parsed.get("success", True),
                applied_patches_count=parsed.get("patches_applied", 1),
                iterations_used=parsed.get("iterations", 1),
                summary=parsed.get("summary", "Refactoring task completed successfully"),
                target_files_modified=parsed.get("files_modified", [])
            )
            return response_obj.model_dump()
        else:
            return {
                "success": False,
                "applied_patches_count": 0,
                "iterations_used": 0,
                "summary": f"Junie CLI returned error code {res.returncode}: {res.stderr}",
                "target_files_modified": []
            }

    except Exception as err:
        return {
            "success": False,
            "applied_patches_count": 0,
            "iterations_used": 0,
            "summary": f"Failed to execute Junie CLI daemon: {str(err)}",
            "target_files_modified": []
        }

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Schema for Junie Diff Verification & Tmux Sessions
This module demonstrates strict **Pydantic v2** validation of Junie CLI session states, semantic search results, and patch diff verification:

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict

class JunieCodeMatch(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    file_path: str = Field(..., description="Relative file path")
    start_line: int = Field(..., ge=1)
    end_line: int = Field(..., ge=1)
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    code_snippet: str

class JunieDiffBlock(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    target_file: str
    added_lines_count: int = Field(..., ge=0)
    deleted_lines_count: int = Field(..., ge=0)
    unified_diff: str

class JunieTmuxSessionReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    session_name: str
    active_pane_id: str
    command_executed: str
    exit_code: int
    stdout_buffer: str
    diffs: List[JunieDiffBlock] = Field(default_factory=list)

def validate_junie_session_output(raw_json: dict) -> Optional[JunieTmuxSessionReport]:
    try:
        report = JunieTmuxSessionReport.model_validate(raw_json)
        print(f"Validated Junie Session '{report.session_name}' successfully.")
        print(f"  Command Exit Code: {report.exit_code}")
        print(f"  Patched Files Count: {len(report.diffs)}")
        return report
    except ValidationError as ve:
        print(f"Pydantic Validation Error for Junie session: {ve}", file=sys.stderr)
        return None

if __name__ == "__main__":
    sample_json = {
        "session_name": "junie-refactor-9912",
        "active_pane_id": "%4",
        "command_executed": "cargo test --package auth",
        "exit_code": 0,
        "stdout_buffer": "running 12 tests... test result: ok. 12 passed; 0 failed",
        "diffs": [
            {
                "target_file": "src/auth/jwt.rs",
                "added_lines_count": 14,
                "deleted_lines_count": 3,
                "unified_diff": "@@ -12,3 +12,14 @@ pub fn validate_token..."
            }
        ]
    }

    validate_junie_session_output(sample_json)
```

## Diagnostic & Troubleshooting Matrix

| Scenario # | Observed Issue / Symptom | Root Cause | Diagnostic Command | Remediation Procedure |
| :---: | :--- | :--- | :--- | :--- |
| **01** | `junie: command not found` | Binary directory not in user `$PATH`. | `which junie || echo $PATH` | Add `export PATH="$HOME/.cargo/bin:$PATH"` to `~/.zshrc` or `~/.bashrc`. |
| **02** | `TmuxBridgeError: no server running on /tmp/tmux-1000` | No active tmux server or socket permissions error. | `tmux ls` | Run `tmux new-session -d -s junie-main` before launching background refactor loops. |
| **03** | AST vector index stale or missing symbols | Repository underwent heavy rebase or branch switch without re-indexing. | `junie index status` | Execute `junie index rebuild --force` to flush and regenerate the SQLite symbol DB. |
| **04** | FastMCP socket connection refused on port 8089 | Port conflict or daemon crashed. | `netstat -tlpn \| grep 8089` | Terminate stale processes (`lsof -ti:8089 \| xargs kill -9`) and restart `junie daemon`. |
| **05** | Tree-sitter parse syntax rejection error | LLM generated code violating language grammar specs. | `junie diff verify --file <path>` | Trigger re-prompting with explicit compiler error messages passed back to the model. |
| **06** | Tmux buffer capture truncation | Target test suite emitted verbose logs exceeding pane scrollback. | `tmux show-options -g history-limit` | Set `set-option -g history-limit 50000` in `~/.tmux.conf`. |
| **07** | High memory usage in SQLite WAL cache | Excessive index writes without WAL checkpointing. | `ls -lh ~/.cache/junie/*.db*` | Run `sqlite3 ~/.cache/junie/symbols.db "PRAGMA wal_checkpoint(TRUNCATE);"` to reclaim disk. |
| **08** | API rate limit error (`429 Too Many Requests`) | Rapid multi-iteration loop exhausted API quota. | `grep "429" ~/.local/share/junie/logs/daemon.log` | Configure exponential backoff and activate local fallback model (`junie config set fallback qwen-3.6-vl`). |
| **09** | Permission denied modifying git worktree | Ephemeral container running as root modified host file ownerships. | `ls -la src/` | Chown files to host user: `sudo chown -R $USER:$USER .`. |
| **10** | Neovim keybinding RPC timeout | Stale IPC socket connection. | `test -S /tmp/junie-ipc.sock && echo "alive"` | Remove dangling socket `rm /tmp/junie-ipc.sock` and restart editor session. |

## Related tools / concepts
- [Claude Code](claude-code.md) — Anthropic CLI agentic tool.
- [Aider](aider.md) — Command-line AI pair programming tool.
- [ripgrep (rg)](ripgrep.md) — High-speed line-oriented search tool.
- [Melty](melty.md) — Open-source AI code assistant.
- [Sourcegraph Cody](sourcegraph_cody.md) — AI codebase assistant with search integration.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open protocol for AI tools.

## Sources / references
- [JetBrains Junie CLI Product Homepage](https://junie.jetbrains.com/)
- [JetBrains AI Lab Research and Development Portal](https://blog.jetbrains.com/ai/)
- [GitHub - JetBrains Junie CLI Repository](https://github.com/jetbrains/junie)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
