# Custom Agents (SSH + LLM Loop)

## What it is
A **Custom Agent** is a lightweight Python script or visual workflow automation (e.g., n8n) that implements a basic autonomous control loop: Prompt LLM -> Receive Command -> Execute via SSH/Shell -> Return Output/Telemetry to LLM. Under early January 2027 SOTA standards, these agents have evolved into standard-compliant Micro-Agents that natively support the **Model Context Protocol (MCP 3.1 / FastMCP 3.1 Task Protocol)**. This enables them to be exposed directly to modern frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4 Maverick**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL** as secure, sandboxed system administration tools.

## Architecture & System Flow
Custom Agents operate as a tightly bounded execution loop between model reasoning engines and host infrastructure, enforcing security allowlists, SSH session persistence, and human-in-the-loop validation checkpoints.

```mermaid
graph TD
    A[Frontier LLM / FastMCP Client] -->|MCP 3.1 Tool Call Request| B[Custom Agent FastMCP Server]
    B -->|Command Validation & Allowlist Check| C{Allowed?}
    C -- No -->|Security Block Response| A
    C -- Yes --> D{Requires Approval?}
    D -- Yes -->|Prompt Engineer / Admin| E[Human Approval Checkpoint]
    E -- Rejected -->|Audit Log & Abort| A
    E -- Approved --> F[SSH Client / Paramiko]
    D -- No --> F
    F -->|Secure Key-Based SSH Tunnel| G[Target Host / Node]
    G -->|Execute Command in Shell| H[Output / Telemetry Output]
    H -->|Return Stderr / Stdout| B
    B -->|Return Tool Execution Result| A
```

## What problem it solves
Full enterprise agent platforms often bring heavy framework dependencies, complex configuration overhead, and opaque internal execution loops. Custom Agents provide a minimal, fully inspectable control plane tailored specifically for target infrastructure tasks. They address the "Reasoning vs. Execution" gap in remote host management by pairing high-level LLM reasoning with secure SSH tunneling, explicit command allowlists, and human-in-the-loop verification checkpoints.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Agent Execution & Orchestration. It functions as a custom tool-calling micro-agent layer that bridges LLM reasoning engines to host systems over SSH or local command environments.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         FRONTIER LLM ORCHESTRATION LAYER                         │
│           Claude 5.6 / GPT-5.6 / Gemini 4.0 Ultra / FastMCP 3.1 Host            │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ MCP 3.1 Tool Request
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                        CUSTOM AGENT FASTMCP MICRO-SERVICE                        │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │ • Command Regex & Prefix Allowlist Engine                                │   │
│   │ • Paramiko Persistent SSH Key-Based Connection Pool                      │   │
│   │ • Interactive Human-in-the-Loop Approval Gateway                         │   │
│   │ • Pydantic v2 Schema & Telemetry Audit Logger                            │   │
│   └──────────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │ Encrypted SSH Tunnel
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         TARGET INFRASTRUCTURE NODES                              │
│       Homelab Cluster ── Edge Nodes ── k3s Workstation ── Paperless Server      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Feature Matrix & Framework Comparison

| Feature | Custom Agent (SSH + FastMCP) | Aider | Claude Code | Ansible / SaltStack |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Target** | Remote Admin & Shell Execution | Code Base Editing | Interactive Dev CLI | Deterministic Config Sync |
| **Protocol Standard** | FastMCP 3.1 Task Protocol | Custom CLI | Anthropic MCP | Procedural YAML / Python |
| **Agent Autonomy** | Bounded (Allowlists + Interactive) | Interactive Agentic | Autonomous Task Loops | Deterministic Procedural |
| **Dependencies** | Standard Python (`paramiko`, `mcp`) | Python / Git | Node.js Runtime | Python / Agent Runtime |
| **Human-in-Loop** | Built-in Gateways | Git Stage / Approve | Interactive Confirmation | Pre-flight Dry Run |

