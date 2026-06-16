# DeepSeek

## What it is
DeepSeek is a leading AI research organization specializing in high-performance, cost-effective large language models (LLMs). As of June 2026, their flagship model is **DeepSeek-V4**, which utilizes a sophisticated Mixture-of-Experts (MoE) architecture to provide frontier-level reasoning and coding capabilities. DeepSeek is known for its "open-weights" philosophy and for pushing the boundaries of what is possible with efficient model training and inference.

## What problem it solves
It addresses the high cost and "black box" nature of proprietary frontier models. DeepSeek provides models that rival the performance of GPT-5.5 and Claude 4.8 Opus in specific domains—particularly mathematics, logic, and software engineering—at a significantly lower price point. It allows developers to use state-of-the-art AI without being locked into a single ecosystem.

## Where it fits in the stack
**Category**: Provider / AI Assistants & Knowledge. It serves as a foundational inference layer, often used as a primary or fallback model in multi-model routing systems like OpenRouter or within autonomous coding agents.

## Typical use cases
- **Autonomous Engineering**: Powering agents like [Cline](../agents/cline.md) and [Roo Code](../agents/roo-code.md) for complex codebase modifications.
- **Mathematical Reasoning**: Solving advanced symbolic math and competitive programming problems via the DeepSeek-R1 reasoning series and its successors.
- **Cost-Optimized RAG**: Serving as a high-throughput, low-latency engine for retrieval-augmented generation pipelines.
- **Synthetic Data Generation**: Using DeepSeek-V4 to generate high-quality training data for smaller, specialized models.

## Strengths
- **SOTA Performance**: Consistently ranks at the top of coding (HumanEval) and math (MATH) benchmarks.
- **OpenWeights**: Allows for local hosting and fine-tuning for specialized enterprise needs.
- **OpenAI-Compatible API**: Drop-in replacement for existing OpenAI-based integrations.
- **Extreme Efficiency**: High tokens-per-second (TPS) throughput even on standard consumer-grade hardware for smaller variants.

## Limitations
- **Data Privacy**: While improved, some enterprise users may have concerns regarding data residency depending on the deployment region.
- **Context Window Utilization**: While the context window is large (256k+), performance can degrade slightly at the extreme edges compared to Claude 4.8 Opus.
- **General Knowledge**: Occasionally trails slightly behind GPT-5.5 in broad, multi-modal creative tasks.

## When to use it
- For any coding-centric task where Claude 4.8 Opus is too expensive.
- When building local-first agentic systems that require high-reasoning open-weights models.
- When you need a highly reliable, OpenAI-compatible secondary provider for redundancy.

## When not to use it
- If your compliance framework strictly forbids the use of models from specific jurisdictions.
- For extremely high-fidelity creative writing where the "tone" of Anthropic models is preferred.

## Getting started

### API Key
1. Create an account at [DeepSeek Platform](https://platform.deepseek.com/).
2. Generate an API key from the "API Keys" section.

### Installation (Python)
DeepSeek provides an OpenAI-compatible API.

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
        {"role": "user", "content": "Explain DeepSeek-V4 MoE architecture."},
    ],
    stream=False
)

print(response.choices[0].message.content)
```

## CLI examples

### Using curl
```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant"},
          {"role": "user", "content": "What is the capital of France?"}
        ],
        "stream": false
      }'
```

### Using OpenRouter CLI
If using DeepSeek via OpenRouter:
```bash
openrouter chat "deepseek/deepseek-chat" "Explain quantum computing."
```

## API examples

### Using the Reasoner Model (R1)
The reasoning series is optimized for chain-of-thought tasks.

```python
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": "Prove that there are infinitely many primes."}
    ]
)
# Note: reasoner models often include a 'reasoning_content' field in the response
# print(response.choices[0].message.reasoning_content)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) — Multi-model gateway including DeepSeek.
- [Qwen](../ai_knowledge/qwen.md) — Competitive open-weights models from Alibaba.
- [Anthropic](anthropic.md) — Primary competitor for high-reasoning tasks.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — Strategy for switching between models.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Implementation patterns for autonomous agents.
- [Roo Code](../agents/roo-code.md) — IDE agent with deep DeepSeek integration.
- [Cline](../agents/cline.md) — Autonomous coding assistant frequently used with DeepSeek.
- [Aider](../development_ops/aider.md) — CLI coding tool optimized for DeepSeek's low latency.

## Sources / references
- [Official Website](https://www.deepseek.com/)
- [DeepSeek API Documentation](https://api-docs.deepseek.com/)
- [GitHub](https://github.com/deepseek-ai)
- [DeepSeek-R1 Release Blog](https://api-docs.deepseek.com/news/news250120)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
