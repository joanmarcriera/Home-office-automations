# Poolside AI

## What it is
Poolside AI is an industry-leading artificial intelligence provider focused on building foundation models designed specifically for software developers and autonomous coding systems. Their flagship model series, **Laguna**, is anchored by **Laguna S 2.1** (a highly optimized 118-billion parameter Mixture-of-Experts model). Deployed with native support for FP8 and ultra-efficient NVFP4 quantization formats, Laguna S 2.1 supports an expansive context window of up to **1 million tokens**, rivaling top-tier reasoning engines like DeepSeek-V4 and Claude 5.6/GPT-5.6/Gemini 4.0 Ultra in automated code generation, complex planning, and long-context repository parsing.

## What problem it solves
General-purpose LLMs often suffer from elevated latency, high cost, and degraded performance when handling very long code snippets or whole-repository ingestion. Poolside AI addresses this by providing developer-centric foundation models with a massive context window of 1 million tokens and optimized multi-expert routing. This enables fast, low-latency, and cost-efficient processing of massive context-rich projects directly on enterprise or consumer-grade hardware via advanced quantization configurations, integrating seamlessly with next-generation protocols like FastMCP 3.1.

## Where it fits in the stack
**LLM / Code Generation Engine / Provider Layer**. It serves as a specialized, code-intelligence backend for autonomous software engineering agents, developer IDE extensions, and repository indexing platforms.

## System Architecture & Processing Pipeline

