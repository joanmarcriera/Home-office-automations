# Braintrust

## What it is
Braintrust is an enterprise-grade platform for evaluating, logging, and improving AI applications. It provides a specialized infrastructure for running evaluations, managing prompts, and tracking experiments in a collaborative environment.

## What problem it solves
It solves the "vibe check" problem in AI development by providing deterministic, data-driven ways to measure model performance. It enables teams to iterate on prompts and models with confidence by quantifying improvements and regressions.

## Where it fits in the stack
**Category**: Process & Understanding / Evaluation

## Typical use cases
- **Automated Evaluations**: Running test suites against new versions of prompts or models.
- **Prompt Playground**: Testing and refining prompts with real data.
- **Experiment Tracking**: Comparing results across different model configurations.
- **Production Logging**: Capturing and analyzing live application traces.

## Strengths
- **Native OpenRouter Integration**: Supports direct log ingestion for monitoring OpenRouter-based traffic.
- **Developer-Centric**: Strong focus on CLI tools and SDKs that fit into existing CI/CD workflows.
- **Enterprise Ready**: Features like RBAC and audit logs for large teams.

## Limitations
- **Cost**: Primarily a paid service for enterprise features.
- **SaaS First**: While it has SDKs, the core analysis platform is hosted.

## When to use it
- When you need a centralized system for team-wide prompt management and evaluation.
- When you need to integrate AI evaluations into your automated CI/CD pipeline.

## When not to use it
- For small, solo projects where local logging or simple scripts are sufficient.

## Getting started

Install the Braintrust SDK:

```bash
pip install braintrust
```

Initialize a simple evaluation in Python:

```python
import braintrust

# Your evaluation logic here...
```

## CLI examples

### braintrust login
Authenticates your local environment:
```bash
braintrust login
```

### braintrust push
Pushes local prompts or configs to the Braintrust platform:
```bash
braintrust push
```

### bt eval
Runs a local evaluation suite (requires the `bt` CLI):
```bash
bt eval
```

## API examples

### Python (Logging a trace)
```python
from braintrust import traced

@traced
def my_ai_function(input_text):
    # Your LLM call here
    return "AI response"

my_ai_function("Hello world")
```

## Related tools / concepts
- [LangSmith](../benchmarking/langsmith.md)
- [Promptfoo](../benchmarking/promptfoo.md)
- [Arize AI](./arize-ai.md)
- [Helicone](./helicone.md)
- [Parea](./parea.md)

## Sources / references
- [Official Website](https://www.braintrustdata.com/)
- [Braintrust Documentation](https://www.braintrustdata.com/docs)
- [OpenRouter Logging Guide](https://openrouter.ai/docs/guides/logging)

## Contribution Metadata
- Last reviewed: 2026-05-26
- Confidence: high
