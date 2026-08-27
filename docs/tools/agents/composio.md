# Composio

## What it is
Composio (v1.5+, early January 2027) is an enterprise-grade tool integration and authentication middleware platform that connects AI agents to over 250+ external SaaS applications, local utilities, and infrastructure services. Serving as a robust bridge between agentic frameworks and actual API execution endpoints, it manages complex OAuth handshakes, API tokens, and secret storage. It features first-class native compatibility with the [Model Context Protocol (MCP) 3.1](../../knowledge_base/agent_protocols.md) and FastMCP 3.1 Task Protocol, enabling low-latency tool execution and standardized routing for early 2027 models like [Claude 5.6](../providers/anthropic.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../providers/google.md), and local options like [Gemma 4](../ai_knowledge/local_llms.md).

## What problem it solves
Giving agents raw access to APIs normally requires writing and maintaining thousands of lines of boilerplate code to handle authentication (OAuth flow redirection, token refresh cycles, encryption), rate-limiting, and payload mapping. Composio completely abstracts this middleware layer. It provides instant, safe connections to popular tools (e.g., GitHub, Slack, Jira, Gmail) while offering developers comprehensive telemetry, permission boundaries, and audit logs of all actions initiated by autonomous agent sessions.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as **Tool Integration, Managed Auth, and Action Middleware** mapping high-level agentic intents to verified physical API schemas.

## Typical use cases
- **Autonomous Engineering Run**: Integrating with version control software and task managers (GitHub, Linear, Jira) to let [Symphony](./symphony.md) agents pull bugs, create feature branches, write code, run CI tests, and submit PRs.
- **Enterprise Executive Co-Pilot**: Linking schedule platforms, corporate messaging boards, and mailservers (Google Workspace, Slack, Outlook) to manage complex cross-organizational communications.
- **Dynamic CRM Management**: Allowing sales-coordination agents to inspect Salesforce records, update pipeline statuses, and dispatch calendar invitations.
- **High-Frequency Local DevOps**: Connecting local scripting hosts with [FastMCP 3.1](../../knowledge_base/patterns/data-copilot-mcp-tooling.md) servers to execute local commands with fine-grained permission control.

## Strengths
- **Huge Pre-built Library**: 250+ instant cloud and local app integrations.
- **Managed Auth & OAuth Handshakes**: Complete secure storage of user access tokens with automated refreshes, meaning agents never handle raw secrets.
- **FastMCP 3.1 Native**: Native support for high-efficiency Model Context Protocol specifications.
- **Framework Agnostic**: Integrates seamlessly with [Agno](./agno.md), [Bee Agent Framework](./bee-agent-framework.md), [CrewAI](../frameworks/crewai.md), and [LangGraph](../frameworks/langgraph.md).

## Limitations
- **Transit Dependency**: High-volume hosted tool calls transit through Composio's API gateways, which might present compliance concerns.
- **Vendor Lock**: Relies on Composio's proprietary schemas and tooling platforms (though open-source client SDKs are available).
- **Service Outage Propagation**: If Composio or a specific downstream SaaS integration goes down, the agent loses physical tool-use capability.

## When to use it
- When your agents need to interact with multiple complex SaaS ecosystems without your team building custom OAuth integrations.
- To maintain deep observability and audit trails of exactly what actions, parameters, and tokens your agent executed.
- When orchestrating tools under standard **MCP 3.1** or **FastMCP 3.1** protocols.

## When not to use it
- For basic agents requiring only 1 or 2 custom in-house database tools that do not require third-party SaaS authentication.
- In hyper-secure, air-gapped environments that forbid routing tool payloads through external orchestrator APIs.
- When you require complete, end-to-end local ownership of the tool execution infrastructure.

## Getting started
### Installation
```bash
pip install composio-core composio-anthropic pydantic
```

### Basic Usage
Initialize Composio toolsets to equip a Claude 5.1 assistant with native GitHub execution tools:
```python
from composio_anthropic import ComposioToolSet, App
from anthropic import Anthropic

# 1. Initialize core clients
client = Anthropic()
toolset = ComposioToolSet(api_key="COMPOSIO_API_KEY")

# 2. Retrieve GitHub tools formatted for FastMCP 3.1
tools = toolset.get_tools(apps=[App.GITHUB], protocol="fastmcp3.1")

# 3. Create agent message requesting repository interaction
response = client.messages.create(
    model="claude-5-6-sonnet",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Create a new issue titled 'Database connection leak' in the repository 'my-org/backend'."}],
    tools=tools
)

# 4. Handle and execute the resulting tool call via Composio
result = toolset.handle_tool_calls(response)
print(result)
```

## CLI examples
```bash
# Authenticate your terminal session with the Composio service
composio login

# Connect your corporate GitHub account via OAuth (triggers browser redirect)
composio add github

# List all connected integrations and their current authorization states
composio list

# Execute a single integration action directly from the command line for testing
composio run github star-repo --params '{"owner": "composiohq", "repo": "composio"}'
```

## API examples
### Composio Connection and Tool Audit Tracing (Pydantic v2)
To maintain security compliance, enterprise agent systems require strict schema verification of all external connections and tool execution logs. The following script demonstrates validating connection and execution telemetry from Composio using Pydantic v2:

```python
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class AuthState(BaseModel):
    app_name: str = Field(..., description="Target application name")
    authenticated: bool = Field(False)
    auth_method: Literal["oauth2", "api_key", "basic", "jwt"] = Field("oauth2")
    last_refresh: Optional[datetime] = Field(None)

class ActionExecution(BaseModel):
    action_id: str
    status: Literal["success", "failed", "rate_limited", "unauthorized"]
    response_payload: Dict[str, Any] = Field(default_factory=dict)
    latency_ms: float = Field(..., ge=0.0)

class ComposioAuditLog(BaseModel):
    trace_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    connection: AuthState
    execution: Optional[ActionExecution] = Field(None)
    mcp_protocol_version: str = Field("3.1")

    @field_validator("mcp_protocol_version")
    @classmethod
    def validate_mcp_ver(cls, val: str) -> str:
        if val not in {"3.0", "3.1"}:
            raise ValueError("Supported MCP protocol versions must be 3.0 or 3.1")
        return val

# Sample telemetry from a Composio tool-calling hook
telemetry_data = {
    "trace_id": "comp-trace-77421",
    "connection": {
        "app_name": "github",
        "authenticated": True,
        "auth_method": "oauth2",
        "last_refresh": "2026-12-05T09:00:00Z"
    },
    "execution": {
        "action_id": "GITHUB_CREATE_ISSUE",
        "status": "success",
        "response_payload": {"issue_number": 421, "url": "https://github.com/my-org/backend/issues/421"},
        "latency_ms": 234.5
    },
    "mcp_protocol_version": "3.1"
}

# Strictly validate the telemetry payload
validated_log = ComposioAuditLog(**telemetry_data)
print(f"Validated Audit Log ID: {validated_log.trace_id}")
print(f"Tool executed: {validated_log.execution.action_id} (Status: {validated_log.execution.status})")
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Zapier](../automation_orchestration/zapier.md)
- [Make](../automation_orchestration/make.md)
- [CrewAI](../frameworks/crewai.md)
- [LangGraph](../frameworks/langgraph.md)
- [Agno](./agno.md)
- [Bee Agent Framework](./bee-agent-framework.md)

## Sources / references
- [Official Website](https://composio.dev/)
- [GitHub Repository](https://github.com/composiohq/composio)
- [Composio Documentation](https://docs.composio.dev/)
- [FastMCP 3.1 Integration Reference](https://docs.composio.dev/protocols/fastmcp3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
