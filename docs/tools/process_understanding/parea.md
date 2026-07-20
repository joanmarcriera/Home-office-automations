# Parea

## What it is
Parea is an AI developer platform for debugging, testing, and monitoring LLM applications. It provides an integrated environment for prompt engineering, automated evaluations, and production observability. As of June 2026, Parea v2.x features enhanced support for **Multi-Agent Tracing**, **LLM-as-a-Judge** scoring, and native [MCP 3.0](../../tools/automation_orchestration/mcp.md) integration.

## What problem it solves
Parea bridges the gap between prompt experimentation and production reliability. It allows developers to test prompts against datasets before deployment, monitor their performance in the wild, and quickly iterate based on production feedback, preventing regressions in complex agentic loops.

## Where it fits in the stack
**Category**: Process & Understanding / AI Development & Observability. It acts as the "Control Plane" for model performance and reliability.

## Typical use cases
- **Prompt Playground**: Experimenting with different models like [Claude 4.8](../providers/anthropic.md) and parameters in a visual UI.
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
Install the official Parea SDK via `pip` (Python) or `@parea-ai/sdk` (Node.js):

```bash
# Install Python SDK
pip install parea-ai

# Or install Node.js SDK
npm install @parea-ai/sdk
```

### Authentication Setup
Get your API key from the Parea dashboard and export it to your environment:

```bash
export PAREA_API_KEY="your_api_key_here"
```

### Hello World Example
Initialize Parea and wrap your LLM function with the `@trace` decorator to automatically log execution data, token consumption, and latency:

```python
from parea import Parea, trace

# Initialize the Parea SDK (reads PAREA_API_KEY from environment)
p = Parea()

@trace
def my_llm_function(user_query: str) -> str:
    # Your LLM call or business logic here
    response_text = f"Processed query: {user_query}"
    return response_text

# Run the function; trace is automatically dispatched to the dashboard
print(my_llm_function("Hello Parea!"))
```

## CLI examples
The `parea` command-line utility provides commands to manage local authentication, run batch evaluations, and fetch deployed prompts:

```bash
# 1. Authenticate your local shell environment with Parea Cloud
parea login

# 2. Run a local evaluation experiment on your functions against a dataset file
parea experiment --func my_script.py:my_func --data ./test_dataset.json

# 3. List or inspect locally deployed prompt assets in your active project
parea deploy list
```

## API examples
Deploy, run, and score automated evaluations (experiments) programmatically using the Parea client.

### Programmatic Experiment with Heuristic Evaluators
Define a target function, prepare a list of test cases, and execute a local evaluation pipeline with automated metric scoring:

```python
from parea import Parea
from parea.schemas import TestCase
from parea.evals.general import levenshtein

p = Parea()

def my_llm_runner(inputs: dict) -> str:
    # Simulated LLM response
    return f"AI Answer: {inputs['query']}"

# Prepare test data with target outputs
test_cases = [
    TestCase(
        inputs={"query": "Draft a welcome message"},
        target="AI Answer: Draft a welcome message"
    )
]

# Configure and run the experiment using the Levenshtein distance metric
experiment_result = p.experiment(
    name="welcome-prompt-test",
    data=test_cases,
    func=my_llm_runner,
).run()

print(f"Experiment completed. Metrics: {experiment_result}")
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
- [Modern LLM Observability Patterns](https://docs.parea.ai/welcome/what_is_parea_ai)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
