# InterCode

## What it is
InterCode is an interactive benchmarking framework designed for evaluating Large Language Models (LLMs) in real-world programming and shell environments. It focuses on multi-turn interactions where the model can execute code or commands and receive feedback from the environment. It is a precursor to more advanced [agentic](../agents/README.md) benchmarks.

## What problem it solves
Standard static benchmarks (like [HumanEval](human-eval.md)) often fail to capture the interactive nature of software development. InterCode addresses this by providing an environment where models must reason over multiple steps, handle errors, and adapt based on actual execution results. It tests the "plan-execute-verify" loop essential for [self-healing agents](../../knowledge_base/self-healing-agent-research.md).

## Where it fits in the stack
**Benchmarking / Agentic Evaluation**. It sits in the "agentic" evaluation space, testing the model's ability to act as a coding assistant or terminal agent. It is often used to validate the performance of [OpenHands](../development_ops/openhands.md) and [Aider](../development_ops/aider.md).

## Typical use cases
- Evaluating LLM performance in Bash/Shell environments.
- Testing SQL generation and execution capabilities using [Data Copilot](../../reference-implementations/data-copilot/README.md) patterns.
- Benchmarking models on multi-step programming tasks that require execution feedback.
- Validating [Claude skills](../../knowledge_base/patterns/skills-best-practices.md) in a sandboxed terminal.

## Key Features
- **Interactive Loops**: Continuous feedback from the shell or database after every command.
- **Gym-like Interface**: Standardized API for reinforcement learning and evaluation.
- **Lightweight Containers**: Uses [Docker](../infrastructure/docker.md) to provide isolated and reproducible environments.
- **Multi-domain support**: Includes datasets for Bash, SQL, and Python.

## Strengths
- **Interactivity**: Models can "try and fail," mirroring human developer workflows.
- **Diversity**: Supports multiple languages and environments.
- **Realism**: Uses actual Dockerized environments for safe, reproducible execution.

## Limitations
- **Complexity**: Harder to set up than static, text-only benchmarks.
- **Resource Intensive**: Requires running [Docker](../infrastructure/docker.md) containers for evaluation.
- **Maintenance**: Environments can drift or become outdated relative to modern libraries.

## When to use it
- When developing coding [agents](../agents/README.md) or terminal-based AI assistants.
- When you need to measure how well a model handles real-world execution errors.

## When not to use it
- For quick, "shallow" evaluations of general model intelligence (use [MMLU](mmlu.md) instead).
- When you don't have the infrastructure to run Docker-based evaluations safely.

## Getting started

### Installation
InterCode requires [Docker](../infrastructure/docker.md) and Python.

```bash
git clone https://github.com/princeton-nlp/intercode
cd intercode
pip install -r requirements.txt

# Run a sample Bash evaluation
python -m intercode.run --env bash --data data/bash/sample.json
```

## Technical examples

### Environment Interaction Loop
A typical interaction in InterCode involves the agent receiving an observation and issuing a command.

```python
import gym
import intercode

# Initialize the Bash environment
env = gym.make('intercode-bash-v0')
observation = env.reset()

# Agent issues a command
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

## Maintenance & Troubleshooting
- **Docker Cleanup**: Running many evaluations can lead to orphaned containers. Use `docker system prune` regularly.
- **Timeout issues**: Complex tasks might require increasing the `timeout` parameter in the environment configuration.

## Related tools / concepts
- [SWE-bench](swe-bench.md)
- [Terminal-Bench](terminal-bench.md)
- [HumanEval](human-eval.md)
- [OpenHands](../development_ops/openhands.md)
- [Docker](../infrastructure/docker.md)
- [Self-healing Agents](../../knowledge_base/self-healing-agent-research.md)
- [MMLU](mmlu.md)
- [Data Copilot](../../reference-implementations/data-copilot/README.md)

## Sources / references
- [GitHub Repository](https://github.com/princeton-nlp/intercode)
- [Research Paper](https://arxiv.org/abs/2306.14898)
- [InterCode: Interactive Code Generation Benchmark (Princeton NLP)](https://nlp.princeton.edu/intercode/)

## Contribution Metadata
- Last reviewed: 2026-05-24
- Confidence: high
