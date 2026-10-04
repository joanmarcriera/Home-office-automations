# Roo Code

## What it is
Roo Code is an open-source, AI-powered autonomous coding agent operating natively across VS Code, JetBrains IDEs, and CLI workflows. Originally forked from Cline, Roo Code has evolved into a highly customizable agentic platform distinguished by its native support for specialized "Custom Modes" (`.roomodes`), multi-model orchestration, and deep Model Context Protocol (**MCP 3.1** / **FastMCP 3.1**) integration. As of early 2027, Roo Code is widely adopted across software engineering teams for its high feature velocity, open-governance model, and flexible orchestration across frontier models such as Anthropic Claude 5.1, OpenAI GPT-5.5/GPT-5.6, Google Gemini 4.0 Pro, DeepSeek-V4, and local models via Ollama and vLLM.

## Architecture & System Topology
Roo Code operates as an event-driven agentic loop running inside the IDE extension host or CLI runner process. It coordinates context management, prompt synthesis, model dispatch, FastMCP tool execution, and user feedback loops through a layered component hierarchy.

```
+----------------------------------------------------------------------------------------------------+
|                                    ROO CODE SYSTEM ARCHITECTURE                                   |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  |                                IDE USER INTERFACE & SIDEBAR PANEL                            |  |
|  |  +---------------------------+  +---------------------------+  +--------------------------+  |  |
|  |  | Mode Selector             |  | Chat & Action View        |  | Context Pinning Window   |  |  |
|  |  | (Code/Architect/Ask/Custom) |  | (Diff Preview/Approval)   |  | (Pinned Files & Docs)    |  |  |
|  |  +-------------+-------------+  +-------------+-------------+  +------------+-------------+  |  |
|  +----------------|------------------------------|-----------------------------|----------------+  |
|                   |                              |                             |                   |
|  +----------------V------------------------------V-----------------------------V----------------+  |
|  |                                  AGENT CORE ORCHESTRATOR                                     |  |
|  |                                                                                              |  |
|  |  +-----------------------+   +----------------------------+   +---------------------------+  |  |
|  |  | Mode Resolution Engine|   | Context Window Manager     |   | Safety & Governance Policy|  |  |
|  |  | (.roomodes Configuration)| | (Token Truncation & Pinned)| | (Command & Edit Approval)|  |  |
|  |  +-----------+-----------+   +-------------+--------------+   +-------------+-------------+  |  |
|  +--------------|-------------------------|--------------------------------|--------------------+  |
|                 |                         |                                |                       |
|  +--------------V-------------------------V--------------------------------V--------------------+  |
|  |                                  MODEL & TOOL BUS INTERFACE                                  |  |
|  |                                                                                              |  |
|  |  +---------------------------------------+    +-------------------------------------------+  |  |
|  |  | LLM Provider Router                   |    | FastMCP 3.1 Protocol Client               |  |  |
|  |  | (Claude 5.1 / GPT-5.5 / DeepSeek-V4)  |    | (JSON-RPC / SSE Transport / Tool Discovery)|  |  |
|  |  +-------------------+-------------------+    +---------------------+---------------------+  |  |
|  +----------------------|------------------------------------------|----------------------------+  |
|                         |                                          |                               |
|                         V                                          V                               |
|        +---------------------------------+        +----------------------------------+             |
|        | LLM APIs & Provider Endpoints   |        | External FastMCP 3.1 Tool Servers|             |
|        | (Anthropic / OpenAI / DeepSeek) |        | (DBs / CI Pipelines / Security)  |             |
|        +---------------------------------+        +----------------------------------+             |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

## What problem it solves
Roo Code eliminates cognitive fatigue and context-switching overhead in software engineering workflows by embedding an autonomous reasoning loop directly into the code editor. Key problem areas resolved include:

1. **Generalist Model Fatigue**: Standard coding assistants apply generic system prompts across all tasks. Roo Code solves this via **Custom Modes**, allowing specialized personas (e.g., Security Auditor, API Architect, System Refactoring Specialist) with constrained tool access and distinct system prompts.
2. **Disconnected Tooling**: Engineering workflows require interacting with databases, terminal sessions, browser viewports, and internal cloud APIs. Roo Code connects these systems through **FastMCP 3.1**, allowing LLMs to safely invoke real-time tools.
3. **Unchecked Agent Actions**: Unrestricted terminal execution and file modification present severe operational risks. Roo Code enforces human-in-the-loop checkpoint approvals, granular mode permissions, and visual git-diff previews prior to committing edits.
4. **Context Saturation & Hallucination**: Massive codebases exhaust model context limits. Roo Code leverages active context pinning, intelligent file-tree indexing, and dynamic snippet injection to maintain high reasoning precision over extended multi-step sessions.

## Where it fits in the stack
**Agent / IDE Extension / CLI / FastMCP Client**. Roo Code functions as the command-and-control interface sitting between the software engineer, local filesystem workspace, terminal subsystem, and remote model infrastructure.

```
+-----------------------------------------------------------------------+
|                         DEVELOPER WORKSPACE                           |
+-----------------------------------------------------------------------+
|  [Engineer Interface] -> VS Code / JetBrains / CLI                    |
|          |                                                            |
|          V                                                            |
|  [Roo Code Core Agent] <---> [.roomodes Persona Definitions]           |
|          |                                                            |
|          +--------------------------+--------------------------+      |
|          | (FastMCP 3.1)            | (System APIs)            |      |
|          V                          V                          V      |
|  [FastMCP Tool Servers]     [Local Filesystem]        [Terminal / Shell] |
|  (Databases / K8s / CI)     (Source / Schemas)        (Tests / Builds)  |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Multi-Phase Architecture & Implementation**: Utilizing "Architect Mode" to formulate system specifications, API signatures, and entity relationship diagrams, then seamlessly transitioning to "Code Mode" to generate implementation files and unit test suites.
- **Automated Refactoring & Framework Upgrades**: Delegating major language version upgrades (e.g., TypeScript 5.x migrations, Python async refactoring) to Roo Code with automated test execution loops that fix regressions in real time.
- **Targeted Security & Vulnerability Auditing**: Switch to a dedicated "Auditor Mode" configured with read-only filesystem access and static analysis MCP tools to audit code for SQL injection, hardcoded credentials, and OWASP Top 10 risks.
- **FastMCP 3.1 Tool Integration**: Wiring internal organizational microservices, diagnostic log streams, and monitoring tools into Roo Code via FastMCP servers to enable real-time debugging during local development.
- **Automated Verification & UI Testing**: Harnessing Roo Code's embedded browser tool group to execute visual regressions, capture UI snapshots, and verify frontend rendering against design specs.

