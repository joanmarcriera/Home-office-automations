# SSH Execution Patterns

## Overview
In a modern AI-automated infrastructure, SSH serves as the primary **execution plane**. This page documents the patterns and security models for allowing LLM-powered agents to interact with remote systems safely.

## Architecture: The Three Planes
A robust automation stack separates concerns into three distinct layers:

1.  **Reasoning Plane (LLM)**: The "Brain." It analyzes the current state and decides *what* needs to be done. It should never have direct access to SSH keys or credentials.
2.  **Control Plane (Agent)**: The "Operator." A script or framework (Aider, OpenHands, Custom Python) that manages the loop, handles the LLM interaction, and initiates connections.
3.  **Execution Plane (SSH)**: The "Hands." The actual remote system being managed. Access is strictly controlled and audited.

## Execution Patterns

### 1. Tool-Based Execution
The agent is provided with a "tool" (function) like `run_ssh_command(host, cmd)`.
- **Workflow**: Agent sends command to controller -> Controller executes via SSH library (e.g., Paramiko, Fabric) -> Output is returned to the agent.
- **Best for**: Dynamic, multi-step troubleshooting and complex configuration.

### 2. Wrapper Script Execution
The agent calls a local wrapper script (e.g., `pi_exec "reboot"`) instead of raw SSH.
- **Workflow**: Agent executes a local command -> Local script handles SSH connection, logging, and pre-command validation.
- **Best for**: Restricting agents to a predefined set of safe operations.

### 3. Human-in-the-Loop (HITL)
Every command proposed by the LLM must be approved by a human before execution.
- **Workflow**: Agent proposes: `rm -rf /var/log/*` -> Controller waits for user input -> User approves/denies -> Loop continues.
- **Best for**: High-stakes production changes and learning phases.

## Security Model

### Dedicated Users
Never use the `root` user for AI-driven SSH. Create a dedicated service user (e.g., `ai-agent`) with the minimal set of permissions required for its task.

### Restricted Sudoers
If the agent needs root privileges, use `/etc/sudoers.d/ai-agent` to restrict it to specific commands:
```text
ai-agent ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx, /usr/bin/apt update
```

### Command Allowlists
Implement a validation layer in your custom agent that checks proposed commands against a regex allowlist before they ever reach the SSH layer.

### Why You NEVER Give SSH Keys to LLM Providers
Directly giving an SSH key to a cloud-based LLM provider (via a "plugin" or "action") creates a massive security hole. If the provider is compromised, or if a prompt injection attack occurs, the attacker has a direct path into your private infrastructure. **Always keep the keys in your local Control Plane.**

## Threat Model

| Threat | Impact | Mitigation |
| :--- | :--- | :--- |
| **Prompt Injection** | Attacker tricks LLM into running malicious commands (e.g. `rm -rf /`). | Human-in-the-loop, command allowlists, restricted sudo. |
| **Hallucination** | LLM invents a non-existent or destructive command. | Syntax validation, dry-run modes, standard error handling. |
| **API Compromise** | LLM provider API key is stolen. | The attacker can use your credits, but cannot access your servers because they don't have your SSH keys. |
| **Controller Compromise**| The machine running the agent is hacked. | Standard host hardening; the keys are here, so this is your most sensitive point. |

## Logging and Auditing
- **Local Logs**: Capture every command sent and the full output in the agent's log.
- **Remote Syslog**: Use `auditd` or standard syslog on the target machine to record all activity by the `ai-agent` user.

## Links to related pages
- [Custom Agents](../tools/development_ops/custom_agents.md)
- [Raspberry Pi Kiosk Automation](../playbooks/raspberry-pi-kiosk-automation.md)
- [Standards and Conventions](../standards.md)