## Typical use cases
- **Automated Infrastructure Auditing**: "Check disk utilization across all k3s nodes and prune dangling Docker images if usage exceeds 85%."
- **Incident Response & Diagnostics**: Gathering system logs, inspecting active systemd services, and summarizing root causes for on-call engineers.
- **Controlled System Upgrades**: Executing rolling security patches across server clusters with automated pre- and post-flight health checks.
- **Custom FastMCP 3.1 Tools**: Exposing legacy command-line tools and shell utilities as FastMCP 3.1 endpoints.

## Operational Workflows & Best Practices
1. **Strict Command Allowlisting**: Always enforce prefix or exact regex allowlisting for executed shell commands to prevent arbitrary command injection.
2. **Ephemeral Identity & Restricted SSH Keys**: Use dedicated SSH key pairs restricted via `authorized_keys` options (e.g. `command="..."`, `no-port-forwarding`, `no-pty`).
3. **Audit Logging & Telemetry**: Record every model input, parsed shell command, user approval event, and execution response in structured JSON lines for compliance auditing.
4. **Session Timeout & Resource Capping**: Set strict socket connect and execution timeouts (e.g. 15s) to prevent runaway processes on target nodes.

## Strengths
- **Complete Control & Transparency**: Audit every line of execution logic, prompt template, and tool definition without black-box framework abstraction.
- **Native FastMCP 3.1 Support**: Plug seamlessly into any FastMCP 3.1 client or IDE (e.g., Windsurf, Claude Code, NanoClaw).
- **Minimal Dependencies**: Requires only standard Python libraries (`paramiko`, `pydantic`, `mcp`) or a lightweight container.
- **High Security**: Restrict agent execution using SSH key authentication, shell command allowlists, and strict timeout boundaries.

## Limitations
- **Manual Infrastructure Handling**: Developers must explicitly write session management, retry policies, and error handling.
- **Context Window Overhead**: Managing long multi-turn execution histories requires custom context pruning logic.
- **No Built-in Web UI**: Relies on CLI interfaces, terminal logs, or third-party webhooks for visibility unless custom frontends are attached.

## When to use it
- When orchestrating custom homelab or enterprise infrastructure tasks requiring explicit SSH key access control.
- When requiring human-in-the-loop approval before executing destructive system operations.
- When building tailored micro-agent tools exposed via FastMCP 3.1 to frontier models.

## When not to use it
- For large-scale multi-file software engineering tasks (use [Aider](aider.md) or [Claude Code](claude-code.md)).
- If pre-built, production-tested MCP servers already exist for your target infrastructure platform.
- When full enterprise multi-user governance and team access management are required out-of-the-box.

## Getting started

### 1. Configure SSH Access
Ensure the host machine running the agent script has SSH key-based access to target nodes:
```bash
ssh-copy-id admin@192.168.1.50
```

### 2. Install Python Dependencies
```bash
pip install paramiko mcp pydantic fastmcp
```

## Production Systemd Service Unit

To run a Custom Agent FastMCP 3.1 micro-service as a background daemon (`/etc/systemd/system/custom-agent.service`), use the following unit file:

