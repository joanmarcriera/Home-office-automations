# Humanity's Last Exam (HLE)

## What it is
HLE is a benchmark designed to test the limits of LLMs on the most difficult human-level tasks. It consists of 3,000 highly complex, multi-disciplinary questions across over a hundred subjects (Mathematics, Physics, Biology, Humanities, etc.). Created by the Center for AI Safety (CAIS) and Scale AI, it represents a "frontier" benchmark where current state-of-the-art models still perform poorly, often achieving near-zero accuracy on its hardest subsets.

## What problem it solves
Addresses the "saturation" of existing benchmarks like MMLU and GPQA. As frontier models reach or exceed human-level performance on older tests, those tests lose their utility as measurement tools. HLE provides a new ceiling, ensuring that progress toward expert-level reasoning remains measurable.

## Where it fits in the stack
**Benchmarking**. Serves as a high-difficulty knowledge and reasoning benchmark for evaluating the upper limits of LLM and multi-modal model capabilities.

## Typical use cases
- **Frontier Model Evaluation**: Comparing the reasoning capabilities of state-of-the-art models (GPT-4o, Claude 3.5 Sonnet, Llama 3.1 405B).
- **Multi-modal Assessment**: Testing models on questions that require both textual reasoning and image understanding (14% of the dataset is multi-modal).
- **Calibration Testing**: Measuring whether models accurately estimate their own confidence in their answers.

## Strengths
- **Extreme Difficulty**: Designed to be the "last academic exam," remaining challenging even as models improve.
- **Closed-ended & Verifiable**: Answers are precise, allowing for automated, low-cost evaluation.
- **Subject Diversity**: Covers over 100 subjects with questions sourced from world-class experts.
- **Private Set**: Includes a held-out private set to combat data contamination and benchmark hacking.

## Limitations
- **Not for Everyday Tasks**: Does not measure "helpful assistant" capabilities or basic instruction following.
- **Low Signal for Small Models**: Smaller or older models often score near zero, making it difficult to distinguish between them.
- **Requires LLM Judge**: While answers are closed-ended, the variety of possible formats (decimals vs. fractions) often requires an LLM judge for automated scoring.

## When to use it
- When evaluating frontier models on the hardest available reasoning tasks.
- When existing benchmarks like MMLU or GPQA show signs of saturation (models scoring >90%).
- When testing a model's ability to handle world-class scientific or mathematical problems.

## When not to use it
- When evaluating models for general-purpose chat or basic RAG tasks.
- When you need a lightweight, fast-running benchmark for early-stage development.
- When you are optimizing for speed or low-cost inference rather than peak intelligence.

## Getting started (CLI Example)

HLE can be run using the UK Government's [Inspect](https://ukgovernmentbeis.github.io/inspect_evals/) framework.

```bash
# Install inspect and the evals package
pip install inspect-ai inspect_evals

# Run the HLE benchmark against an OpenAI model
inspect eval inspect_evals/hle --model openai/gpt-4o
```

### Evaluation Format
Models are typically prompted to provide their response in a structured format to facilitate judging:

```text
Explanation: {detailed reasoning}
Answer: {final exact answer}
Confidence: {0-100%}
```

## Related tools / concepts

- [GPQA](gpqa.md) - Graduate-level Google-proof Q&A.
- [MMLU](mmlu.md) - Massive Multitask Language Understanding.
- [ARC (AI2 Reasoning Challenge)](arc.md) - Challenging questions for reasoning.
- [GSM8K](gsm8k.md) - Grade school math word problems.
- [Chatbot Arena](chatbot-arena.md) - Crowdsourced ELO ratings for LLMs.
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md) - Agentic evaluation framework.
- [SWE-bench](swe-bench.md) - Software engineering benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Unified framework for running multiple benchmarks.

## Sources / references
- [Hugging Face Dataset (cais/hle)](https://huggingface.co/datasets/cais/hle)
- [Scale Labs Leaderboard](https://labs.scale.com/leaderboard/humanitys_last_exam)
- [Humanity's Last Exam - arXiv Paper](https://arxiv.org/abs/2501.14249)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high
