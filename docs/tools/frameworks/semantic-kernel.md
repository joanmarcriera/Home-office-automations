# Semantic Kernel

## What it is
Semantic Kernel is an open-source SDK from Microsoft that allows developers to integrate LLMs into conventional programming languages like C#, Python, and Java. It uses "plugins" to combine AI capabilities with existing code.

## What problem it solves
It bridges the gap between AI models and traditional software engineering. It provides a structured way to manage prompts, state, and tool-calling (native functions) while maintaining type safety, standard development practices, and enterprise-grade scalability.

## Where it fits in the stack
**Framework / Enterprise SDK**. It acts as the orchestration layer for integrating frontier models like Claude 4.8 and GPT-5.5 into established software ecosystems, particularly the Microsoft stack.

## Typical use cases
- **Enterprise App Integration**: Adding AI features to existing .NET or Python applications.
- **Task Automation**: Using LLMs to orchestrate a series of native code functions.
- **Custom Copilots**: Building specialized assistants that interact with internal APIs and databases.
- **Cross-Language AI Strategy**: Implementing a unified AI orchestration layer across a polyglot engineering organization.

## Strengths
- **Multi-language Support**: First-class support for C# / .NET, alongside Python and Java.
- **Extensible Plugins**: Powerful system for wrapping existing business logic as "tools" (plugins).
- **Microsoft Ecosystem**: Native integration with Azure OpenAI, Microsoft Graph, and Azure AI Search.
- **Planner Evolution**: Support for advanced planning mechanisms like `FunctionCallingStepwisePlanner` to solve complex requests.
- **Type Safety**: Strong typing in C# and structured schemas in Python/Java ensure reliable tool interactions.
- **MCP 3.0 Compliance**: Seamless integration with the Model Context Protocol for cross-platform tool use.

## Limitations
- **Complexity**: The "Kernel" and "Plugin" abstractions can feel heavy for small projects or simple scripts.
- **Python Parity**: While significantly improved in 2026, some experimental features still land in the .NET version first.
- **Learning Curve**: Requires understanding the "Semantic" vs "Native" function paradigm.

## When to use it
- When building enterprise-grade applications, especially in a .NET environment.
- When you need to strictly control how AI interacts with your existing codebase via a formal plugin system.
- For building robust, maintainable "Copilot" experiences within corporate software.

## When not to use it
- For quick prototyping or research-focused LLM scripts.
- If you don't need the "kernel" abstraction and prefer a more lightweight approach like `smolagents`.
- For simple chatbot applications that don't require integration with native code.

## Getting started

### Installation
```bash
pip install semantic-kernel
```

### Minimal Python Example
```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

async def main():
    kernel = Kernel()
    # Configure with GPT-4o or Claude via connectors
    kernel.add_service(OpenAIChatCompletion(ai_model_id="gpt-4o"))

    # Define a simple prompt-based function
    func = kernel.add_function(prompt="What is the capital of {{$input}}?", plugin_name="Geo", function_name="Capital")

    result = await kernel.invoke(func, input="France")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples

```bash
# Installing the Semantic Kernel CLI tools (if available via dotnet)
dotnet tool install --global Microsoft.SemanticKernel.CLI

# Using the CLI to scaffold a new plugin
sk-cli create plugin --name MyBusinessPlugin --language python

# Testing a plugin via the CLI
sk-cli invoke --plugin MyBusinessPlugin --function MyFunction --input "test data"
```

## API examples

### Wrapping Native Functions as Plugins
```python
from semantic_kernel.functions import kernel_function

class MathPlugin:
    @kernel_function(
        description="Adds two numbers together",
        name="Add"
    )
    def add(self, number1: float, number2: float) -> float:
        return number1 + number2

# Add the plugin to the kernel
kernel.add_plugin(MathPlugin(), plugin_name="Math")
```

### Using Planners for Complex Tasks
```python
from semantic_kernel.planners import FunctionCallingStepwisePlanner

# Initialize a planner that can use all registered plugins
planner = FunctionCallingStepwisePlanner()

# Execute a complex task using frontier models
result = await planner.execute(kernel, "Analyze the sales data and provide a summary report.")
```

## Related tools / concepts
- [AutoGen](autogen.md)
- [LangChain](../../tools/ai_knowledge/langchain.md)
- [DSPy](dspy.md)
- [Haystack](haystack.md)
- [Smolagents](smolagents.md)
- [LangGraph](langgraph.md)
- [Microsoft Graph](../../tools/providers/microsoft.md)
- [Azure OpenAI](../../tools/providers/azure.md)
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md)

## Sources / references
- [GitHub](https://github.com/microsoft/semantic-kernel)
- [Microsoft Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Semantic Kernel Blog](https://devblogs.microsoft.com/semantic-kernel/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
