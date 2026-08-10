# LLMPerf

## What it is
LLMPerf is an open-source benchmarking framework designed to evaluate the performance, latency, reliability, and cost-efficiency of Large Language Model (LLM) APIs under highly concurrent workloads. Originally developed by the Ray Project, it conducts rigorous multi-user load testing to measure operational performance. In December 2026, it is widely utilized to benchmark agentic concurrency metrics (e.g., "Agentic TPS") across federated cloud endpoints and high-throughput local serving infrastructures.

## What problem it solves
Raw reasoning benchmarks (e.g., Humanity's Last Exam) measure intellectual accuracy, but fail to capture operational performance. For low-latency multi-agent systems and real-time assistants, factors like Time to First Token (TTFT), inter-token latency (ITL), and end-to-end response duration are critical for usability and budget management. LLMPerf solves this by establishing consistent, parallelized, and reproducible load tests, helping engineers detect capacity degradation, configure autoscaling, and verify Service Level Agreements (SLAs).

## Where it fits in the stack
**Benchmarking & Telemetry Layer**. It operates as an external, multi-threaded load generator that stresses model serving endpoints (hosted in-house on engines like [vLLM](../infrastructure/vllm.md) or accessed via cloud providers like OpenAI and Anthropic). It leverages Ray's distributed actor architecture to parallelize requests.

## Typical use cases
- **Endpoint Load Testing**: Testing how TTFT degrades when the number of concurrent user sessions spikes from 10 to 100.
- **Provider SLA Validation**: Running structured tests across [LiteLLM](../../services/litellm.md) to compare Anthropic's Claude 5.1 Sonnet against OpenAI's GPT-5.5 for real-time chat latency.
- **Serving Engine Optimization**: Benchmarking local deployment configurations (e.g., vLLM chunked prefill or FP8 quantization) to find optimal concurrency levels.
- **Tool-Call Concurrency Audits**: Simulating high-concurrency tool-calling sessions using the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) to measure gateway delay.

## Strengths
- **Massive Scalability**: Leverages Ray to distribute concurrent clients across multiple worker nodes, simulating thousands of parallel users.
- **Standardized Methodology**: Employs streaming clients that extract token timings (TTFT, inter-token time) uniformly without provider bias.
- **Rich Metric Reporting**: Generates statistics for throughput (tokens/sec), latency percentiles (P50, P90, P99), and success/error ratios.
- **Extensible Architecture**: Highly customizable client templates that integrate smoothly with any OpenAI-compatible API base.

## Limitations
- **Operational Metrics Only**: Measures speed and volume, but does not analyze correctness, alignment, or semantic quality (pair with [LM Evaluation Harness](lm-evaluation-harness.md) for quality).
- **Network Dependency**: Client-side benchmarking results are heavily affected by network routes; tests must be conducted from inside the same private cloud/homelab mesh for pure engine benchmarks.
- **Resource Intensive**: Running distributed Ray clusters for high-concurrency testing requires significant computing resources.

## When to use it
- When evaluating and comparing cloud API performance under peak load.
- When benchmarking custom-tuned open-weight models (e.g., Qwen 3.6 or Llama 4) on self-hosted vLLM or sglang servers.
- Before launching production-grade multi-agent swarms to verify your infrastructure can handle the concurrent generation load.

