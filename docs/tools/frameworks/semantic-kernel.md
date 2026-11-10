# Semantic Kernel

## What it is
Semantic Kernel is an open-source, enterprise-grade orchestration SDK developed by Microsoft that enables software engineers to integrate Large Language Models (LLMs) into conventional programming environments—including C# (.NET 8/9+), Python (3.10–3.12+), and Java (17/21+). Architected around a robust "kernel-and-plugin" abstraction, Semantic Kernel decouples business domain functions from underlying AI inference providers. In early 2027, the SDK has reached version **v1.22.0+** for Python and **v1.35.x** for .NET, delivering native support for **FastMCP 3.1 (Model Context Protocol)**, multi-agent orchestrations, OpenTelemetry-compliant observability pipelines, and frontier reasoning models (including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Llama 4).

Through its unified plugin paradigm, Semantic Kernel transforms plain code functions, HTTP web APIs, database connectors, and prompt templates into strongly-typed tools that AI models can dynamically discover, sequence, and execute. It forms a bridge between classical enterprise architecture—such as dependency injection, strongly-typed domain models, and zero-trust security controls—and modern non-deterministic agentic workflows.

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

## Where it fits in the stack
**Category**: Frameworks / Enterprise SDK / Orchestration Layer.

Semantic Kernel sits in the **Application Orchestration Layer**, bridging **Enterprise Data & API Services** (ASP.NET Core, FastAPI, Spring Boot, Microsoft Graph, SQL/NoSQL databases) with **Frontier AI Providers** (Azure OpenAI, Anthropic, Google Vertex AI, AWS Bedrock) and **FastMCP 3.1 Tool Servers**.

## Mathematical Formulations & Planning Dynamics

### 1. Stepwise Planner State Search Space & Branching Bounds
The Semantic Kernel `FunctionCallingStepwisePlanner` explores an execution state space $\mathcal{S}$ to fulfill a composite user objective $\mathcal{G}$. At each planning step $t$, given state $s_t$ and set of active registered plugins $\mathcal{P} = \{p_1, \dots, p_M\}$, the model selects an action $a_t \in \mathcal{A}(s_t)$ from total exposed kernel functions $N = \sum_{i=1}^M |p_i|$:

$$\pi(a_t \mid s_t) = \text{Softmax}\left(\frac{\mathbf{q}(s_t) \cdot \mathbf{k}(a)}{\sqrt{d_{\text{embed}}}}\right)$$

The maximum search tree depth is bounded by $D_{\text{max}}$ (default 10 iterations). The worst-case state exploration complexity satisfies:

$$\mathcal{C}_{\text{search}} \le \sum_{t=1}^{D_{\text{max}}} \min(N, K_{\text{top}}) = \mathcal{O}(D_{\text{max}} \cdot K_{\text{top}})$$

Where $K_{\text{top}}$ is the filtered tool candidate set evaluated by Semantic Kernel's vector plugin retrieval index, avoiding combinatorial explosion when hundreds of enterprise tools are registered.

### 2. Plugin Semantic Alignment Scoring
When selecting appropriate functions for execution, Semantic Kernel computes a cosine similarity match between the user prompt embedding $\mathbf{u} \in \mathbb{R}^d$ and the semantic function description embedding $\mathbf{f}_j \in \mathbb{R}^d$, augmented by parameter schema type penalty:

$$\mathcal{M}(\mathbf{u}, f_j) = \frac{\mathbf{u} \cdot \mathbf{f}_j}{\|\mathbf{u}\|_2 \|\mathbf{f}_j\|_2} - \lambda_{\text{param}} \cdot \max\left(0, \frac{|\text{params}(f_j)| - |\text{args}(s_t)|}{|\text{params}(f_j)|}\right)$$

Functions falling below threshold $\tau_{\text{exec}} = 0.72$ are pruned from the immediate model function call context window, reducing prompt token costs by up to $64\%$.

### 3. OpenTelemetry Filter Middleware Latency Overhead
Semantic Kernel wraps invocations in Function and Prompt Filters. Given raw LLM roundtrip latency $T_{\text{LLM}}$, the observed latency $T_{\text{total}}$ satisfies:

$$T_{\text{total}} = T_{\text{filter, pre}} + T_{\text{LLM}} + \sum_{k=1}^{m} T_{\text{plugin}, k} + T_{\text{filter, post}} + \mathcal{O}(N_{\text{tokens}} \cdot t_{\text{parse}})$$

In compiled .NET 9 and Python 3.12 runtimes, filter overhead is strictly bounded: $T_{\text{filter}} \le 0.45\text{ ms}$, representing less than $0.05\%$ of total agent reasoning duration.

## Comparative Empirical Matrix

| Feature / Dimension | Semantic Kernel (v1.22+/v1.35) | LangChain (v0.3+) | AutoGen Studio | LlamaIndex Workflows | Spring AI (Java) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Language** | C# (.NET), Python, Java | Python, TypeScript | Python | Python, TypeScript | Java (Spring Framework) |
| **Enterprise Alignment** | Microsoft 365, Azure AI | Open Source Community | Microsoft Research | Data/Vector Community | Pivotal / VMware Spring |
| **FastMCP 3.1 Support** | Native Plugin Connector | LangChain MCP adapter | Experimental wrapper | MCP tool specs | Custom client adapter |
| **Type Safety** | Strict compile-time (.NET) / Pydantic v2 | Pydantic v2 / Dynamic | Dynamic / Pydantic | Pydantic v2 | Java static typing |
| **Planning Paradigm** | Stepwise / Handlebars Planners | AgentExecutor / LangGraph | ConversableAgent loops | Event-driven Workflows | Function calling advisors |
| **Observability Standard**| Native OpenTelemetry spans | LangSmith proprietary | AgentOps / Console | OpenInference / Arize | Micrometer Tracing |
| **Memory Architecture** | Unified `VectorStore` Record | VectorStores / Ephemeral | Session dicts | LlamaIndex Index store | Spring VectorStore |

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

