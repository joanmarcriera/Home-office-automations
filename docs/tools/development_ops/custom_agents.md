# Custom Agents (SSH + LLM Loop)

## What it is
A **Custom Agent** is a lightweight Python script or visual workflow automation (e.g., n8n) that implements a basic autonomous control loop: Prompt LLM -> Receive Command -> Execute via SSH/Shell -> Return Output/Telemetry to LLM. Under late November/December 2026 SOTA standards, these agents have evolved from raw command-execution scripts to sophisticated, standard-compliant "Micro-Agents" that natively support **Model Context Protocol (MCP 3.1 / FastMCP 3.1)**, allowing them to be plugged directly into modern frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, **Llama 4**, **Gemma 3**, and **Qwen 3.6** as highly secure system administration tools.

## What problem it solves
Provides a tailored, minimal orchestration layer for specific infrastructure tasks without the overhead or complexity of massive agent platforms. It allows for precise control over the security, execution plane, and sandbox boundaries, specifically addressing the "Reasoning vs. Execution" gap in local homelab management while leveraging modern **secure SSH tunneling** and asymmetric keys to safely access private systems.

## Where it fits in the stack
**Agent / Orchestration Layer**. It is the minimal control logic that coordinates the LLM (Reasoning) and the target machine (Execution via SSH). It acts as a bridge between high-level intent and low-level system commands, often serving as a custom MCP server for infrastructure-specific toolsets.

## Typical use cases
- **Server Maintenance**: "Check disk space on all nodes and clear Docker build caches if above 90%."
- **Configuration Updates**: "Update the Nginx proxy settings and perform a graceful service reload."
- **Edge Diagnostics**: "Analyze why the local k3s node on the Raspberry Pi is in a NotReady state."
- **Automated Patching**: Rolling security updates across a cluster with active health checks and automated rollback.
- **Secure Remote Access**: Managing internal resources over an encrypted SSH tunnel without exposing raw ports to the public internet.

## Strengths
- **Simplicity**: Extremely easy to understand, inspect, and modify without complex third-party framework overhead.
- **Security**: You control exactly which commands are allowed, how SSH sessions are handled, and can enforce strict key-based authentication.
- **Portability**: Runs as a lightweight script anywhere, including within n8n or inside a minimal container.
- **Transparency**: Every step of the reasoning and command execution loop is visible and easily logged for auditing.
- **MCP 3.1 / FastMCP 3.1 Ready**: Standardized schema allows the custom agent to be discovered and invoked by any MCP-compliant LLM client.

## Limitations
- **Manual Work**: Requires writing and maintaining the controller script, SSH session pools, and error handling.
- **Context Management**: Needs manual handling of chat history and state (unlike Aider or OpenHands).
- **Tooling**: Lacks advanced "repo mapping" or terminal-emulation features found in larger developer agent suites.
- **Scaling**: Managing dozens of separate custom agents can become complex without a centralized supervisor.

## When to use it
- For specific, repetitive infrastructure tasks where full agent framework overhead is unnecessary.
- When you require a high degree of security, VPC isolation, and explicit human-in-the-loop approval.
- For lightweight automation on resource-constrained edge hardware (e.g., Raspberry Pi Zero).
- When you need to bridge an LLM to a legacy system that only supports SSH interactions.

## When not to use it
- For general software engineering or coding tasks (use [Aider](./aider.md) or [OpenHands](./openhands.md)).
- When the task requires complex reasoning across hundreds of source files or deep codebase understanding.
- If a standardized, pre-built MCP server for the target service already exists.

## Getting started
To build a custom agent, you need a runtime environment (Python 3.11+ recommended) and SSH access to your target machines.

### 1. Set up SSH Keys
Ensure your agent machine has passwordless SSH access to the target.
```bash
ssh-copy-id admin@192.168.1.10
```

### 2. Install Dependencies
```bash
pip install paramiko openai mcp==3.1.0
```

### 3. Configure MCP 3.1
Define your tool schema so frontier models can discover your agent's capabilities.

## CLI examples
Custom agents are often invoked via a CLI controller.

### Basic Diagnostic Run
```bash
# Run a one-off diagnostic on the home server
python custom_agent.py --target 192.168.1.10 --query "Check docker service health"
```

### Batch Update
```bash
# Run an automated update across all nodes in a cluster
python custom_agent.py --cluster k3s-home --action "apt update && apt upgrade -y" --require-approval
```

### SSH Tunnel Setup
```bash
# Establish a secure tunnel before running agent logic
ssh -L 8080:localhost:8080 admin@remote-server -N &
python custom_agent.py --query "Inspect local web service on 8080"
```

## API examples

### MCP 3.1 Server Implementation (Python FastMCP)
This example shows how to expose a custom SSH agent as an MCP 3.1 tool using FastMCP:

