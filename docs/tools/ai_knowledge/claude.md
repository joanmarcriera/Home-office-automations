# Claude

## What it is
Claude is a family of foundational large language models developed by Anthropic. As of July 2026, the flagship model is **Claude 4.8 Opus** (`claude-4-8-opus-20260528`), designed to be helpful, honest, and harmless. It is widely regarded as the industry standard for high-fidelity reasoning and safe agentic behavior, utilizing "Constitutional AI" to align model outputs with human values. In July 2026, Claude 4.8 remains the top-tier benchmark for the **MCP 3.0 Task Protocol**, providing superior reliability for automated execution compared to mid-weight models like Gemma 3.

## What problem it solves
Claude provides state-of-the-art conversational and reasoning capabilities that address the need for precision, safety, and long-context handling in AI applications. It excels at complex tasks such as autonomous coding, multi-step logical analysis, and synthesizing information from massive datasets (with a context window of 500k+ tokens as of mid-2026).

## Where it fits in the stack
AI Model and Reasoning Engine. It sits at the top of the AI stack as the primary intelligence layer, often orchestrated via the **Model Context Protocol (MCP 3.0)** to interact with local files, databases, and third-party APIs using standardized task execution patterns.

## Typical use cases
- **Autonomous Software Engineering**: Using Claude Code to refactor entire repositories or debug complex systems.
- **Enterprise Knowledge Synthesis**: Analyzing thousands of pages of documentation or legal filings in a single pass.
- **Agentic Orchestration**: Serving as the "brain" for multi-agent systems built with LangGraph or CrewAI, leveraging the **MCP 3.0 Task Protocol**.
- **Model Routing**: Dynamically switching between Haiku (latency), Sonnet (balanced), and Opus (reasoning) tiers based on task complexity.

## Strengths
- **Superior Reasoning**: Claude 4.8 Opus consistently outperforms competitors like Gemma 3 in complex logic puzzles and architectural coding benchmarks.
- **High-Fidelity Safety**: Constitutional AI minimizes harmful outputs without sacrificing utility, essential for enterprise deployments.
- **Context Window**: 500k+ token capacity allows for processing entire codebases or library collections.
- **Native MCP 3.0 Support**: Full implementation of the Task Protocol for standardized tool-use and autonomous execution.

## Limitations
- **Closed Source**: The model weights and training methodologies are proprietary, unlike open models like Gemma 3.
- **Strict Rate Limits**: High-demand reasoning models (Opus) often have restrictive tiers on the free API.
- **Computational Cost**: Opus models are more expensive per token compared to Haiku or GPT-4o-mini.

## When to use it
- When you require the highest possible accuracy for complex coding or logical reasoning tasks.
- When working with very large documents that exceed the context limits of other models.
- When building production-grade agents that require strict adherence to safety and the **MCP 3.0 Task Protocol**.

## When not to use it
- For simple, low-stakes tasks where a cheaper model like Claude 3.5 Haiku or GPT-4o-mini is sufficient.
- If you require a fully local, offline model for air-gapped environments (use [vLLM](../infrastructure/vllm.md) with [Gemma 3](local_llms.md)).
- When you need a model with no safety filters or "uncensored" responses.

## Getting started

### Installation
Install the Anthropic Python SDK:
```bash
pip install anthropic
```

### Hello World Example
Quickly test connectivity and reasoning with a simple script:
```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-4-8-opus-20260528",
    max_tokens=10,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)
```

### Web Access
The web interface at [claude.ai](https://claude.ai/) is the most accessible way to interact with the models, featuring "Artifacts" for real-time code and UI previews.

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

### Python (Anthropic SDK)
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-4-8-opus-20260528",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Summarize the latest trends in Agentic Workflows."}
    ]
)

print(message.content[0].text)
```

### Tool Use (MCP 3.0)
```python
# Conceptual example of tool definition using MCP 3.0 Task Protocol
tools = [{
    "name": "get_weather",
    "description": "Get current weather in a location",
    "input_schema": {
        "type": "object",
        "properties": {"location": {"type": "string"}},
        "required": ["location"]
    }
}]

# Claude handles the decision to call the tool natively via MCP 3.0
```

## Related tools / concepts
- [GPT-5.5](chatgpt.md) — The leading reasoning competitor from OpenAI.
- [Gemma 3](local_llms.md) — Google's frontier open model (July 2026) for local deployment.
- [Everything Claude Code](everything-claude-code.md) — Comprehensive guide to the Claude Code ecosystem.
- [Claude How-To](claude-howto.md) — Practical implementation patterns and recipes.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for tool integration (MCP 3.0).
- [Anthropic](../providers/anthropic.md) — Provider overview.
- [Claude Code](../development_ops/claude-code.md) — Terminal-based agent details.
- [Claude Context Mode](../development_ops/claude-context-mode.md) — Managing large context windows.

## Sources / references
- [Official Website](https://claude.ai/)
- [Anthropic Console](https://console.anthropic.com/)
- [Claude API Documentation](https://docs.anthropic.com/claude/docs)
- [Anthropic Blog](https://www.anthropic.com/news)
- [MCP 3.0 Task Protocol Specification](https://modelcontextprotocol.io/spec/3.0/tasks)

## Contribution Metadata
- Last reviewed: 2026-07-02
- Confidence: high
