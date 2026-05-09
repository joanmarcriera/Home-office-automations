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

**Windows (Scoop)**
```bash
scoop install llmfit
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

```bash
# Classic table output in the terminal
llmfit --cli

# Top recommendations in JSON format (ideal for agents)
llmfit recommend --json --limit 5

# Filter recommendations by use case
llmfit recommend --use-case coding --limit 3

# Display detected system hardware specs
llmfit system --json
```

## TUI Interaction
The TUI is the primary way to interact with `llmfit`. Keybindings include:
- `p`: **Plan Mode** — Estimates hardware needed for a specific model/context size.
- `S`: **Simulation** — Overrides detected RAM/VRAM to see what *would* fit on different hardware.
- `D`: **Download Manager** — Manage GGUF downloads and history.
- `b`: **Community Benchmarks** — View real-world performance data from [localmaxxing.com](https://localmaxxing.com/).
- `f`: Cycle fit filters (Runnable, Perfect, Good, etc.).

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
- Last reviewed: 2026-05-08
- Confidence: high
