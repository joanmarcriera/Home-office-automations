# llmfit

## What it is
llmfit is a hardware-to-model fit utility that helps you determine which models and providers are realistic for your machine. As of July 2026, it features a comprehensive database for the **Gemma 3** model family and native integration with the **FastMCP 3.0** adapter for real-time hardware telemetry.

## What problem it solves
It prevents wasted time trying to run models that do not fit your hardware or performance requirements. It provides a data-driven approach to model selection, ensuring that your local AI stack is optimized for the resources available on your machine.

## Where it fits in the stack
**Development & Ops / Model Selection Utility**. It is a planning tool for local AI deployment decisions.

## Typical use cases
- **Choosing Local Models**: Selecting the best performing models (e.g., [Gemma 3](../ai_knowledge/local_llms.md)) that fit within your system's VRAM.
- **Hardware Profile Comparison**: Comparing what can run on different hardware profiles, from edge devices to high-end workstations.
- **Deciding Infrastructure**: Determining whether to use [Ollama](../../services/ollama.md), [LM Studio](../infrastructure/lm-studio.md), or a cloud provider for a specific task.
- **Quantization Optimization**: Finding the "sweet spot" for quantization levels (e.g., Q4_K_M vs Q8_0) for your specific hardware.

## Strengths
- **Fast Hardware Reality Check**: Instantly detects CPU, RAM, and GPU/VRAM to provide tailored model recommendations.
- **Vim-like TUI**: Powerful interactive interface with search, filtering, and bulk comparison modes.
- **Community Benchmarks**: Integration with [localmaxxing.com](https://localmaxxing.com) (press `b`) to see real-world performance data from other users.
- **Hardware Simulation**: Press `S` to override your system specs and see what models would run on a target upgrade (e.g., RTX 5090).
- **Download Manager**: Native management of model downloads and local cache for Ollama, llama.cpp, and LM Studio.

## Limitations
- **Estimation vs. Execution**: Provides theoretical speed and fit estimates; actual performance may vary based on concurrent system load.
- **Workflow Agnostic**: Helps with feasibility and fit, but does not design the application-level workflow or agent architecture.

## When to use it
- Before investing in new hardware for local LLM execution.
- When choosing the optimal quantization level for a specific model on your machine.
- To compare real-world performance data from the community before downloading large models.

## When not to use it
- When you already know you will use hosted frontier APIs (OpenAI, Anthropic, etc.) and have no interest in local execution.
- If you require a tool that actually benchmarks the model on your hardware by running it (see `llm-checker`).

## Getting started

### Installation

**macOS / Linux (Homebrew)**
```bash
brew install llmfit
```

**Python (uv / pip)**
```bash
uv tool install -U llmfit
```

**Quick Install (Script)**
```bash
curl -fsSL https://llmfit.axjns.dev/install.sh | sh
```

### Initial Run
Simply type `llmfit` to launch the interactive TUI. It will automatically detect your CPU, RAM, and GPU/VRAM to provide tailored recommendations.

## CLI examples

### Interactive TUI (Default)
```bash
llmfit
```

### System Audit
```bash
# Display detected system hardware specs in JSON format
llmfit system --json
```

### Hardware Planning
```bash
# Estimate required hardware for a specific model and context length
llmfit plan "google/gemma-3-27b" --context 8192 --json
```

## API examples

### Fetching Node Recommendations
```python
import requests

# Query the local llmfit service for the best coding models
url = "http://localhost:8787/api/v1/models/top?limit=3&use_case=coding"
response = requests.get(url)
models = response.json()

for model in models:
    print(f"Recommended: {model['name']} (Score: {model['score']})")
```

### Starting the Server
```bash
llmfit serve --host 0.0.0.0 --port 8787
```

### Exporting Fit Data
```bash
curl -X GET http://localhost:8787/api/v1/system/fit-report
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Local model runner.
- [LM Studio](../infrastructure/lm-studio.md) — GUI for local models.
- [LocalAI](../infrastructure/localai.md) — Self-hosted OpenAI-compatible API.
- [llama.cpp](../infrastructure/llama-cpp.md) — Port of Meta's Llama model in C/C++.
- [MLX](../infrastructure/mlx.md) — Apple Silicon LLM framework.
- [ExLlamaV2](../infrastructure/exllamav2.md) — Fast inference engine for local LLMs.
- [Gemma 3](../ai_knowledge/local_llms.md) — Canonical guide for the Gemma 3 model family.
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — The underlying protocol for tool extension.

## Sources / References
- [GitHub Repository](https://github.com/AlexsJones/llmfit)
- [Official Website](https://llmfit.axjns.dev/)
- [Release Notes v0.9.30](https://github.com/AlexsJones/llmfit/releases/tag/v0.9.30)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
