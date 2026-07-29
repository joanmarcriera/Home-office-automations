# Anthropic Claude

## What it is
Anthropic is an AI safety and research company that produces the Claude family of LLMs. As of late October / November 2026, it is a proprietary service offering high-performance models known for strong reasoning, coding excellence, and safety. Pricing is usage-based with a free testing tier available via the Anthropic Console.

## What problem it solves
It offers a high-performance alternative to OpenAI with a focus on "Constitutional AI" (safety) and exceptional performance in coding, long-form document analysis, and complex reasoning tasks. It provides a reliable engine for autonomous agents via native [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) support.

## Where it fits in the stack
**LLM / Reasoning Engine / Provider**. It serves as the primary intelligence layer for coding agents and complex document synthesis workflows.

## Typical use cases
- **Pair Programming**: Claude 5.1 Sonnet and 5.1 Opus are the preferred models for tools like [Aider](../development_ops/aider.md).
- **Complex Analysis**: Summarizing long technical documentation or legal files using the 200k+ token context window.
- **Strict Adherence**: Workflows requiring high precision in following complex formatting or reasoning rules.
- **Autonomous Engineering**: Leveraging MCP 3.1 to enable Claude to interact with local and remote tools dynamically.
- **Computer Use**: Utilizing Claude 5.1 Opus for direct interaction with operating systems and browsers.

### Model routing (November 2026)
| Model | Primary Use Case | Default? |
| :--- | :--- | :--- |
| **Claude 5.1 Haiku** | Fast classification, low-latency extraction, and high-volume routing tasks | No |
| **Claude 5.1 Sonnet** | Default model for coding, complex planning, multi-agent coordination, and daily work | Yes |
| **Claude 5.1 Opus** | SOTA software engineering, high-fidelity vision reasoning, and advanced mathematical research | No |
| **Claude 5.1 Mythos** | Large-scale multi-modal simulation and hyper-reliable software factory orchestrators | No |

## Strengths
- **Coding Excellence**: Widely regarded as the strongest daily-driver model family for software engineering.
- **Safety Focus**: Built with Constitutional AI principles for better alignment and reduced harmful outputs.
- **Large Context**: Ability to handle up to 2.5M tokens in [Plandex](../development_ops/plandex.md) integrations.
- **Low Hallucination**: Exhibits high factual accuracy and honesty in complex reasoning.
- **Native MCP Support**: Seamless integration with the Model Context Protocol (MCP 3.1) for extensible tool use.

## Limitations
- **Cloud Dependency**: Requires external API access; no official local/offline version.
- **Rate Limits**: Usage tiers can be restrictive for new accounts.
- **Cost**: High-end models like Opus 5.1 are significantly more expensive than smaller models.

## When to use it
- For software development tasks where Sonnet/Opus is the right default.
- When safety and alignment are critical priorities for your application.
- For analyzing very long documents or entire codebases in a single context.
- When you want a multi-tier routing strategy using the [Model Routing Guide](../../knowledge_base/model_routing_guide.md).

## When not to use it
- When a local/offline solution is required for privacy or cost (consider [Llama 4](../ai_knowledge/local_llms.md)).
- If you need native DALL-E 3 style image generation in the same API call.

## Getting started

### Installation
Install the official Python SDK:
```bash
pip install anthropic
```

### Initial Configuration
Set your API key as an environment variable:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## CLI examples

### Using Claude Code
Claude plugins and CLI tools often interact directly with the API:
```bash
claude "Analyze the current directory and suggest refactorings"
```

### Listing Models via SDK
While not a direct CLI, simple scripts can be used to check availability:
```python
import anthropic
print(anthropic.Anthropic().models.list())
```

## API examples

### 1. Basic Message Creation (Python)
Standard API integration using type annotations and secure clients:

```python
import anthropic

client: anthropic.Anthropic = anthropic.Anthropic()

message: anthropic.types.Message = client.messages.create(
    model="claude-5-1-sonnet-20261022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain the advantages of MCP 3.1."}
    ]
)
print(message.content[0].text)
```

### 2. Streaming Responses
Real-time response streaming for conversational interfaces:

```python
from anthropic import Anthropic

client: Anthropic = Anthropic()

with client.messages.stream(
    model="claude-5-1-sonnet-20261022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a 500-word essay on AI safety."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### 3. Structured Output Validation with Pydantic v2
Parse and validate model-generated structured task execution plans using modern Pydantic v2 schemas:

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, TypeAdapter

class AgenticAction(BaseModel):
    tool_name: str = Field(..., description="The name of the tool to invoke.")
    arguments: dict = Field(..., description="The arguments to pass to the tool.")
    thought_trace: Optional[str] = Field(None, description="The internal reasoning trace of the model.")

class AgentExecutionPlan(BaseModel):
    steps: List[AgenticAction] = Field(..., description="Decomposed list of sequential actions to execute.")
    overall_goal: str = Field(..., description="The main objective of this task execution plan.")

# Example showing how to parse a structured JSON response from Claude 5.1
raw_response: str = """{
  "overall_goal": "Validate local kubernetes deployment of K3s",
  "steps": [
    {
      "tool_name": "execute_bash",
      "arguments": {"command": "kubectl get nodes -o json"},
      "thought_trace": "Retrieve the node status to ensure the cluster is up and ready."
    }
  ]
}"""

# Use Pydantic v2 TypeAdapter for validation
adapter: TypeAdapter[AgentExecutionPlan] = TypeAdapter(AgentExecutionPlan)
plan: AgentExecutionPlan = adapter.validate_json(raw_response)

print(f"Goal: {plan.overall_goal}")
for step in plan.steps:
    print(f"  Step -> Tool: {step.tool_name}, Args: {step.arguments}")
```

## Related tools / concepts
- [OpenAI](../ai_knowledge/openai.md) — Primary competitor for frontier models.
- [OpenRouter](../ai_knowledge/openrouter.md) — Unified API access to Claude and others.
- [Aider](../development_ops/aider.md) — Popular CLI tool optimized for Claude.
- [MCP](../automation_orchestration/mcp.md) — Standard for extending Claude's capabilities.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's agentic coding CLI.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — Strategy for model selection.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Patterns for autonomous execution.
- [Plandex](../development_ops/plandex.md) — Complex engineering tool supporting large context Claude models.
- [Zed](../development_ops/zed.md) — Editor with native Claude integration.

## Sources / references
- [Official Anthropic Website](https://www.anthropic.com/)
- [Anthropic News and Release Logs](https://www.anthropic.com/news)
- [Anthropic Developer Documentation](https://docs.anthropic.com/)
- [Claude 5.1 Announcement and SOTA Benchmarks](https://www.anthropic.com/news/claude-5-1-opus)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
