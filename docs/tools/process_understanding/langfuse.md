# Langfuse

## What it is
An open-source LLM engineering platform for tracing, observability, metrics, and evaluation.

## What problem it solves
It allows developers to debug complex LLM interactions, track costs, monitor latency, and run evaluations (scores) on agent outputs.

## Where it fits in the stack
**Category**: Process & Understanding / Observability

## Key Features
- **Tracing**: Visualizes the nested calls in an agentic loop, including tool calls, LLM latency, and token usage.
- **Evaluation**: Automates model-based grading of responses using LLM-as-a-judge or manual scoring.
- **Prompt Management**: Version-controlled prompt management that allows decoupling prompts from application code.
- **OpenRouter Integration**: Native support for receiving logs from OpenRouter without additional instrumentation.

## Getting started

### Installation
```bash
pip install langfuse
```

### Basic Integration (OpenAI)
Langfuse provides a wrapper for the OpenAI SDK that automatically captures traces.

```python
from langfuse.openai import openai

# Standard OpenAI call, now automatically traced
response = openai.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "How does Langfuse help with AI observability?"}],
  name="obs-test-run" # Optional: name the trace
)

print(response.choices[0].message.content)
```

## CLI examples

### langfuse api traces list
Lists recent traces from your project:
```bash
langfuse api traces list --limit 10
```

### langfuse api prompts get
Retrieves a specific prompt version from the Langfuse prompt management system:
```bash
langfuse api prompts get --name "my-prompt-name"
```

### langfuse integration claudecode enable
Enables tracing for Claude Code sessions:
```bash
langfuse integration claudecode enable
```

## API examples

### Python (LangChain Integration)
```python
from langfuse.callback import CallbackHandler

langfuse_handler = CallbackHandler()

# Pass the handler to your LangChain run
chain.invoke({"input": "Hello!"}, config={"callbacks": [langfuse_handler]})
```

### Python (Scoring a trace)
```python
from langfuse import Langfuse

langfuse = Langfuse()

# Send a score for an existing trace
langfuse.score(
    trace_id="existing-trace-id",
    name="user-feedback",
    value=1,
    comment="Very helpful response"
)
```

## Related tools / concepts
- [AgentOps](agentops.md)
- [Arize AI](arize-ai.md)
- [Braintrust](braintrust.md)
- [Helicone](helicone.md)
- [Parea](parea.md)
- [W&B Weave](wandb-weave.md)

## Sources / references
- [Langfuse Website](https://langfuse.com/)
- [Langfuse CLI Documentation](https://langfuse.com/docs/api-and-data-platform/features/cli)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
