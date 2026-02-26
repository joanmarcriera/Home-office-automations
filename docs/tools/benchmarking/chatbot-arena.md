# Chatbot Arena (LMSYS)

## What it is
Chatbot Arena is a crowdsourced open platform for evaluating LLMs through human preference. Developed by LMSYS, it uses an Elo rating system based on pairwise comparisons where humans vote for the better response from two anonymous models. Its key metric is the Elo Rating, representing the relative skill level of a model based on thousands of matches.

## What problem it solves
Provides a human-preference-based ranking of LLMs that captures subjective quality differences not easily measured by automated benchmarks.

## Where it fits in the stack
**Benchmarking**. Serves as a reference leaderboard for comparing LLM quality based on real human judgments.

## Typical use cases
- Comparing the conversational quality of different LLMs before selecting one for deployment
- Tracking how new model releases rank against established models
- Validating whether automated benchmark scores align with human preferences

## Strengths
- Based on real human preferences rather than synthetic metrics
- Large-scale crowdsourced evaluation provides statistical robustness
- Covers a wide range of models and is continuously updated

## Limitations
- Results depend on the demographics and preferences of the crowd
- Does not measure specific capabilities like code generation or math in isolation
- No way to run it locally or privately on your own models

## When to use it
- When deciding which hosted LLM to use and human-perceived quality matters most
- When validating whether a model that scores well on automated benchmarks also feels good to users

## When not to use it
- When you need to benchmark local or private models not listed on the platform
- When you need domain-specific evaluation (e.g., code, math, science)

## Related tools / concepts
- [AlpacaEval](https://github.com/tatsu-lab/alpaca_eval)
- [MT-Bench](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge)

## Sources / references
- [Chatbot Arena Website](https://chat.lmsys.org/)
- [Leaderboard](https://chat.lmsys.org/?leaderboard)

## Contribution Metadata

- Last reviewed: 2026-02-26
- Confidence: medium
