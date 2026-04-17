# MT-Bench

## What it is
MT-Bench is a multi-turn conversation benchmark designed to evaluate the chat capabilities of Large Language Models (LLMs). It uses a set of 80 high-quality multi-turn questions across eight common categories.

## What problem it solves
It addresses the limitation of single-turn benchmarks by testing an LLM's ability to maintain context, follow instructions across multiple turns, and handle follow-up questions, which is more representative of real-world human-AI interaction.

## Where it fits in the stack
**Benchmarking / Evaluation**. It is a key tool for assessing the conversational proficiency and instruction-following consistency of chat-tuned models.

## Typical use cases
- Evaluating model performance in multi-turn dialogues.
- Comparing the conversational abilities of different LLMs using LLM-as-a-judge.
- Testing context retention and follow-up handling in AI assistants.

## Strengths
- **Multi-turn Focus**: Specifically designed for conversational evaluation.
- **Diverse Categories**: Covers writing, roleplay, extraction, reasoning, math, coding, knowledge I (STEM), and knowledge II (humanities/social science).
- **LLM-as-a-Judge**: Uses strong models (like GPT-4) to grade responses, which has shown high correlation with human preferences.

## Limitations
- **Bias**: The judging model (e.g., GPT-4) may have its own biases or prefer its own style of output.
- **Cost**: Running evaluation with high-end models as judges can be expensive.
- **Static Dataset**: As models are trained on more data, there is a risk of benchmark contamination.

## When to use it
- When you need to assess how well a model handles follow-up questions and maintains context over a conversation.
- To benchmark chat-tuned models against industry leaders using a standardized methodology.

## When not to use it
- If you are only interested in single-turn performance or specific narrow tasks (like pure extraction without dialogue).
- If you lack access to a strong model to serve as the judge for automated grading.

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md)
- [AlpacaEval](alpaca-eval.md)
- [MMLU](mmlu.md)
- [LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)

## Sources / references
- [MT-Bench GitHub Repository](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge)
- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Paper)](https://arxiv.org/abs/2306.05685)

## Contribution Metadata
- Last reviewed: 2026-04-17
- Confidence: high
