# Rivet

## What it is
Rivet is an open-source visual AI programming environment and TypeScript library developed by Ironclad. It allows developers to build, test, and debug complex multi-agent AI systems using a node-based editor. As of early 2027, it has fully integrated with the **Model Context Protocol (MCP 3.1)**, **FastMCP 3.1**, and frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Llama 4, and [Gemma 4](../ai_knowledge/local_llms.md) for high-performance visual reasoning and autonomous multi-agent coordination.

## What problem it solves
It provides a powerful visual interface for designing AI logic, making it easier to manage complex flows and collaborate on agentic behaviors. It solves the performance and cost bottlenecks of traditional sandboxed environments through **agentOS**, which uses WebAssembly (Wasm) and V8 isolates for near-instant cold starts (~6ms). Additionally, **Rivet Actors** address the need for stateful, distributed agent execution with million-scale isolated databases via **SQLite for Rivet Actors**, preventing concurrency conflicts.

## Architecture and Execution Model

Rivet bridges visual node-graph orchestration with stateful edge runtime execution using V8/Wasm isolates and dedicated actor persistence.

```
+-----------------------------------------------------------------------------------+
|                        Rivet Visual AI Architecture & Runtime                     |
+-----------------------------------------------------------------------------------+
                                          |
 1. Visual Design Environment            |
 +-------------------------------+       |
 | Rivet Desktop App / Web UI    |       |
 | - Node-Graph Visual Builder   |       |
 | - Real-time Execution Debugger|       |
 +---------------+---------------+       |
                 |                       |
                 v                       v
 2. Compiled Graph Spec (.rivet-project) |
 +-----------------------------------------------+
 | JSON / Binary Graph Abstract Syntax Tree (AST)|
 +---------------+-------------------------------+
                 |
                 v
 3. Orchestration Engine (FastMCP 3.1 Server / SDK)
 +-----------------------------------------------+
 |  @ironclad/rivet-node / FastMCP Runner        |
 |  - Model API bindings (Claude 5.6, GPT-5.6)   |
 |  - MCP 3.1 Tool-Calling Protocol              |
 +---------------+-------------------------------+
                 |
                 +-----------------------------------+
                 |                                   |
                 v                                   v
 4. Execution Sandbox (agentOS)              5. State & Memory Store
 +-------------------------------+           +-------------------------------+
 |  V8 / Wasm Isolates           |           |  Rivet Actors (Rust / Effect) |
 |  - Near-instant cold start    |---------->|  - Embedded Per-Actor SQLite  |
 |  - POSIX filesystem sandboxing|           |  - Durable State Replication   |
 +-------------------------------+           +-------------------------------+
```

## Where it fits in the stack
**Framework / Visual Orchestrator / Agent Runtime / Edge Infrastructure**. Rivet fits as the graphical execution engine that runs either in local browser/desktop environments or scaled on edge compute nodes.

## Typical use cases
- **Visual Agent Design**: Designing intricate logic and prompt graphs for autonomous or semi-autonomous AI agents.
- **Stateful Edge Computing**: Deploying millions of isolated, stateful actors that run at the edge with built-in SQLite persistence.
- **High-Performance Sandboxing**: Running untrusted AI-generated code in **agentOS** with near-instant cold starts.
- **Agentic Visual Reasoning**: Leveraging frontier multi-modal models like Gemini 4.0 Ultra and Gemma 4 for processing complex visual inputs within agentic graphs.
- **MCP 3.1 Tool-Calling**: Orchestrating visual chains that connect to external data providers dynamically via FastMCP 3.1 and the **MCP 3.1 Task Protocol**.

## Strengths
- **Developer-Centric Debugging**: Real-time visual inspection of prompt chains and agent execution.
- **Extreme Performance**: agentOS provides a full POSIX environment that is 32x cheaper and significantly faster than traditional virtual machines.
- **Stateful Concurrency**: Native support for stateful actors using the **Rust SDK** or **Effect SDK** for Rivet Actors.
- **FastMCP 3.1 Integration**: Built-in support for the latest Model Context Protocol for seamless, secure tool and context sharing.

## Limitations
- **Visual Overhead**: For extremely simple single-prompt AI tasks, the visual graph overhead may be unnecessary.
- **Ecosystem Velocity**: The rapid shift towards a Rust-based core and Actor model requires keeping up with frequent breaking changes in the SDKs.

