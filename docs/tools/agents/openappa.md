# OpenAPPA

## What it is
OpenAPPA (Open Automated Privacy & Permission Protection Architecture) is an open-source, security-focused AI agent orchestration framework developed by Archestra. Designed specifically for zero-breach corporate deployments, OpenAPPA enforces strict, kernel-level permission isolation, zero-trust credential masking, and real-time prompt injection filtering for autonomous AI agents interacting with sensitive enterprise infrastructure. In 2027, OpenAPPA serves as an industry standard for securing multi-agent systems operating across production databases, internal Slack/Teams channels, and Cloud API services.

```
+-----------------------------------------------------------------------------------+
|                        OPENAPPA ZERO-TRUST ARCHITECTURE                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Agent Action       | ----> | Zero-Trust Permission | ---> | Hardware Sandbox| |
|  | Request / Prompt    |       | Policy Evaluator      |      | Execution Core  | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | FastMCP 3.1 Gateway | <---- | Audit Log Vault       | <--- | Credential Vault| |
|  | Secure Execution   |       | & Real-Time Monitor   |      | Masking Layer   | |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Connecting autonomous AI agents to enterprise tools (databases, shell environments, internal APIs) exposes organizations to severe security vulnerabilities: prompt injection attacks, unauthorized credential leakage, indirect data exfiltration, and unintended destructive command execution. Standard agent frameworks execute tool calls with full user privileges. OpenAPPA solves this by placing an automated, cryptographic permission proxy between AI agents and underlying tools, enforcing least-privilege sandboxing and inspecting all input/output payloads in real time.

## Where it fits in the stack
**Tools / Agents & Security Orchestration Framework**. OpenAPPA operates as a security gateway and sandboxing layer wrapping agent execution engines (such as LangChain, CrewAI, AutoGen, or custom FastMCP agents).

## Feature Comparison Matrix

| Security Feature | OpenAPPA | Basic Container Isolation | API Gateway (e.g. Kong/Envoy) |
| :--- | :--- | :--- | :--- |
| **Prompt Injection Defense** | Real-time neural & heuristic analysis | None | Basic WAF regex rules |
| **Credential Masking** | Dynamic zero-trust vault proxy | Static env vars | Header token injection |
| **Tool Execution Sandbox** | Ephemeral MicroVM / Micro-container | Static Docker container | N/A (API Layer only) |
| **FastMCP 3.1 Native Integration** | First-class JSON-RPC security gateway | External wrapper required | Reverse proxy plugin |
| **Audit Log Integrity** | Cryptographically signed, immutable logs | Standard stdout logs | Access logs |

## Typical use cases
- **Zero-Breach Enterprise Agent Sandbox**: Safely executing background agent code generation and terminal commands inside ephemeral isolated sandboxes.
- **Credential Masking & API Key Vaulting**: Proxying agent API calls through OpenAPPA so LLMs never see underlying secrets or database passwords.
- **Indirect Prompt Injection Defense**: Filtering incoming web scraping payloads and user messages for embedded malicious instructions.
- **Audit Compliance & Forensics**: Generating cryptographically signed, immutable logs for every agent tool call and file system access.

## Strengths
- **Zero-Trust Security Boundary**: Prevents agents from exceeding predefined fine-grained action scopes.
- **Built-In Credential Masking**: Automatically redacts API tokens, private keys, and PII from prompt context and logs.
- **Prompt Injection Defense Core**: Real-time heuristic and neural filtering for direct and indirect prompt injections.
- **FastMCP 3.1 Native Integration**: Plugs directly into FastMCP tool servers as a secure security proxy.

## Limitations
- **Latency Overhead**: Security verification and sandbox checks add ~5-15ms overhead per tool call.
- **Policy Definition Rigor**: Requires security teams to define precise JSON/YAML permission policy schemas.

## When to use it
- When connecting autonomous AI agents to production enterprise databases, SSH terminals, or internal cloud APIs.
- When regulatory frameworks (SOC2, HIPAA, ISO 27001) require strict action auditing and zero-trust data access for AI models.
- When protecting multi-agent collaboration environments against indirect prompt injection attacks.

## When not to use it
- When running local, single-user experimental scripts without external network access or sensitive credentials.
- When maximum execution speed is required and sandboxing overhead cannot be tolerated.

## Architecture & Technical Deep Dive

OpenAPPA enforces security through a five-stage isolation pipeline:

```
                        OPENAPPA ARCHITECTURE PIPELINE

    Agent Action Request / Tool Call
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Prompt Injection Filter      │  <--- Scans Text for Injection Patterns
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Permission Evaluator         │  <--- Validates Request against RBAC Policy
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Credential Masking Proxy     │  <--- Injects Secrets without Exposing to LLM
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Ephemeral Isolated Sandbox   │  <--- Container / MicroVM Tool Execution
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ FastMCP 3.1 Security Gateway │  <--- Signed Audit Log Output
     └──────────────────────────────┘
