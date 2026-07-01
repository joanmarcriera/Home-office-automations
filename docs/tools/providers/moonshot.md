# Moonshot AI (Kimi)

## What it is
Moonshot AI (also known as Yuezhianmian) is a leading Chinese AI startup that developed the **Kimi** LLM family. As of July 2026, their flagship model is **Kimi K2.6**, which features trillion-parameter reasoning and native support for 256K token context windows.

## What problem it solves
Enables the processing and analysis of massive documents, entire codebases, or long conversation histories. It serves as a high-performance alternative to `claude-4-8-opus-20260528` and GPT-5.5 for long-context reasoning tasks, particularly in Chinese-language environments. In July 2026, it is frequently used with the MCP 3.0 Task Protocol for complex, multi-modal reasoning.

## Where it fits in the stack
**LLM / Reasoning Engine / Provider**. Often used for "Chat with Document" applications, long-form content synthesis, and complex codebase navigation.

## Typical use cases
- **Large Document Analysis**: Summarizing and querying hundreds of pages of technical, legal, or medical text.
- **Codebase Navigation**: Providing context from an entire repository in a single prompt for better architectural understanding.
- **Intelligent Dialogue**: High-fidelity reasoning and visual reasoning (multimodal) in Chinese and English.
- **Automated Research**: Leveraging Kimi's long context for deep-dive literature reviews and data synthesis.

## Strengths
- **Native Long Context**: A pioneer in reliable 128k to 256k context windows, maintaining high retrieval accuracy (needle-in-a-haystack).
- **OpenAI Compatibility**: Kimi provides an OpenAI-compatible HTTP API, allowing developers to use the standard OpenAI SDKs by simply changing the `base_url`.
- **Trillion-Parameter Reasoning**: The K2.6 models offer state-of-the-art performance in complex logic and professional code generation.
- **Tool Calling**: Robust support for function calling and external tool integration, now optimized for MCP 3.0.

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
Moonshot AI provides an OpenAI-compatible API. Install the SDK:

```bash
pip install --upgrade 'openai>=1.0'
```

Initialize the client with the Moonshot base URL:

```python
from openai import OpenAI

client = OpenAI(
    api_key="$MOONSHOT_API_KEY",
    base_url="https://api.moonshot.ai/v1",
)
```

## CLI examples
```bash
# Test connection via curl
curl https://api.moonshot.ai/v1/models \
     -H "Authorization: Bearer $MOONSHOT_API_KEY"

# Chat via CLI using curl
curl https://api.moonshot.ai/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $MOONSHOT_API_KEY" \
     -d '{"model": "moonshot-v1-8k", "messages": [{"role": "user", "content": "Hi"}]}'
```

## API examples
Basic chat completion using the OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    api_key="$MOONSHOT_API_KEY",
    base_url="https://api.moonshot.ai/v1",
)

completion = client.chat.completions.create(
    model="moonshot-v1-256k",
    messages=[
        {"role": "system", "content": "You are Kimi."},
        {"role": "user", "content": "Summarize this long document."}
    ],
)
print(completion.choices[0].message.content)
```

## Related tools / concepts
- [Dify](../ai_knowledge/dify.md)
- [LangChain](../ai_knowledge/langchain.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Perplexity](../ai_knowledge/perplexity.md)
- [DeepSeek](deepseek.md)
- [MiniMax](minimax.md)
- [Kimi Code CLI](../ai_knowledge/kimi-cli.md)
- [Model Context Protocol](../automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://www.moonshot.cn/)
- [Kimi Open Platform](https://platform.kimi.ai/)
- [API Overview & Compatibility](https://platform.kimi.ai/docs/api/overview)
- [Quickstart Guide](https://platform.kimi.ai/docs/guide/start-using-kimi-api)

## Contribution Metadata
- Last reviewed: 2026-07-01
- Confidence: high
