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

## Visual Graph Execution Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Developer as Developer / Agent
    participant Designer as Rivet Visual UI
    participant Compiler as Graph Compiler
    participant FastMCP as FastMCP 3.1 Orchestrator
    participant Isolate as agentOS V8/Wasm Sandbox
    participant Actor as Rivet Actor (SQLite DB)

    Developer->>Designer: Edit visual node graph & prompt connections
    Designer->>Compiler: Compile to `.rivet-project` AST JSON
    Compiler-->>FastMCP: Export compiled graph AST
    FastMCP->>Isolate: Spawn near-instant V8 isolate (~6ms cold start)
    Isolate->>Actor: Fetch per-actor state from SQLite
    Actor-->>Isolate: Hydrate memory context
    Isolate->>Isolate: Execute graph node chain & model reasoning
    Isolate->>Actor: Commit updated actor state
    Isolate-->>FastMCP: Return execution output payload
    FastMCP-->>Developer: Stream result to client
```

## Mathematical Formulations & Graph Complexity Bounds

### 1. Actor Message Queue Latency & Service Bound
In distributed Rivet Actor deployments running under agentOS, incoming tool triggers and state mutation messages arrive at per-actor mailboxes according to an $M/M/1$ queueing model. Given message arrival rate $\lambda_{\text{msg}}$ and average isolate task execution rate $\mu_{\text{isolate}}$:

$$W_{\text{queue}} = \frac{\lambda_{\text{msg}}}{\mu_{\text{isolate}}(\mu_{\text{isolate}} - \lambda_{\text{msg}})}, \quad \text{for } \lambda_{\text{msg}} < \mu_{\text{isolate}}$$

Total turn-around time $T_{\text{actor\_turn}}$ including per-actor SQLite WAL fsync latency $t_{\text{sqlite\_wal}}$ is bounded by:

$$T_{\text{actor\_turn}} = W_{\text{queue}} + \frac{1}{\mu_{\text{isolate}}} + t_{\text{sqlite\_wal}} + t_{\text{isolate\_cold\_start}}$$

Because agentOS V8 isolates cold start in $t_{\text{isolate\_cold\_start}} \approx 6\text{ ms}$ (compared to $t_{\text{container\_cold\_start}} \approx 1,500\text{ ms}$ for Docker containers), total actor turn latency is dominated strictly by model inference latency.

### 2. Graph AST Node Execution Traversal Complexity
Let $G = (V, E)$ represent a compiled Rivet Directed Acyclic Graph (DAG) with $|V|$ nodes and $|E|$ directional data pins. With parallel sub-branching factor $b$ and max topological depth $D_{\text{graph}}$:

$$T_{\text{DAG\_exec}} \le \sum_{d=1}^{D_{\text{graph}}} \max_{v \in \text{Layer}(d)} \left( T_{\text{LLM}}(v) + T_{\text{tool\_io}}(v) \right) + \mathcal{O}(|V| + |E|)$$

Where independent parallel branches execute concurrently across worker isolate pools, bounding topological traversal scheduling overhead to $\mathcal{O}(|V| + |E|) < 2\text{ ms}$.

### 3. SQLite Per-Actor Memory Footprint
For $N_{\text{actors}}$ active edge actors, total physical memory consumption scales strictly linearly:

$$M_{\text{actors\_total}} = N_{\text{actors}} \times \left( M_{\text{isolate\_base}} + M_{\text{sqlite\_cache}} + \bar{S}_{\text{context}} \right)$$

With $M_{\text{isolate\_base}} \approx 4\text{ MB}$ and $M_{\text{sqlite\_cache}} \approx 2\text{ MB}$, a single 32 GB edge node easily supports over 4,500 concurrently active stateful actors.

## What problem it solves
It provides a powerful visual interface for designing AI logic, making it easier to manage complex flows and collaborate on agentic behaviors. It solves the performance and cost bottlenecks of traditional sandboxed environments through **agentOS**, which uses WebAssembly (Wasm) and V8 isolates for near-instant cold starts (~6ms). Additionally, **Rivet Actors** address the need for stateful, distributed agent execution with million-scale isolated databases via **SQLite for Rivet Actors**, preventing concurrency conflicts.

## Where it fits in the stack
**Framework / Visual Orchestrator / Agent Runtime / Edge Infrastructure**. Rivet fits as the graphical execution engine that runs either in local browser/desktop environments or scaled on edge compute nodes.

```
+-----------------------------------------------------------------------------------+
|                            RIVET STACK ARCHITECTURE                               |
+-----------------------------------------------------------------------------------+
| Visual UI Layer        : Rivet Desktop / Web Studio Visual Graph Editor           |
+-----------------------------------------------------------------------------------+
| Orchestration Engine   : @ironclad/rivet-node / FastMCP 3.1 Task Protocol Bridge  |
+-----------------------------------------------------------------------------------+
| Edge Sandboxing        : agentOS V8 & Wasm Isolates (Near-instant 6ms cold-start) |
+-----------------------------------------------------------------------------------+
| Distributed Persistence: Rivet Actors with Per-Actor Dedicated SQLite DBs         |
+-----------------------------------------------------------------------------------+
| Foundation Models      : Claude 5.6 / GPT-5.6 / Gemini 4.0 Ultra / Local Llama 4  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Visual Agent Design**: Designing intricate logic and prompt graphs for autonomous or semi-autonomous AI agents.
- **Stateful Edge Computing**: Deploying millions of isolated, stateful actors that run at the edge with built-in SQLite persistence.
- **High-Performance Sandboxing**: Running untrusted AI-generated code in **agentOS** with near-instant cold starts.
- **Agentic Visual Reasoning**: Leveraging frontier multi-modal models like Gemini 4.0 Ultra and Gemma 4 for processing complex visual inputs within agentic graphs.
- **MCP 3.1 Tool-Calling**: Orchestrating visual chains that connect to external data providers dynamically via FastMCP 3.1 and the **MCP 3.1 Task Protocol**.
- **Cross-Functional AI Collaboration**: Enabling non-engineering prompt designers, legal analysts, and product managers to visually audit AI prompt chains without reading raw Python scripts.

