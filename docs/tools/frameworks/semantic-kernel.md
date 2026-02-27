# Semantic Kernel

## What it is
Semantic Kernel is an open-source SDK from Microsoft that allows developers to integrate LLMs into conventional programming languages like C#, Python, and Java. It uses "plugins" to combine AI capabilities with existing code.

## What problem it solves
It bridges the gap between AI models and traditional software engineering. It provides a structured way to manage prompts, state, and tool-calling (native functions) while maintaining type safety and standard development practices.

## Where it fits in the stack
**Framework / SDK**. It provides the integration layer for embedding AI into enterprise applications.

## Typical use cases
- **Enterprise App Integration**: Adding AI features to existing .NET or Python applications.
- **Task Automation**: Using LLMs to orchestrate a series of native code functions.
- **Custom Copilots**: Building specialized assistants that interact with internal APIs.

## Strengths
- **Multi-language Support**: First-class support for C# / .NET, alongside Python and Java.
- **Extensible Plugins**: Easy to wrap existing business logic as "tools" for the LLM.
- **Microsoft Ecosystem**: Excellent integration with Azure OpenAI and other Microsoft services.

## Limitations
- **Complexity**: The "Kernel" and "Plugin" abstractions can feel heavy for small projects.
- **Python Parity**: While improving, some features sometimes land in the .NET version before the Python SDK.

## When to use it
- When building enterprise-grade applications, especially in a .NET environment.
- When you need to strictly control how AI interacts with your existing codebase.

## When not to use it
- For quick prototyping or research-focused LLM scripts.
- If you don't need the "kernel" abstraction and prefer a more lightweight approach.

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started
```bash
pip install semantic-kernel
```

```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

async def main():
    kernel = Kernel()
    # Note: Requires OPENAI_API_KEY env var
    kernel.add_service(OpenAIChatCompletion(ai_model_id="gpt-3.5-turbo"))

    # Create a function from a prompt
    func = kernel.add_function(prompt="What is the capital of {{$input}}?", plugin_name="Geo", function_name="Capital")

    result = await kernel.invoke(func, input="France")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts
- [AutoGen](autogen.md)
- [LangChain](../ai_knowledge/langchain.md)
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

## Sources / References
- [GitHub](https://github.com/microsoft/semantic-kernel)
- [Microsoft Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: high