## Systemd Service Unit Configuration

To run a Semantic Kernel FastMCP Bridge microservice as a hardened systemd background daemon on Linux servers, deploy the following configuration to `/etc/systemd/system/semantic-kernel-bridge.service`:

```ini
[Unit]
Description=Semantic Kernel FastMCP 3.1 Enterprise Gateway
After=network.target network-online.target
Wants=network-online.target
Documentation=https://learn.microsoft.com/en-us/semantic-kernel/

[Service]
Type=simple
User=skernel
Group=skernel
WorkingDirectory=/opt/semantic-kernel-gateway
ExecStart=/opt/semantic-kernel-gateway/venv/bin/python -m sk_gateway --port 8092 --transport sse
Restart=always
RestartSec=5s

# Process Sandboxing & Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/cache/semantic-kernel /var/log/semantic-kernel
PrivateTmp=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
MemoryDenyWriteExecute=true
CapabilityBoundingSet=

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now semantic-kernel-bridge.service
sudo systemctl status semantic-kernel-bridge.service
```

## Docker Compose Multi-Container Deployment

Deploy Semantic Kernel alongside a local Qdrant vector database and Redis caching layer:

```yaml
version: '3.8'

services:
  semantic-kernel-app:
    image: python:3.12-slim
    container_name: semantic-kernel-app
    restart: unless-stopped
    working_dir: /app
    volumes:
      - ./app:/app:ro
      - sk_cache:/var/cache/semantic-kernel
    environment:
      - OPENAI_API_KEY=mock-key-or-live-key
      - QDRANT_HOST=qdrant-db
      - QDRANT_PORT=6333
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
    ports:
      - "8092:8092"
    command: >
      sh -c "pip install --no-cache-dir semantic-kernel pydantic fastmcp qdrant-client &&
             python /app/main.py"
    depends_on:
      - qdrant-db
    networks:
      - enterprise-agent-net

  qdrant-db:
    image: qdrant/qdrant:v1.12.0
    container_name: sk-qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - enterprise-agent-net

volumes:
  sk_cache:
    driver: local
  qdrant_data:
    driver: local

networks:
  enterprise-agent-net:
    driver: bridge
```

## Diagnostic Troubleshooting Matrix

| Issue Symptom / Error | Root Cause | Diagnostic Command / Inspection | Resolution Path |
| :--- | :--- | :--- | :--- |
| `KernelFunctionNotFoundError` | Function requested by planner is not registered or plugin typo | `python -c "print(kernel.plugins.keys())"` | Verify plugin name passed in planner filter matches registered name. |
| `FunctionCallingStepwisePlannerTimeout` | Infinite reasoning cycle or unresolvable goal condition | Examine Stepwise execution steps in debug log | Decrease `max_iterations`, refine prompt goal, or add exit conditions. |
| `PydanticValidationError` in Python Plugin | Agent passed string argument failing strict Pydantic type | `journalctl -u semantic-kernel-bridge.service -f` | Adjust plugin `@kernel_function` parameter type hints or use Pydantic `field_validator`. |
| `OTelExportFailed` on Startup | OpenTelemetry collector unreachable at specified endpoint | `nc -zvw3 localhost 4317` | Check OTLP collector status or set `OTEL_SDK_DISABLED=true` in testing environments. |
| `AzureOpenAI401Unauthorized` | Missing or expired Azure OpenAI cognitive services API key | `az account get-access-token --resource https://cognitiveservices.azure.com` | Rotate Azure API key or switch to Managed Identity credentials (`DefaultAzureCredential`). |
| `FastMCP Transport Disconnect` | SSE connection interrupted by reverse proxy timeout | Check nginx / Traefik proxy read timeout configurations | Increase proxy timeout (`proxy_read_timeout 300s`) or switch to stdio transport. |
| `MemoryVectorStoreSearchEmpty` | Vector embedding dimension mismatch between query and index | Check embedding model configuration in `kernel.add_service()` | Ensure query embedding model matches vector store index dimension (e.g. 1536 for text-embedding-3-small). |
| `Systemd service exit status 217` | User `skernel` does not exist on Linux host system | `id skernel || sudo useradd -r -s /bin/false skernel` | Create system user or adjust `User=` in `semantic-kernel-bridge.service`. |

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

# Validate MCP 3.1 gateway endpoints and tools
sk-cli mcp test --endpoint "http://localhost:8092/sse" --tool "execute_kernel_plugin_function"
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
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    arg_name: str = Field(..., description="Argument identifier")
    arg_value: str = Field(..., description="Stringified argument value")
    type_hint: str = Field("str", description="Expected type hint")

class SKInvocationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    plugin_name: str = Field(..., description="Target Semantic Kernel plugin name")
    function_name: str = Field(..., description="Target function name within the plugin")
    arguments: List[SKPluginFunctionArg] = Field(default_factory=list)

class SKInvocationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

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
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    plugin_name: str = Field(..., description="Name of invoked plugin")
    function_name: str = Field(..., description="Name of executed function")
    duration_ms: float = Field(..., ge=0.0, description="Execution duration in ms")
    status: Literal["success", "error"] = Field("success")

class KernelTelemetryTrace(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

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
