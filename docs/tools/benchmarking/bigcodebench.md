# BigCodeBench

## What it is
BigCodeBench is a comprehensive benchmark for evaluating code generation capabilities of LLMs in realistic software engineering scenarios. It features 1,140 programming tasks that require the use of diverse libraries (139 unique libraries) and complex function calls, providing a much higher ceiling than traditional benchmarks.

## What problem it solves
Simple benchmarks like HumanEval or MBPP focus on basic algorithmic tasks that don't reflect real-world programming. BigCodeBench evaluates "tool-use" and the ability to follow complex, multi-step instructions using common Python libraries, addressing the "instruction-following" gap in code generation.

## Where it fits in the stack
BigCodeBench is a core tool in the **Benchmarking** layer for code-specialized models and agents. It is often used to validate the performance of models before they are integrated into IDE assistants or autonomous coding agents.

## Typical use cases
- Comparing the programming performance of different LLMs (e.g., Llama 3 vs. GPT-4).
- Evaluating coding agents that need to use external libraries.
- Ranking instruction-tuned models on their ability to generate functional, production-like code.
- Benchmarking model updates in a CI/CD pipeline for specialized coding LLMs.

## Strengths
- **Realism**: Tasks are software-engineering-oriented rather than purely algorithmic.
- **Large Scale**: Contains over 1,000 tasks, reducing the impact of "noise" or luck in evaluation.
- **Library Diversity**: Covers 139 libraries including `numpy`, `pandas`, `requests`, and `matplotlib`.
- **Instruction Following**: Specifically tests the model's ability to adhere to complex constraints within the prompt.

## Limitations
- **Execution Overhead**: Running the full benchmark can be computationally expensive and slow due to extensive test suites.
- **Python-Centric**: Primarily focuses on Python code generation.
- **Sandboxing Requirement**: Requires a secure execution environment to prevent malicious code execution during testing.

## When to use it
- When evaluating models intended for use as coding assistants or autonomous software engineers.
- When you need to distinguish between high-performing models that already "max out" HumanEval.

## When not to use it
- For base models that have not been instruction-tuned (they will likely fail on the complex natural language instructions).
- When a fast, lightweight evaluation is needed (use HumanEval instead).

## Technical examples

### Running Evaluation (CLI)
BigCodeBench provides a CLI for running evaluations. It is recommended to use Docker for isolation.

```bash
# Evaluate a model's generated samples
bigcodebench.evaluate \
    --samples samples.jsonl \
    --subset hard \
    --parallel 8
```

### Prompt Format example
BigCodeBench prompts typically provide a docstring with specific library requirements.

```python
"""
Write a function to create a 3D scatter plot using matplotlib and return the plot object.
The function should take three lists of coordinates (x, y, z) and a title string.
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_scatter(x, y, z, title):
    # Model should complete this
```

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: Free to use (software). Computational costs for model inference and test execution apply.

## Related tools / concepts
- [HumanEval](../benchmarking/human-eval.md)
- [MBPP](../benchmarking/mbpp.md)
- [EvalPlus](../benchmarking/evalplus.md)
- [SWE-bench](../benchmarking/swe-bench.md)
- [LiveCodeBench](../benchmarking/livecodebench.md)
- [Terminal-Bench](../benchmarking/terminal-bench.md)
- [OpenHands](../development_ops/openhands.md)
- [Claude Code Container MCP](../development_ops/claude-code-container-mcp.md)

## Sources / references
- [BigCodeBench GitHub](https://github.com/bigcode-project/bigcodebench)
- [BigCodeBench: The Next Frontier of Code Generation](https://arxiv.org/abs/2406.15877)
- [BigCodeBench Website](https://bigcode-bench.github.io/)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high
