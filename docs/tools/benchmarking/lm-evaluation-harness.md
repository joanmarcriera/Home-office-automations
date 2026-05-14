# LM Evaluation Harness

## What it is
LM Evaluation Harness (by EleutherAI) is a unified framework for few-shot evaluation of autoregressive language models. It provides a standardized interface to evaluate models on hundreds of different tasks, including MMLU, ARC, HellaSwag, GSM8K, and many more. It is the primary backend for the Hugging Face [Open LLM Leaderboard](../benchmarking/index.md).

## What problem it solves
Eliminates the need for researchers to implement individual, often inconsistent, evaluation pipelines for every new benchmark. By providing a single, standardized framework, it ensures that results are comparable across different papers and models, reducing the "eval-hacking" potential and implementation overhead.

## Where it fits in the stack
**Benchmarking**. It serves as the comprehensive "Swiss Army Knife" for model quality evaluation, sitting between raw model weights and high-level leaderboards.

## Typical use cases
- **Model Comparison**: Running a standard battery of tests (e.g., the "leaderboard" group) to compare a new fine-tuned model against a base model.
- **Regression Testing**: Ensuring that quantization (using [GPTQ](../infrastructure/index.md)) or optimization hasn't significantly degraded model performance.
- **Custom Benchmark Development**: Implementing new evaluation tasks using the framework's YAML-based configuration system.
- **Multi-GPU Evaluation**: Using `accelerate` or `vLLM` backends to rapidly evaluate large models (e.g., Llama-3 70B) across multiple cards.

## Strengths
- **Massive Task Library**: Supports 60+ standard academic benchmarks with hundreds of subtasks.
- **Model Agnostic**: Supports Hugging Face `transformers`, `vLLM`, `GGUF` (via llama.cpp), and various APIs (OpenAI, Anthropic).
- **Community Standard**: Widely adopted by industry and academia; results are considered high-signal.
- **Highly Configurable**: Support for Jinja2 prompt templates, multiple few-shot settings, and automated batch size detection.

## Limitations
- **Focus on Causal LMs**: Primarily designed for autoregressive, decoder-only models; support for encoder-decoder models exists but is less central.
- **Compute Intensive**: Running the full suite of benchmarks can take hours or days on high-end GPUs.
- **Complexity**: The YAML configuration for new tasks can have a steep learning curve for complex multi-choice reasoning.

## When to use it
- When you need to evaluate a model across many standard benchmarks at once.
- When comparing a local or fine-tuned model against baseline results from the Open LLM Leaderboard.
- When you want to ensure your evaluation methodology matches established community standards.

## When not to use it
- When you only need to run a single, highly specialized benchmark that has its own optimized runner (e.g., [SWE-bench](swe-bench.md)).
- When you are benchmarking inference *speed* (latency/throughput) rather than *quality* (use [LLMPerf](llmperf.md) or [Ollama Benchmark](ollama-benchmark-cli.md)).

## Getting started (CLI Examples)

### Installation
```bash
pip install "lm_eval[hf,vllm,api]"
```

### Basic Evaluation (Hugging Face)
Evaluate a model on the `hellaswag` benchmark using a single GPU:
```bash
lm_eval --model hf \
    --model_args pretrained=EleutherAI/pythia-160m \
    --tasks hellaswag \
    --device cuda:0 \
    --batch_size 8
```

### Fast Evaluation (vLLM)
Leverage `vLLM` for much faster inference during evaluation:
```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-3-8b,tensor_parallel_size=1,dtype=auto \
    --tasks gsm8k,mmlu \
    --batch_size auto
```

### API Evaluation
Evaluate a model served via an OpenAI-compatible API:
```bash
export OPENAI_API_KEY="your_key"
lm_eval --model openai-completions \
    --model_args model=davinci-002 \
    --tasks arc_easy
```

## Related tools / concepts

- [MMLU (Massive Multitask Language Understanding)](mmlu.md) - One of the most popular benchmarks in the harness.
- [GSM8K](gsm8k.md) - Grade school math benchmark supported by the harness.
- [HumanEval](human-eval.md) - Code generation benchmark.
- [HLE (Humanity's Last Exam)](humanitys-last-exam.md) - A frontier-difficulty benchmark.
- [LLMPerf](llmperf.md) - Benchmarking operational performance (latency/throughput).
- [Ollama Benchmark](ollama-benchmark-cli.md) - Benchmarking local model speed.
- [SWE-bench](swe-bench.md) - Real-world software engineering benchmark.
- [vLLM](../infrastructure/index.md) - High-throughput inference engine supported as a backend.
- [LiteLLM](../../services/litellm.md) - Multi-provider API proxy supported by the harness.

## Sources / references
- [LM Evaluation Harness GitHub Repository](https://github.com/EleutherAI/lm-evaluation-harness)
- [EleutherAI Documentation](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/docs)
- [Open LLM Leaderboard (Hugging Face)](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
