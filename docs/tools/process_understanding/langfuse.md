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

### Integration with LangChain
```python
from langfuse.callback import CallbackHandler

langfuse_handler = CallbackHandler()

# Pass the handler to your LangChain run
chain.invoke({"input": "Hello!"}, config={"callbacks": [langfuse_handler]})
```

## Related tools / concepts

- [AI Auditing Tools](ai-auditing-tools.md)
- [AgentOps](agentops.md)
- [Arize AI](arize-ai.md)
- [Braintrust](braintrust.md)
- [W&B Weave](wandb-weave.md)
- [Helicone](helicone.md)

## Sources / references
- [Langfuse Website](https://langfuse.com/)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
