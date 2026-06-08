# SSH Execution Patterns

## What it is
SSH Execution Patterns is a collection of architectural designs and security models for allowing LLM-powered agents to interact with remote systems. It defines how an autonomous agent can safely traverse the "Trust Boundary" between a reasoning engine and a physical or virtual execution environment.

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

### Pre-requisites
- A target machine with an SSH server enabled.
- A dedicated service user (e.g., `ai-agent`) on the target machine.
- An agent framework (like [Aider](../tools/development_ops/aider.md) or [Claude Code](../tools/development_ops/claude-code.md)) capable of executing local commands that wrap SSH.
- Support for [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) for standardized tool-calling.

### Architecture: The Three Planes
A robust automation stack separates concerns into three distinct layers:

1.  **Reasoning Plane (LLM)**: The "Brain." Models like [Claude 4.7](../tools/ai_knowledge/claude.md), [GPT-5.5](../tools/ai_knowledge/openai.md), or [Llama 4 Maverick](../tools/ai_knowledge/meta_llama.md) analyze the current state and decide *what* needs to be done. It should never have direct access to SSH keys or credentials.
2.  **Control Plane (Agent)**: The "Operator." A script or framework (e.g., [MCP](../tools/automation_orchestration/mcp.md) server) that manages the loop, handles the LLM interaction, and initiates connections.
3.  **Execution Plane (SSH)**: The "Hands." The actual remote system being managed. Access is strictly controlled and audited.

### Implementation Patterns

#### 1. Tool-Based Execution
The agent is provided with a "tool" (function) like `run_ssh_command(host, cmd)`.
- **Workflow**: Agent sends command to controller -> Controller executes via SSH library (e.g., Paramiko, Fabric) -> Output is returned to the agent.

#### 2. Wrapper Script Execution
The agent calls a local wrapper script (e.g., `pi_exec "reboot"`) instead of raw SSH.
- **Workflow**: Agent executes a local command -> Local script handles SSH connection and pre-command validation.

#### 3. Restricted Sudo Example
If the agent needs root privileges, use `/etc/sudoers.d/ai-agent` to restrict it to specific commands:
```text
ai-agent ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx, /usr/bin/apt update
```

## Related tools / concepts
- [Raspberry Pi Kiosk Automation](../playbooks/raspberry-pi-kiosk-automation.md) — A primary application of these SSH patterns.
- [Aider](../tools/development_ops/aider.md) — A tool that implements many of these patterns for remote repository editing.
- [Claude Code](../tools/development_ops/claude-code.md) — An agent that uses terminal access to interact with systems.
- [Tailscale](../services/tailscale.md) — Often used to provide the secure network layer for SSH connections.
- [Custom Agents](../tools/development_ops/custom_agents.md) — For building controllers that implement custom validation logic.
- [LLM Trust Boundaries](../knowledge_base/patterns/llm-trust-boundaries.md) — The theoretical framework for the security model used here.
- [Infrastructure Overview](infrastructure.md) — Where these servers live in the homelab.
- [Standards and Conventions](../standards.md) — The general rules governing documentation and implementation in this repo.

## Sources / References
- [OpenSSH Official Documentation](https://www.openssh.com/)
- [NIST Guide to SSH](https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high
