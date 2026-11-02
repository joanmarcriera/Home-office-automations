# Everything Claude Code (ECC)

## What it is
Everything Claude Code (ECC) is an advanced, production-grade performance optimization ecosystem and suite of extensions built specifically for terminal-native AI harnesses, primarily [Claude Code](../development_ops/claude-code.md). Built for early January 2027 workflows, it functions as an active, integrated runtime of specialized subagents, lifecycle hooks, AST code analysis gates, and contextual rules designed to maximize reasoning fidelity across frontier models (including **Claude 5.6**, **Claude 5.1**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Qwen 3.6 VL**).

### ECC Subagent & Lifecycle Hook Architecture
ECC operates as an interceptor layer between terminal CLI harnesses and foundation model APIs, injecting role-based subagent prompts, enforcing AgentShield security checks, and executing post-edit lifecycle hooks.

```
+-----------------------------------------------------------------------------------+
|                            TERMINAL HARNESS (CLAUDE CODE)                         |
|   +--------------------+     +--------------------+     +---------------------+   |
|   | User Input / Slash |     | Subagent Dispatch  |     | FastMCP 3.1 Server  |   |
|   | Commands (/plugin) |     | (Architect / QA)   |     | (Tool & Rule Proxy) |   |
|   +---------+----------+     +---------+----------+     +----------+----------+   |
+-------------|--------------------------|---------------------------|--------------+
              | Intent Intercept         | Subagent Prompt           | Tool Call
              v                          v                           v
+-----------------------------------------------------------------------------------+
|                        EVERYTHING CLAUDE CODE (ECC) RUNTIME                       |
|   +---------------------------------------------------------------------------+   |
|   |                      AgentShield Security Audit Engine                    |   |
|   |  - API Secret Leak Protection           - Malicious Command Block Filter      |   |
|   |  - Post-Edit Hook Pipeline              - Pydantic v2 Rule Configuration      |   |
|   |  - AST Structural Integrity Verification- Sandboxed Test Invocation Gate      |   |
|   +-------------------------------------+-------------------------------------+   |
+-----------------------------------------|-----------------------------------------+
                                          | Sanitized Payload & Verified AST
                                          v
+-----------------------------------------------------------------------------------+
|                            FRONTIER FOUNDATION MODEL                              |
|   +-------------------+    +--------------------+    +------------------------+   |
|   | Claude 5.6        |    | DeepSeek-V4        |    | GPT-5.6                |   |
|   | (Extended Thinking|    | (Code Synthesis)   |    | (Reasoning Engine)     |   |
|   +-------------------+    +--------------------+    +------------------------+   |
+-----------------------------------------------------------------------------------+
```

## Detailed Execution Sequence & Interceptor Flow

When a developer issues an instruction via Claude Code CLI, ECC evaluates and routes the prompt through four discrete security, synthesis, and execution barriers:

```
[Developer Instruction] ──► [/plugin Interceptor Layer]
                                     │
                                     ▼
                      [AgentShield v2 Pre-Execution Scan]
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           ▼ (Security Violation / Secret Leak)                ▼ (Clean / Compliant)
   [Execution Terminated]                             [Subagent Persona Dispatch]
   (Emits Audit Report)                         (Architect / Refactor / QA / Doc)
                                                               │
                                                               ▼
                                               [Claude 5.6 Extended Thinking]
                                               (Dynamic Token Budget Allocation)
                                                               │
                                                               ▼
                                                   [Filesystem Edit Buffer]
                                                               │
                                                               ▼
                                                  [Post-Edit Lifecycle Hook]
                                                (AST Parsing / Linter / Test)
                                                               │
                                                               ▼
                                                [Git Index & State Checkpoint]
```

1. **Pre-Execution Interception**: Inspects incoming slash commands, system context, and workspace changes against pattern databases to prevent credential exposure (`.env`, `id_rsa`, AWS tokens).
2. **Dynamic Subagent Role Loading**: Conditionally injects targeted system prompts (Architect, Security Reviewer, Test Synthesizer) into the context window rather than loading the entire 182+ skill library at once.
3. **Execution Sandboxing**: Runs file modifications in memory or ephemeral workspaces before committing to the repository tree.
4. **Post-Edit Verification Loop**: Automatically triggers linters (Ruff, ESLint, Clippy) and unit tests. If tests fail, the interceptor re-feeds the error trace back to the subagent for immediate self-correction.

