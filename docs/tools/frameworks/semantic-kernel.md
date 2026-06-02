# Semantic Kernel

## What it is
Semantic Kernel is an open-source SDK from Microsoft that allows developers to integrate LLMs into conventional programming languages like C#, Python, and Java. It uses "plugins" to combine AI capabilities with existing code.

## What problem it solves
It bridges the gap between AI models and traditional software engineering. It provides a structured way to manage prompts, state, and tool-calling (native functions) while maintaining type safety and standard development practices.

## Where it fits in the stack
Framework / SDK

## Typical use cases
- **Enterprise App Integration**: Adding AI features to existing .NET or Python applications.
- **Task Automation**: Using LLMs to orchestrate a series of native code functions.
- **Custom Copilots**: Building specialized assistants that interact with internal APIs.

## Strengths
- **Multi-language Support**: First-class support for C# / .NET, alongside Python and Java, allowing for unified AI strategies across different tech stacks.
- **Extensible Plugins**: Powerful system for wrapping existing business logic, APIs, and data sources as "tools" (plugins) for the LLM.
- **Microsoft Ecosystem**: Seamless integration with Azure OpenAI, Microsoft Graph, and other enterprise-grade services.
- **Planner Evolution**: Support for advanced planning mechanisms that can automatically combine multiple plugins to solve complex, multi-step requests.

## Advanced Technical Patterns

### 1. Wrapping Native Functions as Plugins
Semantic Kernel excels at making existing code "AI-ready" by wrapping native functions with metadata that the LLM can understand.

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

### 2. Orchestrating AI with Business Logic
The Kernel acts as a central hub, managing the interaction between the LLM and your native plugins.

```python
from semantic_kernel.contents import ChatHistory

# Initialize chat history
history = ChatHistory()

# Use the kernel to process a request using available plugins
result = await kernel.invoke(
    plugin_name="Math",
    function_name="Add",
    number1=10,
    number2=20
)
```

### 3. Using Planners for Complex Tasks
Planners can analyze the user's intent and automatically sequence calls to various plugins to achieve the goal.

```python
from semantic_kernel.planners import FunctionCallingStepwisePlanner

# Initialize a planner that can use all registered plugins
planner = FunctionCallingStepwisePlanner()

# Execute a complex task
result = await planner.execute(kernel, "Calculate the square root of 144 and add 50 to it.")
```

## Limitations
- **Complexity**: The "Kernel" and "Plugin" abstractions can feel heavy for small projects.
- **Python Parity**: While improving, some features sometimes land in the .NET version before the Python SDK.

## When to use it
- When building enterprise-grade applications, especially in a .NET environment.
- When you need to strictly control how AI interacts with your existing codebase.

## When not to use it
- For quick prototyping or research-focused LLM scripts.
- If you don't need the "kernel" abstraction and prefer a more lightweight approach.

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
    kernel.add_service(OpenAIChatCompletion(ai_model_id="gpt-3.5-turbo"))
    func = kernel.add_function(prompt="What is the capital of {{$input}}?", plugin_name="Geo", function_name="Capital")
    result = await kernel.invoke(func, input="France")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts

- [AutoGen](autogen.md)
- [LangChain](../ai_knowledge/langchain.md)
- [DSPy](dspy.md)
- [Haystack](haystack.md)
- [Smolagents](smolagents.md)
- [AutoGen](autogen.md)
- [LangGraph](langgraph.md)
## Sources / References
- [GitHub](https://github.com/microsoft/semantic-kernel)
- [Microsoft Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)

## Contribution Metadata

- Last reviewed: 2026-05-17
- Confidence: high
