# Semantic Kernel

## What it is
Semantic Kernel is an open-source, enterprise-grade orchestration SDK developed by Microsoft that enables software engineers to integrate Large Language Models (LLMs) into conventional programming environments—including C# (.NET 8/9+), Python (3.10–3.12+), and Java (17/21+). Architected around a robust "kernel-and-plugin" abstraction, Semantic Kernel decouples business domain functions from underlying AI inference providers. In early 2027, the SDK has reached version **v1.22.0+** for Python and **v1.35.x** for .NET, delivering native support for **FastMCP 3.1 (Model Context Protocol)**, multi-agent orchestrations, OpenTelemetry-compliant observability pipelines, and frontier reasoning models (including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Llama 4).

Through its unified plugin paradigm, Semantic Kernel transforms plain code functions, HTTP web APIs, database connectors, and prompt templates into strongly-typed tools that AI models can dynamically discover, sequence, and execute. It forms a bridge between classical enterprise architecture—such as dependency injection, strongly-typed domain models, and zero-trust security controls—and modern non-deterministic agentic workflows.

## What problem it solves
Integrating generative AI models into production enterprise systems introduces significant architectural and operational friction:
- **Tight Coupling & Vendor Lock-In**: Hardcoding provider-specific API calls (e.g. OpenAI vs. Anthropic vs. Azure AI) makes switching models or deploying local fallbacks extremely difficult.
- **Unstructured Tool Execution**: Free-form text prompts interacting with raw APIs lack compile-time or runtime type validation, causing unpredictable runtime failures or injection vulnerabilities.
- **Lack of Multi-Language Standardization**: Polyglot enterprise teams often create fragmented, inconsistent AI implementations across C#, Python, and Java codebases.
- **Complex Multi-Step Orchestration**: Manually writing procedural code to sequence dependencies across dozens of internal microservices and external databases quickly becomes unmaintainable.

Semantic Kernel resolves these issues by serving as an abstraction layer with:
- **Unified Kernel Service Registry**: Registers chat completion, text generation, embedding, and vector search services with interchangeable provider implementations.
- **Native & Semantic Plugin Architecture**: Exposes internal C#, Python, or Java methods directly to models using attributes or decorators without manual prompt engineering.
- **Automatic Function Calling Planners**: Sequentially or iteratively plans multi-step tool invocations (`FunctionCallingStepwisePlanner`) based on user intent and dynamic context.
- **Standardized MCP 3.1 Gateway**: Connects directly to external FastMCP 3.1 tool servers, exposing remote MCP capabilities alongside local native plugins.

```
+---------------------------------------------------------------------------------------------------+
|                                SEMANTIC KERNEL ARCHITECTURE                                       |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Client Applications  |     |  Semantic Kernel Core |     |  AI Model Service Connectors  |   |
|   |                       |     |                       |     |                               |   |
|   | - ASP.NET Core Web App| --> | - Kernel Context      | --> | - Azure OpenAI (GPT-5.6)      |   |
|   | - Python FastAPI Micro|     | - Service Provider    |     | - Anthropic (Claude 5.6)      |   |
|   | - Java Enterprise App |     | - Memory & Vector Store|    | - Local Ollama / vLLM         |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                             |                                 |                   |
|                                             v                                 v                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Plugin & Tool Layer  |     |  Planner & Agent Engine|    |  FastMCP 3.1 Server Gateway   |   |
|   |                       |     |                       |     |                               |   |
|   | - Native Code Plugins | <-- | - Stepwise Planner    | <-- | - DB Query Tools              |   |
|   | - Prompt Plugins      |     | - Agent Group Chat    |     | - File System MCP             |   |
|   | - OpenApi Spec Plugins|     | - Filter Extensions   |     | - Enterprise ERP Tools        |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: Frameworks / Enterprise SDK / Orchestration Layer.

Semantic Kernel sits in the **Application Orchestration Layer**, bridging **Enterprise Data & API Services** (ASP.NET Core, FastAPI, Spring Boot, Microsoft Graph, SQL/NoSQL databases) with **Frontier AI Providers** (Azure OpenAI, Anthropic, Google Vertex AI, AWS Bedrock) and **FastMCP 3.1 Tool Servers**.

## Typical use cases
- **Enterprise Copilot Systems**: Building customized workplace assistants integrated into Microsoft Teams, Slack, or internal portals connected to Microsoft Graph and enterprise ERPs.
- **Automated Multi-Step API Pipelines**: Utilizing planners to interpret user queries, synthesize request plans, call REST endpoints, and format combined JSON responses.
- **Polyglot AI Standardization**: Standardizing agentic tool definitions across a enterprise with shared plugin definitions between C# microservices and Python data pipelines.
- **RAG & Hybrid Search Systems**: Interfacing seamlessly with vector databases (Azure AI Search, Pinecone, Qdrant) through unified `VolatileMemoryStore` or `VectorStore` abstractions.

## Strengths
- **Native Multi-Language Parity**: Full first-class support for C#/.NET and Python, alongside an actively maintained Java SDK.
- **Enterprise .NET & Azure Alignment**: Deep alignment with Microsoft technologies including Azure AI Search, Azure OpenAI, Microsoft Graph, and .NET Dependency Injection (`IServiceCollection`).
- **Robust Type Safety**: Compile-time typing in C# and runtime Pydantic v2 validation in Python minimize malformed model invocations.
- **MCP 3.1 Compliance**: Built-in support to consume external FastMCP tool definitions and register them natively as Kernel Plugins.
- **Extensible Middleware (Filters)**: Supports Function Render, Function Invocation, and Prompt Filters for auditing, security scanning, cost management, and token tracking.

## Limitations
- **Heavy Abstraction Footprint**: The core abstractions (Kernel, Plugins, Functions, Memory, Planners) introduce more boilerplate than minimal alternatives like `smolagents`.
- **SDK Release Parity Lag**: Advanced features (such as experimental multi-agent abstractions) occasionally land in the .NET SDK before rolling out to Python and Java.

## When to use it
- When developing production enterprise applications, particularly within Microsoft .NET, Azure, or hybrid Python environments.
- When requiring strict runtime safety, comprehensive telemetry, and formal dependency-injected plugin architectures.
- When building robust Copilot interfaces that require connection to Azure infrastructure and FastMCP 3.1 servers.

## When not to use it
- For quick, single-script AI experiments or simple wrapper utilities where lightweight frameworks are preferred.
- If your stack is strictly non-Microsoft and focused purely on local Python research without enterprise SDK constraints.

## Getting started

### Installation
```bash
# Python Installation
pip install semantic-kernel pydantic mcp

