# ClawHub

## What it is
ClawHub is a central public marketplace and registry for autonomous agent skills, MCP (Model Context Protocol) tool servers, and workflow extensions designed for agentic runtimes like [OpenClaw](../development_ops/openclaw.md) and [Claude Code](../development_ops/claude-code.md). It enables developers and AI agents to discover, publish, audit, and dynamically install modular capabilities to expand the functional scope of local and cloud-based AI assistants.

## What problem it solves
As agentic ecosystems proliferate, discovering and integrating verified tool-calling capabilities across disparate repositories becomes fragmented and error-prone. ClawHub standardizes package distribution, versioning, security auditing, and schema declarations for agent skills, allowing AI models (including Claude 5.6, GPT-5.6, and Qwen 3.6) to install and invoke external tools safely on demand.

## Where it fits in the stack
**AI & Knowledge / Skill Registry & Ecosystem Portal**. It functions at the Ecosystem & Extension layer, interfacing between autonomous agent runtimes (such as [OpenClaw](../development_ops/openclaw.md) or [NanoClaw](../development_ops/nanoclaw.md)) and external APIs/services via standardized Model Context Protocol (MCP 3.1) definitions.

## Typical use cases
- **Dynamic Skill Ingestion**: Allowing an active autonomous agent to search ClawHub and install a domain-specific MCP tool server mid-task.
- **Skill Publishing**: Developers sharing re-usable agent skill packages (e.g., CRM integrations, IoT control, financial analytics) with structured Pydantic schemas.
- **Enterprise Governance**: Auditing third-party agent skills and enforcing zero-trust sandboxing rules before enabling tools in production pipelines.
- **Cross-Agent Capability Sharing**: Re-using skills across heterogeneous frameworks such as [Agency Swarm](../agents/agency-swarm.md), [Agno](../agents/agno.md), and [OpenClaw](../development_ops/openclaw.md).

## Strengths
- **Standardized MCP 3.1 Integration**: Built natively around Model Context Protocol and FastMCP specs.
- **Ecosystem Interoperability**: Compatible with major agentic runtimes including OpenClaw, Claude Code, and Custom Agents.
- **Public & Private Registries**: Supports both open community skill discovery and private enterprise-hosted skill indexes.
- **Automated Schema Verification**: Validates tool inputs and response models against strict schema specifications.

## Limitations
- **Security Risks**: Dynamically downloading third-party skills requires robust local sandboxing to prevent prompt injection or code execution exploits.
- **Ecosystem Maturity**: Rapidly evolving MCP specifications require frequent updates to published skill packages.
- **Dependency Overhead**: Complex skills may introduce nested runtime requirements (Node.js, Python, Docker).

## When to use it
- When building modular AI agents that need to extend their capability set dynamically without hardcoding every tool into system prompts.
- When publishing reusable MCP tool integrations for the broader AI developer community.
- When establishing an enterprise repository of vetted agent tools.

## When not to use it
- For static, single-purpose AI pipelines where fixed function definitions suffice.
- In fully air-gapped environments without private ClawHub mirror infrastructure.
- When zero dynamic code/configuration loading is mandated by strict security compliance.

## Getting started

### Installing the ClawHub CLI
The ClawHub CLI manages skill installation and registry authentication:

```bash
# Install globally via npm
npm install -g @clawhub/cli

# Or run via npx
npx @clawhub/cli list
```

### Searching and Installing Skills
```bash
# Search for published MCP skills
clawhub search "calendar"

# Install a skill into the local agent environment
clawhub install @clawhub/google-calendar-mcp
```

## CLI examples

### Login and Publish a Custom Agent Skill
```bash
# Authenticate with ClawHub registry
clawhub login

# Validate and publish a local skill package
clawhub publish ./my-custom-skill
```

### Inspecting Installed Agent Skills
```bash
# List all active skills in the current workspace
clawhub status
```

## API examples

### Python (Skill Metadata Validation with Pydantic v2)
The following example demonstrates querying the ClawHub registry API and validating skill definitions using strict **Pydantic v2** schemas before execution in an [OpenClaw](../development_ops/openclaw.md) pipeline.

```python
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class SkillToolSchema(BaseModel):
    name: str = Field(..., description="Name of the MCP tool function")
    description: str = Field(..., description="Tool description provided to the LLM")
    parameters_schema: dict = Field(..., description="JSON Schema for tool arguments")

class ClawHubSkillPackage(BaseModel):
    id: str = Field(..., description="Unique skill package identifier")
    name: str = Field(..., description="Human-readable skill name")
    version: str = Field(..., description="Semantic version string")
    repository_url: HttpUrl = Field(..., description="Source repository link")
    verified: bool = Field(False, description="Whether skill passes security auditing")
    tools: List[SkillToolSchema] = Field(default_factory=list)

class ClawHubSearchResponse(BaseModel):
    query: str
    total_results: int
    skills: List[ClawHubSkillPackage]

async def fetch_and_validate_skill(skill_id: str) -> ClawHubSkillPackage:
    # Simulated API response from ClawHub registry
    simulated_payload = {
        "id": "clawhub-dex-crm",
        "name": "Dex Personal CRM MCP",
        "version": "1.4.0",
        "repository_url": "https://github.com/dex-crm/mcp-server",
        "verified": True,
        "tools": [
            {
                "name": "search_contacts",
                "description": "Search personal CRM contacts by name or query",
                "parameters_schema": {"type": "object", "properties": {"query": {"type": "string"}}}
            }
        ]
    }

    validated_skill = ClawHubSkillPackage.model_validate(simulated_payload)
    return validated_skill

if __name__ == "__main__":
    skill = asyncio.run(fetch_and_validate_skill("clawhub-dex-crm"))
    print(f"Validated Skill: {skill.name} v{skill.version} (Verified: {skill.verified})")
    for t in skill.tools:
        print(f" - Tool: {t.name}: {t.description}")
```

### FastMCP Tool Registration Fragment
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ClawHub Extension Runtime")

@mcp.tool()
def search_clawhub_skills(category: str) -> str:
    """Searches ClawHub public marketplace for verified skills matching category."""
    return f"Found 3 skills in category '{category}'"
```

## Related tools / concepts
- [openclaw](../development_ops/openclaw.md) — Autonomous agent framework integrating ClawHub skills.
- [nanoclaw](../development_ops/nanoclaw.md) — Lightweight, security-sandboxed agent runtime.
- [claude-code](../development_ops/claude-code.md) — Terminal-based agent tool supporting MCP extensions.
- [mcp](../automation_orchestration/mcp.md) — Model Context Protocol foundational standard.
- [mcp-registry](../automation_orchestration/mcp-registry.md) — Official MCP server directory.
- [dex](dex.md) — Personal CRM tool with published ClawHub skills.
- [agency-swarm](../agents/agency-swarm.md) — Multi-agent framework with skill orchestration.

## Sources / references
- [ClawHub Official Marketplace](https://www.clawhub.ai/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
