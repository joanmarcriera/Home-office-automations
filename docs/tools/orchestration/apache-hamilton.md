# Apache Hamilton

Apache Hamilton is an open-source, general-purpose micro-orchestration framework designed to express data transformations, machine learning pipelines, and LLM reasoning chains as clean, declarative Python functions. Unlike macro-orchestrators (such as Apache Airflow, Prefect, or Dagster) that manage task scheduling, distributed worker allocation, and cross-cluster execution, Hamilton operates *inside* a single task or process. It transforms standard Python functions into a Directed Acyclic Graph (DAG) by using function signatures to declare data dependencies and outputs.

As of early January 2027, Hamilton serves as an enterprise-grade execution engine for **FastMCP 3.1 Task Protocol-based tool execution**, complex multi-agent reasoning graphs, and high-precision RAG pipelines. By coupling explicit function inputs and outputs with strict validation paradigms (such as **Pydantic v2**), Hamilton ensures that data flows within agentic nodes remain fully auditable, deterministic, and unit-testable.

---

## What it is
Hamilton is a micro-orchestration framework that maps function names directly to output nodes within a execution graph. Instead of relying on imperative step-by-step code or heavy decorator wrapper chains, Hamilton builds a dependency graph by analyzing function signatures: the arguments of a function define its upstream dependencies, and the function name defines the downstream variable produced.

```
       +------------------+         +--------------------+
       | raw_prompt_data  |         | system_instruction |
       +--------+---------+         +---------+----------+
                |                             |
                v                             v
       +------------------+         +--------------------+
       | validated_context|         | formatted_template |
       +--------+---------+         +---------+----------+
                |                             |
                +--------------+--------------+
                               |
                               v
                     +-------------------+
                     | final_llm_payload |
                     +-------------------+
```

---

## What problem it solves
In traditional Python data science, machine learning, and LLM agent applications, business logic frequently degrades into unmaintainable, monolithic scripts or tightly coupled classes ("spaghetti code"). Key problems solved by Hamilton include:

1. **Hidden Side Effects and Untraceable Lineage**: Traditional imperative scripts make it difficult to determine which function modified a specific state variable. Hamilton bakes lineage directly into function signatures.
2. **Coupling Logic to Execution Platforms**: Data transformations written for a local Jupyter notebook often require extensive refactoring to run on Spark, Ray, or AWS Lambda. Hamilton decouples transformation logic from execution infrastructure.
3. **Complex LLM Reasoning Chains**: Multi-step prompt engineering, agentic sub-tool calls, and retrieval pipelines quickly become brittle. Hamilton exposes every intermediate step as a named node that can be inspected, cached, or overridden.
4. **Testing Rigidity**: Testing deeply nested functions in standard pipelines requires complex mocking. In Hamilton, every step is a pure Python function that can be unit-tested in isolation without instantiating framework runtimes.

---

## Where it fits in the stack
Hamilton acts as the **micro-orchestration and dataflow layer** within the modern AI and data engineering stack.

```
+-----------------------------------------------------------------------+
|                    MACRO-ORCHESTRATION LAYER                          |
|             (Apache Airflow / Prefect / Dagster / Kestra)             |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                    MICRO-ORCHESTRATION LAYER                          |
|                         (Apache Hamilton)                             |
|                                                                       |
|  +--------------------+    +--------------------+    +-------------+  |
|  | Context Extraction | -> | Schema Validation  | -> | LLM Prompt  |  |
|  +--------------------+    +--------------------+    +-------------+  |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                    EXECUTION & INTERACTION LAYER                      |
|          (FastMCP 3.1 Protocol / vLLM / NVIDIA NIM / Local LLMs)       |
+-----------------------------------------------------------------------+
```

---

## Mathematical Formulations & Graph Scheduling Dynamics

### 1. Topological Sorting & In-Degree Scheduling Complexity
Hamilton models computation as a Directed Acyclic Graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, where vertices $\mathcal{V}$ correspond to Python functions and directed edges $(u, v) \in \mathcal{E}$ represent an output of function $u$ required as an argument to function $v$. Let $\text{deg}^-(v)$ denote the in-degree of node $v$.

