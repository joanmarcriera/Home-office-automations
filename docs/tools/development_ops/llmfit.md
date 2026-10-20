# llmfit

## What it is
llmfit is a high-performance, command-line hardware-to-model compatibility and estimation utility written in Rust and Python. Developed to simplify local deployment planning and agentic resource scheduling, llmfit automatically scans local host hardware specifications (CPU architecture, RAM speed, PCIe bandwidth, GPU chipset, active VRAM availability, and Apple Silicon Unified Memory configurations) and calculates exactly which models can run locally, what quantization formats are feasible, and what generation throughput (tokens per second) to expect.

As of early 2027, llmfit features native estimation presets for state-of-the-art models like **Gemma 4**, **Llama 4**, **Qwen 3.6**, **DeepSeek-V4**, and supports calculating memory footprints for **MCP 3.1 / FastMCP 3.1** local microservers, embedding models, and vector database sidecars.

## What problem it solves
Setting up local Large Language Models or specialized agent components is traditionally hindered by resource sizing guesswork:
- **Out-of-Memory (OOM) Errors**: Trying to run models that exceed physical GPU VRAM causes immediate system freezes or severe performance fallbacks to CPU paging.
- **Suboptimal Quantization**: Determining if a model runs better under 4-bit, 8-bit, or FP16 precision on a specific hardware configuration requires tedious manual trial-and-error.
- **Microservice Memory Overhead**: Failing to account for the background RAM/VRAM consumed by active local FastMCP 3.1 servers, vector databases, and container sandboxes during multi-agent execution.
- **Context Window Blowup**: Neglecting the exponential VRAM footprint of high-context key-value (KV) caches when expanding context windows from 4K to 32K or 128K tokens.

llmfit solves these bottlenecks by executing instant, predictive mathematical audits of local hardware capability profiles. This ensures that any model or local agent runtime selected by your workspace orchestrator is fully compatible and mathematically guaranteed to fit within physical execution boundaries.

## Hardware Estimation Pipeline Flow

```
+-----------------------------------------------------------------------------------+
|                        LLMFIT HARDWARE ESTIMATION PIPELINE                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Hardware Discovery Engine                                                   |  |
|  | - CUDA / ROCm / Apple Metal System Calls                                    |  |
|  | - Free VRAM, Unified Memory Bandwidth, PCIe Gen4/5 Throughput               |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|                                        v                                          |
|  +-----------------------------------------------------------------------------+  |
|  | Mathematical Sizing Matrix Engine                                           |  |
|  | - Base Weights Footprint: W = (Params * BitsPerWeight) / 8                  |  |
|  | - KV Cache Sizing: KV = 2 * Layers * Heads * Dim * SeqLen * Precision       |  |
|  | - FastMCP 3.1 Agent & Microservice Overhead Factor                         |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|                                        v                                          |
|  +-----------------------------------------------------------------------------+  |
|  | Feasibility & Recommendation TUI                                            |  |
|  | - Interactive Terminal Sizing Matrix                                        |  |
|  | - Tokens/sec Generation Estimator & Quantization Advice (Q4_K_M vs Q8_0)      |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Local Sizing & Planning Utility. llmfit operates as a critical preparatory step. Before launching local LLM container platforms (like [Ollama](../../services/ollama.md), [vLLM](../infrastructure/vllm.md), or [LM Studio](../infrastructure/lm-studio.md)), developers and autonomous scripts run llmfit to dynamically verify host hardware capacity, making it a cornerstone of local-first agent engineering setups.

```
+-----------------------------------------------------------------------------------+
|                              SYSTEM STACK INTEGRATION                             |
+-----------------------------------------------------------------------------------+
|  [ Workspace Agent Orchestrator ] -> Calls `llmfit plan --json`                  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                            LLMFIT HARDWARE AUDIT DAEMON                           |
|       (Direct GPU Hardware Probe | Quantization Math | FastMCP Overhead)         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         LOCAL INFERENCE ENGINE PROVISIONING                        |
|        [ vLLM Instance ]        [ Ollama Service ]        [ FastMCP Tools ]       |
+-----------------------------------------------------------------------------------+
```

## LLM Sizing Utility Comparison

| Dimension / Feature | llmfit | CanItRunLLM | Ollama System Audit | Manual Formula Calculation |
| :--- | :--- | :--- | :--- | :--- |
| **Interface Format** | CLI & Vim TUI | Web UI | CLI Verbose Logs | Manual Math / Spreadsheet |
| **Hardware Scanning** | Automatic (CUDA/ROCm/Metal) | Manual Input | Basic VRAM Probe | Manual Specs Entry |
| **KV Cache Footprint** | Dynamic Context Window Math | Fixed Estimates | Runtime Allocation | Custom Formula |
| **FastMCP 3.1 Modeling** | Native Overhead Sizing | Not Supported | Not Supported | Manual Overhead Addition |
| **JSON Export for CI/CD** | Native `--json` Export | Web Output | None | Manual Entry |
| **Daemon Execution** | Systemd Background Monitor | None | CLI Runtime | None |

## Typical use cases
- **Local Model Sizing Audits**: Checking if your development machine can run **Gemma 4 27B** or if you need to downsize to **Gemma 4 4B** or **Llama 4** variants.
- **Quantization Optimization**: Automatically identifying the maximum quantization level (e.g., Q4_K_M vs Q8_0) that will fit perfectly within available GPU boundaries.
- **Agentic Resource Partitioning**: Allowing developer agents to dynamically size hardware partitions for concurrent local models and active **FastMCP 3.1** server bindings.
- **System Upgrade Simulation**: Simulating hypothetical system configurations (e.g., adding an additional RTX 5090 or upgrading to 128GB Unified Memory) to evaluate performance gains.

## Strengths
- **Instant System Discovery**: Automatically detects complex hardware parameters across macOS (Apple Silicon Unified Memory), Linux (CUDA/ROCm), and Windows environments.
- **Robust Interactive TUI**: Features a highly responsive, Vim-key compatible terminal user interface with dynamic search, multi-model comparison, and filtering.
- **Community-Backed Performance Presets**: Integrates directly with community telemetry databases (such as localmaxxing.com) to provide real-world, verified benchmarks.
- **FastMCP 3.1 Compatibility**: Fully models memory overhead for concurrent tool servers, allowing holistic scheduling calculations for complex multi-agent sandboxes.

## Limitations
- **Mathematical Estimation**: Calculates expected sizing using theoretical model equations; active background host applications can introduce real-world performance variance.
- **Stateless Analysis**: Feasibility calculations are strictly localized and do not automatically resolve third-party cloud API limits.
- **Offline Cache Sizing**: Sizing predictions do not analyze available disk storage space unless explicitly requested via specific CLI commands.

## When to use it
- When choosing between local or hosted inference providers for your application stack.
- Before installing and downloading massive GGUF or SafeTensor models to prevent wasted bandwidth.
- Inside automated setup scripts to dynamically verify that a developer's system meets the minimum requirements for an AI-powered repository.

## When not to use it
- If your development architecture is entirely cloud-hosted and relies solely on remote APIs (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra).
- For tracing live performance execution profiles during active model inference (use specialized telemetry platforms like Prometheus or Arize instead).

## Systemd Daemon Unit Configuration

For continuous hardware telemetry monitoring and automated local agent provisioning, `llmfit` can run as a background systemd service unit.

```ini
[Unit]
Description=LLMFit Hardware Telemetry and Sizing Daemon
After=network.target nvidia-persistenced.service
Wants=nvidia-persistenced.service

