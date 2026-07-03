# Claude

## What it is
Claude is a family of foundational large language models developed by Anthropic. As of July 2026, the flagship model is **Claude 4.8 Opus** (`claude-4-8-opus-20260528`), designed to be helpful, honest, and harmless. It is the industry standard for high-fidelity reasoning and safe agentic behavior, utilizing "Constitutional AI" to align model outputs with human values. With the release of **Gemma 3** in July 2026, Claude 4.8 remains the preferred choice for complex, multi-step enterprise reasoning.

## What problem it solves
Claude provides state-of-the-art conversational and reasoning capabilities that address the need for precision, safety, and long-context handling in AI applications. It excels at complex tasks such as autonomous coding, multi-step logical analysis, and synthesizing information from massive datasets (with a context window of 1M+ tokens as of mid-2026).

## Where it fits in the stack
**AI Model and Reasoning Engine**. It sits at the top of the AI stack as the primary intelligence layer, often orchestrated via the **Model Context Protocol (MCP) 3.0** to interact with local files, databases, and third-party APIs using the standardized **Task Protocol**.

## Typical use cases
- **Autonomous Software Engineering**: Using Claude Code to refactor entire repositories or debug complex systems.
- **Enterprise Knowledge Synthesis**: Analyzing thousands of pages of documentation or legal filings in a single pass.
- **Agentic Orchestration**: Serving as the "brain" for multi-agent systems built with LangGraph or CrewAI.
- **Model Routing**: Dynamically switching between Haiku (latency), Sonnet (balanced), and Opus (reasoning) tiers based on task complexity.

## Strengths
- **Superior Reasoning**: Claude 4.8 Opus consistently outperforms competitors in logic puzzles and coding benchmarks.
- **High-Fidelity Safety**: Constitutional AI minimizes harmful outputs without sacrificing utility.
- **Context Window**: 1M+ token capacity allows for processing entire codebases or library collections.
- **Native MCP 3.0 Support**: Seamless integration with the Model Context Protocol ecosystem and Task Protocol.

## Limitations
- **Closed Source**: The model weights and training methodologies are proprietary (unlike [Gemma 3](local_llms.md)).
- **Strict Rate Limits**: High-demand reasoning models (Opus) often have restrictive tiers on the free API.
- **Computational Cost**: Opus models are more expensive per token compared to Haiku or GPT-4o-mini.

## When to use it
- When you require the highest possible accuracy for complex coding or logical reasoning tasks.
- When working with very large documents that exceed the context limits of other models.
- When building production-grade agents that require strict adherence to safety and tool-calling protocols.

## When not to use it
- For simple, low-stakes tasks where a cheaper model like Claude 3.5 Haiku or GPT-4o-mini is sufficient.
- If you require a fully local, offline model for air-gapped environments (use [vLLM](../infrastructure/vllm.md) or [Gemma 3](local_llms.md)).
- When you need a model with no safety filters or "uncensored" responses.

## Getting started

### Claude.ai
The web interface at [claude.ai](https://claude.ai/) is the most accessible way to interact with the models, featuring "Artifacts" for real-time code and UI previews.

### Anthropic API
1.  Sign up at the [Anthropic Console](https://console.anthropic.com/).
2.  Generate an API key and add billing credits.
3.  Install the SDK: `pip install anthropic`.

### Hello World (Python)
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Licensing
Claude is a proprietary model. Usage is billed per 1M tokens or via monthly subscriptions (Pro/Team) for the web interface.

## CLI examples

### Claude Code CLI
Anthropic's official terminal-based agent for coding:

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Authenticate and initialize
claude auth login
claude init

# Ask a coding question or request a change
claude "Refactor the authentication middleware to use JWT"
```

### Unofficial CLI (anthropic-cli)
```bash
# Prompt Claude from the terminal
anthropic "Explain the difference between PagedAttention and FlashAttention"
```

## API examples

### Batch Message Processing
```python
import anthropic

client = anthropic.Anthropic()

# Example of using the Message Batches API for high-volume processing
# (Availability and syntax as of July 2026)
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "request-1",
            "params": {
                "model": "claude-3-5-sonnet-20240620",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": "Task 1"}]
            }
        }
    ]
)
print(f"Batch created: {batch.id}")
```

### Tool Use (MCP 3.0)
```python
# Conceptual example of tool definition with MCP 3.0 Task Protocol
tools = [{
    "name": "get_weather",
    "description": "Get current weather in a location",
    "input_schema": {
        "type": "object",
        "properties": {"location": {"type": "string"}},
        "required": ["location"]
    }
}]

# Claude handles the decision to call the tool natively via Task Protocol
```

## Related tools / concepts
- [GPT-5.5](chatgpt.md) — The leading reasoning competitor from OpenAI.
- [Gemma 3](local_llms.md) — Google's state-of-the-art open model released July 2026.
- [Everything Claude Code](everything-claude-code.md) — Comprehensive guide to the Claude Code ecosystem.
- [Claude How-To](claude-howto.md) — Practical implementation patterns and recipes.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for tool integration.
- [Anthropic](../providers/anthropic.md) — Provider overview.
- [Claude Code](../development_ops/claude-code.md) — Terminal-based agent details.
- [Claude Context Mode](../development_ops/claude-context-mode.md) — Managing large context windows.

## Sources / references
- [Official Website](https://claude.ai/)
- [Anthropic Console](https://console.anthropic.com/)
- [Claude API Documentation](https://docs.anthropic.com/claude/docs)
- [Anthropic Blog](https://www.anthropic.com/news)

## Contribution Metadata
- Last reviewed: 2026-07-02
- Confidence: high