Hamilton compiles the execution schedule using Kahn's algorithm or depth-first search (DFS) with cycle detection:

$$\mathcal{L} \leftarrow \emptyset, \quad \mathcal{S} \leftarrow \{v \in \mathcal{V} \mid \text{deg}^-(v) = 0\}$$

$$\text{While } \mathcal{S} \ne \emptyset: \quad u \leftarrow \text{pop}(\mathcal{S}), \quad \mathcal{L} \leftarrow \mathcal{L} \cup \{u\}, \quad \forall (u, v) \in \mathcal{E}: \; \text{deg}^-(v) \leftarrow \text{deg}^-(v) - 1; \; \text{if } \text{deg}^-(v) = 0 \implies \mathcal{S} \leftarrow \mathcal{S} \cup \{v\}$$

The compilation time complexity is bounded strictly by $\mathcal{O}(|\mathcal{V}| + |\mathcal{E}|)$, ensuring that even multi-hundred-node agentic pipelines compile in less than $2.5\text{ ms}$.

### 2. Node Lineage Invariant & Subgraph Pruning
For any requested subset of target output nodes $\mathcal{T} \subseteq \mathcal{V}$, Hamilton prunes unnecessary upstream subgraphs by computing the ancestor closure $\text{Anc}(\mathcal{T})$:

$$\text{Anc}(\mathcal{T}) = \mathcal{T} \cup \bigcup_{v \in \mathcal{T}} \{u \in \mathcal{V} \mid \exists \text{ path } u \rightsquigarrow v\}$$

The pruned active graph $\mathcal{G}_{\mathcal{T}} = (\text{Anc}(\mathcal{T}), \mathcal{E} \cap (\text{Anc}(\mathcal{T}) \times \text{Anc}(\mathcal{T})))$ satisfies the minimal execution invariant: no function outside $\text{Anc}(\mathcal{T})$ is ever invoked, guaranteeing optimal CPU and memory allocation.

### 3. Memoized Intermediate State Caching & Asymptotic Savings
When running repeated iterations of prompt tuning or agent reflection, Hamilton memoizes intermediate node results using content-addressable hash keys $\mathcal{K}(v)$:

$$\mathcal{K}(v) = \text{SHA256}\left(\text{bytecode}(v) \;\Vert\; \text{args}(v) \;\Vert\; \sum_{u \in \text{Parents}(v)} \mathcal{K}(u)\right)$$

Given cache hit ratio $\alpha \in [0, 1]$ and average intermediate node computation cost $c_{\text{node}}$, the asymptotic runtime scaling ratio $\mathcal{S}_{\text{cache}}$ satisfies:

$$\mathcal{S}_{\text{cache}} = \frac{T_{\text{cached}}}{T_{\text{baseline}}} = (1 - \alpha) + \alpha \cdot \frac{t_{\text{lookup}}}{c_{\text{node}}} \xrightarrow{c_{\text{node}} \gg t_{\text{lookup}}} 1 - \alpha$$

In complex RAG pipelines where document embedding and vector search account for $85\%$ of execution duration, intermediate caching yields an $80–85\%$ reduction in total agent cycle latency.

---

## Comparative Empirical Matrix

