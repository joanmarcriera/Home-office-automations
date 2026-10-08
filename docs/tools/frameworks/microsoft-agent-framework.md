# Microsoft Agent Framework

## What it is
Microsoft Agent Framework (integrated within **Azure AI Foundry**, **Microsoft AutoGen 0.8+**, and the **Semantic Kernel** ecosystem) is an enterprise-grade suite of libraries and standards for building, orchestrating, and managing multi-agent AI systems. As of early 2027, it serves as a primary backbone for deploying high-autonomy agents in corporate environments, supporting frontier models such as **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro/Ultra**, **DeepSeek-V4**, **Llama 4**, and **Gemma 3**.

## Architecture & Enterprise Multi-Agent Topology
The Microsoft Agent Framework coordinates specialized autonomous agents across Azure enterprise guardrails, connecting agent memory states with FastMCP 3.1 tool gateways and Entra ID identity controls.

```
+---------------------------------------------------------------------------------+
|                             Azure AI Foundry Gateway                            |
|  +------------------+   +-------------------+   +----------------------------+  |
|  | Entra ID Auth    |   | Zero-Trust Access |   | Audit & Compliance Logging |  |
|  +--------+---------+   +---------+---------+   +-------------+--------------+  |
+-----------|-----------------------|---------------------------|-----------------+
            |                       |                           |
            v                       v                           v
+---------------------------------------------------------------------------------+
|                 Microsoft Agent Framework Orchestration Core                    |
|  +---------------------------------------------------------------------------+  |
|  | AgentChat Protocol & Cross-Agent Handoff Engine                           |  |
|  +-------------------------------------+-------------------------------------+  |
|                                        |                                        |
|                                        v                                        |
|  +---------------------------------------------------------------------------+  |
|  | Specialized Agent Roles                                                   |  |
|  |  +---------------------------+   +-------------------------------------+  |  |
|  |  | DevOps Agent (Claude 5.1)   |   | Analyst Agent (GPT-5.6 / DeepSeek)  |  |  |
|  |  +---------------------------+   +-------------------------------------+  |  |
|  +-------------------------------------+-------------------------------------+  |
+----------------------------------------|----------------------------------------+
                                         |
            +----------------------------+----------------------------+
            |                                                         |
            v                                                         v
+---------------------------------------+ +---------------------------------------+
|   Semantic Kernel Plugins & Memory    | |     FastMCP 3.1 Tool Servers          |
|  - Vector Search & Cosmos DB Memory   | |  - Model Context Protocol (MCP 3.1)  |
|  - Enterprise SAP / SQL Drivers       | |  - Microservice Task Execution      |
+---------------------------------------+ +---------------------------------------+
```

## What problem it solves
It simplifies the coordination of multiple LLM-powered agents, providing standardized protocols for communication (via Agent Chat), state management, and long-term memory. It addresses the challenges of "agentic drift," tool-use reliability, and cross-agent consistency that occur when scaling beyond single-prompt interactions in an enterprise context, now fully integrated with the **FastMCP 3.1 Protocol** for standardized, cross-platform task execution.

## Where it fits in the stack
**Category**: Frameworks / Orchestration
It sits between the inference layer (Azure OpenAI Service, Azure AI Foundry, custom local inference) and the application layer, providing the "brain" and "memory" for autonomous workflows. It utilizes **FastMCP 3.1** for ultra-low latency tool hosting and agent discovery.

## Feature Matrix & Enterprise Orchestration Comparison

| Feature | MS Agent Framework | LangGraph | AutoGen 0.8+ | CrewAI |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Enterprise Multi-Agent Suite | Cyclic Graph Agent Flows | Conversational Agent Teams | Role-Playing Agent Teams |
| **Cloud Hosting** | Azure AI Foundry Native | LangGraph Cloud / Self-Host | Ecosystem Agnostic | CrewAI Enterprise Cloud |
| **Identity & Security** | Entra ID (Azure AD), Zero-Trust | Custom OAuth / API Keys | Manual Setup | Team Workspace Auth |
| **Protocol Standards** | AgentChat + FastMCP 3.1 | LangGraph State Graph | Conversational Handoff | Task Delegation Loops |
| **Primary Languages** | C# (.NET), Python | Python, TypeScript | Python, .NET | Python |
| **State Persistence** | Cosmos DB, Azure Blob, SQL | Postgres Checkpointer | SQLite / Custom State | Memory SQLite |