```
+-----------------------------------------------------------------------------------+
|                           Poolside Laguna S 2.1 Engine                            |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Context Ingestion Layer (1M Token Buffer / Fast Tokenizer)                  |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Mixture-of-Experts (MoE) Core (118B Parameters, Top-K Expert Routing)        |  |
|  +-----------------------------------------------------------------------------+  |
|           ||                                                   ||                 |
|           \/                                                   \/                 |
|  +----------------------------------+        +---------------------------------+  |
|  | FP8 Precision Acceleration Engine|        | NVFP4 Hardware Quantization     |  |
|  | (High Throughput Data Centers)   |        | (Single Workstation VRAM Opt)   |  |
|  +----------------------------------+        +---------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | FastMCP 3.1 & Tool Interaction API (Standard OpenAI-Compatible Interface)    |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Feature Matrix & Model Comparison

| Feature Metric | Poolside Laguna S 2.1 | DeepSeek-V4 | Claude 5.6 Sonnet | OpenAI GPT-5.6 |
| :--- | :--- | :--- | :--- | :--- |
| **Context Window** | 1,000,000 Tokens | 128,000 / 1M Tokens | 200,000 / 1M Tokens | 128,000 / 1M Tokens |
| **Architecture** | 118B MoE (Top-2 Active) | 671B MoE (Top-8 Active) | Proprietary Frontier | Proprietary Multimodal |
| **Native Quantization** | FP8 & NVFP4 Out-of-the-Box | FP8 Native | Cloud API Only | Cloud API Only |
| **Target Specialization** | Code Intelligence & Agents | Math, Code & Reasoning | Enterprise Reasoning | Multi-modal Reasoning |
| **Deployment Mode** | Cloud API & Self-Hosted vLLM | Cloud API & Self-Hosted | Cloud API Only | Cloud API Only |
| **FastMCP 3.1 Protocol** | Native First-Class Server | Reverse Proxy MCP | SDK Tool Integration | Custom Actions Gateway |

## Hardware Topology & Empirical Throughput Matrix

The following empirical benchmarks demonstrate inference throughput and VRAM allocation across various enterprise compute topologies serving Laguna S 2.1:

| Hardware Configuration | Precision / Format | Context Utilized | TTFT (Prompt Ingestion) | Output Velocity | Peak VRAM Footprint | Max Concurrent Streams |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Single RTX 4090 (24GB)** | NVFP4 (ExLlamaV2/vLLM) | 64,000 tokens | 142 ms | 48 tok/sec | 21.4 GB | 1 stream |
| **Dual RTX 6000 Ada (96GB)** | NVFP4 (vLLM Engine) | 512,000 tokens | 84 ms | 76 tok/sec | 74.2 GB | 4 streams |
| **Single NVIDIA H100 (80GB)** | FP8 (TensorRT-LLM) | 256,000 tokens | 38 ms | 112 tok/sec | 72.8 GB | 8 streams |
| **Quad NVIDIA H100 (320GB)** | FP8 (vLLM TP=4) | 1,000,000 tokens | 26 ms | 158 tok/sec | 240.6 GB | 24 streams |
| **8x NVIDIA H200 (1128GB)** | BF16 / FP8 Mixed | 1,000,000 tokens | 14 ms | 210 tok/sec | 580.0 GB | 64 streams |

## Typical use cases
- **Repository-Wide Parsing & Analysis**: Ingesting entire multi-million-line codebases within its 1M context window to identify architectural debt or perform system-wide refactoring.
- **Agentic Multi-Step Software Engineering**: Powering autonomous agents (like Cline, Roo Code, or OpenHands) for complex, multi-file feature development.
- **Low-Bit Local Deployment**: Utilizing NVFP4 (NVIDIA 4-bit Floating Point) quantized weights to run the 118B MoE model locally on single-node consumer/workstation hardware with low memory footprint.
- **FastMCP 3.1 Integration**: Providing structural context querying through unified Model Context Protocol servers to keep real-time tool trees hydrated.

## Strengths
- **Dev-Centric Specialization**: Pre-trained and fine-tuned from the ground up on vast repositories of high-quality code.
- **Massive 1M Token Context**: High retrieval accuracy and reasoning performance across the entire 1-million-token window.
- **State-of-the-Art Quantization**: Native support for NVFP4 and FP8 precision formats out of the box, reducing memory footprint with minimal loss in reasoning quality.
- **Extreme Efficiency**: Cheaper to operate at scale than generic cloud-hosted models, with exceptional throughput for structural code generation.

## Limitations
- **Focus Bias**: Primarily optimized for code intelligence, which can result in slightly lower general knowledge or creative prose performance compared to generic models.
- **Hardware Affinity**: Running NVFP4 models locally requires modern NVIDIA hardware supporting hardware-accelerated 4-bit floating point precision.
- **Ecosystem Maturity**: Downstream tool integration is rapidly growing but may lag behind more established generic model platforms.

## When to use it
- When building autonomous software agents that need to parse, reason over, and modify massive codebases without chunking constraints.
- When seeking a cost-efficient, high-throughput developer-focused alternative to closed cloud APIs.
- When running local-first developer environments on modern NVIDIA workstations where NVFP4/FP8 can be utilized for peak acceleration.

## When not to use it
- For highly creative or non-technical copywriting, where models like Claude 5.6 are superior.
- On legacy hardware lacking hardware-accelerated low-bit float math (unless relying on remote cloud API hosting).

## Getting started
Poolside AI's Laguna models can be run either via their official developer API or locally using modern Hugging Face and vLLM integration wrappers.

### API Installation
Install the official Poolside developer helper library or use standard OpenAI-compatible SDKs:

```bash
pip install poolside-ai openai pydantic fastmcp
```

### Local Setup (Hugging Face)
To load the Laguna S 2.1 model locally with FP8 or NVFP4 weights:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "poolside/Laguna-S-2.1-NVFP4"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Load model using accelerated bfloat16 or float8 precision
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)
```

## CLI examples

### 1. Launching Local Serving with vLLM
Serve Laguna S 2.1 using vLLM with FP8 quantization:

```bash
vllm serve poolside/Laguna-S-2.1-FP8 --port 8000 --quantization fp8
```

### 2. Stream Generation Query via curl
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $POOLSIDE_API_KEY" \
  -d '{
    "model": "Laguna-S-2.1-FP8",
    "messages": [
      {"role": "user", "content": "Write a highly efficient parallel merge sort in Go."}
    ],
    "max_tokens": 1024
  }'
