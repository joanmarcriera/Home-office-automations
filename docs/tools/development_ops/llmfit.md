# llmfit

## What it is
llmfit is a hardware-to-model fit utility that helps you determine which models and providers are realistic for your machine.

## What problem it solves
It prevents wasted time trying to run models that do not fit your hardware or performance requirements.

## Where it fits in the stack
**Development & Ops / Model Selection Utility**. It is a planning tool for local AI deployment decisions.

## Typical use cases
- Choosing models for local inference
- Comparing what can run on different hardware profiles
- Deciding whether to use LocalAI, Ollama, or a cloud provider

## Strengths
- Fast hardware reality check
- Useful before investing in local inference setup

## Limitations
- It helps with feasibility, not workload design
- It does not choose the right workflow architecture for you

## When to use it
- Before standing up local model infrastructure

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
Simply type `llmfit` to launch the interactive TUI. As of v0.9.30, it features a new Vim-like TUI for improved navigation. It will automatically detect your CPU, RAM, and GPU/VRAM (including support for Apple M5 silicon) to provide tailored recommendations.

## CLI examples

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
llmfit plan "meta-llama/Llama-3.1-8B" --context 8192 --json
```

## API examples
llmfit can run as a background service to provide fit data via a REST API.

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

## When not to use it
- When you already know you will use hosted frontier APIs (OpenAI, Anthropic, etc.) and have no interest in local execution.
- If you require a tool that actually benchmarks the model on your hardware by running it (see `llm-checker`).

## Related tools / concepts
- [Ollama](../../services/ollama.md)
- [LM Studio](../infrastructure/lm-studio.md)
- [LocalAI](../infrastructure/localai.md)
- [vLLM](../infrastructure/vllm.md)
- [llama.cpp](../infrastructure/llama-cpp.md)
- [MLX](../infrastructure/mlx.md)
- [ExLlamaV2](../infrastructure/exllamav2.md)

## Sources / References
- [GitHub Repository](https://github.com/AlexsJones/llmfit)
- [Official Website](https://llmfit.axjns.dev/)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