# .NET Installation (via CLI)
dotnet add package Microsoft.SemanticKernel
```

### Minimal Python Execution
```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

async def main():
    kernel = Kernel()

    # Register Chat Completion Service
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat-gpt5",
            ai_model_id="gpt-5.6",
            api_key="YOUR_OPENAI_API_KEY"
        )
    )

    # Inline prompt function
    prompt = "Summarize the key architectural benefits of {{$input}} in 3 bullet points."
    summary_func = kernel.add_function(
        prompt=prompt,
        plugin_name="SummarizerPlugin",
        function_name="QuickSummary"
    )

    result = await kernel.invoke(summary_func, input="Semantic Kernel Orchestration")
    print("Summary Output:\n", result)

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples

```bash
# Install global Semantic Kernel CLI (.NET)
dotnet tool install --global Microsoft.SemanticKernel.CLI

# Scaffold a new Python plugin template
sk-cli create plugin --name InventoryPlugin --language python

# Inspect and execute a registered plugin function
sk-cli invoke --plugin InventoryPlugin --function CheckStock --input "sku: SKU-8849"
```

## API examples

### Native C# / .NET Plugin Definition
```csharp
using System.ComponentModel;
using Microsoft.SemanticKernel;

public class InventoryPlugin
{
    [KernelFunction, Description("Retrieves current stock count for a given SKU.")]
    public async Task<int> GetStockAsync(
        [Description("The unique product SKU code")] string sku)
    {
        // Business logic interacting with database or ERP
        await Task.Delay(10);
        return 142;
    }
}

// Registration in ASP.NET Core Service Container
var builder = Kernel.CreateBuilder();
builder.AddOpenAIChatCompletion("gpt-5.6", "YOUR_API_KEY");
builder.Plugins.AddFromType<InventoryPlugin>("Inventory");
Kernel kernel = builder.Build();
```

### Native Python Plugin with FastMCP 3.1 Bridge
```python
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function

class CustomerSupportPlugin:
    @kernel_function(
        name="GetCustomerTier",
        description="Returns the loyalty tier and SLA for a given customer ID."
    )
    def get_customer_tier(self, customer_id: str) -> str:
        # Simulated enterprise CRM lookup
        if customer_id.startswith("VIP"):
            return "Tier: Platinum | SLA: 15-minute response"
        return "Tier: Standard | SLA: 24-hour response"

async def run_kernel_with_plugin():
    kernel = Kernel()
    kernel.add_plugin(CustomerSupportPlugin(), plugin_name="CRM")

    tier_func = kernel.plugins["CRM"]["GetCustomerTier"]
    res = await kernel.invoke(tier_func, customer_id="VIP-90210")
    print("Customer Tier Lookup:", res)

if __name__ == "__main__":
    asyncio.run(run_kernel_with_plugin())
```

## FastMCP 3.1 Integration Pattern