## Operational Best Practices & Governance
1. **Entra ID Role-Based Access**: Restrict agent plugin execution permissions using Microsoft Entra ID managed identities to enforce least-privilege principles across corporate data stores.
2. **Conversation State Checkpointing**: Persist `AgentChat` conversation states in Azure Cosmos DB or Redis to allow agent recovery after system restarts or transient network partitions.
3. **Human-in-the-Loop (HITL) Checkpoints**: Insert explicit approval nodes before triggering destructive FastMCP 3.1 tool calls (such as database migrations or production infrastructure changes).
4. **Token Usage & Cost Monitoring**: Integrate Azure Monitor alerts to track token consumption spikes across multi-agent loops to prevent unexpected billing.

## Typical use cases
- **Multi-agent Collaboration**: Building specialized teams (e.g., a "DevOps Agent" using Claude 5.1 and a "Quality Gate Agent" using DeepSeek-V4) that cooperate on software delivery.
- **Enterprise Research**: Orchestrating research agents that browse internal SharePoint data and external web signals simultaneously.
- **Workflow Automation**: Automating complex, multi-step business processes with native human-in-the-loop (HITL) checkpoints.
- **Legacy Integration**: Using Semantic Kernel "Plugins" to allow agents to safely execute actions against SAP, Salesforce, or custom SQL databases via FastMCP 3.1.

## Strengths
- **Azure AI Foundry Native**: Seamless integration with the latest model catalogs, including native support for DeepSeek-V4, Gemma 3, and Claude 5.1 on Azure.
- **Enterprise Security**: Inherits Azure's robust identity (Entra ID), Zero-Trust Access, data residency, and compliance guardrails.
- **Standardized State Management**: Features a sophisticated `AgentChat` protocol that handles conversation history and state persistence across different providers.
- **FastMCP 3.1 Task Protocol**: Native support for standardized task representations, enabling flawless interoperability with a wide range of external tools.

## Limitations
- **Azure Dependency**: While Semantic Kernel and AutoGen are open-source, the full Agent Framework benefits are most pronounced when locked into the Azure/Microsoft ecosystem.
- **Higher Latency**: The orchestration overhead and enterprise-grade state management can introduce slight latency compared to minimalist frameworks like `smolagents`.
- **API Complexity**: The abstraction layer is deep, which can make debugging "agent-to-agent" handoffs more difficult than in lower-level libraries.

## When to use it
- When building production-grade agents that require strict security, audit logs, and enterprise integration.
- When you need a multi-agent system that leverages both OpenAI, Anthropic, and open-weight models through a unified interface (Azure AI Foundry).
- When you are developing in a .NET or Python enterprise environment with access to FastMCP 3.1 toolsets.

## When not to use it
- For quick, experimental prototypes where a single-file script or a lightweight framework like [CrewAI](crewai.md) would be faster to iterate on.
- If you require a completely ecosystem-agnostic, open-source-only stack without any cloud provider affinity.

## Getting started

### Installation (Python)
Install the core Azure AI agent, identity, and standard Pydantic v2 libraries:

```bash
pip install azure-ai-projects azure-identity semantic-kernel pydantic>=2.0.0
```

### Usage (Hello World Agent - Python)
Configuring a Gemma 3 / DeepSeek-V4 agent within the framework.

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize via Azure AI Foundry connection
project_client = AIProjectClient.from_connection_string(
    conn_str="YOUR_AZURE_FOUNDRY_CONNECTION_STRING",
    credential=DefaultAzureCredential()
)

# Create an agent with Gemma 3
agent = project_client.agents.create_agent(
    model="gemma-3-27b-it",
    name="analyst-agent",
    instructions="Perform deep analysis of the provided data."
)

# Initialize a thread for the conversation
thread = project_client.agents.create_thread()

# Run the agent
run = project_client.agents.create_run(
    thread_id=thread.id,
    assistant_id=agent.id,
    prompt="Summarize the latest trends in agentic orchestration under FastMCP 3.1 standards."
)

