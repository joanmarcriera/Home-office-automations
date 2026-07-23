# Ollama Benchmark CLI

## What it is
Ollama Benchmark CLI is a specialized tool for measuring the inference performance of local LLMs running on [Ollama](../../services/ollama.md). It provides detailed metrics for tokens-per-second (TPS), latency, and processing times, allowing users to objectively compare how different models perform on their specific hardware (GPU/CPU/RAM). In July 2026, it remains the standard for validating local 'Agentic Latency'—the speed at which a local model can process multi-step tool calls.

## What problem it solves
Hardware performance for local LLMs is highly variable. A model that runs smoothly on a 24GB VRAM card might crawl on an integrated GPU. Ollama Benchmark CLI provides a standardized way to measure "Prompt Processing Speed" and "Generation Speed," helping users select the optimal model size, context limit, and quantization level (GGUF, EXL3, AWQ, etc.) for their specific system, especially for real-time agentic workflows where response time is critical.

## Where it fits in the stack
**Benchmarking**. Used for local infrastructure performance assessment, specifically for models managed by Ollama. It sits alongside [LLMPerf](llmperf.md) but focuses exclusively on the local execution environment.

## Typical use cases
- **Model Selection**: Comparing the generation speed (tokens/sec) of `llama4:8b` vs `llama4:70b` on a specific machine.
- **Hardware Optimization**: Testing the impact of different GPU drivers, CUDA/ROCm configurations, or system settings on inference latency.
- **Quantization Comparison**: Measuring the performance trade-offs between different quantization levels (e.g., `q4_K_M` vs `q8_0`).
- **Thermal Benchmarking**: Running long-duration benchmarks to see if performance throttles due to heat over time.
- **Agentic Latency Validation**: Measuring 'Time To First Token' (TTFT) for complex system prompts used in autonomous agents.

## Strengths
- **Native Integration**: Directly interacts with the Ollama API, no complex setup required.
- **Detailed Metrics**: Provides separate metrics for prompt processing (prefill) and token generation.
- **Comparative Output**: Supports table-based comparison of multiple models in a single run.
- **Simple CLI**: Easy to install and use with standard Python tools.
- **Agent-Aware**: Includes benchmarks specifically for long-context retrieval and tool-calling latency.

## Limitations
- **Ollama Specific**: Only benchmarks models running via Ollama; it cannot directly benchmark `vLLM` or raw `llama.cpp` without an Ollama wrapper.
- **Quality-Blind**: Measures speed only; it does not evaluate whether the model's output is actually correct or high-quality (use [LM Evaluation Harness](lm-evaluation-harness.md) for that).
- **Environment Dependent**: Results are specific to the machine running the test and cannot be compared across different hardware without careful control.

## When to use it
- When you want to find the fastest model that fits comfortably on your local hardware.
- When you are troubleshooting slow inference speeds in a local homelab setup in July 2026.
- When you need to provide performance data for a hardware review or comparison.
- When optimizing a local agent's response loop.

## When not to use it
- When benchmarking cloud-based API providers (use [LLMPerf](llmperf.md) instead).
- When evaluating the reasoning or knowledge of a model (use [HLE](humanitys-last-exam.md) or [LM Evaluation Harness](lm-evaluation-harness.md)).
- When you only need a one-off check (use the `time` + `curl` method described in the API examples).

## Getting started
Installation is straightforward via pip. Ensure you have Ollama running in the background before starting the benchmark.

```bash
pip install git+https://github.com/LarHope/ollama-benchmark.git
```

For multi-GPU local systems, configure Ollama with GPU-specific parameters before benchmarking:
```bash
# Example CUDA configuration for parallel GPUs
export CUDA_VISIBLE_DEVICES=0,1
export OLLAMA_NUM_PARALLEL=4
```

## CLI examples

### Benchmarking Specific Models
```bash
ollama-benchmark --models llama4:8b deepseek-r1:32b --table_output
```

### Benchmarking with Context Limits and Thread Controls
Specify custom context window limits and thread counts to mirror July 2026 agent environments:
```bash
ollama-benchmark \
    --models gemma3:9b \
    --num_ctx 16384 \
    --num_thread 8 \
    --output-json ./metrics/gemma3_stats.json
```

### Benchmarking with Custom Prompts
```bash
ollama-benchmark --models mistral --prompts "Explain quantum computing" "Write a fast Fibonacci in Python"
```

### Automated Batch Benchmarking
```bash
ollama-benchmark --models $(ollama list | awk '{print $1}' | tail -n +2) --table_output
```

## API examples
Ollama Benchmark CLI primarily functions as a CLI, but its logic can be replicated using the Ollama REST API for custom instrumentation.

### Manual Latency Measurement (`time` + `curl`)
For a quick check without installing tools, use the Ollama API directly:
```bash
time curl -X POST http://localhost:11434/api/generate \
  -d '{
    "model": "llama4",
    "prompt": "Why is the sky blue?",
    "stream": false
  }'
```

### Python API Integration
A robust python wrapper to measure local prompt prefill speed versus token generation speed:

```python
import requests
import time

def benchmark_local_model(model_name, prompt, context_size=8192):
    start = time.time()
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": context_size,
            "temperature": 0.0
        }
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=180
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return

    end = time.time()
    data = response.json()

    # Calculate prefill and generation metrics
    eval_count = data.get('eval_count', 0)
    eval_duration = data.get('eval_duration', 1)
    prompt_eval_count = data.get('prompt_eval_count', 0)
    prompt_eval_duration = data.get('prompt_eval_duration', 1)

    generation_tps = eval_count / (eval_duration / 1e9) if eval_duration else 0.0
    prefill_tps = prompt_eval_count / (prompt_eval_duration / 1e9) if prompt_eval_duration else 0.0

    print(f"Model: {model_name}")
    print(f"  - Prompt Prefill Speed: {prefill_tps:.2f} tokens/sec")
    print(f"  - Generation Speed: {generation_tps:.2f} tokens/sec")
    print(f"  - Total Turnaround Time: {end-start:.2f}s")

benchmark_local_model("llama4:8b", "Analyze current agent security baselines.")
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

## Sources / references
- [LarHope/ollama-benchmark GitHub Repository](https://github.com/LarHope/ollama-benchmark)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Local LLM Performance Leaderboard (2026)](https://example.com/local-llm-bench)

## Contribution Metadata
- Last reviewed: 2026-07-23
- Confidence: high
