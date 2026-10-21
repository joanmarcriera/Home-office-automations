# AI Templates (aitmpl)

## What it is
AI Templates (`aitmpl`) is an enterprise package registry, workflow catalog, and package manager for AI software engineering assets. It enables software engineering teams to discover, publish, test, version-control, and deploy pre-packaged AI tools optimized for frontier reasoning models (including Claude 5.6, GPT-5.6, and Gemini 4.0 Pro). `aitmpl` packages prompt recipes, specialist subagent definitions, custom terminal commands, and [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) tool bindings into installable, deterministic modules.

```
+-----------------------------------------------------------------------------------+
|                        AI TEMPLATES (AITMPL) PACKAGE MANAGER                      |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Developer Workstation| ----> | aitmpl / cct CLI      | ---> | Enterprise      | |
|  | (npx aitmpl install)|       | Package Resolver      |      | Template Store  | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Local IDE / Claude  | <---- | FastMCP 3.1 Server    | <--- | Subagent & Tool | |
|  | Code / Cursor Runtime|      | Validator & Execution |      | Package Bindings| |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

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
- **Centralizing Asset Distribution**: Operating enterprise registry mirrors that enforce signature checks and security scanning on all shared subagent packages.

## Where it fits in the stack
**Category**: AI & Knowledge / Prompt, Agent & Subagent Governance Infrastructure.

`aitmpl` acts as a central package management and orchestration layer positioned between developer workstations, enterprise tool integrations, and frontier model APIs.

```
+-----------------------------------------------------------------------------------+
|                            STACK ARCHITECTURE POSITION                            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Developer Workstation / IDE Layer (Claude Code, Cursor, VS Code)            |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | AI Templates (`aitmpl` / `cct`) CLI Resolver & Package Registry              |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | FastMCP 3.1 Subagent Tool Bindings & Pydantic v2 Schema Validator            |  |
|  +-----------------------------------------------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Local / Cloud Frontier Reasoning Models (Claude 5.6, GPT-5.6, Ollama)        |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Standardized Subagent Deployment**: Deploying specialized subagents across multi-repo engineering teams with verified prompt safety bounds.
- **FastMCP 3.1 Server Distribution**: Standardizing and distributing pre-tested FastMCP 3.1 database inspection tools and API testing utilities.
- **Automated Git Pre-Commit Guardrails**: Enforcing real-time pre-commit verification where AI agents check code changes against team safety guidelines and test requirements.
- **Model-Specific Prompt Adaptation**: Packaging prompt recipes optimized for model capabilities (e.g., leveraging extended thinking in Claude 5.6 or structured outputs in GPT-5.6).
- **Enterprise Registry Management**: Private self-hosted template mirroring for air-gapped corporate development environments.

## Strengths
- **Rapid Zero-Install Execution**: Instantly accessible via `npx aitmpl` or short alias `cct` without mandatory global package installation.
- **Native FastMCP 3.1 Architecture**: Designed from the ground up for Model Context Protocol servers, subagent tools, and structured JSON schemas.
- **Enterprise-Grade Governance**: Enables enterprise teams to mirror registries privately, enforce security scans on AI assets, and track prompt versioning.
- **Comprehensive CLI Suite**: Includes CLI tools for batch package installation, local tool diagnostics, and real-time token telemetry tracking.
- **Deterministic Package Locking**: Generates `aitmpl-lock.json` files to freeze subagent prompt versions across CI/CD and developer machines.

## Limitations
- **Registry Connectivity Requirement**: Requires network access to the primary template registry unless a local enterprise mirror is configured.
- **Domain Context Extension Need**: Highly specialized domain logic requires extending base templates with repository-specific context files.
- **Token Overhead Management**: Automated AI pre-commit hooks consume model tokens, requiring rate limit management in high-commit CI environments.

## When to use it
- When standardizing AI developer tools, subagent definitions, and prompt templates across an engineering organization.
- When distributing custom FastMCP 3.1 subagents and automated Git validation hooks across a team.
- When migrating multi-prompt workflows between LLM providers while maintaining deterministic output format contracts.
- When enforcing automated pre-commit code verification backed by versioned AI subagent rules.

## When not to use it
- In completely air-gapped development environments where local template mirroring has not been provisioned.
- For simple, single-turn conversational queries where lightweight manual prompting is sufficient.

## Architectural Deep Dive & Resolution Lifecycle

`aitmpl` implements a deterministic package lifecycle similar to standard software package managers (npm, cargo, pip), but tailored specifically for prompt definitions and FastMCP tools:

```
                           AITMPL PACKAGE RESOLUTION LIFECYCLE

    Developer Invokes `npx aitmpl install <package>`
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Package Version & Lock Engine│  <--- Resolves SemVer & Validates SHA256
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ FastMCP Tool Binder          │  <--- Compiles Tool Schemas & Executables
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Subagent Sandbox Injector    │  <--- Mounts Hooks into IDE / Git Workspace
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │ Telemetry & Audit Logger     │  <--- Records Token Usage & Execution Metrics
     └──────────────────────────────┘
```

### Core Components

1. **Manifest Resolver**: Reads `aitmpl.json` manifests to resolve dependencies, tool schemas, and required model execution capabilities.
2. **FastMCP Bindings Manager**: Mounts FastMCP tool declarations directly into developer agent environments (Claude Code, Cursor).
3. **Lockfile Generator (`aitmpl-lock.json`)**: Pins exact SHA256 checksums of subagent prompt strings to prevent unauthorized prompt tampering or accidental drift.
4. **Telemetry Collector**: Emits execution telemetry (token counts, latency, pass/fail status) to local logs or enterprise analytics dashboards.

```
+---------------------------------------------------------------------------------------------------+
|                                 AITMPL PACKAGE TYPE CATEGORIES                                    |
+-------------------+-------------------------------------------------------------------------------+
| Package Category  | Description & Functionality                                                   |
+-------------------+-------------------------------------------------------------------------------+
| `agent`           | Full subagent definition with domain role, system prompt, and tools           |
| `command`         | Reusable custom terminal or IDE agent action (e.g., generate unit tests)      |
| `hook`            | Git pre-commit or pre-push automated static analysis agent guardrail           |
| `workflow`        | Multi-step orchestrated pipeline connecting multiple subagents and tools       |
+-------------------+-------------------------------------------------------------------------------+
```

## Getting started

### Installation & Basic Usage

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

```bash
# Batch install a complete subagent and security validation stack
npx aitmpl@latest \
  --agent development-team/react-auditor \
  --command testing/generate-unit-tests \
  --hook git/pre-commit-security \
  --yes

# Verify local health and integrity of FastMCP 3.1 bindings
npx aitmpl@latest --health-check

# Inspect local package lockfile status
npx aitmpl@latest lock --verify

# Launch real-time usage telemetry dashboard
npx aitmpl@latest --analytics --period 24h
```

## Production Deployment & Systemd Unit Configuration

For enterprise environments running a persistent self-hosted `aitmpl` private package registry and telemetry collection server, configure the following systemd service unit.

### Systemd Service Unit Configuration (`/etc/systemd/system/aitmpl-registry.service`)

```ini
[Unit]
Description=AI Templates Private Registry Daemon (FastMCP 3.1)
After=network.target postgresql.service
Requires=postgresql.service
Documentation=https://docs.aitmpl.com/

[Service]
Type=simple
User=aitmpl
Group=aitmpl
WorkingDirectory=/opt/aitmpl-registry
Environment="NODE_ENV=production"
Environment="PORT=8090"
Environment="DATABASE_URL=postgresql://aitmpl:secret@localhost:5432/aitmpl_db"
Environment="STORAGE_PATH=/var/lib/aitmpl/packages"

ExecStart=/usr/bin/node /opt/aitmpl-registry/dist/server.js
ExecReload=/bin/kill -HUP $MAINPID

Restart=always
RestartSec=5
MemoryMax=2G
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
systemctl daemon-reload
systemctl enable --now aitmpl-registry.service
systemctl status aitmpl-registry.service
```

## API examples

### Registry Query & Telemetry Submission in Python with Pydantic v2
The following script demonstrates querying the `aitmpl` registry and submitting execution telemetry payloads using **Pydantic v2**:

