# GPQA (Graduate-Level Google-Proof Q&A)

## What it is
GPQA is a challenging benchmark for evaluating high-level reasoning and knowledge in LLMs. It consists of 448 multiple-choice questions written by experts (PhD-level) in biology, physics, and chemistry. The questions are designed to be "Google-proof," meaning they are difficult even for non-expert humans to solve with access to the internet. Key metrics include accuracy (percentage of correct answers) and self-consistency (reasoning reliability).

## What problem it solves
Measures whether LLMs possess deep, expert-level scientific knowledge and reasoning that cannot be trivially looked up, providing a more rigorous assessment than general knowledge benchmarks.

## Where it fits in the stack
**Benchmarking**. Used as a reference benchmark for evaluating advanced reasoning in LLMs.

## Typical use cases
- Evaluating LLM performance on graduate-level scientific reasoning
- Comparing models on tasks that require genuine understanding rather than surface-level retrieval
- Assessing progress toward expert-level AI capabilities

## Strengths
- Questions are expert-written and verified to be genuinely difficult
- Covers multiple scientific disciplines
- Resistant to simple retrieval-based strategies

## Limitations
- Limited to 448 questions, which may not cover all scientific domains
- Focuses on biology, physics, and chemistry only
- Multiple-choice format may not fully capture open-ended reasoning ability

## When to use it
- When comparing LLMs on their ability to handle difficult, expert-level scientific questions
- When you need a benchmark that is resistant to memorization and search

## When not to use it
- When evaluating code generation or practical task completion
- When you need broad general-knowledge evaluation (use MMLU instead)

## Related tools / concepts
- [MMLU (Massive Multitask Language Understanding)](https://github.com/hendrycks/test)
- [ARC (AI2 Reasoning Challenge)](https://github.com/allenai/ARC-benchmark)

## Sources / references
- [Arxiv Paper](https://arxiv.org/abs/2311.12022)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