## When not to use it
- When you only want to measure reasoning or math capability (use [Humanity's Last Exam](humanitys-last-exam.md) instead).
- When benchmarking local model speed on a single thread/user with direct hardware access (use [Ollama Benchmark](ollama-benchmark-cli.md) instead).

## Getting started

### 1. Set Up the Environment
Install Ray and the LLMPerf dependencies inside a virtual environment:
```bash
git clone https://github.com/ray-project/llmperf.git
cd llmperf
pip install -e .
```

### 2. Configure Credentials
Set your target API keys and base URLs:
```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_API_BASE="https://api.openai.com/v1"
```

## CLI examples

### Running a Throughput Load Test
Use the standard test script to simulate 15 concurrent users querying a frontier model like GPT-5.5:
```bash
python token_benchmark_ray.py \
    --model "gpt-5.5-preview" \
    --mean-input-tokens 1024 \
    --stddev-input-tokens 128 \
    --mean-output-tokens 256 \
    --stddev-output-tokens 32 \
    --num-concurrent-requests 15 \
    --max-num-completed-requests 150 \
    --llm-api openai \
    --results-dir "./results"
```

### Benchmarking Local vLLM Server Concurrency
Stress-test a local Qwen 3.6 instance hosted on a private vLLM node:
```bash
python token_benchmark_ray.py \
    --model "qwen-3.6-72b-instruct" \
    --mean-input-tokens 500 \
    --stddev-input-tokens 50 \
    --mean-output-tokens 150 \
    --stddev-output-tokens 10 \
    --num-concurrent-requests 30 \
    --max-num-completed-requests 300 \
    --llm-api openai \
    --additional-extra-headers '{"Authorization": "Bearer local-secret-token"}' \
    --results-dir "./local_vllm_results"
```

## API examples

### Python: Validating and Summarizing LLMPerf Results with Pydantic v2
This script demonstrates how to parse and validate LLMPerf output logs using Pydantic v2 to programmatically enforce quality gates on model performance.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, conint, confloat

# 1. Define LLMPerf output schema using Pydantic v2
class LatencyPercentiles(BaseModel):
    p50: confloat(gt=0.0) = Field(..., alias="P50")
    p90: confloat(gt=0.0) = Field(..., alias="P90")
    p99: confloat(gt=0.0) = Field(..., alias="P99")

class BenchmarkMetadata(BaseModel):
    model_name: str = Field(..., description="Canonical ID of the benchmarked model")
    concurrency: conint(gt=0) = Field(..., description="Number of parallel clients simulated")
    total_requests: int = Field(..., description="Total completed requests in this run")

class LLMPerfMetrics(BaseModel):
    metadata: BenchmarkMetadata
    mean_ttft_seconds: confloat(gt=0.0) = Field(..., description="Mean time-to-first-token in seconds")
    mean_itl_seconds: confloat(gt=0.0) = Field(..., description="Mean inter-token latency in seconds")
    tokens_per_second: confloat(gt=0.0) = Field(..., description="Overall token throughput")
    percentiles: LatencyPercentiles
    error_rate: confloat(ge=0.0, le=1.0) = Field(default=0.0, description="Fraction of requests that failed")

# 2. Performance Evaluation logic
def evaluate_serving_sla(metrics: LLMPerfMetrics) -> bool:
    print(f"Evaluating performance metrics for {metrics.metadata.model_name}...")
    print(f"Throughput: {metrics.tokens_per_second:.2f} tok/s | Mean TTFT: {metrics.mean_ttft_seconds:.3f}s")

    # SLA threshold assertions:
    # Let's say we require TTFT < 0.6 seconds and ITL < 0.05 seconds under load.
    sla_ttft_ok = metrics.mean_ttft_seconds < 0.6
    sla_itl_ok = metrics.mean_itl_seconds < 0.05
    sla_errors_ok = metrics.error_rate < 0.01

    if sla_ttft_ok and sla_itl_ok and sla_errors_ok:
        print("RESULT: Endpoint performance meets homelab SLA targets.")
        return True
    else:
        print("RESULT: Endpoint performance failed to meet SLA targets.")
        print(f"Violations: TTFT_OK={sla_ttft_ok}, ITL_OK={sla_itl_ok}, Errors_OK={sla_errors_ok}")
        return False

if __name__ == "__main__":
    # Mock output log from an LLMPerf run
    mock_run_log = {
        "metadata": {
            "model_name": "claude-5.1-sonnet",
            "concurrency": 25,
            "total_requests": 200
        },
        "mean_ttft_seconds": 0.421,
        "mean_itl_seconds": 0.032,
        "tokens_per_second": 842.1,
        "percentiles": {
            "P50": 0.410,
            "P90": 0.520,
            "P99": 0.730
        },
        "error_rate": 0.005
    }

    # Validate output schema
    metrics = LLMPerfMetrics.model_validate(mock_run_log)

    # Execute SLA verification
    passed = evaluate_serving_sla(metrics)
    assert passed is True, "Performance evaluation did not pass!"
```

## Related tools / concepts
- [Ollama Benchmark](ollama-benchmark-cli.md) — Fast local-only hardware benchmarking utility.
- [LiteLLM](../../services/litellm.md) — Load balancer proxy supporting model orchestration and fallbacks.
- [LM Evaluation Harness](lm-evaluation-harness.md) — Standardized framework for evaluating reasoning and content quality.
- [vLLM](../infrastructure/vllm.md) — High-throughput open-weights serving engine.
- [Humanity's Last Exam](humanitys-last-exam.md) — SOTA reasoning capability evaluation benchmark.
- [MBPP](mbpp.md) — Coding benchmark for Python execution.
- [PA-bench](pa-bench.md) — Personal assistant and orchestration benchmark.
- [DREAM](dream.md) — Advanced evaluation metrics for multi-agent loops.

## Sources / references
- [LLMPerf GitHub Repository](https://github.com/ray-project/llmperf)
- [Ray Core Distributed Framework Docs](https://docs.ray.io/en/latest/)
- [LiteLLM Benchmarking Integration Guides](https://docs.litellm.ai/docs/proxy/benchmarking)
- [High-Throughput Serving Standards Q4 2026 Whitepaper](https://example.com/serving-standards-2026)

## Contribution Metadata
- Last reviewed: 2026-12-30
- Confidence: high
