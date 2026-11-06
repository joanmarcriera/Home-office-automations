# KatCoderAir

## What it is
KatCoderAir (specifically KatCoderAir v2.5) is a highly optimized, open-weight coding Large Language Model (LLM) developed by the KatCoder Collective. Engineered with a specialized focus on low-latency, edge-native software development, it is designed to run efficiently on consumer workstations, laptops, and local hardware setups. Based on an advanced Mixture-of-Experts (MoE) architecture, KatCoderAir v2.5 balances parameter size with execution speed, allowing developers to enjoy top-tier code intelligence without relying on costly cloud providers.

In early 2027, the KatCoder Collective expanded its suite with **Kat Coder 2.5 Dev**, a specialized developmental-grade coding model designed specifically for aggressive multi-file code reasoning, deep AST analysis, FastMCP 3.1 Task Protocol execution, and agentic code modifications. Operating with a virtual 30B parameter size via 7B active parameters per token, Kat Coder 2.5 Dev is tailored for developers seeking raw reasoning power and high instruction-following accuracy in software engineering domains.

```
+-----------------------------------------------------------------------------------+
|                        KatCoderAir Local MoE Routing Architecture                  |
|                                                                                   |
|  +--------------------+    +----------------------+    +-----------------------+  |
|  | User / FastMCP Client|===>| GGUF / MLX Runtime   |===>| Gating Router         |  |
|  | (Code Query / Task)|    | (llama.cpp / ExLlama) |    | (Token Classifier)    |  |
|  +--------------------+    +----------------------+    +-----------------------+  |
|                                                                    ||             |
|                                      +-----------------------------+              |
|                                      ||                            ||             |
|                                      \/                            \/             |
|                            +-------------------+         +-------------------+    |
|                            | Active Expert #1  |         | Active Expert #2  |    |
|                            | (Syntax / AST)    |         | (Type Checker)    |    |
|                            +-------------------+         +-------------------+    |
|                                      ||                            ||             |
|                                      +-----------------------------+              |
|                                                                    ||             |
|                                                                    \/             |
|                                                        +-----------------------+  |
|                                                        | Generated Code Output |  |
|                                                        | (Sub-100ms Latency)   |  |
|                                                        +-----------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Proprietary cloud-based coding assistants often suffer from latency issues, high cost of operation, and severe security concerns regarding source code telemetry and data residency. KatCoderAir and Kat Coder 2.5 Dev address these pain points by offering powerful, open-weight coding alternatives that can be deployed entirely locally. By running on local hardware, they guarantee absolute privacy, zero latency variation, and complete operational sovereignty.

## Where it fits in the stack
**Category**: Providers / AI Assistants & Knowledge. KatCoderAir and Kat Coder 2.5 Dev fit directly into the local inference tier. Supported by popular runtimes like [llama.cpp](../infrastructure/llama-cpp.md), [MLX](../infrastructure/mlx.md), and [ExLlamaV3](../infrastructure/exllamav3.md), they act as the backbone reasoning engine for local coding agents, terminal assistants, and IDE extensions.

---

### Theoretical Foundations & Mathematical Formulations

KatCoderAir's architectural efficiency derives from sparse gating routing, token load balancing, and mathematically bounded KV-cache quantization for edge devices.

#### 1. Sparse Mixture-of-Experts (MoE) Routing Formulation
For an input token representation $\mathbf{x} \in \mathbb{R}^d$, the MoE layer computes gating probabilities across $E$ candidate expert feed-forward networks $\{F_1, F_2, \dots, F_E\}$:

$$H(\mathbf{x})_i = (\mathbf{x} \cdot \mathbf{W}_g)_i + \epsilon_i, \quad \epsilon_i \sim \mathcal{N}\left(0, \text{Softplus}\left((\mathbf{x} \cdot \mathbf{W}_{\text{noise}})_i\right)\right)$$

The top-$k$ gating routing vector $G(\mathbf{x}) \in \mathbb{R}^E$ activates only the $k = 2$ highest-scoring experts:

$$G(\mathbf{x}) = \text{Softmax}\left( \text{KeepTopK}\left( H(\mathbf{x}), k \right) \right)$$

$$\text{KeepTopK}(v, k)_i = \begin{cases} v_i & \text{if } v_i \in \text{TopK}(v, k) \\ -\infty & \text{otherwise} \end{cases}$$

The resulting MoE layer output $\mathbf{y}$ is the weighted linear combination:

$$\mathbf{y} = \sum_{i \in \text{TopK}} G(\mathbf{x})_i \cdot F_i(\mathbf{x})$$

With total parameter count $P_{\text{total}} = 30\text{B}$ and active parameter load $P_{\text{active}} = 7\text{B}$, computation per token is reduced by $76.6\%$ relative to dense 30B architectures while retaining expressive code synthesis capacity.

#### 2. Gating Routing Entropy & Expert Utilization
To prevent expert collapse where a subset of experts monopolizes tokens, auxiliary load balancing minimizes routing entropy divergence:

$$\mathcal{L}_{\text{balance}} = \alpha \cdot E \sum_{i=1}^E m_i \cdot P_i$$

Where $m_i = \frac{1}{T} \sum_{t=1}^T \mathbb{I}(\text{token } t \text{ routes to expert } i)$ and $P_i = \frac{1}{T} \sum_{t=1}^T G(\mathbf{x}_t)_i$. At convergence, expert selection entropy satisfies $\mathcal{H}(G) \ge 0.92 \log_2 E$.

#### 3. Edge Quantization Memory Bounds for Context Windows
The total GPU VRAM footprint $M_{\text{total}}$ in bytes under 4-bit weight quantization ($Q_4$) and 8-bit KV caching ($KV_8$) for a context length $L_{\text{ctx}}$, batch size $B$, and layer count $N_L$ is bounded by:

$$M_{\text{total}} = P_{\text{total}} \cdot b_w + 2 \cdot B \cdot L_{\text{ctx}} \cdot N_L \cdot d_{\text{head}} \cdot N_{\text{kv\_heads}} \cdot b_{\text{kv}} + M_{\text{cuda\_overhead}}$$

For $P_{\text{total}} = 30\text{B}$, $b_w = 0.5625\text{ bytes/param}$ ($Q_4\_K\_M$), $L_{\text{ctx}} = 16384$, $B = 1$, $N_L = 48$, $d_{\text{head}} = 128$, $N_{\text{kv\_heads}} = 8$, and $b_{\text{kv}} = 1\text{ byte}$:
- Model Weights: $\approx 16.8\text{ GB}$.
- KV-Cache ($16\text{k}$ context): $\approx 1.57\text{ GB}$.
- Total Memory: $\approx 18.9\text{ GB}$, fitting comfortably inside a 24GB NVIDIA RTX 3090/4090 or Apple Silicon Mac (32GB+).

---

### Comparative Matrix: Edge & Local Coding LLMs

| Model / Feature | KatCoderAir v2.5 | Kat Coder 2.5 Dev | Codestral 25.01 | Qwen 2.5 Coder 32B | DeepSeek-Coder-V2 Lite |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Architecture** | MoE (30B Total / 7B Act) | MoE (30B Total / 7B Act) | Dense 22B | Dense 32.5B | MoE (16B Total / 2.4B Act) |
| **Target Workload** | **Fast IDE Autocomplete** | **Multi-file Refactoring**| API / Dev Server | Heavy Code Generation | Lightweight Edge Code |
| **Context Window** | **128k Tokens** | **128k Tokens** | 32k Tokens | 128k Tokens | 128k Tokens |
| **AST-Aware Attention** | Moderate | **Native Syntax Maps** | Standard Attention | Standard Attention | Standard Attention |
| **Quantized VRAM (Q4)**| **16.8 GB (Q4_K_M)** | **17.2 GB (Q4_K_M)** | 14.5 GB | 20.5 GB | 11.2 GB |
| **Inference TPS (RTX 4090)**| **88–110 tokens/s** | **78–96 tokens/s** | 55–72 tokens/s | 38–48 tokens/s | 95–125 tokens/s |
| **FastMCP 3.1 Support** | **Full Native Tooling** | **Full Task RPC Support**| Tool Calling Endpoint | Agent Protocol | OpenAI Compatible Only |
| **HumanEval / MultiPL-E** | 84.6% | **89.2%** | 81.1% | 88.4% | 81.8% |

---

## Typical use cases
- **Local Autocomplete**: Delivering sub-100ms autocomplete in IDEs such as VS Code.
- **Offline Codebase Generation**: Creating complete multi-file modules in private, air-gapped environments.
- **Advanced Code Refactoring**: Executing complex AST-level optimizations, lint-fixing, and system restructuring using Kat Coder 2.5 Dev.
- **Automated CLI Coding**: Driving agentic developer cycles via terminal assistants like [Aider](../development_ops/aider.md) and [Cline](../agents/cline.md).

## Strengths
- **Low Latency**: Highly optimized attention and routing mechanisms yield exceptional tokens-per-second (TPS) throughput.
- **Extensive Context Window**: Out-of-the-box support for a 128k context window allows entire codebases to be scanned locally.
- **Highly Resource-Efficient**: The MoE architecture enables running a model with a virtual 30B parameter size using only 7B active parameters.
- **Superior Multi-lingual Support**: Highly optimized for Python, TypeScript, Rust, C++, and Go.
- **AST-Aware Reasoning**: Kat Coder 2.5 Dev features specialized attention maps focused on syntax structural dependencies.

## Limitations
- **General Knowledge**: Not a general-purpose model; trails behind [Qwen](../ai_knowledge/qwen.md), [DeepSeek](deepseek.md) (DeepSeek-V4), and Gemma 4 in general trivia, creative writing, or non-technical reasoning.
- **High Concurrency VRAM Footprint**: Though active parameters are small, loading the full MoE weights requires substantial VRAM if running multiple concurrent streams.
- **Setup Complexity**: Requires local model execution setup, which can be more complex than subscribing to a SaaS provider.

## When to use it
- When you require complete, local data privacy for sensitive corporate codebases.
- When you need a reliable offline coding assistant on a consumer GPU or unified memory Mac.
- When latency and immediate response are critical for your autocomplete and chat integrations.
- When performing complex developmental code generation where specialized coding logic is required (using Kat Coder 2.5 Dev).

## When not to use it
- For broad creative writing, general knowledge retrieval, or multi-modal analysis.
- If you do not have a modern GPU with at least 16GB VRAM (or Apple Silicon unified memory).
- If your workflow is fully integrated with cloud-only ecosystems like [Codestral](codestral.md).

---

### Production Multi-Container Docker Compose Stack

The following Docker Compose configuration orchestrates a high-performance local inference stack featuring `llama-server` (with CUDA acceleration), a FastMCP 3.1 code server bridge, and Prometheus metrics exporting:

```yaml
version: "3.8"

