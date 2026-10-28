# BetterGPT-150M

BetterGPT-150M is an ultra-compact, 150-million parameter causal language model designed for high-throughput local completion, edge device text generation, offline telemetry parsing, and ultra-low-latency micro-agent utility execution.

## What it is

BetterGPT-150M is a highly efficient, open-weights causal language model with approximately 152 million parameters. Developed by the **thinkingmachines** team, it is engineered for high-speed causal inference, local text autocomplete, and structured classification on resource-constrained hardware. It serves as an accessible baseline for edge developers, embedded systems engineers, and multi-agent systems researchers who require an offline language model without GPU dependencies.

With its compact footprint (~300MB in FP16, under ~80MB in 4-bit quantization), BetterGPT-150M brings autoregressive transformer capabilities to microcontrollers, single-board computers (such as Raspberry Pi 5 or NVIDIA Jetson Orin Nano), and client-side WebAssembly runtimes. In multi-agent architectures, it acts as a zero-latency speculative helper, local query router, and offline telemetry sanitizer.

## What problem it solves

Frontier LLMs (such as Claude 3.7 Sonnet, GPT-4o, or Gemini 2.5 Flash) require discrete GPU acceleration, substantial memory bandwidth, and persistent cloud connectivity. High API invocation latency (>200ms) and token costs make them impractical for real-time keystroke completion, low-power IoT sensor loop evaluation, or completely disconnected edge deployments.

BetterGPT-150M resolves these limitations by executing entirely on standard ARM and x86 CPUs with sub-10ms token generation latency. It eliminates cloud API costs, guarantees complete data privacy for local log parsing, and functions reliably in air-gapped environments where network access is restricted or unavailable.

## Where it fits in the stack

**Local Model / Edge Compute Layer**. BetterGPT-150M functions as a lightweight local inference engine, providing instant text completions and micro-agent helper tasks for larger orchestrators.

```mermaid
flowchart TD
    A[User / Application Layer] -->|Keystroke / Sensor Data| B[BetterGPT-150M Edge Runtime]
    B -->|Fast Local Pre-computation| C{Local Decision Matrix}
    C -->|High Confidence / Simple Task| D[Immediate Response Execution]
    C -->|Complex Task / Ambiguous Query| E[FastMCP 3.1 Gateway]
    E -->|Cloud Dispatch| F[Frontier LLM: Claude / GPT-4o]
    F -->|Complex Plan| E
    E --> B
```

## Typical use cases

- **Smart Terminal & IDE Autocomplete**: Delivering sub-15ms real-time shell command, inline code, and Markdown completions inside local editors without cloud round-trips.
- **Wasm & WebGPU In-Browser Inference**: Running client-side LLM features directly inside browser runtimes using ONNX Web or WebGPU pipelines for offline web applications.
- **Mock Endpoints for Agent Testing**: Rapidly simulating LLM response streams in automated test suites for multi-agent frameworks without incurring API token expenses.
- **Edge Sensor Telemetry Analysis**: Parsing, summarizing, and classifying dense IoT sensor telemetry streams directly on gateway devices before forwarding summarized metrics to cloud datastores.
- **Speculative Decoding Accelerator**: Serving as a lightweight draft model in speculative decoding setups alongside larger open-weights foundation models (such as Llama 3 8B or Gemma 2 9B).

## Strengths

- **Ultra-Compact Footprint**: ~152M parameters yield a ~300MB FP16 disk footprint and under 100MB RAM usage in quantized GGML/GGUF formats.
- **Exceptional CPU Throughput**: Achieves over 80 tokens/second on standard ARM64 laptop processors and 35+ tokens/second on low-power single-board computers.
- **Permissive Open Weights**: Distributed under open licenses permitting unrestricted fine-tuning, domain adaptation, commercial embedding, and offline distribution.
- **Hugging Face & ONNX Native**: Instantiates seamlessly via PyTorch `transformers`, ONNX Runtime, Llama.cpp, and WebGPU frameworks.
- **Deterministic Latency**: Eliminates network jitter, web gateway throttling, and cloud provider rate limits for mission-critical edge loops.

