# LLMPerf

## What it is
LLMPerf is a tool for benchmarking the performance and cost of LLM APIs. It provides standardized tests for measuring throughput, latency, and cost across different providers and models.

## What problem it solves
Enables objective comparison of LLM API providers on operational metrics (speed, cost, reliability) rather than just model quality, helping inform deployment and provider selection decisions.

## Where it fits in the stack
**Benchmarking**. Used to measure and compare the operational performance of LLM inference endpoints.

## Typical use cases
- Comparing throughput and latency across different LLM API providers
- Measuring cost-per-token for different models and providers
- Establishing performance baselines before and after infrastructure changes

## Strengths
- Standardized testing methodology for fair provider comparison
- Measures practical operational metrics (latency, throughput, cost)
- Open source and extensible

## Limitations
- Focused on API-based providers; local inference requires different tooling
- Results vary based on network conditions and API load
- Does not measure model quality, only serving performance

## When to use it
- When selecting between LLM API providers based on performance and cost
- When monitoring API performance over time

## When not to use it
- When benchmarking local model inference (use [Ollama Benchmark](ollama-benchmark-cli.md) instead)
- When evaluating model quality or accuracy

## Related tools / concepts
- [Ollama Benchmark](ollama-benchmark-cli.md)
- [LiteLLM (Cost tracking features)](../../services/litellm.md)

## Sources / references
- [GitHub Repository](https://github.com/ray-project/llmperf)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