[Service]
Type=simple
User=llmfit
Group=llmfit
ExecStart=/usr/local/bin/llmfit daemon --port 9091 --interval 15 --json-socket /var/run/llmfit/telemetry.sock
Restart=always
RestartSec=5s
Environment=CUDA_VISIBLE_DEVICES=0,1
MemoryMax=512M
ProtectSystem=full
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Getting started

### Installation

**Using Homebrew (macOS / Linux)**
```bash
brew install llmfit
```

**Using python (uv / pip)**
```bash
uv tool install -U llmfit@latest
```

**Via raw script installation**
```bash
curl -fsSL https://llmfit.axjns.dev/install.sh | sh
```

### Initial execution
Launch the interactive Terminal User Interface:
```bash
llmfit
```
- Use `j` and `k` to navigate.
- Type `/` to search by model family or use-case.
- Press `S` to simulate upgraded hardware profiles.

## Production Guidelines & Sizing Best Practices
- **KV Cache Safety Margin**: Always reserve at least 15-20% VRAM buffer beyond base model weights to accommodate KV cache expansion at large context windows (32K+).
- **Multi-Agent Overhead**: When running concurrent FastMCP 3.1 servers or background embedding models, account for an extra 1.5 - 3.0 GB of host RAM/VRAM buffer.
- **CI/CD Gating**: Integrate `llmfit plan --json` checks in local setup scripts to fail fast if developer hardware cannot support required benchmark models.
- **Unified Memory Allocation**: On Apple Silicon, configure macOS sysctl settings (`iogpu.wired_mem_limit`) if dedicating >75% of unified RAM to LLM inference.

## CLI examples

### Export detected hardware profile
```bash
# Output host specs to a clean JSON telemetry file
llmfit system --json > host_profile.json
```

### Plan local model deployment
```bash
# Calculate hardware feasibility for Gemma 4 27B with a 32K context window
llmfit plan "google/gemma-4-27b-it" --context 32768 --json
```

### Request top recommendations
```bash
# Find the top 3 verified local coding models suited for your active hardware
llmfit recommend --use-case coding --limit 3 --json
```

### Run background telemetry check
```bash
# Inspect current available GPU VRAM and active FastMCP overhead
llmfit status --format text
```

## API examples

The following code illustrates utilizing **Pydantic v2** validation and **FastMCP 3.1** server tools to model a development node's local resource constraints and mathematically determine if a target Llama 4 or Gemma 4 model will fit without triggering an OOM condition.

