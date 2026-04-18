# MT-Bench

## What it is
MT-Bench is a benchmark designed to evaluate the multi-turn conversational capabilities of Large Language Models (LLMs). It consists of 80 high-quality, multi-turn questions across eight categories: writing, roleplay, extraction, reasoning, math, coding, knowledge I (STEM), and knowledge II (humanities/social science).

## What problem it solves
Many traditional benchmarks only evaluate single-turn responses, failing to capture a model's ability to maintain context, follow instructions across multiple exchanges, and handle the dynamic nature of real-world conversations.

## Where it fits in the stack
**Benchmarking**. It is a core component of the LMSYS FastChat evaluation framework, providing a more rigorous test of conversational flow than single-turn evaluations.

## Typical use cases
- **Conversational AI Evaluation**: Assessing how well a chatbot handles follow-up questions and maintains context.
- **Model Comparison**: Ranking chat-tuned models based on their ability to handle complex, multi-step instructions.
- **LLM-as-a-Judge Validation**: MT-Bench is often used with GPT-4 as a judge to provide automated, scalable scoring that correlates with human judgment.

## Strengths
- **Multi-turn Focus**: Specifically designed to test conversation depth.
- **Diverse Categories**: Covers a wide range of tasks from coding to roleplay.
- **Strong Human Correlation**: GPT-4 based scoring on MT-Bench shows over 80% agreement with human experts.
- **Open Dataset**: The questions and human judgments are publicly available for research.

## Limitations
- **Judge Bias**: If using an LLM as a judge, it may inherit the biases of that judge (e.g., preference for certain styles or lengths).
- **Scale**: With 80 questions, it is smaller than some "massive" benchmarks, though the multi-turn nature adds complexity.
- **Static Nature**: Like all fixed benchmarks, it risks data contamination over time.

## When to use it
- When evaluating chat-tuned models where multi-turn interaction is a primary use case.
- When you need an automated conversational benchmark that aligns closely with human preference.

## When not to use it
- For evaluating base (non-chat-tuned) models that are not designed for dialogue.
- When you only need to measure narrow technical capabilities like raw code execution or mathematical proof (use specialized benchmarks instead).

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md)
- [AlpacaEval](alpaca-eval.md)
- [GSM8K](gsm8k.md)
- [HumanEval](human-eval.md)

## Sources / references
- [FastChat GitHub (LLM Judge)](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge)
- [MT-Bench Paper: "Judging LLM-as-a-judge" (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
- [LMSYS Leaderboard](https://arena.lmsys.org/leaderboard)

## Contribution Metadata
- Last reviewed: 2026-04-08
- Confidence: high