networks:
  katcoder_net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.31.25.0/24

volumes:
  model_weights:
  server_logs:

services:
  llama_backend:
    image: ghcr.io/ggerganov/llama.cpp:server-cuda
    container_name: katcoder_backend
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    command:
      - "--model"
      - "/models/katcoderair-2.5-q4_k_m.gguf"
      - "--host"
      - "0.0.0.0"
      - "--port"
      - "8080"
      - "--ctx-size"
      - "16384"
      - "--n-gpu-layers"
      - "99"
      - "--threads"
      - "8"
      - "--batch-size"
      - "512"
      - "--metrics"
    volumes:
      - model_weights:/models
    networks:
      - katcoder_net
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  fastmcp_code_server:
    build:
      context: .
      dockerfile_inline: |
        FROM python:3.12-slim
        WORKDIR /opt/katcoder
        RUN pip install --no-cache-dir fastmcp>=3.1.0 pydantic>=2.7.0 openai>=1.30.0 httpx>=0.27.0
        COPY katcoder_mcp.py /opt/katcoder/
        CMD ["python3", "katcoder_mcp.py"]
    container_name: katcoder_fastmcp
    restart: unless-stopped
    depends_on:
      llama_backend:
        condition: service_healthy
    environment:
      LLAMA_ENDPOINT: http://katcoder_backend:8080/v1
      MCP_PORT: 8094
    ports:
      - "8094:8094"
    volumes:
      - server_logs:/var/log/katcoder
    networks:
      - katcoder_net
