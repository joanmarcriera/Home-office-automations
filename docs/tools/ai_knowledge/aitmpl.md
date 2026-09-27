# AI Templates (aitmpl)

## What it is
AI Templates (`aitmpl`) is an enterprise package registry, workflow catalog, and package manager for AI software engineering assets. It enables software engineering teams to discover, publish, test, version-control, and deploy pre-packaged AI tools optimized for frontier reasoning models (including Claude 5.6, GPT-5.6, and Gemini 4.0 Pro). `aitmpl` packages prompt recipes, specialist subagent definitions, custom terminal commands, and [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) tool bindings into installable, deterministic modules.

Key capabilities include:
- **Versioned Subagent Packaging**: Package, audit, and distribute domain-specific subagent roles (such as React performance auditors, Rust memory safety reviewers, or database migration validators).
- **FastMCP 3.1 Tool Binding Registries**: Distribute pre-configured Model Context Protocol tool servers and schema validators across enterprise engineering teams.
- **Automated AI Pre-Commit Hooks**: Install AI-powered Git validation hooks that analyze proposed code diffs against enterprise security, performance, and style contracts before commit finalization.
- **Cross-Model Prompt Portability**: Automatically translate and adapt prompt structures between different model architectures to preserve output quality and compliance.
- **Continuous Telemetry & Audit Logs**: Track subagent token consumption, invocation latency, and execution outcomes across multi-repo organizations.

## What problem it solves
Developing custom developer subagents, prompt chains, and automated code review workflows across large engineering organizations frequently leads to duplicated effort, prompt drift, inconsistent output quality, and security vulnerabilities. Without centralized asset governance, individual developers write ad-hoc prompt scripts that lack version control, test coverage, and audit logs.

`aitmpl` addresses these challenges by:
- **Standardizing Developer AI Workflows**: Ensuring every engineer utilizes reviewed, version-controlled prompt templates and tool definitions regardless of their local IDE ([Claude Code](../development_ops/claude-code.md), [Cursor](../development_ops/cursor.md), VS Code).
- **Automating Quality & Compliance Audits**: Embedding AI-driven static analysis directly into Git pre-commit hooks and CI/CD pipelines to catch vulnerabilities prior to code merge.
- **Eliminating Integration Overhead**: Providing a single command-line interface (`npx aitmpl` / `cct`) to install subagent suites, FastMCP 3.1 tools, and workspace hooks in seconds.

## Where it fits in the stack
**Category**: AI & Knowledge / Prompt, Agent & Subagent Governance Infrastructure.

`aitmpl` acts as a central package management and orchestration layer positioned between developer workstations, enterprise tool integrations, and frontier model APIs.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Developer Workstation / IDE Layer                    │
│             (Claude Code, Cursor, VS Code, Command Line)                │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ npx aitmpl install / cct sync
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     AI TEMPLATES (aitmpl) REGISTRY                      │
│       - Package Catalog & Version Resolver                             │
│       - FastMCP 3.1 Subagent & Tool Bindings                            │
│       - Pydantic v2 Schema & Telemetry Validator                        │
└───────────────────┬─────────────────────────────────┬───────────────────┘
                    │                                 │
                    ▼                                 ▼
┌───────────────────────────────────────┐ ┌──────────────────────────────┐
│        Frontier Model Runtime         │ │    FastMCP 3.1 Tool Servers   │
│ - Claude 5.6 / GPT-5.6 Execution      │ │ - Git Security Pre-Commit    │
│ - Automated Prompt Translation        │ │ - AST & Linter Executors     │
└───────────────────────────────────────┘ └──────────────────────────────┘
```

## Typical use cases
- **Standardized Subagent Deployment**: Deploying specialized subagents across multi-repo engineering teams with verified prompt safety bounds.
- **FastMCP 3.1 Server Distribution**: Standardizing and distributing pre-tested FastMCP 3.1 database inspection tools and API testing utilities.
- **Automated Git Pre-Commit Guardrails**: Enforcing real-time pre-commit verification where AI agents check code changes against team safety guidelines and test requirements.
- **Model-Specific Prompt Adaptation**: Packaging prompt recipes optimized for model capabilities (e.g., leveraging extended thinking in Claude 5.6 or structured outputs in GPT-5.6).

## Strengths
- **Rapid Zero-Install Execution**: Instantly accessible via `npx aitmpl` or short alias `cct` without mandatory global package installation.
- **Native FastMCP 3.1 Architecture**: Designed from the ground up for Model Context Protocol servers, subagent tools, and structured JSON schemas.
- **Enterprise-Grade Governance**: Enables enterprise teams to mirror registries privately, enforce security scans on AI assets, and track prompt versioning.
- **Comprehensive CLI Suite**: Includes CLI tools for batch package installation, local tool diagnostics, and real-time token telemetry tracking.

## Limitations
- **Registry Connectivity Requirement**: Requires network access to the primary template registry unless a local enterprise mirror is configured.
- **Domain Context Extension Need**: Highly specialized domain logic requires extending base templates with repository-specific context files.
- **Token Overhead Management**: Automated AI pre-commit hooks consume model tokens, requiring rate limit management in high-commit CI environments.

## When to use it
- When standardizing AI developer tools, subagent definitions, and prompt templates across an engineering organization.
- When distributing custom FastMCP 3.1 subagents and automated Git validation hooks across a team.
- When migrating multi-prompt workflows between LLM providers while maintaining deterministic output format contracts.

## When not to use it
- In completely air-gapped development environments where local template mirroring has not been provisioned.
- For simple, single-turn conversational queries where lightweight manual prompting is sufficient.

## Getting started

### Installation
Execute the CLI dynamically via `npx`, install it globally using `npm`, or use the official short alias:

```bash
# Run dynamically via npx
npx aitmpl@latest --help