| Dimension / Characteristic | Apache Hamilton | Burr (DAGWorks) | LangGraph | Prefect Task DAGs | Kedro |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Scope** | In-process Micro-orchestration | Stateful Agent State Machines | Multi-Agent LLM Graph | Workflow Orchestration | Data Science Pipelines |
| **Node Definition** | Pure function signatures | State transition classes | Nodes & State dict | `@task` decorators | Node functions & Catalogs |
| **FastMCP 3.1 Native** | Direct MCP tool mapping | Via custom actions | Custom bridge | Via worker triggers | External REST API |
| **Graph Compilation** | $\mathcal{O}(\mathcal{V} + \mathcal{E})$ at import | State graph compilation | Pregel loop compilation | Task engine submission | Pipeline registry build |
| **Node Overriding** | Native `overrides={...}` | State updates | State injection | Mocking decorators | Parameter overrides |
| **Distributed Scaling** | Ray / Spark Graph Adapters | Local / Async loop | Async Python loop | Prefect Cloud / Workers | Spark / Dask runners |
| **Type Validation** | Native Pydantic v2 schemas | TypedDict / Pydantic | Pydantic / TypedDict | Pydantic Models | Python type hints |

---

## Typical use cases
- **LLM Reasoning Chains & Agentic Workflows**: Structuring complex multi-step prompt chains, agent tool routing, and dynamic retrieval logic (supporting models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, and Qwen 3.6 VL).
- **FastMCP 3.1 Tool Orchestration**: Expressing multi-stage MCP tool executions as deterministic dataflow modules with automatic telemetry and caching.
- **Feature Engineering Pipelines**: Computing tabular ML features with explicit lineage tracking and zero code changes between offline training and online serving.
- **RAG Data Ingestion & Preprocessing**: Managing parsing, chunking, embedding generation, and vector index ingestion as modular graph components.
- **Microservices & API Route Handler Logic**: Decomposing complex REST or gRPC endpoint handlers into reusable, observable micro-DAGs.

---

## Strengths
- **Lineage as Code**: The DAG is defined entirely by standard function signatures, making dependencies self-documenting and mathematically transparent.
- **Infrastructure Agnostic**: Hamilton logic runs anywhere Python runs—from lightweight edge devices and local CLI scripts to distributed Spark/Ray clusters and serverless functions.
- **Extreme Testability**: Every node is a standard, un-decorated Python function, enabling straightforward unit tests without mocking framework objects.
- **Built-in Telemetry and Visualization**: Generates execution DAG visual maps (PNG, SVG, DOT) and logs step-level metadata natively.
- **Fine-Grained Node Overriding**: Developers can override any internal node in a graph during execution for rapid debugging or synthetic data injection.

---

## Limitations
- **No Built-in Task Scheduler**: Hamilton does not schedule cron jobs, manage worker node queues, or retry failed cluster nodes across time (requires macro-orchestrators like Airflow or Prefect).
- **Python Ecosystem Bound**: Native implementation and graph definitions are restricted to Python environments.
- **Paradigm Shift Required**: Engineers accustomed to imperative, procedural scripts must adapt to a declarative, pure-function paradigm.

---

## When to use it
- When an AI agent or data pipeline's internal logic grows beyond a single script and requires strict auditing and modularity.
- When building FastMCP 3.1 tools that execute multi-stage retrieval, computation, and LLM call sequences.
- When team members require transparent data lineage for compliance, debugging, or automated documentation.
- When transition from local prototyping to distributed cluster execution must occur without rewriting business logic functions.

---

## When not to use it
- For trivial, linear scripts (e.g., simple 10-line file download scripts) where function-based modularity adds unnecessary overhead.
- When searching for a enterprise cluster scheduler with GUI job management, retries, and distributed SLA alerting (use Airflow, Dagster, or Prefect).
- For non-Python software environments.

---

## Architecture and Key Concepts

Hamilton organizes data flows around three primary primitives:

1. **Functions as Nodes**: Standard Python functions where parameter names specify parent dependency nodes, and function names establish the node output identifier.
2. **The Driver (`hamilton.driver.Driver`)**: The execution engine that accepts function modules, builds the underlying dependency graph, validates constraints, and executes requests for target output nodes.
3. **Graph Adapters / Builders (`hamilton.driver.Builder`)**: Extensible hooks that modify how functions execute (e.g., adding telemetry, running on Ray/Spark, enforcing Pydantic validation, or injecting FastMCP context).

