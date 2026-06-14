# EvalPlus

## What it is
EvalPlus is a rigorous evaluation framework for Large Language Models (LLMs) focused on code generation (LLM4Code). It significantly expands existing benchmarks like HumanEval and MBPP with more comprehensive test cases to improve evaluation accuracy. As of June 2026, it is the industry standard for verifying the coding robustness of frontier models like `claude-4-8-opus-20260528` and GPT-5.5.

## What problem it solves
Original coding benchmarks like [HumanEval](human-eval.md) often have very few test cases, allowing fragile or incorrect code to pass. EvalPlus addresses this "under-testing" problem by adding 80x more tests to HumanEval and 35x more tests to MBPP, revealing model weaknesses that simpler benchmarks miss.

## Where it fits in the stack
**Benchmarking**. It is a specialized tool for deeply evaluating the code generation capabilities and efficiency of LLMs. It sits between basic algorithmic benchmarks and full agentic benchmarks like [SWE-bench](swe-bench.md).

## Typical use cases
- **Rigorous Coding Evaluation**: Testing a model's true coding ability beyond simple benchmarks.
- **Fragility Detection**: Identifying if a model's generated code is robust across many different inputs.
- **Code Efficiency Benchmarking**: Using the EvalPerf extension to measure the execution speed of LLM-generated code.
- **Frontier Model Verification**: Confirming the coding reliability of Claude 4.8 Opus and GPT-5.5.

## Strengths
- **High Rigor**: Expanded test suites (HumanEval+, MBPP+) significantly reduce false positives.
- **Multi-backend Support**: Supports evaluation via vLLM, Hugging Face, OpenAI, Anthropic, Gemini, and Ollama.
- **Security**: Supports safe code execution within Docker containers to protect the host system.
- **Performance Evaluation**: Includes EvalPerf for measuring code efficiency.
- **Open Source**: Licensed under Apache 2.0.

## Limitations
- **Focus**: Primarily limited to Python and coding-specific tasks.
- **Execution Cost**: Running 80x more tests naturally takes more time and compute than the original benchmarks.
- **Language Coverage**: While expanding, its primary strength remains in the Python ecosystem.

## When to use it
- When you are developing or fine-tuning an LLM for code generation and need high-confidence metrics.
- When you want to rank models based on their coding robustness and efficiency.
- When comparing against major industry models (many of which, like Llama 4 Maverick and Qwen 3.5, use EvalPlus).

## When not to use it
- For general knowledge or reasoning tasks (use [MMLU](mmlu.md) or [GPQA](gpqa.md) instead).
- For quick, non-rigorous evaluations of simple code snippets.

## Getting started

### Installation
You can install EvalPlus via pip. For full functionality including vLLM and performance benchmarking:

```bash
pip install "evalplus[vllm,perf]" --upgrade
```

### Setup
Ensure Docker is installed if you intend to run evaluations in a sandboxed environment (highly recommended).

```bash
# Verify installation
evalplus.evaluate --help
```

## CLI examples

### Functional Evaluation (vLLM)
To evaluate a model locally using the vLLM backend on the HumanEval dataset:

```bash
evalplus.evaluate --model "meta-llama/Llama-4-Maverick-8B" \
                  --dataset humaneval \
                  --backend vllm \
                  --greedy
```

### Docker Execution (Safe Sandboxing)
For security, it is highly recommended to run the evaluation inside a Docker container:

```bash
# Generate samples locally first
evalplus.codegen --model "anthropic/claude-4-8-opus-20260528" --dataset humaneval --backend anthropic

# Run evaluation inside the EvalPlus sandbox
docker run --rm -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evaluate --dataset humaneval \
           --samples /app/humaneval/anthropic--claude-4-8-opus-20260528_temp_0.0.jsonl
```

## API examples

EvalPlus provides a Python API for programmatic access to datasets and evaluation utilities:

```python
from evalplus.data import get_human_eval_plus, get_mbpp_plus

# Load the enhanced HumanEval dataset
human_eval_plus = get_human_eval_plus()
first_task = human_eval_plus['HumanEval/0']

print(f"Task ID: {first_task['task_id']}")
print(f"Prompt: {first_task['prompt']}")
print(f"Number of Test Cases: {len(first_task['test_setup'])}")
```

### Custom Inference Example
```python
# samples = []
# for task_id, task in human_eval_plus.items():
#     code = my_model.generate(task['prompt'])
#     samples.append({"task_id": task_id, "solution": code})
# save_jsonl(samples, "my_model_samples.jsonl")
```

## Related tools / concepts
- [HumanEval](human-eval.md) — the foundational benchmark EvalPlus expands upon.
- [MBPP](mbpp.md) — the other major benchmark expanded by EvalPlus.
- [SWE-bench](swe-bench.md) — software engineering benchmark.
- [vLLM](../infrastructure/vllm.md) — optimized inference backend.
- [OpenCompass](opencompass.md) — evaluation platform.
- [HELM](helm.md) — holistic evaluation.
- [LM Evaluation Harness](lm-evaluation-harness.md) — standardized evaluation tool.
- [BigCodeBench](bigcodebench.md) — complex library-use benchmark.

## Sources / References
- [Official Website](https://evalplus.github.io/)
- [GitHub Repository](https://github.com/evalplus/evalplus)
- [NeurIPS 2023 Paper (arXiv 2305.01210)](https://arxiv.org/abs/2305.01210)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
