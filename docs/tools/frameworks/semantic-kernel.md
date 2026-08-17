# Semantic Kernel

## What it is
Semantic Kernel is an open-source SDK from Microsoft that allows developers to integrate Large Language Models (LLMs) into conventional programming languages like C#, Python, and Java. Using a "kernel-and-plugin" architecture, it combines AI capabilities with existing business code. As of late 2026, the SDK has reached **v1.18.0+** (Python SDK) and **v1.30.x** (.NET SDK), featuring native integration with the **Model Context Protocol (MCP 3.1 / FastMCP 3.1)**, advanced agentic orchestration primitives, and native support for frontier models (Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4).

## What problem it solves
It bridges the gap between generative AI models and traditional, enterprise-grade software engineering. It provides a structured way to manage prompt templates, conversation context, and tool-calling (native functions) while maintaining type safety, standard development practices, and cross-language compatibility. This allows teams to avoid rewriting business logic and instead wrap it seamlessly as AI plugins.

## Where it fits in the stack
**Category**: Frameworks / Enterprise SDK / Orchestration Layer

## Typical use cases
- **Enterprise App Integration**: Adding LLM features to existing robust .NET, Python, or Java applications.
- **Dynamic Task Automation**: Using the kernel's planner to solve complex customer requests by dynamically sequencing several native code functions.
- **Custom Copilots**: Building highly specialized workspace assistants that interact with internal APIs, databases, and Microsoft Graph.
- **Cross-Language AI Systems**: Implementing a standardized, consistent AI plugin schema across polyglot engineering organizations.

## Strengths
- **Multi-language Support**: True first-class support for C# / .NET, alongside Python and Java.
- **Enterprise-Grade Planners**: Advanced planning mechanisms, like the `FunctionCallingStepwisePlanner`, which decompose and execute multi-step user requests.
- **Microsoft Stack Native**: Out-of-the-box integration with Azure OpenAI, Microsoft Graph, and Azure AI Search.
- **MCP 3.1 Compliance**: Native ability to host and call Model Context Protocol (MCP) servers for dynamic tool discovery.
- **Type Safety**: Strongly-typed arguments in C# and validation schemas in Python ensure clean tool executions.

## Limitations
- **Heavyweight Abstractions**: The core kernel, planner, and plugin concepts can introduce more boilerplate than lighter alternatives like `smolagents`.
- **Feature Lag**: New or experimental features sometimes land in the .NET version first, with the Python and Java SDKs catching up shortly after.

## When to use it
- When building enterprise applications, particularly within a .NET or enterprise Python environment.
- When you need to strictly control how LLMs interact with your existing codebase via a formal, type-safe plugin architecture.
- For building robust "Copilot" style interfaces connected to corporate APIs and Azure infrastructure.

## When not to use it
- For quick, small-scale AI prototyping where a lightweight script or micro-framework is preferred.
- If you don't need a heavy enterprise kernel abstraction and want to minimize boilerplate.

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
    # Configure with OpenAI GPT-5.5 or Azure OpenAI
    kernel.add_service(OpenAIChatCompletion(ai_model_id="gpt-5.5-preview"))

    # Define a simple prompt-based function
    func = kernel.add_function(
        prompt="What is the capital of {{$input}}?",
        plugin_name="Geo",
        function_name="Capital"
    )

    result = await kernel.invoke(func, input="France")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples

```bash
# Install the Semantic Kernel CLI tool (dotnet-based)
dotnet tool install --global Microsoft.SemanticKernel.CLI

# Scaffold a new plugin skeleton via CLI
sk-cli create plugin --name InventoryPlugin --language python

# Run a plugin function directly from the CLI
sk-cli invoke --plugin InventoryPlugin --function CheckStock --input "item_id: 123"
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

### Type-Safe Plugin Arguments and Output Validation (Python with Pydantic v2)
In Semantic Kernel Python v1.18.0+, all plugin execution contexts, dynamic planner inputs, and execution traces can be strictly validated and marshaled through **Pydantic v2**:

```python
import json
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator

# 1. Define strict validation schemas for Semantic Kernel Plugin executions
class KernelPluginArgument(BaseModel):
    name: str
    value: Any
    type_name: str = Field(..., serialization_alias="typeName", validation_alias="typeName")

class KernelInvocationLog(BaseModel):
    plugin_name: str = Field(..., serialization_alias="pluginName", validation_alias="pluginName")
    function_name: str = Field(..., serialization_alias="functionName", validation_alias="functionName")
    arguments: List[KernelPluginArgument] = Field(default_factory=list)
    execution_time_ms: float = Field(..., ge=0, serialization_alias="executionTimeMs", validation_alias="executionTimeMs")
    status: Literal["success", "error"] = Field(default="success")

class KernelExecutionTrace(BaseModel):
    kernel_id: str = Field(..., serialization_alias="kernelId", validation_alias="kernelId")
    selected_frontier_model: str = Field(..., serialization_alias="selectedFrontierModel", validation_alias="selectedFrontierModel")
    invocations: List[KernelInvocationLog] = Field(default_factory=list)
    completion_tokens: int = Field(..., ge=0, serialization_alias="completionTokens", validation_alias="completionTokens")

    @field_validator("selected_frontier_model")
    @classmethod
    def validate_frontier_model(cls, v: str) -> str:
        allowed = ["Claude 5.1", "GPT-5.5", "Gemini 4.0", "Llama 4", "Gemma 3"]
        if not any(model in v for model in allowed):
            raise ValueError(f"Model {v} must be a late 2026 enterprise frontier model: {allowed}")
        return v

# 2. Simulated Invocation JSON telemetry emitted by Semantic Kernel Python execution hook
sk_invocation_payload = {
    "kernelId": "sk-kernel-enterprise-773",
    "selectedFrontierModel": "GPT-5.5",
    "completionTokens": 780,
    "invocations": [
        {
            "pluginName": "MathPlugin",
            "functionName": "Add",
            "executionTimeMs": 14.2,
            "status": "success",
            "arguments": [
                {"name": "number1", "value": 3.14, "typeName": "float"},
                {"name": "number2", "value": 2.71, "typeName": "float"}
            ]
        }
    ]
}

# 3. Perform validation
try:
    trace = KernelExecutionTrace(**sk_invocation_payload)
    print("Semantic Kernel execution trace successfully validated via Pydantic v2!")
    print(f"Kernel ID: {trace.kernel_id}")
    print(f"Active Model: {trace.selected_frontier_model}")
    for invocation in trace.invocations:
        print(f"  - Invoke: {invocation.plugin_name}.{invocation.function_name} -> {invocation.status}")
        for arg in invocation.arguments:
            print(f"    * Arg: {arg.name} = {arg.value} ({arg.type_name})")
except Exception as e:
    print(f"Semantic Kernel validation failed: {e}")
```

## Related tools / concepts
- [AutoGen](autogen.md)
- [LangChain](../../tools/ai_knowledge/langchain.md)
- [DSPy](dspy.md)
- [Haystack](haystack.md)
- [Smolagents](smolagents.md)
- [LangGraph](langgraph.md)
- [Microsoft Graph](../providers/microsoft-graph.md)
- [Azure OpenAI](../providers/azure-openai.md)
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md)

## Sources / references
- [GitHub](https://github.com/microsoft/semantic-kernel)
- [Microsoft Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Semantic Kernel Blog](https://devblogs.microsoft.com/semantic-kernel/)

## Contribution Metadata
- Last reviewed: 2026-12-10
- Confidence: high
