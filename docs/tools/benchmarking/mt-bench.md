# MT-Bench

## What it is
MT-Bench (Multi-Turn Benchmark) is a set of 80 high-quality multi-turn questions across eight categories, designed to evaluate the conversational and instruction-following abilities of Large Language Models (LLMs). It was developed by the LMSYS Org (the team behind the Chatbot Arena).

## What problem it solves
Most traditional benchmarks focus on single-turn interactions. However, real-world usage of LLMs often involves multiple turns where the model must maintain context, follow follow-up instructions, and refine its previous answers. MT-Bench specifically tests this "multi-turn" capability.

## Where it fits in the stack
**Benchmarking**. It is a key tool for evaluating the "chat" performance of models, sitting between static single-turn benchmarks and full human evaluation.

## Typical use cases
- **Multi-Turn Evaluation**: Assessing how well a model handles follow-up questions and context retention.
- **LLM-as-a-judge Testing**: Using a strong model (like GPT-4) to score the responses of other models on a scale of 1-10.
- **Model Comparison**: Benchmarking open-source chat models against proprietary ones in a conversational setting.

## Strengths
- **Multi-Turn Logic**: Specifically designed to test how models handle the second turn of a conversation.
- **Diverse Categories**: Covers Writing, Roleplay, Reasoning, Math, Coding, Extraction, STEM, and Humanities.
- **Scalable**: Uses an automated scoring system (LLM-as-a-judge) which is faster and cheaper than human evaluation.
- **Well-Aligned**: Scores show a high correlation (over 80%) with human preferences in the Chatbot Arena.

## Limitations
- **Judge Bias**: Relying on an LLM judge can introduce biases (e.g., preference for longer answers or specific styles).
- **Small Sample Size**: With only 80 questions, it provides a "snapshot" rather than an exhaustive evaluation.
- **Limited to 2 Turns**: While it tests multi-turn capability, it only evaluates two turns per question.

## When to use it
- When you are building a chatbot or conversational assistant and need to evaluate its dialogue flow.
- When you want to compare models' ability to follow complex, multi-step instructions in a chat format.

## When not to use it
- For evaluating purely factual knowledge (use [MMLU](mmlu.md)).
- For heavy coding-specific tasks where [BigCodeBench](bigcodebench.md) or [HumanEval](human-eval.md) are more appropriate.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free software/dataset, but requires payment for the judge LLM's API.
- **Self-hostable**: Yes, via the FastChat evaluation framework.

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md)
- [AlpacaEval](alpaca-eval.md)
- [HELM](helm.md)
- **FastChat**: The framework used to run MT-Bench.

## Sources / References
- [GitHub Repository (FastChat)](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge)
- [arXiv: Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)
- [Official Leaderboard](https://chat.lmsys.org/?leaderboard)

## Contribution Metadata
- Last reviewed: 2026-03-30
- Confidence: high
