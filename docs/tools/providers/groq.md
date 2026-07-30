# Groq

## What it is
Groq is an AI infrastructure company that developed the Language Processing Unit (LPU), a new type of processor designed specifically for the extreme high-speed requirements of LLMs. As of late October / November 2026, Groq is the industry benchmark for low-latency inference, supporting Llama 4, Mixtral 10x22B, and the Gemma 3 and Qwen 3.6 models.

## What problem it solves
Solves the "bottleneck" of slow LLM inference, providing near-instantaneous responses that enable real-time applications and highly interactive agents. It eliminates the latency hurdles that often hinder complex agentic workflows, particularly those utilizing the Model Context Protocol (MCP 3.1) Task Protocol for multi-step reasoning.

## Where it fits in the stack
**Inference Provider / Infrastructure**. It provides a high-speed API for the most popular open-source models (Llama, Mixtral, Gemma, Qwen).

## Typical use cases
- **Real-time Agents**: Voice assistants or interactive chatbots that require sub-second response times.
- **High-Volume Processing**: Summarizing or analyzing large quantities of text at hundreds of tokens per second.
- **Interactive Coding**: Powering coding assistants where immediate, fluid feedback is essential.
- **Autonomous Task Execution**: Serving as the fast inference backend for agents executing complex tasks via MCP 3.1.

## Strengths
- **Extreme Speed**: Often 10x+ faster than traditional GPU-based providers (400-800+ tokens/sec).
- **Open Model Support**: Focuses on the best open-weights models like Llama 4, Gemma 3, and Qwen 3.6.
- **Low Latency**: Unmatched time-to-first-token (TTFT) and overall throughput.
- **LPU Efficiency**: Unlike GPUs which excel at parallel pixel processing, LPUs are optimized for the serial nature of text generation, eliminating the "memory wall" that slows down standard hardware.

## Limitations
- **Model Selection**: Limited to the open models they have specifically optimized for their LPU hardware.
- **Context Window**: Historically had smaller context windows than cloud giants, though this is expanding rapidly in late 2026 to support 128k+ across most models.

## When to use it
- When response speed is the absolute top priority.
- For "agentic" workflows where an agent makes many sequential, recursive LLM calls.
- When using Llama or Mistral models and looking for the fastest possible user experience.

## When not to use it
- If you need proprietary models like GPT-5.5 or Claude 5.1.
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

### Fluid Streaming Response
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

### Response Schema and Validation using Pydantic v2
This Python script parses and validates structured telemetry or JSON outputs generated via Groq using **Pydantic v2**:

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class GroqUsageMetrics(BaseModel):
    prompt_tokens: int = Field(..., description="Number of tokens in the input prompt")
    completion_tokens: int = Field(..., description="Number of tokens generated in the completion")
    total_tokens: int = Field(..., description="Sum of prompt and completion tokens")
    prompt_time: float = Field(..., description="Time taken to process the prompt in seconds")
    completion_time: float = Field(..., description="Time taken to generate the completion in seconds")

class GroqResponseMetadata(BaseModel):
    id: str = Field(..., description="Unique chat completion identifier")
    model: str = Field(..., description="Model name evaluated")
    system_fingerprint: Optional[str] = Field(None, description="Groq system fingerprint")
    usage: GroqUsageMetrics = Field(..., description="LPU execution performance metrics")

def validate_groq_response(raw_json: str) -> Optional[GroqResponseMetadata]:
    try:
        data = json.loads(raw_json)
        # Validate result object with Pydantic v2 model_validate
        response_data = GroqResponseMetadata.model_validate(data)
        return response_data
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None
```

## Related tools / concepts
- [Together AI](together.md) — Fast serverless inference provider.
- [Fireworks AI](fireworks.md) — High-throughput open model platform.
- [Mistral AI](mistral.md) — Leading European open weights provider.
- [vLLM](../infrastructure/vllm.md) — High-performance self-hosted serving.
- [SGLang](../infrastructure/sglang.md) — Fast execution engine.
- [OpenRouter](../ai_knowledge/openrouter.md) — Unified API aggregator.
- [LiteLLM](../../services/litellm.md) — Multi-provider routing middleware.
- [Anthropic](anthropic.md) — Creator of Claude 5.1 and desktop agents.

## Sources / references
- [Official Website](https://groq.com/)
- [Groq Cloud Console](https://console.groq.com/)
- [Groq Documentation](https://docs.groq.com/)

## Contribution Metadata
- Last reviewed: 2026-11-04
- Confidence: high
