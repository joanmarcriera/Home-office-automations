# ARC (AI2 Reasoning Challenge)

## What it is
The AI2 Reasoning Challenge (ARC) is a dataset consisting of 7,787 genuine grade-school level, multiple-choice science questions. It is split into two subsets: "Easy" and "Challenge," where the latter contains questions that are difficult for both simple retrieval-based algorithms and word-frequency models.

## What problem it solves
ARC evaluates an LLM's ability to perform multi-hop reasoning and apply commonsense background knowledge. It was designed to move beyond surface-level pattern matching that characterized older benchmarks.

## Where it fits in the stack
**Benchmarking**. It is a standard dataset for evaluating the reasoning and knowledge capabilities of foundational models.

## Typical use cases
- Measuring scientific reasoning in AI models.
- Evaluating the effectiveness of reasoning techniques like Chain-of-Thought (CoT).
- Benchmarking progress in general-purpose AI intelligence.

## Strengths
- **Focus on Reasoning**: The "Challenge" set specifically targets questions that cannot be solved by simple search or statistical correlation.
- **Natural Language**: Uses real-world science questions written by humans.
- **Well-Established**: Widely recognized as a key metric for reasoning performance.

## Limitations
- **Scientific Focus**: Limited to scientific knowledge; does not cover other domains like law or medicine.
- **Multiple-Choice**: Does not evaluate open-ended generation or tool-use capabilities.

## When to use it
- When comparing the reasoning capabilities of different LLMs.
- When testing a model's grasp of grade-school level scientific concepts.

## When not to use it
- For evaluating specific domain expertise outside of science.
- For testing coding or mathematical performance (use [GSM8K](gsm8k.md) or [EvalPlus](evalplus.md) instead).

## Licensing and cost
- **Open Source**: Yes (CC BY-SA 4.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [MMLU](mmlu.md)
- [GPQA](gpqa.md)
- [GSM8K](gsm8k.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)

## Sources / References
- [AI2 ARC Website](https://allenai.org/data/arc)
- [GitHub Repository](https://github.com/allenai/ARC-benchmark)
- [Arxiv Paper](https://arxiv.org/abs/1803.05457)

## Contribution Metadata
- Last reviewed: 2026-03-30
- Confidence: high
