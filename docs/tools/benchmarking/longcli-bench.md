# LongCLI-Bench

## What it is
LongCLI-Bench is a preliminary benchmark and study focused on evaluating AI agents in long-horizon programming tasks within command-line interfaces (CLIs). It measures an agent's ability to plan and execute multi-step engineering workflows.

## What problem it solves
It addresses the gap in agent evaluation for realistic software engineering tasks. Most existing benchmarks are limited by short horizons, data contamination, or lack of fine-grained metrics. LongCLI-Bench tests agents on complex, multi-step tasks fromCS assignments and real-world workflows, highlighting failures in planning and long-term execution.

## Where it fits in the stack
**Eval**: It is a specialized benchmark for evaluating the **Agentic** and **Execution** layers of AI coding systems.

## Technical Capabilities
- **Long-Horizon Workflow Simulation**: Generates multi-step sequences requiring state preservation across shell turns.
- **Automated Grading**: Uses unit tests and environment state assertions to verify task completion.
- **Stalling Detection**: Measures agent "looping" or inactivity during complex planning phases.
- **Reference Plan Injection**: Supports studies on how partial human guidance affects agent performance.

## Typical use cases
- **Coding Assistant Benchmarking**: Testing tools like [Aider](../development_ops/aider.md) or [OpenHands](../development_ops/openhands.md) on complex, multi-tool tasks.
- **Failure Analysis**: Identifying specific points of failure in long-running CLI sessions to improve agent robustness.
- **Human-Agent Collaboration Study**: Evaluating how plan injection and guidance from humans can improve agent success rates.
- **Frontier Model Evaluation**: Evaluating the long-horizon reasoning capabilities of Claude 4.8 Opus (`claude-4-8-opus-20260528`) and GPT-5.5 in terminal environments.

## Strengths
- **Long-Horizon focus**: Specifically targets tasks that require sustained reasoning and multiple sequential actions.
- **Step-Level Scoring**: Pinpoints exactly where an agent stalls or deviates from the task requirements.
- **Realistic Tasks**: Includes "from scratch" development, feature addition, bug fixing, and refactoring scenarios.

## Limitations
- **CLI-Centric**: Focused on terminal interactions, which may not capture all agentic modalities.
- **Nascent Benchmark**: As a preliminary study, it may still be expanding its set of evaluation instances.

## When to use it
- When testing agents designed for autonomous coding or system administration.
- When you need a more rigorous evaluation of an agent's ability to follow complex, multi-step instructions without stalling.

## When not to use it
- For testing general chat capabilities or single-turn information retrieval.
- When evaluation does not involve terminal or shell access.

## Getting started

LongCLI-Bench requires a Python 3.10+ environment and access to the target agent's CLI.

### 1. Installation
```bash
pip install longcli-bench
```

### 2. Verify Installation
```bash
longcli --version
```

## CLI examples

### 1. Run Evaluation on a Specific Task
```bash
python run_eval.py --agent "aider" --task_id "refactor_001" --output_dir "./results"
```

### 2. List Available Tasks
```bash
longcli list-tasks --category refactoring
```

### 3. Show Results Summary
```bash
longcli show-results --dir ./results --format table
```

## API examples

> [!NOTE]
> As of June 2026, LongCLI-Bench primarily operates via CLI for terminal interaction testing. A stable Python API for programmatic task injection is under development.

### 1. Programmatic Task Loading (Preview)
```python
from longcli.bench import TaskLoader

loader = TaskLoader()
task = loader.get_task("refactor_001")
print(f"Task horizon: {task.horizon} steps")
```

## Related tools / concepts
- [SWE-bench](./swe-bench.md)
- [Terminal-Bench](./terminal-bench.md)
- [Aider](../development_ops/aider.md)
- [Plandex](../development_ops/plandex.md)
- [OpenHands](../development_ops/openhands.md)
- [Mentat](../development_ops/mentat.md)
- [Sweep](../development_ops/sweep_dev.md)
- [Claude Code](../development_ops/claude-code-setup.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)

## Sources / references
- [Hugging Face Paper Page](https://huggingface.co/papers/2602.14337)
- [arXiv Preprint (arXiv:2602.14337)](https://arxiv.org/abs/2602.14337)
- [LongCLI-Bench GitHub Repository](https://github.com/finyorko/longcli-bench)


## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high
