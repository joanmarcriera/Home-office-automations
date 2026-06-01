# Terminal-Bench

## What it is
Terminal-Bench is a benchmark for evaluating AI agents' ability to use a terminal. It focuses on tasks that require interacting with a real terminal environment, such as installing software, debugging system issues, and managing files.

## What problem it solves
Measures whether AI agents can effectively operate in a terminal environment, a critical capability for autonomous system administration and DevOps tasks.

## Where it fits in the stack
**Benchmarking**. Used to evaluate AI agents on terminal-based tasks that go beyond code generation.

## Typical use cases
- Evaluating AI agents on terminal interaction tasks (installation, debugging, file management)
- Comparing agent frameworks on their ability to operate in real system environments
- Assessing readiness of AI agents for autonomous system administration

## Strengths
- Tests practical, real-world terminal skills rather than abstract coding problems
- Covers a range of system administration tasks
- Complements code-generation benchmarks like SWE-bench

## Limitations
- Requires a real terminal environment for evaluation, adding setup complexity
- Results may vary depending on the operating system and environment configuration
- Relatively newer benchmark with a smaller community compared to established alternatives

## When to use it
- When evaluating AI agents that need to operate autonomously in terminal environments
- When assessing system administration or DevOps capabilities of AI agents

## When not to use it
- When evaluating pure code generation capabilities (use [HumanEval](human-eval.md) or [MBPP](mbpp.md))
- When you need a well-established benchmark with extensive published results

## Evaluation Methodology
Terminal-Bench (TB-2) uses the **Harbor** framework to provide a consistent, containerized execution environment. Each task is defined by:
1. **Scenario**: A Docker image containing the initial system state.
2. **Instruction**: A natural language prompt describing the goal.
3. **Validator**: A script that checks for successful completion (e.g., verifying a service is running or a file exists with specific content).

## Example Task Configuration
Tasks are typically structured as YAML or JSON objects within the Harbor framework:
```yaml
task_id: "nginx-load-balancer-config"
category: "networking"
difficulty: "hard"
scenario_image: "harbor/ubuntu-22.04-dev"
instruction: "Configure Nginx as a load balancer for two backend servers running on ports 8081 and 8082."
verification:
  type: "bash_script"
  script: "curl -s localhost | grep 'Backend'"
```

## Getting started

Terminal-Bench (TB-2) is typically run using the `tb` CLI tool and requires a Docker environment for sandboxed execution.

### 1. Installation
```bash
pip install terminal-bench
# or using uv
uv tool install terminal-bench
```

### 2. Running a Task
To run a specific task and evaluate an agent:
```bash
# List available tasks
tb list

# Run evaluation for a specific model on a task
tb run --task_id "setup-nginx-server" --model "anthropic/claude-3-5-sonnet"
```

### 3. Harbor Framework Integration
For large-scale evaluations, Terminal-Bench 2.0 uses the **Harbor** framework:
```python
from harbor import HarborSandbox, TerminalBenchTask

with HarborSandbox() as sandbox:
    task = TerminalBenchTask("debug-c-memory-leak")
    result = sandbox.execute_agent(task, agent_config="config.yaml")
    print(f"Task Completed: {result.success}")
```

## Related tools / concepts
- [SWE-bench](swe-bench.md)
- [BigCodeBench](./bigcodebench.md)
- [OpenHands](../agents/openhands.md)
- [Aider](../development_ops/aider.md)
- [Claude Code — Project Setup Guide](../development_ops/claude-code-setup.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [Harbor Framework](https://github.com/harbor-framework/harbor)
- [OSWorld](./os-world.md)
- [PA-bench](./pa-bench.md)

## Sources / references
- [GitHub Repository](https://github.com/harbor-framework/terminal-bench)
- [Terminal-Bench 2.0 (Harbor)](https://github.com/harbor-framework/terminal-bench-2)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high
