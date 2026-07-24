# LiveCodeBench

## What it is
LiveCodeBench is a holistic, contamination-free benchmark for evaluating Large Language Models (LLMs) on complex coding tasks. It continuously collects new problems from premier competitive programming platforms (LeetCode, AtCoder, Codeforces) to ensure model evaluations are conducted on datasets completely absent from their pre-training windows.

## What problem it solves
Traditional coding benchmarks such as HumanEval and MBPP suffer from severe data contamination, as their problem definitions and test suites are widely indexed in pre-training corpora. LiveCodeBench provides a dynamic, time-indexed evaluation framework that assesses a model's true generalization, algorithmic reasoning, and real-time problem-solving abilities rather than its capacity for memory recall.

## Where it fits in the stack
**Eval / Benchmarking**. It serves as a critical, high-signal evaluation layer for validating newly trained foundational models, model alignment strategies, and autonomous coding agents. It integrates directly with execution frameworks to evaluate model performance across distinct temporal slices.

## Typical use cases
- **Frontier Model Evaluation**: Head-to-head coding capacity comparison between frontier models (e.g., Claude 5.1, GPT-5.5, Llama 4, Gemma 3, Qwen 3.6).
- **Contamination Diagnostics**: Identifying whether high performance on legacy benchmarks is inflated by pre-training memorization.
- **Holistic Code Assessment**: Evaluating models across three distinct scenarios: code generation, code execution reasoning (predicting program output), and automated debugging/self-repair.
- **Agentic Sandboxing**: Sandboxed runtime validation of agent-generated code using Model Context Protocol (MCP 3.1) execution servers.

## Strengths
- **Contamination-Free**: Continuous problem ingest from active competitive programming contests released post-2023.
- **Holistic Scenarios**: Goes beyond generation to test program comprehension (execution reasoning) and self-repair (debugging).
- **Time-Indexed Splits**: Enables testing of model generalization based on specific release dates relative to the model's knowledge cutoff.
- **Robust Test Cases**: Leverages highly optimized, comprehensive test suites curated by competitive programming platforms to minimize false positives.

## Limitations
- **Competitive Focus**: Emphasizes algorithmic, puzzle-like competitive programming rather than modular, repository-level software engineering.
- **Python-First Bias**: While the source platforms support diverse languages, the standardized evaluation pipeline is primarily optimized for Python execution.
- **Extremely High Difficulty**: Many problems are tuned for human competitive programmers, which can lead to low floor-level scores for non-frontier or base models.

## When to use it
- When measuring the "true" algorithmic code generation capability of newly launched instruction-tuned models.
- When evaluating a model's program-tracing and dry-run execution reasoning capabilities.
- To audit the performance of local, fine-tuned, or quantized open-weight code models over time.

## When not to use it
- For testing base foundation models that have not undergone instruction tuning or coding alignment.
- When the primary goal is to evaluate repository-wide, multi-file software engineering tasks (use [SWE-bench](swe-bench.md) instead).
- For benchmarking simple API interactions or basic web-application boilerplate code.

## Getting started
LiveCodeBench can be utilized via its public leaderboard or run locally by cloning the evaluation runner and preparing your execution environment.

### 1. Installation
Clone the repository and install the runner requirements. It is recommended to use a virtual environment or an MCP-sandboxed docker container.
```bash
git clone https://github.com/LiveCodeBench/LiveCodeBench
cd LiveCodeBench
pip install -r requirements.txt
```

### 2. Configure Environment
Set up credentials and configure API keys for your preferred LLM providers in a `.env` file:
```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
```

## CLI examples

### Running Baseline Code Generation
Evaluate code generation performance on problems released after a specific date slice using a frontier model:
```bash
python -m lcb_runner.evaluation.main \
    --model "anthropic/claude-5.1" \
    --scenario "codegeneration" \
    --start_date "2026-01-01" \
    --end_date "2026-07-01"
```

### Running Execution Reasoning
Measure the model's ability to predict the output of Python code snippets:
```bash
python -m lcb_runner.evaluation.main \
    --model "openai/gpt-5.5" \
    --scenario "execution" \
    --difficulty "Medium"
```

### Sandboxed Evaluation with Docker
Execute code evaluations in a secure dockerized container to prevent untrusted LLM code execution on host machines:
```bash
python -m lcb_runner.evaluation.main \
    --model "meta-llama/llama-4-70b-instruct" \
    --scenario "codegeneration" \
    --use_docker \
    --difficulty "Hard"
```

## API examples

### Schema of a LiveCodeBench Problem Instance
A typical problem instance returned by the LCB dataset loader contains comprehensive metadata:
```json
{
    "question_id": "lcb-2026-03-45",
    "title": "Subarray Sum Queries",
    "platform": "Codeforces",
    "release_date": "2026-03-15T14:30:00",
    "difficulty": "Hard",
    "question_content": "Implement a dynamic range query...",
    "test_cases": {
        "inputs": ["[[1, 2], [3, 4]]"],
        "outputs": ["[7]"]
    }
}
```

### Programmatic Ingestion and Run Hook
Load and filter LiveCodeBench datasets programmatically within custom evaluation workflows:
```python
from lcb_runner.utils.scenarios import Scenario
from lcb_runner.runner.parser import get_args
from lcb_runner.evaluation.main import run_eval_pipeline

# Initialize configuration programmatically
args = get_args()
args.model = "meta-llama/llama-4-70b-instruct"
args.scenario = Scenario.codegeneration
args.difficulty = "Medium"
args.use_docker = True

# Execute evaluation pipeline
# results = run_eval_pipeline(args)
# print(f"Pass@1 Accuracy: {results['pass_1']:.2f}")
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
- **Cost**: The software and dataset are entirely free. Running evaluations requires LLM provider API tokens or local compute resources.

## Sources / references
- [LiveCodeBench Official Website](https://livecodebench.github.io/)
- [LiveCodeBench GitHub Repository](https://github.com/LiveCodeBench/LiveCodeBench)
- [LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code (arXiv)](https://arxiv.org/abs/2403.07974)

## Contribution Metadata
- Last reviewed: 2026-07-31
- Confidence: high
