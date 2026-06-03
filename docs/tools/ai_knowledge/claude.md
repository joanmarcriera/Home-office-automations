# Claude

## What it is
Claude is a family of foundational large language models developed by Anthropic. It is designed to be helpful, honest, and harmless, with a strong focus on safety, steerability, and high-performance reasoning.

## What problem it solves
Claude provides state-of-the-art conversational and reasoning capabilities. It excels at complex tasks such as coding, creative writing, and data analysis, often with a more "human" and less robotic tone than other models. Its large context window allows it to process entire books or codebases in a single prompt.

## Where it fits in the stack
AI Model and Conversational Assistant. It can be accessed via the Claude.ai web interface, the Anthropic API, or through providers like AWS Bedrock and Google Cloud Vertex AI.

## Typical use cases
- Advanced coding assistance and software engineering tasks.
- Summarizing and analyzing large documents or datasets.
- Creative and technical writing.
- Building agentic workflows using its strong tool-calling capabilities.

## Strengths
- **Reasoning**: Particularly strong at logic and coding.
- **Tone**: Often perceived as more natural and nuanced than ChatGPT.
- **Context Window**: Supports very large contexts (up to 200k+ tokens).
- **Safety**: Built with "Constitutional AI" principles.

## Limitations
- **Availability**: Web interface access can be restricted in some regions.
- **Rate Limits**: Can be strict on the free tier.
- **Closed Source**: The model weights and training data are proprietary.

## When to use it
- When you need high-precision reasoning or coding assistance.
- When you are working with very long documents that exceed standard context limits.
- When you prefer a more conversational and less "assistant-like" tone.

## When not to use it
- If you require a fully local, offline model (use [Local LLMs](local_llms.md)).
- If you need a model with no censorship or safety filters.

## Licensing and cost
- **Open Source**: No (Proprietary).
- **Cost**: Free tier available; paid "Pro" subscription for higher limits; pay-as-you-go API.
- **Self-hostable**: No.

## Getting started

### Claude.ai Web Interface
The fastest way to use Claude is through the official web portal:
1. Visit [claude.ai](https://claude.ai/).
2. Create an account.
3. Start a conversation or upload files for analysis.

### Anthropic Console (API)
For developers looking to integrate Claude into applications:
1. Sign up at the [Anthropic Console](https://console.anthropic.com/).
2. Generate an API key.
3. Install the SDK: `pip install anthropic`.

## CLI examples

### Claude Code CLI
Anthropic's official terminal-based agent for coding:

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Authenticate and initialize in your project
claude auth login
claude init

# Ask a coding question or request a change
claude "Add a new endpoint to the API for user profile updates"
```

### Unofficial CLI (using `anthropic-cli`)
A lightweight wrapper for quick API interactions:

```bash
# Install via pip
pip install anthropic-cli

# Set your API key
export ANTHROPIC_API_KEY='your-api-key'

# Prompt Claude from the terminal
anthropic "Summarize the key features of the Matrix protocol"
```

## API examples

### Python (Anthropic SDK)
Basic message creation example using the modern API:

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain the concept of 'Constitutional AI' in two sentences."}
    ]
)

print(message.content[0].text)
```

### Streaming Responses
For real-time output in terminal or UI applications:

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short story about a time-traveling toaster."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Related tools / concepts
- [ChatGPT](chatgpt.md) — The primary conversational alternative.
- [Gemini](gemini.md) — Google's foundational model family.
- [Anthropic](../providers/anthropic.md) — The company behind Claude.
- [Claude Code](../development_ops/claude-code.md) — Detailed guide for the official CLI.
- [Everything Claude Code](everything-claude-code.md) — Comprehensive resource for Claude Code.
- [Claude How-To](claude-howto.md) — Practical guides and recipes.
- [MCP](../development_ops/claude-context-mode.md) — Model Context Protocol for Claude integrations.
- [AWS Bedrock](https://aws.amazon.com/bedrock/) — Enterprise access to Claude models.

## Sources / References
- [Official Website](https://claude.ai/)
- [Anthropic Website](https://www.anthropic.com/)
- [Claude Documentation](https://docs.anthropic.com/claude/docs)
- [Claude Code npm](https://www.npmjs.com/package/@anthropic-ai/claude-code)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-20