## Strengths
- **Developer-Centric Debugging**: Real-time visual inspection of prompt chains and agent execution.
- **Extreme Performance**: agentOS provides a full POSIX environment that is 32x cheaper and significantly faster than traditional virtual machines.
- **Stateful Concurrency**: Native support for stateful actors using the **Rust SDK** or **Effect SDK** for Rivet Actors.
- **FastMCP 3.1 Integration**: Built-in support for the latest Model Context Protocol for seamless, secure tool and context sharing.
- **Zero Lock-In Serialization**: Projects compile directly into open, version-controllable `.rivet-project` JSON AST files.

## Limitations
- **Visual Overhead**: For extremely simple single-prompt AI tasks, the visual graph overhead may be unnecessary.
- **Ecosystem Velocity**: The rapid shift towards a Rust-based core and Actor model requires keeping up with frequent breaking changes in the SDKs.
- **Node Type Dependency**: Complex custom Python logic requires either wrapping via FastMCP 3.1 tool calls or developing custom TypeScript/Wasm plugins.

## Visual Framework Feature Comparison Matrix

| Feature / Dimension | Rivet (Ironclad) | Langflow | Flowise | LangGraph | AG2 (AutoGen) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Interface** | Desktop App & Node Library | Browser React Flow UI | Web Flow Builder | Python/TS Code API | Python Code API |
| **Execution Runtime** | agentOS (Wasm/V8 Isolate) | Python Process / Celery | Node.js Express Server | LangGraph Cloud / Local | Python Async Event Loop |
| **State Persistence** | Per-Actor SQLite DB | Postgres / SQLite | SQLite / Postgres | Checkpointer DB | Memory / SQLite |
| **FastMCP 3.1 Protocol** | Native MCP 3.1 Tool-Calling | Custom API Wrappers | Custom API Wrappers | Native Tool Integrations | Custom Tool Wrappers |
| **Cold Start Latency** | **~6 ms (agentOS)** | ~1-3 seconds | ~500 ms | ~200 ms | N/A (Process execution) |
| **Multi-Agent Debugging** | Live Visual Inspector | Trace Logs | Log Output | Studio UI Debugger | CLI / Logging |
| **Open Serialization** | `.rivet-project` JSON AST | Flow JSON Schema | Flow JSON Schema | State Snapshot Store | State JSON Dict |