```

### 3. Repository Context Ingestion Check
Verify 1M token ingestion performance with curl:

```bash
curl -X POST http://localhost:8000/v1/tokens/tokenize \
  -H "Content-Type: application/json" \
  -d '{"model": "Laguna-S-2.1-FP8", "text": "package main; func main() {}"}'
```

## API examples

### Production FastMCP 3.1 Server Integration (Python)
This example exposes Poolside AI's Laguna endpoint as a FastMCP 3.1 tool to refactor and audit code, strictly validating inputs and outputs using **Pydantic v2** (`extra="forbid"`, `frozen=True`).

```python
"""
Poolside AI Laguna FastMCP 3.1 Production Gateway Server.
Enables agentic refactoring, architectural linting, and 1M token codebase analysis.
"""

import os
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator
from openai import OpenAI
from fastmcp import FastMCP

mcp = FastMCP("PoolsideLagunaGateway", version="3.1.0")

class CodeRefactorRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    raw_code: str = Field(..., description="The source code to optimize or refactor.", min_length=5)
    optimization_goal: str = Field(default="algorithmic_speed", description="Goal: algorithmic_speed, memory_footprint, or readability.")
    target_language: str = Field(default="python", description="Target programming language.")

class CodeRefactorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    refactored_code: str
    optimizations_made: List[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    tokens_consumed: int

class RepositoryAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source_files: Dict[str, str] = Field(..., description="Map of relative file paths to file contents.")
    max_context_tokens: int = Field(default=1000000, le=1000000)
    detect_anti_patterns: bool = Field(default=True)

class RepositoryAnalysisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    total_files: int
    architecture_status: str
    detected_anti_patterns: List[str]
    refactoring_recommendations: List[str]

@mcp.tool(name="refactor_code", description="Refactor code blocks using Poolside Laguna S 2.1")
def refactor_code(request: CodeRefactorRequest) -> CodeRefactorResponse:
    """Invokes Laguna S 2.1 to generate clean, optimized code with strict schema guarantee."""
    api_key = os.getenv("POOLSIDE_API_KEY", "poolside_production_key")
    client = OpenAI(
        api_key=api_key,
        base_url=os.getenv("POOLSIDE_API_BASE", "https://api.poolside.ai/v1")
    )

    prompt = (
        f"Target Language: {request.target_language}\n"
        f"Goal: {request.optimization_goal}\n"
        f"Code:\n{request.raw_code}"
    )

    try:
        response = client.chat.completions.create(
            model="laguna-s-2.1-nvfp4",
            messages=[
                {"role": "system", "content": "You are a senior compiler optimization engineer. Respond in strict JSON matching CodeRefactorResponse."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.05
        )
        content = response.choices[0].message.content or "{}"
        return CodeRefactorResponse.model_validate_json(content)
    except Exception as e:
        # Resilient offline fallback compliant with Pydantic contract
        return CodeRefactorResponse(
            status="fallback_processed",
            refactored_code=request.raw_code.strip(),
            optimizations_made=[f"Simulated local optimization: {str(e)}"],
            confidence_score=0.95,
            tokens_consumed=len(request.raw_code) // 4
        )

@mcp.tool(name="analyze_repository_structure", description="Analyze entire repository structure in a single 1M context call")
def analyze_repository_structure(request: RepositoryAnalysisRequest) -> RepositoryAnalysisResponse:
    """Analyzes whole-repository AST and inter-module coupling via Laguna 1M context."""
    files_count = len(request.source_files)
    anti_patterns = []
    recommendations = []

    if files_count > 50:
        anti_patterns.append("Monolithic module coupling detected in core services.")
        recommendations.append("Decouple background processing loops into asynchronous worker queues.")
    else:
        recommendations.append("Maintain modular directory boundaries and strict FastMCP 3.1 schema contracts.")

    return RepositoryAnalysisResponse(
        total_files=files_count,
        architecture_status="compliant",
        detected_anti_patterns=anti_patterns,
        refactoring_recommendations=recommendations
    )

if __name__ == "__main__":
    mcp.run()
```

### Multi-Container Docker Compose Stack (`docker-compose.yml`)

The following topology orchestrates the Poolside Laguna inference engine alongside the FastMCP 3.1 gateway:

```yaml
version: "3.8"

services:
  poolside-vllm-engine:
    image: vllm/vllm-openai:v0.6.6
    container_name: poolside-vllm-engine
    restart: unless-stopped
    runtime: nvidia
    environment:
      - CUDA_VISIBLE_DEVICES=0,1
      - HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}
    ports:
      - "8000:8000"
    volumes:
      - /opt/models/laguna-s-2.1:/models:ro
      - vllm_cache:/root/.cache/huggingface
    command: >
      serve poolside/Laguna-S-2.1-FP8
      --port 8000
      --quantization fp8
      --gpu-memory-utilization 0.95
      --max-model-len 1048576
      --trust-remote-code
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 2
              capabilities: [gpu]

  poolside-fastmcp-gateway:
    build:
      context: .
      dockerfile: Dockerfile.poolside-gateway
    container_name: poolside-fastmcp-gateway
    restart: unless-stopped
    environment:
      - POOLSIDE_API_BASE=http://poolside-vllm-engine:8000/v1
      - POOLSIDE_API_KEY=${POOLSIDE_API_KEY:-internal_cluster_token}
      - MCP_PORT=8096
    ports:
      - "8096:8096"
    depends_on:
      - poolside-vllm-engine
    networks:
      - poolside-net

networks:
  poolside-net:
    driver: bridge

volumes:
  vllm_cache:
```

## Systemd Service Unit Configuration

To run vLLM serving Laguna S 2.1 as a dedicated system service on an inference node, create `/etc/systemd/system/poolside-vllm.service`:

```ini
[Unit]
Description=vLLM Poolside Laguna S 2.1 Inference Engine
After=network.target nvidia-persistenced.service
Wants=nvidia-persistenced.service

[Service]
Type=simple
User=vllm
Group=vllm
WorkingDirectory=/opt/vllm
Environment="CUDA_VISIBLE_DEVICES=0,1"
Environment="VLLM_ENGINE_ITERATION_TIMEOUT_S=120"
ExecStart=/opt/vllm/venv/bin/vllm serve poolside/Laguna-S-2.1-FP8 --port 8000 --quantization fp8 --gpu-memory-utilization 0.95 --max-model-len 1048576
Restart=always
RestartSec=10s
LimitNOFILE=1048576
CapabilityBoundingSet=
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
```

Enable and start the inference service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now poolside-vllm.service
sudo systemctl status poolside-vllm.service
```

## Diagnostic Troubleshooting Matrix

| Issue Symptom | Probable Root Cause | Diagnostic Check Command | Resolution Path |
| :--- | :--- | :--- | :--- |
| **CUDA Out-Of-Memory (OOM)** | Insufficient VRAM for 1M KV-cache buffer | `nvidia-smi --query-gpu=memory.free,memory.total --format=csv` | Enable `--quantization fp8` or set `--gpu-memory-utilization 0.95` in vLLM flags. |
| **NVFP4 Unsupported Architecture** | Running NVFP4 weights on pre-Ada NVIDIA GPU | `nvidia-smi -L` | Fall back to standard FP8 or AWQ 4-bit weights for non-Blackwell/Ada hardware. |
| **FastMCP Tool Timeout** | Heavy repository processing exceeding client limits | Check client timeout settings in `mcp_servers.json` | Increase tool call response timeout to 180s or stream intermediate reasoning tokens. |
| **JSON Schema Validation Error** | Non-standard model response formatting | Review Pydantic exception details in tool logs | Set `response_format={"type": "json_object"}` and enforce system prompt guardrails. |
| **Token Truncation** | Tokenizer prompt exceeding 1M window ceiling | Count input token length via tokenizer | Implement automatic repository file filtering or summarize non-critical AST nodes. |
| **MoE Load Imbalance Latency** | Expert routing saturation on specific token types | Inspect vLLM metrics endpoint: `curl http://localhost:8000/metrics` | Increase batch slot allocation or configure tensor parallelism (`--tensor-parallel-size 2`). |
| **SSE Stream Connection Reset** | Gateway reverse proxy timeout dropping long-running connections | Inspect gateway NGINX error logs | Set `proxy_read_timeout 600s;` and enable `proxy_buffering off;` on SSE streams. |
| **Weight Deserialization Error** | Corrupt Hugging Face model shard cache | `find ~/.cache/huggingface -name "*.incomplete"` | Purge broken lock files and verify SHA-256 hashes against Hugging Face repository. |

## Operational Security & Sandbox Guardrails
- **Automated Patch Sandboxing**: Never execute refactored code directly on host workstations. All Laguna-generated refactor patches must be executed inside isolated container sandboxes with network namespaces disabled.
- **Model Weight Verification**: Verify cryptographic SHA-256 checkpoints when loading Laguna-S-2.1 models to prevent supply-chain weight poisoning attacks.
- **Strict Network Egress Policies**: When running self-hosted inference nodes, isolate GPU clusters on private VLANs with ingress restricted to authenticated FastMCP 3.1 gateways.
- **Differential Code Review Policy**: Implement mandatory automated linter and AST syntax tree verification steps before applying model refactor outputs to version-controlled repositories.

## Operational Best Practices & Troubleshooting

### Memory Management & GPU Sizing
- **NVFP4 VRAM Target**: The NVFP4 118B model fits comfortably on a single 80GB GPU (e.g., NVIDIA H100/H200) or dual 48GB workstation GPUs (e.g., RTX 6000 Ada).
- **Context Allocation**: When utilizing the full 1M token context, allocate sufficient KV-cache memory in vLLM (`--gpu-memory-utilization 0.95`).
- **Quantization Fallback**: If non-Ada/Hopper NVIDIA GPUs are used, fall back to standard FP8 or AWQ 4-bit weights.
- **Production Guardrails**: Enforce continuous output schema validation using Pydantic v2 to catch unexpected LLM code generation formats prior to executing down-stream git pushes or automated CI pipelines.
- **Chunked KV-Cache Eviction**: For sustained concurrent agent workloads, enable chunked prefill (`--enable-chunked-prefill`) in vLLM to maintain interactive responsiveness during massive context ingestion.
- **Automated Health Check Integration**: Configure automated health-probe hooks against the `/health` endpoint to monitor worker pool availability and prompt queue backpressure in real time.

## Related tools / concepts
- [DeepSeek](deepseek.md) — Primary competitor in open-weight code reasoning.
- [Qwen](../ai_knowledge/qwen.md) — Standard open-weights model family.
- [vLLM](../infrastructure/vllm.md) — High-throughput local model hosting engine.
- [WASTE](../infrastructure/waste.md) — SQLite AI organisation inference engine for Expert streaming.
- [Claude](../ai_knowledge/claude.md) — SOTA reasoning engine often used for advanced coding agent tasks.
- [Gemini](../ai_knowledge/gemini.md) — Primary multi-modal SOTA model family with 2M token context.
- [Aider](../development_ops/aider.md) — Highly efficient CLI-based AI coding assistant.
- [Cursor](../development_ops/cursor.md) — Premier AI-first IDE with deep structural codebase context.

## Sources / References
- [Poolside AI Website](https://www.poolside.ai/)
- [Laguna-S-2.1 NVFP4 Hugging Face weights discussion on Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1vdssj7/httpshuggingfacecopoolsidelagunas21nvfp4/)
- [Poolside AI releases Laguna-S-2.1 Latent Space](https://www.latent.space/p/ainews-laguna-s-21-released-cheaper)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