## Strengths
- **Granular Custom Modes**: Define custom personas in `.roomodes` with explicit tool group permissions (e.g., `read`, `edit`, `execute`, `browser`, `mcp`), ensuring agents only execute authorized actions.
- **Native FastMCP 3.1 Protocol Support**: Fast, streaming RPC connection to MCP tools with support for dynamic tool discovery, binary transports, and progress notifications.
- **Frontier & Open Model Versatility**: Optimized prompt strategies for Claude 5.1, GPT-5.5/GPT-5.6, DeepSeek-V4, Gemini 4.0 Pro, and local Ollama/vLLM endpoints.
- **Interactive Diff Inspection**: Generates clear line-by-line diffs before making edits, allowing developers to accept, reject, or request adjustments on individual file modifications.
- **Context Pinning & Memory Control**: Explicitly pin files, images, workspace directories, and documentation URLs into the prompt context to keep critical architectural rules active across multi-turn sessions.

## Limitations
- **High Context Token Consumption**: Complex iterative agentic loops that read multiple files and execute terminal commands rapidly consume large context windows, increasing API costs.
- **Initial Setup Overhead**: Configuring enterprise `.roomodes` definitions, custom MCP servers, and granular workspace permission models requires explicit onboarding setup.
- **Rapid Ecosystem Iteration**: Because Roo Code evolves rapidly with community contributions, configuration keys and UI settings receive frequent feature additions.