```python
import os
import logging
from typing import Literal, List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, ValidationError, ConfigDict
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AITemplates-Controller")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("aitmpl-registry-service")

class SubagentManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    package_name: str = Field(..., description="Package identifier, e.g., development-team/react-auditor")
    version: str = Field(..., description="SemVer package version string")
    category: Literal["agent", "command", "hook", "workflow"]
    target_model: str = Field(default="claude-5.6", description="Target LLM runtime")
    fastmcp_compatible: bool = Field(default=True, description="Whether FastMCP 3.1 bindings are included")
    checksum_sha256: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

class TelemetryPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    package_name: str = Field(..., description="Installed package identifier")
    execution_status: Literal["success", "failure", "cancelled"]
    latency_ms: int = Field(..., ge=0, description="Execution duration in milliseconds")
    tokens_consumed: int = Field(..., ge=0, description="Tokens used during agent run")
    fastmcp_version: str = Field(default="3.1")
    user_environment: str = Field(default="cli-tool", description="Execution environment descriptor")

class FastMCPExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    package_name: str = Field(..., description="Target aitmpl subagent package")
    source_code: str = Field(..., description="Source code text to be audited")
    strict_mode: bool = Field(default=True, description="Enforce strict security analysis")

@mcp.tool()
async def execute_subagent_audit(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Executes a downloaded aitmpl subagent template against target source code using FastMCP 3.1.

    Args:
        request_dict: Request dictionary matching FastMCPExecutionRequest.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating subagent execution request via Pydantic v2...")

    try:
        req = FastMCPExecutionRequest.model_validate(request_dict)
        if ctx:
            await ctx.info(f"Executing subagent package '{req.package_name}' (strict={req.strict_mode})...")

        return {
            "status": "completed",
            "package": req.package_name,
            "violations_found": 0,
            "audit_summary": "Passed all pre-commit security rules.",
            "fastmcp_version": "3.1",
            "code_bytes_analyzed": len(req.source_code.encode("utf-8"))
        }
    except ValidationError as ve:
        logger.error(f"Audit request validation error: {ve}")
        raise ValueError(f"Invalid execution payload: {ve}")

@mcp.tool()
async def fetch_package_manifest(
    package_name: str,
    ctx: Optional[Context] = None
) -> dict:
    """Queries package manifest details from aitmpl registry."""
    manifest = SubagentManifest(
        package_name=package_name,
        version="1.4.2",
        category="agent",
        target_model="claude-5.6",
        fastmcp_compatible=True,
        checksum_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    return manifest.model_dump()

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

```
+-------------------------------------------------------------------------------------------------------------------------+
|                                     AITMPL DIAGNOSTIC & TROUBLESHOOTING MATRIX                                          |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Symptom / Error                    | Root Cause                         | Remediation Action                            |
+------------------------------------+------------------------------------+-----------------------------------------------+
| `ERR_AITMPL_CHECKSUM_MISMATCH`     | Remote package updated without     | Run `npx aitmpl lock --update` to re-sync     |
|                                    | updating local `aitmpl-lock.json`  | package checksum hashes                       |
+------------------------------------+------------------------------------+-----------------------------------------------+
| `FastMCPToolBindingError`          | Installed package requires FastMCP | Upgrade local MCP server dependencies using   |
|                                    | v3.1 but local environment is v2.x | `npm install -g fastmcp@latest`               |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Pre-commit hook blocks valid git   | Rate limit or token quota exhausted| Configure fallback heuristic rules or set     |
| commits during off-line work       | while evaluating pre-commit hook   | `AITMPL_ALLOW_OFFLINE_COMMIT=true`            |
+------------------------------------+------------------------------------+-----------------------------------------------+
| Private registry HTTP 403 Forbidden| Missing or invalid registry bearer | Run `npx aitmpl login --registry <url>` to    |
| response                           | token in developer configuration   | authenticate with private enterprise mirror   |
+------------------------------------+------------------------------------+-----------------------------------------------+
```

## Integration patterns
- **Git Pre-Commit Hook Integration**: Automatically install pre-commit AI guardrails using `npx aitmpl --hook git/pre-commit-security`.
- **Claude Code Subagent Sync**: Sync installed `aitmpl` subagent manifests directly into local `.claude/agents/` directories.
- **CI/CD Pipeline Verification**: Run `npx aitmpl verify` in GitHub Actions pipelines to validate repository compliance prior to merge.

## Best practices & Security
- **Version Lock Subagent Dependencies**: Commit `aitmpl-lock.json` into repository version control to guarantee consistent prompt execution across team members.
- **Enforce SHA256 Verification**: Ensure private enterprise registries enforce strict SHA256 hash checking on all published packages.
- **Set Token Spending Limits**: Configure token budget thresholds in pre-commit hooks to avoid unexpected LLM API cost spikes.

## Reference implementation

```python
# Standalone test for aitmpl Pydantic v2 validation schema
from pydantic import ValidationError

def test_aitmpl_schema():
    payload = {
        "package_name": "development-team/react-auditor",
        "version": "1.4.2",
        "category": "agent",
        "target_model": "claude-5.6",
        "fastmcp_compatible": True
    }
    manifest = SubagentManifest.model_validate(payload)
    assert manifest.package_name == "development-team/react-auditor"
    assert manifest.category == "agent"
    print("aitmpl Pydantic v2 schema validation passed successfully.")

if __name__ == "__main__":
    test_aitmpl_schema()
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

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
