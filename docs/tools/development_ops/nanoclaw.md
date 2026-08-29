# NanoClaw

## What it is
**NanoClaw** is a lightweight, AI-native personal assistant and sandboxed agent framework designed as a high-security alternative to [OpenClaw](openclaw.md). Under early January 2027 SOTA standards, it runs on the FastMCP 3.1 runtime layer and Claude Agent SDK, prioritizing codebase simplicity, zero-trust container isolation, and sub-millisecond local-first tool execution across frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4 Maverick**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

## What problem it solves
Executing autonomous AI agents directly on host developer machines poses severe security risks, including prompt injection vulnerabilities and rogue command execution. NanoClaw eliminates these risks by running agent execution logic in ephemeral Linux containers (Docker, Apple Sandbox, or Firecracker microVMs) governed strictly by the **FastMCP 3.1 Task Protocol**. This ensures all filesystem, network, and terminal interactions are sandboxed and verifiable.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Sandboxed Agent Runtime. It acts as an isolated execution plane for personal AI assistants, automated terminal tasks, and local tool-calling integrations, sitting between host OS operations and frontier reasoning models.

## Typical use cases
- **Sandboxed Agentic Workflows**: Executing untrusted code generation, terminal scripts, or web scraping within isolated ephemeral containers.
- **Multi-Channel Assistant Swarms**: Deploying secure, sandboxed assistants across communication platforms (Telegram, Discord, Slack) with isolated memory stores.
- **Self-Evolving Tool Integrations**: Extending agent capabilities using [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) within container boundaries.
- **FastMCP 3.1 Local Tool Execution**: Connecting local system utilities to remote LLM backends over type-safe MCP transports.

## Strengths
- **Zero-Trust Container Sandboxing**: Agents run inside lightweight, ephemeral environments with restricted permissions and no direct host access by default.
- **FastMCP 3.1 Native Integration**: Implements the FastMCP 3.1 Task Protocol, offering sub-millisecond tool registration, type enforcement, and dynamic tool discovery.
- **Minimal Footprint**: Compact codebase (< 3,000 lines of core logic) designed for simple code audits and rapid extension.
- **High Resource Efficiency**: Optimized container base images reduce cold-start latency to under 200ms.

## Limitations
- **Local Container Prerequisite**: Requires Docker, Firecracker, or Apple Container infrastructure installed on the host machine.
- **Single-Node Focus**: Optimized for local-first developer and personal usage rather than multi-region distributed cloud clusters.
- **Execution Overhead**: Ephemeral container provisioning introduces a slight startup delay compared to un-sandboxed shell execution.

## When to use it
- When building personal AI assistants that require execution of arbitrary shell commands or untrusted code.
- If you require strict data containment and ephemeral execution environments for developer automation.
- When modularizing agent workflows using FastMCP 3.1 tool interfaces.

## When not to use it
- For enterprise-scale multi-tenant cloud orchestration (use Kubernetes-native agent solutions or OpenClaw enterprise gateways).
- For simple read-only text generation tasks where tool execution safety is not a factor.
- In environments where container virtualization cannot be installed.

## Getting started

### Installation
NanoClaw requires Node.js 22+ and a local container daemon (Docker 26+ or Apple Container).

```bash
# Clone the repository
git clone https://github.com/qwibitai/nanoclaw.git
cd nanoclaw

# Install dependencies
npm install

# Initialize sandboxed workspace
nanoclaw init --sandbox docker
```

### FastMCP 3.1 Bridge Registration
Register a custom FastMCP tool server with NanoClaw:
```bash
nanoclaw mcp add --name filesystem --command "npx -y @modelcontextprotocol/server-filesystem /tmp/sandbox"
```

## CLI examples

```bash
# Execute a sandboxed task in an isolated ephemeral container
nanoclaw exec "Analyze all files in /workspace/data and summarize key findings"

# List active sandboxed container instances
nanoclaw status

# Inspect container execution audit logs
nanoclaw logs --last 50
```

## API examples

### Programmatic Configuration Validation with Pydantic v2
The following Python module demonstrates modeling and programmatically validating NanoClaw container sandbox settings and FastMCP 3.1 bridge configs under early January 2027 SOTA standards:

```python
from pydantic import BaseModel, Field
from typing import List
import json

class SandboxedRuntimeConfig(BaseModel):
    isolation_layer: str = Field(default="docker", pattern=r"^(docker|apple-sandbox|firecracker|none)$")
    memory_limit_mb: int = Field(default=4096, ge=512, le=32768)
    cpu_cores: float = Field(default=4.0, ge=0.5, le=16.0)
    read_only_root: bool = Field(default=True)

class NanoClawConfig(BaseModel):
    model_name: str = Field(..., pattern=r"^(claude-5\.6-.*|gpt-5\.6-.*|gemini-4\.0-.*|llama-4-.*|gemma-4-.*|qwen-3\.6-.*)$")
    sandbox: SandboxedRuntimeConfig = Field(default_factory=SandboxedRuntimeConfig)
    fastmcp_enabled: bool = Field(default=True)
    mcp_version: str = Field(default="3.1", pattern=r"^3\.1$")
    allowed_tools: List[str] = Field(default_factory=lambda: ["filesystem", "bash", "fetch"])

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "model_name": "claude-5.6-sonnet",
                "sandbox": {
                    "isolation_layer": "docker",
                    "memory_limit_mb": 4096,
                    "cpu_cores": 4.0,
                    "read_only_root": True
                },
                "fastmcp_enabled": True,
                "mcp_version": "3.1",
                "allowed_tools": ["filesystem", "bash", "fetch"]
            }
        }
    }

def validate_nanoclaw_config(payload: dict) -> str:
    """Validates NanoClaw configuration payload using Pydantic v2."""
    try:
        config = NanoClawConfig.model_validate(payload)
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
        "model_name": "claude-5.6-sonnet",
        "sandbox": {
            "isolation_layer": "firecracker",
            "memory_limit_mb": 8192,
            "cpu_cores": 4.0,
            "read_only_root": True
        },
        "fastmcp_enabled": True,
        "mcp_version": "3.1",
        "allowed_tools": ["filesystem", "bash", "fetch", "web_browser"]
    }
    print(validate_nanoclaw_config(test_payload))
```

## Related tools / concepts
- [OpenClaw](openclaw.md) — Enterprise gateway alternative for agentic tool execution.
- [Claude Code](claude-code.md) — Interactive terminal developer agent CLI.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard tool protocol for agents.
- [Windsurf](windsurf.md) — Agentic IDE built on FastMCP 3.1.
- [Axiom Guardian](axiom-guardian.md) — Alignment and challenge guardrail MCP server.

## Sources / References
- [NanoClaw Official GitHub Repository](https://github.com/qwibitai/nanoclaw)
- [NanoClaw Documentation Portal](https://nanoclaw.dev/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/specification/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
