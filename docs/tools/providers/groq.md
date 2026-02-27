# Groq

## What it is
Groq is an AI infrastructure company that developed the Language Processing Unit (LPU), a new type of processor designed specifically for the high-speed requirements of LLMs.

## What problem it solves
Solves the "bottleneck" of slow LLM inference, providing near-instantaneous responses that enable real-time applications and highly interactive agents.

## Where it fits in the stack
**Inference Provider / Infrastructure**. It provides a high-speed API for popular open-source models.

## Typical use cases
- **Real-time Agents**: Voice assistants or chatbots that require sub-second response times.
- **High-Volume Processing**: Summarizing or analyzing large quantities of text quickly.
- **Interactive Coding**: Powering coding assistants where immediate feedback is essential.

## Getting started
Install the SDK:
```bash
pip install groq
```

Basic API call:
```python
from groq import Groq

client = Groq()

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of low latency in AI.",
        }
    ],
    model="llama3-70b-8192",
)

print(chat_completion.choices[0].message.content)
```

## Strengths
- **Extreme Speed**: Often 10x+ faster than traditional GPU-based providers.
- **Open Model Support**: Focuses on the best open-weights models like Llama 3 and Mixtral.
- **Low Latency**: Unmatched time-to-first-token (TTFT) and tokens per second.
- **Pricing**: Very competitive token-based pricing. Offers a generous free tier for developers to experiment.

## Limitations
- **Model Selection**: Limited to the open models they have optimized for their LPU hardware.
- **Context Window**: Historically had smaller context windows than some cloud providers, though this is expanding.

## When to use it
- When speed is the absolute priority.
- For "agentic" workflows where an agent makes many sequential LLM calls.
- When using Llama or Mistral models and looking for the fastest possible response.

## When not to use it
- If you need proprietary models like GPT-4 or Claude.
- For extremely large context tasks (e.g., 200k tokens) that exceed their LPU memory limits.

## Licensing and cost
- **Open Source**: No (Proprietary hardware/platform).
- **Cost**: Paid (Usage-based), Free tier available.
- **Self-hostable**: No (Cloud service).

## Related tools / concepts
- [Together AI](together.md)
- [Fireworks AI](fireworks.md)
- [vLLM](../infrastructure/vllm.md)

## Sources / References
- [Official Website](https://groq.com/)
- [Groq Cloud Console](https://console.groq.com/)
- [Groq Documentation](https://docs.groq.com/)

## Contribution Metadata
- Last reviewed: 2026-02-27
- Confidence: high