```python
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Initialize FastMCP 3.1 Server
mcp = FastMCP("llmfit-sizing-server")

class NodeHardwareSpec(BaseModel):
    available_vram_gb: float = Field(..., ge=0.0, description="Available GPU Video RAM in Gigabytes.")
    available_ram_gb: float = Field(..., ge=0.0, description="Available System RAM in Gigabytes.")
    unified_memory: bool = Field(False, description="True if host platform uses Apple Silicon or Unified Memory.")
    active_mcp_servers_count: int = Field(0, ge=0, description="Number of currently running FastMCP 3.1 background servers.")

    @field_validator("available_vram_gb", "available_ram_gb")
    @classmethod
    def check_non_negative(cls, v: float) -> float:
        if v < 0.0:
            raise ValueError("Memory values must be non-negative")
        return round(v, 2)

class ModelMemoryRequirement(BaseModel):
    model_name: str = Field(..., min_length=2, description="Identifier of the LLM")
    base_weight_size_gb: float = Field(..., gt=0.0, description="Model file footprint on disk/memory.")
    context_overhead_per_10k_tokens_gb: float = Field(..., gt=0.0, description="VRAM footprint for active KV Cache per 10k context.")

class SizingEvaluationResult(BaseModel):
    feasible: bool
    target_context: int
    calculated_total_vram_required_gb: float
    available_vram_gb: float
    mcp_overhead_gb: float
    unified_memory_fallback: bool
    recommended_quantization: str

@mcp.tool()
async def evaluate_model_fit(
    hardware_payload: Dict[str, Any],
    model_payload: Dict[str, Any],
    target_context: int = 16384,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Validates hardware and model parameters via Pydantic v2 and calculates local deployment feasibility."""
    if ctx:
        await ctx.info(f"Evaluating model fit for target context {target_context}...")

    try:
        hw = NodeHardwareSpec.model_validate(hardware_payload)
        model = ModelMemoryRequirement.model_validate(model_payload)

        # FastMCP 3.1 background overhead calculation (0.5 GB per active tool server)
        mcp_overhead = hw.active_mcp_servers_count * 0.5
        kv_cache_factor = target_context / 10000.0
        total_required = model.base_weight_size_gb + (model.context_overhead_per_10k_tokens_gb * kv_cache_factor) + mcp_overhead

        is_feasible = (hw.available_vram_gb >= total_required) or (hw.unified_memory and (hw.available_ram_gb >= total_required))

        quant_rec = "Q8_0 or FP16" if (hw.available_vram_gb >= total_required * 1.5) else ("Q4_K_M" if is_feasible else "Infeasible - Reduce Context or Downsize Model")

        result = SizingEvaluationResult(
            feasible=is_feasible,
            target_context=target_context,
            calculated_total_vram_required_gb=round(total_required, 2),
            available_vram_gb=hw.available_vram_gb,
            mcp_overhead_gb=mcp_overhead,
            unified_memory_fallback=hw.unified_memory,
            recommended_quantization=quant_rec
        )

        return result.model_dump()

    except ValidationError as ve:
        return {"error": "Validation failed", "details": ve.errors()}
    except Exception as e:
        return {"error": "Execution exception", "message": str(e)}

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **CUDA OOM on Model Startup** | VRAM overcommitted beyond physical GPU limits | `llmfit plan <model> --json` | Select lower quantization (Q4_K_M vs Q8_0) or reduce context size |
| **Severe Token Generation Lag** | System fallback to CPU RAM paging due to VRAM overflow | `llmfit system --check-paging` | Configure `iogpu.wired_mem_limit` or restrict GPU layers in Ollama/vLLM |
| **FastMCP Server Crashing** | Unaccounted background VRAM allocation by MCP tool runners | `llmfit status --mcp-audit` | Add 1.5 - 3.0 GB VRAM safety buffer in `llmfit` sizing plan |
| **ROCm GPU Detection Failure** | Missing HIP/ROCm driver path bindings | `llmfit system --device-type rocm` | Set `ROCM_PATH=/opt/rocm` and update `llmfit` hardware drivers |
| **Incorrect Apple Silicon Bandwidth** | macOS sysctl throttle on battery power | `llmfit system --power-state` | Connect host machine to AC power source for full memory bandwidth |

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Local packaging and execution platform for LLMs.
- [vLLM](../infrastructure/vllm.md) — High-throughput local model serving engine.
- [LocalAI](../infrastructure/localai.md) — Multi-model local OpenAI compatible API wrapper.
- [LM Studio](../infrastructure/lm-studio.md) — Visual local inference explorer and service controller.
- [Claude Code](claude-code.md) — Local agent CLI requiring compatibility sizing checks.

## Sources / references
- [llmfit GitHub Repository](https://github.com/AlexsJones/llmfit)
- [Official Sizing & Benchmark Matrix](https://llmfit.axjns.dev/)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
