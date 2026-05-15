# Terminal-Bench

## What it is
Terminal-Bench is a benchmark suite for evaluating AI agents' ability to use a terminal effectively. It focuses on tasks that require interacting with a real shell environment, such as installing software, debugging system issues, managing files, and navigating complex directory structures.

## What problem it solves
It measures whether AI agents can effectively operate in a terminal environment—a critical capability for autonomous system administration and DevOps tasks. Unlike code-generation benchmarks, it evaluates the agent's ability to observe system state, handle CLI errors, and chain terminal commands to achieve a goal.

## Where it fits in the stack
**Benchmarking / Eval**. It provides a standardized environment and set of tasks to evaluate terminal-native agents before they are granted shell access in production environments.

## Typical use cases
- **Agent Benchmarking**: Evaluating AI agents on terminal interaction tasks (installation, debugging, file management).
- **Environment Stress Testing**: Comparing how agent frameworks handle different shell environments (bash, zsh) or operating systems.
- **Guardrail Validation**: Assessing whether an agent respects system constraints or identifies high-risk commands during task execution.

## Strengths
- **Practicality**: Tests real-world terminal skills rather than abstract algorithms.
- **Observability**: Forces agents to parse command output and adjust their strategy based on feedback.
- **Diversity**: Covers a wide range of tasks from basic file manipulation to complex software dependency resolution.

## Limitations
- **Environment Complexity**: Requires a real or containerized terminal environment, adding setup overhead.
- **Safety Risks**: Running autonomous agents in a terminal requires strict sandboxing (e.g., Docker) to prevent accidental system damage.
- **State Drift**: The system state can change between commands, requiring the agent to maintain an accurate internal model of the environment.

## When to use it
- When evaluating AI agents that need to operate autonomously in terminal environments (e.g., [Junie](../development_ops/junie-cli.md)).
- When assessing system administration or DevOps capabilities of a new model or agent architecture.

## When not to use it
- For evaluating pure code generation capabilities (use [HumanEval](human-eval.md) or [MBPP](mbpp.md)).
- When you lack a secure, sandboxed environment to run autonomous shell commands.

## Getting Started: CLI Usage

Terminal-Bench often utilizes a CLI (e.g., `tb`) to orchestrate tasks in a Docker-based sandbox.

```bash
# Install the terminal-bench harness
pip install terminal-bench

# List available tasks
tb list --category sysadmin

# Run a specific task with an agent
tb run --task-id "install-nginx-v1" --agent "my-terminal-agent" --sandbox docker

# View evaluation report
tb report --run-id "run_12345"
```

## Task Examples

| Task ID | Description | Success Criteria |
| :--- | :--- | :--- |
| `debug-python-path` | Fix a `ModuleNotFoundError` in a multi-repo setup. | Script runs successfully. |
| `disk-cleanup-01` | Identify and remove log files older than 30 days. | Disk space increased; no system files deleted. |
| `ssh-setup-key` | Generate and configure an SSH key for a remote host. | `ssh -T` returns success. |

## Related tools / concepts
- [SWE-bench](swe-bench.md)
- [InterCode](intercode.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [LongCLI-Bench](longcli-bench.md)
- [PA-bench](pa-bench.md)
- [Junie CLI (Terminal Agent)](../development_ops/junie-cli.md)

## Sources / references
- [GitHub Repository - Terminal-Bench](https://github.com/pro-puffin/terminal-bench)
- [Terminal-Bench: A Benchmark for Terminal Agents](https://arxiv.org/abs/2410.03505)

## Contribution Metadata

- Last reviewed: 2026-05-15
- Confidence: high
