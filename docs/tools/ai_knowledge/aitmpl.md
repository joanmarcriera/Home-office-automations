# AI Templates (aitmpl)

## What it is
AI Templates (`aitmpl`) is a package registry and workflow catalog for AI engineering assets, providing version-controlled prompt templates, specialist subagent definitions, custom terminal commands, and [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) server configurations. It enables engineering teams to discover, publish, test, and deploy pre-packaged AI tools optimized for frontier models including Claude 5.6, GPT-5.6, and Gemini 4.0 Pro.

## What problem it solves
Developing custom developer agents and multi-step prompt chains often results in duplicated effort, inconsistent output quality, and tool fragmentation across engineering teams. AI Templates solves this by packaging prompt recipes, FastMCP 3.1 tool bindings, and agent behaviors into versioned, installable modules that can be audited, executed via CLI, or embedded into CI/CD pipelines.

## Where it fits in the stack
**AI & Knowledge / Prompt and Agent Infrastructure**. It operates as a discovery and package management layer for reusable developer agent tools, FastMCP 3.1 subagents, and automated Git validation hooks.

```
┌────────────────────────────────────────┐
│             Developer Workstation      │
│      (Claude Code, Cursor, VSCode)     │
└───────────────────┬────────────────────┘
                    │ npx aitmpl / cct install
┌───────────────────▼────────────────────┐
│         AI TEMPLATES REGISTRY          │
│     (FastMCP 3.1 Subagents & Hooks)    │
└──────────┬───────────────────┬─────────┘
           │                   │
┌──────────▼──────────┐ ┌──────▼─────────────────┐
│ Frontier Models     │ │ FastMCP 3.1 Tools     │
│ (Claude 5.6/GPT-5.6)│ │ (Git Hooks / Linters) │
└─────────────────────┘ └────────────────────────┘
```

## Typical use cases
- **Standardized Subagent Deployment**: Bootstrapping specialist agent roles (e.g., React performance auditors or Rust security reviewers) across developer teams.
- **FastMCP 3.1 Server Distribution**: Distributing ready-to-run FastMCP 3.1 tool bindings for database inspection and automated API testing.
- **Automated Pre-Commit Validation**: Installing AI-backed Git hooks that analyze proposed diffs against team safety and style contracts before commit completion.
- **Model-Specific Prompt Portability**: Accessing prompt templates tuned specifically for Claude 5.6, GPT-5.6, or DeepSeek-V4 capabilities.

## Strengths
- **Fast Discovery & Setup**: Speeds up developer agent onboarding via ready-to-use recipes.
- **Native FastMCP 3.1 Support**: Direct integration with Model Context Protocol servers and tool schemas.
- **CLI & CI/CD Portability**: Executable directly via `npx aitmpl` or `cct` without mandatory global installations.
- **Versioned Quality Control**: Pin specific template versions to ensure deterministic behavior across environments.

## Limitations
- **Registry Dependency**: Requires network access to the primary registry unless local mirroring is configured.
- **Template Customization Need**: Highly domain-specific enterprise business logic requires extending off-the-shelf templates.

## When to use it
- When bootstrapping new AI-assisted software projects or standardizing team coding environments.
- When distributing custom FastMCP 3.1 subagents and Git validation hooks across a team.
- To discover battle-tested prompts for newly released frontier models.

## When not to use it
- In strictly air-gapped systems without a private template mirror.
- For trivial, single-turn prompts where custom context creation is faster than registry lookup.

## Getting started

### Installation
Install the CLI globally or run it dynamically using `npx`:

```bash
# Run dynamically via npx
npx aitmpl@latest

# Or use the quick alias
npx cct@latest

# Or install globally
npm install -g aitmpl
```

### Quickstart Example
Install a specialist frontend development agent with FastMCP 3.1 support:

```bash
npx aitmpl@latest --agent development-team/frontend-specialist --yes
```

## CLI examples
The CLI provides complete control over local agent installation, health verification, and session monitoring:

```bash
# Batch install a frontend development stack
npx aitmpl@latest \
  --agent development-team/react-auditor \
  --command testing/generate-unit-tests \
  --hook git/pre-commit-security \
  --yes

# Run health diagnostics on local MCP bindings and template integrity
npx aitmpl@latest --health-check

# Launch real-time telemetry dashboard to monitor token usage
npx aitmpl@latest --analytics
```

## API examples

### Submitting Telemetry via Python with Pydantic v2 Validation
The following Python script uses **Pydantic v2** to validate telemetry payloads sent to the AI Templates registry when tracking agent downloads or execution status.

```python
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl
import requests

class TemplateTelemetryPayload(BaseModel):
    component_name: str = Field(..., min_length=3)
    component_type: Literal["agent", "command", "hook", "workflow"]
    platform: str = Field(default="cli-tool")
    target_model: str = Field(default="claude-5.6")
    fastmcp_version: str = Field(default="3.1")

class TelemetryAPIConfig(BaseModel):
    base_url: HttpUrl = Field(default="https://www.aitmpl.com")
    endpoint_path: str = Field(default="/api/track-download")
    timeout: int = Field(default=10, ge=1)

class TelemetryClient:
    def __init__(self, config: TelemetryAPIConfig):
        self.config = config

    def submit_telemetry(self, payload: TemplateTelemetryPayload) -> dict:
        serialized_payload = payload.model_dump()
        target_url = f"{str(self.config.base_url).rstrip('/')}{self.config.endpoint_path}"
        try:
            response = requests.post(
                target_url,
                json=serialized_payload,
                headers={"Content-Type": "application/json"},
                timeout=self.config.timeout
            )
            return {"status": "success", "status_code": response.status_code}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    client = TelemetryClient(TelemetryAPIConfig())
    payload = TemplateTelemetryPayload(
        component_name="development-team/react-auditor",
        component_type="agent",
        target_model="claude-5.6"
    )
    result = client.submit_telemetry(payload)
    print(f"Telemetry Submission Result: {result['status']}")
```

## Related tools / concepts
- [Claude Plugins](../development_ops/claude-plugins.md) — Plugin architecture for Claude developer tools.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for connecting agents to external systems.
- [Gemini](gemini.md) — Google multimodal LLM ecosystem.
- [Flowise](flowise.md) — Visual flow builder for AI agents.

## Sources / references
- [AI Templates Official Portal](https://www.aitmpl.com/)
- [AI Templates Documentation](https://docs.aitmpl.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