```

---

### Production Systemd Service Unit (`katcoderair-inference.service`)

To deploy KatCoderAir as a persistent local inference daemon with OpenAI-compatible API endpoints, deploy the following unit configuration:

```ini
[Unit]
Description=KatCoderAir v2.5 MoE Inference Gateway
After=network.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=katcoder
Group=katcoder
WorkingDirectory=/opt/katcoderair
ExecStart=/opt/katcoderair/bin/llama-server \
    --model /opt/katcoderair/models/katcoderair-2.5-q4_k_m.gguf \
    --host 127.0.0.1 \
    --port 8080 \
    --ctx-size 16384 \
    --n-gpu-layers 99 \
    --threads 8 \
    --batch-size 512
Restart=always
RestartSec=5s
Environment=LLAMA_ARG_MODEL=/opt/katcoderair/models/katcoderair-2.5-q4_k_m.gguf
Environment=CUDA_VISIBLE_DEVICES=0

# Systemd Hardening Parameters
ProtectSystem=full
ProtectHome=read-only
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

---

## Getting started
To run KatCoderAir v2.5 or Kat Coder 2.5 Dev locally, you can use the GGUF weights via llama.cpp or the MLX format on macOS.

### Installation
Ensure you have the latest `llama.cpp` tools compiled on your path.
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make -j
```

### Run Model
Download the quantized GGUF file and run it using the following command:
```bash
# Run KatCoderAir v2.5
./llama-cli \
  -m ./models/katcoderair-2.5-q4_k_m.gguf \
  -c 8192 \
  -p "Write a Python script that implements a thread-safe cache."

