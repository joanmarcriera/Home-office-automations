# Hamilton

Hamilton is a general-purpose micro-orchestration framework for creating dataflows from simple Python functions. Unlike traditional macro-orchestrators (like Airflow), Hamilton focuses on how code is structured *inside* a task, rather than how tasks are scheduled on a cluster. As of December 2026, it is a core component for managing complex **agentic reasoning chains** and **FastMCP 3.1-based tool execution** where modularity and testability are paramount.

## What it is
Hamilton is a micro-orchestration framework that maps function names to output artifacts. By defining your dataflow as a collection of Python functions where the function signatures define the DAG, Hamilton ensures that your logic is modular, self-documenting, and easy to test.

## What problem it solves
It solves the "unmaintainable spaghetti code" problem in data and ML pipelines. It ensures that data lineage is baked into the code itself, making it impossible to have "hidden" dependencies. This is particularly valuable for LLM-based applications where prompt chains and retrieval logic can become complex and difficult to audit.

## Where it fits in the stack
**Micro-Orchestration / Dataflow Framework**. It sits between your raw Python code and your macro-orchestration layer (Airflow, Prefect). It manages the internal logic of a single task or a microservice, ensuring that the transformation steps are clearly defined.

## Typical use cases
- **LLM Reasoning Chains**: Orchestrating complex prompt chains, retrieval steps, and model calls with clear modularity.
- **FastMCP 3.1 Tool Execution**: Managing the internal logic of complex tools registered with the Model Context Protocol.
- **Feature Engineering**: Creating versioned features for ML models with baked-in lineage.
- **Web Request Logic**: Breaking down complex API response generation into manageable functions.
- **Agentic Workflows**: Providing a structured framework for agents (like those powered by Claude 5.1 or Gemma 3) to execute multi-step reasoning processes that are easy to audit.

## Strengths
- **Lineage as Code**: The DAG is defined by function signatures, ensuring transparent dependencies.
- **Infrastructure Agnostic**: Runs anywhere Python runs—local scripts, Spark, Lambda, or Kubernetes.
- **Extreme Testability**: Every transformation is a standard Python function, making unit testing trivial.
- **Visualization**: Built-in support for visualizing the dataflow DAG for better understanding and debugging.
- **Modularity**: Easy to swap out or modify individual steps in a complex reasoning chain.

## Limitations
- **No Built-in Scheduler**: Requires an external system (Cron, Airflow, Prefect) for scheduling and distributed worker management.
- **Python Only**: Primarily focused on the Python ecosystem.
- **Learning Curve**: Requires a shift from imperative scripting to a declarative, function-based mindset.

