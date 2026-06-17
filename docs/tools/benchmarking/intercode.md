# InterCode

## What it is
InterCode is an interactive benchmarking framework designed for evaluating Large Language Models (LLMs) in real-world programming and shell environments. It focuses on multi-turn interactions where the model can execute code or commands and receive feedback from the environment. It is a precursor to more advanced [agentic](../agents/index.md) benchmarks.

## What problem it solves
Standard static benchmarks (like [HumanEval](human-eval.md)) often fail to capture the interactive nature of software development. InterCode addresses this by providing an environment where models must reason over multiple steps, handle errors, and adapt based on actual execution results. It tests the "plan-execute-verify" loop essential for [self-healing agents](../../knowledge_base/self-healing-agent-research.md) and coding assistants like `claude-4-8-opus-20260528`.

## Where it fits in the stack
**Benchmarking / Agentic Evaluation**. It sits in the "agentic" evaluation space, testing the model's ability to act as a coding assistant or terminal agent. It is often used to validate the performance of [OpenHands](../development_ops/openhands.md) and [Aider](../development_ops/aider.md).

## Typical use cases
- **Evaluating Terminal Agents**: Measuring how well models like GPT-5.5 handle multi-step Bash/Shell tasks.
- **SQL Generation Benchmarking**: Testing SQL generation and execution capabilities using [Data Copilot](../../reference-implementations/data-copilot/README.md) patterns.
- **Multi-step Programming**: Benchmarking models on tasks that require iterative execution and feedback.
- **Skill Validation**: Validating [Claude skills](../../knowledge_base/patterns/skills-best-practices.md) in a sandboxed terminal environment.

## Strengths
- **Interactivity**: Models can "try and fail," mirroring human developer workflows and allowing for self-correction.
- **Diversity**: Supports multiple languages and environments, including Bash, SQL, and Python.
- **Realism**: Uses actual [Docker](../infrastructure/docker.md) containers for safe, reproducible, and realistic execution environments.
- **Standardized API**: Provides a Gym-like interface for easy integration with reinforcement learning workflows.

## Limitations
- **Complexity**: Harder to set up and maintain than static, text-only benchmarks.
- **Resource Intensive**: Requires significant compute to run multiple [Docker](../infrastructure/docker.md) containers for evaluation.
- **Environment Drift**: Sandboxed environments can become outdated relative to modern libraries and OS versions.

## When to use it
- When developing coding [agents](../agents/index.md) or terminal-based AI assistants that need to interact with a system.
- When you need to measure how well a model handles and recovers from real-world execution errors.
- For evaluating models on complex, multi-turn reasoning tasks in a technical domain.

## When not to use it
- For quick, "shallow" evaluations of general model intelligence (use [MMLU](mmlu.md) or [ARC](arc.md) instead).
- When you don't have the infrastructure or permissions to run Docker-based evaluations safely.

## Getting started

### Installation
InterCode requires [Docker](../infrastructure/docker.md) and Python 3.10+.

```bash
git clone https://github.com/princeton-nlp/intercode
cd intercode
pip install -r requirements.txt
```

### Running an Evaluation
1. Ensure the Docker daemon is running.
2. Select a dataset (e.g., Bash or SQL).
3. Run the evaluation script with your target model.

## CLI examples

### Bash Environment Evaluation
```bash
python -m intercode.run --env bash --data data/bash/sample.json
```

### SQL Environment Evaluation
```bash
python -m intercode.run --env sql --data data/sql/sample.json
```

## API examples

### Environment Interaction Loop (Python)
A typical interaction involves the agent receiving an observation and issuing a command.

```python
import gym
import intercode

# Initialize the Bash environment
env = gym.make('intercode-bash-v0')
observation = env.reset()

# Agent issues a command (e.g., from Claude 4.8 Opus)
action = "ls -la"
observation, reward, done, info = env.step(action)

print(f"Shell Output: {observation}")
```

### Task Specification (JSON)
Tasks are defined by their initial state and the "gold" verification script.

```json
{
  "task_id": "bash_001",
  "query": "Find all files larger than 100MB and delete them.",
  "setup": "mkdir test_files; fallocate -l 150M test_files/big.txt",
  "verification": "test ! -f test_files/big.txt"
}
```

## Related tools / concepts
- [SWE-bench](swe-bench.md) — for evaluating models on real-world GitHub issues
- [Terminal-Bench](terminal-bench.md) — a benchmark for terminal-based assistants
- [HumanEval](human-eval.md) — the baseline for static code generation
- [OpenHands](../development_ops/openhands.md) — an open-source platform for autonomous engineering
- [Docker](../infrastructure/docker.md) — the standard for isolated execution environments
- [Self-healing Agents](../../knowledge_base/self-healing-agent-research.md) — agents that fix their own errors
- [MMLU](mmlu.md) — for general multitask language understanding
- [Data Copilot](../../reference-implementations/data-copilot/README.md) — patterns for agentic data interaction

## Sources / references
- [GitHub Repository](https://github.com/princeton-nlp/intercode)
- [Research Paper (arXiv)](https://arxiv.org/abs/2306.14898)
- [InterCode: Interactive Code Generation Benchmark (Princeton NLP)](https://nlp.princeton.edu/intercode/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