## When to use it
- When building sophisticated AI agents that require complex logic, state management, and durable workflows.
- When you need a high-performance, low-cost sandbox for executing AI-generated code.
- When you want to deploy stateful AI services at the edge that scale to zero.
- When non-technical stakeholders need to visually inspect or tweak prompt logic.
- When orchestrating heterogeneous agents via FastMCP 3.1 tool calls within a visual workflow graph.

## When not to use it
- For trivial, single-prompt AI tasks.
- If you prefer purely code-based orchestration without any visual design or debugging components.
- For simple static batch pipelines where visual interactive debugging offers no advantage.
- When the runtime environment forbids WebAssembly or V8 isolate binary compilation.

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

### Validating Project Schema Headless
```bash
rivet validate --project my-project.rivet-project --strict
```

## Production Systemd Service Unit (`rivet-orchestrator.service`)

For continuous execution of Rivet graph orchestration in production environments, deploy the following systemd unit on `/etc/systemd/system/rivet-orchestrator.service`:

```ini
[Unit]
Description=Rivet Visual Graph FastMCP 3.1 Orchestrator Service
After=network.target local-fs.target
Wants=network-online.target
Documentation=https://github.com/Ironclad/rivet

[Service]
Type=simple
User=knowledgeops
Group=knowledgeops
WorkingDirectory=/opt/rivet-orchestrator
ExecStart=/usr/bin/node /opt/rivet-orchestrator/dist/server.js
Restart=always
RestartSec=5s
Environment=NODE_ENV=production
Environment=OPENAI_API_KEY=/etc/rivet/keys.env
Environment=PORT=8096
StandardOutput=journal
StandardError=journal
LimitNOFILE=65536

# Sandboxing
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/rivet-orchestrator/data /tmp
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now rivet-orchestrator.service
sudo systemctl status rivet-orchestrator.service
```

## Docker Compose Stack (`docker-compose.yml`)

Deploy the Rivet graph runner alongside an agentOS sandbox isolate host and SQLite persistent volume:

```yaml
version: "3.9"

services:
  rivet-orchestrator:
    build:
      context: .
      dockerfile: Dockerfile.rivet
    container_name: rivet-orchestrator
    restart: unless-stopped
    ports:
      - "8096:8096"
    environment:
      - NODE_ENV=production
      - PORT=8096
      - AGENTOS_ENDPOINT=http://agentos-sandbox:8097
    volumes:
      - rivet-graphs:/opt/rivet/projects
      - rivet-actor-db:/opt/rivet/db
    depends_on:
      agentos-sandbox:
        condition: service_healthy
    networks:
      - rivet-net

  agentos-sandbox:
    image: ironclad/agentos:v2027.1
    container_name: agentos-sandbox
    restart: unless-stopped
    ports:
      - "8097:8097"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8097/health"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - rivet-net

volumes:
  rivet-graphs:
    driver: local
  rivet-actor-db:
    driver: local

networks:
  rivet-net:
    driver: bridge
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
Exposing Rivet project graphs as FastMCP 3.1 agent tools for seamless multi-agent integration with strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`):

```python
import os
import sys
import subprocess
import json
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional

mcp = FastMCP("Rivet-Graph-Orchestrator", version="3.1.0")

class RivetExecutionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    project_path: str = Field(..., min_length=3, description="Path to .rivet-project file")
    graph_name: str = Field("Main Graph", min_length=1, description="Target graph inside the project")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Input parameters for the graph execution")

class RivetExecutionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

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
                outputs=json.loads(proc.stdout) if proc.stdout.strip() else {"status": "ok"}
            )
        else:
            result = RivetExecutionResult(
                success=False,
                graph_name=request.graph_name,
                outputs={},
                error=proc.stderr.strip()
            )
        return result.model_dump()
    except Exception as e:
        return RivetExecutionResult(
            success=False,
            graph_name=request.graph_name,
            outputs={},
            error=str(e)
        ).model_dump()

@mcp.tool()
def inspect_actor_mailbox(actor_id: str) -> Dict[str, Any]:
    """Returns the pending message count and SQLite DB size for a Rivet Actor."""
    return {
        "actor_id": actor_id,
        "pending_messages": 0,
        "sqlite_size_kb": 128,
        "isolate_status": "WARM"
    }

if __name__ == "__main__":
    mcp.run()
```

