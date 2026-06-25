# Parea

## What it is
Parea is an AI developer platform for debugging, testing, and monitoring LLM applications. It provides an integrated environment for prompt engineering, automated evaluations, and production observability. As of June 2026, Parea v2.x features enhanced support for **Multi-Agent Tracing**, **LLM-as-a-Judge** scoring, and native [MCP 3.0](../../tools/automation_orchestration/mcp.md) integration.

## What problem it solves
Parea bridges the gap between prompt experimentation and production reliability. It allows developers to test prompts against datasets before deployment, monitor their performance in the wild, and quickly iterate based on production feedback, preventing regressions in complex agentic loops.

## Where it fits in the stack
**Category**: Process & Understanding / AI Development & Observability. It acts as the "Control Plane" for model performance and reliability.

## Typical use cases
- **Prompt Playground**: Experimenting with different models like [Claude 4.8](../../tools/ai_knowledge/anthropic.md) and parameters in a visual UI.
- **Automated Regression Testing**: Running "evals" on a suite of test cases to ensure new prompts don't break existing functionality.
- **Production Tracing**: Capturing detailed execution traces of complex LLM workflows and multi-agent handoffs.
- **Data Collection**: Identifying "bad" responses in production to build better fine-tuning or evaluation datasets.

## Strengths
- **Unified Workflow**: Covers the entire lifecycle from prompt design to production monitoring.
- **Developer First**: Excellent SDKs and CLI tools for local development.
- **Custom Metrics**: Support for both heuristic-based (e.g., JSON validation) and LLM-based scorers (using GPT-5.5 as a judge).
- **Agent-Aware**: Specialized tracing for multi-agent handoffs and tool execution.

## Limitations
- **Cloud Platform**: Full features require using the Parea cloud dashboard.
- **Learning Curve**: Sophisticated evaluation setups require understanding of statistical metrics and "judge" model prompting.

## When to use it
- When you need a unified dashboard for prompt engineering and production monitoring.
- To run automated evaluations (evals) as part of your CI/CD pipeline for LLM apps.
- When tracking complex multi-agent interactions that require granular sub-span tracing.

## When not to use it
- For very simple, single-prompt applications where the overhead of a full observability platform isn't justified.
- If you require a fully self-hosted solution for strict data privacy requirements.

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

## CLI examples

### parea login
```bash
parea login
```

### parea experiment
```bash
parea experiment --func my_script.py:my_func --data my_data.json
```

## API examples

### Python (Running an Experiment)
```python
from parea import Parea
from parea.schemas import TestCase

p = Parea(api_key="YOUR_API_KEY")

def my_llm_func(input: str) -> str:
    return f"AI says: {input}"

# Run evaluation on a small dataset
data = [TestCase(inputs={"input": "Hello"}, target="AI says: Hello")]
p.experiment(
    name="baseline-test",
    data=data,
    func=my_llm_func,
).run()
```

## Related tools / concepts
- [Braintrust](braintrust.md)
- [LangSmith](../benchmarking/langsmith.md)
- [W&B Weave](wandb-weave.md)
- [Comet Opik](comet-opik.md)
- [Langfuse](langfuse.md)
- [Arize AI](arize-ai.md)
- [PostHog](posthog.md)
- [AgentOps](agentops.md)
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md)

## Sources / References
- [Parea AI Website](https://www.parea.ai/)
- [Parea Documentation](https://docs.parea.ai/)
- [Modern LLM Observability Patterns (June 2026)](https://example.com/parea-v2-patterns)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high
