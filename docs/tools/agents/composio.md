# Composio

## What it is
Composio is an enterprise tool integration, OAuth management, and action execution middleware platform designed to connect autonomous AI agents with over 250+ SaaS applications, local utilities, and infrastructure endpoints. In early 2027, Composio functions as an essential execution layer between agent reasoning loops ([Claude 5.6](../providers/anthropic.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../providers/google-ai-studio.md), [DeepSeek-V4](../providers/deepseek.md)) and physical REST/GraphQL/gRPC endpoints. It natively supports **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1 Task Protocol** specifications, handling token refreshes, rate limits, permission boundaries, and audit logging.

## What problem it solves
Connecting autonomous agents to external software services (GitHub, Slack, Salesforce, Jira, Google Workspace) traditionally requires writing thousands of lines of fragile boilerplate code to manage OAuth authentication, refresh tokens, encryption, rate limits, and payload transformations. Composio eliminates this friction by providing a managed integration layer that translates high-level agentic intents into verified, secure API execution calls—ensuring agents never expose raw credential secrets.

## Where it fits in the stack
**Layer 6: Agents & Orchestration** — specifically as **Managed Tool Integration, Authentication, and Action Middleware**. It links agent frameworks ([Agno](./agno.md), [CrewAI](../frameworks/crewai.md), [LangGraph](../frameworks/langgraph.md), [Bee Agent Framework](./bee-agent-framework.md)) with downstream SaaS APIs.

## Architecture Diagram
```
+-----------------------------------------------------------------------------------+
|                              Composio Integration Platform                        |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Agent Reasoning Engine (Claude 5.6, GPT-5.6, DeepSeek-V4, Agno, CrewAI)     |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | FastMCP 3.1 / MCP 3.1 Protocol Server & Tool Router                          |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Managed Auth Vault (OAuth2 Refresh, Token Encryption, Permission Scopes)     |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | 250+ Downstream SaaS Integrations (GitHub, Slack, Jira, Gmail, Salesforce)   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Autonomous Software Engineering**: Connecting agents to Gitea/GitHub and Linear to manage bug tickets, push feature commits, and open pull requests.
- **Enterprise Operations Co-Pilot**: Linking Google Workspace and Slack to handle scheduling, draft team announcements, and organize file archives.
- **Automated Sales & CRM Operations**: Enabling lead qualification agents to search Salesforce records, update sales pipeline stages, and send calendar invites.
- **DevOps & Infrastructure Remediation**: Triggering automated cloud resource scaling or diagnostic runs based on incident webhook alerts.

## Strengths
- **Massive Tool Library**: Pre-built integrations for over 250+ cloud services and local developer utilities.
- **Managed Auth & Token Lifecycle**: Handles OAuth2 consent flows, token refreshes, and secret storage out of the box.
- **Native FastMCP 3.1 Support**: Direct compatibility with Model Context Protocol standards for low-latency tool execution.
- **Framework Agnostic**: Integrates seamlessly with Agno, CrewAI, LangGraph, Bee Agent Framework, and custom Python runtimes.

## Limitations
- **External Gateway Dependency**: Hosted tool calls transit through Composio infrastructure, requiring compliance evaluation for strict data-residency environments.
- **Vendor-Specific Schemas**: Relies on Composio tool definitions (though open SDKs are available for custom extensions).

## When to use it
- When your AI agent requires multi-app SaaS interactions without building custom authentication pipelines.
- When you require complete audit trails and security permission boundaries for every action an agent executes.
- When orchestrating tools under standard FastMCP 3.1 specifications.

## When not to use it
- For simple standalone scripts that only query 1-2 internal databases with hardcoded credentials.
- In strict air-gapped environments that prohibit external integration gateways.

## Getting started

### Installation
```bash
pip install composio-core composio-anthropic fastmcp pydantic
```

### Basic Usage with Claude 5.6
```python
from composio_anthropic import ComposioToolSet, App
from anthropic import Anthropic

