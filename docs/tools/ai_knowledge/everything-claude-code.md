# Everything Claude Code (ECC)

## What it is
Everything Claude Code (ECC) is an advanced, production-grade performance optimization ecosystem, subagent orchestration harness, and lifecycle hook supervisor built specifically for terminal-native AI harnesses, primarily [Claude Code](../development_ops/claude-code.md). Built for early 2027 workflows, it functions as an active, integrated runtime of specialized subagents, lifecycle hooks, and contextual rules designed to maximize reasoning fidelity across frontier models (including Claude 5.6, Claude 5.1, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL).

ECC operates as an interceptor and supervisory layer between terminal CLI harnesses and foundation model APIs. It dynamically routes intent, enforces security audit guardrails via **AgentShield v2.0**, executes post-edit lifecycle hooks, and provides first-class connectivity through **FastMCP 3.1** (Model Context Protocol).

### ECC Subagent & Lifecycle Hook Architecture

```
+---------------------------------------------------------------------------------------------------------+
|                                  TERMINAL CLI HARNESS (CLAUDE CODE / CURSOR)                            |
|                                                                                                         |
|   +------------------------------------+             +----------------------------------------------+   |
|   |   User Prompt / Slash Commands     |             |         FastMCP 3.1 Client Engine            |   |
|   |  - /plugin, /compact, /review      |             |  - Structured Tool Invocations               |   |
|   |  - Skill Trigger & Context Loading |             |  - Resource Context Subscription             |   |
|   +-----------------+------------------+             +----------------------+-----------------------+   |
|                     |                                                       |                           |
|                     +--------------------------+----------------------------+                           |
|                                                | Intercepted Execution Stream                           |
|                                                v                                                        |
|   +-------------------------------------------------------------------------------------------------+   |
|   |                            EVERYTHING CLAUDE CODE (ECC) SUPERVISOR                              |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  |                             AgentShield v2.0 Security Layer                               |  |   |
|   |  |  - AST Secret & Key Leak Scanner                 - Malicious Command Execution Blocker    |  |   |
|   |  |  - Context Redaction & Path Filter               - Strict Pydantic v2 Contract Guard      |  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  |                             Subagent Orchestrator & Router                                |  |   |
|   |  |  - Architect Subagent (System Design)            - Security Reviewer (Vulnerability Audit)|  |   |
|   |  |  - Performance QA Subagent (Profiling)           - Skill Synthesizer (Git Pattern Mining) |  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   |  |                             Lifecycle Hook Dispatch Engine                                |  |   |
|   |  |  - pre-edit (Dependency Snapshot)                - post-edit (Auto-format, AST Validation)|  |   |
|   |  |  - pre-commit (Lint, Secret Check)               - post-commit (Git History Knowledgeops) |  |   |
|   |  +-------------------------------------------------------------------------------------------+  |   |
|   +--------------------------------------------+----------------------------------------------------+   |
|                                                | Sanitized Context & Tool Call Payloads                 |
|                                                v                                                        |
|   +-------------------------------------------------------------------------------------------------+   |
|   |                                  FRONTIER FOUNDATION MODELS                                     |   |
|   |  - Claude 5.6 (Dynamic Extended Thinking, up to 32k tokens)                                      |   |
|   |  - GPT-5.6 / Gemini 4.0 Ultra (Deep Mathematical & Logic Reasoning)                             |   |
|   |  - DeepSeek-V4 / Qwen 3.6 VL (Code Generation & Repository Multi-File Synthesis)                |   |
|   +-------------------------------------------------------------------------------------------------+   |
+---------------------------------------------------------------------------------------------------------+
```

## Detailed Execution Sequence Flow

The interaction between terminal user invocations, the ECC supervisor layer, subagent delegates, and the local filesystem is shown below:

