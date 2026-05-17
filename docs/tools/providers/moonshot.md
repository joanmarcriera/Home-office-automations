# Moonshot AI (Kimi)

## What it is
Moonshot AI (also known as Yuezhianmian) is a leading Chinese AI startup that developed the **Kimi** LLM family. Their latest model, **Kimi K2.6**, is designed for trillion-parameter reasoning and native long-context support.

## What problem it solves
Enables the processing and analysis of massive documents, entire codebases, or long conversation histories through its native support for exceptionally long context windows (supporting up to 256K tokens in K2.6).

## Where it fits in the stack
**LLM / Reasoning Engine / Provider**. Often used for "Chat with Document" applications, long-form content synthesis, and complex codebase navigation.

## Typical use cases
- **Large Document Analysis**: Summarizing and querying hundreds of pages of technical, legal, or medical text.
- **Codebase Navigation**: Providing context from an entire repository in a single prompt for better architectural understanding.
- **Intelligent Dialogue**: High-fidelity reasoning and visual reasoning (multimodal) in Chinese and English.

## Strengths
- **Native Long Context**: A pioneer in reliable 128k to 256k context windows, maintaining high retrieval accuracy (needle-in-a-haystack).
- **OpenAI Compatibility**: Kimi provides an OpenAI-compatible HTTP API, allowing developers to use the standard OpenAI SDKs by simply changing the `base_url`.
- **Trillion-Parameter Reasoning**: The K2.5/K2.6 models offer state-of-the-art performance in complex logic and professional code generation.
- **Tool Calling**: Robust support for function calling and external tool integration.

## Limitations
- **Regional Optimization**: While globally accessible via API, the web interface and primary optimizations are centered on mainland China.
- **API Specifics**: Certain Kimi-specific extensions (like the `thinking` parameter) require `extra_body` configuration in standard SDKs.

## When to use it
- When your primary requirement is processing very large amounts of text (256k tokens) in a single context window with high reliability.
- For applications requiring high-fidelity Chinese language processing and reasoning.

## When not to use it
- If your workload requires fully local execution for strict offline air-gapped security.
- For purely image-generation-centric tasks (where specialized models like Midjourney or Flux might be preferred).

## Getting started

Moonshot AI provides an OpenAI-compatible API, making it easy to integrate into existing applications.

### 1. Python SDK Installation
```bash
pip install --upgrade 'openai>=1.0'
```

### 2. Basic Chat Completion
Simply point the `base_url` to Moonshot's endpoint to use their models with the standard OpenAI client.

```python
from openai import OpenAI

client = OpenAI(
    api_key="$MOONSHOT_API_KEY",
    base_url="https://api.moonshot.ai/v1",
)

completion = client.chat.completions.create(
    model="moonshot-v1-128k", # Or moonshot-v1-auto for context-aware selection
    messages=[
        {"role": "system", "content": "You are Kimi, an AI assistant provided by Moonshot AI."},
        {"role": "user", "content": "Analyze this 200-page document for key financial risks."}
    ],
)

print(completion.choices[0].message.content)
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Usage-based pricing; free trial credits available for new developers)
- **Self-hostable**: No

## Related tools / concepts
- [Dify](../ai_knowledge/dify.md)
- [LangChain](../ai_knowledge/langchain.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Perplexity](../ai_knowledge/perplexity.md)
- [DeepSeek](deepseek.md)
- [MiniMax](minimax.md)

## Sources / References
- [Official Website](https://www.moonshot.cn/)
- [Kimi Open Platform](https://platform.kimi.ai/)
- [API Overview & Compatibility](https://platform.kimi.ai/docs/api/overview)
- [Quickstart Guide](https://platform.kimi.ai/docs/guide/start-using-kimi-api)

## Contribution Metadata
- Last reviewed: 2026-05-17
- Confidence: high
