# LangSmith

## What it is
LangSmith is a unified platform for debugging, testing, evaluating, and monitoring LLM applications. It is part of the LangChain ecosystem but is model-agnostic and can be used with any LLM framework. As of July 2026, it serves as the industry-standard "control plane" for complex agentic fleets, featuring native support for [MCP 3.0](../../tools/automation_orchestration/mcp.md) observability.

## What problem it solves
It addresses the "black box" nature of LLMs by providing full visibility into the execution traces of complex chains and agents. It provides tools for creating "golden" evaluation datasets, running automated tests (LLM-as-a-judge), and monitoring production performance for cost, latency, and quality regressions. With the July 2026 update, it now utilizes **ClickHouse** for high-volume OLAP telemetry, enabling sub-second analytics on millions of traces.

## Where it fits in the stack
**Benchmarking / Observability**. It is the primary tool for managing the lifecycle of LLM applications from prototype to production.

## Typical use cases
- **Debugging Agent Loops**: Inspecting intermediate steps and tool calls to find where an agent "stalls" or fails.
- **Golden Dataset Curation**: Creating high-quality reference datasets for regression testing.
- **Production Monitoring**: Real-time tracking of token usage, cost, and latency across large-scale deployments.
- **Collaborative Prompting**: Version-controlled prompt engineering with team-wide testing support.
- **Fleet Management**: Deploying and managing agent "fleets" via LangSmith Deployment (Fleet).
- **Agentic Session Replay**: Utilizing [AgentOps](../process_understanding/agentops.md) integration for visual execution graphs and step-by-step session replays.

## Strengths
- **Deep Ecosystem Integration**: Seamlessly works with LangChain, [LangGraph](../frameworks/langgraph.md), and FastMCP 3.0.
- **High-Fidelity Tracing**: Visualizes hierarchical execution paths including nested tool calls and parallel branches.
- **Advanced Evaluators**: Native support for complex automated grading using frontier models like [Claude 4.8 Opus](../providers/anthropic.md).
- **Polly AI Integration**: Embedded assistant for natural language analysis of failure patterns and performance trends.
- **Scalable Telemetry**: Powered by ClickHouse for real-time OLAP queries on massive agentic datasets.

## Limitations
- **SaaS Lock-in**: While self-hosting is available for enterprise, the primary experience is a proprietary SaaS.
- **Cost at Scale**: High-volume tracing in production can become expensive if not sampled correctly.
- **Learning Curve**: Advanced evaluation and "Fleet" deployment features require significant configuration.

## When to use it
- When building complex LLM applications that require deep tracing for debugging.
- When transitioning from a prototype to a production environment where reliability is critical.
- When collaborating on prompt engineering and evaluation datasets.

## When not to use it
- For very simple, single-call LLM scripts where a full observability platform is overkill.
- If strict data privacy requirements forbid any cloud-based telemetry (and enterprise self-hosting is not feasible).
- When a lightweight, open-source alternative like [Promptfoo](promptfoo.md) is sufficient.

## Getting started
LangSmith requires an API key and the `langsmith` Python package.

### 1. Installation
```bash
pip install langsmith
```

### 2. Configuration
Set your environment variables to enable tracing:
```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="ls__..."
export LANGSMITH_PROJECT="my-agent-v1"
```

### 3. Hello-World Trace
```python
from langsmith import traceable
from openai import OpenAI

client = OpenAI()

@traceable
def my_agent(question: str):
    return client.chat.completions.create(
        model="gpt-5.5",
        messages=[{"role": "user", "content": question}]
    )

my_agent("What is the state of MCP in June 2026?")
```

## CLI examples
The LangSmith CLI helps manage datasets and experiments from the terminal.

```bash
# Log in to your LangSmith account
langsmith login

# Create a new dataset from a CSV file
langsmith dataset create "Golden Tasks" --csv ./tasks.csv

# Run an evaluation experiment against a dataset
langsmith run --dataset "Golden Tasks" --config ./eval_config.yaml
```

## API examples
Automated evaluation is a core feature of LangSmith.

### Running an Evaluation
```python
from langsmith import Client, evaluate

client = Client()

# Define the function to evaluate
def my_app(inputs):
    return "The answer is " + inputs["question"]

# Run automated evaluation
results = evaluate(
    my_app,
    data="My Golden Dataset",
    evaluators=["qa_correctness"],
    experiment_prefix="v1-baseline"
)
```

### Programmatic Trace Analysis (Polly)
Polly can be queried via the SDK to analyze traces.
```python
from langsmith import Client

client = Client()
# Ask Polly to summarize failures in the last 24 hours
summary = client.analyze_traces(
    project_name="prod-fleet",
    query="Why did 5% of traces fail with tool-calling errors?"
)
print(summary.findings)
```

## Related tools / concepts
- [Promptfoo](promptfoo.md) — Open-source evaluation CLI.
- [LangChain](../ai_knowledge/langchain.md) — Primary integration framework.
- [LangGraph](../frameworks/langgraph.md) — Stateful agent orchestration.
- [DREAM](dream.md) — Agentic research evaluation metrics.
- [Benchmarking](index.md) — Overview of evaluation strategies.
- [Claude Code](../development_ops/claude-code-setup.md) — Can be traced using LangSmith.
- [OpenPipe](../infrastructure/openpipe.md) — For fine-tuning based on LangSmith traces.
- [Plandex](../development_ops/plandex.md) — Complex agent that benefits from deep tracing.
- [AgentOps](../process_understanding/agentops.md) — Specialized agent observability integration.
- [ClickHouse](../process_understanding/clickhouse.md) — Underlying OLAP engine for telemetry.

## Sources / references
- [Official Website](https://www.langchain.com/langsmith)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Polly Release Announcement](https://www.langchain.com/blog/polly-langsmith-ga)
- [LangSmith Self-Hosting Guide](https://docs.smith.langchain.com/self-hosting)
- [ClickHouse Integration for Observability](https://clickhouse.com/blog/observability-with-clickhouse)

## Contribution Metadata
- Last reviewed: 2026-07-01
- Confidence: high
