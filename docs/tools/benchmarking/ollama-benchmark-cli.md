# Ollama Benchmark CLI

## What it is
Ollama Benchmark CLI is a specialized tool for measuring the local inference performance of Large Language Models (LLMs) served via [Ollama](../../services/ollama.md). It provides rigorous, low-level metrics for tokens-per-second (TPS), latency, and processing times, enabling developers to objectively compare model performance on their specific local hardware (such as Apple Silicon, multi-GPU rigs, and custom ARM64 nodes). In late November/December 2026, it serves as the standard for validating local "Agentic Latency"—the precise execution time of multi-step, local reasoning and FastMCP 3.1 tool calls.

## What problem it solves
Hardware configurations for local LLMs are highly diverse and unpredictable. Running model reasoning loops locally requires finding the correct sweet spot between generation speed and comprehension. Ollama Benchmark CLI provides a standardized mechanism to benchmark "Prompt Processing Speed" (prefill) and "Token Generation Speed" (decoding). This helps builders select the optimal quantization level, model size (e.g., `llama4:8b` vs `llama4:70b`), and context limits to support smooth, real-time agent execution without hitting memory bottlenecks.

## Where it fits in the stack
**Benchmarking**. Used for local infrastructure performance audits, specifically for models running on top of local services. It sits alongside [LLMPerf](llmperf.md) but specializes in isolated, serverless, or on-premises environments.

## Typical use cases
- **Quantization Optimization**: Benchmarking performance differences across different GGUF precision levels (e.g., `q4_K_M` vs `q8_0`) to maximize local TPS.
- **Hardware Integration Tests**: Measuring performance gains from thermal cooling upgrades, multi-GPU configurations, or CUDA/ROCm updates.
- **Agentic Latency Auditing**: Testing TTFT (Time To First Token) for complex agentic system prompts on local models (such as Gemma 3, Qwen 3.6, and Llama 4).
- **Stress-Testing and Thermal Throttling**: Running high-load loops for extended periods to measure hardware degradation or performance throttling under sustained compute demands.

## Strengths
- **Native Integration**: Directly targets the Ollama REST API endpoints, requiring no complex driver wrappers.
- **Granular Latency Parsing**: Explicitly separates prefill (prompt loading) from generation phase metrics.
- **Batch Comparisons**: Supports evaluating multiple local models in a single, automated execution run with structured comparison tables.

## Limitations
- **Ollama Specific**: Cannot evaluate raw engines like vLLM, Aphrodite, or llama.cpp directly unless they are wrapped in an Ollama-compatible interface.
- **No Qualitative Evaluation**: Only measures processing speed; it does not check if the model's response is accurate or contextually sound (use [HLE](humanitys-last-exam.md) or [LM Evaluation Harness](lm-evaluation-harness.md) for quality evaluations).
- **Environment Dependency**: Results are tightly coupled with the host hardware state (e.g., CPU load, GPU temperature) and cannot be compared across systems without strict environment controls.

## When to use it
- When provisioning or tuning local homelab nodes in late November/December 2026 to run low-latency local agents.
- When validating the execution throughput of local model pools hosting FastMCP 3.1 tool-calling frameworks.
- When testing hardware efficiency during model quantization swaps.

## When not to use it
- For cloud-based model providers (use [LLMPerf](llmperf.md)).
- For qualitative reasoning or capability validation (use [LM Evaluation Harness](lm-evaluation-harness.md)).

## Getting started
Installation is straightforward via standard Python package managers. Ensure the local Ollama service is active before running evaluations.

```bash
pip install git+https://github.com/LarHope/ollama-benchmark.git
```

For multi-GPU local systems, configure Ollama with GPU-specific parameters before benchmarking:
```bash
# Example CUDA configuration for parallel GPUs in late 2026
export CUDA_VISIBLE_DEVICES=0,1
export OLLAMA_NUM_PARALLEL=4
```

## CLI examples

### Benchmarking specific models with comparison table
```bash
ollama-benchmark --models llama4:8b deepseek-r1:32b --table_output
```

### Benchmarking with context limits and thread controls
Specify custom context window limits and thread counts to mirror the active late 2026 agent environments:
```bash
ollama-benchmark \
    --models gemma3:9b \
    --num_ctx 16384 \
    --num_thread 8 \
    --output-json ./metrics/gemma3_stats.json
```

### Benchmarking with custom prompt sequences
```bash
ollama-benchmark --models qwen3.6-instruct --prompts "Explain quantum computing" "Write a fast Fibonacci in Python"
```

## API examples

### Parsing and Validating Ollama Benchmarks with Strict Pydantic v2
This Python script demonstrates how to query the Ollama local API and parse execution metrics using strict **Pydantic v2** validation (`BaseModel`, `Field`, `model_validate`, `ValidationError`).

