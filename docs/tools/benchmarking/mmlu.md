# MMLU (Massive Multitask Language Understanding)

## What it is
MMLU is a comprehensive benchmark designed to measure the general knowledge and problem-solving abilities of Large Language Models. It consists of approximately 16,000 multiple-choice questions across 57 subjects, including STEM, the humanities, social sciences, and more.

## What problem it solves
It provides a standardized way to evaluate a model's "world knowledge" and academic proficiency across a vast array of disciplines, moving beyond narrow tasks to assess broad intellectual capability.

## Where it fits in the stack
**Benchmarking**. It is one of the most widely cited benchmarks for comparing the general intelligence of different LLMs.

## Typical use cases
- **General Model Comparison**: Assessing which model has a broader knowledge base.
- **Tracking Progress**: Measuring how new model versions improve in general world knowledge.
- **Identifying Knowledge Gaps**: Analyzing performance across specific subjects (e.g., Law vs. Physics).

## Strengths
- **Breadth**: Covers a massive range of subjects, from elementary mathematics to professional law and medicine.
- **Industry Standard**: Almost every major LLM release includes MMLU scores.
- **Granularity**: Allows for fine-grained analysis of performance on specific topics.

## Limitations
- **Format**: Multiple-choice format doesn't capture open-ended reasoning or generation quality.
- **Data Contamination**: Due to its popularity, questions may have leaked into the training data of newer models.
- **Ambiguity**: Some questions and answers have been criticized for being ambiguous or containing errors.

## When to use it
- When you want a broad overview of a model's general knowledge and academic proficiency.
- When comparing the general "intelligence" level of various foundation models.

## When not to use it
- When you need to evaluate specific reasoning depth (use [GPQA](gpqa.md) instead).
- When evaluating coding performance (use [HumanEval](human-eval.md) or [SWE-bench](swe-bench.md) instead).

## Related tools / concepts
- [GPQA](gpqa.md)
- [HumanEval](human-eval.md)
- [ARC (AI2 Reasoning Challenge)](https://github.com/allenai/ARC-benchmark)
- [Humanity's Last Exam (HLE)](humanitys-last-exam.md)

## Sources / References
- [Original Paper (Hendrycks et al.)](https://arxiv.org/abs/2009.03300)
- [GitHub Repository](https://github.com/hendrycks/test)

## Contribution Metadata
- Last reviewed: 2026-04-06
- Confidence: high
