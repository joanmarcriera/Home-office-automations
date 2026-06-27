# Anthropic Claude

## What it is
Anthropic is an AI safety and research company that produces the Claude family of LLMs. As of June 2026, it is a proprietary service offering high-performance models known for strong reasoning, coding excellence, and safety. Pricing is usage-based with a free testing tier available via the Anthropic Console.

## What problem it solves
It offers a high-performance alternative to OpenAI with a focus on "Constitutional AI" (safety) and exceptional performance in coding, long-form document analysis, and complex reasoning tasks. It provides a reliable engine for autonomous agents via native [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) support.

## Where it fits in the stack
**LLM / Reasoning Engine / Provider**. It serves as the primary intelligence layer for coding agents and complex document synthesis workflows.

## Typical use cases
- **Pair Programming**: Claude 3.5 Sonnet and 4.8 Opus are the preferred models for tools like [Aider](../development_ops/aider.md).
- **Complex Analysis**: Summarizing long technical documentation or legal files using the 200k+ token context window.
- **Strict Adherence**: Workflows requiring high precision in following complex formatting or reasoning rules.
- **Autonomous Engineering**: Leveraging MCP 3.0 to enable Claude to interact with local and remote tools.
- **Computer Use**: Utilizing Claude 4.8 Opus for direct interaction with operating systems and browsers.

### Model routing (June 2026)
| Model | Primary Use Case | Default? |
| :--- | :--- | :--- |
| **Haiku** | Fast classification, extraction, rewriting, and cheap high-volume tasks | No |
| **Sonnet** | Default coding, planning, and most daily serious work | Yes |
| **Opus 4.7** | Complex software engineering and high-resolution vision tasks | No |
| **Opus 4.8** | Premium escalation for hard synthesis and autonomous browser-agent tasks | No |
| **Mythos** | Frontier-scale simulations and high-reliability software factory architectures | No |

## Strengths
- **Coding Excellence**: Widely regarded as one of the strongest daily-driver models for software engineering.
- **Safety Focus**: Built with Constitutional AI principles for better alignment and reduced harmful outputs.
- **Large Context**: Ability to handle up to 2.5M tokens in [Plandex](../development_ops/plandex.md) integrations.
- **Low Hallucination**: Exhibits high factual accuracy and honesty in complex reasoning.
- **Native MCP Support**: Seamless integration with the Model Context Protocol (MCP 3.0) for extensible tool use.

## Limitations
- **Cloud Dependency**: Requires external API access; no official local/offline version.
- **Rate Limits**: Usage tiers can be restrictive for new accounts.
- **Cost**: High-end models like Opus 4.8 are significantly more expensive than smaller models.

## When to use it
- For software development tasks where Sonnet/Opus is the right default.
- When safety and alignment are critical priorities for your application.
- For analyzing very long documents or entire codebases in a single context.
- When you want a multi-tier routing strategy using the [Model Routing Guide](../../knowledge_base/model_routing_guide.md).

## When not to use it
- When a local/offline solution is required for privacy or cost (consider [Llama 4 Maverick](../ai_knowledge/local_llms.md)).
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

### Basic Message Creation (Python)
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-4-8-opus-20260528",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain the advantages of MCP 3.0."}
    ]
)
print(message.content)
```

### Streaming Responses
```python
with client.messages.stream(
    model="claude-3-5-sonnet-latest",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a 500-word essay on AI safety."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
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

## Sources / References
- [Official Anthropic Website](https://www.anthropic.com/)
- [Anthropic News and Release Logs](https://www.anthropic.com/news)
- [Anthropic Developer Documentation](https://docs.anthropic.com/)
- [Claude 4.8 Opus Announcement](https://www.anthropic.com/news/claude-opus-4-8)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
