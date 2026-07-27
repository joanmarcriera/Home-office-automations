# Groq

## What it is
Groq is an AI infrastructure company that developed the Language Processing Unit (LPU), a new type of processor designed specifically for the extreme high-speed requirements of LLMs. As of July 2026, Groq is the industry benchmark for low-latency inference, supporting Llama 4 Maverick, Mixtral 10x22B, and the newly released Gemma 3 models.

## What problem it solves
Solves the "bottleneck" of slow LLM inference, providing near-instantaneous responses that enable real-time applications and highly interactive agents. It eliminates the latency hurdles that often hinder complex agentic workflows, particularly those utilizing the MCP 3.0 Task Protocol for multi-step reasoning.

## Where it fits in the stack
**Inference Provider / Infrastructure**. It provides a high-speed API for the most popular open-source models (Llama, Mixtral, Gemma).

## Typical use cases
- **Real-time Agents**: Voice assistants or interactive chatbots that require sub-second response times.
- **High-Volume Processing**: Summarizing or analyzing large quantities of text at hundreds of tokens per second.
- **Interactive Coding**: Powering coding assistants where immediate, fluid feedback is essential.
- **Autonomous Task Execution**: Serving as the fast inference backend for agents executing complex tasks via MCP 3.0.

## Strengths
- **Extreme Speed**: Often 10x+ faster than traditional GPU-based providers (400-800+ tokens/sec).
- **Open Model Support**: Focuses on the best open-weights models like Llama 4 and Gemma 3.
- **Low Latency**: Unmatched time-to-first-token (TTFT) and overall throughput.
- **LPU Efficiency**: Unlike GPUs which excel at parallel pixel processing, LPUs are optimized for the serial nature of text generation, eliminating the "memory wall" that slows down standard hardware.

## Limitations
- **Model Selection**: Limited to the open models they have specifically optimized for their LPU hardware.
- **Context Window**: Historically had smaller context windows than cloud giants, though this is expanding rapidly in 2026 to support 128k+ across most models.

## When to use it
- When response speed is the absolute top priority.
- For "agentic" workflows where an agent makes many sequential, recursive LLM calls.
- When using Llama or Mistral models and looking for the fastest possible user experience.

## When not to use it
- If you need proprietary models like GPT-4, GPT-5.5, or Claude 4.8.
- For extremely large context tasks (e.g., 1M+ tokens) where native large-context models like Gemini are superior.

## Getting started
Install the SDK:
```bash
pip install groq
```

Basic API call (Python):
```python
from groq import Groq

client = Groq()

chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "Explain LPU speed with Gemma 3."}],
    model="gemma-3-27b",
)
print(chat_completion.choices[0].message.content)
```

## CLI examples
```bash
# Query a model directly using the Groq API via curl
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
     -H "Authorization: Bearer $GROQ_API_KEY" \
     -d '{"model": "llama-4-70b", "messages": [{"role": "user", "content": "Hello"}]}'

# List available models via API
curl https://api.groq.com/openai/v1/models \
     -H "Authorization: Bearer $GROQ_API_KEY"

# Transcribe an audio file using the Whisper model via Groq's transcription endpoint
curl -X POST "https://api.groq.com/openai/v1/audio/transcriptions" \
     -H "Authorization: Bearer $GROQ_API_KEY" \
     -F "file=@sample.mp3" \
     -F "model=whisper-large-v3"
```

## API examples
Groq enables exceptionally fluid streaming responses using the OpenAI-compatible SDK.

```python
from groq import Groq

client = Groq()

stream = client.chat.completions.create(
    messages=[{"role": "user", "content": "Write a 500-word story."}],
    model="llama-4-70b",
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## Related tools / concepts
- [Together AI](together.md)
- [Fireworks AI](fireworks.md)
- [Mistral](mistral.md)
- [vLLM](../infrastructure/vllm.md)
- [SGLang](../infrastructure/sglang.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [LiteLLM](../../services/litellm.md)
- [Anthropic](anthropic.md)
- [Model Context Protocol](../automation_orchestration/mcp.md)

## Sources / references
- [Official Website](https://groq.com/)
- [Groq Cloud Console](https://console.groq.com/)
- [Groq Documentation](https://docs.groq.com/)

## Contribution Metadata
- Last reviewed: 2026-07-01
- Confidence: high
