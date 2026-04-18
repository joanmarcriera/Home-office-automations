# Ollama Benchmark CLI

## What it is
Ollama Benchmark CLI is a tool for benchmarking local models running on Ollama. It measures tokens-per-second and response latency for different models on your specific hardware.

## What problem it solves
Provides a quick way to measure and compare the inference performance of different models running locally on Ollama, helping identify the best model-hardware configuration for your setup.

## Where it fits in the stack
**Benchmarking**. Used to measure local LLM inference performance on Ollama-hosted models.

## Typical use cases
- Measuring tokens-per-second for different models on local hardware
- Comparing inference latency across model sizes and quantization levels
- Establishing performance baselines after hardware changes

## Strengths
- Directly measures performance on your actual hardware
- Simple to use with existing Ollama installations
- Provides practical metrics (tokens/second, latency) relevant to daily use

## Limitations
- Specific to Ollama; cannot benchmark other inference backends directly
- Results are hardware-dependent and not comparable across different machines
- Limited to inference performance; does not measure model quality

## When to use it
- When selecting which model to run locally based on performance constraints
- When evaluating the impact of hardware upgrades on inference speed

## When not to use it
- When benchmarking cloud API providers (use [LLMPerf](llmperf.md) instead)
- When evaluating model accuracy or quality

## Lightweight Alternative: `time` + `curl`
If you don't want to install a dedicated benchmarking tool, you can get basic latency and throughput metrics using the standard `time` command and `curl`. This is useful for quick checks or when working on a remote server with minimal tools.

```bash
time curl -X POST http://localhost:11434/api/generate \
  -d '{
    "model": "llama3",
    "prompt": "Why is the sky blue?",
    "stream": false
  }'
```

The output will show the total execution time. You can calculate tokens per second by dividing the `total_duration` (returned in the JSON response) by the number of tokens generated.

## Related tools / concepts

- [LLMPerf](llmperf.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [Simple `time` command with `curl`](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [SWE-bench](swe-bench.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
## Sources / references
- [GitHub Repository](https://github.com/marwanjeridi/ollama-benchmark) (Example implementation)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
