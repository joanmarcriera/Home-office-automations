# llmfit

## What it is
llmfit is a high-performance, command-line hardware-to-model compatibility and estimation utility. Developed to simplify local deployment planning, llmfit automatically scans your local host hardware specifications (CPU architecture, RAM speed, GPU chipset, and active VRAM availability) and calculates exactly which models can run locally, what quantization formats are feasible, and what generation performance (tokens per second) to expect. As of late November/December 2026, it features native estimation presets for state-of-the-art models like **Gemma 3**, **Llama 4**, **Qwen 3.6**, and supports calculating memory footprints for **MCP 3.1 / FastMCP 3.1** local microservers.

## What problem it solves
Setting up local Large Language Models or specialized agent components is traditionally hindered by resource sizing guesswork:
- **Out-of-Memory (OOM) Errors**: Trying to run models that exceed physical GPU VRAM causes immediate system freezes or severe performance fallbacks (CPU paging).
- **Suboptimal Quantization**: Determining if a model runs better under 4-bit, 8-bit, or FP16 precision on a specific hardware configuration requires tedious manual trial-and-error.
- **Microservice Memory Overhead**: Failing to account for the background RAM/VRAM consumed by active local MCP servers, databases, and container sandboxes during multi-agent trials.

llmfit solves these bottlenecks by executing instant, predictive mathematical audits of your local hardware capability profile. This ensures that any model or local agent runtime selected by your workspace orchestrator is fully compatible and mathematically guaranteed to fit within your execution boundaries.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Local Sizing & Planning Utility. llmfit operates as a critical preparatory step. Before launching local LLM container platforms (like Ollama, vLLM, or LM Studio), developers and autonomous scripts run llmfit to dynamically verify the host hardware capacity, making it a cornerstone of local-first agent engineering setups.

## Typical use cases
- **Local Model Sizing Audits**: Checking if your development machine can run **Gemma 3 27B** or if you need to downsize to the **Gemma 3 4B** variant.
- **Quantization Optimization**: Automatically identifying the maximum quantization level (e.g., Q4_K_M vs Q8_0) that will fit perfectly within available GPU boundaries.
- **Agentic Resource Partitioning**: Allowing developer agents to dynamically size hardware partitions for concurrent local models and active **FastMCP 3.1** server bindings.
- **System Upgrade Simulation**: Simulating hypothetical system configurations (e.g., adding an additional RTX 5090 or upgrading to 128GB Unified Memory) to evaluate performance gains.

## Strengths
- **Instant System Discovery**: Automatically detects complex hardware parameters across macOS (Apple Silicon Unified Memory), Linux (CUDA/ROCm), and Windows environments.
- **Robust Interactive TUI**: Features a highly responsive, Vim-key compatible terminal user interface with dynamic search, multi-model comparison, and filtering.
- **Community-Backed Performance Presets**: Integrates directly with community telemetry databases (such as localmaxxing.com) to provide real-world, verified benchmarks.
- **MCP 3.1 Compatibility**: Fully models memory overhead for concurrent tool servers, allowing holistic scheduling calculations for complex multi-agent sandboxes.

## Limitations
- **Mathematical Estimation**: Calculates expected sizing using theoretical model equations; active background host applications can introduce real-world performance variance.
- **Stateless Analysis**: Feasibility calculations are strictly localized and do not automatically resolve third-party cloud API limits.
- **Offline Cache Sizing**: Sizing predictions do not analyze available disk storage space unless explicitly requested via specific CLI commands.

## When to use it
- When choosing between local or hosted inference providers for your application stack.
- Before installing and downloading massive GGUF or SafeTensor models to prevent wasted bandwidth.
- Inside automated setup scripts to dynamically verify that a developer's system meets the minimum requirements for an AI-powered repository.

## When not to use it
- If your development architecture is entirely cloud-hosted and relies solely on remote APIs (Anthropic, OpenAI, Gemini).
- For tracing live performance execution profiles during active model inference (use specialized telemetry platforms like Prometheus or Arize instead).

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

## CLI examples

### Export detected hardware profile
```bash
# Output host specs to a clean JSON telemetry file
llmfit system --json > host_profile.json
```

### Plan local model deployment
```bash
# Calculate hardware feasibility for Gemma 3 27B with a 32K context window
llmfit plan "google/gemma-3-27b-it" --context 32768 --json
```

### Request top recommendations
```bash
# Find the top 3 verified local coding models suited for your active hardware
llmfit recommend --use-case coding --limit 3 --json
```

## API examples

The following code illustrates utilizing **Pydantic v2** validation to model a development node's local resource constraints and mathematically determine if a target Llama 4 or Gemma 3 model will fit without triggering an OOM condition.

```python
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Literal
import json

class NodeHardwareSpec(BaseModel):
    available_vram_gb: float = Field(..., ge=0.0, description="Available GPU Video RAM in Gigabytes.")
    available_ram_gb: float = Field(..., ge=0.0, description="Available System RAM in Gigabytes.")
    unified_memory: bool = Field(False, description="True if host platform uses Apple Silicon or Unified Memory.")

class ModelMemoryRequirement(BaseModel):
    model_name: str = Field(..., min_length=2)
    base_weight_size_gb: float = Field(..., gt=0.0, description="Model file footprint on disk/memory.")
    context_overhead_per_10k_tokens_gb: float = Field(..., gt=0.0, description="VRAM footprint for active KV Cache.")

    model_config = {
        "populate_by_name": True
    }

def evaluate_model_fit(hardware_payload: str, model_payload: str, target_context: int = 16384) -> str:
    """Validates parameters via Pydantic v2 and calculates local deployment feasibility."""
    try:
        hw_data = json.loads(hardware_payload)
        model_data = json.loads(model_payload)

        # Pydantic v2 validations
        hw = NodeHardwareSpec.model_validate(hw_data)
        model = ModelMemoryRequirement.model_validate(model_data)

        # Sizing logic
        kv_cache_factor = target_context / 10000.0
        total_required_vram = model.base_weight_size_gb + (model.context_overhead_per_10k_tokens_gb * kv_cache_factor)

        # Sizing check
        has_vram_fit = hw.available_vram_gb >= total_required_vram
        has_ram_fit = hw.available_ram_gb >= model.base_weight_size_gb if hw.unified_memory else False

        is_feasible = has_vram_fit or (hw.unified_memory and (hw.available_ram_gb >= total_required_vram))

        return json.dumps({
            "feasible": is_feasible,
            "target_context": target_context,
            "calculated_total_vram_required_gb": round(total_required_vram, 2),
            "available_vram_gb": hw.available_vram_gb,
            "unified_memory_fallback": hw.unified_memory,
            "model_metadata": model.model_dump()
        }, indent=2)

    except ValidationError as ve:
        return json.dumps({
            "error": "Validation failed on parameters.",
            "details": ve.errors()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Execution exception",
            "message": str(e)
        }, indent=2)

if __name__ == "__main__":
    # Test sizing a Gemma 3 27B model on an 8GB VRAM developer machine
    mock_hw = '{"available_vram_gb": 8.1, "available_ram_gb": 16.0, "unified_memory": false}'
    mock_model = '{"model_name": "gemma-3-27b-it-q4", "base_weight_size_gb": 14.5, "context_overhead_per_10k_tokens_gb": 1.2}'

    print("Direct Feasibility Report:")
    print(evaluate_model_fit(mock_hw, mock_model, target_context=16384))
```

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
- Last reviewed: 2026-12-13
- Confidence: high