```python
import sys
import requests
from pydantic import BaseModel, Field, ValidationError

# Define strict metric validation structures in Pydantic v2
class BenchmarkOptions(BaseModel):
    num_ctx: int = Field(default=8192, description="Context window size used for test")
    temperature: float = Field(default=0.0, description="Temperature parameter")
    num_predict: int = Field(default=512, description="Max tokens to predict")

class BenchmarkResult(BaseModel):
    model: str = Field(..., description="The name of the benchmarked model")
    prompt_tokens: int = Field(..., alias="prompt_eval_count", description="Number of tokens in prompt")
    prefill_duration_ns: int = Field(..., alias="prompt_eval_duration", description="Time spent in prefill (ns)")
    generation_tokens: int = Field(..., alias="eval_count", description="Number of tokens generated")
    generation_duration_ns: int = Field(..., alias="eval_duration", description="Time spent in token generation (ns)")
    total_duration_ns: int = Field(..., alias="total_duration", description="Total API response duration in ns")

    # Property helpers to compute human-readable speeds
    @property
    def prefill_tps(self) -> float:
        if self.prefill_duration_ns > 0:
            return self.prompt_tokens / (self.prefill_duration_ns / 1e9)
        return 0.0

    @property
    def generation_tps(self) -> float:
        if self.generation_duration_ns > 0:
            return self.generation_tokens / (self.generation_duration_ns / 1e9)
        return 0.0

def run_local_benchmark(model_name: str, prompt: str, options: BenchmarkOptions) -> None:
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": options.model_dump()
    }

    print(f"Running benchmark on model '{model_name}'...")
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        raw_data = response.json()

        # Validate with Pydantic V2 model_validate
        metrics = BenchmarkResult.model_validate(raw_data)

        print("📊 Benchmark Metrics Verified:")
        print(f"  - Model: {metrics.model}")
        print(f"  - Prefill Speed: {metrics.prefill_tps:.2f} tokens/sec ({metrics.prompt_tokens} tokens)")
        print(f"  - Generation Speed: {metrics.generation_tps:.2f} tokens/sec ({metrics.generation_tokens} tokens)")
        print(f"  - Total Latency: {raw_data.get('total_duration', 0) / 1e9:.2f} seconds")

    except ValidationError as ve:
        print(f"❌ Metrics validation error: {ve}", file=sys.stderr)
    except requests.RequestException as re:
        print(f"❌ HTTP request failed: {re}", file=sys.stderr)

if __name__ == "__main__":
    # Ensure options are validated
    test_options = BenchmarkOptions(num_ctx=4096, temperature=0.0)

    # Mock a manual metrics dictionary validation for testing when service is offline
    mock_payload = {
        "model": "llama4:8b",
        "prompt_eval_count": 120,
        "prompt_eval_duration": 480000000,   # 0.48s (250 tps)
        "eval_count": 300,
        "eval_duration": 4000000000,         # 4.0s (75 tps)
        "total_duration": 4500000000
    }

    try:
        validated_metrics = BenchmarkResult.model_validate(mock_payload)
        print(f"✅ Offline validation check successful for model: {validated_metrics.model}")
        print(f"  Prefill TPS: {validated_metrics.prefill_tps:.2f}")
        print(f"  Generation TPS: {validated_metrics.generation_tps:.2f}")
    except ValidationError as e:
        print(f"❌ Offline validation check failed: {e}", file=sys.stderr)
```

## Related tools / concepts
- [Ollama Service](../../services/ollama.md) - The underlying model server.
- [LLMPerf](llmperf.md) - Benchmarking API-based LLM performance.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Benchmarking model quality/accuracy.
- [HLE (Humanity's Last Exam)](humanitys-last-exam.md) - Frontier reasoning benchmark.
- [MBPP](mbpp.md) - Code generation benchmark for Python.
- [vLLM](../infrastructure/vllm.md) - High-performance inference server.
- [Aphrodite Engine](../infrastructure/aphrodite-engine.md) - High-throughput local inference engine.
- [Terminus 2](terminal-bench.md) - Benchmarking terminal-based agent interactions.

## Sources / References
- [LarHope/ollama-benchmark GitHub Repository](https://github.com/LarHope/ollama-benchmark)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Local LLM Performance Leaderboard (2026)](https://example.com/local-llm-bench)
- [BetterBench: Accurate PP and TPS Measurements](https://www.reddit.com/r/LocalLLaMA/comments/1vgrii0/introducing_betterbench_more_accurate_pp_and_tps/)

- Last reviewed: 2026-12-30
- Confidence: high
