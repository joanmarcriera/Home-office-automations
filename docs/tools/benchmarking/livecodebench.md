# LiveCodeBench

## What it is
LiveCodeBench is a holistic benchmark for evaluating Large Language Models (LLMs) on coding tasks using a "contamination-free" approach. It continuously collects new problems from competitive programming platforms (LeetCode, AtCoder, Codeforces) to ensure models are tested on data they haven't seen during training.

## What problem it solves
Traditional coding benchmarks like HumanEval and MBPP suffer from data contamination, as their problems are widely available in pre-training datasets. LiveCodeBench provides a dynamic, time-indexed evaluation that measures a model's true generalization and reasoning abilities rather than its ability to recall training data.

## Where it fits in the stack
**Eval**. It is a critical tool for model providers and researchers to benchmark coding intelligence across time, specifically tracking performance on 'frontier' problems released after a model's knowledge cutoff.

## Typical use cases
- **Frontier Model Evaluation**: Comparing the coding capabilities of newly released models (e.g., Claude 4.8 vs. GPT-5.5).
- **Contamination Analysis**: Determining if a model's performance on older benchmarks is due to memorization.
- **Holistic Assessment**: Evaluating code generation, self-repair, and test-case generation in a unified framework.

## Strengths
- **Contamination-Free**: Problems are sourced from competitive programming contests released after model cutoffs.
- **Holistic**: Covers multiple scenarios including code generation, execution reasoning, and debugging.
- **Time-Indexed**: Allows for evaluating models based on the specific date a problem was released.
- **High Quality**: Leverages curated problems with comprehensive test cases from top competitive platforms.

## Limitations
- **Focus on Competitive Programming**: Less focus on large-scale repository-level software engineering tasks.
- **Python Centricity**: While the platforms support many languages, most LLM evaluation focuses on the Python subset.
- **High Difficulty**: Problems can be significantly harder than typical enterprise coding tasks.

## When to use it
- When evaluating the "true" coding intelligence of a new model released after 2023.
- When you need to understand a model's ability to reason about code execution rather than just writing it.
- To track progress in LLM coding capabilities over time.

## When not to use it
- For base models that have not undergone instruction tuning for coding tasks.
- If you require evaluation of large-scale repository-level software engineering (consider [SWE-bench](swe-bench.md) instead).
- For evaluating simple API usage or boilerplate generation.

## Getting started
LiveCodeBench is primarily used as a leaderboard and a dataset for model evaluation. You can interact with it via its official website or by using the evaluation scripts provided in its GitHub repository.

### 1. Installation
```bash
git clone https://github.com/LiveCodeBench/LiveCodeBench
cd LiveCodeBench
pip install -r requirements.txt
```

### 2. Setting up Credentials
Configure your LLM provider API keys in a `.env` file or as environment variables.

## CLI examples

### Running Evaluation
You can use the LiveCodeBench runner to evaluate a model's generations.
```bash
python -m lcb_runner.evaluation.main \
    --model_name "openai/gpt-5.5" \
    --scenario "codegeneration" \
    --release_date "2026-01-01"
```

### Filtering by Difficulty
Run evaluation on a specific difficulty tier:
```bash
python -m lcb_runner.evaluation.main \
    --model_name "anthropic/claude-4.8" \
    --scenario "codegeneration" \
    --difficulty "Hard"
```

### Execution Reasoning
Evaluate the model's ability to predict the output of a given code snippet:
```bash
python -m lcb_runner.evaluation.main \
    --model_name "openai/gpt-5.5" \
    --scenario "execution"
```

## API examples

### Data Structure (JSON)
Each problem in the benchmark includes metadata about its release date and platform.
```json
{
    "question_id": "1234",
    "title": "Example Problem",
    "platform": "LeetCode",
    "release_date": "2026-02-15",
    "difficulty": "Hard",
    "test_cases": [...]
}
```

### Programmatic Access
```python
from lcb_runner.utils.scenarios import Scenario
from lcb_runner.runner.parser import get_args

# Conceptual example of initializing a runner
args = get_args()
args.model = "openai/gpt-5.5"
args.scenario = Scenario.codegeneration

# Execute evaluation
# (Requires local LCB repository setup)
```

## Related tools / concepts
- [HumanEval](human-eval.md) — The legacy standard for Python code generation.
- [MBPP](mbpp.md) — Mostly Basic Python Problems benchmark.
- [EvalPlus](evalplus.md) — Enhancing benchmarks with automated test case generation.
- [BigCodeBench](bigcodebench.md) — Evaluating LLMs on complex, library-heavy coding tasks.
- [SWE-bench](swe-bench.md) — Software engineering benchmark for resolving GitHub issues.
- [Chatbot Arena](chatbot-arena.md) — Human-centric evaluation of LLM capabilities.
- [Terminal-Bench](./terminal-bench.md) — Evaluation of LLM-to-shell interaction.
- [Inspect AI](./inspect-ai.md) — General evaluation framework supporting coding tasks.

## Licensing and cost
- **Open Source**: Yes (MIT License).
- **Cost**: Free to use (software and dataset). Requires LLM API credits for model evaluation.

## Sources / references
- [LiveCodeBench Official Website](https://livecodebench.github.io/)
- [LiveCodeBench GitHub Repository](https://github.com/LiveCodeBench/LiveCodeBench)
- [LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code (arXiv)](https://arxiv.org/abs/2403.07974)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
