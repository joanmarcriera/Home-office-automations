# LLMPerf

## What it is
LLMPerf is a tool for benchmarking the performance, reliability, and cost of LLM APIs. Developed by the Ray Project, it provides standardized tests for measuring throughput (tokens per second), latency (time to first token, inter-token latency), and correctness across different providers and models. It leverages [Ray](https://www.ray.io/) to parallelize requests and simulate high-concurrency workloads.

## What problem it solves
Enables objective comparison of LLM API providers on operational metrics rather than just model quality. In a production environment, factors like speed, cost-per-token, and "time to first token" are critical for user experience. LLMPerf helps engineers make informed decisions about provider selection and capacity planning by providing reproducible performance data.

## Where it fits in the stack
**Benchmarking**. Used to measure and compare the operational performance of LLM inference endpoints (SaaS or self-hosted).

## Typical use cases
- **Provider Comparison**: Comparing throughput and latency between OpenAI, Anthropic, and open-source models hosted on TogetherAI or Anyscale.
- **Capacity Planning**: Determining how many concurrent requests an endpoint can handle before performance degrades significantly.
- **Regression Testing**: Establishing performance baselines before and after infrastructure changes or model version updates.
- **SLA Verification**: Ensuring that a third-party provider is meeting its advertised performance targets.

## Strengths
- **Standardized Methodology**: Uses a consistent prompt format (streaming randomly sampled lines from Shakespeare) to ensure fair comparison.
- **High Concurrency**: Built on Ray, allowing it to easily scale to thousands of concurrent requests.
- **Broad Provider Support**: Integrates with OpenAI, Anthropic, Vertex AI, SageMaker, and any provider supported by [LiteLLM](../../services/litellm.md).
- **Comprehensive Metrics**: Reports mean/stddev for input/output tokens, TTFT (Time To First Token), and total throughput.

## Limitations
- **API Focused**: Primarily designed for API-based providers; while it can hit local endpoints (via OpenAI-compatible APIs), it doesn't measure local hardware utilization directly.
- **Network Dependency**: Results are heavily influenced by the network conditions between the client running LLMPerf and the API endpoint.
- **No Quality Metrics**: Focuses on performance and basic correctness; it does not evaluate reasoning depth or nuance (use [HumanEval](human-eval.md) or [MMLU](mmlu.md) for that).

## When to use it
- When selecting an LLM API provider for a latency-sensitive application.
- When benchmarking the performance of a self-hosted inference server (e.g., [vLLM](../infrastructure/vllm.md)).
- When you need to simulate realistic user load on an LLM endpoint.

## When not to use it
- When evaluating the *quality* of model responses (use [HLE](humanitys-last-exam.md) instead).
- When benchmarking local model execution speed on a single device without an API layer (use [Ollama Benchmark](ollama-benchmark-cli.md) instead).

## Getting started (CLI Examples)

### Installation
```bash
git clone https://github.com/ray-project/llmperf.git
cd llmperf
pip install -e .
```

### Running a Load Test
To measure throughput and latency for an OpenAI-compatible API:

```bash
export OPENAI_API_KEY="your_key"
export OPENAI_API_BASE="https://api.openai.com/v1"

python token_benchmark_ray.py \
    --model "gpt-4o" \
    --mean-input-tokens 550 \
    --stddev-input-tokens 150 \
    --mean-output-tokens 150 \
    --stddev-output-tokens 10 \
    --num-concurrent-requests 5 \
    --max-num-completed-requests 20 \
    --llm-api openai \
    --results-dir "results"
```

### Running a Correctness Test
To verify that a model can perform simple tasks accurately under load:

```bash
python llm_correctness.py \
    --model "gpt-4o" \
    --max-num-completed-requests 10 \
    --num-concurrent-requests 2 \
    --results-dir "correctness_results"
```

## Related tools / concepts

- [Ollama Benchmark](ollama-benchmark-cli.md) - Benchmarking local models.
- [LiteLLM](../../services/litellm.md) - Universal proxy used by LLMPerf for multi-provider support.
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md) - High-level evaluation framework.
- [SWE-bench](swe-bench.md) - Software engineering benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Framework for model quality benchmarks.
- [vLLM](../infrastructure/vllm.md) - High-throughput inference engine often benchmarked by LLMPerf.
- [HumanEval](human-eval.md) - Code generation benchmark.
- [MMLU](mmlu.md) - General knowledge benchmark.

## Sources / references
- [LLMPerf GitHub Repository](https://github.com/ray-project/llmperf)
- [Ray Project Documentation](https://docs.ray.io/en/latest/ray-overview/index.html)
- [LiteLLM Provider Documentation](https://docs.litellm.ai/docs/providers)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
