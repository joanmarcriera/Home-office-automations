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

## Related tools / concepts
- [LLMPerf](llmperf.md)
- [Simple `time` command with `curl`](https://ollama.com/docs/api)

## Sources / references
- [GitHub Repository](https://github.com/marwanjeridi/ollama-benchmark) (Example implementation)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
