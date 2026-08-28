# Rivet

## What it is
Rivet is an open-source visual AI programming environment and TypeScript library developed by Ironclad. It allows developers to build, test, and debug complex multi-agent AI systems using a node-based editor. As of early 2027, it has fully integrated with the **Model Context Protocol (MCP 3.1)**, **FastMCP 3.1**, and frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Llama 4, and [Gemma 4](../ai_knowledge/local_llms.md) for high-performance visual reasoning and autonomous multi-agent coordination.

## What problem it solves
It provides a powerful visual interface for designing AI logic, making it easier to manage complex flows and collaborate on agentic behaviors. It solves the performance and cost bottlenecks of traditional sandboxed environments through **agentOS**, which uses WebAssembly (Wasm) and V8 isolates for near-instant cold starts (~6ms). Additionally, **Rivet Actors** address the need for stateful, distributed agent execution with million-scale isolated databases via **SQLite for Rivet Actors**, preventing concurrency conflicts.

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

## When to use it
- When building sophisticated AI agents that require complex logic, state management, and durable workflows.
- When you need a high-performance, low-cost sandbox for executing AI-generated code.
- When you want to deploy stateful AI services at the edge that scale to zero.

## When not to use it
- For trivial, single-prompt AI tasks.
- If you prefer purely code-based orchestration without any visual design or debugging components.

## Getting started

### Installation
To use Rivet in your Node.js project:
```bash
npm install @ironclad/rivet-node
```

To install Python validation support:
```bash
pip install pydantic
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

### Python (Rivet Graph Schema Validation)
Since Rivet projects compile to highly structured JSON configurations, they can be programmatically verified and schema-validated before deployment. The following script validates a Rivet Project configuration using **Pydantic v2**:

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

# 1. Define robust schemas for Rivet node-graph layouts
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

# 2. Simulated Rivet project specification output
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

# 3. Strictly validate the project configuration
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
