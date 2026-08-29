# NanoClaw

## What it is
**NanoClaw** is a lightweight, AI-native personal assistant framework designed as a secure, containerized alternative to [OpenClaw](openclaw.md). Under early January 2027 SOTA standards, it runs on the Claude Agent SDK and prioritizes codebase simplicity, strong sandboxing, and OS-level isolation, fully supporting the **MCP 3.1 / FastMCP 3.1 Task Protocol** for reliable, secure local-first tool execution across frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, **Gemma 4**, and **Qwen 3.6 VL**.

## What problem it solves
It addresses the security risks and code complexity of heavy agent frameworks by providing a minimalist, container-first assistant that evolves through self-modification and composable skills. It ensures that agentic workflows remain secure and private by utilizing **FastMCP 3.1** for rapid, type-safe tool discovery and execution, preventing raw terminal/command prompt injections from altering host files.

## Where it fits in the stack
[Layer 6: Multi-Agent Frameworks & Workflows](../../knowledge_base/ai_tooling_landscape.md#layer-6-multi-agent-frameworks--workflows). It is a lightweight agent runtime for individuals and developers looking for a secure local-first execution environment that integrates seamlessly with [Gemma 4](../ai_knowledge/local_llms.md) and Claude 5.6.

## Typical use cases
- **Secure AI Assistance**: Sandboxed task execution for personal local automation and terminal manipulation.
- **Custom Agent Swarms**: Building multi-channel agents (WhatsApp, Telegram, etc.) with strict data isolation.
- **Self-Evolving Skills**: Developing agents that modify their own logic through the [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) protocol.
- **Local Tool-Calling**: Using [Gemma 4](../ai_knowledge/local_llms.md) with local system tools via the FastMCP 3.1 Bridge.

## Strengths
- **Security-First**: Native container isolation; agents run in ephemeral Linux containers by default.
- **Minimalist**: Small codebase (under 5k LOC), easy to understand and fork for specific needs.
- **FastMCP 3.1 Integration**: Lowest latency for tool registration and execution in the personal assistant category.
- **High Efficiency**: Optimized layer templates reduce token costs by up to 40% compared to unoptimized patterns.

## Limitations
- **Claude-Centric**: Primary optimization is for Claude models, though [Gemma 4](../ai_knowledge/local_llms.md) and DeepSeek-V4 support is stable via MCP.
- **Self-Modification Risk**: Requires comfort with an assistant that writes its own logic (can be disabled via `NC_READONLY_MODE=true`).
- **Resource Minimums**: Requires at least 4GB RAM and Docker 24+ for the isolation layer to function correctly.

## When to use it
- When you want a personal AI assistant that can be fully understood and customized (low code complexity).
- When you require strong security via Linux container isolation (Apple Container, Firecracker, or Docker).
- If you prefer a "skills over features" model where the assistant evolves through code transformations.

## When not to use it
- If you require a managed service or a complex, multi-user enterprise framework.
- If you are not comfortable with an assistant that modifies its own source code to add features.
- For high-concurrency production workloads that require complex orchestration beyond a single node.

## Getting started

### Installation
NanoClaw requires Node.js 22+ and Docker.

```bash
# Clone the repository
git clone https://github.com/qwibitai/nanoclaw.git
cd nanoclaw

# Install dependencies
npm install

# Initialize with Claude Code
claude /setup
```

### Verifying Isolation
To ensure your agent is correctly sandboxed, run:
```bash
nanoclaw exec "echo 'hello' > /root/secret.txt && ls /root"
```
Then verify that a subsequent command or a different container instance cannot see that file.

## CLI examples

### Execution
```bash
# Run a one-off task in the sandbox
nanoclaw task "Organize my downloads folder into categories"

# List active agent containers
nanoclaw ps
```

### Skill Management
```bash
# Add a new skill via natural language
nanoclaw add-skill "Integrate with my local Obsidian vault"

# View installed skills
nanoclaw list-skills
```

## API examples

### Node.js (Agent SDK)
```javascript
import { NanoClaw } from 'nanoclaw';

const agent = new NanoClaw({
  model: 'claude-5.6',
  sandbox: true
});

const response = await agent.run("Summarize README.md and suggest 3 improvements.");
console.log(response);
```

### FastMCP 3.1 Bridge
NanoClaw can bridge local tools to remote agents via FastMCP:

```json
{
  "mcpBridge": {
    "enabled": true,
    "port": 3000,
    "protocol": "fastmcp-3.1",
    "allowedTools": ["filesystem", "bash"]
  }
}
```

### Robust Configuration Validation with Pydantic v2
The following Python script illustrates how to model and programmatically validate a NanoClaw containerized workspace and active FastMCP 3.1 bridge connection under early January 2027 SOTA standards, ensuring strict schema safety and type correctness using Pydantic v2:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
import json

class SandboxedRuntimeConfig(BaseModel):
    isolation_layer: str = Field(default="docker", pattern=r"^(docker|apple-sandbox|firecracker|none)$")
    memory_limit_mb: int = Field(default=2048, ge=512, le=32768)
    cpu_cores: float = Field(default=2.0, ge=0.5, le=16.0)
    read_only: bool = Field(default=False)

class NanoClawConfig(BaseModel):
    model_name: str = Field(..., pattern=r"^(claude-5\.6.*|gpt-5\.6.*|gemini-4\.0-ultra.*|deepseek-v4.*|gemma-4.*|qwen-3\.6-vl.*)$")
    sandbox: SandboxedRuntimeConfig = Field(default_factory=SandboxedRuntimeConfig)
    fastmcp_enabled: bool = Field(default=True)
    mcp_version: str = Field(default="3.1", pattern=r"^3\.1$")
    allowed_tools: List[str] = Field(default_factory=lambda: ["filesystem", "bash"])

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "model_name": "claude-5.6",
                "sandbox": {
                    "isolation_layer": "docker",
                    "memory_limit_mb": 4096,
                    "cpu_cores": 4.0,
                    "read_only": False
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
        "model_name": "claude-5.6",
        "sandbox": {
            "isolation_layer": "docker",
            "memory_limit_mb": 4096,
            "cpu_cores": 4.0,
            "read_only": False
        },
        "fastmcp_enabled": True,
        "mcp_version": "3.1",
        "allowed_tools": ["filesystem", "bash", "fetch"]
    }
    print(validate_nanoclaw_config(test_payload))
```

## Related tools / concepts
- [OpenClaw](openclaw.md) (The heavier "Gateway" alternative)
- [Claude Code](claude-code.md) (Primary setup tool)
- [Anthropic Agent Skills](../agents/anthropic-agent-skills.md) (Evolution protocol)
- [Symphony](../agents/symphony.md) (Agentic orchestration)
- [Jules](../ai_knowledge/jules.md) (Automated maintenance agent)
- [vLLM](../infrastructure/vllm.md) (Local inference backend)
- [Gemma 4](../ai_knowledge/local_llms.md) (Recommended local model)
- [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) (Standard for tool use)

## Sources / references
- [Official GitHub Repository](https://github.com/qwibitai/nanoclaw)
- [Official Website](https://nanoclaw.dev/)
- [NanoClaw Security Whitepaper](https://nanoclaw.dev/security)
- [FastMCP 3.1 Task Protocol Specification](https://mcp.dev/protocols/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