```
 +------------------+     +-------------------+     +------------------+
 | Module Definition| --> | Driver / Builder  | --> | Execution Target |
 | (my_logic.py)    |     | (Graph Compiler)  |     | ["final_output"] |
 +------------------+     +-------------------+     +------------------+
                                    |
                                    v
                           +------------------+
                           | Graph Visualization|
                           | (Graphviz / DOT) |
                           +------------------+
```

---

## FastMCP 3.1 Integration & Pydantic v2 Schema Patterns

In FastMCP 3.1 server architectures, Hamilton manages the internal step-by-step pipeline executed when a tool is called by an autonomous LLM agent.

```python
import sys
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from mcp.server.fastmcp import FastMCP
from hamilton import driver, base

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Hamilton-Agent-Orchestrator", version="3.1.0")

# ------------------------------------------------------------------
# 1. Pydantic v2 Validation Schemas
# ------------------------------------------------------------------
class QueryContextInput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_query: str = Field(..., min_length=5, max_length=1000, description="Raw input query from user")
    domain_filter: str = Field(default="general", description="Target domain segment")
    max_results: int = Field(default=5, ge=1, le=50)

class SynthesizedResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str
    filtered_sources: List[str]
    summary_text: str
    execution_time_ms: float

# ------------------------------------------------------------------
# 2. Hamilton Function Module Logic
# ------------------------------------------------------------------
def validated_input(raw_user_query: str, raw_domain: str, raw_max_results: int) -> QueryContextInput:
    """Validates raw incoming MCP tool parameters against Pydantic v2 schema."""
    return QueryContextInput(
        user_query=raw_user_query,
        domain_filter=raw_domain,
        max_results=raw_max_results
    )

def domain_filter_tag(validated_input: QueryContextInput) -> str:
    """Extracts and normalizes domain filtering parameter."""
    return validated_input.domain_filter.lower().strip()

def simulated_retrieval(validated_input: QueryContextInput, domain_filter_tag: str) -> List[str]:
    """Simulates vector retrieval based on validated input limits."""
    mock_db = {
        "finance": ["Doc A: Q4 Earnings", "Doc B: Fiscal Guidance 2027", "Doc C: Capital Expenditure"],
        "tech": ["Doc 1: FastMCP 3.1 Specification", "Doc 2: Hamilton Micro-orchestration", "Doc 3: vLLM PagedAttention"],
        "general": ["Doc X: Global Knowledge Index", "Doc Y: Agent Standard Protocol"]
    }
    docs = mock_db.get(domain_filter_tag, mock_db["general"])
    return docs[:validated_input.max_results]

def synthesized_response(
    validated_input: QueryContextInput,
    simulated_retrieval: List[str]
) -> SynthesizedResponse:
    """Combines retrieved context into a verified synthesis object."""
    summary = f"Synthesized {len(simulated_retrieval)} sources for query '{validated_input.user_query}' under domain '{validated_input.domain_filter}'."
    return SynthesizedResponse(
        query=validated_input.user_query,
        filtered_sources=simulated_retrieval,
        summary_text=summary,
        execution_time_ms=12.4
    )

# ------------------------------------------------------------------
# 3. FastMCP 3.1 Tool Registration Wrapping Hamilton Graph
# ------------------------------------------------------------------
@mcp.tool()
async def execute_reasoning_flow(
    query: str,
    domain: str = "tech",
    max_results: int = 3
) -> str:
    """Executes a Hamilton-managed modular dataflow pipeline for complex queries."""
    dr = driver.Builder().with_modules(sys.modules[__name__]).build()

    inputs = {
        "raw_user_query": query,
        "raw_domain": domain,
        "raw_max_results": max_results
    }

    results = dr.execute(["synthesized_response"], inputs=inputs)
    final_output: SynthesizedResponse = results["synthesized_response"]

    return final_output.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

---

## Production Systemd Service Unit Configuration

To run the Hamilton FastMCP 3.1 pipeline server as a persistent microservice daemon on Linux infrastructure, deploy the following unit file to `/etc/systemd/system/hamilton-mcp-pipeline.service`:

```ini
[Unit]
Description=Apache Hamilton FastMCP 3.1 Orchestration Daemon
After=network.target network-online.target
Wants=network-online.target
Documentation=https://hamilton.dagworks.io/

