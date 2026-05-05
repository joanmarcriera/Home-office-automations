# Arize AI

## What it is
Arize AI is an AI observability and LLM evaluation platform designed to help teams monitor, troubleshoot, and improve their machine learning models and AI agents. It provides specialized tools for tracing, evaluation, and root-cause analysis of LLM applications.

## What problem it solves
It addresses the lack of visibility into complex AI systems (the "black box" problem). It helps identify performance regressions, hallucinations, and data drift in real-time, allowing for faster debugging and more reliable production deployments.

## Where it fits in the stack
**Category**: Process & Understanding / Observability

## Typical use cases
- **LLM Tracing**: Visualizing the full execution flow of agentic workflows.
- **Evaluation**: Running automated benchmarks and custom evaluations on model outputs.
- **Drift Detection**: Monitoring for changes in data distributions or model behavior over time.
- **Dataset Management**: Curating and managing datasets for fine-tuning and evaluation.

## Strengths
- **Native OpenRouter Integration**: Directly supports log ingestion from OpenRouter.
- **Phoenix (Open Source)**: Offers a local-first, open-source version (Arize Phoenix) for development and private hosting.
- **End-to-End Tracing**: Excellent visualization of complex, multi-step agent actions.

## Limitations
- **Complexity**: Can have a steep learning curve for advanced observability features.
- **Hosted Cost**: Enterprise features require a paid subscription.

## When to use it
- When moving an LLM application from prototype to production.
- When you need deep, trace-level visibility into agent decision-making.

## When not to use it
- For very simple, single-prompt applications where basic logging is sufficient.

## Getting started

Install the Arize Phoenix library for local tracing:

```bash
pip install arize-phoenix
```

Initialize local tracing in your Python code:

```python
import phoenix as px
px.launch_app()
```

## CLI examples

### px.launch_app()
Starts the local Phoenix UI:
```bash
python -c "import phoenix as px; px.launch_app()"
```

### phoenix
If installed via pip, starts the Phoenix server:
```bash
phoenix
```

### px project list
Lists all available projects (requires `@arizeai/phoenix-cli` or similar environment):
```bash
px project list
```

## API examples

### Python (Tracing with OpenInference)
Arize Phoenix uses OpenInference to automatically trace popular frameworks:

```python
from phoenix.trace.langchain import LangChainInstrumentor

# Initialize instrumentor
LangChainInstrumentor().instrument()

# Your LangChain code here...
# Traces will now be sent to your local Phoenix instance.
```

## Related tools / concepts
- [Langfuse](./langfuse.md)
- [PostHog](./posthog.md)
- [LangSmith](../benchmarking/langsmith.md)
- [Weights & Biases](./wandb-weave.md)
- [AgentOps](./agentops.md)

## Sources / references
- [Official Website](https://arize.com/)
- [Arize Phoenix GitHub](https://github.com/Arize-ai/phoenix)
- [OpenRouter Logging Guide](https://openrouter.ai/docs/guides/logging)

## Contribution Metadata
- Last reviewed: 2026-05-26
- Confidence: high