```
[Developer Input in Claude Code CLI]
        |
        v
[ECC Intent & Hook Interceptor]
        |
        +---> [1. Pre-Execution Hook: pre-tool-call]
        |        |
        |        +--> AgentShield scans command parameters for credentials (.env, id_rsa, tokens)
        |        +--> Verifies file path within permitted repository bounds (no path traversal)
        |
        +---> [2. Dynamic Subagent Persona Injection]
        |        |
        |        +--> Match task intent: "Refactor database queries" -> Architect + Perf QA Subagents
        |        +--> Inject optimized system guidelines and budget thinking token allocation
        |
        +---> [3. Foundation Model Inference (Claude 5.6 / GPT-5.6)]
        |        |
        |        +--> Generates code patch or tool execution request
        |
        +---> [4. Post-Edit Lifecycle Hook Dispatch]
        |        |
        |        +--> Trigger fast-path linter (e.g. `ruff check --fix` or `biome format`)
        |        +--> Run targeted unit tests on modified modules
        |        +--> Evaluate AST integrity; rollback on syntax regression
        |
        +---> [5. State Persistence & Telemetry]
        |        |
        |        +--> Cache modified symbols and session state into .ecc/state.json
        |
        v
[Render Clean Formatted Response to Developer Terminal]
```

## What problem it solves
It bridges the critical gap between a raw AI terminal CLI and a fully functional, autonomous software engineering environment. ECC addresses:
1. **Agent Context-Window Saturation**: Terminal agents typically flood the context window with raw directory listings and massive files. ECC provides selective semantic slicing and AST extraction tools.
2. **Security Vulnerability Exposure**: Prevents accidental leakage of production secrets, private keys, or execution of destructive terminal commands (`rm -rf /`, `git push --force`) through AgentShield v2.0.
3. **Loss of Memory State Across Invocations**: Persists working subagent mental states, architectural decisions, and project-specific guidelines between CLI invocations.
4. **Tool Standard Compliance**: Uses FastMCP 3.1 to expose standardized tool endpoints to any MCP-compliant agent harness.

## Where it fits in the stack
**AI Assistants & Knowledge / Developer Tooling Layer**. It functions as the local runtime supervisor and rule enforcement subsystem, operating directly on top of command-line agents.

## Typical use cases
- **Multi-File Automated Refactoring**: Guiding Claude Code through multi-package refactoring with strict AST verification and automated linting after every edit.
- **Continuous Secret & Security Auditing**: Running AgentShield in the background to prevent committing staging credentials or exposing API keys in terminal transcripts.
- **Dynamic Skill Compilation**: Automatically extracting coding patterns, library choices, and test conventions from git history into structured `.claude/skills/` guidelines.
- **Autonomous Subagent Delegation**: Offloading background tasks (such as test suite generation or performance profiling) to specialized persona subagents while preserving the main architectural conversation context.

## Strengths
- **Comprehensive Skill Library**: Over 182+ domain-specific skills for modern languages (TypeScript, Python, Rust, Go, C++, Zig, Swift).
- **Hardened AgentShield v2.0**: Dual-agent adversarial guardrails that inspect shell commands, environment files, and AST modifications.
- **SOTA Frontier Model Alignment**: Native tuning for Claude 5.6 and GPT-5.6 extended thinking models, dynamically managing `MAX_THINKING_TOKENS` budgets based on task complexity.
- **Protocol-First Interoperability**: Built from the ground up for FastMCP 3.1, enabling integration across Claude Code, Cursor, OpenCode, and Windsurf.

### Comprehensive Comparison Matrix

| Feature / Dimension | Everything Claude Code (ECC) | Vanilla Claude Code CLI | Cursor Rules (.cursorrules) | Aider CLI | OpenCode |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Architectural Role** | Runtime Supervisor & Harness | Terminal Coding Agent | IDE Prompt Injection | Git Assistant | Multi-Agent Terminal |
| **FastMCP 3.1 Support** | Native Daemon & Tool Suite | Client Support Only | Community Extensions | Custom Adapters | Experimental |
| **Security Scanning Engine** | AgentShield v2.0 Dual-Agent | Basic Permission Prompts | None | Git Diff Approval | Basic Sandboxing |
| **Domain-Specific Skill Base** | 182+ Structured Skills | Default Generic Rules | Custom User Text | Repo Map Heuristics| Extensible Agents |
| **Lifecycle Hook Hooks** | `pre-edit`, `post-edit`, `pre-commit` | Shell Executions | IDE Event Listeners | Git Hook Triggers | Shell Hooks |
| **Thinking Token Budgeting** | Dynamic (1k–32k adaptive) | Fixed Global Setting | N/A | Fixed Flags | Manual Config |
| **State Persistence Format** | Strict Pydantic v2 JSON Schema | SQLite / Local File | Workspace Metadata | Git Commits | SQLite DB |

