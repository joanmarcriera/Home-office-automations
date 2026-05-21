# MiniMax

## What it is
MiniMax is a leading AI company that develops large-scale models across multiple modalities, including text, speech, video, and music. Their latest flagship models, the **M2.7** series, are optimized for reasoning, coding, and multi-modal creative tasks.

## What problem it solves
Provides high-performance LLMs with a particular focus on coding productivity and Agentic workflows. It offers a cost-effective alternative to global providers like Anthropic and OpenAI, especially for developers looking for high-value subscription plans that decouple cost from token-based billing.

## Where it fits in the stack
**LLM / Reasoning Engine / Provider**. It is particularly well-suited for integration into AI coding assistants and autonomous agents through its "Token Plan" subscription model.

## Typical use cases
- **AI-Assisted Coding**: Using the M2.7 model for complex software engineering and "vibe coding" tasks.
- **Agentic Workflows**: Leveraging the M2 series for multi-step reasoning and tool use in terminal-native agents.
- **Multimodal Generation**: Creating high-quality speech, video, and music via their specialized models (e.g., Hailuo for video).

## Strengths
- **M2.7 Architecture**: Optimized for multi-language programming and complex code engineering with low latency.
- **Token Plan Subscription**: Offers a predictable monthly cost (Starter/Plus/Max) with a 5-hour rolling reset window for requests, providing an alternative to per-token billing.
- **Broad Tool Compatibility**: Native support in popular coding agents like [Claude Code](../development_ops/claude-code.md), [Cursor](../development_ops/cursor.md), and [Cline](../agents/cline.md).
- **Anthropic Compatibility**: Supports calling models via the Anthropic SDK, allowing for seamless integration into Claude-native workflows.

## Limitations
- **Closed Source**: Proprietary models available only via API.
- **Regional Focus**: While globally accessible, documentation and pricing are primarily centered on the Asian market (RMB/¥).

## When to use it
- For heavy coding tasks where a fixed-cost subscription (Token Plan) is more economical than per-token billing.
- When you need a high-performance alternative to Claude 3.5 Sonnet with compatible API structures for terminal-native agents.

## When not to use it
- If you require fully open-source models for local deployment.
- If your workflow is strictly tied to OpenAI-specific features not supported by the Anthropic-compatible relay.


## Getting started

### API Key
1. Register on the [MiniMax Open Platform](https://platform.minimaxi.com/).
2. Navigate to "Account Management" -> "API Keys" to create your credentials.

### Installation (Python)
MiniMax is compatible with the OpenAI SDK.

```bash
pip install openai
```

### Usage (Hello World)
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_MINIMAX_API_KEY",
    base_url="https://api.minimax.chat/v1"
)

response = client.chat.completions.create(
    model="abab6.5s-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Explain the concept of 'Token Plan' in one sentence."}
    ]
)

print(response.choices[0].message.content)
```

## CLI examples

### Using curl
```bash
curl https://api.minimax.chat/v1/chat/completions   -H "Content-Type: application/json"   -H "Authorization: Bearer $MINIMAX_API_KEY"   -d '{
    "model": "abab6.5s-chat",
    "messages": [
      {"role": "user", "content": "Who founded MiniMax?"}
    ]
  }'
```

## API examples

### Anthropic SDK Compatibility
MiniMax also supports an Anthropic-compatible endpoint, which is useful for tools designed specifically for Claude models.

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="YOUR_MINIMAX_API_KEY",
    base_url="https://api.minimax.chat/v1/anthropic"
)

message = client.messages.create(
    model="abab6.5s-chat",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a Python script to calculate Fibonacci numbers."}
    ]
)
print(message.content)
```
## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription-based "Token Plan" and Pay-as-you-go "Credits")
- **Self-hostable**: No

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md)
- [Everything Claude Code](../ai_knowledge/everything-claude-code.md)
- [Cursor](../development_ops/cursor.md)
- [Cline](../agents/cline.md)
- [OpenClaw](../development_ops/openclaw.md)
- [Anthropic (Claude)](anthropic.md)
- [OpenRouter](../ai_knowledge/openrouter.md)

## Sources / References
- [Official Website](https://www.minimaxi.com/)
- [Open Platform](https://platform.minimaxi.com/)
- [Token Plan Overview](https://platform.minimaxi.com/docs/token-plan/intro)
- [MiniMax Documentation Index](https://platform.minimaxi.com/docs/llms.txt)

## Contribution Metadata
- Last reviewed: 2026-05-21
- Confidence: high