# Run Kat Coder 2.5 Dev
./llama-cli \
  -m ./models/katcoder-2.5-dev-q4_k_m.gguf \
  -c 16384 \
  -p "Implement a custom memory-mapped key-value store in Rust."
```

---

## CLI examples

### Querying the model via curl
```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "katcoderair-v2.5",
    "messages": [
      {"role": "user", "content": "Explain how to write a custom decorator in Python."}
    ]
  }'
```

### Running benchmark via llama-bench
```bash
./llama-bench -m ./models/katcoderair-2.5-q4_k_m.gguf -t 8 -b 512
```

---

## API examples

### Production FastMCP 3.1 Code Generation Tool Server
The complete Python script below runs a FastMCP 3.1 server with strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) to validate code generation and refactoring requests against the local KatCoderAir instance:

```python
import os
import json
import hashlib
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from mcp.server.fastmcp import FastMCP, Context
from openai import OpenAI

mcp = FastMCP(
    name="KatCoderAir-Code-Server",
    version="3.1.0",
    description="Local edge code generation and refactoring server powered by KatCoderAir v2.5 MoE"
)

client = OpenAI(
    base_url=os.getenv("LLAMA_ENDPOINT", "http://localhost:8080/v1"),
    api_key="local-katcoder"
)

class CodeGenRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_description: str = Field(..., min_length=5, max_length=1500, description="Functional specification of code to write")
    target_language: str = Field(default="python", pattern="^(python|typescript|rust|cpp|go)$")
    include_unit_tests: bool = Field(default=True, description="Whether to generate complete unit test suite")
    ast_optimization_pass: bool = Field(default=True, description="Enable Kat Coder 2.5 Dev syntax analysis")

class CodeGenResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_hash: str
    target_language: str
    generated_source_code: str
    test_cases_code: Optional[str] = None
    estimated_tokens_per_sec: float
    model_identifier: str = "katcoderair-2.5-q4_k_m"

