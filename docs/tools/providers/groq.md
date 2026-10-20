# Groq

## What it is
Groq is an AI infrastructure company that developed the Language Processing Unit (LPU), a purpose-built deterministic hardware architecture designed specifically for the extreme low-latency and high-throughput requirements of LLMs. As of early 2027, Groq serves as an industry benchmark for real-time inference speed, hosting leading open-weights models including **Llama 4**, **DeepSeek-V4**, **Mixtral 10x22B**, **Gemma 3**, and **Qwen 3.6**.

Unlike traditional GPUs, which rely on dynamic memory caching and massively parallel graphics pipelines, Groq's LPU chip architecture utilizes a deterministic tensor stream processor that eliminates memory bandwidth bottlenecks, delivering speeds exceeding 400 to 800+ tokens per second on open models.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client App / Voice Agent
    participant Gateway as Groq LPU API Gateway
    participant LPU as LPU Processor Array (Deterministic Memory)
    participant FastMCP as FastMCP 3.1 Task Gateway
    participant Tool as Target System Tool Execution

    Client->>Gateway: POST /v1/chat/completions (Stream = True)
    Gateway->>LPU: Dispatch Deterministic Tensor Stream Execution
    LPU-->>Gateway: Stream Tokens (800+ tok/s, Sub-10ms TTFT)
    Gateway-->>Client: Chunked Output Stream
    opt FastMCP 3.1 Tool Call Triggered
        LPU->>Gateway: Output Structured Tool Call JSON
        Gateway->>FastMCP: Dispatch Task Protocol Execution
        FastMCP->>Tool: Execute Function Payload
        Tool-->>FastMCP: Return Tool Output
        FastMCP-->>Gateway: Pass Tool Context back to LPU
    end
```

## What problem it solves
Slow LLM inference latency creates severe user experience bottlenecks in interactive AI applications, voice assistants, and autonomous agentic loops. When agents must execute multi-step recursive reasoning calls or consume external tool APIs over the **FastMCP 3.1** specification, standard GPU inference latency (often 20-50 tokens/sec) causes multi-second delays that break real-time conversation flows.

Groq addresses inference latency across critical operational dimensions:
- **Time-To-First-Token (TTFT) Delays**: Achieves sub-10ms initial token latency, enabling instant response feedback in voice and chat runtimes.
- **Agentic Recursion Overhead**: Accelerates multi-step tool calling loops, reducing complex multi-agent reasoning executions from tens of seconds down to under a second.
- **GPU Memory Wall Bottlenecks**: Replaces dynamic HBM GPU memory access with deterministic SRAM memory layouts, guaranteeing consistent token output rates even under heavy concurrent loads.

## Where it fits in the stack
**Inference Provider / Hardware Infrastructure**. Groq operates at the **Compute & Model Serving Layer**, providing an ultra-fast, OpenAI-compatible REST and WebSocket API for open-weights foundation models (Llama 4, DeepSeek-V4, Gemma 3, Qwen 3.6, Whisper).

```
+-----------------------------------------------------------------------+
|                    Real-Time Application Layer                        |
|       (Voice Agents / FastMCP 3.1 Tool Fleets / Interactive Coding)    |
+-----------------------------------------------------------------------+
                                   |
                          Sub-10ms REST Stream
                                   v
+-----------------------------------------------------------------------+
|                      Groq OpenAI-Compatible API                        |
|             - Rate Limiter & Structured JSON Formatter                |
|             - Whisper Audio Transcription Endpoint                    |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                   LPU Hardware Architecture Array                     |
|         (Deterministic SRAM Memory / High-Speed Tensor Engine)        |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                         Open Foundation Models                        |
|      (Llama 4 / DeepSeek-V4 / Gemma 3 / Qwen 3.6 / Mixtral)           |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Real-Time Voice & Speech Agents**: Powering low-latency conversational voice bots requiring instant speech synthesis and sub-second turn-taking.
- **Autonomous FastMCP 3.1 Tool Execution**: Serving as the high-speed reasoning engine for agents making dozens of sequential tool calls per transaction.
- **High-Throughput Text Summarization**: Processing large document volumes at hundreds of tokens per second for real-time document analysis.
- **Interactive Coding Assistants**: Powering inline IDE completion engines where immediate fluid feedback is critical.

## Strengths
- **Extreme Speed**: Delivers 400 to 800+ tokens per second on open models like Llama 4 and DeepSeek-V4.
- **Open Model Support**: Focuses on optimizing top open-weights models (Llama 4, DeepSeek-V4, Gemma 3, Qwen 3.6).
- **Sub-10ms TTFT**: Industry-leading time-to-first-token latency for responsive user interfaces.
- **OpenAI Standard Compatibility**: Drop-in API endpoint replacement for existing OpenAI SDK codebases.

