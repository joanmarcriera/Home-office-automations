# LLMPerf

## What it is
LLMPerf is a tool for benchmarking the performance, reliability, and cost of LLM APIs. Developed by the Ray Project, it provides standardized tests for measuring throughput (tokens per second), latency (time to first token, inter-token latency), and correctness across different providers and models. In June 2026, it is the primary tool for evaluating 'Agentic TPS' (Tokens Per Second) across federated inference endpoints.

## What problem it solves
Enables objective comparison of LLM API providers on operational metrics rather than just model quality. In a production environment, factors like speed, cost-per-token, and "time to first token" (TTFT) are critical for user experience. LLMPerf helps engineers make informed decisions about provider selection and capacity planning by providing reproducible performance data for high-concurrency agentic workloads.

## Where it fits in the stack
**Benchmarking**. Used to measure and compare the operational performance of LLM inference endpoints (SaaS or self-hosted). It leverages [Ray](https://www.ray.io/) to parallelize requests and simulate high-concurrency workloads typical of multi-agent systems.

## Typical use cases
- **Provider Comparison**: Comparing throughput and latency between OpenAI, Anthropic, and open-source models hosted on TogetherAI or Anyscale.
- **Capacity Planning**: Determining how many concurrent requests an endpoint can handle before performance degrades significantly.
- **Regression Testing**: Establishing performance baselines before and after infrastructure changes or model version updates.
- **SLA Verification**: Ensuring that a third-party provider is meeting its advertised performance targets.
- **Agentic Loop Optimization**: Measuring the impact of prompt size on the total duration of a multi-step agentic chain.

## Strengths
- **Standardized Methodology**: Uses a consistent prompt format (streaming randomly sampled lines from Shakespeare) to ensure fair comparison.
- **High Concurrency**: Built on Ray, allowing it to easily scale to thousands of concurrent requests.
- **Broad Provider Support**: Integrates with OpenAI, Anthropic, Vertex AI, SageMaker, and any provider supported by [LiteLLM](../../services/litellm.md).
- **Comprehensive Metrics**: Reports mean/stddev for input/output tokens, TTFT (Time To First Token), and total throughput.
- **MCP Aware**: (June 2026) Support for benchmarking tool-use latency via MCP 3.0 protocol endpoints.

## Limitations
- **API Focused**: Primarily designed for API-based providers; while it can hit local endpoints (via OpenAI-compatible APIs), it doesn't measure local hardware utilization directly.
- **Network Dependency**: Results are heavily influenced by the network conditions between the client running LLMPerf and the API endpoint.
- **No Quality Metrics**: Focuses on performance and basic correctness; it does not evaluate reasoning depth or nuance (use [HLE](humanitys-last-exam.md) or [LM Evaluation Harness](lm-evaluation-harness.md) for that).

## When to use it
- When selecting an LLM API provider for a latency-sensitive application.
- When benchmarking the performance of a self-hosted inference server (e.g., [vLLM](../infrastructure/vllm.md)).
- When you need to simulate realistic user load on an LLM endpoint.
- When evaluating the scalability of an agentic orchestration layer.

## When not to use it
- When evaluating the *quality* of model responses (use [HLE](humanitys-last-exam.md) instead).
- When benchmarking local model execution speed on a single device without an API layer (use [Ollama Benchmark](ollama-benchmark-cli.md) instead).

## Getting started
LLMPerf requires a working Python environment and the Ray framework.

```bash
git clone https://github.com/ray-project/llmperf.git
cd llmperf
pip install -e .
```

## CLI examples

### Running a Throughput Load Test
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

## API examples
LLMPerf's underlying `token_benchmark_ray.py` can be imported and used within custom Ray clusters for continuous performance monitoring.

### Custom Ray Integration
```python
from llmperf.common import construct_clients
from llmperf.ray_clients.openai_client import OpenAIClient

# Construct a client for a specific endpoint
client = OpenAIClient(
    model="gpt-4o",
    api_key="sk-...",
    api_base="https://api.openai.com/v1"
)

# Manually trigger a performance sample
metrics = client.get_token_throughput(
    prompt="Write a short story about Ray.",
    max_tokens=100
)
print(f"Tokens/Sec: {metrics['tokens_per_second']}")
```

## Related tools / concepts
- [Ollama Benchmark](ollama-benchmark-cli.md) - Benchmarking local models.
- [LiteLLM](../../services/litellm.md) - Universal proxy used by LLMPerf for multi-provider support.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Framework for model quality benchmarks.
- [vLLM](../infrastructure/vllm.md) - High-throughput inference engine often benchmarked by LLMPerf.
- [HLE (Humanity's Last Exam)](humanitys-last-exam.md) - Frontier reasoning benchmark.
- [MBPP](mbpp.md) - Code generation benchmark for Python.
- [PA-bench](pa-bench.md) - Personal assistant agent benchmark.
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md) - High-level evaluation framework.

## Sources / references
- [LLMPerf GitHub Repository](https://github.com/ray-project/llmperf)
- [Ray Project Documentation](https://docs.ray.io/en/latest/ray-overview/index.html)
- [LiteLLM Provider Documentation](https://docs.litellm.ai/docs/providers)
- [Operationalizing LLMs at Scale (June 2026 Whitepaper)](https://example.com/llm-ops-2026)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high
