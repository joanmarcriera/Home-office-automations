# LangSmith

## What it is
LangSmith is a unified platform for debugging, testing, evaluating, and monitoring LLM applications. It is part of the LangChain ecosystem but can be used with any LLM framework.

## What problem it solves
It addresses the "black box" nature of LLMs by providing full visibility into the execution traces of complex chains and agents. It also provides tools for creating evaluation datasets, running automated tests, and monitoring production performance.

## Where it fits in the stack
Benchmarking / Observability

## Typical use cases
- Debugging complex agentic workflows by inspecting intermediate steps and tool calls.
- Creating "golden" datasets for regression testing.
- Monitoring production applications for cost, latency, and quality.
- Collaborative prompt engineering and testing.
- Managing agent lifecycles via LangSmith Deployment (Fleet).
- Evaluating frontier model performance (Claude 4.8 Opus, GPT-5.5) across large-scale datasets.

## Technical Capabilities
- **Traces**: Hierarchical logs of every LLM call, tool use, and logic step.
- **Evaluators**: Automated checks (LLM-as-a-judge or heuristic) for correctness, hallucination, and safety.
- **Hub**: A version-controlled repository for prompts with native testing support.
- **Fleet**: A control plane for deploying and managing agent "fleets" directly on Kubernetes.
- **Polly**: An embedded AI assistant for natural language analysis of traces and experiments.

## Strengths
- Deep integration with LangChain and LangGraph.
- Powerful trace visualization and filtering.
- Supports manual and automated evaluation.
- Hub for sharing and versioning prompts.

## Limitations
- Proprietary SaaS (though self-hosting is available for enterprise).
- Can add latency if not configured correctly (though usually negligible).
- Learning curve for advanced evaluation features.

## When to use it
- When building complex LLM applications that require tracing for debugging.
- When transitioning from prototype to production and needing reliability metrics.
- When collaborating with a team on prompt engineering.

## When not to use it
- For very simple, single-call LLM scripts where a full observability platform is overkill.
- If strict data privacy requirements forbid sending traces to a third-party SaaS (and enterprise self-hosting is not feasible).

## Getting started

LangSmith requires an API key and a project setup in the LangSmith dashboard.

### 1. Installation
```bash
pip install -U langsmith
```

### 2. Environment Setup
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
```

## CLI examples

### 1. Authentication
```bash
langsmith login
```

### 2. List Projects
```bash
langsmith projects list
```

### 3. List Datasets
```bash
langsmith datasets list
```

## API examples

### 1. Automated Evaluation
The following Python example shows how to run an automated evaluation on a dataset using an LLM-as-a-judge.

```python
from langsmith import Client, evaluate

client = Client()

# Define the logic to be tested
def my_app(inputs):
    return "The answer is " + inputs["question"]

# Define the evaluation task
experiment_results = evaluate(
    my_app,
    data="My Golden Dataset",
    evaluators=["qa_correctness"],
    experiment_prefix="v1-baseline",
)
```

## Implementation: Polly Trace Analysis
Polly can be used via the UI (Cmd+I) or programmatically to analyze failure patterns. In the UI, you can ask:
- "Why did this trace fail to use the correct tool?"
- "Compare the cost and latency of the last 5 experiments."
- "Write a custom evaluator that checks if the output contains medical advice."

## Implementation: Fleet Agent Management
Fleet allows for no-code/low-code agent deployment. When enabled on a self-hosted instance:
1. **Define**: Create an agent in the LangSmith UI.
2. **Deploy**: Fleet handles the Kubernetes service creation and scaling via KEDA.
3. **Monitor**: Traces from the deployed fleet flow natively back into the observability dashboard.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Free tier available, paid tiers for higher volume/enterprise)
- **Self-hostable**: Yes (Enterprise only)

## Related tools / concepts
- [Promptfoo](promptfoo.md)
- [LangChain](../ai_knowledge/langchain.md)
- [LangGraph](../frameworks/langgraph.md)
- [Benchmarking](./index.md)
- [Plandex](../development_ops/plandex.md)
- [OpenPipe](../infrastructure/openpipe.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)
- [RAGFlow](../process_understanding/ragflow.md)
- [Claude Code](../development_ops/claude-code-setup.md)

## Sources / References
- [Official Website](https://www.langchain.com/langsmith)
- [Docs](https://docs.smith.langchain.com/)
- [Polly Release Announcement (2026)](https://www.langchain.com/blog/polly-langsmith-ga)
- [LangSmith Deployment Guide](https://docs.langchain.com/langsmith/deploy-self-hosted-full-platform)

## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high
