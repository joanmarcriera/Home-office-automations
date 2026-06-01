# Ollama Benchmark CLI

## What it is
Ollama Benchmark CLI is a specialized tool for measuring the inference performance of local LLMs running on [Ollama](../../services/ollama.md). It provides detailed metrics for tokens-per-second (TPS), latency, and processing times, allowing users to objectively compare how different models perform on their specific hardware (GPU/CPU/RAM).

## What problem it solves
Hardware performance for local LLMs is highly variable. A model that runs smoothly on a 24GB VRAM card might crawl on an integrated GPU. Ollama Benchmark CLI provides a standardized way to measure "Prompt Processing Speed" and "Generation Speed," helping users select the optimal model size and quantization level for their specific system.

## Where it fits in the stack
**Benchmarking**. Used for local infrastructure performance assessment, specifically for models managed by Ollama.

## Typical use cases
- **Model Selection**: Comparing the generation speed (tokens/sec) of `llama3:8b` vs `llama3:70b` on a specific machine.
- **Hardware Optimization**: Testing the impact of different GPU drivers or system configurations on inference latency.
- **Quantization Comparison**: Measuring the performance trade-offs between different quantization levels (e.g., `q4_K_M` vs `q8_0`).
- **Thermal Benchmarking**: Running long-duration benchmarks to see if performance throttles due to heat over time.

## Strengths
- **Native Integration**: Directly interacts with the Ollama API, no complex setup required.
- **Detailed Metrics**: Provides separate metrics for prompt processing (prefill) and token generation.
- **Comparative Output**: Supports table-based comparison of multiple models in a single run.
- **Simple CLI**: Easy to install and use with standard Python tools.

## Limitations
- **Ollama Specific**: Only benchmarks models running via Ollama; it cannot directly benchmark `vLLM` or raw `llama.cpp` without an Ollama wrapper.
- **Quality-Blind**: Measures speed only; it does not evaluate whether the model's output is actually correct or high-quality (use [HumanEval](human-eval.md) or [MMLU](mmlu.md) for that).
- **Environment Dependent**: Results are specific to the machine running the test and cannot be compared across different hardware without careful control.

## When to use it
- When you want to find the fastest model that fits comfortably on your local hardware.
- When you are troubleshooting slow inference speeds in a local homelab setup.
- When you need to provide performance data for a hardware review or comparison.

## When not to use it
- When benchmarking cloud-based API providers (use [LLMPerf](llmperf.md) instead).
- When evaluating the reasoning or knowledge of a model (use [HLE](humanitys-last-exam.md) or [LM Evaluation Harness](lm-evaluation-harness.md)).
- When you only need a one-off check (use the `time` + `curl` method described below).

## Getting started (CLI Examples)

### Installation
```bash
pip install git+https://github.com/LarHope/ollama-benchmark.git
```

### Benchmarking Specific Models
```bash
ollama-benchmark --models llama3:8b deepseek-r1:32b --table_output
```

### Benchmarking with Custom Prompts
```bash
ollama-benchmark --models mistral --prompts "Explain quantum computing" "Write a fast Fibonacci in Python"
```

### Lightweight Alternative: `time` + `curl`
For a quick check without installing tools, use the Ollama API directly:
```bash
time curl -X POST http://localhost:11434/api/generate \
  -d '{
    "model": "llama3",
    "prompt": "Why is the sky blue?",
    "stream": false
  }'
```
*Note: Calculate tokens/sec by dividing the `total_duration` from the JSON response by the number of tokens generated.*

## Related tools / concepts

- [Ollama Service](../../services/ollama.md) - The underlying model server.
- [LLMPerf](llmperf.md) - Benchmarking API-based LLM performance.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Benchmarking model quality/accuracy.
- [HLE (Humanity's Last Exam)](humanitys-last-exam.md) - Frontier reasoning benchmark.
- [MMLU](mmlu.md) - General knowledge benchmark.
- [HumanEval](human-eval.md) - Code generation benchmark.
- [vLLM](../infrastructure/index.md) - An alternative high-performance inference server.

## Sources / references
- [LarHope/ollama-benchmark GitHub Repository](https://github.com/LarHope/ollama-benchmark)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high