Below is a complete FastMCP 3.1 tool server implementation demonstrating how Semantic Kernel invocation metrics, plugin states, and execution traces are exposed to external agentic clients:

```python
import asyncio
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("SemanticKernelBridgeServer", version="3.1.0")

class SKPluginFunctionArg(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    arg_name: str = Field(..., description="Argument identifier")
    arg_value: str = Field(..., description="Stringified argument value")
    type_hint: str = Field("str", description="Expected type hint")

class SKInvocationRequest(BaseModel):
    plugin_name: str = Field(..., description="Target Semantic Kernel plugin name")
    function_name: str = Field(..., description="Target function name within the plugin")
    arguments: List[SKPluginFunctionArg] = Field(default_factory=list)

class SKInvocationResponse(BaseModel):
    success: bool
    output_result: str
    execution_ms: float
    selected_model: str

@mcp.tool()
def execute_kernel_plugin_function(
    plugin_name: str,
    function_name: str,
    customer_id: str,
    selected_model: str = "gpt-5.6"
) -> str:
    """
    FastMCP tool wrapper executing a Semantic Kernel registered plugin method.
    Returns JSON string adhering to SKInvocationResponse schema.
    """
    start_time = asyncio.get_event_loop().time()

    # Simulated execution within Semantic Kernel Context
    if plugin_name == "CRM" and function_name == "GetCustomerTier":
        output = f"Customer '{customer_id}' holds Gold Status with priority support."
        status = True
    else:
        output = f"Plugin {plugin_name}.{function_name} not found."
        status = False

    end_time = asyncio.get_event_loop().time()
    duration_ms = round((end_time - start_time) * 1000, 2)

    response = SKInvocationResponse(
        success=status,
        output_result=output,
        execution_ms=duration_ms,
        selected_model=selected_model
    )
    return response.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Type-Safe Validation & Observability (Pydantic v2)

In Python implementations of Semantic Kernel, telemetry, prompt logs, and invocation contexts are validated via **Pydantic v2**:

```python
from typing import List, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

class KernelFunctionMetric(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    plugin_name: str = Field(..., description="Name of invoked plugin")
    function_name: str = Field(..., description="Name of executed function")
    duration_ms: float = Field(..., ge=0.0, description="Execution duration in ms")
    status: Literal["success", "error"] = Field("success")

class KernelTelemetryTrace(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    trace_id: str = Field(..., description="Unique OpenTelemetry trace ID")
    frontier_model: str = Field(..., description="Active frontier reasoning model")
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    metrics: List[KernelFunctionMetric] = Field(default_factory=list)

    @field_validator("frontier_model")
    @classmethod
    def validate_frontier_model(cls, val: str) -> str:
        allowed = {"claude-5.6", "gpt-5.6", "gemini-4.0-ultra", "deepseek-v4", "llama-4"}
        normalized = val.lower().strip()
        if not any(model in normalized for model in allowed):
            raise ValueError(f"Model '{val}' must be an allowed enterprise frontier model: {allowed}")
        return val

# Validation demonstration
trace_payload = {
    "trace_id": "tr-sk-99021-az",
    "frontier_model": "gpt-5.6",
    "prompt_tokens": 1240,
    "completion_tokens": 310,
    "metrics": [
        {
            "plugin_name": "CRM",
            "function_name": "GetCustomerTier",
            "duration_ms": 18.5,
            "status": "success"
        }
    ]
}

validated_trace = KernelTelemetryTrace(**trace_payload)
print("Validated SK Trace:", validated_trace.model_dump_json(indent=2))
```

## Related tools / concepts
- [AutoGen](autogen.md): Multi-agent conversation framework from Microsoft Research.
- [LangChain](../../tools/ai_knowledge/langchain.md): Python/TypeScript framework for LLM applications.
- [DSPy](dspy.md): Declarative prompt optimization and compilation framework.
- [Haystack](haystack.md): Open-source NLP and RAG orchestration framework.
- [Smolagents](smolagents.md): Lightweight agent framework focused on code-as-action.
- [LangGraph](langgraph.md): Graph-based agentic workflow orchestration library.
- [Microsoft Graph](../providers/microsoft-graph.md): Unified API endpoint for Microsoft 365 services.
- [Azure OpenAI](../providers/azure-openai.md): Enterprise managed OpenAI service on Microsoft Azure.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md): Open protocol standard for model-tool interoperability.

## Sources / references
- [Microsoft Semantic Kernel GitHub Repository](https://github.com/microsoft/semantic-kernel)
- [Microsoft Learn: Semantic Kernel Overview & Architecture](https://learn.microsoft.com/en-us/semantic-kernel/)
- [Microsoft DevBlog: Semantic Kernel Announcements](https://devblogs.microsoft.com/semantic-kernel/)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