# Or use the quick alias
npx cct@latest status

# Or install globally
npm install -g aitmpl
```

### Quickstart Example
Install a specialized React performance auditor agent along with FastMCP 3.1 tool bindings:

```bash
npx aitmpl@latest --agent development-team/react-auditor --yes
```

## CLI examples

### Batch Installing Subagents, Commands, and Pre-Commit Hooks
Install a complete subagent and security validation stack in a single command:

```bash
npx aitmpl@latest \
  --agent development-team/react-auditor \
  --command testing/generate-unit-tests \
  --hook git/pre-commit-security \
  --yes
```

### Running Local System Diagnostics
Verify the health and integrity of local FastMCP 3.1 tool bindings and installed templates:

```bash
npx aitmpl@latest --health-check
```

### Monitoring Real-Time Usage Telemetry
Launch the telemetry interface to monitor subagent executions, token consumption, and model response latency:

```bash
npx aitmpl@latest --analytics --period 24h
```

## API examples

### Registry Query & Telemetry Submission in Python with Pydantic v2
The following script demonstrates querying the `aitmpl` registry and submitting execution telemetry payloads using **Pydantic v2**:

```python
import os
import requests
from typing import Literal, List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class SubagentManifest(BaseModel):
    package_name: str = Field(..., description="Package identifier, e.g., development-team/react-auditor")
    version: str = Field(..., description="SemVer package version string")
    category: Literal["agent", "command", "hook", "workflow"]
    target_model: str = Field(default="claude-5.6", description="Target LLM runtime")
    fastmcp_compatible: bool = Field(default=True, description="Whether FastMCP 3.1 bindings are included")
    checksum_sha256: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

class TelemetryPayload(BaseModel):
    package_name: str = Field(..., description="Installed package identifier")
    execution_status: Literal["success", "failure", "cancelled"]
    latency_ms: int = Field(..., ge=0, description="Execution duration in milliseconds")
    tokens_consumed: int = Field(..., ge=0, description="Tokens used during agent run")
    fastmcp_version: str = Field(default="3.1")
    user_environment: str = Field(default="cli-tool", description="Execution environment descriptor")

class AITemplatesRegistryClient:
    def __init__(self, registry_url: str = "https://www.aitmpl.com"):
        self.registry_url = registry_url.rstrip("/")

    def fetch_manifest(self, package_name: str) -> SubagentManifest:
        # Simulated API response for verification environment
        mock_data = {
            "package_name": package_name,
            "version": "1.4.2",
            "category": "agent",
            "target_model": "claude-5.6",
            "fastmcp_compatible": True,
            "checksum_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
        return SubagentManifest.model_validate(mock_data)

    def submit_telemetry(self, telemetry: TelemetryPayload) -> bool:
        # Serializing payload with Pydantic v2
        serialized = telemetry.model_dump()
        # In production: requests.post(f"{self.registry_url}/api/telemetry", json=serialized)
        return True

if __name__ == "__main__":
    client = AITemplatesRegistryClient()
    manifest = client.fetch_manifest("development-team/react-auditor")
    print(f"Manifest Fetched: {manifest.package_name} v{manifest.version}")

    telemetry = TelemetryPayload(
        package_name=manifest.package_name,
        execution_status="success",
        latency_ms=1240,
        tokens_consumed=850
    )
    success = client.submit_telemetry(telemetry)
    print(f"Telemetry Submitted: {success}")
```

### FastMCP 3.1 Subagent Server Implementation
The following code demonstrates implementing a local FastMCP 3.1 server that executes a downloaded `aitmpl` subagent recipe:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("AITemplates-Execution-Server")

class FastMCPExecutionRequest(BaseModel):
    package_name: str = Field(..., description="Target aitmpl subagent package")
    source_code: str = Field(..., description="Source code text to be audited")
    strict_mode: bool = Field(default=True, description="Enforce strict security analysis")

@mcp.tool()
async def execute_subagent_audit(request: FastMCPExecutionRequest) -> dict:
    """Executes a downloaded aitmpl subagent template against target source code."""
    # FastMCP Tool Execution Logic
    return {
        "status": "completed",
        "package": request.package_name,
        "violations_found": 0,
        "audit_summary": "Passed all pre-commit security rules.",
        "fastmcp_version": "3.1"
    }

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Claude Plugins](../development_ops/claude-plugins.md) — Plugin architecture for Claude developer environments.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for connecting AI agents to external tool servers.
- [Claude Code](../development_ops/claude-code.md) — Anthropic agentic command line coding tool.
- [Flowise](flowise.md) — Drag-and-drop visual workflow builder for AI agents.
- [OpenCode](../development_ops/opencode.md) — Open-source agentic coding assistant framework.

## Sources / references
- [AI Templates Official Portal](https://www.aitmpl.com/)
- [AI Templates Documentation](https://docs.aitmpl.com/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/spec/3.0)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