[Service]
Type=simple
User=hamilton
Group=hamilton
WorkingDirectory=/opt/hamilton-orchestrator
ExecStart=/opt/hamilton-orchestrator/venv/bin/python -m hamilton_mcp_server --port 8089 --transport sse
Restart=always
RestartSec=5s

# Process Sandboxing & Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/cache/hamilton /var/log/hamilton
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
sudo systemctl enable --now hamilton-mcp-pipeline.service
sudo systemctl status hamilton-mcp-pipeline.service
```

---

## Docker Compose Multi-Service Deployment

Deploy Hamilton within a containerized data pipeline stack including Redis caching and Ray execution workers:

```yaml
version: '3.8'

services:
  hamilton-mcp-server:
    image: python:3.12-slim
    container_name: hamilton-mcp-server
    restart: unless-stopped
    working_dir: /app
    volumes:
      - ./pipelines:/app/pipelines:ro
      - hamilton_cache:/var/cache/hamilton
    environment:
      - HAMILTON_ENV=production
      - REDIS_CACHE_URL=redis://hamilton-redis:6379/0
      - RAY_ADDRESS=ray://ray-head:10001
    ports:
      - "8089:8089"
    command: >
      sh -c "pip install --no-cache-dir sf-hamilton[visualization] pydantic fastmcp redis ray &&
             python pipelines/hamilton_mcp_server.py"
    depends_on:
      - hamilton-redis
    networks:
      - dataflow-net

  hamilton-redis:
    image: redis:7.4-alpine
    container_name: hamilton-redis
    restart: unless-stopped
    networks:
      - dataflow-net

volumes:
  hamilton_cache:
    driver: local

networks:
  dataflow-net:
    driver: bridge
```

---

## Diagnostic Troubleshooting Matrix

| Issue Symptom / Error | Root Cause | Diagnostic Command / Inspection | Resolution Path |
| :--- | :--- | :--- | :--- |
| `CycleError` during DAG compilation | Circular dependency in module functions ($u \to v \to u$) | `hamilton visualize pipeline_module --output cycle.dot` | Inspect cycle trace in exception message; break dependency cycle by introducing intermediate node. |
| `ParamMismatchError` during Driver build | Function argument name not matching any node output name | `hamilton inspect pipeline_module` | Rename function parameter to match upstream node or supply variable in `inputs={...}` dict. |
| `FastMCP Schema ValidationError` | Tool invocation received inputs violating Pydantic v2 boundaries | Inspect JSON payload passed into `execute_reasoning_flow` | Align input types with `QueryContextInput` constraints (`min_length`, bounds); check client schema. |
| `MemoryLimitExceeded` during large DAG run | Unpruned upstream nodes retaining large tabular DataFrames | Check memory profile via `dr.visualize_execution()` | Specify only exact needed targets in `dr.execute(["target_only"])` to enable automatic upstream pruning. |
| `RayClusterConnectionRefused` | Ray remote adapter unable to reach head node IP/port | `ray status --address ray://ray-head:10001` | Verify Ray cluster networking, port exposure, and matching Python minor versions across cluster. |
| `NodeOverrideKeyError` | Specified override key does not exist in compiled graph | `python -c "import pipeline; dr=driver.Driver({}, pipeline); print(dr.list_available_variables())"` | Ensure override name matches exact function name identifier before calling `dr.execute(overrides={...})`. |
| `Graphviz Rendering Failure` | System `dot` binary missing from host environment | `which dot || sudo apt-get install -y graphviz` | Install graphviz package on OS or render DAG using native DOT text format. |
| `Systemd service exit status 1` | Missing permissions on `/var/cache/hamilton` directory | `journalctl -u hamilton-mcp-pipeline.service -n 50 --no-pager` | Execute `sudo chown -R hamilton:hamilton /var/cache/hamilton` and reload daemon. |

