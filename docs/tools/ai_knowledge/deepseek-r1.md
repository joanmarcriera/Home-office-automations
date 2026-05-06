# DeepSeek R1

## What it is
DeepSeek R1 is a SOTA open-weights reasoning model that uses reinforcement learning (RL) to achieve high-level performance in math, coding, and logical reasoning, rivaling proprietary models like OpenAI's o1.

## What problem it solves
It provides a high-reasoning, "thinking" model that is accessible as open weights, allowing for complex multi-step planning and validation without the high cost or privacy concerns of proprietary reasoning APIs.

## Where it fits in the stack
**Category**: Tool / AI Assistants & Knowledge

## Typical use cases
- Complex code generation and debugging.
- Solving advanced mathematical and logical puzzles.
- Reasoning-heavy agentic workflows (e.g., architecture planning).

## Strengths
- SOTA performance for an open-weights model.
- Transparent "Chain of Thought" (CoT) generation.
- Highly cost-effective compared to proprietary reasoning models.

## Limitations
- Higher latency due to the "thinking" process.
- May over-reason on simple tasks.

## When to use it
- For tasks where correctness is more important than speed.
- When you need a logic-heavy model that you can self-host or access via low-cost providers.

## Licensing and cost
- **License**: DeepSeek License (Open Weights)
- **Cost**: Low-cost API access via DeepSeek or OpenRouter; free to self-host.

## Getting started

### Installation
DeepSeek R1 is accessible via an OpenAI-compatible API or can be run locally using Ollama.

```bash
# To run locally via Ollama
ollama run deepseek-r1
```

### Basic API setup (Python)
```bash
pip install openai
```

## CLI examples

### 1. Basic Chat Completion (curl)
```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
        "model": "deepseek-v4-pro",
        "messages": [
          {"role": "user", "content": "Explain quantum entanglement like I am five."}
        ],
        "stream": false
      }'
```

### 2. Reasoning Mode (Thinking enabled)
```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{
        "model": "deepseek-v4-pro",
        "messages": [
          {"role": "user", "content": "Find the derivative of x^2 * sin(x)."}
        ],
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high"
      }'
```

### 3. List Available Models
```bash
curl https://api.deepseek.com/models \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"
```

## API examples

### Python (OpenAI SDK)
```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_DEEPSEEK_API_KEY", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "user", "content": "Write a Python function to sort a list of dictionaries by a specific key."}
    ],
    extra_body={"thinking": {"type": "enabled"}}
)

print(f"Thought: {response.choices[0].message.reasoning_content}")
print(f"Answer: {response.choices[0].message.content}")
```

## Related tools / concepts
- [DeepSeek](deepseek.md)
- [OpenRouter](openrouter.md)
- [Ollama](../../services/ollama.md)
- [ChatGPT](chatgpt.md)
- [Claude](claude.md)
- [Local LLMs](local_llms.md)

## Sources / References
- [DeepSeek Official Site](https://www.deepseek.com/)
- [DeepSeek R1 Technical Report](https://github.com/deepseek-ai/DeepSeek-R1)
- [DeepSeek API Documentation](https://api-docs.deepseek.com/)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