# Initialize clients
client = Anthropic()
toolset = ComposioToolSet(api_key="COMPOSIO_API_KEY")

# Retrieve GitHub tools formatted for FastMCP 3.1
tools = toolset.get_tools(apps=[App.GITHUB], protocol="fastmcp3.1")

# Request action from Claude
response = client.messages.create(
    model="claude-5-6-sonnet",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Create an issue titled 'Memory Leak' in repo 'org/backend'."}],
    tools=tools
)

# Execute resulting tool call via Composio
result = toolset.handle_tool_calls(response)
print("Execution Result:", result)
```

## CLI examples
```bash
# Login to Composio CLI
composio login

# Connect GitHub account via OAuth
composio add github

# List connected integrations and auth status
composio list

# Execute a tool action directly from CLI
composio run github star-repo --params '{"owner": "composiohq", "repo": "composio"}'
```

## API examples
The following Python script demonstrates validating Composio tool connection telemetry and action execution logs using Pydantic v2 and FastMCP 3.1:

```python
from typing import Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from fastmcp import FastMCP

# 1. Initialize FastMCP 3.1 Server
mcp = FastMCP(name="composio-audit-server", version="3.1")

# 2. Define Pydantic v2 Telemetry Models
class AuthStateSchema(BaseModel):
    app_name: str = Field(..., description="Target app name (e.g., github, slack)")
    authenticated: bool = Field(default=False)
    auth_method: Literal["oauth2", "api_key", "jwt"] = Field("oauth2")

class ActionExecutionSchema(BaseModel):
    action_id: str = Field(..., description="Specific action string")
    status: Literal["success", "failed", "rate_limited", "unauthorized"]
    latency_ms: float = Field(..., ge=0.0)
    response_payload: Dict[str, Any] = Field(default_factory=dict)

class ComposioAuditLogSchema(BaseModel):
    trace_id: str = Field(..., description="Unique audit trace identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    connection: AuthStateSchema
    execution: ActionExecutionSchema
    mcp_version: str = Field("3.1")

    @field_validator("mcp_version")
    @classmethod
    def validate_mcp_ver(cls, v: str) -> str:
        if v not in {"3.0", "3.1"}:
            raise ValueError("Supported MCP versions are 3.0 or 3.1")
        return v

# 3. FastMCP Tool Endpoint for Telemetry Validation
@mcp.tool(name="record_audit_log", description="Record and validate Composio action execution telemetry")
def record_audit_log(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and record Composio tool execution logs."""
    try:
        validated_log = ComposioAuditLogSchema.model_validate(payload)
        return {
            "success": True,
            "trace_id": validated_log.trace_id,
            "app_name": validated_log.connection.app_name,
            "action": validated_log.execution.action_id,
            "status": validated_log.execution.status,
            "recorded_at": validated_log.timestamp.isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    sample_audit = {
        "trace_id": "comp-trace-88219",
        "connection": {
            "app_name": "github",
            "authenticated": True,
            "auth_method": "oauth2"
        },
        "execution": {
            "action_id": "GITHUB_CREATE_ISSUE",
            "status": "success",
            "latency_ms": 185.4,
            "response_payload": {"issue_id": 102, "url": "https://github.com/org/repo/issues/102"}
        },
        "mcp_version": "3.1"
    }

    print("Validating Composio audit log payload...")
    res = record_audit_log(sample_audit)
    print("Validation Result:", res)
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol standard for tool execution.
- [Zapier](../automation_orchestration/zapier.md) — Workflow automation platform.
- [Make](../automation_orchestration/make.md) — Visual automation tool.
- [CrewAI](../frameworks/crewai.md) — Multi-agent orchestration framework.
- [Agno](./agno.md) — Lightweight agent framework.

## Sources / references
- [Composio Official Site](https://composio.dev/)
- [Composio GitHub Repository](https://github.com/composiohq/composio)
- [Composio Documentation](https://docs.composio.dev/)
- [FastMCP 3.1 Integration Guide](https://docs.composio.dev/protocols/fastmcp3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
