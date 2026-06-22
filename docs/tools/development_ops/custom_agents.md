# Custom Agents (SSH + LLM Loop)

## What it is
A "Custom Agent" is a lightweight Python script or automation (e.g., n8n) that implements a basic loop: Prompt LLM -> Receive Command -> Execute via SSH -> Return Output to LLM. As of June 2026, these agents have evolved from simple scripts to sophisticated "Micro-Agents" that natively support **Model Context Protocol (MCP 3.0)**, allowing them to be plugged directly into frontier models like Claude 4.8 Opus and GPT-5.5 as specialized system administration tools.

## What problem it solves
Provides a tailored, minimal orchestration layer for specific infrastructure tasks without the overhead or complexity of full agent platforms. It allows for precise control over the security and execution plane, specifically addressing the "Reasoning vs. Execution" gap in local homelab management while leveraging modern **secure SSH tunneling** patterns to bypass complex firewall configurations.

## Where it fits in the stack
**Agent / Orchestration Layer**. It is the logic that coordinates the LLM (Reasoning) and the target machine (Execution via SSH). It acts as a bridge between high-level intent and low-level system commands, often serving as a custom MCP server for infrastructure-specific toolsets.

## Typical use cases
- **Server Maintenance**: "Check disk space on all nodes and clear logs if above 90%."
- **Configuration Updates**: "Update the nginx config on the proxy server and reload the service."
- **Diagnostics**: "Analyze why the service on the Raspberry Pi is failing to start."
- **Automated Patching**: Rolling updates across a k3s cluster with health checks.
- **Secure Remote Access**: Managing internal services over an encrypted SSH tunnel without exposing ports to the public internet.

## Strengths
- **Simplicity**: Easy to understand and modify without specialized agent frameworks.
- **Security**: You control exactly which commands are allowed and how SSH is handled, using modern key-based authentication.
- **Portability**: Can run as a small script anywhere, including within n8n or as a standalone container.
- **Transparency**: Every step of the loop is visible and can be logged easily for auditing.
- **MCP 3.0 Ready**: Can be easily exposed as a standardized tool for any MCP-compliant LLM client.

## Limitations
- **Manual Work**: Requires writing and maintaining the controller script and error handling.
- **Context Management**: Needs manual handling of history and state (unlike Aider or OpenHands).
- **Tooling**: Lacks the advanced "repo map" or "browser" tools of larger frameworks.
- **Scaling**: Managing dozens of custom agents can become complex without a centralized supervisor.

## When to use it
- For specific, repetitive infrastructure tasks where full agent framework overhead is not desired.
- When you need a high degree of security and explicit human-in-the-loop approval.
- For lightweight automation on resource-constrained devices (e.g., Raspberry Pi Zero).
- When you need to bridge an LLM to a legacy system that only supports SSH.

## When not to use it
- For general software engineering or coding tasks (use [Aider](aider.md) or [OpenHands](openhands.md)).
- When the task requires complex reasoning across hundreds of files or repo-wide understanding.
- If a standardized MCP server for the target service already exists.

## Getting started
To build a custom agent, you need a runtime environment (Python 3.11+ recommended) and SSH access to your target machines.

1. **Set up SSH Keys**: Ensure your agent machine has passwordless SSH access to the target.
   ```bash
   ssh-copy-id admin@192.168.1.10
   ```
2. **Install Dependencies**:
   ```bash
   pip install paramiko openai mcp
   ```
3. **Configure MCP 3.0**: Define your tool schema so frontier models can discover your agent's capabilities.

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
### MCP 3.0 Server Implementation (Python)
This example shows how to expose a custom SSH agent as an MCP 3.0 tool.

```python
from mcp.server import Server
import paramiko

server = Server("ssh-custom-agent")

@server.tool()
def run_command(host: str, command: str):
    """Executes a command on a remote host via SSH."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='admin')
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode()

if __name__ == "__main__":
    server.run()
```

### Python Agent Loop with Secure Tunneling
```python
import paramiko
from openai import OpenAI

def secure_agent_loop(query):
    # Setup SSH connection with specific security params
    client = OpenAI()
    ssh = paramiko.SSHClient()
    ssh.connect('internal.homelab', port=22, username='agent_user')

    # LLM Interaction
    response = client.chat.completions.create(
        model="gpt-5.5-preview",
        messages=[{"role": "user", "content": query}],
        tools=[{ "type": "function", "function": { "name": "exec_ssh", "parameters": { ... } } }]
    )
    # ... handle execution and return ...
```

## Related tools / concepts
- [SSH Execution Patterns](../../architecture/ssh_execution_patterns.md) — Architectural deep dive.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — The standard for agent tool-use.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — High-level orchestration patterns.
- [Raspberry Pi Kiosk Automation](../../playbooks/raspberry-pi-kiosk-automation.md) — Real-world application.
- [n8n Error Handling](../../knowledge_base/patterns/n8n-error-handling.md) — Managing failures in visual agents.
- [Claude Code](claude-code.md) — Interactive terminal coding agent.
- [OpenHands](openhands.md) — Full-featured autonomous agent platform.
- [Aider](aider.md) — Terminal-based pair programming.

## Sources / references
- [Paramiko Documentation](https://docs.paramiko.org/)
- [SSH Agent Loop Patterns (GitHub)](https://github.com/joanmarcriera/Home-office-automations)
- [Model Context Protocol (MCP 3.0) Specification](https://modelcontextprotocol.io/introduction)
- [LLM Tool Calling Best Practices (Anthropic)](https://docs.anthropic.com/claude/docs/tool-use)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
