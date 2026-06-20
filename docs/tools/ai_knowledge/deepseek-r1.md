# DeepSeek R1

## What it is
DeepSeek R1 is a state-of-the-art (SOTA) open-weights reasoning model developed by DeepSeek. It utilizes large-scale reinforcement learning (RL) to achieve high-level performance in complex reasoning tasks, including mathematics, coding, and logical deduction. As of June 2026, it remains a primary benchmark for open-weights "thinking" models, rivaling proprietary architectures like OpenAI's o1 and Gemini 3.5.

## What problem it solves
It provides an accessible, high-reasoning alternative to proprietary "black box" models. DeepSeek R1 addresses the need for transparent "Chain of Thought" (CoT) processing, allowing developers and researchers to audit the model's reasoning steps. It enables complex multi-step planning and validation without the high operational costs or data privacy concerns associated with closed-source reasoning APIs.

## Where it fits in the stack
**Category**: Tool / AI Assistants & Knowledge
DeepSeek R1 serves as the "Reasoning Engine" within agentic stacks, often orchestrated by LiteLLM or OpenRouter and integrated into workflows via MCP 3.0.

## Typical use cases
- **Complex Code Orchestration**: Generating, debugging, and refactoring sophisticated multi-file software architectures.
- **Advanced Mathematical Reasoning**: Solving high-level symbolic logic and competitive mathematics problems.
- **Agentic Planning**: Serving as the "Brain" for autonomous agents requiring long-horizon planning and self-correction.
- **Knowledge Synthesis**: Summarizing and connecting disparate technical concepts with high logical consistency.

## Strengths
- **Open Weights Performance**: Delivers performance comparable to the best proprietary reasoning models while remaining open-source.
- **Transparent Reasoning**: Native support for visible "thinking" tokens, enabling better debugging and trust.
- **Cost-Effective**: Significantly lower token costs via API (DeepSeek/OpenRouter) compared to competitors.
- **Licensing**: Released under the DeepSeek License, allowing for broad commercial use and self-hosting.
- **Distilled Variants**: Offers smaller models (e.g., Llama/Qwen-based distillations) that run on consumer-grade hardware.

## Limitations
- **High Latency**: The "thinking" process introduces a delay (~10-60s) before final output generation begins.
- **Over-Reasoning**: May apply excessive logic to simple tasks, leading to verbosity and increased token usage.
- **Infrastructure Requirements**: The full 671B parameter model requires significant VRAM (80GB+ even with quantization) for high-performance self-hosting.

## When to use it
- When correctness and logical depth are prioritized over response speed.
- For tasks requiring formal verification, complex math, or intricate coding logic.
- When you need to self-host a top-tier reasoning model for privacy or compliance reasons.

## When not to use it
- **Low-Latency Chat**: For simple conversational tasks or basic Q&A where a fast model like Llama 3.2-3B or Gemini 3.5 Flash is more efficient.
- **Resource-Constrained Environments**: If you cannot access the full model via API or lack the 40GB+ VRAM required for distilled local versions.
- **Basic Summarization**: Where heavy reasoning is not required to extract key points.

## Getting started

### Local Setup (Ollama)
DeepSeek R1 distilled versions are highly optimized for local execution.

```bash
# Run a distilled 14B version locally
ollama run deepseek-r1:14b
```

### API Access (OpenRouter)
As of June 2026, OpenRouter remains the preferred gateway for accessing the full R1-671B model with unified billing.

```bash
# Ensure your environment variable is set
export OPENROUTER_API_KEY="your_api_key"
```

## CLI examples

### 1. Basic Reasoning Query (curl)
```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
        "model": "deepseek-reasoner",
        "messages": [
          {"role": "user", "content": "Explain the P vs NP problem using a library analogy."}
        ]
      }'
```

### 2. Streaming with Reasoning (Thinking)
```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
        "model": "deepseek-reasoner",
        "messages": [
          {"role": "user", "content": "Write a formal proof that the square root of 2 is irrational."}
        ],
        "stream": true
      }'
```

## API examples

### Python (OpenAI SDK with Thinking)
Using the standard OpenAI client to capture the reasoning content specifically.

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_DEEPSEEK_API_KEY", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": "Design a secure multi-tenant architecture for a SaaS app on AWS."}
    ]
)

# DeepSeek R1 returns reasoning in reasoning_content
print(f"--- Thought ---\n{response.choices[0].message.reasoning_content}")
print(f"--- Answer ---\n{response.choices[0].message.content}")
```

### LiteLLM Integration (MCP 3.0 Compatible)
```python
import litellm

response = litellm.completion(
    model="deepseek/deepseek-reasoner",
    messages=[{"role": "user", "content": "Optimize this SQL query for high-concurrency."}],
    api_base="https://api.deepseek.com"
)
print(response.choices[0].message.content)
```

## Related tools / concepts
- [OpenRouter](openrouter.md) — Unified API access for R1 and competitors.
- [Ollama](../../services/ollama.md) — Local runner for distilled R1 versions.
- [ChatGPT](chatgpt.md) — Comparison model (OpenAI o1).
- [Claude](claude.md) — Comparison model (Claude 4.8 Opus).
- [Gemini](gemini.md) — Comparison model (Gemini 3.5 Ultra).
- [Local LLMs](local_llms.md) — Overview of open-weights alternatives.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md) — Strategy for routing reasoning tasks to R1.
- [LiteLLM](../../services/litellm.md) — Proxy for managing DeepSeek API keys.
- [Perplexity](perplexity.md) — Agentic search tool often used alongside R1.
- [Google Search](google-search.md) — Integrated search for grounding R1 outputs.

## Sources / references
- [DeepSeek Official Site](https://www.deepseek.com/)
- [DeepSeek R1 Technical Report (GitHub)](https://github.com/deepseek-ai/DeepSeek-R1)
- [DeepSeek API Documentation](https://api-docs.deepseek.com/)
- [Model Context Protocol (MCP) Integration](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