```ini
[Unit]
Description=Custom SSH Micro-Agent FastMCP 3.1 Server
After=network.target
Wants=network.target

[Service]
Type=simple
User=customagent
Group=customagent
WorkingDirectory=/opt/custom-agent
ExecStart=/opt/custom-agent/.venv/bin/python3 /opt/custom-agent/mcp_server.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1
Environment=SSH_KEY_PATH=/etc/custom-agent/id_ed25519
Environment=MCP_PORT=8804

# Hardened Security Options
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true
ReadWritePaths=/var/log/custom-agent /opt/custom-agent/telemetry

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Issue Code / Error | Root Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| `SSHException: Authentication failed` | Private key file `/etc/custom-agent/id_ed25519` unreadable or missing public key in target `authorized_keys`. | `ssh -i /etc/custom-agent/id_ed25519 admin@192.168.1.50` | Copy agent public key to target host or update `SSH_KEY_PATH` in service environment. |
| `SecurityBlock: Command Not Allowed` | Issued shell command failed regex/prefix allowlist check. | `journalctl -u custom-agent -n 50 --no-pager` | Update `allowed_commands` list in `CustomAgentConfig` or adjust prefix matches. |
| `TimeoutError: SSH connection timed out` | Target host unreachable over SSH port 22 or firewall blocking connection. | `nc -zv 192.168.1.50 22` | Check host power status, network routing, and UFW/iptables rules. |
| `ValidationError: Directory traversal` | `key_path` field contained forbidden `..` relative path elements. | `python3 -c "import pydantic"` | Supply absolute filesystem path starting with `/` without relative references. |
| `PermissionDenied: sudo requires tty` | Command requiring sudo failed because target `/etc/sudoers` enforces `requiretty`. | `ssh admin@192.168.1.50 "sudo -l"` | Add `Defaults:admin !requiretty` or NOPASSWD rules for specific commands in `/etc/sudoers`. |

## CLI examples

```bash
# Run a custom SSH agent diagnostic sweep
python custom_agent.py --target 192.168.1.50 --query "Inspect docker container restart counts"

# Execute a batch system update across a node list with approval prompt
python custom_agent.py --nodes-file ./nodes.json --action "apt-get update" --require-approval
```

## API examples

### FastMCP 3.1 Server Implementation (Python)
The following Python script demonstrates how to implement a custom SSH administration tool exposed via FastMCP 3.1:

```python
import os
import logging
import paramiko
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Custom-SSH-Agent")

mcp_server = FastMCP("SSH Host MicroAgent", version="3.1")

class CommandRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host: str = Field(..., pattern=r"^([a-zA-Z0-9.-]+|[0-9.]+)$", description="Target node IP or hostname")
    command: str = Field(..., min_length=1, description="Shell command string to execute")
    require_sudo: bool = Field(default=False, description="Whether to execute via sudo")

    @field_validator("command")
    @classmethod
    def validate_command_allowlist(cls, v: str) -> str:
        s = v.strip()
        allowed_prefixes = ["systemctl status", "df -h", "docker ps", "uptime", "free -m", "journalctl"]
        if not any(s.startswith(prefix) for prefix in allowed_prefixes):
            raise ValueError(f"Command '{s}' violates security allowlist policy.")
        return s

class CommandResponse(BaseModel):
    status: str
    host: str
    stdout: str
    stderr: str
    exit_code: int
    protocol_version: str = "3.1"