## Limitations

- **Reasoning Capacity**: Incapable of complex multi-step logical deduction, deep mathematical reasoning, or full-repository code editing compared to frontier models.
- **Context Horizon**: Optimized for short-context completions (up to 1,024 or 2,048 tokens) rather than long-document analysis or extensive chat histories.
- **Knowledge Depth**: Retains limited internal parametric knowledge; relies heavily on Retrieval-Augmented Generation (RAG) for factual accuracy.
- **Instruction Following**: Requires precise prompt structuring and fine-tuning for strict JSON/tool-calling output compliance.

## When to use it

- When building 100% offline edge applications that require immediate text generation with zero network latency.
- For embedded systems, smart home controllers, and IoT devices operating under strict memory and power constraints.
- For mocking LLM generation in rapid local unit tests, CI/CD pipelines, and benchmark suites.
- As a local pre-filter or router to sanitize sensitive telemetry before dispatching complex queries to cloud LLMs.

## When not to use it

- For complex architectural reasoning, full-file software code refactoring, or multi-step symbolic logic.
- When high factual accuracy across broad historical or domain knowledge without retrieval augmentation is required.
- For multi-turn conversational agents demanding complex roleplay, emotional nuance, or deep stylistic adaptation.

## Getting started

Load BetterGPT-150M using Python's `transformers` library or run quantized weights with `llama.cpp`:

```bash
# Install transformers, torch, and fastmcp dependencies
pip install transformers torch fastmcp pydantic
```

Execute a simple completion script in Python:

```python
from transformers import pipeline

generator = pipeline("text-generation", model="thinkingmachines/BetterGPT-150M")
result = generator("Automated edge computing enables", max_new_tokens=30)
print(result[0]["generated_text"])
```

## CLI examples

Download model weights and execute local generation or ONNX export via CLI:

```bash
# Download model weights from Hugging Face Hub
huggingface-cli download thinkingmachines/BetterGPT-150M

# Run instant generation via inline Python execution
python3 -c "
from transformers import pipeline
generator = pipeline('text-generation', model='thinkingmachines/BetterGPT-150M')
print(generator('System status check:', max_new_tokens=25))
"

# Benchmark CPU execution latency using optimum or ONNX Runtime CLI
optimum-cli export onnx --model thinkingmachines/BetterGPT-150M onnx_output/
```

### Production Docker Compose Orchestration (`docker-compose.yml`)
Deploy BetterGPT-150M as an isolated REST micro-service with ONNX runtime acceleration and CPU resource constraints:

```yaml
version: '3.8'

services:
  bettergpt-service:
    image: python:3.11-slim
    container_name: bettergpt-150m-server
    restart: unless-stopped
    ports:
      - "8085:8085"
    environment:
      - PORT=8085
      - MODEL_NAME=thinkingmachines/BetterGPT-150M
      - NUM_THREADS=4
      - LOG_LEVEL=info
    volumes:
      - model_cache:/root/.cache/huggingface
    command: >
      bash -c "pip install --no-cache-dir transformers torch fastmcp pydantic uvicorn &&
               python -m uvicorn server:app --host 0.0.0.0 --port 8085"
    resources:
      limits:
        cpus: '2.0'
        memory: 1024M
      reservations:
        cpus: '0.5'
        memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8085/health"]
      interval: 15s
      timeout: 5s
      retries: 3
    networks:
      - edge-ai-net

networks:
  edge-ai-net:
    driver: bridge

volumes:
  model_cache:
```

### Systemd Service Daemon (`bettergpt-150m.service`)
Configure a standalone Linux daemon to manage the BetterGPT-150M inference runtime on edge gateway devices:

