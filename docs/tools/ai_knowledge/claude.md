# Claude

## What it is
Claude is a family of foundational large language models developed by Anthropic, designed with "Constitutional AI" principles to be helpful, honest, and harmless. As of June 2026, the flagship model is **Claude 4.8 Opus** (`claude-4-8-opus-20260528`), which sets the industry standard for high-fidelity reasoning, complex coding, and nuanced linguistic understanding. It is a proprietary model available via API, web interface, and major cloud providers.

## What problem it solves
Claude provides state-of-the-art conversational and reasoning capabilities. It excels at complex tasks such as coding, creative writing, and data analysis, often with a more "human" and less robotic tone than other models. Its large context window (supporting up to 500k tokens in some configurations) allows it to process entire codebases or library-sized document sets in a single prompt with high retrieval accuracy.

## Where it fits in the stack
AI Reasoning and Orchestration Layer. It serves as the primary "brain" for agentic workflows, complex software engineering tasks (via Claude Code), and enterprise-grade RAG (Retrieval-Augmented Generation) systems. It can be accessed via the Claude.ai web interface, the Anthropic API, or through providers like AWS Bedrock and Google Cloud Vertex AI.

## Typical use cases
- **Autonomous Software Engineering**: Driving complex code migrations and feature implementations using the Claude Code CLI.
- **Large-Scale Document Analysis**: Summarizing and extracting insights from massive datasets or entire technical libraries.
- **High-Fidelity Content Generation**: Producing technical documentation and research reports with high stylistic control.
- **Tool-Use and Agency**: Acting as a controller for Model Context Protocol (MCP) servers to interact with external tools and data.

## Strengths
- **Superior Reasoning**: Consistently outperforms competitors in logic-heavy and multi-step reasoning benchmarks.
- **Context Window**: Ability to process extremely long inputs with high "needle-in-a-haystack" retrieval accuracy.
- **Safety**: Built-in constitutional guardrails reduce the risk of harmful or biased outputs.
- **Natural Tone**: Nuanced communication style that is often preferred for user-facing applications.

## Limitations
- **Proprietary**: Not open-weight; requires reliance on Anthropic's infrastructure or approved cloud partners.
- **Rate Limits**: High-tier models like Opus have stricter rate limits compared to smaller, faster models.
- **Cost**: As a premium reasoning model, it carries a higher price point per token than "Haiku" or "Sonnet" class models.

## When to use it
- When you require high-precision reasoning or complex coding assistance.
- When working with very long documents that exceed standard context limits.
- When you prefer a more conversational and less "assistant-like" tone.

## When not to use it
- If you require a fully local, offline model (use [Local LLMs](local_llms.md)).
- If you need a model with no censorship or safety filters.
- For simple, low-latency tasks like basic classification (use Claude 3.5 Haiku).

## Model routing

Anthropic models are categorized into three "tiers" of capability. Choosing the right tier depends on the complexity of the reasoning required.

| Tier | Model | Recommended Use Case |
| :--- | :--- | :--- |
| **Haiku** | Claude 3.5 Haiku | Low-latency, high-volume tasks like extraction and classification. |
| **Sonnet** | Claude 3.5 Sonnet | The default choice for most agentic workflows, coding, and tool use. |
| **Opus** | Claude 4.8 Opus | Extreme logic puzzles, high-fidelity creative work, and repository-wide engineering. |

See the central policy: [Model Routing Guide](../../knowledge_base/model_routing_guide.md).

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

### Unofficial API Access (using `curl`)
Direct interaction with the Messages API:

```bash
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data '{
       "model": "claude-4-8-opus-20260528",
       "max_tokens": 1024,
       "messages": [{"role": "user", "content": "Explain the PagedAttention algorithm."}]
     }'
```

## API examples

### Python (Anthropic SDK)
Standard request using the June 2026 stable SDK:

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-4-8-opus-20260528",
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
    model="claude-4-8-opus-20260528",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short story about a time-traveling toaster."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Related tools / concepts
- [ChatGPT](chatgpt.md) — The primary conversational alternative (GPT-5.5).
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
- Last reviewed: 2026-06-15
- Confidence: high
