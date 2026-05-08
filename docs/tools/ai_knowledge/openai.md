# OpenAI

## What it is
OpenAI is a leading AI research and deployment company that provides high-performance Large Language Models (LLMs), including the GPT-5.4 and GPT-5.3 families and coding-specialized model lines.

## What problem it solves
Provides state-of-the-art reasoning, coding, and instruction-following capabilities via a reliable API, enabling complex automation and agentic workflows.

## Where it fits in the stack
**LLM / Reasoning Engine**. It serves as the "brain" that processes information, plans actions, and generates code or commands for agents to execute.

## Architecture overview
Cloud-hosted API service. Agents send prompts (context + instructions) to OpenAI's endpoints and receive structured or natural language responses.

## Typical use cases
- **Code Generation**: Used by agents like Aider or OpenHands to write and refactor code.
- **Infrastructure Planning**: Reasoning about system state and proposing shell commands.
- **Data Extraction**: Converting unstructured documents (scans, emails) into structured JSON.

## Strengths
- **State-of-the-art performance**: Strong reasoning, coding, and tool-use capabilities across the GPT-5 family.
- **Large context windows**: Support for processing large codebases or multiple documents.
- **Tool use (Function Calling)**: Robust support for structured output and calling external tools.
- **Reliability**: Highly available API with predictable latency.

## Limitations
- **Privacy**: Data is processed on OpenAI servers (though API data is generally not used for training by default on enterprise/tier accounts).
- **Cost**: Can become expensive with high-volume agentic loops.
- **Dependency**: Requires active internet connection and relies on a third-party provider.

## When to use it
- When maximum reasoning power is required for complex tasks.
- For production-grade automations where reliability is paramount.
- When needing to process very large contexts that local models can't handle yet.

## Effort-level routing

### GPT-5.4 `low`
- Use for: straightforward serious work where you still want GPT-5.4 quality
- Default? No
- Comment: good first pass when latency and cost matter

### GPT-5.4 `medium`
- Use for: the default OpenAI lane for planning, debugging, analysis, and non-trivial implementation help.
- Default? Yes
- Comment: best general OpenAI default. Includes the "Thinking" system for improved reasoning.

### GPT-5.4 `high`
- Use for: hard reasoning, difficult debugging, deeper architecture analysis
- Default? No
- Comment: use when `medium` is not holding up

### GPT-5.4 `xhigh`
- Use for: explicit last-step escalation on very hard or very important reasoning tasks
- Default? No
- Comment: avoid using this as background default because it adds cost and latency quickly

### GPT-5.3 Instant
- Use for: faster, smoother everyday conversations.
- Default? No
- Comment: optimized for lower latency and more natural interaction.

### GPT-5.3 Codex
- Use for: code-specialized generation and editing.
- Default? Only for code-centric lanes
- Comment: use this when the task is mostly code, not broad general reasoning. Includes updated security research preview.

See the central routing guide: [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## When not to use it
- For processing highly sensitive/private data that must remain on-premises.
- When working offline or in air-gapped environments.
- For high-frequency, simple tasks where a cheaper or local model would suffice.

## Getting started

### CLI Example
The `openai` CLI tool allows for quick testing of models and endpoints.

```bash
# Install the CLI
pip install openai

# Export your API key
export OPENAI_API_KEY='your-api-key-here'

# List available models
openai models list

# Run a simple completion
openai chat completions create -m gpt-5.4-medium --message user "Hello, how can I automate my home office?"
```

### Python API Example (Structured Outputs)
Using Pydantic with the OpenAI SDK ensures that the model returns data in a strictly validated schema.

```python
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class HomeTask(BaseModel):
    task_name: str
    priority: int
    estimated_minutes: int

class TaskPlan(BaseModel):
    tasks: list[HomeTask]
    reasoning: str

completion = client.beta.chat.completions.parse(
    model="gpt-5.4-medium",
    messages=[
        {"role": "system", "content": "You are a home office manager."},
        {"role": "user", "content": "I need to clean my desk, water the plants, and reply to 5 emails."}
    ],
    response_format=TaskPlan,
)

plan = completion.choices[0].message.parsed
print(f"Reasoning: {plan.reasoning}")
for task in plan.tasks:
    print(f"- {task.task_name} (Priority: {task.priority})")
```

## Security considerations
- **API Key Management**: Never hardcode keys; use environment variables or secret managers.
- **Data Privacy**: Review OpenAI's data usage policy; ensure sensitive PII is redacted if necessary.
- **Prompt Injection**: Be aware that models can be manipulated via input; implement output validation.

## Related tools / concepts
- [Promptfoo](../benchmarking/index.md) (Acquisition announced 2026-03-11)
- [Anthropic](../providers/anthropic.md)
- [Mistral AI](../providers/mistral.md)
- [OpenRouter](openrouter.md)
- [Aider](../development_ops/aider.md)
- [OpenHands](../development_ops/openhands.md)
- [SSH Execution Patterns](../../architecture/ssh_execution_patterns.md)
- [OpenAI Codex](../development_ops/codex.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)
- [Answer Synthesis Schema](../../reference-implementations/data-copilot/answer-synthesis-schema.md)
- [SQL Validation Playbook](../../playbooks/data-copilot-sql-validation.md)
- [Pydantic AI Framework](../frameworks/pydantic-ai.md)
- [Ollama](../../services/ollama.md)
- [LangChain](../frameworks/langchain.md)

## Sources / References

- [Introducing GPT-5.4](https://openai.com/index/introducing-gpt-5-4)
- [GPT-5.3 Instant](https://openai.com/index/gpt-5-3-instant)
- [GPT-5.3 Instant System Card](https://openai.com/index/gpt-5-3-instant-system-card)
- [Instruction Hierarchy Challenge](https://openai.com/index/instruction-hierarchy-challenge)
- [Improving instruction hierarchy in frontier LLMs](https://openai.com/index/instruction-hierarchy-challenge)
- [OpenAI to acquire Promptfoo](https://openai.com/index/openai-to-acquire-promptfoo)
- [Codex Security Research Preview](https://openai.com/index/codex-security-now-in-research-preview)

## Contribution Metadata

- Last reviewed: 2026-05-08
- Confidence: high