## Visual Framework Feature Comparison Matrix

| Feature / Dimension | Rivet | Langflow | Flowise | LangGraph | AG2 (AutoGen) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Interface** | Desktop App & Node Library | Browser React Flow UI | Web Flow Builder | Python/TS Code API | Python Code API |
| **Execution Runtime** | agentOS (Wasm/V8 Isolate) | Python Process / Celery | Node.js Express Server | LangGraph Cloud / Local | Python Async Event Loop |
| **State Persistence** | Per-Actor SQLite DB | Postgres / SQLite | SQLite / Postgres | Checkpointer DB | Memory / SQLite |
| **FastMCP 3.1 Protocol** | Native MCP 3.1 Tool-Calling | Custom API Wrappers | Custom API Wrappers | Native Tool Integrations | Custom Tool Wrappers |
| **Cold Start Latency** | ~6 ms | ~1-3 seconds | ~500 ms | ~200 ms | N/A (Process execution) |
| **Multi-Agent Debugging** | Live Visual Inspector | Trace Logs | Log Output | Studio UI Debugger | CLI / Logging |

## When to use it
- When building sophisticated AI agents that require complex logic, state management, and durable workflows.
- When you need a high-performance, low-cost sandbox for executing AI-generated code.
- When you want to deploy stateful AI services at the edge that scale to zero.
- When non-technical stakeholders need to visually inspect or tweak prompt logic.

## When not to use it
- For trivial, single-prompt AI tasks.
- If you prefer purely code-based orchestration without any visual design or debugging components.
- For simple static batch pipelines where visual interactive debugging offers no advantage.

## Getting started

### Installation
To use Rivet in your Node.js project:
```bash
npm install @ironclad/rivet-node
```

To install Python validation support:
```bash
pip install pydantic fastmcp
```

### Rivet Actors Setup
To create a new stateful actor using the Rust SDK:
```bash
cargo add rivet-actor
```