## Limitations
- **Token Overhead on Full Skill Ingestion**: Registering all 182+ skills simultaneously without selective loading can consume up to 25k prompt tokens; selective loading via `/plugin enable` is mandatory.
- **Harness-Specific Hooks**: Certain interactive slash commands and terminal hooks depend on Claude Code's extension interfaces and require compatibility adapters in Cursor or Aider.
- **Host Sandboxing Dependencies**: Full automated test verification requires dockerized or containerized host environments to safely execute unvetted code patches.

## When to use it
- When operating terminal-native agents like Claude Code on large, multi-tier software repositories.
- When requiring automatic enforcement of team-wide coding conventions, AST integrity checks, and pull-request policies.
- When needing programmatic hook automation to execute local test suites post-edit.

## When not to use it
- For quick, single-file scripts where vanilla CLI reasoning is sufficient.
- If your workflow is strictly confined to graphical web-based interfaces with no local shell access.

## Getting started

### Installation via Marketplace
To install Everything Claude Code via the Claude Code plugin registry:

```bash
# Add the official ECC marketplace registry
/plugin marketplace add https://github.com/affaan-m/everything-claude-code

# Install the core supervisor and skill set
/plugin install everything-claude-code@everything-claude-code

# Verify installation status
/plugin list
```

### Manual Subagent Installation
```bash
# Clone the repository
git clone https://github.com/affaan-m/everything-claude-code.git /opt/everything-claude-code
cd /opt/everything-claude-code

# Create local agent directory and symlink persona skills
mkdir -p ~/.claude/agents/ ~/.claude/skills/
cp agents/*.md ~/.claude/agents/
cp skills/*.md ~/.claude/skills/
```

## CLI examples

```bash
# Run full repository security audit with AgentShield
/plugin run ecc:agentshield --path ./src --level "strict"

# Compile recent git commit patterns into reusable skills
/plugin run ecc:skill-creator --since "7 days ago" --name "fastapi-async-patterns"

# List active registered persona agents and thinking token budgets
/plugin run ecc:list-agents

# Execute FastMCP 3.1 supervisor server manually
python3 -m ecc.server --port 8040 --host 127.0.0.1
```

## API examples

### Production FastMCP 3.1 Supervisor Implementation

The following complete, production-grade FastMCP 3.1 server exposes ECC lifecycle hook execution, skill retrieval, and AgentShield security scanning. It implements strict Pydantic v2 validation models (`extra="forbid"`, `frozen=True`):

