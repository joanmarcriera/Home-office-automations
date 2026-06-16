# Microsoft Agent Framework

## What it is
Microsoft Agent Framework (integrated within **Azure AI Foundry** and the **Semantic Kernel** ecosystem) is a collection of libraries and standards for building, orchestrating, and managing multi-agent AI systems. In June 2026, it serves as the primary enterprise framework for deploying agents that utilize frontier models like **Claude 4.8 Opus** (via Azure) and **GPT-5.5**, providing high-level abstractions for agent communication, state management, and tool execution.

## What problem it solves
It simplifies the coordination of multiple LLM-powered agents, providing standardized ways for them to communicate, share state, and collaborate on complex tasks. It addresses critical enterprise challenges including agentic memory persistence, role-based tool access control, and cross-agent consistency, preventing the "unreliable agent" problem in production.

## Where it fits in the stack
**Frameworks / Orchestration**. It sits at the orchestration layer, connecting infrastructure (Azure AI Foundry) and models with application-level agentic logic.

## Typical use cases
- **Enterprise Multi-agent Teams**: Building teams of agents with specialized roles (e.g., Researcher, Coder, Reviewer) that collaborate on software development or financial analysis.
- **Automated Customer Support**: Orchestrating agents that can handle complex multi-step support tickets with human-in-the-loop (HITL) handoffs.
- **Business Process Automation**: Integrating agents into existing Microsoft 365 workflows to automate reporting, data entry, and meeting synthesis.
- **Legacy System Interfacing**: Using Semantic Kernel connectors to allow agents to interact securely with on-premises corporate APIs and databases.

## Strengths
- **Azure Integration**: Seamlessly works with Azure OpenAI Service, Azure AI Search, and the broader Azure ecosystem for security and compliance.
- **Enterprise Scale**: Designed with robust security, built-in observability for production monitoring, and support for high-throughput agentic workloads.
- **Sophisticated State Management**: Provides advanced patterns for managing long-term agent memory and conversation history across different model providers.
- **Cross-Language Support**: Strong, first-class support for both **.NET** and **Python**, catering to both enterprise application developers and AI researchers.

## Limitations
- **Learning Curve**: The framework's depth and enterprise features lead to a steeper learning curve compared to lightweight libraries.
- **Ecosystem Gravity**: While usable standalone, its maximum value is realized when deployed within the Microsoft/Azure ecosystem.
- **Rapid Release Cycle**: The framework evolves quickly, requiring regular maintenance to keep up with new features and architectural best practices.

## When to use it
- When building complex, enterprise-grade multi-agent systems that require high security and scalability.
- When you need to integrate AI agents with existing .NET-based corporate infrastructure.
- When you require robust, out-of-the-box orchestration, observability, and state management for agents in production.
- When utilizing Azure AI Foundry as your primary model serving and management platform.

## When not to use it
- For simple, single-agent tasks where a basic SDK or a minimalist library like [Smolagents](smolagents.md) is sufficient.
- If you prefer a completely ecosystem-agnostic, lightweight open-source framework without enterprise overhead.
- When building non-enterprise, small-scale prototypes where speed of initial setup is the only priority.

## Getting started

### Installation (Python)
In June 2026, the framework is primarily accessed via the `azure-ai-projects` library for Azure environments.

```bash
pip install azure-ai-projects azure-identity
```

### Initial Configuration
Initialize the project client to connect to your Azure AI Foundry project:
```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient.from_connection_string(
    conn_str="YOUR_CONNECTION_STRING",
    credential=DefaultAzureCredential()
)
```

## CLI examples

### Azure CLI (Agent Management)
Manage AI agents and projects using the Azure CLI (`az`) with the AI extension.

```bash
# Create a new AI project in a resource group
az ai project create --name my-ai-project --resource-group my-group

# List available agents within a specific project
az ai agent list --project-name my-ai-project

# View logs for a specific agent execution
az ai agent logs --name my-first-agent --project-name my-ai-project
```

## API examples

### Creating and Running an Agent (Python)
Using the Azure AI Agents service to create a simple agent utilizing **GPT-5.5**.

```python
# Create an agent with specific instructions
agent = project_client.agents.create_agent(
    model="gpt-5.5-preview",
    name="analyst-agent",
    instructions="Analyze the provided financial data and suggest optimizations."
)

# Create a conversation thread and run the agent
run = project_client.agents.create_run(
    thread_id="thread-unique-id",
    assistant_id=agent.id,
    prompt="What is our projected Q3 growth based on these spreadsheets?"
)

print(f"Agent Response: {run.messages[0].text}")
```

### Multi-Agent Interaction (.NET)
Defining roles and handoffs in C# using Semantic Kernel.

```csharp
using Microsoft.SemanticKernel.Agents;

// Define a Code Reviewer Agent
ChatCompletionAgent reviewerAgent = new()
{
    Name = "Reviewer",
    Instructions = "Review code for performance and security vulnerabilities.",
    Kernel = kernel
};

// Define a Coder Agent
ChatCompletionAgent coderAgent = new()
{
    Name = "Coder",
    Instructions = "Write optimized C# code based on user requirements.",
    Kernel = kernel
};
```

## Related tools / concepts
- [AutoGen](autogen.md)
- [Semantic Kernel](semantic-kernel.md)
- [CrewAI](crewai.md)
- [LangGraph](../frameworks/langgraph.md)
- [Azure OpenAI](../providers/azure-openai.md)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Aider](../development_ops/aider.md)
- [OpenHands](../development_ops/openhands.md)

## Sources / References
- [Official Microsoft AI Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-services/agents/)
- [Azure AI Foundry Overview](https://ai.azure.com/)
- [Semantic Kernel GitHub Repository](https://github.com/microsoft/semantic-kernel)
- [Microsoft Research: Multi-Agent Systems](https://www.microsoft.com/en-us/research/project/ai-agents/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