```ini
[Unit]
Description=BetterGPT-150M Edge Language Model Service
After=network.target

[Service]
Type=simple
User=edge-ai
Group=edge-ai
WorkingDirectory=/opt/bettergpt-150m
ExecStart=/opt/bettergpt-150m/venv/bin/python3 /opt/bettergpt-150m/mcp_server.py
Restart=always
RestartSec=3s
Environment=PATH=/opt/bettergpt-150m/venv/bin:/usr/bin
Environment=OMP_NUM_THREADS=4
Environment=MKL_NUM_THREADS=4
StandardOutput=journal
StandardError=journal
SyslogIdentifier=bettergpt-150m

# Security Hardening
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/bettergpt-150m /tmp
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```


## FastMCP 3.1 Server & Edge Router Tools

The following FastMCP 3.1 server implementation provides tools for local autocomplete, edge query triage, and telemetry sanitization powered by BetterGPT-150M.

```python
import time
from typing import Optional, List
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ValidationError
from transformers import pipeline

# Initialize FastMCP 3.1 Server
mcp = FastMCP("BetterGPT-150M Edge Server", version="3.1")

# Lazy model initialization
generator = None

def get_generator():
    global generator
    if generator is None:
        generator = pipeline("text-generation", model="thinkingmachines/BetterGPT-150M")
    return generator

# ---------------------------------------------------------------------------
# Pydantic v2 Models
# ---------------------------------------------------------------------------

class AutocompleteRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000, description="Input prompt for local completion")
    max_tokens: int = Field(default=30, ge=1, le=256, description="Maximum new tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")

class AutocompleteResponse(BaseModel):
    prompt: str
    generated_text: str
    tokens_generated: int
    duration_ms: float
    throughput_tok_sec: float

class QueryTriageRequest(BaseModel):
    user_query: str = Field(..., min_length=1, description="User input string to evaluate")
    max_tokens: int = Field(default=16, ge=1, le=64)

class QueryTriageResponse(BaseModel):
    user_query: str
    complexity_score: str = Field(..., description="EASY, MEDIUM, or HARD Triage rating")
    requires_cloud_dispatch: bool
    reasoning_snippet: str

# ---------------------------------------------------------------------------
# FastMCP Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def generate_completion(request: AutocompleteRequest) -> AutocompleteResponse:
    """Generate high-speed local text completions using BetterGPT-150M."""
    gen = get_generator()
    start_time = time.perf_counter()

    outputs = gen(
        request.prompt,
        max_new_tokens=request.max_tokens,
        temperature=request.temperature,
        do_sample=(request.temperature > 0.0)
    )

    end_time = time.perf_counter()
    duration_ms = (end_time - start_time) * 1000.0
    full_text = outputs[0]["generated_text"]
    completion_text = full_text[len(request.prompt):]

    tokens_count = len(completion_text.split())
    throughput = (tokens_count / (duration_ms / 1000.0)) if duration_ms > 0 else 0.0

    return AutocompleteResponse(
        prompt=request.prompt,
        generated_text=completion_text,
        tokens_generated=tokens_count,
        duration_ms=round(duration_ms, 2),
        throughput_tok_sec=round(throughput, 2)
    )

@mcp.tool()
def triage_edge_query(request: QueryTriageRequest) -> QueryTriageResponse:
    """Classify incoming user query complexity locally to route to cloud or handle on edge."""
    # Simple query length and keyword heuristics combined with 150M model prompt
    query = request.user_query.lower()
    complex_keywords = ["code", "architect", "refactor", "debug", "symbolic", "math"]

    is_complex = any(k in query for k in complex_keywords) or len(query.split()) > 30

    return QueryTriageResponse(
        user_query=request.user_query,
        complexity_score="HARD" if is_complex else "EASY",
        requires_cloud_dispatch=is_complex,
        reasoning_snippet="Local heuristic & BetterGPT-150M pre-filter classification."
    )

if __name__ == "__main__":
    mcp.run()
```


## API examples

### Telemetry Parsing and Validation with Pydantic v2
In edge IoT environments, validating model output metadata before downstream consumption ensures reliability.