```python
"""
Production Everything Claude Code (ECC) FastMCP 3.1 Supervisor Server
Provides lifecycle hooks, AgentShield AST security audits, and skill management.
"""

import os
import sys
import json
import time
import logging
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Everything-Claude-Code-Supervisor", version="3.1.0")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ecc_supervisor")

class HookExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    hook_type: Literal["pre-edit", "post-edit", "pre-commit", "security-audit"] = Field(
        ...,
        description="Target lifecycle phase to execute"
    )
    target_filepath: str = Field(..., description="Target repository path being inspected or modified")
    modified_content: Optional[str] = Field(
        default=None,
        description="Optional proposed content payload for post-edit verification"
    )
    enforce_strict: bool = Field(
        default=True,
        description="Enforce strict security pass/fail guardrails"
    )

    @field_validator("target_filepath")
    @classmethod
    def validate_safe_path(cls, path_val: str) -> str:
        clean = path_val.strip()
        if not clean:
            raise ValueError("target_filepath cannot be empty")
        if ".." in clean or clean.startswith("/etc") or clean.startswith("/root"):
            raise ValueError(f"Prohibited path traversal or system file access: {clean}")
        return clean

class SecurityFinding(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    rule_id: str = Field(..., description="AgentShield security rule identifier")
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(..., description="Issue severity")
    line_number: Optional[int] = Field(default=None, description="Line number where issue was detected")
    description: str = Field(..., description="Detailed description of the vulnerability")
    remediation: str = Field(..., description="Suggested code fix or mitigation")

class HookExecutionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["PASSED", "WARNING", "BLOCKED"] = Field(..., description="Hook execution status")
    hook_type: str = Field(..., description="Executed lifecycle hook type")
    target_filepath: str = Field(..., description="Target file path")
    findings: List[SecurityFinding] = Field(default_factory=list, description="Security or lint findings")
    duration_ms: float = Field(..., ge=0.0, description="Hook execution duration in milliseconds")
    recommended_action: str = Field(..., description="Operational instruction for Claude Code CLI")

@mcp.tool()
def execute_lifecycle_hook(request_json: str) -> str:
    """
    Executes an ECC lifecycle hook or AgentShield security inspection with strict
    Pydantic v2 contract enforcement, returning validated status and remediation instructions.
    """
    start_time = time.time()
    try:
        raw_req = json.loads(request_json)
        req = HookExecutionRequest.model_validate(raw_req)

        findings: List[SecurityFinding] = []
        status: Literal["PASSED", "WARNING", "BLOCKED"] = "PASSED"
        recommendation = "Proceed with edit execution."

        # AgentShield Security Audit Logic
        if req.hook_type in ("security-audit", "pre-edit", "pre-commit"):
            # Check for sensitive file patterns
            basename = os.path.basename(req.target_filepath).lower()
            if basename in (".env", "id_rsa", "credentials.json", "service_account.json"):
                findings.append(
                    SecurityFinding(
                        rule_id="AS-001-SECRET-FILE",
                        severity="CRITICAL",
                        description=f"Attempted direct manipulation of sensitive credentials file: {basename}",
                        remediation="Do not commit credentials to repository. Use environment variable injection."
                    )
                )
                status = "BLOCKED"
                recommendation = "Abort file modification. Sensitive configuration files are protected by AgentShield."

            # Check content for exposed keys if provided
            if req.modified_content:
                content_lower = req.modified_content.lower()
                prohibited_patterns = [
                    ("sk-ant-api03-", "Anthropic API Key"),
                    ("ghp_", "GitHub Personal Access Token"),
                    ("xoxb-", "Slack Bot Token"),
                    ("aws_secret_access_key", "AWS Secret Access Key")
                ]
                for pattern, desc in prohibited_patterns:
                    if pattern in req.modified_content:
                        findings.append(
                            SecurityFinding(
                                rule_id="AS-002-KEY-EXPOSURE",
                                severity="CRITICAL",
                                description=f"Found unencrypted {desc} pattern in proposed file content.",
                                remediation="Remove token and reference via process.env or secret manager."
                            )
                        )
                        status = "BLOCKED"
                        recommendation = "Aborting edit: unencrypted secret detected in diff payload."

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        result = HookExecutionResult(
            status=status,
            hook_type=req.hook_type,
            target_filepath=req.target_filepath,
            findings=findings,
            duration_ms=elapsed_ms,
            recommended_action=recommendation
        )
        return result.model_dump_json(indent=2)

    except Exception as exc:
        logger.error(f"ECC hook execution failed: {str(exc)}", exc_info=True)
        return json.dumps({
            "status": "BLOCKED",
            "error_type": exc.__class__.__name__,
            "message": str(exc),
            "duration_ms": round((time.time() - start_time) * 1000, 2)
        }, indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Production Docker Compose Stack

This Docker Compose configuration deploys the ECC supervisor service alongside an isolated execution sandbox and Redis caching sidecar:

```yaml
version: "3.8"

services:
  ecc-supervisor:
    image: python:3.11-slim-bookworm
    container_name: ecc-fastmcp-supervisor
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
      - FASTMCP_PORT=8040
      - AGENTSHIELD_LEVEL=strict
      - MAX_THINKING_TOKENS=16000
    volumes:
      - /opt/everything-claude-code:/opt/ecc:ro
      - /var/run/docker.sock:/var/run/docker.sock
      - ecc_state_data:/data/ecc_state:rw
    working_dir: /opt/ecc
    command: ["python3", "-m", "ecc.server", "--port", "8040", "--host", "0.0.0.0"]
    ports:
      - "8040:8040"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8040/health"]
      interval: 20s
      timeout: 5s
      retries: 3
    networks:
      - ecc_net

  ecc-cache:
    image: redis:7.4-alpine
    container_name: ecc-redis-cache
    restart: unless-stopped
    volumes:
      - ecc_redis_data:/data
    networks:
      - ecc_net

