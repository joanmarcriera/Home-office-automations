# Microsoft Agent Framework

## What it is
Microsoft Agent Framework (integrated within **Azure AI Foundry** and the **Semantic Kernel** ecosystem) is an enterprise-grade suite of libraries and standards for building, orchestrating, and managing multi-agent AI systems. As of July 2026, it serves as a primary backbone for deploying high-autonomy agents in corporate environments, supporting frontier models such as **Gemma 3**, **Claude 4.8 Opus**, and **GPT-5.5**.

## What problem it solves
It simplifies the coordination of multiple LLM-powered agents, providing standardized protocols for communication (via Agent Chat), state management, and long-term memory. It addresses the challenges of "agentic drift," tool-use reliability, and cross-agent consistency that occur when scaling beyond single-prompt interactions in an enterprise context, now enhanced by the **MCP 3.0 Task Protocol** for standardized task execution.

## Where it fits in the stack
**Category**: Frameworks / Orchestration
It sits between the inference layer (Azure OpenAI Service, Azure AI Foundry) and the application layer, providing the "brain" and "memory" for autonomous workflows. It utilizes **FastMCP 3.0** for ultra-low latency tool hosting and agent discovery.

## Typical use cases
- **Multi-agent Collaboration**: Building specialized teams (e.g., a "DevOps Agent" using Claude 4.8 and a "Quality Gate Agent" using Gemma 3) that cooperate on software delivery.
- **Enterprise Research**: Orchestrating research agents that browse internal SharePoint data and external web signals simultaneously.
- **Workflow Automation**: Automating complex, multi-step business processes with native human-in-the-loop (HITL) checkpoints.
- **Legacy Integration**: Using Semantic Kernel "Plugins" to allow agents to safely execute actions against SAP, Salesforce, or custom SQL databases via MCP 3.0.

## Strengths
- **Azure AI Foundry Native**: Seamless integration with the latest model catalogs, including native support for Gemma 3 and Claude 4.8 Opus on Azure.
- **Enterprise Security**: Inherits Azure's robust identity (Entra ID), data residency, and compliance guardrails.
- **Standardized State Management**: Features a sophisticated `AgentChat` protocol that handles conversation history and state persistence across different providers.
- **MCP 3.0 Task Protocol**: Native support for standardized task representations, enabling interoperability with a wide range of external tools.

## Limitations
- **Azure Dependency**: While Semantic Kernel is open-source, the full Agent Framework benefits are most pronounced when locked into the Azure/Microsoft ecosystem.
- **Higher Latency**: The orchestration overhead and enterprise-grade state management can introduce slight latency compared to minimalist frameworks like `smolagents`.
- **API Complexity**: The abstraction layer is deep, which can make debugging "agent-to-agent" handoffs more difficult than in lower-level libraries.

## When to use it
- When building production-grade agents that require strict security, audit logs, and enterprise integration.
- When you need a multi-agent system that leverages both OpenAI and Anthropic models through a unified interface (Azure AI Foundry).
- When you are developing in a .NET-heavy environment but want access to Python-native AI capabilities and MCP 3.0 toolsets.

## When not to use it
- For quick, experimental prototypes where a single-file script or a lightweight framework like [CrewAI](crewai.md) would be faster to iterate on.
- If you require a completely ecosystem-agnostic, open-source-only stack without any cloud provider affinity.

## Getting started

### Installation (Python)
Install the core Azure AI agent and identity libraries:

```bash
pip install azure-ai-projects azure-identity semantic-kernel
```

### Usage (Hello World Agent - Python)
Configuring a Gemma 3 agent within the framework.

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
    prompt="Summarize the latest trends in agentic orchestration."
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

### Multi-Agent Handoff (Semantic Kernel)
Defining a "delegation" pattern between a Researcher and a Writer.

```python
from semantic_kernel.agents import ChatCompletionAgent, AgentGroupChat
from semantic_kernel.agents.strategies import TerminationStrategy

# Define Researcher (using Claude 4.8 Opus)
researcher = ChatCompletionAgent(
    name="Researcher",
    instructions="Gather facts on the topic.",
    kernel=kernel_claude
)

# Define Writer (using Gemma 3)
writer = ChatCompletionAgent(
    name="Writer",
    instructions="Write a summary based on research.",
    kernel=kernel_gemma
)

# Orchestrate in a Group Chat
group_chat = AgentGroupChat(
    agents=[researcher, writer],
    termination_strategy=TerminationStrategy(maximum_iterations=5)
)

await group_chat.add_chat_message("Explain the impact of MCP 3.0 on agentic scaling.")
async for message in group_chat.invoke():
    print(f"{message.role}: {message.content}")
```

## Related tools / concepts
- [AutoGen](autogen.md) - The experimental multi-agent framework from Microsoft Research.
- [Semantic Kernel](semantic-kernel.md) - The underlying orchestration SDK.
- [LangGraph](langgraph.md) - Alternative for complex, cyclic agent workflows.
- [CrewAI](crewai.md) - Lightweight multi-agent framework for rapid prototyping.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - The standard for connecting these agents to tools.
- [Azure OpenAI](../providers/azure-openai.md) - Primary model provider for MS frameworks.
- [OpenAgents](../agents/open-agents.md) - For autonomous engineering agents that can be orchestrated by this framework.
- [Cline](../agents/cline.md) - High-autonomy agent that can integrate with enterprise toolsets.

## Sources / references
- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-studio/)
- [Microsoft Semantic Kernel GitHub](https://github.com/microsoft/semantic-kernel)
- [Gemma 3 on Azure AI Foundry](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/gemma-3-now-available-on-azure-ai/458921)
- [MCP 3.0 Task Protocol Specification](https://modelcontextprotocol.org/task-protocol)

## Contribution Metadata
- Last reviewed: 2026-07-05
- Confidence: high
