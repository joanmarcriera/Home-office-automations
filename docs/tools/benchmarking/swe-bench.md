# SWE-bench

## What it is
SWE-bench is a benchmark for evaluating LLMs on real-world software engineering tasks. It uses actual issues from GitHub and requires the model to generate a functional patch that passes existing tests.

## What problem it solves
Measures whether LLMs can perform practical software engineering work -- understanding codebases, diagnosing issues, and producing working fixes -- rather than just solving isolated coding puzzles.

## Where it fits in the stack
**Benchmarking**. Used as a reference benchmark for evaluating real-world software engineering capabilities of LLMs and AI agents.

## Typical use cases
- Evaluating AI coding agents on their ability to resolve real GitHub issues
- Comparing models on practical software engineering tasks
- Tracking progress of AI agents toward autonomous software development
- Choosing whether an agent is ready for repository-maintenance work that requires reading tests, editing files, and producing a valid patch
- Benchmarking frontier models like Claude 4.8 Opus (`claude-4-8-opus-20260528`) and GPT-5.5 on real-world engineering tasks

## Strengths
- Based on real-world GitHub issues, providing authentic evaluation
- Requires end-to-end engineering skills (reading code, understanding issues, writing patches)
- Validated by existing test suites from the source repositories

## Limitations
- Computationally expensive to run (requires setting up real repositories and test suites)
- Limited to Python repositories in the current dataset
- Pass rates can be influenced by the specific subset of issues selected
- Public leaderboard results do not automatically prove performance on private repositories, unusual stacks, or documentation-heavy maintenance work

## When to use it
- When evaluating AI agents or LLMs on real-world software engineering capability
- When comparing coding agents that claim to autonomously resolve issues

## When not to use it
- When evaluating basic code generation from specifications (use [HumanEval](human-eval.md) instead)
- When you need quick, lightweight benchmarking

## Getting started

SWE-bench requires a Docker environment to safely execute untrusted code and run test suites.

### 1. Installation
```bash
pip install swebench
```

### 2. Running an Evaluation (Inference)
Generate model predictions for a subset of issues:

```bash
python -m swebench.inference.run_api \
    --dataset_name princeton-nlp/SWE-bench_Lite \
    --model_name gpt-4-0613 \
    --output_dir ./predictions
```

### 3. Evaluating Predictions (Docker)
Use `swe-bench-docker` to execute the generated patches against the original repositories:

```bash
docker run -v $(pwd)/predictions:/predictions swebench/swe-bench-eval \
    --predictions /predictions/gpt-4-0613.jsonl \
    --output_dir /results
```

## CLI examples

### 1. Using SWE-bench Verified
The "Verified" subset consists of 500 tasks that have been human-verified to be solvable and have high-quality unit tests.

```bash
# List available instances in the Verified subset
python -m swebench.inference.run_api --dataset_name princeton-nlp/SWE-bench_Verified --list_instances
```

### 2. Run Evaluation on Single Instance
```bash
python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Verified \
    --instance_id django__django-11001 \
    --prediction_path ./predictions/django__django-11001.jsonl
```

### 3. Check Docker Environment
```bash
docker run swebench/swe-bench-eval --version
```

## API examples

### 1. Loading the Dataset
```python
from datasets import load_dataset

# Load the verified subset
dataset = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")

# Access a specific task
task = dataset[0]
print(f"Task ID: {task['instance_id']}")
```

### 2. Custom Evaluation Loop
For agentic workflows, you can integrate SWE-bench as a final validation step in your local environment.

```python
from swebench.harness.test_spec import make_test_spec
from swebench.harness.run_evaluation import run_instance

# Define task instance
instance = {
    "repo": "django/django",
    "pull_number": "12345",
    "instance_id": "django__django-12345",
    "base_commit": "abc123...",
    "patch": "diff --git a/django/db/models/fields/__init__.py...",
    "test_patch": "diff --git a/tests/model_fields/tests.py..."
}

# Run evaluation in Docker
spec = make_test_spec(instance)
result = run_instance(spec)

print(f"Resolved: {result['resolved']}")
```

## Practical evaluation notes

Use SWE-bench as a high-signal engineering benchmark, but interpret it as one part of an agent-readiness picture:

- **Patch correctness**: The benchmark rewards changes that satisfy existing test suites, which is useful for bug-fix agents but less direct for docs, taxonomy, and knowledge-base tasks.
- **Repository navigation**: Strong results imply the model or harness can locate relevant files, reason over issue text, and make coherent edits in a real repo.
- **Harness quality**: Tooling around the model matters. Search, edit, test execution, retries, and patch application can change outcomes as much as the base model.
- **Local validation**: For private repo adoption, run a small internal task set alongside SWE-bench-style metrics so results reflect local languages, CI shape, and review expectations.

## Agent comparison checklist

When using SWE-bench results to compare coding agents, record:

1. The exact benchmark split and date.
2. The model, agent harness, tool access, and retry budget.
3. Whether the run used public issue text only or any extra retrieval.
4. Pass rate plus failure classes: setup failure, wrong file, incomplete patch, flaky test, or unsafe behavior.
5. Cost per resolved issue, not only raw pass rate.

## Related tools / concepts

- [HumanEval](human-eval.md)
- [Terminal-Bench](terminal-bench.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [LongCLI-Bench](longcli-bench.md)
- [Aider](../development_ops/aider.md)
- [OpenHands](../development_ops/openhands.md)
- [Plandex](../development_ops/plandex.md)
- [Claude Code](../development_ops/claude-code-setup.md)
## Sources / references
- [Official Website](https://www.swebench.com/)
- [GitHub Repository](https://github.com/princeton-nlp/SWE-bench)
- [SWE-bench paper](https://arxiv.org/abs/2310.06770)
- [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)

## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high