@mcp.tool(
    name="generate_code_module",
    description="Generates production-grade, type-annotated code modules using local KatCoderAir MoE."
)
async def generate_code_module(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """Generates clean source code and tests via local KatCoderAir inference."""
    if ctx:
        await ctx.info("Validating code generation request schema...")

    try:
        req = CodeGenRequest.model_validate(request_dict)
        task_hash = hashlib.sha256(f"{req.task_description}:{req.target_language}".encode()).hexdigest()

        if ctx:
            await ctx.info(f"Dispatching query to KatCoderAir ({req.target_language}, AST pass: {req.ast_optimization_pass})...")

        system_prompt = f"You are Kat Coder 2.5 Dev. Write idiomatic, memory-safe, and fully type-hinted {req.target_language} code."
        user_prompt = f"Requirement: {req.task_description}\n"
        if req.include_unit_tests:
            user_prompt += "Include comprehensive unit tests with edge case assertions."

        response = client.chat.completions.create(
            model="katcoderair-v2.5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.15,
            max_tokens=4096
        )

        raw_output = response.choices[0].message.content or ""

        res = CodeGenResponse(
            task_hash=task_hash,
            target_language=req.target_language,
            generated_source_code=raw_output,
            test_cases_code=raw_output if req.include_unit_tests else None,
            estimated_tokens_per_sec=92.4
        )

        return {
            "status": "success",
            "code_data": res.model_dump()
        }
    except ValidationError as ve:
        if ctx:
            await ctx.error(f"Validation failure: {ve}")
        raise ValueError(f"Invalid code generation request payload: {ve}")

if __name__ == "__main__":
    mcp.run()
```

### Direct Python Local Inference with llama-cpp-python
```python
from llama_cpp import Llama

# Load the KatCoderAir model
llm = Llama(
    model_path="./models/katcoderair-2.5-q4_k_m.gguf",
    n_ctx=2048,
    n_threads=4
)

# Generate coding solution
output = llm(
    "Q: Write a Rust function to parse a CSV file. A:",
    max_tokens=256,
    stop=["Q:", "\n\n"],
    echo=True
)
print(output["choices"][0]["text"])
```

---

### Systematic Diagnostic & Troubleshooting Matrix

| Issue / Error Symptom | Root Cause | Verification Procedure | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **`CUDA out of memory` during startup** | MoE weights exceed allocated VRAM | Check GPU VRAM via `nvidia-smi` or `rocm-smi` | Lower `--n-gpu-layers` or switch to `Q4_K_M` GGUF quantization. |
| **Sub-optimal token generation speed (< 20 TPS)** | CPU fallback for active expert calculations | Inspect layer offloading output in `journalctl -u katcoderair-inference` | Ensure all MoE router gating layers are offloaded to GPU (`--n-gpu-layers 99`). |
| **Malformed JSON schema responses in FastMCP** | System prompt missing explicit schema constraints | Verify raw curl completions output from `http://localhost:8080/v1/chat/completions` | Enforce JSON Schema parameters in response_format and use Kat Coder 2.5 Dev. |
| **Context truncation on multi-file queries** | Default context window too small for large prompt | Inspect active context length parameter | Increase context limit (`--ctx-size 16384` or `32768`) with KV cache quantization. |
| **Gating Router Misrouting** | Out-of-distribution input causing wrong expert routing | Trace expert activation via llama-bench or debug logs | Add explicit category system tags (e.g. `[PYTHON_AST]`) in user prompt. |
| **FastMCP Subprocess Connection Reset** | Timeout on long-running multi-file code completion passes | Check `journalctl -u katcoderair-inference` for dropped TCP sessions | Set client keepalive and increase HTTP timeout to 120s. |
| **High CPU Load / Host Thread Thrashing** | Thread count set higher than physical CPU cores | Inspect `top` or `htop` thread utilization | Set `--threads` equal to physical core count (e.g. 8 cores). |
| **PydanticFrozenInstanceError** | Post-processing hook attempting in-place field updates on report schema | Review Python traceback logs | Use `res.model_copy(update={...})` instead of direct attribute assignment. |

---

### Operational Best Practices

#### VRAM & Quantization Tuning
1. **Quantization Selection**: For consumer GPUs with 16GB VRAM (NVIDIA RTX 4080 / 5070), use `Q4_K_M` GGUF quantization. For Apple Silicon unified memory (32GB+ M-series Macs), use `Q8_0` or 16-bit MLX weights.
2. **Context Shift Management**: Set `-c 16384` for IDE completion tasks. When analyzing multi-file codebases, enable context shifting (`--ctx-shift`) in llama.cpp to maintain high token throughput across multi-turn developer chat sessions.
3. **MoE Offloading**: Ensure all MoE router gating layers and active experts are offloaded to GPU memory (`-ngl 99`) to eliminate CPU host-RAM transfer overhead during token generation.

---

## Related tools / concepts
- [Local LLMs](../ai_knowledge/local_llms.md) — Standard overview of open weights models.
- [DeepSeek](deepseek.md) — The flagship MoE open-weight models (DeepSeek-V4).
- [Codestral](codestral.md) — Coding model from Mistral AI.
- [llama.cpp](../infrastructure/llama-cpp.md) — The primary runtime engine for CPU/GPU.
- [MLX](../infrastructure/mlx.md) — Apple Silicon array framework.
- [ExLlamaV3](../infrastructure/exllamav3.md) — NVIDIA-optimized local inference.
- [Aider](../development_ops/aider.md) — CLI-based AI editing tool.
- [Qwen](../ai_knowledge/qwen.md) — Foundational open-weight Qwen architecture.

---

## Sources / references
- [KatCoder Collective GitHub](https://github.com/katcoder-collective/katcoderair)
- [Reddit LocalLLaMA Thread: KatCoderAir v2.5 Announcement](https://www.reddit.com/r/LocalLLaMA/comments/1uwbe7w/katcoderair_v25_open_model_soon/)
- [Reddit LocalLLaMA Thread: Kat Coder 2.5 Dev - Do yourself a favor and try it](https://www.reddit.com/r/LocalLLaMA/comments/1ve9r2q/kat_coder_25_dev_do_yourself_a_favor_and_try_it/)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
