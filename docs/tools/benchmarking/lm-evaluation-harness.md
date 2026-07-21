# LM Evaluation Harness

## What it is
LM Evaluation Harness (by EleutherAI) is a unified framework for few-shot evaluation of autoregressive language models. As of July 2026, **v0.4.x+** serves as the stable production standard, providing a standardized, highly optimized interface to evaluate models on hundreds of academic and custom benchmarks. It supports the latest July 2026 frontier models including Gemma 3, Llama 4, Mistral, Qwen 3.6, and Claude 5.1. It features native support for secure execution sandboxes, multi-GPU pipeline optimizations, and advanced tool-calling and agent evaluation benchmarks.

## What problem it solves
It eliminates the high engineering overhead and inconsistencies associated with designing individual evaluation pipelines for every new LLM benchmark. By providing a single, standardized framework, it ensures that results are mathematically comparable across different papers, platforms, and models. This reduces the risk of "eval-hacking" and establishes consistent quality gates for modern agentic software factories.

## Where it fits in the stack
**Benchmarking**. It acts as the comprehensive "Swiss Army Knife" for model quality and capability evaluation. Sitting directly between raw model weights/API endpoints and high-level leaderboards, it is a core validation layer for continuous integration, safety verification, and satisfaction-based agentic testing.

## Typical use cases
- **Model Comparison**: Running standard academic benchmarks (such as MMLU, HellaSwag, ARC) to compare fine-tuned models against established baselines.
- **Regression Testing**: Verifying that quantization, pruning, or compile-time optimizations (via [vLLM](../infrastructure/vllm.md)) haven't degraded model accuracy.
- **Secure Coding Evaluation**: Executing code-generation benchmarks (like HumanEval or MBPP) in isolated execution environments to measure code correctness.
- **Agent and Tool-Calling Evals**: Measuring the decision-making and tool-using efficiency of modern agents using Model Context Protocol (MCP 3.0/3.1) endpoints.
- **Large-Scale Multi-GPU Runs**: Using tensor/pipeline parallelism to perform rapid, distributed evaluation of huge models (e.g., Llama-4 100B) on multi-node clusters.

## Strengths
- **Massive Benchmark Library**: Direct access to 100+ standard academic benchmarks with thousands of subtasks, including advanced July 2026 benchmarks.
- **Model and Backend Agnostic**: Native support for Hugging Face `transformers`, `vLLM`, `GGUF`, and diverse external APIs (OpenAI, Anthropic, Gemini, LiteLLM).
- **Secure Sandboxed Execution**: Native support for Docker and WASM-based secure execution sandboxes to prevent untrusted benchmark or model-generated code from compromising host infrastructure.
- **Multi-GPU Pipeline Optimization**: Seamlessly integrates with DeepSpeed, Accelerate, and vLLM backends for maximum parallelization and rapid context throughput.
- **MCP 3.0/3.1 Integration**: Standarized support for Model Context Protocol, enabling evaluators to inject custom tools and monitor tool-use efficacy programmatically.

## Limitations
- **Autoregressive Focus**: Primarily designed for causal decoder-only language models; support for encoder-decoder structures or multimodal tasks is functional but less mature.
- **Compute Overhead**: Running the complete suite of default benchmarks requires considerable computational power and can take hours or days on standard hardware.
- **YAML Complexity**: Custom task definition via YAML files has a steep learning curve, particularly when designing complex multi-turn reasoning prompts or visual RAG evals.

## When to use it
- When you need to evaluate local or fine-tuned model checkpoints across many standard academic benchmarks at once.
- When validating a model's coding ability (HumanEval/MBPP) and requiring a reliable, secure sandbox execution environment.
- When establishing high-confidence, automated regression testing gates in a CI/CD development pipeline.
- When assessing model performance on agentic benchmarks using structured tool interfaces.

## When not to use it
- When you require a specialized benchmark runner that has its own highly optimized, non-standard system (e.g., [SWE-bench](swe-bench.md) for full-repository patching).
- For pure speed, throughput, or latency profiling (use [LLMPerf](llmperf.md) or [Ollama Benchmark](ollama-benchmark-cli.md) instead).
- For evaluating long-horizon, multi-step autonomous agent trajectories (use [Terminal-Bench](terminal-bench.md) or [PA-bench](pa-bench.md)).

## Getting started
The LM Evaluation Harness requires Python 3.10+ and a suitable backend for model execution. In July 2026, security guidelines strongly recommend running evaluations with code execution inside secure sandboxes (such as Docker or WASM-based runtimes) to prevent malicious or malformed code in benchmark datasets from compromising host environments.