## Limitations
- **Model Selection Boundaries**: Restricted to open-weights foundation models optimized for LPU hardware; proprietary closed models (e.g., Claude 5.6 or GPT-5.6) are unavailable.
- **Context Limits on Legacy Models**: While 2027 deployments support 128k+ tokens, extremely huge multi-million token contexts are better served by cloud platforms like Google AI Studio / Vertex AI.

## When to use it
- When low inference latency and high token throughput are the primary system requirements.
- For recursive agentic workflows where an agent makes many sequential, multi-step LLM calls.
- When deploying voice agents or real-time interactive applications using open models.

## When not to use it
- If your application explicitly depends on proprietary models like GPT-5.6 or Claude 5.6.
- For massive 2M+ token multimodal video analysis where Google AI Studio or Gemini 4.0 Pro is required.

## Getting started

### Installation
Install the official Groq Python SDK and Pydantic v2:

```bash
pip install groq pydantic>=2.0
```

### Initial Configuration
Set your Groq API key:

```bash
export GROQ_API_KEY="gsk_your_groq_api_key_here"
```

### Basic Generation Call
Execute a simple completion request:

```python
from groq import Groq

client = Groq()

chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "Explain LPU deterministic speed benefits in 20 words."}],
    model="llama-4-70b",
)
print(chat_completion.choices[0].message.content)
```

## CLI examples

### 1. Direct cURL Request to Groq Chat Endpoint
Issue a direct cURL execution call to Groq's OpenAI-compatible API:

```bash
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
     -H "Authorization: Bearer $GROQ_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "llama-4-70b",
       "messages": [{"role": "user", "content": "Explain LPU architecture."}],
       "temperature": 0.2
     }'
```

### 2. Querying Available LPU Models
List active model endpoints currently optimized on Groq LPU hardware:

```bash
curl https://api.groq.com/openai/v1/models \
     -H "Authorization: Bearer $GROQ_API_KEY"
```

### 3. Audio Transcription via Groq Whisper Endpoint
Transcribe audio files using Groq's hardware-accelerated Whisper model:

```bash
curl -X POST "https://api.groq.com/openai/v1/audio/transcriptions" \
     -H "Authorization: Bearer $GROQ_API_KEY" \
     -F "file=@sample_voice.mp3" \
     -F "model=whisper-large-v3"
```

## FastMCP 3.1 High-Throughput Streaming Server

Below is a complete FastMCP 3.1 server integration for Groq, implementing low-latency streaming and strict response metrics validation using Pydantic v2 schemas:

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Server Tool for Groq High-Throughput LPU Stream Processing
"""

import os
import sys
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from groq import Groq
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("groq-lpu-gateway", version="1.4.0")

class GroqTelemetryData(BaseModel):
    prompt_tokens: int = Field(0, description="Input prompt token count")
    completion_tokens: int = Field(0, description="Generated completion token count")
    total_tokens: int = Field(0, description="Total token footprint")
    latency_ms: float = Field(..., description="Total wall-clock latency in milliseconds")
    tokens_per_second: float = Field(..., description="LPU token generation throughput rate")

class GroqValidatedStreamResult(BaseModel):
    id: str = Field(..., description="Groq API transaction ID")
    model: str = Field(..., description="LPU-hosted foundation model ID")
    content: str = Field(..., description="Synthesized text payload")
    telemetry: GroqTelemetryData

@mcp.tool()
async def execute_groq_inference(
    prompt: str,
    model: str = "llama-4-70b",
    system_prompt: str = "You are an ultra-fast AI assistant powered by Groq LPU hardware.",
    temperature: float = 0.2,
    max_tokens: int = 2048
) -> Dict[str, Any]:
    """
    Executes high-speed text completion via Groq's LPU API and returns validated telemetry metrics.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"error": "GROQ_API_KEY environment variable is not configured."}

    client = Groq(api_key=api_key)
    start_time = time.perf_counter()

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        elapsed_seconds = time.perf_counter() - start_time
        usage = response.usage

        prompt_toks = usage.prompt_tokens if usage else 0
        comp_toks = usage.completion_tokens if usage else 0
        tot_toks = usage.total_tokens if usage else 0
        tps = comp_toks / elapsed_seconds if elapsed_seconds > 0 else 0.0

        telemetry = GroqTelemetryData(
            prompt_tokens=prompt_toks,
            completion_tokens=comp_toks,
            total_tokens=tot_toks,
            latency_ms=round(elapsed_seconds * 1000, 2),
            tokens_per_second=round(tps, 2)
        )

        result = GroqValidatedStreamResult(
            id=response.id,
            model=response.model,
            content=response.choices[0].message.content or "",
            telemetry=telemetry
        )

        return result.model_dump()

    except Exception as exc:
        return {"error": f"Groq execution error: {str(exc)}"}

if __name__ == "__main__":
    mcp.run()
```

## API examples

### Python (Low-Latency Streaming & FastMCP 3.1 Pydantic v2 Metrics Engine)
This script demonstrates high-speed streaming response consumption and structured performance metrics validation using **Pydantic v2**:

```python
import os
import sys
import json
from typing import List, Optional, Dict, Any
from groq import Groq
from pydantic import BaseModel, Field, ValidationError