```python
import mcp.server.fastmcp as fastmcp
import paramiko

# Initialize FastMCP Server under MCP 3.1 specification
mcp_server = fastmcp.FastMCP("SSH Custom Agent")

@mcp_server.tool()
def execute_ssh_command(host: str, command: str) -> str:
    """Executes a command on a remote host via SSH and returns stdout."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username='admin', timeout=10)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        return output if output else f"Error: {error}"
    except Exception as e:
        return f"SSH Connection Failed: {str(e)}"
    finally:
        ssh.close()

if __name__ == "__main__":
    # Start stdio transport
    mcp_server.run()
```

### Python Agent Loop with OpenAI tool-calling
```python
import paramiko
from openai import OpenAI

def secure_agent_loop(query):
    # Setup OpenAI client and paramiko SSH connection
    client = OpenAI()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('internal.homelab', username='agent_user')

    # LLM Interaction with custom tools using GPT-5.5
    response = client.chat.completions.create(
        model="gpt-5.5-preview",
        messages=[{"role": "user", "content": query}],
        tools=[{
            "type": "function",
            "function": {
                "name": "exec_ssh",
                "description": "Run shell command on internal node",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"}
                    },
                    "required": ["command"]
                }
            }
        }]
    )

    # Process tool call and return response
    return response.choices[0].message
```

### Robust Configuration and SSH Profile Validation with Pydantic v2
The following Python script illustrates how to model and programmatically validate Custom Agent parameters, SSH connection profiles, and command allowlists under late November/December 2026 standards, ensuring strict schema safety and type correctness using Pydantic v2:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
import json

class SSHConnectionConfig(BaseModel):
    host: str = Field(..., pattern=r"^([a-zA-Z0-9.-]+|[0-9.]+)$")
    port: int = Field(default=22, ge=1, le=65535)
    username: str = Field(default="admin", min_length=1)
    key_path: str = Field(..., pattern=r"^/.*$")
    timeout_seconds: int = Field(default=15, ge=1, le=120)

class CustomAgentConfig(BaseModel):
    agent_name: str = Field(..., min_length=2)
    ssh_connections: List[SSHConnectionConfig] = Field(default_factory=list)
    allowed_commands: List[str] = Field(..., min_length=1)
    mcp_version: str = Field(default="3.1", pattern=r"^3\.1$")
    requires_approval: bool = Field(default=True)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "agent_name": "homelab-ssh-microagent",
                "ssh_connections": [
                    {
                        "host": "192.168.1.10",
                        "port": 22,
                        "username": "homelab-admin",
                        "key_path": "/home/admin/.ssh/id_ed25519",
                        "timeout_seconds": 10
                    }
                ],
                "allowed_commands": ["docker restart", "systemctl status", "df -h"],
                "mcp_version": "3.1",
                "requires_approval": True
            }
        }
    }

def validate_custom_agent_config(payload: dict) -> str:
    """Validates Custom Agent configurations and tool definitions using Pydantic v2."""
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
        "agent_name": "homelab-ssh-microagent",
        "ssh_connections": [
            {
                "host": "192.168.1.100",
                "port": 22,
                "username": "admin",
                "key_path": "/root/.ssh/id_rsa",
                "timeout_seconds": 5
            }
        ],
        "allowed_commands": ["docker ps", "docker stop", "docker start"],
        "mcp_version": "3.1",
        "requires_approval": True
    }
    print(validate_custom_agent_config(test_payload))
```

## Related tools / concepts
- [SSH Execution Patterns](../../architecture/ssh_execution_patterns.md) — Architectural deep dive into homelab SSH executions.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — The universal standard for agent tool-use.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — High-level multi-agent orchestration patterns.
- [Raspberry Pi Kiosk Automation](../../playbooks/raspberry-pi-kiosk-automation.md) — Real-world application of custom edge automation.
- [n8n Error Handling](../../knowledge_base/patterns/n8n-error-handling.md) — Managing failures in visual agent workflows.
- [Claude Code](./claude-code.md) — Anthropic's interactive developer agent CLI.
- [OpenHands](./openhands.md) — Full-featured autonomous agent platform.
- [Aider](./aider.md) — Terminal-based Git-integrated collaborative coding.
- [Terminus 2](./terminus-2.md) — Terminal-native tmux bridging AI agent and baseline.
- [Anti-Gravity](./anti_gravity.md) — Google's enterprise agent orchestration and sandbox framework.
- [Droid](./droid.md) — Autonomous task automation and execution agent.
- [Sourcegraph Cody](./sourcegraph_cody.md) — Multi-repository reasoning and context retrieval platform.
- [Codeium](./codeium.md) — AI-powered IDE developer productivity platform.
- [Windsurf](./windsurf.md) — Flow-based agentic development environment and IDE.

## Sources / references
- [Paramiko Documentation](https://docs.paramiko.org/)
- [SSH Agent Loop Patterns (GitHub)](https://github.com/joanmarcriera/Home-office-automations)
- [Model Context Protocol (MCP 3.1) Specification](https://modelcontextprotocol.io/introduction)
- [LLM Tool Calling Best Practices (Anthropic)](https://docs.anthropic.com/claude/docs/tool-use)

## Contribution Metadata
- Last reviewed: 2026-12-17
- Confidence: high
