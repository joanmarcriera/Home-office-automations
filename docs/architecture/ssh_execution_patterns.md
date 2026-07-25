# SSH Execution Patterns

## What it is
SSH Execution Patterns is a collection of architectural designs and security models for allowing LLM-powered agents to interact with remote systems. As of late August 2026, it defines how an autonomous agent can safely traverse the "Trust Boundary" between a reasoning engine and a physical or virtual execution environment using secure transports, sandboxing, and Model Context Protocol (MCP 3.1) secure remote execution specifications.

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
1.  **Reasoning Plane (LLM)**: The "Brain" (Claude 5.1, GPT-5.5, Llama 4). Analyzes state and decides *what* to do. Should never have direct access to SSH keys.
2.  **Control Plane (Agent)**: The "Operator." A script or framework (e.g., MCP 3.1 server) that manages the loop and initiates connections.
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

```python
import paramiko

# Example: Running a command on a remote host via SSH
def run_remote_command(host, user, key_path, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, key_filename=key_path)

    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode('utf-8')
    client.close()
    return output

# print(run_remote_command("192.168.1.50", "ai-agent", "/path/to/key", "uptime"))
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
- [Teleport: Agentless SSH with MCP 3.1 Integrations](https://goteleport.com/ssh-server/)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
