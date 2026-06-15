# Comet Opik

## What it is
Opik is an open-source platform by Comet for evaluating, testing, and monitoring LLM applications. It provides tools for tracing execution, running automated evaluations, and managing production logs.

## What problem it solves
It helps developers transition from experimentation to production-ready AI by providing the tools needed to detect errors, measure quality, and optimize cost and performance.

## Where it fits in the stack
**Category**: Process & Understanding / Observability

## Typical use cases
- **Production Monitoring**: Real-time tracking of LLM application performance.
- **Root Cause Analysis**: Drilling down into traces to understand why an agent failed.
- **Offline Evaluation**: Running quality checks on historical logs.

## Strengths
- **Open Source**: Can be self-hosted, providing full control over your data.
- **Native OpenRouter Integration**: Directly supports log ingestion from OpenRouter.
- **Comet Ecosystem**: Integrates with the broader Comet ML platform for end-to-end model management.

## Limitations
- **Newer Project**: Compared to some competitors, the ecosystem around Opik is still maturing.

## When to use it
- When you want an open-source, self-hostable alternative to LangSmith or Braintrust.
- When you are already using Comet for other machine learning tasks.

## When not to use it
- If you need a hosted, zero-setup solution and don't want to manage your own observability infrastructure (consider the hosted version of LangSmith).
- For extremely simple scripts where the overhead of adding tracing decorators doesn't provide significant value.

## Getting started

### Installation
Install the Opik library via `pip`:

```bash
pip install opik
```

### Hello-world example
Configure the Opik client and run a simple tracked function:

```bash
opik configure
```

```python
from opik import track

@track
def hello_world():
    return "Hello from Opik!"

print(hello_world())
```

## CLI examples

### opik configure
Initializes the Opik configuration and sets up your API key:
```bash
opik configure
```

### opik harbor run
Executes a benchmark using the Harbor evaluation framework with Opik tracking:
```bash
opik harbor run -d terminal-bench@head -a my_agent
```

### comet login
Authenticates with the broader Comet ML platform for production sync:
```bash
comet login
```

## API examples

### Manual Tracing
For fine-grained control, you can create spans manually without decorators.

```python
from opik import Opik

client = Opik(project_name="my-llm-project")
trace = client.trace(name="chat-completion")

span = trace.span(name="llm-call", input={"prompt": "Translate 'hello' to Spanish"})
# ... perform LLM call ...
span.update(output={"response": "hola"})
trace.update(output={"final_response": "hola"})
```

### Automated Evaluation
Run an evaluation on a dataset using LLM-as-a-judge metrics.

```python
from opik.evaluation import evaluate
from opik.evaluation.metrics import Hallucination

def my_agent(input):
    return {"output": "Agent response", "context": ["Context 1"]}

metrics = [Hallucination()]

evaluate(
    dataset_name="my-test-set",
    task=my_agent,
    metrics=metrics
)
```

## Related tools / concepts
- [Langfuse](./langfuse.md)
- [Arize AI](./arize-ai.md)
- [LangSmith](../benchmarking/langsmith.md)
- [Weights & Biases](./wandb-weave.md)
- [AgentOps](./agentops.md)
- [Helicone](helicone.md)
- [Parea](parea.md)
- [ClickHouse](clickhouse.md)

## Sources / references
- [Official Website](https://www.comet.com/site/products/opik/)
- [Opik GitHub](https://github.com/comet-ml/opik)
- [OpenRouter Logging Guide](https://openrouter.ai/docs/guides/logging)

## Contribution Metadata
- Last reviewed: 2026-05-26
- Confidence: high