## When to use it
- When requiring an open-source, highly autonomous agent capable of executing code edits, running terminal commands, and performing visual browser checks in your editor.
- When your engineering organization benefits from specialized modes (e.g., Security, Architecture, Refactoring, Docs) tailored to strict security boundaries.
- When building or leveraging custom FastMCP 3.1 tool servers to connect your IDE agent directly to internal APIs and databases.
- When seeking a multi-provider coding assistant that operates seamlessly across commercial APIs and local open-weight models.

## When not to use it
- For instant single-line code completion where lightweight inline completion tools like GitHub Copilot or Supermaven offer lower latency.
- In locked-down environments where IDE extensions are strictly forbidden from executing shell commands or spawning subprocesses.
- When looking for a zero-configuration, single-turn chatbot that does not interact with the filesystem.

## Getting started

### Installation
1. Search for and install **Roo Code** from the VS Code Marketplace or Open VSX Registry.
2. Open the Roo Code sidebar panel and click the **Settings (Gear)** icon.
3. Select your preferred API Provider (e.g., Anthropic, OpenAI, OpenRouter, DeepSeek, or Ollama).
4. Enter your API key and select your default model (e.g., `claude-5-1-sonnet-20261022` or `deepseek-v4`).

### Workspace Configuration (`.roomodes`)
Create a `.roomodes` file in your repository root to configure project-specific custom modes:

```json
{
  "customModes": [
    {
      "slug": "api-architect",
      "name": "API Architect",
      "roleDefinition": "You are a senior system architect specializing in OpenAPI specifications, FastMCP 3.1 tool interfaces, and Pydantic v2 schemas.",
      "groups": ["read", ["edit", {"fileRegex": "\\.(json|yaml|py|proto)$"}], "mcp"],
      "customInstructions": "Enforce strict schema validation and typing across all API interfaces. Never edit implementation logic directly."
    }
  ]
}
```

## CLI examples

### Running FastMCP 3.1 Tools & Diagnostic Commands
```bash
# Verify local FastMCP 3.1 tool server status and endpoint routing
mcp-server-manager status --verbose

# Launch a local FastMCP 3.1 server for Roo Code integration
python -m mcp_server_database --host 127.0.0.1 --port 8080

# Execute unit tests with JSON reporting for Roo Code auto-fix loops
pytest tests/ --json-report --json-report-file=report.json

# Check environment runtime dependencies required by Roo Code execution sandbox
node --version && python3 --version && git status
```

## API examples

The following Python script demonstrates how to construct a high-performance FastMCP 3.1 tool server that exposes database queries and file verification utilities to Roo Code with streaming progress updates:

```python
import asyncio
from typing import AsyncGenerator, Dict, Any
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

# Initialize FastMCP 3.1 Server for Roo Code Tool Integration
mcp = FastMCP(
    name="RooCodeEnterpriseTools",
    version="3.1.0",
    description="Enterprise diagnostic and database tools for Roo Code agentic workflows"
)

class DatabaseQueryInput(BaseModel):
    query_string: str = Field(..., description="SQL select query string to execute")
    environment: str = Field("development", description="Target environment (development, staging)")
    limit: int = Field(100, ge=1, le=1000, description="Maximum rows to return")

class HealthCheckResult(BaseModel):
    status: str = Field(..., description="Overall health status (healthy, degraded)")
    latency_ms: float = Field(..., description="Service connection latency in milliseconds")
    active_connections: int = Field(..., description="Number of active system connections")

@mcp.tool(name="query_developer_db", description="Executes read-only diagnostic SQL queries against development database")
async def query_developer_db(params: DatabaseQueryInput, ctx: Context) -> Dict[str, Any]:
    """Executes a read-only query with FastMCP 3.1 context reporting."""
    await ctx.report_progress(progress=10, total=100)

    if not params.query_string.strip().lower().startswith("select"):
        raise ValueError("Security violation: Only SELECT queries are permitted in diagnostic mode.")

    await ctx.info(f"Executing query on {params.environment}: {params.query_string[:50]}...")
    await asyncio.sleep(0.1)  # Simulate non-blocking DB IO

    await ctx.report_progress(progress=100, total=100)
    return {
        "status": "success",
        "environment": params.environment,
        "row_count": 2,
        "data": [
            {"id": 101, "service": "auth-service", "status": "active"},
            {"id": 102, "service": "payment-bridge", "status": "active"}
        ]
    }

@mcp.tool(name="stream_system_logs", description="Streams real-time log entries to Roo Code")
async def stream_system_logs(service_name: str, lines: int = 5) -> AsyncGenerator[str, None]:
    """FastMCP 3.1 streaming tool output pattern."""
    for i in range(1, lines + 1):
        await asyncio.sleep(0.05)
        yield f"[LOG {service_name}] Line {i}: Service health normal. Processing batch {i * 10}.\n"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## API & Schema Definitions (Pydantic v2)

Roo Code relies on structured data schemas for mode definitions, tool permissions, and context session management. The following Pydantic v2 models define the complete operational configuration:

```python
from enum import Enum
from typing import List, Dict, Union, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class ToolGroupPermission(str, Enum):
    READ = "read"
    EDIT = "edit"
    EXECUTE = "execute"
    BROWSER = "browser"
    MCP = "mcp"

