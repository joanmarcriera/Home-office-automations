# Windsurf IDE

## What it is
**Windsurf** is the world's first agentic IDE, developed by **Codeium** and deeply integrated with **Cognition's Devin 3.0** reasoning engine and the **FastMCP 3.1 Task Protocol**. Under early January 2027 SOTA standards, it is built on top of an optimized VS Code core featuring the enhanced **Cascade v3.0** AI interaction model. Cascade moves beyond standard chat interfaces into autonomous, multi-file execution, speculative background refactoring, and real-time environment management for frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4 Maverick**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

## What problem it solves
Traditional AI assistants in IDEs act as passive inline autocompleters. Windsurf eliminates both the "context gap" and the "execution gap" by allowing Cascade to index massive multi-gigabyte repositories, inspect active terminal outputs, manage containerized microservices, run Playwright verification loops, and perform non-blocking background edits. It supports [Agentic Session Orchestration](../../knowledge_base/agent_protocols.md) with strict human-in-the-loop validation checkpoints.

## Where it fits in the stack
**Category**: Tool / Development & Ops / Agentic IDE. It serves as the primary developer "Command Center" bridging text editing, terminal execution, containerized testing, and multi-agent coordination.

## Typical use cases
- **Legacy Stack Migration**: Directing Cascade to "Convert this legacy Express.js microservice to Rust/Axum with Pydantic v2 schema endpoints" with automated build and test validation loops.
- **Autonomous Feature Scaffolding**: Generating full-stack features (React UI, FastMCP 3.1 endpoints, database migrations) from natural language requirements.
- **Continuous Background Debugging**: Cascade monitoring background build logs and automatically suggesting or applying targeted patches to failing tests.
- **Large-Scale Structural Refactoring**: Renaming APIs or updating data structures across hundreds of files with semantic precision.
- **Multi-Agent CI/CD Remediation**: Interfacing with remote agent swarms (via FastMCP 3.1) to diagnose and fix failing GitHub Actions or GitLab pipelines.

## Strengths
- **Native FastMCP 3.1 Support**: Out-of-the-box support for FastMCP 3.1 Task Protocol, enabling seamless integration with external databases, vector stores, and custom agent tools.
- **Devin 3.0 Reasoning Engine**: Leverages Cognition's latest long-horizon reasoning loops for complex multi-step refactoring tasks.
- **Real-Time Indexing**: Semantic indexing system processes code diffs in sub-millisecond timeframes.
- **VS Code Extension Ecosystem**: Full compatibility with the standard VS Code plugin ecosystem and customization capabilities.

## Limitations
- **Cloud Dependency**: Advanced Cascade autonomous agent features require active cloud connectivity to Codeium infrastructure.
- **Proprietary Agent Architecture**: The Cascade control plane and Devin reasoning layers remain closed-source.
- **Resource Footprint**: Indexing large repositories alongside active LLM reasoning sessions requires at least 16GB RAM.

## When to use it
- When developing complex enterprise applications requiring multi-file context and automated testing feedback loops.
- If you want an IDE that can autonomously run terminal commands, execute test suites, and fix errors in background sessions.
- When expanding development workflows with FastMCP 3.1 enterprise tools and remote agent infrastructure.

## When not to use it
- In strictly air-gapped or offline development environments where external API access is blocked.
- For lightweight single-file script editing where full agentic indexing overhead is unnecessary.
- If your development workflow mandates an entirely open-source editor and backend model stack.

## Getting started

### Local Installation
1. Download the Windsurf installer for your OS (macOS, Windows, Linux) from the official website.
2. Complete the setup wizard.
3. Authenticate with your Codeium account to activate **Cascade v3.0** and **FastMCP 3.1** capabilities.

### Configuring FastMCP 3.1 Tools
Add FastMCP 3.1 servers to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "google-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-search"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/production"]
    }
  }
}
```

## CLI examples

```bash
# Launch Windsurf in the current workspace
windsurf .

# Open a specific file and line in Cascade mode
windsurf -g src/api/router.py:45

# Compare diffs using Windsurf's interactive agentic diff view
windsurf --diff legacy_handler.py new_handler.py
```

## API examples

### Programmatic Configuration Validation with Pydantic v2
The following Python module demonstrates modeling and validating a Windsurf IDE session profile and FastMCP 3.1 client configuration under early January 2027 SOTA standards:

```python
from pydantic import BaseModel, Field
from typing import List, Dict
import json

class MCPServerConfig(BaseModel):
    command: str = Field(..., min_length=1)
    args: List[str] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)

class WindsurfConfig(BaseModel):
    mcp_servers: Dict[str, MCPServerConfig] = Field(..., alias="mcpServers")
    cascade_version: str = Field(default="3.0", pattern=r"^(3\.0|3\.1)$")
    devin_reasoning_enabled: bool = Field(default=True)
    max_autonomous_steps: int = Field(default=250, ge=10, le=1000)
    primary_model: str = Field(default="claude-5.6-sonnet")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "mcpServers": {
                    "postgres": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/mydb"]
                    }
                },
                "cascade_version": "3.0",
                "devin_reasoning_enabled": True,
                "max_autonomous_steps": 250,
                "primary_model": "claude-5.6-sonnet"
            }
        }
    }

def validate_windsurf_config(payload: dict) -> str:
    """Validates Windsurf IDE configuration payload using Pydantic v2."""
    try:
        config = WindsurfConfig.model_validate(payload)
        return json.dumps({
            "status": "success",
            "validated_config": config.model_dump(by_alias=True)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    test_payload = {
        "mcpServers": {
            "postgres-db": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/homelab"],
                "env": {"PGPASSWORD": "secure_secret"}
            }
        },
        "cascade_version": "3.0",
        "devin_reasoning_enabled": True,
        "max_autonomous_steps": 300,
        "primary_model": "gpt-5.6-turbo"
    }
    print(validate_windsurf_config(test_payload))
```

## Related tools / concepts
- [Cursor](cursor.md) — Competitor AI IDE featuring Composer mode.
- [Aider](aider.md) — Terminal-native git-integrated agentic coding assistant.
- [Claude Code](claude-code.md) — Anthropic's interactive developer agent CLI.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Universal protocol for extending IDE capabilities.
- [NanoClaw](nanoclaw.md) — Containerized personal assistant framework.
- [OpenClaw](openclaw.md) — Gateway for agentic workflows and tool safety.

## Sources / References
- [Windsurf Official Documentation](https://docs.windsurf.com/)
- [Codeium Release Notes (January 2027)](https://codeium.com/blog/windsurf-v3-release)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/specification/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