print(f"Response: {run.messages[0].text}")
```

## CLI examples

### Azure CLI (Project Management)
Manage your AI Foundry resources and agent definitions.

```bash
# List all AI agents in a specific project
az ai agent list --project-name "EnterpriseAgents" --resource-group "AI-Resources"

# Update an agent's instructions
az ai agent update --name "analyst-agent" --instructions "New system prompt here"
```

### Semantic Kernel CLI
Verify plugin availability and agent state.

```bash
# Check available plugins in the local environment
sk-cli plugin list

# Test a kernel prompt against a specific model
sk-cli prompt run --model "gemma-3" --input "Hello Agent!"
```

## API examples

### FastMCP 3.1 Multi-Agent Tool Gateway (Python)
The following Python script creates a FastMCP 3.1 tool gateway that connects Microsoft Agent Framework orchestrators with enterprise microservices:

```python
import os
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("ms-agent-framework-gateway", version="3.1.0")

class DelegationTask(BaseModel):
    target_agent: str = Field(..., description="Target specialized agent name (e.g., DevOpsAgent, AuditAgent)")
    payload_json: str = Field(..., description="JSON serialized payload for the delegated task")

@mcp.tool()
def delegate_task_to_agent(task: DelegationTask) -> dict:
    """FastMCP 3.1 tool for routing agent-to-agent delegation tasks in Microsoft Agent Framework."""
    # In production, this connects to Azure AI Foundry AgentChat threads
    return {
        "status": "delegated",
        "target_agent": task.target_agent,
        "mcp_version": "3.1",
        "execution_id": "azure_run_99214a"
    }

if __name__ == "__main__":
    mcp.run()
```

### Multi-Agent Handoff (Semantic Kernel) with Pydantic v2 Configuration Validation
Defining a "delegation" pattern between a Researcher and a Writer, validating configurations dynamically.

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class AgentPluginConfig(BaseModel):
    plugin_name: str = Field(..., description="Name of the semantic plugin")
    allowed_methods: List[str] = Field(default_factory=list, description="Methods allowed for agent execution")

class AgentDeploymentConfig(BaseModel):
    agent_name: str = Field(..., description="Display name of the agent")
    model_name: str = Field(..., description="Frontier model targeting, e.g., Claude 5.1, GPT-5.5, or DeepSeek-V4")
    instructions: str = Field(..., description="System prompt instructions")
    plugins: List[AgentPluginConfig] = Field(default_factory=list, description="Associated plugins")
    mcp_version: str = Field("3.1", description="Model Context Protocol spec version")

def load_and_validate_agent(config_json: str) -> Optional[AgentDeploymentConfig]:
    try:
        config = AgentDeploymentConfig.model_validate_json(config_json)
        print(f"Successfully validated configuration for agent: {config.agent_name}")
        return config
    except ValidationError as e:
        print(f"Configuration validation failed: {e.errors()}")
        return None

raw_config = """
{
    "agent_name": "SeniorResearcher",
    "model_name": "claude-5-1-sonnet",
    "instructions": "Gather, synthesize, and audit latest research papers on FastMCP 3.1.",
    "plugins": [
        {"plugin_name": "WebSearchPlugin", "allowed_methods": ["search_async"]}
    ],
    "mcp_version": "3.1"
}
"""

validated_config = load_and_validate_agent(raw_config)
```

## Related tools / concepts
- [AutoGen](autogen.md) - The experimental multi-agent framework from Microsoft Research.
- [Semantic Kernel](semantic-kernel.md) - The underlying orchestration SDK.
- [LangGraph](langgraph.md) - Alternative for complex, cyclic agent workflows.
- [CrewAI](crewai.md) - Lightweight multi-agent framework for rapid prototyping.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - The standard for connecting these agents to tools (FastMCP 3.1 compatibility).
- [Azure OpenAI](../providers/azure-openai.md) - Primary model provider for MS frameworks.
- [OpenAgents](../agents/open-agents.md) - For autonomous engineering agents that can be orchestrated by this framework.
- [Cline](../agents/cline.md) - High-autonomy agent that can integrate with enterprise toolsets.

## Sources / references
- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-studio/)
- [Microsoft Semantic Kernel GitHub](https://github.com/microsoft/semantic-kernel)
- [Gemma 3 on Azure AI Foundry](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/gemma-3-now-available-on-azure-ai/458921)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.org/task-protocol)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
