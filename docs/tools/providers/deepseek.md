# DeepSeek

## What it is
DeepSeek is an AI research company that provides a suite of high-performance LLMs, including specialized models for coding and reasoning.

## What problem it solves
It offers a cost-effective, high-quality alternative to Western LLM providers, often outperforming much larger models on benchmarks like HumanEval and GSM8K.

## Where it fits in the stack
**Category**: Provider / AI Assistants & Knowledge

## Typical use cases
- Code generation and assistance (DeepSeek Coder).
- Mathematical reasoning and problem solving.
- Cost-efficient LLM inference via API.

## Strengths
- State-of-the-art performance on coding and math tasks.
- Highly competitive pricing compared to GPT-4o or Claude 3.5.
- Open-weights versions available for many models.

## Limitations
- Latency can be variable depending on geographic region.
- Subject to local regulations that may differ from Western standards.

## When to use it
- When you need top-tier coding performance at a fraction of the cost.
- When you want to experiment with open-weights SOTA models.

## When not to use it
- If your data residency requirements strictly forbid processing in certain jurisdictions.

## What changed
- **DeepSeek R1 Launch**: DeepSeek released R1, a reasoning model that achieves performance parity with OpenAI's o1-preview on math, code, and logic benchmarks.
- **V3 Model Updates**: Improvements to the V3 model architecture for better instruction following and lower latency.


## Getting started

### API Key
1. Create an account at [DeepSeek Platform](https://platform.deepseek.com/).
2. Generate an API key from the "API Keys" section.

### Installation (Python)
DeepSeek provides an OpenAI-compatible API, allowing you to use the standard `openai` library.

```bash
pip install openai
```

### Usage (Hello World)
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello!"},
    ],
    stream=False
)

print(response.choices[0].message.content)
```

## CLI examples

### Using curl
You can interact with the DeepSeek API directly using `curl`:

```bash
curl https://api.deepseek.com/chat/completions   -H "Content-Type: application/json"   -H "Authorization: Bearer $DEEPSEEK_API_KEY"   -d '{
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant"},
          {"role": "user", "content": "Explain quantum entanglement in one sentence."}
        ],
        "stream": false
      }'
```

## API examples

### Model Selection
DeepSeek offers several models optimized for different tasks:
- `deepseek-chat`: General purpose chat model (V3).
- `deepseek-reasoner`: Reasoning-focused model (R1).

```python
# Example for R1 Reasoning model
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": "Solve for x: 2x + 5 = 15"}
    ]
)
```

## Licensing and cost
- **Open Source**: Open-weights (DeepSeek License)
- **Cost**: Paid API (Freemium tier often available)
- **Self-hostable**: Yes (for open-weights models)

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Qwen](../ai_knowledge/qwen.md)
- [Anthropic](anthropic.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Roo Code](../agents/roo-code.md)
- [Cline](../agents/cline.md)
- [Aider](../development_ops/aider.md)

## Sources / References
- [Official Website](https://www.deepseek.com/)
- [DeepSeek API Docs](https://platform.deepseek.com/)
- [GitHub](https://github.com/deepseek-ai)
- [DeepSeek-R1 Release Blog](https://api-docs.deepseek.com/news/news250120)

## Contribution Metadata
- Last reviewed: 2026-05-21
- Confidence: high
