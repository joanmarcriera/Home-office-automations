# Parea

## What it is
Parea is an AI developer platform for debugging, testing, and monitoring LLM applications. It provides an integrated environment for prompt engineering, automated evaluations, and production observability.

## What problem it solves
Parea bridges the gap between prompt experimentation and production reliability. It allows developers to test prompts against datasets before deployment, monitor their performance in the wild, and quickly iterate based on production feedback.

## Where it fits in the stack
**Category**: Process & Understanding / AI Development & Observability

## Typical use cases
- **Prompt Playground**: Experimenting with different models and parameters in a visual UI.
- **Automated Regression Testing**: Running "evals" on a suite of test cases to ensure new prompts don't break existing functionality.
- **Production Tracing**: Capturing detailed execution traces of complex LLM workflows.
- **Data Collection**: Identifying "bad" responses in production to build better fine-tuning or evaluation datasets.

## Strengths
- **Unified Workflow**: Covers the entire lifecycle from prompt design to production monitoring.
- **Developer First**: Excellent SDKs and CLI tools for local development.
- **Custom Metrics**: Support for both heuristic-based (e.g., JSON validation) and LLM-based scorers.
- **Collaboration**: Tools for teams to share prompts, test results, and production traces.

## Limitations
- **Cloud Platform**: Full features require using the Parea cloud dashboard.
- **Newer Entry**: Smaller community compared to older tools like LangSmith.

## Getting started

### Installation
```bash
pip install parea-ai
```

### Basic Tracing
```python
from parea import Parea, trace

p = Parea(api_key="YOUR_API_KEY")

@trace
def my_llm_function(query: str):
    # Your LLM logic here
    return "Result"

my_llm_function("Hello Parea!")
```

## Related tools / concepts
- [Braintrust](braintrust.md)
- [LangSmith](../benchmarking/langsmith.md)
- [W&B Weave](wandb-weave.md)
- [Comet Opik](comet-opik.md)

## Sources / references
- [Parea AI Website](https://www.parea.ai/)
- [Parea Documentation](https://docs.parea.ai/)

## Contribution Metadata
- Last reviewed: 2026-05-09
- Confidence: high