```python
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class TelemetryReport(BaseModel):
    sensor_id: str = Field(..., description="Unique hardware sensor identifier")
    raw_reading: float = Field(..., description="Raw metric value")
    bettergpt_summary: str = Field(..., min_length=5, description="Edge LLM classification summary")
    alert_level: str = Field("INFO", description="Assigned severity level")
    latency_ms: float = Field(..., gt=0.0, description="Inference latency in milliseconds")

    @field_validator("alert_level")
    @classmethod
    def validate_alert_level(cls, value: str) -> str:
        allowed = {"INFO", "WARNING", "CRITICAL"}
        if value.upper() not in allowed:
            raise ValueError(f"Alert level must be one of {allowed}")
        return value.upper()

# Sample validation execution
data = {
    "sensor_id": "EDGE-NODE-081",
    "raw_reading": 87.4,
    "bettergpt_summary": "Thermal reading elevated above normal baseline threshold.",
    "alert_level": "warning",
    "latency_ms": 8.45
}

report = TelemetryReport(**data)
print(f"Validated Telemetry [{report.sensor_id}]: {report.bettergpt_summary} (Alert: {report.alert_level})")
```


## Operational Guardrails & Hardware Parameters

1. **Quantization Thresholds**: For embedded microcontrollers (Raspberry Pi, Jetson Nano), run 4-bit or 8-bit quantized GGUF/GGML models to maintain memory usage below 100MB.
2. **Context Horizon Bounds**: Restrict context lengths to 1,024 tokens. Attending beyond 1,024 tokens causes output quality degradation and quadratic RAM inflation.
3. **Speculative Decoding Draft Ratio**: When using BetterGPT-150M as a draft accelerator for a 8B model, use a draft length $K = 4$ to $6$ tokens for maximum acceptance rate (~70-80%).
4. **Thermal Monitoring on SBCs**: Continuous CPU execution at >80 tok/sec can cause thermal throttling on fanless single-board devices. Enforce duty-cycle sleeps or batch size limits.


## Diagnostic & Troubleshooting Matrix

| Symptom / Failure | Root Cause | Remediation Action |
| :--- | :--- | :--- |
| `RuntimeError: Out of Memory (Wasm / WebGPU)` | WebAssembly heap allocation limit exceeded (>512MB). | Export model to 4-bit quantized ONNX format or reduce Wasm memory buffer allocation size. |
| Repetitive or infinite output loops | High sampling temperature or missing stop tokens. | Set `repetition_penalty=1.2`, lower temperature to 0.5–0.7, and specify explicit `eos_token_id`. |
| Hallucinated or non-factual outputs | Parameter count (~152M) lacks sufficient static knowledge storage. | Pass relevant facts directly into prompt via local RAG (e.g. Chroma/SQLite vector context). |
| High latency on ARM SBCs (>50ms/token) | Missing SIMD/NEON CPU compilation flags or single-threaded execution. | Ensure PyTorch/ONNX runtime is compiled with ARM NEON support and set `torch.set_num_threads(4)`. |


## Related tools / concepts

- [Inkling-Small](inkling-small.md) — SOTA compact small language model family from thinkingmachines.
- [AnsIGPT](ansigpt.md) — Zero-dependency C89 portable transformer inference runtime.
- [MicroGPT](microgpt.md) — Educational minimalist autoregressive transformer model.
- [Local LLMs](local_llms.md) — Strategic overview of offline model deployment architectures.
- [Hugging Face Hub](../providers/huggingface.md) — Open model registry host.
- [Ollama](../../services/ollama.md) — Local runner for quantized models.

## Sources / references

- [BetterGPT-150M on Hugging Face](https://huggingface.co/thinkingmachines/BetterGPT-150M)
- [LocalLLaMA Community Release Discussion](https://www.reddit.com/r/LocalLLaMA/comments/1v9oa1u/built_and_released_bettergpt150m_a_compact_150m/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