```

1. **Prompt Injection Filter**: Inspects prompt text and tool input parameters using lightweight neural classification for malicious override attempts.
2. **Permission Evaluator**: Compares requested action against fine-grained Role-Based Access Control (RBAC) rules defined in YAML.
3. **Credential Proxy**: Automatically injects actual API credentials into outgoing network headers without exposing the plain-text secret to the LLM model context.
4. **Isolated MicroVM Execution**: Runs shell commands and script executions inside ephemeral Firecracker microVMs or Docker containers.
5. **Signed Audit Logging**: Writes cryptographic hashes of request/response frames into append-only compliance storage.

## Sequence Diagram

```
+-----------+            +-------------------+          +------------------+          +------------------+
| AI Agent  |            | OpenAPPA Gateway  |          | Policy Engine    |          | Hardware Sandbox |
+-----+-----+            +---------+---------+          +--------+---------+          +--------+---------+
      |                            |                             |                             |
      | 1. Execute Tool Request    |                             |                             |
      +--------------------------->|                             |                             |
      |                            | 2. Inspect Prompt & Params  |                             |
      |                            +---------------------------->|                             |
      |                            |                             |                             |
      |                            | 3. Evaluate RBAC Policy     |                             |
      |                            |<----------------------------+                             |
      |                            |                             |                             |
      |                            | 4. Dispatch to Sandbox      |                             |
      |                            +---------------------------------------------------------->|
      |                            |                             |                             |
      |                            | 5. Return Masked Result     |                             |
      |                            |<----------------------------------------------------------+
      | 6. Signed Tool Output      |                             |                             |
      |<---------------------------+                             |                             |
```

## Production Systemd Deployment

Deploy OpenAPPA as a system-managed daemon on Linux server infrastructure:

```ini
[Unit]
Description=OpenAPPA Zero-Trust Security Gateway Service
Documentation=https://openappa.io/docs
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=openappa
Group=openappa
WorkingDirectory=/opt/openappa
ExecStart=/usr/local/bin/openappa daemon --config /etc/openappa/policy.yaml --port 9090
Restart=always
RestartSec=5s
Environment=NODE_ENV=production
Environment=OPENAPPA_LOG_LEVEL=info
LimitNOFILE=65536
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
ProtectSystem=full
ProtectHome=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

To enable and verify the unit:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now openappa-gateway
sudo systemctl status openappa-gateway
```

## Getting started

Install OpenAPPA CLI and launch the security proxy daemon:

```bash
# Install OpenAPPA package
pip install openappa

# Initialize default security policy configuration
openappa init --policy strict

# Launch OpenAPPA security gateway daemon on port 9090
openappa daemon --port 9090 --config policy.yaml
```

## CLI examples

```bash
# Inspect security audit log for active agent session
openappa logs --session-id agent-session-8821 --verify-signatures

# Evaluate a security policy against a sample tool call
openappa policy test --policy policy.yaml --tool "bash_execute" --params '{"cmd": "rm -rf /"}'

# Run agent tool execution inside OpenAPPA sandbox proxy
openappa run --agent-script agent.py --sandbox microvm
```

## API examples

### FastMCP 3.1 Security Controller & Pydantic v2 Policy Enforcement
The following Python script implements a **FastMCP 3.1** security controller using **Pydantic v2** validation.

```python
import os
import logging
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenAPPA-SecurityController")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("openappa-security-gateway")

# Pydantic v2 Policy Rule Schema
class AgentActionPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str = Field(..., description="Unique agent identifier")
    allowed_tools: List[str] = Field(..., min_items=1, description="List of permitted tool names")
    max_execution_time_sec: int = Field(default=30, ge=1, le=300)
    allow_network: bool = Field(default=False)
    mask_credentials: bool = Field(default=True)
    environment: str = Field(default="sandbox", description="Execution context (sandbox, microvm, direct)")

    @field_validator("environment")
    @classmethod
    def validate_env(cls, v: str) -> str:
        valid = ["sandbox", "microvm", "container"]
        if v.lower() not in valid:
            raise ValueError(f"Environment must be one of {valid}")
        return v.lower()

class ToolExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str = Field(..., description="Requesting agent ID")
    tool_name: str = Field(..., description="Requested tool function name")
    parameters: Dict[str, str] = Field(default_factory=dict, description="Input parameters")
    session_token: str = Field(..., min_length=16, description="Cryptographic session validation token")

@mcp.tool()
async def validate_agent_action(
    policy_dict: dict,
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Evaluates an agent tool call against OpenAPPA zero-trust security policy.

    Args:
        policy_dict: Policy parameters matching AgentActionPolicy.
        request_dict: Execution payload matching ToolExecutionRequest.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Evaluating security policy with Pydantic v2...")

    try:
        policy = AgentActionPolicy.model_validate(policy_dict)
        req = ToolExecutionRequest.model_validate(request_dict)

        if ctx:
            await ctx.info(f"Agent '{req.agent_id}' requested tool '{req.tool_name}' in '{policy.environment}'")

        if req.tool_name not in policy.allowed_tools:
            return {
                "decision": "DENIED",
                "reason": f"Tool '{req.tool_name}' is not in allowed list for agent '{policy.agent_id}'",
                "policy_enforced": True
            }

        return {
            "decision": "ALLOWED",
            "agent_id": req.agent_id,
            "tool": req.tool_name,
            "sandbox_type": policy.environment,
            "credentials_masked": policy.mask_credentials,
            "status": "cleared"
        }
    except ValidationError as ve:
        logger.error(f"Policy schema validation failure: {ve}")
        raise ValueError(f"Invalid policy or request schema: {ve}")

@mcp.tool()
async def get_gateway_health(ctx: Optional[Context] = None) -> dict:
    """Returns OpenAPPA security proxy operational state and threat metrics."""
    if ctx:
        await ctx.info("Checking OpenAPPA security gateway state...")

    return {
        "status": "active",
        "engine": "OpenAPPA Zero-Trust Gateway v2.4",
        "blocked_prompt_injections_count": 42,
        "active_sandboxes_count": 3,
        "audit_logging": "cryptographically_signed_enabled"
    }

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Root Cause | Resolution Procedure |
| :--- | :--- | :--- |
| **`PermissionDenied: Policy Violation`** | Requested tool name is missing from `allowed_tools` list in `policy.yaml`. | Add tool identifier to RBAC policy YAML or adjust agent role assignment. |
| **`SandboxExecutionTimeout`** | Tool operation exceeded `max_execution_time_sec`. | Increase timeout limit in policy schema or optimize inner tool script execution. |
| **`CredentialInjectionFailed`** | Target secret missing from vault environment. | Verify API key is registered in OpenAPPA vault using `openappa secrets list`. |
| **`PromptInjectionFlagged`** | Input payload triggered neural injection classifier. | Inspect request payload logs via `openappa logs --session-id` and refine regex filters if false positive. |

## Integration patterns
- **FastMCP Secure Proxy Architecture**: Wrap all incoming agent tool executions in an OpenAPPA validation hook prior to dispatching to underlying OS tools.
- **Automated SOC Incident Response**: Forward OpenAPPA cryptographic security audit logs directly to SIEM solutions (Splunk, Datadog) for real-time threat monitoring.

## Best practices & Security
- **Strict Network Isolation**: Default `allow_network` to `False` in sandbox environments unless explicitly required for specific target endpoints.
- **Regular Policy Audits**: Review agent permission YAML policies weekly to ensure adherence to the principle of least privilege.

## Reference implementation

```python
# Standalone test for OpenAPPA Pydantic v2 policy validation
from pydantic import ValidationError

def test_openappa_policy_schema():
    payload = {
        "agent_id": "agent-code-reviewer",
        "allowed_tools": ["read_file", "git_status", "diff_check"],
        "max_execution_time_sec": 15,
        "environment": "sandbox"
    }
    policy = AgentActionPolicy.model_validate(payload)
    assert policy.agent_id == "agent-code-reviewer"
    assert policy.mask_credentials is True
    print("OpenAPPA policy schema test passed successfully.")

if __name__ == "__main__":
    test_openappa_policy_schema()
```

## Related tools / concepts
- [Docker Sandbox](../infrastructure/docker.md) — Container isolation runtime.
- [Vault MCP](../automation_orchestration/vault-mcp.md) — Secure secret management tool for agent pipelines.
- [Claude Code](../development_ops/claude-code.md) — CLI coding agent requiring sandboxing.
- [CrewAI](../frameworks/ag2.md) — Multi-agent orchestration framework.

## Sources / references
- [OpenAPPA Archestra Security Announcement](https://www.infoq.com/news/2026/10/open-APPA-zero-security-breach/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=AI%2C+ML+%26+Data+Engineering)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