## When to use it
- When your logic (e.g., an LLM agent's reasoning process) is becoming too complex to manage in a single script.
- If you need clear data lineage and auditability for regulatory or debugging purposes.
- When you want to reuse individual transformation steps across different projects or environments.

## When not to use it
- For very simple scripts where the overhead of defining functions feels unnecessary.
- If you need a full-featured platform for scheduling, retries, and multi-tenant management (use Airflow).
- For non-Python projects.

## Getting started

### Installation
```bash
pip install sf-hamilton[visualization]
```

### Basic Example
Define your dataflow in a module (e.g., `my_functions.py`):
```python
def spend(raw_marketing_data: dict) -> float:
    return raw_marketing_data["spend"]

def signups(raw_marketing_data: dict) -> int:
    return raw_marketing_data["signups"]

def cost_per_signup(spend: float, signups: int) -> float:
    return spend / signups
```

Execute the dataflow:
```python
from hamilton import driver
import my_functions

dr = driver.Driver({}, my_functions)
results = dr.execute(["cost_per_signup"], inputs={"raw_marketing_data": {"spend": 100, "signups": 10}})
print(results)
```

## CLI examples
Hamilton includes a CLI for project scaffolding and visualization.

```bash
# Visualize a dataflow defined in a module
hamilton visualize my_functions --output dag.png

# Scaffolding a new Hamilton project
hamilton init my_new_project

# Registering a Hamilton-based agent as an MCP 3.1 server (December 2026 CLI)
hamilton mcp-register --module my_agent_logic --port 8080
```

## API examples
Hamilton's power comes from its Driver and Builder API.

```python
from hamilton import driver
import my_functions

# Building a driver with multiple modules
dr = driver.Builder() \
    .with_modules(my_functions) \
    .build()

# Execute and visualize inline
dr.display_all_functions()

# Programmatic execution for an agentic step (Gemma 3)
results = dr.execute(
    ["cost_per_signup"],
    inputs={"raw_marketing_data": {"spend": 100, "signups": 10}}
)
```

### Prompt Input Lineage Validation with Strict Pydantic v2 Schema
The following robust Python example integrates **Pydantic v2** into a Hamilton-based reasoning graph to guarantee strict input parsing and parameter safety at the boundary of an LLM prompt construction flow.

```python
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

# 1. Define input context and parameters using Pydantic v2
class PromptExecutionSchema(BaseModel):
    user_query: str = Field(..., min_length=5, max_length=500)
    system_instruction: str = Field(..., min_length=10)
    agent_model: str = Field(..., pattern="^(claude-5.1|gpt-5.5|gemini-4.0-pro|llama-4|gemma-3|qwen-3.6)$")
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    retrieval_k: int = Field(default=3, ge=1, le=20)

    @model_validator(mode="after")
    def validate_retrieval_settings(self) -> "PromptExecutionSchema":
        if self.agent_model == "gemma-3" and self.retrieval_k > 10:
            raise ValueError("Local Gemma 3 executions are constrained to retrieval_k <= 10 for resource conservation.")
        return self

# 2. Example representation of raw input payload at a node boundary
raw_inputs = {
    "user_query": "Synthesize the recent architectural changes in FastMCP 3.1.",
    "system_instruction": "You are a senior MLOps engineer with advanced expertise in orchestration workflows.",
    "agent_model": "claude-5.1",
    "temperature": 0.1,
    "retrieval_k": 5
}

# 3. Perform programmatic validation using Pydantic v2
try:
    validated_schema = PromptExecutionSchema.model_validate(raw_inputs)
    print("Hamilton Graph boundary inputs are compliant and verified!")
    print(f"Targeting Agent Model: {validated_schema.agent_model}")
    print(f"Validated query length: {len(validated_schema.user_query)}")
except ValidationError as e:
    print(f"Validation failed with error: {e.json()}")
```

## Related tools / concepts
- [Apache Airflow](apache-airflow.md) — For macro-orchestration of Hamilton tasks.
- [Dagster](dagster.md) — Asset-centric orchestrator with similar philosophies.
- [Prefect](prefect.md) — Dynamic Python-native macro-orchestrator.
- [Kestra](kestra.md) — Declarative YAML macro-orchestrator.
- [Flyte](flyte.md) — Large-scale ML orchestration.
- [Argo Workflows](argo-workflows.md) — Kubernetes-native macro-orchestrator.
- [Temporal](temporal.md) — For durable stateful functions.
- [ZenML](zenml.md) — Portable MLOps framework often compared with Hamilton.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Framework for connecting tools to agents.
- [Claude 5.1](../ai_knowledge/claude-mythos.md) — Frontier reasoning model.
- [GPT-5.5](../ai_knowledge/gpt-model.md) — Frontier reasoner.
- [Gemini 4.0 Pro](../ai_knowledge/gemini-macos.md) — SOTA model.
- [Llama 4](../ai_knowledge/llama.md) — Next-generation open-source model.
- [Gemma 3](../ai_knowledge/gemma.md) — SOTA lightweight reasoning model.
- [Qwen 3.6](../ai_knowledge/qwen.md) — Next-generation open reasoning model.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Communication standard protocol for tool-use.

## Sources / references
- [Hamilton Official Documentation](https://hamilton.dagworks.io/)
- [GitHub Repository](https://github.com/dagworks-inc/hamilton)
- [Hamilton UI](https://github.com/DAGWorks-Inc/hamilton-ui-dev)
- [Burr: Stateful Python Applications](https://github.com/DAGWorks-Inc/burr)

## Contribution Metadata
- Last reviewed: 2026-12-26
- Confidence: high
