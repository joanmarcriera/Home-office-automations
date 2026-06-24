# DeepSeek

## What it is
DeepSeek is a leading AI research company that provides a suite of high-performance LLMs, including specialized models for coding and reasoning. In June 2026, their flagship **DeepSeek-V4** and **DeepSeek-R2** reasoning models represent the global standard for cost-efficient, high-performance intelligence, frequently utilized as a baseline for model-agnostic agentic workflows.

## What problem it solves
It addresses the high cost and accessibility barriers of frontier AI. By providing models that achieve performance parity with models like **Claude 4.8 Opus** and **GPT-5.5** at a fraction of the price, it enables massive-scale autonomous engineering and complex research tasks that would be cost-prohibitive on other platforms.

## Where it fits in the stack
**Model Provider / Reasoning Engine**. It is a primary choice for high-volume coding tasks, mathematical reasoning, and as a backbone for open-weights self-hosted infrastructures.

## Typical use cases
- **Massive-Scale Code Refactoring**: Using DeepSeek-V4 to refactor large codebases where token volume is high.
- **Advanced Mathematical Reasoning**: Leveraging DeepSeek-R2 for solving complex symbolic logic and architectural planning tasks.
- **Autonomous Agent Backbone**: Serving as the primary inference engine for agents like [Roo Code](../agents/roo-code.md) and [Cline](../agents/cline.md) in cost-sensitive environments.
- **Local/Private Cloud Deployment**: Deploying open-weights versions of DeepSeek models for secure, air-gapped development.

## Strengths
- **Unmatched Price-to-Performance**: Industry-leading efficiency, offering frontier-level intelligence at significantly lower costs.
- **Reasoning Excellence**: The R-series (R1, R2) models excel at "System 2" thinking, outperforming many larger models on math and logic benchmarks.
- **Open Weights Heritage**: A strong commitment to releasing model weights, fostering a robust community of self-hosted and fine-tuned versions.
- **API Compatibility**: Full OpenAI-compatible API makes integration into existing agentic frameworks seamless.

## Limitations
- **Geographic Latency**: Native API latency can vary depending on the user's location relative to DeepSeek's primary clusters (mitigated via providers like [OpenRouter](../ai_knowledge/openrouter.md)).
- **Regulatory Environment**: Subject to local jurisdiction regulations which may influence model behavior or availability in certain markets.
- **Context Window Management**: While expanding, earlier versions required more careful context management compared to some Western competitors.

## When to use it
- When you need top-tier coding and reasoning performance for high-volume automated tasks.
- When budget efficiency is a primary driver for your AI infrastructure.
- When you require the ability to self-host or fine-tune model weights on your own hardware.
- For "agentic research" where a reasoning model is required for multi-step planning.

## When not to use it
- If your data residency or compliance requirements strictly forbid processing data through specific global regions.
- When you require the specific multimodal or ecosystem-locked features of **Claude 4.8** or **GPT-5.5**.

## Getting started

### API Access
1. Create an account at the [DeepSeek Platform](https://platform.deepseek.com/).
2. Generate an API key from the dashboard.
3. DeepSeek uses a standard credit-based billing system with extremely low per-token rates.

### Installation
DeepSeek is fully compatible with the OpenAI Python and Node.js SDKs.
```bash
pip install openai
```

## CLI examples

### Using curl for Quick Inference
```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "system", "content": "You are a professional software engineer."},
      {"role": "user", "content": "Write a thread-safe singleton in Rust."}
    ],
    "stream": false
  }'
```

## API examples

### Reasoning with DeepSeek-R2 (June 2026)
Utilizing the reasoning model for complex architectural decisions.

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com"
)

# DeepSeek-R2 provides chain-of-thought reasoning
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": "Design a globally distributed KV store with strong consistency."}
    ]
)

print(response.choices[0].message.content)
```

### High-Volume Code Generation
```python
response = client.chat.completions.create(
    model="deepseek-chat", # Points to V4 in June 2026
    messages=[
        {"role": "user", "content": "Implement a full-stack CRUD app using Next.js 16 and Supabase."}
    ]
)
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Qwen](../ai_knowledge/qwen.md)
- [Anthropic (Claude)](anthropic.md)
- [Minimax](minimax.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)
- [Roo Code](../agents/roo-code.md)
- [Cline](../agents/cline.md)
- [Aider](../development_ops/aider.md)

## Sources / references
- [Official Website](https://www.deepseek.com/)
- [DeepSeek API Documentation](https://platform.deepseek.com/api-docs/)
- [DeepSeek GitHub Organization](https://github.com/deepseek-ai)
- [DeepSeek-V4 Technical Report](https://deepseek.com/v4-report)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