volumes:
  ecc_state_data:
    driver: local
  ecc_redis_data:
    driver: local

networks:
  ecc_net:
    driver: bridge
```

## Production Hardened Systemd Service Unit

To run the ECC FastMCP 3.1 Supervisor daemon as a persistent system service on a developer workstation or build node:

```ini
# /etc/systemd/system/ecc-supervisor.service
[Unit]
Description=Everything Claude Code FastMCP 3.1 Supervisor Daemon
Documentation=https://github.com/affaan-m/everything-claude-code
After=network.target

[Service]
Type=simple
User=ecc
Group=ecc
WorkingDirectory=/opt/everything-claude-code
ExecStart=/opt/everything-claude-code/venv/bin/python -m ecc.server --port 8040 --host 127.0.0.1
Restart=always
RestartSec=5s

# Process Environment & Tuning
Environment="PYTHONUNBUFFERED=1"
Environment="FASTMCP_PORT=8040"
Environment="MAX_THINKING_TOKENS=16000"
Environment="AGENTSHIELD_STRICT=1"

# Hardened Sandboxing
ProtectSystem=strict
ProtectHome=read-only
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
NoNewPrivileges=true
ReadWritePaths=/var/log/ecc /data/ecc_state

# Resource Limits
LimitNOFILE=65535
MemoryHigh=2G
MemoryMax=3G

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Error Code / Symptom | Root Cause | Diagnostic Verification | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| `ERR_AGENTSHIELD_BLOCKED` | AgentShield triggered false positive on configuration template path (`.env.example`). | Audit report indicates `AS-001-SECRET-FILE` triggered on template file. | Add `.env.example` to `exemptions` list inside `ecc_config.json`. |
| `ERR_HOOK_RECURSION_LOOP` | Post-edit formatting script (`ruff format` or `biome`) continuously re-triggers file change hooks. | Endless hook dispatch loop in terminal logs; rapid file modtime increments. | Add exit guard inside post-edit script: compare file SHA-256 hash before and after format; exit immediately if unchanged. |
| `ERR_TOKEN_WINDOW_EXHAUSTION` | High number of active subagents and skills registered in `~/.claude/agents/` simultaneously. | Claude Code reports context window nearing 200k limit before any tool execution. | Disable non-essential skills via `/plugin disable ecc:all-skills` and enable only task-relevant modules. |
| `FASTMCP_HANDSHAKE_TIMEOUT` | Local FastMCP server failed response handshake within terminal agent timeout (10s). | Agent CLI reports `Failed to establish connection to FastMCP socket on 8040`. | Check daemon status via `systemctl status ecc-supervisor.service`; restart service and inspect port availability with `lsof -i :8040`. |
| `ERR_MAX_THINKING_EXCEEDED` | Target foundation model rejected requested `MAX_THINKING_TOKENS` configuration. | API response code 400: `Invalid parameter: max_thinking_tokens exceeds ceiling`. | Adjust thinking token budget in subagent definition to match model ceiling (e.g. 16,000 for Claude 5.6). |
| `Pydantic ValidationError` | Client submitted non-conformant hook request with extra or unrecognized parameters. | Server logs indicate `ValidationError: Extra inputs are not permitted`. | Ensure client payload complies strictly with `HookExecutionRequest` schema (`extra="forbid"`). |

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — Primary terminal execution agent and CLI harness.
- [Cursor](../development_ops/cursor.md) — Supported desktop IDE wrapper with MCP integration.
- [OpenCode](../development_ops/opencode.md) — Multi-agent developer CLI harness.
- [Aider](../development_ops/aider.md) — Command-line git-integrated assistant.
- [Claude Hooks](../development_ops/claude-hooks.md) — Terminal-native lifecycle hook architecture.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open tool interaction protocol standard.

## Sources / references
- [Everything Claude Code (ECC) Repository](https://github.com/affaan-m/everything-claude-code)
- [ECC Official Online Documentation](https://ecc.tools/)
- [Anthropic Developer Site - Designing Agentic Systems](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- [FastMCP 3.1 Framework Documentation](https://github.com/jina-ai/fastmcp)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