class FileRegexPermission(BaseModel):
    file_regex: str = Field(..., alias="fileRegex", description="Regex pattern matching allowable file paths")

    model_config = ConfigDict(populate_by_name=True)

class CustomModeDefinition(BaseModel):
    slug: str = Field(..., description="Unique slug for the mode (e.g. 'security-auditor')")
    name: str = Field(..., description="Display title in IDE selector")
    role_definition: str = Field(..., alias="roleDefinition", description="Core system prompt persona instructions")
    groups: List[Union[ToolGroupPermission, FileRegexPermission, str]] = Field(
        ..., description="Tool group permissions or fine-grained regex rules"
    )
    custom_instructions: Optional[str] = Field(None, alias="customInstructions", description="Project-specific guidelines")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("slug")

    def validate_slug(cls, v: str) -> str:
        if not v.islower() or " " in v:
            raise ValueError("Mode slug must be lowercase and hyphenated without spaces.")
        return v

class MCPServerConfig(BaseModel):
    command: str = Field(..., description="Executable binary name or path (e.g., 'python', 'node')")
    args: List[str] = Field(default_factory=list, description="Command line arguments passed to MCP server")
    env: Dict[str, str] = Field(default_factory=dict, description="Environment variables for the process")
    disabled: bool = Field(False, description="Toggle whether server is active in workspace")

class RooWorkspaceSettings(BaseModel):
    custom_modes: List[CustomModeDefinition] = Field(default_factory=list, alias="customModes")
    mcp_servers: Dict[str, MCPServerConfig] = Field(default_factory=dict, alias="mcpServers")
    auto_approval_enabled: bool = Field(False, alias="autoApprovalEnabled", description="Master switch for automated command execution")
    allowed_commands: List[str] = Field(default_factory=list, alias="allowedCommands", description="Whitelist of terminal command patterns allowed without prompt")

    model_config = ConfigDict(populate_by_name=True)
```

## Related tools / concepts
- [Cline](cline.md) — The core open-source coding agent framework from which Roo Code originated.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open protocol standard for model tools and context servers.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's terminal-native agent for software development.
- [Aider](../development_ops/aider.md) — Command-line git-integrated pair programming agent.
- [Windsurf](../development_ops/windsurf.md) — Agentic IDE environment with flow paradigm.
- [Local LLMs](../ai_knowledge/local_llms.md) — Comprehensive guide for serving local open models.
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — TypeScript library for agentic workflows.
- [Playwright](../development_ops/playwright.md) — Browser automation engine powering Roo Code browser tools.

## Sources / references
- [Roo Code Official GitHub Repository](https://github.com/RooCodeInc/Roo-Code)
- [Roo Code Official Documentation](https://docs.roocode.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