### Installation
```bash
# Install core package with Hugging Face, vLLM, and API support
pip install "lm_eval[hf,vllm,api]"

# Install sandbox execution extras
pip install "lm_eval[sandbox]"

# Install MCP support for tool-calling and agentic evaluations
pip install "lm_eval[mcp]"
```

## CLI examples

### Basic Evaluation (Hugging Face)
Evaluate a Hugging Face model on the `hellaswag` benchmark using a single GPU:
```bash
lm_eval --model hf \
    --model_args pretrained=google/gemma-3-8b-it \
    --tasks hellaswag \
    --device cuda:0 \
    --batch_size 8
```

### Fast Multi-GPU Evaluation with vLLM
Leverage `vLLM` for much faster inference during evaluation, distributing the workload using multi-GPU pipeline and tensor parallel optimization:
```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-4-70b-it,tensor_parallel_size=4,dtype=bfloat16 \
    --tasks gsm8k,mmlu_pro \
    --batch_size auto
```

### Secure Evaluation with Sandboxed Code Execution
When evaluating coding benchmarks (such as HumanEval) that require executing generated model code, run them securely in an isolated Docker sandbox:
```bash
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-4-8b-it \
    --tasks humaneval \
    --allow_code_execution \
    --sandbox_backend docker \
    --device cuda:0
```

### Evaluation with MCP Tools
Enable MCP tool support for agentic evaluation, leveraging Model Context Protocol (MCP 3.0/3.1) clients to interact with external tools:
```bash
lm_eval --model mcp \
    --model_args server_url=http://localhost:18789 \
    --tasks mmlu_pro \
    --include_mcp_tools
```

## API examples

### Python API Usage (Basic)
The harness can be integrated directly into Python scripts for automated validation pipelines.

```python
import lm_eval
from lm_eval.models.huggingface import HFLM

# Initialize model
model = HFLM(pretrained="google/gemma-3-8b-it", device="cuda:0")

# Run evaluation
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["arc_easy", "gsm8k"],
    num_fewshot=5,
    batch_size=8
)

# Print results
print(lm_eval.utils.make_table(results))
```

### Programmatic Sandboxed Code Evaluation with Multi-GPU Config
Initialize a parallelized evaluation with a secure sandbox backend to handle code-execution tasks (like MBPP or HumanEval) programmatically.

```python
import lm_eval
from lm_eval.models.huggingface import HFLM

# Initialize Hugging Face model with multi-GPU tensor parallel pipeline
model = HFLM(
    pretrained="meta-llama/Llama-4-70b-it",
    backend="vllm",
    model_args="tensor_parallel_size=2,dtype=bfloat16"
)

# Run evaluation in a secure Docker sandbox
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["humaneval"],
    allow_code_execution=True,
    sandbox={
        "backend": "docker",
        "image": "python:3.10-slim-secure",
        "timeout": 10.0
    }
)

# Access scores
for task, score in results["results"].items():
    print(f"Task: {task} | Pass@1: {score.get('pass@1', 'N/A')}")
```

## Related tools / concepts
- [MMLU](mmlu.md) — Massive Multitask Language Understanding, the standard benchmark for multi-subject reasoning.
- [GSM8K](gsm8k.md) — Grade school math benchmark used to evaluate multi-step arithmetic and reasoning.
- [HumanEval](human-eval.md) — Python code generation benchmark requiring sandboxed validation.
- [Humanitys Last Exam](humanitys-last-exam.md) — Frontier-difficulty benchmark designed to challenge the most capable multi-agent setups.
- [LLMPerf](llmperf.md) — Benchmarking framework for measuring serving operational throughput, TTFT, and latency.
- [Ollama Benchmark](ollama-benchmark-cli.md) — High-performance localized model speed and hardware benchmarking.
- [SWE-bench](swe-bench.md) — Full-repository software engineering agent evaluations.
- [PA-bench](pa-bench.md) — Benchmarking framework designed for web-based multi-step workflows and alignment.
- [Terminal-Bench](terminal-bench.md) — Evaluates performance of LLMs in terminal and interactive shell environments.
- [vLLM](../infrastructure/vllm.md) — High-throughput inference engine serving as a fast execution backend for the harness.
- [LiteLLM](../../services/litellm.md) — Universal multi-provider proxy for standardized API-based benchmark routing.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Open standard for connecting AI models to secure tool sandboxes and databases.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Conceptual architectures utilizing benchmarking frameworks as continuous deployment quality gates.

## Sources / references
- [LM Evaluation Harness GitHub Repository](https://github.com/EleutherAI/lm-evaluation-harness)
- [EleutherAI Documentation](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/docs)
- [Open LLM Leaderboard (Hugging Face)](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
- [AIR-Bench 2026 Specifications](https://github.com/air-bench/air-bench)

- Last reviewed: 2026-07-21
- Confidence: high