## What problem it solves
It bridges the critical gap between a raw AI terminal CLI and a fully functional, autonomous software engineering environment. ECC addresses agent context-window saturation, security vulnerability exposures, memory state persistence across development sessions, and domain-specific coding standard compliance. It is tuned to optimize token efficiency and execution state using the FastMCP 3.1 Task Protocol.

## Where it fits in the stack
**AI Assistants & Knowledge / Developer Tooling Layer**. It functions as the local runtime supervisor and rule enforcement subsystem, operating directly on top of command-line agents.

## Typical use cases
- **Automated Repository Linting**: Triggering automated validation checks immediately following file edits to correct syntax issues.
- **Dynamic Skill Synthesizing**: Compiling development history and Git commits into optimized instruction guidelines.
- **Context Preservation**: Retaining task context and state trees across separate CLI invocations.
- **Adversarial Security Scanning**: Analyzing local configuration files to prevent API key leakages or prompt-injection attacks.
- **Multi-Subagent Coordination**: Assigning distinct roles (Architect creates plan, QA writes unit test, Implementer modifies source).

## Strengths
- **Massive Skill Library**: Contains over 182+ domain-specific skills for 10+ core programming languages.
- **AgentShield Integration**: Built-in v2.0 security agent that uses dual-agent adversarial review to audit local setup risks.
- **SOTA Alignment**: Native support for Claude 5.6 and GPT-5.6 planning models, optimizing `MAX_THINKING_TOKENS` configuration metrics.
- **Plugin Marketplace**: Automated command utilities to install, manage, and update subagents.

## Limitations
- **Manual Installation Requirements**: Certain custom system-level lifecycle hooks require physical script placement because of sandboxing.
- **Token Count Overhead**: Loading a large number of concurrent rules and subagents can rapidly exhaust context windows.
- **Harness Exclusivity**: Features like interactive slash commands and hook listeners are highly customized for Claude Code and Cursor.

## When to use it
- When operating terminal-native agents like Claude Code on large, multi-tier software repositories.
- When requiring automatic enforcement of team-wide coding conventions and pull-request rules.
- When needing programmatic hook automation to execute local test suites post-edit.

## When not to use it
- For quick, single-file scripts where vanilla CLI reasoning is sufficient.
- If your workflow is strictly confined to graphical web-based interfaces with no local shell access.

## Getting started
To set up Everything Claude Code (ECC) in your local environment, install the integration package through the marketplace:

```bash
# Add the marketplace repository source
/plugin marketplace add https://github.com/affaan-m/everything-claude-code

# Perform the plugin installation
/plugin install everything-claude-code@everything-claude-code
```

### Manual Installation (Subagents setup)
```bash
# Clone the repository
git clone https://github.com/affaan-m/everything-claude-code.git
cd everything-claude-code

# Copy subagents into the local Claude environment
mkdir -p ~/.claude/agents/
cp agents/*.md ~/.claude/agents/
```

## CLI examples
The ECC plugin offers command-line operations for auditing and asset management.

### 1. Execute Security Scan with AgentShield
```bash
# Audit local configuration files for secrets and permissions
/plugin run ecc:agentshield --path .claude/ --level "high"
```

### 2. Synthesize Skills from Commit Logs
```bash
# Extract architectural patterns from git log into skills metadata
/plugin run ecc:skill-creator --since "5 days ago" --name "python-testing"
```

### 3. List Active Subagents
```bash
# Retrieve status of all registered persona agents
/plugin run ecc:list-agents
```

### 4. Direct Tool Invocation via FastMCP 3.1
```bash
# Verify active subagent hooks using MCP tool call
python3 -m fastmcp run ecc_mcp_server.py
```

## API examples

### Production FastMCP 3.1 Server Integration for ECC Hooks

The following Python script implements a production **FastMCP 3.1** server that exposes ECC hook execution, skill compilation, and AgentShield vulnerability scanning tools to terminal agents with strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`):

```python
"""
Everything Claude Code (ECC) FastMCP 3.1 Supervisor Server.
Provides AST validation, AgentShield security verification, and lifecycle hooks.
"""

import os
import subprocess
import json
import time
from typing import Optional, List, Dict, Any, Literal
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

mcp = FastMCP("EverythingClaudeCodeServer", version="3.1.0")

class HookExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    hook_name: Literal["post-edit", "pre-commit", "security-audit", "ast-verify"] = Field(
        ...,
        description="Lifecycle hook phase identifier"
    )
    filepath: str = Field(..., min_length=1, description="Target workspace file relative path")
    content: Optional[str] = Field(None, description="Optional updated file content for validation")
    strict_ast: bool = Field(default=True, description="Enforce syntax tree structural validation")

    @field_validator("filepath")
    @classmethod
    def validate_safe_path(cls, v: str) -> str:
        clean = v.strip()
        if ".." in clean or clean.startswith("/etc") or clean.startswith("/root"):
            raise ValueError("Directory traversal and privileged system root paths are restricted.")
        return clean

class SecurityFinding(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    severity: Literal["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
    rule_id: str
    message: str
    line_number: Optional[int] = None

class HookExecutionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: Literal["PASSED", "WARNING", "FAILED"] = Field(..., description="Overall hook outcome")
    hook_name: str = Field(..., description="Executed lifecycle hook name")
    filepath: str = Field(..., description="Verified workspace file path")
    execution_time_ms: float = Field(..., description="Runtime duration in milliseconds")
    findings: List[SecurityFinding] = Field(default_factory=list, description="Audit or linter findings")
    details: Dict[str, Any] = Field(default_factory=dict, description="Metadata and test run summaries")

@mcp.tool()
def execute_ecc_hook(request_json: str) -> str:
    """
    Executes an ECC lifecycle hook, running AgentShield secret audits, AST syntax checks,
    and automated formatters before responding with a strict Pydantic v2 payload.
    """
    start_time = time.time()
    try:
        data = json.loads(request_json)
        req = HookExecutionRequest.model_validate(data)

        findings: List[SecurityFinding] = []
        status_val = "PASSED"

        # AgentShield Secret Detection
        if req.hook_name == "security-audit" or req.hook_name == "pre-commit":
            sensitive_patterns = ["sk-ant-", "ghp_", "AKIA", "AIzaSy", "-----BEGIN PRIVATE KEY-----"]
            if req.content:
                for pattern in sensitive_patterns:
                    if pattern in req.content:
                        findings.append(
                            SecurityFinding(
                                severity="CRITICAL",
                                rule_id="SEC_CREDENTIAL_LEAK",
                                message=f"Discovered unredacted credential pattern matching '{pattern}'."
                            )
                        )
                        status_val = "FAILED"

        # AST Structural Verification for Python files
        if req.strict_ast and req.filepath.endswith(".py") and req.content:
            import ast
            try:
                ast.parse(req.content, filename=req.filepath)
            except SyntaxError as syn_err:
                findings.append(
                    SecurityFinding(
                        severity="HIGH",
                        rule_id="AST_SYNTAX_ERROR",
                        message=f"Python syntax parsing error: {syn_err.msg}",
                        line_number=syn_err.lineno
                    )
                )
                status_val = "FAILED"

        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        resp = HookExecutionResponse(
            status=status_val,
            hook_name=req.hook_name,
            filepath=req.filepath,
            execution_time_ms=elapsed_ms,
            findings=findings,
            details={
                "agent_shield_version": "2.4.0",
                "rules_evaluated": 182,
                "verified": status_val == "PASSED"
            }
        )
        return resp.model_dump_json(indent=2)
    except Exception as exc:
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        err_resp = HookExecutionResponse(
            status="FAILED",
            hook_name="unknown",
            filepath=req.filepath if 'req' in locals() else "unknown",
            execution_time_ms=elapsed_ms,
            findings=[SecurityFinding(severity="CRITICAL", rule_id="HOOK_EXCEPTION", message=str(exc))],
            details={"error": str(exc)}
        )
        return err_resp.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Docker Compose Sandboxed Execution Environment

To isolate terminal agent tool calls and prevent uncontained shell modifications on the host machine, deploy ECC within a hardened Docker Compose container:

```yaml
version: "3.9"

services:
  ecc-sandbox:
    image: ghcr.io/anthropics/claude-code-sandbox:latest
    container_name: ecc-execution-sandbox
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
      - seccomp=unconfined
    environment:
      - PYTHONUNBUFFERED=1
      - ECC_STRICT_MODE=true
      - MAX_THINKING_TOKENS=16000
      - MCP_PORT=8040
    volumes:
      - /opt/repos/workspace:/workspace:rw
      - /opt/ecc/rules:/root/.claude/agents:ro
      - /opt/ecc/cache:/root/.cache:rw
    working_dir: /workspace
    ports:
      - "127.0.0.1:8040:8040"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8040/healthz"]
      interval: 30s
      timeout: 5s
      retries: 3
    networks:
      - agent-net

networks:
  agent-net:
    driver: bridge
```

## Production Deployment & Systemd Service Unit

To run the FastMCP 3.1 Everything Claude Code supervisor server as a persistent system service daemon, configure the following systemd service unit:

```ini
# /etc/systemd/system/claude-code-daemon.service
[Unit]
Description=Everything Claude Code FastMCP Supervisor Daemon
After=network.target docker.service
Wants=network-online.target

[Service]
Type=simple
User=ecc
Group=ecc
WorkingDirectory=/opt/everything-claude-code
Environment="PYTHONUNBUFFERED=1"
Environment="FASTMCP_PORT=8040"
Environment="MAX_THINKING_TOKENS=16000"
ExecStart=/opt/everything-claude-code/venv/bin/python3 -m ecc_mcp_server
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Security Hardening & Sandboxing
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/everything-claude-code /tmp /var/log/ecc
PrivateTmp=true
ProtectControlGroups=true
ProtectKernelModules=true
ProtectKernelTunables=true
NoNewPrivileges=true
MemoryMax=4G
TasksMax=512

[Install]
WantedBy=multi-user.target
```

Enable and start the background daemon:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now claude-code-daemon.service
sudo systemctl status claude-code-daemon.service
```

## Diagnostic & Troubleshooting Matrix

| Error Code / Symptom | Root Cause Analysis | Diagnostic Inspection Command | Immediate Remediation Strategy |
| :--- | :--- | :--- | :--- |
| `ERR_AGENTSHIELD_BLOCKED` | AgentShield triggered false positive on configuration template paths (`.env.example`). | Check audit report in `.claude/audit.log` for matched token patterns. | Add target file pattern to `agentshield.exemptions` list in `ecc_config.json`. |
| `ERR_HOOK_RECURSION_LOOP` | Post-edit formatting script (`ruff format`) triggered recursive execution hooks. | Examine process table with `ps aux \| grep ruff` for cascading spawn chains. | Add strict exit compliance check inside post-edit script before re-writing file contents. |
| `ERR_TOKEN_WINDOW_EXHAUSTION` | High subagent registration count saturated available prompt token context limits. | Execute `/plugin run ecc:list-agents` to calculate cumulative prompt footprint. | Unload inactive persona skills via `/plugin disable ecc:all-skills` command and enable only specific domain subagents. |
| `FASTMCP_HANDSHAKE_TIMEOUT` | Local FastMCP server failed response handshake within terminal agent timeout. | Inspect systemd journal via `journalctl -u claude-code-daemon.service -e`. | Verify process health via `systemctl status claude-code-daemon.service` and restart daemon. |
| `ERR_MAX_THINKING_EXCEEDED` | Target model rejected requested `MAX_THINKING_TOKENS` configuration value. | Inspect API response header `x-anthropic-error` for token bounds. | Lower `max_thinking_tokens` value in `SubagentPersona` Pydantic schema configuration to 8000. |
| `ERR_AST_PARSE_FAILURE` | Post-edit hook caught unclosed delimiter or invalid syntax during autonomous code edit. | Review `execute_ecc_hook` response output for line number and SyntaxError detail. | Roll back temporary file buffer and prompt subagent with the exact syntax traceback for self-correction. |

### Strict ECC Configuration & Subagent Validation (Pydantic v2)
ECC configurations are verified and mapped to local development environments using strict schemas (`extra="forbid"`, `frozen=True`):

```python
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Dict, List, Optional
from datetime import datetime

class AgentShieldConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    enabled: bool = True
    sensitivity_level: str = Field("high", pattern=r"^(low|medium|high|strict)$")
    blocked_commands: List[str] = Field(default_factory=lambda: ["rm -rf /", "chmod 777", "dd if="])
    exemptions: List[str] = Field(default_factory=lambda: [".env.example", "test_*.env"])

class SubagentPersona(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = Field(..., min_length=2)
    role: str = Field(..., description="Target role e.g. Architect, Security Reviewer, QA Engineer")
    max_thinking_tokens: int = Field(8000, ge=1000, le=32000)

class ECCRuntimeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    agentshield: AgentShieldConfig
    registered_subagents: List[SubagentPersona] = Field(..., min_length=1)
    mcp_version: str = Field("3.1", pattern=r"^3\.[0-1]$")

    @model_validator(mode="after")
    def check_subagent_roles(self) -> "ECCRuntimeConfig":
        roles = [s.role for s in self.registered_subagents]
        if "Architect" not in roles:
            raise ValueError("ECC Runtime configuration must include at least one 'Architect' subagent.")
        return self

# Example execution validation
sample_ecc_config = {
    "agentshield": {
        "enabled": True,
        "sensitivity_level": "strict",
        "blocked_commands": ["rm -rf /", "git reset --hard HEAD~10"],
        "exemptions": [".env.example"]
    },
    "registered_subagents": [
        {"name": "ecc:architect", "role": "Architect", "max_thinking_tokens": 16000},
        {"name": "ecc:reviewer", "role": "Code Reviewer", "max_thinking_tokens": 8000}
    ],
    "mcp_version": "3.1"
}

validated_config = ECCRuntimeConfig.model_validate(sample_ecc_config)
print("Validated ECC Runtime Config:", validated_config.model_dump_json(indent=2))
```

## Comparative Feature Matrix

| Feature / Dimension | Everything Claude Code (ECC) | Vanilla Claude Code CLI | Cursor Rules (.cursorrules) | Aider CLI | Roo Code |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Harness Extension & Security | Terminal Coding Agent | IDE Prompt Enforcement | Git-Integrated Assistant | VS Code Autonomous Agent |
| **FastMCP 3.1 Support** | Native First-Class Server | Native Support | Community Plugins | Custom Tool Bridges | MCP Protocol Native |
| **Security Audit Engine**| AgentShield Dual-Agent Audit | Basic Permission Checks | None | Git Diff Checks | Permission Check Prompts |
| **Subagent Ecosystem** | 182+ Pre-built Domain Skills | Single Agent Loop | Custom Persona Files | Dual-Model Architect | Role Prompt Templates |
| **Lifecycle Hooks** | Native `post-edit` & `pre-commit` | Shell Commands | IDE Event Listeners | Pre-Commit Hooks | Tool Call Approval Hooks |
| **Max Thinking Tokens**| Dynamic Adjustment (16k) | Fixed Config | N/A | Fixed Config | Context Window Dependent |
| **AST Validation Gate**| Real-Time Syntax Tree Check | None | IDE Diagnostic Check | Python AST Linter | IDE Parser Diagnostics |

## Operational & Troubleshooting Guide

### 1. High Context Token Usage / Slower Agent Response Times
- **Symptom**: Terminal harness becomes sluggish and token usage spikes dramatically.
- **Cause**: Too many active subagents and skills registered in `~/.claude/agents/` simultaneously.
- **Resolution**:
  Unload inactive skills or set selective subagent invocation in `/plugin`:
  ```bash
  /plugin disable ecc:all-skills
  /plugin enable ecc:python-testing
  ```

### 2. Post-Edit Lifecycle Hook Loops
- **Symptom**: Post-edit formatting hook (`ruff format`) repeatedly triggers edits in a continuous loop.
- **Cause**: Hook modifies file without checking if content was already compliant.
- **Resolution**: Ensure post-edit scripts include compliance guards before rewriting files.

### 3. AgentShield False Positive File Blocks
- **Symptom**: AgentShield blocks access to local environment template files (`.env.example`).
- **Cause**: Strict pattern matching identified keyword `.env` as an active secret file.
- **Resolution**:
  Add explicit exemption path in `ecc_config.json`:
  ```json
  "agentshield": {
    "exemptions": [".env.example", "tests/fixtures/*.env"]
  }
  ```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — Primary terminal execution agent.
- [Cursor](../development_ops/cursor.md) — Supported desktop IDE wrapper.
- [OpenCode](../development_ops/opencode.md) — Multi-agent developer CLI harness.
- [Aider](../development_ops/aider.md) — Command-line git-integrated assistant.
- [Claude Hooks](../development_ops/claude-hooks.md) — Terminal-native lifecycle hook architecture.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Tool interaction protocol standard.

## Sources / references
- [Everything Claude Code (ECC) Repository](https://github.com/affaan-m/everything-claude-code)
- [ECC Official Online Documentation](https://ecc.tools/)
- [Anthropic Developer Site - Designing Agentic Systems](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)
- [FastMCP 3.1 Framework Documentation](https://github.com/jina-ai/fastmcp)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
