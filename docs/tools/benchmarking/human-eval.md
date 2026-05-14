# HumanEval

## What it is
HumanEval is a benchmark released by OpenAI to evaluate the code generation capabilities of Large Language Models. It consists of 164 handwritten programming problems, each including a function signature, docstring, body, and several unit tests. The problems assess the model's ability to solve basic algorithmic tasks. The key metric is **Pass@k**, the probability that at least one of the top k generated code samples passes all unit tests.

## What problem it solves
Provides a standardized, non-contaminated measure of whether LLMs can generate functionally correct code from natural language descriptions. Since the problems were handwritten and not scraped from public repositories (at least initially), it provides a cleaner evaluation of zero-shot coding ability.

## Where it fits in the stack
**Benchmarking**. Used as a primary reference benchmark for code generation and algorithmic reasoning capabilities of LLMs.

## Typical use cases
- Evaluating LLM code generation accuracy on self-contained programming tasks
- Comparing models on their ability to produce correct Python code
- Measuring improvements in code generation across model versions or fine-tuning runs

## Strengths
- Well-established and widely cited benchmark
- Problems are self-contained with clear, automated unit test validation
- Pass@k metric accounts for sampling variability and model creativity
- Focuses on logical correctness rather than just syntax

## Limitations
- Small scale (164 problems), which may not cover the full range of programming patterns
- Focuses primarily on Python and basic algorithmic tasks
- Does not test real-world software engineering skills like debugging, refactoring, or working with large multi-file codebases
- High risk of contamination as it is frequently used in training data for newer models

## When to use it
- When comparing frontier LLMs on their ability to generate correct code from specifications
- When evaluating a model for "coding assistant" use cases
- As a fast, automated check for coding regression in model pipelines

## When not to use it
- When you need to evaluate real-world software engineering capability (use [SWE-bench](swe-bench.md) instead)
- When you need multilingual code generation evaluation (use MultiPL-E)
- For evaluating complex system design or library-specific knowledge

## Getting started

You can run HumanEval using the official OpenAI execution environment or through broader harnesses.

1. Clone the repository: `git clone https://github.com/openai/human-eval`
2. Install the package: `pip install -e human-eval`
3. Run the evaluation script (warning: this executes model-generated code):

```bash
python evaluate_functional_correctness.py samples.jsonl
```

## Technical examples

### Example Problem (HumanEval/0)
```python
from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, any two numbers are closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """
```

### Pass@k Metric
Pass@1 is the most common metric. For a model generating $n$ samples, if $c$ samples pass, the Pass@k is calculated as:

$$Pass@k = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}$$

## Related tools / concepts
- [MBPP (Mostly Basic Python Problems)](mbpp.md)
- [BigCodeBench](https://github.com/bigcode-project/bigcodebench)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [SWE-bench](swe-bench.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [Aider](../development_ops/aider.md)
- [Cursor](../development_ops/cursor.md)

## Sources / references
- [OpenAI HumanEval GitHub](https://github.com/openai/human-eval)
- [Arxiv: Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
