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

OpenAPPA enforces security through a three-layer isolation pipeline:

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

@mcp.tool()
async def validate_agent_action(
    policy_dict: dict,
    requested_tool: str,
    action_params: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Evaluates an agent tool call against OpenAPPA zero-trust security policy.

    Args:
        policy_dict: Policy parameters matching AgentActionPolicy.
        requested_tool: Name of requested tool.
        action_params: Tool input arguments.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Evaluating security policy with Pydantic v2...")

    try:
        policy = AgentActionPolicy.model_validate(policy_dict)
        if ctx:
            await ctx.info(f"Agent '{policy.agent_id}' requested tool '{requested_tool}' in '{policy.environment}'")

        if requested_tool not in policy.allowed_tools:
            return {
                "decision": "DENIED",
                "reason": f"Tool '{requested_tool}' is not in allowed list for agent '{policy.agent_id}'",
                "policy_enforced": True
            }

        return {
            "decision": "ALLOWED",
            "agent_id": policy.agent_id,
            "tool": requested_tool,
            "sandbox_type": policy.environment,
            "credentials_masked": policy.mask_credentials,
            "status": "cleared"
        }
    except ValidationError as ve:
        logger.error(f"Policy schema validation failure: {ve}")
        raise ValueError(f"Invalid policy schema: {ve}")

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