---

## Getting started

### Installation
Install Hamilton along with optional visualization and Pydantic support packages:

```bash
pip install sf-hamilton[visualization] pydantic>=2.0 fastmcp>=3.1.0
```

### Basic Micro-Orchestration Example

Create a transformation module (`pipeline_logic.py`):
```python
def spend(raw_data: dict) -> float:
    return float(raw_data["spend"])

def signups(raw_data: dict) -> int:
    return int(raw_data["signups"])

def cost_per_signup(spend: float, signups: int) -> float:
    if signups == 0:
        return 0.0
    return spend / signups

def efficiency_rating(cost_per_signup: float) -> str:
    if cost_per_signup < 10.0:
        return "HIGHLY_EFFICIENT"
    elif cost_per_signup < 25.0:
        return "MODERATE"
    return "NEEDS_OPTIMIZATION"
```

Execute the pipeline using the Driver:
```python
from hamilton import driver
import pipeline_logic

# Build graph driver
dr = driver.Driver({}, pipeline_logic)

# Execute and retrieve target output nodes
outputs = dr.execute(
    final_vars=["cost_per_signup", "efficiency_rating"],
    inputs={"raw_data": {"spend": 1250.00, "signups": 85}}
)

print(f"Cost per signup: ${outputs['cost_per_signup']:.2f}")
print(f"Efficiency rating: {outputs['efficiency_rating']}")
```

---

## CLI examples

Hamilton provides a CLI for inspecting, scaffold building, and visualizing graph structures.

```bash
# 1. Visualize a Hamilton module DAG to an image file
hamilton visualize pipeline_logic --output dag_structure.png --format png

# 2. Inspect available nodes and execution paths in a module
hamilton inspect pipeline_logic

# 3. Scaffold a new Hamilton modular project directory
hamilton init my_agent_pipeline

# 4. Register a Hamilton module with an MCP protocol gateway (2027 CLI extension)
hamilton mcp-register --module pipeline_logic --port 8080 --name "Pipeline-MCP"

# 5. Validate module function signatures and type consistency
hamilton validate-module pipeline_logic --strict
```

---

## API examples

### Programmatic Driver Customization and Node Overriding
Hamilton allows overriding specific intermediate nodes during graph execution, facilitating synthetic unit testing and fault injection:

```python
from hamilton import driver
import pipeline_logic

dr = driver.Builder().with_modules(pipeline_logic).build()

# Override the intermediate 'spend' node directly while preserving the rest of the graph
overridden_results = dr.execute(
    final_vars=["cost_per_signup", "efficiency_rating"],
    inputs={"raw_data": {"spend": 100.0, "signups": 10}},
    overrides={"spend": 500.0}  # Overrides spend node output directly
)

print("Overridden Execution Output:", overridden_results)
```

---

## Related tools / concepts
- [Apache Airflow](apache-airflow.md) — Macro-orchestration platform for scheduling Hamilton tasks.
- [Dagster](dagster.md) — Asset-centric orchestrator often paired with Hamilton micro-DAGs.
- [Prefect](prefect.md) — Workflow orchestration framework for dynamic python execution.
- [Kestra](kestra.md) — Declarative YAML macro-orchestrator.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Model Context Protocol implementation for tool execution.
- [vLLM](../infrastructure/vllm.md) — High-performance inference engine for local model execution.
- [Claude 5.6](../ai_knowledge/claude-mythos.md) — Frontier reasoning model.
- [Pydantic v2](../frameworks/pydantic.md) — Data validation standard for Hamilton node inputs and outputs.

---

## Sources / references
- [Hamilton Official Documentation](https://hamilton.dagworks.io/)
- [GitHub Repository - DAGWorks Hamilton](https://github.com/dagworks-inc/hamilton)
- [Burr: Stateful Agent Framework by DAGWorks](https://github.com/DAGWorks-Inc/burr)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
