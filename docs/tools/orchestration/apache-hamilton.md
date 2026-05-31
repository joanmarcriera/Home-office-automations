# Hamilton

## What it is
Hamilton is a general-purpose micro-orchestration framework for creating dataflows from simple Python functions. Unlike traditional macro-orchestrators (like Airflow), Hamilton focuses on how code is structured *inside* a task, rather than how tasks are scheduled on a cluster.

## What problem it solves
It solves the "unmaintainable spaghetti code" problem in data and ML pipelines. By mapping function names to output artifacts, Hamilton ensures that lineage is baked into the code, making it self-documenting, unit-testable, and easy to modify.

## Where it fits in the stack
**Micro-Orchestration / Dataflow Framework**. It sits between your raw Python code and your macro-orchestration layer.

## Typical use cases
- **Feature Engineering**: Creating complex, versioned features for ML models with clear lineage.
- **LLM Pipelines**: Orchestrating prompt chains, retrieval steps, and model calls where logic needs to be modular and testable.
- **Web Request Logic**: Breaking down complex API response generation into manageable, reusable functions.
- **Interactive Notebooks**: Replacing monolithic notebook cells with structured Hamilton dataflows for better reproducibility.

## Strengths
- **Lineage as Code**: The DAG is defined by function signatures, making it impossible to have "hidden" dependencies.
- **Infrastructure Agnostic**: Runs anywhere Python runs—from a local script to a Spark cluster or a Lambda function.
- **Testability**: Every transformation is a standard Python function, making unit testing trivial.
- **Visualization**: Built-in support for visualizing the dataflow DAG.
- **Hamilton UI**: A dedicated interface for tracking, versioning, and monitoring dataflow executions.

## Limitations
- **No Built-in Scheduler**: Requires an external system (Cron, Airflow, Prefect) for scheduling and resource management.
- **Python Only**: Primarily focused on the Python ecosystem.
- **Learning Curve**: Requires a shift in mindset from imperative scripts to declarative, function-based dataflows.

## When to use it
- When your data transformation or ML pipeline logic is becoming too complex to manage in a single script or notebook.
- If you need clear data lineage and auditability for regulatory or debugging purposes.
- When you want to reuse dataflow logic across different environments (e.g., local development vs. production).

## When not to use it
- For very simple scripts where the overhead of defining functions feels unnecessary.
- If you need a full-featured platform for scheduling, retries, and distributed worker management (use Airflow instead).

## Licensing and cost
- **Open Source**: Yes (BSD 3-Clause License)
- **Cost**: Free
- **Self-hostable**: Yes

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

# Scaffolding a new Hamilton project (if supported by community plugins)
hamilton init my_new_project
```

## Python examples
Hamilton's power comes from its Python API and drivers.

```python
from hamilton import driver
from hamilton.plugins import h_matplotlib

# Using a specialized driver for visualization or tracking
dr = driver.Builder() \
    .with_modules(my_functions) \
    .with_adapter(h_matplotlib.MatplotlibWriter()) \
    .build()

# Execute and visualize inline (e.g., in Jupyter)
dr.display_all_functions()
```

## Related tools / concepts
- [Apache Airflow](apache-airflow.md) — For macro-orchestration of Hamilton tasks.
- [Dagster](dagster.md) — Another asset-centric orchestrator with similar philosophies.
- [Burr](https://github.com/DAGWorks-Inc/burr) — For stateful agent loops and chatbots (complements Hamilton).
- [Pandas](../frameworks/index.md) — Often used within Hamilton functions for data manipulation.
- [Dask](../infrastructure/index.md) — Hamilton can run on Dask for distributed execution.
- [Ray](../infrastructure/index.md) — Hamilton supports Ray for scaling dataflows.
- [n8n](../../services/n8n.md) — For triggering Hamilton-based microservices.

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high

## Sources / References
- [Hamilton Official Documentation](https://hamilton.dagworks.io/)
- [GitHub Repository](https://github.com/dagworks-inc/hamilton)
- [Hamilton UI](https://github.com/DAGWorks-Inc/hamilton-ui-dev)
- [Burr: Stateful Python Applications](https://github.com/DAGWorks-Inc/burr)
