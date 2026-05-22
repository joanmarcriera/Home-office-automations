# Microsoft Agent Framework

## What it is
Microsoft Agent Framework (part of the broader Azure AI and Semantic Kernel ecosystem) is a collection of libraries and standards for building, orchestrating, and managing multi-agent AI systems. It is designed to provide high-level abstractions for agent communication and state management.

## What problem it solves
It simplifies the coordination of multiple LLM-powered agents, providing standardized ways for them to communicate, share state, and collaborate on complex tasks. It addresses the challenges of agentic memory, tool access control, and cross-agent consistency in an enterprise context.

## Where it fits in the stack
**Category**: Frameworks / Orchestration

## Typical use cases
- **Multi-agent Collaboration**: Building teams of agents with specialized roles (e.g., Researcher, Coder, Reviewer).
- **Enterprise Agent Management**: Deploying agents within existing Microsoft 365 or Azure environments.
- **Workflow Automation**: Orchestrating agents to perform end-to-end business processes with human-in-the-loop (HITL) support.
- **Legacy System Integration**: Using Semantic Kernel connectors to allow agents to interact with corporate APIs and databases.

## Strengths
- **Azure Integration**: Seamlessly works with Azure OpenAI Service, Azure AI Search, and other Azure components.
- **Enterprise Ready**: Designed with robust security, scalability, and built-in observability for production monitoring.
- **Standardized State**: Provides sophisticated patterns for managing agent memory and conversation history across different models.
- **Multi-Language Support**: Strong support for both C# (.NET) and Python, catering to enterprise and AI research teams alike.

## Limitations
- **Complexity**: Can have a steeper learning curve compared to simpler multi-agent frameworks like CrewAI.
- **Ecosystem Affinity**: While usable standalone, its deepest value is realized within the Microsoft/Azure ecosystem.
- **Rapid Evolution**: The framework is evolving quickly, which can lead to frequent updates and breaking changes in earlier versions.

## When to use it
- When building complex, enterprise-grade multi-agent systems, especially if already using Azure.
- When you need robust orchestration, security, and state management for agents in a production environment.
- When you need to integrate agents with .NET-based applications.

## When not to use it
- For simple, single-agent tasks where a basic SDK (like OpenAI's) or a lightweight library (like Smolagents) is sufficient.
- If you prefer a completely lightweight, community-driven, or ecosystem-agnostic open-source framework.


## Getting started

### Installation (Python)
The framework is primarily accessed via the `azure-ai-projects` and `azure-ai-inference` libraries for Azure environments, or via `semantic-kernel` for general use.

```bash
pip install azure-ai-projects azure-identity
```

### Usage (Hello World Agent - Python)
This example uses the Azure AI Agents service to create a simple agent.

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize the client
project_client = AIProjectClient.from_connection_string(
    conn_str="YOUR_CONNECTION_STRING",
    credential=DefaultAzureCredential()
)

# Create an agent
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-first-agent",
    instructions="You are a helpful assistant."
)

# Run a task
run = project_client.agents.create_run(
    thread_id="my-thread",
    assistant_id=agent.id,
    prompt="Tell me a joke!"
)

print(f"Agent Response: {run.messages[0].text}")
```

### Usage (Hello World Agent - .NET)
Semantic Kernel allows for robust agent definitions in C#.

```csharp
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;

// Initialize the Kernel
var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion("deployment-name", "endpoint", "api-key");
var kernel = builder.Build();

// Define the Agent
ChatCompletionAgent agent = new()
{
    Name = "ReviewerAgent",
    Instructions = "You are a code reviewer. Focus on performance.",
    Kernel = kernel
};

// Execute a Conversation
var history = new ChatHistory();
history.AddUserMessage("Review this: for(int i=0; i<10; i++) { Console.WriteLine(i); }");

await foreach (var message in agent.InvokeAsync(history))
{
    Console.WriteLine($"{message.Role}: {message.Content}");
}
```

## CLI examples

### Azure CLI (Agent Management)
Manage AI agents and projects using the Azure CLI (`az`).

```bash
# Create a new AI project
az ai project create --name my-ai-project --resource-group my-group

# List available agents in a project
az ai agent list --project-name my-ai-project
```

## API examples

### Multi-Agent Interaction
Defining roles and handoffs between agents using the framework logic.

```python
# Conceptual multi-agent setup in Semantic Kernel
from semantic_kernel.agents import ChatCompletionAgent

# Define Researcher
researcher = ChatCompletionAgent(
    name="Researcher",
    instructions="Find data on the requested topic.",
    kernel=kernel
)

# Define Writer
writer = ChatCompletionAgent(
    name="Writer",
    instructions="Write a summary based on the research provided.",
    kernel=kernel
)
```

## Licensing and cost
- **Open Source**: Significant parts are open source (e.g., Semantic Kernel); others are proprietary Azure services.
- **Cost**: Variable; libraries are free, but underlying Azure AI services and infrastructure incur costs.
- **Self-hostable**: Yes (the framework libraries can be run anywhere).

## Related tools / concepts
- [AutoGen](autogen.md)
- [Semantic Kernel](semantic-kernel.md)
- [CrewAI](crewai.md)
- [LangGraph](langgraph.md)
- [OpenAI Agents SDK](openai-agents-sdk.md)
- [Azure OpenAI](../providers/azure-openai.md)
- [Plandex](../development_ops/plandex.md)
- [Aider](../development_ops/aider.md)

## Sources / References
- [Official Microsoft AI Agents Site](https://www.microsoft.com/en-us/research/project/ai-agents/)
- [Azure AI Agents Service Documentation](https://learn.microsoft.com/en-us/azure/ai-services/agents/)
- [Semantic Kernel Overview](https://learn.microsoft.com/en-us/semantic-kernel/overview/)

## Contribution Metadata
- Last reviewed: 2026-05-21
- Confidence: high
