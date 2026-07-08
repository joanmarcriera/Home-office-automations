# W&B Weave

## What it is
W&B Weave is a lightweight toolkit for building and evaluating LLM applications, developed by Weights & Biases. As of July 2026, it serves as a core observability layer for the **MCP 3.0 Task Protocol**, providing tools for tracing, versioning, and rigorous evaluation of autonomous AI workflows and agents.

## What problem it solves
It addresses the difficulty of debugging and optimizing complex, multi-step LLM chains and agents. Weave allows developers to capture every step of an AI interaction, compare model outputs side-by-side, and run automated evaluations. In July 2026, it is specifically optimized for **Gemma 3** reasoning traces and high-concurrency tool execution via **FastMCP 3.0**.

## Where it fits in the stack
**Category**: Process & Understanding / AI Observability & Evaluation. It acts as the "black box recorder" for agentic reasoning and tool execution, sitting between the Inference Plane and the Execution Plane.

## Typical use cases
- **Agent Tracing**: Visualizing the inner "thinking" steps and tool calls of autonomous agents like [Gemma 3](../ai_knowledge/local_llms.md) or GPT-5.5.
- **MCP Task Auditing**: Tracking the lifecycle of tasks executed via the [MCP 3.0 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md).
- **Automated Evaluations**: Running scorers (e.g., toxicity, relevance, factual accuracy) against a dataset of model outputs in a CI/CD pipeline.
- **Prompt Engineering**: Testing and versioning different prompt templates with visual comparisons and A/B testing.
- **Latency Analysis**: Identifying bottlenecks in [FastMCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) tool discovery and execution.

## Strengths
- **Easy Integration**: Start tracing with a single line of code (`weave.init`).
- **Standardized Traces**: Organizes logs into easy-to-navigate trace trees, fully compatible with [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md).
- **High Performance**: Optimized for [FastMCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) for ultra-low latency trace collection.
- **Built-in Evaluations**: Includes out-of-the-box scorers and support for custom scoring functions using LLM-as-a-judge.
- **Native Support for Gemma 3**: Specifically tuned to handle the multi-stage reasoning traces of the latest open models.

## Limitations
- **Cloud Dependency**: While highly integrated, it primarily relies on the Weights & Biases cloud platform for advanced visualization and collaboration.
- **Evolving Protocol Support**: As MCP 3.0 is a recent standard, some edge-case tool definitions may require custom instrumentation.

## When to use it
- When building complex LLM applications where tracing internal state and tool calls is critical for debugging.
- When you need a lightweight way to run evaluations and score model performance across datasets.
- If you are already using Weights & Biases for traditional machine learning and want a unified observability platform.
- To audit the behavior of autonomous agents using the [MCP 3.0 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md).

## When not to use it
- For simple, single-prompt applications where the overhead of tracing outweighs the benefits.
- If you require a fully air-gapped or self-hosted observability solution (though W&B offers enterprise self-hosting for large-scale deployments).

## Getting started

### Installation
```bash
pip install weave wandb
```

## CLI examples
```bash
# Login to Weights & Biases
wandb login

# Initialize a new W&B project (Weave uses W&B projects for storage)
wandb init --project my-weave-app

# List runs in the current project to verify connectivity
wandb runs
```

## API examples

### Basic Tracing with Decorators
```python
import weave
import openai

# Initialize Weave with a project name
weave.init("my-llm-app")

@weave.op()
def call_llm(prompt: str):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.5", # Optimized for 2026 models
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# This call will be automatically traced in the W&B dashboard
print(call_llm("What is AI observability?"))
```

### Tracing MCP 3.0 Task Execution
```python
@weave.op()
def execute_mcp_task(task_id: str, tools: list):
    # Tracing the task execution step in the MCP 3.0 lifecycle
    print(f"Executing task {task_id} with tools {tools}")
    # ... execution logic ...
    return "Task completed"
```

## Related tools / concepts
- [Langfuse](langfuse.md) — Alternative open-source observability.
- [AgentOps](agentops.md) — Specialized tracing for multi-agent frameworks.
- [Braintrust](braintrust.md) — High-performance evaluation and proxy.
- [Comet Opik](comet-opik.md) — LLM evaluation and observability.
- [OpenRouter](../ai_knowledge/openrouter.md) — Streams traces directly to Weave.
- [Arize AI](arize-ai.md) — Enterprise-grade ML observability.
- [Ragas](ragas.md) — Framework for RAG evaluation.
- [Gemma 3](../ai_knowledge/local_llms.md) — Target model for reasoning traces.
- [MCP 3.0](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Core integration protocol.

## Sources / references
- [W&B Weave Website](https://wandb.ai/site/weave/)
- [Weave Documentation](https://weave-docs.wandb.ai/)
- [OpenRouter Weave Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/wandb-weave)
- [MCP 3.0 Specification](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2026-07-08
- Confidence: high
