# Chatbot Arena (LMSYS)

## What it is
Chatbot Arena is a crowdsourced open platform for evaluating LLMs through human preference. Developed by LMSYS (Large Model Systems Organization), it uses an Elo rating system based on pairwise comparisons where humans vote for the better response from two anonymous models. Its key metric is the Elo Rating, representing the relative skill level of a model based on thousands of matches.

## What problem it solves
Provides a human-preference-based ranking of LLMs that captures subjective quality differences not easily measured by automated benchmarks. It counters "benchmark contamination" by using blind human testing on unpredictable user prompts.

## Where it fits in the stack
**Benchmarking**. Serves as a reference leaderboard for comparing LLM quality based on real human judgments and "vibe" checks.

## Typical use cases
- Comparing the conversational quality of different LLMs before selecting one for deployment
- Tracking how new model releases rank against established models (e.g., GPT-4 vs. Claude 3.5)
- Validating whether automated benchmark scores (like MMLU) align with human preferences

## Strengths
- Based on real human preferences rather than synthetic metrics
- Large-scale crowdsourced evaluation provides statistical robustness
- Covers a wide range of models and is continuously updated
- Dynamic leaderboards for specific categories (Coding, Hard Prompts, Long Context)

## Limitations
- Results depend on the demographics and preferences of the crowd
- Does not measure specific capabilities like code generation or math in isolation (though category slices help)
- No way to run it locally or privately on your own models for the main leaderboard
- Potential for "style" bias where models with more verbose or polite formatting score higher

## When to use it
- When deciding which hosted LLM to use and human-perceived quality matters most
- When validating whether a model that scores well on automated benchmarks also "feels" good to users
- For tracking state-of-the-art (SOTA) progress in the LLM landscape

## When not to use it
- When you need to benchmark local or private models not listed on the platform
- When you need domain-specific evaluation for niche technical tasks
- For rigorous safety or alignment testing (dedicated benchmarks are better)

## Getting started

Users can participate in the arena by visiting the LMSYS website and entering prompts. For developers, the leaderboard data is often available for analysis.

1. Visit [arena.lmsys.org](https://arena.lmsys.org/).
2. Enter a prompt in the "Side-by-side" mode.
3. Compare Model A and Model B responses.
4. Vote for the better response (or a tie).

## Technical examples

### Elo Rating Calculation
The platform uses the standard Elo rating system. After a match between Model A (rating $R_A$) and Model B (rating $R_B$), the expected score $E_A$ for Model A is:

$$E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}$$

Ratings are updated based on the actual outcome vs. the expected outcome.

### Accessing Leaderboard via API
While the voting is human-based, the leaderboard data can sometimes be queried or downloaded via the Hugging Face dataset:

```python
from datasets import load_dataset

# Load the Chatbot Arena Conversations dataset
dataset = load_dataset("lmsys/chatbot_arena_conversations")
print(dataset['train'][0])
```

## Related tools / concepts
- [AlpacaEval](alpaca-eval.md)
- [MT-Bench](mt-bench.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [SWE-bench](swe-bench.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [MMLU](mmlu.md)
- [GPQA](gpqa.md)
- [OpenAI](../ai_knowledge/openai.md)
- [Anthropic](../providers/anthropic.md)
- [Google Gemini](../ai_knowledge/google-gemini.md)
- [Meta Llama](https://llama.meta.com/)

## Sources / references
- [LMSYS Chatbot Arena](https://arena.lmsys.org/)
- [LMSYS Leaderboard](https://arena.lmsys.org/leaderboard)
- [LMSYS Org GitHub](https://github.com/lm-sys)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high
