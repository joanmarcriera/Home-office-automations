# W&B Weave

## What it is
W&B Weave is a lightweight toolkit for building and evaluating LLM applications, developed by Weights & Biases. It provides tools for tracing, versioning, and rigorous evaluation of AI workflows and agents.

## What problem it solves
It addresses the difficulty of debugging and optimizing complex, multi-step LLM chains and agents. Weave allows developers to capture every step of an AI interaction, compare model outputs side-by-side, and run automated evaluations to improve quality, cost, and latency. In July 2026, it is a primary tool for **Agent Tracing** and performance optimization for frontier models.

## Where it fits in the stack
**Category**: Process & Understanding / AI Observability & Evaluation. It acts as the "black box recorder" for agentic reasoning and tool execution.

## Typical use cases
- **Agent Tracing**: Visualizing the inner "thinking" steps and tool calls of autonomous agents like [Gemma 3](../ai_knowledge/local_llms.md), Claude 4.8, or GPT-5.5.
- **LLM Application Debugging**: Identifying where a prompt chain failed or where latency is accumulating.
- **Automated Evaluations**: Running scorers (e.g., toxicity, relevance, factual accuracy) against a dataset of model outputs.
- **Prompt Engineering**: Testing and versioning different prompt templates with visual comparisons.
- **MCP 3.0 Trace Analysis**: Auditing Model Context Protocol (MCP) tool executions and response fidelity using the MCP 3.0 Task Protocol.

## Strengths
- **Easy Integration**: Start tracing with a single line of code (`weave.init`).
- **Standardized Traces**: Organizes logs into easy-to-navigate trace trees.
- **Agnostic**: Works with any LLM, framework (LangChain, LlamaIndex), or protocol (MCP).
- **Built-in Evaluations**: Includes out-of-the-box scorers and support for custom scoring functions.
- **Human-in-the-Loop**: Supports collecting human feedback on model outputs directly in the dashboard.
- **Native Support for O4/GPT-5.5**: Optimized for the latest reasoning traces from frontier models.

## Limitations
- **Cloud Dependency**: While highly integrated, it primarily relies on the Weights & Biases cloud platform for visualization.
- **Evolving Product**: As a newer addition to the W&B ecosystem, features and APIs are rapidly evolving.

## When to use it
- When building complex LLM applications where tracing internal state and tool calls is critical.
- When you need a lightweight way to run evaluations and score model performance across datasets.
- If you are already using Weights & Biases for traditional machine learning and want a unified observability platform.
- To audit the behavior of autonomous agents in production using FastMCP 3.0.

## When not to use it
- For simple, single-prompt applications where the overhead of tracing outweighs the benefits.
- If you require a fully air-gapped or self-hosted observability solution (though W&B offers enterprise self-hosting).

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

# List runs in the current project
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
        model="gpt-5.5", # Optimized for July 2026 models
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# This call will be automatically traced in the W&B dashboard
print(call_llm("What is AI observability?"))
```

### Tracing MCP 3.0 Tool Calls
```python
@weave.op()
def execute_mcp_tool(tool_name: str, args: dict):
    # Tracing the tool execution step using MCP 3.0 Task Protocol
    print(f"Executing {tool_name} with {args}")
    # ... execution logic ...
    return "Tool output"
```

## Related tools / concepts
- [Langfuse](langfuse.md)
- [AgentOps](agentops.md)
- [Braintrust](braintrust.md)
- [Comet Opik](comet-opik.md)
- [OpenRouter](../ai_knowledge/openrouter.md) (Streams traces to Weave)
- [Arize AI](arize-ai.md)
- [Ragas](ragas.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Weights & Biases (Core)](https://wandb.ai/)
- [Claude 4.8 Opus](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)

## Sources / references
- [W&B Weave Website](https://wandb.ai/site/weave/)
- [Weave Documentation](https://weave-docs.wandb.ai/)
- [OpenRouter Weave Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/wandb-weave)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
