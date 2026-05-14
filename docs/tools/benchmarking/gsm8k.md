# GSM8K (Grade School Math 8K)

## What it is
GSM8K is a benchmark for evaluating the multi-step mathematical reasoning capabilities of LLMs. It contains 8.5K high-quality grade school math word problems that require 2 to 8 steps of basic arithmetic to solve. The key metric is Exact Match (EM), measuring the accuracy of the final numerical answer.

## What problem it solves
Provides a standardized way to measure whether LLMs can perform multi-step arithmetic reasoning, a fundamental capability for practical mathematical tasks and logical planning. It moves beyond simple "calculator" tasks to test the model's ability to decompose a problem into logical steps.

## Where it fits in the stack
**Benchmarking**. Serves as a widely used reference for evaluating mathematical reasoning and Chain-of-Thought (CoT) efficacy in LLMs.

## Typical use cases
- Evaluating LLM arithmetic and multi-step reasoning capabilities
- Measuring the impact of prompting strategies (e.g., Chain-of-Thought, Few-Shot) on math performance
- Comparing models on fundamental mathematical problem-solving
- Regression testing for fine-tuned models to ensure math capabilities haven't degraded

## Strengths
- Large dataset (8.5K problems) provides statistically meaningful results
- Problems are well-defined with unambiguous numerical answers
- Widely adopted, enabling easy cross-model comparisons
- High correlation with a model's general reasoning and instruction-following ability

## Limitations
- Limited to grade-school-level math; does not test advanced mathematics (calculus, linear algebra)
- Problems are relatively formulaic compared to real-world math applications
- Exact Match scoring does not give partial credit for correct reasoning with minor arithmetic errors
- Increasing evidence of benchmark contamination in newer models

## When to use it
- When comparing LLMs on basic mathematical reasoning and logical consistency
- When evaluating the effect of different prompting techniques (like `Let's think step by step`) on math performance
- For base-level capability checks during model development

## When not to use it
- When you need to evaluate advanced mathematical reasoning (use [MATH Benchmark](math-benchmark.md) instead)
- When testing non-mathematical or creative writing capabilities
- For evaluating complex symbolic logic or theorem proving

## Getting started

GSM8K can be evaluated using standard libraries like `lm-eval`.

1. Install the LM Evaluation Harness: `pip install lm-eval`
2. Run the evaluation:

```bash
lm_eval --model hf \
    --model_args pretrained=eleutherai/pythia-70m \
    --tasks gsm8k \
    --device cuda:0 \
    --batch_size 8
```

## Technical examples

### Example Problem
A typical GSM8K problem involves multiple steps:

> **Question**: Janet has 30 apples. She gives 10 to her neighbor and then buys 15 more. How many apples does she have now?
> **Reasoning**:
> 1. Janet starts with 30.
> 2. She gives away 10: 30 - 10 = 20.
> 3. She buys 15 more: 20 + 15 = 35.
> **Answer**: 35

### Evaluation with Chain-of-Thought
Prompting models with `Let's think step by step` often significantly improves GSM8K scores:

```text
Q: [GSM8K Question]
A: Let's think step by step.
[Model generates reasoning steps]
Therefore, the answer is [Number].
```

## Related tools / concepts
- [MATH Benchmark](math-benchmark.md)
- [ASDiv](asdiv.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [SWE-bench](swe-bench.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [GPQA](gpqa.md)
- [MMLU](mmlu.md)

## Sources / references
- [OpenAI GSM8K GitHub Repository](https://github.com/openai/grade-school-math)
- [Arxiv: Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
