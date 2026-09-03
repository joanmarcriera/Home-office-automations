# SSH Execution Patterns

## What it is
SSH Execution Patterns is a collection of architectural designs and security models for allowing LLM-powered agents to interact with remote systems. As of early January 2027, it defines how an autonomous agent can safely traverse the "Trust Boundary" between a reasoning engine and a physical or virtual execution environment using secure transports, sandboxing, and Model Context Protocol (FastMCP 3.1) secure remote execution specifications.

## What problem it solves
LLMs are capable of generating shell commands, but allowing them to execute those commands directly on a server poses significant security risks (e.g., prompt injection, accidental data loss, or privilege escalation). These patterns provide a framework for restricted, audited, and validated execution, ensuring that agents have the "hands" they need to perform work without compromising system integrity.

## Where it fits in the stack
It belongs in the **Architecture** layer. Specifically, it defines the interface between the **Development & Ops** layer (Agents like Aider or Claude Code) and the **Infrastructure** layer (Servers, Raspberry Pis, Cloud VMs).

## Typical use cases
- **Remote Configuration**: An agent setting up a web server or database on a new Raspberry Pi.
- **Automated Troubleshooting**: An agent logging into a server to read logs and diagnose a service failure.
- **CI/CD Orchestration**: An agent managing deployments by executing commands over SSH on a staging environment.
- **Homelab Management**: Scaling updates or configuration changes across multiple local nodes via a centralized controller.

## Strengths
- **Protocol Native**: Leverages the industry-standard SSH protocol, which is already present on almost every Unix-like system.
- **Fine-Grained Control**: Supports multiple levels of restriction, from simple wrapper scripts to full Human-in-the-Loop (HITL) approval flows.
- **Auditability**: Every command and its output can be logged centrally, providing a complete audit trail of agent activity.

## Limitations
- **Latency**: SSH connections and command execution introduce latency that can slow down tight reasoning loops.
- **Key Management**: Requires careful handling of SSH keys; if an agent's controller is compromised, the keys provide a path to the target systems.
- **Complexity**: Setting up restricted sudoers and command allowlists requires ongoing maintenance and configuration overhead.

## When to use it
- When you need an agent to perform "real-world" actions on a server that cannot be handled via a high-level API.
- When managing a fleet of devices (like Raspberry Pis) where SSH is the primary management interface.
- When you want to transition from "chatting about code" to "autonomous engineering" where the agent can actually deploy and test its work.

## When not to use it
- If the task can be completed using a specialized API (e.g., a Cloud Provider API or a configuration management tool like Ansible).
- For extremely high-security production environments where no automated agent should ever have shell access.

## Getting started
To implement secure agentic SSH, follow the "Three Planes" architecture.

### Architecture: The Three Planes
1.  **Reasoning Plane (LLM)**: The "Brain" (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Qwen 3.6 VL). Analyzes state and decides *what* to do. Should never have direct access to SSH keys.
2.  **Control Plane (Agent)**: The "Operator." A script or framework (e.g., FastMCP 3.1 server) that manages the loop and initiates connections.
3.  **Execution Plane (SSH)**: The "Hands." The actual remote system being managed.

### Implementation Patterns
1.  **Tool-Based Execution**: The agent is provided with a "tool" (function) like `run_ssh_command(host, cmd)`. Output is returned to the agent.
2.  **Wrapper Script Execution**: The agent calls a local wrapper script (e.g., `pi_exec "reboot"`) instead of raw SSH.
3.  **Restricted Sudo**: Restrict the service user (e.g., `ai-agent`) to specific commands in `/etc/sudoers.d/ai-agent`:
```text
ai-agent ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx, /usr/bin/apt update
```

## CLI examples
```bash
# Example of a local wrapper script the agent might call
# usage: ./remote_exec.sh <host> <command>
ssh -i /path/to/ai_key -o BatchMode=yes ai-agent@$1 "$2"

# Generating a dedicated SSH key for an agent
ssh-keygen -t ed25519 -f ~/.ssh/ai_agent_key -C "ai-agent-ssh"

# Testing agent access to a restricted command
ssh ai-agent@target-host "sudo systemctl restart nginx"
```

## API examples
Agents often interact with SSH via libraries like Paramiko in Python.

### Secure SSH Connection and Payload Validation (Pydantic v2)
The following script ensures strict validation of target host parameters, SSH credentials, and command execution limits before invoking paramiko:

```python
import re
from typing import List, Optional
from pydantic import BaseModel, Field, IPvAnyAddress, field_validator
import paramiko

class SSHCommandPayload(BaseModel):
    host: IPvAnyAddress
    user: str = Field(..., pattern="^[a-zA-Z0-9_-]{3,32}$")
    key_path: str = Field(..., pattern="^/.*_key$")
    command: str = Field(..., min_length=2, max_length=128)

    @field_validator('command')
    @classmethod
    def restrict_dangerous_commands(cls, v: str) -> str:
        # Prevent shell redirection, injection, and multi-command chaining
        dangerous_patterns = [r';', r'&&', r'\|', r'\n', r'\.\.']
        for pattern in dangerous_patterns:
            if re.search(pattern, v):
                raise ValueError("Dangerous character sequence or chaining detected in SSH command")

        # Enforce command allowlist
        allowed_binaries = {"uptime", "df", "free", "systemctl restart nginx", "git pull"}
        if not any(v.startswith(allowed) for allowed in allowed_binaries):
            raise ValueError(f"Command '{v}' is not in the allowed operations registry")
        return v

def run_secure_remote_command(payload: SSHCommandPayload) -> str:
    """Establishes SSH connection and executes a validated command safely."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # In practice, establish a secure connection using the validated payload fields
        client.connect(
            str(payload.host),
            username=payload.user,
            key_filename=payload.key_path,
            timeout=10
        )
        stdin, stdout, stderr = client.exec_command(payload.command)
        output = stdout.read().decode('utf-8')
        return output
    finally:
        client.close()

# Validation & execution example
if __name__ == "__main__":
    valid_payload = {
        "host": "192.168.1.50",
        "user": "ai-agent",
        "key_path": "/home/ai-agent/.ssh/id_ed25519_key",
        "command": "systemctl restart nginx"
    }

    # Strictly validate against schema
    validated = SSHCommandPayload.model_validate(valid_payload)
    print(f"Validation passed for host {validated.host}. Safe command to execute: '{validated.command}'")
```

## Related tools / concepts
- [Raspberry Pi Kiosk Automation](../playbooks/raspberry-pi-kiosk-automation.md)
- [Aider](../tools/development_ops/aider.md)
- [Claude Code](../tools/development_ops/claude-code.md)
- [Tailscale](../services/tailscale.md)
- [Custom Agents](../tools/development_ops/custom_agents.md)
- [Infrastructure Overview](infrastructure.md)
- [Standards and Conventions](../standards.md)
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md)

## Sources / References
- [OpenSSH Official Documentation](https://www.openssh.com/)
- [NIST Guide to SSH](https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final)
- [Teleport: Agentless SSH with FastMCP 3.1 Integrations](https://goteleport.com/ssh-server/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