### Local Development
Download the Rivet desktop application from the [Official Website](https://rivet.ironcladapp.com/) to start building graphs visually.

## CLI examples

### Running a Graph via CLI
```bash
rivet run my-project.rivet-project --graph "Main Graph" --input userInput="Hello AI"
```

### Deploying to Rivet Compute
```bash
rivet deploy --actor my-agent-actor
```

### Running a Rivet Actor locally
```bash
rivet-actor run --port 8080
```

## API examples

### Node.js TypeScript Example
```typescript
import { runGraph, loadProject, NodeId } from '@ironclad/rivet-node';

async function runRivetGraph() {
  const project = await loadProject('path/to/project.rivet-project');

  const results = await runGraph(project, {
    graph: 'Main Graph' as NodeId,
    inputs: {
      userInput: { type: 'string', value: 'Hello Rivet!' }
    },
    openAiKey: process.env.OPENAI_API_KEY,
  });

  console.log(results.output.value);
}
```

### FastMCP 3.1 Rivet Graph Orchestrator Bridge
Exposing Rivet project graphs as FastMCP 3.1 agent tools for seamless multi-agent integration:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import subprocess
import json

mcp = FastMCP("Rivet-Graph-Orchestrator")

class RivetExecutionRequest(BaseModel):
    project_path: str = Field(..., description="Path to .rivet-project file")
    graph_name: str = Field("Main Graph", description="Target graph inside the project")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Input parameters for the graph execution")

class RivetExecutionResult(BaseModel):
    success: bool
    graph_name: str
    outputs: Dict[str, Any]
    error: Optional[str] = None

@mcp.tool()
def execute_rivet_graph(request: RivetExecutionRequest) -> Dict[str, Any]:
    """
    Executes a compiled Rivet node-graph in agentOS sandbox via FastMCP 3.1 tool call.
    """
    cmd = [
        "rivet", "run", request.project_path,
        "--graph", request.graph_name,
        "--input", json.dumps(request.inputs)
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if proc.returncode == 0:
            result = RivetExecutionResult(
                success=True,
                graph_name=request.graph_name,
                outputs=json.loads(proc.stdout)
            )
        else:
            result = RivetExecutionResult(
                success=False,
                graph_name=request.graph_name,
                outputs={},
                error=proc.stderr
            )
        return result.model_dump()
    except Exception as e:
        return RivetExecutionResult(
            success=False,
            graph_name=request.graph_name,
            outputs={},
            error=str(e)
        ).model_dump()

if __name__ == "__main__":
    mcp.run()
```

### Python (Rivet Graph Schema Validation)
Since Rivet projects compile to highly structured JSON configurations, they can be programmatically verified and schema-validated before deployment. The following script validates a Rivet Project configuration using **Pydantic v2**:

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

class RivetNode(BaseModel):
    id: str = Field(..., description="Unique ID of the node in the graph.")
    type: str = Field(..., description="The type of Rivet node (e.g., chat, prompt, code).")
    title: str = Field(..., description="User-assigned label of the node.")
    config: Dict[str, Any] = Field(default_factory=dict, description="Configuration settings.")

class RivetConnection(BaseModel):
    from_node_id: str = Field(..., serialization_alias="fromNodeId", validation_alias="fromNodeId")
    from_pin: str = Field(..., serialization_alias="fromPin", validation_alias="fromPin")
    to_node_id: str = Field(..., serialization_alias="toNodeId", validation_alias="toNodeId")
    to_pin: str = Field(..., serialization_alias="toPin", validation_alias="toPin")

class RivetGraph(BaseModel):
    graph_id: str = Field(..., serialization_alias="graphId", validation_alias="graphId")
    name: str = Field(..., description="Friendly name of the graph.")
    nodes: List[RivetNode] = Field(..., description="List of nodes in the graph.")
    connections: List[RivetConnection] = Field(default_factory=list)

class RivetProjectSpec(BaseModel):
    project_name: str = Field(..., serialization_alias="projectName", validation_alias="projectName")
    version: str = Field(default="2.0.0")
    graphs: List[RivetGraph] = Field(...)
    target_models: List[str] = Field(default_factory=list, description="Frontier models utilized in this project.")

    @field_validator("target_models")
    @classmethod
    def validate_target_models(cls, v: List[str]) -> List[str]:
        allowed = ["Claude 5.6", "GPT-5.6", "Gemini 4.0 Ultra", "Llama 4", "Gemma 4"]
        for model in v:
            if not any(m in model for m in allowed):
                raise ValueError(f"Model {model} must be an early 2027 SOTA model: {allowed}")
        return v

# Simulated Rivet project specification output
project_payload = {
    "projectName": "Visual Customer Agent",
    "version": "2.4.0",
    "graphs": [
        {
            "graphId": "graph-user-support",
            "name": "Support Pipeline",
            "nodes": [
                {
                    "id": "node-1",
                    "type": "chat",
                    "title": "LLM Generator Node",
                    "config": {"temperature": 0.2}
                }
            ],
            "connections": [
                {
                    "fromNodeId": "node-1",
                    "fromPin": "output",
                    "toNodeId": "node-2",
                    "toPin": "input"
                }
            ]
        }
    ],
    "target_models": ["Claude 5.6", "Gemma 4"]
}

# Strictly validate the project configuration
try:
    project = RivetProjectSpec(**project_payload)
    print("Rivet project specification validated successfully!")
    print(f"Project Name: {project.project_name}")
    print(f"Total Graphs: {len(project.graphs)}")
    print(f"Target Frontier Models: {project.target_models}")
except Exception as e:
    print(f"Project schema validation failed: {e}")
```

## Related tools / concepts
- [Langflow](langflow.md) — Visual workflow builder.
- [Flowise](../ai_knowledge/flowise.md) — Node-based UI for LLM flows.
- [AG2](ag2.md) — Multi-agent conversation framework.
- [Promptfoo](../benchmarking/promptfoo.md) — Evaluation and testing for Rivet graphs.
- [LangGraph](langgraph.md) — Code-centric multi-agent orchestration.
- [PydanticAI](pydantic-ai.md) — Type-safe agent framework from Pydantic.
- [Temporal](../orchestration/temporal.md) — Durable execution often compared with Rivet Workflows.
- [Claude Code](../development_ops/claude-code.md) — Supported via Sandbox Agent SDK integration.

## Sources / References
- [Official Website](https://rivet.ironcladapp.com/)
- [Rivet Developer Blog](https://rivet.dev/blog/)
- [GitHub Repository](https://github.com/Ironclad/rivet)
- [agentOS Documentation](https://sandboxagent.dev/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
