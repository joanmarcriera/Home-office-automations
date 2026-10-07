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
pip install paramiko mcp pydantic
```

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
import mcp.server.fastmcp as fastmcp
import paramiko
from typing import Optional, Dict, Any

mcp_server = fastmcp.FastMCP("SSH Host MicroAgent", version="3.1")

@mcp_server.tool()
def execute_host_command(host: str, command: str, require_sudo: bool = False) -> Dict[str, Any]:
    """Executes an allowed command on a target host via SSH using FastMCP 3.1 protocol."""
    allowed_prefixes = ["systemctl status", "df -h", "docker ps", "uptime", "free -m", "journalctl"]
    if not any(command.startswith(prefix) for prefix in allowed_prefixes):
        return {
            "status": "error",
            "message": f"Command '{command}' is not in the allowed command list.",
            "protocol_version": "3.1"
        }

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username='admin', timeout=10)
        full_command = f"sudo {command}" if require_sudo else command
        stdin, stdout, stderr = ssh.exec_command(full_command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        return {
            "status": "success",
            "host": host,
            "stdout": out,
            "stderr": err,
            "exit_code": stdout.channel.recv_exit_status(),
            "protocol_version": "3.1"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"SSH Connection Failed: {str(e)}",
            "protocol_version": "3.1"
        }
    finally:
        ssh.close()

@mcp_server.tool()
def audit_host_health(host: str) -> Dict[str, Any]:
    """Runs a multi-step host health diagnostic sweep via SSH."""
    commands = {
        "disk_space": "df -h /",
        "memory": "free -m",
        "uptime": "uptime",
        "containers": "docker ps --format '{{.Names}}\t{{.Status}}'"
    }
    results = {}
    for key, cmd in commands.items():
        res = execute_host_command(host, cmd)
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
- Last reviewed: 2026-10-07
- Confidence: high
