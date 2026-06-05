# LiveCodeBench

## What it is
LiveCodeBench is a holistic and contamination-free evaluation benchmark for Large Language Models (LLMs) specialized in code. It continuously collects new problems from periodic contests on platforms like LeetCode, AtCoder, and Codeforces to ensure that models are evaluated on unseen data.

## What problem it solves
Traditional benchmarks such as HumanEval or MBPP are static and have become heavily contaminated, as their problems are often included in the training sets of newer models. LiveCodeBench addresses this by using release dates to evaluate models only on problems published after their training cutoff, providing a truer measure of generalization.

## Where it fits in the stack
**Benchmarking / Evaluation**. It provides a dynamic signal for the capabilities of code-generation models and autonomous agents.

## Typical use cases
- **Contamination Analysis**: Measuring how much a model's performance on older benchmarks is due to memorization vs. generalization.
- **Holistic Capability Assessment**: Evaluating models not just on code generation, but also on self-repair, code execution, and test output prediction.
- **Model Comparison**: Ranking models (e.g., Claude 3.5 vs. GPT-4o) on the latest competitive programming challenges.

## Strengths
- **Contamination-Free**: Annotates problems with release dates, allowing for temporally-scoped evaluations.
- **Holistic**: Beyond generation, it tests execution, repair, and prediction.
- **Dynamic**: Continuously updated with new problems from active coding contest platforms.
- **Diverse**: Covers problems from multiple platforms (LeetCode, AtCoder, Codeforces).

## Limitations
- **Competitive Programming Focus**: Like many benchmarks, it heavily features algorithmic and data structure problems which may not fully represent general software engineering tasks.
- **Python Centricity**: While the platforms support many languages, most LLM evaluation focuses on the Python subset.

## When to use it
- When evaluating the "true" coding intelligence of a new model released after 2023.
- When you need to understand a model's ability to reason about code execution rather than just writing it.

## When not to use it
- For base models that have not undergone instruction tuning for coding tasks.
- If you require evaluation of large-scale repository-level software engineering (consider [SWE-bench](swe-bench.md) instead).

## Getting started
LiveCodeBench is primarily used as a leaderboard and a dataset for model evaluation. You can interact with it via its official website or by using the evaluation scripts provided in its GitHub repository.

## Technical examples

### Running Evaluation (CLI)
You can use the LiveCodeBench repository to evaluate a model's generations.

```bash
# Clone the repository
git clone https://github.com/LiveCodeBench/LiveCodeBench
cd LiveCodeBench

# Run evaluation for a specific model's output
python -m lcb_runner.evaluation.main \
    --model_name "your-model-id" \
    --scenario "codegeneration" \
    --release_date "2024-01-01"
```

### Data Structure (JSON)
Each problem in the benchmark includes metadata about its release date and platform.

```json
{
    "question_id": "1234",
    "title": "Example Problem",
    "platform": "LeetCode",
    "release_date": "2024-02-15",
    "difficulty": "Hard",
    "test_cases": [...]
}
```

## Licensing and cost
- **Open Source**: Yes (MIT License).
- **Cost**: Free to use (software and dataset).

## Related tools / concepts
- [HumanEval](human-eval.md)
- [MBPP](mbpp.md)
- [EvalPlus](evalplus.md)
- [BigCodeBench](bigcodebench.md)
- [SWE-bench](swe-bench.md)
- [Chatbot Arena](chatbot-arena.md)
- [Contamination Analysis](../../knowledge_base/model_comparison_and_evaluation.md)

## Sources / references
- [LiveCodeBench Official Website](https://livecodebench.github.io/)
- [LiveCodeBench GitHub Repository](https://github.com/LiveCodeBench/LiveCodeBench)
- [LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code (arXiv)](https://arxiv.org/abs/2403.07974)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high
