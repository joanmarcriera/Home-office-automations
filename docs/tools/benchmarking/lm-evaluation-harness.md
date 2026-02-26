# LM Evaluation Harness

## What it is
LM Evaluation Harness is a framework for few-shot evaluation of autoregressive language models. It provides a unified interface for evaluating models on hundreds of different tasks, including MMLU, ARC, HellaSwag, and many more.

## What problem it solves
Eliminates the need to implement individual benchmark evaluation pipelines by providing a single, standardized framework that supports hundreds of evaluation tasks out of the box.

## Where it fits in the stack
**Benchmarking**. Serves as a comprehensive evaluation framework for running multiple benchmarks against language models.

## Typical use cases
- Running standardized evaluations across many benchmarks with a single tool
- Comparing local or fine-tuned models against published results
- Building custom evaluation suites for internal model assessment

## Strengths
- Supports hundreds of evaluation tasks in a unified interface
- Widely adopted by the open-source LLM community
- Extensible with custom tasks and metrics

## Limitations
- Primarily designed for autoregressive models; may not suit all architectures
- Running many benchmarks can be computationally expensive
- Configuration can be complex for custom evaluation setups

## When to use it
- When you need to evaluate a model across many standard benchmarks at once
- When comparing a fine-tuned model against baseline results

## When not to use it
- When you only need a single, specific benchmark (run that benchmark directly)
- When benchmarking inference speed rather than model quality

## Related tools / concepts
- [OpenCompass](https://opencompass.org.cn/)
- [HELM](https://crfm.stanford.edu/helm/lite/)

## Sources / references
- [GitHub Repository](https://github.com/EleutherAI/lm-evaluation-harness)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