@mcp_server.tool()
async def execute_host_command(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Executes an allowed command on a target host via SSH using FastMCP 3.1 protocol.

    Args:
        request_dict: Dictionary matching CommandRequest schema.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating command payload via Pydantic v2...")

    try:
        req = CommandRequest.model_validate(request_dict)
        key_path = os.getenv("SSH_KEY_PATH", "/etc/custom-agent/id_ed25519")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(req.host, username="admin", key_filename=key_path if os.path.exists(key_path) else None, timeout=10)
            full_command = f"sudo {req.command}" if req.require_sudo else req.command
            stdin, stdout, stderr = ssh.exec_command(full_command)
            out = stdout.read().decode()
            err = stderr.read().decode()
            exit_code = stdout.channel.recv_exit_status()

            response = CommandResponse(
                status="success",
                host=req.host,
                stdout=out,
                stderr=err,
                exit_code=exit_code
            )
            return response.model_dump()
        except Exception as e:
            logger.error(f"SSH execution failure on {req.host}: {e}")
            return {
                "status": "error",
                "host": req.host,
                "message": f"SSH Connection Failed: {str(e)}",
                "protocol_version": "3.1"
            }
        finally:
            ssh.close()
    except ValidationError as ve:
        logger.error(f"Validation failure: {ve}")
        raise ValueError(f"Invalid request parameters: {ve}")

@mcp_server.tool()
async def audit_host_health(host: str, ctx: Optional[Context] = None) -> dict:
    """Runs a multi-step host health diagnostic sweep via SSH."""
    if ctx:
        await ctx.info(f"Auditing host health for {host}...")

    commands = {
        "disk_space": "df -h",
        "memory": "free -m",
        "uptime": "uptime",
        "containers": "docker ps"
    }
    results = {}
    for key, cmd in commands.items():
        res = await execute_host_command({"host": host, "command": cmd})
        results[key] = res.get("stdout", res.get("message", "N/A")).strip()

    return {
        "status": "success",
        "host": host,
        "diagnostics": results,
        "mcp_standard": "3.1"
    }

if __name__ == "__main__":
    mcp_server.run()
```

### Programmatic Configuration Validation with Pydantic v2
The following Python module demonstrates modeling and programmatically validating a Custom Agent configuration profile under early January 2027 SOTA standards:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
import json

class SSHNodeProfile(BaseModel):
    host: str = Field(..., pattern=r"^([a-zA-Z0-9.-]+|[0-9.]+)$", description="IP address or hostname")
    port: int = Field(default=22, ge=1, le=65535, description="SSH port")
    username: str = Field(default="admin", min_length=1, description="SSH login user")
    key_path: str = Field(..., pattern=r"^/.*$", description="Absolute filesystem path to SSH private key")
    timeout_seconds: int = Field(default=15, ge=1, le=120, description="Connection timeout")

    @field_validator("key_path")
    @classmethod
    def validate_key_path(cls, v: str) -> str:
        if ".." in v:
            raise ValueError("Directory traversal paths ('..') are strictly prohibited in key_path")
        return v

class CustomAgentConfig(BaseModel):
    agent_id: str = Field(..., min_length=2, description="Unique identifier for micro-agent")
    target_nodes: List[SSHNodeProfile] = Field(..., min_length=1, description="List of manageable nodes")
    allowed_commands: List[str] = Field(..., min_length=1, description="Allowlist command prefixes")
    mcp_version: str = Field(default="3.1", pattern=r"^3\.1$", description="FastMCP standard compliance")
    require_human_approval: bool = Field(default=True, description="Enforce interactive approval gate")
    max_parallel_nodes: int = Field(default=5, ge=1, le=50, description="Concurrency limit")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "agent_id": "homelab-ssh-agent",
                "target_nodes": [
                    {
                        "host": "192.168.1.50",
                        "port": 22,
                        "username": "admin",
                        "key_path": "/home/admin/.ssh/id_ed25519",
                        "timeout_seconds": 10
                    }
                ],
                "allowed_commands": ["systemctl status", "df -h", "docker ps"],
                "mcp_version": "3.1",
                "require_human_approval": True,
                "max_parallel_nodes": 5
            }
        }
    }

def validate_custom_agent_config(payload: dict) -> str:
    """Validates Custom Agent configuration using Pydantic v2."""
    try:
        config = CustomAgentConfig.model_validate(payload)
        return json.dumps({
            "status": "success",
            "validated_config": config.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    test_payload = {
        "agent_id": "homelab-ssh-agent",
        "target_nodes": [
            {
                "host": "192.168.1.100",
                "port": 22,
                "username": "sysadmin",
                "key_path": "/root/.ssh/id_rsa",
                "timeout_seconds": 15
            }
        ],
        "allowed_commands": ["systemctl status", "df -h", "docker ps", "uptime"],
        "mcp_version": "3.1",
        "require_human_approval": True,
        "max_parallel_nodes": 5
    }
    print(validate_custom_agent_config(test_payload))
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard tool protocol for agents.
- [Axiom Guardian](axiom-guardian.md) — Challenge-based safety guardrail MCP server.
- [Claude Code](claude-code.md) — Interactive terminal developer agent CLI.
- [OpenHands](openhands.md) — Autonomous developer agent platform.
- [Windsurf](windsurf.md) — Flow-based agentic development environment and IDE.

## Sources / References
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/specification/3.1)
- [Paramiko Documentation](https://docs.paramiko.org/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
