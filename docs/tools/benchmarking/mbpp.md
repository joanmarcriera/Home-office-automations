# MBPP (Mostly Basic Python Problems)

## What it is
MBPP is a benchmark designed to evaluate the code generation performance of LLMs on basic Python tasks. It consists of approximately 1,000 crowd-sourced Python programming problems, designed to be solvable by entry-level programmers. Each problem includes a task description (prompt), a gold-standard code solution, and three automated test cases. It was introduced by Google Research in 2021.

## What problem it solves
Provides a large-scale, standardized evaluation of LLM code generation on "mostly basic" problems. While benchmarks like [HumanEval](human-eval.md) focus on algorithmic complexity, MBPP covers a broader range of fundamental programming concepts, standard library usage, and common data structure manipulations, providing a more robust statistical measure of entry-level coding proficiency.

## Where it fits in the stack
**Benchmarking**. Used as a primary code-generation benchmark for evaluating and comparing the Python coding capabilities of LLMs.

## Typical use cases
- **Model Comparison**: Measuring the `Pass@1` and `Pass@k` metrics of new models against industry baselines.
- **Fine-tuning Evaluation**: Verifying that a model fine-tuned on code datasets (e.g., StarCoder, CodeLlama) has improved on basic programming tasks.
- **Contamination Testing**: Using the "sanitized" version of the dataset to ensure results haven't been inflated by training data leakage.

## Strengths
- **Large Dataset**: With ~1,000 problems, it offers higher statistical confidence than smaller benchmarks.
- **Automated Verification**: Each problem comes with executable test cases, ensuring objective scoring.
- **Sanitized Subset**: A subset of the data has been hand-verified and "sanitized" to remove ambiguous or low-quality problems.
- **Realistic Basics**: Focuses on tasks a junior developer would perform, rather than just "LeetCode-style" puzzles.

## Limitations
- **Basic Level**: Does not evaluate architectural reasoning, multi-file projects, or advanced software engineering patterns (use [SWE-bench](swe-bench.md) for that).
- **Python Only**: Limited to Python code generation.
- **Prompt Sensitivity**: Like all LLM benchmarks, results can vary significantly based on the exact prompt format used.
- **Saturation**: High-end models (GPT-4o, Claude 3.5 Sonnet) are reaching very high scores, reducing its utility for differentiating between the absolute top-tier models.

## When to use it
- When evaluating the fundamental Python coding ability of a model.
- When you need a statistically robust code benchmark that is larger than HumanEval.
- When assessing a model's familiarity with the Python standard library.

## When not to use it
- When evaluating complex, real-world software engineering or repository-wide changes (use [SWE-bench](swe-bench.md) or [BigCodeBench](bigcodebench.md)).
- When testing non-Python languages.
- When evaluating high-level algorithmic reasoning that isn't captured by "basic" problems.

## Getting started (CLI Examples)

MBPP is typically run through evaluation frameworks like the [LM Evaluation Harness](lm-evaluation-harness.md) or [EvalPlus](evalplus.md).

### Running via LM Evaluation Harness
```bash
# Evaluate a model on the mbpp benchmark
lm_eval --model hf \
    --model_args pretrained=EleutherAI/pythia-160m \
    --tasks mbpp \
    --device cuda:0 \
    --batch_size 8
```

### Prompt Format Example
The original paper used a 3-shot prompt with the following structure:
```text
You are an expert Python programmer, and here is your task: {prompt}
Your code should pass these tests:

{test_cases}

[BEGIN]
{generated_code}
[DONE]
```

## Related tools / concepts

- [HumanEval](human-eval.md) - The other "standard" Python code benchmark.
- [EvalPlus](evalplus.md) - A framework that hardens MBPP/HumanEval with thousands of extra test cases.
- [SWE-bench](swe-bench.md) - Real-world software engineering benchmark.
- [BigCodeBench](bigcodebench.md) - A more difficult and modern code benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) - The framework used to run MBPP.
- [HLE (Humanity's Last Exam)](humanitys-last-exam.md) - Frontier difficulty reasoning.
- [MMLU](mmlu.md) - General knowledge benchmark.
- [LiveCodeBench](livecodebench.md) - Contamination-free coding benchmark.

## Sources / references
- [MBPP GitHub Repository (Google Research)](https://github.com/google-research/google-research/tree/master/mbpp)
- [Program Synthesis with Large Language Models (Austin et al., 2021)](https://arxiv.org/abs/2108.07732)
- [Hugging Face Dataset (mbpp)](https://huggingface.co/datasets/mbpp)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high
