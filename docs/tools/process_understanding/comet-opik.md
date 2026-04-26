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

## Getting started

Install the Opik library:

```bash
pip install opik
```

Configure the Opik client:

```bash
opik configure
```

## CLI examples

### opik configure
Sets up your API key and project settings:
```bash
opik configure
```

## API examples

### Python (Tracing a function)
```python
from opik import track

@track
def call_llm(prompt):
    # Your LLM call here
    return "Response"

call_llm("Analyze this code")
```

## Related tools / concepts
- [Langfuse](./langfuse.md)
- [Arize AI](./arize-ai.md)
- [LangSmith](../benchmarking/langsmith.md)

## Sources / references
- [Official Website](https://www.comet.com/site/products/opik/)
- [Opik GitHub](https://github.com/comet-ml/opik)
- [OpenRouter Logging Guide](https://openrouter.ai/docs/guides/logging)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
