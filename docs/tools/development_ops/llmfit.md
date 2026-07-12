# llmfit

## What it is
llmfit is a hardware-to-model fit utility that helps you determine which models and providers are realistic for your machine, now updated with support for **July 2026** hardware and model releases including [Gemma 3](../ai_knowledge/local_llms.md) and [Claude 5.1](../ai_knowledge/claude.md).

## What problem it solves
It prevents wasted time trying to run models that do not fit your hardware or performance requirements. It provides instant feasibility checks for the latest frontier and local models.

## Where it fits in the stack
**Development & Ops / Model Selection Utility**. It is a planning tool for local AI deployment decisions and [MCP 3.0](../../knowledge_base/mcp.md) task protocol resource allocation.

## Typical use cases
- Choosing models for local inference (e.g., deciding between [Gemma 3](../ai_knowledge/local_llms.md) 4B or 27B).
- Comparing what can run on different hardware profiles.
- Deciding whether to use LocalAI, Ollama, or a cloud provider.
- Benchmarking [MCP](../../knowledge_base/mcp.md) server overhead on local hardware.

## Strengths
- **Fast Hardware Reality Check**: Instantly detects CPU, RAM, and GPU/VRAM to provide tailored model recommendations.
- **Vim-like TUI**: Powerful interactive interface with search, filtering, and bulk comparison modes.
- **Community Benchmarks**: Integration with [localmaxxing.com](https://localmaxxing.com) (press `b`) to see real-world performance data from other users.
- **Hardware Simulation**: Press `S` to override your system specs and see what models would run on a target upgrade (e.g., RTX 6090).
- **Download Manager**: Native management of model downloads and local cache for Ollama, llama.cpp, and LM Studio.
- **Protocol Awareness**: Support for estimating memory overhead of [MCP 3.0](../../knowledge_base/mcp.md) Task Protocol runtimes.

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
# or
pip install llmfit
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
- **Navigation**: `j/k` or arrows.
- **Search**: `/` to search by name, provider, or use case.
- **Filters**: `f` (fit), `a` (availability), `R` (runtime).
- **Leaderboard**: `b` to view community benchmarks.
- **Plan Mode**: `p` to calculate hardware requirements for a specific model.

### System Audit
```bash
# Display detected system hardware specs in JSON format
llmfit system --json
```

### Model Recommendations
```bash
# Get top 5 recommendations for coding in JSON format
llmfit recommend --use-case coding --limit 5 --json
```

### Hardware Planning
```bash
# Estimate required hardware for a specific model and context length
llmfit plan "google/gemma-3-27b-it" --context 32768 --json
```

## API examples
llmfit can run as a background service to provide fit data via a REST API or integrate directly as an **OpenClaw Skill**.

### Starting the Server
```bash
llmfit serve --host 0.0.0.0 --port 8787
```

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

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LM Studio](../infrastructure/lm-studio.md)
- [LocalAI](../infrastructure/localai.md)
- [vLLM](../infrastructure/vllm.md)
- [llama.cpp](../infrastructure/llama-cpp.md)
- [MLX](../infrastructure/mlx.md)
- [ExLlamaV2](../infrastructure/exllamav2.md)
- [MCP 3.0](../../knowledge_base/mcp.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Claude 5.1](../ai_knowledge/claude.md)

## Sources / References
- [GitHub Repository](https://github.com/AlexsJones/llmfit)
- [Official Website](https://llmfit.axjns.dev/)
- [Release Notes v1.0.5](https://github.com/AlexsJones/llmfit/releases)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