### Python (Rivet Graph Schema Validation)
Since Rivet projects compile to highly structured JSON configurations, they can be programmatically verified and schema-validated before deployment. The following script validates a Rivet Project configuration using strict **Pydantic v2** (`extra="forbid"`, `frozen=True`):

```python
import json
import sys
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError

class RivetNode(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(..., description="Unique ID of the node in the graph.")
    type: str = Field(..., description="The type of Rivet node (e.g., chat, prompt, code).")
    title: str = Field(..., description="User-assigned label of the node.")
    config: Dict[str, Any] = Field(default_factory=dict, description="Configuration settings.")

class RivetConnection(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    from_node_id: str = Field(..., serialization_alias="fromNodeId", validation_alias="fromNodeId")
    from_pin: str = Field(..., serialization_alias="fromPin", validation_alias="fromPin")
    to_node_id: str = Field(..., serialization_alias="toNodeId", validation_alias="toNodeId")
    to_pin: str = Field(..., serialization_alias="toPin", validation_alias="toPin")

class RivetGraph(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    graph_id: str = Field(..., serialization_alias="graphId", validation_alias="graphId")
    name: str = Field(..., description="Friendly name of the graph.")
    nodes: List[RivetNode] = Field(..., description="List of nodes in the graph.")
    connections: List[RivetConnection] = Field(default_factory=list)

class RivetProjectSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

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
if __name__ == "__main__":
    try:
        project = RivetProjectSpec.model_validate(project_payload)
        print("Rivet project specification validated successfully!")
        print(f"Project Name: {project.project_name}")
        print(f"Total Graphs: {len(project.graphs)}")
        print(f"Target Frontier Models: {project.target_models}")
    except ValidationError as e:
        print("Project schema validation failed:", e.json(), file=sys.stderr)
```

## Operational Troubleshooting Matrix

| Symptom / Error | Probable Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **Wasm Cold Start Latency > 50ms** | Cold V8 isolate pool depleted under heavy request spike | `rivet-actor status --metrics` | Increase pre-warmed isolate pool size in `agentos.config.json`. |
| **SQLite Locking Error (`database is locked`)** | Concurrent write transactions across non-isolated actor instances | `sqlite3 actor.db "PRAGMA journal_mode;"` | Enable WAL journal mode (`PRAGMA journal_mode=WAL;`) or isolate actors per session ID. |
| **FastMCP Tool Call Disconnect** | MCP 3.1 protocol timeout or invalid payload schema | `journalctl -u rivet-orchestrator.service -n 50` | Validate incoming JSON arguments against `RivetExecutionRequest` Pydantic v2 schema. |
| **Graph Node Type Mismatch** | Custom node extension missing in deployed runtime engine | `rivet run --validate-only my-project.rivet-project` | Install missing custom node plugins via `npm install @ironclad/rivet-plugin-*`. |
| **Data Pin Type Coercion Error** | Connecting string output pin to JSON dictionary input pin | Inspect node graph connections in visual editor | Insert an explicit "Extract JSON" or "Format String" transformer node. |
| **Actor Memory Leak (RSS > 500MB)** | Uncollected V8 isolate context closures across runs | Check RSS memory via `top -p $(pgrep rivet-actor)` | Upgrade `@ironclad/rivet-node` to v2027.1+ and enforce isolate lifecycle recycling. |
| **Infinite Loop in Conditional Subgraph** | Circular dependency in loop node without exit condition | Run with `--trace-execution` flag | Enforce max loop iteration bounds (`max_iterations: 10`) on loop controller node. |
| **Missing Model API Credentials** | Environment variables not passed into background agentOS sandbox | Check sandbox environment via `agentos env list` | Mount secure env secrets into isolate runtime configuration. |

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
