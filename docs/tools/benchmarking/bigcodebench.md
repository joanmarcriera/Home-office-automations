# BigCodeBench

## What it is
BigCodeBench is a comprehensive benchmark for evaluating the code generation capabilities of LLMs in realistic software engineering scenarios. It features 1,140 programming tasks that require the use of diverse libraries (139 unique libraries) and complex function calls. As of June 2026, it serves as a critical performance differentiator for frontier models like `claude-4-8-opus-20260528` and GPT-5.5.

## What problem it solves
Simple benchmarks like HumanEval or MBPP focus on basic algorithmic tasks that don't reflect real-world programming. BigCodeBench evaluates "tool-use" and the ability to follow complex, multi-step instructions using common Python libraries, addressing the "instruction-following" gap in code generation.

## Where it fits in the stack
BigCodeBench is a core tool in the **Benchmarking** layer for code-specialized models and agents. It is often used to validate model performance before integration into IDE assistants or autonomous coding agents like [OpenHands](../development_ops/openhands.md).

## Typical use cases
- **Frontier Model Comparison**: Assessing the gap between Claude 4.8 Opus and GPT-5.5 on complex library integration.
- **Agent Validation**: Evaluating coding agents that need to use external libraries (e.g., `pandas`, `requests`).
- **Instruction-Following Rank**: Ranking models on their ability to adhere to complex constraints within a single prompt.
- **CI/CD Benchmarking**: Validating model updates for specialized coding LLMs.

## Strengths
- **Realism**: Tasks are software-engineering-oriented rather than purely algorithmic.
- **Large Scale**: Contains over 1,000 tasks, reducing the impact of "noise" or luck in evaluation.
- **Library Diversity**: Covers 139 libraries including `numpy`, `pandas`, `requests`, and `matplotlib`.
- **Apache 2.0 Licensed**: Open-source and free to use for research and commercial evaluation.

## Limitations
- **Execution Overhead**: Running the full benchmark is computationally intensive and slow.
- **Python-Centric**: Primarily focuses on Python, leaving other languages less covered.
- **Sandboxing Requirement**: Requires a secure execution environment (Docker) to prevent malicious code execution.

## When to use it
- When evaluating models intended for use as coding assistants or autonomous software engineers.
- When you need to distinguish between high-performing models that "max out" simpler benchmarks like HumanEval.
- To measure instruction-following accuracy in a coding context.

## When not to use it
- For base models that have not been instruction-tuned.
- When a fast, lightweight evaluation is needed (use [HumanEval](human-eval.md) instead).
- For evaluating non-Python coding performance.

## Getting started

### Installation
It is recommended to use the BigCodeBench CLI within a sandboxed environment.

```bash
pip install bigcodebench --upgrade
```

### Setup
Ensure you have Docker installed, as most evaluations require a secure runtime to execute model-generated code.

```bash
# Verify installation
bigcodebench --help
```

## CLI examples

### Running Evaluation
Evaluate a model's generated samples (provided in JSONL format) against the "hard" subset:

```bash
bigcodebench.evaluate \
    --samples samples.jsonl \
    --subset hard \
    --parallel 8
```

### Data Generation
Generate the benchmark prompts for model inference:

```bash
bigcodebench.generate --subset complete --save_path prompts.jsonl
```

## API examples

While primarily used via CLI, BigCodeBench data can be accessed programmatically for custom evaluation pipelines:

```python
from datasets import load_dataset

# Load BigCodeBench 'Hard' subset
dataset = load_dataset("bigcode/bigcodebench", split="test")
sample = dataset[0]

print(f"Task ID: {sample['task_id']}")
print(f"Instruction: {sample['instruction']}")
```

### Custom Evaluation Loop
```python
# Conceptual integration with an LLM client
# prompt = sample['complete_prompt']
# response = client.generate(model="claude-4-8-opus-20260528", prompt=prompt)
# save_sample(response, "samples.jsonl")
```

## Related tools / concepts
- [HumanEval](human-eval.md) — the foundational coding benchmark.
- [MBPP](mbpp.md) — crowd-sourced programming problems.
- [EvalPlus](evalplus.md) — enhanced test cases for HumanEval/MBPP.
- [SWE-bench](swe-bench.md) — software engineering benchmark using GitHub issues.
- [LiveCodeBench](livecodebench.md) — benchmark using recent competitive programming problems.
- [OpenHands](../development_ops/openhands.md) — autonomous agent that uses these benchmarks for validation.
- [Claude Code Container MCP](../development_ops/claude-code-container-mcp.md) — sandbox for code execution.
- [vLLM](../infrastructure/vllm.md) — optimized inference engine often used for benchmarking.

## Sources / references
- [BigCodeBench GitHub](https://github.com/bigcode-project/bigcodebench)
- [BigCodeBench: The Next Frontier of Code Generation (arXiv 2406.15877)](https://arxiv.org/abs/2406.15877)
- [BigCodeBench Leaderboard](https://bigcode-bench.github.io/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