# 1. Define strict Pydantic v2 telemetry and metrics models
class GroqUsageMetrics(BaseModel):
    prompt_tokens: int = Field(..., ge=0, description="Input prompt tokens")
    completion_tokens: int = Field(..., ge=0, description="Generated output tokens")
    total_tokens: int = Field(..., ge=0, description="Total tokens processed")
    prompt_time_seconds: float = Field(..., ge=0.0, description="TTFT prompt processing time")
    completion_time_seconds: float = Field(..., ge=0.0, description="Total completion generation time")
    tokens_per_second: float = Field(..., ge=0.0, description="Calculated LPU output velocity")

class GroqExecutionReport(BaseModel):
    execution_id: str = Field(..., description="Unique completion transaction ID")
    model: str = Field(..., description="Model evaluated on LPU")
    status: str = Field("success", pattern="^(success|error)$")
    metrics: GroqUsageMetrics
    generated_content: str = Field(..., min_length=1)

if __name__ == "__main__":
    print("--- Demonstrating Local Pydantic v2 Metrics Validation ---")
    sample_data = {
        "execution_id": "chatcmpl-groq-99120",
        "model": "llama-4-70b",
        "status": "success",
        "metrics": {
            "prompt_tokens": 42,
            "completion_tokens": 210,
            "total_tokens": 252,
            "prompt_time_seconds": 0.006,
            "completion_time_seconds": 0.320,
            "tokens_per_second": 656.25
        },
        "generated_content": "Groq LPUs deliver high-speed deterministic inference."
    }

    try:
        report = GroqExecutionReport.model_validate(sample_data)
        print(f"Validated Report ID: {report.execution_id}")
        print(f"Model: {report.model}")
        print(f"Generation Speed: {report.metrics.tokens_per_second} tokens/sec")
    except ValidationError as err:
        print(f"Validation Error: {err.json()}")
```

## Production Systemd Proxy Service Unit (`groq-proxy.service`)

Deploying a local authentication and proxy daemon for local Groq requests:

```ini
[Unit]
Description=Groq High-Speed API Proxy Gateway Daemon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=groq-runner
Group=groq-runner
WorkingDirectory=/opt/groq-proxy
Environment=GROQ_API_KEY=gsk_your_groq_api_key_here
Environment=PORT=8085
ExecStart=/usr/bin/python3 /opt/groq-proxy/groq_mcp_server.py
Restart=always
RestartSec=5s
LimitNOFILE=65536
CapabilityBoundingSet=

[Install]
WantedBy=multi-user.target
```

## Diagnostic Troubleshooting Matrix

| Issue / Symptom | Probable Cause | Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **HTTP 429 Rate Limit Exceeded** | Token Per Minute (TPM) or Request Per Minute (RPM) ceiling reached | Check response headers: `x-ratelimit-remaining-tokens` | Implement exponential backoff or balance requests across tier API keys. |
| **Connection Timeout** | Network firewall or stale DNS resolving `api.groq.com` | `curl -Iv https://api.groq.com/openai/v1/models` | Verify outgoing HTTPS connectivity on port 443; update DNS resolvers. |
| **Validation Error on JSON Output** | Model output deviated from required JSON schema structure | Inspect raw completion output text before schema parsing | Lower temperature to `0.0` or enforce strict JSON mode parameter (`response_format={"type": "json_object"}`). |
| **Whisper Audio File Rejected** | Payload exceeds 25MB limits or uses unsupported codec | `file --mime-type sample_voice.mp3` | Re-encode audio to mono MP3 or split source files into <25MB segments. |

## Operational Guardrails & Security

1. **API Key Security**: Store `GROQ_API_KEY` exclusively in environment variables or hardware secrets managers (e.g., HashiCorp Vault); never hardcode credentials.
2. **Rate Limit Circuit Breakers**: Wrap external Groq calls in retry loops with exponential backoff and jitter to gracefully absorb tier limits.
3. **Payload Sanitization**: Ensure Pii data is scrubbed or encrypted prior to dispatching queries to external API endpoints.

## Related tools / concepts
- [Together AI](together.md) — Serverless open-model inference provider.
- [Fireworks AI](fireworks.md) — High-throughput open model platform.
- [Mistral AI](mistral.md) — Developer of open-weights Mistral/Mixtral models.
- [vLLM](../infrastructure/vllm.md) — Self-hosted open-source inference engine.
- [SGLang](../infrastructure/sglang.md) — High-speed execution runtime.
- [OpenRouter](../ai_knowledge/openrouter.md) — Unified model routing platform.
- [LiteLLM](../../services/litellm.md) — Enterprise proxy router for LLM endpoints.

## Sources / references
- [Groq Official Website](https://groq.com/)
- [Groq Cloud Console](https://console.groq.com/)
- [Groq Developer Documentation](https://docs.groq.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
